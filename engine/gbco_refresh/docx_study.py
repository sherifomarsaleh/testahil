"""GBCO refresh — 16-section Word study builder. Reads study_numbers.json only (via
docx_base). External-reader language throughout; the contested stake is shown both ways
in every place it appears; the price map and technical read are reproduced from the
published page with their own dates and an explicit staleness statement."""
import os
from docx.shared import Pt, Inches
from docx_base import (doc, D, P, rich, H1, H2, caption, bullet, table, figure,
                       INK, GREY, BRASS, GOLD)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'GBCO_Valuation_Study_19-08-2026_public.docx')

fm = lambda v, d=1: f"{v:,.{d}f}"
pc = lambda v, d=1: f"{v*100:.{d}f}%"
ps = lambda v, d=2: f"EGP {v:,.{d}f}"

a1 = D['auto_h1']; h1 = D['h1']; lob1 = D['lob_h1']; hist = D['hist']; dr = D['drivers']
wac = D['wacc']; dcf = D['dcf']; legs = D['legs']; L = D['lenses']; BW = D['both_ways']
fs = D['fs_forecast']; pub = D['published']; mnt = D['mnt']; fair = D['fair']
lob = D['lob']; V = D['variance']
YRS = ['FY26E', 'FY27E', 'FY28E', 'FY29E', 'FY30E']
spot = D['spot']

# =====================================================================================
# 1 — MASTHEAD + READ FIRST
# =====================================================================================
P("TESTAHIL — STANDING RESEARCH SERIES", size=9, color=BRASS, space_after=2)
P("GB Corp (Ghabbour) — Valuation Study", size=22, bold=True, space_after=0)
P("GBCO.CA on the Egyptian Exchange  ·  fundamental refresh of 19 August 2026  ·  "
  "re-issues the study of 8 July 2026 (amended 9 July) on the first-half 2026 accounts",
  size=10, color=GREY, space_after=10)
H2("READ FIRST")
bullet("This is a re-build of the July 2026 study on new primary evidence: the reviewed "
       "consolidated interim financial statements of 30 June 2026 and the 2Q/1H26 results "
       "release, both published by the company on 13 August 2026.")
bullet(f"The single question that moves this valuation most is what a 42.93% stake in "
       f"MNT-Halan is worth. The June-2026 funding round says USD 1.4bn for the whole "
       f"company ({ps(BW['A']['sotp'])} per GB Corp share on our sum of the parts); the "
       f"company's own balance sheet carries the stake at EGP {fm(mnt['carrying']/1000)}bn "
       f"({ps(BW['B']['sotp'])} per share) — and the reviewer states it could not verify "
       f"that figure. We compute the whole study BOTH ways, side by side, and never "
       f"average the two.")
bullet(f"Fair-value range: {ps(fair['bear'], 1)} / {ps(fair['base'], 1)} / "
       f"{ps(fair['full'], 1)} (bear / central / bull) against a last exchange close of "
       f"{ps(spot)} on 22 July 2026 — the latest close in our price library. The company's "
       f"own investor page quoted {ps(D['spot_ir'])} on 19 August 2026.")
bullet("The probability map and the technical read in this document are reproduced from "
       "our published page unchanged, with their own dates shown. They were built on "
       "price data of 22 July 2026 and were NOT re-struck for this refresh; only the "
       "fundamental range moved. A fresh price feed updates them on their own schedule.")
bullet("No rating and no price target. Fair-value ranges and probabilities only.")

# =====================================================================================
# 2 — HEADLINE
# =====================================================================================
H1("The headline")
rich([(f"{ps(fair['base'], 1)} central fair value ", dict(bold=True, size=13)),
      (f"— or {ps(L['central']['B'])} if you take the company's own book at its word",
       dict(size=13))], space_after=4)
P(f"The first half of 2026 settled the operating question and sharpened the valuation "
  f"one. Operationally, GB Corp beat the July study's pace almost everywhere that "
  f"matters: automotive revenue ran about "
  f"{pc([v for v in V if v['line']=='Auto revenue'][0]['deviation'], 0)} ahead of the "
  f"forecast's seasonal path, commercial vehicles nearly doubled, and the working-capital "
  f"discipline the model hoped for actually printed (net debt fell to "
  f"EGP {fm(a1['nd']/1000)}bn, {fm(2.14, 2)}x EBITDA). What fell short sits below the "
  f"operating line: net finance cost rose 42% and the effective tax rate reached "
  f"{pc(D['etr_h1'])} because regional losses in Iraq and Jordan earn no tax relief — "
  f"group profit fell 24.5% on a 35% revenue gain.")
P(f"The valuation question is now officially two-sided. In June, Egypt's largest bank "
  f"led a funding round valuing MNT-Halan at USD 1.4bn; GB Corp's stake, translated at "
  f"today's {fm(D['usdegp'], 2)} pound, is worth EGP {fm(legs['mnt_round_egp']/1000)}bn "
  f"on that mark. The company's balance sheet carries the same stake at "
  f"EGP {fm(mnt['carrying']/1000)}bn — and the auditor's review report says it was not "
  f"given MNT-Halan's accounts and could not verify the number, for the second period "
  f"running. That disagreement is worth {ps(BW['gap_ps'])} per share. We show every "
  f"result in both framings rather than blending them.")

# =====================================================================================
# 3 — VALUATION SUMMARY
# =====================================================================================
H1("Valuation summary — every read at a glance")
rows = [["Lens", "Bear", "Base", "Bull", "Weight"],
        ["Sum of the parts — stake at the round mark", fm(BW['A']['sotp_bear'], 2),
         fm(BW['A']['sotp'], 2), fm(BW['A']['sotp_bull'], 2), pc(L['weights']['sotp'], 0)],
        ["Sum of the parts — stake at the balance-sheet mark", fm(BW['B']['sotp_bear'], 2),
         fm(BW['B']['sotp'], 2), fm(BW['B']['sotp_bull'], 2), "(same weight, alternate framing)"],
        ["Book value & sustainable return", fm(L['book']['bear'], 2), fm(L['book']['base'], 2),
         fm(L['book']['bull'], 2), pc(L['weights']['book'], 0)],
        ["Relative multiples", fm(L['relative']['bear'], 2), fm(L['relative']['base'], 2),
         fm(L['relative']['bull'], 2), pc(L['weights']['relative'], 0)],
        ["Normalised earnings power", fm(L['normalized']['bear'], 2), fm(L['normalized']['base'], 2),
         fm(L['normalized']['bull'], 2), pc(L['weights']['normalized'], 0)],
        ["Weighted central — round mark", fm(L['central']['bear'], 2), fm(L['central']['A'], 2),
         fm(L['central']['bull'], 2), "100%"],
        ["Weighted central — balance-sheet mark", "—", fm(L['central']['B'], 2), "—", "100%"],
        ["Published range (this refresh)", fm(fair['bear'], 1), fm(fair['base'], 1),
         fm(fair['full'], 1), ""],
        ["July 2026 study, for comparison", fm(pub['fair']['bear'], 1), fm(pub['fair']['base'], 1),
         fm(pub['fair']['full'], 1), ""]]
table(rows, [2.55, 0.95, 0.95, 0.95, 1.55], band_rows={7, 8})
caption(f"EGP per share. The bear of the published range lives in the balance-sheet-mark "
        f"world with operating setbacks; the bull lives in the round-mark world with the "
        f"operating tailwinds. Last close {ps(spot)} (22 July 2026).")
figure(os.path.join(HERE, 'fig1_football.png'), 6.9,
       "Every lens, with the contested stake computed both ways — the two darkest bars are "
       "the same synthesis under the two marks.")

# =====================================================================================
# 4 — COMPANY OVERVIEW
# =====================================================================================
H1("Company overview")
P("GB Corp is Egypt's largest automotive assembler and distributor and, through GB "
  "Capital, one of its largest non-bank lenders. The automotive side spans passenger "
  "cars (Hyundai, Chery, Changan, Haval, Deepal, MG, Mazda, Genesis and others, "
  "assembled and imported), commercial vehicles and construction equipment (Volvo, "
  "Fuso, Marcopolo bus building, exports), two- and three-wheelers (Bajaj), tires and "
  "parts. The Sadat assembly plant became fully operational in the half, with a locally "
  "assembled Changan SUV already the best-seller in its class; a further Hyundai model "
  "arrives in September 2026 and a third Changan model late in the year. The financing "
  "side (GB Lease & factoring, Drive consumer finance and its Forsa instalment arm, "
  "fleet and bus rental, SME lending, securitisation) carried a net loan book of EGP "
  "24.0bn at June 2026, up 33.6% in a year, with non-performing loans at 2.8%.")
P(f"Alongside the consolidated businesses sits a 42.93% associate stake in MNT-Halan, "
  f"the Egyptian-origin fintech whose lending book now reaches roughly USD 1.95bn across "
  f"Egypt, Turkey and Pakistan. The Ghabbour family controls 63.38% of GB Corp; Olayan "
  f"of Saudi Arabia holds 3.61% and the Miri Strategic Emerging Markets Fund 7.37%. "
  f"1,085.5mn shares are outstanding; the free float is 36.6%.")
rows = [["H1-2026, EGP mn", "Group", "Automotive", "GB Capital"],
        ["Revenue", fm(h1['rev']), fm(a1['rev']), fm(D['capital_h1']['rev'])],
        ["Gross profit", fm(h1['gp']), fm(a1['gp']), fm(D['capital_h1']['gp'])],
        ["Operating profit", fm(h1['op']), fm(a1['op']), fm(D['capital_h1']['op'])],
        ["Net profit (attributable)", fm(h1['np']), fm(a1['np_after_nci']), fm(D['capital_h1']['np'])],
        ["Net debt / book", fm(D['bs']['nd_group']), fm(a1['nd']), fm(D['capital_h1']['book'])]]
table(rows, [2.4, 1.5, 1.5, 1.5])
caption("From the reviewed interim statements and the results release of 13 August 2026. "
        "GB Capital's last row is its net loan portfolio; the group's is net debt.")

# =====================================================================================
# 5 — SECTION 1: FUNDAMENTAL VALUATION
# =====================================================================================
H1("1  Fundamental valuation")

H2("1.1  The cash-flow model — the primary lens, with the full waterfall")
P(f"The automotive business is valued on a five-year free-cash-flow-to-the-firm model "
  f"dated 30 June 2026, the date of the reviewed balance sheet. Revenue is not a growth "
  f"rate applied to a revenue line: each line of business is built on its own disclosed "
  f"units and prices — locally assembled and imported cars separately, buses, trucks and "
  f"construction equipment separately, two-, three- and four-wheelers on their own count "
  f"— with unit costs escalated on their own physical classes. Sections 1.6 and 1.7 set "
  f"the build out line by line. The waterfall below then runs to present value at the "
  f"{pc(wac['wacc_cds'], 2)} cost of capital built in section 1.8. Every line is "
  f"computed, not typed.")
hdr = ["EGP mn"] + YRS
rws = [hdr]
for key, lab, d_ in [('rev', 'Revenue', 0), ('gp', 'Gross profit', 0),
                     ('gpm', '  margin on revenue', None), ('ebit', 'Operating profit', 0),
                     ('etr', '  effective tax rate', None),
                     ('nopat', 'Net operating profit after tax', 0),
                     ('dna', 'Add back depreciation & amortisation', 0),
                     ('capex', 'Less capital expenditure', 0),
                     ('dwc', 'Less the working-capital build', 0),
                     ('fcff', 'Free cash flow to the firm', 0)]:
    row = [lab]
    for r in dcf['rows']:
        row.append(pc(r[key], 1) if d_ is None else fm(r[key], d_))
    rws.append(row)
table(rws, [2.25, 0.95, 0.95, 0.95, 0.95, 0.95], band_rows={10})
P(f"Two conventions are deliberate. The valuation date is 30 June 2026, so the realized "
  f"first half — {fm(dcf['h1_fcff'], 0)} of free cash flow, computed from the disclosed "
  f"half-year actuals — is removed rather than counted twice (it is already inside the "
  f"net debt the bridge subtracts), and the remaining flows are discounted mid-period. "
  f"That makes the second half of 2026 visibly cash-negative "
  f"({fm(dcf['h2_fcff'], 0)}): the first half released EGP "
  f"{fm(-(a1['wc']-hist['FY25']['wc'])/1000, 1)}bn of working capital as inventories "
  f"unwound, and the year-end always rebuilds stock ahead of the selling season. And tax "
  f"runs at each year's own modelled effective rate — {pc(dr['etr_path'][0], 0)} in the "
  f"first year against a 22.5% statute, because Iraqi and Jordanian losses shield "
  f"nothing — gliding to the statute only as the regional drag ends.")
H2("The lines that price this business, and how each is set")
P("Three constructions in that waterfall carry most of the answer, and each was "
  "challenged in review. None is an assumption dropped in from outside; each is shown "
  "with the evidence, the alternative a reviewer would propose, and what that "
  "alternative costs.")
alts = D['alternatives']
rows = [["Line", "What the model uses", "The evidence, and what the alternative costs"],
 ["Working capital",
  f"{pc(dr['wc_pct'][0], 1)} of revenue gliding to {pc(dr['wc_pct'][-1], 1)}",
  f"The measured cycle at 30 June — 122 days of inventory, 27 of receivables, 82 of "
  f"payables — and five disclosed quarterly snapshots spanning 16.7–18.9bn. A reviewer "
  f"would carry the FY25 year-end 28.5% instead; that was the pre-buying outlier, and "
  f"pricing it in costs EGP {fm((dcf['auto_eq']-alts['wc_at_fy25_peak']['auto_eq'])/D['shares'], 2)} "
  f"per share of the automotive leg ({fm(alts['wc_at_fy25_peak']['auto_eq'], 0)} vs "
  f"{fm(dcf['auto_eq'], 0)}). Held, and stress-shown."],
 ["The margin path",
  f"one more year of the measured compression (to {pc(dr['gpm_path'][1], 1)} in FY27E), "
  f"then cost moves with price",
  f"First halves printed {pc(a1['h1_25_gp']/a1['h1_25_rev'], 1)} then "
  f"{pc(a1['gp']/a1['rev'], 1)} — one measured year of compression. Compounding the "
  f"cost-price differential every year instead drives the margin to "
  f"{pc(alts['margin_compounds']['gpm_fy30'], 1)} by FY30E and the automotive leg to "
  f"EGP {fm(alts['margin_compounds']['auto_eq'], 0)}mn "
  f"({fm(alts['margin_compounds']['auto_eq']/D['shares'], 2)} a share) — a forecast "
  f"story the disclosed series cannot measure, priced here and rejected. The offsetting "
  f"force (three more locally assembled models) is real and equally unquantified."],
 ["The terminal value",
  f"FY30E after-tax operating profit grown {pc(wac['tg'], 1)}, less reinvestment forced "
  f"to growth ÷ a terminal return of {pc(dcf['roic_t'], 1)}",
  f"Growth in the perpetuity is paid for, not assumed free. The July edition used plain "
  f"Gordon on year-five cash flow — its hidden implied terminal return was "
  f"{pc(dcf['roic_implied_gordon'], 1)}, above even today's realized "
  f"{pc(0.229, 1)}; that construction is worth EGP "
  f"{fm(dcf['auto_eq_gordon']/D['shares'], 2)} a share and is shown as the labelled "
  f"alternative. At the forward model's transitional 15% marginal return the leg would "
  f"be worth {fm(alts['tv_roic_15']['auto_eq']/D['shares'], 2)}; the "
  f"{pc(dcf['roic_t'], 1)} used sits on the leg's own realized returns."]]
table(rows, [1.15, 1.85, 3.95], size=8.4)
H2("The bridge from enterprise value to the equity")
pvr = dcf['pv_rows']
rows = [["Line", "EGP mn", "Note"],
        ["Present value of the discounted flows", fm(dcf['pv_sum'], 0),
         f"H2-26E {fm(pvr[0]['fcff'], 0)} plus FY27E-FY30E, each mid-period"],
        ["Terminal cash flow", fm(dcf['tv_fcff_terminal'], 0),
         f"FY30E NOPAT {fm(dcf['rows'][-1]['nopat'], 0)} grown {pc(wac['tg'], 1)}, times one "
         f"less the {pc(dcf['reinv_t'], 1)} reinvestment rate (growth ÷ terminal return "
         f"{pc(dcf['roic_t'], 1)}) — the growth is paid for"],
        ["Present value of the terminal value", fm(dcf['pv_tv'], 0),
         f"capitalised at {pc(wac['wacc_cds'], 2)} − {pc(wac['tg'], 1)}; "
         f"{pc(dcf['tv_pct'], 0)} of enterprise value — disclosed here, in the summary "
         f"and in section 7, and stressed in 1.9"],
        ["Enterprise value — automotive", fm(dcf['ev'], 0), "the two lines above"],
        ["Less net debt", fm(-dcf['auto_nd'], 0),
         "the segment's 30-Jun-26 figure from the release's own net-debt table "
         "(debt + leasing notes − cash − inter-segment balances)"],
        ["Less non-controlling interests", fm(-dcf['auto_nci'], 0),
         "the automotive segment's minority book at 30-Jun-26"],
        ["Automotive equity value", fm(dcf['auto_eq'], 0), ""],
        ["Per share", fm(dcf['auto_eq']/D['shares'], 2),
         "the cash-flow leg alone; the group's other legs are added in section 1.5"],
        ["ALTERNATIVE — Gordon on year-five cash flow", fm(dcf['auto_eq_gordon'], 0),
         f"the July construction; implied terminal return "
         f"{pc(dcf['roic_implied_gordon'], 1)}, disclosed rather than hidden. Worth "
         f"{fm((dcf['auto_eq_gordon']-dcf['auto_eq'])/D['shares'], 2)} a share more; both "
         f"are shown"]]
table(rows, [2.30, 1.05, 3.60], size=8.6, band_rows={7, 8})
H2("1.2  Book value and sustainable return — the asset lens")
bd = D['book_decomp']
rows = [["What the restated book is made of (per share)", "EGP"],
        ["Automotive segment equity", fm(bd['auto'], 2)],
        ["GB Capital operating equity (ex-associates)", fm(bd['capital_oper'], 2)],
        ["Associates at the balance-sheet carrying", fm(bd['assoc_at_book'], 2)],
        ["Inter-segment eliminations", fm(bd['elim'], 2)],
        ["Restated book value per share", fm(bd['total'], 2)],
        ["… with MNT-Halan at the round instead", fm(bd['marked_A'], 2)]]
table(rows, [4.4, 1.6], band_rows={5, 6})
P(f"Restated book is {ps(bd['total'])} per share — the prior-year accounts were restated "
  f"upward by EGP 2.88bn, mostly the MNT-Halan write-up, so the book already contains "
  f"part of the contested mark. Forecast return on that equity runs {pc(fs[0]['roe'])} "
  f"in FY26E, recovering toward {pc(fs[-1]['roe'])} by FY30E as regional losses fade and "
  f"the tax rate normalises — below the {pc(wac['ke_cds'], 1)} cost of equity "
  f"throughout, which is why this lens anchors at plain book (price-to-book of one) "
  f"rather than a premium. The bull case is the marked book ({ps(bd['marked_A'])}, the "
  f"round-mark uplift of {ps(bd['mnt_uplift'])} inside it); the bear "
  f"({ps(L['book']['bear'])}) is 0.8x book, the discount the market applies to "
  f"sub-hurdle returns.")
H2("1.3  Relative multiples")
P(f"On the statement-forecast for the full year 2026 the group earns "
  f"{ps(L['relative']['eps26'])} per share. Egypt's closest listed financing peer, "
  f"Contact Financial, trades at {fm(D['peers']['CNFN'], 1)}x trailing earnings; "
  f"AutoNation, the mature-market auto retailer, at {fm(D['peers']['AN'], 1)}x; Dogus "
  f"Otomotiv, Turkey's closest analogue to the distribution business, at "
  f"{fm(D['peers']['DOAS'], 1)}x; Bajaj Auto, the two-wheeler partner, at "
  f"{fm(D['peers']['BAJAJ'], 1)}x in a far richer market. A {fm(8.0,0)}–{fm(11.0,0)}x "
  f"band with {fm(9.5,1)}x at the centre prices GBCO at {ps(L['relative']['bear'])} / "
  f"{ps(L['relative']['base'])} / {ps(L['relative']['bull'])}. This lens is deliberately "
  f"stake-blind: earnings capture only MNT-Halan's equity pickup, not its mark — which "
  f"is exactly why it sits at the cautious end of the field.")

H2("1.4  Normalised earnings power")
rows = [["Normalisation walk (mid-cycle)", "EGP mn"],
        ["FY27E automotive operating profit", fm(dcf['rows'][1]['ebit'], 0)],
        ["Financing cost at an eased 17% on today's net debt", fm(-a1['nd']*dr['fin_norm_rate'], 0)],
        ["Tax at the statutory 22.5% (no loss-stranding)", fm(-(dcf['rows'][1]['ebit']-a1['nd']*dr['fin_norm_rate'])*D['tax_statutory'], 0)],
        ["GB Capital net profit, FY27E (incl. associates)", fm(dr['cap_np_path'][1], 0)],
        ["Normalised group profit", fm(L['normalized']['norm_pat'], 0)],
        ["Per share x 8.5", fm(L['normalized']['base'], 2)]]
table(rows, [4.4, 1.6], band_rows={5, 6})
dst = D['distortions']
rows = [["The two distortions, priced separately", "EGP mn / year", "Per share"],
        ["Tax above statute on unshielded regional losses", fm(dst['tax']['egp_mn'], 0),
         fm(dst['tax']['per_share'], 2)],
        ["Funding cost above the eased-cycle rate", fm(dst['funding']['egp_mn'], 0),
         fm(dst['funding']['per_share'], 2)]]
table(rows, [3.4, 1.4, 1.2])
P(f"What normalisation removes: the {pc(D['etr_h1'], 1)} effective tax rate (statutory "
  f"is 22.5% — the excess is Iraqi and Jordanian losses that shield nothing), and a "
  f"funding bill still priced off a 19% policy corridor that the central bank has begun "
  f"easing. At 8.5x — between the Egyptian financing peer and the mature-market "
  f"retailers — normalised power is worth {ps(L['normalized']['base'])} "
  f"(bear {ps(L['normalized']['bear'])}, bull {ps(L['normalized']['bull'])}). This lens "
  f"leans furthest into the recovery; its weight reflects that.")

H2("1.5  Synthesis — four lenses, one field")
P(f"Weights: sum of the parts {pc(L['weights']['sotp'], 0)}, book "
  f"{pc(L['weights']['book'], 0)}, relative {pc(L['weights']['relative'], 0)}, "
  f"normalised {pc(L['weights']['normalized'], 0)}. Under the round mark the weighted "
  f"central is {ps(L['central']['A'])}; under the company's balance-sheet mark it is "
  f"{ps(L['central']['B'])}. We publish the round-mark central as the base — the round "
  f"is real third-party money, led by the country's largest bank — and we let the "
  f"balance-sheet framing define the bear side of the published range, because the "
  f"auditor's inability to verify the carrying value is not a technicality. The two "
  f"numbers are {ps(round(L['central']['A'], 2)-round(L['central']['B'], 2))} apart; "
  f"nothing in this study "
  f"averages them.")

H2("1.6  The drivers — every line on its own volumes and prices")
P("Before re-setting a single driver, the July forecast was scored against the half "
  "that actually printed:")
rows = [["Line", "July study, FY26E", "H1-26 actual", "Full-year pace vs forecast", "Verdict"]]
for v in V:
    if v.get('h1_share_fy25'):
        rows.append([v['line'],
                     fm(v['forecast_fy26e'], 0), fm(v['actual_h1'], 0),
                     f"{v['deviation']*100:+.0f}%", v['verdict'].lower()])
table(rows, [1.8, 1.35, 1.15, 1.55, 1.0])
caption("'Full-year pace' compares the half against the forecast using last year's "
        "seasonal split, so a strong second half is not mistaken for a miss. Anything "
        "beyond five percent is treated as a forecast error to be explained, not "
        "smoothed over.")
P("Three real errors surfaced. Commercial vehicles were under-forecast by a third — the "
  "bus and truck replacement cycle plus exports ran far ahead of the modelled recovery. "
  "Tires were over-forecast — last year's base carried a one-off dealer stock transfer "
  "the old model treated as run-rate. And group profit was over-forecast for a reason "
  "that had nothing to do with operations: the old model taxed everything at a flat "
  "28% and carried no financing-cost line; the real half printed a 41% effective rate "
  "and 42% higher finance costs. All three mechanisms are now modelled explicitly.")
figure(os.path.join(HERE, 'fig4_variance.png'), 6.9,
       "The scorecard behind the driver re-set.")
P("The re-built stack — every disclosed unit grown on its own driver. FY26E is never "
  "typed: it is the disclosed first half plus a second half built on the FY25 measured "
  "seasonal split, with one visible tempering judgement per line. Locally assembled "
  "cars are the driver (the launch calendar) and imports the residual; buses are the "
  "driver and trucks the residual; unit costs escalate on their own physical classes "
  "(imported content on the currency path, domestic on the inflation path) and margins "
  "fall out as outputs:")
rows = [["Driver", "H1-26 actual", "FY26E", "FY27E", "FY30E", "Set by"],
        ["Locally assembled cars (units)", fm(lob1['ckd_u'], 0), fm(lob['FY26E']['ckd_u'], 0),
         fm(lob['FY27E']['ckd_u'], 0), fm(lob['FY30E']['ckd_u'], 0),
         "the launch calendar: Hyundai Sep-26, third Changan 4Q26"],
        ["Imported cars (units, residual)", fm(lob1['cbu_u'], 0), fm(lob['FY26E']['cbu_u'], 0),
         fm(lob['FY27E']['cbu_u'], 0), fm(lob['FY30E']['cbu_u'], 0),
         "total market path less the localization drive"],
        ["Passenger cars — total units", fm(lob1['pc_u'], 0), fm(lob['FY26E']['pc_u'], 0),
         fm(lob['FY27E']['pc_u'], 0), fm(lob['FY30E']['pc_u'], 0),
         "market +18% maturing; share held"],
        ["Passenger cars — price (EGP mn)", fm(lob1['pc_r']/lob1['pc_u'], 3),
         fm(lob['FY26E']['pc_asp'], 3), fm(lob['FY27E']['pc_asp'], 3), fm(lob['FY30E']['pc_asp'], 3),
         "realized +10.8%; capped below cost inflation ahead"],
        ["Buses (units)", fm(lob1['bus_u'], 0), fm(lob['FY26E']['bus_u'], 0),
         fm(lob['FY27E']['bus_u'], 0), fm(lob['FY30E']['bus_u'], 0),
         "tourism/fleet recovery off a weak base"],
        ["Trucks (units, residual)", fm(lob1['truck_u'], 0), fm(lob['FY26E']['truck_u'], 0),
         fm(lob['FY27E']['truck_u'], 0), fm(lob['FY30E']['truck_u'], 0),
         "replacement demand net of the bus driver"],
        ["Commercial & equipment — revenue", fm(lob1['cv_r'], 0), fm(lob['FY26E']['cv_r'], 0),
         fm(lob['FY27E']['cv_r'], 0), fm(lob['FY30E']['cv_r'], 0),
         "units x price, both separately grown"],
        ["Two/three/four-wheelers — units", fm(lob1['lm_u'], 0), fm(lob['FY26E']['lm_u'], 0),
         fm(lob['FY27E']['lm_u'], 0), fm(lob['FY30E']['lm_u'], 0),
         "India supply constraint resolves"],
        ["Tires & parts trading — revenue", fm(lob1['tr_r'], 0), fm(lob['FY26E']['tr_r'], 0),
         fm(lob['FY27E']['tr_r'], 0), fm(lob['FY30E']['tr_r'], 0),
         "one-off margin benefit resets next year"],
        ["Other automotive — revenue", fm(lob1['oth_r'], 0), fm(lob['FY26E']['oth_r'], 0),
         fm(lob['FY27E']['oth_r'], 0), fm(lob['FY30E']['oth_r'], 0), "after-sales residual"],
        ["Automotive total revenue", fm(a1['rev'], 0), fm(lob['FY26E']['auto_rev'], 0),
         fm(lob['FY27E']['auto_rev'], 0), fm(lob['FY30E']['auto_rev'], 0), ""]]
table(rows, [1.75, 0.92, 0.85, 0.85, 0.85, 1.78], size=8.2, band_rows={3, 11})
P(f"The margin mechanics: gross margin printed {pc(a1['gp']/a1['rev'], 1)} in the half "
  f"against {pc(a1['h1_25_gp']/a1['h1_25_rev'], 1)} a year earlier — one measured year "
  f"of compression, driven by supply normalising and the pound. The model carries "
  f"exactly one more year of that differential (to {pc(dr['gpm_path'][1], 1)} in FY27E) "
  f"and then holds the cost-to-price relationship flat: the compression is evidenced, a "
  f"compounding forever-version of it is not, and the offsetting force — three more "
  f"locally assembled models — is real but equally unquantified in the filings. Second-"
  f"half margins are set off last year's measured seasonal gap "
  f"({pc(dr['seasonal_gap'], 1)} below the first half), not assumed.")
figure(os.path.join(HERE, 'fig3_drivers.png'), 6.9,
       "History and forecast, stacked by line of business.")
P(f"Working capital is projected on its measured cycle — 122 days of inventory, 27 of "
  f"receivables, 82 of payables at June 2026 (a 67-day cash cycle) — expressed as "
  f"{pc(dr['wc_pct'][0], 1)} of revenue gliding to {pc(dr['wc_pct'][-1], 1)}, anchored "
  f"on five disclosed quarterly snapshots rather than the year-end peak. Capital "
  f"spending follows the company's own half ({fm(a1['capex'], 0)} spent, EGP "
  f"{fm(D['bs']['commitments'], 0)}mn contractually committed). The effective tax rate "
  f"glides from 38% to the statutory 22.5% as the regional drag fades — management "
  f"itself guides the Jordanian rationalisation to largely end this year.")

H2("1.7  The crux — one stake, two official answers")
P(f"Strip everything else away and this valuation is a view on one number. GB Corp's "
  f"stake in MNT-Halan has produced three official prints inside fourteen months: the "
  f"accounts carried 44.01% before the June round; the reviewed statements now say "
  f"42.93% after its first close; and the company's own June release described 41.61% "
  f"as the position once the round fully closes. The statements outrank the release for "
  f"today's number, so 42.93% is used. On that stake, the two official answers to "
  f"'what is it worth' are EGP {fm(legs['mnt_round_egp']/1000)}bn (the round: USD 1.4bn "
  f"led by Al Ahly Capital of the National Bank of Egypt, translated at "
  f"{fm(D['usdegp'], 2)}) and EGP {fm(mnt['carrying']/1000)}bn (the equity-method "
  f"carrying value — written up 2.46bn in a restatement, and explicitly not verified by "
  f"the reviewing auditor, who was not provided MNT-Halan's statements for the second "
  f"period in a row). The gap is {ps(BW['gap_ps'])} per GB Corp share; the round mark "
  f"alone equals {pc(legs['mnt_round_egp']/(D['spot_ir']*D['shares']), 0)} of the "
  f"company's entire market value at the August quote — the market has already chosen "
  f"its framing, and it is not the round.")
rows = [["If the second close lands at…", "Stake value (EGP mn)", "Sum of the parts / share",
         "Weighted central / share"]]
for step in D['crux_ladder']:
    lab = (step.get('label') or f"USD {step['round_usd']:,.0f}mn")
    rows.append([lab, fm(step['assoc']-D['other_assoc']-D['fvoci'], 0) if step.get('round_usd')
                 else fm(mnt['carrying'], 0), fm(step['sotp'], 2), fm(step['central'], 2)])
table(rows, [2.15, 1.55, 1.65, 1.60], size=8.8)
caption("The ladder prices the crux through the whole synthesis, not just the one line. "
        "What settles it: MNT-Halan's audited numbers reaching the reviewer, the second "
        "close completing, or any arm's-length secondary sale. Until then, both answers "
        "run through every table in this study.")
H2("1.8  Macro & country — the cost of capital, built from scratch")
P(f"Egypt's 10-year local bond yielded {pc(wac['rf_obs'], 2)} on 19 August 2026. That "
  f"yield already contains the sovereign's own default risk, so charging an "
  f"emerging-market equity premium on top of the raw yield would count the same risk "
  f"twice — the error that inflated the July study's discount rate and is corrected "
  f"here. We strip the sovereign's default spread and add it back once, inside the "
  f"equity premium, on two published bases:")
rows = [["Cost of equity", "CDS basis", "Rating basis"],
        ["Observed 10Y local yield (19-Aug-26)", pc(wac['rf_obs'], 2), pc(wac['rf_obs'], 2)],
        ["less sovereign default spread", pc(D['ds_cds'], 2), pc(D['ds_rating'], 2)],
        ["risk-free, normalised", pc(wac['rf_star_cds'], 2), pc(wac['rf_star_rating'], 2)],
        ["equity risk premium (Egypt, Jan-26 tables)", pc(D['erp_cds'], 2), pc(D['erp_rating'], 2)],
        ["beta (own shares vs the EGX 30, weekly, five years)", fm(wac['beta'], 3), fm(wac['beta'], 3)],
        ["Cost of equity", pc(wac['ke_cds'], 2), pc(wac['ke_rating'], 2)]]
table(rows, [3.3, 1.35, 1.35], band_rows={6})
P(f"The beta is this study's own regression of GBCO's weekly returns on the exchange's "
  f"published index over five years: {fm(wac['beta'], 3)} with a standard error of "
  f"{fm(D['beta']['se'], 3)} across {fm(D['beta']['n'], 0)} weeks, explaining "
  f"{pc(D['beta']['r2'], 0)} of the variance — a usable, conservative estimate that "
  f"replaces the July study's assumption of exactly 1.0 (its earlier attempt, five "
  f"annual observations, was rightly discarded as meaningless).")
rows = [["Cost of debt — the evidence", "Rate", "Dated"],
        ["Company's own average on current EGP borrowings (H1-26 statements)", pc(wac['kd_pretax_local'], 2), "13-Aug-26"],
        ["Company's own average on USD borrowings", pc(D['kd_usd'], 2), "13-Aug-26"],
        ["Consumer-finance bond programme, 2022 vintage (fixed)", "13.5–14.0%", "2022"],
        ["Central-bank overnight deposit corridor (held, July meeting)", pc(D['cbe_dep'], 1), "11-Jul-26"]]
table(rows, [4.0, 1.0, 1.0])
P(f"Essentially the whole EGP 43.5bn borrowing book floats, so the current average IS "
  f"the marginal rate — it reprices as the central bank moves. The blended pre-tax cost "
  f"is {pc(wac['kd_blended'], 2)} ({pc(wac['pct_local'], 0)} local at "
  f"{pc(wac['kd_pretax_local'], 2)}, the dollar tranche carried at its coupon plus "
  f"expected depreciation, {pc(wac['kd_fx_local_equiv'], 2)} in pound terms — the "
  f"currency split of the debt itself is not disclosed and is bounded at no more than "
  f"17% dollar from the statements' currency-exposure table; we carry 10% and flag it). "
  f"One deliberate tension is disclosed rather than hidden: the borrowing average sits "
  f"below the 10-year sovereign yield. That is tenor, not magic — the company borrows "
  f"short against a policy corridor of 19% while the long end carries the fiscal "
  f"premium; a corporate cannot out-borrow its sovereign at matched maturity, and at "
  f"matched maturity it does not.")
P(f"Weights use the market's own equity value ({ps(D['spot_ir'])} on the company's "
  f"investor page, 19 August, times 1,085.5mn shares) against the automotive segment's "
  f"gross debt including leasing notes — the lending platform's funding belongs to its "
  f"loan book, not to the automotive capital structure, and is valued inside that leg "
  f"instead. Result: equity {pc(wac['we'], 0)} / debt {pc(wac['wd'], 0)}, and a "
  f"weighted average cost of capital of {pc(wac['wacc_cds'], 2)} on the CDS basis "
  f"({pc(wac['wacc_rating'], 2)} on the rating basis — both are used and shown, the "
  f"CDS basis as primary, continuing the July study's choice). Every contested "
  f"construction above is priced in section 1.9 rather than just named.")

H2("1.9  Sensitivity")
figure(os.path.join(HERE, 'fig2_sens.png'), 6.2,
       "The two live judgements, priced: what the stake is really worth, and how much "
       "conglomerate discount the structure deserves.")
alts = D['alternatives']
rows = [["One driver at a time (all else the base)", "Automotive leg / share", "Central / share moves by"],
        [f"Terminal return {pc(0.15, 0)} (the forward model's marginal)",
         fm(alts['tv_roic_15']['auto_eq']/D['shares'], 2),
         fm((alts['tv_roic_15']['auto_eq']-dcf['auto_eq'])*L['weights']['sotp']*(1-legs['disc'])/D['shares'], 2)],
        [f"Terminal return {pc(0.20, 0)}", fm(alts['tv_roic_20']['auto_eq']/D['shares'], 2),
         fm((alts['tv_roic_20']['auto_eq']-dcf['auto_eq'])*L['weights']['sotp']*(1-legs['disc'])/D['shares'], 2)],
        [f"Gordon on year-five cash flow (July construction)",
         fm(dcf['auto_eq_gordon']/D['shares'], 2),
         fm((dcf['auto_eq_gordon']-dcf['auto_eq'])*L['weights']['sotp']*(1-legs['disc'])/D['shares'], 2)],
        ["Margin compression compounds every year",
         fm(alts['margin_compounds']['auto_eq']/D['shares'], 2),
         fm((alts['margin_compounds']['auto_eq']-dcf['auto_eq'])*L['weights']['sotp']*(1-legs['disc'])/D['shares'], 2)],
        ["Effective tax stays at the H1 41.0%",
         fm(alts['etr_stays_41']['auto_eq']/D['shares'], 2),
         fm((alts['etr_stays_41']['auto_eq']-dcf['auto_eq'])*L['weights']['sotp']*(1-legs['disc'])/D['shares'], 2)],
        ["Working capital at the FY25 year-end peak",
         fm(alts['wc_at_fy25_peak']['auto_eq']/D['shares'], 2),
         fm((alts['wc_at_fy25_peak']['auto_eq']-dcf['auto_eq'])*L['weights']['sotp']*(1-legs['disc'])/D['shares'], 2)]]
table(rows, [3.0, 1.9, 2.0], size=8.8)
P(f"The grid spans the whole disagreement: at the company's own book mark "
  f"({pc(D['sens']['mult_B'], 0)} of the round) with a 10% holding discount the sum of "
  f"the parts is worth about {ps(BW['B']['sotp'])}; at the full round mark, "
  f"{ps(BW['A']['sotp'])}. Beyond the grid: one point of automotive gross margin is "
  f"worth about {ps((dcf['auto_eq_pm1']-dcf['auto_eq_mm1'])/2/D['shares'])} per share "
  f"on the cash-flow leg; one point of discount rate about "
  f"{ps(abs(BW['A']['sotp']*0.055))} on the sum of the parts; the difference between "
  f"the two equity-premium bases is {pc(wac['wacc_rating']-wac['wacc_cds'], 2)} of "
  f"discount rate. The published bear-to-bull range is wide because the honest range IS "
  f"wide: it contains a real, unresolved factual question, not just parameter noise.")

# =====================================================================================
# 6 — SECTION 2: TECHNICAL (reproduced)
# =====================================================================================
H1("2  Technical & price structure — as published, unchanged")
P(f"This section reproduces our live page's technical read exactly as it stands. Its "
  f"own stamps: computed {pub['asof']['tech']['computed']} on price data through "
  f"{pub['asof']['tech']['data']}. This refresh did not touch it — a technical read "
  f"moves only when the price library moves.", size=9.5, italic=True, color=GREY)
P(f"Trend: {pub['tech']['trend']}.")
P(pub['tech']['summary'])
rows = [["Resistance", "Support"]]
for i in range(3):
    rows.append([fm(pub['levels']['res'][i], 2), fm(pub['levels']['sup'][i], 2)])
table(rows, [1.6, 1.6])
bullet(pub['tech']['bull'], bold_head="Bull trigger: ")
bullet(pub['tech']['bear'], bold_head="Bear trigger: ")

# =====================================================================================
# 7 — SECTION 3: PROBABILISTIC PRICE MAP (reproduced)
# =====================================================================================
H1("3  A probabilistic price map — as published, with its dates")
P(f"The published probability cone was struck on the closing library of "
  f"{pub['asof']['mc']['data']} and computed on {pub['asof']['mc']['computed']}. It is "
  f"reproduced here unchanged and is now four weeks old against this refresh: its "
  f"one-month window resolves on {pub['dist']['t20']['resolve']}, days away. Treat the "
  f"levels below as the record of what was published, not as a fresh forecast — a new "
  f"price data-set re-strikes the map on its own schedule, independently of this "
  f"fundamental refresh.", size=9.5, italic=True, color=GREY)
rows = [["Horizon", "5th", "25th", "median", "75th", "95th", "resolves"]]
for hz, lab in [('t20', '1 month'), ('t60', '3 months')]:
    d_ = pub['dist'][hz]
    rows.append([lab, fm(d_['p5'], 2), fm(d_['p25'], 2), fm(d_['p50'], 2),
                 fm(d_['p75'], 2), fm(d_['p95'], 2), d_['resolve']])
table(rows, [1.05, 0.85, 0.85, 0.85, 0.85, 0.85, 1.15])
caption(f"EGP per share, from a 50,000-path simulation anchored at the "
        f"{ps(spot)} close of {pub['asof']['mc']['data']}.")
rows = [["Price level", "Touch within 1 month", "Touch within 3 months"]]
for lvl, p1, p3 in pub['touch']:
    rows.append([fm(lvl, 2), f"{p1}%", f"{p3}%"])
table(rows, [1.4, 1.8, 1.8])
caption("Probability of trading at the level at any point inside the window, not of "
        "finishing there.")
pst = D['prior_step0']
P(f"When that map was built, the engine behind it had beaten its no-skill benchmark on "
  f"this stock's own five-year record — its probability scores were "
  f"{pc(pst['nonoverlap_skill'])} better than the benchmark on strictly non-overlapping "
  f"three-month windows and {pc(pst['monthly_skill'])} better sampled monthly, with "
  f"{pc(pst['cov90'], 0)} of outcomes inside its 90% bands ({pst['n']:.0f} windows). "
  f"Those statistics travel with the July strike; they are not re-measured here.")

# =====================================================================================
# 8 — SECTION 4: COMPARISON OF THE LENSES
# =====================================================================================
H1("4  Comparison of the lenses")
rows = [["Lens", "What it sees", "What it is blind to", "Where it lands"],
        ["Sum of the parts", "each business on its own economics; the stake at a real mark",
         "which mark is true — so it is computed twice", f"{fm(BW['B']['sotp'], 1)} or {fm(BW['A']['sotp'], 1)}"],
        ["Book & return", "the restated accounting floor", "franchise value above book; the unbooked round gain",
         fm(L['book']['base'], 1)],
        ["Relative multiples", "what buyers pay today for comparable earnings",
         "the stake entirely; the tax normalisation", fm(L['relative']['base'], 1)],
        ["Normalised power", "the business with the two distortions removed",
         "how long the distortions actually last", fm(L['normalized']['base'], 1)]]
table(rows, [1.25, 2.15, 2.15, 1.30])
P(f"The pattern is the tell: the two stake-blind lenses sit at "
  f"{fm(L['relative']['base'], 0)}–{fm(L['normalized']['base'], 0)}, the stake-aware "
  f"framings at {fm(L['central']['B'], 0)}–{fm(L['central']['A'], 0)}. The market's "
  f"August quote of {fm(D['spot_ir'], 1)} prices GB Corp as if the operating "
  f"businesses were nearly the whole story and MNT-Halan's round were mostly noise. "
  f"That is a coherent position — it is the balance-sheet framing — but it leaves the "
  f"round-mark upside as a free option on a documented, bank-led transaction.")

# =====================================================================================
# 9 — SECTION 5: CATALYSTS
# =====================================================================================
H1("5  Catalysts to watch")
bullet("MNT-Halan's second closing — size and price either validate the USD 1.4bn mark "
       "or re-price the crux directly.", bold_head="The stake: ")
bullet("The central bank's next meetings against 14.9% July inflation: each cut "
       "reprices the floating funding book downward and extends car affordability.",
       bold_head="Rates: ")
bullet("September's additional Hyundai model, the third locally assembled Changan in "
       "the fourth quarter, and the new mainstream electric brand launched in August.",
       bold_head="Launches: ")
bullet("The new bank-participation rules in securitisation: management expects delayed "
       "issuance and dearer funding in the second half, normalising thereafter.",
       bold_head="Funding plumbing: ")
bullet("Iraq and Jordan: management guides the drag to largely end from the fourth "
       "quarter — the single biggest swing to the tax rate and to reported profit.",
       bold_head="Regional: ")
bullet("Full-year 2026 results: the first print against this refresh's forecast — "
       "revenue near EGP 104bn and earnings near EGP 2.8 per share are the marks to "
       "beat.", bold_head="The next print: ")

# =====================================================================================
# 10 — SECTION 6: READING THE ZONES
# =====================================================================================
H1("6  Reading the probability zones")
P(f"The published three-month map (struck {pub['asof']['mc']['data']}) put the middle "
  f"half of outcomes between {fm(pub['dist']['t60']['p25'], 2)} and "
  f"{fm(pub['dist']['t60']['p75'], 2)}, with a median of "
  f"{fm(pub['dist']['t60']['p50'], 2)}. Overlaying this refresh's fair-value range: the "
  f"balance-sheet-mark central ({fm(L['central']['B'], 1)}) sits inside the map's "
  f"middle band — the market can reach the conservative framing on ordinary "
  f"volatility. The round-mark central ({fm(L['central']['A'], 1)}) sits near the "
  f"map's upper quartile: reaching it inside a quarter historically required either "
  f"the stake question resolving or an earnings surprise. The map is the July strike; "
  f"the overlay is today's fundamentals — read the four-week gap between their dates "
  f"accordingly.")

# =====================================================================================
# 11 — SECTION 7: CAVEATS
# =====================================================================================
H1("7  Caveats — what would change our mind")
bullet("The reviewer could not verify the MNT-Halan carrying value (second consecutive "
       "period) and the associate contributed EGP 410mn of the period's profit. If "
       "audited numbers eventually disappoint, both framings fall, not just one.")
bullet(f"{pc(dcf['tv_pct'], 0)} of the automotive enterprise value is terminal. A "
       f"one-point widening of the spread between discount rate and terminal growth "
       f"removes roughly a tenth of that leg.")
bullet("The margin path assumes exactly one more year of the measured compression, then "
       "stability. If supply keeps improving faster than localisation offsets it, the "
       "flat-after-FY27 assumption is the study's soft spot.")
bullet("The tax-rate glide to 22.5% depends on the regional losses actually ending. "
       "Each year they persist costs roughly EGP 0.4–0.5 of earnings per share against "
       "our path.")
bullet("The pound: the round mark is a dollar number. The same round is worth 6.8% more "
       "in pounds than at the July study purely from depreciation — and the mechanism "
       "runs both ways.")
bullet(f"Working capital is modelled on the measured cycle; the five disclosed quarters "
       f"span 16.7–18.9bn but the year-end build is real. A repeat of the 2025 year-end "
       f"peak (28.5% of revenue) would push the FY26E cash flow negative.")
bullet(f"The price-side of this document (the probability map and technical levels) is "
       f"dated {pub['asof']['mc']['data']} and is stale by four weeks at issue. It is "
       f"reproduced for completeness, not re-struck.")

# =====================================================================================
# 12 — APPENDIX A: STATEMENTS
# =====================================================================================
H1("Appendix A — Financial statements")
H2("A.1  Income statement — three disclosed years and the five-year model")
rows = [["EGP mn", "FY23", "FY24", "FY25"] + YRS]
def hrow(lab, hvals, fvals, d=0):
    return [lab] + [fm(v, d) for v in hvals] + [fm(v, d) for v in fvals]
rows.append(hrow("Automotive revenue", [hist[y]['auto_rev'] for y in ['FY23','FY24','FY25']],
                 [r['rev'] for r in dcf['rows']]))
rows.append(hrow("GB Capital revenue", [hist[y]['cap_rev'] for y in ['FY23','FY24','FY25']],
                 [f['cap_rev'] for f in fs]))
rows.append(hrow("Group revenue", [hist[y]['group_rev'] for y in ['FY23','FY24','FY25']],
                 [f['group_rev'] for f in fs]))
rows.append(hrow("Automotive operating profit", [hist[y]['auto_ebit'] for y in ['FY23','FY24','FY25']],
                 [r['ebit'] for r in dcf['rows']]))
rows.append(["Financing cost (automotive)", "—", "—", "—"] + [fm(-f['fin_cost'], 0) for f in fs])
rows.append(["Group net profit (attributable)"] +
            [fm(hist[y]['np'], 0) for y in ['FY23','FY24','FY25']] +
            [fm(f['group_np'], 0) for f in fs])
rows.append(["Earnings per share (EGP)"] +
            [fm(hist[y]['np']/D['shares'], 2) for y in ['FY23','FY24','FY25']] +
            [fm(f['eps'], 2) for f in fs])
table(rows, [1.80, 0.63, 0.63, 0.63, 0.66, 0.66, 0.66, 0.66, 0.66], size=8.6,
      band_rows={len(rows)-2, len(rows)-1})
caption(f"History from the company's issued statements (2026 comparatives restated where "
        f"the company restated them). The half-year already delivered: revenue "
        f"{fm(h1['rev'], 0)}mn, attributable profit {fm(h1['np'], 0)}mn, earnings per "
        f"share {fm(h1['np']/D['shares'], 3)}.")
H2("A.2  Balance sheet — the disclosed position")
hb = {y: hist[y]['bs'] for y in ['FY23', 'FY24', 'FY25']}
rows = [["EGP mn", "FY23", "FY24", "FY25 (restated)", "30-Jun-26"],
        ["Inventories", fm(hb['FY23']['inv'], 0), fm(hb['FY24']['inv'], 0), fm(hb['FY25']['inv'], 0),
         fm(D['bs']['inv_group'], 0)],
        ["Receivables & debtors (current)", fm(hb['FY23']['ar']+hb['FY23']['adv'], 0),
         fm(hb['FY24']['ar']+hb['FY24']['adv'], 0), fm(hb['FY25']['ar']+hb['FY25']['adv'], 0),
         fm(D['bs']['ar_group']+D['bs']['debtors_group'], 0)],
        ["Investments in associates", fm(hb['FY23']['assoc'], 0), fm(hb['FY24']['assoc'], 0),
         fm(hb['FY25']['assoc'], 0), fm(D['assoc_total'], 0)],
        ["Cash & equivalents", fm(hb['FY23']['cash'], 0), fm(hb['FY24']['cash'], 0),
         fm(hb['FY25']['cash'], 0), fm(D['bs']['cash'], 0)],
        ["Total assets", fm(hb['FY23']['ta'], 0), fm(hb['FY24']['ta'], 0), fm(hb['FY25']['ta'], 0),
         fm(D['bs']['ta_group'], 0)],
        ["Borrowings & overdrafts", fm(hb['FY23']['borrow'], 0), fm(hb['FY24']['borrow'], 0),
         fm(hb['FY25']['borrow'], 0), fm(D['bs']['debt_total'], 0)],
        ["Parent equity", fm(hb['FY23']['eq'], 0), fm(hb['FY24']['eq'], 0), fm(hb['FY25']['eq'], 0),
         fm(D['bs']['parent_eq'], 0)],
        ["Group net debt", fm(hb['FY23']['nd_lc'], 0), fm(hb['FY24']['nd_lc'], 0),
         fm(hb['FY25']['nd_lc'], 0), fm(D['bs']['nd_group'], 0)],
        ["Book value per share (EGP)", fm(hb['FY23']['eq']/D['shares'], 2),
         fm(hb['FY24']['eq']/D['shares'], 2), fm(hb['FY25']['eq']/D['shares'], 2), fm(D['bvps'], 2)]]
table(rows, [2.15, 1.1, 1.1, 1.25, 1.15], size=8.8, band_rows={len(rows)-1})
caption("FY25 as restated in the June-2026 statements (associates +2,460mn, receivables "
        "reclass, equity +2,883mn). The receivables line for FY23-24 groups automotive "
        "receivables and advances; from FY25 the group figures are shown.")
H2("A.3  Forecast balance-sheet and cash-flow markers")
rows = [["Marker"] + YRS,
        ["Automotive working capital", *[fm(r['wc'], 0) for r in dcf['rows']]],
        ["Automotive net debt (cash-sweep)", *[fm(f['auto_nd'], 0) for f in fs]],
        ["Associates carrying (equity-method roll)", *[fm(f['assoc_carrying'], 0) for f in fs]],
        ["Parent equity (profit less the held dividend)", *[fm(f['equity'], 0) for f in fs]],
        ["Book value per share (EGP)", *[fm(f['bvps'], 2) for f in fs]],
        ["Return on equity", *[pc(f['roe'], 1) for f in fs]],
        ["Free cash flow to the firm (automotive)", *[fm(r['fcff'], 0) for r in dcf['rows']]]]
table(rows, [2.7, 0.85, 0.85, 0.85, 0.85, 0.85], size=8.8)

# =====================================================================================
# 13 — APPENDIX B: PEERS, RISKS, RESEARCH
# =====================================================================================
H1("Appendix B — Peer frame, risk register and the research base")
H2("B.1  Peers (context only)")
rows = [["Peer", "Trailing P/E", "Note"],
        ["Contact Financial (Egypt, consumer finance)", fm(D['peers']['CNFN'], 2),
         "the direct local financing peer"],
        ["Dogus Otomotiv (Turkey, distribution)", fm(D['peers']['DOAS'], 2),
         "P/B 0.62 on inflation-restated book"],
        ["AutoNation (US, auto retail)", fm(D['peers']['AN'], 2), "forward 8.35"],
        ["Bajaj Auto (India, two-wheelers)", fm(D['peers']['BAJAJ'], 2),
         "partner brand, far richer market"],
        ["GB Corp at the July close / FY26E", fm(spot/fs[0]['eps'], 1), "on this study's forecast"]]
table(rows, [2.9, 1.2, 2.7], band_rows={5})
H2("B.2  Risk register")
rows = [["Risk", "Where it bites", "Mitigant / marker"],
        ["MNT-Halan opacity: reviewer not provided its accounts (twice)",
         "the crux — both framings", "audited numbers; the second close"],
        ["Regional losses persist (Iraq geopolitics, Jordan demand)",
         "tax rate, reported profit", "management guides the drag ending from Q4"],
        ["Securitisation rule change raises funding cost",
         "GB Capital's second half", "normalisation expected as banks adapt"],
        ["Pound step-devaluation", "costs, the dollar debt, sentiment",
         "pricing power demonstrated; stake mark rises in pounds"],
        ["Family control (63.4%)", "governance discount",
         "long listed record; institutional register"],
        ["Algeria arbitration (claim at least USD 24mn)", "one-off recovery, not modelled",
         "carried at zero in this study"],
        ["Year-end working-capital peak repeats", "FY26 cash flow",
         "five quarterly snapshots anchor the path"]]
table(rows, [2.55, 2.05, 2.30], size=8.8)
H2("B.3  The research base")
P("Built on four layers of evidence, from the inside out: the company's own issued "
  "statements and releases (the only source for its reported numbers), its investor "
  "materials, official market and country data (exchange prices, the published index, "
  "central-bank and statistics-office prints, the January-2026 country-risk tables), "
  "and finally market aggregators for peer multiples only. Every input in the model "
  "carries its value, source, date and layer in the companion bibliography document, "
  "which also lists the judgement calls and what would overturn each, the searches "
  "that returned nothing, and one material discrepancy found between aggregators. "
  f"{D['n_register']} registered inputs across the model.")

# =====================================================================================
# 14 — APPENDIX C: EXPERT PANEL
# =====================================================================================
H1("Appendix C — Three experts, one company")
E = D['experts']
H2("C.1  Expert 1 — the sum-of-the-parts practitioner")
P("Worldview: conglomerates are collections of separable claims; value each at its own "
  "economics and let the structure discount tell you about governance, not about the "
  "assets. Works best when the parts have observable marks; fails when the biggest "
  "mark is itself the question — which this expert answers by taking the most recent "
  "arm's-length transaction as primary evidence.")
rows = [["Worked valuation", "EGP mn"],
        ["Automotive equity (cash-flow model)", fm(dcf['auto_eq'], 0)],
        ["GB Capital operating equity", fm(legs['cap_oper_eq'], 0)],
        ["MNT-Halan at the round (42.93% x USD 1.4bn x 50.71)", fm(legs['mnt_round_egp'], 0)],
        ["Other associates and holdings", fm(D['other_assoc']+D['fvoci'], 0)],
        ["Sum", fm(dcf['auto_eq']+legs['cap_oper_eq']+legs['assoc_A'], 0)],
        ["Structure discount at 8% (thinner than the house 10%: a bank-led round IS the evidence)",
         fm(-(dcf['auto_eq']+legs['cap_oper_eq']+legs['assoc_A'])*0.08, 0)],
        ["Equity  /  per share", f"{fm((dcf['auto_eq']+legs['cap_oper_eq']+legs['assoc_A'])*0.92, 0)}  /  {fm(E['e1']['base'], 2)}"]]
table(rows, [4.6, 1.6], band_rows={7})
P(f"Named sensitivity: every 10% shaved off the round mark costs "
  f"{ps(legs['mnt_round_egp']*0.10*0.92/D['shares'])} per share. Falsifier, stated in "
  f"advance: the second closing completes below USD 1.4bn, or the next audited "
  f"accounts carry the stake below its current book — either overturns the primary-"
  f"evidence claim and this valuation with it.")
H2("C.2  Expert 2 — the normalised-earnings conservative")
P("Worldview: pay for demonstrated earning power, normalised for distortions you can "
  "name and date; never pay for marks you cannot audit. Works best when distortions "
  "are genuinely temporary; fails when 'temporary' becomes structural — Egypt has "
  "taught that lesson before.")
rows = [["Worked valuation", "Value"],
        ["Normalised group profit (walk in section 1.4)", fm(L['normalized']['norm_pat'], 0) + " mn"],
        ["Per share", fm(L['normalized']['norm_pat']/D['shares'], 2)],
        ["Multiple (between the local financing peer and mature retail)", fm(8.5, 1) + "x"],
        ["Value  /  range", f"{fm(E['e2']['base'], 2)}  /  {fm(E['e2']['rng'][0], 1)}–{fm(E['e2']['rng'][1], 1)}"]]
table(rows, [4.6, 1.6], band_rows={4})
P(f"Named sensitivity: if normalised funding costs land at 20% instead of 17%, the "
  f"walk loses EGP {fm(a1['nd']*0.03*(1-D['tax_statutory']), 0)}mn of profit — about "
  f"{ps(a1['nd']*0.03*(1-D['tax_statutory'])/D['shares']*8.5)} of value at the same "
  f"multiple. Falsifier: the regional losses are still distorting the tax line in the "
  f"FY27 accounts, or the easing cycle stalls with inflation re-accelerating past 20%.")
H2("C.3  Expert 3 — the returns-on-capital sceptic")
P("Worldview: a business is worth its capital employed scaled by the ratio of what it "
  "earns to what that capital costs; growth without spread is a treadmill. Works best "
  "at cycle mid-points; fails at inflection points, which it systematically "
  "undervalues — this expert accepts that bias knowingly.")
rows = [["Worked valuation", "EGP mn"],
        ["Automotive capital employed (June-26)", fm(E['e3']['ce'], 0)],
        ["Trailing return on it", pc(E['e3']['roce'], 1)],
        ["Cost of capital", pc(wac['wacc_cds'], 2)],
        ["Implied automotive enterprise value (capital x return/cost)", fm(E['e3']['ce']*E['e3']['roce']/wac['wacc_cds'], 0)],
        ["less net debt and minorities", fm(-(dcf['auto_nd']+dcf['auto_nci']), 0)],
        ["GB Capital at 0.9x operating book", fm(legs['cap_oper_eq']*0.9, 0)],
        ["Associates at 0.85x the balance-sheet carrying (no round credit)", fm(legs['assoc_B']*0.85, 0)],
        ["Equity  /  per share", f"—  /  {fm(E['e3']['base'], 2)}"]]
table(rows, [4.6, 1.6], band_rows={8})
P(f"Named sensitivity: two points of return on capital either way move this reading by "
  f"about {ps(E['e3']['ce']*0.02/wac['wacc_cds']/D['shares'])}. Falsifier: returns on "
  f"capital recover above 26% with the working-capital cycle holding — the treadmill "
  f"claim dies and the sceptic concedes the growth is funded.")
H2("C.4  Cross-examination")
bullet("Expert 2 to Expert 1: 'Your primary evidence is one round the auditor never "
       "saw close.' — Partially conceded: the first close is documented and bank-led; "
       "the second is pending. The 8% discount stands, but Expert 1 accepts the bear "
       "leg must live in the book-mark world.")
bullet("Expert 1 to Expert 3: 'You value a franchise gaining share in an 18%-growth "
       "market at its trailing return.' — Rejected by Expert 3: trailing is what is "
       "proven; the model's own forward returns barely clear the hurdle.")
bullet("Expert 3 to Expert 2: 'Your normalisation assumes the easing cycle completes "
       "on schedule.' — Conceded in part: the walk uses 17%, not the corridor's "
       "eventual floor; the bear case (0.85x profit, 7.5x) absorbs a stall.")
H2("C.5  The three in one room")
figure(os.path.join(HERE, 'figD1_experts.png'), 6.4, "Three methods, one company.")
P(f"The room agrees on more than the spread suggests: all three would own the "
  f"operating businesses near {fm(min(E['e3']['base'], E['e2']['base'], E['e1']['base']), 0)}; "
  f"the entire quarrel is the stake and the speed of normalisation. The panel's span "
  f"— {fm(E['e3']['base'], 1)} to {fm(E['e2']['base'], 1)} at the centres — brackets "
  f"the published central from both sides.")
H2("C.6  Reading the divergence")
rows = [["Assumption", "Who differs", "Worth per share"],
        ["MNT-Halan: round mark vs balance-sheet carrying", "Expert 1 vs Expert 3",
         fm(BW['gap_ps'], 2)],
        ["Normalisation completes vs trailing persists", "Expert 2 vs Expert 3",
         fm(E['e2']['base']-E['e3']['base'], 2)],
        ["Structure discount 8% vs the house 10%", "Expert 1 vs the house",
         fm((dcf['auto_eq']+legs['cap_oper_eq']+legs['assoc_A'])*0.02/D['shares'], 2)],
        ["Equity-premium basis (CDS vs rating)", "inside the house model",
         fm(abs(BW['A']['sotp']*0.055*(wac['wacc_rating']-wac['wacc_cds'])/0.01), 2)]]
table(rows, [3.1, 1.9, 1.5])

# =====================================================================================
# 15/16 — ABOUT + DISCLOSURE
# =====================================================================================
H1("About this series")
P("Standing research on Egyptian and regional listed companies: full fundamental "
  "studies, probability-calibrated price maps graded in public, and refreshes like "
  "this one whenever the company's own disclosures move the evidence. Every forecast "
  "this series publishes is dated, resolved on its date, and scored against what "
  "happened; the record — hits and misses alike — stays on the site.")
H1("Disclosure & disclaimer")
P("This document is research, not investment advice, and contains no rating and no "
  "price target. Fair values are ranges with stated assumptions; probabilities are "
  "model outputs with stated calibration records. The authors hold no position in the "
  "securities discussed. Figures derive from the company's own published statements "
  "and releases and from sourced public market data, each dated in the companion "
  "bibliography; errors are ours alone. Prices can and do leave any range. Do your "
  "own work.", size=9, color=GREY)

doc.save(OUT)
print("saved", OUT)
n_par = len(doc.paragraphs); n_tab = len(doc.tables)
print(f"paragraphs {n_par} | tables {n_tab}")
