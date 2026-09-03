#!/usr/bin/env python3
"""Projected vs actual on ARCC — ours, and an outside house's, scored the same way.

WHY THIS EXISTS. [R-GAP-01] audits an answer against a PRICE, which is the market's
opinion. This scores a forecast against what the company actually FILED, which is not
an opinion. The two answer different questions and only this one can find a systemic
bias, because a bias is a direction that repeats and a price disagreement is one
observation.

WHAT IT SCORES, and the second half is the point:
  1. OUR FY2026 forecast against ARCC's own filed first half, annualised where the
     line is a flow.
  2. EFG HERMES' 24-Nov-2025 forecast for FY2025 against the FY2025 audited outturn
     that their own 6-Aug-2026 edition prints — the only fully-resolved forecast
     either house has on this name.

THE SECOND ONE IS NOT A COURTESY. An outside forecast is worth reading only once you
know where it is biased, and this pair measures exactly that on the line that matters
most to our disagreement with them. Reading a target price without scoring the house
that wrote it is taking an opinion for evidence.

READ THE FIGURES HERE, never from a document: every number below carries the filing or
the edition it came from.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

# ARCC's own filings, as this study already parsed them cell by cell.
ACTUAL_H1_26 = {"revenue": 6080.58, "gross_profit": 2461.54, "pat": 2172.45,
                "capex": 608.43, "dna": 161.25}
ACTUAL_FY25 = {"revenue": 12447.3, "ebitda": 5017.0, "ebit": 4727.0,
               "net_income": 3398.0, "eps": 9.50, "capex": 799.0,
               "cash": 3459.0, "net_cash": 2324.0}
ACTUAL_CAPEX = {"FY2023": 58.54, "FY2024": 912.02, "FY2025": 796.47}

# EFG Hermes, 24-Nov-2025 edition (engine/external_research/EFG_ARCC_24-11-2025.pdf)
EFG_NOV25_FY25E = {"revenue": 12310, "ebitda": 5027, "ebit": 4744,
                   "net_income": 3348, "eps": 9.60, "capex": 288,
                   "cash": 2793, "net_cash": 2036}
EFG_NOV25_FWD = {"FY2026": {"revenue": 12440, "ebitda": 4843, "net_income": 3289},
                 "FY2027": {"revenue": 12557, "ebitda": 4731, "net_income": 3215}}
# EFG Hermes, 6-Aug-2026 edition — the same years, restated nine months later
EFG_AUG26_FWD = {"FY2026": {"revenue": 13144, "ebitda": 5132, "net_income": 3500},
                 "FY2027": {"revenue": 13528, "ebitda": 5485, "net_income": 3810}}

# our own FY2026 forecast, from engine/arcc_study/study_numbers.json
OURS_FY26 = {"revenue": 13349.3, "ebitda": 5210.0, "capex": 890.0, "dna": 343.7}


def rows():
    out = []
    # 1. OURS against the filed half, annualised. A half is not a year and the
    #    doubling is stated rather than hidden: cement is seasonal, so this is a
    #    RUN RATE, evidence of direction and not a restatement of the year.
    for k, ours in (("revenue", OURS_FY26["revenue"]), ("capex", OURS_FY26["capex"]),
                    ("dna", OURS_FY26["dna"])):
        run = ACTUAL_H1_26[k] * 2
        out.append(("ours FY2026 vs H1-2026 run rate", k, ours, run, ours / run - 1))
    # 2. EFG's fully resolved year
    for k in ("revenue", "ebitda", "ebit", "net_income", "eps", "capex", "cash",
              "net_cash"):
        out.append(("EFG Nov-2025 FY2025e vs FY2025 audited", k,
                    EFG_NOV25_FY25E[k], ACTUAL_FY25[k],
                    EFG_NOV25_FY25E[k] / ACTUAL_FY25[k] - 1))
    # 3. EFG's own revision of the SAME years, nine months apart. Not an error —
    #    a forecast is not wrong until it resolves — but a revision DIRECTION is
    #    evidence about the prior, and a house that revises one way twice was
    #    leaning.
    for y in ("FY2026", "FY2027"):
        for k in ("revenue", "ebitda", "net_income"):
            out.append(("EFG revision, Nov-2025 -> Aug-2026", "%s %s" % (y, k),
                        EFG_NOV25_FWD[y][k], EFG_AUG26_FWD[y][k],
                        EFG_NOV25_FWD[y][k] / EFG_AUG26_FWD[y][k] - 1))
    return out


def main():
    last = None
    for block, k, a, b, e in rows():
        if block != last:
            print("\n" + block)
            last = block
        print("  {:<24}{:>12}{:>12}  {:>+7.1f}%".format(
            k, format(a, ",.1f"), format(b, ",.1f"), e * 100))
    print("\nARCC's OWN FILED CAPEX: " + "  ".join(
        "%s %s" % (y, format(v, ",.0f")) for y, v in ACTUAL_CAPEX.items()))
    print("  H1-2026 alone: %s, of which %s is assets under construction —"
          % (format(ACTUAL_H1_26["capex"], ",.0f"), format(505.54, ",.0f")))
    print("  a PROGRAMME, which ends. Neither house models it ending.")


if __name__ == "__main__":
    main()
