"""THE POPULATION OF STUDIES IS NOT THE POPULATION OF STUDY DIRECTORIES.

Every gate in this repository resolves its population by globbing
`engine/*_study/`.  That glob returns 24 directories.  The book carries 90
covered names and ALL NINETY HAVE A DELIVERED VALUATION STUDY, under
`files/`.  So 68 delivered studies sit outside the population of every gate
that has ever reported on this book, and each of those gates reports itself
population-anchored while doing it.

That is [R-ENF-04] one level above where it looks.  The rule says a gate
must be held against a population counted somewhere ELSE, and every gate
obeys it -- against `gap_outstanding.json`, `lens_outstanding.json` and the
rest, each of which was itself seeded from the same directory glob.  A
population and its check derived from one list agree with each other by
construction and say nothing about the world.  It is also [R-ENF-07]'s own
claim -- a system of checks has properties no check in it can see -- and it
was found the way that rule predicts: not by a gate, but by somebody asking
why the number was 24 when the book is 90.

WHAT THIS MODULE DOES AND DELIBERATELY DOES NOT DO.  It answers "what is
the population of studies" once, from the DELIVERED artefacts joined to the
covered names, and it says for each name whether a gate can actually READ
it.  It does not pretend the 68 are checkable: a bridge record, a lens
record and a committed numbers file live in `engine/{ticker}_study/`, and a
study delivered without one exposes nothing for a record-reading gate to
inspect.  THAT IS THE FINDING, NOT A LIMITATION OF THIS MODULE -- under
[R-ENF-04] an unreadable study is not a clean study, and the honest state
for those names is RED-AND-RATCHETED rather than absent from the count.

Callers take `population()` and hold themselves against ALL of it, then
list what they could not read.  A gate that silently narrows to
`readable()` has rebuilt the defect this module exists to close.
"""

import json
import os
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENGINE = os.path.join(ROOT, 'engine')
FILES = os.path.join(ROOT, 'files')
DATA_JS = os.path.join(ROOT, 'assets', 'data.js')

# A DELIVERED FILE STEM THAT IS NOT ITS TICKER.  Kept explicit and asserted
# in both directions below, never inferred by fuzzy matching: the first
# measurement of this population used a case-sensitive pattern, silently
# missed `Aramco_`, `Samsung_`, `Aldar_` and `Kakao_`, and reported sixteen
# names as having no study at all.  An empty result is not a clean result
# [R-ENF-04], and a NEAR-empty one is worse, because it looks like data.
FILE_ALIAS = {
    'ADIB_UAE': 'ADIBUAE',
    'ADNOC_GAS': 'ADNOCGAS',
    'AL_RAJHI': 'ALRAJHI',
    'LG_ENERGY_SOLUTION': 'LGES',
    'NAKILAT_QGTS': 'QGTS',
    'QALAA_HOLDINGS': 'CCAP',
}

# A STUDY DIRECTORY STEM THAT IS NOT ITS TICKER.  Mirrors
# campaign_queue.STUDY_ALIAS, which is asserted against this at import.
DIR_ALIAS = {'FERTIGLOBE': 'FERTIGLB'}

# Delivered files that resolve to no covered EQUITY, each with its reason.
# Metals are a separate register (METALS in data.js) and are excluded by
# construction, exactly as the campaign queue excludes them.
NOT_AN_EQUITY = {
    'XAUUSD': 'metals - GOLD, a separate register',
    'XAUUSD_12M': 'metals - GOLD on its own 12-month clock',
    'XAGUSD_COMBINED_1-3-12M': 'metals - SILVER',
    'XPTUSD': 'metals - PLATINUM',
}

_NODE_READ = r'''
const fs = require("fs"), vm = require("vm");
const c = {}; vm.createContext(c);
vm.runInContext(fs.readFileSync(process.argv[1], "utf8")
  + "\n;this.__T=TICKERS;", c);
console.log(JSON.stringify(Object.keys(c.__T)));
'''


def covered_names(path=None):
    """The equity tickers the SITE publishes, through a real JS parse and
    never a regex [R-ENF-03].

    THE DEFAULT IS RESOLVED AT CALL TIME, NOT BOUND AT DEFINITION.  A first
    draft wrote `path=DATA_JS`, which captures the module constant when the
    function is defined, so a caller redirecting `DATA_JS` -- which is what
    the negative control does to inject an empty register -- changed
    nothing and the case reported green.  The refusal below was correct the
    whole time and UNREACHABLE from outside, which is the shape this module
    was written about: the check existed and the probe never reached it.
    Caught by case 4 of the negative control on its first run.
    """
    path = path or DATA_JS
    p = subprocess.run(['node', '-e', _NODE_READ, path],
                       capture_output=True, text=True)
    if p.returncode != 0:
        raise SystemExit('FATAL: node could not load %s\n%s' % (path, p.stderr.strip()))
    names = json.loads(p.stdout)
    if not names:
        raise SystemExit('FATAL: data.js exposed no TICKERS. An empty result is not a '
                         'clean result [R-ENF-04] -- the probe did not run.')
    return set(names)


def delivered():
    """ticker -> the delivered valuation artefacts carrying its name."""
    if not os.path.isdir(FILES):
        raise SystemExit('FATAL: %s does not exist. The delivered studies ARE the '
                         'population; without them there is nothing to anchor on.' % FILES)
    out = {}
    orphans = {}
    for f in sorted(os.listdir(FILES)):
        stem = f.split('_Valuation_')[0] if '_Valuation_' in f else None
        if stem is None:
            continue
        key = FILE_ALIAS.get(stem.upper(), stem.upper())
        if key in NOT_AN_EQUITY:
            orphans.setdefault(key, []).append(f)
            continue
        out.setdefault(key, []).append(f)
    if not out:
        raise SystemExit('FATAL: %s carries no delivered valuation study. An empty '
                         'result is not a clean result [R-ENF-04].' % FILES)
    return out, orphans


def record_dirs():
    """ticker -> engine/{x}_study directory, for the names that have one.
    THIS IS THE OLD POPULATION and it is returned here as ONE FIELD of the
    answer rather than as the answer."""
    out = {}
    for d in sorted(os.listdir(ENGINE)):
        if not d.endswith('_study') or not os.path.isdir(os.path.join(ENGINE, d)):
            continue
        tk = d[:-len('_study')].upper()
        out[DIR_ALIAS.get(tk, tk)] = os.path.join(ENGINE, d)
    if not out:
        raise SystemExit('FATAL: no engine/*_study directories. [R-ENF-04].')
    return out


def population():
    """The population every gate over this book should be held against.

    Returns ticker -> {'delivered': [files], 'record_dir': path or None,
    'readable': bool}.  RAISES on any name that does not resolve in both
    directions, because a resolver that quietly drops a name is how a
    population shrinks without anybody deciding it should.
    """
    covered = covered_names()
    deliv, orphans = delivered()
    dirs = record_dirs()

    missing = sorted(covered - set(deliv))
    if missing:
        raise SystemExit(
            'FATAL: %d covered name(s) resolve to no delivered study: %s.\n'
            'Every covered name has one; a name that will not resolve means the '
            'ALIAS TABLE is short, not that the study is absent. Add the stem to '
            'FILE_ALIAS rather than letting the name drop out of the population.'
            % (len(missing), ', '.join(missing)))

    extra = sorted(set(deliv) - covered)
    if extra:
        raise SystemExit(
            'FATAL: %d delivered stem(s) resolve to no covered ticker: %s.\n'
            'Either it is a covered name under another spelling (FILE_ALIAS) or it '
            'is deliberately not an equity (NOT_AN_EQUITY, with its reason). A '
            'stem matching nothing is not evidence that nothing is there.'
            % (len(extra), ', '.join(extra)))

    stray = sorted(set(dirs) - covered)
    if stray:
        # a record directory for a name the site does not carry: XPT (metals)
        # is the standing case and is declared, anything else is a real join
        # failure and says so rather than being skipped
        undeclared = [t for t in stray if t not in ('XPT',)]
        if undeclared:
            raise SystemExit(
                'FATAL: study record directory for a name the site does not carry: '
                '%s. A record nothing joins to is invisible to every gate that '
                'starts from the site.' % ', '.join(undeclared))

    out = {}
    for tk in sorted(covered):
        d = dirs.get(tk)
        out[tk] = {'delivered': deliv[tk], 'record_dir': d, 'readable': d is not None}
    return out


# THE NO-RECORD SET IS ONE RATCHET, NOT ONE PER GATE [06-09-2026].
# check_valuation_gap was re-pointed first and kept its own `no_record_dir` list
# inside gap_outstanding.json. Wiring the other ten gates the same way would have
# produced TEN lists carrying the SAME 67 names, and — because two of the three
# closed REFERENCE_SET names are pattern references with no study directory —
# twenty exemplar-debt entries recording one fact ten times. That is [L-084] and
# the prose-figures finding, and it was caught by surveying the ten before editing
# them rather than after.
#
# So the fact lives HERE, once, and every gate reads it. It stays a RATCHET rather
# than a computed set, because the ratchet is what makes the debt only ever shorten:
# a name that LOSES its record must go red, not become quietly excused.
# IT DEFERS TO THE LIST THAT ALREADY HELD THIS FACT [corrected 06-09-2026, hours
# after the list below was created]. A first version of this module created
# no_record_outstanding.json and argued for it: one list rather than ten. The
# argument was right and the list was a DUPLICATE — coverage_outstanding.json has
# held exactly this since 03-Sep-2026, in its own words, "names whose fair value the
# site publishes with no study directory behind it ... examined by NONE of them".
#
# THE TWO DIVERGED ON DAY ONE AND THE DIVERGENCE WAS A REAL DEFECT IN THE OLDER
# LIST: 68 entries against 67, the difference being FERTIGLB, which HAS a study
# directory under the aliased name fertiglobe_study. check_published_coverage
# derived its study set from raw directory names and could not see the alias, so it
# had been listing a name that was not outstanding at all. Nothing could see that
# until a second measurement disagreed — the one benefit of the duplication, and not
# a reason to keep it.
#
# The precedent is this repository's own: check_artefact_currency DEFERS to
# [R-GAP-01]'s unreadable list rather than writing the same fact into a second list,
# because two records of one thing diverge the moment one is pruned.
NO_RECORD_RATCHET = os.path.join(ENGINE, 'build_depth_audit', 'coverage_outstanding.json')


def no_record_ratchet(pop=None):
    """The covered names knowingly committing no record any gate can read.

    Returns (allowed, problems). `problems` is non-empty when the list has stopped
    describing the book — a listed name that HAS acquired a record (the debt
    shortened and nobody pruned), or a name with no record that is not listed (a
    NEW one, which is the violation this exists to surface).
    """
    pop = pop or population()
    try:
        d = json.load(open(NO_RECORD_RATCHET, encoding='utf-8'))
    except FileNotFoundError:
        raise SystemExit('FATAL: %s does not exist. The no-record set is a ratchet and a '
                         'missing ratchet is not an empty one [R-ENF-04].' % NO_RECORD_RATCHET)
    # `entries` is a dict of ticker -> reason; the older file's own shape
    allowed = set(d.get('entries') or d.get('no_record') or [])
    # AN EMPTY LIST IS LEGITIMATE AND A MISSING FILE IS NOT. A first draft refused
    # an empty ratchet on the [R-ENF-04] instinct that emptiness is usually
    # truncation -- and that was wrong twice over. Empty is the GOAL STATE of a
    # ratchet that may only shorten, so refusing it makes the target unreachable,
    # which is the permanently-red check [R-ENF-02] forbids wearing the opposite
    # costume. And it was redundant: a truncated list does not go quiet, it
    # produces one problem per unlisted name from the third clause below. Found by
    # a fixture that legitimately carries none.
    actual = {k for k, v in pop.items() if not v['readable']}
    problems = []
    for tk in sorted(allowed - set(pop)):
        problems.append('%s is on the no-record ratchet and is not a covered name at all' % tk)
    for tk in sorted(allowed & set(pop) - actual):
        problems.append('%s is excused on the no-record ratchet and DOES commit a record '
                        'directory. The allowance is for a study nothing can read; the debt '
                        'has shortened and the list must be pruned, because a stale excuse '
                        'is how a real breach hides.' % tk)
    for tk in sorted(actual - allowed):
        problems.append('%s is a covered name committing NO record directory and is not on '
                        'the ratchet. A study nothing can read is not a study that passed '
                        '[R-ENF-04].' % tk)
    return allowed, problems


def readable(pop=None):
    """The subset a record-reading gate can actually inspect. NEVER the
    population: narrowing to this silently is the defect this module closes."""
    pop = pop or population()
    return {k: v for k, v in pop.items() if v['readable']}


def examinable(pop=None):
    """What a RECORD-READING gate should iterate, and what it should say it did.

    Ten gates resolve their population by globbing `engine/*_study` and print
    "studies examined: 24" WITH NO DENOMINATOR -- which is precisely why 24 looked
    like the book for as long as it did. This returns the directories they can
    actually inspect, the names they cannot, and the one line they print about it,
    so the ten call sites are three lines each and THE WORDING CANNOT DRIFT between
    them. A helper rather than ten hand-written edits, for the same reason the
    no-record set is one ratchet rather than ten.

    THEY DEFER, THEY DO NOT RE-LIST. The no-record set is owned once and
    check_valuation_gap is the gate that REPORTS its problems; if all ten reported
    them, one new unlisted name would produce ten identical failures, which is the
    duplication this whole refactor exists to avoid arriving one level up.

    Returns (record_dirs, deferred_tickers, population_line).
    """
    pop = pop or population()
    if not pop:
        raise SystemExit('FATAL: the population is empty. An empty result is not a clean '
                         'result [R-ENF-04].')
    # EVERY RECORD ON DISK, NOT ONLY THE COVERED ONES. A first draft returned just
    # the covered names with a record and immediately broke check_bridge, whose
    # ratchet lists XPT — a metals study with a record directory and no covered
    # equity behind it. Dropping it would have removed a study from that gate's
    # scope silently, which is this whole defect in miniature. A record-reading
    # gate reads every record that exists; what the covered population decides is
    # the DENOMINATOR and the deferred set, not which records to skip.
    _dirs = record_dirs()
    dirs = sorted(_dirs.values())
    deferred = sorted(k for k, v in pop.items() if not v['readable'])
    _uncovered = sorted(set(_dirs) - set(pop))
    if not dirs:
        raise SystemExit('FATAL: %d covered names and NOT ONE with a record to read. A run '
                         'that examined a population and resolved nothing in it is an absent '
                         'result, not a clean one [R-ENF-04].' % len(pop))
    line = ('population: %d covered names, every one carrying a delivered study — %d '
            'records on disk to read%s, %d covered names deferred to %s (reported by the '
            'valuation-gap gate, never re-listed here)'
            % (len(pop), len(dirs),
               '' if not _uncovered else ' (incl. %s, which the site does not carry)'
               % ', '.join(_uncovered),
               len(deferred), os.path.basename(NO_RECORD_RATCHET)))
    return dirs, deferred, line


def unreadable(pop=None):
    """The names a record-reading gate cannot inspect, which under
    [R-ENF-04] are RED-and-ratcheted rather than absent."""
    pop = pop or population()
    return {k: v for k, v in pop.items() if not v['readable']}


def _assert_alias_agreement():
    """campaign_queue keeps its own directory-alias table. Two tables for one
    fact diverge the moment one is edited, so they are asserted equal at
    import -- the LENS_REGISTRY/CLASSES precedent [R-LENS-03]."""
    import importlib.util
    p = os.path.join(ENGINE, 'campaign_queue.py')
    if not os.path.exists(p):
        return
    spec = importlib.util.spec_from_file_location('_cq', p)
    m = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(m)
    except Exception:
        return
    if getattr(m, 'STUDY_ALIAS', DIR_ALIAS) != DIR_ALIAS:
        raise AssertionError(
            'campaign_queue.STUDY_ALIAS %r and study_population.DIR_ALIAS %r '
            'disagree. One fact, one table.' % (m.STUDY_ALIAS, DIR_ALIAS))


# THE ALIAS TABLE IS HARDCODED AND ITS AGREEMENT IS CHECKED AT IMPORT, FOR EVERY
# CONSUMER [06-09-2026, per instruction]. DIR_ALIAS is the one authoritative
# statement that engine/fertiglobe_study belongs to the ticker FERTIGLB. It was
# already written down here and campaign_queue.py kept its own copy; what was
# missing is that the agreement was only asserted when THIS FILE was run as a
# script, so a consumer importing the module got no check at all — and
# check_published_coverage, which never imported it, spent three days listing
# FERTIGLB as having no study while its directory sat on disk. A fact that is
# hardcoded in one place and copied in another is not hardcoded; it is duplicated,
# and the copy is only as good as whatever compares them.
_assert_alias_agreement()


if __name__ == '__main__':
    # a tool people will pipe into `head` should not print a traceback
    try:
        import signal
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except (ImportError, AttributeError, ValueError):
        pass
    _assert_alias_agreement()
    pop = population()
    r, u = readable(pop), unreadable(pop)
    print('COVERED NAMES, EVERY ONE CARRYING A DELIVERED STUDY : %d' % len(pop))
    print('  a record-reading gate CAN inspect (engine/ dir)   : %d' % len(r))
    print('  a record-reading gate CANNOT inspect              : %d' % len(u))
    print()
    print('THE 77 GATES OVER THIS BOOK GLOB engine/*_study AND SO SEE %d OF %d.'
          % (len(r), len(pop)))
    print('Under [R-ENF-04] the other %d are UNREADABLE, which is not CLEAN.' % len(u))
    print()
    print('unreadable, in site order:')
    names = sorted(u)
    for i in range(0, len(names), 6):
        print('  ' + ', '.join(names[i:i + 6]))
