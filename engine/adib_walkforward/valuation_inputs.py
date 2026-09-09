#!/usr/bin/env python3
"""ADIB (EGX) — the valuation-input block beside the driver panel, per origin.

[R-FCAL-01 AMENDED] "A driver panel is not a record a value can be rebuilt from, and
the difference stays invisible until something tries." GENERATED - never hand-edited.
`python3 scripts/check_valuation_inputs.py` reads the JSON this writes.

A BANK'S BLOCK IS NOT AN INDUSTRIAL ONE, AND THE DIFFERENCE IS DECLARED RATHER THAN
QUIETLY FILLED. Three of the seven items mean something different here, and one means
nothing at all:

  cash   For an industrial company this is a bridge item that is added to enterprise
         value. For a bank it is an OPERATING asset - the CBE reserve requirement and
         the settlement float - and it is never netted against anything. Recorded as
         the filed figure with that basis stated, so nobody adds it to an equity value
         later. L-111: a bank is valued on what reaches the shareholder, not on EV.

  debt   THE TRAP-(i) ITEM, AND IT INVERTS FOR A BANK. The liabilities that actually
         bear the cost of deposits are customers' deposits + due to banks +
         subordinated financing. For an industrial company the protocol's rule
         EXCLUDES customer deposits; here they are the largest part of it. Both the
         full interest-bearing total and the wholesale-only sub-line are recorded, so
         neither reading can be taken by accident.

  wc     MISSING BY CONSTRUCTION, with its reason. A bank has no inventory, no DSO,
         no DIO and no DPO; its 'working capital' is its balance sheet. The nearest
         meaningful figure - other assets less other liabilities - is recorded beside
         it as `bank_equivalent` and is explicitly NOT a working-capital cycle.

  capex / ppe / dep  Real but immaterial: D&A runs EGP 80-178mn against PBT of EGP
         0.4-17.5bn. Recorded in full anyway, because the point of the block is that
         a value can be REBUILT, and a figure nobody thought material is exactly the
         one that is missing when someone tries.
"""
from __future__ import annotations
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import panel, bottom_up as bu  # noqa: E402

PAR = 10.0            # LE 10 per share - FY2018 note 34/2, FY2015 note 32/2
UNIT = 1000.0         # the panel is in EGP '000; this record is in units of one pound

# Cash and due from the Central Bank of Egypt, EGP '000, as filed.
CASH = {2013: 1696497.0, 2014: 1318949.0, 2015: 1181844.0, 2016: 1322098.0,
        2017: 2125571.0, 2018: 2656168.0, 2019: 5078157.0, 2020: 4633212.0,
        2021: 6068383.0, 2022: 9926973.0, 2023: 9985417.0, 2024: 13811689.0,
        2025: 19086612.0}

# Fixed assets net of accumulated depreciation, EGP '000, AS ORIGINALLY REPORTED.
PPE = {2013: 427652.0, 2014: 546288.0, 2015: 605415.0, 2016: 641804.0,
       2017: 743069.0, 2018: 751822.0, 2019: 774104.0, 2020: 724641.0,
       2021: 518271.0, 2022: 496468.0, 2023: 647461.0, 2024: 713160.0,
       2025: 953087.0}

# Depreciation of fixed assets + amortisation of intangibles, EGP '000, off the
# cash-flow reconciliation of each year's own filing.
DEP = {2013: 62941.0 + 17337.0, 2014: 63790.0 + 21865.0, 2015: 65323.0 + 21749.0,
       2016: 68125.0 + 5439.0, 2017: 82909.0 + 1023.0, 2018: 101905.0 + 318.0,
       2019: 110750.0, 2020: 147235.0, 2021: 109966.0, 2022: 99908.0,
       2023: None, 2024: 132268.0, 2025: 177748.0}

DEP_MISSING = {
 2023: ("the cash-flow reconciliation line is a raster in both the FY2023 filing and "
        "the FY2024 filing's comparative column, and the two OCR passes return 92,471 "
        "and 99,471 at every threshold tried up to 1200 dpi. The reconciliation has "
        "twenty-odd items so it does not foot on this line alone, and a figure that "
        "cannot be pinned to a single digit does not enter the panel. The derived "
        "identity is recorded beside it."),
}

# Payments to purchase fixed assets and branch fixtures, EGP '000, off the investing
# section of each year's own cash-flow statement. None = not read; derived instead.
CAPEX = {2013: None, 2014: None, 2015: None, 2016: None, 2017: None,
         2018: 121024.0, 2019: 135256.0, 2020: 177347.0, 2021: 62847.0,
         2022: 54084.0, 2023: 234666.0, 2024: 178671.0, 2025: 420578.0}

SRC = ('ADIB-Egypt own audited consolidated financial statements, adib.eg; '
       'see panel.SOURCES for the per-year document, date and route')


def wholesale_debt(y):
    b = panel.BS[bu.fy(y)]
    return (b.get('due_to_banks') or 0.0) + (b.get('subordinated') or 0.0)


def bank_equivalent_wc(y):
    """other assets less other liabilities - NOT a working-capital cycle. See module docstring."""
    b = panel.BS[bu.fy(y)]
    ta, ib = b['total_assets'], bu.interest_bearing(y)
    tl = b['total_liab']
    return dict(other_liabilities_ex_funding=(tl - ib) * UNIT,
                note='total liabilities less the interest-bearing funding block')


def record_for(y):
    b = panel.BS[bu.fy(y)]
    route = panel.SOURCES[bu.fy(y)]['route']
    doc = panel.SOURCES[bu.fy(y)]['doc']
    cap = b['capital'] * UNIT
    out = {}

    out['cash'] = dict(value=CASH[y] * UNIT, as_at='%d-12-31' % y, source=SRC + ' — ' + doc,
                       route=route,
                       basis='cash and due from the Central Bank of Egypt. AN OPERATING '
                             'ASSET FOR A BANK, not a bridge item: it is the CBE reserve '
                             'requirement and settlement float and is never added to an '
                             'equity value. [L-111]')
    out['debt'] = dict(value=bu.interest_bearing(y) * UNIT, as_at='%d-12-31' % y,
                       source=SRC + ' — ' + doc, route=route,
                       lines={'customers_deposits': b['cust_deposits'] * UNIT,
                              'due_to_banks': (b.get('due_to_banks') or 0.0) * UNIT,
                              'subordinated_financing': (b.get('subordinated') or 0.0) * UNIT},
                       wholesale_only=wholesale_debt(y) * UNIT,
                       basis='INTEREST-BEARING ONLY [R-FCAL-01 trap (i)], AND FOR A BANK '
                             'THAT INCLUDES CUSTOMERS\' DEPOSITS, which is the exact '
                             'inversion of the industrial case. The `Cost of deposits and '
                             'similar costs` line is the return paid on precisely these '
                             'three balances. Other liabilities, current income tax, other '
                             'provisions and defined-benefit obligations are EXCLUDED — at '
                             'FY2025 they are EGP 17.9bn of the EGP 312.1bn total, and '
                             'dividing the funding charge by total liabilities would '
                             'understate the rate by about a sixth of itself.')
    out['ppe'] = dict(value=PPE[y] * UNIT, as_at='%d-12-31' % y, source=SRC + ' — ' + doc,
                      route=route, basis='fixed assets net of accumulated depreciation')

    if DEP.get(y) is not None:
        out['dep'] = dict(value=DEP[y] * UNIT, as_at='FY%d' % y, source=SRC + ' — ' + doc,
                          route=route,
                          basis='depreciation of fixed assets plus amortisation of '
                                'intangible assets, off the cash-flow reconciliation')
    else:
        dppe = (PPE[y] - PPE[y - 1]) * UNIT if (y - 1) in PPE else None
        out['dep'] = dict(missing=DEP_MISSING[y], derived=False,
                          identity_not_available=(
                            'capex = dppe + d&a cannot settle it either, because capex '
                            'IS disclosed here (EGP %s) and d&a is the unknown; running '
                            'the identity backwards gives d&a = capex - dppe = EGP %s, '
                            'which is recorded as an ARITHMETIC CONSEQUENCE and not as a '
                            'reading of the filing.'
                            % ('{:,.0f}'.format(CAPEX[y] * UNIT) if CAPEX.get(y) else 'n/a',
                               '{:,.0f}'.format(CAPEX[y] * UNIT - dppe)
                               if (CAPEX.get(y) and dppe is not None) else 'n/a')))

    if CAPEX.get(y) is not None:
        out['capex'] = dict(value=CAPEX[y] * UNIT, as_at='FY%d' % y, source=SRC + ' — ' + doc,
                            route=route, derived=False,
                            basis='payments to purchase fixed assets and branch fixtures, '
                                  'investing section of the cash-flow statement')
    else:
        dppe = (PPE[y] - PPE[y - 1]) if (y - 1) in PPE else None
        d = DEP.get(y)
        if dppe is None or d is None:
            out['capex'] = dict(missing='neither the cash-flow investing line nor the '
                                        'prior-year PP&E needed by the identity is in hand '
                                        'for this year', derived=False)
        else:
            out['capex'] = dict(value=(dppe + d) * UNIT, as_at='FY%d' % y,
                                source=SRC + ' — ' + doc, route=route,
                                derived=True, identity='capex = dppe + d&a',
                                basis='the cash-flow investing line is not separately '
                                      'disclosed in this year\'s own filing; DERIVED by '
                                      'the identity, which is arithmetic and not an '
                                      'assumption, and labelled as such')

    out['wc'] = dict(missing='A BANK HAS NO WORKING-CAPITAL CYCLE. There is no inventory, '
                             'no DSO, no DIO and no DPO; the balance sheet IS the working '
                             'capital and it is already carried in `debt` and in the '
                             'driver panel. Recording a number here would invent a '
                             'quantity the issuer does not have.',
                     derived=False, bank_equivalent=bank_equivalent_wc(y))
    out['shares'] = dict(value=cap / PAR, as_at='%d-12-31' % y, source=SRC + ' — ' + doc,
                         route=route, issued_capital=cap, par_value=PAR,
                         basis='issued and paid-in capital over the LE 10 par value the '
                               'filings state (FY2018 note 34/2: "LE 2Bn represented by '
                               '200mn shares with a nominal value of LE 10 per share"; '
                               'FY2015 note 32/2 the same at LE 1.9bn). THE YEAR\'S OWN '
                               'COUNT, never today\'s carried back — capital moved '
                               '1,999,503 → 2,000,000 → 4,000,000 → 5,000,000 → 6,000,000 '
                               '→ 12,000,000 (EGP \'000) across this window.',
                         weighted_average_note=(
                             'the count implied by the filed EPS differs from the year-end '
                             'count in every capital-increase year (FY2025: 12,588,572 / '
                             '11.25 = 1,119mn against a year-end 1,200mn). The year-end '
                             'count is recorded; the weighted average is noted, never '
                             'substituted.'))
    return out


def build():
    doc = {
     '_': ('The inputs a VALUE is rebuilt from at each of this run\'s origins, committed '
           'beside the driver panel under [R-FCAL-01 AMENDED]. GENERATED by '
           'engine/adib_walkforward/valuation_inputs.py from panel.py; never hand-edited.'),
     'run': 'ADIB',
     'rule': '[R-FCAL-01 AMENDED]',
     'company': 'Abu Dhabi Islamic Bank (ADIB) – Egypt S.A.E., EGX: ADIB. NOT ADIB Group '
                'PJSC (ADX: ADIB), which is the separate covered name ADIBUAE.',
     'class': 'bank',
     'currency': 'EGP',
     'units': 'units of one Egyptian pound. The panel is in EGP thousands; every figure '
              'here is multiplied by 1,000 on the way in.',
     'basis': 'consolidated',
     'fiscal_year_end': '31 December',
     'origins_declared_by': 'PRE_REGISTRATION_09-09-2026.md',
     'route': ('per year, in panel.SOURCES: text layer where the filing carries one, '
               'otherwise two independent OCR passes (largest embedded image at native '
               'resolution upscaled, and a page render), with disagreement settled by the '
               'statement\'s OWN arithmetic and, where that was not decisive, by the '
               'comparative column of the following year\'s filing. Every statement in '
               'the panel foots exactly; panel.py asserts it.'),
     'point_in_time': ('every year is carried AS ORIGINALLY REPORTED, from its own '
                       'filing\'s own column. The six later restatements inside this '
                       'window are in panel.RESTATEMENTS beside the figures they would '
                       'replace and are never substituted. The one exception is FY2021, '
                       'whose English consolidated filing does not exist on the issuer\'s '
                       'site — it is taken from the FY2022 comparative and that is stated '
                       'in basis break B9.'),
     'bank_note': __doc__.split('A BANK\'S BLOCK', 1)[1].strip(),
     'sources': {k: v['url'] for k, v in panel.SOURCES.items()},
     'origins': {},
     'prior_year_anchor': {},
    }
    for o in bu.ORIGINS:
        doc['origins'][bu.fy(o)] = record_for(o)
    doc['prior_year_anchor'][bu.fy(bu.ORIGINS[0] - 1)] = record_for(bu.ORIGINS[0] - 1)
    doc['prior_year_anchor']['_why'] = (
        'FY2013 is the year before the first origin. The run does not test it, so '
        'recording it as an origin would misstate what was tested; it is committed here '
        'because every FY2014 average balance needs its opening.')
    return doc


if __name__ == '__main__':
    d = build()
    json.dump(d, open(os.path.join(HERE, 'valuation_inputs.json'), 'w'), indent=1)
    print('origins %d + prior-year anchor %s'
          % (len(d['origins']), ','.join(k for k in d['prior_year_anchor'] if not k.startswith('_'))))
    for o in bu.ORIGINS:
        r = d['origins'][bu.fy(o)]
        miss = [k for k, v in r.items() if isinstance(v, dict) and 'missing' in v]
        der = [k for k, v in r.items() if isinstance(v, dict) and v.get('derived')]
        s = r['shares']
        print('  %s shares %13.0f (capital %.0f / par %.0f)  missing:%s  derived:%s'
              % (bu.fy(o), s['value'], s['issued_capital'], s['par_value'],
                 ','.join(miss) or '-', ','.join(der) or '-'))
