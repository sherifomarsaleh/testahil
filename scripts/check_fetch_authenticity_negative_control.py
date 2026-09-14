#!/usr/bin/env python3
"""Negative control for the fetch-authenticity gate.

A CHECK NOBODY HAS SEEN FAIL IS NOT EVIDENCE, and on this instrument the clean cases matter
more than the dirty ones. Both of its tests are the kind that widen easily: a size bar, a
list of signatures, a set of directory names. Widening any of them would turn real filings
into failures, and the first response to that would be to loosen the gate — which is the
move [R-COC-01] forbids.

So the cases below are weighted to prove NARROWNESS, not sensitivity:

  case 10  the IMF's mis-extensioned .xls at its named path is allowed
  case 11  THE SAME BYTES AT ANOTHER PATH STILL FAIL — the exception is one path, not a
           pattern, so the next fetch failure cannot inherit it
  case 12  a real 300 KB filing that QUOTES "the requested URL was rejected" in its own
           text does not fire — the size bar is what separates a block page from a
           document that discusses one
  case 13  a block signature OUTSIDE a study's source directories does not fire — this
           gate governs what a study fetched, not every file in the repository
  case 14  a small HTML capture that is genuine content does not fire
"""
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
import check_fetch_authenticity as G                                   # noqa: E402

PDF = b'%PDF-1.7\n1 0 obj\n<< /Type /Catalog >>\nendobj\ntrailer\n'
XLSX = b'PK\x03\x04\x14\x00\x00\x00\x08\x00' + b'\x00' * 40
WAF = (b'<html><head><title>Request Rejected</title></head>\n<body>The requested URL was '
       b'rejected. Please consult with your administrator.<br/><br/>\nYour support ID is '
       b'f63899a7-69d2-4c00-a113-f144bad68c25<br/><br/></body></html>\n')
IMPERVA = (b'<!DOCTYPE html>\n<html><head>\n<script type="text/javascript">\n(function(){\n'
           b'window["bobcmn"] = "10111111111010200000005";\n})();\n</script></head></html>')
JSON404 = b'{"data":null,"error":{"status":404,"name":"NotFoundError","message":"Not Found"}}'
WEO = 'WEO Country Code\tISO\tWEO Subject Code\tCountry\n'.encode('utf-16-le')

# (label, relative path, bytes, must fire on test 1, must fire on test 2)
CASES = [
    ('1  a WAF rejection page under a .pdf name in a filings directory',
     'engine/xx_study_pending/filings/CBE_MPR_Q1_2026.pdf', WAF, True, True),
    ('2  an Imperva bot challenge under a .pdf name',
     'engine/xx_study_pending/src/egx_fy2025.pdf', IMPERVA, True, True),
    ('3  an API 404 envelope under a .pdf name',
     'engine/xx_study_pending/src/pdf/bodsum.pdf', JSON404, True, True),
    ('4  a WAF page with an HONEST .html extension — type is fine, content is not',
     'engine/xx_study_pending/src/cbe.html', WAF, False, True),
    ('5  a Cloudflare challenge saved as a source capture',
     'engine/xx_study_pending/sources/ir.html',
     b'<html><body>Checking your browser before accessing the site.</body></html>',
     False, True),
    ('6  an S3 AccessDenied body saved as a filing',
     'engine/xx_study_pending/filings/fy2025.xml',
     b'<?xml version="1.0"?><Error><Code>AccessDenied</Code></Error>', False, True),

    ('7  a real PDF — must NOT fire',
     'engine/xx_study_pending/filings/fy2025_audited.pdf', PDF, False, False),
    ('8  a real workbook — must NOT fire',
     'files/XX_Valuation_Model_09092026.xlsx', XLSX, False, False),
    ('9  a genuine HTML capture in a source directory — must NOT fire',
     'engine/xx_study_pending/src/ir_page.html',
     b'<!DOCTYPE html><html><body><h1>Investor Relations</h1><p>FY2025 revenue EGP 9,089m'
     b'</p></body></html>', False, False),

    ('10 the IMF WEO file at its NAMED path — allowed by exception',
     'engine/scem_walkforward/weo/WEOApr2025all.xls', WEO, False, False),
    ('11 THE SAME BYTES AT ANOTHER PATH — the exception is a path, not a pattern',
     'engine/xx_study_pending/weo/WEOApr2025all.xls', WEO, True, False),
    ('12 a 300 KB filing that QUOTES a rejection page in its own prose — must NOT fire',
     'engine/xx_study_pending/filings/it_policy.html',
     b'<html><body><p>Our portal returns "The requested URL was rejected" when the firewall'
     b' refuses a session.</p>' + b'<p>padding</p>' * 30000 + b'</body></html>',
     False, False),
    ('13 a block signature OUTSIDE any study source directory — must NOT fire',
     'docs/session_notes/waf_examples.html', WAF, False, False),
    ('14 a short genuine capture in a filings directory — must NOT fire',
     'engine/xx_study_pending/filings/note.txt',
     b'Revenue for the year ended 31 December 2025: EGP 9,089,149,688.', False, False),
]


def run_cases():
    d = tempfile.mkdtemp(prefix='fetch-nc-')
    bad = []
    try:
        rels = []
        for _, rel, blob, _, _ in CASES:
            p = os.path.join(d, rel)
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, 'wb') as fh:
                fh.write(blob)
            rels.append(rel)
        type_bad, block_bad, n_type, n_block = G.survey(d, rels)
        t_hit = {r for r, _ in type_bad}
        b_hit = {r for r, _ in block_bad}
        for label, rel, _, want_t, want_b in CASES:
            got_t, got_b = rel in t_hit, rel in b_hit
            ok = (got_t == want_t) and (got_b == want_b)
            print('  %s  %s' % ('PASS' if ok else 'FAIL', label))
            if not ok:
                bad.append('%s — test1 fired=%s wanted=%s, test2 fired=%s wanted=%s'
                           % (label, got_t, want_t, got_b, want_b))
        print('\n  (%d files put to test 1, %d to test 2)' % (n_type, n_block))
    finally:
        shutil.rmtree(d, ignore_errors=True)
    return bad


def run_unreadable():
    """A file that cannot be read is a failure, never a skip.

    The planted case is a TRACKED SYMLINK whose target is gone — git records the link, so
    the path is in the population, and opening it raises. A permission bit would not do:
    CI and this repo both run as root, where chmod 0 is not a barrier, and the control
    would pass for the wrong reason.
    """
    d = tempfile.mkdtemp(prefix='fetch-nc-')
    try:
        rel = 'engine/xx_study_pending/filings/fy2025_audited.pdf'
        p = os.path.join(d, rel)
        os.makedirs(os.path.dirname(p))
        os.symlink(os.path.join(d, 'gone', 'never_fetched.pdf'), p)
        type_bad, _, _, _ = G.survey(d, [rel])
        unreadable = any('UNREADABLE' in why for _, why in type_bad)
        print('  %s  15 an unreadable file is a failure, not a skip'
              % ('PASS' if unreadable else 'FAIL'))
        return [] if unreadable else ['an unreadable file was skipped instead of failing']
    finally:
        shutil.rmtree(d, ignore_errors=True)


def run_empty_population():
    """[R-ENF-04] — a run that examines nothing must FAIL, not pass."""
    d = tempfile.mkdtemp(prefix='fetch-nc-')
    try:
        os.makedirs(os.path.join(d, 'scripts'))
        shutil.copy(os.path.join(ROOT, 'scripts', 'check_fetch_authenticity.py'),
                    os.path.join(d, 'scripts'))
        with open(os.path.join(d, 'readme.txt'), 'w') as fh:
            fh.write('nothing here has a binary extension\n')
        for cmd in (['git', 'init', '-q'], ['git', 'add', '-A']):
            subprocess.run(cmd, cwd=d, check=True, capture_output=True)
        p = subprocess.run([sys.executable, 'scripts/check_fetch_authenticity.py'],
                           cwd=d, capture_output=True, text=True)
        ok = p.returncode != 0 and 'examined nothing' in p.stdout
        print('  %s  16 a run that examines nothing FAILS [R-ENF-04]'
              % ('PASS' if ok else 'FAIL'))
        return [] if ok else ['an empty population exited %d and did not fail loudly'
                              % p.returncode]
    finally:
        shutil.rmtree(d, ignore_errors=True)


def main():
    print('NEGATIVE CONTROL — fetch authenticity\n')
    bad = run_cases()
    print()
    bad += run_unreadable()
    bad += run_empty_population()
    if bad:
        print('\nFAIL — %d control(s) did not behave as specified:' % len(bad))
        for b in bad:
            print('  %s' % b)
        return 1
    print('\nPASS — %d conditions. The gate fires on every planted failure, stays silent on'
          ' every\nplanted clean case, and its one exception list is keyed on exact paths.'
          % (len(CASES) + 2))
    return 0


if __name__ == '__main__':
    sys.exit(main())
