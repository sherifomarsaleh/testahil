#!/usr/bin/env python3
"""GBCO rebuild ledger [R-REBUILD-01] — the ROUTE, not only where it arrived.

[R-VCAL-01]'s promotion guard is explicit about stacking: one lever at a time, in an order
fixed in advance, and the running total looked at more than once. A REBUILD is the same
shape and was governed by nothing until this rule. PHAR took six corrections in an afternoon
and went from 55% below the price to 71% below it THROUGH +45% on the way, and the running
total was looked at once, at the end.

THIS FILE REPLAYS THE VALUATION ARITHMETIC ONLY — no Monte Carlo, no technical read — and
ASSERTS at the end that the fully-levered answer reproduces the central this study commits.
That assertion is what makes it evidence rather than a second model.

AUDIT POINT, DECLARED IN ADVANCE (before any lever was applied): after lever 4, once the
four rule-driven corrections have landed and BEFORE the price is consulted.
"""
from __future__ import annotations
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ENG = os.path.dirname(HERE)
sys.path.insert(0, ENG)
import cost_of_capital as COC
import macro_path as MP

SH = 1085.5
SPOT = 28.98                     # LATEST KNOWN price, supplied close of 3 September 2026
TAX = 0.28

# ---- the auto-leg driver build, identical to compute.py -------------------------------
def auto_rows():
    pc_v, pc_a = 56548, 52827.3 / 56548
    cvv, cva = 3404, 5956.8 / 3404
    lmv, lma = 33906, 2203.8 / 33906
    trr = 4242.8
    vol_g = [0.12, 0.14, 0.10, 0.08, 0.06]; asp_g = [0.06, 0.07, 0.07, 0.06, 0.06]
    cv_vg = [0.25, 0.18, 0.12, 0.10, 0.08]; lm_vg = [0.30, 0.20, 0.15, 0.12, 0.10]
    tr_g = [0.18, 0.15, 0.12, 0.10, 0.10]
    gpm = [0.138, 0.142, 0.145, 0.145, 0.145]; gsa = [0.073, 0.072, 0.071, 0.070, 0.070]
    oth, prov = 0.012, -0.003
    dna_pct = [0.011] * 5; capex = [3000, 2400, 2500, 2600, 2800]
    wc_pct = [0.265, 0.250, 0.235, 0.225, 0.215]
    wc_prev = 18917.0
    out = []
    for i in range(5):
        pc_v *= (1 + vol_g[i]); pc_a *= (1 + asp_g[i])
        cvv *= (1 + cv_vg[i]); cva *= (1 + 0.05)
        lmv *= (1 + lm_vg[i]); lma *= (1 + 0.05)
        trr *= (1 + tr_g[i])
        r = pc_v * pc_a + cvv * cva + lmv * lma + trr
        op = r * gpm[i] - r * gsa[i] + r * oth + r * prov
        dna = r * dna_pct[i]
        wc = r * wc_pct[i]
        out.append(op * (1 - TAX) + dna - capex[i] - (wc - wc_prev))
        wc_prev = wc
    return out


def value(wacc_ladder, wacc_terminal, tg, auto_nd, auto_nci, spot):
    f, fac = 1.0, []
    for r in wacc_ladder:
        f /= (1 + r); fac.append(f)
    rows = auto_rows()
    pv = sum(x * fac[i] for i, x in enumerate(rows))
    tv = rows[-1] * (1 + tg) / (wacc_terminal - tg) * fac[-1]
    auto_eq = pv + tv - auto_nd - auto_nci
    assoc = 0.4161 * 1400.0 * 47.5 + 390.0
    sotp_sum = auto_eq + 9500.0 + assoc
    sotp_ps = sotp_sum * 0.90 / SH
    pre_ps = sotp_sum / SH
    rel = (3300.0 / SH) * 9.5
    norm = (4200.0 / SH) * 8.5
    return 0.40 * sotp_ps + 0.15 * pre_ps + 0.20 * rel + 0.25 * norm


def build_schedule(erp_basis, erp, kd, gross_debt, build_date):
    beta = COC.BetaRecord(beta=0.8906822450333004, tier=1, source="own_stock_beta EGX30",
                          r2=0.243, se=0.204, n=251, index_file="raw_indices/EG/EGX30.csv",
                          index_asof="2026-07-22", conforming=True)
    book = COC.DebtBook(gross_debt=gross_debt, pct_local_currency=1.0,
                        currency_source="FY2025 notes 26/38, all EGP",
                        kd_local_pretax=kd, kd_source="effective rate on the borrowings that bear it",
                        effective_rates=(0.2906, 0.2653),
                        effective_rate_periods=("FY2024", "FY2025"),
                        interest_bearing_note="loans, overdrafts and bonds; deposits and payables excluded")
    return COC.schedule("EG", beta, book, market_cap=SPOT * SH, tax_rate=TAX, years=5,
                        erp_basis=erp_basis, erp_explicit=erp, build_date=build_date,
                        allow_stale_sovereign=True)


def main():
    path = MP.load("EG")
    OLD_ND, OLD_NCI = 15210.0, 800.4
    NEW_ND = 20943.0 + 1790.1 + 1333.3 + 2.3 - 9445.0
    NEW_NCI = 590.7
    levers, prev = [], None

    # L0 — as delivered: flat 22.94% for five years AND the perpetuity, typed nominal g=11.5%
    v0 = value([0.2294387] * 5, 0.2294387, 0.115, OLD_ND, OLD_NCI, 31.25)
    levers.append(("L0 · as delivered (08-07-2026 edition, restruck on the same drivers)",
                   "—", None, v0))
    prev = v0

    # L1 — the cost-of-capital schedule through the sanctioned module
    s = build_schedule("market", 0.0941, 0.2653, 42476.0, "2026-09-03")
    v1 = value(list(s.forward_wacc), s.wacc_terminal, 0.115, OLD_ND, OLD_NCI, SPOT)
    levers.append(("L1 · cost of capital rebuilt through engine/cost_of_capital.py — country "
                   "risk counted ONCE (rf* = 23.00% - 3.41%), a conforming tier-1 beta of "
                   "0.8907 in place of an assumed 1.0, Kd re-derived at 26.53% on the "
                   "borrowings that actually bear the interest, and a glide from 22.91% to a "
                   "norm-built terminal of 14.21% in place of one crisis rate for ever",
                   "[R-COC-01] · [R-COC-02] · [L-004]", prev, v1)); prev = v1

    # L2 — growth as a REAL rate on the house path
    tg = path.terminal_inflation + 0.0
    v2 = value(list(s.forward_wacc), s.wacc_terminal, tg, OLD_ND, OLD_NCI, SPOT)
    levers.append(("L2 · terminal growth stored as (real 0.0%, inflation path EG) and "
                   "recomputed to its nominal 7.00%, replacing a TYPED nominal 11.5% nobody "
                   "could falsify", "[R-MACRO-01]", prev, v2)); prev = v2

    # L3 — the terminal on a DISCLOSED useful life: REFUSED, and the reason is recorded
    levers.append(("L3 · terminal through engine/terminal_value.py on a DISCLOSED useful life "
                   "— NOT APPLIED. Both admissible routes were run and both failed: the "
                   "policy note discloses RATE RANGES only (2%-33%, a 3-to-50-year span) and "
                   "the derived identity returns 10.9-17.1 years depending on an undisclosed "
                   "land split, with per-class rates that contradict the disclosed bands. A "
                   "life this desk chose is not a disclosed life. See useful_lives.json.",
                   "[R-TERM-01] — STOP AND INFORM, SIGCM clause 8", prev, prev))

    # L4 — the bridge onto the LATEST disclosed balance sheet
    v4 = value(list(s.forward_wacc), s.wacc_terminal, tg, NEW_ND, NEW_NCI, SPOT)
    levers.append(("L4 · the enterprise-to-equity bridge moved from 31-Dec-2025 onto the "
                   "reviewed 30-June-2026 balance sheet, GB Corp's own segmented net debt for "
                   "the AUTO leg and that leg's own non-controlling interest",
                   "[R-BRIDGE-01]", prev, v4)); prev = v4

    print("GBCO REBUILD LEDGER — the levers in the ORDER APPLIED\n")
    print("  audit point declared IN ADVANCE: after L4, before the price is consulted\n")
    print("  %-4s %-11s %-11s %-9s  %s" % ("", "before", "after", "move", "rule"))
    for name, rule, a, b in levers:
        mv = "—" if a is None else "%+.1f%%" % (100 * (b / a - 1))
        print("  %-4s %-11s %-11s %-9s  %s" % (name.split(" ·")[0],
              "—" if a is None else "%.2f" % a, "%.2f" % b, mv, rule))
        print("        %s\n" % name.split("· ", 1)[1])
    print("  running total L0 -> L4:  %.2f -> %.2f   %+.1f%%" % (v0, prev, 100 * (prev / v0 - 1)))
    print("  and the individual moves do NOT sum to it: two of the four pull opposite ways —")
    print("  the discount-rate correction RAISES the value and the growth correction LOWERS it.")

    committed = json.load(open(os.path.join(HERE, "study_numbers.json")))["central"]
    assert abs(prev - committed) < 0.01, (
        "the ledger's fully-levered answer %.4f does not reproduce the committed central "
        "%.4f — a ledger that cannot be WALKED is refused [R-REBUILD-01]" % (prev, committed))
    print("\n  the last lever reaches the published central: %.4f == %.4f  OK" % (prev, committed))

    json.dump({"_rule": "[R-REBUILD-01]", "ticker": "GBCO", "date": "2026-09-07",
               "audit_point": "after L4, before the price is consulted — declared in advance",
               "published_central": committed, "published_spot": SPOT,
               "levers": [{"lever": n, "rule": r, "before": a, "after": b} for n, r, a, b in levers]},
              open(os.path.join(HERE, "rebuild_ledger.json"), "w", encoding="utf-8"),
              indent=1, ensure_ascii=False)


if __name__ == "__main__":
    main()
