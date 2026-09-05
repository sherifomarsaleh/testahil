"""STC study — master computation. Outputs study_numbers.json + backtest tables.
Saudi Telecom Company (Tadawul: 7010).

Price history comes from the PERSISTENT LIBRARY at engine/raw_ohlc/SA/STC.csv, which is
the file the whole engine reads for this name. The study previously carried its own
one-off export beside it; a study-local copy of a series the library already holds is a
second source for one fact, and the two drift apart the moment either is refreshed.
"""
import json
import os
import sys

import numpy as np
import pandas as pd
import primitives as m
from wacc_builder import WaccInputs, build_wacc, RegressionBetaAttempt

HERE = os.path.dirname(os.path.abspath(__file__))
OHLC = os.path.join(HERE, '..', 'raw_ohlc', 'SA', 'STC.csv')

df = m.load_ohlc(OHLC)
close = df['Price'].values
spot = float(close[-1])
spot_date = str(df['Date'].iloc[-1].date())
N = len(df)

# ---------------- Step 0 backtest (zero drift = house default for non-EGX) ---
res, summ = m.backtest(df, horizon=60, secular_drift=False)          # adopted config
res_sec, summ_sec = m.backtest(df, horizon=60, secular_drift=True)   # rejected diagnostic
res21, summ21 = m.backtest(df, horizon=60, step=21, secular_drift=False)
pit_hist = np.histogram(res['pit'], bins=10, range=(0, 1))[0].tolist()
# block bootstrap CI on CRPS skill (n windows, resample with replacement)
rng_bs = np.random.default_rng(7)
sk = []
c, cb = res['crps'].values, res['crps_bench'].values
for _ in range(4000):
    idx = rng_bs.integers(0, len(c), len(c))
    sk.append(1 - c[idx].sum() / cb[idx].sum())
sk = np.array(sk)
boot = dict(lo90=float(np.percentile(sk, 5)), hi90=float(np.percentile(sk, 95)),
            p_pos=float(np.mean(sk > 0)))

# ---------------- Forward run parameters ------------------------------------
v = m.yz_variance_proxy(df)
beta_har = m.fit_har(v, N - 1, horizon=60)
dv = m.har_forecast_daily_var(v, N - 1, beta_har, horizon=60)
anchor_vol = float(np.sqrt(dv * 252))
drift_daily = 0.0   # zero-drift class: international/GCC name (Step 0-adopted)

# ---------------- 16-factor stack (7 continuous + 9 discrete) ---------------
continuous = [
    ("SAMA/Fed policy-rate path (easing)", "+"),
    ("Oil price / fiscal impulse (govt ICT & mega-project spend)", "+"),
    ("Vision 2030 / non-oil GDP digital demand", "+"),
    ("KSA mobile competition (Mobily/Zain share & price pressure)", "−"),
    ("Data-centre / AI buildout economics (center3–HUMAIN)", "±"),
    ("Subsidiary drag→contribution (stc bank, solutions, intl)", "±"),
    ("TASI flows / index weight (free float 38%)", "±"),
]
cont_drift_q = 0.002
discrete = [
    ("2Q26 results (~late Jul 2026)",                  0.90, 0.004),
    ("Special dividend announced with 2Q/3Q results",  0.20, 0.020),
    ("SAMA/Fed cut ≥25bp (Sep/Oct)",                   0.55, 0.006),
    ("center3/HUMAIN AI-DC milestone (toward 1GW)",    0.35, 0.010),
    ("TAWAL/DIIC monetization event",                  0.10, 0.015),
    ("Telefónica mark deterioration spillover",        0.25, -0.006),
    ("KSA mobile price-war escalation / weak prints",  0.20, -0.015),
    ("Regional geopolitical escalation",               0.25, -0.020),
    ("PIF further sell-down / index-flow event",       0.10, -0.012),
]
disc_drift_q = sum(p * i for _, p, i in discrete)
factor_drift_q = cont_drift_q + disc_drift_q

# ---------------- Forward simulation (50,000 paths, seed 42) ----------------
H = 60
rng = np.random.default_rng(42)
n_paths = 50000
sd = np.sqrt(dv)
z = rng.standard_normal((n_paths, H))
chi = rng.chisquare(5, n_paths)
mix = np.sqrt(3.0 / chi)[:, None]
incr = drift_daily + cont_drift_q / H + z * mix * sd
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
levels = [50, 48, 46, 44, 42, 40, 38, 36]
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
zones_edges = [0, 38, 42, 46, 50, 1e9]
zone_probs = [float(np.mean((pT60 >= a) & (pT60 < b))) for a, b in zip(zones_edges[:-1], zones_edges[1:])]
fan = {p: np.percentile(paths, p, axis=0).tolist() for p in pcts}

# ---------------- Technicals -------------------------------------------------
s = pd.Series(close)
sma = {n_: float(s.rolling(n_).mean().iloc[-1]) for n_ in [20, 50, 100, 200]}
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
chg20 = float(close[-1]/close[-21]-1); chg60 = float(close[-1]/close[-61]-1)

# ---------------- Valuation model -------------------------------------------
SH = 4989.8          # mn shares outstanding net of ~10.2mn treasury (5,000 issued)
TAX = 0.097          # normalized effective zakat+tax (FY23 9.5%, FY24 9.8%; FY25 −3.2% one-off credit)
MKTCAP = spot * SH

# ===== Historical anchors (stc.com IR releases; restated continuing-ops) =====
hist = dict(
    rev={'FY23': 71777.0, 'FY24': 75893.0, 'FY25': 77819.0},
    gp={'FY23': 34740.0, 'FY24': 37326.0, 'FY25': 37700.0},
    ebitda={'FY23': 22445.0, 'FY24': 23951.0, 'FY25': 24469.0},
    ebit={'FY23': 13161.0, 'FY24': 14426.0, 'FY25': 14438.0},
    np_att={'FY23': 13295.0, 'FY24': 24689.0, 'FY25': 14828.0},
    np_cont_att={'FY23': 12536.0, 'FY24': 10716.0, 'FY25': 14828.0},  # ex-discontinued (FY24 incl. 13,973 disc-ops; FY23 759)
    assets={'FY23': 159646.0, 'FY24': 160638.0, 'FY25': 157477.0},
    cash={'FY23': 28138.0, 'FY24': 30755.0, 'FY25': 15080.0},
    debt={'FY23': 21958.0, 'FY24': 15132.0, 'FY25': 15191.0},
    eq_att={'FY23': 78985.0, 'FY24': 89417.0, 'FY25': 83414.0},
    nci={'FY23': 2530.0, 'FY24': 3069.0, 'FY25': 3482.0},   # FY25 primary (Q1-26 FS comparative); FY23/24 estimated
    ocf={'FY23': 22418.0, 'FY24': 19885.0, 'FY25': 18283.0},
    fcf={'FY23': 12628.0, 'FY24': 7959.0, 'FY25': 6488.0},
    capex={'FY23': 9790.0, 'FY24': 11927.0, 'FY25': 11795.0},
    dna={'FY23': 9284.0, 'FY24': 9525.0, 'FY25': 10031.0},  # EBITDA − EBIT (both disclosed)
    dps={'FY23': 1.60, 'FY24': 3.75, 'FY25': 2.20},         # FY24 incl. SAR 2.00 special (paid 2025)
)
# Segment history (stc.com FY25 presentation; FY24 restated)
seg_hist = dict(
    ksa_cbu={'FY24': 31741.0, 'FY25': 32826.0},
    ksa_ebu={'FY24': 13466.0, 'FY25': 13514.0},
    ksa_wc={'FY24': 4313.0, 'FY25': 4779.0},
    ksa={'FY24': 49644.0, 'FY25': 51119.0},
    subs={'FY24': 26249.0, 'FY25': 26700.0},   # group − KSA (net of eliminations)
)

# ===== Forecast drivers (top-down, §3.5-C: subs×ARPU not disclosed → normalized margins) =====
yrs = ['FY26E', 'FY27E', 'FY28E', 'FY29E', 'FY30E']
g_cbu = [0.030, 0.028, 0.025, 0.022, 0.020]
g_ebu = [0.020, 0.035, 0.040, 0.040, 0.035]
g_wc  = [0.060, 0.050, 0.040, 0.035, 0.030]
g_sub = [0.060, 0.058, 0.052, 0.047, 0.042]
ebitda_m = [0.318, 0.320, 0.322, 0.323, 0.325]
dna_pct  = [0.129, 0.128, 0.127, 0.126, 0.125]
capex_pct = [0.165, 0.165, 0.160, 0.155, 0.150]   # guidance band 15–17.5%, edging up 2026–27
wc_out_pct = [0.008, 0.006, 0.005, 0.004, 0.004]  # net WC/OCF-conversion drag as % of revenue (receivables-led; FY25 conversion gap)
payout_dps = [2.20, 2.20, 2.30, 2.40, 2.55]       # policy 0.55/q locked to Q3-27, then growing

fc = {}
cbu, ebu, wc_, sub = seg_hist['ksa_cbu']['FY25'], seg_hist['ksa_ebu']['FY25'], seg_hist['ksa_wc']['FY25'], seg_hist['subs']['FY25']
for i, y in enumerate(yrs):
    cbu *= (1 + g_cbu[i]); ebu *= (1 + g_ebu[i]); wc_ *= (1 + g_wc[i]); sub *= (1 + g_sub[i])
    fc[y] = dict(cbu=cbu, ebu=ebu, wc=wc_, ksa=cbu + ebu + wc_, sub=sub, rev=cbu + ebu + wc_ + sub)

# ===== Cost of capital — the sanctioned schedule [R-COC-01] ==================
# The whole ladder comes from engine/cost_of_capital.py through this study's own
# coc_run.py, which reads the debt book facility by facility out of note 26 and the
# finance cost out of note 39/40. Nothing about the rate is typed here: the risk-free
# is normalised by Saudi Arabia's OWN default spread so country risk is counted once,
# the weights are market-value, and the schedule is FLAT because the riyal is pegged
# and today is already the terminal — stated by the module rather than assumed here.
#
# The beta is re-derived live through beta_regression.own_stock_beta against TASI, the
# published index of the exchange this stock is listed on. It replaces a 40-session
# DAILY regression, which the standing rule says is not one of the three tiers at all;
# the module refuses to build on a non-conforming tier-1 beta, which is why the
# schedule and the beta land in the same pass.
import coc_run as COCRUN

# A sensitivity run rebuilds the schedule on a stated beta and prints the answer without
# writing anything, so the rebuild ledger can measure what the beta correction alone was
# worth rather than assert a direction for it.
_SENS_BETA = float(sys.argv[sys.argv.index('--beta') + 1]) if '--beta' in sys.argv else None

# WHICH LEVERS OF THE REBUILD PLAN ARE IN THIS FILE. Declared in one place so an artefact
# can state the state it was struck in, and so a measurement taken at one point in the
# rebuild cannot be silently overwritten by a later one: the sensitivity artefact is NAMED
# for its lever set, and a run with more levers in writes a different file rather than
# replacing a number the ledger is chaining through. [R-ENF-06]
LEVERS_APPLIED = ['mechanical', 'R-COC-01', 'R-BETA-04', 'R-MACRO-01']
SENS_TAG = 'after_coc'      # the lever set the retired-beta measurement belongs to

SCHED = COCRUN.build(beta_value=_SENS_BETA, erp_basis='market')  # swap basis, CENTRAL
SCHED_RATING = COCRUN.build(beta_value=_SENS_BETA, erp_basis='rating')
BETA = _SENS_BETA if _SENS_BETA is not None else COCRUN.BETA.beta

WACC = SCHED.wacc_exp
WACC_RATING = SCHED_RATING.wacc_exp
KE_RATING, KE_MARKET = SCHED_RATING.ke_exp, SCHED.ke_exp
KD_AT = SCHED.kd_aftertax
WE, WD = SCHED.weight_equity, SCHED.weight_debt
DF = list(SCHED.discount_factors)                 # one date, one price of time
DF_TERMINAL = SCHED.terminal_discount_factor
WACC_TERMINAL = SCHED.wacc_terminal

# Terminal growth is STORED AS A REAL RATE AND RECOMPUTES TO ITS NOMINAL on the house
# Saudi path [R-MACRO-01]. The delivered study typed 2.5% nominal, which is unfalsifiable:
# nobody can tell from the page whether it meant terminal inflation plus half a point or
# something else. The real growth is the rule's own STATED DEFAULT OF ZERO — a mature
# domestic telecom growing with the economy in perpetuity and no further — because any
# other figure would have to be sourced and nothing in the filings supplies one, and
# reverse-engineering the real rate that reproduces the typed 2.5% would be keeping the
# number and inventing a reason for it.
TG_REAL = 0.0
TG = COCRUN.MACRO.terminal_growth(TG_REAL)      # = terminal inflation + the stated real

# ===== DCF (FCFF, full build) =================================================
rows = []
for i, y in enumerate(yrs):
    r = fc[y]['rev']
    ebitda = r * ebitda_m[i]
    dna = r * dna_pct[i]
    ebit = ebitda - dna
    nopat = ebit * (1 - TAX)
    capex = r * capex_pct[i]
    dwc = r * wc_out_pct[i]
    fcff = nopat + dna - capex - dwc
    rows.append(dict(year=y, rev=r, ebitda=ebitda, dna=dna, ebit=ebit, nopat=nopat,
                     capex=capex, dwc=dwc, fcff=fcff))
for i, rw in enumerate(rows):
    rw['df'] = DF[i]
    rw['pv'] = rw['fcff'] * rw['df']
pv_sum = sum(rw['pv'] for rw in rows)

# ===== The terminal, through the sanctioned module [R-TERM-01] ===============
# The retired construction charged g x IC every year for ever, which reads as a capital
# maintenance programme with a replacement cycle of 1/g — a fact about the currency and
# not about the asset. At a pegged 2% terminal that is FIFTY YEARS against a base whose
# own accounts run twenty-one, so it bought half the maintenance this company needs. It
# also never added book depreciation back although NOPAT is already net of it, so one
# model carried two definitions of free cash flow with the terminal holding most of the
# value.
#
# The life and the age are DERIVED from note 10's own roll-forward by the identity the
# protocol already sanctions, because this company discloses RANGES rather than a single
# life. All three conditions that break that identity were checked on the policy note
# first and all three are clear; the working is in TERMINAL_EVIDENCE_05-09-2026.md.
import terminal_value as TVM

TERM_LIFE = 134_634_729 / 6_453_343          # depreciable gross cost over the year's charge
TERM_AGE = 98_254_770 / 6_453_343            # accumulated depreciation over the same charge
# Net working capital from the LATEST DISCLOSED balance sheet, 30 June 2026, reviewed:
# inventories, contract assets and trade receivables less trade and other payables and
# contract liabilities. SAR millions, to match the model.
TERM_WC = (1_781_441 + 9_971_423 + 26_727_997 - 21_198_207 - 3_727_610) / 1000.0
# Capital per unit of REAL growth, used ONLY where the sensitivity grid moves terminal
# growth off the house terminal inflation. The base case states real growth of zero and
# is charged no growth capital at all, so this figure shapes the grid and never the
# answer. It is the depreciable gross base at CURRENT cost — the same escalation the
# maintenance charge uses, so the grid cannot quietly price growth on a historical base
# while maintenance is priced on a current one.
TERM_IC_PER_UNIT_GROWTH = (134_634_729 / 1000.0) * (1.0 + 0.02) ** (98_254_770 / 6_453_343)

_t = TVM.build(TVM.TerminalInputs(
    nopat=rows[-1]['nopat'],
    wacc=WACC_TERMINAL,
    inflation=COCRUN.MACRO.terminal_inflation,
    real_growth=TG_REAL,
    dna_book=rows[-1]['dna'],
    maintenance_basis='book_dna_escalated',
    average_age_years=TERM_AGE,
    average_age_source=(
        "Note 10 of the FY2025 audited statements, the property and equipment "
        "roll-forward: accumulated depreciation of SAR 98,254,770 thousand over the "
        "year's own charge of SAR 6,453,343 thousand. An identity off the accounts, not "
        "a figure this desk chose, and the same note gives 14.18 and 13.60 years on the "
        "two years behind it."),
    useful_life_years=TERM_LIFE,
    useful_life_source=(
        "Derived from note 10 of the FY2025 audited statements: depreciable gross cost of "
        "SAR 134,634,729 thousand — total cost of 141,541,105 less capital work in "
        "progress of 4,910,376 and land of 1,996,000, both disclosed separately in the "
        "same note — over the year's own charge of SAR 6,453,343 thousand. The company "
        "discloses RANGES rather than one life (buildings 25-50 years, telecommunication "
        "network and equipment 3-30, other assets 2-20, note 4.11), so a single figure has "
        "to come from the identity; 19.54 and 19.84 years stand behind it on the two "
        "earlier filed years."),
    working_capital=TERM_WC,
))
tv = _t.tv
pv_tv = tv * DF_TERMINAL
ev = pv_sum + pv_tv
# EV → equity bridge (marks)
assoc = 4641.0        # investments in associates & JVs, 31-Dec-25 FS (incl. 43.06% DIIC/TAWAL)
telefonica = 8630.0   # 9.97% Telefónica at €3.50 (6-Jul-26): 561mn sh × €3.50 × 4.40 SAR/EUR ≈ SAR 8.6bn (cost €2.1bn ≈ 8.5bn)
net_debt = 7063.0     # Q1-26 IR basis (total debt 22,475 − IR cash 15,412, excl. stc bank cash 6.0bn)
nci_v = 2335.0        # NCI book, 31-Mar-26 FS
eq_dcf = ev + assoc + telefonica - net_debt - nci_v
dcf_ps = eq_dcf / SH

def dcf_ps_at(wacc, g, ebitda_shift=0.0, capex_shift=0.0):
    pv = 0.0
    for i, y in enumerate(yrs):
        r = fc[y]['rev']
        ebitda_ = r * (ebitda_m[i] + ebitda_shift)
        dna_ = r * dna_pct[i]
        nopat_ = (ebitda_ - dna_) * (1 - TAX)
        fcff_ = nopat_ + dna_ - r * (capex_pct[i] + capex_shift) - r * wc_out_pct[i]
        pv += fcff_ / (1 + wacc) ** (i + 1)
        if i == 4:
            fcff5, nopat5, dna5 = fcff_, nopat_, dna_
    # THE SENSITIVITY MUST USE THE SAME TERMINAL AS THE BASE. A grid centred on a
    # construction the study does not publish grades a different model, which is the
    # defect one of this house's own studies shipped when its base call site was
    # corrected and its sensitivity engine was not.
    tv_ = TVM.build(TVM.TerminalInputs(
        nopat=nopat5, wacc=wacc, inflation=COCRUN.MACRO.terminal_inflation,
        real_growth=(1.0 + g) / (1.0 + COCRUN.MACRO.terminal_inflation) - 1.0,
        dna_book=dna5, maintenance_basis='book_dna_escalated',
        average_age_years=TERM_AGE, average_age_source='see the base call site',
        useful_life_years=TERM_LIFE, useful_life_source='see the base call site',
        working_capital=TERM_WC,
        incremental_capital_per_unit_growth=(
            None if abs((1.0 + g) / (1.0 + COCRUN.MACRO.terminal_inflation) - 1.0) < 1e-12
            else TERM_IC_PER_UNIT_GROWTH),
    )).tv
    pvtv = tv_ / (1 + wacc) ** 5
    return (pv + pvtv + assoc + telefonica - net_debt - nci_v) / SH

# ===== DDM (cash-flow cross-check: the locked 0.55/q policy) ==================
KE = KE_RATING
pv_div = sum(payout_dps[i] / (1 + KE) ** (i + 1) for i in range(5))
# The dividend lens carried its OWN terminal growth of 3.0% against the cash-flow lens's
# 2.5%, in the same model, on the same company, in the same economy — two answers to one
# question, which is the incoherence [R-MACRO-01] exists to close. It sits on the same
# path at the same stated real rate: a dividend cannot grow faster than the business that
# pays it, in perpetuity.
tg_div = COCRUN.MACRO.terminal_growth(TG_REAL)
tv_div = payout_dps[-1] * (1 + tg_div) / (KE - tg_div)
pv_tv_div = tv_div / (1 + KE) ** 5
ddm_ps = pv_div + pv_tv_div
ddm_tv_pct = pv_tv_div / ddm_ps

# ===== Relative & Normalized ==================================================
ebitda26 = rows[0]['ebitda']
np26 = (rows[0]['ebit'] + 500 + 200) * (1 - TAX) * (1 - 0.025)   # attributable: + assoc 0.5 + net fin 0.2, − 2.5% NCI
eps26 = np26 / SH
rel_evx = dict(bear=8.0, base=9.0, bull=10.0)
rel = {}
for k, x in rel_evx.items():
    ev_r = ebitda26 * x
    rel[k] = (ev_r + assoc + telefonica - net_debt - nci_v) / SH
norm_pat = 14400.0
norm_eps = norm_pat / SH
norm = dict(bear=(13600/SH)*13.5, base=norm_eps*15.0, bull=(15200/SH)*16.5)
dcf_lens = dict(bear=dcf_ps_at(WACC + 0.010, 0.020, -0.005, +0.010),
                base=dcf_ps, bull=dcf_ps_at(WACC - 0.007, 0.030, +0.004, -0.007))
def ddm_at(ke, g, dps_path):
    pv = sum(dps_path[i] / (1 + ke) ** (i + 1) for i in range(5))
    tv_ = dps_path[-1] * (1 + g) / (ke - g)
    return pv + tv_ / (1 + ke) ** 5
ddm_lens = dict(bear=ddm_at(KE + 0.005, 0.020, [2.20, 2.20, 2.20, 2.20, 2.20]),
                base=ddm_ps,
                bull=ddm_at(KE - 0.005, 0.0325, [2.20, 2.20, 2.35, 2.55, 2.75]))
weights = dict(dcf=0.35, ddm=0.25, relative=0.20, normalized=0.20)
central = (weights['dcf'] * dcf_lens['base'] + weights['ddm'] * ddm_lens['base']
           + weights['relative'] * rel['base'] + weights['normalized'] * norm['base'])
central_bear = (weights['dcf'] * dcf_lens['bear'] + weights['ddm'] * ddm_lens['bear']
                + weights['relative'] * rel['bear'] + weights['normalized'] * norm['bear'])
central_bull = (weights['dcf'] * dcf_lens['bull'] + weights['ddm'] * ddm_lens['bull']
                + weights['relative'] * rel['bull'] + weights['normalized'] * norm['bull'])

# ===== Sensitivity grids ======================================================
wacc_steps = [WACC - 0.010, WACC - 0.005, WACC, WACC + 0.005, WACC + 0.010]
g_steps = [0.015, 0.020, 0.025, 0.030, 0.035]
sens_wg = [[(dcf_ps_at(w, g) if w - g > 0.02 else None) for g in g_steps] for w in wacc_steps]
capex_steps = [-0.010, -0.005, 0.0, 0.005, 0.010]     # capex intensity shift (pp of revenue)
margin_steps = [-0.010, -0.005, 0.0, 0.005, 0.010]    # EBITDA margin shift
sens_cm = [[dcf_ps_at(WACC, TG, mm, cc) for cc in capex_steps] for mm in margin_steps]

# ===== Dividend cover stress (device A-2, crux in real units) =================
div_bill = 2.20 * SH / 1000  # SAR bn per year under the locked policy
cover = []
for label, cint in [('15.0%', 0.150), ('16.5% (base FY26E)', 0.165), ('17.5% (top of guidance)', 0.175)]:
    r = fc['FY26E']['rev']
    ocf_e = r * ebitda_m[0] * (1 - TAX) + r * dna_pct[0] * TAX - r * wc_out_pct[0]  # approx: NOPAT+D&A−ΔWC
    fcf_e = ocf_e - r * cint
    cover.append(dict(capex=label, fcf=fcf_e / 1000, div=div_bill, cover=fcf_e / 1000 / div_bill))

# ===== Experts ================================================================
# Expert 1 — Hisham (cash returns / ROIC vs WACC, economic profit)
ic = 90500.0   # invested capital ≈ equity att 83.4bn + net debt 7.1bn (FY25/Q1-26)
roic = rows[0]['nopat'] / ic
ep = (roic - WACC) * ic
FADE = 0.025   # excess returns decay 2.5%/yr toward the cost of capital (moat half-life ~25yr)
def e1_ps_at(fade, wacc_):
    ep_ = (rows[0]['nopat'] / ic - wacc_) * ic
    mult = 1.0 / (wacc_ + fade - TG)          # growing-fading EP perpetuity
    ev_ = ic + ep_ * mult
    return (ev_ + assoc + telefonica - net_debt - nci_v) / SH
e1_ps = e1_ps_at(FADE, WACC)
e1_ev = ic + ep / (WACC + FADE - TG)
e1 = dict(base=e1_ps, rng=(e1_ps_at(0.040, WACC + 0.005), e1_ps_at(0.010, WACC - 0.005)))
# Expert 2 — Karim (normalized earnings power)
e2 = dict(base=norm['base'], rng=(norm['bear'], norm['bull']))
# Expert 3 — Omar (macro-policy scenario tree on the DDM/rate path)
scen = [(0.30, ddm_lens['bull'] * 1.02), (0.45, ddm_ps), (0.25, ddm_lens['bear'] * 0.96)]
e3 = dict(base=sum(p * v_ for p, v_ in scen))

out = dict(
    spot=spot, spot_date=spot_date, shares=SH, mktcap=MKTCAP,
    step0=dict(nonoverlap=summ, monthly=summ21, secular=summ_sec,
               pit_hist=pit_hist, n_rows=len(res), boot=boot),
    engine=dict(anchor_vol=anchor_vol, drift_daily=drift_daily,
                drift_q=drift_daily * 60, factor_drift_q=factor_drift_q,
                cont_drift_q=cont_drift_q, disc_drift_q=disc_drift_q),
    mc=dict(q20=q20, q60=q60, touch=touch, prob_read=prob_read, zones=zone_probs, fan=fan),
    tech=dict(sma=sma, rsi=rsi, macd=macd, hi52=hi52, lo52=lo52, rv252=rv252,
              chg20=chg20, chg60=chg60),
    levers_applied=LEVERS_APPLIED,
    coc_record=COCRUN.record(SCHED),
    terminal_record=_t.record,
    hist=hist, seg_hist=seg_hist,
    drivers=dict(g_cbu=g_cbu, g_ebu=g_ebu, g_wc=g_wc, g_sub=g_sub, ebitda_m=ebitda_m,
                 dna_pct=dna_pct, capex_pct=capex_pct, wc_out_pct=wc_out_pct, payout_dps=payout_dps),
    forecast=fc,
    dcf=dict(rows=rows, pv_sum=pv_sum, tv=tv, pv_tv=pv_tv, ev=ev, tv_pct=pv_tv / ev,
             # Exposed so the terminal census can score this terminal from outside rather
             # than report it unreadable. Both are real quantities the module already used:
             # the terminal year's own after-tax operating profit, and the depreciable gross
             # base at CURRENT cost, which is the same escalation the maintenance charge
             # rests on.
             nopat_term=rows[-1]['nopat'], ic_repl=TERM_IC_PER_UNIT_GROWTH,
             terminal_maintenance=_t.maintenance, terminal_fcff=_t.fcff,
             terminal_life_years=TERM_LIFE, terminal_age_years=TERM_AGE,
             wacc=WACC, wacc_rating_basis=WACC_RATING, tg=TG, assoc=assoc, telefonica=telefonica,
             net_debt=net_debt, nci=nci_v, eq=eq_dcf, ps=dcf_ps,
             wacc_build=dict(rf=SCHED.rf_observed, default_spread=SCHED.default_spread,
                             rf_star=SCHED.rf_star, erp_market=SCHED.erp,
                             erp_rating=SCHED_RATING.erp, beta=BETA,
                             beta_reg=dict(beta=COCRUN.BETA_RAW['beta'],
                                           r2=COCRUN.BETA_RAW['r2'],
                                           n=COCRUN.BETA_RAW['n'],
                                           se=COCRUN.BETA_RAW['se'],
                                           window_years=COCRUN.BETA_RAW['window_years'],
                                           index_file=COCRUN.BETA_RAW['index_file'],
                                           index_asof=COCRUN.BETA_RAW['index_asof'],
                                           conforming=COCRUN.BETA_RAW['conforming']),
                             ke_rating=KE_RATING, ke_market=KE_MARKET,
                             kd_pretax=SCHED.kd_pretax, kd_aftertax=KD_AT,
                             we=WE, wd=WD, wacc_market=WACC, wacc_rating=WACC_RATING,
                             tax=TAX, regime=SCHED.regime,
                             beta_source=COCRUN.BETA.source,
                             kd_source=COCRUN.DEBT.kd_source,
                             debt_currency_evidence=COCRUN.DEBT.currency_source,
                             weights_source=COCRUN.WEIGHTS_SOURCE,
                             disclosures=list(SCHED.disclosures))),
    ddm=dict(dps=payout_dps, pv_div=pv_div, tv=tv_div, pv_tv=pv_tv_div, ps=ddm_ps,
             tv_pct=ddm_tv_pct, ke=KE, g=tg_div),
    lenses=dict(dcf=dcf_lens, ddm=ddm_lens, relative=rel, normalized=norm,
                central=dict(bear=central_bear, base=central, bull=central_bull),
                weights=weights),
    rel_basis=dict(ebitda26=ebitda26, np26=np26, eps26=eps26, evx=rel_evx,
                   norm_pat=norm_pat, norm_eps=norm_eps),
    sens=dict(wacc_steps=wacc_steps, g_steps=g_steps, table_wg=sens_wg,
              margin_steps=margin_steps, capex_steps=capex_steps, table_cm=sens_cm),
    cover=cover, div_bill=div_bill,
    experts=dict(e1=e1, e2=e2, e3=e3, e1_roic=roic, e1_ic=ic, e1_ep=ep),
)
res.to_csv('backtest_rows.csv', index=False)
np.save('fan.npy', np.array([fan[p] for p in pcts]))
np.save('pT20.npy', pT20[:20000]); np.save('pT60.npy', pT60[:20000])
# A SENSITIVITY RUN NEVER WRITES. It exists to measure one lever's own worth, and an
# answer struck on a beta this study does not adopt must not reach the committed record.
if _SENS_BETA is None:
    with open(os.path.join(HERE, 'study_numbers.json'), 'w') as f:
        json.dump(out, f, indent=1, default=float)
else:
    # It writes ONE artefact and it is not the study's numbers: the answer this study
    # would reach on a beta it does not adopt, so the rebuild ledger can read the lever's
    # own worth instead of a figure somebody copied off a terminal. [R-ENF-06]
    with open(os.path.join(HERE, 'beta_sensitivity_%s.json' % SENS_TAG), 'w') as f:
        json.dump(dict(beta=_SENS_BETA, levers_applied=LEVERS_APPLIED,
                       what=('the answer on a beta this study does NOT adopt, produced '
                             'only to measure what the beta correction was worth on its '
                             'own. The 40-session daily regression the delivered study '
                             'carried is not one of the three tiers, and the sanctioned '
                             'schedule refuses to build on it as a study beta.'),
                       wacc_market=WACC, wacc_rating=WACC_RATING,
                       ke_market=KE_MARKET, ke_rating=KE_RATING,
                       lenses=dict(dcf=dcf_lens, ddm=ddm_lens, relative=rel,
                                   normalized=norm),
                       central=dict(bear=central_bear, base=central, bull=central_bull),
                       weights=weights), f, indent=1, default=float)
    print('SENSITIVITY RUN on beta %.4f — beta_sensitivity_%s.json only'
          % (_SENS_BETA, SENS_TAG))
print('spot', spot, spot_date, '| anchor_vol', round(anchor_vol, 4), '| factor_q', round(factor_drift_q * 100, 2), '%')
print('Step0 zero-drift non-overlap:', {k: round(v_, 4) if isinstance(v_, float) else v_ for k, v_ in summ.items()})
print('boot:', boot)
print('WACC market %.3f%% | rating %.3f%% | Ke %.3f/%.3f | Kd_at %.3f | We %.3f'
      % (WACC*100, WACC_RATING*100, KE_MARKET*100, KE_RATING*100, KD_AT*100, WE))
print('T60:', {k: round(v_, 1) for k, v_ in q60.items()}, '| P(up)=%.3f odds=%.2f' % (prob_read['p_above'], prob_read['odds']))
print('DCF: EV %.0f TV%% %.0f%% eq %.0f ps %.2f | DDM %.2f (TV %.0f%%) | rel %.1f | norm %.1f | central %.1f [%.1f-%.1f]' %
      (ev, 100 * pv_tv / ev, eq_dcf, dcf_ps, ddm_ps, ddm_tv_pct * 100, rel['base'], norm['base'], central, central_bear, central_bull))
print('FCFF path:', [round(r['fcff']) for r in rows])
print('rev path:', [round(r['rev']) for r in rows])
print('cover:', [(c['capex'], round(c['fcf'], 1), round(c['cover'], 2)) for c in cover])
print('experts:', round(e1['base'], 1), round(e2['base'], 1), round(e3['base'], 1), '| ROIC %.1f%%' % (roic * 100))
