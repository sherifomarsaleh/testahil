#!/usr/bin/env python3
"""ADIB (EGX) — corrections, under the two-clause test. Pre-registration §5.

EXPANDING WINDOW ONLY. The correction applied at origin `o` is estimated from errors
that had RESOLVED before `o` - that is, from origins whose whole horizon ran out on or
before `o`. At the FY2014-FY2018 origins almost nothing has resolved, so most origins
get no correction at all and say so.

HALF STRENGTH by default. Applied only where the bias holds its sign across BOTH eras.
Reset at basis break B2 (the loss era ends at FY2013), so no error observed on a
loss-era target ever feeds a correction.

THE SECOND CLAUSE IS NOT A FORMALITY [L-003]. A correction that passes its own test and
does not match how that driver class is built across the market's book is usually
correcting our own mis-specification, and adopting it would hide the defect. That clause
is answered in words at the end of this file and in the training record, not by a number.
"""
from __future__ import annotations
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import panel, macro, bottom_up as bu, score  # noqa: E402

STRENGTH = 0.5
STABLE_ONLY = True
RESET_AFTER = 2013           # break B2: no target year at or before FY2013 feeds a correction


def resolved_errors(before_origin, line, hmax=5):
    """Errors an analyst standing at `before_origin` could already have observed.

    A cell (o', h) is resolved at o if o' + h <= o AND its target year is after the
    B2 reset. The origin itself is excluded - its own error is exactly what is being
    forecast.
    """
    out = []
    for o2 in bu.ORIGINS:
        if o2 >= before_origin:
            continue
        m = bu.build(o2, hmax)
        if not m:
            continue
        for h in range(1, hmax + 1):
            y = o2 + h
            if y > before_origin or y > bu.LAST or y <= RESET_AFTER:
                continue
            p = m.get(y, {}).get(line)
            a = score.actual(y, line)
            e, st = score.logerr(p, a)
            if st == 'ok':
                out.append(e)
    return out


def stable_sign(line):
    """Does the bias hold its sign across both eras? Measured on the full record."""
    rows = score.cells()
    ok = [r for r in rows if r['method'] == 'model' and r['line'] == line
          and r['status'] == 'ok']
    early = [r['e'] for r in ok if r['origin'] <= 2017]
    late = [r['e'] for r in ok if r['origin'] >= 2018]
    if not early or not late:
        return False, None, None
    a, b = sum(early) / len(early), sum(late) / len(late)
    return (a * b > 0), a, b


def correction_at(o, line, hmax=5):
    """The half-strength expanding-window correction factor for `line` at origin `o`."""
    es = resolved_errors(o, line, hmax)
    if len(es) < 3:
        return 1.0, 0, 'too few resolved cells (%d)' % len(es)
    if STABLE_ONLY:
        st, _, _ = stable_sign(line)
        if not st:
            return 1.0, len(es), 'bias changes sign between eras - NOT a bias'
    bias = sum(es) / len(es)
    return math.exp(-STRENGTH * bias), len(es), 'applied'


def adjusted_cells(hmax=5):
    """Rebuild the aggregates FROM ADJUSTED DRIVERS, not by scaling the answer.

    The corrections are applied to the DRIVER lines - the balance-sheet volume, the
    yield-bearing income lines, fees, overheads and the loss charge - and PBT and net
    profit are recomputed from them. Correcting net profit directly would be a fudge on
    the answer, which is the thing L-002 exists to forbid.
    """
    DRIVERS = ['fin_customers', 'cust_deposits', 'total_assets', 'fin_income',
               'cost_funds', 'net_fees', 'other_nii', 'admin', 'other_op', 'ecl']
    rows, log = [], {}
    for o in bu.ORIGINS:
        m = bu.build(o, hmax)
        if not m:
            continue
        meta = m['_meta']
        k = {}
        for f in DRIVERS:
            k[f], n, why = correction_at(o, f, hmax)
            log.setdefault(o, {})[f] = dict(factor=k[f], n_resolved=n, why=why)
        txr, nci = meta['tax_rate'], meta['nci_share']
        for h in range(1, hmax + 1):
            y = o + h
            if y > bu.LAST or y not in m:
                continue
            adj = {f: m[y][f] * k.get(f, 1.0) for f in DRIVERS}
            adj['net_funds'] = adj['fin_income'] + adj['cost_funds']
            adj['pbt'] = (adj['net_funds'] + adj['net_fees'] + adj['other_nii']
                          + adj['other_op'] + adj['ecl'] + adj['admin'])
            adj['tax'] = -txr * adj['pbt']
            adj['np'] = adj['pbt'] + adj['tax']
            adj['np_parent'] = adj['np'] * (1.0 - nci)
            for f in score.LINES:
                a = score.actual(y, f)
                pr, pa = m[y].get(f), adj.get(f)
                er, sr = score.logerr(pr, a)
                ea, sa = score.logerr(pa, a)
                rows.append(dict(origin=o, h=h, year=y, line=f,
                                 raw=pr, adj=pa, actual=a,
                                 e_raw=er, e_adj=ea, s_raw=sr, s_adj=sa))
    return rows, log


def share_drift_sensitivity(hmax=5):
    """REPORTED, NEVER SELECTED. What if R2 let the share drift at its trailing rate?

    R2 holds ADIB's share of system credit FLAT at the origin. That is the protocol's
    own conservatism - volume anchored on an exogenous driver, never on the company's
    own trend. This measures the cost of that choice; it does not adopt the alternative.
    """
    out = []
    for o in bu.ORIGINS:
        s0, s3 = bu.share_of_system(o), bu.share_of_system(o - 3)
        if not s0 or not s3:
            continue
        g = (s0 / s3) ** (1 / 3.0) - 1.0
        m = bu.build(o, hmax)
        if not m:
            continue
        for h in range(1, hmax + 1):
            y = o + h
            if y > bu.LAST or y not in m:
                continue
            a = score.actual(y, 'fin_customers')
            pr = m[y]['fin_customers']
            pd = pr * (1.0 + g) ** h
            er, _ = score.logerr(pr, a)
            ed, _ = score.logerr(pd, a)
            if er is not None and ed is not None:
                out.append((o, h, g, er, ed))
    return out


def main():
    print('=== STABILITY GATE: does each driver bias hold its sign across eras? ===')
    print('%-15s %10s %10s  %s' % ('driver', 'early', 'late', 'verdict'))
    stab = {}
    for f in score.LINES:
        st, a, b = stable_sign(f)
        stab[f] = st
        if a is None:
            print('%-15s %10s %10s  no cells in one era' % (f, '-', '-'))
            continue
        print('%-15s %+10.3f %+10.3f  %s'
              % (f, a, b, 'stable - correctable' if st else 'SIGN FLIPS - not a bias, no correction'))
    print()

    rows, log = adjusted_cells()
    print('=== ADJUSTED vs RAW, BY ORIGIN (MAE on net profit attributable) ===')
    print('%-8s %6s %10s %10s %9s  %s' % ('origin', 'n', 'raw MAE', 'adj MAE', 'change', 'corrections applied'))
    for o in bu.ORIGINS:
        sel = [r for r in rows if r['origin'] == o and r['line'] == 'np_parent'
               and r['s_raw'] == 'ok' and r['s_adj'] == 'ok']
        if not sel:
            print('%-8s %6s  (no scorable net-profit cell)' % (bu.fy(o), '-'))
            continue
        mr = sum(abs(r['e_raw']) for r in sel) / len(sel)
        ma = sum(abs(r['e_adj']) for r in sel) / len(sel)
        applied = sorted(f for f, d in log.get(o, {}).items() if d['why'] == 'applied')
        print('%-8s %6d %10.3f %10.3f %+8.1f%%  %s'
              % (bu.fy(o), len(sel), mr, ma, 100 * (ma / mr - 1) if mr else float('nan'),
                 ','.join(applied) or 'none'))
    print()

    print('=== ADJUSTED vs RAW, WHOLE RECORD, PER DRIVER ===')
    print('%-15s %5s %9s %9s %9s %9s' % ('driver', 'n', 'raw bias', 'adj bias', 'raw MAE', 'adj MAE'))
    for f in score.LINES:
        sel = [r for r in rows if r['line'] == f and r['s_raw'] == 'ok' and r['s_adj'] == 'ok']
        if not sel:
            continue
        print('%-15s %5d %+9.3f %+9.3f %9.3f %9.3f'
              % (f, len(sel),
                 sum(r['e_raw'] for r in sel) / len(sel),
                 sum(r['e_adj'] for r in sel) / len(sel),
                 sum(abs(r['e_raw']) for r in sel) / len(sel),
                 sum(abs(r['e_adj']) for r in sel) / len(sel)))
    print()

    sd = share_drift_sensitivity()
    if sd:
        mr = sum(abs(x[3]) for x in sd) / len(sd)
        md = sum(abs(x[4]) for x in sd) / len(sd)
        br = sum(x[3] for x in sd) / len(sd)
        bd = sum(x[4] for x in sd) / len(sd)
        print('=== SENSITIVITY, REPORTED NEVER SELECTED: R2 share-flat vs share-drift ===')
        print('financing volume, %d cells:  share-FLAT bias %+.3f MAE %.3f  |  '
              'share-DRIFT bias %+.3f MAE %.3f' % (len(sd), br, mr, bd, md))
        print('mean trailing 3-year share drift across origins: %+.1f%%/yr'
              % (100 * sum(x[2] for x in sd) / len(sd)))

    json.dump(dict(stability=stab, log={str(k): v for k, v in log.items()},
                   strength=STRENGTH, reset_after=RESET_AFTER),
              open(os.path.join(HERE, 'corrections_log.json'), 'w'), indent=1)


if __name__ == '__main__':
    main()
