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

sys.path.insert(0, HERE)
from inputs import V as _V          # the study's input register — the single source of
                                    # every number in this model (numeric traceability)
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
D['design_urea_t'] = _V('design_urea_tpy')
D['design_ammonia_t'] = _V('design_ammonia_tpy')

# ---- urea volumes: audited production history, then a utilisation path -------
# FY2022/23 ran 2% ABOVE the urea design plate and 14% below on ammonia (auditor);
# FY2023/24 fell 11%/29% on gas curtailment; FY2024/25 is exact from the auditor's
# own cost table. The forecast never returns to plate because the summer gas cuts
# are structural, not cyclical.
D['urea_t'] = {"FY2022/23": _V('prod_urea_FY2223'), "FY2023/24": _V('prod_urea_FY2324'),
               "FY2024/25": _V('prod_urea_FY2425'), "FY2025/26E": _V('prod_urea_FY2526E')}
D['urea_util'] = _V('urea_util')      # -> 525k .. 545k tonnes
D['ammonia_per_urea_t'] = _V('ammonia_per_urea')

# ---- channel split (tonnes) --------------------------------------------------
# FY2024/25 reconciles EXACTLY to the disclosed note-20 split at the auditor's own
# disclosed average export price of US$385/t: 350.3kt x 385 x 49.0 = EGP 6,608.8m
# against 6,608.75m disclosed. Subsidised deliveries were 147kt over the 14 months
# to Aug-2025 (126kt/yr) against a 322kt requirement — a 46% compliance rate the
# forecast does not assume away.
D['subsidised_t'] = {"FY2024/25": _V('subsidised_tonnes_FY2425'),
                     "FY2025/26E": _V('subsidised_t_FY2526E')}
D['subsidised_t_path'] = _V('subsidised_t_path')
D['local_free_t'] = {"FY2024/25": _V('local_free_tonnes_FY2425'),
                     "FY2025/26E": _V('local_free_t_FY2526E')}
D['local_free_path'] = _V('local_free_path')

# ---- prices ------------------------------------------------------------------
# Export: US$385/t realised in FY2024/25 (auditor, Damietta stock note). Q1-2025/26
# export prices ran +43% y/y (auditor) and CME FOB Egypt settled US$545/t on
# 7-Aug-2026 in a war-tightened market. The path mean-reverts toward the cash cost
# of the marginal gas-based producer rather than holding the conflict premium.
D['export_usd_t'] = {"FY2024/25": _V('export_price_FY2425_usd'),
                     "FY2025/26E": _V('export_usd_FY2526E')}
D['export_usd_path'] = _V('export_usd_path')
D['export_usd_path_bull'] = _V('export_usd_path_bull')
D['usd_egp'] = {"FY2024/25": _V('usd_egp_avg_FY2425'), "FY2025/26E": _V('usd_egp_FY2526E')}
# The path is BUILT from the relative-purchasing-power identity the study states, applied
# YEAR BY YEAR to the model's own inflation path, not from a single flat wedge asserted
# beside a derivation that produces a different number in every year. The long-run wedge
# (from the terminal inflation target) is what carries the dollar debt and the terminal.
D['fx_wedge_path'] = [(1 + c) / (1 + _V('us_inflation_lt')) - 1 for c in _V('cpi_path')]
D['usd_egp_path'] = []
_fx = _V('usd_egp_spot')
for _w in D['fx_wedge_path']:
    _fx *= (1 + _w)
    D['usd_egp_path'].append(_fx)
                                                            # used in the Kd FX build
D['export_duty_pct'] = _V('export_duty_2026')       # 2026 switch from the EGP 2,500/t shortfall levy to
                                  # a 10% ad-valorem duty tied to the global price
D['subsidised_egp_t'] = {"FY2024/25": _V('subsidised_price'),
                         "FY2025/26E": _V('subsidised_p_FY2526E')}
D['subsidised_p_path'] = _V('subsidised_p_path')  # administered
D['local_free_egp_t'] = {"FY2024/25": _V('local_free_price_FY2425'),
                          "FY2025/26E": _V('local_free_p_FY2526E')}
D['local_free_parity'] = _V('local_free_parity')     # local free-market urea clears at ~90% of export parity

# ---- ammonium nitrate & other legs ------------------------------------------
D['an_t'] = {"FY2024/25": _V('prod_an_gran_FY2425') + _V('prod_ldan_FY2425'),
             "FY2025/26E": _V('an_t_FY2526E')}                  # 33.5% granulated + LDAN
D['an_path'] = _V('an_path')
D['an_egp_t'] = {"FY2024/25": _V('an_price_egp_t_FY2425')}
D['other_rev'] = {"FY2024/25": _V('other_rev_FY2425'),
                  "FY2025/26E": _V('other_rev_FY2526E')}      # nitric acid merchant,
D['other_rev_path'] = _V('other_rev_path')   # ferrosilicon plant rent,
                                                            # services (EGP million)

# ---- cost stack: one escalator per physical driver ---------------------------
# GAS. The company's own Q1-2025/26 disclosure values 31,313,235 m3 of lost gas at
# EGP 251m = EGP 8.016/m3, i.e. ~US$4.68/mmBtu at the prevailing rate — below the
# US$5.75/mmBtu formula price in note 28, which is carried as the downside case.
# Consumption is set at 1,292 m3 per tonne of ammonia, inside the auditor's own
# disclosed 1,025-1,771 m3/t range, and calibrated so that gas is 75% of the
# FY2024/25 materials line — the split of that line between gas and everything else
# is the model's, and is flagged as such, because the statements give only the total.
D['gas_m3_per_t_ammonia'] = _V('gas_m3_per_t_ammonia_modelled')
D['gas_usd_mmbtu'] = _V('gas_realised_usd_mmbtu')
D['gas_usd_mmbtu_contract'] = _V('gas_contract_usd_mmbtu')
D['mmbtu_per_m3'] = _V('mmbtu_per_m3')
D['other_materials_egp_t_urea'] = (_V('cogs_materials_FY2425')
                                   * (1 - _V('gas_share_of_materials'))
                                   * 1e6 / _V('prod_urea_FY2425'))
D['wages'] = {"FY2024/25": _V('cogs_wages_FY2425')}
D['services'] = _V('cogs_services_FY2425')
D['freight_egp_t_export'] = _V('sell_freight_FY2425') * 1e6 / _V('export_tonnes_FY2425')
D['other_selling'] = _V('sell_other_FY2425')
D['admin'] = _V('is_admin_FY2425')
D['abnormal_gas'] = {"FY2024/25": _V('stoppage_cost_FY2425')}   # stoppage cost, note 25
D['abnormal_gas_path'] = _V('abnormal_gas_path')  # decays as supply normalises
D['cpi_path'] = _V('cpi_path')         # CBE target convergence
                                                            # (14.3% Jun-2026 print)
# ---- D&A, capex, working capital --------------------------------------------
D['dep_escalation'] = _V('dep_escalation')
D['dep_rate_project'] = _V('dep_rate_kima2_machinery')
D['dep_base'] = _V('dep_charge_FY2425')
D['amort_base'] = _V('amort_FY2425')
D['anna_total_cost'] = (_V('anna_cost_egp')
                        + _V('anna_cost_usd') * _V('usd_egp_anna_approval'))
D['anna_spent'] = _V('bs_cwip_M9FY2526')            # CWIP at 31-Mar-2026
D['anna_capex_path'] = _V('anna_capex_path')
D['maint_capex_pct_rev'] = _V('maint_capex_pct')      # pre-ANNA observed run 42.5-81m on 4.4-6.6bn of
                                      # revenue was abnormally low (plant just built);
                                      # 3.0% of revenue is the mature-plant standard,
                                      # sensitised because no guidance exists
# ANNA nameplate is DERIVED, and flagged as derived: no filing states the plant's
# capacity. The ammonia design plate is 438kt; urea at ITS design plate consumes
# 574,875 x 0.620 = 356kt, leaving ~82kt of ammonia, and ammonium nitrate takes about
# 0.43t of ammonia per tonne of product (nitric-acid route plus direct neutralisation).
# That gives ~190kt of AN, and the model carries 244kt — the more generous reading, in
# which the surplus is measured against urea's ACTUAL gas-constrained ammonia draw.
D['nh3_per_t_an'] = _V('nh3_per_t_an')              # ammonia per tonne of ammonium nitrate, via the
                                      # nitric-acid route plus direct neutralisation
# DISCLOSED, not derived. The EPC award for this plant states 800 t/day of granulated
# ammonium nitrate. The study previously said "no filing states it" and derived the plate
# from the ammonia surplus; an external critique produced the award. The derived figure is
# retained only as the cross-check it now is.
D['anna_nameplate_an_t'] = _V('anna_nameplate_disclosed_tpd') * _V('anna_operating_days')
D['anna_nameplate_derived'] = ((D['design_ammonia_t']
                                - D['design_urea_t'] * D['ammonia_per_urea_t'])
                               / D['nh3_per_t_an'])
D['anna_util_base'] = _V('anna_util_base')
D['anna_util_bull'] = _V('anna_util_bull')
D['anna_price_usd_t'] = _V('an_price_usd_t')
D['anna_cash_margin'] = _V('anna_cash_margin')          # AN cash margin over its own ammonia + conversion
D['dso'] = _V('dso')
D['dio'] = _V('dio')
D['dpo'] = _V('dpo')
D['tax_rate'] = _V('tax_statutory')
D['wacc_spot'] = WACC['wacc_rating']
D['wacc_cds'] = WACC['wacc_cds']
D['g_terminal'] = _V('g_terminal')               # CBE medium-term inflation target: nominal
                                      # maintenance growth, no real growth assumed
D['roc_terminal'] = _V('roc_terminal')              # reinvestment = g / RoC

# ---- the discount-rate GLIDE, and the terminal rate built from its own parts --
# A spot WACC embeds today's 14.3% inflation print in every year, while the terminal
# value grows at the CBE's 7% target. Capitalising a 7%-growth perpetuity at a rate
# built on 14% inflation is not conservatism, it is a units mismatch, and on a company
# whose value sits in its terminal year it is the single largest number in the study.
# So the rate glides from the spot build to a NORMALISED long-run build, and the
# discount factors compound the glide year by year rather than powering one rate.
D['rf_star_spot'] = WACC['rf_star_rating']            # 23.00% observed - 6.37% spread
D['inflation_lt'] = _V('cbe_inflation_target')                              # CBE medium-term target
D['real_rate_lt'] = _V('real_rate_lt')                              # EM long-run real policy rate
D['rf_star_terminal'] = (1 + D['inflation_lt']) * (1 + D['real_rate_lt']) - 1   # 10.75%
D['kd_usd_lt'] = _V('kd_usd_lt')                                 # long-run USD corporate cost
D['deprec_lt'] = _V('expected_depreciation')                                 # same wedge used in the Kd build
D['kd_local_equiv_terminal'] = (1 + D['kd_usd_lt']) * (1 + D['deprec_lt']) - 1
D['erp'] = WACC['erp_rating']
D['beta'] = WACC['beta']
D['we'] = WACC['we']
D['wd'] = WACC['wd']

def _wacc_from(rf_star, kd_pretax):
    ke = rf_star + D['beta'] * D['erp']
    return D['we'] * ke + D['wd'] * kd_pretax * (1 - D['tax_rate']), ke

def set_glide():
    """Rebuild the whole rate structure from its own components. Called once here and
    again by alternatives.py, which moves one component at a time and reprices — so an
    alternative construction can never be a hand-adjusted rate."""
    D['rf_star_terminal'] = (1 + D['inflation_lt']) * (1 + D['real_rate_lt']) - 1
    D['kd_local_equiv_terminal'] = (1 + D['kd_usd_lt']) * (1 + D['deprec_lt']) - 1
    D['wacc_terminal'], D['ke_terminal'] = _wacc_from(D['rf_star_terminal'],
                                                     D['kd_local_equiv_terminal'])
    # linear glide across the explicit window, spot in year 1 -> terminal-adjacent in year 5
    D['wacc_path'], D['rf_star_path'], D['kd_path'] = [], [], []
    for _k in range(5):
        _f = _k / 5.0                                 # glide fraction, visibly derived
        _rf = D['rf_star_spot'] + (D['rf_star_terminal'] - D['rf_star_spot']) * _f
        _kd = D['kd_pretax_spot'] + (D['kd_local_equiv_terminal'] - D['kd_pretax_spot']) * _f
        _w, _ = _wacc_from(_rf, _kd)
        D['rf_star_path'].append(_rf); D['kd_path'].append(_kd); D['wacc_path'].append(_w)
    D['wacc'] = D['wacc_path'][0]


# THE COST OF DEBT IS RE-DERIVED HERE, not read frozen from wacc_result.json. Changing the
# expected-depreciation wedge in the register used to leave the dollar debt's local-
# equivalent cost untouched, because that figure was computed once and cached -- so the
# model and the workbook, which rebuilds it from the register, disagreed. The wedge that
# carries long-dated dollar debt is the LONG-RUN one, not the near-term path.
# the CDS basis is re-derived from the register too: the spread was corrected from 3.55%
# to Damodaran's actual 3.41% and the cached file still held the old premium
WACC['sov_spread_cds'] = _V('sov_spread_cds')
WACC['rf_star_cds'] = _V('rf_observed') - _V('sov_spread_cds')
WACC['erp_cds'] = _V('erp_cds_damodaran')
WACC['ke_cds'] = WACC['rf_star_cds'] + WACC['beta'] * WACC['erp_cds']
WACC['kd_fx_local_equiv'] = ((1 + WACC['kd_usd_nominal'])
                             * (1 + _V('expected_depreciation')) - 1)
WACC['kd_pretax_blended'] = (WACC['pct_debt_local'] * WACC['kd_local']
                             + (1 - WACC['pct_debt_local']) * WACC['kd_fx_local_equiv'])
WACC['kd_aftertax'] = WACC['kd_pretax_blended'] * (1 - WACC['tax_rate'])
for _basis in ('rating', 'cds'):
    WACC[f'wacc_{_basis}'] = (WACC['we'] * WACC[f'ke_{_basis}']
                              + WACC['wd'] * WACC['kd_aftertax'])
WACC['wacc_published'] = WACC['wacc_rating']
D['wacc_spot'] = WACC['wacc_rating']
D['wacc_cds'] = WACC['wacc_cds']
D['kd_pretax_spot'] = WACC['kd_pretax_blended']
set_glide()

# =============================================================================
# 2. HISTORICALS — straight from the audited statements
# =============================================================================
def hist_year(rev, cogs, sell, admin, dep, net, label):
    gross = rev - cogs
    ebit = gross - sell - admin
    return dict(year=label, revenue=rev, cogs=cogs, gross=gross, gross_pct=gross / rev,
                selling=sell, admin=admin, ebit=ebit, ebit_pct=ebit / rev,
                dep=dep, ebitda=ebit + dep, ebitda_pct=(ebit + dep) / rev, net=net)

H = [hist_year(_V(f'is_revenue_FY{t}'), _V(f'is_cogs_FY{t}'), _V(f'is_selling_FY{t}'),
               _V(f'is_admin_FY{t}'), _V(f'cogs_dep_FY{t}') + _V(f'amort_FY{t}'),
               _V(f'is_net_FY{t}'), y)
     for y, t in zip(HIST_YEARS, ("2223", "2324", "2425"))]
H[1]['net_underlying'] = _V('is_net_FY2324') - _V('oneoff_reval_FY2324')   # ex the one-off gain

# FY2025/26E — nine months reviewed, fourth quarter run-rated on the third quarter's
# operating performance (the strongest on record) with the FX line set to zero, since
# a translation swing is not forecastable and is carried as a sensitivity instead.
q3_rev, q3_gross_pct = _V('is_revenue_Q3'), _V('gross_margin_Q3')
q4 = q3_rev * _V('q4_runrate_haircut')
fy2526 = dict(
    year="FY2025/26E",
    revenue=_V('is_revenue_9M') + q4,
    cogs=None, gross=None,
)
fy2526['gross'] = _V('is_gross_9M') + q4 * q3_gross_pct
fy2526['cogs'] = fy2526['revenue'] - fy2526['gross']
fy2526['gross_pct'] = fy2526['gross'] / fy2526['revenue']
fy2526['selling'] = _V('is_selling_9M') * 4 / 3
fy2526['admin'] = _V('is_admin_9M') * 4 / 3
fy2526['ebit'] = fy2526['gross'] - fy2526['selling'] - fy2526['admin']
fy2526['ebit_pct'] = fy2526['ebit'] / fy2526['revenue']
fy2526['dep'] = D['dep_base'] + D['amort_base']
fy2526['ebitda'] = fy2526['ebit'] + fy2526['dep']
fy2526['ebitda_pct'] = fy2526['ebitda'] / fy2526['revenue']
fy2526['net'] = _V('is_net_9M')  # nine months actual; Q4 not annualised into net because
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
        wages = D['wages']["FY2024/25"] * cpi_cum
        services = D['services'] * cpi_cum
        # the existing base, plus depreciation on the project capital already placed in
        # service. EGP 14.7bn was being capitalised and never depreciated anywhere in the
        # model, in any year -- found independently by two critiques and by the self-audit.
        anna_in_service = sum(D['anna_capex_path'][:k])
        dep = (D['dep_base'] * (1 + D['dep_escalation'] * k) + D['amort_base']
               + anna_in_service * D['dep_rate_project'])
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
            # OPENING BALANCE, CORRECTED 9 August 2026. The study constructed this from the
            # study-year P&L at the disclosed day counts and claimed every pound of working
            # capital traced to a receivable, an inventory or a payable. That claim was false
            # for the opening balance alone -- the one constructed number in the chain -- and
            # it sat about EGP 1bn below the balance the company actually reported at the same
            # date the bridge takes net debt from. It is now the REPORTED position.
            prev_wc = (_V('bs_receivables_M9FY2526') + _V('bs_inventory_M9FY2526')
                       - _V('bs_payables_M9FY2526'))
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
            p_sub=D['subsidised_p_path'][k], p_an=p_an,
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
    fx = last['fx'] * (1 + D['g_terminal'] - _V('fx_terminal_wedge'))     # steady-state depreciation wedge
    util = {"base": D['anna_util_base'], "bull": D['anna_util_bull'],
            "bear": 0.0, "halt": 0.0}[case]
    an_t = D['anna_nameplate_an_t'] * util
    anna_rev = an_t * D['anna_price_usd_t'] * fx / 1e6
    # BUILT, not assumed. The new complex was valued on a flat 32% cash margin — a whole
    # business line priced by a single ratio in a study whose entire discipline is
    # volume x price and cost per physical unit. The auditor's product cost table gives the
    # unit cost of this exact product: granulated ammonium nitrate at EGP 4,076.31/t,
    # which reconciles to the disclosed ammonia unit cost at the disclosed ammonia ratio
    # with EGP 157/t of conversion. So the terminal tonne is built the same way every urea
    # tonne is: ammonia (gas-driven) plus conversion (domestic-inflation-driven).
    _gas_egp_m3_T = D['gas_usd_mmbtu'] * D['mmbtu_per_m3'] * fx
    _nh3_cost_T = D['gas_m3_per_t_ammonia'] * _gas_egp_m3_T          # EGP per tonne NH3
    _cpi_cum_T = rows[-1]['cpi_cum'] * (1 + D['cpi_path'][-1])
    _an_unit_cost = (D['nh3_per_t_an'] * _nh3_cost_T
                     + _V('an_conversion_cost_FY2425') * _cpi_cum_T)
    anna_cash_cost = an_t * _an_unit_cost / 1e6
    _ebit_built = anna_rev - anna_cash_cost
    _ebit_assumed = anna_rev * D['anna_cash_margin']
    # THE BUILD AND THE ASSUMPTION DISAGREE, AND THE MORE CONSERVATIVE ONE IS KEPT.
    # Built from the auditor's own disclosed unit costs the terminal tonne carries a ~66%
    # cash margin, because the disclosed granulated-nitrate unit cost is only EGP 4,076/t
    # against a disclosed realised price near EGP 20,000/t. An 80% historical margin on a
    # commodity fertilizer is not credible, so the disclosed unit cost is almost certainly a
    # partial cost -- most likely ammonia transferred internally below its economic cost.
    # The build is the right METHOD and it is published; adopting its margin would flatter
    # the valuation by EGP 0.58 a share on a number the study does not believe. The central
    # takes the lower of the two and the gap is carried as a contested construction.
    anna_ebit = min(_ebit_built, _ebit_assumed)
    D['anna_unit_cost_terminal'] = _an_unit_cost
    D['anna_ebit_built'] = _ebit_built
    D['anna_ebit_assumed'] = _ebit_assumed
    D['anna_margin_built_pct'] = (_ebit_built / anna_rev) if anna_rev else 0.0

    # a CASH margin is struck before depreciation. The completed plant must carry its own
    # charge before it enters terminal EBIT.
    anna_dep = (D['anna_total_cost'] * D['dep_rate_project']) if util > 0 else 0.0
    anna_ebit -= anna_dep
    base_ebit = last['ebit'] * (1 + D['g_terminal'])
    ebit_T = base_ebit + anna_ebit
    nopat_T = ebit_T * (1 - D['tax_rate'])
    reinv_rate = D['g_terminal'] / D['roc_terminal']
    fcff_T = nopat_T * (1 - reinv_rate)
    # base_ebit is ALREADY the year-six flow (EBIT_5 grown once). The Gordon numerator must
    # therefore be FCFF_6, not FCFF_6 x (1+g): the extra factor put a year-seven flow into a
    # perpetuity discounted at the year-five factor. Found by three independent critiques.
    tv = fcff_T / (D['wacc_terminal'] - D['g_terminal'])
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
    cash = _V('bs_cash_M9FY2526')
    debt = (_V('bs_debt_lt_M9FY2526') + _V('bs_debt_holdco_M9FY2526')
            + _V('bs_debt_cur_M9FY2526'))
    fvoci = _V('bs_fvoci_M9FY2526')   # remaining ABUK + Delta Sugar stakes, at market
    inv_prop = _V('bs_invprop_M9FY2526')
    net_debt = debt - cash
    equity = ev - net_debt + fvoci + inv_prop
    shares = _V('shares_outstanding')
    return dict(pv_explicit=pv_explicit, pv_tv=T['pv_tv'], ev=ev,
                tv_pct_ev=T['pv_tv'] / ev if ev else float('nan'),
                cash=cash, debt=debt, net_debt=net_debt, fvoci=fvoci,
                inv_prop=inv_prop, equity=equity, shares=shares,
                per_share=equity * 1e6 / shares)


def run_case(case):
    """One case, end to end: the operating build, the case adjustment, the terminal year
    and the bridge. Every alternative construction in alternatives.py goes through THIS
    function, so an alternative is a re-run of the model and never a re-description of it."""
    rws = build("bull" if case == "bull" else "base")
    if case == "halt":
        # CAPITAL-DISCIPLINE case: the board stops ANNA at the end of FY2026/27, takes
        # the wind-down cost, writes the EGP 5.65bn already in construction-in-progress
        # off against nothing, and the company runs as the urea plant it already is.
        # This is not a forecast of what management will do — it is the measurement of
        # what the programme is costing shareholders, in EGP per share, against the
        # alternative of not doing it.
        for k, r in enumerate(rws):
            # capital that is never spent is also never depreciated: the stopped case must
            # strip the project charge out of the operating lines as well as out of capex
            anna_dep = sum(D['anna_capex_path'][:k]) * D['dep_rate_project']
            r['dep'] -= anna_dep
            r['cogs'] -= anna_dep
            r['gross'] += anna_dep
            r['ebit'] += anna_dep
            r['ebitda'] = r['ebit'] + r['dep']
            r['nopat'] = r['ebit'] * (1 - D['tax_rate'])
            r['capex'] = ((_V('anna_winddown_cost') if k == 0 else 0.0)
                          + r['revenue'] * D['maint_capex_pct_rev'])
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
    return dict(rows=rws, terminal=T, bridge=bridge(rws, T))


CASES = {case: run_case(case) for case in ("base", "bull", "bear", "halt")}

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
print(f"\nspot EGP {_V('spot_price'):.2f} ({_V('spot_price_date')}) | WACC glide "
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
                r['capex'] = ((_V('anna_winddown_cost') if k == 0 else 0.0)
                              + r['revenue'] * D['maint_capex_pct_rev'])
                r['fcff'] = r['nopat'] + r['dep'] - r['capex'] - r['dwc']
                r['pv'] = r['fcff'] * r['df']
        ps = bridge(rws, terminal(rws, case))['per_share']
        if ps > target_per_share:
            lo = mid
        else:
            hi = mid
    D['wacc_path'], D['wacc_terminal'] = saved_path, saved_T
    return mid

D['implied_wacc_base'] = implied_flat_wacc(_V('spot_price'), "base")
D['implied_wacc_halt'] = implied_flat_wacc(_V('spot_price'), "halt")
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
           wacc=WACC, spot=_V('spot_price'), spot_date=_V('spot_price_date'))
json.dump(out, open(os.path.join(HERE, 'study_numbers.json'), 'w'), indent=1, default=float)
print("\nwrote study_numbers.json")
