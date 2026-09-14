#!/usr/bin/env python3
"""PHDC -- the [R-ASSET-01] operating asset base, committed as it measures.

THIS IS THE CASE THE RULE WAS ADOPTED ON, in the principal's own words: a study that
"takes into consideration current landbank of a developer but does not account for new
land added to the developer landbank". The bridge has been held to the LATEST disclosed
balance sheet since [R-BRIDGE-01]; nothing held the LAND, which on a developer is the
quantity the value is built out of, disclosed by the same company in the same documents.

WHAT THE MEASUREMENT SAYS, AND IT IS NOT COMFORTABLE. The land bank is registered at
33.0 million square metres, dated 31 December 2024, sourced to the FY2024 earnings
release. The information set this study claims to have read ends 31 March 2026 -- its
bridge stands on that reviewed balance sheet and its register carries a 1Q2026 earnings
release. So the asset base is FIFTEEN MONTHS OLDER than the information set, and the
test is an ordering rather than a threshold: there is nothing to argue about.

WHY NO `not_restated_since` IS DECLARED, WHICH IS THE HONEST HALF. The rule's release
is real and cannot be gamed: a developer that has bought no land may say so, name the
later disclosures it actually checked, and conform at any age. THIS STUDY CANNOT SAY
THAT YET. Its own register names a 1Q2026 earnings release -- exactly the document a
developer restates a land bank in -- and that release is not committed to this
repository, so whether it carries an updated figure has not been established. Declaring
a reason nobody checked would switch the check off rather than declare it, and an empty
or invented list of "disclosures checked" is worse than no list.

So the record is committed AS IT MEASURES and this study stays on the asset-base ratchet
with the reason printed, which is a readable failure where there was previously no
record at all. What closes it is a document, not a sentence: read the FY2025 and 1Q2026
releases for a land-bank figure, and either carry the newer number or declare the
absence of a restatement with those two named.

    python3 asset_base_record.py    adds `asset_base_record` and `information_set_ends`
"""
import io, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import asset_base as AB                                          # noqa: E402

PATH = os.path.join(HERE, 'study_numbers.json')
D = json.load(open(PATH, encoding='utf-8'))


def _dig(o, key):
    if isinstance(o, dict):
        if key in o:
            return o[key]
        for v in o.values():
            r = _dig(v, key)
            if r is not None:
                return r
    elif isinstance(o, list):
        for v in o:
            r = _dig(v, key)
            if r is not None:
                return r
    return None


_lb = _dig(D, 'land_bank_sqm_mn')
LAND = float(_lb['value'] if isinstance(_lb, dict) else _lb)
LAND_DATE = (_lb.get('date') if isinstance(_lb, dict) else None) or '2024-12-31'
LAND_SRC = (_lb.get('source') if isinstance(_lb, dict) else None) or ''

# THE INFORMATION SET THIS STUDY ACTUALLY READ. Its bridge stands on the reviewed
# 31-March-2026 balance sheet, which the bridge record already names, so this date is
# read off the study's own construction rather than chosen.
INFO_SET_ENDS = (D.get('bridge_record') or {}).get('balance_sheet_date') or '2026-03-31'

record = dict(
    rule='R-ASSET-01',
    quantity='land bank',
    unit='million square metres',
    value=LAND,
    as_at=LAND_DATE,
    disclosure=(
        "%s. It is the only land-bank figure this study registers, and it is the quantity "
        "the whole present-value net asset view is built out of: absorption runs on the "
        "company's own delivery rate ACROSS THIS AREA, so a land bank that has grown "
        "understates the value and one that has been consumed overstates it."
        % (LAND_SRC or 'the FY2024 earnings release')),
    note=(
        "COMMITTED AS IT MEASURES. This base is {gap} months older than the information "
        "set this study claims to have read, and no not_restated_since is declared "
        "because none can honestly be: the study's own register names a 1Q2026 earnings "
        "release, which is exactly the document a developer restates a land bank in, and "
        "that release is not committed here — so whether the figure moved has not been "
        "established. A reason nobody checked switches the check off rather than "
        "declaring it. WHAT CLOSES THIS IS A DOCUMENT AND NOT A SENTENCE: read the FY2025 "
        "and 1Q2026 releases for a land-bank figure, then either carry the newer number "
        "or declare the absence of a restatement with those two named."
        .format(gap=(int(INFO_SET_ENDS[:4]) - int(str(LAND_DATE)[:4])) * 12
                + int(INFO_SET_ENDS[5:7]) - int(str(LAND_DATE)[5:7]))),
)

fails = AB.check(record, INFO_SET_ENDS)
D['asset_base_record'] = record
D['information_set_ends'] = INFO_SET_ENDS
io.open(PATH, 'w', encoding='utf-8').write(
    json.dumps(D, indent=1, ensure_ascii=False, default=float) + '\n')

print('asset_base_record written for PHDC')
print('   land bank            {0:>10,.1f} million sqm   as at {1}'.format(LAND, LAND_DATE))
print('   information set ends {0}'.format(INFO_SET_ENDS))
if fails:
    print('   asset_base.check: FAILS, and the record is committed as it measures --')
    for f in fails:
        print('     %s' % f)
else:
    print('   asset_base.check: PASSES')
