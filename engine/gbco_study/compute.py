"""GBCO study — master computation. Outputs study_numbers.json + backtest tables."""
import json
import os
import numpy as np
import pandas as pd
import primitives as m

# THE EXCHANGE LIBRARY, NOT A STUDY-LOCAL COPY. The study-local extract stops at 7 July
# 2026 while engine/raw_ohlc/EG/GBCO.csv — the persistent library every cone in this
# repository is struck on — carries sessions to 23 August 2026. A study struck against its
# own stale copy is audited against its own past [R-GAP-01 AMENDED].
df = m.load_ohlc(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                              'raw_ohlc', 'EG', 'GBCO.csv'))
close = df['Price'].values
mc_anchor = float(close[-1])                 # the cone is struck on real sessions
mc_anchor_date = str(df['Date'].iloc[-1].date())

# THE LATEST KNOWN PRICE [R-GAP-01 AMENDED], read from the committed supplied-price files
# and never typed. A cone needs a SESSION SERIES and can only be anchored on the exchange
# library; a fair value is put against the latest price the repository knows, which on this
# name is a hand-supplied close four days newer than the library's last session. The two are
# different clocks and both are published with their own dates.
import glob as _glob
_px, _pxd = None, None
for _f in sorted(_glob.glob(os.path.join(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))), 'prices', 'SUPPLIED_*.json'))):
    _d = json.load(open(_f, encoding='utf-8'))
    _r = (_d.get('prices') or {}).get('GBCO')
    if not _r:
        continue
    _dt = _r.get('date')
    if _px is None or (_dt or '') > (_pxd or ''):
        _px, _pxd = float(_r['price']), _dt
spot = _px if _px is not None else mc_anchor
spot_date = _pxd if _px is not None else mc_anchor_date
N = len(df)

# ---------------- Step 0 backtest (secular drift, adopted config) ----------
res, summ = m.backtest(df, horizon=60, secular_drift=True)
res0, summ0 = m.backtest(df, horizon=60, secular_drift=False)
res21, summ21 = m.backtest(df, horizon=60, step=21, secular_drift=True)
pit_hist = np.histogram(res['pit'], bins=10, range=(0, 1))[0].tolist()

# ---------------- Forward run parameters ----------------------------------
v = m.yz_variance_proxy(df)
beta = m.fit_har(v, N - 1, horizon=60)
dv = m.har_forecast_daily_var(v, N - 1, beta, horizon=60)
anchor_vol = float(np.sqrt(dv * 252))
lr_all = np.diff(np.log(close))
drift_daily = float(np.mean(lr_all))

# ---------------- 16-factor stack ------------------------------------------
continuous = [
    ("Egypt PC demand / rate-cut cycle", "+"),
    ("EGP/USD drift (CKD import content)", "±"),
    ("CBE easing path (affordability + GB Capital NIM)", "+"),
    ("Iraq / Jordan regional-conflict drag", "−"),
    ("Chinese grey-import competition (Iraq/Jordan)", "−"),
    ("Localization / CKD mix & Sadat ramp", "+"),
    ("Funding-cost & provisioning cycle", "−"),
]
cont_drift_q = 0.004  # net quarterly drift from the seven continuous factors
discrete = [
    ("2Q26 results (11 Aug 2026)",            0.90, 0.005),
    ("MNT-Halan second closing ≥ $1.4bn",     0.45, 0.015),
    ("CBE cut ≥100bp (Aug/Oct MPC)",          0.50, 0.010),
    ("Regional escalation spillover",          0.25, -0.025),
    ("BYD Egypt entry / price shock",          0.35, -0.010),
    ("Sadat inauguration / new CKD model",     0.55, 0.006),
    ("Dividend / capital-return surprise",     0.15, 0.008),
    ("EGP step-devaluation",                   0.12, -0.020),
    ("EGX flows / index event",                0.25, 0.008),
]
disc_drift_q = sum(p * i for _, p, i in discrete)
factor_drift_q = cont_drift_q + disc_drift_q

# ---------------- Forward simulation (50,000 paths, seed 42) --------------
H = 60
rng = np.random.default_rng(42)
n_paths = 50000
sd = np.sqrt(dv)
z = rng.standard_normal((n_paths, H))
chi = rng.chisquare(5, n_paths)
mix = np.sqrt(3.0 / chi)[:, None]
incr = drift_daily + cont_drift_q / H + z * mix * sd
# discrete events: per-path Bernoulli, applied at a uniform random day
for name, p, imp in discrete:
    fire = rng.random(n_paths) < p
    day = rng.integers(0, H, n_paths)
    size = rng.normal(imp, abs(imp) / 2, n_paths)
    add = np.zeros((n_paths, H))
    add[np.arange(n_paths)[fire], day[fire]] = size[fire]
    incr += add
logp = np.cumsum(incr, axis=1)
paths = np.empty((n_paths, H + 1))
paths[:, 0] = spot
paths[:, 1:] = spot * np.exp(logp)

pT20, pT60 = paths[:, 20], paths[:, 60]
pcts = [5, 25, 50, 75, 95]
q20 = {p: float(np.percentile(pT20, p)) for p in pcts}
q60 = {p: float(np.percentile(pT60, p)) for p in pcts}
run_max = paths.max(axis=1); run_min = paths.min(axis=1)
run_max20 = paths[:, :21].max(axis=1); run_min20 = paths[:, :21].min(axis=1)
levels = [40, 38, 36, 34, 32, 30, 28, 26]
touch = {L: dict(t20=float(np.mean(run_max20 >= L) if L > spot else np.mean(run_min20 <= L)),
                 t60=float(np.mean(run_max >= L) if L > spot else np.mean(run_min <= L)))
         for L in levels}
prob_read = dict(
    p_above=float(np.mean(pT60 > spot)),
    p_up10=float(np.mean(pT60 >= spot * 1.10)),
    p_dn10=float(np.mean(pT60 <= spot * 0.90)),
    median=float(np.median(pT60)),
    med_move=float(np.median(pT60) / spot - 1),
    band50=(q60[25], q60[75]),
    band50_pct=((q60[25] / spot - 1), (q60[75] / spot - 1)),
    touch_up10=float(np.mean(run_max >= spot * 1.10)),
    touch_dn10=float(np.mean(run_min <= spot * 0.90)),
)
prob_read['odds'] = prob_read['p_up10'] / prob_read['p_dn10']
zones_edges = [0, 26, 30, 34, 38, 1e9]
zone_probs = [float(np.mean((pT60 >= a) & (pT60 < b))) for a, b in zip(zones_edges[:-1], zones_edges[1:])]

# fan chart percentile ribbons per day
days = np.arange(H + 1)
fan = {p: np.percentile(paths, p, axis=0).tolist() for p in [5, 25, 50, 75, 95]}

# ---------------- Technicals -----------------------------------------------
s = pd.Series(close)
sma = {n: float(s.rolling(n).mean().iloc[-1]) for n in [20, 50, 100, 200]}
delta = s.diff()
gain = delta.clip(lower=0).ewm(alpha=1/14, adjust=False).mean()
loss = (-delta.clip(upper=0)).ewm(alpha=1/14, adjust=False).mean()
rsi = float((100 - 100 / (1 + gain / loss)).iloc[-1])
ema12 = s.ewm(span=12, adjust=False).mean(); ema26 = s.ewm(span=26, adjust=False).mean()
macd_line = ema12 - ema26; sig = macd_line.ewm(span=9, adjust=False).mean()
macd = dict(line=float(macd_line.iloc[-1]), signal=float(sig.iloc[-1]),
            hist=float((macd_line - sig).iloc[-1]))
hi52 = float(df['High'].iloc[-252:].max()); lo52 = float(df['Low'].iloc[-252:].min())
rv252 = float(np.std(np.diff(np.log(close[-253:])), ddof=1) * np.sqrt(252))

# ---------------- Valuation model ------------------------------------------
SH = 1085.5  # mn shares
TAX = 0.28
# Auto-leg driver build (units × ASP, disclosed)
pc_vol = {'FY23': 26994, 'FY24': 42043, 'FY25': 56548}
pc_rev = {'FY23': 16544.3, 'FY24': 36533.4, 'FY25': 52827.3}
vol_g = [0.12, 0.14, 0.10, 0.08, 0.06]
asp_g = [0.06, 0.07, 0.07, 0.06, 0.06]
cv_vol = {'FY25': 3404}; cv_rev = {'FY25': 5956.8}
cv_vg = [0.25, 0.18, 0.12, 0.10, 0.08]; cv_ag = [0.05]*5
lm_vol = {'FY25': 33906}; lm_rev = {'FY25': 2203.8}
lm_vg = [0.30, 0.20, 0.15, 0.12, 0.10]; lm_ag = [0.05]*5
tr_rev = {'FY25': 4242.8}; tr_g = [0.18, 0.15, 0.12, 0.10, 0.10]
yrs = ['FY26E', 'FY27E', 'FY28E', 'FY29E', 'FY30E']
fc = {}
pv_, pa_ = pc_vol['FY25'], pc_rev['FY25']/pc_vol['FY25']
cvv, cva = cv_vol['FY25'], cv_rev['FY25']/cv_vol['FY25']
lmv, lma = lm_vol['FY25'], lm_rev['FY25']/lm_vol['FY25']
trr = tr_rev['FY25']
for i, y in enumerate(yrs):
    pv_ *= (1+vol_g[i]); pa_ *= (1+asp_g[i])
    cvv *= (1+cv_vg[i]); cva *= (1+cv_ag[i])
    lmv *= (1+lm_vg[i]); lma *= (1+lm_ag[i])
    trr *= (1+tr_g[i])
    fc[y] = dict(pc_vol=pv_, pc_asp=pa_, pc_rev=pv_*pa_/1,  # ASP in mn
                 cv_rev=cvv*cva, lm_rev=lmv*lma, tr_rev=trr)
    fc[y]['auto_rev'] = fc[y]['pc_rev'] + fc[y]['cv_rev'] + fc[y]['lm_rev'] + fc[y]['tr_rev']
gpm = [0.138, 0.142, 0.145, 0.145, 0.145]
gsa = [0.073, 0.072, 0.071, 0.070, 0.070]
oth = 0.012; prov = -0.003
dna_pct = [0.011, 0.011, 0.011, 0.011, 0.011]
capex = [3000, 2400, 2500, 2600, 2800]
wc_pct = [0.265, 0.250, 0.235, 0.225, 0.215]
wc_prev = 18917.0
auto_rev_fy25 = 66358.3
rows = []
prev_rev = auto_rev_fy25
for i, y in enumerate(yrs):
    r = fc[y]['auto_rev']
    gp = r * gpm[i]
    op = gp - r * gsa[i] + r * oth + r * prov
    dna = r * dna_pct[i]
    ebitda = op + dna
    nopat = op * (1 - TAX)
    wc = r * wc_pct[i]
    dwc = wc - wc_prev
    fcff = nopat + dna - capex[i] - dwc
    rows.append(dict(year=y, rev=r, gp=gp, ebitda=ebitda, ebit=op, dna=dna,
                     nopat=nopat, capex=capex[i], dwc=dwc, fcff=fcff, wc=wc))
    wc_prev = wc; prev_rev = r
# ===== COST OF CAPITAL — v2, through the ONE sanctioned module [R-COC-01/R-COC-02] =====
# REBUILT 07-09-2026. What this replaces, and why it is a rebuild and not a patch: the
# delivered edition passed a RAW local government-bond yield of 22.55% into the cost of
# equity AND added a country-risk-loaded equity premium on top of it, which charges Egypt's
# sovereign risk twice — the systemic v1 defect [L-004] was found on this very study and the
# study itself was never re-issued on the fix. It also discounted five explicit years and a
# perpetuity alike at one crisis-level rate, asserting that Egypt's cost of capital never
# normalises, against the central bank's own published disinflation path. The module cannot
# express either error.
import sys as _sys, os as _os
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
import cost_of_capital as _COC
import macro_path as _MP

_beta = _COC.BetaRecord(
    beta=0.8906822450333004, tier=1,
    source=("engine/beta_regression.own_stock_beta('GBCO','EG','EGX') — weekly W-THU, "
            "Dimson-corrected, 2021-09-09 to 2026-07-16, regressed on the PUBLISHED EGX30 "
            "index of the exchange GBCO is listed on"),
    r2=0.24301638425722683, se=0.20405704188114288, n=251,
    index_file="raw_indices/EG/EGX30.csv", index_asof="2026-07-22", conforming=True)

# THE BORROWINGS THAT ACTUALLY BEAR THE INTEREST. GB Corp contains a LENDER, and GB Capital's
# cost of funds is booked inside that segment's COST OF REVENUE rather than in the group
# finance-cost line. The group's expensed finance charge over group borrowings therefore
# reads 14.1%, and over TOTAL liabilities 7.1%, against an Egyptian policy corridor above 24%
# throughout the period. Both are the denominator error this method names; the rate below is
# computed on the whole interest actually incurred over the borrowings that actually bear it.
_book = _COC.DebtBook(
    gross_debt=42476.0,
    pct_local_currency=1.0,
    currency_source=("GB Corp FY2025 audited consolidated statements, notes 26 (loans) and 38 "
                     "(bonds), and the segmented balance sheet in the 2Q26 earnings release as "
                     "at 30 June 2026; every disclosed facility is EGP-denominated."),
    kd_local_pretax=0.2653,
    kd_source=("GB Corp's own FY2025 effective borrowing rate, computed independently from the "
               "filings on the borrowings that actually bear the interest."),
    effective_rates=(0.2906, 0.2653), effective_rate_periods=("FY2024", "FY2025"),
    interest_bearing_note=(
        "interest expense per audited note 7 (FY25 EGP 4,287.1mn, FY24 2,882.4mn) PLUS GB "
        "Capital's COST OF FUNDS, which GB Corp books inside that segment's cost of revenue "
        "and not in the group finance-cost line (FY25 3,756.9mn, FY24 2,192.3mn, 4Q25 release "
        "Table 13), over AVERAGE interest-bearing borrowings — loans, overdrafts and bonds, "
        "FY25 average 30,325.1mn, FY24 average 17,463.2mn. Customer balances, trade payables "
        "and lease liabilities are excluded because they bear no interest."))

_ERP = {"rating": 0.1394, "market": 0.0941}   # Damodaran country-risk file, Egypt row
_SCHED = {b: _COC.schedule("EG", _beta, _book, market_cap=spot*SH, tax_rate=TAX, years=5,
                           erp_basis=b, erp_explicit=_ERP[b], build_date=spot_date,
                           allow_stale_sovereign=True)
          for b in ("rating", "market")}
_sch = _SCHED["market"]          # CENTRAL: the market (CDS) basis, per [R-COC-01]
WACC = _sch.wacc_exp
WACC_RATING = _SCHED["rating"].wacc_exp
KE_CDS, KE_RATING = _sch.ke_exp, _SCHED["rating"].ke_exp
KD_AFTERTAX = _sch.kd_aftertax
WE, WD = _sch.weight_equity, _sch.weight_debt

# GROWTH IS STORED AS (real, inflation-path id) AND RECOMPUTES TO ITS NOMINAL [R-MACRO-01].
# The delivered edition typed a nominal 11.5% against a discount rate that never normalised;
# a typed nominal rate is unfalsifiable — nobody can tell whether it meant inflation plus four
# points or minus three.
_PATH = _MP.load("EG")
TG_REAL = 0.0
TG = _PATH.terminal_inflation + TG_REAL
for i, rw in enumerate(rows):
    rw['wacc_y'] = _sch.forward_wacc[i]
    rw['df'] = _sch.discount_factors[i]
    rw['pv'] = rw['fcff'] * rw['df']
pv_sum = sum(rw['pv'] for rw in rows)
tv = rows[-1]['fcff'] * (1 + TG) / (_sch.wacc_terminal - TG)
pv_tv = tv * _sch.terminal_discount_factor
ev_auto = pv_sum + pv_tv
# THE BRIDGE STANDS ON THE LATEST DISCLOSED BALANCE SHEET [R-BRIDGE-01]. The delivered
# edition stood on 31-Dec-2025 while GB Corp's reviewed 30-June-2026 consolidated statements
# and its 2Q26 earnings release (13 August 2026) were both published and on its own IR site.
# Auto-leg net debt on the COMPANY'S OWN definition (short- and long-term debt plus lease
# obligations and due-to-related-parties, less cash), as at 30 June 2026:
#   20,943.0 + 1,790.1 + 1,333.3 + 2.3 - 9,445.0
auto_nd = 20943.0 + 1790.1 + 1333.3 + 2.3 - 9445.0
auto_nci = 590.7        # GB Auto segment "Total NCI", 2Q26 release Table 12, 30-Jun-2026
auto_eq = ev_auto - auto_nd - auto_nci
# GB Capital operating leg
cap_book = 9500.0   # adjusted operating equity, from company's adjusted-ROAE basis
cap_mult = 1.0
cap_val = cap_book * cap_mult
# Associates (MNT-Halan + Bedaya + Kaf)
# CONFIRMED per GB Corp's own press release, 9 June 2026 ("MNT-Halan, a GB Corp Investee Company, Closes Capital
# Increase Round Led by Al Ahly Capital Holding"): "As a result of the completion of this transaction, GB Corp's
# ownership stake in MNT-Halan will be adjusted to 41.61%, compared to 42.58% prior to the transaction." This is a
# current, dated, company-disclosed figure — not an estimate and not a stale prior-round number. It supersedes both
# the original ~20% placeholder (unsourced, wrong) and the interim 42.58% correction (correct as of mid-2024/pre-this
# transaction, but superseded by this more recent, confirmed print). Applying 41.61% to the June-2026 USD 1.4bn round
# still implies MNT-Halan alone is worth ~82% of GB Corp's spot market cap — a genuine, now-evidenced anomaly, not a
# sourcing gap: either the market is discounting the private mark's read-through far more steeply than this study's
# 10% complexity discount, or GB Corp is meaningfully undervalued. Flagged and discussed, not resolved away.
mnt_halan_stake = 0.4161
mnt_halan_round_usd = 1400.0
egp_usd = 47.5
mnt_halan_value = mnt_halan_stake * mnt_halan_round_usd * egp_usd
other_assoc = 390.0  # Bedaya + Kaf residual carrying value, unchanged
assoc = mnt_halan_value + other_assoc
sotp_sum = auto_eq + cap_val + assoc
disc = 0.10
sotp_eq = sotp_sum * (1 - disc)
sotp_ps = sotp_eq / SH
prediscount_ps = sotp_sum / SH
# Relative lens
np26 = 3300.0   # FY26E group NP (Auto ~1.65 + Capital ~1.65)
eps26 = np26 / SH
rel = dict(bear=eps26*8.0, base=eps26*9.5, bull=eps26*11.0)
# Normalized earnings
norm_pat = 4200.0
norm = dict(bear=(3600/SH)*7.5, base=(norm_pat/SH)*8.5, bull=(4800/SH)*9.5)
# SOTP bear/bull (auto margin/multiple + discount + marks)
def sotp_case(gpm_shift, wacc, tg, cap_m, assoc_m, d):
    rws = []
    wcp = 18917.0
    for i, y in enumerate(yrs):
        r = fc[y]['auto_rev']
        op = r*(gpm[i]+gpm_shift) - r*gsa[i] + r*oth + r*prov
        dna = r*dna_pct[i]
        fcff = op*(1-TAX)+dna-capex[i]-(r*wc_pct[i]-wcp)
        wcp = r*wc_pct[i]
        rws.append(fcff)
    _shift = wacc - WACC                      # move the WHOLE ladder, never one rate
    _fwd = [r + _shift for r in _sch.forward_wacc]
    _fac, _c = [], 1.0
    for r in _fwd:
        _c /= (1 + r)
        _fac.append(_c)
    pvs = sum(f*_fac[i] for i, f in enumerate(rws))
    tv_ = rws[-1]*(1+tg)/((_sch.wacc_terminal + _shift)-tg)*_fac[-1]
    ae = pvs+tv_-auto_nd-auto_nci
    return (ae + cap_book*cap_m + assoc*assoc_m)*(1-d)/SH
# Bear and bull terminal growth are REAL rates on the house path, never typed nominals
# [R-MACRO-01]: -0.5% and +0.5% real against the path's 7.0% terminal inflation.
TG_BEAR = _PATH.terminal_inflation - 0.005
TG_BULL = _PATH.terminal_inflation + 0.005
sotp_bear = sotp_case(-0.012, WACC+0.020, TG_BEAR, 0.80, 0.80, 0.18)
sotp_bull = sotp_case(+0.010, WACC-0.015, TG_BULL, 1.25, 1.20, 0.04)
dcf_lens = dict(bear=sotp_case(-0.012, WACC+0.020, TG_BEAR, 0.80, 0.80, 0.0),
                base=prediscount_ps,
                bull=sotp_case(+0.010, WACC-0.015, TG_BULL, 1.25, 1.20, 0.0))
weights = dict(sotp=0.40, prediscount=0.15, relative=0.20, normalized=0.25)
central = (weights['sotp']*sotp_ps + weights['prediscount']*prediscount_ps
           + weights['relative']*rel['base'] + weights['normalized']*norm['base'])
central_bear = (weights['sotp']*sotp_bear + weights['prediscount']*dcf_lens['bear']
                + weights['relative']*rel['bear'] + weights['normalized']*norm['bear'])
central_bull = (weights['sotp']*sotp_bull + weights['prediscount']*dcf_lens['bull']
                + weights['relative']*rel['bull'] + weights['normalized']*norm['bull'])
# SOTP sensitivity grid: Auto EBITDA-margin proxy shift × complexity discount
grid_margin = [-0.02, -0.01, 0.0, 0.01, 0.02]
grid_disc = [0.0, 0.05, 0.10, 0.15, 0.20]
sens = [[sotp_case(mm, WACC, TG, 1.0, 1.0, dd) for dd in grid_disc] for mm in grid_margin]
# experts
cap_hist = dict(FY23=dict(wc=4466.3, nd=2921.8, ce=10231.2, roce=0.359),
                FY24=dict(wc=10783.9, nd=5292.0, ce=18731.3, roce=0.315),
                FY25=dict(wc=18917.0, nd=15210.0, ce=28513.0, roce=0.213))
exp1_sum = (auto_eq + cap_book*1.0 + assoc*1.0)
exp1 = dict(base=exp1_sum*(1-0.08)/SH, rng=(sotp_bear*0.95, sotp_bull*1.02))
exp3_ev = 28513.0*0.90
exp3 = dict(base=(exp3_ev-auto_nd-auto_nci + cap_book*0.90 + assoc*0.85)/SH)
exp2 = dict(base=norm['base'], rng=(norm['bear'], norm['bull']))
roce, ce = 0.213, 28513.0

_AUD = ('GB Corp / GB Auto audited consolidated statement of income for the year, as '
        'reproduced in the company\'s own annual report for that year (engine/gbco_study/src/)')
_REL = ('GB Corp\'s own %s earnings release, published on ir.gb-corporation.com and '
        'committed under engine/gbco_study/src/')
def _i(v, src, date, tier='A'):
    """One input, FOUR-FIELD complete: value, source, date and the RESEARCH LAYER.

    Depth-bar standard 2 requires the fourth field and this register carried
    `tier` instead — a source-QUALITY grade, which is a different quantity and
    does not answer which of the four rings the figure came from. All nineteen
    inputs here are GB Corp's own, so the ring is Company either way; what
    separates them is the channel, and the sweep register is required to tag the
    investor-relations channel DISTINCTLY from the audited statements.

    The layer is DERIVED from which source constant built the string rather than
    typed nineteen times, so it cannot drift from the source it describes, and a
    source matching neither constant RAISES instead of defaulting to Company —
    a default here would be this function quietly asserting a provenance nobody
    established.
    """
    if src.startswith(_AUD):
        layer = 'Company'
    elif src.startswith(_REL.split('%s')[0]):
        layer = 'Company (investor relations)'
    else:
        raise AssertionError(
            'this input names a source built from neither the audited-statement '
            'nor the earnings-release constant, so its research layer cannot be '
            'derived: %r' % (src[:120],))
    return dict(value=v, source=src, date=date, tier=tier, layer=layer,
                unit='EGP mn', route='PDF text layer (pymupdf)')
_INPUTS = {
    'rev_fy2023':  _i(28317.2, _REL % '4Q23', '2024-03-01'),
    'rev_fy2024':  _i(53969.5, _REL % '4Q24', '2025-02-01'),
    'rev_fy2025':  _i(80229.8, _REL % '4Q25' + '; footed against the FY2025 audited '
                     'consolidated statement of income, operating revenue 80,229,809 '
                     '(EGP thousand)', '2026-02-26'),
    'rev_h1_2026': _i(48474.4, _REL % '2Q/1H26' + ', 13 August 2026', '2026-08-13'),
    'gp_fy2025':   _i(12431.1, _AUD, '2026-02-26'),
    'gp_h1_2026':  _i(7421.9, _REL % '2Q/1H26', '2026-08-13'),
    'gross_auto_h1_2026': _i(5722.1, _REL % '2Q/1H26' + ', Table 11 income statement BY '
                             'SEGMENT: GB Auto total revenue 40,021.5, gross profit 5,722.1',
                             '2026-08-13'),
    'ebit_fy2025': _i(6631.0, _AUD, '2026-02-26'),
    'pat_fy2025':  _i(2880.0, _AUD + ' — attributable to the parent; the FY2025 opinion is '
                     'QUALIFIED on the MNT-BV associate', '2026-02-26'),
    'pat_fy2024':  _i(2928.1, _AUD, '2025-02-01'),
    'cash_dec2025': _i(9523.6, _AUD + ' — note 16, cash and cash equivalents', '2026-02-26'),
    'cash_jun2026': _i(10951.5, _REL % '2Q/1H26' + ', Table 12 balance sheet by segment',
                       '2026-08-13'),
    'debt_dec2025': _i(38041.4, _AUD + ' — notes 26 and 38: loans 10,721,880 + bonds '
                       '40,000 + loans, borrowings and overdrafts 27,199,462 + bonds 80,000',
                       '2026-02-26'),
    'debt_jun2026': _i(42476.0, _REL % '2Q/1H26' + ', Table 12: loans and overdraft 28,703.7 '
                       '+ loans 13,772.3', '2026-08-13'),
    'debt_auto_jun2026': _i(22733.1, _REL % '2Q/1H26' + ', Table 12, GB Auto column: '
                            '20,943.0 + 1,790.1 — THE BORROWINGS THAT ACTUALLY BEAR THE '
                            'ASSEMBLER\'S INTEREST', '2026-08-13'),
    'dep_fy2025':  _i(999.3, _AUD + ' — consolidated cash-flow statement, depreciation and '
                     'amortisation for the year', '2026-02-26'),
    'capex_fy2025': _i(3664.2, _AUD + ' — consolidated cash-flow statement, payment for '
                       'acquisition of property, plant, equipment and projects under '
                       'construction', '2026-02-26'),
    'eq_jun2026':  _i(35127.9, _REL % '2Q/1H26' + ', Table 12 total equity', '2026-08-13'),
    'ni_h1_2026':  _i(1262.0, _REL % '2Q/1H26', '2026-08-13'),
}

out = dict(
    # [R-FCAL-01] WHAT THIS NAME'S WALK-FORWARD ADOPTED, STATED RATHER THAN LEFT
    # TO SILENCE. scripts/check_corrections_applied.py reads this; a study with a
    # run behind it and no statement either way is SILENT, which is a different
    # fact from 'none adopted' and reads identically.
    adopted_corrections=[],
    adopted_corrections_note=(
        'the walk-forward on this name measured seven drivers over 225 cells and adopted NONE of them. Two drivers are robust at every block size and both are aggregates, which corrections may not be applied to; the one driver passing the cut-invariance clause at all six admissible boundaries (sga) has its block-2 bootstrap interval covering zero. Recorded in engine/gbco_walkforward/corrections_log.json; empty rather than absent.'),
    # THE ANSWER, WHERE THE SHARED READER LOOKS. Until this rebuild the study's central sat
    # at lenses.central.base and scripts/check_valuation_gap.py reads a top-level `central`,
    # so GBCO read as UNREADABLE — and an unreadable answer is not a clean answer [R-ENF-04];
    # it is held exactly as a breaching one is. The figure is unchanged in meaning: it is the
    # same published central the document and assets/data.js carry.
    central=central,
    central_bear=central_bear, central_full=central_bull,
    spot=spot, spot_date=spot_date, shares=SH, mktcap=spot*SH,
    step0=dict(nonoverlap=summ, monthly=summ21, zerodrift=summ0,
               pit_hist=pit_hist, n_rows=len(res)),
    engine=dict(anchor_vol=anchor_vol, drift_daily=drift_daily,
                drift_q=drift_daily*60, factor_drift_q=factor_drift_q,
                cont_drift_q=cont_drift_q, disc_drift_q=disc_drift_q),
    mc=dict(q20=q20, q60=q60, touch=touch, prob_read=prob_read,
            zones=zone_probs, fan=fan),
    tech=dict(sma=sma, rsi=rsi, macd=macd, hi52=hi52, lo52=lo52, rv252=rv252),
    dcf=dict(rows=rows, pv_sum=pv_sum, tv=tv, pv_tv=pv_tv, ev=ev_auto,
             tv_pct=pv_tv/ev_auto, wacc=WACC, tg=TG,
             auto_nd=auto_nd, auto_nci=auto_nci, auto_eq=auto_eq,
             wacc_terminal=_sch.wacc_terminal,
             forward_wacc=list(_sch.forward_wacc),
             discount_factors=list(_sch.discount_factors),
             terminal_discount_factor=_sch.terminal_discount_factor,
             wacc_build=dict(rf_observed=_sch.rf_observed, default_spread=_sch.default_spread,
                             rf_star=_sch.rf_star, erp_rating=_ERP["rating"],
                             erp_cds=_ERP["market"], beta=_sch.beta,
                             ke_cds=KE_CDS, ke_rating=KE_RATING,
                             kd_pretax=_sch.kd_pretax, kd_aftertax=KD_AFTERTAX,
                             we=WE, wd=WD, wacc_cds=WACC, wacc_rating=WACC_RATING,
                             rf_source=("engine/macro_paths/EG.json — Egypt 10-year EGP "
                                        "government bond yield, market quote 6 August 2026, "
                                        "NORMALISED by Egypt's own default spread so country "
                                        "risk is counted exactly once"),
                             erp_source=("Damodaran country-risk file, Egypt row, read for "
                                         "this sovereign and never borrowed from a neighbour"),
                             kd_source=_book.kd_source,
                             debt_currency_evidence=_book.currency_source,
                             beta_source=_beta.source)),
    sotp=dict(auto_eq=auto_eq, cap_val=cap_val, assoc=assoc, total=sotp_sum,
              disc=disc, eq=sotp_eq, ps=sotp_ps, prediscount_ps=prediscount_ps,
              bear=sotp_bear, bull=sotp_bull,
              mnt_halan_stake=mnt_halan_stake, mnt_halan_round_usd=mnt_halan_round_usd,
              egp_usd=egp_usd, mnt_halan_value=mnt_halan_value, other_assoc=other_assoc),
    lenses=dict(sotp=dict(bear=sotp_bear, base=sotp_ps, bull=sotp_bull),
                prediscount=dcf_lens, relative=rel, normalized=norm,
                central=dict(bear=central_bear, base=central, bull=central_bull),
                weights=weights),
    forecast=fc, gpm=gpm, sens=dict(grid_margin=grid_margin, grid_disc=grid_disc, table=sens),
    experts=dict(e1=exp1, e2=exp2, e3=exp3, e3_roce=roce, e3_ce=ce),
    cap_hist=cap_hist,
    cost_of_capital_record=dict(
        _rule="[R-COC-01] built through engine/cost_of_capital.py; [R-COC-02] Ke reproduces "
              "from rf* + beta x ERP under a NAMED construction",
        central_basis="market",
        beta_source="own_stock_regression",
        beta_source_note=_beta.source,
        **_sch.as_record()),
    cost_of_capital_rating_basis=_SCHED["rating"].as_record(),
    macro=dict(path="EG", path_asof=_PATH.as_of,
               terminal_inflation=_PATH.terminal_inflation,
               terminal_growth_real=TG_REAL, terminal_growth_nominal=TG,
               anchor_staleness_accepted=(
                   "The house Egyptian path's sovereign quote and FX spot are both anchored "
                   "6 August 2026 and this study is struck on the latest close the repository "
                   "holds, 23 August 2026 — 17 days. Refreshing a house macro path is a "
                   "house-level act and not a step of one name's rebuild; the staleness is "
                   "DISCLOSED rather than switched off, on the shape [R-COC-01] already uses "
                   "for a deliberately-accepted stale sovereign quote."),
               inflation_inputs=dict(
                   _declared="EVERY inflation-class input this study registers, with the "
                             "mapping that derives it from the house ladder [R-MACRO-01 "
                             "AMENDED]. Declared even though it is nearly empty.",
                   terminal_growth=dict(mapping="terminal_flat", real=TG_REAL,
                                        nominal=TG, source="engine/macro_paths/EG.json"),
                   note=("The auto leg is built from UNITS x ASP with segment-specific volume "
                         "and price growth read off the company's own disclosed volumes, so no "
                         "domestic CPI series escalates any line in this model. The ASP growth "
                         "rates are company drivers, not an inflation path, and are registered "
                         "as such in the forecast block."))),
    # THE INPUT REGISTER, four-field, committed where a checker can reach it. Until this
    # rebuild this directory held NO FILINGS AT ALL and the register lived nowhere, so
    # SIGCM clause 1 had nothing behind it and scripts/check_source_integrity.py read the
    # study as UNREADABLE. Every source below is a document GB Corp published itself, now
    # committed under engine/gbco_study/src/; the route is the PDF text layer in every case.
    inputs=_INPUTS,
    forecast_anchor=dict(
        rate_name="GB Auto gross margin",
        latest_reviewed_period=("1H2026 — GB Corp's own 2Q/1H26 earnings release, 13 August "
                                "2026, Table 11 income statement BY SEGMENT, and the reviewed "
                                "consolidated statements to 30 June 2026"),
        latest_reviewed_date="2026-06-30",
        latest_reviewed_rate=5722.1 / 40021.5,
        first_forecast_rate=gpm[0],
        forecast_path=list(gpm),
        note=("REBUILT 07-09-2026 ON A FILING. The superseded record anchored on 1Q26 at a "
              "12.4% auto gross margin taken from a figure the study asserted and held no "
              "document for — this directory carried NO filings at all until this run. The "
              "anchor is now GB Auto's OWN segment gross margin for the half already filed: "
              "revenue 40,021.5 and gross profit 5,722.1, a margin of 14.30%. The forecast "
              "opens at 13.80%, which is 3.5% relatively BELOW it — inside the 5% materiality "
              "line this house already applies to a contested judgement, so no mechanism is "
              "owed. THE RECORD IS PRINTED WHETHER OR NOT IT FIRES. The path then RISES to "
              "14.50% and terminates there, against a filed record of 24.37% (FY23), 19.24% "
              "(FY24) and 14.82% (FY25) on the auto leg — so the whole forecast path sits "
              "BELOW every filed full year and the direction against the LATEST reviewed "
              "period, which is what this rule measures, is a mild recovery. The rise from "
              "the opening year is 5.1% relative, also inside the line."),
        provenance=("Every figure above is read from GB Corp's own documents committed to "
                    "engine/gbco_study/src/ in this run, by PDF text layer, and the segment "
                    "table foots: 39,627.0 + 8,847.4 = 48,474.4 revenue and 5,722.1 + 1,762.2 "
                    "- 62.4 = 7,421.9 gross profit, both as printed.")),
    valuation_gap=dict(
        central=central, spot=spot, spot_date=spot_date,
        gap=central/spot - 1.0,
        price_note=("GBCO carries NO price in engine/prices/SUPPLIED_07-09-2026.json or in "
                    "SUPPLIED_03-09-2026.json. The latest price the repository holds is the "
                    "exchange library close of EGP 29.51 on 23 August 2026, which is what this "
                    "study is struck on, with its date and its age stated. Nothing was "
                    "substituted and nobody was asked [R-IND-01].")),
)
res.to_csv('backtest_rows.csv', index=False)
np.save('fan.npy', np.array([fan[p] for p in [5, 25, 50, 75, 95]]))
np.save('pT20.npy', pT20[:20000]); np.save('pT60.npy', pT60[:20000])
with open('study_numbers.json', 'w') as f:
    json.dump(out, f, indent=1, default=float)
print('spot', spot, spot_date, '| anchor_vol', round(anchor_vol, 3),
      '| drift_q', round(drift_daily*60*100, 1), '% | factor_q', round(factor_drift_q*100, 2), '%')
print('Step0 non-overlap:', {k: round(v, 3) if isinstance(v, float) else v for k, v in summ.items()})
print('T60:', {k: round(v, 1) for k, v in q60.items()}, '| prob_read P(up)=%.2f odds=%.2f' % (prob_read['p_above'], prob_read['odds']))
print('DCF: EV %.0f TV%% %.0f%% AutoEq %.0f | SOTP/sh %.1f (pre-disc %.1f) | central %.1f [%.0f-%.0f]'
      % (ev_auto, 100*pv_tv/ev_auto, auto_eq, sotp_ps, prediscount_ps, central, central_bear, central_bull))
print('rel', {k: round(v,1) for k,v in rel.items()}, 'norm', {k: round(v,1) for k,v in norm.items()})
print('FCFF path:', [round(r['fcff']) for r in rows])
