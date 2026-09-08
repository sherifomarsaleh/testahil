"""SWDY's rebuild ledger [R-REBUILD-01] — the levers in the order applied.

The audit point was declared BEFORE the sequence was built: stop and run [R-GAP-01]'s
eight headings after the last lever that MOVES THE CENTRAL, and before any file is
staged. That is the terminal-basis lever; the workbook lever after it moves the
workbook's published answer and not the study's.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
# The shared instrument is imported, never reimplemented [R-ENF-03]. It is loaded by
# path and REGISTERED in sys.modules first, because it defines dataclasses and
# dataclasses resolves annotations through sys.modules at class-creation time.
import importlib.util as _ilu
_spec = _ilu.spec_from_file_location(
    'engine_rebuild_ledger', os.path.join(os.path.dirname(HERE), 'rebuild_ledger.py'))
RL = _ilu.module_from_spec(_spec)
sys.modules['engine_rebuild_ledger'] = RL
_spec.loader.exec_module(RL)

L = RL.Ledger(
    ticker='SWDY',
    started_at='the delivered edition of 05-08-2026 as it stood on 7 September 2026',
    start_value=55.482176,
    start_spot=105.20,
    audit_after='terminal flows on the last-explicit-year basis')

L.apply(
    'the disclosed useful life at full precision', 'R-TERM-01', 55.479725,
    why='The life was registered as 17.26 and the identity resolves to 17.2627. A record '
        'storing a ROUNDED figure is its own failure: nothing about note 17 is uncertain '
        'to two decimal places, and the terminal is built on this number.',
    evidence='swdy_study/useful_lives.json. Route one FAILS on this name — the policy '
             'note discloses five RANGES and no scalar, machinery (65% of the depreciable '
             'base) spanning 5 to 15 years. Route two gives 17.2627 from average '
             'depreciable gross cost over the year\'s own charge, corroborated twice: the '
             'same note a year earlier gives 17.9761, and the composite implied by '
             'charging every class at the LONG END of its own range gives 17.3041 — '
             'agreement to 0.24%.')

L.apply(
    'the strike moved to the latest known price', 'R-GAP-01', 56.264792,
    why='The study was struck at EGP 105.20 of 5 August 2026. NO STUDY IS DELIVERED '
        'AGAINST A STALE PRICE: the latest committed close is EGP 130.00 of 3 September '
        '2026, so the valuation date moves with it and the anchor roll lengthens from 217 '
        'days to 246. The market-value equity weight moves with the price too, which '
        'takes the explicit-window cost of capital from 26.63% to 26.94%.',
    evidence='engine/prices/SUPPLIED_03-09-2026.json. The same file records that the '
             'figure first arrived as 90.50 and was CORRECTED to 130.00 on 6 September '
             '2026 after disagreeing with this name\'s own price library on all 35 '
             'overlapping sessions after 14 June 2026.')

L.apply(
    'terminal flows on the last-explicit-year basis', 'R-TERM-01', 52.696890,
    why='THE MODULE GROWS THE FLOWS ONE YEAR ITSELF AND THIS STUDY HAD ALREADY GROWN '
        'THEM. terminal_value.TerminalInputs says so in its first sentence and warns in '
        'terms that a NOPAT handed in already grown by (1+g) overstates the terminal by '
        'exactly (1+g) — a year-seven flow discounted at the year-five factor. NOPAT, '
        'book depreciation and the working-capital base were all multiplied by 1.07 '
        'before being passed to a function that multiplies by 1.07 again. The terminal '
        'carries 84% of enterprise value here, so the error is the answer.',
    evidence='The module\'s own note records that SIX OF EIGHT CALLERS read the field '
             'the other way on 4 September 2026; this study was one of them and was not '
             'corrected then. Terminal value 319,477 -> 298,577 EGP mn. THE CORRECTION '
             'LOWERS THE VALUE, moving it further from the traded price, which is the '
             'only direction that proves the discipline is not fitting to a quote.')

L.apply(
    'the workbook publishes the answer the study publishes', 'depth-bar standard 3',
    52.696890,
    why='The delivered workbook published EGP 59.3132 where the delivered document '
        'published 55.4822, +6.9%, with ZERO formula errors — two builder defects pulling '
        'OPPOSITE ways, and the builder\'s own expected-value map holding the right figure '
        'for both cells. DCF!C25 still carried the g x IC reinvestment identity '
        '[R-TERM-01] retired, which compute.py computes and labels "published unused, '
        'feeds nothing" (-6.5% alone); SOTP Bridge!C12 carried no line for the employees\' '
        'statutory share the model deducts at 12.19% (+14.4% alone). THE STUDY\'S CENTRAL '
        'DOES NOT MOVE HERE; the workbook\'s published answer moves 59.3132 -> 52.6969.',
    evidence='recalc.py named all 27 disagreeing cells in under a second and had simply '
             'not been run after the last rebuild. It now reports 594 formulas, 0 '
             'unresolvable, 594 cell-level agreements and 41 headline reconciliations '
             'passed. Two of its own headline addresses were ALREADY STALE and had been '
             'reporting as mismatches rather than being fixed — Summary C12 is EMPTY and '
             'read as 0.0000, which the tolerance turned into a difference rather than an '
             'error [L-066/L-067].')

rec = L.record()
rec['workbook_answer'] = dict(before=59.313220, after=52.696890,
                              note='the workbook is the artefact a reader receives; its '
                                   'own answer is tracked beside the study\'s')
rec['also_carried'] = [
    "[L-294] applied to EVERY lens that produces a per-share equity value, not only to "
    "the cash-flow lens. The employees' statutory share was charged in the bridge, the "
    "currency alternative, the sensitivity helper and the scenarios, and NOT in the three "
    "cross-checks a reader is shown beside the central, so the same company was worth "
    "12.19% more per share depending on which lens was reading it. Relative 80.58 -> "
    "71.64, normalised 109.52 -> 97.90. THE CENTRAL IS UNMOVED: under [R-LENS-03] the "
    "class primary IS the central and the cross-checks are published beside it.",
    "The terminal's own record is now COMMITTED beside the DCF block. Without it the "
    "workbook cannot build the sanctioned construction as live formulas and has to carry "
    "a number - which is how the retired g x IC formula survived in DCF!C25 while "
    "compute.py had already moved off it [R-ENF-06].",
]
RL.assert_rebuild(rec, 'SWDY')
json.dump(rec, open(os.path.join(HERE, 'rebuild_ledger.json'), 'w'), indent=1)
print('SWDY rebuild ledger — %d levers, %d distinct rules' % (len(rec['levers']),
                                                              rec['distinct_rules']))
for lv in rec['levers']:
    print('  %-52s %8.4f -> %8.4f  %+7.2f%%   [%s]'
          % (lv['name'][:52], lv['before'], lv['after'], 100 * lv['move'], lv['rule']))
print('  %-52s %8.4f -> %8.4f  %+7.2f%%' % ('CUMULATIVE', rec['start_value'], rec['value'],
                                            100 * rec['cumulative_move']))
print('  audit declared after: %s' % rec['audit_after'])
