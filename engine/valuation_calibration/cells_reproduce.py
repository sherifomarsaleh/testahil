"""Can a run's committed per-cell file reproduce the skill numbers it publishes?

WHY THIS IS THE TEST. [R-FCAL-01] requires skill against BOTH naive benchmarks at
every horizon, and every run computes it on the cells the model and the benchmark
BOTH resolve -- correct, and invisible from outside unless the file records both
sides. Three of the five runs committed a per-cell dump that recorded only the
MODEL's projection, wrote `projected: null` for every freeze and trend cell, and
SILENTLY SKIPPED any benchmark cell the log score could not take. A file like that
looks complete, is read as the run's evidence, and cannot rebuild a single one of
the numbers it sits beside.

WHAT IT DOES NOT DO. It does not re-derive the science, re-run a projection, or
second-guess a skill definition; it reads the committed cells, applies the run's
OWN published definition, and asks whether the answer comes back. A reproducer
that reimplemented the model would be testing something else [R-ENF-03].

TOLERANCE IS THE PUBLISHED ROUNDING, NEVER CHOSEN: runs round their skill to four
decimals, so the bar is half a unit in the last published place. A first cut used
1e-9 and reported twenty-two of EGCH's twenty-eight numbers as mismatches with the
sample size agreeing EXACTLY -- which is the signature of a wrong probe and not a
wrong run, and it was read as one for about a minute.

AN EMPTY RESULT IS NOT A CLEAN RESULT [R-ENF-04]. That same first cut looked for a
`drivers` key in every run's scores file; ARCC calls it `detail.skill`, so the probe
found nothing to compare and printed "0 reproduce, 0 do not" -- a run that was never
examined, reported in the words of a run that passed. Every run's reader is named
here, a run whose scores expose no skill number at all is REPORTED, and a pass with
zero comparisons REFUSES.

Read live: python3 engine/valuation_calibration/cells_reproduce.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ENG = os.path.dirname(HERE)

# (ticker, directory, the setting the MODEL's cells carry, {published key: cell setting})
RUNS = [
    ("AMOC", "amoc_walkforward", "asknown", {"skill_vs_freeze": "freeze",
                                             "skill_vs_trend": "trend"}),
    ("ARCC", "arcc_walkforward", "asknown", {"vs_freeze": "freeze",
                                             "vs_trend": "trend",
                                             "skill_freeze": "freeze",
                                             "skill_trend": "trend"}),
    ("EGCH", "egch_walkforward", "asknown", {"skill_vs_freeze": "freeze",
                                             "skill_vs_trend": "trend"}),
    ("TMGH", "tmgh_walkforward", "asknown", {"skill_freeze": "freeze",
                                             "skill_trend": "trend"}),
    ("PHDC", "phdc_walkforward", "as_known", {"skill_freeze": "freeze",
                                              "skill_trend": "trend"}),
]

TOL = 5e-5          # half a unit in the fourth decimal, the place runs publish to

# KNOWINGLY OUTSTANDING, WITH THE MEASUREMENT RATHER THAN A SHRUG [R-ENF-02].
# A run listed here is allowed to disagree; a run NOT listed is not, and the list
# may only ever shorten. The reason is required and is the diagnosis owed, not an
# excuse — an entry that cannot say what was measured is a silence with a filename.
OUTSTANDING = {
    # EMPTY, AND THE ENTRY THAT WAS HERE CAME OFF THE SAME DAY IT WENT ON.
    # TMGH was listed 07-09-2026 rebuilding 33 of its 148 published skill numbers,
    # with the direction of the defect deliberately NOT asserted because equal
    # counts over different sets is arithmetically possible and naming a culprit
    # before tracing the pairing is the assertion this instrument exists to catch.
    # Traced the same day: its skill divided the model's mean absolute error over
    # ITS OWN cells by the benchmark's over ITS OWN, and reported n as min() of the
    # two counts — a number belonging to neither sample. The cells were never the
    # wrong half. Corrected in that run's score.py to pair on shared cells, the
    # construction its four siblings already use; 115 of 148 figures moved, HIGHER
    # in 69 and LOWER in 46, median 0.0818, and by_driver, by_era and macro_split
    # came back byte-identical, so only the skill numbers were ever affected.
}


def load_cells(d):
    """{setting: {(origin, horizon, driver): row}} from a run's committed file.

    Two shapes are read AS THEY ARE rather than renamed: a flat list carrying a
    `setting` field, and a dict keyed by setting whose rows name their fields
    differently. Renaming one to look like the other is how a reader stops
    matching what the run actually wrote.
    """
    raw = json.load(open(os.path.join(ENG, d, "error_cells.json"), encoding="utf-8"))
    out = {}
    if isinstance(raw, list):
        for r in raw:
            out.setdefault(r["setting"], {})[
                (r["origin"], r["horizon"], r["driver"])] = r.get("log_error")
    else:
        for setting, rows in raw.items():
            for r in rows:
                out.setdefault(setting, {})[
                    (r["origin"], r["h"], r["field"])] = r.get("e")
    return out


def published_skill(d):
    """{(driver, horizon or None): {published_key: {"n": .., "skill": ..}}}.

    FOUR SHAPES, READ AS THEY ARE. Two runs publish skill per driver, two per
    driver PER HORIZON, and one nests it under `detail`. A first cut knew only the
    first shape and reported the other runs as exposing no skill number — which is
    a statement about the reader, printed in the words of a statement about the
    run.
    """
    sc = json.load(open(os.path.join(ENG, d, "scores.json"), encoding="utf-8"))
    src = sc.get("drivers")
    if src is None and isinstance(sc.get("detail"), dict):
        src = sc["detail"].get("skill")
    out = {}
    if isinstance(src, dict):
        for k, v in src.items():
            # BOTH fields required: a published skill with no sample size cannot
            # be held to one, and checking only the value would report a match on
            # a number computed over a different set of cells.
            got = {kk: vv for kk, vv in v.items()
                   if isinstance(vv, dict) and "skill" in vv and "n" in vv}
            if got:
                out[(k, None)] = got
    bh = sc.get("by_horizon")
    if isinstance(bh, dict):
        for driver, per_h in bh.items():
            if not isinstance(per_h, dict):
                continue
            for h, block in per_h.items():
                if not isinstance(block, dict):
                    continue
                got = {kk: vv for kk, vv in block.items()
                       if isinstance(vv, dict) and "skill" in vv and "n" in vv}
                if got:
                    out[(driver, int(h))] = got
    return out


def check(name, d, model_setting, benches):
    cells = load_cells(d)
    pub = published_skill(d)
    M = cells.get(model_setting, {})
    if not M:
        return name, 0, 0, "no %s cells in the committed file" % model_setting
    if not pub:
        return name, 0, 0, "scores file exposes no skill number this reader can find"
    ok = bad = 0
    misses = []
    for (driver, horizon), entry in pub.items():
        for key, setting in benches.items():
            got = entry.get(key)
            if not isinstance(got, dict) or got.get("skill") is None:
                continue
            B = cells.get(setting, {})
            shared = [k for k in M
                      if k[2] == driver and M[k] is not None
                      and (horizon is None or k[1] == horizon)
                      and B.get(k) is not None]
            if not shared:
                continue
            m = sum(abs(M[k]) for k in shared) / len(shared)
            b = sum(abs(B[k]) for k in shared) / len(shared)
            if not b:
                continue
            s = 1.0 - m / b
            good = len(shared) == got["n"] and abs(s - got["skill"]) <= TOL
            ok += good
            bad += not good
            if not good:
                misses.append("%s%s %s: file n=%d s=%.4f vs published n=%d s=%.4f"
                              % (driver, "" if horizon is None else " h%d" % horizon,
                                 key, len(shared), s, got["n"], got["skill"]))
    return name, ok, bad, misses


def main():
    print("can each run's committed cells rebuild the skill it publishes?\n")
    total_ok = total_bad = examined = 0
    outstanding_hit = set()
    for name, d, ms, benches in RUNS:
        if not os.path.exists(os.path.join(ENG, d, "error_cells.json")):
            print("  %-6s NO per-cell file — reported, never skipped [R-ENF-04]" % name)
            continue
        nm, ok, bad, misses = check(name, d, ms, benches)
        examined += 1
        total_ok += ok
        total_bad += bad
        if isinstance(misses, str):
            print("  %-6s NOT COMPARABLE — %s" % (nm, misses))
            continue
        held = nm in OUTSTANDING and bad
        print("  %-6s %3d reproduce, %3d do not%s"
              % (nm, ok, bad, "   OUTSTANDING — allowed to disagree" if held else ""))
        for m in misses[:6]:
            print("           %s" % m)
        if held:
            total_bad -= bad
            outstanding_hit.add(nm)
    print("\n  %d runs examined, %d skill numbers reproduce, %d do not"
          % (examined, total_ok, total_bad))
    if not examined or not total_ok:
        print("\nREFUSED — a run that compared nothing is not a run that agreed "
              "[R-ENF-04].")
        return 1
    stale = sorted(set(OUTSTANDING) - outstanding_hit)
    if stale:
        print("\nFAIL — listed as outstanding and no longer disagreeing: %s. A "
              "ratchet may only SHORTEN, so remove the entry in the commit that "
              "fixes it [R-ENF-02]." % ", ".join(stale))
        return 1
    if total_bad:
        print("\nFAIL — a per-cell file that cannot rebuild its own published skill "
              "is not the evidence it is read as.")
        return 1
    for nm in sorted(outstanding_hit):
        print("\n  OUTSTANDING %s — %s" % (nm, OUTSTANDING[nm]))
    if outstanding_hit:
        print("\nOK — every published skill number rebuilds from the cells committed "
              "beside it, EXCEPT on the run(s) named above, whose disagreement is "
              "held with its measurement rather than reported as agreement.")
    else:
        print("\nOK — every published skill number rebuilds from the cells committed "
              "beside it.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
