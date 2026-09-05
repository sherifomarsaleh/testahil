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
from inputs import V as _V
from inputs import _HOUSE          # the house macro path [R-MACRO-01], not a second copy          # the study's input register — the single source of
                                    # every number in this model (numeric traceability)
from inputs import REG as _REG
import terminal_value as TV        # [R-TERM-01] — the ONLY sanctioned terminal


def _SRC(k):
    """An input's own source field, so a provenance string is never retyped."""
    return _REG[k]['source']

FY25 = json.load(open(os.path.join(HERE, 'extract_fy2425.json')))
HIST = json.load(open(os.path.join(HERE, 'extract_history.json')))
NINE = json.load(open(os.path.join(HERE, 'extract_9m_fy2526.json')))

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
# THE AUDITOR'S OWN DISCLOSED STANDARD RATE IS 1,200 m3/t, AND IT WAS REGISTERED AS A
# PRIMARY INPUT AND CONSUMED BY NOTHING until 5 September 2026, when an audit run from
# outside this study found it sitting unused while the model ran a constructed allocation.
# It is now a live CROSS-CHECK on that allocation, which is what a disclosed figure the
# model does not adopt should be.
#
# THE MODELLED RATE IS NOT SUBSTITUTED BY IT, AND THE REASON IS ARITHMETIC RATHER THAN
# PREFERENCE. 1,200 is the STANDARD — what the plant consumes when it runs to specification
# — and this plant does not: the same auditor's report discloses 38,480,270 m3 of gas LOST
# in FY2024/25, which over that year's own 318,242 tonnes of ammonia is 120.9 m3/t. Standard
# plus disclosed loss is 1,320.9 m3/t, and the model's allocation-implied 1,292 sits between
# the two, 7.7% above the standard and 2.2% below standard-plus-loss. A model of what this
# plant actually consumes has to carry the losses; adopting the standard would model a plant
# that does not exist.
#
# WHAT THAT LEAVES OPEN, STATED RATHER THAN CLOSED: whether the abnormal-gas line charged
# separately below the gross margin is charging some of the SAME lost gas a second time
# depends on whether those losses sit inside the disclosed materials line, which the
# statements do not split. The direction is known — if they do, the model overstates cost —
# and the size is bounded by the abnormal path itself. The substitution is priced in the
# contested-constructions table rather than argued about here.
_gas_standard = _V('gas_standard_m3_t')
_gas_loss_rate = _V('gas_loss_FY2425_m3') / _V('prod_ammonia_FY2425')
assert _V('gas_usage_low_m3_t') <= D['gas_m3_per_t_ammonia'] <= _V('gas_usage_high_m3_t'), \
    'the allocation-implied gas rate must sit inside the auditor\'s own disclosed range'
assert _gas_standard <= D['gas_m3_per_t_ammonia'] <= _gas_standard + _gas_loss_rate * 1.05, \
    ('the allocation-implied gas rate must sit between the disclosed STANDARD and that '
     'standard plus the disclosed LOSS: below the standard it models a plant running better '
     'than specification, above standard-plus-loss it charges gas nobody reports')
D['gas_standard_m3_t'] = _gas_standard
D['gas_loss_rate_m3_t'] = _gas_loss_rate
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
# the fixed-asset base the terminal maintenance charge is struck on
D['fa_avg_age_years'] = _V('fa_avg_age_years')
D['fa_life_implied_years'] = _V('fa_life_implied_years')
D['terminal_force_half_life'] = False  # the age is MEASURED; see the terminal
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
D['inflation_lt'] = _V('inflation_terminal')   # the SAME inflation terminal growth carries (L-055)
D['real_rate_lt'] = _V('real_rate_lt')                              # EM long-run real policy rate
# THE HOUSE PATH OWNS THIS QUANTITY AND THIS STUDY WAS COMPUTING IT ITSELF.
# macro_path.terminal_rf() is terminal inflation PLUS the real-rate convention —
# additive, derived, never quoted. This line compounded them instead, which is a
# second convention about inflation inside a model whose terminal GROWTH already
# comes from the house path additively ([L-055]: one model, one inflation). Worth
# 38.5 basis points on the terminal risk-free rate and, through the whole terminal
# block, several per cent on the answer. Corrected 5 September 2026.
D['rf_star_terminal'] = _HOUSE.terminal_rf
D['kd_usd_lt'] = _V('kd_usd_lt')                                 # long-run USD corporate cost
D['deprec_lt'] = _V('expected_depreciation')                                 # same wedge used in the Kd build
D['kd_local_equiv_terminal'] = (1 + D['kd_usd_lt']) * (1 + D['deprec_lt']) - 1

def _wacc_from(rf_star, kd_pretax):
    ke = rf_star + D['beta'] * D['erp']
    return D['we'] * ke + D['wd'] * kd_pretax * (1 - D['tax_rate']), ke

def set_glide():
    """Rebuild the whole rate structure from its own components. Called once here and
    again by alternatives.py, which moves one component at a time and reprices — so an
    alternative construction can never be a hand-adjusted rate. The risk-free rate glides
    linearly from spot to terminal; the cost of debt is built YEAR BY YEAR from the dollar
    coupon and that year's derived currency wedge (the same wedge the revenue build uses)."""
    D['rf_star_terminal'] = _HOUSE.terminal_rf
    _kd_fx_T = (1 + D['kd_usd_lt']) * (1 + D['deprec_lt']) - 1
    D['kd_fx_terminal'] = _kd_fx_T                                  # the dollar leg alone
    D['kd_local_equiv_terminal'] = kd_blend(D['kd_local'], _kd_fx_T)   # blended with the local leg
    D['wacc_terminal'], D['ke_terminal'] = _wacc_from(D['rf_star_terminal'],
                                                     D['kd_local_equiv_terminal'])
    D['wacc_path'], D['rf_star_path'], D['kd_path'] = [], [], []
    for _k in range(5):
        _f = _k / 5.0                                 # glide fraction, visibly derived
        _rf = D['rf_star_spot'] + (D['rf_star_terminal'] - D['rf_star_spot']) * _f
        _kd = kd_blend(D['kd_local'], kd_fx_year(_k))
        _w, _ = _wacc_from(_rf, _kd)
        D['rf_star_path'].append(_rf); D['kd_path'].append(_kd); D['wacc_path'].append(_w)
    D['wacc'] = D['wacc_path'][0]


# =============================================================================
# THE COST OF CAPITAL IS BUILT HERE, ONCE, THROUGH wacc_builder — the register is the only
# source, and no second file holds a second cost of debt. [Edition 1 September 2026, on
# audit: the 8 August edition's wacc_result.json carried a 4.5% wedge and a 3.55% CDS spread
# while this module re-derived both, so the Word table and the workbook disagreed.]
#
# THE FX LEG IS BUILT YEAR BY YEAR ON THE STUDY'S OWN DERIVED CURRENCY PATH (L-048, one
# path): Kd_fx(t) = (1 + dollar coupon) x (1 + wedge_t) - 1, where wedge_t is the relative
# purchasing-power depreciation the inflation path implies in that year (7.4% in year one
# gliding to the 2.5% terminal wedge). A flat wedge on the debt beside a gliding wedge on
# revenue would be the same event counted two ways.
# =============================================================================
import wacc_builder as _wb
_BETA_REC = json.load(open(os.path.join(HERE, 'beta_result.json')))
_SHARES = _V('shares_outstanding')
_MCAP = _V('spot_price') * _SHARES
_DEBT_M = (_V('bs_debt_lt_M9FY2526') + _V('bs_debt_holdco_M9FY2526') + _V('bs_debt_cur_M9FY2526'))
D['kd_local'] = _V('kd_local')
D['kd_usd_nominal'] = _V('kd_usd_nominal')
D['pct_debt_local'] = _V('bs_debt_holdco_M9FY2526') / _DEBT_M
D['kd_floor'] = None            # set only by the sovereign-floored ALTERNATIVE in alternatives.py
D['company_spread_over_policy'] = max(0.0, _V('kd_local') - _V('policy_rate'))


def kd_fx_year(k):
    """Dollar leg at local-equivalent cost in explicit year k, on the derived wedge path."""
    return (1 + D['kd_usd_nominal']) * (1 + D['fx_wedge_path'][k]) - 1


def kd_blend(kd_local, kd_fx):
    if D['kd_floor'] is not None:
        kd_local, kd_fx = max(kd_local, D['kd_floor']), max(kd_fx, D['kd_floor'])
    return D['pct_debt_local'] * kd_local + (1 - D['pct_debt_local']) * kd_fx


def _wacc_inputs(k):
    return _wb.WaccInputs(
        rf_observed=_V('rf_observed'), erp_rating=_V('erp_rating'),
        sov_default_spread_rating=_V('sov_spread_rating'), erp_cds=_V('erp_cds_damodaran'),
        sov_default_spread_cds=_V('sov_spread_cds'), beta=_BETA_REC['beta'],
        beta_source="beta_result.json — own-stock weekly regression on the published EGX30",
        kd_pretax_local=D['kd_local'], kd_pretax_fx_local_equiv=kd_fx_year(k),
        pct_debt_local_ccy=D['pct_debt_local'], tax_rate=D['tax_rate'],
        market_cap=_MCAP, total_debt=_DEBT_M * 1e6, kd_is_marginal=True,
        rf_source="register: rf_observed", erp_source="register: erp_rating",
        kd_source="register: kd_local, kd_usd_nominal, fx_wedge_path", weights_source="register: spot_price x shares_outstanding; balance-sheet debt at 31 March 2026")


_res = [_wb.build_wacc(_wacc_inputs(k)) for k in range(5)]
_r0 = _res[0]
_below = [k for k in range(5) if kd_fx_year(k) < _r0.rf_star_rating]
_fx_leg_sentence = None
if _below:
    _yrs = ", ".join("%s (%.2f%%)" % (YEARS[k], kd_fx_year(k) * 100) for k in _below)
    _wdg = ", ".join("%.1f%%" % (D['fx_wedge_path'][k] * 100) for k in _below)
    _fx_leg_sentence = (
        "The dollar leg's local-equivalent cost sits below the %.2f%% normalised risk-free rate in %s, "
        "because the currency wedge in those years (%s) is smaller than the gap between the %.1f%% "
        "coupon and that rate. It is left as built, because the wedge is the study's one currency path "
        "and the debt may not carry a second." % (_r0.rf_star_rating * 100, _yrs, _wdg, D['kd_usd_nominal'] * 100))
WACC = dict(
    spot=_V('spot_price'), shares=_SHARES, market_cap=_MCAP, total_debt=_DEBT_M * 1e6,
    rf_observed=_V('rf_observed'), sov_spread_rating=_V('sov_spread_rating'), sov_spread_cds=_V('sov_spread_cds'),
    rf_star_rating=_r0.rf_star_rating, rf_star_cds=_r0.rf_star_cds,
    erp_rating=_V('erp_rating'), erp_cds=_V('erp_cds_damodaran'), beta=_BETA_REC['beta'],
    ke_rating=_r0.ke_rating, ke_cds=_r0.ke_cds,
    kd_local=D['kd_local'], kd_usd_nominal=D['kd_usd_nominal'], pct_debt_local=D['pct_debt_local'],
    fx_wedge_path=list(D['fx_wedge_path']), kd_fx_path=[kd_fx_year(k) for k in range(5)],
    kd_fx_local_equiv=kd_fx_year(0), kd_pretax_blended=_r0.kd_pretax_blended, kd_aftertax=_r0.kd_aftertax,
    kd_pretax_path=[r.kd_pretax_blended for r in _res],
    tax_rate=D['tax_rate'], we=_r0.we, wd=_r0.wd,
    wacc_rating=_r0.wacc_rating, wacc_cds=_r0.wacc_cds, wacc_published=_r0.wacc_cds,
    # A DIFFERENCE OF TWO RATES IS BASIS POINTS, and it is COMPUTED here rather than
    # scaled inside a builder: depth-bar standard 3 forbids a financial numeral in a
    # builder, and a bare 1e4 beside two rates is exactly that.
    wacc_rating_less_cds_bp=(_r0.wacc_rating - _r0.wacc_cds) * 10000.0,
    warnings_by_year={YEARS[k]: r.warnings for k, r in enumerate(_res)},
    # the builder gates its local-below-sovereign check on an all-local book; on a 0.3%-local
    # book it stays silent, so the fact is stated here in the same words and printed in §1.8
    # the builder's own warning strings are kept as a record and NEVER printed: a reader is
    # handed the fact each warning detects, in the study's words, with the priced alternative
    builder_warnings=sorted({w for r in _res for w in r.warnings}),
    disclosures=[
        (f"The company's own local-currency facility carries {D['kd_local']*100:.2f}% against a "
         f"{_V('rf_observed')*100:.2f}% sovereign ten-year yield: a same-currency corporate borrowing "
         f"below its sovereign. It is the company's disclosed rate on a state-bank facility and is "
         f"used as disclosed.")
        if D['kd_local'] < _V('rf_observed') else None,
        _fx_leg_sentence,
    ],
    company_spread_over_policy=D['company_spread_over_policy'],
    sovereign_floor=_V('rf_observed') + D['company_spread_over_policy'],
)
WACC['disclosures'] = list(dict.fromkeys(d for d in WACC['disclosures'] if d))   # each distinct warning once
WACC['years_fx_leg_below_rf_star'] = [YEARS[k] for k in range(5) if kd_fx_year(k) < _r0.rf_star_rating]
# THE CDS BASIS IS THE HOUSE DEFAULT AND THIS STUDY WAS THE ONLY ONE NOT USING IT
# [corrected 03-Sep-2026]. [R-COC-01]: "Both premium bases are published and one is
# named CENTRAL (the swap basis by default -- the market's own live pricing of the
# sovereign's credit, against an agency judgement updated in steps)." AMOC names the
# CDS basis central and records the choice as its largest contested number; ARCC
# records erp_basis "cds". EGCH published the RATING basis: an equity risk premium
# of 13.94% against 9.41% for the SAME sovereign on the SAME day, and a sovereign
# spread of 6.37% against 3.41%. Three studies in one market on two conventions is
# the incoherence [R-MACRO-01] exists to close, and the odd one out took the higher
# premium. Both remain published; the central is now the one the rule names.
D['rf_star_spot'] = WACC['rf_star_cds']
D['erp'] = WACC['erp_cds']
D['beta'] = WACC['beta']
D['we'] = WACC['we']
D['wd'] = WACC['wd']
D['wacc_spot'] = WACC['wacc_cds']
D['wacc_rating_alt'] = WACC['wacc_rating']
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
    # THE PROJECT'S DEPRECIATION IS CHARGED ONCE, AND IT WAS CHARGED TWICE. The explicit
    # window depreciates the complex AS IT IS SPENT, so the last explicit year already
    # carries the charge on the part in service; the terminal line above then charges the
    # WHOLE plant. Grossing the last explicit year's profit without first removing the
    # in-service part therefore charged that part twice — on the base case, EGP 482mn of
    # depreciation on a plant that appears once in the accounts. THE MODEL ALREADY KNEW
    # HOW TO DO THIS: the programme-stopped branch strips exactly this charge before it
    # grosses, which is why that branch was never wrong. Under the retired construction
    # the error only depressed profit; under the sanctioned one book depreciation is also
    # the BASE OF THE REPLACEMENT CHARGE, so it was depressing the value twice over.
    _anna_dep_in_last = ((sum(D['anna_capex_path'][:len(rows) - 1]) * D['dep_rate_project'])
                         if util > 0 else 0.0)
    base_ebit = (last['ebit'] + _anna_dep_in_last) * (1 + D['g_terminal'])
    ebit_T = base_ebit + anna_ebit
    nopat_T = ebit_T * (1 - D['tax_rate'])
    # Book depreciation in the terminal year, on exactly the construction ebit_T charges:
    # the existing plant's charge grown with the rest of that profit, plus the complex's
    # own full-year charge once. It is an ADD-BACK and the base of the maintenance charge,
    # so the two must be the same number or the waterfall is not a waterfall.
    dna_T = (last['dep'] - _anna_dep_in_last) * (1 + D['g_terminal']) + anna_dep
    wc_T = last['wc'] * (1 + D['g_terminal'])

    # ---- THE RETIRED CONSTRUCTION, kept in two lines so the change stays legible -------
    # rr = g / RoC substitutes to a charge of g x IC every year for ever, so the implied
    # replacement cycle is 1/g — 14.3 years at a 7% terminal, a fact about the pound and
    # not about a urea plant. The disclosed rate for this plant's machinery is 3.95%, a
    # 25.3-year life, and the base is 4.45 years old.
    reinv_rate = D['g_terminal'] / D['roc_terminal']
    fcff_retired = nopat_T * (1 - reinv_rate)
    # base_ebit is ALREADY the year-six flow (EBIT_5 grown once). The Gordon numerator must
    # therefore be FCFF_6, not FCFF_6 x (1+g): the extra factor put a year-seven flow into a
    # perpetuity discounted at the year-five factor. Found by three independent critiques.
    tv_retired = fcff_retired / (D['wacc_terminal'] - D['g_terminal'])

    # ---- THE SANCTIONED CONSTRUCTION [R-TERM-01] --------------------------------------
    # terminal_value.build() applies the Gordon step ITSELF — tv = fcff x (1+g)/(w-g) —
    # and values the terminal at the END of the year whose figures it is handed, which is
    # where the year-five factor above discounts it. THE FIGURES ABOVE ARE THE YEAR-SIX
    # ONES, so each is handed over one year earlier and the module grows it back. Handing
    # over the year-six figures directly would grow them a second time and overstate the
    # terminal by exactly (1+g) — 7.0% here, and it is what six of this house's eight
    # studies did until 4 September 2026 [L-329]. The assertion below is the bridge
    # between the two presentations: whatever the module returns must equal this study's
    # own convention applied to the year-six free cash flow.
    # REAL growth is DERIVED from the terminal growth this study carries and the terminal
    # inflation it discounts at, so the two cannot disagree about inflation [L-055]. At the
    # central they are the same number and real growth is exactly zero; the alternative
    # terminal growth is a real DECLINE and says so in real terms rather than in nominal.
    _g_real = (1.0 + D['g_terminal']) / (1.0 + D['inflation_lt']) - 1.0
    # The capital a unit of REAL growth consumes, at replacement cost: one year's
    # replacement-cost consumption multiplied by the life over which the base turns over,
    # which is the whole depreciable base at what it would cost to build now. INERT at the
    # central, where real growth is zero; it binds in the alternative and in the grid,
    # which is exactly where an assumption that growth is free would hide.
    _dna5 = dna_T / (1 + D['g_terminal'])
    _inc_cap = (_dna5 * (1 + D['inflation_lt']) ** D['fa_avg_age_years']
                * D['fa_life_implied_years'])
    # AND IT IS ONE-SIDED, WHICH IS AN ECONOMIC STATEMENT AND NOT A CONVENIENCE. Real
    # growth costs capital here; real DECLINE releases none of it. This is a single site:
    # a urea train cannot be part-sold, and shrinking output leaves the same plant to
    # maintain. Letting the identity run symmetrically would have credited the alternative
    # terminal — a real decline of 3.7% a year — with a permanent capital release of about
    # EGP 1.9bn a year, which drives the implied payout to 128% of profit and the module
    # REFUSES it outright: a going concern distributing more than it earns for ever is a
    # liquidation. The refusal is right and the fix is the assumption, not the module.
    if _g_real < 0:
        _inc_cap = 0.0
    # THE CONTESTED CONSTRUCTION, priced rather than described. The escalator rests on the
    # AGE of the base, and this company's accounts let that be MEASURED — accumulated
    # depreciation over the year's own charge. Where they do not, the shared construction
    # assumes half the life, which on a base this young is more than twice the truth. The
    # alternative below is what this same terminal would say if the age had to be assumed,
    # and it is the largest single contested number in the study.
    _age = None if D.get('terminal_force_half_life') else D['fa_avg_age_years']
    _T = TV.build(TV.TerminalInputs(
        nopat=nopat_T / (1 + D['g_terminal']),
        wacc=D['wacc_terminal'], inflation=D['inflation_lt'], real_growth=_g_real,
        dna_book=_dna5,
        average_age_years=_age,
        average_age_source=(_SRC('fa_accum_dep_FY2425') if _age is not None else ''),
        useful_life_years=D['fa_life_implied_years'],
        useful_life_source=_SRC('fa_cost_gross_FY2425'),
        maintenance_basis='book_dna_escalated',
        working_capital=wc_T / (1 + D['g_terminal']),
        incremental_capital_per_unit_growth=_inc_cap))
    fcff_T = _T.fcff * (1 + D['g_terminal'])        # the year-six flow the page prints
    tv = _T.tv
    assert abs(tv - fcff_T / (D['wacc_terminal'] - D['g_terminal'])) < 1e-6 * abs(tv), (
        'the module and this study state the same perpetuity two ways and they must agree')
    pv_tv = tv * rows[-1]['df']
    return dict(fx=fx, anna_util=util, an_t=an_t, anna_rev=anna_rev, anna_ebit=anna_ebit,
                base_ebit=base_ebit, ebit_T=ebit_T, nopat_T=nopat_T,
                anna_dep=anna_dep, anna_dep_in_last=_anna_dep_in_last,
                dna_T=dna_T, wc_T=wc_T,
                maintenance_T=_T.maintenance * (1 + D['g_terminal']),
                wc_charge_T=_T.wc_charge * (1 + D['g_terminal']),
                floor_T=_T.floor, payout_T=_T.fcff / (nopat_T / (1 + D['g_terminal'])),
                growth_capex_T=_T.growth_capex * (1 + D['g_terminal']),
                inc_cap=_inc_cap, g_real=_g_real,
                reinv_rate=reinv_rate, fcff_retired=fcff_retired, tv_retired=tv_retired,
                terminal_record=_T.record,
                fcff_T=fcff_T, tv=tv, pv_tv=pv_tv,
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

# ==================== FUNDAMENTAL WALK-FORWARD, CARRIED IN ====================
# [R-FCAL-01] is a standing step of every study and every update, and its result belongs in
# the delivered document rather than only in the internal record. The training record itself
# (panel, error cells, pre-registration) stays internal; what a reader sees is the scope, the
# honest headline, and the bands the record licenses on the far forecast years.
_WF = os.path.join(HERE, '..', 'egch_walkforward')
_FR = json.load(open(os.path.join(_WF, 'forward_ranges.json')))
_WS = json.load(open(os.path.join(_WF, 'scores.json')))
_WD = json.load(open(os.path.join(_WF, 'diagnostics.json')))
WALKFORWARD = dict(
    ran=True, scope='FULL', origins=len(_WS['origins']), horizons='1-5', cells=_WS['cells'],
    window='FY2008-FY2025, KIMA\'s own audited statements (18 fiscal years, FY2014 partial)',
    headline=dict(
        net_bias=_WS['drivers']['net']['overall']['bias'],
        net_mae=_WS['drivers']['net']['overall']['mae'],
        net_n=_WS['drivers']['net']['overall']['n'],
        net_share_over=_WS['drivers']['net']['overall']['share_over'],
        net_skill_vs_freeze=_WS['drivers']['net']['skill_vs_freeze']['skill'],
        revenue_bias=_WS['drivers']['revenue']['overall']['bias'],
        revenue_skill_vs_freeze=_WS['drivers']['revenue']['skill_vs_freeze']['skill'],
        cost_skill_vs_freeze=_WS['drivers']['cost_of_sales']['skill_vs_freeze']['skill'],
        volume_bias=_WS['drivers']['urea_t']['overall']['bias'],
        volume_n=_WS['drivers']['urea_t']['overall']['n'],
        fx_contribution_pct_revenue=_WD['net_decomposition_mean']['fx'],
        tax_contribution_pct_revenue=_WD['net_decomposition_mean']['tax_current']),
    bands=_FR['published_band'],
    corrections_adopted=0,
    corrections_note=('None. Every correction that passed its own sign test on the expanding record '
                      'made the next origin worse when applied, and none matches how the driver is '
                      'built across the book. All are watch flags.'),
    what_it_changed=('Three things. The terminal inflation now equals the inflation terminal growth '
                     'is set at (the previous edition discounted a 5%-growth perpetuity at a rate '
                     'built on 7% inflation). The currency path is derived from the same inflation '
                     'identity that carries the dollar debt. And years three to five of the forecast '
                     'are published as ranges from the record\'s own error distribution, because on '
                     'this company the method did not beat "no change" on the profit line.'))

# ============================ THE GATES =================================
# [R-ENF-02] A study must call these in its OWN code; scripts/check_study_provenance.py runs the
# same tests from outside so a study cannot pass by not checking itself.
sys.path.insert(0, os.path.join(HERE, '..'))
import research_protocol as _rp
BETA_REC = json.load(open(os.path.join(HERE, 'beta_result.json')))
_rp.assert_beta_provenance(BETA_REC)
assert abs(BETA_REC['beta'] - WACC['beta']) < 5e-4, "the WACC beta and the regression record disagree"

# --- ground-up: a RECORD per revenue line, covering 100% of revenue [R-SIGCM-02] ----
_R0 = CASES['base']['rows'][0]
_TOT = _R0['revenue']
_TSRC = ("Auditor's product-cost table in the audited FY2024/25 statements (urea 513,385 t; "
         "ammonia 318,242 t; granulated and low-density nitrate 26,058 t)")
DRIVER_LINES = [
    _rp.DriverLine(name='export urea', level='unit', share_of_revenue=_R0['rev_exp'] / _TOT, unit='tonne',
                   unit_source=_TSRC + "; export tonnes = output less the two domestic legs",
                   price_basis="world urea f.o.b. Egypt in US$/t through the derived currency path, net of the 10% ad-valorem duty",
                   cost_basis="gas at the administered dollar price x m3 per tonne of ammonia; other materials, wages and services per tonne"),
    _rp.DriverLine(name='subsidised urea', level='derived', share_of_revenue=_R0['rev_sub'] / _TOT, unit='tonne',
                   unit_source=_TSRC, price_basis="administered cooperative supply price",
                   cost_basis="same physical cost stack as export urea",
                   gap_note="Tonnes are the auditor's 147kt over fourteen months annualised, not a year the company disclosed as such."),
    _rp.DriverLine(name='free-market urea', level='derived', share_of_revenue=_R0['rev_free'] / _TOT, unit='tonne',
                   unit_source=_TSRC, price_basis="90% of export parity",
                   cost_basis="same physical cost stack as export urea",
                   gap_note="Tonnes are the residual of the note-20 local revenue after the subsidised leg at an implied price; the filings do not split the three domestic channels."),
    _rp.DriverLine(name='nitrates', level='derived', share_of_revenue=_R0['rev_an'] / _TOT, unit='tonne',
                   unit_source=_TSRC, price_basis="FY2024/25 implied EGP/t carried on the currency path",
                   cost_basis="ammonia embodied at the disclosed ammonia unit cost plus disclosed conversion cost",
                   gap_note="The realised nitrate price is implied from the revenue note, not disclosed per tonne."),
    _rp.DriverLine(name='other (merchant nitric acid, plant rent, services)', level='segment',
                   share_of_revenue=_R0['rev_other'] / _TOT,
                   gap_note="A small residual line the filings disclose in total only; grown on domestic inflation."),
]
GROUND_UP = _rp.assert_ground_up(DRIVER_LINES, ticker='EGCH')
D['gates'] = dict(standard_version=_rp.STANDARD_VERSION, beta=BETA_REC, ground_up=GROUND_UP)

out = dict(drivers=D, hist=H, fy2526=fy2526, years=YEARS, hist_years=HIST_YEARS,
           walkforward=WALKFORWARD, gates=D['gates'], standard_version=_rp.STANDARD_VERSION,
           cases={k: dict(rows=v['rows'], terminal=v['terminal'], bridge=v['bridge'])
                  for k, v in CASES.items()},
           wacc=WACC, spot=_V('spot_price'), spot_date=_V('spot_price_date'))
# compute.py is IMPORTED by alternatives.py, sensitivity.py and the ladder, each of which re-runs
# this module and would otherwise overwrite the answer lenses.py wrote back (central, fair, spot)
# with a file that no longer carries it. The answer keys are carried over from the file on disk;
# lenses.py, which runs immediately after the first compute pass, always refreshes them.
#
# THE CARRY-OVER WAS AN ENUMERATED LIST AND IT WENT STALE THE MOMENT A KEY WAS ADDED
# [generalised 03-Sep-2026]. It named ('central', 'fair'), which was complete when it
# was written. lenses.py has since added central_two_sided, lens_record, macro_record
# and bridge_record -- the records [R-LENS-03], [R-MACRO-01] and [R-BRIDGE-01] are
# each checked from outside on -- and every one of them was silently dropped the next
# time alternatives.py imported this module. Three repo gates went red at once and the
# study looked, from the outside, like one that had never committed a record at all.
#
# A fix that names the keys it knows about is a fix that expires. So the rule is
# inverted: EVERYTHING ON DISK THAT THIS MODULE DOES NOT ITSELF PRODUCE IS CARRIED
# OVER, and a key added by any later stage survives an import of this one without
# anybody remembering to come back here. That is [R-ENF-01]'s "close the class, not
# the instance" applied to a build script.
try:
    _prev = json.load(open(os.path.join(HERE, 'study_numbers.json')))
    for _k, _v in _prev.items():
        if _k not in out:
            out[_k] = _v
    for _k in ('central', 'fair'):          # produced here, but the ANSWER is lenses.py's
        if _k in _prev:
            out[_k] = _prev[_k]
except (OSError, ValueError):
    pass
json.dump(out, open(os.path.join(HERE, 'study_numbers.json'), 'w'), indent=1, default=float)
print("\nwrote study_numbers.json")
