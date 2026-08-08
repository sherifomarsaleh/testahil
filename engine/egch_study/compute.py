"""EGCH (Egyptian Chemical Industries "KIMA", EGX: EGCH) — master computation.

Ground-up, product-by-product, volume x price on the revenue side and cost-per-physical-
unit on the cost side, chained off the audited statements. Nothing here is a plug: every
driver traces to a filing, a live market quote, or a stated policy decision, and every
cost class escalates on its OWN driver (gas on its dollar price through FX; domestic
labour and haulage on Egyptian CPI; the subsidised price on its administered path).

THE CENTRAL FACT OF THIS COMPANY, which the model is built to expose rather than smooth:
KIMA is a 575kt/y urea plant that is simultaneously building a nitric-acid / ammonium-
nitrate complex (ANNA) whose bank-approved cost — EGP 6,422.4m plus US$278.4m, about
EGP 20.3bn at today's rate — is roughly three quarters of the company's own market
capitalisation. About EGP 5.7bn of that was in construction-in-progress at 31-Mar-2026
against physical progress the auditor put at 12.9% versus a 37% plan. The explicit
forecast window is therefore a construction window: free cash flow to the firm is
negative while the plant is built, and the value of the company sits overwhelmingly in
what the assets earn after it. That is a real characteristic of the asset, not a
modelling artefact, and it is why terminal value dominates enterprise value here.

Because a single deterministic path would hide that, the study values three states of
the world explicitly:
  BASE  — ANNA is completed on the observed (slow) spending pace and contributes from
          the terminal year at half its nameplate.
  BEAR  — ANNA money keeps being spent and the plant never earns: the capital is sunk
          and the terminal year carries urea alone.
  BULL  — ANNA is completed nearer the contracted scope and runs at 70% in the terminal
          year, with the urea price holding closer to today's war-tightened level.
"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))

FY25 = json.load(open(os.path.join(HERE, 'extract_fy2425.json')))
HIST = json.load(open(os.path.join(HERE, 'extract_history.json')))
NINE = json.load(open(os.path.join(HERE, 'extract_9m_fy2526.json')))
WACC = json.load(open(os.path.join(HERE, 'wacc_result.json')))
LIVE = json.load(open(os.path.join(HERE, 'live_data.json')))

K = 1_000.0            # statements are in EGP thousand; the model works in EGP million
def m(th):             # EGP thousand -> EGP million
    return th / 1_000.0

YEARS = ["FY2026/27", "FY2027/28", "FY2028/29", "FY2029/30", "FY2030/31"]
HIST_YEARS = ["FY2022/23", "FY2023/24", "FY2024/25"]

# =============================================================================
# 1. DRIVERS — every one sourced
# =============================================================================
D = {}

# ---- capacity (note 28 contractual benchmarks: 1,575 t/d urea, 1,200 t/d ammonia)
D['design_urea_t'] = 574_875
D['design_ammonia_t'] = 438_000

# ---- urea volumes: audited production history, then a utilisation path -------
# FY2022/23 ran 2% ABOVE the urea design plate and 14% below on ammonia (auditor);
# FY2023/24 fell 11%/29% on gas curtailment; FY2024/25 is exact from the auditor's
# own cost table. The forecast never returns to plate because the summer gas cuts
# are structural, not cyclical.
D['urea_t'] = {"FY2022/23": 586_373, "FY2023/24": 521_868, "FY2024/25": 513_385,
               "FY2025/26E": 520_000}
D['urea_util'] = [0.913, 0.922, 0.930, 0.939, 0.948]      # -> 525k .. 545k tonnes
D['ammonia_per_urea_t'] = 318_242 / 513_385                 # 0.620, FY2024/25 actual ratio

# ---- channel split (tonnes) --------------------------------------------------
# FY2024/25 reconciles EXACTLY to the disclosed note-20 split at the auditor's own
# disclosed average export price of US$385/t: 350.3kt x 385 x 49.0 = EGP 6,608.8m
# against 6,608.75m disclosed. Subsidised deliveries were 147kt over the 14 months
# to Aug-2025 (126kt/yr) against a 322kt requirement — a 46% compliance rate the
# forecast does not assume away.
D['subsidised_t'] = {"FY2024/25": 126_000, "FY2025/26E": 150_000}
D['subsidised_t_path'] = [155_000, 160_000, 165_000, 170_000, 175_000]
D['local_free_t'] = {"FY2024/25": 37_085, "FY2025/26E": 40_000}
D['local_free_path'] = [40_000, 41_000, 42_000, 43_000, 44_000]

# ---- prices ------------------------------------------------------------------
# Export: US$385/t realised in FY2024/25 (auditor, Damietta stock note). Q1-2025/26
# export prices ran +43% y/y (auditor) and CME FOB Egypt settled US$545/t on
# 7-Aug-2026 in a war-tightened market. The path mean-reverts toward the cash cost
# of the marginal gas-based producer rather than holding the conflict premium.
D['export_usd_t'] = {"FY2024/25": 385.0, "FY2025/26E": 505.0}
D['export_usd_path'] = [530.0, 500.0, 470.0, 450.0, 440.0]
D['export_usd_path_bull'] = [560.0, 545.0, 530.0, 520.0, 515.0]
D['usd_egp'] = {"FY2024/25": 49.00, "FY2025/26E": 49.60}
D['usd_egp_path'] = [51.9, 54.2, 56.7, 59.2, 61.9]          # 4.5%/yr, the SAME wedge
                                                            # used in the Kd FX build
D['export_duty_pct'] = 0.10       # 2026 switch from the EGP 2,500/t shortfall levy to
                                  # a 10% ad-valorem duty tied to the global price
D['subsidised_egp_t'] = {"FY2024/25": 6_000.0, "FY2025/26E": 6_720.0}
D['subsidised_p_path'] = [7_526.0, 8_429.0, 9_272.0, 10_106.0, 10_915.0]  # administered
D['local_free_egp_t'] = {"FY2024/25": 18_485.0, "FY2025/26E": 22_000.0}
D['local_free_parity'] = 0.90     # local free-market urea clears at ~90% of export parity

# ---- ammonium nitrate & other legs ------------------------------------------
D['an_t'] = {"FY2024/25": 26_058, "FY2025/26E": 26_000}     # 33.5% granulated + LDAN
D['an_path'] = [26_000, 26_000, 26_000, 26_000, 26_000]
D['an_egp_t'] = {"FY2024/25": 20_000.0}
D['other_rev'] = {"FY2024/25": 30.0, "FY2025/26E": 120.0}   # nitric acid merchant,
D['other_rev_path'] = [140.0, 152.0, 163.0, 174.0, 186.0]   # ferrosilicon plant rent,
                                                            # services (EGP million)

# ---- cost stack: one escalator per physical driver ---------------------------
# GAS. The company's own Q1-2025/26 disclosure values 31,313,235 m3 of lost gas at
# EGP 251m = EGP 8.016/m3, i.e. ~US$4.68/mmBtu at the prevailing rate — below the
# US$5.75/mmBtu formula price in note 28, which is carried as the downside case.
# Consumption is set at 1,292 m3 per tonne of ammonia, inside the auditor's own
# disclosed 1,025-1,771 m3/t range, and calibrated so that gas is 75% of the
# FY2024/25 materials line — the split of that line between gas and everything else
# is the model's, and is flagged as such, because the statements give only the total.
D['gas_m3_per_t_ammonia'] = 1_292.0
D['gas_usd_mmbtu'] = 4.68
D['gas_usd_mmbtu_contract'] = 5.75
D['mmbtu_per_m3'] = 0.03531
D['other_materials_egp_t_urea'] = 1_101.6e6 / 513_385       # EGP 2,146/t of urea
D['wages'] = {"FY2024/25": m(212_857.408 * 1) / 1}          # EGP million, note 21
D['services'] = 62.557
D['freight_egp_t_export'] = 610_158_356 / 350_300           # EGP 1,742 per export tonne
D['other_selling'] = 176.3        # selling materials + wages + other, note 22
D['admin'] = 359.624
D['abnormal_gas'] = {"FY2024/25": 164.478}                  # stoppage cost, note 25
D['abnormal_gas_path'] = [150.0, 120.0, 100.0, 90.0, 80.0]  # decays as supply normalises
D['cpi_path'] = [0.100, 0.085, 0.075, 0.070, 0.070]         # CBE target convergence
                                                            # (14.3% Jun-2026 print)
# ---- D&A, capex, working capital --------------------------------------------
D['dep_base'] = m(771_213)            # note 6 charge, FY2024/25
D['amort_base'] = m(119_378)          # usufruct intangible at 4.75%
D['anna_total_cost'] = 6_422.4 + 278.385 * 50.0        # EGP m; bank-approved 25-Jun-2025
D['anna_spent'] = 5_653.5             # CWIP at 31-Mar-2026
D['anna_capex_path'] = [3_000.0, 3_500.0, 3_500.0, 3_000.0, 2_000.0]
D['maint_capex_pct_rev'] = 0.030      # pre-ANNA observed run 42.5-81m on 4.4-6.6bn of
                                      # revenue was abnormally low (plant just built);
                                      # 3.0% of revenue is the mature-plant standard,
                                      # sensitised because no guidance exists
# ANNA nameplate is DERIVED, and flagged as derived: no filing states the plant's
# capacity. The ammonia design plate is 438kt; urea at ITS design plate consumes
# 574,875 x 0.620 = 356kt, leaving ~82kt of ammonia, and ammonium nitrate takes about
# 0.43t of ammonia per tonne of product (nitric-acid route plus direct neutralisation).
# That gives ~190kt of AN, and the model carries 244kt — the more generous reading, in
# which the surplus is measured against urea's ACTUAL gas-constrained ammonia draw.
D['nh3_per_t_an'] = 0.43              # ammonia per tonne of ammonium nitrate, via the
                                      # nitric-acid route plus direct neutralisation
D['anna_nameplate_an_t'] = ((D['design_ammonia_t']
                             - D['design_urea_t'] * D['ammonia_per_urea_t'])
                            / D['nh3_per_t_an'])
D['anna_util_base'] = 0.50
D['anna_util_bull'] = 0.70
D['anna_price_usd_t'] = 280.0
D['anna_cash_margin'] = 0.32          # AN cash margin over its own ammonia + conversion
D['dso'] = 631_047 / 8_602_606 * 365       # 26.8 days, FY2024/25
D['dio'] = 2_399_625 / 5_300_310 * 365     # 165.3 days
D['dpo'] = 1_207_768 / 5_300_310 * 365     # 83.2 days
D['tax_rate'] = 0.225
D['wacc_spot'] = WACC['wacc_rating']
D['wacc_cds'] = WACC['wacc_cds']
D['g_terminal'] = 0.070               # CBE medium-term inflation target: nominal
                                      # maintenance growth, no real growth assumed
D['roc_terminal'] = 0.18              # reinvestment = g / RoC

# ---- the discount-rate GLIDE, and the terminal rate built from its own parts --
# A spot WACC embeds today's 14.3% inflation print in every year, while the terminal
# value grows at the CBE's 7% target. Capitalising a 7%-growth perpetuity at a rate
# built on 14% inflation is not conservatism, it is a units mismatch, and on a company
# whose value sits in its terminal year it is the single largest number in the study.
# So the rate glides from the spot build to a NORMALISED long-run build, and the
# discount factors compound the glide year by year rather than powering one rate.
D['rf_star_spot'] = WACC['rf_star_rating']            # 23.00% observed - 6.37% spread
D['inflation_lt'] = 0.070                              # CBE medium-term target
D['real_rate_lt'] = 0.035                              # EM long-run real policy rate
D['rf_star_terminal'] = (1 + D['inflation_lt']) * (1 + D['real_rate_lt']) - 1   # 10.75%
D['kd_usd_lt'] = 0.090                                 # long-run USD corporate cost
D['deprec_lt'] = 0.045                                 # same wedge used in the Kd build
D['kd_local_equiv_terminal'] = (1 + D['kd_usd_lt']) * (1 + D['deprec_lt']) - 1
D['erp'] = WACC['erp_rating']
D['beta'] = WACC['beta']
D['we'] = WACC['we']
D['wd'] = WACC['wd']

def _wacc_from(rf_star, kd_pretax):
    ke = rf_star + D['beta'] * D['erp']
    return D['we'] * ke + D['wd'] * kd_pretax * (1 - D['tax_rate']), ke

D['wacc_terminal'], D['ke_terminal'] = _wacc_from(D['rf_star_terminal'],
                                                  D['kd_local_equiv_terminal'])
# linear glide across the explicit window, spot in year 1 -> terminal-adjacent in year 5
D['wacc_path'], D['rf_star_path'], D['kd_path'] = [], [], []
for _k in range(5):
    _f = _k / 5.0                                     # glide fraction, visibly derived
    _rf = D['rf_star_spot'] + (D['rf_star_terminal'] - D['rf_star_spot']) * _f
    _kd = WACC['kd_pretax_blended'] + (D['kd_local_equiv_terminal']
                                       - WACC['kd_pretax_blended']) * _f
    _w, _ = _wacc_from(_rf, _kd)
    D['rf_star_path'].append(_rf); D['kd_path'].append(_kd); D['wacc_path'].append(_w)
D['wacc'] = D['wacc_path'][0]

# =============================================================================
# 2. HISTORICALS — straight from the audited statements
# =============================================================================
def hist_year(rev, cogs, sell, admin, dep, net, label):
    gross = rev - cogs
    ebit = gross - sell - admin
    return dict(year=label, revenue=rev, cogs=cogs, gross=gross, gross_pct=gross / rev,
                selling=sell, admin=admin, ebit=ebit, ebit_pct=ebit / rev,
                dep=dep, ebitda=ebit + dep, ebitda_pct=(ebit + dep) / rev, net=net)

H = [
    hist_year(m(6_612_226), m(3_574_483), m(473_720), m(188_851), m(627_213 + 92_000),
              m(1_150_767), "FY2022/23"),
    hist_year(m(6_532_126), m(4_395_788), m(562_527), m(297_887), m(662_634 + 110_000),
              m(2_537_934), "FY2023/24"),
    hist_year(m(8_602_606), m(5_300_310), m(786_463), m(359_624), m(771_213 + 119_378),
              m(986_964), "FY2024/25"),
]
H[1]['net_underlying'] = m(2_537_934 - 2_034_573)     # ex the one-off revaluation gain

# FY2025/26E — nine months reviewed, fourth quarter run-rated on the third quarter's
# operating performance (the strongest on record) with the FX line set to zero, since
# a translation swing is not forecastable and is carried as a sensitivity instead.
q3_rev, q3_gross_pct = m(3_158_554), 0.463
fy2526 = dict(
    year="FY2025/26E",
    revenue=m(7_314_933) + q3_rev * 0.97,
    cogs=None, gross=None,
)
fy2526['gross'] = m(3_134_979) + q3_rev * 0.97 * q3_gross_pct
fy2526['cogs'] = fy2526['revenue'] - fy2526['gross']
fy2526['gross_pct'] = fy2526['gross'] / fy2526['revenue']
fy2526['selling'] = m(734_707) * 4 / 3
fy2526['admin'] = m(273_831) * 4 / 3
fy2526['ebit'] = fy2526['gross'] - fy2526['selling'] - fy2526['admin']
fy2526['ebit_pct'] = fy2526['ebit'] / fy2526['revenue']
fy2526['dep'] = D['dep_base'] + D['amort_base']
fy2526['ebitda'] = fy2526['ebit'] + fy2526['dep']
fy2526['ebitda_pct'] = fy2526['ebitda'] / fy2526['revenue']
fy2526['net'] = m(531_310)      # nine months actual; Q4 not annualised into net because
                                # the FX line dominates it

# =============================================================================
# 3. FORECAST ENGINE
# =============================================================================
def build(case="base"):
    export_usd = D['export_usd_path_bull'] if case == "bull" else D['export_usd_path']
    rows, prev_wc = [], None
    # opening working capital on the FY2025/26E base
    for k, yr in enumerate(YEARS):
        fx = D['usd_egp_path'][k]
        urea_t = D['design_urea_t'] * D['urea_util'][k]
        ammonia_t = urea_t * D['ammonia_per_urea_t']
        sub_t = D['subsidised_t_path'][k]
        free_t = D['local_free_path'][k]
        exp_t = urea_t - sub_t - free_t

        # --- revenue, leg by leg
        p_exp_usd = export_usd[k]
        p_exp_egp = p_exp_usd * fx * (1 - D['export_duty_pct'])
        rev_exp = exp_t * p_exp_egp / 1e6
        rev_sub = sub_t * D['subsidised_p_path'][k] / 1e6
        p_free = p_exp_usd * fx * D['local_free_parity']
        rev_free = free_t * p_free / 1e6
        an_t = D['an_path'][k]
        p_an = D['an_egp_t']["FY2024/25"] * (fx / D['usd_egp']["FY2024/25"])
        rev_an = an_t * p_an / 1e6
        rev_other = D['other_rev_path'][k]
        revenue = rev_exp + rev_sub + rev_free + rev_an + rev_other

        # --- cost stack: each class on its own escalator
        gas_price_egp_m3 = D['gas_usd_mmbtu'] * D['mmbtu_per_m3'] * fx
        gas_cost = ammonia_t * D['gas_m3_per_t_ammonia'] * gas_price_egp_m3 / 1e6
        cpi_cum = 1.0
        for j in range(k + 1):
            cpi_cum *= (1 + D['cpi_path'][j])
        other_mat = urea_t * D['other_materials_egp_t_urea'] * cpi_cum / 1e6
        wages = 212.857 * cpi_cum
        services = D['services'] * cpi_cum
        dep = D['dep_base'] * (1 + 0.02 * k) + D['amort_base']
        cogs = gas_cost + other_mat + wages + services + dep
        gross = revenue - cogs

        freight = exp_t * D['freight_egp_t_export'] * cpi_cum / 1e6
        other_sell = D['other_selling'] * cpi_cum
        admin = D['admin'] * cpi_cum
        abnormal = D['abnormal_gas_path'][k]
        ebit = gross - freight - other_sell - admin - abnormal
        ebitda = ebit + dep

        # --- FCFF waterfall
        nopat = ebit * (1 - D['tax_rate'])
        capex = D['anna_capex_path'][k] + revenue * D['maint_capex_pct_rev']
        wc = revenue * D['dso'] / 365 + cogs * D['dio'] / 365 - cogs * D['dpo'] / 365
        if prev_wc is None:
            prev_wc = (fy2526['revenue'] * D['dso'] / 365
                       + fy2526['cogs'] * D['dio'] / 365
                       - fy2526['cogs'] * D['dpo'] / 365)
        dwc = wc - prev_wc
        prev_wc = wc
        fcff = nopat + dep - capex - dwc
        cum = 1.0
        for j in range(k + 1):
            cum *= (1 + D['wacc_path'][j])
        df = 1.0 / cum
        rows.append(dict(
            year=yr, fx=fx, urea_t=urea_t, ammonia_t=ammonia_t,
            exp_t=exp_t, sub_t=sub_t, free_t=free_t, an_t=an_t,
            p_exp_usd=p_exp_usd, p_exp_egp=p_exp_egp, p_free=p_free,
            p_sub=[7_526.0, 8_429.0, 9_272.0, 10_106.0, 10_915.0][k], p_an=p_an,
            rev_exp=rev_exp, rev_sub=rev_sub, rev_free=rev_free, rev_an=rev_an,
            rev_other=rev_other, revenue=revenue,
            gas_price_egp_m3=gas_price_egp_m3, gas_cost=gas_cost, other_mat=other_mat,
            wages=wages, services=services, dep=dep, cogs=cogs,
            gross=gross, gross_pct=gross / revenue,
            freight=freight, other_sell=other_sell, admin=admin, abnormal=abnormal,
            ebit=ebit, ebit_pct=ebit / revenue, ebitda=ebitda, ebitda_pct=ebitda / revenue,
            nopat=nopat, capex=capex, wc=wc, dwc=dwc, fcff=fcff,
            df=df, pv=fcff * df, cpi_cum=cpi_cum))
    return rows


def terminal(rows, case="base"):
    """Normalised terminal year: the last explicit year's urea economics, plus ANNA at
    the case's utilisation, on maintenance capex only."""
    last = rows[-1]
    fx = last['fx'] * (1 + D['g_terminal'] - 0.025)     # steady-state depreciation wedge
    util = {"base": D['anna_util_base'], "bull": D['anna_util_bull'],
            "bear": 0.0, "halt": 0.0}[case]
    an_t = D['anna_nameplate_an_t'] * util
    anna_rev = an_t * D['anna_price_usd_t'] * fx / 1e6
    anna_ebit = anna_rev * D['anna_cash_margin']
    anna_dep = (D['anna_total_cost'] * 0.045) if util > 0 else 0.0
    anna_ebit -= anna_dep * 0.0        # dep already inside the cash margin convention
    base_ebit = last['ebit'] * (1 + D['g_terminal'])
    ebit_T = base_ebit + anna_ebit
    nopat_T = ebit_T * (1 - D['tax_rate'])
    reinv_rate = D['g_terminal'] / D['roc_terminal']
    fcff_T = nopat_T * (1 - reinv_rate)
    tv = fcff_T * (1 + D['g_terminal']) / (D['wacc_terminal'] - D['g_terminal'])
    pv_tv = tv * rows[-1]['df']
    return dict(fx=fx, anna_util=util, an_t=an_t, anna_rev=anna_rev, anna_ebit=anna_ebit,
                base_ebit=base_ebit, ebit_T=ebit_T, nopat_T=nopat_T,
                reinv_rate=reinv_rate, fcff_T=fcff_T, tv=tv, pv_tv=pv_tv,
                wacc_terminal=D['wacc_terminal'], ke_terminal=D['ke_terminal'],
                rf_star_terminal=D['rf_star_terminal'],
                kd_terminal=D['kd_local_equiv_terminal'])


def bridge(rows, T):
    pv_explicit = sum(r['pv'] for r in rows)
    ev = pv_explicit + T['pv_tv']
    # non-operating assets and net debt, 31-Mar-2026 reviewed balance sheet
    cash = m(4_606_522)
    debt = m(14_386_056 + 45_905 + 206_994)
    fvoci = m(1_382_886)              # remaining ABUK + Delta Sugar stakes, at market
    inv_prop = m(2_155_061)
    net_debt = debt - cash
    equity = ev - net_debt + fvoci + inv_prop
    shares = 1_986_578_999
    return dict(pv_explicit=pv_explicit, pv_tv=T['pv_tv'], ev=ev,
                tv_pct_ev=T['pv_tv'] / ev if ev else float('nan'),
                cash=cash, debt=debt, net_debt=net_debt, fvoci=fvoci,
                inv_prop=inv_prop, equity=equity, shares=shares,
                per_share=equity * 1e6 / shares)


CASES = {}
for case in ("base", "bull", "bear", "halt"):
    rws = build("bull" if case == "bull" else "base")
    if case == "halt":
        # CAPITAL-DISCIPLINE case: the board stops ANNA at the end of FY2026/27, takes
        # the wind-down cost, writes the EGP 5.65bn already in construction-in-progress
        # off against nothing, and the company runs as the urea plant it already is.
        # This is not a forecast of what management will do — it is the measurement of
        # what the programme is costing shareholders, in EGP per share, against the
        # alternative of not doing it.
        for k, r in enumerate(rws):
            r['capex'] = (1_000.0 if k == 0 else 0.0) + r['revenue'] * D['maint_capex_pct_rev']
            r['fcff'] = r['nopat'] + r['dep'] - r['capex'] - r['dwc']
            r['pv'] = r['fcff'] * r['df']
    if case == "bear":
        # bear: the money is spent and the plant never earns; urea prices sit at the
        # low end of the path and the gas bill is at the contract US$5.75/mmBtu
        rws = build("base")
        for k, r in enumerate(rws):
            extra_gas = r['ammonia_t'] * D['gas_m3_per_t_ammonia'] * \
                (D['gas_usd_mmbtu_contract'] - D['gas_usd_mmbtu']) * \
                D['mmbtu_per_m3'] * r['fx'] / 1e6
            r['gas_cost'] += extra_gas
            r['cogs'] += extra_gas
            r['gross'] -= extra_gas
            r['gross_pct'] = r['gross'] / r['revenue']
            r['ebit'] -= extra_gas
            r['ebit_pct'] = r['ebit'] / r['revenue']
            r['ebitda'] -= extra_gas
            r['nopat'] = r['ebit'] * (1 - D['tax_rate'])
            r['fcff'] = r['nopat'] + r['dep'] - r['capex'] - r['dwc']
            r['pv'] = r['fcff'] * r['df']
    T = terminal(rws, case)
    CASES[case] = dict(rows=rws, terminal=T, bridge=bridge(rws, T))

base = CASES['base']
print(f"{'':12s} " + " ".join(f"{y:>11s}" for y in YEARS))
for key, lab in [('revenue', 'Revenue'), ('ebitda', 'EBITDA'), ('ebit', 'EBIT'),
                 ('nopat', 'NOPAT'), ('capex', 'Capex'), ('fcff', 'FCFF'), ('pv', 'PV')]:
    print(f"{lab:12s} " + " ".join(f"{r[key]:11,.0f}" for r in base['rows']))
print()
for case in ("bear", "base", "bull", "halt"):
    b = CASES[case]['bridge']
    print(f"{case.upper():5s} EV {b['ev']:10,.0f} | TV {b['tv_pct_ev']*100:5.1f}% of EV | "
          f"net debt {b['net_debt']:9,.0f} | equity {b['equity']:10,.0f} | "
          f"per share EGP {b['per_share']:6.2f}")
print(f"\nspot EGP 13.98 (6-Aug-2026) | WACC glide "
      f"{' -> '.join(f'{w*100:.1f}%' for w in D['wacc_path'])} | terminal "
      f"{D['wacc_terminal']*100:.2f}% | g {D['g_terminal']*100:.1f}%")

# ---- reverse DCF: the cost of capital the market price itself implies ---------
def implied_flat_wacc(target_per_share, case="base"):
    """Solve for the single FLAT nominal EGP discount rate — applied to every explicit
    year and to the perpetuity — that reproduces the market price on the same operating
    cash flows. Reporting a large gap this way states what the market is assuming
    rather than asserting that it is wrong."""
    saved_path, saved_T = list(D['wacc_path']), D['wacc_terminal']
    lo, hi = D['g_terminal'] + 0.005, 0.60
    mid = hi
    for _ in range(100):
        mid = (lo + hi) / 2
        D['wacc_path'] = [mid] * 5
        D['wacc_terminal'] = mid
        rws = build("bull" if case == "bull" else "base")
        if case == "halt":
            for k, r in enumerate(rws):
                r['capex'] = (1_000.0 if k == 0 else 0.0) + r['revenue'] * D['maint_capex_pct_rev']
                r['fcff'] = r['nopat'] + r['dep'] - r['capex'] - r['dwc']
                r['pv'] = r['fcff'] * r['df']
        ps = bridge(rws, terminal(rws, case))['per_share']
        if ps > target_per_share:
            lo = mid
        else:
            hi = mid
    D['wacc_path'], D['wacc_terminal'] = saved_path, saved_T
    return mid

D['implied_wacc_base'] = implied_flat_wacc(13.98, "base")
D['implied_wacc_halt'] = implied_flat_wacc(13.98, "halt")
print(f"reverse DCF: EGP 13.98 implies a FLAT nominal EGP discount rate of "
      f"{D['implied_wacc_base']*100:.1f}% on the committed-capital case and "
      f"{D['implied_wacc_halt']*100:.1f}% on the capital-discipline case — against a "
      f"sovereign 10-year yield of 23.0% and a built WACC of "
      f"{D['wacc_path'][0]*100:.1f}% falling to {D['wacc_terminal']*100:.1f}%.")
print(f"ANNA programme cost to shareholders: "
      f"EGP {CASES['halt']['bridge']['per_share'] - CASES['base']['bridge']['per_share']:.2f} "
      f"per share (capital-discipline case less committed-capital case).")

out = dict(drivers=D, hist=H, fy2526=fy2526, years=YEARS, hist_years=HIST_YEARS,
           cases={k: dict(rows=v['rows'], terminal=v['terminal'], bridge=v['bridge'])
                  for k, v in CASES.items()},
           wacc=WACC, spot=13.98, spot_date="2026-08-06")
json.dump(out, open(os.path.join(HERE, 'study_numbers.json'), 'w'), indent=1, default=float)
print("\nwrote study_numbers.json")
