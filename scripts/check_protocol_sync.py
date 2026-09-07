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
import json
import datetime as _dt
import subprocess
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FULL = os.path.join(ROOT, 'engine', 'Standing_Research_Protocol.md')
# [R-DOC-01] The digest is named for the day of its latest amendment, so the
# path is resolved by pattern — a typed filename here would strand this gate
# at the first rename. Exactly one match or fail loudly.
import glob as _glob
_digests = sorted(_glob.glob(os.path.join(ROOT, 'engine', 'PROJECT_INSTRUCTIONS_*.md')))
assert len(_digests) == 1, 'expected exactly one digest file, found %r' % _digests
DIGEST = _digests[0]
CODE_DIRS = [os.path.join(ROOT, 'engine'), os.path.join(ROOT, 'scripts')]

RULE_ID = re.compile(r'\[(R-[A-Z]{2,6}-\d{2})[,\]]')

# Ratcheted per [R-ENF-02]: an id already cited in code before this check existed
# is allowed to fail while its rule is written up, and the list may only SHORTEN.
ORPHAN_FILE = os.path.join(ROOT, 'engine', 'build_depth_audit',
                           'rule_id_outstanding.json')


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
REV_ANY = re.compile(r'(?:DIGEST|PROTOCOL) REVISION (\d{4}-\d{2}-\d{2}[a-z]?)\b')


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


def extra_stamps(path):
    """Every stamp in the document BEYOND the one it opens with.  [R-DOC-01]

    A DOCUMENT THAT STATES TWO REVISIONS STATES NONE, which is the same defect as the
    rule stating two limits, and this gate could not see it: the digest is a SINGLE
    LINE, so readline() returns the whole document and the opening match is satisfied
    by the first stamp however many follow it.

    Found 07-09-2026, on this gate's own output being green. A union merge of the
    single-line digest kept both sides' opening sentences, so the file carried
    "DIGEST REVISION 2026-09-06c ... DIGEST REVISION 2026-09-06b ..." and every check
    in the repository read the first one and passed. The stamp exists so a pasted copy
    can declare its own age; a copy carrying two ages declares neither, and the reader
    it was written for is the one person who cannot run this gate.

    Shape-matched rather than word-listed, and safe for the same reason rule ids and
    repository paths are: "DIGEST REVISION" followed by an ISO date is not a phrase
    that occurs innocently in prose written for anyone.
    """
    txt = open(path, encoding='utf-8').read()
    hits = list(REV_ANY.finditer(txt))
    return [(m.group(1), m.start()) for m in hits[1:]]


# A PASSAGE THIS LONG DOES NOT RECUR BY ACCIDENT, AND THE THREE THAT DO ARE NAMED.
# The window is 300 characters because that is roughly two sentences of this prose:
# short enough to catch a spliced rule header (the shortest real one measured 106
# chars of overlap) and long enough that ordinary house phrasing -- "READ THE
# POPULATION LIVE", "THE GENERAL LESSON, WHICH IS NOT ABOUT" -- cannot reach it,
# since those diverge within a clause. Measured on the repaired file: the whole
# document carries exactly three repeats at 100 chars and NONE at 300.
DUP_WINDOW = 300

# Deliberate restatements, each a rule quoting another ON PURPOSE. Named with the
# reason rather than tolerated by a length cutoff, because an allowance nobody has
# to justify is where the next splice hides.
DUP_ALLOWED = {
    "that is the evidence to revisit this clause": (
        "[R-GAP-02 AMENDED] and [R-MERGE-01] both state their own falsifier in the "
        "same words, deliberately: each records the evidence that would reopen it."),
    "a stale base year, an over-charged discount rate": (
        "[R-GAP-01] and [R-GAP-02 AMENDED] both list the DCF errors that run one way; "
        "the second rule's asymmetry is that list, so it restates it rather than "
        "pointing at it."),
    "the higher a market's inflation the more brutal the charge": (
        "[R-TERM-01 CLAUSE TWO] QUOTES the sentence it is correcting, which is the "
        "point of the clause."),
}


def duplicated_passages(path, window=DUP_WINDOW):
    """Maximal passages appearing twice in one document.  [R-DOC-01]

    A MERGE CAN SATISFY EVERY CHECK AND STILL PRODUCE A DOCUMENT NEITHER SIDE WROTE.
    The 06-09-2026 union merge of the single-line digest duplicated the revision
    stamp -- closed by extra_stamps() above -- and, found the day after, spliced
    FIVE fragments into the body: a rule header repeated with a neighbouring rule's
    sentence between the copies, a general lesson inserted into a different rule,
    and a sentence left cut off mid-clause. 2,035 characters, every one of them
    text that belonged somewhere else in the same file, and nothing could see it.

    The full protocol took NO damage from the same merge, which is the whole
    finding: it has line breaks, so git resolved it hunk by hunk. A single-line
    file has no merge granularity, so the resolution is a splice and the splice is
    invisible to a reader and to a diff alike.

    Arithmetic about the file, not a word list: identical text is identical text.
    """
    s = open(path, encoding='utf-8').read()
    seen, hits = {}, []
    for i in range(len(s) - window + 1):
        w = s[i:i + window]
        if w in seen:
            hits.append((seen[w], i))
        else:
            seen[w] = i
    regions = []
    for a, b in hits:
        if regions and a == regions[-1][0] + regions[-1][2] and b == regions[-1][1] + regions[-1][2]:
            regions[-1][2] += 1
        else:
            regions.append([a, b, 1])
    out = []
    for a, b, n in regions:
        text = s[b:b + n + window - 1]
        if any(k in text for k in DUP_ALLOWED):
            continue
        out.append((a, b, n + window - 1, text[:90]))
    return out


def amendment_days(root=ROOT, paths=None):
    """The day(s) the governing documents were last amended, as a witness OUTSIDE them.

    [R-DOC-01 AMENDED 07-09-2026] THE STAMP NAMES THE DAY THE DOCUMENT WAS ACTUALLY
    AMENDED, AND NOTHING HAD EVER ASKED WHEN THAT WAS. The rule says the digest is
    named for the day of its LATEST AMENDMENT so the filename and the stamp "agree on
    their face". A first draft of this check compared those two to each other and
    PASSED — of course it did: both are typed by the same hand in the same edit and
    they had never disagreed. On 07-09-2026 three amendments landed at 00:45, 01:02
    and 01:25 UTC carrying 2026-09-06d, e and f under a filename dated 06-09-2026,
    every one internally consistent and every one naming a day the edits were not made
    on. TWO FIELDS THAT AGREE WITH EACH OTHER AND NOT WITH THE WORLD IS THE
    SELF-ATTESTATION SHAPE [R-ENF-01] CLOSES EVERYWHERE ELSE, and the only witness
    outside the document is when it was committed.

    THE ZONE IS AMBIGUOUS AND THE AMBIGUITY IS ADMITTED RATHER THAN RESOLVED BY
    PICKING ONE. The project's clock is Africa/Cairo and CI runs in UTC, so a commit
    between 21:00 and midnight UTC falls on two different days depending on which is
    meant, and choosing one here would be a free parameter the PROMOTION RULE forbids.
    Both readings are returned; what the caller refuses is a stamp matching NEITHER.

    Returns (days, when) or raises RuntimeError — an unanswerable check is not a
    clean one [R-ENF-04].
    """
    paths = list(paths or (DIGEST, FULL))
    log = subprocess.run(['git', 'log', '-1', '--format=%at', '--'] + paths,
                         cwd=root, capture_output=True, text=True)
    if log.returncode != 0:
        raise RuntimeError('git could not say when the governing documents were last '
                           'amended: %s' % log.stderr.strip()[:140])
    dirty = subprocess.run(['git', 'status', '--porcelain', '--'] + paths,
                           cwd=root, capture_output=True, text=True)
    if dirty.returncode == 0 and dirty.stdout.strip():
        base = _dt.datetime.now(_dt.timezone.utc)
        when = 'the working tree (amended, not yet committed)'
    else:
        ts = log.stdout.strip()
        if not ts.isdigit():
            raise RuntimeError('no commit was found touching the governing documents, '
                               'so the stamp cannot be checked against when they were '
                               'amended. On a shallow clone, fetch full depth.')
        base = _dt.datetime.fromtimestamp(int(ts), _dt.timezone.utc)
        when = 'the last commit touching them'
    days = sorted({base.date().isoformat(),
                   (base + _dt.timedelta(hours=3)).date().isoformat()})
    return days, when


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
    try:
        allowed, when = amendment_days()
    except RuntimeError as exc:
        print('FAIL — %s An unanswerable check is not a clean one [R-ENF-04].' % exc)
        return 1
    if rd[:10] not in allowed:
        print('FAIL — the documents are stamped %s and %s says they were amended on '
              '%s (UTC or Africa/Cairo). [R-DOC-01] requires the stamp to name the '
              'day of the amendment, the digest to be RENAMED to that day in the '
              'SAME COMMIT as the first edit of it, the revision letters to restart '
              'at "a", and the include line at the top of CLAUDE.md to move with the '
              'rename — so a copy pasted into somebody else\'s project files declares '
              'its own age on its face.' % (rd, when, ' or '.join(allowed)))
        return 1
    fname = os.path.basename(DIGEST)
    m_fn = re.search(r'PROJECT_INSTRUCTIONS_(\d{2})-(\d{2})-(\d{4})\.md$', fname)
    if not m_fn:
        print('FAIL — the digest filename %r carries no DD-MM-YYYY date, so the rule '
              'that it names its own amendment day cannot be checked [R-ENF-04].'
              % fname)
        return 1
    fn_date = '%s-%s-%s' % (m_fn.group(3), m_fn.group(2), m_fn.group(1))
    if rd[:10] != fn_date:
        print('FAIL — the digest is named for %s and stamped %s. Rename engine/%s to '
              'engine/PROJECT_INSTRUCTIONS_%s-%s-%s.md and move the CLAUDE.md include '
              'line with it, in the same commit.'
              % (fn_date, rd, fname, rd[8:10], rd[5:7], rd[0:4]))
        return 1

    dupes = {os.path.basename(p): extra_stamps(p) for p in (FULL, DIGEST)}
    if any(dupes.values()):
        for name, extra in dupes.items():
            for rev, at in extra:
                print(f'FAIL — {name} carries a SECOND revision stamp ({rev}) at '
                      f'character {at}. A document that states two revisions states '
                      f'none; the stamp exists so a pasted copy can declare its own '
                      f'age. Delete the superseded sentence and bump.')
        return 1
    spliced = {os.path.basename(p): duplicated_passages(p) for p in (FULL, DIGEST)}
    if any(spliced.values()):
        for name, regions in spliced.items():
            for a, b, n, head in regions:
                print(f'FAIL — {name} repeats {n} characters verbatim, at {a} and {b}. '
                      f'A passage that long does not recur by accident; this is a merge '
                      f'splice. Passage begins: {head!r}')
        print('If a rule genuinely quotes another at this length, name it in '
              'DUP_ALLOWED with its reason — an allowance nobody has to justify is '
              'where the next splice hides.')
        return 1
    print(f'revision stamp: {rf} (both documents agree, one stamp each, no spliced '
          f'passage over {DUP_WINDOW} characters)')
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

    # A THIRD POPULATION, WHICH THIS GATE HAD NEVER LOOKED AT. It compared the two
    # documents to each other and printed, for information, which rules the code
    # enforces — but never asked the reverse question: is there a [R-...] id
    # CITED IN CODE that resolves in neither document? [R-DOC-01] already requires
    # an identifier to appear in the full protocol, in the digest AND in the code
    # that enforces it; two of those three were checked.
    #
    # It was not hypothetical. On 03-Sep-2026 [R-VCAL-01] was cited in eight files
    # — a module docstring, a pre-registration, two gates — and existed in neither
    # governing document, while this check reported the documents in perfect
    # agreement. A rule id that resolves nowhere reads to every later session as
    # settled law, and nothing was looking.
    orphans = {rid: where for rid, where in sorted(code.items())
               if rid not in full and rid not in digest}
    known = set()
    if os.path.exists(ORPHAN_FILE):
        try:
            known = set(json.load(open(ORPHAN_FILE, encoding='utf-8'))
                        .get('outstanding', []))
        except Exception as exc:
            print('FAIL — the orphan ratchet list will not parse (%s)' % exc)
            return 1
    vanished = sorted(known - set(orphans))
    new_orphans = {r: w for r, w in orphans.items() if r not in known}

    if orphans:
        print('\nrule ids cited in code and present in NEITHER document: %d '
              '(%d allowed on the ratchet)'
              % (len(orphans), len(orphans) - len(new_orphans)))
        for rid, where in orphans.items():
            print('   %-14s %s%s' % (rid, ', '.join(sorted(set(where))[:3]),
                                     '   [outstanding]' if rid in known else ''))
    if vanished:
        print('\nFAIL — the ratchet lists %s, which is cited nowhere in code. The '
              'list may only ever SHORTEN, and an entry that no longer resolves is '
              'not a shortening, it is a stale list. Prune it.' % ', '.join(vanished))
        return 1
    if new_orphans:
        print('\nFAIL — a rule id is cited in code and defined in neither governing '
              'document: %s. Adopt it in BOTH documents in one commit, or stop '
              'citing an identifier that resolves nowhere — to a later session an '
              'unresolvable [R-...] reads exactly like settled law.'
              % ', '.join(sorted(new_orphans)))
        return 1

    if orphans:
        # Say what is actually true. "Every id resolves" would be false while two
        # sit on the ratchet, and a green line that overstates itself is how a
        # ratchet quietly becomes a permanent exemption.
        print('\nOK — the two governing documents carry the same tagged rules. %d '
              'id(s) still resolve nowhere and are allowed on the ratchet; the '
              'list may only shorten.' % len(orphans))
    else:
        print('\nOK — the two governing documents carry the same tagged rules, and '
              'every rule id cited in code resolves.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
