#!/usr/bin/env python3
"""SWDY -- the [R-BRIDGE-01] enterprise-to-equity bridge record, READ OUT of the
committed numbers rather than typed.

WHY IT DID NOT EXIST. check_bridge.py listed this name as "carries no bridge
record", which is not the same thing as a bridge that is wrong: the study builds a
perfectly explicit bridge in compute.py and prints it in the delivered document, and
nothing outside the study could read it, because [R-BRIDGE-01] asks for a record of
the CHOICES (which sheet, which minority basis, cash charged how often) and the study
committed only the resulting numbers. A number cannot be checked for a choice.

IT READS study_numbers.json AND RUNS NOTHING. That is deliberate and it was learned
the expensive way in this very pass: compute.py WRITES study_numbers.json, so a
record generator that imports compute.py to get its figures silently reverts every
other record already added to that file. The anchor record was written, then wiped by
exactly that, and the working tree came back byte-identical to HEAD -- which reads
like nothing happened rather than like something was lost. Every figure below is read
from the committed `dcf` block and the input register, and the build order is
recorded in build_records.py.

WHAT THE RECORD SAYS, AND TWO OF THE FOUR ANSWERS ARE UNCOMFORTABLE. The record is
committed as the model actually computes, not as the rule would like:

  (1) THE SHEET IS 31-DEC-2025 AND THE LATEST DISCLOSED IS 30-JUN-2026. The study
      argues its case at length and the argument is real -- the valuation is STRUCK
      at the December sheet and rolled forward, the June deterioration is the same
      working-capital absorption the FY2026 forecast already carries, and deducting
      it in the bridge as well would charge one outflow twice. [R-BRIDGE-01] does
      not admit that argument, and the honest thing is to record the construction
      as it is and let the gate say so, rather than to describe the bridge as
      standing on a sheet it does not stand on.

  (2) CASH IS NETTED IN THE DISCOUNT-RATE WEIGHTS AND ADDED BACK IN THE BRIDGE. The
      adopted weights are net (debt weight 6.88% against a gross 18.34%) and the
      bridge deducts NET financial debt, which is deducting gross debt and adding
      the cash back at face. That is defect (iii) of [R-BRIDGE-01] arriving on a
      net-DEBT company rather than a net-cash one, so it runs the other way: net
      weights UNDERSTATE the debt weight, and with a cost of debt far below the cost
      of equity that RAISES the discount rate and LOWERS the value. The correction
      is worth about 2.4 points of discount rate and it moves the answer UP, toward
      a price this study sits far below. It is recorded here and NOT applied in this
      pass, because a lever is taken one at a time with its own ledger entry
      [R-VCAL-01, R-REBUILD-01] and the direction it happens to point is not a
      reason to hurry it or to hold it.

The other two are clean and are worth naming for the same reason: the minority is
deducted from EQUITY value rather than enterprise value, and the bridge FOOTS -- the
lines sum to the equity value and the equity value divides to the published central,
asserted here rather than assumed.

    python3 bridge_record.py        adds `bridge_record` to study_numbers.json
"""
import io, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import research_protocol as RP                                   # noqa: E402

PATH = os.path.join(HERE, 'study_numbers.json')
D = json.load(open(PATH, encoding='utf-8'))
V = {k: x['value'] for k, x in D['inputs'].items()}
DCF = D['dcf']

SH = float(V['shares_mn'])
EV = float(DCF['ev'])
ND = float(DCF['nd'])
ASSOC = float(DCF['assoc'])
NCI_VAL = float(DCF['nci_val'])
NCI_SHARE = float(DCF['nci_share'])
EQ_ATTR = float(DCF['eq_attr'])
ROLL = float(DCF['roll'])
PS = float(DCF['ps'])

# derived by identity from figures the file already carries -- nothing typed
EQ_PRE_NCI = EV - ND + ASSOC
EMP_CHARGE = EQ_PRE_NCI - NCI_VAL - EQ_ATTR
ACCRETION = EQ_ATTR * (ROLL - 1.0)
# THE ROLLED DIVIDEND, READ FROM THE MODEL AND NOT RE-DERIVED. This line used to
# read `V['dps_fy25'] * SH`, which deducts the dividend as if it left at the anchor.
# It left on 4 June 2026 and the model rolls it forward from that date; re-deriving
# it here made the bridge record disagree with the study it records by 12 piastres a
# share. A second reader of one fact is a defect even when it is three characters
# long [R-ENF-03] — so there is one reader now, and it is the model.
DIVIDEND = float(DCF['div_at_anchor']) * SH
EQUITY_AT_ANCHOR = EQ_ATTR + ACCRETION - DIVIDEND

# ARITHMETIC IS THE ARBITER. The bridge must reach the published central from the
# published enterprise value, or one of the two is wrong.
assert abs(EQUITY_AT_ANCHOR / SH - PS) < 1e-6, (
    'the bridge reaches %.6f a share against a published %.6f' % (EQUITY_AT_ANCHOR / SH, PS))

BS_DATE = '2025-12-31'
LATEST = '2026-06-30'

record = dict(
    rule='R-BRIDGE-01',
    balance_sheet_date=BS_DATE,
    latest_disclosed_date=LATEST,
    latest_disclosed_source=(
        "The study's own committed input register (study_numbers.json `inputs`), whose "
        "H1-2026 constant names the reviewed condensed interim consolidated financial "
        "statements for the six months ended 30 June 2026, approved for issuance on 11 "
        "August 2026 and published on the company's own investor-relations archive. Every "
        "H1-2026 figure in this study -- revenue, operating profit, segment revenue and "
        "profit, net financial debt, cash, borrowings, investees and the minority's share "
        "of profit and of equity -- is registered against that document with its date and "
        "layer, so the latest disclosed sheet is established from a register rather than "
        "asserted."),
    balance_sheet_reason=(
        "The bridge deducts net financial debt at 31 December 2025, the audited date the "
        "valuation is STRUCK at, and every lens is then rolled to the 3 September 2026 "
        "anchor at the cost of equity net of the dividend paid inside the window. The "
        "study's own stated reason for not using the June sheet is that the "
        "{0:+,.0f} deterioration over the half is the same working-capital absorption the "
        "model's FY2026 forecast already carries, so deducting it again in the bridge "
        "would charge one outflow twice. THE RULE DOES NOT ADMIT THAT ARGUMENT and the "
        "record does not pretend otherwise: the construction is committed as it is, this "
        "study stays on the bridge ratchet, and the re-strike onto the June sheet -- which "
        "moves the explicit window's start with it -- is a rebuild rather than a patch."
        .format((float(V['h1_26_debt']) - float(V['h1_26_cash'])) - ND)),

    nci=dict(
        basis='value_share',
        applied_to='equity_value',
        deduction=NCI_VAL,
        share=NCI_SHARE,
        proxy_source=(
            "The minority's share of GROUP PROFIT in the audited FY2025 consolidated "
            "financial statements -- profit attributable to non-controlling interests over "
            "profit for the year -- used as the proxy for its share of equity VALUE because "
            "the subsidiaries carrying the minority (Rowad for Modern Engineering and the "
            "Qatari and free-zone cable ventures) publish no separate financial statements "
            "in the group's filings, so their own economics cannot be valued directly."),
        book=float(V['nci_fy25']),
        profit_share=NCI_VAL,
        proportional=float(V['nci_fy25']) / (float(V['eqp_fy25']) + float(V['nci_fy25'])) * EQ_PRE_NCI,
        framing_note=(
            "Book is the balance-sheet carrying amount at 31 December 2025 and is a COST, "
            "not a value -- the model capitalises 100% of the subsidiaries' cash flow, so "
            "the minority's claim is worth its share of that value. Deducting book ({0:,.0f}) "
            "rather than the adopted {1:,.0f} would overstate equity attributable to the parent "
            "by {2:,.0f}, which is EGP {3:.2f} a share before the roll."
            .format(float(V['nci_fy25']), NCI_VAL, NCI_VAL - float(V['nci_fy25']),
                    (NCI_VAL - float(V['nci_fy25'])) / SH)),
    ),

    cash=dict(
        treatment='added_at_face',
        weights_basis='net',
        note=(
            "The bridge deducts NET financial debt, which is deducting gross borrowings and "
            "adding the cash back at face; the adopted discount-rate weights are also net "
            "(debt weight %.2f%% against a gross %.2f%%). That is the same cash reaching the "
            "answer twice, and on a net-DEBT company it runs the opposite way to the case "
            "the rule was written on: net weights understate the debt weight, and with a "
            "cost of debt of %.2f%% against a cost of equity of %.2f%% that RAISES the "
            "discount rate from %.2f%% to %.2f%% and LOWERS the value. The study already "
            "computes the gross-weighted rate and publishes it. Recorded, not corrected in "
            "this pass: it is one lever, it belongs in a rebuild ledger with its own audit "
            "point, and the fact that it moves the answer toward a price this study sits far "
            "below is neither a reason to take it nor a reason to leave it."
            % (100 * float(D['wacc']['wd_exp']), 100 * float(D['wacc']['wd_gross']),
               100 * float(D['wacc']['kd']), 100 * float(D['wacc']['ke_exp']),
               100 * float(D['wacc']['wacc_exp_gross']), 100 * float(D['wacc']['wacc_exp']))),
    ),

    associates=dict(
        basis='book',
        listed=False,
        value=ASSOC,
        book_reason=(
            "Equity-accounted investees are carried at the AUDITED FY2025 carrying value with "
            "no uplift and no growth factor applied. None is separately listed on any "
            "exchange -- they are the group's own joint ventures and associates in cables, "
            "wire and infrastructure -- so no market price exists to prefer over book, which "
            "is why the book basis is adopted here rather than merely defaulted to."),
    ),

    dividend=dict(
        deducted=True,
        declared_date='2026-05-06',
        value=DIVIDEND,
        per_share=float(V['dps_fy25']),
        note=(
            "The FY2025 cash dividend of EGP %.2f a share was recommended with the FY2025 "
            "results and RATIFIED BY THE ORDINARY GENERAL ASSEMBLY ON 6 MAY 2026 -- after "
            "the 31 December 2025 balance sheet the bridge stands on, so it is still inside "
            "the equity being valued and comes out exactly once, in the roll to the anchor "
            "date. A dividend declared before the sheet would already be out of that equity "
            "and deducting it would take it twice." % float(V['dps_fy25'])),
    ),

    lines=[
        dict(name='Enterprise value, discounted cash flow at 31 December 2025', value=EV),
        dict(name='Less net financial debt at 31 December 2025', value=-ND),
        dict(name='Plus equity-accounted investees at audited carrying value', value=ASSOC),
        dict(name='Less minority interests at their share of equity value', value=-NCI_VAL),
        dict(name="Less the employees' statutory share of profit", value=-EMP_CHARGE),
        dict(name='Plus accretion at the cost of equity over %d/365 of a year to the '
                  '3 September 2026 anchor' % int(DCF['anchor_days']), value=ACCRETION),
        dict(name='Less the FY2025 dividend paid inside that window', value=-DIVIDEND),
    ],
    equity_value=EQUITY_AT_ANCHOR,
    shares_mn=SH,
    per_share=PS,
    published_central=PS,
    published_spot=float(D['spot']),
    equity_value_at_balance_sheet_date=EQ_ATTR,
    per_share_at_balance_sheet_date=float(DCF['ps_dec']),
)

D['bridge_record'] = record
io.open(PATH, 'w', encoding='utf-8').write(
    json.dumps(D, indent=1, ensure_ascii=False, default=float) + '\n')

print('bridge_record written for SWDY')
for ln in record['lines']:
    print('   {0:<78} {1:>14,.1f}'.format(ln['name'][:78], ln['value']))
print('   {0:<78} {1:>14,.1f}'.format('EQUITY VALUE AT THE ANCHOR', EQUITY_AT_ANCHOR))
print('   {0:<78} {1:>14.4f}'.format('PER SHARE (published central)', PS))
try:
    RP.assert_bridge(record, 'SWDY')
    print('   assert_bridge: PASSES')
except AssertionError as e:
    print('   assert_bridge: FAILS, and the record is committed as it measures --')
    for line in str(e).splitlines()[1:]:
        print('     %s' % line.strip())
