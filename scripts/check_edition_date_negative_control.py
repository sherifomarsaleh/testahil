#!/usr/bin/env python3
"""The edition-date gate must fire on every shape it claims to catch, and on nothing else.

Every failing case is a construction that actually shipped. Every clean case is one that
must NOT fire, including the form that is BETTER than what the rule requires — a masthead
carrying an as-of date and an issue date, which is more honest than carrying one.
"""
import datetime
import json
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GATE = os.path.join('scripts', 'check_edition_date.py')


def write_pdf(path, pages):
    """A minimal PDF of one or more real pages, written by hand.

    THE CONTROL BUILDS ITS OWN PDF RATHER THAN CONVERTING A .docx, and the reason is the
    thing being tested: the clause failed on TEXT SPLIT ACROSS A LINE BREAK and on a study
    whose masthead sits on PAGE TWO behind a cover, so the control has to be able to put a
    break and a page boundary in a chosen place. A converter decides both for itself, and a
    fixture whose condition depends on a converter's layout choice is one that may quietly
    stop injecting its own condition — the failure [R-ENF-04] names, which this control's
    own case 5 has caught once already.

    Pages are a LIST OF LISTS. A cover-page fixture that faked the boundary with a form-feed
    inside the text would test nothing while its comment claimed otherwise, which is worse
    than no fixture: it stops the next reader looking.
    """
    objs, contents = [None, None], []
    for lines in pages:
        txt = ('BT /F1 11 Tf 40 760 Td 14 TL\n'
               + ''.join('(%s) Tj T*\n' % l.replace('\\', '\\\\').replace('(', '\\(')
                         .replace(')', '\\)') for l in lines) + 'ET')
        contents.append(txt)
    font_no = 3 + 2 * len(pages)
    kids = []
    for i, txt in enumerate(contents):
        pno, cno = 3 + 2 * i, 4 + 2 * i
        kids.append('%d 0 R' % pno)
        objs.append('<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] '
                    '/Resources << /Font << /F1 %d 0 R >> >> /Contents %d 0 R >>'
                    % (font_no, cno))
        objs.append('<< /Length %d >>\nstream\n%s\nendstream' % (len(txt), txt))
    objs.append('<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>')
    objs[0] = '<< /Type /Catalog /Pages 2 0 R >>'
    objs[1] = ('<< /Type /Pages /Kids [%s] /Count %d >>' % (' '.join(kids), len(pages)))

    out, offs = b'%PDF-1.4\n', []
    for i, o in enumerate(objs, 1):
        offs.append(len(out))
        out += ('%d 0 obj\n%s\nendobj\n' % (i, o)).encode()
    x = len(out)
    out += ('xref\n0 %d\n0000000000 65535 f \n' % (len(objs) + 1)).encode()
    for o in offs:
        out += ('%010d 00000 n \n' % o).encode()
    out += ('trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n'
            % (len(objs) + 1, x)).encode()
    open(path, 'wb').write(out)


def plant(root, name, paras, with_pdf=True):
    """Plant a delivered study — BOTH artefacts, because that is what a study is.

    THE PDF IS NOT DECORATION ON THIS FIXTURE. The gate anchors its PDF population
    [R-ENF-04], so a fixture planting a lone .docx makes the gate refuse for a reason that
    has nothing to do with the case under test — and every masthead case did exactly that
    when the anchor was added, which is the fixture being unrealistic rather than the
    anchor being wrong. A study in this book ships as a Word file and the PDF converted
    from it, so the fixture ships both, carrying the same paragraphs.
    """
    import docx
    d = docx.Document()
    for p in paras:
        d.add_paragraph(p)
    sd = os.path.join(root, 'engine', '%s_study' % name.split('_')[0].lower())
    os.makedirs(sd, exist_ok=True)
    d.save(os.path.join(sd, name))
    if with_pdf:
        write_pdf(os.path.join(sd, os.path.splitext(name)[0] + '.pdf'), [list(paras)])


def build(tmp, docs, ratchet=None, with_pdf=True):
    os.makedirs(os.path.join(tmp, 'scripts'), exist_ok=True)
    os.makedirs(os.path.join(tmp, 'engine', 'build_depth_audit'), exist_ok=True)
    shutil.copy(os.path.join(ROOT, GATE), os.path.join(tmp, GATE))
    for name, paras in docs.items():
        plant(tmp, name, paras, with_pdf=with_pdf)
    json.dump({'outstanding': ratchet or {}},
              open(os.path.join(tmp, 'engine', 'build_depth_audit',
                                'edition_outstanding.json'), 'w'), indent=1)


def run(tmp):
    r = subprocess.run([sys.executable, GATE], cwd=tmp, capture_output=True, text=True)
    return r.returncode, (r.stdout or '') + (r.stderr or '')


GOOD = ['ZZZ plc', 'Some Exchange · ZZZ · edition of 3 September 2026', 'Headline']
CASES = [
    # ---- the three shapes that shipped -------------------------------------------------
    ('PHDC as it shipped — a 3 Sep edition whose masthead reads 2 September',
     {'ZZZ_Valuation_Study_03-09-2026.docx':
      ['PALM HILLS', 'Egyptian Exchange · ZZZ · edition of 2 September 2026', 'READ FIRST']},
     True, 'masthead states'),
    ('TMGH as it shipped — a 2 Sep edition whose masthead reads 1 September',
     {'ZZZ_Valuation_Study_02-09-2026.docx':
      ['TALAAT MOUSTAFA', 'Egyptian Exchange · ZZZ', 'Valuation study · 1 September 2026']},
     True, 'masthead states'),
    ('SAVOLA as it shipped — the edition date appears NOWHERE in the document',
     {'ZZZ_Valuation_Study_19-08-2026.docx':
      ['Independent Valuation Study', 'Savola Group Company', 'Kingdom of Saudi Arabia']},
     True, 'NOWHERE'),
    ('DU as it shipped — the date is present, buried in the body',
     {'ZZZ_Valuation_Study_09-08-2026.docx':
      ['Independent Valuation Study', 'Emirates Integrated Telecommunications', 'Headline']
      + ['filler'] * 40 + ['the licence runs only to 9 August 2026, one day after this study']},
     True, 'not in the masthead'),
    ('a document that will not open', {}, True, 'zero delivered studies'),
    # ---- and the ones that must NOT fire -----------------------------------------------
    ('CLEAN — the date stated plainly in the masthead',
     {'ZZZ_Valuation_Study_03-09-2026.docx': GOOD}, False, None),
    ('CLEAN — AMOC\'s form, an AS-OF date and an ISSUE date, which is better than the rule '
     'requires and must not be punished for carrying two',
     {'ZZZ_Valuation_Study_03-09-2026.docx':
      ['Alexandria Mineral Oils', 'EGX: ZZZ · Valuation study as of 6 August 2026, '
       'issued 3 September 2026', 'Headline']}, False, None),
    ('CLEAN — a zero-padded rendering, 03 September 2026',
     {'ZZZ_Valuation_Study_03-09-2026.docx':
      ['ZZZ plc', 'edition of 03 September 2026', 'Headline']}, False, None),
    ('CLEAN — an ISO rendering, 2026-09-03',
     {'ZZZ_Valuation_Study_03-09-2026.docx':
      ['ZZZ plc', 'edition of 2026-09-03', 'Headline']}, False, None),
    ('CLEAN — a US rendering, September 3, 2026',
     {'ZZZ_Valuation_Study_03-09-2026.docx':
      ['ZZZ plc', 'edition of September 3, 2026', 'Headline']}, False, None),
]


def main():
    bad = 0
    for name, docs, must_fail, expect in CASES:
        tmp = tempfile.mkdtemp(prefix='nced')
        try:
            build(tmp, docs)
            rc, out = run(tmp)
            ok = ((rc != 0) == must_fail) and (expect is None or expect in out)
            print('%-4s %s' % ('PASS' if ok else 'FAIL', name[:96]))
            if not ok:
                bad += 1
                print('      rc=%d wanted %s%s' % (rc, 'RED' if must_fail else 'GREEN',
                                                   (' containing %r' % expect) if expect else ''))
                print('      ' + '\n      '.join(out.strip().splitlines()[-5:]))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    # the ratchet excuses, and only what it names
    tmp = tempfile.mkdtemp(prefix='nced')
    try:
        build(tmp, {'ZZZ_Valuation_Study_03-09-2026.docx':
                    ['ZZZ', 'edition of 2 September 2026', 'x']},
              {'engine/zzz_study/ZZZ_Valuation_Study_03-09-2026.docx': 'known'})
        rc, out = run(tmp)
        ok = rc == 0 and 'ratcheted' in out
        print('%-4s a ratcheted stale masthead stays GREEN' % ('PASS' if ok else 'FAIL'))
        bad += 0 if ok else 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # a ratchet naming a document that is gone must FAIL
    tmp = tempfile.mkdtemp(prefix='nced')
    try:
        build(tmp, {'ZZZ_Valuation_Study_03-09-2026.docx': GOOD},
              {'engine/vanished_study/GONE_Valuation_Study_01-01-2026.docx': 'x'})
        rc, out = run(tmp)
        ok = rc != 0 and 'no longer exist' in out
        print('%-4s a ratchet naming a vanished document FAILS [R-ENF-04]'
              % ('PASS' if ok else 'FAIL'))
        bad += 0 if ok else 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # ---- THE FIGURE-DATE CLAUSE, on the two constructions that shipped -----------------
    # Both had a COMPUTED price with a TYPED date beside it, in a figure a reader sees, and
    # both disagreed with their own study's committed spot: PHDC by eleven days, EGCH by
    # twenty-eight. BOROUGE types one too and it is RIGHT, which is the clean case — the
    # rule is that the date must be correct, not that a figure may never name one.
    import importlib.util as _u
    _sp = _u.spec_from_file_location('ced', os.path.join(ROOT, GATE))
    _m = _u.module_from_spec(_sp)
    sys.modules['ced'] = _m
    _sp.loader.exec_module(_m)

    for nm, spot, line, must_fire in (
            ("PHDC as it shipped — a figure dating a computed close eleven days early",
             '2026-09-03', 'ax.text(x, y, "close %.2f (23 Aug 2026)" % spot)', True),
            ("EGCH as it shipped — twenty-eight days early",
             '2026-09-03', 'ax.text(a, b, f"6 August 2026 close, EGP {SPOT:,.2f}")', True),
            ("CLEAN — BOROUGE's, which types a date and gets it right",
             '2026-08-07', 'ax.set_xlabel("Trading sessions from 7 August 2026 close")',
             False),
            ("CLEAN — a comment recording a defect that was FIXED is not the defect",
             '2026-09-03', '    # this read "6 August 2026 close" and was wrong', False),
            ("CLEAN — a date in a figure label with no price word beside it",
             '2026-09-03', 'ax.set_title("Five years to 6 August 2026")', False)):
        tmp = tempfile.mkdtemp(prefix='ncedf')
        try:
            sd = os.path.join(tmp, 'engine', 'zzz_study')
            os.makedirs(sd, exist_ok=True)
            open(os.path.join(sd, 'figures.py'), 'w').write(line + '\n')
            json.dump({'spot_date': spot}, open(os.path.join(sd, 'study_numbers.json'), 'w'))
            _m.ROOT = tmp
            ex, offenders = _m.audit_figure_dates()
            fired = bool(offenders)
            ok = (fired == must_fire)
            print('%-4s %s' % ('PASS' if ok else 'FAIL', nm[:96]))
            if not ok:
                print('      examined %d, offenders %s' % (ex, offenders))
                globals()['_extra_bad'] = globals().get('_extra_bad', 0) + 1
        finally:
            _m.ROOT = ROOT
            shutil.rmtree(tmp, ignore_errors=True)
    bad += globals().get('_extra_bad', 0)

    # ---- THE DELIVERED-PDF CLAUSE ------------------------------------------------------
    # THE PDF IS WHAT A READER RECEIVES AND THE .docx IS THE BUILD ARTEFACT. On 03-Sep-2026
    # TMGH's masthead was corrected in the Word file and its delivered PDF sat NINETEEN
    # HOURS behind, still showing the date that had just been fixed — invisible to the
    # masthead clause, which opens the .docx.
    #
    # TWO OF THESE FIVE ARE CLEAN CASES THE FIRST DRAFT FAILED, and they are here because
    # each was the INSTRUMENT being wrong rather than a document being wrong: a PDF wraps
    # where the column ends, so a correct date renders across a line break and a substring
    # search called four sound documents undated; and a study with a COVER PAGE carries its
    # masthead on page 2, so reading one page called those undated too.
    for nm, dt, pages, must_fire in (
            ("TMGH as it shipped — the PDF nineteen hours behind its own .docx",
             datetime.date(2026, 9, 2),
             [['TALAAT MOUSTAFA', 'Valuation study - 1 September 2026', 'Headline']], True),
            ("a PDF carrying no date at all",
             datetime.date(2026, 9, 3), [['ZZZ plc', 'Independent Valuation Study']], True),
            ("CLEAN — the date SPLIT ACROSS A LINE BREAK, which is how a PDF wraps",
             datetime.date(2026, 9, 3),
             [['ZZZ plc', 'Egyptian Exchange - ZZZ - edition of 3', 'September 2026']],
             False),
            ("CLEAN — a COVER PAGE, the masthead on page two",
             datetime.date(2026, 9, 3),
             [['ZZZ plc', 'Independent Valuation Study'],
              ['Egyptian Exchange - ZZZ - edition of 3 September 2026', 'READ FIRST']],
             False),
            ("a THIRD page is not read — the masthead is not buried in the body",
             datetime.date(2026, 9, 3),
             [['ZZZ plc'], ['Contents'],
              ['edition of 3 September 2026']], True)):
        tmp = tempfile.mkdtemp(prefix='ncedp')
        try:
            sd = os.path.join(tmp, 'engine', 'zzz_study')
            os.makedirs(sd, exist_ok=True)
            base = os.path.join(sd, 'ZZZ_Valuation_Study_%s.' % dt.strftime('%d-%m-%Y'))
            plant(tmp, 'ZZZ_Valuation_Study_%s.docx' % dt.strftime('%d-%m-%Y'),
                  [l for pg in pages for l in pg])
            write_pdf(base + 'pdf', pages)
            _m.ROOT = tmp
            ex, offenders = _m.audit_delivered_pdfs()
            # THE MUTATION MUST BE ASSERTED TO HAVE LANDED. A fixture whose PDF the
            # extractor never read reports zero offenders, which is indistinguishable
            # from a clean document — the shape [R-ENF-04] is named for.
            if ex != 1:
                print('FAIL the fixture did not reach the extractor (examined %d)' % ex)
                bad += 1
                continue
            ok = (bool(offenders) == must_fire)
            print('%-4s %s' % ('PASS' if ok else 'FAIL', nm[:96]))
            if not ok:
                bad += 1
                print('      examined %d, offenders %s' % (ex, offenders))
        finally:
            _m.ROOT = ROOT
            shutil.rmtree(tmp, ignore_errors=True)

    # AN EMPTY PDF POPULATION IS A BROKEN PROBE, NOT A CLEAN BOOK: with no .pdf beside any
    # .docx the clause examines nothing, and the gate must refuse rather than pass.
    tmp = tempfile.mkdtemp(prefix='ncedz')
    try:
        build(tmp, {'ZZZ_Valuation_Study_03-09-2026.docx': GOOD}, with_pdf=False)
        rc, out = run(tmp)
        ok = rc != 0 and 'zero delivered PDFs' in out
        print('%-4s a run that read zero PDFs FAILS [R-ENF-04]' % ('PASS' if ok else 'FAIL'))
        bad += 0 if ok else 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    total = len(CASES) + 2 + 5 + 6
    print('\n%d/%d conditions behaved as specified' % (total - bad, total))
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
