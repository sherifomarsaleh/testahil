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
#
# THE PREDICATE IS A PATH CONSTRUCTION, NOT THE WORD [RE-POINTED 03-Sep-2026]. The first
# draft keyed the population on the STRING "data.js" appearing anywhere, and three of the
# thirteen files it ratcheted never open the file at all: two carry "data.js" inside an
# external-reader SCRUB WORD LIST — the list of internal vocabulary a delivered document
# may not contain — and one names it in a prose comment, while each separately uses a
# regular expression for something else entirely (matching a scrub word against a
# paragraph, parsing a date out of a filename). Their work was right and the check fired
# on it. Per [R-COC-01] the answer is to RE-POINT the check at the quantity it means,
# never to widen it and never to change the work to satisfy it: a file reads the site's
# data if it RESOLVES THE PATH to it, or if it goes through the shared reader. Naming the
# file in a sentence is not reading it. The cost of the wrong predicate was not cosmetic —
# a ratchet entry standing over innocent work is an entry that would silently EXCUSE that
# file the day it did start parsing data.js by hand.
READS_RX = re.compile(r"""['\"]assets['\"]\s*[,/]\s*['\"]data\.js['\"]"""
                      r"""|['\"][^'\"]*assets/data\.js['\"]"""
                      r"""|import\s+site_data|from\s+site_data\b|site_data\.""")
# a real parse: either through the shared reader, or by evaluating the file in node
OK_RX = re.compile(r'(import\s+site_data|from\s+site_data|site_data\.|'
                   r'runInContext|vm\.createContext)')
# the construction the rule names
REGEX_RX = re.compile(r're\.(search|findall|finditer|match)\s*\(')

# A WRITER IS A DIFFERENT OBLIGATION, AND HOLDING IT TO THE READER'S ONE WAS THE CHECK
# POINTED AT THE WRONG MEASUREMENT [RE-POINTED 03-Sep-2026, per R-COC-01]. Three files
# WRITE assets/data.js, and each does assert-guarded string surgery — CORRECTLY, because a
# JSON round-trip would destroy the file's formatting and the prose comments a reader of
# the repository depends on. Forbidding a regex there would forbid the only sound way to
# do the job, so those three sat on the ratchet as a debt that could never be paid, which
# is the permanently-red check [R-ENF-02] forbids wearing a different hat.
#
# What a writer owes is not "read through the parse" but "prove the PARSER agrees with
# what you wrote", and that is where the real hole was. Every writer verified with
# `node --check`. A DUPLICATED KEY IS VALID JAVASCRIPT: node --check passes it, the parser
# takes the LAST and a regex takes the FIRST — which is the exact defect [R-ENF-03] was
# adopted on, a page publishing a support ABOVE its own close while both gates read the
# half the reader never saw. Demonstrated on a real copy of data.js in the negative
# control, not asserted. So a writer must call site_data.assert_written(), and one that
# appends LEDGER rows must also assert the lifecycle invariant the protocol has required
# since 29-Jul-2026 and which executed in no writer at all.
WRITES_RX = re.compile(r'open\(\s*DATA_JS\s*,\s*[\'"]w')
VERIFIES_RX = re.compile(r'site_data\.assert_written\s*\(')
LEDGER_RX = re.compile(r'insert_ledger\s*\(|insert_rows\s*\(')
LIFECYCLE_RX = re.compile(r'site_data\.assert_ledger_lifecycle\s*\(')


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
        if rel in ('engine/site_data.py', 'scripts/check_site_data_reader.py'):
            continue
        try:
            src = open(f, encoding='utf-8').read()
        except Exception:
            continue
        if not READS_RX.search(src):
            continue
        examined += 1
        # A NEGATIVE CONTROL PLANTS A BROKEN FILE ON PURPOSE, so requiring it to verify
        # that the file it deliberately corrupted parses to what it meant is incoherent —
        # the corruption IS what it meant, and a check firing there fires on work that is
        # right [R-COC-01]. THE EXEMPTION IS SCOPED TO THE WRITER CLAUSE IT WAS WRITTEN
        # FOR AND NOTHING ELSE. A first draft skipped these files entirely, which is an
        # exemption wider than its own reason: it also stopped checking whether a control
        # READS data.js by regular expression, where no argument excuses it, and it
        # removed five files from the population so the count fell 31 -> 26 for a reason
        # that had nothing to do with reading. A TRUE EXEMPTION ON THE WRONG OBJECT is
        # the safest hiding place there is — nobody is lying, the reason survives review,
        # and the work happens where the check does not reach.
        is_control = os.path.basename(rel).endswith('_negative_control.py')
        if WRITES_RX.search(src) and not is_control:
            # a writer is judged on whether it verifies, not on how it edits
            if not VERIFIES_RX.search(src):
                bad.append('%s (writes data.js and never asserts the parser agrees)' % rel)
            elif LEDGER_RX.search(src) and not LIFECYCLE_RX.search(src):
                bad.append('%s (appends LEDGER rows without asserting the lifecycle '
                           'invariant)' % rel)
            continue
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
