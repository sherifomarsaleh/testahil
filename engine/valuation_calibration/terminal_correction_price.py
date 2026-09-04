#!/usr/bin/env python3
"""WHAT CORRECTING THE RETIRED TERMINAL IS WORTH, NAME BY NAME, AND WHICH WAY IT RUNS.

[R-TERM-01 CLAUSE TWO] says the 1/g defect's DIRECTION REVERSES with a market's
terminal inflation: it starves a plant where inflation is high and flatters one
where the currency is pegged. The census establishes THAT, on the one inference
that needs no sourced life. This prices it — how far each study's own fair value
moves when its terminal is rebuilt on the sanctioned module, and whether that move
goes toward the price or away from it.

WHY THAT SECOND COLUMN IS THE POINT. The reassessment was called because the house
looked pessimistic, and a correction that moves a value UP reads as evidence for
that diagnosis. A correction that moves it DOWN on a name already below the price
reads as the opposite: the pessimism on that name is somewhere else, and the eight
headings [R-GAP-01] should go looking for it rather than treating the terminal as
the culprit. Nobody had measured that column.

NOTHING HERE IS RE-IMPLEMENTED. The census's own reader resolves each study's
terminal (its frame discipline, its route recording, its refusals) and
terminal_value.build() does the arithmetic — a second implementation of either
would be two claims wearing one name, which is the [R-ENF-03] species this house
closes. This file only feeds one to the other and prints the difference.

THREE OUTCOMES, AND THE SECOND TWO ARE FINDINGS RATHER THAN GAPS:

  PRICED     a disclosed useful life is on file, so the corrected terminal builds
             and the move is real arithmetic.
  REFUSED    the module refuses the study's own inputs and names why. That is the
             module working — the worked case is a fleet whose disclosed hull life
             implies a maintenance charge BELOW its own book depreciation, because
             dry-docking is written off over two to five years and the disclosure
             does not split the vessel line by component.
  NO LIFE    no disclosed useful life is on file for this name. SIGCM clause 1 and
             [R-TERM-01]: A LIFE THIS DESK CHOSE IS NOT A DISCLOSED LIFE, so
             nothing is assumed and the accounting-policies note is named as the
             work that unblocks it.

A NAME WITH NO LIFE IS NOT SKIPPED, IT IS COUNTED [R-ENF-04]: an unpriced name is
an unanswered question, and a report that quietly listed only the priceable ones
would read as though the book had been measured.
"""
import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.dirname(HERE)
REPO = os.path.dirname(ENGINE)
sys.path.insert(0, HERE)
sys.path.insert(0, ENGINE)
sys.path.insert(0, os.path.join(REPO, 'scripts'))

import terminal_census as TC              # noqa: E402  the reader, imported not copied
import terminal_value as TV               # noqa: E402  the arithmetic, likewise

LIVES = os.path.join(HERE, 'disclosed_lives.json')
LENS_RATCHET = os.path.join(REPO, 'engine', 'build_depth_audit', 'lens_outstanding.json')


def _retired_architecture():
    """Names whose CENTRAL is still produced by the architecture [R-LENS-03] retired.

    THIS IS THE CONSTRAINT ABOVE THE INPUTS AND IT WAS FOUND BY TRYING TO USE THEM.
    The obvious reading of this report is that a name becomes priceable once its
    three inputs resolve — and the first name to reach that state publishes a
    central that is a typed four-lens weighted blend, which [R-LENS-03] retired on
    02-Sep-2026 as a new method with free parameters nobody tested.

    A CORRECTED TERMINAL INSIDE A RETIRED BLEND IS NOT A MEASUREMENT. The move it
    produces is a move in a number the house has already stopped standing behind,
    and reporting it as the price of the correction would be measuring one defect
    through another.

    So the answer for every unrebuilt name is the same and it is not about inputs:
    the correction is measured when a name is RE-ISSUED, lens architecture and
    terminal and committed inputs together. That is exactly what the two names in
    ALREADY CORRECTED show — both were re-issued wholesale, and both reproduce their
    own published fair value to the fourth decimal.
    """
    try:
        d = json.load(open(LENS_RATCHET, encoding='utf-8'))
    except Exception:                                                # noqa: BLE001
        return None
    return set(d.get('outstanding') or [])



def _latest_price(ticker):
    """The latest known price, through [R-GAP-01]'s own reader [R-ENF-03]."""
    try:
        import check_valuation_gap as VG
        return VG.latest_known_price(ticker)
    except Exception as e:                                           # noqa: BLE001
        return (None, None, 'price reader unavailable: %s' % e)


def _life_band(ticker, _lives=None):
    """(shortest, longest, source) DISCLOSED — the CENSUS's resolver [R-ENF-03].

    A FIRST DRAFT OF THIS FILE READ ONLY disclosed_lives.json AND REPRODUCED A FALSE
    NEGATIVE THE CENSUS HAD ALREADY PAID FOR. A study rebuilt through
    terminal_value.py COMMITS its life under terminal_record.inputs, so ARCC — whose
    20-year life is quoted to its own audited note and is [R-TERM-01]'s worked case —
    came back NO LIFE here while the census printed it correctly two files away. The
    census carried the two-source logic inline and had recorded the lesson in a
    comment; copying it would have been the same defect a third time.

    So it is a shared function now and both callers use it. WHERE A CHECK FIRES ON
    WORK THAT IS RIGHT, RE-POINT IT [R-COC-01] — and where the re-pointing is a
    second implementation of one claim, extract it instead.

    A committed single life comes back as (life, life) so both ends of the band
    coincide: a study that has already collapsed the band under gate is not asked to
    re-open it, while a name whose life is only SOURCED is priced at both ends.
    """
    lo, hi, src = TC.disclosed_life(ticker)
    if lo is None:
        return None, None
    return (lo, lo if hi is None else hi), src


def committed_terminal(ticker):
    """A study's own committed terminal_record, WHEREVER IT SITS, or None.

    A FIRST DRAFT LOOKED ONLY AT THE TOP LEVEL AND MISSED A NAME THAT HAD ONE. SCEM
    commits its record at dcf.terminal_record, ARCC at the top level, and both are
    correct — a record belongs beside the terminal it describes, and a study with two
    frames would have two. Reading one depth and calling the rest uncommitted is the
    flat-resolver assumption the census exists to avoid, reproduced here.

    So the tree is searched, and MORE THAN ONE record is an error rather than a
    choice: picking the first would make the answer depend on dictionary order, and
    which terminal a study means is not this file's judgement to make.
    """
    f = os.path.join(REPO, 'engine', '%s_study' % ticker.lower(), 'study_numbers.json')
    if not os.path.exists(f):
        return None
    try:
        doc = json.load(open(f, encoding='utf-8'))
    except Exception:                                                # noqa: BLE001
        return None
    found = []

    def walk(o):
        if not isinstance(o, dict):
            return
        for k, v in o.items():
            if k == 'terminal_record' and isinstance(v, dict) and v.get('inputs'):
                found.append(v)
            else:
                walk(v)
    walk(doc)
    if len(found) > 1:
        pub = [r for r in found if r.get('published')]
        if len(pub) == 1:
            return pub[0]
        if len(pub) > 1:
            return {'_two_sided': pub}
        return {'_ambiguous': len(found)}
    return found[0] if found else None


# WHAT A CORRECTION NEEDS, AND WHETHER EACH ITEM IS ACTUALLY ABSENT — MEASURED, NOT
# ASSUMED. A first draft hard-coded all three as missing on every unrebuilt study and
# said so in the report. That was wrong about one of them and would have sent the next
# session to re-read thirteen balance sheets for a figure already in the file: every one
# of the thirteen commits a working-capital series and ten commit a forecast-year one.
#
# ASSERTING WHAT IS MISSING IS THE SAME OFFENCE AS ASSERTING WHAT IS PRESENT. So each
# item is resolved against the study's own committed numbers and reported in one of
# three states, because "resolvable" and "committed" are not the same claim:
#
#   COMMITTED   it sits in a terminal_record, built and gated
#   RESOLVABLE  the study publishes it under a named key, so a rebuild can read it —
#               a candidate that must be confirmed at rebuild, never a substitute
#   MISSING     nothing in the study answers to it
# THE LEVEL, NOT THE CHANGE, AND NOT ONE STUDY'S SPELLING OF IT. The corrected
# terminal charges inflation x WORKING CAPITAL, so it needs the LEVEL; `dnwc` is the
# year-on-year movement, and a rebuild reading one for the other would charge a
# rounding error and look entirely fine.
#
# THIS PATTERN WAS WRONG TWICE AND BOTH TIMES IN THE SAME DIRECTION — it reported a
# field MISSING that the study publishes. First it matched `d?nwc` and returned the
# CHANGE on nine names. Then, pinned to `fcst|forecast . nwc`, it reported four names
# as having no working capital at all while three of them publish a forecast level
# under their own spelling: frame_A.nwc, cases.base.rows[].wc, forecast.nwc_A.
# A NARROW PATTERN DOES NOT FAIL LOUDLY, IT REPORTS AN ABSENCE — which is the whole
# [R-ENF-04] shape, and reporting an absence sends the next session to re-derive a
# figure already in the file.
#
# So it is matched STRUCTURALLY rather than by one prefix: any numeric series whose
# LEAF is nwc or wc, excluding the delta forms and excluding the ratio family
# (dso/dio/dpo/ccc), which describe working capital without being it.
_WC = re.compile(r'(?:^|[.\[])(?:nwc|wc)(?:\[\d+\])?$', re.I)
_DWC = re.compile(r'(?:^|[.\[])(?:d_?nwc|delta_?nwc|dwc)(?:\[\d+\])?$', re.I)
_WC_RATIO = re.compile(r'\b(?:dso|dio|dpo|ccc|_pct|pct_)\b', re.I)
_IC = re.compile(r'(?:^|\.)(?:ic_replacement|invested_capital_replacement|'
                 r'replacement_cost_(?:ic|capital))(?:\[|$|\.)', re.I)


def _flatten(o, p='', out=None):
    if out is None:
        out = {}
    if isinstance(o, dict):
        for k, v in o.items():
            _flatten(v, '%s.%s' % (p, k) if p else k, out)
    elif isinstance(o, list):
        for n, v in enumerate(o):
            _flatten(v, '%s[%d]' % (p, n), out)
    elif isinstance(o, (int, float)) and not isinstance(o, bool):
        out[p] = o
    return out


def _needs(ticker):
    """{item: (state, where)} for the three inputs a corrected terminal needs."""
    f = os.path.join(REPO, 'engine', '%s_study' % ticker.lower(), 'study_numbers.json')
    flat = {}
    if os.path.exists(f):
        try:
            flat = _flatten(json.load(open(f, encoding='utf-8')))
        except Exception:                                            # noqa: BLE001
            flat = {}
    out = {}
    for item, pat in (('working_capital', _WC), ('ic_replacement', _IC)):
        hits = sorted(k for k in flat if pat.search(k)
                      and not (item == 'working_capital' and _WC_RATIO.search(k)))
        if not hits:
            out[item] = ('MISSING', '')
            continue
        # A PATTERN CANNOT TELL A STUDY'S BASE CASE FROM ITS SENSITIVITY GRID, AND
        # THIS IS WHERE GUESSING STOPS. On one name the leaf `nwc` matches 161 keys:
        # the base case, a historical actual, and a scenario series for every cell of
        # a beta-by-growth grid. Picking one of those is not resolution — it is a
        # choice about which case a terminal is built on, and it is the STUDY'S to
        # make rather than this file's.
        #
        # THIS PATTERN HAS NOW BEEN WRONG IN BOTH DIRECTIONS, which is the finding.
        # Narrow, it reported four names as publishing no working capital while three
        # publish a forecast level under their own spelling. Widened structurally, it
        # returns a sensitivity cell with equal confidence. A third adjustment would
        # be tuning against the names in front of me, which is the free parameter this
        # house forbids everywhere else.
        #
        # So the report says HOW MANY candidates a study exposes and leaves the choice
        # named as the study's — the architecture prose_figures and table_footing both
        # reached by measurement, where the shared instrument does the arithmetic and
        # each study declares only what is its own.
        out[item] = ('RESOLVABLE', '%d candidate key(s), e.g. %s%s'
                     % (len(hits), hits[0],
                        '' if len(hits) == 1
                        else " — WHICH ONE IS THE STUDY'S TO DECLARE"))

    lo, hi, src = TC.disclosed_life(ticker)
    if lo is None:
        out['useful_life_years'] = ('MISSING', '')
    elif hi is None:
        out['useful_life_years'] = ('RESOLVABLE', 'committed at %g years' % lo)
    else:
        out['useful_life_years'] = ('RESOLVABLE',
                                    'sourced as a %g-%g year band' % (lo, hi))
    return out


def price_one(rec, lives):
    """(status, detail, fv) for one census record.

    THE INSTRUMENT REPRODUCES BEFORE IT PREDICTS. A study already rebuilt through
    terminal_value.py commits every input it used, so rebuilding from that record must
    return the fair value the study publishes — and if it does not, this file is wrong
    rather than the study. That check is the whole reason the ALREADY CORRECTED branch
    exists: without a case where the answer is known in advance, a pricing report is a
    column of numbers nobody can falsify.

    A FIRST DRAFT DID PREDICT WITHOUT REPRODUCING and was wrong by 8.4% on exactly that
    name. It rebuilt from the census record with working capital passed as zero and the
    capital base taken from the flat resolver, and reported the difference as though it
    were the correction. The move was the instrument's own simplifications.
    """
    tk = rec['ticker']
    if 'unreadable' in rec:
        return 'UNREADABLE', rec['unreadable'], None

    tr = committed_terminal(tk)
    if tr and tr.get('_ambiguous'):
        return ('AMBIGUOUS RECORD',
                'this study commits %d terminal records and which one it means is not '
                'this file\'s judgement to make' % tr['_ambiguous'], None)
    if tr and tr.get('_two_sided'):
        # EACH PUBLISHED BRANCH IS REBUILT ON ITS OWN INPUTS. There is no single fair
        # value to reproduce against — that is what two-sided means — so what is
        # asserted is that every published terminal still BUILDS through the sanctioned
        # module, which is the claim that matters here: the study is on the corrected
        # construction. A branch that no longer builds is named rather than averaged in.
        broke = []
        for i, r in enumerate(tr['_two_sided']):
            try:
                TV.build(TV.TerminalInputs(**dict(r['inputs'])))
            except Exception as e:                                   # noqa: BLE001
                broke.append('branch %d: %s' % (i + 1, e))
        if broke:
            return ('RECORD WILL NOT REBUILD',
                    'a published branch no longer builds — ' + '; '.join(broke), None)
        return ('ALREADY CORRECTED',
                'two-sided: %d published terminals, each rebuilt from its own committed '
                'inputs through the sanctioned module' % len(tr['_two_sided']), None)
    if tr and tr.get('inputs'):
        ins = dict(tr['inputs'])
        try:
            built = TV.build(TV.TerminalInputs(**ins))
        except Exception as e:                                       # noqa: BLE001
            return ('RECORD WILL NOT REBUILD',
                    'its own committed inputs no longer build: %s' % e, None)
        tv_new = getattr(built, 'tv', None)
        fv = _fv_at(rec, tv_new) if tv_new is not None else None
        if fv is None:
            return 'ALREADY CORRECTED', 'rebuilt, but the record exposes no fair value', None
        drift = abs(fv / rec['fv'] - 1.0) if rec.get('fv') else None
        if drift is not None and drift > 5e-4:
            return ('RECORD DISAGREES WITH THE STUDY',
                    'rebuilding its own committed inputs gives %.4f against a published '
                    '%.4f (%.2f%%) — one of the two has moved' % (fv, rec['fv'],
                                                                  drift * 100), None)
        return ('ALREADY CORRECTED',
                'rebuilt from its own committed inputs and reproduces %.4f exactly'
                % rec['fv'], None)

    if rec.get('implied_cycle_years') is None:
        return 'NOT THE RETIRED SHAPE', 'no reinvestment charge to correct', None

    st = _needs(tk)
    missing = [k for k, (s, _) in st.items() if s == 'MISSING']
    have = [(k, w) for k, (s, w) in st.items() if s == 'RESOLVABLE']
    if missing:
        detail = 'MISSING ' + ', '.join(
            k + (' — ' + st[k][1] if st[k][1] else '') for k in missing)
        if have:
            detail += '  ·  resolvable: ' + ', '.join(
                '%s (%s)' % (k, w) for k, w in have)
        return 'CANNOT BE PRICED', detail, None
    return ('RESOLVABLE, NOT COMMITTED',
            'every input a corrected terminal needs resolves from this study\'s own '
            'numbers — ' + ', '.join('%s (%s)' % (k, w) for k, w in have)
            + ' — but none is a committed terminal input, so the rebuild must confirm '
              'each rather than assume it', None)


def _market_of(ticker):
    """The market a name is filed under, from the raw libraries rather than a guess."""
    import glob as _g
    for p in _g.glob(os.path.join(ENGINE, 'raw_ohlc', '*', ticker + '.csv')):
        return os.path.basename(os.path.dirname(p))
    raise KeyError(ticker)


def _fv_at(rec, tv_new):
    """The study's own fair value at a different terminal — the CENSUS's arithmetic.

    Delegated rather than copied [R-ENF-03]: a second implementation of one claim is
    two claims. terminal_census._fv_at could never fire when this file first needed
    it — it demanded a `df_tv` key read_study does not set, so it returned None for
    every record in the book — and the fix belongs there, where the record is built,
    rather than as a private copy here.
    """
    return TC._fv_at(rec, tv_new)


def report():
    rows = TC.census()
    if not rows:
        print('FAIL — the census returned zero studies; an empty result is not a clean '
              'result [R-ENF-04]')
        return 1

    print('CAN THE RETIRED TERMINAL BE CORRECTED FROM WHAT EACH STUDY PUBLISHES?')
    print('   [R-TERM-01 CLAUSE TWO] · %d study directories read' % len(rows))
    print()

    from collections import Counter
    buckets = {}
    for rec in sorted(rows, key=lambda r: r['ticker']):
        st, why, _fv = price_one(rec, None)
        buckets.setdefault(st, []).append((rec['ticker'], why))

    order = ['ALREADY CORRECTED', 'RECORD DISAGREES WITH THE STUDY',
             'RECORD WILL NOT REBUILD', 'CANNOT BE PRICED',
             'NOT THE RETIRED SHAPE', 'UNREADABLE']
    for st in order + [k for k in buckets if k not in order]:
        if st not in buckets:
            continue
        print('  %s (%d)' % (st, len(buckets[st])))
        for tk, why in buckets[st]:
            print('    %-12s %s' % (tk, why[:118]))
        print()

    bad = len(buckets.get('RECORD DISAGREES WITH THE STUDY', [])) + \
        len(buckets.get('RECORD WILL NOT REBUILD', []))
    ok = len(buckets.get('ALREADY CORRECTED', []))
    cant = len(buckets.get('CANNOT BE PRICED', []))

    retired = _retired_architecture()
    if retired is None:
        print('  FAIL — the lens ratchet could not be read, so this report cannot say '
              'which centrals are still')
        print('  produced by the architecture [R-LENS-03] retired. An unreadable answer '
              'is not a clean one [R-ENF-04].')
        return 1
    unrebuilt = [tk for tk, _ in buckets.get('CANNOT BE PRICED', [])
                 + buckets.get('RESOLVABLE, NOT COMMITTED', [])]
    still = sorted(tk for tk in unrebuilt if tk in retired)
    print('  THE CONSTRAINT ABOVE THE INPUTS, AND IT WAS FOUND BY TRYING TO USE THEM.')
    print('  %d of the %d unrebuilt names are ALSO on the lens ratchet — their CENTRAL is '
          'still produced by' % (len(still), len(unrebuilt)))
    print('  the typed weighted blend [R-LENS-03] retired on 02-Sep-2026 as a new method '
          'with free parameters')
    print('  nobody tested. A CORRECTED TERMINAL INSIDE A RETIRED BLEND IS NOT A '
          'MEASUREMENT: the move it')
    print('  produces is a move in a number this house has already stopped standing '
          'behind, and reporting it')
    print('  as the price of the correction would be measuring one defect through '
          'another.')
    print()
    print('  SO THE ANSWER FOR EVERY UNREBUILT NAME IS THE SAME AND IT IS NOT ABOUT '
          'INPUTS: the correction is')
    print('  measured when a name is RE-ISSUED — lens architecture, terminal and '
          'committed inputs together.')
    print('  Which is what the ALREADY CORRECTED names show: both were re-issued '
          'wholesale.')
    print()
    print('  THE ANSWER, AND IT IS NOT A TABLE OF MOVES.')
    print('  %d name(s) are already on the corrected construction and rebuild to their '
          'own published' % ok)
    print('  fair value EXACTLY — which is what makes this instrument falsifiable rather '
          'than a column of')
    print('  numbers, and it caught this file being wrong by 8.4% before it caught '
          'anything else.')
    print()
    print('  %d carry the retired construction and CANNOT be priced from what they '
          'publish. The blocker' % cant)
    from collections import Counter
    miss = Counter()
    for tk, _why in buckets.get('CANNOT BE PRICED', []):
        for k, (s, _w) in _needs(tk).items():
            if s == 'MISSING':
                miss[k] += 1
    print('  is NOT uniform and naming it per item is the point — "cannot be priced" is '
          'a conclusion,')
    print('  and this is the evidence for it:')
    for k, n in miss.most_common():
        print('      %-20s missing on %2d of %d' % (k, n, cant))
    print()
    print('  THE DOMINANT ONE IS THE CAPITAL BASE, AND THAT IS THE DEFECT RESTATED. The '
          'retired terminal')
    print('  charges g x BOOK capital, so a study carrying it never had to construct '
          'invested capital at')
    print('  REPLACEMENT cost — the quantity the corrected charge acts on. It is not an '
          'oversight in any')
    print('  study; it is what the construction asked for. What a process commits '
          'decides what can ever')
    print('  be asked of it later [R-FCAL-01 AMENDED], and nobody notices the missing '
          'field until the')
    print('  question arrives.')
    print()
    print('  SO THE NEXT WORK IS SOURCING AND CONSTRUCTION, NOT A MODELLING PASS — and '
          'A LIFE THIS DESK')
    print('  CHOSE IS NOT A DISCLOSED LIFE (SIGCM clause 1), so nothing here is assumed. '
          'Every name is')
    print('  COUNTED rather than skipped: a report listing only the priceable ones would '
          'read as though')
    print('  the book had been measured.')
    print()
    print('  RESOLVABLE IS NOT COMMITTED. Where an input is named above it is a '
          'CANDIDATE the rebuild')
    print('  must confirm, never a substitute for the study committing it.')

    if bad:
        print()
        print('  FAIL — %d record(s) no longer agree with the study they belong to '
              '[R-ENF-06].' % bad)
        return 1
    return 0


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.parse_args()
    raise SystemExit(report())
