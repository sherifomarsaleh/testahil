#!/usr/bin/env python3
"""A SOURCE CONSTANT REBOUND AFTER AN INPUT HAS BEEN REGISTERED AGAINST IT [L-290].

    python3 scripts/check_source_rebinding.py [--prune]

WHY THIS EXISTS. Every gate in this repository asks whether an input carries its
four fields; none can ask whether the document named in the third field is the one
the number came out of, because a source is a STRING and any string satisfies the
check. That makes the source the one field in the register that can be silently
wrong while everything else reports clean -- and it fails invisibly in a way a wrong
VALUE does not, because a wrong value usually breaks an arithmetic check somewhere
downstream and a wrong source breaks nothing at all.

WHAT HAPPENED. A study defined a new source constant naming note 15 of an annual
report and assigned it to a name that, sixty lines earlier, already held that
company's FY2025 financial statements. Twelve inputs registered after that line --
three debt tranches, three facility spreads, a rejected capitalisation rate and five
non-current-asset geography figures -- were re-sourced to a note carrying none of
them. No value moved. The four-field assertion passed on all 208 inputs, the
workbook reconciled 1,084 of 1,084 formula cells, every document gate was green, and
the bibliography printed the wrong document beside each of the twelve. It shipped in
two commits.

WHAT THIS CHECKS, AND WHAT IT DELIBERATELY DOES NOT. It cannot tell whether a source
names the document a figure came from -- that is a research question and stays with
SIGCM and the QC gate. It checks the MECHANICAL half, which is exact and needs no
judgement: a module-level name that has been READ by a registration call and is then
REASSIGNED at module level is a source whose meaning changed under the inputs
already registered against it. That condition cannot occur innocently. A constant
assigned once and read many times is the ordinary shape; assign, read, reassign is
not, and a study that genuinely needs two documents needs two names.

The population is the study directories on disk [R-ENF-04]: a run that examined zero
files, or zero registration calls across the files it found, FAILS rather than
reporting clean -- an absent answer is not a clean one.
"""
import ast
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ENGINE = os.path.join(ROOT, 'engine')
OUTSTANDING = os.path.join(ENGINE, 'build_depth_audit', 'source_rebinding_outstanding.json')

# the calls that REGISTER an input against a source. A study naming its registrar
# something else is invisible to this check and that is stated rather than implied:
# the population count below is what makes such a study show up as examined-nothing.
REGISTRARS = ('inp', 'register_input', 'add_input')


def _module_level_string_names(tree):
    """Names assigned a string (or string concatenation) at module level, in order.

    Returns {name: [statement index, ...]} -- more than one index is a rebinding.
    """
    out = {}
    for i, node in enumerate(tree.body):
        if not isinstance(node, ast.Assign):
            continue
        if not _is_stringy(node.value):
            continue
        for t in node.targets:
            if isinstance(t, ast.Name):
                out.setdefault(t.id, []).append(i)
    return out


def _is_stringy(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return True
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        return _is_stringy(node.left) or _is_stringy(node.right)
    if isinstance(node, ast.JoinedStr):
        return True
    return False


def _reads_by_registrars(tree):
    """{name: [statement index, ...]} for names read inside a registration call."""
    out = {}
    for i, node in enumerate(tree.body):
        for call in (n for n in ast.walk(node) if isinstance(n, ast.Call)):
            fn = call.func
            name = fn.id if isinstance(fn, ast.Name) else getattr(fn, 'attr', None)
            if name not in REGISTRARS:
                continue
            for arg in ast.walk(call):
                if isinstance(arg, ast.Name) and isinstance(arg.ctx, ast.Load):
                    out.setdefault(arg.id, []).append(i)
    return out


def scan(path):
    """Every source constant in `path` rebound after a registration read it."""
    try:
        tree = ast.parse(open(path, encoding='utf-8').read(), filename=path)
    except SyntaxError as e:
        return [('%s does not parse: %s' % (os.path.basename(path), e))], 0
    assigns = _module_level_string_names(tree)
    reads = _reads_by_registrars(tree)
    findings = []
    for name, at in assigns.items():
        if len(at) < 2 or name not in reads:
            continue
        first_read = min(reads[name])
        later = [a for a in at if a > first_read]
        if later and min(at) <= first_read:
            after = [r for r in reads[name] if r > min(later)]
            findings.append(
                '%s is assigned a source at module level, read by a registration '
                'call, and REASSIGNED afterwards; %d input(s) are registered against '
                'it after the reassignment and carry the second document, not the '
                'first.' % (name, len(after)))
    return findings, sum(len(v) for v in reads.values())


def main(argv):
    prune = '--prune' in argv
    known = set()
    d = {}
    if os.path.exists(OUTSTANDING):
        d = json.load(open(OUTSTANDING, encoding='utf-8'))
        known = set(d.get('outstanding', []))

    dirs = sorted(glob.glob(os.path.join(ENGINE, '*_study')))
    if not dirs:
        print('FAIL — the population is empty: no engine/*_study directories were '
              'found. An empty result is not a clean result [R-ENF-04].')
        return 1

    examined, reads_total, bad = 0, 0, {}
    for dd in dirs:
        tk = os.path.basename(dd)[:-6].upper()
        for f in sorted(glob.glob(os.path.join(dd, '*.py'))):
            examined += 1
            findings, nreads = scan(f)
            reads_total += nreads
            if findings:
                bad.setdefault(tk, []).extend(
                    '%s: %s' % (os.path.basename(f), x) for x in findings)

    print('source-constant rebinding [L-290]')
    print('  %d python files across %d study directories; %d registration reads'
          % (examined, len(dirs), reads_total))
    if not examined or not reads_total:
        print('FAIL — examined %d files and found %d registration reads. A run that '
              'read nothing cannot report clean [R-ENF-04]; either the population '
              'resolver broke or the registrar is named something this check does '
              'not know.' % (examined, reads_total))
        return 1

    for tk in sorted(bad):
        tag = '[outstanding]' if tk in known else '[NEW]'
        print('  %-12s %s' % (tk, tag))
        for x in bad[tk]:
            print('     ', x)

    if prune:
        d['outstanding'] = sorted(set(bad) & known)
        d.setdefault('_', 'Ratcheted [R-ENF-02]: the list may only ever SHORTEN.')
        json.dump(d, open(OUTSTANDING, 'w', encoding='utf-8'), indent=1)
        print('pruned — now %d entries' % len(d['outstanding']))

    new = sorted(set(bad) - known)
    stale = sorted(known - set(bad))
    if stale and not prune:
        print('  (%d listed name(s) no longer offend: %s — run --prune)'
              % (len(stale), ', '.join(stale)))
    if new:
        print('FAIL — %d study(ies) rebind a source constant after registering '
              'inputs against it: %s' % (len(new), ', '.join(new)))
        return 1
    print('OK — no study rebinds a source constant under its own registered inputs.')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
