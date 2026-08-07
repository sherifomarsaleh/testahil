"""ARCC beta — tier-1 own-stock weekly regression against an equal-weight EGX composite
built from the full engine/raw_ohlc/EG library (house pattern: CLHO / RMDA / SWDY / SCEM),
5-year window, RegressionBetaAttempt usability gate.

Three things are produced rather than asserted:
  * the diagnostic triple (n, R-squared, SE) and the resulting 90% confidence interval;
  * a Dimson (1979) lead-lag sum-beta, which recovers the co-movement a thinly traded
    stock books late and which is the standard correction for non-synchronous trading;
  * the self-inclusion variant, so the contamination from leaving the subject inside its
    own equal-weight index is visible as a number rather than dismissed as negligible.

The ADOPTED beta is decided by the gate, in code, not chosen in prose.
"""
import sys, os, glob, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import numpy as np
import pandas as pd
from primitives import load_ohlc
from data_quality import clean_ohlc, screen
from wacc_builder import RegressionBetaAttempt

TKR = 'ARCC'


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


raw, _ = clean_ohlc(load_ohlc(os.path.join(HERE, f'{TKR}_Stock_Price_History.csv')),
                    TKR, verbose=False, market='EG')
flat_self = float(screen(raw)['flat_frac'])
sub = raw.set_index('Date')['Price']

comp, flats = {}, []
for f in sorted(glob.glob(os.path.join(HERE, '..', 'raw_ohlc', 'EG', '*.csv'))):
    t = os.path.basename(f)[:-4]
    try:
        df, _ = clean_ohlc(load_ohlc(f), t, verbose=False, market='EG')
    except Exception as e:                                    # pragma: no cover
        print('skip', t, e)
        continue
    flats.append(float(screen(df)['flat_frac']))
    if t != TKR:                       # exclude the subject from its own index
        comp[t] = df.set_index('Date')['Price']
flat_median = float(np.median(flats))

cut = sub.index.max() - pd.DateOffset(years=5)
wk_sub = weekly(sub[sub.index >= cut])
rets = {}
for t, s in comp.items():
    w = weekly(s[s.index >= cut])
    r = np.log(w / w.shift(1)).dropna()
    if len(r) >= 100:
        rets[t] = r
R = pd.DataFrame(rets)
mkt = R.mean(axis=1, skipna=True)                  # equal-weight composite weekly log-return
re_ = np.log(wk_sub / wk_sub.shift(1)).dropna()
al = pd.concat([re_.rename('sub'), mkt.rename('mkt')], axis=1, sort=True).dropna()

# ---- tier-1 contemporaneous OLS beta ---------------------------------------
x, y = al['mkt'].values, al['sub'].values
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
bd, r2d, sed, _ = ols(Xd, D['sub'].values)
sum_beta = float(bd[1:].sum())
Xd_inv = np.linalg.inv(Xd.T @ Xd)
resid = D['sub'].values - Xd @ bd
sigma2 = float((resid ** 2).sum() / (len(D) - Xd.shape[1]))
cov_b = Xd_inv * sigma2
se_sum = float(np.sqrt(cov_b[1:, 1:].sum()))
dim_ci = (sum_beta - 1.645 * se_sum, sum_beta + 1.645 * se_sum)

# ---- disclosure variant: the same regression WITH the subject left in the index --
mkt_in = pd.DataFrame({**rets, TKR: re_}).mean(axis=1, skipna=True)
al_in = pd.concat([re_.rename('sub'), mkt_in.rename('mkt')], axis=1, sort=True).dropna()
b_in, r2_in, se_in, _ = ols(
    np.column_stack([np.ones(len(al_in)), al_in['mkt'].values]), al_in['sub'].values)

# ---- the gate decides ------------------------------------------------------
weak = bool(r2 < 0.10 or (ci[1] - ci[0]) > 2 * abs(beta))
if ok:
    beta_used = beta
    basis = 'tier-1 own-stock weekly regression (usability gate PASSED)'
    why = (f"n = {n} weekly observations, R-squared = {r2:.3f} against the 0.05 floor, "
           f"SE(beta) = {se_beta:.3f} against |beta| = {abs(beta):.3f}. All three "
           f"conditions of the usability gate are met, so the regression estimate is "
           f"adopted rather than a default.")
else:
    beta_used = 1.0
    basis = 'tier-3 default on a GENUINE usability-gate failure, disclosed with diagnostics'
    why = (f"The tier-1 regression FAILS the usability gate: {msg}. A silent default is "
           f"forbidden; a default shown with the diagnostics that triggered it is "
           f"permitted, and this is that case.")

out = dict(
    ticker=TKR,
    beta=beta, r2=float(r2), n=int(n), se=se_beta,
    ci90=[float(ci[0]), float(ci[1])],
    usable=bool(ok), gate_msg=msg,
    composite_names=len(rets), window_years=5, frequency='weekly',
    weak=weak,
    weak_reason=(f"R-squared = {r2*100:.1f}% against the 10% weak-instrument threshold; "
                 f"the 90% confidence interval [{ci[0]:.2f}, {ci[1]:.2f}] spans "
                 f"{(ci[1]-ci[0])/abs(beta):.2f}x the point estimate"),
    warnings=att.interim_warnings(),
    adopted=dict(
        beta_used=float(beta_used), basis=basis, why=why,
        corroboration=(
            f"Cross-checked two ways. (i) The Dimson sum-beta is {sum_beta:.3f} with a 90% "
            f"interval of [{dim_ci[0]:.2f}, {dim_ci[1]:.2f}]; the adopted {beta_used:.2f} "
            f"{'sits inside' if dim_ci[0] <= beta_used <= dim_ci[1] else 'sits outside'} it. "
            f"(ii) The simple prior for a cyclical, capital-intensive materials business is "
            f"1.0-1.5 and for a defensive or staple business 0.6-0.9; the adopted figure is "
            f"read against both in the study rather than accepted at face value."),
        sensitivity_required=[0.6, 0.8, 1.0, 1.15, 1.3]),
    dimson=dict(
        sum_beta=sum_beta, se_sum=se_sum, r2=float(r2d), n=int(len(D)),
        ci90=[float(dim_ci[0]), float(dim_ci[1])],
        coefficients=dict(lead=float(bd[1]), contemporaneous=float(bd[2]),
                          lag1=float(bd[3]), lag2=float(bd[4])),
        uplift_vs_ols=float(sum_beta - beta),
        note=("Dimson (1979) sum-beta over one lead, the contemporaneous term and two lags. "
              "The uplift over the contemporaneous OLS beta measures how much co-movement "
              "is booked late because the stock does not trade on every session.")),
    self_inclusion_bias=dict(
        beta_index_including_subject=float(b_in[1]), r2_including=float(r2_in),
        beta_index_excluding_subject=beta, r2_excluding=float(r2),
        note=("Leaving the subject inside its own equal-weight index injects a "
              "self-covariance term into the numerator. The excluding figure is the correct "
              "one and is what is reported; the including figure is disclosed so the size of "
              "the contamination is visible rather than assumed away.")),
    thin_trading=dict(
        flat_frac=round(flat_self, 4), eg_panel_median=round(flat_median, 4),
        ratio=round(flat_self / flat_median, 2),
        note=("Share of sessions closing unchanged, against the median of the Egyptian "
              "library. A high ratio is the documented mechanism for a downward-biased "
              "contemporaneous beta.")),
    plausibility=dict(
        sector_prior="cyclical / capital-intensive materials: 1.0-1.5",
        defensive_prior="defensive or staple: 0.6-0.9",
        net_cash_note=("The company carries no net financial leverage, which genuinely damps "
                       "equity beta relative to a levered sector peer and is a real reason "
                       "for an estimate below the cyclical band rather than an excuse.")),
)
json.dump(out, open(os.path.join(HERE, 'beta_result.json'), 'w'), indent=1)
print(f"OLS beta   {beta:.3f} | R2 {r2:.3f} | n {n} | SE {se_beta:.3f} "
      f"| CI90 [{ci[0]:.2f},{ci[1]:.2f}] | usable={ok} | weak={weak}")
print(f"  gate: {msg}")
print(f"Dimson sum {sum_beta:.3f} | SE {se_sum:.3f} | R2 {r2d:.3f} | n {len(D)} "
      f"| CI90 [{dim_ci[0]:.2f},{dim_ci[1]:.2f}] | uplift {sum_beta-beta:+.3f}")
print(f"  coefficients: lead {bd[1]:+.3f}  contemp {bd[2]:+.3f}  lag1 {bd[3]:+.3f}  lag2 {bd[4]:+.3f}")
print(f"  composite {len(rets)} names ({TKR} excluded from its own index)")
print(f"  self-inclusion: beta {float(b_in[1]):.3f} (R2 {float(r2_in):.3f}) if {TKR} is left IN")
print(f"  thin trading: flat_frac {flat_self:.3f} vs EG median {flat_median:.3f} "
      f"({flat_self/flat_median:.2f}x)")
print(f"  ADOPTED beta = {beta_used:.3f} — {basis}")
