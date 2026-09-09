#!/usr/bin/env python3
"""A DATE THE RECORD HOLDS MAY NOT BE TYPED AGAIN ANYWHERE ELSE.  [R-ENF-06]

THE FAILURE THIS EXISTS TO STOP, MEASURED RATHER THAN IMAGINED. On 09-09-2026 three
studies were re-issued and every one of them shipped with a date that had been written
down somewhere instead of read: PHAR's masthead said "Prepared 9 August 2026 · at the
close of 6 August 2026" on a September edition anchored to a September price; ARCC's
bibliography was headed 6 August; SWDY said 217/365 of a year to a 5-August anchor while
its model rolled 246 days to 3 September. Two negative controls broke the same way, one
naming an edition that had moved and one naming a study that had been fixed.

Every one was a one-line repair. The cost was never the repair — it was that each
defect only revealed itself when something downstream disagreed, roughly one per
twenty-minute CI cycle. A sweep found ONE HUNDRED AND THIRTY-NINE of them in two
minutes. That ratio is the whole argument for this file: the fix is cheap and serial
discovery is not.

WHAT IT CHECKS, AND WHAT IT DELIBERATELY DOES NOT. A study's record owns a small set of
dates — the edition, the study date, the price date, the as-of, the spot date. Those are
facts the record states, so re-typing one creates a second copy that drifts silently.
Every OTHER date in a study is a fact about the WORLD — the day a filing was audited,
the day a rate was published, the day an index was read — and those are properly typed,
because no record holds them and nothing can derive them. A first cut that flagged every
date literal fired 1,569 times across 275 files, almost all of it work that is right.
Per [R-COC-01] it was RE-POINTED rather than widened: only a literal that reproduces a
date the study's OWN record already carries is a finding.

RATCHET [R-ENF-02]: the 139 found on adoption day are listed with the study and the file
that carries each. They bind nothing forward — a NEW one fails the build — and the list
may only ever SHORTEN. Nothing here condemns a study for a date typed before this rule
existed; it stops the next one.

    python3 scripts/check_typed_dates.py            report and enforce
    python3 scripts/check_typed_dates.py --prune    shorten the list where it is clean
"""
import datetime as dt
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENGINE = os.path.join(ROOT, 'engine')
OUTSTANDING = os.path.join(ENGINE, 'build_depth_audit', 'typed_dates_outstanding.json')

MONTHS = ('January February March April May June July August September October '
          'November December').split()

#: the dates a study's own record OWNS. Re-typing one of these is the defect.
OWNED_KEYS = ('study_date', 'price_date', 'asof', 'edition_date', 'spot_date')


def written_forms(iso):
    """Every shape this repository writes a date in, for one ISO date."""
    try:
        d = dt.date.fromisoformat(str(iso)[:10])
    except (TypeError, ValueError):
        return []
    m = MONTHS[d.month - 1]
    return [d.strftime('%d-%m-%Y'), d.strftime('%d%m%Y'),
            '%d %s %d' % (d.day, m, d.year), '%d %s %d' % (d.day, m[:3], d.year)]


def owned_dates(numbers):
    """The dates this study's record states, by the key that states them."""
    meta = numbers.get('meta') or {}
    out = {}
    for k in OWNED_KEYS:
        v = meta.get(k) or numbers.get(k)
        if v:
            out[k] = v
    return out


def census():
    rows = []
    for nf in sorted(glob.glob(os.path.join(ENGINE, '*_study', 'study_numbers.json'))):
        sdir = os.path.dirname(nf)
        tk = os.path.basename(sdir)[:-len('_study')].upper()
        try:
            numbers = json.load(open(nf, encoding='utf-8'))
        except (OSError, ValueError) as exc:
            rows.append(dict(ticker=tk, state='unreadable', why=str(exc)[:60]))
            continue
        owned = owned_dates(numbers)
        if not owned:
            rows.append(dict(ticker=tk, state='no_dated_record'))
            continue
        want = {}
        for key, iso in owned.items():
            for form in written_forms(iso):
                want.setdefault(form, key)
        found = []
        for py in sorted(glob.glob(os.path.join(sdir, '*.py'))):
            # A COMMENT IS NOT A CLAIM THE DOCUMENT MAKES. Explaining in prose that a
            # date used to be typed is exactly what these repairs record, and flagging
            # that would punish the fix.
            body = '\n'.join(ln for ln in open(py, encoding='utf-8', errors='ignore')
                             if not ln.lstrip().startswith('#'))
            for form, key in want.items():
                if re.search(r"['\"][^'\"]*" + re.escape(form) + r"[^'\"]*['\"]", body):
                    found.append((os.path.basename(py), form, key))
        rows.append(dict(ticker=tk, state='read', owned=owned, found=sorted(set(found))))
    return rows


def load_ratchet():
    if not os.path.exists(OUTSTANDING):
        return {}
    return json.load(open(OUTSTANDING, encoding='utf-8')).get('outstanding', {})


def main(argv):
    prune = '--prune' in argv
    rat = load_ratchet()
    rows = census()
    read = [r for r in rows if r['state'] == 'read']

    print('TYPED DATES  [R-ENF-06]  a date the record holds is never typed again')
    print('   %d study record(s) examined · %d readable · %d literal(s) found'
          % (len(rows), len(read), sum(len(r['found']) for r in read)))

    # POPULATION-ANCHORED BOTH WAYS [R-ENF-04]: a sweep that read nothing is not a
    # clean sweep, and neither is one that found no study to read.
    if not rows:
        print('\nFAIL — no study record was examined at all. An empty result is not a '
              'clean result [R-ENF-04].')
        return 1
    if not read:
        print('\nFAIL — %d study record(s) exist and NONE was readable [R-ENF-04].'
              % len(rows))
        return 1

    fail, clean_now = [], []
    print()
    for r in sorted(read, key=lambda r: r['ticker']):
        tk = r['ticker']
        listed = set(tuple(x) for x in rat.get(tk, []))
        live = set(r['found'])
        if not live:
            if tk in rat:
                clean_now.append(tk)
            continue
        new = sorted(live - listed)
        mark = '%d listed' % len(listed) if listed else 'NEW'
        print('    %-11s %d literal(s)  [%s]' % (tk, len(live), mark))
        for fn, form, key in sorted(live)[:3]:
            print('                  %s carries %r, which the record states as %s'
                  % (fn, form, key))
        for fn, form, key in new:
            fail.append('%s: %s types %r, and the record already states it as %s'
                        % (tk, fn, form, key))
        if listed - live:
            clean_now.append('%s (%d of %d)' % (tk, len(listed - live), len(listed)))

    for tk in sorted(rat):
        if tk not in {r['ticker'] for r in read}:
            fail.append('the list names %s and no readable study record of that name '
                        'exists — the list is anchored on nothing [R-ENF-04]' % tk)

    if clean_now:
        print('\n  ENTRIES NOW CLEAN: %s' % ', '.join(str(c) for c in clean_now))
        if prune:
            keep = {}
            for r in read:
                if r['ticker'] in rat and r['found']:
                    keep[r['ticker']] = [list(x) for x in sorted(set(r['found'])
                                                                & set(tuple(y) for y in rat[r['ticker']]))]
            keep = {k: v for k, v in keep.items() if v}
            json.dump({'rule': 'R-ENF-06 a date the record holds is never typed again',
                       'outstanding': keep},
                      open(OUTSTANDING, 'w', encoding='utf-8'), indent=1)
            print('  --prune: list shortened to %d study/studies, %d literal(s)'
                  % (len(keep), sum(len(v) for v in keep.values())))
        else:
            print('  run with --prune to shorten the list (it may only ever SHORTEN)')

    if fail:
        print('\nFAIL — %d new typed date(s):' % len(fail))
        for f in fail[:20]:
            print('  - ' + f)
        print('\nRead it from the record instead. A date written in two places is two '
              'facts, and one of them goes stale without anything noticing.')
        return 1
    print('\nOK — no study types a date its own record already states, beyond the '
          'listed ones.')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
