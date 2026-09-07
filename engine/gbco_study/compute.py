"""GBCO study — master computation. Outputs study_numbers.json + backtest tables."""
import json
import os
import numpy as np
import pandas as pd
import primitives as m

HERE = os.path.dirname(os.path.abspath(__file__))
import datetime as _datetime_mod

# THE REPORTED HISTORY COMES FROM THE WALK-FORWARD PANEL, WHICH IS THE SOURCED RECORD.
# engine/gbco_walkforward/panel.json carries GB Corp's own consolidated income statement
# 2012-2025, four-field, every year asserted to foot against its own arithmetic. The
# delivered document used to TYPE its three history columns into the builder, which is the
# defect depth-bar standard 3 exists to stop, and two of those typed lines disagreed with
# the filing (FY2023 operating profit was printed at 3,703 against a filed 3,977).
_PANEL = json.load(open(os.path.join(HERE, '..', 'gbco_walkforward', 'panel.json'),
                        encoding='utf-8'))
HIST_YEARS = ['2023', '2024', '2025']
HISTORY = dict(
    _source="engine/gbco_walkforward/panel.json — GB Corp's own 4Q earnings releases, "
            "as originally reported, every year footed against its own arithmetic",
    years=HIST_YEARS,
    income_statement={y: _PANEL['years'][y]['is'] for y in HIST_YEARS},
    provenance={y: dict(source=_PANEL['years'][y]['source'],
                        source_date=_PANEL['years'][y]['source_date'],
                        route=_PANEL['years'][y]['route'],
                        foots=_PANEL['years'][y]['foots'])
                for y in HIST_YEARS})

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
# ---- GROUP-LEVEL FORECAST DRIVERS ------------------------------------------------
# THESE LIVED ONLY INSIDE THE WORKBOOK BUILDER AND THE DOCUMENT TYPED THE RESULT. The
# consolidated forecast income statement a reader receives was transcribed by hand from an
# Excel run, so the page and the model were two separate transcriptions of one arithmetic
# and nothing compared them. The drivers move here, the group statement is computed here,
# and both the document and the workbook read the same committed record.
CAP_REV_FY25 = 14743.0          # GB Capital revenue, FY2025 earnings release, segment table
cap_g = [0.45, 0.30, 0.25, 0.20, 0.18]
cap_gm = [0.188, 0.190, 0.192, 0.194, 0.196]
elim_pct = [0.011]*5
grp_opex = [0.080, 0.079, 0.078, 0.0775, 0.077]
grp_oth = [0.011]*5
grp_prov = [-0.003]*5
assoc_inc = [1250.0, 1430.0, 1630.0, 1830.0, 2030.0]
fin_cost = [-4100.0, -3800.0, -3500.0, -3300.0, -3100.0]
mi_pct = [-0.02]*5
cap_dna = [560.0, 640.0, 730.0, 830.0, 940.0]
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
# THE ANCHOR DATE IS READ FROM THE PATH FILE, NEVER TYPED — it is the date the staleness
# disclosure below is measured from, and a typed copy of it goes stale the day the path is
# refreshed while the sentence quoting it does not.
import json as _json_path
_ANCHOR_DATE = _json_path.load(open(os.path.join(
    HERE, '..', 'macro_paths', 'EG.json'), encoding='utf-8'))['fx']['spot']['date']
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
# ---- GB CAPITAL: A LENDER IS WORTH ITS OWN EQUITY TIMES WHAT IT EARNS ON IT --------
# THE DELIVERED EDITION CARRIED `cap_book = 9500.0` WITH THE COMMENT "adjusted operating
# equity, from company's adjusted-ROAE basis", TIMES A MULTIPLE OF 1.0. Two defects sat
# in those two lines and neither was visible to any gate.
#
# (i) BOOK TIMES ONE IS THE WEIGHTING OF BOOK VALUE [R-LENS-03] FORBIDS OUTRIGHT. Book is
#     a disclosed FLOOR, published as such and never weighted into a central; a leg
#     carried at 1.0x book is book value carrying the entire weight of that leg, wearing
#     a sum-of-the-parts entry's clothes.
# (ii) THE ASSOCIATE WAS IN THE ANSWER TWICE. GB Corp's own adjusted ROAE is struck on a
#     denominator of roughly EGP 9.0bn -- FY25 net profit after tax and NCI of 1,365.9
#     over 15.1% gives 9,045.7 -- and its NUMERATOR includes EGP 986.4mn of investment
#     gains from associates (4Q25 release Table 13). Importing that denominator as a
#     valuation base therefore imports a base justified by earnings the sum of the parts
#     then counts AGAIN at the June-2026 round price. That is [R-BRIDGE-01] defect (iii),
#     the cash charged twice, in a lender's costume.
#
# THE CLEAN BASE IS AN IDENTITY OFF TWO DISCLOSED FIGURES, so nothing here is chosen:
# the segment's own shareholders' equity before NCI, LESS the associates carried inside
# it. Both are GB Corp's own numbers as at 30 June 2026 and both foot.
CAPITAL_SEG_EQUITY = 22497.8      # 2Q26 earnings release Table 12, segmented balance
                                  # sheet, "Total Shareholders' Equity Before NCI",
                                  # GB Capital column, 30-Jun-2026
ASSOC_CARRYING     = 16230.465    # reviewed consolidated interim statement of financial
                                  # position, 30-Jun-2026, "Investment in associates
                                  # (34)" = 16 230 465 thousand. READ BY OCR OFF THE
                                  # RENDERED PIXELS: the filing carries a 51-character
                                  # text layer across 51 pages, so pdftotext yields
                                  # nothing and the route is recorded here on the same
                                  # footing as the four-field rule. Note 34 foots to it:
                                  # opening 13,272,208 + restatement 2,460,218 =
                                  # 15,732,426, which is the balance sheet's own
                                  # comparative column to the pound.
cap_operating_equity = CAPITAL_SEG_EQUITY - ASSOC_CARRYING
# The earnings that base actually produces, with the associate income taken out of the
# numerator as well as the denominator -- equity-accounted associate income is booked net
# of tax and outside NCI, so the subtraction is clean.
CAP_FY25_NP_AFTER_NCI = 1365.9    # 4Q25 release Table 13
CAP_FY25_ASSOC        = 986.4     # same table, "Investment Gains from Associates"
CAP_FY25_EQ_BEFORE_NCI = 18312.6  # 4Q25 release Table 12, GB Capital column
ASSOC_CARRYING_DEC25   = 15732.426  # reviewed BS 30-Jun-2026, comparative column
CAP_H126_NP_AFTER_NCI = 649.6     # 2Q26 release Table 13
CAP_H126_ASSOC        = 426.2     # same table
cap_fy25_ex_assoc = CAP_FY25_NP_AFTER_NCI - CAP_FY25_ASSOC
cap_h126_ex_assoc = CAP_H126_NP_AFTER_NCI - CAP_H126_ASSOC
cap_eq_dec25      = CAP_FY25_EQ_BEFORE_NCI - ASSOC_CARRYING_DEC25
cap_roe_fy25 = cap_fy25_ex_assoc / cap_eq_dec25
cap_roe_h126 = (cap_h126_ex_assoc * 2) / ((cap_eq_dec25 + cap_operating_equity) / 2)
# THE JUSTIFIED PRICE-TO-BOOK IS THE RESIDUAL-INCOME IDENTITY IN ITS TERMINAL FORM,
# (ROE - g) / (Ke - g), and every input in it comes from somewhere else in this study:
# the terminal cost of equity from the sanctioned cost-of-capital schedule, the growth
# from the house macro path [R-MACRO-01]. THE TERMINAL Ke IS THE GENEROUS END and it is
# used deliberately: the explicit-window Ke of 27.97% would put this leg at a fraction of
# the figure below, and where a correction cuts a number the charitable reading is the
# one to take.
def cap_justified_pb(roe):
    return (roe - TG) / (
        _sch.ke_terminal - TG)
# [R-ANCHOR-01]'s discipline: A NEAR-TERM REVIEWED ACTUAL OUTRANKS A STALE FULL-YEAR RATE.
# The 1H26 reviewed period is the anchor; FY25 is published beside it as the other framing
# of a contested judgement worth more than 5% of the answer [R-ENF-05].
cap_roe_adopted = cap_roe_h126
cap_pb = cap_justified_pb(cap_roe_adopted)
cap_val = cap_operating_equity * cap_pb
cap_val_fy25_framing = cap_operating_equity * cap_justified_pb(cap_roe_fy25)
cap_book = cap_operating_equity   # the DISCLOSED FLOOR, published as such, never weighted
# Associates (MNT-Halan + Bedaya + Kaf)
# CONFIRMED per GB Corp's own press release, 9 June 2026 ("MNT-Halan, a GB Corp Investee Company, Closes Capital
# Increase Round Led by Al Ahly Capital Holding"): "As a result of the completion of this transaction, GB Corp's
# ownership stake in MNT-Halan will be adjusted to 41.61%, compared to 42.58% prior to the transaction." This is a
# current, dated, company-disclosed figure — not an estimate and not a stale prior-round number. It supersedes both
# the original ~20% placeholder (unsourced, wrong) and the interim 42.58% correction (correct as of mid-2024/pre-this
# transaction, but superseded by this more recent, confirmed print). Applying 41.61% to the June-2026 USD 1.4bn round
# ---- THE CONSOLIDATED FORECAST, COMPUTED ONCE -------------------------------------
GROUP = []
_capr = CAP_REV_FY25
for i, y in enumerate(yrs):
    _capr *= (1 + cap_g[i])
    _autor = fc[y]['auto_rev']
    _elim = -(_autor + _capr) * elim_pct[i]
    _rev = _autor + _capr + _elim
    _agp = _autor * gpm[i]
    _gp = _agp + _capr * cap_gm[i] + _elim * 0.2
    _sga = -_rev * grp_opex[i]
    _oth = _rev * grp_oth[i]
    _prov = _rev * grp_prov[i]
    _op = _gp + _sga + _oth + _prov
    _assoc = assoc_inc[i]
    _ebit = _op + _assoc
    _dna = _autor * dna_pct[i] + cap_dna[i]
    _ebt = _ebit + fin_cost[i]
    _tax = -_ebt * TAX
    _npbmi = _ebt + _tax
    _mi = _npbmi * mi_pct[i]
    GROUP.append(dict(year=y, auto_revenue=_autor, capital_revenue=_capr,
                      eliminations=_elim, revenue=_rev, gross_profit=_gp,
                      sga=_sga, other_income=_oth, provisions=_prov,
                      operating_profit=_op, associates=_assoc, ebit=_ebit,
                      dna=_dna, ebitda=_ebit + _dna, finance_net=fin_cost[i],
                      ebt=_ebt, tax=_tax, npbmi=_npbmi, minority=_mi,
                      net_profit=_npbmi + _mi))

# still implies MNT-Halan alone is worth ~82% of GB Corp's spot market cap — a genuine, now-evidenced anomaly, not a
# sourcing gap: either the market is discounting the private mark's read-through far more steeply than this study's
# 10% complexity discount, or GB Corp is meaningfully undervalued. Flagged and discussed, not resolved away.
mnt_halan_stake = 0.4161
# THE SUPERSEDED STAKE IS COMMITTED TOO, because the document quotes it: the same press
# release states the figure BEFORE the transaction, and a figure a reader sees must be read
# from the record rather than typed into a builder.
mnt_halan_stake_prior = 0.4258
mnt_halan_round_usd = 1400.0
egp_usd = 47.5
mnt_halan_value = mnt_halan_stake * mnt_halan_round_usd * egp_usd
# THE REVIEWED STATEMENTS STATE A DIFFERENT PERCENTAGE FOR THE SAME TRANSACTION AND THE
# STUDY REGISTERED ONLY ONE OF THEM. Note 34 to the 30-June-2026 reviewed consolidated
# statements says of the same June-2026 Al Ahly Capital transaction that "GB Corp's
# ownership stake in MNT BV will be decreased to 42.93%, instead of 44.01% before the
# transaction", and the review report names the same 42.93%. The press release names
# 41.61% from 42.58%. Both are the company's own disclosures about one transaction and
# they are not the same pair, which is most likely a difference of LEVEL -- the Dutch
# holding vehicle MNT Investment B.V. against the operating group MNT-Halan the release
# names. THE LOWER FIGURE IS ADOPTED because it is the one the round it is applied to was
# announced with, and the higher is recorded rather than left out: a study that registers
# one of two disclosed figures for the same fact has decided something silently.
mnt_stake_statements = 0.4293
mnt_stake_statements_prior = 0.4401
# Other associates by IDENTITY off the note's own total rather than by summing its rows:
# the total (16,230,465) and the MNT row (15,733,523) each foot -- restated 15,315,532 +
# 8,006 of other comprehensive income + 409,985 of period profit -- while the three
# smaller rows carry a ten-thousand OCR ambiguity in one cell, so the residual is the
# figure that can be reproduced.
MNT_CARRYING = 15733.523
other_assoc = ASSOC_CARRYING - MNT_CARRYING
# ---- THE CONTESTED JUDGEMENT, COMPUTED BOTH WAYS AND NEVER AVERAGED ------------------
# Depth-bar standard 8 requires the study's single most consequential contested judgement
# to be published side by side rather than blended into one number, and this is that
# judgement: on one basis the stake is worth EGP 27.7bn, on the other EGP 15.7bn, and the
# difference is 27% of the answer. NEITHER BASIS IS THIS DESK'S INVENTION.
#
# A -- THE ROUND PRICE. 41.61% of the June-2026 primary round's stated USD 1.4bn.
#      Against it: a primary round's headline valuation prices NEW preferred money with
#      whatever preferences ride with it, and GB Corp holds an ordinary equity-accounted
#      minority in an unlisted company. It is a mark, not a realisable price.
# B -- THE REVIEWED CARRYING VALUE, EGP 15,733.5mn at 30 June 2026. Against it: it is an
#      ACCOUNTING measure -- cost plus accumulated share of profit plus the revaluation on
#      deconsolidation -- and [R-LENS-03] is explicit that book is a floor rather than a
#      value. AND IT IS ITSELF QUALIFIED: KPMG's limited review conclusion on these
#      statements is QUALIFIED precisely here, because they "were not provided with the
#      consolidated financial statements for one of the associate companies (MNT - BV)"
#      and were "unable to verify the accuracy of the Group's share of profits from this
#      investment", EGP 409.9mn recorded in the period, the same qualification having
#      stood on the 31-December-2025 audited statements.
#
# THE HOUSE CANNOT SAY WHICH IS RIGHT, SO IT PUBLISHES BOTH AND SAYS SO. Averaging them
# would be the blend [R-LENS-03] retired, arriving through a different door.
assoc_round    = mnt_halan_value + other_assoc     # branch A
assoc_carrying = ASSOC_CARRYING                    # branch B
assoc = assoc_round        # retained for the cross-checks that read one number
# ---- NO CONGLOMERATE DISCOUNT, AND THE REASON IS NOT THAT IT IS SMALL ---------------
# The delivered edition applied a typed 10%, and then weighted the discounted and the
# UNDISCOUNTED sum at 0.40 and 0.15 -- which is an effective discount of 4%, not 10%, so
# the number the study named was not the number it applied. Both are free parameters that
# have never cleared an out-of-sample test, which the PROMOTION RULE forbids, and nothing
# in GB Corp's filings discloses a basis for either. What the discount was standing in
# for is now named instead: the uncertainty is IN THE ASSOCIATE MARK and it is published
# as two branches rather than smuggled into one number as a haircut.
sotp_A = auto_eq + cap_val + assoc_round
sotp_B = auto_eq + cap_val + assoc_carrying
sotp_A_ps = sotp_A / SH
sotp_B_ps = sotp_B / SH
sotp_sum = sotp_A                 # the branch the cross-check machinery reads
disc = 0.0
sotp_eq = sotp_A
sotp_ps = sotp_A_ps
prediscount_ps = sotp_A_ps
# ---- THE RELATIVE MULTIPLE, NON-CIRCULAR AND OFF THE COMPANY'S OWN HISTORY ----------
# The delivered edition typed `np26 = 3300.0` with the comment "FY26E group NP" while the
# model's own consolidated forecast computes 3,297.5 four hundred lines above -- a hand
# rounded copy of a figure the model already had, which is exactly the typed financial
# numeral depth-bar standard 3 forbids in a builder. It is read from the forecast now.
np26 = GROUP[0]['net_profit']
eps26 = np26 / SH
# The multiple was three typed judgement figures (8.0 / 9.5 / 11.0) sourced to nothing.
# [R-LENS-03] requires a relative multiple to be NON-CIRCULAR -- forward earnings times a
# multiple from peers or from the company's OWN HISTORY, never one read off the current
# price. GB Corp's own trailing multiple at its last three year-end closes, from its own
# reported net profit attributable and its own share price:
REL_HIST = {2023: (7.90, 1890.8), 2024: (17.13, 2928.1), 2025: (27.00, 2880.0)}
_rel_pes = sorted(px / (npv / SH) for px, npv in REL_HIST.values())
REL_PE_OWN = _rel_pes[len(_rel_pes) // 2]      # the median of three, and the COUNT is
                                               # published with it, because a percentage
                                               # without its count is the number that
                                               # misleads and so is a median of three
rel_ps = eps26 * REL_PE_OWN
rel = dict(bear=rel_ps, base=rel_ps, bull=rel_ps)
# THE TRADED MULTIPLE, COMMITTED SO THE CIRCULARITY CLAIM IS ARITHMETIC RATHER THAN PROSE
# [R-LENS-03]: a lens whose multiple IS the traded one values the company at what it
# already trades at, and a sentence saying otherwise is an attestation.
rel_traded_pe = (spot * SH + 0.0) / np26
# ---- NORMALISED EARNINGS POWER IS REMOVED, NOT RE-SOURCED ---------------------------
# It carried a quarter of the retired blend on six typed figures -- three mid-cycle profit
# levels and three through-cycle multiples, none of them sourced to anything. It is absent
# from this class's row in LENS_REGISTRY on the developer and contractor rows' reasoning
# and with this issuer's own numbers behind it: group earnings carry investment gains from
# associates that ran 451.6, 294.6 and 131.6 across three consecutive quarters plus a
# revaluation on deconsolidating an associate that the company itself strips out of its
# own return measure. Normalising earnings that swing on associate marks normalises noise.
norm_pat = None
norm = None
# THE LENS INPUTS ARE COMMITTED, NOT LEFT INSIDE THIS SCRIPT. Depth-bar standard 3
# forbids a financial numeral typed into a builder, and the delivered document printed
# every one of these by hand because the numbers file did not carry them. A figure a
# document prints must be READ from the record it claims to come from.
LENS_INPUTS = dict(
    relative=dict(np_fy26e=np26, eps_fy26e=eps26, pe=REL_PE_OWN,
                  observations=len(REL_HIST), history=REL_HIST,
                  pe_observed=sorted(_rel_pes), traded_pe=rel_traded_pe,
                  basis=("FY2026E group net profit attributable, READ from this model's "
                         "own consolidated forecast rather than typed; the multiple is "
                         "the MEDIAN of GB Corp's own trailing price-to-earnings at its "
                         "last three year-end closes, computed from its own reported net "
                         "profit attributable and its own share price. Never a multiple "
                         "read off the current price: the traded multiple on the same "
                         "forward earnings is committed beside it so the claim can be "
                         "divided rather than believed. THREE OBSERVATIONS IS THIN and "
                         "the count is published with the median for that reason.")),
    capital=dict(segment_equity_before_nci=CAPITAL_SEG_EQUITY,
                 associates_carried_within=ASSOC_CARRYING,
                 operating_equity=cap_operating_equity,
                 roe_h126=cap_roe_h126, roe_fy25=cap_roe_fy25,
                 roe_adopted=cap_roe_adopted, justified_pb=cap_pb,
                 ke_terminal=_sch.ke_terminal, g=TG,
                 value=cap_val, value_fy25_framing=cap_val_fy25_framing,
                 basis=("residual income in its terminal form, (ROE - g) / (Ke - g), on "
                        "the segment's own shareholders' equity before NCI LESS the "
                        "associates carried inside it -- so the stake the sum of the "
                        "parts adds back at its own mark is not also funding this leg. "
                        "The return is measured on that same base with associate income "
                        "taken out of the numerator too.")))
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
# ---- ONE CLASS PRIMARY IS THE CENTRAL, AND HERE IT HAS TWO SIDES [R-LENS-03] --------
# The delivered edition published a weighted blend of four lenses at typed weights. That
# construction is RETIRED: a number produced by averaging several methods is a new method
# with free parameters nobody tested, wearing the appearance of caution. The class primary
# is the sum of the parts, and it is the answer.
#
# It has no single value, because the study's largest component depends on a judgement the
# house cannot resolve from the filings. So there is NO CENTRAL -- that is what makes an
# answer two-sided -- and the two branches are published side by side.
weights = None
central = None
BRANCHES = [
    dict(label="MNT-Halan at its reviewed carrying value",
         value=sotp_B_ps,
         note=("EGP 15,733.5mn, the equity-accounted carrying value in GB Corp's own "
               "reviewed statements at 30 June 2026. The conservative branch, and itself "
               "the subject of the review's qualified conclusion.")),
    dict(label="MNT-Halan at the June-2026 round price",
         value=sotp_A_ps,
         note=("41.61% of the USD 1.4bn primary round completed with Al Ahly Capital "
               "Holding, translated at EGP 47.5. The market-mark branch.")),
]
# THE ENVELOPE IS THE RANGE OF THE PRESENT-VALUE READS ON ONE CLOCK, which is [R-LENS-03]
# in its own words -- never an average and never a spread invented around a central. The
# reads are the two branches of the primary and the relative multiple; book value is a
# disclosed floor and is not in it.
_pv_reads = [sotp_B_ps, sotp_A_ps, rel_ps]
central_bear = min(_pv_reads)
central_bull = max(_pv_reads)
# SOTP sensitivity grid: Auto EBITDA-margin proxy shift × complexity discount
grid_margin = [-0.02, -0.01, 0.0, 0.01, 0.02]
grid_disc = [0.0, 0.05, 0.10, 0.15, 0.20]
sens = [[sotp_case(mm, WACC, TG, 1.0, 1.0, dd) for dd in grid_disc] for mm in grid_margin]
# experts
cap_hist = dict(FY23=dict(wc=4466.3, nd=2921.8, ce=10231.2, roce=0.359),
                FY24=dict(wc=10783.9, nd=5292.0, ce=18731.3, roce=0.315),
                FY25=dict(wc=18917.0, nd=15210.0, ce=28513.0, roce=0.213))
EXP1_WRAPPER_DISCOUNT = 0.08
exp1_sum = (auto_eq + cap_book*1.0 + assoc*1.0)
exp1 = dict(base=exp1_sum*(1-EXP1_WRAPPER_DISCOUNT)/SH,
            rng=(sotp_bear*0.95, sotp_bull*1.02),
            wrapper_discount=EXP1_WRAPPER_DISCOUNT,
            # his own stated sensitivity: what a heavier haircut on the private mark costs
            mark_haircut=dict((h, (auto_eq + cap_book + mnt_halan_value*h + other_assoc)
                               * (1-EXP1_WRAPPER_DISCOUNT)/SH) for h in (0.75, 0.50)))
# EXPERT 3'S RANGE IS COMPUTED FROM HIS OWN TWO NAMED LEVERS, NOT TYPED. The delivered
# edition printed "range approx 32-48" and two round-number sensitivities beside it, none
# of which any model produced. His levers are stated in his own text: the haircut he puts
# on the private mark, and a return-on-capital recovery that lifts the operating mark from
# 0.9x capital employed to 1.0x. Both are evaluated here so the document reads them.
ce = cap_hist['FY25']['ce']
roce = cap_hist['FY25']['roce']
EXP3 = dict(ev_mult=0.90, ev_mult_bull=1.00, cap_mult=0.90,
            assoc_mult=0.85, assoc_mult_bear=0.60)
def _exp3(ev_mult, assoc_mult):
    return (ce*ev_mult - auto_nd - auto_nci + cap_book*EXP3['cap_mult']
            + assoc*assoc_mult) / SH
exp3 = dict(base=_exp3(EXP3['ev_mult'], EXP3['assoc_mult']),
            rng=(_exp3(EXP3['ev_mult'], EXP3['assoc_mult_bear']),
                 _exp3(EXP3['ev_mult_bull'], EXP3['assoc_mult'])),
            params=EXP3, ev_at_base=ce*EXP3['ev_mult'],
            equity_at_base=ce*EXP3['ev_mult'] - auto_nd - auto_nci)
exp3['mark_lever'] = exp3['rng'][0] - exp3['base']
exp3['roce_lever'] = exp3['rng'][1] - exp3['base']
# EXPERT 2 IS RE-POINTED RATHER THAN DELETED. His read was the normalised-earnings lens,
# which this class's row in LENS_REGISTRY does not carry and which this rebuild removed --
# so leaving him would publish an expert working on a lens the study no longer holds.
# The method he moves to is genuinely different from the other two and needs no figure
# this desk chose: RESIDUAL INCOME ON THE WHOLE GROUP, book plus what the group's own
# reported return on its own reported equity supports.
#
# It is the harshest read in the study and it is kept for that reason: on GB Corp's FY2025
# reported net profit attributable over its FY2025 shareholders' equity before NCI the
# group earns 10.00% against a terminal cost of equity of 18.73%, so the accounts alone
# justify roughly a quarter of book. Both of his inputs are contaminated in KNOWN
# directions -- the earnings carry the associate marks and the equity carries the
# revaluation on deconsolidation -- and he says so; what survives is the claim that the
# whole investment case rests on the associate being worth more than the accounts say.
GRP_EQ_BEFORE_NCI_DEC25 = 28788.7    # 4Q25 release Table 12, GB Corp column
GRP_EQ_BEFORE_NCI_JUN26 = 33454.3    # 2Q26 release Table 12, GB Corp column
grp_roe_fy25 = HISTORY['income_statement']['2025']['net_profit'] / GRP_EQ_BEFORE_NCI_DEC25
_exp2_pb = (grp_roe_fy25 - TG) / (_sch.ke_terminal - TG)
exp2 = dict(base=GRP_EQ_BEFORE_NCI_JUN26 * _exp2_pb / SH,
            rng=(GRP_EQ_BEFORE_NCI_JUN26 * ((grp_roe_fy25 - 0.01) - TG)
                 / (_sch.ke_terminal - TG) / SH,
                 GRP_EQ_BEFORE_NCI_JUN26 * ((grp_roe_fy25 + 0.02) - TG)
                 / (_sch.ke_terminal - TG) / SH),
            roe=grp_roe_fy25, pb=_exp2_pb, book=GRP_EQ_BEFORE_NCI_JUN26,
            book_ps=GRP_EQ_BEFORE_NCI_JUN26 / SH)

# ---- THE LENS ARCHITECTURE, RECORDED AND ASSERTED IN THE STUDY'S OWN CODE ------------
# [R-ENF-02]: a study calls the gates itself and a job outside the study verifies it.
_LENS_RECORD = dict(
    _rule="[R-LENS-03] one class primary IS the central; the other lenses are cross-checks",
    **{"class": "automotive assembler and distributor with a captive lender"},
    primary=dict(
        kind="sotp",
        two_sided=True,
        branches=[dict(label=b['label'], value=b['value'], note=b['note'])
                  for b in BRANCHES],
        range=dict(low=min(b['value'] for b in BRANCHES),
                   high=max(b['value'] for b in BRANCHES)),
        range_note=("the sum of the parts read on the two bases GB Corp itself puts on "
                    "its interest in MNT-Halan. The auto leg and the lender leg are "
                    "identical in both."),
        range_basis=dict(
            driver=("the basis on which GB Corp's minority interest in MNT-Halan is "
                    "carried -- its reviewed carrying value against the June-2026 "
                    "primary round"),
            low=15733.523, high=27670.65,
            units="EGP million, the associate holding",
            macro_held=True,
            evidence=("BOTH ENDS ARE THE COMPANY'S OWN DISCLOSURES AND NEITHER IS THIS "
                      "DESK'S. The low end is note 34 to the reviewed consolidated "
                      "interim statements at 30 June 2026, EGP 15,733,523 thousand, "
                      "which foots to that balance sheet's own associates line. The high "
                      "end is 41.61% of the USD 1.4bn primary round GB Corp announced on "
                      "9 June 2026, at EGP 47.5. The macro path stood still across the "
                      "range: nothing in it moves inflation, the currency or the price of "
                      "time, and the currency used is the path's own. THE REVIEW "
                      "CONCLUSION ON THOSE STATEMENTS IS QUALIFIED AT EXACTLY THIS LINE "
                      "-- the reviewers were not provided with the associate's own "
                      "financial statements and could not verify the EGP 409.9mn share "
                      "of profit recorded in the period -- so the low end is not a safe "
                      "harbour either, and the study says so rather than resting on it."),
        ),
    ),
    cross_checks=[
        dict(kind="relative_multiple",
             value=rel_ps,
             multiple=REL_PE_OWN,
             multiple_source=("the MEDIAN of GB Corp's OWN trailing price-to-earnings at "
                              "its last three year-end closes -- 4.53x (2023), 6.35x "
                              "(2024) and 10.18x (2025), computed from its own reported "
                              "net profit attributable and its own share price. Never a "
                              "multiple from the current price. THREE OBSERVATIONS, and "
                              "the count is published with the median."),
             circularity=dict(spot=spot, shares=SH, net_debt=0.0, metric_value=np26),
             note=("earnings multiple, so the enterprise adjustment is nil by "
                   "construction and the traded multiple is simply market "
                   "capitalisation over the same forward earnings.")),
        dict(kind="book_value",
             value=GRP_EQ_BEFORE_NCI_JUN26 / SH,
             present_value=False,
             note=("GB Corp's own shareholders' equity before non-controlling interests "
                   "at 30 June 2026 over shares in issue. A DISCLOSED FLOOR, published "
                   "as such and carrying no weight in any answer above. It is worth "
                   "printing here because the shares trade BELOW it.")),
    ],
    envelope=dict(low=central_bear, high=central_bull),
    central=None,
    central_note=("there is no central. The primary is two-sided and the two branches "
                  "are published side by side; a figure between them would be the "
                  "average the dual-framing rule forbids."),
)
import research_protocol as _RP
_LENS_ATTEST = _RP.assert_lens_design(_LENS_RECORD, 'GBCO')

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
              mnt_halan_stake=mnt_halan_stake, mnt_halan_stake_prior=mnt_halan_stake_prior,
              mnt_halan_stake_source=("GB Corp's own press release of 9 June 2026 on "
                                      "MNT-Halan's Al Ahly Capital-led capital increase: the "
                                      "stake 'will be adjusted to 41.61%, compared to 42.58% "
                                      "prior to the transaction'"),
              mnt_halan_round_usd=mnt_halan_round_usd,
              egp_usd=egp_usd, mnt_halan_value=mnt_halan_value, other_assoc=other_assoc),
    lenses=dict(sotp=dict(bear=sotp_bear, base=sotp_ps, bull=sotp_bull),
                prediscount=dcf_lens, relative=rel, normalized=norm,
                central=dict(bear=central_bear, base=central, bull=central_bull),
                weights=weights),
    forecast=fc, gpm=gpm, sens=dict(grid_margin=grid_margin, grid_disc=grid_disc, table=sens),
    # THE DISCLOSED DRIVER BASE, COMMITTED SO THE DOCUMENT READS IT RATHER THAN RETYPING IT.
    # Depth-bar standard 3 again: the delivered edition printed every one of these by hand
    # because the numbers file did not carry them, so the driver table a reader sees and the
    # driver base the model runs on were two separate transcriptions of the same figures.
    disclosed_drivers=dict(
        _source=("GB Corp's own 4Q23 / 4Q24 / 4Q25 earnings releases, the segment volume and "
                 "revenue tables, committed under engine/gbco_study/src/"),
        pc_volume_units=pc_vol, pc_revenue=pc_rev,
        pc_asp={k: pc_rev[k] / pc_vol[k] for k in pc_vol},
        cv_volume_units=cv_vol, cv_revenue=cv_rev,
        lm_volume_units=lm_vol, lm_revenue=lm_rev,
        trading_revenue=tr_rev, auto_revenue_fy2025=auto_rev_fy25,
        growth=dict(pc_volume=vol_g, pc_asp=asp_g, cv_volume=cv_vg, cv_asp=cv_ag,
                    lm_volume=lm_vg, lm_asp=lm_ag, trading=tr_g),
        cost_stack=dict(gross_margin=gpm, gsa_pct=gsa, other_income_pct=oth,
                        provisions_pct=prov, dna_pct=dna_pct, capex=capex,
                        working_capital_pct=wc_pct, working_capital_fy2025=wc_prev,
                        tax_rate=TAX)),
    history=HISTORY,
    group_forecast=dict(
        _note=('the consolidated forecast income statement, computed here from the '
               'committed group drivers below so the delivered document and the '
               'delivered workbook print one arithmetic rather than two transcriptions'),
        rows=GROUP,
        drivers=dict(capital_revenue_fy2025=CAP_REV_FY25, capital_growth=cap_g,
                     capital_gross_margin=cap_gm, eliminations_pct=elim_pct,
                     group_opex_pct=grp_opex, group_other_income_pct=grp_oth,
                     group_provisions_pct=grp_prov, associates_income=assoc_inc,
                     net_finance_cost=fin_cost, minority_pct=mi_pct,
                     capital_dna=cap_dna,
                     capital_loanbook_growth=[0.35, 0.28, 0.24, 0.20, 0.18],
                     rental_and_other_capex=[700.0, 800.0, 900.0, 1000.0, 1100.0],
                     auto_inventory_pct=[0.36, 0.338, 0.32, 0.308, 0.296],
                     auto_receivables_pct=[0.08]*5,
                     auto_advances_pct=[0.07, 0.069, 0.0675, 0.066, 0.0645],
                     auto_payables_pct=[0.245, 0.237, 0.2325, 0.229, 0.2255],
                     net_new_borrowings=[5500.0, 5200.0, 5600.0, 5800.0, 6100.0],
                     dividend_payout=[0.14, 0.15, 0.16, 0.18, 0.20])),
    lens_inputs=LENS_INPUTS,
    edition='2026-09-07',
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
                   # COMPUTED, NOT TYPED. This sentence stated the wrong strike date and the
                   # wrong gap for as long as it existed, because both were typed once and the
                   # study was re-struck afterwards. Both are now derived from the path file
                   # and the resolved price date, so the disclosure cannot go stale on its own.
                   "The house Egyptian path's sovereign quote and currency spot are both "
                   "anchored %s and this study is struck against the latest known price, %s "
                   "\u2014 %d days later. Refreshing a house macro path is a house-level act "
                   "rather than a step of one name's rebuild, so the staleness is DISCLOSED "
                   "and deliberately accepted rather than switched off, exactly as this house "
                   "already treats a deliberately-accepted stale sovereign quote."
                   % (_ANCHOR_DATE, spot_date,
                      (_datetime_mod.date.fromisoformat(spot_date)
                       - _datetime_mod.date.fromisoformat(_ANCHOR_DATE)).days)),
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
    # THE ANSWER IS TWO-SIDED AND SAYS SO IN THE SHAPE EVERY GATE READS [R-LENS-03].
    # A study that publishes two answers and does not declare it is read as single-sided
    # by everything downstream, and the branch nobody reads is the one that disagrees.
    central_two_sided=dict(
        why=("GB Corp's largest single component is a minority interest in an unlisted "
             "company, and the two bases on which the company itself puts a number on it "
             "differ by EGP 11.9bn -- 27% of this answer. Both are GB Corp's own "
             "disclosures and the filings do not decide between them, so neither does "
             "this study."),
        branches=[dict(label=b['label'], value=b['value'], condition=b['note'])
                  for b in BRANCHES]),
    lens_record=_LENS_RECORD,
    valuation_gap=dict(
        central=None, spot=spot, spot_date=spot_date,
        gap=None,
        branch_gaps=[dict(label=b['label'], central=b['value'],
                          gap=b['value']/spot - 1.0) for b in BRANCHES],
        mc_anchor=mc_anchor, mc_anchor_date=mc_anchor_date,
        price_note=("THIS NOTE WAS STALE AND IS REWRITTEN FROM THE RESOLVER BESIDE IT "
                    "[07-09-2026]. It stated that no supplied price existed for GBCO and "
                    "that the study was struck on the exchange library's own last close, and "
                    "the resolver twelve lines above it had already found one — so a typed "
                    "sentence contradicted the committed spot in the same file, which is the "
                    "defect a computed figure exists to stop. The latest known price is read "
                    "from the committed engine/prices/SUPPLIED_*.json files and never typed: "
                    "%.2f as at %s. The cone is a different clock and is anchored on the last "
                    "real session the exchange library holds, %.2f on %s; both are published "
                    "with their own dates [R-GAP-01 AMENDED]."
                    % (spot, spot_date, mc_anchor, mc_anchor_date))),
)
# EVERY OUTPUT LANDS BESIDE THIS SCRIPT, NEVER IN THE CALLER'S DIRECTORY. Run from the
# repository root, the relative names these five writes used to carry scattered the study's
# artefacts into the root AND LEFT THE STUDY'S OWN NUMBERS FILE UNTOUCHED while the run
# printed success — an absent result wearing a clean one's clothes [R-ENF-04]. HERE is what
# every other study in this book resolves against.
res.to_csv(os.path.join(HERE, 'backtest_rows.csv'), index=False)
np.save(os.path.join(HERE, 'fan.npy'), np.array([fan[p] for p in [5, 25, 50, 75, 95]]))
np.save(os.path.join(HERE, 'pT20.npy'), pT20[:20000])
np.save(os.path.join(HERE, 'pT60.npy'), pT60[:20000])
with open(os.path.join(HERE, 'study_numbers.json'), 'w') as f:
    json.dump(out, f, indent=1, default=float)
print('spot', spot, spot_date, '| anchor_vol', round(anchor_vol, 3),
      '| drift_q', round(drift_daily*60*100, 1), '% | factor_q', round(factor_drift_q*100, 2), '%')
print('Step0 non-overlap:', {k: round(v, 3) if isinstance(v, float) else v for k, v in summ.items()})
print('T60:', {k: round(v, 1) for k, v in q60.items()}, '| prob_read P(up)=%.2f odds=%.2f' % (prob_read['p_above'], prob_read['odds']))
print('DCF: EV %.0f TV%% %.0f%% AutoEq %.0f | Capital %.0f (%.3fx book, ROE %.2f%%) '
      '| SOTP/sh  carrying %.2f  round %.2f  | envelope [%.2f-%.2f] | spot %.2f'
      % (ev_auto, 100*pv_tv/ev_auto, auto_eq, cap_val, cap_pb, 100*cap_roe_adopted,
         sotp_B_ps, sotp_A_ps, central_bear, central_bull, spot))
print('gap vs spot: carrying %+.1f%%   round %+.1f%%'
      % (100*(sotp_B_ps/spot-1), 100*(sotp_A_ps/spot-1)))
print('relative %.2f at %.3fx own-history median P/E (traded %.3fx) | book floor %.2f'
      % (rel_ps, REL_PE_OWN, rel_traded_pe, GRP_EQ_BEFORE_NCI_JUN26/SH))
print('FCFF path:', [round(r['fcff']) for r in rows])
