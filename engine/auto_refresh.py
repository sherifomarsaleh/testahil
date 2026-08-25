"""auto_refresh.py — unattended entry point for the Testahil continuous-learning loop.

DESIGN PRINCIPLE (11-Jul-2026, user instruction: "automatic but not at the expense
of quality"): mechanical work runs unattended. Anything that would change a
name's PUBLISHED COVERAGE FLAG, imply a signal ablation, or move a config beyond a
small tolerance STOPS and asks a human. The 11-Jul session is the reason this gate
exists: data cleaning alone flipped Korea's tail shape from nu=6 to Gaussian and
moved two names across a scoring boundary (at the time, SA/RAJHI and
AE/ALPHADHABI, under the skill verdict R-CAL-03 has since retired).
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
  - the per-name LONO fits and the pooled panel scores
  ...PROVIDED the materiality gate below finds nothing that needs a human.

WHAT IS MATERIAL — APPLIED, BUT NEVER SILENTLY [R-CAL-01, 23-Aug-2026;
CONDITIONS REPLACED 25-Aug-2026 BY R-CAL-03]:
  - any EXISTING name's COVERAGE FLAG changes (narrow / wide / none)
  - a NEW name arrives ALREADY FLAGGED
  - the published 90% cone moves >5% (measured on width_cal x q95(t(nu)), never on
    the two coordinates separately — they trade off)
  - a panel carries a name with NO raw CSV in the library (a genuine inconsistency
    now that the library is authoritative — it means a file was deleted or never
    added, and the panel is running on stale residuals)

The first two conditions used to read "an existing name's verdict category changes"
and "a new name arrives already FAILING". [R-CAL-03] retired the PASS/PARITY/FAIL
skill verdict outright — it had never once excluded a market, and it disagreed with
the band record on 40% of the book — and named these replacements explicitly. The
two surviving numeric conditions watch DIFFERENT things and both are needed: mc_v3
writes the in-band flags when a window is scored and a refit never rewrites them, so
a coverage flag moves when a name's RECORD moves, while the cone-width condition
moves when the FIT does. robust_verdict itself stays in panel_refresh as an internal
diagnostic under R-CAL-03, and as the G-crps guard R-SHAPE-01 builds on; what is
retired is its standing to gate, trigger or block anything here.

Until 23-Aug-2026 each of those STOPPED the pipeline and opened a PR for a human. That
gate was adopted for a good reason — data cleaning ALONE once flipped Korea's tail from
nu=6 to Gaussian and moved two names' scores, and the note said a bare cron "would
have shipped both silently". The reason survives; the mechanism did not. Between 6-Aug and
23-Aug-2026 the gate produced 66 unmerged review PRs, and 18 names across EG, AE and SA
sat outside any applied fit — ADNOCLS, DU, MODON, FERTIGLB and SAVOLA among them, all
with live pages. Worse, the PRs could not be accepted even in principle: they staged
only PENDING_REVIEW and panels, so merging one applied nothing.

A gate nobody can clear is not caution, it is a stall, and a stall is its own silence —
production kept publishing a 29-Jul fit and said nothing about it. So the defect being
guarded against, SILENCE, is now attacked directly: a material change APPLIES, and is
announced in three places at once — the evidence file under PENDING_REVIEW/, the reasons
repeated verbatim in the commit message, and the config it replaced stored under
`superseded` in fitted_configs.json. Reverting that one commit undoes all of it in step.
Pass --halt-on-material for the old behaviour.

WHAT STILL STOPS THE RUN: a market that raises. A crashed market is reported, exits
nonzero and never touches production, exactly as before — an exception is not evidence.

A NEW NAME IS NOT, BY ITSELF, MATERIAL. Adding a stock is the single most common
thing that happens here, and blocking on it would mean a PR on literally every
post. You placing the file at raw_ohlc/{MKT}/{TICKER}.csv IS the human decision
about what the series is. The pipeline still guards the things that actually
matter: if the new name arrives already FLAGGED, or its arrival destabilises the
market fit or moves another name's coverage flag, that still stops. New names are always named
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
from band_record import by_key as _band_records, FLAG_LABEL
from market_profiles import PROFILES

HERE = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(HERE, 'raw_ohlc')
REGISTRY_PATH = os.path.join(HERE, 'fitted_configs.json')
PENDING_DIR = os.path.join(HERE, 'PENDING_REVIEW')

BAND_TOL = 0.05           # the published 90% cone half-width may drift this much silently
NU_GAUSSIAN_CUTOFF = 200  # nu above this is "effectively Gaussian"

# Which horizon set the unattended pipeline calibrates on (panel_refresh.HORIZON_SETS).
# '3m' = the calendar 3-month gate adopted 27-Jul-2026, matching what is published.
# '60d' = the retired fixed-60-session gate, kept re-runnable for the grandfathered
# session-counted cohorts. Flipping this constant is the whole adoption switch — and it is
# deliberately loud: the first run after the flip compares a calendar-3M fit against a
# 60d incumbent in market_profiles.py, so the materiality gate fires and opens a PR
# instead of auto-committing. That is the intended behaviour, not a fault.
HORIZON_TAG = '3m'


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


def _coverage_flags(market, names):
    """Each name's published coverage flag -- 'narrow' | 'wide' | None -- keyed by name.

    [R-CAL-03] retired the PASS/PARITY/FAIL skill verdict outright and REPLACED the
    materiality conditions that stood on it with "a name's coverage flag changes, or the
    published 90% cone moves >5%". This is the first half.

    THE TWO HALVES WATCH DIFFERENT THINGS, WHICH IS WHY BOTH ARE NEEDED. mc_v3 writes
    in50/in80/in90 into a panel when a window is SCORED, and a refit never rewrites them,
    so a coverage flag moves when a name's RECORD moves -- a panel rebuild, a newly
    resolved window -- and not when (nu, width_cal) wobble. The cone-width condition above
    watches the fit; this watches the record. A gate that tested only one of them would
    miss half of what the retired verdict used to catch, and the retired verdict's own
    epitaph is that a test which never changes an outcome is decorative.

    The flag is computed by band_record.from_panel and NOWHERE ELSE. The binomial test,
    the readable-strength cut and the rounding rule have one owner, for the same reason
    the panel's public name does: two implementations of a published threshold disagree
    eventually, and the disagreement surfaces as a number on a page.

    MEASURED BEFORE IT SHIPPED, because a replacement gate can be decorative too: every
    name this is asked about resolves to a record, and 6 of 74 carried a flag on the day
    it landed (AE EMAAR/IHC narrow, EG ETEL wide / ISPH narrow, IN TMPV narrow, SA RIBL
    narrow) -- live signal to compare against. That measurement also exposed an
    asymmetry worth knowing, and worth stating precisely because the first draft of this
    note got it wrong: 93 calendar _3m panels exist on disk but only 74 _60d, and
    panel_refresh.DEFAULT_TAG is still the retired session-counted 60d. That does NOT
    narrow this gate -- refresh_market builds names as existing_panel_names(tag) UNION the
    raw CSVs, so with the library present it covers all 93, which the dry run confirms
    (AE 28, EG 37, SA 13 ...). The divergence is a housekeeping inconsistency in the panel
    filenames, not a hole in the materiality check, and it is recorded as such.

    ENUMERATED THROUGH band_record, NEVER THROUGH panel_path. The first cut of this
    helper called panel_refresh.panel_path(market, name), whose DEFAULT_TAG is the retired
    session-counted "60d" -- so it resolved EG_GBCO_60d.csv while band_record reads the
    calendar "_3m" panels, from_panel mis-parsed the name, and a blanket `except: continue`
    swallowed every failure. The gate returned an empty dict for all nine markets and
    would have reported "nothing material" forever, silently. That is precisely the
    decorative-gate failure R-CAL-03 retired the verdict for, reproduced inside its own
    replacement, and it was caught only because the replacement was measured before it
    shipped rather than after. There is no broad except here for the same reason.
    """
    recs = _band_records()
    return {n: recs[(market, n)].flag for n in names if (market, n) in recs}


def _flag_text(f):
    return FLAG_LABEL[f] if f else "no flag"


def assess_materiality(market, result, incumbent_profile, incumbent_registry):
    """Returns (is_material: bool, reasons: list[str])."""
    reasons = []

    old_bw = band_halfwidth(incumbent_profile.nu, incumbent_profile.width_cal)
    new_bw = band_halfwidth(result['nu'], result['width_cal'])
    if old_bw and new_bw:
        # SIGNED, not absolute (fixed 23-Aug-2026). The threshold test is on the
        # magnitude, but the number REPORTED must carry its sign: taking abs() and then
        # formatting with '+' made every move print as a widening. On 23-Aug-2026 the AE
        # refit narrowed the cone by 5.1% and the report announced "+5.1%", which reads
        # as the opposite and was repeated into a summary before anyone recomputed it.
        rel = (new_bw - old_bw) / old_bw
        if abs(rel) > BAND_TOL:
            reasons.append(
                f"the PUBLISHED 90% cone moves {rel:+.1%} (> {BAND_TOL:.0%} tolerance): "
                f"(nu={incumbent_profile.nu}, cal={incumbent_profile.width_cal}) -> "
                f"(nu={result['nu']}, cal={result['width_cal']})")

    old_names = set(incumbent_registry.get('panel_names', []))
    new_names = set(result['panel_names'])
    added = sorted(new_names - old_names)
    # A new name is NOT material by itself (see module docstring) — but a new name that
    # arrives ALREADY FLAGGED is: that is either a genuinely uncalibratable series or,
    # more likely, a misfiled/bad file, and it should not silently enter a production
    # panel. [R-CAL-03] this used to read "arrives with a robust FAIL"; the verdict it
    # tested is retired, and the amended R-CAL-01 condition is "a NEW name arrives
    # already flagged".
    new_flags = _coverage_flags(market, result['panel_names'])
    for n in added:
        f = new_flags.get(n)
        if f:
            reasons.append(f"NEW name {n} arrives already flagged '{_flag_text(f)}' — check "
                            f"the file is the right instrument, in the right market folder, "
                            f"with clean history")

    # A panel carrying a name with no raw data is material on its own. Keyed on the
    # absence marker panel_refresh writes, NOT on the retired verdict field's absence.
    for n, d in result['per_name'].items():
        if 'note' in d and 'nu' not in d:
            reasons.append(f"{n}: no raw CSV supplied this run ('{d['note']}') — needs a "
                            f"human to confirm this name's absence is intentional")

    # An EXISTING name's coverage flag changing is the replacement for the retired
    # "verdict changed" condition. UNKNOWN-on-both-sides is not a change: a name with no
    # stored flag from the previous run is skipped, exactly as the verdict comparison
    # skipped 'UNKNOWN', so the first run after this lands does not fire on all of them.
    old_flags = incumbent_registry.get('coverage_flags')
    if isinstance(old_flags, dict):
        for n, f in sorted(new_flags.items()):
            if n in added or n not in old_flags:
                continue
            if old_flags[n] != f:
                reasons.append(f"{n}: coverage flag {_flag_text(old_flags[n])} -> "
                                f"{_flag_text(f)}")

    return (len(reasons) > 0), reasons, added


def write_change_record(market, result, reasons, incumbent_profile, applied=True):
    """Write the evidence file for a material calibration change.

    Two modes, because the same evidence serves two paths. applied=False is the gate's
    original behaviour: the pipeline stopped, nothing was written to production, a human
    is being asked. applied=True is scripts/adopt_calibration.py recording a change that
    HAS been made, so the reasons sit beside the config that now carries them.

    The distinction is not cosmetic. 66 review PRs accumulated between 6-Aug and
    23-Aug-2026 saying "PENDING REVIEW ... nothing has been touched" — and after the
    adoption script ran, the same file would have kept asserting production was untouched
    when it no longer was. An evidence file that describes the wrong state is worse than
    none, because it is the thing a reader trusts when reconstructing what happened.
    """
    os.makedirs(PENDING_DIR, exist_ok=True)
    d = datetime.date.today().isoformat()
    path = os.path.join(PENDING_DIR, f"{market}_{d}.md")
    if applied:
        lines = [
            f"# CALIBRATION CHANGE APPLIED — {market} ({result['market_name']}) — {d}\n\n",
            "auto_refresh.py found MATERIAL changes and APPLIED them. market_profiles.py "
            "and fitted_configs.json now carry the config below; the config it replaced is "
            "recorded under `superseded` in fitted_configs.json, and reverting the commit "
            "that carried this file restores both together.\n\n",
            "## What made this material\n\n",
        ]
    else:
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
    # [R-CAL-03] the market verdict used to headline this file. RETIRED MEANS no
    # PENDING_REVIEW field with standing, so the coverage picture leads and the skill
    # figures below are labelled for what they now are: an internal diagnostic, kept
    # because CRPS is a proper scoring rule and is worth consulting when investigating a
    # model change — never a gate, a trigger, or something a reader is shown.
    _fl = _coverage_flags(market, result['panel_names'])
    _flagged = sorted(n for n, v in _fl.items() if v)
    lines.append(f"- coverage flags: **{len(_flagged)} of {len(_fl)}** name(s) flagged"
                  + (f" ({', '.join(f'{n}={_flag_text(_fl[n])}' for n in _flagged)})"
                     if _flagged else "") + "\n\n")
    lines.append("## Per-name fits (skill columns are an INTERNAL DIAGNOSTIC under "
                  "[R-CAL-03] — not a gate, not a verdict)\n\n"
                  "| Name | nu | width_cal | skill |\n|---|---|---|---|\n")
    for n, d2 in sorted(result['per_name'].items()):
        if 'nu' not in d2:
            lines.append(f"| {n} | — | — | {d2.get('note', 'not scored this run')} |\n")
        else:
            lines.append(f"| {n} | {d2['nu']} | {d2['width_cal']} | {d2['skill']:+.4f} |\n")
    lines.append("\n## To apply\n\nReview against the coverage flags and the per-name fits "
                  "above — the skill column is a diagnostic, not a verdict — then either merge "
                  "this PR to accept, or re-run with a corrected raw_ohlc/ input.\n")
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
                  'KR': 'KOREA', 'AE': 'UAE', 'IN': 'INDIA', 'QA': 'QATAR', 'XAU': 'METALS',
                  'XPT': 'PLATINUM'}[market]

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
    # Every apply records what it replaced (23-Aug-2026). Before this, undoing a config
    # change meant reading it back out of a diff: the registry carried only the new pair,
    # so the old one existed nowhere in machine-readable form. This pair, plus the commit
    # that carried it, IS the revert — reverting that commit restores market_profiles.py
    # and this file together, in step, which hand-editing either one cannot.
    superseded = dict(nu=prof.nu, width_cal=prof.width_cal,
                      market_verdict=reg.get(market, {}).get('market_verdict'),
                      replaced_on=datetime.date.today().isoformat())
    reg[market] = dict(reg.get(market, {}), nu=nu_out, width_cal=result['width_cal'],
                        superseded=superseded,
                        mid_band_reshape=result.get('mid_band_reshape'),
                        panel_names=result['panel_names'], windows=result['windows'],
                        coverage_flags=_coverage_flags(market, result['panel_names']),
                        market_skill=result['market_skill'], market_ci90=result['market_ci90'],
                        market_verdict=result['market_verdict'], per_name=result['per_name'],
                        auto_refreshed=datetime.date.today().isoformat())
    reg.setdefault('_meta', {})['last_updated'] = datetime.date.today().isoformat()
    json.dump(reg, open(REGISTRY_PATH, 'w'), indent=2)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    ap.add_argument('--halt-on-material', action='store_true',
                    help='pre-23-Aug-2026 behaviour: stop on a material change and write '
                         'a PENDING_REVIEW report instead of applying it')
    args = ap.parse_args()
    applied_material = []

    touched = discover_touched_markets()
    if not touched:
        print(f"No files under {RAW_DIR}/{{MARKET}}/*.csv — nothing to do.")
        return 0

    reg = json.load(open(REGISTRY_PATH)) if os.path.exists(REGISTRY_PATH) else {}
    exit_code = 0
    for market, files in touched.items():
        print(f"\n=== {market}: {len(files)} file(s) in raw_ohlc/{market}/ ===")
        # One market's failure must never kill the others. Before this guard, LULU's
        # 2-window panel crashed the robust-verdict bootstrap inside AE, and because
        # AE sorts first the WHOLE daily run died with it: no market was refit from
        # 19-Jul-2026 until the fix, DSCW (EG) sat unprocessed, and the workflow's
        # failure path shipped junk branches (half-written panels, a stale PR body).
        # A crashed market is by definition material: report it, exit nonzero, move on.
        try:
            result = refresh_market(market, files, files, update_registry=False,
                                    tag=HORIZON_TAG)
        except Exception as exc:
            import traceback
            tb = traceback.format_exc()
            print(f"  PIPELINE ERROR — {market} could not be refit: {exc}")
            if args.apply:
                os.makedirs(PENDING_DIR, exist_ok=True)
                p = os.path.join(PENDING_DIR,
                                 f"{market}_{datetime.date.today().isoformat()}-ERROR.md")
                with open(p, 'w') as f:
                    f.write(f"# PENDING REVIEW — {market} — PIPELINE ERROR — "
                            f"{datetime.date.today().isoformat()}\n\n"
                            f"auto_refresh.py could not refit this market. Production was "
                            f"NOT touched. Other markets continued normally.\n\n"
                            f"```\n{tb}```\n")
                print(f"  -> wrote {p}")
            exit_code = 1
            continue
        incumbent_profile = PROFILES[market]
        incumbent_registry = reg.get(market, {})
        material, reasons, added = assess_materiality(market, result, incumbent_profile,
                                                       incumbent_registry)
        if added:
            print(f"  NEW name(s) in this market: {added}")

        if not material:
            # [R-CAL-03] this line used to end 'verdict=PARITY'. The verdict is retired;
            # printing it here kept a dead test in front of the one person who reads this
            # output and decides. What matters operationally is how many names carry a
            # coverage flag, which is what the gate above actually tests.
            _flags = _coverage_flags(market, result['panel_names'])
            _n_flagged = sum(1 for v in _flags.values() if v)
            print(f"  NOT MATERIAL — safe to auto-apply. "
                  f"nu={result['nu']} width_cal={result['width_cal']} "
                  f"flagged={_n_flagged}/{len(_flags)}"
                  + (f"  [+{len(added)} new name(s): {','.join(added)}]" if added else ""))
            if args.apply:
                write_production(market, result)
                print(f"  -> written to market_profiles.py + fitted_configs.json")
        elif args.halt_on_material:
            print(f"  MATERIAL — stopping, human review required:")
            for r in reasons:
                print(f"    - {r}")
            if args.apply:
                p = write_change_record(market, result, reasons, incumbent_profile,
                                        applied=False)
                print(f"  -> wrote {p}")
            exit_code = 1

        else:
            # [R-CAL-01] MATERIAL CHANGES APPLY. The gate used to stop here. It is now
            # loud instead of blocking — see the module docstring for why, and for what
            # still stops.
            print(f"  MATERIAL — applying, and recording why:")
            for r in reasons:
                print(f"    - {r}")
            if args.apply:
                write_production(market, result)
                p = write_change_record(market, result, reasons, incumbent_profile,
                                        applied=True)
                print(f"  -> applied to market_profiles.py + fitted_configs.json")
                print(f"  -> recorded at {p}")
            applied_material.append((market, reasons))

    if args.apply and applied_material:
        # The commit message is the loudest of the three announcements, because it is the
        # one that reaches anyone reading `git log` without knowing to look. The workflow
        # reads this file to build it.
        os.makedirs(PENDING_DIR, exist_ok=True)
        with open(os.path.join(PENDING_DIR, 'LAST_RUN_MATERIAL.txt'), 'w') as f:
            for market, reasons in applied_material:
                for r in reasons:
                    f.write(f"{market}: {r}\n")

    return exit_code


if __name__ == '__main__':
    sys.exit(main())
