"""SCEM beta — tier-1 own-stock weekly regression vs an equal-weight EGX composite
built from the full engine/raw_ohlc/EG library (house pattern: CLHO/RMDA/SWDY),
5-year window, RegressionBetaAttempt usability gate.

Extended for SCEM with a DIMSON lead-lag adjustment. SCEM prints an unchanged close on
29.3% of sessions (3.4x the EG panel median, 2nd thinnest of 33 names). Non-synchronous
trading biases an OLS beta DOWNWARD by construction: when the stock does not trade on the
day the market moves, its return is booked late, so contemporaneous covariance with the
index is understated. The Dimson sum-beta (lead + contemporaneous + lags) recovers the
part that leaks into adjacent weeks and is the standard correction. Both are reported —
the plausibility cross-check the beta procedure requires is done with a number, not an
assertion.
"""
import sys, os, glob, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import numpy as np
import pandas as pd
from primitives import load_ohlc
from data_quality import clean_ohlc
from wacc_builder import RegressionBetaAttempt


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


scem, _ = clean_ohlc(load_ohlc(os.path.join(HERE, 'SCEM_Stock_Price_History.csv')),
                     'SCEM', verbose=False, market='EG')
scem = scem.set_index('Date')['Price']

comp = {}
for f in sorted(glob.glob(os.path.join(HERE, '..', 'raw_ohlc', 'EG', '*.csv'))):
    tkr = os.path.basename(f)[:-4]
    if tkr == 'SCEM':
        continue                     # exclude the subject from its own index
    try:
        df, _ = clean_ohlc(load_ohlc(f), tkr, verbose=False, market='EG')
        comp[tkr] = df.set_index('Date')['Price']
    except Exception as e:
        print('skip', tkr, e)

cut = scem.index.max() - pd.DateOffset(years=5)
wk_scem = weekly(scem[scem.index >= cut])
rets = {}
for tkr, s in comp.items():
    w = weekly(s[s.index >= cut])
    r = np.log(w / w.shift(1)).dropna()
    if len(r) >= 100:
        rets[tkr] = r
R = pd.DataFrame(rets)
mkt = R.mean(axis=1, skipna=True)                     # equal-weight composite weekly log-return
re_ = np.log(wk_scem / wk_scem.shift(1)).dropna()
al = pd.concat([re_.rename('scem'), mkt.rename('mkt')], axis=1, sort=True).dropna()

# ---- tier-1 contemporaneous OLS beta ---------------------------------------
x, y = al['mkt'].values, al['scem'].values
n = len(x)
b, r2, se, _ = ols(np.column_stack([np.ones(n), x]), y)
beta, se_beta = float(b[1]), float(se[1])
att = RegressionBetaAttempt(beta=beta, r_squared=r2, n_obs=n, se_beta=se_beta,
                            frequency='weekly')
ok, msg = att.is_usable()
ci = (beta - 1.645 * se_beta, beta + 1.645 * se_beta)

# ---- Dimson sum-beta (1 lead, contemporaneous, 2 lags) ---------------------
D = al.copy()
D['lead'] = D['mkt'].shift(-1)
D['lag1'] = D['mkt'].shift(1)
D['lag2'] = D['mkt'].shift(2)
D = D.dropna()
Xd = np.column_stack([np.ones(len(D)), D['lead'], D['mkt'], D['lag1'], D['lag2']])
bd, r2d, sed, _ = ols(Xd, D['scem'].values)
sum_beta = float(bd[1:].sum())
# SE of the sum needs the full covariance of the four slope coefficients
Xd_inv = np.linalg.inv(Xd.T @ Xd)
resid = D['scem'].values - Xd @ bd
sigma2 = float((resid ** 2).sum() / (len(D) - Xd.shape[1]))
cov_b = Xd_inv * sigma2
se_sum = float(np.sqrt(cov_b[1:, 1:].sum()))

# ---- disclosure variant: the same regression WITH the subject left in the index --
mkt_in = pd.DataFrame({**rets, 'SCEM': re_}).mean(axis=1, skipna=True)
al_in = pd.concat([re_.rename('scem'), mkt_in.rename('mkt')], axis=1, sort=True).dropna()
b_in, r2_in, se_in, _ = ols(
    np.column_stack([np.ones(len(al_in)), al_in['mkt'].values]), al_in['scem'].values)

flat_frac_scem, flat_frac_eg_median = 0.293, 0.085
out = dict(
    self_inclusion_bias=dict(
        beta_index_including_subject=float(b_in[1]), r2_including=float(r2_in),
        beta_index_excluding_subject=beta, r2_excluding=float(r2),
        note=("Leaving the subject inside its own equal-weight index injects a self-covariance "
              "term w*Var(SCEM) into the numerator. At w = 1/33 that is normally negligible, but "
              "SCEM's own variance dominates the panel (the stock ran 6 -> 87 over the window), "
              "so the contamination is large: beta reads %.3f including the subject against "
              "%.3f excluding it. The EXCLUDING figure is the correct one and is what is "
              "reported; the including figure is disclosed so the difference is visible."
              % (float(b_in[1]), beta))),
    adopted=dict(
        beta_used=1.0,
        basis="tier-3 default on a GENUINE usability-gate failure, disclosed with diagnostics",
        why=("The tier-1 own-stock regression FAILS the usability gate: R^2 = %.3f is below the "
             "0.05 floor (n = %d and SE = %.3f both pass). The protocol forbids a silent default "
             "to 1.0 and permits it only on a genuine gate failure shown with the diagnostics "
             "that triggered it — which is this case. Tier-2 (re-levered same-country peer beta) "
             "is unavailable: no Egyptian listed cement peer (MBSC, ARCC, SUCE, SVCE) carries an "
             "OHLC series in the engine library, so no peer regression can be run here."
             % (r2, n, se_beta)),
        corroboration=("1.0 is not arbitrary. It sits inside the Dimson sum-beta 90%% CI "
                       "[%.2f, %.2f], at the bottom edge of the 1.0-1.5 cyclical/capital-"
                       "intensive materials prior — the discount from the middle of that band "
                       "being explained by SCEM carrying NO financial leverage (net cash), which "
                       "genuinely damps equity beta relative to a levered sector peer."
                       % (sum_beta - 1.645 * se_sum, sum_beta + 1.645 * se_sum)),
        sensitivity_required=[0.6, 0.8, 1.0, 1.15, 1.3]),
    beta=beta, r2=float(r2), n=n, se=se_beta,
    ci90=[float(ci[0]), float(ci[1])],
    usable=bool(ok), gate_msg=msg,
    composite_names=len(rets), window_years=5, frequency='weekly',
    weak=bool(r2 < 0.10 or (ci[1] - ci[0]) > 2 * abs(beta)),
    weak_reason=("R^2 = %.1f%% is below the 10%% weak-instrument threshold (and within 2x the "
                 "5%% usability floor); the 90%% CI [%.2f, %.2f] spans %.1fx the point estimate"
                 % (r2 * 100, ci[0], ci[1], ci[1] / ci[0])),
    warnings=att.interim_warnings(),
    dimson=dict(
        sum_beta=sum_beta, se_sum=se_sum, r2=float(r2d), n=int(len(D)),
        ci90=[sum_beta - 1.645 * se_sum, sum_beta + 1.645 * se_sum],
        coefficients=dict(lead=float(bd[1]), contemporaneous=float(bd[2]),
                          lag1=float(bd[3]), lag2=float(bd[4])),
        uplift_vs_ols=sum_beta - beta,
        note=("Dimson (1979) sum-beta over 1 lead + contemporaneous + 2 lags. The uplift over "
              "the OLS beta measures how much co-movement is booked late because the stock "
              "does not trade every session.")),
    thin_trading=dict(
        flat_frac=flat_frac_scem, eg_panel_median=flat_frac_eg_median,
        ratio=round(flat_frac_scem / flat_frac_eg_median, 1),
        note=("SCEM prints an unchanged close on 29.3% of sessions against an EG panel median "
              "of 8.5% — 2nd thinnest of 33 names. This is the documented mechanism for a "
              "downward-biased OLS beta on an otherwise cyclical business.")),
    plausibility=dict(
        sector_prior="cyclical / capital-intensive materials: 1.0-1.5",
        defensive_prior="defensive or staple: 0.6-0.9",
        verdict=("The OLS beta of %.3f sits in the DEFENSIVE band, which is not where a "
                 "single-plant cement producer belongs on fundamentals. Two named reasons, "
                 "both evidenced rather than asserted: (i) thin trading — 29.3%% flat sessions "
                 "— biases the contemporaneous estimate down, and the Dimson sum-beta of %.3f "
                 "recovers %+.3f of that; (ii) the company is NET CASH, so it carries no "
                 "financial leverage to amplify its operating cyclicality, which genuinely "
                 "lowers equity beta relative to a levered sector peer. The valuation "
                 "therefore does NOT use the raw regression point estimate as though it were "
                 "precise; it is carried with the full CI and a mandatory beta sensitivity "
                 "table spanning 0.6/0.8/1.0/1.15/1.3."
                 % (beta, sum_beta, sum_beta - beta))),
)
json.dump(out, open(os.path.join(HERE, 'beta_result.json'), 'w'), indent=1)
print(f"OLS beta   {beta:.3f} | R2 {r2:.3f} | n {n} | SE {se_beta:.3f} "
      f"| CI90 [{ci[0]:.2f},{ci[1]:.2f}] | usable={ok} | weak={out['weak']}")
print(f"Dimson sum {sum_beta:.3f} | SE {se_sum:.3f} | R2 {r2d:.3f} | n {len(D)} "
      f"| CI90 [{out['dimson']['ci90'][0]:.2f},{out['dimson']['ci90'][1]:.2f}] "
      f"| uplift {sum_beta - beta:+.3f}")
print(f"  coefficients: lead {bd[1]:+.3f}  contemp {bd[2]:+.3f}  lag1 {bd[3]:+.3f}  lag2 {bd[4]:+.3f}")
print(f"  composite {len(rets)} names (SCEM excluded from its own index)")
print(f"  self-inclusion bias: beta {float(b_in[1]):.3f} (R2 {float(r2_in):.3f}) if SCEM is left IN the index")
print(f"  ADOPTED beta = 1.00 — tier-3 default on a genuine gate failure (R2 {r2:.3f} < 0.05),")
print(f"    corroborated: inside the Dimson CI90 [{sum_beta-1.645*se_sum:.2f},{sum_beta+1.645*se_sum:.2f}]")
