"""A CHECK NOBODY HAS SEEN FAIL IS NOT EVIDENCE.

Reinjects every condition scripts/check_lens_design.py claims to catch and
asserts the gate goes RED, plus clean cases that must NOT fire.

The headline case is PHDC's own architecture, exactly as it shipped on
30-Aug-2026: four lenses at typed weights of 45/15/20/20, three of them valuing
a developer on reported accounting earnings and historical-cost book, producing
a central 28% below a market its own cash-flow lens sat within 2.2% of.

    python3 scripts/check_lens_design_negative_control.py
"""
import json, os, shutil, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# THIS FIXTURE SUPPLIES ITS OWN POPULATION [06-09-2026]. The gate resolves the
# book through engine/study_population.py; this control runs it against a
# sandboxed tree holding studies it planted, which is the point of the control.
# The escape is explicit and the gate PRINTS that it took it, so a fixture
# population can never be mistaken for the real one.
_FIXTURE_ENV = dict(os.environ, TESTAHIL_FIXTURE_POPULATION='1')

GATE = os.path.join("scripts", "check_lens_design.py")

GOOD = {
    "class": "real-estate developer, off-plan, percentage-of-completion",
    "primary": {"kind": "dcf", "value": 14.54},
    "cross_checks": [
        {"kind": "relative_multiple", "value": 11.17,
         "multiple_source": "the multiples the shares have carried over five years of own history",
         "multiple": 6.20,
         "circularity": {"spot": 12.40, "shares": 2100.0, "net_debt": 4800.0,
                         "metric_value": 4900.0}},
        {"kind": "rnav", "value": 12.80,
         "note": "land at cost with a labelled market cross-check, absorption on the "
                 "company's own delivery rate, discounted on the schedule"},
        {"kind": "book_value", "value": 6.63, "present_value": False,
         "note": "a disclosed floor, published as such"},
    ],
    "envelope": {"low": 11.17, "high": 14.54},
    "central": 14.54,
}


def sandbox():
    tmp = tempfile.mkdtemp(prefix="lens_nc_")
    os.makedirs(os.path.join(tmp, "engine", "build_depth_audit"))
    os.makedirs(os.path.join(tmp, "scripts"))
    for f in ("research_protocol.py", "macro_path.py", "lessons_register.py"):
        shutil.copy(os.path.join(ROOT, "engine", f), os.path.join(tmp, "engine", f))
    shutil.copytree(os.path.join(ROOT, "engine", "macro_paths"),
                    os.path.join(tmp, "engine", "macro_paths"))
    shutil.copy(os.path.join(ROOT, "scripts", "check_lens_design.py"),
                os.path.join(tmp, "scripts", "check_lens_design.py"))
    return tmp


def put_study(tmp, ticker, record, raw=None, extra=None):
    d = os.path.join(tmp, "engine", "%s_study" % ticker.lower())
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, "study_numbers.json")
    if raw is not None:
        open(p, "w").write(raw); return
    doc = {"meta": {"ticker": ticker}}
    if record is not None:
        doc["lens_record"] = record
    # `extra` puts DOCUMENT-level keys beside the record — central_two_sided above
    # all — because the branch-wise identity clause is the one test that needs both
    # halves, and a fixture carrying only the record cannot express its failure.
    if extra:
        doc.update(extra)
    json.dump(doc, open(p, "w"), indent=1)


def put_list(tmp, tickers):
    json.dump({"why": "negative control", "adopted": "2026-09-02",
               "outstanding": sorted(tickers)},
              open(os.path.join(tmp, "engine", "build_depth_audit",
                                "lens_outstanding.json"), "w"), indent=1)


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
            rec = json.loads(json.dumps(GOOD)); mutate(rec)
            put_study(tmp, "NCL", rec); put_list(tmp, [])
        return build

    def m_phdc_as_shipped(r):
        # the architecture exactly as PHDC published it on 30-Aug-2026
        r["primary"] = {"kind": "dcf", "value": 14.86, "weight": 0.45}
        r["cross_checks"] = [
            {"kind": "book_value", "value": 6.56, "weight": 0.15},
            {"kind": "relative_multiple", "value": 11.17, "weight": 0.20,
             "multiple_source": "own history", "multiple": 6.20,
             "circularity": {"spot": 12.40, "shares": 2100.0, "net_debt": 4800.0,
                             "metric_value": 4900.0}},
            {"kind": "normalised_earnings", "value": 5.17, "weight": 0.20,
             "basis": "capitalised at the cost of equity"},
        ]
        r["central"] = 10.94

    def m_typed_weights(r):
        r["cross_checks"][0]["weight"] = 0.2

    def m_central_not_primary(r):
        r["central"] = 10.94

    def m_circular(r):
        r["cross_checks"][0]["multiple_source"] = "the multiple implied by the current price"

    def m_nominal_stasis(r):
        # a lens this class does not permit at all, added with the very basis
        # that made it useless: nominal stasis in a 15%-inflation currency
        r["cross_checks"].append({"kind": "normalised_earnings", "value": 5.17,
                                  "basis": "capitalised at the cost of equity"})
        r["envelope"] = {"low": 5.17, "high": 14.54}

    def m_book_weighted(r):
        r["cross_checks"][-1]["weight"] = 0.15

    def m_wrong_primary(r):
        r["primary"] = {"kind": "book_value", "value": 6.63}

    def m_unregistered_class(r):
        r["class"] = "widget assembler"

    def m_envelope(r):
        r["envelope"] = {"low": 2.0, "high": 40.0}

    def m_rnav_unevidenced(r):
        r["primary"] = {"kind": "rnav", "value": 14.54, "substitution_reason": "developer"}

    # ---- the string was the whole check [added 03-Sep-2026, AMOC re-strike] ----
    # AMOC's relative lens exactly as it shipped on 03-Sep-2026: the multiple is
    # (market cap + net debt) / base-year EBITDA -- the traded multiple, re-rated
    # by zero -- while the record says it comes "from the company's own history
    # and its regional peers, never a multiple read off the current price". The
    # prose check above reads that sentence, finds the reassuring words and
    # passes. What exposed it was the re-strike: the lens moved +51% when the
    # price moved +48%, which is what an anchored-on-price lens does and what an
    # anchored-on-history lens cannot do.
    AMOC_EBITDA = 2951.062
    AMOC_ND = -3001.5
    AMOC_SH = 1291.5
    AMOC_SPOT = 13.50
    AMOC_TRADED = (AMOC_SPOT * AMOC_SH + AMOC_ND) / AMOC_EBITDA

    def m_amoc_relative_as_shipped(r):
        r["cross_checks"][0] = {
            "kind": "relative_multiple", "value": 12.589,
            "multiple_source": "enterprise value to EBITDA from the company's own history "
                               "and its regional peers, never a multiple read off the "
                               "current price",
            "multiple": AMOC_TRADED,
            "circularity": {"spot": AMOC_SPOT, "shares": AMOC_SH,
                            "net_debt": AMOC_ND, "metric_value": AMOC_EBITDA}}

    def m_no_circularity_block(r):
        # the check switched off rather than passed: a source in prose, no numbers
        r["cross_checks"][0].pop("circularity", None)

    def m_no_multiple(r):
        r["cross_checks"][0].pop("multiple", None)

    def m_circularity_wont_divide(r):
        r["cross_checks"][0]["circularity"]["metric_value"] = 0.0

    for n, m in (("1 PHDC's architecture as shipped", m_phdc_as_shipped),
                 ("2 a typed weight on a cross-check", m_typed_weights),
                 ("3 central is not the primary", m_central_not_primary),
                 ("4 multiple taken from the price", m_circular),
                 ("5 nominal-stasis earnings power", m_nominal_stasis),
                 ("6 book value weighted", m_book_weighted),
                 ("7 wrong primary for the class", m_wrong_primary),
                 ("8 unregistered class", m_unregistered_class),
                 ("9 envelope invented around the central", m_envelope),
                 ("10 RNAV primary, disclosure unevidenced", m_rnav_unevidenced),
                 ("10a AMOC's relative lens as shipped -- the traded multiple",
                  m_amoc_relative_as_shipped),
                 ("10b no circularity block: the check switched off",
                  m_no_circularity_block),
                 ("10c the adopted multiple is not committed", m_no_multiple),
                 ("10d the circularity numbers do not divide", m_circularity_wont_divide)):
        case(n, broken(m), True, results)

    def b_norecord(tmp):
        put_study(tmp, "NCL", None); put_list(tmp, [])
    case("11 new study, no record, not listed", b_norecord, True, results)

    def b_unreadable(tmp):
        put_study(tmp, "NCL", None, raw="{nope"); put_list(tmp, [])
    case("12 numbers file will not parse", b_unreadable, True, results)

    def b_empty(tmp):
        put_list(tmp, ["GHOST"])
    case("13 empty population", b_empty, True, results)

    # ---- TWO-SIDED, added 06-09-2026 with the branch-wise identity clause -----
    # The clause it replaces was firing on work that was right: a study forbidden to
    # average its two framings has no scalar central, and demanding one demanded the
    # midpoint the dual-framing rule prohibits. These cases exist to prove the
    # replacement is HARDER, not looser — the flag must not become an opt-out.
    def _two_sided(branch_a=10.0, branch_b=14.0, **over):
        rec = json.loads(json.dumps(GOOD))
        rec.pop("central", None)
        rec["primary"].pop("value", None)
        rec["primary"]["two_sided"] = True
        rec["primary"]["branches"] = [
            {"label": "Frame A — the charge persists", "value": branch_a},
            {"label": "Frame B — the charge normalises", "value": branch_b}]
        # the range and the envelope move WITH the branches, and range_basis is kept
        # from GOOD: a fixture that drops an unrelated required field tests that field
        # rather than the clause it was written for, and would report the clean case
        # red for the wrong reason [R-ENF-07]
        lo, hi = min(branch_a, branch_b), max(branch_a, branch_b)
        rec["primary"]["range"] = {"low": lo, "high": hi}
        # a range needs its origin declared whatever else is true of the record, so the
        # fixture supplies one — otherwise the clean case goes red on range_basis and
        # proves nothing about the clause it was written for
        rec["primary"]["range_basis"] = {
            "driver": "the provision charge, across the two framings the filings support",
            "evidence": "the two framings are the company's own disclosed charge and its "
                        "own five-year average; nothing between them is invented",
            "low": lo, "high": hi, "macro_held": True}
        if isinstance(rec.get("envelope"), dict):
            rec["envelope"] = {"low": lo, "high": hi}
        rec["primary"].update(over)
        return rec

    def _published(a=10.0, b=14.0):
        return {"central_two_sided": {"branches": [
            {"label": "Frame A — the charge persists", "value": a},
            {"label": "Frame B — the charge normalises", "value": b}]}}

    def b_ts_no_branches(tmp):
        rec = _two_sided(); rec["primary"]["branches"] = []
        put_study(tmp, "NCL", rec, extra=_published()); put_list(tmp, [])
    case("14 two_sided declared with NO branches — the opt-out", b_ts_no_branches, True, results)

    def b_ts_mismatch(tmp):
        put_study(tmp, "NCL", _two_sided(10.0, 14.0),
                  extra=_published(10.0, 19.0)); put_list(tmp, [])
    case("15 record's branches are not the branches published", b_ts_mismatch, True, results)

    def b_ts_scalar(tmp):
        rec = _two_sided(); rec["primary"]["value"] = 10.0
        put_study(tmp, "NCL", rec, extra=_published()); put_list(tmp, [])
    case("16 two_sided AND a scalar value beside the branches", b_ts_scalar, True, results)

    def b_ts_central(tmp):
        rec = _two_sided(); rec["central"] = 12.0
        put_study(tmp, "NCL", rec, extra=_published()); put_list(tmp, [])
    case("17 two_sided AND a record central — the midpoint by the back door",
         b_ts_central, True, results)

    def b_ts_identical(tmp):
        put_study(tmp, "NCL", _two_sided(10.0, 10.0),
                  extra=_published(10.0, 10.0)); put_list(tmp, [])
    case("18 two branches carrying the same value", b_ts_identical, True, results)

    def b_ts_unlabelled(tmp):
        rec = _two_sided(); rec["primary"]["branches"][1]["label"] = "  "
        put_study(tmp, "NCL", rec, extra=_published()); put_list(tmp, [])
    case("19 a branch with no label", b_ts_unlabelled, True, results)

    def b_ts_range_excludes(tmp):
        rec = _two_sided(10.0, 14.0)
        rec["primary"]["range"] = {"low": 10.5, "high": 13.0}
        put_study(tmp, "NCL", rec, extra=_published()); put_list(tmp, [])
    case("21 the primary's range does not contain its own branches",
         b_ts_range_excludes, True, results)

    def b_pub_ts_rec_single(tmp):
        # BOROUGE exactly as it shipped: the document publishes two branches and the
        # record names ONE of them as the answer. Caught live, on no ratchet.
        put_study(tmp, "NCL", GOOD, extra=_published()); put_list(tmp, [])
    case("20 study publishes two branches, record declares a single-sided primary",
         b_pub_ts_rec_single, True, results)

    # ---- clean ------------------------------------------------------------
    def c_two_sided(tmp):
        put_study(tmp, "NCL", _two_sided(), extra=_published()); put_list(tmp, [])
    case("clean: a two-sided record whose branches ARE the published branches",
         c_two_sided, False, results)

    def c_good(tmp):
        put_study(tmp, "NCL", GOOD); put_list(tmp, [])
    case("clean: primary central, cross-checks", c_good, False, results)

    def c_listed(tmp):
        rec = json.loads(json.dumps(GOOD)); m_phdc_as_shipped(rec)
        put_study(tmp, "NCL", rec); put_list(tmp, ["NCL"])
    case("clean: a listed outstanding study", c_listed, False, results)

    def c_rnav(tmp):
        rec = json.loads(json.dumps(GOOD))
        rec["cross_checks"] = [c for c in rec["cross_checks"] if c["kind"] != "rnav"]
        rec["cross_checks"].append({"kind": "dcf", "value": 14.54})
        rec["envelope"] = {"low": 11.17, "high": 14.54}
        rec["central"] = 14.54
        rec["primary"] = {"kind": "rnav", "value": 14.54,
                          "substitution_reason": "the land bank is disclosed by project and a "
                                                 "transaction establishes its value per acre",
                          "disclosure_evidence": [
                              "disclosed land area by project",
                              "a sourced land value per unit of area, or a transaction that establishes one",
                              "the company's own delivery or absorption rate"]}
        put_study(tmp, "NCL", rec); put_list(tmp, [])
    case("clean: RNAV primary, fully evidenced", c_rnav, False, results)

    def c_own_history_multiple(tmp):
        # THE CASE THIS MUST NOT BREAK: a multiple genuinely from own history,
        # committed beside the three numbers that reproduce the traded one, and
        # standing clear of it. A gate that could not tell this from AMOC's
        # would push studies to hide the ingredients, which is the opposite of
        # what it measures.
        rec = json.loads(json.dumps(GOOD))
        rec["cross_checks"][0] = {
            "kind": "relative_multiple", "value": 9.80,
            "multiple_source": "the median enterprise-value-to-EBITDA multiple the "
                               "company's own shares carried at each of the last five "
                               "fiscal year ends",
            "multiple": 4.10,
            "circularity": {"spot": 12.40, "shares": 2100.0, "net_debt": 4800.0,
                            "metric_value": 4900.0}}
        rec["envelope"] = {"low": 9.80, "high": 14.54}
        put_study(tmp, "NCL", rec); put_list(tmp, [])
    case("clean: an own-history multiple clear of the traded one",
         c_own_history_multiple, False, results)

    def c_bank(tmp):
        rec = {"class": "bank",
               "primary": {"kind": "ddm", "value": 20.0},
               "cross_checks": [{"kind": "residual_income", "value": 22.0},
                                {"kind": "book_value", "value": 15.0, "present_value": False}],
               "envelope": {"low": 20.0, "high": 22.0}, "central": 20.0}
        put_study(tmp, "NCL", rec); put_list(tmp, [])
    case("clean: a bank on dividends and residual income", c_bank, False, results)

    # ---- the origin of the bear and the bull [per instruction, 03-Sep-2026] ----
    # ARCC'S CONSTRUCTION EXACTLY AS IT SHIPPED is the headline case, the way PHDC's
    # blend is the headline case above: the range built by moving the discount rate
    # and terminal growth together. Both carry the same terminal inflation under
    # [R-MACRO-01], so the corners published as bear and bull are the two least
    # coherent cells in the grid, and its own note calls it "never a spread invented
    # around the answer" -- a cautious label on the construction it disclaims.
    RANGE = {"low": 3.76, "high": 44.85}

    def m_range_no_basis(r):
        r["primary"]["range"] = dict(RANGE)
        r["primary"].pop("range_basis", None)

    def m_arcc_as_shipped(r):
        r["primary"]["range"] = dict(RANGE)
        r["primary"]["range_basis"] = {
            "driver": "the discount rate and the terminal growth moved together",
            "low": 47.78, "high": 59.33, "macro_held": True,
            "evidence": "the cash-flow lens across its own crux, on one clock, never a "
                        "spread invented around the answer"}

    def m_amoc_as_shipped(r):
        r["primary"]["range"] = dict(RANGE)
        r["primary"]["range_basis"] = {
            "driver": "five simultaneous driver moves - volume, margin, currency, cost "
                      "of capital and terminal growth",
            "low": 4.93, "high": 16.73, "macro_held": True,
            "evidence": "joint-worst and joint-best, not a confidence interval"}

    def m_range_macro_moved(r):
        r["primary"]["range"] = dict(RANGE)
        r["primary"]["range_basis"] = {
            "driver": "cash conversion", "low": 0.039, "high": 0.179,
            "evidence": "the company's own filed cash-flow statements",
            "macro_held": False}

    def m_range_no_evidence(r):
        r["primary"]["range"] = dict(RANGE)
        r["primary"]["range_basis"] = {
            "driver": "cash conversion", "low": 0.039, "high": 0.179,
            "macro_held": True, "evidence": "   "}

    def m_range_no_endpoints(r):
        r["primary"]["range"] = dict(RANGE)
        r["primary"]["range_basis"] = {
            "driver": "cash conversion", "macro_held": True,
            "evidence": "the company's own filed cash-flow statements"}

    case("range published with no declared origin", broken(m_range_no_basis), True, results)
    case("ARCC as shipped: discount rate x terminal growth",
         broken(m_arcc_as_shipped), True, results)
    case("AMOC as shipped: five moves incl. cost of capital",
         broken(m_amoc_as_shipped), True, results)
    case("range where the macro path moved too", broken(m_range_macro_moved), True, results)
    case("range basis with no evidence", broken(m_range_no_evidence), True, results)
    case("range basis with no endpoint values", broken(m_range_no_endpoints), True, results)

    # AND THE TWO CLEAN CASES, because a gate that reddens on a legitimate
    # construction teaches studies to stop publishing ranges at all.
    def c_business_crux(tmp):
        rec = json.loads(json.dumps(GOOD))
        rec["primary"]["range"] = dict(RANGE)
        rec["primary"]["range_basis"] = {
            "driver": "cash conversion - the rate at which contracted sales become "
                      "operating cash",
            "low": 0.0394, "high": 0.1787, "macro_held": True,
            "evidence": "the full observed span of that rate in the company's own filed "
                        "cash-flow statements"}
        rec["envelope"] = {"low": RANGE["low"], "high": RANGE["high"]}
        put_study(tmp, "NCL", rec); put_list(tmp, [])

    def c_sanctioned_framing(tmp):
        rec = json.loads(json.dumps(GOOD))
        rec["primary"]["range"] = dict(RANGE)
        rec["primary"]["range_basis"] = {
            "driver": "two readings of the crux crossed with the two published "
                      "equity-risk-premium bases",
            "low": 63.70, "high": 123.03, "macro_held": True,
            "evidence": "the four cases published side by side",
            "sanctioned_framing": "[R-COC-01] - both premium bases are published and one "
                                  "is named central"}
        rec["envelope"] = {"low": RANGE["low"], "high": RANGE["high"]}
        put_study(tmp, "NCL", rec); put_list(tmp, [])

    case("clean: range from a business crux on filed evidence",
         c_business_crux, False, results)
    case("clean: a framing [R-COC-01] requires both ways",
         c_sanctioned_framing, False, results)

    print("\nNEGATIVE CONTROL — scripts/check_lens_design.py")
    for name, ok, rc, last in results:
        print("  %-40s %-4s exit %d   %s" % (name, "ok" if ok else "MISS", rc, last[:66]))
    bad = [n for n, ok, _, _ in results if not ok]
    if bad:
        print("\nFAILED on: %s" % ", ".join(bad)); return 1
    print("\nAll %d conditions behave as claimed." % len(results))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
