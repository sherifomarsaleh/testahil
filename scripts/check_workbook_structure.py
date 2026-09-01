#!/usr/bin/env python3
"""The delivered workbook must BE the model report's sixteen sheets.  [R-ENF-01]

WHY THIS EXISTS
    On 1 September 2026 the AMOC rebuild shipped a workbook of SEVEN sheets — READ FIRST,
    Assumptions, Base Year, Product and Cost, Forecast, Sensitivity, Lenses — against the
    sixteen the model report requires. Its own compute.py attested

        MODEL_STUDY = ModelStudyChecklist(structure_matches_model=True, ...)
        assert_model_study(MODEL_STUDY)

    and the assertion passed, because a checklist that a study fills in about itself tests
    the study's opinion of its work and not the work. The same file recalculated with zero
    disagreements across 5,775 formula cells, cleared the external-reader scrub, and passed
    the table-discipline check: every gate that could see the workbook was looking at its
    contents rather than its shape.

    This is the composite-beta lesson in another costume — a self-set boolean nothing
    outside the study ever checked — and per [R-ENF-01] the fix closes the CLASS, not the
    instance: the sheet list is now read off the delivered .xlsx by a job that runs over
    every study directory from outside.

WHAT IT CHECKS, per study directory under engine/*_study/
    1. the directory has a workbook at all
    2. the LATEST-dated workbook in it — the one that would be published — opens
    3. its sheet names are exactly research_protocol.MODEL_STUDY['excel_sheets'], in that
       order. The list is imported, never copied here: a check that carries its own copy of
       the standard stops testing the standard the moment one of them moves.

THE POPULATION IS ANCHORED ELSEWHERE  [R-ENF-04]
    This gate globs engine/*_study, so a bad pattern would find nothing and report clean.
    It therefore holds the glob against a population counted somewhere else: every ticker
    named in workbook_outstanding.json must resolve to a study directory on disk, and a run
    that examined ZERO workbooks fails outright. Exact, never a threshold.

THE RATCHET  [R-ENF-02]
    Studies already off the standard on adoption day are listed in workbook_outstanding.json
    and are allowed to fail. The build breaks on a NEW mismatch, a NEW study with no
    workbook, or a study directory with no entry either way. The list may only ever get
    SHORTER — --prune rewrites it. A permanently red check is one everyone learns to ignore.

USAGE
    python3 scripts/check_workbook_structure.py          # gate; exit 1 on any hard fail
    python3 scripts/check_workbook_structure.py --prune  # drop the now-passing entries
"""
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENGINE = os.path.join(ROOT, 'engine')
OUTSTANDING = os.path.join(ENGINE, 'build_depth_audit', 'workbook_outstanding.json')
sys.path.insert(0, ENGINE)
import research_protocol as RP                                          # noqa: E402

WANT = list(RP.MODEL_STUDY['excel_sheets'])


def latest_workbook(sdir):
    """The workbook that would be published: the newest by the date in its filename.

    Study directories keep superseded editions beside the current one. Picking by
    modification time would make the answer depend on what a checkout happened to touch,
    so the date is read out of the filename, which is where these builders put it.
    """
    xs = [p for p in glob.glob(os.path.join(sdir, '*.xlsx'))
          if not os.path.basename(p).startswith('~$')]
    if not xs:
        return None
    def key(p):
        m = re.findall(r'(\d{8})', os.path.basename(p))
        if not m:
            return ('', os.path.basename(p))
        d = m[-1]
        return (d[4:] + d[2:4] + d[:2], os.path.basename(p))
    return sorted(xs, key=key)[-1]


def sheets_of(path):
    import openpyxl
    wb = openpyxl.load_workbook(path, read_only=True)
    try:
        return list(wb.sheetnames)
    finally:
        wb.close()


def examine(sdir):
    """(ticker, status, detail). status is 'ok' or a one-line reason it is not."""
    tk = os.path.basename(sdir)[:-len('_study')].upper()
    p = latest_workbook(sdir)
    if p is None:
        return tk, 'no workbook in the study directory', None
    try:
        names = sheets_of(p)
    except Exception as e:                                              # noqa: BLE001
        return tk, 'workbook will not open: %s: %s' % (type(e).__name__, e), p
    missing = [x for x in WANT if x not in names]
    extra = [x for x in names if x not in WANT]
    if missing or extra:
        return tk, ('%d sheets — missing %s; unexpected %s'
                    % (len(names), missing or 'nothing', extra or 'nothing')), p
    if names != WANT:
        return tk, '16 sheets, all named correctly, but NOT in the model order', p
    return tk, 'ok', p


def main(argv):
    prune = '--prune' in argv
    dirs = sorted(glob.glob(os.path.join(ENGINE, '*_study')))
    if not dirs:
        print('FAIL — examined zero study directories. An empty result is not a clean '
              'result [R-ENF-04]: the glob resolved nothing, which means this gate did '
              'not run rather than that everything passed.')
        return 1
    known = {}
    if os.path.exists(OUTSTANDING):
        known = json.load(open(OUTSTANDING, encoding='utf-8')).get('entries', {})

    on_disk = {os.path.basename(d)[:-len('_study')].upper() for d in dirs}
    stranded = sorted(set(known) - on_disk)

    results = [examine(d) for d in dirs]
    print('MODEL-REPORT SHEET LIST — %d sheets' % len(WANT))
    print('examined %d study directories\n' % len(results))

    ok, breaches, new = [], [], []
    for tk, status, path in results:
        if status == 'ok':
            ok.append(tk)
            continue
        breaches.append((tk, status, path))
        if tk not in known:
            new.append((tk, status))

    print('MATCHES THE MODEL REPORT (%d): %s' % (len(ok), ', '.join(ok) or 'none'))
    if breaches:
        print('\nOFF THE STANDARD (%d):' % len(breaches))
        for tk, status, path in breaches:
            print('   %-12s %s' % (tk, status))
            if path:
                print('   %-12s   %s' % ('', os.path.basename(path)))

    now_passing = sorted(set(known) & set(ok))
    if now_passing:
        print('\nNOW PASSING — remove from the list (%d): %s'
              % (len(now_passing), ', '.join(now_passing)))

    if prune:
        keep = {k: v for k, v in known.items() if k not in now_passing and k in on_disk}
        for tk, status, _ in breaches:
            keep.setdefault(tk, status)
        json.dump({'note': ('Studies whose delivered workbook was already off the '
                            'model-report sheet list when this gate was adopted '
                            '(01-Sep-2026). Allowed to fail; the list may only ever get '
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
        print('The population this gate is held against must exist [R-ENF-04].')
        bad += 1
    unlisted = [tk for tk, _, _ in results if tk not in known and tk not in ok]
    if unlisted:
        print('\nFAIL — %d new violation(s):' % len(unlisted))
        for tk, status in new:
            print('   %s: %s' % (tk, status))
        print('\nThe workbook a reader receives is part of the deliverable, not packaging. '
              'Build the missing sheets, or say in the study why this class cannot carry '
              'them — but do not attest structure_matches_model on a file that does not.')
        bad += 1
    if not bad:
        print('\nOK — no new violations.')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
