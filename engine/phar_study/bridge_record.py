#!/usr/bin/env python3
"""PHAR -- the [R-BRIDGE-01] enterprise-to-equity bridge record, READ OUT of the
committed numbers rather than typed.

IT READS study_numbers.json AND RUNS NOTHING. compute.py WRITES that file, so a
record generator that imports it to fetch its figures silently reverts every other
record already added -- measured on another study in this same pass, where it left
the working tree byte-identical to HEAD and so read like nothing had happened rather
than like something had been lost. Run build_records.py, which owns the order.

THE STUDY IS TWO-SIDED, so the bridge is too. Both frames share every line above the
enterprise value except the provision charge, so the record carries FRAME A as its
footed triple -- the frame that reads lower, which is the conservative half of a
published pair -- and publishes FRAME B's equity value and per-share figure beside
it. Neither is averaged into the other.

TWO THINGS THIS RECORD SURFACES, BOTH COMMITTED AS THEY MEASURE:

  (1) THE ASSOCIATES ARE NOT AT BOOK AND NOT AT MARKET. [R-BRIDGE-01] admits two
      bases -- market where the associate is listed, book otherwise -- and this study
      capitalises the associates' normalised earnings at a multiple and adds the
      active-ingredient plant at its carrying cost. That is a THIRD basis, and it is
      the largest single deviation in the bridge -- several times the disclosed
      carrying value, and the record prints the multiple, the per-share difference
      and what book would give. It names the basis it actually uses rather than
      claiming one from the list, so the gate can say so; book is published beside
      it with what it would give. NOT corrected here: whether an unlisted associate
      contributing real disclosed earnings is worth its carrying cost is a lens
      question with a rule attached, and both halves of that belong in their own
      pass with their own ledger entry.

  (2) THE BRIDGE MIXES TWO SHEETS, AND ONE OF THE TWO IS DEFENSIBLE. Net debt comes
      from the audited 31-December-2025 sheet the forecast opens from; the minority
      comes from AFTER the reviewed 31-March-2026 sheet, because the subsidiary
      carrying essentially all of it was DECONSOLIDATED in the first quarter of 2026.
      Those are different kinds of fact -- one is a timing movement the first
      forecast year already carries, the other is a permanent change in what the
      group owns, and deducting a minority in a company the group no longer
      consolidates would be wrong at any date. The rule tests the date, not the kind,
      so the record states the date the bridge stands on and lets the gate fire.

    python3 bridge_record.py        adds `bridge_record` to study_numbers.json
"""
import io, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import research_protocol as RP                                   # noqa: E402

PATH = os.path.join(HERE, 'study_numbers.json')
D = json.load(open(PATH, encoding='utf-8'))
I = D['inputs']
V = {k: x['value'] for k, x in I.items()}
A, B = D['dcf']['frame_A'], D['dcf']['frame_B']

SH = float(V['shares_mn'])
NET_DEBT = float(A['net_debt'])
NCI = float(A['nci'])
ASSOC_VALUE = float(A['assoc_value'])
ASSOC_BOOK = float(V['assoc_bv_fy25'])
ASSOC_X = ASSOC_VALUE / ASSOC_BOOK
ASSOC_PS = (ASSOC_VALUE - ASSOC_BOOK) / SH
PS_A, PS_B = float(A['per_share']), float(B['per_share'])

assert abs(float(A['equity']) / SH - PS_A) < 1e-9, 'frame A does not divide to its own per share'
assert abs(float(B['equity']) / SH - PS_B) < 1e-9, 'frame B does not divide to its own per share'

record = dict(
    rule='R-BRIDGE-01',
    two_sided=True,
    balance_sheet_date='2025-12-31',
    latest_disclosed_date='2026-03-31',
    latest_disclosed_source=(
        "The study's own committed input register (study_numbers.json `inputs`), whose "
        "Q1-2026 constant names the REVIEWED consolidated interim financial statements for "
        "the three months ended 31 March 2026. Every Q1-2026 figure in this study -- "
        "revenue, gross profit, the provision charge, receivables, cash, borrowings, "
        "property, capital work in progress, the associate carrying value, depreciation and "
        "the minority -- is registered against that document with its date and layer, so "
        "the latest disclosed sheet is established from a register rather than asserted."),
    balance_sheet_reason=(
        "Net debt is the audited 31-December-2025 position ({0:,.1f}), which is the sheet the "
        "forecast OPENS from: the same gross borrowings figure is the opening balance of the "
        "projected balance sheet, and the first forecast year carries the working-capital "
        "build and the capital expenditure that move it. The reviewed 31-March-2026 sheet "
        "shows net debt of {1:,.1f}, {2:+,.1f} over the quarter, and deducting that movement "
        "in the bridge as well as forecasting it would charge one outflow twice -- worth EGP "
        "{3:.2f} a share. THE RULE TESTS THE DATE AND NOT THAT ARGUMENT, and the record does "
        "not pretend otherwise: the construction is committed as it is and this study stays "
        "on the bridge ratchet. Re-striking the valuation onto the March sheet moves the "
        "explicit window's start with it and is a rebuild rather than a patch."
        .format(NET_DEBT, float(V['q1_debt']) - float(V['q1_cash']),
                (float(V['q1_debt']) - float(V['q1_cash'])) - NET_DEBT,
                ((float(V['q1_debt']) - float(V['q1_cash'])) - NET_DEBT) / SH)),

    nci=dict(
        basis='subsidiary',
        applied_to='equity_value',
        deduction=NCI,
        book=float(V['nci_fy25']),
        profit_share=float(V['nci_fwd']),
        proportional=NCI,
        evidence=(
            "The audited 31-December-2025 minority was {0:,.1f}, and essentially all of it "
            "was the active-ingredient company's minorities. That company was DECONSOLIDATED "
            "in the first quarter of 2026, so the group no longer owns the interest the "
            "December figure measures; the reviewed 31-March-2026 statements carry {1:,.3f}, "
            "which is what is deducted. This is a change in the group's PERIMETER rather "
            "than a movement in a balance, which is why it is taken from the later sheet "
            "while net debt is not -- and why deducting the December figure alongside the "
            "March associate value would charge the same interest twice."
            .format(float(V['nci_fy25']), NCI)),
        framing_note=(
            "Deducting the audited December figure of {0:,.1f} rather than the adopted "
            "{1:,.3f} would take EGP {2:.2f} a share off the answer -- and would be wrong, "
            "because it charges the group for a minority in a company it had already "
            "deconsolidated by the valuation's own information date."
            .format(float(V['nci_fy25']), NCI, (float(V['nci_fy25']) - NCI) / SH)),
    ),

    cash=dict(
        treatment='added_at_face',
        weights_basis='net',
        note=(
            "The bridge deducts NET debt -- gross borrowings less the audited cash balance -- "
            "and the adopted discount-rate weights are also net. The study publishes the "
            "gross-weighted rate beside the adopted one. On a net-DEBT company this runs the "
            "opposite way to the case the rule was written on: net weights understate the "
            "debt weight and, with a cost of debt below the cost of equity, RAISE the "
            "discount rate and LOWER the value. Recorded, not corrected in this pass."),
    ),

    associates=dict(
        basis='earnings_multiple',
        listed=False,
        value=ASSOC_VALUE,
        book=ASSOC_BOOK,
        book_reason=(
            "STATED PLAINLY BECAUSE THE RULE ADMITS ONLY MARKET OR BOOK AND THIS IS NEITHER. "
            "The associates are unlisted, so no market price exists and the rule's own answer "
            "would be the disclosed carrying value of {0:,.1f}. This study instead capitalises "
            "their normalised earnings of {1:,.1f} at {2:.1f} times and adds the "
            "active-ingredient plant at its carrying cost of {3:,.1f}, reaching {4:,.1f} -- "
            "{5:.1f} times book, and a difference of EGP {6:.2f} a share against a Frame A "
            "central of EGP {7:.2f}. It is the largest single deviation in this bridge and it "
            "is recorded rather than relabelled: writing 'book' here would make the gate green "
            "and the record false. Carrying the associates at book instead would take Frame A "
            "to EGP {8:.2f} and Frame B to EGP {9:.2f}. NOT changed in this pass -- whether an "
            "unlisted associate contributing disclosed earnings is worth its carrying cost is "
            "a lens question with its own rule, and it belongs in its own pass with its own "
            "ledger entry and audit point."
            .format(ASSOC_BOOK, float(V['assoc_norm']) * float(V['assoc_multiple']),
                    float(V['assoc_multiple']), float(V['arab_api_cost']), ASSOC_VALUE,
                    ASSOC_X, ASSOC_PS, PS_A,
                    PS_A - ASSOC_PS, PS_B - ASSOC_PS)),
    ),

    dividend=dict(
        deducted=False,
        note=("No declared-but-unpaid dividend is deducted. The payout continues inside the "
              "forecast as a cash outflow that funds the projected balance sheet, which is "
              "where a continuing distribution belongs; a dividend deducted in the bridge as "
              "well would come out twice."),
    ),

    lines=[
        dict(name='Enterprise value of the operations, discounted cash flow (Frame A)',
             value=float(A['ev_core'])),
        dict(name='Plus associates at capitalised normalised earnings and the '
                  'active-ingredient plant at carrying cost', value=ASSOC_VALUE),
        dict(name='Plus available-for-sale investments at carrying value',
             value=float(V['afs_fy25'])),
        dict(name='Less net debt at 31 December 2025', value=-NET_DEBT),
        dict(name='Less non-controlling interests after the first-quarter deconsolidation',
             value=-NCI),
    ],
    equity_value=float(A['equity']),
    shares_mn=SH,
    per_share=PS_A,

    branches=[
        dict(label='Frame A - provision charge permanent at 5.25% of revenue',
             equity_value=float(A['equity']), per_share=PS_A),
        dict(label='Frame B - provision charge normalising to 2.5% of revenue',
             equity_value=float(B['equity']), per_share=PS_B),
    ],
    published_central=None,
    published_central_branches=[PS_A, PS_B],
    published_spot=float(V['spot']),
)

D['bridge_record'] = record
io.open(PATH, 'w', encoding='utf-8').write(
    json.dumps(D, indent=1, ensure_ascii=False, default=float) + '\n')

print('bridge_record written for PHAR')
for ln in record['lines']:
    print('   {0:<74} {1:>12,.1f}'.format(ln['name'][:74], ln['value']))
print('   {0:<74} {1:>12,.1f}'.format('EQUITY VALUE (Frame A)', float(A['equity'])))
print('   {0:<74} {1:>12.4f}'.format('PER SHARE (Frame A)', PS_A))
print('   {0:<74} {1:>12.4f}'.format('PER SHARE (Frame B)', PS_B))
try:
    RP.assert_bridge(record, 'PHAR')
    print('   assert_bridge: PASSES')
except AssertionError as e:
    print('   assert_bridge: FAILS, and the record is committed as it measures --')
    for line in str(e).splitlines()[1:]:
        print('     %s' % line.strip())
