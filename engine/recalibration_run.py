"""THE BOARD FOR THE 90-NAME RECALIBRATION — where every name is, and whose move it is.

WHAT WAS MISSING WAS NOT A PLAN.  `Recalibration_Runbook_17-09-2026.md` is the order of
work for one name and `Recalibration_Campaign_Plan_17-09-2026.md` is the order the names
are worked in.  Both are prose, and prose cannot answer the only question a programme of
this size asks every morning: WHICH NAME DO I TOUCH NEXT, AND WHAT IS IT WAITING FOR.
At one name a person remembers.  At ninety, across seven steps, two of which stop dead
and hand the work to the principal, nobody remembers — and the failure is not that
somebody forgets, it is that a name sits in a hand-off nobody is tracking while the desk
works on something else.

STATE IS DERIVED FROM THE REPOSITORY, NEVER STORED.  There is no step pointer per name
and no "mark step 2 done" command, deliberately: this repository has paid repeatedly for
records somebody has to remember to update -- the stale digest, the stale library list,
the technical read that had to be told the library moved, and, this same week, a lever
applied to a model and never written into the record that a gate outside it reads.  A
board maintained by hand would go stale the first afternoon somebody was in a hurry, and
it would go stale SILENTLY, which is the shape that survives.  So every step here is a
PROBE over artefacts that the step itself produces, and a name's position is wherever the
probes stop.  Delete an artefact and the name moves back; that is the behaviour wanted.

A PROBE THAT CANNOT READ ITS ARTEFACT REPORTS UNREADABLE AND NEVER DONE [R-ENF-04].  An
empty result is not a clean result, and on a board it is worse than elsewhere, because an
absent answer here reads exactly like a finished name.

THE ARTEFACT NAMES ARE TAKEN FROM WHAT THE BOOK ACTUALLY CONTAINS, not from what a
convention ought to be [L-355].  They were read off the two names that have been through
this runbook end to end -- PHDC and GBCO -- and where those two disagree BOTH spellings
are accepted, because a reader that knows one convention finds nothing under the other
and reports that as a result.  Every name is in NAMES below, in one place, so a third
spelling is added once rather than hunted.

WHAT IT DELIBERATELY DOES NOT DO.  It does not run any step, does not decide anything,
and does not write to the repository.  It is a reader.  The steps are judgement work
governed by the runbook and the standing rules; what this supplies is the thing neither
of those can -- an honest answer to where ninety names actually are.

    python3 engine/recalibration_run.py                 the board
    python3 engine/recalibration_run.py --next          the next name the DESK can act on
    python3 engine/recalibration_run.py --waiting       everything held by the principal
    python3 engine/recalibration_run.py --ticker TK     one name, every step, with evidence
    python3 engine/recalibration_run.py --brief TK      where TK is + the runbook's own
                                                        prompt for the step it is at
    python3 engine/recalibration_run.py --market EG     one market
    python3 engine/recalibration_run.py --json
    python3 engine/recalibration_run.py --selfcheck   every artefact name this
                                                     reader looks for resolves
"""

import glob
import io
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENGINE = os.path.join(ROOT, 'engine')
SCRIPTS = os.path.join(ROOT, 'scripts')
for _p in (ENGINE, SCRIPTS):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import campaign_queue as CQ                                      # noqa: E402
import check_calibration_deliverables as CD                      # noqa: E402

FV_MOVEMENT = os.path.join(ENGINE, 'fv_movement.json')
PRICES = os.path.join(ENGINE, 'prices')

# WHOSE MOVE IT IS. The distinction is the whole point of the board: a name the desk is
# blocked on is work, and a name the principal is blocked on is a message somebody has to
# send. Counting them together is how a hand-off sits for a week.
DESK, PRINCIPAL, DONE, UNREADABLE, HELD = ('DESK', 'PRINCIPAL', 'DONE',
                                          'UNREADABLE', 'HELD')

# EVERY ARTEFACT NAME THE RUNBOOK'S STEPS PRODUCE, IN ONE PLACE. Read off PHDC and GBCO,
# the two names that have been through it; where they differ both are accepted.
NAMES = {
    'news_handover': ('EXTERNAL_NEWS_PROMPT_*.md',),
    'news_returns':  ('EXTERNAL_NEWS_*.md',),
    'qc_gate':       ('QC_GATE_*.md',),
    'gap_review':    ('GAP_REVIEW_*.md',),
    'driver_call':   ('DRIVER_IMPACT_*.md', 'RECALIBRATION_*.md', 'UPDATE_*.md'),
    'audit_out':     ('HANDOVER_*.md',),
    'audit_back':    ('CRITIQUE_RESPONSE_*.md',),
}
# MARKET_DISSENT_*.md IS DELIBERATELY NOT HERE. A draft carried it and the self-check
# refused it -- correctly, since no name in the book has ever filed one, so the pattern
# matched nothing and there is no way to tell a spelling this reader invented from a step
# nothing has reached. It was not declared as an exception, it was REMOVED: the dissent
# is [R-GAP-02]'s release and check_publish_block.verdict() already rules on it, so a
# second reader here would be two records of one fact, which diverge the moment one is
# pruned. Step 6 defers to that gate rather than re-deriving anything it owns.




# ---------------------------------------------------------- the step's own words
# THE RUNBOOK IS READ, NEVER COPIED. A board that tells you where a name is and leaves
# you to find what to do next is half a process, and the half it leaves out is the half
# somebody does from memory. So `--brief` lifts the step's OWN prompt out of
# Recalibration_Runbook_17-09-2026.md at the moment it is relied on -- the same
# discipline as the campaign queue, for the same reason: a prompt copied into a second
# file is a prompt that stops moving when the first one is amended, and this repository
# has paid for that in both governing documents already.
RUNBOOK_GLOB = os.path.join(ENGINE, 'Recalibration_Runbook_*.md')


def runbook_path():
    hits = sorted(glob.glob(RUNBOOK_GLOB))
    if not hits:
        raise SystemExit('FATAL: no %s on disk. The steps are the runbook\'s, and a '
                         'brief with no runbook behind it would be this file inventing '
                         'the process it exists to report on.' % os.path.basename(RUNBOOK_GLOB))
    return hits[-1]


def step_prompt(n):
    """The runbook's own text for step n, verbatim, with its blockquote markers stripped."""
    txt = io.open(runbook_path(), encoding='utf-8').read()
    lines = txt.splitlines()
    start = None
    for i, ln in enumerate(lines):
        if ln.startswith('## STEP %d ' % n) or ln.startswith('## STEP %d\u2014' % n):
            start = i
            break
    if start is None:
        raise SystemExit('FATAL: %s carries no "## STEP %d" heading. A brief that cannot '
                         'find its step reports nothing, which reads exactly like a step '
                         'with nothing to do [R-ENF-04].'
                         % (os.path.basename(runbook_path()), n))
    out = []
    for ln in lines[start + 1:]:
        if ln.startswith('## '):
            break
        out.append(ln)
    return '\n'.join(out).strip()


def _study_dir(tk):
    d = os.path.join(ENGINE, '%s_study' % tk.lower())
    return d if os.path.isdir(d) else None


def _newest(sdir, key):
    """(basename, date) of the newest artefact of `key`, or (None, None).

    EXTERNAL_NEWS_PROMPT_* MATCHES EXTERNAL_NEWS_* AND THAT IS NOT A DETAIL: the
    hand-over and the returns are two different states of one step, and a glob that
    cannot tell them apart reports a name as having its answers back the moment the
    question was asked. The prompt is excluded from the returns explicitly.
    """
    if not sdir:
        return (None, None)
    best = (None, None)
    for pat in NAMES[key]:
        for p in glob.glob(os.path.join(sdir, pat)):
            b = os.path.basename(p)
            if key == 'news_returns' and b.startswith('EXTERNAL_NEWS_PROMPT_'):
                continue
            dt = CD._date(b)
            if dt and (best[1] is None or dt > best[1]):
                best = (b, dt)
    return best


def _edition(sdir):
    """(basename, date) of the newest delivered valuation document."""
    if not sdir:
        return (None, None)
    return CD._latest(sdir, '*Valuation_Study*.docx', '*Valuation_Study*.pdf',
                      '*_Study_*.docx')


def _fmt(dt):
    return '%02d-%02d-%d' % (dt[2], dt[1], dt[0]) if dt else '(undated)'


# ---------------------------------------------------------------- the probes
# Each returns (state, evidence). The evidence is what an operator reads to know what to
# do next, so it names the artefact rather than describing it.

def step0(tk, q):
    """FREEZE, THEN ASK — the baseline and the supplied price."""
    try:
        entries = json.load(open(FV_MOVEMENT, encoding='utf-8'))['entries']
    except Exception as e:
        return UNREADABLE, 'fv_movement.json will not read (%s); a missing baseline store is not an empty one' % e
    base = (entries.get(tk) or {}).get('baseline')
    if not base:
        return DESK, 'no frozen baseline — run: python3 engine/fv_movement.py snapshot %s (CANNOT be done after the rebuild)' % tk
    priced = False
    for p in sorted(glob.glob(os.path.join(PRICES, 'SUPPLIED_*.json'))):
        try:
            d = json.load(open(p, encoding='utf-8'))
        except Exception:
            continue
        blob = json.dumps(d)
        if '"%s"' % tk in blob:
            priced = True
            break
    if not priced:
        return DESK, 'baseline frozen %s; NO supplied price for this name — ask for it in one line, then route around it [R-GAP-01 AMENDED]' % base.get('captured', '?')
    return DONE, 'baseline frozen %s, supplied price on file' % base.get('captured', '?')


def step1(tk, q):
    """RECALIBRATE — the walk-forward run and its two required documents."""
    rundir = os.path.join(ROOT, q['run_dir'])
    if not os.path.isdir(rundir):
        return DESK, 'no %s — the fundamental walk-forward has not run [R-FCAL-01]' % q['run_dir']
    draft = os.path.join(rundir, 'lessons_draft.json')
    if not os.path.exists(draft):
        return DESK, 'run exists, never harvested — run: python3 engine/lessons_harvest.py %s (a run that produces one document and not the other is not finished)' % tk
    try:
        d = json.load(open(draft, encoding='utf-8'))
    except Exception as e:
        return UNREADABLE, 'lessons_draft.json will not parse (%s)' % e
    drafts = d.get('drafts', [])
    open_ones = [x.get('proposed_id') for x in drafts
                 if not x.get('registered') and not x.get('declined')]
    if open_ones:
        return DESK, '%d harvested lesson(s) with no scope ruling: %s — the one step deliberately not automated' % (len(open_ones), ', '.join(str(x) for x in open_ones[:4]))
    return DONE, 'run present, %d lesson(s) harvested and ruled on' % len(drafts)


def step2(tk, q):
    """INTERNAL QC — a QC gate at the CURRENT edition, and a gap review if it is owed."""
    sdir = _study_dir(tk)
    if not sdir:
        return DESK, 'no engine/%s_study — the record has to be reconstructed from the delivered documents before any gate can read it' % tk.lower()
    edoc, edate = _edition(sdir)
    if not edate:
        return UNREADABLE, 'no dated valuation document in %s_study — an unreadable edition is not a clean one' % tk.lower()
    qc, qcd = _newest(sdir, 'qc_gate')
    if not qcd:
        return DESK, 'edition %s carries NO QC gate' % _fmt(edate)
    if qcd < edate:
        return DESK, 'QC gate is %s while the edition is %s — a gate written against a superseded document' % (_fmt(qcd), _fmt(edate))
    gr, grd = _newest(sdir, 'gap_review')
    return DONE, 'QC gate %s at edition %s%s' % (
        _fmt(qcd), _fmt(edate),
        ', gap review %s' % _fmt(grd) if grd else ', no gap review on file')


def step3(tk, q):
    """EXTERNAL NEWS — hands off to the principal, and stops."""
    sdir = _study_dir(tk)
    ho, hod = _newest(sdir, 'news_handover')
    rt, rtd = _newest(sdir, 'news_returns')
    if rtd and (not hod or rtd >= hod):
        return DONE, 'returns in: %s' % rt
    if hod:
        return PRINCIPAL, 'handed over %s (%s) — waiting on the search returns' % (_fmt(hod), ho)
    return DESK, 'no hand-over prompt built — build it from the study\'s own driver list and dated negative searches, then STOP'


def step4(tk, q):
    """DOES IT MOVE A DRIVER — a rebuild ledger that walks, or a stated no-change."""
    sdir = _study_dir(tk)
    led = os.path.join(sdir, 'rebuild_ledger.json') if sdir else None
    if led and os.path.exists(led):
        try:
            d = json.load(open(led, encoding='utf-8'))
        except Exception as e:
            return UNREADABLE, 'rebuild_ledger.json will not parse (%s)' % e
        n = len(d.get('levers', []))
        return DONE, 'rebuild ledger walks %d lever(s) [R-REBUILD-01]' % n
    call, calld = _newest(sdir, 'driver_call')
    if calld:
        return DONE, 'driver call recorded: %s' % call
    return DESK, 'no rebuild ledger and no stated no-change — an unchanged answer is legitimate and must still be written down'


def step5(tk, q):
    """EXTERNAL AUDIT — hands off to the principal, and stops twice."""
    sdir = _study_dir(tk)
    out, outd = _newest(sdir, 'audit_out')
    back, backd = _newest(sdir, 'audit_back')
    if backd and (not outd or backd >= outd):
        return DONE, 'audit answered: %s' % back
    if outd:
        return PRINCIPAL, 'delivered for audit %s (%s) — waiting on the outcome' % (_fmt(outd), out)
    qc, qcd = _newest(sdir, 'qc_gate')
    edoc, edate = _edition(sdir)
    if qcd and edate and qcd >= edate:
        return DONE, 'no external audit run; the in-house alternative stands — QC gate %s from outside the study' % _fmt(qcd)
    return DESK, 'not handed over for audit and no in-house QC gate at this edition'


def step6(tk, q):
    """THE PUBLISH GATE — read live, never remembered."""
    try:
        import check_publish_block as PB
        # verdict() returns (may_publish, reason, rows) -- unpacked by SLICE rather than
        # by count, because a gate that grows a field should not silently make this
        # report every name unreadable, which is what a two-tuple unpack did on its
        # first run.
        res = PB.verdict(tk)
        ok, why = res[0], res[1]
    except Exception as e:
        return UNREADABLE, 'check_publish_block could not rule on this name (%s)' % e
    # A HOLD IS NOT AN ERROR AND IS NOT THE DESK'S MOVE EITHER. Most of the book is held
    # on the METHOD, which no per-name work releases -- so it is reported as its own
    # state rather than as a task somebody could pick up and fail to finish.
    return (DONE, 'PUBLISH — %s' % why) if ok else (HELD, 'HELD — %s' % why)


STEPS = (
    (0, 'freeze & ask',    step0),
    (1, 'recalibrate',     step1),
    (2, 'internal QC',     step2),
    (3, 'external news',   step3),
    (4, 'does it move',    step4),
    (5, 'external audit',  step5),
    (6, 'publish gate',    step6),
)


# THE WAVE, WHICH IS THE CAMPAIGN PLAN'S ONE DECISION AND HAD TO BE ENCODED OR IGNORED.
# The queue runs market-major: every EGX name, then every UAE name, and so on. The plan
# decides something the queue does not -- that all 22 RECORD-BACKED re-issues are worked
# before any record is reconstructed, because a class defect is cheapest to find where a
# gate can see it at all, and a study with no record commits nothing any gate can open.
# Left unencoded, `--next` would hand out an EGX reconstruction the moment the ninth EGX
# re-issue closed and the plan would be quietly contradicted by the tool that implements
# it. So the wave is computed here, from the tier, and the queue's market order runs
# INSIDE it -- the plan changing the order across waves and the queue keeping it within.
WAVES = {'current': 0, 'reissue': 1, 'reissue-no-record': 5}


def wave_of(q):
    return WAVES.get(q['tier'], 5)


# THE EGX CHECKPOINT IS THE CAMPAIGN'S OWN AND IS REPORTED, NEVER ENFORCED SILENTLY.
# "HARD STOP AFTER EGX to review whether the method generalises before UAE begins" is a
# judgement somebody makes out loud; a tool that simply refused to name the next UAE name
# would look like a bug, and one that crossed the boundary without saying so would hide
# the decision. So it is announced when it is reached and the name is still given.
# EGX IS FINISHED BEFORE ANY OTHER MARKET STARTS [per instruction, 17-09-2026:
# "Delay other markets till we finish EGX first"]. This REPLACES the plan's
# record-backed-first ordering across markets: the queue's own fixed market order runs,
# and EGX -- ALL of it, both tiers -- completes before UAE begins.
#
# WHAT "FINISHED" MEANS HERE IS STEP 6, NOT STEP 7, and that is not a softening. While
# the method hold stands, NO name can reach step 7: the publish gate refuses every study
# in the book until Phase 1 closes. A definition keyed on step 7 would therefore never be
# satisfied and this constraint would never release -- the gate with no release
# [R-CAL-01] forbids, arriving as an ordering rule instead of a gate. A name standing at
# step 6 has had every step of the runbook done to it and is waiting on a book-wide
# event, which is the finished state available.
#
# THE COST IS STATED RATHER THAN DISCOVERED: every non-EGX market waits the length of the
# EGX campaign -- 37 names against the 9 the previous ordering would have taken before
# UAE started -- and their pages carry their pre-rebuild fair values throughout, which is
# the debt [R-GAP-03] measures and which does not shorten meanwhile.
MARKET_FIRST = 'EG'


def market_blocked(rows, nxt):
    """Why `nxt` may not be started yet, or None."""
    if nxt['market'] == MARKET_FIRST:
        return None
    first = [r for r in rows if r['market'] == MARKET_FIRST]
    if not first:
        return ('the first-market constraint names %s and the board carries no %s name '
                'at all, which is the resolver breaking rather than that market being '
                'clear [R-ENF-04]' % (MARKET_FIRST, MARKET_FIRST))
    outstanding = [r for r in first if r['step'] < 6]
    if not outstanding:
        return None
    return ('%s IS NOT FINISHED: %d of %d of its names are still short of the publish '
            'gate (%s%s). Per the standing instruction, no other market starts until it '
            'is. The campaign\'s own hard stop then applies at the boundary -- state '
            'whether the method generalised before the first name of the next market.'
            % (MARKET_FIRST, len(outstanding), len(first),
               ', '.join(r['ticker'] for r in outstanding[:8]),
               ' …' if len(outstanding) > 8 else ''))


def checkpoint_note(rows, nxt):
    return market_blocked(rows, nxt)


def position(tk, q, upto=None):
    """(step_no, step_name, state, evidence) — the FIRST step that is not done.

    Walking in order rather than reporting the furthest artefact is deliberate: a study
    with a QC gate and no frozen baseline has not skipped ahead, it has lost the one
    thing that cannot be recovered afterwards, and a board that showed it at step 2
    would hide exactly that.
    """
    for n, name, probe in STEPS:
        if upto is not None and n > upto:
            break
        state, why = probe(tk, q)
        if state != DONE:
            return (n, name, state, why)
    return (7, 'complete', DONE, 'every step satisfied')


def board(market=None):
    queue, excluded, standard, covered = CQ.build_queue()
    if not queue:
        raise SystemExit('FATAL: the campaign queue is empty. An empty result is not a '
                         'clean result [R-ENF-04].')
    rows = []
    for q in queue:
        if market and q['market'] != market:
            continue
        n, name, state, why = position(q['ticker'], q)
        rows.append({'ticker': q['ticker'], 'market': q['market'],
                     'market_label': q['market_label'], 'exchange': q['exchange'],
                     'tier': q['tier'], 'position': q['position'], 'wave': wave_of(q),
                     'step': n, 'step_name': name, 'state': state, 'evidence': why})
    if not rows:
        raise SystemExit('FATAL: no names in scope — a board that examined nothing is not '
                         'a board with nothing on it [R-ENF-04].')
    return rows, standard, covered


def brief(tk):
    """Where this name is, and the runbook's own words for what comes next."""
    queue, _, standard, _ = CQ.build_queue()
    q = next((x for x in queue if x['ticker'] == tk), None)
    if not q:
        raise SystemExit('FATAL: %s is not in the campaign queue.' % tk)
    n, name, state, why = position(tk, q)
    if n == 7:
        print('%s is complete under the runbook. Nothing to brief.' % tk)
        return 0
    print('=' * 78)
    print('%s — %s, %s, tier %s' % (tk, q['market_label'], q['exchange'], q['tier']))
    print('STEP %d · %s · %s' % (n, name.upper(), state))
    print('WHY: %s' % why)
    print('=' * 78)
    print()
    body = step_prompt(n)
    # {TICKER} is the runbook's own placeholder; {CLASS} is left as written because the
    # class is a judgement the lens registry holds and this reader must not guess it.
    print(body.replace('{TICKER}', tk))
    return 0


def selfcheck():
    """Every name this reader looks for is a name the book actually produces.

    THE FAILURE THIS GUARDS IS THE ONE THAT PRODUCES A NUMBER RATHER THAN AN ERROR
    [L-355]: a probe that looks for an artefact under a spelling nobody uses finds
    nothing, and reports the step as not done, for every name in the book, forever. That
    reads exactly like ninety names with work outstanding, which is a plausible state.
    So each pattern must match somewhere, and each step must exist in the runbook.
    """
    bad = []
    for key, pats in sorted(NAMES.items()):
        hits = 0
        for pat in pats:
            hits += len(glob.glob(os.path.join(ENGINE, '*_study', pat)))
        if not hits:
            bad.append('%-14s matches NOTHING in the book: %s — either no name has '
                       'reached the step that writes it, or the spelling is wrong, and '
                       'from inside this file those look identical'
                       % (key, ', '.join(pats)))
    for n_, name, _ in STEPS:
        try:
            body = step_prompt(n_)
        except SystemExit as e:
            bad.append('step %d (%s): %s' % (n_, name, e))
            continue
        if len(body) < 200:
            bad.append('step %d (%s) resolves to %d characters of runbook — too short to '
                       'be the step' % (n_, name, len(body)))
    print('SELF-CHECK — %d artefact name(s), %d step(s)' % (len(NAMES), len(STEPS)))
    for b in bad:
        print('  FAIL  %s' % b)
    if not bad:
        print('  every artefact name resolves in the book; every step resolves in the runbook')
    return 1 if bad else 0


def main(argv):
    if '--selfcheck' in argv:
        return selfcheck()
    market = argv[argv.index('--market') + 1].upper() if '--market' in argv else None
    one = argv[argv.index('--ticker') + 1].upper() if '--ticker' in argv else None

    if '--brief' in argv:
        tk = argv[argv.index('--brief') + 1].upper()
        return brief(tk)

    if one:
        queue, _, standard, _ = CQ.build_queue()
        q = next((x for x in queue if x['ticker'] == one), None)
        if not q:
            raise SystemExit('FATAL: %s is not in the campaign queue.' % one)
        print('%s — %s, %s, tier %s, built to %s'
              % (one, q['market_label'], q['exchange'], q['tier'], q['built_to']))
        print()
        stop = None
        for n, name, probe in STEPS:
            state, why = probe(one, q)
            mark = {DONE: ' ok ', DESK: 'DESK', PRINCIPAL: 'WAIT',
                    UNREADABLE: '????', HELD: 'HELD'}[state]
            print('  %d %-15s [%s]  %s' % (n, name, mark, why))
            if state != DONE and stop is None:
                stop = (n, name, state)
        print()
        print('POSITION: %s' % ('complete' if stop is None
                                else 'step %d %s — %s' % (stop[0], stop[1], stop[2])))
        return 0

    rows, standard, covered = board(market)

    if '--json' in argv:
        print(json.dumps({'standard': standard, 'covered': covered, 'rows': rows}, indent=1))
        return 0

    if '--next' in argv:
        # THE FIRST MARKET SORTS AHEAD OF EVERY OTHER, then wave, then queue position.
        # Ordering it here rather than only warning at the boundary is the difference
        # between a rule and a note: a `--next` that named a UAE name and printed a
        # caution beside it would be handing out the work it is meant to withhold.
        todo = sorted((r for r in rows if r['state'] in (DESK, UNREADABLE)),
                      key=lambda r: (0 if r['market'] == MARKET_FIRST else 1,
                                     r['wave'], r['position']))
        if not todo:
            print('NEXT: nothing the desk can act on — every name is waiting on you, held '
                  'on the method, or complete.')
            return 0
        r = todo[0]
        note = checkpoint_note(rows, r)
        if note:
            print(note)
            print()
        print('NEXT FOR THE DESK: wave %d · #%d %s (%s, tier %s)'
              % (r['wave'], r['position'], r['ticker'], r['market_label'], r['tier']))
        print('  step %d %s — %s' % (r['step'], r['step_name'], r['evidence']))
        print('  the step\'s own words: python3 engine/recalibration_run.py --brief %s'
              % r['ticker'])
        left = [x for x in todo if x['wave'] == r['wave']]
        print('  wave %d has %d name(s) the desk can act on' % (r['wave'], len(left)))
        return 0

    if '--waiting' in argv:
        wait = [r for r in rows if r['state'] == PRINCIPAL]
        if not wait:
            print('Nothing is waiting on you. Every name is the desk\'s move or complete.')
            return 0
        print('WAITING ON YOU — %d name(s). These are the two steps that hand over.' % len(wait))
        last = None
        for r in wait:
            if r['market_label'] != last:
                last = r['market_label']
                print('\n== %s ==' % last)
            print('  %-11s step %d %s' % (r['ticker'], r['step'], r['step_name']))
            print('     %s' % r['evidence'])
        print('\nBatch these by market before sending: a wave\'s throughput is set by how '
              'fast the packs come back, not by the modelling.')
        return 0

    print('RECALIBRATION BOARD — %d name(s), read live from the repository' % len(rows))
    print('live standard %s   covered names %d' % (standard, covered))
    print()
    counts = {}
    for r in rows:
        counts.setdefault((r['step'], r['step_name']),
                          {DESK: 0, PRINCIPAL: 0, UNREADABLE: 0, DONE: 0, HELD: 0})
        counts[(r['step'], r['step_name'])][r['state']] += 1
    print('  step                    desk   waiting-on-you   held   unreadable')
    for (n, name), c in sorted(counts.items()):
        if n == 7:
            continue
        print('  %d %-20s %5d   %14d %6d   %10d'
              % (n, name, c[DESK], c[PRINCIPAL], c[HELD], c[UNREADABLE]))
    done = sum(1 for r in rows if r['step'] == 7)
    print('  %-22s %5d complete' % ('', done))
    print()
    print('WHOSE MOVE:  desk %d   you %d   held-on-method %d   unreadable %d   complete %d'
          % (sum(1 for r in rows if r['state'] == DESK),
             sum(1 for r in rows if r['state'] == PRINCIPAL),
             sum(1 for r in rows if r['state'] == HELD),
             sum(1 for r in rows if r['state'] == UNREADABLE), done))
    print()
    last = None
    for r in sorted(rows, key=lambda x: (x['wave'], x['position'])):
        key = 'WAVE %d — %s' % (r['wave'], r['market_label'])
        if key != last:
            last = key
            print('== %s ==' % key)
        mark = {DONE: 'done', DESK: 'DESK', PRINCIPAL: 'WAIT',
                UNREADABLE: '????', HELD: 'HELD'}[r['state']]
        print('  %-11s %d %-15s [%s]  %s'
              % (r['ticker'], r['step'], r['step_name'], mark, r['evidence'][:96]))
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
