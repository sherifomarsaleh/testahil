"""The statement walk-forward's DECISION RULE — when a measured bias is acted on.

WHY THIS EXISTS. The fundamental walk-forward has measured five companies and
changed almost nothing. The standing rule said a correction enters the live
drivers only if it passes its own test AND is consistent with how that driver
class is built across the book, and otherwise it is a WATCH FLAG — "recorded,
graded live, revisited at every refit, acted on by nobody". The second clause is
real and has done its job; the trouble is that "watch flag" became the DEFAULT,
so the measurement layer produced findings and the valuation layer never heard
them. PHDC's profit over-forecast (+1.12 log, 97% of cells) and TMGH's sales
under-forecast (-0.88 log) are the two largest numbers this project has measured
about its own method, and neither moved a driver.

WHAT THIS MODULE IS. A pre-registered rule, fixed here BEFORE it is run on any
record, that decides three things mechanically:

    1. IS THE BIAS REAL?      robust across bootstrap block sizes {2,3,4}
    2. IS IT STABLE?          the sign holds in every era with enough cells
    3. DOES CORRECTING HELP?  the driver beats FREEZE out of sample

and then, only if all three hold, HOW HARD to correct — by shrinkage toward zero
on the bias's own standard error, never by a typed fraction.

THE STRENGTH IS DERIVED, NOT CHOSEN. The old rule applied corrections at "HALF
STRENGTH by default". A half is a free parameter: it is the same number whether
a bias is measured on eight cells or eighty, and this house forbids free
parameters everywhere else. The shrinkage below is the ordinary reliability
weight — treat the observed bias b as a true bias plus noise of standard error
se, and the posterior mean is

    correction = b * max(0, 1 - se^2 / b^2)

which is zero when the bias is indistinguishable from noise, approaches the full
bias when it is measured precisely, and happens to land near half strength when
b is about 1.4 standard errors — so the retired default was not absurd, it was
just the right answer for one particular signal-to-noise ratio applied to all of
them.

WHAT THIS MODULE IS NOT. It does not decide whether a correction is CONSISTENT
with how the driver class is built across the market's book. That clause stands
untouched and stays a human judgement, because it is the clause that caught the
finance-cost correction which passed every statistical test and was arithmetic
rather than evidence. A correction this module ADOPTS is a correction that has
earned its statistics; it still has to clear that second gate before it reaches
a live driver, and `verdict()` says so in as many words.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

# ---------------------------------------------------------------------------
# PRE-REGISTERED CONSTANTS. Fixed here before the rule is run on any record, so
# that no threshold can be chosen after seeing which names it would promote.
# Each is a bar, not a tuning knob, and each says what it is for.

BLOCKS = (2, 3, 4)          # the house robustness bar, mirrored from the engine
MIN_CELLS = 8               # below this a bias is a handful of observations
MIN_ERA_CELLS = 5           # an era with fewer cells cannot vote on stability
CI_LEVEL_Z = 1.959964       # the bootstrap intervals are 95%, two-sided
MIN_SKILL_VS_FREEZE = 0.0   # beating "no change" is the bar, not beating it well

# A correction smaller than this in log terms is not worth carrying: it is
# inside the rounding of the drivers it would adjust, and every carried
# correction is a thing a future reader has to understand.
MIN_MATERIAL_CORRECTION = 0.05


@dataclass
class Verdict:
    """What the rule decided about one driver, and every reason behind it."""
    driver: str
    bias: float
    n: int
    se: Optional[float]
    robust: bool
    era_stable: bool
    era_detail: Dict[str, float]
    beats_freeze: Optional[bool]
    freeze_skill: Optional[float]
    shrinkage: Optional[float]
    correction: float
    decision: str            # 'adopt' | 'watch' | 'none'
    reasons: List[str] = field(default_factory=list)

    def as_dict(self):
        d = dict(self.__dict__)
        d["reasons"] = list(self.reasons)
        return d


def se_from_bootstrap(boot: dict) -> Optional[float]:
    """The bias's standard error, read from the WIDEST bootstrap interval.

    The widest block is the most conservative reading of how much the estimate
    moves when neighbouring observations are allowed to travel together, and
    these cells are anything but independent — the same origin feeds five
    horizons and the same year appears in five origins. Taking the narrowest
    interval would overstate the precision of exactly the quantity this rule
    scales its correction by.
    """
    if not boot:
        return None
    widths = []
    for b in BLOCKS:
        v = boot.get(str(b)) or boot.get(b)
        if not v:
            continue
        lo, hi = v.get("lo"), v.get("hi")
        if lo is None or hi is None:
            continue
        widths.append(abs(hi - lo))
    if not widths:
        return None
    return max(widths) / (2.0 * CI_LEVEL_Z)


def is_robust(boot: dict) -> bool:
    """The interval excludes zero at EVERY block size, not the best one.

    A sign that survives only at one block length is a sign that survives only
    at one guess about how the observations clump together.
    """
    if not boot:
        return False
    seen = 0
    for b in BLOCKS:
        v = boot.get(str(b)) or boot.get(b)
        if not v or v.get("lo") is None or v.get("hi") is None:
            return False
        seen += 1
        if v["lo"] <= 0.0 <= v["hi"]:
            return False
    return seen == len(BLOCKS)


def era_stability(era_block: dict) -> (bool, Dict[str, float]):
    """A bias that changes sign between eras is not a bias.

    The standing protocol already says so — 'report the instability, never
    correct for it: the average of two opposite regimes was true in neither' —
    and this makes it mechanical. Eras too thin to vote are excluded and named
    rather than counted as agreement, because an era with three cells agreeing
    by chance is not evidence of stability.
    """
    detail, signs = {}, []
    for era, v in (era_block or {}).items():
        n = v.get("n", 0)
        b = v.get("bias")
        if b is None:
            continue
        detail[era] = b
        if n >= MIN_ERA_CELLS:
            signs.append(1 if b > 0 else (-1 if b < 0 else 0))
    if len(signs) < 2:
        # one era cannot demonstrate stability ACROSS eras; the rule declines to
        # call it stable rather than passing it by default
        return False, detail
    return (all(s > 0 for s in signs) or all(s < 0 for s in signs)), detail


def freeze_skill(horizon_block: dict) -> Optional[float]:
    """Cell-weighted skill against FREEZE across the horizons that resolved.

    A method that cannot beat 'write down last year's number' has not earned the
    precision it displays — that is the protocol's sentence and it is not a
    figure of speech. Weighting by cells stops a single thin horizon from
    carrying the verdict.
    """
    num = den = 0.0
    for _h, blk in (horizon_block or {}).items():
        sk = (blk or {}).get("skill_freeze") or {}
        n, s = sk.get("n"), sk.get("skill")
        if not n or s is None:
            continue
        num += n * s
        den += n
    return (num / den) if den else None


def shrink(bias: float, se: Optional[float]) -> (float, Optional[float]):
    """Reliability weight: how much of the measured bias survives its own noise.

    correction = bias * max(0, 1 - se^2 / bias^2)

    Zero when the bias is indistinguishable from noise; the whole bias when it
    is measured precisely. This REPLACES the typed half-strength default, which
    applied the same fraction to a bias measured on eight cells and one measured
    on eighty.
    """
    if se is None or se <= 0 or bias == 0:
        return 0.0, None
    k = max(0.0, 1.0 - (se * se) / (bias * bias))
    return bias * k, k


def decide(driver: str, driver_block: dict, era_block: dict,
           horizon_block: dict) -> Verdict:
    """Run the rule on one driver's committed score record."""
    bias = driver_block.get("bias", 0.0)
    n = driver_block.get("n", 0)
    boot = driver_block.get("boot") or {}
    se = se_from_bootstrap(boot)
    robust = is_robust(boot)
    stable, era_detail = era_stability(era_block)
    sk = freeze_skill(horizon_block)
    beats = None if sk is None else (sk > MIN_SKILL_VS_FREEZE)
    corr, k = shrink(bias, se)

    reasons = []
    if n < MIN_CELLS:
        reasons.append("only %d resolved cells, below the %d the rule requires"
                       % (n, MIN_CELLS))
    if not robust:
        reasons.append("the bootstrap interval covers zero at one or more block "
                       "sizes, so the sign is not robust")
    if not stable:
        if len([e for e, _ in era_detail.items()]) < 2:
            reasons.append("only one era has enough cells to vote, so stability "
                           "across regimes is undemonstrated rather than shown")
        else:
            reasons.append("the sign is not the same in every era with enough "
                           "cells: %s" % ", ".join("%s %+.3f" % (e, b)
                                                   for e, b in era_detail.items()))
    if beats is False:
        reasons.append("the driver does not beat FREEZE out of sample "
                       "(skill %+.4f), so correcting a bias in a forecast worse "
                       "than 'no change' would be polishing the wrong object" % sk)
    if beats is None:
        reasons.append("no FREEZE comparison is recorded for this driver, and "
                       "an absent benchmark is not a passed one")
    if abs(corr) < MIN_MATERIAL_CORRECTION:
        reasons.append("the shrunk correction is %+.4f in log terms, inside the "
                       "materiality floor of %.2f" % (corr, MIN_MATERIAL_CORRECTION))

    passes = (n >= MIN_CELLS and robust and stable and beats is True
              and abs(corr) >= MIN_MATERIAL_CORRECTION)
    if passes:
        decision = "adopt"
        reasons.append("robust across blocks %s, sign stable in every era with "
                       "at least %d cells, beats FREEZE by %+.4f, and the bias "
                       "of %+.4f shrinks to %+.4f on its own standard error of "
                       "%.4f (weight %.2f)"
                       % (list(BLOCKS), MIN_ERA_CELLS, sk, bias, corr, se, k))
    elif n >= MIN_CELLS and (robust or stable):
        decision = "watch"
    else:
        decision = "none"

    return Verdict(driver=driver, bias=bias, n=n, se=se, robust=robust,
                   era_stable=stable, era_detail=era_detail,
                   beats_freeze=beats, freeze_skill=sk,
                   shrinkage=k, correction=(corr if passes else 0.0),
                   decision=decision, reasons=reasons)


def run(scores: dict) -> Dict[str, Verdict]:
    """Apply the rule to every driver in one study's committed scores.json."""
    by_driver = scores.get("by_driver") or {}
    by_era = scores.get("by_era") or {}
    by_h = scores.get("by_horizon") or {}
    return {d: decide(d, blk, by_era.get(d) or {}, by_h.get(d) or {})
            for d, blk in by_driver.items()}


def summary(verdicts: Dict[str, Verdict]) -> dict:
    counts = {"adopt": 0, "watch": 0, "none": 0}
    for v in verdicts.values():
        counts[v.decision] += 1
    return {"drivers": len(verdicts), **counts,
            "adopted": sorted(d for d, v in verdicts.items() if v.decision == "adopt")}


if __name__ == "__main__":
    import glob
    import json
    import os
    import sys

    paths = sys.argv[1:] or sorted(glob.glob(
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                     "*_walkforward", "scores.json")))
    print("THE DECISION RULE, run on every committed walk-forward record")
    print("=" * 78)
    total = {"adopt": 0, "watch": 0, "none": 0}
    for p in paths:
        tk = os.path.basename(os.path.dirname(p)).replace("_walkforward", "").upper()
        try:
            sc = json.load(open(p))
        except Exception as exc:
            print("\n%-6s could not be read: %s" % (tk, exc))
            continue
        v = run(sc)
        s = summary(v)
        for k in total:
            total[k] += s[k]
        print("\n%-6s %d drivers -> adopt %d, watch %d, none %d"
              % (tk, s["drivers"], s["adopt"], s["watch"], s["none"]))
        for d, vv in sorted(v.items(), key=lambda kv: -abs(kv[1].bias)):
            mark = {"adopt": "ADOPT", "watch": "watch", "none": "  -  "}[vv.decision]
            print("   %-5s %-22s bias %+7.4f  n=%-3d %s"
                  % (mark, d[:22], vv.bias, vv.n,
                     ("correction %+.4f" % vv.correction) if vv.decision == "adopt"
                     else vv.reasons[0][:72] if vv.reasons else ""))
    print("\n" + "=" * 78)
    print("across every record: adopt %d, watch %d, none %d"
          % (total["adopt"], total["watch"], total["none"]))
