#!/usr/bin/env python3
"""[R-ENF-03] assets/data.js is read through a real JavaScript parse, everywhere.

The rule is not new. It was adopted after a READER — not a check — found a ticker page
publishing a support ABOVE its own close while both existing gates reported that page
clean: they parsed data.js with regular expressions, re.search returns the FIRST match, a
JavaScript object literal takes the LAST, and the entry declared its levels TWICE. Every
tool inspected the half the reader never saw.

WHAT WAS MEASURED ON 03-Sep-2026, four weeks after that rule was written down: eleven files
across the book read assets/data.js and NINE of them did it with a regular expression. Two
did it correctly. Nothing was wrong with the nine except that the rule lived in prose and
in the two places somebody had implemented it, which is the same finding as the prose-figure
gate, the sweep register and the external-reader scrub in the same week: A RULE THAT ONE
STUDY IMPLEMENTS IS A RULE THAT ONE STUDY OBEYS.

engine/site_data.py is now the shared reader. This gate requires any file that opens
assets/data.js to go through it or to evaluate the file itself (vm.runInContext), and
refuses a regular expression over its contents. Ratcheted [R-ENF-02] — the nine are listed
and allowed, the list may only ever SHORTEN — and population-anchored [R-ENF-04]: a run
that examined zero files FAILS, because a checker finding nothing to check is the failure
this rule's own family is named for.
"""
import argparse
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RATCHET = os.path.join(ROOT, 'engine', 'build_depth_audit', 'sitedata_outstanding.json')

# THE POPULATION IS "FILES THAT READ THE SITE'S DATA", WHICH INCLUDES THE ONES DOING IT
# CORRECTLY. A file that goes through the shared reader never mentions data.js at all, so a
# population keyed only on that string counts the offenders and none of the compliant files
# — and once every offender is fixed the gate would examine ZERO and refuse. The negative
# control caught exactly that: three of its cases failed on an empty population rather than
# on the condition each was written to test.
READS_RX = re.compile(r'data\.js|site_data')
# a real parse: either through the shared reader, or by evaluating the file in node
OK_RX = re.compile(r'(import\s+site_data|from\s+site_data|site_data\.|'
                   r'runInContext|vm\.createContext)')
# the construction the rule names
REGEX_RX = re.compile(r're\.(search|findall|finditer|match)\s*\(')


def files():
    out = []
    for pat in ('engine/*_study/*.py', 'engine/*.py', 'scripts/*.py'):
        out += glob.glob(os.path.join(ROOT, pat))
    return sorted(set(out))


def audit():
    """(examined, offenders) — files that read data.js without a real parse."""
    examined, bad = 0, []
    for f in files():
        rel = os.path.relpath(f, ROOT)
        if rel in ('engine/site_data.py', 'scripts/check_site_data_reader.py',
                   'scripts/check_site_data_reader_negative_control.py'):
            continue
        try:
            src = open(f, encoding='utf-8').read()
        except Exception:
            continue
        if not READS_RX.search(src):
            continue
        examined += 1
        if OK_RX.search(src):
            continue
        if REGEX_RX.search(src):
            bad.append(rel)
    return examined, bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--prune', action='store_true')
    a = ap.parse_args()

    rat = json.load(open(RATCHET)) if os.path.exists(RATCHET) else {}
    allowed = set(rat.get('outstanding', []))

    examined, bad = audit()
    if not examined:
        print('FAIL — examined zero files that read assets/data.js; an empty result is not '
              'a clean result [R-ENF-04]')
        return 1
    stranded = sorted(p for p in allowed if not os.path.exists(os.path.join(ROOT, p)))
    if stranded:
        print('FAIL — the ratchet names files that no longer exist: %s [R-ENF-04]'
              % stranded)
        return 1

    print('files reading assets/data.js: %d;  regex readers: %d' % (examined, len(bad)))
    for p in sorted(bad):
        print('  [%s] %s' % ('ratcheted' if p in allowed else 'NEW', p))
    fixed = sorted(allowed - set(bad))
    if fixed:
        print('\nNOW READING THROUGH A REAL PARSE — remove from the list (%d): %s'
              % (len(fixed), ', '.join(fixed)))

    if a.prune:
        keep = sorted(set(bad) & allowed)
        grown = sorted(set(bad) - allowed)
        if grown:
            print('\nREFUSING TO PRUNE — the list would GROW by %s. A ratchet may only ever '
                  'SHORTEN [R-ENF-02].' % grown)
            return 1
        rat['outstanding'] = keep
        json.dump(rat, open(RATCHET, 'w'), indent=1)
        print('\npruned: %d -> %d' % (len(allowed), len(keep)))
        return 0

    new = sorted(set(bad) - allowed)
    if new:
        print('\nFAIL — reads assets/data.js by regular expression: %s\n'
              'A regex over a JavaScript object literal returns the FIRST match where the '
              'parser takes the LAST. Use engine/site_data.py.' % new)
        return 1
    print('\nOK — no new violations. %d file(s) on the ratchet, which may only SHORTEN.'
          % len(allowed))
    return 0


if __name__ == '__main__':
    sys.exit(main())
