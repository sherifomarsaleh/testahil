"""ARCC walk-forward — the two-clause promotion test for corrections.

A correction is applied at HALF STRENGTH, expanding window only (it may use
errors resolved strictly before its origin), and it enters the live drivers only
if it passes BOTH clauses:

  CLAUSE 1  its own test -- the bias holds its sign in every era it is observed
            in, and survives the block bootstrap at all three block lengths.
  CLAUSE 2  it is consistent with how that driver class is built across the
            market's book.

CLAUSE 2 IS NOT A FORMALITY AND HAS ALREADY DONE ITS JOB ONCE.  On PHDC a
finance-cost correction passed clause 1 convincingly and failed clause 2, and
that failure is what exposed a wrong denominator: the "bias" was arithmetic, not
evidence.  A CORRECTION FACTOR IS HONEST WHEN THE MODEL IS RIGHT AND REALITY IS
AWKWARD; WHEN THE MODEL IS WRONG, A CORRECTION HIDES IT.

Anything that fails is a WATCH FLAG: recorded, graded live, revisited at every
refit, acted on by nobody.
"""

import json
import bottom_up as B
import score as S

# Clause 2 is a JUDGEMENT and is therefore written down, with its reason, rather
# than computed.  Each entry is decided against how the driver class is built
# across this book -- not against this name's own numbers, which is the whole
# point of the second clause.
CLAUSE2 = {
    'cpt': (False,
            "REFUSED. 71% of this driver's error disappears under perfect macro "
            "foresight (MAE 0.406 knowable, 0.120 with the realised FX path). "
            "The driver is not biased; the MACRO PATH IT WAS GIVEN was wrong, "
            "and no origin could have known the pound would go from 15.6 to "
            "49.2. Scaling cost per tonne up by 16% at every origin would be "
            "correcting for an unforecastable currency collapse, and would be "
            "flatly wrong in a stable-currency era -- which is most of this "
            "book. Every other cement and heavy-industrial study builds cost "
            "per tonne from a disclosed cost stack escalated per driver class, "
            "with no name-level multiplier anywhere. WATCH FLAG."),
    'fin': (False,
            "REFUSED, and the refusal names a SPECIFICATION DEFECT rather than "
            "a bias. Eleven of twenty-five cells project finance costs of "
            "exactly zero against an actual charge: the pre-registered debt "
            "path amortises at the trailing average repayment and never "
            "re-borrows, so once ARCC settled its debt in FY2023 the rule had "
            "the company debt-free forever -- and it then signed a EUR 25mn "
            "EBRD facility in 2025. A multiplier on zero is still zero. This is "
            "L-002 exactly: fix the wiring, do not reach for a factor. WATCH "
            "FLAG, with the defect named for the next edition."),
}


def candidates(summary):
    """Clause 1: robust across all three block lengths AND sign-stable by era."""
    out = {}
    for d, r in summary.items():
        if not r.get('n'):
            continue
        out[d] = dict(bias=r['bias'], robust=r.get('robust', False),
                      sign_stable=r.get('sign_stable', False),
                      by_era={k: v['bias'] for k, v in r.get('by_era', {}).items()},
                      passes_clause1=bool(r.get('robust') and r.get('sign_stable')))
    return out


def expanding_correction(driver, origin, rows):
    """Half strength, on errors RESOLVED before this origin only."""
    prior = [r['e'] for r in rows
             if r['driver'] == driver and r['e'] is not None and r['year'] < origin]
    if len(prior) < 3:
        return 0.0
    return -0.5 * (sum(prior) / len(prior))


def test_adjusted_vs_raw(driver, rows):
    """Rebuild the driver with its correction and compare, BY ORIGIN."""
    out = []
    for o in B.ORIGINS:
        adj = expanding_correction(driver, o, rows)
        if adj == 0.0:
            continue
        sub = [r for r in rows if r['driver'] == driver and r['origin'] == o
               and r['e'] is not None]
        if not sub:
            continue
        raw = sum(abs(r['e']) for r in sub) / len(sub)
        new = sum(abs(r['e'] + adj) for r in sub) / len(sub)
        out.append(dict(origin=o, adj=adj, mae_raw=raw, mae_adj=new,
                        improves=new < raw, n=len(sub)))
    return out


if __name__ == '__main__':
    rows = S.build(True)
    summ = S.summarise(rows)
    cand = candidates(summ)
    log = {'candidates': cand, 'tests': {}, 'decisions': {}}

    print('=== CLAUSE 1 — its own test ===')
    print('%-10s %8s %-8s %-14s %s' % ('driver', 'bias', 'robust', 'era-stable', 'clause 1'))
    for d, c in cand.items():
        print('%-10s %8.3f %-8s %-14s %s'
              % (d, c['bias'], 'YES' if c['robust'] else 'no',
                 'yes' if c['sign_stable'] else 'NO',
                 'PASS' if c['passes_clause1'] else 'fail'))

    passed = [d for d, c in cand.items() if c['passes_clause1']]
    print('\nclause 1 passed by: %s' % (', '.join(passed) or 'nothing'))

    print('\n=== ADJUSTED vs RAW, BY ORIGIN (half strength, expanding window) ===')
    for d in passed:
        t = test_adjusted_vs_raw(d, rows)
        log['tests'][d] = t
        if not t:
            print('  %-8s no origin has three prior resolved errors — untestable' % d)
            continue
        ok = sum(1 for x in t if x['improves'])
        print('  %-8s %d of %d origins improve' % (d, ok, len(t)))
        for x in t:
            print('      FY%d  adj %+.3f   MAE %.3f -> %.3f  %s'
                  % (x['origin'], x['adj'], x['mae_raw'], x['mae_adj'],
                     'better' if x['improves'] else 'WORSE'))

    print('\n=== CLAUSE 2 — consistency with how the class is built across the book ===')
    promoted, watch = [], []
    for d in passed:
        ok, why = CLAUSE2.get(d, (False, 'no clause-2 judgement recorded — '
                                          'refused by default, because an '
                                          'unanswered question must not pass '
                                          'as a clean result'))
        log['decisions'][d] = {'promoted': ok, 'reason': why}
        (promoted if ok else watch).append(d)
        print('\n  %s: %s' % (d, 'PROMOTED' if ok else 'WATCH FLAG'))
        for line in [why[i:i + 74] for i in range(0, len(why), 74)]:
            print('      %s' % line)

    print('\n' + '=' * 72)
    print('PROMOTED INTO THE LIVE DRIVERS: %s' % (', '.join(promoted) or 'NOTHING'))
    print('WATCH FLAGS (recorded, graded live, acted on by nobody): %s'
          % (', '.join(watch) or 'none'))
    # corrections_log.json in the shape lessons_harvest.py reads: one entry per
    # origin, each naming what was applied and what it did to the average miss.
    log['log'] = []
    for d in passed:
        for x in log['tests'].get(d, []):
            log['log'].append(dict(
                origin=x['origin'], driver=d,
                corrections={d: dict(applied=x['adj'],
                                     outcome_mae_change=x['mae_adj'] - x['mae_raw'])}))
    json.dump(log, open('corrections_log.json', 'w'), indent=1, default=str)
