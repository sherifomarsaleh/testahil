"""tech_record.py — the per-name calibration record for the TECHNICAL lens.

The analogue of band_record.py, for the other lens. band_record answers "how
often did the published 90% band actually hold"; this answers "which statements
in this name's technical read has its own history earned".

WHAT IT MAY AND MAY NOT SAY, AND WHY — all three settled by measurement, not
taste (evidence: engine/lab/ta_calibration/, 92 names, 89,190 claims, 2011-2026):

  TAPE (the ATR word)      PER NAME. Spearman(ATR% at origin, realized forward
                           vol) is significantly positive for 70 of 78 testable
                           names at one month and 61 of 78 at three, median rho
                           +0.39/+0.35. This is the best-calibrated statement
                           the technical read makes.
  TREND (the MA stack)     PER NAME ONLY WHERE EARNED. The above-stack vs
                           below-stack gap in forward up-rate is significant for
                           7 of 71 names at one month and 15 at three. No name
                           is significantly REVERSED at either horizon. Where a
                           name has not earned its own figure the market's is
                           the honest one.
  LEVELS (S/R)             NEVER PER NAME, AND NOT PENDING MORE DATA. Published
                           levels do hold ~3-4pp more often than a distance-
                           matched non-level (robust in 15 of 16 pooled cells),
                           but resolving a 3-4pp effect needs about 560 paired
                           observations. Fifteen years yields a median of 62 per
                           name and the best-endowed name in the book has 239 —
                           short by an order of magnitude, and denser origins do
                           not help because the windows overlap. A per-name
                           level record would be a number that cannot separate
                           an honest read from a broken one.
  MOMENTUM (RSI)           NO RECORD. The information is real and sits in the
                           tails, but the words carried it backwards until
                           31-Aug-2026 and the fix was to the wording, not to a
                           figure worth publishing.

STRENGTH LADDER, DELIBERATELY THE SAME SHAPE AS band_record's long/short/
market-only: say it per name where the name's own history supports it, fall back
to the market where it does not, and never print a figure that cannot separate
an honest read from a broken one. The two ladders were derived independently and
landed in the same place.

GENERATED, NEVER TYPED, and regenerated in the same pass as any refit, panel
rebuild or roll-forward — a stale record is the defect the 29-Jul technical-read
rule closed. Keyed on (market, ticker) because ticker strings collide across
markets: ADIB is a different bank in EG and AE and the two share a filename, a
collision that already defeated one count in this project's history.

RENDERS NOWHERE UNTIL INSTRUCTED. Same disposition as CALIB under [R-REC-01]:
built, committed, regenerated, and consulted — a fair thing to read when
investigating the technical read — but what a reader is shown is a decision that
belongs to whoever owns the page, not to the builder.
"""
from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass, asdict, field
from typing import Optional

import numpy as np
from scipy import stats

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)
_LAB = os.path.join(_HERE, 'lab', 'ta_calibration')
if _LAB not in sys.path:
    sys.path.insert(0, _LAB)

ALPHA = 0.05          # the level every "earned" test is taken at
TAPE_MIN_N = 30       # below this a rank correlation is noise with a decimal point
TREND_MIN_N = 10      # per side; a gap needs both states populated to exist at all


@dataclass
class TechRecord:
    market: str
    ticker: str
    origins: int
    first: str
    last: str
    # tape
    tape_n: int = 0
    tape_rho: Optional[float] = None
    tape_p: Optional[float] = None
    tape_earned: bool = False
    # trend
    trend_n_above: int = 0
    trend_n_below: int = 0
    trend_up_above: Optional[float] = None
    trend_up_below: Optional[float] = None
    trend_gap: Optional[float] = None
    trend_p: Optional[float] = None
    trend_earned: bool = False
    trend_reversed: bool = False
    notes: list = field(default_factory=list)

    def clause(self, horizon_label='three months'):
        """The one place this record is put into words. Nothing else may phrase it.

        A TESTED NULL IS NOT MISSING DATA, and the first draft of this method said
        it was: RAYA, with 149 readings, read "this name's own history is not
        enough to say" when the truth is that the test ran on plenty of history
        and came back negative. Those are opposite statements — one says come
        back later, the other says we looked and it does not hold here — and
        collapsing them into the softer one is the same defect as the momentum
        words and as "failed calibration test". The three cases are kept apart.
        """
        bits = []
        if self.tape_earned:
            bits.append(f"across {self.tape_n} readings, how busy the tape looked has "
                        f"tracked how much the price actually moved over the following "
                        f"{horizon_label} (rank correlation {self.tape_rho:+.2f})")
        elif self.tape_n < TAPE_MIN_N:
            bits.append(f"only {self.tape_n} readings of its own have resolved — too few "
                        f"to say whether its tape reading tracks what follows")
        else:
            bits.append(f"over {self.tape_n} readings its tape reading has NOT tracked "
                        f"what followed (rank correlation {self.tape_rho:+.2f}), so no "
                        f"claim is made for this name")
        if self.trend_earned and not self.trend_reversed:
            bits.append(f"and when it has traded above its whole moving-average stack the "
                        f"price has finished higher {self.trend_up_above*100:.0f}% of the "
                        f"time against {self.trend_up_below*100:.0f}% below it "
                        f"({self.trend_n_above} and {self.trend_n_below} readings)")
        elif self.trend_reversed:
            bits.append("and its moving-average stack has pointed the WRONG way on its own "
                        "history — recorded, not acted on")
        return '; '.join(bits) + '.'


def _tape(sub):
    v = sub.dropna(subset=['atr_pct', 'rlz_vol'])
    if len(v) < TAPE_MIN_N:
        return len(v), None, None, False
    rho, p = stats.spearmanr(v.atr_pct, v.rlz_vol)
    return len(v), float(rho), float(p), bool(p < ALPHA and rho > 0)


def _trend(sub):
    a = sub[sub.trend.str.startswith('Trading above the whole')]
    b = sub[sub.trend.str.startswith('Trading below the whole')]
    if len(a) < TREND_MIN_N or len(b) < TREND_MIN_N:
        return len(a), len(b), None, None, None, None, False, False
    ka, kb = int((a.fwd_ret > 0).sum()), int((b.fwd_ret > 0).sum())
    p1, p2 = ka / len(a), kb / len(b)
    pool = (ka + kb) / (len(a) + len(b))
    se = np.sqrt(pool * (1 - pool) * (1 / len(a) + 1 / len(b)))
    z = (p1 - p2) / se if se > 0 else 0.0
    p = float(2 * (1 - stats.norm.cdf(abs(z))))
    earned = bool(p < ALPHA)
    return (len(a), len(b), float(p1), float(p2), float(p1 - p2), p,
            earned and p1 > p2, earned and p1 < p2)


def build(months: int = 3, step: int = 21, verbose: bool = False):
    """Recompute every name's record from the libraries. Self-verifying."""
    import glob
    import pandas as pd
    import replay

    raw = os.path.join(_HERE, 'raw_ohlc')
    libs = [(m, os.path.basename(f)[:-4])
            for m in sorted(os.listdir(raw))
            for f in sorted(glob.glob(os.path.join(raw, m, '*.csv')))]
    out, skipped = {}, []
    for market, ticker in libs:
        try:
            r = replay.harvest(market, ticker, step=step)
        except Exception as e:
            skipped.append((market, ticker, f'{type(e).__name__}: {e}'))
            continue
        s = r[(r.claim == 'state') & (r.months == months)] if len(r) else r
        if not len(s):
            skipped.append((market, ticker, 'too little history to reach a first origin'))
            continue
        tn, tr, tp, te = _tape(s)
        na, nb, ua, ub, gap, gp, ge, gr = _trend(s)
        rec = TechRecord(market=market, ticker=ticker, origins=int(len(s)),
                         first=str(s.origin.min()), last=str(s.origin.max()),
                         tape_n=tn, tape_rho=tr, tape_p=tp, tape_earned=te,
                         trend_n_above=na, trend_n_below=nb, trend_up_above=ua,
                         trend_up_below=ub, trend_gap=gap, trend_p=gp,
                         trend_earned=ge, trend_reversed=gr)
        out[f'{market}/{ticker}'] = rec
        if verbose:
            print(f'  {market}/{ticker}: {rec.clause()}', flush=True)

    # COUNT AGAINST A KNOWN TOTAL — the libraries on disk, counted on
    # (market, ticker) and never on the bare ticker string.
    assert len(out) + len(skipped) == len(libs), (
        f'population mismatch: {len(out)} + {len(skipped)} != {len(libs)}')
    return out, skipped, len(libs)


if __name__ == '__main__':
    recs, skipped, total = build(verbose='-v' in sys.argv)
    payload = {k: asdict(v) for k, v in recs.items()}
    path = os.path.join(_HERE, 'tech_records.json')
    json.dump({'built_from': 'engine/raw_ohlc, replayed through technicals.compute()',
               'libraries': total, 'recorded': len(recs),
               'skipped': [{'market': m, 'ticker': t, 'why': w} for m, t, w in skipped],
               'records': payload}, open(path, 'w'), indent=1)
    tape = sum(1 for r in recs.values() if r.tape_earned)
    tr = sum(1 for r in recs.values() if r.trend_earned)
    rv = sum(1 for r in recs.values() if r.trend_reversed)
    print(f'{len(recs)} records of {total} libraries ({len(skipped)} skipped)')
    print(f'  tape earned : {tape}')
    print(f'  trend earned: {tr}   (reversed: {rv})')
    print(f'wrote {path}')
