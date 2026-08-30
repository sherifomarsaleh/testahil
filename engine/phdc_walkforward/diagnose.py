"""Decompose the PHDC walk-forward errors and lay out each origin side by side.

Two things §4 of the prompt asks for that a headline table cannot answer:
which driver each aggregate's miss actually comes from, and what the projected
income statement looked like against the real one at every origin.

The decomposition is a one-at-a-time substitution: replace ONE projected driver
with its realised value, rebuild the aggregate from the same arithmetic the
projection used, and measure how much of the absolute log error disappears.
That attributes the miss to a driver without assuming the drivers are
independent — the residual after all substitutions is reported too, and it is
the part the bridge itself gets wrong.
"""
import json, os, math
import bottom_up as B
import score as S

HERE = os.path.dirname(os.path.abspath(__file__))


def npat_from(gross, sga, da, interest, tax_rate):
    if None in (gross, sga, interest):
        return None
    npbt = gross - sga - (da or 0.0) - interest
    return npbt * (1 - tax_rate) if npbt > 0 else npbt


def decompose(panel):
    """How much of the net-profit miss each driver accounts for."""
    contrib = {k: [] for k in ("is.gross_profit", "is.sga", "is.admin_depr",
                               "is.finance_cost")}
    residual = []
    for o in S.ORIGINS:
        proj = B.project(panel, o)
        tax_rate = 0.225 if o >= 2015 else 0.25
        for h in B.HORIZONS:
            t = o + h
            if t > S.LAST_ACTUAL:
                continue
            p = proj[h]
            act = {k: B.actual(panel, t, k) for k in contrib}
            base = npat_from(p["is.gross_profit"], p["is.sga"],
                             p["is.admin_depr"], p["is.finance_cost"], tax_rate)
            true = B.actual(panel, t, "is.npat_mi")
            if base is None or true is None or base <= 0 or true <= 0:
                continue
            e0 = abs(math.log(base / true))
            for k in contrib:
                if act[k] is None:
                    continue
                sub = dict(p)
                sub[k] = act[k]
                v = npat_from(sub["is.gross_profit"], sub["is.sga"],
                              sub["is.admin_depr"], sub["is.finance_cost"], tax_rate)
                if v is None or v <= 0:
                    continue
                e1 = abs(math.log(v / true))
                contrib[k].append(e0 - e1)
            allsub = npat_from(act["is.gross_profit"], act["is.sga"],
                               act["is.admin_depr"], act["is.finance_cost"], tax_rate)
            if allsub and allsub > 0:
                residual.append(abs(math.log(allsub / true)))
    out = {}
    for k, v in contrib.items():
        if v:
            out[k] = {"n": len(v), "mean_error_removed": round(sum(v) / len(v), 4)}
    out["_residual_with_every_driver_correct"] = {
        "n": len(residual),
        "mean_abs_log_error": round(sum(residual) / len(residual), 4) if residual else None}
    return out


IS_ROWS = [("Revenue", "is.revenue"), ("Cost of revenue", "is.cogs"),
           ("Gross profit", "is.gross_profit"), ("SG&A", "is.sga"),
           ("D&A", "is.admin_depr"), ("Finance cost", "is.finance_cost"),
           ("Profit before tax", "is.npbt"),
           ("Net profit after tax and MI", "is.npat_mi")]


def side_by_side(panel, path):
    lines = ["# PHDC — projected versus actual income statement, every origin",
             "",
             "Each block is one origin. The projection uses only fiscal years up to",
             "that origin, on the inflation path knowable there (`as-known`). EGP",
             "million. `err` is the log error, ln(projected/actual).", ""]
    for o in S.ORIGINS:
        proj = B.project(panel, o)
        lines.append("## Origin FY%d" % o)
        lines.append("")
        hs = [h for h in B.HORIZONS if o + h <= S.LAST_ACTUAL]
        if not hs:
            continue
        head = "| line | " + " | ".join("FY%d (h%d)" % (o + h, h) for h in hs) + " |"
        lines.append(head)
        lines.append("|" + "---|" * (len(hs) + 1))
        for label, f in IS_ROWS:
            cells = []
            for h in hs:
                p = proj[h].get(f)
                a = B.actual(panel, o + h, f)
                if p is None or a is None:
                    cells.append("–")
                elif p > 0 and a > 0:
                    cells.append("%.0f / %.0f · %+.2f" % (p, a, math.log(p / a)))
                else:
                    cells.append("%.0f / %.0f" % (p, a))
            lines.append("| %s | %s |" % (label, " | ".join(cells)))
        lines.append("")
        lines.append("*projected / actual · log error*")
        lines.append("")
    open(path, "w").write("\n".join(lines))
    return len(lines)


def one_offs(panel):
    """One-offs the company itself attributed, and the record with them classified."""
    return [
        {"year": 2013, "item": "Village Mall disposal",
         "amount_revenue": 240.0, "amount_profit": 52.0,
         "source": "FY2015 earnings release footnote — the company excludes it "
                   "from its own 2013 revenue and profit chart",
         "treatment": "scored on the company's ex-disposal basis"},
        {"year": 2020, "item": "COVID-19",
         "evidence": "handovers fell to 633 units from 964; construction spend "
                     "EGP 1.5bn, the lowest of the window",
         "treatment": "retained in the sample, flagged; record reported with and "
                      "without"},
        {"year": 2024, "item": "Taaleem 32.6%, Macor +10% to 69.5%, Novotel October 20%",
         "source": "FY2024 earnings release",
         "treatment": "perimeter change; no restated pre-acquisition series is "
                      "published, so no chain factor exists and FY2024-25 "
                      "aggregate errors carry the flag"},
    ]


def guidance_ledger():
    """Management's own targets against outcome, as the releases state them."""
    import glob, re
    TXT = os.environ.get("PHDC_TXT",
        "/tmp/claude-0/-home-user-testahil/2283e95e-66db-5f22-bba6-0db833f32495/scratchpad/phdc_src/text")
    pats = [r"[^.]{0,160}target of ([\d,]+) units[^.]{0,80}\.",
            r"[^.]{0,160}targets? of EGP\s?([\d.,]+)\s?(billion|bn|million|mn)[^.]{0,80}\.",
            r"[^.]{0,160}(?:surpassing|exceeding|beating|below|missing) (?:its )?"
            r"(?:previously announced )?(?:FY\d{4} )?target[^.]{0,100}\."]
    out = []
    for path in sorted(glob.glob(os.path.join(TXT, "*_Q4_ER.txt"))):
        fy = int(os.path.basename(path)[:4])
        t = re.sub(r"\s+", " ", open(path, encoding="utf-8").read())
        for p in pats:
            for m in re.finditer(p, t):
                s = m.group(0).strip()
                if len(s) > 20 and not any(x["sentence"] == s for x in out):
                    out.append({"fy": fy, "sentence": s[:280]})
    return out


if __name__ == "__main__":
    panel = B.load()
    d = decompose(panel)
    print("NET-PROFIT ERROR DECOMPOSITION — mean absolute log error removed")
    print("by replacing ONE projected driver with its realised value\n")
    for k, v in sorted(d.items(), key=lambda kv: -(kv[1].get("mean_error_removed") or -9)):
        if k.startswith("_"):
            continue
        print("  %-20s n=%-3d removes %+.3f of %.3f" %
              (k, v["n"], v["mean_error_removed"],
               S.summarise(S.cells(panel), "is.npat_mi")["mae"]))
    r = d["_residual_with_every_driver_correct"]
    print("\n  with EVERY driver replaced by its actual, the bridge still misses by "
          "%.3f (n=%d)" % (r["mean_abs_log_error"], r["n"]))
    n = side_by_side(panel, os.path.join(HERE, "phdc_IS_projected_vs_actual_all_origins.md"))
    g = guidance_ledger()
    json.dump({"decomposition": d, "one_offs": one_offs(panel), "guidance": g},
              open(os.path.join(HERE, "diagnostics.json"), "w"), indent=1)
    print("\nper-origin side-by-side written (%d lines); guidance statements found: %d"
          % (n, len(g)))


# --------------------------------------------------------------------------
# Guidance ledger. Two different things get called "guidance" in these
# releases and they must not be pooled: a target the release RETROSPECTIVELY
# says it beat, and a FORWARD target for a year not yet run. Only the second is
# a forecast. Scoring them together would flatter the record, because a target
# is only quoted retrospectively when it was beaten.
GUIDANCE = [
    {"for_fy": 2016, "metric": "units_delivered", "target": 1800, "kind": "referenced",
     "quoted_in": "2016_Q4_ER"},
    {"for_fy": 2017, "metric": "units_delivered", "target": 1600, "kind": "referenced",
     "quoted_in": "2017_Q4_ER"},
    {"for_fy": 2018, "metric": "units_delivered", "target": 1500, "kind": "referenced",
     "quoted_in": "2018_Q4_ER"},
    {"for_fy": 2019, "metric": "units_delivered", "target": 1350, "kind": "forward",
     "quoted_in": "2018_Q4_ER"},
    {"for_fy": 2021, "metric": "units_delivered", "target": 1450, "kind": "forward",
     "quoted_in": "2020_Q4_ER"},
    {"for_fy": 2020, "metric": "new_sales", "target": 12000.0, "kind": "referenced",
     "quoted_in": "2020_Q4_ER"},
]


def guidance_scored(panel):
    import math
    out = []
    for g in GUIDANCE:
        a = B.actual(panel, g["for_fy"], g["metric"])
        row = dict(g, actual=a)
        if a and a > 0 and g["target"] > 0:
            row["e"] = round(math.log(g["target"] / a), 4)
            row["outcome"] = "beaten" if a > g["target"] else "missed"
            row["gap_pct"] = round(100 * (a / g["target"] - 1), 1)
        out.append(row)
    fwd = [r["e"] for r in out if r.get("kind") == "forward" and "e" in r]
    ref = [r["e"] for r in out if r.get("kind") == "referenced" and "e" in r]
    return {"rows": out,
            "forward_bias_log": round(sum(fwd) / len(fwd), 4) if fwd else None,
            "forward_n": len(fwd),
            "referenced_bias_log": round(sum(ref) / len(ref), 4) if ref else None,
            "referenced_n": len(ref)}
