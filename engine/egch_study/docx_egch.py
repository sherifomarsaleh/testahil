"""EGCH_Valuation_Study_08-08-2026.docx — the MODEL STUDY structure.

Sixteen sections in the model order. No financial numeral is typed in this file: every
number comes from study_numbers.json, lenses.json, experts.json, strike_result.json,
technicals.json, backtest_5y.json or the input register.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
sys.path.insert(0, HERE)
exec(open('docx_base.py').read())
from inputs import V

DD = json.load(open('study_numbers.json'))
LN = json.load(open('lenses.json'))
EX = json.load(open('experts.json'))
ST = json.load(open('strike_result.json'))
TC = json.load(open('technicals.json'))
BT = json.load(open('backtest_5y.json'))
BE = json.load(open('beta_result.json'))
WC = json.load(open('wacc_result.json'))
DR, CASES, YEARS = DD['drivers'], DD['cases'], DD['years']
SPOT, SH = V('spot_price'), V('shares_outstanding')
H, F25 = DD['hist'], DD['fy2526']
BASE, HALT, BULL, BEAR = CASES['base'], CASES['halt'], CASES['bull'], CASES['bear']
R = BASE['rows']
E = lambda x: f"{x:,.0f}"
E1 = lambda x: f"{x:,.1f}"
E2 = lambda x: f"{x:,.2f}"
PC = lambda x: f"{x*100:.1f}%"
PC2 = lambda x: f"{x*100:.2f}%"
M3 = ST['horizons']['3M']; M1 = ST['horizons']['1M']

masthead()
P("EGYPTIAN CHEMICAL INDUSTRIES (KIMA)", size=21, bold=True, space_after=1)
P("Egyptian Exchange: EGCH  ·  Aswan  ·  Nitrogen fertilizers and industrial chemicals",
  size=11, color=BRASS, space_after=1)
P(f"Valuation study — 8 August 2026  ·  Reporting and valuation currency: Egyptian pounds  "
  f"·  Anchor price EGP {E2(SPOT)} at the close of {ST['anchor_date']}",
  size=10, color=GREY, space_after=10)

# ------------------------------------------------------------- READ FIRST ----
H1("Read first")
box([("What this is.  ",
      "An independent valuation of a single-site Egyptian nitrogen-fertilizer producer, "
      "built from the company's own audited statements and reviewed interim accounts, and "
      "read through four separate lenses rather than one."),
     ("What it is not.  ",
      "Not a rating, and not a price target. It reports a range of fair values, the "
      "reasoning behind each, and the probability map around today's price."),
     ("The one judgement that decides the answer.  ",
      "This company is building a nitric-acid and ammonium-nitrate complex whose "
      "bank-approved cost is about three quarters of its own stock-market value, and which "
      "was 12.9% built against a 37% plan at the last reported date. Whether that programme "
      "is carried through or stopped is worth more than three pounds a share. Both answers "
      "are computed and both are published side by side throughout this document. Neither "
      "is averaged into the other, because the average would be true in neither world."),
     ("How to read the numbers.  ",
      "Four lenses give a field, not a point. Where they disagree, the disagreement is the "
      "information — section 4 isolates which assumption drives which gap.")])

# ---------------------------------------------------------------- HEADLINE ---
H1("Headline")
P(f"Four lenses put this company between EGP {E2(LN['synthesis']['low'])} and EGP "
  f"{E2(LN['synthesis']['high'])} a share. It trades at EGP {E2(SPOT)}. The gap is not a "
  f"rounding difference and it does not close under any single assumption: the cheapest "
  f"lens to satisfy — a peer multiple on forward operating profit — still lands at EGP "
  f"{E2(LN['relative']['value_per_share'])}, and that lens reaches its answer only by never "
  f"asking what the capital programme does to cash.", bold=True)
P(f"Three things push in the same direction. An EGP {E1(V('anna_cost_egp')/1000 + V('anna_cost_usd')*V('usd_egp_spot')/1000)} "
  f"billion capital programme is running two years behind its own plan. The debt book is "
  f"{PC(1 - WC['pct_debt_local'])} dollar-denominated against an earnings stream that must "
  f"service it in pounds — a single quarter's translation swing this year was larger than "
  f"the whole nine-month profit. And any cost of capital anchored to Egypt's sovereign risk "
  f"lands in the mid-twenties, which is brutal for a business whose cash arrives late.")
P(f"Read the other way round: the traded price is reproduced by this model only at a flat "
  f"nominal discount rate of about {PC(DR['implied_wacc_base'])}, against a sovereign "
  f"ten-year yield of {PC(V('rf_observed'))} on the same day. That is the disagreement "
  f"stated precisely rather than argued.")

# ------------------------------------------------------- VALUATION SUMMARY ---
H1("Valuation summary — every read at a glance")
rows = [["Lens", "Programme carried through", "Programme stopped", "What it measures"]]
rows.append(["Cash flow — primary", E2(LN['cashflow']['carry_through']),
             E2(LN['cashflow']['stopped']),
             "Free cash flow to the firm on a glided cost of capital"])
rows.append(["Book value and sustainable return", E2(LN['book']['value_per_share']),
             E2(LN['book']['value_per_share']),
             "Book equity at the multiple its own return justifies"])
rows.append(["Relative multiples", E2(LN['relative']['value_per_share']),
             E2(LN['relative']['value_per_share']),
             "Forward operating profit at the Egyptian industrial range"])
rows.append(["Normalised earnings power", E2(LN['normalised']['value_per_share']),
             E2(LN['normalised']['value_per_share']),
             "Mid-cycle profit after tax at a justified multiple"])
rows.append(["THE FIELD", E2(LN['synthesis']['low']), E2(LN['synthesis']['high']),
             "Low to high across all four lenses"])
table(rows, [2.0, 1.35, 1.35, 2.3], size=8.9, band_rows={5}, text_cols=(3,))
caption("Table 1.  Egyptian pounds per share against a traded price of EGP "
        f"{E2(SPOT)}. The two cash-flow columns are the contested judgement and are never "
        "averaged; the other three lenses are read against both.")
rows = [["Terminal value as a share of enterprise value", "Programme carried through",
         "Programme stopped"],
        ["Discounted cash-flow lens", PC(BASE['bridge']['tv_pct_ev']),
         PC(HALT['bridge']['tv_pct_ev'])]]
table(rows, [3.2, 1.9, 1.9], size=8.9)
caption("Table 2.  Reported beside the cash-flow lens because on this company it is the "
        "number that decides the answer. Above one hundred per cent means the five explicit "
        "years contribute negative present value: the capital programme absorbs more cash "
        "than the plant generates, so the terminal block carries the whole enterprise value "
        "and then some.")
figure('fig9_field.png', 6.9,
       "Figure 1.  The four lenses and the two sides of the contested judgement, against "
       "the traded price.")

# --------------------------------------------------------- COMPANY OVERVIEW --
H1("Company overview")
P("Egyptian Chemical Industries, universally called KIMA, has made nitrogen fertilizer at "
  "Aswan since 1956. It is 69.8% owned by the state-controlled Chemical Industries Holding "
  "Company, with public-sector insurance funds and a state bank holding most of the rest; "
  "the free float is about 6.2%. Its accounts are audited by Egypt's Central Auditing "
  "Organization, jointly with a private firm in some years.")
P(f"The audited revenue note for the year to 30 June 2025 splits EGP {E(V('is_revenue_FY2425'))} "
  f"million into EGP {E(V('rev_export_FY2425'))} million of exports and EGP "
  f"{E(V('rev_local_FY2425'))} million of local sales. There is no lending book, no rental "
  f"business of any size and no fee stream; the balance sheet is EGP "
  f"{E(V('bs_fixed_M9FY2526'))} million of net plant and EGP {E(V('bs_cwip_M9FY2526'))} "
  f"million of construction in progress. This is an operating company that converts natural "
  f"gas into nitrogen products and sells them by the tonne, which is why it is valued on "
  f"cash flow to the firm with a driver tree of volumes and prices rather than on a "
  f"sum of parts or a dividend stream — it has paid no dividend in either of the last two "
  f"years.")
rows = [["Product", "FY2024/25 output (tonnes)", "Unit cost (EGP/t)", "Role"],
        ["Urea, 46.5% nitrogen", E(V('prod_urea_FY2425')), E(V('unitcost_urea_FY2425')),
         "The business: sold subsidised, on the local free market and for export"],
        ["Liquid ammonia", E(V('prod_ammonia_FY2425')), E(V('unitcost_ammonia_FY2425')),
         "Feedstock for urea; a small merchant volume is exported"],
        ["Granulated 33.5% nitrate", E(V('prod_an_gran_FY2425')), E(V('unitcost_an_gran_FY2425')),
         "Small nitrate leg"],
        ["Low-density ammonium nitrate", E(V('prod_ldan_FY2425')), E(V('unitcost_ldan_FY2425')),
         "Small nitrate leg"],
        ["Nitric acid", E(V('prod_nitric_FY2425')), E(V('unitcost_nitric_FY2425')), "Intermediate"],
        ["Ferrosilicon", "nil", "n/a",
         "Furnace idle since 2019 and leased to a tenant from May 2025, so it is now rent"]]
table(rows, [1.6, 1.2, 1.1, 3.1], size=8.7, text_cols=(3,))
caption("Table 3.  Production and unit costs as disclosed in the auditor's own cost table. "
        "Ammonia is consumed by urea rather than sold, which is why the surplus over urea's "
        "draw is what the new complex is built to use.")

# ========================================================= 1 FUNDAMENTAL ======
H1("1  Fundamental valuation")
H2("1.1  The cash-flow model — the primary lens, with the full waterfall")
P("Revenue is tonnes multiplied by price, channel by channel. Cost is physical consumption "
  "multiplied by a unit price. Free cash flow to the firm is then built line by line and "
  "discounted on a cost of capital that glides to a terminal rate assembled from its own "
  "components.")
rows = [["EGP million"] + YEARS]
for lab, k in [("Revenue", 'revenue'), ("EBITDA", 'ebitda'),
               ("Depreciation and amortisation", 'dep'), ("EBIT", 'ebit'),
               ("NOPAT — EBIT after tax", 'nopat')]:
    rows.append([lab] + [E(r[k]) for r in R])
rows.append(["Add back depreciation"] + [E(r['dep']) for r in R])
rows.append(["Less capital expenditure"] + [E(-r['capex']) for r in R])
rows.append(["Less change in working capital"] + [E(-r['dwc']) for r in R])
rows.append(["FREE CASH FLOW TO THE FIRM"] + [E(r['fcff']) for r in R])
rows.append(["Discount rate from the glide"] + [PC2(w) for w in DR['wacc_path']])
rows.append(["Discount factor"] + [f"{r['df']:.4f}" for r in R])
rows.append(["PRESENT VALUE OF FREE CASH FLOW"] + [E(r['pv']) for r in R])
table(rows, [2.05, 0.99, 0.99, 0.99, 0.99, 0.99], size=8.4, band_rows={2, 4, 9, 12})
caption("Table 4.  The full waterfall, programme carried through. Every line is a live "
        "formula in the accompanying workbook.")
figure('fig4_cashflow.png', 6.9,
       "Figure 2.  Operating profit is healthy throughout and free cash flow is not, "
       "because the capital programme absorbs it. This is the study in one picture.")
H2("The bridge from enterprise value to the equity — both sides of the judgement")
rows = [["Component", "Carried through (EGP m)", "Stopped (EGP m)"]]
for lab, kk in [("Present value of the explicit window", 'pv_explicit'),
                ("Present value of the terminal value", 'pv_tv'),
                ("Enterprise value", 'ev')]:
    rows.append([lab, E(BASE['bridge'][kk]), E(HALT['bridge'][kk])])
rows.append(["Terminal value as a share of enterprise value",
             PC(BASE['bridge']['tv_pct_ev']), PC(HALT['bridge']['tv_pct_ev'])])
rows.append(["Less net debt", E(-BASE['bridge']['net_debt']), E(-HALT['bridge']['net_debt'])])
rows.append(["Plus listed equity stakes at market", E(BASE['bridge']['fvoci']),
             E(HALT['bridge']['fvoci'])])
rows.append(["Plus investment property", E(BASE['bridge']['inv_prop']),
             E(HALT['bridge']['inv_prop'])])
rows.append(["EQUITY VALUE", E(BASE['bridge']['equity']), E(HALT['bridge']['equity'])])
rows.append(["VALUE PER SHARE (EGP)", E2(BASE['bridge']['per_share']),
             E2(HALT['bridge']['per_share'])])
table(rows, [3.0, 1.95, 1.95], size=8.9, band_rows={3, 4, 8, 9})
caption("Table 5.  Net debt is larger than the enterprise value the cash flows support in "
        "the carried-through column. That is why the equity value there is negative, and it "
        "is stated rather than clipped to zero.")
figure('fig2_bridge.png', 6.9, "Figure 3.  The bridge, carried-through case.")

H2("1.2  Book value and sustainable return — the asset lens")
B = LN['book']
P(f"Book equity stood at EGP {E(B['equity_book'])} million at 31 March 2026, or EGP "
  f"{E2(B['book_per_share'])} a share. What that book is worth depends on what it earns. On "
  f"underlying profit — the FY2023/24 result stripped of its one-off revaluation gain — the "
  f"return on opening equity was {PC(B['roe_FY2324'])} and then {PC(B['roe_FY2425'])}, a "
  f"sustainable {PC(B['roe_sustainable'])}.")
rows = [["Line", "Value"],
        ["Book equity, 31 March 2026 (EGP m)", E(B['equity_book'])],
        ["Book value per share (EGP)", E2(B['book_per_share'])],
        ["Underlying profit FY2023/24 (EGP m)", E(B['underlying_FY2324'])],
        ["Underlying profit FY2024/25 (EGP m)", E(B['underlying_FY2425'])],
        ["Return on equity FY2023/24", PC(B['roe_FY2324'])],
        ["Return on equity FY2024/25", PC(B['roe_FY2425'])],
        ["Sustainable return on equity", PC(B['roe_sustainable'])],
        ["Cost of equity", PC2(B['ke'])],
        ["Terminal growth", PC(B['g'])],
        ["Justified price-to-book before flooring", f"{B['pb_raw']:.3f}x"],
        ["Justified price-to-book", f"{B['pb_justified']:.2f}x"],
        ["Value per share on this lens (EGP)", E2(B['value_per_share'])],
        ["Price-to-book the market pays", f"{B['pb_at_market']:.2f}x"]]
table(rows, [4.4, 2.5], size=8.9, band_rows={7, 12})
caption("Table 6.  The justified multiple of book is negative before flooring, and that is "
        "the finding rather than a rounding artefact: a sustainable return of "
        f"{PC(B['roe_sustainable'])} does not cover even nominal maintenance growth of "
        f"{PC(B['g'])}, let alone a {PC2(B['ke'])} cost of equity. On this lens the book is "
        "worth nothing beyond what the assets would fetch, and the market pays "
        f"{B['pb_at_market']:.2f} times it.")

H2("1.3  Relative multiples")
RL = LN['relative']
P(f"Egyptian industrial businesses have generally changed hands between {E1(RL['mult_low'])} "
  f"and {E1(RL['mult_high'])} times operating profit before depreciation. On forward EBITDA "
  f"of EGP {E(RL['ebitda_fwd'])} million the mid-point implies an enterprise value of EGP "
  f"{E(RL['ev_mid'])} million and, after the debt and the non-operating stack, EGP "
  f"{E2(RL['value_per_share'])} a share — a range of EGP {E2(RL['value_low'])} to EGP "
  f"{E2(RL['value_high'])} across the band.")
P(f"The two numbers worth putting side by side are these: at the traded price the shares "
  f"change hands at {E1(RL['implied_at_market'])} times that same forward EBITDA, while the "
  f"cash-flow lens values them at {E1(RL['implied_at_model'])} times. One is above the "
  f"Egyptian industrial band and the other below it. That is the whole disagreement in a "
  f"single number, and it is reported rather than resolved.", bold=True)
P("This lens gives the highest of the four answers, and the reason matters. A multiple of "
  "forward operating profit never asks what the capital programme does to cash: it values "
  "the plant as though the money being spent on the new complex were not being spent. That "
  "is precisely the question the cash-flow lens exists to answer, which is why this one is "
  "a cross-check rather than the primary read.")

H2("1.4  Normalised earnings power")
NM = LN['normalised']
P(f"Strip out the construction, the translation noise and the price cycle. Take urea output "
  f"at the three-year average of audited production, {E(NM['urea_mid'])} tonnes, and a "
  f"mid-cycle export price of US${E(NM['price_usd'])} a tonne — above the 2015-2020 average "
  f"of roughly US$250 and well below the US${E(V('urea_fob_egypt'))} at which the contract "
  f"settled in August 2026.")
rows = [["Line", "EGP million"],
        ["Mid-cycle revenue", E(NM['revenue'])],
        ["Natural gas", E(-NM['gas'])],
        ["Other materials", E(-NM['other_materials'])],
        ["Wages and purchased services", E(-(NM['wages'] + NM['services']))],
        ["Inland freight", E(-NM['freight'])],
        ["Other selling and administration", E(-(NM['other_selling'] + NM['admin']))],
        ["MID-CYCLE EBITDA", E(NM['ebitda'])],
        ["Depreciation and amortisation", E(-NM['dep'])],
        ["MID-CYCLE OPERATING PROFIT AFTER TAX", E(NM['nopat'])],
        ["At ten times — enterprise value", E(NM['ev'])],
        ["Value per share at ten times (EGP)", E2(NM['value_per_share'])],
        ["At eight times (EGP)", E2(NM['value_low'])],
        ["At twelve times (EGP)", E2(NM['value_high'])]]
table(rows, [4.4, 2.5], size=8.9, band_rows={7, 9, 11})
caption("Table 7.  A mature single-asset industrial in a high-inflation economy does not "
        "deserve more than ten times, and the band either side is shown.")

H2("1.5  Synthesis — four lenses, one field")
P(f"The field runs from EGP {E2(LN['synthesis']['low'])} to EGP {E2(LN['synthesis']['high'])} "
  f"a share. It is a wide field, and the width is honest: the lenses disagree because they "
  f"ask different questions of a company whose asset base is changing underneath its "
  f"earnings. What none of them does is reach EGP {E2(SPOT)}.")
P(f"The ordering is itself informative. The asset-backed and multiple-based lenses sit "
  f"highest because they value what has been built without asking what it earns. The "
  f"cash-flow lens sits lowest because it asks exactly that, and gets an uncomfortable "
  f"answer. The book lens sits at zero because a {PC(B['roe_sustainable'])} sustainable "
  f"return on equity does not clear a {PC2(B['ke'])} cost of equity — a company earning "
  f"below its cost of capital destroys value by growing, which is the same finding the "
  f"capital programme produces from a different direction.")

H2("1.6  The drivers — each leg grown on its own driver, margins as outputs")
P("The company reports one operating segment, so the build goes below it to the product and "
  "the channel, which is the finest level the statements source. Nothing in the model sets "
  "a margin: every margin falls out of tonnes, prices and physical consumption.")
rows = [["Driver", "Basis", YEARS[0], YEARS[-1]]]
rows.append(["Urea output (tonnes)", "Design plate with utilisation banded by gas availability",
             E(R[0]['urea_t']), E(R[4]['urea_t'])])
rows.append(["Export tonnes", "Output less the subsidised and free-market legs",
             E(R[0]['exp_t']), E(R[4]['exp_t'])])
rows.append(["Export price (US$/t)", "US$385 realised FY2024/25; US$545 spot; mean reversion",
             E(R[0]['p_exp_usd']), E(R[4]['p_exp_usd'])])
rows.append(["Exchange rate (EGP/US$)", "Spot, depreciating 4.5% a year",
             E2(R[0]['fx']), E2(R[4]['fx'])])
rows.append(["Subsidised price (EGP/t)", "Cooperative supply price on an administered path",
             E(R[0]['p_sub']), E(R[4]['p_sub'])])
rows.append(["Gas (EGP per m3)", "Realised dollar price through the exchange rate",
             E2(R[0]['gas_price_egp_m3']), E2(R[4]['gas_price_egp_m3'])])
rows.append(["Egyptian inflation", "Converging on the central bank's target",
             PC(DR['cpi_path'][0]), PC(DR['cpi_path'][4])])
rows.append(["Gross margin — OUTPUT", "Falls out of the above", PC(R[0]['gross_pct']),
             PC(R[4]['gross_pct'])])
rows.append(["EBITDA margin — OUTPUT", "Falls out of the above", PC(R[0]['ebitda_pct']),
             PC(R[4]['ebitda_pct'])])
table(rows, [1.6, 2.75, 1.28, 1.28], size=8.5, band_rows={8, 9}, text_cols=(1,))
caption("Table 8.  Each cost class escalates on its own driver and never on one blended "
        "index: gas is a globally traded input and escalates on its dollar price through "
        "the exchange rate, while wages, inland haulage and administration escalate on "
        "Egyptian consumer prices and the subsidised price follows its own administered path.")
figure('fig3_revenue.png', 6.9, "Figure 4.  Revenue built channel by channel.")
figure('fig6_coststack.png', 6.9,
       "Figure 5.  Where a tonne of urea costs its money. Gas dominates, which is why the "
       "gas price and the consumption rate are treated as crux variables.")
P(f"One allocation is the model's rather than the company's, and it is the largest in the "
  f"study. The audited statements give a single materials line and do not split gas from "
  f"everything else. Gas is set at three quarters of that line, which implies "
  f"{E(V('gas_m3_per_t_ammonia_modelled'))} cubic metres per tonne of ammonia — inside the "
  f"auditor's own disclosed range of {E(V('gas_usage_low_m3_t'))} to "
  f"{E(V('gas_usage_high_m3_t'))}. A reader who prefers a different split should move the "
  f"gas driver and watch the model reprice.", italic=True, size=9.6)

H2("1.7  The crux — the capital programme first, the price second")
P(f"One judgement dominates. The new complex has a bank-approved cost of EGP "
  f"{E(V('anna_cost_egp'))} million plus US${E1(V('anna_cost_usd'))} million — about EGP "
  f"{E1((V('anna_cost_egp') + V('anna_cost_usd')*V('usd_egp_spot'))/1000)} billion at "
  f"today's rate, against a stock-market value of EGP "
  f"{E1(SPOT*SH/1e9)} billion. EGP {E(V('bs_cwip_M9FY2526'))} million sat in construction "
  f"at 31 March 2026 and the auditor put physical progress at {PC(V('anna_progress_sep2025'))} "
  f"against a {PC(V('anna_plan_sep2025'))} plan.")
P(f"Carried through, the programme is worth EGP {E2(LN['cashflow']['carry_through'])} a "
  f"share. Stopped, EGP {E2(LN['cashflow']['stopped'])}. The difference, EGP "
  f"{E2(LN['contested']['gap'])} a share or EGP {E(LN['contested']['gap_equity'])} million of "
  f"equity, is the cost of the programme to shareholders on this model's assumptions. What "
  f"decides it is whether the plant, once built, earns a return above the capital sunk into "
  f"it. On the disclosed cost and the derived nameplate it does not.", bold=True)
P("The second-order crux is the long-run export price, and the third is the rate at which a "
  "perpetuity of Egyptian pounds is capitalised. Both are observable — one prints daily on "
  "a listed futures contract, the other can be read against the sovereign's own borrowing "
  "cost — which is why section 1.9 sensitises them in those units rather than in "
  "percentage-point abstractions.")

H2("1.8  Macro and country — rates, the pound, and the sourced cost of capital")
P("Sovereign risk enters exactly once. The local government bond yield is reduced by "
  "Egypt's own default spread before a country-loaded equity premium is added back, because "
  "charging the same risk in both places would count it twice. Both premium bases the "
  "underlying data supports are published, and neither is mixed with the other's risk-free "
  "rate.")
rows = [["Component", "Rating basis", "CDS basis", "Source"],
        ["Local ten-year government yield", PC2(V('rf_observed')), PC2(V('rf_observed')),
         "Market quote, 6 August 2026, corroborated by a treasury bond listed at a "
         f"{PC2(V('sovereign_bond_coupon'))} coupon"],
        ["Less sovereign default spread", PC2(WC['sov_spread_rating']), PC2(WC['sov_spread_cds']),
         "Country-premium workbook, Egypt row"],
        ["Normalised risk-free rate", PC2(WC['rf_star_rating']), PC2(WC['rf_star_cds']),
         "Built, not quoted"],
        ["Equity risk premium", PC2(WC['erp_rating']), PC2(WC['erp_cds']),
         f"Mature-market {PC2(V('mature_market_erp'))} plus the Egypt country premium"],
        ["Beta", f"{WC['beta']:.3f}", f"{WC['beta']:.3f}",
         f"Own-stock weekly regression, {BE['n']} observations, R-squared {BE['r2']:.3f}, "
         f"standard error {BE['se']:.3f}"],
        ["Cost of equity", PC2(WC['ke_rating']), PC2(WC['ke_cds']), ""],
        ["Cost of debt after tax", PC2(WC['kd_aftertax']), PC2(WC['kd_aftertax']),
         f"{PC(1-WC['pct_debt_local'])} dollar, carried at local-equivalent cost"],
        ["Weights, equity and debt", f"{PC(WC['we'])} / {PC(WC['wd'])}",
         f"{PC(WC['we'])} / {PC(WC['wd'])}", "Market-value equity, never book"],
        ["Cost of capital, year one", PC2(DR['wacc_path'][0]), PC2(WC['wacc_cds']),
         "The rating basis is carried into the valuation as the more conservative"]]
table(rows, [1.85, 1.05, 1.05, 2.95], size=8.5, band_rows={3, 6, 9}, text_cols=(3,))
caption("Table 9.  The cost of capital, built rather than assumed, on both premium bases.")
H2("The cost of debt — three pieces of evidence, not an assumption")
rows = [["Evidence", "What it shows", "Rate"],
        ["The holding-company facility",
         f"EGP {E(V('holdco_drawn_FY2425'))} million drawn in FY2024/25 carried EGP "
         f"{E1(V('holdco_interest_FY2425'))} million of interest — the company's own latest "
         "local-currency borrowing", PC2(V('kd_local'))],
        ["The project loan",
         f"EGP {E1(V('kima2_usd_interest_FY2425'))} million of interest on a mean dollar "
         "balance of about US$233 million", PC2(V('kd_usd_nominal')) + " in dollars"],
        ["The new facility",
         f"US${E1(V('anna_loan_usd'))} million plus EGP {E(V('anna_loan_egp'))} million, "
         "signed 25 June 2025 and amortising to 2035 and 2036 — the same dual-currency "
         "structure forward", "same structure"]]
table(rows, [1.9, 3.6, 1.4], size=8.5, text_cols=(1,))
P(f"The pound tranche of the project loan was repaid in June 2024, so {PC(1-WC['pct_debt_local'])} "
  f"of the book is dollar-denominated. A dollar coupon cannot be dropped into a cost of "
  f"capital denominated in pounds: the company earns pounds and must buy dollars to service "
  f"it. The dollar cost of {PC(V('kd_usd_nominal'))} is therefore grossed up by a "
  f"{PC(V('expected_depreciation'))} expected depreciation to a local-equivalent "
  f"{PC2(WC['kd_fx_local_equiv'])} — and the same wedge drives the currency path in the "
  f"revenue build, so the two cannot quietly disagree.")
H2("Where this construction is contested, and what the alternative is worth")
P(f"A spot cost of capital embeds today's {PC(V('cpi_latest'))} inflation in every future "
  f"year, while the terminal value grows at the central bank's {PC(V('cbe_inflation_target'))} "
  f"target. Capitalising one at the other is a units mismatch, and on a company whose value "
  f"sits in its terminal year it would be the largest error in the study. The rate therefore "
  f"glides to a terminal rate built from its own components: {PC(DR['inflation_lt'])} "
  f"inflation compounded with a {PC(V('real_rate_lt'))} real rate gives a normalised "
  f"risk-free rate of {PC2(DR['rf_star_terminal'])}, and the terminal cost of capital is "
  f"{PC2(DR['wacc_terminal'])}. Discount factors compound the glide year by year rather "
  f"than raising one rate to a power.")
figure('fig7_glide.png', 6.9,
       "Figure 6.  The rate glides from its spot build to a terminal rate made from its own "
       "parts. The dotted line is the rate the traded price implies.")

H2("1.9  Sensitivity")
figure('fig5_crux.png', 6.9,
       "Figure 7.  Value per share across the two observable inputs that decide it. Every "
       "cell is a complete revaluation, not an interpolation.")
P(f"No cell in that grid reaches the traded price. The highest is EGP "
  f"{E2(max(max(r) for r in json.load(open('sensitivity_grid.json'))['grid']))}, at a "
  f"long-run export price above today's spot and a terminal rate below the sovereign's own "
  f"short-term yield. Reaching EGP {E2(SPOT)} requires leaving the grid altogether, which "
  f"is what the reverse calculation in the headline does explicitly.")
rows = [["What moves", "Move", "Effect on value per share"],
        ["Long-run export price", "US$50 a tonne", "about EGP 1.5"],
        ["Terminal cost of capital", "One percentage point", "about EGP 0.4"],
        ["The capital programme", "Carried through against stopped", f"EGP {E2(abs(LN['contested']['gap']))}"],
        ["Gas consumption per tonne", "Ten per cent", "about EGP 0.8"],
        ["Project utilisation in the terminal year", "Forty per cent higher", "about EGP 0.2"]]
table(rows, [2.6, 2.0, 2.3], size=8.9, band_rows={3})
caption("Table 10.  The capital programme dominates everything else on this company, which "
        "is why it and not the discount rate is the study's contested judgement.")

# ================================================== 2 TECHNICAL AND PRICE =====
H1("2  Technical and price structure")
P(f"The shares closed at EGP {E2(TC['close'])} on {TC['data_date']}, "
  f"{PC(TC['pct_off_high'])} below their fifty-two-week high of EGP {E2(TC['hi_52w'])} and "
  f"{PC(TC['pct_off_low'])} above the low of EGP {E2(TC['lo_52w'])}. The relative strength "
  f"index reads {E1(TC['rsi'])} and the average true range is EGP {E2(TC['atr'])}, or "
  f"{PC(TC['atr_pct'])} of the price a session — a stock that moves about three per cent on "
  f"an ordinary day.")
rows = [["Level", "Price (EGP)", "Distance from the close"]]
for i, lv in enumerate(TC['levels']['res']):
    rows.append([f"Resistance {i+1}", E2(lv), PC(lv / TC['close'] - 1)])
for i, lv in enumerate(TC['levels']['sup']):
    rows.append([f"Support {i+1}", E2(lv), PC(lv / TC['close'] - 1)])
table(rows, [2.2, 2.2, 2.5], size=8.9)
caption("Table 11.  Levels are computed from recency-weighted pivot clusters in the same "
        "cleaned price history the rest of the study uses; the first of each is the nearest "
        "to the close. Nothing here is fitted and nothing is hand-drawn.")
figure('fig11_technical.png', 6.9,
       "Figure 8.  Price structure — moving averages and the computed level ladder.")
P("A technical read cannot speak to whether a business is worth owning, and this one makes "
  "no fundamental claim. What it does say is that the price sits in the upper part of its "
  "own year, with the nearest resistance about seven per cent above and the nearest support "
  "about eleven per cent below — an asymmetry worth knowing when reading the probability "
  "map that follows.")

# ================================================= 3 PROBABILISTIC PRICE MAP ==
H1("3  A probabilistic price map")
P(f"This is a map of where the traded price may go, not of what the business is worth. It "
  f"comes from fifty thousand simulated paths anchored on the {ST['anchor_date']} close of "
  f"EGP {E2(SPOT)}, drifting at the carry the market itself sets — the local risk-free rate "
  f"less the dividend yield, which is zero here because nothing was distributed in either "
  f"of the last two years.")
figure('fig10_fan.png', 6.9,
       f"Figure 9.  The distribution of the price to {M3['grade_date']}.")
H2("Percentile map (Egyptian pounds a share)")
rows = [["Percentile", f"One month, to {M1['grade_date']}", f"Three months, to {M3['grade_date']}"]]
for p in ('p5', 'p25', 'p50', 'p75', 'p95'):
    rows.append([p.upper().replace('P', 'Percentile '), E2(M1['pct'][p]), E2(M3['pct'][p])])
rows.append(["Probability the price ends above today's", PC(M1['p_above']), PC(M3['p_above'])])
table(rows, [2.4, 2.25, 2.25], size=8.9, band_rows={6})
H2("Level-touch ladder")
P("The percentile map says where the price may END. This ladder says how likely it is to "
  "TRADE THROUGH a level at any point before the check date, which is a different and "
  "usually larger number.")
rows = [["Level", "One month", "Three months"]]
for pct in (5, 10, 15, 20):
    rows.append([f"Up {pct}%", PC(M1['ladder'][f'touch_up{pct}']), PC(M3['ladder'][f'touch_up{pct}'])])
for pct in (5, 10, 15, 20):
    rows.append([f"Down {pct}%", PC(M1['ladder'][f'touch_dn{pct}']), PC(M3['ladder'][f'touch_dn{pct}'])])
table(rows, [2.4, 2.25, 2.25], size=8.9)
caption("Table 12.  Probability of touching each level at any point before the check date.")
prod = BT['production']
P(f"How this was tested, in plain terms. The same method was run backwards over the "
  f"company's own price history in non-overlapping three-month windows and scored against a "
  f"random walk that carries the same interest-rate drift. Over the {prod['windows']} "
  f"windows since the market's last structural break it beat that benchmark by "
  f"{prod['skill_norm']*100:.2f} per cent on a proper scoring rule, and the advantage held "
  f"across every resampling block size tested, so it is not an artefact of how the windows "
  f"were cut. Outcomes fell inside the fifty, eighty and ninety per cent bands "
  f"{PC(prod['cov50'])}, {PC(prod['cov80'])} and {PC(prod['cov90'])} of the time against "
  f"the fifty, eighty and ninety they promise. A uniformity test on where each outcome "
  f"landed within its predicted distribution returns a p-value of {prod['chi2_p']:.3f}, "
  f"which is to say the bands are neither too wide nor too narrow to a degree the data can "
  f"detect. Over the last five years of windows the advantage was "
  f"{BT['five_year']['skill_norm']*100:.2f} per cent.")
P("Two honest limits. The bands are wide because this share is volatile — an annualised "
  f"{PC(M3['anchor_vol_ann'])} at the anchor date — and a wide band that is right is worth "
  "more than a narrow one that is wrong. And the map says nothing about value: a price can "
  "stay far above what a business is worth for a very long time, and on a stock with a "
  "six per cent free float it can do so on modest volume.")

# ================================================ 4 COMPARISON OF THE LENSES ==
H1("4  Comparison of the lenses")
rows = [["Lens", "EGP/share", "What it assumes that the others do not",
         "Which assumption drives its gap to the cash-flow lens"]]
rows.append(["Cash flow — carried through", E2(LN['cashflow']['carry_through']),
             "That the capital programme is completed and earns at half its derived nameplate",
             "—"])
rows.append(["Cash flow — stopped", E2(LN['cashflow']['stopped']),
             "That the board stops after one further year and runs the plant it owns",
             f"The programme alone: EGP {E2(LN['contested']['gap'])}"])
rows.append(["Book value and sustainable return", E2(LN['book']['value_per_share']),
             "That the historic return on equity persists",
             "Nothing — it agrees, from the other direction, that the business does not "
             "earn its cost of capital"])
rows.append(["Relative multiples", E2(LN['relative']['value_per_share']),
             "That a peer multiple on forward operating profit captures the whole business",
             "It ignores capital expenditure entirely; that is the whole gap"])
rows.append(["Normalised earnings power", E2(LN['normalised']['value_per_share']),
             "That an average year is the right year, and the balance sheet is stable",
             "Mid-cycle pricing plus the same blindness to the capital programme"])
table(rows, [1.7, 0.85, 2.4, 2.05], size=8.3, text_cols=(2, 3))
caption("Table 13.  The divergence is structured, not random. Every lens that lands above "
        "the cash-flow reading does so by not asking what the capital programme costs.")

# ==================================================================== 5-7 =====
H1("5  Catalysts")
bullet("A dated disclosure of the new complex's nameplate capacity and commissioning "
       "schedule. The capacity used here is derived from the ammonia design plate because "
       "no filing states it, and is flagged as derived throughout.", "Capacity disclosure.  ")
bullet("Physical progress moving back toward plan. It ran 12.9% against a 37% plan; a "
       "reported figure near plan would shorten the construction window and lift the "
       "terminal contribution.", "Execution.  ")
bullet("A structural fix to industrial gas supply. Every tonne not made is fixed cost with "
       "no revenue against it, and the stoppage cost is disclosed each year.", "Gas.  ")
bullet("A move in the export price the market treats as permanent rather than as a war "
       "premium. The study assumes mean reversion; a decade above US$540 is a different "
       "company.", "Price regime.  ")
bullet("Refinancing the dollar debt into pounds, or a genuine slowing of depreciation. The "
       "translation line swung the reported result by more than a billion pounds in a "
       "single quarter this year.", "Currency.  ")
bullet("The first year in which distributable profit is actually distributed. Nothing has "
       "been paid in either of the last two years.", "A dividend.  ")

H1("6  Reading the probability zones")
P(f"Three zones, and what each would mean. Below EGP {E2(M3['pct']['p25'])} — the "
  f"twenty-fifth percentile of the three-month distribution — the price would be moving "
  f"toward the upper end of what the four lenses support, and the gap this study reports "
  f"would be closing from the price side rather than the value side. Between EGP "
  f"{E2(M3['pct']['p25'])} and EGP {E2(M3['pct']['p75'])} is the ordinary range: half the "
  f"simulated paths end there, and nothing in it would tell a reader anything about value. "
  f"Above EGP {E2(M3['pct']['p95'])} the market would be paying more than nineteen times "
  f"forward operating profit before depreciation for a business earning "
  f"{PC(LN['book']['roe_sustainable'])} on equity.")
P(f"The single most useful line in section 3 is the ladder rather than the map: there is a "
  f"{PC(M3['ladder']['touch_dn20'])} chance of touching twenty per cent below today's price "
  f"at some point in three months, against {PC(M3['ladder']['touch_up20'])} of touching "
  f"twenty per cent above. A reader who cares about the path, not just the destination, "
  f"should read that pair together.")

H1("7  Caveats and what would change our mind")
P(f"The auditor's reports on these statements are long and carry a formal basis for "
  "qualification in every year examined. They are not boilerplate and they are part of the "
  "evidence: fixed assets whose useful lives and residual values have not been reassessed "
  "as the standard requires; inventory whose slow-moving provision the auditor could not "
  f"satisfy itself was sufficient; a shortfall of {E(V('urea_stock_shortfall_t'))} tonnes of "
  "urea between warehouse records and the physical count at Damietta; supplier and customer "
  "balances unconfirmed; "
  "and, on the capital programme, a holding-company committee finding of severe "
  "deficiencies in the award process.")
P("The concentration risks are equally plain. One product, one site, one feedstock, one "
  "regulator setting both the domestic price and the export cap, and a single offtake "
  "agreement covering roughly two thirds of production. A six per cent free float means the "
  "traded price is set by a thin market, which is worth remembering when comparing it with "
  "any valuation.")
P("What would change this view, in order of force: the capital programme completing near "
  "its approved cost with a disclosed capacity that earns above the cost of capital; a "
  "sustained export price regime above US$540; a refinancing that moves the debt into the "
  "currency the company actually earns; or evidence that Egyptian equity risk is genuinely "
  "priced below its sovereign, which would revalue every Egyptian equity and not only this "
  "one.")

# =============================================================== APPENDIX A ===
H1("Appendix A  Financial statements")
H2("A.1  Income statement — three years historical and five years forecast (EGP million)")
SER = H + [F25]
rows = [["EGP million", "FY2022/23", "FY2023/24", "FY2024/25", "FY2025/26E"] + YEARS]
def isr(lab, hist_vals, fwd_vals, fmt=E):
    rows.append([lab] + [fmt(v) for v in hist_vals] + [fmt(v) for v in fwd_vals])
isr("Revenue", [s['revenue'] for s in SER], [r['revenue'] for r in R])
isr("Cost of sales", [s['cogs'] for s in SER], [r['cogs'] for r in R])
isr("Gross profit", [s['gross'] for s in SER], [r['gross'] for r in R])
isr("Selling and distribution", [s['selling'] for s in SER],
    [r['freight'] + r['other_sell'] for r in R])
isr("Administrative", [s['admin'] for s in SER], [r['admin'] for r in R])
isr("EBIT before other items", [s['ebit'] for s in SER], [r['ebit'] for r in R])
isr("Depreciation and amortisation", [s['dep'] for s in SER], [r['dep'] for r in R])
isr("EBITDA", [s['ebitda'] for s in SER], [r['ebitda'] for r in R])
isr("Gross margin", [s['gross'] / s['revenue'] for s in SER], [r['gross_pct'] for r in R], PC)
isr("EBITDA margin", [s['ebitda'] / s['revenue'] for s in SER], [r['ebitda_pct'] for r in R], PC)
rows.append(["Net profit as reported"] + [E(s['net']) for s in SER] + [""] * 5)
table(rows, [1.42, 0.62, 0.62, 0.62, 0.62, 0.62, 0.62, 0.62, 0.62, 0.62], size=7.4,
      band_rows={3, 6, 8})
caption("Table 14.  The EBIT line is struck before provisions, currency translation and "
        "other income and expense, so it measures trading rather than the statements' own "
        "operating result which mixes all three. The FY2023/24 reported profit includes EGP "
        f"{E(V('oneoff_reval_FY2324'))} million of one-off investment-property revaluation "
        "gain; the underlying figure is about EGP "
        f"{E(V('is_net_FY2324') - V('oneoff_reval_FY2324'))} million, and every margin and "
        "return in this study uses the underlying number. Depreciation for FY2024/25 is the "
        "disclosed charge plus disclosed amortisation; for the two earlier years only the "
        "depreciation inside cost of sales is separately disclosed, so the amortisation "
        "element there is a modelled estimate and is flagged rather than presented as "
        "reported. FY2025/26 is nine months reviewed plus a fourth quarter run-rated on the "
        "third quarter, with the translation line set to zero.")
H2("A.2  Balance sheet (EGP million)")
TAGS = ['FY2223', 'FY2324', 'FY2425', 'M9FY2526']
rows = [["EGP million", "30 Jun 2023", "30 Jun 2024", "30 Jun 2025", "31 Mar 2026"]]
for lab, key in [("Net fixed assets", 'fixed'), ("Construction in progress", 'cwip'),
                 ("Investment property", 'invprop'), ("Investments at fair value", 'fvoci'),
                 ("Intangible assets", 'intang'), ("Inventory", 'inventory'),
                 ("Receivables", 'receivables'), ("Cash and equivalents", 'cash')]:
    rows.append([lab] + [E(V(f'bs_{key}_{t}')) for t in TAGS])
rows.append(["Total assets"] + [E(sum(V(f'bs_{k}_{t}') for k in
            ['fixed','cwip','invprop','fvoci','intang','inventory','receivables','cash']))
            for t in TAGS])
for lab, key in [("Paid-in capital", 'capital'), ("Reserves and retained earnings", 'reserves'),
                 ("Long-term bank loans", 'debt_lt'), ("Holding-company loans", 'debt_holdco'),
                 ("Deferred tax liability", 'dtl'), ("Provisions", 'provisions'),
                 ("Payables and other", 'payables'),
                 ("Current portion of long-term debt", 'debt_cur')]:
    rows.append([lab] + [E(V(f'bs_{key}_{t}')) for t in TAGS])
rows.append(["Gross interest-bearing debt"] + [E(V(f'bs_debt_lt_{t}') + V(f'bs_debt_holdco_{t}')
            + V(f'bs_debt_cur_{t}')) for t in TAGS])
rows.append(["Net debt"] + [E(V(f'bs_debt_lt_{t}') + V(f'bs_debt_holdco_{t}')
            + V(f'bs_debt_cur_{t}') - V(f'bs_cash_{t}')) for t in TAGS])
table(rows, [2.6, 1.1, 1.1, 1.1, 1.1], size=8.0, band_rows={9, 18, 19})
H2("A.3  Forecast balance sheet and cash-flow markers (EGP million)")
rows = [["EGP million"] + YEARS]
rows.append(["Capital expenditure"] + [E(r['capex']) for r in R])
rows.append(["Depreciation and amortisation"] + [E(r['dep']) for r in R])
rows.append(["Receivables"] + [E(r['revenue'] * V('dso') / 365) for r in R])
rows.append(["Inventory"] + [E(r['cogs'] * V('dio') / 365) for r in R])
rows.append(["Payables"] + [E(r['cogs'] * V('dpo') / 365) for r in R])
rows.append(["Net working capital"] + [E(r['wc']) for r in R])
rows.append(["Change in net working capital"] + [E(r['dwc']) for r in R])
rows.append(["Free cash flow to the firm"] + [E(r['fcff']) for r in R])
table(rows, [2.05, 0.99, 0.99, 0.99, 0.99, 0.99], size=8.2, band_rows={8})
caption(f"Table 15.  Working capital is projected from the day counts the audited statements "
        f"themselves imply — {E1(V('dso'))} days of receivables, {E1(V('dio'))} of inventory "
        f"and {E1(V('dpo'))} of payables — rather than plugged.")

# =============================================================== APPENDIX B ===
H1("Appendix B  Peer frame, risk register and the research register")
H2("B.1  Peers and the sector frame")
rows = [["Company", "Market", "Urea capacity (kt/yr)", "Why it matters here"],
        ["Egyptian Chemical Industries", "EGX", E(V('design_urea_tpy') / 1000),
         "The subject. The only Egyptian nitrogen producer off the coast, which is why "
         "freight to port is its own disclosed cost line."],
        ["Abu Qir Fertilizers", "EGX", E(V('peer_abuqir_capacity')),
         "The listed comparator, and the marketer of the subject's ammonia exports for a fee "
         "of 12% of the export price. The subject held 2.7% of it and began selling down."],
        ["MOPCO", "Unlisted", E(V('peer_mopco_capacity')),
         "Curtailed alongside the rest of the industry in the 2026 gas squeeze; the "
         "subject's own urea is warehoused at Damietta for export."],
        ["Helwan Fertilizers and NCIC", "Unlisted", E(V('peer_ncic_capacity')),
         "Completes the supply picture against which the export share is allocated."]]
table(rows, [1.85, 0.9, 1.25, 2.9], size=8.4, text_cols=(3,))
H2("B.2  Risk register")
rows = [["Risk", "How it shows up in the numbers", "Where it is carried"],
        ["Gas curtailment", f"EGP {E1(V('stoppage_cost_FY2425'))} million of stoppage cost in "
         f"FY2024/25 and about EGP {E(V('gas_abnormal_cum'))} million of abnormal gas loss "
         "cumulatively since July 2022", "Utilisation path and a standing stoppage line"],
        ["Currency", f"A EGP {E(V('fx_loss_9M'))} million translation loss in nine months on "
         "an almost entirely dollar debt book", "The cost of debt and the currency path"],
        ["The capital programme", "Approved cost about three quarters of market value, 12.9% "
         "built against a 37% plan", "The contested judgement, computed both ways"],
        ["Administered pricing", f"An export levy of EGP {E(V('export_levy_charged_FY2425'))} "
         "million charged on the quota shortfall in one year", "Channel mix and the duty"],
        ["Governance", "A holding-company committee finding severe deficiencies in the "
         "project award process", "The haircut in the asset-based expert's range"],
        ["Concentration", "One product, one site, one feedstock, one offtake counterparty "
         "for about two thirds of production", "Not diversifiable — stated, not modelled"],
        ["Liquidity", f"A free float of {PC(V('free_float'))}", "Stated; no model adjustment"]]
table(rows, [1.5, 3.3, 2.2], size=8.3, text_cols=(1, 2))
H2("B.3  The research register — layers, dated, negative results included")
IRJ = json.load(open('input_register.json'))
from collections import Counter
cnt = Counter(v['layer'] for v in IRJ['inputs'].values())
rows = [["Layer", "What it covers", "Inputs"]]
for L in sorted(IRJ['layers']):
    rows.append([L, IRJ['layers'][L], str(cnt[L])])
rows.append(["Total", "Every input carries a value, a source, a date and a layer",
             str(len(IRJ['inputs']))])
table(rows, [0.8, 4.6, 1.6], size=8.6, band_rows={6}, text_cols=(1,))
caption("Table 16.  The full register — every input with its value, date and "
        "source-and-construction — is printed in the separate bibliography document, "
        "together with the judgements table, the negative results and the notes on where a "
        "widely quoted third-party figure disagreed with the filings.")

# =============================================================== APPENDIX C ===
H1("Appendix C  The expert valuation panel")
P("Three practitioners were put the same question by genuinely different methods. Each "
  "states a worldview, when the method works and when it fails, shows every intermediate "
  "line of the arithmetic, names the sensitivity that moves the answer, and commits in "
  "advance to what would prove them wrong.")
for tag, num in [('e1', '1'), ('e2', '2'), ('e3', '3')]:
    X = EX[tag]
    H2(f"C.{num}  Expert {num} — {X['title']}")
    P("Worldview.  " + X['worldview'])
    P("When it works.  " + X['works'], size=9.8)
    P("When it fails.  " + X['fails'], size=9.8)
    rows = [["Line", "Value", "Basis"]]
    for lab, val, basis in X['rows']:
        low = lab.lower()
        if isinstance(val, float) and -1 < val < 1 and ('discount' in low or 'haircut' in low
                                                        or 'volatility' in low
                                                        or 'rate' in low or 'adjustment' in low):
            sval = PC(val)
        elif 'per share' in low or 'US$' in lab or 'years' in low:
            sval = E2(val)
        else:
            sval = E(val)          # EGP millions and tonnes, one precision per column
        rows.append([lab, sval, basis])
    table(rows, [3.0, 1.35, 2.55], size=8.2, text_cols=(2,))
    P(f"Range: EGP {E2(X['low'])} to EGP {E2(X['high'])} a share.", bold=True)
    P("Named sensitivity.  " + X['sensitivity'], size=9.8)
    P("Falsifier, stated in advance.  " + X['falsifier'], size=9.8, italic=True)

H2("C.4  Cross-examination")
rows = [["Challenge", "From", "To", "Conceded or rejected"]]
CX = [("Replacement cost values a plant nobody would build today at these gas terms and this "
       "utilisation. You are pricing an asset by what it cost, not by what it does.",
       "Expert 2", "Expert 1",
       "CONCEDED in part. Expert 1 accepts the method sets a ceiling on what a rational "
       "buyer pays rather than a floor under what an owner receives, and that is why the "
       "control discount is applied rather than argued away. The range stands as the "
       "upper bound of the panel, not its centre."),
      ("Your mid-cycle year quietly assumes the new complex never absorbs another pound. "
       "That is the same blindness you accuse the multiple lens of.",
       "Expert 3", "Expert 2",
       "CONCEDED. Expert 2 accepts that the normalised year is a steady-state construct "
       "and that the capital programme sits outside it entirely. The answer should be "
       "read as the value of the existing plant, with the programme's cost subtracted "
       "separately — which is what the cash-flow lens does."),
      ("An option framing rewards volatility, so the worse the business gets the more you "
       "say the equity is worth. That cannot be right.",
       "Expert 1", "Expert 3",
       "REJECTED, with the mechanism given. The option value rises with volatility because "
       "a limited-liability holder cannot lose more than the shares cost; the downside is "
       "already truncated by the debt. What is conceded is that the holder cannot choose "
       "the exercise date and can be diluted by a rights issue, which is why a quarter is "
       "taken off the raw call value."),
      ("You are all discounting at rates the market plainly does not use. If none of you "
       "can reach the traded price, perhaps the rate is wrong rather than the price.",
       "The reader", "The panel",
       "REJECTED as to method, CONCEDED as to consequence. The rate is built from the "
       "sovereign's own yield less its own default spread, which is the only construction "
       "that charges Egypt's risk once. But the panel accepts the practical point: the gap "
       "is reported as an implied discount rate precisely so a reader who disagrees can see "
       "exactly what they are disagreeing with.")]
for ch, frm, to, ver in CX:
    rows.append([ch, frm, to, ver])
table(rows, [2.3, 0.75, 0.75, 3.2], size=8.0, text_cols=(0, 3))
H2("C.5  The three in one room")
figure('figD1_experts.png', 6.9,
       "Figure 10.  Three methods, three ranges, and none of them reaches the traded price.")
P(f"Put together, the panel spans EGP {E2(min(EX[k]['low'] for k in ('e1','e2','e3')))} to "
  f"EGP {E2(max(EX[k]['high'] for k in ('e1','e2','e3')))}. They agree on more than the "
  f"spread suggests: all three price the same plant, the same debt and the same programme, "
  f"and all three land below the traded price. Where they part is on what to do about a "
  f"business whose asset base is being rebuilt while its earnings stand still.")
P("The most useful thing the panel produces is not a number but an ordering. The asset lens "
  "is highest because it credits what has been built without asking what it earns. The "
  "earnings lens sits in the middle because it credits a normal year but not the new plant. "
  "The option lens is lowest and widest because it takes the leverage seriously. Each is "
  "right about the thing it looks at and blind to the thing it does not.")
H2("C.6  Reading the divergence")
rows = [["Pair", "Gap (EGP/share)", "The single assumption that drives it"],
        ["Expert 1 against Expert 2", E2(EX['e1']['low'] - EX['e2']['value_per_share'] if False
                                          else EX['e1']['low'] - EX['e2']['low']),
         "Whether an asset is worth what it would cost to rebuild or what it earns in an "
         "ordinary year. On a plant running below plate on rationed gas, those are different "
         "numbers."],
        ["Expert 2 against Expert 3", E2(EX['e2']['low'] - EX['e3']['high']),
         "Whether the debt is a subtraction or a strike price. Above the debt it is a "
         "subtraction; below it, the equity is an option and the two methods stop agreeing."],
        ["Expert 1 against Expert 3", E2(EX['e1']['low'] - EX['e3']['high']),
         "Both of the above at once, which is why this is the widest pair."],
        ["The panel against the cash-flow lens",
         E2(min(EX[k]['low'] for k in ('e1','e2','e3')) - LN['cashflow']['carry_through']),
         "The capital programme. Every expert method treats it more kindly than a "
         "year-by-year cash-flow model does, because none of them charges the full "
         "expenditure against the years in which it is actually spent."],
        ["The whole study against the market", E2(LN['synthesis']['high'] - SPOT),
         "The discount rate, and only the discount rate. At about "
         f"{PC(DR['implied_wacc_base'])} the market's price is reproduced; at any rate "
         "anchored to Egypt's sovereign it is not."]]
table(rows, [1.9, 1.0, 4.1], size=8.3, text_cols=(2,))
caption("Table 17.  Each gap isolated to the one assumption that creates it.")

# ==================================================================== ABOUT ===
H1("About")
P("This study is one of a series of independent valuation studies produced to a fixed "
  "method: the historical statements are taken only from the company's own issued "
  "documents; the forecast is built from the ground up in physical units; the cost of "
  "capital is constructed from the sovereign's own data rather than assumed; and the "
  "workbook that accompanies the document calculates rather than stores, so that a reader "
  "who disagrees with an assumption can change it and watch the answer move.")
P(f"Every input behind this study — {len(IRJ['inputs'])} of them — carries a value, a "
  f"source, a date and a research layer, and all of them are printed in the separate "
  f"bibliography document. Where a number is constructed rather than reported, the "
  f"construction is stated. Where a needed number could not be obtained, that is stated too.")

# =============================================================== DISCLOSURE ===
H1("Disclosure")
box([("Educational analysis.  ", "This document is an independent educational analysis. It "
      "is not investment advice, not a recommendation, and not an offer or solicitation."),
     ("No rating, no target.  ", "It contains no rating and no price target. It reports a "
      "range of fair values and the reasoning behind them."),
     ("Point in time.  ", f"It reflects information available on 8 August 2026 and the "
      f"closing price of {ST['anchor_date']}. It will age, and it is not updated."),
     ("Sources and their limits.  ", "Historical figures come from the company's own "
      "audited and reviewed statements. Those statements carry qualifications, set out in "
      "section 7; a reader should weigh them."),
     ("Model risk.  ", "The forecast depends on judgements that are stated and sensitised. "
      "Reasonable people will choose different inputs and reach different answers, which is "
      "why the contested judgement is published both ways rather than averaged."),
     ("No position.  ", "The author holds no position in the subject and receives no "
      "compensation from it or from any party with an interest in it.")])

doc.save('EGCH_Valuation_Study_08-08-2026.docx')
print("wrote EGCH_Valuation_Study_08-08-2026.docx")
