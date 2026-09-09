"""ABUK — the valuation-input block, one per origin. [R-FCAL-01 AMENDED]

A driver panel is not a record a VALUE can be rebuilt from.  These are the seven
items a rebuild at each origin needs, taken from the same statements and under
the same point-in-time discipline as every other figure in this run.

Built AS THE RUN WENT, not retro-fitted.  A missing item is recorded as missing
with its reason and is never omitted; the share count is footed against issued
capital over par in the document that states it; a derived capex names the
identity it was derived by; and the route — text layer or OCR, with the file —
is recorded on every value.
"""
import json, os
import panel as P

HERE = os.path.dirname(os.path.abspath(__file__))
ORIGINS = ["FY2019", "FY2020", "FY2021", "FY2022", "FY2023", "FY2024"]
ANCHOR = "FY2018"

# Depreciation.  Two routes and both are labelled.  Where the fixed-asset note
# was read the charge is DISCLOSED.  Where it was not, the charge is DERIVED by
# the identity capex = dPP&E + D&A, adjusted for the net book value of disposals
# implied by the proceeds and the capital gain the income statement prints.
DEP_DERIVED = {
    "FY2019": dict(value=69238409,
                   why="capex 130,162,865 less the movement in net fixed assets "
                       "and projects under construction (1,143,527,276 - "
                       "1,082,818,259 = 60,709,017) less an implied disposal book "
                       "value of 215,439 (proceeds 2,934,438 less the capital "
                       "gain of 2,718,999 the income statement prints)"),
    "FY2021": dict(value=96617424,
                   why="capex 146,587,751 less the movement in net fixed assets, "
                       "projects under construction (1,383,303,350 - "
                       "1,334,407,430 = 48,895,920) less an implied disposal book "
                       "value of 1,074,407"),
    "FY2022": dict(value=78070978,
                   why="capex 210,456,468 less the movement in net fixed assets, "
                       "projects under construction and right-of-use assets "
                       "(1,515,606,548 - 1,383,303,350 = 132,303,198) less an "
                       "implied disposal book value of 82,292"),
    "FY2023": dict(value=186072622,
                   why="capex 151,217,123 plus the FALL in net fixed assets "
                       "(1,221,255,529 - 1,186,400,030 = 34,855,499); the "
                       "disposal book value is not separable from the FY2023 "
                       "comparative and is not adjusted for, so this is an "
                       "upper bound"),
}

DEP_MISSING = {
    "FY2020": ("the identity capex = dPP&E + D&A does not hold across FY-Jun-2020 "
               "on this issuer: net fixed assets rose EGP 448.4m against capex of "
               "EGP 229.3m, so a revaluation or a transfer sits inside the "
               "movement and any charge derived from it would be arithmetic "
               "wearing the costume of a disclosure. The charge is disclosed only "
               "in the fixed-asset note of the audited FY-Jun-2021 filing, which "
               "is a fifty-page Arabic scan with no text layer, and that note was "
               "not read in this run."),
}


def block(year, is_anchor=False):
    bs = P.BS.get(year)
    if bs is None:
        return None
    def rec(v, item, extra=None):
        if v is None:
            return None
        d = dict(value=v, source="%s — %s" % (bs["doc"], bs["src"]),
                 route="%s [%s]" % (bs["route"], bs["shelf"]), tier=bs["tier"],
                 document_date=bs["date"])
        if extra:
            d.update(extra)
        return d

    out = {}
    out["cash"] = rec(bs.get("cash"), "cash") or {
        "missing": "the closing-cash line on this scan does not foot to the "
                   "filing's own cash-flow reconciliation and was not accepted"}
    if year == "FY2022" and bs.get("cash_src"):
        out["cash"]["source"] = bs["cash_src"]
        out["cash"]["route"] = "text layer (pdftotext -layout) [abuqir.net live shelf]"

    out["debt"] = rec(bs.get("debt"), "debt", {
        "note": "INTEREST-BEARING BORROWINGS ONLY — bank loans and notes payable, "
                "long-term portion plus the portion due within one year. "
                "Suppliers, other creditors and the tax-authority balance are "
                "excluded because they bear no interest, which is the whole point "
                "of the rule."})
    if out["debt"] is None:
        out["debt"] = {"missing": "the borrowings block on the FY-Jun-2022 scan "
                                  "was not separately read; the company discloses "
                                  "'no loans at the reporting date' in the "
                                  "H1-2026 interest-rate-risk note, so the "
                                  "balance is small, but a figure that was not "
                                  "read is not recorded"}

    cap = bs.get("capex")
    out["capex"] = rec(cap, "capex", {
        "derived": False,
        "note": "payments for the purchase of fixed assets and assets under "
                "construction, as disclosed in the cash-flow statement"})

    out["ppe"] = rec(bs.get("ppe"), "ppe", {
        "note": "net book value of fixed assets; projects under construction of "
                "%s are recorded beside it and are not included"
                % ("{:,}".format(bs["puc"]) if bs.get("puc") else "an amount not read"),
        "projects_under_construction": bs.get("puc")})

    if year in DEP_DERIVED:
        d = DEP_DERIVED[year]
        out["dep"] = dict(value=d["value"], derived=True,
                          identity="capex = dppe + d&a",
                          source="%s — %s" % (bs["doc"], bs["src"]),
                          route="%s [%s]" % (bs["route"], bs["shelf"]),
                          note="DERIVED. " + d["why"], tier=bs["tier"],
                          document_date=bs["date"])
    elif year in P.DEP:
        d = P.DEP[year]
        out["dep"] = dict(value=d["value"], derived=False, source=d["src"],
                          route=d["route"], tier="A")
    else:
        out["dep"] = {"missing": DEP_MISSING[year]}

    inv, recv, pay = bs.get("inventory"), bs.get("receivable"), bs.get("payable")
    if inv is not None and recv is not None and pay is not None:
        out["wc"] = dict(value=inv + recv - pay,
                         source="%s — %s" % (bs["doc"], bs["src"]),
                         route="%s [%s]" % (bs["route"], bs["shelf"]),
                         tier=bs["tier"], document_date=bs["date"],
                         inventory=inv, receivables=recv, payables=pay,
                         note="inventories plus trade and other receivables less "
                              "suppliers and other creditors. THE CAPTION WIDENS "
                              "AT FY2023: the pre-FY2023 filings print one "
                              "'suppliers and other creditors' line while the "
                              "restated presentation splits trade payables out, "
                              "so the two windows are not the same measure and "
                              "the break is in the basis-break register.")
    else:
        out["wc"] = {"missing": "the payables caption on this scan does not foot "
                                "to its printed current-liability subtotal, so "
                                "working capital is not recorded rather than "
                                "recorded wrong"}

    out["shares"] = dict(P.SHARES)
    out["shares"]["note"] = (
        "The count is footed in the document that states it: issued capital EGP "
        "1,892,813,580 over a par value of EGP 1.50 reproduces 1,261,875,720. "
        "The same paid-in capital is printed on the balance sheet of every "
        "filing from FY-Jun-2018 to FY-Jun-2025, so no count is carried back "
        "into a year the filings do not support.")
    return out


def main():
    doc = {"_ticker": "ABUK", "_built": "2026-09-09",
           "_scope": "FULL run, origins FY2019..FY2024, horizons 1-5",
           "_currency": "EGP",
           "prior_year_anchor": {ANCHOR: block(ANCHOR, True)},
           "origins": {o: block(o) for o in ORIGINS}}
    json.dump(doc, open(os.path.join(HERE, "valuation_inputs.json"), "w"),
              indent=1, sort_keys=True, default=float)
    return doc


if __name__ == "__main__":
    d = main()
    for o in ORIGINS:
        b = d["origins"][o]
        print(o, " ".join("%s=%s" % (k, "MISSING" if "missing" in b[k]
                                     else ("%.0f" % b[k]["value"]))
                          for k in ("cash", "debt", "capex", "ppe", "dep", "wc")))
