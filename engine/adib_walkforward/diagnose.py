#!/usr/bin/env python3
"""ADIB (EGX) — diagnostics: the macro/company split, the era sub-sample, the
per-origin side-by-side income statements. Pre-registration §4.

Three re-runs at every origin:
  1 AS PRE-REGISTERED  macro projected mechanically from origin-available data
  2 PERFECT MACRO      realised CPI and realised system credit; company drivers untouched
  3 PERFECT FORESIGHT  every driver at its realised value; the residual must be zero

THE SPLIT'S OWN CHECK, IN ITS BANK FORM. The protocol's check is that a unit volume
driver carries no inflation term and must return a zero macro share by construction. A
bank has no unit driver - every line it reports is nominal EGP. The equivalent here is
ADIB's SHARE OF SYSTEM CREDIT: numerator and denominator are nominal EGP of the same
year, so inflation cancels identically and the share must return a macro share of
EXACTLY ZERO. If it does not, the split is wired wrong and nothing below it is safe.
"""
from __future__ import annotations
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import panel, macro, bottom_up as bu, score  # noqa: E402


def realised_cpi(o, hmax=5):
    return {o + h: macro.CPI_PCT.get(o + h) for h in range(0, hmax + 1)
            if macro.CPI_PCT.get(o + h) is not None}


def realised_credit(o, hmax=5):
    return {o + h: macro.SYSTEM_CREDIT.get(o + h) for h in range(0, hmax + 1)
            if macro.SYSTEM_CREDIT.get(o + h) is not None}


def macro_split(lines=None, hmax=5):
    """MAE as pre-registered vs MAE on perfect macro, per line. Macro share of the miss."""
    lines = lines or score.LINES
    base = score.cells(hmax=hmax)
    perf = score.cells(hmax=hmax, cpi_path_fn=realised_cpi, credit_path_fn=realised_credit)

    def mae(rows, line):
        e = [abs(r['e']) for r in rows
             if r['method'] == 'model' and r['line'] == line and r['status'] == 'ok']
        return (sum(e) / len(e)) if e else None

    out = {}
    for f in lines:
        a, b = mae(base, f), mae(perf, f)
        if a is None or b is None or a == 0:
            out[f] = None
            continue
        out[f] = dict(mae_asreg=a, mae_perfect_macro=b,
                      macro_share=(a - b) / a, company_share=b / a)
    return out, base, perf


def share_driver_check(hmax=5):
    """The split's own check: ADIB's share of system credit must be macro-invariant.

    The share is projected FLAT at its origin value under every macro path, so its
    projection cannot move when the macro path is replaced. Measured, not asserted:
    the maximum absolute difference between the two runs' projected shares.
    """
    worst = 0.0
    for o in bu.ORIGINS:
        a = bu.build(o, hmax)
        b = bu.build(o, hmax, cpi_path=realised_cpi(o, hmax),
                     credit_path=realised_credit(o, hmax))
        if not a or not b:
            continue
        sa, sb = a['_meta']['share_of_system'], b['_meta']['share_of_system']
        worst = max(worst, abs(sa - sb))
    return worst


def era_tables(hmax=5):
    """All 11 origins vs the 9 whose whole five-year window sits in the profit era."""
    allr = score.cells(hmax=hmax)
    late = score.cells(origins=[o for o in bu.ORIGINS if o >= bu.ERA_BREAK], hmax=hmax)
    return allr, late


def side_by_side(o, hmax=5):
    """The projected-vs-actual income statement for one origin. Required for EVERY origin."""
    m = bu.build(o, hmax)
    if m is None:
        return None
    fields = ['fin_income', 'cost_funds', 'net_funds', 'net_fees', 'other_nii',
              'admin', 'other_op', 'ecl', 'pbt', 'tax', 'np', 'np_parent',
              'fin_customers', 'cust_deposits', 'total_assets']
    rows = []
    for h in range(1, hmax + 1):
        y = o + h
        if y > bu.LAST:
            break
        for f in fields:
            a = score.actual(y, f)
            p = m[y].get(f)
            rows.append((y, f, p, a, (p / a) if (a not in (None, 0)) else None))
    return rows, m['_meta']


def one_offs():
    """Every one-off in the history, classified, with the record shown both ways."""
    return [
     dict(year='FY2012', item='Cost of credit -978,291 on a EGP 5.1bn financing book',
          size_pct_pbt=None, kind='company / legacy-book cleanup',
          effect='Sets the FY2014 origin cost-of-risk driver to 6.25%, ten times any '
                 'later reading, and drives that origin to a projected LOSS at every '
                 'horizon. FY2014 is the only origin whose net-profit cells are '
                 'sign-broken.'),
     dict(year='FY2013 and FY2014', item='Cost of credit +69,144 and +65,290 (net releases)',
          kind='company / reversal of the FY2012 cleanup',
          effect='Cost of risk is NEGATIVE in the FY2015 origin window (-0.52%), so that '
                 'origin projects an impairment CREDIT at every horizon. Two of the five '
                 'sign-broken ecl cells come from here.'),
     dict(year='FY2015', item='Tax 414,722 on PBT 633,961 - a 65.4% effective rate',
          kind='company / deferred-tax-asset unwind from the loss era',
          effect='Lifts the trailing effective tax rate at the FY2016-FY2018 origins to '
                 '52-57%, against a statutory 22.5%. R13 reports the statutory '
                 'sensitivity beside it.'),
     dict(year='FY2016 Nov', item='EGP float, 8.9 -> ~18 per USD',
          kind='MACRO', effect='The single largest source of the under-forecast at the '
                              'FY2014-FY2016 origins.'),
     dict(year='FY2020', item='COVID; CBE 300bp cut in March; payment moratoria',
          kind='MACRO', effect='The FY2019 origin is the only origin that OVER-forecasts '
                              'net profit at h=1 (+0.356).'),
     dict(year='FY2021', item='Gain on sale of financial investments in subsidiaries 87,920',
          kind='company / disposal',
          effect='3.9% of FY2021 PBT. Inside the derived other_nii block; not separately '
                 'forecast and not excluded.'),
     dict(year='FY2022-FY2024', item='Three EGP devaluation steps, 19.2 -> 30.6 -> 45.3',
          kind='MACRO', effect='The FY2021-FY2023 origins under-forecast net profit by '
                              '0.03 to 0.70 in logs at h=1.'),
     dict(year='FY2022 and FY2021', item='Discontinued operations -5,806 and -22,859',
          kind='company', effect='Below 0.2% of PBT. Left inside reported np, which is '
                                'what a naive benchmark freezes.'),
    ]


def main():
    print('=== THE SPLIT\'S OWN CHECK (bank form) ===')
    w = share_driver_check()
    print('max |share_asreg - share_perfectmacro| over all origins: %.3e' % w)
    print('PASS - the share driver is macro-invariant by construction'
          if w < 1e-12 else 'FAIL - the split is wired wrong; nothing below it is safe')
    print()

    print('=== MACRO / COMPANY SPLIT (MAE, all 45 cells per line) ===')
    sp, base, perf = macro_split()
    print('%-15s %10s %10s %10s %10s' % ('driver', 'as reg', 'perf macro', 'macro%', 'company%'))
    for f in score.LINES:
        v = sp.get(f)
        if not v:
            print('%-15s   (not scorable)' % f)
            continue
        print('%-15s %10.3f %10.3f %9.0f%% %9.0f%%'
              % (f, v['mae_asreg'], v['mae_perfect_macro'],
                 100 * v['macro_share'], 100 * v['company_share']))
    print()

    print('=== ERA SUB-SAMPLE: all 11 origins vs the 9 from FY2016 (reported, not selected) ===')
    allr, late = era_tables()
    print('%-15s %20s %20s' % ('driver', 'all origins', 'FY2016+ origins'))
    print('%-15s %8s %10s %8s %10s' % ('', 'bias', 'MAE', 'bias', 'MAE'))
    for f in score.LINES:
        a = score.summarise(allr, 'model', by_h=False).get((f, 0))
        b = score.summarise(late, 'model', by_h=False).get((f, 0))
        if not (a and a.get('n')) or not (b and b.get('n')):
            continue
        print('%-15s %+8.3f %10.3f %+8.3f %10.3f' % (f, a['bias'], a['mae'], b['bias'], b['mae']))
    print()

    print('=== SKILL ON THE FY2016+ SUB-SAMPLE ===')
    for f in ('np_parent', 'pbt', 'net_funds', 'fin_customers'):
        k = score.skill(late, f)
        if k:
            print('%-15s n=%d  model %.3f  freeze %.3f  trend %.3f  vs freeze %+.0f%%  vs trend %+.0f%%'
                  % (f, k['n'], k['model'], k['freeze'], k['trend'],
                     100 * k['vs_freeze'], 100 * k['vs_trend']))

    json.dump(dict(share_check=w, macro_split=sp, one_offs=one_offs()),
              open(os.path.join(HERE, 'diagnostics.json'), 'w'), indent=1)


if __name__ == '__main__':
    main()
