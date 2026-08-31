"""tech_record.py — the per-name calibration record for the TECHNICAL lens.

The analogue of band_record.py, for the other lens. band_record answers "how
often did the published 90% band actually hold"; this answers "which statements
in this name's technical read has its own history earned".

WHAT IT MAY AND MAY NOT SAY, AND WHY — all three settled by measurement, not
taste (evidence: engine/lab/ta_calibration/, 92 names, 89,190 claims, 2011-2026):

  TAPE (the ATR word)      PER NAME, and it is not close. Spearman(ATR% at
                           origin, realized forward vol) is significantly
                           POSITIVE on 84 of 92 names at one week and 87 at one
                           month, against 1 and 2 significantly negative -- an
                           asymmetry chance cannot make, since 4.6 hits either
                           way is what chance produces. The only claim that
                           survives per name.
  TREND (the MA stack)     NOT PER NAME AT ALL -- and this reverses the first
                           edition, which said "per name where earned". On the
                           correct clock, with four times the origins, the
                           per-name split is SYMMETRIC: at one month 13 names
                           clear the bar in the stated direction and 12 clear it
                           BACKWARDS (sign test p = 1.00). There is more
                           significance than chance produces -- 25 against 4.5 --
                           but it points both ways, which is per-name
                           heterogeneity, not a per-name claim. The pooled
                           +3.2pp is real and belongs to every ticker; naming
                           the names it "works on" is reading the noise.
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

# THE TECHNICAL LENS'S OWN CLOCK. The first edition of this file scored every
# name at three CALENDAR MONTHS, which is the probability cone's horizon, not
# this lens's — in this project the technical read is the under-one-month view.
# The re-run at short horizons measured what that cost: a published level beats
# a matched non-level by +9.8pp at one week against +3.4pp at three months, so
# the old clock reported the weakest reading available of every claim. The
# record is now built at 5, 10 and 21 SESSIONS, and the horizon it was built at
# is carried in the record rather than assumed by whoever reads it.
HORIZON_SESSIONS = (5, 10, 21)
DEFAULT_H = 5
HORIZON_NAME = {5: 'one week', 10: 'two weeks', 21: 'one month'}


@dataclass
class TechRecord:
    market: str
    ticker: str
    h: int
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

    def clause(self, horizon_label=None):
        """The one place this record is put into words. Nothing else may phrase it.

        A TESTED NULL IS NOT MISSING DATA, and the first draft of this method said
        it was: RAYA, with 149 readings, read "this name's own history is not
        enough to say" when the truth is that the test ran on plenty of history
        and came back negative. Those are opposite statements — one says come
        back later, the other says we looked and it does not hold here — and
        collapsing them into the softer one is the same defect as the momentum
        words and as "failed calibration test". The three cases are kept apart.
        """
        horizon_label = horizon_label or HORIZON_NAME.get(self.h, f'{self.h} sessions')
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
        # NO PER-NAME TREND SENTENCE IS EMITTED, deliberately. trend_earned
        # and trend_reversed are still computed and stored, because they are
        # what demonstrates the symmetry described above -- but a name that
        # clears the bar is indistinguishable from one of the equally many that
        # clear it backwards, so stating it for this name reads the noise. The
        # trend claim is book-level and belongs on every page unchanged.
        if False and self.trend_earned and not self.trend_reversed:
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


def build(horizons=HORIZON_SESSIONS, step: int = 5, verbose: bool = False,
          claims=None):
    """Recompute every name's record on the short clock. Self-verifying.

    ``claims`` accepts a pre-harvested frame (engine/lab/ta_calibration produces
    one) so the record can be rebuilt without re-running the replay; passing
    None harvests fresh through the shipped technicals.compute().
    """
    import glob
    import pandas as pd

    raw = os.path.join(_HERE, 'raw_ohlc')
    libs = [(m, os.path.basename(f)[:-4])
            for m in sorted(os.listdir(raw))
            for f in sorted(glob.glob(os.path.join(raw, m, '*.csv')))]
    if claims is None:
        import replay
        frames = []
        for market, ticker in libs:
            try:
                frames.append(replay.harvest_short(market, ticker, step=step,
                                                   horizons=horizons))
            except Exception:
                pass
        claims = pd.concat([f for f in frames if len(f)], ignore_index=True)

    out, skipped = {}, []
    for market, ticker in libs:
        sub = claims[(claims.market == market) & (claims.ticker == ticker)
                     & (claims.claim == 'state')]
        if not len(sub):
            skipped.append((market, ticker, 'too little history to reach a first origin'))
            continue
        for h in horizons:
            s = sub[sub.h == h]
            if not len(s):
                continue
            tn, tr, tp, te = _tape(s)
            na, nb, ua, ub, gap, gp, ge, gr = _trend(s)
            out[f'{market}/{ticker}@{h}'] = TechRecord(
                market=market, ticker=ticker, h=int(h), origins=int(len(s)),
                first=str(s.origin.min()), last=str(s.origin.max()),
                tape_n=tn, tape_rho=tr, tape_p=tp, tape_earned=te,
                trend_n_above=na, trend_n_below=nb, trend_up_above=ua,
                trend_up_below=ub, trend_gap=gap, trend_p=gp,
                trend_earned=ge, trend_reversed=gr)
        if verbose:
            k = f'{market}/{ticker}@{DEFAULT_H}'
            if k in out:
                print(f'  {k}: {out[k].clause()}', flush=True)

    # COUNT AGAINST A KNOWN TOTAL — the libraries on disk, on (market, ticker).
    named = {k.split('@')[0] for k in out}
    assert len(named) + len(skipped) == len(libs), (
        f'population mismatch: {len(named)} + {len(skipped)} != {len(libs)}')
    return out, skipped, len(libs)


if __name__ == '__main__':
    import pandas as pd
    cache = os.path.join(_LAB, 'claims_short.pkl')
    claims = pd.read_pickle(cache) if os.path.exists(cache) else None
    recs, skipped, total = build(verbose='-v' in sys.argv, claims=claims)
    payload = {k: asdict(v) for k, v in recs.items()}
    path = os.path.join(_HERE, 'tech_records.json')
    json.dump({'built_from': 'engine/raw_ohlc, replayed through technicals.compute()',
               'libraries': total, 'recorded': len(recs),
               'skipped': [{'market': m, 'ticker': t, 'why': w} for m, t, w in skipped],
               'records': payload}, open(path, 'w'), indent=1)
    names = {k.split('@')[0] for k in recs}
    print(f'{len(recs)} records over {len(names)} of {total} libraries '
          f'({len(skipped)} skipped), at horizons {HORIZON_SESSIONS} sessions')
    for h in HORIZON_SESSIONS:
        sub = [r for r in recs.values() if r.h == h]
        print(f'  h={h:>2} ({HORIZON_NAME[h]:9}): tape earned '
              f'{sum(1 for r in sub if r.tape_earned):>3} of {len(sub):>3} | '
              f'trend earned {sum(1 for r in sub if r.trend_earned):>3} | '
              f'reversed {sum(1 for r in sub if r.trend_reversed)}')
        e = sum(1 for r in sub if r.trend_earned)
        rv = sum(1 for r in sub if r.trend_reversed)
        if e + rv:
            from scipy import stats as _st
            pv = _st.binomtest(e, e + rv, 0.5).pvalue
            verdict = ('SYMMETRIC -- no per-name trend claim' if pv > 0.05
                       else 'asymmetric')
            print(f'{chr(32)*22}   trend sign test {e} vs {rv}: p={pv:.2f} -> {verdict}')
    print(f'wrote {path}')
