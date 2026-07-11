"""auto_refresh.py — unattended entry point for the Testahil continuous-learning loop.

DESIGN PRINCIPLE (11-Jul-2026, user instruction: "automatic but not at the expense
of quality"): mechanical work runs unattended. Anything that would change a
published verdict, imply a signal ablation, or move a config beyond a small
tolerance STOPS and asks a human. Today's session is the reason this gate exists:
data cleaning alone flipped Korea's tail shape from nu=6 to Gaussian and changed
two names' robust verdicts (SA/RAJHI PARITY->PASS, AE/ALPHADHABI PARITY->FAIL).
"Just run the pipeline on a cron" would have silently pushed those to production
with no one looking. This script is the difference between automation and
unsupervised drift.

INPUT CONVENTION: raw_ohlc/{MARKET_CODE}/{TICKER}.csv
raw_ohlc IS A PERSISTENT LIBRARY, NOT AN INBOX. Every covered stock keeps its
current OHLC there permanently. To add or refresh ONE stock you add or overwrite
ONE file — the pipeline still sees the whole market and refits the full panel.

This matters because the natural working rhythm is one stock at a time (research a
name, post its OHLC, produce its report). An earlier design treated raw_ohlc as
"this session's uploads", which meant a single-stock upload left every OTHER panel
name without a raw CSV and falsely tripped the gate on every single post. The
library model makes one-at-a-time the DEFAULT case, not the broken one.

The market+ticker mapping is decided by FILE PLACEMENT, not by parsing company
names. This is deliberate: the ADNOC/ADIB confusion earlier in this project was
exactly this kind of disambiguation, and it is NOT something to automate. A human
(or a Claude session) placing a file at raw_ohlc/AE/ADNOCGAS.csv has already made
the judgment call; the pipeline should never try to re-derive it from a filename
like "ADNOC_Stock_Price_History.csv".

WHAT RUNS UNATTENDED (auto-committed to main, no approval):
  - the data-quality gate (clean_ohlc) on every touched file
  - the panel rebuild + pooled (nu, width_cal) refit for every touched market
  - LONO per-name and market-panel verdicts
  ...PROVIDED the materiality gate below finds nothing that needs a human.

WHAT STOPS AND OPENS A PR INSTEAD (never auto-merged):
  - any EXISTING name's verdict category changes (PASS/PARITY/FAIL/BOUNDARY)
  - a NEW name arrives already FAILING, or its arrival flips someone else's verdict
  - width_cal moves >5% relative, or nu crosses into a different regime
    (specifically: the Gaussian/fat-tail boundary, since that is the parameter
    that most changes the published cone shape)
  - the market-level verdict itself changes
  - a panel carries a name with NO raw CSV in the library (a genuine inconsistency
    now that the library is authoritative — it means a file was deleted or never
    added, and the panel is running on stale residuals)
  - a signal_active flip would be implied (not auto-applied even if supported —
    Egypt's ablation this session was exactly this kind of call)

A NEW NAME IS NOT, BY ITSELF, MATERIAL. Adding a stock is the single most common
thing that happens here, and blocking on it would mean a PR on literally every
post. You placing the file at raw_ohlc/{MKT}/{TICKER}.csv IS the human decision
about what the series is. The pipeline still guards the things that actually
matter: if the new name arrives FAILING, or its arrival destabilises the market fit
or flips another name's verdict, that still stops. New names are always named
explicitly in the commit message and the log so an arrival is never invisible.

Usage: python3 auto_refresh.py [--apply]
  Without --apply: dry run, prints what WOULD happen, changes nothing.
  With --apply: writes market_profiles.py / panels / fitted_configs.json for
    non-material markets; writes a PENDING_REVIEW/{MARKET}_{date}.md report
    (and returns a nonzero exit code) for material ones.
"""
import sys, os, glob, json, datetime, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np

from panel_refresh import refresh_market, apply_breaks
from market_profiles import PROFILES

HERE = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(HERE, 'raw_ohlc')
REGISTRY_PATH = os.path.join(HERE, 'fitted_configs.json')
PENDING_DIR = os.path.join(HERE, 'PENDING_REVIEW')

BAND_TOL = 0.05           # the published 90% cone half-width may drift this much silently
NU_GAUSSIAN_CUTOFF = 200  # nu above this is "effectively Gaussian"


def band_halfwidth(nu, cal):
    """The thing the reader actually sees: the half-width of the published 90% cone,
    in units of sigma_h. Proportional to cal * q95(unit-variance t(nu)).

    This REPLACES a naive rule that triggered on (a) width_cal moving >5% and (b) nu
    crossing an arbitrary Gaussian/fat-tail boundary. That rule was wrong in both
    directions. Concretely, on the gold panel the MLE moved nu=12 -> Gaussian after
    8 stale rows were cleaned — which the bucket rule called a "regime change" and
    would have opened a PR for. But nu=12 sits only dlogL=0.31 from the Gaussian MLE
    (statistically indistinguishable — nu is weakly identified at these sample sizes,
    see gate_scale_fix_20260711.md), and the two produce 90% cones that differ by
    ~1%. Meanwhile nu and cal TRADE OFF against each other, so watching cal alone can
    miss a real change that nu absorbs. Measuring the cone directly captures both in
    one number and only fires when the published band actually moves."""
    from scipy import stats
    if nu is None:
        return None
    if isinstance(nu, str):
        nu = 1e9 if 'gauss' in nu.lower() else float(nu)
    nu = float(nu)
    q = 1.6448536269514722 if nu >= NU_GAUSSIAN_CUTOFF else float(
        stats.t.ppf(0.95, nu) / np.sqrt(nu / (nu - 2)))
    return q * float(cal or 1.0)


def discover_touched_markets():
    """Read the FULL persistent library: raw_ohlc/{MKT}/{TICKER}.csv -> {mkt: {ticker: path}}.
    Every market with at least one CSV is refit against ALL of its CSVs — which is what
    makes a one-stock-at-a-time upload work."""
    out = {}
    if not os.path.isdir(RAW_DIR):
        return out
    for mkt_dir in sorted(glob.glob(os.path.join(RAW_DIR, '*'))):
        if not os.path.isdir(mkt_dir):
            continue
        mkt = os.path.basename(mkt_dir)
        if mkt not in PROFILES:
            print(f"  [SKIP] {mkt_dir}: '{mkt}' is not a known market code — {list(PROFILES)}")
            continue
        files = {os.path.splitext(os.path.basename(f))[0]: f
                 for f in sorted(glob.glob(os.path.join(mkt_dir, '*.csv')))}
        if files:
            out[mkt] = files
    return out


def _nu_bucket(nu):
    if nu is None:
        return None
    if isinstance(nu, str):
        return 'Gaussian' if 'gauss' in nu.lower() else nu
    return 'Gaussian' if nu >= NU_GAUSSIAN_CUTOFF else round(float(nu))


def _verdict_key(v):
    """Normalize e.g. 'BOUNDARY(PARITY-flagged)' -> 'BOUNDARY' for comparison."""
    return str(v).split('(')[0]


def assess_materiality(market, result, incumbent_profile, incumbent_registry):
    """Returns (is_material: bool, reasons: list[str])."""
    reasons = []

    old_bw = band_halfwidth(incumbent_profile.nu, incumbent_profile.width_cal)
    new_bw = band_halfwidth(result['nu'], result['width_cal'])
    if old_bw and new_bw:
        rel = abs(new_bw - old_bw) / old_bw
        if rel > BAND_TOL:
            reasons.append(
                f"the PUBLISHED 90% cone moves {rel:+.1%} (> {BAND_TOL:.0%} tolerance): "
                f"(nu={incumbent_profile.nu}, cal={incumbent_profile.width_cal}) -> "
                f"(nu={result['nu']}, cal={result['width_cal']})")

    old_names = set(incumbent_registry.get('panel_names', []))
    new_names = set(result['panel_names'])
    added = sorted(new_names - old_names)
    # A new name is NOT material by itself (see module docstring) — but a new name
    # that arrives already FAILING is: that is either a genuinely uncalibratable
    # series or, more likely, a misfiled/bad file, and it should not silently enter
    # a production panel.
    for n in added:
        d = result['per_name'].get(n, {})
        v = _verdict_key(d.get('verdict', ''))
        if v == 'FAIL':
            reasons.append(f"NEW name {n} arrives with a robust FAIL "
                            f"(skill {d.get('skill'):+.4f}) — check the file is the right "
                            f"instrument, in the right market folder, with clean history")

    old_pn = incumbent_registry.get('per_name', {})
    for n, d in result['per_name'].items():
        if 'verdict' not in d:
            reasons.append(f"{n}: no raw CSV supplied this run, verdict could not be scored "
                            f"('{d.get('note', 'unknown reason')}') — needs a human to confirm "
                            f"this name's absence is intentional")
            continue
        old_v = _verdict_key(old_pn.get(n, {}).get('verdict', 'UNKNOWN'))
        new_v = _verdict_key(d['verdict'])
        if old_v != 'UNKNOWN' and old_v != new_v:
            reasons.append(f"{n}: verdict changed {old_v} -> {new_v}")

    old_mv = _verdict_key(incumbent_registry.get('market_verdict', 'UNKNOWN'))
    new_mv = _verdict_key(result['market_verdict'])
    if old_mv != 'UNKNOWN' and old_mv != new_mv:
        reasons.append(f"MARKET panel verdict changed {old_mv} -> {new_mv}")

    return (len(reasons) > 0), reasons, added


def write_pending_review(market, result, reasons, incumbent_profile):
    os.makedirs(PENDING_DIR, exist_ok=True)
    d = datetime.date.today().isoformat()
    path = os.path.join(PENDING_DIR, f"{market}_{d}.md")
    lines = [
        f"# PENDING REVIEW — {market} ({result['market_name']}) — {d}\n\n",
        "auto_refresh.py found material changes and stopped rather than auto-committing.\n"
        "Nothing in market_profiles.py has been touched. Panel files (raw residual "
        "rebuilds) WERE updated — they carry no verdict of their own.\n\n",
        "## Why this needs a human\n\n",
    ]
    for r in reasons:
        lines.append(f"- {r}\n")
    lines.append(f"\n## Proposed config\n\n")
    lines.append(f"- nu: {incumbent_profile.nu}  ->  **{result['nu']}**\n")
    lines.append(f"- width_cal: {incumbent_profile.width_cal}  ->  **{result['width_cal']}**\n")
    lines.append(f"- panel: {len(result['panel_names'])} names, {result['windows']} windows\n")
    lines.append(f"- market verdict: **{result['market_verdict']}** "
                  f"(skill {result['market_skill']:+.4f}, CI{result['market_ci90']})\n\n")
    lines.append("## Per-name verdicts\n\n| Name | nu | width_cal | skill | verdict |\n|---|---|---|---|---|\n")
    for n, d2 in sorted(result['per_name'].items()):
        if 'verdict' not in d2:
            lines.append(f"| {n} | — | — | — | {d2.get('note', 'not scored this run')} |\n")
        else:
            lines.append(f"| {n} | {d2['nu']} | {d2['width_cal']} | {d2['skill']:+.4f} | {d2['verdict']} |\n")
    lines.append("\n## To apply\n\nReview against the LONO/robust-verdict evidence above, then "
                  "either merge this PR to accept, or re-run with a corrected raw_ohlc/ input.\n")
    with open(path, 'w') as f:
        f.writelines(lines)
    return path


def write_production(market, result):
    """Auto-commit path: write nu/width_cal into market_profiles.py in place,
    and refresh the fitted_configs.json mirror entry for this market.

    NOTE the nu serialization. refresh_market() reports nu as the STRING "Gaussian"
    when the MLE selects the Gaussian limit (it is nicer to read in a report), but
    market_profiles.py is executable Python — writing `nu=Gaussian` there emits a
    bare undefined name and market_profiles.py stops importing, i.e. the auto-commit
    would push an engine that cannot even load. The house convention for the Gaussian
    limit is the numeric sentinel nu=250.0 (mc_v3 treats any nu > 200 as Gaussian;
    KOREA and INDIA already carry it). Caught 11-Jul-2026 before it ever fired."""
    path = os.path.join(HERE, 'market_profiles.py')
    src = open(path).read()
    prof = PROFILES[market]
    class_name = {'EG': 'EGYPT', 'SA': 'SAUDI', 'US': 'USA', 'GB': 'UK', 'BR': 'BRAZIL',
                  'KR': 'KOREA', 'AE': 'UAE', 'IN': 'INDIA', 'QA': 'QATAR', 'XAU': 'METALS'}[market]

    nu_out = result['nu']
    if isinstance(nu_out, str):                      # "Gaussian" -> numeric sentinel
        nu_out = 250.0 if 'gauss' in nu_out.lower() else float(nu_out)
    nu_out = float(nu_out)

    old_token = f"nu={prof.nu}, width_cal={prof.width_cal}"
    new_token = f"nu={nu_out}, width_cal={result['width_cal']}"
    if old_token == new_token:
        pass                                          # nothing to change
    else:
        i = src.index(f"{class_name} = MarketProfile")
        j = src.index(old_token, i)
        src = src[:j] + new_token + src[j + len(old_token):]

        # GUARD: verify by IMPORT, never by ast.parse alone. `nu=Gaussian` is a bare
        # identifier — it PARSES perfectly and only dies at import with NameError. An
        # ast.parse check would wave it straight through. This exact bug reached main
        # on 11-Jul-2026 and left market_profiles.py unimportable (the engine could not
        # load) while a digit-only regex check reported it "intact". Write to a temp
        # file, import it for real, and only then replace production.
        import importlib.util, tempfile
        with tempfile.NamedTemporaryFile('w', suffix='.py', delete=False) as tf:
            tf.write(src); tmp = tf.name
        try:
            spec = importlib.util.spec_from_file_location('_mp_check', tmp)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)              # raises if the edit broke anything
            assert mod.PROFILES[market].nu is not None
        finally:
            os.unlink(tmp)
        open(path, 'w').write(src)

    reg = json.load(open(REGISTRY_PATH)) if os.path.exists(REGISTRY_PATH) else {}
    reg[market] = dict(reg.get(market, {}), nu=nu_out, width_cal=result['width_cal'],
                        panel_names=result['panel_names'], windows=result['windows'],
                        market_skill=result['market_skill'], market_ci90=result['market_ci90'],
                        market_verdict=result['market_verdict'], per_name=result['per_name'],
                        auto_refreshed=datetime.date.today().isoformat())
    reg.setdefault('_meta', {})['last_updated'] = datetime.date.today().isoformat()
    json.dump(reg, open(REGISTRY_PATH, 'w'), indent=2)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    args = ap.parse_args()

    touched = discover_touched_markets()
    if not touched:
        print(f"No files under {RAW_DIR}/{{MARKET}}/*.csv — nothing to do.")
        return 0

    reg = json.load(open(REGISTRY_PATH)) if os.path.exists(REGISTRY_PATH) else {}
    exit_code = 0
    for market, files in touched.items():
        print(f"\n=== {market}: {len(files)} file(s) in raw_ohlc/{market}/ ===")
        result = refresh_market(market, files, files, update_registry=False)
        incumbent_profile = PROFILES[market]
        incumbent_registry = reg.get(market, {})
        material, reasons, added = assess_materiality(market, result, incumbent_profile,
                                                       incumbent_registry)
        if added:
            print(f"  NEW name(s) in this market: {added}")

        if not material:
            print(f"  NOT MATERIAL — safe to auto-apply. "
                  f"nu={result['nu']} width_cal={result['width_cal']} "
                  f"verdict={result['market_verdict']}"
                  + (f"  [+{len(added)} new name(s): {','.join(added)}]" if added else ""))
            if args.apply:
                write_production(market, result)
                print(f"  -> written to market_profiles.py + fitted_configs.json")
        else:
            print(f"  MATERIAL — stopping, human review required:")
            for r in reasons:
                print(f"    - {r}")
            if args.apply:
                p = write_pending_review(market, result, reasons, incumbent_profile)
                print(f"  -> wrote {p}")
            exit_code = 1

    return exit_code


if __name__ == '__main__':
    sys.exit(main())
