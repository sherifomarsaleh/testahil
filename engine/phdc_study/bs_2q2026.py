"""PHD's reviewed consolidated statements at 30 June 2026, read and FOOTED.

SUPPLIED BY THE PRINCIPAL 17-09-2026 after this session established it could not be
reached from the container: the IR result centre carries no 1H2026 release, and the EGX
disclosure feed embedded on the company's own site puts its data API on port 8080, which
this environment's network policy resets. [R-IND-01]'s ladder ended there, and the
principal supplying the document IS the rule working rather than a failure of it.

WHAT IT IS: "Periodic Consolidated Financial Statements On 30 June 2026 Together with
Limited Review Report", Mostafa Shawki / Forvis Mazars. A SCANNED document -- 70 bytes of
text layer across 70 pages, produced by a Xerox scanner, created 17 August and modified
18 August 2026, which matches the 18-August lodgement the external returns reported.
Read by OCR off the rendered pixels and held to the statements' OWN arithmetic.

ARITHMETIC IS THE ARBITER, NOT THE EXTRACTOR'S CONFIDENCE, AND IT EARNED ITS KEEP TWICE:
  * the cash-flow statement printed investing as "(495 865 155)" and its own components
    sum to -3,495,865,155 -- A DROPPED LEADING DIGIT. With it restored, operating plus
    investing plus financing reproduces the stated net movement EXACTLY, and the closing
    balance ties to the balance sheet to the pound. Read as printed, it would have
    overstated free cash by three billion pounds.
  * the 31-December-2025 comparative column is out by exactly 4,000,000, which locates a
    single misread digit in current assets rather than condemning the column.
Both are recorded rather than silently corrected, because a reader is entitled to know
which figures were read and which were recovered.
"""
import os

SOURCE = ("PHD periodic consolidated financial statements on 30 June 2026 with limited "
          "review report (Mostafa Shawki / Forvis Mazars), supplied by the principal "
          "17-09-2026; scan with no text layer, read by OCR off the rendered pixels at "
          "190dpi with the two disputed liability rows re-read at 400dpi")
AS_AT = "2026-06-30"

# ---- CONSOLIDATED FINANCIAL POSITION, 30 June 2026 (EGP) --------------------------
BS = dict(
    investments_assoc=3_898_477_847, subordinated_loan_assoc=34_333_473,
    investment_property=1_008_419_552, fixed_assets=5_637_373_917,
    total_noncurrent_assets=67_800_794_295,
    work_in_progress=23_915_930_580, accounts_receivable=35_055_008_362,
    debtors_other=14_932_335_834, suppliers_advances=10_490_853_035,
    fin_inv_amortised=13_016_407_445, inv_fair_value=179_503_696,
    notes_recv_st=20_530_518_157, notes_recv_st_undel=695_420_618,
    cash=7_804_246_906,
    total_current_assets=126_966_492_432, total_assets=194_767_286_727,
    equity_parent=18_910_859_404, nci_equity=1_723_048_810,
    total_equity=20_633_908_214,
    # the eight lines the study's OWN gross-debt definition sums, verified by
    # reproducing its committed 31-Mar-2026 figure of 32,369.847 from the same eight
    loans_long_term=10_236_280_237, notes_payable_long_term=4_016_714_644,
    lease_liabilities_lt=78_329_645, banks_credit_balances=1_529_842_495,
    credit_facilities=13_922_422_891, current_portion_st_loans=650_151_650,
    notes_payable_short_term=4_778_461_505, lease_liabilities_st=63_263_828,
    # the rest of the non-current side, carried so the subtotal can be footed
    land_purchase_liab_lt=47_134_741, residents_association_lt=34_337_384_836,
    deferred_tax_liab=42_575_123, joint_shares_lt=3_530_990_688,
    total_noncurrent_liabs=52_289_409_914,
    total_current_liabs=121_843_968_599, total_liabilities=174_133_378_513,
)
DEBT_LINES = ("loans_long_term", "notes_payable_long_term", "lease_liabilities_lt",
              "banks_credit_balances", "credit_facilities", "current_portion_st_loans",
              "notes_payable_short_term", "lease_liabilities_st")

# ---- CONSOLIDATED STATEMENT OF INCOME, six months to 30 June 2026 (EGP) -----------
IS = dict(
    revenue=19_528_117_727, cost_of_revenues=12_539_272_168, cash_discount=62_823_483,
    gross_profit=6_926_022_076,
    opex_total=4_782_297_260,            # the statement's own stated subtotal
    other_revenues_total=994_053_646,
    amortization_discount_notes=523_193_960, gain_fv_investments=15_253_619,
    credit_interest_amortised_cost=455_606_067,
    npbt=3_137_778_462, current_tax=844_118_629, deferred_tax=1_133_557,
    npat_before_nci=2_292_526_276, nci_share=27_703_559, npat_after_nci=2_264_822_717,
)
IS_PRIOR = dict(revenue=15_879_129_165, gross_profit=6_664_688_497,
                npat_before_nci=2_582_379_370, npat_after_nci=2_443_380_942)

# ---- CONSOLIDATED STATEMENT OF CASH FLOWS, six months to 30 June 2026 (EGP) -------
CF = dict(
    operating=1_499_068_217,
    investing=-3_495_865_155,            # RECOVERED from its own components, see above
    investing_as_printed=-495_865_155,   # what the page shows; kept so the repair is visible
    financing=254_599_656,
    net_movement=-1_742_197_282,
    opening_cash=9_419_526_159, closing_cash=7_804_246_906,
    adj_retained=25_338_062, fx_translation=101_285_488, ecl_effect=294_479,
)

def check():
    """Every total reproduces from the lines printed above it, or this refuses."""
    out = []
    a = BS["total_noncurrent_assets"] + BS["total_current_assets"]
    assert a == BS["total_assets"], (a, BS["total_assets"])
    out.append(("balance sheet: non-current + current = total assets", a))
    b = BS["total_equity"] + BS["total_liabilities"]
    assert b == BS["total_assets"], (b, BS["total_assets"])
    out.append(("balance sheet: equity + liabilities = total assets", b))
    assert BS["equity_parent"] + BS["nci_equity"] == BS["total_equity"]
    out.append(("equity: parent + non-controlling", BS["total_equity"]))
    nc = (BS["loans_long_term"] + BS["notes_payable_long_term"] + BS["land_purchase_liab_lt"]
          + BS["residents_association_lt"] + BS["deferred_tax_liab"]
          + BS["lease_liabilities_lt"] + BS["joint_shares_lt"])
    assert nc == BS["total_noncurrent_liabs"], (nc, BS["total_noncurrent_liabs"])
    out.append(("non-current liabilities foot to their own subtotal", nc))
    g = IS["revenue"] - IS["cost_of_revenues"] - IS["cash_discount"]
    assert g == IS["gross_profit"], (g, IS["gross_profit"])
    out.append(("income: revenue - cost - discount = gross profit", g))
    o = (IS["amortization_discount_notes"] + IS["gain_fv_investments"]
         + IS["credit_interest_amortised_cost"])
    assert o == IS["other_revenues_total"]
    out.append(("income: other revenues foot", o))
    p = IS["gross_profit"] - IS["opex_total"] + IS["other_revenues_total"]
    assert p == IS["npbt"], (p, IS["npbt"])
    out.append(("income: gross - expenses + other = profit before tax", p))
    n = IS["npbt"] - IS["current_tax"] - IS["deferred_tax"]
    assert n == IS["npat_before_nci"]
    out.append(("income: profit after tax before minority", n))
    assert n - IS["nci_share"] == IS["npat_after_nci"]
    out.append(("income: profit after minority", IS["npat_after_nci"]))
    m = CF["operating"] + CF["investing"] + CF["financing"]
    assert m == CF["net_movement"], (m, CF["net_movement"])
    out.append(("cash flow: the three activities reproduce the net movement", m))
    c = (CF["opening_cash"] + CF["net_movement"] + CF["adj_retained"]
         + CF["fx_translation"] + CF["ecl_effect"])
    assert c == CF["closing_cash"] == BS["cash"], (c, CF["closing_cash"], BS["cash"])
    out.append(("cash flow ties to the balance sheet's own cash", c))
    return out

def gross_debt_egp_mn():
    return sum(BS[k] for k in DEBT_LINES) / 1e6

def net_debt_egp_mn():
    return gross_debt_egp_mn() - BS["cash"] / 1e6

if __name__ == "__main__":
    for name, v in check():
        print(f"  OK  {name:<58} {v:>20,}")
    print()
    print(f"  gross debt   {gross_debt_egp_mn():>12,.3f} EGP mn")
    print(f"  cash         {BS['cash']/1e6:>12,.3f}")
    print(f"  NET DEBT     {net_debt_egp_mn():>12,.3f}")
    print(f"  minority (book) {BS['nci_equity']/1e6:>9,.3f}")
    print(f"  associates   {BS['investments_assoc']/1e6:>12,.3f}   "
          f"investment property {BS['investment_property']/1e6:,.3f}")
    print()
    print(f"  1H2026 gross margin  {IS['gross_profit']/IS['revenue']*100:>6.2f}%   "
          f"1H2025 {IS_PRIOR['gross_profit']/IS_PRIOR['revenue']*100:.2f}%")
    print(f"  revenue YoY          {IS['revenue']/IS_PRIOR['revenue']*100-100:>6.2f}%")
    print(f"  profit YoY, after minority {IS['npat_after_nci']/IS_PRIOR['npat_after_nci']*100-100:>6.2f}%"
          f"   before minority {IS['npat_before_nci']/IS_PRIOR['npat_before_nci']*100-100:.2f}%")
    print(f"  OPERATING CASH FLOW / REVENUE  {CF['operating']/IS['revenue']*100:>6.2f}%")
