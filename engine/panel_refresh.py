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
import hashlib
import numpy as np
import pandas as pd
from mc_v3 import fit_nu_scale, shrink_cal, backtest_v3, simulate_terminal_v3
from primitives import crps_sample
from primitives import load_ohlc as _raw_load_ohlc
from market_profiles import PROFILES
from data_quality import clean_ohlc


def load_ohlc(path, ticker="", market=None):
    """Every series entering a panel passes the data-quality gate first.
    `market` selects the exchange's daily-limit-derived artifact threshold."""
    df, _ = clean_ohlc(_raw_load_ohlc(path), ticker, verbose=False, market=market)
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
    but grep shows NEITHER primitives.py NOR mc_v3.py ever reads the field. Break
    filtering was therefore never applied — it only *appeared* to be, because
    min_history=260 happens to push most markets' first origin past their break
    anyway. It bites for real when a name carries history from before the break
    (e.g. EAND's OHLC starts 2016, six years before the UAE Jan-2022 workweek
    switch, while every other AE name starts 2021)."""
    if not getattr(profile, 'breaks', None):
        return r
    last = max(pd.Timestamp(b) for b in profile.breaks)
    return r[pd.DatetimeIndex(r['origin']) >= last].reset_index(drop=True)


# ---------------------------------------------------------------- horizon set
# HORIZON SETS (27-Jul-2026). '60d' is the retired session-counted gate that
# calibrated every session-counted cohort; it stays here, untouched and re-runnable,
# because those cohorts are grandfathered and must keep grading under the fit
# they were published on. '3m' is the calendar-anchored gate: a per-origin
# window running to the first session on or after origin + 3 calendar months,
# so the gate scores the horizon that is actually published.
# Panels are namespaced by tag, so the two calibrations never overwrite each
# other and can be compared side by side.
HORIZON_SETS = {
    '60d': dict(months=None, horizon=60,
                label='3 months (retired, session-counted)'),
    '3m':  dict(months=3, horizon=None,
                label='3 months (calendar-anchored)'),
}
DEFAULT_TAG = '60d'


def _hset(tag):
    if tag not in HORIZON_SETS:
        raise KeyError(f"unknown horizon tag {tag!r}; "
                       f"expected one of {sorted(HORIZON_SETS)}")
    return HORIZON_SETS[tag]


def panel_path(market, name, tag=DEFAULT_TAG):
    return os.path.join(PANELS_DIR, f"{market}_{name}_{tag}.csv")


HASH_PATH = os.path.join(HERE, 'panel_hashes.json')


def _file_hash(path):
    return hashlib.sha256(open(path, 'rb').read()).hexdigest()[:16]


def _load_hashes():
    if os.path.exists(HASH_PATH):
        try:
            return json.load(open(HASH_PATH))
        except Exception:
            return {}
    return {}


def _save_hashes(h):
    json.dump(h, open(HASH_PATH, 'w'), indent=2)


# ---------------------------------------------------------------- fast rescore
def fast_rescore(r, nu, cal, n_paths=N_PATHS, seed=SEED):
    """Re-score a prebuilt panel under a new (nu, width_cal) WITHOUT re-running the
    engine. This is EXACT, not an approximation, and it is what makes a one-stock-at-
    a-time upload practical (the naive path re-ran ~3 full backtests per name, each
    O(n^2) in the HAR refit — the full 65-stock library timed out).

    Why it is exact: nu and width_cal enter ONLY at the simulation step.
      sigma_h(cal) = sigma_h(1.0) * cal          [HAR variance is cal-independent]
      alpha(cal)   = alpha(1.0) * cal            [alpha = IC*sigma_h*sign*clip(z),
                                                  and its cap is +/-0.5*sigma_h —
                                                  both scale linearly in sigma_h]
      carry        = drift - alpha               [cal-invariant]
      => drift(cal) = carry + alpha(1.0)*cal
    The benchmark (crps_b) depends on neither, so it is reused as stored.
    Panels are built at the baseline (nu=8, width_cal=1.0), so r's sigma_h/alpha are
    the (1.0) quantities. Verified bit-for-bit against backtest_v3 before adoption.
    """
    carry = r['drift'].values - r['alpha'].values
    sigma = r['sigma_h'].values * cal
    drift = carry + r['alpha'].values * cal
    spot = r['spot'].values
    realized = r['realized'].values
    idx = r['origin_idx'].values
    out = np.empty(len(r))
    for i in range(len(r)):
        samp = simulate_terminal_v3(spot[i], sigma[i], drift[i], nu=nu,
                                     n_paths=n_paths, seed=int(seed + idx[i]))
        out[i] = crps_sample(samp, realized[i])
    return out


def existing_panel_names(market, tag=DEFAULT_TAG):
    return sorted({os.path.basename(f).split('_')[1]
                   for f in glob.glob(os.path.join(PANELS_DIR,
                                                   f"{market}_*_{tag}.csv"))})


def build_panel_file(market, name, raw_csv_path, profile, tag=DEFAULT_TAG):
    """Baseline backtest (nu=8.0, width_cal=1.0) -> writes/overwrites the
    panel window-file. Panel files are training scaffolding (re-derived from
    raw history each refresh), NOT published forecasts — overwrite is safe
    and expected; the Calibration Ledger's append-only rule does not apply
    here."""
    hs = _hset(tag)
    df = load_ohlc(raw_csv_path, name, market=market)
    rows = backtest_v3(df, profile, horizon=hs['horizon'] or 60,
                       horizon_months=hs['months'], nu=8.0, width_cal=1.0,
                       use_signal=profile.signal_active,
                       n_paths=N_PATHS, seed=SEED, min_history=MIN_HISTORY)
    r = pd.DataFrame(rows)
    # The per-origin RNG seed is (seed + origin_idx); recording origin_idx is
    # what lets fast_rescore re-simulate EXACTLY instead of re-running the
    # engine. backtest_v3 now emits it directly — under a calendar horizon the
    # stride VARIES per window, so the old MIN_HISTORY + i*60 reconstruction is
    # only valid for the fixed-h '60d' set and is no longer used.
    if 'origin_idx' not in r.columns:      # panel built by a pre-27-Jul engine
        r['origin_idx'] = MIN_HISTORY + np.arange(len(r)) * 60
    r.to_csv(panel_path(market, name, tag), index=False)
    return r, df


def verdict_ci(crps, crps_b, block, n_boot=3000, seed=SEED):
    rng = np.random.default_rng(seed)
    n = len(crps)
    # A series with fewer windows than the block size cannot be block-bootstrapped at
    # that block: rng.integers(0, n-block+1) has high<=0 and raises. This is not a
    # hypothetical — LULU (listed Nov-2024, 2 post-burn-in windows) entered raw_ohlc/AE
    # and the unattended loop crashed HERE on block=3, which killed the ENTIRE daily
    # run for every market from 19-Jul-2026 onward (AE is processed first
    # alphabetically). A thin name must degrade gracefully, never crash the loop.
    if n < block:
        return float('nan'), float('nan'), "NOBLOCK"
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
    if "NOBLOCK" in verds:
        # The robust standard (CI < 0 across ALL of blocks {2,3,4}) cannot even be
        # evaluated when a block cannot run. A too-thin name therefore gets an
        # explicit PROVISIONAL verdict: never FAIL (the robust bar is unmeetable),
        # never a silent PARITY (that would overstate the evidence), never a crash.
        # It re-resolves automatically once the name accrues >=4 windows.
        return "PROVISIONAL(insufficient-windows)", detail
    if all(v == "FAIL" for v in verds):
        return "FAIL", detail
    if len(set(verds)) > 1:
        return "BOUNDARY(PARITY-flagged)", detail
    return verds[0], detail


# ------------------------------------------------- [R-SHAPE-01] mid-band reshape
# Guarded mid-band shape selection (adopted 24-Aug-2026, per instruction —
# investor session, "reshape UAE and Egypt to make it less conservative").
#
# WHY. nu is weakly identified: on these panels several tail-shapes sit inside
# the 95% likelihood region, and MLE breaks that tie blindly. The tie is not
# innocuous — shapes on the SAME iso-90% ridge (cal * T95(nu) held constant, the
# very quantity R-CAL-01's materiality metric watches) differ visibly in how
# wide the 25-75 band is. Measured 24-Aug-2026: AE's production shape caught
# 53.8% in its 50% band while a ridge-mate caught 50.1% with the SAME 90% edge.
# Picking the ridge point whose 50% band actually catches half is calibration,
# not narrowing; every guard below exists so this can never become the
# CRPS-selection mistake (in-sample coverage chasing) the promotion rule
# already rejected once.
#
# THE GUARDS ARE THE RELEASE (a gate with no release is a stall): a market
# reshapes at any refit where ALL guards pass, and silently keeps its MLE shape
# otherwise. On adoption day that meant: AE reshaped; EG declined (split-half —
# its mid-band over-coverage lives only in the late half while the early half
# already under-covers, so no single shape helps both); SA declined (0.4pt from
# target — nothing to fix). The declines are the rule working, not exceptions.
RESHAPE_GRID = (3.0, 3.5, 4.0, 4.5, 5.0, 6.0, 8.0, 10.0, 12.0, 15.0, 20.0,
                30.0, 1e9)
RESHAPE_MIN_IMPROVE = 0.01      # candidate must close >= 1pt of |cov50 - 50%|
RESHAPE_MAX_DLL = 3.0           # must stay inside the 95% joint likelihood region
RESHAPE_CAL_CLIP = (0.85, 1.30)  # same legality clip shrink_cal enforces


def _tq(p, nu):
    """Quantile of the engine's UNIT-VARIANCE t (mc_v3: x = t_nu/sqrt(nu/(nu-2)))."""
    from scipy import stats as _st
    if nu >= 200:
        return float(_st.norm.ppf(p))
    return float(_st.t.ppf(p, nu) / np.sqrt(nu / (nu - 2)))


def _pool_frame(panel, names):
    frames = []
    for n in names:
        r = panel[n]
        frames.append(pd.DataFrame({
            'u': r['u'].values,
            'a': np.where(r['sigma_h'].values > 0,
                          r['alpha'].values / r['sigma_h'].values, 0.0),
            'origin': pd.to_datetime(r['origin']),
            'name': n,
        }))
    big = pd.concat(frames, ignore_index=True)
    return big[np.isfinite(big['u'])].reset_index(drop=True)


def _cov50(big, nu, cal):
    """Exact fast_rescore algebra: drift_new = carry + alpha*cal, sigma_new =
    sigma_h*cal, so a window is inside the 25-75 band iff
    cal*T25 <= u - a*(cal-1) <= cal*T75 with a = alpha/sigma_h at baseline."""
    u_adj = big['u'].values - big['a'].values * (cal - 1)
    return float(np.mean((cal * _tq(.25, nu) <= u_adj) & (u_adj <= cal * _tq(.75, nu))))


def _loglik(u, nu, s):
    from scipy import stats as _st
    if nu >= 200:
        return float(_st.norm.logpdf(u / s).sum() - len(u) * np.log(s))
    k = np.sqrt(nu / (nu - 2))
    return float(_st.t.logpdf(u * k / s, nu).sum() + len(u) * (np.log(k) - np.log(s)))


def _ridge_candidate(big, w90, ll_max):
    """Admissible ridge point closest to 50% mid-band coverage. Admissible =
    same 90% edge (by construction), cal inside the legality clip, and inside
    the 95% joint likelihood region — 'shapes the data cannot tell apart'."""
    u = big['u'].values
    best = None
    for nu in RESHAPE_GRID:
        cal = w90 / _tq(.95, nu)
        if not (RESHAPE_CAL_CLIP[0] <= cal <= RESHAPE_CAL_CLIP[1]):
            continue
        if ll_max - _loglik(u, nu, cal) > RESHAPE_MAX_DLL:
            continue
        c50 = _cov50(big, nu, cal)
        if best is None or abs(c50 - .5) < abs(best[2] - .5):
            best = (nu, cal, c50)
    return best


def reshape_mid_band(panel, names, nu_mle, cal_mle):
    """Returns (nu, cal, note). Keeps (nu_mle, cal_mle) unless EVERY guard passes:
      G-flat     candidate inside the 95% joint likelihood region (and legal cal);
      G-improve  closes >= RESHAPE_MIN_IMPROVE of the mid-band coverage error;
      G-split    BOTH calendar halves move strictly toward 50% (kills a
                 regime artifact — the exact EG failure mode of 24-Aug-2026);
      G-lono     leave-one-name-out: each name scored under a shape selected
                 WITHOUT it; pooled held-out coverage must improve too;
      G-crps     proper-score parity: the reshaped cone's pooled crps/spot must
                 not be ROBUSTLY worse than the MLE shape's across bootstrap
                 blocks {2,3,4} (the house robustness bar, mirrored).
    The verdict machinery (per-name LONO fits, robust_verdict) is untouched —
    this selects the PRODUCTION shape only."""
    big = _pool_frame(panel, names)
    u = big['u'].values
    nu_raw, s_raw = fit_nu_scale(u)
    ll_max = _loglik(u, nu_raw, s_raw)
    w90 = cal_mle * _tq(.95, nu_mle)
    base = dict(applied=False, mle_shape=[nu_mle, round(cal_mle, 3)],
                w90_sigma=round(w90, 4))

    cand = _ridge_candidate(big, w90, ll_max)
    c50_mle = _cov50(big, nu_mle, cal_mle)
    if cand is None or (cand[0] == nu_mle):
        return nu_mle, cal_mle, dict(base, reason="MLE shape already closest "
                                     "admissible point", cov50=round(c50_mle, 4))
    nu_c, cal_c, c50_c = cand

    if abs(c50_mle - .5) - abs(c50_c - .5) < RESHAPE_MIN_IMPROVE:
        return nu_mle, cal_mle, dict(base, reason=f"G-improve: gain "
                                     f"{abs(c50_mle-.5)-abs(c50_c-.5):.3f} < "
                                     f"{RESHAPE_MIN_IMPROVE}")

    med = big['origin'].median()
    for tag, half in (("early", big[big['origin'] <= med]),
                      ("late", big[big['origin'] > med])):
        if abs(_cov50(half, nu_c, cal_c) - .5) >= abs(_cov50(half, nu_mle, cal_mle) - .5):
            return nu_mle, cal_mle, dict(base, reason=f"G-split: {tag} half does "
                                         "not move toward 50%")

    held_in, held_n = 0.0, 0
    for n in names:
        others = big[big['name'] != n]
        mine = big[big['name'] == n]
        if not len(mine) or not len(others):
            continue
        nur, sr = fit_nu_scale(others['u'].values)
        cand_n = _ridge_candidate(others, w90, _loglik(others['u'].values, nur, sr))
        nu_h, cal_h = (cand_n[0], cand_n[1]) if cand_n else (nu_mle, cal_mle)
        held_in += _cov50(mine, nu_h, cal_h) * len(mine)
        held_n += len(mine)
    lono50 = held_in / max(held_n, 1)
    if abs(lono50 - .5) >= abs(c50_mle - .5):
        return nu_mle, cal_mle, dict(base, reason=f"G-lono: held-out cov50 "
                                     f"{lono50:.3f} no better than MLE shape")

    c_new, c_mle, spots = [], [], []
    for n in names:
        r = panel[n]
        if 'origin_idx' not in r.columns or not len(r):
            continue
        c_new.append(fast_rescore(r, nu_c, cal_c) / r['spot'].values)
        c_mle.append(fast_rescore(r, nu_mle, cal_mle) / r['spot'].values)
    cn, cm = np.concatenate(c_new), np.concatenate(c_mle)
    cis = {b: verdict_ci(cn, cm, b) for b in (2, 3, 4)}
    if all(ci[2] == "FAIL" for ci in cis.values()):
        return nu_mle, cal_mle, dict(base, reason="G-crps: reshaped cone robustly "
                                     "worse on proper score across blocks {2,3,4}")

    return nu_c, cal_c, dict(
        base, applied=True, to=[nu_c, round(cal_c, 3)],
        cov50=dict(mle=round(c50_mle, 4), reshaped=round(c50_c, 4),
                   lono_heldout=round(lono50, 4)),
        delta_ll=round(ll_max - _loglik(u, nu_c, cal_c), 2),
        crps_parity_ci={b: [round(float(ci[0]), 4), round(float(ci[1]), 4)]
                        for b, ci in cis.items()},
        note="90% edge held exactly (cal*T95 unchanged); 25-75 band reshaped "
             "to catch half; adopted under R-SHAPE-01's five guards")


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
    df = load_ohlc(raw_csv_path, market=profile.code)
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
def refresh_market(market, new_csvs, raw_csv_lookup, update_registry=True,
                   tag=DEFAULT_TAG):
    """market: profile code, e.g. 'SA'
    new_csvs: dict {name: raw_csv_path} for names touched THIS session
              (new names, or existing names with updated OHLC)
    raw_csv_lookup: dict {name: raw_csv_path} for EVERY name on the panel
              (old names not touched this session need their raw path too,
              so LONO/pooled rescoring can run against full current history)
    update_registry: if True (default — the historical interactive behaviour
              this whole session used), writes straight to fitted_configs.json
              and appends to market_fits_log.md. Set False when called from
              auto_refresh.py's unattended path: writing the registry must go
              through the materiality gate, or an unattended degraded/partial
              re-run (e.g. one name's raw CSV missing) silently corrupts the
              registry even when production (market_profiles.py) is correctly
              protected. Caught 11-Jul-2026 while building auto_refresh.py.
    tag:      horizon set (see HORIZON_SETS). '60d' is the retired
              session-counted gate kept for the grandfathered session-counted
              cohorts; '3m' is the live calendar-anchored gate. Panels and
              content hashes are namespaced per tag, so refreshing one horizon
              set never invalidates the other's cache.
    Returns a result dict; also writes panel files always (panel files are
    training scaffolding, not a verdict — see build_panel_file)."""
    profile = PROFILES[market]
    _hset(tag)
    os.makedirs(PANELS_DIR, exist_ok=True)
    hashes = _load_hashes()

    # 1. rebuild ONLY the panels whose raw CSV actually changed (content hash).
    #    This is what makes posting one stock cheap: 1 rebuild, not N.
    rebuilt = []
    for name, path in new_csvs.items():
        h = _file_hash(path)
        key = f"{market}_{name}" if tag == '60d' else f"{market}_{name}_{tag}"
        if hashes.get(key) != h or not os.path.exists(panel_path(market, name, tag)):
            build_panel_file(market, name, path, profile, tag=tag)
            hashes[key] = h
            rebuilt.append(name)
    _save_hashes(hashes)

    # 2. pool 'u' across the FULL current panel (old + new), break-filtered
    names = sorted(set(existing_panel_names(market, tag)) | set(new_csvs))
    panel = {n: apply_breaks(pd.read_csv(panel_path(market, n, tag)), profile) for n in names}
    names = [n for n in names if len(panel[n]) > 0]
    pooled_u = np.concatenate([panel[n]['u'].values for n in names])
    nu_pool, s_pool = fit_nu_scale(pooled_u)
    cal_pool = shrink_cal(s_pool)
    # [R-SHAPE-01] guarded mid-band reshape: production shape is the ridge point
    # whose 50% band catches half, IF every guard passes; MLE shape otherwise.
    nu_pool, cal_pool, reshape_note = reshape_mid_band(panel, names, nu_pool, cal_pool)

    # 3. LONO per-name verdicts + pooled market verdict — all via fast_rescore,
    #    which is bit-for-bit identical to re-running the engine (verified) but
    #    skips the O(n^2) HAR refit. The naive path timed out on the full library.
    per_name = {}
    for n in names:
        r = panel[n]
        if 'origin_idx' not in r.columns:
            per_name[n] = dict(note="panel predates origin_idx — supply the raw CSV to rebuild")
            continue
        if len(names) >= 2:
            u = np.concatenate([panel[m]['u'].values for m in names if m != n])
            nu_l, s_l = fit_nu_scale(u); cal_l = shrink_cal(s_l)
        else:
            nu_l, cal_l = nu_pool, cal_pool
        c = fast_rescore(r, nu_l, cal_l)
        cb = r['crps_b'].values
        spot = r['spot'].values
        cn, cbn = c / spot, cb / spot
        sk = float(1 - cn.sum() / cbn.sum())
        sk_raw = float(1 - c.sum() / cb.sum())
        verd, detail = robust_verdict(cn, cbn)
        nu_disp = round(float(nu_l), 3) if nu_l < 200 else "Gaussian"
        per_name[n] = dict(nu=nu_disp, width_cal=round(float(cal_l), 3),
                            skill=round(sk, 4), skill_raw_basis=round(sk_raw, 4),
                            verdict=verd,
                            ci_block2=[round(float(detail[2][0]), 3),
                                       round(float(detail[2][1]), 3)])

    allc, allb, allc_r, allb_r = [], [], [], []
    weights = {}
    for n in names:
        r = panel[n]
        if 'origin_idx' not in r.columns:
            continue
        c = fast_rescore(r, nu_pool, cal_pool)
        cb = r['crps_b'].values; spot = r['spot'].values
        allc.append(c / spot); allb.append(cb / spot)
        allc_r.append(c); allb_r.append(cb)
        weights[n] = float((cb / spot).sum())
    ac, ab = np.concatenate(allc), np.concatenate(allb)
    market_skill = float(1 - ac.sum() / ab.sum())
    lo, hi, market_verdict = verdict_ci(ac, ab, block=6)
    lo, hi = float(lo), float(hi)
    acr, abr = np.concatenate(allc_r), np.concatenate(allb_r)
    market_skill_raw = float(1 - acr.sum() / abr.sum())
    tot = sum(weights.values()) or 1.0
    top_name = max(weights, key=weights.get) if weights else None
    top_share = round(weights[top_name] / tot, 3) if top_name else None

    result = dict(
        market=market, market_name=profile.name,
        fit_date=datetime.date.today().isoformat(),
        panel_names=names, windows=len(pooled_u),
        rebuilt_this_run=rebuilt,
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
        mid_band_reshape=reshape_note,
        per_name=per_name,
    )

    if update_registry:
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
             (f"Mid-band reshape [R-SHAPE-01]: applied from "
              f"{result['mid_band_reshape']['mle_shape']} — "
              f"{result['mid_band_reshape']['note']}\n"
              if result.get('mid_band_reshape', {}).get('applied') else
              f"Mid-band reshape [R-SHAPE-01]: not applied "
              f"({result.get('mid_band_reshape', {}).get('reason', 'n/a')}).\n"),
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
