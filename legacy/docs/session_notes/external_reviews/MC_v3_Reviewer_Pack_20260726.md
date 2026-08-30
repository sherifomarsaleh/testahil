# Testahil MC Engine v3 — Independent Reviewer Pack
**Snapshot date: 26 July 2026 · prepared for external review of the latest Monte-Carlo work**

---

## 0. READ FIRST — provenance and how to verify

- **Repository (public, read-only):** `https://github.com/sherifomarsaleh/testahil`
- **Production branch snapshot packed here:** `main` @ commit `bb6a89914b1b27013a3add404b6dadf2323668d1` (2026-07-23T14:01:05Z).
- **Pending-adoption branch packed here:** `feat/adaptive-width-overlay-eg` @ `1518c23df7a8a9e1418f03bcf2807396059c1abf` (2026-07-24). **NOT merged into main** — verified live on 26-Jul-2026. Open PR; see §3.
- Every code listing in §6 is **verbatim** from those commits (SHA-256 per file in §6.0; a script re-extracted each block and diffed it byte-for-byte against the fetched file before this pack was issued — zero differences).
- **Volatility warning:** every fitted number quoted here (ν, width_cal, verdicts, skills, panel sizes) is a **snapshot at the commit above**. An unattended GitHub-Actions pipeline refits a whole market whenever one stock's OHLC file is posted, so these numbers go stale without notice. Before relying on any figure, re-read the live source of truth:
  `curl -s https://raw.githubusercontent.com/sherifomarsaleh/testahil/main/engine/market_profiles.py`
- `engine/market_profiles.py` **is the single source of truth** (it is what production imports). `engine/fitted_configs.json` is a *derived mirror* and — as found on 26-Jul-2026 — is currently **stale** (still carries the retired one-name XAU self-fit and is missing EG/DSCW). Nothing in production reads the mirror; it is excluded from this pack's code section for that reason and flagged as a regeneration item.
- Determinism: all production forecasts use `seed=42`, `n_paths=50,000`. Backtests seed per-origin (`seed + origin_index`) so windows are independent but reproducible.

## 1. What the engine is (one page)

**Name:** carry-anchored YZ-HAR-t, `engine/mc_v3.py` (production since 10-Jul-2026; `mc_v2.py` is a legacy reference that v3 imports primitives from — both listed in §6).

| Component | Specification |
|---|---|
| **Drift** | Carry anchor `ln(1+rf) − ln(1+q)` scaled to horizon — rf from the per-market policy schedule in `market_profiles.py`, q per name. Plus an optional shrunk signal alpha (dead-zone 0.5σ, clip ±2z, cap ±0.5σ_H) — **currently ablated OFF in every market** (`signal_active=False` everywhere, set by panel ablation, never assumption). So live drift = pure carry. |
| **Width** | Gap-aware Yang-Zhang daily-variance proxy (overnight² + Rogers-Satchell) → pooled log-HAR (lags 1/5/22) forecast of mean forward daily variance, with lognormal half-variance bias correction `exp(s²/2)` and a 0.8/0.2 log-space shrink toward the trailing-252d proxy mean. Multiplied by a per-market cross-fitted `width_cal`. |
| **Shape** | Unit-variance Student-t(ν) via per-path chi-square mixture; ν fitted per market by MLE on pooled LONO-cross-fitted standardized 60d residuals. Gaussian limit is the numeric sentinel `nu=250.0`. |
| **Benchmark (null)** | Carry-anchored lognormal random walk, trailing-252d close-close vol — same carry as the engine, so measured skill can never harvest the time-value of money. |
| **Gate (Step 0)** | 5-yr walk-forward, h=60, non-overlapping windows; pooled **scale-normalized** CRPS skill (crps/spot) with calendar-block bootstrap 90% CI → PASS / PARITY / FAIL. A name-level FAIL must be robust across bootstrap block sizes {2,3,4}; a block-dependent sign flip = BOUNDARY, recorded PARITY-flagged. |
| **Data gate (Step 0.0)** | `data_quality.py` runs before any series enters a panel. Detection is principled: each exchange's own daily price limit defines what one session can physically do (per-market thresholds — EGX ±20%, Tadawul ±10%, ADX ±15%, QE ±10%, KOSPI ±30%, NSE ±20%, US/metals none). Two **known defects** found 26-Jul-2026 on extended history — see §4 and the proposed patch in §6.6. |

**Standing promotion rule:** nothing enters the engine — from a human or from the pipeline — without surviving the same out-of-sample (LONO / held-out) test the forecasts must survive. This rule has teeth: it killed CRPS-based (ν, width_cal) selection (won in-sample, lost under LONO in both markets tested), shrinkage v2, Amihud-conditioned ν, illiquidity-conditioned width, Round-8 FV-pull, and both external systems reviewed this week (§4).

**Fit identifiability caveat (standing):** ν is weakly identified — on some panels every ν from 5 to Gaussian sits inside the 95% likelihood interval, and ν trades off against width_cal. The fitted object is the **(ν, width_cal) pair**, honestly summarized as the cone they jointly produce (`width_cal × q95(t(ν))` — also the quantity the pipeline's materiality gate watches). Never read either coordinate alone as precise.

## 2. Fitted state at this snapshot (from `market_profiles.py` @ bb6a899)

All markets carry-only. Full fit provenance (panel composition, ablations, data repairs, break-cut evidence) is embedded as `fit_meta` strings inside the code listing §6.3 — deliberately, so the provenance travels with the numbers.

| Market | ν | width_cal | Panel | Market verdict (skill, 90% CI basis) | Name-level exceptions |
|---|---|---|---|---|---|
| EG (EGX) | 4.0 | 0.972 | 30 names, 478 windows | PASS +0.0204 under the adopted 2022-03-21 break cut | 0 FAILs; 5+ BOUNDARY(PARITY-flagged) |
| SA (Tadawul) | 6.0 | 1.063 | 11 names, 190 w | PARITY +0.0023 | **ELM robust FAIL −0.0142** |
| AE (ADX/DFM) | 10.0 | 1.028 | 18 names, 274 w | PARITY +0.0033 | ALPHADHABI back to PARITY (was robust FAIL); ADCB BOUNDARY; LULU PROVISIONAL(insufficient-windows) |
| KR (KOSPI) | 250.0 (Gaussian) | 1.154 | 3 names | PARITY +0.0144 | **LGES robust FAIL −0.0268** (over-coverage signature: cov90=1.00, PIT 0.471) |
| US | 12.0 | 1.014 | 3 names, 54 w | PARITY | — |
| IN (NSE) | 250.0 (Gaussian) | 0.930 | 3 names, 51 w | PARITY +0.0046 | — |
| QA (QE) | 12.0 | 0.972 | 3 names, 54 w | PARITY −0.010 | **IQCD robust FAIL −0.018** |
| XAU (Gold+Silver) | 20.0 | 1.035 | 2 names, 86 w | PASS +0.0099 (first non-circular metals fit, LONO) | — |
| XPT (Platinum) | 250.0 (Gaussian) | 0.853 | 1 name, 62 w | PARITY −0.0004 — PROVISIONAL single-name self-fit | — |
| GB / BR | — | — | — | placeholder stubs, no fit | — |

Three robust name-level FAILs live in the system (ELM, LGES, IQCD). Two of the three (LGES; formerly ALPHADHABI) share the **over-coverage** signature — cone too wide for a name whose own vol sits below the panel average, PIT well-centred — which is precisely the failure mode the adaptive-width overlay (§3) was built for. **Metals honesty note:** XAU/XPT remain the weakest calibration in the system — 2-name and single-name panels; platinum's self-fit is circular by construction; do not read metals cones with EGX/GCC confidence.

## 3. The latest adopted work: adaptive per-stock width overlay (EG-only)

`engine/adaptive_width.py` (§6.5) — **adopted 23-Jul-2026, EG-only, going-forward, currently on an unmerged feature branch and DORMANT even if merged** (history gate; see below). This is the single most recent engine change and the centrepiece of the review request.

- **What it is:** an ONLINE per-name multiplier on cone width, learned from that name's own resolved 60-day standardized residuals: `m_raw = clip(sqrt(EWMA_0.85(u²)), 0.7, 1.5)`, then gentled + dead-zoned: `mult = 1 + 0.5·sign(m_raw−1)·max(0, |m_raw−1| − 0.10)`. Walk-forward safe (only resolved windows enter).
- **What it is not:** a refit. Pooled (ν, width_cal), carry drift, and tail ν are untouched; flag off ⇒ bit-for-bit the prior engine.
- **Promotion evidence (the claim, exactly):** 30-name EG panel, strict LONO / held-out FINAL split, block bootstrap {2,3,4}: proper score at **parity** (log-CRPS 0.0154 → 0.0152, zero cost — this is *not* a CRPS gain) while per-name calibration improved: pooled |std_u−1| 0.096 → 0.069; cov90 0.903 → 0.893 (both in-band); 24/30 names moved closer to std_u=1. Replicated as the panel grew (11/11, 13/16, 17/21, 24/30). It cleared the same OOS gate that killed the CRPS-selection and Amihud arms.
- **History gate:** below `MIN_WINDOWS=28` resolved windows the multiplier is forced to exactly 1.0 (the overlay over-corrects on ~5-yr histories). At this snapshot the production EG library carries ~17 windows/name ⇒ the overlay is **inert everywhere** even if merged. The 15-yr EG library ingested 26-Jul-2026 (not yet pushed) moves 26/30 names past the gate — that upload, not more modelling, is what activates it.
- **Scope:** every other market runs mult=1.0 until it clears the same LONO gate on its own panel.

## 4. The latest evaluation work (22–26 Jul 2026): what was tested and what fell

The reviewer should treat these as the system's current evidentiary frontier. Primary docs live in the project (`claude/v4_lab/*`, `claude/external_reviews/*`, `claude/data/*`); condensed here.

**4.1 Two external MC systems reviewed and rejected (26-Jul).** CHAR-MC: shipped code assigned coverage/CRPS by *matching the asset's name string* (its scoring function was never called); repaired properly it is 3.75% worse than production in CRPS, robust across blocks, beating production on 3/26 names. Gemini-MC: rejected as submitted (panel FAIL −0.0977 post-break, negative in 27/28 series; cov90 0.807); fully repaired it passes coverage but still does not beat production. **Convergent value extracted:** four independent implementations put EGX ν ≈ 4 (settled); three independent tests find no exploitable EGX 20-day momentum in either direction (carry-only stands); four independent rejections map the boundary of per-name width adaptation — only the gentled/dead-zoned/history-gated form (§3) survives.

**4.2 Multi-horizon gate protocol — ADOPTED as standing practice (26-Jul).** At a single horizon two width parameters are perfectly confounded; the gate ran h=60 only while T+20 is published and graded. Production re-verified through its own chain at h ∈ {5,10,20,40,60} (28 EGX series, 5,468 windows): cov90 ∈ [0.885, 0.907] at every horizon, and reusing the h=60 fit at T+20 gives cov90 = 0.910 vs 0.907 purpose-fitted — **the published T+20 cone is in band**. (An external claim that short horizons were 24% too narrow was measured on the RW *benchmark*, not production — recorded so nobody "fixes" a cone that isn't broken.)

**4.3 Three production defects found by extending EGX history to 2011–2012 (26-Jul) — open, patch proposed, not pushed:**
1. **`data_quality.py` corrupts series containing a zero close** — vendor writes Price=0.00 with valid O/H/L; `log(0)=−inf` → back-adjust factor of inf/0 rescales *all prior history* (on OCDI: 536 rows to zero). 17 rows across 6 of 28 series.
2. **Spike-and-revert bad prints mis-repaired as corporate actions** — two opposite rescalings that don't cancel leave prior history permanently mis-scaled (BTFH +7.9%/−8.1%, HELI +2.9%) and keep the bad print. Fix: revert-scan before back-adjusting (§6.6).
3. **Price-space CRPS is non-convergent for a lognormal-t** — a Student-t has no MGF, so E[exp(σT)] = ∞ for every σ>0; one window carried 99.45% of a 1,293-window panel's CRPS under production's own simulator. Invisible at median σ_h; detonates on high-σ, low-price windows. Proposed fix: score in **log space** (finite, scale-free; worst-window share 99.45% → 0.80%). Needs its own PR + re-verification that existing short-panel verdicts are unchanged.

**4.4 Open empirical questions the reviewer should weigh:**
- **Full-sample PARITY:** production's post-2022 EGX PASS (+0.0128, log-space, 461 w) degrades to PARITY (−0.0023) over 2012–2026 (1,293 w). Either the 2022-03-21 break cut does real work (serial-devaluation regime) or the PASS is partly sample-specific — currently unresolved, honestly recorded.
- **Break-cut re-test on the full 30-name panel (26-Jul):** long-history calibration vs the adopted post-2022-03-21 cut is PARITY at every block size — the cut **stands**. (An earlier same-day 26-name result claiming LONG wins did not survive panel completion; retracted. Lesson recorded: block-bootstrap robustness ≠ panel-composition robustness.)
- **Indices FAIL under the stock fit:** EGX30/EGX70 scored for the first time — PROD FAILs (cov90 0.772) — but confounded by q=0 on a price index; index profile (sourced dividend yield, index-appropriate limits, own fit) is a prerequisite before any index verdict or publication.
- **EG 15-yr library (32 series, 97,756 cleaned sessions) ingested but NOT pushed** — blocked behind the dq patch (the current gate would corrupt 6 series on ingest). EGX70 has no usable pre-2019 intraday range; RAYA is flat High==Low on 34.6% of sessions (decision needed before it enters a fit).

**4.5 Rejected-and-closed register (do not revive):** raw secular / unshrunk trend drift · CRPS-based (ν,width_cal) selection · shrinkage v2 (71 names) · Amihud→dynamic-ν · illiquidity-conditioned width · Roll bid-ask denoising (precondition fails: 28/30 EG names have *positive* lag-1 autocorr) · Round-8 FV-pull (policy: fundamentals stay out of MC drift) · Hurst-gated drift, ACI tail-stretch, HARQ-as-submitted (Gemini) · CHAR-MC (θ saturation, γ momentum, price-bucket λ). Each has a project doc with the walk-forward evidence.

## 5. The unattended loop (context for "who changes the numbers")

`engine/raw_ohlc/{MARKET}/{TICKER}.csv` is a persistent library; posting one file triggers a GitHub-Actions refit of that whole market against the full library (content-hashed panels; a closed-form fast rescore verified bit-for-bit against the engine). Mechanical refits auto-commit; the run **stops and opens a PR** when a materiality tripwire fires: an existing name's verdict changes, a new name arrives already FAILING, the market verdict changes, a panel carries a name with no raw data, or the published 90% cone moves >5% — measured on `width_cal × q95(t(ν))`, never on ν or width_cal separately (they trade off). Engine changes ship via feature branch + PR, never direct to main. Verification-by-import is mandatory before any commit of `market_profiles.py` (a bare `nu=Gaussian` once parsed cleanly and died only at import; the Gaussian limit is therefore the numeric sentinel 250.0).

## 6. Code — verbatim listings

Reading order: 6.1 primitives → 6.2 engine → 6.3 profiles/fits → 6.4 data gate → 6.5 overlay (branch) → 6.6 proposed patch.

### 6.0 File manifest (SHA-256 of the exact bytes embedded below)

| § | File | SHA-256 |
|---|---|---|
| 6.1 | `engine/mc_v2.py` | `a40d31fe719b3e817c84250a5fcdfa4f1cfe257569eb6d6c43f8a61549c14500` |
| 6.2 | `engine/mc_v3.py` | `c28a25061f54cf34481910ecac0324df073fc32c8bfab1a29f53f615a7e32fab` |
| 6.3 | `engine/market_profiles.py` | `4464d0be2fed9727417382aceea68459cef6a643f8d806ad811f71681a920b5c` |
| 6.4 | `engine/data_quality.py` | `aff2d1281925b92913be4ef0fc5c81d30cc144330c92bc572c11648c755d2ebf` |
| 6.5 | `engine/adaptive_width.py` | `32c614ee5bbe7e71afcc5745e4bfcc0d629a89c2c5e3600a1079a546c78d70b9` |
| 6.6 | `dq_patch.py` | `d07b5d5770f9d6fb596865bb4c10af9498b2eeb17301c8ed6de888ddeb74e7f5` |


### 6.1 engine/mc_v2.py (main @ bb6a899) — v2 primitives imported by v3 (YZ proxy, HAR features, CRPS/Winkler, legacy reference engine)

```python
"""mc_v2.py — Testahil YZ-HAR Monte Carlo engine (v2).
Width : pooled log-HAR cascade (variance lags 1/5/22) on a gap-aware
        Yang-Zhang variance proxy (overnight^2 + Rogers-Satchell),
        projecting the average daily variance over the next H sessions.
Shape : unit-variance Student-t(5) via a per-path chi-square variance
        mixture on the Gaussian diffusion (60-day aggregate exactly t5).
Drift : asset-class-conditional — expanding-window mean daily log-return
        (secular) when enabled; zero otherwise. No kvol floor.
"""
import numpy as np
import pandas as pd


def load_ohlc(path):
    df = pd.read_csv(path)
    df.columns = [c.replace('﻿', '').strip() for c in df.columns]
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
    df = df.sort_values('Date').reset_index(drop=True)
    for c in ['Price', 'Open', 'High', 'Low']:
        df[c] = pd.to_numeric(df[c].astype(str).str.replace(',', ''), errors='coerce')
    df = df.dropna(subset=['Price', 'Open', 'High', 'Low']).reset_index(drop=True)
    return df


def yz_variance_proxy(df):
    """Gap-aware daily variance proxy: overnight-return^2 + Rogers-Satchell."""
    o, h, l, c = df['Open'].values, df['High'].values, df['Low'].values, df['Price'].values
    c_prev = np.roll(c, 1)
    with np.errstate(divide='ignore', invalid='ignore'):
        overnight = np.log(o / c_prev)
        rs = np.log(h / c) * np.log(h / o) + np.log(l / c) * np.log(l / o)
    v = overnight ** 2 + rs
    v[0] = np.nan
    v = np.where(v <= 0, np.nan, v)  # guard degenerate bars
    return pd.Series(v, index=df.index)


def har_features(v, idx):
    """log variance averages at lags 1 / 5 / 22 ending at idx (inclusive)."""
    if idx < 22:
        return None
    w = v.iloc[:idx + 1].ffill()
    v1 = w.iloc[-1]
    v5 = w.iloc[-5:].mean()
    v22 = w.iloc[-22:].mean()
    if not np.all(np.isfinite([v1, v5, v22])) or min(v1, v5, v22) <= 0:
        return None
    return np.log([v1, v5, v22])


def fit_har(v, end_idx, horizon=60, min_obs=60):
    """Fit log-HAR: log(mean var over next `horizon` d) ~ log v1,v5,v22.
    Uses only data up to end_idx (walk-forward safe)."""
    X, y = [], []
    vv = v.ffill()
    for t in range(22, end_idx - horizon):
        f = har_features(v, t)
        if f is None:
            continue
        fut = vv.iloc[t + 1:t + 1 + horizon]
        m = fut.mean()
        if np.isfinite(m) and m > 0:
            X.append(f)
            y.append(np.log(m))
    if len(y) < min_obs:
        return None
    X = np.column_stack([np.ones(len(y)), np.array(X)])
    beta, *_ = np.linalg.lstsq(X, np.array(y), rcond=None)
    return beta


def har_forecast_daily_var(v, origin_idx, beta, horizon=60):
    f = har_features(v, origin_idx)
    if f is None or beta is None:
        w = v.ffill().iloc[max(0, origin_idx - 251):origin_idx + 1]
        return float(w.mean())
    return float(np.exp(beta[0] + beta[1:] @ f))


def simulate_terminal(spot, daily_var, horizon, drift_daily=0.0,
                      n_paths=50000, seed=42, nu=5):
    """Terminal-price distribution at T+horizon under the YZ-HAR width,
    unit-variance t(nu) shape (per-path chi-square mixture), given drift."""
    rng = np.random.default_rng(seed)
    sigma_h = np.sqrt(daily_var * horizon)
    z = rng.standard_normal(n_paths)
    chi = rng.chisquare(nu, n_paths)
    mix = np.sqrt((nu - 2) / chi)          # unit-variance t(nu) multiplier
    shocks = z * mix * sigma_h
    logret = drift_daily * horizon + shocks
    return spot * np.exp(logret)


def simulate_paths(spot, daily_var, horizon, drift_daily=0.0,
                   n_paths=50000, seed=42, nu=5):
    """Full path array (n_paths, horizon+1) for fan charts / touch ladders."""
    rng = np.random.default_rng(seed)
    sd = np.sqrt(daily_var)
    z = rng.standard_normal((n_paths, horizon))
    chi = rng.chisquare(nu, n_paths)
    mix = np.sqrt((nu - 2) / chi)[:, None]
    incr = drift_daily + z * mix * sd
    logp = np.cumsum(incr, axis=1)
    paths = np.empty((n_paths, horizon + 1))
    paths[:, 0] = spot
    paths[:, 1:] = spot * np.exp(logp)
    return paths


def crps_sample(samples, y):
    """Sample CRPS: E|X−y| − 0.5·E|X−X'| (unbiased pairwise form)."""
    s = np.sort(np.asarray(samples, dtype=float))
    n = len(s)
    t1 = np.mean(np.abs(s - y))
    i = np.arange(1, n + 1)
    t2 = 2.0 / (n * n) * np.sum((2 * i - n - 1) * s)
    return t1 - 0.5 * t2


def winkler(lo, hi, y, alpha=0.10):
    w = hi - lo
    if y < lo:
        w += 2.0 / alpha * (lo - y)
    elif y > hi:
        w += 2.0 / alpha * (y - hi)
    return w


def trailing_cc_vol(close, idx, window=252):
    lr = np.diff(np.log(close[max(0, idx - window):idx + 1]))
    return float(np.std(lr, ddof=1))


def backtest(df, horizon=60, step=None, secular_drift=False,
             n_paths=8000, seed=42, min_history=260):
    """Walk-forward Step 0 backtest. Non-overlapping when step=horizon."""
    if step is None:
        step = horizon
    v = yz_variance_proxy(df)
    close = df['Price'].values
    n = len(df)
    rows = []
    origin = min_history
    while origin + horizon < n:
        beta = fit_har(v, origin, horizon=horizon)
        dv = har_forecast_daily_var(v, origin, beta, horizon=horizon)
        spot = close[origin]
        drift = 0.0
        if secular_drift:
            lr = np.diff(np.log(close[:origin + 1]))
            drift = float(np.mean(lr))
        samp = simulate_terminal(spot, dv, horizon, drift_daily=drift,
                                 n_paths=n_paths, seed=seed + origin)
        y = close[origin + horizon]
        # benchmark: zero-drift lognormal random walk, trailing cc vol
        sig_b = trailing_cc_vol(close, origin)
        rngb = np.random.default_rng(seed + origin + 1)
        bench = spot * np.exp(sig_b * np.sqrt(horizon) * rngb.standard_normal(n_paths))
        q = np.percentile(samp, [5, 10, 25, 50, 75, 90, 95])
        qb = np.percentile(bench, [5, 95])
        pit = float(np.mean(samp <= y))
        rows.append(dict(
            origin=df['Date'].iloc[origin], spot=spot, realized=y,
            crps=crps_sample(samp, y), crps_bench=crps_sample(bench, y),
            wink=winkler(q[0], q[6], y), wink_bench=winkler(qb[0], qb[1], y),
            pit=pit,
            in50=q[2] <= y <= q[4], in80=q[1] <= y <= q[5], in90=q[0] <= y <= q[6],
            p5=q[0], p25=q[2], p50=q[3], p75=q[4], p95=q[6],
            anchor_vol=np.sqrt(dv * 252), drift_daily=drift,
        ))
        origin += step
    r = pd.DataFrame(rows)
    if len(r) == 0:
        return r, {}
    skill = 1 - r['crps'].sum() / r['crps_bench'].sum()
    iskill = 1 - r['wink'].sum() / r['wink_bench'].sum()
    summary = dict(n=len(r), crps_skill=skill, interval_skill=iskill,
                   cov50=r['in50'].mean(), cov80=r['in80'].mean(),
                   cov90=r['in90'].mean(), pit_mean=r['pit'].mean())
    return r, summary
```

### 6.2 engine/mc_v3.py (main @ bb6a899) — PRODUCTION engine: carry-anchored YZ-HAR-t, backtest, pooled gate, bootstrap, (nu, width_cal) MLE

```python
"""mc_v3.py — Testahil Monte Carlo engine v3 ("carry-anchored YZ-HAR-t").

Drift : carry anchor  ln(1+rf) - ln(1+q)  scaled to horizon (forward-consistent
        null for a PRICE forecast; rf from the MarketProfile schedule)
        + shrunk signal alpha  IC * sigma_H * sign * clip(z)  (dead zone 0.5,
        clip ±2, hard cap ±0.5*sigma_H), active per profile fallback rule.
Width : gap-aware Yang-Zhang proxy + pooled log-HAR (lags 1/5/22) forecasting
        mean forward daily variance, WITH the lognormal half-variance bias
        correction exp(s^2/2) and a 0.8/0.2 log-space shrink toward the
        trailing-252d proxy mean. Multiplied by a cross-fitted width_cal.
Shape : unit-variance Student-t(nu) via per-path chi-square mixture; nu fitted
        per market on pooled standardized 60d residuals (LONO cross-fitted),
        replacing the hard-coded t(5).
Bench : carry-anchored lognormal random walk, trailing 252d cc vol — the same
        carry as the engine, so skill isolates signal + width, never the anchor.
Gate  : pooled panel CRPS skill with a calendar-block bootstrap 90% CI ->
        PASS (CI>0) / PARITY (straddles 0) / FAIL (CI<0); pinball-0.5 and
        Winkler-90 skills reported alongside.
"""
import numpy as np
import pandas as pd
from mc_v2 import load_ohlc, yz_variance_proxy, crps_sample, winkler, trailing_cc_vol


# ---------------------------------------------------------------- width (HAR+)
def fit_har_v3(v, end_idx, horizon=60, min_obs=60):
    """log-HAR fit as in v2 but also returns residual variance s2 for the
    lognormal bias correction. Walk-forward safe (data up to end_idx only)."""
    from mc_v2 import har_features
    X, y = [], []
    vv = v.ffill()
    for t in range(22, end_idx - horizon):
        f = har_features(v, t)
        if f is None:
            continue
        fut = vv.iloc[t + 1:t + 1 + horizon]
        m = fut.mean()
        if np.isfinite(m) and m > 0:
            X.append(f); y.append(np.log(m))
    if len(y) < min_obs:
        return None, None
    Xd = np.column_stack([np.ones(len(y)), np.array(X)])
    ya = np.array(y)
    beta, *_ = np.linalg.lstsq(Xd, ya, rcond=None)
    resid = ya - Xd @ beta
    s2 = float(np.var(resid, ddof=Xd.shape[1]))
    return beta, s2


def har_forecast_v3(v, origin_idx, beta, s2, horizon=60,
                    shrink=0.8, bias_correct=True):
    """Bias-corrected, shrunk forecast of mean forward daily variance."""
    from mc_v2 import har_features
    w = v.ffill().iloc[max(0, origin_idx - 251):origin_idx + 1]
    v_trail = float(w.mean())
    f = har_features(v, origin_idx)
    if f is None or beta is None:
        return v_trail
    pred = beta[0] + beta[1:] @ f
    if bias_correct and s2 is not None:
        pred = pred + 0.5 * s2
    # 0.8/0.2 log-space shrink toward the trailing proxy mean (noise control)
    logv = shrink * pred + (1 - shrink) * np.log(max(v_trail, 1e-12))
    return float(np.exp(logv))


# ---------------------------------------------------------------- drift
def carry_log_h(profile, date, q_annual, horizon):
    rf = profile.carry_rate(date)
    return (np.log1p(rf) - np.log1p(q_annual)) * horizon / 252.0


def signal_z(close, idx, kind):
    """Standardized signal at origin idx (walk-forward safe)."""
    if kind is None or idx < 260:
        return 0.0
    lr = np.diff(np.log(close[max(0, idx - 251):idx + 1]))
    sd = np.std(lr, ddof=1)
    if not np.isfinite(sd) or sd <= 0:
        return 0.0
    if kind == "mom_12_1":
        if idx < 252:
            return 0.0
        r = np.log(close[idx - 21] / close[idx - 252])
        return float(r / (sd * np.sqrt(231)))
    if kind == "rev_1m":
        r = np.log(close[idx] / close[idx - 21])
        return float(r / (sd * np.sqrt(21)))
    return 0.0


def signal_alpha(profile, close, idx, sigma_h, dead=0.5, clipz=2.0):
    if not profile.signal_active or profile.signal_type is None:
        return 0.0, 0.0
    z = signal_z(close, idx, profile.signal_type)
    if abs(z) < dead:
        return 0.0, z
    a = profile.ic * sigma_h * profile.signal_sign * float(np.clip(z, -clipz, clipz))
    a = float(np.clip(a, -0.5 * sigma_h, 0.5 * sigma_h))
    return a, z


# ---------------------------------------------------------------- simulation
def simulate_terminal_v3(spot, sigma_h, drift_log_h, nu=8.0,
                         n_paths=50000, seed=42):
    rng = np.random.default_rng(seed)
    z = rng.standard_normal(n_paths)
    if nu is None or nu > 200:
        mix = 1.0
    else:
        chi = rng.chisquare(nu, n_paths)
        mix = np.sqrt((nu - 2) / chi)
    return spot * np.exp(drift_log_h + z * mix * sigma_h)


def simulate_paths_v3(spot, daily_var, horizon, drift_log_h, nu=8.0,
                      n_paths=50000, seed=42, width_cal=1.0):
    rng = np.random.default_rng(seed)
    sd = np.sqrt(daily_var) * width_cal
    z = rng.standard_normal((n_paths, horizon))
    if nu is None or nu > 200:
        mix = np.ones((n_paths, 1))
    else:
        chi = rng.chisquare(nu, n_paths)
        mix = np.sqrt((nu - 2) / chi)[:, None]
    incr = drift_log_h / horizon + z * mix * sd
    logp = np.cumsum(incr, axis=1)
    paths = np.empty((n_paths, horizon + 1))
    paths[:, 0] = spot
    paths[:, 1:] = spot * np.exp(logp)
    return paths


# ---------------------------------------------------------------- backtest
def backtest_v3(df, profile, horizon=60, q_annual=0.0, use_signal=True,
                nu=None, width_cal=None, n_paths=20000, seed=42,
                min_history=260, legacy_mode=None):
    """Walk-forward, non-overlapping. legacy_mode replicates v2 for the ladder:
      'v2_egx_dev' -> t5, zero carry, expanding-mean secular drift (old EGX dev)
      'v2_zero'    -> t5, zero carry, zero drift (old non-EGX)
    Benchmark is ALWAYS the carry-anchored trailing-vol lognormal RW (new null).
    nu/width_cal default to the profile's own fitted config (standing per-market
    fit rule, 10-Jul-2026) when not passed explicitly.
    """
    if nu is None:
        nu = profile.nu if getattr(profile, 'nu', None) else 8.0
    if width_cal is None:
        width_cal = getattr(profile, 'width_cal', 1.0)
    v = yz_variance_proxy(df)
    close = df['Price'].values
    n = len(df)
    rows = []
    origin = min_history
    while origin + horizon < n:
        date = df['Date'].iloc[origin]
        spot = close[origin]
        y = close[origin + horizon]

        # --- engine drift & width per rung ---
        if legacy_mode is not None:
            from mc_v2 import fit_har, har_forecast_daily_var
            beta = fit_har(v, origin, horizon=horizon)
            dv = har_forecast_daily_var(v, origin, beta, horizon=horizon)
            sigma_h = np.sqrt(dv * horizon)
            if legacy_mode == 'v2_egx_dev':
                drift = float(np.mean(np.diff(np.log(close[:origin + 1])))) * horizon
            else:
                drift = 0.0
            nu_use, z = 5.0, 0.0
            alpha = 0.0
        else:
            beta, s2 = fit_har_v3(v, origin, horizon=horizon)
            dv = har_forecast_v3(v, origin, beta, s2, horizon=horizon)
            sigma_h = np.sqrt(dv * horizon) * width_cal
            carry = carry_log_h(profile, date, q_annual, horizon)
            alpha, z = (signal_alpha(profile, close, origin, sigma_h)
                        if use_signal else (0.0, signal_z(close, origin, profile.signal_type)))
            drift = carry + alpha
            nu_use = nu

        samp = simulate_terminal_v3(spot, sigma_h, drift, nu=nu_use,
                                    n_paths=n_paths, seed=seed + origin)

        # --- carry-anchored benchmark (fixed null across all rungs) ---
        carry_b = carry_log_h(profile, date, q_annual, horizon)
        sig_b = trailing_cc_vol(close, origin) * np.sqrt(horizon)
        rngb = np.random.default_rng(seed + origin + 1)
        bench = spot * np.exp(carry_b + sig_b * rngb.standard_normal(n_paths))

        q_e = np.percentile(samp, [5, 25, 50, 75, 95])
        q_b = np.percentile(bench, [5, 25, 50, 75, 95])
        rows.append(dict(
            origin=date, spot=spot, realized=y, z=z, alpha=alpha,
            drift=drift, sigma_h=sigma_h,
            crps=crps_sample(samp, y), crps_b=crps_sample(bench, y),
            pin50=0.5 * abs(y - q_e[2]), pin50_b=0.5 * abs(y - q_b[2]),
            wink=winkler(q_e[0], q_e[4], y), wink_b=winkler(q_b[0], q_b[4], y),
            pit=float(np.mean(samp <= y)),
            in50=q_e[1] <= y <= q_e[3], in80=np.percentile(samp, 10) <= y <= np.percentile(samp, 90),
            in90=q_e[0] <= y <= q_e[4],
            w90=(q_e[4] - q_e[0]) / spot, w90_b=(q_b[4] - q_b[0]) / spot,
            med_disp=(q_e[2] / spot - 1),
            u=(np.log(y / spot) - drift) / sigma_h if sigma_h > 0 else np.nan,
        ))
        origin += horizon
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- pooled gate
def pooled_scores(frames):
    r = pd.concat(frames, ignore_index=True)
    out = dict(
        n=len(r),
        crps_skill=1 - r['crps'].sum() / r['crps_b'].sum(),
        pin50_skill=1 - r['pin50'].sum() / r['pin50_b'].sum(),
        wink_skill=1 - r['wink'].sum() / r['wink_b'].sum(),
        cov50=r['in50'].mean(), cov80=r['in80'].mean(), cov90=r['in90'].mean(),
        pit_mean=r['pit'].mean(),
        w90_ratio=(r['w90'] / r['w90_b']).mean(),
        med_abs_disp=r['med_disp'].abs().mean(),
    )
    return out, r


def block_bootstrap_ci(r, B=3000, seed=0, block='6M', level=90):
    """Calendar-block bootstrap of pooled CRPS skill: resample half-year blocks
    jointly across names (preserves cross-sectional dependence)."""
    rng = np.random.default_rng(seed)
    blk = pd.PeriodIndex(pd.DatetimeIndex(r['origin']), freq=block.replace('M', 'M'))
    r = r.assign(_blk=pd.DatetimeIndex(r['origin']).to_period('2Q').astype(str))
    blocks = r['_blk'].unique()
    nb = len(blocks)
    g = {b: r[r['_blk'] == b] for b in blocks}
    bs = []
    for _ in range(B):
        pick = rng.choice(blocks, nb, replace=True)
        c = sum(g[b]['crps'].sum() for b in pick)
        cb = sum(g[b]['crps_b'].sum() for b in pick)
        bs.append(1 - c / cb)
    bs = np.array(bs)
    lo, hi = np.percentile(bs, [(100 - level) / 2, 100 - (100 - level) / 2])
    return float(lo), float(hi), float(np.mean(bs > 0))


def verdict(lo, hi):
    if lo > 0:
        return "PASS"
    if hi < 0:
        return "FAIL"
    return "PARITY"


# ---------------------------------------------------------------- shape fit
def fit_nu_scale(u, nu_grid=(4, 5, 6, 8, 10, 12, 15, 20, 30, 1e9),
                 s_grid=np.linspace(0.75, 1.40, 66)):
    """MLE over (nu, scale) for standardized 60d residuals u; unit-variance
    t(nu) parameterization (scale multiplies the unit-variance t)."""
    from scipy import stats
    u = np.asarray(u, float)
    u = u[np.isfinite(u)]
    best = (-np.inf, 8.0, 1.0)
    for nu in nu_grid:
        if nu > 200:
            for s in s_grid:
                ll = stats.norm.logpdf(u / s).sum() - len(u) * np.log(s)
                if ll > best[0]:
                    best = (ll, float(nu), float(s))
        else:
            k = np.sqrt(nu / (nu - 2))  # unit-variance t: x = t_nu / k
            for s in s_grid:
                ll = stats.t.logpdf(u * k / s, nu).sum() + len(u) * (np.log(k) - np.log(s))
                if ll > best[0]:
                    best = (ll, float(nu), float(s))
    return best[1], best[2]


def shrink_cal(s, w=0.7, lo=0.85, hi=1.30):
    return float(np.clip(1 + w * (s - 1), lo, hi))
```

### 6.3 engine/market_profiles.py (main @ bb6a899) — SINGLE SOURCE OF TRUTH: per-market profiles, carry schedules, fitted (nu, width_cal) + full fit provenance

```python
"""market_profiles.py — Testahil universal-engine Market Profile registry (v3).

One engine, markets as data. Each profile supplies:
  carry anchor (local risk-free schedule, annual, decimal),
  signal spec (type/sign/IC — literature prior, re-estimated on pooled panels),
  tail nu (None -> fit on pooled panel, LONO cross-fitted),
  calendar + limit notes, regime-break dates (vol estimated post-break only).

Carry convention: price-forecast drift = ln(1+rf) - ln(1+q), i.e. the
forward-consistent carry for a PRICE (not total-return) series. q = dividend
yield per name (continuous approximation).

Backtest carry schedules are piecewise policy-rate-derived approximations,
GATE-NEUTRAL by construction (engine and benchmark carry the same anchor, so
the CRPS/pinball/interval skill difference is unaffected by the level).
Live-forecast anchors must be freshly sourced per Cost_of_Capital_Reference.md
staleness rules before any publish.

STANDING PER-MARKET FIT RULE (user, 10-Jul-2026 — "every market is different"):
every market Testahil operates in carries its OWN fitted (nu, width_cal) from
its OWN pooled panel — never a borrowed archetype presented as final. A new
market's FIRST action is fitting its own shape/width on its first covered
names' panel; until that fit exists, any borrowed config is FLAGGED and no
name-level FAIL under a borrowed config is treated as real (borrowed configs
fabricate FAILs — QGTS under Egypt's devaluation-fat nu=4 is the canonical
case; PARITY under its own Gaussian/0.92 fit). Single-name fits are
PROVISIONAL until the panel reaches 2+ names; refits follow the panel-growth
cadence (~2+ new names or ~1yr new windows) with the outlier-triggered
immediate-review exception. backtest_v3 resolves nu/width_cal from the
profile automatically when not passed explicitly.

ROBUST-VERDICT RULE (10-Jul-2026): a name-level FAIL requires the bootstrap
CI to sit entirely below zero ROBUSTLY across block sizes {2,3,4} (10k draws,
50k paths). A verdict that flips sign with the block choice is BOUNDARY ->
recorded as PARITY with a flag, reviewed at the name's next live grade.
(ALINMA is the current boundary case.)
"""
from dataclasses import dataclass, field
from typing import Optional, List, Tuple
import pandas as pd

Sched = List[Tuple[str, float]]  # [(effective_date_iso, annual_rate_decimal)]


@dataclass
class MarketProfile:
    code: str
    name: str
    carry_schedule: Sched            # policy-derived, backtest use (gate-neutral)
    rf_live: float                   # current sourced/estimated anchor for live forecasts
    rf_live_source: str
    signal_type: Optional[str]       # 'mom_12_1' | 'rev_1m' | None
    signal_sign: int                 # +1 momentum, -1 contrarian/reversal
    ic: float                        # information-coefficient prior
    signal_active: bool              # False -> carry-only (fallback rule)
    nu: Optional[float] = None       # None -> fit from pooled panel
    width_cal: float = 1.0           # per-market cone multiplier from the panel shape fit
    fit_meta: str = ""               # provenance of the (nu, width_cal) fit
    breaks: List[str] = field(default_factory=list)
    notes: str = ""

    def carry_rate(self, date) -> float:
        d = pd.Timestamp(date)
        r = self.carry_schedule[0][1]
        for eff, rate in self.carry_schedule:
            if d >= pd.Timestamp(eff):
                r = rate
        return r


FED_SCHEDULE = [
    ("2009-01-01", 0.0013), ("2015-12-17", 0.0038), ("2016-12-15", 0.0063),
    ("2017-03-16", 0.0088), ("2017-06-15", 0.0113), ("2017-12-14", 0.0138),
    ("2018-03-22", 0.0163), ("2018-06-14", 0.0188), ("2018-09-27", 0.0213),
    ("2018-12-20", 0.0238), ("2019-08-01", 0.0213), ("2019-09-19", 0.0188),
    ("2019-10-31", 0.0163), ("2020-03-16", 0.0013), ("2022-03-17", 0.0038),
    ("2022-05-05", 0.0088), ("2022-06-16", 0.0163), ("2022-07-28", 0.0238),
    ("2022-09-22", 0.0313), ("2022-11-03", 0.0388), ("2022-12-15", 0.0438),
    ("2023-02-02", 0.0463), ("2023-03-23", 0.0488), ("2023-05-04", 0.0513),
    ("2023-07-27", 0.0538), ("2024-09-19", 0.0488), ("2024-11-08", 0.0463),
    ("2024-12-19", 0.0438), ("2025-09-18", 0.0413), ("2025-10-30", 0.0388),
    ("2025-12-11", 0.0363), ("2026-06-18", 0.0363),
]  # Fed funds target midpoints (policy history; Jun-2026 3.50-3.75% per cached note)

EGYPT = MarketProfile(
    code="EG", name="Egypt (EGX)",
    carry_schedule=[
        ("2020-01-01", 0.0825), ("2022-03-21", 0.0925), ("2022-05-19", 0.1125),
        ("2022-10-27", 0.1325), ("2022-12-22", 0.1625), ("2023-03-30", 0.1825),
        ("2023-08-03", 0.1925), ("2024-02-01", 0.2125), ("2024-03-06", 0.2725),
        ("2025-04-17", 0.2500), ("2025-05-22", 0.2400), ("2025-08-28", 0.2200),
        ("2025-10-02", 0.2100), ("2026-02-20", 0.2000), ("2026-04-02", 0.1950),
    ],
    rf_live=0.1950,
    rf_live_source=("CBE main operation rate 19.50% (corridor 19.00/20.00), held since "
                    "2 Apr 2026 [CBE Q1-2026 MPR, cached Cost_of_Capital_Reference.md]. "
                    "Short-tenor anchor for a 60-trading-day horizon; 10Y alt = 22.55% "
                    "(investing.com 3-Jul-2026). FLAG: source a fresh 3M T-bill auction "
                    "yield before first EGX publish under v3 — bills have traded above "
                    "the corridor; 19.50% is the conservative sourced floor."),
    signal_type="rev_1m", signal_sign=-1, ic=0.08, signal_active=False,
    nu=4.0, width_cal=0.972,
    fit_meta=(
        "REFIT 11-Jul-2026 on the FULL 27-name EG panel (351 post-break windows) - "
        "supersedes the 7-name/115-window fit (nu=4, cal=0.965, signal ON). The fit "
        "is CONVERGED: going 25 -> 27 names (adding COMI and ORAS) left nu=4 and "
        "cal=0.909 completely unchanged. Three changes, each tested: (1) "
        "DATA-QUALITY GATE (data_quality.py) cleans every series first, with a "
        "PER-MARKET artifact threshold derived from the exchange's daily price "
        "limit (EGX +/-20% -> every clean name tops out at |log move| <= 0.223, so "
        "anything past 0.29 cannot be trading). Two artifacts found: EFIH carried "
        "flat 0.50 pre-IPO placeholder rows (a fake +333% log jump) and an "
        "unadjusted 3:2 split on 26-May-2025; OCDI/SODIC carried an unadjusted "
        "corporate action on 14-Aug-2025 showing as a fake -73% crash. OCDI was IN "
        "the production 7-name fit - but repairing it does NOT move nu (still 4; "
        "cal 0.979 -> 0.958), so Egypt's fat tail is GENUINE devaluation-jump risk, "
        "not a data bug. (2) BREAK FILTERING ADOPTED: calibrating on "
        "post-2023-01-11 origins only beats calibrating on all windows "
        "out-of-sample (LONO +0.0211 vs +0.0198, both scored on the same post-break "
        "windows) AND narrows the cone from cal=0.972 to 0.909. (3) SIGNAL ABLATED "
        "OFF - this was the LAST active signal in the system. On the panel the "
        "empirical IC of rev_1m is +0.018: the house prior's contrarian sign=-1 is "
        "REFUTED and the magnitude is ~0. Ablation: carry-only +0.0252 beats "
        "signal-ON +0.0211; the signal helps in only 13/25 names; paired bootstrap "
        "P(signal helps)=0.31. Fallback rule applies. The rev_1m/IC-0.08 prior is "
        "retained for re-estimation, but signal_active=False. EVERY market in the "
        "system is now carry-only. RESULT: panel PASS +0.0270 CI[+0.018,+0.038] on "
        "the scale-normalized gate; top-name weight 8.9% (vs 42% under the old "
        "price-weighted gate). ZERO name-level FAILs. PASS: CCAP +0.090, EMFD "
        "+0.078, HELI +0.070, PHDC +0.066, LCSW +0.051, OCDI +0.048, PRDC +0.037. "
        "BOUNDARY(PARITY-flagged): FWRY, ETEL, EFIH, GBCO, ABUK. 15 PARITY (incl. "
        "the two names added last: COMI +0.023, ORAS +0.021). NB PHDC moved to PASS "
        "on refreshed OHLC (1328 rows to 28-Jun-2026, vs a stale 1223-row project "
        "copy) - relevant, since PHDC carries the live ledger cohorts. The old "
        "7-name panel was sector-concentrated (5 of 7 were RE developers); the "
        "27-name panel is cross-sector and its lower headline skill is the more "
        "honest number. UPDATE 13-Jul-2026: CLHO added (28 -> 29 names, 351 -> 377 windows), reviewed "
        "in PR #4 and merged by Sherif. nu=4.0 and cal=0.909 UNCHANGED. CLHO itself: skill -0.0199, "
        "PARITY -- unremarkable, inside the existing PARITY range (ISPH -0.044, OIH -0.011). The one "
        "side-effect: CCAP's OWN verdict moved PASS -> BOUNDARY(PARITY-flagged) (skill +0.0906, still "
        "positive, CI[0.006,0.207] -- straddles the boundary, not a sign flip), which is why the "
        "materiality gate correctly stopped for review rather than auto-committing. Market panel: "
        "PASS +0.0259 CI[0.017,0.036], materially the same as pre-CLHO. "
        "UPDATE 22-Jul-2026: DSCW added (29 -> 30 names, 462 -> 478 windows under the "
        "adopted 2022-03-21 break cut below). NOT material by itself - nu and cal "
        "UNCHANGED at 4.0/0.972. DSCW itself: skill +0.0117, BOUNDARY(PARITY-flagged) "
        "CI[-0.007,+0.027] - unremarkable, inside the existing PARITY/BOUNDARY range."),
    # EGYPT BREAKS RE-DERIVED, 13-Jul-2026 (Sherif: "devaluation is a way of life in
    # Egypt, even sharp ones") -- and he is right, which changes the answer.
    #
    # THE OLD LIST WAS WRONG ON ITS FACE: it ended at 2023-01-11 and MISSED the largest
    # devaluation in the series, 6-Mar-2024 (EGP ~30.9 -> ~50.2). apply_breaks cuts at
    # MAX(breaks), so the live filter only worked BY ACCIDENT -- it happened to leave the
    # Mar-2024 float INSIDE the sample. Had the list been "complete", the filter would have
    # excised the very jump the fat tail (nu=4) exists to price.
    #
    # THE DEEPER POINT: a devaluation is not a one-off regime change here, it is the
    # process -- Mar-2022, Oct-2022, Jan-2023, Mar-2024. Filtering them out filters out
    # the risk. Cutting at the TRUE last break (2024-03-06) leaves a devaluation-free
    # sample, and the fit obediently thins the tail (nu 4 -> 5) and narrows the cone
    # (cal 0.909 -> 0.850). It then WINS the skill test -- because it is scored on a calm
    # period. That is the trap, and the original adoption test walked into it: it compared
    # configs "both scored on the same post-break windows", which is circular by construction.
    #
    # MEASURED on the committed 29-name panel. The column that matters is coverage during
    # the windows that actually CONTAIN the Mar-2024 float:
    #   cut          nu    cal   windows  panel skill  FAILs   dev-window 90% coverage
    #   none/2016   4.0  0.958      508     +0.0169      1            86.2%
    #   2022-03-21  4.0  0.972      462     +0.0204      0            86.2%   <-- ADOPTED
    #   2023-01-11  4.0  0.909      377     +0.0259      0            82.8%   (retired)
    #   2024-03-06  5.0  0.850      237     +0.0376      1            82.8%   (the trap)
    #
    # 2022-03-21 is where Egypt's SERIAL-devaluation regime begins: the pound sat flat at
    # ~15.7 for years, then stepped Mar-22 -> Oct-22 -> Jan-23 -> Mar-24. Cutting there keeps
    # THREE devaluations in the calibration sample -- so the cone is the widest of any config
    # (0.972), devaluation coverage is the best available (86.2%), and there are ZERO
    # name-level FAILs. Going further back to 2016 drags in the stable, managed post-float
    # years -- a genuinely different regime -- and it HURTS (skill falls, CLHO turns FAIL)
    # without improving jump coverage at all.
    #
    # Cost, stated honestly: headline panel skill falls +0.0259 -> +0.0204. We accept that.
    # A cone that is too narrow during a devaluation is the failure mode that loses money,
    # and the lower headline number is the more honest one.
    breaks=["2016-11-03", "2022-03-21"],
    notes=("Literature: no EGX momentum; overreaction/short-term reversal supported "
           "(EGX event studies; Kuwait 1m reversal ~3.1%/mo t≈4.4 as GCC analogue). "
           "Signal sign/IC re-estimated on the 6-name pooled panel each cycle."),
)

SAUDI = MarketProfile(
    code="SA", name="Saudi Arabia (Tadawul)",
    carry_schedule=[
        ("2020-01-01", 0.0100), ("2022-03-17", 0.0125), ("2022-05-05", 0.0175),
        ("2022-06-16", 0.0225), ("2022-07-28", 0.0300), ("2022-09-22", 0.0375),
        ("2022-11-03", 0.0450), ("2022-12-15", 0.0500), ("2023-02-02", 0.0525),
        ("2023-03-23", 0.0550), ("2023-05-04", 0.0575), ("2023-07-27", 0.0600),
        ("2024-09-19", 0.0550), ("2024-11-08", 0.0525), ("2024-12-19", 0.0500),
        ("2025-09-18", 0.0475), ("2025-10-30", 0.0450), ("2025-12-11", 0.0425),
        ("2026-06-18", 0.0400),
    ],
    rf_live=0.0425,
    rf_live_source=("SAMA repo-anchored ESTIMATE ~4.25% (Fed 3.50-3.75% post Jun-2026 "
                    "FOMC + historical SAMA +50bp spread). FLAG per house no-UST-shortcut "
                    "rule: a direct SAR govt sukuk quote was inaccessible via available "
                    "tools this session (investing.com/WGB tables JS-walled) — replace "
                    "with FTSE SAGBI or iBoxx Tadawul SAR sukuk yield before publish. "
                    "Sensitivity: ±50bp = ±0.12% on the 60d median — immaterial vs band."),
    signal_type="mom_12_1", signal_sign=-1, ic=0.06, signal_active=False,
    nu=6.0, width_cal=1.063,
    fit_meta=(
        "REFIT 11-Jul-2026 on the 11-name SA panel "
        "(ACWA/ALINMA/ARAMCO/ELM/EXTRA/MAADEN/RAJHI/RIBL/SABIC/SNB/STC, 190 windows) "
        "— supersedes the 2-name fit (nu=5, cal=1.28). The old cal=1.28 was CAP-BOUND "
        "thin-panel conservatism, not real Tadawul vol: on an 11-name panel the MLE "
        "lands at scale=1.09 -> cal=1.063, a ~17% narrower cone. LONO out-of-sample "
        "check of the SELECTION PROCEDURE: MLE +0.0008 beats both a direct CRPS-skill "
        "grid search (-0.0011, overfits) and the old incumbent (-0.0000) — "
        "MLE-on-residuals retained as the house method. Panel PARITY +0.0023 "
        "CI[-0.004,+0.008] on the corrected scale-normalized gate. Per-name (LONO, "
        "robust blocks): RAJHI PASS +0.0151 (clean: PIT 0.495, width ratio 0.991); "
        "ELM robust FAIL -0.0142 across blocks {2,3,4}; all others PARITY. Signal "
        "still OFF — 11 names clears the ~5-name threshold, so the mom_12_1 IC is now "
        "estimable and should be ablated at the next refit. "),
    breaks=["2015-06-15"],
    notes=("Signal OFF (fallback rule): 1-name panel cannot establish IC; literature "
           "sign-unstable (contrarian post-2015 opening). Runs carry-only until the "
           "Saudi panel reaches ~5 covered names."),
)

# ---- Approved-design stubs (priors from the two profile tables signed off 09/10-Jul) ----
USA = MarketProfile("US", "United States", FED_SCHEDULE, 0.0363,
    "UST 10Y 4.58% (tradingeconomics 8-Jul-2026, cached CoC-Reference); use 3M bill 3.71% "
    "(investing.com 10-Jul-2026) for the 60d carry at publish.",
    "mom_12_1", +1, 0.05, False, nu=12.0, width_cal=1.014,
    fit_meta=("Fitted 10-Jul-2026 on the 3-name US panel (AAPL/NVDA/TSLA, 54 windows, "
              "2021-2026): nu=12, cal=1.014 - thin tails like metals, far from EGX. "
              "SIGNAL ABLATION on this panel: carry-only (+0.012 CI[-0.006,+0.017]) "
              "marginally beats the mom_12_1 prior ON (+0.010 CI[-0.013,+0.019]) -> "
              "fallback rule applies, signal_active=False; the JT prior is retained "
              "for re-estimation at ~5 names. Panel verdict PARITY. Per-name "
              "(carry-only LONO, robust blocks): AAPL PARITY -0.002 (was BOUNDARY "
              "with the signal ON - the momentum prior was hurting it), NVDA PARITY "
              "+0.002, TSLA PARITY +0.015."),
    notes="Mature-market momentum prior (JT 12-1) - ablated OFF on the first panel; "
          "re-estimate as the panel grows.")
UK = MarketProfile("GB", "United Kingdom", [("2020-01-01", 0.0400)], 0.0400,
    "PLACEHOLDER — source gilt/3M at first UK study.", "mom_12_1", +1, 0.05, True,
    notes="Strong UK momentum literature.")
BRAZIL = MarketProfile("BR", "Brazil", [("2020-01-01", 0.1300)], 0.1300,
    "PLACEHOLDER — source Selic/DI at first BR study.", "mom_12_1", +1, 0.07, True,
    notes="EM momentum prior (Rouwenhorst).")
KOREA = MarketProfile("KR", "South Korea", [("2020-01-01", 0.0300)], 0.0300,
    "PLACEHOLDER — source KTB at first KR study.", None, +1, 0.03, False,
    nu=250.0, width_cal=1.154,
    fit_meta=(
        "REFIT 11-Jul-2026 on the 3-name KR panel after a MAJOR DATA REPAIR - "
        "supersedes nu=6/cal=1.070. THE INVESTING.COM KOREAN EXPORT CONTAINS "
        "PHANTOM NON-TRADING ROWS: ~160 rows per name carrying NaN volume and "
        "O=H=L=C, of which 144 of SAMSUNG's 170 fall on a SUNDAY (KOSPI is closed). "
        "Raw density is 276.8 rows/yr; after removing them it is 245.8/yr - exactly "
        "the KOSPI calendar. These phantom rows inject fake zero-return, "
        "zero-intraday-range days straight into the Yang-Zhang variance proxy, "
        "DEPRESSING the volatility estimate. The 10-Jul repair caught only the 13 "
        "pre/post-split price-scale rows (fixed by dividing by 5, which SYNTHESIZES "
        "a price on a day the market never opened); it never saw the ~160 phantom "
        "rows. They are now DROPPED, not rescaled. EFFECT: the tail goes 6 -> "
        "Gaussian and the cone WIDENS 1.070 -> 1.154 - the old fit was "
        "simultaneously too narrow AND falsely fat-tailed, an artifact of the "
        "depressed vol. Skill nevertheless IMPROVES: panel PARITY +0.0144 "
        "CI[-0.005,+0.017] (was +0.006). Per-name (LONO, robust blocks): SAMSUNG "
        "PARITY +0.0094, KAKAO PARITY +0.0022, LGES robust FAIL -0.0268 across "
        "blocks {2,3,4} - and its signature is OVER-COVERAGE: cov80=1.00 and "
        "cov90=1.00 (every outcome inside the 80% band), cone 1.112x the benchmark, "
        "PIT 0.471 (well centred). LGES is not mis-centred, it is simply too wide: "
        "it IPO'd Jan-2022, has the shortest history and only 13 windows, and the "
        "market-level width_cal over-widens a name whose own vol is below the panel "
        "average. This is the clearest case in the whole system for a NAME-LEVEL "
        "width_cal shrunk toward the market fit - proposed, NOT implemented, "
        "pending an out-of-sample test."),
    notes="Asia momentum-failure pattern: carry-only.")
UAE = MarketProfile("AE", "UAE (ADX/DFM)", FED_SCHEDULE, 0.0365,
    "Carry = USD/Fed policy path (AED hard-pegged); rf_live 3.65% = CBUAE Base Rate held "
    "17-Jun-2026. NB the peg 'never-UST' rule governs the VALUATION rf (AED govt bond) -- "
    "the MC carry correctly tracks the Fed for a pegged currency.", "rev_1m", -1, 0.06, False,
    nu=10.0, width_cal=1.028,
    fit_meta=(
        "REFIT 11-Jul-2026 on the 14-name AE panel (237 post-break windows), RE-RUN "
        "through the data-quality gate - supersedes nu=4/cal=1.070. Adds "
        "ADIB/DIB/TWOPOINTZERO/EAND to the prior 10. Tail moves 4 -> 10: the old "
        "fat tail was carried by IHC/EMAAR idiosyncratic swings on a smaller panel; "
        "four more well-behaved names dilute it. HONESTY NOTE: nu is only WEAKLY "
        "IDENTIFIED - every nu from 5 to Gaussian sits inside the 95% likelihood "
        "interval (nu=4 is only dlogL=2.23 away), and nu trades off against cal. "
        "The (nu,cal) PAIR is fitted; neither coordinate is individually precise. "
        "LONO OOS: this MLE config scores +0.0032 vs the incumbent's -0.0017. "
        "Data-quality gate dropped 3-5 stale no-trade rows each from EAND/ADCB/ADIB "
        "- immaterial (cal 1.056 -> 1.049, nu unchanged). BREAK FILTERING APPLIED: "
        "EAND's OHLC starts 2016, so 21 of its 39 windows predate the Jan-2022 "
        "workweek switch and are excluded from the calibration sample; unfiltered "
        "they pulled the fit to nu=6/cal=1.084. Panel PARITY +0.0049 "
        "CI[-0.004,+0.015]. Per-name: ALPHADHABI robust FAIL -0.0122 (cone 1.136x "
        "benchmark, cov90=0.94 vs a 0.90 target - over-wide, same signature as "
        "KR/LGES); all 13 others PARITY. Signal OFF; 14 names now clears the "
        "threshold for a rev_1m ablation. "
        "UPDATE 22-Jul-2026: BURJEEL/DEWA/LULU/SALIK added (14 -> 18 names, 237 -> 274 "
        "windows); ADIBUAE removed as a byte-identical duplicate of ADIB that was "
        "double-weighting ADIB's windows in every pooled and LONO fit (cmp-verified, "
        "not a data change). nu unchanged at 10; cal 1.049 -> 1.028 (narrower - the "
        "four new names are well-behaved). Panel PARITY +0.0033 CI[-0.005,+0.013]. "
        "MATERIALITY: two verdicts changed, both reviewed before merge (PR #13). "
        "ALPHADHABI: robust FAIL -0.0122 -> PARITY -0.0094 CI[-0.022,0.0] - removing "
        "the double-counted ADIB windows and adding four well-behaved names both moved "
        "the panel-average vol enough to bring ALPHADHABI's own cone back to a "
        "defensible width; no longer a robust FAIL under blocks {2,3,4}. ADCB: PARITY "
        "-> BOUNDARY(PARITY-flagged), skill +0.0259 CI[0.001,0.067] - straddles the "
        "boundary, not a sign flip; flagged for the next grade (ADCB is the bank "
        "reference-study exemplar, worth watching). New names: BURJEEL PARITY +0.0099, "
        "SALIK PARITY -0.0139, DEWA BOUNDARY(PARITY-flagged) -0.0056. LULU: only 2 "
        "non-overlapping windows since its Nov-2024 IPO - too thin for the robust "
        "{2,3,4}-block standard (block=3 has no valid start); verdict is "
        "PROVISIONAL(insufficient-windows) under the now-fixed verdict_ci (previously "
        "this crashed the entire daily AE run; see panel_refresh.py NOBLOCK fix, same "
        "PR). Re-resolves automatically once LULU accrues >=4 windows."),
    breaks=["2022-01-01"], notes=("Workweek switch Jan-2022: vol pool post-2022 only. "
    "CORRECTION 11-Jul-2026: re-run through the data_quality gate (EAND/ADCB/ADIB carried "
    "10 trading-halt rows with O=H=L=C and no volume, which flatten the YZ intraday range "
    "and bias the variance proxy DOWN). Immaterial as expected -- width_cal 1.056 -> 1.049, "
    "nu unchanged at 10, panel skill +0.0039 -> +0.0049, ALPHADHABI still a robust FAIL -- "
    "but the fit now conforms to the house cleaning gate."))
INDIA = MarketProfile("IN", "India (NSE)", [("2020-01-01", 0.0650)], 0.0650,
    "PLACEHOLDER — source 10Y G-Sec at first IN study.", "mom_12_1", +1, 0.07, False,
    nu=250.0, width_cal=0.930,
    fit_meta=(
        "REFIT 11-Jul-2026 on the 3-name IN panel (TMPV/RELIANCE/INFY, 51 windows, "
        "2021-2026), RE-RUN through the market-aware data-quality gate and the "
        "scale-normalized gate - EXACT REPRODUCTION of the 10-Jul fit: nu stays at "
        "the Gaussian limit, cal stays 0.930. Screened for the same phantom-row "
        "corruption found in the Korean export (144/170 of one Korean name's "
        "dropped rows fell on a Sunday, when the KOSPI is closed): India's export "
        "is CLEAN - 247.6 rows/yr across all three names, exactly the NSE calendar, "
        "zero phantom rows, no price-limit artifacts. Panel PARITY +0.0046 "
        "CI[-0.006,+0.016] on the corrected gate (was +0.002 on the old "
        "price-weighted one); top-name weight TMPV 43.7% (no single name dominates "
        "as badly as UAE's old IHC problem, but still the largest share of any "
        "3-name panel in the system - worth a 4th name). All three PARITY, zero "
        "FAILs: INFY +0.0070, RELIANCE +0.0090, TMPV -0.0001. SIGNAL RE-CONFIRMED "
        "OFF: empirical IC of mom_12_1 is -0.0933 against the house prior's sign=+1 "
        "- WRONG SIGN, same pattern as Egypt's now-retired rev_1m signal. LONO "
        "ablation shows ZERO difference between signal-ON and carry-only at this "
        "panel size (the dead-zone/cap machinery absorbs it either way) - not "
        "enough data to safely re-estimate the sign, so the mom_12_1/IC-0.07 prior "
        "is RETAINED unchanged for later re-estimation, signal_active stays False. "
        "The backtest carry schedule is still a flat 6.50% placeholder (RBI repo "
        "actually ranged 4.00->6.50->~5.50 over the window) - gate-neutral for "
        "skill scoring but MUST be sourced properly (live G-Sec / real RBI "
        "schedule) before any IN publish."),
    notes="Robust Indian momentum evidence in the literature - but ablated OFF on "
          "the first panel; re-estimate as the panel grows.")
QATAR = MarketProfile("QA", "Qatar (QE)",
    carry_schedule=[
        ("2020-01-01", 0.0100), ("2022-03-17", 0.0125), ("2022-05-05", 0.0175),
        ("2022-06-16", 0.0225), ("2022-07-28", 0.0300), ("2022-09-22", 0.0375),
        ("2022-11-03", 0.0450), ("2022-12-15", 0.0500), ("2023-02-02", 0.0525),
        ("2023-03-23", 0.0550), ("2023-05-04", 0.0575), ("2023-07-27", 0.0600),
        ("2024-09-19", 0.0550), ("2024-11-08", 0.0525), ("2024-12-19", 0.0500),
        ("2025-09-18", 0.0475), ("2025-10-30", 0.0450), ("2025-12-11", 0.0425),
        ("2026-06-18", 0.0400),
    ],
    rf_live=0.0425,
    rf_live_source=("QCB-tracking ESTIMATE: Qatar's peg means QCB moved with the Fed on "
                    "essentially the SAMA dates/levels; schedule cloned from the Saudi "
                    "SAMA-repo schedule as the backtest carry (gate-neutral by "
                    "construction). FLAG per no-UST-shortcut rule: source a real QAR "
                    "sovereign/T-bill yield before any Qatar publish."),
    signal_type="rev_1m", signal_sign=-1, ic=0.06, signal_active=False,
    nu=12.0, width_cal=0.972,
    fit_meta=("Fitted 10-Jul-2026 on the 3-name QA panel (QGTS/QNB/IQCD, 54 windows, "
              "2021-2026) - REPLACES the provisional QGTS-only self-fit (Gaussian/"
              "0.916). nu=12, cal=0.972: thin-tailed pegged market, cone near-"
              "unbiased. Panel verdict PARITY -0.010 CI[-0.017,+0.001] - on low-vol "
              "Qatari mega-caps the HAR cascade adds ~nothing over trailing vol. "
              "Per-name (LONO, robust-verdict blocks {2,3,4}): QGTS PARITY -0.012 "
              "(robust; its old FAIL confirmed as the borrowed-config artifact), "
              "QNB PARITY -0.005 (robust), IQCD FAIL -0.018 (ROBUST across all "
              "blocks - a genuine name-level FAIL under own-market config, the "
              "first; HAR width underperforms plain trailing vol on this name; "
              "banner decision = separately-initiated publish step)."),
    notes="Thin literature: carry-only until a ~5-name Qatar panel exists.")

METALS = MarketProfile("XAU", "Metals (Gold/Silver, USD)", FED_SCHEDULE, 0.0363,
    "USD cost-of-carry anchor: Fed funds midpoint schedule (q=0, no dividend). "
    "Documented assumption: the carry-anchored null for a zero-yield USD store of "
    "value is spot x exp(rf) — the futures-contango-consistent center; gate-neutral "
    "(same anchor both sides).",
    None, +1, 0.0, False,
    nu=20.0, width_cal=1.035,
    fit_meta=("PROVISIONAL single-instrument self-fit 10-Jul-2026 (GOLD, 67 windows "
              "2009-2026): nu=12, cal=1.014 - near-Gaussian, tails far thinner than "
              "EGX (nu=4); the old borrowed t5 was too fat for metals. Verdict "
              "PARITY +0.009 CI[-0.003,+0.028] (near-PASS). Silver shares this fit, "
              "flagged, until its own OHLC panel exists. "
              "UPDATE 22-Jul-2026 (PR #13, de-circularization): raw_ohlc/XAG/SILVER.csv "
              "sat unused under a profile code ('XAG') the unattended loop never reads; "
              "moved to raw_ohlc/XAU/ so it pools natively under this profile - the FIRST "
              "time XAU has been a real multi-name panel. Panel: 2 names, 86 windows, "
              "nu 12->20 / cal 1.014->1.035. MARKET VERDICT PARITY -> PASS +0.0099 "
              "CI[0.001,0.015]. Per-name via LONO (fit excluding that name's own "
              "contribution, score it OOS - each metal's FIRST non-circular verdict): "
              "GOLD PARITY +0.0011, SILVER PASS +0.0181. A cross-code 3-metal pool "
              "(with platinum: nu=20, cal=0.965, 148w, all PARITY/PASS) was analyzed and "
              "NOT adopted - hard-coding pooled numbers across profile codes fights the "
              "per-market refit loop (every future run would flag materiality drift "
              "against a number that isn't really this profile's own fit). Per the "
              "standing per-market fit rule, XAU fits its own panel; XPT stays a "
              "flagged single-name provisional until copper history or an approved "
              "fit-group mechanism exists."),
    notes="Carry-only. Shape/width fitted on the pooled GOLD+SILVER panel (2 names, "
          "de-circularized via LONO as of 22-Jul-2026) - the first non-circular metals "
          "fit in the system. Still the weakest panel by name-count in Testahil.")

PLATINUM = MarketProfile("XPT", "Platinum (USD)", FED_SCHEDULE, 0.0363,
    "USD cost-of-carry anchor: Fed funds midpoint schedule (q=0, no yield). Same "
    "documented assumption as METALS: the carry-anchored null for a zero-yield USD "
    "store of value is spot x exp(rf); gate-neutral (same anchor both sides).",
    None, +1, 0.0, False,
    nu=250.0, width_cal=0.853,
    fit_meta=("PROVISIONAL single-instrument self-fit 20-Jul-2026 (PLATINUM, 62 windows "
              "2012-2026, production chain, reproduction check vs live gold registry EXACT: "
              "67 windows, +0.0035, CI[-0.005,+0.013]): nu=Gaussian (MLE scale 0.790 -> "
              "width_cal 0.853, clip floor 0.85 active). Verdict PARITY -0.0004 "
              "CI[-0.009,+0.009] robust {2,3,4}. De-circularized cross-check (fit "
              "gold+silver, score platinum OOS): PARITY -0.0114 CI[-0.032,+0.009]. "
              "Borrowed live METALS (Gaussian/1.0): PARITY -0.0094. Pooled 3-metal fit "
              "(nu=20, cal=0.965, 148 windows) is the likely future config once metals "
              "pool - NOT adopted (per-market fit rule). Platinum does NOT arrive "
              "failing. Step-0.0 gate: 4041->4032 rows, 260.0 rows/yr = metals Mon-Fri "
              "calendar, zero corporate-action repairs."),
    notes="Carry-only. Single-name PROVISIONAL self-fit, flagged circular like gold's "
          "first fit; metals remain the weakest calibration in the system.")

PROFILES = {p.code: p for p in [EGYPT, SAUDI, USA, UK, BRAZIL, KOREA, UAE, INDIA, QATAR, METALS, PLATINUM]}
```

### 6.4 engine/data_quality.py (main @ bb6a899) — Step 0.0 gate AS CURRENTLY IN PRODUCTION (carries the two defects described in section 4.3; patch in 6.6)

```python
"""data_quality.py — OHLC cleaning gate for the Testahil learning loop (11-Jul-2026).

A continuous-learning system is only as good as what it ingests. This gate runs
BEFORE any series enters a calibration panel.

Two failure modes found on the first full EGX ingest:

1. PRE-LISTING PLACEHOLDERS. e-finance (EFIH) carried flat 0.50 rows with NaN
   volume for the days before its 19-Oct-2021 IPO, then opened at 13.98 — which
   the engine read as a +333% (log) one-day return.

2. UNADJUSTED CORPORATE ACTIONS. EFIH's 3:2 split on 26-May-2025 (19.77 -> open
   13.18, ratio exactly 1.500) and SODIC/OCDI's action on 14-Aug-2025 (61.00 ->
   open 17.50) appear as fake -34% and -73% one-day crashes.

DETECTION IS PRINCIPLED, NOT A MAGIC THRESHOLD: the EGX enforces a daily price
limit (circuit breaker) around +/-20%. Empirically every clean EGX name in our
25-name universe tops out at |log move| <= 0.223. A single-session move beyond
that is not reachable by trading — it can only be a corporate action or a data
error. The 0.35 threshold sits well clear of the limit AND well clear of the
largest plausible ex-dividend drop (a 29.5% single-payment yield), so genuine
ex-div gaps -- which the engine SHOULD see, since it forecasts price and its
carry anchor is rf - q -- are never touched.

Repair is a standard back-adjustment: scale all prior O/H/L/C by the observed
ratio so the artifact day's return becomes zero.
"""
import numpy as np
import pandas as pd

# Exchange daily price limits (circuit breakers). A single-session move beyond the
# limit is NOT reachable by trading — it can only be a corporate action or a data
# error. This is the principled basis for artifact detection, and it is PER-MARKET:
# a global threshold is wrong. KOSPI's limit is +/-30%, so a legitimate Korean
# limit-down day is log(0.70) = -0.357 — which an EGX-calibrated threshold of 0.35
# would have falsely "repaired". (Caught 11-Jul-2026 on the Korea ingest.)
DAILY_LIMIT = {
    'EG': 0.20,   # EGX
    'SA': 0.10,   # Tadawul
    'AE': 0.15,   # ADX / DFM
    'QA': 0.10,   # Qatar Exchange
    'KR': 0.30,   # KOSPI
    'IN': 0.20,   # NSE (banded 5/10/20)
    'US': None,   # no single-stock limit — real -40% earnings crashes happen
    'GB': None,
    'BR': None,
    'XAU': None,  # spot metal, no limit
    'XPT': None,  # spot metal, no limit
}
NO_LIMIT_THRESHOLD = 0.70   # markets without a limit: only a >50% one-day move is suspect
LIMIT_SAFETY = 1.30         # margin above the limit before we call it an artifact


def jump_threshold(market):
    lim = DAILY_LIMIT.get(market)
    if lim is None:
        return NO_LIMIT_THRESHOLD
    return abs(np.log(1 - lim)) * LIMIT_SAFETY


def clean_ohlc(df, ticker="", verbose=True, market=None):
    df = df.copy().reset_index(drop=True)
    log = []

    # --- 1. drop non-trading placeholder rows (no volume AND no intraday range) ---
    novol = df['Vol.'].isna() | (df['Vol.'].astype(str).str.strip().isin(['', 'nan', 'None', '-']))
    flat = (df['High'] == df['Low'])
    placeholder = novol & flat
    if placeholder.any():
        # only strip a LEADING placeholder block (pre-listing); interior halts are real
        first_real = int((~placeholder).idxmax())
        lead = placeholder.iloc[:first_real].sum()
        if lead:
            log.append(f"dropped {lead} leading pre-listing placeholder rows "
                       f"(flat price, no volume) before {df['Date'].iloc[first_real].date()}")
            df = df.iloc[first_real:].reset_index(drop=True)
        interior = placeholder.sum() - lead
        if interior:
            df = df[~(df['Vol.'].isna() & (df['High'] == df['Low']))].reset_index(drop=True)
            log.append(f"dropped {interior} interior stale/no-trade rows")

    # --- 2. detect + back-adjust unadjusted corporate actions ---
    thr = jump_threshold(market)
    for _ in range(6):  # iterate: repairing one can reveal another
        p = df['Price'].values
        lr = np.diff(np.log(p))
        hits = np.where(np.abs(lr) > thr)[0]
        if len(hits) == 0:
            break
        i = int(hits[0])                       # index of the day BEFORE the break
        factor = p[i + 1] / p[i]               # scale prior history onto the new basis
        d = df['Date'].iloc[i + 1].date()
        for c in ['Price', 'Open', 'High', 'Low']:
            df.loc[:i, c] = df.loc[:i, c] * factor
        log.append(f"back-adjusted {i+1} rows before {d} by x{factor:.4f} "
                   f"(raw 1-day log move {lr[i]:+.3f} exceeds the {market or '?'} "
                   f"artifact threshold {thr:.3f} — not reachable by trading)")

    if verbose and log:
        print(f"  [{ticker}] " + f"\n  [{ticker}] ".join(log))
    return df, log


def screen(df):
    """Post-clean sanity metrics."""
    lr = np.diff(np.log(df['Price'].values))
    return dict(rows=len(df), max_abs_log=float(np.abs(lr).max()),
                flat_frac=float((np.abs(lr) < 1e-9).mean()))
```

### 6.5 engine/adaptive_width.py (feat/adaptive-width-overlay-eg @ 1518c23 — NOT on main) — the adopted-but-unmerged, history-gated EG width overlay

```python
"""adaptive_width.py — Testahil per-stock ONLINE width overlay.

ADOPTED 23-Jul-2026, EG ONLY, GOING FORWARD. Holds a MECHANISM (and a small set of
fixed a-priori constants); it holds no per-market fit and never goes stale.

WHAT IT DOES
    A per-name multiplier on the market cone width, learned ONLINE from that name's OWN
    resolved 60-day residuals. It corrects the single thing the pooled (nu, width_cal)
    structurally cannot: a name whose OWN volatility sits below (or above) the panel
    average is given a market-level cone that is too WIDE (or too narrow) for it. The
    dominant failure this fixes is OVER-COVERAGE — the system's robust FAILs (LGES, Korea;
    ALPHADHABI, ADX) are OVER-covered (cov90 ~= 1.00) with well-CENTRED PITs (~0.47): not
    mis-centred, simply too wide, because their own vol is below the panel average.

OVERLAY, NOT A REFIT
    The pooled (nu, width_cal) are UNCHANGED and keep driving the Step-0 calibration gate.
    This layer multiplies width_cal for the LIVE forecast ONLY, per name. It NEVER touches
    drift (pure carry) and NEVER touches the tail nu. Turn the flag off and the engine is
    bit-for-bit the previous production engine.

SPEC (all constants fixed a-priori; only the shrink s was ever fitted — on an 11-name DEV
split — and it has been out-of-sample on every name added since):
    m_raw = clip( sqrt( EWMA_lambda( u^2 over the resolved past ) ), 0.7, 1.5 )
    mult  = 1 + s * sign(m_raw - 1) * max(0, |m_raw - 1| - dz)
  with lambda = 0.85 (EWMA on resolved windows, most-recent weighted 1), s = 0.5 (gentle),
  dz = 0.10 (dead zone: leave a name untouched when its implied mis-calibration is within
  +/-10% of correct). std_u = 1 is perfectly width-calibrated; <1 => cone too wide (tighten),
  >1 => too narrow (widen).
    u = (log(close[o+H]/close[o]) - carry) / (sqrt(HAR_var * H) * width_cal),  q = 0 in carry
        (drift is common to every s and cancels in the paired promotion delta; q=0 keeps the
         residual a pure WIDTH object).
  WALK-FORWARD SAFE: a 60d window opened at origin o' only enters the estimate once it has
  RESOLVED, i.e. o'+H <= today. Nothing uses an outcome it could not have known.

PROMOTION EVIDENCE (30-name EG panel; strict LONO / held-out FINAL; block bootstrap {2,3,4}Q):
    proper score : log-CRPS skill 0.0154 (baseline) -> 0.0152 (overlay) = PARITY, robust
                   across block sizes -> ZERO proper-score cost (this is NOT a CRPS gain).
    calibration  : pooled |std_u - 1| 0.096 -> 0.069 ; cov90 0.903 -> 0.893 (both in-band);
                   24 / 30 names moved CLOSER to std_u = 1.
    Replicated as the panel grew: 11/11, 13/16, 17/21, 24/30. The win is per-name width
    HONESTY at no cost to the proper score — that, and only that, is the claim.
  Same OOS gate that KILLED the CRPS-selection idea and the Amihud/dynamic-DoF arm. It passed.

HISTORY GATE (safety — read this before activating a new market)
    The overlay OVER-CORRECTS on short (~5yr) history and only behaves on long (~10-15yr)
    history. Below MIN_WINDOWS resolved 60d windows the multiplier is FORCED to 1.0 (exact
    baseline — always safe, since baseline is the currently adopted, validated engine).
    OPERATIONAL REALITY as of adoption: engine/raw_ohlc/EG currently carries mostly ~5-year
    histories (~17 resolved windows per name) — squarely in the over-correction regime — so
    with this gate the overlay is DORMANT (mult == 1.0) on the live library and merging it
    changes nothing. It begins to act, per name, ONLY once that name's LONG history is loaded
    into raw_ohlc/EG (bringing it to >= MIN_WINDOWS). MIN_WINDOWS is a CONSERVATIVE floor,
    not an OOS-tuned knob: it sits above the ~16-17-window 5yr failure regime and below the
    ~30-window ISPH long history; making it larger only keeps the overlay at baseline longer,
    which cannot hurt.

SCOPE / PROMOTION RULE
    EG ONLY. Every other market runs mult == 1.0 (flag off) until it clears the SAME 30-name-
    style LONO gate on its OWN panel. Activation is the per-profile flag width_overlay_active.

GOING-FORWARD ONLY
    Applies to cohorts anchored on/after adoption. Published / graded cohorts are NEVER
    retro-fitted (append-only ledger). Turning the overlay live for a market is a reviewed-PR
    / materiality step, because it moves some published 90% cones by >5%.
"""
import numpy as np

from mc_v2 import yz_variance_proxy
from mc_v3 import (fit_har_v3, har_forecast_v3, carry_log_h,
                   signal_alpha, simulate_paths_v3)

# ---- fixed a-priori constants (RULES, not a fit) ------------------------------------------
EWMA_LAM = 0.85            # EWMA decay on resolved windows (most-recent weight 1.0)
CLIP = (0.7, 1.5)          # clip on the raw sqrt-EWMA multiplier
SHRINK = 0.5               # gentle shrink s toward 1.0
DEAD_ZONE = 0.10           # leave a name untouched within +/-10% of correct
H = 60                     # forecast/residual horizon (trading days)
MIN_HIST = 260             # burn-in before the first residual window
MIN_WINDOWS = 28           # history gate: below this many resolved windows -> baseline (mult=1.0)


def gentle(m_raw: float) -> float:
    """Gentle + dead-zoned shrink of a raw multiplier toward 1.0 (the validated map)."""
    dev = float(m_raw) - 1.0
    sign = 1.0 if dev > 0 else (-1.0 if dev < 0 else 0.0)
    return 1.0 + SHRINK * sign * max(0.0, abs(dev) - DEAD_ZONE)


def resolved_u2(df, profile, horizon: int = H, min_hist: int = MIN_HIST):
    """Standardized-residual u^2 for every RESOLVED non-overlapping `horizon`-day window,
    using the profile's OWN base (nu, width_cal) config and pure-carry drift (q=0).
    Walk-forward safe by construction: the loop only reaches windows whose outcome exists."""
    v = yz_variance_proxy(df)
    close = df['Price'].values
    cal = float(getattr(profile, 'width_cal', 1.0) or 1.0)
    out = []
    o = min_hist
    n = len(df)
    while o + horizon < n:
        beta, s2 = fit_har_v3(v, o, horizon=horizon)
        dv = har_forecast_v3(v, o, beta, s2, horizon=horizon)
        sig = float(np.sqrt(dv * horizon) * cal)
        if sig > 0:
            drift = float(carry_log_h(profile, df['Date'].iloc[o], 0.0, horizon))
            u = (np.log(close[o + horizon] / close[o]) - drift) / sig
            out.append(u * u)
        o += horizon
    return out


def live_width_mult(df, profile, horizon: int = H, min_hist: int = MIN_HIST,
                    return_detail: bool = False):
    """The per-name LIVE width multiplier at today's origin.

    Returns 1.0 (exact baseline) when the overlay is inactive for this market OR the name has
    fewer than MIN_WINDOWS resolved windows (short history -> over-correction risk). Otherwise
    returns the validated gentle+dead-zoned online multiplier.
    """
    active = bool(getattr(profile, 'width_overlay_active', False))
    if not active:
        return (1.0, dict(active=False, reason='flag_off', n_windows=0, m_raw=1.0)) if return_detail else 1.0
    u2 = resolved_u2(df, profile, horizon, min_hist)
    if len(u2) < MIN_WINDOWS:
        d = dict(active=True, reason='insufficient_history', n_windows=len(u2), m_raw=1.0)
        return (1.0, d) if return_detail else 1.0
    w = np.array([EWMA_LAM ** k for k in range(len(u2))][::-1])
    m_raw = float(np.clip(np.sqrt(np.sum(w * np.array(u2)) / np.sum(w)), *CLIP))
    mult = float(gentle(m_raw))
    if return_detail:
        return mult, dict(active=True, reason='applied', n_windows=len(u2), m_raw=m_raw)
    return mult


def live_paths(df, profile, spot, date, q_annual, horizon: int = H,
               n_paths: int = 50000, seed: int = 42):
    """Canonical LIVE forecast path set for a covered name, WITH the per-market width overlay
    applied per profile.width_overlay_active. The base engine (mc_v3) is untouched — this only
    scales width_cal by the per-name multiplier and then calls simulate_paths_v3 exactly as the
    standing roll-forward chain does (drift = carry + signal-if-active; nu from the profile;
    seed 42). Returns (paths[n_paths, horizon+1], meta)."""
    v = yz_variance_proxy(df)
    close = df['Price'].values
    o = len(df) - 1
    beta, s2 = fit_har_v3(v, o, horizon=horizon)
    dv = har_forecast_v3(v, o, beta, s2, horizon=horizon)
    mult = live_width_mult(df, profile, horizon)
    cal_eff = float(getattr(profile, 'width_cal', 1.0) or 1.0) * mult
    sigma_h = float(np.sqrt(dv * horizon) * cal_eff)
    carry = float(carry_log_h(profile, date, q_annual, horizon))
    alpha, _ = signal_alpha(profile, close, o, sigma_h)   # 0.0 when signal inactive (all markets today)
    drift = carry + alpha
    nu = float(profile.nu) if getattr(profile, 'nu', None) else 8.0
    paths = simulate_paths_v3(spot, dv, horizon, drift, nu=nu,
                              n_paths=n_paths, seed=seed, width_cal=cal_eff)
    meta = dict(mult=mult, width_cal_base=float(getattr(profile, 'width_cal', 1.0) or 1.0),
                width_cal_eff=cal_eff, sigma_h=sigma_h, drift=drift, nu=nu)
    return paths, meta


if __name__ == "__main__":
    # Data-free self-check of the validated map and the safety fallbacks (VERIFY BY IMPORT).
    assert abs(gentle(1.00) - 1.00) < 1e-12          # centred -> untouched
    assert abs(gentle(1.05) - 1.00) < 1e-12          # inside dead zone -> untouched
    assert abs(gentle(1.40) - 1.15) < 1e-12          # 1 + 0.5*(0.40-0.10)
    assert abs(gentle(0.70) - 0.90) < 1e-12          # 1 - 0.5*(0.30-0.10)

    class _P:  # flag OFF -> exact baseline regardless of data
        width_overlay_active = False
        width_cal = 0.972
        nu = 4.0
    assert live_width_mult(None, _P()) == 1.0
    print("adaptive_width self-check OK — gentle map + inactive fallback verified; "
          f"MIN_WINDOWS={MIN_WINDOWS}, lambda={EWMA_LAM}, s={SHRINK}, dz={DEAD_ZONE}")
```

### 6.6 dq_patch.py (PROPOSED 26-Jul-2026, not pushed; archived at project doc claude/v4_lab/dq_patch_proposed_20260726.py) — fix for the two data-gate defects

```python
"""dq_patch.py — proposed fix for TWO defects in engine/data_quality.py that only
become reachable once EGX history extends back before ~2021.

DEFECT 1 — NON-POSITIVE PRICE ROWS.
The vendor writes Price = 0.00 on some sessions while Open/High/Low are valid
(a missing-close artifact). clean_ohlc does np.log(0) = -inf, reads it as an
infinite one-day move, and computes factor = p[i+1]/p[i] = inf (or 0.0). It then
multiplies EVERY prior row by 0 or inf. Measured on this upload: 17 such rows
across 5 of 16 names — and on OCDI it rescales 536 rows of history to zero.
These rows survive the existing placeholder filter because they carry real
volume and a real High != Low range.
FIX: drop non-positive / non-finite Price rows BEFORE the jump scan. Dropping,
not imputing — no invented closes enter a calibration panel.

DEFECT 2 — SPIKE-AND-REVERT BAD PRINTS TREATED AS CORPORATE ACTIONS.
A one-session bad print (BTFH 4.638 -> 16.390 -> 5.006; HELI 0.330 -> 12.080 ->
0.340) is not a corporate action. A corporate action is ONE-WAY and permanent.
The current iterative back-adjust handles each leg separately and applies two
rescalings that do NOT cancel:
    BTFH  x3.5339 then x0.3054 -> net 1.0793  (+7.9% on 952 prior rows)
    BTFH  x3.0933 then x0.2971 -> net 0.9190  (-8.1% on 989 prior rows)
    HELI  x36.606 then x0.0281 -> net 1.0286  (+2.9% on 228 prior rows)
so prior history is left permanently mis-scaled AND the bad print itself stays.
FIX: before treating a breach as a corporate action, check whether the NEXT
session reverses it. If breach i and breach i+1 are opposite-signed and their
sum returns within the artifact threshold of the pre-spike level, it is a
single-session bad print -> drop that ONE row, rescale nothing.

Both fixes are conservative: they only ever REMOVE rows the exchange could not
have traded, and they strictly reduce the number of back-adjustments applied.
"""
import numpy as np
import pandas as pd
import sys
sys.path.insert(0, '/tmp/mcrev/testahil/engine')
from data_quality import jump_threshold


def clean_ohlc_v2(df, ticker="", verbose=False, market=None):
    df = df.copy().reset_index(drop=True)
    log = []

    # --- 0. leading pre-listing placeholders (unchanged behaviour) -----------
    novol = df['Vol.'].isna() | (df['Vol.'].astype(str).str.strip()
                                 .isin(['', 'nan', 'None', '-']))
    flat = (df['High'] == df['Low'])
    placeholder = novol & flat
    if placeholder.any():
        first_real = int((~placeholder).idxmax())
        lead = int(placeholder.iloc[:first_real].sum())
        if lead:
            log.append(f"dropped {lead} leading pre-listing placeholder rows")
            df = df.iloc[first_real:].reset_index(drop=True)
        interior = int(placeholder.sum() - lead)
        if interior:
            df = df[~(df['Vol.'].isna() & (df['High'] == df['Low']))].reset_index(drop=True)
            log.append(f"dropped {interior} interior stale/no-trade rows")

    # --- FIX 1: non-positive / non-finite closes ----------------------------
    bad = ~np.isfinite(df['Price'].values) | (df['Price'].values <= 0)
    if bad.any():
        d0 = df.loc[bad, 'Date']
        log.append(f"FIX1 dropped {int(bad.sum())} rows with a non-positive/missing close "
                   f"({d0.iloc[0].date()}..{d0.iloc[-1].date()}) — vendor missing-close "
                   f"artifact, would have produced log(0) = -inf")
        df = df[~bad].reset_index(drop=True)

    # --- FIX 2 + corporate actions ------------------------------------------
    thr = jump_threshold(market)
    for _ in range(12):
        p = df['Price'].values
        lr = np.diff(np.log(p))
        hits = np.where(np.abs(lr) > thr)[0]
        if len(hits) == 0:
            break
        i = int(hits[0])
        # spike-and-revert? a breach at i that REVERSES within MAXBLOCK sessions
        # is a bad-print block, not a corporate action (which is one-way and
        # permanent). BTFH 2016-05 is a 3-session block, so adjacent-only is not
        # enough — scan forward.
        MAXBLOCK = 5
        rev = None
        for k in range(1, min(MAXBLOCK, len(lr) - i)):
            cum = lr[i:i + k + 1].sum()
            if abs(lr[i + k]) > thr and np.sign(lr[i + k]) != np.sign(lr[i]) \
                    and abs(cum) <= thr:
                rev = k
                break
        if rev is not None:
            d0 = df['Date'].iloc[i + 1].date(); d1 = df['Date'].iloc[i + rev].date()
            log.append(f"FIX2 dropped {rev} bad-print row(s) {d0}..{d1} "
                       f"({p[i]:.3f} -> {p[i+1]:.3f} ... -> {p[i+rev+1]:.3f}; "
                       f"net log over the block {lr[i:i+rev+1].sum():+.3f}) — reverts "
                       f"within {rev} session(s), so NOT a corporate action; "
                       f"rescaled nothing")
            df = df.drop(index=range(i + 1, i + rev + 1)).reset_index(drop=True)
            continue
        # genuine one-way corporate action -> back-adjust (unchanged behaviour)
        factor = p[i + 1] / p[i]
        if not np.isfinite(factor) or factor <= 0:
            log.append(f"FIX1 guard: refused a non-finite back-adjust factor at "
                       f"{df['Date'].iloc[i+1].date()}")
            break
        d = df['Date'].iloc[i + 1].date()
        for c in ['Price', 'Open', 'High', 'Low']:
            df.loc[:i, c] = df.loc[:i, c] * factor
        log.append(f"back-adjusted {i+1} rows before {d} by x{factor:.4f} "
                   f"(raw 1-day log move {lr[i]:+.3f} exceeds the {market} "
                   f"artifact threshold {thr:.3f})")

    if verbose and log:
        print(f"  [{ticker}] " + f"\n  [{ticker}] ".join(log))
    return df, log
```

---

## 7. Reproduction guide

```bash
git clone https://github.com/sherifomarsaleh/testahil.git && cd testahil
git checkout bb6a89914b1b27013a3add404b6dadf2323668d1        # this pack's main snapshot
python3 -c "import sys; sys.path.insert(0,'engine'); import market_profiles, mc_v3, data_quality; print('import OK')"
```
Verification is **by import, not by parse** — house rule after a bare-identifier bug (`nu=Gaussian`) once parsed cleanly and left the engine unloadable.

**Canonical live-forecast chain** (what a published cohort runs, exactly):
`data_quality.clean_ohlc(market=…)` → `mc_v2.yz_variance_proxy` → `mc_v3.fit_har_v3(v, origin, horizon=60)` → `mc_v3.har_forecast_v3` → `mc_v3.carry_log_h(profile, date, q_annual, 60)` (profile `rf_live`) → `mc_v3.simulate_paths_v3(spot, dv, 60, drift, nu=profile.nu, width_cal=profile.width_cal, n_paths=50000, seed=42)`. Signal alpha is a structural no-op today (`signal_active=False` in every profile). Once the overlay branch merges *and* a name clears MIN_WINDOWS, EG's `width_cal` is first passed through `adaptive_width.live_width_mult()` — a no-op for every EG name at this snapshot.

**Canonical gate run:** `mc_v3.backtest_v3(df, profile, horizon=60, q_annual=0)` per name → `pooled_scores(frames)` → `block_bootstrap_ci` → `verdict`. Name-level FAILs must hold across block sizes {2,3,4}.

`adaptive_width.py` self-check: `python3 engine/adaptive_width.py` on the feature branch (asserts the gentle-map fixed points and the flag-off ⇒ 1.0 fallback).

## 8. Where the primary evidence lives (project docs, by claim)

| Claim in this pack | Primary doc |
|---|---|
| Overlay adoption evidence (LONO, 30-name) | `claude/v4_lab/Adaptive_Width_Verdict_11stock_20260723.md`, `Adaptive_Width_LongHistory_20260723.md` |
| Session synthesis, frontier diagnosis | `claude/v4_lab/MC_Improvement_Session_Synthesis_20260723.md` |
| CHAR-MC audit → rejection | `claude/external_reviews/CHAR_MC_*` (5 docs, 26-Jul) |
| Gemini-MC audit → rejection; 3 production defects | `claude/v4_lab/Gemini_MC_Part{1,2,3}*_2026072{3,6}.md` |
| Cross-review synthesis, multi-horizon adoption | `claude/external_reviews/CHAR_and_Gemini_MC_Synthesis_WhatToKeep_20260726.md` |
| EG 15-yr library ingest + break-cut PARITY retest | `claude/data/EG_15yr_Library_Ingest_and_Calibration_Finding_20260726.md` |
| 74-name master evaluation workbook + stale-mirror finding | `claude/engine_docs/Master_Evaluations_Workbook_Build_20260726.md` |
| Rejected arms (each with walk-forward evidence) | `claude/v4_lab/*REJECTED*.md`, `Round8_FVPull_RETIRED_20260723.md`, `claude/shrinkage/*` |

## 9. Reviewer's checklist — where scrutiny is most valuable

1. **The overlay's promotion logic** (§3/§6.5): is parity-on-proper-score + improved |std_u−1| a sufficient adoption bar, given four rejected width-adaptation arms? Is MIN_WINDOWS=28 defensible as a conservative floor rather than a tuned knob?
2. **The 2022-03-21 break cut** (§4.4): PARITY on the full 30-name retest means it survives, but the full-sample PASS→PARITY degradation is unresolved. Is the serial-devaluation regime argument sound, or is the post-break PASS favourable-sample?
3. **Log-space CRPS migration** (§4.3): the non-convergence finding is mathematically clean; the open question is whether re-scoring changes any standing verdict on the short panels.
4. **The dq patch** (§6.6): conservative by construction (only removes untradeable rows), but the 5-session revert-scan window and the interaction with genuine multi-leg corporate actions deserve independent eyes.
5. **ν weak identification** (§1): any review that quotes ν without width_cal (or vice versa) is reviewing the wrong object — the cone multiple `width_cal × q95(t(ν))` is the honest coordinate.
6. **Metals**: circular/thin by admission; treat as out of scope for calibration claims.

---
*Pack prepared 26-Jul-2026 from live repo state. Nothing in this pack was pushed to the repository; the dq patch and the log-CRPS change remain proposals pending PR review. All fitted numbers go stale on the next library post — re-read `engine/market_profiles.py` live before quoting.*
