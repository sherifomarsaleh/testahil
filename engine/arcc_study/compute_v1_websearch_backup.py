"""ARCC (Arabian Cement Company S.A.E., EGX: ARCC) — master computation.

Emits study_numbers.json, the single source of truth every builder reads. No numeral is
typed into a builder script; no financial arithmetic happens outside this file.

Structure, enforced:
  INPUTS  — every hardcoded figure is a four-field dict {value, source, date, ring}.
            A bare numeral in the inputs block fails the build.
  CALC    — the unit build, the cost of capital, the cash-flow waterfall, the terminal
            block, the four lenses, the sensitivity surfaces and the statements.
  ASSERT  — the build raises, and writes nothing, unless the enterprise-to-equity bridge
            closes exactly, terminal value as a share of enterprise value is computed and
            printed, the implied fair value sits inside a stated plausibility band, and
            net cash and minority interests carry the right signs into the bridge.

The operating line is built BOTTOM-UP from physical quantities: kiln utilisation, a
clinker factor, an alternative-fuel substitution rate, specific thermal and electrical
energy, and a per-tonne cost stack. EBITDA is an OUTPUT of that stack, not an assumed
margin, and the FY2025 reconstruction is asserted against the DISCLOSED operating profit.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import numpy as np

LOG = []
def say(s):
    LOG.append(s); print(s)


def I(value, source, date, ring):
    return dict(value=value, source=source, date=date, ring=ring)


EGX = ("EGX filing reported by Mubasher Info, Arab Finance, Zawya and cemnet/International "
       "Cement Review")
SP = ("Balance-sheet and income-statement data from S&P Global Market Intelligence as "
      "carried by independent aggregations (stockanalysis.com, simplywall.st, "
      "investing.com), cross-read against each other")

# ============================== INPUTS ======================================
INP = dict(
    # ---- anchors ---------------------------------------------------------
    spot=I(59.00, "Closing price 06-Aug-2026 from the supplied EGX daily series (open "
           "58.40, high 59.90, low 58.25, volume 1.34mn)", "2026-08-06", "Market"),
    shares_mn=I(374.87, "374.87mn shares in issue. Corroborated THREE ways and the "
                "corroboration is unusually clean: the FY2024 distribution of EGP 1.10bn "
                "at EGP 2.94 per share implies 374.15mn; the FY2025 distribution of EGP "
                "2.00bn at EGP 5.34 per share implies 374.53mn; and the quoted share "
                "count is 374.87mn. All three agree to within 0.2%",
                "2026-08-06", "Company"),
    tax_stat=I(0.225, "Egypt statutory corporate income tax rate", "2026-01-01", "Country"),

    # ---- disclosed history (EGP mn) --------------------------------------
    rev_fy23=I(6040.0, EGX + " — FY2023 net sales, up from EGP 4.67bn in FY2022",
               "2025-03-01", "Company"),
    rev_fy24=I(8729.0, EGX + " — FY2024 net sales", "2026-03-01", "Company"),
    rev_fy25=I(12447.0, EGX + " — FY2025 net sales, +42.58%", "2026-03-01", "Company"),
    pat_fy23=I(697.49, EGX + " — FY2023 attributable profit, up from EGP 358.98mn in "
               "FY2022", "2025-03-01", "Company"),
    pat_fy24=I(1160.0, EGX + " — FY2024 attributable profit", "2026-03-01", "Company"),
    pat_fy25=I(3599.0, EGX + " — FY2025 attributable profit, +210.3%",
               "2026-03-01", "Company"),
    eps_fy24=I(3.02, EGX + " — FY2024 disclosed earnings per share", "2026-03-01", "Company"),
    eps_fy25=I(9.49, EGX + " — FY2025 disclosed earnings per share", "2026-03-01", "Company"),
    ebit_fy25=I(4595.82, SP + " — FY2025 operating income. This is the disclosed anchor "
                "the bottom-up cost stack is calibrated to reproduce", "2026-03-01",
                "Company"),
    rev_q4_25=I(3645.60, SP + " — fourth-quarter 2025 net sales", "2026-03-01", "Company"),
    ebitda_q4_25=I(1393.01, SP + " — fourth-quarter 2025 EBITDA. One of the three legs of "
                   "the depreciation triangulation", "2026-03-01", "Company"),
    gross_margin=I(0.4077, SP + " — trailing gross margin. Used to derive cost of sales "
                   "and, through it, the inventory leg of the property estimate",
                   "2026-03-01", "Company"),
    rev_q1_26=I(2995.0, EGX + " — first-quarter 2026 net sales, from EGP 2.554bn",
                "2026-05-12", "Company"),
    pat_q1_26=I(943.068, EGX + " — first-quarter 2026 attributable profit, from EGP "
                "590.347mn, +59.74%", "2026-05-12", "Company"),
    rev_q1_25=I(2554.0, EGX + " — first-quarter 2025 net sales", "2025-05-12", "Company"),
    dps_fy24=I(2.94, EGX + " — FY2024 dividend per share, EGP 1.10bn in total",
               "2025-04-01", "Company"),
    dps_fy25=I(5.34, EGX + " — FY2025 dividend per share, EGP 2.00bn in total",
               "2026-04-01", "Company"),
    div_fy24_total=I(1100.0, EGX + " — FY2024 total cash distribution", "2025-04-01",
                     "Company"),
    div_fy25_total=I(2000.0, EGX + " — FY2025 total cash distribution", "2026-04-01",
                     "Company"),

    # ---- balance sheet (EGP mn) ------------------------------------------
    ta_fy25=I(8783.72, SP + " — total assets on the latest reported balance sheet",
              "2026-03-01", "Company"),
    cash_fy25=I(3459.39, SP + " — cash and equivalents", "2026-03-01", "Company"),
    debt_fy25=I(1035.19, SP + " — total interest-bearing debt. The company is NET CASH by "
                "roughly EGP 2.42bn", "2026-03-01", "Company"),
    eq_fy25_rep=I(4642.73, SP + " — total equity as reported. A separate aggregation "
                  "prints total liabilities of EGP 2,894.13mn, which does NOT close "
                  "against this total-asset and equity pair; liabilities are therefore "
                  "DERIVED on the sheet as assets less equity and the disagreement is "
                  "disclosed rather than averaged away", "2026-03-01", "Company"),
    tl_alt=I(2894.13, SP + " — the alternative total-liabilities print. Carried only so "
             "the reader can see the size of the disagreement", "2026-03-01", "Company"),
    nci=I(150.0, "Non-controlling interests deducted in the enterprise-to-equity bridge. "
          "No minority-interest balance is separately retrievable. The size is inferred "
          "from the profit statements: disclosed FY2025 earnings per share of EGP 9.49 on "
          "374.87mn shares gives EGP 3,557mn against a stated attributable profit of EGP "
          "3,599mn, a gap of about 1.2% which is consistent with the statutory employees' "
          "and directors' profit share rather than with a large minority. Set at a "
          "deliberately non-trivial EGP 150mn and SENSITISED", "2026-08-06", "House"),

    # ---- plant, volume and price -----------------------------------------
    cap_cement_mt=I(5.00, "Cement capacity. Two production lines in Suez governorate "
                    "producing on average about five million tonnes of first-quality "
                    "clinker and cement a year. Cross-check: the same disclosure puts the "
                    "plant at about 6% of Egypt's nominal capacity, and 6% of 76Mt is "
                    "4.6Mt, so the nameplate is corroborated to within 9% by an "
                    "independent route", "2026-01-01", "Company"),
    cap_clinker_mt=I(3.60, "Kiln clinker capacity. The PAIR with cement capacity OBSERVES "
                     "the clinker factor rather than assuming it", "2026-01-01", "Company"),
    clinker_factor=I(0.7200, "Tonnes of clinker per tonne of cement. Anchored on the "
                     "capacity pair (3.60/5.00 = 0.720) but carried as an INDEPENDENT "
                     "lever, because blending is a real operating decision: a lower factor "
                     "means more cement per tonne of clinker and less fuel per tonne of "
                     "cement. This company is pursuing exactly that, through supplementary "
                     "cementitious materials, calcined clay and a 50%-slag CEM III product",
                     "2026-01-01", "Company"),
    kiln_util=I([0.7200, 0.7680, 0.7900, 0.8050, 0.8150, 0.8220],
                "Kiln utilisation, FY2025A then FY2026E-FY2030E. The FY2026 step is the "
                "first full year without the production quota abolished in May 2025, and "
                "is corroborated by first-quarter 2026 revenue growth of 17.3% against a "
                "roughly flat price. The path then flattens as 12.6Mt of dormant national "
                "capacity restarts", "2026-08-06", "House"),
    domestic_share=I([0.880, 0.880, 0.870, 0.860, 0.850, 0.840],
                     "Domestic share of despatches. Drifts down as export capacity "
                     "competes for the same tonnes, within the 30% statutory export cap",
                     "2026-01-01", "Industry"),
    price_dom_egp_t=I([3512.24, 3600.00, 3780.00, 3950.00, 4128.00, 4293.00],
                      "Domestic realised price ex-works. The FY2025 figure is the level "
                      "the DISCLOSED revenue implies given the volume build and the export "
                      "split — it is a reconciliation, not an assumption. FY2026 is set at "
                      "the EGP 3,600/t level the industry expects for 2026, and the path "
                      "then grows at 4.0-5.0% a year, DELIBERATELY BELOW the assumed cost "
                      "inflation, because the same decision that freed volume also removed "
                      "the mechanism supporting price", "2026-01-15", "Industry"),
    price_exp_usd_t=I([62.0, 60.0, 58.5, 57.5, 56.5, 55.5],
                      "Export price free on board, US dollars per tonne. Declining because "
                      "the EU carbon border mechanism raises the landed cost of Egyptian "
                      "cement in Europe; the decline is set shallower than a high-clinker "
                      "peer would face, because this producer's alternative-fuel and "
                      "low-clinker position is worth an estimated EUR 5.4/t of relief",
                      "2026-01-01", "Industry"),

    # ---- the cost stack ---------------------------------------------------
    thermal_gj_t_clinker=I(3.30, "Specific thermal energy. Industry band 3.2-3.6 GJ per "
                           "tonne of clinker for a dry preheater/precalciner kiln; set at "
                           "the efficient end for a 2010-vintage plant", "2026-08-06",
                           "Industry"),
    af_share=I([0.520, 0.550, 0.580, 0.600, 0.620, 0.640],
               "Alternative-fuel substitution rate — the share of the thermal requirement "
               "met by refuse-derived fuel and biomass rather than petcoke or coal. This "
               "is the single most company-specific line in the model: the producer is "
               "Egypt's alternative-fuel leader and is targeting a 120,000-tonne annual "
               "emissions reduction through it", "2026-01-01", "Company"),
    fuel_fossil_usd_gj=I(4.00, "Delivered solid fossil fuel, petcoke or coal at roughly "
                         "USD 128/t and about 32 GJ/t", "2026-08-06", "Industry"),
    fuel_alt_usd_gj=I(1.80, "Delivered alternative fuel. Refuse-derived fuel and biomass "
                      "cost materially less per gigajoule than imported petcoke, which is "
                      "the entire economic point of the substitution programme; set at 45% "
                      "of the fossil price", "2026-08-06", "Industry"),
    power_kwh_t_cement=I(100.0, "Specific electrical energy. Industry band 90-110 kWh per "
                         "tonne of cement", "2026-08-06", "Industry"),
    power_tariff=I(2.60, "Egyptian industrial electricity tariff, EGP per kWh, after "
                   "phased subsidy reform", "2026-08-06", "Country"),
    rawmat_egp_t=I(195.0, "Quarrying, raw meal and additives per tonne of cement",
                   "2026-08-06", "Industry"),
    packaging_egp_t=I(55.0, "Bag cost per tonne of bagged cement", "2026-08-06", "Industry"),
    bagged_share=I(0.70, "Bagged share of Egyptian despatches", "2026-08-06", "Industry"),
    distribution_egp_t=I(190.0, "Outbound freight and selling per tonne. Set BELOW a "
                         "typical Egyptian plant because the works sits on the Suez "
                         "corridor, close both to the Cairo demand centre and to the port "
                         "used for exports", "2026-08-06", "House"),
    fixed_usd_t_capacity=I(15.7583, "Fixed cash cost per tonne of INSTALLED capacity, so "
                           "it does not vanish when volume falls. Industry band USD 10-20. "
                           "This is the level the FY2025 reconciliation implies against an "
                           "independently built variable stack — reported as a calibration, "
                           "not solved away and presented as an observation",
                           "2026-08-06", "House"),

    # ---- currency and inflation -------------------------------------------
    fx=I(50.30, "USD/EGP at the valuation date", "2026-08-06", "Country"),
    fx_path=I([49.30, 50.60, 53.10, 55.80, 58.60, 61.50],
              "USD/EGP path, FY2025 average then FY2026E-FY2030E. Raises the pound cost of "
              "imported fuel AND the pound value of export revenue; the two legs partly "
              "offset, which is why this is one driver and not two", "2026-08-06", "House"),
    cost_infl=I([1.000, 1.115, 1.226, 1.336, 1.443, 1.544],
                "Cumulative local cost-inflation index on the pound-denominated cost "
                "lines, from the FY2025 base. Steps of 11.5%, 10.0%, 9.0%, 8.0% and 7.0% "
                "track the disinflation path the central bank's own reporting describes",
                "2026-07-10", "Country"),

    # ---- capital intensity -------------------------------------------------
    dna_peer_egp_t=I(155.0, "Peer depreciation per tonne of despatch — the disclosed "
                     "FY2025 charge of a listed Egyptian cement comparator over its "
                     "despatched volume. The second leg of the depreciation triangulation",
                     "2026-08-06", "Industry"),
    inv_days=I(60.0, "Inventory days on cost of sales, used only to size the property base "
               "in the third leg of the depreciation triangulation", "2026-08-06", "House"),
    recv_days=I(30.0, "Receivable days on revenue, used only to size the property base in "
                "the third leg of the depreciation triangulation", "2026-08-06", "House"),
    dep_rate=I(0.060, "Composite depreciation rate on the net property base. The third leg "
               "of the triangulation", "2026-08-06", "House"),
    dna_pct=I([0.025, 0.028, 0.031, 0.034, 0.036],
              "Depreciation as a share of revenue across the forecast. RISING, because "
              "capital spent from here is incurred at today's replacement cost and adds a "
              "far larger depreciable base per tonne than the legacy pre-devaluation book "
              "carries", "2026-08-06", "House"),
    capex_usd_t_cap=I(4.00, "Maintenance capital expenditure in US dollars per tonne of "
                      "installed capacity. Set at the ECONOMIC level rather than at book "
                      "depreciation: a historic-cost asset base in a currency that has "
                      "devalued several times understates what it actually costs to keep a "
                      "plant running, and charging book depreciation as capex would "
                      "flatter free cash flow by construction. This is deliberately "
                      "conservative", "2026-08-06", "Industry"),
    wc_pct_drev=I(0.12, "Change in working capital over change in revenue",
                  "2026-08-06", "House"),
    payout=I(0.56, "Dividend payout ratio from FY2026E, held at the FY2025 outturn of "
             "EGP 2.00bn on EGP 3.599bn of attributable profit", "2026-08-06", "House"),
    cash_yield=I([0.185, 0.160, 0.145, 0.135, 0.130], "Yield earned on the cash balance "
                 "across the forecast, easing with the policy rate", "2026-08-06", "House"),
    cash_yield_fy25=I(0.210, "Yield earned on cash through FY2025, against a policy rate "
                      "held at 19.50% and bank deposit rates above it", "2026-08-06",
                      "House"),

    # ---- cost of capital ---------------------------------------------------
    rf=I(0.2231, "Egypt 10-year local-currency government bond yield", "2026-07-21",
         "Country"),
    sov_spread_cds=I(0.0340, "Egypt CDS-implied sovereign default spread, Damodaran "
                     "January-2026 country risk file, CDS column. NETTED OUT of the local "
                     "risk-free rate so that sovereign default risk is charged once and "
                     "not twice", "2026-01-05", "Country"),
    erp_cds=I(0.0941, "Egypt equity risk premium, CDS-based, Damodaran January-2026: "
              "mature-market 4.23% plus 3.40% scaled by the relative equity/bond "
              "volatility ratio", "2026-01-05", "Country"),
    kd=I(0.2150, "Marginal pre-tax cost of debt. The central bank's main operation rate is "
         "19.50% and Egyptian corporate borrowing prices above it; 21.5% is the level a "
         "well-banked industrial pays. See the cost-of-debt integrity section: the company "
         "is NET CASH and gross debt is 4.5% of the capital base, so a 700 basis point "
         "error in this input moves the blended rate by about 31 basis points",
         "2026-08-06", "House"),
    kd_path=I([0.2150, 0.1900, 0.1700, 0.1580, 0.1500],
              "Cost-of-debt path across the forecast. The discount-rate glide inherits its "
              "SHAPE from this path rather than from a second, independent judgement",
              "2026-08-06", "House"),
    kd_term=I(0.1500, "Terminal cost of debt — the Egyptian long-run corporate borrowing "
              "norm of 14-16%, midpoint", "2026-08-06", "House"),
    rf_term=I(0.1250, "Terminal risk-free rate, NORM-BUILT from the central bank's own "
              "stated medium-term inflation target of 7% plus a standard emerging-market "
              "real-rate convention of about 5.5 percentage points. Deliberately not a "
              "historical average, and never reverse-engineered from a price",
              "2026-08-06", "House"),
    erp_term=I(0.0700, "Terminal equity risk premium, normalised below the currently "
               "elevated level rather than held flat into perpetuity", "2026-08-06",
               "House"),
    wd_term=I(0.2000, "Terminal debt weight. The company is net cash today; the terminal "
              "state assumes a normalised, modestly geared balance sheet", "2026-08-06",
              "House"),
    g_term=I(0.0500, "Terminal growth. The house default for an established emerging-market "
             "industrial once currency turbulence has passed, against a terminal risk-free "
             "rate that already embeds disinflation — so approximately zero in real terms",
             "2026-08-06", "House"),
    stub_years=I(0.583, "Elapsed fraction of FY2026 at the valuation date — seven of "
                 "twelve months. The elapsed part is rolled into the opening cash balance "
                 "and the unearned part is discounted, so the period is counted exactly "
                 "once", "2026-08-06", "House"),

    # ---- lens inputs -------------------------------------------------------
    repl_usd_t=I(130.0, "Replacement cost per annual tonne of cement capacity, USD 120-150 "
                 "band", "2026-08-06", "Industry"),
    ev_t_just=I(95.0, "Justified enterprise value per annual tonne of capacity. Set well "
                "below replacement cost because a market carrying 76Mt of capacity against "
                "54Mt of consumption does not pay replacement cost", "2026-08-06", "House"),
    ev_ebitda_just=I(4.50, "Justified enterprise value to EBITDA on normalised earnings. "
                     "Struck against a thin and internally inconsistent Egyptian peer set "
                     "and disclosed as WEAKLY ANCHORED, which is why the relative lens "
                     "carries a low weight", "2026-08-06", "House"),
    pe_just=I(7.00, "Justified price to earnings on normalised OPERATING earnings, cash "
              "excluded and added back at face", "2026-08-06", "House"),
    norm_mgn=I(0.308, "Mid-cycle EBITDA margin: the midpoint of the FY2024 outturn and the "
               "FY2025 peak, both reconstructed by the same method. It lands close to the "
               "FY2030 forecast margin, which is a check on the forecast rather than a "
               "coincidence", "2026-08-06", "House"),
    norm_rev_haircut=I(0.94, "Haircut to the FY2025 revenue base for the normalised lens. "
                       "Applying a mid-cycle MARGIN to a PEAK revenue base would be half a "
                       "normalisation in the one lens whose purpose is refusing to "
                       "capitalise a peak", "2026-08-06", "House"),

    # ---- history reconstruction -------------------------------------------
    util_fy23=I(0.6600, "FY2023 kiln utilisation under the production quota",
                "2026-08-06", "House"),
    util_fy24=I(0.6840, "FY2024 kiln utilisation under the production quota. The pair with "
                "FY2025 reproduces the DISCLOSED +42.6% revenue step as a +5.3% volume "
                "step on a +35.5% price step, which is the cross-check that the quota "
                "abolition worked mainly through price and not mainly through volume",
                "2026-08-06", "House"),

    # ---- sector and peers --------------------------------------------------
    egy_capacity_mt=I(76.0, "Egyptian nameplate cement capacity", "2025-10-01", "Industry"),
    egy_cons_mt=I(54.0, "Egyptian domestic cement consumption 2025", "2025-10-01", "Industry"),
    egy_prod_mt=I(65.0, "Egyptian cement production 2025", "2026-01-01", "Industry"),
    egy_exports_mt=I(18.5, "Egyptian cement and clinker exports 2025", "2026-01-01",
                     "Industry"),
    egy_revival_mt=I(12.6, "Dormant Egyptian capacity under revival from the second half "
                     "of 2026", "2025-10-01", "Industry"),
    egy_gdp_egp_bn=I(18000.0, "Egyptian nominal gross domestic product, order of magnitude, "
                     "used only for the terminal-growth crossover arithmetic",
                     "2026-01-01", "Country"),
    egy_gdp_growth=I(0.180, "Egyptian nominal GDP growth used in the same crossover "
                     "arithmetic", "2026-01-01", "Country"),
    peer_scem_rev=I(9090.0, "Sinai Cement FY2025 revenue", "2026-03-10", "Industry"),
    peer_scem_pat=I(2290.0, "Sinai Cement FY2025 profit after tax", "2026-03-10", "Industry"),
    peer_scem_mcap=I(20604.19, "Sinai Cement market capitalisation at 06-Aug-2026",
                     "2026-08-06", "Industry"),
    peer_mbsc_rev=I(5700.0, "Misr Beni Suef Cement FY2025 net sales", "2026-03-01",
                    "Industry"),
    peer_mbsc_pat=I(3946.0, "Misr Beni Suef Cement FY2025 attributable profit",
                    "2026-03-01", "Industry"),
    peer_mbsc_mcap=I(13730.0, "Misr Beni Suef Cement market capitalisation",
                     "2026-08-06", "Industry"),

    # ---- lens weights ------------------------------------------------------
    w_dcf=I(0.50, "Weight, cash-flow lens. The highest weight because it is the only lens "
            "that prices the specific thing this company is: a fixed asset with a known "
            "cost stack in a market whose supply is about to expand", "2026-08-06", "House"),
    w_rel=I(0.20, "Weight, relative lens. Held down because the Egyptian peer set is thin "
            "and its published multiples do not reconcile", "2026-08-06", "House"),
    w_norm=I(0.22, "Weight, normalised-earnings lens", "2026-08-06", "House"),
    w_asset=I(0.08, "Weight, asset lens. Deliberately small: restarting a mothballed line "
              "costs a fraction of building one, and 12.6Mt of restart capacity is queuing, "
              "so replacement cost is a ceiling and not a floor", "2026-08-06", "House"),
)

V = {k: v['value'] for k, v in INP.items()}
for k, v in INP.items():
    assert set(v) == {'value', 'source', 'date', 'ring'} and str(v['source']).strip(), k
    assert v['ring'] in ('Market', 'Company', 'Industry', 'Country', 'House'), k
TAX = V['tax_stat']
YRS = ['FY2026E', 'FY2027E', 'FY2028E', 'FY2029E', 'FY2030E']
HIST = ['FY2023', 'FY2024', 'FY2025']

say("=" * 78)
say("ARCC — Arabian Cement Company S.A.E. — master computation")
say("=" * 78)

# ==================== 1. SHARE COUNT TRIANGULATION ==========================
sh_div24 = V['div_fy24_total'] / V['dps_fy24']
sh_div25 = V['div_fy25_total'] / V['dps_fy25']
SHT = dict(from_fy24_distribution=sh_div24, from_fy25_distribution=sh_div25,
           quoted=V['shares_mn'], mean=(sh_div24 + sh_div25 + V['shares_mn']) / 3,
           adopted=V['shares_mn'],
           spread=(max(sh_div24, sh_div25, V['shares_mn']) /
                   min(sh_div24, sh_div25, V['shares_mn']) - 1))
assert SHT['spread'] < 0.005, SHT
SH = V['shares_mn']
MKTCAP = V['spot'] * SH
say(f"\n[Share count] {sh_div24:,.2f}mn from the FY2024 distribution | {sh_div25:,.2f}mn "
    f"from the FY2025 distribution | {V['shares_mn']:,.2f}mn quoted — spread "
    f"{SHT['spread']:.2%}. Adopted {SH:,.2f}mn; market capitalisation EGP {MKTCAP:,.0f}mn")

# ==================== 2. DEPRECIATION TRIANGULATION =========================
cogs_fy25 = V['rev_fy25'] * (1 - V['gross_margin'])
inv_fy25 = cogs_fy25 * V['inv_days'] / 365.0
recv_fy25 = V['rev_fy25'] * V['recv_days'] / 365.0
ppe_est = V['ta_fy25'] - V['cash_fy25'] - inv_fy25 - recv_fy25
dna_m1 = V['ebitda_q4_25'] / V['rev_q4_25'] * V['rev_fy25'] - V['ebit_fy25']
vol_fy25 = V['cap_clinker_mt'] * V['kiln_util'][0] / V['clinker_factor']
dna_m2 = V['dna_peer_egp_t'] * vol_fy25
dna_m3 = ppe_est * V['dep_rate']
DNA25 = (dna_m1 + dna_m2 + dna_m3) / 3.0
DNA_T = DNA25 / vol_fy25
DNAT = dict(m1_q4_margin_closure=dna_m1, m2_peer_per_tonne=dna_m2,
            m3_property_base=dna_m3, adopted=DNA25, per_tonne=DNA_T,
            pct_of_revenue=DNA25 / V['rev_fy25'], ppe_estimate=ppe_est,
            cogs=cogs_fy25, inventory=inv_fy25, receivables=recv_fy25)
say(f"\n[Depreciation — three methods, averaged on the sheet] "
    f"Q4 margin closure {dna_m1:,.1f} | peer per tonne {dna_m2:,.1f} | property base "
    f"{dna_m3:,.1f}  ->  adopted {DNA25:,.1f} ({DNA25/V['rev_fy25']:.2%} of revenue, "
    f"EGP {DNA_T:,.1f}/t). The spread is wide and is disclosed as such.")

# ==================== 3. BOTTOM-UP OPERATING BUILD ==========================
cf = V['clinker_factor']
BU = []
for i in range(6):
    clk = V['cap_clinker_mt'] * V['kiln_util'][i]
    cem = clk / cf
    dom = cem * V['domestic_share'][i]
    exp = cem - dom
    fx, infl, af = V['fx_path'][i], V['cost_infl'][i], V['af_share'][i]
    rev = dom * V['price_dom_egp_t'][i] + exp * V['price_exp_usd_t'][i] * fx
    fuel_usd_gj = af * V['fuel_alt_usd_gj'] + (1 - af) * V['fuel_fossil_usd_gj']
    c_fuel = V['thermal_gj_t_clinker'] * cf * fuel_usd_gj * fx
    c_pow = V['power_kwh_t_cement'] * V['power_tariff'] * infl
    c_raw = V['rawmat_egp_t'] * infl
    c_pack = V['packaging_egp_t'] * V['bagged_share'] * infl
    c_dist = V['distribution_egp_t'] * infl
    var_t = c_fuel + c_pow + c_raw + c_pack + c_dist
    fixed = V['fixed_usd_t_capacity'] * V['cap_cement_mt'] * V['fx_path'][0] * infl
    eb = rev - var_t * cem - fixed
    BU.append(dict(clinker=clk, cement=cem, dom=dom, exp=exp, util=V['kiln_util'][i],
                   af=af, fuel_usd_gj=fuel_usd_gj, rev=rev, price=rev / cem,
                   c_fuel=c_fuel, c_pow=c_pow, c_raw=c_raw, c_pack=c_pack, c_dist=c_dist,
                   var_t=var_t, var=var_t * cem, fixed=fixed, ebitda=eb, mgn=eb / rev))
rev_f = [b['rev'] for b in BU[1:]]
ebitda_f = [b['ebitda'] for b in BU[1:]]
recon_rev = BU[0]['rev'] / V['rev_fy25'] - 1
recon_ebit = (BU[0]['ebitda'] - DNA25) / V['ebit_fy25'] - 1
say(f"\n[Bottom-up FY2025] revenue {BU[0]['rev']:,.0f} vs disclosed {V['rev_fy25']:,.0f} "
    f"({recon_rev:+.3%}); EBITDA {BU[0]['ebitda']:,.0f} (margin {BU[0]['mgn']:.1%}); "
    f"operating profit {BU[0]['ebitda']-DNA25:,.0f} vs DISCLOSED {V['ebit_fy25']:,.0f} "
    f"({recon_ebit:+.3%}) — EBITDA is an OUTPUT of the cost stack")
say(f"[Forecast margins] " + "  ".join(f"{b['mgn']:.1%}" for b in BU[1:]) +
    "  — gliding down from the FY2025 peak on capacity restart and energy reform")

# ==================== 4. HISTORICAL CLOSURE =================================
netfin_fy25 = V['cash_fy25'] * V['cash_yield_fy25'] - V['debt_fy25'] * V['kd']
pbt_fy25 = V['ebit_fy25'] + netfin_fy25
TAXE = 1 - V['pat_fy25'] / pbt_fy25
assert TAX <= TAXE < TAX + 0.12, f"effective tax rate {TAXE:.4f} outside plausible band"
vol_h = [V['cap_clinker_mt'] * u / cf for u in (V['util_fy23'], V['util_fy24'],
                                                V['kiln_util'][0])]
rev_h = [V['rev_fy23'], V['rev_fy24'], V['rev_fy25']]
pat_h = [V['pat_fy23'], V['pat_fy24'], V['pat_fy25']]
dna_h = [DNA_T * v for v in vol_h]
ebit_h = [V['pat_fy23'] / (1 - TAXE), V['pat_fy24'] / (1 - TAXE), V['ebit_fy25']]
ebitda_h = [ebit_h[i] + dna_h[i] for i in range(3)]
price_h = [rev_h[i] / vol_h[i] for i in range(3)]
say(f"\n[FY2025 closure] disclosed operating profit {V['ebit_fy25']:,.0f} plus net finance "
    f"income {netfin_fy25:,.0f} (treasury on EGP {V['cash_fy25']:,.0f} of cash at "
    f"{V['cash_yield_fy25']:.1%} less interest on EGP {V['debt_fy25']:,.0f} of debt at "
    f"{V['kd']:.1%}) gives pre-tax profit {pbt_fy25:,.0f}; against disclosed profit after "
    f"tax {V['pat_fy25']:,.0f} the EFFECTIVE tax rate is {TAXE:.2%}, above the statutory "
    f"{TAX:.1%} — the effective rate is what the model uses")
say(f"[Volume and price history] volumes " +
    " ".join(f"{v:.3f}" for v in vol_h) + " Mt; realised prices " +
    " ".join(f"{p:,.0f}" for p in price_h) + " EGP/t. The disclosed +42.6% FY2025 revenue "
    f"step decomposes as {vol_h[2]/vol_h[1]-1:+.1%} volume on {price_h[2]/price_h[1]-1:+.1%} "
    "price")

# ==================== 5. COST OF CAPITAL ====================================
rf_star = V['rf'] - V['sov_spread_cds']
BETA = json.load(open(os.path.join(HERE, 'beta_result.json')))
beta_used = BETA['adopted']['beta_used']
ke_exp = rf_star + beta_used * V['erp_cds']
kd_at = V['kd'] * (1 - TAX)
net_debt_bs = V['debt_fy25'] - V['cash_fy25']
wd_gross = V['debt_fy25'] / (V['debt_fy25'] + MKTCAP)
wd_net = net_debt_bs / (net_debt_bs + MKTCAP)
wacc_exp = (1 - wd_gross) * ke_exp + wd_gross * kd_at
wacc_exp_netw = (1 - wd_net) * ke_exp + wd_net * kd_at
beta_t = beta_used * (1 + (1 - TAX) * V['wd_term'] / (1 - V['wd_term']))
ke_term = V['rf_term'] + beta_t * V['erp_term']
wacc_term = (1 - V['wd_term']) * ke_term + V['wd_term'] * V['kd_term'] * (1 - TAX)
assert wacc_term < wacc_exp, (wacc_term, wacc_exp)
kdp = V['kd_path']
glide = [(kdp[0] - kdp[i]) / (kdp[0] - kdp[-1]) for i in range(5)]
fwd = [wacc_exp - (wacc_exp - wacc_term) * g for g in glide]
REM = 1.0 - V['stub_years']
t_mid = [REM / 2] + [REM + (k - 0.5) for k in range(1, 5)]


def factors(f_):
    out = []
    for i in range(5):
        yl, fa, j = t_mid[i], 1.0, 0
        while yl > 1e-12 and j < 5:
            st = min(1.0, yl)
            fa *= (1 + f_[j]) ** st
            yl -= st
            j += 1
        out.append(1.0 / fa)
    return out


df_ = factors(fwd)
assert all(0 < d <= 1.0 for d in df_) and all(df_[i] > df_[i + 1] for i in range(4))
say(f"\n[Cost of capital] risk-free {V['rf']:.2%} less sovereign spread "
    f"{V['sov_spread_cds']:.2%} = {rf_star:.2%}; cost of equity {ke_exp:.2%} at beta "
    f"{beta_used:.3f}; after-tax cost of debt {kd_at:.2%} on a {wd_gross:.2%} weight -> "
    f"explicit-window rate {wacc_exp:.2%}")
say(f"[Terminal] beta re-levered {beta_used:.3f} -> {beta_t:.3f}; terminal cost of equity "
    f"{ke_term:.2%}; terminal rate {wacc_term:.2%}. Glide fractions " +
    " ".join(f"{g:.3f}" for g in glide) + " inherited from the cost-of-debt path")
say(f"[Discounting] one price of time per date: the terminal value is capitalised at the "
    f"terminal rate and brought home on the SAME cumulative factor as the year-5 cash "
    f"flow ({df_[-1]:.4f})")

# ==================== 6. DCF WATERFALL ======================================
dna_f = [rev_f[i] * V['dna_pct'][i] for i in range(5)]
ebit_f = [ebitda_f[i] - dna_f[i] for i in range(5)]
nopat = [ebit_f[i] * (1 - TAXE) for i in range(5)]
capex = [V['cap_cement_mt'] * V['capex_usd_t_cap'] * V['fx_path'][i + 1] for i in range(5)]
prev_rev = [V['rev_fy25']] + rev_f[:-1]
dwc = [(rev_f[i] - prev_rev[i]) * V['wc_pct_drev'] for i in range(5)]
ic_repl = V['cap_cement_mt'] * V['repl_usd_t'] * V['fx']
roic_t = nopat[-1] * (1 + V['g_term']) / ic_repl
nopat0 = (ebitda_h[2] - dna_h[2]) * (1 - TAXE)
fcff = [nopat[i] + dna_f[i] - capex[i] - dwc[i] for i in range(5)]
fcff[0] *= REM
pv = [fcff[i] * df_[i] for i in range(5)]
sum_pv = float(np.sum(pv))
rr_t = V['g_term'] / roic_t
tv = nopat[-1] * (1 + V['g_term']) * (1 - rr_t) / (wacc_term - V['g_term'])
pv_tv = tv * df_[-1]
ev = sum_pv + pv_tv
tv_share = pv_tv / ev
cash_at_val = V['cash_fy25'] + fcff[0] / REM * V['stub_years']
net_cash = cash_at_val - V['debt_fy25']
eq_dcf = ev + net_cash - V['nci']
fv_dcf = eq_dcf / SH
say(f"\n[Free cash flow] " + " ".join(f"{x:,.0f}" for x in fcff) +
    f"  (FY2026 carries only the {REM*12:.0f} unearned months)")
say(f"[Bridge] enterprise value {ev:,.0f} = explicit {sum_pv:,.0f} + terminal {pv_tv:,.0f}; "
    f"plus net cash {net_cash:,.0f}, less minorities {V['nci']:,.0f} = equity "
    f"{eq_dcf:,.0f} -> EGP {fv_dcf:.2f} per share")
say(f"[Terminal value] {tv_share:.1%} of enterprise value; terminal return on capital "
    f"{roic_t:.2%} against a terminal rate of {wacc_term:.2%}, so reinvestment is "
    f"{rr_t:.1%} of terminal profit")

# ==================== 7. THE OTHER LENSES ===================================
eb_norm = V['rev_fy25'] * V['norm_rev_haircut'] * V['norm_mgn']
fv_rel = (eb_norm * V['ev_ebitda_just'] + net_cash - V['nci']) / SH
nopat_norm = (eb_norm - DNA25) * (1 - TAXE)
fv_norm = (nopat_norm * V['pe_just'] + net_cash - V['nci']) / SH
ev_spot = MKTCAP - net_cash + V['nci']
ev_per_t = ev_spot / (V['cap_cement_mt'] * V['fx'])
ev_asset = V['ev_t_just'] * V['cap_cement_mt'] * V['fx']
fv_asset = (ev_asset + net_cash - V['nci']) / SH
LENS = {'DCF (cash flow)': fv_dcf, 'Relative multiples': fv_rel,
        'Normalised earnings': fv_norm, 'Asset / replacement cost': fv_asset}
WT = {'DCF (cash flow)': V['w_dcf'], 'Relative multiples': V['w_rel'],
      'Normalised earnings': V['w_norm'], 'Asset / replacement cost': V['w_asset']}
assert abs(sum(WT.values()) - 1.0) < 1e-9
fv_central = float(sum(LENS[k] * WT[k] for k in LENS))
say(f"\n[Lenses] " + " | ".join(f"{k.split()[0]} {v:.2f}" for k, v in LENS.items()))
say(f"[Central] EGP {fv_central:.2f} against a market price of EGP {V['spot']:.2f} "
    f"({fv_central/V['spot']-1:+.1%}); the market is paying USD {ev_per_t:.1f} per annual "
    f"tonne against a replacement cost of USD {V['repl_usd_t']:.0f}")

# ==================== 8. SENSITIVITY ========================================
def reval(nc=None, g=None, we=None, beta_=None, mgn_shift=0.0, capex_mult=1.0,
          dna_shift=0.0, nci=None):
    nc = net_cash if nc is None else nc
    g = V['g_term'] if g is None else g
    nci_ = V['nci'] if nci is None else nci
    we = wacc_exp if we is None else we
    if beta_ is not None:
        we = (1 - wd_gross) * (rf_star + beta_ * V['erp_cds']) + wd_gross * kd_at
        bt = beta_ * (1 + (1 - TAX) * V['wd_term'] / (1 - V['wd_term']))
        wt = (1 - V['wd_term']) * (V['rf_term'] + bt * V['erp_term']) + \
            V['wd_term'] * V['kd_term'] * (1 - TAX)
    else:
        wt = wacc_term
    f_ = [we - (we - wt) * gg for gg in glide]
    d_ = factors(f_)
    eb = [ebitda_f[i] + rev_f[i] * mgn_shift for i in range(5)]
    dn = [dna_f[i] + rev_f[i] * dna_shift for i in range(5)]
    ei = [eb[i] - dn[i] for i in range(5)]
    np_ = [ei[i] * (1 - TAXE) for i in range(5)]
    cx = [c * capex_mult for c in capex]
    fc = [np_[i] + dn[i] - cx[i] - dwc[i] for i in range(5)]
    fc[0] *= REM
    s = float(np.sum([fc[i] * d_[i] for i in range(5)]))
    rt = np_[-1] * (1 + g) / ic_repl
    tvl = np_[-1] * (1 + g) * (1 - g / rt) / (wt - g)
    return (s + tvl * d_[-1] + nc - nci_) / SH


nc_grid = [net_cash - 1500, net_cash - 750, net_cash, net_cash + 750, net_cash + 1500]
wacc_grid = [wacc_exp - 0.03, wacc_exp - 0.015, wacc_exp, wacc_exp + 0.015, wacc_exp + 0.03]
g_grid = [0.03, 0.04, 0.05, 0.06, 0.07]
beta_grid = [0.6, 0.8, 1.0, 1.15, 1.3]
mgn_grid = [-0.04, -0.02, 0.0, 0.02, 0.04]
SENS = dict(
    nc_grid=nc_grid, net_cash=[reval(nc=x) for x in nc_grid],
    wacc_grid=wacc_grid, g_grid=g_grid,
    wacc_g=[[reval(we=x, g=gg) for gg in g_grid] for x in wacc_grid],
    beta_grid=beta_grid, beta=[reval(beta_=b) for b in beta_grid],
    mgn_grid=mgn_grid, mgn=[reval(mgn_shift=m) for m in mgn_grid],
    wt_grid=[wacc_term - 0.02, wacc_term - 0.01, wacc_term, wacc_term + 0.01,
             wacc_term + 0.02],
)
def reval_two_anchor(we, wt):
    """Explicit-window rate and terminal rate varied INDEPENDENTLY around their own bases."""
    d_ = factors([we - (we - wt) * gg for gg in glide])
    s = float(np.sum([fcff[i] * d_[i] for i in range(5)]))
    tvl = nopat[-1] * (1 + V['g_term']) * (1 - rr_t) / (wt - V['g_term'])
    return (s + tvl * d_[-1] + net_cash - V['nci']) / SH


SENS['exp_term'] = [[reval_two_anchor(x, y) for y in SENS['wt_grid']] for x in wacc_grid]
say(f"\n[Sensitivity] fair value across the explicit-window rate and terminal growth "
    f"spans EGP {min(min(r) for r in SENS['wacc_g']):.2f} to "
    f"{max(max(r) for r in SENS['wacc_g']):.2f}")

# ==================== 9. CONTESTED CHOICES, COMPUTED ========================
fv_beta_dimson = reval(beta_=BETA['dimson']['sum_beta'])
fv_netw = reval(we=wacc_exp_netw)
fv_nci0 = reval(nci=0.0)
fv_capex_bookdep = reval(capex_mult=float(np.mean(dna_f)) / float(np.mean(capex)))
CONTESTED = [
    dict(choice='Beta: contemporaneous regression (adopted) vs Dimson lead-lag sum-beta',
         adopted=f"{beta_used:.3f}", alternative=f"{BETA['dimson']['sum_beta']:.3f}",
         fv_adopted=fv_dcf, fv_alternative=fv_beta_dimson,
         effect=fv_beta_dimson / fv_dcf - 1,
         note=('The regression passes the usability gate, so it is adopted. It is also '
               'statistically weak, and the standard correction for a thinly traded share '
               'is the lead-lag sum-beta, which is higher. The alternative is therefore '
               'computed as a VALUE rather than described.')),
    dict(choice='Capital-structure weights: gross debt (adopted) vs net debt',
         adopted=f"{wd_gross:.2%}", alternative=f"{wd_net:.2%}",
         fv_adopted=fv_dcf, fv_alternative=fv_netw, effect=fv_netw / fv_dcf - 1,
         note=('Net debt is negative, so a net-debt weight makes the blended rate exceed '
               'the cost of equity — which prices the treasury, not the plant. Cash is '
               'stripped to the bridge instead, so the discount rate belongs to the '
               'operating assets and the weights use gross debt.')),
    dict(choice='Minority interests: EGP 150mn deducted (adopted) vs none',
         adopted='150', alternative='0', fv_adopted=fv_dcf, fv_alternative=fv_nci0,
         effect=fv_nci0 / fv_dcf - 1,
         note=('No minority balance is separately retrievable. A deliberately non-trivial '
               'figure is deducted rather than omitted, and the cost of the choice is '
               'shown.')),
    dict(choice='Capex: economic maintenance in dollars per tonne (adopted) vs book '
                'depreciation',
         adopted=f"USD {V['capex_usd_t_cap']:.2f}/t",
         alternative='book depreciation', fv_adopted=fv_dcf,
         fv_alternative=fv_capex_bookdep, effect=fv_capex_bookdep / fv_dcf - 1,
         note=('Setting capex equal to book depreciation would flatter free cash flow by '
               'construction, because the book base is pre-devaluation historic cost. The '
               'adopted treatment is the conservative one and the size of the conservatism '
               'is published.')),
]
say("\n[Contested choices, each computed rather than argued]")
for c in CONTESTED:
    say(f"  {c['choice']}: {c['fv_adopted']:.2f} -> {c['fv_alternative']:.2f} "
        f"({c['effect']:+.1%})")

# ==================== 10. TERMINAL-GROWTH RECONCILIATION ====================
nopat_h = [(ebitda_h[i] - dna_h[i]) * (1 - TAXE) for i in range(3)]
nopat_cagr = (nopat_h[2] / nopat_h[0]) ** (1 / 2) - 1
pat_cagr_4y = (V['pat_fy25'] / 358.98) ** (1 / 3) - 1
share_gdp = V['rev_fy25'] / (V['egy_gdp_egp_bn'] * 1000.0)
cross_yrs = float(np.log(1 / share_gdp) /
                  np.log((1 + pat_cagr_4y) / (1 + V['egy_gdp_growth'])))
TR = dict(
    history=[dict(year=HIST[i], revenue=rev_h[i], ebitda=ebitda_h[i], dna=dna_h[i],
                  nopat=nopat_h[i], volume=vol_h[i], price=price_h[i],
                  margin=ebitda_h[i] / rev_h[i],
                  character='quota-constrained' if i < 2 else 'post-quota price spike')
             for i in range(3)],
    nopat_cagr=nopat_cagr, pat_cagr_since_fy22=pat_cagr_4y,
    roic_repl=roic_t, rr_repl=rr_t, ic_repl=ic_repl,
    basis_adopted='replacement cost',
    capex_history_available=False,
    capex_note=('No capital-expenditure history is retrievable for this company from any '
                'source at the evidentiary standard used elsewhere in this study, so the '
                'reinvestment-character column of the reconciliation cannot be filled from '
                'disclosure. It is left empty rather than estimated, and the terminal '
                'return on capital is anchored on replacement cost instead — the more '
                'conservative of the two available anchors, because a historic-cost book '
                'base would flatter it.'),
    crossover_years=cross_yrs, share_of_gdp=share_gdp,
    g_ceiling_note=('Recent profit growth cannot be a terminal rate. Compounding the '
                    f'{pat_cagr_4y:.0%} profit growth achieved since FY2022 against '
                    f'{V["egy_gdp_growth"]:.0%} nominal economic growth, this company '
                    f'would equal the entire Egyptian economy in about {cross_yrs:.0f} '
                    'years. That is arithmetic, not a modelling opinion, and it is the '
                    'strongest single disqualifier for an inflated terminal rate.'),
)
say(f"\n[Terminal growth] recent profit growth of {pat_cagr_4y:.0%} a year would put this "
    f"company at the size of the whole Egyptian economy in {cross_yrs:.0f} years. Terminal "
    f"growth is held at {V['g_term']:.0%} and sensitised 3-7%")
GDV = dict(fv_at_g3=reval(g=0.03), fv_at_g7=reval(g=0.07), roic_term=roic_t,
           wacc_term=wacc_term)
GDV['holds'] = bool(GDV['fv_at_g7'] < GDV['fv_at_g3'])
say(f"[Growth destroys value] terminal return on capital {roic_t:.1%} sits BELOW the "
    f"terminal rate {wacc_term:.1%}, so faster terminal growth LOWERS the valuation: "
    f"EGP {GDV['fv_at_g3']:.2f} at 3% against {GDV['fv_at_g7']:.2f} at 7%. "
    f"{'Confirmed' if GDV['holds'] else 'NOT confirmed'}")

# ==================== 11. STATEMENTS ========================================
pbt_f, tax_f, pat_f, cash_b, eq_b, ppe_b, wc_b, div_f, treas_f, ta_b = ([] for _ in range(10))
c_, e_ = V['cash_fy25'], V['eq_fy25_rep']
p_, wc_ = ppe_est, inv_fy25 + recv_fy25
for i in range(5):
    ti = c_ * V['cash_yield'][i] - V['debt_fy25'] * kdp[i]
    pbt = ebit_f[i] + ti
    tx = pbt * TAXE
    pat = pbt - tx
    dv = pat * V['payout']
    p_ += capex[i] - dna_f[i]
    wc_ += dwc[i]
    c_ += pat + dna_f[i] - capex[i] - dwc[i] - dv
    e_ += pat - dv
    for L, x in ((treas_f, ti), (pbt_f, pbt), (tax_f, tx), (pat_f, pat), (div_f, dv),
                 (cash_b, c_), (eq_b, e_), (ppe_b, p_), (wc_b, wc_),
                 (ta_b, c_ + p_ + wc_)):
        L.append(x)
eq_gap = dict(rolled=V['ta_fy25'] - V['tl_alt'], reported=V['eq_fy25_rep'],
              gap=V['ta_fy25'] - V['tl_alt'] - V['eq_fy25_rep'],
              derived_liabilities=V['ta_fy25'] - V['eq_fy25_rep'], alt_liabilities=V['tl_alt'])
say(f"\n[Balance-sheet disagreement, disclosed not smoothed] total assets "
    f"{V['ta_fy25']:,.0f} less reported equity {V['eq_fy25_rep']:,.0f} gives derived "
    f"liabilities {eq_gap['derived_liabilities']:,.0f}; a separate aggregation prints "
    f"{V['tl_alt']:,.0f}, a gap of {eq_gap['gap']:,.0f}. The DERIVED figure is carried")

# ==================== 12. EXPERT PANEL ======================================
fcff_mid = float(np.mean(fcff[1:]))
e3 = (fcff_mid / 0.175 + net_cash - V['nci']) / SH
EXPERTS = [
    dict(label='Expert 1', method='Replacement-cost industrialist', central=fv_asset,
         low=((V['ev_t_just'] - 15) * V['cap_cement_mt'] * V['fx'] + net_cash - V['nci']) / SH,
         high=((V['ev_t_just'] + 15) * V['cap_cement_mt'] * V['fx'] + net_cash - V['nci']) / SH,
         summary=('Values the plant, not the earnings stream. Five million tonnes of grey '
                  'cement capacity costs about USD %.0f per annual tonne to build. Nobody '
                  'pays replacement cost for capacity in a market carrying %.0fMt of it '
                  'against %.0fMt of consumption, so the justified figure is marked down '
                  'to USD %.0f. Against that, the market is paying USD %.0f per annual '
                  'tonne — the plant is on sale relative to the cost of putting one there, '
                  'which is the whole of this case.'
                  % (V['repl_usd_t'], V['egy_capacity_mt'], V['egy_cons_mt'],
                     V['ev_t_just'], ev_per_t)),
         falsifier=('Find an Egyptian line built, bought or restarted below USD %.0f per '
                    'annual tonne. The 12.6Mt revival programme is the live test and it '
                    'runs against this lens: restarting a mothballed kiln costs a fraction '
                    'of building one, which is exactly why this valuation is a ceiling and '
                    'not a floor, and why it carries only %.0f%% of the weight.'
                    % (V['ev_t_just'], V['w_asset'] * 100))),
    dict(label='Expert 2', method='Mid-cycle earnings-power analyst', central=fv_norm,
         low=(nopat_norm * (V['pe_just'] - 1) + net_cash - V['nci']) / SH,
         high=(nopat_norm * (V['pe_just'] + 1) + net_cash - V['nci']) / SH,
         summary=('Refuses to capitalise a peak, and refuses it on BOTH legs. FY2025 was '
                  'the best year the Egyptian cement industry has had in over a decade: '
                  'the margin is normalised to %.1f%% against the %.1f%% actually earned, '
                  'and the revenue base is cut %.0f%% because that revenue embeds the '
                  'post-quota price spike. What is left is capitalised at %.0f times, with '
                  'the cash added back at face rather than capitalised at the same '
                  'multiple as the operating business — cash is worth cash.'
                  % (V['norm_mgn'] * 100, BU[0]['mgn'] * 100,
                     (1 - V['norm_rev_haircut']) * 100, V['pe_just'])),
         falsifier=('Two consecutive years of realised prices above EGP 4,200 per tonne '
                    'WITH the 12.6Mt revival actually proceeding would prove the mid-cycle '
                    'base too low. Equally, a single year in which the alternative-fuel '
                    'programme stalls and the fuel bill reverts to a fossil-only stack '
                    'would prove it too high.')),
    dict(label='Expert 3', method='Cash-return and distribution investor', central=e3,
         low=(fcff_mid / 0.20 + net_cash - V['nci']) / SH,
         high=(fcff_mid / 0.15 + net_cash - V['nci']) / SH,
         summary=('Ignores the terminal value entirely and asks what the cash stream is '
                  'worth to someone who has to be paid in cash. Average free cash flow to '
                  'the firm across FY2027-FY2030 is EGP %.0fmn; required at a 17.5%% cash '
                  'return — the level a pound-denominated investor can obtain from '
                  'government paper once disinflation is priced — that is a business worth '
                  'EGP %.0fmn before the net cash of EGP %.0fmn is added back. The company '
                  'already distributes %.0f%% of profit, so this is not a hypothetical '
                  'claim on retained value.'
                  % (fcff_mid, fcff_mid / 0.175, net_cash, V['payout'] * 100)),
         falsifier=('A required cash return above 20%% — which is what a failure of the '
                    'disinflation path would produce — takes this valuation to EGP %.2f '
                    'and below the market price. So would any year in which maintenance '
                    'capital spending has to rise materially above the USD %.2f per tonne '
                    'of capacity assumed here, which is the number to watch in the cash '
                    'flow statement rather than in the earnings release.'
                    % ((fcff_mid / 0.20 + net_cash - V['nci']) / SH, V['capex_usd_t_cap']))),
]

LR = {}
for k, v in LENS.items():
    LR[k] = dict(bear=v * 0.90, base=v, bull=v * 1.10)
LR['DCF (cash flow)'] = dict(bear=reval(mgn_shift=-0.02, we=wacc_exp + 0.015), base=fv_dcf,
                             bull=reval(mgn_shift=0.02, we=wacc_exp - 0.015))
LR['Weighted central'] = dict(
    bear=float(sum(LR[k]['bear'] * WT[k] for k in WT)), base=fv_central,
    bull=float(sum(LR[k]['bull'] * WT[k] for k in WT)))

# ==================== 13. PEERS =============================================
PEERS = dict(
    scem=dict(name='Sinai Cement (SCEM)', rev=V['peer_scem_rev'], pat=V['peer_scem_pat'],
              mcap=V['peer_scem_mcap'], pe=V['peer_scem_mcap'] / V['peer_scem_pat'],
              ps=V['peer_scem_mcap'] / V['peer_scem_rev']),
    mbsc=dict(name='Misr Beni Suef Cement (MBSC)', rev=V['peer_mbsc_rev'],
              pat=V['peer_mbsc_pat'], mcap=V['peer_mbsc_mcap'],
              pe=V['peer_mbsc_mcap'] / V['peer_mbsc_pat'],
              ps=V['peer_mbsc_mcap'] / V['peer_mbsc_rev']),
    self=dict(name='Arabian Cement (ARCC)', rev=V['rev_fy25'], pat=V['pat_fy25'],
              mcap=MKTCAP, pe=MKTCAP / V['pat_fy25'], ps=MKTCAP / V['rev_fy25']),
    sector=dict(capacity_mt=V['egy_capacity_mt'], consumption_mt=V['egy_cons_mt'],
                production_mt=V['egy_prod_mt'], exports_mt=V['egy_exports_mt'],
                revival_mt=V['egy_revival_mt'],
                share_of_capacity=V['cap_cement_mt'] / V['egy_capacity_mt'],
                revival_pct_of_consumption=V['egy_revival_mt'] / V['egy_cons_mt'],
                utilisation=V['egy_prod_mt'] / V['egy_capacity_mt']),
)

# ==================== ASSERT ================================================
A = []
def chk(cond, msg):
    assert cond, 'ASSERT FAILED: ' + msg
    A.append(msg)


chk(abs((ev + net_cash - V['nci']) - eq_dcf) < 1e-6,
    f"bridge closes exactly: EV {ev:,.2f} + net cash {net_cash:,.2f} - NCI {V['nci']:,.2f} "
    f"= equity {eq_dcf:,.2f}")
chk(net_cash > 0, f"net cash carries a POSITIVE sign into the bridge ({net_cash:,.1f}); "
                  f"the company holds more cash than debt")
chk(V['nci'] > 0, f"minority interests are DEDUCTED ({V['nci']:,.1f}), not added")
chk(0.0 < tv_share < 0.85, f"terminal value is {tv_share:.1%} of enterprise value — "
                           f"computed and printed, and inside the 85% ceiling")
chk(0.35 < fv_central / V['spot'] < 3.0,
    f"implied fair value to spot {fv_central/V['spot']:.2f}x is inside the stated "
    f"plausibility band of 0.35x-3.0x")
chk(wacc_term < wacc_exp, f"terminal rate {wacc_term:.2%} is BELOW the explicit-window "
                          f"rate {wacc_exp:.2%}")
chk(abs(recon_rev) < 0.005, f"bottom-up FY2025 revenue reproduces the disclosed figure to "
                            f"{recon_rev:+.3%}")
chk(abs(recon_ebit) < 0.010, f"bottom-up FY2025 operating profit reproduces the DISCLOSED "
                             f"figure to {recon_ebit:+.3%}")
chk(all(BU[i]['mgn'] > BU[i + 1]['mgn'] for i in range(1, 5)),
    "the forecast EBITDA margin glides DOWN every year from the FY2025 peak")
chk(TAXE >= TAX, f"the effective tax rate used ({TAXE:.2%}) is at or above the statutory "
                 f"rate ({TAX:.2%})")
chk(GDV['holds'], "growth destroys value at the terminal return on capital, and the model "
                  "shows it: the valuation FALLS as terminal growth rises")
chk(SHT['spread'] < 0.005, f"the share count agrees across three independent routes to "
                           f"{SHT['spread']:.3%}")
chk(all(df_[i] > df_[i + 1] for i in range(4)), "discount factors decline monotonically")
chk(abs(sum(WT.values()) - 1.0) < 1e-9, "lens weights sum to exactly 1")
chk(min(LENS.values()) <= fv_central <= max(LENS.values()),
    "the weighted central sits inside the range of the four lenses")
say("\n" + "=" * 78)
say("ASSERT LOG")
for i, m in enumerate(A, 1):
    say(f"  {i:2d}. {m}")
say("=" * 78)

# ==================== EMIT ==================================================
OUT = dict(
    meta=dict(ticker='ARCC', company='Arabian Cement Company S.A.E.', market='EGX',
              market_code='EG', currency='EGP', asof='2026-08-06', spot=V['spot'],
              shares_mn=SH, mktcap=MKTCAP,
              klass='single-asset cement operating company (net cash)',
              sector='Construction materials — cement'),
    inputs=INP,
    bottom_up=BU, clinker_factor=cf,
    dna_triangulation=DNAT, share_triangulation=SHT,
    history=dict(years=HIST, revenue=rev_h, ebitda=ebitda_h, dna=dna_h, ebit=ebit_h,
                 pat=pat_h, nopat=nopat_h, volume_mt=vol_h, price_t=price_h,
                 utilisation=[V['util_fy23'], V['util_fy24'], V['kiln_util'][0]],
                 margin=[ebitda_h[i] / rev_h[i] for i in range(3)],
                 eps=[pat_h[i] / SH for i in range(3)],
                 netfin_fy25=netfin_fy25, pbt_fy25=pbt_fy25, tax_eff=TAXE),
    forecast=dict(years=YRS, revenue=rev_f, ebitda=ebitda_f, dna=dna_f, ebit=ebit_f,
                  nopat=nopat, capex=capex, dwc=dwc, fcff=fcff, df=df_, pv=pv,
                  fwd_wacc=fwd, glide=glide, t_mid=t_mid, treasury=treas_f, pbt=pbt_f,
                  tax=tax_f, pat=pat_f, dividends=div_f, cash=cash_b, equity=eq_b,
                  ppe=ppe_b, wc=wc_b, total_assets=ta_b,
                  volume_mt=[b['cement'] for b in BU[1:]],
                  price_t=[b['price'] for b in BU[1:]],
                  margin=[b['mgn'] for b in BU[1:]],
                  eps=[p / SH for p in pat_f], dps=[d / SH for d in div_f]),
    wacc=dict(rf=V['rf'], rf_star=rf_star, beta=beta_used, ke_exp=ke_exp, kd=V['kd'],
              kd_at=kd_at, wd_gross=wd_gross, wd_net=wd_net, wacc_exp=wacc_exp,
              wacc_exp_net_weights=wacc_exp_netw, beta_term=beta_t, ke_term=ke_term,
              kd_term_at=V['kd_term'] * (1 - TAX), wacc_term=wacc_term,
              ke_raw_retired=V['rf'] + beta_used * V['erp_cds'], mktcap=MKTCAP),
    dcf=dict(sum_pv=sum_pv, tv=tv, pv_tv=pv_tv, ev=ev, tv_share=tv_share,
             cash_at_val=cash_at_val, net_cash=net_cash, nci=V['nci'], equity=eq_dcf,
             fv=fv_dcf, roic_term=roic_t, rr_term=rr_t, ic_repl=ic_repl,
             nopat_term=nopat[-1] * (1 + V['g_term']), nopat0=nopat0,
             net_debt_bs=net_debt_bs, rem=REM),
    lenses=dict(values=LENS, weights=WT, central=fv_central, low=min(LENS.values()),
                high=max(LENS.values()), ebitda_norm=eb_norm, nopat_norm=nopat_norm,
                ev_per_t_spot=ev_per_t, ev_asset=ev_asset, ev_spot=ev_spot,
                bvps=V['eq_fy25_rep'] / SH,
                roe_sust=V['pat_fy25'] / V['eq_fy25_rep']),
    lens_ranges=LR, sensitivity=SENS, contested=CONTESTED,
    terminal_reconciliation=TR, growth_destroys_value=GDV, equity_gap=eq_gap,
    experts=EXPERTS, peers=PEERS, assert_log=A, log=LOG,
)
with open(os.path.join(HERE, 'study_numbers.json'), 'w') as f:
    json.dump(OUT, f, indent=1, default=float)
print(f"\nwrote study_numbers.json — central EGP {fv_central:.2f}, spot {V['spot']:.2f}, "
      f"TV {tv_share:.1%} of EV, {len(A)} assertions passed")
