#!/usr/bin/env python3
"""EGCH -- the [R-ASSET-01] operating asset base, and the information set it is held
against.

WHY IT DID NOT EXIST. The bridge stands on the LATEST DISCLOSED BALANCE SHEET and
check_bridge enforces that; nothing said the same of the OPERATING ASSET BASE -- the
installed capacity a replacement-cost lens is built out of -- although it is disclosed
by the same company in the same filings on the same day. This study's failure line was
not that its capacity was stale but that it "states no information-set end date, so its
asset base cannot be held to anything": there was nothing to compare against.

THE TEST IS AN ORDERING, NOT A THRESHOLD. The asset base may not be OLDER than the
information set the study says it read, and there is no number of days to argue about
-- which is right, because a plant's nameplate is restated when the company builds or
retires a line, never on a clock. A producer that has commissioned nothing for three
years conforms at any age, provided it says so and names the later disclosures it
actually checked.

WHAT THIS STUDY'S BASE IS, AND ITS ONE ADDITION. The operating plates are the
contractual benchmarks in note 28 of the FY2024/25 audited statements -- 1,575 tonnes a
day of urea and 1,200 of ammonia -- and no later filing restates them. The one thing
that DOES change the base is the ammonium-nitrate line under construction, and it is
carried explicitly rather than folded into the plates it has not yet joined: its
capacity comes from the EPC award rather than from a filing, which is the same figure
the valuation's contested branch turns on, and it is labelled as such.

IT READS study_numbers.json AND RUNS NOTHING, for the reason the SWDY and PHAR
generators record: compute.py and lenses.py both WRITE that file, so a record generator
that imports either to fetch its figures reverts whatever was added after it.

    python3 asset_base_record.py    adds `asset_base_record` and `information_set_ends`
"""
import io, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import asset_base as AB                                          # noqa: E402

PATH = os.path.join(HERE, 'study_numbers.json')
D = json.load(open(PATH, encoding='utf-8'))
DR = D['drivers']

UREA = float(DR['design_urea_t'])
NH3 = float(DR['design_ammonia_t'])
ANNA = float(DR['anna_nameplate_an_t'])

# THE INFORMATION SET THIS STUDY ACTUALLY READ. The latest filing it consumes is the
# nine-month interim to 31 March 2026, limited review dated 20 May 2026 -- the same
# statement its bridge already stands on, which is why this date and the bridge's
# agree rather than being two answers to one question.
INFO_SET_ENDS = '2026-03-31'

record = dict(
    rule='R-ASSET-01',
    quantity='urea nameplate capacity',
    unit='tonnes per year',
    value=UREA,
    as_at='2025-06-30',
    disclosure=(
        "Note 28 of the audited consolidated financial statements for the year ended 30 "
        "June 2025 states the plants' CONTRACTUAL BENCHMARKS -- 1,575 tonnes a day of urea "
        "and 1,200 tonnes a day of ammonia -- which are the design plates the whole "
        "utilisation path is measured against. The urea figure is that plate times 365 "
        "days ({0:,.0f} tonnes a year) and the ammonia plate is stated directly as {1:,.0f} "
        "tonnes a year. These are the operating lines the company has today; no later "
        "filing restates either."
        .format(UREA, NH3)),
    components={
        'urea_design_tpy': UREA,
        'ammonia_design_tpy': NH3,
        'ammonium_nitrate_under_construction_tpy': ANNA,
    },
    under_construction=dict(
        quantity='ammonium-nitrate line under construction',
        unit='tonnes per year',
        value=ANNA,
        as_at='2023-06-09',
        disclosure=(
            "The EPC award for this plant, announced 9 June 2023 -- 600 tonnes a day of "
            "nitric acid converted to 800 tonnes a day of fertilizer-grade granulated "
            "ammonium nitrate, at {0:,.0f} operating days a year. IT IS NOT IN A FILING and "
            "is labelled as such: the study had previously said no filing states the plate "
            "and DERIVED it from the ammonia surplus instead, reaching {1:,.0f} tonnes, and "
            "an outside critique found the award. Both figures are carried; the disclosed "
            "one is adopted."
            .format(float(DR.get('anna_operating_days', 330) if isinstance(DR.get('anna_operating_days'), (int, float)) else 330),
                    float(DR['anna_nameplate_derived']))),
        note=(
            "CARRIED SEPARATELY RATHER THAN ADDED TO THE PLATES, because it has not joined "
            "them: the line is not commissioned, and whether it ever is IS this study's "
            "contested judgement and the reason it publishes two answers instead of one. "
            "Folding an uncommissioned plant into the operating asset base would state as "
            "installed capacity the very thing the study says is undecided."),
    ),
    not_restated_since=dict(
        reason=(
            "A nameplate is restated when a company builds or retires a line, not on a "
            "clock, and this company has commissioned nothing since the plates in note 28 "
            "were stated. The one addition in progress is the ammonium-nitrate line, which "
            "is carried above under its own heading at its own disclosed capacity and its "
            "own date, so nothing about the base is being carried forward silently. What "
            "HAS moved between the two dates is utilisation rather than capacity -- gas "
            "curtailment, which the forecast models on the company's own production "
            "history and which is a fact about throughput, not about the plant."),
        disclosures_checked=[
            "Interim statements for the nine months ended 31 March 2026, limited review "
            "dated 20 May 2026 -- the latest filing this study reads, and the sheet its "
            "bridge stands on. It discloses no change to either design plate and no "
            "commissioning of the line under construction.",
            "Interim statements for the six months ended 31 December 2025, from which the "
            "third quarter is derived by difference. No change to either plate.",
            "Audited consolidated financial statements for the year ended 30 June 2025, "
            "note 28, which is where the plates themselves are stated.",
        ],
    ),
    note=(
        "THE BASE IS OLDER THAN THE INFORMATION SET AND SAYS SO, WHICH IS WHAT THE RELEASE "
        "IS FOR. The ordering test would otherwise refuse a producer that has built nothing "
        "-- the commonest case there is -- so the study declares the gap, gives its reason, "
        "and names the later filings it actually opened. An empty reason would switch the "
        "check off rather than declare it, and a list of filings nobody read would be "
        "worse than no list."),
)

fails = AB.check(record, INFO_SET_ENDS)
D['asset_base_record'] = record
D['information_set_ends'] = INFO_SET_ENDS
io.open(PATH, 'w', encoding='utf-8').write(
    json.dumps(D, indent=1, ensure_ascii=False, default=float) + '\n')

print('asset_base_record written for EGCH')
print('   urea design plate      {0:>12,.0f} t/y   as at 2025-06-30 (note 28)'.format(UREA))
print('   ammonia design plate   {0:>12,.0f} t/y'.format(NH3))
print('   under construction     {0:>12,.0f} t/y   ammonium nitrate, EPC award 2023-06-09'
      .format(ANNA))
print('   information set ends   {0}'.format(INFO_SET_ENDS))
if fails:
    print('   asset_base.check: FAILS --')
    for f in fails:
        print('     %s' % f)
else:
    print('   asset_base.check: PASSES')
