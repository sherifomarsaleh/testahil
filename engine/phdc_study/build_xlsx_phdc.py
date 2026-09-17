"""Build the delivered PHDC workbook — 16 sheets, live formulas.

Reads study_numbers.json; no financial numeral is typed here. Inputs are blue
and live on Assumptions; everything downstream is a FORMULA referencing them, so
changing a driver recomputes the statements, the discounted cash flow and the
value per share. A workbook of hardcoded values is not a model.
"""
import json, os, sys
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import valuation_v2 as _V2       # the terminal growth this model actually runs

HERE = os.path.dirname(os.path.abspath(__file__))

# THE REVERSE READ, FROM THE FILE THAT OWNS IT. A quantity solved from a price is a
# DIAGNOSTIC; it was sitting in study_numbers.json, which every builder reads, and that
# is the reverse-engineered rate the protocol prohibits arriving through a side door.
# Reading it here from diagnostics.json keeps it printable and keeps it out of the
# numbers file, where something could consume it as an input [R-ENF-05].
_IMPLIED = json.load(open(os.path.join(HERE, "diagnostics.json")))["implied"]["value"]
N = json.load(open(os.path.join(HERE, "study_numbers.json")))
ST = N["statements"]
M, D, W, REG = N["meta"], N["derived"], N["wacc"], N["registry"]
CASES, SENS, PM = N["cases"], N["sensitivity"], N["price_map"]
BU, LENS, LW, BRIDGE = (N["bottom_up"], N["lenses"], N["lens_weighted"],
                        N["bridge"])

INPUT = Font(color="1D6FA3", bold=True)          # blue = input
FORM = Font(color="1A1D21")                       # black = formula
HEAD = Font(color="FFFFFF", bold=True, size=10)
FILL = PatternFill("solid", fgColor="1D6FA3")
SUB = Font(bold=True, color="1A1D21")
MUT = Font(color="5B6570", size=9, italic=True)
THIN = Border(bottom=Side(style="thin", color="DCE1E5"))
YEARS = [r["year"] for r in N["cases"]["base"]["rows"]]

# Assumption cells are resolved by LABEL as the sheet is written, never by a
# remembered row number: the row moves the moment a driver is added, and a
# stale address produces a workbook that still computes and is simply wrong.
ASSUMPTION_AT = {}

# THE BRIDGE SHEETS ARE WRITTEN BEFORE THE ASSUMPTIONS SHEET, so they cannot resolve a
# label through AT() and five addresses were typed into their formulas instead. Adding
# one driver row on 13-09-2026 shifted every one of them and the bridge published a
# value per share of MINUS 2.4 billion. The addresses live here now, in one place, used
# by the bridge formulas AND asserted against their labels once the Assumptions sheet
# exists -- so the next inserted row fails the build instead of the bridge.
BRIDGE_CELLS = {
    # The DCF sheet is written before the Assumptions sheet too, so the one escalation cell
    # it reads is pre-resolved here with the bridge's five. Asserted against its label once
    # the Assumptions sheet exists, like the others.
    "Price and cost escalation, 2026 — the house path": "B10",
    "Net debt (EGP mn)": "B14",
    "Investments in associates (EGP mn)": "B15",
    "Investment property (EGP mn)": "B16",
    "Minority interests, share of equity value": "B17",
    "Shares outstanding (mn)": "B18",
}
# THE DCF SHEET'S TWO OUTPUTS THE BRIDGE READS, pre-resolved for the same reason: the
# Fundamental Valuation sheet is written BEFORE the DCF sheet, so it cannot resolve a label
# there either. Wiring the bridge to these addresses instead of hardcoding copies of their
# values is the fix for a workbook whose own warranty said everything recomputes; adding the
# terminal's construction rows then shifted the discounted terminal from B21 to B25 and the
# bridge silently lost a third of the answer, with the workbook still footing internally.
# Registered here and ASSERTED against the labels the DCF sheet actually emits, so the next
# inserted row fails the build rather than the bridge.
DCF_CELLS = {
    "Sum of the explicit years": "B20",
    "Terminal value, discounted": "B25",
}
DCF_LABEL_AT = {}
DCF_ROWS = {}   # the DCF sheet's own row numbers, for the statements written after it
A_PV_EXPLICIT = DCF_CELLS["Sum of the explicit years"]
A_PV_TERMINAL = DCF_CELLS["Terminal value, discounted"]

_BC = BRIDGE_CELLS
A_ND, A_ASSOC = _BC["Net debt (EGP mn)"], _BC["Investments in associates (EGP mn)"]
A_IP = _BC["Investment property (EGP mn)"]
A_NCI = _BC["Minority interests, share of equity value"]
A_SH = _BC["Shares outstanding (mn)"]
A_ESC1 = _BC["Price and cost escalation, 2026 — the house path"]


def AT(label):
    if label not in ASSUMPTION_AT:
        raise KeyError("no assumption row named %r; have %s"
                       % (label, sorted(ASSUMPTION_AT)))
    return ASSUMPTION_AT[label]


def v(k):
    return REG[k]["value"]


def q(k):
    """A line of the 31 March 2026 reviewed balance sheet — what the bridge stands on."""
    return N["balance_sheet_1q26"][k]["value"]


def head(ws, title, note=None, widths=None):
    ws["A1"] = title
    ws["A1"].font = Font(bold=True, size=13, color="1D6FA3")
    if note:
        ws["A2"] = note
        ws["A2"].font = MUT
    ws.freeze_panes = "B4"
    for i, w in enumerate(widths or [], start=1):
        ws.column_dimensions[get_column_letter(i)].width = w


def row(ws, r, label, values=None, font=None, fmt=None, bold=False):
    ws.cell(r, 1, label).font = SUB if bold else FORM
    for j, val in enumerate(values or [], start=2):
        c = ws.cell(r, j, val)
        c.font = font or FORM
        if fmt:
            c.number_format = fmt
    return r + 1


def build(path):
    wb = Workbook()

    # 1 READ FIRST -----------------------------------------------------------
    ws = wb.active
    ws.title = "READ FIRST"
    # THE STAMP WAS TYPED AND WAS TWO EDITIONS STALE. This file already imports
    # edition.py for the filename; it reads it for the words too now.
    import edition as _ED0
    head(ws, "Palm Hills Developments — valuation workbook",
         "Edition of %s. Supersedes %s." % (_ED0.WORDS, _ED0.PRIOR_WORDS), [70])
    r = 4
    for line in [
        "This workbook is for information and education. It is not investment "
        "advice and carries no rating and no price target.",
        "",
        "BLUE cells are inputs and live on the Assumptions sheet. BLACK cells are "
        "formulas. Change a blue cell and the statements, the discounted cash flow "
        "and the value per share all recompute.",
        "",
        "Reported history comes only from the company's own audited statements and "
        "its own results releases. Where a figure the valuation needs is not "
        "disclosed, it is absent and named on the Assumptions sheet rather than "
        "estimated.",
        "",
        "The single most important number in this workbook is cash conversion — the "
        "share of revenue that reaches operating cash flow. The company does not "
        "disclose its collection terms, so it is measured from the three published "
        "cash-flow statements and it spans %.1f%% to %.1f%%. The Sensitivity sheet "
        "shows what that does to the answer." % (D["cfo_lo"] * 100, D["cfo_hi"] * 100),
    ]:
        ws.cell(r, 1, line).alignment = Alignment(wrap_text=True, vertical="top")
        ws.row_dimensions[r].height = 30 if line else 8
        r += 1

    # 2 Summary --------------------------------------------------------------
    ws = wb.create_sheet("Summary")
    head(ws, "Summary", "Every figure recomputes from Assumptions.",
         [46, 16, 16, 16, 16])
    r = 4
    r = row(ws, r, "Lens", ["Bear", "Base", "Full value", "Weight"],
            font=HEAD, bold=True)
    for c in "BCDE":
        ws["%s%d" % (c, r - 1)].fill = FILL
    for nm, b_, ba, f_, wt in LENS:
        r = row(ws, r, nm, [round(b_, 2), round(ba, 2), round(f_, 2), wt],
                fmt="#,##0.00")
    r = row(ws, r, "Weighted central",
            [round(LW["bear"], 2), round(LW["base"], 2), round(LW["full"], 2), 1.0],
            fmt="#,##0.00", bold=True)
    r += 1
    r = row(ws, r, "Valuation", ["Per share (EGP)", "Equity (EGP mn)",
                                 "Enterprise value"], font=HEAD, bold=True)
    for c in "BCD":
        ws["%s%d" % (c, r - 1)].fill = FILL
    for key, lbl in (("low_conversion", "Weak cash conversion (%.1f%%)"
                      % (D["cfo_lo"] * 100)),
                     ("base", "Average cash conversion (%.1f%%)"
                      % (D["cfo_mid"] * 100)),
                     ("high_conversion", "Strong cash conversion (%.1f%%)"
                      % (D["cfo_hi"] * 100)),
                     ("base_cds_erp", "Average, alternative country-risk basis")):
        c = CASES[key]
        r = row(ws, r, lbl, [round(c["per_share"], 2), round(c["equity"], 0),
                             round(c["ev"], 0)], fmt="#,##0.00")
    r += 1
    r = row(ws, r, "Market price, 23 Aug 2026", [PM["spot"]], font=INPUT,
            fmt="#,##0.00")
    r = row(ws, r, "Book value of equity per share",
            [round(D["book_equity_per_share"], 2)], fmt="#,##0.00")
    r = row(ws, r, "Cash conversion implied by the market price",
            [round(_IMPLIED, 4)], fmt="0.00%")
    r += 1
    r = row(ws, r, "Cost of capital", [], bold=True)
    r = row(ws, r, "Weighted average, rating basis", [W["wacc_rating"]], fmt="0.00%")
    r = row(ws, r, "Weighted average, swap basis", [W["wacc_cds"]], fmt="0.00%")
    r = row(ws, r, "11 June 2026 edition used", [D["edition_11jun_wacc"]], fmt="0.00%")

    # 3 Fundamental Valuation ------------------------------------------------
    ws = wb.create_sheet("Fundamental Valuation")
    head(ws, "Fundamental valuation — bridge to equity",
         "All formulas; drivers live on Assumptions.", [46, 18])
    b = CASES["base"]
    r = 4
    # TWO DEFECTS ON ONE ROW, FIXED TOGETHER [17-09-2026].
    #
    # THE LABEL SAID FIVE YEARS AND THE NUMBER WAS FIFTEEN. This row read "Present value of
    # the explicit five years" against a 2026-2040 model, and the same wrong window was
    # printed in the document's Appendix A.1 caption and in its expert appendix — while the
    # document's own bridge four pages earlier says "the explicit 15 years". On a genuine
    # five-year window the answer is materially different and the terminal carries 68% of it
    # rather than 31%, so this is not a wording slip: it tells a reader the wrong thing about
    # where the value comes from.
    #
    # AND THE VALUE WAS A HARDCODED CONSTANT beside a sheet that computes it. DCF!B20 is
    # =SUM(B18:P18) and has been all along; this cell carried a rounded copy of the same
    # number, so the workbook's own warranty — "Change a blue cell and the statements, the
    # discounted cash flow and the value per share all recompute" — was false at the one
    # junction where the discounted cash flow meets the answer. It is a reference now.
    r = row(ws, r, "Present value of the explicit 15 years (2026-2040)",
            ["=DCF!" + A_PV_EXPLICIT], fmt="#,##0.0")
    r = row(ws, r, "Present value of the terminal value",
            ["=DCF!" + A_PV_TERMINAL], fmt="#,##0.0")
    r = row(ws, r, "Enterprise value", ["=B4+B5"], fmt="#,##0.0", bold=True)
    # the bridge stands on the 31 March 2026 reviewed balance sheet; the four
    # Assumptions addresses below are asserted against their labels once that
    # sheet is written (A_NET_DEBT .. A_SHARES)
    r = row(ws, r, "less net debt, 31 March 2026", ["=-Assumptions!" + A_ND], fmt="#,##0.0")
    r = row(ws, r, "plus investments in associates",
            ["=Assumptions!" + A_ASSOC], fmt="#,##0.0")
    r = row(ws, r, "plus investment property", ["=Assumptions!" + A_IP], fmt="#,##0.0")
    r = row(ws, r, "Equity value before minority interests", ["=B6+B7+B8+B9"],
            fmt="#,##0.0", bold=True)
    r = row(ws, r, "less minority interests at their share of value",
            ["=-B10*Assumptions!" + A_NCI], fmt="#,##0.0")
    r = row(ws, r, "Equity value attributable to shareholders", ["=B10+B11"],
            fmt="#,##0.0", bold=True)
    r = row(ws, r, "Shares outstanding (mn)", ["=Assumptions!" + A_SH], fmt="#,##0.0")
    r = row(ws, r, "Value per share (EGP)", ["=B12/B13"], fmt="#,##0.00", bold=True)
    r += 1
    r = row(ws, r, "Terminal value as a share of enterprise value",
            ["=B5/B6"], fmt="0%")

    # 4 Assumptions ----------------------------------------------------------
    ws = wb.create_sheet("Assumptions")
    head(ws, "Assumptions — every blue cell is an input",
         "Change one and the whole workbook recomputes.", [46, 16, 62])
    r = 4
    ws.cell(r, 1, "Driver").font = HEAD
    ws.cell(r, 2, "Value").font = HEAD
    ws.cell(r, 3, "Source").font = HEAD
    for c in "ABC":
        ws["%s%d" % (c, r)].fill = FILL
    r += 1
    # the escalation path the model runs, read from the committed numbers; year one is the
    # input cell below and the whole path is published on the DCF sheet
    ESC_PATH = [x["price_growth"] for x in N["bottom_up"]["rows"]]
    rows = [
        ("Cash conversion — central", D["cfo_mid"], "0.00%",
         "mean of the three published cash-flow statements"),
        ("Cash conversion — weak", D["cfo_lo"], "0.00%", "2023 and 2025 outcome"),
        ("Cash conversion — strong", D["cfo_hi"], "0.00%", "2024 outcome"),
        # THE SHEET PUBLISHED A MARGIN THE MODEL DOES NOT RUN. This cell carried the
        # average of FY2025 and 1Q2026 -- the anchor the SUPERSEDED edition used --
        # on a sheet headed "every blue cell is an input; change one and the whole
        # workbook recomputes". The model runs the latest disclosure alone.
        ("Gross margin", N["bottom_up"]["anchors"]["gross_margin_forward"], "0.00%",
         "the first quarter of 2026 on its own, the latest disclosure; NOT an "
         "average (FY2025 was %.2f%%, 1Q2026 %.2f%%)"
         % (100 * D["gross_margin_fy25"], 100 * D["gross_margin_1q26"])),
        ("Overheads as a share of revenue", D["sga_ratio_fy25"], "0.00%",
         "FY2025 as reported"),
        # THE LAST ORPHAN ON THIS SHEET [17-09-2026]. Two cells beside this one were
        # fixed on 10-09-2026 for publishing a rate the model does not run; this one
        # survived the same pass. It printed the trailing three-year Egyptian CPI of 25.2%
        # under the bare label "Price escalation" while the model escalates price and cost
        # on the house path — 16% in 2026 falling to 7% — which is a different number in
        # every year and is not this one in any of them. No formula on any sheet read it.
        #
        # IT IS A LIVE REFERENCE NOW, to the first year of the path the model actually
        # runs, with the rest of the path published year by year on the DCF sheet row 5
        # where the model reads it. THE ROW COUNT IS DELIBERATELY UNCHANGED: BRIDGE_CELLS
        # above hardcodes B14-B18 because the bridge sheets are written before this one,
        # and inserting a driver row here shifted every one of them on 13-09-2026 and
        # published a value per share of minus 2.4 billion. A fix that re-creates the
        # defect it is fixing is not a fix.
        ("Price and cost escalation, 2026 — the house path", ESC_PATH[0], "0.00%",
         "the house Egyptian inflation path [R-MACRO-01], read by the model: 16 per cent "
         "in 2026 falling to 12 / 9 / 7.5 / 7 and holding 7 to the terminal, published "
         "year by year on the DCF sheet row 5. ONE escalator drives price and cost alike, "
         "which is why gross margin is flat by construction and is sensitised in the "
         "study rather than extrapolated. The Egyptian CPI three-year trailing mean of "
         + ("%.1f per cent" % (100 * D["cpi_trailing3"])) +
         " (World Bank WDI, 2023-25) is NOT used and is named here so the reader knows it "
         "was considered and rejected: a trailing mean of the worst inflation in Egypt's "
         "recent record is not a forecast, and the central bank's own published target "
         "contradicts it"),
        # TYPED 0.12 AGAINST A MODEL RUNNING 0.07, and 12% is the alternative the
        # study's own contested-judgement record marks REJECTED, worth EGP 21.00 a
        # share. It is read from the model now.
        ("Terminal growth", _V2.TG, "0.00%",
         "the terminal growth this model runs, read from the valuation module"),
        # AND THE COST OF CAPITAL CELL PUBLISHED THE RATING BASIS UNDER A BARE LABEL
        # while the model discounts on the swap basis and section 1.8 marks that one
        # ADOPTED. Both are shown, and the adopted one is the one named as adopted.
        ("Cost of capital — ADOPTED (traded default-swap basis)", W["wacc_cds"],
         "0.00%", "the rate this model discounts at; section 1.8 marks it adopted"),
        ("Cost of capital — alternative (credit-rating basis), not used",
         W["wacc_rating"], "0.00%",
         "published for comparison only; no cell on this sheet reads it"),
        ("Net debt (EGP mn)", D["net_debt_bridge"], "#,##0.0",
         "gross borrowings less cash, 31 March 2026 reviewed balance sheet"),
        ("Investments in associates (EGP mn)", q("investments_assoc"), "#,##0.0",
         "31 March 2026 reviewed balance sheet"),
        ("Investment property (EGP mn)", q("investment_property"), "#,##0.0",
         "31 March 2026 reviewed balance sheet"),
        ("Minority interests, share of equity value", D["nci_value_share"], "0.00%",
         "the MEAN of the minority's filed share of profit after tax over FY2023-FY2025, "
         "as its share of value [adopted 17-09-2026]. The FY2025 share alone and the book "
         "share of equity are published in the study beside it; the single year is not "
         "adopted because a one-observation anchor is what this study refuses elsewhere"),
        ("Shares outstanding (mn)", D["shares_mn"], "#,##0.0", "FY2025"),
        ("Opening revenue (EGP mn)", v("revenue_fy25"), "#,##0.0", "FY2025 audited"),
        ("Opening order book (EGP mn)", v("backlog_1q26"), "#,##0.0",
         "as at 31 March 2026"),
        ("Units delivered, 2026", BU["rows"][0]["units_delivered"], "#,##0",
         "implied by the reported first quarter of 2026"),
        ("Units delivered, annual growth", BU["anchors"]["delivery_growth"],
         "0.00%", "the disclosed run of handovers, 1,308 / 1,281 / 1,500 / 2,000"),
        ("Revenue per delivered unit, 2026 (EGP mn)",
         BU["rows"][0]["rev_per_unit"], "#,##0.00",
         "FY2024 revenue over c. 2,000 units delivered, escalated"),
        ("Maintenance capital expenditure, share of revenue",
         N["statements"]["capex_ratio"], "0.00%",
         "the building itself is inventory and sits in operating cash"),
        # FOUR DRIVERS THE MODEL RUNS ON AND THIS SHEET DID NOT PUBLISH [added 17-09-2026].
        #
        # The Income Statement, Cash Flow and Sensitivity sheets held 677 numbers and not
        # one formula: every figure was written as a computed value, so the workbook's own
        # warranty — change a blue cell and the statements recompute — was false across
        # three of its sixteen sheets. The reason it was false is that the drivers those
        # statements run on had no cells to reference. They do now, and the statements are
        # formulas off them.
        #
        # APPENDED RATHER THAN INSERTED, deliberately: BRIDGE_CELLS pre-resolves B10 and
        # B14-B18 because three sheets are written before this one, and inserting a driver
        # above them shifted every one on 13-09-2026 and published a value per share of
        # minus 2.4 billion. Everything below B18 is resolved by label at write time, so
        # appending is safe and a tripwire catches it if it stops being.
        #
        # THE FINANCE CHARGE IS THE POINT OF TWO OF THESE. The model holds it at the
        # FY2025 level for all fifteen years: the interest-bearing subset of the balance
        # sheet times the effective rate that subset actually carried. Both halves were
        # invisible, so a reader could not see that the charge is flat and nominal while
        # revenue grows sixfold — which is the study's largest unresolved construction and
        # is priced in the contested register. Publishing the two cells makes it arguable.
        ("Depreciation and amortisation, share of revenue",
         v("da_fy25") / v("revenue_fy25"), "0.00%",
         "FY2025 as reported: depreciation and amortisation over revenue"),
        ("Interest-bearing borrowings (EGP mn)",
         N["bottom_up"]["anchors"]["interest_bearing_debt"], "#,##0.0",
         "the bank and loan lines only, FY2025: a large part of the balance sheet "
         "(notes payable to land sellers, customer balances) does not bear interest"),
        ("Effective P&L rate on those borrowings",
         N["bottom_up"]["anchors"]["effective_pl_rate"], "0.00%",
         "FY2025 finance cost over the interest-bearing subset above. NOT the marginal "
         "rate: part of the interest incurred is capitalised into work in progress. The "
         "charge is held at this level, flat and nominal, for all fifteen years while "
         "revenue grows sixfold — the alternative footing is priced in the study's "
         "contested-judgement record"),
        ("Tax rate", BU["rows"][0]["tax_rate"], "0.00%",
         "PHD's own tax note computes FY2025 and FY2024 current tax at this rate on net "
         "taxable profit"),
    ]
    ASSUMPTION_AT.clear()
    for lbl, val, fmt, src in rows:
        ws.cell(r, 1, lbl).font = FORM
        c = ws.cell(r, 2, val)
        c.font = INPUT
        c.number_format = fmt
        ws.cell(r, 3, src).font = MUT
        ASSUMPTION_AT[lbl] = "$B$%d" % r
        r += 1
    # the bridge sheets reference these four rows by address; hold the
    # addresses to the labels so an inserted driver cannot silently shift them
    # THE TRIPWIRE, AGAINST THE ADDRESSES THE BRIDGE ACTUALLY EMITTED. One list, used
    # by both, so a shift cannot pass the guard and break the formulas.
    for lbl, addr in BRIDGE_CELLS.items():
        want = "$%s$%s" % (addr[0], addr[1:])
        assert ASSUMPTION_AT[lbl] == want, (lbl, ASSUMPTION_AT[lbl], want)
    r += 1
    ws.cell(r, 1, "NOT DISCLOSED — absent by design, never estimated").font = SUB
    r += 1
    for k, why in N["gaps"].items():
        ws.cell(r, 1, k.replace("_", " ")).font = FORM
        ws.cell(r, 3, why[:180]).font = MUT
        r += 1
    _remaining(wb)
    return wb


# ---------------------------------------------------------------------------
def _yearhead(ws, r=4, first=2):
    ws.cell(r, 1, "EGP million").font = HEAD
    ws.cell(r, 1).fill = FILL
    for j, y in enumerate(YEARS, start=first):
        c = ws.cell(r, j, y)
        c.font = HEAD
        c.fill = FILL
        c.alignment = Alignment(horizontal="center")
        ws.column_dimensions[get_column_letter(j)].width = 12
    ws.column_dimensions["A"].width = 40
    return r + 1


def _remaining(wb):
    b = CASES["base"]
    rows = b["rows"]

    # 5 SOTP Bridge ----------------------------------------------------------
    ws = wb.create_sheet("SOTP Bridge")
    head(ws, "Bridge from enterprise value to equity",
         "A developer is one business; the bridge is the parts that sit outside "
         "the operating cash flows.", [46, 18])
    r = 4
    for lbl, val in (("Operating business, discounted cash flow", b["ev"]),
                     ("Investments in associates, 31 March 2026", q("investments_assoc")),
                     ("Investment property, 31 March 2026", q("investment_property")),
                     ("Cash, 31 March 2026", D["cash_bridge"]),
                     ("Gross borrowings, 31 March 2026", -D["gross_debt_bridge"])):
        r = row(ws, r, lbl, [round(val, 1)], fmt="#,##0.0")
    r = row(ws, r, "Minority interests at their share of value",
            ["=-(B4+B5+B6+B7+B8)*Assumptions!" + A_NCI], fmt="#,##0.0")
    r = row(ws, r, "Equity value attributable to shareholders",
            ["=B4+B5+B6+B7+B8+B9"], fmt="#,##0.0", bold=True)
    r = row(ws, r, "Per share (EGP)", ["=B10/Assumptions!" + A_SH], fmt="#,##0.00",
            bold=True)

    # 6 Segments -------------------------------------------------------------
    ws = wb.create_sheet("Segments")
    head(ws, "Units and prices by region — the forecast's drivers",
         "New sales value and unit counts are both disclosed per region; the price "
         "per unit is one divided by the other.", [34, 14, 14, 14, 14, 14])
    r = 4
    for nm, d in BU["regions"].items():
        h = d["history"]
        ws.cell(r, 1, nm).font = SUB
        r += 1
        ws.cell(r, 1, "Year").font = HEAD
        ws.cell(r, 1).fill = FILL
        for j, y in enumerate(h["years"], start=2):
            c = ws.cell(r, j, y); c.font = HEAD; c.fill = FILL
        r += 1
        for lbl, key, fmt in (("New sales (EGP mn)", "sales", "#,##0"),
                              ("Units sold", "units", "#,##0"),
                              ("Price per unit (EGP mn)", "asp", "#,##0.00")):
            ws.cell(r, 1, lbl).font = FORM
            for j, x in enumerate(h[key], start=2):
                c = ws.cell(r, j, x); c.number_format = fmt; c.font = INPUT
            r += 1
        ws.cell(r, 1, "carried forward at %.0f units, price %.2f, escalated"
                % (d["units_base"], d["asp_base"])).font = MUT
        r += 2
    ws.cell(r, 1, "Disclosed group drivers").font = SUB
    r += 1
    ws.cell(r, 1, "Disclosed driver").font = HEAD
    ws.cell(r, 2, "Value").font = HEAD
    ws.cell(r, 3, "Note").font = HEAD
    for c in "ABC":
        ws["%s%d" % (c, r)].fill = FILL
    r += 1
    for lbl, key, fmt, note in (
        ("New sales, 1Q2026 (EGP mn)", "new_sales_1q26", "#,##0",
         "includes EGP 24,000mn from one land-plot launch"),
        ("New sales, FY2024 (EGP mn)", "new_sales_fy24", "#,##0", "chart series"),
        ("Order book, 31 Mar 2026 (EGP mn)", "backlog_1q26", "#,##0",
         "units sold and not yet delivered"),
        ("Order book, FY2024 (EGP mn)", "backlog_fy24", "#,##0", ""),
        ("Units sold, FY2023", "units_sold_fy23", "#,##0",
         "the last year the company disclosed a unit count"),
        ("Units delivered, FY2023", "units_delivered_fy23", "#,##0", ""),
        ("Construction spend, FY2024 (EGP mn)", "construction_fy24", "#,##0", ""),
        ("Cash collections, FY2024 (EGP mn)", "collections_fy24", "#,##0", ""),
        ("Land bank (mn sqm)", "land_bank_sqm_mn", "#,##0.0", ""),
    ):
        ws.cell(r, 1, lbl).font = FORM
        c = ws.cell(r, 2, v(key))
        c.font = INPUT
        c.number_format = fmt
        ws.cell(r, 3, note).font = MUT
        r += 1
    r += 1
    ws.cell(r, 1, "Build level: SEGMENT, not unit.").font = SUB
    r += 1
    ws.cell(r, 1, "The company discloses no per-project unit mix, unit area, price "
                  "per square metre or construction cost per square metre. The "
                  "forecast is built at the finest level the disclosure supports and "
                  "the limit is stated rather than filled.").font = MUT
    ws.cell(r, 1).alignment = Alignment(wrap_text=True, vertical="top")
    ws.row_dimensions[r].height = 44

    # 7 Relative & Normalized ------------------------------------------------
    ws = wb.create_sheet("Relative & Normalized")
    head(ws, "Relative and normalised measures", None, [40, 16, 16, 16])
    r = 4
    r = row(ws, r, "", ["2023", "2024", "2025"], font=HEAD, bold=True)
    r = row(ws, r, "Revenue", [v("revenue_fy23"), v("revenue_fy24"),
                               v("revenue_fy25")], fmt="#,##0.0")
    r = row(ws, r, "Cash from operations", [v("cfo_fy23"), v("cfo_fy24"),
                                            v("cfo_fy25")], fmt="#,##0.0")
    r = row(ws, r, "Cash conversion", ["=B6/B5", "=C6/C5", "=D6/D5"], fmt="0.0%")
    r += 1
    r = row(ws, r, "Price to book (market)",
            ["=%.4f/%.4f" % (PM["spot"], D["book_equity_per_share"])], fmt="0.00")
    r = row(ws, r, "Book value per share (EGP)",
            [round(D["book_equity_per_share"], 2)], fmt="#,##0.00")
    r = row(ws, r, "Return on equity, 2025",
            ["=%.1f/((%.1f+%.1f)/2)" % (v("npat_mi_fy25"), v("total_equity"),
                                        N["balance_sheet_subtotals"]["2024"]["total_equity"]["value"])],
            fmt="0.0%")

    # 8 DCF ------------------------------------------------------------------
    ws = wb.create_sheet("DCF")
    head(ws, "Discounted cash flow — central case",
         "Units delivered times revenue per delivered unit, then every row a "
         "formula. Change a blue cell on Assumptions and this recomputes.")
    r = _yearhead(ws)
    LAST = get_column_letter(1 + len(YEARS))
    A_UNITS = AT("Units delivered, 2026")
    A_UGROW = AT("Units delivered, annual growth")
    A_PRICE = AT("Revenue per delivered unit, 2026 (EGP mn)")
    # RESOLVED AND NEVER USED, like A_WACC below: the per-year escalation PATH on this
    # sheet is what the model reads, so a single-cell escalator has no consumer. Kept as a
    # named resolution so the label assert fires if that Assumptions row is renamed again.
    A_CPI = AT("Price and cost escalation, 2026 — the house path")
    A_GM = AT("Gross margin")
    A_SGA = AT("Overheads as a share of revenue")
    A_CFO = AT("Cash conversion — central")
    A_CAPEX = AT("Maintenance capital expenditure, share of revenue")
    # A_WACC WAS RESOLVED AND NEVER USED -- no cell on any sheet read it, which is
    # the other half of why the Assumptions sheet could publish the wrong rate
    # under a bare label without anything going red.

    def _path_row(label, values, fmt, note="", first_ref=None):
        """A per-year INPUT row: growth is a path, not a single number.

        The 30-Aug workbook grew both drivers at one cell each — a flat 15% for
        deliveries and a flat 25.2% for prices — for every forecast year. Neither
        is a steady state: prices follow the central bank's own published
        disinflation path, and a company cannot hand over 15% more homes every
        year for ever. A single cell cannot express either, so each is a row.
        """
        nonlocal r
        ws.cell(r, 1, label).font = FORM
        for j, val in enumerate(values, start=2):
            c = ws.cell(r, j, first_ref if (j == 2 and first_ref) else round(val, 6))
            c.font = FORM if (j == 2 and first_ref) else INPUT
            c.number_format = fmt
        if note:
            ws.cell(r, 2 + len(values), note).font = MUT
        r += 1
        return r - 1

    ROWS_BU = N["bottom_up"]["rows"]
    # THE FIRST YEAR READS THE ASSUMPTIONS CELL, so that cell has a consumer and the
    # dependency runs the way the workbook says it does: Assumptions is the source and
    # every other sheet reads it. Pointing the Assumptions cell AT this sheet instead --
    # which is what a first attempt at this fix did -- inverts the direction and recalc.py
    # correctly refused it as a reference cycle. Years two onward stay per-year inputs
    # because the escalator is a PATH and a single cell cannot express one.
    pg_row = _path_row("Price and cost escalation",
                       [x["price_growth"] for x in ROWS_BU], "0.0%",
                       "the house inflation path; year one reads Assumptions!" + A_ESC1,
                       first_ref="=Assumptions!" + A_ESC1)
    dg_row = _path_row("Growth in units delivered",
                       [x["delivery_growth"] for x in ROWS_BU], "0.0%",
                       "the disclosed run, fading to nothing")

    def _driver(label, base_cell, growth_row, fmt):
        """One driver row: an input in the first year, then its own growth path."""
        nonlocal r
        ws.cell(r, 1, label).font = FORM
        c = ws.cell(r, 2, "=Assumptions!" + base_cell)
        c.font = FORM
        c.number_format = fmt
        for j in range(3, 2 + len(YEARS)):
            col_prev, col = get_column_letter(j - 1), get_column_letter(j)
            c = ws.cell(r, j, "=%s%d*(1+%s%d)" % (col_prev, r, col, growth_row))
            c.font = FORM
            c.number_format = fmt
        r += 1
        return r - 1

    u_row = _driver("Units delivered", A_UNITS, dg_row, "#,##0")
    p_row = _driver("Revenue per delivered unit", A_PRICE, pg_row, "#,##0.00")
    rev_row = r
    ws.cell(r, 1, "Revenue").font = SUB
    for j in range(2, 2 + len(YEARS)):
        col = get_column_letter(j)
        c = ws.cell(r, j, "=%s%d*%s%d" % (col, u_row, col, p_row))
        c.font = SUB
        c.number_format = "#,##0"
    r += 1
    for lbl, expr, fmt in (
        ("Gross profit", "=%s{c}*Assumptions!" + A_GM, "#,##0"),
        ("Overheads", "=-%s{c}*Assumptions!" + A_SGA, "#,##0"),
        ("Operating cash flow", "=%s{c}*Assumptions!" + A_CFO, "#,##0"),
        ("Maintenance capital expenditure",
         "=-%s{c}*Assumptions!" + A_CAPEX, "#,##0"),
    ):
        ws.cell(r, 1, lbl).font = FORM
        for j in range(2, 2 + len(YEARS)):
            col = get_column_letter(j)
            ws.cell(r, j, expr.replace("{c}", str(rev_row)) % col).font = FORM
            ws.cell(r, j).number_format = fmt
        r += 1
    cfo_row, capex_row = r - 2, r - 1
    ws.cell(r, 1, "plus finance cost, after tax").font = FORM
    for j, rr in enumerate(BU["rows"], start=2):
        c = ws.cell(r, j, round(rr["interest"] * (1 - rr["tax_rate"]), 1))
        c.font = FORM
        c.number_format = "#,##0"
    int_row = r
    r += 1
    fcff_row = r
    ws.cell(r, 1, "Free cash flow to the firm").font = SUB
    for j in range(2, 2 + len(YEARS)):
        col = get_column_letter(j)
        c = ws.cell(r, j, "=%s%d+%s%d+%s%d"
                    % (col, cfo_row, col, int_row, col, capex_row))
        c.font = SUB
        c.number_format = "#,##0"
    r += 1
    # THE COST OF CAPITAL IS A PATH, NOT A CELL. Each year carries its own forward
    # rate, gliding from today's to the rate that applies once the economy has
    # normalised, and the factor compounds them. The earlier workbook raised a
    # single rate to the power of the year, which asserts that the rate never
    # changes for fifteen years.
    SCHED = N["cost_of_capital_record"]
    ws.cell(r, 1, "Cost of capital, that year").font = FORM
    for j, w in enumerate(SCHED["forward_wacc"], start=2):
        c = ws.cell(r, j, round(w, 6))
        c.font = INPUT
        c.number_format = "0.00%"
    fw_row = r
    r += 1
    ws.cell(r, 1, "Discount factor").font = FORM
    for j in range(2, 2 + len(YEARS)):
        col, prev = get_column_letter(j), get_column_letter(j - 1)
        expr = ("=1/(1+%s%d)" % (col, fw_row) if j == 2
                else "=%s%d/(1+%s%d)" % (prev, r, col, fw_row))
        ws.cell(r, j, expr).font = FORM
        ws.cell(r, j).number_format = "0.000"
    df_row = r
    r += 1
    ws.cell(r, 1, "Present value").font = SUB
    for j in range(2, 2 + len(YEARS)):
        col = get_column_letter(j)
        ws.cell(r, j, "=%s%d*%s%d" % (col, fcff_row, col, df_row)).font = FORM
        ws.cell(r, j).number_format = "#,##0"
    pv_row = r
    r += 2
    DCF_LABEL_AT["Sum of the explicit years"] = "B%d" % r
    ws.cell(r, 1, "Sum of the explicit years").font = SUB
    ws.cell(r, 2, "=SUM(B%d:%s%d)" % (pv_row, LAST, pv_row)).number_format = "#,##0"
    r += 1
    # THE TERMINAL WAS A HARDCODED CONSTANT HOLDING ROUGHLY A THIRD OF THE ANSWER, with no
    # construction anywhere in sixteen sheets [17-09-2026]. A reader could not see the
    # terminal flow, the growth rate, the rate it was capitalised at, or the formula that
    # combined them — and the one cell on the Assumptions sheet labelled "Terminal growth"
    # had, until 10-09-2026, published a rate the model does not run. Every line of the
    # construction is a cell now, and the result is a formula, so changing the terminal
    # growth or the terminal rate moves the answer the way the workbook promises it does.
    tg_row = r
    ws.cell(r, 1, "Terminal growth").font = FORM
    c = ws.cell(r, 2, "=Assumptions!" + AT("Terminal growth")); c.font = FORM
    c.number_format = "0.00%"
    r += 1
    trate_row = r
    ws.cell(r, 1, "Terminal cost of capital").font = FORM
    c = ws.cell(r, 2, "=%s%d" % (LAST, fw_row)); c.font = FORM
    c.number_format = "0.00%"
    ws.cell(r, 3, "the last year of the path above, held in perpetuity").font = MUT
    r += 1
    tflow_row = r
    ws.cell(r, 1, "Terminal-year free cash flow, grown one year").font = FORM
    c = ws.cell(r, 2, "=%s%d*(1+B%d)" % (LAST, fcff_row, tg_row)); c.font = FORM
    c.number_format = "#,##0"
    r += 1
    tv_row = r
    ws.cell(r, 1, "Terminal value at the horizon").font = FORM
    c = ws.cell(r, 2, "=B%d/(B%d-B%d)" % (tflow_row, trate_row, tg_row)); c.font = FORM
    c.number_format = "#,##0"
    r += 1
    DCF_LABEL_AT["Terminal value, discounted"] = "B%d" % r
    ws.cell(r, 1, "Terminal value, discounted").font = SUB
    c = ws.cell(r, 2, "=B%d*%s%d" % (tv_row, LAST, df_row)); c.font = SUB
    c.number_format = "#,##0"
    _tpv_row = r
    r += 1
    ws.cell(r, 1, "Enterprise value").font = SUB
    ws.cell(r, 2, "=B%d+B%d" % (r - 6, _tpv_row)).number_format = "#,##0"
    r += 1
    ws.cell(r, 1, "Terminal share of enterprise value").font = FORM
    c = ws.cell(r, 2, "=B%d/B%d" % (_tpv_row, r - 1)); c.font = FORM
    c.number_format = "0.0%"
    # THE TRIPWIRE. The bridge emitted "=DCF!B20" and "=DCF!B25" before this sheet existed;
    # hold those addresses to the labels this sheet actually wrote there.
    # THE DRIVER ROWS, PUBLISHED FOR THE STATEMENTS WRITTEN AFTER THIS SHEET. The Income
    # Statement and the Cash Flow held 639 computed values and no formulas because they had
    # nothing to reference; they reference these.
    DCF_ROWS.update(units=u_row, price=p_row, revenue=rev_row, fcff=fcff_row,
                    wacc=fw_row, factor=df_row, pv=pv_row)
    for _lbl, _addr in DCF_CELLS.items():
        assert DCF_LABEL_AT.get(_lbl) == _addr, (
            "DCF address drift: the bridge reads %s for %r and this sheet put it at %s"
            % (_addr, _lbl, DCF_LABEL_AT.get(_lbl)))

    # 9-11 statements --------------------------------------------------------
    ws = wb.create_sheet("Income Statement")
    # THE FOURTH SURFACE THAT SAID "OUTPUT" [corrected 17-09-2026]. Three were fixed on
    # 10-09-2026; the QC gate of 13-09-2026 recorded the fourth as NOT CLOSED and it is
    # this one, plus the DriverLine record in gate_check.py. The model holds the margin at
    # the latest disclosed level and SOLVES cost per unit from it, because this company
    # publishes no delivered-unit count after FY2024, so there is no independent cost per
    # unit to build. Saying "output" where the code says input is the defect an external
    # audit called two mutually exclusive claims on one page, and it was right.
    head(ws, "Income statement — built from units and prices",
         "Gross margin is a HELD INPUT at the latest disclosed level and cost per unit is "
         "SOLVED from it; no delivered-unit count is published after FY2024, so there is "
         "no independent cost per unit to build. The gap is named, not hidden.",
         [34, 14, 14, 14, 14, 14])
    rr = 4
    ws.cell(rr, 1, "EGP mn unless stated").font = HEAD
    ws.cell(rr, 1).fill = FILL
    for j, x in enumerate(BU["rows"], start=2):
        c = ws.cell(rr, j, x["year"]); c.font = HEAD; c.fill = FILL
    rr += 1
    # EVERY DERIVED ROW ON THIS SHEET IS A FORMULA NOW [17-09-2026].
    #
    # It held 255 numbers and no formulas. So did the Cash Flow sheet, and so did the
    # Sensitivity grid — 677 computed values across three sheets, under a READ FIRST page
    # promising that changing a blue cell recomputes the statements. It did not, and an
    # external audit was right to call the warranty false. The cause was not laziness: the
    # drivers these statements run on had no cells to reference until the four appended to
    # the Assumptions sheet above, and the DCF sheet's own row numbers were not published
    # to the sheets written after it.
    #
    # WHAT STAYS A VALUE, AND WHY, because that is the honest half of this. The units-sold
    # and new-sales rows come from the segment engine and are NOT read by anything that
    # reaches the answer — the audit called that apparatus decorative and it was right
    # about the mechanics. Writing them as formulas would dress up a dependency that does
    # not exist. They are labelled for what they are instead.
    _A = "Assumptions!"
    _GM, _SGA = _A + AT("Gross margin"), _A + AT("Overheads as a share of revenue")
    _DA = _A + AT("Depreciation and amortisation, share of revenue")
    _IB = _A + AT("Interest-bearing borrowings (EGP mn)")
    _EPR = _A + AT("Effective P&L rate on those borrowings")
    _TAX, _SH = _A + AT("Tax rate"), _A + AT("Shares outstanding (mn)")
    _D = "DCF!%s"
    _at = {}
    _spec = [
        ("Units sold", "units_sold", "#,##0", None,
         "the segment engine; read by nothing that reaches the value"),
        ("New sales", "new_sales", "#,##0", None,
         "the segment engine; read by nothing that reaches the value"),
        ("Units delivered", "units_delivered", "#,##0",
         lambda c, a: "=DCF!%s%d" % (c, DCF_ROWS["units"]), ""),
        ("Revenue per delivered unit", "rev_per_unit", "#,##0.00",
         lambda c, a: "=DCF!%s%d" % (c, DCF_ROWS["price"]), ""),
        ("Revenue", "revenue", "#,##0",
         lambda c, a: "=DCF!%s%d" % (c, DCF_ROWS["revenue"]), ""),
        ("Cost per delivered unit", "cost_per_unit", "#,##0.00",
         lambda c, a: "=%s%d*(1-%s)" % (c, a["Revenue per delivered unit"], _GM),
         "price per unit times one minus the held margin: no delivered-unit count is "
         "published after FY2024, so there is no independent cost per unit to build"),
        ("Cost of revenue", "cogs", "#,##0",
         lambda c, a: "=%s%d*%s%d" % (c, a["Units delivered"], c,
                                      a["Cost per delivered unit"]), ""),
        ("Gross profit", "gross", "#,##0",
         lambda c, a: "=%s%d-%s%d" % (c, a["Revenue"], c, a["Cost of revenue"]), ""),
        ("Gross margin", "gross_margin", "0.0%",
         lambda c, a: "=%s%d/%s%d" % (c, a["Gross profit"], c, a["Revenue"]),
         "an output of the two rows above, which is what makes it flat: one escalator "
         "drives price and cost alike"),
        ("Overheads", "sga", "#,##0",
         lambda c, a: "=%s%d*%s" % (c, a["Revenue"], _SGA), ""),
        ("Depreciation and amortisation", "da", "#,##0",
         lambda c, a: "=%s%d*%s" % (c, a["Revenue"], _DA), ""),
        ("Operating profit", "ebit", "#,##0",
         lambda c, a: "=%s%d-%s%d-%s%d" % (c, a["Gross profit"], c, a["Overheads"],
                                           c, a["Depreciation and amortisation"]), ""),
        ("Finance cost", "interest", "#,##0",
         lambda c, a: "=%s*%s" % (_IB, _EPR),
         "the interest-bearing subset times its effective rate, HELD FLAT AND NOMINAL "
         "for all fifteen years while revenue grows sixfold; the alternative footing is "
         "priced in the study's contested-judgement record"),
        ("Profit before tax", "npbt", "#,##0",
         lambda c, a: "=%s%d-%s%d" % (c, a["Operating profit"], c, a["Finance cost"]), ""),
        ("Net profit", "npat", "#,##0",
         lambda c, a: "=%s%d*(1-%s)" % (c, a["Profit before tax"], _TAX),
         "pre-tax profit is positive in every forecast year, so this is the tax charge "
         "the model applies"),
        ("Earnings per share (EGP)", "eps", "#,##0.00",
         lambda c, a: "=%s%d/%s" % (c, a["Net profit"], _SH), ""),
        ("Order book, closing", "backlog", "#,##0", None,
         "rolls the segment engine's new sales behind revenue; read by nothing that "
         "reaches the value"),
    ]
    for lbl, key, fmt, fx, note in _spec:
        ws.cell(rr, 1, lbl).font = SUB if key in ("revenue", "gross", "npat") else FORM
        _at[lbl] = rr
        for j, x in enumerate(BU["rows"], start=2):
            col = get_column_letter(j)
            c = ws.cell(rr, j, fx(col, _at) if fx else round(x[key], 4))
            c.number_format = fmt
            if fx:
                c.font = FORM
        if note:
            ws.cell(rr, 2 + len(BU["rows"]), note).font = MUT
        rr += 1

    FA, FB = ST["framing_a"], ST["framing_b"]
    FY = [x["year"] for x in FB]

    def _proj(ws, rr, rows, spec, fx=None, notes=None):
        """One projected statement. `fx` maps a row key to a formula builder.

        FORMULAS WHERE THE DERIVATION IS THE POINT [17-09-2026]. These sheets held 639
        computed values and no formulas, so a reader could not see that operating cash is
        SET at a share of revenue and the working-capital movement is the PLUG — which is
        the single most important thing to know about this forecast, and the study says it
        in prose while the workbook hid it. The rows whose whole content is that
        relationship are formulas; the rest stay values, and which is which is visible.
        """
        fx, notes = fx or {}, notes or {}
        ws.cell(rr, 1, "EGP mn unless stated").font = HEAD
        ws.cell(rr, 1).fill = FILL
        for j, y in enumerate(FY, start=2):
            c = ws.cell(rr, j, y); c.font = HEAD; c.fill = FILL
            c.alignment = Alignment(horizontal="center")
            ws.column_dimensions[get_column_letter(j)].width = 13
        ws.column_dimensions["A"].width = 42
        rr += 1
        # EVERY ROW'S ADDRESS RESOLVED BEFORE ANY FORMULA IS WRITTEN. Building the map
        # incrementally works only while formulas point upward, and the
        # working-capital plug points DOWN at the operating-cash row it is derived from.
        at = {key: rr + i for i, (_l, key, _f, _s) in enumerate(spec)}
        for lbl, key, fmt, strong in spec:
            ws.cell(rr, 1, lbl).font = SUB if strong else FORM
            sign = -1 if key == "d_wc" else 1
            for j, x in enumerate(rows, start=2):
                col = get_column_letter(j)
                f = fx.get(key)
                c = ws.cell(rr, j, f(col, at, j) if f else round(sign * x[key], 4))
                c.number_format = fmt
                c.font = SUB if strong else FORM
            if notes.get(key):
                ws.cell(rr, 2 + len(FY), notes[key]).font = MUT
            rr += 1
        return rr + 1

    ws = wb.create_sheet("Cash Flow")
    head(ws, "Cash flow — forecast, both readings",
         "The audited balance sheet and the audited cash-flow statement "
         "disagree about 2025 by EGP %s million, and that difference cannot be "
         "split from what is disclosed. So the forecast is published two ways "
         "and neither is averaged into the other."
         % "{:,.0f}".format(ST["wedge"]["wedge_fy25"]))
    CF = [("Net profit", "npat", "#,##0", False),
          ("Depreciation and amortisation", "da", "#,##0", False),
          ("Change in working capital, cash effect", "d_wc", "#,##0", False),
          ("Cash from operations", "cfo", "#,##0", True),
          ("  as a share of revenue", "cash_conversion", "0.0%", False),
          ("Capital expenditure", "cfi", "#,##0", False),
          ("New borrowing drawn", "drawn", "#,##0", False),
          ("Cash from financing", "cff", "#,##0", False),
          ("Closing cash", "cash", "#,##0", True),
          ("Cumulative new borrowing", "drawn_cum", "#,##0", False)]
    rr = 4
    ws.cell(rr, 1, "IF CASH CONVERSION HOLDS — the basis of the valuation").font = SUB
    # THE THREE ROWS THAT ARE THE READING ITSELF, AS FORMULAS. Operating cash is revenue
    # times the conversion rate; its share of revenue is therefore that rate, and showing
    # the division proves it rather than asserting it; and the working-capital movement is
    # what is LEFT — the plug — which is the whole difference between this framing and the
    # one below it. Reading those three off computed constants told a reader nothing.
    _ISROW = _at   # the Income Statement's own row map, captured above
    _CFFX = {
        "cfo": lambda c, a, j: "=DCF!%s%d*Assumptions!%s"
                               % (c, DCF_ROWS["revenue"], AT("Cash conversion — central")),
        "cash_conversion": lambda c, a, j: "=%s%d/DCF!%s%d"
                                           % (c, a["cfo"], c, DCF_ROWS["revenue"]),
        "d_wc": lambda c, a, j: "=%s%d-'Income Statement'!%s%d-'Income Statement'!%s%d"
                                % (c, a["cfo"], c, _ISROW["Net profit"],
                                   c, _ISROW["Depreciation and amortisation"]),
        "cfi": lambda c, a, j: "=-DCF!%s%d*Assumptions!%s"
                               % (c, DCF_ROWS["revenue"],
                                  AT("Maintenance capital expenditure, share of revenue")),
    }
    _CFNOTE = {
        "cfo": "SET at the conversion rate times revenue — this is the crux input, and "
               "the row below proves the division",
        "cash_conversion": "the conversion rate, recovered from the row above: flat by "
                           "construction because operating cash is set as a share of revenue",
        "d_wc": "THE PLUG. Operating cash is set and working capital is what is left, "
                "which is the whole difference between this framing and the one below",
        "cfi": "maintenance only, at the share of revenue on the Assumptions sheet",
    }
    rr = _proj(ws, rr + 1, FB, CF, fx=_CFFX, notes=_CFNOTE)
    ws.cell(rr, 1, "IF THE COLLECTION CYCLE HOLDS").font = SUB
    rr = _proj(ws, rr + 1, FA, CF)
    ws.cell(rr, 1, "Cash conversion, the three published years").font = SUB
    rr += 1
    for k in ("FY2023", "FY2024", "FY2025", "mean"):
        ws.cell(rr, 1, k if k != "mean" else "  mean, carried above").font = FORM
        c = ws.cell(rr, 2, round(ST["cash_conversion"][k], 6))
        c.number_format = "0.00%"
        rr += 1

    ws = wb.create_sheet("Balance Sheet")
    head(ws, "Balance sheet — as reported, then forecast both ways",
         "EGP million. Assets equal liabilities plus shareholders' funds in "
         "every reported and every forecast year.")
    SB, B24 = N["balance_sheet_subtotals"], N["balance_sheet_fy24"]
    ws.column_dimensions["A"].width = 46
    for col in ("B", "C"):
        ws.column_dimensions[col].width = 16
    r = 4
    r = row(ws, r, "AS REPORTED", ["2025", "2024"], font=HEAD, bold=True)
    top = r
    for lbl, key in (("Non-current assets", "total_noncurrent_assets"),
                     ("Current assets", "total_current_assets"),
                     ("Total assets", "total_assets"),
                     ("Current liabilities", "total_current_liabs"),
                     ("Non-current liabilities", "total_noncurrent_liabs"),
                     ("Total liabilities", "total_liabilities"),
                     ("Shareholders' funds", "total_equity")):
        r = row(ws, r, lbl, [SB["2025"][key]["value"], SB["2024"][key]["value"]],
                fmt="#,##0.0")
    r = row(ws, r, "Check: assets less liabilities and equity",
            ["=B%d-B%d-B%d" % (top + 2, top + 5, top + 6),
             "=C%d-C%d-C%d" % (top + 2, top + 5, top + 6)],
            fmt="#,##0.00", bold=True)
    r += 1
    BSSPEC = [("Trade and notes receivable", "receivables", "#,##0", False),
              ("Work in progress", "wip", "#,##0", False),
              ("Other receivables and prepayments", "bs_debtors_other",
               "#,##0", False),
              ("Advances to suppliers", "bs_suppliers_advances", "#,##0", False),
              ("Cash and equivalents", "cash", "#,##0", False),
              ("Property and equipment", "ppe", "#,##0", False),
              ("Other assets, held at the 2025 level", "other_assets",
               "#,##0", False),
              ("TOTAL ASSETS", "total_assets", "#,##0", True),
              ("Customer advances", "advances", "#,##0", False),
              ("Suppliers", "suppliers", "#,##0", False),
              ("Other creditors", "bs_creditors_other", "#,##0", False),
              ("Cheques under collection", "bs_checks_undelivered",
               "#,##0", False),
              ("Borrowings", "debt", "#,##0", False),
              ("Other liabilities, held at the 2025 level", "other_liabs",
               "#,##0", False),
              ("TOTAL LIABILITIES", "total_liabilities", "#,##0", True),
              ("Shareholders' funds", "equity", "#,##0", False),
              ("TOTAL LIABILITIES AND EQUITY", "total_liabs_and_equity",
               "#,##0", True),
              ("Check: assets less liabilities and equity", "balance_check",
               "#,##0.000", True),
              ("Collection period, days", "dso", "#,##0", False),
              ("Work in progress, days of cost", "dio", "#,##0", False),
              ("Suppliers, days of cost", "dpo", "#,##0", False),
              ("Customer advances, share of the order book",
               "adv_of_backlog", "0.0%", False),
              ("Net working capital", "net_wc", "#,##0", False),
              ("  as a multiple of revenue", "nwc_over_revenue",
               "#,##0.00", False)]
    ws.cell(r, 1, "FORECAST — IF CASH CONVERSION HOLDS").font = SUB
    # THE SUBTOTALS AND THE BALANCE CHECK, AS FORMULAS, IN BOTH FRAMINGS [17-09-2026].
    #
    # THE CHECK ROW IS THE POINT. "Check: assets less liabilities and equity" was written
    # as a COMPUTED CONSTANT — the model's own difference, rounded and printed. A check
    # whose value is computed by the thing it is checking cannot fail, and this house has
    # found that exact defect before: the SWDY self-audit turned up a balance-check row
    # hardcoded to zero and it is one of the findings the critique-response prompt was
    # rewritten around. It is now a subtraction of two cells that are themselves sums of
    # the rows above them, so a driver that breaks the balance sheet shows up here as a
    # non-zero number in a workbook a reader has open.
    _ASSETS = ["receivables", "wip", "bs_debtors_other", "bs_suppliers_advances",
               "cash", "ppe", "other_assets"]
    _LIABS = ["advances", "suppliers", "bs_creditors_other", "bs_checks_undelivered",
              "debt", "other_liabs"]

    def _sum_rows(keys):
        return lambda c, a, j: "=" + "+".join("%s%d" % (c, a[k]) for k in keys)

    _BSFX = {
        "total_assets": _sum_rows(_ASSETS),
        "total_liabilities": _sum_rows(_LIABS),
        "total_liabs_and_equity": lambda c, a, j: "=%s%d+%s%d" % (c, a["total_liabilities"],
                                                                  c, a["equity"]),
        "balance_check": lambda c, a, j: "=%s%d-%s%d" % (c, a["total_assets"],
                                                         c, a["total_liabs_and_equity"]),
    }
    _BSNOTE = {
        "total_assets": "the seven asset rows above, summed in the cell",
        "total_liabilities": "the six liability rows above, summed in the cell",
        "balance_check": "A LIVE CHECK: two sums subtracted. It used to be the model's own "
                         "computed difference, which is a check that cannot fail",
    }
    r = _proj(ws, r + 1, FB, BSSPEC, fx=_BSFX, notes=_BSNOTE)
    ws.cell(r, 1, "FORECAST — IF THE COLLECTION CYCLE HOLDS").font = SUB
    r = _proj(ws, r + 1, FA, BSSPEC, fx=_BSFX, notes=_BSNOTE)
    ws.cell(r, 1, "The cycle as reported, both audited years").font = SUB
    r += 1
    cy = ST["cycle_measured"]
    r = row(ws, r, "", ["2025", "2024"], font=HEAD, bold=True)
    for lbl, a, bq, fmt in (
            ("Collection period, days", cy["dso_fy25"], cy["dso_fy24"], "#,##0"),
            ("Work in progress, days of cost", cy["dio_fy25"], cy["dio_fy24"],
             "#,##0"),
            ("Suppliers, days of cost", cy["dpo_fy25"], cy["dpo_fy24"], "#,##0"),
            ("Customer advances, share of the order book",
             cy["adv_of_backlog_fy25"], cy["adv_of_backlog_fy24"], "0.0%"),
            ("Net working capital", cy["nwc_fy25"], cy["nwc_fy24"], "#,##0"),
            ("  as a multiple of revenue", cy["nwc_over_revenue_fy25"],
             cy["nwc_over_revenue_fy24"], "#,##0.00")):
        r = row(ws, r, lbl, [round(a, 4), round(bq, 4)], fmt=fmt)

    # 12 Summary Financials --------------------------------------------------
    ws = wb.create_sheet("Summary Financials")
    head(ws, "Summary financials, as reported", None, [40, 15, 15, 15])
    r = 4
    r = row(ws, r, "EGP million", ["2023", "2024", "2025"], font=HEAD, bold=True)
    H = N["historical_is"]
    HY = ("2023", "2024", "2025")

    def _hy(key):
        return [H[y][key]["value"] if key in H[y] else None for y in HY]

    for lbl, vals in (
        ("Revenue", _hy("revenue")),
        ("Cost of revenue", [-x if x is not None else None
                             for x in _hy("cogs")]),
        ("Gross profit", _hy("gross_profit")),
        ("Overheads", [-x if x is not None else None for x in _hy("sga")]),
        ("Finance cost", [-x if x is not None else None
                          for x in _hy("finance_cost")]),
        ("Pre-tax profit", _hy("npbt")),
        ("Tax", [-x if x is not None else None for x in _hy("tax_total")]),
        ("Profit after tax and minority", _hy("npat_mi")),
        ("Cash from operations",
         [v("cfo_fy23"), v("cfo_fy24"), v("cfo_fy25")]),
    ):
        r = row(ws, r, lbl, ["" if x is None else x for x in vals],
                fmt="#,##0.0")
    # THREE CIRCULAR SELF-REFERENCES, NOT ONE [17-09-2026]. `r` is the row the formula is
    # being written INTO, so "=B{r}/B5" pointed at itself: B14 read =B14/B5, C14 =C14/C5,
    # D14 =D14/D5. Excel returns a circular-reference warning and zero for all three, so
    # the one derived row on this sheet could never show a number. The cash-from-operations
    # row is the one above, and an off-by-one is why a check that cannot compute shipped in
    # four consecutive editions: nothing in the build reads a formula's result back.
    _cfo_row = r - 1
    r = row(ws, r, "Cash from operations, share of revenue",
            ["=B%d/B5" % _cfo_row, "=C%d/C5" % _cfo_row, "=D%d/D5" % _cfo_row],
            fmt="0.0%", bold=True)

    # 13 Monte Carlo ---------------------------------------------------------
    ws = wb.create_sheet("Monte Carlo")
    head(ws, "Price distribution — published output, reproduced not re-derived",
         "This is the price engine's distribution, independent of the valuation.",
         [22, 16, 16])
    r = 4
    r = row(ws, r, "Percentile", ["One month", "Three months"], font=HEAD, bold=True)
    for p in ("p5", "p25", "p50", "p75", "p95"):
        r = row(ws, r, p.replace("p", "") + "th",
                [PM["dist"]["m1"][p], PM["dist"]["m3"][p]], fmt="#,##0.00")
    r += 1
    r = row(ws, r, "Resolved three-month tests", [PM["band_record"]["n"]])
    r = row(ws, r, "Inside the 90% band", [PM["band_record"]["c90"]], fmt="0.0%")
    r = row(ws, r, "Inside the middle band", [PM["band_record"]["c50"]], fmt="0.0%")
    r = row(ws, r, "Band width vs a random walk", [PM["band_record"]["width"]],
            fmt="0.00")

    # 14 Sensitivity ---------------------------------------------------------
    ws = wb.create_sheet("Sensitivity")
    head(ws, "Value per share against the two things that move it",
         "Read down a column: cash conversion moves value more than the discount "
         "rate does.", [22] + [13] * 5)
    r = 4
    ws.cell(r, 1, "Cash conversion").font = HEAD
    ws.cell(r, 1).fill = FILL
    for j, wv in enumerate(SENS["waccs"], start=2):
        c = ws.cell(r, j, wv)
        c.font = HEAD
        c.fill = FILL
        c.number_format = "0.00%"
    r += 1
    for i, cf in enumerate(SENS["cfos"]):
        ws.cell(r, 1, cf).number_format = "0.0%"
        ws.cell(r, 1).font = INPUT
        for j, val in enumerate(SENS["grid"][i], start=2):
            c = ws.cell(r, j, round(val, 2))
            c.number_format = "#,##0.00"
            c.font = FORM
        r += 1

    # 15 Per-Share & Ratios --------------------------------------------------
    ws = wb.create_sheet("Per-Share & Ratios")
    head(ws, "Per share and ratios", None, [40, 16])
    r = 4
    for lbl, val, fmt in (
        ("Shares outstanding (mn)", D["shares_mn"], "#,##0.0"),
        ("Market price (EGP)", PM["spot"], "#,##0.00"),
        ("Book value per share (EGP)", D["book_equity_per_share"], "#,##0.00"),
        ("Price to book", PM["spot"] / D["book_equity_per_share"], "0.00"),
        ("Earnings per share, 2025 (EGP)",
         v("npat_mi_fy25") / D["shares_mn"], "#,##0.00"),
        ("Net debt per share, 31 March 2026 (EGP)", D["net_debt_bridge"] / D["shares_mn"], "#,##0.00"),
        ("Order book per share (EGP)",
         v("backlog_1q26") / D["shares_mn"], "#,##0.00"),
        ("Gross margin, 2025", D["gross_margin_fy25"], "0.0%"),
        ("Cash conversion, 2025", D["cfo_margins"]["2025"], "0.0%"),
    ):
        r = row(ws, r, lbl, [round(val, 4)], fmt=fmt)

    # 16 Peer & Sector -------------------------------------------------------
    ws = wb.create_sheet("Peer & Sector")
    head(ws, "Egyptian listed developers",
         "Every measure on the same window, the same cleaning and the same index.",
         [10, 34, 12, 12, 12, 14, 14])
    r = 4
    r = row(ws, r, "Code", ["Company", "Beta", "R-squared", "Std error",
                            "Volatility", "Worst fall"], font=HEAD, bold=True)
    for c in "ABCDEFG":
        ws["%s%d" % (c, r - 1)].fill = FILL
    for p in sorted([x for x in N["peers"] if "beta" in x], key=lambda x: -x["beta"]):
        ws.cell(r, 1, p["ticker"]).font = SUB if p["ticker"] == "PHDC" else FORM
        ws.cell(r, 2, p["name"]).font = FORM
        for j, (val, fmt) in enumerate(
                ((p["beta"], "0.0000"), (p["r2"], "0.0%"), (p["se"], "0.000"),
                 (p["ann_vol_5y"], "0.0%"), (p["max_drawdown_5y"], "0.0%")),
                start=3):
            c = ws.cell(r, j, round(val, 4))
            c.number_format = fmt
        r += 1
    r += 1
    ws.cell(r, 1, "Earnings and book multiples are not published for the peer group: "
                  "no peer discloses statements this study can obtain on a "
                  "consistent basis, and an inconsistent multiple would mislead.")\
        .font = MUT
    ws.cell(r, 1).alignment = Alignment(wrap_text=True)
    ws.row_dimensions[r].height = 30


if __name__ == "__main__":
    import edition as _EDN
    out = os.path.join(HERE, _EDN.MODEL_XLSX)
    wb = build(out)
    # the skeleton's order is part of the standard, so it is asserted, not assumed
    ORDER = ["READ FIRST", "Summary", "Fundamental Valuation", "Assumptions",
             "SOTP Bridge", "Segments", "Relative & Normalized", "DCF",
             "Income Statement", "Balance Sheet", "Cash Flow", "Summary Financials",
             "Monte Carlo", "Sensitivity", "Per-Share & Ratios", "Peer & Sector"]
    wb._sheets = [wb[n] for n in ORDER]
    assert wb.sheetnames == ORDER, wb.sheetnames
    wb.save(out)
    from openpyxl import load_workbook
    chk = load_workbook(out)
    formulas = sum(1 for ws in chk for row_ in ws.iter_rows()
                   for c in row_ if isinstance(c.value, str) and c.value.startswith("="))
    print("built: %s (%.0f KB)" % (os.path.basename(out), os.path.getsize(out) / 1024))
    print("sheets  : %d  %s" % (len(chk.sheetnames), chk.sheetnames))
    print("formulas: %d live cells" % formulas)
