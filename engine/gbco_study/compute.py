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

# EVERY TOTAL A READER SEES IS REPRODUCIBLE FROM THE ROWS PRINTED ABOVE IT [audit
# finding 6]. Appendix A.2 printed GB Corp's own "Operating Profit" line and the rows above
# it do not sum to it in two of the three years -- by 269.0 in FY2023 and 355.7 in FY2024,
# which are those years' PROVISIONS to the pound. The company's own presentation changed:
# operating profit EXCLUDED provisions in FY2023 and INCLUDES them from FY2024, and the
# study's own committed EBIT proves which is which (FY2023's 4,769.7 less associates of
# 1,061.7 is 3,708.0, not the printed 3,977.0). The line the table prints is computed here
# from the rows above it, on ONE basis across the three years, and the as-reported figures
# are carried beside it rather than replaced -- a restatement is noted, never substituted.
_FOOTED_OP = {y: round(
    _is['gross_profit'] + _is['selling'] + _is['admin'] + _is['other_income']
    + _is['provisions'], 1)
    for y, _is in ((yy, HISTORY['income_statement'][yy]) for yy in HIST_YEARS)}
for _y in HIST_YEARS:
    _ebit_implied = HISTORY['income_statement'][_y]['ebit'] - HISTORY['income_statement'][_y]['associates']
    assert abs(_FOOTED_OP[_y] - _ebit_implied) < 0.15, (_y, _FOOTED_OP[_y], _ebit_implied)

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
# ---- THE CONE IS STRUCK ON THE SESSION SERIES, NOT ON THE SUPPLIED CLOSE -------------
# `mc_anchor` is defined four hundred lines above with the comment "the cone is struck on
# real sessions", and this block then seeded every path with `spot` — the hand-supplied
# close of 3 September, which is not in the library and has no session behind it. THE
# CODE'S OWN STATED CONVENTION AND THE CODE DISAGREED, and the document inherited the
# disagreement: it told a reader four times that the cone was computed on the exchange
# library's last session while the arithmetic ran from a different number, and section 3
# printed BOTH — its probability table measured against one and the level-touch ladder's
# "against the anchor" column against the other, in one section, two tables apart.
#
# TWO CLOCKS IS THE RULE AND IS NOT WHAT WENT WRONG. A fair value is delivered against the
# LATEST KNOWN price [R-GAP-01 AMENDED]; a probability cone needs a session series and a
# supplied close is not one. Both dates are published. What was wrong is that the cone was
# not on its own clock at all.
paths[:, 0] = mc_anchor
paths[:, 1:] = mc_anchor * np.exp(logp)

# ASSERTED RATHER THAN ASSUMED, because nothing about a wrong anchor looks wrong: every
# percentile is a plausible price and the only witness is the number the paths started on.
assert abs(paths[0, 0] - mc_anchor) < 1e-12 and float(paths[:, 0].min()) == \
    float(paths[:, 0].max()) == mc_anchor, (
    "the cone must start on the session anchor it says it starts on")

pT20, pT60 = paths[:, 20], paths[:, 60]
pcts = [5, 25, 50, 75, 95]
q20 = {p: float(np.percentile(pT20, p)) for p in pcts}
q60 = {p: float(np.percentile(pT60, p)) for p in pcts}
run_max = paths.max(axis=1); run_min = paths.min(axis=1)
run_max20 = paths[:, :21].max(axis=1); run_min20 = paths[:, :21].min(axis=1)
levels = [40, 38, 36, 34, 32, 30, 28, 26]
touch = {L: dict(t20=float(np.mean(run_max20 >= L) if L > mc_anchor else np.mean(run_min20 <= L)),
                 t60=float(np.mean(run_max >= L) if L > mc_anchor else np.mean(run_min <= L)))
         for L in levels}
prob_read = dict(
    p_above=float(np.mean(pT60 > mc_anchor)),
    p_up10=float(np.mean(pT60 >= mc_anchor * 1.10)),
    p_dn10=float(np.mean(pT60 <= mc_anchor * 0.90)),
    median=float(np.median(pT60)),
    med_move=float(np.median(pT60) / mc_anchor - 1),
    band50=(q60[25], q60[75]),
    band50_pct=((q60[25] / mc_anchor - 1), (q60[75] / mc_anchor - 1)),
    touch_up10=float(np.mean(run_max >= mc_anchor * 1.10)),
    touch_dn10=float(np.mean(run_min <= mc_anchor * 0.90)),
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
# THE FIFTH LINE, WHICH THE DELIVERED EDITION ZEROED FOR EVERY FORECAST YEAR [audit
# finding 5]. GB Auto's FY2025 total revenue is EGP 66,358.3mn and the four lines above
# sum to 65,230.7 -- the base year carried a fifth line of 1,127.6 that the forecast did
# not. It is two disclosed components, and both are named rather than merged:
#   * 682.8 of revenue outside the four published business lines. The 4Q25 release gives
#     GB Auto's external revenue as 65,913.5 against those four lines' 65,230.7, and its
#     line tables are headed "Sales AND AFTER-SALES Activity" without publishing the
#     after-sales revenue separately.
#   * 444.8 of inter-segment revenue (Table 8, "Inter-Segment Revenue"), which is real
#     revenue to this segment and is removed again at group level by the elimination line.
# IT MATTERS BECAUSE THE MARGIN IS STRUCK ON THE WHOLE. Table 8's gross margin of 14.8%
# is computed on TOTAL revenue of 66,358.3, so applying that margin to a forecast revenue
# that omits the fifth line understates gross profit by construction.
# HELD FLAT, per [R-ANCHOR-01]'s discipline on an observable the company does not break
# out: the company publishes no volume, price or growth rate for it, so it is carried at
# its own filed level rather than grown at a rate nothing measures.
os_rev = {'FY25': 682.8}      # outside the four published lines
is_rev = {'FY25': 444.8}      # inter-segment
of_rev = {'FY25': os_rev['FY25'] + is_rev['FY25']}
assert abs(pc_rev['FY25'] + cv_rev['FY25'] + lm_rev['FY25'] + tr_rev['FY25']
           + of_rev['FY25'] - 66358.3) < 0.05
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
                 cv_rev=cvv*cva, lm_rev=lmv*lma, tr_rev=trr, of_rev=of_rev['FY25'])
    fc[y]['auto_rev'] = (fc[y]['pc_rev'] + fc[y]['cv_rev'] + fc[y]['lm_rev']
                         + fc[y]['tr_rev'] + fc[y]['of_rev'])
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
# fin_cost IS DERIVED BELOW, once the cost-of-capital schedule exists [audit finding 9].
# The delivered edition typed a ladder falling -4,100 -> -3,100 while its own balance-sheet
# markers grew group borrowings 38,041 -> 66,241: a finance cost falling while the debt
# behind it rises, with no derivation anywhere and nothing that could have reconciled them.
mi_pct = [-0.02]*5
cap_dna = [560.0, 640.0, 730.0, 830.0, 940.0]
gpm = [0.138, 0.142, 0.145, 0.145, 0.145]
gsa = [0.073, 0.072, 0.071, 0.070, 0.070]
oth = 0.012; prov = -0.003
dna_pct = [0.011, 0.011, 0.011, 0.011, 0.011]
capex = [3000, 2400, 2500, 2600, 2800]
# THE WORKING-CAPITAL ANCHOR [audit finding 2 -- the largest finding in that audit and
# the one this study's own self-audit missed]. The delivered edition ran the cash-flow
# walk from the 31-Dec-2025 stock while the bridge deducted 30-June-2026 net debt: TWO
# BALANCE-SHEET DATES IN ONE CALCULATION. It then glided the intensity down a typed ladder
# to 21.5% on a stated mechanism -- the stock build unwinding and payables re-extending.
#
# THE MECHANISM IS MEASURED IN THE COMPANY'S OWN PERIOD PAIR AND ONLY HALF OF IT HOLDS.
# From this study's own conversion-cycle record (asset_cycle.json, built from the disclosed
# segment tables with every table footed):
#     stock build unwinding    DIO 149.0 -> 127.1 days   MEASURED, HOLDS
#     payables re-extending    DPO 112.7 ->  83.3 days   CONTRADICTED, they SHORTENED
# and the net cash cycle got WORSE, 61.3 -> 69.3 days. [R-ANCHOR-01] permits a drift away
# from the latest reviewed actual only where a named mechanism has a MEASURED like-for-like
# direction; a mechanism contradicted by the company's own filings is not a mechanism, so
# the intensity is HELD FLAT at the level the latest reviewed period actually filed.
#
# ONE BASIS THROUGHOUT, which is what makes the two numbers comparable: working capital as
# the release's Table 6 defines it, over GB Auto's TOTAL REVENUE as its Table 8 defines it
# -- the same revenue line this model forecasts.
WC_TOTAL_REV_FY25 = 66358.3     # 4Q25 release Table 8, GB Auto Total Revenue FY25
WC_TOTAL_REV_1H25 = 30672.7     # 2Q26 release Table 8, prior-year column
WC_TOTAL_REV_1H26 = 40021.5     # 2Q26 release Table 8
WC_TTM_REV = WC_TOTAL_REV_FY25 - WC_TOTAL_REV_1H25 + WC_TOTAL_REV_1H26
# THE ANCHOR IS THE SUM OF THE FOUR DISCLOSED COMPONENTS, NOT THE TABLE'S STATED TOTAL,
# and the difference between them is a tenth of a million -- the release's own rounding,
# five rows printed to one decimal place. Both are GB Corp's own figures; the components
# are the ones the workbook projects its balance sheet from, so taking the anchor from
# them is what stops the model and the workbook carrying two numbers for one quantity.
WC_COMPONENTS_2Q26 = 22959.1 + 5873.5 + 1153.7 + 2598.9 - 15492.5   # Table 6, 30-Jun-2026
assert abs(WC_COMPONENTS_2Q26 - 17092.8) <= 0.25   # 5 rows x 0.5 x 10^-1, the printed rounding
WC_BASE_INTENSITY = 18917.0 / WC_TOTAL_REV_FY25          # 28.51% at 31-Dec-2025
WC_ANCHOR = WC_COMPONENTS_2Q26 / WC_TTM_REV               # 22.58% at 30-Jun-2026
# THE FOUR COMPONENTS REPRODUCE THE NET FIGURE, asserted rather than assumed: the workbook
# projects its balance sheet from them and the cash-flow model from the net intensity, and
# nothing compared the two until the recalculation gate did.
assert abs(WC_COMPONENTS_2Q26 / WC_TTM_REV - WC_ANCHOR) < 1e-12
wc_pct = [WC_ANCHOR] * 5
# THE OPENING WORKING CAPITAL, CAPTURED BEFORE THE LOOP CONSUMES THE NAME. The record
# committed `working_capital_fy2025=wc_prev` four hundred lines below, and wc_prev is the
# loop's running variable — so the field named for the base year carried FY2030E's
# closing balance, 31,123.6 against a base of 18,917.0, and read as a working-capital
# intensity of 46.9% of FY2025 revenue where the real opening intensity is 28.5%. A
# FIELD WHOSE NAME SAYS ONE YEAR AND WHOSE VALUE IS ANOTHER IS WORSE THAN A MISSING
# FIELD: this author read it as the filed actual and drew a conclusion from it before
# checking what wrote it, which is [R-ENF-06]'s lesson arriving through a variable name.
# THE WALK NOW STARTS WHERE THE BRIDGE STANDS. 17,092.8 is GB Auto's working capital at
# 30 June 2026 on Table 6's own definition, the same date the net-debt bridge below is
# struck at.
WC_OPENING = WC_COMPONENTS_2Q26
wc_prev = WC_OPENING
# ...AND THE FIRST FORECAST YEAR IS THEREFORE A STUB. This is the same defect one layer
# down, and it is not one the audit raised. A bridge struck at 30 June 2026 already
# reflects the cash the first half of 2026 produced -- GB Auto's net debt fell from
# 15,210.0 at 31 December 2025 to 14,493.6 at 30 June 2026 -- so discounting a FULL
# calendar-2026 free cash flow beside it counts that half twice: once in the debt it has
# already paid down, and once in the cash flow. The working-capital delta needs no
# correction because it now runs from the 30-June stock and is already the second half's
# alone; the profit, depreciation and capital expenditure are full-year figures and are
# scaled to the part of the year still unearned.
#
# THE FRACTION IS MEASURED, NOT HALVED: GB Auto's first-half total revenue is a disclosed
# actual and the share of the model's own FY2026E revenue it represents is what has been
# earned. IT IS A PROPORTIONALITY ASSUMPTION ACROSS THE THREE LINES and is labelled as one
# -- a second half is not a pro-rata copy of a first half, and replacing the first half
# with its actual income statement would be the better construction. What it replaces is
# not a better approximation but a double count.
AUTO_1H26_TOTAL_REV = 40021.5      # 2Q26 release Table 8, GB Auto Total Revenue 1H26
STUB_EARNED = AUTO_1H26_TOTAL_REV / (fc['FY26E']['pc_rev'] + fc['FY26E']['cv_rev']
                                     + fc['FY26E']['lm_rev'] + fc['FY26E']['tr_rev']
                                     + fc['FY26E']['of_rev'])
STUB_FRACTION = 1.0 - STUB_EARNED
assert 0.0 < STUB_FRACTION < 1.0, (
    "the model forecasts a full year at or below what the company has already filed for "
    "six months, which is a finding about the forecast rather than a stub: %r" % STUB_EARNED)
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
    _earned = STUB_FRACTION if i == 0 else 1.0
    fcff = (nopat + dna - capex[i]) * _earned - dwc
    rows.append(dict(year=y, rev=r, gp=gp, ebitda=ebitda, ebit=op, dna=dna,
                     nopat=nopat, capex=capex[i], dwc=dwc, fcff=fcff, wc=wc,
                     unearned_fraction=_earned))
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

# THE BRIDGE STANDS ON THE LATEST DISCLOSED BALANCE SHEET [R-BRIDGE-01]. The delivered
# edition stood on 31-Dec-2025 while GB Corp's reviewed 30-June-2026 consolidated statements
# and its 2Q26 earnings release (13 August 2026) were both published and on its own IR site.
#
# THE COMPANY'S OWN DEFINITION IS THE ONE THE COMPANY PRINTS, AND THE DELIVERED EDITION
# DID NOT REPRODUCE IT [audit finding 24, and self-audit S-2 reached independently]. It
# claimed "the COMPANY'S OWN definition" in a comment and came out at 14,623.7 against a
# published 14,493.6, because it took only the NON-CURRENT portion of the notes payable to
# leasing (1,333.3 of 2,345.8) and omitted the due-FROM-related-parties balance the
# company's own table nets. A definition asserted in a comment is not a definition; the
# five rows below are Table 7's own, in its own order, and they foot to its own total.
#
#   Total debt                                   22 733.1   (20,943.0 short + 1,790.1 long)
#   Notes payable (due to leasing)                2 345.8
#   less Cash                                    (9 445.0)
#   Due to related parties - inter segment            1.8
#   less Due from related parties - inter segment (1 142.1)
#   NET DEBT                                     14 493.6
#
# THESE INPUTS SIT HERE, ABOVE THE SCHEDULE, BECAUSE THE SCHEDULE NOW DEPENDS ON THEM:
# the Auto leg is discounted at the Auto leg's OWN cost of capital and the equity weight
# in it is this leg's own equity value, which the bridge produces.
AUTO_TOTAL_DEBT_ST   = 20943.0
AUTO_TOTAL_DEBT_LT   = 1790.1
AUTO_LEASE_NOTES     = 2345.8
AUTO_CASH            = 9445.0
AUTO_DUE_TO_RELATED  = 1.8
AUTO_DUE_FROM_RELATED = 1142.1
auto_nd = (AUTO_TOTAL_DEBT_ST + AUTO_TOTAL_DEBT_LT + AUTO_LEASE_NOTES - AUTO_CASH
           + AUTO_DUE_TO_RELATED - AUTO_DUE_FROM_RELATED)
assert abs(auto_nd - 14493.6) < 0.05, auto_nd   # GB Corp 2Q26 earnings release, Table 7
# THE MINORITY AT ITS SHARE OF VALUE, NOT AT BOOK [R-BRIDGE-01 defect (ii); self-audit
# S-1]. The delivered edition deducted EGP 590.7mn -- the minority's BOOK equity in GB
# Auto's segment balance sheet -- from a leg valued by capitalising 100% of that segment's
# cash flow. The minority's claim is on the VALUE those cash flows produce, not on what its
# share historically cost, and [R-BRIDGE-01] does not allow book to be the adopted basis.
#
# THE BASIS IS value_share AND THE PROXY IS NAMED, because GB Corp does not disclose which
# subsidiaries carry the minority or what they earn: the minority's proportion of the
# segment's own disclosed book equity, applied to the segment's equity VALUE. Both figures
# are the company's own, from Table 12 of the 2Q26 earnings release as at 30 June 2026.
AUTO_EQUITY_BOOK_BEFORE_NCI = 12998.3   # "Total Shareholders' Equity Before NCI", GB Auto
AUTO_NCI_BOOK               = 590.7     # "Total NCI", GB Auto
assert abs((AUTO_EQUITY_BOOK_BEFORE_NCI + AUTO_NCI_BOOK) - 13589.0) < 0.05   # "Total Equity"
AUTO_NCI_SHARE = AUTO_NCI_BOOK / (AUTO_EQUITY_BOOK_BEFORE_NCI + AUTO_NCI_BOOK)
# The three reference framings [R-BRIDGE-01] requires published beside the adopted basis:
AUTO_NCI_AT_BOOK = AUTO_NCI_BOOK
AUTO_NCI_PROFIT_SHARE = 246.8           # GB Auto segment NCI in 1H26 profit, Table 8
auto_nci = AUTO_NCI_BOOK                # superseded below; kept so the book framing is
                                        # committed rather than described

# ===== ONE CAPITAL STRUCTURE THROUGHOUT [audit finding 11] ============================
# THE DELIVERED EDITION RAN THREE OF THEM IN ONE CALCULATION: the GROUP's borrowings and
# the GROUP's market capitalisation in the weights, a GROUP cost of debt whose numerator
# deliberately included GB CAPITAL'S cost of funds, and then the AUTO SEGMENT's net debt
# in the bridge. The published 22.88% landed within 0.3pp of one internally consistent
# pairing -- right by offsetting errors rather than by construction, and no reader could
# have told. The leg being valued is GB Auto's and the bridge deducts GB Auto's net debt,
# so the rate that discounts it is GB Auto's.
#
# THE EFFECTIVE RATE IS COMPUTED HERE FROM THE COMPANY'S OWN QUARTERLY TABLE rather than
# from an opening/closing average, because this book grew 77% in FY2025 and an average of
# two year-ends describes a balance that existed for none of it. On this book the two
# constructions agree to four basis points, which is worth recording: the re-basing
# mechanism [R-COC-01 AMENDED] names is real here and its effect on the rate is not.
# DENOMINATOR: total debt PLUS the notes payable due to leasing, because the release states
# in its own footnote that the finance cost INCLUDES the leasing expense -- the numerator
# and the denominator have to be the same book [R-FCAL-01 trap (i), facing the other way].
AUTO_DEBT_Q      = [12119.3, 14466.7, 18092.2, 18208.0, 21486.3]  # 4Q24..4Q25, Table 7
AUTO_LEASE_Q     = [752.7, 722.9, 1600.1, 2160.3, 2576.2]         # same table
AUTO_FIN_COST_FY25 = 3689.4                                        # Table 8, FY25
AUTO_DEBT_Q26    = [21486.3, 21452.2, 22733.1]                     # 4Q25, 1Q26, 2Q26
AUTO_LEASE_Q26   = [2576.2, 2464.1, 2345.8]
AUTO_FIN_COST_1H26 = 2206.7                                        # Table 8, 1H26

def _quarter_weighted(xs):
    return sum((a + b) / 2.0 for a, b in zip(xs[:-1], xs[1:])) / (len(xs) - 1)

AUTO_EFF_FY25 = AUTO_FIN_COST_FY25 / (_quarter_weighted(AUTO_DEBT_Q)
                                      + _quarter_weighted(AUTO_LEASE_Q))
AUTO_EFF_1H26 = (AUTO_FIN_COST_1H26 * 2.0) / (_quarter_weighted(AUTO_DEBT_Q26)
                                              + _quarter_weighted(AUTO_LEASE_Q26))
# THE BOOK IS NOT ALL LOCAL CURRENCY AND THE DELIVERED EDITION ASSERTED THAT IT WAS
# [audit finding 4]. Note 26 to the FY2025 audited statements states two average rates for
# the year -- EGP 21.91% and USD 8.30% (EGP 29.19% and USD 8.40% in 2024) -- so a single-
# currency shortcut is contradicted by the company's own note. THE SPLIT ITSELF IS NOT
# DISCLOSED, so it is DERIVED by identity from the two disclosed rates and this segment's
# own measured rate, and LABELLED as derived: an identity is not an assumption and the
# label is what keeps the two apart. The rates are the GROUP's, applied to the SEGMENT's
# measured rate, which is the only currency evidence the filings carry; SIGCM clause 8 is
# met by naming that rather than by asserting a split.
NOTE26_KD_EGP, NOTE26_KD_USD = 0.2191, 0.0830
AUTO_PCT_LOCAL = (AUTO_EFF_FY25 - NOTE26_KD_USD) / (NOTE26_KD_EGP - NOTE26_KD_USD)
AUTO_KD = AUTO_EFF_1H26     # the latest independently computed rate, per [R-ANCHOR-01]

_auto_book = _COC.DebtBook(
    gross_debt=AUTO_TOTAL_DEBT_ST + AUTO_TOTAL_DEBT_LT + AUTO_LEASE_NOTES,
    pct_local_currency=AUTO_PCT_LOCAL,
    currency_source=("GB Corp FY2025 audited consolidated statements, note 26 (loans, "
                     "borrowings and overdrafts): the average interest rate of the current "
                     "EGP and USD loans and borrowings was 21.91% and 8.30% respectively "
                     "during the year (29.19% and 8.40% during 2024). The note states the "
                     "two RATES and not the two BALANCES, so the split carried here is "
                     "DERIVED by identity from those rates and GB Auto's own measured "
                     "effective rate, and is labelled derived wherever it is quoted."),
    kd_local_pretax=AUTO_KD,
    kd_source=("GB Auto's OWN effective borrowing rate over the latest reviewed period, "
               "computed independently from GB Corp's 2Q26 earnings release, Tables 7 and "
               "8, on the borrowings that actually bear the charge."),
    effective_rates=(AUTO_EFF_FY25, AUTO_EFF_1H26),
    effective_rate_periods=("FY2025", "1H2026 annualised"),
    interest_bearing_note=(
        "GB Auto's SEGMENT finance cost (FY25 EGP 3,689.4mn; 1H26 EGP 2,206.7mn, "
        "annualised) over a QUARTER-WEIGHTED average of that segment's own total debt plus "
        "its notes payable due to leasing (Table 7, five quarters to 4Q25 and three to "
        "2Q26). The leasing notes are inside the denominator because the release's own "
        "footnote says the finance cost includes the leasing expense. Trade payables, "
        "advances from customers, debtors and other credit balances are excluded because "
        "they bear no interest, and GB CAPITAL'S COST OF FUNDS IS EXCLUDED ALTOGETHER -- "
        "it is a different entity's funding and putting it here is what finding 11 named."))

_ERP = {"rating": 0.1394, "market": 0.0941}   # Damodaran country-risk file, Egypt row
# MARKET-VALUE EQUITY WEIGHTS ON A LEG WITH NO QUOTED PRICE. [R-COC-01] requires the
# equity weight to be a MARKET value and never book, and a SEGMENT has no market price --
# which is why the delivered edition reached for the group's market capitalisation and so
# weighted GB Auto's cash flows by GB Corp's equity. The weight is instead taken to a FIXED
# POINT: the leg is valued, its own equity value becomes the weight, and the map is solved
# to convergence. It is reproducible arithmetic rather than a chosen number, the map is
# monotone decreasing in the weight (more equity weight, higher cost of capital, lower
# value), so it is BISECTED rather than iterated -- a damped iteration converges here too
# and bisection cannot fail to.
_PATH = _MP.load("EG")
TG_REAL = 0.0
TG = _PATH.terminal_inflation + TG_REAL


def _auto_schedules(mcap):
    return {b: _COC.schedule("EG", _beta, _auto_book, market_cap=mcap, tax_rate=TAX,
                             years=5, erp_basis=b, erp_explicit=_ERP[b],
                             build_date=spot_date, allow_stale_sovereign=True)
            for b in ("rating", "market")}


def _auto_equity_at(sch):
    """The leg's TOTAL equity value -- before the minority's share of it.

    That is the quantity the capital structure is made of: the weight is what the
    whole of this leg's equity is worth against what it owes, and the minority owns
    a slice of that equity rather than sitting outside it.
    """
    pv = sum(rw['fcff'] * df for rw, df in zip(rows, sch.discount_factors))
    tv_ = rows[-1]['fcff'] * (1 + TG) / (sch.wacc_terminal - TG)
    return pv + tv_ * sch.terminal_discount_factor - auto_nd


def _f(mcap):
    return _auto_equity_at(_auto_schedules(mcap)["market"]) - mcap


_lo, _hi = 1.0, 1.0e6
assert _f(_lo) > 0 and _f(_hi) < 0, (_f(_lo), _f(_hi))
for _AUTO_W_ITERS in range(1, 201):
    _mid = 0.5 * (_lo + _hi)
    if _f(_mid) > 0:
        _lo = _mid
    else:
        _hi = _mid
    if _hi - _lo < 1e-9 * _hi:
        break
AUTO_EQUITY_WEIGHT = 0.5 * (_lo + _hi)
_SCHED = _auto_schedules(AUTO_EQUITY_WEIGHT)
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
# THE ANCHOR DATE IS READ FROM THE PATH FILE, NEVER TYPED — it is the date the staleness
# disclosure below is measured from, and a typed copy of it goes stale the day the path is
# refreshed while the sentence quoting it does not.
import json as _json_path
_ANCHOR_DATE = _json_path.load(open(os.path.join(
    HERE, '..', 'macro_paths', 'EG.json'), encoding='utf-8'))['fx']['spot']['date']
for i, rw in enumerate(rows):
    rw['wacc_y'] = _sch.forward_wacc[i]
    rw['df'] = _sch.discount_factors[i]
    rw['pv'] = rw['fcff'] * rw['df']
pv_sum = sum(rw['pv'] for rw in rows)
tv = rows[-1]['fcff'] * (1 + TG) / (_sch.wacc_terminal - TG)
pv_tv = tv * _sch.terminal_discount_factor
ev_auto = pv_sum + pv_tv
auto_total_eq = ev_auto - auto_nd            # the WHOLE of this leg's equity
auto_nci_value = AUTO_NCI_SHARE * auto_total_eq
AUTO_NCI_PROPORTIONAL = auto_nci_value      # the proportional framing IS the adopted one
                                            # here, the proxy being a proportion
auto_eq = auto_total_eq - auto_nci_value    # the parent's share
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
# A RESTATED FIGURE MINUS AN UNRESTATED ONE IS NOT A BASE [audit finding 8]. The
# delivered edition subtracted the associates at their RESTATED 31-Dec-2025 carrying value
# from GB Capital's segment equity as the 4Q25 release printed it -- a release of 26
# February 2026, four months BEFORE the restatement appeared. Note 34's adjustment of
# +2,460,218 thousand raises the associate AND the equity that carries it by the same
# amount, so netting one restated against the other unrestated HALVED the operating base
# and doubled every return struck on it. Both sides are moved onto the restated basis
# here; the unrestated equity is kept beside it so the reader can see the step.
CAP_FY25_EQ_BEFORE_NCI_AS_RELEASED = 18312.6   # 4Q25 release Table 12, GB Capital column
ASSOC_RESTATEMENT_DEC25 = 2460.218             # note 34, "adjustments on the beginning
                                               # balance", the only adjustment in the table
CAP_FY25_EQ_BEFORE_NCI = CAP_FY25_EQ_BEFORE_NCI_AS_RELEASED + ASSOC_RESTATEMENT_DEC25
ASSOC_CARRYING_DEC25   = 15732.426  # reviewed BS 30-Jun-2026, comparative column, and
                                    # note 34's own restated total: 13,272.208 + 2,460.218
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
# ---- THE FINANCE COST, DERIVED FROM THE MODEL'S OWN COST OF DEBT [audit finding 9] ----
# A rate ladder times a book, rather than five typed numbers. Both come from somewhere the
# model already holds: the forward cost of debt is the sanctioned schedule's own glide
# between the adopted rate and the norm-built terminal, and the book is GB Auto's own
# interest-bearing borrowings at 30 June 2026.
#
# WHY GB AUTO'S BOOK AND NOT THE GROUP'S, on a GROUP income-statement line: GB Capital's
# cost of funds is booked inside that segment's COST OF REVENUE and never reaches the
# group finance-cost line. The arithmetic says so rather than the reasoning -- GB Auto's
# own FY2025 finance cost is EGP 3,689.4mn against a group net finance cost of 3,702.1mn,
# a difference of 0.3%, so the group's expensed charge IS essentially the Auto leg's. That
# ratio is carried forward as the small non-Auto residual rather than assumed away.
#
# THE BOOK IS HELD FLAT AND THAT IS A STATED LIMITATION, NOT A FORECAST. This model has no
# projected balance sheet -- capital expenditure, depreciation and working capital are
# three independent ratios with nothing joining them (self-audit S-5) -- so there is no
# sourced borrowings path to multiply. Holding the latest disclosed book flat is the
# least-invented choice available and it is named wherever the line is published; building
# the roll-forward that would replace it is a rebuild of the forecast, not a repair.
GROUP_FIN_COST_FY25 = 3702.1        # 4Q25 release Table 1, "Net Finance Cost", FY25
GROUP_TO_AUTO_FIN = GROUP_FIN_COST_FY25 / AUTO_FIN_COST_FY25
AUTO_GROSS_DEBT = AUTO_TOTAL_DEBT_ST + AUTO_TOTAL_DEBT_LT + AUTO_LEASE_NOTES
KD_FORWARD = [_sch.kd_pretax - (_sch.kd_pretax - _sch.kd_terminal_pretax) * f
              for f in _sch.glide_fractions]
fin_cost = [-(AUTO_GROSS_DEBT * k * GROUP_TO_AUTO_FIN) for k in KD_FORWARD]

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
# THE EXCHANGE RATE IS THE HOUSE PATH'S, READ FROM IT, WITH ITS DATE [audit finding 32;
# [R-MACRO-01]]. The delivered edition typed 47.5 with no source and no date, on a line
# worth roughly half of the upper branch -- and the audit's complaint is exactly right that
# four different dates were in play for one rate. A study may not carry a currency of its
# own: engine/macro_paths/EG.json holds one dated sourced anchor for the market and every
# study reads it, which is what stops two studies valuing the same economy differently.
egp_usd = _PATH.fx_spot
EGP_USD_DATE = _json_path.load(open(os.path.join(
    HERE, '..', 'macro_paths', 'EG.json'), encoding='utf-8'))['fx']['spot']['date']
EGP_USD_TYPED_BEFORE = 47.5      # committed so the move is countable rather than described
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
# THE ASSOCIATES NOTE, RE-READ OFF THE RENDERED PIXELS AND FOOTED IN EVERY DIRECTION
# [audit finding 16]. The delivered edition carried 15,733,523 with a comment that
# reconstructed it as "restated 15,315,532 + 8,006 of other comprehensive income +
# 409,985 of period profit", and recorded a "ten-thousand OCR ambiguity" in the three
# smaller rows. THE AMBIGUITY WAS IN THE MNT ROW ITSELF and the reconstruction was wrong
# in two cells: MNT's restated opening is 15,313,538, and MNT has NO other comprehensive
# income at all -- the 32,119 in that column is Bedaia's. Note 34 as filed:
#
#   row (EGP 000)      31-Dec-25    adjustment   restated    div      OCI     profit    add'ns   30-Jun-26
#   MNT Investment BV  12 853 320    2 460 218  15 313 538     -        -    409 985        -   15 723 523
#   Misr E-commerce       125 701            -     125 701     -        -    (16 060)       -      109 641
#   Bedaia                152 983            -     152 983 (21 220) 32 119     12 959       -      176 841
#   Kaf for life          140 204            -     140 204     -        -      3 256   77 000      220 460
#   TOTAL              13 272 208    2 460 218  15 732 426 (21 220) 32 119    410 140   77 000   16 230 465
#
# EVERY COLUMN AND EVERY ROW FOOTS EXACTLY on this reading and the delivered figure foots
# on none of them, which is the arbitration the four-field rule asks for: ARITHMETIC IS
# THE ARBITER, NOT THE EXTRACTOR'S CONFIDENCE. Route: 500-dpi render of page 34 of the
# reviewed consolidated interim statements, read as an image, the filing carrying no text
# layer at all (0 characters across 51 pages).
MNT_CARRYING = 15723.523
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
# ---- THE BRIDGE AS A RECORD OF CHOICES, NOT ONLY AS ARITHMETIC [R-BRIDGE-01] --------
# The delivered edition committed NO bridge record at all -- check_bridge.py reported
# "GBCO carries no bridge record" and the study sits on that ratchet (self-audit S-1).
# The bridge is where the whole two-sided answer lands and its construction was unrecorded,
# which is the point of the rule: the number a bridge produces cannot be checked by
# recomputing it, so the CHOICES are what get checked -- which sheet, on what basis the
# minority comes out, and whether the cash is charged for once or twice.
BRIDGE_RECORD = dict(
    _rule="[R-BRIDGE-01]",
    branch="the associate at its carrying value -- the branch every committed artefact in "
           "this study declares as its central; the round-price branch differs in ONE line "
           "and is published beside it",
    balance_sheet_date="2026-06-30",
    latest_disclosed_date="2026-06-30",
    latest_disclosed_source=(
        "engine/gbco_study/sweep_register.json, Company ring, 'official financial "
        "statements': GB Corp's REVIEWED consolidated interim statements at 30 June 2026 "
        "and its 2Q/1H26 earnings release of 13 August 2026, both obtained from the "
        "company's own investor-relations filings page (attempted and reachable, logged "
        "in the register's primary-access record)."),
    nci=dict(
        basis="value_share",
        applied_to="equity_value",
        deduction=auto_nci_value,
        proxy_source=(
            "GB Corp does not disclose which subsidiaries carry the GB Auto minority or "
            "what they earn, so the minority's SHARE is proxied by its proportion of the "
            "segment's own disclosed book equity -- EGP 590.7mn of 13,589.0mn, 2Q26 "
            "earnings release Table 12 as at 30 June 2026 -- and applied to the segment's "
            "equity VALUE. Both figures are the company's own and the segment balance "
            "sheet foots: 12,998.3 before minorities plus 590.7 is the stated 13,589.0."),
        share=AUTO_NCI_SHARE,
        book=AUTO_NCI_AT_BOOK,
        profit_share=AUTO_NCI_PROFIT_SHARE,
        proportional=AUTO_NCI_PROPORTIONAL,
        note=("BOOK IS PUBLISHED AS A REFERENCE FRAMING AND IS NOT THE ADOPTED BASIS. The "
              "delivered edition deducted book from a leg valued by capitalising 100% of "
              "that segment's cash flow, which hands the parent the minority's share of "
              "everything the model expects the segment to earn.")),
    cash=dict(
        treatment="added_at_face",
        weights_basis="gross",
        note=("The operations are discounted at a GROSS-debt-weighted rate and the cash is "
              "then netted inside the company's own net-debt figure. That is the "
              "value-the-whole-firm-and-add-the-cash construction, and it is the one this "
              "record names: the prohibited pair is cash added at face beside NET weights, "
              "which discounts the operations as though holding a deposit made them "
              "riskier and then counts the deposit at par as well.")),
    associates=dict(
        basis="book", listed=False,
        note=("MNT-Halan is UNLISTED, so no market price exists and 'book' here is the "
              "reviewed equity-accounted carrying value, EGP 15,723.523mn at 30 June 2026 "
              "on note 34's own arithmetic. The June-2026 round price is published as the "
              "SECOND BRANCH rather than as this line's basis, because it is a "
              "third-party mark GB Corp has never adopted -- and KPMG's review conclusion "
              "on these very statements is qualified on this investment.")),
    dividend=dict(deducted=False,
                  note="No dividend is declared after the balance-sheet date, so none is "
                       "deducted; the FY2025 distribution proposal is stated in note 10 as "
                       "awaiting the general assembly."),
    lines=[
        dict(name="GB Auto, enterprise value on its own cash flows", value=ev_auto),
        dict(name="less GB Auto net debt at 30 June 2026", value=-auto_nd),
        dict(name="less the minority's share of GB Auto equity value", value=-auto_nci_value),
        dict(name="plus GB Capital, the operating lender", value=cap_val),
        dict(name="plus the associates at their reviewed carrying value", value=assoc_carrying),
    ],
    equity_value=sotp_B,
    shares_mn=SH,
    per_share=sotp_B_ps,
)
import research_protocol as _RP_bridge                                 # noqa: E402
_RP_bridge.assert_bridge(BRIDGE_RECORD, 'GBCO')

# ---- THE RELATIVE MULTIPLE, NON-CIRCULAR AND OFF THE COMPANY'S OWN HISTORY ----------
# The delivered edition typed `np26 = 3300.0` with the comment "FY26E group NP" while the
# model's own consolidated forecast computes 3,297.5 four hundred lines above -- a hand
# rounded copy of a figure the model already had, which is exactly the typed financial
# numeral depth-bar standard 3 forbids in a builder. It is read from the forecast now.
np26 = GROUP[0]['net_profit']
# EARNINGS PER SHARE IS WHAT THE COMPANY PUBLISHES AS EARNINGS PER SHARE [audit finding
# 26]. The delivered edition divided profit attributable to the parent by the share count
# and captioned the row as the company's own reporting. It is not: note 10 to the audited
# statements deducts the employees' share of profit and the board of directors' bonus
# before dividing, and publishes 2.635 for FY2025 and 2.609 for FY2024 against 2.653 and
# 2.697 on the attributable line. A MULTIPLE AND ITS EARNINGS MUST BE ON ONE BASIS, so the
# historical multiples below are struck on the company's OWN published basic figure and
# the forecast earnings carry the same deduction.
#
#   note 10 (EGP 000)            FY2025      FY2024 reclassified
#   attributable to the parent   2 880 046   2 928 121
#   employees' share of profit           -     (76 549)
#   board of directors' bonus      (19 470)    (19 016)
#                                2 860 576   2 832 556
#   over 1,085,500 thousand shares   2.635       2.609
EPS_DEDUCTION_FY25 = (2880.046 - 2860.576) / 2880.046     # 0.676%
EPS_DEDUCTION_FY24 = (2928.121 - 2832.556) / 2928.121     # 3.264%, published beside it
# [R-ANCHOR-01]: the latest full year is the anchor and the earlier one is the other
# framing. The two differ by a factor of five because the employees' share follows the
# DISTRIBUTION and none was made in FY2025 -- so this is a contested judgement and both
# values are carried rather than averaged.
eps26 = np26 * (1 - EPS_DEDUCTION_FY25) / SH
eps26_fy24_framing = np26 * (1 - EPS_DEDUCTION_FY24) / SH
# The multiple was three typed judgement figures (8.0 / 9.5 / 11.0) sourced to nothing.
# [R-LENS-03] requires a relative multiple to be NON-CIRCULAR -- forward earnings times a
# multiple from peers or from the company's OWN HISTORY, never one read off the current
# price. GB Corp's own trailing multiple at its last three year-end closes, from its own
# reported net profit attributable and its own share price:
# year-end close against the company's OWN published basic earnings per share (FY2023
# annual report note 9; FY2024 and FY2025 annual report note 10), never a figure this
# desk constructed from the attributable line.
REL_HIST = {2023: (7.90, 1.682), 2024: (17.13, 2.609), 2025: (27.00, 2.635)}
_rel_pes = sorted(px / eps for px, eps in REL_HIST.values())
REL_PE_OWN = _rel_pes[len(_rel_pes) // 2]      # the median of three, and the COUNT is
                                               # published with it, because a percentage
                                               # without its count is the number that
                                               # misleads and so is a median of three
rel_ps = eps26 * REL_PE_OWN
rel = dict(bear=rel_ps, base=rel_ps, bull=rel_ps)
# THE TRADED MULTIPLE, COMMITTED SO THE CIRCULARITY CLAIM IS ARITHMETIC RATHER THAN PROSE
# [R-LENS-03]: a lens whose multiple IS the traded one values the company at what it
# already trades at, and a sentence saying otherwise is an attestation.
rel_traded_pe = spot / eps26
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
                  eps_deduction_fy25=EPS_DEDUCTION_FY25,
                  eps_deduction_fy24_framing=EPS_DEDUCTION_FY24,
                  eps26=eps26, eps26_fy24_framing=eps26_fy24_framing,
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
                 # RESTATED AGAINST RESTATED [audit finding 8] -- both figures committed
                 # so the workbook cannot quietly carry the as-released one.
                 segment_equity_before_nci_dec2025_as_released=(
                     CAP_FY25_EQ_BEFORE_NCI_AS_RELEASED),
                 associates_restatement_dec2025=ASSOC_RESTATEMENT_DEC25,
                 segment_equity_before_nci_dec2025=CAP_FY25_EQ_BEFORE_NCI,
                 associates_carried_within_dec2025=ASSOC_CARRYING_DEC25,
                 operating_equity_dec2025=cap_eq_dec25,
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
    # THE OPENING WORKING CAPITAL IS READ, NOT RETYPED. This line carried a literal
    # 18917.0 -- a second copy of WC_OPENING, correct on the day it was written and
    # silently wrong the moment the anchor moved to the 30-June-2026 stock. The grid's
    # own reproduction assertion is what caught it, which is the check working: the
    # carrying rung stopped reproducing the published branch within the same run.
    wcp = WC_OPENING
    for i, y in enumerate(yrs):
        r = fc[y]['auto_rev']
        op = r*(gpm[i]+gpm_shift) - r*gsa[i] + r*oth + r*prov
        dna = r*dna_pct[i]
        fcff = ((op*(1-TAX)+dna-capex[i]) * (STUB_FRACTION if i == 0 else 1.0)
                - (r*wc_pct[i]-wcp))
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
    # THE MINORITY IS A SHARE OF THIS LEG'S EQUITY VALUE, AND THE GRID HAS TO SAY SO TOO.
    # This line deducted the minority at BOOK while the bridge above deducts its share of
    # value, so the grid stopped reproducing the published branch the moment the basis
    # changed -- caught, again, by the grid's own reproduction assertion rather than by a
    # reader.
    ae = (pvs + tv_ - auto_nd) * (1.0 - AUTO_NCI_SHARE)
    # THE LENDER LEG IS cap_val, NOT cap_book. This line read cap_book, which was 9,500
    # when the case function was written and is now the leg's DISCLOSED BOOK FLOOR of
    # 6,267.3 — so every case built here was valuing the lender at book while the study
    # values it on residual income, and the rename would have carried that silently.
    # A variable whose meaning changed under a case function is the unit error [R-TERM-01]
    # names: nothing about the arithmetic looks wrong.
    # THE MARK MULTIPLE SCALES MNT-HALAN, NOT THE WHOLE ASSOCIATES BLOCK. It used to
    # multiply `assoc`, which carries the three small associates too — so the grid's
    # carrying rung came out at 41.1509 against a published branch of 41.3484, because it
    # was also marking Bedaia, Milo and Kaf down to 57% of a round they were never in.
    # The rungs are a claim about ONE holding and the arithmetic now says so.
    return (ae + cap_val*cap_m + mnt_halan_value*assoc_m + other_assoc)*(1-d)/SH
# Bear and bull terminal growth are REAL rates on the house path, never typed nominals
# [R-MACRO-01]: -0.5% and +0.5% real against the path's 7.0% terminal inflation.
TG_BEAR = _PATH.terminal_inflation - 0.005
TG_BULL = _PATH.terminal_inflation + 0.005
# A DIAGNOSTIC CASE PAIR, AND NOT THE PUBLISHED ENVELOPE — which is central_bear and
# central_bull, the min and max of the present-value reads, per [R-LENS-03]. These two flex
# the macro ladder as well as the business drivers, and that rule refuses such a construction
# as a published RANGE precisely because terminal growth and the terminal risk-free rate
# carry the same inflation, so the corners are internally contradictory. They are kept as an
# internal spread and are labelled here as one; the discount they used to carry is gone with
# the discount itself.
sotp_bear = sotp_case(-0.012, WACC+0.020, TG_BEAR, 0.80, 0.80, 0.0)
sotp_bull = sotp_case(+0.010, WACC-0.015, TG_BULL, 1.25, 1.20, 0.0)
dcf_lens = dict(bear=sotp_bear, base=prediscount_ps, bull=sotp_bull)
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
# THE SECOND AXIS WAS A COMPLEXITY DISCOUNT THIS STUDY NO LONGER APPLIES, so the grid
# priced a lever that is not in the model and its centre cell reproduced no published
# answer. It is re-pointed at the CRUX — the basis on which the associate is carried —
# and its rungs are EVIDENCED rather than evenly spaced: the two published branches, and
# the two haircuts the expert panel argues for in its own words. AN INTERPOLATED RUNG
# WOULD PRINT AN AVERAGE OF THE TWO BRANCHES WHILE CALLING IT A SENSITIVITY, which is the
# averaging the dual-framing rule forbids arriving through a grid.
grid_margin = [-0.02, -0.01, 0.0, 0.01, 0.02]
_mark_round = mnt_halan_value
# THE CARRYING RUNG IS THE RATIO ITSELF, NOT A ROUNDED COPY OF IT. A first draft rounded
# it to six places to keep the set tidy and then compared the rounded value against the
# unrounded ratio, so the rung that IS the published branch was labelled "57% of the round"
# — the one label in the grid that had to be right. Rounding a value and then testing it
# against its own source is the same shape as a check that reads what a process declares.
_mark_carry = MNT_CARRYING / _mark_round
grid_mark = sorted([0.50, _mark_carry, 0.75, 1.00])
grid_mark_labels = [("the reviewed carrying value" if m == _mark_carry else
                     "the June-2026 round price" if m == 1.00 else
                     "%.0f%% of the round" % (100 * m)) for m in grid_mark]
assert grid_mark_labels.count("the reviewed carrying value") == 1, (
    "the grid must carry the published branch as a rung, exactly once")
sens = [[sotp_case(mm, WACC, TG, 1.0, mk, 0.0) for mk in grid_mark]
        for mm in grid_margin]
# A GRID WHOSE RUNGS NAME THE PUBLISHED BRANCHES MUST REPRODUCE THEM. Asserted rather
# than assumed: the first draft came out 0.20 low on the carrying rung and the label was
# the only thing that would have told a reader, which is not a check.
_zero = grid_margin.index(0.0)
assert abs(sens[_zero][grid_mark.index(_mark_carry)] - sotp_B_ps) < 1e-9
assert abs(sens[_zero][grid_mark.index(1.00)] - sotp_A_ps) < 1e-9
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

import research_protocol as _RP

# ---- [R-FCAL-01] THE WALK-FORWARD SCOPE DECISION, STATED IN THE STUDY -----------------
# The rule has required this since 31-Aug-2026 and this study did not carry it, though the
# decision itself was made and written down where nobody outside the run would look: the
# pre-registration's own section 0. A decision recorded only in the place that acted on it
# is a decision no reader of the study can check.
_WF_SCOPE = dict(
    rule="R-FCAL-01",
    scope="FULL",
    sourceable_fiscal_years=14,
    earliest_sourceable="FY2012",
    basis=("this name's own walk-forward pre-registration, section 0: \"FULL. Fourteen "
           "sourceable fiscal years, FY2012-FY2025, every one tier A from a document "
           "the run holds\". Fourteen is at or above eight, so the FULL branch applies."),
    status="run",
    note=("The fundamental walk-forward HAS been run on this name: nine origins, FY2016 "
          "through FY2024, horizons one to five, 225 scored cells. NO correction was "
          "promoted into the live drivers. The finance-cost candidate is the one worth "
          "naming: its bias is large and its sign flips at four of six admissible cuts, "
          "so it fails the stability clause outright -- and it is also the trap the rule "
          "names by name, where a finance charge divided by a broader liabilities total "
          "manufactures a bias that looks exactly like evidence."))

# ---- [R-SIGCM-02] HOW EACH REVENUE LINE WAS ACTUALLY BUILT ---------------------------
# The ground-up clause is no longer attestable by a flag, and this study committed no
# driver record at all. The lines below cover 100% of the FIRST FORECAST YEAR's group
# revenue -- a line left out of the record is a line nobody checked -- and every one below
# unit level carries the gap rather than going quiet about it.
_F26 = GROUP[0]
_REV26 = _F26['revenue']
_DD = disclosed_drivers if 'disclosed_drivers' in dir() else None
_DL = [
    _RP.DriverLine(
        name="passenger cars", level="unit",
        share_of_revenue=fc['FY26E']['pc_rev'] / _REV26,
        unit="vehicles sold",
        unit_source=("GB Corp's own 4Q23, 4Q24 and 4Q25 earnings releases, the passenger-car "
                     "volume and revenue tables: 26,994 units on EGP 16,544.3mn, 42,043 on "
                     "36,533.4mn and 56,548 on 52,827.3mn"),
        price_basis=("the average selling price the same table implies, revenue divided by "
                     "its own units, across THREE disclosed years so the rate has an "
                     "observable trend rather than a single point"),
        cost_basis=("the auto leg's gross margin, held at the level the latest reviewed "
                    "half filed and drifting only where the company's own period pair "
                    "measures a direction")),
    _RP.DriverLine(
        name="commercial vehicles", level="unit",
        share_of_revenue=fc['FY26E']['cv_rev'] / _REV26,
        unit="vehicles sold",
        unit_source="the 4Q25 earnings release segment table: 3,404 units on EGP 5,956.8mn",
        price_basis=("revenue divided by its own units in that table. ONE DISCLOSED YEAR, "
                     "so the level is observable and its trend is not; the price is grown "
                     "at a stated rate rather than at a measured one"),
        cost_basis="the auto leg's gross margin, as above"),
    _RP.DriverLine(
        name="motorcycles and three-wheelers", level="unit",
        share_of_revenue=fc['FY26E']['lm_rev'] / _REV26,
        unit="units sold",
        unit_source="the 4Q25 earnings release segment table: 33,906 units on EGP 2,203.8mn",
        price_basis=("revenue divided by its own units in that table. ONE DISCLOSED YEAR, "
                     "as above"),
        cost_basis="the auto leg's gross margin, as above"),
    _RP.DriverLine(
        name="tyres, parts and trading", level="segment",
        share_of_revenue=fc['FY26E']['tr_rev'] / _REV26,
        cost_basis="the auto leg's gross margin, as above",
        gap_note=("NO UNIT IS DISCLOSED. The releases give this activity's revenue as a "
                  "segment line and publish neither a volume nor a price for it, so the "
                  "build stops at the segment and says so rather than inventing a unit. "
                  "It is grown on a stated rate; that rate is not measured against "
                  "anything the company publishes.")),
    _RP.DriverLine(
        name="other and inter-segment auto revenue", level="topdown",
        share_of_revenue=fc['FY26E']['of_rev'] / _REV26,
        cost_basis=("the auto leg's gross margin, which is the margin this line is ALREADY "
                    "inside: the release strikes GB Auto's 14.8% on TOTAL revenue of "
                    "66,358.3, so applying that margin to a revenue figure that omits this "
                    "line is what understated gross profit in the delivered edition"),
        gap_note=("NEITHER A UNIT NOR A SEGMENT IS DISCLOSED FOR IT, and it is not one "
                  "activity: EGP 682.8mn is GB Auto's external revenue outside its four "
                  "published business lines (65,913.5 less 65,230.7), which the release's "
                  "own tables head 'Sales AND AFTER-SALES Activity' without ever publishing "
                  "the after-sales revenue separately; EGP 444.8mn is inter-segment revenue, "
                  "real to this segment and removed again by the group elimination line. It "
                  "is HELD FLAT at its own filed level rather than grown, because the "
                  "company publishes no volume, price or growth rate for it and a growth "
                  "rate nothing measures is worse than no growth rate. THE DELIVERED "
                  "EDITION ZEROED IT for every forecast year [audit finding 5].")),
    _RP.DriverLine(
        name="GB Capital (the financing businesses)", level="segment",
        share_of_revenue=_F26['capital_revenue'] / _REV26,
        cost_basis=("the segment's own gross margin, which its income-statement table "
                    "discloses in full -- cost of sales and cost of funds separately"),
        gap_note=("BUILT ON THE SEGMENT TOTAL WHILE A FINER SPLIT IS DISCLOSED, and that "
                  "is the honest statement of it: Table 13 of each release breaks this "
                  "revenue down by company -- GB Lease, Drive, GB Auto Rental, GBBR, "
                  "Capital Securitization, Kredit -- and the model consumes the total. "
                  "No UNIT is disclosed for any of them (a lending business's unit would "
                  "be portfolio times a rate, and the portfolio is disclosed only in "
                  "total), so a finer build would still not reach unit level; what it "
                  "would reach is six growth paths instead of one, which is a real "
                  "improvement this record names rather than hides.")),
    _RP.DriverLine(
        name="intersegment eliminations", level="topdown",
        share_of_revenue=_F26['eliminations'] / _REV26,
        cost_basis=("the eliminated sales are reversed WITH their own cost, at a stated "
                    "20% gross margin on the eliminated revenue. THAT PROPORTION IS TYPED "
                    "RATHER THAN DISCLOSED and is named here as such: the releases publish "
                    "the elimination as a single revenue figure and never split it, so the "
                    "cost reversed with it cannot be sourced. It is the one line in this "
                    "record whose cost side rests on a chosen number, and it is 1.1% of "
                    "group revenue."),
        gap_note=("A CONTRA RATHER THAN A REVENUE LINE, carried here so the record covers "
                  "the whole of group revenue: a line omitted is a line nobody checked. "
                  "It is a percentage of the two legs' combined revenue, and the releases "
                  "disclose the elimination only as a single figure, so there is nothing "
                  "finer to build it from.")),
]
_GROUND_UP = _RP.assert_ground_up(_DL, 'GBCO')

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
            # READ, NOT TYPED. Both ends were typed literals and both went stale in this
            # pass: the carrying value moved when note 34 was re-read off the pixels and
            # the round value moved when the currency came from the house path.
            low=MNT_CARRYING, high=mnt_halan_value,
            units="EGP million, the associate holding",
            macro_held=True,
            evidence=("THE TWO ENDS ARE NOT THE SAME KIND OF NUMBER, AND AN EARLIER "
                      "EDITION OF THIS RECORD SAID THEY WERE. The low end is GB Corp's "
                      "OWN: note 34 to the reviewed consolidated interim statements at 30 "
                      "June 2026, EGP %s thousand, every column and row of which foots on "
                      "this reading and on no other. The high end is a THIRD-PARTY MARK "
                      "the company has never adopted as its own carrying value -- %.2f%% "
                      "of the USD %s mn primary round completed with Al Ahly Capital "
                      "Holding, which GB Corp's 9 June 2026 release names for the STAKE "
                      "and not for the round figure, translated at the house path's own "
                      "USD/EGP %.2f of %s. The macro path stood still across the range: "
                      "nothing in it moves inflation, the currency or the price of time. "
                      "THE REVIEW CONCLUSION ON THOSE STATEMENTS IS QUALIFIED AT EXACTLY "
                      "THIS LINE -- the reviewers were not provided with the associate's "
                      "own financial statements and could not verify the EGP %s mn share "
                      "of profit recorded in the period -- so the low end is not a safe "
                      "harbour either, and the study says so rather than resting on it."
                      % (format(MNT_CARRYING * 1000, ',.0f'), 100 * mnt_halan_stake,
                         format(mnt_halan_round_usd, ',.0f'), egp_usd, EGP_USD_DATE,
                         format(409.985, ',.3f'))),
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
             # THE METRIC IS THE EARNINGS THE MULTIPLE IS ACTUALLY APPLIED TO, WHICH IS
             # NOT THE ATTRIBUTABLE LINE. The multiples in REL_HIST are struck on the
             # company's OWN PUBLISHED BASIC EPS, whose numerator is net profit
             # attributable LESS the employees' and board statutory share of profit
             # (EPS_DEDUCTION_FY25, 0.676% on the FY2025 framing). This block committed
             # the raw attributable figure while the lens multiplied the EPS-basis one,
             # so the two disagreed by exactly that deduction and NOTHING SAID SO -- the
             # committed operand named a different quantity from the one in use, which is
             # the same shape as an artefact declaring a vintage it was not built at.
             # It broke twice from one cause: `multiple x metric_value / shares` gave
             # 18.2024 against a published 18.0794, and research_protocol's own derived
             # `_traded_multiple` came out 10.4533 against the 10.52x this study PRINTS.
             # Committing the operand the lens uses closes both; no printed figure moves.
             circularity=dict(spot=spot, shares=SH, net_debt=0.0,
                              metric_value=np26 * (1 - EPS_DEDUCTION_FY25),
                              metric_basis=("FY2026E net profit attributable LESS the "
                                            "employees' and board statutory share of "
                                            "profit -- the SAME basis as the company's "
                                            "own published basic earnings per share, "
                                            "which is the denominator every multiple in "
                                            "this lens's own history was struck on"),
                              net_profit_attributable=np26),
             note=("earnings multiple, so the enterprise adjustment is nil by "
                   "construction and the traded multiple is simply market "
                   "capitalisation over the same forward earnings -- on the earnings "
                   "basis the multiple is struck on, never the attributable line.")),
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
             auto_total_eq=auto_total_eq, auto_nci_share=AUTO_NCI_SHARE,
             working_capital_opening=WC_OPENING, working_capital_anchor=WC_ANCHOR,
             auto_nci_value=auto_nci_value, unearned_fraction=STUB_FRACTION,
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
    forecast=fc, gpm=gpm, sens=dict(grid_margin=grid_margin, grid_mark=grid_mark,
                            grid_mark_labels=grid_mark_labels, table=sens,
                            axis=("the auto leg's gross-margin shift against the basis on which the associate is carried; the centre-right cell IS the round-price branch and the carrying-value rung IS the other branch")),
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
                        working_capital_pct=wc_pct, working_capital_opening=WC_OPENING,
                        working_capital_opening_intensity=WC_OPENING / WC_TTM_REV,
                        working_capital_base_intensity=WC_BASE_INTENSITY,
                        working_capital_ttm_revenue=WC_TTM_REV,
                        working_capital_closing_fy30e=wc_prev,
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
                     # THE WORKBOOK'S WORKING CAPITAL IS THE MODEL'S WORKING CAPITAL,
                     # COMPONENT BY COMPONENT. These four ratios were a typed glide and
                     # they are a SECOND IMPLEMENTATION of the quantity L15 re-anchored --
                     # the delivered workbook projected its balance sheet from them while
                     # the cash-flow model used wc_pct, and the study's own recalculation
                     # gate is what caught the two disagreeing after the anchor moved.
                     # They are now the company's OWN disclosed components at 30 June 2026
                     # over the same trailing-twelve-month revenue, held flat on the same
                     # [R-ANCHOR-01] reasoning, and they reproduce WC_ANCHOR by identity:
                     #   30.326 + 7.758 + 4.957 - 20.463 = 22.578%
                     auto_inventory_pct=[22959.1 / WC_TTM_REV] * 5,
                     auto_receivables_pct=[5873.5 / WC_TTM_REV] * 5,
                     auto_advances_pct=[(1153.7 + 2598.9) / WC_TTM_REV] * 5,
                     auto_payables_pct=[15492.5 / WC_TTM_REV] * 5,
                     auto_working_capital_pct=wc_pct,
                     auto_unearned_fraction=STUB_FRACTION,
                     net_new_borrowings=[5500.0, 5200.0, 5600.0, 5800.0, 6100.0],
                     dividend_payout=[0.14, 0.15, 0.16, 0.18, 0.20])),
    bridge_record=BRIDGE_RECORD,
    lens_inputs=LENS_INPUTS,
    # THE EDITION IS THE DAY THE WORK WAS DONE. This re-issue answers the forensic
    # audit of the 07-09-2026 edition and moves the published answer, so it is a new
    # edition rather than a restamp of the old one.
    edition='2026-09-17',
    experts=dict(e1=exp1, e2=exp2, e3=exp3, e3_roce=roce, e3_ce=ce),
    # ---- WHAT THIS STUDY COMMITS ABOUT THE ANSWER ITSELF, beyond the answer ----------
    audit_2026_09_17=dict(
        _what="the figures the 17-09-2026 audit response needed and the study did not carry",
        # finding 6 -- the historical operating-profit line and the basis break beneath it
        operating_profit_basis_break=dict(
            what="GB Corp's own 'Operating Profit' line EXCLUDED provisions in its FY2023 "
                 "presentation and INCLUDES them from FY2024. Both years' figures are the "
                 "company's own and they are not on one basis.",
            fy2023_as_reported=HISTORY['income_statement']['2023']['operating_profit'],
            fy2023_on_the_current_basis=_FOOTED_OP['2023'],
            fy2024_as_first_reported=HISTORY['income_statement']['2024']['operating_profit'],
            fy2024_as_restated=_FOOTED_OP['2024'],
            fy2025=_FOOTED_OP['2025'],
            footed_operating_profit=_FOOTED_OP,
            evidence="The study's own committed EBIT proves which basis is which: FY2023 "
                     "EBIT of 4,769.7 less associates of 1,061.7 is 3,708.0, and FY2024's "
                     "6,688.5 less 867.6 is 5,820.9 -- the footed figures, not the printed "
                     "ones. GB Corp's 4Q/FY25 release prints FY2024 operating profit as "
                     "5,820.8 in its own Table 1."),
        # finding 12 -- the life the terminal's own capital charge implies
        terminal_capex_to_dna=capex[-1] / rows[-1]['dna'],
        terminal_capex=capex[-1],
        terminal_dna=rows[-1]['dna'],
        disclosed_life_range=[10.9, 17.1],
        implied_life_note=(
            "The asset-life refusal is honest and the construction pins a charge anyway. "
            "In the terminal year this model spends %.2f times its own book depreciation "
            "on capital expenditure. A company replacing its asset base over the 10.9-to-"
            "17.1-year composite the filings support would spend about book depreciation "
            "grossed for cost inflation, so the terminal is charging ABOVE replacement "
            "rather than below it -- which is the one direction [R-TERM-01 CLAUSE TWO]'s "
            "inference runs without a sourced life."),
        # finding 25 -- the company's own return for the same segment
        capital_return_disclosed=dict(
            fy2025=0.151, h1_2026=0.135,
            basis="GB Corp's own adjusted return on average equity for the GB Capital "
                  "segment, as published in its 4Q25 and 2Q26 earnings releases.",
            why_not_adopted=(
                "Its numerator includes EGP 986.4mn of investment gains from associates and "
                "its denominator is an equity base those associates sit inside. Importing it "
                "would count MNT-Halan once in the lender leg and again as the sum of the "
                "parts' largest single line. The study's 10.10% takes the associate out of "
                "both, which is why the two figures differ and why the company's is printed "
                "here rather than adopted.")),
        # finding 32 -- the currency, and what it was before
        egp_usd=egp_usd, egp_usd_date=EGP_USD_DATE,
        egp_usd_typed_before=EGP_USD_TYPED_BEFORE,
        # finding 21 -- the scenario span the workbook prints and the document did not
        # finding 21 -- the scenario span the workbook prints and the document did not
        scenario_span=dict(
            low=sotp_bear, high=sotp_bull,
            what="the study's own committed scenario reads on the primary: a gross-margin "
                 "shift, the WHOLE cost-of-capital ladder moved together, terminal growth "
                 "shifted in REAL terms, and the marks on the lender and the associates "
                 "moved with them -- a stress on the model at once rather than one driver "
                 "at a time.",
            why_it_is_not_the_envelope=(
                "[R-LENS-03]'s envelope is the RANGE OF THE PRESENT-VALUE READS, which is a "
                "different object: the two branches and the relative cross-check. This span "
                "is a stress on ONE of those reads and sits outside the envelope on both "
                "sides, which is why the delivered workbook printed it and the document did "
                "not. It is published in both from this edition rather than in one.")),
    ),
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
               # THE TERMINAL ANCHORS, COMMITTED SO THE WORKBOOK CAN BUILD THE TERMINAL
               # RATE AS A FORMULA RATHER THAN CARRY IT AS A CONSTANT [audit finding 18].
               real_rate_convention=_PATH.real_rate_convention,
               erp_terminal=_PATH.erp_terminal,
               kd_terminal=_PATH.kd_terminal,
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
    walkforward_scope=_WF_SCOPE,
    driver_lines=[vars(l) for l in _DL],
    ground_up=_GROUND_UP,
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
