#!/usr/bin/env python3
"""Reinject the 5-September-2026 condition and require check_workflow_deps to catch it.

The defect it was written for: the band-vocabulary gate grew a top-level openpyxl import
when it was extended to read delivered workbooks, the workflow's pip line was not extended
with it, and Actions went red on twenty-two workbooks at once — every one reported
UNREADABLE, which the gate is right to say and which was the wrong reason to be red.

Each case copies the repository's workflow and script layout into a sandbox, makes ONE
change, and asserts the checker's verdict. Every mutation is verified to have LANDED before
its result is believed: a case that silently changed nothing reports a green meaning only
that the file was untouched, which this repository has shipped once already.
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHECKER = os.path.join(ROOT, 'scripts', 'check_workflow_deps.py')


def stage(dst):
    """The layout the checker reads: the workflows, the scripts and the engine sources."""
    n = 0
    for sub in ('.github/workflows', 'scripts'):
        src = os.path.join(ROOT, sub)
        shutil.copytree(src, os.path.join(dst, sub))
        n += len(os.listdir(src))
    # engine: only the .py files matter, and copying the whole tree is 300MB
    for dp, _, fs in os.walk(os.path.join(ROOT, 'engine')):
        rel = os.path.relpath(dp, ROOT)
        for f in fs:
            if f.endswith('.py'):
                out = os.path.join(dst, rel, f)
                os.makedirs(os.path.dirname(out), exist_ok=True)
                shutil.copy2(os.path.join(dp, f), out)
                n += 1
    return n


def run(work):
    # RUN THE SANDBOX'S OWN COPY. The checker resolves its root from its own __file__, so
    # invoking the real one with cwd set to the sandbox reads the REAL repository and
    # reports clean on every injected defect — which is what the first draft of this control
    # did, and its four green results meant only that nothing had been examined.
    staged = os.path.join(work, 'scripts', 'check_workflow_deps.py')
    r = subprocess.run([sys.executable, staged], capture_output=True, text=True, cwd=work,
                       env=dict(os.environ, PYTHONPATH=work))
    return r.returncode != 0, r.stdout + r.stderr


# ---- the cases -------------------------------------------------------------------------

PROBE = 'scripts/_nc_probe.py'


def _add_probe(work, body, workflow='study-provenance.yml'):
    """Plant a script of our own and wire it into ONE workflow.

    THE FIRST DRAFT MUTATED AN EXISTING GATE AND THAT WAS THE WRONG FIXTURE: scripts/
    inject_site_chrome.py imports check_page_integrity, and deploy-pages.yml runs it with
    no pip line at all, so an import added to the one propagated into the other and the
    checker was RIGHT to fire. Its "clean" cases were failing on a real finding. A probe of
    our own reaches exactly one workflow and nothing else.
    """
    p = os.path.join(work, PROBE)
    open(p, 'w').write(body)
    wf = os.path.join(work, '.github/workflows', workflow)
    t = open(wf).read()
    out = re.sub(r'(\n(\s+)run: python3 scripts/)', r'\n\2run: python3 ' + PROBE + r'\1', t,
                 count=1)
    assert out != t, 'no step to attach the probe to — control is stale'
    open(wf, 'w').write(out)
    return os.path.exists(p) and PROBE in open(wf).read()


def case_drop_openpyxl(work):
    """THE CONDITION AS IT SHIPPED: the gate imports openpyxl, the workflow does not
    install it. Targeted at the pip LINE — the comment above it names openpyxl too, and a
    naive first-occurrence replace edits the comment and leaves the dependency in place."""
    p = os.path.join(work, '.github/workflows/band-record.yml')
    s = open(p).read()
    out = re.sub(r'(run: pip install [^\n#]*?) openpyxl', r'\1', s, count=1)
    assert out != s, 'openpyxl was not on the band-record pip line — control is stale'
    open(p, 'w').write(out)
    return 'openpyxl' not in re.search(r'run: pip install [^\n#]+', out).group(0)


def case_new_top_level_import(work):
    """A gate grows a top-level third-party import nobody added to the pip line."""
    return _add_probe(work, 'import nowhere_on_pypi_xyz\nprint(nowhere_on_pypi_xyz)\n')


def case_pip_line_emptied(work):
    """A workflow that installs nothing at all must not read as satisfied."""
    p = os.path.join(work, '.github/workflows/study-provenance.yml')
    s = open(p).read()
    out = re.sub(r'pip install [^\n#]+', 'pip install', s, count=1)
    assert out != s, 'no pip install line found — control is stale'
    open(p, 'w').write(out)
    return True


def case_no_workflows(work):
    """[R-ENF-04] an empty population is not a clean one."""
    d = os.path.join(work, '.github/workflows')
    for f in os.listdir(d):
        os.remove(os.path.join(d, f))
    return not os.listdir(d)


# ---- clean cases, which must NOT fire ---------------------------------------------------

def clean_function_level_import(work):
    """An import INSIDE a function is not what a pip line has to cover for the script to
    start, and flagging it would fire on modules a gate legitimately never reaches. This is
    the residue the checker's own docstring states rather than hides."""
    return _add_probe(work, 'def _never_called():\n    import nowhere_on_pypi_xyz\n'
                            '    return nowhere_on_pypi_xyz\n')


def clean_alias_distribution(work):
    """python-docx installs as `python-docx` and imports as `docx`. A checker comparing the
    two strings naively would condemn every workflow that reads a document."""
    return _add_probe(work, 'import docx\nprint(docx)\n')


def clean_local_module(work):
    """Importing this repository's own modules and packages is not a dependency."""
    return _add_probe(work, 'import band_record\nimport engine\nprint(band_record, engine)\n')


CASES = [('the openpyxl condition exactly as it shipped', case_drop_openpyxl),
         ('a gate grows a top-level import nobody installed', case_new_top_level_import),
         ('a pip line emptied', case_pip_line_emptied),
         ('no workflows at all', case_no_workflows)]
CLEAN = [('an import inside a function', clean_function_level_import),
         ('a distribution whose import name differs', clean_alias_distribution),
         ("this repository's own modules", clean_local_module)]


def main():
    failures = []
    for label, mutate, must_fail in ([(a, b, True) for a, b in CASES]
                                     + [(a, b, False) for a, b in CLEAN]):
        with tempfile.TemporaryDirectory() as tmp:
            work = os.path.join(tmp, 'repo')
            os.makedirs(work)
            stage(work)
            if not mutate(work):
                failures.append('%s: the mutation did not land — control is stale' % label)
                continue
            red, out = run(work)
            if red != must_fail:
                failures.append('%s: checker %s' % (
                    label, 'PASSED on an injected defect' if must_fail
                    else 'FAILED on a legitimate case\n      ' + out.strip()[:300]))
            else:
                print('  %s: %s' % ('caught' if must_fail else 'allowed', label))
    if failures:
        print('NEGATIVE CONTROL FAILED:')
        for f in failures:
            print('  ' + f)
        return 1
    print('negative control OK — %d defects caught, %d legitimate cases allowed through'
          % (len(CASES), len(CLEAN)))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
