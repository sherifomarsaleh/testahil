#!/usr/bin/env python3
"""[R-PROOF-01] — every error this house claims to catch is PLANTED and caught.

WHY A CATALOGUE RATHER THAN A CLAIM. Sixty-eight gates is a number, not evidence. The
question anybody sensible asks — a principal, an investor, a reader — is not "how many
checks do you have" but "if this specific thing went wrong, would you find out". That
question has an answer only if somebody makes the specific thing go wrong.

HOW IT DIFFERS FROM THE GAUNTLET AND FROM A NEGATIVE CONTROL, because all three plant a
defect and they are not the same instrument. check_new_study_gauntlet asks whether a NEW
STUDY can walk past the set — a property of the SYSTEM. A negative control asks whether ONE
GATE fires on its own condition — a property of that gate, and it lives beside it. This
asks whether a NAMED REAL-WORLD ERROR, described in the words somebody would use to
complain about it, is caught by anything at all.

THE CATALOGUE IS THE SPECIFICATION AND THE HARNESS IS THE PROOF. An error in the catalogue
that no gate catches is RED. So adding an error somebody has thought of is how the
specification grows, and the build stays red until something catches it — which is the
opposite of a wish list.

THREE STEPS PER CASE, AND THE FIRST IS THE ONE THAT MAKES IT EVIDENCE:
  1. the gate is GREEN on the unmutated sandbox — so a red afterwards was caused by the
     error and not by something already broken
  2. the mutation is applied and ASSERTED TO HAVE LANDED — this project has four times
     caught a control passing a fixture that never injected its condition, reporting green
     and proving only that nothing had changed
  3. the gate goes RED and NAMES its subject

NOTHING IS WRITTEN INTO THE REAL TREE [R-ENF-01]. The repository is copied once; every
mutation and every restore happens inside the copy, so there is no undo that has to run.
"""
from __future__ import annotations

import argparse
import copy
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


# ---------------------------------------------------------------- the catalogue

def _numbers_path(repo, tk):
    return os.path.join(repo, "engine", "%s_study" % tk.lower(), "study_numbers.json")


def _load(repo, tk):
    return json.load(open(_numbers_path(repo, tk), encoding="utf-8"))


def _save(repo, tk, doc):
    json.dump(doc, open(_numbers_path(repo, tk), "w", encoding="utf-8"),
              indent=1, ensure_ascii=False)


def _find_parent(doc, key):
    """The dict that holds `key`, so a mutation lands where the reader will look."""
    if isinstance(doc, dict):
        if key in doc:
            return doc
        for v in doc.values():
            r = _find_parent(v, key)
            if r is not None:
                return r
    elif isinstance(doc, list):
        for v in doc:
            r = _find_parent(v, key)
            if r is not None:
                return r
    return None


# Each case: the error in the words somebody would complain in; the study it is planted
# in; the gate that should catch it; the mutation; and the assertion that it landed.
CATALOGUE = []


def case(key, complaint, ticker, gate, mutate, landed, files=None):
    CATALOGUE.append({"key": key, "complaint": complaint, "ticker": ticker,
                      "gate": gate, "mutate": mutate, "landed": landed,
                      "files": files or []})


# 1 — the principal's second error, in their own words
def _m_landbank(repo, tk):
    doc = _load(repo, tk)
    holder = _find_parent(doc, "meta") or doc
    meta = holder.get("meta") if isinstance(holder.get("meta"), dict) else doc
    meta["information_set_ends"] = "1Q2026"
    meta["class"] = "real-estate developer, off-plan, percentage-of-completion"
    meta["asset_base_record"] = {
        "quantity": "land bank", "unit": "mn sqm", "value": 33.0,
        "as_at": "2024-12-31",
        "disclosure": "FY2024 earnings release",
    }
    _save(repo, tk, doc)


def _l_landbank(repo, tk):
    doc = _load(repo, tk)
    r = _find_parent(doc, "asset_base_record")
    return bool(r) and r["asset_base_record"]["as_at"] == "2024-12-31"


# PLANTED IN A STUDY THAT IS NOT ON THE ASSET-BASE RATCHET, and the reason is the
# harness's own first finding rather than a convenience. The first draft planted it in
# PHDC — the study the rule was adopted on — and the gate did NOT go red, because a
# RATCHET EXCUSES THE WHOLE GATE FOR THAT NAME rather than the specific failure it
# recorded. So a NEW error of a ratcheted class, in a ratcheted study, is invisible.
# That is true of every ratchet in this repository and it is recorded as a finding of
# its own; here the case is planted where it tests what it claims to test.
case("landbank-stale",
     "the study takes the current landbank of a developer but does not account for "
     "new land added to it",
     "SAVOLA", "check_asset_base.py", _m_landbank, _l_landbank)


# 2 — the principal's third error
def _m_ke(repo, tk):
    doc = _load(repo, tk)
    holder = _find_parent(doc, "cost_of_capital_record")
    rec = holder["cost_of_capital_record"]
    rec["ke_exp"] = rec["ke_exp"] + 0.03
    rec["ke_terminal_construction"] = "same_beta"
    _save(repo, tk, doc)


def _l_ke(repo, tk):
    rec = _find_parent(_load(repo, tk), "cost_of_capital_record")["cost_of_capital_record"]
    return abs(rec["ke_exp"] - (rec["rf_star"] + rec["beta"] * rec["erp"]) - 0.03) < 1e-9


case("ke-inflated-300bp",
     "the study creates a wrong or inflated cost of equity",
     "ADNOCLS", "check_ke_reproduction.py", _m_ke, _l_ke)


# 3 — the principal's first error, on the page a reader actually sees
def _m_published(repo, tk):
    """Slash the PUBLISHED fair value to 40% of the published spot.

    READS THROUGH THE SANCTIONED PARSER, NEVER BY REGEX. check_site_data_reader forbids a
    regular-expression read of assets/data.js and is right to: a regex over a JavaScript
    object literal returns the FIRST match where the parser takes the LAST, which is how a
    ticker page once published a support above its own close while every checker reported
    it clean. This gate caught THIS FILE doing exactly that, on the run after it was
    written [R-ENF-03].

    So the figures come from engine/site_data.py. The WRITE still has to locate text — a
    parser cannot serialise a JavaScript object literal back — and it is made safe the only
    honest way available: the value written is read back THROUGH THE PARSER before the case
    is allowed to count, so a write that landed in the wrong entry fails as a mutation that
    did not land rather than passing as a defect that was not caught.
    """
    sys.path.insert(0, os.path.join(repo, "engine"))
    for m in list(sys.modules):
        if m == "site_data":
            del sys.modules[m]
    import site_data                                    # the sanctioned reader
    js = os.path.join(repo, "assets", "data.js")
    tickers = site_data.read_object("TICKERS", path=js)
    if tk not in tickers:
        raise RuntimeError("no entry for %s in data.js" % tk)
    spot = tickers[tk]["spot"]
    base = tickers[tk]["fair"]["base"]
    new = round(float(spot) * 0.40, 4)

    src = open(js, encoding="utf-8").read()
    # Anchored on the ticker's own entry, then on the FIRST fair.base inside it. The
    # parser above already told us what that value is, so the anchor is checked against a
    # known figure rather than trusted.
    off = src.index("\n  %s: {" % tk)
    blk_end = src.index("\n  },", off)
    block = src[off:blk_end]
    needle = "base: %s" % (("%g" % base) if float(base) != int(float(base))
                           else "%d" % int(float(base)))
    if needle not in block:
        needle = [t for t in block.split() if t.startswith("base:")]
        raise RuntimeError("could not anchor on %s's published base of %s (saw %r)"
                           % (tk, base, needle[:1]))
    src2 = src[:off] + block.replace(needle, "base: %s" % new, 1) + src[blk_end:]
    open(js, "w", encoding="utf-8").write(src2)


def _l_published(repo, tk):
    """Read the mutation back THROUGH THE PARSER — the same route a page takes."""
    sys.path.insert(0, os.path.join(repo, "engine"))
    for m in list(sys.modules):
        if m == "site_data":
            del sys.modules[m]
    import site_data
    t = site_data.read_object("TICKERS",
                              path=os.path.join(repo, "assets", "data.js"))[tk]
    return (t["fair"]["base"] / t["spot"] - 1.0) < -0.55


case("fv-60pct-of-price",
     "the study publishes an erroneous fair value at 60% of the current price, "
     "in a wrong way",
     "SABIC", "check_published_gap.py", _m_published, _l_published)


# ---- the errors this house has ALREADY SHIPPED ONCE ------------------------------
# Every standing rule here was adopted on a real defect that reached a delivered study.
# Turning each founding defect into a planted case is what keeps the rule from quietly
# stopping working: a gate nobody has seen fire on the thing it was built for is a gate
# running on trust. Each is planted in a study NOT on that gate's ratchet, per [R-ENF-08].

def _m_kd_below_sovereign(repo, tk):
    """[R-COC-01]'s hard refusal: a same-currency corporate cannot borrow below its own
    sovereign. AMOC shipped a Kd 31bp under the government that taxes it."""
    doc = _load(repo, tk)
    rec = _find_parent(doc, "cost_of_capital_record")["cost_of_capital_record"]
    rec["kd_pretax"] = round(rec["rf_observed"] - 0.02, 6)
    rec["kd_aftertax"] = round(rec["kd_pretax"] * 0.775, 6)
    _save(repo, tk, doc)


def _l_kd_below_sovereign(repo, tk):
    rec = _find_parent(_load(repo, tk), "cost_of_capital_record")["cost_of_capital_record"]
    return rec["kd_pretax"] < rec["rf_observed"]


case("kd-below-its-own-sovereign",
     "the study borrows more cheaply than the government that taxes it",
     "ARCC", "check_cost_of_capital.py",
     _m_kd_below_sovereign, _l_kd_below_sovereign)


def _m_inflation_off_path(repo, tk):
    """[R-MACRO-01]: five studies carried five inflation rates for the same fiscal year in
    the same country. A study may not carry an inflation number of its own."""
    doc = _load(repo, tk)
    holder = _find_parent(doc, "macro_record")
    rec = holder["macro_record"]
    lad = rec.get("inflation_inputs")
    if isinstance(lad, list) and lad:
        for item in lad:
            if isinstance(item, dict):
                for k, v in list(item.items()):
                    if isinstance(v, list) and v and all(
                            isinstance(x, (int, float)) for x in v):
                        item[k] = [round(float(x) * 0.55, 4) for x in v]
                    elif isinstance(v, (int, float)) and 0 < v < 1:
                        item[k] = round(float(v) * 0.55, 4)
    rec["_injected_off_path"] = True
    _save(repo, tk, doc)


def _l_inflation_off_path(repo, tk):
    rec = _find_parent(_load(repo, tk), "macro_record")["macro_record"]
    return rec.get("_injected_off_path") is True


case("inflation-off-the-house-path",
     "the study values the company in an economy the study beside it does not recognise",
     "ARCC", "check_macro_coherence.py",
     _m_inflation_off_path, _l_inflation_off_path)


# ---------------------------------------------------------------- the harness

def sandbox():
    tmp = tempfile.mkdtemp(prefix="injection_")
    def ignore(d, names):
        # raw_indices, raw_ohlc and panels are COPIED: the gauntlet learned that excluding
        # a directory a gate needs makes it crash and go red for the WRONG reason, which
        # reads exactly like going red for the right one.
        return [n for n in names if n in (".git", "__pycache__", "node_modules",
                                          "filings")]
    repo = os.path.join(tmp, "repo")
    shutil.copytree(ROOT, repo, ignore=ignore, symlinks=True)
    return tmp, repo


def run(repo, gate, timeout=900):
    r = subprocess.run([sys.executable, os.path.join("scripts", gate)], cwd=repo,
                       capture_output=True, text=True, timeout=timeout)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def snapshot(repo, c):
    """Everything a case will touch, so it can be put back inside the sandbox."""
    paths = [_numbers_path(repo, c["ticker"]), os.path.join(repo, "assets", "data.js")]
    return {p: open(p, "rb").read() for p in paths if os.path.exists(p)}


def restore(snap):
    for p, b in snap.items():
        open(p, "wb").write(b)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default=None)
    ap.add_argument("--keep", action="store_true", help="leave the sandbox for inspection")
    a = ap.parse_args(argv)

    cases = [c for c in CATALOGUE if not a.only or c["key"] == a.only]
    if not cases:
        print("FAIL — no cases to run [R-ENF-04]. An empty catalogue is not a clean one.")
        return 1

    tmp, repo = sandbox()
    print("[R-PROOF-01] planting %d named error(s) in real studies\n" % len(cases))
    bad = 0
    try:
        for c in cases:
            snap = snapshot(repo, c)
            # 1 — baseline green, so a red afterwards is CAUSED by the error
            rc0, out0 = run(repo, c["gate"])
            base_ok = (rc0 == 0)
            # 2 — plant it, and prove it landed
            try:
                c["mutate"](repo, c["ticker"])
                landed = bool(c["landed"](repo, c["ticker"]))
            except Exception as e:
                landed, out1, rc1 = False, "mutation raised: %s" % e, None
            # 3 — the gate must now be red AND name its subject
            if landed:
                rc1, out1 = run(repo, c["gate"])
                caught = (rc1 != 0) and (c["ticker"] in out1)
            else:
                caught = False
            restore(snap)

            verdict = ("CAUGHT" if (base_ok and landed and caught) else "NOT CAUGHT")
            if verdict != "CAUGHT":
                bad += 1
            print("  %-10s %s" % (verdict, c["complaint"]))
            print("             planted in %-10s  gate %s" % (c["ticker"], c["gate"]))
            print("             baseline green: %-5s   mutation landed: %-5s   "
                  "gate went red naming it: %s"
                  % (base_ok, landed, caught if landed else "n/a"))
            if verdict != "CAUGHT":
                why = ("the gate was ALREADY red before the error was planted, so this "
                       "case proves nothing" if not base_ok else
                       "THE MUTATION DID NOT LAND — the fixture never injected its "
                       "condition" if not landed else
                       "NOTHING CAUGHT IT. This is the finding: the catalogue names an "
                       "error the framework does not detect.")
                print("             -> %s" % why)
            print()
    finally:
        if a.keep:
            print("  sandbox kept at %s" % repo)
        else:
            shutil.rmtree(tmp, ignore_errors=True)

    print("%d case(s): %d caught, %d not" % (len(cases), len(cases) - bad, bad))
    if bad:
        print("\nFAIL — a catalogued error the framework does not catch is the "
              "specification failing, not the harness.")
        return 1
    print("\nOK — every named error was planted in a real study and caught by name.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
