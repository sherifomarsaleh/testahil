#!/usr/bin/env python3
"""A NEW STUDY MUST CLEAR EVERY GATE, AND THIS PROVES IT RATHER THAN ASSERTING IT.

[R-ENF-07]

WHY THIS EXISTS
    The point of a ratcheted gate is that knowingly-outstanding work is listed and allowed
    to fail while the build breaks on a NEW violation. Every gate in this repository says
    so in its own docstring, and every one is negative-controlled on its own conditions.
    What none of them tests is the claim the whole design rests on:

        A STUDY DIRECTORY CREATED TOMORROW, WITH NOTHING IN IT, GOES RED EVERYWHERE.

    That is a property of the SYSTEM rather than of any gate, so no gate can check it. It
    is also the exact claim the programme was asked to deliver — that a study is produced
    correctly and passes several checks without anyone intervening — and it is the kind of
    claim that is true by construction right up to the day a ratchet is seeded one entry
    too generously, or a gate globs a pattern a new directory happens not to match, or a
    check skips a study whose numbers file will not parse.

    So this walks the whole set: it copies the repository into a sandbox, plants an empty
    study directory called ZZTEST_study, and runs every ratcheted gate. Each one must go
    RED and must NAME the new study. A gate that stays green on a study with no numbers, no
    documents, no workbook, no sweep and no records is a gate a new name can walk past.

WHAT A PASS MEANS, AND WHAT IT DOES NOT
    A pass means every gate in the set REFUSES an unknown study directory. It does not mean
    the gates are individually right — each has its own negative control for that — and it
    does not mean a study cannot be wrong in a way no gate models. It means the guideline
    BINDS on a new name rather than depending on whoever builds it remembering to look.

USAGE
    python3 scripts/check_new_study_gauntlet.py           # gate
    python3 scripts/check_new_study_gauntlet.py --verbose # each gate's own last line
"""
import glob
import json
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TICKER = 'ZZTEST'

# THE SET IS SPLIT, AND THE SPLIT IS THE FINDING [measured 03-Sep-2026 on the first run].
# A single list of "study gates" turned out to conflate two different kinds of check, and
# four of the seventeen stayed green on an empty directory for a perfectly good reason:
# they bite on ARTEFACTS, not on the directory. A study with no delivered documents cannot
# leak internal vocabulary and cannot publish a retired blend. Demanding that those gates
# refuse an empty directory would be a false claim about what they check — so they are
# tested the way they actually work, by planting a MINIMAL OFFENDING ARTEFACT and asserting
# they catch it.
#
# a builder that READS the artefact, which is what makes the artefact gate's subject exist
BUILDER_STUB = "import json\nd = json.load(open('diagnostics.json'))\n"

# DIRECTORY GATES: must refuse a study directory that exists and holds nothing. These are
# the checks a new name cannot walk past by simply not producing something.
DIRECTORY_GATES = [
    'check_study_provenance.py',
    'check_workbook_structure.py',
    'check_document_structure.py',
    'check_sweep_module.py',
    'check_prose_figures.py',
    'check_valuation_gap.py',
    'check_macro_coherence.py',
    'check_bridge.py',
    'check_lens_design.py',
    'check_cost_of_capital.py',
    'check_output_records.py',
    'check_forecast_anchor.py',
]

# ARTEFACT GATES: bite once the study produces the artefact they read, and are tested by
# planting one that should trip them. `plant` returns the files to create.
ARTEFACT_GATES = {
    'check_delivered_vocabulary.py': (
        'a delivered document naming a standing rule',
        lambda: {'%s_Valuation_Study_03-09-2026.docx' % TICKER: ('docx', 'Adopted under '
                                                                 '[R-GAP-01] in September.')}),
    'check_artefact_currency.py': (
        'a builder-read JSON carrying a central and declaring no vintage',
        lambda: {'diagnostics.json': ('json', {'central': 12.34, 'note': 'no declaration'}),
                 'build_it.py': ('py', BUILDER_STUB)}),
}

# NOT IN EITHER SET, and each with the reason, because a name in a list that resolves to
# the wrong subject is worse than an absence [R-ENF-04]:
#   check_valuation_inputs.py       anchors on WALK-FORWARD run directories, not on study
#                                   directories — a new study is not its subject
#   check_calibration_deliverables.py  anchors on the campaign queue's calibrated names
#   check_lens_vocabulary.py        reads delivered PDFs; with no PDF there is nothing to
#                                   read, and its own population anchoring covers the case
#                                   where the whole book has none
EXCLUDED = {
    'check_valuation_inputs.py': 'anchors on walk-forward run directories, not study '
                                 'directories',
    'check_calibration_deliverables.py': "anchors on the campaign queue's calibrated names",
    'check_lens_vocabulary.py': 'reads delivered PDFs; an empty study has none',
}


def sandbox():
    """A copy of the repository with one empty study directory planted in it.

    Copied rather than mutated: a gate that rebuilds a ratchet, or a --prune run reached by
    accident, must not be able to touch the real tree. This repository has already paid for
    running repo-mutating steps against a live checkout once.
    """
    tmp = tempfile.mkdtemp(prefix='gauntlet_')
    def ignore(d, names):
        # raw_indices was excluded in the first draft and check_study_provenance CRASHED on
        # its absence — going red for the wrong reason, which reads exactly like going red
        # for the right one. An excluded directory a gate needs is a sandbox defect
        # masquerading as a finding [R-ENF-04].
        return [n for n in names
                if n in ('.git', '__pycache__', 'raw_ohlc', 'panels', 'node_modules',
                         'filings')]
    shutil.copytree(ROOT, os.path.join(tmp, 'repo'), ignore=ignore, symlinks=True)
    repo = os.path.join(tmp, 'repo')
    os.makedirs(os.path.join(repo, 'engine', '%s_study' % TICKER.lower()), exist_ok=True)
    return tmp, repo


def run(repo, gate):
    r = subprocess.run([sys.executable, os.path.join('scripts', gate)],
                       cwd=repo, capture_output=True, text=True, timeout=1800)
    out = (r.stdout or '') + (r.stderr or '')
    lines = [l for l in out.strip().splitlines() if l.strip()]
    return r.returncode, out, (lines[-1] if lines else '')


def plant(sdir, files):
    """Create the artefacts an artefact gate needs as its subject."""
    for name, (kind, payload) in files.items():
        path = os.path.join(sdir, name)
        if kind == 'docx':
            import docx
            d = docx.Document()
            d.add_paragraph(payload)
            d.save(path)
        elif kind == 'json':
            json.dump(payload, open(path, 'w', encoding='utf-8'))
        else:
            open(path, 'w', encoding='utf-8').write(payload)


def main(argv):
    verbose = '--verbose' in argv
    tmp, repo = sandbox()
    sdir = os.path.join(repo, 'engine', '%s_study' % TICKER.lower())
    try:
        print('NEW-STUDY GAUNTLET — an empty engine/%s_study/ planted in a sandbox copy'
              % TICKER.lower())
        print('%d directory gates, %d artefact gates, %d excluded with a stated reason\n'
              % (len(DIRECTORY_GATES), len(ARTEFACT_GATES), len(EXCLUDED)))

        red, wrong, missing = [], [], []

        print('DIRECTORY GATES — must refuse a study directory that holds nothing')
        for gate in DIRECTORY_GATES:
            if not os.path.exists(os.path.join(repo, 'scripts', gate)):
                missing.append(gate)
                continue
            try:
                rc, out, last = run(repo, gate)
            except Exception as e:                                      # noqa: BLE001
                rc, out, last = 1, '', '%s: %s' % (type(e).__name__, e)
            named = TICKER in out
            ok = rc != 0 and named
            (red if ok else wrong).append((gate, rc, named, last))
            print('   %-4s %-40s exit %d%s' % ('RED ' if ok else 'MISS', gate, rc,
                                               '' if named else '   (does not name it)'))
            if verbose:
                print('        %s' % last[:150])

        print('\nARTEFACT GATES — bite once the study produces what they read')
        for gate, (what, mk) in ARTEFACT_GATES.items():
            if not os.path.exists(os.path.join(repo, 'scripts', gate)):
                missing.append(gate)
                continue
            for f in os.listdir(sdir):
                os.remove(os.path.join(sdir, f))
            try:
                plant(sdir, mk())
                rc, out, last = run(repo, gate)
            except Exception as e:                                      # noqa: BLE001
                rc, out, last = 0, '', '%s: %s' % (type(e).__name__, e)
            named = TICKER in out
            ok = rc != 0 and named
            (red if ok else wrong).append((gate, rc, named, last))
            print('   %-4s %-40s exit %d   %s' % ('RED ' if ok else 'MISS', gate, rc, what))
            if verbose:
                print('        %s' % last[:150])
        for f in os.listdir(sdir):
            os.remove(os.path.join(sdir, f))

        print('\nEXCLUDED, each with its reason')
        for gate, why in EXCLUDED.items():
            print('   %-45s %s' % (gate, why))
            if not os.path.exists(os.path.join(repo, 'scripts', gate)):
                missing.append(gate)

        print('\n%d of %d gates refuse a new study'
              % (len(red), len(red) + len(wrong)))
        rc = 0
        if missing:
            print('\nFAIL — %d gate(s) named in this file do not exist: %s'
                  % (len(missing), ', '.join(sorted(set(missing)))))
            print('The lists ARE the claim; a name resolving to nothing means the claim is '
                  'about a gate that is not there [R-ENF-04].')
            rc = 1
        if wrong:
            print('\nFAIL — %d gate(s) did not refuse the new study, or went red without '
                  'naming it:' % len(wrong))
            for gate, code, named, last in wrong:
                print('   %-40s exit %d  names it: %s' % (gate, code, named))
                print('   %-40s   %s' % ('', last[:130]))
            print('\nA gate that does not refuse a study with no numbers, no documents, no '
                  'workbook, no sweep and no records is one a new name can walk past. '
                  'Either it should cover a new study and does not, or it belongs in '
                  'ARTEFACT_GATES or EXCLUDED — and saying WHICH is the whole point of '
                  'this file.')
            rc = 1
        if rc == 0:
            print('\nOK — every directory gate refuses an empty study by name, and every '
                  'artefact gate catches a planted offender. The guideline binds on a new '
                  'study rather than on whoever builds it remembering to look.')
        return rc
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
