"""significance_pooled.py -- SIGNED pre-registered pooled test, interim power.

H0 critical values re-simulated at the run's REAL per-cohort, per-market block
dimensions (30,000 replications), mirroring the pooled estimator exactly
(within-market percentile ranks -> pooled average-rank Spearman; within-market
z-scored returns -> pooled tercile spread on stable-sorted factor percentiles).
Block bootstrap {2,3,4}, TRUE drop-one-name jackknife (market:name keyed --
EG:ADIB and AE:ADIB are different listings), cohort-share check, the SS6
five-part ADOPT checklist, and power simulated at the same interim dimensions
(8,000 reps; true Spearman rho induced via bivariate normals with Pearson
r = 2 sin(pi*rho/6)).

Seeds: H0 rng 42, bootstrap 0, power 7. B_H0=30000 (chunked), B_POWER=8000.
"""
import pickle
import numpy as np
from scipy.stats import spearmanr, rankdata

OUT = '/home/claude/selection'
with open(f'{OUT}/pooled_results.pkl', 'rb') as f:
    results = pickle.load(f)

FACTORS = ['F1', 'F2', 'F3', 'F4', 'F5', 'F6']
EXPECTED_SIGN = {'F1': 1, 'F2': -1, 'F3': -1, 'F4': 1, 'F5': 1, 'F6': 1}
MARKETS = ['EG', 'AE', 'SA']
ALPHA_SINGLE = 0.05
ALPHA_BONF = 0.05 / 6
B_H0 = 30000
B_BOOT = 5000
B_POWER = 8000
CHUNK = 5000
MIN_NAMES = 6
RHO_GRID = [0.03, 0.05, 0.08, 0.10]


def rank_pearson(A, Bm):
    """Row-wise Spearman via average ranks (mirrors scipy.spearmanr on ties)."""
    ra = rankdata(A, method='average', axis=1)
    rb = rankdata(Bm, method='average', axis=1)
    ra = ra - ra.mean(axis=1, keepdims=True)
    rb = rb - rb.mean(axis=1, keepdims=True)
    num = (ra * rb).sum(axis=1)
    den = np.sqrt((ra ** 2).sum(axis=1) * (rb ** 2).sum(axis=1))
    return np.where(den > 0, num / den, 0.0)


def pooled_stat_batch(sizes, B, rng, rho=0.0, sign=1):
    """B replications of (pooled IC, pooled spread) for one cohort with market
    block sizes `sizes`. rho=0 -> H0. rho>0 -> true Spearman rho in direction
    `sign` via bivariate normal latents (Pearson r = 2 sin(pi rho/6))."""
    r = 2.0 * np.sin(np.pi * rho / 6.0)
    fac_pct, ret_pct, ret_z = [], [], []
    for nb in sizes:
        Z1 = rng.standard_normal((B, nb))
        Z2 = rng.standard_normal((B, nb))
        fac_lat = sign * (r * Z1 + np.sqrt(1.0 - r * r) * Z2)
        Rf = fac_lat.argsort(axis=1).argsort(axis=1).astype(np.float64)
        fac_pct.append(Rf / (nb - 1))
        Rv = Z1.argsort(axis=1).argsort(axis=1).astype(np.float64)
        ret_pct.append(Rv / (nb - 1))
        z = (Z1 - Z1.mean(axis=1, keepdims=True)) / Z1.std(axis=1, ddof=1, keepdims=True)
        ret_z.append(z)
    FP = np.concatenate(fac_pct, axis=1)
    RP = np.concatenate(ret_pct, axis=1)
    RZ = np.concatenate(ret_z, axis=1)
    ic = rank_pearson(FP, RP)
    k = FP.shape[1] // 3
    order = np.argsort(FP, axis=1, kind='stable')
    top = np.take_along_axis(RZ, order[:, -k:], axis=1).mean(axis=1)
    bot = np.take_along_axis(RZ, order[:, :k], axis=1).mean(axis=1)
    return ic, top - bot


def sim_mean_stats(structures, B, rng, rho=0.0, sign=1):
    """Mean-across-cohorts IC and spread, B replications, chunked."""
    ics = np.empty(B)
    sps = np.empty(B)
    done = 0
    while done < B:
        b = min(CHUNK, B - done)
        mat_ic = np.empty((b, len(structures)))
        mat_sp = np.empty((b, len(structures)))
        for i, sizes in enumerate(structures):
            ic, sp = pooled_stat_batch(sizes, b, rng, rho, sign)
            mat_ic[:, i] = ic
            mat_sp[:, i] = sp
        ics[done:done + b] = mat_ic.mean(axis=1)
        sps[done:done + b] = mat_sp.mean(axis=1)
        done += b
    return ics, sps


def block_bootstrap_ci(ics, sizes=(2, 3, 4), B=B_BOOT, seed=0):
    r = np.random.default_rng(seed)
    n = len(ics)
    out = {}
    for k in sizes:
        starts = np.arange(max(1, n - k + 1))
        nb = int(np.ceil(n / k))
        means = np.empty(B)
        for i in range(B):
            picks = r.choice(starts, nb)
            sel = np.concatenate([np.arange(s, min(s + k, n)) for s in picks])
            means[i] = ics[sel].mean()
        out[k] = (float(np.quantile(means, 0.05)), float(np.quantile(means, 0.95)))
    return out


def pct_rank(v):
    return (rankdata(v, method='average') - 1.0) / (len(v) - 1.0)


def cohort_pooled_ic(blocks_dict, drop=None):
    """Recompute a cohort's pooled IC from stored raw blocks, optionally
    dropping one 'MKT:NAME'. Returns None if the cohort dies (min-6 rules)."""
    fac_pct, ret_pct = [], []
    for m in MARKETS:
        if m not in blocks_dict:
            continue
        b = blocks_dict[m]
        names, fv, rv = b['names'], np.array(b['fac']), np.array(b['fwd'])
        if drop is not None and drop[0] == m and drop[1] in names:
            keep = [i for i, n in enumerate(names) if n != drop[1]]
            if len(keep) < MIN_NAMES:
                continue  # this market block dies
            fv, rv = fv[keep], rv[keep]
        fac_pct.append(pct_rank(fv))
        ret_pct.append(pct_rank(rv))
    if not fac_pct:
        return None
    fp = np.concatenate(fac_pct)
    rp = np.concatenate(ret_pct)
    if len(fp) < MIN_NAMES:
        return None
    return float(spearmanr(fp, rp)[0])


rng = np.random.default_rng(42)
prng = np.random.default_rng(7)
summary = {}

for fac in FACTORS:
    rows = results[fac]
    structures = [[len(r['blocks'][m]['names']) for m in MARKETS if m in r['blocks']]
                  for r in rows]
    ics = np.array([r['ic'] for r in rows])
    spreads = np.array([r['spread'] for r in rows])
    mean_ic, mean_sp = ics.mean(), spreads.mean()
    exp = EXPECTED_SIGN[fac]

    # --- estimator-mirror sanity: vectorized path must equal stored spearman ---
    for r_ in rows[:5] + rows[-5:]:
        chk = cohort_pooled_ic(r_['blocks'])
        assert abs(chk - r_['ic']) < 1e-9, (fac, r_['date'], chk, r_['ic'])

    # --- H0 critical values at the real dimensions ---
    h0_ic, h0_sp = sim_mean_stats(structures, B_H0, rng)
    if exp > 0:
        crit_ic_s, crit_ic_b = np.quantile(h0_ic, 1 - ALPHA_SINGLE), np.quantile(h0_ic, 1 - ALPHA_BONF)
        crit_sp_s, crit_sp_b = np.quantile(h0_sp, 1 - ALPHA_SINGLE), np.quantile(h0_sp, 1 - ALPHA_BONF)
        clears_s, clears_b = mean_ic > crit_ic_s, mean_ic > crit_ic_b
        sp_clears_b = mean_sp > crit_sp_b
    else:
        crit_ic_s, crit_ic_b = np.quantile(h0_ic, ALPHA_SINGLE), np.quantile(h0_ic, ALPHA_BONF)
        crit_sp_s, crit_sp_b = np.quantile(h0_sp, ALPHA_SINGLE), np.quantile(h0_sp, ALPHA_BONF)
        clears_s, clears_b = mean_ic < crit_ic_s, mean_ic < crit_ic_b
        sp_clears_b = mean_sp < crit_sp_b
    sign_ok = np.sign(mean_ic) == exp

    # --- rule 3: per-market signs ---
    mkt_means = {}
    for m in MARKETS:
        mic = [r['per_mkt_ic'][m] for r in rows if m in r['per_mkt_ic']]
        if mic:
            mkt_means[m] = (len(mic), float(np.mean(mic)))
    mkts_agree = sum(1 for m, (n, v) in mkt_means.items() if np.sign(v) == exp)

    # --- block bootstrap + BOUNDARY flag (same rule as the EG pass) ---
    ci = block_bootstrap_ci(ics)
    boundary = False
    if sign_ok and clears_s:
        sgn = [(lo > 0) if exp > 0 else (hi < 0) for k, (lo, hi) in ci.items()]
        boundary = not all(sgn) and any(sgn)

    # --- TRUE drop-one-name jackknife (market:name) ---
    all_keys = sorted(set((m, n) for r in rows for m in r['blocks'] for n in r['blocks'][m]['names']))
    flips, jk_min, jk_max = [], mean_ic, mean_ic
    breaks_bar = []
    for key in all_keys:
        jk = []
        for r_ in rows:
            v = cohort_pooled_ic(r_['blocks'], drop=key) if key[0] in r_['blocks'] and key[1] in r_['blocks'][key[0]]['names'] else r_['ic']
            if v is not None:
                jk.append(v)
        if not jk:
            continue
        mjk = float(np.mean(jk))
        jk_min, jk_max = min(jk_min, mjk), max(jk_max, mjk)
        if np.sign(mjk) != np.sign(mean_ic) and abs(mean_ic) > 1e-9:
            flips.append((f'{key[0]}:{key[1]}', mjk))
        if clears_b:
            still = (mjk > crit_ic_b) if exp > 0 else (mjk < crit_ic_b)
            if not still:
                breaks_bar.append(f'{key[0]}:{key[1]}')

    # --- rule 5: cohort share of the pooled mean ---
    tot = ics.sum()
    max_share = float(np.max(ics / tot)) if abs(tot) > 1e-9 else np.nan

    # --- five-part checklist ---
    rule1 = bool(clears_b and sign_ok)
    rule2 = bool(sp_clears_b and np.sign(mean_sp) == exp)
    rule3 = bool(mkts_agree >= 2)
    rule4 = bool((not flips) and (not breaks_bar))
    rule5 = bool(not np.isnan(max_share) and max_share <= 0.25) if abs(tot) > 1e-9 else False
    adopted = all([rule1, rule2, rule3, rule4, rule5]) and fac != 'F5'

    if fac == 'F5':
        verdict = 'BLOCKED (volume DQ)'
    elif not sign_ok:
        verdict = 'WRONG SIGN'
    elif adopted:
        verdict = 'BOUNDARY' if boundary else 'ADOPTED'
    elif clears_b:
        verdict = 'clears Bonf, fails rules'
    elif clears_s:
        verdict = 'single-only'
    else:
        verdict = 'not detected'

    # --- power at these interim dimensions ---
    power = {}
    for rho in RHO_GRID:
        p_ic, _ = sim_mean_stats(structures, B_POWER, prng, rho=rho, sign=exp)
        power[rho] = float(np.mean(p_ic > crit_ic_b) if exp > 0 else np.mean(p_ic < crit_ic_b))

    print(f'\n{fac}  N={len(rows)}  mean pooled IC={mean_ic:+.4f}  spread={mean_sp:+.4f}z  '
          f'sign_ok={sign_ok}')
    print(f'   crit IC single/Bonf: {crit_ic_s:+.4f} / {crit_ic_b:+.4f}   '
          f'crit spread Bonf: {crit_sp_b:+.4f}')
    print(f'   rules: 1(IC>Bonf)={rule1} 2(spread)={rule2} 3(mkts {mkts_agree}/3)={rule3} '
          f'4(jackknife)={rule4} 5(maxshare={max_share if not np.isnan(max_share) else float("nan"):.2f})={rule5}'
          if not np.isnan(max_share) else
          f'   rules: 1={rule1} 2={rule2} 3(mkts {mkts_agree}/3)={rule3} 4={rule4} 5=n/a (mean~0)')
    print(f'   per-market: ' + '  '.join(f'{m} n={n} IC={v:+.4f}' for m, (n, v) in mkt_means.items()))
    print(f'   block-boot 90% CI: ' + '  '.join(f'b{k}[{lo:+.4f},{hi:+.4f}]' for k, (lo, hi) in ci.items()))
    print(f'   jackknife: range [{jk_min:+.4f},{jk_max:+.4f}]; sign flips: '
          f'{[f[0] for f in flips] if flips else "none"}'
          + (f'; breaks Bonf bar: {breaks_bar}' if breaks_bar else ''))
    print(f'   power at Bonf bar (interim dims): ' +
          '  '.join(f'rho={r_}:{100*p:.0f}%' for r_, p in power.items()))
    print(f'   VERDICT: {verdict}')

    summary[fac] = dict(n_cohorts=len(rows), mean_ic=float(mean_ic), mean_spread=float(mean_sp),
                        sign_ok=bool(sign_ok), crit_ic_single=float(crit_ic_s),
                        crit_ic_bonf=float(crit_ic_b), crit_sp_single=float(crit_sp_s),
                        crit_sp_bonf=float(crit_sp_b), rules=[rule1, rule2, rule3, rule4, rule5],
                        mkt_means=mkt_means, mkts_agree=mkts_agree, ci=ci,
                        jk_flips=[f[0] for f in flips], jk_range=(float(jk_min), float(jk_max)),
                        breaks_bar=breaks_bar, max_share=max_share, power=power,
                        verdict=verdict, boundary=bool(boundary))

with open(f'{OUT}/pooled_summary.pkl', 'wb') as f:
    pickle.dump(summary, f)
print('\nSaved pooled_summary.pkl')
