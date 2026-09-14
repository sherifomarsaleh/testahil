#!/usr/bin/env python3
"""AMOC -- the [R-ASSET-01] operating asset base, committed AS IT MEASURES.

WHAT THE ASSET BASE IS ON A REFINER. This study values the plant on replacement cost: it
divides gross fixed assets at cost by annual throughput to get a capital intensity, charges
maintenance at cost over the implied asset life, and funds every incremental tonne at that
intensity. So gross cost is not a balance-sheet line here, it is the quantity the terminal
capital charge and the whole growth-costs-something argument are built out of.

WHAT THE MEASUREMENT SAYS, AND IT IS NOT COMFORTABLE. The base is EGP 2,740,810,692 at
31 December 2025, from note 6 of the reviewed statements for the six months then ended.
The information set this study claims to have read ends 30 JUNE 2026: its bridge stands on
that balance sheet, and its register cites the reviewed statements for the six months to
30-Jun-2026 note by note -- accounts payable at note 10-3, receivables at 9-B, cash at 9-E,
credit interest at 14-B, cost of sales by nature at 15-A. So the study had that filing OPEN
and took its asset base from the one before it. Six months, and the test is an ordering
rather than a threshold, so there is nothing to argue about.

WHY NO `not_restated_since` IS DECLARED, WHICH IS THE HONEST HALF. The rule's release is
real: a company whose gross cost has not moved may say so, name the later disclosures it
actually checked, and conform at any age. THIS STUDY CANNOT SAY THAT. A reviewed set
carries a fixed-asset note as a matter of course, and the FY2026 note is exactly where a
year of additions would appear -- the half to 31-Dec-2025 alone added 22,912,385 against
disposals of 1,447,608, so the figure moves. Nothing in this repository carries that note:
filings/ holds 30-06-2025, 31-12-2025 and the standalone, and AUDITED_EXTRACT.md covers
the 31-Dec-2025 set, a Q1-2026 filing and the 2024 comparative -- not the 30-Jun-2026 one.
Declaring a reason nobody checked would switch the check off rather than declare it.

NOTE THE FISCAL YEAR, because it is easy to read this wrongly. AMOC runs July to June, so
31 December is a HALF-year end and 30 June is the year end. The base is therefore a full
financial year behind the information set, not a stub.

WHAT CLOSES THIS IS A DOCUMENT AND NOT A SENTENCE: read note 6 of the reviewed statements
for the six months to 30 June 2026 -- the same filing this study already reads for five
other notes -- and either carry the newer gross cost or declare the absence of a
restatement with that note named.

    python3 asset_base_record.py    adds `asset_base_record` and `information_set_ends`
"""
import io, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import asset_base as AB                                          # noqa: E402

PATH = os.path.join(HERE, 'study_numbers.json')
D = json.load(open(PATH, encoding='utf-8'))

_PPE = D['inputs']['ppe_gross']
VALUE = float(_PPE['value'])
AS_AT = _PPE['date']

# THE INFORMATION SET IS READ OFF THE STUDY'S OWN CONSTRUCTION, never chosen: the bridge
# names the balance sheet it stands on and the same record names the latest disclosure it
# reached, so this date cannot flatter the comparison.
_BR = D['bridge_record']
INFO_SET_ENDS = _BR.get('latest_disclosed_date') or _BR['balance_sheet_date']

record = dict(
    rule='R-ASSET-01',
    quantity='gross fixed assets at cost',
    unit='EGP',
    value=VALUE,
    as_at=AS_AT,
    disclosure=(
        '%s. It is the quantity the replacement-cost view is built out of: capital '
        'intensity is this figure over annual throughput, maintenance capital expenditure '
        'is this figure over the implied asset life, and every incremental tonne is funded '
        'at that intensity — so a gross cost that has grown understates what growth costs '
        'and one that has not understates nothing.' % _PPE['source'][:220]),
    note=(
        'COMMITTED AS IT MEASURES. This base is {gap} months older than the information set '
        'this study claims to have read, and no not_restated_since is declared because none '
        'can honestly be: the study cites the reviewed statements for the six months to '
        '30-Jun-2026 for five separate notes and took its asset base from the set before '
        'them, and that filing\'s own fixed-asset note is not committed here. A reviewed set '
        'carries one as a matter of course and the figure moves — the half to 31-Dec-2025 '
        'alone added 22,912,385 against disposals of 1,447,608. AMOC runs a July-to-June '
        'year, so this is a full financial year behind rather than a stub. WHAT CLOSES IT IS '
        'A DOCUMENT: read note 6 of the 30-Jun-2026 reviewed statements and either carry the '
        'newer gross cost or declare the absence of a restatement with that note named.'
        .format(gap=(int(INFO_SET_ENDS[:4]) - int(str(AS_AT)[:4])) * 12
                + int(INFO_SET_ENDS[5:7]) - int(str(AS_AT)[5:7]))),
)

fails = AB.check(record, INFO_SET_ENDS)
D['asset_base_record'] = record
D['information_set_ends'] = INFO_SET_ENDS
io.open(PATH, 'w', encoding='utf-8').write(
    json.dumps(D, indent=1, ensure_ascii=False, default=float) + '\n')

print('asset_base_record written for AMOC')
print('   gross fixed assets   {0:>18,.0f} EGP   as at {1}'.format(VALUE, AS_AT))
print('   information set ends {0}'.format(INFO_SET_ENDS))
if fails:
    print('   asset_base.check: FAILS, and the record is committed as it measures --')
    for f in fails:
        print('     %s' % f)
else:
    print('   asset_base.check: PASSES')
