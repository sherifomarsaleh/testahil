"""EGCH (KIMA) walk-forward — corrections, estimated on an expanding window and tested
under BOTH clauses (PRE_REGISTRATION §7).

A correction on driver d at origin o is −½ × mean(e_d) over the cells RESOLVED before o
(target year ≤ o), applied only where (i) the sign has held in every era resolved so far,
(ii) the moving-block bootstrap over the resolved origins keeps the sign at every block
length available, and (iii) no reset is in force. RESETS: at the plant replacement (the
first origin standing in FY2020 or later discards everything resolved before it) and
after any resolved driver error beyond its own two-sigma. Aggregates are rebuilt from
adjusted drivers and adjusted-vs-raw is reported by origin. Clause 2 — consistency with
how the driver class is built across the market's book — is applied to whatever passes.

The roles of the two samples: the rolling record estimates; the non-overlapping origins
{FY2012, FY2017, FY2022} confirm.
"""
import os, sys, json, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import panel as P
import bottom_up as B
import score as S

CORRECTABLE = ["revenue", "cost_of_sales", "selling", "admin", "debit_interest"]
CONFIRM_ORIGINS = ["FY2012", "FY2017", "FY2022"]
BREAK_ORIGIN = 2020

BOOK_CONVENTION = {
    "revenue": ("Revenue is volume x realisation on a disclosed unit in every ground-up study; a "
                "multiplier on the revenue LEVEL would be unique to this name."),
    "cost_of_sales": ("Each physical cost class escalates on its own driver (gas on its administered "
                      "dollar price through FX, labour on CPI) everywhere in the book — never a blended "
                      "index and never a multiplier on the total (L-009)."),
    "selling": "Freight is cost per tonne shipped, escalated on domestic CPI, across the book.",
    "admin": "Overheads are a fixed base escalated on CPI across the book.",
    "debit_interest": ("Interest is a disclosed rate on the borrowings that bear it, in the currency "
                       "they are borrowed in, across the book. A multiplier on the charge would hide "
                       "a rate or a currency that was read wrongly (L-002)."),
}


def resolved_before(rows, origin, driver):
    """log errors on cells whose target has been reported by the origin date."""
    return [r for r in rows if r["e"][driver] is not None and B.y(r["target"]) <= B.y(origin)]


def era_signs(cells):
    by = {}
    for r in cells:
        by.setdefault(r["era"], []).append(r["e"][r["_d"]])
    return {e: (sum(v) / len(v)) for e, v in by.items()}


def boot_same_sign(cells, seed=42, nboot=1000):
    by_o = {}
    for r in cells:
        by_o.setdefault(r["origin"], []).append(r["e"][r["_d"]])
    have = sorted(by_o)
    out = {}
    for L in (2, 3, 4):
        if len(have) < L + 1:
            continue
        rnd = random.Random(seed + L)
        starts = list(range(0, len(have) - L + 1))
        stats = []
        for _ in range(nboot):
            vals = []
            while len(vals) < len(have):
                s = rnd.choice(starts)
                for o in have[s:s + L]:
                    vals.extend(by_o[o])
            stats.append(sum(vals) / len(vals))
        stats.sort()
        lo, hi = stats[int(0.05 * len(stats))], stats[int(0.95 * len(stats)) - 1]
        out[L] = (lo > 0 and hi > 0) or (lo < 0 and hi < 0)
    return out


def main():
    rows = S.build_cells()
    log = []
    for o in B.ORIGINS:
        entry = {"origin": o, "era": S.ERA[o], "corrections": {}, "confirm_origin": o in CONFIRM_ORIGINS}
        for d in CORRECTABLE:
            cells = [dict(r, _d=d) for r in resolved_before(rows, o, d)]
            # reset at the plant replacement: an origin in or after FY2020 sees only cells whose
            # ORIGIN is in or after FY2020 (nothing from the old plant informs the new one)
            if B.y(o) >= BREAK_ORIGIN:
                cells = [c for c in cells if B.y(c["origin"]) >= BREAK_ORIGIN]
            rec = {"n_resolved": len(cells)}
            if len(cells) < 5:
                rec["applied"] = 0.0
                rec["why"] = "fewer than five resolved cells"
                entry["corrections"][d] = rec
                continue
            errs = [c["e"][d] for c in cells]
            mean = sum(errs) / len(errs)
            sd = (sum((x - mean) ** 2 for x in errs) / max(len(errs) - 1, 1)) ** 0.5
            # reset after a resolved error beyond its own two sigma (the most recent resolved cell)
            latest = max(cells, key=lambda c: (B.y(c["target"]), c["h"]))
            shock = abs(latest["e"][d] - mean) > 2 * sd if sd > 0 else False
            es = era_signs(cells)
            era_ok = len(set(1 if v > 0 else -1 for v in es.values())) == 1
            bs = boot_same_sign(cells)
            boot_ok = bool(bs) and all(bs.values())
            rec.update(mean_resolved=mean, sd_resolved=sd, era_signs=es, era_stable=era_ok,
                       bootstrap_same_sign=bs, bootstrap_ok=boot_ok, two_sigma_shock=shock)
            if era_ok and boot_ok and not shock:
                rec["applied"] = -0.5 * mean
                rec["why"] = "clause 1 passed on the resolved record"
            else:
                rec["applied"] = 0.0
                rec["why"] = ("era sign unstable" if not era_ok else "bootstrap sign unstable" if not boot_ok
                              else "reset: two-sigma shock in the latest resolved cell")
            entry["corrections"][d] = rec
        # rebuild the aggregates at this origin with the adjusted drivers and score vs raw
        adj_vs_raw = {}
        for h in B.HORIZONS:
            t = B.fyname(B.y(o) + h)
            if t not in P.IS or B.y(t) > 2025:
                continue
            p = B.project(o, h)
            a = P.actual(t)
            q = dict(p)
            for d, rec in entry["corrections"].items():
                if rec.get("applied") and q.get(d) is not None:
                    q[d] = q[d] * math.exp(rec["applied"])
            if q.get("pbt") is not None:
                q["gross_profit"] = q["revenue"] - q["cost_of_sales"]
                q["pbt"] = (q["revenue"] - q["cost_of_sales"] - q["selling"] - q["admin"] - q["provisions"]
                            + q["other_bucket"] + q["reval_gain"] + q["fx"] + q["investment_income"]
                            + q["credit_interest"] - q["debit_interest"])
                q["tax_current"] = P.TAX_REGIME[o] * max(q["pbt"], 0)
                q["net"] = q["pbt"] - q["tax_current"]
            cell = {}
            for k in ("revenue", "cost_of_sales", "gross_profit", "pbt", "net"):
                cell[k] = {"raw": S.logerr(p.get(k), a.get(k)), "adjusted": S.logerr(q.get(k), a.get(k))}
            adj_vs_raw[str(h)] = cell
        entry["adjusted_vs_raw"] = adj_vs_raw
        # per-driver outcome: change in MAE across this origin's matured cells
        for d, rec in entry["corrections"].items():
            if rec.get("applied"):
                pairs = [(c[d]["raw"], c[d]["adjusted"]) for c in adj_vs_raw.values()
                         if d in c and c[d]["raw"] is not None and c[d]["adjusted"] is not None] if d in ("revenue", "cost_of_sales") else []
                if d in ("selling", "admin", "debit_interest"):
                    pairs = []
                    for h in B.HORIZONS:
                        t = B.fyname(B.y(o) + h)
                        if t not in P.IS or B.y(t) > 2025:
                            continue
                        p, a = B.project(o, h), P.actual(t)
                        raw = S.logerr(p.get(d), a.get(d))
                        adj = S.logerr(p.get(d) * math.exp(rec["applied"]) if p.get(d) else None, a.get(d))
                        if raw is not None and adj is not None:
                            pairs.append((raw, adj))
                if pairs:
                    rec["outcome_mae_change"] = (sum(abs(b) for _, b in pairs) - sum(abs(a) for a, _ in pairs)) / len(pairs)
                    rec["outcome_n"] = len(pairs)
        log.append(entry)

    # summary per driver: how often applied, and did it help on the confirm origins
    summary = {}
    for d in CORRECTABLE:
        applied = [e for e in log if e["corrections"][d].get("applied")]
        helped = [e["corrections"][d]["outcome_mae_change"] for e in applied if "outcome_mae_change" in e["corrections"][d]]
        conf = [e for e in applied if e["confirm_origin"]]
        summary[d] = {"origins_applied": [e["origin"] for e in applied], "n_applied": len(applied),
                      "mean_mae_change_when_applied": (sum(helped) / len(helped)) if helped else None,
                      "helped_count": sum(1 for x in helped if x < 0), "hurt_count": sum(1 for x in helped if x > 0),
                      "confirm_origins_applied": [e["origin"] for e in conf],
                      "clause2_convention": BOOK_CONVENTION[d]}
        # disposition
        if not applied:
            summary[d]["disposition"] = "no correction estimated — clause 1 never passed on the expanding record"
        else:
            hc, hu = summary[d]["helped_count"], summary[d]["hurt_count"]
            summary[d]["disposition"] = ("WATCH FLAG — clause 1 passed at %d origin(s) (helped %d / hurt %d); NOT promoted: "
                                         "clause 2 — %s" % (len(applied), hc, hu, BOOK_CONVENTION[d]))
    out = {"policy": ("Expanding window, half strength, sign held across resolved eras and bootstrap blocks, "
                      "reset at the plant replacement and after a two-sigma shock. Everything that passes clause 1 "
                      "is tested against clause 2 and, failing it, filed as a WATCH FLAG — recorded, graded at the "
                      "next update, acted on by nobody."),
           "log": log, "summary": summary, "adopted": []}
    json.dump(out, open(os.path.join(HERE, "corrections_log.json"), "w"), indent=1, default=str)
    return out


if __name__ == "__main__":
    o = main()
    print("CORRECTIONS — " + o["policy"] + "\n")
    for d, s in o["summary"].items():
        print("%-16s applied at %-40s helped %d hurt %d mean dMAE %s\n   -> %s" % (
            d, ",".join(s["origins_applied"]) or "none", s["helped_count"], s["hurt_count"],
            ("%+.3f" % s["mean_mae_change_when_applied"]) if s["mean_mae_change_when_applied"] is not None else "n/a",
            s["disposition"][:160]))
    print("\nper origin (applied log-corrections):")
    for e in o["log"]:
        ap = {d: round(r["applied"], 3) for d, r in e["corrections"].items() if r.get("applied")}
        print("  %s %s %s" % (e["origin"], "confirm" if e["confirm_origin"] else "       ", ap or "-"))
