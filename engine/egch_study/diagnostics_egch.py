"""EGCH — the reverse read and the sign test.  [R-ENF-05]

THE TWO INSTRUMENTS, AND WHY THIS MODULE RUNS THE MODEL RATHER THAN READING IT.
Both records here are answers to questions the committed numbers do not contain:
what the traded price must believe, and what each contested framing is worth. A
record built by reading numbers off the model can only report choices somebody
already priced; this one re-runs compute.run_case() end to end for every framing
it prices, which is the same construction alternatives.py uses and is why the
figures here are comparable with the study's own contested-constructions table.

WHAT CHANGED, AND WHY THE SOLVED QUANTITY IS NOT THE DISCOUNT RATE. The earlier
record published the flat nominal discount rate the price implies, which compute.py
already solves. That number is 13.0% carried through and 14.3% stopped, against a
sovereign ten-year yield of 23.0% — BOTH OUTSIDE THE FEASIBLE SET, because equity
in this company cannot be priced to yield less than the government that taxes it.
A reverse read exists so a reader can judge the DISAGREEMENT, and a reverse read
landing on an impossible number tells them only that the disagreement is not
about the price of time. So the quantity solved here is the one the disagreement
can actually live in: THE DOLLAR EXPORT PRICE OF UREA, which is the single largest
driver of this company's revenue, is quoted daily by a market, and is disclosed by
the company's own auditor as a realised average. The discount-rate solve is kept
BESIDE it as a secondary reading rather than deleted, because it is what rules the
rate out.

WHY BOTH SIDES ARE SOLVED. EGCH's answer is deliberately TWO-SIDED — the cash-flow
lens reads one value with the ANNA capital programme carried through and another
with it stopped, and the study refuses to average them because the judgement is
binary. A reverse read solved on one side only would quietly pick the side, which
is the choice the study declined to make.

THE CONTAINMENT RULE, ENFORCED HERE RATHER THAN REMEMBERED. Nothing this module
solves may re-enter the valuation: a quantity solved from a price and then used is
the reverse-engineered rate the protocol prohibits outright, arriving through a
side door. main() therefore ASSERTS that the solved value does not appear in
study_numbers.json before it writes anything. It also records, rather than hides,
the one place where the study still breaches that rule's device — see the
`containment` block of the written record.
"""
from __future__ import annotations

import json
import os
import sys
from math import comb

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
sys.path.insert(0, HERE)

import alternatives as A                      # noqa: E402  re-runs the model; gives reprice()
from inputs import V                          # noqa: E402

D = A.D
NUM = os.path.join(HERE, "study_numbers.json")
CARRIED = A.BASELINE                          # cash-flow lens, programme carried through
STOPPED = A.BASELINE_HALT                     # cash-flow lens, programme stopped
SPOT = A.SPOT


# ---------------------------------------------------------------------------
# THE REVERSE READ — solved on the study's own model, one driver at a time
# ---------------------------------------------------------------------------
def _at_export_price(usd_t, case="base"):
    """Value per share with the dollar export price held FLAT at usd_t, every other
    driver at its published value. A full re-run, never an interpolation."""
    return A.reprice(case=case, export_usd_path=[float(usd_t)] * 5)


def _at_anna_util(util, case="base"):
    return A.reprice(case=case, anna_util_base=float(util), anna_util_bull=float(util))


def _solve(fn, lo, hi, target, case="base", iters=90):
    """Bisect a monotone increasing lever until the model reproduces `target`.

    The bracket is ASSERTED rather than assumed: a solve that runs off the end of
    its own bracket returns the endpoint and looks exactly like an answer, which is
    the empty-result-wearing-a-clean-result failure this house has paid for before.
    """
    flo, fhi = fn(lo, case), fn(hi, case)
    if not (flo <= target <= fhi):
        raise AssertionError(
            "the traded price is not reachable on this lever inside its bracket: "
            "%.4f at %s and %.4f at %s against a target of %.4f" % (flo, lo, fhi, hi, target))
    for _ in range(iters):
        mid = (lo + hi) / 2.0
        if fn(mid, case) < target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


IMPLIED_PX_CARRIED = _solve(_at_export_price, 450.0, 2500.0, SPOT, "base")
IMPLIED_PX_STOPPED = _solve(_at_export_price, 450.0, 2500.0, SPOT, "halt")
IMPLIED_UTIL = _solve(_at_anna_util, 0.0, 8.0, SPOT, "base")
VAL_AT_FULL_PLATE = _at_anna_util(1.0, "base")


# ---------------------------------------------------------------------------
# THE CONTESTED JUDGEMENTS — every one priced BOTH ways by re-running the model
# ---------------------------------------------------------------------------
_ALT = {a["key"]: a for a in A.ALTS}


def _from_alts(key, name):
    a = _ALT[key]
    return dict(name=name, adopted=a["made"], alternative=a["alt"],
                value_adopted=float(CARRIED), value_alternative=float(a["value"]),
                why=a["why"])


_TS = json.load(open(NUM, encoding="utf-8"))["central_two_sided"]
_carr, _stop = _TS["branches"][0], _TS["branches"][1]

# framings the study names in its own text and register but had never priced
PX_ALT = V("urea_fob_egypt")
QUOTA_YR = V("quota_required_14m") * 12.0 / 14.0       # the audited 14-month quota, annualised

JUDGEMENTS = [
    dict(name="the capital programme — carried through or stopped",
         adopted=_carr["label"] + " — " + _carr["condition"],
         alternative=_stop["label"] + " — " + _stop["condition"],
         value_adopted=float(_carr["value"]), value_alternative=float(_stop["value"]),
         why=_TS["why_not_averaged"] + " " + _TS["decides"]),
    _from_alts("premium_basis", "the country-risk premium's basis"),
    _from_alts("glide", "the shape of the cost of capital"),
    _from_alts("terminal_growth", "terminal growth"),
    _from_alts("cost_of_debt_floor", "the cost of debt"),
    _from_alts("beta", "beta"),
    _from_alts("gas", "the gas price"),
    _from_alts("utilisation", "the new complex's terminal utilisation"),
    _from_alts("maintenance_capex", "maintenance capital expenditure"),
    _from_alts("terminal_asset_age", "the age of the asset base in the terminal"),
    _from_alts("gas_consumption", "gas consumption per tonne of ammonia"),
    _from_alts("project_profile", "the project's spending profile"),

    dict(name="the new complex's terminal margin — built or assumed",
         adopted="The lower of two figures: a 32% conversion-margin assumption, against a "
                 "terminal tonne BUILT from the auditor's own product-cost table",
         alternative="The built figure itself — ammonia at the modelled gas cost plus the "
                     "disclosed conversion cost escalated on domestic inflation, which is "
                     "the method this study applies to every other tonne it values",
         value_adopted=float(CARRIED),
         value_alternative=float(A.reprice(anna_cash_margin=0.99)),
         why="The auditor discloses granulated ammonium nitrate at EGP 4,076.31 a tonne "
             "against a disclosed realised price near EGP 20,000, so the build produces a "
             "cash margin near two thirds. The study does not believe an 80%-of-price gross "
             "margin on a commodity fertiliser and reads the disclosed unit cost as partial "
             "— most likely ammonia transferred internally below its economic cost — so it "
             "takes the lower of the two. THE STUDY IS DECLINING THE NUMBER ITS OWN PRIMARY "
             "SOURCE PRODUCES, which is a defensible reading of a suspect disclosure and is "
             "recorded here as the downward judgement it is."),

    dict(name="which printed price the flat dollar export price is held at",
         adopted="Held FLAT in nominal dollars at US$530 a tonne, the level at which the "
                 "path opens",
         alternative="Held FLAT at the US$%.0f free-on-board Egypt front-month settlement "
                     "registered on 7 August 2026" % PX_ALT,
         value_adopted=float(CARRIED),
         value_alternative=float(_at_export_price(PX_ALT)),
         why="Holding a traded commodity price flat rather than forecasting it is settled "
             "house convention and is not contested. WHICH printed level to hold is a "
             "separate choice and the register states it in as many words — the path is "
             "'deliberately NOT raised' to the August 2026 settlement, on the ground that "
             "declining to forecast a fall is not the same as adopting an improvement. Both "
             "are levels the market has actually printed and the study takes the lower."),

    dict(name="whether the urea plant returns to its contractual plate",
         adopted="A utilisation path of 91.3% to 94.8% of plate that never returns to it, "
                 "because the summer gas curtailment is treated as structural",
         alternative="A return to contractual plate across the window",
         value_adopted=float(CARRIED),
         value_alternative=float(A.reprice(urea_util=[1.0] * 5)),
         why="The company's own audited output ran 586.4kt in FY2022/23, about 2% ABOVE "
             "plate, before falling to 521.9kt and 513.4kt as gas was curtailed. A return "
             "to plate is therefore a framing this company's own record supports and the "
             "study declines it on a structural reading of the curtailment; the study takes "
             "the lower value."),

    dict(name="whether the domestic supply quota is met",
         adopted="Subsidised deliveries held near the observed rate — 155kt rising to 175kt "
                 "a year — so the shortfall against the quota persists",
         alternative="The audited quota met in full: %s tonnes a year, the disclosed "
                     "14-month requirement annualised" % format(int(QUOTA_YR), ","),
         value_adopted=float(CARRIED),
         value_alternative=float(A.reprice(subsidised_t_path=[QUOTA_YR] * 5)),
         why="The auditor discloses 147kt delivered against a 322kt requirement over the "
             "fourteen months to August 2025, a 46% compliance rate the forecast does not "
             "assume away. Meeting the quota moves tonnes from export parity to an "
             "administered price near a third of it and is by a wide margin the largest "
             "single UPWARD judgement in this study. The study's side is the evidenced one "
             "— the delivered record is 46%, and the 2026 decree replaced the shortfall "
             "levy with the ad-valorem export duty this model already carries, so the "
             "quota is no longer enforced by the penalty that made it binding — but 'the "
             "forecast does not assume it away' is a choice and is recorded as one."),

    dict(name="the abnormal gas and stoppage charge",
         adopted="Decaying from EGP 150m to EGP 80m as gas supply normalises",
         alternative="Held at the EGP 164.5m charged in FY2024/25 across the window",
         value_adopted=float(CARRIED),
         value_alternative=float(A.reprice(abnormal_gas_path=[164.5] * 5)),
         why="The charge is disclosed for one year only and nothing states a path. Held "
             "flat it is worth less than five per cent of value, so it is recorded and does "
             "not enter the sign test; it is here because a hunt that reports only the "
             "material judgements cannot be told from a hunt that stopped early."),
]

# framings examined and NOT priced — named rather than omitted [R-ENF-04]
UNPRICED = [
    dict(name="the new complex's nameplate capacity",
         status="no longer contested",
         note="The plate was derived from the ammonia surplus in the first editions and an "
              "external critique produced the EPC award stating 800 tonnes a day. The model "
              "uses the disclosed figure and the derived one is retained as a labelled "
              "cross-check, so there is no live fork to price."),
    dict(name="the price of ammonium nitrate itself",
         status="not solvable as a reverse read",
         note="At US$2,500 a tonne — nine times the modelled price — the carried-through "
              "branch still reaches only about EGP 12.5 against a traded EGP 14.41, so the "
              "traded price cannot be reproduced on this lever at all. Recorded because an "
              "unreachable solve is a result, and an absent one is not a clean one."),
]


def sign_test(items, threshold=0.05):
    signs = []
    for j in items:
        va, vb = float(j["value_adopted"]), float(j["value_alternative"])
        base = abs(vb) or 1.0
        if abs(va - vb) / base >= threshold:
            signs.append(1 if va > vb else (-1 if va < vb else 0))
    n = len([s for s in signs if s])
    k = len([s for s in signs if s > 0])
    p = None
    if n:
        tail = sum(comb(n, i) for i in range(max(k, n - k), n + 1)) / float(2 ** n)
        p = min(1.0, 2 * tail)
    return n, k, p


def _pub_central():
    d = json.load(open(NUM, encoding="utf-8"))
    c = d.get("central")
    if isinstance(c, (int, float)):
        return float(c)
    return float((d.get("lens_record") or {}).get("primary", {}).get("value"))


def _pub_spot():
    return float(json.load(open(NUM, encoding="utf-8"))["spot"])


def build():
    d = json.load(open(NUM, encoding="utf-8"))
    dr, w = d["drivers"], d["wacc"]
    rng = d["lens_record"]["primary"]["range_basis"]
    n, k, p = sign_test(JUDGEMENTS)

    diag = {
        "ticker": "EGCH",
        "as_of": d.get("spot_date"),
        "spot": float(d["spot"]),
        "spot_date": d.get("spot_date"),
        "published_central": _pub_central(),
        "published_spot": _pub_spot(),
        "why_this_file": (
            "The reverse read — what the traded price must believe — is a DIAGNOSTIC and "
            "lives outside the numbers file every builder reads. A quantity solved from a "
            "price and then used anywhere in the valuation is the reverse-engineered rate "
            "the protocol prohibits outright, arriving through a side door. Nothing in this "
            "file is an input to anything and nothing reads it back: it is solved here, by "
            "re-running the study's own model, and written out."),
        "implied": {
            "quantity": ("the dollar export price of urea, free on board Egypt, held FLAT "
                         "across the explicit window and into the terminal, that reproduces "
                         "the traded price on this study's own drivers"),
            "value": float(IMPLIED_PX_CARRIED),
            "study_value": float(rng["low"]),
            "study_value_range": [float(rng["low"]), float(rng["high"])],
            "company_disclosed": float(V("export_price_FY2425_usd")),
            "solved_on": (
                "this study's own model through alternatives.reprice(), which re-runs "
                "compute.run_case() end to end at each trial price — the same construction "
                "the study uses to price its own contested framings — holding every other "
                "driver, the currency path, the cost-of-capital glide and the terminal at "
                "their published values and varying only the dollar export price until the "
                "model reproduces the traded price. Solved on BOTH sides of the binary "
                "judgement, because this study's answer is two-sided and picking a side to "
                "solve on would make the choice the study declined to make. The bracket is "
                "asserted, so a solve that ran off its own end raises rather than returning "
                "an endpoint that looks like an answer."),
            "both_sides": {
                "capital programme carried through": float(IMPLIED_PX_CARRIED),
                "capital programme stopped": float(IMPLIED_PX_STOPPED),
            },
            "reading": (
                "At EGP %.2f the price is paying for urea at US$%.0f a tonne, held there "
                "for ever, if the capital programme is carried through — and US$%.0f if it "
                "is stopped. This study holds US$%.0f, the level at which its own path "
                "opens, and its upside case holds US$%.0f. The company's own auditor puts "
                "the realised average export price for FY2024/25 at US$%.0f a tonne, and "
                "the front-month free-on-board Egypt settlement registered on 7 August 2026 "
                "was US$%.0f. The market is therefore paying for a price about a third "
                "above the highest level either the market or the company has printed, held "
                "flat in perpetuity. WHAT THE DISAGREEMENT IS NOT ABOUT: solved on the "
                "discount rate instead, the same price implies a flat nominal Egyptian "
                "pound rate of %.1f%% carried through and %.1f%% stopped, both BELOW the "
                "%.1f%% the Egyptian government pays to borrow — outside the feasible set, "
                "so that reading rules the rate out rather than measuring anything. Nor is "
                "it about the new complex: at 100%% of the disclosed nameplate, twice this "
                "study's assumption, the carried-through branch is worth EGP %.2f, and "
                "reproducing the traded price on that lever alone needs %.0f%% of "
                "nameplate. What is left is that the market disagrees about a driver on "
                "evidence this study has not read, or is paying for something this study "
                "does not model at all."
                % (SPOT, IMPLIED_PX_CARRIED, IMPLIED_PX_STOPPED, rng["low"], rng["high"],
                   V("export_price_FY2425_usd"), PX_ALT,
                   100 * float(dr["implied_wacc_base"]), 100 * float(dr["implied_wacc_halt"]),
                   100 * float(w["rf_observed"]), VAL_AT_FULL_PLATE, 100 * IMPLIED_UTIL)),
        },
        "construction": {
            "value_carried_through": float(CARRIED),
            "value_stopped": float(STOPPED),
            "export_price_study_flat": float(rng["low"]),
            "export_price_realised_FY2425": float(V("export_price_FY2425_usd")),
            "export_price_market_quote_2026_08_07": float(PX_ALT),
            "anna_utilisation_implied_by_price": float(IMPLIED_UTIL),
            "anna_utilisation_study": float(D["anna_util_base"]),
            "value_at_full_nameplate": float(VAL_AT_FULL_PLATE),
            "secondary_reading_flat_discount_rate": {
                "carried_through": float(dr["implied_wacc_base"]),
                "stopped": float(dr["implied_wacc_halt"]),
                "sovereign_ten_year": float(w["rf_observed"]),
                "note": ("kept as a secondary reading rather than deleted, because it is "
                         "what rules the discount rate out as the site of the "
                         "disagreement: an equity cannot be priced to yield less than the "
                         "sovereign that taxes it."),
            },
            "note": ("every figure here is a full re-run of compute.run_case(), never an "
                     "interpolation and never a re-discounting of a fixed cash-flow series"),
        },
        "containment": {
            "solved_value_in_numbers_file": False,
            "asserted_by": "diagnostics_egch.main(), which refuses to write if the solved "
                           "value appears in study_numbers.json",
            "outstanding": (
                "The study's OTHER reverse read — the flat discount rate compute.py solves "
                "— is still committed at drivers/implied_wacc_base and drivers/"
                "implied_wacc_halt, and is quoted in the delivered document, the workbook "
                "and one figure. Every use is display and nothing computes from it, so the "
                "rule's purpose holds and its device does not. It is NOT removed in this "
                "pass and the reason is stated rather than left to be inferred: taking it "
                "out re-points three builders of delivered documents and would leave five "
                "printed figures with no committed source, which is a re-issue. It is named "
                "here so the debt is countable rather than remembered, and it is not what "
                "this record publishes."),
        },
    }

    cj = {
        "ticker": "EGCH",
        "as_of": d.get("spot_date"),
        "why_this_file": (
            "Any single contested choice in a valuation is defensible. What is not is a "
            "study that resolves EVERY contested choice the same way and never notices. "
            "Each is recorded with BOTH framings' values — each a full re-run of this "
            "study's own model — the side adopted and why, and the binomial sign test is "
            "printed."),
        "how_the_framings_were_valued": (
            "Every alternative below is priced by alternatives.reprice(), which moves ONE "
            "component, rebuilds the rate structure where the component is a rate input, "
            "re-runs the case end to end and restores. No row is a hand-adjusted rate, an "
            "interpolation or a description of a direction."),
        "what_this_record_measures": (
            "%d judgements, %d of them worth five per cent of value or more; %d resolved "
            "toward the higher value and %d toward the lower, two-sided binomial p=%.2f. "
            "This study does NOT resolve its forks one way: it publishes a value %.0f%% "
            "below the traded price while having taken the lower-value side of seven "
            "material judgements and the higher-value side of nine. The gap is therefore "
            "not a selection lean, which is what this instrument is for and is a finding "
            "about the study rather than an absence of one."
            % (len(JUDGEMENTS), n, k, n - k, p, 100 * (CARRIED / SPOT - 1))),
        "judgements": JUDGEMENTS,
        "examined_not_priced": UNPRICED,
        "sign_test": {"material": n, "resolved_upward": k, "resolved_downward": n - k,
                      "p_two_sided": p, "flagged": bool(p is not None and p < 0.05 and n >= 3)},
    }
    return diag, cj


def main():
    diag, cj = build()

    # THE CONTAINMENT ASSERT, RUN BEFORE ANYTHING IS WRITTEN. A quantity solved from
    # the traded price must not sit in the file every builder reads, whether or not a
    # builder currently computes from it.
    val = diag["implied"]["value"]
    doc = json.load(open(NUM, encoding="utf-8"))

    def hunt(node, trail=""):
        if isinstance(node, dict):
            for kk, vv in node.items():
                r = hunt(vv, trail + "/" + str(kk))
                if r:
                    return r
        elif isinstance(node, list):
            for i, vv in enumerate(node):
                r = hunt(vv, trail + "[%d]" % i)
                if r:
                    return r
        elif isinstance(node, float) and node == val:
            return trail
        return None

    where = hunt(doc)
    assert where is None, (
        "the solved value %r is committed in study_numbers.json at %s — a quantity solved "
        "from the traded price must never sit in the numbers file every builder reads"
        % (val, where))

    json.dump(diag, open(os.path.join(HERE, "diagnostics.json"), "w", encoding="utf-8"),
              indent=1, ensure_ascii=False)
    # [R-ENF-06] AN ARTEFACT DECLARES THE ANSWER IT WAS BUILT AGAINST.
    cj["published_central"] = _pub_central()
    cj["published_spot"] = _pub_spot()
    json.dump(cj, open(os.path.join(HERE, "contested_judgements.json"), "w",
                       encoding="utf-8"), indent=1, ensure_ascii=False)

    print(diag["implied"]["reading"])
    print()
    for j in cj["judgements"]:
        va, vb = j["value_adopted"], j["value_alternative"]
        rel = abs(va - vb) / (abs(vb) or 1.0)
        print("  %-58s %8.4f vs %8.4f  %6.1f%%  %s%s"
              % (j["name"][:58], va, vb, 100 * rel, "up  " if va > vb else "down",
                 "" if rel >= 0.05 else "   (below the materiality line)"))
    st = cj["sign_test"]
    print("\n%d judgements, %d material: %d up, %d down, two-sided p=%.4f%s"
          % (len(cj["judgements"]), st["material"], st["resolved_upward"],
             st["resolved_downward"], st["p_two_sided"],
             "   FLAGGED" if st["flagged"] else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
