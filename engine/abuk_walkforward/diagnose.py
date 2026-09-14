"""ABUK fundamental walk-forward — diagnosis.

Three things: the macro/company split with its own zero-by-construction check,
the decomposition of the revenue and net-profit errors into their drivers, and
the projected-versus-actual income statement for EVERY origin.
"""
import json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
ORIGINS = ["FY2019", "FY2020", "FY2021", "FY2022", "FY2023", "FY2024"]


def mae(scores, key, d):
    return scores[key]["drivers"][d]["mae"]


def bias(scores, key, d):
    return scores[key]["drivers"][d]["bias"]


def split(scores):
    """|e| under the model, under actual macro, under full foresight.

    macro share   = (MAE_model - MAE_macro_perfect) / MAE_model
    company share = (MAE_macro_perfect - MAE_foresight) / MAE_model
    residual      = MAE_foresight / MAE_model  (what perfect foresight still
                    cannot explain — the model's own specification)
    """
    out = {}
    for d in ("vol_proxy", "rev", "cogs", "gp", "sell", "admin", "nonop",
              "pbt", "np"):
        m = mae(scores, "model", d)
        mp = mae(scores, "macro_perfect", d)
        fs = mae(scores, "foresight", d)
        if not m:
            continue
        out[d] = dict(mae_model=m, mae_macro_actual=mp, mae_foresight=fs,
                      macro_share=(m - mp) / m,
                      company_share=(mp - fs) / m,
                      spec_residual=fs / m)
    return out


def sidebyside(panel, proj):
    lines = ["# ABUK — projected versus actual income statement, EVERY origin",
             "",
             "INTERNAL. EGP millions. `model` is the pre-registered ground-up "
             "build at that origin; `actual` is what the company reported.",
             ""]
    for o in ORIGINS:
        lines += ["## Origin %s" % o, "",
                  "| target | h | revenue model | revenue actual | gross profit model | "
                  "gross profit actual | net profit model | net profit actual | "
                  "net profit log err |",
                  "|---|---|---:|---:|---:|---:|---:|---:|---:|"]
        for t, row in sorted(proj["model"][o].items()):
            a = panel["years"][t]
            e = math.log(row["np"] / a["np"]) if row["np"] > 0 and a["np"] > 0 else None
            lines.append("| %s | %d | %s | %s | %s | %s | %s | %s | %s |" % (
                t, row["h"], f"{row['rev']/1e6:,.0f}", f"{a['rev']/1e6:,.0f}",
                f"{row['gp']/1e6:,.0f}", f"{a['gp']/1e6:,.0f}",
                f"{row['np']/1e6:,.0f}", f"{a['np']/1e6:,.0f}",
                "n/a" if e is None else "%+.3f" % e))
        lines.append("")
    return "\n".join(lines)


def main():
    panel = json.load(open(os.path.join(HERE, "panel.json")))
    proj = json.load(open(os.path.join(HERE, "projections.json")))
    scores = json.load(open(os.path.join(HERE, "scores.json")))
    sp = split(scores)
    zero_check = abs(sp["vol_proxy"]["macro_share"]) < 1e-9
    doc = {"split": sp,
           "zero_by_construction_check": {
               "driver": "vol_proxy",
               "macro_share": sp["vol_proxy"]["macro_share"],
               "passes": zero_check,
               "why": ("D1 carries no inflation, FX or urea term, so substituting "
                       "the actual macro path must leave its error untouched. A "
                       "non-zero share here would mean the split is wired wrong "
                       "and the whole diagnosis is void.")},
           "era_stability": {}}
    for d, s in scores["model"]["drivers"].items():
        pre = s["by_era"]["pre"]
        post = s["by_era"]["post"]
        if not pre or not post:
            continue
        doc["era_stability"][d] = dict(
            pre_bias=pre["bias"], post_bias=post["bias"],
            same_sign=(pre["bias"] > 0) == (post["bias"] > 0),
            verdict=("bias holds its sign across eras"
                     if (pre["bias"] > 0) == (post["bias"] > 0)
                     else "SIGN CHANGES BETWEEN ERAS — this is instability, not a "
                          "bias, and it is reported rather than corrected for"))
    json.dump(doc, open(os.path.join(HERE, "diagnostics.json"), "w"), indent=1,
              sort_keys=True, default=float)
    open(os.path.join(HERE, "abuk_IS_projected_vs_actual_all_origins.md"),
         "w").write(sidebyside(panel, proj))
    return doc


if __name__ == "__main__":
    d = main()
    print("%-10s %10s %10s %10s %10s" % ("driver", "MAE model", "macro%", "company%", "spec%"))
    for k, s in d["split"].items():
        print("%-10s %10.3f %9.0f%% %9.0f%% %9.0f%%" % (
            k, s["mae_model"], 100 * s["macro_share"],
            100 * s["company_share"], 100 * s["spec_residual"]))
    z = d["zero_by_construction_check"]
    print("\nzero-by-construction check on the volume driver: macro share %.2e -> %s"
          % (z["macro_share"], "PASS" if z["passes"] else "FAIL"))
    print("\nera stability (bias pre FY2020-21 / post FY2022-25):")
    for k, s in d["era_stability"].items():
        print("  %-10s pre %+.3f  post %+.3f  -> %s" % (
            k, s["pre_bias"], s["post_bias"],
            "same sign" if s["same_sign"] else "SIGN CHANGES"))
