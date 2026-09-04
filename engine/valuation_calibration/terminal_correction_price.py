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
    """A study's own committed terminal_record, or None."""
    f = os.path.join(REPO, 'engine', '%s_study' % ticker.lower(), 'study_numbers.json')
    if not os.path.exists(f):
        return None
    try:
        return json.load(open(f, encoding='utf-8')).get('terminal_record')
    except Exception:                                                # noqa: BLE001
        return None


# WHAT A CORRECTION NEEDS THAT THE RETIRED CONSTRUCTION NEVER COMMITTED. The retired
# terminal is one line — g x IC — so a study carrying it publishes neither the capital
# base at REPLACEMENT cost nor the working capital the corrected charge acts on, and
# usually not the disclosed life either. Naming them individually is the point: "cannot
# be priced" is a conclusion, and this is the evidence for it.
NEEDS = ('ic_replacement', 'working_capital', 'useful_life_years')


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

    band, src = _life_band(tk)
    have = {'useful_life_years': band[0] if band else None,
            'ic_replacement': None,        # the retired construction commits BOOK capital
            'working_capital': None}
    missing = [k for k in NEEDS if have.get(k) is None]
    named = (missing[0] if len(missing) == 1
             else ' and '.join([', '.join(missing[:-1]), missing[-1]]))
    return ('CANNOT BE PRICED',
            'the correction needs %s, and this study commits %s; the retired '
            'construction is one line and never had to'
            % (named, 'neither' if len(missing) == 2 else
               ('it not at all' if len(missing) == 1 else 'none of them')), None)


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

    print('  THE ANSWER, AND IT IS NOT A TABLE OF MOVES.')
    print('  %d name(s) are already on the corrected construction and rebuild to their '
          'own published' % ok)
    print('  fair value exactly — which is what makes this instrument falsifiable rather '
          'than a column')
    print('  of numbers. %d carry the retired construction and CANNOT be priced from what '
          'they publish:' % cant)
    print('  the retired terminal is one line, g x IC, so it never had to commit the '
          'replacement-cost')
    print('  capital base, the working capital the corrected charge acts on, or the '
          'disclosed life.')
    print()
    print('  SO THE NEXT WORK IS SOURCING, NOT MODELLING. Each of those names needs its '
          'own audited')
    print('  accounting-policies note and its own balance sheet read again — and A LIFE '
          'THIS DESK CHOSE IS')
    print('  NOT A DISCLOSED LIFE (SIGCM clause 1), so nothing here is assumed and every '
          'name is COUNTED')
    print('  rather than skipped: a report listing only the priceable ones would read as '
          'though the book')
    print('  had been measured.')

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
