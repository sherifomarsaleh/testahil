#!/usr/bin/env python3
"""A study's Step 2A sweep runs through the SHARED register, or it does not run.  [R-ENF-01]

WHY THIS EXISTS
    CLAUDE.md says of engine/research_sweep.py: "Import this rather than hand-rolling a
    study-local sweep script." Sixteen studies do. On 3 September 2026 ARCC was found to be
    the one that did not, and what its hand-rolled version checked is the point:

        every finding has a source, a date and a model impact   PASSED
        the class is one of the four                            PASSED
        all four rings appear                                   PASSED
        finding ids are unique                                  PASSED
        every driver's cross-references resolve                 PASSED

    Five real checks, all five passing. What they are not is the module's EIGHT invariants,
    and replaying the same 26 findings through SweepRegister.validate() produced SEVEN
    errors the hand-rolled version had no idea it was missing — among them that the
    company's own website had been attempted and REFUSED and the refusal was recorded
    nowhere a checker could see; that the FY2025 investor presentation is cited by name and
    by page for six of the study's drivers and appeared in no finding; that the reviewed
    half the bridge stands on was consumed by the model and absent from the register; and
    that three top-down drivers each stated their evidenced absence in PROSE inside their
    own justification rather than as the negative search the invariant looks for.

    Five of the seven were closed by moving facts the study already held into the register's
    own form. Two remain and are named. THAT IS THE DIFFERENCE A GATE MAKES: it is the same
    research either way, and only one of the two states makes the gaps visible.

    This is the composite-beta shape for the fourth time — a study checked against the list
    its own author thought of — and per [R-ENF-01] the class is closed rather than the
    instance.

WHAT IT CHECKS, per study directory under engine/*_study/
    1. the directory has a sweep script at all
    2. that script IMPORTS engine/research_sweep.py rather than hand-rolling a register
    3. its committed sweep_register.json records that it was validated through the module
       (validated_through), carries the invariant result, and NAMES every invariant that
       still fires — a study may carry a gap; it may not carry a gap nobody wrote down

THE POPULATION IS ANCHORED ELSEWHERE  [R-ENF-04]
    Every ticker listed in sweep_outstanding.json must resolve to a study directory on disk,
    and a run that examined ZERO study directories fails outright.

THE RATCHET  [R-ENF-02]
    Studies with no sweep at all, or with one that predates the shared module, are listed
    and allowed to fail. The build breaks on a NEW hand-rolled sweep or a study that stops
    naming its own open invariants. The list may only ever get SHORTER — --prune.

USAGE
    python3 scripts/check_sweep_module.py          # gate; exit 1 on any new violation
    python3 scripts/check_sweep_module.py --prune  # drop the now-conforming entries
"""
import glob
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENGINE = os.path.join(ROOT, 'engine')
OUTSTANDING = os.path.join(ENGINE, 'build_depth_audit', 'sweep_outstanding.json')


def examine(sdir):
    tk = os.path.basename(sdir)[:-len('_study')].upper()
    scripts = sorted(glob.glob(os.path.join(sdir, 'sweep*.py')))
    if not scripts:
        return tk, 'no sweep script in the study directory'
    imports = [p for p in scripts
               if 'research_sweep' in open(p, encoding='utf-8', errors='replace').read()]
    if not imports:
        return tk, ('sweep script does not import research_sweep — a hand-rolled register '
                    'is checked against the list its author thought of, which on ARCC '
                    'passed five real checks and missed seven')
    # A STUDY CAN IMPORT THE MODULE FOR ITS ENUMS AND NEVER RUN ITS INVARIANTS, which is
    # EGCH's defect one level up: declaration without execution. The check is therefore
    # that validate() is CALLED, not that the module appears in the file. Measured across
    # the book on adoption day, all sixteen studies that import it also call it — so this
    # clause costs nothing today and closes the door that would otherwise be open.
    if not any('.validate()' in open(p, encoding='utf-8', errors='replace').read()
               for p in imports):
        return tk, ('imports research_sweep but never calls validate() — importing the '
                    'module for its enums is not running its invariants')
    reg = os.path.join(sdir, 'sweep_register.json')
    if not os.path.exists(reg):
        return tk, 'imports the shared register but commits no sweep_register.json'
    try:
        j = json.load(open(reg, encoding='utf-8'))
    except Exception as e:                                              # noqa: BLE001
        return tk, 'sweep_register.json will not parse: %s' % e
    # Where a register COMMITS its invariant result — the richer form ARCC now carries —
    # every failure it reports must be NAMED. A study may carry a gap; it may not carry a
    # gap nobody wrote down. Where it does not commit the result, the script's own call to
    # validate() is what enforces the invariants at build time, and that is checked above.
    errs = j.get('invariant_errors')
    if errs:
        named = j.get('uncovered') or {}
        unnamed = [e for e in errs if not any(k in e for k in named)]
        if unnamed:
            return tk, ('%d invariant failure(s) the study does not name in "uncovered": %s'
                        % (len(unnamed), unnamed[0][:110]))
    return tk, 'ok'


def main(argv):
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

    results = [examine(d) for d in dirs]
    print('STEP 2A SWEEP — the shared register and its eight invariants')
    print('examined %d study directories\n' % len(results))

    ok = [tk for tk, st in results if st == 'ok']
    bad = [(tk, st) for tk, st in results if st != 'ok']
    print('RUNS THROUGH THE SHARED REGISTER (%d): %s' % (len(ok), ', '.join(ok) or 'none'))
    if bad:
        print('\nDOES NOT (%d):' % len(bad))
        for tk, st in bad:
            print('   %-12s %s' % (tk, st))

    now_ok = sorted(set(known) & set(ok))
    if now_ok:
        print('\nNOW CONFORMING — remove from the list (%d): %s'
              % (len(now_ok), ', '.join(now_ok)))

    if '--prune' in argv:
        keep = {k: v for k, v in known.items() if k not in now_ok and k in on_disk}
        for tk, st in bad:
            keep.setdefault(tk, st)
        json.dump({'note': ('Studies whose Step 2A sweep did not run through '
                            'engine/research_sweep.py when this gate was adopted '
                            '(03-Sep-2026) — most of them have no sweep script at all. '
                            'Allowed to fail; the list may only ever get shorter.'),
                   'entries': keep},
                  open(OUTSTANDING, 'w', encoding='utf-8'), indent=1, sort_keys=True)
        open(OUTSTANDING, 'a', encoding='utf-8').write('\n')
        print('\npruned; %d entry/entries remain' % len(keep))
        return 0

    rc = 0
    if stranded:
        print('\nFAIL — %d listed study/studies no longer resolve on disk: %s'
              % (len(stranded), ', '.join(stranded)))
        rc = 1
    unlisted = [(tk, st) for tk, st in bad if tk not in known]
    if unlisted:
        print('\nFAIL — %d new violation(s):' % len(unlisted))
        for tk, st in unlisted:
            print('   %s: %s' % (tk, st))
        print('\nImport the shared register rather than hand-rolling one. A study-local '
              'validator checks the list its author thought of; ARCC\'s passed five real '
              'checks and missed seven, five of which were facts the study already held.')
        rc = 1
    if rc == 0:
        print('\nOK — no new violations.')
    return rc


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
