#!/usr/bin/env python3
"""The delivered STUDY DOCUMENT must carry the model report's sections.  [R-ENF-01]

WHY THIS EXISTS
    On 1 September 2026 [R-ENF-02] was amended because one of assert_model_study()'s nine
    self-attested fields turned out to be measurable from outside: AMOC attested
    structure_matches_model=True while its delivered WORKBOOK carried seven sheets against
    the model report's sixteen. scripts/check_workbook_structure.py closed that half by
    reading the sheet list off the delivered .xlsx.

    The OTHER half of the same attestation was left self-certified, and on 3 September 2026
    three outside audits found exactly what that predicts, in three different studies:

        AMOC   Appendix C has C.1-C.3 and then stops — no cross-examination (C.4), no
               three-in-one-room (C.5), no divergence table (C.6). Depth-bar standard 7
               requires all three by name.
        ARCC   no Company overview, no About this series, no Disclosure — three top-level
               sections of the sixteen simply absent — and the same C.4/C.5/C.6 gap.

    Both studies attested structure_matches_model=True. Neither was lying: nobody had
    counted. That is the composite-beta lesson for the third time in one costume or
    another, and per [R-ENF-01] the fix closes the CLASS rather than patching the two
    documents: the section list is read off the delivered .docx by a job that runs over
    every study directory from outside.

WHAT THE STANDARD IS, AND WHERE IT IS READ FROM
    CLAUDE.md says of the model report: "open it beside the study you are writing. Every
    study matches its sections list." So this gate reads the required sections OUT OF THE
    MODEL REPORT DOCUMENT — engine/model_report/MODEL_REPORT_09-08-2026.docx, resolved
    through research_protocol.MODEL_STUDY, never a list typed here. A check that carries
    its own copy of the standard stops testing the standard the moment one of them moves.

    What is compared is the SECTION MARKER, not the prose: '1.4', 'Appendix C', 'C.5',
    'About this series'. A study's headings name its own company and its own crux and must
    be free to — the model report's 1.7 is "what the fleet earns per day" and no other
    company has a fleet. What may not vary is whether the section is there at all.

    The derivation is self-tested: the model report must satisfy the marker set derived
    from it, and that set must agree with the numbering MODEL_STUDY['word_skeleton'] names
    in prose. If the two documents ever disagree the gate refuses rather than picking one.

THE POPULATION IS ANCHORED ELSEWHERE  [R-ENF-04]
    This gate globs engine/*_study, so a bad pattern would find nothing and report clean.
    Every ticker named in document_outstanding.json must resolve to a study directory on
    disk, and a run that examined ZERO documents fails outright. A document that cannot be
    OPENED is a failure, never a skip: an unreadable document is not a clean one.

THE RATCHET  [R-ENF-02]
    Studies already off the standard on adoption day are listed and allowed to fail. The
    build breaks on a NEW mismatch or a study directory with no entry either way. The list
    may only ever get SHORTER — --prune rewrites it.

USAGE
    python3 scripts/check_document_structure.py          # gate; exit 1 on any hard fail
    python3 scripts/check_document_structure.py --prune  # drop the now-passing entries
    python3 scripts/check_document_structure.py --show TK   # what one document carries
"""
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENGINE = os.path.join(ROOT, 'engine')
OUTSTANDING = os.path.join(ENGINE, 'build_depth_audit', 'document_outstanding.json')
sys.path.insert(0, ENGINE)
import research_protocol as RP                                          # noqa: E402

MODEL_DOC = os.path.join(ROOT, RP.MODEL_STUDY['model_report_document'])

# A marker is what a section is CALLED in the skeleton, stripped of the company's own
# prose. Anything not matching one of these shapes is body text or a sub-heading a study
# is free to invent.
# The number may carry a trailing period ('1. Fundamental valuation') and the About
# section may be 'About this series' or 'About this study'. Both are house rendering
# conventions, not different sections, and the first draft of this gate reported eight
# studies as missing sections they plainly carry. A check firing on work that is right is
# re-pointed at what it meant to measure, never widened and never ignored [R-COC-01]:
# what the standard names is the SECTION, and a section is not absent because its title
# ends in a different noun.
_MARKER_RX = re.compile(
    r'^(?:'
    r'(?P<num>\d(?:\.\d)?)\.?\s|'                    # 1 , 1. , 1.4
    r'(?P<app>Appendix\s+[ABC])\b|'                  # Appendix A , Appendix A —
    r'(?P<sub>[ABC]\.\d)\.?\s|'                       # A.2 , C.5
    # Measured across the whole book, EVERY heading beginning with 'About' is this one
    # section, under three renderings — 'About', 'About this series', 'About this
    # study'. So the marker is the word, not a list of spellings: a list would need
    # extending the first time a study wrote a fourth, and a section is not absent
    # because its title ends in a different noun.
    r'(?P<about>About)\b|'
    r'(?P<named>Headline|Valuation summary|Company overview|Disclosure)\b'
    r')', re.I)


def markers(texts):
    """The ordered, de-duplicated section markers a document carries."""
    out = []
    for t in texts:
        m = _MARKER_RX.match(t)
        if not m:
            continue
        k = (m.group('num') or m.group('app') or m.group('sub')
             or ('About this series' if m.group('about') else None) or m.group('named'))
        k = re.sub(r'\s+', ' ', k).strip()
        k = k[:1].upper() + k[1:] if k[:1].isalpha() else k
        # 'Disclosure & Disclaimer' / 'Disclosure and disclaimer' are one section.
        if k.lower().startswith('disclosure'):
            k = 'Disclosure'
        if k not in out:
            out.append(k)
    return out


class Unreadable(Exception):
    """The document opened and yielded no headings at all."""


def headings(path):
    """The document's headings, under EITHER convention this book uses.

    Two are in play and both are legitimate: the model report and the older builders style
    headings as bold runs at heading size, while docx_phdc.py and the TMGH builder use
    Word's real Heading styles. A reader cannot tell them apart and neither should this.

    The first draft read only bold runs, and PHDC and TMGH came back with ZERO headings —
    which it then reported as 'missing all 36 sections', a confident wrong answer about two
    of the most complete documents in the repository. That is [R-ENF-04] inside a gate
    written to enforce it: an empty probe reads exactly like a catastrophic failure, and
    the two must never be reported as the same thing. An empty extraction now RAISES.
    """
    import docx
    d = docx.Document(path)
    out = []
    for p in d.paragraphs:
        t = p.text.strip()
        if not t:
            continue
        if (p.style.name or '').startswith('Heading'):
            out.append(re.sub(r'\s+', ' ', t))
            continue
        if not p.runs:
            continue
        r = p.runs[0]
        sz = r.font.size.pt if r.font.size else None
        if r.bold and (sz is None or sz >= 11.5):
            out.append(re.sub(r'\s+', ' ', t))
    if not out:
        raise Unreadable(
            'the document opened but yielded no headings under either convention '
            '(Word Heading styles, or bold runs at 11.5pt or larger). This gate cannot '
            'tell a document with no sections from a document it cannot read, so it '
            'refuses rather than reporting every section missing.')
    return out


def latest_study_doc(sdir):
    """The study document that would be published: newest by the DD-MM-YYYY in its name.

    Superseded editions sit beside the current one and a lexical sort on DDMMYYYY picks the
    wrong file — that defect has now been paid for twice in this repository (L-067), so the
    date is parsed. Bibliographies, source registers and QC gates are not the study.
    """
    cands = []
    for p in glob.glob(os.path.join(sdir, '*.docx')):
        b = os.path.basename(p)
        if b.startswith('~$'):
            continue
        if not re.search(r'valuation[_ ]study', b, re.I):
            continue
        m = re.findall(r'(\d{2})-(\d{2})-(\d{4})', b)
        key = (m[-1][2] + m[-1][1] + m[-1][0]) if m else ''
        cands.append((key, b, p))
    if not cands:
        return None
    return sorted(cands)[-1][2]


def required():
    """The marker set the model report itself carries, cross-checked against the numbering
    MODEL_STUDY['word_skeleton'] names. Two records of one standard: if they disagree this
    refuses rather than choosing, because choosing would silently make one of them the
    standard and nothing would say which."""
    want = markers(headings(MODEL_DOC))
    skel = ' | '.join(RP.MODEL_STUDY['word_skeleton'])
    named = set(markers(list(RP.MODEL_STUDY['word_skeleton'])))
    # The skeleton writes runs as ranges for a human to read — 'C.1-C.3 Expert 1/2/3',
    # '1.1 ... 1.9'. Expanding them here is not the gate being lenient: a range names its
    # members, and forcing the prose into a flat list to satisfy a literal probe would make
    # the document worse to read in order to make the checker simpler to write.
    for a, b in re.findall(r'\b([A-C]\.\d|\d\.\d)\s*[-\u2013]\s*([A-C]?\.?\d(?:\.\d)?)\b', skel):
        pre = a.split('.')[0]
        lo, hi = int(a.split('.')[1]), int(b.split('.')[-1])
        for i in range(lo, hi + 1):
            named.add('%s.%d' % (pre, i))
    for k in want:
        # every marker the model report carries must be traceable in the skeleton prose
        if k in named:
            continue
        probe = (r'\b%s\b' % re.escape(k)) if not k[0].isdigit() else (r'(?<![\d.])%s\b' % re.escape(k))
        if not re.search(probe, skel, re.I):
            raise SystemExit(
                'REFUSING — the model report carries section %r and MODEL_STUDY'
                "['word_skeleton'] does not name it. Two records of one standard "
                'disagree; fix them together rather than letting this gate pick one.' % k)
    return want


def examine(sdir, want):
    tk = os.path.basename(sdir)[:-len('_study')].upper()
    p = latest_study_doc(sdir)
    if p is None:
        return tk, 'no valuation study document in the directory', None, []
    try:
        got = markers(headings(p))
    except Unreadable as e:
        return tk, 'headings unreadable — %s' % e, p, []
    except Exception as e:                                              # noqa: BLE001
        return tk, ('document could not be read (%s: %s). An unreadable document is not a '
                    'clean one.' % (type(e).__name__, e)), p, []
    missing = [k for k in want if k not in got]
    if missing:
        return tk, 'missing %d section(s): %s' % (len(missing), ', '.join(missing)), p, got
    order = [k for k in got if k in want]
    if order != want:
        first = next((a for a, b in zip(order, want) if a != b), order[len(want):][:1])
        return tk, 'all sections present but out of the model order (at %r)' % first, p, got
    return tk, 'ok', p, got


def main(argv):
    want = required()

    if '--show' in argv:
        tk = argv[argv.index('--show') + 1].lower()
        sdir = os.path.join(ENGINE, '%s_study' % tk)
        _, status, path, got = examine(sdir, want)
        print(os.path.basename(path) if path else '(no document)')
        print('status:', status)
        print('carries:', ', '.join(got) or 'nothing')
        print('wanted :', ', '.join(want))
        return 0

    dirs = sorted(glob.glob(os.path.join(ENGINE, '*_study')))
    if not dirs:
        print('FAIL — examined zero study directories. An empty result is not a clean '
              'result [R-ENF-04].')
        return 1
    known = {}
    if os.path.exists(OUTSTANDING):
        known = json.load(open(OUTSTANDING, encoding='utf-8')).get('entries', {})
    on_disk = {os.path.basename(d)[:-len('_study')].upper() for d in dirs}
    stranded = sorted(set(known) - on_disk)

    prune = '--prune' in argv
    results = [examine(d, want) for d in dirs]
    print('MODEL-REPORT SECTION LIST — %d sections, read off %s'
          % (len(want), os.path.basename(MODEL_DOC)))
    print('   ' + ', '.join(want))
    print('examined %d study directories\n' % len(results))

    ok, breaches = [], []
    for tk, status, path, _ in results:
        (ok if status == 'ok' else breaches).append(
            tk if status == 'ok' else (tk, status, path))

    print('MATCHES THE MODEL REPORT (%d): %s' % (len(ok), ', '.join(ok) or 'none'))
    if breaches:
        print('\nOFF THE STANDARD (%d):' % len(breaches))
        for tk, status, path in breaches:
            print('   %-12s %s' % (tk, status))

    now_passing = sorted(set(known) & set(ok))
    if now_passing:
        print('\nNOW PASSING — remove from the list (%d): %s'
              % (len(now_passing), ', '.join(now_passing)))

    if prune:
        keep = {k: v for k, v in known.items() if k not in now_passing and k in on_disk}
        for tk, status, _ in breaches:
            keep.setdefault(tk, status)
        json.dump({'note': ('Studies whose delivered study document was already off the '
                            'model-report section list when this gate was adopted '
                            '(03-Sep-2026). Allowed to fail; the list may only ever get '
                            'shorter. --prune rewrites it.'),
                   'entries': keep},
                  open(OUTSTANDING, 'w', encoding='utf-8'), indent=1, sort_keys=True)
        open(OUTSTANDING, 'a', encoding='utf-8').write('\n')
        print('\npruned; %d entry/entries remain' % len(keep))
        return 0

    bad = 0
    if stranded:
        print('\nFAIL — %d listed study/studies no longer resolve on disk: %s'
              % (len(stranded), ', '.join(stranded)))
        bad += 1
    unlisted = [(tk, st) for tk, st, _ in breaches if tk not in known]
    if unlisted:
        print('\nFAIL — %d new violation(s):' % len(unlisted))
        for tk, st in unlisted:
            print('   %s: %s' % (tk, st))
        print('\nA section a reader never sees is a section that was not written. Build it, '
              'or amend the model report — but do not attest structure_matches_model on a '
              'document that does not carry it.')
        bad += 1
    if not bad:
        print('\nOK — no new violations.')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
