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


def plant(root, name, paras):
    import docx
    d = docx.Document()
    for p in paras:
        d.add_paragraph(p)
    sd = os.path.join(root, 'engine', '%s_study' % name.split('_')[0].lower())
    os.makedirs(sd, exist_ok=True)
    d.save(os.path.join(sd, name))


def build(tmp, docs, ratchet=None):
    os.makedirs(os.path.join(tmp, 'scripts'), exist_ok=True)
    os.makedirs(os.path.join(tmp, 'engine', 'build_depth_audit'), exist_ok=True)
    shutil.copy(os.path.join(ROOT, GATE), os.path.join(tmp, GATE))
    for name, paras in docs.items():
        plant(tmp, name, paras)
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

    total = len(CASES) + 2
    print('\n%d/%d conditions behaved as specified' % (total - bad, total))
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
