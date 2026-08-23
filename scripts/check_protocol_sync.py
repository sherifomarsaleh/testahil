#!/usr/bin/env python3
"""Check the two governing documents carry the same standing rules.  [R-DOC-01]

WHY
    CLAUDE.md records that the condensed digest "has gone stale three times already this
    session from exactly this drift". The remedy in place was a written instruction to
    remember to update both files. Nothing checked it, and on 23-Aug-2026 the copy held
    outside the repository was found to be one amendment behind — which is the same class
    of failure, on the document that describes how to avoid it.

HOW
    Every standing rule adopted from 23-Aug-2026 carries a stable identifier in the form
    [R-AREA-NN]: R-ENF-01, R-SIGCM-02, R-BETA-04 and so on. The identifier appears in the
    full protocol, in the condensed digest, and in the code that enforces the rule. This
    script compares the ID sets and fails on any rule present in one document and not the
    other.

    Rules adopted BEFORE 23-Aug-2026 are not retro-tagged in bulk — that would be a large
    edit with no reader benefit and real risk of a transcription error. Each acquires an ID
    the next time it is amended. The set therefore grows from the bottom up, and this check
    binds only what has been tagged.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FULL = os.path.join(ROOT, 'engine', 'Standing_Research_Protocol.md')
DIGEST = os.path.join(ROOT, 'engine', 'PROJECT_INSTRUCTIONS_11-07-2026.md')
CODE_DIRS = [os.path.join(ROOT, 'engine'), os.path.join(ROOT, 'scripts')]

RULE_ID = re.compile(r'\[(R-[A-Z]{2,6}-\d{2})[,\]]')


def ids_in(path):
    return set(RULE_ID.findall(open(path, encoding='utf-8').read()))


def ids_in_code():
    found = {}
    for d in CODE_DIRS:
        for dirpath, _, files in os.walk(d):
            if '__pycache__' in dirpath:
                continue
            for f in files:
                if not f.endswith(('.py', '.js', '.yml')):
                    continue
                p = os.path.join(dirpath, f)
                try:
                    txt = open(p, encoding='utf-8', errors='ignore').read()
                except OSError:
                    continue
                for rid in RULE_ID.findall(txt):
                    found.setdefault(rid, []).append(os.path.relpath(p, ROOT))
    return found


REV = re.compile(r'^(?:DIGEST|PROTOCOL) REVISION (\d{4}-\d{2}-\d{2}[a-z]?)\b')


def revision(path):
    """The revision stamp both documents must carry as their first line.  [R-DOC-01]

    Added after three rounds in one day of pasting back a copy one edit stale: every
    revision of a 54,000-character block looks identical to every other, so a copy has to
    be able to declare its own age. An UNBUMPED stamp is worse than none -- it certifies a
    copy that has moved -- so the gate also fails when the two documents disagree.
    """
    first = open(path, encoding='utf-8').readline()
    m = REV.match(first)
    return m.group(1) if m else None


def main():
    full, digest = ids_in(FULL), ids_in(DIGEST)
    rf, rd = revision(FULL), revision(DIGEST)
    if rf is None or rd is None:
        missing = [p for p, r in ((FULL, rf), (DIGEST, rd)) if r is None]
        print('FAIL — no revision stamp on: ' + ', '.join(os.path.basename(m) for m in missing))
        print('Both governing documents must open with "<DIGEST|PROTOCOL> REVISION YYYY-MM-DD[x]".')
        return 1
    if rf != rd:
        print(f'FAIL — revision stamps disagree: full protocol {rf}, digest {rd}. '
              f'Amend both in the same commit and bump both.')
        return 1
    print(f'revision stamp: {rf} (both documents agree)')
    code = ids_in_code()

    only_full = sorted(full - digest)
    only_digest = sorted(digest - full)
    both = sorted(full & digest)

    print(f'tagged rules — full protocol: {len(full)}   digest: {len(digest)}   in both: {len(both)}')
    for rid in both:
        where = code.get(rid)
        print(f'   {rid}  {"enforced in " + where[0] if where else "prose only"}')
    if only_full:
        print(f'\nFAIL — in the full protocol but NOT in the digest: {only_full}')
    if only_digest:
        print(f'\nFAIL — in the digest but NOT in the full protocol: {only_digest}')
    if only_full or only_digest:
        print('\nBoth files must carry the same standing rules. Amend them in the SAME '
              'commit — that is the rule this check exists to enforce.')
        return 1
    print('\nOK — the two governing documents carry the same tagged rules.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
