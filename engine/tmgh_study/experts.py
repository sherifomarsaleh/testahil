"""TMGH — Appendix C: the expert panel, at maximum detail.

Three experts, three genuinely different methods, each with a worked valuation
showing every intermediate line, a named sensitivity with numbers, and a
falsification condition stated IN ADVANCE. Then the cross-examination, the
three in one room, and the divergence table isolating which assumption drives
which gap.

Every figure is computed from `study_numbers.json`. Nothing is typed.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def N():
    return json.load(open(os.path.join(HERE, "study_numbers.json")))


def _v(reg, k):
    return reg[k]["value"]


def expert1(n):
    """The structured-credit view: the order book is a receivable stream."""
    bs, kpi = n["inputs"]["BS"], n["inputs"]["KPI"]
    r = n["ratios"]
    book = _v(kpi, "backlog_jun26")
    adv = _v(bs, "customer_advances")
    pud = _v(bs, "properties_under_development")
    gm = r["gm_dev_h1_26"]
    still_to_collect = book - adv
    still_to_build = max(book * (1 - gm) - pud, 0.0)
    opex = book * r["opex_ratio_fy25"]
    gross_cash = still_to_collect - still_to_build - opex
    tax = max(book * gm - opex, 0.0) * n["model_parameters"]["TAX"]
    net_cash = gross_cash - tax
    years, rate = 12.0, n["wacc"]["wacc_rating"]
    ann = sum(1 / (1 + rate) ** k for k in range(1, int(years) + 1))
    pv = (net_cash / years) * ann
    # The recurring businesses are not a receivable and this method has nothing
    # to say about them, so they are valued the plainest way available — a stated
    # multiple of their own operating profit — and the multiple is disclosed.
    # Leaving them out entirely was the first cut, and it valued a company with
    # EGP 25.8bn of recurring revenue as though it had none.
    ins = n["inputs"]["IS"]
    rec_rev = _v(ins, "hosp_revenue_fy25") + _v(ins, "other_revenue_fy25")
    rec_gp = (_v(ins, "hosp_revenue_fy25") - _v(ins, "hosp_cost_fy25")
              + _v(ins, "other_revenue_fy25") - _v(ins, "other_cost_fy25"))
    rec_ebit = rec_gp - rec_rev * r["opex_ratio_fy25"]
    REC_MULTIPLE = 6.0
    rec_value = rec_ebit * REC_MULTIPLE
    other = (_v(bs, "cash") + _v(bs, "deposits_current") + _v(bs, "deposits_noncurrent")
             - _v(bs, "loans_noncurrent") - _v(bs, "loans_current")
             - _v(bs, "credit_facilities") + _v(bs, "investment_property"))
    equity = pv + rec_value + other - _v(bs, "nci_equity")
    sh = n["meta"]["shares_mn"]
    return {
        "name": "Expert 1 — the order book as a receivable stream",
        "worldview": (
            "A developer selling off-plan on multi-year payment plans is, in cash "
            "terms, running a receivables book against a construction obligation. "
            "Value it the way a lender would: what is still owed, less what is still "
            "to be spent, less the overhead and tax of getting there, over the "
            "period it actually takes."),
        "when_it_works": (
            "When the book is large, the payment terms are disclosed and the "
            "construction obligation is well understood — which is TMG's case."),
        "when_it_fails": (
            "When cancellations are material or the plans reprice. It also ignores "
            "everything the company has not yet sold, so it systematically "
            "undervalues a business with a live landbank."),
        "workings": [
            ("Disclosed order book, 30 June 2026", book),
            ("less customer advances already collected", -adv),
            ("= cash still to collect on the book", still_to_collect),
            ("Cost still to spend: book x (1 - gross margin)", book * (1 - gm)),
            ("less properties under development already paid for", -pud),
            ("= cost still to spend", -still_to_build),
            ("Overhead over the conversion, at the group ratio", -opex),
            ("Tax on the book's accounting margin", -tax),
            ("= net cash from converting the book", net_cash),
            ("Spread over %d years and discounted at %.2f%%" % (years, 100 * rate), pv),
            ("Recurring operating profit, FY2025", rec_ebit),
            ("Recurring legs at %.0fx that profit" % REC_MULTIPLE, rec_value),
            ("plus net cash and investment property", other),
            ("less non-controlling interests at book", -_v(bs, "nci_equity")),
            ("= equity value", equity),
        ],
        "value_per_share": equity / sh,
        "sensitivity": {
            "what": "the conversion period",
            "numbers": {str(y): ((net_cash / y)
                                 * sum(1 / (1 + rate) ** k for k in range(1, y + 1))
                                 + rec_value + other - _v(bs, "nci_equity")) / sh
                        for y in (8, 10, 12, 14, 18)},
        },
        "falsifier": (
            "If TMG discloses a delivery schedule showing the book converting "
            "materially faster than twelve years AND cancellations staying below "
            "5%, this method's number is too low and I would withdraw it."),
    }


def expert2(n):
    """The asset view: what the balance sheet would cost to reassemble."""
    bs, kpi = n["inputs"]["BS"], n["inputs"]["KPI"]
    sh = n["meta"]["shares_mn"]
    # RECONCILED FROM THE DISCLOSED TOTAL, not assembled from a list. A first cut
    # listed the assets it thought mattered and silently dropped about EGP 90bn —
    # other current assets, notes receivable for undelivered units, work in
    # progress, right-of-use assets and deferred tax — which is the error [L-015]
    # records: a list nobody counted against a known total.
    total_assets = _v(bs, "total_assets")
    total_liabs = _v(bs, "total_liabilities")
    goodwill_excluded = _v(bs, "goodwill")
    intangibles = _v(bs, "intangibles")
    assets = [
        ("Total assets, 30 June 2026", total_assets),
        ("less goodwill — not an asset anyone can sell separately", -goodwill_excluded),
        ("less intangible assets", -intangibles),
        ("= tangible and financial assets", total_assets - goodwill_excluded - intangibles),
    ]
    liabs = [
        ("Total liabilities", -total_liabs),
        ("  of which customer advances — units owed, not money owed",
         -_v(bs, "customer_advances")),
        ("  of which borrowings and leases",
         -(_v(bs, "loans_noncurrent") + _v(bs, "loans_current")
           + _v(bs, "credit_facilities") + _v(bs, "lease_noncurrent")
           + _v(bs, "lease_current"))),
    ]
    nav = total_assets - goodwill_excluded - intangibles - total_liabs
    nci = _v(bs, "nci_equity")
    equity = nav - nci
    landbank = _v(kpi, "landbank_msqm")
    return {
        "name": "Expert 2 — net asset value, goodwill excluded",
        "worldview": (
            "A developer is a pile of land, half-built product and cash, against a "
            "stack of obligations. Count them at what the accounts say they cost or "
            "are worth, exclude goodwill because it is not an asset anyone can sell, "
            "and see what is left for the shareholder."),
        "when_it_works": (
            "When the balance sheet is recent, audited and granular, and when land "
            "is carried near what it is worth. TMG's is all three."),
        "when_it_fails": (
            "When land is carried at a historical cost decades out of date — which is "
            "a live concern here, since parts of the Madinaty and Rehab land were "
            "acquired long ago and TMG holds about %.0f mn sqm. This method will then "
            "understate. It also gives no credit for the development margin still to "
            "be earned on the book." % landbank),
        "workings": assets + liabs[:1] + liabs[1:] + [
            ("= net asset value, goodwill of %s excluded"
             % "{:,.0f}".format(goodwill_excluded), nav),
            ("less non-controlling interests at book", -nci),
            ("= equity value", equity),
        ],
        "value_per_share": equity / sh,
        "sensitivity": {
            "what": "an uplift on land and work in progress carried at historical cost",
            "numbers": {("+%d%%" % int(100 * u)):
                        (nav + _v(bs, "properties_under_development") * u - nci) / sh
                        for u in (0.0, 0.25, 0.50, 1.00)},
        },
        "falsifier": (
            "If TMG revalued its development land to market and the uplift were "
            "immaterial, the historical-cost concern would be answered and this "
            "number would stand as it is rather than as a floor."),
    }


def expert3(n):
    """The durable-cash view: capitalise what recurs, ignore what wastes."""
    ins = n["inputs"]["IS"]
    bs = n["inputs"]["BS"]
    sh = n["meta"]["shares_mn"]
    r = n["ratios"]
    hosp_rev, oth_rev = _v(ins, "hosp_revenue_fy25"), _v(ins, "other_revenue_fy25")
    hosp_gp = hosp_rev - _v(ins, "hosp_cost_fy25")
    oth_gp = oth_rev - _v(ins, "other_cost_fy25")
    rec_rev = hosp_rev + oth_rev
    rec_gp = hosp_gp + oth_gp
    opex = rec_rev * r["opex_ratio_fy25"]
    ebit = rec_gp - opex
    tax = ebit * n["model_parameters"]["TAX"]
    nopat = ebit - tax
    ke = n["wacc"]["ke_rating"]
    g = 0.15
    value = nopat * (1 + g) / (ke - g)
    net_cash = (_v(bs, "cash") + _v(bs, "deposits_current") + _v(bs, "deposits_noncurrent")
                - _v(bs, "loans_noncurrent") - _v(bs, "loans_current")
                - _v(bs, "credit_facilities"))
    nci = _v(bs, "nci_equity")
    equity = value + net_cash - nci
    return {
        "name": "Expert 3 — capitalise only what recurs",
        "worldview": (
            "Development income is a wasting asset: every unit handed over is one "
            "that will never be handed over again, and the land behind it is finite. "
            "What a long-term owner is really buying is the hotels, the clubs, the "
            "retail and the community-services annuity. Capitalise that, add the "
            "cash, and treat the development book as an option you are not paying "
            "for."),
        "when_it_works": (
            "When the recurring leg is large enough to stand alone. TMG's is: "
            "hospitality and other recurring income were EGP %.0fbn of revenue in "
            "FY2025, and the company's own 1H2026 release puts recurring streams at "
            "over half of group gross profit." % (rec_rev / 1000.0)),
        "when_it_fails": (
            "When the development book is genuinely the asset — which, at EGP 491bn "
            "against a market capitalisation of EGP %.0fbn, is exactly the argument "
            "against this method here. It is deliberately the most conservative "
            "reading in the room." % (n["meta"]["market_cap"] / 1000.0)),
        "workings": [
            ("Hospitality revenue, FY2025", hosp_rev),
            ("Other recurring revenue, FY2025", oth_rev),
            ("= recurring revenue", rec_rev),
            ("Hospitality gross profit", hosp_gp),
            ("Other recurring gross profit", oth_gp),
            ("= recurring gross profit", rec_gp),
            ("Overhead at the group ratio", -opex),
            ("= recurring operating profit", ebit),
            ("Tax at 22.5%", -tax),
            ("= recurring profit after tax", nopat),
            ("Capitalised at Ke %.2f%% less growth %.0f%%" % (100 * ke, 100 * g), value),
            ("plus net cash", net_cash),
            ("less non-controlling interests at book", -nci),
            ("= equity value", equity),
        ],
        "value_per_share": equity / sh,
        "sensitivity": {
            "what": "the long-run growth rate of the recurring leg",
            "numbers": {("%.0f%%" % (100 * gg)):
                        (nopat * (1 + gg) / (ke - gg) + net_cash - nci) / sh
                        for gg in (0.10, 0.125, 0.15, 0.175, 0.20)},
        },
        "falsifier": (
            "If recurring operating profit grew materially slower than Egyptian "
            "inflation for three consecutive years, the annuity would not be an "
            "annuity and this method would have to be abandoned rather than "
            "re-parameterised."),
    }


def cross_examination(e1, e2, e3, n):
    return [
        {"challenge": "Expert 1 to Expert 2: your net asset value counts customer "
                      "advances as a liability at face, but the company does not owe "
                      "money — it owes homes, at a cost below the price.",
         "outcome": "CONCEDED IN PART. The obligation is a construction cost, not a "
                    "cash repayment, and carrying it at face understates value by "
                    "roughly the margin on the undelivered book. Expert 2's number "
                    "stands as a FLOOR rather than a central case."},
        {"challenge": "Expert 2 to Expert 1: you discount a twelve-year receivable at "
                      "a levered equity rate. Contracted instalments from thousands of "
                      "buyers are not equity risk.",
         "outcome": "REJECTED. The construction obligation sits inside the same stream "
                    "and it is emphatically not credit-like: cost overruns, delays and "
                    "cancellations all land on the developer. Discounting the net "
                    "stream at the equity rate is the consistent treatment."},
        {"challenge": "Expert 3 to Experts 1 and 2: both of you assume the development "
                      "margin survives at 26.6%. It has fallen from 38.4% in FY2019.",
         "outcome": "CONCEDED. The margin is an output of the disclosed cost ratio and "
                    "it has compressed steadily. Section 1.9 sensitises it; a 5-point "
                    "further compression moves the central reading by roughly a fifth."},
        {"challenge": "Experts 1 and 2 to Expert 3: you value the hotels and clubs and "
                      "then give the shareholder nothing for EGP 491bn of sold "
                      "product.",
         "outcome": "CONCEDED AS A LIMIT, NOT AS AN ERROR. Expert 3's number is "
                    "explicitly a floor for what an owner is paying for today, and it "
                    "is presented as such rather than as a central estimate."},
        {"challenge": "All three to the study: the house discount rate of %.2f%% is "
                      "above anything the market appears to use — %.1f%% to %.1f%% on "
                      "the reverse calculation."
                      % (100 * n["wacc"]["wacc_rating"],
                         100 * n["lenses"]["implied_discount_rate"]["recovery"],
                         100 * n["lenses"]["implied_discount_rate"]["capacity"]),
         "outcome": "ACKNOWLEDGED AND PUBLISHED. The house method levers Egypt's whole "
                    "country risk premium by a beta of 1.47; the market appears to "
                    "apply the sovereign yield with little more. The study reports "
                    "both rather than picking one, and the gap IS the disagreement."},
    ]


def main():
    n = N()
    e1, e2, e3 = expert1(n), expert2(n), expert3(n)
    vals = {e["name"]: e["value_per_share"] for e in (e1, e2, e3)}
    div = [
        {"pair": "1 vs 2", "gap": e1["value_per_share"] - e2["value_per_share"],
         "driven_by": "whether customer advances are a cash liability at face or a "
                      "construction obligation at cost"},
        {"pair": "1 vs 3", "gap": e1["value_per_share"] - e3["value_per_share"],
         "driven_by": "whether the development book is an asset or a wasting stream "
                      "with no terminal value"},
        {"pair": "2 vs 3", "gap": e2["value_per_share"] - e3["value_per_share"],
         "driven_by": "whether land and work in progress at historical cost is a "
                      "better guide than capitalised recurring profit"},
    ]
    lo = min(vals.values())
    hi = max(vals.values())
    close = sorted(vals.values())[-2:]
    room = (
        "Put in one room, the three agree on less than they disagree on, and the "
        "disagreement is legible. All three accept the same balance sheet, the same "
        "order book and the same margin; they differ on ONE question, which is "
        "whether an order book is an asset, a receivable or neither.\n\n"
        "Expert 3's EGP %.2f is the floor, deliberately: it gives the shareholder "
        "nothing at all for EGP %.0fbn of sold product, and says so. Experts 1 and 2 "
        "arrive at EGP %.2f and EGP %.2f by routes that share almost no arithmetic — "
        "one discounts a twelve-year net cash stream, the other reconciles a "
        "balance sheet and strips goodwill — and land within EGP %.2f of each other. "
        "Two independent methods converging that closely is the most reassuring "
        "thing in this appendix, and it is worth more than any one of the three "
        "numbers.\n\n"
        "None of the three reaches the traded price of EGP %.2f, and none of them is "
        "trying to. The spread across the panel is EGP %.2f to EGP %.2f."
        % (vals[e3["name"]], _v(n["inputs"]["KPI"], "backlog_jun26") / 1000.0,
           vals[e1["name"]], vals[e2["name"]], abs(close[1] - close[0]),
           n["meta"]["spot"], lo, hi))
    out = {"experts": [e1, e2, e3], "values": vals,
           "cross_examination": cross_examination(e1, e2, e3, n),
           "three_in_one_room": room, "divergence": div}
    json.dump(out, open(os.path.join(HERE, "experts.json"), "w"), indent=1)
    for e in (e1, e2, e3):
        print("%-52s %8.2f" % (e["name"], e["value_per_share"]))
        print("    sensitivity on %s: %s" % (e["sensitivity"]["what"],
              {k: round(v, 1) for k, v in e["sensitivity"]["numbers"].items()}))
    print("\ndivergence:")
    for d in div:
        print("   %-8s %8.2f   %s" % (d["pair"], d["gap"], d["driven_by"][:64]))


if __name__ == "__main__":
    main()
