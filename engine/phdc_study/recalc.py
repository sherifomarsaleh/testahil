"""Independently recalculate the delivered workbook and compare it to the study.

Numeric traceability: a clean-looking workbook is not evidence. This evaluates
the formula cells that matter from the workbook's OWN inputs, without touching
the Python model, and checks the answers against study_numbers.json. Anything
that will not parse is reported as a FAILURE, never skipped.
"""
import json, os, re, sys
from openpyxl import load_workbook

HERE = os.path.dirname(os.path.abspath(__file__))
N = json.load(open(os.path.join(HERE, "study_numbers.json")))
XL = os.path.join(HERE, "PHDC_Valuation_Model_30082026.xlsx")


def evaluate(wb, sheet, ref, depth=0):
    """Resolve one cell, following formula references. Raises on anything it
    cannot parse — an unparseable cell is a failure, not a skip."""
    if depth > 24:
        raise ValueError("reference cycle at %s!%s" % (sheet, ref))
    val = wb[sheet][ref].value
    if val is None:
        return 0.0
    if isinstance(val, (int, float)):
        return float(val)
    if not (isinstance(val, str) and val.startswith("=")):
        raise ValueError("cell %s!%s is neither number nor formula: %r"
                         % (sheet, ref, val))
    expr = val[1:]
    tok = re.compile(r"(?:'([^']+)'|([A-Za-z][A-Za-z0-9 &_\-]*))!\$?([A-Z]+)\$?(\d+)"
                     r"|\$?([A-Z]+)\$?(\d+)")

    def sub(m):
        if m.group(3):
            sh = (m.group(1) or m.group(2)).strip()
            return repr(evaluate(wb, sh, "%s%s" % (m.group(3), m.group(4)), depth + 1))
        return repr(evaluate(wb, sheet, "%s%s" % (m.group(5), m.group(6)), depth + 1))

    py = tok.sub(sub, expr).replace("^", "**")
    if re.search(r"SUM\(", py, re.I):
        raise ValueError("SUM not resolved at %s!%s: %s" % (sheet, ref, expr))
    return float(eval(py, {"__builtins__": {}}, {}))


def main():
    wb = load_workbook(XL)
    checks, fails = [], 0

    def chk(name, got, want, tol):
        nonlocal fails
        ok = abs(got - want) <= tol
        checks.append({"check": name, "workbook": round(got, 4),
                       "study": round(want, 4), "ok": ok})
        if not ok:
            fails += 1

    base = N["cases"]["base"]
    D = N["derived"]

    ev = evaluate(wb, "Fundamental Valuation", "B6")
    chk("enterprise value", ev, base["ev"], 1.0)
    eq = evaluate(wb, "Fundamental Valuation", "B10")
    chk("equity value", eq, base["equity"], 1.0)
    ps = evaluate(wb, "Fundamental Valuation", "B12")
    chk("value per share", ps, base["per_share"], 0.01)
    tv = evaluate(wb, "Fundamental Valuation", "B14")
    chk("terminal share of enterprise value", tv, base["terminal_share"], 0.001)

    sotp = evaluate(wb, "SOTP Bridge", "B10")
    chk("bridge sheet agrees with the valuation sheet on value per share",
        sotp, base["per_share"], 0.02)

    # the discounted-cash-flow sheet's own revenue path against the model's
    ws = wb["DCF"]
    for j, r in zip(range(2, 12), base["rows"]):
        col = ws.cell(1, j).column_letter
        got = evaluate(wb, "DCF", "%s6" % col)
        chk("DCF revenue %d" % r["year"], got, r["revenue"], 1.0)

    bs = wb["Balance Sheet"]
    chk("balance sheet balances, 2025", evaluate(wb, "Balance Sheet", "B12"), 0.0, 0.2)
    chk("balance sheet balances, 2024", evaluate(wb, "Balance Sheet", "C12"), 0.0, 0.2)

    for k, want in (("B5", D["cfo_mid"]), ("B12", N["wacc"]["wacc_rating"]),
                    ("B13", D["net_debt"]), ("B16", D["shares_mn"])):
        chk("assumption %s" % k, evaluate(wb, "Assumptions", k), want, 0.01)

    json.dump(checks, open(os.path.join(HERE, "recalc_result.json"), "w"), indent=1)
    for c in checks:
        print("  %-52s workbook %12.4f   study %12.4f   %s"
              % (c["check"][:52], c["workbook"], c["study"],
                 "ok" if c["ok"] else "MISMATCH"))
    print("\n%d checks, %d mismatches" % (len(checks), fails))
    if fails:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
