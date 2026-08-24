"""band_record.py — [R-CAL-02] the investor-facing calibration object.

WHAT THIS REPLACES, AND WHY
---------------------------
Until 24-Aug-2026 every public surface carried the engine's three-way SKILL
verdict — PASS / PARITY / FAIL — a statement about whether a name's cone beat a
carry-anchored random walk on CRPS by a statistically significant margin. That
verdict remains the Step 0 gate and is untouched inside the engine (see
mc_v3.verdict); it simply no longer reaches a reader.

Two independent reasons, one of them a defect rather than a matter of taste:

1. IT ANSWERS THE WRONG QUESTION. An investor reading a cone wants to know
   whether the bands can be trusted — did the price actually land inside the
   90% band about 90% of the time? The skill verdict answers a modelling
   question instead: is our score better than a naive benchmark's? A cone can be
   perfectly honest and still tie, and at 1-3 month horizons a tie is the
   ordinary, expected outcome for a dispersion product that never claimed edge.

2. THE LABEL WAS FACTUALLY WRONG ON THE NAMES IT FLAGGED. The site called a FAIL
   a "failed calibration test". It is not a calibration test. Measured on the
   live panels on 24-Aug-2026, all five names then flagged FAIL had 90%-band
   coverage AT OR ABOVE 97% against a 90% target -- ADNOCDRILL 100.0% (15
   windows), ADNOCDIST 100.0% (30), BOROUGE 100.0% (12), EMPOWER 100.0% (10),
   CLHO 97.2% (36). Every one of them contained more outcomes than advertised;
   their bands were too WIDE, which is the opposite failure and a far more
   benign one. Meanwhile the five names whose bands genuinely ran NARROW --
   ISPH 76.7%, EMAAR 78.9%, RIBL 78.9%, IHC 80.9%, TMPV 81.0%, each significant
   at p<0.05 -- carried no flag at all. The scheme warned about cones that
   contained everything and stayed silent on cones that missed more often than
   they promised.

THE REPLACEMENT is two plain facts plus a flag that is only raised when earned:

  * THE BAND RECORD: "over N resolved three-month forecasts, the price finished
    inside the 90% band X% of the time" (target 90%). Directly checkable against
    the public ledger, no benchmark and no significance test to explain.
  * RECORD STRENGTH: long / short / market-only, from the resolved-window count.
  * A FLAG ONLY WHEN EARNED: bands ran narrow, or bands ran wide, when the name's
    own coverage sits outside a two-sided binomial test at the 5% level.
    Otherwise no flag -- the ordinary case is silence, not a verdict token.

WHERE THE STRENGTH THRESHOLDS COME FROM (derived 24-Aug-2026 on the live
93-panel book, not chosen round). Two independent readings agree:

  * POWER. A name's own coverage number is only worth printing if it could catch
    a cone that is badly miscalibrated. Testing a claimed 90% against a true 75%
    at the 5% level, power reaches the conventional 90% bar at n=40 (n=30: 80%,
    n=22: 68%, n=16: 60%). Below ~22 the 90% CI on the coverage estimate is
    wider than +/-10pp, so the number cannot separate an honest cone from a
    broken one and should not be read on its own.
  * THE BOOK'S OWN SHAPE. The window counts are not uniform: there is an EMPTY
    BAND at 17-21 windows and a second gap at 31-35, so cuts at 22 and 40 fall
    in real gaps and no name sits one resolved window from a boundary.

MIN_WINDOWS=28 in adaptive_width.py is a DIFFERENT gate for a different job (how
much own-history before a per-name width multiplier may move off 1.0) and is
deliberately not reused here; that one guards against over-correction, this one
guards against printing an unreadable number.

This module is the SINGLE SOURCE OF TRUTH for the public wording. Pages and
studies read it rather than restating a coverage figure in prose, because a
coverage number is volatile -- it moves on every grade.
"""
from __future__ import annotations

import glob
import os
from dataclasses import dataclass, asdict
from typing import Optional, List

PANEL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "panels")

# --- derived thresholds (see module docstring for the derivation) -------------
STRENGTH_LONG_MIN = 40    # >=90% power to catch a cone running 15pp narrow
STRENGTH_SHORT_MIN = 22   # below this the name's own coverage is unreadable
TARGET_COVERAGE = 0.90    # the band the record is stated against
FLAG_ALPHA = 0.05         # two-sided binomial level for narrow/wide

STRENGTH_LABEL = {
    "long":        "long record",
    "short":       "short record",
    "market-only": "market record only",
}
FLAG_LABEL = {
    "narrow": "bands ran narrow",
    "wide":   "bands ran wide",
    None:     "",
}


@dataclass
class BandRecord:
    """One name's public calibration record. Every field is computed."""
    instrument: str
    market: str
    n: int                      # resolved non-overlapping 3-month windows
    hits: int                   # of those, how many finished inside the 90% band
    cov50: Optional[float]
    cov80: Optional[float]
    cov90: Optional[float]
    ci_lo: Optional[float]      # 90% interval on cov90
    ci_hi: Optional[float]
    strength: str               # 'long' | 'short' | 'market-only'
    flag: Optional[str]         # 'narrow' | 'wide' | None
    p_value: Optional[float]

    # -- the public sentences; nothing else may phrase these ------------------
    def sentence(self) -> str:
        """The band record, as a reader sees it."""
        if self.strength == "market-only":
            return (f"{self.instrument} has {self.n} resolved three-month "
                    f"forecast{'s' if self.n != 1 else ''} of its own — too few to read on "
                    f"their own, so the bands are judged on the whole {self.market} panel "
                    f"instead, and this name's record is still accumulating.")
        pct = f"{self.cov90 * 100:.0f}%"
        s = (f"Over {self.n} resolved three-month forecasts, the price finished inside "
             f"the 90% band {pct} of the time.")
        if self.flag == "narrow":
            s += (" That is below the 90% these bands aim at: they have been running "
                  "narrower than advertised, so treat them as a floor on how far price "
                  "can travel, not a ceiling.")
        elif self.flag == "wide":
            s += (" That is above the 90% these bands aim at: they have been running "
                  "wider than they need to, so the real spread of outcomes has been "
                  "tighter than the cone shows.")
        else:
            s += " That is what the bands aim at."
        if self.strength == "short":
            s += (f" The record is short — {self.n} windows is enough to read but not "
                  f"enough to be precise about.")
        return s

    def chip(self) -> str:
        """The one-line label for a table cell or a page chip."""
        if self.strength == "market-only":
            return f"market record only ({self.n} own window{'s' if self.n != 1 else ''})"
        base = f"{self.cov90 * 100:.0f}% inside the 90% band, {self.n} windows"
        return f"{base} — {FLAG_LABEL[self.flag]}" if self.flag else base

    def to_dict(self) -> dict:
        return asdict(self)


def _binom_test(k: int, n: int, p: float) -> float:
    from scipy import stats
    return float(stats.binomtest(k, n, p).pvalue)


def _jeffreys_ci(k: int, n: int, level: float = 0.90):
    from scipy import stats
    lo, hi = stats.beta.ppf([(1 - level) / 2, 1 - (1 - level) / 2],
                            k + 0.5, n - k + 0.5)
    return float(lo), float(hi)


def strength_for(n: int) -> str:
    if n >= STRENGTH_LONG_MIN:
        return "long"
    if n >= STRENGTH_SHORT_MIN:
        return "short"
    return "market-only"


def from_panel(path: str) -> BandRecord:
    """Build a name's record from its committed 3-month calibration panel."""
    import pandas as pd
    base = os.path.basename(path)
    if not base.endswith("_3m.csv"):
        raise ValueError(f"band record reads the 3-month panel, got {base}")
    market, instrument = base[:-7].split("_", 1)
    d = pd.read_csv(path)
    n = len(d)
    if n == 0:
        raise ValueError(f"empty panel: {base}")
    hits = int(d["in90"].sum())
    strength = strength_for(n)
    if strength == "market-only":
        # The name's own number is not readable; do not compute a flag from it.
        return BandRecord(instrument, market, n, hits,
                          float(d["in50"].mean()), float(d["in80"].mean()),
                          float(d["in90"].mean()), None, None, strength, None, None)
    p = _binom_test(hits, n, TARGET_COVERAGE)
    lo, hi = _jeffreys_ci(hits, n)
    flag = None
    if p < FLAG_ALPHA:
        flag = "narrow" if hits / n < TARGET_COVERAGE else "wide"
    return BandRecord(instrument, market, n, hits,
                      float(d["in50"].mean()), float(d["in80"].mean()),
                      float(d["in90"].mean()), lo, hi, strength, flag, p)


# Ledger instrument names are not panel filenames, and the difference is not
# cosmetic: ADIB is a DIFFERENT BANK in each market -- ledger "ADIB" is the
# Egyptian one (EGP) and "ADIBUAE" the UAE one (AED), against panels EG_ADIB and
# AE_ADIB. Keying a record by bare name would silently hand one bank the other's
# coverage. Every record is therefore keyed (market, instrument), and every
# ledger name that is not identical to its panel name is resolved HERE,
# explicitly, and asserted -- never inferred from a filename.
LEDGER_ALIAS = {
    "2POINTZERO": ("AE", "TWOPOINTZERO"),
    "ADIB":       ("EG", "ADIB"),
    "ADIBUAE":    ("AE", "ADIB"),
    "ALRAJHI":    ("SA", "RAJHI"),
    "Gold":       ("XAU", "GOLD"),
    "Silver":     ("XAU", "SILVER"),
    "Platinum":   ("XPT", "PLATINUM"),
    "Kakao":      ("KR", "KAKAO"),
    "Samsung":    ("KR", "SAMSUNG"),
}


def all_records(panel_dir: str = PANEL_DIR) -> List[BandRecord]:
    out = []
    for f in sorted(glob.glob(os.path.join(panel_dir, "*_3m.csv"))):
        try:
            out.append(from_panel(f))
        except ValueError:
            continue
    return out


def by_key(panel_dir: str = PANEL_DIR) -> dict:
    """Records keyed (market, instrument) -- the only safe key, see LEDGER_ALIAS."""
    return {(r.market, r.instrument): r for r in all_records(panel_dir)}


def resolve(ledger_name: str, records: dict) -> BandRecord:
    """Map a ledger instrument to its panel record, or raise.

    Raises rather than returning None: a name that cannot be resolved must stop
    the build, not quietly publish no record ([R-ENF-01]).
    """
    if ledger_name in LEDGER_ALIAS:
        key = LEDGER_ALIAS[ledger_name]
        if key not in records:
            raise KeyError(f"alias {ledger_name} -> {key} has no panel")
        return records[key]
    hits = [r for (m, t), r in records.items() if t == ledger_name]
    if len(hits) == 1:
        return hits[0]
    if not hits:
        raise KeyError(f"no panel for ledger instrument {ledger_name!r}; "
                       f"add it to LEDGER_ALIAS")
    raise KeyError(f"ledger instrument {ledger_name!r} matches {len(hits)} panels "
                   f"({[r.market for r in hits]}); it needs a LEDGER_ALIAS entry")


def market_record(market: str, panel_dir: str = PANEL_DIR) -> dict:
    """The pooled fallback a market-only name is judged on. Computed, never quoted."""
    import pandas as pd
    n = hits = names = 0
    for f in sorted(glob.glob(os.path.join(panel_dir, f"{market}_*_3m.csv"))):
        d = pd.read_csv(f)
        n += len(d); hits += int(d["in90"].sum()); names += 1
    if not n:
        raise ValueError(f"no panels for market {market}")
    return {"market": market, "names": names, "n": n, "hits": hits, "cov90": hits / n}


def assert_no_verdict_tokens(text: str, where: str = "") -> None:
    """[R-CAL-02] Public surfaces carry no skill-verdict vocabulary.

    Fails rather than warns, per [R-ENF-01]: a rule that can be checked is
    checked from outside the thing it governs.
    """
    import re
    banned = [
        (r"\bPARITY\b", "PARITY"),
        (r"\bmatches benchmark\b", "matches benchmark"),
        (r"failed calibration", "failed calibration"),
        (r"\bCRPS\b", "CRPS"),
        (r"calibration (?:test |gate )?(?:FAIL|PASS)\b", "calibration PASS/FAIL"),
    ]
    hits = [lab for pat, lab in banned if re.search(pat, text, re.I)]
    if hits:
        raise AssertionError(
            f"[R-CAL-02] skill-verdict vocabulary on a public surface"
            f"{' (' + where + ')' if where else ''}: {', '.join(sorted(set(hits)))}")


if __name__ == "__main__":
    recs = all_records()
    by = {}
    for r in recs:
        by.setdefault(r.strength, []).append(r)
    print(f"{len(recs)} names — " + ", ".join(
        f"{k}: {len(v)}" for k, v in sorted(by.items())))
    print()
    for r in recs:
        if r.flag:
            print(f"  {r.flag.upper():6s} {r.instrument:12s} {r.chip()}")
