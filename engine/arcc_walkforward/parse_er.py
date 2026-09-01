"""Physical drivers from ARCC's OWN quarterly and annual EARNINGS RELEASES.

The release is the second half of what [L-008] requires: a period is not
researched until BOTH its statements and its results release are in.  The
statements carry no tonne; the release carries the tonnes, the split between
local and export, the market share, and the company's own cash-cost measure —
the operating anchors the accounts never state.

The releases print one table with a fixed shape — metric, unit, then the
quarter's figure, the comparable quarter, the variance, the full year, the
comparable full year, the variance — so the FULL-YEAR column is read by
POSITION IN THAT TABLE, not by pattern-matching a number out of prose.  Where a
release prints only three figures (a first-quarter release has no full year),
the full-year fields are absent and the row is skipped rather than guessed.
"""
import os, re, sys, json

IR = "/tmp/claude-0/-home-user-testahil/82898002-da86-5df7-8203-457959546ece/scratchpad/irtext"

METRICS = {
    "acc domestic sales volume": "local_kt",
    "acc exports volume": "export_kt",
    "acc total volumes": "total_kt",
    "local market share": "market_share",
    "market share": "market_share",
    "revenues": "revenue_mn",
    "total revenues": "revenue_mn",
    "rev/ton": "rev_per_t",
    "cash cost": "cash_cost_mn",
    "cash cost/ton": "cost_per_t",
    "ebitda": "ebitda_mn",
    "ebitda/ton": "ebitda_per_t",
    "net profit": "net_profit_mn",
    "cash gross profit": "cash_gp_mn",
    "local revenues": "local_revenue_mn",
    "export revenues": "export_revenue_mn",
    "clinker export volume": "clinker_export_kt",
    "cement exports volume": "cement_export_kt",
    "local sales volume": "local_kt",
    "total export": "export_kt",
}

NUM = re.compile(r"^\(?-?[\d,]+(?:\.\d+)?\)?%?$")

# Annual releases, with the fiscal year each reports.  Quarterly releases are
# read too but only their FULL-YEAR-TO-DATE column would be a partial year, so
# they are excluded here: a nine-month figure entering an annual panel is the
# same error class as a half annualised.
ANNUAL_ER = {
    "FY-2015-Earnings-Release": "FY2015",
    "FY-2016-Earnings-Release": "FY2016",
    "4Q-2017-Earnings-Release": "FY2017",
    "4Q_2018_Earnings_Release": "FY2018",
    "4Q_2019_EARNINGS_RELEASEPDF": "FY2019",
    "4Q_2020_Earnings_Release": "FY2020",
    "FY_2021_Earnings_Release": "FY2021",
    "FY_2022_Earnings_Release": "FY2022",
    "ACC_4Q_2023_Earnings_Release": "FY2023",
    "ACC_FY2024_Earnings_Release": "FY2024",
}


def val(s):
    s = s.strip()
    neg = s.startswith("(") and s.endswith(")")
    pct = s.endswith("%")
    d = re.sub(r"[^\d.]", "", s)
    if not d or d == ".":
        return None
    v = float(d)
    if neg:
        v = -v
    return v / 100.0 if pct else v


def table(doc):
    """{metric: {"fy": v, "fy_prior": v, "q": v, "q_prior": v}} from one release."""
    fn = os.path.join(IR, doc + ".txt")
    if not os.path.exists(fn):
        return None
    lines = [l.strip() for l in open(fn, encoding="utf-8", errors="replace").read().splitlines()]
    out = {}
    for i, l in enumerate(lines):
        key = METRICS.get(l.lower().strip())
        if not key:
            continue
        j = i + 1
        # the unit line, then the numeric run
        if j < len(lines) and lines[j] and not NUM.match(lines[j]):
            unit = lines[j]; j += 1
        else:
            unit = None
        nums = []
        while j < len(lines) and len(nums) < 6:
            if not lines[j]:
                j += 1; continue
            if NUM.match(lines[j]):
                nums.append(val(lines[j])); j += 1
            else:
                break
        if len(nums) >= 6:
            out.setdefault(key, {"unit": unit, "q": nums[0], "q_prior": nums[1],
                                 "fy": nums[3], "fy_prior": nums[4]})
    return out


def harvest():
    rows, missing = [], []
    for doc, fy in ANNUAL_ER.items():
        t = table(doc)
        if not t:
            missing.append(doc); continue
        prior = "FY%d" % (int(fy[2:]) - 1)
        for k, v in t.items():
            rows.append({"metric": k, "fy": fy, "value": v["fy"], "unit": v["unit"],
                         "doc": doc, "column": "current"})
            if v.get("fy_prior") is not None:
                rows.append({"metric": k, "fy": prior, "value": v["fy_prior"],
                             "unit": v["unit"], "doc": doc, "column": "comparative"})
    return rows, missing


if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(json.dumps(table(sys.argv[1]), indent=1))
    else:
        rows, missing = harvest()
        print("rows", len(rows), "missing releases", missing)
        by = {}
        for r in rows:
            by.setdefault(r["metric"], {}).setdefault(r["fy"], []).append(r["value"])
        for m in sorted(by):
            print("%-18s %s" % (m, " ".join("%s=%s" % (k[2:], sorted(set(v)))
                                            for k, v in sorted(by[m].items()))))
