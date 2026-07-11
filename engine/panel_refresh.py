"""panel_refresh.py — Testahil continuous-learning ingestion pipeline (v1, 11-Jul-2026)

The reusable machinery behind "every new OHLC upload makes the MC more
accurate." Point it at a manifest of {market_code: {name: raw_csv_path}} for
whatever names have new or updated history this session, for any market or
metal, and it:

  1. Rebuilds each name's panel window-file (engine/panels/{MKT}_{NAME}_60d.csv)
     from raw OHLC via backtest_v3 at the NEUTRAL baseline (nu=8.0, width_cal=1.0,
     use_signal=profile.signal_active) — this is what generates the standardized
     residual column 'u' that the shape fit trains on. u is invariant to the
     eventual (nu, width_cal) choice, so this baseline is stable scaffolding,
     never a claim about the market's real shape.
  2. Pools 'u' across EVERY name currently on that market's panel (old + new)
     and re-fits (nu, width_cal) via fit_nu_scale + shrink_cal — the market's
     full history, not just what changed this session.
  3. Re-scores every name under LONO (leave-one-name-out) fits for a de-
     circularized per-name verdict, and under the pooled fit for the market
     panel verdict — applying the robust-verdict rule (name FAIL requires the
     block-bootstrap CI to be entirely below zero across block sizes {2,3,4};
     a block-dependent sign flip is BOUNDARY, recorded PARITY-flagged, never a
     silent FAIL).
  4. Writes the single canonical machine-readable registry entry for that
     market into fitted_configs.json (this file becomes the one source of
     truth other build scripts should read (nu, width_cal, signal fields),
     replacing the old pattern of numbers scattered across dated .md notes).
  5. Appends a dated, human-readable note to market_fits_log.md (append-only,
     same spirit as the Calibration Ledger — never overwrite a past entry).

USAGE
-----
Edit MANIFEST below (or call refresh_market() directly from another script)
with this session's new/updated raw CSVs, then:  python3 panel_refresh.py

This does NOT touch market_profiles.py, publish anything, or write to the
live site — it only updates the engine-side fit registry. Site/ledger publish
stays a separate, explicitly-initiated step per the Standing Research Protocol.
"""
import sys, os, glob, json, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import pandas as pd
from mc_v3 import fit_nu_scale, shrink_cal, backtest_v3
from mc_v2 import load_ohlc as _raw_load_ohlc
from market_profiles import PROFILES
from data_quality import clean_ohlc


def load_ohlc(path, ticker=""):
    """Every series entering a panel passes the data-quality gate first."""
    df, _ = clean_ohlc(_raw_load_ohlc(path), ticker, verbose=False)
    return df

HERE = os.path.dirname(os.path.abspath(__file__))
PANELS_DIR = os.path.join(HERE, 'panels')
REGISTRY_PATH = os.path.join(HERE, 'fitted_configs.json')
LOG_PATH = os.path.join(HERE, 'market_fits_log.md')
N_PATHS = 20000
SEED = 42
MIN_HISTORY = 260


# ---------------------------------------------------------------- utilities
def apply_breaks(r, profile):
    """Drop windows whose ORIGIN precedes the market's last structural break.

    Closes a documented-but-unimplemented gap (found 11-Jul-2026): the Standing
    Research Protocol says "volatility pools use post-break windows only where a
    MarketProfile lists a structural break", and every profile declares `breaks`,
    but grep shows NEITHER mc_v2.py NOR mc_v3.py ever reads the field. Break
    filtering was therefore never applied — it only *appeared* to be, because
    min_history=260 happens to push most markets' first origin past their break
    anyway. It bites for real when a name carries history from before the break
    (e.g. EAND's OHLC starts 2016, six years before the UAE Jan-2022 workweek
    switch, while every other AE name starts 2021)."""
    if not getattr(profile, 'breaks', None):
        return r
    last = max(pd.Timestamp(b) for b in profile.breaks)
    return r[pd.DatetimeIndex(r['origin']) >= last].reset_index(drop=True)


def panel_path(market, name):
    return os.path.join(PANELS_DIR, f"{market}_{name}_60d.csv")


def existing_panel_names(market):
    return sorted({os.path.basename(f).split('_')[1]
                   for f in glob.glob(os.path.join(PANELS_DIR, f"{market}_*_60d.csv"))})


def build_panel_file(market, name, raw_csv_path, profile):
    """Baseline backtest (nu=8.0, width_cal=1.0) -> writes/overwrites the
    panel window-file. Panel files are training scaffolding (re-derived from
    raw history each refresh), NOT published forecasts — overwrite is safe
    and expected; the Calibration Ledger's append-only rule does not apply
    here."""
    df = load_ohlc(raw_csv_path)
    rows = backtest_v3(df, profile, horizon=60, nu=8.0, width_cal=1.0,
                        use_signal=profile.signal_active,
                        n_paths=N_PATHS, seed=SEED, min_history=MIN_HISTORY)
    r = pd.DataFrame(rows)
    r.to_csv(panel_path(market, name), index=False)
    return r, df


def verdict_ci(crps, crps_b, block, n_boot=3000, seed=SEED):
    rng = np.random.default_rng(seed)
    n = len(crps)
    boot = []
    for _ in range(n_boot):
        starts = rng.integers(0, n - block + 1, size=int(np.ceil(n / block)))
        idx = np.concatenate([np.arange(s, s + block) for s in starts])[:n]
        boot.append(1 - crps[idx].sum() / crps_b[idx].sum())
    lo, hi = np.percentile(boot, [5, 95])
    v = "PASS" if lo > 0 else ("FAIL" if hi < 0 else "PARITY")
    return lo, hi, v


def robust_verdict(crps, crps_b):
    """House rule: name-level FAIL only if CI < 0 across ALL of block={2,3,4}.
    A sign flip across block sizes -> BOUNDARY (PARITY-flagged), never FAIL."""
    detail = {b: verdict_ci(crps, crps_b, b) for b in (2, 3, 4)}
    verds = [detail[b][2] for b in (2, 3, 4)]
    if all(v == "FAIL" for v in verds):
        return "FAIL", detail
    if len(set(verds)) > 1:
        return "BOUNDARY(PARITY-flagged)", detail
    return verds[0], detail


def rescore(raw_csv_path, profile, nu, cal):
    """Returns (skill_norm, skill_raw, r). SCALE-NORMALIZED skill is primary.

    WHY (fixed 11-Jul-2026): CRPS is denominated in PRICE UNITS, so pooling raw
    CRPS across names weights each name by its share price, not its information
    content. Measured on the live panels: IHC (382 AED) carried 57.9% of the
    14-name UAE panel and ELM (874 SAR) carried 58.7% of the 11-name Saudi
    panel — a "panel verdict" that was arithmetically a one-name verdict. The
    same defect applies WITHIN a name across time (IHC ran 42 -> 382, so its
    recent windows outweighed its early ones ~9:1).

    Dividing each window's CRPS by that window's spot makes the score scale-free
    and fixes both. Validated on all three fitted markets (EG/SA/AE): ZERO
    verdict changes, market-level or name-level, but CIs tighten sharply (UAE
    panel CI went from +/-0.07 to +/-0.01) and headline skills de-inflate
    (Egypt's pooled PASS was +0.059 raw vs +0.039 normalized — the raw figure
    was ~50% overstated by TMGH's 42% price weight).

    The raw basis is still reported so numbers already published against the
    old basis remain reconcilable."""
    df = load_ohlc(raw_csv_path)
    rows = backtest_v3(df, profile, horizon=60, nu=nu, width_cal=cal,
                        use_signal=profile.signal_active,
                        n_paths=N_PATHS, seed=SEED, min_history=MIN_HISTORY)
    r = pd.DataFrame(rows)
    r = apply_breaks(r, profile)
    r['crps_n'] = r['crps'] / r['spot']
    r['crps_b_n'] = r['crps_b'] / r['spot']
    skill_norm = 1 - r['crps_n'].sum() / r['crps_b_n'].sum()
    skill_raw = 1 - r['crps'].sum() / r['crps_b'].sum()
    return skill_norm, skill_raw, r


# ---------------------------------------------------------------- main entry
def refresh_market(market, new_csvs, raw_csv_lookup):
    """market: profile code, e.g. 'SA'
    new_csvs: dict {name: raw_csv_path} for names touched THIS session
              (new names, or existing names with updated OHLC)
    raw_csv_lookup: dict {name: raw_csv_path} for EVERY name on the panel
              (old names not touched this session need their raw path too,
              so LONO/pooled rescoring can run against full current history)
    Returns a result dict; also writes panel files + updates the registry
    + appends the log entry."""
    profile = PROFILES[market]
    os.makedirs(PANELS_DIR, exist_ok=True)

    # 1. rebuild/refresh panel files for touched names
    for name, path in new_csvs.items():
        build_panel_file(market, name, path, profile)

    # 2. pool 'u' across the FULL current panel (old + new)
    names = sorted(set(existing_panel_names(market)) | set(new_csvs))
    panel = {n: apply_breaks(pd.read_csv(panel_path(market, n)), profile) for n in names}
    names = [n for n in names if len(panel[n]) > 0]
    pooled_u = np.concatenate([panel[n]['u'].values for n in names])
    nu_pool, s_pool = fit_nu_scale(pooled_u)
    cal_pool = shrink_cal(s_pool)

    # 3. LONO per-name verdicts + pooled market verdict
    per_name = {}
    for n in names:
        path = raw_csv_lookup.get(n) or new_csvs.get(n)
        if path is None:
            per_name[n] = dict(note="raw CSV not supplied this session — "
                                     "panel u reused, LONO verdict skipped")
            continue
        if len(names) >= 2:
            u = np.concatenate([panel[m]['u'].values for m in names if m != n])
            nu_l, s_l = fit_nu_scale(u); cal_l = shrink_cal(s_l)
        else:
            nu_l, cal_l = nu_pool, cal_pool
        sk, sk_raw, r = rescore(path, profile, nu_l, cal_l)
        verd, detail = robust_verdict(r['crps_n'].values, r['crps_b_n'].values)
        nu_disp = round(float(nu_l), 3) if nu_l < 200 else "Gaussian"
        per_name[n] = dict(nu=nu_disp, width_cal=round(cal_l, 3),
                            skill=round(float(sk), 4),
                            skill_raw_basis=round(float(sk_raw), 4),
                            verdict=verd,
                            ci_block2=[round(float(detail[2][0]), 3),
                                       round(float(detail[2][1]), 3)])

    allc, allb, allc_r, allb_r = [], [], [], []
    for n in names:
        path = raw_csv_lookup.get(n) or new_csvs.get(n)
        if path is None:
            continue
        _, _, r = rescore(path, profile, nu_pool, cal_pool)
        allc.append(r['crps_n'].values); allb.append(r['crps_b_n'].values)
        allc_r.append(r['crps'].values); allb_r.append(r['crps_b'].values)
    ac, ab = np.concatenate(allc), np.concatenate(allb)
    market_skill = float(1 - ac.sum() / ab.sum())
    lo, hi, market_verdict = verdict_ci(ac, ab, block=6)
    lo, hi = float(lo), float(hi)
    acr, abr = np.concatenate(allc_r), np.concatenate(allb_r)
    market_skill_raw = float(1 - acr.sum() / abr.sum())
    # concentration diagnostic: how much of the pooled weight does one name carry?
    weights = {}
    for n in names:
        pf = panel.get(n)
        if pf is not None and 'spot' in pf:
            weights[n] = float((pf['crps_b'] / pf['spot']).sum())
    tot = sum(weights.values()) or 1.0
    top_name = max(weights, key=weights.get) if weights else None
    top_share = round(weights[top_name] / tot, 3) if top_name else None

    result = dict(
        market=market, market_name=profile.name,
        fit_date=datetime.date.today().isoformat(),
        panel_names=names, windows=len(pooled_u),
        nu=round(float(nu_pool), 3) if nu_pool < 200 else "Gaussian",
        width_cal=round(float(cal_pool), 3),
        mle_scale=round(float(s_pool), 3),
        gate_basis="scale-normalized (crps/spot) — primary since 11-Jul-2026",
        market_skill=round(float(market_skill), 4),
        market_skill_raw_basis=round(float(market_skill_raw), 4),
        market_ci90=[round(lo, 3), round(hi, 3)],
        market_verdict=market_verdict,
        top_name_weight_share=top_share, top_name=top_name,
        signal_active=profile.signal_active,
        per_name=per_name,
    )

    _update_registry(market, result)
    _append_log(result)
    return result


def _update_registry(market, result):
    reg = {}
    if os.path.exists(REGISTRY_PATH):
        with open(REGISTRY_PATH) as f:
            reg = json.load(f)
    reg[market] = result
    reg.setdefault('_meta', {})['last_updated'] = datetime.date.today().isoformat()
    with open(REGISTRY_PATH, 'w') as f:
        json.dump(reg, f, indent=2)


def _append_log(result):
    lines = [f"\n## {result['market']} ({result['market_name']}) — refit {result['fit_date']}\n",
             f"Gate basis: {result.get('gate_basis','')}\n",
             f"Panel: {len(result['panel_names'])} names ({', '.join(result['panel_names'])}), "
             f"{result['windows']} pooled windows.\n",
             f"Production fit: nu={result['nu']}, width_cal={result['width_cal']} "
             f"(mle_scale={result['mle_scale']}).\n",
             f"Market panel verdict: skill={result['market_skill']:+.4f} "
             f"CI90={result['market_ci90']} **{result['market_verdict']}**\n",
             "\n| Name | nu | width_cal | skill | verdict |\n|---|---|---|---|---|\n"]
    for n, d in result['per_name'].items():
        if 'note' in d:
            lines.append(f"| {n} | — | — | — | {d['note']} |\n")
        else:
            lines.append(f"| {n} | {d['nu']} | {d['width_cal']} | {d['skill']:+.4f} | {d['verdict']} |\n")
    header = "# Testahil market fit log (append-only)\n" if not os.path.exists(LOG_PATH) else ""
    with open(LOG_PATH, 'a') as f:
        if header:
            f.write(header)
        f.writelines(lines)


if __name__ == '__main__':
    print("Import refresh_market(market, new_csvs, raw_csv_lookup) and call it "
          "per market from a driver script with this session's uploaded CSVs.")
