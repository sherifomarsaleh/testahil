#!/usr/bin/env python3
"""EMFD — operating KPIs from the company's own results releases.

[R-FCAL-01] §1 and L-008: a period is not researched until both its statements
AND its results release are in. The statements carry revenue and cost; only the
release carries the DELIVERED UNIT COUNT and the CONTRACTED SALES VALUE, and for
this class of company those are the drivers — revenue is units delivered times
price per unit delivered, and nothing in the financial statements discloses
either half.

Extracted mechanically from the release text, then cross-checked against the
audited statements: a release that quotes a revenue figure the statements do not
carry is a release for a different basis, and the mismatch must surface here
rather than inside a driver.

Output: kpi.json
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import extract as E                                    # noqa: E402

# "Delivered 935 units", "Delivered units reached 1,386 units", "Delivered 819
# units". The count is small and unseparated, so it is matched on its own and
# never through the money pattern.
UNITS = [
    re.compile(r"Deliver(?:ed|ing)\s+(?:units\s+reached\s+)?([\d,]{3,6})\s+units", re.I),
    re.compile(r"Deliver(?:ed|ing)\s+([\d,]{3,6})\s+units", re.I),
    re.compile(r"deliveries\s+reaching\s+([\d,]{3,6})\s+units", re.I),
]
# "Gross sales reached EGP 11.97 billion", "Committed net sales of EGP 8.6
# billion", "achieving EGP 11,973 million"
SALES = [
    ("gross_sales", re.compile(r"[Gg]ross sales(?:\s+reached|\s+of)?\s+EGP\s*"
                               r"([\d.,]+)\s*(billion|million|bn|mn)", re.I)),
    ("net_sales", re.compile(r"(?:[Cc]ommitted\s+)?net sales(?:\s+came in at|"
                             r"\s+reached|\s+of)?\s+EGP\s*([\d.,]+)\s*"
                             r"(billion|million|bn|mn)", re.I)),
]
SCALE = {"billion": 1e9, "bn": 1e9, "million": 1e6, "mn": 1e6}


def flat(path):
    import pymupdf
    doc = pymupdf.open(path)
    out = []
    for i in range(doc.page_count):
        t, route, rot = E.page(path, i)
        out.append(t)
    return " ".join(" ".join("\n".join(out).split()).split()), route


def main():
    reg = json.load(open(os.path.join(HERE, "ir_register.json")))["documents"]
    releases = [d for d in reg if d["kind"] in ("ER", "AR") and d.get("is_pdf")]

    rows, unresolved = {}, []
    for d in sorted(releases, key=lambda x: (x["year"], x["period"])):
        path = os.path.join(E.SCRATCH, d["name"])
        if not os.path.exists(path):
            continue
        text, route = flat(path)
        rec = {"document": d["name"], "url": d["url"], "kind": d["kind"],
               "period": d["period"], "route": route,
               "tier": "A — the company's own results release"}
        for rx in UNITS:
            m = rx.search(text)
            if m:
                rec["units_delivered"] = int(m.group(1).replace(",", ""))
                rec["units_quote"] = text[max(0, m.start() - 60):m.end() + 20]
                break
        for key, rx in SALES:
            m = rx.search(text)
            if m:
                rec[key] = float(m.group(1).replace(",", "")) * \
                    SCALE[m.group(2).lower()]
        # the release also quotes recognised revenue; capture it so the KPI and
        # the audited statement can be reconciled rather than assumed to agree
        # the releases word this three ways across four years: "Revenues of
        # EGP 4.01 billion", "Revenues recognized according to the Completed
        # Contract (CC) method recorded EGP 4,009 million", and "Revenues
        # recognised ... recorded EGP 4,511 million"
        m = re.search(r"[Rr]evenues?\b.{0,90}?EGP\s*([\d.,]+)\s*"
                      r"(billion|million|bn|mn)", text)
        if m:
            rec["revenue_quoted"] = float(m.group(1).replace(",", "")) * \
                SCALE[m.group(2).lower()]
            rec["revenue_quote_precision"] = m.group(1)
        # A fiscal year can carry BOTH a results release and a management
        # annual report, and only one of them holds the unit count. Merging
        # rather than overwriting stops the second document erasing what the
        # first found -- which it did, silently, until the unresolved list
        # named two years whose counts were sitting in the output.
        if d["period"] in ("Year-End", "Q4"):
            prior = rows.get(d["year"], {})
            merged = dict(prior)
            for k, v in rec.items():
                if k not in merged or merged[k] in (None, "—"):
                    merged[k] = v
            merged.setdefault("documents", [])
            merged["documents"] = sorted(set(prior.get("documents", []))
                                         | {d["name"]})
            rows[d["year"]] = merged

    for y, r in sorted(rows.items()):
        if "units_delivered" not in r:
            unresolved.append({
                "year": y, "documents": r.get("documents", []),
                "why": "no delivered-unit count in any document the company's "
                       "register carries for this year — the FY2018-FY2020 "
                       "management reports are Arabic scans of the board "
                       "report and no results release for those years is on "
                       "the register"})

    # --- reconcile the release against the audited statement ---------------
    recon = []
    pj = os.path.join(HERE, "panel.json")
    if os.path.exists(pj):
        panel = json.load(open(pj))["years"]
        for y, rec in sorted(rows.items()):
            q = rec.get("revenue_quoted")
            a = panel.get(str(y), {}).get("lines", {}).get("revenue")
            if q is None or a is None:
                continue
            # the release rounds to the nearest million or to two decimals of a
            # billion, so agreement is judged at the release's own precision
            # Judge agreement at the RELEASE'S OWN precision, not at a fixed
            # tolerance: "EGP 3.2 billion" promises nothing finer than ±0.05bn,
            # and scoring it against a percentage band reports a disagreement
            # where the release is simply rounder than the statement.
            q_txt = rec.get("revenue_quote_precision", "")
            dec = len(q_txt.split(".")[1]) if "." in q_txt else 0
            unit = 1e9 if q >= 1e9 and dec else 1e6
            half = 0.5 * unit / (10 ** dec)
            recon.append({"year": y, "release_says": q, "statement_says": a,
                          "release_precision": q_txt,
                          "tolerance": half,
                          "agrees_within_rounding": abs(q - a) <= half})

    out = {"by_year": {str(k): v for k, v in sorted(rows.items())},
           "reconciliation_release_vs_statement": recon,
           "years_without_a_unit_count": unresolved}
    json.dump(out, open(os.path.join(HERE, "kpi.json"), "w"), indent=1,
              sort_keys=True)

    print("  year  units delivered   gross sales        net sales         "
          "revenue in release")
    for y, r in sorted(rows.items()):
        print("  {}  {:>15}  {:>16}  {:>16}  {:>18}".format(
            y, r.get("units_delivered", "—"),
            "{:,.0f}".format(r["gross_sales"]) if "gross_sales" in r else "—",
            "{:,.0f}".format(r["net_sales"]) if "net_sales" in r else "—",
            "{:,.0f}".format(r["revenue_quoted"]) if "revenue_quoted" in r
            else "—"))
    print()
    for c in recon:
        print("  FY{} release {:,.0f} vs audited {:,.0f} -> {}".format(
            c["year"], c["release_says"], c["statement_says"],
            "agrees" if c["agrees_within_rounding"] else "DISAGREES"))
    if unresolved:
        print("\n  no unit count for: %s"
              % ", ".join(str(u["year"]) for u in unresolved))


if __name__ == "__main__":
    main()
