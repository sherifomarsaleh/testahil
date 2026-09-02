"""A CHECK NOBODY HAS SEEN FAIL IS NOT EVIDENCE.

Reinjects every condition scripts/check_cost_of_capital.py claims to catch, and
asserts the gate goes RED. Clean cases must NOT fire.

The failure cases are the repository's own:

  1. A FLAT RATE IN A TRANSITION MARKET — PHDC and TMGH discount every explicit
     year and the terminal alike at 26.25% and 32.37%, which asserts Egypt's
     cost of capital never normalises.
  2. TWO PRICES FOR ONE DATE — the terminal brought home on a lower factor than
     the last explicit year's cash flow. Measured on one reconciliation: 0.410
     against 0.532, a 30% premium for relabelling the same pound.
  3. THE SOVEREIGN COUNTED TWICE — the raw local yield beside a premium that
     already carries country risk. The version-1 bug that reached GBCO.
  4. A QUOTED TERMINAL — a terminal risk-free rate set by hand rather than
     derived from the target plus the real-rate convention.
  5. KD BELOW THE SOVEREIGN — found in AMOC's own committed record on the day
     this gate was written: 22.00% against its own recorded 22.31%.
  6. KD ON A CONTRACTUAL MIDPOINT — one study took the midpoint of a disclosed
     15-25.27% range while the rate actually paid was 24.0%.
  7. AN UNDESCRIBED DENOMINATOR — the finance charge divided by a liabilities
     total that includes balances bearing no interest, which understates the
     rate by a multiple.
  8. A NON-MONOTONE LADDER, and a ladder that does not sit on its own fractions.
  9. NO ALTERNATIVE PREMIUM BASIS published beside the adopted one.
 10. NO RECORD / UNREADABLE / EMPTY POPULATION.

    python3 scripts/check_cost_of_capital_negative_control.py
"""
import json, os, shutil, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GATE = os.path.join("scripts", "check_cost_of_capital.py")

sys.path.insert(0, os.path.join(ROOT, "engine"))
import cost_of_capital as COC                                    # noqa: E402


def good_record():
    b = COC.BetaRecord(beta=1.0493, tier=1, source="own-stock regression", conforming=True,
                       se=0.1823, r2=0.299, n=251)
    d = COC.DebtBook(gross_debt=33552.7, pct_local_currency=1.0,
                     currency_source="all eight borrowing lines are EGP",
                     kd_local_pretax=0.255, kd_source="the company's own latest issue",
                     effective_rates=(0.243, 0.251),
                     effective_rate_periods=("FY2024", "FY2025"),
                     interest_bearing_note="finance cost over the average bank and loan lines only")
    s = COC.schedule("EG", b, d, market_cap=43470.8, tax_rate=0.225, years=5,
                     erp_explicit=0.0941, erp_basis="cds", allow_stale_sovereign=True)
    return s.as_record()


def sandbox():
    tmp = tempfile.mkdtemp(prefix="coc_nc_")
    os.makedirs(os.path.join(tmp, "engine", "build_depth_audit"))
    os.makedirs(os.path.join(tmp, "scripts"))
    for f in ("research_protocol.py", "macro_path.py", "cost_of_capital.py"):
        shutil.copy(os.path.join(ROOT, "engine", f), os.path.join(tmp, "engine", f))
    shutil.copytree(os.path.join(ROOT, "engine", "macro_paths"),
                    os.path.join(tmp, "engine", "macro_paths"))
    shutil.copy(os.path.join(ROOT, "scripts", "check_cost_of_capital.py"),
                os.path.join(tmp, "scripts", "check_cost_of_capital.py"))
    return tmp


def put_study(tmp, ticker, record, raw=None):
    d = os.path.join(tmp, "engine", "%s_study" % ticker.lower())
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, "study_numbers.json")
    if raw is not None:
        open(p, "w").write(raw); return
    doc = {"meta": {"ticker": ticker}}
    if record is not None:
        doc["cost_of_capital_record"] = record
    json.dump(doc, open(p, "w"), indent=1)


def put_list(tmp, tickers):
    json.dump({"why": "negative control", "adopted": "2026-09-02",
               "outstanding": sorted(tickers)},
              open(os.path.join(tmp, "engine", "build_depth_audit",
                                "coc_outstanding.json"), "w"), indent=1)


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
    GOOD = good_record()
    results = []

    def broken(mutate):
        def build(tmp):
            rec = json.loads(json.dumps(GOOD)); mutate(rec)
            put_study(tmp, "NCC", rec); put_list(tmp, [])
        return build

    def m_flat(r):
        flat = r["wacc_exp"]
        r["wacc_terminal"] = flat
        r["forward_wacc"] = [flat] * 5
        cum = 1.0; df = []
        for w in r["forward_wacc"]:
            cum /= (1 + w); df.append(cum)
        r["discount_factors"] = df; r["terminal_discount_factor"] = df[-1]
        r["glide_fractions"] = [0.0] * 5

    def m_two_prices(r):
        r["terminal_discount_factor"] = r["discount_factors"][-1] * 1.3

    def m_double_count(r):
        r["rf_star"] = r["rf_observed"]

    def m_quoted_terminal(r):
        r["rf_terminal"] = 0.105

    def m_kd_below_sovereign(r):
        # AMOC's own committed pair, as found on 02-Sep-2026
        r["kd_pretax"] = 0.2200
        r["rf_observed"] = 0.2231
        r["rf_star"] = 0.2231 - r["default_spread"]
        r["kd_integrity"]["effective_rates"] = [0.215, 0.220]

    def m_midpoint(r):
        r["kd_integrity"]["effective_rates"] = [0.240]

    def m_escape_abused(r):
        # the stop-and-inform escape used as a waiver: no rate, and a reason that
        # names an inconvenience rather than a disclosure
        r["kd_integrity"]["effective_rates"] = []
        r["kd_integrity"]["effective_rate_unavailable"] = "not available"

    # THE SHAPE OF THE EVIDENCE, NOT ONLY ITS VALUES. Every case above hands the
    # gate an effective_rates that is already a well-formed sequence, so none of
    # them could ever have caught what happened on 02-Sep-2026: the ARCC re-issue
    # recorded effective_rates as a MAPPING of fiscal year to rate, the gate
    # reached eff[-1], died with a bare KeyError before printing anything at all,
    # and a run of it read as "no ARCC failures" when it had examined nothing.
    # Seventeen synthetic conditions passed while the gate was broken on real
    # data. These three cases are that incident.
    def m_eff_mapping(r):
        # the shape that crashed it. A mapping NAMES its periods and is better
        # evidence than a bare list, so the gate must ACCEPT it — this case is
        # registered as one that must stay GREEN.
        r["kd_integrity"]["effective_rates"] = {"FY2024": 0.243, "FY2025": 0.251}

    def m_eff_garbage(r):
        # a shape that is neither: the gate must REFUSE with a message, never die
        r["kd_integrity"]["effective_rates"] = "0.243 and 0.251"

    def m_eff_nonnumeric(r):
        r["kd_integrity"]["effective_rates"] = [0.243, "n/a"]

    def m_denominator(r):
        r["kd_integrity"]["interest_bearing_note"] = ""

    def m_nonmonotone(r):
        r["forward_wacc"] = list(r["forward_wacc"])
        r["forward_wacc"][2], r["forward_wacc"][3] = r["forward_wacc"][3], r["forward_wacc"][2]

    def m_offladder(r):
        r["forward_wacc"] = [w - 0.01 for w in r["forward_wacc"]]

    def m_nobasis(r):
        r["sensitivity"] = {}

    for n, m in (("1 flat rate in a transition market", m_flat),
                 ("2 two prices for one date", m_two_prices),
                 ("3 sovereign counted twice", m_double_count),
                 ("4 quoted terminal risk-free", m_quoted_terminal),
                 ("5 Kd below its own sovereign", m_kd_below_sovereign),
                 ("6 Kd on one period only", m_midpoint),
                 ("7 effective-rate denominator undescribed", m_denominator),
                 ("7b stop-and-inform escape used as a waiver", m_escape_abused),
                 ("8 ladder not monotone", m_nonmonotone),
                 ("9 ladder off its own fractions", m_offladder),
                 ("10 no alternative premium basis", m_nobasis),
                 ("12 effective_rates neither a sequence nor a mapping", m_eff_garbage),
                 ("13 effective_rates carries a non-numeric entry", m_eff_nonnumeric)):
        case(n, broken(m), True, results)

    # a period-keyed mapping is GOOD evidence and must not be refused
    case("CLEAN — effective_rates as a period-keyed mapping, must PASS",
         broken(m_eff_mapping), False, results)

    def b_norecord(tmp):
        put_study(tmp, "NCC", None); put_list(tmp, [])
    case("11 new study, no record, not listed", b_norecord, True, results)

    def b_unreadable(tmp):
        put_study(tmp, "NCC", None, raw="{nope"); put_list(tmp, [])
    case("12 numbers file will not parse", b_unreadable, True, results)

    def b_empty(tmp):
        put_list(tmp, ["GHOST"])
    case("13 empty population", b_empty, True, results)

    def c_good(tmp):
        put_study(tmp, "NCC", GOOD); put_list(tmp, [])
    case("clean: a conforming schedule", c_good, False, results)

    def c_escape(tmp):
        # the escape used HONESTLY: no independent rate, and a reason naming the
        # disclosure that is missing
        rec = json.loads(json.dumps(GOOD))
        rec["kd_integrity"]["effective_rates"] = []
        rec["kd_integrity"]["effective_rate_unavailable"] = (
            "part of the interest incurred is capitalised into work in progress and the "
            "statements do not disclose the capitalised amount separately, so interest "
            "incurred over average interest-bearing debt cannot be computed from what the "
            "company discloses; the charge that IS disclosed understates the rate by a "
            "large multiple")
        put_study(tmp, "NCC", rec); put_list(tmp, [])
    case("clean: escape used honestly, disclosure named", c_escape, False, results)

    def c_listed(tmp):
        rec = json.loads(json.dumps(GOOD)); m_flat(rec)
        put_study(tmp, "NCC", rec); put_list(tmp, ["NCC"])
    case("clean: a listed outstanding study", c_listed, False, results)

    print("\nNEGATIVE CONTROL — scripts/check_cost_of_capital.py")
    for name, ok, rc, last in results:
        print("  %-42s %-4s exit %d   %s" % (name, "ok" if ok else "MISS", rc, last[:62]))
    bad = [n for n, ok, _, _ in results if not ok]
    if bad:
        print("\nFAILED on: %s" % ", ".join(bad)); return 1
    print("\nAll %d conditions behave as claimed." % len(results))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
