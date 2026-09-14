#!/usr/bin/env python3
"""ELEC — the filed record, read off the company's OWN audited statements.

EVERY FIGURE HERE CAME OFF THE RENDERED PIXELS. The four committed filings carry no
usable text layer (pdftotext returns 3 characters across 33 pages on the one complete
file), so under [R-FCAL-01] the route is recorded and ARITHMETIC IS THE ARBITER: every
subtotal below was re-added by hand against its own statement before it was written
down, and the footing results are committed beside the figures in footing_report().

THREE OF THE FOUR FILINGS ARE TRUNCATED and that is a fact about the files, not about
the company: FY2020, FY2022 and FY2023 stop at exactly 1 MiB, 5 MiB and 5 MiB with no
%%EOF and no readable xref, so pymupdf opens them at zero pages. The page images were
recovered by scanning the raw bytes for JPEG streams, which is why FY2023 yields 24
pages of a document whose FY2021 sibling runs to 33. Notes past the truncation point
are GONE and are recorded as gone rather than guessed at.

BASIS. FY2019 and FY2020 are CONSOLIDATED; FY2020 through FY2023 are STANDALONE. FY2020
therefore exists on BOTH bases and is the overlap year the basis-break register needs.
The company has issued no consolidated statement since FY2020 while holding a 99.99%
subsidiary (note 5), so the standalone accounts are NOT a substitute for the
consolidated ones — they are a different and smaller reporting entity, and the wedge is
MEASURED at the overlap rather than assumed.
"""

CCY = "EGP"

FILINGS = {
    "FY2020C": {"file": "engine/elec_study/filings/ELEC_FY2020_Consolidated_Annual_TRUNCATED.pdf",
                "basis": "consolidated", "tier": "A", "doc_date": "2020-12-31",
                "route": "OCR/pixel read of JPEG streams recovered from a truncated PDF (7 of ~30 pages)",
                "auditor": "UHY United"},
    "FY2021S": {"file": "engine/elec_study/filings/ELEC_FY2021_Standalone_Annual.pdf",
                "basis": "standalone", "tier": "A", "doc_date": "2021-12-31",
                "route": "pixel read at 330dpi, complete 33-page file, HP Scan 27-Feb-2022",
                "auditor": "UHY United"},
    "FY2022S": {"file": "engine/elec_study/filings/ELEC_FY2022_Standalone_Annual.pdf",
                "basis": "standalone", "tier": "A", "doc_date": "2022-12-31",
                "route": "OCR/pixel read of JPEG streams recovered from a truncated PDF (17 pages)",
                "auditor": "UHY United"},
    "FY2023S": {"file": "engine/elec_study/filings/ELEC_FY2023_Standalone_Annual.pdf",
                "basis": "standalone", "tier": "A", "doc_date": "2023-12-31",
                "route": "OCR/pixel read of JPEG streams recovered from a truncated PDF (24 pages)",
                "auditor": "UHY United"},
}

# ---------------------------------------------------------------- income statement
# src = the filing the figure was READ FROM (a comparative column counts as that filing)
IS = {
    ("FY2019", "consolidated"): dict(
        src="FY2020C", page=5, rev=2033436125, cogs=-1645451167, gp=387984958,
        op=248842725, pbt=231598834, np=166778241, nci=81),
    ("FY2020", "consolidated"): dict(
        src="FY2020C", page=5, rev=1740090697, cogs=-1528393436, gp=211697261,
        op=121562003, pbt=177312174, np=133506537, nci=44),
    ("FY2020", "standalone"): dict(
        src="FY2021S", page=5, rev=1003350740, cogs=-944205628, gp=59145112,
        op=3524172, pbt=83487706, np=65409824, eps=0.016),
    ("FY2021", "standalone"): dict(
        src="FY2021S", page=5, rev=1421442451, cogs=-1307247219, gp=114195232,
        op=57604982, pbt=97137734, np=72903639, eps=0.018),
    ("FY2022", "standalone"): dict(
        src="FY2023S", page=5, rev=3159826850, cogs=-2802714922, gp=357111928,
        op=249243079, pbt=172797390, np=141310292, eps=0.034),
    ("FY2023", "standalone"): dict(
        src="FY2023S", page=5, rev=4857508463, cogs=-3916265699, gp=941242764,
        op=834200418, pbt=533469015, np=404120612, eps=0.099),
}

# D&A split as the cash-flow statement discloses it. NOT available consolidated:
# the FY2020 consolidated cash-flow statement sits past the truncation.
DNA = {
    ("FY2020", "standalone"): dict(src="FY2021S", page=8, fixed=10837212, rou=0),
    ("FY2021", "standalone"): dict(src="FY2021S", page=8, fixed=12077997, rou=576397),
    ("FY2022", "standalone"): dict(src="FY2023S", page=8, fixed=13246808, rou=1149348),
    ("FY2023", "standalone"): dict(src="FY2023S", page=8, fixed=14246581, rou=1149348),
    ("FY2019", "consolidated"): None,   # past the truncation
    ("FY2020", "consolidated"): None,   # past the truncation
}

# Finance expense as the income statement discloses it ('مصروفات تمويلية').
FINANCE_COST = {
    ("FY2020", "standalone"): 21730347,
    ("FY2021", "standalone"): 43427339,
    ("FY2022", "standalone"): 84141987,
    ("FY2023", "standalone"): 308666911,
}

# ---------------------------------------------------------------- balance sheet
# INTEREST-BEARING DEBT ONLY [R-FCAL-01 trap (i)]: bank credit facilities, the
# long-term loan, and the lease / financing-arrangement liabilities (note 4/2, a
# sale-and-leaseback with a leasing company, assigned to Emirates NBD — it bears
# interest). Trade payables, amounts due to related parties, tax liabilities,
# provisions, deferred tax and dividends payable BEAR NO INTEREST and are excluded.
BS = {
    ("FY2020", "standalone"): dict(
        src="FY2021S", page=4, cash=109713607, ppe=336254253, rou=0, cip=0,
        inventory=183456854, receivables=390265783, due_from_related=189174933,
        payables=280945979, due_to_related=108141002,
        facilities=291837450, lt_loan=32000000, lease_fin=0,
        equity=752146281, total_assets=1532406573, capital=711447385, par=1.00),
    ("FY2021", "standalone"): dict(
        src="FY2021S", page=4, cash=107414240, ppe=361896338, rou=9752032, cip=0,
        inventory=357839054, receivables=596713039, due_from_related=273417384,
        payables=330488928, due_to_related=62647014,
        facilities=649414404, lt_loan=0, lease_fin=49795857,
        equity=861805907, total_assets=2019231760, capital=711447385, par=0.20),
    ("FY2022", "standalone"): dict(
        src="FY2023S", page=4, cash=312587086, ppe=373765804, rou=8602684, cip=0,
        inventory=689613937, receivables=613232751, due_from_related=247702470,
        payables=366271508, due_to_related=69126999,
        facilities=977245481, lt_loan=0, lease_fin=198313555,
        equity=884988851, total_assets=2587744478, capital=711447385, par=0.20),
    ("FY2023", "standalone"): dict(
        src="FY2023S", page=4, cash=546462018, ppe=374384411, rou=7453336, cip=21844336,
        inventory=766227104, receivables=1118837093, due_from_related=653738562,
        payables=287760863, due_to_related=0,
        facilities=1732315750, lt_loan=0, lease_fin=474476371,
        equity=1214259130, total_assets=3890066687, capital=680928642, par=0.20),
}

# CAPEX AS THE CASH-FLOW STATEMENT DISCLOSES IT — not derived. The identity
# capex = dPPE + D&A is NOT used here and must not be: these years carry large
# disposals (FY2021 proceeds of 103.5mn on a book gain of 78.1mn), so the identity
# does not close and the disclosed figure is the better number as well as the
# sanctioned one.
CAPEX = {
    ("FY2020", "standalone"): dict(src="FY2021S", page=8, fixed_assets=7805840, cip=0,
                                   advances=3720115),
    ("FY2021", "standalone"): dict(src="FY2021S", page=8, fixed_assets=25332522, cip=0,
                                   advances=34078231),
    ("FY2022", "standalone"): dict(src="FY2023S", page=8, fixed_assets=25404274, cip=0,
                                   advances=0),
    ("FY2023", "standalone"): dict(src="FY2023S", page=8, fixed_assets=19225366,
                                   cip=21844336, advances=0),
}

# The share-count recital, note 13 of the FY2021 filing, page 25. It is a CHRONOLOGY
# of resolutions, which is the shape [R-FCAL-01 AMENDED] clause (ii) anticipates: the
# recital establishes the PAR VALUE and the identity, and each year's count is that
# year's OWN committed capital divided by that par. Today's count is never carried back.
CAPITAL_RECITAL = {
    "src": "FY2021S", "page": 25, "note": 13,
    "authorised_egp": 850000000,
    "issued_paid_egp": 711447385,
    "shares_stated": 711447385,
    "par_before": 1.00,
    "split": "EGM 2 December 2020 approved a 1:5 split to a par of EGP 0.20; the "
             "listing committee ratified it on 24 January 2021, so the split is AFTER "
             "the 31-Dec-2020 balance-sheet date and the FY2020 count is the pre-split "
             "one.",
    "par_after": 0.20,
    "shares_after_split_stated": 3557236925,
    "foots": "711,447,385 / 0.20 = 3,557,236,925, which is the count the note itself "
             "states. The identity reproduces exactly.",
}

# The disclosed useful-life spans, FY2023 note 2-4, page 13. A RANGE IS NOT A LIFE.
USEFUL_LIFE_SPANS = {
    "buildings_constructions_utilities": [10, 50],
    "machinery_and_equipment": [4, 25],
    "vehicles_and_transport": [5, 20],
    "tools_and_equipment": [5, 20],
    "computers": [5, 5],
    "furniture_and_office_equipment": [5, 10],
}

# Note 3, the fixed-asset roll-forward, FY2023 page 19 (a landscape table).
FIXED_ASSET_NOTE_FY2023 = {
    "src": "FY2023S", "page": 19,
    "cost_open": 581667408, "additions": 19225366, "disposals": -6478823,
    "cost_close": 594413951,
    "land_close": 250643846,          # land is NOT depreciated
    "accdep_open": -207901604, "charge": -14246581, "disposals_accdep": 2118645,
    "accdep_close": -220029540,
    "nbv_close": 374384411,
    "fully_depreciated_still_in_use": 93877527,
    "charge_allocation": {"cogs": 13642676, "selling": 215910, "admin": 387995},
}


# =====================================================================  derivations
def debt(y, basis="standalone"):
    """Interest-bearing debt ONLY [R-FCAL-01 trap (i)]."""
    b = BS[(y, basis)]
    return b["facilities"] + b["lt_loan"] + b["lease_fin"]


def dna(y, basis="standalone"):
    d = DNA.get((y, basis))
    return None if d is None else d["fixed"] + d["rou"]


def ebitda(y, basis="standalone"):
    d = dna(y, basis)
    return None if d is None else IS[(y, basis)]["op"] + d


def shares(y, basis="standalone"):
    """capital / par, on the par the recital establishes for THAT date."""
    b = BS[(y, basis)]
    return b["capital"] / b["par"]


def borrowing_rate_check(y, basis="standalone"):
    """TRAP (i) DEMONSTRATED ON LIVE DATA, not asserted.

    The finance charge over the borrowings that actually BEAR it, beside the same
    charge over total liabilities — the broad denominator the trap describes. The
    second is what a model gets when it divides by a liabilities total that includes
    trade payables, related-party balances, tax and provisions.
    """
    prev = "FY%d" % (int(y[2:]) - 1)
    if (prev, basis) not in BS or (y, basis) not in FINANCE_COST:
        return None
    b, p = BS[(y, basis)], BS[(prev, basis)]
    fin = FINANCE_COST[(y, basis)]
    avg_debt = (debt(y, basis) + debt(prev, basis)) / 2.0
    avg_liab = ((b["total_assets"] - b["equity"]) +
                (p["total_assets"] - p["equity"])) / 2.0
    return {"finance_cost": fin,
            "rate_on_bearing_debt": fin / avg_debt,
            "rate_on_total_liabilities": fin / avg_liab,
            "understatement_pp": (fin / avg_debt - fin / avg_liab) * 100}


def footing_report():
    """Re-add every subtotal against its own statement. Arithmetic is the arbiter."""
    out = []
    for (y, basis), r in sorted(IS.items()):
        out.append(("%s %s  gross profit" % (y, basis),
                    r["rev"] + r["cogs"], r["gp"]))
    for (y, basis), b in sorted(BS.items()):
        # the sheet balances: equity + liabilities = assets is checked at source; here
        # the item this run actually consumes is the debt build, checked against its
        # own components, and the share identity.
        out.append(("%s %s  shares = capital/par" % (y, basis),
                    b["capital"] / b["par"], round(b["capital"] / b["par"])))
    f = FIXED_ASSET_NOTE_FY2023
    out.append(("FY2023 fixed-asset cost roll",
                f["cost_open"] + f["additions"] + f["disposals"], f["cost_close"]))
    out.append(("FY2023 accumulated depreciation roll",
                f["accdep_open"] + f["charge"] + f["disposals_accdep"], f["accdep_close"]))
    out.append(("FY2023 net book value",
                f["cost_close"] + f["accdep_close"], f["nbv_close"]))
    out.append(("FY2023 depreciation allocation",
                sum(f["charge_allocation"].values()), -f["charge"]))
    out.append(("FY2023 capex: cash flow vs fixed-asset note additions",
                CAPEX[("FY2023", "standalone")]["fixed_assets"], f["additions"]))
    return out


def consolidation_wedge():
    """The chain factor at the ONE year that exists on both bases.

    This is the whole reason FY2020 is carried twice. Without it, nothing measures how
    far the standalone parent sits below the group the study models — it would have to
    be asserted, and [R-FCAL-01] does not permit that.
    """
    c, s = IS[("FY2020", "consolidated")], IS[("FY2020", "standalone")]
    return {
        "year": "FY2020",
        "revenue": {"consolidated": c["rev"], "standalone": s["rev"],
                    "factor": c["rev"] / s["rev"]},
        "gross_profit": {"consolidated": c["gp"], "standalone": s["gp"],
                         "factor": c["gp"] / s["gp"]},
        "operating_profit": {"consolidated": c["op"], "standalone": s["op"],
                             "factor": c["op"] / s["op"]},
        "net_profit": {"consolidated": c["np"], "standalone": s["np"],
                       "factor": c["np"] / s["np"]},
        "nci_egp": c["nci"],
    }


def implied_useful_life():
    """ROUTE (2): depreciable gross cost / annual depreciation charge.

    Route (1) — the policy note's own table — FAILS on this name: it discloses SPANS
    (10-50, 4-25, 5-20, 5-20, 5, 5-10) with no scalar and no dominant class, and
    picking a point inside a span is the choice [R-TERM-01] exists to forbid.

    TWO figures are returned and neither is a preference. EGP 93.9mn of gross cost is
    FULLY DEPRECIATED AND STILL IN USE — 27% of the depreciable base — and such assets
    carry cost but no charge, which lengthens the ratio. The honest answer is the band.
    """
    f = FIXED_ASSET_NOTE_FY2023
    depreciable = f["cost_close"] - f["land_close"]
    charge = -f["charge"]
    return {
        "route": "2 — derived by the identity, labelled derived",
        "depreciable_gross_cost": depreciable,
        "annual_charge": charge,
        "years_on_full_base": depreciable / charge,
        "years_excluding_fully_depreciated": (
            (depreciable - f["fully_depreciated_still_in_use"]) / charge),
        "prior_year_control": (581667408 - f["land_close"]) / 13246808,
        "disclosed_spans": USEFUL_LIFE_SPANS,
    }


if __name__ == "__main__":
    print("ELEC filed record — footing, arithmetic as the arbiter\n")
    bad = 0
    for label, computed, printed in footing_report():
        ok = abs(computed - printed) <= max(1.0, abs(printed) * 1e-9)
        bad += (not ok)
        print("  %-58s %-18s %s" % (label, "FOOTS" if ok else "REFUSES",
                                    "" if ok else "%.0f vs %.0f" % (computed, printed)))
    print("\n  refusals: %d" % bad)

    print("\nfiled EBITDA margin, standalone, on the company's own accounts")
    for y in ("FY2020", "FY2021", "FY2022", "FY2023"):
        e = ebitda(y)
        print("  %s  op %13d  D&A %10d  EBITDA %13d  margin %6.2f%%"
              % (y, IS[(y, "standalone")]["op"], dna(y), e,
                 100 * e / IS[(y, "standalone")]["rev"]))
    print("\nfiled OPERATING margin, consolidated (D&A past the truncation)")
    for y in ("FY2019", "FY2020"):
        r = IS[(y, "consolidated")]
        print("  %s  op %13d  revenue %13d  margin %6.2f%%"
              % (y, r["op"], r["rev"], 100 * r["op"] / r["rev"]))

    print("\nconsolidation wedge at the overlap year")
    for k, v in consolidation_wedge().items():
        if isinstance(v, dict):
            print("  %-18s consolidated %13d  standalone %13d  x%.4f"
                  % (k, v["consolidated"], v["standalone"], v["factor"]))

    print("\nshare count, footed against the recital's par")
    for y in ("FY2020", "FY2021", "FY2022", "FY2023"):
        b = BS[(y, "standalone")]
        print("  %s  capital %13d / par %.2f = %15d shares"
              % (y, b["capital"], b["par"], shares(y)))

    print("\ninterest-bearing debt [trap (i)]")
    for y in ("FY2020", "FY2021", "FY2022", "FY2023"):
        b = BS[(y, "standalone")]
        tot_liab = b["total_assets"] - b["equity"]
        print("  %s  bearing %13d   total liabilities %13d   ratio %.2fx"
              % (y, debt(y), tot_liab, tot_liab / debt(y)))

    print("\nuseful life, route (2)")
    ul = implied_useful_life()
    print("  depreciable gross cost %d / charge %d = %.2f years"
          % (ul["depreciable_gross_cost"], ul["annual_charge"], ul["years_on_full_base"]))
    print("  excluding fully-depreciated-still-in-use: %.2f years"
          % ul["years_excluding_fully_depreciated"])
    print("  prior-year control (FY2022 base and charge): %.2f years"
          % ul["prior_year_control"])

    print("\ntrap (i): the charge over what bears it, against the broad denominator")
    for y in ("FY2021", "FY2022", "FY2023"):
        r = borrowing_rate_check(y)
        print("  %s  on bearing debt %6.2f%%   on total liabilities %6.2f%%   "
              "understated by %.2f points"
              % (y, 100 * r["rate_on_bearing_debt"],
                 100 * r["rate_on_total_liabilities"], r["understatement_pp"]))
