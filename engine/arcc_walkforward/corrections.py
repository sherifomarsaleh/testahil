"""ARCC walk-forward — corrections, tested under BOTH clauses of §5.

Clause one is arithmetic and is computed here: expanding window, half strength,
applied only where the bias holds its sign across both eras and survives the
bootstrap at all three block lengths, then the aggregates are rebuilt from the
adjusted drivers and tested adjusted-against-raw by origin.

Clause two is a JUDGEMENT and it is signed rather than computed: does the
correction match how that driver class is built across the market's book? It is
not a formality. On PHDC it is what caught a finance-cost "bias" that was
arithmetic wearing the costume of evidence ([L-002], [L-003]).

THE GENERAL RULE THIS MODULE ENFORCES: a correction factor is honest when the
model is right and reality is awkward; when the model is WRONG, a correction
hides it. So a driver whose rule scores WORSE THAN FREEZE is never corrected —
it is reported as mis-specified, because multiplying a wrong rule by a constant
leaves a wrong rule.
"""
import os, sys, json, math

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bottom_up as B
import score as S
import diagnose as D

HALF = 0.5


def expanding_correction(rows, driver, origin):
    """The half-strength correction available AT `origin`: estimated only on
    cells whose target had already resolved before that origin's own year."""
    y = int(origin[2:])
    errs = [r["e"][driver] for r in rows
            if r["e"][driver] is not None and int(r["target"][2:]) < y]
    if len(errs) < 3:
        return None, len(errs)
    return math.exp(-HALF * (sum(errs) / len(errs))), len(errs)


def test(driver, rows):
    """Adjusted against raw, by origin, on the cells that had a correction."""
    per_origin, raw_abs, adj_abs = [], [], []
    for o in B.ORIGINS:
        k, n = expanding_correction(rows, driver, o)
        if k is None:
            continue
        cells = [r for r in rows if r["origin"] == o and r["e"][driver] is not None]
        if not cells:
            continue
        raw = [abs(r["e"][driver]) for r in cells]
        adj = [abs(r["e"][driver] + math.log(k)) for r in cells]
        per_origin.append({"origin": o, "k": k, "estimated_on": n, "n_cells": len(cells),
                           "mae_raw": sum(raw) / len(raw), "mae_adj": sum(adj) / len(adj),
                           "improves": sum(adj) < sum(raw)})
        raw_abs += raw
        adj_abs += adj
    if not raw_abs:
        return None
    return {"per_origin": per_origin,
            "mae_raw": sum(raw_abs) / len(raw_abs),
            "mae_adj": sum(adj_abs) / len(adj_abs),
            "improves_overall": sum(adj_abs) < sum(raw_abs),
            "origins_improved": sum(1 for p in per_origin if p["improves"]),
            "origins_tested": len(per_origin)}


# ---------------------------------------------------------------------------
# CLAUSE TWO — signed, not computed. Every candidate that passes clause one is
# ruled on here, and the reason is recorded whether it passes or fails.
# ---------------------------------------------------------------------------
CLAUSE_TWO = {
 "vol_local": dict(passes=False, reason=(
    "THE RULE IS WRONG, NOT MERELY BIASED. Local volume driven by Egyptian population "
    "growth scores WORSE THAN FREEZE (skill -0.166): holding last year's tonnage would "
    "have beaten it at every horizon. ARCC's local volume FELL through the window "
    "(3,944kt in FY2019 to 2,618kt in FY2024) while the population rose, because the "
    "company was reallocating clinker to export, not because demand grew. A multiplier "
    "on a rule that points the wrong way leaves a rule that points the wrong way "
    "([L-002]). The finding is a specification defect and no correction may hide it.")),
 "vol_export": dict(passes=False, reason=(
    "SPECIFICATION, NOT CALIBRATION. Exports went from 50kt in FY2016 to 2,436kt in "
    "FY2024 — a channel that did not exist becoming half the book. A persistence rule "
    "against a structural build-out under-forecasts by construction, and the correction "
    "that would fix the average would be a growth assumption smuggled in as a constant.")),
 "price_local": dict(passes=False, reason=(
    "THIS IS ONE FINDING ABOUT THE INFLATION PATH, NOT SIX ABOUT SIX DRIVERS. Local "
    "price, raw materials per tonne, transport per tonne, overheads per tonne and G&A "
    "are ALL under-forecast, all by the same mechanism: the origin's last published "
    "inflation rate understated what Egypt actually ran. Correcting the PRICE leg alone "
    "would manufacture a margin trend out of the correction, which is [L-009] and "
    "[L-110] in a new costume; correcting every leg together is not a driver correction "
    "at all, it is an inflation forecast, and no forecast of a macro variable is "
    "permitted at an origin. WATCH FLAG.")),
 "price_export": dict(passes=False, reason=(
    "Same finding as price_local on the currency leg, and worse conditioned: the bias is "
    "-0.531 in the pre-2022 era and -0.032 after it, so essentially the whole of it is "
    "one regime. The macro split attributes 80.5% of this miss to the exchange-rate path "
    "itself — the highest macro share of any driver here — which makes it a statement "
    "about Egypt's currency, not about how this company prices a tonne of clinker.")),
 "services": dict(passes=False, reason=(
    "Transportation services are a pass-through billed alongside export tonnage, and "
    "exports quadrupled. The bias tracks the export build-out (vol_export) and correcting "
    "it would double-count the same structural error twice.")),
 "raw_per_t": dict(passes=False, reason=(
    "Part of the same inflation-path finding as price_local, and the class rule cuts "
    "against it directly: [L-110] says a globally traded input follows the world price "
    "and the exchange rate, so a domestic-inflation correction applied to a line that is "
    "half imported coal would be the exact substitution that lesson was adopted to stop. "
    "WATCH FLAG.")),
 "transport_per_t": dict(passes=False, reason=(
    "The largest cost bias in the run (-0.675) and entirely structural: transport per "
    "tonne went from 19 EGP in FY2018 to 157 in FY2025 as the mix swung to export "
    "clinker moving to port. That is a mix effect, not an escalation error, and the fix "
    "is to drive transport off EXPORT tonnage rather than total tonnage.")),
 "transport": dict(passes=False, reason="Same finding as transport_per_t, at the total rather than the unit level."),
 "overhead_per_t": dict(passes=False, reason=(
    "Part of the same inflation-path finding. Its skill against freeze is the highest of "
    "any cost driver (+0.470), so the RULE is working; what it misses is the size of the "
    "inflation, which is macro. WATCH FLAG.")),
 "mfg_dep": dict(passes=True, reason=(
    "THE ONE CANDIDATE THAT SURVIVES BOTH CLAUSES. Depreciation held flat under-forecasts "
    "by 5.9% on average, the sign holds in both eras, and it is robust at all three block "
    "lengths. It matches the book: every other study in this repository builds "
    "depreciation off a PP&E roll-forward and therefore grows it with the capital "
    "programme, so a small upward adjustment to a flat-held depreciation line is "
    "consistent with how the driver class is built everywhere else rather than a quirk of "
    "this name. It is also the SMALLEST correction in the candidate set, which is what a "
    "genuine calibration adjustment ought to look like.")),
 "provisions": dict(passes=False, reason=(
    "The bias is -1.409 pooled and -1.850 against -0.014 by era — one era carries "
    "essentially all of it, and the level is a management estimate that jumped from "
    "2,245,000 in FY2018 to 111,939,885 in FY2022 on a single legal matter. A correction "
    "on a line that moves fifty-fold on one event is fitting to an event.")),
 "interest_income": dict(passes=False, reason=(
    "THE LARGEST BIAS IN THE RUN (-1.641) AND A PURE SPECIFICATION DEFECT. Interest "
    "income went from 4.9mn in FY2018 to 226.3mn in FY2025 as ARCC built a net cash "
    "position and Egyptian deposit rates went to 27%. Held flat, it cannot track either. "
    "The fix is to drive it off the cash balance at the deposit rate — which is how every "
    "other study in the book builds it — not to multiply a flat line by a constant.")),
}


def run():
    rows, out = S.run()
    _, diag = D.run()
    results = []
    for c in diag["correction_candidates"]:
        if not c["clears_bar"]:
            continue
        d = c["driver"]
        t = test(d, rows)
        two = CLAUSE_TWO.get(d, dict(passes=False, reason="not ruled on"))
        results.append({
            "driver": d, "bias": c["bias"], "era1": c["era1"], "era2": c["era2"],
            "skill_vs_freeze": c["skill_vs_freeze"], "equals_freeze": c["equals_freeze"],
            "clause_one": t,
            "clause_one_passes": bool(t and t["improves_overall"]),
            "clause_two_passes": two["passes"], "clause_two_reason": two["reason"],
            "disposition": ("ADOPTED" if (t and t["improves_overall"] and two["passes"])
                            else "WATCH FLAG"),
        })
    return results


if __name__ == "__main__":
    res = run()
    json.dump(res, open(os.path.join(HERE, "corrections_log.json"), "w"), indent=1, default=str)
    print("Candidates clearing the pre-registered bar: %d" % len(res))
    print()
    print("%-18s %8s %9s %9s %8s %8s  %s" %
          ("driver", "bias", "MAE raw", "MAE adj", "clause1", "clause2", "disposition"))
    for r in res:
        t = r["clause_one"]
        print("%-18s %+8.3f %9.3f %9.3f %8s %8s  %s" %
              (r["driver"], r["bias"], t["mae_raw"] if t else float("nan"),
               t["mae_adj"] if t else float("nan"),
               "pass" if r["clause_one_passes"] else "fail",
               "pass" if r["clause_two_passes"] else "fail", r["disposition"]))
    print()
    ad = [r for r in res if r["disposition"] == "ADOPTED"]
    print("ADOPTED: %s" % (", ".join(r["driver"] for r in ad) or "none"))
    print("WATCH FLAGS: %d" % (len(res) - len(ad)))
