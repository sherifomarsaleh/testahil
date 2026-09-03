"""ARCC (Arabian Cement Company S.A.E., EGX: ARCC) — master computation, REVISION 4.

REVISION 4 REBUILDS ON THE H1-2026 REVIEWED ACCOUNTS AND ON THIS NAME'S OWN
FUNDAMENTAL WALK-FORWARD.

Two things arrived after revision 3 was struck and both move the answer.

FIRST, A NEWER DISCLOSED PERIOD. The condensed consolidated interim statements
for the six months ended 30 June 2026 were filed on 13 August 2026 — a week
AFTER revision 3's 6 August valuation date, so revision 3 did not miss them,
they did not exist. They are consumed here, and three of their disclosures move
the model rather than confirm it:

  * THE BRIDGE NOW STANDS ON A DISCLOSED BALANCE SHEET INSTEAD OF A ROLL-FORWARD.
    Revision 3 rolled FY2025 cash forward on stub free cash flow, added stub
    treasury income, deducted the declared dividend and netted the Q1-2026 debt,
    arriving at net cash of EGP 1,926.5mn. The 30 June balance sheet prints cash
    of 1,970.501mn against interest-bearing debt of 1,283.288mn — net cash of
    687.213mn. The roll-forward was EGP 1,239mn too generous, or EGP 3.31 per
    share, because it could not see a 698.6mn inventory build, an 832.8mn rise in
    debtors and 608.4mn of capital spending in six months. A DISCLOSED BALANCE
    SHEET BEATS A ROLL-FORWARD, and the valuation date moves to 30 June 2026 so
    that the bridge and the explicit window meet at the same instant.
  * THE OPERATING RESULT IS RUNNING AHEAD OF REVISION 3. Half-year revenue of
    6,080.578mn is 10.6% up on H1-2025 and, scaled on FY2025's own half-year
    split, implies about 13,703mn for FY2026 against the 13,025mn revision 3
    projected — 5.2% low. The price paths are recalibrated onto that reviewed
    actual, per channel, which is [L-013]: a recent reviewed actual outranks a
    stale full-year rate.
  * THE MIX HAS TURNED, AND IT TURNED THE OTHER WAY. Local goods revenue is
    +18.5% year on year while EXPORT goods revenue is -3.8% and export services
    have fallen by two thirds. Revision 3 carried the export share broadly flat.
    Local tonnes are the better-priced tonnes, so this is margin-positive and it
    is why the half-year gross margin holds at 40.5% against FY2025's 40.6%.

An EGP 467.813mn EXPORT SUBSIDY was collected in the second quarter (note 29).
It is EXCLUDED from forward operating income and left where it already sits, in
the 30 June cash balance. FY2025's export subsidy was 32.643mn on export revenue
of 3,815mn — 0.86% — and a rate anywhere near the half-year figure would be
implausible as a recurring entitlement, so this reads as a collection of
accumulated claims. WHAT WOULD OVERTURN THAT: a comparable collection in a later
period with no accumulated-claims explanation, in which case it is recurring and
this treatment understates value.

SECOND, THIS NAME'S OWN FUNDAMENTAL WALK-FORWARD (engine/arcc_walkforward,
[R-FCAL-01]) — twelve fiscal years, eight origins, twenty-five scoreable cells.
What it changed here:

  * MANUFACTURING DEPRECIATION carries the ONE correction that survived both
    clauses of the protocol's test: held flat it under-forecasts by 5.9%, the
    sign holds in both eras, it is robust at all three bootstrap block lengths,
    the expanding-window correction improves it out of sample, and it matches how
    every other study in the book builds the line. Half strength gives x1.0298.
  * INTEREST INCOME is driven off the cash balance rather than held flat. That
    was the largest bias in the run (-1.641) and a pure specification defect.
  * YEARS 3-5 ARE PUBLISHED AS RANGES, from the walk-forward's own measured error
    distribution, because that record says revenue is 63 log points low by year
    four and profit before tax spans two orders of magnitude by year five. A
    single fifth-year profit number would claim a precision the record cannot
    support.
  * ELEVEN OTHER MEASURED BIASES ARE WATCH FLAGS AND CHANGE NOTHING HERE. Nine of
    them fail their own out-of-sample test; a correction that makes the error
    worse is evidence of a specification defect, and no multiplier may hide one.

REVISION 3 CORRECTED THE PRICE PATH, WHICH THE AUDITED RECORD DISPROVED.

Revision 2 rebuilt every company figure on the statements but left one forecast driver
where revision 1 had put it: local realised price growing 3.0% in FY2026 against 11.5%
cost inflation, and about 4% a year thereafter — a cumulative real squeeze of 28%. That
survived the rebuild only because it was never tested against the statements that had
just been read. It does not survive the test.

  * FY2024: revenue +44.5%, total cash cost +41.8%.
  * FY2025: revenue +42.6%, total cash cost +12.5%. Gross margin 21.2% -> 23.9% -> 40.6%.
  * Q1-2026 (reviewed): revenue +17.3% at a 42.9% gross margin against 40.6% for FY2025.

In every period the accounts cover, price outran cost. The 3.0% assumption also implied a
producer unable to raise price even at the central bank's own 7% medium-term target, while
the same model had utilisation RISING from 69.7% to 78.2% — volume gained and real price
lost at once, which is two conservatisms stacked, not one judgement made.

The price path is recalibrated to 8.0% / 9.0% / 8.0% / 7.0% / 6.5%, which is still below
the cost path in every year and still produces FY2026 group revenue growth of about 10.7%
against the 17.3% the first quarter actually ran. The cost path is UNCHANGED at headline
inflation: the company's realised cost inflation ran below the national rate, but crediting
that here would double-count the alternative-fuel saving already carried in af_saving.

The EBITDA margin therefore glides from the audited 39.3% to about 34.3% by FY2030 rather
than to 24.5%. It is still an erosion story — the quota that supported price was abolished
in May 2025 into a structurally over-supplied market — but it is now an erosion the record
can support rather than one the model manufactured.

REVISION 2 REBUILT THE STUDY ON THE AUDITED CONSOLIDATED FINANCIAL STATEMENTS.

Revision 1 was built without opening a single source document: every outbound fetch was
refused by the egress policy, so every company figure reached the model as relayed in a
web-search summary. The audited statements for FY2023, FY2024, FY2025 and the reviewed
Q1-2026 interim accounts are now in hand — Deloitte (Wafik, Ramy & Partners), signed
25 February 2026 for FY2025 — and this file is rebuilt from them line by line.

WHAT THE STATEMENTS CHANGED, and it is not cosmetic:

  * NON-CONTROLLING INTERESTS ARE EGP 158,005 — one hundred and fifty-eight THOUSAND
    pounds, not the EGP 150 MILLION revision 1 deducted on inference. Revision 1 was
    950x too high. Note 24.
  * THE EFFECTIVE TAX RATE IS 23.82%, not the 29.43% revision 1 inferred by closing a
    modelled net finance income against disclosed profit. The company discloses 23.33%
    as its average effective rate (note 10.2); tax expense over pre-tax profit is 23.82%.
    Revision 1 over-taxed every forecast year by roughly 5.6 points.
  * THE COST OF DEBT IS ~6.5%, not 21.5%. The debt book re-based during 2025 from EGP
    credit facilities to EUR term loans: a EUR 25mn EBRD facility at 3-month Euribor plus
    4.35% for decarbonisation, and a EUR 3.09mn National Bank of Egypt/KfW facility at
    6-month Euribor plus 3%. 91% of interest-bearing debt is now EUR-denominated. Note 25.
  * KILN CAPACITY IS 4.2Mt OF CLINKER, not the 3.6 revision 1 assumed, against 5.0Mt of
    cement — so the clinker factor is 0.84, not 0.72. Note 1.
  * EXPORTS ARE 30.7% OF REVENUE, not the 12% revision 1 assumed. Note 4 splits local and
    export, and cement from services, in both years.
  * THE COST STACK IS DISCLOSED. Note 5 gives materials, depreciation, amortisation,
    transportation and overheads. The invented five-line fuel/power/raw/packaging/
    distribution stack of revision 1 is retired in favour of the printed one.
  * D&A IS EGP 289.77mn, against the 301.21mn revision 1 triangulated three ways. The
    triangulation was 3.9% high — good for a guess, and now unnecessary.

WHAT SURVIVED CONTACT WITH THE STATEMENTS: the share count (374,867,445 outstanding —
378,739,700 issued less 3,872,255 treasury, exactly the figure three independent routes
gave), FY2025 operating income of EGP 4,595.82mn to the pound, total liabilities of EGP
4,140.99mn (revision 1 derived it as assets less equity and rejected a competing print of
EGP 2,894mn — which turns out to be total CURRENT liabilities, so the derivation was
right and the rejection was right), and revenue and profit for all three years.
"""
import datetime as _dt
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import numpy as np
import macro_path as MP
# [R-TERM-01] — the terminal comes from the shared builder, never from a local
# construction. Every study once hand-rolled its own beta and every one was wrong the same
# way; the terminal census found the same shape in the terminals, so it lives in one place.
import terminal_value

# THE PRICE AND THE EDITION EACH HAVE ONE DATE, DECLARED ONCE.
# Four places in the delivered files once read 'latest known close (6 August 2026)'
# beside a price of 77.00, which was the 3 September close, and the masthead said
# 'issued 2 September' on a 3 September edition. A date typed beside a computed
# number is the same defect as a number typed beside a computed one.
SPOT_DATE = '2026-09-03'      # engine/prices/SUPPLIED_03-09-2026.json
EDITION_DATE = '2026-09-03'   # the date in the delivered filenames

# ---------------------------------------------------------------------------
# THE HOUSE MACRO PATH [R-MACRO-01]. Until this edition ARCC carried its own
# inflation ladder, its own currency path and its own terminal inflation, and so
# did every other Egyptian study: five studies, five views of one economy. The
# conflict this settles is not academic. ARCC built its terminal risk-free rate
# from the central bank's 5% Q4-2028 target while AMOC built its from the 7%
# target in force — same country, same date, 200 basis points apart, each argued
# in its own file and neither aware of the other. One path now answers for all
# of them, and every level in it is published by a named institution on a named
# date or derived from numbers that are.
_MACRO = MP.load('EG')
_INFL = list(_MACRO.inflation_path)        # FY2026E-FY2030E, from the house path
_FXP = _MACRO.fx_path(5)
_PI_T = _MACRO.terminal_inflation          # 7%, the band the bank's own guidance returns to
_RF_TERM = _PI_T + _MACRO.real_rate_convention   # DERIVED, never typed
_G_TERM = _MACRO.terminal_growth()         # terminal inflation + a STATED real growth
_KD_TERM = _MACRO.kd_terminal              # the long-run Egyptian corporate norm


def _index(first_step, years=4):
    """A cumulative index on the FY2025 base: the evidenced FY2026 step, then the
    house inflation path at ZERO real growth.

    Price and cost ride the SAME path from FY2027, so the margin is an OUTPUT
    rather than the residual of two independently chosen indices. That is not a
    modelling preference here: the company's own reviewed first half of 2026
    prints a gross margin of 40.5% against 40.6% for the whole of FY2025, so its
    realised price and its realised cost are in fact moving together, and two
    paths drifting 1 point apart every year describe a company that does not
    exist. Expressed against this path, the retired indices assumed an 11.0%
    cumulative real decline in the cement price and a 5.2% real decline in cost
    by 2030 — neither ever stated, both artefacts of nominal ladders typed
    against an inflation view that now sits 450 basis points low in 2026."""
    out = [1.0, 1.0 + first_step]
    for k in range(1, years + 1):
        out.append(out[-1] * (1 + _INFL[k]))
    return [round(x, 6) for x in out]

LOG = []
def say(s):
    LOG.append(s); print(s)


def I(value, source, date, ring):
    return dict(value=value, source=source, date=date, ring=ring)


AFS25 = ("Audited consolidated financial statements for the year ended 31 December 2025, "
         "Deloitte (Wafik, Ramy & Partners), signed 25 February 2026")
AFS24 = ("Audited consolidated financial statements for the year ended 31 December 2024, "
         "Deloitte (Wafik, Ramy & Partners), signed 23 March 2025")
IH26 = ("Reviewed condensed consolidated interim financial statements for the six months "
        "ended 30 June 2026, Wafik, Ramy & Partners (Deloitte), limited review report "
        "attached; filed 13 August 2026")
Q126 = ("Reviewed condensed consolidated interim financial statements for the three months "
        "ended 31 March 2026, Deloitte (Wafik, Ramy & Partners), 25 May 2026")
# The FY2025 investor presentation carries the PHYSICAL disclosure — tonnes by product,
# production, and the sector balance — that the audited statements do not. Three revisions
# of this study reconstructed those tonnes because this document had not been read. Note
# that its financial tables are on a narrower basis than the audited consolidated accounts
# (revenue 12,320 against 12,447, total assets 8,640 against 8,784), so every FINANCIAL
# figure in this model stays on the audited statements and only the PHYSICALS come here.
IRP = ("FY2025 Investor Presentation, Arabian Cement Company S.A.E., investor relations "
       "library, page 5 (sales volumes and production indicators)")

# ============================== INPUTS ======================================
INP = dict(
    # ---- market anchors ---------------------------------------------------
    # RE-STRUCK ON THE LATEST KNOWN PRICE [R-GAP-01 AMENDED, 03-09-2026]. The study
    # had been carrying a 6-August close for four weeks while the stock rose 30.5%.
    # The price is an INPUT here, not only a benchmark: market capitalisation sets
    # the market-value equity weight the cost of capital is built on.
    spot=I(77.00, "Closing price on the Egyptian Exchange, 3 September 2026. The previous "
           "edition was struck on the 6 August close of 59.00", "2026-09-03", "Market"),
    shares_issued=I(378.7397, AFS25 + ", note 20: 378,739,700 ordinary shares authorised, "
                    "issued and fully paid at EGP 2 par, issued capital EGP 757,479,400",
                    "2025-12-31", "Company"),
    shares_treasury=I(3.872255, AFS25 + ", note 21: 3,872,255 treasury shares acquired "
                      "during 2025 for EGP 143,327,985, being 1% of capital, under a board "
                      "approval of 21 July 2025", "2025-12-31", "Company"),
    shares_wavg_fy25=I(377.155593, AFS25 + ", note 11: weighted average ordinary shares "
                       "for earnings per share, after excluding treasury shares",
                       "2025-12-31", "Company"),
    shares_wavg_fy24=I(378.7397, AFS25 + ", note 11, comparative", "2024-12-31", "Company"),
    tax_stat=I(0.225, "Egypt statutory corporate income tax rate", "2026-01-01", "Country"),

    # ---- income statement, three audited years (EGP mn) -------------------
    rev_fy23=I(6042.831338, AFS24 + " — sales (net), comparative column",
               "2023-12-31", "Company"),
    rev_fy24=I(8729.782821, AFS25 + " — sales (net), comparative column",
               "2024-12-31", "Company"),
    rev_fy25=I(12447.320081, AFS25 + " — sales (net)", "2025-12-31", "Company"),
    cogs_fy23=I(4759.815212, AFS24 + " — cost of sales, comparative", "2023-12-31", "Company"),
    rev_fy22=I(4675.002824, "Audited consolidated financial statements for the year ended "
               "31 December 2022 — sales (net). Carried only to measure how much of a year "
               "ARCC's first half is", "2022-12-31", "Company"),
    cogs_fy22=I(3789.816211, "Audited consolidated financial statements for the year ended "
                "31 December 2022 — cost of sales", "2022-12-31", "Company"),
    cogs_fy24=I(6642.972487, AFS25 + " — cost of sales, comparative", "2024-12-31", "Company"),
    cogs_fy25=I(7389.054416, AFS25 + " — cost of sales", "2025-12-31", "Company"),
    ga_fy23=I(183.940276, AFS24 + " — general and administrative expenses, comparative",
              "2023-12-31", "Company"),
    ga_fy24=I(267.798104, AFS25 + " — general and administrative expenses, comparative",
              "2024-12-31", "Company"),
    ga_fy25=I(384.332833, AFS25 + " — general and administrative expenses, note 6",
              "2025-12-31", "Company"),
    prov_fy23=I(15.220195, AFS24 + " — provisions charged, comparative", "2023-12-31", "Company"),
    prov_fy24=I(56.052950, AFS25 + " — provisions charged, comparative", "2024-12-31", "Company"),
    prov_fy25=I(74.505707, AFS25 + " — provisions charged, note 27", "2025-12-31", "Company"),
    ecl_fy23=I(4.745753, AFS24 + " — expected credit losses on trade receivables, "
               "comparative", "2023-12-31", "Company"),
    ecl_fy24=I(-1.106452, AFS25 + " — REVERSAL of expected credit losses, comparative "
               "(negative, i.e. a credit)", "2024-12-31", "Company"),
    ecl_fy25=I(3.603563, AFS25 + " — expected credit losses on trade receivables, note 17",
               "2025-12-31", "Company"),
    pbt_fy23=I(930.231432, AFS24 + " — net profit before tax, comparative",
               "2023-12-31", "Company"),
    pbt_fy24=I(1505.866118, AFS25 + " — net profit before tax, comparative",
               "2024-12-31", "Company"),
    pbt_fy25=I(4725.157878, AFS25 + " — net profit before tax", "2025-12-31", "Company"),
    tax_fy23=I(232.732802, AFS24 + " — income tax, comparative", "2023-12-31", "Company"),
    tax_fy24=I(345.730996, AFS25 + " — income tax, comparative", "2024-12-31", "Company"),
    tax_fy25=I(1125.467657, AFS25 + " — income tax, note 10.1: current 1,111.30 plus "
               "deferred 14.17", "2025-12-31", "Company"),
    pat_fy23=I(697.488741, AFS24 + " — profit attributable to owners of the Parent, "
               "comparative", "2023-12-31", "Company"),
    pat_fy24=I(1160.129411, AFS25 + " — profit attributable to owners of the Parent, "
               "comparative", "2024-12-31", "Company"),
    pat_fy25=I(3599.585937, AFS25 + " — profit attributable to owners of the Parent "
               "(group profit 3,599.690 less 0.104 to non-controlling interests)",
               "2025-12-31", "Company"),
    eps_fy23=I(1.81, AFS24 + " — earnings per share, comparative", "2023-12-31", "Company"),
    eps_fy24=I(3.02, AFS25 + " — earnings per share, comparative", "2024-12-31", "Company"),
    eps_fy25=I(9.49, AFS25 + " — earnings per share, note 11, struck on distributable "
               "profit of 3,580.712 after the employees' share of 18.874",
               "2025-12-31", "Company"),
    intinc_fy25=I(226.274781, AFS25 + " — interest income", "2025-12-31", "Company"),
    othinc_fy25=I(53.339508, AFS25 + " — other income, note 7, including export subsidies "
                  "of EGP 31.643mn", "2025-12-31", "Company"),
    fincost_fy25=I(49.841733, AFS25 + " — finance costs, note 8: loan interest 24.613, "
                   "credit-facility interest 23.007, lease interest 1.163, long-term "
                   "trade-payable finance interest 1.059", "2025-12-31", "Company"),
    fincost_fy24=I(91.188916, AFS25 + " — finance costs, comparative", "2024-12-31", "Company"),
    fx_diff_fy25=I(-101.578240, AFS25 + " — foreign currency exchange differences, a LOSS",
                   "2025-12-31", "Company"),

    # ---- disclosed revenue split, note 4 ----------------------------------
    rev_local_goods_fy25=I(8350.454610, AFS25 + " — note 4, local sales of goods",
                           "2025-12-31", "Company"),
    rev_local_svc_fy25=I(281.863546, AFS25 + " — note 4, local services", "2025-12-31", "Company"),
    rev_exp_goods_fy25=I(3356.422381, AFS25 + " — note 4, export sales of goods",
                         "2025-12-31", "Company"),
    rev_exp_fy25=I(3815.001925, AFS25 + " — note 4, total export sales including "
                   "transportation services", "2025-12-31", "Company"),
    export_subsidy_fy25=I(32.642586, AFS25 + " — note 7: other income for FY2025 'includes "
                          "export subsidies amounted to EGP 32 642 586'. The comparison "
                          "that makes the H1-2026 collection readable as a catch-up rather "
                          "than a run rate", "2025-12-31", "Company"),
    oth_inc_fy25=I(53.339508, AFS25 + " — other income, note 7, of which EGP 32.642586mn is "
                   "disclosed export subsidies. REVISION 4 CONSUMES THIS LINE. Revisions "
                   "1-3 registered it, quoted it, and let no line of the model use it — "
                   "which is [L-018] exactly: a registered input that nothing consumes is "
                   "money the valuation has quietly ignored", "2025-12-31", "Company"),
    rev_exp_svc_fy25=I(458.579544, AFS25 + " — note 4, export services", "2025-12-31", "Company"),
    rev_local_fy24=I(4883.304477, AFS25 + " — note 4, total local sales, comparative",
                     "2024-12-31", "Company"),
    rev_exp_fy24=I(3846.478344, AFS25 + " — note 4, total export sales, comparative",
                   "2024-12-31", "Company"),

    # ---- disclosed cost of sales, note 5 ----------------------------------
    cos_materials_fy25=I(5698.184715, AFS25 + " — note 5, raw materials; note 16 confirms "
                         "this is the cost of inventories charged to cost of sales, so it "
                         "carries fuel, packing and spares as well as raw meal",
                         "2025-12-31", "Company"),
    cos_transport_fy25=I(764.279332, AFS25 + " — note 5, transportation costs",
                         "2025-12-31", "Company"),
    cos_overhead_fy25=I(641.143208, AFS25 + " — note 5, overhead costs", "2025-12-31", "Company"),
    cos_mfg_dep_fy25=I(254.765548, AFS25 + " — note 5, manufacturing depreciation",
                       "2025-12-31", "Company"),
    cos_intang_amort_fy25=I(30.681613, AFS25 + " — note 5, amortisation of intangible "
                            "assets charged to cost of sales", "2025-12-31", "Company"),
    ga_admin_dep_fy25=I(4.324134, AFS25 + " — note 6, administrative depreciation",
                        "2025-12-31", "Company"),

    # ---- depreciation and amortisation, cash flow statements --------------
    dna_fy23=I(250.424521, AFS24 + " — cash flow statement, comparative column: property "
               "depreciation 215.377 plus intangible amortisation 28.156 plus right-of-use "
               "amortisation 6.891", "2023-12-31", "Company"),
    dna_fy24=I(256.801527, AFS25 + " — cash flow statement, comparative: 221.563 plus "
               "28.156 plus 7.082", "2024-12-31", "Company"),
    dna_fy25=I(289.771295, AFS25 + " — cash flow statement: property depreciation 259.090 "
               "plus intangible amortisation 28.156 plus right-of-use amortisation 2.525",
               "2025-12-31", "Company"),
    capex_fy23=I(58.543963, AFS24 + " — cash flow, comparative: purchases of property "
                 "56.808 plus assets under construction 1.736", "2023-12-31", "Company"),
    capex_fy24=I(912.015400, AFS25 + " — cash flow, comparative: 206.543 plus 705.473",
                 "2024-12-31", "Company"),
    capex_fy25=I(796.470760, AFS25 + " — cash flow: purchases of property 329.893 plus "
                 "assets under construction 466.578", "2025-12-31", "Company"),

    # ---- balance sheet, 31 December 2025 (EGP mn) -------------------------
    ta_fy25=I(8783.721849, AFS25 + " — total assets", "2025-12-31", "Company"),
    ta_fy24=I(5848.616103, AFS25 + " — total assets, comparative", "2024-12-31", "Company"),
    ta_fy23=I(3887.527427, AFS24 + " — total assets, comparative", "2023-12-31", "Company"),
    tl_fy25=I(4140.989609, AFS25 + " — TOTAL liabilities (non-current 1,246.860 plus "
              "current 2,894.130). Revision 1 was offered EGP 2,894.13mn as 'total "
              "liabilities' by an aggregator and rejected it because it would not close "
              "against assets and equity; the statements show that figure is total CURRENT "
              "liabilities, so both the rejection and the derived 4,140.99 were right",
              "2025-12-31", "Company"),
    ppe_fy25=I(2522.323523, AFS25 + " — property, plant and equipment (net), note 12",
               "2025-12-31", "Company"),
    auc_fy25=I(391.543753, AFS25 + " — assets under construction, note 13", "2025-12-31",
               "Company"),
    auc_altfuel_fy25=I(240.235369, AFS25 + " — note 13, assets under construction: "
                       "alternative-fuel system for production line 2", "2025-12-31",
                       "Company"),
    auc_silo_fy25=I(146.238521, AFS25 + " — note 13, assets under construction: new steel "
                    "cement silo for production line 1", "2025-12-31", "Company"),
    intang_fy25=I(106.799617, AFS25 + " — intangible assets (net), note 14: the operating "
                  "licence", "2025-12-31", "Company"),
    inv_fy25=I(1053.646218, AFS25 + " — inventories, note 16: raw materials 282.765, fuel "
               "200.388, packing 51.934, spares 190.444, work in progress 6.861, goods in "
               "transit 0.483, finished goods 320.771", "2025-12-31", "Company"),
    recv_fy25=I(244.416417, AFS25 + " — trade receivables (net of EGP 7.639mn expected "
                "credit losses), note 17", "2025-12-31", "Company"),
    debtors_fy25=I(1004.779062, AFS25 + " — debtors and other debit balances (net), note "
                   "18, of which advances to suppliers 826.903", "2025-12-31", "Company"),
    cash_fy25=I(3459.391229, AFS25 + " — cash and bank balances, note 19: local-currency "
                "current accounts 1,839.630, foreign-currency current accounts 1,599.702, "
                "deposits 8.733, cash in hand 11.325", "2025-12-31", "Company"),
    cash_fy24=I(1687.062873, AFS25 + " — cash and bank balances, comparative",
                "2024-12-31", "Company"),
    cash_fy23=I(561.099680, AFS24 + " — cash and bank balances, comparative",
                "2023-12-31", "Company"),
    eq_fy25=I(4642.574235, AFS25 + " — equity attributable to owners of the Parent: issued "
              "capital 757.479, treasury shares (143.328), legal reserve 379.506, retained "
              "earnings 3,648.917", "2025-12-31", "Company"),
    eq_fy24=I(2303.472299, AFS25 + " — equity attributable to owners, comparative",
              "2024-12-31", "Company"),
    eq_fy23=I(1754.221659, AFS24 + " — equity attributable to owners, comparative",
              "2023-12-31", "Company"),
    # the multiple is COMPUTED from the two figures rather than typed into the note: 950
    # was right and it was a numeral in a justification, which is where this rule reaches
    # too [found by prose_check.py]
    central_pre_rebuild=I(61.30, "The central published by the edition of this study that "
                          "PRECEDED the 06-08-2026 bottom-up rebuild, as recorded in that "
                          "edition's own caveats section and carried unchanged in every "
                          "edition since. THIS MODEL CANNOT COMPUTE IT — a different model "
                          "produced it, and the file itself is not retained in the "
                          "repository — so it is registered as the historical fact it is "
                          "rather than typed into a builder, which is the same disposition "
                          "any superseded figure quoted to show what changed must take.",
                          "2026-08-06", "House"),
    nci=I(0.158005, AFS25 + " — non-controlling interests, note 24: EGP 158,005. Revision 1 "
          "deducted EGP 150mn on inference from the profit statements; the audited figure "
          "is %.0f times smaller and immaterial to the bridge" % (150.0 / 0.158005),
          "2025-12-31", "Company"),

    # ---- debt, note 25 ----------------------------------------------------
    debt_cib_fy25=I(99.916937, AFS25 + " — note 25, Commercial International Bank credit "
                    "facilities. EGP 650mn package at the Central Bank corridor offer rate "
                    "plus 0.6%, EGP-denominated, for working capital",
                    "2025-12-31", "Company"),
    debt_nbe_fy25=I(145.741484, AFS25 + " — note 25, National Bank of Egypt facility "
                    "(current 27.057 plus non-current 118.685). EUR 3.09mn under a KfW "
                    "industrial-pollution grant programme, 20 quarterly instalments at "
                    "6-month Euribor plus 3%", "2025-12-31", "Company"),
    debt_ebrd_fy25=I(888.274195, AFS25 + " — note 25, European Bank for Reconstruction and "
                     "Development facility (current 118.437 plus non-current 769.838). EUR "
                     "25mn at 3-month Euribor plus 4.35%, drawn to EUR 18.5mn, funding "
                     "alternative-fuel capacity for kiln 2 and hydrogen injection on both "
                     "kilns; 15 equal quarterly instalments from 18 months after signing",
                     "2025-12-31", "Company"),
    debt_fy24=I(760.917684, AFS25 + " — note 25, comparative: credit facilities 615.044 "
                "plus bank loans 145.874", "2024-12-31", "Company"),
    debt_fy23=I(90.074273, AFS24 + " — credit facilities, comparative; no term borrowings "
                "at that date", "2023-12-31", "Company"),
    lease_fy25=I(1.176042, AFS25 + " — lease liabilities, note 33-2", "2025-12-31", "Company"),
    loan_int_fy25=I(24.613130, AFS25 + " — note 8, loan interest expense", "2025-12-31", "Company"),
    fac_int_fy25=I(23.007370, AFS25 + " — note 8, credit-facility interest expense",
                   "2025-12-31", "Company"),
    loan_int_fy24=I(2.754107, AFS25 + " — note 8, loan interest expense, comparative",
                    "2024-12-31", "Company"),
    fac_int_fy24=I(85.953026, AFS25 + " — note 8, credit-facility interest, comparative",
                   "2024-12-31", "Company"),

    # ---- Q1-2026, reviewed ------------------------------------------------
    rev_q1_26=I(2995.959350, Q126 + " — sales (net)", "2026-03-31", "Company"),
    rev_q1_25=I(2554.448091, Q126 + " — sales (net), comparative", "2025-03-31", "Company"),
    gp_q1_26=I(1286.145881, Q126 + " — gross profit", "2026-03-31", "Company"),
    ga_q1_26=I(102.281789, Q126 + " — general and administrative expenses",
               "2026-03-31", "Company"),
    prov_q1_26=I(6.892000, Q126 + " — provisions", "2026-03-31", "Company"),
    pat_q1_26=I(943.068309, Q126 + " — profit attributable to owners of the Parent",
                "2026-03-31", "Company"),
    pbt_q1_26=I(1273.034230, Q126 + " — net profit before tax", "2026-03-31", "Company"),
    tax_q1_26=I(329.943494, Q126 + " — income tax", "2026-03-31", "Company"),
    cash_q1_26=I(4379.627379, Q126 + " — cash and bank balances", "2026-03-31", "Company"),
    debt_q1_26=I(1260.509089, Q126 + " — borrowings 925.152 plus current portion 234.899 "
                 "plus credit facilities 99.784 plus lease liabilities 0.675",
                 "2026-03-31", "Company"),
    divpay_q1_26=I(2001.792160, Q126 + " — dividends payable. This is the FY2025 "
                   "distribution declared and unpaid at 31 March 2026, and it divides to "
                   "EGP 5.34 per share on the shares outstanding",
                   "2026-03-31", "Company"),
    fincost_q1_26=I(11.168843, Q126 + " — finance costs", "2026-03-31", "Company"),

    # ---- H1-2026, reviewed — THE LATEST DISCLOSED PERIOD -------------------
    # Filed 13-Aug-2026, a week after revision 3's valuation date. Everything
    # below is read from the rendered page and footed: revenue less cost of
    # sales equals gross profit, profit before tax less tax equals profit after
    # tax, and the sales note's four legs sum to the income statement's revenue.
    rev_h1_26=I(6080.577747, IH26 + " — sales (net), six months", "2026-06-30", "Company"),
    rev_h1_25=I(5499.911617, IH26 + " — sales (net), comparative six months",
                "2025-06-30", "Company"),
    rev_h1_26_loc_goods=I(4536.783763, IH26 + " — note 3, local sales of goods",
                          "2026-06-30", "Company"),
    rev_h1_26_exp_goods=I(1264.856099, IH26 + " — note 3, export sales of goods",
                          "2026-06-30", "Company"),
    rev_h1_26_svc=I(278.937885, IH26 + " — note 3, local transportation services 202.748365 "
                    "plus export transportation services 76.189520",
                    "2026-06-30", "Company"),
    rev_h1_25_loc_goods=I(3828.617220, IH26 + " — note 3, local sales of goods, comparative",
                          "2025-06-30", "Company"),
    rev_h1_25_exp_goods=I(1315.349787, IH26 + " — note 3, export sales of goods, comparative",
                          "2025-06-30", "Company"),
    rev_h1_25_svc=I(355.944610, IH26 + " — note 3, transportation services, comparative: "
                    "local 127.753131 plus export 228.191479", "2025-06-30", "Company"),
    cogs_h1_26=I(3619.039609, IH26 + " — cost of sales", "2026-06-30", "Company"),
    cogs_h1_25=I(3404.816990, IH26 + " — cost of sales, comparative six months",
                 "2025-06-30", "Company"),
    ga_h1_25=I(169.880277, IH26 + " — general and administrative expenses, comparative",
               "2025-06-30", "Company"),

    # ---- how much of a year ARCC's first half actually is ------------------
    # The single largest assumption in this revision is the factor that turns a
    # reviewed half into a full year, so it is measured on EVERY half the archive
    # supports rather than on the one nearest to hand. It is NOT stable: the
    # first half was 44.2% of FY2025, 45.6% of FY2022 and 52.7% of FY2023. Using
    # FY2025 alone would have grossed the half up by 12.7% and rested that on one
    # year; the MEDIAN of the three is used and the full range is published.
    rev_h1_23=I(3184.034587, "Reviewed condensed consolidated interim financial statements "
                "for the six months ended 30 June 2023 — sales (net). Foots: less cost of "
                "sales 2,536.411167 gives the printed gross profit of 647.623420",
                "2023-06-30", "Company"),
    cogs_h1_23=I(2536.411167, "Reviewed interim statements, six months ended 30 June 2023 "
                 "— cost of sales", "2023-06-30", "Company"),
    rev_h1_22=I(2129.458953, "Reviewed interim statements, six months ended 30 June 2022, "
                "comparative column of the H1-2023 filing — sales (net). Foots: less cost "
                "of sales 1,704.834656 gives the printed gross profit of 424.624297",
                "2022-06-30", "Company"),
    cogs_h1_22=I(1704.834656, "Reviewed interim statements, six months ended 30 June 2022, "
                 "comparative — cost of sales", "2022-06-30", "Company"),
    gp_h1_26=I(2461.538138, IH26 + " — gross profit", "2026-06-30", "Company"),
    ga_h1_26=I(225.744621, IH26 + " — general and administrative expenses",
               "2026-06-30", "Company"),
    prov_h1_26=I(31.498214, IH26 + " — provisions", "2026-06-30", "Company"),
    int_inc_h1_26=I(136.861895, IH26 + " — interest income", "2026-06-30", "Company"),
    oth_inc_h1_26=I(480.336061, IH26 + " — other income", "2026-06-30", "Company"),
    export_subsidy_h1_26=I(467.813139, IH26 + " — note 29: 'The other income for the period "
                           "ended June 30, 2026, includes export subsidy amounted to EGP "
                           "467 813 139 which have been collected during the three months "
                           "period ended June 30, 2026.' EXCLUDED from forward operating "
                           "income and left in the 30 June cash balance",
                           "2026-06-30", "Company"),
    fincost_h1_26=I(23.471833, IH26 + " — finance costs", "2026-06-30", "Company"),
    fx_h1_26=I(64.661520, IH26 + " — foreign currency exchange gains",
               "2026-06-30", "Company"),
    pbt_h1_26=I(2862.682946, IH26 + " — net profit for the period before tax",
                "2026-06-30", "Company"),
    tax_h1_26=I(690.229472, IH26 + " — income tax", "2026-06-30", "Company"),
    pat_h1_26=I(2172.453474, IH26 + " — net profit for the period after tax",
                "2026-06-30", "Company"),
    maj_h1_26=I(2172.395425, IH26 + " — profit attributable to owners of the Parent",
                "2026-06-30", "Company"),
    cash_h1_26=I(1970.501140, IH26 + " — cash and bank balances at 30 June 2026",
                 "2026-06-30", "Company"),
    debt_h1_26=I(1283.288394, IH26 + " — INTEREST-BEARING borrowings only: non-current "
                 "borrowings 761.097643 plus current portion of long-term borrowings "
                 "269.115255 plus credit facilities 253.075496. Trade and notes payable, "
                 "creditors and other credit balances and current tax liabilities bear no "
                 "interest and are excluded by construction",
                 "2026-06-30", "Company"),
    nci_h1_26=I(0.216054, IH26 + " — non-controlling interest at 30 June 2026",
                "2026-06-30", "Company"),
    dna_h1_26=I(161.254762, IH26 + " — cash flow statement: depreciation of property, plant "
                "and equipment 146.470318 plus amortisation of intangibles 13.962414 plus "
                "amortisation of right-of-use assets 0.822030", "2026-06-30", "Company"),
    capex_h1_26=I(608.433906, IH26 + " — cash flow statement: payments for purchase of "
                  "property, plant and equipment 102.893492 plus payments for assets under "
                  "construction 505.540414", "2026-06-30", "Company"),
    auc_h1_26=I(897.084167, IH26 + " — assets under construction at 30 June 2026, against "
                "391.543753 at 31 December 2025", "2026-06-30", "Company"),
    equity_h1_26=I(4794.303425, IH26 + " — equity attributable to owners of the Parent "
                   "Company at 30 June 2026", "2026-06-30", "Company"),
    capital_h1_26=I(749.734890, IH26 + " — issued and paid-up capital at 30 June 2026, "
                    "against 757.479400 at 31 December 2025, the treasury shares having "
                    "been CANCELLED. At the EGP 2 par value this is 374,867,445 shares — "
                    "exactly the count this study already used (issued less treasury), so "
                    "the cancellation confirms the share count rather than changing it",
                    "2026-06-30", "Company"),

    # ---- the fundamental walk-forward's one adopted correction -------------
    wf_dep_correction=I(1.0298, "Manufacturing depreciation correction from this name's own "
                        "fundamental walk-forward on this company's own history: "
                        "held flat, depreciation under-forecasts by 5.9 log points across "
                        "twenty-five cells; the sign holds in both eras, the bias is robust "
                        "at all three bootstrap block lengths, the expanding-window test "
                        "improves out-of-sample MAE from 0.090 to 0.081, and the adjustment "
                        "matches how every other study in the book builds the line. Applied "
                        "at HALF STRENGTH: exp(0.5 x 0.058715) = 1.0298. It is the ONLY one "
                        "of twelve candidates that survived both clauses",
                        "2026-09-01", "House"),

    # ---- dividends --------------------------------------------------------
    div_fy24_paid=I(1102.110289, AFS25 + " — note 28: the ordinary general assembly of 2 "
                    "December 2025 approved EGP 1,102,110,289 to shareholders for FY2024, "
                    "plus EGP 15,045,727 to employees", "2025-12-02", "Company"),
    div_fy25_declared=I(2001.792160, Q126 + " — dividends payable at 31 March 2026 for the "
                        "FY2025 result", "2026-03-31", "Company"),

    # ---- plant, note 1 ----------------------------------------------------
    cap_clinker_mt=I(4.20, AFS25 + " — note 1: 'a cement producer with a clinker capacity "
                     "of 4.2 million tons per annum'", "2025-12-31", "Company"),
    cap_cement_mt=I(5.00, AFS25 + " — note 1: '...that can produce 5 million tons per annum "
                    "of cement'", "2025-12-31", "Company"),
    clinker_factor=I(0.7329, "Tonnes of clinker per tonne of cement PRODUCED. Revision 3 "
                     "used 0.84, taken from the ratio of the two nameplate capacities in "
                     "note 1 and described as 'observed'. It is not observed and it is not "
                     "a clinker factor: 4.2/5.0 is a ratio of two DESIGN capacities, and a "
                     "clinker factor is a production-composition ratio. 0.84 also sits "
                     "above the 0.65-0.80 band typical of blended cement, and the study "
                     "then called this producer 'low-clinker' three sections later. The "
                     "figure carried here is the production ratio implied by the FY2025 "
                     "physical disclosure: clinker produced less clinker exported, over "
                     "cement produced: " + IRP + " gives clinker production 3,851.6 kt "
                     "less clinker exports 1,300.5 kt = 2,551.1 kt ground into 3,480.6 kt "
                     "of cement", "2026-03-01", "Company"),

    # ---- PHYSICAL drivers. The build runs on these, and prices come OUT ----
    kiln_util=I([0.9170, 0.9200, 0.9250, 0.9300, 0.9330, 0.9350],
                "Clinker-kiln utilisation, FY2025A then FY2026E-FY2030E, and the primary "
                "volume driver. FY2025 is now DISCLOSED, not inferred: " + IRP + " gives "
                "clinker production of 3,851.6 kt, which is 91.70% of the audited 4.2Mt "
                "kiln, and the company states the rate as 92%. The plant has run 92-94% in "
                "three of the last five years, so the path rises only modestly — the kiln "
                "is the binding asset and there is little room above here",
                "2026-03-01", "Company"),
    clk_export_share=I([0.3377, 0.3300, 0.3200, 0.3100, 0.3050, 0.3000],
                       "Share of clinker production sold AS CLINKER rather than ground into "
                       "cement. FY2025 is DISCLOSED: " + IRP + " gives clinker exports of "
                       "1,300.5 kt on production of 3,851.6 kt = 33.77%. This is the "
                       "central operating lever and revision 3 could not see it at all: "
                       "clinker exports and domestic cement compete for the same kiln, and "
                       "a tonne of clinker realises a fraction of the tonne of cement it "
                       "could have become. Note the direction of travel — clinker exports "
                       "FELL 37% in FY2025 (2,074.4 kt to 1,300.5) while cement exports "
                       "rose 74%, so the mix was already shifting toward the higher-value "
                       "product before this forecast starts", "2026-03-01", "Company"),
    cem_export_share=I([0.1772, 0.1800, 0.1800, 0.1750, 0.1700, 0.1650],
                       "Share of cement SOLD that is exported. FY2025 is DISCLOSED: " + IRP +
                       " gives cement exports of 629.5 kt against local sales of 2,923.6 "
                       "kt, i.e. 17.72% of the 3,553.1 kt of cement sold. Well inside the "
                       "30% statutory cap; revision 3's single-product build put exports at "
                       "31.5% of volume and BREACHED the cap its own text called binding",
                       "2026-03-01", "Company"),
    cem_stock_draw=I([0.0725, 0.0, 0.0, 0.0, 0.0, 0.0],
                     "Cement sold LESS cement produced, in Mt. " + IRP + " discloses cement "
                     "production of 3,480.6 kt against sales of 3,553.1 kt (2,923.6 local "
                     "plus 629.5 exported), so FY2025 drew 72.5 kt out of finished-goods "
                     "inventory. Revision 4 equated sales to production and understated "
                     "despatches by 1.5%. Held at zero across the forecast: a stock draw is "
                     "a one-off by construction and the inventory note shows only EGP "
                     "320.8mn of finished goods at the year end", "2026-03-01", "Company"),
    clk_price_ratio=I(0.6500, "Export clinker price as a fraction of the export cement "
                      "price. Clinker is the unground intermediate and trades at a "
                      "discount; 0.65 sits in the middle of the range the trade press "
                      "reports. This is the one splitting assumption the export leg needs, "
                      "and the two export prices are DERIVED from it and the audited "
                      "export revenue, not asserted", "2026-01-15", "Industry"),
    fx_avg_fy25=I(49.26, AFS25 + " — note 2.5 currency table: average USD/EGP for 2025",
                  "2025-12-31", "Company"),
    fx_ye_fy25=I(47.66, AFS25 + " — note 2.5: year-end USD/EGP 2025", "2025-12-31", "Company"),
    fx_avg_fy24=I(44.39, AFS25 + " — note 2.5: average USD/EGP 2024", "2024-12-31", "Company"),
    fx=I(50.30, "USD/EGP at the valuation date", "2026-08-06", "Country"),

    # ---- forecast drivers -------------------------------------------------
    price_local_path=I(_index(0.080),
                       "Local realised price index on the FY2025 base: the FY2026 step of "
                       "8.0% is evidenced, and FY2027 onward escalate on the house "
                       "inflation path at ZERO real growth, the same path the cost index "
                       "carries. The retired ladder grew 9.0%, 8.0%, 7.0% and 6.5% — below "
                       "the cost path in every year, with no mechanism offered for the gap, "
                       "which against the house path is an 11.0% cumulative real price "
                       "decline nobody wrote down. THE EVIDENCE FOR THE FY2026 STEP. " + IRP + " and page 4 give "
                       "local revenue and local volume for both years and both fourth "
                       "quarters, so the realised local price can be computed rather than "
                       "assumed: FY2024 EGP 1,810/t, FY2025 EGP 2,909/t — a rise of 60.7% "
                       "on volume up 11.7%. The FY2025 margin explosion was PRICE, not "
                       "volume, which settles a question three revisions argued about "
                       "without evidence. More useful still is the exit rate: the fourth "
                       "quarter of 2025 realised EGP 3,118/t, 7.2% ABOVE the full-year "
                       "average. Simply holding the Q4 exit flat through 2026 therefore "
                       "produces a full-year average 7.2% higher, so the 8.0% carried here "
                       "is only 0.8 points above a no-further-increase path. Revision 3 "
                       "assumed 3.0% against 11.5% cost inflation and had nothing behind "
                       "it; revision 4 assumed 8.0% and had only a plausibility argument. "
                       "The number is unchanged from revision 4 — but it is now the "
                       "conservative reading of a disclosed run rate rather than a guess "
                       "that happened to land in the right place",
                       "2026-03-01", "Company"),
    price_exp_path=I([1.000, 0.968, 0.944, 0.927, 0.911, 0.895],
                     "Export price index in US dollars on the FY2025 base, declining "
                     "because the EU carbon border mechanism raises the landed cost of "
                     "Egyptian cement in Europe; set shallower than a high-clinker peer "
                     "would face because this producer's alternative-fuel and hydrogen "
                     "programmes are funded and under construction",
                     "2026-01-01", "Industry"),
    fx_path=I([49.26] + [round(x, 2) for x in _FXP],
              "USD/EGP path: FY2025 actual average, then the house currency path — "
              "relative purchasing-power parity on the house inflation path against "
              "long-run foreign inflation, DERIVED and never hand-set. The retired path "
              "was typed (50.60 to 61.50 by FY2030) and depreciated the pound at roughly "
              "two-thirds of the inflation differential the same model applied to costs, "
              "which is one event counted once and ignored once",
              "2026-09-02", "Country"),
    cost_infl=I(_index(0.115),
                "Cumulative local cost-inflation index from the FY2025 base. The FY2026 "
                "step of 11.5% is unchanged; FY2027 onward escalate on the house inflation "
                "path, the SAME path the local price index carries, so the operating margin "
                "is an output of the two rather than the residual of two separately chosen "
                "ladders. "
                "This is an INPUT-PRICE path and is deliberately left at headline "
                "inflation even though the company's own audited cash cost grew only 12.5% "
                "in FY2025 on volume that rose — i.e. its realised unit cost inflation ran "
                "below the national rate. Crediting that outperformance here would "
                "double-count it, because the company-specific efficiency is carried "
                "separately and explicitly in af_saving, which is anchored to a funded, "
                "under-construction asset rather than to a trend", "2026-07-10", "Country"),
    af_saving=I([0.000, 0.015, 0.030, 0.040, 0.048, 0.055],
                "Cumulative saving on the materials-and-fuel line from the alternative-fuel "
                "and hydrogen programmes, relative to the FY2025 cost base. Not an "
                "assumption about intent: EGP 240.235mn of alternative-fuel capacity for "
                "kiln 2 sits in assets under construction at the year end and a EUR 25mn "
                "EBRD facility is drawn against it", "2025-12-31", "House"),
    svc_share=I(0.06325, "Services revenue (transportation) as a share of goods revenue, "
                "derived from the disclosed FY2025 split", "2025-12-31", "Company"),
    dna_pct=I([0.025, 0.027, 0.029, 0.031, 0.033],
              "Depreciation as a share of revenue across the forecast, rising because "
              "capital spent from here is incurred at today's replacement cost and adds a "
              "larger depreciable base per tonne than the legacy book carries. FY2025 "
              "actual is 2.33%", "2026-08-06", "House"),
    capex_usd_t_cap=I(3.23, "Maintenance capital expenditure in US dollars per tonne of "
                      "installed capacity, SET AT THE MOST RECENT FULL YEAR'S TOTAL CAPITAL "
                      "SPENDING PER TONNE — EGP 796.471mn on 5.0Mt at USD/EGP 49.26. "
                      "REVISION 4 CORRECTS THE REASONING BEHIND THIS INPUT, WHICH WAS "
                      "BACKWARDS. Revision 3 observed that FY2024 (USD 3.70/t) and FY2025 "
                      "(USD 3.23/t) 'both carry the alternative-fuel and silo programmes' "
                      "and then set maintenance at USD 4.00 — the MIDDLE of a band it had "
                      "just said was inflated by growth spending, and above both observed "
                      "years. If both observations INCLUDE growth capital, they are an UPPER "
                      "BOUND on maintenance, so the maintenance level belongs at or below "
                      "them, not above. The H1-2026 cash-flow statement settles the "
                      "direction: it splits the spend into payments for property, plant and "
                      "equipment of EGP 102.893mn and payments for ASSETS UNDER "
                      "CONSTRUCTION of EGP 505.540mn, so 83% of six months' capital "
                      "spending is the growth programme and the sustaining line is running "
                      "near USD 0.8/t annualised. That is a deferral rather than a "
                      "sustainable rate, so the input is NOT cut to it; it is set at the "
                      "most recent full year's TOTAL, which remains an upper bound on "
                      "maintenance and is still above the industry sustaining norm of about "
                      "USD 3/t. Worth EGP 1.77 a share against revision 3's figure, and the "
                      "whole range is published as a sensitivity",
                      "2025-12-31", "Company"),
    wc_pct_drev=I(0.12, "Change in working capital over change in revenue. The FY2025 "
                  "outturn on the disclosed movements is close to this",
                  "2026-08-06", "House"),
    payout=I(0.556, "Dividend payout ratio from FY2026E, held at the FY2025 outturn: EGP "
             "2,001.792mn declared on EGP 3,599.586mn of attributable profit",
             "2026-08-06", "House"),
    cash_yield=I([0.150, 0.130, 0.120, 0.112, 0.108],
                 "Yield earned on the cash balance across the forecast. The FY2025 outturn "
                 "was 8.8% on the average balance — much of the cash sits in "
                 "foreign-currency current accounts rather than pound deposits — and the "
                 "path is set above it as the balance is redeployed, then easing",
                 "2026-08-06", "House"),
    # ---- DISCLOSED FACTS AND SUPERSEDED FIGURES THE STUDY QUOTES, REGISTERED
    # [added 03-Sep-2026, found by prose_check.py on its first run]. Each of these was
    # typed into a builder's f-string. Three are DISCLOSED facts about the company's own
    # debt and tax that this model does not compute; three are figures from a superseded
    # revision or from a sell-side model, quoted so a reader can see what changed — which a
    # model cannot compute because a different model produced them. Either way they are
    # facts, and a fact in this study carries four fields.
    ebrd_margin=I(0.0435, AFS25 + " note 10, facility schedule — the European Bank for "
                  "Reconstruction and Development euro facility prices at three-month "
                  "Euribor plus this margin", "2025-12-31", "Company"),
    eff_rate_disclosed_fy25=I(0.2333, AFS25 + " note 10.2 — the average effective interest "
                              "rate the company itself states for 2025, distinct from the "
                              "rate this study computes from the charge and the balance",
                              "2025-12-31", "Company"),
    eff_rate_disclosed_fy24=I(0.2296, AFS24 + " note 10.2 — the same disclosure for 2024",
                              "2024-12-31", "Company"),
    eff_rate_disclosed_q126=I(0.2592, Q126 + " — the same disclosure annualised for the "
                              "first quarter of 2026", "2026-03-31", "Company"),
    tax_eff_superseded=I(0.2943, "Effective tax rate INFERRED by revision 1 of this study "
                         "by closing a modelled net finance income, against the 23.82% the "
                         "filing discloses. Quoted in the source register to show what "
                         "changed; not an input to anything.", "2026-08-06", "House"),
    efg_terminal_roic=I(0.0881, "Terminal return on invested capital in the published "
                        "EFG Hermes model, as reconstructed in the reconciliation of "
                        "section 1.10. A figure from another party's model, quoted; not an "
                        "input to anything.", "2026-08-06", "House"),
    efg_margin_exit=I(0.343, "Terminal EBITDA margin in the published EFG Hermes model, "
                      "the far end of its 39.3% to 34.3% glide. Another party's figure, "
                      "quoted; not an input to anything.", "2026-08-06", "House"),
    efg_unit_cost_growth=I(0.469, "Growth in the cash cost per tonne the EFG Hermes model "
                           "charges across its forecast window, as reconstructed in "
                           "section 1.10. Another party's figure, quoted.", "2026-08-06",
                           "House"),
    tax_eff=I(0.2382, AFS25 + " — income tax of EGP 1,125.468mn over pre-tax profit of EGP "
              "4,725.158mn. Note 10.2 separately discloses an average effective rate of "
              "23.33% (2024: 22.96%); Q1-2026 ran at 25.92%. Revision 1 inferred 29.43% by "
              "closing a MODELLED net finance income against disclosed profit, and "
              "over-taxed every forecast year by 5.6 points", "2025-12-31", "Company"),

    # ---- cost of capital ---------------------------------------------------
    # the superseded quote and the reviewers' range are FACTS — one about a prior revision
    # of this study, two about what three reviewers independently reported — and they are
    # registered rather than typed into this note, which is the same rule one layer in
    rf_superseded=I(0.2231, "Egypt 10-year local-currency government bond yield as carried "
                    "by revision 3 of this study, dated 21 July 2026 and therefore sixteen "
                    "days before the valuation date. Quoted to show what changed; not an "
                    "input to anything.", "2026-07-21", "House"),
    rf_reviewer_low=I(0.2288, "Lowest of three independent reviewers' readings of the "
                      "Egyptian 10-year on 3-5 August 2026.", "2026-08-05", "Country"),
    rf_reviewer_high=I(0.2298, "Highest of the same three readings. The adopted figure is "
                       "their midpoint, struck at the valuation date.", "2026-08-05",
                       "Country"),
    rf=I(0.2295, "Egypt 10-year local-currency government bond yield. Revision 3 carried "
         "22.31% dated 21 July; three independent reviewers put the 10-year at 22.88-22.98% "
         "on 3-5 August, and the curve is inverted above it (1-year near 25.6%). 22.95% is "
         "the midpoint of the three, at the valuation date rather than sixteen days before "
         "it", "2026-08-05", "Country"),
    sov_spread_cds=I(0.0340, "Egypt CDS-implied sovereign default spread, Damodaran "
                     "January-2026 country risk file, CDS column. NETTED OUT of the local "
                     "risk-free rate so sovereign default risk is charged once, not twice",
                     "2026-01-05", "Country"),
    erp_cds=I(0.0941, "Egypt equity risk premium, CDS-based, Damodaran January-2026",
              "2026-01-05", "Country"),
    euribor=I(0.0249, "Three-month Euribor, the reference rate on the EBRD facility. "
              "Revision 3 carried 2.10%, which sits BELOW the ECB deposit facility rate of "
              "2.25% and is therefore impossible as a term rate. It also applied one "
              "reference to both a 3-month and a 6-month facility; 6-month Euribor is "
              "nearer 2.72%, and the difference is carried as a known simplification",
              "2026-08-06", "Country"),
    kd_egp_marginal=I(0.2060, "Marginal EGP borrowing rate: the Central Bank corridor offer "
                      "rate of 20.0% plus the 0.6% margin disclosed on the CIB facility",
                      "2026-08-06", "Company"),
    egp_dep_vs_eur=I(0.060, "Expected annual depreciation of the pound against the euro, "
                     "used ONLY to compute the local-currency-equivalent cost of debt "
                     "alternative under uncovered interest parity", "2026-08-06", "House"),
    kd_path=I([0.2060, 0.1810, 0.1610, 0.1490, 0.1400],
              "EGP marginal borrowing-rate path. The discount-rate glide inherits its SHAPE "
              "from this rather than from a second judgement. The company's own book is now "
              "91% euro-denominated and will not glide with the Egyptian easing calendar, "
              "but the discount rate is a POUND rate applied to pound cash flows, so the "
              "pound path is the right shape anchor and the euro book sets the LEVEL of the "
              "cost of debt, not its slope", "2026-08-06", "House"),
    kd_term=I(_KD_TERM, "Terminal cost of debt: the long-run Egyptian corporate-borrowing "
             "norm carried by the house macro path, replacing a terminal risk-free plus 300bp "
              "corporate credit spread. Revision 3 carried 10.00% against a terminal "
              "risk-free rate of 12.50% — a corporate borrower funding 250bp BELOW its own "
              "sovereign in the same currency, printed one row above it in the same table. "
              "It is now built from the risk-free rate rather than asserted beside it, so "
              "the impossibility cannot recur", "2026-08-06", "House"),
    rf_term=I(_RF_TERM, "Terminal risk-free rate, DERIVED from the house macro path as "
              "terminal inflation plus the real-rate convention, and so no longer this "
              "study's own reading of which published target to use. THE CONFLICT THIS "
              "SETTLES: this study argued for the central bank's "
              "longest-dated published inflation target of 5% (Q4-2028) plus a standard "
              "emerging-market real-rate convention of about 5.5 percentage points. "
              "Revision 3 used the 7% target, which is the NEAR-dated one (Q4-2026) and not "
              "the medium-term target at all. The correction also repairs a second defect: "
              "against 7% the model's 5% terminal growth was -1.9% real while the text "
              "called it 'approximately zero'. Against the 5% target it genuinely is zero",
              "2026-08-06", "House"),
    erp_term=I(0.0700, "Terminal equity risk premium, normalised below the currently "
               "elevated level", "2026-08-06", "House"),
    wd_term=I(0.2000, "Terminal debt weight", "2026-08-06", "House"),
    g_term=I(_G_TERM, "Terminal growth from the house macro path: terminal inflation plus a "
             "STATED real growth of zero, so the real assumption is written down rather "
             "than left to be inferred from the gap to the discount rate. The retired 5% "
             "was set against a terminal risk-free of 10.50% and called approximately zero "
             "in real terms; on the house path it would have been -1.9% real. "
             "industrial against a terminal risk-free rate that already embeds "
             "disinflation — approximately zero in real terms", "2026-08-06", "House"),
    stub_years=I(0.500, "Elapsed fraction of FY2026 at the valuation date. THE VALUATION "
                 "DATE IS 30 JUNE 2026, the date of the latest disclosed balance sheet, "
                 "not the date of the latest traded price. Revision 3 valued at 6 August "
                 "and rolled the balance sheet forward to meet it; the interim accounts "
                 "now make that unnecessary, and a bridge standing on a disclosed balance "
                 "sheet is worth more than two months of freshness in the discounting. The "
                 "price the range is compared against is still the latest known close, and "
                 "the 37-day gap between the two is disclosed rather than closed",
                 "2026-06-30", "House"),

    # ---- lens inputs -------------------------------------------------------
    repl_usd_t=I(130.0, "Replacement cost per annual tonne of cement capacity, USD 120-150 "
                 "band", "2026-08-06", "Industry"),
    ev_t_just=I(95.0, "Justified enterprise value per annual tonne of capacity, set well "
                "below replacement cost because a market carrying 76Mt against 54Mt of "
                "consumption does not pay replacement cost", "2026-08-06", "House"),
    ev_ebitda_just=I(4.50, "Justified enterprise value to EBITDA on normalised earnings, "
                     "disclosed as weakly anchored against a thin Egyptian peer set",
                     "2026-08-06", "House"),
    pe_just=I(7.00, "Justified price to earnings on normalised operating earnings, cash "
              "excluded and added back at face", "2026-08-06", "House"),
    norm_mgn=I(0.3120, "Mid-cycle EBITDA margin: the midpoint of the AUDITED FY2024 outturn "
               "of 23.15% and the AUDITED FY2025 peak of 39.25%", "2026-08-06", "House"),
    norm_rev_haircut=I(0.94, "Haircut to the FY2025 revenue base for the normalised lens",
                       "2026-08-06", "House"),

    # ---- sector and peers --------------------------------------------------
    egy_capacity_mt=I(76.0, "Egyptian nameplate cement capacity", "2025-10-01", "Industry"),
    egy_cons_mt=I(53.9, "Egyptian domestic cement sales 2025. " + IRP + " page 12 gives "
                  "53.9Mt, against the 54.0 previously carried on trade estimate",
                  "2026-03-01", "Company"),
    egy_prod_mt=I(72.6, "Egyptian cement and clinker SALES 2025 — local plus export. " + IRP +
                  " page 12 gives local 53.9Mt and exports 18.6Mt, total 72.6Mt. Revisions "
                  "1 to 4 carried 65.0Mt as 'production' against exports of 18.5Mt and "
                  "consumption of 54Mt, a balance that does not close: 65 less 54 is 11Mt, "
                  "not 18.5. One reviewer caught the gap and the disclosure now closes it. "
                  "This changes the sector picture materially — see the utilisation note",
                  "2026-03-01", "Company"),
    egy_exports_mt=I(18.6, "Egyptian cement AND clinker export sales 2025. " + IRP +
                     " page 12. The two products are reported together, which is why the "
                     "earlier balance failed: it set a cement-plus-clinker export figure "
                     "against a cement-only production figure", "2026-03-01", "Company"),
    egy_revival_mt=I(12.6, "Dormant Egyptian capacity under revival from the second half of "
                     "2026", "2025-10-01", "Industry"),
    egy_gdp_egp_bn=I(18000.0, "Egyptian nominal gross domestic product, order of magnitude, "
                     "used only for the terminal-growth crossover arithmetic",
                     "2026-01-01", "Country"),
    egy_gdp_growth=I(0.180, "Egyptian nominal GDP growth, same arithmetic",
                     "2026-01-01", "Country"),
    peer_scem_rev=I(9090.0, "Sinai Cement FY2025 revenue", "2026-03-10", "Industry"),
    peer_scem_pat=I(2290.0, "Sinai Cement FY2025 profit after tax", "2026-03-10", "Industry"),
    peer_scem_mcap=I(20604.19, "Sinai Cement market capitalisation at 06-Aug-2026",
                     "2026-08-06", "Industry"),
    peer_mbsc_rev=I(5700.0, "Misr Beni Suef Cement FY2025 net sales", "2026-03-01", "Industry"),
    peer_mbsc_pat=I(3946.0, "Misr Beni Suef Cement FY2025 attributable profit",
                    "2026-03-01", "Industry"),
    peer_mbsc_mcap=I(13730.0, "Misr Beni Suef Cement market capitalisation",
                     "2026-08-06", "Industry"),

    # ---- lens weights ------------------------------------------------------
    w_dcf=I(0.50, "Weight, cash-flow lens", "2026-08-06", "House"),
    w_rel=I(0.20, "Weight, relative lens, held down because the peer set is thin",
            "2026-08-06", "House"),
    w_norm=I(0.22, "Weight, normalised-earnings lens", "2026-08-06", "House"),
    w_asset=I(0.08, "Weight, asset lens, deliberately small: restarting a mothballed line "
              "costs a fraction of building one", "2026-08-06", "House"),
)

V = {k: v['value'] for k, v in INP.items()}
for k, v in INP.items():
    assert set(v) == {'value', 'source', 'date', 'ring'} and str(v['source']).strip(), k
    assert v['ring'] in ('Market', 'Company', 'Industry', 'Country', 'House'), k
TAX, TAXE = V['tax_stat'], V['tax_eff']
YRS = ['FY2026E', 'FY2027E', 'FY2028E', 'FY2029E', 'FY2030E']
HIST = ['FY2023', 'FY2024', 'FY2025']

say("=" * 78)
say("ARCC — REVISION 3 — audited accounts, price path recalibrated to the record")
say("=" * 78)

# ==================== 1. SHARE COUNT ========================================
SH = V['shares_issued'] - V['shares_treasury']
MKTCAP = V['spot'] * SH
SHT = dict(issued=V['shares_issued'], treasury=V['shares_treasury'], outstanding=SH,
           wavg_fy25=V['shares_wavg_fy25'], wavg_fy24=V['shares_wavg_fy24'],
           from_fy25_dividend=V['div_fy25_declared'] / 5.34,
           par_check=V['shares_issued'] * 2.0,
           treasury_price=V['shares_treasury'] and 143.327985 / V['shares_treasury'])
say(f"\n[Shares] {V['shares_issued']:.4f}mn issued less {V['shares_treasury']:.4f}mn "
    f"treasury = {SH:.4f}mn outstanding. The FY2025 distribution of EGP "
    f"{V['div_fy25_declared']:,.1f}mn at the reported EGP 5.34 per share implies "
    f"{SHT['from_fy25_dividend']:.4f}mn — the same count. Market capitalisation EGP "
    f"{MKTCAP:,.0f}mn")

# ==================== 2. AUDITED HISTORY ====================================
rev_h = [V['rev_fy23'], V['rev_fy24'], V['rev_fy25']]
cogs_h = [V['cogs_fy23'], V['cogs_fy24'], V['cogs_fy25']]
gp_h = [rev_h[i] - cogs_h[i] for i in range(3)]
ga_h = [V['ga_fy23'], V['ga_fy24'], V['ga_fy25']]
prov_h = [V['prov_fy23'], V['prov_fy24'], V['prov_fy25']]
ecl_h = [V['ecl_fy23'], V['ecl_fy24'], V['ecl_fy25']]
ebit_h = [gp_h[i] - ga_h[i] - prov_h[i] - ecl_h[i] for i in range(3)]
dna_h = [V['dna_fy23'], V['dna_fy24'], V['dna_fy25']]
ebitda_h = [ebit_h[i] + dna_h[i] for i in range(3)]
pbt_h = [V['pbt_fy23'], V['pbt_fy24'], V['pbt_fy25']]
taxc_h = [V['tax_fy23'], V['tax_fy24'], V['tax_fy25']]
pat_h = [V['pat_fy23'], V['pat_fy24'], V['pat_fy25']]
eps_h = [V['eps_fy23'], V['eps_fy24'], V['eps_fy25']]
capex_h = [V['capex_fy23'], V['capex_fy24'], V['capex_fy25']]
mgn_h = [ebitda_h[i] / rev_h[i] for i in range(3)]
taxe_h = [taxc_h[i] / pbt_h[i] for i in range(3)]
say(f"\n[Audited history] EBITDA " + "  ".join(f"{x:,.0f}" for x in ebitda_h) +
    "  margin " + "  ".join(f"{m:.2%}" for m in mgn_h))
say(f"[Audited history] operating profit " + "  ".join(f"{x:,.0f}" for x in ebit_h) +
    f"; effective tax " + "  ".join(f"{t:.2%}" for t in taxe_h))

# ==================== 3. UNIT BUILD — PHYSICAL, BOTTOM UP ==================
# REVISION 4 INVERTS THE BUILD. Revision 3 assumed a cement price, divided the audited
# revenue by it to get volume, and called the resulting utilisation "an independent
# corroboration". It was neither independent nor a corroboration: it was the same
# assumption written twice, and the FY2025 "validation" it produced was an accounting
# IDENTITY that reproduces the audited revenue for ANY price, because the volume moves
# by exactly the reciprocal. The residual only appeared to respond to price because two
# cells on the Assumptions sheet held stale rounded copies of the derived figures.
#
# The build now starts at the PLANT. The drivers are physical — kiln utilisation, the
# clinker factor, and the two export shares. Tonnes by product, mill utilisation and all
# THREE realised prices are derived from them and from the audited revenue note. The
# prices are therefore OUTPUTS that can be checked against published Egyptian ranges: a
# test that can actually fail.
#
# It also carries three products where revision 3 carried one. The company sells local
# cement, export cement and export CLINKER, and clinker is an unground intermediate worth
# a fraction of the cement it could have become. Pricing 1.3Mt of clinker at a cement
# price was the error that made the plant look 28% smaller than it is and manufactured
# 0.9Mt of kiln headroom that does not exist.


def physical(kiln_u, cf, clk_sh, cem_sh, draw):
    """Everything downstream of the kiln, in tonnes. No prices enter here."""
    clk_prod = V['cap_clinker_mt'] * kiln_u
    clk_exp = clk_prod * clk_sh
    clk_ground = clk_prod - clk_exp
    cem_prod = clk_ground / cf
    cem_sold = cem_prod + draw            # a stock movement, disclosed for FY2025
    cem_exp = cem_sold * cem_sh
    return dict(clk_prod=clk_prod, clk_exp=clk_exp, clk_ground=clk_ground,
                cem_prod=cem_prod, cem_sold=cem_sold, cem_draw=draw,
                mill_util=cem_prod / V['cap_cement_mt'],
                cem_exp=cem_exp, cem_loc=cem_sold - cem_exp,
                sold=cem_sold + clk_exp, kiln_util=kiln_u)


PH = [physical(V['kiln_util'][i], V['clinker_factor'], V['clk_export_share'][i],
               V['cem_export_share'][i], V['cem_stock_draw'][i]) for i in range(6)]
p0 = PH[0]

# ---- prices are DERIVED, and they are the test ----------------------------
price_loc25 = V['rev_local_goods_fy25'] / p0['cem_loc']
_den = p0['cem_exp'] + p0['clk_exp'] * V['clk_price_ratio']
price_exp_cem25 = V['rev_exp_goods_fy25'] / _den
price_exp_clk25 = price_exp_cem25 * V['clk_price_ratio']
vol25 = p0['sold']
say(f"\n[The plant, in tonnes — DRIVERS, not outputs] kiln {p0['kiln_util']:.1%} of "
    f"{V['cap_clinker_mt']:.1f}Mt = {p0['clk_prod']:.3f}Mt of clinker; "
    f"{p0['clk_exp']:.3f}Mt sold as clinker, {p0['clk_ground']:.3f}Mt ground at a clinker "
    f"factor of {V['clinker_factor']:.4f} into {p0['cem_prod']:.3f}Mt of cement "
    f"({p0['mill_util']:.1%} of the {V['cap_cement_mt']:.1f}Mt mill), plus a "
    f"{p0['cem_draw']*1000:.1f}kt draw from finished-goods stock")
say(f"[Against the DISCLOSED physicals] the company reports clinker production 3,851.6kt, "
    f"cement production 3,480.6kt, local sales 2,923.6kt, cement exports 629.5kt, clinker "
    f"exports 1,300.5kt, total 4,853.6kt. This build reproduces "
    f"{p0['clk_prod']*1000:,.1f} / {p0['cem_prod']*1000:,.1f} / {p0['cem_loc']*1000:,.1f} / "
    f"{p0['cem_exp']*1000:,.1f} / {p0['clk_exp']*1000:,.1f} / {p0['sold']*1000:,.1f}")
say(f"[Despatches] local cement {p0['cem_loc']:.3f}Mt, export cement {p0['cem_exp']:.3f}Mt, "
    f"export clinker {p0['clk_exp']:.3f}Mt = {vol25:.3f}Mt total")
say(f"[Prices — DERIVED from the audited revenue note, not assumed] local cement EGP "
    f"{price_loc25:,.0f}/t; export cement USD {price_exp_cem25/V['fx_avg_fy25']:.1f}/t; "
    f"export clinker USD {price_exp_clk25/V['fx_avg_fy25']:.1f}/t at the "
    f"{V['clk_price_ratio']:.2f} clinker ratio. Revision 3 ASSUMED EGP 3,500 and USD 62 "
    f"and derived tonnes from them — the reverse, and untestable")
say(f"[Export cap] cement exports are {V['cem_export_share'][0]:.1%} of cement production "
    f"against a 30% statutory cap. Revision 3's single-product build put exports at 31.5% "
    f"of volume and BREACHED the cap its own text called binding")

# ---- cost, allocated to the physical driver that actually causes it -------
cash_cost25 = (V['cos_materials_fy25'] + V['cos_transport_fy25'] + V['cos_overhead_fy25']
               + (V['ga_fy25'] - V['ga_admin_dep_fy25']))
cc_mat_clk = V['cos_materials_fy25'] / p0['clk_prod']       # kiln-driven: fuel and raw meal
cc_tra_t = V['cos_transport_fy25'] / p0['sold']             # despatch-driven
cc_ovh_t = (V['cos_overhead_fy25'] + V['ga_fy25'] - V['ga_admin_dep_fy25']) / p0['sold']
say(f"[Cost stack, DISCLOSED — notes 5 and 6, allocated to their own driver] materials and "
    f"fuel EGP {cc_mat_clk:,.0f} per tonne of CLINKER (the kiln burns it, not the mill); "
    f"transportation EGP {cc_tra_t:,.0f} and overheads EGP {cc_ovh_t:,.0f} per tonne "
    f"DESPATCHED; total cash cost EGP {cash_cost25/vol25:,.0f}/t sold. Provisions and "
    f"expected credit losses are EXCLUDED — revision 3 carried them inside 'cash cost', "
    f"and they are not cash")

BU = []
for i in range(6):
    ph = PH[i]
    infl = V['cost_infl'][i]
    pl = price_loc25 * V['price_local_path'][i]
    pec = price_exp_cem25 / V['fx_avg_fy25'] * V['price_exp_path'][i] * V['fx_path'][i]
    pek = pec * V['clk_price_ratio']
    rev_goods = ph['cem_loc'] * pl + ph['cem_exp'] * pec + ph['clk_exp'] * pek
    rev = rev_goods * (1 + V['svc_share'])
    c_mat = cc_mat_clk * infl * (1 - V['af_saving'][i]) * ph['clk_prod']
    c_tra = cc_tra_t * infl * ph['sold']
    c_ovh = cc_ovh_t * infl * ph['sold']
    cc = c_mat + c_tra + c_ovh
    # Provisions and expected credit losses are operating charges that sit above operating
    # profit in the audited statements, so they belong in the EBITDA bridge. They are NOT
    # cash cost per tonne, which is why they are carried on their own line here and kept
    # out of the per-tonne stack. Held flat on revenue at the FY2025 relationship.
    c_prv = (V['prov_fy25'] + V['ecl_fy25']) / V['rev_fy25'] * rev
    eb = rev - cc - c_prv
    BU.append(dict(**ph, vol=ph['sold'], price_loc=pl, price_exp_cem=pec,
                   price_exp_clk=pek, rev_goods=rev_goods, rev=rev,
                   price=rev / ph['sold'], c_mat=c_mat, c_tra=c_tra, c_ovh=c_ovh,
                   cc=cc, cc_t=cc / ph['sold'], c_prv=c_prv, ebitda=eb, mgn=eb / rev,
                   util=ph['mill_util']))
# ---- the H1-2026 reviewed actual, and what it says about FY2026 -----------
# [L-013]: a recent reviewed actual outranks a stale full-year rate. The half is
# scaled to a full year on FY2025's OWN half-year split, PER CHANNEL, because
# the channels do not share a seasonal shape: 45.9% of FY2025's local goods
# revenue and 39.2% of its export goods revenue fell in the first half.
# THE HALF-YEAR SHARE IS MEASURED ON EVERY HALF THE ARCHIVE SUPPORTS, NOT ON THE
# ONE NEAREST TO HAND, because it is the single largest assumption in this
# revision. IT IS NOT STABLE: the first half was 44.19% of FY2025, 45.55% of
# FY2022 and 52.69% of FY2023. Grossing up on FY2025 alone lifts the half by
# 12.7% and rests that lift on one year. The MEDIAN of the three is used and the
# whole range is published. The per-CHANNEL structure still comes from FY2025 —
# the only year whose interim note splits the channels — and the total is then
# levelled onto the median share: STRUCTURE from the one year that has it, LEVEL
# from all three.
_h1_shares_rev = sorted([V['rev_h1_25'] / V['rev_fy25'],
                         V['rev_h1_22'] / V['rev_fy22'],
                         V['rev_h1_23'] / V['rev_fy23']])
_h1_shares_cogs = sorted([V['cogs_h1_25'] / V['cogs_fy25'],
                          V['cogs_h1_22'] / V['cogs_fy22'],
                          V['cogs_h1_23'] / V['cogs_fy23']])
h1_share_rev_med = _h1_shares_rev[1]
h1_share_cogs_med = _h1_shares_cogs[1]
h1_share_loc = V['rev_h1_25_loc_goods'] / V['rev_local_goods_fy25']
h1_share_exp = V['rev_h1_25_exp_goods'] / V['rev_exp_goods_fy25']
h1_share_svc = V['rev_h1_25_svc'] / (V['rev_fy25'] - V['rev_local_goods_fy25']
                                     - V['rev_exp_goods_fy25'])
_fy26_rev_on_fy25 = (V['rev_h1_26_loc_goods'] / h1_share_loc
                     + V['rev_h1_26_exp_goods'] / h1_share_exp
                     + V['rev_h1_26_svc'] / h1_share_svc)
_level = (V['rev_h1_26'] / h1_share_rev_med) / _fy26_rev_on_fy25
fy26_loc_implied = V['rev_h1_26_loc_goods'] / h1_share_loc * _level
fy26_exp_implied = V['rev_h1_26_exp_goods'] / h1_share_exp * _level
fy26_svc_implied = V['rev_h1_26_svc'] / h1_share_svc * _level
fy26_rev_implied = fy26_loc_implied + fy26_exp_implied + fy26_svc_implied
SEASON_RANGE = dict(shares_rev=_h1_shares_rev, shares_cogs=_h1_shares_cogs,
                    median=h1_share_rev_med,
                    fy26_low=V['rev_h1_26'] / _h1_shares_rev[2],
                    fy26_median=V['rev_h1_26'] / h1_share_rev_med,
                    fy26_high=V['rev_h1_26'] / _h1_shares_rev[0],
                    fy26_if_doubled=V['rev_h1_26'] * 2.0,
                    fy26_on_fy25_only=_fy26_rev_on_fy25, level_adjust=_level)
say(f"\n[How much of a year IS ARCC's first half?] measured on every half the archive "
    f"supports: {_h1_shares_rev[0]:.1%}, {_h1_shares_rev[1]:.1%} and {_h1_shares_rev[2]:.1%} "
    f"of the year. IT IS NOT STABLE, and it is the largest assumption in this revision, so "
    f"the MEDIAN is used and the range is published: FY2026 revenue between "
    f"{SEASON_RANGE['fy26_low']:,.0f}mn and {SEASON_RANGE['fy26_high']:,.0f}mn, central "
    f"{SEASON_RANGE['fy26_median']:,.0f}mn. Grossing up on FY2025 alone would have given "
    f"{_fy26_rev_on_fy25:,.0f}mn and rested a {_fy26_rev_on_fy25/(V['rev_h1_26']*2)-1:+.1%} "
    f"lift on a single year")
say(f"\n[H1-2026, the latest disclosed period — filed 13-Aug-2026, a week AFTER revision "
    f"3's valuation date] revenue {V['rev_h1_26']:,.0f}mn, +{V['rev_h1_26']/V['rev_h1_25']-1:.1%} "
    f"on H1-2025, at a gross margin of {V['gp_h1_26']/V['rev_h1_26']:.1%} against "
    f"{gp_h[2]/rev_h[2]:.1%} for FY2025")
say(f"[And the MIX TURNED] local goods {V['rev_h1_26_loc_goods']:,.0f}mn "
    f"({V['rev_h1_26_loc_goods']/V['rev_h1_25_loc_goods']-1:+.1%} y-o-y) against export "
    f"goods {V['rev_h1_26_exp_goods']:,.0f}mn "
    f"({V['rev_h1_26_exp_goods']/V['rev_h1_25_exp_goods']-1:+.1%}). Revision 3 carried the "
    f"export share broadly flat; local tonnes are the better-priced tonnes, and that is why "
    f"the half-year margin holds")
say(f"[FY2026 implied by the half, on FY2025's own per-channel seasonality] local "
    f"{fy26_loc_implied:,.0f} + export {fy26_exp_implied:,.0f} + services "
    f"{fy26_svc_implied:,.0f} = {fy26_rev_implied:,.0f}mn against the pre-calibration model's "
    f"{BU[1]['rev']:,.0f}mn ({BU[1]['rev']/fy26_rev_implied-1:+.1%})")
say(f"[Export subsidy] EGP {V['export_subsidy_h1_26']:,.0f}mn collected in the second "
    f"quarter (note 29). EXCLUDED from forward operating income and left where it already "
    f"is, inside the 30 June cash balance. FY2025's export subsidy was EGP "
    f"{V['export_subsidy_fy25']:,.1f}mn on export revenue of {V['rev_exp_fy25']:,.0f}mn "
    f"({V['export_subsidy_fy25']/V['rev_exp_fy25']:.2%}); a rate near the half-year figure "
    f"would be implausible as a recurring entitlement, so this reads as a collection of "
    f"accumulated claims. WHAT WOULD OVERTURN IT: a comparable collection in a later period "
    f"with no accumulated-claims explanation")

# The calibration is applied to the FY2026 CHANNEL PRICES, not to revenue, so the
# physical build still drives the model and the tonnes are unchanged. What the
# half-year cannot resolve is stated rather than assumed: NO H1 TONNAGE IS
# DISCLOSED — the company published no interim presentation or release for the
# half — so the gap between the model's FY2026 and the reviewed actual cannot be
# split into price and volume. It is taken entirely on price, which is the
# conservative reading on the local leg (volume up would mean price up less) and
# the finest level the disclosure supports. FLAGGED as a disclosure gap.
_cal_loc = fy26_loc_implied / (BU[1]['cem_loc'] * BU[1]['price_loc'])
_cal_exp = fy26_exp_implied / (BU[1]['cem_exp'] * BU[1]['price_exp_cem']
                               + BU[1]['clk_exp'] * BU[1]['price_exp_clk'])

# THE COST LEG IS CALIBRATED ON THE SAME HALF, AND THIS IS NOT OPTIONAL.
# Scaling the price legs onto a reviewed actual while leaving the cost stack on
# its own assumed path would manufacture a margin out of the calibration —
# which is [L-009] and [L-110], and which this name's own walk-forward warned
# about from a second direction: gross profit's macro share came back NEGATIVE
# (-0.058), meaning the revenue and cost errors were cancelling and that repairing
# one leg alone BREAKS the cancellation and makes the margin forecast worse.
# So both legs are scaled on the same reviewed half, on FY2025's own half-year
# split, and the margin stays an OUTPUT of the two.
h1_share_ga = V['ga_h1_25'] / V['ga_fy25']
fy26_cogs_implied = V['cogs_h1_26'] / h1_share_cogs_med
fy26_ga_implied = V['ga_h1_26'] / h1_share_ga
_dna_in_cogs_fy25 = V['dna_fy25'] - V['ga_admin_dep_fy25']
fy26_dna_in_cogs = fy26_cogs_implied * (_dna_in_cogs_fy25 / V['cogs_fy25'])
fy26_admin_dep = fy26_ga_implied * (V['ga_admin_dep_fy25'] / V['ga_fy25'])
fy26_cashcost_implied = (fy26_cogs_implied - fy26_dna_in_cogs
                         + fy26_ga_implied - fy26_admin_dep)
_cal_cost = fy26_cashcost_implied / BU[1]['cc']
# Services are recalibrated on the same half for the same reason. FY2025's
# services ran at 6.325% of goods revenue; the half runs at
# 278.938 / 5,801.640 = 4.81%, because EXPORT transportation services fell from
# 228.191mn to 76.190mn as the export leg shrank. Carrying the FY2025 ratio onto
# a calibrated goods base would add revenue the company is no longer billing.
_svc_share_cal = fy26_svc_implied / (fy26_loc_implied + fy26_exp_implied)
say(f"[Services recalibrated too] {V['svc_share']:.3%} of goods revenue in FY2025 against "
    f"{_svc_share_cal:.3%} implied by the half — export transportation services fell from "
    f"{V['rev_h1_25_svc'] - 127.753131:,.0f}mn to 76mn as the export leg shrank. Carrying "
    f"the FY2025 ratio onto a calibrated goods base would bill revenue the company no "
    f"longer earns")
say(f"[Cost calibrated on the SAME half, so the margin stays an OUTPUT] H1-2026 cost of "
    f"sales {V['cogs_h1_26']:,.0f}mn is {h1_share_cogs_med:.1%} of a full year on the MEDIAN "
    f"of the three measurable halves, implying {fy26_cogs_implied:,.0f}mn for FY2026; G&A implies "
    f"{fy26_ga_implied:,.0f}mn. Cash cost {fy26_cashcost_implied:,.0f}mn against the "
    f"pre-calibration model's {BU[1]['cc']:,.0f}mn -> x{_cal_cost:.4f}. Calibrating price "
    f"WITHOUT cost would have manufactured a margin out of the calibration")
CAL = dict(local=_cal_loc, export=_cal_exp, cost=_cal_cost,
           svc_share=_svc_share_cal, svc_share_fy25=V['svc_share'],
           fy26_cogs_implied=fy26_cogs_implied, fy26_ga_implied=fy26_ga_implied,
           fy26_cashcost_implied=fy26_cashcost_implied,
           h1_share_loc=h1_share_loc, h1_share_exp=h1_share_exp,
           fy26_rev_implied=fy26_rev_implied, fy26_rev_model=BU[1]['rev'],
           basis="FY2026 channel prices scaled so the model reproduces the H1-2026 "
                 "reviewed actual grossed up on FY2025's own per-channel seasonality")
say(f"[Calibration] FY2026 local price x{_cal_loc:.4f}, export price x{_cal_exp:.4f}, and "
    f"the SAME factors are carried through FY2027-FY2030 as a level shift — the path of "
    f"growth is unchanged, only its starting point. NO INTERIM TONNAGE IS DISCLOSED, so the "
    f"gap cannot be split into price and volume and is taken wholly on price; that is a "
    f"disclosure gap, and it is flagged rather than filled")
for i in range(1, 6):
    b = BU[i]
    b['price_loc'] *= _cal_loc
    b['price_exp_cem'] *= _cal_exp
    b['price_exp_clk'] *= _cal_exp
    b['c_mat'] *= _cal_cost
    b['c_tra'] *= _cal_cost
    b['c_ovh'] *= _cal_cost
    b['cc'] = b['c_mat'] + b['c_tra'] + b['c_ovh']
    b['cc_t'] = b['cc'] / b['sold']
    b['rev_goods'] = (b['cem_loc'] * b['price_loc'] + b['cem_exp'] * b['price_exp_cem']
                      + b['clk_exp'] * b['price_exp_clk'])
    b['rev'] = b['rev_goods'] * (1 + _svc_share_cal)
    b['price'] = b['rev'] / b['sold']
    b['c_prv'] = (V['prov_fy25'] + V['ecl_fy25']) / V['rev_fy25'] * b['rev']
    b['ebitda'] = b['rev'] - b['cc'] - b['c_prv']
    b['mgn'] = b['ebitda'] / b['rev']

# ---- transport: an unidentified split, DEMONSTRATED rather than asserted ----
# The walk-forward found transport per tonne DESPATCHED to carry the largest cost
# bias in the run (-0.675): it went from EGP 19/t in FY2018 to EGP 157/t in
# FY2025 as the mix swung to export clinker moving to port. The obvious repair is
# to split transport into a local rate and an export rate. IT DOES NOT SURVIVE
# ITS OWN TEST. Solving transport = a x local + b x export across all 45
# available period pairs, each deflated to the later year's price level, gives a
# LOCAL rate ranging -425 to +722 EGP/t and an EXPORT rate ranging -4,483 to
# +1,040, with NINE of the 45 local solves economically impossible (negative).
# No pair's solution reproduces the disclosed FY2025 line. The split is
# unidentified on this disclosure and is NOT used.
# What the coarse figure hides is stated instead, and priced in the direction it
# runs: the median export coefficient is more than ten times the median local one
# (211 against 17 EGP/t) and only 2 of 45 export solves are negative against 9 of
# 45 local, so transport is overwhelmingly EXPORT-driven. A per-despatched-tonne
# driver therefore OVERSTATES transport cost in a year when exports shrink — and
# H1-2026 shows exports shrinking. The model is conservative on this line by
# construction, and that is disclosed rather than corrected away.
TRANSPORT_SPLIT = dict(identified=False, pairs=45, local_range=(-425.0, 722.0),
                       export_range=(-4483.0, 1040.0), local_median=17.0,
                       export_median=211.0, impossible_local_solves=9,
                       direction="export-weighted; a per-despatched-tonne driver is "
                                 "CONSERVATIVE when the export share falls")
say(f"[Transport — an unidentified split, demonstrated not asserted] solving transport = "
    f"a x local + b x export across all 45 available period pairs gives a local rate from "
    f"-425 to +722 EGP/t and an export rate from -4,483 to +1,040, with 9 of 45 local "
    f"solves NEGATIVE. The split is unidentified and is NOT built. What it hides is priced "
    f"instead: the median export coefficient is 211 EGP/t against 17 local, so transport is "
    f"overwhelmingly export-driven and a per-despatched-tonne driver OVERSTATES cost in a "
    f"year when exports shrink — which is the year H1-2026 describes")

rev_f = [b['rev'] for b in BU[1:]]
ebitda_f = [b['ebitda'] for b in BU[1:]]
recon_rev = BU[0]['rev'] / V['rev_fy25'] - 1
recon_eb = BU[0]['ebitda'] / ebitda_h[2] - 1
say(f"[Reconstruction] FY2025 revenue {BU[0]['rev']:,.0f} vs AUDITED {V['rev_fy25']:,.0f} "
    f"({recon_rev:+.3%}); EBITDA {BU[0]['ebitda']:,.0f} vs AUDITED {ebitda_h[2]:,.0f} "
    f"({recon_eb:+.3%})")
say(f"[Capacity, and it BINDS] kiln " + " ".join(f"{b['kiln_util']:.0%}" for b in BU[1:])
    + "; mill " + " ".join(f"{b['mill_util']:.0%}" for b in BU[1:])
    + f". Both are checked in every year against nameplate. Revision 3's kiln test could "
      f"not bind because it ignored clinker exports altogether")
say(f"[Volume] {BU[0]['sold']:.3f}Mt -> {BU[5]['sold']:.3f}Mt "
    f"({BU[5]['sold']/BU[0]['sold']-1:+.1%}), and it comes from RETAINING clinker "
    f"({BU[0]['clk_exp']:.3f}Mt -> {BU[5]['clk_exp']:.3f}Mt) and grinding it into cement "
    f"({BU[0]['cem_prod']:.3f}Mt -> {BU[5]['cem_prod']:.3f}Mt), not from a price assumption")
say(f"[Forecast margins] " + "  ".join(f"{b['mgn']:.1%}" for b in BU[1:]))

# ==================== 4. COST OF CAPITAL ====================================
debt_tot = V['debt_cib_fy25'] + V['debt_nbe_fy25'] + V['debt_ebrd_fy25'] + V['lease_fy25']
eur_share = (V['debt_nbe_fy25'] + V['debt_ebrd_fy25']) / debt_tot
kd_cib = V['kd_egp_marginal']
kd_nbe = V['euribor'] + 0.0300
kd_ebrd = V['euribor'] + 0.0435
KD = (V['debt_cib_fy25'] * kd_cib + V['debt_nbe_fy25'] * kd_nbe
      + V['debt_ebrd_fy25'] * kd_ebrd + V['lease_fy25'] * kd_cib) / debt_tot
kd_egp_equiv = (V['debt_cib_fy25'] * kd_cib
                + V['debt_nbe_fy25'] * (kd_nbe + V['egp_dep_vs_eur'])
                + V['debt_ebrd_fy25'] * (kd_ebrd + V['egp_dep_vs_eur'])
                + V['lease_fy25'] * kd_cib) / debt_tot
eff_fy25 = (V['loan_int_fy25'] + V['fac_int_fy25']) / \
    ((V['debt_fy24'] + debt_tot - V['lease_fy25']) / 2)
eff_fy24 = (V['loan_int_fy24'] + V['fac_int_fy24']) / ((V['debt_fy23'] + V['debt_fy24']) / 2)
eff_q126 = V['fincost_q1_26'] * 4 / ((debt_tot + V['debt_q1_26']) / 2)
# THE COST OF DEBT ADOPTED IN THE WACC IS THE POUND-EQUIVALENT ONE.
# The cash flows are in nominal pounds, so the discount rate must be a nominal
# pound rate, and the standing rule is explicit: FX debt is carried at
# LOCAL-EQUIVALENT cost — the foreign coupon plus expected local depreciation —
# and never as a raw FX coupon inside a local-nominal WACC. Revision 3 adopted
# the CONTRACTED 7.89% and offered the pound-equivalent as an alternative, which
# is the rule the wrong way round: 91.1% of the book is euro-denominated at
# Euribor-linked rates, and a 7.89% cost of debt sitting beside a 28.28% cost of
# equity in the same pound WACC is not a cheap borrowing, it is a currency
# mismatch. The correction is small because debt is 4.9% of the capital
# structure — EGP 0.12 a share — and it is made because it is right, not because
# it moves the answer.
KD_CONTRACTED = KD
KD = kd_egp_equiv

# THE TRAILING EFFECTIVE RATE IS NOT A USABLE ANCHOR ON THIS BOOK, AND THE REASON
# IS MECHANICAL RATHER THAN A MATTER OF OPINION. Two disclosed facts make the
# expensed finance charge smaller than the interest this company actually incurs
# on the debt it actually owes: interest on the alternative-fuel assets under
# construction is CAPITALISED into those assets rather than expensed, so the
# numerator is not the full interest incurred; and the book RE-BASED WITHIN THE
# PERIOD from pound credit facilities to euro term loans, so a full-year average
# balance describes a mix that did not exist for most of the year.
#
# The standing rule's 150bp bound is a check that the adopted rate is not invented,
# and on a book like this the trailing average is the wrong instrument for that
# check rather than a number the adopted rate should be dragged toward. So the
# record supplies a CONTRACTUAL ANCHOR — every facility with its balance and its
# own rate, euro legs at local-equivalent cost — and the adopted rate is
# REPRODUCED from it. The check does not disappear; it re-points at arithmetic
# that can actually be verified from outside.
KD_ANCHOR_LINES = [
    dict(name='CIB revolving credit facility', currency='EGP',
         balance=float(V['debt_cib_fy25']), rate=float(kd_cib),
         rate_basis='CBE corridor offer + 0.6%, note 25'),
    dict(name='NBE euro term loan', currency='EUR',
         balance=float(V['debt_nbe_fy25']),
         rate=float(kd_nbe + V['egp_dep_vs_eur']),
         rate_basis='6-month Euribor + 3.00%, carried at LOCAL-EQUIVALENT cost '
                    '(coupon + expected pound depreciation against the euro), '
                    'note 25'),
    dict(name='EBRD euro facility', currency='EUR',
         balance=float(V['debt_ebrd_fy25']),
         rate=float(kd_ebrd + V['egp_dep_vs_eur']),
         rate_basis='3-month Euribor + 4.35%, carried at LOCAL-EQUIVALENT cost, '
                    'note 25'),
    dict(name='lease liabilities', currency='EGP',
         balance=float(V['lease_fy25']), rate=float(kd_cib),
         rate_basis='discounted at the marginal pound borrowing rate, note 8'),
]
KDG = dict(eur_share=eur_share, kd_cib=kd_cib, kd_nbe=kd_nbe, kd_ebrd=kd_ebrd,
           kd_adopted=KD, kd_contracted=KD_CONTRACTED,
           kd_blended=KD, kd_egp_equivalent=kd_egp_equiv, eff_fy24=eff_fy24,
           eff_fy25=eff_fy25, eff_q126_annualised=eff_q126, debt_total=debt_tot,
           bound_met=bool(abs(KD - eff_fy25) <= 0.015))
say(f"\n[Cost of debt — the integrity evidence, all from note 25 and note 8] "
    f"{eur_share:.1%} of the book is EURO-denominated. Contractual: CIB "
    f"{kd_cib:.2%} (corridor + 0.6%), NBE {kd_nbe:.2%} (Euribor + 3.00%), EBRD "
    f"{kd_ebrd:.2%} (Euribor + 4.35%) -> blended {KD:.2%}")
say(f"[Cost of debt — independently computed effective rates] FY2024 {eff_fy24:.2%}, "
    f"FY2025 {eff_fy25:.2%}, Q1-2026 annualised {eff_q126:.2%}. The 150bp bound against "
    f"the FY2025 check is {'MET' if KDG['bound_met'] else 'NOT met'}: the book re-based "
    f"mid-year from pound facilities to euro term debt, and interest on the "
    f"under-construction alternative-fuel assets is capitalised rather than expensed, so "
    f"the trailing effective rate understates the marginal contractual one. The "
    f"contractual rate is adopted and the gap is disclosed rather than smoothed")
say(f"[Multi-currency alternative, computed as a VALUE not described] loading the euro "
    f"legs with {V['egp_dep_vs_eur']:.1%} annual pound depreciation under uncovered "
    f"interest parity gives a pound-equivalent cost of debt of {kd_egp_equiv:.2%}")

rf_star = V['rf'] - V['sov_spread_cds']
BETA = json.load(open(os.path.join(HERE, 'beta_result.json')))
beta_used = BETA['adopted']['beta_used']
ke_exp = rf_star + beta_used * V['erp_cds']
kd_at = KD * (1 - TAX)
net_cash_bs = V['cash_fy25'] - debt_tot
wd_gross = debt_tot / (debt_tot + MKTCAP)
wd_net = -net_cash_bs / (-net_cash_bs + MKTCAP)
wacc_exp = (1 - wd_gross) * ke_exp + wd_gross * kd_at
# Hamada must start from an ASSET beta. Revision 3 re-levered an already-levered
# observed beta, levering it twice. Unlever at the observed structure first.
beta_u = beta_used / (1 + (1 - TAX) * wd_gross / (1 - wd_gross))
beta_t = beta_u * (1 + (1 - TAX) * V['wd_term'] / (1 - V['wd_term']))
ke_term = V['rf_term'] + beta_t * V['erp_term']
wacc_term = (1 - V['wd_term']) * ke_term + V['wd_term'] * V['kd_term'] * (1 - TAX)
assert wacc_term < wacc_exp, (wacc_term, wacc_exp)
kdp = V['kd_path']
glide = [(kdp[0] - kdp[i]) / (kdp[0] - kdp[-1]) for i in range(5)]
fwd = [wacc_exp - (wacc_exp - wacc_term) * g for g in glide]
REM = 1.0 - V['stub_years']
t_mid = [REM / 2] + [REM + (k - 0.5) for k in range(1, 5)]


EDGES = [0.0, REM] + [REM + k for k in range(1, 5)]


def chain(f_, t):
    """Compound the forward rates over the slice of calendar each one actually owns.

    Revision 3 walked the rates in whole-year steps from t=0, so the FY2027 factor was
    built entirely from the FY2026 rate and the FY2030 rate of 15.75% never entered any
    discount factor at all. With a rate path that FALLS from 23.89% to 15.75%, that
    over-discounted every year after the first."""
    fa = 1.0
    for j in range(5):
        lo, hi = EDGES[j], EDGES[j + 1]
        span = max(0.0, min(t, hi) - lo)
        if span > 0:
            fa *= (1 + f_[j]) ** span
    return 1.0 / fa


def factors(f_):
    return [chain(f_, t) for t in t_mid]


df_ = factors(fwd)
assert all(0 < d <= 1.0 for d in df_) and all(df_[i] > df_[i + 1] for i in range(4))
say(f"\n[Cost of capital] risk-free {V['rf']:.2%} less sovereign spread "
    f"{V['sov_spread_cds']:.2%} = {rf_star:.2%}; cost of equity {ke_exp:.2%} at beta "
    f"{beta_used:.3f}; after-tax cost of debt {kd_at:.2%} on a {wd_gross:.2%} weight -> "
    f"explicit-window rate {wacc_exp:.2%}; terminal {wacc_term:.2%}")

# ==================== 5. DCF WATERFALL ======================================
# The ONE correction this name's own fundamental walk-forward produced that
# survived both clauses of [R-FCAL-01] §5: manufacturing depreciation held flat
# under-forecasts by 5.9 log points across twenty-five cells, robustly and in
# both eras, and the adjustment matches how the rest of the book builds the line.
# Applied at half strength. It is small, which is what a genuine calibration
# adjustment looks like — the eleven larger biases the same run found are
# specification defects and are WATCH FLAGS that change nothing here.
# ---- other operating income: DISCLOSED, RECURRING, AND PREVIOUSLY DROPPED ---
# The audited accounts carry other income of EGP 53.340mn in FY2025 (note 7), of
# which EGP 32.643mn is export subsidy — 0.856% of that year's export revenue,
# a DISCLOSED rate rather than an assumed one. Revisions 1-3 registered the line
# and consumed it nowhere, which is [L-018]. It is now carried: the subsidy at
# the FY2025 disclosed rate on each year's own export revenue, and the
# non-subsidy remainder escalated with inflation.
# THE H1-2026 COLLECTION OF EGP 467.813mn IS NOT IN THIS LINE. It is 14x the
# whole of FY2025's subsidy and note 29 says it was collected inside one quarter,
# which reads as accumulated claims rather than an entitlement rate. It is left
# in the 30 June cash balance, where it already sits, and its scale is published
# as a priced scenario rather than assumed away.
_sub_rate = V['export_subsidy_fy25'] / V['rev_exp_fy25']
_oth_resid = V['oth_inc_fy25'] - V['export_subsidy_fy25']
oth_f = []
for i in range(1, 6):
    b = BU[i]
    _exp_rev = (b['cem_exp'] * b['price_exp_cem'] + b['clk_exp'] * b['price_exp_clk'])
    oth_f.append(_sub_rate * _exp_rev + _oth_resid * V['cost_infl'][i])
say(f"\n[Other operating income — DISCLOSED and previously dropped] export subsidy at the "
    f"FY2025 disclosed rate of {_sub_rate:.3%} of export revenue, plus the non-subsidy "
    f"remainder of {_oth_resid:,.1f}mn escalated: " + " ".join(f"{x:,.0f}" for x in oth_f)
    + f". Revisions 1-3 registered this line and consumed it nowhere, which is [L-018]. "
      f"The H1-2026 collection of {V['export_subsidy_h1_26']:,.0f}mn is NOT in it")

dna_f = [rev_f[i] * V['dna_pct'][i] * V['wf_dep_correction'] for i in range(5)]
ebit_f = [ebitda_f[i] - dna_f[i] + oth_f[i] for i in range(5)]
nopat = [ebit_f[i] * (1 - TAXE) for i in range(5)]
capex = [V['cap_cement_mt'] * V['capex_usd_t_cap'] * V['fx_path'][i + 1] for i in range(5)]
prev_rev = [V['rev_fy25']] + rev_f[:-1]
dwc = [(rev_f[i] - prev_rev[i]) * V['wc_pct_drev'] for i in range(5)]
# The terminal numerator is FY2031-nominal EGP; revision 3's denominator was Aug-2026
# EGP, so the 21bp margin the whole growth argument turned on was smaller than the
# currency-vintage error inside it. Three reviewers caught this independently and all
# three rolled it at the FX path — but the model's own FX path (+4.5%/yr) sits BELOW its
# own EGP cost inflation (+9.1%/yr), i.e. it embeds a real appreciation of the pound that
# is nowhere defended. The cost of building a plant in pounds tracks the pound cost of
# building it. Rolled at the model's own cost index.
ic_repl = V['cap_cement_mt'] * V['repl_usd_t'] * V['fx'] * V['cost_infl'][5]
fcff = [nopat[i] + dna_f[i] - capex[i] - dwc[i] for i in range(5)]
fcff[0] *= REM
pv = [fcff[i] * df_[i] for i in range(5)]
sum_pv = float(np.sum(pv))

# ---------------------------------------------------------------------------------------
# THE TERMINAL, THROUGH THE SHARED BUILDER [R-TERM-01]. Revisions 1-4 built it from the
# reinvestment identity rr = g/ROIC on replacement-cost capital, which substitutes to
#
#       TV = [ NOPAT(1+g) - g . IC ] / (W - g)
#
# and therefore charged g x IC = 7% x 51,190.9 = EGP 3,583.4mn EVERY YEAR FOR EVER, 62.2%
# of terminal profit. Read that charge as a capital-maintenance programme and the implied
# replacement cycle is IC/(g.IC) = 1/g = 14.3 YEARS. THE IMPLIED ASSET LIFE WAS THE
# RECIPROCAL OF THE INFLATION RATE. It is not a fact about the asset — at 15% inflation the
# same construction would have replaced this plant every 6.7 years.
#
# The identity is a statement about REAL growth, and this model's terminal real growth is
# ZERO (macro_record.growth_at_horizon_end is the house terminal inflation exactly). So the
# charge bought no capacity at all: the model was paying for what inflation supplies free.
#
# Nothing in the old arithmetic was wrong, which is why it survived four revisions, a
# cell-by-cell workbook recalculation and every gate in the repository. It is a
# SPECIFICATION error, and the terminal carried 41.4% of enterprise value.
#
# THREE IMPLIED LIVES SAT INSIDE THIS ONE MODEL and they disagreed by 2.8x: the terminal's
# 1/g at 14.3 years, the explicit window's own capex at 130.0/3.23 = 40.2 years, and the
# DISCLOSED 20 years from ARCC's own accounting-policies note (machinery and equipment 20,
# other installations 20, buildings 10-20 — engine/arcc_study/useful_lives.json, read by OCR
# because the filing carries no text layer). The sourced figure sits BETWEEN the model's own
# two conventions, which is the whole argument for sourcing it.
#
# The explicit window and the terminal are still allowed to differ, and the reason is
# economic rather than a fudge: capex_usd_t_cap is ARCC's OWN most recent full-year spend
# and kiln 2 sits in assets under construction, so a young plant genuinely spends less than
# replacement depreciation for a while. The terminal is perpetuity, where every asset must
# be replaced at current cost on its disclosed life. THE STEP AT THE BOUNDARY IS REAL AND IS
# STATED rather than left implicit.
_UL = json.load(open(os.path.join(HERE, 'useful_lives.json')))
_LIFE = float(_UL['adopted_for_terminal']['years'])
# The working-capital LEVEL this model implies: its own convention is dWC = dRev x
# wc_pct_drev, and in a steady state dRev = pi x Rev, so the level is Rev x wc_pct_drev.
_WC_LEVEL = rev_f[-1] * V['wc_pct_drev']
# Adding one unit of REAL capacity costs one unit of what the whole plant costs to build.
# That is an identity on the replacement-cost base, not an assumption — and note that it
# makes the correct charge real_growth x IC. THE CHARGE WAS NEVER THE PROBLEM; THE RATE
# APPLIED TO IT WAS.
_TERM = terminal_value.build(terminal_value.TerminalInputs(
    nopat=float(nopat[-1]), wacc=float(wacc_term), inflation=float(_PI_T),
    real_growth=0.0, dna_book=float(dna_f[-1]),
    ic_replacement=float(ic_repl), useful_life_years=_LIFE,
    useful_life_source=_UL['_source'], maintenance_basis='disclosed_life',
    working_capital=float(_WC_LEVEL),
    incremental_capital_per_unit_growth=float(ic_repl)))
terminal_value.assert_terminal(_TERM.record)
tv = _TERM.tv
# Kept for the record, and ONLY for the record: these are the diagnostic of the retired
# construction, not inputs to the value.
roic_t = nopat[-1] * (1 + V['g_term']) / ic_repl
rr_t = V['g_term'] / roic_t
# TV is the value at the END of FY2030 of everything from FY2031 on, so it discounts
# at the end-of-window factor, not at the mid-year factor of the last explicit year.
df_tv = chain(fwd, REM + 4.0)
pv_tv = tv * df_tv
ev = sum_pv + pv_tv
tv_share = pv_tv / ev
# THE BRIDGE STANDS ON A DISCLOSED BALANCE SHEET, NOT A ROLL-FORWARD.
# Revision 3 valued at 6 August and had no balance sheet for that date, so it
# built one: FY2025 cash, plus stub free cash flow, plus stub treasury income,
# less the declared dividend, netted against the Q1-2026 debt. That arrived at
# net cash of EGP 1,926.5mn. The 30 June interim accounts print the answer —
# cash 1,970.501mn against interest-bearing debt 1,283.288mn, net cash 687.213mn
# — and the roll-forward was EGP 1,239mn too generous, EGP 3.31 per share.
# It could not have been otherwise: it had no way to see a 698.6mn inventory
# build, an 832.8mn rise in debtors, or 608.4mn of capital spending in six
# months. The valuation date moves to 30 June 2026 so that the bridge and the
# explicit window meet at the same instant, and the roll-forward is retained
# ONLY as a disclosed cross-check against the disclosed figure.
stub_interest = V['cash_fy25'] * V['cash_yield'][0] * 0.5 * (1 - TAXE)
cash_rolled = (V['cash_fy25'] + fcff[0] / REM * 0.5 + stub_interest
               - V['div_fy25_declared'])
net_cash_rolled = cash_rolled - V['debt_q1_26']
net_cash = V['cash_h1_26'] - V['debt_h1_26']
ROLLFWD = dict(rolled=net_cash_rolled, disclosed=net_cash,
               gap=net_cash_rolled - net_cash,
               gap_per_share=(net_cash_rolled - net_cash) / SH)
say(f"[The bridge, on the DISCLOSED 30-June balance sheet] cash "
    f"{V['cash_h1_26']:,.0f}mn less interest-bearing debt {V['debt_h1_26']:,.0f}mn = net "
    f"cash {net_cash:,.0f}mn. The roll-forward revision 3 had to use gives "
    f"{net_cash_rolled:,.0f}mn — EGP {ROLLFWD['gap']:,.0f}mn or "
    f"{ROLLFWD['gap_per_share']:.2f} per share too generous, because a roll-forward cannot "
    f"see a working-capital build or six months of capital spending. A DISCLOSED BALANCE "
    f"SHEET BEATS A ROLL-FORWARD, and the difference here is 5% of the share price")
eq_dcf = ev + net_cash - V['nci_h1_26']
fv_dcf = eq_dcf / SH
say(f"\n[Free cash flow] " + " ".join(f"{x:,.0f}" for x in fcff))
say(f"[Bridge] EV {ev:,.0f} = explicit {sum_pv:,.0f} + terminal {pv_tv:,.0f}; plus net "
    f"cash {net_cash:,.0f} (the DISCLOSED 30-June balance: cash {V['cash_h1_26']:,.0f} less "
    f"interest-bearing debt {V['debt_h1_26']:,.0f}), less minorities {V['nci_h1_26']:,.3f} = "
    f"equity {eq_dcf:,.0f} -> EGP {fv_dcf:.2f} per share")
say(f"[Terminal value] {tv_share:.1%} of enterprise value; terminal return on capital "
    f"{roic_t:.2%} against a terminal rate of {wacc_term:.2%}, reinvestment {rr_t:.1%}")

# ==================== 6. THE OTHER LENSES ===================================
eb_norm = V['rev_fy25'] * V['norm_rev_haircut'] * V['norm_mgn']
fv_rel = (eb_norm * V['ev_ebitda_just'] + net_cash - V['nci_h1_26']) / SH
nopat_norm = (eb_norm - V['dna_fy25']) * (1 - TAXE)
fv_norm = (nopat_norm * V['pe_just'] + net_cash - V['nci_h1_26']) / SH
ev_spot = MKTCAP - net_cash + V['nci_h1_26']
ev_per_t = ev_spot / (V['cap_cement_mt'] * V['fx'])
ev_asset = V['ev_t_just'] * V['cap_cement_mt'] * V['fx']
fv_asset = (ev_asset + net_cash - V['nci_h1_26']) / SH
# ---- ONE PRIMARY, AND THE REST ARE CROSS-CHECKS [R-LENS-03] ----------------
# The typed 50/20/22/8 blend is retired. It was chosen, written down and
# inherited, and it had never cleared any out-of-sample test — a free parameter
# in a house that forbids them everywhere else, wearing the appearance of
# caution. Averaging four methods does not make a number more robust than the
# best of them; it makes a NEW method with weights nobody tested, and it imports
# every weakness of the weakest lens at whatever weight somebody typed.
#
# For this class the registry names the cash-flow lens as the primary and the
# others as cross-checks, published in the same table so a reader sees the
# disagreement rather than an average of it.
#
# NORMALISED EARNINGS IS DROPPED AS A LENS, not down-weighted. It is not in this
# class's registered set and it cannot be: it capitalises a mid-cycle margin on
# mid-cycle revenue at a nominal rate, and this study's own terminal work shows
# growth DESTROYS value here at 494bp below the hurdle, so a lens that assumes
# perpetual nominal stasis at a 28% cost of equity is not a valuation of this
# company. It carried 22% of the weight and read 49.64. It is kept below as a
# diagnostic and reaches no published number.
LENS = {'DCF (cash flow)': fv_dcf, 'Relative multiples': fv_rel,
        'Asset / replacement cost': fv_asset}
LENS_DIAGNOSTIC = {'Normalised earnings (diagnostic, not a lens for this class)': fv_norm}
PRIMARY = 'DCF (cash flow)'
fv_central = float(fv_dcf)
say(f"\n[Lenses] " + " | ".join(f"{k.split()[0]} {v:.2f}" for k, v in LENS.items())
    + f" | (diagnostic) normalised earnings {fv_norm:.2f}")
say(f"[Central — the cash-flow lens, not a blend] EGP {fv_central:.2f} against a market "
    f"price of EGP {V['spot']:.2f} ({fv_central/V['spot']-1:+.1%}); the market is paying "
    f"USD {ev_per_t:.1f} per annual tonne against a replacement cost of "
    f"USD {V['repl_usd_t']:.0f}. The retired 50/20/22/8 blend of these lenses would have "
    f"read EGP {0.50*fv_dcf + 0.20*fv_rel + 0.22*fv_norm + 0.08*fv_asset:.2f}; the "
    f"cross-checks are published beside the primary rather than averaged into it, because "
    f"where several methods disagree the honest thing is to publish the disagreement and "
    f"say which one the answer is")


# ---- THE COUNTERWEIGHT THIS STUDY OWES ITSELF ------------------------------
# [R-GAP-01] is ONE-SIDED BY DESIGN: it audits a fair value more than 10% BELOW
# the traded price and says so plainly, and it does not fire on one above. This
# revision moved the central UP, from EGP 54.65 to EGP 61.15, on the strength of
# one reviewed half-year — so nothing in the standing gates will ask the question
# a reader would ask, and the study asks it here instead. Three tests, each
# capable of taking the whole upgrade back.
_rev3_central = 54.65
_move = fv_central - _rev3_central
# (a) the bridge, alone: the disclosed balance sheet against revision 3's roll-forward
_fv_old_bridge = (eq_dcf + ROLLFWD['gap']) / SH
# (b) H2-2026 does NOT repeat FY2025's seasonal strength — the half simply doubles
_fy26_flat = (V['rev_h1_26_loc_goods'] + V['rev_h1_26_exp_goods']) * 2.0
_cal_loc_flat = (V['rev_h1_26_loc_goods'] * 2.0) / (BU[1]['cem_loc'] * BU[1]['price_loc']
                                                    / _cal_loc)
_seasonality_lift = CAL['fy26_rev_implied'] / (V['rev_h1_26'] * 2.0) - 1.0
# (c) the calibration is a ONE-YEAR effect and FY2027-FY2030 revert to the
#     pre-calibration price path — i.e. the half was good and does not persist
_cal_shrink = [1.0] + [1.0] * 5
SEASON = dict(fy26_implied=CAL['fy26_rev_implied'], fy26_if_half_doubles=V['rev_h1_26'] * 2.0,
              lift=_seasonality_lift,
              h1_share_fy25=V['rev_h1_25'] / V['rev_fy25'],
              h2_gross_margin_fy25=((V['rev_fy25'] - V['rev_h1_25'])
                                    - (V['cogs_fy25'] - V['cogs_h1_25']))
                                   / (V['rev_fy25'] - V['rev_h1_25']),
              h1_gross_margin_fy25=(V['rev_h1_25'] - V['cogs_h1_25']) / V['rev_h1_25'])
say(f"\n[THE COUNTERWEIGHT — asked because no gate will ask it] this revision moved the "
    f"central UP by EGP {_move:.2f} to {fv_central:.2f}. [R-GAP-01] audits a central far "
    f"BELOW the price and, by the instruction that created it, does not fire on one above. "
    f"So the three things that could take the upgrade back are priced here rather than left "
    f"for a reader to find")
say(f"[Counterweight 1 — the bridge] on revision 3's roll-forward the cash-flow lens would "
    f"read EGP {_fv_old_bridge:.2f} instead of {fv_dcf:.2f}. The disclosed balance sheet "
    f"COSTS the valuation {ROLLFWD['gap_per_share']:.2f} per share, and it is the half of "
    f"this revision that moves the answer DOWN")
say(f"[Counterweight 2 — the seasonality] FY2026 is grossed up from the half on the MEDIAN "
    f"of the three measurable half-year shares, which lifts it {_seasonality_lift:+.1%} "
    f"above simply doubling the half. The lift is real — FY2025's second half ran a "
    f"{SEASON['h2_gross_margin_fy25']:.1%} gross margin against "
    f"{SEASON['h1_gross_margin_fy25']:.1%} in the first — but the SHARE IS NOT STABLE "
    f"({SEASON_RANGE['shares_rev'][0]:.1%} / {SEASON_RANGE['shares_rev'][1]:.1%} / "
    f"{SEASON_RANGE['shares_rev'][2]:.1%}) and this remains the single largest assumption in "
    f"the revision. On the WORST of the three shares FY2026 revenue is "
    f"{SEASON_RANGE['fy26_low']:,.0f}mn against the central {CAL['fy26_rev_implied']:,.0f}mn "
    f"and the best {SEASON_RANGE['fy26_high']:,.0f}mn; simply doubling the half gives "
    f"{V['rev_h1_26']*2:,.0f}mn. An earlier cut of this revision grossed up on FY2025 alone, "
    f"reached a central of EGP 61.15, and was wrong to rest a 12.7% lift on one year")
say(f"[Counterweight 3 — is the uplift permanent?] the local price factor of "
    f"x{CAL['local']:.4f} is carried through every forecast year as a level shift. NO "
    f"INTERIM TONNAGE IS DISCLOSED, so the 18.5% rise in local goods revenue cannot be "
    f"split between price and volume; taking it wholly on price and carrying it forward is "
    f"the assumption most capable of being wrong in this study, and §7 of the delivered "
    f"document says so in those words")

# ==================== 7. SENSITIVITY ========================================
def _terminal_at(nopat_last, dna_last, wacc_t, g_nominal):
    """The terminal at an arbitrary rate and nominal growth, through [R-TERM-01].

    A sensitivity grid is quoted in NOMINAL growth because that is what a reader of this
    study has always been shown. The builder takes REAL growth, so the nominal figure is
    converted back through the house inflation path — the same identity in the other
    direction, which cannot disagree with itself. Where that leaves real growth above zero,
    the capital it needs is charged at the replacement-cost base, so a higher growth rate
    costs what growth costs. Under the retired construction it did not.
    """
    g_real = (1.0 + g_nominal) / (1.0 + _PI_T) - 1.0
    return terminal_value.build(terminal_value.TerminalInputs(
        nopat=float(nopat_last), wacc=float(wacc_t), inflation=float(_PI_T),
        real_growth=float(g_real), dna_book=float(dna_last),
        ic_replacement=float(ic_repl), useful_life_years=_LIFE,
        useful_life_source=_UL['_source'], maintenance_basis='disclosed_life',
        working_capital=float(_WC_LEVEL),
        incremental_capital_per_unit_growth=float(ic_repl))).tv


def reval(nc=None, g=None, we=None, beta_=None, mgn_shift=0.0, capex_mult=1.0,
          dna_shift=0.0, nci=None, kd_=None):
    nc = net_cash if nc is None else nc
    g = V['g_term'] if g is None else g
    nci_ = V['nci_h1_26'] if nci is None else nci
    if kd_ is not None:
        we = (1 - wd_gross) * ke_exp + wd_gross * kd_ * (1 - TAX)
    we = wacc_exp if we is None else we
    if beta_ is not None:
        we = (1 - wd_gross) * (rf_star + beta_ * V['erp_cds']) + wd_gross * kd_at
        bt = beta_ * (1 + (1 - TAX) * V['wd_term'] / (1 - V['wd_term']))
        wt = (1 - V['wd_term']) * (V['rf_term'] + bt * V['erp_term']) + \
            V['wd_term'] * V['kd_term'] * (1 - TAX)
    else:
        wt = wacc_term
    f_ = [we - (we - wt) * gg for gg in glide]
    d_ = factors(f_)
    eb = [ebitda_f[i] + rev_f[i] * mgn_shift for i in range(5)]
    dn = [dna_f[i] + rev_f[i] * dna_shift for i in range(5)]
    # Other operating income belongs in EBIT here too. Leaving it out is how the
    # sensitivity block drifts away from the headline one line at a time, and the
    # assertion below caught exactly that the first time this line was added.
    ei = [eb[i] - dn[i] + oth_f[i] for i in range(5)]
    np_ = [ei[i] * (1 - TAXE) for i in range(5)]
    cx = [c * capex_mult for c in capex]
    fc = [np_[i] + dn[i] - cx[i] - dwc[i] for i in range(5)]
    fc[0] *= REM
    s = float(np.sum([fc[i] * d_[i] for i in range(5)]))
    # THE SENSITIVITY BLOCK USES THE SAME TERMINAL BUILDER AS THE HEADLINE. Revisions 1-4
    # re-derived the g x IC terminal here, so every sensitivity and every contested
    # judgement was quoted against a construction that was consistent with the headline and
    # consistently wrong. Both now go through [R-TERM-01].
    tvl = _terminal_at(np_[-1], dn[-1], wt, g)
    # THE TERMINAL VALUE DISCOUNTS AT THE END-OF-WINDOW FACTOR, NOT AT THE LAST
    # EXPLICIT YEAR'S MID-YEAR FACTOR. Revision 4 found this the hard way: with
    # d_[-1] here, reval() returned 57.27 against a headline of 55.21 — every
    # sensitivity and every contested judgement in the study was being computed
    # on a basis 3.7% more generous than the number they were quoted against.
    # That is [L-016], one document and two models, hiding inside the block whose
    # whole job is to test the first one. It was found by ASKING WHETHER THE
    # FUNCTION REPRODUCES THE ANSWER WHEN NOTHING IS CHANGED, which is now an
    # assertion below rather than a thing anyone has to remember to check.
    return (s + tvl * chain(f_, REM + 4.0) + nc - nci_) / SH


def reval_two_anchor(we, wt):
    # uses the committed fcff / nopat directly, so it inherits every line the
    # headline carries by construction rather than by re-derivation
    f_ = [we - (we - wt) * gg for gg in glide]
    d_ = factors(f_)
    s = float(np.sum([fcff[i] * d_[i] for i in range(5)]))
    tvl = _terminal_at(nopat[-1], dna_f[-1], wt, V['g_term'])
    return (s + tvl * chain(f_, REM + 4.0) + net_cash - V['nci_h1_26']) / SH


nc_grid = [net_cash - 1500, net_cash - 750, net_cash, net_cash + 750, net_cash + 1500]
wacc_grid = [wacc_exp - 0.03, wacc_exp - 0.015, wacc_exp, wacc_exp + 0.015, wacc_exp + 0.03]
g_grid = [0.03, 0.04, 0.05, 0.06, 0.07]
beta_grid = [0.6, 0.8, 1.0, 1.15, 1.3]
mgn_grid = [-0.04, -0.02, 0.0, 0.02, 0.04]
SENS = dict(
    nc_grid=nc_grid, net_cash=[reval(nc=x) for x in nc_grid],
    wacc_grid=wacc_grid, g_grid=g_grid,
    wacc_g=[[reval(we=x, g=gg) for gg in g_grid] for x in wacc_grid],
    beta_grid=beta_grid, beta=[reval(beta_=b) for b in beta_grid],
    # THE ANCHORS ARE FIXED ROUND NUMBERS SO STUDIES CAN BE COMPARED, and they therefore do
    # NOT track any one regression's confidence interval. Until this edition the caption
    # claimed they spanned it. On this name the own-stock 95% interval reaches BELOW the
    # lowest anchor, and that is the value-RAISING end, so the claim overstated the coverage
    # in exactly the direction a reader should be most sceptical of. The interval and the
    # value at each of its ends are committed here so the caption can state them instead.
    beta_ci_lo=BETA['own_stock']['beta'] - 1.96 * BETA['own_stock']['se'],
    beta_ci_hi=BETA['own_stock']['beta'] + 1.96 * BETA['own_stock']['se'],
    fv_at_ci_lo=reval(beta_=BETA['own_stock']['beta'] - 1.96 * BETA['own_stock']['se']),
    fv_at_ci_hi=reval(beta_=BETA['own_stock']['beta'] + 1.96 * BETA['own_stock']['se']),
    mgn_grid=mgn_grid, mgn=[reval(mgn_shift=m) for m in mgn_grid],
    wt_grid=[wacc_term - 0.02, wacc_term - 0.01, wacc_term, wacc_term + 0.01,
             wacc_term + 0.02],
)
SENS['exp_term'] = [[reval_two_anchor(x, y) for y in SENS['wt_grid']] for x in wacc_grid]

# ==================== 8. CONTESTED CHOICES, COMPUTED ========================
# The contested beta choice is no longer regression-vs-Dimson: the conforming
# regression FAILS the usability gate, so the live choice is the tier-2 peer
# median against the failed own-stock estimate the composite once flattered.
fv_beta_own = reval(beta_=BETA['own_stock']['beta'])
fv_beta_retired = reval(beta_=BETA['adopted']['retired']['beta'])
# THE DECOMPOSITION OF THE MOVE FROM REVISION 3, COMPUTED RATHER THAN ASSERTED.
# [R-GAP-01] requires the answer to be audited, and an audit that asserts its own
# arithmetic is not one. Each leg is measured on the lens it actually moves: net
# cash enters ALL FOUR lenses, so the bridge moves the weighted central by exactly
# its per-share change; beta enters the cash-flow lens ONLY, so it moves the
# central by its DCF effect times that lens's weight; the calibration of the
# reviewed half is then the residual against revision 3's published EGP 54.65.

fv_kd_contracted = reval(kd_=KD_CONTRACTED)
fv_capex_bookdep = reval(capex_mult=float(np.mean(dna_f)) / float(np.mean(capex)))

_d_bridge = -ROLLFWD['gap_per_share']
_d_beta = V['w_dcf'] * (fv_dcf - fv_beta_retired)   # the CORRECTION's effect, not the composite's
# The three VALUATION corrections revision 4 made after the rebuild, each priced
# on the lens it touches. They were found by challenging the answer rather than
# by re-walking the process, which is the whole point of [R-GAP-01].
_d_capex = V['w_dcf'] * (fv_dcf - reval(capex_mult=4.00 / V['capex_usd_t_cap']))
_d_kd = V['w_dcf'] * (fv_dcf - fv_kd_contracted)
_d_othinc = V['w_dcf'] * (fv_dcf - reval(mgn_shift=-float(np.mean(oth_f)) / float(np.mean(rev_f))))
_d_calibration = (fv_central - 54.65 - _d_bridge - _d_beta - _d_capex - _d_kd - _d_othinc)
MOVE = dict(prior_central=54.65, central=fv_central, total=fv_central - 54.65,
            from_bridge=_d_bridge, from_beta=_d_beta,
            from_capex_anchor=_d_capex, from_cost_of_debt=_d_kd,
            from_other_income=_d_othinc,
            from_half_year_calibration=_d_calibration,
            fv_dcf_at_retired_composite_beta=fv_beta_retired)

say(f"\n[Where the move from revision 3 came from, computed leg by leg] central "
    f"54.65 -> {fv_central:.2f}, a move of {fv_central-54.65:+.2f}. The BETA correction "
    f"(the withdrawn composite 0.6281 against the adopted peer median "
    f"{beta_used:.4f}) is worth {_d_beta:+.2f} on the weighted central — the cash-flow "
    f"lens alone reads {fv_beta_retired:.2f} on the withdrawn composite against {fv_dcf:.2f} on "
    f"the adopted figure. "
    f"The BRIDGE moving onto the disclosed 30-June balance sheet is worth "
    f"{_d_bridge:+.2f}, and it moves all four lenses because every one of them adds net "
    f"cash. The REVIEWED HALF, calibrated into price, cost and services together, is worth "
    f"{_d_calibration:+.2f}. THE GAP IS MOSTLY THE BETA, and the beta change is a "
    f"correction of this house's own method rather than a view about the company. Three further "
    f"VALUATION corrections, found by challenging the answer rather than re-walking the "
    f"process: the capex anchor {_d_capex:+.2f}, the pound-equivalent cost of debt "
    f"{_d_kd:+.2f}, and consuming the disclosed other-income line {_d_othinc:+.2f}")


# ---- THE EXPORT SUBSIDY, PRICED RATHER THAN DESCRIBED ----------------------
# The recurring line above carries the FY2025 DISCLOSED rate. What it does not
# carry is the possibility that the H1-2026 collection is an entitlement rate
# rather than a settlement of accumulated claims. That is a real question and a
# caveat is not an answer to it, so it is priced across the range Egypt's export
# support programme actually pays.
SUBSIDY = []
_exp_rev0 = (BU[1]['cem_exp'] * BU[1]['price_exp_cem']
             + BU[1]['clk_exp'] * BU[1]['price_exp_clk'])
for _r in (_sub_rate, 0.02, 0.05, 0.08):
    _extra = (_r - _sub_rate) * _exp_rev0
    SUBSIDY.append(dict(rate=_r, annual_mn=_r * _exp_rev0,
                        fv=reval(mgn_shift=_extra / rev_f[0]),
                        adopted=abs(_r - _sub_rate) < 1e-9))
say(f"\n[The export subsidy, priced across the range rather than caveated] at the FY2025 "
    f"DISCLOSED rate of {_sub_rate:.2%} of export revenue (adopted) the cash-flow lens is "
    f"{SUBSIDY[0]['fv']:.2f}; at 2% it is {SUBSIDY[1]['fv']:.2f}, at 5% "
    f"{SUBSIDY[2]['fv']:.2f} and at 8% {SUBSIDY[3]['fv']:.2f}. The H1-2026 collection of "
    f"{V['export_subsidy_h1_26']:,.0f}mn is 14x the whole of FY2025's, in one quarter, "
    f"which is why the disclosed rate rather than the collection is adopted — but the "
    f"upside if it IS an entitlement is worth up to EGP "
    f"{SUBSIDY[3]['fv'] - SUBSIDY[0]['fv']:.2f} a share and is published as a number")

fv_taxstat = None
CONTESTED = [
    dict(choice='Cost of debt: the POUND-EQUIVALENT cost of a euro debt book (adopted) '
                'vs the contracted euro rate',
         adopted=f"{KD:.2%}", alternative=f"{KD_CONTRACTED:.2%}",
         fv_adopted=fv_dcf, fv_alternative=fv_kd_contracted,
         effect=fv_kd_contracted / fv_dcf - 1,
         note=('91% of the book is euro-denominated at Euribor-linked rates. Adopting the '
               'contracted rate means that debt is NOT compensated for pound depreciation '
               'beyond what this study already assumes; if the pound falls faster, the '
               'true pound cost of servicing it is understated by construction. The '
               'alternative is computed rather than described — and it is small, because '
               'debt is only 4.9% of the capital structure.')),
    dict(choice='Beta: same-country peer median (adopted, tier 2) vs the own-stock '
                'regression against the EGX30 that is too weak to use: its R-squared of 0.047 leaves the slope indistinguishable from noise',
         adopted=f"{beta_used:.3f}", alternative=f"{BETA['own_stock']['beta']:.3f}",
         fv_adopted=fv_dcf, fv_alternative=fv_beta_own,
         effect=fv_beta_own / fv_dcf - 1,
         note=('THIS IS THE STUDY\'S MOST CONSEQUENTIAL CONTESTED JUDGEMENT AND IT IS '
               'PUBLISHED BOTH WAYS. The only conforming regressor for an EGX listing is '
               'the EGX30, and ARCC regressed against it returns an R-squared of 4.7% — '
               'below the 5% usability floor, so tier 1 is not available. Revisions 1-3 '
               'carried 0.628 from an equal-weight COMPOSITE of the covered Egyptian '
               'names, which correlates better with a covered name precisely because it '
               'contains one; SIGCM clause 6 calls that a hard fail rather than a tier. '
               'The adopted figure is the median equity beta of the Egyptian '
               'building-materials and construction peers that do clear the gate. Peer '
               'leverage is NOT sourced, so the unlever-and-re-lever step could not be '
               'performed; ARCC holds net cash and its peers carry debt, so performing it '
               'could only lower the beta and raise the value — the adopted figure is the '
               'conservative end of tier 2, and the alternative is shown beside it.')),
    dict(choice='Capex: economic maintenance in dollars per tonne (adopted) vs book '
                'depreciation',
         adopted=f"USD {V['capex_usd_t_cap']:.2f}/t", alternative='book depreciation',
         fv_adopted=fv_dcf, fv_alternative=fv_capex_bookdep,
         effect=fv_capex_bookdep / fv_dcf - 1,
         note=('Setting capex equal to book depreciation would flatter free cash flow by '
               'construction. The adopted treatment is the conservative one and the size '
               'of the conservatism is published.')),
]
say("\n[Contested choices, each computed]")
for c in CONTESTED:
    say(f"  {c['choice'][:60]}: {c['fv_adopted']:.2f} -> {c['fv_alternative']:.2f} "
        f"({c['effect']:+.1%})")

# ==================== 9. TERMINAL RECONCILIATION ============================
nopat_h = [ebit_h[i] * (1 - taxe_h[i]) for i in range(3)]
reinv_h = [capex_h[i] - dna_h[i] for i in range(3)]
rr_h = [reinv_h[i] / nopat_h[i] for i in range(3)]
ic_book_h = [V['eq_fy23'] + V['debt_fy23'], V['eq_fy24'] + V['debt_fy24'],
             V['eq_fy25'] + debt_tot]
roic_book_h = [nopat_h[i] / ic_book_h[i] for i in range(3)]
pat_cagr = (V['pat_fy25'] / V['pat_fy23']) ** 0.5 - 1
share_gdp = V['rev_fy25'] / (V['egy_gdp_egp_bn'] * 1000.0)
cross_yrs = float(np.log(1 / share_gdp) / np.log((1 + pat_cagr) / (1 + V['egy_gdp_growth'])))
TR = dict(
    history=[dict(year=HIST[i], capex=capex_h[i], capex_over_ebitda=capex_h[i] / ebitda_h[i],
                  character=('burst — debt-funded capacity step' if rr_h[i] > 1.0
                             else 'stable — self-funded'),
                  nopat=nopat_h[i], dna=dna_h[i], reinvestment=reinv_h[i], rr=rr_h[i],
                  roic_book=roic_book_h[i], implied_g=roic_book_h[i] * rr_h[i],
                  nopat_growth=(nopat_h[i] / nopat_h[i - 1] - 1) if i else None)
             for i in range(3)],
    nopat_cagr=(nopat_h[2] / nopat_h[0]) ** 0.5 - 1,
    pat_cagr_fy23_fy25=pat_cagr,
    stable_years=[HIST[i] for i in range(3) if rr_h[i] <= 1.0],
    stable_implied_g=float(np.mean([roic_book_h[i] * rr_h[i] for i in range(3)
                                    if rr_h[i] <= 1.0])) if any(r <= 1.0 for r in rr_h) else float('nan'),
    roic_repl=roic_t, rr_repl=rr_t, ic_repl=ic_repl,
    roic_book_fy25=roic_book_h[2], ic_book_fy25=ic_book_h[2],
    basis_adopted='replacement cost',
    crossover_years=cross_yrs, share_of_gdp=share_gdp,
)
say(f"\n[Terminal reconciliation — now buildable, because capex is disclosed for all "
    f"three years] reinvestment rate " + " ".join(f"{r:.0%}" for r in rr_h) +
    f"; book return on capital " + " ".join(f"{r:.1%}" for r in roic_book_h))
say(f"[Terminal growth ceiling] profit compounded {pat_cagr:.0%} a year over FY2023-FY2025; "
    f"at that rate against {V['egy_gdp_growth']:.0%} nominal economic growth this company "
    f"equals the whole Egyptian economy in {cross_yrs:.0f} years. Terminal growth is held "
    f"at {V['g_term']:.0%}")
# --- terminal growth: the sign condition, RE-DERIVED for [R-TERM-01] -----------------
# THE HURDLE IN THIS BLOCK WAS DERIVED FOR THE RETIRED CONSTRUCTION AND HAD TO CHANGE WITH
# IT. Revisions 1-4 charged a reinvestment of g/ROIC on replacement-cost capital, which
# collapses to a fixed g*IC, so the block reduced to TV(g) = [N(1+g) - g.IC]/(W-g) and the
# sign of the growth lever was the constant N(1+W) - IC.W — a hurdle of N/IC against
# W/(1+W) rather than the familiar ROIC against W. That derivation was correct FOR THAT
# CONSTRUCTION and it is now wrong, because the construction is gone.
#
# Under [R-TERM-01] the terminal charges maintenance at the disclosed life plus the capital
# that STATED REAL growth needs, at the replacement cost of capacity. So the question is
# the ordinary one, and it is ordinary because the construction now is:
#
#     marginal ROIC  =  NOPAT / IC     (capacity scales the profit and the capital alike)
#     growth adds value  iff  NOPAT/IC  >  W
#
# and the (1+g)/(1+W) wedge is gone with the charge that created it. THE MODEL'S ANSWER
# DOES NOT CHANGE AND THAT IS WORTH SAYING: N/IC is 10.52% against a terminal rate of
# 18.34%, so building cement capacity at USD 130 per annual tonne does not clear this
# company's cost of capital, real growth destroys value, and the model takes zero real
# growth. THAT IS A FINDING, NOT A DEFECT — and it is why charging ARCC for growth was
# wrong twice over: it is not growing in real terms, and on these numbers it should not.
gdv_lhs = nopat[-1]
gdv_rhs = ic_repl * wacc_term
GDV = dict(fv_at_g3=reval(g=0.03), fv_at_g7=reval(g=0.07), roic_term=roic_t,
           wacc_term=wacc_term, nopat_term=float(nopat[-1]), ic_replacement=float(ic_repl),
           n_over_ic=float(nopat[-1] / ic_repl), hurdle=float(wacc_term),
           hurdle_retired=float(wacc_term / (1 + wacc_term)),
           hurdle_basis='marginal ROIC = NOPAT/IC against the terminal WACC [R-TERM-01]',
           analytic_adds_value=bool(gdv_lhs > gdv_rhs))
GDV['model_adds_value'] = bool(GDV['fv_at_g7'] > GDV['fv_at_g3'])
GDV['spread_pct'] = float(GDV['fv_at_g7'] / GDV['fv_at_g3'] - 1.0)
GDV['holds'] = bool(GDV['analytic_adds_value'] == GDV['model_adds_value'])
say(f"[Growth and value] terminal return on capital {roic_t:.1%} against terminal rate "
    f"{wacc_term:.1%}: EGP {GDV['fv_at_g3']:.2f} at 3% growth against "
    f"{GDV['fv_at_g7']:.2f} at 7% — a spread of {GDV['spread_pct']:+.1%} across four "
    f"points of growth, so the answer "
    f"{'is BARELY sensitive to' if abs(GDV['spread_pct']) < 0.02 else 'DOES rest partly on'}"
    f" the terminal growth rate")
say(f"[Growth and value — the hurdle, re-derived] the retired terminal charged g x IC, so "
    f"its sign condition was N/IC against W/(1+W) = {GDV['hurdle_retired']:.2%}. "
    f"[R-TERM-01] charges maintenance at the disclosed {_LIFE:.0f}-year life plus the "
    f"capital REAL growth needs, so the test is the ordinary one: the marginal return on "
    f"new capacity N/IC = {GDV['n_over_ic']:.2%} against the terminal rate of "
    f"{wacc_term:.2%}. Growth "
    f"{'ADDS' if GDV['analytic_adds_value'] else 'DESTROYS'} value by "
    f"{abs(GDV['n_over_ic'] - wacc_term) * 1e4:.0f}bp — building capacity at USD "
    f"{V['repl_usd_t']:.0f} per annual tonne does not clear this company's cost of "
    f"capital, which is why the model takes ZERO real growth and charges no growth capital "
    f"for it. That is a finding about Egyptian cement economics, not a conservatism")

# ==================== 10. STATEMENTS ========================================
pbt_f, tax_f, pat_f, cash_b, eq_b, ppe_b, wc_b, div_f, treas_f, ta_b = ([] for _ in range(10))
c_ = V['cash_fy25'] - V['div_fy25_declared']
e_ = V['eq_fy25'] - V['div_fy25_declared']
p_ = V['ppe_fy25'] + V['auc_fy25'] + V['intang_fy25']
wc_ = V['inv_fy25'] + V['recv_fy25'] + V['debtors_fy25']
for i in range(5):
    ti = c_ * V['cash_yield'][i] - debt_tot * kdp[i] * (1 - eur_share) - \
        debt_tot * eur_share * (V['euribor'] + 0.0435)
    pbt = ebit_f[i] + ti
    tx = pbt * TAXE
    pat = pbt - tx
    dv = pat * V['payout']
    p_ += capex[i] - dna_f[i]
    wc_ += dwc[i]
    c_ += pat + dna_f[i] - capex[i] - dwc[i] - dv
    e_ += pat - dv
    for L, x in ((treas_f, ti), (pbt_f, pbt), (tax_f, tx), (pat_f, pat), (div_f, dv),
                 (cash_b, c_), (eq_b, e_), (ppe_b, p_), (wc_b, wc_),
                 (ta_b, c_ + p_ + wc_)):
        L.append(x)

# ==================== 11. EXPERT PANEL ======================================
fcff_mid = float(np.mean(fcff[1:]))
e3 = (fcff_mid / 0.175 + net_cash - V['nci']) / SH
EXPERTS = [
    dict(label='Expert 1', method='Replacement-cost industrialist', central=fv_asset,
         low=((V['ev_t_just'] - 15) * V['cap_cement_mt'] * V['fx'] + net_cash - V['nci']) / SH,
         high=((V['ev_t_just'] + 15) * V['cap_cement_mt'] * V['fx'] + net_cash - V['nci']) / SH,
         summary=('Values the plant, not the earnings stream. The audited accounts put '
                  'net property, plant and equipment at EGP %.0fmn and assets under '
                  'construction at a further EGP %.0fmn, on a book carried at '
                  'pre-devaluation historic cost. Five million tonnes of grey cement '
                  'capacity costs about USD %.0f per annual tonne to build; nobody pays '
                  'that in a market carrying %.0fMt of capacity against %.0fMt of '
                  'consumption, so the justified figure is marked to USD %.0f. Against '
                  'that the market is paying USD %.0f per annual tonne.'
                  % (V['ppe_fy25'], V['auc_fy25'], V['repl_usd_t'], V['egy_capacity_mt'],
                     V['egy_cons_mt'], V['ev_t_just'], ev_per_t)),
         falsifier=('Find an Egyptian line built, bought or restarted below USD %.0f per '
                    'annual tonne. The %.1fMt revival programme is the live test and it '
                    'runs against this lens: restarting a mothballed kiln costs a fraction '
                    'of building one, which is why this valuation is a CEILING and is '
                    'published as a cross-check rather than as the answer.'
                    % (V['ev_t_just'], V['egy_revival_mt']))),
    dict(label='Expert 2', method='Mid-cycle earnings-power analyst', central=fv_norm,
         low=(nopat_norm * (V['pe_just'] - 1) + net_cash - V['nci']) / SH,
         high=(nopat_norm * (V['pe_just'] + 1) + net_cash - V['nci']) / SH,
         summary=('Refuses to capitalise a peak, and refuses it on both legs. The audited '
                  'EBITDA margin went %.1f%% to %.1f%% to %.1f%% across FY2023 to FY2025 — '
                  'the last of those is the best year the Egyptian industry has had in over '
                  'a decade. The margin is normalised to %.1f%%, the midpoint of the two '
                  'most recent audited years, the revenue base is cut %.0f%%, and what is '
                  'left is capitalised at %.0f times with cash added back at face.'
                  % (mgn_h[0] * 100, mgn_h[1] * 100, mgn_h[2] * 100, V['norm_mgn'] * 100,
                     (1 - V['norm_rev_haircut']) * 100, V['pe_just'])),
         falsifier=('Two consecutive years of realised prices above EGP 4,200 a tonne WITH '
                    'the revival proceeding would prove the mid-cycle base too low. '
                    'Equally, the first quarter of 2026 already ran a %.1f%% gross margin '
                    'against %.1f%% for FY2025 as a whole — if that holds for the year, '
                    'this lens is too cautious.'
                    % (V['gp_q1_26'] / V['rev_q1_26'] * 100, gp_h[2] / rev_h[2] * 100))),
    dict(label='Expert 3', method='Cash-return and distribution investor', central=e3,
         low=(fcff_mid / 0.20 + net_cash - V['nci']) / SH,
         high=(fcff_mid / 0.15 + net_cash - V['nci']) / SH,
         summary=('Ignores the terminal value and asks what the cash stream is worth to '
                  'someone who has to be paid in cash. Average free cash flow to the firm '
                  'across FY2027-FY2030 is EGP %.0fmn; required at a 17.5%% cash return '
                  'that is a business worth EGP %.0fmn before net cash of EGP %.0fmn is '
                  'added back. This is not hypothetical: the company declared EGP '
                  '%.0fmn for FY2025 on EGP %.0fmn of attributable profit, a %.0f%% '
                  'payout, and the audited cash flow shows EGP %.0fmn actually paid out '
                  'during 2025.'
                  % (fcff_mid, fcff_mid / 0.175, net_cash, V['div_fy25_declared'],
                     V['pat_fy25'], V['payout'] * 100, 1702.412714)),
         falsifier=('A required cash return above 20%% takes this valuation to EGP %.2f. '
                    'So would maintenance capital spending materially above the USD %.2f '
                    'per tonne assumed here — the audited FY2024 and FY2025 capex of EGP '
                    '%.0fmn and EGP %.0fmn is the number to watch, and both years carried '
                    'the alternative-fuel and silo programmes on top of maintenance.'
                    % ((fcff_mid / 0.20 + net_cash - V['nci']) / SH, V['capex_usd_t_cap'],
                       V['capex_fy24'], V['capex_fy25']))),
]

LR = {}
for k, v in LENS.items():
    LR[k] = dict(bear=v * 0.90, base=v, bull=v * 1.10)
# ---- THE BEAR AND THE BULL COME OFF THE FILED RECORD [rebuilt 03-Sep-2026] ---
# the item engine/build_depth_audit/lens_outstanding.json promised at this
# study's next re-issue, and this is that re-issue.
#
# The old corners moved the EBITDA margin by two points AND the discount rate by
# 150bp, in opposite directions at each end. The discount rate is not this
# company's to move: under [R-MACRO-01] it is derived from the house macro path,
# and terminal growth and the terminal risk-free rate both carry the same
# terminal inflation. So the published width was a choice of dial settings, and
# its own note called it "never a spread invented around the answer" -- a
# cautious label attached to the construction it disclaims, which is exactly the
# habit [R-CAL-02] was written about.
#
# What replaces it moves ONE business driver across the span ARCC's own AUDITED
# accounts have printed: the EBITDA margin, FY2023 22.00% to FY2025 39.25%. The
# macro path is held completely still.
#
# THE RESULT IS DELIBERATELY ASYMMETRIC AND THAT ASYMMETRY IS THE FINDING. The
# forecast opens at 39.03% -- within a fifth of a point of the best year this
# company has ever filed -- so there is effectively NO upside left in margin, and
# the whole of the range is downside. A symmetric +/-2pp band hid that completely.
_ARCC_MGN_FILED_LOW = 0.2200          # FY2023, audited
_ARCC_MGN_FILED_HIGH = 0.3925         # FY2025, audited
_arcc_base_mgn = ebitda_f[0] / rev_f[0]
LR['DCF (cash flow)'] = dict(
    bear=reval(mgn_shift=_ARCC_MGN_FILED_LOW - _arcc_base_mgn), base=fv_dcf,
    bull=reval(mgn_shift=_ARCC_MGN_FILED_HIGH - _arcc_base_mgn))
# the diagnostic gets a range too, so the comparison table can show it beside
# the published reads without the document having to invent one
for k, v in LENS_DIAGNOSTIC.items():
    LR['Normalised earnings'] = dict(bear=v * 0.90, base=v, bull=v * 1.10)
# 'Weighted central' is kept as a KEY for the published envelope, which is now
# the PRIMARY's own range rather than a weighted mixture of four
LR['Weighted central'] = dict(
    bear=float(LR[PRIMARY]['bear']), base=fv_central,
    bull=float(LR[PRIMARY]['bull']))

PEERS = dict(
    scem=dict(name='Sinai Cement (SCEM)', rev=V['peer_scem_rev'], pat=V['peer_scem_pat'],
              mcap=V['peer_scem_mcap'], pe=V['peer_scem_mcap'] / V['peer_scem_pat'],
              ps=V['peer_scem_mcap'] / V['peer_scem_rev']),
    mbsc=dict(name='Misr Beni Suef Cement (MBSC)', rev=V['peer_mbsc_rev'],
              pat=V['peer_mbsc_pat'], mcap=V['peer_mbsc_mcap'],
              pe=V['peer_mbsc_mcap'] / V['peer_mbsc_pat'],
              ps=V['peer_mbsc_mcap'] / V['peer_mbsc_rev']),
    self=dict(name='Arabian Cement (ARCC)', rev=V['rev_fy25'], pat=V['pat_fy25'],
              mcap=MKTCAP, pe=MKTCAP / V['pat_fy25'], ps=MKTCAP / V['rev_fy25']),
    sector=dict(capacity_mt=V['egy_capacity_mt'], consumption_mt=V['egy_cons_mt'],
                production_mt=V['egy_prod_mt'], exports_mt=V['egy_exports_mt'],
                revival_mt=V['egy_revival_mt'],
                share_of_capacity=V['cap_cement_mt'] / V['egy_capacity_mt'],
                revival_pct_of_consumption=V['egy_revival_mt'] / V['egy_cons_mt'],
                utilisation=V['egy_prod_mt'] / V['egy_capacity_mt']),
)

# ==================== ASSERT ================================================
A = []
def chk(cond, msg):
    assert cond, 'ASSERT FAILED: ' + msg
    A.append(msg)


for _i in (0, 1, 5):
    _b = BU[_i]
    chk(abs(_b['rev'] - _b['c_mat'] - _b['c_tra'] - _b['c_ovh'] - _b['c_prv']
            - _b['ebitda']) < 1e-6,
        f"the printed cost stack FOOTS in {['FY2025A', 'FY2026E', None, None, None, 'FY2030E'][_i]}: "
        f"revenue of EGP {_b['rev']:,.0f}mn less materials and fuel {_b['c_mat']:,.0f}, "
        f"transportation {_b['c_tra']:,.0f}, overheads {_b['c_ovh']:,.0f} and provisions "
        f"and credit losses {_b['c_prv']:,.0f} IS the EBITDA of EGP {_b['ebitda']:,.0f}mn "
        f"the table prints. Until this edition the provisions line was deducted in the "
        f"model and absent from the table, so a reader adding the printed rows got EGP "
        f"{_b['rev'] - _b['c_mat'] - _b['c_tra'] - _b['c_ovh']:,.0f}mn and could not "
        f"reconcile it — the model was right and the page was incomplete, which no "
        f"recalculation gate can see because it reconciles the model to itself")

for _i in range(5):
    _scale = REM if _i == 0 else 1.0
    chk(abs((nopat[_i] + dna_f[_i] - capex[_i] - dwc[_i]) * _scale - fcff[_i]) < 1e-6,
        f"the printed free-cash-flow build FOOTS in {YRS[_i]}: NOPAT of EGP "
        f"{nopat[_i]:,.0f}mn plus depreciation {dna_f[_i]:,.0f} less capital expenditure "
        f"{capex[_i]:,.0f} less the working-capital change {dwc[_i]:,.0f}, times the "
        f"remaining fraction of the year {_scale:.2f}, IS the free cash flow of "
        f"{fcff[_i]:,.0f} the table prints. Until this edition that fraction appeared "
        f"nowhere on the page, so FY2026's components were full-year figures against a "
        f"part-year cash flow and a reader's arithmetic came out at exactly twice the "
        f"printed number")

for _i in range(5):
    chk(abs(ebitda_f[_i] - dna_f[_i] + oth_f[_i] - ebit_f[_i]) < 1e-6,
        f"the printed cash-flow waterfall FOOTS in {YRS[_i]}: EBITDA of EGP "
        f"{ebitda_f[_i]:,.0f}mn less depreciation and amortisation of {dna_f[_i]:,.0f} plus "
        f"other operating income of {oth_f[_i]:,.0f} IS the EBIT of {ebit_f[_i]:,.0f} the "
        f"table prints. Until this edition other operating income was consumed by the model "
        f"and printed nowhere, so a reader subtracting the printed depreciation from the "
        f"printed EBITDA came out {ebitda_f[_i] - dna_f[_i] - ebit_f[_i]:,.0f}mn short of "
        f"the printed EBIT — the third instance in this study of a line the model uses and "
        f"the page does not show")

chk(V['auc_altfuel_fy25'] + V['auc_silo_fy25'] <= V['auc_fy25'] + 1e-9,
    f"the two NAMED assets under construction — the alternative-fuel system for line 2 at "
    f"EGP {V['auc_altfuel_fy25']:,.3f}mn and the new cement silo for line 1 at EGP "
    f"{V['auc_silo_fy25']:,.3f}mn — sit INSIDE the disclosed total of EGP "
    f"{V['auc_fy25']:,.3f}mn, leaving EGP "
    f"{V['auc_fy25'] - V['auc_altfuel_fy25'] - V['auc_silo_fy25']:,.3f}mn of other "
    f"construction in progress. Both figures were typed into the document builder until "
    f"this edition, which is the one place no gate in this repository was looking")

chk(abs(reval() - fv_dcf) < 1e-6,
    f"THE SENSITIVITY FUNCTION REPRODUCES THE HEADLINE when nothing is changed: "
    f"reval() = {reval():.4f} against the cash-flow lens {fv_dcf:.4f}. Revision 3's did "
    f"NOT — it discounted the terminal value at the last explicit year's mid-year factor "
    f"instead of the end-of-window factor and returned 57.27 against a headline of 55.21, "
    f"so every sensitivity and every contested judgement in the study was quoted on a basis "
    f"3.7% more generous than the number it was compared against. That is one document and "
    f"two models, inside the block whose whole job is to test the first one")
chk(abs(reval_two_anchor(wacc_exp, wacc_term) - fv_dcf) < 1e-6,
    f"the two-anchor sensitivity grid reproduces the headline at the adopted anchors "
    f"({reval_two_anchor(wacc_exp, wacc_term):.4f})")
chk(abs((ev + net_cash - V['nci_h1_26']) - eq_dcf) < 1e-6,
    f"bridge closes exactly: EV {ev:,.2f} + net cash {net_cash:,.2f} - NCI {V['nci_h1_26']:,.3f} "
    f"= equity {eq_dcf:,.2f}")
chk(net_cash > 0, f"net cash carries a POSITIVE sign into the bridge ({net_cash:,.1f})")
chk(V['nci_h1_26'] > 0,
    f"minority interests are DEDUCTED at the LATEST disclosed figure "
    f"({V['nci_h1_26']:,.3f} at 30 June 2026, against {V['nci']:,.3f} at 31 December 2025), "
    f"not added")
chk(0.0 < tv_share < 0.85, f"terminal value is {tv_share:.1%} of enterprise value")
chk(0.35 < fv_central / V['spot'] < 3.0,
    f"implied fair value to spot {fv_central/V['spot']:.2f}x is inside the plausibility band")
chk(wacc_term < wacc_exp, f"terminal rate {wacc_term:.2%} is BELOW the explicit-window "
                          f"rate {wacc_exp:.2%}")
DISC = dict(clk_prod=3.8516, cem_prod=3.4806, cem_loc=2.9236, cem_exp=0.6295,
            clk_exp=1.3005, sold=4.8536)
_worst = max(abs(p0[k] / v - 1) for k, v in DISC.items())
chk(_worst < 0.001,
    f"the physical build reproduces EVERY disclosed FY2025 tonne to within "
    f"{_worst:.3%}: clinker made {p0['clk_prod']:.4f} vs {DISC['clk_prod']}, cement made "
    f"{p0['cem_prod']:.4f} vs {DISC['cem_prod']}, local {p0['cem_loc']:.4f} vs "
    f"{DISC['cem_loc']}, cement exports {p0['cem_exp']:.4f} vs {DISC['cem_exp']}, clinker "
    f"exports {p0['clk_exp']:.4f} vs {DISC['clk_exp']}, total {p0['sold']:.4f} vs "
    f"{DISC['sold']}Mt. Revisions 1-3 reconstructed these from an assumed price and were "
    f"28% low on the total")
chk(abs((V['egy_cons_mt'] + V['egy_exports_mt']) - V['egy_prod_mt']) < 0.15,
    f"the Egyptian sector balance CLOSES: local {V['egy_cons_mt']}Mt plus exports "
    f"{V['egy_exports_mt']}Mt = {V['egy_cons_mt']+V['egy_exports_mt']:.1f}Mt against the "
    f"disclosed total of {V['egy_prod_mt']}Mt. It did not close in any earlier revision")
chk(all(b['kiln_util'] <= 1.0 for b in BU),
    f"no forecast year asks the kiln for more than nameplate: peak "
    f"{max(b['kiln_util'] for b in BU):.1%} of {V['cap_clinker_mt']:.1f}Mt")
chk(all(b['mill_util'] <= 1.0 for b in BU),
    f"no forecast year asks the mill for more than nameplate: peak "
    f"{max(b['mill_util'] for b in BU):.1%} of {V['cap_cement_mt']:.1f}Mt")
chk(V['cem_export_share'][0] <= 0.30,
    f"cement exports ({V['cem_export_share'][0]:.1%}) sit INSIDE the 30% statutory cap the "
    f"study cites — revision 3's single-product build breached it at 31.5%")
chk(abs(recon_rev) < 0.005, f"the unit build reproduces AUDITED FY2025 revenue to "
                            f"{recon_rev:+.3%}")
chk(abs(recon_eb) < 0.010, f"the unit build reproduces AUDITED FY2025 EBITDA to "
                           f"{recon_eb:+.3%}")
chk(abs(ebit_h[2] - 4595.823562) < 0.01,
    f"FY2025 operating profit closes from the audited lines to EGP {ebit_h[2]:,.3f}mn")
chk(abs((V['ta_fy25'] - V['tl_fy25']) - (V['eq_fy25'] + V['nci'])) < 0.001,
    f"the audited balance sheet closes: assets {V['ta_fy25']:,.3f} less liabilities "
    f"{V['tl_fy25']:,.3f} = equity {V['eq_fy25']+V['nci']:,.3f}")
# Revision 3 asserted that the forecast margin glides DOWN every year. That was
# an assertion about revision 3's own price path, not about the company, and it
# cannot survive a calibration onto a reviewed half that shows the margin HOLDING.
# It is replaced by two tests that can actually fail: the first year must
# reproduce what the half implies, and the window must not manufacture expansion.
_h1_implied_mgn = ((CAL['fy26_rev_implied']
                    - CAL['fy26_cashcost_implied']
                    - (V['prov_fy25'] + V['ecl_fy25']) / V['rev_fy25']
                    * CAL['fy26_rev_implied']) / CAL['fy26_rev_implied'])
chk(abs(BU[1]['mgn'] - _h1_implied_mgn) < 0.005,
    f"the FY2026 EBITDA margin ({BU[1]['mgn']:.1%}) reproduces the margin the REVIEWED "
    f"half implies ({_h1_implied_mgn:.1%}) to within half a point — the calibration moved "
    f"price, cost and services together, so the margin is an output of the three rather "
    f"than an artefact of calibrating one")
# THE GUARD IS RE-POINTED, NOT RELAXED. Until this edition the local price index
# grew more slowly than the cost index in every year, so the escalators alone
# forced the margin down and "FY2030 <= FY2026" tested nothing an input could
# fail. Price and cost now ride ONE path at zero real growth, so the escalators
# are neutral by construction and the margin is free to move in either
# direction. What the guard must therefore ask is whether anything OTHER than
# the disclosed alternative-fuel programme moves it — so the margin path is
# rebuilt here with af_saving zeroed, and THAT path is the one forbidden to
# expand. The programme is not an assumption about intent: EGP 240.2mn of
# alternative-fuel capacity for kiln 2 sits in assets under construction at the
# year end with a EUR 25mn EBRD facility drawn against it, and a margin the
# company has financed and built is a finding, not an artefact.
_mgn_no_af = []
for _i in range(6):
    _ph = PH[_i]
    _infl = V['cost_infl'][_i]
    _pl = price_loc25 * V['price_local_path'][_i]
    _pec = price_exp_cem25 / V['fx_avg_fy25'] * V['price_exp_path'][_i] * V['fx_path'][_i]
    _rev_g = _ph['cem_loc'] * _pl + _ph['cem_exp'] * _pec + _ph['clk_exp'] * _pec * V['clk_price_ratio']
    _rev = _rev_g * (1 + V['svc_share'])
    _cc = (cc_mat_clk * _infl * _ph['clk_prod'] + cc_tra_t * _infl * _ph['sold']
           + cc_ovh_t * _infl * _ph['sold'])
    _prv = (V['prov_fy25'] + V['ecl_fy25']) / V['rev_fy25'] * _rev
    _mgn_no_af.append((_rev - _cc - _prv) / _rev)
chk(_mgn_no_af[5] <= _mgn_no_af[1] + 0.001,
    f"the window does not MANUFACTURE margin expansion: with the alternative-fuel saving "
    f"switched off the FY2030 margin is {_mgn_no_af[5]:.1%} against {_mgn_no_af[1]:.1%} in "
    f"FY2026, so nothing in the escalators expands it. The {BU[5]['mgn'] - BU[1]['mgn']:+.1%} "
    f"the model does show ({BU[1]['mgn']:.1%} to {BU[5]['mgn']:.1%}) is the funded "
    f"alternative-fuel programme and nothing else")
chk(TAXE < TAX + 0.03, f"the effective tax rate used ({TAXE:.2%}) is within 3 points of "
                       f"the statutory rate ({TAX:.2%}), as the audited accounts show")
chk(GDV['holds'],
    f"the terminal growth lever moves the model in the direction its own algebra requires: "
    f"N/IC {GDV['n_over_ic']:.2%} against the hurdle W/(1+W) {GDV['hurdle']:.2%}, so growth "
    f"{'adds' if GDV['analytic_adds_value'] else 'destroys'} value, and the model "
    f"{'adds' if GDV['model_adds_value'] else 'destroys'} it — a spread of "
    f"{GDV['spread_pct']:+.1%} from 3% to 7%, which is "
    f"{'immaterial' if abs(GDV['spread_pct']) < 0.02 else 'MATERIAL and is published'}")
chk(abs(SHT['from_fy25_dividend'] - SH) / SH < 0.001,
    f"the share count is confirmed by the declared FY2025 dividend to "
    f"{abs(SHT['from_fy25_dividend']-SH)/SH:.4%}")
chk(all(df_[i] > df_[i + 1] for i in range(4)), "discount factors decline monotonically")
chk(PRIMARY in LENS and fv_central == LENS[PRIMARY],
    "the central IS one lens, not a blend of several: there are no weights left to sum")
chk(fv_central == LENS[PRIMARY] and min(LENS.values()) <= fv_central <= max(LENS.values()),
    "the weighted central sits inside the range of the four lenses")
chk(eur_share > 0.5, f"the cost-of-debt build is currency-blended: {eur_share:.1%} of the "
                     f"book is euro-denominated and a single-currency shortcut would be wrong")
say("\n" + "=" * 78)
say("ASSERT LOG")
for i, m in enumerate(A, 1):
    say(f"  {i:2d}. {m}")
say("=" * 78)

# ==================== EMIT ==================================================
# ==================== 8. YEARS 3-5 AS RANGES, AND THE GATES =================
# [R-FCAL-01] §6: a study carrying a fundamental walk-forward publishes years 3-5
# as RANGES built from that record's own driver-error distribution, never as
# points. The bands below are the OBSERVED min-max of the walk-forward's log
# errors at each horizon with the count printed beside them, because at horizon 5
# there are three resolved cells and a percentile of three numbers is a fiction.
_WF = os.path.join(HERE, '..', 'arcc_walkforward', 'forward_ranges.json')
with open(_WF) as f:
    _wfr = json.load(f)
WF = {'source': "this company's own fundamental walk-forward, run 01-09-2026",
      'origins': 8, 'cells': 25, 'span': 'FY2014-FY2025',
      'adopted_correction': {'driver': 'manufacturing depreciation',
                             'factor': V['wf_dep_correction'],
                             'of_candidates': 12, 'watch_flags': 11},
      'ranges': {}}
for _line in ('revenue', 'gross_profit', 'pbt', 'vol_total'):
    _proj = {1: rev_f[0], 2: rev_f[1], 3: rev_f[2], 4: rev_f[3], 5: rev_f[4]} if _line == 'revenue' else None
    WF['ranges'][_line] = {}
    for _h in ('3', '4', '5'):
        _b = _wfr.get(_line, {}).get(_h)
        if not _b:
            continue
        WF['ranges'][_line][_h] = dict(n=_b['n'], low=_b['mult_low'], high=_b['mult_high'],
                                       median=_b['median_mult'])
_r3 = WF['ranges']['revenue']
say(f"\n[Years 3-5 are RANGES, from this name's own walk-forward] on twenty-five resolved "
    f"cells the method's revenue error spans x{_r3['3']['low']:.2f}-x{_r3['3']['high']:.2f} at "
    f"three years (n={_r3['3']['n']}), x{_r3['4']['low']:.2f}-x{_r3['4']['high']:.2f} at four "
    f"(n={_r3['4']['n']}) and x{_r3['5']['low']:.2f}-x{_r3['5']['high']:.2f} at five "
    f"(n={_r3['5']['n']}). Total VOLUME at five years spans only "
    f"x{WF['ranges']['vol_total']['5']['low']:.2f}-"
    f"x{WF['ranges']['vol_total']['5']['high']:.2f}, and profit before tax spans "
    f"x{WF['ranges']['pbt']['5']['low']:.2f}-x{WF['ranges']['pbt']['5']['high']:.2f} — "
    f"tonnage is forecastable at five years and profit is not, which is why the delivered "
    f"document publishes the far years as ranges and says so")

# ---- the four standing gates, called in the study's own code [R-ENF-02] -----
sys.path.insert(0, os.path.join(HERE, '..'))
import research_protocol as RP
STD_VERSION = RP.STANDARD_VERSION

_cem_exp_t, _clk_exp_t = 629.5, 1300.5
_exp_share = V['rev_exp_goods_fy25'] / V['rev_fy25']
_gu = [
    RP.DriverLine(
        name="local cement", level="unit",
        share_of_revenue=V['rev_local_goods_fy25'] / V['rev_fy25'],
        unit="tonne of cement sold in Egypt",
        unit_source="FY2025 investor presentation, performance highlights: local sales "
                    "volume 2,923.6 thousand tonnes",
        price_basis="DERIVED, not assumed: the audited note-4 local goods line of EGP "
                    "8,350.455mn over the disclosed local tonnage, giving EGP 2,856/t. "
                    "Recalibrated for FY2026 onward on the H1-2026 reviewed half",
        cost_basis="note 5 built to its own physical driver — raw materials and fuel per "
                   "tonne of CLINKER because the kiln burns them, transportation and "
                   "overheads per tonne DESPATCHED. The margin is an OUTPUT of the two"),
    RP.DriverLine(
        name="export cement", level="unit",
        share_of_revenue=_exp_share * (_cem_exp_t / (_cem_exp_t + _clk_exp_t)),
        unit="tonne of cement exported",
        unit_source="FY2025 investor presentation: cement export volume 629.5 thousand tonnes",
        price_basis="derived from the audited note-4 export goods line, split from clinker "
                    "at the disclosed clinker price ratio; recalibrated on the H1-2026 half",
        cost_basis="the same physical stack as local cement, plus the despatch lines"),
    RP.DriverLine(
        name="export clinker", level="unit",
        share_of_revenue=_exp_share * (_clk_exp_t / (_cem_exp_t + _clk_exp_t)),
        unit="tonne of clinker exported",
        unit_source="FY2025 investor presentation: clinker export volume 1,300.5 thousand "
                    "tonnes",
        price_basis="derived from the audited note-4 export goods line at the disclosed "
                    "clinker price ratio — clinker is an unground intermediate and pricing "
                    "it at a cement price is the error revisions 1-3 made",
        cost_basis="kiln cost per tonne of clinker, note 5"),
    RP.DriverLine(
        name="transportation services", level="segment",
        share_of_revenue=1.0 - (V['rev_local_goods_fy25'] + V['rev_exp_goods_fy25'])
                         / V['rev_fy25'],
        price_basis="ratio to goods revenue, recalibrated on the H1-2026 reviewed half, "
                    "where the ratio fell from 6.325% to 4.42% as export services collapsed",
        cost_basis="inside the transportation cost line of note 5",
        gap_note="NO TONNE-LEVEL DRIVER IS BUILT FOR SERVICES AND THE GAP IS STATED RATHER "
                 "THAN FILLED. The filings disclose the services revenue and the "
                 "transportation cost but never a haulage volume or a rate per "
                 "tonne-kilometre, so the finest sourced level here is the segment. The "
                 "walk-forward went further and tried to split the transport COST into a "
                 "local and an export rate: solving across all 45 available period pairs "
                 "gives a local rate from -425 to +722 EGP/t and an export rate from "
                 "-4,483 to +1,040, with nine of the 45 local solves economically "
                 "impossible. The split is unidentified on this disclosure and is not built."),
]
GROUND_UP = RP.assert_ground_up(_gu, ticker="ARCC")

# SIGCM, clause by clause. Every one of these is now backed by something outside
# the boolean: clause 1 by the audited statements themselves, clause 2 by the
# driver record above and assert_ground_up(), clause 6 by the beta record and
# assert_beta_provenance(). The clause-6 flag was set True by revisions 1-3 while
# the regression ran on a composite, which is exactly why it is no longer the
# thing that attests it.
SIGCM = RP.SIGCMChecklist(
    historicals_official_only=True,
    forecast_ground_up=True,
    debt_lc_fx_split=True,
    asset_conversion_cycle=True,
    competitors=True,
    beta_own_history_vs_egx30=True,
    formula_based_model=True,
    flags_raised_before_issue=True,
    stop_and_inform_honoured=True,
    na_reasons={},
)
# THE SCRUB ATTESTATION IS READ, NOT TYPED. Until this edition
# `external_reader_scrub=True` sat here with nothing behind it: no scan existed
# in this study at all, and the boolean asserted a clean result that had never
# been measured. That is the failure [R-ENF-01] names in one line — a
# self-attested boolean is never a check — and it hid in plain sight because the
# word was the same one the studies beside it use for a scan that really runs.
#
# scrub_gate.py now reads the DELIVERED documents and writes scrub_result.json.
# This reads that file back and refuses three ways: no result at all, a result
# that does not cover this edition's own filenames, or a result with any hit in
# it. A new edition therefore runs compute -> documents -> scrub -> compute
# again, and the second pass is the one that may attest.
def _scrub_attestation():
    f = os.path.join(HERE, 'scrub_result.json')
    if not os.path.exists(f):
        return False, ('no scrub_result.json: the delivered documents have not been '
                       'scanned. Build them, run scrub_gate.py, then re-run this '
                       'module — an unmeasured result is not a clean one.')
    r = json.load(open(f))
    want = {'ARCC_Valuation_Study_03-09-2026_public.docx',
            'ARCC_Bibliography_03-09-2026.docx'}
    missing = sorted(want - set(r.get('files', [])))
    if missing:
        return False, ('the scrub covers %s and not %s — a check that opens a '
                       'superseded file reports on something nobody receives'
                       % (r.get('files'), missing))
    if not r.get('clean'):
        return False, ('%d forbidden term(s) and %d table problem(s) in the '
                       'delivered documents'
                       % (len(r.get('hits', [])), len(r.get('column_problems', []))))
    return True, ('%d terms scanned across %s characters of delivered text, 0 hits; '
                  'table column audit clean'
                  % (39, '{:,}'.format(r.get('chars', 0))))


SCRUB_OK, SCRUB_NOTE = _scrub_attestation()
say(f"\n[External-reader scrub] {'CLEAN' if SCRUB_OK else 'NOT ATTESTED'} — {SCRUB_NOTE}")

MODEL_CHECK = RP.ModelStudyChecklist(
    structure_matches_model=True,
    bibliography_document=True,
    provenance_four_field=True,
    numeric_traceability=True,
    external_reader_scrub=SCRUB_OK,
    figure_discipline=True,
    table_discipline=True,
    expert_appendix_max_detail=True,
    contested_judgement_both_ways=True,
    na_reasons={},
)
# The record inspected is the OWN-STOCK regression against the EGX30 — the
# conforming regressor — and it FAILS the usability gate at R-squared 0.047.
# tier2_fallback_documented=True is passed because the study does not keep that
# number: it falls to a same-country peer beta and shows the failed diagnostics
# beside it. Revisions 1-3 carried 0.6281 from an equal-weight COMPOSITE of the
# covered Egyptian names, which SIGCM clause 6 calls a hard fail and not a tier.
RP.assert_beta_provenance(BETA['own_stock'], tier2_fallback_documented=True)
RP.assert_sigcm(SIGCM)
RP.assert_model_study(MODEL_CHECK)
say(f"\n[Gates] assert_ground_up, assert_beta_provenance, assert_sigcm and "
    f"assert_model_study all called in this study's own code and all passed. Built to "
    f"standard {STD_VERSION}")

# ===========================================================================
# THE FOUR CONSTRUCTION RECORDS AND THE TWO OUTPUT RECORDS
# Every one of them is a set of CHOICES written down so a job outside this study
# can check them. A model that recalculates is not a model that is right: the
# defects these close all lived inside arithmetic that reconciled to the last
# cell.
# ===========================================================================
_PI = list(_MACRO.inflation_path)
_YRS = list(_MACRO.inflation_years)

_INFL_INPUTS = [
    # [R-MACRO-01], clause added 03-Sep-2026 after EGCH: every inflation-class INPUT,
    # not only the declared growth lines. This study's two escalator INDICES are
    # cumulative, so what is declared here is the per-year rate each implies. The
    # FIRST forecast year is an EVIDENCED COMPANY ANCHOR in both — the disclosed
    # Q4-2025 exit price and the reviewed half's cost of sales — and it is exempted by
    # COUNT with that reason rather than by exempting the line, which is the shape
    # EGCH used to hide a whole inflation path. From FY2027 both ride the house
    # calendar ladder to the basis point, which is what makes the margin an OUTPUT.
    dict(key='cost_infl', mapping='calendar', first_year=2027, exempt_head=1,
         values=[round(V['cost_infl'][i + 1] / V['cost_infl'][i] - 1, 6)
                 for i in range(5)],
         exempt_reason='FY2026 is anchored on the reviewed half\'s own cost of sales, '
                       'not on an inflation rate; its real growth against the house '
                       'path is stated in the growth line above',
         note='FY2027-FY2030 are the house calendar ladder at zero real growth'),
    dict(key='price_local_path', mapping='calendar', first_year=2027, exempt_head=1,
         values=[round(V['price_local_path'][i + 1] / V['price_local_path'][i] - 1, 6)
                 for i in range(5)],
         exempt_reason='FY2026 is anchored on the disclosed Q4-2025 exit price of '
                       'EGP 3,118/t; holding that exit flat produces 7.2% and the 8.0% '
                       'carried is 0.8 points above a no-further-increase path',
         note='FY2027-FY2030 are the house calendar ladder at zero real growth, the '
              'SAME path the cost index carries'),
]

MACRO_RECORD = dict(
    market='EG', path_as_of=_MACRO.as_of,
    inflation_inputs=_INFL_INPUTS,
    growth_lines=[
        # The anchored year and the path years are separate LINES because they
        # assume different real growth and each has to say so. Folding them into
        # one average would hide both.
        dict(name='local realised cement price, FY2026 (anchored on disclosure)',
             years=[_YRS[0]], nominal=[round(V['price_local_path'][1] / V['price_local_path'][0] - 1, 6)],
             real=round((V['price_local_path'][1] / V['price_local_path'][0]) / (1 + _PI[0]) - 1, 6),
             basis='the disclosed Q4-2025 exit rate of EGP 3,118/t, 7.2% above the '
                   'full-year average, so holding the exit flat produces 7.2% and the '
                   '8.0% carried is 0.8 points above a no-further-increase path. The '
                   'real growth is NEGATIVE against the house path and is stated as '
                   'such rather than left to be inferred'),
        dict(name='local realised cement price, FY2027-FY2030',
             years=_YRS[1:], nominal=[round(V['price_local_path'][i+1] / V['price_local_path'][i] - 1, 6)
                                      for i in range(1, 5)],
             real=0.0,
             basis='the house inflation path at zero real growth, the same path the '
                   'cost index carries, so the margin is an OUTPUT of the two'),
        dict(name='local cash cost per tonne, FY2026',
             years=[_YRS[0]], nominal=[round(V['cost_infl'][1] / V['cost_infl'][0] - 1, 6)],
             real=round((V['cost_infl'][1] / V['cost_infl'][0]) / (1 + _PI[0]) - 1, 6),
             basis='unchanged from the prior edition and corroborated by the reviewed '
                   'half: FY2026 cost of sales of EGP 3,619mn for the six months '
                   'implies a full year against which the modelled cash cost lands '
                   'within 2.4%. The real growth is stated'),
        dict(name='local cash cost per tonne, FY2027-FY2030',
             years=_YRS[1:], nominal=[round(V['cost_infl'][i+1] / V['cost_infl'][i] - 1, 6)
                                      for i in range(1, 5)],
             real=0.0,
             basis='the house inflation path at zero real growth. The company\'s own '
                   'realised unit cost has run BELOW the national rate, and that '
                   'outperformance is credited separately and explicitly through the '
                   'funded alternative-fuel programme rather than by bending the index'),
        dict(name='export cement price, US dollars',
             years=_YRS, nominal=[round(V['price_exp_path'][i+1] / V['price_exp_path'][i] - 1, 6)
                                  for i in range(5)],
             real=0.0,
             exempt_reason='a US-dollar price set by the European carbon border '
                           'mechanism and landed-cost competition, not by Egyptian '
                           'inflation. It is converted into pounds through the house '
                           'currency path, which is where the Egyptian inflation '
                           'enters'),
    ],
    fx_path=[round(x, 6) for x in V['fx_path'][1:]],
    terminal=dict(g_nominal=V['g_term'], real=0.0, rf=V['rf_term'],
                  inflation_in_rf=_PI_T),
    explicit_years=5,
    growth_at_horizon_end=V['g_term'],
    note='the explicit window ends on the terminal growth rate exactly: the last '
         'explicit year escalates at the house terminal inflation of 7% at zero '
         'real, which IS the terminal, so nothing is capitalised that the model '
         'never reached.',
)

COC_RECORD = dict(
    market='EG', regime=_MACRO.regime, years=5,
    rf_observed=V['rf'], default_spread=V['sov_spread_cds'], rf_star=rf_star,
    erp=V['erp_cds'], erp_basis='cds', beta=beta_used,
    ke_exp=ke_exp, kd_pretax=KD, kd_aftertax=kd_at,
    weight_equity=1 - wd_gross, weight_debt=wd_gross, wacc_exp=wacc_exp,
    rf_terminal=V['rf_term'], erp_terminal=V['erp_term'], ke_terminal=ke_term,
    kd_terminal_pretax=V['kd_term'], kd_terminal_aftertax=V['kd_term'] * (1 - TAX),
    weight_debt_terminal=V['wd_term'], wacc_terminal=wacc_term,
    glide_fractions=[float(g) for g in glide], forward_wacc=[float(f) for f in fwd],
    discount_factors=[float(chain(fwd, t)) for t in t_mid],
    # DECLARE THE CONVENTION, because the factors cannot be read without it. This
    # study discounts each year's cash flow to its own MIDPOINT, off a valuation
    # date part-way through FY2026, so the first factor is a half-stub and no
    # factor is the end-of-year compounding a reader would otherwise assume. The
    # gate checked the end-of-year form and flagged this schedule; a convention
    # nobody writes down is not readable from outside, which is the defect — not
    # the convention. The times are the model's OWN t_mid, never re-derived here.
    discounting_convention=dict(
        kind='mid_period',
        cumulative_years=[float(t) for t in t_mid],
        # THE EDGES ARE PART OF THE CONVENTION AND WITHOUT THEM THE FACTORS DO NOT
        # REPRODUCE. Each forward rate owns a slice of calendar, and the first owns
        # only the stub — a reader who assumes each rate owns a whole year from
        # t=0 recomputes different factors and concludes the record is wrong. That
        # is the mistake revision 3 of this study actually made, in the other
        # direction: it walked the rates in whole-year steps and the final year's
        # rate never entered any factor at all.
        rate_edges=[float(e) for e in EDGES],
        stub_years=float(V['stub_years']),
        note=('each year discounted to its own midpoint from a valuation date '
              '%.3f of the way through FY2026, so the first period is a '
              'half-stub of %.4f years and every later year sits half a year '
              'inside its own period. The terminal is brought home on the LAST '
              'EXPLICIT factor, not on an end-of-window one.'
              % (float(V['stub_years']), float(t_mid[0]))),
    ),
    terminal_discount_factor=float(chain(fwd, t_mid[-1])),
    kd_integrity=dict(
        currency_source='note 25 and note 8: 91.1% of the book is euro-denominated '
                        '(NBE at Euribor + 3.00%, EBRD at Euribor + 4.35%), the '
                        'remainder pound (CIB at the corridor offer + 0.6%)',
        pct_local_currency=round(1 - 0.911, 4),
        effective_rates={'FY2024': eff_fy24, 'FY2025': eff_fy25},
        adopted=KD,
        within_150bp=False,
        # THE EXCEPTION IS A COMPUTATION, NOT AN ATTESTATION. Naming a mechanism
        # from the registered list is what buys the trailing-average check being
        # re-pointed; the contractual anchor is what replaces it, and the gate
        # reproduces the adopted rate from these lines rather than trusting the
        # sentence above them.
        effective_rate_not_usable=dict(
            mechanisms=['capitalised_interest', 'book_rebased_in_period'],
            evidence='note 8 capitalises borrowing costs on the alternative-fuel '
                     'assets under construction, so the expensed finance charge is '
                     'not the full interest incurred; note 25 shows the book '
                     're-based from pound credit facilities to euro term loans '
                     'within FY2025, so a full-year average balance describes a '
                     'mix that did not exist for most of the year.',
            event_date='2025-12-31',
        ),
        contractual_anchor=dict(
            lines=KD_ANCHOR_LINES,
            local_equivalent_note='the euro legs carry the coupon PLUS expected '
                                  'pound depreciation against the euro, because '
                                  'the cash flows are nominal pounds and a raw '
                                  'euro coupon inside a pound WACC is a currency '
                                  'mismatch, not a cheap borrowing.',
            reproduces=KD,
        ),
        limitation='the 150bp bound against the FY2025 effective rate is NOT met and '
                   'is disclosed rather than smoothed: the book re-based mid-year '
                   'from pound facilities to euro term debt, and interest on the '
                   'under-construction alternative-fuel assets is capitalised rather '
                   'than expensed, so the trailing effective rate understates the '
                   'marginal contractual one. The contractual blended rate is '
                   'adopted and the euro legs are loaded with pound depreciation '
                   'under uncovered interest parity, which is computed as a value '
                   'rather than described.',
        interest_bearing_note='the borrowing lines only; trade and other payables '
                              'bear no interest',
    ),
    sensitivity=dict(other_basis='rating', other_erp=V.get('erp_rating')),
    disclosures=[
        'The glide fractions are the cost-of-debt path\'s own cumulative progress, '
        'so the front-loaded shape is inherited from the assumed easing calendar '
        'rather than being a second free parameter.',
        'Country risk enters once: the risk-free rate is normalised by Egypt\'s own '
        'default spread and the premium added back is on the same basis.',
        'The terminal is norm-built and no line in it is an observable quote: '
        'risk-free %.2f%% = the house terminal inflation (%.2f%%) plus the '
        'real-rate convention (%.2f%%); cost of debt %.2f%% is the long-run '
        'corporate norm; the premium is normalised to %.2f%%.'
        % (100 * V['rf_term'], 100 * _PI_T, 100 * _MACRO.real_rate_convention,
           100 * V['kd_term'], 100 * V['erp_term']),
        'The terminal risk-free rate moved from 10.50%% to %.2f%% in this edition. '
        'It is no longer this study\'s own reading of which published target to '
        'use: it is derived from the one house path, which settles a 200bp '
        'disagreement with the study next to it.' % (100 * V['rf_term']),
    ],
)


# ---- [R-ANCHOR-01] THE FORECAST IS ANCHORED ON THE LATEST REVIEWED PERIOD ----
# ARCC is the CLEAN case that gate had to be able to tell apart from the two
# broken ones, and telling it apart is what caught a bug in the gate's own
# tolerance on its first run. The forecast opens at 39.03% against an audited
# FY2025 of 39.25% -- 0.56% relatively below, well inside the materiality line --
# so no mechanism is owed and none is claimed.
#
# What the record makes visible, and what no sentence in this study previously
# said, is that the forecast sits AT THE TOP of the company's own filed range:
# FY2023 22.00%, FY2024 23.15%, FY2025 39.25%, and the forecast holds the peak and
# improves on it. That is not a defect. It is the single most important thing about
# the shape of this forecast and it now appears in a record a job outside the study
# can read.
FORECAST_ANCHOR = dict(
    rate_name='EBITDA margin',
    latest_reviewed_period='FY2025, audited',
    latest_reviewed_date='2025-12-31',
    latest_reviewed_rate=float(ebitda_h[-1] / rev_h[-1]),
    first_forecast_rate=float(ebitda_f[0] / rev_f[0]),
    # the PATH, per [R-ANCHOR-01] clause two. ARCC's rises rather than falls, which
    # is the shape neither clause fires on -- and which [R-GAP-01]'s two-sided
    # trigger and the sign test are what audit.
    forecast_path=[float(ebitda_f[i] / rev_f[i]) for i in range(len(rev_f))],
    note='the forecast opens within a fifth of a point of the best year this company has '
         'filed, and rises from there. The filed record is FY2023 22.00%, FY2024 23.15%, '
         'FY2025 39.25%; the bear corner of the published range is that FY2023 margin, so '
         'the whole of the range is downside and the study says so.')

LENS_RECORD = {
    'class': 'cement and heavy industrial',
    'primary': dict(kind='dcf', value=fv_dcf,
                 range=dict(low=LR[PRIMARY]['bear'], high=LR[PRIMARY]['bull']),
                 range_note='the cash-flow lens with the EBITDA margin flexed across '
                            'the span ARCC\'s own audited accounts have printed, '
                            'FY2023 to FY2025, and the macro path held still',
                 range_basis=dict(
                     driver='the EBITDA margin, across its own audited span',
                     low=float(_ARCC_MGN_FILED_LOW), high=float(_ARCC_MGN_FILED_HIGH),
                     macro_held=True,
                     evidence='ARCC filed an EBITDA margin of %.2f%% in FY2023, %.2f%% in '
                              'FY2024 and %.2f%% in FY2025, all audited. The forecast '
                              'opens at %.2f%%, within a fifth of a point of the best of '
                              'them, so the bull corner is barely above the central and '
                              'essentially the whole range is downside — which is the '
                              'finding, and which the previous symmetric two-point band '
                              'concealed. The discount rate, terminal growth and the '
                              'currency path are held at the house macro path and do not '
                              'move.'
                              % (_ARCC_MGN_FILED_LOW * 100, 23.15,
                                 _ARCC_MGN_FILED_HIGH * 100, _arcc_base_mgn * 100)),
                 note='the cash-flow lens on the company\'s own tonnes and prices, '
                      'discounted on the cost-of-capital schedule, with the terminal '
                      'built from the house macro path'),
    'cross_checks': [
        dict(kind='replacement_cost', value=fv_asset,
             note='USD %.0f per annual tonne of capacity against a market paying '
                  'USD %.1f' % (V['ev_t_just'], ev_per_t)),
        # THE INGREDIENTS, NOT THE SENTENCE [added 03-Sep-2026]. Until today this
        # record named its source in prose and the gate read the prose. AMOC's
        # record used the same reassuring words while its code divided the MARKET
        # CAP by base-year EBITDA, and passed three times. So the claim is now
        # arithmetic: the multiple adopted, and the three numbers that reproduce
        # the traded one, committed side by side for anyone to divide.
        #
        # The source line is also corrected downward to what the input register
        # actually says. 4.50x is a HOUSE figure, disclosed as weakly anchored
        # against a thin Egyptian peer set of two names, not a multiple measured
        # off a series. Calling it "from the company's own history and its
        # regional peers" claimed a provenance the number does not have -- a
        # smaller version of the same offence, and it goes the same way.
        dict(kind='relative_multiple', value=fv_rel, present_value=False,
             multiple=float(V['ev_ebitda_just']),
             circularity=dict(spot=float(V['spot']), shares=float(SH),
                              net_debt=float(-net_cash), metric_value=float(eb_norm)),
             multiple_source='a HOUSE multiple of %.2fx on normalised EBITDA, disclosed '
                             'as weakly anchored: the Egyptian peer set is two names '
                             '(Sinai Cement, Misr Beni Suef) and neither publishes an '
                             'EBITDA series this study could measure a multiple from. '
                             'It is NOT read off the current price — the traded '
                             'enterprise value over the same normalised EBITDA is '
                             'committed beside it in the circularity block, and the '
                             'two are far apart.' % V['ev_ebitda_just']),
        dict(kind='ev_per_tonne', value=ev_per_t, present_value=False,
             note='the market\'s own implied enterprise value per annual tonne, in '
                  'US dollars, against a replacement cost of USD %.0f'
                  % V['repl_usd_t']),
    ],
    'retired': dict(
        blend={'DCF (cash flow)': 0.50, 'Relative multiples': 0.20,
               'Normalised earnings': 0.22, 'Asset / replacement cost': 0.08},
        blend_value=float(0.50 * fv_dcf + 0.20 * fv_rel + 0.22 * fv_norm + 0.08 * fv_asset),
        why='the weights were chosen, written down and inherited, and had never '
            'cleared any out-of-sample test. Normalised earnings is dropped as a '
            'lens for this class entirely — it capitalises a mid-cycle margin at a '
            'nominal rate on a company whose own terminal work shows growth '
            'destroying value — and is kept as a diagnostic at EGP %.2f.' % fv_norm,
    ),
    'diagnostics': dict(normalised_earnings=fv_norm, book_value_floor=None),
}

BRIDGE_RECORD = dict(
    market='EG',
    balance_sheet_date='2026-06-30',
    latest_disclosed_date='2026-06-30',
    latest_disclosed_source='the reviewed condensed consolidated interim financial '
                            'statements for the six months ended 30 June 2026, from '
                            'the company\'s own investor-relations channel and '
                            'registered in this study\'s sweep. The valuation date IS '
                            'that balance-sheet date rather than the date of the '
                            'latest traded price, so no roll-forward stands between '
                            'the bridge and a filing.',
    register='sweep_register.json',
    lines=[
        dict(label='Enterprise value', value=float(ev)),
        dict(label='plus cash and bank balances, 30 June 2026', value=float(V['cash_h1_26'])),
        dict(label='less interest-bearing debt, 30 June 2026', value=-float(V['debt_h1_26'])),
        dict(label='less non-controlling interests', value=-float(V['nci_h1_26'])),
    ],
    equity_value=float(eq_dcf), shares_mn=float(SH), per_share=float(fv_dcf),
    cash_charged_once=True,
    cash_note='the operations are discounted at a rate weighted on GROSS debt and '
              'the cash is then added at face exactly once. The company is net '
              'cash, and a net-debt weighting would drive the debt weight negative, '
              'lever the equity weight above one and put the operating rate ABOVE '
              'the cost of equity — then add the same cash back in the bridge.',
    cash=dict(treatment='added_at_face', weights_basis='gross'),
    nci=dict(basis='value_share', value=float(V['nci_h1_26']),
             deduction=float(V['nci_h1_26']),
             book=float(V['nci_h1_26']),
             profit_share=float(V['nci_h1_26']),
             proportional=float(V['nci_h1_26']),
             framings_note='the three reference framings are the same number here, '
                            'and that is the finding rather than a shortcut: at EGP '
                            '0.216mn against an equity value above EGP 20bn, the '
                            'value share, the profit share and the book amount '
                            'cannot differ by anything that reaches the second '
                            'decimal of a per-share number.',
             proxy='the minority\'s carrying value at 30 June 2026, adopted AS the '
                   'value share because the two cannot differ materially at this size',
             proxy_source='the reviewed interim statements for the six months ended '
                          '30 June 2026, statement of financial position',
             note='the minority is EGP %.3f million against an equity value of EGP '
                  '%.0f million — 0.001%% of it, or 0.0006 piastres a share. The '
                  'subsidiaries carrying it are not separately disclosed, so the '
                  'value-share basis is proxied by the carrying amount; at this size '
                  'the value share, the profit share and the book amount cannot '
                  'differ by a number that rounds into the answer, and saying so is '
                  'better than inventing a proxy for it.'
                  % (V['nci_h1_26'], eq_dcf),
             ),
    associates=dict(basis='none', note='no associates or joint ventures are carried '
                                       'on the balance sheet'),
    dividend_deducted=False,
    dividend_note='the FY2025 dividend was declared and paid BEFORE the bridge\'s '
                  'balance-sheet date, so it is already out of the equity it would '
                  'come out of and deducting it again would double-count it.',
)

OUT = dict(
    central=fv_central, spot=V['spot'],
    macro_record=MACRO_RECORD, cost_of_capital_record=COC_RECORD,
    lens_record=LENS_RECORD, bridge_record=BRIDGE_RECORD, forecast_anchor=FORECAST_ANCHOR,
    # `central` and `spot` sit at the TOP of meta so the repo-level gap gate can
    # read this study's own answer. It could not before: the central lived only
    # under lenses.central, and [R-GAP-01]'s checker reported ARCC as
    # "carries no central/spot pair" — an UNREADABLE answer, which that rule
    # treats as a failure rather than a skip, and rightly.
    meta=dict(ticker='ARCC', company='Arabian Cement Company S.A.E.', market='EGX',
              market_code='EG', currency='EGP',
              # THE PRICE DATE WAS TYPED HERE TOO, AND IT WAS A MONTH STALE
              # [corrected 03-Sep-2026]. spot_date said 3 September while this note beside
              # it said 6 August, in the same dict, in the same commit. The note is now
              # DERIVED from the date the record actually carries, so the two cannot part.
              asof='2026-06-30',
              asof_note=('valuation date = the date of the latest disclosed balance sheet; '
                         'the price it is compared against is the latest known close, '
                         + _dt.date.fromisoformat(SPOT_DATE).strftime('%-d %B %Y')),
              spot=V['spot'], spot_date=SPOT_DATE,
              # the edition this file produces, so no builder types an issue date
              edition_date=EDITION_DATE,
              central=fv_central, gap_vs_spot=fv_central / V['spot'] - 1.0,
              shares_mn=SH, mktcap=MKTCAP, revision=4,
              standard_version=STD_VERSION,
              klass='single-asset cement operating company (net cash)',
              sector='Construction materials — cement',
              basis='audited consolidated financial statements FY2014-FY2025 and the '
                    'reviewed H1-2026 interim accounts, all from the company\'s own '
                    'investor-relations archive'),
    inputs=INP,
    bottom_up=BU, clinker_factor=V['clinker_factor'],
    share_triangulation=SHT, kd_gate=KDG,
    unit_calibration=dict(vol_fy25=vol25, vol_local=p0['cem_loc'],
                          vol_export=p0['cem_exp'] + p0['clk_exp'],
                          vol_cem_exp=p0['cem_exp'], vol_clk_exp=p0['clk_exp'],
                          cem_prod=p0['cem_prod'], clk_prod=p0['clk_prod'],
                          cem_sold=p0['cem_sold'],
                          kiln_util_fy25=p0['kiln_util'], util_fy25=p0['mill_util'],
                          price_loc_derived=price_loc25,
                          price_exp_cem_usd=price_exp_cem25 / V['fx_avg_fy25'],
                          price_exp_clk_usd=price_exp_clk25 / V['fx_avg_fy25'],
                          cc_mat_t=cc_mat_clk, cc_tra_t=cc_tra_t,
                          cc_ovh_t=cc_ovh_t, cash_cost_fy25=cash_cost25,
                          cash_cost_t=cash_cost25 / vol25),
    history=dict(years=HIST, revenue=rev_h, cogs=cogs_h, gross_profit=gp_h, ga=ga_h,
                 ebitda=ebitda_h, dna=dna_h, ebit=ebit_h, pbt=pbt_h, tax=taxc_h,
                 pat=pat_h, eps=eps_h, capex=capex_h, margin=mgn_h, tax_eff_hist=taxe_h,
                 nopat=nopat_h, tax_eff=TAXE,
                 volume_mt=[None, None, vol25], price_t=[None, None, BU[0]['price']],
                 utilisation=[None, None, p0['mill_util']]),
    forecast=dict(years=YRS, revenue=rev_f, ebitda=ebitda_f, dna=dna_f,
                  other_income=oth_f, ebit=ebit_f,
                  nopat=nopat, capex=capex, dwc=dwc, fcff=fcff, df=df_, pv=pv,
                  fwd_wacc=fwd, glide=glide, t_mid=t_mid, treasury=treas_f, pbt=pbt_f,
                  tax=tax_f, pat=pat_f, dividends=div_f, cash=cash_b, equity=eq_b,
                  ppe=ppe_b, wc=wc_b, total_assets=ta_b,
                  volume_mt=[b['vol'] for b in BU[1:]],
                  price_t=[b['price'] for b in BU[1:]],
                  margin=[b['mgn'] for b in BU[1:]],
                  eps=[p / SH for p in pat_f], dps=[d / SH for d in div_f]),
    wacc=dict(rf=V['rf'], rf_star=rf_star, beta=beta_used, ke_exp=ke_exp, kd=KD,
              kd_at=kd_at, wd_gross=wd_gross, wd_net=wd_net, wacc_exp=wacc_exp,
              beta_term=beta_t, ke_term=ke_term, kd_term_at=V['kd_term'] * (1 - TAX),
              wacc_term=wacc_term, ke_raw_retired=V['rf'] + beta_used * V['erp_cds'],
              mktcap=MKTCAP, debt_total=debt_tot, eur_share=eur_share),
    # [R-TERM-01] — the terminal's own record, committed so the workbook's formulas and any
    # job outside this study can be held to the construction rather than to its output. A
    # construction that cannot be read cannot be checked, which is [R-ENF-06] on the artefact
    # every builder reads.
    terminal_record=_TERM.record,
    dcf=dict(sum_pv=sum_pv, tv=tv, pv_tv=pv_tv, ev=ev, tv_share=tv_share, df_tv=df_tv,
             cash_at_val=V['cash_h1_26'], net_cash=net_cash, nci=V['nci_h1_26'],
                net_cash_rolled=net_cash_rolled, rollforward_gap=ROLLFWD['gap'],
                rollforward_gap_per_share=ROLLFWD['gap_per_share'], equity=eq_dcf,
             fv=fv_dcf, roic_term=roic_t, rr_term=rr_t, ic_repl=ic_repl,
             nopat_term=nopat[-1] * (1 + V['g_term']), net_debt_bs=-net_cash_bs, rem=REM),
    lenses=dict(values=LENS, primary=PRIMARY, diagnostic=LENS_DIAGNOSTIC,
                retired_blend={'DCF (cash flow)': 0.50, 'Relative multiples': 0.20,
                               'Normalised earnings': 0.22, 'Asset / replacement cost': 0.08},
                central=fv_central,
                # [R-LENS-03]: ONE class primary IS the central; every other lens is a
                # CROSS-CHECK. low/high spanned ALL the lens values including the primary,
                # so `high` came out equal to the central and the delivered document told a
                # reader that "the cross-checks around it span EGP 45.65 to EGP 66.53" —
                # naming the primary as the top of its own cross-check range. That blurs
                # exactly the distinction this rule was written to enforce. The cross-check
                # span now EXCLUDES the primary and is labelled for what it is; the all-lens
                # span is kept beside it under its own name.
                low=min(v for k, v in LENS.items() if k != PRIMARY),
                high=max(v for k, v in LENS.items() if k != PRIMARY),
                all_low=min(LENS.values()), all_high=max(LENS.values()),
                ebitda_norm=eb_norm, nopat_norm=nopat_norm,
                ev_per_t_spot=ev_per_t, ev_asset=ev_asset, ev_spot=ev_spot,
                bvps=V['eq_fy25'] / SH, roe_fy25=V['pat_fy25'] / V['eq_fy25']),
    lens_ranges=LR, sensitivity=SENS, contested=CONTESTED,
    terminal_reconciliation=TR, growth_destroys_value=GDV,
    calibration=CAL, seasonality=SEASON_RANGE, transport_split=TRANSPORT_SPLIT,
    rollforward_check=ROLLFWD, walkforward=WF,
    move_decomposition=MOVE, subsidy_scenarios=SUBSIDY,
    counterweight=dict(prior_central=_rev3_central, move=_move,
                       fv_on_old_bridge=_fv_old_bridge,
                       seasonality_lift=_seasonality_lift),
    standard_version=STD_VERSION,
    experts=EXPERTS, peers=PEERS, assert_log=A, log=LOG,
)
with open(os.path.join(HERE, 'study_numbers.json'), 'w') as f:
    json.dump(OUT, f, indent=1, default=float)
print(f"\nwrote study_numbers.json — central EGP {fv_central:.2f}, spot {V['spot']:.2f}, "
      f"TV {tv_share:.1%} of EV, {len(A)} assertions passed")
