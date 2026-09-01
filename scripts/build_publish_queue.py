"""Stage the calibrated deliverables for a SINGLE BATCH PUBLICATION at the end of
the fundamental-calibration campaign.

Per instruction of 1 September 2026: nothing from the campaign goes live one name
at a time. The whole book publishes together, in a new location, with TWO FILES
PER CALIBRATED TICKER — the valuation report as a PDF and the workbook beside it.
Until then `assets/data.js` carries the PRE-CALIBRATION range and the calibrated
one lives in engine/fv_movement.json and in each study's own numbers file.

This script does not publish anything. It assembles the queue, records what each
file carries, and REFUSES rather than staging a name it cannot vouch for: a
missing PDF, a workbook whose study reports no fair value, or a fair value that
disagrees with the movement register are all failures here, because the point of
staging early is that the batch publication is mechanical when it comes.

    python3 scripts/build_publish_queue.py            build and verify
    python3 scripts/build_publish_queue.py --check    verify only, no writes
"""
import argparse, glob, json, os, re, shutil, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENGINE = os.path.join(ROOT, 'engine')
QUEUE = os.path.join(ENGINE, 'publish_queue')
MOVEMENT = os.path.join(ENGINE, 'fv_movement.json')

# A name enters the queue when it has a walk-forward run directory on disk. That
# is the same anchor scripts/check_lessons_register.py uses, and it is chosen for
# the same reason: a queue keyed on its own list can quietly stop being fed,
# while one keyed on the runs cannot [R-ENF-04].
def calibrated():
    out = []
    for d in sorted(glob.glob(os.path.join(ENGINE, '*_walkforward'))):
        t = os.path.basename(d)[:-len('_walkforward')].upper()
        out.append((t, d))
    return out


def newest(pattern):
    """The most recent file matching a dated pattern, by the date IN THE NAME."""
    hits = []
    for p in glob.glob(pattern):
        m = re.search(r'(\d{2})[-_]?(\d{2})[-_]?(\d{4})', os.path.basename(p))
        if m:
            hits.append(('%s%s%s' % (m.group(3), m.group(2), m.group(1)), p))
    return max(hits)[1] if hits else None


def study_dir(t):
    return os.path.join(ENGINE, '%s_study' % t.lower())


def recorded_fair(t, mv):
    e = (mv.get('entries', {}).get(t) or {}).get('editions') or []
    return e[-1]['fair'] if e else None


def build(check_only=False):
    mv = json.load(open(MOVEMENT))
    rows, problems = [], []
    for t, run in calibrated():
        sd = study_dir(t)
        if not os.path.isdir(sd):
            problems.append('%s: a walk-forward ran but there is no %s_study directory'
                            % (t, t.lower()))
            continue
        report = newest(os.path.join(sd, '%s_Valuation_Study_*.pdf' % t))
        book = newest(os.path.join(sd, '%s_Valuation_Model_*.xlsx' % t))
        fair = recorded_fair(t, mv)
        if not report:
            problems.append('%s: no valuation report PDF. The deliverable is a PDF; the Word '
                            'file is the build artefact.' % t)
        if not book:
            problems.append('%s: no valuation workbook' % t)
        if not fair:
            problems.append('%s: no fair value recorded in the movement register, so there is '
                            'nothing to say this file carries' % t)
        if problems and problems[-1].startswith(t):
            continue
        rows.append({'ticker': t, 'report': os.path.relpath(report, ROOT),
                     'workbook': os.path.relpath(book, ROOT), 'fair': fair,
                     'report_bytes': os.path.getsize(report),
                     'workbook_bytes': os.path.getsize(book)})
    if not rows:
        problems.append('the queue is EMPTY and that is not a clean result — no calibrated '
                        'name produced a stageable pair [R-ENF-04]')
    if check_only:
        return rows, problems
    if os.path.isdir(QUEUE):
        shutil.rmtree(QUEUE)
    for r in rows:
        d = os.path.join(QUEUE, r['ticker'])
        os.makedirs(d)
        for k in ('report', 'workbook'):
            src = os.path.join(ROOT, r[k])
            shutil.copy2(src, os.path.join(d, os.path.basename(src)))
    json.dump({'_': 'Staged for a SINGLE BATCH PUBLICATION at the end of the fundamental-'
                    'calibration campaign, per instruction of 01-09-2026. Two files per '
                    'calibrated ticker: the valuation report as a PDF and the workbook. '
                    'assets/data.js deliberately still carries the PRE-CALIBRATION range for '
                    'every name below; publishing is a separate, explicitly-requested step.',
               'staged': len(rows), 'names': rows},
              open(os.path.join(QUEUE, 'MANIFEST.json'), 'w'), indent=1)
    return rows, problems


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true')
    a = ap.parse_args()
    rows, problems = build(check_only=a.check)
    print('calibrated names with a run directory: %d' % len(calibrated()))
    for r in rows:
        f = r['fair']
        print('  %-6s %-52s %6.0f KB' % (r['ticker'], os.path.basename(r['report']),
                                         r['report_bytes'] / 1024))
        print('  %-6s %-52s %6.0f KB   carries %s / %s / %s'
              % ('', os.path.basename(r['workbook']), r['workbook_bytes'] / 1024,
                 f['bear'], f['base'], f['full']))
    print()
    if problems:
        print('REFUSED — %d problem(s):' % len(problems))
        for p in problems:
            print('  ', p)
        sys.exit(1)
    print('publish queue OK — %d name(s), %d files, staged under engine/publish_queue/'
          % (len(rows), 2 * len(rows)))
