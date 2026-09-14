#!/usr/bin/env python3
"""TMGH -- the [R-ASSET-01] operating asset base, committed so a gate can read it.

WHY THIS STUDY WAS ON THE RATCHET AND WHAT WAS ACTUALLY WRONG. Not the land bank: it is
CURRENT. The study commits landbank_msqm = 20.0 dated 30 June 2026, sourced to the
company's own 1H 2026 earnings release. What was missing was the RECORD -- nothing stated
the vintage in a form the gate could read, so the check could say nothing at all about it
and reported that as a failure rather than as silence. An artefact checked for existence
rather than for currency is one defect; a quantity that is current and unreadable is the
mirror of it, and both end with a gate that cannot speak.

THE TEST IS AN ORDERING, NOT A THRESHOLD. The asset base may not be older than the
information set the study says it read. Here they are the SAME DAY: the land bank is
disclosed as at 30 June 2026 and the bridge stands on the reviewed 30 June 2026 balance
sheet, which is the strongest form this test can pass -- not "recent enough" but "the same
instant", so there is no gap for a reader to argue about.

WHY A DEVELOPER'S LAND BANK IS THE ASSET BASE AT ALL. It is the quantity the value is
built out of: absorption runs on the company's own delivery rate ACROSS THIS AREA, so a
land bank that has grown understates the value and one that has been consumed overstates
it. [R-ASSET-01] was adopted on exactly that case, in the principal's own words -- a study
that takes the current land bank of a developer and does not account for land added to it.

    python3 asset_base_record.py    adds `asset_base_record` and `information_set_ends`
"""
import io, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import asset_base as AB                                          # noqa: E402

PATH = os.path.join(HERE, 'study_numbers.json')
D = json.load(open(PATH, encoding='utf-8'))

_LB = D['inputs']['KPI']['landbank_msqm']
LAND = float(_LB['value'])
LAND_DATE = _LB['date']
LAND_SRC = _LB['source']

# THE INFORMATION SET THIS STUDY ACTUALLY READ, taken from the study's own construction
# rather than chosen: the bridge names the reviewed balance sheet it stands on, and the
# same record names the latest disclosure it reached.
_BR = D['bridge_record']
INFO_SET_ENDS = _BR.get('latest_disclosed_date') or _BR['balance_sheet_date']

record = dict(
    rule='R-ASSET-01',
    quantity='land bank',
    unit='million square metres',
    value=LAND,
    as_at=LAND_DATE,
    disclosure=(
        '%s. Stated on the release\'s own indicator panel as "c.20 mn sqm", so the figure '
        'carries the company\'s own rounding and this record carries it unrounded further. '
        'It is the quantity the whole present-value view is built out of: absorption runs '
        'on the delivery rate ACROSS THIS AREA, so a land bank that has grown understates '
        'the value and one consumed overstates it.' % LAND_SRC),
    note=(
        'THE ASSET BASE AND THE INFORMATION SET ARE THE SAME DAY, {d}. The land bank is '
        'disclosed as at that date in the 1H 2026 earnings release and the bridge stands '
        'on the reviewed balance sheet of the same date, so the ordering this rule tests '
        'is satisfied with no gap at all rather than with an acceptable one. No '
        'not_restated_since is declared and none is needed: a release is not being '
        'stretched forward here, it is contemporaneous.'.format(d=LAND_DATE)),
)

fails = AB.check(record, INFO_SET_ENDS)
D['asset_base_record'] = record
D['information_set_ends'] = INFO_SET_ENDS
io.open(PATH, 'w', encoding='utf-8').write(
    json.dumps(D, indent=1, ensure_ascii=False, default=float) + '\n')

print('asset_base_record written for TMGH')
print('   land bank            {0:>10,.1f} million sqm   as at {1}'.format(LAND, LAND_DATE))
print('   information set ends {0}'.format(INFO_SET_ENDS))
if fails:
    print('   asset_base.check: FAILS, and the record is committed as it measures --')
    for f in fails:
        print('     %s' % f)
else:
    print('   asset_base.check: PASSES')
