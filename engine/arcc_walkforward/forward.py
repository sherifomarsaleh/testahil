"""ARCC — the forward view, with years 3-5 as RANGES built from this record.

[R-FCAL-01] §6: years 3 to 5 are published as RANGES drawn from this run's own
driver-error distribution, NEVER as points.  The walk-forward's second purpose is
exactly this -- calibrated uncertainty at the horizons where a point estimate is
a fiction -- and the first purpose (per-driver bias detection) is upstream of it.

The width comes from the measured log-error distribution at each horizon, so it
is this company's own record of how wrong this method has been at that distance,
not an assumed spread.
"""

import json
import math

import bottom_up as B
import panel as P
import score as S

# The study year, swept in before the build [SIGCM]: both disclosed 2026
# quarters, read off the audited interim filings.
H1_2026 = dict(sales=6080577747, sales_prior=5499911617,
               q1_sales=2995959350, q1_cogs=1709813469, q1_npat=943090736,
               src='Q2_2026_cons note 3 / Q1_2026_cons p5')


def error_quantiles(driver='sales'):
    """The measured log-error distribution, by horizon, from this run."""
    rows = S.build(True)
    out = {}
    for h in range(1, 6):
        es = sorted(r['e'] for r in rows
                    if r['driver'] == driver and r['h'] == h and r['e'] is not None)
        if len(es) < 2:
            continue
        def q(p):
            i = p * (len(es) - 1)
            lo, hi = math.floor(i), math.ceil(i)
            return es[lo] + (es[hi] - es[lo]) * (i - lo)
        out[h] = dict(n=len(es), p10=q(0.10), p50=q(0.50), p90=q(0.90),
                      lo=es[0], hi=es[-1])
    return out


def forward():
    """FY2026-FY2030 from the FY2025 origin, on the same pre-registered rules."""
    rows = []
    for h in range(1, 6):
        p = B.project(2025, h)
        rows.append(dict(h=h, year=2025 + h, sales=p['sales'], npat=p['npat'],
                         vol=p['vol'], rpt=p['rpt'], cpt=p['cpt'],
                         gp=p['gp'], margin=(p['sales'] - p['cogs']) / p['sales']))
    return rows


if __name__ == '__main__':
    fwd = forward()
    qs = error_quantiles('sales')
    qn = error_quantiles('npat')

    print('=== THE STUDY YEAR, SWEPT IN BEFORE THE BUILD ===')
    print('  H1-2026 group sales   EGP %.1fmn  (H1-2025: %.1fmn, +%.1f%%)'
          % (H1_2026['sales'] / 1e6, H1_2026['sales_prior'] / 1e6,
             100 * (H1_2026['sales'] / H1_2026['sales_prior'] - 1)))
    print('  Q1-2026 net profit    EGP %.1fmn' % (H1_2026['q1_npat'] / 1e6))
    print('  source: %s' % H1_2026['src'])

    print('\n=== FORWARD FROM FY2025, EGP million ===')
    print('%-6s %-3s %10s %10s %9s  %s' %
          ('year', 'h', 'sales', 'net profit', 'GM', 'published as'))
    for r in fwd:
        how = 'POINT' if r['h'] <= 2 else 'RANGE ONLY'
        print('%-6d %-3d %10.0f %10.0f %8.1f%%  %s'
              % (r['year'], r['h'], r['sales'] / 1e6, r['npat'] / 1e6,
                 100 * r['margin'], how))

    print('\n=== YEARS 3-5 AS RANGES, from this run\'s own error distribution ===')
    print('(a projection is divided by exp(error), because e = ln(proj/actual))')
    print('%-6s %-3s %2s %14s %14s %14s' %
          ('year', 'h', 'n', 'low', 'central', 'high'))
    out = {}
    for r in fwd:
        h = r['h']
        if h < 3 or h not in qs:
            continue
        lo = r['sales'] / math.exp(qs[h]['p90'])
        mid = r['sales'] / math.exp(qs[h]['p50'])
        hi = r['sales'] / math.exp(qs[h]['p10'])
        out[r['year']] = dict(h=h, n=qs[h]['n'], sales_low=lo, sales_mid=mid,
                              sales_high=hi, point=r['sales'])
        print('%-6d %-3d %2d %14.0f %14.0f %14.0f'
              % (r['year'], h, qs[h]['n'], lo / 1e6, mid / 1e6, hi / 1e6))

    print('\nthe error distribution these ranges are built from (log, sales):')
    for h, q in sorted(qs.items()):
        print('  h%d  n=%d  p10 %+.3f  p50 %+.3f  p90 %+.3f' %
              (h, q['n'], q['p10'], q['p50'], q['p90']))
    print('\n=== SENSITIVITY: the same ranges on the E3 (devaluation) cells only ===')
    print('reported, NOT selected on — the two are shown together because the')
    print('record cannot say which regime the next five years resemble.')
    rows = S.build(True)
    for h in (3, 4, 5):
        e3 = sorted(r['e'] for r in rows if r['driver'] == 'sales' and r['h'] == h
                    and r['e'] is not None and r['era'] == 'E3 devaluation')
        if len(e3) >= 2:
            print('  h%d  n=%d  min %+.3f  max %+.3f' % (h, len(e3), e3[0], e3[-1]))
        else:
            print('  h%d  n=%d — too few cells to quote a spread' % (h, len(e3)))

    print('\n!! HOW THIS RANGE MUST BE READ, and it is not a forecast of the company:')
    print('   it is the measured record of HOW WRONG THIS METHOD HAS BEEN at this')
    print('   distance, and that record is dominated by a single unrepeatable event')
    print('   -- the pound going from 15.6 to 49.2 between 2021 and 2025. The median')
    print('   error is negative because no origin could foresee that. Carrying the')
    print('   width forward assumes another shock of that size is as likely as not,')
    print('   which is a statement nobody has evidence for. The range is published')
    print('   with that caveat attached, and the bias inside it is NOT promoted into')
    print('   the drivers -- clause 2 refused exactly that correction on cost per')
    print('   tonne, and re-centring the range would have smuggled it back in.')

    print('\nAND THE WIDTH IS THE POINT. At h=5 the measured spread runs from')
    print('%+.3f to %+.3f in log terms — a range of roughly %.1fx on the level.'
          % (qs[5]['p10'], qs[5]['p90'],
             math.exp(qs[5]['p90'] - qs[5]['p10'])))
    print('A POINT ESTIMATE AT FIVE YEARS WOULD BE A FICTION, AND THIS RECORD IS')
    print('WHY THE STUDY PUBLISHES YEARS 3-5 AS RANGES.')

    json.dump({'forward': fwd, 'ranges': out, 'quantiles_sales': qs,
               'quantiles_npat': qn, 'study_year': H1_2026},
              open('forward_ranges.json', 'w'), indent=1, default=str)
