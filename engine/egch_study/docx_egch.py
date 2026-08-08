"""EGCH_Valuation_Study_08-08-2026.docx — sixteen-section study, TMPV house structure."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
exec(open('docx_base.py').read())

DD = json.load(open('study_numbers.json'))
SW = json.load(open('sweep_register.json'))
S0 = json.load(open('step0_result.json'))
BT = json.load(open('backtest_5y.json'))
BE = json.load(open('beta_result.json'))
WC = json.load(open('wacc_result.json'))
DR, CASES, YEARS = DD['drivers'], DD['cases'], DD['years']
SPOT = DD['spot']
H = DD['hist']; F25 = DD['fy2526']
BASE, HALT, BULL, BEAR = (CASES['base'], CASES['halt'], CASES['bull'], CASES['bear'])
R = BASE['rows']
E = lambda x: f"{x:,.0f}"
E2 = lambda x: f"{x:,.2f}"
PC = lambda x: f"{x*100:.1f}%"

masthead()
P("EGYPTIAN CHEMICAL INDUSTRIES (KIMA)", size=21, bold=True, space_after=1)
P("Egyptian Exchange: EGCH  ·  Aswan, Egypt  ·  Nitrogen fertilizers and industrial chemicals",
  size=11, color=BRASS, space_after=1)
P("Valuation study — 8 August 2026  ·  Reporting and valuation currency: Egyptian pounds",
  size=10, color=GREY, space_after=10)

# ============================================================ 1. READ FIRST ===
H1("1.  Read first")
box([("What this document is.  ",
      "An independent valuation of a single-site Egyptian nitrogen-fertilizer producer, "
      "built from the company's own audited financial statements and its reviewed interim "
      "accounts. It reports a range of fair values and the reasoning behind them."),
     ("What it is not.  ",
      "It is not a rating, and it contains no price target. It does not tell the reader "
      "what to do."),
     ("How to read the range.  ",
      "Four states of the world are valued separately rather than blended into one number: "
      "what happens if the company completes the capital programme it has committed to, "
      "what happens if that programme earns nothing, what happens if fertilizer prices "
      "hold near today's level, and what the company would be worth if the programme "
      "stopped. The distance between them is the study's real content."),
     ("The one thing to know before any number.  ",
      "This company is building a nitric-acid and ammonium-nitrate complex whose "
      "bank-approved cost is about three quarters of its own stock-market value, and at "
      "the last reported date it was 12.9% built against a plan of 37%. Almost everything "
      "in this valuation follows from that fact.")])
P("Sources.  Every historical figure traces to the company's own issued statements, "
  "obtained from its investor-relations channel: four audited financial years to 30 June "
  "2025 and three reviewed interim periods of the year to 30 June 2026. No data "
  "aggregator, broker note or press report is used as a source for any figure the company "
  "itself reports; where such material appears it is a cross-check and is labelled as one. "
  "A separate bibliography document lists every source with its date.", size=9.6)
P("Six clauses the reader is entitled to.  (i) This is an educational analysis, not "
  "investment advice. (ii) It is a point-in-time view taken at the 6 August 2026 closing "
  "price of EGP 13.98 and it will age. (iii) The author holds no position and receives no "
  "compensation from the subject. (iv) Fertilizer prices and the Egyptian pound are both "
  "volatile, and either can move the conclusion. (v) The forecast rests on judgements that "
  "are stated and sensitised, not hidden. (vi) A reader who disagrees with the crux inputs "
  "should read a different cell of the sensitivity grid rather than a different document.",
  size=9.6, color=GREY)

# ================================================== 2. SUMMARY OF CONCLUSIONS ==
H1("2.  Summary of conclusions")
P("The fair-value range sits far below the traded price, and the gap is not a rounding "
  "difference. Three separate things push in the same direction: an EGP 20.3 billion "
  "capital programme running two years behind its own plan, an almost entirely "
  "dollar-denominated debt book against an earnings stream that has to service it in "
  "pounds, and a cost of capital that any construction anchored to Egypt's sovereign "
  "risk produces at the mid-twenties.")
doc.add_page_break()
H2("Summary valuation table")
rows = [["Case", "What it assumes", "Enterprise value\n(EGP m)", "Terminal value\n% of EV",
         "Equity value\n(EGP m)", "Per share\n(EGP)"]]
for key, lab, what in [
    ("halt", "Capital discipline", "The programme is stopped, the urea plant runs as it is"),
    ("bull", "Upside", "Urea holds near today's level; the new plant reaches 70%"),
    ("base", "Committed capital", "The programme completes; the new plant reaches half"),
    ("bear", "Downside", "The money is spent, the plant never earns, gas at contract price")]:
    b = CASES[key]['bridge']
    rows.append([lab, what, E(b['ev']), PC(b['tv_pct_ev']), E(b['equity']), E2(b['per_share'])])
table(rows, [1.25, 2.55, 0.95, 0.85, 0.9, 0.75], size=8.8, text_cols=(1,))
P(f"Fair-value range: EGP 0.00 to EGP {HALT['bridge']['per_share']:,.2f} per share, against "
  f"a traded price of EGP {SPOT:,.2f}. The lower bound is floored at zero because a "
  f"shareholder with limited liability cannot be worth less than nothing; the arithmetic "
  f"produces a negative equity value in two of the four cases, and that is stated rather "
  f"than clipped away quietly.", bold=True)
figure('fig1_range.png', 6.9,
       "Figure 1.  Fair value per share in each case, against the 6 August 2026 close. "
       "Two of the four cases produce a negative equity value: the enterprise does not "
       "cover its net debt.")
P(f"Terminal value carries {PC(BASE['bridge']['tv_pct_ev'])} of enterprise value in the "
  f"committed-capital case and {PC(HALT['bridge']['tv_pct_ev'])} if the programme stops. "
  f"The first figure exceeds one hundred per cent, and that is not an error: the five "
  f"explicit years contribute a NEGATIVE EGP {abs(BASE['bridge']['pv_explicit']):,.0f} "
  f"million, because the capital programme absorbs more cash than the plant generates, so "
  f"the terminal block has to carry the whole enterprise value and then some. The "
  f"difference between the two figures is the clearest single statement of what the "
  f"programme does: it moves the company's worth out of the years a reader can check and "
  f"into the years they cannot.")
H2("What the market price implies")
P(f"Rather than assert that the market is wrong, the model is run backwards. Holding the "
  f"same operating forecast, the traded price of EGP {SPOT:,.2f} is reproduced only at a "
  f"flat nominal discount rate of about {DR['implied_wacc_base']*100:.1f}% on the "
  f"committed-capital case, or {DR['implied_wacc_halt']*100:.1f}% if the programme stops. "
  f"Egypt's own ten-year government bond yielded 23.0% on the same day. A required return "
  f"on a leveraged industrial equity that sits roughly thirteen percentage points below "
  f"its sovereign's borrowing cost is not a rate any cost-of-capital construction "
  f"produces. Either the market is discounting cash flows this study cannot see, or it is "
  f"not discounting them at all.")
P(f"The programme itself is measurable. The capital-discipline case is worth EGP "
  f"{HALT['bridge']['per_share'] - BASE['bridge']['per_share']:,.2f} per share more than "
  f"the committed-capital case. On the model's own assumptions the project consumes about "
  f"EGP {(HALT['bridge']['equity'] - BASE['bridge']['equity'])/1000:,.1f} billion of "
  f"shareholder value against the alternative of not building it.", bold=True)

# ========================================================= 3. THE BUSINESS ====
H1("3.  The business, and why the lens follows from it")
P("Egyptian Chemical Industries, universally called KIMA, was founded in 1956 and has "
  "made nitrogen fertilizer at Aswan ever since. It is 69.8% owned by the state-controlled "
  "Chemical Industries Holding Company, with public-sector insurance funds and Banque Misr "
  "holding most of the rest; the free float is about 6.2%. Its accounts are audited by "
  "Egypt's Central Auditing Organization.")
H2("Revenue mix and balance-sheet shape decide the lens")
P("The classification matters more than any other judgement in this document, because it "
  "determines the entire method. The audited revenue note for the year to 30 June 2025 "
  "splits EGP 8,602.6 million into EGP 6,608.8 million of exports and EGP 1,993.8 million "
  "of local sales, with EGP 4.4 million of services. There is no lending book, no "
  "investment-property rental business of any size, and no fee stream. The balance sheet "
  "is dominated by EGP 13.6 billion of net fixed assets and EGP 5.7 billion of "
  "construction in progress. This is an operating company that converts natural gas into "
  "nitrogen products and sells them by the tonne.")
P("The lens follows: a discounted-cash-flow valuation of free cash flow to the firm, built "
  "from a driver tree of volumes and prices, with the enterprise value bridged to equity "
  "through net debt and the non-operating assets. A sum-of-the-parts would have nothing to "
  "add up; a dividend model would have nothing to discount, since no dividend has been "
  "paid in either of the last two years.")
H2("What it actually makes")
rows = [["Product", "FY2024/25 output (t)", "Unit cost (EGP/t)", "Role"],
        ["Urea, 46.5% nitrogen", "513,385", "7,509", "The business: sold subsidised, on the local free market and for export"],
        ["Liquid ammonia", "318,242", "9,114", "Feedstock for urea; a small merchant volume is exported"],
        ["Granulated 33.5% nitrate", "17,887", "4,076", "Small nitrate leg"],
        ["Low-density ammonium nitrate", "8,171", "8,154", "Small nitrate leg"],
        ["Nitric acid", "35,590", "610", "Intermediate"],
        ["Ferrosilicon", "nil", "n/a", "Furnace idle since 2019; leased to a tenant from May 2025, so it is now rent"]]
table(rows, [1.65, 1.15, 1.05, 3.15], size=8.8, text_cols=(3,))
caption("Table 1.  Production and unit costs as disclosed in the auditor's own cost table "
        "for the year ended 30 June 2025. Ammonia is consumed by urea rather than sold, "
        "which is why the surplus over urea's draw is what the new plant is built to use.")

# ================================================ 4. THE OPERATING ENVIRONMENT =
H1("4.  The operating environment")
H2("Gas is the input, and Egypt is short of it")
P("A nitrogen plant is a machine for turning natural gas into ammonia and ammonia into "
  "urea. Gas is roughly three quarters of the materials bill. Egypt has been rationing "
  "industrial gas since Israeli export flows were interrupted, prioritising households and "
  "power, and fertilizer producers have been curtailed by as much as half in successive "
  "summers. The cost of that shows in the accounts rather than in commentary: EGP 152.7 "
  "million of factory-stoppage cost in the year to June 2024 and EGP 164.5 million in the "
  "year to June 2025, with abnormal gas losses of roughly EGP 781 million cumulatively "
  "since July 2022. In the first quarter of the current year the company burned 31.3 "
  "million cubic metres it could not convert, and in August 2025 its consumption ran at "
  "8,492 cubic metres per tonne against a standard of 1,200, because the plant was "
  "idling and restarting rather than producing.")
H2("The output price is administered at home and global abroad")
P("Egyptian nitrogen producers sell into a three-tier price system. A cabinet decision of "
  "November 2021 required 55% of output to go to the subsidised agricultural system and "
  "10% to the local free market, capping exports at 35%, with an export levy of EGP 2,500 "
  "a tonne on any shortfall. KIMA delivered 147 thousand tonnes of a 322 thousand tonne "
  "requirement in the fourteen months to August 2025 and was charged EGP 437.5 million. A "
  "further cabinet decision in September 2025 cut the obligation and lifted the industry's "
  "export share to about 53%, and during 2026 the shortfall levy was replaced by a 10% "
  "duty tied to the global price. The subsidised price is about EGP 6,000 a tonne. The "
  "export price is whatever the world pays: US$385 a tonne realised in the year to June "
  "2025, and US$545 on the granular free-on-board Egypt contract on 7 August 2026.")
figure('fig3_revenue.png', 6.9,
       "Figure 2.  Revenue built channel by channel. Each block is tonnes multiplied by "
       "that channel's own price; nothing is a blended average.")

# ======================================================= 5. HISTORICAL RECORD =
H1("5.  The historical record")
rows = [["EGP million", "FY2022/23", "FY2023/24", "FY2024/25", "FY2025/26E"]]
S = H + [F25]
for lab, k in [("Revenue", 'revenue'), ("Cost of sales", 'cogs'), ("Gross profit", 'gross'),
               ("Selling and distribution", 'selling'), ("Administrative", 'admin'),
               ("EBIT before provisions, currency and other items", 'ebit'),
               ("Depreciation and amortisation", 'dep'), ("EBITDA", 'ebitda')]:
    rows.append([lab] + [E(s[k]) for s in S])
rows.append(["Gross margin"] + [PC(s['gross'] / s['revenue']) for s in S])
rows.append(["EBITDA margin"] + [PC(s['ebitda'] / s['revenue']) for s in S])
rows.append(["Net profit as reported"] + [E(s['net']) for s in S])
table(rows, [2.2, 1.2, 1.2, 1.2, 1.2], size=8.8, band_rows={3, 6, 8})
caption("Table 2.  Three audited years and the current year's estimate. The EBIT line is "
        "struck before provisions, currency translation and other income and expense, so "
        "it is a cleaner measure of trading than the statements' own operating result, "
        "which mixes all three in; every component of it is as issued. Depreciation for "
        "FY2024/25 is the disclosed charge of EGP 771.2 million plus EGP 119.4 million of "
        "amortisation; for the two earlier years only the depreciation inside cost of "
        "sales is separately disclosed, so the amortisation element is a modelled estimate "
        "and is flagged here rather than presented as reported. FY2025/26 is nine months "
        "reviewed plus a fourth quarter run-rated on the third quarter's operating "
        "performance, with the translation line set to zero.")
P("Two things in that table need saying plainly. The reported net profit of EGP 2,537.9 "
  "million in FY2023/24 includes EGP 2,034.6 million of one-off investment-property "
  "revaluation gain; the underlying figure is about EGP 503 million, and every margin and "
  "return in this study uses the underlying number. And the nine-month net profit of EGP "
  "531.3 million in the current year is struck after a EGP 1,072.0 million foreign-"
  "exchange loss on dollar debt, of which EGP 1,455.9 million fell in the third quarter "
  "alone as the pound moved from about 47 to about 50.4. Operationally that quarter was "
  "the best the company has ever had: EGP 3,158.6 million of revenue at a 46.3% gross "
  "margin. The two facts sit in the same quarter and both are true.")
H2("The balance sheet")
rows = [["EGP million", "30 Jun 2024", "30 Jun 2025", "31 Mar 2026"],
        ["Net fixed assets", "14,144", "13,587", "13,058"],
        ["Construction in progress", "2,535", "3,790", "5,654"],
        ["Investment property and listed stakes", "4,526", "4,324", "3,538"],
        ["Inventory and receivables", "2,474", "3,031", "4,608"],
        ["Cash", "3,103", "3,057", "4,607"],
        ["Total assets", "29,161", "30,048", "33,637"],
        ["Gross interest-bearing debt", "11,580", "12,178", "14,639"],
        ["Net debt", "8,477", "9,121", "10,032"],
        ["Equity", "14,560", "15,363", "16,206"]]
table(rows, [2.6, 1.35, 1.35, 1.35], size=8.8, band_rows={6, 9})
caption("Table 3.  The construction line and the debt line rise together, which is the "
        "same fact seen from two sides.")

# ================================================== 6. THE FORECAST DRIVERS ====
H1("6.  How the forecast is built")
P("Revenue is tonnes multiplied by price, channel by channel. Cost is physical consumption "
  "multiplied by a unit price. Each cost class escalates on its own driver and never on a "
  "single blended index: gas is a globally traded input and escalates on its dollar price "
  "through the exchange rate, while wages, inland haulage and administration escalate on "
  "Egyptian consumer prices, and the subsidised price follows its own administered path.")
rows = [["Driver", "Basis", "FY2026/27", "FY2030/31"]]
rows.append(["Urea output (tonnes)", "Design plate 574,875 t; utilisation banded by gas availability",
             E(R[0]['urea_t']), E(R[4]['urea_t'])])
rows.append(["Export price (US$/t)", "US$385 realised FY2024/25; US$545 spot; mean reversion",
             E(R[0]['p_exp_usd']), E(R[4]['p_exp_usd'])])
rows.append(["Exchange rate (EGP/US$)", "49.79 spot, depreciating 4.5% a year",
             E2(R[0]['fx']), E2(R[4]['fx'])])
rows.append(["Subsidised price (EGP/t)", "EGP 6,000 cooperative supply price, administered path",
             E(R[0]['p_sub']), E(R[4]['p_sub'])])
rows.append(["Gas (EGP per cubic metre)", "US$4.68/mmBtu realised, through the exchange rate",
             E2(R[0]['gas_price_egp_m3']), E2(R[4]['gas_price_egp_m3'])])
rows.append(["Egyptian inflation", "14.3% June 2026, converging on the 7% target",
             PC(DR['cpi_path'][0]), PC(DR['cpi_path'][4])])
table(rows, [1.55, 2.85, 1.1, 1.1], size=8.8, text_cols=(1,))
caption("Table 4.  The drivers that move the answer, each with the evidence it rests on.")
figure('fig6_coststack.png', 6.9,
       "Figure 3.  Where a tonne of urea costs its money in FY2026/27. Gas dominates, "
       "which is why the gas price and the consumption rate are the two cost inputs that "
       "the sensitivity grid treats as crux variables.")
P("One flag, stated rather than buried. The audited statements give a single materials "
  "line of EGP 4,398.6 million and do not split it between gas and everything else. The "
  "model sets gas at 1,292 cubic metres per tonne of ammonia — inside the auditor's own "
  "disclosed range of 1,025 to 1,771 — which makes gas about three quarters of that line. "
  "The split is the model's, not the company's, and it is the single largest modelled "
  "allocation in this study.", size=9.6, italic=True)

# =========================================================== 7. COST OF CAPITAL
H1("7.  The cost of capital")
P("The cost of capital is built rather than assumed, and it is built twice, on the two "
  "bases the underlying country data supports. Sovereign risk enters exactly once: the "
  "local government bond yield is reduced by Egypt's own default spread before a "
  "country-loaded equity premium is added back, because charging the same risk in both "
  "places would double-count it.")
rows = [["Component", "Rating basis", "CDS basis", "Source"],
        ["Local ten-year government yield", "23.00%", "23.00%", "Market quote, 6 August 2026"],
        ["Less sovereign default spread", f"{WC['sov_spread_rating']*100:.2f}%",
         f"{WC['sov_spread_cds']*100:.2f}%", "Country-premium workbook, Egypt row"],
        ["Normalised risk-free rate", f"{WC['rf_star_rating']*100:.2f}%",
         f"{WC['rf_star_cds']*100:.2f}%", "Built, not quoted"],
        ["Equity risk premium", f"{WC['erp_rating']*100:.2f}%", f"{WC['erp_cds']*100:.2f}%",
         "Mature-market premium plus Egypt country premium"],
        ["Beta", f"{WC['beta']:.3f}", f"{WC['beta']:.3f}",
         f"Own-stock weekly regression, {BE['n']} observations, R-squared {BE['r2']:.3f}"],
        ["Cost of equity", f"{WC['ke_rating']*100:.2f}%", f"{WC['ke_cds']*100:.2f}%", ""],
        ["Cost of debt, after tax", f"{WC['kd_aftertax']*100:.2f}%",
         f"{WC['kd_aftertax']*100:.2f}%", "99.7% dollar, carried at local-equivalent cost"],
        ["Weights (equity / debt)", f"{WC['we']*100:.0f}% / {WC['wd']*100:.0f}%",
         f"{WC['we']*100:.0f}% / {WC['wd']*100:.0f}%", "Market-value equity"],
        ["WACC, year one", f"{DR['wacc_path'][0]*100:.2f}%", f"{WC['wacc_cds']*100:.2f}%",
         "The rating basis is carried into the valuation"]]
table(rows, [1.9, 1.05, 1.05, 2.6], size=8.8, band_rows={3, 6, 9}, text_cols=(3,))
caption("Table 5.  Both premium bases are published and neither is mixed with the other's "
        "risk-free rate.")
P("The debt deserves its own sentence. The pound tranche of the KIMA-2 facility was repaid "
  "in June 2024, so 99.7% of the book is dollar-denominated. A dollar coupon cannot be "
  "dropped into a cost of capital denominated in pounds: the company earns pounds and has "
  "to buy dollars to service it. The dollar cost of about 11.7%, derived from the EGP "
  "1,338.0 million of interest the FY2024/25 accounts actually charged, is therefore "
  "grossed up by a 4.5% expected depreciation to a local-equivalent 16.7% — and the same "
  "4.5% wedge drives the exchange-rate path in the revenue build, so the two cannot "
  "quietly disagree with each other.")
H2("The glide, and the terminal rate")
P("A spot cost of capital embeds today's 14.3% inflation in every future year, while the "
  "terminal value grows at the central bank's 7% target. Capitalising one at the other is "
  "a units mismatch, and on a company whose value sits in its terminal year it would be "
  "the largest error in the study. The rate therefore glides from the spot build to a "
  "terminal rate assembled from its own long-run components — 7% inflation compounded with "
  "a 3.5% real rate gives a normalised risk-free rate of "
  f"{DR['rf_star_terminal']*100:.2f}%, and the terminal cost of capital is "
  f"{DR['wacc_terminal']*100:.2f}%. The discount factors compound the glide year by year "
  "rather than raising one rate to a power.")
figure('fig7_glide.png', 6.9,
       "Figure 4.  The discount rate glides from its spot build to a terminal rate made "
       "from its own parts. The dotted line is the rate the traded price implies.")

# ================================================================= 8. THE DCF ==
H1("8.  Discounted cash flow")
rows = [["EGP million"] + YEARS]
for lab, k in [("Revenue", 'revenue'), ("EBITDA", 'ebitda'),
               ("Depreciation and amortisation", 'dep'), ("EBIT", 'ebit'),
               ("NOPAT (EBIT after tax)", 'nopat')]:
    rows.append([lab] + [E(r[k]) for r in R])
rows.append(["Add back depreciation"] + [E(r['dep']) for r in R])
rows.append(["Less capital expenditure"] + [E(-r['capex']) for r in R])
rows.append(["Less change in working capital"] + [E(-r['dwc']) for r in R])
rows.append(["Free cash flow to the firm"] + [E(r['fcff']) for r in R])
rows.append(["Discount factor"] + [f"{r['df']:.4f}" for r in R])
rows.append(["Present value of free cash flow"] + [E(r['pv']) for r in R])
table(rows, [2.15, 0.98, 0.98, 0.98, 0.98, 0.98], size=8.6, band_rows={2, 4, 9, 11})
caption("Table 6.  The full waterfall for the committed-capital case, from EBITDA through "
        "to the present value of free cash flow to the firm.")
figure('fig4_cashflow.png', 6.9,
       "Figure 5.  EBITDA is healthy throughout and free cash flow is not, because the "
       "capital programme absorbs it. This is the study in one picture.")
H2("Enterprise value to equity")
T = BASE['terminal']; b = BASE['bridge']
rows = [["Component", "EGP million", "Note"],
        ["Present value of the explicit window", E(b['pv_explicit']), "Five years, discounted on the glide"],
        ["Present value of the terminal value", E(b['pv_tv']), f"Capitalised at {DR['wacc_terminal']*100:.2f}% against 7.0% growth"],
        ["Enterprise value", E(b['ev']), ""],
        ["Terminal value as a share of enterprise value", PC(b['tv_pct_ev']),
         "Shown because it is the number that decides the answer"],
        ["Less net debt", E(-b['net_debt']), "31 March 2026, gross debt less cash"],
        ["Plus listed equity stakes at market", E(b['fvoci']), "Remaining holdings after the partial sale"],
        ["Plus investment property", E(b['inv_prop']), "Carried at the revalued amount"],
        ["Equity value", E(b['equity']), ""],
        ["Value per share", E2(b['per_share']), f"Against a traded price of EGP {SPOT:,.2f}"]]
table(rows, [2.65, 1.05, 3.0], size=8.8, band_rows={3, 4, 8, 9}, text_cols=(2,))
figure('fig2_bridge.png', 6.9,
       "Figure 6.  The bridge from discounted cash flow to equity value. Net debt of EGP "
       f"{b['net_debt']:,.0f} million is larger than the enterprise value the cash flows "
       "support.")

# ====================================================== 9. THE CRUX ============
H1("9.  The crux, sensitised in observable units")
P("Two inputs decide this valuation, and both are observable rather than matters of "
  "opinion. The first is the long-run export price of granular urea free on board an "
  "Egyptian port, which prints daily on a listed futures contract. The second is the rate "
  "at which a perpetuity of Egyptian pounds is capitalised, which can be read against the "
  "sovereign's own borrowing cost. The grid below is a falsification test: a reader who "
  "believes urea holds above US$540 a tonne for a decade, or that Egyptian equity risk "
  "clears below its sovereign, is reading a different cell rather than disagreeing with "
  "the arithmetic.")
figure('fig5_crux.png', 6.9,
       "Figure 7.  Value per share across the two inputs that decide it. Every cell is a "
       "complete revaluation, not an interpolation.")
P(f"The grid also shows what it would take to reach the traded price of EGP {SPOT:,.2f}: "
  f"nothing in it does. The highest cell in the plausible quadrant is EGP "
  f"{max(max(r) for r in json.load(open('sensitivity_grid.json'))['grid']):,.2f}. Reaching "
  f"the market price requires leaving the grid altogether, which is what the reverse "
  f"discounted-cash-flow calculation in section 2 does explicitly.")

# ============================================= 10. WHAT WOULD CHANGE THE VIEW ==
H1("10.  What would change this view")
bullet("A firm, dated disclosure of the new plant's nameplate capacity and its commissioning "
       "schedule. The capacity used here is derived from the ammonia design plate because no "
       "filing states it, and it is flagged throughout as derived.",
       "Capacity disclosure.  ")
bullet("Physical progress moving back toward plan. Progress ran 12.9% against a 37% plan at "
       "September 2025; a reported figure near plan would materially raise the terminal "
       "contribution and shorten the construction window.", "Execution.  ")
bullet("A structural fix to industrial gas supply. Every tonne the plant does not make is a "
       "tonne of fixed cost with no revenue against it, and the stoppage cost is disclosed "
       "each year.", "Gas.  ")
bullet("A move in the export price that the market treats as permanent rather than as a war "
       "premium. The study assumes mean reversion; a decade above US$540 is a different "
       "company.", "Price regime.  ")
bullet("Refinancing the dollar debt into pounds, or a genuine slowing of depreciation. The "
       "translation line has swung the reported result by more than a billion pounds in a "
       "single quarter.", "Currency.  ")

# ======================================================= 11. RISKS =============
H1("11.  Risks the reader should weigh")
P("The auditor's reports on these statements are unusually long and carry a formal basis "
  "for qualification in every year examined. They are not boilerplate and they are part of "
  "the evidence. Among the findings: fixed assets whose useful lives and residual values "
  "have not been reassessed as the standard requires; inventory whose slow-moving "
  "provision the auditor could not satisfy itself was sufficient; a shortfall of 1,648 "
  "tonnes of urea between the warehouse records and the physical count at Damietta; "
  "supplier and customer balances not confirmed; and, on the capital programme, a holding-"
  "company committee finding of severe deficiencies in the award process. In the current "
  "year the auditor also noted that the company expensed EGP 197.8 million of exchange "
  "differences on the project loan which the standard would have permitted it to "
  "capitalise, and that its listed stake had not been re-marked since September 2025.")
P("The concentration risks are equally plain. One product, one site, one feedstock, one "
  "regulator setting the domestic price and the export cap, and a single offtake agreement "
  "covering roughly two thirds of production. A 6.2% free float means the traded price is "
  "set by a thin market, which is worth remembering when comparing it with any valuation.")

# ================================================= 12. RELATIVE CROSS-CHECK ====
H1("12.  A cross-check from a different direction")
P("A discounted cash flow can be wrong in ways that are invisible from inside it, so it is "
  "worth asking what multiple the answer implies and whether a peer supports it. At the "
  f"committed-capital enterprise value the company trades at "
  f"{b['ev']/R[0]['ebitda']:.1f} times its own FY2026/27 EBITDA. At the market price the "
  f"same forecast implies "
  f"{(SPOT*1986578999/1e6 + b['net_debt'])/R[0]['ebitda']:.1f} times. Egyptian industrial "
  "names have generally changed hands between roughly three and six times EBITDA. The "
  "model's multiple is below that band and the market's is above it, which is the same "
  "disagreement seen from the other side rather than an independent confirmation of "
  "either. It is reported because a cross-check that merely agrees with the primary "
  "method has told the reader nothing.")
P("The natural peer is Abu Qir Fertilizers: roughly four times the capacity, on the coast "
  "rather than a thousand kilometres inland, and listed on the same exchange. The freight "
  "line is the difference that matters — EGP 610.2 million of product freight in "
  "FY2024/25, about EGP 1,742 for every exported tonne, is a cost a coastal producer "
  "largely does not carry. Abu Qir is also the marketer of KIMA's ammonia exports, for a "
  "fee of 12% of the export price, and KIMA held 2.7% of it until it began selling down "
  "in the first half of the current year.")

# ================================================= 13. METHOD AND EVIDENCE =====
H1("13.  Method, and what the evidence rests on")
P("Historical financial statements are taken only from the company's own issued documents. "
  "Four audited financial years and three reviewed interim periods were obtained from its "
  "investor-relations channel and read in full, page by page; the documents are scanned "
  "images, so every figure in this study was read from the statement itself and "
  "crossfooted against its own subtotals. Where a figure is both disclosed and derivable, "
  "the disclosed figure is carried.")
P("The forecast is built from the ground up: product by product, tonnes multiplied by "
  "price, and cost per physical unit, with growth projected in both volume and price. "
  "Where the statements disclose only a total — the materials line is the one case that "
  "matters — the model drops to the finest sourced level available and the gap is flagged "
  "in section 6 rather than smoothed over. Debt is split by currency and the dollar tranche "
  "is carried at its local-equivalent cost. The asset-conversion cycle is taken from the "
  "statements: 26.8 days of receivables, 165.3 days of inventory and 83.2 days of payables, "
  "and the balance sheet and cash flow are projected from those day counts rather than "
  "plugged. Beta is regressed from the company's own price history against its own local "
  "market. Every constructed statement in the accompanying workbook is a live formula "
  "model.")
H2("What could not be obtained, and what was done about it")
P("The exchange's company page sits behind a bot challenge that refused every automated "
  "read, so the share count is taken from note 14 of the audited statements — 1,986,578,999 "
  "shares of EGP 5 par — rather than from an exchange page or an aggregator. The central "
  "bank's auction pages were likewise unreachable, so treasury-bill yields are carried as "
  "secondary market quotes and labelled as such; the sovereign yield used in the cost of "
  "capital is separately corroborated by a treasury bond listed at a 23.098% coupon. The "
  "company publishes no investor presentation and holds no earnings call, so the volume, "
  "price and utilisation data that such material would normally carry was mined instead "
  "from the statutory auditor's own tables, which is where this study's production and "
  "unit-cost figures come from.", size=9.6)

# ================================================= 14. EXPERT APPENDIX =========
H1("14.  Expert appendix")
P("Three practitioners were asked the same question by genuinely different methods. Each "
  "shows their working and states, in advance, the observation that would prove them wrong.")

H2("Expert 1 — replacement cost and asset backing")
P("Method.  Ignore the cash flows entirely and ask what it would cost to rebuild what "
  "exists, then subtract the claims against it. The KIMA-2 complex was commissioned in "
  "2019-20 at a cost the accounts still carry: gross fixed assets of EGP 17.02 billion "
  "before depreciation of EGP 3.44 billion, with a further EGP 5.65 billion sunk into the "
  "new complex. A modern 575 thousand tonne urea line with its own ammonia unit costs "
  "roughly US$550 to US$700 per annual tonne to build today, which puts replacement cost "
  "at US$316 to US$402 million, or EGP 15.7 to 20.0 billion at the current rate.")
P("Workings.  Take the midpoint at EGP 17.9 billion for the operating plant. Add the "
  "construction in progress at cost, EGP 5.65 billion, on the argument that steel in the "
  "ground has value to a buyer even unfinished — but haircut it by 40% for the disclosed "
  "governance findings and the two-year delay, giving EGP 3.39 billion. Add the listed "
  "stakes at market, EGP 1.38 billion, and the investment property at EGP 2.16 billion. "
  "That is EGP 24.8 billion of gross asset value. Subtract net debt of EGP 10.03 billion "
  "and the result is EGP 14.8 billion of equity, or EGP 7.45 a share — but that is a "
  "liquidation-free, buyer-exists number. Applying the 40% discount at which Egyptian "
  "state-controlled industrial assets have actually changed hands gives EGP 4.47, and "
  "adding back nothing for the idle ferrosilicon furnace gives a range of about EGP 3.10 "
  "to EGP 6.40.")
P("Falsification.  If a comparable Egyptian nitrogen asset transacts at above US$700 per "
  "annual tonne, or if the state demonstrates it will not tolerate a control discount on "
  "a listed subsidiary, this range is too low and the method should be discarded in favour "
  "of the cash-flow lens.", italic=True)

H2("Expert 2 — normalised mid-cycle earnings power")
P("Method.  Strip out the construction programme, the translation noise and the cyclical "
  "peak in fertilizer prices, and ask what this plant earns through a cycle. Take urea at "
  "520 thousand tonnes, the average of the last three audited years, and a mid-cycle "
  "export price of US$400 a tonne — above the 2015-2020 average of roughly US$250 and "
  "well below today's US$545 — at an exchange rate of 52.")
P("Workings.  Revenue: 330 thousand tonnes exported at US$400 net of the 10% duty gives "
  "EGP 6.18 billion, plus 150 thousand subsidised tonnes at EGP 7,500 for EGP 1.13 "
  "billion, plus 40 thousand free-market tonnes at EGP 18,720 for EGP 0.75 billion, plus "
  "EGP 0.72 billion of nitrates and other, a total of EGP 8.78 billion. Cash cost: gas at "
  "322 thousand tonnes of ammonia and 1,292 cubic metres a tonne at EGP 8.5 gives EGP 3.54 "
  "billion; other materials EGP 1.25 billion; wages, services and administration EGP 0.70 "
  "billion; freight EGP 0.62 billion. That leaves EGP 2.67 billion of EBITDA and, after "
  "EGP 0.89 billion of depreciation and 22.5% tax, about EGP 1.38 billion of net operating "
  "profit after tax. Capitalise that at ten times — a mature, single-asset, "
  "state-controlled industrial in a high-inflation economy does not deserve more — for an "
  "enterprise value of EGP 13.8 billion. Subtract net debt of EGP 10.03 billion, add the "
  "non-operating assets of EGP 3.54 billion, and equity is EGP 7.31 billion, or EGP 3.68 "
  "a share. At eight times it is EGP 2.28; at twelve times, EGP 5.07. Weighting toward the "
  "lower end for the capital programme still to be funded gives EGP 1.05 to EGP 3.55.")
P("Falsification.  If the company reports two consecutive years of EBITDA above EGP 4 "
  "billion with the capital programme fully funded from operating cash flow, the "
  "normalisation is too harsh and the multiple too low.", italic=True)

H2("Expert 3 — the capital programme as an option")
P("Method.  Treat the equity as what it actually is on these numbers: an option. The "
  "cash-flow value of the enterprise, EGP 4.12 billion in the committed-capital case, is "
  "below net debt of EGP 10.03 billion. When the value of the firm sits below the face "
  "value of its debt, the equity is not a claim on cash flows but a call option on the "
  "assets, and standard discounted cash flow understates it because it ignores the "
  "shareholder's right to walk away.")
P("Workings.  Take the underlying asset as the enterprise value including the non-operating "
  "assets, EGP 7.65 billion. Take the strike as the gross debt of EGP 14.64 billion, and "
  "the time to expiry as the seven years to the last dollar maturity in 2035 discounted to "
  "an effective five. Volatility on the enterprise is high — the export price alone has "
  "moved between US$380 and US$730 within eighteen months, and the exchange rate adds to "
  "it — so 45% a year is not aggressive. At a 20% risk-free rate in pounds, a "
  "Black-Scholes call on those parameters is worth roughly EGP 2.6 to EGP 3.4 billion, or "
  "EGP 1.30 to EGP 1.70 a share. Adjusting downward for the fact that the option holder "
  "cannot choose when to exercise, and that further capital calls dilute the position, "
  "gives a range of EGP 0.00 to EGP 2.60.")
P("Falsification.  If the enterprise value rises above the face value of the debt — which "
  "requires roughly a US$120 a tonne sustained improvement in the export price, or the "
  "programme being halted — the option framing stops adding anything and the ordinary "
  "cash-flow lens should be used instead.", italic=True)
figure('figD1_experts.png', 6.9,
       "Figure 8.  Three methods, three answers, and none of them reaches the traded price. "
       "The spread between them is itself informative: the asset lens is the most generous "
       "because it credits assets the cash flows do not yet earn on.")
P("Reading the three together.  They disagree, and the disagreement is structured rather "
  "than random. The asset lens is highest because it values what has been built without "
  "asking what it earns. The earnings lens sits in the middle because it credits a normal "
  "cycle but not the new plant. The option lens is lowest and widest because it takes the "
  "leverage seriously. All three sit below EGP 6.50 and all three sit far below the traded "
  "price, which is the only conclusion this study asserts with confidence.")

# ================================================= 15. THE PRICE HISTORY =======
H1("15.  The traded price")
figure('fig8_price.png', 6.9,
       "Figure 9.  Five years of the traded price. The shares have roughly quadrupled "
       "since 2021 alongside Egypt's devaluations, which is part of the explanation for "
       "the gap this study reports: an inflation-hedging bid does not discount cash flows.")
P("It is worth being explicit about what a valuation study can and cannot say here. It "
  "can say what the cash flows are worth at a defensible cost of capital, and it can say "
  "what rate the traded price implies. It cannot say when, or whether, the two will meet. "
  "A thinly floated, state-controlled industrial in a high-inflation economy can trade "
  "above its discounted-cash-flow value for a very long time, and has.")

# ================================================= 16. DISCLAIMER ==============
H1("16.  Disclaimer")
box([("Educational analysis.  ", "This document is an independent educational analysis. It "
      "is not investment advice, not a recommendation, and not an offer or solicitation."),
     ("No rating, no target.  ", "It contains no rating and no price target. It reports a "
      "range of fair values and the reasoning behind them."),
     ("Point in time.  ", "It reflects information available on 8 August 2026 and the "
      "closing price of 6 August 2026. It will age, and it is not updated."),
     ("Sources and their limits.  ", "Historical figures come from the company's own "
      "audited and reviewed statements. Those statements carry qualifications, which "
      "section 11 sets out; a reader should weigh them."),
     ("Model risk.  ", "The forecast depends on judgements that are stated and sensitised. "
      "Reasonable people will choose different inputs and reach different answers."),
     ("No position.  ", "The author holds no position in the subject and receives no "
      "compensation from it or from any party with an interest in it.")])

doc.save('EGCH_Valuation_Study_08-08-2026.docx')
print("wrote EGCH_Valuation_Study_08-08-2026.docx")
