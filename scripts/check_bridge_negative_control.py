"""A CHECK NOBODY HAS SEEN FAIL IS NOT EVIDENCE.

Reinjects, into a throwaway copy of the study directories, every condition
scripts/check_bridge.py claims to catch, and asserts the gate goes RED on each.
Three CLEAN cases must NOT fire.

Every failure case is a defect this repository actually shipped:

  1. STALE SHEET — the bridge on 31-Dec-2025 while a reviewed 31-Mar-2026 sheet
     sat on the company's own archive (PHDC, 30-Aug-2026 edition).
  2. NO REGISTER — a study that cannot establish what the latest disclosed sheet
     even is. An unestablished answer is not a clean one.
  3. MINORITY AT BOOK — CLHO deducted book and overstated parent equity by about
     a third of the minority.
  4. MINORITY NOT DEDUCTED — PHDC deducted nothing while dividing by parent
     shares.
  5. MINORITY OFF ENTERPRISE VALUE — an equity share applied to an enterprise
     number, handing the minority a share of growth assets it does not own.
  6. CASH CHARGED TWICE — net-debt weights in the rate AND the cash added at
     face in the bridge (AMOC, before its 01-Sep-2026 correction).
  7. A BRIDGE THAT DOES NOT FOOT — the lines do not sum to the stated equity.
  8. PER-SHARE THAT DOES NOT DIVIDE.
  9. A DIVIDEND DECLARED BEFORE THE SHEET DATE, deducted again.
 10. NO RECORD, NOT LISTED — a new study with no bridge record and no ratchet entry.
 11. EMPTY POPULATION — no studies, and a list naming one that does not exist.

THE DECLARATION HALF [13-09-2026, R-BRIDGE-01 CLAUSE FIVE]. A study that values on
equity directly owes no bridge and must SAY so, and the whole weight of that rests on
the declaration being unfakeable. So every way out is reinjected here: a declaration
silent on the claim itself, one that asserts something else, one that drops the
register, one on a stale sheet, one naming no lenses, one whose primary lens is not
among them, one whose per-share does not divide, one that divides to a figure the study
does not publish, four that declare no enterprise value while the study's own committed
numbers state one, and a study that commits BOTH a bridge and a declaration that it
builds none. Two clean cases hold the other side: a complete declaration, and one whose
numbers file says IN PROSE that it computes no weighted cost of capital — prose about
the absence is evidence FOR the declaration and must not fire, which is ADIB's own
no_wacc_reason and would have refused the very study the clause was written for.

    python3 scripts/check_bridge_negative_control.py
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# THIS FIXTURE SUPPLIES ITS OWN POPULATION [06-09-2026]. The gate resolves the
# book through engine/study_population.py; this control runs it against a
# sandboxed tree holding studies it planted, which is the point of the control.
# The escape is explicit and the gate PRINTS that it took it, so a fixture
# population can never be mistaken for the real one.
_FIXTURE_ENV = dict(os.environ, TESTAHIL_FIXTURE_POPULATION='1')

GATE = os.path.join("scripts", "check_bridge.py")

GOOD = {
    "market": "EG",
    "balance_sheet_date": "2026-06-30",
    "latest_disclosed_date": "2026-06-30",
    "latest_disclosed_source": "the interim statements registered in the study's own sweep",
    "lines": [
        {"label": "Enterprise value", "value": 100000.0},
        {"label": "plus cash", "value": 20000.0},
        {"label": "less borrowings", "value": -30000.0},
        {"label": "less minority interests at their share of value", "value": -10000.0},
    ],
    "nci": {"basis": "value_share", "deduction": 10000.0, "applied_to": "equity_value",
            "proxy_source": "the minority's filed share of profit after tax",
            "book": 8000.0, "profit_share": 0.125, "proportional": 0.10},
    "cash": {"treatment": "added_at_face", "weights_basis": "gross"},
    "associates": {"basis": "book", "listed": False},
    "dividend": {"deducted": False},
    "equity_value": 80000.0,
    "shares_mn": 1000.0,
    "per_share": 80.0,
}


def sandbox():
    tmp = tempfile.mkdtemp(prefix="bridge_nc_")
    os.makedirs(os.path.join(tmp, "engine", "build_depth_audit"))
    os.makedirs(os.path.join(tmp, "scripts"))
    for f in ("research_protocol.py", "macro_path.py"):
        shutil.copy(os.path.join(ROOT, "engine", f), os.path.join(tmp, "engine", f))
    shutil.copytree(os.path.join(ROOT, "engine", "macro_paths"),
                    os.path.join(tmp, "engine", "macro_paths"))
    shutil.copy(os.path.join(ROOT, "scripts", "check_bridge.py"),
                os.path.join(tmp, "scripts", "check_bridge.py"))
    return tmp


def put_study(tmp, ticker, record, raw=None, declaration=None, extra=None):
    d = os.path.join(tmp, "engine", "%s_study" % ticker.lower())
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, "study_numbers.json")
    if raw is not None:
        open(p, "w").write(raw)
        return
    doc = {"meta": {"ticker": ticker}}
    if record is not None:
        doc["bridge_record"] = record
    if declaration is not None:
        doc["equity_direct_declaration"] = declaration
    if extra:
        doc.update(extra)
    json.dump(doc, open(p, "w"), indent=1)


def put_list(tmp, tickers):
    json.dump({"why": "negative control", "adopted": "2026-09-02",
               "outstanding": sorted(tickers)},
              open(os.path.join(tmp, "engine", "build_depth_audit",
                                "bridge_outstanding.json"), "w"), indent=1)


def case(name, build, expect_red, results):
    tmp = sandbox()
    try:
        build(tmp)
        r = subprocess.run([sys.executable, GATE], cwd=tmp, capture_output=True, text=True,
                       env=_FIXTURE_ENV)
        out = (r.stdout + r.stderr).strip()
        red = r.returncode != 0
        ok = red == expect_red
        results.append((name, ok, r.returncode, out.splitlines()[-1] if out else ""))
        if not ok:
            print("\n---- %s ----\n%s" % (name, out))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    results = []

    def broken(mutate):
        def build(tmp):
            rec = json.loads(json.dumps(GOOD))
            mutate(rec)
            put_study(tmp, "NCB", rec)
            put_list(tmp, [])
        return build

    def m_stale(r):
        r["balance_sheet_date"] = "2025-12-31"

    def m_noregister(r):
        r.pop("latest_disclosed_source")
        r.pop("latest_disclosed_date")

    def m_book(r):
        r["nci"]["basis"] = "book"

    def m_nodeduct(r):
        r["nci"]["deduction"] = 0
        r["lines"] = [l for l in r["lines"] if "minority" not in l["label"]]
        r["equity_value"] = 90000.0
        r["per_share"] = 90.0

    def m_on_ev(r):
        r["nci"]["applied_to"] = "enterprise_value"

    def m_twice(r):
        r["cash"]["weights_basis"] = "net"

    def m_nofoot(r):
        r["lines"][0]["value"] = 120000.0

    def m_pershare(r):
        r["per_share"] = 95.0

    def m_dividend(r):
        r["dividend"] = {"deducted": True, "declared_date": "2026-03-01"}

    for n, m in (("1 stale balance sheet", m_stale),
                 ("2 no register establishing latest", m_noregister),
                 ("3 minority at book", m_book),
                 ("4 minority not deducted", m_nodeduct),
                 ("5 minority off enterprise value", m_on_ev),
                 ("6 cash charged twice", m_twice),
                 ("7 bridge does not foot", m_nofoot),
                 ("8 per share does not divide", m_pershare),
                 ("9 dividend declared before the sheet", m_dividend)):
        case(n, broken(m), True, results)

    def b_norecord(tmp):
        put_study(tmp, "NCB", None)
        put_list(tmp, [])
    case("10 new study, no record, not listed", b_norecord, True, results)

    def b_unreadable(tmp):
        put_study(tmp, "NCB", None, raw="{not json")
        put_list(tmp, [])
    case("11 numbers file will not parse", b_unreadable, True, results)

    def b_empty(tmp):
        put_list(tmp, ["GHOST"])
    case("12 empty population", b_empty, True, results)

    # ---- THE DECLARATION [R-BRIDGE-01 CLAUSE FIVE, 13-09-2026] --------------
    # Modelled on ADIB's own committed shape: seven lenses that each land on equity per
    # share, a reviewed 30-June-2026 sheet, the sweep finding that establishes it is the
    # latest, and equity over shares reaching the figure the study publishes.
    DECL = {
        "declared_on": "2026-09-13",
        "no_enterprise_value": True,
        "why": "a bank is valued on what reaches the shareholder; deposits are its raw "
               "material and not its financing",
        "lenses": ["dividend_discount", "free_cash_flow_to_equity", "residual_income",
                   "relative_multiples", "book_value_and_sustainable_return",
                   "book_value_floor", "normalised_earnings_power"],
        "primary_lens": "dividend_discount",
        "balance_sheet_date": "2026-06-30",
        "latest_disclosed_date": "2026-06-30",
        "latest_disclosed_source": "the reviewed interim statements registered in the "
                                   "study's own Step 2A sweep",
        "equity_value": 66691.468,
        "shares_mn": 1500.0,
        "per_share": 44.460978,
    }
    CENTRAL = {"central": 44.460978}

    def declared(mutate=None, extra=None, record=None):
        def build(tmp):
            dec = json.loads(json.dumps(DECL))
            if mutate:
                mutate(dec)
            ex = dict(CENTRAL)
            if extra:
                ex.update(extra)
            put_study(tmp, "NCB", record, declaration=dec, extra=ex)
            put_list(tmp, [])
        return build

    def d_silent(dec):
        # the exact shape the clause exists to refuse: the study stops saying it, which
        # is where it already stood before the clause existed
        dec.pop("no_enterprise_value")

    def d_false(dec):
        dec["no_enterprise_value"] = "not applicable"

    def d_no_register(dec):
        dec.pop("latest_disclosed_date"); dec.pop("latest_disclosed_source")

    def d_stale(dec):
        dec["balance_sheet_date"] = "2025-12-31"

    def d_no_lenses(dec):
        dec["lenses"] = []

    def d_primary_not_among(dec):
        dec["primary_lens"] = "discounted_cash_flow"

    def d_no_divide(dec):
        dec["per_share"] = 52.05

    for n, m in (("13 a declaration silent on the claim itself", d_silent),
                 ("14 a declaration that asserts something else", d_false),
                 ("15 a declaration with no register establishing latest", d_no_register),
                 ("16 a declaration on a stale balance sheet", d_stale),
                 ("17 a declaration naming no lenses", d_no_lenses),
                 ("18 a primary lens not among the declared lenses", d_primary_not_among),
                 ("19 a declaration whose per share does not divide", d_no_divide)):
        case(n, declared(m), True, results)

    # THE CLAUSE THAT KEEPS THIS FROM BEING A WAY OUT. Each of these is a shape a real
    # industrial study in this book commits, planted under a declaration that says it
    # does not exist anywhere.
    for n, ex in (("20 declared, and an enterprise value in the numbers",
                   {"valuation": {"enterprise_value": 100000.0}}),
                  ("21 declared, and a net debt in the numbers",
                   {"fcst_bs": [{"net_debt": 24133.2}]}),
                  ("22 declared, and a WACC in the numbers",
                   {"coc_record": {"wacc_exp": 0.2743}}),
                  ("23 declared, and an enterprise-value line in a table",
                   {"value_table": {"lines": [{"label": "Enterprise value",
                                               "value": 24364.6}]}})):
        case(n, declared(extra=ex), True, results)

    def b_both(tmp):
        dec = json.loads(json.dumps(DECL))
        put_study(tmp, "NCB", GOOD, declaration=dec, extra=dict(CENTRAL))
        put_list(tmp, [])
    case("24 commits BOTH a bridge and a declaration that it builds none",
         b_both, True, results)

    def b_not_the_published_answer(tmp):
        dec = json.loads(json.dumps(DECL))
        put_study(tmp, "NCB", None, declaration=dec, extra={"central": 37.18})
        put_list(tmp, [])
    case("25 a declaration that divides to a figure the study does not publish",
         b_not_the_published_answer, True, results)

    # ---- clean cases -------------------------------------------------------
    def c_declared(tmp):
        put_study(tmp, "NCB", None, declaration=json.loads(json.dumps(DECL)),
                  extra=dict(CENTRAL))
        put_list(tmp, [])
    case("clean: a complete no-bridge declaration", c_declared, False, results)

    def c_declared_prose(tmp):
        # PROSE ABOUT THE ABSENCE IS EVIDENCE FOR THE DECLARATION, NOT AGAINST IT.
        put_study(tmp, "NCB", None, declaration=json.loads(json.dumps(DECL)),
                  extra=dict(CENTRAL, cost_of_capital_record={
                      "no_wacc_reason": "a bank has no weighted cost of capital: deposits "
                                        "are raw material, not financing",
                      "net_debt_note": "there is no net debt in this valuation"}))
        put_list(tmp, [])
    case("clean: a declaration beside prose saying there is no WACC",
         c_declared_prose, False, results)

    def c_good(tmp):
        put_study(tmp, "NCB", GOOD)
        put_list(tmp, [])
    case("clean: a conforming bridge", c_good, False, results)

    def c_listed(tmp):
        rec = json.loads(json.dumps(GOOD)); m_stale(rec)
        put_study(tmp, "NCB", rec)
        put_list(tmp, ["NCB"])
    case("clean: a listed outstanding study", c_listed, False, results)

    def c_netweights(tmp):
        # net-debt weights are legitimate WHEN the cash is not also added at face
        rec = json.loads(json.dumps(GOOD))
        rec["cash"] = {"treatment": "inside_the_flow", "weights_basis": "net"}
        rec["lines"] = [l for l in rec["lines"] if l["label"] != "plus cash"]
        rec["lines"][0]["value"] = 120000.0
        put_study(tmp, "NCB", rec)
        put_list(tmp, [])
    case("clean: net weights, cash not re-added", c_netweights, False, results)

    def c_nonci(tmp):
        rec = json.loads(json.dumps(GOOD))
        rec["nci"] = {"basis": "none_disclosed",
                      "evidence": "the statements show no non-controlling interest line"}
        rec["lines"] = [l for l in rec["lines"] if "minority" not in l["label"]]
        rec["equity_value"] = 90000.0
        rec["per_share"] = 90.0
        put_study(tmp, "NCB", rec)
        put_list(tmp, [])
    case("clean: no minority, evidenced", c_nonci, False, results)

    print("\nNEGATIVE CONTROL — scripts/check_bridge.py")
    for name, ok, rc, last in results:
        print("  %-38s %-4s exit %d   %s" % (name, "ok" if ok else "MISS", rc, last[:70]))
    bad = [n for n, ok, _, _ in results if not ok]
    if bad:
        print("\nFAILED on: %s" % ", ".join(bad))
        return 1
    print("\nAll %d conditions behave as claimed." % len(results))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
