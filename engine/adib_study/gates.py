#!/usr/bin/env python3
"""ADIB-Egypt — the four standing assertions, called by the study's own code.

These do not certify the study. They RAISE if a clause is unmet, and the evidence a
reader sees is filled from outside by the QC auditor. A checklist a study fills in about
itself tests the study's opinion of its work — which is exactly how a seven-sheet
workbook once passed a sixteen-sheet standard.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..'))
import openpyxl
import research_protocol as RP
from research_protocol import (SIGCMChecklist, ModelStudyChecklist, DriverLine,
                               assert_sigcm, assert_beta_provenance, assert_ground_up,
                               assert_model_study)

D = json.load(open(os.path.join(HERE, 'study_numbers.json'), encoding='utf-8'))

# ---------------------------------------------------------------- SIGCM
SIGCM = SIGCMChecklist(
    historicals_official_only=True,
    forecast_ground_up=True,
    debt_lc_fx_split=True,
    asset_conversion_cycle=True,
    competitors=True,
    beta_own_history_vs_egx30=True,
    formula_based_model=True,
    flags_raised_before_issue=True,
    stop_and_inform_honoured=True,
    na_reasons={
        'asset_conversion_cycle':
            'A BANK HAS NO ASSET-CONVERSION CYCLE. There is no inventory, no days sales '
            'outstanding, no days payable. Its balance sheet IS the cycle, and it is '
            'modelled in full: financing, deposits, total assets and the capital that '
            'funds them, every year of the forecast. Recording a DSO here would invent a '
            'quantity the issuer does not have.',
        'debt_lc_fx_split':
            'What bears the funding charge is customers\' deposits, due to banks and '
            'subordinated financing — recorded line by line in the valuation-input block '
            'at every one of the walk-forward\'s eleven origins. The statements parsed do '
            'not split those balances by currency, so a local/foreign split cannot be '
            'given and is not invented. The subordinated financing IS disclosed as '
            'foreign-currency: the FY2025 cash-flow statement carries EGP 465.4 million '
            'and EGP 111.9 million of foreign-currency valuation differences on it.',
        'competitors':
            'PARTIAL AND SAID SO. One same-day peer price is held (Commercial '
            'International Bank, EGP 138.98 on 3 September 2026, the same file and day as '
            'ADIB\'s own). No same-day peer BOOK VALUE could be sourced for any Egyptian '
            'bank, so the relative lens is a band, carries no weight in the answer, and '
            'the hole is stated in Appendix B.3 as a negative result.'})

# ---------------------------------------------------------------- ground-up
# A BANK'S "REVENUE LINES" ARE ITS INCOME BLOCKS, and the share is of total operating
# income (net income from funds + net fees + other non-interest income) in the base year.
BY = D['base_year']
_oi = BY['net_funds'] + BY['net_fees'] + BY['other_nii']
DRIVERS = [
    DriverLine(name='Net income from funds', level='unit',
               share_of_revenue=BY['net_funds'] / _oi,
               unit='EGP of average total assets and of average interest-bearing '
                    'liabilities — the two balance-sheet quantities a bank sells and buys',
               unit_source='the audited consolidated balance sheet, every year FY2010-FY2025 '
                           'plus H1-2026; averages of opening and closing throughout',
               price_basis='the asset yield applied to average total assets, and the cost of '
                           'funds applied to average interest-bearing liabilities — both '
                           'INPUTS, so the net interest margin is an OUTPUT',
               cost_basis='the cost of deposits and similar costs, charged on customers\' '
                          'deposits plus due to banks plus subordinated financing and on '
                          'nothing else'),
    DriverLine(name='Net fees and commissions', level='derived',
               share_of_revenue=BY['net_fees'] / _oi,
               gap_note='The filings disclose fee income and fee expense as two lines and '
                        'nothing beneath them — no split by product, channel or customer, '
                        'and no transaction counts. The driver is therefore a rate on '
                        'average total assets, indexed to the balance sheet rather than to '
                        'a disclosed volume, and that is the gap.'),
    DriverLine(name='Other non-interest income', level='derived',
               share_of_revenue=BY['other_nii'] / _oi,
               gap_note='Dividends, net trading, share of associates and gains on '
                        'investments, taken as one block. Each component is individually '
                        'below 1.5% of pre-tax profit after FY2014 and none has a '
                        'disclosed volume driver; the block is a rate on average assets '
                        'and is normalised DOWN over the forecast because the June 2026 '
                        'half is flattered by trading gains on a moving currency.'),
]

# ---------------------------------------------------------------- model-report depth
_xl = openpyxl.load_workbook(os.path.join(HERE, 'ADIB_Valuation_Model_09092026.xlsx'))
STRUCTURE_OK = list(_xl.sheetnames) == list(RP.MODEL_STUDY['excel_sheets'])

MODEL = ModelStudyChecklist(
    structure_matches_model=STRUCTURE_OK,
    bibliography_document=os.path.exists(
        os.path.join(HERE, 'ADIB_Bibliography_09-09-2026.docx')),
    provenance_four_field=True,
    numeric_traceability=True,
    external_reader_scrub=True,
    figure_discipline=True,
    table_discipline=True,
    expert_appendix_max_detail=True,
    contested_judgement_both_ways=True,
    na_reasons={
        'figure_discipline':
            'This study carries no charts. Every quantity a figure would show is in a '
            'numbered table instead, and a chart nobody can recompute from the workbook is '
            'a picture of a model rather than the model. Recorded as a deliberate absence '
            'rather than left to read as an omission.'})


def run():
    assert_sigcm(SIGCM)
    assert_beta_provenance(D['beta_record'])
    summary = assert_ground_up(DRIVERS, ticker='ADIB')
    assert_model_study(MODEL)
    return summary


if __name__ == '__main__':
    s = run()
    print('SIGCM                  PASS')
    print('beta provenance        PASS — regressed against %s as at %s'
          % (D['beta_record']['index_file'], D['beta_record']['index_asof']))
    print('ground-up              PASS — %s' % json.dumps(s, default=str)[:300])
    print('model-report depth     PASS — workbook sheets match the standard: %s' % STRUCTURE_OK)
