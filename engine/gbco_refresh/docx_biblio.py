"""GBCO refresh — standalone bibliography document. Reads study_numbers.json only.
Primary-documents table, the FULL input register grouped by research layer, the
judgements table with what-would-overturn-each, negative results, and aggregator
discrepancies."""
import os
from docx_base import doc, D, P, H1, H2, caption, bullet, table, GREY, BRASS

from docx.shared import Inches as _In
doc.sections[0].left_margin = doc.sections[0].right_margin = _In(0.70)
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'GBCO_Bibliography_19-08-2026.docx')

P("TESTAHIL — STANDING RESEARCH SERIES", size=9, color=BRASS, space_after=2)
P("GB Corp (GBCO.CA) — Bibliography & input register", size=20, bold=True, space_after=0)
P("Companion to the valuation study refresh of 19 August 2026", size=10, color=GREY,
  space_after=10)

H2("READ FIRST")
P("Every number in the study and the workbook traces to a row in this document. Inputs "
  "are organised in four layers, from the inside out: COMPANY (the subject's own issued "
  "statements, releases and investor materials — the only admissible source for its "
  "reported figures), COUNTRY (sovereign yields, inflation, policy rates, currency, "
  "country-risk tables), INDUSTRY (market prints and peer marks, context only), and "
  "GLOBAL (rates and supply-chain conditions). A value with no source and date does not "
  "enter the model; where a needed figure is not disclosed, the gap itself is recorded "
  "below rather than silently bridged.")

H1("Primary documents")
rows = [["#", "Document", "Publisher / date", "What was taken"],
 ["1", "Consolidated interim financial statements, 30 June 2026 (limited review, KPMG "
       "Hazem Hassan — qualified conclusion on the MNT B.V. associate)",
       "GB Corp, 13-Aug-2026", "the primary statements; segment note; borrowings and "
       "their average rates; associates note (stake 42.93%, carrying 15,723.5); the "
       "FY2025 restatement; tax reconciliation; currency exposures; commitments"],
 ["2", "2Q/1H26 earnings release", "GB Corp, 13-Aug-2026",
       "volumes and prices per line of business; quarterly working-capital and net-debt "
       "tables; segment income statements and balance sheets; GB Capital portfolio, "
       "asset quality and subsidiary detail; management guidance"],
 ["3", "Press release: MNT-Halan closes capital-increase round led by Al Ahly Capital",
       "GB Corp, 09-Jun-2026", "the USD 1.4bn round mark (first close; second pending), "
       "corroborated by Reuters, Zawya and Enterprise coverage"],
 ["4", "FY2025 statements / fourth-quarter release", "GB Corp, Feb-2026",
       "the FY25 base year (extracted for the July study, cell-verified; net-debt-to-"
       "EBITDA cross-check reproduces the disclosed 2.39x)"],
 ["5", "FY2024 statements / fourth-quarter release", "GB Corp, Mar-2025", "second history year"],
 ["6", "FY2023 statements / fourth-quarter release", "GB Corp, Mar-2024", "third history year"],
 ["7", "Investor-relations filings page (ir.gb-corporation.com)", "GB Corp, accessed 19-Aug-2026",
       "primary-access confirmation that the supplied documents are the company's own; "
       "the live EGX quote (29.70) used for market-value weights"],
 ["8", "Country risk tables (ctryprem), January 2026 edition", "A. Damodaran, NYU Stern, 05-Jan-2026",
       "Egypt: default spreads 6.37% (rating) / 3.41% (CDS); total equity premia 13.94% / 9.41%"],
 ["9", "Egypt 10-year local-currency bond quote", "investing.com, 19-Aug-2026", "22.92% observed yield"],
 ["10", "USD/EGP quote", "investing.com, 19-Aug-2026", "50.71 (52-week range 46.64-54.86)"],
 ["11", "July 2026 consumer-price print", "CAPMAS via national press, 10-Aug-2026",
        "urban inflation 14.9% year on year"],
 ["12", "July 2026 monetary-policy decision", "State Information Service / Daily News Egypt, 11-Jul-2026",
        "overnight deposit rate held at 19.00%, third consecutive hold"],
 ["13", "First-half 2026 vehicle-market prints", "AMIC via Zawya / Arab Finance, Jul-2026",
        "passenger-car market 62.3k units (+18%); total market 102.1k (+40.5%)"],
 ["14", "Peer multiple pages (Contact Financial, Dogus Otomotiv, AutoNation, Bajaj Auto)",
        "investing.com / stockanalysis.com, 19-Aug-2026", "trailing multiples, context only"],
 ["15", "GBCO daily price history and the exchange's published index series",
        "EGX via the research price library, through 22-Jul-2026",
        "the five-year weekly beta regression; the published price map's anchor close"]]
table(rows, [0.55, 2.20, 1.50, 2.85], size=8.2)

H1("The input register — every input, four fields")
P(f"{D['n_register']} inputs. Value, source and construction, date, layer. Paths are "
  f"listed FY26E through FY30E.", size=9.5, color=GREY)
by_layer = {}
for r in D['register']:
    by_layer.setdefault(r['layer'], []).append(r)
order = [('COMPANY', 'Company layer'), ('COUNTRY', 'Country layer'),
         ('INDUSTRY', 'Industry layer'), ('GLOBAL', 'Global layer')]
n = 0
for key, label in order:
    entries = by_layer.get(key, [])
    if not entries:
        continue
    H2(f"{label} — {len(entries)} inputs")
    rows = [["#", "Input", "Value", "Source & construction", "Date"]]
    for r in entries:
        n += 1
        v = r['value']
        if isinstance(v, float):
            vs = f"{v:,.4f}".rstrip('0').rstrip('.') if abs(v) < 10 else f"{v:,.1f}"
        elif isinstance(v, (list, tuple)):
            vs = ", ".join(("—" if x is None else (f"{x:,.3f}".rstrip('0').rstrip('.')
                                                   if isinstance(x, float) else str(x))) for x in v)
        elif isinstance(v, dict):
            vs = ", ".join(f"{k} {x}" for k, x in v.items())
        else:
            vs = str(v)
        src = r['source'] + ((" — " + r['note']) if r.get('note') else "")
        rows.append([str(n), r['name'], vs[:80], src[:200], r['date']])
    table(rows, [0.55, 1.95, 1.20, 2.65, 0.75], size=7.4)

H1("Judgements — and what would overturn each")
rows = [["Judgement", "Basis", "What would overturn it"],
 ["The June round (USD 1.4bn) anchors the base framing of the MNT-Halan stake; the "
  "company's book anchors the bear framing; the two are never averaged",
  "an arm's-length, bank-led first close outweighs an equity-method carrying value the "
  "reviewer could not verify",
  "the second closing pricing below USD 1.4bn; audited accounts marking the stake down; "
  "any secondary sale below the round"],
 ["Gross margin carries exactly one more year of the measured compression, then the "
  "cost-to-price relationship holds flat",
  "one year of compression is measured (15.5% to 14.3% first halves); a compounding "
  "extension is a story, and the localisation offset is real but unquantified",
  "FY27 automotive gross margin printing below 12.6% or above 14.0%"],
 ["The effective tax rate glides from 38% to the statutory 22.5% by FY30",
  "the excess over statute is unshielded regional losses; management guides the "
  "Jordanian drag ending from Q4-2026",
  "regional losses still distorting the FY27 tax line"],
 ["Working capital runs at 23.0% of revenue gliding to 21.0%",
  "the last-twelve-month measured ratio, anchored on five disclosed quarterly "
  "snapshots; FY25's 28.5% year-end was the pre-buying outlier",
  "the FY26 year-end ratio printing above 26%"],
 ["The marginal cost of debt is the disclosed 20.82% average on the EGP book",
  "essentially the whole book floats (43.5bn variable), so the current average IS the "
  "marginal rate; short tenor against a 19% corridor explains sitting under the 10-year",
  "a new fixed-rate issue materially above; the corridor re-tightening"],
 ["The debt book is carried 90% local / 10% dollar",
  "the split is not disclosed; total dollar liabilities including trade payables bound "
  "the dollar share at 17%, and dollar deposits offset most of it",
  "disclosure of a larger dollar tranche"],
 ["Currency and inflation glide paths (8%->5% depreciation, 12%->8% inflation)",
  "the realized 6.8% depreciation since July and the 14.9% July print, converging on "
  "the policy trajectory",
  "a step-devaluation; inflation re-accelerating past 20%"],
 ["GB Capital's operating leg is worth its book (6,267mn) at the centre",
  "adjusted returns of 13.5% sit below the cost of equity, against 30%+ book growth "
  "and 100% provision coverage; the local peer trades at 9.4x earnings",
  "sustained returns above 20% (re-rate above book) or a credit event (below)"],
 ["Capital-structure weights pair the group's market equity with the automotive "
  "segment's own debt",
  "the lending platform's funding belongs to its loan book, which is valued as a "
  "separate leg — mixing it into the automotive discount rate double-counts",
  "segment-level market values becoming observable (a stake sale or listing)"],
 ["Second-half volumes follow last year's measured seasonal split",
  "the 2025 halves are the only clean seasonal yardstick; three launches support the "
  "second half",
  "the third-quarter print falling far off the implied path"]]
table(rows, [2.30, 2.55, 2.25], size=8.2)

H1("Negative results — searched, not found")
rows = [["What was sought", "Where", "Outcome"],
 ["Per-tranche currency split of borrowings", "statement notes on borrowings and risk",
  "not disclosed; bounded from the currency-exposure table and flagged"],
 ["Functional cost detail below the by-nature note", "the statement notes",
  "not disclosed; ratios anchored on the half's actuals and held"],
 ["MNT-Halan financial statements for the period", "the disclosure set; public record",
  "not available — the reviewing auditor states it was not provided them either; the "
  "carrying value is therefore unverifiable from outside"],
 ["Trade or sanction actions touching Egyptian auto imports or the Bajaj/Hyundai/"
  "Changan supply chains", "press sweep, 19-Aug-2026", "nothing found"],
 ["A dated, primary print of the FY-level tires-versus-parts split for 2025",
  "the release set used for the July study", "not separately disclosed; the trading "
  "line is modelled as one"],
 ["BYD or further Chinese-brand Egypt entry on hard evidence", "press sweep",
  "market-entry chatter only; carried as a priced risk factor, not a driver"]]
table(rows, [2.60, 1.95, 2.55], size=8.4)

H1("Aggregator discrepancies")
bullet("Contact Financial's market capitalisation is quoted anywhere between EGP 4.5bn "
       "(07-Jul date) and EGP 6.6bn across services on different dates. Peer multiples "
       "are context only in this study; no subject figure relies on an aggregator.")
bullet("One bond-data service's Egypt 10-year page rendered placeholder dashes with no "
       "values; the quote was taken from a second service and dated. The two sources "
       "were not in conflict — one was simply empty.")
bullet("Dogus Otomotiv's price-to-book of 0.62 sits on an inflation-restated Turkish "
       "book value; it is not comparable to an Egyptian book and is quoted with that "
       "caveat.")

P("End of bibliography.", size=9, color=GREY, space_before=12)
doc.save(OUT)
print("saved", OUT, "| tables:", len(doc.tables), "| paragraphs:", len(doc.paragraphs))
