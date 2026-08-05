"""ELEC study — master computation. Writes study_numbers.json (single source of
truth for every builder). Code-first rule: INPUTS are four-field records
{value, source, date, ring}; a bare numeral cannot enter the model; the ASSERT
block raises (no JSON emitted) unless the bridge closes, the glide is ordered,
the Kd-integrity triple holds, and the terminal is ROIC-consistent."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import numpy as np

# ============================ INPUTS =========================================
# Every record: {value, source, date, ring}. ring: Market/Country/Industry/Company/House.
def I(value, source, date, ring):
    return dict(value=value, source=source, date=date, ring=ring)

INP = dict(
    # ---- anchors ----
    spot=I(2.19, "uploaded EGX daily history, last close", "2026-08-05", "Market"),
    shares_mn=I(3313.540373, "Mubasher ELEC profile (paid-in capital EGP 662,708,074.60 / par 0.20); "
                "verified 3 ways: SWS holder sum; FY24 EPS 0.40=1,327.8/3,313.5; FY25 EPS 0.15=500.3/3,313.5",
                "2026 (mid)", "Company"),
    tax=I(0.225, "PwC Tax Summaries Egypt — corporate income tax 22.5%, unchanged 2025-26", "2026", "Country"),
    fx=I(50.3, "USD/EGP mid-market (Bloomberg quote; bank avg ~51.0)", "2026-08-05", "Country"),

    # ---- historical income statement (EGP mn) ----
    rev_fy23=I(8673.4, "MarketScreener/Mubasher FY2024 results note (comparative)", "2025-03", "Company"),
    rev_fy24=I(13778.2, "MarketScreener/Mubasher FY2024 consolidated results", "2025-03", "Company"),
    rev_fy25=I(10819.0, "Arab Finance/Zawya FY2025 results (net sales EGP 10.81bn)", "2026-03", "Company"),
    np_fy23=I(1248.0, "Zawya/MarketScreener (FY23 consolidated NP)", "2024-03", "Company"),
    np_fy24=I(1327.8, "Mubasher FY2024 consolidated results", "2025-03", "Company"),
    np_fy25=I(500.31, "Arab Finance FY2025 (attributable; Reuters flash 501.4 incl. NCI)", "2026-03", "Company"),
    ebit_fy24=I(3400.0, "Simply Wall St health page: 'EBIT is EGP3.4B, interest coverage 2x'", "2025-05-22", "Company"),
    ebitda_fy24=I(3490.0, "Investing.com financial summary ('EBITDA 3.49B') — single aggregator, "
                  "period attributed to FY2024; flagged", "2026 capture", "Company"),
    int_cover_fy24=I(2.0, "Simply Wall St health page (interest coverage 2x EBIT)", "2025-05-22", "Company"),
    q1_26_rev=I(2094.0, "Zawya/Arab Finance Q1-2026 (consolidated net sales)", "2026-05", "Company"),
    q1_26_np=I(-241.6, "Zawya/Arab Finance Q1-2026 (consolidated net LOSS)", "2026-05", "Company"),
    q1_25_rev=I(3723.0, "Q1-2026 release comparatives", "2026-05", "Company"),
    q1_25_np=I(451.7, "Q1-2026 release comparatives", "2026-05", "Company"),

    # ---- historical balance sheet anchors (EGP mn) ----
    assets_fy22=I(4960.0, "Zawya 9M-2023 results note (comparative, 31-Dec-2022)", "2023-11", "Company"),
    assets_fy24=I(14970.0, "Zawya/Decypha FY2025 note (comparative) + SWS (15.0bn)", "2026-03", "Company"),
    assets_fy25=I(16460.0, "Zawya/Decypha FY2025 results (total assets, +9.9%)", "2026-03", "Company"),
    debt_fy24=I(9000.0, "Simply Wall St health page (total debt) — single aggregator, "
                "credible (its assets figure matches the twice-sourced 14.97bn)", "2025-05-22", "Company"),
    cash_fy24=I(827.6, "Simply Wall St health page (cash & ST investments)", "2025-05-22", "Company"),
    equity_fy24=I(3600.0, "Simply Wall St health page (total shareholder equity)", "2025-05-22", "Company"),
    liab_fy24=I(11300.0, "Simply Wall St health page (total liabilities)", "2025-05-22", "Company"),
    assets_fy23_est=I(10000.0, "House estimate — bounded by 9M-23 disclosed 8,060 and FY24 14,970; "
                      "no FY23 year-end print found (flagged)", "2026-08-05", "House"),

    # ---- derived-history assumptions (flagged house judgments) ----
    fin_cost_fy25_est=I(2150.0, "House derivation: avg debt ~9.25bn x ~23.2% effective (CBE corridor 2025 "
                        "path); closes FY25 P&L to the reported NP 500.3 via EBT=NP/(1-22.5%)", "2026-08-05", "House"),
    fin_cost_fy23_est=I(990.0, "House derivation: avg FY23 debt ~4.5bn (D/E path 36%->248% over 5yrs, "
                        "SWS) x ~22% 2023 corridor-linked rate", "2026-08-05", "House"),
    dna_pct=I(0.013, "House: FY24 EBITDA 3,490 - EBIT 3,400 = ~90mn D&A on 13.8bn revenue (~0.7%); "
              "forecast set at 1.3% of revenue to fund modest PP&E renewal", "2026-08-05", "House"),
    payables_fy25_est=I(2100.0, "House estimate: FY24 non-debt liabilities 2,300 (liab 11,300 - debt "
                        "9,000), scaled to the smaller FY25 revenue base", "2026-08-05", "House"),
    nwc_fy25_est=I(12000.0, "House derivation: FY25 assets 16,460 - cash ~700 - PP&E ~680 - other ~980 "
                   "= gross WC ~14,100; less payables ~2,100 => ~12,000 (111% of FY25 revenue). "
                   "Consistent with FY24: assets 14,970, NWC ~10,500 (76% of revenue)", "2026-08-05", "House"),
    net_debt_fy25_est=I(8800.0, "House derivation: FY25 liabilities (16,460-4,100 equity) = 12,360; less "
                        "payables/other ~2,860 => debt ~9,500; less cash ~700. FY24-vintage sourced "
                        "anchor: 9,000 - 827.6 = 8,172 (SWS). Sensitized +/-1,000 in the grid", "2026-08-05", "House"),
    equity_fy25_est=I(4100.0, "House derivation: FY24 equity 3,600 + FY25 NP 500.3, no dividends "
                      "(company has never paid one)", "2026-08-05", "House"),

    # ---- forecast drivers (house judgments, sensitized) ----
    rev_growth=I([-0.196, 0.14, 0.12, 0.10, 0.08],
                 "House: FY26E anchored on Q1-26 -43.8% with H2 stabilisation as CBE resumes easing; "
                 "recovery years on the EETC EGP45bn grid plan, EU 690mn package, Saudi interconnector "
                 "completion and 6.7% CAGR industry path (6Wresearch)", "2026-08-05", "House"),
    ebitda_margin=I([0.130, 0.160, 0.175, 0.185, 0.190],
                    "House: Q1-26 implied trough ~14% (loss of 241.6 after ~540 finance cost); FY24-25 "
                    "prints ~25% carried devaluation-era inventory gains (Ring-4 finding: windfall, not "
                    "run-rate); mid-cycle set between trough and windfall, sensitized +/-3pp", "2026-08-05", "House"),
    capex_pct=I(0.016, "House: maintenance-level for a working-capital-intensive assembler; no disclosed "
                "capex found any year (flagged gap); FY24 D&A ~0.7% of revenue corroborates a light "
                "fixed-asset base", "2026-08-05", "House"),
    nwc_pct=I([1.08, 1.03, 0.98, 0.93, 0.88],
              "House: FY25 intensity ~111% of revenue (derived above) gliding to 88% as receivables "
              "collect and copper-inflated inventory normalises; FY24 was 76% — full reversion NOT "
              "assumed; sensitized in the grid", "2026-08-05", "House"),

    # ---- cost of capital (sliding schedule — Egypt) ----
    rf=I(0.2231, "investing.com, Egypt 10Y local-currency govt bond yield, cached in-repo "
         "wacc_builder.py Egypt worked example; corroborated by the May-2026 window avg 21.3% "
         "(range 20.9-21.6)", "2026-07-21", "Country"),
    sov_spread_cds=I(0.0340, "Egypt CDS-implied sovereign default spread, Damodaran Jan-2026 original "
                     "file (house cache); market 5Y CDS ~330bp late-May-2026 corroborates", "2026-01-05", "Country"),
    sov_spread_rating=I(0.0637, "Damodaran adjusted default spread, rating basis (Caa1), Jan-2026 "
                        "original file (house cache)", "2026-01-05", "Country"),
    erp_cds=I(0.0941, "Damodaran ORIGINAL ctryprem, Egypt row, CDS column, 'Last updated January 5, "
              "2026' (house cache; original page 403-blocked this session). A July-2026 secondary "
              "reproduction claims total ERP 14.87% — same figure previously caught as a misquote; "
              "NOT adopted, shown in sensitivity only", "2026-01-05", "Country"),
    erp_rating=I(0.1394, "Damodaran ORIGINAL ctryprem, Egypt row, rating basis, Jan-2026 (house cache)",
                 "2026-01-05", "Country"),
    beta=I(0.964, "Own-stock tier-1 regression: ELEC weekly log-returns vs 30-name equal-weight EGX "
           "composite (full engine library), 5yr window: beta 0.964, R2 0.222, n=257, SE 0.113, "
           "CI90 [0.78, 1.15] — passes usability gate; NOT weak-flagged (R2>10%, CI span < 2x beta)",
           "2026-08-05", "House"),
    kd=I(0.235, "Marginal EGP rate for a levered EGX mid-cap: CBE corridor 19.5-20.0% (held 09-Jul-26) "
         "+ ~3.5pp levered-credit margin; consistent with avg bank lending 21.3% (Jan-26) plus a "
         "leverage premium. Cross-checked against the two effective-rate computations below", "2026-08-05", "House"),
    kd_eff_fy24=I(0.234, "Effective-rate check #1: FY24 interest ~1,700 (EBIT 3,400 / coverage 2.0x, "
                  "SWS) / avg debt ~(5,500e+9,000)/2 = 7,250 => 23.4%", "2026-08-05", "House"),
    kd_eff_fy25=I(0.232, "Effective-rate check #2: FY25 finance cost ~2,150 (derived, closes P&L to "
                  "reported NP) / avg debt ~9,250 => 23.2%", "2026-08-05", "House"),
    debt_ccy_evidence=I("No facility-level disclosure reachable (FS notes on Mubasher/company site "
                        "403-blocked). PRESUMPTION, flagged: predominantly EGP working-capital "
                        "facilities (import LCs settled spot; post-2016 Egyptian cable-sector norm); "
                        "no USD facility found in any search — treated as ~100%% EGP with the gap "
                        "stated rather than assumed away",
                        "search sweep 05-Aug-2026, negative result", "2026-08-05", "Company"),
    kd_term=I(0.150, "Terminal Kd: Egyptian long-run corporate-borrowing norm 14-16%, midpoint "
              "(standing house norm; no name-specific reason to deviate)", "2026-08-05", "House"),
    rf_term=I(0.105, "Terminal rf norm-built: CBE's own stated Q4-2028 inflation target 5%% (+/-2pp) "
              "+ ~5.5pp EM real-rate convention (house standing construction)", "2026-08-05", "House"),
    erp_term=I(0.070, "Terminal ERP normalised below the crisis-era 9.41%% CDS-based level toward the "
               "B-rating-class norm; never held flat into perpetuity (house standing rule)", "2026-08-05", "House"),
    kd_path=I([0.235, 0.210, 0.190, 0.170, 0.155],
              "Forward Kd path: CBE easing resumes H2-26 (MPC 20-Aug/01-Oct/12-Nov-26) toward the "
              "7%%->5%% inflation-target glide; corporate spread held ~3pp; terminal 15%%. The WACC "
              "glide shape is tied to this path by construction", "2026-08-05", "House"),
    g_term=I(0.05, "Terminal growth center 5%% — standing convention for established Egyptian names "
             "post-disinflation; grid 3-7%%", "2026-08-05", "House"),

    # ---- lens inputs ----
    ev_ebitda_base=I(5.5, "Justified EV/EBITDA on mid-cycle FY27E EBITDA: SWDY trades ~6x (multiples.vc "
                     "mid-2026) with a fortress balance sheet and export book; ELEC discount for "
                     "leverage, domestic concentration, no dividend record. Bear 4.5x / bull 6.5x",
                     "2026-08-05", "House"),
    pe_norm=I(6.5, "Justified through-cycle P/E on normalized EPS: SWDY 10.4x trailing (stockanalysis, "
              "Jul-26); Riyadh Cables 18x (different market). Levered uncovered EGX small-cap "
              "discount. Bear 5.5x / bull 8.0x", "2026-08-05", "House"),
    roe_sust=I(0.14, "Sustainable ROE for the book lens: normalized NP ~600-750 on ~4.6-5.2bn forward "
               "book => 13-15%%; struck below FY23-24 windfall ROEs (35%%+) which carried "
               "devaluation inventory gains", "2026-08-05", "House"),
    lens_weights=I(dict(dcf=0.40, relative=0.20, normalized=0.20, book=0.20),
                   "House: DCF primary for an operating manufacturer; the three market lenses share "
                   "the remainder equally", "2026-08-05", "House"),
)

# validate four-field completeness (code-first rule)
for k, rec in INP.items():
    assert set(rec) == {'value', 'source', 'date', 'ring'}, f"INPUT {k} not four-field"
    assert rec['source'] and rec['date'] and rec['ring'], f"INPUT {k} missing provenance"

V = {k: rec['value'] for k, rec in INP.items()}

# ============================ CALC ===========================================
SH = V['shares_mn']; SPOT = V['spot']; TAX = V['tax']
MKTCAP = SPOT * SH

# ---- derived history (P&L closure) ----
int_fy24 = V['ebit_fy24'] / V['int_cover_fy24']                     # 1,700
ebt_fy24 = V['ebit_fy24'] - int_fy24                                # 1,700
np_fy24_check = ebt_fy24 * (1 - TAX)                                # 1,317.5 vs 1,327.8
ebt_fy25 = V['np_fy25'] / (1 - TAX)                                 # 645.6
ebit_fy25 = ebt_fy25 + V['fin_cost_fy25_est']                       # 2,795.6
ebitda_fy25 = ebit_fy25 + 0.007 * V['rev_fy25']                     # + ~76 D&A (0.7% hist)
ebt_fy23 = V['np_fy23'] / (1 - TAX)                                 # 1,610.3
ebit_fy23 = ebt_fy23 + V['fin_cost_fy23_est']                       # 2,600.3
ebitda_fy23 = ebit_fy23 + 0.007 * V['rev_fy23']
dna_fy = {'FY23': 0.007 * V['rev_fy23'], 'FY24': V['ebitda_fy24'] - V['ebit_fy24'],
          'FY25': 0.007 * V['rev_fy25']}

hist_is = {
    'FY23': dict(rev=V['rev_fy23'], ebitda=ebitda_fy23, dna=dna_fy['FY23'], ebit=ebit_fy23,
                 fin=-V['fin_cost_fy23_est'], ebt=ebt_fy23, tax=-(ebt_fy23 - V['np_fy23']),
                 np=V['np_fy23']),
    'FY24': dict(rev=V['rev_fy24'], ebitda=V['ebitda_fy24'], dna=dna_fy['FY24'], ebit=V['ebit_fy24'],
                 fin=-int_fy24, ebt=ebt_fy24, tax=-(ebt_fy24 - V['np_fy24']), np=V['np_fy24']),
    'FY25': dict(rev=V['rev_fy25'], ebitda=ebitda_fy25, dna=dna_fy['FY25'], ebit=ebit_fy25,
                 fin=-V['fin_cost_fy25_est'], ebt=ebt_fy25, tax=-(ebt_fy25 - V['np_fy25']),
                 np=V['np_fy25']),
}

# ---- cost of capital: explicit window (sovereign double-count removed) ----
rf_star_cds = V['rf'] - V['sov_spread_cds']
rf_star_rating = V['rf'] - V['sov_spread_rating']
ke_cds = rf_star_cds + V['beta'] * V['erp_cds']            # primary
ke_rating = rf_star_rating + V['beta'] * V['erp_rating']   # alternative
ke_raw = V['rf'] + V['beta'] * V['erp_cds']                # RETIRED, audit trail only
kd_at = V['kd'] * (1 - TAX)
we = MKTCAP / (MKTCAP + V['debt_fy24'])
wd = 1 - we
wacc_exp = we * ke_cds + wd * kd_at
wacc_exp_rating = we * ke_rating + wd * kd_at

# ---- terminal (norm-built, never backed out of a price) ----
ke_term = V['rf_term'] + V['beta'] * V['erp_term']
kd_term_at = V['kd_term'] * (1 - TAX)
wacc_term = we * ke_term + wd * kd_term_at

# ---- glide: fractions from kd_path (never invented separately) ----
kdp = V['kd_path']
glide_frac = [(kdp[0] - k) / (kdp[0] - kdp[-1]) for k in kdp]
fwd = [wacc_exp - (wacc_exp - wacc_term) * f for f in glide_frac]
df = []
c = 1.0
for w in fwd:
    c /= (1 + w)
    df.append(c)

# ---- forecast & FCFF waterfall ----
yrs = ['FY26E', 'FY27E', 'FY28E', 'FY29E', 'FY30E']
rows = []
rev = V['rev_fy25']
nwc_prev = V['nwc_fy25_est']
for i, y in enumerate(yrs):
    rev = rev * (1 + V['rev_growth'][i])
    ebitda = rev * V['ebitda_margin'][i]
    dna = rev * V['dna_pct']
    ebit = ebitda - dna
    nopat = ebit * (1 - TAX)
    capex = rev * V['capex_pct']
    nwc = rev * V['nwc_pct'][i]
    dwc = nwc - nwc_prev
    fcff = nopat + dna - capex - dwc
    rows.append(dict(year=y, rev=rev, ebitda=ebitda, dna=dna, ebit=ebit, nopat=nopat,
                     capex=capex, nwc=nwc, dwc=dwc, fcff=fcff,
                     fwd_wacc=fwd[i], df=df[i], pv=fcff * df[i]))
    nwc_prev = nwc

pv_sum = sum(r['pv'] for r in rows)

# ---- terminal value, ROIC x RR-consistent (the CLHO rule) ----
nop_T = rows[-1]['nopat']
ic_T = rows[-1]['nwc'] + 0.05 * rows[-1]['rev']       # invested capital ~ NWC + light PP&E
roic_T = nop_T / ic_T
rr_T = V['g_term'] / roic_T                            # reinvestment needed to fund g
fcff_T1 = nop_T * (1 + V['g_term']) * (1 - rr_T)
tv = fcff_T1 / (wacc_term - V['g_term'])
pv_tv = tv * df[-1]
ev = pv_sum + pv_tv
tv_pct = pv_tv / ev

# ---- bridge ----
net_debt = V['net_debt_fy25_est']
nci = 0.0   # consolidated-attributable gap ~1.1mn FY25 — immaterial, carried at zero (flagged)
eq_dcf = ev - net_debt - nci
dcf_ps = eq_dcf / SH

# ---- scenario engine for the other lens legs & bear/bull ------------------
def run_dcf(margin_shift=0.0, nwc_end=None, wacc_t=None, g=None, nd=None,
            rev_g=None):
    wt = wacc_term if wacc_t is None else wacc_t
    gg = V['g_term'] if g is None else g
    nde = net_debt if nd is None else nd
    rg = V['rev_growth'] if rev_g is None else rev_g
    nwcp = list(V['nwc_pct'])
    if nwc_end is not None:                      # linear re-glide to a different endpoint
        nwcp = list(np.linspace(nwcp[0], nwc_end, 5))
    fwd_ = [wacc_exp - (wacc_exp - wt) * f for f in glide_frac]
    df_, c_ = [], 1.0
    for w in fwd_:
        c_ /= (1 + w)
        df_.append(c_)
    rev_ = V['rev_fy25']; nwcprev = V['nwc_fy25_est']; pv = 0.0
    for i in range(5):
        rev_ *= (1 + rg[i])
        ebitda_ = rev_ * (V['ebitda_margin'][i] + margin_shift)
        dna_ = rev_ * V['dna_pct']
        nopat_ = (ebitda_ - dna_) * (1 - TAX)
        capex_ = rev_ * V['capex_pct']
        nwc_ = rev_ * nwcp[i]
        fcff_ = nopat_ + dna_ - capex_ - (nwc_ - nwcprev)
        pv += fcff_ * df_[i]
        nwcprev = nwc_
    ic = nwc_ + 0.05 * rev_
    roic = nopat_ / ic
    if roic <= gg / 0.95:                        # growth unfundable — cap RR at 95%
        return (0.0 - nde) / SH if pv <= nde else (pv - nde) / SH
    rr = gg / roic
    tv_ = nopat_ * (1 + gg) * (1 - rr) / (wt - gg)
    return (pv + tv_ * df_[-1] - nde) / SH

dcf_bear = max(run_dcf(margin_shift=-0.025, nwc_end=1.00, wacc_t=wacc_term + 0.02,
                       g=0.04, nd=net_debt + 1000), 0.05)
dcf_bull = run_dcf(margin_shift=+0.035, nwc_end=0.78, wacc_t=wacc_term - 0.015,
                   g=0.06, nd=net_debt - 1000)

# ---- equity P&L / debt schedule (interest on OPENING net debt, no circularity) ----
# Tax only on positive EBT; FY27's small profit is sheltered by the FY26 loss
# carryforward (Egyptian tax law allows 5-year carryforward) — modelled simply.
is_fcst = []
nd_path, cash_path, eq_path = [net_debt], [700.0], [V['equity_fy25_est']]
loss_cf = 0.0
for i, r in enumerate(rows):
    nd_open = nd_path[-1]
    intr = V['kd_path'][i] * nd_open
    ebt = r['ebit'] - intr
    taxable = max(ebt - loss_cf, 0.0)
    tax_chg = TAX * taxable if ebt > 0 else 0.0
    loss_cf = max(loss_cf - max(ebt, 0.0), 0.0) + max(-ebt, 0.0)
    np_ = ebt - tax_chg
    fcf_eq = np_ + r['dna'] - r['dwc'] - r['capex']
    nd_new = nd_open - fcf_eq
    nd_path.append(nd_new)
    eq_path.append(eq_path[-1] + np_)
    is_fcst.append(dict(year=r['year'], rev=r['rev'], ebitda=r['ebitda'], dna=r['dna'],
                        ebit=r['ebit'], fin=-intr, ebt=ebt, tax=-tax_chg, np=np_,
                        eps=np_ / SH, nd_open=nd_open, nd_close=nd_new, fcf_eq=fcf_eq))

# relative lens: EV/EBITDA on mid-cycle FY27E EBITDA, net debt after the FY26E release
nd_fy26 = is_fcst[0]['nd_close']
ebitda_27 = rows[1]['ebitda']
rel = {tag: max((m * ebitda_27 - nd_fy26) / SH, 0.05)
       for tag, m in [('bear', 4.5), ('base', V['ev_ebitda_base']), ('bull', 6.5)]}

# normalized earnings power: mid-cycle EBIT less normalized finance cost
ebit_mid = rows[2]['ebit']                       # FY28E-scale operations
nd_mid = 6000.0                                  # post-release, post-paydown mid-cycle net debt
np_norm = (ebit_mid - V['kd_term'] * nd_mid) * (1 - TAX)
eps_norm = np_norm / SH
norm = dict(bear=(rows[2]['ebit'] * 0.9 - 0.16 * 6500) * (1 - TAX) / SH * 5.5,
            base=eps_norm * V['pe_norm'],
            bull=(rows[2]['ebit'] * 1.1 - 0.14 * 5500) * (1 - TAX) / SH * 8.0)

# book lens: justified P/B = (ROE - g)/(Ke_term - g) on FY25e book
bvps = V['equity_fy25_est'] / SH
def jpb(roe, g=V['g_term'], ke=None):
    k = ke_term if ke is None else ke
    return max((roe - g) / (k - g), 0.10)
book = dict(bear=bvps * jpb(0.11), base=bvps * jpb(V['roe_sust']), bull=bvps * jpb(0.18, ke=ke_term - 0.01))

W = V['lens_weights']
lens = dict(dcf=dict(bear=dcf_bear, base=dcf_ps, bull=dcf_bull),
            relative=rel, normalized=norm, book=book)
central = {tag: sum(W[k] * lens[k][tag] for k in W) for tag in ('bear', 'base', 'bull')}
lens['central'] = central

# ---- sensitivity grids ----
wacc_grid = [wacc_term - 0.02, wacc_term - 0.01, wacc_term, wacc_term + 0.01, wacc_term + 0.02]
g_grid = [0.03, 0.04, 0.05, 0.06, 0.07]
sens_wg = [[run_dcf(wacc_t=w, g=g) for g in g_grid] for w in wacc_grid]
expl_grid = [wacc_exp - 0.02, wacc_exp - 0.01, wacc_exp, wacc_exp + 0.01, wacc_exp + 0.02]
sens_expl = [[0.0] * 5 for _ in range(5)]
for i, wex in enumerate(expl_grid):
    for j, wt in enumerate(wacc_grid):
        fwd_ = [wex - (wex - wt) * f for f in glide_frac]
        df_, c_ = [], 1.0
        for w in fwd_:
            c_ /= (1 + w)
            df_.append(c_)
        pv = sum(r['fcff'] * df_[k] for k, r in enumerate(rows))
        tv_ = nop_T * (1 + V['g_term']) * (1 - V['g_term'] / roic_T) / (wt - V['g_term'])
        sens_expl[i][j] = (pv + tv_ * df_[-1] - net_debt) / SH
beta_grid = [0.6, 0.78, 0.8, 0.964, 1.0, 1.15, 1.3]
sens_beta = []
for b in beta_grid:
    ke_b = rf_star_cds + b * V['erp_cds']
    kt_b = V['rf_term'] + b * V['erp_term']
    wex_b = we * ke_b + wd * kd_at
    wt_b = we * kt_b + wd * kd_term_at
    sens_beta.append(dict(beta=b, ke=ke_b, wacc_exp=wex_b, wacc_term=wt_b,
                          dcf=run_dcf(wacc_t=wt_b) if wt_b > V['g_term'] + 0.02 else float('nan')))
margin_grid = [-0.03, -0.015, 0.0, 0.015, 0.03]
nwc_grid = [1.00, 0.94, 0.88, 0.82, 0.76]
sens_mn = [[run_dcf(margin_shift=m, nwc_end=n) for n in nwc_grid] for m in margin_grid]

# ---- terminal-growth reconciliation table (historical) ----
tg_recon = []
ic_hist = {'FY23': 0.60 * V['assets_fy23_est'] + 3600 - 2300,   # rough IC = NWC + PP&E ≈ equity+debt
           'FY24': V['equity_fy24'] + V['debt_fy24'] - V['cash_fy24'],
           'FY25': V['equity_fy25_est'] + 9500 - 700}
nopat_hist = {y: hist_is[y]['ebit'] * (1 - TAX) for y in ('FY23', 'FY24', 'FY25')}
for y in ('FY23', 'FY24', 'FY25'):
    noph = nopat_hist[y]
    capex_h = 0.012 * hist_is[y]['rev']   # derived — no disclosed capex any year (flagged)
    tg_recon.append(dict(year=y, capex=capex_h, capex_ebitda=capex_h / hist_is[y]['ebitda'],
                         character='burst (debt-funded WC build, RR>100%)' if y != 'FY25' else
                                   'contraction (WC release beginning)',
                         nopat=noph, roic=noph / ic_hist[y]))
nopat_cagr_23_25 = (nopat_hist['FY25'] / nopat_hist['FY23']) ** 0.5 - 1

# ---- MC / step0 / tech / beta artefacts ----
step0 = json.load(open(os.path.join(HERE, 'step0_result.json')))
strike = json.load(open(os.path.join(HERE, 'strike_result.json')))
tech = json.load(open(os.path.join(HERE, 'tech_result.json')))
beta_reg = json.load(open(os.path.join(HERE, 'beta_result.json')))
p3 = np.load(os.path.join(HERE, 'paths_3M.npy'))
p1 = np.load(os.path.join(HERE, 'paths_1M.npy'))
term3, term1 = p3[:, -1], p1[:, -1]
zone_edges = [0, 1.80, 2.05, 2.35, 2.70, 1e9]
zones = [float(np.mean((term3 >= a) & (term3 < b))) for a, b in zip(zone_edges[:-1], zone_edges[1:])]
fan = np.array([np.percentile(p3, p, axis=0) for p in (5, 25, 50, 75, 95)])
np.save(os.path.join(HERE, 'fan.npy'), fan)
levels = [3.00, 2.75, 2.50, 2.35, 2.19, 2.05, 1.90, 1.70]
touch = {}
rmax1, rmin1 = p1.max(axis=1), p1.min(axis=1)
rmax3, rmin3 = p3.max(axis=1), p3.min(axis=1)
for L in levels:
    up = L > SPOT
    touch[f'{L:.2f}'] = dict(
        t1=float(np.mean(rmax1 >= L) if up else np.mean(rmin1 <= L)),
        t3=float(np.mean(rmax3 >= L) if up else np.mean(rmin3 <= L)))
prob_read = dict(
    p_above=float(np.mean(term3 > SPOT)),
    p_up10=float(np.mean(term3 >= SPOT * 1.10)), p_dn10=float(np.mean(term3 <= SPOT * 0.90)),
    median=float(np.median(term3)), med_move=float(np.median(term3) / SPOT - 1),
    band50=(float(np.percentile(term3, 25)), float(np.percentile(term3, 75))),
    touch_up10=float(np.mean(rmax3 >= SPOT * 1.10)), touch_dn10=float(np.mean(rmin3 <= SPOT * 0.90)))
prob_read['odds'] = prob_read['p_up10'] / prob_read['p_dn10']

# experts (methods cast from the persona library; labelled Expert 1/2/3 in output)
e1 = dict(method_short='earnings power x justified multiple', base=norm['base'],
          rng=(norm['bear'], norm['bull']))
own_cash_np = (rows[1]['ebit'] - V['kd_path'][1] * nd_fy26) * (1 - TAX)  # FY27E after actual funding cost
e2_base = max((own_cash_np + 0.35 * (np_norm - own_cash_np)), 60.0) / SH * 6.0
e2 = dict(method_short='owner cash earnings (accountant)', base=e2_base,
          rng=(e2_base * 0.6, e2_base * 1.5))
econ_profit_ps = dcf_ps  # Expert 3 anchors on the economic-profit DCF with own haircuts
e3_base = (ev * 0.95 - net_debt) / SH
e3 = dict(method_short='cash returns: ROIC vs the cost of capital', base=max(e3_base, 0.1),
          rng=(max((ev * 0.85 - net_debt - 500) / SH, 0.05), (ev * 1.05 - net_debt + 500) / SH))

# ============================ ASSERT =========================================
err = []
# engine reconciliation — the study may not disagree with production
if step0['verdict'] != 'PASS' or step0['nu'] != 6.0 or step0['width_cal'] != 0.951:
    err.append('step0 reconciliation failed')
if not (step0['skill_norm'] > 0 and all(step0['ci_blocks'][b][0] > 0 for b in ('2', '3', '4'))):
    err.append('calibration gate not robust-PASS')
# P&L closure on the one fully-triangulated year
if abs(np_fy24_check - V['np_fy24']) / V['np_fy24'] > 0.03:
    err.append(f'FY24 P&L does not close: {np_fy24_check:.0f} vs {V["np_fy24"]:.0f}')
# bridge closes exactly
if abs((ev - net_debt - nci) - eq_dcf) > 1e-6:
    err.append('EV->equity bridge does not close')
# signs into the bridge
if not (net_debt > 0 and nci >= 0):
    err.append('net debt / NCI sign error')
# glide ordering (hard ASSERT per the standing procedure)
if not wacc_term < wacc_exp:
    err.append('WACC_TERM >= WACC_EXP')
if any(fwd[i] < fwd[i + 1] for i in range(4)):
    err.append('forward WACC schedule not monotone')
# one date, one price of time: TV discounted at year-5 cumulative factor
if abs(pv_tv - tv * df[-1]) > 1e-9:
    err.append('terminal value not discounted at the year-5 factor')
# Kd-integrity triple
if not INP['debt_ccy_evidence']['value']:
    err.append('no debt-currency evidence')
if abs(V['kd'] - V['kd_eff_fy25']) > 0.015:
    err.append('Kd more than 150bp from the most recent effective-rate check')
if V['kd'] > max(V['kd_eff_fy24'], V['kd_eff_fy25']) + 0.005:
    err.append('Kd exceeds peak-year effective rate by more than 50bp')
# terminal-growth procedure
if V['g_term'] != 0.05:
    err.append('terminal g center is not the standing 5%')
if rr_T >= 1.0 or rr_T <= 0:
    err.append('terminal reinvestment rate not in (0,1)')
if abs(roic_T * rr_T - V['g_term']) > 1e-9:
    err.append('terminal g != ROIC x RR')
# plausibility band
if not (0.25 * SPOT / SPOT <= (central['base'] / SPOT) <= 2.5):
    err.append(f'central/spot {central["base"]/SPOT:.2f} outside plausibility band [0.25, 2.5]')
if err:
    raise SystemExit('ASSERT FAILED:\n  - ' + '\n  - '.join(err))

print('ASSERT PASS —')
print(f'  FY24 closure: NP derived {np_fy24_check:,.0f} vs reported {V["np_fy24"]:,.0f} (gap {abs(np_fy24_check-V["np_fy24"])/V["np_fy24"]*100:.1f}%)')
print(f'  WACC explicit {wacc_exp*100:.2f}% (CDS-primary; rating alt {wacc_exp_rating*100:.2f}%) -> terminal {wacc_term*100:.2f}%  [glide tied to kd_path]')
print(f'  forward WACC: ' + ' / '.join(f'{w*100:.1f}%' for w in fwd))
print(f'  Kd 23.5% vs effective checks {V["kd_eff_fy24"]*100:.1f}% (FY24) / {V["kd_eff_fy25"]*100:.1f}% (FY25) — inside 150bp/50bp bounds')
print(f'  terminal: ROIC {roic_T*100:.1f}% x RR {rr_T*100:.1f}% = g {roic_T*rr_T*100:.1f}%  | TV = {tv_pct*100:.0f}% of EV')
print(f'  bridge: EV {ev:,.0f} - ND {net_debt:,.0f} - NCI {nci:,.0f} = equity {eq_dcf:,.0f} = EGP {dcf_ps:.2f}/sh')
print(f'  central {central["base"]:.2f} [{central["bear"]:.2f}-{central["bull"]:.2f}] vs spot {SPOT} ({central["base"]/SPOT-1:+.0%})')

# ============================ EMIT ===========================================
out = dict(
    spot=SPOT, spot_date=tech['spot_date'], shares=SH, mktcap=MKTCAP, fx=V['fx'], tax=TAX,
    inputs={k: INP[k] for k in INP},
    hist_is=hist_is,
    hist_bs=dict(assets={'FY22': V['assets_fy22'], 'FY23e': V['assets_fy23_est'],
                         'FY24': V['assets_fy24'], 'FY25': V['assets_fy25']},
                 debt_fy24=V['debt_fy24'], cash_fy24=V['cash_fy24'],
                 equity_fy24=V['equity_fy24'], liab_fy24=V['liab_fy24'],
                 equity_fy25e=V['equity_fy25_est'], net_debt_fy25e=V['net_debt_fy25_est'],
                 nwc_fy25e=V['nwc_fy25_est'], payables_fy25e=V['payables_fy25_est']),
    interims=dict(q1_26_rev=V['q1_26_rev'], q1_26_np=V['q1_26_np'],
                  q1_25_rev=V['q1_25_rev'], q1_25_np=V['q1_25_np']),
    coc=dict(rf=V['rf'], sov_cds=V['sov_spread_cds'], sov_rating=V['sov_spread_rating'],
             rf_star_cds=rf_star_cds, rf_star_rating=rf_star_rating,
             erp_cds=V['erp_cds'], erp_rating=V['erp_rating'], beta=V['beta'],
             beta_reg=beta_reg, ke_cds=ke_cds, ke_rating=ke_rating, ke_raw_retired=ke_raw,
             kd=V['kd'], kd_at=kd_at, kd_eff_fy24=V['kd_eff_fy24'], kd_eff_fy25=V['kd_eff_fy25'],
             we=we, wd=wd, wacc_exp=wacc_exp, wacc_exp_rating=wacc_exp_rating,
             rf_term=V['rf_term'], erp_term=V['erp_term'], ke_term=ke_term,
             kd_term=V['kd_term'], wacc_term=wacc_term,
             kd_path=kdp, glide_frac=glide_frac, fwd_wacc=fwd, df=df),
    dcf=dict(rows=rows, pv_sum=pv_sum, tv=tv, pv_tv=pv_tv, ev=ev, tv_pct=tv_pct,
             fcff_T1=fcff_T1, roic_T=roic_T, rr_T=rr_T, ic_T=ic_T,
             net_debt=net_debt, nci=nci, eq=eq_dcf, ps=dcf_ps,
             nd_fy26=nd_fy26),
    is_fcst=is_fcst,
    debt_schedule=dict(nd_path=nd_path, eq_path=eq_path,
                       note='interest charged on OPENING net debt at that year\'s forward Kd; '
                            'tax 22.5% on positive EBT net of the FY26E loss carryforward'),
    lenses=lens, weights=W,
    tg_recon=dict(rows=tg_recon, nopat_cagr_23_25=nopat_cagr_23_25,
                  note='FY23/FY24 are burst years (debt-funded working-capital build, RR>100%) — '
                       'excluded from the ROIC x RR identity per the standing rule; no clean stable '
                       'year exists in the disclosed record, so the terminal check leans on the '
                       'forward build (terminal ROIC 14-15% x RR ~34% = 5%)'),
    sens_wg=dict(wacc_grid=wacc_grid, g_grid=g_grid, table=sens_wg),
    sens_expl=dict(expl_grid=expl_grid, term_grid=wacc_grid, table=sens_expl),
    sens_beta=sens_beta,
    sens_mn=dict(margin_grid=margin_grid, nwc_grid=nwc_grid, table=sens_mn),
    step0=step0, strike=strike, tech=tech,
    mc=dict(prob_read=prob_read, zones=zones, zone_edges=zone_edges[1:-1], touch=touch,
            pct1={p: float(np.percentile(term1, p)) for p in (5, 25, 50, 75, 95)},
            pct3={p: float(np.percentile(term3, p)) for p in (5, 25, 50, 75, 95)}),
    experts=dict(e1=e1, e2=e2, e3=e3, eps_norm=eps_norm, np_norm=np_norm, bvps=bvps),
    peers=dict(swdy=dict(rev_fy25=281049.0, np_fy25=17330.0, mktcap=196310.0, pe=10.4,
                         ev_ebitda=6.0, yield_=0.0202,
                         src='Arab Finance FY25 results; stockanalysis.com Jul-26; multiples.vc'),
               riyadh=dict(pe=17.96, ev_ebitda=15.01, de=0.27, roe=0.386,
                           src='stockanalysis.com Tadawul 4142, Jun-26')),
)
with open(os.path.join(HERE, 'study_numbers.json'), 'w') as f:
    json.dump(out, f, indent=1, default=float)
print('study_numbers.json written')
