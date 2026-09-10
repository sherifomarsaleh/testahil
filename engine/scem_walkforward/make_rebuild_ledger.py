#!/usr/bin/env python3
"""SCEM — the REBUILD LEDGER [R-REBUILD-01], built through the shared module.

The route this study took from its delivered 06-08-2026 edition to the answer this
run leaves, lever by lever, each naming the rule it serves, with an audit point
declared in advance. Written through engine/rebuild_ledger.py rather than by hand
[R-ENF-03]: a record that models the shared form is not the shared form.

EVERY 'AFTER' IS THE CENTRAL COMMITTED IN THAT COMMIT'S OWN study_numbers.json, read
back out of git, so nothing here is a reconstruction from memory.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.dirname(HERE)
sys.path.insert(0, ENGINE)
import rebuild_ledger as RL     # noqa: E402

LED = RL.Ledger(
    ticker='SCEM',
    started_at='2026-09-07',
    start_value=53.1169974189689,
    start_spot=79.00,
    audit_after=(
        "the levers serving [R-TERM-01] — the only rule THIS run applies, so the audit "
        "point is where that rule finishes moving the answer, however many places it "
        "turns out to reach. Declared before the first of them was applied, and it now "
        "carries two: the disclosed life behind the maintenance charge, and the basis "
        "the terminal is fed on. THAT IS THE MODULE'S OWN POINT — two levers serving one "
        "rule are ONE piece of evidence, and reading them as two independent "
        "confirmations that the study was too high would be counting one rule twice. "
        "[R-GAP-01]'s eight-heading review then runs on what the group leaves, in either "
        "direction, because the trigger has been two-sided since 02-Sep-2026 and this "
        "central sits ABOVE the price."),
)

LED.apply(
    name='the historicals rebuilt from the company\'s own audited statements',
    rule='SIGCM clause 1',
    after=72.58943911297973,
    why=("The first two editions took revenue, profit and the balance sheet from Global "
         "Cement, cemnet, Daily News Egypt, Arab Finance and an aggregator's carry of "
         "S&P Global Market Intelligence while SIX AUDITED PDFs SAT ONE CLICK FROM THE "
         "COMPANY'S OWN HOMEPAGE, no authentication and no portal. Every error ran the "
         "same way and every one understated the company: equity EGP 6,020.3mn filed "
         "against 5,240.0mn used, cash 4,762.3mn against 3,850.0mn, FY2025 depreciation "
         "122.6mn against 418.1mn, operating profit 3,304.1mn against an EBIT of "
         "2,640.0mn. A reviewed 31-March-2026 balance sheet carrying EGP 5,802.0mn of "
         "cash and ONE QUARTER'S PROFIT OF EGP 1,114.5mn against a full prior year of "
         "2,284.5mn had never been opened. The cost stack was worse than the balance "
         "sheet: the old model built it from four industry rules of thumb summing to "
         "EGP 2,553.7mn against a DISCLOSED materials line of EGP 3,592.5mn, and "
         "assumed a fixed cost 2.17x the company's actual one."),
    evidence=("commit 0c5d3014, 04-09-2026; engine/scem_study/filings_extract.py, whose "
              "assertions are the footings the filings themselves print"))

LED.apply(
    name='re-struck on the latest known price',
    rule='R-GAP-01',
    after=88.48522205972965,
    why=("The study was struck against the 06-August close of EGP 79.00 and the shares "
         "had risen 27.2 per cent in the month since. A fair value published against a "
         "month-old price is a comparison a reader cannot use, whatever the fair value "
         "is worth."),
    evidence='commit 2c919615; EGX close of 02-09-2026, EGP 100.50')

LED.apply(
    name='five construction standards applied together',
    rule='R-MACRO-01 / R-COC-01 / R-LENS-03 / R-BRIDGE-01 / R-ANCHOR-01',
    after=123.27165156625448,
    why=("[R-MACRO-01] the study carried an inflation ladder two points a year below the "
         "house one and a terminal growth of 5 per cent against a terminal rate built on "
         "7 — a perpetual real decline nothing disclosed (+9.3%). [R-COC-01] the cost of "
         "debt sat 81bp BELOW the sovereign that taxes the company, and the discount "
         "factors compounded in whole-year steps from t=0 so the FY2030 rate entered no "
         "factor at all (net +1.8%). [R-LENS-03] the typed 48/21/23/8 blend retired and "
         "normalised earnings dropped as a lens for this class; the central IS the "
         "cash-flow read. [R-BRIDGE-01], [R-ANCHOR-01] and [R-ENF-05] records committed. "
         "THE INTERNAL SPLIT OF THIS LEVER IS NOT FULLY RECOVERABLE FROM THE "
         "REPOSITORY — five rules moved in one commit and only three carry a measured "
         "percentage in its message — and saying so is the point of this rule: it is "
         "recorded as one lever because that is what the evidence supports, not because "
         "the rules are one piece of evidence."),
    evidence='commit 104639d8, 04-09-2026')

LED.apply(
    name='the terminal built on the disclosed SCALAR life of the dominant class',
    rule='R-TERM-01',
    after=116.92808,
    why=("The delivered edition took a 25.89-year life: note 3/2's disclosed rates "
         "resolved at the MIDPOINT of two ranges and then cost-weighted as an ARITHMETIC "
         "MEAN OF LIVES. The midpoint half is small — measured across the whole "
         "disclosed span the weighted life runs 24.71 to 27.45 years. THE AVERAGING IS "
         "THE LARGE HALF: an arithmetic mean of lives is not the quantity that turns a "
         "capital base into an annual charge, the charge-reproducing average is the "
         "harmonic one at 20.73 years, and the two disagree by 25 per cent on the SAME "
         "disclosed table with nothing in the note saying which is meant. Route one of "
         "the disclosed-life rule needs no average at all: machinery is 69.5 per cent of "
         "note 4's gross cost and note 3/2 states its rate as a SCALAR 5 per cent, so "
         "the disclosed life of the class that dominates the replacement-cost base is 20 "
         "years — the construction ARCC's own precedent adopted. THE VALIDATION THE OLD "
         "FIGURE CARRIED WAS TWO ERRORS CANCELLING: it claimed the implied rate "
         "'reproduces the filed FY2025 charge to within 1.2 per cent, 121.3 against "
         "122.6'; the 121.3 is an arithmetic-mean rate that UNDERSTATES the disclosed "
         "rates' own product of 151.5mn, and the 122.6 is depreciation AND intangible "
         "amortisation against a filed fixed-asset charge of 99.2mn. An understated rate "
         "was compared with an overstated total and they agreed."),
    evidence=('engine/scem_study/useful_lives.json, route 1; note 3/2 at printed page 8 '
              'of the FY2025 audited statements, cross-checked against the IDENTICAL '
              'table in the FY2022, FY2023 and FY2024 filings, each stating the rates '
              'are "consistent with preceeding year"'))

LED.apply(
    name='the terminal fed on the last explicit year\'s basis, not the terminal year\'s',
    rule='R-TERM-01',
    after=111.62128401804542,
    why=("engine/terminal_value.py states the contract on TerminalInputs in terms: the "
         "figures are IN THE LAST EXPLICIT YEAR'S money, not the terminal year's, because "
         "the module grows the free cash flow one year itself — tv = fcff x (1+g) / "
         "(wacc - g) already puts the first perpetuity year in the numerator and values "
         "the terminal AT THE END OF THE LAST EXPLICIT YEAR, which is where the year-five "
         "discount factor puts it. Its own words: pass a NOPAT already grown by (1+g) and "
         "the terminal is overstated by exactly (1+g), a year-seven flow discounted at "
         "the year-five factor. BOTH of this study's call sites did exactly that, "
         "multiplying nopat and dna_book by (1 + g_term) before handing them in. WHAT "
         "MAKES IT AN ERROR RATHER THAN A CONVENTION IS THAT IT WAS NOT APPLIED TO THE "
         "WHOLE FLOW: working_capital and ic_replacement in the SAME call went in "
         "ungrown, so the maintenance charge and the working-capital charge sat in year "
         "five's money while the profit they were deducted from sat in year six's. The "
         "terminal falls 8.64 per cent, enterprise value 5.75 per cent and the central "
         "4.54 per cent. Nothing else in the model moves: the explicit window's present "
         "value and the bridge are untouched, and the terminal-year diagnostics "
         "(terminal NOPAT, terminal return on capital, the reinvestment share) are "
         "terminal-year ratios by their own definition and are unchanged to the last "
         "decimal. THE CORRECTION MOVES THE ANSWER TOWARD THE PRICE AND THAT IS NEITHER "
         "A REASON TO LIKE IT NOR A REASON TO DOUBT IT — the standing rule that a "
         "correction moving the answer away from the price is not a reason to reconsider "
         "it holds equally in the other direction."),
    evidence=("engine/terminal_value.py, the TerminalInputs docstring and the nopat field "
              "comment; engine/scem_study/compute.py, the base-case terminal in "
              "build_dcf() and the terminal inside reval(), both corrected in the same "
              "pass so the sensitivity grid still centres on the published central, which "
              "that grid's own assertion enforces"))

if __name__ == '__main__':
    rec = LED.record()
    RL.assert_rebuild(rec)
    rec['_run'] = ('produced by the SCEM FUNDAMENTAL walk-forward of 07-09-2026 '
                   '[R-FCAL-01] — not the price-engine walk-forward and not the '
                   'technical one')
    rec['_start_note'] = ('the start is the 06-08-2026 DELIVERED edition\'s own '
                          'committed central of EGP 53.1170, which is also the frozen '
                          'fair-value baseline in engine/fv_movement.json (base 53.12) '
                          '— the two agree, which is the check that the route below '
                          'starts where the reader\'s number actually was')
    json.dump(rec, open(os.path.join(ENGINE, 'scem_study', 'rebuild_ledger.json'), 'w'),
              indent=1)
    print(RL.render(rec) if hasattr(RL, 'render') else '')
    print('\nBY RULE')
    for r, g in sorted(rec['rules'].items(), key=lambda kv: kv[1]['first_before']):
        print('  %-58s %8.3f -> %8.3f  %+7.1f%%'
              % (r[:58], g['first_before'], g['last_after'], 100 * g['move']))
