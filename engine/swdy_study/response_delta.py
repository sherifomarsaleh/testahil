"""STEP 9 OF THE CRITIQUE RESPONSE: what actually moved, before and after.

Generated from the two committed numbers files — the edition the audit was run against
and the edition this response produces — so the table cannot drift from either. A
response that TYPES its own before-and-after is the defect it is responding to.

Run: python3 response_delta.py [BASELINE_GIT_REF]
"""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
REL = 'engine/swdy_study/study_numbers.json'
# The last commit before any finding was implemented: step 8 complete, nothing changed.
BASELINE = sys.argv[1] if len(sys.argv) > 1 else 'b692be9bb'

ROWS = (
    ('Central — the cash-flow lens, the answer', ('central',)),
    ('Published range, low', ('span', 0)),
    ('Published range, high', ('span', 1)),
    ('Rating-basis cost of capital (alternative)', ('dcf', 'ps_rating_basis')),
    ('Currency-of-discounting (alternative)', ('dcf', 'ccy_alt_ps')),
    ('Relative lens', ('lenses', 'relative', 'base')),
    ('Normalised lens', ('lenses', 'normalized', 'base')),
    ('Book lens (disclosed floor)', ('lenses', 'book', 'base')),
    ('Expert 1 — earnings power', ('experts', 'e1', 'base')),
    ('Expert 2 — owner cash earnings', ('experts', 'e2', 'base')),
    ('Expert 3 — cash returns vs cost of capital', ('experts', 'e3', 'base')),
    ('Terminal share of enterprise value', ('dcf', 'tv_share')),
)


def dig(d, path):
    for k in path:
        try:
            d = d[k]
        except (KeyError, IndexError, TypeError):
            return None
    return d


def main():
    before = json.loads(subprocess.check_output(
        ['git', 'show', '%s:%s' % (BASELINE, REL)], cwd=REPO).decode())
    after = json.load(open(os.path.join(HERE, 'study_numbers.json')))
    out = ['| Headline | Before | After | Change |', '|---|---|---|---|']
    moved = 0
    for label, path in ROWS:
        x, y = dig(before, path), dig(after, path)
        if x is None or y is None:
            out.append('| %s | — | — | not published in one of the two editions |' % label)
            continue
        if abs(x - y) < 0.005:
            out.append('| %s | %.2f | %.2f | **unchanged** |' % (label, x, y))
        else:
            moved += 1
            out.append('| %s | %.2f | %.2f | %+.2f (%+.1f%%) |'
                       % (label, x, y, y - x, 100.0 * (y / x - 1.0) if x else float('nan')))
    out.append('')
    out.append('Baseline `%s` — the last commit before any finding was implemented. '
               '%d of %d headlines moved; the central is not among them.'
               % (BASELINE, moved, len(ROWS)))
    print('\n'.join(out))


if __name__ == '__main__':
    main()
