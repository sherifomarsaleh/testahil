"""BOROUGE beta — tier-1 own-stock weekly regression against the FTSE ADX General Index.

CHANGED 09-Aug-2026. The regressor is now the ADX general index (engine/raw_indices/AE/
FADGI.csv), which is what the beta rule actually asks for: a stock's beta comes from its
OWN price history regressed against its OWN local index, exactly as EGX30 is the regressor
for an EGX name. The previous revision used an equal-weight composite of the other AE names
in the price library, which was a stand-in adopted only because no ADX index series existed
in any repository. The composite is retained below as a CORROBORATION, not as the estimate.

Why the change is not cosmetic. An equal-weight composite of seventeen names is not the
market: it over-weights small, thinly traded constituents, which drags its own volatility
up and its covariance with any single name down. A capitalisation-weighted general index is
the object the cost-of-capital formula assumes. Swapping one for the other moves the beta,
and the study reports the move rather than quietly restating.

Five things are produced rather than asserted:
  * the diagnostic triple (n, R-squared, SE) and the resulting 90% confidence interval;
  * a Dimson (1979) lead-lag sum-beta, the standard correction for non-synchronous trading;
  * the equal-weight composite beta, as an independent corroboration of the index beta;
  * the index-membership disclosure — the subject IS a constituent of its own regressor,
    and its approximate weight is stated rather than waved away;
  * a window sensitivity (2, 3, 4 and 5 years), because the rule permits any window from
    two to five years and the choice should be visible.

The ADOPTED beta is decided by the gate, in code, not chosen in prose.
"""
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import numpy as np                                          # noqa: E402
import pandas as pd                                         # noqa: E402
from data_quality import clean_ohlc, screen                 # noqa: E402
from primitives import load_ohlc                            # noqa: E402
from wacc_builder import RegressionBetaAttempt              # noqa: E402

TKR = 'BOROUGE'
INDEX_FILE = os.path.join(HERE, '..', 'raw_indices', 'AE', 'FADGI.csv')
INDEX_NAME = 'FTSE ADX General Index'


def weekly(px):
    return px.resample('W-THU').last().dropna()


def ols(X, y):
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    yhat = X @ b
    ss_res = float(((y - yhat) ** 2).sum())
    ss_tot = float(((y - y.mean()) ** 2).sum())
    n, k = X.shape
    r2 = 1 - ss_res / ss_tot
    XtX_inv = np.linalg.inv(X.T @ X)
    sigma2 = ss_res / (n - k)
    se = np.sqrt(np.diag(XtX_inv) * sigma2)
    return b, r2, se, ss_res


def logret(w):
    return np.log(w / w.shift(1)).dropna()


# ---- the subject ------------------------------------------------------------
raw, _ = clean_ohlc(load_ohlc(os.path.join(HERE, f'{TKR}_Stock_Price_History.csv')),
                    TKR, verbose=False, market='AE')
flat_self = float(screen(raw)['flat_frac'])
sub = raw.set_index('Date')['Price']

# ---- the market: the ADX general index, through the same cleaning gate -------
idx_raw = load_ohlc(INDEX_FILE)
idx_clean, idx_rep = clean_ohlc(idx_raw, 'FADGI', verbose=False, market='AE')
idx = idx_clean.set_index('Date')['Price']
idx_screen = screen(idx_clean)

# ---- the corroborating equal-weight composite, subject excluded --------------
comp, flats = {}, []
for f in sorted(glob.glob(os.path.join(HERE, '..', 'raw_ohlc', 'AE', '*.csv'))):
    t = os.path.basename(f)[:-4]
    try:
        df, _ = clean_ohlc(load_ohlc(f), t, verbose=False, market='AE')
    except Exception as e:                                   # pragma: no cover
        print('skip', t, e)
        continue
    flats.append(float(screen(df)['flat_frac']))
    if t != TKR:
        comp[t] = df.set_index('Date')['Price']
flat_median = float(np.median(flats))


def regress(years):
    """Weekly OLS of the subject on the index over the trailing `years` window."""
    cut = sub.index.max() - pd.DateOffset(years=years)
    re_ = logret(weekly(sub[sub.index >= cut]))
    rm = logret(weekly(idx[idx.index >= cut]))
    al = pd.concat([re_.rename('sub'), rm.rename('mkt')], axis=1, sort=True).dropna()
    x, y = al['mkt'].values, al['sub'].values
    n = len(x)
    b, r2, se, _ = ols(np.column_stack([np.ones(n), x]), y)
    return dict(years=years, beta=float(b[1]), r2=float(r2), n=int(n),
                se=float(se[1]), alpha=float(b[0])), al


WINDOWS = {y: regress(y)[0] for y in (2, 3, 4, 5)}
main, al = regress(5)
beta, se_beta, r2, n = main['beta'], main['se'], main['r2'], main['n']
att = RegressionBetaAttempt(beta=beta, r_squared=r2, n_obs=n, se_beta=se_beta,
                            frequency='weekly')
ok, msg = att.is_usable()
ci = (beta - 1.645 * se_beta, beta + 1.645 * se_beta)

# ---- Dimson sum-beta (1 lead, contemporaneous, 2 lags) ----------------------
Dm = al.copy()
Dm['lead'] = Dm['mkt'].shift(-1)
Dm['lag1'] = Dm['mkt'].shift(1)
Dm['lag2'] = Dm['mkt'].shift(2)
Dm = Dm.dropna()
Xd = np.column_stack([np.ones(len(Dm)), Dm['lead'], Dm['mkt'], Dm['lag1'], Dm['lag2']])
bd, r2d, sed, _ = ols(Xd, Dm['sub'].values)
sum_beta = float(bd[1:].sum())
resid = Dm['sub'].values - Xd @ bd
sigma2 = float((resid ** 2).sum() / (len(Dm) - Xd.shape[1]))
cov_b = np.linalg.inv(Xd.T @ Xd) * sigma2
se_sum = float(np.sqrt(cov_b[1:, 1:].sum()))
dim_ci = (sum_beta - 1.645 * se_sum, sum_beta + 1.645 * se_sum)

# ---- corroboration: the equal-weight composite the previous revision used ----
cut5 = sub.index.max() - pd.DateOffset(years=5)
rets = {}
for t, s in comp.items():
    r = logret(weekly(s[s.index >= cut5]))
    if len(r) >= 100:
        rets[t] = r
Rc = pd.DataFrame(rets)
mkt_c = Rc.mean(axis=1, skipna=True)
re5 = logret(weekly(sub[sub.index >= cut5]))
al_c = pd.concat([re5.rename('sub'), mkt_c.rename('mkt')], axis=1, sort=True).dropna()
bc, r2c, sec, _ = ols(np.column_stack([np.ones(len(al_c)), al_c['mkt'].values]),
                      al_c['sub'].values)
beta_comp, se_comp = float(bc[1]), float(sec[1])

# ---- index membership: the subject is a constituent of its own regressor -----
# Borouge's weight in the index is its free-float market capitalisation over the index's.
# The exact divisor is not published, so the weight is bounded rather than asserted: full
# market capitalisation over total ADX capitalisation is an UPPER bound on it, because the
# index is free-float weighted and Borouge's float is roughly a tenth of its shares.
MKTCAP_AED = 30_057_691_583 * 2.40 / 1e9            # AED billion, at the 7-Aug close
ADX_TOTAL_AED = 3_100.0                              # AED billion, ADX market statistics
weight_upper = MKTCAP_AED / ADX_TOTAL_AED
FLOAT_SHARE = 0.10                                   # ~10% free float since the 2022 listing
weight_est = weight_upper * FLOAT_SHARE / (1 - 0.0)   # free-float weighted

# ---- the gate decides -------------------------------------------------------
weak = bool(r2 < 0.10 or (ci[1] - ci[0]) > 2 * abs(beta))
if ok:
    beta_used = beta
    basis = ('tier-1 own-stock weekly regression against its own local index '
             '(usability gate PASSED)')
    why = (f"n = {n} weekly observations against the ADX general index, R-squared = "
           f"{r2:.3f} against the 0.05 floor, SE(beta) = {se_beta:.3f} against |beta| = "
           f"{abs(beta):.3f}. All three conditions of the usability gate are met, so the "
           f"regression estimate is adopted rather than a default.")
else:
    beta_used = 1.0
    basis = 'tier-3 default on a GENUINE usability-gate failure, disclosed with diagnostics'
    why = (f"The tier-1 regression FAILS the usability gate: {msg}. A silent default is "
           f"forbidden; a default shown with the diagnostics that triggered it is "
           f"permitted, and this is that case.")

out = dict(
    ticker=TKR,
    regressor=INDEX_NAME,
    regressor_file='engine/raw_indices/AE/FADGI.csv',
    regressor_span=[str(idx.index.min().date()), str(idx.index.max().date())],
    regressor_rows=int(len(idx_clean)),
    regressor_repairs=idx_rep if isinstance(idx_rep, list) else list(idx_rep or []),
    regressor_flat_frac=round(float(idx_screen['flat_frac']), 4),
    regressor_max_abs_log=round(float(idx_screen['max_abs_log']), 4),
    beta=beta, r2=float(r2), n=int(n), se=se_beta,
    ci90=[float(ci[0]), float(ci[1])],
    usable=bool(ok), gate_msg=msg,
    window_years=5, frequency='weekly',
    weak=weak,
    weak_reason=(f"R-squared = {r2 * 100:.1f}% against the 10% weak-instrument threshold; "
                 f"the 90% confidence interval [{ci[0]:.2f}, {ci[1]:.2f}] spans "
                 f"{(ci[1] - ci[0]) / abs(beta):.2f}x the point estimate"),
    warnings=att.interim_warnings(),
    window_sensitivity=WINDOWS,
    adopted=dict(
        beta_used=float(beta_used), basis=basis, why=why,
        corroboration=(
            f"Cross-checked three ways. (i) The Dimson sum-beta is {sum_beta:.3f} with a "
            f"90% interval of [{dim_ci[0]:.2f}, {dim_ci[1]:.2f}]; the adopted "
            f"{beta_used:.2f} "
            f"{'sits inside' if dim_ci[0] <= beta_used <= dim_ci[1] else 'sits outside'} "
            f"it. (ii) The same regression against an equal-weight composite of the other "
            f"{len(rets)} names in the AE library gives {beta_comp:.3f} (R-squared "
            f"{r2c:.3f}) — a different construction of 'the market' reaching a "
            f"{'similar' if abs(beta_comp - beta) < 0.25 else 'materially different'} "
            f"answer. (iii) The simple prior for a cyclical, capital-intensive materials "
            f"business is 1.0-1.5 and for a defensive or staple business 0.6-0.9; the "
            f"adopted figure is read against both in the study rather than accepted at "
            f"face value."),
        sensitivity_required=[0.6, 0.8, 1.0, 1.15, 1.3]),
    dimson=dict(
        sum_beta=sum_beta, se_sum=se_sum, r2=float(r2d), n=int(len(Dm)),
        ci90=[float(dim_ci[0]), float(dim_ci[1])],
        coefficients=dict(lead=float(bd[1]), contemporaneous=float(bd[2]),
                          lag1=float(bd[3]), lag2=float(bd[4])),
        uplift_vs_ols=float(sum_beta - beta),
        note=("Dimson (1979) sum-beta over one lead, the contemporaneous term and two "
              "lags. The uplift over the contemporaneous OLS beta measures how much "
              "co-movement is booked late because the stock does not trade on every "
              "session.")),
    composite_corroboration=dict(
        beta=beta_comp, r2=float(r2c), se=se_comp, n=int(len(al_c)),
        names=len(rets),
        note=("An equal-weight composite of the other AE names in the price library, the "
              "regressor the previous revision of this study used. It is retained as a "
              "corroboration only. An equal-weight composite over-weights small, thinly "
              "traded constituents, which is why the capitalisation-weighted general "
              "index is the correct regressor and this is the cross-check.")),
    index_membership=dict(
        subject_is_constituent=True,
        market_cap_aed_bn=round(MKTCAP_AED, 1),
        adx_total_aed_bn=ADX_TOTAL_AED,
        weight_upper_bound=round(weight_upper, 4),
        weight_estimate_free_float=round(weight_est, 4),
        note=("The subject IS a constituent of its own regressor, which injects a "
              "self-covariance term into the numerator exactly as it did with the "
              "composite. The difference is magnitude: in a seventeen-name equal-weight "
              "composite the subject carried about a seventeenth of the index; in a "
              "free-float capitalisation-weighted general index with roughly a 10% float "
              "it carries well under one per cent. The contamination is therefore an "
              "order of magnitude smaller and is bounded above rather than assumed "
              "away.")),
    thin_trading=dict(
        flat_frac=round(flat_self, 4), ae_panel_median=round(flat_median, 4),
        ratio=round(flat_self / flat_median, 2),
        index_flat_frac=round(float(idx_screen['flat_frac']), 4),
        note=("Share of sessions closing unchanged, against the median of the AE library "
              "and against the index itself. A high ratio is the documented mechanism for "
              "a downward-biased contemporaneous beta, and it is why the Dimson "
              "correction is run.")),
    plausibility=dict(
        sector_prior="cyclical / capital-intensive materials: 1.0-1.5",
        defensive_prior="defensive or staple: 0.6-0.9",
        net_cash_note=("The company carries roughly 0.8x net debt to EBITDA and its "
                       "earnings are levered to a global commodity price benchmark, both "
                       "of which argue for an estimate at or above the cyclical band "
                       "rather than below it.")),
)
json.dump(out, open(os.path.join(HERE, 'beta_result.json'), 'w'), indent=1)

print(f"regressor: {INDEX_NAME}, {len(idx_clean):,} sessions "
      f"{idx.index.min().date()} -> {idx.index.max().date()}, "
      f"flat {idx_screen['flat_frac']:.4f}, max |log move| {idx_screen['max_abs_log']:.4f}")
print(f"OLS beta   {beta:.3f} | R2 {r2:.3f} | n {n} | SE {se_beta:.3f} "
      f"| CI90 [{ci[0]:.2f},{ci[1]:.2f}] | usable={ok} | weak={weak}")
print(f"  gate: {msg}")
print("  window sensitivity: " + "  ".join(
    f"{y}yr {WINDOWS[y]['beta']:.3f} (R2 {WINDOWS[y]['r2']:.3f}, n {WINDOWS[y]['n']})"
    for y in (2, 3, 4, 5)))
print(f"Dimson sum {sum_beta:.3f} | SE {se_sum:.3f} | R2 {r2d:.3f} | n {len(Dm)} "
      f"| CI90 [{dim_ci[0]:.2f},{dim_ci[1]:.2f}] | uplift {sum_beta - beta:+.3f}")
print(f"  coefficients: lead {bd[1]:+.3f}  contemp {bd[2]:+.3f}  "
      f"lag1 {bd[3]:+.3f}  lag2 {bd[4]:+.3f}")
print(f"corroboration: equal-weight composite of {len(rets)} names gives "
      f"{beta_comp:.3f} (R2 {r2c:.3f}, SE {se_comp:.3f})")
print(f"  index membership: subject weight <= {weight_upper:.2%} of the index "
      f"(free-float estimate {weight_est:.2%})")
print(f"  thin trading: flat_frac {flat_self:.3f} vs AE median {flat_median:.3f} "
      f"({flat_self / flat_median:.2f}x); index {idx_screen['flat_frac']:.3f}")
print(f"  ADOPTED beta = {beta_used:.3f} — {basis}")
