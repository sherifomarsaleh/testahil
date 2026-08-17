"""ADNOCLS beta — the adopted figure comes from engine/beta_regression.py, which is the
only admissible producer of a regression beta in this repository, and everything else in
this file is DISCLOSURE around it.

`own_stock_beta('ADNOCLS', 'AE', 'ADX')` resolves the regressor itself from the exchange
registry, runs the data-quality gate on both series before a single return is computed,
and matches the weekly grid to the exchange's real trading week. Its returned record is
the provenance: index file, index as-of, week rule, window, the diagnostic triple and the
interval. NOTHING IN THE DELIVERED DOCUMENTS DESCRIBES THE REGRESSION EXCEPT OUT OF THAT
RECORD — this study was one of the eight that were found still regressing against a
hand-built composite through their own script, and the failure that made the rule binding
was a source string describing a construction the study no longer used.

Two things the record does not carry are computed here and published as disclosure,
each labelled as the study-local construction it is:
  * the equal-weight composite variants — the ADX-listed subset and the wider ADX+DFM
    library — so the difference between a published capitalisation-weighted index and a
    hand-built proxy is visible as a number rather than assumed immaterial. They are
    reported, never adopted;
  * the self-inclusion variant, so the contamination from leaving the subject inside its
    own equal-weight index is visible as a number.

The sanctioned estimate is itself a lead-lag (Dimson) sum beta — one lag, the
contemporaneous term and one lead — so no separate lead-lag correction is computed or
published here: it is already inside the adopted figure. The cross-check the record does
carry is the Blume shrinkage, two-thirds of the measured slope plus one-third of 1.0.

Window: the routine takes the longest window up to five years. ADNOCLS listed on
02-Jun-2023 and the index series ends before the share's last session, so the window is
the listed history to the index's last session — reported from the record, not from a
five-year label.
"""
import sys, os, glob, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import numpy as np
import pandas as pd
from primitives import load_ohlc
from data_quality import clean_ohlc, screen
from wacc_builder import RegressionBetaAttempt
from beta_regression import own_stock_beta   # the only sanctioned producer of a beta

TKR = 'ADNOCLS'
# ADX-listed names in the UAE library. DFM names (DEWA, DIB, EMAAR, EMAARDEV, ENBD,
# SALIK) are excluded from the primary composite and used only in the disclosure variant.
ADX_NAMES = {'ADCB', 'ADIB', 'ADNOCGAS', 'AGTHIA', 'ALDAR', 'ALPHADHABI',
             'BURJEEL', 'EAND', 'FAB', 'IHC', 'LULU', 'TWOPOINTZERO'}


def weekly(px):
    return px.resample('W-FRI').last().dropna()


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


# THE ADOPTED FIGURE, AND WITH IT THE PROVENANCE. Everything below that describes the
# regression reads out of this record; the study does not choose the regressor, name the
# file, count the observations or date the series for itself.
SANCTIONED = own_stock_beta(TKR, 'AE', 'ADX')

IDX_PATH = os.path.join(HERE, '..', SANCTIONED['index_file'])   # resolved, not chosen
IDX_CODE = os.path.basename(SANCTIONED['index_file'])[:-4]
IDX_NAME = 'FTSE ADX General Index'
idx_raw, idx_log = clean_ohlc(load_ohlc(IDX_PATH), IDX_CODE, verbose=False,
                              market='AE')
idx_px = idx_raw.set_index('Date')['Price']

raw, _ = clean_ohlc(load_ohlc(os.path.join(HERE, f'{TKR}_Stock_Price_History.csv')),
                    TKR, verbose=False, market='AE')
flat_self = float(screen(raw)['flat_frac'])
sub = raw.set_index('Date')['Price']

comp_adx, comp_all, flats = {}, {}, []
for f in sorted(glob.glob(os.path.join(HERE, '..', 'raw_ohlc', 'AE', '*.csv'))):
    t = os.path.basename(f)[:-4]
    try:
        df, _ = clean_ohlc(load_ohlc(f), t, verbose=False, market='AE')
    except Exception as e:                                    # pragma: no cover
        print('skip', t, e)
        continue
    flats.append(float(screen(df)['flat_frac']))
    if t == TKR:                       # exclude the subject from its own index
        continue
    comp_all[t] = df.set_index('Date')['Price']
    if t in ADX_NAMES:
        comp_adx[t] = df.set_index('Date')['Price']
flat_median = float(np.median(flats))

span_years = (sub.index.max() - sub.index.min()).days / 365.25
cut = max(sub.index.min(), sub.index.max() - pd.DateOffset(years=5))
wk_sub = weekly(sub[sub.index >= cut])
re_ = np.log(wk_sub / wk_sub.shift(1)).dropna()


def build(comp):
    rets = {}
    for t, s in comp.items():
        w = weekly(s[s.index >= cut])
        r = np.log(w / w.shift(1)).dropna()
        if len(r) >= 50:
            rets[t] = r
    R = pd.DataFrame(rets)
    return rets, R.mean(axis=1, skipna=True)


rets_adx, mkt_adx = build(comp_adx)
rets_all, mkt_all = build(comp_all)

wk_idx = weekly(idx_px[idx_px.index >= cut])
mkt_index = np.log(wk_idx / wk_idx.shift(1)).dropna()

al = pd.concat([re_.rename('sub'), mkt_index.rename('mkt')], axis=1, sort=True).dropna()
unused_weeks = int((wk_sub.index > wk_idx.index.max()).sum())

# ---- the adopted figure, read out of the sanctioned record ------------------
beta, se_beta, r2, n = (SANCTIONED['beta'], SANCTIONED['se'],
                        SANCTIONED['r2'], SANCTIONED['n'])
ci = tuple(SANCTIONED['ci90'])
ok, msg = SANCTIONED['usable'], SANCTIONED['gate_msg']
att = RegressionBetaAttempt(beta=beta, r_squared=r2, n_obs=n, se_beta=se_beta,
                            frequency=SANCTIONED['frequency'])

# ---- equal-weight composite variants, disclosed not adopted ----------------
al_adx = pd.concat([re_.rename('sub'), mkt_adx.rename('mkt')], axis=1, sort=True).dropna()
b_c, r2_c, se_c, _ = ols(
    np.column_stack([np.ones(len(al_adx)), al_adx['mkt'].values]), al_adx['sub'].values)
al_full = pd.concat([re_.rename('sub'), mkt_all.rename('mkt')], axis=1, sort=True).dropna()
b_f, r2_f, se_f, _ = ols(
    np.column_stack([np.ones(len(al_full)), al_full['mkt'].values]), al_full['sub'].values)

# NO LEAD-LAG BLOCK IS COMPUTED HERE. The sanctioned routine runs the regression with one
# lag, the contemporaneous term and one lead and returns their sum, so the adopted beta IS
# the lead-lag estimate. A second, study-local sum-beta published beside it as "the
# correction" would tell a reader the adopted figure lacks a correction it already carries.
# The cross-check the record does supply is the Blume shrinkage below.
BLUME = float(SANCTIONED['blume_crosscheck'])

# ---- the subject is INSIDE the published index, and that cannot be removed ----
# ADNOCLS is a constituent of the index it is regressed against. On an equal-weight
# proxy the subject can simply be dropped; on a published capitalisation-weighted
# index it cannot. The equal-weight proxy is therefore run both ways so the size of
# that contamination is measurable, and the measurement is reported against the index
# regression rather than left implicit.
mkt_in = pd.DataFrame({**rets_adx, TKR: re_}).mean(axis=1, skipna=True)
al_in = pd.concat([re_.rename('sub'), mkt_in.rename('mkt')], axis=1, sort=True).dropna()
b_in, r2_in, se_in, _ = ols(
    np.column_stack([np.ones(len(al_in)), al_in['mkt'].values]), al_in['sub'].values)

# ---- the gate decides ------------------------------------------------------
# The gate is the routine's own, not a second one re-implemented here: a study that
# re-derives the verdict can disagree with the record it is quoting.
weak = bool(SANCTIONED['weak'])
if not ok:                                                   # pragma: no cover
    raise SystemExit(f'the sanctioned regression FAILS the usability gate: {msg}. A '
                     f'silent default is forbidden — stop and disclose.')
beta_used = beta
basis = ("tier-1 own-stock weekly regression against the published index of the share's "
         "own exchange, produced by the engine's sanctioned routine")
why = (f"n = {n} weekly observations against the published index of the share's own "
       f"exchange, resolved by the routine from the exchange the share is listed on, over "
       f"{SANCTIONED['first_obs']} to {SANCTIONED['last_obs']}. R-squared = {r2:.3f}, "
       f"SE(beta) = {se_beta:.3f}. {msg}.")

out = dict(
    ticker=TKR,
    sanctioned=SANCTIONED,
    beta=beta, r2=float(r2), n=int(n), se=se_beta,
    ci90=[float(ci[0]), float(ci[1])],
    usable=bool(ok), gate_msg=msg,
    regressor=IDX_NAME,
    regressor_code=IDX_CODE,
    regressor_file=SANCTIONED['index_file'],
    regressor_asof=SANCTIONED['index_asof'],
    regressor_conforming=bool(SANCTIONED['conforming']),
    regressor_interim_note=SANCTIONED['interim_note'],
    week_rule=SANCTIONED['week_rule'],
    regressor_basis=('The published capitalisation-weighted index of the exchange the '
                     'share is listed on — the local index the beta rule asks for, '
                     'resolved from that exchange by the routine rather than chosen by '
                     'the study.'),
    regressor_rows=int(len(idx_raw)),
    regressor_span=[str(idx_raw['Date'].min().date()), str(idx_raw['Date'].max().date())],
    regressor_repairs=SANCTIONED['index_dq'],
    stock_repairs=SANCTIONED['stock_dq'],
    unused_stock_weeks=unused_weeks,
    unused_note=(f"The index series ends {SANCTIONED['index_asof']}, before the last stock "
                 f'session used elsewhere in the study (2026-08-07). {unused_weeks} weekly '
                 'stock observations therefore fall outside the regression. The window '
                 'stops where the index stops rather than pairing the stock against a '
                 'stale index level.'),
    composite_names=len(rets_adx), composite_basis='ADX-listed names in the UAE library',
    window_years=SANCTIONED['window_years'], frequency=SANCTIONED['frequency'],
    first_obs=SANCTIONED['first_obs'], last_obs=SANCTIONED['last_obs'],
    listed_years=round(span_years, 2),
    window_note=("The stock listed on 02-Jun-2023 and the index series ends before its "
                 f"last session, so the regression window runs {SANCTIONED['first_obs']} "
                 f"to {SANCTIONED['last_obs']} — {SANCTIONED['window_years']:.2f} years, "
                 "short of the five-year target, which no amount of method can create."),
    lead_lag=("The estimate is a lead-lag sum beta: the routine regresses on one lag, the "
              "contemporaneous return and one lead and sums the three slopes, so the "
              "co-movement a thinly traded share books late is already inside the adopted "
              "figure rather than published beside it as a separate correction."),
    blume_crosscheck=BLUME,
    blume_note=("Blume shrinkage on the adopted slope — two-thirds of the measured figure "
                "plus one-third of 1.0, the standard adjustment for the tendency of a "
                "measured beta to drift toward the market over time. It is a cross-check "
                "reported by the same record, and it is not what the study discounts at."),
    weak=weak,
    weak_reason=(f"R-squared = {r2*100:.1f}% against the 10% weak-instrument threshold; "
                 f"the 90% confidence interval [{ci[0]:.2f}, {ci[1]:.2f}] spans "
                 f"{(ci[1]-ci[0])/abs(beta):.2f}x the point estimate"),
    warnings=att.interim_warnings(),
    adopted=dict(
        beta_used=float(beta_used), basis=basis, why=why,
        corroboration=(
            f"Cross-checked three ways. (i) Shrunk toward the market on the Blume "
            f"adjustment the same record reports, the slope is {BLUME:.3f}, which "
            f"{'sits inside' if ci[0] <= BLUME <= ci[1] else 'sits outside'} the "
            f"regression's own 90% interval of [{ci[0]:.2f}, {ci[1]:.2f}] and moves the "
            f"estimate {'toward' if abs(BLUME - 1) < abs(beta_used - 1) else 'away from'} "
            f"one. (ii) Regressing against an equal-weight composite of the exchange's own "
            f"names instead of the published index gives {float(b_c[1]):.3f} "
            f"(R-squared {float(r2_c):.3f}), and against the wider ADX+DFM library "
            f"{float(b_f[1]):.3f} (R-squared {float(r2_f):.3f}). (iii) The sector prior for "
            f"a listed tanker owner is 0.9-1.4 and for a contracted, fee-based marine "
            f"services provider 0.5-0.9; the adopted figure is read against both in the "
            f"study rather than accepted at face value."),
        sensitivity_required=[0.5, 0.7, 0.9, 1.1, 1.3]),
    composite_variant=dict(beta=float(b_c[1]), r2=float(r2_c), n=int(len(al_adx)),
                           se=float(se_c[1]), names=len(rets_adx),
                           note=("Equal-weight composite of the exchange's own listed "
                                 "names, the subject excluded. This was the regressor "
                                 "before the published index was available; disclosed so "
                                 "the effect of the change is visible, not adopted.")),
    full_library_variant=dict(beta=float(b_f[1]), r2=float(r2_f), n=int(len(al_full)),
                              se=float(se_f[1]), names=len(rets_all),
                              note="ADX + DFM equal-weight composite; disclosed, not adopted."),
    self_inclusion_bias=dict(
        beta_proxy_including_subject=float(b_in[1]), r2_including=float(r2_in),
        beta_proxy_excluding_subject=float(b_c[1]), r2_excluding=float(r2_c),
        note=("The subject is a constituent of the published index it is regressed "
              "against, and on a capitalisation-weighted index that cannot be undone. "
              "The equal-weight proxy is run both ways to measure how large the resulting "
              "self-covariance is: the two figures here differ by "
              f"{abs(float(b_in[1]) - float(b_c[1])):.3f}, which is the scale of the "
              "upward pull the published-index beta also carries. It is disclosed rather "
              "than assumed away, and it works against the study's own conclusion, since "
              "removing it would lower the beta further.")),
    thin_trading=dict(
        flat_frac=round(flat_self, 4), ae_panel_median=round(flat_median, 4),
        ratio=round(flat_self / flat_median, 2),
        note=("Share of sessions closing unchanged, against the median of the UAE library. "
              "A high ratio is the documented mechanism for a downward-biased "
              "contemporaneous beta.")),
    plausibility=dict(
        tanker_owner_prior="listed crude/product tanker owner: 0.9-1.4",
        contracted_services_prior="contracted, fee-based marine services: 0.5-0.9",
        mix_note=("Roughly half of group revenue is contracted work for the parent group "
                  "and half is exposed to spot and short-charter shipping markets, so an "
                  "estimate between the two priors is the economically coherent answer.")),
)
json.dump(out, open(os.path.join(HERE, 'beta_result.json'), 'w'), indent=1)
print(f"SANCTIONED beta {beta:.4f} | R2 {r2:.3f} | n {n} | SE {se_beta:.3f} "
      f"| CI90 [{ci[0]:.4f},{ci[1]:.4f}] | usable={ok} | weak={weak}")
print(f"  gate: {msg}")
print(f"  regressor {IDX_CODE} ({SANCTIONED['index_file']}) as of "
      f"{SANCTIONED['index_asof']}, week rule {SANCTIONED['week_rule']}, "
      f"conforming={SANCTIONED['conforming']}; lead-lag sum beta by construction")
print(f"  Blume cross-check {BLUME:.4f}")
print(f"  composite {len(rets_adx)} ADX names ({TKR} excluded from its own index); "
      f"full library variant beta {float(b_f[1]):.3f} on {len(rets_all)} names")
print(f"  self-inclusion: beta {float(b_in[1]):.3f} (R2 {float(r2_in):.3f}) if {TKR} is left IN")
print(f"  thin trading: flat_frac {flat_self:.3f} vs AE median {flat_median:.3f} "
      f"({flat_self/flat_median:.2f}x)")
print(f"  regression window {SANCTIONED['window_years']:.2f} yr "
      f"({SANCTIONED['first_obs']} to {SANCTIONED['last_obs']}); "
      f"listed history {span_years:.2f} yr from 02-Jun-2023")
print(f"  ADOPTED beta = {beta_used:.3f} — {basis}")
