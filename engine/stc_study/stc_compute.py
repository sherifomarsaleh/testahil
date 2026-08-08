"""STC study — master computation. Outputs stc_study_numbers.json + backtest tables.
Saudi Telecom Company (Tadawul: 7010). Spot from the attached daily history (7 Jul 2026)."""
import json
import numpy as np
import pandas as pd
import mc_v2 as m
from wacc_builder import WaccInputs, build_wacc, RegressionBetaAttempt

df = m.load_ohlc('STC_Stock_Price_History.csv')
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

# ===== WACC — bottom-up, sourced (house rule §3.5-G) =========================
reg = RegressionBetaAttempt(beta=0.4753, r_squared=0.1426, n_obs=40, se_beta=0.1890)
usable, gate_msg = reg.is_usable()
assert usable, gate_msg
BETA = round(reg.beta, 2)
wacc_inputs = WaccInputs(
    rf=0.055,
    rf_source="Derived SAR 10Y sovereign: KSA govt-guaranteed USD 10Y priced UST+95bp on 8-Jul-2026 (SRC $1.5bn 10y sukuk; UST 10Y 4.45%) = 5.40%, plus the SAR-over-USD sovereign pickup documented in the Saudi Exchange 'KSA Sovereign Local Currency Debt Primer Update' (21-May-2026); cross-checked vs FAB Securities' 5.5% SAR rf (27-Feb-2026). Flagged: derived, no free live SAR 10Y screen quote exists.",
    erp_rating=0.0501, erp_cds=0.0572,
    erp_source="Damodaran ORIGINAL file (pages.stern.nyu.edu/~adamodar/.../ctryprem.html), Saudi Arabia row, 'Last updated: January 5, 2026': Moody's Aa3, CRP 0.78% + mature 4.23% = 5.01% (rating); CDS-based 5.72%.",
    beta=BETA,
    beta_source=f"Genuine daily STC-vs-TASI regression, n=40 paired sessions (5-May→7-Jul-2026, investing.com TASI closes): beta={reg.beta:.3f}, R2={reg.r_squared:.3f}, SE={reg.se_beta:.3f} — passes the usability gate (n≥24, R2≥5%, SE<|beta|, beta>0). Flag: 9-week window (longer TASI history not programmatically accessible); beta sensitivity grid published.",
    kd_pretax_local=0.050,
    kd_source="stc's own instruments: Jan-2026 $2bn sukuk priced 4.489% (5y, T+75) / 5.083% (10y, T+90); May-2019 $1.25bn sukuk 3.89%; SAR bank murabaha ≈ 3M SAIBOR 4.79% (Apr-2026, SAMA-linked) + ~60–100bp. Weighted outstanding book ≈ 5.0% pre-tax.",
    kd_pretax_fx=None, pct_debt_local_ccy=1.0,
    debt_currency_evidence="Named instruments: USD sukuk $1.25bn (2019, 3.89%) + $2.0bn (Jan-2026, 4.489%/5.083%) = SAR 12.2bn of Q1-26 sukuk 12.16bn; ECA loan $584mn (2021); remainder SAR murabaha/facilities. USD-linked ≈ 55-60% of gross debt, but SAR is pegged 3.75 — USD legs are economically quasi-SAR, so a single blended local-cost Kd is used (no floating-FX tranche).",
    tax_rate=TAX,
    market_cap=MKTCAP, total_debt=22475.0,
    weights_source="Market cap = spot(43.58) × shares(4,989.8mn) = SAR 217.5bn; total debt = Q1-2026 IR-disclosed total debt SAR 22,475mn (post Jan-26 $2bn sukuk; excl. leases 2,296).",
)
_wr = build_wacc(wacc_inputs)
WACC = _wr.wacc_rating          # primary: rating-based ERP ("standard practice" per Damodaran)
WACC_CDS = _wr.wacc_cds         # alternative: CDS-based ERP ("more current")
KE_RATING, KE_CDS = _wr.ke_rating, _wr.ke_cds
KD_AT = _wr.kd_aftertax
WE, WD = _wr.we, _wr.wd
TG = 0.025                      # terminal growth, nominal SAR

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
    rw['df'] = 1 / (1 + WACC) ** (i + 1)
    rw['pv'] = rw['fcff'] * rw['df']
pv_sum = sum(rw['pv'] for rw in rows)
tv = rows[-1]['fcff'] * (1 + TG) / (WACC - TG)
pv_tv = tv * rows[-1]['df']
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
            fcff5 = fcff_
    tv_ = fcff5 * (1 + g) / (wacc - g)
    pvtv = tv_ / (1 + wacc) ** 5
    return (pv + pvtv + assoc + telefonica - net_debt - nci_v) / SH

# ===== DDM (cash-flow cross-check: the locked 0.55/q policy) ==================
KE = KE_RATING
pv_div = sum(payout_dps[i] / (1 + KE) ** (i + 1) for i in range(5))
tg_div = 0.030
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
    hist=hist, seg_hist=seg_hist,
    drivers=dict(g_cbu=g_cbu, g_ebu=g_ebu, g_wc=g_wc, g_sub=g_sub, ebitda_m=ebitda_m,
                 dna_pct=dna_pct, capex_pct=capex_pct, wc_out_pct=wc_out_pct, payout_dps=payout_dps),
    forecast=fc,
    dcf=dict(rows=rows, pv_sum=pv_sum, tv=tv, pv_tv=pv_tv, ev=ev, tv_pct=pv_tv / ev,
             wacc=WACC, wacc_cds=WACC_CDS, tg=TG, assoc=assoc, telefonica=telefonica,
             net_debt=net_debt, nci=nci_v, eq=eq_dcf, ps=dcf_ps,
             wacc_build=dict(rf=wacc_inputs.rf, erp_rating=wacc_inputs.erp_rating,
                             erp_cds=wacc_inputs.erp_cds, beta=BETA,
                             beta_reg=dict(beta=reg.beta, r2=reg.r_squared, n=reg.n_obs, se=reg.se_beta),
                             ke_rating=KE_RATING, ke_cds=KE_CDS,
                             kd_pretax=wacc_inputs.kd_pretax_local, kd_aftertax=KD_AT,
                             we=WE, wd=WD, wacc_rating=WACC, wacc_cds=WACC_CDS, tax=TAX,
                             rf_source=wacc_inputs.rf_source, erp_source=wacc_inputs.erp_source,
                             kd_source=wacc_inputs.kd_source,
                             debt_currency_evidence=wacc_inputs.debt_currency_evidence,
                             beta_source=wacc_inputs.beta_source,
                             weights_source=wacc_inputs.weights_source)),
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
with open('stc_study_numbers.json', 'w') as f:
    json.dump(out, f, indent=1, default=float)
print('spot', spot, spot_date, '| anchor_vol', round(anchor_vol, 4), '| factor_q', round(factor_drift_q * 100, 2), '%')
print('Step0 zero-drift non-overlap:', {k: round(v_, 4) if isinstance(v_, float) else v_ for k, v_ in summ.items()})
print('boot:', boot)
print('WACC rating %.3f%% | CDS %.3f%% | Ke %.3f/%.3f | Kd_at %.3f | We %.3f' % (WACC*100, WACC_CDS*100, KE_RATING*100, KE_CDS*100, KD_AT*100, WE))
print('T60:', {k: round(v_, 1) for k, v_ in q60.items()}, '| P(up)=%.3f odds=%.2f' % (prob_read['p_above'], prob_read['odds']))
print('DCF: EV %.0f TV%% %.0f%% eq %.0f ps %.2f | DDM %.2f (TV %.0f%%) | rel %.1f | norm %.1f | central %.1f [%.1f-%.1f]' %
      (ev, 100 * pv_tv / ev, eq_dcf, dcf_ps, ddm_ps, ddm_tv_pct * 100, rel['base'], norm['base'], central, central_bear, central_bull))
print('FCFF path:', [round(r['fcff']) for r in rows])
print('rev path:', [round(r['rev']) for r in rows])
print('cover:', [(c['capex'], round(c['fcf'], 1), round(c['cover'], 2)) for c in cover])
print('experts:', round(e1['base'], 1), round(e2['base'], 1), round(e3['base'], 1), '| ROIC %.1f%%' % (roic * 100))
