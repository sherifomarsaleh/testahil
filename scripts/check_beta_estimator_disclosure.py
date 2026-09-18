#!/usr/bin/env python3
"""[R-BETA-05] A DOCUMENT THAT QUOTES THE BETA DIAGNOSTICS NAMES THE ESTIMATOR.

Adopted 18-09-2026 on an outside forensic audit of a delivered study. It applied the
textbook single-regressor identity

    t^2 = R^2 (n - 2) / (1 - R^2)

to the four diagnostics that study prints -- beta 1.4718, standard error 0.185, R-squared
32.6%, n 251 -- and found them mutually inconsistent: the printed (t, n) pair implies an
R-squared of 20.30%, the printed (R-squared, n) pair implies a standard error of 0.1341,
and the two are consistent only at n = 133 against a printed 251. Its arithmetic is exact
and its conclusion -- "these cannot come from one regression" -- is CORRECT.

They do not come from one regression. beta_regression.own_stock_beta() runs a DIMSON
estimator: the stock's weekly return on the index's return in the same week and in the week
either side, beta the SUM of three coefficients, the standard error the square root of the
summed 3x3 covariance block, R-squared that of the whole model. The identity does not apply
and no delivered page said so.

THE ESTIMATOR IS SOUND AND THE DISCLOSURE IS NOT. That distinction is the whole rule, and
it is [R-COC-02]'s general lesson on a different quantity: a check that fires on correct
work has usually found a construction nobody wrote down, and the repair is to make the
construction DECLARABLE and then require the declaration -- never to widen the check until
the honest case passes, and never to change the estimator so that a reader's shortcut
happens to work.

WHAT IT CHECKS, AND THE CONDITION IS DELIBERATELY NARROW: only where a study's committed
record says the estimator is Dimson AND the delivered document QUOTES the diagnostics a
reader would test -- a standard error, or explained variation beside the beta. A study that
quotes a beta and no diagnostics has given a reader nothing to test and is not in scope; a
study that names the estimator anywhere in the document passes, wherever it names it,
because this is a disclosure test rather than a placement test.

THE RECORD IS READ THROUGH NAMED ADAPTERS, NOT GUESSED. Two shapes exist in this book: a
flat record whose `dimson` is a BOOLEAN, and one whose `dimson` is a SUB-RECORD carrying the
coefficients and its own note. A reader that guesses finds the sub-dict, reads no `beta`
beside it, and reports the study as carrying no beta at all -- which is exactly what the
first measurement of this population did, and is [L-355] landing on the instrument written
to close it. Both shapes are named below and an UNRECOGNISED shape is RED, never skipped.

POPULATION-ANCHORED [R-ENF-04] BOTH WAYS: a run that examines zero study directories fails,
and so does one that reads zero beta records across directories that are present -- a reader
that stopped resolving records looks exactly like a book with no betas in it.

RATCHETED [R-ENF-02] with each entry carrying its MEASUREMENT rather than a bare name, and
the list may only ever SHORTEN. The exemplar is ON it, consciously, in the commit that
adopts this: per [R-ENF-01 EXTENDED 04-Sep-2026] a new standard is either MET by the
exemplar or ADDED to its list deliberately, the choice being made either way and the only
question being whether anybody sees it. Bringing a published exemplar to a new standard is a
re-issue, so it is added -- and check_exemplar_debt.py will say so.
"""
import json, glob, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RATCHET = os.path.join(ROOT, 'engine', 'build_depth_audit', 'beta_estimator_outstanding.json')

# The diagnostics a reader can test. Both must be findable near a beta for the study to be
# in scope; either alone is a number without an identity to check it against.
QUOTES_DIAG = (re.compile(r'standard error', re.I),
               re.compile(r'explain(?:ing|s|ed)?\s+\d+[\d.,]*\s*%\s+of the variation', re.I),
               re.compile(r'R.?squared', re.I))
# The estimator, named in any of the ways an outside reader would recognise. NOT a word list
# standing in for the concept: each of these names the construction rather than describing it.
NAMES_EST = re.compile(r'[Dd]imson|week either side|lead and lag|sum[- ]beta|'
                       r'sum of (?:those )?three coefficients', re.I)


def read_beta_record(numbers):
    """Named adapters, one per committed shape. An unrecognised shape returns ('?', None)."""
    hits = []

    def walk(o):
        if isinstance(o, dict):
            # shape A -- flat record, `dimson` a boolean beside `beta`
            if 'beta' in o and 'dimson' in o and isinstance(o.get('dimson'), bool):
                hits.append(('flat', o))
                return
            # shape B -- `dimson` is a SUB-RECORD carrying the coefficients
            if 'dimson' in o and isinstance(o.get('dimson'), dict):
                hits.append(('nested', o))
                return
            # a record carrying `dimson` in ANY OTHER shape is UNRECOGNISED, never skipped.
            # The first draft fell through to the recursion here and returned "no beta
            # record", which reads exactly like a study that has none -- the absent answer
            # in a clean answer's clothes [R-ENF-04], inside the gate written to refuse it.
            # Its own negative control caught this on the first run.
            if 'dimson' in o:
                hits.append(('unknown', o))
                return
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)

    walk(numbers)
    if not hits:
        return (None, None)
    shape, rec = hits[0]
    if shape == 'unknown':
        return ('unknown', None)
    if shape == 'flat':
        return ('flat', bool(rec.get('dimson')))
    sub = rec['dimson']
    # a sub-record IS a Dimson estimate by construction -- it carries the coefficients
    return ('nested', bool(sub.get('coefficients') or sub.get('sum_beta') or sub.get('note')))


def latest_study_doc(d):
    cands = [f for f in glob.glob(os.path.join(d, '*.docx'))
             if 'Bibliograph' not in f and 'Sources' not in f and not
             os.path.basename(f).startswith('~$')]
    if not cands:
        return None

    def key(f):
        m = re.search(r'(\d{2})-(\d{2})-(\d{4})', os.path.basename(f))
        return (m.group(3), m.group(2), m.group(1)) if m else ('0', '0', '0')
    return max(cands, key=key)


def doc_text(f):
    from docx import Document
    d = Document(f)
    t = "\n".join(p.text for p in d.paragraphs)
    for tb in d.tables:
        for r in tb.rows:
            t += "\n" + " | ".join(c.text for c in r.cells)
    return t


def main(prune=False):
    ratchet = json.load(open(RATCHET)) if os.path.exists(RATCHET) else {'outstanding': {}}
    dirs = sorted(glob.glob(os.path.join(ROOT, 'engine', '*_study')))
    if not dirs:
        print('FAIL — zero study directories examined. The population resolver is broken, '
              'not the book. [R-ENF-04]')
        return 1

    read = 0
    problems, ok, unrecognised = [], [], []
    for sd in dirs:
        tk = os.path.basename(sd).replace('_study', '').upper()
        nj = os.path.join(sd, 'study_numbers.json')
        if not os.path.exists(nj):
            continue
        try:
            numbers = json.load(open(nj))
        except Exception as e:
            problems.append((tk, f'numbers file will not parse: {e}'))
            continue
        shape, is_dimson = read_beta_record(numbers)
        if shape is None:
            continue                      # no beta record: not in scope, not a failure
        read += 1
        if shape not in ('flat', 'nested'):
            unrecognised.append(tk)
            continue
        if not is_dimson:
            ok.append((tk, 'not a Dimson estimate'))
            continue
        doc = latest_study_doc(sd)
        if doc is None:
            ok.append((tk, 'no delivered study document'))
            continue
        t = doc_text(doc)
        quotes = sum(bool(p.search(t)) for p in QUOTES_DIAG)
        if quotes == 0:
            ok.append((tk, 'quotes no diagnostic a reader could test'))
            continue
        if NAMES_EST.search(t):
            ok.append((tk, 'names the estimator'))
            continue
        problems.append((tk, f'Dimson beta; the document quotes {quotes} of '
                             f'{len(QUOTES_DIAG)} testable diagnostics and names no estimator '
                             f'({os.path.basename(doc)})'))

    if read == 0:
        print('FAIL — %d study directories are present and ZERO beta records were read. '
              'A reader that stopped resolving records looks exactly like a book with no '
              'betas in it. [R-ENF-04]' % len(dirs))
        return 1

    print('BETA ESTIMATOR DISCLOSURE — [R-BETA-05]')
    print('examined %d study directories; read %d beta records' % (len(dirs), read))
    for tk, why in sorted(ok):
        print('   ok    %-13s %s' % (tk, why))
    for tk in sorted(unrecognised):
        print('   RED   %-13s committed beta record is in an unrecognised shape — a reader '
              'that guesses reports it as absent [L-355]' % tk)
    outstanding = ratchet.get('outstanding', {})
    listed = [p for p in problems if p[0] in outstanding]
    new = [p for p in problems if p[0] not in outstanding]
    for tk, why in sorted(listed):
        print('   known %-13s %s' % (tk, why))
    for tk, why in sorted(new):
        print('   NEW   %-13s %s' % (tk, why))

    if prune:
        still = {p[0] for p in problems} | set(unrecognised)
        kept = {k: v for k, v in outstanding.items() if k in still}
        dropped = sorted(set(outstanding) - set(kept))
        json.dump({'rule': '[R-BETA-05]', 'outstanding': kept}, open(RATCHET, 'w'), indent=1)
        print('\npruned: dropped %d (%s); the list may only ever SHORTEN'
              % (len(dropped), ', '.join(dropped) or 'none'))
        return 0

    for tk in outstanding:
        if tk not in {p[0] for p in problems} | set(unrecognised):
            print('   FAIL  %-13s is on the ratchet and no longer fails — run --prune' % tk)
            return 1
    if new or unrecognised:
        print('\nFAIL — %d new breach(es) and %d unrecognised record shape(s).'
              % (len(new), len(unrecognised)))
        return 1
    print('\nOK — no new breach. %d on the ratchet, which may only SHORTEN.' % len(listed))
    return 0


if __name__ == '__main__':
    sys.exit(main(prune='--prune' in sys.argv))
