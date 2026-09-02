"""Arithmetic behind GAP_REVIEW_02-09-2026.md — the ABOVE-price review [R-GAP-01 amended].

Every figure in that review that is not read straight off a filing is computed
here, from the study's own committed numbers, and printed. Nothing is typed.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
import valuation_v2 as V2, bottom_up_model as BU, cost_of_capital as COC

N = json.load(open(os.path.join(HERE, "study_numbers.json")))
R = {k: v["value"] for k, v in N["registry"].items()}
W, SCHED = N["wacc"], N["cost_of_capital_record"]
SH = BU.SHARES_MN
CENTRAL, SPOT = N["central"], N["spot"]
out = {}
p = lambda *a: print(*a)

p("=" * 76); p("PHDC GAP REVIEW — the ABOVE-price case, 02-Sep-2026"); p("=" * 76)
p("central %.4f   spot %.2f   gap %+.1f%%" % (CENTRAL, SPOT, 100 * (CENTRAL / SPOT - 1)))
out["central"], out["spot"] = CENTRAL, SPOT
out["gap"] = CENTRAL / SPOT - 1

p("\n[1] WHERE THE MOVE CAME FROM — one lens at a time, against the 30-Aug edition")
prior = N["derived"]["prior_edition_lenses"]
L = V2.lenses()
p("  30-Aug DCF base                       %8.2f" % prior["dcf_base"])
p("  02-Sep DCF base, new standard         %8.2f" % L["primary"]["value"])
p("  30-Aug weighted blend (retired)       %8.2f" % N["derived"]["prior_edition_fair"]["base"])
p("  02-Sep central = the cash-flow lens   %8.2f" % CENTRAL)
out["prior_dcf"], out["prior_blend"] = prior["dcf_base"], N["derived"]["prior_edition_fair"]["base"]

p("\n[2] DECOMPOSITION — each change alone, from the 30-Aug construction")
S = V2.SCHEDULES["rating"]
mid = L["cfo"]["mid"]
flat = COC.flat_schedule(W["wacc_rating"], len(BU.build()["rows"]))
steps = [
    ("30-Aug construction: flat rate, 5-year window, g=12%", None),
]
p("  the 30-Aug construction cannot be rebuilt exactly here — its five-year window")
p("  no longer exists in the model — so the decomposition is run the other way, by")
p("  removing one change at a time from the CURRENT build:")
cur = V2.dcf(mid, S)["per_share"]
flat_now = V2.dcf(mid, flat)["per_share"]
p("    current build                                    %8.2f" % cur)
p("    with a FLAT rate instead of the schedule         %8.2f   (%+.2f)"
  % (flat_now, flat_now - cur))
out["current"], out["flat_rate_instead"] = cur, flat_now
tv_share = V2.dcf(mid, S)["terminal_share"]
p("    terminal share of enterprise value               %7.1f%%" % (100 * tv_share))
out["terminal_share"] = tv_share

p("\n[3] HORIZON — does the window run until growth has converged?")
rows = BU.build()["rows"]
g = [rows[i]["revenue"] / rows[i - 1]["revenue"] - 1 for i in range(1, len(rows))]
p("  explicit years %d; revenue growth %.1f%% falling to %.1f%%"
  % (len(rows), 100 * g[0], 100 * g[-1]))
p("  terminal growth %.2f%%; gap at the boundary %.2fpp"
  % (100 * V2.TG, 100 * abs(g[-1] - V2.TG)))
out["years"], out["growth_end"], out["tg"] = len(rows), g[-1], V2.TG

p("\n[4] DISCOUNT RATE — the ladder, and cash charged once")
p("  " + "  ".join("%.2f%%" % (100 * w) for w in SCHED["forward_wacc"]))
p("  terminal %.2f%%   equity weight %.3f (below one, so no negative debt weight)"
  % (100 * SCHED["wacc_terminal"], SCHED["weight_equity"]))
p("  net debt deducted once in the bridge, at %.1f; weights stand on GROSS debt"
  % N["derived"]["net_debt_bridge"])
out["wacc_exp"], out["wacc_term"] = SCHED["wacc_exp"], SCHED["wacc_terminal"]

p("\n[5] TERMINAL — growth against the inflation inside the terminal rate")
p("  terminal risk-free %.2f%% = terminal inflation %.2f%% + real convention %.2f%%"
  % (100 * SCHED["rf_terminal"], 100 * V2.PATH.terminal_inflation,
     100 * V2.PATH.real_rate_convention))
p("  terminal growth %.2f%% = the same inflation, zero real. Real growth assumed: %.2f%%"
  % (100 * V2.TG, 100 * V2.TERMINAL_REAL_GROWTH))

p("\n[6] BALANCE SHEET — the bridge stands on the latest disclosed sheet")
p("  %s; net debt %.1f, associates %.1f, investment property %.1f, minority %.2f/sh"
  % (N["derived"]["bridge_balance_sheet"], N["derived"]["net_debt_bridge"],
     N["balance_sheet_1q26"]["investments_assoc"]["value"],
     N["balance_sheet_1q26"]["investment_property"]["value"],
     N["cases"]["base"]["nci_deduction"] / SH))

p("\n[7] CLAIMS AGAINST THE RECORD — every quantity the study asserts, recomputed")
d = N["cases"]["base"]
checks = [
    ("units delivered 2026 implied by the reported quarter",
     rows[0]["units_delivered"], "implied, not disclosed"),
    ("gross margin held at the average of FY2025 and 1Q2026",
     rows[0]["gross_margin"], "%.4f vs (%.4f + %.4f)/2 = %.4f"
     % (rows[0]["gross_margin"], N["derived"]["gross_margin_fy25"],
        N["derived"]["gross_margin_1q26"],
        (N["derived"]["gross_margin_fy25"] + N["derived"]["gross_margin_1q26"]) / 2)),
    ("deliveries in the last year against the first",
     rows[-1]["units_delivered"] / rows[0]["units_delivered"], "x over %d years" % len(rows)),
]
for lbl, val, note in checks:
    p("  %-58s %10.4f   %s" % (lbl, val, note))
out["deliveries_multiple"] = rows[-1]["units_delivered"] / rows[0]["units_delivered"]

p("\n[8] MULTIPLE CROSS-CHECK — what the central implies")
eps25 = R["npat_mi_fy25"] / SH
eps26e = rows[0]["npat"] / SH
ebitda25 = R["npbt_fy25"] + R["finance_cost_fy25"] + R["da_fy25"]
nd = N["derived"]["net_debt_bridge"]
for lbl, px in (("central", CENTRAL), ("spot", SPOT),
                ("the multiple cross-check", N["lenses"][1][2])):
    eqv = px * SH
    ev = eqv + nd - N["balance_sheet_1q26"]["investments_assoc"]["value"] \
        - N["balance_sheet_1q26"]["investment_property"]["value"]
    p("  %-24s %6.2f | mcap %9.0f | EV %9.0f | P/E25 %5.2fx | P/E26e %5.2fx | "
      "EV/EBITDA25 %5.2fx | P/B %4.2fx | mcap/backlog %4.1f%%"
      % (lbl, px, eqv, ev, px / eps25, px / eps26e, ev / ebitda25,
         px / (N["balance_sheet_1q26"]["equity_parent"]["value"] / SH),
         100 * eqv / R["backlog_1q26"]))
out["eps25"], out["eps26e"], out["ebitda25"] = eps25, eps26e, ebitda25
out["pe25_central"] = CENTRAL / eps25
out["mcap_over_backlog_central"] = CENTRAL * SH / R["backlog_1q26"]

json.dump(out, open(os.path.join(HERE, "gap_review_calcs_above.json"), "w"), indent=1)
p("\nwrote gap_review_calcs_above.json")
