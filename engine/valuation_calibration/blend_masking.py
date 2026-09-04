#!/usr/bin/env python3
"""HOW FAR IS EACH STUDY'S PUBLISHED CENTRAL FROM THE LENS IT CALLS PRIMARY? [L-291]

    python3 engine/valuation_calibration/blend_masking.py

WHY THIS EXISTS. [R-LENS-03] retired the typed blend on 02-Sep-2026 on the evidence of
one name, where the blend landed 28% BELOW a market the cash-flow lens agreed with to
within 2.2%: it MANUFACTURED a disagreement. Reading the gap list on 04-Sep-2026 turned
up the opposite case — a study whose primary lens sits well ABOVE the price while its
blend reports a fraction of that, and another whose blend FLIPS THE SIGN outright.

So a blend does not bias an answer, it MASKS one, and it masks in whichever direction
happens to be convenient. That is why a house running them reads as inconsistent rather
than as wrong in a fixed direction — which is exactly what the pooled valuation
calibration measured and could not explain: a mean about a tenth below the price with a
median sitting ON it is the signature of masking, not of a bias.

WHAT IT MEASURES, AND WHAT IT DOES NOT. It reports, per study, the lens the study ITSELF
calls primary, the central it publishes, and both against the spot the study was struck
at. It does NOT say which is right: a primary lens far from the price may be the thing
that is wrong, and this file takes no view. What it says is how much of the study's own
disagreement with the market the published number is not showing.

THE POPULATION IS ANCHORED ON THE STUDY DIRECTORIES [R-ENF-04] and a run that finds no
blends at all FAILS rather than reporting clean — an empty answer here would mean the
resolver broke, not that the book is conformed, and the two must never read alike.

READ IT LIVE. Every figure here moves when a study is re-issued, so it is never quoted
from a document — the same discipline the calibration figures obey.
"""
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
ENGINE = os.path.join(REPO, 'engine')

# The keys a lens dict uses for its central read. A study spells this its own way and the
# set is small and closed; an unrecognised spelling makes the study UNREADABLE here rather
# than silently absent, because those are different claims.
BASE_KEYS = ('base', 'value', 'central', 'mid')
WEIGHT_KEYS = ('w', 'weight')


def _base(v):
    for k in BASE_KEYS:
        if isinstance(v.get(k), (int, float)):
            return float(v[k])
    return None


def _weight(v):
    for k in WEIGHT_KEYS:
        if v.get(k) is not None:
            return v[k]
    return None


def read(ticker):
    """(primary, central, spot, weights) for one study, or a reason it cannot be read."""
    f = os.path.join(ENGINE, '%s_study' % ticker.lower(), 'study_numbers.json')
    if not os.path.exists(f):
        return None, 'no committed numbers file'
    try:
        n = json.load(open(f, encoding='utf-8'))
    except Exception as e:                                           # noqa: BLE001
        return None, 'numbers file will not parse: %s' % e
    L = n.get('lenses')
    if not isinstance(L, dict):
        return None, 'exposes no lens panel'

    # THE FIRST DRAFT ASKED WHETHER THE WEIGHT KEYS SURVIVE and that is the wrong
    # question, which one name made obvious: a study that has been conformed keeps its
    # four weights as the record of what was retired — beside an explicit
    # `retired_blend` entry carrying the number it used to publish — while its central
    # is its primary and nothing is masked. Reading the keys reported it as a blend.
    #
    # WHAT MATTERS IS WHETHER THE PUBLISHED CENTRAL IS THE PRIMARY, and that is
    # independent of whether any weights are still written down. Re-pointed at that,
    # per [R-COC-01]: when a check fires on work that is right, re-point it rather than
    # widen it. The weights are still read and reported, because a study carrying live
    # weights AND a masked central is a different case from one carrying neither.
    ws = {k: _weight(v) for k, v in L.items()
          if isinstance(v, dict) and _weight(v) is not None and k != 'central'}

    # THE BOOK SPELLS ITS LENS PANEL THREE WAYS and the resolver reads all three rather
    # than reporting two-thirds of the book as unreadable. A panel this file does not
    # recognise still REFUSES — an unrecognised shape and a conformed study must never
    # read alike [R-ENF-04] — which is why each shape is named here instead of a
    # best-effort scan.
    #
    #   (a) one dict per lens, each carrying base/value, the primary named in its `name`
    #   (b) a `values` sub-dict keyed by lens NAME with a sibling `primary` key naming
    #       which of them it is — the shape the two conformed studies use
    #   (c) a two-sided study, handled below: no single central by construction
    prim = prim_k = None
    if isinstance(L.get('values'), dict) and isinstance(L.get('primary'), str):
        prim_k = L['primary']
        pv = L['values'].get(prim_k)
        prim = float(pv) if isinstance(pv, (int, float)) else _base(pv) if isinstance(pv, dict) else None
    if prim is None:
        for k, v in L.items():
            if not isinstance(v, dict):
                continue
            if 'primary' in str(v.get('name') or '').lower():
                prim, prim_k = _base(v), k
                break
    if prim is None and isinstance(L.get('dcf'), dict):
        prim, prim_k = _base(L['dcf']), 'dcf'
    if prim is None:
        if (n.get('central_two_sided') or {}).get('branches'):
            return None, 'TWO-SIDED — no single central, which is the conformed shape'
        return None, 'lens panel is in a shape this file does not read'

    cen = n.get('central')
    if not isinstance(cen, (int, float)):
        cv = L.get('central')
        # a panel spells its central either as a nested dict or as a bare number, and
        # reading only the first shape reported a CONFORMED study as unreadable
        cen = cv if isinstance(cv, (int, float)) else _base(cv) if isinstance(cv, dict) else None
    if not isinstance(cen, (int, float)):
        # A TWO-SIDED ANSWER HAS NO SINGLE CENTRAL BY CONSTRUCTION and that is the
        # architecture this rule asked for, not a study that failed to publish one.
        # The two must never read alike.
        if (n.get('central_two_sided') or {}).get('branches'):
            return None, 'TWO-SIDED — no single central, which is the conformed shape'
        return None, 'exposes no published central'

    spot = n.get('spot')
    if not isinstance(spot, (int, float)) or not spot:
        return None, 'exposes no spot'
    return (prim, cen, float(spot), ws, prim_k), None


def main():
    dirs = sorted(glob.glob(os.path.join(ENGINE, '*_study')))
    if not dirs:
        print('FAIL — no engine/*_study directories. An empty population is not a clean '
              'one [R-ENF-04].')
        return 1

    rows, unreadable, not_blends = [], [], []
    for d in dirs:
        tk = os.path.basename(d)[:-6].upper()
        got, why = read(tk)
        if got is None:
            (not_blends if why.startswith('TWO-SIDED') else unreadable).append((tk, why))
            continue
        prim, cen, spot, ws, prim_k = got
        rows.append((tk, prim, cen, spot, prim / spot - 1.0, cen / spot - 1.0,
                     prim / cen - 1.0 if cen else 0.0, prim_k, ws))

    print('BLEND MASKING — the published central against the lens the study calls primary')
    print('   [L-291] · %d study directories · %d publish a typed blend · %d do not · '
          '%d unreadable' % (len(dirs), len(rows), len(not_blends), len(unreadable)))
    if not rows:
        print('\nFAIL — not one study resolved to a blend. That is not a conformed book, it '
              'is a broken resolver: the studies that retired the blend keep their lens '
              'keys and set the weights to None, so a zero here means this file stopped '
              'reading them [R-ENF-04].')
        return 1

    print('\n  %-13s%9s%9s%8s%10s%10s%10s' %
          ('ticker', 'primary', 'central', 'spot', 'prim/px', 'cent/px', 'masked'))
    print('  ' + '-' * 69)
    flips, degenerate = [], []
    for tk, p, c, s, gp, gc, m, pk, ws in sorted(rows, key=lambda r: -abs(r[6])):
        flag = ''
        # A PRIMARY AT ITS OWN FLOOR IS NOT A MASKED ANSWER, IT IS A MODEL SAYING NOTHING.
        # One study's cash-flow lens floors at 0.01 against a spot of 2.19, so the ratio
        # against it is arithmetic on a floor and ranking the book by it would put that
        # name on top of a list it does not belong at the top of.
        if abs(p) < 0.05 * s:
            flag = '  <- PRIMARY AT ITS FLOOR, the ratio is not a masking figure'
            degenerate.append(tk)
        elif (gp > 0) != (gc > 0):
            flag = '  <- SIGN FLIP'
            flips.append(tk)
        print('  {:<13}{:9.2f}{:9.2f}{:8.2f}{:+10.1%}{:+10.1%}{:+10.1%}{}'
              .format(tk, p, c, s, gp, gc, m, flag))

    print('\n  MASKED is how far the blend moves the answer from the study\'s own primary '
          'lens.\n  It is NOT a claim that the primary is right: a primary far from the '
          'price may be\n  the thing that is wrong, and this file takes no view. It is how '
          'much of the\n  study\'s own disagreement the published number is not showing.')
    if flips:
        print('\n  SIGN FLIP on %d name(s): %s — the primary lens and the published central '
              'sit on\n  OPPOSITE sides of the price, so the gap gate audits one direction '
              'while the study\'s\n  own primary lens asserts the other, and the '
              'publication block reads the wrong side.'
              % (len(flips), ', '.join(flips)))
    conformed = [t for t, _p, _c, _s, _gp, _gc, m, _pk, _w in rows if abs(m) < 1e-9]
    if conformed:
        print('\n  CONFORMED (%d): %s — the published central IS the primary lens, so '
              'nothing is\n  masked. These are the controls, and a run where none of them '
              'reads 0.0%% would mean\n  this file had stopped resolving rather than that '
              'the book had drifted.'
              % (len(conformed), ', '.join(conformed)))
    if degenerate:
        print('\n  DEGENERATE PRIMARY (%d): %s' % (len(degenerate), ', '.join(degenerate)))
    if not_blends:
        print('\n  TWO-SIDED, NO SINGLE CENTRAL (%d): %s'
              % (len(not_blends), ', '.join(t for t, _ in not_blends)))
    if unreadable:
        print('\n  UNREADABLE (%d), each with its reason — an absent answer is not a clean '
              'one:' % len(unreadable))
        for tk, why in unreadable:
            print('    %-13s %s' % (tk, why))
    return 0


if __name__ == '__main__':
    sys.exit(main())
