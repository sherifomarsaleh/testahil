"""Assemble the PHDC walk-forward panel: value / source / date / tier.

Tiers, as the prompt defines them:
  A  the company's own audited or reviewed statements and its own IR documents
  B  exchange or regulator filing
  C  credible third party

Reported historicals are tier A throughout, per SIGCM clause 1. Only the
exogenous macro series — Egyptian CPI, EGP/USD, urban population — are tier C,
and they are exogenous inputs to the forecast, never the company's own reported
numbers.

Nothing is interpolated. A year that cannot be sourced for a field simply has
no record for that field, and the coverage table says so.
"""
import os, json, urllib.request, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
WB = "https://api.worldbank.org/v2/country/EGY/indicator/%s?format=json&per_page=80&date=2008:2025"
MACRO = {"cpi_pct": "FP.CPI.TOTL.ZG", "egp_usd": "PA.NUS.FCRF",
         "urban_pop": "SP.URB.TOTL", "population": "SP.POP.TOTL"}


def rec(value, source, date, tier, note=None, derived=None):
    r = {"value": value, "source": source, "date": date, "tier": tier}
    if note:
        r["note"] = note
    if derived:
        r["derived"] = derived
    return r


def fetch_macro(cache=os.path.join(HERE, "macro_eg.json")):
    if os.path.exists(cache):
        return json.load(open(cache))
    out = {}
    for name, ind in MACRO.items():
        with urllib.request.urlopen(WB % ind, timeout=90) as r:
            d = json.loads(r.read().decode())
        out[name] = {int(x["date"]): x["value"] for x in d[1] if x["value"] is not None}
        out[name + "_source"] = ("World Bank WDI indicator %s "
                                 "(api.worldbank.org, Egypt, Arab Rep.)" % ind)
    out["_retrieved"] = datetime.date.today().isoformat()
    json.dump(out, open(cache, "w"), indent=1)
    return out


IR_URL = "https://ir.palmhillsdevelopments.com/en-us/financial/resultcenter"


def npbt_of(d):
    v = d.get("is.npbt")
    return v["value"] if v else None


def build():
    import parse_kpi
    fs = json.load(open(os.path.join(HERE, "fs_parsed.json")))
    series, narr = parse_kpi.build()
    macro = fetch_macro()
    panel = {}

    def yr(y):
        return panel.setdefault(str(y), {})

    # ---- reported statement lines, from each year's OWN filing (tier A) -----
    for ystr, r in fs.items():
        y = int(ystr)
        if r.get("_unresolved"):
            continue
        stem = r["_stem"]
        src = "PHD consolidated financial statements FY%d (%s), via %s" % (y, stem, IR_URL)
        for k, v in r.items():
            if not k.startswith(("is.", "bs.")) or k.endswith("._src"):
                continue
            if v[0] is None:
                continue
            yr(y)[k] = rec(round(v[0], 4), src, "%d-12-31" % y, "A",
                           note="EGP million; parse route %s/%s, checked against the "
                                "statement's own footing" % (r["_route"], r["_gutter"]))

    # ---- FY2022: filed in Arabic only, taken from FY2023's comparative ------
    r23 = fs.get("2023")
    if r23 and not r23.get("_unresolved"):
        src = ("PHD consolidated financial statements FY2023, comparative column "
               "(31 Dec 2022), via %s — the FY2022 statement itself is published "
               "in Arabic only" % IR_URL)
        for k, v in r23.items():
            if not k.startswith(("is.", "bs.")) or k.endswith("._src"):
                continue
            if v[1] is None:
                continue
            yr(2022)[k] = rec(round(v[1], 4), src, "2022-12-31", "A",
                              note="EGP million; comparative column of the following "
                                   "year's filing")

    # ---- FY2014: pre-dates the IR archive; from FY2015's comparative -------
    r15 = fs.get("2015")
    if r15 and not r15.get("_unresolved"):
        src = ("PHD consolidated financial statements FY2015, comparative column "
               "(31 Dec 2014), via %s — the IR result centre's earliest filing "
               "is 1Q2015" % IR_URL)
        for k, v in r15.items():
            if not k.startswith(("is.", "bs.")) or k.endswith("._src"):
                continue
            if v[1] is None:
                continue
            yr(2014)[k] = rec(round(v[1], 4), src, "2014-12-31", "A",
                              note="EGP million; comparative column of the following "
                                   "year's filing")

    # ---- operating drivers from the releases (tier A) ----------------------
    for field in ("new_sales", "units_sold"):
        for y, readings in series[field].items():
            if not readings:
                continue
            # point-in-time: the FIRST release to report the year is what an
            # origin at that year could have seen. Later readings are kept
            # alongside so a restatement is visible rather than overwritten.
            first = min(readings)
            yr(y)[field] = rec(readings[first],
                               "PHD earnings release %s, embedded chart series, via %s"
                               % (first, IR_URL),
                               "%s-12-31" % first[:4], "A",
                               note="EGP million" if field == "new_sales" else "units")
            if len(set(readings.values())) > 1:
                yr(y)[field + "_restated"] = rec(
                    readings[max(readings)],
                    "PHD earnings release %s, same chart series restated" % max(readings),
                    "%s-12-31" % max(readings)[:4], "A",
                    note="later reading of the same year; the origin uses the "
                         "as-first-reported figure above")

    for fy, fields in narr.items():
        for field, d in fields.items():
            yr(fy)[field] = rec(d["value"],
                                "PHD %d full-year earnings release, quoted: \"%s\""
                                % (fy, d["sentence"]),
                                "%d-12-31" % fy, "A",
                                note="EGP million" if field != "units_delivered" else "units")

    # ---- earnings-release statement summary: cross-check, and gap fill -----
    # The release is the company's own document, so it is tier A like the
    # filing. Its role here is secondary: it CHECKS the statement wherever both
    # report a line, and it FILLS a line the scanned statement would not yield.
    # Its unit (EGP thousand vs million) is not assumed — it is fixed against
    # the statement's own revenue for the same year, which is a figure already
    # verified by the statement's footing. A release whose revenue matches
    # neither scale is not used at all, and says so.
    import parse_er
    reg = json.load(open(os.path.join(HERE, "ir_register.json")))
    checks = []
    for r in reg:
        if r["quarter"] != "Q4" or not r["year"]:
            continue
        y = r["year"]
        er = parse_er.parse_release("%d_Q4_ER" % y, y, "Q4")
        if not er or not er.get("is.revenue"):
            continue
        def calibrate(er_key, stmt_keys):
            """Fix one table's unit against a line the filing already verified."""
            ev = er.get(er_key)
            if not ev or ev[0] is None:
                return None
            for sk in stmt_keys:
                sv = yr(y).get(sk)
                if not sv:
                    continue
                for cand in (1.0, 0.001, 1000.0):
                    if abs(abs(ev[0]) * cand - abs(sv["value"])) <= \
                            max(2.0, 0.01 * abs(sv["value"])):
                        return cand
            return None

        scale_is = calibrate("is.revenue", ["is.revenue"])
        scale_bs = calibrate("bs.total_current_assets",
                             ["bs.total_current_assets"]) or \
            calibrate("bs.total_equity", ["bs.total_equity"])
        if scale_is is None:
            checks.append({"year": y, "status": "release income statement not used "
                           "— revenue reconciles to the filing at no scale",
                           "release_revenue": er["is.revenue"][0],
                           "statement_revenue": (yr(y).get("is.revenue") or {}).get("value")})
        src = ("PHD FY%d full-year earnings release (%d_Q4_ER), via %s"
               % (y, y, IR_URL))
        for k, v in er.items():
            if not k.startswith(("is.", "bs.", "cf.")) or k.endswith("._label"):
                continue
            if v[0] is None:
                continue
            sc = scale_is if k.startswith("is.") else scale_bs
            if sc is None:
                continue
            val = round(v[0] * sc, 4)
            have = yr(y).get(k)
            if have is None:
                yr(y)[k] = rec(val, src, "%d-12-31" % y, "A",
                               note="EGP million; from the company's own results "
                                    "release because the filed statement's line did "
                                    "not resolve")
            else:
                # The release shows deductions in brackets and the filing shows
                # them positive, so the two agree on magnitude and differ on
                # sign by convention. Compare magnitudes.
                d = abs(abs(have["value"]) - abs(val))
                tol = max(1.0, 0.01 * abs(have["value"]))
                if d > tol:
                    checks.append({"year": y, "field": k,
                                   "statement": have["value"], "release": val,
                                   "abs_diff": round(d, 3),
                                   "status": "filing and release disagree"})
    json.dump(checks, open(os.path.join(HERE, "source_crosschecks.json"), "w"), indent=1)

    # ---- reconcile the profit lines by triangulation ------------------------
    # The bottom of these income statements wraps across three physical lines,
    # and on the scanned years the wrap leaves fragments that a label match can
    # attach to the wrong figures. Rather than keep tightening label patterns,
    # the three lines are reconciled against each other and against the
    # company's own release: net profit after minority interest must equal net
    # profit before minority interest less the minority share, and the release
    # states it directly. Where two of the three agree, that value stands and
    # the disagreement is recorded; where they do not, the field is dropped
    # rather than guessed.
    import parse_er
    recon = []
    for y in range(2014, 2026):
        d = yr(y)
        pre = d.get("is.npat_pre_nci")
        nci = d.get("is.nci")
        got = d.get("is.npat_mi")
        er = parse_er.parse_release("%d_Q4_ER" % y, y, "Q4") or {}
        erv = None
        if er.get("is.npat_mi") and er["is.npat_mi"][0] is not None:
            raw = er["is.npat_mi"][0]
            stmt_rev = (d.get("is.revenue") or {}).get("value")
            for sc in (1.0, 0.001, 1000.0):
                if stmt_rev and 0 < abs(raw * sc) <= 1.5 * stmt_rev:
                    erv = round(raw * sc, 4)
                    break
        # On two scanned years the wrap put NET PROFIT BEFORE MINORITY INTEREST
        # and NET PROFIT BEFORE TAX on the same figures. They cannot be equal —
        # the tax charge sits between them — so where they are, the pre-minority
        # line is rebuilt from the two lines that did reconcile.
        if pre and npbt_of(d) is not None and abs(pre["value"] - npbt_of(d)) < 1e-6:
            if got and nci:
                pre = rec(round(got["value"] + abs(nci["value"]), 4),
                          "DERIVED = net profit after minority interest plus the "
                          "minority share, both from the FY%d filing" % y,
                          "%d-12-31" % y, "A",
                          derived="is.npat_mi + is.nci",
                          note="EGP million; the filed line itself did not resolve "
                               "separately from profit before tax on this scan")
                d["is.npat_pre_nci"] = pre
        derived = None
        if pre and nci:
            derived = round(pre["value"] - abs(nci["value"]), 4)
        cands = {"parsed": got["value"] if got else None,
                 "derived": derived, "release": erv}
        vals = [v for v in cands.values() if v is not None]
        agree = None
        for v in vals:
            if sum(1 for w in vals if abs(w - v) <= max(1.0, 0.01 * abs(v))) >= 2:
                agree = v
                break
        if agree is not None:
            d["is.npat_mi"] = rec(agree,
                                  "PHD FY%d consolidated statements and full-year "
                                  "earnings release, reconciled" % y,
                                  "%d-12-31" % y, "A",
                                  note="EGP million; net profit after tax and minority "
                                       "interest, agreed by at least two of "
                                       "{filed line, filed line less minority share, "
                                       "results release}")
        elif "is.npat_mi" in d:
            del d["is.npat_mi"]
        recon.append({"year": y, "candidates": cands, "adopted": agree})
        # total tax charge, as an identity off two reconciled lines
        npbt = d.get("is.npbt")
        if npbt and pre and abs(npbt["value"]) > 0:
            d["is.tax_total"] = rec(round(npbt["value"] - pre["value"], 4),
                                    "DERIVED = net profit before income tax and "
                                    "minority interest less net profit before "
                                    "minority interest, both from the FY%d filing" % y,
                                    "%d-12-31" % y, "A",
                                    derived="is.npbt - is.npat_pre_nci")
    json.dump(recon, open(os.path.join(HERE, "profit_reconciliation.json"), "w"), indent=1)

    # ---- drop figures the series itself contradicts -------------------------
    # An OCR'd flow line can lose leading digits and come back near zero while
    # still looking like a number. A cost line that collapses to under 2% of the
    # prior year's, on a year whose revenue grew, is not a real figure — it is a
    # truncated one. Those are REMOVED and listed, never carried: a hole is
    # visible downstream, a plausible-looking wrong number is not.
    dropped = []
    for y in range(2015, 2026):
        for k in ("is.sga", "is.finance_cost", "is.cogs", "is.admin_depr"):
            cur, prev = yr(y).get(k), yr(y - 1).get(k)
            if not cur or not prev or abs(prev["value"]) < 100:
                continue
            if abs(cur["value"]) < 0.02 * abs(prev["value"]):
                dropped.append({"year": y, "field": k, "value": cur["value"],
                                "prior_year": prev["value"],
                                "reason": "under 2% of the prior year — reads as a "
                                          "truncated scan, not a reported figure"})
                del yr(y)[k]
    json.dump(dropped, open(os.path.join(HERE, "dropped_figures.json"), "w"), indent=1)

    # ---- exogenous macro (tier C) ------------------------------------------
    for name in ("cpi_pct", "egp_usd", "urban_pop", "population"):
        for y, v in macro[name].items():
            yr(y)["macro." + name] = rec(v, macro[name + "_source"],
                                         macro["_retrieved"], "C",
                                         note="exogenous; forecast input only, never a "
                                              "source for the company's own reported "
                                              "figures")
    return panel


if __name__ == "__main__":
    p = build()
    json.dump(p, open(os.path.join(HERE, "panel.json"), "w"), indent=1)
    yrs = sorted(int(y) for y in p)
    print("panel years: %d-%d (%d)" % (yrs[0], yrs[-1], len(yrs)))
    key = ["is.revenue", "is.gross_profit", "is.npbt", "new_sales", "units_sold",
           "units_delivered", "construction_spend", "backlog", "bs.total_current_assets"]
    hdr = "year  " + "".join("%-14s" % k.split(".")[-1][:13] for k in key)
    print(hdr)
    for y in yrs:
        row = "%-6d" % y
        for k in key:
            v = p[str(y)].get(k)
            row += "%-14s" % ("-" if v is None else ("%.1f" % v["value"]))
        print(row)
    n = sum(len(v) for v in p.values())
    tiers = {}
    for v in p.values():
        for r in v.values():
            tiers[r["tier"]] = tiers.get(r["tier"], 0) + 1
    print("\nrecords: %d   by tier: %s" % (n, tiers))
