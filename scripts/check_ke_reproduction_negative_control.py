#!/usr/bin/env python3
"""Negative control for [R-COC-02]. A check nobody has seen fail is not evidence.

EVERY MUTATION ASSERTS THAT IT LANDED. THE CASE COUNT IS ASSERTED AGAINST A CONSTANT.
NOTHING IS WRITTEN INTO THE REAL TREE.

THE CLEAN HALF IS WHAT THIS GATE TURNS ON, and it is drawn from the two constructions the
book actually runs rather than from cases invented to be easy: ARCC's relevered terminal
EXACTLY as it stands, declared, must stay GREEN, because the first draft of this check
condemned it and the answer to a check firing on work that is right is to re-point it
[R-COC-01]. So must ADNOCLS's plain same_beta terminal, and a record with no terminal at
all, which is not this test's subject.

THE PRINCIPAL'S OWN ERROR IS CASE ONE: a cost of equity typed 300 basis points high. It
passed every check in this repository until today.
"""
from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ENGINE = os.path.join(ROOT, "engine")
for p in (ENGINE, ROOT):
    if p not in sys.path:
        sys.path.insert(0, p)

import ke_reproduction as kr                 # noqa: E402

DECLARED_CASES = 14

# ARCC's record, the fields this gate reads, exactly as committed.
ARCC = {
    "rf_star": 0.1955, "beta": 0.9275220650537075, "erp": 0.0941,
    "ke_exp": 0.28277982632155385,
    "rf_terminal": 0.125, "erp_terminal": 0.07,
    "ke_terminal": 0.20021378024369318,
    "weight_equity": 0.9621629210350936, "weight_debt": 0.03783707896490645,
    "weight_debt_terminal": 0.2,
}
# ADNOCLS's shape: a plain same_beta terminal on a pegged market.
PLAIN = {
    "rf_star": 0.0424, "beta": 0.6, "erp": 0.0866,
    "ke_exp": 0.0424 + 0.6 * 0.0866,
    "rf_terminal": 0.042, "erp_terminal": 0.0858,
    "ke_terminal": 0.042 + 0.6 * 0.0858,
    "weight_equity": 0.9, "weight_debt": 0.1, "weight_debt_terminal": 0.1,
}


def d(base, **kw):
    r = dict(base)
    for k, v in kw.items():
        if v is None:
            r.pop(k, None)
        else:
            r[k] = v
    return r


CASES = []
def case(name, rec, expect_fail, injected):
    CASES.append((name, rec, expect_fail, injected))


# ---- RED --------------------------------------------------------------
case("THE PRINCIPAL'S ERROR — Ke typed 300bp high",
     d(ARCC, ke_exp=ARCC["ke_exp"] + 0.03, ke_terminal_construction="relevered",
       relevering_tax_rate=0.225),
     True, lambda r: abs(r["ke_exp"] - ARCC["ke_exp"] - 0.03) < 1e-12)

case("a beta quietly raised, Ke left as it was",
     d(ARCC, beta=1.3, ke_terminal_construction="relevered", relevering_tax_rate=0.225),
     True, lambda r: r["beta"] == 1.3)

case("an ERP quietly raised",
     d(ARCC, erp=0.14, ke_terminal_construction="relevered", relevering_tax_rate=0.225),
     True, lambda r: r["erp"] == 0.14)

case("ARCC's relevered terminal, UNDECLARED as it ships today",
     d(ARCC), True, lambda r: "ke_terminal_construction" not in r)

case("ADNOCLS's plain terminal, UNDECLARED",
     d(PLAIN), True, lambda r: "ke_terminal_construction" not in r)

case("declared same_beta on a terminal that was actually relevered",
     d(ARCC, ke_terminal_construction="same_beta"),
     True, lambda r: r["ke_terminal_construction"] == "same_beta")

case("declared relevered at the WRONG tax rate",
     d(ARCC, ke_terminal_construction="relevered", relevering_tax_rate=0.30),
     True, lambda r: r["relevering_tax_rate"] == 0.30)

case("declared relevered with NO tax rate — solved out of the answer",
     d(ARCC, ke_terminal_construction="relevered"),
     True, lambda r: "relevering_tax_rate" not in r)

case("a construction off the closed list",
     d(ARCC, ke_terminal_construction="our terminal is different"),
     True, lambda r: r["ke_terminal_construction"] not in kr.TERMINAL_CONSTRUCTIONS)

case("FERTIGLOBE's shape — a record with no rf_star, beta, erp or ke_exp",
     {"ke_terminal": 0.19, "note": "a record that cannot support the identity"},
     True, lambda r: "rf_star" not in r)

case("no record at all", None, True, lambda r: r is None)

# ---- CLEAN ------------------------------------------------------------
case("ARCC's relevered terminal, DECLARED — must stay green",
     d(ARCC, ke_terminal_construction="relevered", relevering_tax_rate=0.225),
     False, lambda r: r["relevering_tax_rate"] == 0.225)

case("a plain same_beta terminal, DECLARED",
     d(PLAIN, ke_terminal_construction="same_beta"),
     False, lambda r: r["ke_terminal_construction"] == "same_beta")

case("a record with an explicit Ke and NO terminal — not this test's subject",
     {"rf_star": 0.1955, "beta": 0.9275220650537075, "erp": 0.0941,
      "ke_exp": 0.28277982632155385},
     False, lambda r: "ke_terminal" not in r)


def main():
    print("[R-COC-02] negative control — every mutation asserts it landed\n")
    assert len(CASES) == DECLARED_CASES, (
        "case count moved: %d present, %d declared. A control that quietly loses cases "
        "reports fewer-of-fewer and reads as clean." % (len(CASES), DECLARED_CASES))
    bad = 0
    for name, rec, expect, injected in CASES:
        if not injected(rec):
            print("  FIXTURE  %-52s MUTATION DID NOT LAND" % name)
            bad += 1
            continue
        fails = kr.check(rec)
        got = len(fails) > 0
        ok = (got == expect)
        print("  %-6s [%s] %-52s %s"
              % ("ok" if ok else "WRONG", "RED" if expect else "CLEAN", name,
                 (fails[0][:66] if fails else "reproduces")))
        if not ok:
            bad += 1
    print("\n%d case(s): %d red-expected, %d clean-expected"
          % (len(CASES), sum(1 for c in CASES if c[2]),
             sum(1 for c in CASES if not c[2])))
    if bad:
        print("FAIL — %d case(s) did not behave as declared." % bad)
        return 1
    print("OK — fires on every injected defect and on none of the clean cases.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
