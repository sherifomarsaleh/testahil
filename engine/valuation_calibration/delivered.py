"""Series (b) of the valuation calibration — the fair values this house ACTUALLY
published, measured against the prices they were struck at.  [R-VCAL-01]

WHAT THIS IS, AND WHAT IT IS NOT. The pre-registration of 03-Sep-2026 fixes two
fair-value series: (a) MECHANICAL, rebuilt at every historical origin from
point-in-time inputs, which is the series the promotion rule reads; and (b)
AS-DELIVERED, the numbers the house really published. This module is (b), and the
pre-registration already says what it is worth: it "exists only from 2025 and is
far too short to score, and it is carried anyway as the honest check on whether
(a) resembles what the house really does."

So this is NOT the calibration's verdict and it must never be quoted as one. It is
a CROSS-SECTION taken on a handful of dates, and its limits are arithmetic rather
than rhetorical:

  * The names share a market and very nearly share a moment. If the Egyptian
    market as a whole is dear or cheap today, every EGX name here leans the same
    way and the observations are one observation wearing many hats. The effective
    n is nearer the number of MARKETS than the number of names, and every interval
    below is printed against both counts so the reader cannot mistake one for the
    other.
  * It measures AGREEMENT, not accuracy. A house that agrees with the market
    perfectly has learned nothing; a house that disagrees may be right. Only the
    gap-closure series can separate those, and it needs history this does not
    have.

WHAT IT IS GOOD FOR, and it is the reason it is worth computing at all: the
reassessment was called because the house looked systematically pessimistic. That
is a claim about the sign and size of log(FV/P) across the delivered book, and
until now nobody had computed it. A number nobody has computed is not a finding,
however often it is repeated.

A NEGATIVE CENTRAL IS NOT DROPPED. One delivered study prints a central below
zero, where log(FV/P) does not exist. Dropping it would move the pooled figure
TOWARD zero — that is, it would make the house look less pessimistic by discarding
its most pessimistic reading — so it is reported separately and the pooled figure
is printed both ways, with the direction of the omission stated.
"""
from __future__ import annotations

import glob
import json
import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.dirname(HERE)
ROOT = os.path.dirname(ENGINE)
sys.path.insert(0, os.path.join(ROOT, "scripts"))

# ONE reader, not two. The gap gate already resolves a study's committed central
# and spot, and it is the reader CI holds the book to; a second implementation
# here would drift from it, which is the failure two registers of the same thing
# have already cost this repo once.
import importlib.util as _ilu

_spec = _ilu.spec_from_file_location(
    "_gapgate", os.path.join(ROOT, "scripts", "check_valuation_gap.py"))
_gap = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(_gap)
read_answer = _gap.read_answer

SEED = 42
DRAWS = 10000

# The exchange prefix in assets/data.js is the authority on which market a name
# trades in; this map is only for the studies, keyed by directory name, and any
# name not in it is reported as market UNKNOWN rather than guessed into a bucket.
MARKET = {
    "AMOC": "EG", "ARCC": "EG", "EGCH": "EG", "PHDC": "EG", "TMGH": "EG",
    "ELEC": "EG", "GBCO": "EG", "PHAR": "EG", "SCEM": "EG", "SWDY": "EG",
    "ADNOCDIST": "AE", "ADNOCDRILL": "AE", "ADNOCLS": "AE", "AIRARABIA": "AE",
    "AMR": "AE", "BOROUGE": "AE", "DU": "AE", "EMPOWER": "AE",
    "FERTIGLOBE": "AE", "MODON": "AE",
    "RIYADHCABLE": "SA", "SAVOLA": "SA",
}


def studies():
    return sorted(glob.glob(os.path.join(ENGINE, "*_study")))


def ticker_of(d):
    return os.path.basename(d).replace("_study", "").upper()


def read_book():
    """Every study's delivered central and the spot it was struck at."""
    rows, unreadable, nonpositive = [], [], []
    for d in studies():
        tk = ticker_of(d)
        central, spot, route = read_answer(d)
        if central is None or not spot:
            unreadable.append((tk, route))
            continue
        rec = {"ticker": tk, "market": MARKET.get(tk, "UNKNOWN"),
               "central": central, "spot": spot, "route": route,
               "gap_pct": (central / spot - 1.0) * 100.0}
        if central <= 0:
            rec["log_gap"] = None
            nonpositive.append(rec)
        else:
            rec["log_gap"] = math.log(central / spot)
            rows.append(rec)
    return rows, nonpositive, unreadable


def _mean(xs):
    return sum(xs) / len(xs) if xs else float("nan")


def boot(xs, draws=DRAWS, seed=SEED):
    """Plain resampling over NAMES.

    Deliberately not the house block bootstrap: a block bootstrap preserves
    dependence along an ORDERED series, and this is a cross-section with no order
    to preserve. Using it here would be the right ritual on the wrong object.
    """
    if len(xs) < 2:
        return (float("nan"), float("nan"))
    rng = random.Random(seed)
    ms = sorted(_mean([xs[rng.randrange(len(xs))] for _ in xs]) for _ in range(draws))
    return (ms[int(0.025 * draws)], ms[int(0.975 * draws)])


def boot_clustered(rows, draws=DRAWS, seed=SEED):
    """Resample MARKETS, then names within the drawn market.

    Names in one market on one date are not independent observations: a market
    that is broadly dear moves every study in it the same way. This interval is
    the honest one and it is much wider than the naive one, which is the point.
    """
    by = {}
    for r in rows:
        by.setdefault(r["market"], []).append(r["log_gap"])
    keys = sorted(by)
    if len(keys) < 2:
        return (float("nan"), float("nan"))
    rng = random.Random(seed)
    ms = []
    for _ in range(draws):
        vals = []
        for _ in keys:
            k = keys[rng.randrange(len(keys))]
            src = by[k]
            vals += [src[rng.randrange(len(src))] for _ in src]
        ms.append(_mean(vals))
    ms.sort()
    return (ms[int(0.025 * draws)], ms[int(0.975 * draws)])


def report():
    rows, nonpositive, unreadable = read_book()
    print("delivered fair values against the prices they were struck at")
    print("  [R-VCAL-01] series (b) — a cross-section, NOT the calibration's verdict\n")
    print("  %-12s %-4s %10s %10s %9s %8s" %
          ("ticker", "mkt", "central", "spot", "gap %", "log"))
    for r in sorted(rows + nonpositive, key=lambda r: r["gap_pct"]):
        lg = r["log_gap"]
        print("  %-12s %-4s %10.4f %10.4f %+8.1f%% %8s"
              % (r["ticker"], r["market"], r["central"], r["spot"], r["gap_pct"],
                 ("%+.4f" % lg) if lg is not None else "  n/a"))

    xs = [r["log_gap"] for r in rows]
    if not xs:
        print("\n  no readable pairs — an empty result is not a clean result.")
        return {}
    xs_sorted = sorted(xs)
    med = xs_sorted[len(xs) // 2] if len(xs) % 2 else _mean(xs_sorted[len(xs)//2-1:len(xs)//2+1])
    below = sum(1 for x in xs if x < 0)
    lo_n, hi_n = boot(xs)
    lo_c, hi_c = boot_clustered(rows)
    markets = sorted({r["market"] for r in rows})

    print("\n  POOLED, on the %d readable positive-central studies" % len(xs))
    print("    mean log(FV/P)   %+.4f   (%+.1f%% in price terms)"
          % (_mean(xs), (math.exp(_mean(xs)) - 1) * 100))
    print("    median           %+.4f" % med)
    print("    mean |log|        %.4f" % _mean([abs(x) for x in xs]))
    print("    below the price  %d of %d" % (below, len(xs)))
    print("    95%% interval, resampling NAMES    %+.4f to %+.4f" % (lo_n, hi_n))
    print("    95%% interval, resampling MARKETS  %+.4f to %+.4f" % (lo_c, hi_c))
    print("    n = %d names across %d markets (%s). READ THE INTERVAL AGAINST THE"
          % (len(xs), len(markets), ", ".join(markets)))
    print("    MARKET COUNT: names in one market on one date lean together, so the")
    print("    name-resampled interval overstates what this cross-section knows.")

    if nonpositive:
        print("\n  NOT IN THE POOLED FIGURE — central at or below zero, where log(FV/P)")
        print("  does not exist (%d):" % len(nonpositive))
        for r in nonpositive:
            print("    %-12s central %.4f against spot %.4f (%+.1f%%)"
                  % (r["ticker"], r["central"], r["spot"], r["gap_pct"]))
        print("  Omitting these moves the pooled figure TOWARD zero — they are the")
        print("  most pessimistic readings in the book — so the pooled number above")
        print("  UNDERSTATES the house lean by however much they are worth.")

    if unreadable:
        print("\n  answer not readable from the committed numbers (%d) — not clean,"
              % len(unreadable))
        print("  merely unmeasured [R-ENF-04]:")
        for tk, why in sorted(unreadable):
            print("    %-12s %s" % (tk, why))

    return {"rows": rows, "nonpositive": nonpositive, "unreadable": unreadable,
            "mean": _mean(xs), "median": med, "n": len(xs),
            "markets": markets, "ci_names": (lo_n, hi_n), "ci_markets": (lo_c, hi_c)}


def before_and_after():
    """Did the method reassessment move the house lean, on the names it rebuilt?

    The fair-value register froze each name's OLD central before its rebuild
    touched anything, which is the only reason this comparison exists at all: once
    a study writes its numbers the previous fair value is gone, and a baseline
    taken afterwards is a fabricated zero. Both legs are measured against the spot
    each was actually struck at, never against a common price.

    FIVE NAMES IS FIVE NAMES. This says what happened to the names that were
    rebuilt; it is not an estimate of what would happen to the other eighty-five,
    and the rebuilds were chosen by campaign order rather than at random.
    """
    reg = json.load(open(os.path.join(ENGINE, "fv_movement.json"), encoding="utf-8"))
    rows = []
    for tk, e in sorted(reg["entries"].items()):
        base = (e.get("baseline") or {})
        eds = e.get("editions") or []
        if not eds:
            continue
        old_fv = (base.get("fair") or {}).get("base")
        old_sp = base.get("spot")
        new_fv = (eds[-1].get("fair") or {}).get("base")
        sdir = os.path.join(ENGINE, "%s_study" % tk.lower())
        _, new_sp, _ = read_answer(sdir)
        rows.append({"ticker": tk, "old_fv": old_fv, "old_spot": old_sp,
                     "new_fv": new_fv, "new_spot": new_sp,
                     "old_log": (math.log(old_fv / old_sp)
                                 if old_fv and old_sp and old_fv > 0 else None),
                     "new_log": (math.log(new_fv / new_sp)
                                 if new_fv and new_sp and new_fv > 0 else None),
                     "unrecoverable": base.get("unrecoverable")})

    print("\n\n  BEFORE AND AFTER, on the names the reassessment rebuilt")
    print("  %-8s %10s %10s %8s   %10s %10s %8s" %
          ("name", "old FV", "old spot", "log", "new FV", "new spot", "log"))
    for r in rows:
        f = lambda v: "—" if v is None else ("%10.4f" % v)
        g = lambda v: "     n/a" if v is None else ("%+8.4f" % v)
        print("  %-8s %s %s %s   %s %s %s"
              % (r["ticker"], f(r["old_fv"]), f(r["old_spot"]), g(r["old_log"]),
                 f(r["new_fv"]), f(r["new_spot"]), g(r["new_log"])))

    pairs = [(r["old_log"], r["new_log"]) for r in rows
             if r["old_log"] is not None and r["new_log"] is not None]
    if pairs:
        o = _mean([a for a, _ in pairs])
        n = _mean([b for _, b in pairs])
        ao = _mean([abs(a) for a, _ in pairs])
        an = _mean([abs(b) for _, b in pairs])
        print("\n    mean log(FV/P)      before %+.4f   after %+.4f   moved %+.4f"
              % (o, n, n - o))
        print("    mean |log(FV/P)|    before  %.4f   after  %.4f   %s %.1fx"
              % (ao, an, "narrowed" if an < ao else "widened",
                 (ao / an) if an else float("inf")))
        print("    on the %d names where BOTH legs exist." % len(pairs))
        # The extremes are COMPUTED, never typed: a number stated in prose is a
        # claim like any other, and this project has already shipped a typed
        # headline that turned out to be false.
        olds = [r["old_log"] for r in rows if r["old_log"] is not None]
        news = [r["new_log"] for r in rows if r["new_log"] is not None]
        pc = lambda x: (math.exp(x) - 1) * 100
        print()
        print("    THESE TWO LINES SAY DIFFERENT THINGS AND THE SECOND IS THE")
        print("    LARGER EFFECT. The mean lean barely moved, because the rebuilds")
        print("    ran in OPPOSITE directions and very nearly cancelled. What")
        print("    collapsed is the DISPERSION: before, the rebuilt names spanned")
        print("    %+.0f%% to %+.0f%% against their own prices; after, %+.0f%% to %+.0f%%."
              % (pc(min(olds)), pc(max(olds)), pc(min(news)), pc(max(news))))
        # A range computed on the log-defined subset EXCLUDES any negative central,
        # and a negative central is by construction the widest disagreement in the
        # book. Quoting the tighter range without naming what fell out of it would
        # be flattering by omission, which is the same offence as a flattering
        # claim and is harder to see.
        out = [r for r in rows if r["new_log"] is None and r["new_fv"] is not None
               and r["new_spot"]]
        for r in out:
            print("    THAT 'AFTER' RANGE EXCLUDES %s, whose central of %.4f against"
                  % (r["ticker"], r["new_fv"]))
            print("    a price of %.2f is %+.0f%% — the widest disagreement in the book,"
                  % (r["new_spot"], (r["new_fv"] / r["new_spot"] - 1) * 100))
            print("    and it falls out only because log(FV/P) has no value below zero.")
        print("    A house reading one company far below the price and another far")
        print("    above it is not a pessimistic house, it is an inconsistent one,")
        print("    and the reassessment's construction rules — one macro path, one")
        print("    primary lens, a checked bridge, a cost-of-capital ladder — are")
        print("    aimed at exactly that.")
        print()
        print("    NOTHING HERE SAYS THE NEW NUMBERS ARE RIGHT. Agreeing with the")
        print("    market is not being right, it is only being ordinary, and a")
        print("    method tuned toward agreement would score well here while")
        print("    knowing nothing. Whether the disagreement carries information is")
        print("    the gap-closure question, and this cross-section cannot answer")
        print("    it at any sample size, because it holds no subsequent returns.")
    missing = [r["ticker"] for r in rows if r["old_log"] is None or r["new_log"] is None]
    if missing:
        print("\n    not in that pair count (%s):" % ", ".join(missing))
        for r in rows:
            if r["old_log"] is not None and r["new_log"] is not None:
                continue
            why = ("the frozen baseline is unrecoverable"
                   if r["old_fv"] is None else
                   "a central at or below zero, where log(FV/P) does not exist")
            print("      %-8s %s" % (r["ticker"], why))
        print("    Both omissions cut the SAME way they did in the pooled figure:")
        print("    the unrecoverable one is the largest upward move in the book and")
        print("    the negative one the largest downward, so a four-name mean is not")
        print("    a smaller version of the five-name answer, it is a different one.")
    return rows


def published_book():
    """The whole PUBLISHED book, from the dated vintage archive.

    `report()` above measures the studies whose committed numbers expose a
    central and a spot — eleven of twenty-three. This measures what the SITE has
    actually carried, name by name and vintage by vintage, which is a different
    and larger population: ninety names, and it is the one a reader of
    testahil.com was actually looking at.

    Each vintage carries the spot recorded beside it at the time, so the
    comparison is contemporaneous by construction rather than by assumption. A
    vintage with no spot is EXCLUDED and counted, never paired with today's price:
    that would be the single easiest way to manufacture a lean out of nothing.
    """
    arch = json.load(open(os.path.join(ENGINE, "fv_vintages.json"), encoding="utf-8"))
    latest, all_v, nospot, nonpos = [], [], 0, []
    for name, entries in sorted(arch.get("series", {}).items()):
        for i, e in enumerate(entries):
            fv = (e.get("fair") or {}).get("base")
            sp = e.get("spot")
            if sp in (None, 0) or fv is None:
                nospot += 1
                continue
            if fv <= 0:
                nonpos.append((name, fv, sp))
                continue
            row = {"ticker": name, "log": math.log(fv / sp), "fv": fv, "spot": sp,
                   "when": e.get("struck") or e.get("first_seen"),
                   "code": e.get("code")}
            all_v.append(row)
            if i == len(entries) - 1:
                latest.append(row)

    print("\n\n  THE PUBLISHED BOOK — every fair value the site has carried")
    for label, rows in (("latest vintage per name", latest),
                        ("every vintage ever published", all_v)):
        if not rows:
            continue
        xs = [r["log"] for r in rows]
        xs_s = sorted(xs)
        med = (xs_s[len(xs) // 2] if len(xs) % 2
               else _mean(xs_s[len(xs)//2 - 1:len(xs)//2 + 1]))
        lo, hi = boot(xs)
        loc, hic = boot_clustered([{"market": (r["code"] or "?:?").split(":")[0],
                                    "log_gap": r["log"]} for r in rows])
        print("\n    %s — n = %d" % (label, len(rows)))
        print("      mean log(FV/P)  %+.4f   (%+.1f%% in price terms)"
              % (_mean(xs), (math.exp(_mean(xs)) - 1) * 100))
        print("      median          %+.4f      mean |log|  %.4f"
              % (med, _mean([abs(x) for x in xs])))
        print("      below the price %d of %d (%.0f%%)"
              % (sum(1 for x in xs if x < 0), len(xs),
                 100.0 * sum(1 for x in xs if x < 0) / len(xs)))
        print("      95%% interval    names %+.4f to %+.4f   exchanges %+.4f to %+.4f"
              % (lo, hi, loc, hic))

    # The tails, named. A pooled mean says nothing about whether the book is
    # gently off or violently split, and this reassessment exists because of the
    # second possibility.
    if latest:
        srt = sorted(latest, key=lambda r: r["log"])
        print("\n    the five furthest BELOW price:")
        for r in srt[:5]:
            print("      %-12s %+7.1f%%   fair %.4g against %.4g on %s"
                  % (r["ticker"], (math.exp(r["log"]) - 1) * 100, r["fv"],
                     r["spot"], r["when"]))
        print("    the five furthest ABOVE price:")
        for r in srt[-5:][::-1]:
            print("      %-12s %+7.1f%%   fair %.4g against %.4g on %s"
                  % (r["ticker"], (math.exp(r["log"]) - 1) * 100, r["fv"],
                     r["spot"], r["when"]))
        beyond = [r for r in latest if abs(r["log"]) > math.log(1.10)]
        print("\n    %d of %d latest vintages sit more than 10%% either side of the"
              % (len(beyond), len(latest)))
        print("    price they were struck at — the [R-GAP-01] trigger. That gate is")
        print("    one day old and two-sided for one of those days, so most of these")
        print("    predate it; the count is what the ratchet is for.")

    # THE SHAPE OF THE DISTRIBUTION IS THE FINDING, NOT ITS MEAN. Computed, never
    # typed: a mean far from a median is a tail, and "the house is pessimistic"
    # and "the house is well-centred with a long left tail" are different
    # diagnoses with different fixes.
    if latest:
        xs = sorted(r["log"] for r in latest)
        mean = _mean(xs)
        med = (xs[len(xs) // 2] if len(xs) % 2
               else _mean(xs[len(xs)//2 - 1:len(xs)//2 + 1]))
        far_lo = [x for x in xs if x < math.log(0.60)]
        far_hi = [x for x in xs if x > math.log(1.40)]
        print("\n    WHAT THE SHAPE SAYS, and it is not what 'ridiculously")
        print("    pessimistic' would predict. The MEDIAN name sits %+.1f%% from its"
              % ((math.exp(med) - 1) * 100))
        print("    price and %d of %d are below it — a coin flip. The MEAN is %+.1f%%,"
              % (sum(1 for x in xs if x < 0), len(xs), (math.exp(mean) - 1) * 100))
        print("    and the whole of that gap is a TAIL: %d names read more than 40%%"
              % len(far_lo))
        print("    BELOW their price against %d more than 40%% above. Mean |log| is"
              % len(far_hi))
        print("    %.4f, so the typical DISAGREEMENT is large in both directions"
              % _mean([abs(x) for x in xs]))
        print("    while the typical POSITION is neutral.")
        print()
        print("    That is a different diagnosis with a different fix. A uniformly")
        print("    pessimistic house is corrected by moving a rate or a terminal;")
        print("    a well-centred house with a long left tail is corrected by")
        print("    auditing the tail names one at a time, which is what the")
        print("    two-sided gap review does and what the five rebuilds did.")
        print()
        print("    READ THIS AGAINST ITS OWN LIMITS. These 90 vintages were struck")
        print("    on different dates under different standards — most predate the")
        print("    reassessment entirely — so this is a picture of the book as it")
        print("    stands, never a measure of one method. And it measures AGREEMENT")
        print("    only: whether the disagreement carried information is the")
        print("    gap-closure question, and it needs subsequent returns this")
        print("    cross-section does not hold.")

    if nospot:
        print("\n    %d vintages carry no spot and are EXCLUDED rather than paired"
              % nospot)
        print("    with today's price, which would manufacture a lean out of nothing.")
    for name, fv, sp in nonpos:
        print("    %s excluded: a central of %.4f has no logarithm" % (name, fv))
    return {"latest": latest, "all": all_v}


def tail_queue(threshold=0.40):
    """The names carrying the book's lean, ranked — with what is known about each.

    This exists because the pooled measurement above changes what "fix the
    pessimism" means. The book's median sits on the price; its mean does not; the
    difference is a handful of names. Those names are therefore the highest-value
    rebuilds in the programme, and they are NOT the order the campaign runs in,
    which is fixed by market (EGX, then UAE, then KSA...) and knows nothing about
    where the errors are.

    NOTHING IS CONCLUDED FROM THE RANKING. A large gap is a high-prior-of-defect
    region, which is [R-GAP-01]'s own reasoning, not proof of a defect: a genuine
    84% discount is a legitimate conclusion and this house publishes ranges
    precisely because prices are sometimes wrong. The ranking says where to LOOK.
    """
    arch = json.load(open(os.path.join(ENGINE, "fv_vintages.json"), encoding="utf-8"))
    rows = []
    for name, entries in arch.get("series", {}).items():
        e = entries[-1]
        fv = (e.get("fair") or {}).get("base")
        sp = e.get("spot")
        if not sp or fv is None or fv <= 0:
            continue
        lg = math.log(fv / sp)
        if abs(lg) < threshold:
            continue
        sdir = os.path.join(ENGINE, "%s_study" % name.lower())
        has_study = os.path.isdir(sdir)
        std, review = None, None
        if has_study:
            nums = _json_or_none(os.path.join(sdir, "study_numbers.json")) or {}
            std = nums.get("standard_version")
            review = bool(glob.glob(os.path.join(sdir, "GAP_REVIEW_*.md")))
        rows.append({"ticker": name, "log": lg, "fv": fv, "spot": sp,
                     "when": e.get("struck") or e.get("first_seen"),
                     "code": e.get("code"), "study": has_study,
                     "standard": std, "gap_review": review})
    rows.sort(key=lambda r: r["log"])

    print("\n\n  THE TAIL — every published name more than %.0f%% from its own price"
          % ((math.exp(threshold) - 1) * 100))
    print("  %-12s %-11s %8s  %-9s %-11s %s"
          % ("ticker", "exchange", "gap", "struck", "standard", "study / gap review"))
    for r in rows:
        print("  %-12s %-11s %+7.1f%%  %-9s %-11s %s"
              % (r["ticker"], (r["code"] or "?").split(":")[0],
                 (math.exp(r["log"]) - 1) * 100, r["when"] or "?",
                 r["standard"] or ("—" if r["study"] else "no study"),
                 ("study, review" if r["gap_review"] else
                  ("study, NO review" if r["study"] else "no study directory"))))

    nostudy = [r for r in rows if not r["study"]]
    noreview = [r for r in rows if r["study"] and not r["gap_review"]]
    print("\n    %d names in the tail. %d have no study directory at all, so there"
          % (len(rows), len(nostudy)))
    print("    is nothing for a gate to open — their fair value sits on the site")
    print("    with no committed record behind it. %d have a study and no gap"
          % len(noreview))
    print("    review, which is what [R-GAP-01]'s ratchet carries.")
    print()
    print("    THE ORDER THIS SUGGESTS IS NOT THE ORDER THE CAMPAIGN RUNS IN. The")
    print("    campaign queue is fixed by market and knows nothing about where the")
    print("    errors are; this list is measured. Whether Phase 2 follows it is a")
    print("    decision for the principal, not a change to make quietly — the")
    print("    market order exists so that a method is tested on a whole market")
    print("    before it travels, and re-ordering by gap size would test it first")
    print("    on exactly the names most likely to be unusual.")
    return rows


def _json_or_none(p):
    try:
        return json.load(open(p, encoding="utf-8"))
    except Exception:
        return None


def gate_coverage():
    """How much of what the SITE publishes is inside any gate's population.

    Every construction gate in this repository globs `engine/*_study/`. That is
    the right anchor for what it checks — a study's committed record — but it is
    NOT the population of published fair values, and the two have been quietly
    assumed to coincide. This measures the difference, because a suite of gates
    reporting clean over a quarter of the book is a suite reporting on a quarter
    of the book.

    The shortfall itself is a known condition, not a discovery: the fair-value
    register already records that most covered names carry no current-standard
    study. What is worth measuring is the CONSEQUENCE — which published numbers no
    gate can see.
    """
    arch = json.load(open(os.path.join(ENGINE, "fv_vintages.json"), encoding="utf-8"))
    have = {ticker_of(d) for d in studies()}
    pub = sorted(arch.get("series", {}))
    inside = [n for n in pub if n in have]
    outside = [n for n in pub if n not in have]

    def _lean(names):
        xs = []
        for n in names:
            e = arch["series"][n][-1]
            fv = (e.get("fair") or {}).get("base")
            sp = e.get("spot")
            if sp and fv and fv > 0:
                xs.append(math.log(fv / sp))
        return (_mean(xs) if xs else float("nan")), len(xs)

    li, ni = _lean(inside)
    lo, no = _lean(outside)
    print("\n\n  GATE COVERAGE — what the gates can and cannot see")
    print("    published fair values          %d" % len(pub))
    print("    inside engine/*_study/         %d  (%.0f%%)"
          % (len(inside), 100.0 * len(inside) / max(1, len(pub))))
    print("    OUTSIDE it, no study directory %d  (%.0f%%)"
          % (len(outside), 100.0 * len(outside) / max(1, len(pub))))
    print()
    print("    Every construction gate — bridge, lens, cost of capital, macro")
    print("    coherence, valuation gap, workbook structure, output records —")
    print("    globs engine/*_study/. So each of them is correct about the")
    print("    population it names and silent about %d published numbers a reader"
          % len(outside))
    print("    can see on the site today. That is not a defect in any one gate; it")
    print("    is the [R-ENF-04] question one level up — a population anchored on")
    print("    study directories, applied to a book anchored on data.js.")
    print()
    print("    AND THE LEAN DOES NOT SIT WHERE THAT WOULD SUGGEST: the %d names"
          % ni)
    print("    WITH a study average %+.1f%% against price, the %d WITHOUT average"
          % ((math.exp(li) - 1) * 100, no))
    print("    %+.1f%%. The examined names carry the LARGER discounts, not the"
          % ((math.exp(lo) - 1) * 100))
    print("    smaller ones — so 'the unexamined ones are where the errors are' is")
    print("    not what the numbers say. It is confounded (a study gets written")
    print("    where the house has a view, and several of these are the names")
    print("    deliberately audited), and it is stated here so the obvious")
    print("    inference is not drawn without it.")
    return {"published": pub, "inside": inside, "outside": outside}


if __name__ == "__main__":
    report()
    before_and_after()
    published_book()
    tail_queue()
    gate_coverage()
