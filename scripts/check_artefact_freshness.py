#!/usr/bin/env python3
"""A DELIVERED ARTEFACT MAY NOT BE OLDER THAN THE NUMBERS IT PUBLISHES.

WHY THIS EXISTS
---------------
On 13-09-2026 six studies were audited from outside, one agent per study, roughly half an
hour each. Six came back NOT DELIVERABLE, and the single largest defect class in every one
of them was the same thing: an artefact that was not rebuilt when the numbers moved.

    AMOC   four of five figures publish EGP 11.40 while every table publishes 20.05.
           Figure 4 shows every bar BELOW the spot line under a caption reading "Every
           concession moves the answer further above the price."
    ARCC   four figures rendered against a central of 66.53 beside a summary table
           reading 77.18; the workbook PDF prints 77.49 and a cost of capital of 27.60%
           against the .xlsx's 77.18 and 27.96%.
    SCEM   nine figures built when the central was 111.62; the study now publishes
           122.67, and Figure 1's own label reads "base 111.6" beside it.
    TMGH   the workbook PDF is three days older than the workbook and publishes a cost of
           equity the edition had already retired.

None of that is subtle and none of it needed judgement. Every one was found by a reader
opening the delivered PDF and looking, because NOTHING IN THIS REPOSITORY COMPARED A
DELIVERED ARTEFACT AGAINST THE NUMBERS FILE IT DERIVES FROM. check_data_freshness.py
covers assets/data.js and nothing else; the figure gates check pixels and axes, not
content; check_delivered_pdf_currency.py filters on `Valuation_Study` in the filename, so
it never opens a workbook PDF or a figure at all.

The second cause is the same one: 23 of 25 studies have no single build entry point, so
reissuing a study is a remembered sequence of six or seven commands and whatever step is
forgotten ships stale, silently, with every other gate green.

WHAT IT CHECKS, IN TWO TIERS
----------------------------
TIER A, and it fails outright: A RENDERED FILE MAY NOT BE OLDER THAN THE FILE IT WAS
RENDERED FROM. A .pdf beside the .docx or .xlsx of the same name is a render of it, and a
render that predates its own source is stale with no judgement required and no honest
reading in which it is not. This is ARCC's workbook PDF printing 77.49 against its
spreadsheet's 77.18, and TMGH's printing a cost of equity the edition had retired.

TIER B, and it is ratcheted: A FIGURE MAY NOT BE OLDER THAN THE NUMBERS FILE. A .png in a
study directory is drawn from the numbers, so a figure committed before the numbers moved
is drawing the old ones. This is AMOC's four-of-five at 11.40, ARCC's four at 66.53 and
SCEM's nine at 111.62.

WHAT IT DELIBERATELY DOES NOT DO. It does not hold a .docx or .xlsx against the numbers
file. That test over-fires: a record added to the numbers file that no document prints --
a bridge record, a lens record, a standard stamp -- moves the numbers file without making
any document wrong, and a gate that cries stale on every record-only edit would be
ignored inside a week. Documents are covered on CONTENT by check_prose_figures and
check_delivered_pdf_currency; this gate covers what those two cannot see.

WHY COMMIT TIME AND NOT FILE MTIME. mtime is set by checkout, so on a fresh clone every
file in the repository is the same age and the test would pass vacuously -- an empty
result wearing a clean one's clothes [R-ENF-04]. Commit time is a property of the history
and survives a clone. A study whose numbers file is UNCOMMITTED is reported as unknown
rather than passed, for the same reason.

Ratcheted [R-ENF-02]: the list is seeded once, at creation, with what is already stale,
and may only ever SHORTEN. Population-anchored [R-ENF-04]: zero studies examined FAILS.

    python3 scripts/check_artefact_freshness.py
    python3 scripts/check_artefact_freshness.py --seed    (once, at creation)
"""
import glob
import hashlib
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENGINE = os.path.join(ROOT, 'engine')
OUTSTANDING = os.path.join(ENGINE, 'build_depth_audit', 'artefact_freshness_outstanding.json')

# what a reader actually receives, and the figures those documents embed
ARTEFACT_GLOBS = ('*Valuation_Study*.docx', '*Valuation_Study*.pdf',
                  '*Valuation_Model*.xlsx', '*Valuation_Model*.pdf',
                  '*Bibliography*.docx', '*Bibliography*.pdf',
                  '*Sources*.docx', '*Sources*.pdf',
                  '*.png')
NUMBERS = ('study_numbers.json', 'numbers.json')


def build_manifest(sdir):
    """What the study's last FULL build recorded, if it still describes this tree.

    COMMIT TIME ANSWERS THE WRONG QUESTION for a deterministic artefact. A figure that
    regenerates byte-identically is never re-committed, so git keeps its old commit and
    this gate reads a figure produced seconds ago as fourteen thousand minutes stale.
    ARCC came out of a full rebuild with five such figures reported behind their own
    numbers file. A check firing on work that is right has found a construction nobody
    wrote down [R-COC-01], and the construction is the build itself: engine/
    build_all_shared.py records the numbers file it built from and the digest of every
    artefact beside it, and an artefact whose digest still matches, against a numbers
    file whose digest still matches, WAS produced from these numbers.

    THE MANIFEST CANNOT EXCUSE A CHANGED FILE. Both digests are checked against the
    tree as it stands, so editing either one drops the artefact straight back to the
    commit-time test. It is evidence, not a flag.
    """
    p_ = os.path.join(sdir, 'build_manifest.json')
    nf = os.path.join(sdir, 'study_numbers.json')
    if not (os.path.exists(p_) and os.path.exists(nf)):
        return {}
    try:
        man = json.load(open(p_, encoding='utf-8'))
    except Exception:                                                   # noqa: BLE001
        return {}
    if man.get('numbers_sha256') != _sha(nf):
        return {}
    return man.get('artefacts') or {}


def _sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b''):
            h.update(chunk)
    return h.hexdigest()


def commit_time(path):
    """Unix time of the last commit touching `path`, or None if never committed."""
    rel = os.path.relpath(path, ROOT)
    try:
        out = subprocess.run(['git', 'log', '-1', '--format=%ct', '--', rel],
                             cwd=ROOT, capture_output=True, text=True, timeout=30)
    except Exception:                                                # noqa: BLE001
        return None
    s = (out.stdout or '').strip()
    return int(s) if s.isdigit() else None


def dirty(path):
    rel = os.path.relpath(path, ROOT)
    out = subprocess.run(['git', 'status', '--porcelain', '--', rel],
                         cwd=ROOT, capture_output=True, text=True, timeout=30)
    return bool((out.stdout or '').strip())


def numbers_file(sdir):
    for n in NUMBERS:
        p = os.path.join(sdir, n)
        if os.path.exists(p):
            return p
    # A STUDY MAY NAME ITS NUMBERS FILE AFTER ITSELF. XPT writes study_numbers_xpt.json,
    # so this returned None and the gate reported the whole study UNKNOWN -- which is the
    # right verdict for a study whose numbers cannot be found and the wrong one for a
    # study whose numbers are sitting there under a slightly different name. Reported as
    # unknown only when nothing of the shape exists.
    import glob as _glob
    found = sorted(_glob.glob(os.path.join(sdir, 'study_numbers*.json')))
    return found[0] if found else None


def current_edition_artefacts(sdir):
    """Only the CURRENT edition's artefacts. A superseded document is a record of what was
    delivered then; holding it to today's numbers would demand it be rewritten, which is
    the permanently-red check [R-ENF-02] forbids.

    The edition is resolved from edition.py where the study has one, and otherwise from the
    newest date stamped into a delivered filename -- never from mtime, for the reason in
    the header.
    """
    import re
    # A STUDY MAY NOT HOLD ITS OWN DELIVERED FILES. XPT's builders write to the working
    # directory and its published study, workbook and PDF live in files/, which is where
    # a reader gets them -- so this reported "no delivered artefact of the current edition
    # found" for a study with three of them. Searched there too, by ticker prefix, exactly
    # as the workbook formula-target gate resolves the same case.
    tk = os.path.basename(sdir)[:-len('_study')].lower()
    roots = [sdir]
    if not glob.glob(os.path.join(sdir, '*Valuation_Study*')) \
            and not glob.glob(os.path.join(sdir, '*Valuation_Model*')):
        pub = os.path.join(os.path.dirname(ENGINE), 'files')
        if os.path.isdir(pub):
            roots.append(pub)

    def _in_roots(pattern):
        hits = []
        for root in roots:
            for f in glob.glob(os.path.join(root, pattern)):
                if root is sdir or os.path.basename(f).lower().startswith(tk):
                    hits.append(f)
        return hits

    stamps = set()
    for pat in ('*Valuation_Study*', '*Valuation_Model*'):
        for f in _in_roots(pat):
            m = re.search(r'(\d{2})-(\d{2})-(\d{4})', os.path.basename(f))
            if m:
                stamps.add('%s-%s-%s' % m.groups())
                continue
            m = re.search(r'(\d{2})(\d{2})(\d{4})', os.path.basename(f))
            if m:
                stamps.add('%s-%s-%s' % m.groups())
    def key(s):
        d, mo, y = s.split('-')
        return (y, mo, d)
    latest = max(stamps, key=key) if stamps else None
    d, mo, y = (latest.split('-') if latest else ('', '', ''))
    compact = '%s%s%s' % (d, mo, y)

    out = []
    for pat in ARTEFACT_GLOBS:
        for f in sorted(_in_roots(pat)):
            b = os.path.basename(f)
            if b.startswith('~$'):
                continue
            if pat == '*.png':
                out.append(f)                      # figures carry no edition in the name
            elif latest and (latest in b or compact in b):
                out.append(f)
    return out, latest


def main():
    seed = '--seed' in sys.argv
    sdirs = sorted(glob.glob(os.path.join(ENGINE, '*_study')))
    if not sdirs:
        print('FAIL — zero study directories examined. An empty result is not a clean '
              'result [R-ENF-04].')
        return 1

    held, held_a = {}, {}
    if os.path.exists(OUTSTANDING):
        _o = json.load(open(OUTSTANDING, encoding='utf-8'))
        held = _o.get('stale', {})
        # TIER A CARRIES A RATCHET TOO, and it is a SEPARATE list from Tier B's.
        #
        # A render older than its own source is the harder failure and it stays hard for
        # anything not recorded here. What this list holds is the debt that existed when
        # the gate was first RUN in CI: eight studies outside the recalibration set whose
        # PDFs predate their documents, several by weeks. Without it the gate could not
        # enter a workflow at all, and a gate in no workflow is the state this one spent
        # its first day in -- written, correct, and running nowhere.
        #
        # The two lists are not interchangeable: an entry excusing a stale PDF must not
        # excuse a stale figure or the reverse. Both may only ever SHORTEN.
        held_a = _o.get('stale_renders', {})

    stale, unknown, clean, examined = {}, [], 0, 0
    for sdir in sdirs:
        tk = os.path.basename(sdir)[:-len('_study')].upper()
        nf = numbers_file(sdir)
        if nf is None:
            unknown.append((tk, 'no committed numbers file in the study directory'))
            continue
        nt = commit_time(nf)
        if nt is None:
            unknown.append((tk, 'the numbers file has never been committed, so nothing '
                                'can be dated against it'))
            continue
        if dirty(nf):
            unknown.append((tk, 'the numbers file has uncommitted changes, so whether the '
                                'artefacts match it is unknown rather than clean'))
            continue
        arts, edition = current_edition_artefacts(sdir)
        if not arts:
            unknown.append((tk, 'no delivered artefact of the current edition found'))
            continue
        examined += 1
        behind = []
        produced = build_manifest(sdir)

        # TIER A — a render against the file it was rendered from.
        by_stem = {}
        for a in arts:
            stem, ext = os.path.splitext(os.path.basename(a))
            by_stem.setdefault(stem, {})[ext.lower()] = a
        for stem, exts in sorted(by_stem.items()):
            pdf = exts.get('.pdf')
            src = exts.get('.docx') or exts.get('.xlsx')
            if not pdf or not src:
                continue
            pt, st = commit_time(pdf), commit_time(src)
            if pt is None:
                behind.append((os.path.basename(pdf), 'never committed', 'A'))
            elif st is not None and pt < st:
                behind.append((os.path.basename(pdf),
                               'rendered from %s and committed %d min BEFORE it'
                               % (os.path.basename(src), (st - pt) // 60), 'A'))

        # TIER B — a figure against the numbers it draws.
        for a in arts:
            if not a.lower().endswith('.png'):
                continue
            base = os.path.basename(a)
            # PRODUCED BY THE LAST FULL BUILD, FROM THESE NUMBERS, and still byte-for-byte
            # what that build wrote. Its commit time is then a fact about git and not
            # about the artefact.
            if produced.get(base) == _sha(a):
                continue
            at = commit_time(a)
            if at is None:
                behind.append((base, 'never committed', 'B'))
            elif at < nt:
                behind.append((base, 'committed %d min before the numbers file'
                               % ((nt - at) // 60), 'B'))

        if behind:
            stale[tk] = behind
        else:
            clean += 1

    if seed:
        os.makedirs(os.path.dirname(OUTSTANDING), exist_ok=True)
        json.dump({'_': 'Seeded once, at this gate\'s creation, with every artefact already '
                        'behind its own numbers file. This list may only ever SHORTEN: an '
                        'entry leaves when the study is rebuilt whole. Nothing may be added.',
                   'seeded': '2026-09-13',
                   'stale': {k: sorted({b[0] for b in v if b[2] == 'B'})
                             for k, v in stale.items()
                             if any(b[2] == 'B' for b in v)},
                   'stale_renders': {k: sorted({b[0] for b in v if b[2] == 'A'})
                                     for k, v in stale.items()
                                     if any(b[2] == 'A' for b in v)}},
                  open(OUTSTANDING, 'w'), indent=1)
        print('seeded %s with %d study/studies' % (OUTSTANDING, len(stale)))
        return 0

    print('ARTEFACT FRESHNESS — a delivered file may not predate the numbers it publishes')
    print('  study directories examined : %d' % examined)
    print('  every artefact current     : %d' % clean)
    print('  stale                      : %d' % len(stale))
    if unknown:
        print('\nUNKNOWN, and unknown is not clean [R-ENF-04] (%d):' % len(unknown))
        for tk, why in unknown:
            print('   %-12s %s' % (tk, why))

    hard, soft = {}, {}
    for tk, behind in sorted(stale.items()):
        allowed = set(held.get(tk, []))
        allowed_a = set(held_a.get(tk, []))
        a_rows = [b for b in behind if b[2] == 'A' and b[0] not in allowed_a]
        b_rows = [b for b in behind if b[2] == 'B' and b[0] not in allowed]
        print('\n%s — %d artefact(s) behind their source:' % (tk, len(behind)))
        for name, why, tier in behind:
            held_here = (name in allowed) if tier == 'B' else (name in allowed_a)
            tag = '   [ratcheted]' if held_here else ''
            print('   %s  %-50s %s%s' % (tier, name, why, tag))
        if a_rows:
            hard[tk] = a_rows
        if b_rows:
            soft[tk] = b_rows

    print('\nTIER A breaches (a render older than its own source): %d study/studies'
          % len(hard))
    print('TIER B breaches (a figure older than the numbers), not ratcheted: %d' % len(soft))

    if unknown or hard or soft:
        print('\nFAIL — rebuild the study WHOLE rather than the file that was noticed: '
              'the class this gate exists for is the step somebody forgot, not the file.')
        return 1
    print('\nOK — no rendered file predates its source and no figure predates its numbers.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
