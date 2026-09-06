"""The book-wide fundamental walk-forward campaign queue.

WHY THIS IS CODE AND NOT A LIST IN THE PROMPT.  The campaign runs over every
covered name in the register, and that register moves: a name is added by
placing an OHLC file, a study is built, a standard is bumped.  A queue written
into a document would be authoritative-looking and wrong within a week -- the
same failure the stale-library list and the stale digest each produced already.
So `Fundamental_Walkforward_Campaign_Prompt.md` states the ORDERING RULE and
names this module; the ORDER ITSELF is resolved live, here, at the moment it is
relied on.

MARKET ORDER IS FIXED BY INSTRUCTION (01-Sep-2026): EGX, UAE, KSA, Qatar,
India, Korea, USA.  It is not derived from anything and must not be reordered
on a later reading of the data.

WITHIN A MARKET the order is by the standard each name was last built to
[R-STD-01], because that is what makes a book-wide re-issue a finite, countable
queue rather than an open-ended one:

    tier 1  reissue      a study exists but was built to an older standard,
                         or carries no standard stamp at all
    tier 2  first-build  no study directory exists -- the name carries a
                         published fair value that no study of the current
                         standard ever produced
    tier 3  current      a study stamped at the live STANDARD_VERSION

Alphabetical inside each tier, so the queue is deterministic and two readings a
week apart differ only where the repository actually moved.

METALS ARE EXCLUDED BY CONSTRUCTION, not by oversight.  GOLD, SILVER and
PLATINUM have no issuer, no financial statements and no drivers, so the
fundamental method has nothing to project and nothing to score against.  They
are counted and named in the exclusion list rather than silently dropped --
per [R-ENF-04] an absent name must be an accounted-for name.

Read the queue:   python3 engine/campaign_queue.py
                  python3 engine/campaign_queue.py --market EG
                  python3 engine/campaign_queue.py --next
"""

import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENGINE = os.path.join(ROOT, 'engine')
DATA_JS = os.path.join(ROOT, 'assets', 'data.js')
OUTSTANDING = os.path.join(ENGINE, 'build_depth_audit', 'outstanding.json')

# Fixed by instruction, 01-Sep-2026.  (market code, exchange prefixes, label)
MARKET_ORDER = (
    ('EG', ('EGX',),            'Egypt / EGX'),
    ('AE', ('ADX', 'DFM'),      'UAE / ADX + DFM'),
    ('SA', ('TADAWUL',),        'Saudi Arabia / Tadawul'),
    ('QA', ('QSE',),            'Qatar / QSE'),
    ('IN', ('NSE',),            'India / NSE'),
    ('KR', ('KRX',),            'Korea / KRX'),
    ('US', ('NASDAQ',),         'United States / NASDAQ'),
)

# A study directory stem that is not its ticker. IMPORTED, NOT COPIED: this file
# carried its own copy and the two were compared only when study_population ran as
# a script, so the consumer that never imported either got no alias at all and
# listed a studied name as unstudied for three days. One table, every consumer
# imports it, nothing left to drift.
from study_aliases import DIR_ALIAS as STUDY_ALIAS  # noqa: E402

# Study directories that intentionally resolve to no equity in the queue.
STUDY_NOT_IN_QUEUE = {'XPT': 'metals study - no issuer, no statements, no drivers'}

NODE_READ = r'''
const fs = require("fs"), vm = require("vm");
const c = {}; vm.createContext(c);
vm.runInContext(fs.readFileSync(process.argv[1], "utf8")
  + "\n;this.__T=TICKERS;this.__M=(typeof METALS!=='undefined')?METALS:{};", c);
console.log(JSON.stringify({tickers: c.__T, metals: c.__M}));
'''


def load_register(path=DATA_JS):
    """The objects the PAGE sees.  Loaded through node, never regex-parsed --
    a JS object literal takes the LAST duplicate key and re.search takes the
    FIRST, which is how a ticker page once shipped a support above its own
    close with both gates reporting clean [R-ENF-03]."""
    p = subprocess.run(['node', '-e', NODE_READ, path],
                       capture_output=True, text=True)
    if p.returncode != 0:
        raise SystemExit('FATAL: node could not load %s\n%s' % (path, p.stderr.strip()))
    d = json.loads(p.stdout)
    return d['tickers'], d['metals']


def study_standards():
    """ticker -> standard_version stamped by its study, or None if unstamped.
    Absent from the dict means no study directory at all."""
    sys.path.insert(0, ENGINE)
    from research_protocol import STANDARD_VERSION
    out = {}
    for d in sorted(os.listdir(ENGINE)):
        if not d.endswith('_study') or not os.path.isdir(os.path.join(ENGINE, d)):
            continue
        tk = d[:-len('_study')].upper()
        tk = STUDY_ALIAS.get(tk, tk)
        version = None
        for f in sorted(os.listdir(os.path.join(ENGINE, d))):
            if not f.endswith('.json'):
                continue
            try:
                j = json.load(open(os.path.join(ENGINE, d, f), encoding='utf-8'))
            except Exception:
                continue
            if isinstance(j, dict) and 'standard_version' in j:
                version = j['standard_version']
                break
        out[tk] = version
    return out, STANDARD_VERSION


def build_queue(path=DATA_JS):
    """The campaign queue, in run order, plus everything deliberately left out.

    Refuses rather than returns a short queue: every covered name must land in
    exactly one of queue/excluded, and every study directory must resolve to a
    covered name or be declared in STUDY_NOT_IN_QUEUE.  An empty or short
    result is not a clean result [R-ENF-04]."""
    tickers, metals = load_register(path)
    stamps, current = study_standards()

    total = len(tickers) + len(metals)
    queue, excluded, seen = [], [], set()

    for market, prefixes, label in MARKET_ORDER:
        tiers = {1: [], 2: [], 3: []}
        for tk, row in tickers.items():
            code = row.get('code') or ''
            if ':' not in code:
                continue
            ex = code.split(':', 1)[0]
            if ex not in prefixes:
                continue
            if tk in stamps:
                tier = 3 if stamps[tk] == current else 1
            else:
                tier = 2
            tiers[tier].append((tk, ex, stamps.get(tk, '(no study)')))
        for tier in (1, 2, 3):
            for tk, ex, stamp in sorted(tiers[tier]):
                seen.add(tk)
                queue.append({
                    'position': len(queue) + 1,
                    'ticker': tk, 'market': market, 'exchange': ex,
                    'market_label': label,
                    'tier': {1: 'reissue', 2: 'first-build', 3: 'current'}[tier],
                    'built_to': stamp if stamp else '(study carries no stamp)',
                    'run_dir': 'engine/%s_walkforward' % tk.lower(),
                })

    for tk in metals:
        excluded.append((tk, 'metals - no issuer, no statements, no drivers'))
    for tk in tickers:
        if tk not in seen:
            code = tickers[tk].get('code') or ''
            excluded.append((tk, 'exchange prefix %r is in no market of the fixed '
                                 'run order' % (code.split(':', 1)[0] if ':' in code
                                                else '(none)')))

    # --- the refusals ------------------------------------------------------
    if len(queue) + len(excluded) != total:
        raise SystemExit('FATAL: %d queued + %d excluded != %d covered names. '
                         'A name in neither list is a name nobody decided about.'
                         % (len(queue), len(excluded), total))
    if not queue:
        raise SystemExit('FATAL: the queue is empty. An empty result is not a '
                         'clean result -- the register did not load.')
    covered = set(tickers) | set(metals)
    for tk in stamps:
        if tk not in covered and tk not in STUDY_NOT_IN_QUEUE:
            raise SystemExit('FATAL: study directory for %r resolves to no covered '
                             'name. Add it to STUDY_ALIAS or STUDY_NOT_IN_QUEUE.' % tk)
    return queue, excluded, current, total


def main(argv):
    market = None
    if '--market' in argv:
        market = argv[argv.index('--market') + 1].upper()
    queue, excluded, current, total = build_queue()

    if '--next' in argv:
        done = [q for q in queue if os.path.isdir(os.path.join(ROOT, q['run_dir']))]
        todo = [q for q in queue if not os.path.isdir(os.path.join(ROOT, q['run_dir']))]
        print('run directories present: %d of %d' % (len(done), len(queue)))
        if todo:
            n = todo[0]
            print('NEXT: #%d %s (%s, %s, tier %s, built to %s)'
                  % (n['position'], n['ticker'], n['market_label'], n['exchange'],
                     n['tier'], n['built_to']))
        else:
            print('NEXT: none -- every name in the queue has a run directory.')
        return 0

    if '--json' in argv:
        print(json.dumps({'queue': queue, 'excluded': excluded,
                          'standard': current, 'covered': total}, indent=1))
        return 0

    print('live standard %s   covered names %d   queued %d   excluded %d'
          % (current, total, len(queue), len(excluded)))
    print()
    last = None
    for q in queue:
        if market and q['market'] != market:
            continue
        if q['market_label'] != last:
            last = q['market_label']
            n = sum(1 for x in queue if x['market_label'] == last)
            print('== %s == %d names' % (last, n))
        print('  %3d  %-12s %-8s %-11s %s'
              % (q['position'], q['ticker'], q['exchange'], q['tier'], q['built_to']))
    if not market:
        print()
        print('EXCLUDED (%d), each with its reason:' % len(excluded))
        for tk, why in excluded:
            print('  %-12s %s' % (tk, why))
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
