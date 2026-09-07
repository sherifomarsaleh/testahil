# SCEM — GAP REVIEW, 07-09-2026  [R-GAP-01]

[R-GAP-01] AUDITED CENTRAL: 111.62 — EGP 111.62 a share.
[R-GAP-01] AUDITED GAP: +11.1 per cent against the price this edition is STRUCK at,
EGP 100.50, the close of 2026-09-02 from the price file committed at
engine/prices/SUPPLIED_03-09-2026.json, read live through engine/prices/gap_today.py.

THE NEWEST PRICE THIS REPOSITORY HOLDS IS NEWER STILL AND IS DISCLOSED RATHER THAN
QUIETLY IGNORED: the persistent library at engine/raw_ohlc/EG/SCEM.csv closed at EGP 98.52 on 2026-09-06,
which puts the same central at +13.3 per cent. The audit below is unchanged by the
difference — both figures sit on the SAME side of the price and inside the same band,
so no heading of this review answers differently against one than against the other,
and neither is close to the ten-point trigger from the other direction. RE-STRIKING
THE STUDY ON THE LIBRARY CLOSE IS A SEPARATE LEVER: the spot enters the market
capitalisation and therefore the equity weight in the cost of capital, so moving it
moves the answer, and it is recorded in the rebuild ledger when it is taken rather
than folded silently into an edition that was struck on the supplied file.

THE TRIGGER IS TWO-SIDED AND THIS ONE FIRES ON THE HIGH SIDE. Since 02-Sep-2026 a central
more than ten per cent from the latest known price owes this review in EITHER direction,
because a gate that can only fire one way teaches the work to drift the other, and it does
so while looking rigorous. The question below is not whether the market is right. It is
whether WE made a mistake, and here the mistake would have to be an OPTIMISTIC one.

WHAT MOVED SINCE THE LAST REVIEW, AND BOTH LEVERS SERVE ONE RULE
  123.27   the 04-09-2026 edition, audited at +22.7 per cent
  -5.1%    the terminal LIFE: the disclosed SCALAR of the dominant class, 20 years, in
           place of a 25.89-year figure that resolved two disclosed RANGES at their
           midpoints and then averaged the five classes' LIVES arithmetically.
  -4.5%    the terminal BASIS: the flow inputs are handed to the sanctioned module in the
           LAST EXPLICIT YEAR's money, as that module's own contract requires, instead of
           pre-grown by (1+g). See heading 5.
  111.62   this edition

  Both levers serve [R-TERM-01] and together they are ONE piece of evidence, not two:
  read as a rule rather than as a pair of coincidences the terminal correction is worth
  -9.5 per cent on this study, and the rebuild ledger groups them that way.

THE REST OF THIS EDITION IS EVIDENCE RATHER THAN ARITHMETIC. It is the output of the
FUNDAMENTAL walk-forward [R-FCAL-01] — the forecasting method rebuilt at five past
origins from this company's own audited statements and scored against what it actually
reported. That is not the price-engine walk-forward and not the technical one.

---

## 1. LATEST FILINGS

**Every disclosed period has been read, and THREE MORE FILINGS WERE OPENED FOR THIS
EDITION than the last one had.** The company publishes exactly six documents and all six
are now on disk and read:

  * `SCC-AFS-E-1225.pdf` — audited, year ended 31 December 2025. Revenue, notes 24/25/26,
    note 4's fixed-asset table, note 3/2's depreciation rates, note 27's earnings-per-share
    working. The base year.
  * `SCC-AFS-E-0326.pdf` — REVIEWED, three months ended 31 March 2026, auditor's report
    dated 11 May 2026. The latest disclosed balance sheet and the sheet the bridge stands
    on: cash EGP 5,802.0mn, lease liabilities EGP 152.7mn, one quarter's profit of EGP
    1,114.5mn against a full prior year of EGP 2,284.5mn.
  * `SCC-AFS-E-1224.pdf` — audited FY2024, and the disposal gain of EGP 1,517.4mn.
  * `SCC-AFS-E-1223.pdf` — **NEW TO THIS EDITION.** Audited FY2023 with FY2022 comparatives.
  * `SCC-AFS-E-1222.pdf` — **NEW TO THIS EDITION.** Audited FY2022 with FY2021 comparatives.
  * `SCC-AFS-A-1221.pdf` — **DOWNLOADED AND UNREADABLE**, and that is recorded rather than
    passed over. It is Arabic and its figures are Eastern Arabic numerals which no OCR
    route available here reads. FY2020 is therefore left out and the walk-forward's window
    shortened rather than filled from a vendor.

Nothing is disclosed and unread. THE NEGATIVE SEARCH MATTERS AS MUCH AS THE POSITIVE ONE:
every OCR'd page of the FY2022 and FY2023 filings was searched for tonne, tons, capacity
and utilisation, and this issuer discloses NO PHYSICAL VOLUME ANYWHERE, in any year. The
capacity and utilisation the unit build runs on are industry-ring drivers from a plant
register and the trade press, not the company's own reported figures, and heading 7 prices
what that is worth.

## 2. BASE YEAR

FY2025 foots to the filed statements line by line and nothing in it is annualised, scaled
or solved. Revenue EGP 9,089.1mn, EBITDA EGP
3,455.2mn at 38.0 per cent,
depreciation and amortisation EGP 122.6mn, profit after tax
EGP 2,284.5mn — every one of them the face of the audited
statement, cross-checked two ways: the walk-forward panel and the study's own extract read
the same scans independently and agree on twenty figures, asserted rather than assumed.

The cost stack is the disclosed cost NOTE, not a per-tonne assumption: note 24's own total
plus its change in inventory IS the cost of sales the income statement prints, in every one
of the five years now on the panel, and that footing runs as an assertion at import.

**WHAT THE WALK-FORWARD SAYS ABOUT THIS BASE YEAR, WHICH IS THE POINT OF HAVING RUN IT.**
Across nine resolved driver-cells this method forecast BELOW what the company reported on
eleven of thirteen drivers — revenue by a factor of 1.75
on average, EBITDA by far more. If this study is wrong about FY2026 onward, this company's
own history says the error is more likely to be that the forecast is TOO LOW than too
high. That is evidence pointing away from the optimistic-error hypothesis this review is
required to test, and it is stated because it is inconvenient for a reviewer looking for a
reason the number is too big.

## 3. MACRO COHERENCE

Inflation, currency and price are ONE path and it is the house path [R-MACRO-01]. The
study carries no inflation number of its own; every inflation-class input is derived from
the house Egyptian ladder with its mapping declared, and the currency is relative
purchasing-power parity on that same ladder rather than hand-set. Terminal growth is
stored as a real rate on the house terminal inflation, so a perpetual real decline cannot
be typed in by accident.

The walk-forward adds an independent reading of the same question, on POINT-IN-TIME data
rather than today's: at origin FY2021 the IMF's October 2021 edition projected Egyptian
inflation of 6.7, 7.1 and 7.1 per cent for 2022 to 2024 and the outturn was 16.5, 28.9 and
26.5. Giving the model perfect foresight of that path removes 32.9 per cent
of its revenue error and 37.8 per cent of its
materials error — so a THIRD of this method's historical miss is the macro path and two
thirds is the company. The split carries its own check and it passes: depreciation, finance
expense and interest income have no inflation term in their rules and return a macro share
of zero to within a tenth of a point, by construction.

## 4. DISCOUNT RATE

The operations are discounted on the schedule the sanctioned module returns [R-COC-01] and
the cash is charged for exactly once. This is a NET CASH company — EGP
6,555.1mn at the valuation date, 21.5 per cent of the
answer — so the trap [R-BRIDGE-01] names is live here and is avoided the way that rule
requires: the operating rate is a market-value weighted cost of capital on a debt weight
of 0.52 per cent, NOT a net-debt weight that would
go negative and lever the equity weight above one, and the cash is then added at face in
the bridge and nowhere else.

**THE RECORD NOW DECLARES HOW ITS TERMINAL COST OF EQUITY WAS BUILT** [R-COC-02], which it
did not before this edition: `ke_terminal_construction` is `relevered` at a stated
22.50 per cent tax rate, because the terminal
carries a 20 per cent debt weight against half a per cent in the explicit window. Two right
answers a hundred basis points apart are indistinguishable from a typing error until the
record says which arithmetic produced them, and a rate solved out of the answer it explains
is the reverse-engineered construction this house prohibits outright — so it is declared,
not solved. `beta_source` is declared too, as `tier3_fallback` on a genuine usability-gate
failure with the diagnostics beside it.

Ordering holds: terminal 19.0 per cent below explicit
29.0 per cent, country risk counted once, cost of debt
above the sovereign.

## 5. TERMINAL

**THIS IS WHERE THIS EDITION CHANGED, AND IT CHANGED AGAINST THE VALUE.**

The terminal is built by the sanctioned module on a DISCLOSED useful life, never on the
reciprocal of the inflation rate. What moved is WHICH disclosed figure. Note 3/2 discloses
RATES rather than lives and two of its five classes are RANGES — buildings 2 to 2.5 per
cent, furniture 10 to 25. The 04-09 edition resolved both at their midpoints and then took
a cost-weighted ARITHMETIC MEAN OF LIVES, giving 25.89 years.

Two things are wrong with that and only the second is large. Resolving a range by its
midpoint is the choice this rule exists to forbid, but measured across the whole disclosed
span the weighted life only runs 24.71 to 27.45 years, so that half is small. **THE
AVERAGING IS THE LARGE HALF:** an arithmetic mean of LIVES is not the quantity that turns a
capital base into an annual charge — the charge-reproducing average is the harmonic one,
1/(cost-weighted rate) = 20.73 years — and the two disagree by a quarter on the SAME
disclosed table with nothing in the note saying which is meant.

Route one of the disclosed-life rule needs no average at all. Machinery is EGP 2,182.6mn of
note 4's EGP 3,140.9mn gross cost — 69.5 per cent — and note 3/2 states its rate as a
SCALAR five per cent. The disclosed life of the class that dominates a capacity-based
replacement-cost base is therefore 20 years, which is also the construction ARCC's own
precedent adopted, and it is adopted here. Worth −5.1 per cent.

**THE VALIDATION THE OLD FIGURE CARRIED WAS TWO ERRORS CANCELLING**, and finding that is
what a review is for. It claimed the implied rate 'reproduces the filed FY2025 charge to
within 1.2 per cent, 121.3 against 122.6'. It does — and the 121.3 is an arithmetic-mean
rate that UNDERSTATES the disclosed rates' own product of EGP 151.5mn, while the 122.6
includes intangible amortisation against a filed FIXED-ASSET charge of EGP 99.2mn. An
understated rate was compared with an overstated total and they agreed to 1.2 per cent.

**AND THE BASIS THE MODULE IS FED ON WAS WRONG IN THE SAME BLOCK, WHICH THIS REVIEW
FOUND AFTER THE LIFE WAS FIXED.** `terminal_value.py` states its contract in terms: the
inputs are in the LAST EXPLICIT YEAR's money, because the module grows the free cash flow
one year itself — the capitalisation puts the first perpetuity year in the numerator and
values the result at the end of FY2030, which is where the year-five discount factor puts
it. Both of this study's call sites handed in a profit and a book depreciation already
multiplied by (1+g). What makes that an error rather than a convention is that it was not
done to the whole flow: the maintenance charge and the working-capital charge in the SAME
call went in ungrown, so the waterfall deducted one year's costs from the next year's
profit. Corrected on both sites together, so the sensitivity grid still centres on the
published answer, which that grid's own assertion enforces. Worth -4.5 per cent: the
terminal falls 8.6 per cent, enterprise value 5.8 per cent.

Terminal free cash flow is EGP 3,677.1mn, positive, and the terminal
sits above the NOPAT-perpetuity floor of EGP 24,378.4mn. The implied replacement cycle is
26.1 years against 1/g of 14.3 — an
asset fact rather than a currency fact.

**AND THE SHORTER LIFE PRODUCED A REFUSAL WORTH REPORTING.** At this company's worst filed
EBITDA margin — FY2023's 6.6 per cent
— terminal free cash flow on the new maintenance charge turns NEGATIVE and
`terminal_value.build()` refuses outright: a going concern that consumes cash for ever is a
liquidation and must be valued as one. The 25.89-year life never met that because it
charged a fifth less maintenance. The bear bound of the range is therefore published as
what it is — the lowest margin at which the going-concern reading survives, solved on the
refusal itself and never on a value — and below it the disclosed book value is the floor.

The terminal is 64.5 per cent of enterprise value and that remains the
structural weak point of this answer.

## 6. BALANCE SHEET

The bridge stands on the LATEST disclosed sheet, the REVIEWED statement at 31 March 2026:
cash EGP 5,802.0mn and interest-bearing debt of EGP 152.7mn, the whole of which is lease
liabilities under EAS 49 — **this company has no bank borrowings at all at that date**. The
four months from the sheet to the valuation date are carried on the model's own free cash
flow, so the period is counted once. Non-controlling interests are deducted from EQUITY
value. The bridge foots and the equity divides to the stated per-share figure.

The walk-forward commits a full valuation-input block at every one of five origins — cash,
interest-bearing debt, PP&E, depreciation, the working-capital lines, capital spending and
the share count — and the share count is footed TWICE at each: issued capital over the EGP
10 par reproduces the count, and that count reproduces the year's own PRINTED earnings per
share. It changes three times over the panel, 68,058,443 to 133,065,867 to 260,812,477, so
a count carried back would have been visible as an EPS that did not reproduce.

**AND TWO BALANCE-SHEET FIGURES IN THE INPUT REGISTER WERE STILL COMING FROM THE TRADE
PRESS.** FY2024 total assets and total liabilities were sourced to "EGX filing reported by
Global Cement, cemnet/International Cement Review, Daily News Egypt and Arab Finance" —
a VENUE rather than a document, which names where the statements were lodged and did not
read them, and a plain breach of the source-integrity rule that governs every historical
this house uses. The audited FY2024 statements have been in this study's own directory
since the 04-09-2026 rebuild. Read off the balance sheet on their printed page 5, by OCR
off the rendered pixels because that filing carries no text layer at all, and footed
against the page's own arithmetic: total assets EGP 5,695.61mn, total liabilities EGP 1,959.81mn and
total equity EGP 3,735.80mn, which add exactly, as do the non-current and current subtotals.

**THE FILED FIGURES DIFFER MATERIALLY AND IN BOTH DIRECTIONS.** The relayed pair ran
12.1 per cent HIGH on assets and 17.8 per cent LOW on liabilities, so the equity they
closed to was EGP 4,775.06mn against a filed EGP 3,735.80mn — overstated by 27.8 per cent. Two
consequences follow and both are findings rather than repairs. First, FY2023 equity was
DERIVED here by rolling FY2024 equity back through FY2024 profit alone, which omits the
EGP 1,277.47mn paid in under the capital increase during that year; the filing's own comparative
column prints NEGATIVE EGP 614.03mn and the roll-back returned a positive figure whichever
totals it started from. It now carries the capital increase and reproduces the filed
number. Second, the caveat this study had carried for three editions — that the equity
roll does not close and the difference is consistent with an unitemised distribution —
was an artefact of the relayed figures: on the audited ones, FY2024 equity plus FY2025
profit gives EGP 6,020.34mn against a reported EGP 6,020.34mn, agreeing to the pound, and there is
nothing left to explain. NONE OF IT REACHES THE FAIR VALUE, which stands on the reviewed
31-March-2026 sheet and never on FY2024; what it reaches is what a reader is told about
this company's balance-sheet history.

**WHAT THE PANEL ADDS THAT THE BRIDGE DOES NOT SHOW:** in FY2023 this company carried EGP
2,608.0mn of interest-bearing debt and NEGATIVE equity of EGP 614.0mn. Three years later it
has EGP 4,762.3mn of cash and EGP 6,020.3mn of equity. The balance sheet the bridge stands
on is not a long-standing condition; it is three years old, and a reader is entitled to
know that before treating the net cash as structural.

## 7. CLAIMS AGAINST THE RECORD

Every superlative and every 'never' in the delivered documents is computed rather than
typed: `prose_check.py` reconciles 289 figures in the two delivered documents against the
model's own committed outputs and reports zero unmatched. Two figures that are real and are
not model outputs — Vicat's 77.6 per cent holding and the
corresponding 22.4 per cent float — were TYPED in nine places
across the two documents and registered nowhere; they are now four-field inputs sourced to
the Financial Regulatory Authority tender-offer filing, which is the rule working the way
it is written: a false positive is fixed by widening the rendering set, never by deleting
the figure.

**THE LARGEST CLAIM AGAINST THE RECORD THIS REVIEW FOUND IS IN THE PREVIOUS EDITION'S OWN
CAVEATS SECTION, AND IT WAS FALSE.** The delivered document of 04-09-2026 opens section 7
with "The audited statements could not be obtained" — in the very edition whose entire
historical base had been rebuilt that same day from those exact audited statements. Four
more caveats beside it described the retired vendor-sourced model: that capital expenditure
was a top-down assumption when the cash-flow statement discloses it, that the fixed cost
block was calibrated when notes 24 to 26 disclose it line by line, that the disposal gain
was estimated when the filing states it. Nothing numeric could catch any of it, because
none of it is a number. Section 7 is rewritten to what is actually true, and the general
lesson is recorded: **a rebuild that moves every number must hunt the prose that described
the old ones, and the caveats section is where stale prose survives longest precisely
because a reader trusts it most.**

Two of this study's own gates were opening the SUPERSEDED workbook by name — `recalc.py`
and `driver_test.py` both named the 04-09-2026 file while the delivered one had moved — so
the driver test was reporting green drivers against a workbook nobody ships (it now reports 52 against the delivered one). That is
L-066/L-067 recurring. Both now resolve the latest edition by date and refuse an empty
glob rather than skipping.

## 8. MULTIPLE CROSS-CHECK

At the fair value the company trades on 6.6x enterprise value to
FY2025 EBITDA and 5.6x FY2026; at the market price,
5.7x and 4.9x. On earnings the fair value
implies 12.7x FY2025 and 7.8x FY2026 against
11.5x and 7.0x at the market.

**THESE ARE NOT DEMANDING MULTIPLES AND THAT IS THE HONEST READING OF THE GAP.** A 6.6
times enterprise-to-EBITDA on a plant whose replacement cost is several times its book, in
a market where domestic consumption rose 13.4 per cent in 2025 and the production quota
regime was permanently lifted in July 2025, is not a heroic number. Some 25 per cent of
the market capitalisation is net cash, so the operating business is being asked to justify
less than it appears. Against that, seven to nine dormant Egyptian lines are under study
for revival — up to 12.6Mt, some 23 per cent of 2025 domestic consumption — landing INSIDE
this forecast window, and the kiln utilisation path is the study's largest contested
judgement, priced at 12.0 per cent of value both ways.

## VERDICT

**THE ANSWER IS AUDITED AND ONE RULE MOVED IT, IN TWO PLACES.** The terminal now stands on
the disclosed scalar life of the class that dominates its own capital base, and it is now
fed on the basis the sanctioned module's own contract states — the last explicit year's
money rather than a profit already grown a year. Together those took the central from EGP
123.27 to EGP 111.62, -9.5 per cent, and the gap from +22.7 per cent to +11.1 per cent.
Both corrections moved the answer TOWARD the price, and that is neither a reason to have
made them nor a reason to distrust them: a disclosed figure decided the first and a
documented contract decided the second, and this house has recorded before that a
correction moving the answer away from the price is not a reason to reconsider it either.
The converse of that sentence is the one that binds here.

One further defect was found and it does not touch the number: two FY2024 balance-sheet
inputs were still sourced to trade press relaying an exchange filing rather than to the
filing itself, while the audited statements sat in this study's own directory. They are
re-sourced, the filed figures differ by up to 28 per cent on the equity they close to, and
the equity-roll caveat this study had carried for three editions turns out to have been an
artefact of the relayed numbers rather than a distribution. See heading 6.

Nothing else in the eight headings produced a defect that changes the number. What they
produced instead is a set of things a reader should know: that this issuer discloses no
volume at all, so the physical build rests on industry sources; that the net cash position
is three years old rather than structural; that two thirds of this method's historical miss
on this company is the company rather than the macro path, and that the miss ran BELOW the
outturn on eleven of thirteen drivers.

**THE REMAINING GAP IS NOT CLAIMED AS A MARKET ERROR.** [R-GAP-02]'s publish block is
one-sided and does not hold a study above the price, so no dissent is filed and none is
implied; publishing to the live site remains a separate, explicitly-requested step and this
campaign never publishes.
