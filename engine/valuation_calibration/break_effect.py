"""The break-effect cut, read from every run's own per-cell error file.

The reassessment's founding premise was a single house lean of about -45% on the
level drivers. Split by the era of the ORIGIN rather than pooled, on three names,
that lean sat almost entirely on the origins whose forecast window spans Egypt's
devaluations. This runs the same cut over every run that commits per-cell errors,
so the claim is held against five names rather than three, and so a run that
stops committing them FAILS rather than being skipped [R-ENF-04].

TWO THINGS THIS DELIBERATELY DOES NOT DO, both learned by getting them wrong on
the first draft of this file:

 1. It does not compare POOLED LEVELS ACROSS NAMES. Each run scores its own
    driver list, and the intersection is not the same mix from one name to the
    next -- PHDC contributes a single revenue line where TMGH contributes six
    drivers including two balance-sheet items. A pooled mean over different
    mixes is a number about the mixes. What is comparable is the WITHIN-NAME
    difference between eras, which holds the mix fixed by construction, and the
    per-family cut below, which holds it fixed by selection.

 2. It does not decide which origins are break origins by typing a year range.
    Each run declares the era of every origin in its own pre-registration and
    writes it into every cell; those labels are read. A typed range would have
    called AMOC's FY2023 and FY2024 origins normal when that run's own record
    calls them devaluation years.

Read live: python3 engine/valuation_calibration/break_effect.py
"""
import os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
ENG = os.path.dirname(HERE)

# (directory, driver key, horizon key, error key, setting key, as-known value,
#  target-year key)
RUNS = {
    "ARCC": ("arcc_walkforward", "driver", "horizon", "log_error", "setting", "asknown", "year"),
    "AMOC": ("amoc_walkforward", "driver", "horizon", "log_error", "setting", "asknown", "year"),
    "EGCH": ("egch_walkforward", "driver", "horizon", "log_error", "setting", "asknown", "year"),
    "TMGH": ("tmgh_walkforward", "driver", "horizon", "log_error", "setting", "asknown", "year"),
    # PHDC writes the same information under different key names and nests its
    # rows by setting. It is read in its own shape rather than renamed, because
    # renaming a delivered artefact to satisfy a reader is the offence this
    # repository names elsewhere.
    "PHDC": ("phdc_walkforward", "field", "h", "e", "setting", "as_known", "target"),
}

# Driver families, so the cross-name column is like-for-like. A name's own driver
# vocabulary differs; these are the lines that mean the same thing.
FAMILY = {
    "revenue": {"revenue", "net_sales", "total_revenue", "sales", "new_sales"},
    "cost": {"cost_of_sales", "cos", "opex"},
    "profit": {"net_profit", "npat", "net", "majority", "pbt"},
}
LEVEL = set().union(*FAMILY.values()) | {"gross_profit", "operating_profit", "ebit",
                                         "ppe", "da"}


# The fiscal years Egypt devalued in. A fact about the calendar, not a label,
# so it applies the same way to every name whatever each run's own era vocabulary.
DEVAL_YEARS = {2022, 2023, 2024, 2025}


def is_break(era):
    """ORIGIN-side cut. A run's own label decides -- every run in this book names
    the devaluation era in words, and none of them names it by year. This asks
    WHAT THE ANALYST KNEW at the origin."""
    return "devaluation" in str(era).lower()


def _year(v):
    if isinstance(v, int):
        return v
    digits = "".join(c for c in str(v) if c.isdigit())
    return int(digits[-4:]) if len(digits) >= 4 else None


def hit_break(target):
    """TARGET-side cut. Asks whether the year BEING FORECAST was a devaluation
    year. This is a different question from is_break() and the two disagree --
    an FY2020 origin forecasting to FY2025 knew nothing of the devaluation and
    was hit by all of it. Both are reported; neither is a correction of the
    other."""
    y = _year(target)
    return (y in DEVAL_YEARS) if y is not None else None


def load(name):
    d, dk, hk, ek, sk, sv, yk = RUNS[name]
    path = os.path.join(ENG, d, "error_cells.json")
    if not os.path.exists(path):
        return None, "no per-cell file at %s/error_cells.json" % d
    raw = json.load(open(path))
    rows = []
    if isinstance(raw, dict):
        for setting, lst in raw.items():
            if setting == sv:
                rows.extend(lst)
    else:
        rows = [r for r in raw if r.get(sk) == sv]
    out = []
    for r in rows:
        e = r.get(ek)
        drv = str(r.get(dk, ""))
        if e is None or drv not in LEVEL:
            continue
        out.append({"driver": drv, "h": r.get(hk), "e": float(e),
                    "era": r.get("era"), "break": is_break(r.get("era")),
                    "target": _year(r.get(yk)), "hit": hit_break(r.get(yk))})
    if not out:
        return None, "file present but no scoreable level cells"
    return out, None


def mean(v):
    return sum(v) / len(v) if v else None


def cut(cells, key="break"):
    brk = [c["e"] for c in cells if c[key]]
    rest = [c["e"] for c in cells if c[key] is False]
    return {"n": len(cells), "pooled": mean([c["e"] for c in cells]),
            "n_break": len(brk), "break": mean(brk),
            "n_rest": len(rest), "rest": mean(rest),
            "effect": (mean(brk) - mean(rest)) if (brk and rest) else None}


def main():
    res, missing = {}, []
    for name in sorted(RUNS):
        cells, why = load(name)
        if cells is None:
            missing.append((name, why))
            continue
        res[name] = {"all": cut(cells), "hit": cut(cells, "hit"),
                     "hit_family": {f: cut([c for c in cells if c["driver"] in members], "hit")
                                    for f, members in FAMILY.items()
                                    if any(c["driver"] in members for c in cells)},
                     "drivers": sorted(set(c["driver"] for c in cells)),
                     "eras": sorted(set(str(c["era"]) for c in cells)),
                     "family": {f: cut([c for c in cells if c["driver"] in members])
                                for f, members in FAMILY.items()
                                if any(c["driver"] in members for c in cells)}}

    # [R-ENF-04] both ways: directories present with nothing readable is a run
    # that was not read, not a run that found nothing.
    on_disk = [n for n in RUNS if os.path.isdir(os.path.join(ENG, RUNS[n][0]))]
    if not on_disk:
        raise SystemExit("FAIL: no walk-forward directories on disk")
    if not res:
        raise SystemExit("FAIL: %d run directories present, none readable" % len(on_disk))

    def line(n, label, r):
        return ("%-6s %-8s %5d %8s %5d %8s %5d %8s %8s" %
                (n, label, r["n"],
                 "%.3f" % r["pooled"] if r["pooled"] is not None else "-",
                 r["n_break"], "%.3f" % r["break"] if r["break"] is not None else "-",
                 r["n_rest"], "%.3f" % r["rest"] if r["rest"] is not None else "-",
                 "%.3f" % r["effect"] if r["effect"] is not None else "-"))

    print("Break-effect cut -- as-known setting, mean log error, era from each run's own labels")
    print("The EFFECT column is the comparable one: it holds the driver mix fixed within a name.")
    print("The pooled/break/rest levels are NOT comparable across names -- different mixes.\n")
    print("%-6s %-8s %5s %8s %5s %8s %5s %8s %8s" %
          ("name", "family", "n", "pooled", "n_brk", "break", "n_rst", "rest", "effect"))
    for n in sorted(res):
        print(line(n, "all", res[n]["all"]))
        for f in ("revenue", "cost", "profit"):
            if f in res[n]["family"]:
                print(line("", f, res[n]["family"][f]))

    print()
    print("TARGET-side cut -- the year being forecast, %s" % sorted(DEVAL_YEARS))
    print("%-6s %-8s %5s %8s %5s %8s %5s %8s %8s" %
          ("name", "family", "n", "pooled", "n_hit", "hit", "n_rst", "rest", "effect"))
    for n in sorted(res):
        print(line(n, "all", res[n]["hit"]))
        for f in ("revenue", "cost", "profit"):
            if f in res[n]["hit_family"]:
                print(line("", f, res[n]["hit_family"][f]))
    # Does the effect COMPOUND with the horizon? A rate error should; a level
    # shock should not. Cut inside the devaluation years only, so the question is
    # about the effect rather than about which years each horizon reaches.
    print()
    print("Horizon shape INSIDE the devaluation years -- mean log error by h")
    hs = sorted({c["h"] for n in res for c in (load(n)[0] or []) if c["h"] is not None})
    print("%-6s %s" % ("name", " ".join("%8s" % ("h=%s" % h) for h in hs)))
    for n in sorted(res):
        cells = load(n)[0] or []
        row = []
        for h in hs:
            v = [c["e"] for c in cells if c["h"] == h and c["hit"]]
            row.append("%8s" % ("%.3f" % mean(v) if v else "-"))
        print("%-6s %s" % (n, " ".join(row)))

    for n, why in missing:
        print("%-6s NOT READ -- %s" % (n, why))
    print()
    for n in sorted(res):
        r = res[n]["all"]
        if r["n_rest"] == 0 or r["n_break"] == 0:
            print("%s: one side of the cut is empty -- no contrast, not a null result." % n)
        print("%-6s eras: %s" % (n, "; ".join(res[n]["eras"])))
    return res


if __name__ == "__main__":
    main()
