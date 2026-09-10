"""ABUK fundamental walk-forward — the driver panel, with four-field provenance.

EVERY company figure here was read off the issuer's own audited or reviewed
statements.  Nothing is estimated, interpolated or inferred: where a year could
not be sourced it is absent and the window is shorter.

ROUTE MATTERS AND IS RECORDED PER FIGURE.  The company rebuilt its website in
November 2025 and its live shelf begins at the quarter ended 30-Sep-2023, so
FY-Jun-2015 .. FY-Jun-2022 come from the OLD abuqir.net shelf retrieved through
the Internet Archive.  Those filings are the company's own audited statements,
but they are PURE SCANS in Arabic with Eastern-Arabic numerals and zero
characters of text layer, and tesseract's Arabic model runs minutes per page on
them and mangles the digits.  Every figure from them was therefore read off the
rendered pixels at 400 dpi, and ACCEPTED ONLY WHERE THE STATEMENT FOOTS AGAINST
ITS OWN ARITHMETIC.  Residuals that do not foot are recorded in `residual`,
never repaired.

CROSS-FILING CONFIRMATION.  Eight of the eleven years appear twice — once as
their own year and once as the following year's comparative column, in a
separately filed document.  Where both were read they agree to the pound and
that is recorded in `confirmed_by`.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))

A = "A"   # audited / company
B = "B"   # exchange or regulator
C = "C"   # credible third party

ARCHIVE = ("abuqir.net old investor shelf, retrieved through the Internet "
           "Archive (web.archive.org); the document is the company's own "
           "audited statement")
LIVE = "abuqir.net investor shelf (live)"

OCR400 = ("read off rendered pixels at 400 dpi (pdftoppm) — the filing carries "
          "zero characters of text layer")
TEXT = "text layer (pdftotext -layout), arithmetic-confirmed"

# ---------------------------------------------------------------------------
# income statement, EGP, fiscal years ended 30 June
# old presentation FY2015..FY2022; restated/reclassified presentation FY2023..FY2025
# ---------------------------------------------------------------------------
IS = {
 "FY2015": dict(rev=3544240878, cogs=2259952296, gp=1284288582, sell=245658281,
                admin=89545910, pbt=1255662561, tax=352501790, np=903160772,
                basis="old", src="FS_FY2016_Jun.pdf p3 comparative column",
                doc="audited FS year ended 30-Jun-2016", date="2016-08", tier=A,
                route=OCR400, shelf=ARCHIVE, residual=None),
 "FY2016": dict(rev=3935699327, cogs=2634828591, gp=1300870736, sell=250279385,
                admin=102324115, pbt=1197667472, tax=177551288, np=1020116184,
                basis="old", src="FS_FY2016_Jun.pdf p3",
                doc="audited FS year ended 30-Jun-2016", date="2016-08", tier=A,
                route=OCR400, shelf=ARCHIVE, residual="PBT line-sum out by 1 EGP",
                confirmed_by="FS_FY2017_Jun.pdf p3 comparative — every line identical"),
 "FY2017": dict(rev=6021581324, cogs=3961280341, gp=2060300983, sell=306679827,
                admin=100828410, pbt=2839401822, tax=601133612, np=2238268211,
                basis="old", src="FS_FY2017_Jun.pdf p3",
                doc="audited FS year ended 30-Jun-2017", date="2017-08", tier=A,
                route=OCR400, shelf=ARCHIVE, residual="PBT line-sum out by 2 EGP"),
 "FY2018": dict(rev=7552977690, cogs=4878668511, gp=2674309178, sell=375046548,
                admin=112967922, pbt=3012414750, tax=592398978, np=2420015772,
                basis="old", src="FS_FY2018_Jun.pdf p28",
                doc="audited FS year ended 30-Jun-2018", date="2018-08", tier=A,
                route=OCR400, shelf=ARCHIVE, residual="PBT line-sum out by 1 EGP",
                confirmed_by="FS_FY2019_Jun.pdf p60 comparative — every line identical"),
 "FY2019": dict(rev=8584530675, cogs=5144059304, gp=3440471371, sell=413064139,
                admin=135878439, pbt=4065061217, tax=907927901, np=3157133317,
                basis="old", src="FS_FY2019_Jun.pdf p60",
                doc="audited FS year ended 30-Jun-2019", date="2019-08", tier=A,
                route=OCR400, shelf=ARCHIVE,
                residual="the non-operating block sums 5,001 EGP below the printed "
                         "profit before tax; recorded, not repaired",
                confirmed_by="net profit 3,157m matches the FY-Jun-2020 results "
                             "report's prior-year column"),
 "FY2020": dict(rev=7881735379, cogs=4997393877, gp=2884341502, sell=396430335,
                admin=154616443, pbt=3408681603, tax=713795595, np=2694886008,
                basis="old", src="FS_FY2021_Jun.pdf p12 comparative column",
                doc="audited FS year ended 30-Jun-2021", date="2021-08", tier=A,
                route=OCR400, shelf=ARCHIVE, residual=None,
                confirmed_by="revenue 7,882m and net profit 2,695m match the "
                             "FY-Jun-2020 results report exactly"),
 "FY2021": dict(rev=8839412881, cogs=4932573761, gp=3906839120, sell=411820536,
                admin=158309129, pbt=4318095163, tax=802087982, np=3516007181,
                basis="old", src="FS_FY2021_Jun.pdf p12",
                doc="audited FS year ended 30-Jun-2021", date="2021-08", tier=A,
                route=OCR400, shelf=ARCHIVE, residual="PBT line-sum out by 1 EGP",
                confirmed_by="FS_FY2022_Jun.pdf p13 comparative — every line identical"),
 "FY2022": dict(rev=16330932653, cogs=5703316993, gp=10627615660, sell=472363265,
                admin=233442677, pbt=11558392552, tax=2504253224, np=9054139328,
                basis="old", src="FS_FY2022_Jun.pdf p13",
                doc="audited FS year ended 30-Jun-2022", date="2022-09", tier=A,
                route=OCR400, shelf=ARCHIVE,
                residual="the non-operating block sums 6,000,129 EGP above the "
                         "printed profit before tax; recorded, not repaired",
                confirmed_by="net profit 9,054,139,328 matches the transition note "
                             "in the audited FY-Jun-2024 filing to the pound"),
 "FY2023": dict(rev=21657256289, cogs=9041419564, gp=12615836725, sell=777218814,
                admin=697101648, pbt=17868068727, tax=3847599932, np=14020468795,
                other_inc=209240601, other_exp=33658715, ecl=117850015,
                opprof=11199248134, divinc=1032338375, finc=1837507150,
                fcost=70401373, fx=3869376441,
                basis="new", src="FS_FY2024_Jun_EN.pdf p2 comparative column "
                                 "(restated and reclassified)",
                doc="audited FS year ended 30-Jun-2024", date="2024-08-29", tier=A,
                route=TEXT, shelf=LIVE, residual=None),
 "FY2024": dict(rev=18527811974, cogs=10192200227, gp=8335611747, sell=1085969759,
                admin=729401857, pbt=17110420757, tax=3632015353, np=13478405404,
                other_inc=45930716, other_exp=121223964, ecl=8956748,
                opprof=6435990135, divinc=1485115084, finc=2550733178,
                fcost=110284295, fx=6748866655,
                basis="new", src="FS_FY2024_Jun_EN.pdf p2",
                doc="audited FS year ended 30-Jun-2024", date="2024-08-29", tier=A,
                route=TEXT, shelf=LIVE, residual=None,
                restated_to="PBT 17,108,562,667 / tax 3,631,829,544 / net profit "
                            "13,476,733,123 in the FY-Jun-2025 comparative; the "
                            "as-filed column is used, point-in-time"),
 "FY2025": dict(rev=22915657021, cogs=12470407550, gp=10445249471, sell=1275781242,
                admin=702764619, pbt=11936535086, tax=2583771838, np=9352763248,
                other_inc=207064297, other_exp=534913124, ecl=-24031242,
                opprof=8162886025, divinc=1091097833, finc=2137928944,
                fcost=45995317, fx=584061897, assoc=6555705,
                basis="new", src="FS_FY2025_Jun_EN.pdf p6",
                doc="audited FS year ended 30-Jun-2025", date="2025-08-31", tier=A,
                route=TEXT, shelf=LIVE, residual="PBT line-sum out by 1 EGP"),
}

# ---------------------------------------------------------------------------
# balance sheet and cash flow items used by the valuation-input block
# ---------------------------------------------------------------------------
BS = {
 "FY2018": dict(ppe=603015943, puc=479802316, cash=831016265, invest=3756906542,
                inventory=1075449353, receivable=457150386, payable=None,
                debt=76452968+62997247+48113292+23181000, equity=4881609711,
                total_assets=7870604429, capex=107713238,
                src="FS_FY2019_Jun.pdf p59 comparative column, p63 cash flow",
                doc="audited FS year ended 30-Jun-2019", date="2019-08", tier=A,
                route=OCR400, shelf=ARCHIVE,
                residual="the suppliers-and-other-creditors line does not foot to "
                         "its printed current-liability subtotal on this scan, so "
                         "the payable is not recorded"),
 "FY2019": dict(ppe=654177675, puc=489349601, cash=403129219, invest=5530311673,
                inventory=1216610035, receivable=439113216, payable=1385902985,
                debt=26547862+45866247+45084096+17181000, equity=6258535887,
                total_assets=9056193232, capex=130162865,
                src="FS_FY2019_Jun.pdf p59, p63",
                doc="audited FS year ended 30-Jun-2019", date="2019-08", tier=A,
                route=OCR400, shelf=ARCHIVE,
                residual="the non-current-liability block sums 160,001 EGP above "
                         "its printed subtotal; total assets and total equity both "
                         "foot to the pound and govern"),
 "FY2020": dict(ppe=1102832506, puc=231574924, cash=576327552, invest=5347396728,
                inventory=1276052732, receivable=441789956, payable=1469948288,
                debt=45506+28635247+25605299+17181000, equity=6799731013,
                total_assets=9311636860, capex=229268790,
                src="FS_FY2021_Jun.pdf p11 comparative column, p15 cash flow",
                doc="audited FS year ended 30-Jun-2021", date="2021-08", tier=A,
                route=OCR400, shelf=ARCHIVE, residual=None),
 "FY2021": dict(ppe=1004125359, puc=379177991, cash=625228485, invest=6599853793,
                inventory=1282390100, receivable=615690423, payable=1364622718,
                debt=45506, equity=8360606168,
                total_assets=10847844464, capex=146587751,
                src="FS_FY2021_Jun.pdf p11, p15",
                doc="audited FS year ended 30-Jun-2021", date="2021-08", tier=A,
                route=OCR400, shelf=ARCHIVE, residual=None,
                confirmed_by="FS_FY2022_Jun.pdf p12 and p16 comparatives — "
                             "identical to the pound"),
 "FY2022": dict(ppe=1221255529, puc=294255347, cash=2933798595, invest=11268037193,
                inventory=1563956789, receivable=866781117, payable=None,
                debt=None, equity=None, total_assets=None, capex=210456468,
                src="FS_FY2022_Jun.pdf p12, p16",
                doc="audited FS year ended 30-Jun-2022", date="2022-09", tier=A,
                route=OCR400, shelf=ARCHIVE, residual=None,
                cash_src="cash at 30-Jun-2022 is taken from the audited "
                         "FY-Jun-2024 filing's cash-flow statement, FY2023 "
                         "comparative column, 'Cash & cash equivalent at the "
                         "beginning of the year' EGP 2,933,798,595 — text layer. "
                         "The FY-Jun-2022 scan's own closing-cash line was read "
                         "as 2,933,398,095 and does not foot to it by 400,500 "
                         "EGP, so the text-layer figure governs and the "
                         "discrepancy is recorded rather than averaged."),
 "FY2023": dict(ppe=1186400030, puc=None, cash=17464775441, invest=None,
                inventory=1873998330, receivable=257042674, payable=41178382,
                debt=0, equity=None, total_assets=None, capex=151217123,
                src="FS_FY2024_Jun_EN.pdf notes 4, 11, 12, 17, 24 and the "
                    "cash-flow statement, comparative columns",
                doc="audited FS year ended 30-Jun-2024", date="2024-08-29", tier=A,
                route=TEXT, shelf=LIVE, residual=None),
 "FY2024": dict(ppe=1875134305, puc=None, cash=23354598768, invest=None,
                inventory=2072434578, receivable=241793653, payable=92153797,
                debt=0, equity=33121608804, total_assets=42329153379,
                capex=418523619,
                src="FS_FY2024_Jun_EN.pdf notes 4, 11, 12, 17, 24, statement of "
                    "changes in equity and the cash-flow statement",
                doc="audited FS year ended 30-Jun-2024", date="2024-08-29", tier=A,
                route=TEXT, shelf=LIVE, residual=None),
}

# depreciation charge: disclosed where the fixed-asset note was read, otherwise
# DERIVED by capex = dPP&E + D&A and labelled as such.
DEP = {
 "FY2024": dict(value=120504043, derived=False,
                src="FS_FY2024_Jun_EN.pdf note 4, accumulated-depreciation block",
                route=TEXT),
 "FY2025": dict(value=168591319, derived=False,
                src="FS_FY2025_Jun_EN.pdf note 4, accumulated-depreciation block",
                route=TEXT),
}

SHARES = dict(value=1261875720, issued_capital=1892813580, par_value=1.5,
              src="FS_FY2024_Jun_EN.pdf note 18B — 'EGP 1 892 813 580 divided "
                  "into 1 261 875 720 shares of EGP 1.5 par value'",
              route=TEXT,
              also="the same paid-in capital of EGP 1,892,813,580 is printed on "
                   "the balance sheet of every filing from FY-Jun-2018 to "
                   "FY-Jun-2025, so the count is unchanged across every origin "
                   "this run tests and no count is carried back into a year the "
                   "filings do not support")

ORDER = ["FY%d" % y for y in range(2015, 2026)]


def load_macro():
    return json.load(open(os.path.join(HERE, "macro.json")))


def build():
    m = load_macro()["fiscal_year_derived"]
    rows = {}
    for y in ORDER:
        r = dict(IS[y])
        fy = m[y]
        r["urea_usd_t"] = fy["urea_usd_t"]
        r["egp_usd"] = fy["egp_usd"]
        r["cpi_pct"] = fy["cpi_eg_pct"]
        # DERIVED: the volume proxy the archive supports.  ABUK does not disclose
        # per-product tonnage anywhere (negative search F45), so the finest
        # sourceable physical driver is revenue deflated by the world urea price
        # and the exchange rate.  Units: tonne-equivalents at world urea parity.
        r["vol_proxy"] = r["rev"] / (fy["urea_usd_t"] * fy["egp_usd"])
        r["vol_proxy_note"] = ("DERIVED: revenue / (urea USD per tonne x EGP per "
                               "USD). A price-deflated volume proxy, not a "
                               "disclosed tonnage.")
        r["cogs_ratio"] = r["cogs"] / r["rev"]
        r["sell_ratio"] = r["sell"] / r["rev"]
        r["etr"] = r["tax"] / r["pbt"]
        r["nonop"] = r["pbt"] - r["gp"] + r["sell"] + r["admin"]
        rows[y] = r
    doc = {
        "_ticker": "ABUK",
        "_built": "2026-09-09",
        "_span": "FY-Jun-2015 .. FY-Jun-2025, eleven complete fiscal years",
        "_why_it_stops_there": (
            "It stops at FY-Jun-2025 because that is the last COMPLETE twelve-month "
            "fiscal year the company reported: it then changed its year end from 30 "
            "June to 31 December and filed an audited SIX-MONTH transitional period "
            "to 31-Dec-2025, which is not an annual actual and is excluded from "
            "scoring. It stops at FY-Jun-2015 because the FY-Jun-2016 audited "
            "statements are the oldest annual filing recoverable from the company's "
            "shelf, and FY2015 is their comparative column; no FY-Jun-2014 or "
            "earlier annual filing could be located on abuqir.net, in the Internet "
            "Archive's capture of it, or through the exchange."),
        "_provenance_summary": (
            "Eleven years, every one tier A off the issuer's own audited statements. "
            "FY2023-FY2025 (the most recent three) and every current-year quarter "
            "come from the live company shelf with a clean text layer. FY2015-FY2022 "
            "come from the same company's audited statements retrieved through the "
            "Internet Archive after the November-2025 website rebuild removed them, "
            "read off rendered pixels and accepted only where they foot."),
        "shares": SHARES,
        "dep_disclosed": DEP,
        "balance_sheet": BS,
        "years": rows,
    }
    json.dump(doc, open(os.path.join(HERE, "panel.json"), "w"), indent=1,
              sort_keys=True, default=float)
    return doc


if __name__ == "__main__":
    d = build()
    print("%-8s %14s %14s %8s %8s %8s %9s %8s %8s" % (
        "FY", "revenue", "net profit", "cogs%", "sell%", "etr%", "urea$/t",
        "EGP/USD", "vol prx"))
    for y in ORDER:
        r = d["years"][y]
        print("%-8s %14.0f %14.0f %7.1f%% %7.1f%% %7.1f%% %9.1f %8.2f %8.0f" % (
            y, r["rev"], r["np"], 100 * r["cogs_ratio"], 100 * r["sell_ratio"],
            100 * r["etr"], r["urea_usd_t"], r["egp_usd"], r["vol_proxy"]))
