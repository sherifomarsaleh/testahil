#!/usr/bin/env python3
"""A CHECK NOBODY HAS SEEN FAIL IS NOT EVIDENCE.

Reinjects every condition scripts/check_forecast_anchor.py claims to catch and
asserts the gate goes RED, plus clean cases that must NOT fire.

The headline case is AMOC's own forecast exactly as it stood on 3 September 2026:
a first forecast year of 9.494% against a filed half of 12.428%, an implied
second half of 6.56%, and a mechanism whose direction is contradicted by the
company's own five filed periods.

    python3 scripts/check_forecast_anchor_negative_control.py
"""
import json, os, shutil, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GATE = os.path.join("scripts", "check_forecast_anchor.py")

# ---- AMOC's own numbers, as they shipped -----------------------------------
AMOC_LATEST = 0.12428          # gross margin, six months to 30-Jun-2026, reviewed
AMOC_FIRST = 0.09494           # FY2026E gross margin as the study forecast it
AMOC_COST_A = 0.93146          # cost per unit of revenue, first filed period
AMOC_COST_B = 0.87572          # cost per unit of revenue, latest filed period -- it FELL

GOOD = {
    "rate_name": "gross margin",
    "latest_reviewed_period": "six months to 30 June 2026",
    "latest_reviewed_date": "2026-06-30",
    "latest_reviewed_rate": 0.12428,
    "first_forecast_rate": 0.12500,
}


def sandbox():
    tmp = tempfile.mkdtemp(prefix="anchor_nc_")
    os.makedirs(os.path.join(tmp, "engine", "build_depth_audit"))
    os.makedirs(os.path.join(tmp, "scripts"))
    shutil.copy(os.path.join(ROOT, GATE), os.path.join(tmp, GATE))
    return tmp


def put_study(tmp, ticker, record, raw=None):
    d = os.path.join(tmp, "engine", "%s_study" % ticker.lower())
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, "study_numbers.json")
    if raw is not None:
        open(p, "w").write(raw); return
    doc = {"meta": {"ticker": ticker}}
    if record is not None:
        doc["forecast_anchor"] = record
    json.dump(doc, open(p, "w"), indent=1)


def put_list(tmp, tickers):
    json.dump({"why": "negative control", "adopted": "2026-09-03",
               "outstanding": sorted(tickers)},
              open(os.path.join(tmp, "engine", "build_depth_audit",
                                "anchor_outstanding.json"), "w"), indent=1)


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
            rec = json.loads(json.dumps(GOOD)); mutate(rec)
            put_study(tmp, "NCL", rec); put_list(tmp, [])
        return build

    # ---- THE HEADLINE CASE -------------------------------------------------
    def m_amoc_as_shipped(r):
        # exactly as it stood: a forecast 2.93 points below the filed half, and no
        # mechanism named anywhere in the study
        r["latest_reviewed_rate"] = AMOC_LATEST
        r["first_forecast_rate"] = AMOC_FIRST

    def m_amoc_with_a_contradicted_mechanism(r):
        # the mechanism the model was ACTUALLY running -- input cost outpacing
        # price -- supplied with the company's own like-for-like measurement,
        # which runs the other way. This is the clause the gate exists for.
        r["latest_reviewed_rate"] = AMOC_LATEST
        r["first_forecast_rate"] = AMOC_FIRST
        r["mechanism"] = {
            "name": "input_cost_outpacing_price",
            "disclosure": "the pound conversion legs escalate at the domestic inflation "
                          "ladder while realised price grows at the currency differential",
            "like_for_like": {
                "measures": "cost per unit of revenue",
                "period_a": "six months to 31 December 2024", "value_a": AMOC_COST_A,
                "period_b": "six months to 30 June 2026", "value_b": AMOC_COST_B,
                "higher_is_worse": True},
        }

    def m_egch_as_shipped(r):
        # EGCH: gross margin forecast to fall from 45.66% to 33.02% on a typed,
        # unsourced dollar price path, with no mechanism declared
        r["rate_name"] = "gross margin"
        r["latest_reviewed_rate"] = 0.4566
        r["first_forecast_rate"] = 0.3302

    def m_mechanism_not_on_list(r):
        r["first_forecast_rate"] = 0.09494
        r["mechanism"] = {"name": "the rate looked wrong",
                          "disclosure": "judgement",
                          "like_for_like": {"measures": "x", "period_a": "a", "value_a": 1.0,
                                            "period_b": "b", "value_b": 2.0}}

    def m_mechanism_no_disclosure(r):
        r["first_forecast_rate"] = 0.09494
        r["mechanism"] = {"name": "subsidy_or_levy_withdrawal", "disclosure": "",
                          "like_for_like": {"measures": "x", "period_a": "a", "value_a": 1.0,
                                            "period_b": "b", "value_b": 2.0}}

    def m_mechanism_no_measurement(r):
        r["first_forecast_rate"] = 0.09494
        r["mechanism"] = {"name": "subsidy_or_levy_withdrawal",
                          "disclosure": "the levy note in the FY2025 filing"}

    def m_no_latest_rate(r):
        r.pop("latest_reviewed_rate")

    def m_no_rate_name(r):
        r.pop("rate_name")

    def m_unparseable_rates(r):
        r["first_forecast_rate"] = "about nine and a half per cent"

    # ---- CLAUSE TWO: THE PATH ---------------------------------------------
    # EGCH'S PATH EXACTLY AS IT SHIPPED, and it is the case that proves the
    # opening-year test alone is not enough: the forecast OPENS at 45.66%
    # against a latest audited year of 38.39% -- seven points ABOVE it, which
    # clause one is right not to fire on -- and then falls to 33.02%, below
    # every audited year but one, on a typed dollar price path nothing sourced.
    # A gate reading only the first forecast year passes this.
    def m_egch_path_as_shipped(r):
        r["latest_reviewed_rate"] = 0.38387
        r["first_forecast_rate"] = 0.45664
        r["forecast_path"] = [0.45664, 0.42200, 0.38230, 0.35070, 0.33020]

    def m_path_declines_no_mechanism(r):
        r["forecast_path"] = [0.12428, 0.12000, 0.11500, 0.11000, 0.10500]

    def m_path_unparseable(r):
        r["forecast_path"] = [0.12428, "a bit less", 0.11]

    for n, m in (("14 EGCH's path as shipped -- opens above, falls below",
                  m_egch_path_as_shipped),
                 ("15 a declining path with no mechanism", m_path_declines_no_mechanism),
                 ("16 a path that does not parse", m_path_unparseable)):
        case(n, broken(m), True, results)

    for n, m in (("1 AMOC as shipped -- 2.93pp below the filed half, no mechanism",
                  m_amoc_as_shipped),
                 ("2 AMOC's mechanism, contradicted by its own filings",
                  m_amoc_with_a_contradicted_mechanism),
                 ("3 EGCH as shipped -- 45.66% to 33.02%, no mechanism", m_egch_as_shipped),
                 ("4 mechanism not on the closed list", m_mechanism_not_on_list),
                 ("5 mechanism with no disclosure", m_mechanism_no_disclosure),
                 ("6 mechanism with no like-for-like measurement", m_mechanism_no_measurement),
                 ("7 no latest reviewed rate", m_no_latest_rate),
                 ("8 no rate named", m_no_rate_name),
                 ("9 rates that do not parse", m_unparseable_rates)):
        case(n, broken(m), True, results)

    def b_norecord(tmp):
        put_study(tmp, "NCL", None); put_list(tmp, [])
    case("10 new study, no record, not listed", b_norecord, True, results)

    def b_unreadable(tmp):
        put_study(tmp, "NCL", None, raw="{nope"); put_list(tmp, [])
    case("11 numbers file will not parse", b_unreadable, True, results)

    def b_empty(tmp):
        put_list(tmp, [])
    case("12 empty population", b_empty, True, results)

    def b_ghost(tmp):
        put_study(tmp, "NCL", GOOD); put_list(tmp, ["GHOST"])
    case("13 outstanding list names a study not on disk", b_ghost, True, results)

    # ---- clean -------------------------------------------------------------
    def c_good(tmp):
        put_study(tmp, "NCL", GOOD); put_list(tmp, [])
    case("clean: forecast at the latest reviewed rate", c_good, False, results)

    def c_above(tmp):
        # ARCC's shape: the forecast opens essentially AT the filed peak. This gate
        # must not fire on it -- that direction is [R-GAP-01]'s and the sign test's,
        # and a gate firing both ways here would collide with them.
        rec = json.loads(json.dumps(GOOD))
        rec["rate_name"] = "EBITDA margin"
        rec["latest_reviewed_period"] = "FY2025, audited"
        rec["latest_reviewed_rate"] = 0.3925
        rec["first_forecast_rate"] = 0.3903
        put_study(tmp, "NCL", rec); put_list(tmp, [])
    case("clean: ARCC's shape -- forecast at the filed peak", c_above, False, results)

    def c_mechanism_agreeing(tmp):
        # a decline that is NAMED, SOURCED and MEASURED in the right direction:
        # this is what the rule permits and it must stay green
        rec = json.loads(json.dumps(GOOD))
        rec["first_forecast_rate"] = 0.0900
        rec["mechanism"] = {
            "name": "subsidy_or_levy_withdrawal",
            "disclosure": "the fuel subsidy schedule in the FY2025 notes, effective "
                          "1 January 2027",
            "like_for_like": {
                "measures": "energy cost per tonne as a share of revenue",
                "period_a": "H1 2025", "value_a": 0.181,
                "period_b": "H1 2026", "value_b": 0.224,
                "higher_is_worse": True},
        }
        put_study(tmp, "NCL", rec); put_list(tmp, [])
    case("clean: a decline named, sourced and measured the right way",
         c_mechanism_agreeing, False, results)

    def c_path_flat(tmp):
        # a path held essentially flat must not fire
        rec = json.loads(json.dumps(GOOD))
        rec["forecast_path"] = [0.12500, 0.12480, 0.12460, 0.12450, 0.12440]
        put_study(tmp, "NCL", rec); put_list(tmp, [])
    case("clean: a path held flat", c_path_flat, False, results)

    def c_path_declines_with_mechanism(tmp):
        # EGCH's CORRECTED shape: the path still declines 7.9% because domestic
        # cost legs escalate against a dollar-linked price, and the mechanism is
        # named, sourced and MEASURED in the right direction from its own audited
        # accounts (cost per unit of revenue rose 54.059% -> 61.613%)
        rec = json.loads(json.dumps(GOOD))
        rec["latest_reviewed_rate"] = 0.38387
        rec["first_forecast_rate"] = 0.45664
        rec["forecast_path"] = [0.45664, 0.44900, 0.43930, 0.42970, 0.42080]
        rec["mechanism"] = {
            "name": "input_cost_outpacing_price",
            "disclosure": "pound-denominated cost legs against a dollar-linked "
                          "export price, both from the audited cost stack",
            "like_for_like": {
                "measures": "cost per unit of revenue, audited full years",
                "period_a": "FY2022/23", "value_a": 0.54059,
                "period_b": "FY2024/25", "value_b": 0.61613,
                "higher_is_worse": True},
        }
        put_study(tmp, "NCL", rec); put_list(tmp, [])
    case("clean: EGCH corrected -- path declines, mechanism measured and agreeing",
         c_path_declines_with_mechanism, False, results)

    def c_path_rises(tmp):
        rec = json.loads(json.dumps(GOOD))
        rec["forecast_path"] = [0.12500, 0.12700, 0.12900, 0.13100, 0.13300]
        put_study(tmp, "NCL", rec); put_list(tmp, [])
    case("clean: a rising path", c_path_rises, False, results)

    def c_listed(tmp):
        rec = json.loads(json.dumps(GOOD)); m_amoc_as_shipped(rec)
        put_study(tmp, "NCL", rec); put_list(tmp, ["NCL"])
    case("clean: a listed outstanding study", c_listed, False, results)

    def c_tolerance(tmp):
        # a difference inside the rounding width of a two-decimal filed rate must
        # not fire: a study is never asked to explain what its source cannot resolve
        rec = json.loads(json.dumps(GOOD))
        rec["first_forecast_rate"] = GOOD["latest_reviewed_rate"] - 0.0015
        put_study(tmp, "NCL", rec); put_list(tmp, [])
    case("clean: inside the rounding tolerance", c_tolerance, False, results)

    print("\n  %-62s %-4s %s" % ("condition", "ok", "gate said"))
    print("  " + "-" * 100)
    for n, ok, rc, line in results:
        print("  %-62s %-4s exit %d   %s" % (n, "ok" if ok else "WRONG", rc, line[:60]))
    bad = [r for r in results if not r[1]]
    print("\n%s" % ("All %d conditions behave as claimed." % len(results) if not bad
                    else "FAIL - %d condition(s) did not behave as claimed." % len(bad)))
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
