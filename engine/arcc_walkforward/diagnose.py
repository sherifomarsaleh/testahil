"""ARCC walk-forward — decomposition, per-origin statements, and the one thing
this record says most clearly.

Three jobs [R-FCAL-01 §4]: decompose the revenue and net-profit errors into the
drivers that caused them; show the projected-versus-actual income statement side
by side for EVERY origin; and list every sign case rather than letting it vanish.
"""

import json
import math

import bottom_up as B
import panel as P
import score as S


def decompose():
    """Revenue error = volume error + price error, in log space, exactly.

    ln(vol·rpt / (vol*·rpt*)) = ln(vol/vol*) + ln(rpt/rpt*).  The identity is
    what makes this a decomposition rather than an attribution."""
    out = []
    for o, h, y, p, a in B.cells():
        ev = math.log(p['vol'] / a['vol'])
        ep = math.log(p['rpt'] / a['rpt'])
        es = math.log(p['seg'] / a['seg'])
        ec = math.log(p['cpt'] / a['cpt'])
        out.append(dict(origin=o, h=h, year=y, e_seg=es, from_vol=ev,
                        from_price=ep, residual=es - ev - ep,
                        e_cost_per_t=ec,
                        margin_p=(p['sales'] - p['cogs']) / p['sales'],
                        margin_a=(a['sales'] - a['cogs']) / a['sales']))
    return out


def profit_bridge():
    """What the net-profit miss is MADE of, in EGP, line by line.

    Log error on net profit is nearly meaningless on its own when the level is
    small (FY2019 net profit is EGP 29mn on sales of EGP 3.1bn -- a 1% revenue
    miss is a 100% profit miss).  The bridge in EGP says which line did it."""
    out = []
    for o, h, y, p, a in B.cells():
        out.append(dict(
            origin=o, h=h, year=y,
            d_sales=p['sales'] - a['sales'],
            d_cash_cost=-(p['cash_cost'] - a['cash_cost']),
            d_dna=-(p['dna'] - a['dna']),
            d_ga=-(p['ga'] - a['ga']),
            d_fin=-(p['fin'] - a['fin']),
            d_fx=-(0.0 - (a['pbt'] - (a['sales'] - a['cogs'] - a['ga'] - a['fin']))),
            d_npat=p['npat'] - a['npat'],
            npat_p=p['npat'], npat_a=a['npat']))
    return out


def statements():
    """The projected-versus-actual income statement, EVERY origin. EGP million."""
    lines = []
    for o in B.ORIGINS:
        lines.append('')
        lines.append('### Origin FY%d — projected against actual, EGP million' % o)
        lines.append('')
        cells = [(h, y, p, a) for (oo, h, y, p, a) in B.cells() if oo == o]
        yrs = ' | '.join('FY%d' % y for _, y, _, _ in cells)
        lines.append('| line | ' + yrs + ' |')
        lines.append('|---|' + '---|' * len(cells))
        for label, key in (('Volume (kt)', 'vol'), ('Revenue/t (EGP)', 'rpt'),
                           ('Cash cost/t (EGP)', 'cpt'), ('Segment revenue', 'seg'),
                           ('Other revenue', 'other'), ('**Group sales**', 'sales'),
                           ('Cash cost', 'cash_cost'), ('D&A', 'dna'),
                           ('G&A', 'ga'), ('Finance costs', 'fin'),
                           ('**Net profit**', 'npat')):
            sc = 1.0 if key in ('vol', 'rpt', 'cpt') else 1e6
            row = []
            for _, _, p, a in cells:
                pv, av = p.get(key), a.get(key)
                row.append('%s / %s' % (
                    ('%.0f' % (pv / sc)) if pv is not None else '-',
                    ('%.0f' % (av / sc)) if av is not None else '-'))
            lines.append('| %s | ' % label + ' | '.join(row) + ' |')
        lines.append('')
        lines.append('*projected / actual*')
    return '\n'.join(lines)


if __name__ == '__main__':
    dec, br = decompose(), profit_bridge()
    json.dump({'decomposition': dec, 'profit_bridge': br},
              open('diagnostics.json', 'w'), indent=1)
    open('arcc_IS_projected_vs_actual_all_origins.md', 'w').write(
        '# ARCC — projected against actual, every origin\n'
        '\n*Internal training record. Never shown to a reader.*\n' + statements())

    print('=== REVENUE ERROR DECOMPOSED (log, segment revenue) ===')
    print('%-7s %-3s %8s %9s %9s %9s' %
          ('origin', 'h', 'e_seg', 'from vol', 'from px', 'residual'))
    for r in dec:
        print('%-7d %-3d %8.3f %9.3f %9.3f %9.3f' %
              (r['origin'], r['h'], r['e_seg'], r['from_vol'],
               r['from_price'], r['residual']))
    n = len(dec)
    print('\npooled: volume %.3f   price %.3f   (residual %.2e — the identity holds)'
          % (sum(r['from_vol'] for r in dec) / n,
             sum(r['from_price'] for r in dec) / n,
             max(abs(r['residual']) for r in dec)))

    print('\n=== MARGIN: what the model thought, and what happened ===')
    print('%-7s %-3s %-6s %9s %9s %9s' %
          ('origin', 'h', 'year', 'proj GM', 'act GM', 'miss pp'))
    for r in dec:
        print('%-7d %-3d %-6d %8.1f%% %8.1f%% %8.1f' %
              (r['origin'], r['h'], r['year'], 100 * r['margin_p'],
               100 * r['margin_a'], 100 * (r['margin_p'] - r['margin_a'])))

    print('\n=== SIGN CASES — listed, never dropped ===')
    rows = S.build(True)
    for r in rows:
        if r['sign_case']:
            print('  %s origin %d h%d FY%d: projected %.0f, actual %.0f (EGPmn)'
                  % (r['driver'], r['origin'], r['h'], r['year'],
                     (r['proj'] or 0) / 1e6, (r['actual'] or 0) / 1e6))
