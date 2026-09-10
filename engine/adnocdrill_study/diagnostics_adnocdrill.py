#!/usr/bin/env python3
"""ADNOCDRILL — the output records [R-ENF-05], GENERATED.

TWO INSTRUMENTS, both aimed at a house that leans one way and cannot see it because
every individual choice was defensible.

THE REVERSE READ. Every study states what IT believes and almost none states what the
PRICE believes, and the two are the same model read backwards. This solves the group
EBITDA margin the traded price implies under this study's own drivers, holding every
other driver at its published value, so a reader can judge the DISAGREEMENT rather
than the conclusion.

THE HARD PART IS KEEPING IT OUT OF THE MODEL AND THE RULE IS STRUCTURAL, NOT
REMEMBERED. It lives here and in diagnostics.json, NEVER in study_numbers.json, and
assert_reverse_dcf() refuses any study whose builders read that file back in: a
quantity solved from a price and re-entering the valuation is the reverse-engineered
rate the cost-of-capital procedure prohibits outright, arriving through a side door.
Nothing this file writes is an input to anything. The last assert below checks that
the solved value is absent from the numbers file every builder reads, which is the
half of the rule a leak test cannot see.

THE SIGN TEST. Any single contested choice is defensible; what is not is a study
resolving EVERY one the same way and never noticing. Each fork is valued BOTH WAYS by
re-running this study's own compute.py end to end with ONE thing changed, and a
binomial sign test is printed. A study landing them all one way is FLAGGED, never
failed — a company can genuinely deserve a consistent read.

HOW THE ALTERNATIVES ARE VALUED, AND WHY IT IS A RE-RUN RATHER THAN A RESTATEMENT.
V(k) is the only accessor for an input in compute.py (INP[ appears nowhere else in
that file), so an input override is a one-line patch of V's body and every downstream
figure re-derives through the study's own code — the bridge, the asserts, the lens
set and the weights included. Forks that are not inputs are applied as single source
substitutions, each asserted to have landed exactly once, so a substitution that
stopped matching after an edit FAILS rather than silently valuing nothing. Running
with no override at all must reproduce the published answer to the last digit, and
that is asserted first: a harness that cannot reproduce the study is measuring
something else.

NOTHING HERE CHANGES A DRIVER, A FORECAST, A RATE OR A FAIR VALUE. Valuing the other
framing of a judgement is a calculation reported, never a change made.
"""
import json
import os
import sys
from math import comb

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = open(os.path.join(HERE, "compute.py"), encoding="utf-8").read()
NUMBERS = os.path.join(HERE, "study_numbers.json")

V_OLD = "def V(k):\n    return INP[k]['value']"
V_NEW = "def V(k):\n    return _OV[k] if k in _OV else INP[k]['value']"

# The study's own record-consistency assert describes the shape of the CALIBRATED
# forecast. A counterfactual that removes the calibration makes that NOTE wrong, not
# the arithmetic, so it is neutralised for that one variant and the fact is recorded
# in the entry rather than left for a reader to discover.
NOTE_ASSERT = ("assert _FA_PATH_A[0] < min(_FA_FILED), ('the forecast no longer opens below "
               "every filed period; '\n                                        'the note below "
               "says it does', _FA_PATH_A[0], _FA_FILED)")
NEUTRALISED = "pass  # record-note assert neutralised for this counterfactual only"

LATEST_PRICE = 5.80
LATEST_PRICE_DATE = "close 3 September 2026, engine/prices/SUPPLIED_03-09-2026.json"


def run(overrides=None, subs=()):
    """Re-run this study's own compute.py with ONE thing changed."""
    src = SRC.replace(V_OLD, V_NEW)
    assert src != SRC, "the input accessor could not be patched"
    for old, new in subs:
        n = src.count(old)
        assert n == 1, "substitution did not land exactly once (%d): %r" % (n, old[:70])
        src = src.replace(old, new)
    g = {"__name__": "_variant", "__file__": os.path.join(HERE, "compute.py"),
         "_OV": dict(overrides or {})}
    sys.path.insert(0, HERE)
    sys.path.insert(0, os.path.dirname(HERE))
    exec(compile(src, os.path.join(HERE, "compute.py"), "exec"), g)
    return g


def blend(g):
    return sum(g["FAIR"][k] * g["LENS_WEIGHT"][k] for k in g["FAIR"])


def solve(f, lo, hi, target, it=300):
    flo = f(lo) - target
    if (f(hi) - target) * flo > 0:
        return None
    for _ in range(it):
        mid = (lo + hi) / 2.0
        fm = f(mid) - target
        if flo * fm <= 0:
            hi = mid
        else:
            lo, flo = mid, fm
    return (lo + hi) / 2.0


def sign_test(signs):
    n = len([s for s in signs if s])
    k = len([s for s in signs if s > 0])
    if not n:
        return n, k, None
    tail = sum(comb(n, i) for i in range(max(k, n - k), n + 1)) / float(2 ** n)
    return n, k, min(1.0, 2 * tail)


def main():
    base = run()
    C = base
    published = blend(base)
    committed = json.load(open(NUMBERS, encoding="utf-8"))
    assert abs(published - committed["central"]) < 1e-12, (
        "the harness does not reproduce the published central; it is measuring something else")
    F0 = dict(base["FAIR"])
    spot_strike = base["V"]("spot_aed")

    # ------------------------------------------------------------------ THE REVERSE READ
    # Solved on the study's OWN published sensitivity axis: a level shift in points of
    # revenue on the EBITDA the model discounts, which is what revalue(margin_shift=)
    # does and what section 1.9 publishes. Everything else is held at its published
    # value. The margin is chosen over the discount rate because it is the one quantity
    # in this model a reader can check against the company's own filings.
    rev = base["revalue"]
    shift, implied, study_margin = {}, {}, {}
    for case in ("A", "B"):
        s = solve(lambda x, c=case: rev(margin_shift=x, case=c), -0.30, 0.30, LATEST_PRICE)
        m = base["CASE"][case]["rows"][-1]["ebitda_margin"]
        shift[case], study_margin[case], implied[case] = s, m, m + s
    # the other quantities the same model yields, published beside it so that the choice
    # of quantity is visible rather than asserted
    also = {}
    we = C["mkt_cap"] / (C["mkt_cap"] + C["gross_debt_now"])
    wd = 1 - we

    def wacc_at_beta(b):
        return we * (C["rf_star"] + b * C["V"]("erp_rating")) + wd * C["kd_after_tax"]

    def val_at_terminal_roic(roic, case):
        rows, g_, w = C["CASE"][case]["rows"], C["TERMINAL_G"][case], C["WACC"]
        pv = sum(r["fcff"] / (1 + w) ** n for n, r in enumerate(rows, start=1))
        tv = rows[-1]["nopat"] * (1 + g_) * (1 - g_ / roic) / (w - g_)
        ev = pv + tv / (1 + w) ** len(rows)
        return C["bridge"](ev * (1 + w) ** C["STUB_YEARS"]
                           - C["FCFF_1H26"] * (1 + w) ** (C["STUB_YEARS"] / 2))

    for case in ("A", "B"):
        assert abs(val_at_terminal_roic(C["V"]("terminal_roic"), case)
                   - F0["dcf_" + case]) < 1e-9, "the terminal re-solve does not reproduce the lens"
        also["flat_cost_of_capital_" + case] = solve(
            lambda x, c=case: rev(wacc=x, case=c), 0.03, 0.30, LATEST_PRICE)
        also["terminal_nominal_growth_" + case] = solve(
            lambda x, c=case: rev(g=x, case=c), -0.05, C["WACC"] - 0.001, LATEST_PRICE)
        also["equity_beta_" + case] = solve(
            lambda x, c=case: rev(wacc=wacc_at_beta(x), case=c), 0.05, 3.0, LATEST_PRICE)
        also["terminal_return_on_capital_" + case] = solve(
            lambda x, c=case: val_at_terminal_roic(x, c), 0.03, 5.0, LATEST_PRICE)

    filed = {"FY%d" % y: C["H"][y]["ebitda"] / C["H"][y]["revenue"] for y in (2023, 2024, 2025)}
    filed["1H2026_reviewed"] = C["V"]("ebitda_1h26") / C["V"]("rev_1h26")
    guided26 = (C["V"]("g26_ebitda_lo") + C["V"]("g26_ebitda_hi")) / 2 / C["V"]("g26_revenue")

    diagnostics = {
        "ticker": "ADNOCDRILL",
        "as_of": committed["meta"]["study_date"],
        "spot": LATEST_PRICE,
        "spot_date": LATEST_PRICE_DATE,
        "spot_at_strike": spot_strike,
        # [R-ENF-06]: the answer this diagnostic was generated against
        "published_central": published,
        "published_spot": spot_strike,
        "why_this_file": (
            "The reverse read — what the traded price must believe — is a DIAGNOSTIC and "
            "lives outside the numbers file every builder reads. A margin, growth or rate "
            "solved from a price and then used anywhere in the valuation is the "
            "reverse-engineered terminal the cost-of-capital procedure prohibits outright, "
            "arriving through a side door. Nothing in this file is an input to anything: no "
            "builder reads it, and the generator asserts that the solved value is absent "
            "from study_numbers.json."),
        "implied": {
            "quantity": ("the group EBITDA margin the traded price implies, as a level shift "
                         "in points of revenue on this study's own forecast margin path, "
                         "reported at the last explicit year (FY2030)"),
            "value": implied["A"],
            "value_other_framing": implied["B"],
            "study_value": study_margin["A"],
            "study_value_other_framing": study_margin["B"],
            "level_shift_points_of_revenue": {"A": shift["A"], "B": shift["B"]},
            "solved_on": (
                "this study's own model through compute.revalue(margin_shift=...), the "
                "sensitivity axis the study itself publishes — holding every driver, the "
                "fleet plan, the cost stack, the cost of capital, the terminal and the "
                "enterprise-to-equity bridge at their published values and varying only the "
                "EBITDA margin until the cash-flow lens reproduces the traded price, on each "
                "of the two framings of the crux"),
            "company_disclosed": {
                "filed_group_ebitda_margin": filed,
                "guided_fy2026_midpoint": guided26,
                "note": ("audited consolidated statements FY2023-25 and the reviewed 1H-2026 "
                         "condensed interim; the FY2026 figure is the midpoint of the "
                         "company's own reaffirmed EBITDA guidance over its own reaffirmed "
                         "revenue guidance"),
            },
            "reading": (
                "At AED %.2f the price is paying for an FY2030 group EBITDA margin of %.1f%% "
                "on the continued-expansion framing and %.1f%% on the capacity-plateau "
                "framing, against this study's own forecasts of %.1f%% and %.1f%%. THE PRICE "
                "SITS BETWEEN THE TWO FRAMINGS, so the disagreement changes sign depending on "
                "which future a reader holds: on the expansion case the market is %.1f points "
                "BELOW this study, on the plateau case %.1f points ABOVE it. Neither implied "
                "figure is a belief the filings rule out, and the arithmetic is stated exactly "
                "rather than rounded in this study's favour: the company has filed %.1f%%, "
                "%.1f%% and %.1f%% for FY2023, FY2024 and FY2025 and %.1f%% for the reviewed "
                "first half of 2026, and guides %.1f%% for the full year — so the expansion "
                "framing's implied %.2f%% sits %.0f basis points BELOW the weakest half-year "
                "this company has filed and the plateau framing's implied %.2f%% sits %.0f "
                "basis points ABOVE its best full year. Both are just outside a four-period "
                "record rather than inside it, and both are inside a rounding of it. A reverse "
                "read landing on a believable number is evidence against a dissent rather than "
                "for one. The disagreement is two points of margin on a driver a reader can "
                "check in the next filing, which is a more useful statement than \"the study "
                "is %.1f%% below the price\"."
                % (LATEST_PRICE, 100 * implied["A"], 100 * implied["B"],
                   100 * study_margin["A"], 100 * study_margin["B"],
                   100 * (study_margin["A"] - implied["A"]),
                   100 * (implied["B"] - study_margin["B"]),
                   100 * filed["FY2023"], 100 * filed["FY2024"], 100 * filed["FY2025"],
                   100 * filed["1H2026_reviewed"], 100 * guided26,
                   100 * implied["A"], 10000 * (min(filed.values()) - implied["A"]),
                   100 * implied["B"], 10000 * (implied["B"] - max(filed.values())),
                   100 * abs(published / LATEST_PRICE - 1))),
        },
        "also_solved_on_the_same_model": also,
        "also_solved_note": (
            "Every quantity the same model yields at the same price, published so that the "
            "choice of ONE quantity above is visible rather than asserted. The margin is the "
            "one reported as the reverse read because it is the only one of the five with a "
            "comparator in the company's own filings; the beta has one in this study's own "
            "regression record (adopted 0.795 five-year weekly, with its own two-, three- and "
            "four-year windows at 0.890, 1.025 and 0.836 and a 90% interval of 0.577 to "
            "1.014), and the terminal return on capital is UNREACHABLE on the plateau framing "
            "because that framing sits below the price at any return."),
    }

    # ------------------------------------------------------- THE CONTESTED JUDGEMENTS
    # Each entry is valued by re-running the model with that one fork flipped. `value_adopted`
    # is the study's PUBLISHED answer — the five-lens weighted central, which is what a reader
    # receives and what the gap reader reads — so materiality is measured against the answer
    # rather than against the lens a judgement happens to govern.
    def flip(overrides=None, subs=()):
        return blend(run(overrides, subs))

    J = []

    # the two lens-specific forks are run first, because the note below states how far each
    # moves ITS OWN lens as well as the published answer and neither figure may be typed:
    # a number stated in prose is computed or it is not stated.
    _book_g = run(subs=[("roe_sustainable = roe_forecast_2030",
                         "roe_sustainable = float(roe_historical)")])
    _norm_g = run(subs=[("norm_rate = WACC                      # no growth credited means no g "
                         "in the denominator",
                         "norm_rate = WACC - 0.020              # Fisher-consistent alternative")])
    _book_alt, _norm_alt = blend(_book_g), blend(_norm_g)
    _book_lens_share = abs(F0["book"] - _book_g["FAIR"]["book"]) / _book_g["FAIR"]["book"]
    _norm_lens_share = (abs(F0["normalised"] - _norm_g["FAIR"]["normalised"])
                        / _norm_g["FAIR"]["normalised"])
    _book_answer_share = abs(published - _book_alt) / _book_alt
    _norm_answer_share = abs(published - _norm_alt) / _norm_alt

    def J_(name, adopted, alternative, value_alt, why, **extra):
        row = dict(name=name, adopted=adopted, alternative=alternative,
                   value_adopted=published, value_alternative=value_alt, why=why)
        row["move_from_alternative_to_adopted"] = published - value_alt
        row["share_of_published_answer"] = abs(published - value_alt) / abs(value_alt)
        row.update(extra)
        J.append(row)

    prim_mid = (F0["dcf_A"] + F0["dcf_B"]) / 2
    J_("the central architecture",
       "the five-lens weighted blend the study publishes (0.25/0.25/0.20/0.15/0.15)",
       "the class primary alone — the cash-flow lens, at the study's own equal weighting "
       "of its two framings",
       prim_mid,
       "an operating company's class primary is the discounted cash flow, and the other "
       "lenses are cross-checks published beside it rather than weights averaged into it. "
       "Three of the five lenses carrying half the weight here value a 44%%-margin franchise "
       "on historical-cost book, on trailing peer multiples struck partly off loss-making "
       "land drillers, and on flat nominal earnings capitalised at a nominal rate. The "
       "weights were typed and have never cleared an out-of-sample test. This is the largest "
       "single judgement in the study and it is the one the two cash-flow framings expose: "
       "they straddle the traded price and their midpoint lands %.2f%% from it, while "
       "the blend sits %.1f%% below."
       % (100 * abs(prim_mid / LATEST_PRICE - 1), 100 * (1 - published / LATEST_PRICE)),
       lens_values=F0)

    _BETAS = {"weekly_2y": 0.8898089280137128, "weekly_3y": 1.0245736478865013,
              "weekly_4y": 0.8358415790193425, "monthly_5y": 0.47099338076868474}
    _beta_alt = {k: flip({"beta_raw": v}) for k, v in _BETAS.items()}
    J_("the beta estimate",
       "the five-year WEEKLY own-stock regression against the published index, 0.795",
       "the study's own three-year weekly regression against the same index, 1.025",
       _beta_alt["weekly_3y"],
       "THE DIRECTION OF THIS ENTRY IS NOT ROBUST TO THE ALTERNATIVE CHOSEN, AND THAT IS "
       "RECORDED HERE RATHER THAN SETTLED BY PICKING ONE. The protocol's first tier is a "
       "two-to-five-year own-stock weekly OR MONTHLY regression on the longest usable window, "
       "and this study ran four alternatives that all clear the usability gate. Three are "
       "weekly and all three sit ABOVE the adopted beta — two-year %.3f (answer %.4f), "
       "three-year %.3f (answer %.4f), four-year %.3f (answer %.4f) — so against any of them "
       "the study took the higher-value side. The fourth is the five-year MONTHLY regression "
       "at %.3f, which sits far BELOW it and gives %.4f: against that one the study took the "
       "LOWER-value side, by %.1f%%, which is the largest single move in this whole record. A "
       "window alternative is recorded as the framing because the adopted choice is a WINDOW "
       "choice at the study's own stated frequency, and the sign test is printed BOTH WAYS "
       "below so the reader is not asked to take that on trust. Beta is the single most "
       "powerful driver in the model and the only input estimated from market data rather than "
       "read from a filing."
       % (_BETAS["weekly_2y"], _beta_alt["weekly_2y"], _BETAS["weekly_3y"],
          _beta_alt["weekly_3y"], _BETAS["weekly_4y"], _beta_alt["weekly_4y"],
          _BETAS["monthly_5y"], _beta_alt["monthly_5y"],
          100 * abs(published - _beta_alt["monthly_5y"]) / _beta_alt["monthly_5y"]),
       alternatives_tested={k: {"beta": _BETAS[k], "answer": _beta_alt[k]} for k in _BETAS},
       direction_not_robust=True)

    J_("the risk-free basis",
       "the US ten-year yield of 4.69% normalised by the United States' own default spread "
       "of 0.23%, giving 4.46%, on the argument that the cash flows are dollars",
       "the house market path's AED anchor — the UAE federal AED Treasury Bond auction yield "
       "of 4.48% less its own rating-basis default spread of 0.42%, giving 4.06%",
       flip({"ust10": 0.0448, "us_default_spread": 0.0042}),
       "both constructions count country risk exactly once and strip the same basis of "
       "default spread as the equity premium adds back, so neither double-counts; they differ "
       "in WHICH instrument the risk-free is measured on. The house anchor measures the "
       "risk-free and the spread on the SAME instrument, which is the construction that keeps "
       "country risk entering once by arithmetic rather than by argument. The caveat runs the "
       "other way and is stated rather than buried: the house anchor's own source note records "
       "that the AED federal instrument is an approximately FIVE-year tenor, against the "
       "study's TEN-year US Treasury, so part of the 40-basis-point difference between the two "
       "normalised risk-free rates is tenor rather than basis and this fork is smaller than "
       "those two numbers make it look. HOW MUCH SMALLER IS NOT QUANTIFIED HERE, because no "
       "like-tenor AED figure is committed in this study or in the house path, and estimating "
       "one to finish the sentence would be inventing the very number the entry is about.")

    J_("the terminal capitalisation rate",
       "the weighted cost of capital, on the argument that the capital structure weights are "
       "struck on gross debt and a firm holding cash alongside undiminished gross borrowings "
       "has not de-levered",
       "the cost of equity, on the argument that the model's own 2030 balance sheet has the "
       "firm in net cash",
       flip(subs=[("    terminal_rate = WACC", "    terminal_rate = ke_rating")]),
       "this study implemented the alternative, priced it, and REVERSED it — recorded in its "
       "own code beside the line. Two reasons are given and the second is the stronger: "
       "reading the terminal capital structure off NET debt after refusing to read today's "
       "off net debt treats one quantity two ways in one model; and a rate that switches on "
       "the SIGN of terminal net debt is discontinuous, which a driver test caught when a "
       "HEAVIER working-capital burden made the company more valuable. The reversal raises "
       "the answer, which is why it is recorded here rather than only in the code.")

    J_("the book lens' sustainable return",
       "the return the model itself forecasts for 2030, 30.6%",
       "the realised FY2024-25 average the first edition used, 36.7%",
       _book_alt,
       "a return entering a perpetual formula has to be one the business can be held to in "
       "perpetuity, and this study already forecasts exactly that — falling as the capital "
       "base grows into the fleet being built. Using the realised return would make the book "
       "lens richer than the cash-flow model four sections above it on nothing more than the "
       "past having been measured on a smaller balance sheet. The average across the forecast "
       "window, 32.2%, sits between the two and is published beside them.")

    J_("the normalised lens' capitalisation",
       "flat nominal profit capitalised at the nominal cost of capital, with no growth "
       "credited in the denominator",
       "a Fisher-consistent reading — a real rate on flat real earnings, the nominal rate "
       "less the house terminal inflation of 2.0%",
       _norm_alt,
       "holding earnings flat in NOMINAL terms while discounting at a NOMINAL rate is a "
       "perpetual real decline of about two points a year, not prudence, and nothing "
       "disclosed supports one for a fleet on multi-year contracts with an explicit fuel "
       "escalation pass-through. The adopted construction was itself a correction — an "
       "earlier edition divided by the rate less a growth rate while the text beside it said "
       "no growth was credited — and it corrected the arithmetic without reaching the unit.")

    J_("the segment calibration",
       "the unit build reconciled to the company's own FY2026 segment guidance, as persistent "
       "level shifts of 0.900, 1.025 and 1.080 on the three segments' unit rates",
       "the raw ground-up build, uncalibrated",
       flip(subs=[("CASE = {c: build_case(c, CALIB) for c in ('A', 'B')}",
                   "CALIB = dict(onshore=1.0, offshore=1.0, ofs=1.0)\n"
                   "CASE = {c: build_case(c, CALIB) for c in ('A', 'B')}"),
                  (NOTE_ASSERT, NEUTRALISED)]),
       "guidance is scored and never consumed, because management's forward targets lean the "
       "same way an optimistic model does — and this year consumes it, which the study says "
       "in terms. It runs AGAINST the value here rather than for it: the raw build totals "
       "5,086mn against a guided 5,000mn, so consuming the guidance cuts the anchor year and "
       "every year after it through a persistent level shift. The guidance is also rounded to "
       "one decimal, so the shifts are solved against roundings. The study's own "
       "forecast-anchor note describes the calibrated path, so it was neutralised for this "
       "counterfactual — the note is what stops being true, not the arithmetic.")

    J_("the cost and day-rate escalators",
       "1.5% on the oilfield-services, general and day-rate lines, sourced to this study's "
       "own consumer-price and producer-price reads",
       "2.0% on the same lines, the house market path's published inflation ladder",
       flip({"esc_oilfield": 0.020, "esc_general": 0.020, "esc_dayrate": 0.020}),
       "one escalator per driver class is the rule and this study obeys it — wages already "
       "sit at 2.0% and fuel escalates on its own commodity path, so neither moves here. What "
       "is contested is the level on the domestic lines. Raising revenue and the domestic "
       "cost lines together RAISES the answer, so the adopted 1.5% is the lower-value side; "
       "the study's own reasoning for it is explicit and the gap is flagged rather than "
       "smoothed away.")

    J_("the relative lens' earnings base",
       "trailing last-twelve-month EBITDA of 2,173mn excluding the joint-venture share",
       "the company's own guided FY2026 EBITDA midpoint of 2,250mn",
       flip(subs=[("rel_ev = blended_multiple * ltm_ebitda_ex_jv",
                   "rel_ev = blended_multiple * ebitda_fy26")]),
       "every multiple in the peer table is an enterprise value struck today over that "
       "company's last twelve months, so applying it to a guided forward figure would credit "
       "this company with a year of growth no peer in the denominator is credited with. The "
       "adopted basis is the internally consistent one and it is also the lower one, which is "
       "why it is recorded here rather than treated as merely mechanical.")

    J_("the working-capital ratio",
       "9.008% of revenue, off the 30 June 2026 balance sheet — the only one that "
       "consolidates the two regional acquisitions",
       "5.913% of revenue, the FY2023-25 audited average the first edition used",
       flip(subs=[("        wc = revenue * WC_PCT_REVENUE\n",
                   "        wc = revenue * WC_PCT_REVENUE_HIST\n")]),
       "the audited average is built entirely from year ends that PRE-DATE the acquisitions "
       "and was being applied to a revenue line that consolidates them from 2026, which is an "
       "internal inconsistency. The mid-year objection was tested against the company's own "
       "cash-flow statement and answered: working capital RELEASED 154mn over 1H-2025, so "
       "this company runs BELOW its year end at mid-year rather than above it. Raising the "
       "ratio lowers the valuation, and the study raised it.")

    J_("the minority deduction",
       "the 62,530 put liability alone",
       "the put liability AND the 53,594 book non-controlling interest",
       flip(subs=[("                - V('debt_1h26') - V('lease_1h26') - V('finliab_1h26'))",
                   "                - V('debt_1h26') - V('lease_1h26') - V('finliab_1h26')\n"
                   "                - V('nci_1h26'))"),
                  ("                                      - V('finliab_1h26'))) < 1.0, "
                   "(c, \"bridge does not close\")",
                   "                                      - V('finliab_1h26') - V('nci_1h26'))) "
                   "< 1.0, (c, \"bridge does not close\")")]),
       "these are two names for one claim: under the shareholders' arrangements the parent may "
       "be required to buy the 30% of one subsidiary and the 20% of the other, and the company "
       "has recognised the present value of that exercise price as a liability with a matching "
       "negative investment reserve in owners' equity. Deducting both charges the parent twice "
       "for the same stakes. The put is the deduction that survives because it is the cash the "
       "parent would actually pay — and it is also the larger of the two, so the adopted side "
       "is not simply the cheaper one, though the net effect of dropping the double count "
       "raises the answer.")

    J_("FY2026 capital spending",
       "700mn, the middle of the company's guided 600-800mn range",
       "600mn, the guided low end",
       flip(subs=[("    'A': {2026: 700_000.0, 2027: 600_000.0, 2028: 520_000.0, "
                   "2029: 420_000.0, 2030: 380_000.0},",
                   "    'A': {2026: 600_000.0, 2027: 600_000.0, 2028: 520_000.0, "
                   "2029: 420_000.0, 2030: 380_000.0},")]),
       "the company guides a range and the study takes the midpoint rather than an end of it, "
       "which is the defensible default; the low end is equally disclosed and would raise the "
       "answer. Recorded because a midpoint is still a choice.")

    J_("the depreciation anchor",
       "the FY2025 charge over the FY2024 closing asset base",
       "the reviewed 1H-2026 charge annualised over the same base",
       flip(subs=[("DEP_RATE = V('dna_fy25') / (H[2024]['ppe'] + H[2024]['rou'] "
                   "+ H[2024]['intangibles'])",
                   "DEP_RATE = (V('dna_1h26') * 2) / (H[2024]['ppe'] + H[2024]['rou'] "
                   "+ H[2024]['intangibles'])")]),
       "a near-term reviewed actual outranks a stale full-year rate, and this study's own "
       "normalised lens uses the annualised half-year charge and argues in terms that it is "
       "'what the fleet being priced actually carries' — while the primary lens anchors on "
       "FY2025. One model, two depreciation anchors, and the study argues for the one it does "
       "not use in its primary. The move is tiny and runs the opposite way to intuition, "
       "because depreciation is a tax shield here: LOWERING it lowers free cash flow at a 9% "
       "tax rate faster than it raises terminal profit, so the adopted anchor is the "
       "higher-value side by 0.09%.")

    crux_expansion = published + 0.25 * (F0["dcf_A"] - F0["dcf_B"])
    crux_plateau = published - 0.25 * (F0["dcf_A"] - F0["dcf_B"])
    J_("the crux — what happens to drilling demand once the capacity target is met",
       "neither: both futures are computed in full, published side by side as separate lines, "
       "and enter the central at a quarter of the weight each",
       "resolving it — adopting one of the two framings outright",
       published,
       "THIS FORK CARRIES NO DIRECTION AND THE ZERO SPREAD ABOVE IS THE REASON, NOT A DODGE. "
       "The two resolutions are AED %.4f (the expansion case alone in the blend) and AED %.4f "
       "(the plateau case alone), and they are symmetric about the published answer BY "
       "CONSTRUCTION because the study weights them equally — so there is no single "
       "'other framing' to price against and the sign test cannot be given one without the "
       "author choosing which. The spread is %.4f, %.1f%% of the published answer and %.1f%% "
       "of the cash-flow lens itself, so it is the largest disagreement in the study by "
       "width; it is recorded here with both tails valued rather than left out, because what "
       "a study may not do is go unmeasured. The company itself has declined to guide 2027 "
       "until rig and services phasing is fixed, which is the disclosed reason two cases "
       "exist rather than one."
       % (crux_expansion, crux_plateau, crux_expansion - crux_plateau,
          100 * (crux_expansion - crux_plateau) / published,
          100 * (F0["dcf_A"] - F0["dcf_B"]) / ((F0["dcf_A"] + F0["dcf_B"]) / 2)),
       value_if_expansion_case_alone=crux_expansion,
       value_if_plateau_case_alone=crux_plateau,
       directionless=True)

    # the study-level sign test the gate computes, and the count across every recorded
    # judgement, which the 5% threshold necessarily excludes
    mat = [j for j in J if j["share_of_published_answer"] >= 0.05]
    all_signed = [j for j in J if not j.get("directionless")]
    n_m, k_m, p_m = sign_test([1 if j["value_adopted"] > j["value_alternative"] else -1
                               for j in mat])
    # the same test with the beta fork read against its MONTHLY alternative instead of its
    # weekly one — the one material judgement whose direction the choice of alternative
    # decides. Published because a single reported p-value would hide that.
    _flip_beta = [(-1 if j["name"] == "the beta estimate"
                   else (1 if j["value_adopted"] > j["value_alternative"] else -1)) for j in mat]
    n_b, k_b, p_b = sign_test(_flip_beta)
    n_a, k_a, p_a = sign_test([1 if j["value_adopted"] > j["value_alternative"] else -1
                               for j in all_signed])

    contested = {
        "ticker": "ADNOCDRILL",
        "as_of": committed["meta"]["study_date"],
        # [R-ENF-06]: the answer this record was generated against
        "published_central": published,
        "published_spot": spot_strike,
        "basis": (
            "value_adopted is the study's PUBLISHED answer — the five-lens weighted central, "
            "which is what a reader receives — and value_alternative is that same answer with "
            "ONE fork flipped and every other driver held at its published value. Each "
            "alternative is produced by re-running this study's own compute.py end to end, "
            "never by restating a delta: the harness reproduces the published central to the "
            "last digit before any variant is run, and every source substitution is asserted "
            "to have landed exactly once."),
        "how_the_threshold_bites_here": (
            "MATERIALITY IS MEASURED AGAINST THE PUBLISHED ANSWER, AND ON THIS STUDY THAT IS "
            "NOT A NEUTRAL CHOICE — it is worth saying so rather than letting a reader "
            "discover it. The published answer is a five-lens blend, so a judgement governing "
            "ONE lens reaches the answer only at that lens's weight: the book lens' return "
            "moves its own lens by %.1f%% and the published answer by %.1f%%, and the "
            "normalised lens' Fisher inconsistency moves its own lens by %.1f%% and the "
            "published answer by %.1f%%. %d judgements clear 5%% of the published answer and "
            "%d more are recorded below it. The dampening is real — a %.1f%% move in the "
            "answer is a %.1f%% move in the answer — but it is produced by the blend, which "
            "is judgement number one in this list, so the architecture that makes the others "
            "look small is itself the largest of them. Both counts are published below."
            % (100 * _book_lens_share, 100 * _book_answer_share,
               100 * _norm_lens_share, 100 * _norm_answer_share,
               len(mat), len(J) - len(mat),
               100 * _book_answer_share, 100 * _book_answer_share)),
        "sign_test_material": {"n": n_m, "resolved_upward": k_m, "p": p_m},
        "sign_test_material_beta_read_the_other_way": {
            "n": n_b, "resolved_upward": k_b, "p": p_b,
            "note": ("the beta fork against the five-year MONTHLY regression rather than the "
                     "three-year weekly one. It is the only material judgement whose direction "
                     "the choice of alternative decides, so the test is printed both ways: "
                     "neither reading reaches the 5% flag, so the CONCLUSION is robust even "
                     "though the direction of that one entry is not.")},
        "sign_test_all_recorded_judgements": {
            "n": n_a, "resolved_upward": k_a, "p": p_a,
            "note": ("every recorded fork that carries a direction, whatever its size. This is "
                     "not the gate's test and is not a substitute for it — it is the count the "
                     "5%% threshold necessarily hides, published because the instrument exists "
                     "to measure the PATTERN of choices rather than any one of them.")},
        "unvalued": [{
            "name": "the terminal construction",
            "adopted": ("the reinvestment identity — reinvestment = growth / return on capital, "
                        "terminal value = profit x (1 - reinvestment) / (rate - growth) — which "
                        "carries %.1f%% of enterprise value on the expansion framing and %.1f%% "
                        "on the plateau framing"
                        % (100 * C["CASE"]["A"]["tv_pct_of_ev"],
                           100 * C["CASE"]["B"]["tv_pct_of_ev"])),
            "alternative": "the sanctioned terminal, built on a DISCLOSED asset life with "
                           "maintenance charged at current cost",
            "why_unvalued": (
                "the alternative has no value because the input it requires has not been "
                "sourced for this name. The sanctioned construction rests on a useful life "
                "read from the company's own accounting-policies note; this study commits no "
                "such life in its input register, and the house register of disclosed lives "
                "carries no entry for this name at all. A LIFE THIS DESK CHOSE IS NOT A "
                "DISCLOSED LIFE, so the honest output is stop-and-inform rather than a number: "
                "the sign of this fork is decided entirely by the life picked, and picking one "
                "here would be this desk choosing the direction of its own audit. What this "
                "study DOES commit is the maintenance figure its own register carries from the "
                "FY2025 management discussion — around USD %.0f million a year — and that "
                "figure alone cannot close the construction, because the module also needs the "
                "life over which the asset base is replaced. This study's own dated gap review "
                "rebuilt the terminal across candidate lives and found the answer moving in "
                "BOTH directions depending which was used, which is the measured form of the "
                "same statement. It is listed here rather than omitted because an absent answer "
                "is not a clean one, and this is the largest single construction in the study — "
                "the terminal carries roughly three-quarters of enterprise value on both "
                "framings." % (C["V"]("g_maint_capex") / 1000.0)),
            "what_would_close_it": ("the useful-life band from the FY2025 audited "
                                    "accounting-policies note, committed to the house register "
                                    "of disclosed lives with its page and the route it was read "
                                    "by, and a weighted life derived from the property and "
                                    "equipment note's own composition"),
        }],
        "judgements": J,
    }

    # ------------------------------------------------------------------------ WRITE
    for path, doc in ((os.path.join(HERE, "diagnostics.json"), diagnostics),
                      (os.path.join(HERE, "contested_judgements.json"), contested)):
        json.dump(doc, open(path, "w", encoding="utf-8"), indent=1)

    # THE STRUCTURAL HALF OF THE RULE, ASSERTED RATHER THAN REMEMBERED: the quantity
    # solved from the traded price must not sit in the file every builder reads.
    raw = open(NUMBERS, encoding="utf-8").read()
    for v in (implied["A"], implied["B"], shift["A"], shift["B"]) + tuple(
            x for x in also.values() if isinstance(x, float)):
        assert repr(v) not in raw, ("a reverse-read value has reached study_numbers.json: %r" % v)

    print("REVERSE READ  price AED %.2f implies an FY2030 EBITDA margin of %.2f%% (expansion) "
          "/ %.2f%% (plateau)\n              against this study's %.2f%% / %.2f%%, and a filed "
          "record of %.2f%%-%.2f%%"
          % (LATEST_PRICE, 100 * implied["A"], 100 * implied["B"],
             100 * study_margin["A"], 100 * study_margin["B"],
             100 * min(filed.values()), 100 * max(filed.values())))
    print("SIGN TEST     %d judgements, %d material (>=5%% of the published answer), "
          "%d up / %d down, p=%.4f" % (len(J), n_m, k_m, n_m - k_m, p_m))
    print("              across all %d directional judgements: %d up / %d down, p=%.4f"
          % (n_a, k_a, n_a - k_a, p_a))
    for j in sorted(J, key=lambda r: -r["share_of_published_answer"]):
        print("   %-52s %7.4f vs %7.4f  %5.1f%%  %s"
              % (j["name"][:52], j["value_adopted"], j["value_alternative"],
                 100 * j["share_of_published_answer"],
                 "—" if j.get("directionless") else
                 ("UP" if j["value_adopted"] > j["value_alternative"] else "DOWN")))


if __name__ == "__main__":
    main()
