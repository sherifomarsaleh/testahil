#!/usr/bin/env python3
"""A CHECK NOBODY HAS SEEN FAIL IS NOT EVIDENCE.

Reinjects every condition scripts/check_artefact_currency.py claims to catch and
asserts the gate goes RED, plus clean cases that must NOT fire.

THE THREE HEADLINE CASES ARE THE THREE THAT PROVOKED THE RULE, rebuilt as they
stood on 3 September 2026:

  AMOC   case_adversarial.json, base central 5.954 against a published 11.834
  ARCC   efg_bridge.json, `end` 54.65 against a published 53.21 -- the case the
         gate's own FIRST DRAFT could not see, because it carries its figure under
         a key the value-key list did not know
  EGCH   contested_judgements.json, value_adopted -1.0621 against a published
         1.7854

    python3 scripts/check_artefact_currency_negative_control.py
"""
import json, os, shutil, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GATE = os.path.join("scripts", "check_artefact_currency.py")


def sandbox():
    tmp = tempfile.mkdtemp(prefix="artefact_nc_")
    os.makedirs(os.path.join(tmp, "engine", "build_depth_audit"))
    os.makedirs(os.path.join(tmp, "scripts"))
    shutil.copy(os.path.join(ROOT, GATE), os.path.join(tmp, GATE))
    # THE SANDBOX CARRIES WHAT THE GATE ACTUALLY NEEDS. This gate imports the
    # valuation-gap gate's answer reader rather than re-implementing it [R-ENF-03],
    # and a sandbox without it makes every case go red for the WRONG reason — which
    # reads exactly like going red for the right one, and is how a negative control
    # stops being evidence. The gauntlet learned this the same way.
    for dep in ("check_valuation_gap.py",):
        shutil.copy(os.path.join(ROOT, "scripts", dep),
                    os.path.join(tmp, "scripts", dep))
    return tmp


def put(tmp, ticker, central, spot, artefacts):
    d = os.path.join(tmp, "engine", "%s_study" % ticker.lower())
    os.makedirs(d, exist_ok=True)
    json.dump({"meta": {"ticker": ticker}, "central": central, "spot": spot},
              open(os.path.join(d, "study_numbers.json"), "w"), indent=1)
    for name, body in artefacts.items():
        json.dump(body, open(os.path.join(d, name), "w"), indent=1)


def put_list(tmp, tickers):
    json.dump({"_": "negative control", "seeded": "2026-09-03",
               "outstanding": sorted(tickers)},
              open(os.path.join(tmp, "engine", "build_depth_audit",
                                "artefact_outstanding.json"), "w"), indent=1)


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

    # ---- the three that provoked the rule ---------------------------------
    def c_amoc(tmp):
        put(tmp, "AMOC", 11.834178, 13.50, {"case_adversarial.json": {
            "base": {"central": 5.954022}, "published_central": 5.954022}})
        put_list(tmp, [])
    case("1 AMOC's case_adversarial.json as it stood -- base 5.954 vs 11.834",
         c_amoc, True, results)

    def c_arcc(tmp):
        # THE CASE THE FIRST DRAFT COULD NOT SEE: the figure is under `end`
        put(tmp, "ARCC", 53.2091, 77.00, {"efg_bridge.json": {
            "start": 69.75, "end": 54.65, "market": 59.00,
            "published_central": 54.65}})
        put_list(tmp, [])
    case("2 ARCC's efg_bridge.json -- the answer under a key named `end`",
         c_arcc, True, results)

    def c_egch(tmp):
        put(tmp, "EGCH", 1.7854, 14.41, {"contested_judgements.json": {
            "judgements": [{"value_adopted": -1.0621}],
            "published_central": -1.0621}})
        put_list(tmp, [])
    case("3 EGCH's contested_judgements.json -- a full edition behind",
         c_egch, True, results)

    # ---- the undeclared case, which is the one the rule actually closes ----
    def c_undeclared(tmp):
        put(tmp, "NCL", 10.0, 12.0, {"thing.json": {"base": {"central": 10.0}}})
        put_list(tmp, [])
    case("4 an artefact that declares no vintage at all", c_undeclared, True, results)

    def c_stale_spot(tmp):
        put(tmp, "NCL", 10.0, 12.0, {"thing.json": {
            "base": {"central": 10.0}, "published_central": 10.0,
            "published_spot": 9.10}})
        put_list(tmp, [])
    case("5 the central agrees and the SPOT is stale", c_stale_spot, True, results)

    def c_empty(tmp):
        put_list(tmp, [])
    case("6 empty population", c_empty, True, results)

    def c_ghost(tmp):
        put(tmp, "NCL", 10.0, 12.0, {})
        put_list(tmp, ["GHOST"])
    case("7 outstanding list names a study not on disk", c_ghost, True, results)

    # ---- clean -------------------------------------------------------------
    def k_current(tmp):
        put(tmp, "NCL", 10.0, 12.0, {"thing.json": {
            "base": {"central": 10.0}, "published_central": 10.0,
            "published_spot": 12.0}})
        put_list(tmp, [])
    case("clean: an artefact declaring the current answer", k_current, False, results)

    def k_alternative(tmp):
        # THE CASE THIS MUST NOT BREAK: an artefact whose own figures differ from the
        # study's ON PURPOSE -- an adversarial give-back, an alternative construction,
        # a price-cone anchor. Only the DECLARATION has to match. A gate that could
        # not tell this from a stale file would push studies to stop committing them.
        put(tmp, "NCL", 10.0, 12.0, {"thing.json": {
            "base": {"central": 10.0},
            "give_back": {"central": 14.7},
            "alternative": {"central": 6.2},
            "published_central": 10.0, "published_spot": 12.0}})
        put_list(tmp, [])
    case("clean: alternatives that legitimately differ from the central",
         k_alternative, False, results)

    def k_listed(tmp):
        put(tmp, "NCL", 10.0, 12.0, {"thing.json": {"base": {"central": 10.0}}})
        put_list(tmp, ["NCL"])
    case("clean: a listed outstanding study", k_listed, False, results)

    def k_no_valuation(tmp):
        put(tmp, "NCL", 10.0, 12.0, {"notes.json": {"why": "prose only", "n": 3}})
        put_list(tmp, [])
    case("clean: an artefact carrying no valuation figure", k_no_valuation, False, results)

    # THE AMBIGUOUS KEY, BOTH WAYS [added 05-Sep-2026]. `end` is in VALUE_KEYS because a
    # bridge artefact carries its figure under that name, and three raw market-data
    # downloads in one study directory carry a UNIX TIMESTAMP under
    # chart.result[0].meta.currentTradingPeriod.regular.end. The gate demanded they
    # declare the fair value they were built against, which is a false accusation, and a
    # false accusation is the more expensive error [L-301]. Re-pointed to the ROOT rather
    # than widened, so both halves are tested: the deep one must NOT fire and the root
    # one must still fire.
    def k_deep_end(tmp):
        put(tmp, "NCL", 10.0, 12.0, {"yh_series.json": {"chart": {"result": [
            {"meta": {"symbol": "^TASI", "currentTradingPeriod": {
                "regular": {"start": 1786258800, "end": 1786276800}}}}]}}})
        put_list(tmp, [])
    case("clean: a market download whose deep `end` is a UNIX timestamp",
         k_deep_end, False, results)

    def k_root_end(tmp):
        put(tmp, "NCL", 10.0, 12.0,
            {"bridge.json": {"start": 8.0, "end": 9.5, "reviewer": "a name"}})
        put_list(tmp, [])
    case("a bridge whose ROOT `end` is a valuation figure and declares no vintage",
         k_root_end, True, results)

    # THIS CASE IS INVERTED, NOT DELETED [03-Sep-2026]. It asserted that a two-sided study
    # must NOT fire, on the reasoning that its branches are [R-GAP-01]'s business and this
    # gate must not invent a comparison. The reasoning was wrong in a way that mattered:
    # the gate skipped every two-sided study ENTIRELY, with a comment claiming the branches
    # were "handled by its branches" while nothing handled them, and EGCH's
    # contested_judgements.json sat stale at 1.7854 against a published 2.3109 for the whole
    # day. An artefact carrying a valuation figure must declare its vintage whether the
    # study publishes one answer or two.
    #
    # Keeping the case and flipping its expectation is the sharpest available evidence the
    # change took effect — the same discipline [R-GAP-01] recorded when its own one-sided
    # case was inverted. Deleting it would have left the change untested exactly where it
    # matters.
    def m_two_sided_undeclared(tmp):
        d = os.path.join(tmp, "engine", "ncl_study")
        os.makedirs(d, exist_ok=True)
        json.dump({"central": None, "spot": 14.41,
                   "central_two_sided": {"branches": [
                       {"label": "carried through", "value": 1.79,
                        "condition": "the programme is completed"},
                       {"label": "stopped", "value": 5.90,
                        "condition": "the programme is halted"}]}},
                  open(os.path.join(d, "study_numbers.json"), "w"), indent=1)
        json.dump({"base": {"central": 1.79}},
                  open(os.path.join(d, "thing.json"), "w"), indent=1)
        put_list(tmp, [])
    case("EGCH's shape: a two-sided study whose artefact declares no vintage",
         m_two_sided_undeclared, True, results)

    def k_two_sided_declared(tmp):
        """And the construction that must still pass: two-sided, and the artefact SAYS what
        it was built against."""
        d = os.path.join(tmp, "engine", "ncl_study")
        os.makedirs(d, exist_ok=True)
        json.dump({"central": None, "spot": 14.41,
                   "central_two_sided": {"branches": [
                       {"label": "carried through", "value": 1.79,
                        "condition": "the programme is completed"},
                       {"label": "stopped", "value": 5.90,
                        "condition": "the programme is halted"}]}},
                  open(os.path.join(d, "study_numbers.json"), "w"), indent=1)
        json.dump({"base": {"central": 1.79}, "published_central": 1.79,
                   "published_spot": 14.41},
                  open(os.path.join(d, "thing.json"), "w"), indent=1)
        put_list(tmp, [])
    case("clean: a two-sided study whose artefact declares its vintage",
         k_two_sided_declared, False, results)

    def m_unparseable_numbers(tmp):
        """An unreadable answer is not a clean answer [R-ENF-04] — this was a silent skip."""
        d = os.path.join(tmp, "engine", "ncl_study")
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "study_numbers.json"), "w").write("{not json,")
        json.dump({"base": {"central": 1.79}},
                  open(os.path.join(d, "thing.json"), "w"), indent=1)
        put_list(tmp, [])
    case("an unparseable study_numbers.json beside a valuation artefact",
         m_unparseable_numbers, True, results)

    def m_no_numbers_file(tmp):
        """Artefacts and no published answer to be current with — also a silent skip."""
        d = os.path.join(tmp, "engine", "ncl_study")
        os.makedirs(d, exist_ok=True)
        json.dump({"base": {"central": 1.79}},
                  open(os.path.join(d, "thing.json"), "w"), indent=1)
        put_list(tmp, [])
    case("valuation artefacts and no study_numbers.json at all",
         m_no_numbers_file, True, results)

    print("\n  %-62s %-6s %s" % ("condition", "ok", "gate said"))
    print("  " + "-" * 104)
    for n, ok, rc, line in results:
        print("  %-62s %-6s exit %d   %s" % (n, "ok" if ok else "WRONG", rc, line[:56]))
    bad = [r for r in results if not r[1]]
    print("\n%s" % ("All %d conditions behave as claimed." % len(results) if not bad
                    else "FAIL - %d condition(s) did not behave as claimed." % len(bad)))
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
