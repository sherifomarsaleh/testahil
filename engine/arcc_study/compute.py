"""ARCC (Arabian Cement Company S.A.E., EGX: ARCC) — master computation, REVISION 3.

REVISION 3 CORRECTS THE PRICE PATH, WHICH THE AUDITED RECORD DISPROVED.

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
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import numpy as np

LOG = []
def say(s):
    LOG.append(s); print(s)


def I(value, source, date, ring):
    return dict(value=value, source=source, date=date, ring=ring)


AFS25 = ("Audited consolidated financial statements for the year ended 31 December 2025, "
         "Deloitte (Wafik, Ramy & Partners), signed 25 February 2026")
AFS24 = ("Audited consolidated financial statements for the year ended 31 December 2024, "
         "Deloitte (Wafik, Ramy & Partners), signed 23 March 2025")
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
    spot=I(59.00, "Closing price 06-Aug-2026 from the supplied EGX daily series (open "
           "58.40, high 59.90, low 58.25)", "2026-08-06", "Market"),
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
    auc_fy25=I(391.543753, AFS25 + " — assets under construction, note 13: alternative-fuel "
               "system for production line 2 EGP 240.235mn, new steel cement silo for line "
               "1 EGP 146.239mn", "2025-12-31", "Company"),
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
    nci=I(0.158005, AFS25 + " — non-controlling interests, note 24: EGP 158,005. Revision 1 "
          "deducted EGP 150mn on inference from the profit statements; the audited figure "
          "is 950 times smaller and immaterial to the bridge", "2025-12-31", "Company"),

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
    price_local_path=I([1.0000, 1.0800, 1.1772, 1.2714, 1.3604, 1.4488],
                       "Local realised price index on the FY2025 base: growth of 8.0%, "
                       "9.0%, 8.0%, 7.0% and 6.5%, below the cost path in every year. IT IS "
                       "NOW ANCHORED ON A DISCLOSED PRICE HISTORY AND A DISCLOSED EXIT "
                       "RATE, which no earlier revision had. " + IRP + " and page 4 give "
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
    fx_path=I([49.26, 50.60, 53.10, 55.80, 58.60, 61.50],
              "USD/EGP path, FY2025 actual average then FY2026E-FY2030E",
              "2026-08-06", "House"),
    cost_infl=I([1.000, 1.115, 1.226, 1.336, 1.443, 1.544],
                "Cumulative local cost-inflation index from the FY2025 base. Steps of "
                "11.5%, 10.0%, 9.0%, 8.0% and 7.0% track the disinflation path the central "
                "bank's own reporting describes, converging on its 7% medium-term target. "
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
    capex_usd_t_cap=I(4.00, "Maintenance capital expenditure in US dollars per tonne of "
                      "installed capacity. Cross-check against disclosure: FY2025 capex of "
                      "EGP 796.471mn on 5.0Mt at an average USD/EGP of 49.26 is USD 3.23/t, "
                      "and FY2024's EGP 912.015mn is USD 4.11/t — but both years carry the "
                      "alternative-fuel and silo programmes, so the maintenance level is "
                      "set at the middle of that band and held", "2026-08-06", "Industry"),
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
    tax_eff=I(0.2382, AFS25 + " — income tax of EGP 1,125.468mn over pre-tax profit of EGP "
              "4,725.158mn. Note 10.2 separately discloses an average effective rate of "
              "23.33% (2024: 22.96%); Q1-2026 ran at 25.92%. Revision 1 inferred 29.43% by "
              "closing a MODELLED net finance income against disclosed profit, and "
              "over-taxed every forecast year by 5.6 points", "2025-12-31", "Company"),

    # ---- cost of capital ---------------------------------------------------
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
    kd_term=I(0.1350, "Terminal cost of debt = the terminal risk-free rate plus a 300bp "
              "corporate credit spread. Revision 3 carried 10.00% against a terminal "
              "risk-free rate of 12.50% — a corporate borrower funding 250bp BELOW its own "
              "sovereign in the same currency, printed one row above it in the same table. "
              "It is now built from the risk-free rate rather than asserted beside it, so "
              "the impossibility cannot recur", "2026-08-06", "House"),
    rf_term=I(0.1050, "Terminal risk-free rate, NORM-BUILT from the central bank's "
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
    g_term=I(0.0500, "Terminal growth, the house default for an established emerging-market "
             "industrial against a terminal risk-free rate that already embeds "
             "disinflation — approximately zero in real terms", "2026-08-06", "House"),
    stub_years=I(0.583, "Elapsed fraction of FY2026 at the valuation date — seven of twelve "
                 "months", "2026-08-06", "House"),

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
KDG = dict(eur_share=eur_share, kd_cib=kd_cib, kd_nbe=kd_nbe, kd_ebrd=kd_ebrd,
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
dna_f = [rev_f[i] * V['dna_pct'][i] for i in range(5)]
ebit_f = [ebitda_f[i] - dna_f[i] for i in range(5)]
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
roic_t = nopat[-1] * (1 + V['g_term']) / ic_repl
fcff = [nopat[i] + dna_f[i] - capex[i] - dwc[i] for i in range(5)]
fcff[0] *= REM
pv = [fcff[i] * df_[i] for i in range(5)]
sum_pv = float(np.sum(pv))
rr_t = V['g_term'] / roic_t
tv = nopat[-1] * (1 + V['g_term']) * (1 - rr_t) / (wacc_term - V['g_term'])
# TV is the value at the END of FY2030 of everything from FY2031 on, so it discounts
# at the end-of-window factor, not at the mid-year factor of the last explicit year.
df_tv = chain(fwd, REM + 4.0)
pv_tv = tv * df_tv
ev = sum_pv + pv_tv
tv_share = pv_tv / ev
# The bridge adds the cash BALANCE but revision 3 rolled the stub on FCFF, which
# excludes the treasury income actually earned on that balance over the seven months.
stub_interest = V['cash_fy25'] * V['cash_yield'][0] * V['stub_years'] * (1 - TAXE)
cash_at_val = (V['cash_fy25'] + fcff[0] / REM * V['stub_years'] + stub_interest
               - V['div_fy25_declared'])
# and the fresher disclosed debt is in the model already, used only as a check
net_cash = cash_at_val - V['debt_q1_26']
eq_dcf = ev + net_cash - V['nci']
fv_dcf = eq_dcf / SH
say(f"\n[Free cash flow] " + " ".join(f"{x:,.0f}" for x in fcff))
say(f"[Bridge] EV {ev:,.0f} = explicit {sum_pv:,.0f} + terminal {pv_tv:,.0f}; plus net "
    f"cash {net_cash:,.0f} (after deducting the EGP {V['div_fy25_declared']:,.0f}mn FY2025 "
    f"dividend declared and unpaid at 31 March 2026), less minorities {V['nci']:,.3f} = "
    f"equity {eq_dcf:,.0f} -> EGP {fv_dcf:.2f} per share")
say(f"[Terminal value] {tv_share:.1%} of enterprise value; terminal return on capital "
    f"{roic_t:.2%} against a terminal rate of {wacc_term:.2%}, reinvestment {rr_t:.1%}")

# ==================== 6. THE OTHER LENSES ===================================
eb_norm = V['rev_fy25'] * V['norm_rev_haircut'] * V['norm_mgn']
fv_rel = (eb_norm * V['ev_ebitda_just'] + net_cash - V['nci']) / SH
nopat_norm = (eb_norm - V['dna_fy25']) * (1 - TAXE)
fv_norm = (nopat_norm * V['pe_just'] + net_cash - V['nci']) / SH
ev_spot = MKTCAP - net_cash + V['nci']
ev_per_t = ev_spot / (V['cap_cement_mt'] * V['fx'])
ev_asset = V['ev_t_just'] * V['cap_cement_mt'] * V['fx']
fv_asset = (ev_asset + net_cash - V['nci']) / SH
LENS = {'DCF (cash flow)': fv_dcf, 'Relative multiples': fv_rel,
        'Normalised earnings': fv_norm, 'Asset / replacement cost': fv_asset}
WT = {'DCF (cash flow)': V['w_dcf'], 'Relative multiples': V['w_rel'],
      'Normalised earnings': V['w_norm'], 'Asset / replacement cost': V['w_asset']}
assert abs(sum(WT.values()) - 1.0) < 1e-9
fv_central = float(sum(LENS[k] * WT[k] for k in LENS))
say(f"\n[Lenses] " + " | ".join(f"{k.split()[0]} {v:.2f}" for k, v in LENS.items()))
say(f"[Central] EGP {fv_central:.2f} against a market price of EGP {V['spot']:.2f} "
    f"({fv_central/V['spot']-1:+.1%}); the market is paying USD {ev_per_t:.1f} per annual "
    f"tonne against a replacement cost of USD {V['repl_usd_t']:.0f}")


# ==================== 7. SENSITIVITY ========================================
def reval(nc=None, g=None, we=None, beta_=None, mgn_shift=0.0, capex_mult=1.0,
          dna_shift=0.0, nci=None, kd_=None):
    nc = net_cash if nc is None else nc
    g = V['g_term'] if g is None else g
    nci_ = V['nci'] if nci is None else nci
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
    ei = [eb[i] - dn[i] for i in range(5)]
    np_ = [ei[i] * (1 - TAXE) for i in range(5)]
    cx = [c * capex_mult for c in capex]
    fc = [np_[i] + dn[i] - cx[i] - dwc[i] for i in range(5)]
    fc[0] *= REM
    s = float(np.sum([fc[i] * d_[i] for i in range(5)]))
    rt = np_[-1] * (1 + g) / ic_repl
    tvl = np_[-1] * (1 + g) * (1 - g / rt) / (wt - g)
    return (s + tvl * d_[-1] + nc - nci_) / SH


def reval_two_anchor(we, wt):
    d_ = factors([we - (we - wt) * gg for gg in glide])
    s = float(np.sum([fcff[i] * d_[i] for i in range(5)]))
    tvl = nopat[-1] * (1 + V['g_term']) * (1 - rr_t) / (wt - V['g_term'])
    return (s + tvl * d_[-1] + net_cash - V['nci']) / SH


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
    mgn_grid=mgn_grid, mgn=[reval(mgn_shift=m) for m in mgn_grid],
    wt_grid=[wacc_term - 0.02, wacc_term - 0.01, wacc_term, wacc_term + 0.01,
             wacc_term + 0.02],
)
SENS['exp_term'] = [[reval_two_anchor(x, y) for y in SENS['wt_grid']] for x in wacc_grid]

# ==================== 8. CONTESTED CHOICES, COMPUTED ========================
fv_beta_dimson = reval(beta_=BETA['dimson']['sum_beta'])
fv_kd_egp = reval(kd_=kd_egp_equiv)
fv_capex_bookdep = reval(capex_mult=float(np.mean(dna_f)) / float(np.mean(capex)))
fv_taxstat = None
CONTESTED = [
    dict(choice='Cost of debt: currency composition as contracted (adopted) vs the '
                'pound-equivalent under uncovered interest parity',
         adopted=f"{KD:.2%}", alternative=f"{kd_egp_equiv:.2%}",
         fv_adopted=fv_dcf, fv_alternative=fv_kd_egp, effect=fv_kd_egp / fv_dcf - 1,
         note=('91% of the book is euro-denominated at Euribor-linked rates. Adopting the '
               'contracted rate means that debt is NOT compensated for pound depreciation '
               'beyond what this study already assumes; if the pound falls faster, the '
               'true pound cost of servicing it is understated by construction. The '
               'alternative is computed rather than described — and it is small, because '
               'debt is only 4.9% of the capital structure.')),
    dict(choice='Beta: contemporaneous regression (adopted) vs lead-lag sum-beta',
         adopted=f"{beta_used:.3f}", alternative=f"{BETA['dimson']['sum_beta']:.3f}",
         fv_adopted=fv_dcf, fv_alternative=fv_beta_dimson,
         effect=fv_beta_dimson / fv_dcf - 1,
         note=('The regression passes the usability gate, so it is adopted. It is also '
               'statistically weak, and the standard correction for a thinly traded share '
               'is higher.')),
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
# --- terminal growth: the ANALYTIC sign condition, not the textbook shortcut ----------
# The terminal block reinvests g/ROIC of terminal NOPAT, and ROIC is itself defined as
# N*(1+g)/IC on replacement-cost capital. The reinvestment charge therefore collapses to a
# FIXED g*IC and the whole block reduces to
#         TV(g) = [ N*(1+g) - g*IC ] / (W - g)
#         dTV/dg  proportional to  N*(1+W) - IC*W          <- no g in it at all
# so the direction of the growth lever is a CONSTANT of the model, and the hurdle is
#         N/IC  vs  W/(1+W)
# NOT the familiar ROIC vs W. The two differ by exactly (1+g)/(1+W), because ROIC is
# measured on TERMINAL-YEAR profit while the capital base is measured at the valuation
# date. Revision 2 sat at N/IC = 8.2% against a 13.6% hurdle and growth destroyed value;
# the corrected price path lifts terminal NOPAT enough to cross it by about 20bp, so
# growth now ADDS value — marginally, and the check below verifies the model agrees with
# its own algebra whichever side of the hurdle it lands on.
gdv_lhs = nopat[-1] * (1.0 + wacc_term)
gdv_rhs = ic_repl * wacc_term
GDV = dict(fv_at_g3=reval(g=0.03), fv_at_g7=reval(g=0.07), roic_term=roic_t,
           wacc_term=wacc_term, nopat_term=float(nopat[-1]), ic_replacement=float(ic_repl),
           n_over_ic=float(nopat[-1] / ic_repl), hurdle=float(wacc_term / (1 + wacc_term)),
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
say(f"[Growth and value — the correct hurdle] the terminal block reduces to "
    f"[N(1+g) - g.IC]/(W-g), so the sign of the growth lever is the constant "
    f"N(1+W) - IC.W and the test is N/IC vs W/(1+W), not ROIC vs W. "
    f"N/IC = {GDV['n_over_ic']:.3%} against a hurdle of {GDV['hurdle']:.3%} -> growth "
    f"{'ADDS' if GDV['analytic_adds_value'] else 'DESTROYS'} value by "
    f"{abs(GDV['n_over_ic']-GDV['hurdle'])*1e4:.0f}bp. Revision 3 read 13.81% against a "
    f"13.61% hurdle and concluded growth added value by 21bp — but its denominator was in "
    f"Aug-2026 pounds against a FY2031 numerator, and the currency-vintage error was "
    f"larger than the margin it was measuring")

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
                    'annual tonne. The 12.6Mt revival programme is the live test and it '
                    'runs against this lens: restarting a mothballed kiln costs a fraction '
                    'of building one, which is why this valuation is a ceiling and carries '
                    'only %.0f%% of the weight.'
                    % (V['ev_t_just'], V['w_asset'] * 100))),
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
LR['DCF (cash flow)'] = dict(bear=reval(mgn_shift=-0.02, we=wacc_exp + 0.015), base=fv_dcf,
                             bull=reval(mgn_shift=0.02, we=wacc_exp - 0.015))
LR['Weighted central'] = dict(
    bear=float(sum(LR[k]['bear'] * WT[k] for k in WT)), base=fv_central,
    bull=float(sum(LR[k]['bull'] * WT[k] for k in WT)))

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


chk(abs((ev + net_cash - V['nci']) - eq_dcf) < 1e-6,
    f"bridge closes exactly: EV {ev:,.2f} + net cash {net_cash:,.2f} - NCI {V['nci']:,.3f} "
    f"= equity {eq_dcf:,.2f}")
chk(net_cash > 0, f"net cash carries a POSITIVE sign into the bridge ({net_cash:,.1f})")
chk(V['nci'] > 0, f"minority interests are DEDUCTED ({V['nci']:,.3f}), not added")
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
chk(all(BU[i]['mgn'] > BU[i + 1]['mgn'] for i in range(1, 5)),
    "the forecast EBITDA margin glides DOWN every year from the FY2025 peak")
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
chk(abs(sum(WT.values()) - 1.0) < 1e-9, "lens weights sum to exactly 1")
chk(min(LENS.values()) <= fv_central <= max(LENS.values()),
    "the weighted central sits inside the range of the four lenses")
chk(eur_share > 0.5, f"the cost-of-debt build is currency-blended: {eur_share:.1%} of the "
                     f"book is euro-denominated and a single-currency shortcut would be wrong")
say("\n" + "=" * 78)
say("ASSERT LOG")
for i, m in enumerate(A, 1):
    say(f"  {i:2d}. {m}")
say("=" * 78)

# ==================== EMIT ==================================================
OUT = dict(
    meta=dict(ticker='ARCC', company='Arabian Cement Company S.A.E.', market='EGX',
              market_code='EG', currency='EGP', asof='2026-08-06', spot=V['spot'],
              shares_mn=SH, mktcap=MKTCAP, revision=3,
              klass='single-asset cement operating company (net cash)',
              sector='Construction materials — cement',
              basis='audited consolidated financial statements FY2023-FY2025 and reviewed '
                    'Q1-2026 interim accounts'),
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
    forecast=dict(years=YRS, revenue=rev_f, ebitda=ebitda_f, dna=dna_f, ebit=ebit_f,
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
    dcf=dict(sum_pv=sum_pv, tv=tv, pv_tv=pv_tv, ev=ev, tv_share=tv_share, df_tv=df_tv,
             cash_at_val=cash_at_val, net_cash=net_cash, nci=V['nci'], equity=eq_dcf,
             fv=fv_dcf, roic_term=roic_t, rr_term=rr_t, ic_repl=ic_repl,
             nopat_term=nopat[-1] * (1 + V['g_term']), net_debt_bs=-net_cash_bs, rem=REM),
    lenses=dict(values=LENS, weights=WT, central=fv_central, low=min(LENS.values()),
                high=max(LENS.values()), ebitda_norm=eb_norm, nopat_norm=nopat_norm,
                ev_per_t_spot=ev_per_t, ev_asset=ev_asset, ev_spot=ev_spot,
                bvps=V['eq_fy25'] / SH, roe_fy25=V['pat_fy25'] / V['eq_fy25']),
    lens_ranges=LR, sensitivity=SENS, contested=CONTESTED,
    terminal_reconciliation=TR, growth_destroys_value=GDV,
    experts=EXPERTS, peers=PEERS, assert_log=A, log=LOG,
)
with open(os.path.join(HERE, 'study_numbers.json'), 'w') as f:
    json.dump(OUT, f, indent=1, default=float)
print(f"\nwrote study_numbers.json — central EGP {fv_central:.2f}, spot {V['spot']:.2f}, "
      f"TV {tv_share:.1%} of EV, {len(A)} assertions passed")
