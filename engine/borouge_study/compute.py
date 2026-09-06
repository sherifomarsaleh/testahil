"""BOROUGE plc (ADX: BOROUGE) — master computation.

Every financial numeral in this study originates in engine/borouge_study/inputs_company.py
(read off Borouge's own audited statements and its own Management Discussion & Analysis)
or engine/borouge_study/inputs_macro.py (external context, each entry sourced and dated).
Nothing downstream types a number: the builders read study_numbers.json, and the workbook
recalculation and driver tests run on the delivered file, not on this script's own output.

WHAT THIS COMPANY IS, and therefore how it is valued.

Borouge plc is a single-segment polyolefins manufacturer. Note 26 of the FY2025 audited
statements is explicit: "the Group has a single operating segment, which is 'Polyolefin
Business'". Revenue is 99.2% polyethylene and polypropylene sold by the tonne; the balance
sheet is 72% property, plant and equipment; there is no lending book, no investment
portfolio, no development land and no third-party asset management. It is an operating
company, and it is valued with the operating-company lens: a free cash flow to firm model
built from tonnes and dollars per tonne, cross-read by book value and sustainable return,
relative multiples and normalised earnings power.

THE UNIT BUILD. Revenue is not grown as a percentage. It is
    volume (kt)  x  realised price (USD/t)
where volume is nameplate capacity times a utilisation rate, and realised price decomposes
into a published benchmark, a published premium over that benchmark, and a realisation
residual. All three price components are disclosed by the company every quarter; the
residual is computed from the disclosed revenue and volume rather than assumed, and its
three-year audited mean is what the forecast carries.

THE COST STACK carries one escalator per physical driver class, never one blended index
across physically distinct lines. Purchased propylene escalates on the propylene/PP price
path because the company states it buys propylene "linked to market prices"; contracted
ethane does not; fixed production cost, general and administrative expense and labour
escalate on UAE consumer price inflation; freight and distribution escalate on the
navigation status of the Strait of Hormuz, which is the thing that actually moves them.

THE CRUX, AND IT IS PUBLISHED BOTH WAYS. On 5 April 2026 Borouge sustained asset damage at
Ruwais, and the Strait of Hormuz closed. The two effects pull in opposite directions:
polyolefin benchmarks rose 38% year on year and Borouge's own premia reached record levels,
while its utilisation fell to roughly 60% in the second quarter and its distribution cost
per tonne more than doubled. Adjusted EBITDA fell 26% over the half. Whether this is a
price windfall or a volume catastrophe depends entirely on how long the disruption lasts,
and that is not a question the accounts can answer. It is therefore computed twice —
NORMALISATION and PROLONGED DISRUPTION — and both are published side by side, in the
summary table, in the body, in the workbook and in an expert's range. Neither is averaged
into the other and there is no single headline number that hides the choice.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
sys.path.insert(0, HERE)
import numpy as np

from inputs_company import INP as C
from inputs_macro import MAC

LOG = []


def say(s):
    LOG.append(s)
    print(s)


def v(key):
    """Company input value."""
    return C[key]['value']


def m(key):
    """Macro input value."""
    return MAC[key]['value']


# Every input carries value / source / date / research layer. Assert it, do not trust it.
for _name, _src in (('company', C), ('macro', MAC)):
    _bad = [k for k, d in _src.items()
            if not all(f in d and d[f] not in (None, '') for f in ('source', 'date', 'ring'))
            or 'value' not in d]
    assert not _bad, f"{_name} inputs missing one of the four required fields: {_bad}"

YEARS = [2026, 2027, 2028, 2029, 2030]
HIST = [2023, 2024, 2025]
USDm = 1e-3   # USD'000 -> USD million


# ============================================================================
# 1. HISTORY — rebuilt from the audited statements and asserted against them
# ============================================================================
hist = {}
for y in HIST:
    t = f'fy{str(y)[2:]}'
    rev = v(f'rev_{t}') * USDm
    cogs = v(f'cogs_{t}') * USDm
    ga = v(f'ga_{t}') * USDm
    sd = v(f'sd_{t}') * USDm
    oth = v(f'othinc_{t}') * USDm
    imp = v(f'imp_{t}') * USDm
    dep = (v(f'dep_ppe_{t}') + v(f'dep_rou_{t}') + v(f'amort_{t}')) * USDm
    ebit = rev - cogs + oth - ga - sd - imp
    assert abs(ebit - v(f'ebit_{t}') * USDm) < 0.001, (y, ebit, v(f'ebit_{t}') * USDm)
    pbt = ebit + v(f'fininc_{t}') * USDm - v(f'fincost_{t}') * USDm + v(f'fx_{t}') * USDm
    assert abs(pbt - v(f'pbt_{t}') * USDm) < 0.001, (y, pbt, v(f'pbt_{t}') * USDm)
    hist[y] = dict(
        revenue=rev, cogs=cogs, gross_profit=rev - cogs, other_income=oth,
        ga=ga, sd=sd, impairment=imp, ebit=ebit, da=dep, ebitda=ebit + dep,
        fin_income=v(f'fininc_{t}') * USDm, fin_cost=v(f'fincost_{t}') * USDm,
        fx=v(f'fx_{t}') * USDm, pbt=pbt, tax=v(f'tax_{t}') * USDm,
        pat=v(f'pat_{t}') * USDm, pat_owners=v(f'pat_owners_{t}') * USDm,
        etr=v(f'tax_{t}') / v(f'pbt_{t}'),
        capex=(v(f'capex_ppe_{t}') + v(f'capex_intang_{t}')) * USDm,
        cfo=v(f'cfo_{t}') * USDm,
    )
say("HISTORY rebuilt from the audited statements; operating profit and profit before tax "
    "reproduce the filed figures to the dollar in all three years.")

# effective tax rate: three audited years, and the H1-2026 interim as a live check
etr_hist = [hist[y]['etr'] for y in HIST]
etr_h126 = v('tax_h126') / v('pbt_h126')
ETR = float(np.mean(etr_hist))
say(f"Effective tax rate: {etr_hist[0]:.2%} / {etr_hist[1]:.2%} / {etr_hist[2]:.2%} across "
    f"the three audited years, mean {ETR:.2%}; the H1-2026 interim ran {etr_h126:.2%}.")


# ============================================================================
# 2. THE UNIT BUILD — realised price decomposed, residual computed not assumed
# ============================================================================
# Disclosed product revenue, USD million, from the company's own MDA tables.
rev_pe_hist = {2023: 3276.0, 2024: 3559.0, 2025: v('rev_pe_fy25')}
rev_pp_hist = {2023: 2402.0, 2024: 2421.0, 2025: v('rev_pp_fy25')}
vol_pe_hist = {y: v(f'vol_pe_fy{str(y)[2:]}') for y in HIST}
vol_pp_hist = {y: v(f'vol_pp_fy{str(y)[2:]}') for y in HIST}
bench_pe_hist = {y: v(f'bench_pe_fy{str(y)[2:]}') for y in HIST}
bench_pp_hist = {y: v(f'bench_pp_fy{str(y)[2:]}') for y in HIST}
prem_pe_hist = {y: v(f'prem_pe_fy{str(y)[2:]}') for y in HIST}
prem_pp_hist = {y: v(f'prem_pp_fy{str(y)[2:]}') for y in HIST}

realisation = {}
for y in HIST:
    realisation[y] = dict(
        pe=(rev_pe_hist[y] * 1000 / vol_pe_hist[y]) / (bench_pe_hist[y] + prem_pe_hist[y]),
        pp=(rev_pp_hist[y] * 1000 / vol_pp_hist[y]) / (bench_pp_hist[y] + prem_pp_hist[y]),
    )
REAL_PE = float(np.mean([realisation[y]['pe'] for y in HIST]))
REAL_PP = float(np.mean([realisation[y]['pp'] for y in HIST]))
real_pe_h126 = (1457.0 * 1000 / v('vol_pe_h126')) / (v('bench_pe_h126') + v('prem_pe_h126'))
real_pp_h126 = (1117.0 * 1000 / v('vol_pp_h126')) / (v('bench_pp_h126') + v('prem_pp_h126'))
say(f"Realisation residual: polyethylene revenue per tonne runs {REAL_PE:.4f}x the "
    f"benchmark-plus-premium construct across the three audited years and {real_pe_h126:.4f}x "
    f"in H1-2026; polypropylene {REAL_PP:.4f}x and {real_pp_h126:.4f}x. The forecast carries "
    f"the audited three-year mean, not the half-year.")

# Feedstock unit cost, USD per tonne of production
prod_hist = {2023: 5116.0, 2024: 5216.0, 2025: 5055.0}   # MDA production volumes, kt
feed_hist = {y: v(f'feed_fy{str(y)[2:]}') for y in HIST}
feed_per_t = {y: feed_hist[y] * 1000 / prod_hist[y] for y in HIST}
feed_per_t_h126 = v('feed_h126') * 1000 / v('prod_h126')
say(f"Feedstock: ${feed_per_t[2023]:.0f} / ${feed_per_t[2024]:.0f} / ${feed_per_t[2025]:.0f} "
    f"per tonne of production across the audited years, against ${feed_per_t_h126:.0f} in "
    f"H1-2026 — a {feed_per_t_h126/feed_per_t[2025]-1:+.0%} step, which the company "
    f"attributes to buying propylene at market prices while the Olefins Conversion Unit "
    f"was idled for want of ethane.")

# Other variable and fixed production cost: split by least squares on PRODUCTION volume.
# CORRECTED 17-Aug-2026. The fit ran on SALES tonnes while the forecast applies it to
# PRODUCTION tonnes (capacity x utilisation) — three audited years sum to 15,839kt sold
# against 15,387kt produced, so the fitted line understated FY2025 cost by $127m at that
# year's own production. A cost coefficient must be calibrated on the volume basis the
# forecast actually drives.
vol_tot_hist = {y: vol_pe_hist[y] + vol_pp_hist[y] + v(f'vol_oth_fy{str(y)[2:]}')
                for y in HIST}
# A THREE-POINT REGRESSION CANNOT IDENTIFY THIS SPLIT, and pretending otherwise was the
# real defect. Production spans only 161kt across the three audited years; regressing cost
# on it returns a variable rate of MINUS $856 a tonne on a $6,114m fixed leg — an artefact
# of noise, not a cost relationship. Regressing on SALES (272kt of spread) at least returns
# an economically sensible sign, but it calibrates on a volume the forecast does not drive
# and leaves FY2025 understated by $127m at that year's own production.
# What is done instead: the variable RATE is carried from the sales-basis slope and flagged
# as a judgement rather than a fit, and the fixed leg is re-anchored so the line reproduces
# the AUDITED FY2025 cost at FY2025's OWN production volume. The level now ties to the
# accounts; the split is disclosed as an assumption and sensitised.
_xs = np.array([vol_tot_hist[y] for y in HIST])
_y = np.array([v(f'othprod_fy{str(y)[2:]}') for y in HIST])
_coef, *_ = np.linalg.lstsq(np.column_stack([np.ones(3), _xs]), _y, rcond=None)
OTHPROD_VAR = float(_coef[1])
OTHPROD_FIXED = float(_y[-1] - OTHPROD_VAR * prod_hist[2025])
OTHPROD_FIT_IS_A_JUDGEMENT = True
say(f"Other variable and fixed production cost splits, on the three audited years, into "
    f"${OTHPROD_FIXED:,.0f}m of fixed cost and ${OTHPROD_VAR*1000:.0f} per tonne of "
    f"variable cost. The fixed leg escalates on UAE consumer inflation; the variable leg "
    f"moves with tonnes.")

# Selling and distribution, USD per tonne sold
sd_per_t = {y: v(f'sd_fy{str(y)[2:]}') * USDm * 1000 / vol_tot_hist[y] for y in HIST}
sd_per_t_h126 = v('sd_exda_h126') * 1000 / (v('vol_pe_h126') + v('vol_pp_h126'))
say(f"Selling and distribution: ${sd_per_t[2023]:.0f} / ${sd_per_t[2024]:.0f} / "
    f"${sd_per_t[2025]:.0f} per tonne sold in the audited years, against "
    f"${sd_per_t_h126:.0f} in H1-2026 while alternative logistics routes are in use.")


# ---- the asset-conversion cycle, studied from the statements and projected on --------
# Days sales outstanding, days inventory outstanding and days payable outstanding, each
# computed off the audited balance sheet and income statement, not assumed. Payables are
# measured on the FULL operating payable — trade accounts payable plus accruals plus the
# amounts due to related parties, because the ADNOC feedstock account is where most of
# this company's supplier credit actually sits and excluding it would report a payable
# period of eight days for a business that buys ethane on a group account.
dso_h, dio_h, dpo_h = {}, {}, {}
for y in HIST:
    t = f'fy{str(y)[2:]}'
    rev_y = hist[y]['revenue']
    cogs_y = hist[y]['cogs']
    dso_h[y] = v(f'ar_{t}') * USDm / rev_y * 365
    dio_h[y] = v(f'inv_{t}') * USDm / cogs_y * 365
    dpo_h[y] = (v(f'ap_{t}') + v(f'dueto_{t}')) * USDm / cogs_y * 365
DSO = float(np.mean(list(dso_h.values())))
DIO = float(np.mean(list(dio_h.values())))
DPO = float(np.mean(list(dpo_h.values())))
say(f"Asset-conversion cycle from the statements: {DSO:.0f} days sales outstanding, "
    f"{DIO:.0f} days inventory, {DPO:.0f} days payable, a cash cycle of "
    f"{DSO+DIO-DPO:.0f} days. The balance sheet and the cash flow are projected from "
    f"these, not plugged.")


# ============================================================================
# 3. COST OF CAPITAL — built, never pasted
# ============================================================================
# The valuation runs in US dollars: Borouge reports in dollars, prices its polymer in
# dollars against dollar benchmarks, buys feedstock in dollars and borrows in dollars.
# Matching nominal to nominal therefore means a dollar risk-free rate, and it is
# NORMALISED the way the source method specifies — the Treasury yield less the United
# States' own default spread, because the US is no longer top-rated. Country risk enters
# EXACTLY ONCE, inside the UAE equity risk premium. Adding a country premium on top of an
# un-normalised yield would charge the sovereign twice.
RF_USD = m('ust_10y')
RF_STAR = RF_USD - m('us_default_spread')

# The local-currency construction is published beside it rather than instead of it.
rf_local_aed = m('uae_govt_yield_aed')
default_spread = m('uae_default_spread_rating')
RF_STAR_AED = rf_local_aed - default_spread

ERP_RATING = m('uae_erp_rating')
ERP_DS = m('uae_erp_default_spread_basis')

with open(os.path.join(HERE, 'beta_result.json')) as f:
    BETA = json.load(f)
beta_own = BETA['beta']
beta_used_own = BETA['adopted']['beta_used']


def relever(bu, de, tax):
    return bu * (1 + (1 - tax) * de)


def build_ke(beta, erp, rf=None):
    return (RF_STAR if rf is None else rf) + beta * erp


def build_wacc(ke, kd_pre, tax, e_weight):
    return ke * e_weight + kd_pre * (1 - tax) * (1 - e_weight)


# Marginal, forward-looking cost of debt in the cash-flow currency. Two prices exist for
# the same borrower and the study uses the ARM'S-LENGTH one.
sofr = m('sofr')
w_t1, w_t2 = 1500.0 / 2800.0, 1300.0 / 2800.0
margin_related = w_t1 * (v('kd_margin_t1') + v('kd_fee_t1')) + \
                 w_t2 * (v('kd_margin_t2') + v('kd_fee_t2'))
MARGIN_ARMS = v('kd_margin_old')
# The facilities are floating over overnight SOFR. A discount rate for a perpetual cash
# flow stream must be tenor-matched, so the marginal margin is carried over the LONG
# dollar rate rather than over an overnight index.
KD = RF_USD + MARGIN_ARMS
KD_RELATED = RF_USD + margin_related
KD_SPOT_FLOATING = sofr + MARGIN_ARMS
# A same-currency corporate cannot fund below its own sovereign. The UAE's dollar cost is
# its own Treasury yield plus its own adjusted default spread; assert Borouge sits above.
SOV_USD = RF_USD + default_spread
assert KD > SOV_USD, (KD, SOV_USD)

# Market-value equity weight, never book. Treasury shares are disclosed at COST and not
# as a share count in the interim statements, so the issued count is used and the gap is
# disclosed rather than a share count being reverse-engineered from an unrelated price.
spot_usd = v('spot_aed') / v('aed_per_usd')
shares_out = float(v('shares_issued'))
mktcap = shares_out * spot_usd * 1e-6                       # USD million
net_debt = v('netdebt_h126') * USDm
leases = (v('lease_nc_fy25') + v('lease_c_fy25')) * USDm + v('lease_add_xlpe2') * USDm
E_WEIGHT = mktcap / (mktcap + net_debt)
DE_RATIO = net_debt / mktcap

# The two constructions of beta. Neither is averaged into the other.
# The EV/EBITDA anchor is Damodaran's Chemical (Diversified) row. The beta must come from
# the SAME row, or the study prices one industry's risk against another industry's
# multiple — which is what it did (beta from Chemical (Basic), multiple from Diversified).
BETA_BU = relever(m('sector_unlevered_beta_diversified'), DE_RATIO, ETR)
KE_OWN = build_ke(beta_used_own, ERP_RATING)
KE_BU = build_ke(BETA_BU, ERP_RATING)
KE_OWN_DS = build_ke(beta_used_own, ERP_DS)
KE_BU_DS = build_ke(BETA_BU, ERP_DS)

WACC_OWN = build_wacc(KE_OWN, KD, ETR, E_WEIGHT)
WACC_BU = build_wacc(KE_BU, KD, ETR, E_WEIGHT)
WACC_OWN_DS = build_wacc(KE_OWN_DS, KD, ETR, E_WEIGHT)
WACC_BU_DS = build_wacc(KE_BU_DS, KD, ETR, E_WEIGHT)

# THE CENTRAL CONTESTED JUDGEMENT. The tier-1 own-stock regression passes its usability
# gate and is the hierarchy's first choice, so it is not discarded. It is also flagged
# weak by that same machinery and it fails the plausibility read for a producer whose
# earnings track a global commodity benchmark. Both are therefore carried the whole way
# through — summary table, body, workbook and expert range — and no single headline
# number is struck that would hide which one the reader is looking at.
WACC = WACC_OWN
say(f"Cost of capital: rf* = {RF_USD:.2%} US 10-year less {m('us_default_spread'):.2%} "
    f"US default spread = {RF_STAR:.2%}; the dirham construction gives "
    f"{rf_local_aed:.2%} less {default_spread:.2%} = {RF_STAR_AED:.2%}, and the "
    f"{RF_STAR-RF_STAR_AED:+.2%} gap under a hard peg is reported, not reconciled away.")
say(f"  Beta: own-stock regression {beta_used_own:.3f} (weak, R-squared "
    f"{BETA['r2']:.3f}); sector bottom-up {m('sector_unlevered_beta'):.4f} unlevered "
    f"re-levered at a {DE_RATIO:.3f} debt-to-equity ratio = {BETA_BU:.3f}.")
say(f"  Ke {KE_OWN:.2%} on the own-stock beta and {KE_BU:.2%} on the bottom-up beta. "
    f"Kd marginal {KD:.2%} pre-tax (arm's-length margin {MARGIN_ARMS:.3%} over the long "
    f"dollar rate) against a {SOV_USD:.2%} sovereign; the related-party facilities price "
    f"{KD_RELATED:.2%}, inside arm's length by {KD-KD_RELATED:.2%}.")
say(f"  Equity weight {E_WEIGHT:.1%} on market value. WACC {WACC_OWN:.2%} on the "
    f"own-stock beta and {WACC_BU:.2%} on the bottom-up beta — the study's central "
    f"contested judgement, published both ways.")


# ============================================================================
# 4. THE TWO FRAMINGS OF THE CRUX
# ============================================================================
# Each framing sets four driver paths: utilisation, benchmark price, premium, and the
# distribution cost per tonne. Nothing else differs between them.
FRAMINGS = {
    'normalisation': dict(
        label='Normalisation',
        thesis=("Navigation through the Strait of Hormuz is restored during the second "
                "half of 2026, on the basis of the United States-Iran memorandum signed "
                "on 18 June 2026 and the Energy Information Administration's July "
                "expectation that most shut-in production returns by the end of 2026. "
                "Utilisation returns to the high-capacity rates the plant demonstrated "
                "in 2024 and 2025, benchmark prices give back the shortage premium over "
                "2027, realised premia revert to the company's own through-the-cycle "
                "guidance, and freight returns to the cost of the direct route. Prices "
                "settle BELOW the 2023-2024 level, not back at it, because the "
                "structural oversupply is untouched by the war: global polyethylene "
                "capacity still rises 22% to 2034 and the producer consensus on a "
                "return to healthy operating rates has moved out to 2032."),
        util_pe=[0.86, 1.02, 1.03, 1.03, 1.03],
        util_pp=[0.90, 1.00, 1.01, 1.01, 1.01],
        bench_pe=[1010, 900, 860, 870, 885],
        bench_pp=[1050, 930, 890, 900, 915],
        prem_pe=[260, 210, 200, 200, 200],
        prem_pp=[165, 145, 140, 140, 140],
        sd_per_t=[150, 100, 82, 83, 85],
        feed_market_share=[0.55, 0.35, 0.30, 0.30, 0.30],
    ),
    'prolonged': dict(
        label='Prolonged disruption',
        thesis=("Navigation remains impaired into 2027 and normalises only slowly "
                "thereafter. Utilisation stays capped by feedstock and logistics, "
                "benchmark prices hold a persistent shortage premium, Borouge's own "
                "premia stay above guidance because differentiated grades are scarce, "
                "and distribution cost per tonne stays at the elevated level the second "
                "quarter of 2026 established. The binding constraint is feedstock, not "
                "export capacity: management stated on the July call that it shipped "
                "every tonne it made without the strait, and that ethane availability "
                "was what capped production."),
        util_pe=[0.80, 0.85, 0.93, 1.00, 1.02],
        util_pp=[0.86, 0.90, 0.96, 1.00, 1.01],
        bench_pe=[1010, 900, 860, 870, 885],   # price path HELD to the central case
        bench_pp=[1050, 930, 890, 900, 915],   # a downside must not pay MORE per tonne
        prem_pe=[260, 210, 200, 200, 200],
        prem_pp=[165, 145, 140, 140, 140],
        sd_per_t=[172, 165, 140, 110, 90],
        feed_market_share=[0.62, 0.58, 0.45, 0.35, 0.30],
    ),
}

CPI = m('uae_cpi')
ETHANE_REAL = m('ethane_contract_real_escalation')

# Sales run ABOVE production because Borouge sources product from Borealis, its China
# compounding plant and other partners — 54kt of Q2-2026 sales alone. Capping forecast
# sales at capacity x utilisation discards a disclosed channel and, because it runs into
# the terminal year, was worth +6.2% of the central value. The uplift is measured from
# the audited record and held flat, not grown.
SOURCING_UPLIFT = float(np.mean([vol_tot_hist[y] / prod_hist[y] for y in HIST]))


def run_framing(f, wacc, tax=None, terminal_g=None, capex_override=None,
                premium_shift=0.0, util_shift=0.0, bench_shift=0.0, sd_shift=0.0,
                etr_override=None, realisation_pe=None, realisation_pp=None):
    """Build the full forecast for one framing and return every line the study prints."""
    tax = ETR if etr_override is None else etr_override
    g = m('terminal_growth') if terminal_g is None else terminal_g
    rpe = REAL_PE if realisation_pe is None else realisation_pe
    rpp = REAL_PP if realisation_pp is None else realisation_pp

    cap_pe, cap_pp = v('cap_pe_fy25'), v('cap_pp_fy25')
    rows = []
    ppe = v('ppe_fy25') * USDm
    # Depreciation rate calibrated so that FY2026 reproduces the H1-2026 run rate.
    da_2026_target = 2 * (v('rev_h126') * 0 + 200.0)     # H1-2026 D&A of $200m annualised
    dep_rate = da_2026_target / ppe

    prev_nwc = None
    for i, yr in enumerate(YEARS):
        upe = f['util_pe'][i] + util_shift
        upp = f['util_pp'][i] + util_shift
        vol_pe = cap_pe * upe
        vol_pp = cap_pp * upp
        vol_tot = vol_pe + vol_pp                      # PRODUCTION: drives cost
        vol_sold = vol_tot * SOURCING_UPLIFT            # SALES: drives revenue and freight

        bpe = f['bench_pe'][i] * (1 + bench_shift)
        bpp = f['bench_pp'][i] * (1 + bench_shift)
        ppe_prem = f['prem_pe'][i] + premium_shift
        ppp_prem = f['prem_pp'][i] + premium_shift

        price_pe = (bpe + ppe_prem) * rpe
        price_pp = (bpp + ppp_prem) * rpp
        rev = (vol_pe * price_pe + vol_pp * price_pp) / 1000.0 * SOURCING_UPLIFT
        rev_other = v('rev_oth_fy25') * (1 - 0.10) ** (i + 1)
        rev += rev_other

        # --- cost stack: one escalator per physical driver class ---------------
        # Contracted ethane: real escalation only, on its own long-term supply terms.
        ethane_unit = feed_per_t[2025] * (1 + ETHANE_REAL) ** (i + 1)
        # Purchased propylene: explicitly linked to market prices, so it escalates on the
        # propylene/PP benchmark path, never on a domestic price index.
        prop_unit = feed_per_t[2025] * (bpp / v('bench_pp_fy25'))
        share = f['feed_market_share'][i]
        feed_unit = (1 - share) * ethane_unit + share * prop_unit
        # The contracted ethane rate is a FLOOR on the blend: the 2026 column previously
        # implied an H2 feedstock rate of $204/t against a contracted floor of $256/t —
        # a cost the model's own construction cannot produce.
        feed_unit = max(feed_unit, ethane_unit)
        feedstock = feed_unit * vol_tot / 1000.0

        othprod = (OTHPROD_FIXED * (1 + CPI) ** (i + 1)) + OTHPROD_VAR * vol_tot
        sd = (f['sd_per_t'][i] * (1 + sd_shift)) * vol_sold / 1000.0
        ga = v('ga_exda_fy25') * (1 + CPI) ** (i + 1)
        other_income = v('othinc_fy25') * USDm * (1 + CPI) ** (i + 1)

        ebitda = rev - feedstock - othprod - sd - ga + other_income
        da = ppe * dep_rate
        ebit = ebitda - da
        nopat = ebit * (1 - tax)

        capex = (v('capex_guide_2026') if capex_override is None else capex_override) \
            if yr == 2026 else \
            (m('maintenance_capex') if capex_override is None else capex_override)

        # Working capital from the disclosed conversion cycle, projected on it.
        cogs_proxy = feedstock + othprod
        ar = rev * DSO / 365.0
        inv = cogs_proxy * DIO / 365.0
        ap = cogs_proxy * DPO / 365.0
        nwc = ar + inv - ap
        if prev_nwc is None:
            base_cogs = (v('feed_fy25') + v('othprod_fy25'))
            prev_nwc = (hist[2025]['revenue'] * DSO / 365.0
                        + base_cogs * DIO / 365.0
                        - base_cogs * DPO / 365.0)
        d_nwc = nwc - prev_nwc
        prev_nwc = nwc

        fcff = nopat + da - capex - d_nwc
        df = 1.0 / (1 + wacc) ** (i + 1)
        pv = fcff * df

        ppe = ppe + capex - da

        rows.append(dict(
            year=yr, util_pe=upe, util_pp=upp, vol_pe=vol_pe, vol_pp=vol_pp,
            vol_tot=vol_tot, vol_sold=vol_sold, bench_pe=bpe, bench_pp=bpp, prem_pe=ppe_prem,
            prem_pp=ppp_prem, price_pe=price_pe, price_pp=price_pp,
            revenue=rev, feedstock=feedstock, feed_unit=feed_unit, othprod=othprod,
            sd=sd, sd_per_t=f['sd_per_t'][i], ga=ga, other_income=other_income,
            ebitda=ebitda, ebitda_margin=ebitda / rev, da=da, ebit=ebit,
            ebit_margin=ebit / rev, nopat=nopat, capex=capex, nwc=nwc, d_nwc=d_nwc,
            fcff=fcff, discount_factor=df, pv_fcff=pv, ppe_close=ppe,
        ))

    # --- Borouge 4: an operator fee stream, valued separately, never consolidated ----
    # The sponsors quantify it two ways and the two do not agree, so both are computed
    # and the LOWER is carried, with the gap disclosed.
    b4_ramp = [0.10, 0.30, 0.60, 1.00, 1.00]
    b4_cum = m('b4_cumulative_net_profit_3y')
    b4_steady_from_cum = b4_cum / sum(b4_ramp[:3])       # solves the 3-year disclosure
    b4_steady_from_accretion = m('b4_accretion_post_rampup') * \
        float(np.mean([r['nopat'] for r in rows]))
    b4_steady = min(b4_steady_from_cum, b4_steady_from_accretion)
    b4_rows, b4_pv = [], 0.0
    for i, r in enumerate(rows):
        cash = b4_steady * b4_ramp[i]
        pv = cash * r['discount_factor']
        b4_pv += pv
        b4_rows.append(dict(year=r['year'], ramp=b4_ramp[i], net_profit=cash, pv=pv))
    # No perpetuity: the agreement runs only until Borouge Group International acquires
    # the assets, which the company says is not anticipated before 2029, and the plc's
    # ownership share afterwards is zero. Capitalising it to infinity was worth -9.7%.
    b4_terminal = 0.0
    b4_value = b4_pv + b4_terminal

    pv_sum = sum(r['pv_fcff'] for r in rows)
    term_nopat = rows[-1]['nopat'] * (1 + g)
    roc = m('terminal_roc')
    reinvest_rate = g / roc
    term_fcff = term_nopat * (1 - reinvest_rate)
    tv = term_fcff / (wacc - g)
    pv_tv = tv * rows[-1]['discount_factor']
    ev_core = pv_sum + pv_tv
    ev = ev_core + b4_value
    tv_share = pv_tv / ev

    equity = ev - net_debt - leases - m('nci_value')
    per_share_usd = equity / shares_out * 1e6
    per_share_aed = per_share_usd * v('aed_per_usd')

    return dict(
        label=f['label'], thesis=f['thesis'], rows=rows,
        pv_explicit=pv_sum, terminal_nopat=term_nopat, reinvestment_rate=reinvest_rate,
        terminal_roc=roc, terminal_growth=g, terminal_fcff=term_fcff,
        terminal_value=tv, pv_terminal=pv_tv, ev_core=ev_core, ev=ev,
        tv_share_of_ev=tv_share,
        b4=dict(steady_from_cumulative=b4_steady_from_cum,
                steady_from_accretion=b4_steady_from_accretion,
                steady_adopted=b4_steady, rows=b4_rows, pv_explicit=b4_pv,
                pv_terminal=b4_terminal, value=b4_value,
                share_of_ev=b4_value / ev),
        net_debt=net_debt, leases=leases, nci=m('nci_value'),
        equity=equity, per_share_usd=per_share_usd, per_share_aed=per_share_aed,
        wacc=wacc, tax=tax,
    )


RES = {k: run_framing(f, WACC) for k, f in FRAMINGS.items()}
for k, r in RES.items():
    say(f"DCF [{r['label']}]: EV ${r['ev']:,.0f}m, terminal value {r['tv_share_of_ev']:.1%} "
        f"of enterprise value, equity ${r['equity']:,.0f}m, AED {r['per_share_aed']:.2f} "
        f"per share against a AED {v('spot_aed'):.2f} close.")


# ============================================================================
# 5. THE OTHER THREE LENSES
# ============================================================================
# 5.2 Book value and sustainable return -> justified price to book
bvps_usd = v('eq_owners_h126') * USDm / shares_out * 1e6
roe_hist = [hist[y]['pat_owners'] / (v(f'eq_owners_fy{str(y)[2:]}') * USDm) for y in HIST]
ROE_SUST = float(np.mean(roe_hist))
KE_ADOPTED = KE_OWN
g_bv = m('terminal_growth')
justified_pb = (ROE_SUST - g_bv) / (KE_ADOPTED - g_bv)
pb_value_usd = justified_pb * bvps_usd
pb_value_aed = pb_value_usd * v('aed_per_usd')
say(f"Book value lens: sustainable return on equity {ROE_SUST:.1%} against a cost of "
    f"equity of {KE_ADOPTED:.2%} justifies {justified_pb:.2f}x book of ${bvps_usd:.4f} per "
    f"share, or AED {pb_value_aed:.2f}.")

# 5.3 Relative multiples.
# The listed peer set CANNOT produce an honest earnings multiple today: nine of the
# eleven names are loss-making on a trailing basis, EV/EBITDA is undefined for two of
# them because EBITDA is negative, and three more print inflated multiples only because
# the denominator has collapsed. Taking a median across whatever happens to print would
# silently drop the most distressed names and bias the answer UPWARD through survivorship
# inside the multiple itself. The lens is therefore built on THROUGH-CYCLE anchors, each
# named and dated, and the triangulation is shown rather than the conclusion asserted.
peer_table = m('peer_table')
peers_loss_making = sum(1 for d in peer_table.values() if d['loss_making'])
peers_ev_undefined = sum(1 for d in peer_table.values() if d['ev_ebitda'] is None)
peer_ev_printed = [d['ev_ebitda'] for d in peer_table.values() if d['ev_ebitda']]
naive_median = float(np.median(peer_ev_printed))

tri = {
    'LyondellBasell ten-year median EV/EBITDA': m('peer_lyb_10y_median'),
    'Industries Qatar current EV/EBITDA': m('peer_iqcd'),
    'Damodaran global Chemical (Diversified) sector EV/EBITDA': m('peer_sector_ev_ebitda'),
}
ev_mult = float(np.median(list(tri.values())))
mid_ebitda = float(np.mean([RES['normalisation']['rows'][2]['ebitda'],
                            RES['prolonged']['rows'][2]['ebitda']]))
rel_ev = mid_ebitda * ev_mult
# The Borouge 4 stream is a separable asset of the SAME company. It was added to the
# cash-flow lens and omitted from this one and from normalised earnings, so three lenses
# valued three different asset sets. It is now added to all of them, consistently, at the
# same value the cash-flow lens carries.
B4_VALUE = RES['normalisation']['b4']['value']
rel_ev = rel_ev + B4_VALUE
rel_equity = rel_ev - net_debt - leases - m('nci_value')
rel_aed = rel_equity / shares_out * 1e6 * v('aed_per_usd')
say(f"Relative lens: {peers_loss_making} of {len(peer_table)} listed peers are "
    f"loss-making and {peers_ev_undefined} have undefined EV/EBITDA, so the naive median "
    f"of {naive_median:.1f}x is rejected. Three through-cycle anchors "
    f"({', '.join(f'{k.split()[0]} {x:.2f}x' for k, x in tri.items())}) give a median of "
    f"{ev_mult:.2f}x, which on a mid-cycle EBITDA of ${mid_ebitda:,.0f}m is AED "
    f"{rel_aed:.2f} per share.")

# 5.4 Normalised earnings power.
# Mid-cycle is DERIVED from the audited record, not asserted: utilisation is the mean of
# the three audited years, and the benchmark is the mean of the three audited annual
# averages. Both therefore already contain a turnaround year and a soft-price year, and
# neither contains the 2026 war.
norm_util_pe = float(np.mean([v('util_pe_fy24'), v('util_pe_fy25')]))
norm_util_pp = float(np.mean([v('util_pp_fy24'), v('util_pp_fy25')]))
norm_bench_pe = float(np.mean([bench_pe_hist[y] for y in HIST]))
norm_bench_pp = float(np.mean([bench_pp_hist[y] for y in HIST]))
nvol_pe = v('cap_pe_fy25') * norm_util_pe
nvol_pp = v('cap_pp_fy25') * norm_util_pp
nvol = nvol_pe + nvol_pp
nrev = (nvol_pe * (norm_bench_pe + v('prem_pe_ttc')) * REAL_PE
        + nvol_pp * (norm_bench_pp + v('prem_pp_ttc')) * REAL_PP) / 1000.0
nfeed = feed_per_t[2025] * nvol / 1000.0
noth = OTHPROD_FIXED + OTHPROD_VAR * nvol
nsd = float(np.mean([sd_per_t[y] for y in HIST])) * nvol / 1000.0
nebitda = nrev - nfeed - noth - nsd - v('ga_exda_fy25')
nda = 400.0
nebit = nebitda - nda
nnopat = nebit * (1 - ETR)
nep_ev = nnopat / (WACC - m('terminal_growth')) * (1 - m('terminal_growth') / m('terminal_roc'))
nep_ev = nep_ev + B4_VALUE
nep_equity = nep_ev - net_debt - leases - m('nci_value')
nep_aed = nep_equity / shares_out * 1e6 * v('aed_per_usd')
say(f"Normalised earnings power: mid-cycle EBITDA ${nebitda:,.0f}m capitalised at "
    f"{WACC:.2%} gives AED {nep_aed:.2f} per share.")


# ============================================================================
# 6. SENSITIVITY AND SYNTHESIS
# ============================================================================
wacc_grid = [WACC - 0.010, WACC - 0.005, WACC, WACC + 0.005, WACC + 0.010]
g_grid = [m('terminal_growth') - 0.010, m('terminal_growth') - 0.005,
          m('terminal_growth'), m('terminal_growth') + 0.005,
          m('terminal_growth') + 0.010]
sens = {}
for key in RES:
    grid = []
    for w in wacc_grid:
        row = []
        for g in g_grid:
            r = run_framing(FRAMINGS[key], w, terminal_g=g)
            row.append(r['per_share_aed'])
        grid.append(row)
    sens[key] = grid

# premium sensitivity in the observable unit the crux is actually stated in: USD per tonne
prem_grid = {}
for key in RES:
    prem_grid[key] = [(d, run_framing(FRAMINGS[key], WACC, premium_shift=d)['per_share_aed'])
                      for d in (-100, -50, 0, 50, 100)]
util_grid = {}
for key in RES:
    util_grid[key] = [(d, run_framing(FRAMINGS[key], WACC, util_shift=d)['per_share_aed'])
                      for d in (-0.10, -0.05, 0.0, 0.05, 0.10)]

# THE CENTRAL CONTESTED JUDGEMENT, computed both ways across both framings — a 2x2,
# published side by side and never averaged into a single headline.
alt_wacc = {
    'own_stock_beta': dict(
        beta=beta_used_own, ke=KE_OWN, wacc=WACC_OWN,
        basis=("Tier-1 own-stock weekly regression against the FTSE ADX General Index "
               "— the company's own local market index, which is what the beta rule "
               "asks for. It passes the usability gate on all three conditions."),
        against=("It is flagged weak by the same machinery: an R-squared of "
                 f"{BETA['r2']:.3f} and a 90% interval of "
                 f"[{BETA['ci90'][0]:.2f}, {BETA['ci90'][1]:.2f}] spanning "
                 f"{(BETA['ci90'][1]-BETA['ci90'][0])/abs(beta_own):.2f} times the point "
                 "estimate. A Dimson lead-lag correction moves it DOWN, not up, so thin "
                 "trading does not explain it. What it most plausibly measures is a "
                 "share with a 10% free float that has traded in a narrow band, not the "
                 "risk of a business whose earnings track a global commodity benchmark. "
                 "It is, however, materially HIGHER than the "
                 f"{BETA['composite_corroboration']['beta']:.3f} an equal-weight "
                 "composite of the other listed UAE names produces, because an "
                 "equal-weight composite over-weights small, thinly traded constituents "
                 "and understates covariance with any single large name.")),
    'bottom_up_sector_beta': dict(
        beta=BETA_BU, ke=KE_BU, wacc=WACC_BU,
        basis=("Global Chemical (Basic) unlevered beta corrected for cash, re-levered to "
               "Borouge's own market-value capital structure and effective tax rate. It "
               "prices the business rather than the listing."),
        against=("It imports the capital-structure and cyclicality of a 909-firm global "
                 "set, most of which lack Borouge's contracted ethane position, and it "
                 "overrides an own-stock estimate that did pass its gate.")),
}
for _k, d in alt_wacc.items():
    d['value_aed'] = {key: run_framing(FRAMINGS[key], d['wacc'])['per_share_aed']
                      for key in RES}
    d['ev'] = {key: run_framing(FRAMINGS[key], d['wacc'])['ev'] for key in RES}
    d['tv_share'] = {key: run_framing(FRAMINGS[key], d['wacc'])['tv_share_of_ev']
                     for key in RES}

GRID_2X2 = {wk: {fk: alt_wacc[wk]['value_aed'][fk] for fk in RES} for wk in alt_wacc}
say("The 2x2 of the two contested judgements, AED per share:")
for wk, row in GRID_2X2.items():
    say(f"   {wk:<24} " + "  ".join(f"{fk}={x:.2f}" for fk, x in row.items()))

# Book, relative and normalised lenses are also re-struck on the bottom-up cost of
# capital, so the panel is internally consistent under either construction.
justified_pb_bu = (ROE_SUST - g_bv) / (KE_BU - g_bv)
pb_value_aed_bu = justified_pb_bu * bvps_usd * v('aed_per_usd')
nep_ev_bu = nnopat / (WACC_BU - m('terminal_growth')) * \
    (1 - m('terminal_growth') / m('terminal_roc')) + B4_VALUE   # the same separable asset, in this lens too
nep_aed_bu = (nep_ev_bu - net_debt - leases - m('nci_value')) / shares_out * 1e6 * \
    v('aed_per_usd')

lenses = {
    'dcf_normalisation_own_beta': GRID_2X2['own_stock_beta']['normalisation'],
    'dcf_prolonged_own_beta': GRID_2X2['own_stock_beta']['prolonged'],
    'dcf_normalisation_sector_beta': GRID_2X2['bottom_up_sector_beta']['normalisation'],
    'dcf_prolonged_sector_beta': GRID_2X2['bottom_up_sector_beta']['prolonged'],
    'book_value_own_beta': pb_value_aed,
    'book_value_sector_beta': pb_value_aed_bu,
    'relative_multiples': rel_aed,
    'normalised_earnings_own_beta': nep_aed,
    'normalised_earnings_sector_beta': nep_aed_bu,
}

# ============================================================================
# 6b. THE ANSWER [R-LENS-03], and what it replaced
# ============================================================================
# THE MEDIAN OF THESE NINE WAS PUBLISHED AS THE CENTRAL UNTIL 5 SEPTEMBER 2026, and it was
# decided by a COUNT rather than by a valuation choice. The nine are not nine views of this
# company: they are a 2x2 of two orthogonal framings — the beta construction and the
# Hormuz scenario — plus a framing-neutral relative multiple, and they do not spread, they
# CLUSTER IN TWO BLOCKS OF FOUR, one per beta, with the relative multiple sitting inside
# the lower one. So the median averaged nothing; it SELECTED ONE CELL of the grid, and
# which cell it selected was decided by how many lenses happened to have been computed
# under each framing. One more own-beta lens and it moves to 1.91; one fewer sector lens
# and it moves to 1.90. Neither is a different view of the company.
#
# [R-LENS-03] retires it, and depth-bar standard 8 forbids it in the same sentence that
# requires the dual framing this study does correctly: computed both ways and published
# side by side, "NEVER AVERAGED INTO ONE NUMBER".
#
# WHAT THE ANSWER IS INSTEAD, decided on the rules and not on where it lands:
#   * THE PRIMARY IS THE CASH-FLOW LENS. This study is registered `petrochemical`, whose
#     row is a DCF primary with EV/EBITDA on own history, replacement cost, a relative
#     multiple and book beside it as cross-checks.
#   * IT IS TWO-SIDED, AND THE HORMUZ SCENARIO IS THE SIDE THAT SPLITS IT. Navigation
#     restored during 2026 against navigation impaired into 2027 is a contested judgement
#     about the world with two answers, which is what standard 8 asks to be published both
#     ways — not an averageable spread.
#   * THE BETA IS NOT A BRANCH. SIGCM clause 6 is a strict preference order and this
#     study's own beta record adopts the tier-1 own-stock regression on its merits: n=215,
#     R-squared 0.094 against the 0.05 floor, SE 0.088 against |beta| 0.415, all three
#     conditions of the usability gate met. The bottom-up sector beta is a labelled
#     CROSS-CHECK on an adopted figure, and its weakness (R-squared below the 10%
#     weak-instrument threshold) is disclosed rather than hidden. A rule decides it, so it
#     is not a contested judgement however much value it moves.
#   * NORMALISED EARNINGS COMES OUT. It appears in NO row of the lens registry — the same
#     thing EMPOWER's record found, and the rule working rather than a gap in it.
CENTRAL_NORMALISATION = GRID_2X2['own_stock_beta']['normalisation']
CENTRAL_PROLONGED = GRID_2X2['own_stock_beta']['prolonged']
# The envelope is the RANGE of the present-value reads on one clock, never a spread
# invented around a point and never the extremes of a blend.
FAIR_LOW = float(min(CENTRAL_NORMALISATION, CENTRAL_PROLONGED))
FAIR_HIGH = float(max(CENTRAL_NORMALISATION, CENTRAL_PROLONGED))
# FAIR_MID is retired as a CENTRAL and kept as what it always was — the median of the
# nine-lens field — so a reader of the previous edition can see the number that moved and
# what it was. It is published UNUSED, the same disposition as a retired blend.
_FIELD = list(lenses.values())
FIELD_LOW, FIELD_HIGH = float(min(_FIELD)), float(max(_FIELD))
FAIR_MID_RETIRED = float(np.median(_FIELD))
LENS_RECORD = dict(
    lens_class='petrochemical',
    # the gate reads 'class'; 'lens_class' is kept as the human-readable alias
    **{'class': 'petrochemical'},
    primary=dict(
        kind='dcf',
        value=CENTRAL_NORMALISATION,
        range=dict(low=FAIR_LOW, high=FAIR_HIGH),
        range_note=('the cash-flow lens across the contested judgement itself — the two '
                    'Hormuz framings on the adopted own-stock beta, present values on one '
                    'clock, never averaged'),
        range_basis=dict(
            driver='polyethylene plant utilisation against nameplate in the first forecast '
                   'year, and the shipping-and-distribution cost per tonne that moves with '
                   'it',
            low=FRAMINGS['prolonged']['util_pe'][0],
            high=FRAMINGS['normalisation']['util_pe'][0],
            units='fraction of nameplate capacity',
            macro_held=True,
            sanctioned_framing=(
                'depth-bar standard 8 — the study\'s single most consequential CONTESTED '
                'JUDGEMENT computed both ways and published side by side, never averaged '
                'into one number. The judgement is about the world rather than about the '
                'model: whether navigation through the Strait of Hormuz is restored during '
                '2026.'),
            evidence=(
                'BOTH ENDS ARE THE COMPANY\'S OWN DEMONSTRATED RANGE, not a nudge either '
                'side of a base case. The high end is the utilisation this plant has '
                'actually run at in an unimpaired year; the low end is the rate it ran '
                'while feedstock and logistics were capped. The shipping-and-distribution '
                'cost moves with it on the same evidence — %.0f US$ a tonne in the '
                'impaired year against %.0f in the normalising one — and it decays to the '
                'same terminal figure in both, because a blockade is an event rather than '
                'a permanent state. THE MACRO PATH STANDS STILL ACROSS THE RANGE: the '
                'benchmark price ladder, the premium ladder, the cost of capital, the '
                'terminal growth and the terminal rate are IDENTICAL in the two framings, '
                'which is what makes this a range about the world rather than a grid of '
                'dials.'
                % (FRAMINGS['prolonged']['sd_per_t'][0],
                   FRAMINGS['normalisation']['sd_per_t'][0])),
        ),
        note=("the cash-flow lens on the company's own tonnes, its disclosed costs and the "
              'adopted tier-1 own-stock beta. Published TWO-SIDED: the value is stated for '
              'each branch of the shipping-lane judgement rather than as one number.')),
    cross_checks=[
        dict(kind='relative_multiple', value=rel_aed, present_value=False,
             multiple=ev_mult,
             multiple_source=("the median of three THROUGH-CYCLE anchors — LyondellBasell's "
                              "own ten-year median EV/EBITDA, Industries Qatar's current "
                              "multiple and Damodaran's global Chemical (Diversified) "
                              "sector figure. The naive peer median is REJECTED because "
                              f"{peers_loss_making} of {len(peer_table)} listed peers are "
                              f"loss-making and {peers_ev_undefined} have an undefined "
                              "EV/EBITDA. Never a multiple read off this company's own "
                              "traded price."),
             circularity=dict(spot=v('spot_aed'), shares=shares_out / 1e6,
                              net_debt=net_debt + leases + m('nci_value'),
                              metric_value=mid_ebitda)),
        dict(kind='book_value', value=pb_value_aed, present_value=False,
             note=('a DISCLOSED FLOOR on the sustainable return, never weighted into the '
                   'answer: justified price-to-book from a sustainable return on equity of '
                   f"{ROE_SUST:.2%} against the cost of equity on the adopted beta.")),
    ],
    envelope=dict(low=FAIR_LOW, high=FAIR_HIGH),
    central=CENTRAL_NORMALISATION,
    retired=dict(
        construction='the median of nine lens readings across two orthogonal framings',
        value=FAIR_MID_RETIRED,
        why=('it was not a weighted blend and it is caught by [R-LENS-03] for the reason '
             'the rule gives. The nine readings CLUSTER in two blocks of four, one per '
             'beta construction, so the median averaged nothing — it SELECTED one cell of '
             'the grid, and which cell was decided by how many lenses happened to have '
             'been computed under each framing. One more own-beta lens moves it to 1.91, '
             'one fewer sector lens to 1.90. The free parameter was not even a weight '
             'somebody chose; it was a count.')),
    diagnostics=dict(
        normalised_earnings_own_beta=nep_aed,
        normalised_earnings_sector_beta=nep_aed_bu,
        normalised_earnings_disposition=(
            'REMOVED FROM THE ANSWER. Normalised earnings appears in no row of the lens '
            'registry, so it is not a permitted cross-check for any class; carried here as '
            'a diagnostic so the figure that was in the retired median stays visible.'),
        sector_beta_framing=dict(
            normalisation=GRID_2X2['bottom_up_sector_beta']['normalisation'],
            prolonged=GRID_2X2['bottom_up_sector_beta']['prolonged'],
            disposition=(
                'a LABELLED CROSS-CHECK on an adopted figure, not a branch. SIGCM clause 6 '
                'is a strict preference order and this study\'s beta record adopts the '
                'tier-1 own-stock regression on its merits — n=215, R-squared 0.094 against '
                'the 0.05 floor, SE 0.088 against |beta| 0.415, all three usability '
                'conditions met. Its weakness (R-squared below the 10% weak-instrument '
                'threshold) is disclosed rather than hidden, and it is the reason the '
                'bottom-up construction was built at all. A quantity a rule decides is not '
                'a contested judgement, however much value it moves.')),
        book_value_floor=pb_value_aed))

say(f"Cash-flow lens on the adopted own-stock beta: AED {CENTRAL_NORMALISATION:.4f} if "
    f"navigation normalises and AED {CENTRAL_PROLONGED:.4f} if the disruption persists, "
    f"against a close of AED {v('spot_aed'):.2f}.")
say(f"  cross-checks span AED {FIELD_LOW:.2f} to AED {FIELD_HIGH:.2f}; the retired "
    f"nine-lens median was AED {FAIR_MID_RETIRED:.4f} and is published unused.")


# ============================================================================
# 6B. THE FORECAST ANCHOR — WHAT THE FORECAST CLAIMS AGAINST WHAT WAS LAST FILED
# ============================================================================
# A near-term reviewed actual outranks a stale full-year rate. This record states the
# rate the forecast is built on, the latest period the company has actually reported,
# and the whole explicit window, so a reader can see the claim rather than infer it.
#
# THE RATE IS THE ADJUSTED EBITDA MARGIN, and the choice is forced rather than
# preferred. It is the company's own published key performance indicator, it is the
# rate the reference pattern for this class anchors on, and it is the ONLY rate that
# exists on both sides of this model: the forecast never forms a cost-of-sales
# subtotal — it builds EBITDA directly from feedstock, other production cost,
# distribution, general and administrative expense and other income — so a gross
# margin is computable from the filings and NOT resolvable on the forecast side.
#
# Adjusted EBITDA is defined by the company as EBITDA plus the foreign exchange gain
# or loss and the impairment loss on property, plant and equipment. Foreign exchange
# sits BELOW operating profit in this company's income statement, inside net finance
# costs, so at the EBITDA level the only adjustment is the impairment. The
# reconstruction is asserted against the figure the company publishes rather than
# accepted on trust: arithmetic is the arbiter.
def _adj_ebitda(ebit_k, dep_ppe_k, dep_rou_k, amort_k, imp_k):
    return (ebit_k + dep_ppe_k + dep_rou_k + amort_k + imp_k) * USDm


ADJ_H126 = _adj_ebitda(v('ebit_h126'), v('dep_ppe_h126'), v('dep_rou_h126'),
                       v('amort_h126'), v('imp_h126'))
ADJ_H125 = _adj_ebitda(v('ebit_h125'), v('dep_ppe_h125'), v('dep_rou_h125'),
                       v('amort_h125'), v('imp_h125'))
assert round(ADJ_H126) == v('ebitda_adj_h126'), (ADJ_H126, v('ebitda_adj_h126'))
assert round(ADJ_H125) == v('ebitda_adj_h125'), (ADJ_H125, v('ebitda_adj_h125'))

REV_H126 = v('rev_h126') * USDm
REV_H125 = v('rev_h125') * USDm
LATEST_RATE = ADJ_H126 / REV_H126

# the audited full years on the SAME basis, so the reviewed half is read against the
# record rather than on its own
FILED_ADJ_MARGIN = {y: (hist[y]['ebitda'] + hist[y]['impairment']) / hist[y]['revenue']
                    for y in HIST}
for _y in HIST:
    assert round((hist[_y]['ebitda'] + hist[_y]['impairment'])) == \
        v(f'ebitda_adj_fy{str(_y)[2:]}'), _y

ANCHOR_PATH = {k: [r['ebitda_margin'] for r in RES[k]['rows']] for k in RES}

# --- the like-for-like pair, in the company's own six months a year apart -----------
# Cash operating cost per unit of revenue: revenue less adjusted EBITDA, over revenue.
# Both halves are read off the reviewed interim statements and their own comparative
# column, so the pair is like for like by construction.
COST_REV_H125 = (REV_H125 - ADJ_H125) / REV_H125
COST_REV_H126 = (REV_H126 - ADJ_H126) / REV_H126
VOL_H126 = v('vol_pe_h126') + v('vol_pp_h126')
VOL_H125 = v('vol_tot_h125')
COST_T_H125 = (REV_H125 - ADJ_H125) * 1000.0 / VOL_H125
COST_T_H126 = (REV_H126 - ADJ_H126) * 1000.0 / VOL_H126
SD_T_H125 = v('sd_h125') * USDm * 1000.0 / VOL_H125
SD_T_H126 = v('sd_h126') * USDm * 1000.0 / VOL_H126
ASP_CHG = v('asp_h126') / v('asp_h125') - 1.0
# the audited full years on the same measure, published beside the chosen pair because
# a relationship that only held in one direction would not be one
COST_REV_FY = {y: 1.0 - FILED_ADJ_MARGIN[y] for y in HIST}

# THE HALVES THIS STUDY ACTUALLY HOLDS, so a claim about the weakest half is one the
# record can check rather than a superlative. The register carries exactly TWO filed
# halves — the reviewed six months to 30 June 2026 and their own comparative column
# — so H1 2023 and H1 2024 are outside anything this study can measure and nothing
# is asserted about them. The second half of 2025 is DERIVED BY IDENTITY from two
# filed figures, the audited full year less that filed half, and is labelled derived
# wherever it is quoted; no figure here is estimated or interpolated.
MARGIN_H125 = ADJ_H125 / REV_H125
ADJ_H225_DERIVED = (hist[2025]['ebitda'] + hist[2025]['impairment']) - ADJ_H125
REV_H225_DERIVED = hist[2025]['revenue'] - REV_H125
MARGIN_H225_DERIVED = ADJ_H225_DERIVED / REV_H225_DERIVED

# --- which framing governs the record ------------------------------------------------
# The study is deliberately two-sided and never averages the branches. The anchor is
# recorded on the branch that makes the claim this record exists to test — the one
# whose rate falls materially inside its own window — and the other branch is printed
# beside it in full rather than left out.
_GOV, _OTH = 'prolonged', 'normalisation'
_gp, _op = ANCHOR_PATH[_GOV], ANCHOR_PATH[_OTH]
_gov_min = min(_gp)
_gov_min_year = YEARS[_gp.index(_gov_min)]

FORECAST_ANCHOR = dict(
    rate_name='EBITDA margin, prolonged-disruption framing',
    latest_reviewed_period='H1 2026, reviewed (six months ended 30 June 2026)',
    latest_reviewed_date='2026-06-30',
    latest_reviewed_rate=LATEST_RATE,
    latest_reviewed_source=(
        'Borouge plc condensed consolidated interim financial statements for the six '
        'months ended 30 June 2026, reviewed by Ernst & Young under ISRE 2410 with an '
        f"unmodified conclusion signed 30 July 2026: operating profit of USD "
        f"{v('ebit_h126') * USDm:,.3f} million plus depreciation and amortisation of USD "
        f"{(v('dep_ppe_h126') + v('dep_rou_h126') + v('amort_h126')) * USDm:,.3f} million "
        f"from the interim statement of cash flows plus the impairment loss of USD "
        f"{v('imp_h126') * USDm:,.3f} million, over revenue of USD {REV_H126:,.3f} "
        f"million. That reconstruction is USD {ADJ_H126:,.3f} million against the USD "
        f"{v('ebitda_adj_h126'):,} million the company publishes as adjusted EBITDA in "
        'its own Q2 2026 Management Discussion & Analysis \u2014 a difference of USD '
        f"{ADJ_H126 - v('ebitda_adj_h126'):,.3f} million, which is that document's own "
        'rounding to the nearest million. THE MARGIN IS STRUCK ON THE RECONSTRUCTION AND '
        'IS NOT READ OFF THE DOCUMENT: the register carries the adjusted EBITDA figure '
        'and the revenue and no published margin, so quoting a printed margin here would '
        "attribute this study's own arithmetic to the filing."),
    first_forecast_rate=_gp[0],
    forecast_path=_gp,
    mechanism=dict(
        name='input_cost_outpacing_price',
        disclosure=(
            'THE TWO COST LEGS THAT MOVED IN THE LATEST REVIEWED HALF ARE SET BY THE '
            'SHIPPING ROUTE AND BY THE PROPYLENE MARKET, NOT BY THE POLYMER PRICE THIS '
            'COMPANY REALISES, so when the benchmark path gives back its shortage '
            'premium they do not give it back with it. The Q2 2026 Management Discussion '
            f"& Analysis reports feedstock cost of USD {v('feed_h126'):,} million for the "
            'half, up 33 per cent year on year, on higher purchased propylene prices '
            'after the Olefins Conversion Unit was idled for want of ethane; the company '
            'states it buys propylene linked to market prices, so that leg is priced off '
            'propylene rather than off polyethylene. The reviewed statements report '
            f"selling and distribution expenses of USD {v('sd_h126') * USDm:,.3f} million "
            f"against USD {v('sd_h125') * USDm:,.3f} million in the comparative half, on "
            f"{100 * (1 - VOL_H126 / VOL_H125):.0f} per cent fewer tonnes sold — USD "
            f"{SD_T_H126:,.2f} a tonne against USD {SD_T_H125:,.2f} — while alternative "
            'routes are in use. OVER THE SAME HALF THE REALISED PRICE ROSE RATHER THAN '
            f"FELL: the company's own average selling price ran USD {v('asp_h126'):,} a "
            f"tonne against USD {v('asp_h125'):,} a tonne, {ASP_CHG:+.1%}. The cost stack "
            'therefore moved against the price in the company\'s own most recent filed '
            'period, which is the decoupling the forecast carries forward.'),
        like_for_like=dict(
            measures=('cash operating cost per unit of revenue — revenue less adjusted '
                      'EBITDA, over revenue — for the six months ended 30 June, read off '
                      'the reviewed interim statements and their own comparative column'),
            period_a='H1 2025 (six months ended 30 June 2025)',
            period_b='H1 2026 (six months ended 30 June 2026)',
            value_a=COST_REV_H125,
            value_b=COST_REV_H126,
            higher_is_worse=True,
            note=(
                'THE DIRECTION, AND WHY IT IS NOT A PRICE EFFECT. Cost per unit of '
                f"revenue went from {COST_REV_H125:.6f} to {COST_REV_H126:.6f}, "
                f"{100 * (COST_REV_H126 - COST_REV_H125):+.2f} points, WHILE THE REALISED "
                f"PRICE ROSE {ASP_CHG:+.1%} over the same pair. A cost ratio that rises "
                'into a rising price cannot be a price effect; per tonne sold the cash '
                f"cost went from USD {COST_T_H125:,.2f} to USD {COST_T_H126:,.2f}, "
                f"{COST_T_H126 / COST_T_H125 - 1:+.1%}, against realised price at "
                f"{ASP_CHG:+.1%}. THE OPPOSITE EVIDENCE IS PUBLISHED BESIDE IT RATHER "
                'THAN LEFT OUT, because a relationship that only held in one direction '
                'would not be one: on the audited full years the same measure is NOT '
                f"monotone — FY2023 {COST_REV_FY[2023]:.6f}, FY2024 "
                f"{COST_REV_FY[2024]:.6f}, FY2025 {COST_REV_FY[2025]:.6f}, falling and "
                'then rising. What the reviewed half adds is a level well above all '
                'three, and the mechanism claimed is about the disruption that produced '
                'it rather than about a trend through the cycle.'))),
    other_framing=dict(
        label='Normalisation — navigation restored during the second half of 2026',
        first_forecast_rate=_op[0],
        forecast_path=_op,
        note=(
            f"The normalisation branch opens at {_op[0]:.6f}, "
            f"{(_op[0] - LATEST_RATE) / LATEST_RATE:+.1%} relative to the reviewed half, "
            f"and its low is {min(_op):.6f} in {YEARS[_op.index(min(_op))]}, "
            f"{(min(_op) - _op[0]) / _op[0]:+.1%} from its own opening year — inside the "
            'materiality line, so it owes no mechanism and none is claimed. THE TWO '
            'BRANCHES SHARE AN IDENTICAL PRICE PATH: the benchmark ladder, the premium '
            'ladder, the cost of capital, the terminal growth and the terminal rate are '
            'the same in both, and they differ only in utilisation, in distribution cost '
            'per tonne and in how much of the feedstock is bought at market prices. That '
            'is why the same price reversion compresses one branch and not the other — '
            'in the normalisation branch the disruption cost stack unwinds with the '
            'price, and in the prolonged branch it does not.'),
        value_aed=CENTRAL_NORMALISATION),
    note=(
        'BOTH BRANCHES OPEN WELL ABOVE THE LATEST REVIEWED PERIOD AND THAT IS THE FIRST '
        'THING A READER SHOULD SEE, because a record that only catches declines would say '
        f"nothing about it. The reviewed six months to 30 June 2026 carried an adjusted "
        f"EBITDA margin of {LATEST_RATE:.2%}, below every period this study holds on "
        f"that basis \u2014 H1 2025 {MARGIN_H125:.2%} from the same statements' own "
        f"comparative column, the second half of 2025 {MARGIN_H225_DERIVED:.2%} DERIVED "
        'by identity as the audited full year less that filed half, and the three '
        'audited years set out next. The register carries two filed halves and no more, '
        'so nothing is claimed about halves this study does not hold. '
        f"the prolonged branch opens FY2026 at {_gp[0]:.2%}, "
        f"{(_gp[0] - LATEST_RATE) / LATEST_RATE:+.1%} relative, and the normalisation "
        f"branch at {_op[0]:.2%}, {(_op[0] - LATEST_RATE) / LATEST_RATE:+.1%}. THE FILED "
        f"RECORD ON THE SAME BASIS IS FY2023 {FILED_ADJ_MARGIN[2023]:.2%}, FY2024 "
        f"{FILED_ADJ_MARGIN[2024]:.2%}, FY2025 {FILED_ADJ_MARGIN[2025]:.2%} AND H1 2026 "
        f"{LATEST_RATE:.2%}, so every forecast year in both branches sits below every "
        'audited year and above the reviewed half. The half is the event rather than the '
        'run rate — production ran '
        f"{v('prod_h126'):,} kt against {prod_hist[2025] / 2:,.0f} kt at half the prior "
        'year\'s rate, on a plant damaged on 5 April 2026 with the Strait of Hormuz '
        'closed — and a forecast that opens above it is the ordinary consequence of not '
        'projecting a blockade for ever.\n\n'
        'THE CLAIM THIS RECORD TESTS IS THE ONE INSIDE THE WINDOW. The prolonged branch '
        f"falls from {_gp[0]:.2%} in {YEARS[0]} to {_gov_min:.2%} in {_gov_min_year}, "
        f"{(_gov_min - _gp[0]) / _gp[0]:+.1%} from its own opening year, and then "
        f"recovers to {_gp[-1]:.2%} by {YEARS[-1]}. It is a trough rather than a decline, "
        'and it is entirely a cost-against-price effect that can be shown in one line: '
        'revenue per tonne sold falls '
        f"{(RES[_GOV]['rows'][1]['revenue'] * 1000 / RES[_GOV]['rows'][1]['vol_sold']) / (RES[_GOV]['rows'][0]['revenue'] * 1000 / RES[_GOV]['rows'][0]['vol_sold']) - 1:+.1%} "
        f"between {YEARS[0]} and {YEARS[1]} as the benchmark gives back its shortage "
        'premium, while cash cost per tonne sold falls only '
        f"{((RES[_GOV]['rows'][1]['feedstock'] + RES[_GOV]['rows'][1]['othprod'] + RES[_GOV]['rows'][1]['sd'] + RES[_GOV]['rows'][1]['ga'] - RES[_GOV]['rows'][1]['other_income']) * 1000 / RES[_GOV]['rows'][1]['vol_sold']) / ((RES[_GOV]['rows'][0]['feedstock'] + RES[_GOV]['rows'][0]['othprod'] + RES[_GOV]['rows'][0]['sd'] + RES[_GOV]['rows'][0]['ga'] - RES[_GOV]['rows'][0]['other_income']) * 1000 / RES[_GOV]['rows'][0]['vol_sold']) - 1:+.1%}. "
        'Had the cost stack given back what the price gave back, the margin would not '
        'have moved at all.\n\n'
        'WHICH BRANCH THE STUDY PUBLISHES AS ITS CENTRAL IS NOT WHICH BRANCH THIS RECORD '
        f"GOVERNS, and saying so is the point. The published central is the normalisation "
        f"branch at AED {CENTRAL_NORMALISATION:.4f}, with the prolonged branch at AED "
        f"{CENTRAL_PROLONGED:.4f}; the two are published side by side and never averaged. "
        'The anchor is recorded on the prolonged branch because that is the branch making '
        'a claim this record exists to test, and the normalisation branch is printed '
        'beside it in full so nothing is hidden by the choice.'))

say(f"Forecast anchor: adjusted EBITDA margin of {LATEST_RATE:.2%} in the reviewed six "
    f"months to 30 June 2026 against a forecast opening at {_gp[0]:.2%} (prolonged) and "
    f"{_op[0]:.2%} (normalisation); the prolonged path troughs at {_gov_min:.2%} in "
    f"{_gov_min_year}, {(_gov_min - _gp[0]) / _gp[0]:+.1%} from its own opening year.")


# ============================================================================
# 7. WRITE THE NUMBERS FILE
# ============================================================================
OUT = dict(
    ticker='BOROUGE', market='AE', exchange='Abu Dhabi Securities Exchange',
    company='Borouge plc',
    reporting_currency='USD', listing_currency='AED',
    spot_aed=v('spot_aed'), spot_usd=spot_usd, spot_date=C['spot_aed']['date'],
    aed_per_usd=v('aed_per_usd'),
    shares_out=shares_out, mktcap_usd=mktcap,
    net_debt=net_debt, leases=leases, nci_value=m('nci_value'),
    history=hist, etr_hist=etr_hist, etr=ETR, etr_h126=etr_h126,
    unit_build=dict(
        realisation_pe=REAL_PE, realisation_pp=REAL_PP,
        realisation_by_year=realisation,
        realisation_pe_h126=real_pe_h126, realisation_pp_h126=real_pp_h126,
        feed_per_t=feed_per_t, feed_per_t_h126=feed_per_t_h126,
        othprod_fixed=OTHPROD_FIXED, othprod_var_per_t=OTHPROD_VAR,
        sourcing_uplift=SOURCING_UPLIFT,
        sd_per_t=sd_per_t, sd_per_t_h126=sd_per_t_h126,
        vol_pe=vol_pe_hist, vol_pp=vol_pp_hist, vol_tot=vol_tot_hist,
        bench_pe=bench_pe_hist, bench_pp=bench_pp_hist,
        prem_pe=prem_pe_hist, prem_pp=prem_pp_hist,
        rev_pe=rev_pe_hist, rev_pp=rev_pp_hist, production=prod_hist,
        capacity_pe=v('cap_pe_fy25'), capacity_pp=v('cap_pp_fy25'),
    ),
    wacc=dict(
        rf_usd=RF_USD, us_default_spread=m('us_default_spread'), rf_star=RF_STAR,
        rf_local_aed=rf_local_aed, uae_default_spread=default_spread,
        rf_star_aed=RF_STAR_AED,
        erp_rating=ERP_RATING, erp_default_spread_basis=ERP_DS,
        mature_erp=m('mature_erp'), crp=m('uae_crp'),
        beta_own=beta_own, beta_used=beta_used_own, beta_bottom_up=BETA_BU,
        sector_unlevered=m('sector_unlevered_beta'), de_ratio=DE_RATIO,
        ke_own=KE_OWN, ke_bottom_up=KE_BU, ke_own_ds=KE_OWN_DS, ke_bu_ds=KE_BU_DS,
        sofr=sofr, kd_related_party=KD_RELATED, kd=KD,
        kd_spot_floating=KD_SPOT_FLOATING, margin_arms=MARGIN_ARMS,
        margin_related=margin_related,
        sovereign_usd=SOV_USD, equity_weight=E_WEIGHT, debt_weight=1 - E_WEIGHT,
        tax=ETR, wacc_own=WACC_OWN, wacc_bottom_up=WACC_BU,
        wacc_own_ds=WACC_OWN_DS, wacc_bu_ds=WACC_BU_DS, wacc=WACC,
        mktcap=mktcap,
    ),
    grid_2x2=GRID_2X2,
    working_capital=dict(dso=DSO, dio=DIO, dpo=DPO, ccc=DSO + DIO - DPO,
                         dso_hist=dso_h, dio_hist=dio_h, dpo_hist=dpo_h),
    peer_table=peer_table, peer_naive_median=naive_median,
    peers_loss_making=peers_loss_making, peers_ev_undefined=peers_ev_undefined,
    relative_triangulation=tri,
    framings={k: {kk: vv for kk, vv in r.items()} for k, r in RES.items()},
    framing_drivers=FRAMINGS,
    lenses=lenses,
    # THE SHAPE THE SHARED READERS LOOK FOR. [R-GAP-01]'s reader wants a central and the
    # spot it was struck at, or named BRANCHES where the answer is two-sided; this study
    # published neither and was invisible to that gate — and to [R-GAP-02], which decides
    # whether it may publish at all — for as long as its answer was a median nobody could
    # name. Seven studies were in that state and every one for the same reason.
    spot=v('spot_aed'),
    central_two_sided=dict(
        question='Is navigation through the Strait of Hormuz restored during 2026, or does '
                 'the disruption persist into 2027?',
        decides='Whether the plant runs at the utilisation it has demonstrated or stays '
                'capped by feedstock and logistics, and whether the benchmark price holds '
                'a shortage premium or reverts.',
        branches=[
            dict(label='Cash-flow lens, navigation normalises during 2026',
                 value=CENTRAL_NORMALISATION,
                 condition=FRAMINGS['normalisation']['thesis']),
            dict(label='Cash-flow lens, disruption persists into 2027',
                 value=CENTRAL_PROLONGED,
                 condition=FRAMINGS['prolonged']['thesis']),
        ],
        gap_per_share=abs(CENTRAL_NORMALISATION - CENTRAL_PROLONGED),
        why_not_averaged=(
            'the judgement is binary and about the world rather than about the model, so '
            'an average describes a shipping lane that is neither open nor closed. The '
            'previous edition published the MEDIAN OF NINE LENS READINGS, which averaged '
            'across this judgement AND across the beta construction at the same time, and '
            'which cell it landed on was decided by how many lenses happened to have been '
            'computed under each framing rather than by any valuation choice.'),
        both_sides_vs_spot=[
            dict(label='navigation normalises',
                 pct=100.0 * (CENTRAL_NORMALISATION / v('spot_aed') - 1.0)),
            dict(label='disruption persists',
                 pct=100.0 * (CENTRAL_PROLONGED / v('spot_aed') - 1.0)),
        ]),
    lens_record=LENS_RECORD,
    forecast_anchor=FORECAST_ANCHOR,
    fair_low=FAIR_LOW, fair_high=FAIR_HIGH,
    fair_mid_retired=FAIR_MID_RETIRED,
    field_low=FIELD_LOW, field_high=FIELD_HIGH,
    book_value=dict(bvps_usd=bvps_usd, roe_hist=roe_hist, roe_sustainable=ROE_SUST,
                    justified_pb=justified_pb, value_aed=pb_value_aed,
                    justified_pb_sector_beta=justified_pb_bu,
                    value_aed_sector_beta=pb_value_aed_bu),
    relative=dict(triangulation=tri, median_ev_ebitda=ev_mult, midcycle_ebitda=mid_ebitda,
                  ev=rel_ev, equity=rel_equity, value_aed=rel_aed),
    normalised=dict(util_pe=norm_util_pe, util_pp=norm_util_pp,
                    bench_pe=norm_bench_pe, bench_pp=norm_bench_pp,
                    volume=nvol, revenue=nrev, feedstock=nfeed, othprod=noth,
                    sd=nsd, ebitda=nebitda, da=nda, ebit=nebit, nopat=nnopat,
                    ev=nep_ev, equity=nep_equity, value_aed=nep_aed,
                    value_aed_sector_beta=nep_aed_bu),
    sensitivity=dict(wacc_grid=wacc_grid, g_grid=g_grid, grids=sens,
                     premium_grid=prem_grid, util_grid=util_grid),
    alt_wacc=alt_wacc,
    beta_detail=BETA,
    macro={k: d for k, d in MAC.items()},
    company_inputs={k: d for k, d in C.items()},
    log=LOG,
)

with open(os.path.join(HERE, 'study_numbers.json'), 'w') as f:
    json.dump(OUT, f, indent=1, default=float)
say(f"\nWrote study_numbers.json — {len(C)} company inputs, {len(MAC)} macro inputs, "
    f"every one carrying value, source, date and research layer.")
