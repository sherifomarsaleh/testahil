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

import os
import re
import sys
from dataclasses import dataclass
from typing import Optional, List

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)                      # panel_refresh imports flat
from panel_refresh import PANELS_DIR, panel_path, existing_panel_names  # noqa: E402,F401

PANEL_DIR = PANELS_DIR                             # panel layout has ONE owner


def _registry():
    """scripts/build_market_registry.py — the repo's existing market/name registry.

    Loaded by path because scripts/ is not a package. Everything below that could
    be a second copy of a mapping it already owns is derived from it instead.
    """
    import importlib.util
    path = os.path.join(_ROOT, "scripts", "build_market_registry.py")
    spec = importlib.util.spec_from_file_location("_bmr", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

# --- derived thresholds (see module docstring for the derivation) -------------
STRENGTH_LONG_MIN = 40    # >=90% power to catch a cone running 15pp narrow
STRENGTH_SHORT_MIN = 22   # below this the name's own coverage is unreadable
TARGET_COVERAGE = 0.90    # the band the record is stated against
FLAG_ALPHA = 0.05         # two-sided binomial level for narrow/wide

FLAG_LABEL = {"narrow": "bands ran narrow", "wide": "bands ran wide"}

# Reader-facing market names come from the registry that already generates them
# into assets/markets.js, so a panel has ONE public name. Two generator scripts
# briefly carried their own dicts here and had already disagreed on AE
# ("Abu Dhabi and Dubai" vs "UAE") — the two-sources-of-truth class this whole
# change exists to close, reintroduced one layer up.
MARKET_LABEL = {m: meta["short"] for m, meta in _registry().MARKET_META}
MARKET_HEADING = {m: meta["label"] for m, meta in _registry().MARKET_META}
# Panels are per market code; the registry groups XAU and XPT as one book.
MARKET_GROUP = {m: meta["group"] for m, meta in _registry().MARKET_META}


def pct(v):
    """The ONE rounding rule for a published coverage figure.

    Python's format uses banker's rounding and JS Math.round does not: at 37/40
    the page's static text would print 92% and the same page's rendered text 93%.
    Both sides now round half-up. assets/app.js carries the transliteration.
    """
    return f"{int(v * 100 + 0.5)}%"


# --- verdict vocabulary: ONE table, read by the gate AND by the assert below --
# Case matters. The verdict was always written in caps, while lowercase "parity"
# is an ordinary word in this book (a currency peg, an export price basis) — a
# case-insensitive ban flagged five such lines, and a check that cries wolf is
# one everyone learns to ignore.
BANNED_CASE_SENSITIVE = [(r"\bPARITY\b", "PARITY"), (r"\bROBUST FAIL\b", "ROBUST FAIL")]
BANNED = [
    (r"BOUNDARY\s*\(PARITY", "BOUNDARY(PARITY)"),
    (r"matches benchmark", "matches benchmark"),
    (r"failed calibration", "failed calibration"),
    (r"no single-name edge", "no single-name edge"),
    (r"calibration (?:test |gate )?(?:FAILS?|PASSES?)\b", "calibration PASS/FAIL"),
    (r"skill-validated", "skill-validated"),
]
# CRPS is a legitimate methodology explanation where the scoring rule is taught,
# and nowhere else: naming it beside a company is the verdict wearing a hat.
CRPS_ALLOWED_IN = {"method.html"}


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
    strength: str               # 'long' | 'short' | 'market-only'
    flag: Optional[str]         # 'narrow' | 'wide' | None
    p_value: Optional[float]    # why the flag fired (or did not)

    # -- THE public sentences. Nothing else may phrase these ------------------
    # Every surface renders through here: both generators, and assets/app.js as a
    # literal transliteration for the render-time refresh. Six independent
    # phrasings existed briefly and had already drifted — one page's static text
    # said "the Abu Dhabi and Dubai panel", the same page said "the UAE panel" on
    # the coverage index, and app.js overwrote both with "that panel" at render
    # time. Three public names for one panel, in a change written to stop exactly
    # that.

    def record_clause(self, inner_bands=True, arabic=False, one_sentence=False):
        """The volatile sentence — the one app.js also rewrites at render time.

        one_sentence=True keeps the whole clause to a SINGLE sentence, for
        surfaces that splice by sentence (the coverage index). A two-sentence
        clause there left an orphaned tail on every regeneration, which then
        duplicated on the next run.
        """
        if self.strength == "market-only":
            m = market_record(self.market)
            lab = MARKET_LABEL.get(self.market, self.market)
            if arabic:
                return (f"لم يُغلق سوى {self.n} توقعاً ربع سنوياً خاصاً بهذا السهم — أقل من أن "
                        f"يُحكم به عليه وحده، لذا فالنطاقات هي نطاقات السوق: {m['n']} توقعاً عبر "
                        f"{m['names']} اسماً أنهت داخل نطاق الـ90% بنسبة {pct(m['cov90'])}.")
            head = (f"Only {self.n} three-month forecast{'s' if self.n != 1 else ''} of its own "
                    f"ha{'ve' if self.n != 1 else 's'} resolved so far — too few to say anything "
                    f"reliable about this name specifically, so no name-level claim is made")
            pool = (f"the market&rsquo;s: across the {m['names']} names in the {lab} panel, "
                    f"{m['n']} resolved forecasts finished inside their 90% bands "
                    f"{pct(m['cov90'])} of the time.")
            return (f"{head}, and the bands are {pool}" if one_sentence
                    else f"{head}. The bands are {pool}")
        if arabic:
            return (f"عبر {self.n} توقعاً ربع سنوياً مُنجزاً، أنهى السعر داخل نطاق الـ90% بنسبة "
                    f"{pct(self.cov90)} من المرات، مقابل الـ90% المستهدفة.")
        s = (f"Over {self.n} resolved three-month forecasts, the price finished inside the 90% "
             f"band {pct(self.cov90)} of the time, against the 90% that band aims at")
        s += (f" — and inside the 80% and 50% bands {pct(self.cov80)} and {pct(self.cov50)} "
              f"of the time." if inner_bands else ".")
        join = (" — ", "") if one_sentence else (" That is ", "That is ")
        if self.flag == "narrow":
            s = s[:-1] + join[0] + ("short of what the bands promise: they have been running "
                 "narrower than the evidence supports, so read the range as a floor on how far "
                 "price can travel, not a ceiling.")
        elif self.flag == "wide":
            s = s[:-1] + join[0] + ("more than the bands promise: the real spread of outcomes "
                 "has been tighter than the cone shows — the safer direction to be wrong in, "
                 "but still a miss.")
        return s

    def chip(self):
        """The one-line label for a table cell or a page chip."""
        if self.strength == "market-only":
            return f"market record only ({self.n} own window{'s' if self.n != 1 else ''})"
        base = f"{pct(self.cov90)} inside the 90% band, {self.n} windows"
        return f"{base} — {FLAG_LABEL[self.flag]}" if self.flag else base


def _binom_test(k: int, n: int, p: float) -> float:
    from scipy import stats
    return float(stats.binomtest(k, n, p).pvalue)


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
    # Three columns of twenty-five. Coverage is the mean of the in-band flags,
    # the same definition mc_v3.pooled_scores uses (asserted in __main__).
    d = pd.read_csv(path, usecols=["in50", "in80", "in90"])
    n = len(d)
    if n == 0:
        raise ValueError(f"empty panel: {base}")
    hits = int(d["in90"].sum())
    strength = strength_for(n)
    if strength == "market-only":
        # The name's own number is not readable; do not compute a flag from it.
        return BandRecord(instrument, market, n, hits,
                          float(d["in50"].mean()), float(d["in80"].mean()),
                          float(d["in90"].mean()), strength, None, None)
    p = _binom_test(hits, n, TARGET_COVERAGE)
    flag = None
    if p < FLAG_ALPHA:
        flag = "narrow" if hits / n < TARGET_COVERAGE else "wide"
    return BandRecord(instrument, market, n, hits,
                      float(d["in50"].mean()), float(d["in80"].mean()),
                      float(d["in90"].mean()), strength, flag, p)


# Ledger instrument names are not panel filenames, and the difference is not
# cosmetic: ADIB is a DIFFERENT BANK in each market -- ledger "ADIB" is the
# Egyptian one (EGP) and "ADIBUAE" the UAE one (AED), against panels EG_ADIB and
# AE_ADIB. Keying a record by bare name would silently hand one bank the other's
# coverage. Every record is therefore keyed (market, instrument), and every
# ledger name that is not identical to its panel name is resolved HERE,
# explicitly, and asserted -- never inferred from a filename.
def _ledger_alias():
    """Ledger instrument name -> (market, panel name).

    DERIVED from scripts/build_market_registry.ALIAS, which already owns this
    mapping in the other direction ("AE/TWOPOINTZERO" -> "2POINTZERO") and is
    asserted bijective there against both LEDGER and TICKERS. It was briefly
    hand-copied here, which meant a new covered name with a spelling mismatch
    needed two edits in two key shapes — miss one and a surface mis-keys silently.

    The mapping is not cosmetic: ADIB is a DIFFERENT BANK per market — ledger
    "ADIB" is the Egyptian one and "ADIBUAE" the UAE one, against panels EG_ADIB
    and AE_ADIB — so a bare-name key would hand one bank the other's coverage.
    """
    out = {}
    for key, ledger_name in _registry().ALIAS.items():
        market, panel = key.split("/", 1)
        out[ledger_name] = (market, panel)
    # The inverse of an alias can leave the un-aliased twin ambiguous: with
    # AE/ADIB claimed by ADIBUAE, plain "ADIB" still matches two panels, so it
    # needs the one entry the registry's direction cannot express.
    for ledger_name, (market, panel) in list(out.items()):
        if panel not in out and sum(1 for k in _registry().ALIAS if k.endswith("/" + panel)) == 1:
            twins = [m for m in MARKET_LABEL if os.path.exists(panel_path(m, panel, "3m"))]
            if len(twins) == 2:
                other = [m for m in twins if m != market][0]
                out.setdefault(panel, (other, panel))
    return out


LEDGER_ALIAS = _ledger_alias()


_CACHE = {}


def all_records(panel_dir: str = PANEL_DIR) -> List[BandRecord]:
    """Every name's record. Memoized per panel_dir: a full sweep parses 93 CSVs,
    and the callers together were doing it 25 times per CI run."""
    if panel_dir not in _CACHE:
        out = []
        for f in sorted(existing_panel_names_paths(panel_dir)):
            try:
                out.append(from_panel(f))
            except ValueError:
                continue
        _CACHE[panel_dir] = out
    return _CACHE[panel_dir]


def existing_panel_names_paths(panel_dir: str = PANEL_DIR) -> List[str]:
    import glob
    return sorted(glob.glob(os.path.join(panel_dir, "*_3m.csv")))


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
    """The pooled fallback a market-only name is judged on.

    Summed from the records already in memory rather than re-reading the market's
    panels: it was re-globbing and re-parsing on every call, and the generators
    call it once per market-only name — 458 redundant panel reads in one pass,
    growing with coverage.
    """
    sub = [r for r in all_records(panel_dir) if r.market == market]
    if not sub:
        raise ValueError(f"no panels for market {market}")
    n = sum(r.n for r in sub)
    hits = sum(r.hits for r in sub)
    return {"market": market, "names": len(sub), "n": n, "hits": hits, "cov90": hits / n}


def scan_text(text: str, where: str = "") -> List[str]:
    """Verdict vocabulary in `text`, as report lines. The gate and the generators
    both call this, so they cannot reach opposite conclusions on one string."""
    hits = []
    checks = [(p, lab, 0) for p, lab in BANNED_CASE_SENSITIVE]
    checks += [(p, lab, re.I) for p, lab in BANNED]
    if where not in CRPS_ALLOWED_IN:
        checks.append((r"\bCRPS\b", "CRPS outside the methodology page", 0))
    for pat, label, flags in checks:
        for m in re.finditer(pat, text, flags):
            line = text[:m.start()].count("\n") + 1
            hits.append(f"{where}:{line}: {label}" if where else f"{label}")
    return hits


def assert_no_verdict_tokens(text: str, where: str = "") -> None:
    """[R-CAL-02] Public surfaces carry no skill-verdict vocabulary.

    Fails rather than warns, per [R-ENF-01]: a rule that can be checked is
    checked from outside the thing it governs.
    """
    hits = scan_text(text, where)
    if hits:
        raise AssertionError(f"[R-CAL-02] skill-verdict vocabulary: {'; '.join(hits)}")


def _selfcheck():
    """Coverage here must equal the engine's own definition of panel coverage.

    mc_v3.pooled_scores() is what the calibration gate reports cov50/80/90 from.
    This module reads three columns directly instead (cheaper, and it needs no
    benchmark columns), so the two definitions are pinned together here rather
    than left to drift apart silently.
    """
    import pandas as pd
    import mc_v3
    path = existing_panel_names_paths()[0]
    got = from_panel(path)
    ref, _ = mc_v3.pooled_scores([pd.read_csv(path)])
    for k, mine in (("cov50", got.cov50), ("cov80", got.cov80), ("cov90", got.cov90)):
        assert abs(ref[k] - mine) < 1e-12, f"{k}: {mine} vs pooled_scores {ref[k]}"
    return os.path.basename(path)


if __name__ == "__main__":
    print(f"coverage definition agrees with mc_v3.pooled_scores on {_selfcheck()}")
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
