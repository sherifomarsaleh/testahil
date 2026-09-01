"""Names the campaign examined, could not source documents for, and PARKED.

[R-CAMP-01]  DOCUMENT SUPPLY IS THE BINDING CONSTRAINT, NOT COMPUTE.

WHY THIS EXISTS.  The campaign's scope decision has three outcomes -- FULL,
LIGHT and SKIP -- and every one of them is a statement about THE ARCHIVE: how
many fiscal years the company has actually published.  None of them describes
the case that stopped the campaign at its first name: the archive is fine and
the DOCUMENTS CANNOT BE REACHED.  AMOC has published audited statements for
decades; amoc.com.eg, mist.egx.com.eg and disclosure.efsa.gov.eg are all
rejected at this container's gateway.

Recording that as SKIP -- "walk-forward not run, insufficient sourceable
history (2 years)" -- would be false in the specific way this protocol keeps
paying for: an ABSENT answer wearing the costume of a clean one [R-ENF-04].
The sentence would read as a fact about the company and would actually be a
fact about the network, and nothing in the register would ever distinguish
them again.  A SKIP is closed forever; a PARK reopens the moment the documents
arrive.

SO PARKING IS ITS OWN OUTCOME, AND IT IS NOT A SKIP AND NOT A DEFERRAL.
    SKIP    the company never published enough years.       Position CLOSED.
    PARK    it published them and we cannot reach them.     Position OPEN.

AND IT MUST NOT STALL THE CAMPAIGN.  Blocking the queue on one unreachable
host would reproduce the failure [R-CAL-01] was amended to close: an
unclearable gate that produced 66 unmerged PRs in seventeen days while
production went on publishing a month-old fit and said nothing.  A GATE WITH
NO RELEASE IS A STALL.  The release here is: record the park, name the exact
filings needed, move to the next name.

WHAT A PARK MAY NOT DO.  It may not create engine/{tk}_walkforward/ and it may
not freeze a fair-value baseline.  Both gates anchor on the run directories on
disk, so either one would turn them red for a run that is not happening -- and
a permanently red check is one everyone learns to ignore.  check() enforces
both exclusions rather than trusting the operator to remember them.

THE ATTEMPT LOG IS THE POINT, NOT THE REASON STRING.  "Could not get the
documents" is an assertion; a dated list of URLs with the status each returned
is evidence, and it is what lets the next session re-probe instead of
believing this one.  ARCC is the worked case for why that matters: CLAUDE.md
recorded arabiancementcompany.com as connect_rejected, and on 01-Sep-2026 it
answered 200 and served 175 filings.  WHEN A PROBE COMES BACK EMPTY THE FIRST
HYPOTHESIS IS THAT THE PROBE DID NOT RUN -- so every park carries what was
tried, when, and what came back, and re-probing is an ordinary step of
resuming rather than a favour to the sceptical.

    python3 engine/campaign_parked.py list
    python3 engine/campaign_parked.py check
    python3 engine/campaign_parked.py unpark TICKER --note "..."
"""

import json
import os
import sys
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENGINE = os.path.join(ROOT, 'engine')
STORE = os.path.join(ENGINE, 'campaign_parked.json')

REASONS = ('documents',)


def _load():
    if not os.path.exists(STORE):
        return {'entries': {}}
    return json.load(open(STORE, encoding='utf-8'))


def _save(d):
    json.dump(d, open(STORE, 'w', encoding='utf-8'), indent=1, sort_keys=True)
    open(STORE, 'a', encoding='utf-8').write('\n')


def _queue():
    sys.path.insert(0, ENGINE)
    import campaign_queue as cq
    queue, excluded, _, _ = cq.build_queue()
    return queue, excluded


def parked_tickers():
    """The set the queue skips.  Imported by campaign_queue -- keep it cheap
    and side-effect free."""
    return {k for k, v in _load()['entries'].items() if not v.get('unparked')}


def park(ticker, reason, attempts, documents, unpark_when, note=None, when=None):
    """Record a name as parked.  Attempts carry their OUTCOME, not just a URL."""
    ticker = ticker.upper()
    queue, _ = _queue()
    row = next((q for q in queue if q['ticker'] == ticker), None)
    if row is None:
        raise SystemExit('FATAL: %r is not in the campaign queue.' % ticker)
    if reason not in REASONS:
        raise SystemExit('FATAL: reason must be one of %r' % (REASONS,))
    if not attempts:
        raise SystemExit('FATAL: a park with no logged attempt is an assertion, '
                         'not evidence.')
    if not documents:
        raise SystemExit('FATAL: a park must name the exact documents needed, '
                         'or nobody can unblock it.')
    d = _load()
    d['entries'][ticker] = {
        'ticker': ticker, 'market': row['market'], 'exchange': row['exchange'],
        'position': row['position'], 'tier': row['tier'],
        'reason': reason,
        'parked': when or date.today().isoformat(),
        'attempts': attempts,
        'documents_needed': documents,
        'unpark_when': unpark_when,
        'note': note,
        'unparked': None,
    }
    _save(d)
    print('%s PARKED (%s) at queue position %d — %d attempt(s) logged, '
          '%d document(s) requested.'
          % (ticker, reason, row['position'], len(attempts), len(documents)))
    return 0


def unpark(ticker, note=None, when=None):
    ticker = ticker.upper()
    d = _load()
    e = d['entries'].get(ticker)
    if not e:
        raise SystemExit('FATAL: %s is not parked.' % ticker)
    if e.get('unparked'):
        raise SystemExit('FATAL: %s was already unparked on %s.'
                         % (ticker, e['unparked']['when']))
    e['unparked'] = {'when': when or date.today().isoformat(), 'note': note}
    _save(d)
    print('%s UNPARKED — it re-enters the queue at position %d.'
          % (ticker, e['position']))
    return 0


def show():
    d = _load()
    queue, _ = _queue()
    live = [e for e in d['entries'].values() if not e.get('unparked')]
    freed = [e for e in d['entries'].values() if e.get('unparked')]
    print('queue %d   parked %d   released %d'
          % (len(queue), len(live), len(freed)))
    for e in sorted(live, key=lambda x: x['position']):
        print()
        print('  #%d %s (%s, %s) PARKED %s — %s'
              % (e['position'], e['ticker'], e['market'], e['exchange'],
                 e['parked'], e['reason']))
        print('     needs:')
        for doc in e['documents_needed']:
            print('       - %s' % doc)
        print('     unpark when: %s' % e['unpark_when'])
        print('     attempts (%d):' % len(e['attempts']))
        for a in e['attempts']:
            print('       %-6s %s  %s' % (a.get('result', '?'), a.get('url', ''),
                                          a.get('outcome', '')))
    for e in sorted(freed, key=lambda x: x['position']):
        print()
        print('  #%d %s released %s — %s'
              % (e['position'], e['ticker'], e['unparked']['when'],
                 e['unparked'].get('note') or ''))
    return 0


def check():
    """Gate.  Declares what it examined and counts against the queue [R-ENF-04]."""
    d = _load()
    queue, excluded = _queue()
    inq = {q['ticker'] for q in queue}
    exc = {t for t, _ in excluded}
    runs = {x[:-len('_walkforward')].upper()
            for x in os.listdir(ENGINE)
            if x.endswith('_walkforward') and os.path.isdir(os.path.join(ENGINE, x))}
    sys.path.insert(0, ENGINE)
    import fv_movement
    baselines = set(fv_movement._load()['entries'])

    live = {k: v for k, v in d['entries'].items() if not v.get('unparked')}
    fails = []
    for tk, e in sorted(live.items()):
        if tk not in inq:
            fails.append('%s is parked but is not in the campaign queue' % tk)
        if tk in exc:
            fails.append('%s is both parked and excluded — one decision, not two' % tk)
        if tk in runs:
            fails.append('%s is parked AND has engine/%s_walkforward on disk. '
                         'Parking and running are exclusive: the run directory '
                         'turns both campaign gates red for a run that is not '
                         'happening.' % (tk, tk.lower()))
        if tk in baselines:
            fails.append('%s is parked AND carries a frozen fair-value baseline. '
                         'fv_movement.check() fails a baseline with no run behind '
                         'it — freeze it when the run starts, not when it is '
                         'deferred.' % tk)
        if not e.get('attempts'):
            fails.append('%s is parked with no logged attempt — an assertion, '
                         'not evidence' % tk)
        for a in e.get('attempts', []):
            if not a.get('outcome'):
                fails.append('%s logs an attempt to %s with no OUTCOME. The rule '
                             'is log the attempt AND its outcome.'
                             % (tk, a.get('url', '?')))
        if not e.get('documents_needed'):
            fails.append('%s is parked without naming the documents needed' % tk)
        if not e.get('unpark_when'):
            fails.append('%s is parked with no stated unpark condition' % tk)

    print('queue: %d   parked: %d   released: %d   run dirs: %d'
          % (len(inq), len(live), len(d['entries']) - len(live), len(runs)))
    for f in fails:
        print('  FAIL  %s' % f)
    if fails:
        return 1
    if not live:
        print('  [ok]   nothing parked; %d names in the queue, all reachable '
              'or already run' % len(inq))
    else:
        print('  [ok]   %d parked name(s), each with logged attempts and '
              'outcomes, a document request and an unpark condition'
              % len(live))
        print('  [ok]   no parked name carries a run directory or a frozen baseline')
    return 0


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 0
    cmd = argv[1]
    if cmd == 'list':
        return show()
    if cmd == 'check':
        return check()
    if cmd == 'unpark':
        a = argv[2:]
        note = a[a.index('--note') + 1] if '--note' in a else None
        return unpark(a[0], note)
    print(__doc__)
    return 1


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
