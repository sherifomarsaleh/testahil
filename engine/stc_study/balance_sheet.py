"""STC — why the forecast balance sheet is NOT built, and what the valuation stands on instead.

SIGCM clause 4 wants the balance sheet projected from the asset-conversion cycle, and clause
7 wants a live formula model running driver to income statement to balance sheet to cash
flow. The working-capital half of that is done and committed (working_capital.py). THE
SHEET ITSELF CANNOT CARRY THE REST, and the reason is a defect in the primary document.

THE REVIEWED INTERIM'S OWN BALANCE SHEET DOES NOT FOOT IN ITS CURRENT COLUMN. Every
prior-year column foots to zero and every current one fails — four subtotals and both
totals. That is not an extraction problem and it was not assumed to be one: the file was
re-fetched from the company's own site, re-extracted, and then RE-READ BY OCR OFF THE
RENDERED PIXELS at 300 dots per inch, per SIGCM's own instruction that arithmetic is the
arbiter and not the extractor's confidence. Both routes return the same figures. The
December column reproducing perfectly from the same routes is what rules the extractor out:
a broken extractor does not fail one column of a two-column table and leave the other exact.

SO THE SHEET IS NOT USED AS A BASE FOR A PROJECTION. A statement is accepted only if it
foots against its own arithmetic, and this one does not; solving for the figures that would
make it foot would be inventing them, and the identity cannot say WHICH of the six in each
block is wrong.

WHAT THE VALUATION ACTUALLY STANDS ON IS CORROBORATED SOMEWHERE ELSE, and that is why the
bridge is sound while this projection is not. Each line the enterprise-to-equity bridge uses
reconciles against the interim's own CASH FLOW statement rather than against the failing
subtotals: cash of 12,940,389 plus 6,000,384 at the bank is the 18,940,773 closing balance
that statement states, TO THE RIYAL; and borrowings of 22,094,126 plus 1,442,428 roll from
the audited 15,191,428 through the same statement's own 8,720,100 drawn and 346,194 repaid,
which the cost-of-capital schedule already asserts to twelve basis points.

A LINE CORROBORATED BY A SECOND STATEMENT IS EVIDENCE; A SUBTOTAL THAT DOES NOT FOOT IS NOT.
The bridge uses the first kind and the projection would have needed the second.

WHAT WOULD UNBLOCK IT: the FY2026 audited statements, whose December column can be expected
to foot as every audited December column here does, or an interim whose current column
reproduces.
"""
from __future__ import annotations

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

SOURCE = ("the reviewed interim condensed consolidated statement of financial position at "
          "30 June 2026, re-fetched from the company's own site, re-extracted, and re-read "
          "by OCR off the page rendered at 300 dots per inch")
AS_AT = '2026-06-30'

BLOCKS = {
    'non-current assets': dict(
        jun=[42_732_448, 702_617, 17_097_769, 1_761_166, 12_909_648, 1_287_416, 22_280_131],
        jun_total=98_770_994,
        dec=[43_286_335, 864_066, 17_325_168, 1_740_608, 12_935_637, 1_407_043, 21_902_057],
        dec_total=99_460_914),
    'current assets': dict(
        jun=[1_781_441, 9_971_423, 26_727_997, 9_494_602, 1_062_181, 12_940_389, 6_000_384,
             247_643],
        jun_total=68_226_960,
        dec=[1_923_203, 8_427_932, 26_727_198, 5_593_303, 1_704_161, 7_161_953, 6_214_118,
             263_887],
        dec_total=58_015_755),
    'non-current liabilities': dict(
        jun=[22_094_126, 6_291_164, 1_642_836, 680_466, 418_768, 7_199_836],
        jun_total=37_327_166,
        dec=[14_404_268, 5_152_157, 1_714_519, 1_271_654, 482_373, 7_892_783],
        dec_total=30_917_754),
    'current liabilities': dict(
        jun=[21_198_207, 3_727_610, 606_300, 1_167_743, 1_442_428, 616_066, 13_199_380],
        jun_total=41_967_634,
        dec=[22_259_436, 4_088_197, 923_193, 1_533_741, 787_160, 538_711, 10_042_137],
        dec_total=40_172_575),
}
TOTAL_ASSETS = dict(jun=166_996_964, dec=157_476_669)
TOTAL_LIABILITIES = dict(jun=79_284_799, dec=71_090_329)

CORROBORATED = {
    'cash': dict(
        value=12_940_389, plus_bank=6_000_384, closing_per_cash_flow=18_940_773,
        how="the interim cash-flow statement's own closing balance, to the riyal"),
    'borrowings': dict(
        value=22_094_126 + 1_442_428, audited_open=15_191_428, drawn=8_720_100,
        repaid=346_194,
        how="rolls from the audited FY2025 book through the interim cash-flow statement's "
            "own financing movements, asserted to twelve basis points by the "
            "cost-of-capital schedule"),
}


def residuals():
    out = {}
    for name, b in BLOCKS.items():
        out[name] = dict(jun=sum(b['jun']) - b['jun_total'],
                         dec=sum(b['dec']) - b['dec_total'])
    for col in ('jun', 'dec'):
        out.setdefault('assets against the stated total', {})[col] = (
            BLOCKS['non-current assets']['%s_total' % col]
            + BLOCKS['current assets']['%s_total' % col] - TOTAL_ASSETS[col])
        out.setdefault('liabilities against the stated total', {})[col] = (
            BLOCKS['non-current liabilities']['%s_total' % col]
            + BLOCKS['current liabilities']['%s_total' % col] - TOTAL_LIABILITIES[col])
    return out


def check():
    """The finding is asserted so it cannot quietly stop being true.

    If a later filing makes the June column foot, THIS FAILS — and it should, because the
    reason this study does not build a forecast balance sheet would have gone away and
    somebody has to notice.
    """
    problems = []
    r = residuals()
    if not any(v['jun'] for v in r.values()):
        problems.append('the June column now foots everywhere. The reason this study does '
                        'not build a forecast balance sheet has gone away and the '
                        'projection should be built.')
    bad_dec = {k: v['dec'] for k, v in r.items() if v['dec']}
    if bad_dec:
        problems.append('the prior-year column no longer foots either, which would make '
                        'this an extraction problem after all rather than a defect in one '
                        'column: %s' % bad_dec)
    c = CORROBORATED['cash']
    if c['value'] + c['plus_bank'] != c['closing_per_cash_flow']:
        problems.append("cash no longer reconciles to the cash-flow statement's closing "
                        'balance, which is the corroboration the bridge rests on')
    return problems


def record():
    return dict(ticker='STC', as_at=AS_AT, source=SOURCE,
                residuals=residuals(), corroborated=CORROBORATED,
                forecast_balance_sheet_built=False,
                reason=("the reviewed interim's balance sheet does not foot in its CURRENT "
                        'column — four subtotals and both totals — while every prior-year '
                        'column foots exactly, on the text layer and on OCR off the '
                        'rendered pixels alike. A statement is accepted only if it foots '
                        'against its own arithmetic; solving for the figures that would '
                        'make it foot would be inventing them, and the identity cannot say '
                        'which of the six in each block is wrong.'),
                unblocked_by=('the FY2026 audited statements, whose December column can be '
                              'expected to foot as every audited December column here '
                              'does, or an interim whose current column reproduces'))


if __name__ == '__main__':
    problems = check()
    for p in problems:
        print('FAIL', p)
    r = residuals()
    print('%-38s %14s %14s' % ('', '30 Jun 2026', '31 Dec 2025'))
    for k, v in r.items():
        print('%-38s %+14s %+14s' % (k, format(v['jun'], ','), format(v['dec'], ',')))
    print()
    print('Every prior-year column foots to zero and every current one fails, on the text')
    print('layer and on OCR off the page at 300 dots per inch alike. The forecast balance')
    print('sheet is NOT built, and the reason is recorded rather than papered over.')
    print()
    print('What the bridge uses is corroborated by a SECOND statement:')
    c = CORROBORATED['cash']
    print('  cash       %s + %s = %s, %s'
          % (format(c['value'], ','), format(c['plus_bank'], ','),
             format(c['closing_per_cash_flow'], ','), c['how']))
    b = CORROBORATED['borrowings']
    print('  borrowings %s, %s' % (format(b['value'], ','), b['how']))
    if not problems:
        with open(os.path.join(HERE, 'balance_sheet.json'), 'w') as f:
            json.dump(record(), f, indent=1)
        print('\nwrote balance_sheet.json')
    raise SystemExit(1 if problems else 0)
