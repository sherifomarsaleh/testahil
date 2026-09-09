#!/usr/bin/env python3
"""[R-FCAL-01 AMENDED] — how far the valuation-input carry has actually got.

CLAUDE.md names this as debt rather than a blocker, and says it must be COUNTABLE RATHER
THAN REMEMBERED: taking the valuation-input block to more origins across the completed runs
is a copy out of filings each run has already parsed, so it is work with a rate. A rate
needs a denominator, and nothing in the repository produced one.

WHY THIS IS A MODULE AND NOT A NUMBER IN A DOCUMENT. Three things move underneath any count
of this: runs are added, origins are carried, and a block that could not be read yesterday
can be read today. A status sentence would rot [R-DOC-02]. So this reads the runs on disk.

IT ANCHORS ON THE RUN DIRECTORIES, the way fv_movement.py check does, so a run that stops
being fed FAILS rather than reporting clean. And it REFUSES per run rather than returning
zero: the valuation-input block has at least four different shapes across eleven runs, and a
reader that guesses a key finds nothing and reports it as a result [L-355]. Every shape it
accepts is named below; anything else is UNREADABLE and says so.
"""
import glob
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))

# The shapes actually committed, each read off a real file rather than assumed. Every one
# of them keys its origins by fiscal year under 'origins'; what differs is everything else.
INPUT_ORIGIN_KEYS = ('origins',)
# Where a run states the origins it holds and does not hold explicitly, that is better
# evidence than the length of a dict, and it is read in preference.
HELD_KEYS = ('origins_held',)
NOT_HELD_KEYS = ('origins_not_held', 'origins_blocked')

# The run's own origin set, in order of how directly it is stated.
SCORE_ORIGIN_KEYS = ('origins',)
SCORE_DERIVED_KEYS = ('by_era', 'detail', 'cells')


# A four-digit year inside a filing's name, bounded to the range this book covers. This is
# EVIDENCE OF SPAN AND NOT A DENOMINATOR: one filing carries comparative columns, so a run
# with a single FY2025 statement legitimately reaches six origins from it, and a run with
# 233 quarterly filings does not owe an origin per file. What the span shows is HEADROOM —
# where the paper on disk reaches years the block does not — and headroom is a judgement
# per run, which is exactly why it is reported beside the counts and never subtracted from
# them.
YEAR_RE = re.compile(r'(?<!\d)(20[0-2]\d)(?!\d)')


def _filing_year_span(d):
    """(earliest, latest, how many files) across the run's own filings directory."""
    years = set()
    n = 0
    for p in glob.glob(os.path.join(d, 'filings', '*')):
        if not os.path.isfile(p):
            continue
        n += 1
        years.update(int(y) for y in YEAR_RE.findall(os.path.basename(p)))
    if not years:
        return None, None, n
    return min(years), max(years), n


def _load(path):
    try:
        with open(path) as fh:
            return json.load(fh), None
    except (OSError, ValueError) as exc:
        return None, str(exc)


def _origins_from_scores(j):
    """(origins, how it was established) or (None, why not)."""
    for k in SCORE_ORIGIN_KEYS:
        v = j.get(k)
        if isinstance(v, list) and v:
            return sorted(str(x) for x in v), "scores.json['%s']" % k
        if isinstance(v, dict) and v:
            return sorted(map(str, v)), "scores.json['%s'] keys" % k
    for k in SCORE_DERIVED_KEYS:
        v = j.get(k)
        if isinstance(v, list) and v and isinstance(v[0], dict):
            got = {str(c[f]) for c in v for f in ('origin', 'origin_fy', 'fy') if f in c}
            if got:
                return sorted(got), "the origins named in scores.json['%s']" % k
    return None, 'no origin list and none derivable from by_era, detail or cells'


def survey(root=HERE):
    """One row per walk-forward run on disk. Never skips, never guesses."""
    rows = []
    for d in sorted(glob.glob(os.path.join(root, '*_walkforward'))):
        tk = os.path.basename(d).replace('_walkforward', '').upper()
        row = {'run': tk, 'dir': d, 'carried': None, 'scored': None,
               'held': None, 'not_held': None, 'route': None, 'note': ''}
        lo, hi, nfiles = _filing_year_span(d)
        row['span'] = (lo, hi)
        row['files'] = nfiles

        skip = os.path.join(d, 'skip_record.json')
        vi = os.path.join(d, 'valuation_inputs.json')
        sc = os.path.join(d, 'scores.json')

        if not os.path.exists(vi):
            row['note'] = 'NO valuation_inputs.json'
            if os.path.exists(skip):
                j, err = _load(skip)
                row['note'] += ' — run carries a skip_record.json'
            rows.append(row)
            continue

        j, err = _load(vi)
        if j is None:
            row['note'] = 'UNREADABLE valuation_inputs.json — %s' % err
            rows.append(row)
            continue

        for k in INPUT_ORIGIN_KEYS:
            v = j.get(k)
            if isinstance(v, dict) and v:
                row['carried'] = sorted(map(str, v))
                row['route'] = "valuation_inputs.json['%s'] keys" % k
                break
        if row['carried'] is None:
            row['note'] = ('UNREADABLE — no origins dict. Keys present: %s'
                           % ', '.join(sorted(j)[:12]))
            rows.append(row)
            continue

        for k in HELD_KEYS:
            if isinstance(j.get(k), list):
                row['held'] = sorted(map(str, j[k]))
        for k in NOT_HELD_KEYS:
            v = j.get(k)
            if isinstance(v, (list, dict)) and v:
                row['not_held'] = sorted(map(str, v))

        if not os.path.exists(sc):
            row['note'] = ('no scores.json, so the run\'s own origin set is not stated and '
                           'the carry has no denominator')
            rows.append(row)
            continue
        s, err = _load(sc)
        if s is None:
            row['note'] = 'UNREADABLE scores.json — %s' % err
            rows.append(row)
            continue
        got, how = _origins_from_scores(s)
        if got is None:
            row['note'] = 'scores.json states no origin set — %s' % how
        else:
            row['scored'] = got
            row['note'] = how
        rows.append(row)
    return rows


def report(rows):
    out = []
    out.append('VALUATION-INPUT CARRY — [R-FCAL-01 AMENDED], read off the runs on disk')
    out.append('')
    out.append('%-7s %8s %8s %6s %-13s  %s'
               % ('run', 'carried', 'scored', 'files', 'paper spans', 'how the denominator was established'))
    out.append('%-7s %8s %8s %6s %-13s  %s'
               % ('-' * 7, '-' * 8, '-' * 8, '-' * 6, '-' * 13, '-' * 48))
    carried_t = scored_t = 0
    unreadable, no_denom = [], []
    for r in rows:
        c = len(r['carried']) if r['carried'] is not None else None
        s = len(r['scored']) if r['scored'] is not None else None
        if c is not None:
            carried_t += c
        if s is not None:
            scored_t += s
        if c is None:
            unreadable.append(r['run'])
        elif s is None:
            no_denom.append(r['run'])
        lo, hi = r.get('span', (None, None))
        span = '%d–%d' % (lo, hi) if lo else '—'
        out.append('%-7s %8s %8s %6s %-13s  %s'
                   % (r['run'], '—' if c is None else c, '—' if s is None else s,
                      r.get('files', 0), span, r['note'][:48]))
    out.append('')
    out.append('  %d origins carried against %d scored, across %d runs on disk.'
               % (carried_t, scored_t, len(rows)))
    if unreadable:
        out.append('  NO READABLE BLOCK (each is debt, not a pass): %s'
                   % ', '.join(unreadable))
    if no_denom:
        out.append('  BLOCK READ BUT NO DENOMINATOR — the carry cannot be scored on '
                   'these: %s' % ', '.join(no_denom))
    out.append('')
    out.append('  PAPER SPANS IS EVIDENCE, NOT A TARGET. A single filing carries comparative')
    out.append('  columns, so ABUK legitimately reaches six origins off one FY2025 statement,')
    out.append('  and SWDY does not owe an origin for each of 233 quarterly files. Where the')
    out.append('  span reaches years the block does not, that is HEADROOM to be ruled on per')
    out.append('  run — never a number to subtract.')
    out.append('')
    out.append('  A run missing from this table is a run that stopped being fed. The table '
               'is\n  anchored on the directories, so it cannot report clean by finding '
               'nothing.')
    return '\n'.join(out)


if __name__ == '__main__':
    print(report(survey()))
