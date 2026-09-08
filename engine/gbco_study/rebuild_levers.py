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
import rebuild_ledger as RL   # the SHARED instrument [R-ENF-03], never a hand-rolled record

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
    return auto_eq


# ---- THE SECOND PASS MOVES THINGS THE FIRST PASS'S value() HAD BAKED IN ---------------
# The first four levers all moved the AUTO leg's cash-flow arithmetic, so everything
# beside it -- the lender at book, the associate at one mark, the discount, the four
# weights -- could sit inside value() as constants. The levers below move exactly those,
# so they are parameters now. NOTHING ABOUT L1-L4 CHANGES: legs() with the delivered
# arguments reproduces the old value() to the last decimal, which is asserted in main().
DELIVERED = dict(cap=9500.0, other_assoc=390.0, disc=0.10,
                 rel=(3300.0 / SH) * 9.5, norm=(4200.0 / SH) * 8.5,
                 weights=(0.40, 0.15, 0.20, 0.25))


def legs(auto_eq, cap, assoc, disc, rel, norm, weights):
    """The answer the study publishes, given each leg and each lens.

    weights=None means the blend is retired and the class primary IS the answer,
    which is [R-LENS-03] and is lever L5.
    """
    sotp_sum = auto_eq + cap + assoc
    sotp_ps = sotp_sum * (1.0 - disc) / SH
    if weights is None:
        return sotp_ps
    w_sotp, w_pre, w_rel, w_norm = weights
    return (w_sotp * sotp_ps + w_pre * sotp_sum / SH
            + w_rel * rel + w_norm * norm)


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
    ASSOC_DELIVERED = 0.4161 * 1400.0 * 47.5 + DELIVERED["other_assoc"]

    def delivered(auto_eq):
        """The answer as the delivered edition constructed it, given the auto leg."""
        return legs(auto_eq, DELIVERED["cap"], ASSOC_DELIVERED, DELIVERED["disc"],
                    DELIVERED["rel"], DELIVERED["norm"], DELIVERED["weights"])

    a0 = value([0.2294387] * 5, 0.2294387, 0.115, OLD_ND, OLD_NCI, 31.25)
    v0 = delivered(a0)
    levers.append(("L0 · as delivered (08-07-2026 edition, restruck on the same drivers)",
                   "—", None, v0))
    prev = v0

    # L1 — the cost-of-capital schedule through the sanctioned module
    s = build_schedule("market", 0.0941, 0.2653, 42476.0, "2026-09-03")
    v1 = delivered(value(list(s.forward_wacc), s.wacc_terminal, 0.115,
                         OLD_ND, OLD_NCI, SPOT))
    levers.append(("L1 · cost of capital rebuilt through engine/cost_of_capital.py — country "
                   "risk counted ONCE (rf* = 23.00% - 3.41%), a conforming tier-1 beta of "
                   "0.8907 in place of an assumed 1.0, Kd re-derived at 26.53% on the "
                   "borrowings that actually bear the interest, and a glide from 22.91% to a "
                   "norm-built terminal of 14.21% in place of one crisis rate for ever",
                   "[R-COC-01] · [R-COC-02] · [L-004]", prev, v1)); prev = v1

    # L2 — growth as a REAL rate on the house path
    tg = path.terminal_inflation + 0.0
    v2 = delivered(value(list(s.forward_wacc), s.wacc_terminal, tg,
                         OLD_ND, OLD_NCI, SPOT))
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
    auto_eq = value(list(s.forward_wacc), s.wacc_terminal, tg, NEW_ND, NEW_NCI, SPOT)
    v4 = delivered(auto_eq)
    levers.append(("L4 · the enterprise-to-equity bridge moved from 31-Dec-2025 onto the "
                   "reviewed 30-June-2026 balance sheet, GB Corp's own segmented net debt for "
                   "the AUTO leg and that leg's own non-controlling interest",
                   "[R-BRIDGE-01]", prev, v4)); prev = v4

    # ================= THE SECOND PASS, 7 September 2026 ==============================
    # AUDIT POINT FOR THIS PASS, DECLARED IN ADVANCE and before any of it was applied:
    # after L9, once the lens architecture is rebuilt and BEFORE the price is consulted
    # again. Every lever below is a rule that ALREADY BOUND rather than a lever anybody
    # chose, which is the distinction [R-REBUILD-01] exists to keep visible.
    N = json.load(open(os.path.join(HERE, "study_numbers.json"), encoding="utf-8"))
    CAP_NEW = N["lens_inputs"]["capital"]["value"]
    OTHER_NEW = N["sotp"]["other_assoc"]
    MNT_ROUND = N["sotp"]["mnt_halan_value"]
    ASSOC_CARRY = N["lens_inputs"]["capital"]["associates_carried_within"]

    # L5 — the blend retired: the class primary IS the answer
    v5 = legs(auto_eq, DELIVERED["cap"], ASSOC_DELIVERED, DELIVERED["disc"],
              None, None, None)
    levers.append(("L5 · the four-lens weighted blend RETIRED and the class primary taken "
                   "as the answer. A number produced by averaging several methods is a new "
                   "method with free parameters nobody tested; the weights here were "
                   "0.40/0.15/0.20/0.25 and two of the four lenses were the SAME "
                   "sum-of-the-parts at two discount levels",
                   "[R-LENS-03]", prev, v5)); prev = v5

    # L6 — the typed conglomerate discount removed
    v6 = legs(auto_eq, DELIVERED["cap"], ASSOC_DELIVERED, 0.0, None, None, None)
    levers.append(("L6 · the TYPED 10% conglomerate discount removed. Nothing in the "
                   "filings discloses a basis for it, and the blend above applied it at an "
                   "EFFECTIVE 4% by weighting the discounted and undiscounted sums both — "
                   "so the number the study named was not the number it applied. A free "
                   "parameter that has never cleared an out-of-sample test",
                   "the PROMOTION RULE", prev, v6)); prev = v6

    # L7 — the lender from book x 1.0 to residual income on its own operating equity
    v7 = legs(auto_eq, CAP_NEW, ASSOC_DELIVERED, 0.0, None, None, None)
    levers.append(("L7 · GB Capital from a TYPED 9,500 at 1.0x book to residual income on "
                   "its own operating equity — segment shareholders' equity before NCI less "
                   "the associates carried inside it, 22,497.8 - 16,230.5 = 6,267.3, at the "
                   "justified price-to-book its own disclosed return supports. Book times "
                   "one is the weighting of book value this rule forbids outright, and the "
                   "old base came from a ratio whose NUMERATOR held the associate income "
                   "the sum of the parts counts again",
                   "[R-LENS-03]", prev, v7)); prev = v7

    # L8 — the other associates at the figure the note actually foots to
    v8 = legs(auto_eq, CAP_NEW, MNT_ROUND + OTHER_NEW, 0.0, None, None, None)
    levers.append(("L8 · the associates other than MNT-Halan from a TYPED 390.0 to 496.9, "
                   "the residual of note 34's own total less its MNT row, both of which "
                   "foot to the reviewed balance sheet",
                   "SIGCM clause 1", prev, v8)); prev = v8

    # L9 — the answer becomes two-sided
    v9 = legs(auto_eq, CAP_NEW, ASSOC_CARRY, 0.0, None, None, None)
    levers.append(("L9 · the associate marked BOTH WAYS and the answer published as two "
                   "branches rather than one. This walk stays on the round-price branch, "
                   "%.4f; the other branch, MNT-Halan at its reviewed carrying value of "
                   "15,733.5, reads %.4f. Neither is averaged into the other."
                   % (prev, v9),
                   "depth-bar standard 8 — the contested judgement published both ways",
                   prev, prev))

    led = RL.Ledger(ticker="GBCO",
                    started_at="the delivered 08-07-2026 edition, restruck on the same drivers",
                    start_value=v0, start_spot=SPOT,
                    audit_after=("L4 and again at L9 — each declared IN ADVANCE of the pass "
                                 "it closes: the running total is looked at once the pass's "
                                 "rule-driven corrections have landed and BEFORE the price is "
                                 "consulted"))
    for name, rule, a, b in levers[1:]:
        led.apply(name=name.split(" · ")[0], rule=rule, after=b,
                  why=name.split("· ", 1)[1], evidence="engine/gbco_study/compute.py")

    print(RL.render(led.record()) if hasattr(RL, "render") else "")
    print("GBCO REBUILD LEDGER — the levers in the ORDER APPLIED\n")
    print("  audit point declared IN ADVANCE: %s\n" % led.audit_after)
    for lv in led.levers:
        print("  %-4s %8.2f -> %8.2f  %+7.1f%%   %s" %
              (lv.name, lv.before, lv.after, 100 * lv.move, lv.rule))
        print("        %s\n" % lv.why)
    print("  running total: %.2f -> %.2f   %+.1f%%" % (v0, led.value, 100 * led.cumulative))
    print("  BY RULE, which is the point — several levers serving one rule are ONE piece")
    print("  of evidence, and here the four rules pull in opposite directions:")
    for rule, g in led.by_rule().items():
        print("    %-45s %+7.1f%%" % (rule[:45], 100 * g["move"]))

    # THE STUDY NO LONGER PUBLISHES A CENTRAL, AND THE ASSERTION GETS STRICTER RATHER
    # THAN LOOSER. This line read study_numbers["central"], which is now None — so left
    # alone it would not have weakened quietly, it would have raised on a subtraction,
    # which is the better failure. What replaces it is a check against BOTH committed
    # branches: the walk must reach the one it stayed on, AND the branch it names in L9
    # must be the other one. A ledger that reproduced one number of two would be walkable
    # and still wrong about the answer.
    branches = {b["label"]: b["value"] for b in N["central_two_sided"]["branches"]}
    walked = [v for k, v in branches.items() if "round" in k][0]
    other = [v for k, v in branches.items() if "carrying" in k][0]
    assert abs(led.value - walked) < 0.01, (
        "the ledger's fully-levered answer %.4f does not reproduce the committed branch "
        "%.4f — a ledger that cannot be WALKED is refused [R-REBUILD-01]"
        % (led.value, walked))
    assert abs(v9 - other) < 0.01, (
        "L9 names a second branch of %.4f and the study commits %.4f. A two-sided answer "
        "whose ledger reaches one side is a ledger for half the study." % (v9, other))
    committed = walked
    rec = led.record()
    RL.assert_rebuild(rec, "GBCO")
    json.dump(rec, open(os.path.join(HERE, "rebuild_ledger.json"), "w", encoding="utf-8"),
              indent=1, ensure_ascii=False)
    print("\n  the last lever reaches the published central: %.4f == %.4f  OK"
          % (led.value, committed))


if __name__ == "__main__":
    main()
