"""GB Auto's asset-conversion cycle, built from GB Corp's own disclosed segment tables.

SIGCM clause 4 — "study DSO/DIO/DPO and the cash-conversion cycle from the statements and
PROJECT the balance-sheet and cash-flow items from them".  The delivered edition projected
working capital from one typed intensity ratio on revenue and separated no component; the
07-09-2026 QC gate recorded that as row 21 FAIL.  This builds the cycle.

WHY THE SEGMENT TABLE AND NOT THE CONSOLIDATED BALANCE SHEET, which is the whole reason
this is not a five-line script: GB Corp CONTAINS A LENDER.  The consolidated
"Accounts and notes receivables" line is EGP 13,465.1mn at 31-Dec-2025 against GB Auto's
own disclosed trade receivables of EGP 5,316.9mn, the difference being GB Capital's loan
book -- a financing asset, not a trade receivable.  Dividing a lender's book by an
assembler's revenue manufactures a days figure several times too long, which is
[R-FCAL-01]'s interest-rate trap ("the borrowings that ACTUALLY BEAR IT") arriving in
working-capital costume: a large, robust and entirely spurious number.  The cash-flow lens
values the AUTO leg, so the cycle is built on the AUTO segment, whose components GB Corp
discloses quarterly and whose total is the WC_OPENING the model already carries.

ARITHMETIC IS THE ARBITER.  Every disclosed table is footed to its own stated total before
a single day is computed, and the extraction route is recorded per source.
"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))

# GB AUTO segment working capital, EGP mn, as the company itself publishes it.
# ROUTE: text layer (pdftotext -layout) of GB Corp's own quarterly earnings releases,
# committed under src/.  Each quarter appears in two releases a year apart; where the two
# disagree the later basis is taken and the break is registered below.
DISCLOSED = {
    "4Q22": dict(inventory=3920.0, receivables=1432.2, advances=742.5,
                 debtors_other=1927.1, payables=4715.9, working_capital=3305.9,
                 source="GB_Corp_ER_4Q23_-_ER_-_FINAL.pdf, Table 6", basis="payables NET of finance-lease liabilities"),
    "4Q23": dict(inventory=6366.1, receivables=1743.5, advances=913.6,
                 debtors_other=1547.9, payables=6104.7, working_capital=4466.3,
                 source="GB_Corp_ER_4Q24-_E_-_Final.pdf, Table 6", basis="payables GROSS"),
    "4Q24": dict(inventory=21134.3, receivables=3708.7, advances=1583.0,
                 debtors_other=3258.5, payables=18900.5, working_capital=10783.9,
                 source="GB_Corp_ER_4Q25-_E_-_Final.pdf, Table 6", basis="payables GROSS"),
    "4Q25": dict(inventory=24649.7, receivables=5316.9, advances=1299.6,
                 debtors_other=3371.0, payables=15720.2, working_capital=18917.0,
                 source="GB_Corp_ER_2Q26-_E_-_Final.pdf, Table 6", basis="payables GROSS"),
    "2Q26": dict(inventory=22959.1, receivables=5873.5, advances=1153.7,
                 debtors_other=2598.9, payables=15492.5, working_capital=17092.8,
                 source="GB_Corp_ER_2Q26-_E_-_Final.pdf, Table 6", basis="payables GROSS"),
}
# GB AUTO segment flows, EGP mn, from the consolidation table of the same releases.
FLOWS = {
    "FY2023": dict(revenue=23429.5, cost_of_sales=17616.4, days=365, opening="4Q22", closing="4Q23"),
    "FY2024": dict(revenue=46692.0, cost_of_sales=37634.6, days=366, opening="4Q23", closing="4Q24"),
    "FY2025": dict(revenue=65913.5, cost_of_sales=56076.4, days=365, opening="4Q24", closing="4Q25"),
    "1H2026": dict(revenue=39627.0, cost_of_sales=33904.9, days=181, opening="4Q25", closing="2Q26"),
}
# A BASIS BREAK IS REGISTERED BEFORE MODELLING, NEVER RECONCILED AWAY [R-FCAL-01].
BASIS_BREAKS = [dict(
    period="4Q22 and 4Q23", what="payables shown NET of finance-lease liabilities",
    measured="the 4Q23 release reports 4Q23 payables of 5,828.9 and the 4Q24 release reports "
             "6,104.7 for the same date; the difference of 275.8 reconciles to the pound "
             "against the 275.9 of lease liabilities the 4Q23 release names in its own footnote",
    consequence="FY2023's payable days are computed on CLOSING balances only. Averaging a "
                "net-basis opening with a gross-basis closing would be a days figure of no "
                "definition at all, and is not done.")]
# The consolidated statements restate too, and it is registered rather than smoothed.
RESTATEMENTS = [
    dict(line="Accounts and notes receivables, 31-Dec-2024",
         as_reported=7581.323, restated=8334.218,
         where="FY2024 audited statements as reported; FY2025 audited statements label the "
               "2024 column 'Restated'"),
    dict(line="Accounts and notes receivables, 31-Dec-2025",
         as_reported=13465.131, restated=14157.949,
         where="FY2025 audited statements as reported; the 30-June-2026 reviewed interim "
               "carries the higher figure as its comparative"),
]

def foot():
    """Every disclosed total must reproduce from its own printed components."""
    out = {}
    for q, d in DISCLOSED.items():
        calc = d["inventory"] + d["receivables"] + d["advances"] + d["debtors_other"] - d["payables"]
        gap = calc - d["working_capital"]
        assert abs(gap) <= 0.15, f"{q}: components sum to {calc}, table states {d['working_capital']}"
        out[q] = dict(computed=round(calc, 1), stated=d["working_capital"], gap=round(gap, 2))
    return out

def cycle():
    rows = {}
    for per, f in FLOWS.items():
        o, c = DISCLOSED[f["opening"]], DISCLOSED[f["closing"]]
        avg_basis = "closing" if per == "FY2023" else "average"
        pick = (lambda k: c[k]) if avg_basis == "closing" else (lambda k: (o[k] + c[k]) / 2)
        dso = pick("receivables") / f["revenue"] * f["days"]
        dio = pick("inventory") / f["cost_of_sales"] * f["days"]
        dpo = pick("payables") / f["cost_of_sales"] * f["days"]
        adv = pick("advances") / f["revenue"] * f["days"]
        dob = pick("debtors_other") / f["revenue"] * f["days"]
        annualised = f["revenue"] * 365 / f["days"]
        rows[per] = dict(dso=round(dso, 2), dio=round(dio, 2), dpo=round(dpo, 2),
                         ccc=round(dso + dio - dpo, 2), advance_days=round(adv, 2),
                         debtor_days=round(dob, 2), balance_basis=avg_basis,
                         wc_closing=c["working_capital"],
                         wc_over_annualised_revenue=round(c["working_capital"] / annualised, 4))
    return rows

def trailing_twelve_months():
    """The anchor [R-ANCHOR-01] asks for: the latest reviewed period on a full-year base."""
    rev = FLOWS["FY2025"]["revenue"] - 30493.8 + FLOWS["1H2026"]["revenue"]   # less 1H25, plus 1H26
    cos = FLOWS["FY2025"]["cost_of_sales"] - 25741.9 + FLOWS["1H2026"]["cost_of_sales"]
    wc = DISCLOSED["2Q26"]["working_capital"]
    return dict(revenue=round(rev, 1), cost_of_sales=round(cos, 1), working_capital=wc,
                wc_over_revenue=round(wc / rev, 4),
                source="1H2025 auto revenue 30,493.8 and cost of sales 25,741.9 from the "
                       "2Q26 release's own prior-year column")

RECORD = dict(
    ticker="GBCO", segment="GB Auto", unit="EGP mn", as_of="2026-09-17",
    # [R-ENF-06]: an artefact a builder reads declares the answer it was built against.
    # THIS STUDY PUBLISHES NO SINGLE CENTRAL. The field names the branch this record is
    # anchored on -- the reviewed carrying value, the LOWER of the two -- exactly as
    # contested_judgements.json does, and both branches are declared beside it.
    published_central=41.348367298232716,
    published_central_is="MNT-Halan at its reviewed carrying value",
    published_central_two_sided=[41.348367298232716, 52.345259974418816],
    published_spot=28.98,
    rule="SIGCM clause 4; QC gate 07-09-2026 row 21",
    disclosed=DISCLOSED, flows=FLOWS, footing=foot(), cycle=cycle(),
    ttm_to_30_june_2026=trailing_twelve_months(),
    basis_breaks=BASIS_BREAKS, restatements=RESTATEMENTS,
    receivables_contamination=dict(
        group_current_receivables_31dec2025=13465.131,
        auto_segment_trade_receivables_31dec2025=5316.9,
        note="the difference is GB Capital's loan book and a group-level days figure is "
             "meaningless; the cycle is built on the auto segment alone"),
)

if __name__ == "__main__":
    with open(os.path.join(HERE, "asset_cycle.json"), "w", encoding="utf-8") as fh:
        json.dump(RECORD, fh, indent=1, ensure_ascii=False)
    c = RECORD["cycle"]
    print(f"{'period':<9}{'DSO':>7}{'DIO':>8}{'DPO':>8}{'CCC':>8}{'WC/rev':>9}  basis")
    for p, r in c.items():
        print(f"{p:<9}{r['dso']:>7.1f}{r['dio']:>8.1f}{r['dpo']:>8.1f}{r['ccc']:>8.1f}"
              f"{r['wc_over_annualised_revenue']*100:>8.1f}%  {r['balance_basis']}")
    t = RECORD["ttm_to_30_june_2026"]
    print(f"\nTTM to 30-Jun-2026: working capital {t['working_capital']:,.1f} / revenue "
          f"{t['revenue']:,.1f} = {t['wc_over_revenue']*100:.2f}%")
    print("every disclosed table foots to its own stated total:",
          all(abs(v['gap']) <= 0.15 for v in RECORD['footing'].values()))
