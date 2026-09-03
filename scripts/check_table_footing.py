#!/usr/bin/env python3
"""[R-ENF-01] Every total a reader sees is reproducible from the rows printed above it.

WHY THIS EXISTS. Three defects were found in ARCC on 03-Sep-2026 by rendering the delivered
PDF and reading it page by page. All three were the same shape — a table printing components
and a figure that does not follow from them — and all three sat in a document that had
already passed the recalculation gate (919 of 919 formula cells), the prose-figure check
(533 figures, none unmatched), the external-reader scrub and the table-column audit.

THE REASON EVERY EXISTING GATE WAS BLIND IS EXACT AND WORTH STATING, because it is a
property of those gates rather than an oversight in them. The recalculation gate reconciles
the model TO ITSELF, so a correct model passes however wrong the page is. prose_figures
matches each figure against the model's own numbers, and every figure in all three tables
was computed and individually correct — the defect lived in the RELATIONSHIP BETWEEN
figures, which no per-figure check can see. The table audit measures column widths. Nothing
in this repository was asking whether a reader could add up what was printed.

WHY IT IS PER-STUDY-DECLARED RATHER THAN A BOOK-WIDE ARITHMETIC BAR, and this was MEASURED
before it was decided. Run book-wide with no declarations, the instrument flags 15% of all
tables in the latest editions. Two false-positive classes account for nearly all of it and
one of them is IRREDUCIBLE: a row labelled "Total equity" listed AMONG line items in a
summary balance sheet is structurally indistinguishable from a roll-up, and so is a driver
named "Blended ARPU" in a sensitivity grid. A gate firing on one table in seven is the
permanently-red check [R-ENF-02] forbids and the check everyone learns to ignore. So the
shared instrument does the arithmetic and each study declares its own exceptions WITH
REASONS, which is exactly the architecture prose_figures uses and for exactly the same
reason: a shared instrument beats a good local one, and the judgement a script cannot make
is the one the study signs for.

TWO THINGS THIS DELIBERATELY DOES NOT DO. It does not treat the presence of the script as
conformance — it RUNS it, because a green tick on a red result is the worst outcome and is
case 2 of the negative control. And --measure prints the book-wide advisory, which is NEVER
a threshold, for the same reason check_prose_figures' advisory is not: an undeclared study
cannot be told apart from a defective one by a number.

Ratcheted [R-ENF-02] (may only SHORTEN, --prune), population-anchored [R-ENF-04] (a run that
examined zero studies FAILS, and every listed ticker must resolve on disk).
"""
import argparse
import glob
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RATCHET = os.path.join(ROOT, 'engine', 'build_depth_audit', 'footing_outstanding.json')
DATE_RX = re.compile(r'(\d{2})-(\d{2})-(\d{4})')


def studies():
    return sorted(glob.glob(os.path.join(ROOT, 'engine', '*_study')))


def ticker(d):
    return os.path.basename(d)[:-6].upper()


def load_ratchet():
    if not os.path.exists(RATCHET):
        return {}
    return json.load(open(RATCHET))


def latest_docs(d):
    """The LATEST edition of each delivered document kind. A superseded edition is not
    delivered, and holding one to today's standard would make the ratchet grow."""
    best = {}
    for f in glob.glob(os.path.join(d, '*.docx')):
        b = os.path.basename(f)
        if b.startswith('~$'):
            continue
        m = DATE_RX.search(b)
        key = 'BIB' if 'Bibliograph' in b else 'STUDY'
        k = (m.group(3), m.group(2), m.group(1)) if m else ('0', '0', '0')
        if key not in best or k > best[key][0]:
            best[key] = (k, f)
    return [v[1] for v in best.values()]


def measure():
    """The book-wide advisory. NEVER a bar — see the module docstring."""
    sys.path.insert(0, os.path.join(ROOT, 'engine'))
    import table_footing as TF
    import docx
    tot_t = tot_p = 0
    for d in studies():
        for p in latest_docs(d):
            try:
                doc = docx.Document(p)
            except Exception:
                continue
            for tbl in doc.tables:
                rows = TF.grid(tbl)
                if len(rows) < 3:
                    continue
                tot_t += 1
                tot_p += len(TF.check_table(rows))
    pct = tot_p / tot_t * 100 if tot_t else 0.0
    print(f'ADVISORY (never a bar): {tot_t} tables in the latest editions, {tot_p} totals '
          f'not reproducible column-wise, {pct:.1f}%. An UNDECLARED study cannot be told '
          f'apart from a defective one by this number, which is the argument FOR the '
          f'per-study declaration rather than a substitute for it.')
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--measure', action='store_true')
    ap.add_argument('--prune', action='store_true')
    a = ap.parse_args()
    if a.measure:
        return measure()

    rat = load_ratchet()
    allowed = set(rat.get('outstanding', []))
    ds = studies()
    if not ds:
        print('FAIL — examined zero studies; an empty result is not a clean result '
              '[R-ENF-04]')
        return 1

    on_disk = {ticker(d) for d in ds}
    stranded = sorted(allowed - on_disk)
    if stranded:
        print(f'FAIL — ratchet names studies that do not resolve on disk: {stranded} '
              f'[R-ENF-04]')
        return 1

    red, green, missing, examined_any = [], [], [], False
    for d in ds:
        tk = ticker(d)
        script = os.path.join(d, 'footing_check.py')
        if not os.path.exists(script):
            missing.append(tk)
            continue
        examined_any = True
        r = subprocess.run([sys.executable, script], cwd=d, capture_output=True, text=True)
        tail = (r.stdout or r.stderr).strip().splitlines()
        line = tail[-1] if tail else '(no output)'
        (green if r.returncode == 0 else red).append((tk, line))

    print('STUDIES WITH A FOOTING CHECK:')
    for tk, line in green:
        print(f'  [ok  ] {tk:12s} {line}')
    for tk, line in red:
        print(f'  [RED ] {tk:12s} {line}')
    if missing:
        print(f'\nNO FOOTING CHECK YET ({len(missing)}): {", ".join(sorted(missing))}')

    if a.prune:
        keep = sorted(set(missing) | {tk for tk, _ in red})
        grown = sorted(set(keep) - allowed)
        if grown:
            print(f'\nREFUSING TO PRUNE — the list would GROW by {grown}. A ratchet may '
                  f'only ever SHORTEN [R-ENF-02].')
            return 1
        rat['outstanding'] = keep
        json.dump(rat, open(RATCHET, 'w'), indent=2)
        print(f'\npruned: {len(allowed)} -> {len(keep)}')
        return 0

    if not examined_any and not missing:
        print('FAIL — examined nothing [R-ENF-04]')
        return 1

    new_red = [tk for tk, _ in red if tk not in allowed]
    new_missing = [tk for tk in missing if tk not in allowed]
    if new_red or new_missing:
        if new_red:
            print(f'\nFAIL — NEW red study: {sorted(new_red)}')
        if new_missing:
            print(f'\nFAIL — study with no footing check and no ratchet entry: '
                  f'{sorted(new_missing)}')
        return 1
    print(f'\nOK — no new violations. {len(green)} studies check their totals; '
          f'{len(allowed)} outstanding on the ratchet, which may only SHORTEN.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
