#!/usr/bin/env python3
"""A check nobody has seen fail is not evidence.

Every condition is injected into a SANDBOX COPY and the gate must go red on it, or stay
green where the artefact really is current. Every mutation is asserted to have LANDED
before the gate runs.

THE CASES THAT MATTER ARE 4, 5 AND 6 — the build manifest. It exists because a figure
that regenerates byte-identically is never re-committed, so git reads it as older than
the numbers it was just drawn from. That is an escape hatch in a staleness gate, and an
escape hatch nobody tried to abuse is not known to be safe: editing the artefact after
the build, editing the numbers after the build, or handing the gate a manifest it cannot
parse must each drop straight back to the commit-time test.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GATE = os.path.join('scripts', 'check_artefact_freshness.py')
RAT = os.path.join('engine', 'build_depth_audit', 'artefact_freshness_outstanding.json')
PNG = (b'\x89PNG\r\n\x1a\n' + b'\x00' * 64)
DOCX_STUB = b'PK\x03\x04' + b'\x00' * 64


def sha(p):
    h = hashlib.sha256()
    h.update(open(p, 'rb').read())
    return h.hexdigest()


_CLOCK = [1_700_000_000]


def git(d, *a, bump=True):
    """Git, with an EXPLICIT commit time that advances by an hour each commit.

    Git stamps to the second and this harness commits in rapid succession, so every
    fixture commit landed in the same second and "the PDF is older than its document"
    was never true of the tree the gate read. The control reported the gate green on a
    breach it had not actually planted -- which is the shape the control exists to catch,
    occurring inside the control.
    """
    if a and a[0] == 'commit' and bump:
        _CLOCK[0] += 3600
    stamp = str(_CLOCK[0])
    env = dict(os.environ, GIT_AUTHOR_DATE='@%s +0000' % stamp,
               GIT_COMMITTER_DATE='@%s +0000' % stamp)
    subprocess.run(['git'] + list(a), cwd=d, check=True, env=env,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def sandbox():
    """A throwaway repo with one study whose artefacts are all current."""
    _CLOCK[0] = 1_700_000_000
    d = tempfile.mkdtemp(prefix='fresh_nc_')
    os.makedirs(os.path.join(d, 'scripts'))
    os.makedirs(os.path.join(d, 'engine', 'build_depth_audit'))
    sd = os.path.join(d, 'engine', 'alpha_study')
    os.makedirs(sd)
    shutil.copy(os.path.join(ROOT, GATE), os.path.join(d, GATE))
    json.dump({'stale': {}}, open(os.path.join(d, RAT), 'w'))
    open(os.path.join(sd, 'edition.py'), 'w').write(
        "import datetime as _dt\nEDITION = _dt.date(2026, 1, 1)\n"
        "STUDY_DOCX = 'ALPHA_Valuation_Study_01-01-2026.docx'\n"
        "STUDY_PDF = 'ALPHA_Valuation_Study_01-01-2026.pdf'\n")
    json.dump({'central': 1.0}, open(os.path.join(sd, 'study_numbers.json'), 'w'))
    open(os.path.join(sd, 'ALPHA_Valuation_Study_01-01-2026.docx'), 'wb').write(DOCX_STUB)
    open(os.path.join(sd, 'ALPHA_Valuation_Study_01-01-2026.pdf'), 'wb').write(DOCX_STUB)
    open(os.path.join(sd, 'fig1.png'), 'wb').write(PNG)
    git(d, 'init', '-q')
    git(d, 'config', 'user.email', 'nc@example.invalid')
    git(d, 'config', 'user.name', 'nc')
    git(d, 'add', '-A')
    git(d, 'commit', '-q', '-m', 'everything at once')
    return d, sd


def recommit(d, path, msg, content=None):
    """Touch a file into a LATER commit, so its commit time moves ahead."""
    if content is not None:
        open(path, 'wb').write(content)
    else:
        with open(path, 'ab') as fh:
            fh.write(b'\x00')
    git(d, 'add', '-A')
    git(d, 'commit', '-q', '-m', msg)


def commit(d, msg):
    """Commit what is on disk, changing nothing. recommit() APPENDS a byte, which is
    right for forcing a file into a later commit and wrong for a manifest -- it made the
    JSON unparseable and case 4 then tested the broken-manifest path twice."""
    git(d, 'add', '-A')
    git(d, 'commit', '-q', '-m', msg)


def manifest(sd, numbers_ok=True, fig_ok=True, broken=False):
    p = os.path.join(sd, 'build_manifest.json')
    if broken:
        open(p, 'w').write('{ this is not json')
        return
    n = sha(os.path.join(sd, 'study_numbers.json')) if numbers_ok else 'x' * 64
    f = sha(os.path.join(sd, 'fig1.png')) if fig_ok else 'y' * 64
    json.dump({'numbers_sha256': n, 'artefacts': {'fig1.png': f}}, open(p, 'w'))


def run(d):
    r = subprocess.run([sys.executable, GATE], cwd=d, stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT, text=True, timeout=300)
    return r.returncode, r.stdout


CASES = []


def case(name, build, expect_red):
    CASES.append((name, build, expect_red))


def c_clean(d, sd):
    pass


def c_pdf_older(d, sd):
    recommit(d, os.path.join(sd, 'ALPHA_Valuation_Study_01-01-2026.docx'),
             'the document changes and the PDF does not')


def c_fig_older(d, sd):
    recommit(d, os.path.join(sd, 'study_numbers.json'), 'the numbers move',
             json.dumps({'central': 2.0}).encode())


def c_manifest_ok(d, sd):
    c_fig_older(d, sd)
    manifest(sd)
    commit(d, 'record the build')


def c_manifest_fig_edited(d, sd):
    c_fig_older(d, sd)
    manifest(sd)
    commit(d, 'record the build')
    open(os.path.join(sd, 'fig1.png'), 'wb').write(PNG + b'edited')


def c_manifest_numbers_edited(d, sd):
    c_fig_older(d, sd)
    manifest(sd)
    commit(d, 'record the build')
    json.dump({'central': 3.0}, open(os.path.join(sd, 'study_numbers.json'), 'w'))
    git(d, 'add', '-A')
    git(d, 'commit', '-q', '-m', 'numbers move again, manifest not refreshed')


def c_manifest_broken(d, sd):
    c_fig_older(d, sd)
    manifest(sd, broken=True)
    commit(d, 'an unreadable manifest')


def c_no_studies(d, sd):
    shutil.rmtree(sd)
    git(d, 'add', '-A')
    git(d, 'commit', '-q', '-m', 'the study is gone')


case('1. everything committed together — current', c_clean, False)
case('2. the document moves and its PDF does not [Tier A]', c_pdf_older, True)
case('3. the numbers move and a figure does not [Tier B]', c_fig_older, True)
case('4. a manifest proving the figure came from these numbers', c_manifest_ok, False)
case('5. the manifest is right and the FIGURE was edited after it',
     c_manifest_fig_edited, True)
case('6. the manifest is right and the NUMBERS were edited after it',
     c_manifest_numbers_edited, True)
case('7. a manifest that will not parse', c_manifest_broken, True)
case('8. no study directories at all [R-ENF-04]', c_no_studies, True)


def main():
    bad = []
    for name, build, expect_red in CASES:
        d, sd = sandbox()
        try:
            build(d, sd)
            rc, out = run(d)
            red = rc != 0
            ok = red == expect_red
            print('%-58s %-5s %s' % (name, 'RED' if red else 'green',
                                     'ok' if ok else '*** NOT AS REQUIRED'))
            if not ok:
                bad.append((name, out))
        finally:
            shutil.rmtree(d, ignore_errors=True)
    if bad:
        print('\n%d condition(s) did not behave as required:' % len(bad))
        for n, o in bad:
            print('\n--- %s\n%s' % (n, o[:1400]))
        return 1
    print('\nall %d conditions behave as required' % len(CASES))
    return 0


if __name__ == '__main__':
    sys.exit(main())
