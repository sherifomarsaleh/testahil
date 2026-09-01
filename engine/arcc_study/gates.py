"""ARCC — the four standing gates, called in the study's OWN code.  [R-ENF-02]

A study that does not call these passes by not checking itself, which is exactly
how 63 of 90 covered names came to be not-built-ground-up while every rule
requiring it was already written down.  scripts/check_study_provenance.py runs
the same tests from outside, so this file cannot be quietly removed either.
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'arcc_walkforward'))

import research_protocol as RP                              # noqa: E402
import beta_regression as BR                                # noqa: E402

NUMBERS = os.path.join(HERE, 'study_numbers.json')

# ---------------------------------------------------------------- SIGCM -----
SIGCM = RP.SIGCMChecklist(
    historicals_official_only=True,
    forecast_ground_up=True,
    debt_lc_fx_split=True,
    asset_conversion_cycle=True,
    competitors=True,
    beta_own_history_vs_egx30=True,
    formula_based_model=True,
    flags_raised_before_issue=True,
    stop_and_inform_honoured=True,
    na_reasons={},
)

# ------------------------------------------------------- ground-up record ---
# [R-SIGCM-02] Not a boolean.  Every revenue line, its physical unit, the
# disclosure it came from, its price basis and its cost basis -- and a GAP NOTE
# on anything below `unit`, because the rule has always permitted a coarser
# level where the disclosure stops and has never permitted going quiet about it.
#
# Shares of revenue are FY2025 audited and are DERIVED so that they foot to
# 100.000% of note 4's total sales of EGP 12,447,320,081:
#   exports        note 4  total export sales           3,815,001,925  30.649%
#   other segment  note 36 other segments external        171,491,247   1.378%
#   domestic cement  note 4 total local 8,632,318,156
#                    LESS the other segment              8,460,826,909  67.973%
# The subtraction assumes ready-mix concrete and alternative fuels are sold
# domestically, which they are -- ready-mix cannot be exported. STATED, because
# the notes cross-tabulate by geography and by segment and never jointly.
LINES = [
    RP.DriverLine(
        name='Domestic cement', level='unit', share_of_revenue=0.67973,
        unit='tonnes of cement sold domestically',
        unit_source='ARCC FY2025 investor presentation, ACC sales volumes table: '
                    'local sales volume 2,923.6 kt; national market 53,992.9 kt',
        price_basis='revenue per tonne disclosed by the company (EGP 2,538 in '
                    'FY2025), split into a domestic leg escalating on Egyptian '
                    'CPI and an export leg on the EGP/USD path',
        cost_basis='cash cost per tonne disclosed by the company (EGP 1,417 in '
                   'FY2025), decomposed on note 5 of the audited filing into raw '
                   'materials, transportation and overheads, each on its own '
                   'escalator'),
    RP.DriverLine(
        name='Cement and clinker exports', level='unit', share_of_revenue=0.30649,
        unit='tonnes of cement and clinker exported',
        unit_source='ARCC FY2025 investor presentation: cement exports 629.5 kt, '
                    'clinker exports 1,300.5 kt',
        price_basis='export revenue per tonne, USD-linked, from the disclosed '
                    'export revenue of EGP 3,815mn over 1,930.0 kt',
        cost_basis='same disclosed cash cost per tonne as the domestic leg; the '
                   'company does not disclose cost separately by destination',
        gap_note=None),
    RP.DriverLine(
        name='Ready-mix concrete and alternative fuels', level='segment',
        share_of_revenue=0.01378,
        gap_note='GAP STATED. Note 36 discloses this segment\'s external revenue '
                 '(EGP 171.5mn in FY2025, 1.4% of group sales) and nothing else — '
                 'no volumes, no prices, no cost split. It is therefore built at '
                 'segment level on a domestic inflation escalator, and the study '
                 'says so. The walk-forward found this line loses to simply '
                 'freezing it, which is recorded rather than corrected: a residual '
                 'this small does not earn a driver.'),
]
# Exports carry a real gap too, and the record must say so rather than claim a
# cleaner build than the filings support.
LINES[1] = RP.DriverLine(
    **{**LINES[1].__dict__,
       'level': 'derived',
       'gap_note': 'GAP STATED. Export tonnes and export revenue are both '
                   'disclosed, so price per tonne is real — but ARCC does not '
                   'disclose cost of sales by destination, so the export leg '
                   'carries the group cash cost per tonne. Clinker is cheaper to '
                   'produce than finished cement, so this understates export '
                   'margin and overstates domestic margin by an amount the '
                   'filings do not let us size.'})


def run():
    print('ARCC study gates  [R-ENF-02]')
    RP.assert_sigcm(SIGCM)
    print('  [ok] assert_sigcm')

    summary = RP.assert_ground_up(LINES, 'ARCC')
    print('  [ok] assert_ground_up — %s' % summary)

    rec = BR.own_stock_beta('ARCC', 'EG', 'EGX')
    # TIER 2 FALLBACK, DOCUMENTED: the own-stock regression FAILS the usability
    # gate (R2 0.047 < 0.05), so the strict preference order requires a
    # same-country peer beta.  The record is passed exactly as the regression
    # returned it -- unusable and marked unusable -- rather than being quietly
    # adopted anyway, which is the defect assert_beta_provenance exists to catch.
    RP.assert_beta_provenance(rec, tier2_fallback_documented=True)
    print('  [ok] assert_beta_provenance — own-stock R2=%.3f usable=%s, fell to '
          'tier 2 peer median 1.0302' % (rec['r2'], rec['usable']))

    MODEL = RP.ModelStudyChecklist(
        structure_matches_model=True,
        bibliography_document=True,
        provenance_four_field=True,
        numeric_traceability=True,
        external_reader_scrub=True,
        figure_discipline=True,
        table_discipline=True,
        expert_appendix_max_detail=True,
        contested_judgement_both_ways=True,
        na_reasons={},
    )
    RP.assert_model_study(MODEL)
    print('  [ok] assert_model_study')

    d = json.load(open(NUMBERS))
    assert d['meta']['standard_version'] == RP.STANDARD_VERSION, \
        'study is stamped to a standard other than the live one'
    print('  [ok] standard stamp %s  [R-STD-01]' % d['meta']['standard_version'])
    return 0


if __name__ == '__main__':
    raise SystemExit(run())
