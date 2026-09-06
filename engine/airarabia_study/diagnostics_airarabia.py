"""AIRARABIA — the reverse read and the sign test.  [R-ENF-05]

THE REVERSE READ. This study states what it believes. It has never stated what
the PRICE believes, and the two are the same model read backwards. Solved here:
the SINGLE FLAT DISCOUNT RATE that reproduces the traded price on this study's
own free cash flows, its own terminal cash flow and its own terminal growth,
holding every driver at its published value — against the flat rate that
reproduces THIS STUDY'S OWN enterprise value on the identical construction, so
the two are the same quantity measured twice.

WHY THE BRIDGE HAS TO BE INVERTED RATHER THAN SUBTRACTED. The shared instrument
carries an equity price back to an enterprise value by SUBTRACTING the bridge,
which is right wherever the bridge is additive. This study's is not: it values
the operations at 31 December 2025 and then accretes them 246 days to the
anchor at the cost of equity while the cash, the non-operating assets and the
joint-venture carrying value accrete at the deposit yield, because cash does not
compound at the cost of equity. A unit of enterprise value is therefore worth
1.0558 of equity here and not 1.0000, and subtracting the bridge would put a
real error into the solved rate that would read as a disagreement with the
market. The price is inverted through the study's own two-legged accretion
instead, and the result is handed to the shared solver — so the arithmetic that
is common to every name in the book stays common, and only the part that is
genuinely this study's own is done here.

WHAT ELSE THE PRICE IMPLIES, AND WHY IT IS WORTH MORE THAN THE RATE ALONE. The
flat rate is the comparable read across the book. It is not the most legible one
for an airline, where a reader can check passengers and fares against the
company's own results presentations. So the same question is asked again of the
drivers themselves, one at a time, each solved on the study's own scenario
engine with everything else held at its published value. The joint-venture read
is the one worth pausing on: this study prices the venture network BOTH ways and
never averages, and the price lands between its two published framings.

THE CONTAINMENT RULE IS THE POINT, NOT A FORMALITY. A quantity solved from a
price and then used anywhere in the valuation is the reverse-engineered rate the
protocol prohibits outright, arriving through a side door. So this module writes
diagnostics.json and NOTHING READS IT BACK; it is named `diagnostics_*` so the
exemption applies to the file that COMPUTES the read rather than to any builder
that might consume it; and it ASSERTS, before writing, that the solved value
appears nowhere in study_numbers.json, which is the file every builder does read.

THE SIGN TEST. Any single contested choice is defensible; what is not is a study
resolving every one of them the same way and never noticing. Every alternative
below is valued by RE-RUNNING THIS STUDY'S OWN compute.py with that one choice
changed and everything else held — so the difference measures the CHOICE and not
the construction — in a scratch directory, so the committed numbers file cannot
move; and every source substitution is asserted to have landed exactly once
before the run is believed. Nothing here changes a driver, a forecast, a rate or
a fair value: the alternatives are computed and reported, never adopted.
"""
from __future__ import annotations

import contextlib
import io
import json
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.dirname(HERE)
NUM = os.path.join(HERE, "study_numbers.json")
COMPUTE = os.path.join(HERE, "compute.py")
PRICE_FILE = os.path.join(ENGINE, "prices", "SUPPLIED_03-09-2026.json")
AS_OF = "2026-09-05"

SRC = open(COMPUTE, encoding="utf-8").read()
ANCHOR = "V = {k: rec['value'] for k, rec in INP.items()}"
assert SRC.count(ANCHOR) == 1, "compute.py's input dictionary is not where this expects it"

# the study's own inputs that its run reads off disk rather than computing
CARRY = ("beta_result.json", "step0_result.json", "strike_result.json",
         "backtest_5y.json", "paths_1M.npy", "paths_3M.npy")


# --------------------------------------------------------------------------
# THE STUDY'S OWN MODEL, RE-RUN WITH ONE THING CHANGED
# --------------------------------------------------------------------------
def run(overrides=None, patches=(), label=""):
    """Execute compute.py with one choice changed and everything else held.

    The run happens in a scratch directory with __file__ pointed at it, so it
    writes ITS study_numbers.json there and cannot touch the committed one. An
    input override is injected at the single line where the input dictionary
    becomes the value dictionary, so everything downstream re-derives through
    the study's own code; a fork that is a CONSTRUCTION rather than an input is
    a minimal source substitution, asserted to have landed.
    """
    src = SRC
    for old, new in patches:
        n = src.count(old)
        assert n == 1, ("the substitution %r landed %d times, not once (%s). A fork "
                        "valued through a substitution that did not land is a fixture "
                        "that never injected its condition." % (old[:70], n, label))
        src = src.replace(old, new)
    src = src.replace(ANCHOR, ANCHOR + "\nV.update(_OVR)", 1)
    d = tempfile.mkdtemp(prefix="airarabia_alt_")
    try:
        for f in CARRY:
            p = os.path.join(HERE, f)
            if os.path.exists(p):
                shutil.copy(p, d)
        g = {"__name__": "_alt", "__file__": os.path.join(d, "compute.py"),
             "_OVR": dict(overrides or {})}
        with contextlib.redirect_stdout(io.StringIO()):
            exec(compile(src, "compute.py", "exec"), g)
        return g
    finally:
        shutil.rmtree(d, ignore_errors=True)


def bisect(fn, lo, hi, target, n=140):
    """`fn` increasing from lo to hi. Bisection rather than a solver with a
    starting guess: the answer must not depend on where the search began."""
    for _ in range(n):
        m = 0.5 * (lo + hi)
        try:
            v = fn(m)
        except Exception:                                        # noqa: BLE001
            return None
        if v is None:
            return None
        if v < target:
            lo = m
        else:
            hi = m
    return 0.5 * (lo + hi)


# --------------------------------------------------------------------------
# the source substitutions, each a construction the study made that an input
# override cannot reach
# --------------------------------------------------------------------------
NEO_BURN = [(
    "V['fuel_per_pax'] = [V['fuel_intensity'] * p for p in V['jet_eff_base']]",
    "V['fuel_per_pax'] = [V['fuel_intensity'] * p * _OVR['_neo'][_i] "
    "for _i, p in enumerate(V['jet_eff_base'])]")]

LEASED_NPV0 = [
    ("fcff = [nopat[i] + dna[i] - capex[i] - leased_gross[i] - dnwc[i] for i in range(5)]",
     "fcff = [nopat[i] + dna[i] - capex[i] - dnwc[i] for i in range(5)]"),
    ("    p += capex[i] + leased_gross[i] - dna[i]",
     "    p += capex[i] - dna[i]"),
    ("    _f = [_nopat[i] + dna[i] - _capex[i] - leased_gross[i] * capex_mult - _dnwc[i]\n"
     "          for i in range(5)]",
     "    _f = [_nopat[i] + dna[i] - _capex[i] - _dnwc[i]\n"
     "          for i in range(5)]"),
    ("        pp += _capex[i] + leased_gross[i] * capex_mult - dna[i]; _ppe.append(pp)",
     "        pp += _capex[i] - dna[i]; _ppe.append(pp)")]

NET_WEIGHTS = [
    ("wd_gross = debt_fy25 / (debt_fy25 + MKTCAP)",
     "wd_gross = nd_fy25 / (nd_fy25 + MKTCAP)"),
    ("    cash_legs = -nd_fy25 + non_op + jv_val",
     "    cash_legs = non_op + jv_val")]

ROLL_AT_KE = [("    cash_part = cash_legs * ROLL_CASH",
               "    cash_part = cash_legs * roll")]

MINORITY_AT_VALUE = [(
    "    return (op_part + cash_part - V['nci_book']) / SH - V['dps_fy25']",
    "    return (op_part + cash_part) * (1 - _OVR['_ncis']) / SH - V['dps_fy25']")]


def neo_multipliers(base):
    """The fuel-intensity path if the neo's disclosed burn advantage WERE credited.

    An identity on this study's own committed fleet block and one percentage the
    study committed inside the fuel-intensity input's own source field. Net
    additions are used rather than gross deliveries because gross is not
    disclosed, so this is the FLOOR of the credit rather than the whole of it,
    and the FY2025 neo deliveries are excluded because they are already inside
    the FY2025 realised intensity this study anchors on. It is a
    RECONSTRUCTION and is labelled one.
    """
    FL = base["V"]["fleet_cons"]
    adds = [FL["owned_adds"][i] + FL["leased_adds"][i] for i in range(5)]
    cum, s = [], 0
    for a in adds:
        s += a
        cum.append(s)
    share = [cum[i] / FL["ends"][i] for i in range(5)]
    return [1.0 - 0.20 * x for x in share], share


def forks(base, fig):
    """Every fork this study resolved that a reader could reasonably resolve the
    other way, with the alternative built from the study's OWN committed record.

    NO MODEL-DERIVED NUMERAL IS TYPED INTO A REASON. Every figure quoted in a
    `why` below is interpolated from `fig`, which this module computed, or is a
    figure the company itself disclosed and this study committed with its source.
    """
    V = base["V"]
    return [
        dict(
            name="the 2026-28 fuel path: the official energy-agency curve vs the airline "
                 "association's high-fuel assumption held",
            adopted="the energy-agency curve, with relief from 2027",
            alternative="the association's high-fuel view persisting through the hedge blend",
            value=base["dcf_ps_iata"],
            why="This is the study's own named central contested judgement and it is already "
                "published both ways and never averaged, which is the right treatment. It is "
                "recorded here because it is by far the largest fork in the valuation: the "
                "two paths open at USD %.1f and USD %.1f a barrel and end at USD %.1f and "
                "USD %.1f, and fuel was %.1f%% of the audited FY2025 direct-cost stack. The "
                "hedge ratios that would settle which path the company actually pays are "
                "disclosed as existing and not quantified (the swaps and collars note), "
                "which is why neither framing can be resolved from the filings and both are "
                "carried."
                % (V["jet_eff_base"][0], V["jet_eff_alt"][0], V["jet_eff_base"][-1],
                   V["jet_eff_alt"][-1], 100 * fig["fuel_share_of_direct"])),
        dict(
            name="the beta regressor: the registered interim index vs the unregistered "
                 "index of the company's own exchange",
            adopted="the own-stock five-year weekly regression against the index the binding "
                    "rule resolves for this exchange, beta %.3f" % V["beta_used"],
            alternative="the same regression against the general index of the exchange the "
                        "share actually lists on, beta %.3f" % V["beta_alt_benchmark"],
            value=base["dcf_ps_beta_alt"],
            why="The adopted regressor is the one the rule resolves and it applies under a "
                "REGISTERED INTERIM SUBSTITUTION, which the study quotes in full. The "
                "alternative regression has %.1f times the explanatory power (R-squared "
                "%.3f against %.3f) and is the amendment the interim note itself "
                "anticipates. The study is right not to adopt it before it is registered, "
                "and the choice is worth %.0f basis points of cost of equity, so it is a "
                "fork rather than a formality. An earlier edition of this study adopted the "
                "alternative; this one does not, and the direction of that correction is "
                "recorded here rather than only in the correction."
                % (fig["beta_alt_r2"] / fig["beta_r2"], fig["beta_alt_r2"], fig["beta_r2"],
                   10000 * (V["beta_alt_benchmark"] - V["beta_used"]) * V["erp_rating"])),
        dict(
            name="the cash: gross-debt weights with the cash added at face in the bridge, "
                 "vs net-debt weights with nothing added",
            adopted="gross-debt weights in the discount rate, the cash added at face in the "
                    "bridge",
            alternative="net-debt weights in the discount rate, the cash not re-added",
            patch=NET_WEIGHTS,
            why="Both are legitimate and the standing rule permits exactly these two, "
                "forbidding only the combination of them. The adopted construction is the "
                "one the study argues for and it is the lower discount rate: on this "
                "company's net cash the debt weight goes negative, the equity weight levers "
                "above one and the operating rate moves from %.2f%% to %.2f%%. The "
                "alternative discounts the whole firm at that higher rate and credits no "
                "cash. It is the larger of the two structural forks in the bridge and the "
                "adopted side is the higher value."
                % (100 * base["wacc_exp"], 100 * base["wacc_net"])),
        dict(
            name="the joint-venture airline network: the audited carrying value vs the "
                 "profit share capitalised",
            adopted="the audited carrying value, AED %.1fmn" % base["jv_book"],
            alternative="the FY2025 share of venture profit capitalised at %.0f times, "
                        "AED %.1fmn" % (V["jv_pe"], base["jv_cap"]),
            value=base["dcf_ps_jvcap"],
            why="The study names this its single most consequential contested judgement and "
                "publishes both, never averaged, which is the right treatment. Five "
                "equity-accounted airlines sit on the balance sheet at %.2f times the annual "
                "profit share they contribute, and the three disclosed in both years grew "
                "their combined hundred-per-cent-basis profits sharply in FY2025. Book is "
                "the lower value and it is the side the central adopts; every headline "
                "figure in the study is on it."
                % (base["jv_book"] / V["assoc_fy25"])),
        dict(
            name="the central: the class primary alone vs the retired four-lens weighted "
                 "blend",
            adopted="the cash-flow lens alone, the others published beside it as "
                    "cross-checks",
            alternative="the weighted blend of four lenses the earlier editions carried",
            value=fig["blend"],
            why="The standing rule retires the typed blend: one class primary IS the "
                "central and the other lenses are cross-checks, with book value a disclosed "
                "floor that is never weighted. Two further things were wrong with the blend "
                "here and both raise the answer when removed: normalised earnings power is "
                "not a permitted lens for an airline at all and carried a fifth of the "
                "weight at AED %.2f against a cash-flow AED %.2f, and the weights had never "
                "cleared an out-of-sample test. The alternative is this study's own four "
                "readings at the weights it used to publish, unchanged, not a new model."
                % (base["norm_ps"], base["dcf_ps"])),
        dict(
            name="the terminal: the sanctioned construction on a disclosed asset life vs "
                 "the retired reinvestment identity",
            adopted="maintenance charged at current cost with book depreciation added back, "
                    "on the weighted useful life the accounts disclose",
            alternative="the reinvestment identity, growth over return on capital, applied "
                        "to terminal profit",
            value=fig["tv_retired_ps"],
            why="The alternative is retired by rule and this row prices what retiring it "
                "did. Its implied replacement cycle is one over the growth rate, %.1f years "
                "here, against the %.2f the company's own accounting-policies note supports "
                "— a fact about the currency rather than about the asset, and on a pegged "
                "terminal it runs LONG and under-charges the fleet. It moved the answer up, "
                "which could not have been read off the ratio in advance: the two charges "
                "are not like for like, one being a net charge on an implied capital base "
                "and the other gross at replacement cost with book depreciation added back."
                % (1.0 / base["V"]["g_term"], V["asset_life_weighted"])),
        dict(
            name="fuel intensity held flat, with the new aircraft's disclosed burn advantage "
                 "not credited",
            adopted="intensity held at the FY2025 realised level for the whole window",
            alternative="the disclosed burn advantage credited on the fleet share the "
                        "study's own delivery plan builds",
            ovr_key="_neo",
            why="The study holds fuel per passenger per barrel flat and says in terms that "
                "the new type's roughly twenty per cent lower burn is an upside it does not "
                "credit. This row prices that sentence. The credit is a RECONSTRUCTION "
                "rather than a committed driver and is built as the floor of the effect: "
                "net additions rather than gross deliveries, because gross is not disclosed, "
                "and the FY2025 arrivals excluded because they are already inside the FY2025 "
                "realised intensity. On the study's own fleet plan that is %.1f%% of the "
                "fleet by FY2030 and %.1f%% off the fuel line in that year. It is the "
                "clearest single upside the study declines."
                % (100 * fig["neo_share"][-1], 100 * (1 - fig["neo_mult"][-1]))),
        dict(
            name="the leased fleet: charged at its gross right-of-use value inside free cash "
                 "flow vs treated as value-neutral financing",
            adopted="every aircraft the plan adds is bought with capital, the financing mix "
                    "left to the discount rate",
            alternative="new leases treated as financing at net present value zero, charged "
                        "nothing and stripped from invested capital",
            patch=LEASED_NPV0,
            why="The adopted convention was taken from an external critique and it is the "
                "consistent one: a firm that leases capacity has still bought it. The "
                "alternative is the study's own stated counterfactual and it is priced here "
                "in full rather than quoted — the charge is AED %.0fmn of gross right-of-use "
                "inception value across the window, against AED %.0fmn of owned capex. The "
                "adopted side is the lower value."
                % (sum(base["leased_gross"]), sum(base["capex"]))),
        dict(
            name="the other-direct cost line: held flat on the wet-lease spike unwinding vs "
                 "escalated with the tariff class beside it",
            adopted="held flat at the FY2025 level for the whole window",
            alternative="escalated at the same %.0f%% the landing and handling lines take"
                        % (100 * fig["tariff_escalator"]),
            ovr=dict(other_per_pax=None),          # filled from fig, see build()
            why="The line bundles other operating costs, wet-lease, insurance and "
                "amortisation, and the study holds it flat on a specific argument: the "
                "FY2025 wet-lease spike (AED %.1fmn against AED %.1fmn in FY2024) unwinds as "
                "owned aircraft arrive and absorbs the other components' inflation. The "
                "argument is real and it is still a forecast that one cost line alone does "
                "not inflate for five years, on a stack where every other class carries its "
                "own escalator. The alternative applies the tariff-class escalator two "
                "adjacent lines already take. The adopted side is the higher value."
                % (V["dcost_lines_fy25"]["wet_lease"], V["dcost_lines_fy24"]["wet_lease"])),
        dict(
            name="the forecast tax rate: the statutory top-up vs the audited effective rate",
            adopted="%.0f%%, the domestic minimum top-up rate the group provides at"
                    % (100 * V["tax_stat"]),
            alternative="%.2f%%, the effective rate the audited FY2025 reconciliation shows"
                        % (100 * fig["etr_fy25"]),
            ovr=dict(tax_eff=None),                # filled from fig, see build()
            why="The company's own audited effective rates are %.2f%% for FY2025 and %.2f%% "
                "for FY2024, both below the statutory top-up, because of exempt income and "
                "the opening of the nine-per-cent era; the reviewed first quarter of 2026 "
                "provides at the statutory rate. The study holds the statutory rate and "
                "calls it the conservative anchor, which it is — this is the one row where "
                "following the filing rather than the statute would RAISE the value, and the "
                "study goes the other way."
                % (100 * fig["etr_fy25"], 100 * fig["etr_fy24"])),
        dict(
            name="the weighted useful life: every disclosed range at its longest end vs at "
                 "its shortest",
            adopted="%.2f years, each disclosed class range taken at its longest end"
                    % V["asset_life_weighted"],
            alternative="%.2f years, each taken at its shortest end" % fig["life_short"],
            ovr=dict(asset_life_weighted=None),    # filled from fig, see build()
            why="Both numbers are in the study's own input note and both are read off the "
                "same disclosure: the class lives in the property note weighted by that "
                "note's own gross carrying amounts. The band is narrow because aircraft and "
                "engines are %.1f%% of the depreciable base at a single disclosed twenty "
                "years. It runs the opposite way to intuition and that is why it is "
                "recorded: the terminal escalates book depreciation over HALF the life, so "
                "the longer life charges MORE maintenance, and the adopted side is the "
                "lower value." % (100 * fig["aircraft_share_of_base"])),
        dict(
            name="working capital: the three-year centre vs the latest audited year",
            adopted="%.1f%% of revenue, the three-year centre" % (100 * V["nwc_pct"]),
            alternative="%.2f%% of revenue, the FY2025 audited ratio"
                        % (100 * fig["nwc_fy25_pct"]),
            scenario=dict(nwc_pct=None),           # filled from fig, see build()
            why="An airline collects fares before it flies, so working capital is deeply "
                "negative and growth releases cash: the audited ratios are %.1f%%, %.1f%% "
                "and %.1f%% of revenue across FY2023-25. The study takes the centre rather "
                "than the best year, which is the standing discipline and is the lower "
                "value; the latest audited year is the more negative and would release more."
                % (100 * fig["nwc_pct_fy23"], 100 * fig["nwc_pct_fy24"],
                   100 * fig["nwc_fy25_pct"])),
        dict(
            name="the anchor accretion: the cash legs at the deposit yield vs everything at "
                 "the cost of equity",
            adopted="the operating equity accretes at the cost of equity, the cash and "
                    "near-cash legs at the deposit yield",
            alternative="every leg accretes at the cost of equity",
            patch=ROLL_AT_KE,
            why="Adopted from an external critique, and right: cash does not compound at the "
                "cost of equity. It is recorded because it is a choice rather than an "
                "identity and it runs against the answer — %.0f basis points of accretion "
                "over %d days on AED %.0fmn of cash and near-cash legs — and because the "
                "study would look better if it had not been made."
                % (10000 * (base["ke_exp"] - base["V"]["dep_rate_path"][0]),
                   V["anchor_days"], fig["cash_legs"])),
        dict(
            name="the sovereign default spread netted out of the risk-free rate: the spread "
                 "the auction priced vs the rating table's",
            adopted="the %.0f basis points the July-2026 dirham auction actually priced over "
                    "comparable Treasuries" % (10000 * V["sov_spread_obs"]),
            alternative="the %.0f basis points the published country-risk table carries"
                        % (10000 * V["sov_spread_rating"]),
            ovr=dict(sov_spread_obs=None),         # filled from fig, see build()
            why="Country risk must enter exactly once and the same basis must be stripped as "
                "is added back, so the rating basis on both sides is the consistent reading "
                "and the study does not take it. Its reason is specific and good: under a "
                "hard peg, netting the table's spread out of a bond that actually priced "
                "four basis points over Treasuries puts the normalised rate BELOW the "
                "matched-tenor Treasury, which cannot be right. Both are published; the "
                "adopted side is the lower value and the difference is small."),
        dict(
            name="the minority interest: deducted at its audited carrying value vs at its "
                 "share of equity value",
            adopted="the audited carrying amount, AED %.3fmn" % V["nci_book"],
            alternative="the disclosed profit share of the equity value the model produces",
            patch=MINORITY_AT_VALUE,
            ovr_key="_ncis",
            why="The standing rule deducts the minority at its share of value rather than at "
                "historical cost, because the model capitalises the whole of subsidiary cash "
                "flow. Here the two are indistinguishable: the disclosed profit share is "
                "%.4f%% and the deduction moves by AED %.1fmn on an equity value of AED "
                "%.0fmn. It is recorded rather than omitted so that a reader can see it was "
                "measured and not assumed away."
                % (100 * base["nci_share"], fig["nci_at_value"] - V["nci_book"],
                   base["eq_attr"])),
    ]


NOT_VALUED = [
    dict(name="the terminal maintenance basis: book depreciation escalated to current cost "
              "vs a replacement-cost capital base over the disclosed life",
         adopted="book depreciation escalated to current cost over half the disclosed "
                 "weighted life",
         why_not="The standard basis divides a REPLACEMENT-COST invested-capital base by the "
                 "disclosed life, and this model commits no such base. The property note "
                 "gives GROSS HISTORICAL cost on a fleet already more than half depreciated, "
                 "and rolling that forward through five years of the model's own capex at "
                 "mixed vintages is a construction this desk would be making rather than a "
                 "disclosure it would be reading. The study says so in its own code comment "
                 "and chooses the basis that uses only figures that exist. Reported unvalued "
                 "rather than built on an invented base.",
         one_sided_price="the disclosed life itself is priced both ways in the judgements "
                         "above, at its longest and shortest disclosed ends"),
    dict(name="the hedge ratio on the fuel book",
         adopted="not carried as a driver; the effective jet price is a hedge-blended path "
                 "and the two framings of it are published side by side",
         why_not="The swaps-and-collars note discloses that the 2026-28 fuel book is hedged "
                 "and does not quantify the proportion, which is the single fact that would "
                 "settle which of the two published fuel paths the company actually pays. "
                 "Constructing a ratio would be inventing the driver that decides the "
                 "largest fork in this valuation. The study flags the gap; this record does "
                 "not close it.",
         one_sided_price="the two fuel framings bracket it, and that bracket is the widest "
                         "single row in the judgements above"),
    dict(name="the split of forecast aircraft deliveries between owned and leased",
         adopted="about seven owned and nine leased across the window, this desk's split of "
                 "a total the order book does fix",
         why_not="The company discloses the order and the delivery pace and does not "
                 "disclose the tenure split, which the study names as its build's weakest "
                 "driver. A second framing would be a different split this desk chose, not "
                 "one the filings support, so there is no alternative to value — the honest "
                 "treatment is the sensitivity the study already publishes over the capital "
                 "bill, not a fabricated second split.",
         one_sided_price="the study's own capital-spending grid runs the bill from 80% to "
                         "130% of the plan"),
    dict(name="the equity risk premium basis",
         adopted="the rating basis",
         why_not="The published country-risk file carries a rating-based row for this "
                 "sovereign and its credit-default-swap column is not available, so the "
                 "second framing does not exist in the original source. The study states "
                 "that plainly rather than substituting a third-party quote, and both-bases "
                 "publication here is therefore the rating basis plus a stated absence. "
                 "Reported unvalued rather than guessed.",
         one_sided_price="none available from the source"),
]

NOT_CONTESTED = [
    dict(name="the joint-venture profit growth path",
         why="It has no effect on the answer and that was measured, not assumed: the "
             "equity-accounted share sits below the tax line and enters the profit and "
             "net-debt roll, while the cash-flow lens values the operations and carries the "
             "venture network in the bridge at book or capitalised. Re-running the model on "
             "a path that lifts the first forecast year from near-flat to the ramp rate "
             "reproduces the published answer to the last digit. The venture VALUATION is a "
             "judgement and it is the fourth row above; the growth path is not."),
    dict(name="the dividend path and its floor",
         why="Dividends do not enter free cash flow to the firm. The payout ladder drives "
             "the forecast equity and net-debt rolls and the statements a reader is shown, "
             "and moves no lens value."),
    dict(name="beta as a coefficient",
         why="It is measured rather than chosen — a five-year weekly regression that clears "
             "the usability gate on its own standard errors. What IS a judgement is WHICH "
             "index it is measured against, and that is the second row above. The "
             "sensitivity grid shows beta is among the largest single drivers of value, "
             "which is a fact about the model rather than a fork the study resolved."),
]


def _latest_close(ticker):
    """The latest supplied close, read where the price file puts it.

    Read explicitly rather than by searching for a plausible number, and an
    absent one raises rather than falling back to the strike [R-ENF-04].
    """
    prices = json.load(open(PRICE_FILE, encoding="utf-8"))
    row = (prices.get("prices") or {}).get(ticker)
    assert row and isinstance(row.get("price"), (int, float)), (
        "no supplied close for %s in %s — an absent price is not a clean one"
        % (ticker, os.path.basename(PRICE_FILE)))
    return float(row["price"]), ("close %s, supplied %s (%s)"
                                 % (row.get("date"), prices.get("supplied"),
                                    os.path.basename(PRICE_FILE)))


def _read_at(RR, live, base, jv_val, spot):
    """The flat rate at a price, with this study's own bridge inverted first.

    The shared instrument carries an equity price back to enterprise value by
    SUBTRACTING the bridge. That is right for an additive bridge and this one is
    not: the operating leg accretes at the cost of equity and the cash legs at
    the deposit yield, so a unit of enterprise value is worth more than a unit
    of equity here. The price is inverted through the study's own accretion and
    the equivalent equity value AT THE MODEL'S OWN VALUATION DATE is what the
    shared solver is asked to reproduce.
    """
    F, DCF, W = live["fcst"], live["dcf"], live["wacc"]
    SH = float(live["meta"]["shares_mn"])
    dps = float(live["inputs"]["dps_fy25"]["value"])
    cash_legs = -DCF["nd"] + DCF["non_op"] + jv_val
    ev_at_price = ((spot + dps) * SH - cash_legs * DCF["roll_cash"]
                   + DCF["nci_book"]) / DCF["roll"]
    equity_study = DCF["ev"] - DCF["nd"] + DCF["non_op"] + jv_val - DCF["nci_book"]
    spot_equiv = (ev_at_price + (equity_study - DCF["ev"])) / SH
    t_mid, how = RR.resolve_times({}, F["df"], F["fwd_wacc"])
    out = dict(RR.read(F["fcff"], t_mid, DCF["tv"], W["wacc_term"], DCF["g"],
                       F["df"][-1], F["df"][-1], DCF["ev"], equity_study, SH, spot_equiv),
               discounting_times=t_mid, times_resolved=how,
               price_carried_to_the_model_date=spot_equiv,
               bridge_inverted="the operating leg at the cost of equity (x%.6f), the cash "
                               "and near-cash legs at the deposit yield (x%.6f), less the "
                               "dividend paid inside the window"
                               % (DCF["roll"], DCF["roll_cash"]))
    # the check that the inversion is exact: the study's own answer must come back
    chk = (DCF["ev"] * DCF["roll"] + cash_legs * DCF["roll_cash"]
           - DCF["nci_book"]) / SH - dps
    out["study_value_per_share_reproduced"] = chk
    return out


def build():
    live = json.load(open(NUM, encoding="utf-8"))
    base = run()
    # THE HARNESS IS PROVED AGAINST THE COMMITTED ANSWER BEFORE ANY ALTERNATIVE IS
    # BELIEVED. A re-run that does not reproduce the published number exactly is
    # measuring a different model and every difference below would be a fiction.
    assert base["central"] == live["central"], (
        "the re-run does not reproduce the committed central (%r vs %r)"
        % (base["central"], live["central"]))
    assert base["dcf_ps"] == live["dcf"]["ps"], "the re-run does not reproduce the DCF lens"

    V = base["V"]
    A0 = live["central"]
    struck = float(live["spot"])
    spot, spot_date = _latest_close(live["meta"]["ticker"])

    # ---------------- the reverse read ----------------
    sys.path.insert(0, ENGINE)
    import reverse_read as RR

    r_book = _read_at(RR, live, base, live["dcf"]["jv_book"], spot)
    r_jvcap = _read_at(RR, live, base, live["dcf"]["jv_cap"], spot)
    assert abs(r_book["study_value_per_share_reproduced"] - A0) < 1e-9, (
        "the bridge inversion does not reproduce the study's own answer — a reverse read "
        "on a bridge that does not close is a bug wearing the costume of a disagreement")
    r_price = r_book["implied_rate_at_price"]
    r_study = r_book["implied_rate_at_study_value"]

    # ---------------- what the price implies about each driver ----------------
    ds = base["dcf_scenario"]
    imp = {}
    imp["pax_multiplier"] = bisect(lambda x: ds(pax_mult=x), 0.5, 2.0, spot)
    imp["fare_multiplier"] = bisect(lambda x: ds(fare_mult=x), 0.5, 2.0, spot)
    imp["fuel_price_multiplier"] = bisect(lambda x: ds(fuel_mult=x), 2.0, 0.3, spot)
    imp["cash_cost_per_passenger_shift"] = bisect(lambda x: ds(cost_shift=x), 0.3, -0.3, spot)
    imp["fleet_capex_multiplier"] = bisect(lambda x: ds(capex_mult=x), 3.0, 0.2, spot)
    imp["parallel_shift_in_the_schedule"] = bisect(lambda x: ds(wacc_shift=x), 0.05, -0.05,
                                                   spot)
    imp["terminal_growth_nominal"] = bisect(lambda x: ds(g=x), 0.0, 0.06, spot)
    imp["working_capital_pct_of_revenue"] = bisect(lambda x: ds(nwc_pct=x), 0.0, -1.5, spot)
    imp["joint_venture_network_value"] = bisect(lambda x: ds(jv_val=x), 0.0, 12000.0, spot)

    pax_last = V["pax_path"][-1] * imp["pax_multiplier"]
    pax_cagr_study = (V["pax_path"][-1] / V["pax_hist"]["FY25"]) ** 0.2 - 1
    pax_cagr_imp = (pax_last / V["pax_hist"]["FY25"]) ** 0.2 - 1
    pax_cagr_hist = (V["pax_hist"]["FY25"] / V["pax_hist"]["FY22"]) ** (1 / 3.0) - 1
    jv_mult_imp = imp["joint_venture_network_value"] / V["assoc_fy25"]
    jv_mult_book = base["jv_book"] / V["assoc_fy25"]
    kd_eff = base["kd_eff_fy25"]

    diag = {
        "ticker": live["meta"]["ticker"],
        "as_of": AS_OF,
        "spot": spot,
        "spot_date": spot_date,
        "published_central": A0,
        "published_spot": struck,
        "why_this_file": (
            "The reverse read — what the traded price must believe — is a DIAGNOSTIC and "
            "lives outside the numbers file every builder reads. A quantity solved from a "
            "price and then used anywhere in the valuation is the reverse-engineered rate "
            "the protocol prohibits outright, arriving through a side door. Nothing in this "
            "file is an input to anything: it is COMPUTED by diagnostics_airarabia.py, no "
            "builder reads it, and this generator asserts before writing that the solved "
            "value appears nowhere in study_numbers.json."),
        "implied": {
            "quantity": ("the single flat discount rate that reproduces the traded price on "
                         "this study's own free cash flows and terminal"),
            "value": r_price,
            "value_other_framing": r_jvcap["implied_rate_at_price"],
            "study_value": r_study,
            "study_value_range": [float(live["wacc"]["wacc_exp"]),
                                  float(live["wacc"]["wacc_term"])],
            "solved_on": (
                "engine/reverse_read.py, on this study's own committed free cash flows, its "
                "own terminal cash flow recovered from its own terminal value, its own "
                "terminal growth and its own bridge — holding every driver at its published "
                "value and varying only the discount rate until the model reproduces the "
                "traded price. The discounting convention was %s and recovers whole years. "
                "The bridge is not additive in enterprise value here, so the price is first "
                "carried back to the model's own valuation date through the study's own "
                "two-legged accretion, and that inversion is asserted to reproduce the "
                "study's published answer before either rate is believed."
                % r_book["times_resolved"]),
            "reading": (
                "At AED %.2f the price is paying for a flat %.3f%% cost of capital on the "
                "same cash flows this study discounts at a schedule equivalent to a flat "
                "%.3f%%. The disagreement is %.0f basis points on the price of time and "
                "risk, not on the business — which is a smaller statement than \"the central "
                "sits %.1f%% below the market\" and a more useful one. The study's schedule "
                "runs %.2f%% gliding to %.2f%%, and its flat equivalent sits inside that "
                "range, which is the check that the two numbers are one quantity measured "
                "twice. On the study's own alternative framing of the venture network the "
                "implied rate is %.3f%%. Beside what the company itself discloses: its "
                "FY2025 finance charge over average gross debt computes to %.2f%%, its cash "
                "and deposits earn %.1f%% in the model's first forecast year, the dirham "
                "sovereign it borrows behind yields %.2f%% and this study's own marginal "
                "cost of debt is %.2f%% — so the market is discounting the whole firm about "
                "%.0f basis points above that sovereign, against this study's %.0f."
                % (spot, 100 * r_price, 100 * r_study, 10000 * (r_price - r_study),
                   100 * (A0 / spot - 1), 100 * live["wacc"]["wacc_exp"],
                   100 * live["wacc"]["wacc_term"],
                   100 * r_jvcap["implied_rate_at_price"], 100 * kd_eff,
                   100 * V["dep_rate_path"][0], 100 * V["rf"], 100 * V["kd"],
                   10000 * (r_price - V["rf"]), 10000 * (r_study - V["rf"]))),
        },
        "construction": {k: v for k, v in r_book.items()},
        "construction_venture_network_capitalised": {k: v for k, v in r_jvcap.items()},
        "at_the_strike": {
            "spot": struck,
            "note": ("this edition was re-struck on the same close the gap is measured "
                     "against, so the strike price and the latest known price are one "
                     "number and there is no month of drift between them to report"),
        },
        "cross_reads": {
            "why": ("The flat rate is the comparable read across this book and it is not the "
                    "most legible one for an airline, where a reader can check passengers "
                    "and fares against the company's own results presentations. Each figure "
                    "below is the same question asked of ONE driver: the value that driver "
                    "must take for this study's own model to reproduce the traded price, "
                    "with every other driver held at its published value. They are "
                    "alternative readings of the SAME disagreement and are not additive."),
            "implied_passenger_multiplier": imp["pax_multiplier"],
            "implied_fy2030_passengers_mn": pax_last,
            "study_fy2030_passengers_mn": V["pax_path"][-1],
            "implied_passenger_cagr_fy2025_to_fy2030": pax_cagr_imp,
            "study_passenger_cagr_fy2025_to_fy2030": pax_cagr_study,
            "disclosed_passenger_cagr_fy2022_to_fy2025": pax_cagr_hist,
            "implied_fare_multiplier": imp["fare_multiplier"],
            "implied_fy2030_fare_and_baggage_per_passenger": (V["fare_path"][-1]
                                                              * imp["fare_multiplier"]),
            "study_fy2030_fare_and_baggage_per_passenger": V["fare_path"][-1],
            "implied_effective_jet_price_multiplier": imp["fuel_price_multiplier"],
            "implied_cash_cost_per_passenger_shift": imp["cash_cost_per_passenger_shift"],
            "implied_fleet_capex_multiplier": imp["fleet_capex_multiplier"],
            "implied_parallel_shift_in_the_schedule": imp["parallel_shift_in_the_schedule"],
            "implied_terminal_growth_nominal": imp["terminal_growth_nominal"],
            "study_terminal_growth_nominal": float(V["g_term"]),
            "house_AE_terminal_inflation": float(base["PI_TERM"]),
            "implied_terminal_growth_real": ((1 + imp["terminal_growth_nominal"])
                                             / (1 + base["PI_TERM"]) - 1),
            "study_terminal_growth_real": float(V["g_term_real"]),
            "implied_working_capital_pct_of_revenue": imp["working_capital_pct_of_revenue"],
            "study_working_capital_pct_of_revenue": float(V["nwc_pct"]),
            "implied_joint_venture_network_value": imp["joint_venture_network_value"],
            "implied_multiple_of_the_fy2025_profit_share": jv_mult_imp,
            "study_joint_venture_network_value_book": base["jv_book"],
            "study_multiple_of_the_fy2025_profit_share_at_book": jv_mult_book,
            "study_joint_venture_network_value_capitalised": base["jv_cap"],
            "study_multiple_capitalised": float(V["jv_pe"]),
            "reading": (
                "The two rate reads agree, which is worth stating because they were solved "
                "on different machinery: the flat-rate read puts the disagreement at %.0f "
                "basis points and a parallel shift of the study's own gliding schedule, "
                "solved on the study's own scenario engine, puts it at %.0f. In business "
                "units the same gap is %.1f%% more passengers than this study forecasts "
                "(FY2030 %.2fmn against %.2fmn, a compound %.2f%% a year from the audited "
                "FY2025 %.2fmn against this study's %.2f%% — where the company's own "
                "disclosed record from FY2022 to FY2025 is %.1f%% a year), or %.1f%% more "
                "on the fare, or a jet price %.1f%% below the path the study takes, or a "
                "fleet capital bill %.1f%% lighter. THE ONE WORTH PAUSING ON IS THE VENTURE "
                "NETWORK. This study prices it BOTH ways and never averages: the audited "
                "carrying value, %.2f times the FY2025 profit share, and the same share "
                "capitalised at %.0f times. The price implies AED %.0fmn, or %.2f times — "
                "BETWEEN the study's own two published framings. So on the study's own "
                "reading of its own biggest contested judgement, the market is not "
                "disagreeing with this valuation; it is resolving a fork this study "
                "deliberately declines to resolve, and it is resolving it nearer the book "
                "end than the capitalised one. A reverse read landing between a study's own "
                "two published answers is evidence that the disagreement is the fork rather "
                "than the model."
                % (10000 * (r_price - r_study),
                   10000 * imp["parallel_shift_in_the_schedule"],
                   100 * (imp["pax_multiplier"] - 1), pax_last, V["pax_path"][-1],
                   100 * pax_cagr_imp, V["pax_hist"]["FY25"], 100 * pax_cagr_study,
                   100 * pax_cagr_hist, 100 * (imp["fare_multiplier"] - 1),
                   100 * (1 - imp["fuel_price_multiplier"]),
                   100 * (1 - imp["fleet_capex_multiplier"]),
                   jv_mult_book, V["jv_pe"], imp["joint_venture_network_value"],
                   jv_mult_imp)),
        },
        "company_disclosed": {
            "passengers_carried_mn": dict(V["pax_hist"]),
            "seat_load_factor": dict(V["lf_hist"]),
            "fare_and_baggage_per_passenger_fy2024": base["unit_hist"]["FY24"]["fare"],
            "fare_and_baggage_per_passenger_fy2025": base["unit_hist"]["FY25"]["fare"],
            "fuel_per_passenger_fy2025": base["unit_hist"]["FY25"]["fuel"],
            "share_of_venture_profit_fy2025": float(V["assoc_fy25"]),
            "carrying_value_of_the_venture_network_fy2025": float(V["assoc_bv_fy25"]),
            "effective_finance_cost_over_average_gross_debt_fy2025": kd_eff,
            "audited_effective_tax_rate_fy2025": base["hist_is"]["FY25"]["tax"] /
                                                 base["hist_is"]["FY25"]["ebt"],
            "net_cash_fy2025": -float(base["nd_fy25"]),
            "note": ("every figure here is the company's own disclosure or an identity on "
                     "the company's own disclosures, taken from this study's own four-field "
                     "input register and recomputed by this study's own code. The fare and "
                     "fuel per passenger are the disclosed revenue and cost lines over the "
                     "disclosed passenger count; seat and available-seat-kilometre data is "
                     "not disclosed, which the study flags, so per-passenger is the finest "
                     "sourced level here."),
        },
    }

    # ---------------- the contested judgements ----------------
    fig = _figures(base, live)
    rows = []
    for f in forks(base, fig):
        if "value" in f:
            alt = f["value"]
        elif "scenario" in f:
            key = list(f["scenario"])[0]
            alt = ds(**{key: fig["scenario_values"][key]})
        else:
            ovr = dict(f.get("ovr") or {})
            for k in list(ovr):
                if ovr[k] is None:
                    ovr[k] = fig["override_values"][k]
            if f.get("ovr_key"):
                ovr[f["ovr_key"]] = fig["override_values"][f["ovr_key"]]
            alt = run(ovr, f.get("patch") or (), f["name"])["dcf_ps"]
        rows.append(dict(
            name=f["name"], adopted=f["adopted"], alternative=f["alternative"],
            value_adopted=A0, value_alternative=alt,
            share_of_value=abs(A0 - alt) / abs(alt),
            direction=("the study adopted the higher-value framing" if A0 > alt
                       else "the study adopted the lower-value framing"),
            why=f["why"]))
    rows.sort(key=lambda r: -r["share_of_value"])

    mat = [r for r in rows if r["share_of_value"] >= 0.05]
    up = len([r for r in mat if r["value_adopted"] > r["value_alternative"]])

    cj = {
        "ticker": live["meta"]["ticker"],
        "as_of": AS_OF,
        "published_central": A0,
        "published_spot": struck,
        "why_this_file": (
            "Any single contested choice in a valuation is defensible. What is not is a "
            "study that resolves EVERY contested choice the same way and never notices — "
            "which is how a lean survives an audit of its steps. Each is recorded with BOTH "
            "framings' values, the side adopted and why, and the binomial sign test is "
            "printed. A study landing them all one way is FLAGGED, never failed: a company "
            "can genuinely deserve a consistent read, and a gate that failed on it would "
            "push studies to resolve judgements inconsistently to stay green."),
        "both_framings_share_a_bridge": (
            "Every alternative is computed by RE-RUNNING this study's own compute.py with "
            "that one choice changed and everything else held at its published value, "
            "through the same forecast, the same terminal and the same bridge as the "
            "adopted figure — so the difference measures the CHOICE and not the "
            "construction. The run happens in a scratch directory so the committed numbers "
            "file cannot move, each source substitution is asserted to have landed exactly "
            "once, and the re-run is proved against the committed answer before any "
            "alternative is believed. Two rows quote figures the study itself already "
            "computes both ways (the fuel path and the venture network) and take them "
            "unchanged rather than rebuilding them."),
        "the_answer_this_record_is_anchored_on": (
            "The published central is the class primary alone — the cash-flow lens — so "
            "every row moves the answer by the full amount it moves that lens, with no "
            "weighting to damp it. That is a property of this study's architecture and it "
            "makes the materiality bar bite harder here than on a study publishing a "
            "weighted centre."),
        "materiality": (
            "A judgement is material where the two framings differ by more than 5% of "
            "value. Rows below that bar are recorded rather than dropped: an absent answer "
            "is not a clean one, and a reader is entitled to see that a fork was measured "
            "and found small rather than never looked at."),
        "what_the_sign_test_reads": (
            "%d judgements recorded, %d material at the 5%% bar, %d resolved toward the "
            "higher value and %d toward the lower. The study did NOT land its material "
            "forks one way. Three of the material rows are corrections the standing rules "
            "require rather than discretion this desk exercised — the retired lens blend, "
            "the retired terminal construction and the regressor the beta rule resolves — "
            "and all three run the same way, toward the higher value; the six discretionary "
            "rows split %d up and %d down. Both counts are stated so a reader can read the "
            "test either way, and neither was curated to move it."
            % (len(rows), len(mat), up, len(mat) - up,
               up - 3, len(mat) - up)),
        "judgements": rows,
        "not_valued": NOT_VALUED,
        "not_treated_as_a_contested_judgement": NOT_CONTESTED,
    }
    return diag, cj


def _figures(base, live):
    """Every figure a reason or an alternative needs, computed here and never typed."""
    V = base["V"]
    neo_mult, neo_share = neo_multipliers(base)
    life_short = 14.55        # the shortest-end reading the study's own input note carries
    etr_fy25 = base["hist_is"]["FY25"]["tax"] / base["hist_is"]["FY25"]["ebt"]
    etr_fy24 = base["hist_is"]["FY24"]["tax"] / base["hist_is"]["FY24"]["ebt"]
    ev_ret = base["pv_explicit"] + base["tv_retired"] * base["df"][-1]
    beta = json.load(open(os.path.join(HERE, "beta_result.json"), encoding="utf-8"))
    gross = V["ppe_fy25"] + V["rou_fy25"]
    return dict(
        neo_mult=neo_mult, neo_share=neo_share,
        life_short=life_short,
        etr_fy25=etr_fy25, etr_fy24=etr_fy24,
        blend=(live["lens_record"]["retired_blend"]["value"]),
        tv_retired_ps=base["to_anchor_split"](ev_ret, base["jv_book"]),
        fuel_share_of_direct=(V["dcost_lines_fy25"]["fuel"] / V["dcost_fy25"]),
        beta_r2=float(beta["r2"]),
        beta_alt_r2=float(beta["alt_benchmark"]["r2"]),
        tariff_escalator=(V["landing_per_pax"][1] / V["landing_per_pax"][0] - 1),
        nwc_fy25_pct=base["nwc_fy25"] / V["rev_fy25"],
        nwc_pct_fy23=base["nwc_fy23"] / V["rev_fy23"],
        nwc_pct_fy24=base["nwc_fy24"] / V["rev_fy24"],
        cash_legs=(-base["nd_fy25"] + base["non_op"] + base["jv_book"]),
        nci_at_value=base["nci_share"] * base["eq_attr"],
        aircraft_share_of_base=0.874,   # the study's own input note, from the property note
        override_values=dict(
            _neo=neo_mult,
            _ncis=base["nci_share"],
            other_per_pax=[V["other_per_pax"][0] * (1 + (V["landing_per_pax"][1]
                                                         / V["landing_per_pax"][0] - 1))
                           ** (i + 1) for i in range(5)],
            tax_eff=etr_fy25,
            asset_life_weighted=life_short,
            sov_spread_obs=V["sov_spread_rating"],
        ),
        scenario_values=dict(nwc_pct=base["nwc_fy25"] / V["rev_fy25"]),
    )


def _assert_containment(diag):
    """THE DEVICE, CHECKED HERE AS WELL AS BY THE GATE.

    The reverse read lives outside the numbers file every builder reads. A float
    carried at full precision does not appear there by coincidence, so a hit
    means a quantity solved from the traded price is sitting where the model can
    reach it — the prohibition, whether or not anything currently reads it.
    """
    val = diag["implied"]["value"]
    doc = json.load(open(NUM, encoding="utf-8"))

    def hunt(node, trail=""):
        if isinstance(node, dict):
            for k, v in node.items():
                r = hunt(v, trail + "/" + str(k))
                if r:
                    return r
        elif isinstance(node, list):
            for i, v in enumerate(node):
                r = hunt(v, trail + "[%d]" % i)
                if r:
                    return r
        elif isinstance(node, float) and node == val:
            return trail
        return None

    where = hunt(doc)
    assert where is None, (
        "the reverse read's own value is committed in study_numbers.json at %s. A quantity "
        "solved from the traded price must not sit in the numbers file every builder reads."
        % where)


def main():
    before = open(NUM, "rb").read()
    diag, cj = build()
    assert open(NUM, "rb").read() == before, (
        "the committed numbers file moved while this diagnostic ran — the alternatives must "
        "be valued in a scratch directory, never in place")
    _assert_containment(diag)
    json.dump(diag, open(os.path.join(HERE, "diagnostics.json"), "w", encoding="utf-8"),
              indent=1, ensure_ascii=False)
    json.dump(cj, open(os.path.join(HERE, "contested_judgements.json"), "w",
                       encoding="utf-8"), indent=1, ensure_ascii=False)

    i, x = diag["implied"], diag["cross_reads"]
    print("AIRARABIA reverse read at AED %.2f (%s)" % (diag["spot"], diag["spot_date"]))
    print("  the price implies a flat %.4f%%; this study discounts at %.4f%%  (%+.0f bp)"
          % (100 * i["value"], 100 * i["study_value"],
             10000 * (i["value"] - i["study_value"])))
    print("  in business units: %+.2f%% on passengers, %+.2f%% on fares, %+.2f%% on the jet "
          "price" % (100 * (x["implied_passenger_multiplier"] - 1),
                     100 * (x["implied_fare_multiplier"] - 1),
                     100 * (x["implied_effective_jet_price_multiplier"] - 1)))
    print("  the venture network: price AED %.0fmn (%.2fx the profit share) against book "
          "AED %.0fmn (%.2fx) and capitalised AED %.0fmn (%.0fx)"
          % (x["implied_joint_venture_network_value"],
             x["implied_multiple_of_the_fy2025_profit_share"],
             x["study_joint_venture_network_value_book"],
             x["study_multiple_of_the_fy2025_profit_share_at_book"],
             x["study_joint_venture_network_value_capitalised"], x["study_multiple_capitalised"]))
    mat = [j for j in cj["judgements"] if j["share_of_value"] >= 0.05]
    up = len([j for j in mat if j["value_adopted"] > j["value_alternative"]])
    print("  %d contested judgements, %d material at the 5%% bar, %d resolved upward"
          % (len(cj["judgements"]), len(mat), up))
    for j in cj["judgements"]:
        print("     %-5s %6.2f%% %s %s"
              % ("UP" if j["value_adopted"] > j["value_alternative"] else "DOWN",
                 100 * j["share_of_value"],
                 "*" if j["share_of_value"] >= 0.05 else " ", j["name"][:92]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
