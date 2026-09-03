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

    python3 scripts/check_bridge_negative_control.py
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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


def put_study(tmp, ticker, record, raw=None):
    d = os.path.join(tmp, "engine", "%s_study" % ticker.lower())
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, "study_numbers.json")
    if raw is not None:
        open(p, "w").write(raw)
        return
    doc = {"meta": {"ticker": ticker}}
    if record is not None:
        doc["bridge_record"] = record
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
        r = subprocess.run([sys.executable, GATE], cwd=tmp, capture_output=True, text=True)
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

    # ---- clean cases -------------------------------------------------------
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
