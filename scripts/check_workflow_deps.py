#!/usr/bin/env python3
"""Every third-party module a CI gate imports AT TOP LEVEL is installed by its workflow.

WHY THIS EXISTS. On 5 September 2026 the band-vocabulary gate was extended to read the
delivered WORKBOOKS, which needs openpyxl. It passed here and it passed the local CI
runner — both environments already had openpyxl — and went red in Actions on all
twenty-two workbooks at once, every one reported as UNREADABLE. The gate was right: an
unreadable workbook is not a clean one. IT WAS RED FOR THE WRONG REASON, which is the
failure this repository has already recorded once inside a sandbox, and which reads
exactly like being red for the right one.

WHAT IT CHECKS AND WHAT IT DELIBERATELY DOES NOT. The bar is TOP-LEVEL imports, followed
through local modules, because those are what fail at import time — the thing a `pip
install` line has to cover for the script to run at all. An import inside a function fails
only when that function is called, which is a question about code paths rather than about
the environment, and a check that guessed at it would fire on modules a gate legitimately
never reaches. So the residue is stated rather than hidden: a gate that grows a new call
into a function-level scipy import can still go red on a missing dependency, and this will
not have warned about it.

THE LOCAL CI RUNNER CANNOT SUBSTITUTE FOR THIS. It runs the workflow's STEPS in whatever
environment it finds, so it models what the commands are and not what they run inside; on
the day this was written it reported 93 of 93 green while Actions was failing.
"""
from __future__ import annotations

import ast
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#: import name -> distribution name, where they differ.
ALIAS = {'docx': 'python-docx', 'PIL': 'pillow', 'yaml': 'pyyaml',
         'dateutil': 'python-dateutil', 'sklearn': 'scikit-learn',
         'bs4': 'beautifulsoup4', 'cv2': 'opencv-python'}


def _norm(p):
    return p.lower().replace('_', '-').split('==')[0].split('[')[0]


def _local_module(name):
    """Resolve a bare import to something in this repository, or None.

    A PACKAGE resolves to its __init__.py, which is why this returns a path rather than a
    boolean: `import engine` is local and its own top-level imports still count.
    """
    for cand in (os.path.join(ROOT, name, '__init__.py'),
                 os.path.join(ROOT, 'engine', name, '__init__.py'),
                 os.path.join(ROOT, 'engine', name + '.py'),
                 os.path.join(ROOT, 'scripts', name + '.py')):
        if os.path.exists(cand):
            return cand
    if os.path.isdir(os.path.join(ROOT, name)):
        return os.path.join(ROOT, name)          # a plain directory on sys.path
    hits = glob.glob(os.path.join(ROOT, 'engine', '**', name + '.py'), recursive=True)
    return hits[0] if len(hits) == 1 else None


def top_level_imports(path, seen=None):
    """Third-party modules this script imports at module scope, following local ones."""
    seen = seen if seen is not None else set()
    path = os.path.abspath(path)
    if path in seen or not os.path.exists(path):
        return set()
    if os.path.isdir(path):                      # a namespace directory has nothing to read
        seen.add(path)
        return set()
    seen.add(path)
    try:
        tree = ast.parse(open(path, encoding='utf-8').read())
    except (SyntaxError, OSError):
        return set()
    names = set()
    for node in tree.body:                      # MODULE SCOPE ONLY — that is the whole bar
        if isinstance(node, ast.Import):
            names |= {a.name.split('.')[0] for a in node.names}
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            names.add(node.module.split('.')[0])
        elif isinstance(node, (ast.If, ast.Try)):
            # a guarded top-level import still runs on the happy path
            for sub in ast.walk(node):
                if isinstance(sub, ast.Import):
                    names |= {a.name.split('.')[0] for a in sub.names}
                elif isinstance(sub, ast.ImportFrom) and sub.level == 0 and sub.module:
                    names.add(sub.module.split('.')[0])
    out = set()
    for n in names:
        if n in sys.stdlib_module_names:
            continue
        local = _local_module(n)
        if local:
            out |= top_level_imports(local, seen)
        else:
            out.add(n)
    return out


def survey():
    problems, examined = [], 0
    for wf in sorted(glob.glob(os.path.join(ROOT, '.github', 'workflows', '*.yml'))):
        src = open(wf, encoding='utf-8').read()
        installed = set()
        for m in re.finditer(r'pip install ([^\n#]+)', src):
            installed |= {_norm(p) for p in m.group(1).split()
                          if p.strip() and not p.startswith('-')}
        scripts = set(re.findall(r'python3? +((?:scripts|engine)/[\w./-]+\.py)', src))
        for rel in sorted(scripts):
            path = os.path.join(ROOT, rel)
            if not os.path.exists(path):
                continue
            examined += 1
            for mod in sorted(top_level_imports(path)):
                dist = _norm(ALIAS.get(mod, mod))
                if dist not in installed:
                    problems.append('%s runs %s, which imports %r at top level; the '
                                    'workflow installs %s'
                                    % (os.path.basename(wf), rel, mod,
                                       ', '.join(sorted(installed)) or 'nothing'))
    return problems, examined


def main():
    problems, examined = survey()
    # [R-ENF-04] an empty population is not a clean one.
    if not examined:
        print('FAIL — no workflow script was examined at all. This repository runs gates '
              'from its workflows, so reading none means the resolver broke rather than '
              'the dependencies being complete.')
        return 1
    if problems:
        print('FAIL — %d gate(s) import a module their workflow does not install:'
              % len(problems))
        for p in problems:
            print('  ' + p)
        print('\nA gate red on a missing dependency is red for the WRONG reason, and it '
              'reads exactly like being red for the right one.')
        return 1
    print('OK — every top-level third-party import of every workflow gate is installed '
          'by that workflow. %d script invocation(s) examined.' % examined)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
