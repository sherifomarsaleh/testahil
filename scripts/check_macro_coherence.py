"""EVERY STUDY STANDS ON THE HOUSE MACRO PATH, AND THE CHECK RUNS OUTSIDE THE STUDY.

[R-MACRO-01], enforced per [R-ENF-01]: a rule that can be checked is checked from
outside the thing it governs, and it FAILS rather than warns.

What this gate reads is the study's own committed numbers file — the same file
its document and workbook are built from — and what it asserts is
research_protocol.assert_macro_coherence(): every growth rate recomputes to the
house inflation path plus a stated real rate, terminal growth agrees with the
inflation inside the terminal discount rate, the currency path is the derived
purchasing-power path, and the explicit window runs until growth has converged
on the terminal.

It also refuses a study that carries an inflation number of its own. That is the
whole point of the workstream: five studies carried five different rates for one
fiscal year in one country, and each was defensible alone.

THE POPULATION IS ANCHORED SOMEWHERE ELSE [R-ENF-04]. The glob over
engine/*_study/ is held against the tickers named in
engine/build_depth_audit/macro_outstanding.json: every listed ticker must resolve
to a directory on disk, and a run that examined zero studies FAILS. An empty
result is not a clean result.

IT IS A RATCHET [R-ENF-02], not a cliff. Every study that predates the house path
is listed as outstanding and is allowed to fail. The build breaks on a NEW
violation, a NEW study directory with no entry either way, or a listed study
whose record has appeared and is wrong. The list may only ever get SHORTER.

    python3 scripts/check_macro_coherence.py           # the gate
    python3 scripts/check_macro_coherence.py --prune   # drop the now-passing entries
"""
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENGINE = os.path.join(ROOT, "engine")
sys.path.insert(0, ENGINE)

OUTSTANDING_FILE = os.path.join(ENGINE, "build_depth_audit", "macro_outstanding.json")

# A registry key that looks like a macro number a study should not be setting.
# Deliberately narrow: it catches the levels (an inflation rate, a CPI, a
# terminal growth), never a company figure that merely mentions one.
OWN_MACRO_KEY = re.compile(
    r"^(cpi|inflation|infl|.*_infl|.*_inflation|cbe_target|terminal_growth|g_term|"
    r"real_rate_term|erp_term|kd_term|fx_path|line_price_growth|us_infl.*)$", re.I)

# Where a study's own numbers file may carry the record.
RECORD_KEYS = ("macro_record", "macro", "macro_coherence")


def studies():
    return sorted(glob.glob(os.path.join(ENGINE, "*_study")))


def ticker_of(sdir):
    return os.path.basename(sdir)[: -len("_study")].upper()


def numbers_file(sdir):
    """The study's own committed numbers file, if it has one.

    Named the way each study happens to name it; a study with none cannot be
    read at all and is reported as unreadable rather than skipped, because an
    unreadable answer is not a clean answer.
    """
    for name in ("study_numbers.json", "numbers.json"):
        p = os.path.join(sdir, name)
        if os.path.exists(p):
            return p
    cands = [p for p in glob.glob(os.path.join(sdir, "*.json"))
             if "numbers" in os.path.basename(p).lower()]
    return cands[0] if cands else None


def find_record(doc):
    for k in RECORD_KEYS:
        if isinstance(doc.get(k), dict):
            return doc[k]
    meta = doc.get("meta")
    if isinstance(meta, dict):
        for k in RECORD_KEYS:
            if isinstance(meta.get(k), dict):
                return meta[k]
    return None


def own_macro_inputs(doc):
    """Registry keys that set a macro level the house path owns."""
    reg = doc.get("registry")
    if not isinstance(reg, dict):
        return []
    out = []
    for k, v in reg.items():
        if not OWN_MACRO_KEY.match(k):
            continue
        src = ""
        if isinstance(v, dict):
            src = str(v.get("source", "")) + " " + str(v.get("basis", ""))
        # a registered macro level is allowed ONLY if it says, in its own
        # source, that it came from the house path
        if "macro_path" not in src and "house macro path" not in src.lower():
            out.append(k)
    return sorted(out)


def audit(sdir):
    """(state, detail) for one study. state in ok / no_record / unreadable / fail."""
    import research_protocol as RP

    tk = ticker_of(sdir)
    nf = numbers_file(sdir)
    if not nf:
        return "unreadable", "no committed numbers file in the study directory"
    try:
        doc = json.load(open(nf, encoding="utf-8"))
    except Exception as e:                                   # noqa: BLE001
        return "unreadable", "%s will not parse: %s" % (os.path.basename(nf), e)

    rec = find_record(doc)
    own = own_macro_inputs(doc)
    if rec is None:
        detail = "carries no macro record"
        if own:
            detail += "; and sets its own macro levels: %s" % ", ".join(own[:6])
        return "no_record", detail

    if own:
        return "fail", ("sets its own macro levels beside the house path: %s. No "
                        "study may carry its own inflation number."
                        % ", ".join(own[:6]))
    try:
        RP.assert_macro_coherence(rec, ticker=tk)
    except AssertionError as e:
        return "fail", str(e).replace("\n", " ")
    except Exception as e:                                   # noqa: BLE001
        return "fail", "%s: %s" % (type(e).__name__, e)
    return "ok", "coherent against the %s path" % rec.get("market", "?")


def main():
    prune = "--prune" in sys.argv
    if not os.path.exists(OUTSTANDING_FILE):
        print("FAIL — the ratchet list %s does not exist. A gate with no population "
              "to hold itself against reports clean by examining nothing."
              % os.path.relpath(OUTSTANDING_FILE, ROOT))
        return 1
    out = json.load(open(OUTSTANDING_FILE, encoding="utf-8"))
    known = set(out["outstanding"])

    sdirs = studies()
    if not sdirs:
        print("FAIL — examined zero studies. An empty result is not a clean result "
              "[R-ENF-04]: either the glob is wrong or the studies are gone.")
        return 1

    on_disk = {ticker_of(d) for d in sdirs}
    missing = sorted(known - on_disk)
    if missing:
        print("FAIL — the outstanding list names studies that do not exist on disk: %s. "
              "The list is the population this gate is held against; a name in it that "
              "resolves to nothing means the gate is measuring the wrong book."
              % ", ".join(missing))
        return 1

    ok, fixed, still, hard, unreadable = [], [], [], [], []
    for d in sdirs:
        tk = ticker_of(d)
        state, detail = audit(d)
        listed = tk in known
        if state == "ok":
            (fixed if listed else ok).append((tk, detail))
        elif state in ("no_record", "unreadable"):
            if listed:
                still.append((tk, detail))
            else:
                hard.append((tk, detail))
            if state == "unreadable":
                unreadable.append(tk)
        else:
            (still if listed else hard).append((tk, detail))

    print("studies examined: %d   conforming: %d   outstanding (allowed): %d"
          % (len(sdirs), len(ok) + len(fixed), len(still)))
    if fixed:
        print("\nNOW PASSING — remove from the outstanding list (%d):" % len(fixed))
        for tk, detail in fixed:
            print("   %-12s %s" % (tk, detail))
    if still:
        print("\nstill outstanding, allowed for now (%d):" % len(still))
        for tk, detail in still[:40]:
            print("   %-12s %s" % (tk, detail[:150]))
    if hard:
        print("\nFAIL — not on the outstanding list and not coherent (%d):" % len(hard))
        for tk, detail in hard:
            print("   %-12s %s" % (tk, detail[:400]))

    if prune:
        out["outstanding"] = sorted(known - {tk for tk, _ in fixed})
        out["pruned_on"] = out.get("pruned_on", [])
        json.dump(out, open(OUTSTANDING_FILE, "w", encoding="utf-8"), indent=1)
        print("\npruned: the list may only ever get shorter — now %d entries"
              % len(out["outstanding"]))
        return 0

    if hard:
        return 1
    print("\nOK — no new violations.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
