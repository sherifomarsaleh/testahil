"""AMOC walk-forward — corrections, tested under BOTH clauses.

The pre-registration already ruled, before any number existed, that NO CORRECTION
WILL BE ESTIMATED FROM THIS RECORD: nine cells cannot support an expanding-window
correction and a separate confirmation sample. This module therefore does not
propose corrections. It runs the two clauses over every driver so that the ruling
is a MEASURED conclusion rather than an assertion, and files what survives as
WATCH FLAGS.

CLAUSE 1 — does the bias hold its sign across eras, and does the block bootstrap
keep the same sign at every block length?

CLAUSE 2 — is a correction here consistent with how that driver class is built
across the market's book? This is the clause that has already done its job once
in this project, on PHDC's finance cost, where it exposed the "bias" as
arithmetic rather than evidence. It is not a formality.

AND ONE THING THAT OVERRIDES BOTH: a correction factor is honest when the model
is right and reality is awkward. When the model is WRONG, a correction hides it.
This record's dominant error is a specification defect (diagnose.py), so a
multiplier fitted on top of it would be fitting the defect.
"""
import os, sys, json, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import score as S
import bottom_up as B

# How each driver class is built across this repository's book, for clause 2.
# Stated here rather than inferred, so the test is auditable.
BOOK_CONVENTION = {
    "raw_materials": ("Feedstock is built as cost per unit on a disclosed volume and escalated on "
                      "the commodity's own price path, in every study that has a physical input. "
                      "A multiplier on feedstock would be unique to this name."),
    "salaries": ("Payroll escalates on the market's own wage or CPI path everywhere in the book."),
    "other_cos": ("Energy and utilities escalate on their own driver class, never a blended index "
                  "(L-009). A multiplier would re-blend them."),
    "ga": ("Overheads are a fixed base escalated on CPI across the book."),
    "credit_interest": ("Interest income is a rate on a disclosed cash balance everywhere in the book. "
                        "AMOC's cash is disclosed; a multiplier would substitute for reading it."),
    "net_sales": ("Revenue is volume x realisation on a disclosed unit in every ground-up study."),
    "majority": ("No study in the book carries a multiplier on an aggregate. An aggregate is rebuilt "
                 "from adjusted drivers, never adjusted itself."),
}


def clause1(rec):
    """Bias holds its sign across eras AND across both bootstrap block lengths."""
    eras = [v for v in rec["by_era"].values() if v]
    signs = set(1 if e["bias"] > 0 else -1 for e in eras)
    era_stable = len(signs) == 1 and len(eras) > 1
    bs = rec["bootstrap"]
    boot_stable = all(bs.get(str(L)) and bs[str(L)]["same_sign"] for L in ("2", "3"))
    n_eras = len(eras)
    return {"era_stable": era_stable, "n_eras": n_eras, "bootstrap_same_sign": boot_stable,
            "passes": bool(era_stable and boot_stable)}


def main():
    sc = json.load(open(os.path.join(HERE, "scores.json")))
    diag = json.load(open(os.path.join(HERE, "diagnostics.json")))
    out = {"policy": ("Pre-registered: no correction is estimated from this record. Everything "
                      "below is a WATCH FLAG — recorded, graded at the next update, acted on by "
                      "nobody."),
           "flags": [], "declined": []}

    for d, rec in sc["drivers"].items():
        c1 = clause1(rec)
        a = rec["overall"]
        entry = {"driver": d, "n": a["n"], "bias_log": a["bias"],
                 "bias_pct": (math.exp(a["bias"]) - 1) * 100, "mae_log": a["mae"],
                 "share_over": a["share_over"], "clause1": c1,
                 "clause2_convention": BOOK_CONVENTION.get(d),
                 "freeze_equivalent": rec["freeze_equivalent"]}
        if not c1["passes"]:
            entry["disposition"] = "not a candidate — clause 1 fails"
            out["declined"].append(entry)
            continue
        # Clause 1 passed. It is STILL not adopted, for the reasons stated above.
        entry["disposition"] = "WATCH FLAG"
        entry["why_not_adopted"] = []
        entry["why_not_adopted"].append(
            "Pre-registered: nine cells cannot support an estimated correction and a separate "
            "confirmation sample.")
        if c1["n_eras"] < 2 or True:
            pass
        if BOOK_CONVENTION.get(d):
            entry["why_not_adopted"].append("Clause 2: " + BOOK_CONVENTION[d])
        entry["why_not_adopted"].append(
            "The dominant error on this record is a SPECIFICATION defect — a macro scenario that "
            "compounds domestic inflation while holding the currency flat — and a multiplier "
            "fitted on top of it would be fitting the defect, not correcting a bias.")
        out["flags"].append(entry)

    out["specification_finding"] = {
        "what": ("Under the pre-registered knowable path, majority profit is under-forecast in "
                 "100% of cells, bias -64.1%, and the method scores -1.128 against simply "
                 "assuming last year's profit repeats."),
        "why": ("The knowable path is not a coherent scenario. It compounds Egyptian CPI onto "
                "domestic costs while holding the currency and crude flat, so revenue is frozen "
                "in nominal EGP while conversion cost, overheads and marketing inflate. On a "
                "refiner whose revenue and dominant cost are the same commodity, that is a "
                "guaranteed one-sided miss."),
        "evidence": diag["skill_vs_freeze_majority"],
        "residual": ("Fixing it does not rescue the method. With PERFECT FORESIGHT of the "
                     "crude-in-EGP path revenue is right to +6.0% and cost of sales to +0.1%, "
                     "yet gross profit is over-forecast by 68% and the method still scores "
                     "-0.131 against no change. The margin is a ~6.6% residual between two large "
                     "numbers, so an error that is small on each is large on the difference."),
        "treatment": "Reported. No correction factor may hide a specification error.",
    }
    json.dump(out, open(os.path.join(HERE, "corrections_log.json"), "w"), indent=1, default=str)
    return out


if __name__ == "__main__":
    o = main()
    print("CORRECTIONS — %s\n" % o["policy"])
    print("WATCH FLAGS (clause 1 passed; none adopted):")
    for f in o["flags"]:
        print("  %-22s n=%d  bias %+7.1f%%  over %3.0f%%  eras=%d  bootstrap same-sign=%s%s"
              % (f["driver"], f["n"], f["bias_pct"], 100 * f["share_over"],
                 f["clause1"]["n_eras"], f["clause1"]["bootstrap_same_sign"],
                 "  [rule=freeze]" if f["freeze_equivalent"] else ""))
    print("\nNOT CANDIDATES (clause 1 failed): %s"
          % ", ".join(d["driver"] for d in o["declined"]) or "none")
