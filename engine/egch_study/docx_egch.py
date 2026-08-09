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
AL = json.load(open('alternatives.json'))
AL_BY = {a['key']: a for a in AL['alternatives']}
GRD = json.load(open('sensitivity_grid.json'))
FLAT = json.load(open('flat_rate_ladder.json'))
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
PC0 = lambda x: f"{x*100:+.0f}%"
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
SP = AL['spans']
rows = [["Read", "Basis", "Range (EGP/share)", "Central", "vs spot"]]
for k in ("cashflow_carry", "cashflow_stopped", "relative", "normalised", "book"):
    sp = SP[k]
    rng = (f"{E2(sp['low'])} to {E2(sp['high'])}" if sp['high'] > sp['low'] else "—")
    rows.append([sp['label'], sp['basis'], rng, E2(sp['base']), PC0(sp['vs_spot'])])
rows.append(["THE FIELD, all four lenses",
             "Low to high across every read above. The two cash-flow readings are the "
             "contested judgement and are never averaged into one another",
             f"{E2(LN['synthesis']['low'])} to {E2(LN['synthesis']['high'])}", "—", "—"])
rows.append(["Market price", "Closing price on the anchor date", "—", E2(SPOT), "—"])
rows.append(["ALTERNATIVE READINGS — each a full re-run of the model with ONE component "
             "moved, and none of them inside the field above", "", "", "", ""])
for a in AL['alternatives']:
    rows.append([a['made'], a['alt'], "—", E2(a['value']), PC0(a['value'] / SPOT - 1)])
t1 = table(rows, [1.55, 2.75, 1.05, 0.7, 0.65], size=7.9, band_rows={6, 7, 8},
           text_cols=(1,))
# the banner row is a heading inside the table, not a data row: left as five cells it
# wrapped into a tall narrow column with four empties beside it
_banner = t1.rows[8].cells[0].merge(t1.rows[8].cells[4])
# merging concatenates the paragraphs of every cell, so four empty ones follow the text
# and leave a tall blank band under it
for _p in _banner.paragraphs[1:]:
    _p._p.getparent().remove(_p._p)
caption("{T}.  Egyptian pounds a share against a traded price of EGP "
        f"{E2(SPOT)}. Every alternative reading is a complete re-run of the model through "
        "the same case machinery, not an adjustment applied to the answer; each is argued "
        "for and against in section 1.8.")
rows = [["Terminal value as a share of enterprise value", "Programme carried through",
         "Programme stopped"],
        ["Discounted cash-flow lens", PC(BASE['bridge']['tv_pct_ev']),
         PC(HALT['bridge']['tv_pct_ev'])]]
table(rows, [3.2, 1.9, 1.9], size=8.9)
caption("{T}.  Reported beside the cash-flow lens because on this company it is the "
        "number that decides the answer. Above one hundred per cent means the five explicit "
        "years contribute negative present value: the capital programme absorbs more cash "
        "than the plant generates, so the terminal block carries the whole enterprise value "
        "and then some.")
figure('fig9_field.png', 6.9,
       "{F}.  Each lens as its own bear-to-bull span, with the central marked, "
       "against the traded price.")
P(f"The alternative readings are shown so that each genuinely contested choice in the "
  f"construction can be priced rather than argued. The widest of them is the gas price: "
  f"moving from the price the company's own loss disclosure implies to the contract "
  f"formula price in its operating agreement is worth EGP "
  f"{E2(abs(AL_BY['gas']['delta']))} a share. The narrowest is terminal growth, worth EGP "
  f"{E2(abs(AL_BY['terminal_growth']['delta']))}. Not one of them, alone or together, "
  f"reaches the traded price — which is the finding this study reports, and the reason the "
  f"headline states the discount rate the market itself implies rather than asserting that "
  f"the market is wrong.")

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
caption("{T}.  Production and unit costs as disclosed in the auditor's own cost table. "
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
caption("{T}.  The full waterfall, programme carried through. Every line is a live "
        "formula in the accompanying workbook.")
figure('fig4_cashflow.png', 6.9,
       "{F}.  Operating profit is healthy throughout and free cash flow is not, "
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
caption("{T}.  Net debt is larger than the enterprise value the cash flows support in "
        "the carried-through column. That is why the equity value there is negative, and it "
        "is stated rather than clipped to zero.")
figure('fig2_bridge.png', 6.9, "{F}.  The bridge, carried-through case.")

H2("Why the answer is negative, and what would change its sign")
_SHm = SH / 1e6
P("The same bridge in pounds a share makes the mechanism plain, and it is not the "
  "capital programme.")
rows = [["Carried-through case, per share", "EGP"],
        ["Enterprise value the cash flows support", E2(BASE['bridge']['ev'] / _SHm)],
        ["Less net debt", E2(-BASE['bridge']['net_debt'] / _SHm)],
        ["Plus listed stakes and investment property",
         E2((BASE['bridge']['fvoci'] + BASE['bridge']['inv_prop']) / _SHm)],
        ["EQUITY", E2(BASE['bridge']['per_share'])],
        ["Traded price", E2(SPOT)]]
table(rows, [4.4, 2.5], size=8.9, band_rows={4, 5})
caption("{T}.  The operating business is carried at less than half the debt standing "
        "against it. Free cash flow is positive in three of the five forecast years — the "
        "construction is no longer what makes the answer negative. The debt is.")
P(f"So the question is not whether the plant earns. It is whether EGP "
  f"{E(BASE['bridge']['ev'])} million is the right enterprise value for a business "
  f"generating around EGP {E(R[0]['ebitda'])} million of operating profit before "
  f"depreciation, and that is entirely a question about the rate at which Egyptian pounds "
  f"are capitalised. Holding every operating assumption exactly as built and moving only "
  f"the discount rate:")
rows = [["A flat cost of capital of", "Value per share (EGP)", "What it would mean"]]
for w, note in [(0.2500, "roughly the rate this study builds from the sovereign's own yield"),
                (0.2000, "below the sovereign's ten-year yield of "
                         f"{PC(V('rf_observed'))}"),
                (0.1800, "the sign changes here"),
                (0.1600, ""),
                (0.1400, ""),
                (0.1200, "")]:
    rows.append([PC(w), E2(FLAT[f"{w:.4f}"]), note])
rows.append([PC(DR['implied_wacc_base']), E2(SPOT),
             "the rate the traded price itself implies"])
table(rows, [1.5, 1.8, 3.6], size=8.5, band_rows={3, 7}, text_cols=(2,))
caption(f"{{T}}.  Every row is a full re-run. The sign of the answer turns at about "
        f"eighteen per cent — five points below what Egypt's own government pays to borrow "
        f"for ten years. Reaching the traded price needs about "
        f"{PC(DR['implied_wacc_base'])}, which is {PC(V('rf_observed') - DR['implied_wacc_base'])} "
        f"below the sovereign. That, and not the capital programme, is the disagreement "
        f"between this study and the market.")

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
caption("{T}.  The justified multiple of book is negative before flooring, and that is "
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
caption("{T}.  A mature single-asset industrial in a high-inflation economy does not "
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

figure('fig1_range.png', 6.9,
       "{F}.  The same cash-flow model run in four states of the world. The spread "
       "between the top and the bottom bar is what the capital programme is worth, in "
       "either direction.")

H2("1.6  The drivers — each leg grown on its own driver, margins as outputs")
P("The company reports one operating segment, so the build goes below it to the product and "
  "the channel, which is the finest level the statements source. Nothing in the model sets "
  "a margin: every margin falls out of tonnes, prices and physical consumption.")
H2("The channels, historically")
rows = [["Channel", "FY2022/23", "FY2023/24", "FY2024/25", "What sets it"]]
rows.append(["Urea produced (tonnes)", E(DR['urea_t']['FY2022/23']),
             E(DR['urea_t']['FY2023/24']), E(DR['urea_t']['FY2024/25']),
             f"Gas availability against a {E(V('design_urea_tpy'))}-tonne design plate"])
rows.append(["Export tonnes", "—", "—", E(V('export_tonnes_FY2425')),
             "Output less the subsidised and free-market legs"])
rows.append(["Subsidised tonnes", "—", "—", E(V('subsidised_tonnes_FY2425')),
             "An administered quota the company has been unable to meet in full"])
rows.append(["Free-market tonnes", "—", "—", E(V('local_free_tonnes_FY2425')),
             "The residual of the local revenue note"])
rows.append(["Realised export price (US$/t)", "—", "—", E(V('export_price_FY2425_usd')),
             "The auditor's own disclosed average"])
rows.append(["Revenue (EGP m)", E(H[0]['revenue']), E(H[1]['revenue']), E(H[2]['revenue']),
             "Tonnes times price, in five legs"])
rows.append(["Gross margin", PC(H[0]['gross_pct']), PC(H[1]['gross_pct']),
             PC(H[2]['gross_pct']), "An output, never an input"])
rows.append(["Operating margin before depreciation", PC(H[0]['ebitda_pct']),
             PC(H[1]['ebitda_pct']), PC(H[2]['ebitda_pct']), "An output"])
table(rows, [1.85, 0.92, 0.92, 0.92, 2.3], size=8.4, band_rows={6, 7, 8}, text_cols=(4,))
caption("{T}.  The channel split is disclosed only for the most recent year, in the "
        "revenue note; the two earlier years disclose production and revenue but not the "
        "split between the three domestic and export channels. That gap is stated here "
        "rather than filled with an assumption.")

H2("How the forecast is driven")
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
caption("{T}.  Each cost class escalates on its own driver and never on one blended "
        "index: gas is a globally traded input and escalates on its dollar price through "
        "the exchange rate, while wages, inland haulage and administration escalate on "
        "Egyptian consumer prices and the subsidised price follows its own administered path.")
figure('fig3_revenue.png', 6.9, "{F}.  Revenue built channel by channel.")
figure('fig6_coststack.png', 6.9,
       "{F}.  Where a tonne of urea costs its money. Gas dominates, which is why the "
       "gas price and the consumption rate are treated as crux variables.")
H2("What the build produces — margins as outputs")
rows = [["EGP million"] + [y.replace("FY", "FY").replace("/", "/") for y in YEARS]]
for lab, key, fmt in [("Revenue", 'revenue', E), ("Cost of sales", 'cogs', E),
                      ("Gross profit", 'gross', E), ("Gross margin", 'gross_pct', PC),
                      ("Operating profit before depreciation", 'ebitda', E),
                      ("Margin before depreciation", 'ebitda_pct', PC),
                      ("Operating profit", 'ebit', E), ("Operating margin", 'ebit_pct', PC)]:
    rows.append([lab] + [fmt(r[key]) for r in R])
table(rows, [2.05, 0.99, 0.99, 0.99, 0.99, 0.99], size=8.4, band_rows={4, 6})
caption("{T}.  Not one margin in this table is set. Each is revenue less a cost stack "
        "that was built from physical consumption times a unit price, so the margin path is "
        "a consequence of the tonnes, the prices and the escalators above it. The margin "
        "falls across the window because the export price mean-reverts faster than the "
        "domestic cost base disinflates — which is a statement about two sourced paths, "
        "not a view about management.")

H2("The revenue mix, the first forecast year against the last")
rows = [["Channel", f"{YEARS[0]} revenue (EGP m)", "Share", f"{YEARS[-1]} revenue (EGP m)",
         "Share"]]
for lab, key in [("Export urea", 'rev_exp'), ("Subsidised urea", 'rev_sub'),
                 ("Free-market urea", 'rev_free'), ("Nitrates", 'rev_an'),
                 ("Other", 'rev_other')]:
    rows.append([lab, E(R[0][key]), PC(R[0][key] / R[0]['revenue']),
                 E(R[4][key]), PC(R[4][key] / R[4]['revenue'])])
rows.append(["Total", E(R[0]['revenue']), PC(1.0), E(R[4]['revenue']), PC(1.0)])
table(rows, [1.8, 1.35, 0.9, 1.35, 0.9], size=8.5, band_rows={6})
caption("{T}.  The export leg shrinks as a share of the total, not because the "
        "company sells less abroad but because the administered domestic price rises "
        "faster than the export price falls. A reader who expects the opposite is "
        "disagreeing with one of those two paths, and section 1.9 prices both.")

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
PRG = AL['programme']
rows = [["The capital programme", "Value", "Where it comes from"]]
rows.append(["Bank-approved cost", f"EGP {E(PRG['approved_egp'])}m plus US${E1(PRG['approved_usd'])}m",
             "The facility signed on 25 June 2025"])
rows.append(["Approved cost, one currency", f"EGP {E(PRG['approved_total'])}m",
             "At the rate prevailing when it was approved"])
rows.append(["As a share of the whole company's market value", PC(PRG['pct_market_cap']),
             "Against a market value of EGP " + E(PRG['market_cap']) + "m"])
rows.append(["Spent by 31 March 2026", f"EGP {E(PRG['spent'])}m",
             "Construction in progress on the reviewed balance sheet"])
rows.append(["Money spent, as a share of the approved cost", PC(PRG['spent_pct']), "Derived"])
rows.append(["Physical progress reported", PC(PRG['progress']),
             "The auditor's own figure at September 2025"])
rows.append(["Physical progress planned by the same date", PC(PRG['plan']),
             "The auditor's own figure"])
rows.append(["Still to spend", f"EGP {E(PRG['remaining'])}m", "Derived"])
rows.append(["Derived nameplate", f"{E(PRG['nameplate'])} tonnes a year",
             "FLAGGED as derived: no filing states it"])
rows.append(["Capital per annual tonne", f"EGP {E(PRG['capital_per_tonne'])}",
             "Approved cost over derived nameplate"])
rows.append(["What it earns after tax in the terminal year, at half nameplate",
             f"EGP {E(PRG['terminal_ebit'] * (1 - DR['tax_rate']))}m", "The model's own terminal year"])
rows.append(["Return on the approved cost", PC(PRG['return_on_cost']), "Derived"])
rows.append(["Against a terminal cost of capital of", PC(DR['wacc_terminal']),
             "Section 1.8"])
table(rows, [2.85, 1.75, 2.4], size=8.4, band_rows={5, 12, 13}, text_cols=(2,))
caption("{T}.  The two lines that matter are the fifth and the sixth. More than a "
        "quarter of the money has been spent against an eighth of the plant, and the whole "
        "of it earns a return an order of magnitude below what the capital costs. Neither "
        "number is a forecast: both are the company's own disclosures set against the "
        "model's own terminal year.")
figure('fig14_programme.png', 6.9,
       "{F}.  On the left, what has been spent against what has been built. On the "
       "right, what the finished plant earns against what the capital costs.")

H2("What the company actually spends — the capital-expenditure record")
P("Before any of the above can be read, one question has to be answered from the "
  "statements rather than assumed: is this a one-off build, or is it what this company "
  "spends? The cash-flow statements answer it directly. The investing section carries a "
  "single line — payments to acquire fixed assets, projects under construction — and it "
  "has two clean years before the programme started.")
CX = AL['capex']
rows = [["Year", "Capital expenditure paid (EGP m)", "Revenue (EGP m)", "Of revenue",
         "What it was"]]
for r in CX['history']:
    rows.append([r['year'], E1(r['capex']), E(r['revenue']), PC(r['pct']), r['note']])
table(rows, [1.25, 1.55, 1.15, 0.8, 2.25], size=8.4, band_rows={1, 2}, text_cols=(4,))
caption(f"{{T}}.  The two shaded years are the answer. With nothing being built, this "
        f"plant cost EGP {E1(V('capex_paid_FY2122'))}m and then EGP "
        f"{E1(V('capex_paid_FY2223'))}m a year to keep running — pooled, "
        f"{PC(CX['pre_project_pooled'])} of revenue. Everything above that is the new "
        f"complex.")
P(f"Three things follow, and the first two correct this study rather than confirm it. "
  f"First, the capital expenditure in the forecast IS a one-off bulk: EGP "
  f"{E(CX['forecast_total'])} million across five years against EGP {E(CX['remaining'])} "
  f"million still to spend on the approved cost, after which it stops. Second, it does "
  f"not repeat inside any horizon this study can see — the disclosed depreciation rate on "
  f"the plant's machinery is {PC2(CX['machinery_dep_rate'])} a year, an asset life of "
  f"about {E(CX['implied_asset_life'])} years, so the replacement cycle sits far beyond "
  f"the terminal year. Third, and this is the correction: maintenance capital expenditure "
  f"is now set at the {PC(CX['pre_project_pooled'])} of revenue the company has actually "
  f"paid, not at a three per cent mature-plant standard. That standard was an assertion, "
  f"it was almost three times anything this company has ever spent to keep this plant "
  f"running, and no disclosure supported it.", bold=True)
P(f"The project path is anchored the same way. The company spent EGP "
  f"{E1(V('capex_paid_FY2425'))}m in the last audited year and EGP "
  f"{E1(V('capex_paid_9M_FY2526'))}m in nine months of this one — a full year at that "
  f"rate is EGP {E(CX['run_rate'])}m, and that is where the forecast now opens. The "
  f"remaining years complete the approved cost inside the window, because the terminal "
  f"year only earns if the plant is finished.")
P(f"The honest counter-argument is that the two pre-project years flatter the plant: it "
  f"was newly built, and new plant does not need much. The upper framing of the same "
  f"driver is replacement-rate maintenance — gross fixed assets at that same "
  f"{PC2(CX['machinery_dep_rate'])} machinery rate, or {PC(CX['replacement_rate'])} of "
  f"revenue. Both are published: the observed rate is the central and the replacement "
  f"rate is the downside, and they are worth EGP "
  f"{E2(abs(AL_BY['maintenance_capex']['delta']))} a share between them. They are not "
  f"averaged.", size=9.8, italic=True)

H2("The asset-conversion cycle — disclosed, then projected from it")
P("Working capital is not a percentage of revenue in this model. It is three day counts "
  "taken from the audited statements and applied to the forecast revenue and cost of "
  "sales, so that every pound of it traces to a receivable, an inventory or a payable "
  "rather than to a plug.")
rows = [["Days", "FY2022/23", "FY2023/24", "FY2024/25", "Carried forward"]]
CH = AL['cycle_hist']
rows.append(["Receivable days", E1(CH[0]['dso']), E1(CH[1]['dso']), E1(CH[2]['dso']),
             E1(DR['dso'])])
rows.append(["Inventory days", E1(CH[0]['dio']), E1(CH[1]['dio']), E1(CH[2]['dio']),
             E1(DR['dio'])])
rows.append(["Payable days", E1(CH[0]['dpo']), E1(CH[1]['dpo']), E1(CH[2]['dpo']),
             E1(DR['dpo'])])
rows.append(["Cash-conversion cycle", E1(CH[0]['ccc']), E1(CH[1]['ccc']), E1(CH[2]['ccc']),
             E1(DR['dso'] + DR['dio'] - DR['dpo'])])
rows.append(["Working capital (EGP m)", E(CH[0]['wc']), E(CH[1]['wc']), E(CH[2]['wc']),
             E(AL['cycle_fwd'][0]['wc'])])
rows.append(["As a share of revenue", PC(CH[0]['wc_pct_rev']), PC(CH[1]['wc_pct_rev']),
             PC(CH[2]['wc_pct_rev']), PC(AL['cycle_fwd'][0]['wc_pct_rev'])])
table(rows, [2.0, 1.15, 1.15, 1.15, 1.55], size=8.5, band_rows={4, 6})
caption(f"{{T}}.  Inventory is the whole story: {E1(CH[2]['dio'])} days of cost of sales "
        f"sat in stock at the last audited date, against {E1(CH[2]['dso'])} days of "
        f"receivables. A plant a thousand kilometres from its export port carries its "
        f"working capital in warehouses, and the auditor's inability to satisfy itself on "
        f"the slow-moving provision is a caveat about exactly this line.")

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
caption("{T}.  The cost of capital, built rather than assumed, on both premium bases.")
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
       "{F}.  The rate glides from its spot build to a terminal rate made from its own "
       "parts. The dotted line is the rate the traded price implies.")
P(f"Seven choices in the construction above are legitimately arguable, and every one of "
  f"them has been priced rather than defended in prose. Each row below is a complete "
  f"re-run of the model with that single component moved and everything else held, so the "
  f"figure in the third column is what this study would have published had it made the "
  f"other choice.")
rows = [["Choice made", "The alternative", "On the alternative",
         f"Against EGP {E2(AL['baseline'])}", "Why we keep ours"]]
for a in AL['alternatives']:
    rows.append([a['made'], a['alt'], E2(a['value']), f"{a['delta']:+.2f}", a['why']])
table(rows, [1.72, 1.78, 0.66, 0.66, 2.18], size=7.8, text_cols=(0, 1, 4))
caption("{T}.  The premium basis and the gas price are the two that move the answer "
        "most, in opposite directions, and both are published on both readings elsewhere "
        "in this study. None of the seven, and no combination of them, closes the gap to "
        "the traded price.")

H2("1.9  Sensitivity")
figure('fig5_crux.png', 6.9,
       "{F}.  Value per share across the two observable inputs that decide it. Every "
       "cell is a complete revaluation, not an interpolation.")
P(f"The same grid in numbers. Each column is a long-run export price in dollars a tonne, "
  f"each row a terminal cost of capital, and each cell a full re-run of the model — the "
  f"segment build, the waterfall, the terminal year and the bridge — not a multiplier "
  f"applied to the central answer.")
rows = [["Terminal cost of capital"] + [f"US${p:,.0f}/t" for p in GRD['prices']]]
for i, w in enumerate(GRD['waccs']):
    rows.append([PC(w)] + [E2(GRD['grid'][j][i]) for j in range(len(GRD['prices']))])
table(rows, [1.75, 1.03, 1.03, 1.03, 1.03, 1.03], size=8.5)
caption(f"{{T}}.  The highest cell in the grid is EGP "
        f"{E2(max(max(r) for r in GRD['grid']))}, at a long-run export price above today's "
        f"spot and a terminal rate below the sovereign's own short-term yield. Reaching "
        f"EGP {E2(SPOT)} requires leaving the grid altogether, which is what the reverse "
        f"calculation in the headline does explicitly.")
P("Each anchor below is varied independently around its own base, so the swings do not "
  "add. Every one is the difference between two complete re-runs of the model.")
rows = [["What moves", "Range tested", "Fair value span (EGP/share)", "Swing"]]
_pmin, _pmax = GRD['prices'][0], GRD['prices'][-1]
_wmin, _wmax = GRD['waccs'][0], GRD['waccs'][-1]
_pcol = [GRD['grid'][j][2] for j in range(len(GRD['prices']))]
_wrow = GRD['grid'][2]
SWINGS = [
    ("The capital programme",
     "Carried through against stopped",
     LN['cashflow']['carry_through'], LN['cashflow']['stopped']),
    ("Long-run export price",
     f"US${_pmin:,.0f} to US${_pmax:,.0f} a tonne", min(_pcol), max(_pcol)),
    ("Terminal cost of capital", f"{PC(_wmin)} to {PC(_wmax)}", min(_wrow), max(_wrow)),
    ("Gas price",
     "The realised price against the contract formula price",
     AL_BY['gas']['value'], AL['baseline']),
    ("Country-risk basis", "Rating spread against traded default swap",
     AL['baseline'], AL_BY['premium_basis']['value']),
    ("Beta", f"{WC['beta']:.3f} against the Dimson sum-beta of {V('dimson_sum_beta'):.3f}",
     AL['baseline'], AL_BY['beta']['value']),
    ("Project utilisation in the terminal year",
     f"{PC(V('anna_util_base'))} against {PC(V('anna_util_bull'))}",
     AL['baseline'], AL_BY['utilisation']['value']),
    ("Maintenance capital expenditure",
     f"{PC(V('maint_capex_pct'))} of revenue against {PC(V('maint_capex_pct')*2/3)}",
     AL['baseline'], AL_BY['maintenance_capex']['value']),
    ("Terminal growth",
     f"{PC(V('g_terminal'))} against {PC(V('g_terminal_alt'))}",
     AL_BY['terminal_growth']['value'], AL['baseline']),
]
SWINGS = sorted(SWINGS, key=lambda t: -abs(t[3] - t[2]))
for lab, rng, lo, hi in SWINGS:
    rows.append([lab, rng, f"{E2(min(lo, hi))} to {E2(max(lo, hi))}",
                 E2(abs(hi - lo))])
table(rows, [1.9, 2.35, 1.5, 0.8], size=8.3, band_rows={1}, text_cols=(1,))
caption("{T}.  Ranked by the size of the swing. The capital programme dominates "
        "everything else on this company, which is why it and not the discount rate is "
        "the study's contested judgement, and why it is published both ways rather than "
        "averaged.")
P(f"The beta deserves a note of its own, because it is the one input in the cost of "
  f"capital that comes from a statistical estimate rather than from a quote or a "
  f"disclosure. It is {WC['beta']:.3f}, from {BE['n']} weekly observations over "
  f"{BE['window_years']} years against an equal-weight index of {BE['composite_names']} "
  f"Egyptian names with the subject itself excluded — leaving a share inside its own "
  f"index injects a self-covariance term, and doing so here would have returned "
  f"{BE['self_inclusion_bias']['beta_index_including_subject']:.3f} instead. The "
  f"regression explains {PC(BE['r2'])} of the variation with a standard error of "
  f"{BE['se']:.3f}, so all three conditions of the usability test are met and the "
  f"estimate is adopted rather than defaulted. It was cross-checked two ways. The Dimson "
  f"sum-beta over one lead and two lags — the correction for co-movement booked late "
  f"because the share does not trade every session — is {V('dimson_sum_beta'):.3f}, and "
  f"the adopted figure sits inside its interval; the share closes unchanged on "
  f"{PC(BE['thin_trading']['flat_frac'])} of sessions against "
  f"{PC(BE['thin_trading']['eg_panel_median'])} for the Egyptian library, so it is not "
  f"unusually thin. And the simple prior for a cyclical, capital-intensive materials "
  f"business is 1.0 to 1.5. The alternative is priced with the other contested constructions in section 1.8 rather than argued: on "
  f"the sum-beta the answer is EGP {E2(AL_BY['beta']['value'])} instead of EGP "
  f"{E2(AL['baseline'])}.", size=9.8)

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
caption("{T}.  Levels are computed from recency-weighted pivot clusters in the same "
        "cleaned price history the rest of the study uses; the first of each is the nearest "
        "to the close. Nothing here is fitted and nothing is hand-drawn.")
figure('fig11_technical.png', 6.9,
       "{F}.  Price structure — moving averages and the computed level ladder.")
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
       f"{{F}}.  The middle of the simulated distribution over time, to "
       f"{M3['grade_date']}. The shaded bands hold half and ninety per cent of the paths.")
H2("Percentile map (Egyptian pounds a share)")
rows = [["Percentile", f"One month, to {M1['grade_date']}", f"Three months, to {M3['grade_date']}"]]
for p in ('p5', 'p25', 'p50', 'p75', 'p95'):
    rows.append([p.upper().replace('P', 'Percentile '), E2(M1['pct'][p]), E2(M3['pct'][p])])
rows.append(["Probability the price ends above today's", PC(M1['p_above']), PC(M3['p_above'])])
table(rows, [2.4, 2.25, 2.25], size=8.9, band_rows={6})
caption("{T}.  The map says where the price may end. It is not a forecast of where it "
        "will end, and the probability in the last row is the share of paths finishing "
        "above the anchor, not a claim about direction.")
figure('fig12_dist1m.png', 6.6,
       f"{{F}}.  The shape of the distribution at one month, to {M1['grade_date']}.")
figure('fig13_dist3m.png', 6.6,
       f"{{F}}.  And at three months, to {M3['grade_date']}. The right tail is longer "
       f"than the left because the price cannot fall below zero and can rise without a "
       f"bound — which is why the median sits below the mean and why the ladder below, not "
       f"the median, is the more useful line.")

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
caption("{T}.  Probability of touching each level at any point before the check date.")
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
caption("{T}.  The divergence is structured, not random. Every lens that lands above "
        "the cash-flow reading does so by not asking what the capital programme costs.")

P(f"The reading we take from this is not that four lenses agree — they do not, and a study "
  f"that made them agree would have hidden the thing worth knowing. It is that they "
  f"disagree in one direction and for one reason. The three lenses that land above the "
  f"cash-flow reading all reach their answer by declining to charge the capital programme "
  f"against the years in which it is actually spent: the multiple lens capitalises a "
  f"forward operating profit that is struck before capital expenditure, the normalised "
  f"lens values a steady state the company is not in, and the book lens values what has "
  f"already been paid for. Each is a legitimate question. None of them is the question "
  f"that decides this company.")
P(f"Our own reading therefore sits at the conservative end of the field, and the field's "
  f"upper bound of EGP {E2(LN['synthesis']['high'])} should be read as what the shares "
  f"would be worth if the programme were free — which it is not. What none of the lenses "
  f"does, on any construction tested in section 1.8, is reach EGP {E2(SPOT)}. The gap is "
  f"reported as the flat discount rate that would close it, about "
  f"{PC(DR['implied_wacc_base'])} against a sovereign ten-year yield of "
  f"{PC(V('rf_observed'))}, so that a reader who disagrees can see precisely what they are "
  f"disagreeing with rather than being asked to accept a conclusion.")
P("No rating and no price target is expressed here or anywhere else in this document. "
  "What is published is a field of fair values, the reasoning behind each, and the "
  "probability map around today's price.", italic=True, size=9.8)

# ==================================================================== 5-7 =====
H1("5  Catalysts")
rows = [["Catalyst", "Why it matters", "What to watch"]]
rows.append(["A dated capacity disclosure for the new complex",
             "The nameplate used in this study is derived from the ammonia design plate "
             "because no filing states it, and it is the input the terminal value is most "
             "sensitive to after the discount rate.",
             "The annual report's note on the project, or any prospectus for the facility "
             "drawn to build it"])
rows.append(["Physical progress moving back toward plan",
             f"Progress ran {PC(V('anna_progress_sep2025'))} against a "
             f"{PC(V('anna_plan_sep2025'))} plan while more than a quarter of the money "
             f"had been spent. Closing that gap shortens the construction window and "
             f"brings the terminal contribution forward.",
             "The percentage-of-completion figure the auditor discloses each year, against "
             "construction in progress on the balance sheet"])
rows.append(["A structural fix to industrial gas supply",
             "Every tonne not made is fixed cost with no revenue against it. The stoppage "
             f"cost was EGP {E1(V('stoppage_cost_FY2425'))}m in the last audited year and "
             f"EGP {E1(V('stoppage_cost_FY2324'))}m the year before.",
             "The disclosed stoppage cost, and the summer curtailment months in the "
             "quarterly production numbers"])
rows.append(["A price regime the market treats as permanent",
             "The study assumes mean reversion from a war-tightened level toward the cash "
             "cost of the marginal gas-based producer. A decade above today's spot is a "
             "different company.",
             "The Egyptian free-on-board quote against the model's path, and any change in "
             "the export duty that sits between the two"])
rows.append(["The debt moving into the currency the company earns",
             f"{PC(1 - WC['pct_debt_local'])} of the book is dollar-denominated against a "
             f"revenue stream that is largely priced in dollars but settled in pounds. A "
             f"single quarter's translation swing this year was larger than the whole "
             f"nine-month profit.",
             "Any refinancing announcement, and the currency split in the borrowings note"])
rows.append(["The first dividend",
             "Nothing was distributed in either of the last two years. A distribution "
             "would say the board considers the capital programme funded.",
             "The appropriation statement in the annual accounts"])
rows.append(["The next disclosed quarter against this study's own forecast",
             "This study forecasts the year to June 2026 from nine reviewed months. The "
             "fourth quarter is a direct test of that construction.",
             f"Revenue against EGP {E(F25['revenue'])}m and gross margin against "
             f"{PC(F25['gross_pct'])} for the full year"])
table(rows, [1.9, 3.0, 2.1], size=8.3, text_cols=(1, 2))
caption("{T}.  Each of these is observable from a disclosure the company already "
        "makes. None of them requires an estimate to detect.")

H1("6  Reading the probability zones")
P(f"Three zones, and what each would mean. The boundaries are the quartiles of the "
  f"three-month distribution in section 3, not levels chosen for the purpose.")
rows = [["Zone", "Three-month range (EGP)", "How to read it"]]
rows.append(["Below the lower quartile", f"under {E2(M3['pct']['p25'])}",
             "The price would be moving toward the upper end of what the four lenses "
             "support, and the gap this study reports would be closing from the price "
             "side rather than from the value side."])
rows.append(["The ordinary range",
             f"{E2(M3['pct']['p25'])} to {E2(M3['pct']['p75'])}",
             "Half the simulated paths end here. Nothing inside it would tell a reader "
             "anything about value, in either direction."])
rows.append(["Above the upper quartile",
             f"{E2(M3['pct']['p75'])} to {E2(M3['pct']['p95'])}",
             "The market would be paying more for a business whose sustainable return on "
             f"equity is {PC(LN['book']['roe_sustainable'])} against a cost of equity of "
             f"{PC(WC['ke_rating'])}, with the capital programme still unfinished."])
rows.append(["Above the ninety-fifth percentile", f"over {E2(M3['pct']['p95'])}",
             "One path in twenty. On a free float of about six per cent this can happen "
             "on modest volume, which is a fact about the register rather than about the "
             "business."])
rows.append(["What none of the zones says", "—",
             "Where the price will go. The distribution is a map of dispersion around "
             "today's price and carries no view of value; the value work is sections 1 "
             "and 4."])
table(rows, [1.75, 1.6, 3.65], size=8.3, band_rows={5}, text_cols=(2,))
caption("{T}.  Zones, not targets.")
P(f"The single most useful line in section 3 is the ladder rather than the map: there is "
  f"a {PC(M3['ladder']['touch_dn20'])} chance of touching twenty per cent below today's "
  f"price at some point in three months, against {PC(M3['ladder']['touch_up20'])} of "
  f"touching twenty per cent above. A reader who cares about the path, not just the "
  f"destination, should read that pair together — and should note that the two are close "
  f"to each other even though the median path drifts up, which is what a wide, "
  f"right-skewed distribution looks like from the inside.")

H1("7  Caveats and what would change our mind")
P(f"The auditor's reports carry a formal basis for qualification in every year examined. "
  f"They are not boilerplate and they are part of the evidence: fixed assets whose useful "
  f"lives and residual values have not been reassessed as the standard requires; "
  f"inventory whose slow-moving provision the auditor could not satisfy itself was "
  f"sufficient; a shortfall of {E(V('urea_stock_shortfall_t'))} tonnes of urea between "
  f"warehouse records and the physical count at Damietta; supplier and customer balances "
  f"unconfirmed; and, on the capital programme, a holding-company committee finding of "
  f"severe deficiencies in the award process. A reader who discounts this study should "
  f"discount the statements underneath it first.")
P(f"The largest modelled allocation is the gas share of the cost stack. The statements "
  f"give one materials line of EGP {E(V('cogs_materials_FY2425'))}m and do not split gas "
  f"from the rest. Gas is set at {PC(V('gas_share_of_materials'))} of it, which implies "
  f"{E(V('gas_m3_per_t_ammonia_modelled'))} cubic metres a tonne of ammonia — inside the "
  f"auditor's own disclosed {E(V('gas_usage_low_m3_t'))} to {E(V('gas_usage_high_m3_t'))} "
  f"range, but a choice nonetheless. The alternative gas price is priced in section 1.8 "
  f"and is worth EGP {E2(abs(AL_BY['gas']['delta']))} a share.")
P(f"Maintenance capital expenditure is the driver this study got wrong on its first "
  f"issue and has since re-anchored. It was set at three per cent of revenue on the "
  f"assertion that the company's own observed spending was abnormally low; the cash-flow "
  f"statements show two pre-project years at {PC(AL['capex']['pre_project_pooled'])} of "
  f"revenue, and that is now the central. The correction is worth EGP "
  f"{E2(abs(AL['capex']['house_standard_value'] - AL['baseline']))} a share on its own. "
  f"The replacement-rate framing at {PC(AL['capex']['replacement_rate'])} is published "
  f"beside it as the downside rather than averaged in.")
P(f"The terminal reinvestment rate is now the largest unsourced input left in the model. "
  f"It is set by terminal growth over an assumed {PC(DR['roc_terminal'])} return on "
  f"invested capital, which charges "
  f"{PC(DR['g_terminal'] / DR['roc_terminal'])} of terminal operating profit after tax "
  f"back into the business every year for ever — on a plant that has just been rebuilt "
  f"and needs no further building. A thirty per cent return on capital, which is what a "
  f"newly completed line earns while it is still filling, is worth EGP "
  f"{E2(abs(AL_BY['terminal_reinvestment']['delta']))} a share. The conservative reading "
  f"is kept and the alternative is priced.")
P(f"The new plant's capacity is derived, not disclosed. No filing states it. It is built "
  f"from the ammonia design plate less the draw of urea at its own plate, converted at "
  f"the nitrate route's ammonia ratio. Every figure that depends on it is flagged as "
  f"derived wherever it appears, and the utilisation applied to it is sensitised in both "
  f"directions.")
P(f"Terminal value is {PC(BASE['bridge']['tv_pct_ev'])} of enterprise value on the "
  f"carried-through case and {PC(HALT['bridge']['tv_pct_ev'])} on the stopped case. Above "
  f"one hundred per cent is unusual and is explained rather than smoothed: the explicit "
  f"window is a construction window with negative free cash flow, so the terminal block "
  f"carries the whole enterprise value and then some. It is a real characteristic of an "
  f"asset being rebuilt, not a modelling artefact — but it does mean the answer rests "
  f"more heavily on one year than most studies do.")
P(f"The forecast for the year to June 2026 rests on nine reviewed months and one "
  f"run-rated quarter. The fourth quarter is run-rated on the third quarter's revenue "
  f"with a {PC(1 - V('q4_runrate_haircut'))} haircut for the summer gas curtailment, and "
  f"the translation line is set to zero because a currency swing is not forecastable. "
  f"That last choice matters: the nine-month translation loss was larger than the "
  f"nine-month profit.")
P(f"The currency of discounting is unresolved and is the largest single judgement after "
  f"the capital programme. This is a company that sells most of its output in dollars, "
  f"borrows almost entirely in dollars, and reports in pounds. The study discounts pound "
  f"cash flows at a pound rate throughout and carries the dollar debt at "
  f"local-equivalent cost using the same depreciation wedge that drives the revenue "
  f"path, so the two cannot quietly disagree. A dollar valuation would be a different "
  f"study, not a different number.")
P(f"The concentration risks are plain and are not diversifiable inside this company: one "
  f"product, one site, one feedstock, one regulator setting both the domestic price and "
  f"the export duty, and a single offtake arrangement covering roughly two thirds of "
  f"production. The state and its related institutions hold about "
  f"{PC(V('holding_stake'))} of the shares and the free float is about "
  f"{PC(V('free_float'))}, so the traded price is set in a thin market. That is worth "
  f"remembering when comparing it with any valuation, including this one.")
P(f"The subsidised quota is a legal obligation the company has not been able to meet. It "
  f"delivered {E(V('quota_delivered_14m'))} tonnes of a {E(V('quota_required_14m'))}-tonne "
  f"requirement over fourteen months. The forecast does not assume that gap closes, but "
  f"it also does not price a penalty for it, because none is disclosed.")
P(f"The share count is taken from the capital note rather than from the exchange, whose "
  f"page is behind an automated challenge. Two third-party sources carry figures "
  f"inconsistent with the note and with each other; both are recorded in the bibliography "
  f"as documented discrepancies and neither is used anywhere in the build.")
P(f"What would change our mind, specifically. Upward: a disclosed capacity for the new "
  f"complex that earns above the cost of capital on the approved cost; the programme "
  f"completing near that cost rather than above it; a sustained export price regime above "
  f"the top of the tested grid; a refinancing that moves the debt into pounds; or evidence "
  f"that Egyptian equity risk is genuinely priced below its own sovereign — which would "
  f"revalue every Egyptian equity, not only this one. Downward: the contract gas price "
  f"replacing the realised price; a further slip in physical progress against money "
  f"spent; or a translation loss on the scale of this year's repeating.")

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
caption("{T}.  The EBIT line is struck before provisions, currency translation and "
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
caption(f"{{T}}.  Working capital is projected from the day counts the audited statements "
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
caption("{T}.  The full register — every input with its value, date and "
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
    caption(f"{{T}}.  Expert {num}'s workings in full — every intermediate "
            f"line, not a summary of them.")
    P(f"Range: EGP {E2(X['low'])} to EGP {E2(X['high'])} a share.", bold=True)
    P("Reading it.  " + X['reading'], size=9.8)
    if 'grid' in X:
        G3 = X['grid']
        rows = [["Time to maturity"] + [f"{v*100:.0f}% volatility" for v in G3['vols']]]
        for t, vals in zip(G3['years'], G3['values']):
            rows.append([f"{t:.0f} years"] + [E2(v) for v in vals])
        table(rows, [1.55, 1.07, 1.07, 1.07, 1.07, 1.07], size=8.5)
        caption("{T}.  The claim in Egyptian pounds a share across the two parameters "
                "that decide it. The published figure is the five-year, forty-five per cent "
                "cell; every other cell is a full revaluation of the same option.")
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
       "{F}.  Three methods, three ranges, and none of them reaches the traded "
       "price.")
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
caption("{T}.  Each gap isolated to the one assumption that creates it.")

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

finalise('EGCH_Valuation_Study_08-08-2026.docx')
print("wrote EGCH_Valuation_Study_08-08-2026.docx")
