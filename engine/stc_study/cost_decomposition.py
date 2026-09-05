"""STC — what the blended cost side hides, priced against the study's own committed answer.

THE QUESTION THIS ANSWERS. The model holds each disclosed segment's gross margin flat, so
every cost line sits on the revenue of the segment it belongs to. That is the right base
for most of the stack. It is NOT the right base for the lines whose driver is something
other than revenue at all, and the standing instruction for that case is to DECOMPOSE AND
PRICE what the coarse figure hides rather than either asserting it hides nothing or filling
an unidentified split with an imported ratio.

WHAT IS PRICED, AND WHY EACH ONE AND NOT THE OTHERS.

  Commercial service provisioning fees   the sub-note levies it on the Saudi operating
                                         segment, which the model already grows at its own
                                         rate — far slower than the group's
  License fees                           near-fixed; its own two-year CAGR, measured
  Repairs and maintenance                the asset base being maintained, which the model
                                         already projects through capex against depreciation
  Amortisation of contract costs         subscriber acquisition; the model already carries a
                                         subscriber volume path, and it grows FASTER than
                                         revenue

FOUR LINES ARE DELIBERATELY NOT PRICED AND THE REASON IS THE SAME EACH TIME — there is no
sourced driver, and inventing one to complete a table is worse than the gap it closes:

  Network access charges     12.97% of revenue, no disclosed unit rate
  Employees costs             7.12%, no headcount anywhere in the filings — searched, absent
  Others                      3.48%, a residual of three unrelated things
  Frequency spectrum fees     0.34%, and lumpy: 361,932 / 137,427 / 265,470. The first
                             Saudi licence expiry falls in 2029, INSIDE the explicit window,
                             and no renewal cost is disclosed. That is a gap to NAME, not a
                             driver to build, and escalating a three-year mean at CPI would
                             dress a guess as a construction.

THE DEVICE LINE IS THE CASE THE RULE WAS WRITTEN FOR and cost_stack demonstrates it: the
line costs more than the devices sell for in every year, so it is not device cost of sales,
and solved across every available period pair the split ranges from -1.08 to +5.86 on the
device ratio. Unidentified, shown to be unidentified, and left alone.

NOTHING HERE IS AN INPUT TO THE MODEL. It reads the study's committed answer and prices a
construction against it; the model does not read this file back.
"""
from __future__ import annotations

import json
import os

import coc_run as COCRUN          # the house macro path, through the study's own resolver
import cost_stack as C
import segments as S

HERE = os.path.dirname(os.path.abspath(__file__))
NUMBERS = os.path.join(HERE, 'study_numbers.json')


#: The FY2025 depreciable gross cost, note 10 — the base repairs and maintenance maintains.
#: Named here rather than read back from the terminal record, which publishes the LIFE (the
#: same figure over the year's charge) rather than the base itself.
GROSS_DEPRECIABLE = 134_634_729 / 1000.0


def _load():
    with open(NUMBERS) as f:
        return json.load(f)


def price(d=None):
    """Each line on the base the filings name, against the model's own forecast path."""
    d = d or _load()
    fc = d['forecast']
    yrs = list(fc)
    rev = [fc[y]['rev'] for y in yrs]                       # SR million
    dr = d['drivers']
    # [R-MACRO-01] a study may not carry an inflation number of its own; this is the house
    # Saudi ladder, read through the same resolver the model itself uses.
    fy = d['drivers'].get('forecast_years') or [2026 + i for i in range(len(yrs))]
    infl = [COCRUN.MACRO.inflation(y) for y in fy]
    ksa_real = dr['segment_real_growth']['stc']
    sub_real = dr['unit_volume_real']
    dna_pct, capex_pct = dr['dna_pct'], dr['capex_pct']

    rev25 = float(C.REVENUE[2]) / 1000.0
    ksa25 = float(S.REVENUE['stc'][2]) / 1000.0

    def held(base25):
        """The model's construction: a constant share of the revenue it is allocated to."""
        return [base25 / rev25 * r for r in rev]

    out = {}

    # 1. the levy, on the Saudi segment the sub-note names
    levy25 = C.GOVERNMENT_CHARGES['Commercial service provisioning fees'][2] / 1000.0
    ksa, v = [], ksa25
    for i in range(len(yrs)):
        v *= (1.0 + ksa_real) * (1.0 + infl[i])
        ksa.append(v)
    out['Commercial service provisioning fees'] = (held(levy25),
                                                   [levy25 / ksa25 * k for k in ksa])

    # 2. licence fees, at their own measured growth
    lic = [x / 1000.0 for x in C.GOVERNMENT_CHARGES['License fees']]
    lic_cagr = (lic[2] / lic[0]) ** 0.5 - 1.0
    own, v = [], lic[2]
    for _ in yrs:
        v *= (1.0 + lic_cagr)
        own.append(v)
    out['License fees'] = (held(lic[2]), own)

    # 3. repairs and maintenance, on the asset base. THE BASE GROWS BY NET CAPEX OVER THE
    #    BASE — a rate — never by the difference of two shares of revenue, which is not one.
    rm25 = C.COST_OF_REVENUES['Repairs and maintenance'][2] / 1000.0
    base = GROSS_DEPRECIABLE
    own, v = [], rm25
    for i in range(len(yrs)):
        net_add = (capex_pct[i] - dna_pct[i]) * rev[i]
        v *= (1.0 + net_add / base) * (1.0 + infl[i])
        base += net_add
        own.append(v)
    out['Repairs and maintenance'] = (held(rm25), own)

    # 4. contract-cost amortisation, on subscribers
    ca25 = C.COST_OF_REVENUES['Amortisation and impairment of contract costs'][2] / 1000.0
    own, v = [], ca25
    for i in range(len(yrs)):
        v *= (1.0 + sub_real) * (1.0 + infl[i])
        own.append(v)
    out['Amortisation and impairment of contract costs'] = (held(ca25), own)

    return dict(years=yrs, revenue=rev, lines=out)


def value_effect(d=None):
    """Price the whole decomposition through the study's OWN committed sensitivity grid."""
    d = d or _load()
    p = price(d)
    net = sum(own[-1] - h[-1] for h, own in p['lines'].values())
    margin_shift = -net / p['revenue'][-1]
    sens = d['sens']
    ms, tbl = sens['margin_steps'], sens['table_cm']
    mid = ms.index(0.0)
    step = ms[mid + 1] - ms[mid]
    per_unit = (tbl[mid + 1][mid] - tbl[mid][mid]) / step
    central = d['central']
    return dict(net_cost_change_fy_final=net, margin_shift=margin_shift,
                sar_per_unit_of_margin=per_unit,
                central_effect=margin_shift * per_unit,
                central_before=central, central_after=central + margin_shift * per_unit,
                pct_of_central=margin_shift * per_unit / central)


def record(d=None):
    d = d or _load()
    p = price(d)
    v = value_effect(d)
    return dict(
        ticker='STC',
        # [R-ENF-06] the answer this artefact was generated against.
        published_central=d['central'], published_spot=d['spot'],
        years=p['years'], revenue=p['revenue'],
        lines={k: dict(held_at_share_of_revenue=h, on_its_own_base=o,
                       final_year_difference=o[-1] - h[-1])
               for k, (h, o) in p['lines'].items()},
        not_priced={
            'Network access charges': 'no disclosed unit rate',
            'Employees costs': 'no headcount disclosed anywhere in the filings',
            'Others': 'a residual of three unrelated things',
            'Frequency spectrum fees': ('lumpy, and the first Saudi licence expiry falls '
                                        'inside the explicit window with no disclosed '
                                        'renewal cost — a gap to name, not a driver'),
        },
        value_effect=v,
        finding=(
            'Put each line on the base the filings name and the model\'s final forecast '
            'year moves by a net %s of cost, which is %.3f points of margin and %.2f%% of '
            'the central. The offsets run BOTH ways and that is the finding: the levy and '
            'the licence fee fall against a group that grows faster than the Saudi segment '
            'they are charged on, while maintenance and subscriber-acquisition costs rise '
            'against it, and the two nearly cancel. The blended construction is not hiding '
            'a mix effect here — which is worth knowing precisely because the same test on '
            'another name in this book found one worth seventeen per cent.'
            % ('SR %.1f million' % v['net_cost_change_fy_final'],
               100 * v['margin_shift'], 100 * v['pct_of_central'])),
    )


if __name__ == '__main__':
    r = record()
    v = r['value_effect']
    print('%-42s %10s %10s %9s' % ('line', 'held', 'own base', 'diff'))
    print('-' * 74)
    for k, x in r['lines'].items():
        print('%-42s %10.1f %10.1f %+9.1f'
              % (k[:42], x['held_at_share_of_revenue'][-1], x['on_its_own_base'][-1],
                 x['final_year_difference']))
    print('-' * 74)
    print('%-42s %10s %10s %+9.1f'
          % ('NET', '', '', v['net_cost_change_fy_final']))
    print()
    print('margin shift %+.4f points   central %.4f -> %.4f   (%+.3f%%)'
          % (100 * v['margin_shift'], v['central_before'], v['central_after'],
             100 * v['pct_of_central']))
    print()
    for k, why in r['not_priced'].items():
        print('  not priced: %-30s %s' % (k, why))
    with open(os.path.join(HERE, 'cost_decomposition.json'), 'w') as f:
        json.dump(r, f, indent=1)
    print('\nwrote cost_decomposition.json')
