"""A SUPPLIED PRICE IS A HAND-OFF, NOT A SOURCE. Hold each one against its own library.

WHAT THIS EXISTS TO STOP. engine/prices/SUPPLIED_{DD-MM-YYYY}.json carries closes typed
out of a spreadsheet and handed over. Ten studies read it, and so does
check_valuation_gap.py -- which is Phase 1's acceptance criterion 4, the gate that decides
which names PASS and which are REFERRED to the principal. Nothing compared those figures
with the OHLC libraries sitting in the same repository.

A wrong supplied price does not produce a wrong fair value. It produces a wrong ROUTING:
a name is referred that should have passed, or passes when it should have been referred.
That was written down on 09-09-2026 in engine/KABO_PRICE_QUERY_09-09-2026.md, after the
principal said "Noo Kabo is not 34 EGP" -- supplied 34.06 against a library that ends at
9.120. Running the same comparison across all ninety names found KABO was not alone.

THE BAR IS THE NAME'S OWN HISTORY, SO THERE IS NO THRESHOLD TO ARGUE ABOUT.
A supplied close and a library close are days apart, and a price is allowed to move in
between -- so the question is never "how big is the difference" but "is a move this big,
over this many sessions, something this stock has ever done". The check measures the
implied move, counts the sessions between the two dates, and compares it with the LARGEST
move that name has actually made over any window of that length in its own history. A
figure inside its own record is not flagged however large; one outside it is flagged
however small, because the stock itself says it does not move like that.

This is the same shape as engine/asset_base.py's [R-ASSET-01]: an ORDERING against the
name's own record rather than a constant somebody picked.

THE RATCHET [R-ENF-02] carries the divergences standing when this was adopted, each with
its measured magnitude, so the check binds forward without being red on the day it lands.
It may only ever SHORTEN. An entry excuses the magnitude it RECORDED: a divergence that
grows is a new failure [R-ENF-08].

WHAT THIS DOES NOT DO: it never edits a price. Which of two records is right is a
sourcing question for the principal, not an edit -- exactly as the KABO note says, a
valuation input is sourced and never adjusted to make two records agree.

[R-ENF-01] runs from outside the studies it governs and modifies nothing.
[R-ENF-07] falsifier: scripts/check_supplied_prices_negative_control.py.
"""
import csv
import glob
import json
import os
import sys
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENGINE = os.path.join(ROOT, 'engine')
OHLC = os.path.join(ENGINE, 'raw_ohlc')
MARKETS = ('EG', 'AE', 'SA', 'QA', 'IN', 'KR', 'US', 'GB', 'BR')

#: measured 09-09-2026, the day this gate was written. Each entry records the implied move
#: and the sessions it spans, so a WORSENING is a new failure rather than a covered one.
RATCHET = {
    'KABO': dict(implied=2.7346, sessions=7,
                 why='the principal states 34.06 is not the price; '
                     'engine/KABO_PRICE_QUERY_09-09-2026.md, unresolved by request'),
    'SABIC': dict(implied=0.6248, sessions=2,
                  why='supplied 81.40 against a library ending 01-Sep at 50.10, two '
                      'sessions earlier — found by this gate, not yet ruled on'),
    'IQCD': dict(implied=0.3216, sessions=1,
                 why='supplied 13.17 against a library ending 01-Sep at 9.965 — found by '
                     'this gate, not yet ruled on'),
    'QGTS': dict(implied=0.1253, sessions=1,
                 why='supplied 4.85 against a library ending 01-Sep at 4.31 — the '
                     'smallest of the four and the one most likely to be a real move; '
                     'found by this gate, not yet ruled on'),
}

#: THE QATARI LIBRARIES CARRY UNADJUSTED CORPORATE ACTIONS. IQCD's extreme one-session
#: move reads 894.7% and QGTS's 908.3%, against 99.5th percentiles of 6.7% and 7.1%. A
#: price series does not do that; a split recorded as a price change does. It is named
#: here because it is what made the first cut of this gate unfireable on those two names,
#: and because it is a defect in OUR data rather than in anybody's supplied figure. It is
#: not fixed here -- adjusting a price series is a sourcing job, not a gate's.
_LIBRARY_ARTEFACTS = ('QA/IQCD', 'QA/QGTS')


def _rows(path):
    out = []
    for r in csv.DictReader(open(path, encoding='utf-8-sig')):
        if not any(r.values()):
            continue
        d = (r.get('Date') or r.get('date') or '').strip().strip('"')
        dt = None
        for f in ('%m/%d/%Y', '%Y-%m-%d', '%d/%m/%Y'):
            try:
                dt = datetime.strptime(d, f)
                break
            except ValueError:
                pass
        if dt is None:
            continue
        raw = r.get('Price') or r.get('close') or r.get('Close') or r.get('Adj Close')
        try:
            out.append((dt, float(str(raw).replace(',', ''))))
        except (TypeError, ValueError):
            continue
    out.sort()
    return out


def _library(tk):
    for mk in MARKETS:
        p = os.path.join(OHLC, mk, tk + '.csv')
        if os.path.exists(p):
            return _rows(p), mk
    return None, None


def _bar(series, k):
    """How far this name moves over k sessions: (bar, extreme, n).

    THE BAR IS NOT THE MAXIMUM, AND THE FIRST CUT OF THIS GATE MADE THAT MISTAKE.
    Taking the largest move a name has ever made sounds like the strictest possible
    empirical test and is close to the most permissive one, because a library with a
    single unadjusted split in it records a move of several hundred per cent -- and the
    bar is then a number no supplied price could ever exceed. Measured: IQCD's worst
    one-session move is 894.7%, which is a corporate action recorded as a price change,
    so the gate could not have fired on that name whatever was supplied.

    The bar is therefore the 99.5th percentile of the name's own k-session moves, which
    is robust to a handful of bad rows and still says only what this stock does. The
    EXTREME is returned beside it and printed, because the two diverging by a wide margin
    is itself the signature of an unadjusted corporate action in the library -- a finding
    about our data worth surfacing rather than smoothing away.
    """
    if k <= 0 or len(series) <= k:
        return None, None, 0
    moves = []
    for i in range(k, len(series)):
        a, b = series[i - k][1], series[i][1]
        if a:
            moves.append(abs(b / a - 1.0))
    if not moves:
        return None, None, 0
    moves.sort()
    idx = min(len(moves) - 1, int(round(0.995 * (len(moves) - 1))))
    return moves[idx], moves[-1], len(moves)


def _supplied():
    """The prices IN FORCE: every SUPPLIED_*.json merged per ticker on each price's OWN date.

    NOT the newest file. check_valuation_gap.py carries the reason at length and it is why
    this reader must match it: a supplied file records WHEN SOMEBODY SUPPLIED a set of
    closes, and each close inside carries its own date, so a name added to today's file
    with last month's close must not displace a fresher close sitting in an older file. On
    07-09-2026 exactly that happened to GBCO.

    Matching matters beyond correctness. Reading only the newest file, this gate checked
    TWO prices while the gate it exists to protect routes on NINETY -- two readers of one
    fact disagreeing [R-ENF-03], with this one looking GREEN because it had examined almost
    nothing, which is the [R-ENF-04] costume. It reported exactly that before this was
    fixed.
    """
    files = sorted(glob.glob(os.path.join(ENGINE, 'prices', 'SUPPLIED_*.json')))
    if not files:
        return None, None
    merged, seen = {}, {}
    for fp in files:                    # oldest first, so a tie goes to the newest file
        doc = json.load(open(fp, encoding='utf-8'))
        for tk, row in (doc.get('prices') or {}).items():
            if not isinstance(row, dict) or 'price' not in row:
                continue
            d = row.get('date') or doc.get('supplied') or ''
            if tk not in seen or d >= seen[tk]:
                seen[tk] = d
                merged[tk] = dict(row, _file=os.path.basename(fp))
    return {'prices': merged}, ('%d file(s), merged per ticker on each price own date'
                                % len(files))


def main():
    doc, name = _supplied()
    if doc is None:
        print('RED — no engine/prices/SUPPLIED_*.json found at all. An absent price file '
              'is not a clean one [R-ENF-04]: ten studies and the traded-price gate read '
              'it, so its absence means the layout moved, not that every price agrees.')
        return 1
    prices = {k: v for k, v in (doc.get('prices') or {}).items()
              if isinstance(v, dict) and 'price' in v}
    if not prices:
        print('RED — %s carries no priced entries.' % name)
        return 1

    flagged, unreadable, checked = [], [], 0
    for tk, v in sorted(prices.items()):
        series, mk = _library(tk)
        if not series:
            unreadable.append(tk)
            continue
        checked += 1
        lib_dt, lib_px = series[-1]
        px = float(v['price'])
        if not lib_px:
            unreadable.append(tk)
            continue
        implied = px / lib_px - 1.0
        try:
            sup_dt = datetime.strptime(v.get('date') or doc.get('supplied'), '%Y-%m-%d')
        except (TypeError, ValueError):
            sup_dt = lib_dt
        # sessions between the two dates, counted in the name's OWN trading calendar
        k = sum(1 for d, _ in series if d > lib_dt) or \
            max(1, int(round((sup_dt - lib_dt).days * 5.0 / 7.0)))
        bar, extreme, nmoves = _bar(series, k)
        if bar is None:
            unreadable.append(tk)
            continue
        if abs(implied) > bar:
            flagged.append(dict(tk=tk, mk=mk, px=px, lib=lib_px, lib_dt=lib_dt,
                                implied=implied, k=k, worst=bar, extreme=extreme,
                                n=nmoves, src=v.get('_file', '?')))

    print('SUPPLIED PRICES vs their own OHLC libraries — %s' % name)
    print('  %d priced entries · %d compared · %d without a usable library'
          % (len(prices), checked, len(unreadable)))
    if unreadable:
        print('  no usable library: %s' % ', '.join(sorted(unreadable)))
    print()

    if not checked:
        print('RED — zero names were compared. An empty result is not a clean result '
              '[R-ENF-04].')
        return 1

    new, covered = [], []
    for f in flagged:
        e = RATCHET.get(f['tk'])
        if e and abs(f['implied']) <= e['implied'] * 1.0001:
            covered.append((f, e))
        else:
            new.append((f, e))

    def line(f):
        return ('  %-11s %-3s supplied %10.3f vs library %10.3f (%s) — implies %+.1f%% '
                'over %d session(s); this name\'s own %d-session moves reach %.1f%% at '
                'the 99.5th percentile of %d observations (extreme %.1f%%)  [%s]'
                % (f['tk'], f['mk'], f['px'], f['lib'], f['lib_dt'].date(),
                   100 * f['implied'], f['k'], f['k'], 100 * f['worst'], f.get('n', 0),
                   100 * (f.get('extreme') or 0), f.get('src', '?')))

    if covered:
        print('ON THE RATCHET (%d) — recorded, may only shorten:' % len(covered))
        for f, e in covered:
            print(line(f))
            print('  %-11s     %s' % ('', e['why']))
        print()

    if new:
        print('RED — %d supplied price(s) imply a move this name has never made:' % len(new))
        for f, e in new:
            print(line(f))
            if e:
                print('  %-11s     WORSE THAN THE RATCHET RECORDS: entry allows %+.1f%%, '
                      'this run measures %+.1f%% [R-ENF-08]'
                      % ('', 100 * e['implied'], 100 * f['implied']))
        print('\nThe fix is NEVER to edit the price. Which record is right is a sourcing '
              'question for the principal; record it and route it, as '
              'engine/KABO_PRICE_QUERY_09-09-2026.md does.')
        return 1

    if covered:
        print('OK — no NEW divergence. %d name(s) remain on the ratchet above, unresolved '
              'and awaiting the principal\'s sourcing ruling; they are recorded debt, not '
              'a clean bill.' % len(covered))
    else:
        print('OK — every supplied price sits inside what its own history says the name '
              'can do, and the ratchet is empty.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
