#!/usr/bin/env python3
"""ELEC — the valuation-input block [R-FCAL-01 AMENDED], generated, never typed.

WHY IT EXISTS ON A RUN THAT IS A SKIP, which is the question this file has to answer.
The amendment's own reason is that "not carrying them means NO VALUATION THIS HOUSE
MAKES CAN EVER BE REBUILT AT A PAST ORIGIN, permanently, for any year whose filings are
no longer to hand." ELEC IS EXACTLY THAT CASE AND MORE SHARPLY THAN ANY NAME SO FAR:
the issuer lists 61 statement files and serves none of them (19 live-host files, all
404 on 07-09-2026, re-probed rather than taken on report), and the 42 consolidated ones
sit on a host whose DNS does not resolve. The four PDFs this repository happens to hold
are, as far as anything here can establish, the only copies within reach. So the block
is carried for every year that CAN be sourced, whether or not a walk-forward tested it.

WHAT `origins` MEANS HERE, SAID PLAINLY RATHER THAN LEFT TO BE INFERRED. This run's
scope is SKIP and it tested ZERO origins — `walkforward_origins_tested` is [] and says
so. The `origins` key is the schema's name for the years the BLOCK covers, which is
what a later value-rebuild consumes; it is not a claim that a forecast was struck from
those years. Recording untested years as walk-forward origins would misstate what the
run did, which the protocol forbids in terms, so the record declares both facts.

FY2020 sits under `prior_year_anchor`: it is a comparative column in the FY2021 filing
rather than a year with its own statement set in hand, and it is carried because a
dPPE identity at FY2021 needs it.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import filed_record as F                                        # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "valuation_inputs.json")
ORIGINS = ("FY2021", "FY2022", "FY2023")
ANCHOR = "FY2020"


def _src(y):
    b = F.BS[(y, "standalone")]
    f = F.FILINGS[b["src"]]
    return f["file"], f["route"], b


def block(y):
    file_, route, b = _src(y)
    cap = F.CAPEX[(y, "standalone")]
    dna = F.DNA[(y, "standalone")]
    cf_file = F.FILINGS[cap["src"]]["file"]
    cf_route = F.FILINGS[cap["src"]]["route"]

    return {
        "basis": "standalone — the company has issued no consolidated statement since "
                 "FY2020 while holding a 99.99% subsidiary (note 5), so this is the "
                 "parent entity and NOT the group the delivered study models.",
        "cash": {"value": b["cash"], "source": "%s, statement of financial position, "
                 "page %d, 'نقدية بالصندوق ولدى البنوك'" % (file_, b["page"]),
                 "route": route},
        "debt": {"value": F.debt(y),
                 "source": "%s, page %d — bank credit facilities + long-term loan + "
                           "lease and financing-arrangement liabilities (note 4/2), "
                           "current and non-current. INTEREST-BEARING ONLY: trade "
                           "payables, amounts due to related parties, tax liabilities, "
                           "provisions, deferred tax and dividends payable are excluded "
                           "because they bear no interest [R-FCAL-01 trap (i)]."
                           % (file_, b["page"]),
                 "route": route,
                 "components": {"credit_facilities": b["facilities"],
                                "long_term_loan": b["lt_loan"],
                                "lease_and_financing": b["lease_fin"]},
                 "total_liabilities_for_contrast": b["total_assets"] - b["equity"]},
        "ppe": {"value": b["ppe"],
                "source": "%s, page %d, 'أصول ثابتة' net book value" % (file_, b["page"]),
                "route": route,
                "right_of_use": b["rou"], "capital_work_in_progress": b["cip"]},
        "dep": {"value": dna["fixed"] + dna["rou"],
                "source": "%s, statement of cash flows, page %d — depreciation of fixed "
                          "assets %d plus amortisation of right-of-use assets %d. The "
                          "fixed-asset charge reconciles to note 3's own roll-forward "
                          "and to its allocation across cost of sales, selling and "
                          "administrative expenses."
                          % (cf_file, dna["page"], dna["fixed"], dna["rou"]),
                "route": cf_route},
        "capex": {"value": cap["fixed_assets"] + cap["cip"],
                  "derived": False,
                  "source": "%s, statement of cash flows, page %d, 'مدفوعات لشراء أصول "
                            "ثابتة' %d plus payments on projects under construction %d. "
                            "DISCLOSED, not derived: the identity capex = dPPE + D&A "
                            "does not close on these years because of large disposals "
                            "(FY2021 proceeds 103,532,162 on a book gain of 78,121,376), "
                            "and where the cash-flow statement discloses the figure the "
                            "amendment requires the disclosed one."
                            % (cf_file, cap["page"], cap["fixed_assets"], cap["cip"]),
                  "route": cf_route,
                  "advances_for_asset_purchases": cap["advances"]},
        "wc": {"value": (b["inventory"] + b["receivables"] + b["due_from_related"]
                         - b["payables"] - b["due_to_related"]),
               "source": "%s, page %d — inventory + trade and other receivables + due "
                         "from related parties, less trade and other payables and "
                         "amounts due to related parties" % (file_, b["page"]),
               "route": route,
               "lines": {"inventory": b["inventory"], "receivables": b["receivables"],
                         "due_from_related_parties": b["due_from_related"],
                         "payables": -b["payables"],
                         "due_to_related_parties": -b["due_to_related"]}},
        "shares": {"value": round(b["capital"] / b["par"]),
                   "issued_capital": b["capital"], "par_value": b["par"],
                   "source": "%s, page %d for the committed capital; the par value and "
                             "the identity come from the FY2021 filing's note 13 recital "
                             "(page 25), which states issued capital of 711,447,385 in "
                             "711,447,385 shares of EGP 1, a 1:5 split approved 2-Dec-2020 "
                             "and ratified by the listing committee on 24-Jan-2021 taking "
                             "par to EGP 0.20 and the count to 3,557,236,925. The count "
                             "for each year is THAT YEAR'S OWN committed capital over that "
                             "par; no count is carried back [R-FCAL-01 AMENDED (ii)]."
                             % (file_, b["page"]),
                   "route": route},
    }


def main():
    rec = {
        "_rule": "[R-FCAL-01 AMENDED] — a run commits the inputs a VALUE is rebuilt "
                 "from, not only the drivers.",
        "ticker": "ELEC", "currency": "EGP", "built": "2026-09-07",
        "scope": "skip",
        "walkforward_origins_tested": [],
        "_origins_key_means": (
            "THE YEARS THIS BLOCK COVERS, not walk-forward origins. This run's scope is "
            "SKIP — walk-forward not run — insufficient sourceable history (4 years) — "
            "so no forecast was struck from any year and none was scored. The block is "
            "committed anyway because these filings are, on today's evidence, "
            "unobtainable from the issuer, and a year whose figures are not written "
            "down now cannot be rebuilt later."),
        "_basis_warning": (
            "EVERY FIGURE HERE IS STANDALONE. The delivered study models CONSOLIDATED "
            "figures. The company has issued no consolidated statement since FY2020, so "
            "these are not comparable to the study's own panel and must never be "
            "substituted into it. The measured wedge at the one overlap year is in "
            "basis_breaks.md."),
        "_route": "All four filings carry no usable text layer. Figures were read off "
                  "the rendered pixels and every subtotal was re-added against its own "
                  "statement; filed_record.footing_report() reproduces the checks and "
                  "returns zero refusals.",
        "prior_year_anchor": {ANCHOR: block(ANCHOR)},
        "origins": {y: block(y) for y in ORIGINS},
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(rec, fh, indent=1, ensure_ascii=False)
    print("wrote", OUT)
    print("  anchor  %s" % ANCHOR)
    print("  covered %s" % ", ".join(ORIGINS))


if __name__ == "__main__":
    main()
