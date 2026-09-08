"""DU beta — through the SANCTIONED house routine, never a study-local regression.

REWRITTEN 08-09-2026, critique response finding S1. What stood here until this edition was a
study-local weekly regression: it read a reformatted copy of the FTSE ADX General series from
INSIDE this directory (ADXGI_daily.csv), sampled its own weekly grid off ISO week numbers, and
applied no Dimson lead-lag correction. It returned beta 0.488. SIGCM clause 6 and CLAUDE.md
both say the same thing in the same words -- "NEVER hand-roll a study-local beta script" -- and
this study was one of the scripts they were written about.

Run through beta_regression.own_stock_beta(), which resolves the regressor itself from
raw_indices/, runs Step 0.0 on both series, matches the weekly grid to the exchange's real
trading week and Dimson-corrects for thin trading, the answer is 0.5569, not 0.488. That is
worth -AED 1.05 per share, -6.3% of the central, and it moves the answer TOWARD the price.

THE REGRESSOR IS THE REGISTERED INTERIM AND IT IS DISCLOSED AS ONE. DU lists on the DFM;
wacc_builder maps ("AE","DFM") to FTSE ADX General as a labelled exception adopted 10-Aug-2026
and held open 23-Aug-2026, on measured evidence that FADGI explains the DFM names better than
the ADX names it actually covers. index_interim_note() carries that disclosure and ends "Quote
this note wherever the beta is quoted, and never call such a beta conforming" -- so the record
below carries the note verbatim and conforming=False, and every document that quotes the beta
quotes the note with it.

The DFM General cross-check runs against the REGISTERED raw_indices/AE/DFMGI.csv (2,307 rows),
not the 1,099-row copy this directory used to carry, and it reuses beta_regression's OWN
helpers rather than re-implementing them.
"""
import sys, os, glob, json

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.join(HERE, '..')
sys.path.insert(0, ENGINE)

import numpy as np
import pandas as pd

import beta_regression as BR
from beta_regression import own_stock_beta
from primitives import load_ohlc
from data_quality import clean_ohlc
from wacc_builder import RegressionBetaAttempt
from beta_regression import WEEK_END

# ---------------------------------------------------------------------------
# THE ADOPTED BETA — one call, no local arithmetic
# ---------------------------------------------------------------------------
rec = own_stock_beta('DU', 'AE', 'DFM', root=ENGINE)

# ---------------------------------------------------------------------------
# CROSS-CHECKS, published beside it and never adopted. Both reuse the module's own
# helpers; neither is a second implementation of the adopted number.
# ---------------------------------------------------------------------------
RULE = WEEK_END.get('AE', 'W-FRI')


def _against(index_csv, dimson=True):
    s, _ = clean_ohlc(load_ohlc(os.path.join(ENGINE, 'raw_ohlc', 'AE', 'DU.csv')),
                      'DU', verbose=False, market='AE')
    i, _ = clean_ohlc(load_ohlc(index_csv), os.path.basename(index_csv)[:-4],
                      verbose=False, market='AE')
    s = s.set_index('Date').sort_index()['Price']
    i = i.set_index('Date').sort_index()['Price']
    cut = s.index.max() - pd.DateOffset(years=5)
    al = pd.concat([BR._weekly_logret(s[s.index >= cut], RULE).rename('y'),
                    BR._weekly_logret(i[i.index >= cut], RULE).rename('m')],
                   axis=1, sort=True).dropna()
    if dimson:
        al = al.assign(lag=al['m'].shift(1), lead=al['m'].shift(-1)).dropna()
        X = np.column_stack([np.ones(len(al)), al['lag'], al['m'], al['lead']])
        b, r2, cov, _ = BR._ols(al['y'].values, X)
        beta, se = float(b[1:4].sum()), float(np.sqrt(cov[1:4, 1:4].sum()))
    else:
        X = np.column_stack([np.ones(len(al)), al['m']])
        b, r2, cov, _ = BR._ols(al['y'].values, X)
        beta, se = float(b[1]), float(np.sqrt(cov[1, 1]))
    return dict(beta=beta, r2=float(r2), se=se, n=len(al),
                index_file=os.path.relpath(index_csv, ENGINE),
                index_asof=str(i.index.max().date()))


dfm = _against(os.path.join(ENGINE, 'raw_indices', 'AE', 'DFMGI.csv'))
dfm['note'] = ('DFM General Index, DU\'s own listing venue, from the REGISTERED series '
               'raw_indices/AE/DFMGI.csv. HELD BUT NOT REGISTERED as a regressor: '
               'wacc_builder.EXCHANGE_INDEX still maps ("AE","DFM") to FTSE ADX General and a '
               'session may not re-point it on the reasoning that this file exists. Published '
               'as a labelled cross-check, never adopted.')

# ---- equal-weight AE composite: a coverage artefact, shown so its distance is visible ----
comp = {}
for f in sorted(glob.glob(os.path.join(ENGINE, 'raw_ohlc', 'AE', '*.csv'))):
    tkr = os.path.basename(f)[:-4]
    if tkr == 'DU':
        continue
    try:
        df, _ = clean_ohlc(load_ohlc(f), tkr, verbose=False, market='AE')
        comp[tkr] = df.set_index('Date').sort_index()['Price']
    except Exception as exc:                                    # pragma: no cover
        print('skip', tkr, exc)
_du, _ = clean_ohlc(load_ohlc(os.path.join(ENGINE, 'raw_ohlc', 'AE', 'DU.csv')),
                    'DU', verbose=False, market='AE')
_du = _du.set_index('Date').sort_index()['Price']
_cut = _du.index.max() - pd.DateOffset(years=5)
_R = pd.DataFrame({t: BR._weekly_logret(s[s.index >= _cut], RULE) for t, s in comp.items()})
_mkt = _R.mean(axis=1, skipna=True).dropna()
_al = pd.concat([BR._weekly_logret(_du[_du.index >= _cut], RULE).rename('y'),
                 _mkt.rename('m')], axis=1, sort=True).dropna()
_X = np.column_stack([np.ones(len(_al)), _al['m']])
_b, _r2, _cov, _ = BR._ols(_al['y'].values, _X)
composite = dict(beta=float(_b[1]), r2=float(_r2), se=float(np.sqrt(_cov[1, 1])),
                 n=len(_al), names=len(comp),
                 note='equal-weight AE library composite. A CONSTITUENT COMPOSITE IS NOT A '
                      'REGRESSOR and is not a tier: it changes whenever a stock is posted, it '
                      'mixes ADX with DFM inside one market code, and it shares constituents '
                      'with the panel it prices. Shown only so its distance from the published '
                      'index is visible.')

rec['dfm_alt'] = dfm
rec['composite_alt'] = composite
json.dump(rec, open(os.path.join(HERE, 'beta_result.json'), 'w'), indent=1)

print(f"ADOPTED  beta {rec['beta']:.4f} | R2 {rec['r2']:.3f} | n {rec['n']} | SE {rec['se']:.3f}"
      f" | CI90 [{rec['ci90'][0]:.2f},{rec['ci90'][1]:.2f}] | dimson={rec['dimson']}"
      f" | usable={rec['usable']} | conforming={rec['conforming']}")
print(f"         index {rec['index_file']} as of {rec['index_asof']}, week rule {rec['week_rule']}")
print(f"CROSS    DFM General {dfm['beta']:.4f} (R2 {dfm['r2']:.3f}, n {dfm['n']}) "
      f"| composite {composite['beta']:.4f} (n {composite['n']}, {composite['names']} names)")
print("INTERIM NOTE CARRIED:", (rec['interim_note'] or '')[:80], '...')
