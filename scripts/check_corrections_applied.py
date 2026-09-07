"""Every correction a STUDY claims reconciles to the walk-forward that produced it.

NAMED IN THE PROGRAMME'S OWN ACCEPTANCE CRITERIA AND NEVER BUILT. Part E criterion
1 lists seven gates that must be green with negative controls; six are, and this
one did not exist — while criterion 2 requires in terms that "every claimed
correction reconciles to its log". An acceptance criterion naming a check nobody
wrote cannot be met, and nothing was counting it: [R-ENF-01]'s own failure applied
to the definition of done rather than to a study.

WHAT IT HOLDS. A study that claims a correction must name a walk-forward run that
ADOPTED it, on the same driver, at a factor reproducing from that run's OWN
committed bias at the strength [R-FCAL-01] fixes — half, by default, so the factor
is exp(-bias/2). A study claiming NO correction must say so explicitly rather than
be silent, because silence and "none adopted" are the same file to a reader and
different facts about the work.

MATCHED ON MEANING, NOT ON A SUBSTRING, and that clause was earned in the first
five minutes: a search for the word found SCEM carrying `corrections_applied: 69`,
which is a count of EDITORIAL corrections inside a revision note on a study with no
walk-forward run at all. A gate keying on the word would have opened with a
spectacular false positive about a study that has done nothing wrong.

Read live: python3 scripts/check_corrections_applied.py
"""
import glob
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ENG = os.path.join(ROOT, "engine")

HALF = 0.5          # [R-FCAL-01]: corrections at HALF STRENGTH by default
TOL = 5e-4          # the factors are published to four decimals

# Ratchet [R-ENF-02]: a run whose study is knowingly silent. EMPTY at adoption
# of the silence clause -- the one study that was silent (PHDC) was CONFORMED
# rather than listed, because its generator was to hand, reproduces its own
# output byte for byte, and the declaration moves no valued figure.
SILENT_OK = set()


def _numbers(d):
    p = os.path.join(d, "study_numbers.json")
    if not os.path.exists(p):
        return None
    try:
        return json.load(open(p, encoding="utf-8"))
    except Exception:
        return "unparseable"


def _find(obj, key):
    """Every value stored under `key`, at any depth."""
    out = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == key:
                out.append(v)
            out.extend(_find(v, key))
    elif isinstance(obj, list):
        for v in obj:
            out.extend(_find(v, key))
    return out


def claims(nums):
    """(adopted_claims, declared_none) — a study's own statement about corrections.

    Keyed on the fields a study uses to make the CLAIM, never on the word appearing
    somewhere in the file.
    """
    adopted = []
    for v in _find(nums, "adopted_correction"):
        if isinstance(v, dict) and v.get("driver"):
            adopted.append((str(v["driver"]), v.get("factor")))
    for v in _find(nums, "adopted_corrections"):
        if isinstance(v, list):
            for e in v:
                if isinstance(e, dict) and e.get("driver"):
                    adopted.append((str(e["driver"]), e.get("factor")))
                elif isinstance(e, str):
                    adopted.append((e, None))
    declared_none = any(v == 0 for v in _find(nums, "corrections_adopted")) or \
        any(isinstance(v, list) and not v for v in _find(nums, "adopted_corrections"))
    return adopted, declared_none


def _adopt_arcc(rec):
    return {str(c.get("driver")): c.get("bias")
            for c in rec.get("candidates", [])
            if str(c.get("disposition", "")).upper() == "ADOPTED"}


def _adopt_listed(rec):
    """EGCH and TMGH both keep a top-level `adopted` list. Empty on both today."""
    out = {}
    for e in rec.get("adopted", []) or []:
        if isinstance(e, dict) and e.get("driver"):
            out[str(e["driver"])] = e.get("bias")
        elif isinstance(e, str):
            out[e] = None
    return out


def _adopt_amoc(rec):
    """Pre-registered as estimating NO correction from this record: `policy` says so
    in terms and everything under `flags` is a watch flag. An empty adoption set is
    a legitimate state, and it is returned because the record SAYS so rather than
    because a key was missing."""
    assert "policy" in rec or "flags" in rec, "AMOC's record no longer has its shape"
    return {}


def _adopt_phdc(rec):
    """The per-origin `log` records half-strength shifts the expanding-window rule
    APPLIED inside the test — six of them, at the 2023 and 2024 origins — and NONE
    was promoted into the live drivers.

    APPLIED AND ADOPTED ARE TWO DIFFERENT QUANTITIES and this adapter answers the
    second. scripts/check_correction_boundary.py deliberately reads the WIDER one,
    because a sign-stability claim is what that gate tests; naming both readers here
    is cheaper than one reader that silently answers the other gate's question."""
    assert "log" in rec, "PHDC's record no longer has its shape"
    return {}


# ONE NAMED ADAPTER PER RUN. The five records have five shapes — candidates /
# adopted / policy+flags / log / adopted+watch_flags — and the reader this replaced
# looked for two of them and returned an EMPTY DICT for the other three. It happened
# to be right on all five today, and on two of them BY NOT FINDING A KEY rather than
# by reading one, which is an absent answer wearing a clean answer's clothes
# [R-ENF-04]: the day a run promotes a correction in the `log` shape, that reader
# reports the run adopted nothing and either refuses a study that correctly claims it
# or passes one that failed to. The precedent is check_correction_boundary.py, which
# had to learn the same thing after a census reported "twelve candidates, one
# adopted" while missing four applied corrections in another run.
ADAPTERS = {
    "ARCC": _adopt_arcc,
    "EGCH": _adopt_listed,
    "TMGH": _adopt_listed,
    "AMOC": _adopt_amoc,
    "PHDC": _adopt_phdc,
}


class UnknownRecordShape(Exception):
    pass


def run_adoptions(ticker):
    """{driver: bias} the run itself records as ADOPTED, or None if there is no run.

    Raises UnknownRecordShape for a run this file has no adapter for — a new run is
    REPORTED rather than read as having adopted nothing."""
    d = os.path.join(ENG, "%s_walkforward" % ticker.lower())
    p = os.path.join(d, "corrections_log.json")
    if not os.path.exists(p):
        return None
    rec = json.load(open(p, encoding="utf-8"))
    fn = ADAPTERS.get(ticker.upper())
    if fn is None:
        raise UnknownRecordShape(ticker)
    return fn(rec)


def has_run(ticker):
    return os.path.isdir(os.path.join(ENG, "%s_walkforward" % ticker.lower()))


# The study's driver name and the run's need not be the same string — a study
# writes for a reader. Named rather than fuzzy-matched: a wrong pairing reconciles
# the wrong correction and reports it clean.
ALIAS = {("ARCC", "manufacturing depreciation"): "mfg_dep"}


def main():
    print("does every claimed correction reconcile to the run that produced it?\n")
    studies = sorted(glob.glob(os.path.join(ENG, "*_study")))
    examined = claimed = 0
    failures = []
    for sd in studies:
        tk = os.path.basename(sd).replace("_study", "").upper()
        nums = _numbers(sd)
        if nums is None:
            continue
        if nums == "unparseable":
            failures.append("%s: numbers file will not parse — unreadable is not "
                            "clean [R-ENF-04]" % tk)
            print("  %-12s numbers file will not parse" % tk)
            continue
        examined += 1
        adopted, declared_none = claims(nums)
        if not adopted and not declared_none:
            # SILENCE IS NOT A DECLARATION, and this file's own opening paragraph has
            # said so since it was written while the code skipped past it — a comment
            # asserting a check that does not exist, which is worse than no comment
            # because it stops the next reader looking. A study with NO walk-forward
            # correctly says nothing and must not fire; a study WITH one owes the
            # reader the difference between "we looked and promoted nothing" and
            # "nobody asked".
            if has_run(tk) and tk not in SILENT_OK:
                failures.append("%s: has a walk-forward run and its numbers file says "
                                "nothing about corrections either way. Silence and "
                                "'none adopted' are the same file to a reader and "
                                "different facts about the work." % tk)
                print("  %-12s SILENT — a run behind it and no statement either way" % tk)
            continue
        try:
            runs = run_adoptions(tk)
        except UnknownRecordShape:
            failures.append("%s: its corrections record matches no named adapter, so "
                            "nothing can be read from it. A new record shape is "
                            "REPORTED, never read as having adopted nothing "
                            "[R-ENF-04]." % tk)
            print("  %-12s UNKNOWN RECORD SHAPE — no named adapter" % tk)
            continue
        if not adopted:
            extra = ""
            if runs:
                extra = ("   [the run adopted %s — the study says none]"
                         % ", ".join(sorted(runs)))
                failures.append("%s: declares no correction while its run adopted %s"
                                % (tk, ", ".join(sorted(runs))))
            print("  %-12s declares NO correction adopted%s" % (tk, extra))
            continue
        for drv, factor in adopted:
            claimed += 1
            if runs is None:
                failures.append("%s: claims a correction on %r with no walk-forward "
                                "run to reconcile against" % (tk, drv))
                print("  %-12s %-26s NO RUN" % (tk, drv))
                continue
            key = ALIAS.get((tk, drv), drv)
            if key not in runs:
                failures.append("%s: claims %r, which its run did not adopt (adopted: "
                                "%s)" % (tk, drv, ", ".join(sorted(runs)) or "nothing"))
                print("  %-12s %-26s NOT ADOPTED BY THE RUN" % (tk, drv))
                continue
            bias = runs[key]
            if factor is None or bias is None:
                failures.append("%s: %r carries no factor or the run carries no bias, "
                                "so nothing can be reconciled" % (tk, drv))
                print("  %-12s %-26s NOTHING TO RECONCILE" % (tk, drv))
                continue
            want = math.exp(-HALF * float(bias))
            ok = abs(float(factor) - want) <= TOL
            if not ok:
                failures.append("%s: %r claims %.4f, the run's own bias %.6f at half "
                                "strength gives %.4f" % (tk, drv, factor, bias, want))
            print("  %-12s %-26s %s  claimed %.4f, exp(-bias/2) %.4f"
                  % (tk, drv, "reconciles" if ok else "DOES NOT RECONCILE",
                     factor, want))

    print("\n  %d study numbers file(s) read, %d claimed correction(s)"
          % (examined, claimed))
    if not examined:
        print("\nREFUSED — a run that read no study is not a run that found nothing "
              "[R-ENF-04].")
        return 1
    if failures:
        for f in failures:
            print("    %s" % f)
        print("\nFAIL — a correction a study claims must reconcile to the run that "
              "produced it.")
        return 1
    print("\nOK — every claimed correction names a run that adopted it and reproduces "
          "from that run's own bias at half strength.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
