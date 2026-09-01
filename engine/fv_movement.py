"""The fair-value movement half of the Fundamental Analysis Calibration Register.

WHAT THIS EXISTS TO PREVENT.  The campaign's whole point is new-versus-old fair
value, and the campaign is also the one sanctioned thing that MOVES
TICKERS.{TK}.fair.  So the moment a name is rebuilt, its old fair value is gone
from assets/data.js and cannot be recovered from the file that held it.  The
old number therefore has to be frozen BEFORE the run starts, in a record that
is not the thing being changed -- the same rule as the as-of stamps and the
band record: A FILE THAT STATES A FACT WHICH MOVES MUST NOT BE THE THING THAT
REMEMBERS IT.

data.js carries fair{bear,base,full} with NO date and NO standard stamp, so
there is no way to reconstruct after the fact when a superseded fair value was
struck or what method produced it.  snapshot() captures that, once, per name.

APPEND-ONLY, like the ledgers.  A baseline may not be re-captured and a
delivered movement may not be retro-edited; a re-run appends an edition rather
than overwriting one.  The generated register is rebuilt wholesale from this
JSON and is never hand-edited.

    python3 engine/fv_movement.py snapshot TICKER      before the run starts
    python3 engine/fv_movement.py record   TICKER ...  after the study delivers
    python3 engine/fv_movement.py build                regenerate the register
    python3 engine/fv_movement.py check                gate: runs vs records
"""

import json
import os
import sys
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENGINE = os.path.join(ROOT, 'engine')
STORE = os.path.join(ENGINE, 'fv_movement.json')
REGISTER = os.path.join(ENGINE, 'Fundamental_Calibration_FV_Register.md')

LEGS = ('bear', 'base', 'full')
SCOPES = ('full', 'light', 'skip')


def _load():
    if not os.path.exists(STORE):
        return {'entries': {}}
    return json.load(open(STORE, encoding='utf-8'))


def _save(d):
    json.dump(d, open(STORE, 'w', encoding='utf-8'), indent=1, sort_keys=True)
    open(STORE, 'a', encoding='utf-8').write('\n')


def _queue_row(ticker):
    sys.path.insert(0, ENGINE)
    import campaign_queue as cq
    queue, _, current, _ = cq.build_queue()
    for q in queue:
        if q['ticker'] == ticker:
            return q, current
    raise SystemExit('FATAL: %r is not in the campaign queue. Run '
                     'campaign_queue.py to see the 90 names it covers -- a '
                     'ticker that is not there is either metals or a typo.'
                     % ticker)


def snapshot(ticker, when=None, unrecoverable=None):
    """Freeze the pre-campaign fair value.  Once, before the run touches it.

    `unrecoverable` declares, with a reason, that the pre-campaign number
    cannot be established -- the run already happened, or the history that held
    it is outside this clone.  It is recorded as absent rather than filled in
    with whatever data.js holds today, because a baseline read AFTER the run is
    not a baseline, and a movement computed against it would be a fabricated
    zero.  This is the declared-exception ratchet, not an escape hatch: the
    list may only ever shorten."""
    sys.path.insert(0, ENGINE)
    import campaign_queue as cq
    tickers, _ = cq.load_register()
    if ticker not in tickers:
        raise SystemExit('FATAL: %r carries no entry in assets/data.js.' % ticker)
    row, _ = _queue_row(ticker)
    d = _load()
    if ticker in d['entries']:
        raise SystemExit('FATAL: %s already has a frozen baseline (captured %s). '
                         'A baseline is a historical fact and is append-only -- '
                         'it is never re-captured, because the second capture '
                         'would read a fair value this campaign itself moved.'
                         % (ticker, d['entries'][ticker]['baseline']['captured']))

    t = tickers[ticker]
    fair = t.get('fair') or {}
    missing = [k for k in LEGS if fair.get(k) is None]
    if missing and not unrecoverable:
        raise SystemExit('FATAL: %s has no %s fair value to compare against.'
                         % (ticker, '/'.join(missing)))
    d['entries'][ticker] = {
        'ticker': ticker, 'market': row['market'], 'exchange': row['exchange'],
        'tier': row['tier'], 'ccy': t.get('ccy'),
        'baseline': {
            'unrecoverable': unrecoverable,
            'fair': None if unrecoverable else {k: fair[k] for k in LEGS},
            'spot': t.get('spot'), 'spot_date': t.get('spotDate'),
            'built_to': row['built_to'],
            'captured': when or date.today().isoformat(),
            'note': 'assets/data.js carries no date or standard stamp on fair{}; '
                    'built_to is the study standard, not the strike date of '
                    'these numbers, which is not recoverable.',
        },
        'editions': [],
    }
    _save(d)
    if unrecoverable:
        print('%s baseline recorded as UNRECOVERABLE: %s' % (ticker, unrecoverable))
    else:
        print('%s baseline frozen: bear %s / base %s / full %s %s (built to %s)'
              % (ticker, fair['bear'], fair['base'], fair['full'],
                 t.get('ccy') or '', row['built_to']))
    return 0


def record(ticker, bear, base, full, scope, origins, lessons, when=None):
    """Append this run's delivered fair value beside the frozen baseline."""
    if scope not in SCOPES:
        raise SystemExit('FATAL: scope must be one of %s.' % ', '.join(SCOPES))
    d = _load()
    if ticker not in d['entries']:
        raise SystemExit('FATAL: %s has no frozen baseline. Snapshot BEFORE the '
                         'run, never after -- once the study has written '
                         'data.js the old fair value is gone and old-versus-new '
                         'cannot be computed at all.' % ticker)
    e = d['entries'][ticker]
    prev = e['editions'][-1]['fair'] if e['editions'] else e['baseline']['fair']
    new = {'bear': float(bear), 'base': float(base), 'full': float(full)}
    if not new['bear'] <= new['base'] <= new['full']:
        raise SystemExit('FATAL: %s fair range is not ordered bear <= base <= '
                         'full (%s). A range that crosses itself is an input '
                         'error, not a finding.' % (ticker, new))
    base0 = e['baseline']['fair']
    e['editions'].append({
        'edition': len(e['editions']) + 1,
        'delivered': when or date.today().isoformat(),
        'scope': scope, 'origins': origins,
        'fair': new,
        'vs_baseline_pct': ({k: round(100.0 * (new[k] - base0[k]) / base0[k], 1)
                             for k in LEGS} if base0 else None),
        'vs_previous_pct': ({k: round(100.0 * (new[k] - prev[k]) / prev[k], 1)
                             for k in LEGS} if prev else None),
        'lessons': sorted(lessons),
    })
    _save(d)
    ed = e['editions'][-1]
    if ed['vs_baseline_pct'] is None:
        print('%s edition %d recorded: base %s. No movement computed -- the '
              'baseline is unrecoverable (%s).'
              % (ticker, ed['edition'], new['base'], e['baseline']['unrecoverable']))
    else:
        m = ed['vs_baseline_pct']
        print('%s edition %d recorded: base %s -> %s (%+.1f%% vs baseline); '
              'bear %+.1f%%, full %+.1f%%; lessons %s'
              % (ticker, ed['edition'], base0['base'], new['base'],
                 m['base'], m['bear'], m['full'],
                 ', '.join(sorted(lessons)) or '(none)'))
    return 0


def build():
    """Regenerate the register wholesale.  Never hand-edited."""
    d = _load()
    sys.path.insert(0, ENGINE)
    import campaign_queue as cq
    queue, excluded, current, total = cq.build_queue()
    done = [q for q in queue if q['ticker'] in d['entries']
            and d['entries'][q['ticker']]['editions']]

    L = []
    L.append('# Fundamental Analysis Calibration Register — fair-value movement')
    L.append('')
    L.append('**GENERATED** by `engine/fv_movement.py` from `engine/fv_movement.json`. '
             'Never hand-edited. Rebuilt wholesale at every run.')
    L.append('')
    L.append('This is the fair-value half of the register. The lessons half is '
             '`engine/Lessons_Register.md`, generated from `engine/lessons_register.py`; '
             'the two are cross-referenced by lesson id and never duplicated.')
    L.append('')
    L.append('Internal record. No rating, no price target, no recommendation — a range '
             'and what moved it. Nothing here reaches the live site.')
    L.append('')
    L.append('| | |')
    L.append('|---|---|')
    L.append('| covered names | %d |' % total)
    L.append('| in the campaign queue | %d |' % len(queue))
    L.append('| excluded (metals — no issuer, no statements, no drivers) | %d |' % len(excluded))
    L.append('| baselines frozen | %d |' % len(d['entries']))
    L.append('| fair values re-derived | %d |' % len(done))
    L.append('| live study standard | %s |' % current)
    L.append('')
    if not done:
        L.append('No name has been re-derived yet. An empty register is reported as '
                 'empty rather than as complete — an absent result is not a clean one.')
    for market, _pref, label in cq.MARKET_ORDER:
        rows = [q for q in queue if q['market'] == market
                and q['ticker'] in d['entries'] and d['entries'][q['ticker']]['editions']]
        if not rows:
            continue
        L.append('')
        L.append('## %s' % label)
        L.append('')
        L.append('| # | name | ccy | scope | old base | new base | base | bear | full | built to → | lessons |')
        L.append('|---|---|---|---|---|---|---|---|---|---|---|')
        for q in rows:
            e = d['entries'][q['ticker']]
            ed = e['editions'][-1]
            b = e['baseline']
            mv = ed['vs_baseline_pct']
            L.append('| %d | %s | %s | %s | %s | %s | %s | %s | %s | %s → %s | %s |'
                     % (q['position'], q['ticker'], e['ccy'] or '', ed['scope'],
                        b['fair']['base'] if b['fair'] else 'unrecoverable',
                        ed['fair']['base'],
                        '%+.1f%%' % mv['base'] if mv else 'n/a',
                        '%+.1f%%' % mv['bear'] if mv else 'n/a',
                        '%+.1f%%' % mv['full'] if mv else 'n/a',
                        b['built_to'], current, ', '.join(ed['lessons']) or '—'))
    L.append('')
    L.append('Percentages are the delivered edition against the **frozen pre-campaign '
             'baseline**, captured before the run touched `assets/data.js`. Where a name '
             'carries more than one edition, `vs_previous_pct` in the JSON holds the '
             'edition-on-edition move.')
    L.append('')
    open(REGISTER, 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    print('wrote %s — %d re-derived of %d queued' % (REGISTER, len(done), len(queue)))
    return 0


def check():
    """Every run directory on disk has a record, and every record a run.

    Anchored on the run directories, not on this file: a register that stopped
    being fed must FAIL, not report clean [R-ENF-04]."""
    d = _load()
    runs = {x[:-len('_walkforward')].upper()
            for x in os.listdir(ENGINE)
            if x.endswith('_walkforward') and os.path.isdir(os.path.join(ENGINE, x))}
    sys.path.insert(0, ENGINE)
    import campaign_queue as cq
    queue, _, _, _ = cq.build_queue()
    inq = {q['ticker'] for q in queue}
    fails = []
    if not runs:
        fails.append('no walk-forward run directories found at all — either the '
                     'campaign has not started or this check is looking in the '
                     'wrong place; an empty result is not a clean result')
    for tk in sorted(runs & inq):
        e = d['entries'].get(tk)
        if not e:
            fails.append('%s has a walk-forward run on disk and no frozen '
                         'baseline — its old fair value may already be '
                         'unrecoverable' % tk)
        elif not e['editions']:
            fails.append('%s has a baseline and a run but no delivered fair '
                         'value recorded' % tk)
    for tk in sorted(d['entries']):
        if tk not in runs:
            fails.append('%s carries a record with no walk-forward run '
                         'directory behind it' % tk)
    print('run directories: %d   in queue: %d   records: %d'
          % (len(runs), len(runs & inq), len(d['entries'])))
    for f in fails:
        print('  FAIL  %s' % f)
    if fails:
        return 1
    print('  [ok]   every run in the queue has a frozen baseline and a '
          'recorded fair value')
    return 0


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 0
    cmd = argv[1]
    if cmd == 'snapshot':
        a = argv[2:]
        why = a[a.index('--unrecoverable') + 1] if '--unrecoverable' in a else None
        return snapshot(a[0].upper(), unrecoverable=why)
    if cmd == 'record':
        a = argv[2:]
        def opt(flag, dflt=None):
            return a[a.index(flag) + 1] if flag in a else dflt
        lessons = [x for x in (opt('--lessons', '') or '').split(',') if x]
        return record(a[0].upper(), opt('--bear'), opt('--base'), opt('--full'),
                      opt('--scope', 'full'), opt('--origins', ''), lessons)
    if cmd == 'build':
        return build()
    if cmd == 'check':
        return check()
    print(__doc__)
    return 1


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
