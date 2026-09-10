"""The projected-versus-actual income statement, side by side, for EVERY origin.

[R-FCAL-01] §4 requires this for every origin, not for a selection. INTERNAL.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bottom_up as B

OUT = os.path.join(HERE, 'swdy_IS_projected_vs_actual_all_origins.md')
LINES = [('A_revenue', 'Revenue'),
         ('D4_cables_revenue', '  cables'),
         ('D5_contracting_revenue', '  contracting'),
         ('D6_other_revenue', '  other'),
         ('A_cost_of_revenue', 'Cost of revenue'),
         ('A_gross_profit', 'Gross profit'),
         ('D10_sga', 'Selling, general and administrative'),
         ('D11_depreciation', 'Depreciation and amortisation'),
         ('D15_finance_costs', 'Finance costs'),
         ('D16_finance_income', 'Finance income'),
         ('D12_capex', 'Capital expenditure')]


def fmt(v):
    return '—' if v is None else ('%,.0f' % v).replace(',', ' ') if False else \
        ('%.0f' % v if abs(v) < 1000 else '{:,.0f}'.format(v))


def main():
    out = ['# SWDY — projected versus actual, every origin, every horizon',
           '',
           '**INTERNAL.** Never shown to a reader. EGP million except cable tonnage and',
           'per-tonne figures. `proj` is the mechanical rule at that origin; `act` is what',
           'the company reported. A cell is blank where the driver is outside its own',
           'definition window or the actual is absent — those are COUNTED in scores.json,',
           'never quietly dropped.', '']
    for o in B.ORIGINS:
        out.append('## Origin FY%d' % o)
        p = B.paths(o)
        out.append('')
        out.append('Macro as known at the origin: inflation %.2f%% (published for %s), real '
                   'GDP %.2f%% (published for %s), currency %+.2f%%, copper USD %s/t.'
                   % (100 * p['cpi'], p['cpi_year'], 100 * p['gdp'], p['gdp_year'],
                      100 * p['fx'], ('%.0f' % p['copper']) if p['copper'] else 'n/a'))
        r = B.borrowing_rate(o)
        if r:
            out.append('')
            out.append('Borrowing rate formed on the borrowings that actually bear it: '
                       '%.2f%%.' % (100 * r))
        out.append('')
        heads = ['line'] + sum([['FY%d proj' % (o + h), 'FY%d act' % (o + h)]
                                for h in B.HORIZONS if o + h <= 2025], [])
        out.append('| ' + ' | '.join(heads) + ' |')
        out.append('|' + '---|' * len(heads))
        projs = {h: B.project(o, h)[0] for h in B.HORIZONS if o + h <= 2025}
        acts = {h: B.actual(o + h) for h in B.HORIZONS if o + h <= 2025}
        for k, lab in LINES:
            row = [lab]
            for h in sorted(projs):
                pv, av = projs[h].get(k), acts[h].get(k)
                sc = 1e-6 if not k.startswith(('D1_', 'D2_', 'D3_')) else 1.0
                row += ['—' if pv is None else '{:,.0f}'.format(pv * sc),
                        '—' if av is None else '{:,.0f}'.format(av * sc)]
            out.append('| ' + ' | '.join(row) + ' |')
        for k, lab in (('D1_cable_volume_t', 'Cable volume (tonnes)'),
                       ('D2_cable_price_t', 'Cable price per tonne (EGP)'),
                       ('D3_cable_cost_t', 'Cable cost per tonne (EGP)')):
            row = [lab]
            any_ = False
            for h in sorted(projs):
                pv, av = projs[h].get(k), acts[h].get(k)
                any_ = any_ or pv is not None or av is not None
                row += ['—' if pv is None else '{:,.0f}'.format(pv),
                        '—' if av is None else '{:,.0f}'.format(av)]
            if any_:
                out.append('| ' + ' | '.join(row) + ' |')
        out.append('')
    open(OUT, 'w').write('\n'.join(out) + '\n')
    print('wrote %s (%d origins)' % (os.path.basename(OUT), len(B.ORIGINS)))


if __name__ == '__main__':
    main()
