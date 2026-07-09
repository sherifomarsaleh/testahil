"""GBCO study — master computation. Outputs study_numbers.json + backtest tables."""
import json
import numpy as np
import pandas as pd
import mc_v2 as m

df = m.load_ohlc('GB_AUTO_Stock_Price_History.csv')
close = df['Price'].values
spot = float(close[-1])
spot_date = str(df['Date'].iloc[-1].date())
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
# ===== WACC — bottom-up, sourced (house rule §3.5-G, rebuilt 09-07-2026) =====
# Every input below is sourced; see Cost_of_Capital_Reference.md for the Egypt cache and
# the Fundamental Driver Ledger (S2) for the correction history on the ERP figure.
from wacc_builder import WaccInputs, build_wacc
_wacc_inputs = WaccInputs(
    rf=0.2255,
    rf_source="investing.com, Egypt 10Y local-currency govt bond yield, 3-Jul-2026",
    erp_rating=0.1394, erp_cds=0.0941,
    erp_source="Damodaran ORIGINAL file (ctryprem.html), Egypt row, 'Last updated January 2026'",
    beta=1.0,
    beta_source="assumed_1.0 -- n=5 annual GBCO-vs-EGX30 regression gave beta=-0.15, R2=0.008 (unusable); "
                 "higher-frequency EGX30 data inaccessible via available tools; house rule default applied",
    kd_pretax_local=0.207,
    kd_source="CBE weighted-average EGP bank lending rate, <12mo tenor, Feb-2026 (CEIC/TradingEconomics "
               "quoting CBE); cross-checked against CBE overnight lending-rate ceiling 20.0% held since Apr-2026",
    kd_pretax_fx=None, pct_debt_local_ccy=1.0,
    debt_currency_evidence="5 separately disclosed GB Corp/GB Capital financing facilities found, all EGP-"
                            "denominated; zero USD facilities found in any search",
    tax_rate=0.28,
    market_cap=31.25*1085.5, total_debt=38041.4,
    weights_source="market cap = spot x shares; total debt = FY25 disclosed consolidated borrowings",
)
_wr = build_wacc(_wacc_inputs)
WACC = _wr.wacc_cds       # primary: CDS-based ERP (more current than the rating-based figure)
WACC_RATING = _wr.wacc_rating   # alternative, shown alongside in the study as "standard practice" per Damodaran
TG = 0.115                # terminal growth unchanged; WACC-TG spread widens slightly (10.5pt -> 11.4pt vs prior)
KE_CDS, KE_RATING = _wr.ke_cds, _wr.ke_rating
KD_AFTERTAX = _wr.kd_aftertax
WE, WD = _wr.we, _wr.wd
for i, rw in enumerate(rows):
    rw['df'] = 1 / (1 + WACC) ** (i + 1)
    rw['pv'] = rw['fcff'] * rw['df']
pv_sum = sum(rw['pv'] for rw in rows)
tv = rows[-1]['fcff'] * (1 + TG) / (WACC - TG)
pv_tv = tv * rows[-1]['df']
ev_auto = pv_sum + pv_tv
auto_nd = 15210.0
auto_nci = 800.4
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
    pvs = sum(f/(1+wacc)**(i+1) for i, f in enumerate(rws))
    tv_ = rws[-1]*(1+tg)/(wacc-tg)/(1+wacc)**5
    ae = pvs+tv_-auto_nd-auto_nci
    return (ae + cap_book*cap_m + assoc*assoc_m)*(1-d)/SH
sotp_bear = sotp_case(-0.012, WACC+0.020, 0.105, 0.80, 0.80, 0.18)
sotp_bull = sotp_case(+0.010, WACC-0.015, 0.125, 1.25, 1.20, 0.04)
dcf_lens = dict(bear=sotp_case(-0.012, WACC+0.020, 0.105, 0.80, 0.80, 0.0),
                base=prediscount_ps,
                bull=sotp_case(+0.010, WACC-0.015, 0.125, 1.25, 1.20, 0.0))
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

out = dict(
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
             wacc_build=dict(rf=_wacc_inputs.rf, erp_rating=_wacc_inputs.erp_rating,
                             erp_cds=_wacc_inputs.erp_cds, beta=_wacc_inputs.beta,
                             ke_cds=KE_CDS, ke_rating=KE_RATING,
                             kd_pretax=_wacc_inputs.kd_pretax_local, kd_aftertax=KD_AFTERTAX,
                             we=WE, wd=WD, wacc_cds=WACC, wacc_rating=WACC_RATING,
                             rf_source=_wacc_inputs.rf_source, erp_source=_wacc_inputs.erp_source,
                             kd_source=_wacc_inputs.kd_source,
                             debt_currency_evidence=_wacc_inputs.debt_currency_evidence,
                             beta_source=_wacc_inputs.beta_source)),
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
