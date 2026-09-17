#!/usr/bin/env python3
"""The route this study took, in the order the levers were applied [R-REBUILD-01].

TWO PASSES, ONE CHAIN. L1-L9 are the 07-09-2026 rebuild from the delivered 08-07-2026
edition; L10-L19 are the response to the forensic audit of that edition, whose order was
declared in REBUILD_PLAN_17-09-2026.md and committed BEFORE any figure moved.

L10 is bookkeeping and is recorded with its full arithmetic move rather than absorbed:
the first pass walked the ROUND-PRICE branch while every committed artefact in this study
-- the numbers file, the conversion-cycle record, the gap review -- declares the CARRYING
branch as its central. That was an inconsistency in the ledger rather than a valuation
decision, and hiding it inside the next lever would have made that lever look twice the
size it is.
"""
import json
import os
import sys
from dataclasses import asdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from rebuild_ledger import Ledger, Lever, assert_rebuild, render      # noqa: E402

PRIOR = json.load(open(os.path.join(HERE, 'rebuild_ledger_07-09-2026.json'), encoding='utf-8'))

L = Ledger(
    ticker="GBCO",
    started_at=PRIOR['started_at'],
    start_value=PRIOR['start_value'],
    start_spot=PRIOR['start_spot'],
    audit_after=(
        "TWO STOPS AND ONE STANDING TRIGGER, all three declared in "
        "REBUILD_PLAN_17-09-2026.md and committed in an earlier commit than any recomputed "
        "figure. (1) AFTER L14, the inputs complete and the constructions untouched, so the "
        "construction levers are measured against a clean base -- read at -0.94% cumulative, "
        "the four input levers largely cancelling. (2) AFTER L19, the constructions "
        "complete, before any document is rebuilt. (3) STANDING, at every lever: a running "
        "total passing 10% either side of the latest known price owes [R-GAP-01]'s "
        "eight-heading review before any file is staged. The carrying branch entered this "
        "pass at +42.7% and CROSSED BACK INSIDE THE BAND AT L15, which is the crossing the "
        "plan said to watch for -- during the rebuild rather than at the end of it."),
    levers=[Lever(**{k: v for k, v in lv.items() if k in
                     ('name', 'rule', 'before', 'after', 'why', 'evidence')})
            for lv in PRIOR['levers']])


def add(name, rule, after, why, evidence):
    L.apply(name, rule, after, why, evidence)


add("L10 — the ledger tracks the study's DECLARED central, the carrying branch",
    "bookkeeping · [R-ENF-06]", 41.348367298232716,
    "Finding 1 establishes that the June-2026 round price is not one of GB Corp's own two "
    "disclosures: the study's committed record cites the company's 9-June release for the "
    "41.61% STAKE, and the round figure itself carries no source field at all. Both branches "
    "stay published and are relabelled; what changes here is only which of them this ledger "
    "walks.",
    "NO VALUATION MOVED. study_numbers.json, asset_cycle.json and GAP_REVIEW_07-09-2026.md "
    "all declare 41.3484 as this study's central and have since the 07-09 edition; the "
    "ledger walked 52.3453. The two branches were both published throughout, so a reader "
    "saw both numbers either way. Recorded at its full -21.0% rather than folded into L11, "
    "because a bookkeeping correction absorbed into a valuation lever makes that lever look "
    "twice its size.")

add("L11 — the associate carrying value, re-read off the pixels",
    "SIGCM clause 1", 41.348367298232716,
    "Audit finding 16: note 34 reads 15,723,523 thousand and the study carried 15,733,523. "
    "The delivered edition's own comment reconstructed its figure from 'restated 15,315,532 "
    "+ 8,006 of other comprehensive income + 409,985 of period profit' and recorded a "
    "'ten-thousand OCR ambiguity' in the three SMALLER rows. The ambiguity was in the MNT "
    "row itself.",
    "Re-read at 500 dpi off the rendered page, the filing carrying no text layer at all. "
    "EVERY COLUMN AND EVERY ROW FOOTS ON THE AUDIT'S FIGURE AND ON NONE OF THEM ON THE "
    "STUDY'S: 12,853,320 + 2,460,218 = 15,313,538 restated; + 409,985 profit = 15,723,523; "
    "the four rows' restated column sums to the stated 15,732,426 and the June column to the "
    "stated 16,230,465, both exactly. Two further cells of the old reconstruction were also "
    "wrong -- the restated opening is 15,313,538 and MNT has NO other comprehensive income, "
    "the 32,119 in that column being Bedaia's. THE CARRYING BRANCH DOES NOT MOVE because the "
    "residual absorbs it; the ROUND branch rises EGP 0.0092 per share, 52.345260 -> 52.354472.")

add("L12 — GB Auto net debt, at the company's own published figure",
    "[R-BRIDGE-01]", 41.46821990072005,
    "Audit finding 24, and self-audit S-2 reached independently before the audit was opened. "
    "The code claimed 'the COMPANY'S OWN definition' in a comment and produced 14,623.7 "
    "against a published 14,493.6.",
    "Reconciled to Table 7's own five rows: the delivered edition took only the NON-CURRENT "
    "portion of the notes payable to leasing (1,333.3 of 2,345.8) and omitted the "
    "due-FROM-related-parties balance of 1,142.1 that the company's own table nets. "
    "22,733.1 + 2,345.8 - 9,445.0 + 1.8 - 1,142.1 = 14,493.6 exactly. +EGP 0.1199 per share, "
    "which reproduces the self-audit's own price to the fourth decimal.")

add("L13 — the GB Capital base, struck restated against restated",
    "SIGCM clause 1", 40.387038137321575,
    "Audit finding 8: a RESTATED associate carrying value was subtracted from an UNRESTATED "
    "segment equity, halving the lender's operating base and doubling every return struck "
    "on it.",
    "Note 34's adjustment of +2,460,218 thousand raises the associate AND the equity that "
    "carries it. The 4Q25 release of 26 February 2026 predates the restatement by four "
    "months, so its 18,312.6 is the unrestated figure; 18,312.6 + 2,460.218 = 20,772.818 is "
    "the like-for-like one. The lender leg falls from EGP 1,656mn to 482mn, which is the "
    "audit's own figure to the million, -2.61% per share.")

add("L14 — the fifth GB Auto revenue line, carried rather than zeroed",
    "SIGCM clause 2", 40.96201150274129,
    "Audit finding 5: GB Auto's FY2025 total revenue is 66,358.3 and the four driver lines "
    "sum to 65,230.7. The base year carried a fifth line of 1,127.6 that the forecast did "
    "not, while the gross margin applied to that forecast is struck by the company on the "
    "WHOLE of total revenue.",
    "Two disclosed components, both named rather than merged: EGP 682.8mn of external "
    "revenue outside the four published business lines, and EGP 444.8mn of inter-segment "
    "revenue. HELD FLAT, because the company publishes no volume, price or growth rate for "
    "either. +1.42%, which is the audit's 'carried flat' price. CAUGHT BY A GATE BEFORE IT "
    "WAS CAUGHT BY ANYONE: adding the revenue without adding its driver record took the "
    "ground-up coverage to 98.9% and assert_ground_up refused the run.")

add("L15 — the walk and the bridge on one date, the intensity held at the reviewed level",
    "[R-ANCHOR-01] · [R-BRIDGE-01]", 29.94540767229232,
    "Audit finding 2, the largest in that audit and THE ONE THIS STUDY'S OWN SELF-AUDIT "
    "MISSED -- the same defect had been fixed on another name in the same session hours "
    "earlier. The cash-flow walk ran from the 31-Dec-2025 working-capital stock while the "
    "bridge deducted 30-June-2026 net debt, and the intensity then glided down a typed "
    "ladder to 21.5% on a mechanism nothing had measured.",
    "THREE PARTS, MEASURED SEPARATELY. (a)+(b) the opening stock moves to 17,092.8 at 30 "
    "June 2026 and the intensity is held flat at 22.58% -- working capital over TRAILING "
    "TWELVE-MONTH total revenue of 75,707.1 on the company's own Table 6 and Table 8 "
    "definitions, against a base-year 28.51% on the same basis -- because the stated "
    "mechanism's two halves measure in OPPOSITE directions in this company's own conversion "
    "cycle: stock build unwinding, DIO 149.0 -> 127.1 days, holds; payables re-extending, "
    "DPO 112.7 -> 83.3 days, is contradicted, and the net cycle got WORSE at 61.3 -> 69.3 "
    "days. That alone is -24.94% and lands at 30.744, against the audit's own independently "
    "derived 31.11. (c) is not the audit's and is the same defect one layer down: a bridge "
    "struck at 30 June already reflects the cash the first half produced -- net debt fell "
    "15,210.0 -> 14,493.6 -- so a FULL calendar-2026 free cash flow beside it counts that "
    "half twice. The first year's profit, depreciation and capital expenditure are scaled to "
    "the 49.77% of the year still unearned, measured from GB Auto's own disclosed first-half "
    "revenue against the model's own FY2026E. A further -2.60%.")

add("L16 — one capital structure throughout",
    "[R-COC-01]", 31.830516310283087,
    "Audit finding 11: three capital structures in one calculation -- the GROUP's borrowings "
    "and market capitalisation in the weights, a GROUP cost of debt whose numerator "
    "deliberately included GB CAPITAL's cost of funds, and the AUTO segment's net debt in "
    "the bridge. The published 22.88% landed within 0.3pp of one internally consistent "
    "pairing: right by offsetting errors, and no reader could have told.",
    "GB Auto's own book (22,733.1 of debt plus 2,345.8 of leasing notes) and its own cost of "
    "debt: the segment's finance cost over a QUARTER-WEIGHTED average of the borrowings that "
    "actually bear it, 20.02% for FY2025 and 18.20% for 1H2026 annualised, the leasing notes "
    "inside the denominator because the release's own footnote says the charge includes the "
    "leasing expense. The equity weight is a segment's, so it has no quoted price and is "
    "taken to a FIXED POINT by bisection rather than borrowed from the group's market "
    "capitalisation. Finding 4 rides with it: note 26 discloses EGP and USD average rates of "
    "21.91% and 8.30% and does NOT split the balances, so the currency weight is derived by "
    "identity and labelled derived, and the delivered edition's claim that the book was "
    "entirely local-currency is retired. WACC falls 22.88% -> 19.40% in the explicit window "
    "and the terminal barely moves, 14.18% -> 14.16%, so the answer rises 6.30%.")

add("L17 — the minority at its share of value, not at book",
    "[R-BRIDGE-01]", 31.63664910279553,
    "Self-audit S-1: the study committed NO bridge record at all, and writing one forces the "
    "minority basis to be chosen. [R-BRIDGE-01] does not permit book to be the adopted "
    "basis: the model capitalises 100% of the segment's cash flow, so the minority's claim "
    "is on the VALUE those flows produce.",
    "The basis is value_share and the proxy is named, because GB Corp does not disclose "
    "which subsidiaries carry the minority: its proportion of the segment's own disclosed "
    "book equity, 590.7 of 13,589.0 = 4.347% from Table 12, applied to the leg's equity "
    "value. Book, profit share and proportional are all published beside the adopted basis. "
    "EGP 801.2mn deducted against 590.7 at book, -0.61%. THE GRID CAUGHT IT: the sensitivity "
    "case function still deducted book and stopped reproducing the published branch inside "
    "the same run, which is the second time in this pass that a study-local assertion found "
    "a second copy of a quantity before a reader could.")

add("L18 — the relative cross-check on derived inputs",
    "depth-bar standard 3 · [R-LENS-03]", 31.63664910279553,
    "Audit findings 9, 10 and 26. The finance-cost ladder fell -4,100 -> -3,100 while the "
    "model's own markers grew borrowings 38,041 -> 66,241, with no derivation anywhere; the "
    "FY2026E group profit followed from it; and earnings per share was profit attributable "
    "to the parent divided by the share count, captioned as the company's own reporting when "
    "note 10 deducts the employees' share of profit and the board bonus first.",
    "THE CARRYING BRANCH DOES NOT MOVE and this is still a lever, because the relative lens "
    "IS the published bear: 19.59 -> 18.08, -7.7% on a number a reader is shown. The ladder "
    "is now a rate times a book -- the schedule's own forward cost of debt on GB Auto's "
    "interest-bearing borrowings held flat, scaled by the FY2025 group-to-Auto finance-cost "
    "ratio of 1.0034 -- and it comes out HIGHER than the typed one, which is the honest "
    "direction. The multiple is struck on the company's own published basic earnings per "
    "share on both sides, 1.682 / 2.609 / 2.635, moving the own-history median from 6.350x "
    "to 6.566x. The book held flat is a STATED limitation: this model has no projected "
    "balance sheet, and building one is a rebuild rather than a repair.")

_N = json.load(open(os.path.join(HERE, 'study_numbers.json'), encoding='utf-8'))
_BRANCHES = {b['label']: b['value'] for b in _N['central_two_sided']['branches']}
_CARRY = [v for k, v in _BRANCHES.items() if 'carrying' in k.lower()]
assert len(_CARRY) == 1, _BRANCHES
_AUD = _N['audit_2026_09_17']

add("L19 — the exchange rate is the house path's, with its date",
    "SIGCM clause 1 · [R-MACRO-01]", _CARRY[0],
    "Audit finding 32: EGP/USD 47.5 was typed with no source and no date on a line worth "
    "roughly half the upper branch, and the audit's complaint that four different dates were "
    "in play for one rate is exactly right.",
    "A study may not carry a currency of its own. engine/macro_paths/EG.json holds ONE dated "
    "sourced anchor for this market -- USD/EGP %.2f as at %s -- and every study reads it, "
    "which is what stops two studies valuing the same economy differently. The typed %.1f is "
    "committed beside it so the move is countable rather than described. THE CARRYING BRANCH "
    "IS UNTOUCHED, because the carrying value is already in pounds; the ROUND branch is a "
    "dollar figure and moves with the rate."
    % (_AUD['egp_usd'], _AUD['egp_usd_date'], _AUD['egp_usd_typed_before']))

if __name__ == '__main__':
    rec = asdict(L)
    for lv in rec['levers']:
        lv['move'] = lv['after'] / lv['before'] - 1.0 if lv['before'] else float('nan')
    rec['value'] = L.value
    rec['cumulative_move'] = L.cumulative
    rec['rules'] = L.by_rule()
    rec['distinct_rules'] = sorted(rec['rules'])
    rec['start_gap'] = rec['start_value'] / rec['start_spot'] - 1.0
    rec['gap'] = rec['value'] / rec['start_spot'] - 1.0
    rec['second_pass_from'] = dict(
        lever='L10', value=PRIOR['value'],
        note="the 07-09-2026 delivered edition's own answer on the branch the first pass "
             "walked; the second pass begins by moving the tracked quantity to the branch "
             "every committed artefact declares as this study's central.")
    rec['branches_at_the_end'] = _BRANCHES
    assert_rebuild(rec, 'GBCO')
    json.dump(rec, open(os.path.join(HERE, 'rebuild_ledger.json'), 'w', encoding='utf-8'),
              indent=1, ensure_ascii=False)
    print(render(rec))
    print("\ncumulative move: %+.2f%%  (%.4f -> %.4f against a spot of %.2f)"
          % (rec['cumulative_move'] * 100, rec['start_value'], rec['value'], rec['start_spot']))
    print("second pass alone: %+.2f%%  (%.4f -> %.4f), gap %+.1f%% -> %+.1f%%"
          % ((rec['value'] / PRIOR['value'] - 1.0) * 100, PRIOR['value'], rec['value'],
             (PRIOR['value'] / rec['start_spot'] - 1.0) * 100, rec['gap'] * 100))
