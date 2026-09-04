#!/usr/bin/env python3
"""Prove check_source_rebinding.py fires on the defect it was written for [L-290].

The gate went green on its first run because the one instance had already been
fixed, and a check nobody has seen fail is not evidence. So the FERTIGLOBE
rebinding is reinjected here exactly as it shipped, alongside the shapes that must
NOT fire -- because a gate that fires on the ordinary case is the permanently-red
check [R-ENF-02] forbids, and the clean cases are what separate the two.

EVERY MUTATION IS ASSERTED TO HAVE LANDED before the gate runs on it. A fixture
that silently failed to inject its condition produces a green that proves nothing,
which is the failure [R-ENF-04] names and which this repository has already paid
for once in another negative control.
"""
import ast
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import check_source_rebinding as G                                    # noqa: E402


# 1. THE DEFECT EXACTLY AS IT SHIPPED: a constant naming the FY2025 statements,
#    read by inputs, then rebound to a note in the annual report, with further
#    inputs registered against it afterwards.
SHIPPED = '''
FS25 = "Fertiglobe plc, Consolidated Financial Statements FY2025 (PwC-signed)"
inp('cost_staff_fy25', 254.6, FS25 + " - employee benefit expenses", '2025-12-31', 'COMPANY')
FS25 = 'Fertiglobe plc, Annual Report 2025, note 15 (non-controlling interests)'
inp('nci_pct_sorfert', 0.4901, FS25 + " - Sorfert Algeria SpA", '2025-12-31', 'COMPANY')
inp('debt_usd_fy25', 1651.9, FS25 + " - borrowings", '2025-12-31', 'COMPANY')
'''

# 2. the same shape one statement tighter: rebound immediately after the read
TIGHT = '''
SRC = "statements A"
inp('a', 1.0, SRC, '2025-12-31', 'COMPANY')
SRC = "statements B"
inp('b', 2.0, SRC, '2025-12-31', 'COMPANY')
'''

# 3. an f-string source, which is stringy and must be caught the same way
FSTRING = '''
SRC = f"statements A"
inp('a', 1.0, SRC, '2025-12-31', 'COMPANY')
SRC = f"statements B"
inp('b', 2.0, SRC, '2025-12-31', 'COMPANY')
'''

# ---- clean cases, each a real shape this repository actually contains ----

# 4. THE ORDINARY SHAPE: assigned once, read many times
ONCE = '''
FS25 = "statements"
inp('a', 1.0, FS25 + " - one", '2025-12-31', 'COMPANY')
inp('b', 2.0, FS25 + " - two", '2025-12-31', 'COMPANY')
inp('c', 3.0, FS25 + " - three", '2025-12-31', 'COMPANY')
'''

# 5. two documents under TWO NAMES, which is the fix and must stay green
TWO_NAMES = '''
FS25 = "statements"
AR25_N15 = "annual report, note 15"
inp('a', 1.0, FS25 + " - one", '2025-12-31', 'COMPANY')
inp('b', 2.0, AR25_N15 + " - two", '2025-12-31', 'COMPANY')
'''

# 6. a name rebound BEFORE anything reads it -- building a constant up in steps is
#    ordinary and no input has been registered against the earlier value
BEFORE = '''
SRC = "statements"
SRC = SRC + " (signed)"
inp('a', 1.0, SRC, '2025-12-31', 'COMPANY')
inp('b', 2.0, SRC, '2025-12-31', 'COMPANY')
'''

# 7. a rebound name that is not a source at all -- never read by a registrar
NOT_A_SOURCE = '''
NOTE = "first"
inp('a', 1.0, "a literal source", '2025-12-31', 'COMPANY')
NOTE = "second"
print(NOTE)
'''

# 8. a non-string rebinding, which is a counter or an accumulator and not provenance
NUMERIC = '''
SRC = "statements"
n = 0
inp('a', 1.0, SRC, '2025-12-31', 'COMPANY')
n = 1
inp('b', 2.0, SRC, '2025-12-31', 'COMPANY')
'''

CASES = [
    ('the FERTIGLOBE rebinding exactly as it shipped', SHIPPED, True),
    ('rebound one statement after the first read', TIGHT, True),
    ('an f-string source rebound after a read', FSTRING, True),
    ('assigned once, read three times (the ordinary shape)', ONCE, False),
    ('two documents under two names (the fix)', TWO_NAMES, False),
    ('rebound BEFORE any input reads it', BEFORE, False),
    ('a rebound name no registrar ever reads', NOT_A_SOURCE, False),
    ('a numeric rebinding beside a stable source', NUMERIC, False),
]


def mutation_landed(name, src, want_fire):
    """The fixture must actually contain the condition it claims to test."""
    tree = ast.parse(src)
    assigns = G._module_level_string_names(tree)
    reads = G._reads_by_registrars(tree)
    if want_fire:
        ok = any(len(v) >= 2 for v in assigns.values()) and bool(reads)
        why = 'a string name assigned twice at module level, and a registration read'
    else:
        ok = bool(reads) or name.startswith('a rebound name')
        why = 'at least one registration call to be examined'
    return ok, why


def main():
    failures = []
    for name, src, want_fire in CASES:
        landed, why = mutation_landed(name, src, want_fire)
        if not landed:
            failures.append('%s: THE FIXTURE DID NOT INJECT ITS CONDITION (needs %s). '
                            'A green from a fixture that never carried the defect '
                            'proves nothing.' % (name, why))
            continue
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, 'compute.py')
            open(path, 'w', encoding='utf-8').write(src)
            findings, nreads = G.scan(path)
        fired = bool(findings)
        ok = fired == want_fire
        print('  [%s] %-52s fires=%-5s expected=%-5s' %
              ('OK ' if ok else 'BAD', name[:52], fired, want_fire))
        if findings:
            for f in findings:
                print('        ', f[:110])
        if not ok:
            failures.append(name)

    print()
    if failures:
        print('NEGATIVE CONTROL FAILED:')
        for f in failures:
            print('  -', f)
        return 1
    print('NEGATIVE CONTROL PASSED — the gate fires on all three offending shapes '
          'and on none of the five clean ones.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
