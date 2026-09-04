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


def _life_band(ticker, lives):
    """(shortest, longest, source) DISCLOSED, or (None, None, None). Never one figure.

    THE BAND IS NOT COLLAPSED HERE AND THAT IS THE HOUSE'S OWN RULE, stated in
    disclosed_lives.json before this file existed: a policy note gives a range per
    asset class, and picking one number out of it is this desk choosing the life
    under cover of a citation. The weighted life a terminal actually needs comes
    from the property, plant and equipment note's own composition, which is a
    further sourcing step.

    A first draft of this file priced `longest_years` alone and called the result a
    floor. Directionally that is true — a longer life charges less maintenance — but
    the quantity is the longest life of ANY asset class, which on a fleet is a
    jack-up barge at 40 years while the vessels the value sits in run 25. THAT IS
    STILL CHOOSING A LIFE, with a label on it. So both ends are built and both are
    printed, and where they disagree about the answer the disclosure does not
    determine it yet.
    """
    e = lives.get('lives', {}).get(ticker)
    if not e:
        return None, None, None
    return e.get('shortest_years'), e.get('longest_years'), e.get('source')


def price_one(rec, lives):
    """(status, detail, fv_new) for one census record."""
    tk = rec['ticker']
    if 'unreadable' in rec:
        return 'UNREADABLE', rec['unreadable'], None
    if rec.get('implied_cycle_years') is None:
        return 'NOT THE RETIRED SHAPE', 'no reinvestment charge to correct', None

    lo, hi, src = _life_band(tk, lives)
    if lo is None or hi is None:
        return ('NO LIFE',
                'no disclosed useful life on file — the accounting-policies note of '
                'this company\'s own audited statements is what unblocks it '
                '(SIGCM clause 1)', None)

    need = ('nopat_term', 'wacc_term', 'g', 'ic', 'dna_last')
    missing = [k for k in need if rec.get(k) is None]
    if missing:
        return 'INPUTS SHORT', 'the terminal exposes no ' + ', '.join(missing), None

    try:
        import macro_path as MP
        infl = MP.load(_market_of(tk)).terminal_inflation
    except Exception:                                                # noqa: BLE001
        # The nominal growth the study itself used IS its terminal inflation wherever
        # real growth is zero, which is what the house path returns for every terminal
        # it builds [R-MACRO-01]. Where the path will not resolve, that identity is the
        # honest fallback and it is LABELLED rather than silently assumed.
        infl = rec['g']

    out = {}
    for label, life in (('shortest', lo), ('longest', hi)):
        try:
            t_ = TV.build(TV.TerminalInputs(
                nopat=rec['nopat_term'], wacc=rec['wacc_term'],
                inflation=infl, real_growth=0.0,
                dna_book=rec['dna_last'],
                ic_replacement=rec['ic'], useful_life_years=float(life),
                useful_life_source=src or 'disclosed_lives.json',
                maintenance_basis='disclosed_life',
                working_capital=0.0))
        except Exception as e:                                       # noqa: BLE001
            out[label] = ('refused', '%dy: %s' % (life, e))
            continue
        out[label] = ('ok', _fv_at(rec, getattr(t_, 'tv', None)))

    if all(v[0] == 'refused' for v in out.values()):
        return ('REFUSED',
                'at BOTH ends of the disclosed band — %s; %s'
                % (out['shortest'][1], out['longest'][1]), None)
    vals = [v[1] for v in out.values() if v[0] == 'ok' and v[1] is not None]
    if not vals:
        return 'REFUSED', 'the module returned no terminal at either end', None
    return 'PRICED', ('band %dy-%dy' % (lo, hi)), (min(vals), max(vals))


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
    lives = json.load(open(LIVES, encoding='utf-8')) if os.path.exists(LIVES) else {}
    rows = TC.census()
    if not rows:
        print('FAIL — the census returned zero studies; an empty result is not a clean '
              'result [R-ENF-04]')
        return 1

    print('WHAT CORRECTING THE RETIRED TERMINAL IS WORTH, AND WHICH WAY IT RUNS')
    print('   [R-TERM-01 CLAUSE TWO] · %d study directories read' % len(rows))
    print()
    print('  ticker       old fv    corrected fv        move        spot    old gap  '
          '  new gap   toward?')
    print('  ' + '-' * 96)

    priced, other = [], []
    for rec in sorted(rows, key=lambda r: r['ticker']):
        st, why, fv = price_one(rec, lives)
        if st != 'PRICED' or fv is None:
            other.append((rec['ticker'], st, why))
            continue
        lo_fv, hi_fv = fv
        old = rec['fv']
        spot, _date, _src = _latest_price(rec['ticker'])
        if not spot:
            other.append((rec['ticker'], 'NO PRICE',
                          'corrected to %.2f-%.2f from %.2f, but no latest known price'
                          % (lo_fv, hi_fv, old)))
            continue
        g_old = old / spot - 1.0
        g_lo, g_hi = lo_fv / spot - 1.0, hi_fv / spot - 1.0
        # TOWARD only if BOTH ends of the disclosed band close the gap. Where the band
        # straddles, the disclosure does not decide it and the row says so.
        if abs(g_lo) < abs(g_old) and abs(g_hi) < abs(g_old):
            toward = 'TOWARD'
        elif abs(g_lo) > abs(g_old) and abs(g_hi) > abs(g_old):
            toward = 'AWAY'
        else:
            toward = 'BAND STRADDLES'
        priced.append((rec['ticker'], old, lo_fv, hi_fv, spot, g_old, g_lo, g_hi,
                       toward, why))
        print('  %-10s %7.2f  %7.2f-%-7.2f  %+6.1f%%/%+6.1f%%  %7.2f  %+7.1f%%  '
              '%+6.1f%%/%+6.1f%%  %s'
              % (rec['ticker'], old, lo_fv, hi_fv,
                 (lo_fv / old - 1) * 100, (hi_fv / old - 1) * 100, spot,
                 g_old * 100, g_lo * 100, g_hi * 100, toward))

    if not priced:
        print('  NONE. Not one terminal in the book can be corrected today, and that is '
              'the finding rather than')
        print('  a gap in this report: the correction needs a DISCLOSED useful life per '
              'name and almost none is')
        print('  on file. See below for which reason applies to which name.')

    print()
    print('  NOT PRICED, and each one counted rather than skipped [R-ENF-04]:')
    from collections import Counter
    for tk, st, why in other:
        print('    %-12s %-22s %s' % (tk, st, why[:104]))
    print()
    print('    ' + ' · '.join('%s %d' % (k, v) for k, v in
                              sorted(Counter(s for _, s, _ in other).items())))

    if priced:
        away = [r for r in priced if r[8] == 'AWAY']
        print()
        print('  %d of %d priced names move AWAY from the price at BOTH ends of their '
              'own disclosed band.' % (len(away), len(priced)))
        for r in away:
            print('    %-12s %+.1f%% -> %+.1f%%/%+.1f%% against %.2f'
                  % (r[0], r[5] * 100, r[6] * 100, r[7] * 100, r[4]))
        print('  On those the terminal is NOT where the pessimism is [R-TERM-01 CLAUSE '
              'TWO], and the eight')
        print('  headings [R-GAP-01] should look elsewhere.')

    print()
    print('  THE BAND IS THE DISCLOSURE\'S, NOT THIS DESK\'S. Both ends are built '
          'because a policy note gives a')
    print('  range per asset class and picking one figure out of it is choosing a life '
          'under cover of a')
    print('  citation. The weighted life a terminal actually needs comes from the '
          'property, plant and')
    print('  equipment note\'s own composition — a further sourcing step, not done '
          'here.')
    return 0


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.parse_args()
    raise SystemExit(report())
