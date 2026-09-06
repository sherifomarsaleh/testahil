#!/usr/bin/env python3
"""A fair value far BELOW the traded price is a claim that needs auditing.  [R-GAP-01]

WHY THIS EXISTS
    On 1 September 2026 the AMOC rebuild published a central fair value of EGP 5.53
    against a market price of EGP 9.10 — thirty-nine per cent below — and every gate in
    this repository passed it. SIGCM passed. The beta was conforming. The model-report bar
    passed. The workbook recalculated with zero disagreements across 5,775 formula cells.
    The external-reader scrub was clean. None of that was wrong; none of it was looking at
    the answer.

    What the answer was hiding: the reviewed half-year statements had been downloaded from
    the company's own archive and never opened, so the study was still calling that period
    "a press release rather than a filing" and had solved its gross profit from the profit
    line; the coherence test that justified doing so estimated the half's other income by
    doubling one quarter's; three macro paths contradicted each other; the operating cash
    flows were discounted at a rate 374 basis points ABOVE the cost of equity because the
    company holds net cash, and the same cash was then added back at face; terminal growth
    of 5% sat against a terminal discount rate embedding 7% inflation; and the headline
    claimed the market price required a margin "above the best single quarter this company
    has ever filed" when the company had filed a higher one twice. Corrected, the study
    prints 8.64 against 9.10.

    Every one of those is the model being wrong, not the company being cheap. The market
    price was the only thing in the room saying so.

WHAT IT CHECKS, per covered name (the population is the book — see below)
    1. the study's own committed numbers resolve to a central fair value and the spot it
       was struck against — a study whose answer cannot be read is NOT clean [R-ENF-04]
    2. where the central sits more than GAP_LIMIT below OR GAP_LIMIT_ABOVE above that spot, a dated gap review
       exists in the study directory
    3. that review actually covers the required headings, so it cannot be a rubber stamp

THE RATCHET
    Known breaches and unreadable studies are listed in gap_outstanding.json and allowed
    to fail; the build breaks on a NEW breach, a NEW unreadable study, or a study directory
    with no entry either way. The list may only ever get SHORTER — --prune rewrites it.
    A permanently red check is one everyone learns to ignore.

THE POPULATION IS THE BOOK, NOT THE DIRECTORIES  [R-ENF-04, RE-POINTED 06-09-2026]
    THIS GATE USED TO GLOB engine/*_study AND THAT WAS THE WRONG POPULATION. All 90
    covered names carry a delivered valuation study under files/; 23 have a record
    directory. So for its whole life this gate audited 23 fair values and reported
    itself population-anchored — against gap_outstanding.json, which had itself been
    seeded from the same glob. A population and the list that checks it, both derived
    from one glob, agree with each other by construction and say nothing about the world.
    Sixty-seven studies publish a fair value this gate had never once put against a price.

    It now takes its population from engine/study_population.py: the covered names joined
    to their delivered artefacts, resolved in BOTH directions and refusing rather than
    returning a short list. Anchored both ways — a run that examined zero NAMES fails, and
    a run that READ zero records across present names fails, which is the distinction an
    absent answer hides behind.

    TWO RATCHET GROUPS, NOT INTERCHANGEABLE, which is [R-TERM-01]'s own negative-control
    lesson arriving again: `no_record_dir` excuses a study that commits no record for any
    gate to read, `unreadable` excuses one whose committed numbers do not expose an
    answer. A name in both, or moving between them, goes RED until the move is recorded —
    otherwise a study escapes a real unreadable answer by being re-filed as merely
    undirectoried.

USAGE
    python3 scripts/check_valuation_gap.py          # gate; exit 1 on any hard fail
    python3 scripts/check_valuation_gap.py --prune  # drop the now-passing entries
"""
import glob
import re
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENGINE = os.path.join(ROOT, 'engine')
OUTSTANDING = os.path.join(ENGINE, 'build_depth_audit', 'gap_outstanding.json')

# The trigger. As instructed on 1 September 2026: a central fair value more than ten per
# cent BELOW the latest known market price. TWO-SIDED FROM 2 September 2026 [R-GAP-01
# amended, method reassessment WS7]: the same ten per cent ABOVE the price fires the same
# eight-heading review.
#
# Why the extension. The one-sidedness was on the record as a decision, and its stated cost
# was that an over-optimistic study would get no automatic audit and that nothing else
# supplied one. The method reassessment then measured what the one-sided defence had cost:
# because only the downside was audited, every correction the house made ran the same way,
# and the lean survived inside a process that looked rigorous. A gate that can only fire in
# one direction teaches the work to drift in the other.
#
# The trigger stays EVIDENTIAL rather than deferential, in both directions. A large gap
# either way is a high-prior-of-defect region, and the price is the only instrument in the
# room that measures it. The rule does not say the answer must change: a genuine 39%
# discount and a genuine 39% premium are both legitimate conclusions, and this project
# publishes ranges precisely because prices are sometimes wrong. It says the answer is
# AUDITED before it ships.
#
# The threshold is the instruction's own and is not dressed up as a derivation. What is
# defensible is the shape: a review costs an hour and a shipped error costs the study.
GAP_LIMIT = -0.10
GAP_LIMIT_ABOVE = 0.10

# What a review must cover. These are not invented headings: each one names a defect that
# was actually present in the AMOC study the day this rule was adopted, and each was
# individually capable of producing the whole gap.
REQUIRED_SECTIONS = {
    'LATEST FILINGS': 'every disclosed period actually read, the most recent named with its date',
    'BASE YEAR': 'foots to filed periods, and what is annualised or solved rather than filed',
    'MACRO COHERENCE': 'inflation, currency and price paths mutually consistent',
    'DISCOUNT RATE': 'the operating rate is the right one and cash is charged for once',
    'TERMINAL': 'terminal growth coherent with the inflation inside the terminal discount rate',
    'BALANCE SHEET': 'the bridge stands on the latest disclosed balance sheet',
    'CLAIMS AGAINST THE RECORD': 'every "best ever"/"never" statement checked against the filings',
    'MULTIPLE CROSS-CHECK': 'the earnings and enterprise multiples the fair value implies',
}
REVIEW_GLOB = 'GAP_REVIEW_*.md'

# The route string a two-sided answer returns. A sentinel rather than a bare None,
# because "this study published two named branches and no average" and "this study
# published nothing" must never read the same to a caller.
TWO_SIDED = '%s publishes a TWO-SIDED answer: %d named branches, no single central'


def _num(x):
    if isinstance(x, (int, float)):
        return float(x)
    if isinstance(x, dict):
        for k in ('value', 'central', 'base', 'mid'):
            if isinstance(x.get(k), (int, float)):
                return float(x[k])
    return None


def read_branches(sdir):
    """The named branches of a TWO-SIDED answer, or [].

    A study whose contested judgement is BINARY and straddles a decision may
    publish both branches and no single figure — EGCH is the worked case: carried
    through the cash-flow lens reads about -1.06 and stopped about +2.82, and a
    number in between describes a world in which the capital programme is half
    built. The dual-framing rule already forbids averaging such a pair; this is
    the further step of not printing an average at all.

    A two-sided answer is READABLE, not missing. Every consumer of read_answer()
    gets an explicit "no single central, N branches" rather than the silence a
    study with no answer produces, because those are different states and reading
    one as the other is how a real answer gets filed as a gap.
    """
    for fn in ("study_numbers.json", "numbers.json"):
        p = os.path.join(sdir, fn)
        if not os.path.exists(p):
            continue
        try:
            j = json.load(open(p, encoding="utf-8"))
        except Exception:
            return []
        ts = j.get("central_two_sided") or {}
        out = []
        for b in (ts.get("branches") or []):
            v = _num(b.get("value"))
            if v is not None and (b.get("label") or "").strip():
                out.append({"label": b["label"], "value": v,
                            "condition": b.get("condition") or ""})
        return out
    return []



# ---------------------------------------------------------------- latest known price
#
# [R-GAP-01] SAYS "THE LATEST KNOWN MARKET PRICE" AND THIS GATE WAS READING THE SPOT
# THE STUDY RECORDED AT STRIKE. Those are the same number on the day a study is
# built and diverge every day after, so a study struck on a stale library passed
# this gate forever — and the staler the library, the more certainly it passed.
#
# Measured on 3 September 2026, on prices the principal supplied: ARCC was struck
# at 59.00 on 6 August and had traded to 76.81, AMOC struck at 9.10 and traded to
# 13.43. Against their struck spots the gate read -9.4% and +8.9% and stayed
# silent; against the market it was asked to compare with, they are -30.4% and
# -26.2%, both deep in the high-prior-of-defect region this rule exists to audit.
# The gate was not wrong about its arithmetic. It was reading the wrong price.
#
# The house's own price source is the persistent OHLC library, so that is what is
# read, newest row first, and THE DATE IS PRINTED BESIDE THE FIGURE — a library
# four weeks old still yields a stale comparison, and the honest fix is to say how
# old rather than to pretend a strike-date spot is current. Where no library
# resolves, the struck spot is used and the record says so; that is a fallback,
# never a preference.
# THE LIBRARY IS NOT ALWAYS THE LATEST KNOWN PRICE, AND ON 3 SEPTEMBER 2026 IT WAS
# FOUR WEEKS BEHIND ONE [added 03-Sep-2026]. The clause above reads the persistent
# OHLC library, which is right whenever the library is the newest thing the house
# holds. It was not: the principal supplied ninety dated closes for 2-3 September
# while every EGX library still ended on 6 August, so this gate reported studies
# struck on the SUPPLIED prices as diverging from the "latest known" — naming the
# current answer stale against a comparison a month older than it.
#
# That is the [R-ENF-04] species: not a wrong answer, an answer from the wrong
# source presented with the same confidence. [R-GAP-01 AMENDED] settles which
# source, and it is not a preference between two files: the supplied prices are a
# COMMITTED ARTEFACT at engine/prices/SUPPLIED_{DD-MM-YYYY}.json precisely so a
# session that cannot see a figure quoted in conversation asks the repository
# instead. So both are read and THE NEWER DATE WINS, whichever it is — a fresh
# vendor export overtakes a supplied file the same way, with no edit here.
def supplied_price(ticker):
    """(price, date, source) from the newest committed SUPPLIED_*.json, else (None, None, why)."""
    files = sorted(glob.glob(os.path.join(ENGINE, 'prices', 'SUPPLIED_*.json')))
    if not files:
        return None, None, 'no supplied price file'
    best = (None, None, 'ticker not in the supplied prices')
    for fp in files:                       # oldest first, so the newest file wins
        try:
            doc = json.load(open(fp, encoding='utf-8'))
        except Exception as e:
            return None, None, 'supplied prices unreadable: %s' % e
        rows = doc.get('prices') or doc.get('closes') or {}
        row = rows.get(ticker.upper())
        if not isinstance(row, dict):
            continue
        try:
            px = float(row['price'])
        except (KeyError, TypeError, ValueError):
            continue
        best = (px, row.get('date') or doc.get('supplied_on'),
                os.path.relpath(fp, ROOT))
    return best


_ALIAS_CACHE = None


def _resolve_ticker(ticker):
    """A study directory stem is not always its ticker. IMPORTED, never re-declared.

    engine/campaign_queue.py has carried STUDY_ALIAS = {'FERTIGLOBE': 'FERTIGLB'}
    and STUDY_NOT_IN_QUEUE = {'XPT': ...} since the campaign was written, with the
    reason stated: a silent mismatch would put a rebuilt name in the wrong tier and
    nobody would see it. THIS GATE DID NOT IMPORT THEM and keyed on the directory
    stem, so it reported FERTIGLOBE as having 'no latest known price' while that
    price sat in the supplied file under its real ticker — which means the gap on
    that study has never been measured and [R-GAP-01]'s audit has never fired on it.

    A SECOND COPY WOULD BE TWO CLAIMS WEARING ONE NAME [R-ENF-03], and the protocol
    already names this exact class: ledger names are not panel filenames, records
    are keyed through an EXPLICIT asserted alias, never inferred from a filename.
    So the map is imported and the import failing is a failure, not a fallback.
    """
    global _ALIAS_CACHE
    if _ALIAS_CACHE is None:
        # RESOLVED BESIDE THIS FILE, NOT THROUGH ENGINE. The alias map is a property
        # of the REPOSITORY; ENGINE is repointed at a temp directory by this gate's
        # own negative control, which substitutes a study population and has no
        # reason to carry a module about ticker names. Reading it through ENGINE
        # made the control crash on an absence and go red for the WRONG reason —
        # which reads exactly like going red for the right one, and is the finding
        # the new-study gauntlet recorded on its own first run.
        import importlib.util
        here = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(os.path.dirname(here), 'engine', 'campaign_queue.py')
        spec = importlib.util.spec_from_file_location('_cq', path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)          # a missing map is a FAILURE, never a
        _ALIAS_CACHE = (mod.STUDY_ALIAS,      # silent fallback to the raw ticker:
                        mod.STUDY_NOT_IN_QUEUE)   # that is the mismatch it prevents
    alias, not_in_queue = _ALIAS_CACHE
    return alias.get(ticker.upper(), ticker.upper()), not_in_queue


def latest_known_price(ticker):
    """(price, date, source): the NEWER of the supplied prices and the OHLC library."""
    ticker, not_in_queue = _resolve_ticker(ticker)
    if ticker in not_in_queue:
        return None, None, ('%s — %s' % (ticker, not_in_queue[ticker]))
    lib = _library_price(ticker)
    sup = supplied_price(ticker)
    if sup[0] is not None and lib[0] is not None:
        return sup if (sup[1] or '') >= (lib[1] or '') else lib
    if sup[0] is not None:
        return sup
    if lib[0] is not None:
        return lib
    # neither resolved: report the library's reason, which is the one that names a
    # missing house artefact rather than a missing hand-off
    return lib


def _library_price(ticker):
    """(price, date, source) from the persistent OHLC library, or (None, None, why)."""
    hits = glob.glob(os.path.join(ENGINE, 'raw_ohlc', '*', '%s.csv' % ticker.upper()))
    if not hits:
        return None, None, 'no OHLC library for %s' % ticker
    try:
        with open(hits[0], encoding='utf-8', errors='replace') as fh:
            rows = [l for l in fh.read().splitlines() if l.strip()]
    except Exception as e:
        return None, None, 'library unreadable: %s' % e
    # the libraries are written newest-first; the header, if any, is not a date
    for line in rows:
        cells = [c.strip().strip('"') for c in line.split(',')]
        if len(cells) < 2:
            continue
        m = re.match(r'^(\d{2})/(\d{2})/(\d{4})$', cells[0])
        if not m:
            continue
        try:
            px = float(cells[1].replace(',', ''))
        except ValueError:
            continue
        return px, '%s-%s-%s' % (m.group(3), m.group(1), m.group(2)), os.path.relpath(
            hits[0], ROOT)
    return None, None, 'no dated row found in %s' % os.path.basename(hits[0])


def read_answer(sdir):
    """The study's own central fair value and the spot it was struck at.

    Returns (central, spot, route) or (None, None, why). Deliberately tries the shapes the
    studies in this repository actually use rather than one canonical schema — and returns
    the ROUTE it took, because a number found by a fallback is not the same evidence as one
    found where it belongs.

    A TWO-SIDED study returns central None with a route that SAYS SO, and its
    branches come from read_branches(). Callers must distinguish that from an
    unreadable study: one has published an answer this repository's scalar shape
    cannot hold, the other has published nothing.
    """
    for fn in ('study_numbers.json', 'numbers.json'):
        p = os.path.join(sdir, fn)
        if not os.path.exists(p):
            continue
        try:
            j = json.load(open(p, encoding='utf-8'))
        except Exception as e:
            return None, None, 'unreadable %s: %s' % (fn, e)
        meta = j.get('meta') or {}
        central = _num(j.get('central')) or _num(j.get('fair')) or _num(meta.get('central'))
        spot = _num(j.get('spot')) or _num(meta.get('spot'))
        if central is not None and spot:
            return central, spot, fn
        branches = read_branches(sdir)
        if branches and spot:
            return None, spot, TWO_SIDED % (fn, len(branches))
        return None, None, '%s carries no central/spot pair' % fn
    return None, None, 'no committed numbers file'


def read_review(sdir):
    """The most recent gap review in a study directory, and the headings it covers."""
    hits = sorted(glob.glob(os.path.join(sdir, REVIEW_GLOB)))
    if not hits:
        return None, [], None, [], None
    raw = open(hits[-1], encoding='utf-8').read()
    txt = raw.upper()
    covered = [k for k in REQUIRED_SECTIONS if k in txt]
    return (os.path.basename(hits[-1]), covered, _audited_central(raw),
            _audited_centrals(raw), _audited_gap(raw))


# A REVIEW AUDITS AN ANSWER, AND THE ANSWER MOVES. On 2 September 2026 EGCH's
# central went from 3.76 to -1.06 while its review — written for 3.76 — sat in
# the directory unchanged, and this gate passed the study, because it checked
# that a review EXISTED and covered the eight headings and never that it audited
# the number the study now publishes. A check that green-lights a stale artefact
# is reporting on something nobody receives, which is the same species as a gate
# opening a superseded workbook.
#
# The review therefore states the central it audited, on its own line, and this
# gate compares. The marker is deliberately plain text a person writing a review
# will produce anyway.
AUDITED_RX = re.compile(
    r'AUDITED[ _]CENTRAL\s*[:=]\s*(-?[0-9][0-9,]*\.?[0-9]*)', re.I)
AUDIT_TOL = 0.005          # half a per cent of the central, not a round number:
                           # a review is stale when the answer has MOVED, not when
                           # it has been re-rounded

# A REVIEW AUDITS A DISAGREEMENT, AND THE DISAGREEMENT MOVES EVEN WHEN THE ANSWER
# DOES NOT [added 03-Sep-2026, per the principal: "the gate checks a review audits
# the current answer, not the current gap — that's why all four pass while every
# one was written for a much smaller disagreement"].
#
# The AUDITED CENTRAL marker was added on 02-Sep-2026 and closed a real hole: a
# review written for a central the study no longer publishes. It does not close
# this one. A review can audit exactly the right central and still have been
# written against a price four weeks old, and the whole point of the eight
# headings is to interrogate a DISAGREEMENT — how large it is is the question,
# not a detail beside it.
#
# Measured on the day it was named: PHDC's review audits 17.1517, which is
# precisely what the study publishes, so this gate passed it — while the review
# was written at +12.8% against a strike price of 15.20 and the day's price of
# 14.40 makes the gap +19.1%. A review of a 13% disagreement is not a review of a
# 19% one; a reader reaches the headings expecting them to have been asked at the
# size the study now carries.
#
# So a review states the GAP it audited as well as the central, and this gate
# compares both. The tolerance is in PERCENTAGE POINTS of gap rather than
# relative, because the thing that matters is how far the disagreement has moved
# in the units the trigger itself is stated in.
AUDITED_GAP_RX = re.compile(
    r'AUDITED[ _]GAP\s*[:=]\s*([+-]?[0-9][0-9,]*\.?[0-9]*)\s*%', re.I)
AUDIT_GAP_TOL = 0.05       # five percentage points of gap. NOT a new free parameter:
                           # it is half the ten-point trigger this rule is stated in,
                           # so a review goes stale when the disagreement has moved by
                           # half the distance that would have triggered one from
                           # nothing. Anything tighter would fire on a price that
                           # simply moved a little between build and delivery.


def _audited_centrals(raw):
    """EVERY audited-central line in a review, not just the first.

    A two-sided study has two answers, and a review that audits one of them has
    audited half the study. findall rather than search for exactly that reason.
    """
    out = []
    for m in AUDITED_RX.finditer(raw):
        try:
            out.append(float(m.group(1).replace(',', '')))
        except ValueError:
            continue
    return out


def _audited_central(raw):
    vals = _audited_centrals(raw)
    return vals[0] if vals else None


def _audited_gap(raw):
    """The gap a review states it audited, as a fraction, or None."""
    m = AUDITED_GAP_RX.search(raw)
    if not m:
        return None
    try:
        return float(m.group(1).replace(',', '')) / 100.0
    except ValueError:
        return None


def load_outstanding():
    d = json.load(open(OUTSTANDING, encoding='utf-8'))
    return (d, set(d.get('breach_no_review', [])), set(d.get('unreadable', [])),
            set(d.get('review_central_unstated', [])))


# A DIRECTORY THAT IS NOT AN EQUITY VALUATION IS EXEMPT, AND THE EXEMPTION IS EXECUTED
# RATHER THAN DECLARED [added 05-Sep-2026].
#
# gap_outstanding.json has carried an `exempt` block since the rule was seeded — "XPT:
# metals study - no issuer, no equity fair value of this shape" — and NOTHING READ IT.
# So the same name sat in `unreadable` as well, as a defect to be cleared, and it can
# never be cleared: a metal has no issuer, no statements and no equity, so there is no
# central fair value for it to expose. A permanently-uncleara ble entry on a ratchet is
# the permanently-red check [R-ENF-02] forbids, one level down — it makes the
# outstanding list one longer than it is and implies work nobody can ever do.
#
# The exemption is now enforced, and it is deliberately narrow so it cannot become an
# escape hatch:
#   * it needs a REASON, and an empty one fails rather than exempting;
#   * every exempt name is PRINTED, because an exemption a reader cannot see is
#     indistinguishable from a study the gate silently skipped;
#   * an exempt study that DOES expose a central FAILS. That is the clause that keeps
#     it honest: the exemption says "this is not an equity valuation", so a central
#     appearing there means either the exemption is wrong or the study is, and both
#     are findings rather than passes.
def exemptions(d):
    ex = d.get('exempt') or {}
    bad = [k for k, v in ex.items() if not str(v or '').strip()]
    return ex, bad


def resolve_population():
    """THE SEAM. The gate resolves its population through one call so the
    negative control can substitute a fixture and test THIS gate's logic,
    while engine/study_population.py is negative-controlled separately on its
    own eight conditions. Each instrument tested on what it decides.

    THE IMPORT IS LAZY, AND THAT IS NOT TIDINESS. A first draft imported
    study_population at module level behind a sys.path insert computed from
    __file__, which broke every OTHER gate's sandbox that copies this script
    without engine/ beside it: check_artefact_currency's negative control went
    red on all ten of its cases with ModuleNotFoundError, and three of them
    were scored 'ok' — a control reporting the right verdict for the wrong
    reason, which reads exactly like the right one [R-ENF-07]. Importing here
    means a caller that substitutes this function never needs the module at
    all, which is what a seam is for.
    """
    engine = os.path.join(ROOT, 'engine')
    if engine not in sys.path:
        sys.path.insert(0, engine)
    import study_population
    return study_population.population()


def resolve_no_record(pop):
    """The shared no-record ratchet, read through the same lazy seam. A second
    seam so the negative control can supply both halves of the fixture."""
    engine = os.path.join(ROOT, 'engine')
    if engine not in sys.path:
        sys.path.insert(0, engine)
    import study_population
    return study_population.no_record_ratchet(pop)


def main(argv):
    prune = '--prune' in argv
    (d, known_breach, known_unreadable, known_unstated) = load_outstanding()

    # THE POPULATION IS THE BOOK. Every covered name carries a delivered study;
    # what varies is whether it also commits a record this gate can read.
    pop = resolve_population()
    # THE NO-RECORD SET IS SHARED, NOT THIS GATE'S. It was kept here for one day
    # and moved the moment the ten sibling gates were surveyed: ten gates keeping
    # ten copies of the same 67 names is the twenty-three-hand-maintained-sets
    # mistake, and it would have written one fact into the exemplar ratchet ten
    # times over. It stays a ratchet — a name that LOSES its record goes red.
    known_no_record, _nr_problems = resolve_no_record(pop)
    ok, breaches, unreadable, reviewed, new_fail = [], [], [], [], []
    no_record = []
    exempt, exempt_no_reason = exemptions(d)
    exempted = []
    for k in sorted(exempt_no_reason):
        new_fail.append('%s is listed exempt with no reason. An exemption without one is '
                        'a name switched off, not a name excused.' % k)

    # [R-ENF-04] ANCHORED BOTH WAYS, against a population this gate does not own
    if not pop:
        new_fail.append('this gate examined ZERO covered names. An empty result is not '
                        'a clean result — re-run the resolver before believing it.')
    for _m in _nr_problems:
        new_fail.append(_m)
    vanished = sorted((known_breach | known_unreadable) - set(pop))
    if vanished:
        new_fail.append('%d name(s) in gap_outstanding.json resolve to no covered name '
                        '(%s). Either the resolver did not run or the names left the '
                        'book without the list being pruned; neither is a pass.'
                        % (len(vanished), ', '.join(vanished)))
    # THE TWO GROUPS EXCUSE TWO DIFFERENT CONDITIONS AND ARE NOT INTERCHANGEABLE
    both = sorted(known_unreadable & known_no_record)   # noqa: E501  see note above
    if both:
        new_fail.append('%s listed in BOTH no_record_dir and unreadable. They excuse '
                        'different conditions — no record to read, versus a record whose '
                        'numbers expose no answer — and a name carrying both allowances '
                        'escapes whichever one it actually breaches.' % ', '.join(both))

    price_notes, price_basis = [], []
    for tk in sorted(pop):
        sdir = pop[tk]['record_dir']
        if sdir is None:
            # DELIVERED, AND INVISIBLE TO EVERY RECORD-READING GATE. Not skipped and
            # not silently narrowed away: this is the state the re-pointing exists to
            # make countable, and under [R-ENF-04] it is UNREADABLE, which is not CLEAN.
            no_record.append((tk, len(pop[tk]['delivered'])))
            # the shared reader above has already reported any name missing from the
            # ratchet; reporting it again here would say one fact twice
            continue
        central, spot, route = read_answer(sdir)
        if tk in exempt:
            exempted.append((tk, exempt[tk]))
            if central is not None:
                new_fail.append(
                    '%s is listed exempt from this gate — %r — and its committed numbers '
                    'DO resolve to a central fair value of %.4f. Either the exemption is '
                    'wrong or the study is; an exemption is not a place to put an answer '
                    'nobody wants audited.' % (tk, exempt[tk], central))
            continue
        # [R-GAP-01] compares against THE LATEST KNOWN MARKET PRICE. Prefer the
        # house's own price library over the spot the study froze at strike; fall
        # back to the struck spot only where no library resolves, and say which was
        # used and how old it is, because a comparison against a four-week-old close
        # is a weaker claim than one against today's and must not read the same.
        if spot:
            live, pxdate, pxsrc = latest_known_price(tk)
            if live:
                price_basis.append((tk, pxdate))
                if abs(live - spot) > max(0.005 * spot, 0.005):
                    price_notes.append('%s: struck at %.2f, latest known %.2f (%s)'
                                       % (tk, spot, live, pxdate))
                spot = live
            else:
                price_notes.append('%s: no price library (%s) — compared against the '
                                   'struck spot, which is a fallback and not the rule'
                                   % (tk, pxsrc))
        if central is None and spot:
            branches = read_branches(sdir)
            if branches:
                # A TWO-SIDED ANSWER IS AUDITED ON EVERY BRANCH. Publishing two
                # numbers instead of one is not a way to publish two unaudited
                # numbers: each branch outside the band needs the review to exist,
                # to cover the headings, and to state THAT branch as an audited
                # central. A review naming one of two answers has audited half the
                # study.
                out = [b for b in branches
                       if not (GAP_LIMIT <= b["value"] / spot - 1.0 <= GAP_LIMIT_ABOVE)]
                if not out:
                    ok.append((tk, 0.0))
                    continue
                review, covered, _a, audited_all, _ag = read_review(sdir)
                missing = [k for k in REQUIRED_SECTIONS if k not in covered]
                unaudited = [b for b in out
                             if not any(abs(a - b["value"])
                                        <= max(AUDIT_TOL * abs(b["value"]), 0.005)
                                        for a in audited_all)]
                if review and not missing and not unaudited:
                    reviewed.append((tk, min(b["value"] / spot - 1.0 for b in out),
                                     review, audited_all[0] if audited_all else None))
                    continue
                breaches.append((tk, min(b["value"] / spot - 1.0 for b in out),
                                 review, missing, None, bool(unaudited)))
                if tk not in known_breach and tk not in known_unstated:
                    if not review:
                        why = 'no gap review in the study directory'
                    elif missing:
                        why = ('the review %s does not cover %s'
                               % (review, ', '.join(missing)))
                    else:
                        why = ('the review %s states no audited central for %s. A '
                               'two-sided answer is audited on EVERY branch; a review '
                               'naming one of two answers has audited half the study.'
                               % (review, '; '.join('%s (%.4f)' % (b["label"], b["value"])
                                                    for b in unaudited)))
                    new_fail.append('%s: publishes %d branches and no single central, '
                                    '%d of them outside the band, and %s.'
                                    % (tk, len(branches), len(out), why))
                continue
        if central is None:
            unreadable.append((tk, route))
            if tk not in known_unreadable:
                new_fail.append('%s: its committed numbers do not resolve to a central fair '
                                'value and a spot (%s). A study whose answer cannot be read '
                                'is not a study that passed.' % (tk, route))
            continue
        gap = central / spot - 1.0
        if GAP_LIMIT <= gap <= GAP_LIMIT_ABOVE:
            ok.append((tk, gap))
            continue
        side = 'below' if gap < 0 else 'above'
        review, covered, audited, audited_all, audited_gap = read_review(sdir)
        missing = [k for k in REQUIRED_SECTIONS if k not in covered]
        if review and not missing and audited is None and tk not in known_unstated:
            new_fail.append('%s: the review %s states no AUDITED CENTRAL, so nothing '
                            'can tell whether it audits the answer the study now '
                            'publishes.' % (tk, review))
        stale = (audited is not None
                 and abs(audited - central) > max(AUDIT_TOL * abs(central), 0.005))
        # the SECOND way a review goes stale: the answer stood still and the
        # disagreement moved
        gap_stale = (audited_gap is not None and gap is not None
                     and abs(audited_gap - gap) > AUDIT_GAP_TOL)
        stale = stale or gap_stale
        if review and not missing and not stale:
            reviewed.append((tk, gap, review, audited))
            continue
        breaches.append((tk, gap, review, missing, audited, stale))
        if tk not in known_breach and tk not in known_unstated:
            if not review:
                why = 'no gap review in the study directory'
            elif missing:
                why = 'the review %s does not cover %s' % (review, ', '.join(missing))
            elif gap_stale:
                why = ('the review %s audits a gap of %+.1f%% while the study now sits '
                       'at %+.1f%% against the latest known price. The answer has not '
                       'moved and the DISAGREEMENT has, and the eight headings exist to '
                       'interrogate a disagreement at the size it actually is.'
                       % (review, 100 * audited_gap, 100 * gap))
            elif stale:
                why = ('the review %s audits a central of %.4f while the study now '
                       'publishes %.4f. A review of a number the study no longer '
                       'carries is not a review of this study.'
                       % (review, audited, central))
            else:
                why = 'the review %s states no audited central' % review
            new_fail.append('%s: central is %.1f%% %s the spot it was struck at, and %s.'
                            % (tk, abs(100 * gap), side, why))

    print('covered names (every one carrying a delivered study): %d' % len(pop))
    print('  answer READ and audited : %d   reviewed: %d   breaching: %d'
          % (len(ok) + len(reviewed) + len(breaches), len(reviewed), len(breaches)))
    print('  record present, answer unreadable : %d' % len(unreadable))
    print('  NO RECORD DIRECTORY AT ALL        : %d   exempt: %d'
          % (len(no_record), len(exempted)))
    # [R-ENF-04] BOTH WAYS: zero names fails above, and zero answers READ across
    # present names fails here — the distinction an absent answer hides behind
    if pop and not (ok or reviewed or breaches):
        new_fail.append('this gate READ zero answers across %d covered names. A run that '
                        'examined a population and resolved nothing in it is an absent '
                        'result, not a clean one.' % len(pop))
    for tk, why in sorted(exempted):
        # printed, never silent: an exemption a reader cannot see is indistinguishable
        # from a study this gate quietly skipped
        print('   EXEMPT  %-11s %s' % (tk, why))
    print('trigger: central more than %.0f%% BELOW or %.0f%% ABOVE the spot it was struck at\n'
          % (-100 * GAP_LIMIT, 100 * GAP_LIMIT_ABOVE))

    if reviewed:
        print('OUTSIDE THE BAND, AND REVIEWED (%d):' % len(reviewed))
        for tk, gap, rv, aud in reviewed:
            print('   %-12s %+6.1f%%  %s%s'
                  % (tk, 100 * gap, rv,
                     '' if aud is None else '  (audits %.4f)' % aud))
    if breaches:
        print('\nOUTSIDE THE BAND, NOT REVIEWED (%d):' % len(breaches))
        for tk, gap, rv, missing, aud, stale in breaches:
            state = ('no review' if not rv
                     else ('missing: ' + ', '.join(missing)) if missing
                     else ('STALE — audits %.4f' % aud) if (stale and aud is not None)
                     # a two-sided study reaches here with no single audited
                     # number: the branch it fails on is the one the review
                     # never names, which the failure line above spells out
                     else 'a branch with no audited central stated' if stale
                     else 'no audited central stated')
            print('   %-12s %+6.1f%%  %s' % (tk, 100 * gap, state))
    if unreadable:
        print('\nANSWER NOT READABLE (%d) — tracked, because an unreadable answer is not a '
              'clean one:' % len(unreadable))
        for tk, why in unreadable:
            print('   %-12s %s' % (tk, why))
    if no_record:
        print('\nDELIVERED, WITH NO RECORD ANY GATE CAN READ (%d) — the fair value is '
              'published and has never been put against a price by this gate:'
              % len(no_record))
        names = sorted(t for t, _ in no_record)
        for i in range(0, len(names), 6):
            print('   ' + ', '.join(names[i:i + 6]))

    now_passing = sorted(({b[0] for b in breaches} ^ known_breach) & known_breach) + \
        sorted(({tk for tk, _ in unreadable} ^ known_unreadable) & known_unreadable)
    if now_passing:
        print('\nNOW PASSING — remove from the list (%d): %s'
              % (len(now_passing), ', '.join(now_passing)))

    if prune:
        d['breach_no_review'] = sorted({b[0] for b in breaches} & known_breach)
        d['unreadable'] = sorted({tk for tk, _ in unreadable} & known_unreadable)
        json.dump(d, open(OUTSTANDING, 'w'), indent=1)
        print('\npruned; %d breach + %d unreadable remain (the no-record set is a '
              'shared ratchet and is pruned where it lives)'
              % (len(d['breach_no_review']), len(d['unreadable'])))
        return 0

    if new_fail:
        print('\nFAIL — %d new violation(s):' % len(new_fail))
        for m in new_fail:
            print('   ' + m)
        print('\nA fair value far from the traded price, in EITHER direction, is the case '
              'where the market is telling you something the model may have missed. Write '
              'the review, or fix what it would have found.')
        return 1
    # THE PRICE BASIS IS ALWAYS STATED, NEVER ONLY WHEN IT DIVERGES. The gate now
    # reads the price library, and on the calibrated names the library AGREES with
    # every struck spot — because each study was struck on its library's last row.
    # That is not the comparison being current: it means the house's own LATEST
    # KNOWN price is as old as the library, and how old is exactly what a reader
    # has to be told. A basis printed only on divergence would report a four-week-old
    # comparison in silence, which is the staleness this reading was changed to end.
    if price_basis:
        print('\n  PRICE BASIS — [R-GAP-01] compares against the LATEST KNOWN price:')
        print('    %d of %d readable studies compared against their own OHLC library'
              % (len(price_basis), len(ok) + len(reviewed) + len(breaches)))
        for t, d in sorted(price_basis, key=lambda x: x[1])[:6]:
            print('      %-12s last close %s' % (t, d))
        print('    a library that has stopped is a stale comparison, not a passing one;'
              '\n    only a fresh export moves it.')
    if price_notes:
        print('\n  where the struck spot and the latest known price DIVERGE:')
        for n in price_notes:
            print('    %s' % n)

    print('\nOK — no new violations.')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
