#!/usr/bin/env python3
"""[R-ENF-01] A STUDY THAT PRINTS A WATERFALL RUNS THE WATERFALL CHECK.

A table that names its operations in words — "Plus net cash", "Less depreciation and
amortisation", "Add back the impairment" — is giving a reader instructions, and nothing in
this repository asked whether following them arrives where the page says. table_footing
tests rows whose LABEL DECLARES A TOTAL, and a waterfall never says "total"; prose_figures
matches each figure against the model, and every figure in every one of the defects found
on 04-Sep-2026 was computed and individually correct. THE DEFECT LIVES IN THE RELATIONSHIP
BETWEEN THE ROWS, which is what nothing inspecting figures one at a time can see.

WHY THE CHECK IS ON THE BUILDER AND NOT ON THE PAGE. The page-side reading was built first
and run over the whole book twice; it flags 30.7% of the tables that carry an operator row,
and the residue is irreducible because a statement mixes labelled and unlabelled steps and
the page cannot say which is which. engine/table_residual.py carries that measurement in
full. The builder knows the anchor because it put it there, so the check moves to where the
answer is knowable — the [R-COC-01] lesson applied to an instrument's own first draft.

WHAT THIS GATE DOES, and it is the check_sweep_module shape exactly:
    THE POPULATION COMES FROM THE DELIVERED DOCUMENTS, not from the code — every study
    whose latest-edition documents contain a table with an operator-labelled row.
    THE REQUIREMENT IS ON THE CODE — that study must IMPORT engine/table_residual.py and
    must CALL waterfall(). Importing a module for its helpers and never running its
    assertion is declaration without execution, one level up, and check_sweep_module was
    written after exactly that.
    THE GATE DOES NOT RE-DERIVE THE ARITHMETIC ITSELF. A second implementation of the same
    claim is the [R-ENF-03] species; the builder's own call fires at every build, which is
    when the study is rebuilt anyway.

Ratcheted [R-ENF-02]: every study printing a waterfall today without the call is listed and
allowed, the build breaks on a NEW one, and the list may only ever SHORTEN (--prune).
Population-anchored [R-ENF-04] BOTH WAYS: a run that examined zero documents FAILS, and so
does one that found zero waterfall tables across present documents — the distinction an
absent answer hides behind.
"""
import argparse
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'engine'))
import table_residual as TR                                            # noqa: E402

RATCHET = os.path.join(ROOT, 'engine', 'build_depth_audit', 'waterfall_outstanding.json')
DATE = re.compile(r'(\d{2})-(\d{2})-(\d{4})')
CALL = re.compile(r'\bwaterfall\s*\(')
IMPORT = re.compile(r'\b(?:import\s+table_residual|from\s+table_residual\s+import)\b')


def latest(paths):
    """The LATEST edition of each document by DATE, never by string sort [L-067]."""
    keep = {}
    for p in paths:
        b = os.path.basename(p)
        if b.startswith('~$'):
            continue
        m = DATE.search(b)
        key, stamp = DATE.sub('', b), (m.group(3) + m.group(2) + m.group(1)) if m else ''
        if key not in keep or stamp > keep[key][0]:
            keep[key] = (stamp, p)
    return sorted(v[1] for v in keep.values())


def waterfall_tables(path):
    """(table index, first operator label) for every table in one document that instructs."""
    from docx import Document
    out = []
    for n, t in enumerate(Document(path).tables):
        rows = TR.grid(t)
        labels = [(r[0] if r else '') or '' for r in rows]
        for i, lab in enumerate(labels):
            # a lone operator word with no figures beside it is a section heading, not a
            # step, and a header row is never a step
            if i and TR.op_of(lab) and any(TR.parse_cell(c) is not None
                                           for c in rows[i][1:]):
                out.append((n, lab.strip()[:60]))
                break
    return out


def survey():
    """Every study, what its documents instruct, and whether its code runs the check."""
    rows, docs_seen, tables_seen = [], 0, 0
    for d in sorted(glob.glob(os.path.join(ROOT, 'engine', '*_study'))):
        tk = os.path.basename(d).replace('_study', '').upper()
        found = []
        for p in latest(glob.glob(os.path.join(d, '*.docx'))):
            docs_seen += 1
            try:
                hits = waterfall_tables(p)
            except Exception as exc:                       # a document that will not open
                rows.append((tk, 'UNREADABLE', os.path.basename(p), str(exc)[:80]))
                continue
            tables_seen += len(hits)
            found += [(os.path.basename(p), n, lab) for n, lab in hits]
        if not found:
            continue
        src = ''
        for f in sorted(glob.glob(os.path.join(d, '*.py'))):
            try:
                src += open(f, encoding='utf-8').read()
            except OSError:
                continue
        if not IMPORT.search(src):
            rows.append((tk, 'NO IMPORT', found[0][0], '%d waterfall table(s); first says '
                         '%r' % (len(found), found[0][2])))
        elif not CALL.search(src):
            rows.append((tk, 'NOT CALLED', found[0][0], 'imports table_residual and never '
                         'calls waterfall() — declaration without execution'))
        else:
            rows.append((tk, 'OK', found[0][0], '%d waterfall table(s)' % len(found)))
    return rows, docs_seen, tables_seen


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--prune', action='store_true',
                    help='rewrite the ratchet with the studies that still fail; it may '
                         'only ever SHORTEN')
    a = ap.parse_args()

    rows, docs, tables = survey()
    allowed = (set(json.load(open(RATCHET))['outstanding'])
               if os.path.exists(RATCHET) else set())

    if docs == 0:
        print('FAIL — examined zero documents; the population is empty, which is not a '
              'clean result but an absent one')
        return 1
    if tables == 0:
        print('FAIL — read %d document(s) and found zero tables that instruct a reader. '
              'Either every waterfall in the book has gone or the reader is broken; both '
              'are findings and neither is clean.' % docs)
        return 1
    on_disk = {os.path.basename(d).replace('_study', '').upper()
               for d in glob.glob(os.path.join(ROOT, 'engine', '*_study'))}
    missing = sorted(allowed - on_disk)
    if missing:
        print('FAIL — the ratchet names studies that do not exist on disk: %s'
              % ', '.join(missing))
        return 1

    bad = [r for r in rows if r[1] != 'OK']
    new = [r for r in bad if r[0] not in allowed]

    print('%d document(s) read, %d table(s) instructing a reader, %d study/studies printing '
          'one' % (docs, tables, len(rows)))
    for tk, state, doc, note in rows:
        mark = '>> ' if (state != 'OK' and tk not in allowed) else '   '
        tag = state if state == 'OK' else (
            '%s (ratchet)' % state if tk in allowed else state)
        print('%s%-12s %-22s %-44s %s' % (mark, tk, tag, doc[:44], note[:74]))

    if a.prune:
        keep = sorted({r[0] for r in bad})
        if set(keep) - allowed and allowed:
            print('REFUSED — --prune may only ever SHORTEN the ratchet; %s would be added'
                  % ', '.join(sorted(set(keep) - allowed)))
            return 1
        json.dump({'rule': 'R-ENF-01 / waterfall assertions',
                   'note': 'Studies printing a table that instructs a reader whose builder '
                           'does not run engine/table_residual.waterfall(). May only ever '
                           'SHORTEN. Each closes at its study\'s next re-issue.',
                   'outstanding': keep}, open(RATCHET, 'w'), indent=1)
        print('ratchet rewritten with %d entr%s'
              % (len(keep), 'y' if len(keep) == 1 else 'ies'))
        return 0

    if new:
        print('\nFAIL — %d study/studies print a table that instructs a reader and never '
              'check that following it arrives at the printed answer:' % len(new))
        for tk, state, doc, note in new:
            print('   %-12s %-12s %s' % (tk, state, note))
        return 1
    print('\nOK — no new violations. %d stud%s on the ratchet, which may only SHORTEN.'
          % (len(allowed), 'y' if len(allowed) == 1 else 'ies'))
    return 0


if __name__ == '__main__':
    sys.exit(main())
