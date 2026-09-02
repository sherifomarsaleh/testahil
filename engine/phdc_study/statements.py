"""Projected income statement, balance sheet and cash flow, and the full
discounted-cash-flow waterfall, for PHDC.

THE CENTRAL DIFFICULTY, STATED BEFORE ANY NUMBER IS PROJECTED. Palm Hills'
audited balance sheet and its audited cash-flow statement tell two different
stories about the same year, and the gap between them is the largest single
uncertainty in this valuation.

  Working capital on the balance sheet rose EGP 20,085mn in 2025.
  Net profit plus depreciation less operating cash says it rose EGP 3,146mn.
  The difference is EGP 16,939mn, or 46.8% of the year's revenue.

A wedge that size is not depreciation and it is not capitalised interest. It is
consolidation, land taken on deferred terms, and reclassification inside a
percentage-of-completion book, and the FY2025 cash-flow statement is published
only in its three totals, so the wedge CANNOT be decomposed from what is
disclosed. It is therefore not decomposed here. It is measured, named, carried
into the gap register, and the projection is built BOTH WAYS around it:

  FRAMING A — THE CYCLE HELD. Every working-capital line stays at its measured
  FY2025 ratio to revenue. The balance sheet is built from those ratios, cash
  from operations falls out of the accrual bridge, and the funding gap is met
  by borrowing, because a company cannot run a negative cash balance. This
  framing asks: if the collection cycle does not change, what does the growth
  cost to fund?

  FRAMING B — THE CASH CONVERSION HELD. Cash from operations is set at the
  company's OWN disclosed conversion — 4.3%, 17.9% and 3.9% of revenue in the
  three published years — and working capital is the derived line. This framing
  asks: if the cash keeps converting as it has, what must the cycle do? The
  answer is printed as an implied collection period, every year, so the reader
  can judge it rather than take it.

The published valuation stands on Framing B, because that is the lens the
company's own cash-flow statements support and it is the one the study already
publishes as its crux. Framing A is published beside it, unaveraged, because
the two do not agree and a single number would hide that they don't.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

import inputs as IN
import bottom_up_model as BU

REG = BU.REG
F24 = {k: v["value"] for k, v in IN.BALANCE_SHEET_FY24.items()}
W = json.load(open(os.path.join(HERE, "wacc_result.json")))
M = BU.build()
ROWS = M["rows"]
TAX = BU.TAX
SHARES = BU.SHARES_MN
KD = W["kd_pretax_local"]

# --- the working-capital book, on the lines present in BOTH audited sheets ---
# Restricted to the matched set on purpose: FY2025 discloses notes payable and
# deferred revenue that the FY2024 comparative column does not, and a ratio
# measured on a line that exists in one year only is not a ratio.
WC_ASSETS = ["accounts_receivable", "notes_recv_lt", "notes_recv_lt_undel",
             "notes_recv_st", "notes_recv_st_undel", "debtors_other",
             "work_in_progress", "suppliers_advances"]
WC_LIABS = ["advances_customers", "suppliers", "creditors_other",
            "checks_undelivered"]
RECV_LINES = ["accounts_receivable", "notes_recv_lt", "notes_recv_lt_undel",
              "notes_recv_st", "notes_recv_st_undel"]

R25, R24 = REG["revenue_fy25"], REG["revenue_fy24"]
C25, C24 = REG["cogs_fy25"], REG["cogs_fy24"]
WA25 = sum(REG[k] for k in WC_ASSETS); WA24 = sum(F24[k] for k in WC_ASSETS)
WL25 = sum(REG[k] for k in WC_LIABS);  WL24 = sum(F24[k] for k in WC_LIABS)
NWC25, NWC24 = WA25 - WL25, WA24 - WL24
RECV25 = sum(REG[k] for k in RECV_LINES)
RECV24 = sum(F24[k] for k in RECV_LINES)

# --- the cycle, measured on the two audited sheets --------------------------
DSO25, DSO24 = 365 * RECV25 / R25, 365 * RECV24 / R24
DIO25, DIO24 = (365 * REG["work_in_progress"] / C25,
                365 * F24["work_in_progress"] / C24)
DPO25, DPO24 = 365 * REG["suppliers"] / C25, 365 * F24["suppliers"] / C24
ADV25, ADV24 = (REG["advances_customers"] / REG["backlog_1q26"],
                F24["advances_customers"] / REG["backlog_fy24"])

# --- the wedge, measured, not decomposed ------------------------------------
NPAT25, DA25, CFO25 = REG["npat_mi_fy25"], REG["da_fy25"], REG["cfo_fy25"]
DWC_BOOK_25 = NWC25 - NWC24
DWC_CASH_25 = NPAT25 + DA25 - CFO25
WEDGE_25 = DWC_BOOK_25 - DWC_CASH_25
WEDGE_RATIO = WEDGE_25 / R25

# --- cash conversion, the company's own three disclosed years ---------------
CONV = {"FY2023": REG["cfo_fy23"] / REG["revenue_fy23"],
        "FY2024": REG["cfo_fy24"] / REG["revenue_fy24"],
        "FY2025": CFO25 / R25}
CONV_LO = min(CONV.values())
CONV_HI = max(CONV.values())
CONV_MID = sum(CONV.values()) / len(CONV)

CAPEX_RATIO = 0.01               # maintenance only; the build itself is inventory
DIVIDEND = 0.0                   # the company has not paid a cash dividend
MIN_CASH = REG["cash"] * 0.25    # a floor, not a target: a quarter of FY2025 cash

# Balances outside the working-capital book and outside cash and fixed assets,
# held at their audited FY2025 level so the sheet foots without a plug.
#
# BOTH SIDES ARE ANCHORED ON THE SAME PUBLISHED TOTAL. The FY2025 statements
# report total assets of EGP 172,129.8mn against total liabilities plus equity
# of EGP 172,129.9mn — they foot to EGP 0.1mn, which is rounding in the
# published statement, not an error in it. Anchoring the liabilities residual
# on total assets less equity rather than on the reported liabilities total
# puts that EGP 0.1mn where it belongs, inside the unmodelled liabilities line,
# instead of leaving it to reappear in every projected year as a balance that
# does not foot.
AUDITED_ROUNDING = (REG["total_assets"] - REG["total_liabilities"]
                    - REG["total_equity"])
OTHER_ASSETS = (REG["total_assets"] - WA25 - REG["cash"] - REG["fixed_assets"])
OTHER_LIABS = (REG["total_assets"] - REG["total_equity"] - WL25
               - BU.GROSS_DEBT)


def _mix(net):
    """Split a net working-capital total across the FY2025 leg mix."""
    k = net / NWC25
    return ({a: REG[a] * k for a in WC_ASSETS}, {l: REG[l] * k for l in WC_LIABS}, k)


def project(framing):
    """One projection. framing is 'cycle' (A) or 'conversion' (B)."""
    assert framing in ("cycle", "conversion")
    ppe, cash, equity = REG["fixed_assets"], REG["cash"], REG["total_equity"]
    debt, prev_nwc = BU.GROSS_DEBT, NWC25
    drawn_cum = 0.0
    out = []
    for r in ROWS:
        rev, cogs = r["revenue"], r["cogs"]
        capex = rev * CAPEX_RATIO
        if framing == "cycle":
            assets = {a: REG[a] / R25 * rev for a in WC_ASSETS}
            liabs = {l: REG[l] / R25 * rev for l in WC_LIABS}
            nwc = sum(assets.values()) - sum(liabs.values())
            d_nwc = nwc - prev_nwc
            cfo = r["npat"] + r["da"] - d_nwc
        else:
            cfo = rev * CONV_MID
            d_nwc = r["npat"] + r["da"] - cfo
            nwc = prev_nwc + d_nwc
            assets, liabs, _ = _mix(nwc)
        cfi = -capex
        cash_pre = cash + cfo + cfi - DIVIDEND
        drawn = max(0.0, MIN_CASH - cash_pre)      # a company short of cash borrows
        drawn_cum += drawn
        cff = drawn - DIVIDEND
        cash = cash_pre + drawn
        debt += drawn
        ppe = ppe + capex - r["da"]
        equity = equity + r["npat"] - DIVIDEND
        recv = sum(assets[k] for k in RECV_LINES)
        ta = sum(assets.values()) + cash + ppe + OTHER_ASSETS
        tl = sum(liabs.values()) + debt + OTHER_LIABS
        out.append({
            "year": r["year"],
            **{k: r[k] for k in ("revenue", "cogs", "gross", "gross_margin",
                                 "sga", "da", "ebit", "interest", "npbt",
                                 "npat", "eps", "backlog", "new_sales",
                                 "units_sold", "units_delivered",
                                 "rev_per_unit", "cost_per_unit")},
            "tax": r["npbt"] - r["npat"],
            **{("bs_" + k): v for k, v in assets.items()},
            **{("bs_" + k): v for k, v in liabs.items()},
            "receivables": recv, "wip": assets["work_in_progress"],
            "advances": liabs["advances_customers"],
            "suppliers": liabs["suppliers"],
            "net_wc": nwc, "d_wc": d_nwc,
            "dso": 365 * recv / rev,
            "dio": 365 * assets["work_in_progress"] / cogs,
            "dpo": 365 * liabs["suppliers"] / cogs,
            "adv_of_backlog": liabs["advances_customers"] / r["backlog"],
            "ppe": ppe, "cash": cash, "other_assets": OTHER_ASSETS,
            "other_liabs": OTHER_LIABS, "capex": capex,
            "cfo": cfo, "cfi": cfi, "cff": cff, "drawn": drawn,
            "drawn_cum": drawn_cum, "debt": debt, "equity": equity,
            "total_assets": ta, "total_liabilities": tl,
            "total_liabs_and_equity": tl + equity,
            "balance_check": ta - tl - equity,
            "cash_conversion": cfo / rev, "nwc_over_revenue": nwc / rev,
            "unmodelled_interest": drawn_cum * KD,
        })
        prev_nwc = nwc
    return out


def _discounter(sched):
    import cost_of_capital as COC
    return COC.Discounter(sched)


def waterfall(rows, sched, framing):
    """Operating profit to a present value, every line shown.

    Framing B reproduces valuation_v2.dcf() exactly and is asserted against it:
    free cash flow to the firm is operating cash plus the after-tax finance
    charge added back, less capital expenditure. Framing A takes the same path
    from net operating profit after tax so the working-capital draw is visible
    on its own line.
    """
    out, pv = [], 0.0
    for i, s in enumerate(rows, start=1):
        nopat = s["ebit"] * (1 - TAX)
        if framing == "conversion":
            fcff = s["cfo"] + s["interest"] * (1 - TAX) - s["capex"]
        else:
            fcff = nopat + s["da"] - s["capex"] - s["d_wc"]
        df = _discounter(sched).factor(i)
        pv += fcff * df
        out.append({"year": s["year"], "revenue": s["revenue"],
                    "ebit": s["ebit"], "tax_on_ebit": s["ebit"] * TAX,
                    "nopat": nopat, "da": s["da"], "capex": s["capex"],
                    "d_wc": s["d_wc"], "cfo": s["cfo"],
                    "interest_addback": s["interest"] * (1 - TAX),
                    "fcff": fcff, "discount_factor": df, "pv": fcff * df})
    return out, pv


def terminal(rows, sched, tg, framing):
    """A growing-perpetuity terminal value, and ONLY where one is legitimate.

    A perpetuity formula applied to a negative flow returns a large negative
    number that looks like a valuation and is not one: it asserts the company
    keeps burning cash for ever at a compounding rate, which is not a forecast
    anybody made. Where the year-five flow is negative the terminal value is
    returned as None and the framing is reported as a FUNDING STATEMENT rather
    than a value.
    """
    last = rows[-1]
    if framing == "conversion":
        tail = last["cfo"] + last["interest"] * (1 - TAX) - last["capex"]
    else:
        tail = (last["ebit"] * (1 - TAX) + last["da"] - last["capex"]
                - last["d_wc"])
    if tail <= 0:
        return tail, None, None
    # capitalised at the TERMINAL rate and brought home on the window's own
    # factor -- one date, one price of time [R-COC-01]
    dc = _discounter(sched)
    pv_tv = tail * dc.perpetuity_factor(tg)
    tv = pv_tv / dc.factor(len(rows))
    return tail, tv, pv_tv


def bridge(rows, sched, tg, framing):
    wf, pv = waterfall(rows, sched, framing)
    tail, tv, pv_tv = terminal(rows, sched, tg, framing)
    valuable = pv_tv is not None
    ev = (pv + pv_tv) if valuable else None
    # the same bridge as valuation_v2: latest disclosed sheet, minority at its
    # share of value
    eq_gross = (ev - BU.NET_DEBT_BRIDGE + BU.BS_BRIDGE["investments_assoc"]
                + BU.BS_BRIDGE["investment_property"]) if valuable else None
    nci = (eq_gross * BU.NCI_VALUE_SHARE) if valuable else None
    eq = (eq_gross - nci) if valuable else None
    return {"waterfall": wf, "pv_explicit": pv, "terminal_flow": tail,
            "terminal_value": tv, "pv_terminal": pv_tv, "ev": ev,
            "net_debt": BU.NET_DEBT_BRIDGE, "net_debt_date": BU.BRIDGE_BS_DATE,
            "equity_before_nci": eq_gross, "nci_deduction": nci, "equity": eq,
            "per_share": (eq / SHARES) if valuable else None,
            "terminal_share": (pv_tv / ev) if valuable and ev else None,
            "wacc": sched.wacc_exp, "wacc_terminal": sched.wacc_terminal, "terminal_growth": tg, "framing": framing,
            "yields_a_value": valuable,
            "funding_required": rows[-1]["drawn_cum"],
            "funding_interest": rows[-1]["unmodelled_interest"],
            "funding_interest_vs_ebit": (rows[-1]["unmodelled_interest"]
                                         / rows[-1]["ebit"])}


def build():
    return {"cycle": project("cycle"), "conversion": project("conversion")}


# ---------------------------------------------------------------------------
def _tbl(rows, spec, width=11):
    yrs = [r["year"] for r in rows]
    print(("%-38s" % "EGP mn unless stated")
          + "".join(("%%%dd" % width) % y for y in yrs))
    for lbl, key, fmt, sc in spec:
        print(("%-38s" % lbl)
              + "".join(fmt % (r[key] * sc) for r in rows))


N = ("%11.0f", 1.0); P = ("%10.1f%%", 100.0); D = ("%11.2f", 1.0)


def report():
    st = build()
    A, B = st["cycle"], st["conversion"]
    wr = V.SCHEDULES["rating"]
    tg = 0.12

    print("THE TWO AUDITED SHEETS, AND WHAT THEY DISAGREE ABOUT")
    print("  %-42s %11s %11s" % ("", "FY2025", "FY2024"))
    for lbl, a, b in (("Operating assets", WA25, WA24),
                      ("Operating liabilities", WL25, WL24),
                      ("Net working capital", NWC25, NWC24)):
        print("  %-42s %11.0f %11.0f" % (lbl, a, b))
    print("  %-42s %11.2f %11.2f" % ("  as a multiple of revenue",
                                     NWC25 / R25, NWC24 / R24))
    print("  %-42s %11.0f %11.0f" % ("Collection period, days", DSO25, DSO24))
    print("  %-42s %11.0f %11.0f" % ("Work in progress, days of cost",
                                     DIO25, DIO24))
    print("  %-42s %11.0f %11.0f" % ("Suppliers, days of cost", DPO25, DPO24))
    print("  %-42s %10.1f%% %10.1f%%" % ("Customer advances, share of order book",
                                         100 * ADV25, 100 * ADV24))
    print()
    print("  %-42s %11.0f" % ("Working capital rose, on the balance sheet",
                              DWC_BOOK_25))
    print("  %-42s %11.0f" % ("Working capital rose, on the cash flow",
                              DWC_CASH_25))
    print("  %-42s %11.0f  (%.1f%% of revenue)"
          % ("THE WEDGE — measured, not decomposed", WEDGE_25,
             100 * WEDGE_RATIO))
    print("  %-42s %11.1f" % ("audited sheet's own rounding, carried",
                                   AUDITED_ROUNDING))
    print("  the FY2025 cash-flow statement is published in three totals only,")
    print("  so this cannot be split from disclosure. It is not split here.")
    print()
    print("CASH CONVERSION, THE COMPANY'S OWN THREE DISCLOSED YEARS")
    for k in ("FY2023", "FY2024", "FY2025"):
        print("  %-42s %10.2f%%" % (k, 100 * CONV[k]))
    print("  %-42s %10.2f%%" % ("mean, carried in Framing B", 100 * CONV_MID))
    print()

    print("PROJECTED INCOME STATEMENT — shared by both framings")
    _tbl(A, [("Units delivered", "units_delivered", "%11.0f", 1),
             ("Revenue per delivered unit, EGP mn", "rev_per_unit", *D),
             ("Revenue", "revenue", *N),
             ("Cost per delivered unit, EGP mn", "cost_per_unit", *D),
             ("Cost of revenue", "cogs", *N),
             ("Gross profit", "gross", *N),
             ("Gross margin", "gross_margin", *P),
             ("Overheads", "sga", *N),
             ("Depreciation and amortisation", "da", *N),
             ("Operating profit", "ebit", *N),
             ("Finance cost", "interest", *N),
             ("Profit before tax", "npbt", *N),
             ("Tax at 22.5%", "tax", *N),
             ("Net profit", "npat", *N),
             ("Earnings per share, EGP", "eps", *D)])

    for tag, rows, title in (("A", A, "FRAMING A — THE CYCLE HELD"),
                             ("B", B, "FRAMING B — THE CASH CONVERSION HELD")):
        print("\n" + "=" * 96)
        print(title)
        print("=" * 96)
        print("\nPROJECTED BALANCE SHEET (%s)" % tag)
        _tbl(rows, [("Trade and notes receivable", "receivables", *N),
                    ("Work in progress", "wip", *N),
                    ("Other receivables and prepayments",
                     "bs_debtors_other", *N),
                    ("Advances to suppliers", "bs_suppliers_advances", *N),
                    ("Cash and equivalents", "cash", *N),
                    ("Property and equipment", "ppe", *N),
                    ("Other assets, held at audited level",
                     "other_assets", *N),
                    ("TOTAL ASSETS", "total_assets", *N),
                    ("Customer advances", "advances", *N),
                    ("Suppliers", "suppliers", *N),
                    ("Other creditors", "bs_creditors_other", *N),
                    ("Cheques under collection", "bs_checks_undelivered", *N),
                    ("Borrowings", "debt", *N),
                    ("Other liabilities, held at audited level",
                     "other_liabs", *N),
                    ("TOTAL LIABILITIES", "total_liabilities", *N),
                    ("Shareholders' funds", "equity", *N),
                    ("TOTAL LIABILITIES AND EQUITY",
                     "total_liabs_and_equity", *N),
                    ("Balance check", "balance_check", *N)])
        print("\nTHE CYCLE THIS FRAMING IMPLIES (%s)" % tag)
        _tbl(rows, [("Collection period, days", "dso", "%11.0f", 1),
                    ("Work in progress, days of cost", "dio", "%11.0f", 1),
                    ("Suppliers, days of cost", "dpo", "%11.0f", 1),
                    ("Advances, share of order book", "adv_of_backlog", *P),
                    ("Net working capital", "net_wc", *N),
                    ("  as a multiple of revenue", "nwc_over_revenue",
                     "%11.2f", 1)])
        print("\nPROJECTED CASH FLOW (%s)" % tag)
        _tbl(rows, [("Net profit", "npat", *N),
                    ("Depreciation and amortisation", "da", *N),
                    ("Change in working capital", "d_wc", *N),
                    ("CASH FROM OPERATIONS", "cfo", *N),
                    ("  as a share of revenue", "cash_conversion", *P),
                    ("Capital expenditure", "cfi", *N),
                    ("New borrowing drawn", "drawn", *N),
                    ("CASH FROM FINANCING", "cff", *N),
                    ("Closing cash", "cash", *N),
                    ("Cumulative new borrowing", "drawn_cum", *N),
                    ("  its interest, NOT in the profit above",
                     "unmodelled_interest", *N)])
        fr = "cycle" if tag == "A" else "conversion"
        br = bridge(rows, wr, tg, fr)
        print("\nDISCOUNTED CASH FLOW — the full waterfall (%s)" % tag)
        _tbl(br["waterfall"],
             ([("Operating profit", "ebit", *N),
               ("less tax at 22.5%", "tax_on_ebit", *N),
               ("Net operating profit after tax", "nopat", *N),
               ("plus depreciation and amortisation", "da", *N),
               ("less increase in working capital", "d_wc", *N),
               ("less capital expenditure", "capex", *N)]
              if fr == "cycle" else
              [("Operating profit", "ebit", *N),
               ("Cash from operations", "cfo", *N),
               ("plus finance cost after tax", "interest_addback", *N),
               ("less capital expenditure", "capex", *N)])
             + [("FREE CASH FLOW TO THE FIRM", "fcff", *N),
                ("Discount factor at %.2f%%" % (100 * wr),
                 "discount_factor", "%11.3f", 1),
                ("PRESENT VALUE", "pv", *N)])
        if br["yields_a_value"]:
            print("\nBRIDGE TO VALUE PER SHARE (%s)" % tag)
            for lbl, v, f in (
                    ("Present value of the explicit %d years" % len(ROWS),
                     br["pv_explicit"], "%14.0f"),
                    ("Year-five free cash flow", br["terminal_flow"], "%14.0f"),
                    ("Terminal value at %.0f%% growth" % (100 * tg),
                     br["terminal_value"], "%14.0f"),
                    ("Present value beyond year five",
                     br["pv_terminal"], "%14.0f"),
                    ("ENTERPRISE VALUE", br["ev"], "%14.0f"),
                    ("less net debt", -br["net_debt"], "%14.0f"),
                    ("plus investments in associates",
                     REG["investments_assoc"], "%14.0f"),
                    ("plus investment property",
                     REG["investment_property"], "%14.0f"),
                    ("EQUITY VALUE", br["equity"], "%14.0f"),
                    ("Shares outstanding, millions", SHARES, "%14.0f"),
                    ("VALUE PER SHARE, EGP", br["per_share"], "%14.2f")):
                print(("  %-46s" + f) % (lbl, v))
            print("  %-46s%13.0f%%" % ("terminal share of enterprise value",
                                       100 * br["terminal_share"]))
        else:
            print("\nNO VALUE IS TAKEN FROM THIS FRAMING, AND WHY (%s)" % tag)
            print("  Year-five free cash flow is EGP %.0fmn — negative. A "
                  "growing-perpetuity" % br["terminal_flow"])
            print("  formula applied to a negative flow returns a large "
                  "negative number that looks")
            print("  like a valuation and is not one: it asserts the company "
                  "burns cash for ever at")
            print("  a compounding rate, which is not a forecast anybody made. "
                  "So no terminal value")
            print("  is taken and no value per share is published from this "
                  "framing. What it")
            print("  measures instead is what the growth would cost to fund:")
            print("  %-46s%14.0f" % ("Present value of the explicit %d years" % len(ROWS),
                                     br["pv_explicit"]))
            print("  %-46s%14.0f" % ("New borrowing required by 2030",
                                     br["funding_required"]))
            print("  %-46s%14.0f" % ("Its annual interest at %.2f%%, by 2030"
                                     % (100 * KD), br["funding_interest"]))
            print("  %-46s%13.0f%%" % ("that interest as a share of 2030 "
                                       "operating profit",
                                       100 * br["funding_interest_vs_ebit"]))
    return st


def verify():
    """Every check this module has to pass before its output may be used."""
    out = []
    st = build()
    for tag, rows in (("A", st["cycle"]), ("B", st["conversion"])):
        worst = max(abs(r["balance_check"]) for r in rows)
        out.append(("balance sheet foots, framing %s" % tag, worst < 1e-6,
                    "worst residual %.2e EGP mn" % worst))
        neg = [r["year"] for r in rows if r["cash"] < 0]
        out.append(("cash never negative, framing %s" % tag, not neg,
                    "negative in %s" % neg if neg else "none"))
        for r in rows:
            ta = (r["receivables"] + r["wip"] + r["bs_debtors_other"]
                  + r["bs_suppliers_advances"] + r["cash"] + r["ppe"]
                  + r["other_assets"])
            assert abs(ta - r["total_assets"]) < 1e-6, r["year"]
        out.append(("total assets is the sum of its own lines, framing %s"
                    % tag, True, "all %d years" % len(ROWS)))
    # Framing B must reproduce the published discounted cash flow exactly
    import valuation_v2 as V
    pub = V.dcf(V.lenses()["cfo"]["mid"], V.SCHEDULES["rating"])
    mine = bridge(st["conversion"], V.SCHEDULES["rating"], V.TG, "conversion")
    for k in ("pv_explicit", "pv_terminal", "ev", "equity", "per_share"):
        d = abs(pub[k] - mine[k])
        out.append(("framing B reproduces the published DCF: %s" % k,
                    d < 1e-6, "difference %.2e" % d))
    # the wedge is carried as a disclosed gap, not silently absorbed
    out.append(("the FY2025 wedge is on the gap register",
                any("wedge" in t.lower() for t in IN.GAPS.values()),
                "inputs.GAPS['cash_flow_statement_detail']"))
    return out


if __name__ == "__main__":
    st = report()
    print("\n" + "=" * 96)
    print("CHECKS")
    ok = True
    for name, passed, note in verify():
        ok &= bool(passed)
        print("  [%s] %-56s %s" % ("PASS" if passed else "FAIL", name, note))
    wr = V.SCHEDULES["rating"]
    payload = {
        "cycle_measured": {"dso_fy25": DSO25, "dso_fy24": DSO24,
                           "dio_fy25": DIO25, "dio_fy24": DIO24,
                           "dpo_fy25": DPO25, "dpo_fy24": DPO24,
                           "adv_of_backlog_fy25": ADV25,
                           "adv_of_backlog_fy24": ADV24,
                           "nwc_fy25": NWC25, "nwc_fy24": NWC24,
                           "nwc_over_revenue_fy25": NWC25 / R25,
                           "nwc_over_revenue_fy24": NWC24 / R24},
        "wedge": {"d_wc_book_fy25": DWC_BOOK_25,
                  "d_wc_cash_fy25": DWC_CASH_25, "wedge_fy25": WEDGE_25,
                  "wedge_over_revenue": WEDGE_RATIO},
        "cash_conversion": {**CONV, "mean": CONV_MID,
                            "low": CONV_LO, "high": CONV_HI},
        "statements": st,
        "dcf": {"cycle": bridge(st["cycle"], wr, 0.12, "cycle"),
                "conversion": bridge(st["conversion"], wr, 0.12,
                                     "conversion")},
        "checks": [{"name": n, "pass": bool(p), "note": t}
                   for n, p, t in verify()],
    }
    json.dump(payload, open(os.path.join(HERE, "statements.json"), "w"),
              indent=1, default=str)
    print("\n  all checks pass" if ok else "\n  CHECKS FAILED")
    sys.exit(0 if ok else 1)
