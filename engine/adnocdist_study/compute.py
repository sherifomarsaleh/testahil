"""ADNOC Distribution (ADX: ADNOCDIST) — the study's computation.

Writes study_numbers.json, the single source of truth every builder reads. No
financial numeral is typed into any builder; each one interpolates this file.

Code-first rule: INPUTS are four-field records {value, source, date, layer}; a
bare numeral cannot enter the model. The ASSERT block raises (and no JSON is
emitted) unless the income statements tie out to the filings, the forecast
balance sheet balances in every year, the cost-of-debt integrity triple holds,
the EV-to-equity bridge closes in both frames, the terminal block is
ROIC-consistent, and the lens weights sum to one.

UNITS: AED million throughout, except per-share and per-litre figures (AED) and
volumes (million litres). The filings report in AED thousands; every input
record carries the conversion in its source string.

THE CENTRAL CONTESTED JUDGEMENT — inventory movements. The company reports both
a headline and an "underlying" EBITDA, the difference being inventory gains and
losses: AED 254m (FY2024), AED 335m (FY2025) and AED 762m in H1-2026 alone,
against fuel volume growth of just 1.6% in that half. Whether that windfall
belongs in a forward earnings base is the single judgement that moves this
valuation most, so it is computed BOTH WAYS and published side by side:
  Frame A — NORMALISED: inventory movements are a timing effect on a
    pass-through cost and revert to zero through the cycle. FY2026 carries only
    the AED 762m already realised in the first half; FY2027 onward carry zero.
  Frame B — THROUGH-CYCLE CARRY: a persistent positive contribution, set at the
    FY2024-FY2025 average of AED 295m every forecast year, with FY2026 carrying
    the realised first half plus a second half at the FY2025 second-half rate.
Neither is averaged into the other.
"""
import os, json
HERE = os.path.dirname(os.path.abspath(__file__))


def I(value, source, date, layer):
    return dict(value=value, source=source, date=date, layer=layer)


# ---- source strings, hoisted so every record cites the document, not a memory
AUD23 = ("Abu Dhabi National Oil Company for Distribution PJSC, audited consolidated "
         "financial statements for the year ended 31 December 2023, published on the "
         "company's investor-relations site; figures as reported in AED'000 and "
         "converted to AED million")
AUD24 = ("Abu Dhabi National Oil Company for Distribution PJSC, audited consolidated "
         "financial statements for the year ended 31 December 2024, published on the "
         "company's investor-relations site; figures as reported in AED'000 and "
         "converted to AED million")
AUD25 = ("Abu Dhabi National Oil Company for Distribution PJSC, audited consolidated "
         "financial statements for the year ended 31 December 2025, published on the "
         "company's investor-relations site; figures as reported in AED'000 and "
         "converted to AED million")
INT26 = ("Abu Dhabi National Oil Company for Distribution PJSC, reviewed interim condensed "
         "consolidated financial statements for the six months ended 30 June 2026, "
         "published on the company's investor-relations site")
MDA25 = ("ADNOC Distribution, Management Discussion & Analysis Report, full year 2025, "
         "3 February 2026")
MDA26 = ("ADNOC Distribution, Management Discussion & Analysis Report, second quarter and "
         "first half 2026, 5 August 2026")
DECK25 = ("ADNOC Distribution, results presentation, full year 2025, 3 February 2026, "
          "operating-performance appendix")
DECK26 = ("ADNOC Distribution, results presentation, second quarter and first half 2026, "
          "5 August 2026, operating-performance appendix")
MKT = ("Daily price history for the ADX listing supplied for this study, cleaned through "
       "the study's own data screen")

INP = dict(
    # ---------------- market ----------------
    spot=I(4.07, MKT + "; last close 7 August 2026", "2026-08-07", "Market"),
    shares_mn=I(12500.0, AUD25 + ", share capital note: AED 1,000,000 thousand of "
                "issued capital in shares of AED 0.08 each", "2025-12-31", "Company"),

    # ---------------- income statement, three audited years ----------------
    rev_fy23=I(34629.178, AUD23, "2023-12-31", "Company"),
    rev_fy24=I(35453.716, AUD24, "2024-12-31", "Company"),
    rev_fy25=I(35896.617, AUD25, "2025-12-31", "Company"),
    dc_fy23=I(28792.893, AUD23 + ", direct costs", "2023-12-31", "Company"),
    dc_fy24=I(29237.684, AUD24 + ", direct costs", "2024-12-31", "Company"),
    dc_fy25=I(28950.827, AUD25 + ", direct costs", "2025-12-31", "Company"),
    gp_fy23=I(5836.285, AUD23 + ", gross profit", "2023-12-31", "Company"),
    gp_fy24=I(6216.032, AUD24 + ", gross profit", "2024-12-31", "Company"),
    gp_fy25=I(6945.790, AUD25 + ", gross profit", "2025-12-31", "Company"),
    da_exp_fy23=I(2916.538, AUD23 + ", distribution and administrative expenses",
                  "2023-12-31", "Company"),
    da_exp_fy24=I(3194.942, AUD24 + ", distribution and administrative expenses",
                  "2024-12-31", "Company"),
    da_exp_fy25=I(3323.546, AUD25 + ", distribution and administrative expenses",
                  "2025-12-31", "Company"),
    oi_fy23=I(145.645, AUD23 + ", other income", "2023-12-31", "Company"),
    oi_fy24=I(138.059, AUD24 + ", other income", "2024-12-31", "Company"),
    oi_fy25=I(167.665, AUD25 + ", other income", "2025-12-31", "Company"),
    imp_fy23=I(82.143, AUD23 + ", impairment losses and other operating expenses",
               "2023-12-31", "Company"),
    imp_fy24=I(90.254, AUD24 + ", impairment losses and other operating expenses",
               "2024-12-31", "Company"),
    imp_fy25=I(284.305, AUD25 + ", impairment losses and other operating expenses",
               "2025-12-31", "Company"),
    op_fy23=I(2983.249, AUD23 + ", operating profit", "2023-12-31", "Company"),
    op_fy24=I(3068.895, AUD24 + ", operating profit", "2024-12-31", "Company"),
    op_fy25=I(3505.604, AUD25 + ", operating profit", "2025-12-31", "Company"),
    intinc_fy23=I(98.834, AUD23 + ", interest income", "2023-12-31", "Company"),
    intinc_fy24=I(143.893, AUD24 + ", interest income", "2024-12-31", "Company"),
    intinc_fy25=I(71.274, AUD25 + ", interest income", "2025-12-31", "Company"),
    fin_fy23=I(432.757, AUD23 + ", finance costs", "2023-12-31", "Company"),
    fin_fy24=I(457.111, AUD24 + ", finance costs", "2024-12-31", "Company"),
    fin_fy25=I(402.945, AUD25 + ", finance costs", "2025-12-31", "Company"),
    pbt_fy23=I(2649.326, AUD23 + ", profit before tax", "2023-12-31", "Company"),
    pbt_fy24=I(2755.677, AUD24 + ", profit before tax", "2024-12-31", "Company"),
    pbt_fy25=I(3173.933, AUD25 + ", profit before tax", "2025-12-31", "Company"),
    tax_fy23=I(18.837, AUD23 + ", income tax expense", "2023-12-31", "Company"),
    tax_fy24=I(283.394, AUD24 + ", income tax expense", "2024-12-31", "Company"),
    tax_fy25=I(322.891, AUD25 + ", income tax expense", "2025-12-31", "Company"),
    np_fy23=I(2630.489, AUD23 + ", profit for the year", "2023-12-31", "Company"),
    np_fy24=I(2472.283, AUD24 + ", profit for the year", "2024-12-31", "Company"),
    np_fy25=I(2851.042, AUD25 + ", profit for the year", "2025-12-31", "Company"),
    nci_fy23=I(29.068, AUD23 + ", profit attributable to non-controlling interests",
               "2023-12-31", "Company"),
    nci_fy24=I(52.008, AUD24 + ", profit attributable to non-controlling interests",
               "2024-12-31", "Company"),
    nci_fy25=I(57.042, AUD25 + ", profit attributable to non-controlling interests",
               "2025-12-31", "Company"),
    eps_fy23=I(0.208, AUD23 + ", basic and diluted earnings per share", "2023-12-31", "Company"),
    eps_fy24=I(0.194, AUD24 + ", basic and diluted earnings per share", "2024-12-31", "Company"),
    eps_fy25=I(0.224, AUD25 + ", basic and diluted earnings per share", "2025-12-31", "Company"),

    # ---- depreciation and amortisation, from the cash-flow reconciliation ----
    dep_ppe_fy23=I(507.107, AUD24 + ", cash-flow statement, FY2023 comparative column",
                   "2023-12-31", "Company"),
    dep_ppe_fy24=I(602.186, AUD24 + ", cash-flow statement", "2024-12-31", "Company"),
    dep_ppe_fy25=I(594.222, AUD25 + ", cash-flow statement", "2025-12-31", "Company"),
    dep_rou_fy23=I(146.412, AUD24 + ", cash-flow statement, FY2023 comparative column",
                   "2023-12-31", "Company"),
    dep_rou_fy24=I(151.669, AUD24 + ", cash-flow statement", "2024-12-31", "Company"),
    dep_rou_fy25=I(151.000, AUD25 + ", cash-flow statement", "2025-12-31", "Company"),
    amort_fy23=I(43.046, AUD24 + ", cash-flow statement, FY2023 comparative column",
                 "2023-12-31", "Company"),
    amort_fy24=I(31.952, AUD24 + ", cash-flow statement", "2024-12-31", "Company"),
    amort_fy25=I(30.724, AUD25 + ", cash-flow statement", "2025-12-31", "Company"),

    # ---- cash flow ----
    ocf_fy23=I(5051.268, AUD24 + ", FY2023 comparative", "2023-12-31", "Company"),
    ocf_fy24=I(3931.453, AUD24, "2024-12-31", "Company"),
    ocf_fy25=I(3922.041, AUD25, "2025-12-31", "Company"),
    capex_ppe_fy23=I(1000.290, AUD24 + ", payments for purchases of property, plant and "
                     "equipment, FY2023 comparative", "2023-12-31", "Company"),
    capex_ppe_fy24=I(1116.830, AUD24 + ", payments for purchases of property, plant and "
                     "equipment", "2024-12-31", "Company"),
    capex_ppe_fy25=I(1180.747, AUD25 + ", payments for purchases of property, plant and "
                     "equipment", "2025-12-31", "Company"),
    capex_adv_fy23=I(31.951, AUD24 + ", payments for advances to contractors, FY2023 "
                     "comparative", "2023-12-31", "Company"),
    capex_adv_fy24=I(62.403, AUD24 + ", payments for advances to contractors",
                     "2024-12-31", "Company"),
    capex_adv_fy25=I(26.647, AUD25 + ", payments for advances to contractors",
                     "2025-12-31", "Company"),
    divpaid_fy23=I(2622.890, AUD24 + ", dividends paid, FY2023 comparative",
                   "2023-12-31", "Company"),
    divpaid_fy24=I(2613.700, AUD24 + ", dividends paid", "2024-12-31", "Company"),
    divpaid_fy25=I(2599.146, AUD25 + ", dividends paid", "2025-12-31", "Company"),
    leasepay_fy25=I(201.454, AUD25 + ", payment of lease liabilities", "2025-12-31", "Company"),

    # ---------------- balance sheet, three audited years ----------------
    ppe_fy23=I(7189.661, AUD23 + ", property, plant and equipment", "2023-12-31", "Company"),
    ppe_fy24=I(7552.178, AUD24 + ", property, plant and equipment", "2024-12-31", "Company"),
    ppe_fy25=I(8032.197, AUD25 + ", property, plant and equipment", "2025-12-31", "Company"),
    rou_fy23=I(1778.418, AUD23 + ", right-of-use assets", "2023-12-31", "Company"),
    rou_fy24=I(1726.351, AUD24 + ", right-of-use assets", "2024-12-31", "Company"),
    rou_fy25=I(1445.804, AUD25 + ", right-of-use assets", "2025-12-31", "Company"),
    gwi_fy23=I(1053.811, AUD23 + ", goodwill and intangible assets", "2023-12-31", "Company"),
    gwi_fy24=I(599.307, AUD24 + ", goodwill and intangible assets", "2024-12-31", "Company"),
    gwi_fy25=I(621.853, AUD25 + ", goodwill and intangible assets", "2025-12-31", "Company"),
    onca_fy23=I(56.183, AUD23 + ", advances to contractors 38.466 plus deferred tax asset "
                "2.166 plus other non-current assets 15.551", "2023-12-31", "Company"),
    onca_fy24=I(62.103, AUD24 + ", advances to contractors 47.656 plus other non-current "
                "assets 14.447", "2024-12-31", "Company"),
    onca_fy25=I(49.420, AUD25 + ", advances to contractors 36.596 plus other non-current "
                "assets 12.824", "2025-12-31", "Company"),
    inv_fy23=I(1294.423, AUD23 + ", inventories", "2023-12-31", "Company"),
    inv_fy24=I(1619.887, AUD24 + ", inventories", "2024-12-31", "Company"),
    inv_fy25=I(1574.254, AUD25 + ", inventories", "2025-12-31", "Company"),
    tr_fy23=I(3519.413, AUD23 + ", trade receivables and other current assets",
              "2023-12-31", "Company"),
    tr_fy24=I(2935.982, AUD24 + ", trade receivables and other current assets",
              "2024-12-31", "Company"),
    tr_fy25=I(2632.515, AUD25 + ", trade receivables and other current assets",
              "2025-12-31", "Company"),
    dfrp_fy23=I(805.558, AUD23 + ", due from related parties", "2023-12-31", "Company"),
    dfrp_fy24=I(750.723, AUD24 + ", due from related parties", "2024-12-31", "Company"),
    dfrp_fy25=I(758.468, AUD25 + ", due from related parties", "2025-12-31", "Company"),
    td_fy23=I(200.225, AUD23 + ", term deposits", "2023-12-31", "Company"),
    td_fy24=I(200.225, AUD24 + ", term deposits", "2024-12-31", "Company"),
    td_fy25=I(200.000, AUD25 + ", term deposits", "2025-12-31", "Company"),
    cash_fy23=I(2993.937, AUD23 + ", cash and bank balances", "2023-12-31", "Company"),
    cash_fy24=I(2734.038, AUD24 + ", cash and bank balances", "2024-12-31", "Company"),
    cash_fy25=I(2360.854, AUD25 + ", cash and bank balances", "2025-12-31", "Company"),
    ta_fy23=I(18891.629, AUD23 + ", total assets", "2023-12-31", "Company"),
    ta_fy24=I(18180.794, AUD24 + ", total assets", "2024-12-31", "Company"),
    ta_fy25=I(17675.365, AUD25 + ", total assets", "2025-12-31", "Company"),
    eqp_fy23=I(3472.066, AUD23 + ", equity attributable to owners of the Company",
               "2023-12-31", "Company"),
    eqp_fy24=I(2991.839, AUD24 + ", equity attributable to owners of the Company",
               "2024-12-31", "Company"),
    eqp_fy25=I(3230.423, AUD25 + ", equity attributable to owners of the Company",
               "2025-12-31", "Company"),
    nciq_fy23=I(323.767, AUD23 + ", non-controlling interests", "2023-12-31", "Company"),
    nciq_fy24=I(189.437, AUD24 + ", non-controlling interests", "2024-12-31", "Company"),
    nciq_fy25=I(230.374, AUD25 + ", non-controlling interests", "2025-12-31", "Company"),
    borr_fy23=I(5492.280, AUD23 + ", borrowings: term loan non-current 5,492.280, no short "
                "term borrowing", "2023-12-31", "Company"),
    borr_fy24=I(5590.644, AUD24 + ", borrowings: term loan non-current 5,494.859 plus short "
                "term borrowings 95.785", "2024-12-31", "Company"),
    borr_fy25=I(5545.975, AUD25 + ", borrowings note: term loan non-current 5,499.591 plus "
                "short term borrowings 46.384", "2025-12-31", "Company"),
    lease_fy23=I(1747.264, AUD23 + ", lease liabilities: non-current 1,564.251 plus current "
                 "183.013", "2023-12-31", "Company"),
    lease_fy24=I(1722.622, AUD24 + ", lease liabilities: non-current 1,540.894 plus current "
                 "181.728", "2024-12-31", "Company"),
    lease_fy25=I(1446.327, AUD25 + ", lease liabilities note: non-current 1,289.459 plus "
                 "current 156.868", "2025-12-31", "Company"),
    tp_fy23=I(2541.355, AUD23 + ", trade and other payables", "2023-12-31", "Company"),
    tp_fy24=I(2797.054, AUD24 + ", trade and other payables", "2024-12-31", "Company"),
    tp_fy25=I(3115.634, AUD25 + ", trade and other payables", "2025-12-31", "Company"),
    dtrp_fy23=I(4827.631, AUD23 + ", due to related parties", "2023-12-31", "Company"),
    dtrp_fy24=I(4439.345, AUD24 + ", due to related parties", "2024-12-31", "Company"),
    dtrp_fy25=I(3646.512, AUD25 + ", due to related parties", "2025-12-31", "Company"),
    provs_fy25=I(453.592, AUD25 + ", provision for decommissioning 167.399 plus provision "
                 "for employees' end of service benefit 207.103 plus deferred tax liability "
                 "79.090", "2025-12-31", "Company"),
    oncl_fy25=I(6.528, AUD25 + ", other non-current liabilities", "2025-12-31", "Company"),
    tl_fy25=I(14214.568, AUD25 + ", total liabilities", "2025-12-31", "Company"),

    # ---------------- revenue disaggregation (the unit build's revenue leg) ----
    rev_retfuel_fy24=I(22223.252, AUD25 + ", revenue note, FY2024 comparative: Retail (B2C) "
                       "fuel", "2024-12-31", "Company"),
    rev_retfuel_fy25=I(22796.987, AUD25 + ", revenue note: Retail (B2C) fuel",
                       "2025-12-31", "Company"),
    rev_nonfuel_fy24=I(1575.410, AUD25 + ", revenue note, FY2024 comparative: Retail (B2C) "
                       "non-fuel", "2024-12-31", "Company"),
    rev_nonfuel_fy25=I(1783.747, AUD25 + ", revenue note: Retail (B2C) non-fuel",
                       "2025-12-31", "Company"),
    rev_corp_fy24=I(10084.840, AUD25 + ", revenue note, FY2024 comparative: Commercial "
                    "(B2B) corporate", "2024-12-31", "Company"),
    rev_corp_fy25=I(9571.682, AUD25 + ", revenue note: Commercial (B2B) corporate",
                    "2025-12-31", "Company"),
    rev_avi_fy24=I(1570.214, AUD25 + ", revenue note, FY2024 comparative: Commercial (B2B) "
                   "aviation", "2024-12-31", "Company"),
    rev_avi_fy25=I(1744.201, AUD25 + ", revenue note: Commercial (B2B) aviation",
                   "2025-12-31", "Company"),
    rev_retfuel_h126=I(13169.965, INT26 + ", revenue note: Retail (B2C) fuel, six months",
                       "2026-06-30", "Company"),
    rev_nonfuel_h126=I(927.421, INT26 + ", revenue note: Retail (B2C) non-fuel, six months",
                       "2026-06-30", "Company"),
    rev_corp_h126=I(6282.376, INT26 + ", revenue note: Commercial (B2B) corporate, six "
                    "months", "2026-06-30", "Company"),
    rev_avi_h126=I(1655.242, INT26 + ", revenue note: Commercial (B2B) aviation, six months",
                   "2026-06-30", "Company"),
    rev_h126=I(22035.004, INT26 + ", revenue, six months ended 30 June 2026",
               "2026-06-30", "Company"),
    gp_h126=I(4252.102, INT26 + ", gross profit, six months ended 30 June 2026",
              "2026-06-30", "Company"),
    op_h126=I(2516.642, INT26 + ", operating profit, six months ended 30 June 2026",
              "2026-06-30", "Company"),
    np_h126=I(2127.694, INT26 + ", profit for the period, six months ended 30 June 2026",
              "2026-06-30", "Company"),
    daexp_h126=I(1646.280, INT26 + ", distribution and administrative expenses, six months",
                 "2026-06-30", "Company"),
    dna_h126=I(369.702, INT26 + ", distribution and administrative expenses note: "
               "depreciation and amortisation, six months", "2026-06-30", "Company"),
    oi_h126=I(90.705, INT26 + ", other income, six months", "2026-06-30", "Company"),
    imp_h126=I(179.885, INT26 + ", impairment losses and other operating expenses, six "
               "months", "2026-06-30", "Company"),
    rev_q126=I(8833.596, INT26 + ", revenue for the six months 22,035.004 less the three "
               "months ended 30 June 13,201.408", "2026-03-31", "Company"),
    rev_retfuel_h125=I(10771.947, INT26 + ", revenue note, prior-period comparative column: "
                       "Retail (B2C) fuel", "2025-06-30", "Company"),
    rev_nonfuel_h125=I(838.658, INT26 + ", revenue note, prior-period comparative column: "
                       "Retail (B2C) non-fuel", "2025-06-30", "Company"),
    rev_corp_h125=I(4685.586, INT26 + ", revenue note, prior-period comparative column: "
                    "Commercial (B2B) corporate", "2025-06-30", "Company"),
    rev_avi_h125=I(815.393, INT26 + ", revenue note, prior-period comparative column: "
                   "Commercial (B2B) aviation", "2025-06-30", "Company"),
    gp_retfuel_h125=I(1993.0, "Derived from " + MDA26 + ": fuel retail gross profit of AED "
                      "2,462 million in the first half of 2026 was stated to be 23.5% above "
                      "the prior period, which places the prior period at AED 1,993 million. "
                      "The company does not print the prior-period segment figure itself",
                      "2025-06-30", "Company"),
    gp_comm_h125=I(841.0, "Derived from " + MDA26 + ": commercial gross profit of AED 1,268 "
                   "million was stated to be 50.8% above the prior period, which places the "
                   "prior period at AED 841 million", "2025-06-30", "Company"),
    gp_nonfuel_h125=I(465.0, "Derived from " + MDA26 + ": non-fuel retail gross profit of "
                      "AED 522 million was stated to be 12.3% above the prior period, which "
                      "places the prior period at AED 465 million", "2025-06-30", "Company"),
    rev_fy22=I(32111.061, "Abu Dhabi National Oil Company for Distribution PJSC, audited "
               "consolidated financial statements for the year ended 31 December 2023, "
               "FY2022 comparative column", "2022-12-31", "Company"),
    np_fy22=I(2748.508, "FY2023 audited filing, FY2022 comparative column: profit for the "
              "year", "2022-12-31", "Company"),

    # ---------------- volumes (million litres) — the unit build's volume leg ----
    vol_retail_fy24=I(10349.0, DECK25 + ", fuel volumes: Retail (B2C), FY2024 comparative",
                      "2024-12-31", "Company"),
    vol_retail_fy25=I(11042.0, DECK25 + ", fuel volumes: Retail (B2C)", "2025-12-31", "Company"),
    vol_comm_fy24=I(4680.0, DECK25 + ", fuel volumes: Commercial (B2B), FY2024 comparative",
                    "2024-12-31", "Company"),
    vol_comm_fy25=I(4668.0, DECK25 + ", fuel volumes: Commercial (B2B)", "2025-12-31", "Company"),
    vol_retail_h126=I(5376.0, DECK26 + ", fuel volumes: Retail (B2C), six months",
                      "2026-06-30", "Company"),
    vol_retail_h125=I(5324.0, DECK26 + ", fuel volumes: Retail (B2C), prior-period "
                      "comparative", "2025-06-30", "Company"),
    vol_comm_h126=I(2372.0, DECK26 + ", fuel volumes: Commercial (B2B), six months",
                    "2026-06-30", "Company"),
    vol_comm_h125=I(2300.0, DECK26 + ", fuel volumes: Commercial (B2B), prior-period "
                    "comparative", "2025-06-30", "Company"),
    vol_corp_h126=I(2015.0, DECK26 + ", of which corporate, six months", "2026-06-30", "Company"),
    vol_avi_h126=I(357.0, DECK26 + ", of which aviation, six months", "2026-06-30", "Company"),
    vol_corp_h125=I(2068.0, DECK26 + ", of which corporate, prior-period comparative",
                    "2025-06-30", "Company"),
    vol_avi_h125=I(232.0, DECK26 + ", of which aviation, prior-period comparative",
                   "2025-06-30", "Company"),

    # ---------------- segment gross profit ----------------
    gp_retfuel_fy25=I(4233.0, MDA25 + ", fuel retail gross profit", "2025-12-31", "Company"),
    gp_nonfuel_fy25=I(984.0, MDA25 + ", non-fuel retail gross profit", "2025-12-31", "Company"),
    gp_comm_fy25=I(1729.0, MDA25 + ", commercial gross profit", "2025-12-31", "Company"),
    gp_retfuel_h126=I(2462.0, MDA26 + ", fuel retail gross profit, six months",
                      "2026-06-30", "Company"),
    gp_nonfuel_h126=I(522.0, MDA26 + ", non-fuel retail gross profit, six months",
                      "2026-06-30", "Company"),
    gp_comm_h126=I(1268.0, MDA26 + ", commercial gross profit, six months",
                   "2026-06-30", "Company"),

    # ---------------- inventory movements — the contested judgement ----------
    invgain_fy24=I(254.0, MDA25 + ", inventory gains of AED 254 million in 2024",
                   "2024-12-31", "Company"),
    invgain_fy25=I(335.0, MDA25 + ", inventory gains of AED 335 million in 2025",
                   "2025-12-31", "Company"),
    invgain_retfuel_fy25=I(321.0, MDA25 + ", fuel retail inventory gains", "2025-12-31", "Company"),
    invgain_comm_fy25=I(14.0, MDA25 + ", commercial segment inventory gains",
                        "2025-12-31", "Company"),
    invgain_h125=I(147.0, MDA26 + ", inventory gains of AED 147 million in H1 2025",
                   "2025-06-30", "Company"),
    invgain_h126=I(762.0, MDA26 + ", inventory gains of AED 762 million in H1 2026",
                   "2026-06-30", "Company"),
    invgain_retfuel_h126=I(528.0, MDA26 + ", fuel retail inventory gains, six months",
                           "2026-06-30", "Company"),
    invgain_comm_h126=I(233.0, MDA26 + ", commercial segment inventory gains, six months",
                        "2026-06-30", "Company"),
    invgain_retfuel_h125=I(148.0, MDA26 + ", fuel retail inventory gains, prior-period "
                           "comparative", "2025-06-30", "Company"),
    invgain_comm_h125=I(-1.0, MDA26 + ", commercial segment inventory losses of AED 1 "
                        "million, prior-period comparative", "2025-06-30", "Company"),
    ebitda_und_fy24=I(3633.0, MDA25 + ", underlying EBITDA, defined by the company as EBITDA "
                      "excluding inventory movements and one-off items", "2024-12-31", "Company"),
    ebitda_und_fy25=I(4001.0, MDA25 + ", underlying EBITDA", "2025-12-31", "Company"),

    # ---------------- network and transactions ----------------
    stations_fy25=I(1010.0, MDA25 + ", total stations network: 567 UAE, 199 Saudi Arabia, "
                    "244 Egypt", "2025-12-31", "Company"),
    stations_h126=I(1045.0, MDA26 + ", total stations network: 569 UAE, 231 Saudi Arabia, "
                    "245 Egypt", "2026-06-30", "Company"),
    stations_h125=I(939.0, DECK26 + ", total service stations, prior-period comparative",
                    "2025-06-30", "Company"),
    stations_uae_h126=I(569.0, DECK26 + ", service stations, UAE", "2026-06-30", "Company"),
    stations_ksa_h126=I(231.0, DECK26 + ", service stations, Saudi Arabia",
                        "2026-06-30", "Company"),
    stations_egy_h126=I(245.0, DECK26 + ", service stations, Egypt", "2026-06-30", "Company"),
    cstores_h126=I(541.0, MDA26 + ", total convenience stores network: 387 UAE, 15 Saudi "
                   "Arabia, 139 Egypt", "2026-06-30", "Company"),
    fueltxn_h126=I(100.9, DECK26 + ", fuel transactions, UAE, millions, six months",
                   "2026-06-30", "Company"),
    fueltxn_h125=I(96.2, DECK26 + ", fuel transactions, UAE, prior-period comparative",
                   "2025-06-30", "Company"),
    nonfueltxn_h126=I(26.4, DECK26 + ", non-fuel transactions, UAE, millions, six months",
                      "2026-06-30", "Company"),
    nonfueltxn_h125=I(26.0, DECK26 + ", non-fuel transactions, UAE, prior-period comparative",
                      "2025-06-30", "Company"),
    evpoints_h126=I(406.0, MDA26 + ", electric-vehicle fast and super-fast charging points "
                    "in the UAE", "2026-06-30", "Company"),

    # ---------------- cost of capital ----------------
    rf_observed=I(0.0448, "UAE Ministry of Finance, July 2026 auction of dirham-denominated "
                  "federal Treasury Bonds: yield to maturity of 4.48% on the January 2031 "
                  "tranche, 4 basis points above comparable US Treasuries. This is a local-"
                  "currency sovereign yield at a tenor matching the forecast horizon, not a "
                  "US Treasury substituted for one", "2026-07-30", "Country"),
    sov_spread=I(0.0004,
                 "Sovereign default spread ACTUALLY EMBEDDED IN THE INSTRUMENT the risk-free "
                 "rate is taken from: the UAE Ministry of Finance July-2026 auction cleared "
                 "the January-2031 dirham Treasury Bond at 4.48%, a spread of 4 basis points "
                 "over comparable US Treasuries. CHANGED 09-Aug-2026, superseding the 0.42% "
                 "ratings-based figure from the published country-risk file. The "
                 "normalisation exists to remove sovereign credit risk from the observed "
                 "yield so it is not counted twice inside the equity risk premium; the amount "
                 "to remove is the amount the yield actually contains. Removing 42 basis "
                 "points from a bond carrying 4 produced a normalised rate 38 basis points "
                 "BELOW the matched-tenor US Treasury and 59 below the US 10-year, which "
                 "cannot be right for a currency hard-pegged to the dollar. The 0.42% "
                 "ratings figure remains the basis of the country risk premium added back "
                 "inside the equity risk premium, so country risk still enters exactly once",
                 "2026-07-30", "Country"),
    erp_total=I(0.0487, "Damodaran country risk premium file, January 2026 vintage: United "
                "Arab Emirates total equity risk premium 4.87%, being the 4.23% mature-market "
                "premium plus a 0.64% country risk premium", "2026-01-01", "Country"),
    erp_mature=I(0.0423, "Damodaran country risk premium file, January 2026 vintage: "
                 "mature-market equity risk premium", "2026-01-01", "Country"),
    crp=I(0.0064, "Damodaran country risk premium file, January 2026 vintage: United Arab "
          "Emirates country risk premium", "2026-01-01", "Country"),
    beta=I(0.6494, "Five-year weekly regression of the company's own returns against the "
           "FTSE ADX General Index, the published index of its own exchange; 257 weekly "
           "observations to 24-Jul-2026, R-squared 0.179, standard error 0.087, 90% "
           "confidence interval 0.51 to 0.79. Supersedes the 0.509 carried by the first "
           "edition, which regressed against an equal-weight composite of the exchange's "
           "listed names because no published index series was held at the time",
           "2026-07-24", "Market"),
    credit_margin=I(0.0060, AUD25 + ", borrowings note: the term loan refinanced in October "
                    "2022 carries EIBOR plus a margin of 0.60% on the dirham portion and the "
                    "Secured Overnight Financing Rate plus 0.85% on the US dollar portion",
                    "2025-12-31", "Company"),
    credit_margin_usd=I(0.0085, AUD25 + ", borrowings note: US dollar facility margin",
                        "2025-12-31", "Company"),
    cb_base_rate=I(0.0365, "Central Bank of the UAE, Base Rate applicable to the Overnight "
                   "Deposit Facility, maintained at 3.65% at the July 2026 review",
                   "2026-07-29", "Country"),
    tax_statutory=I(0.09, "United Arab Emirates federal corporate tax at 9%, in force for "
                    "financial years beginning on or after 1 June 2023",
                    "2023-06-01", "Country"),
    tax_effective=I(0.1017, "Computed from the audited filings: income tax expense of AED "
                    "322.891 million over profit before tax of AED 3,173.933 million in "
                    "FY2025, above the 9% federal rate because the Egyptian subsidiary is "
                    "taxed at a higher rate", "2025-12-31", "Company"),

    # ---------------- forecast drivers ----------------
    vol_retail_g=I([0.012, 0.020, 0.018, 0.015, 0.012],
                   "Retail fuel volume growth. Anchored on the 1.0% achieved in the first "
                   "half of 2026 and the 6.7% of FY2025, then set from the two forces that "
                   "actually move it: network expansion (the network went from 939 to 1,045 "
                   "stations year on year, with Saudi Arabia growing 65% on a capital-light "
                   "dealer-owned model) against a slow electric-vehicle drag that builds "
                   "through the decade. The taper to 1.2% by FY2030 is the drag being priced, "
                   "not an assumption of decline", "2026-08-05", "Company"),
    vol_comm_g=I([0.030, 0.025, 0.020, 0.018, 0.015],
                 "Commercial fuel volume growth. The first half of 2026 grew 3.1%, with "
                 "aviation up 53.9% offsetting a deliberate 2.5% reduction in corporate "
                 "volumes under a stated value-over-volume strategy. Aviation growth "
                 "decelerates off a small base", "2026-08-05", "Company"),
    gp_retfuel_per_l_g=I([0.020, 0.020, 0.020, 0.020, 0.020],
                         "Escalation of the structural retail fuel margin per litre. This is "
                         "a domestic regulated-margin line, so it takes the domestic "
                         "inflation escalator, not a commodity path — the fuel itself is a "
                         "pass-through cost and is escalated separately through the realised "
                         "price", "2026-08-05", "Industry"),
    gp_comm_per_l_g=I([0.170, 0.020, 0.020, 0.020, 0.020],
                      "Escalation of the structural commercial margin per litre. The 17% "
                      "step in FY2026 is the realised first-half outcome, where corporate "
                      "gross profit per litre excluding inventory movements was 28% higher "
                      "year on year on the company's own disclosure; it then reverts to the "
                      "domestic inflation escalator", "2026-08-05", "Company"),
    rev_nonfuel_g=I([0.100, 0.100, 0.090, 0.080, 0.080],
                    "Non-fuel retail revenue growth, driven by transactions and store format "
                    "rather than by fuel. The company's own medium-term target is to double "
                    "non-fuel transactions between 2023 and 2030, which is 10.4% a year "
                    "compounded; the forecast takes that rate for two years and then fades "
                    "it. Supporting evidence: 16 new properties opened in the first half of "
                    "2026 against 8 a year earlier, a partnership announced with Americana "
                    "Restaurants for up to 200 quick-service restaurants, and 30 large-format "
                    "sites planned by 2030 of which seven are open", "2026-08-05", "Company"),
    gm_nonfuel=I([0.560, 0.560, 0.560, 0.560, 0.560],
                 "Non-fuel retail gross margin, held at the level realised in the first half "
                 "of 2026 (AED 522 million of gross profit on AED 927 million of revenue, "
                 "56.3%) and the 55.2% of FY2025", "2026-06-30", "Company"),
    price_retfuel=I([2.420, 2.340, 2.363, 2.387, 2.411],
                    "Realised retail price per litre. The first half of 2026 realised AED "
                    "2.4498 against AED 2.0233 a year earlier, a 21% increase driven by "
                    "crude, not by the company. The path assumes the second half of 2026 "
                    "moderates, crude normalises through FY2027, and the realised price then "
                    "escalates at 1.0% a year. This is a globally-traded input on its own "
                    "commodity path — it is deliberately NOT escalated on a domestic "
                    "inflation index", "2026-08-05", "Global"),
    price_comm=I([3.050, 2.950, 2.980, 3.010, 3.040],
                 "Realised commercial price per litre, on the same crude path as the retail "
                 "price. The first half of 2026 realised AED 3.3453 across corporate and "
                 "aviation combined against AED 2.3924 a year earlier", "2026-08-05", "Global"),
    cash_opex_g=I([0.040, 0.040, 0.040, 0.040, 0.040],
                  "Cash operating cost growth. Staff, utilities, repairs and marketing are "
                  "domestic service costs, so they take the domestic inflation escalator of "
                  "about 2% plus roughly 2.5% of network growth, less the company's stated "
                  "efficiency programme of up to AED 184 million of like-for-like cost "
                  "reduction over 2024-2028. The first half of 2026 grew 4.0% year on year, "
                  "which is the rate carried", "2026-08-05", "Country"),
    other_income_g=I([0.030, 0.030, 0.030, 0.030, 0.030],
                     "Other income growth, held at the domestic inflation escalator",
                     "2026-08-05", "Country"),
    impair_norm=I([360.0, 220.0, 225.0, 230.0, 235.0],
                  "Impairment losses and other operating expenses. FY2025 carried AED 284.3 "
                  "million and the first half of 2026 AED 179.9 million, both elevated by "
                  "what the company describes as prudence-based provisioning; FY2026 carries "
                  "the realised first half annualised, then a normalised level escalating "
                  "with inflation", "2026-08-05", "Company"),
    stations_g=I([0.025, 0.045, 0.040, 0.035, 0.030],
                 "Service-station network growth. The network grew 11.3% in the year to "
                 "June 2026 (939 to 1,045 stations) on the company's stated expansion "
                 "programme across the United Arab Emirates, Saudi Arabia and Egypt. The "
                 "path decelerates from that realised rate as the domestic network "
                 "saturates and the incremental site becomes marginal. This is a CAPITAL "
                 "decision and is modelled separately from throughput because the two have "
                 "different futures", "2026-06-30", "Company"),
    litres_per_station_g=I([-0.010, -0.025, -0.020, -0.010, -0.005],
                           "Growth in litres sold per station. Realised at MINUS 9.3% in "
                           "the year to June 2026: retail volume rose 1.0% while the "
                           "network rose 11.3%, so throughput per site fell. The decline "
                           "fades as the expansion rate itself slows and the newest sites "
                           "mature toward the network average. This is the single most "
                           "important observable on the terminal-growth question and it is "
                           "now a model driver rather than a narrative aside",
                           "2026-06-30", "Company"),
    vol_corp_g=I([0.000, 0.005, 0.010, 0.010, 0.010],
                 "Corporate fuel volume growth. Realised MINUS 2.6% in the first half of "
                 "2026 (2,068 to 2,015 million litres) on customer rationalisation. Held "
                 "roughly flat thereafter", "2026-06-30", "Company"),
    vol_avi_g=I([0.000, 0.040, 0.030, 0.025, 0.020],
                "Aviation fuel volume growth. Realised PLUS 53.9% in the first half of 2026 "
                "(232 to 357 million litres) on new airline contracts and Gulf traffic "
                "recovery. Faded hard, because a 54% step is a contract ramp and not a "
                "growth rate; carrying it forward would capitalise a one-off", 
                "2026-06-30", "Company"),
    price_corp=I([3.05, 2.95, 2.98, 3.01, 3.04],
                 "Realised corporate price per litre, on the same crude path as the retail "
                 "leg. Anchored on the 3.12 realised in the first half of 2026",
                 "2026-06-30", "Company"),
    price_avi=I([4.55, 4.40, 4.44, 4.49, 4.53],
                "Realised aviation price per litre, on the same crude path. Anchored on the "
                "4.64 realised in the first half of 2026. Jet fuel prices roughly 50% above "
                "the corporate leg, which is why blending the two destroys information",
                "2026-06-30", "Company"),
    fueltxn_g=I([0.010, 0.025, 0.022, 0.020, 0.018],
                "Growth in fuel transactions. Realised 4.9% in the first half of 2026 (96.2 "
                "to 100.9 million) on the larger network", "2026-06-30", "Company"),
    conversion_g=I([-0.005, -0.010, 0.000, 0.005, 0.005],
                   "Growth in the non-fuel conversion rate — the share of fuel customers "
                   "who also buy inside. It FELL from 27.0% to 26.2% in the year to June "
                   "2026, which is the opposite of what the non-fuel strategy needs, and "
                   "the forecast carries that deterioration before assuming it stabilises",
                   "2026-06-30", "Company"),
    basket_g=I([0.015, 0.035, 0.030, 0.030, 0.030],
               "Growth in the average non-fuel basket, on the domestic price escalator plus "
               "the stated shift toward higher-margin food service", "2026-06-30", "Company"),
    dep_rate=I(0.0836,
               "Depreciation and amortisation as a share of the OPENING fixed and "
               "right-of-use asset base, measured off the audited FY2025 accounts (775.9 on "
               "an opening base of 9,278.5). Replaces a hardcoded five-year depreciation "
               "array: the charge is now an output of the asset base the model itself rolls "
               "forward", "2025-12-31", "Company"),
    maint_capex_rate=I(0.0836,
                       "Maintenance capital spending as a share of the opening fixed and "
                       "right-of-use base, set equal to the depreciation rate — the "
                       "standard steady-state condition that a network replaces what it "
                       "consumes. Growth spending is modelled separately, per station added",
                       "2025-12-31", "Company"),
    capex_per_station=I(3.5924,
                        "Capital cost per station added, in AED million. Backed out of the "
                        "company's OWN FY2026 capital-spending guidance: the guidance "
                        "midpoint of 1,010 less maintenance of 792.4 on the opening base "
                        "leaves 217.6 for the 60.6 stations the network plan adds, giving "
                        "3.59 per station (about USD 1.0 million). So FY2026 still "
                        "reconciles to guidance while FY2027-30 follow the network plan "
                        "rather than a pasted array", "2026-02-03", "Company"),
    dna_fwd=I([800.0, 830.0, 862.0, 894.0, 926.0],
              "Depreciation and amortisation, grown on the asset base as capital spending "
              "exceeds the current charge; the first half of 2026 charge of AED 369.7 million "
              "annualises to AED 739 million before the year's additions",
              "2026-08-05", "Company"),
    capex_fwd=I([1010.0, 1060.0, 1100.0, 1140.0, 1180.0],
                "Capital expenditure. FY2026 takes the midpoint of the company's own "
                "reaffirmed guidance of US$250-300 million, which is AED 0.9-1.1 billion; "
                "FY2025 spent AED 1,051 million on an accrual basis. Later years grow with "
                "the network target of 1,150 stations by 2028 from about 1,000 at the end of "
                "2025. Saudi expansion is capital-light because those stations are "
                "dealer-owned and company-operated", "2026-08-05", "Company"),
    tax_dmtt=I(0.15, "United Arab Emirates domestic minimum top-up tax of 15%, in force for "
               "financial years beginning on or after 1 January 2025 for groups with "
               "consolidated revenue above EUR 750 million. The FY2025 audited tax "
               "reconciliation does NOT apply it — that note reconciles at the 9% domestic "
               "rate for an effective 10.2% — so the base case follows the filing and the "
               "15% case is priced as a sensitivity rather than assumed",
               "2025-01-01", "Country"),
    invmove_A=I([762.0, 0.0, 0.0, 0.0, 0.0],
                "Inventory movements, NORMALISED frame. FY2026 carries only the AED 762 "
                "million already realised in the first half; nothing is assumed for the "
                "second half and nothing thereafter, on the view that a timing difference on "
                "a pass-through cost nets to zero through a full price cycle",
                "2026-08-05", "Company"),
    invmove_B=I([950.0, 295.0, 295.0, 295.0, 295.0],
                "Inventory movements, THROUGH-CYCLE frame. FY2026 carries the realised first "
                "half plus a second half at the FY2025 second-half rate of AED 188 million; "
                "later years carry the FY2024-FY2025 average of AED 295 million, on the view "
                "that a company holding physical stock in a market with a persistent upward "
                "price drift earns a small positive contribution on average",
                "2026-08-05", "Company"),
    g_terminal=I(0.015, "Terminal growth. Set below the 2% domestic inflation escalator "
                 "because a fuel retailer's principal volume driver faces a structural "
                 "electric-vehicle drag beyond the forecast horizon; the non-fuel business "
                 "grows faster but is a fifth of gross profit",
                 "2026-08-05", "Industry"),
    roic_terminal=I(0.250, "Terminal return on invested capital. The company earned a 32.7% "
                    "return on capital employed in FY2025 and 40.1% in the first half of "
                    "2026 on its own measure; the terminal figure fades that toward a level "
                    "a mature, more capital-intensive network would sustain",
                    "2026-08-05", "Company"),
    beta_drift_frac=I(0.389, "Fraction of the distance from the measured beta to the "
                      "market beta of one that the terminal beta is allowed to travel, as "
                      "transition risk in the business rises and the regulated margin "
                      "becomes a smaller share of a more diversified earnings base. Stated "
                      "as a fraction so the terminal beta is DERIVED from the measured one "
                      "rather than asserted alongside it: re-measure the beta and the "
                      "terminal beta follows",
                      "2026-08-05", "Market"),
    wd_terminal=I(0.100, "Terminal debt weight, above today's 5.5% because the current "
                  "weight reflects an unusually high equity market value against a small "
                  "and stable borrowing book", "2026-08-05", "Market"),
    payout_floor=I(0.75,
                   "Dividend policy FLOOR as the company actually states it: USD 700 million "
                   "a year, or a minimum of 75% of net profit, whichever is higher, for the "
                   "years 2024 to 2030. ADDED 09-Aug-2026: the study previously used the "
                   "realised 92% payout as though it were the policy term, in two places, "
                   "contradicting both the primary disclosure and the study's own catalyst "
                   "table", "2026-04-01", "Company"),
    payout=I(0.92, "Dividend payout used in the equity roll-forward. Dividends paid were AED "
             "2,622.9 million, AED 2,613.7 million and AED 2,599.1 million in FY2023, FY2024 "
             "and FY2025 against profit attributable to owners of AED 2,601.4 million, AED "
             "2,420.3 million and AED 2,794.0 million — a payout that has run at or above "
             "100% of earnings and is set slightly below that as profits step up",
             "2025-12-31", "Company"),
    dps=I(0.2057, "Dividend per share. FY2025 dividends paid of AED 2,599.146 million over "
          "12,500 million shares is AED 0.2079; the company's stated policy sets a fixed "
          "annual dividend of 20.57 fils per share", "2025-12-31", "Company"),
)

V = {k: v['value'] for k, v in INP.items()}
for k, rec in INP.items():
    assert set(rec) == {'value', 'source', 'date', 'layer'}, k
    assert rec['source'] and rec['date'] and rec['layer'], f'{k} is not four-field complete'

YRS = ['FY2026E', 'FY2027E', 'FY2028E', 'FY2029E', 'FY2030E']
HYRS = ['FY2023', 'FY2024', 'FY2025']
N = 5

# ============================ HISTORY ============================
H = {}
for y in ('23', '24', '25'):
    key = f'FY20{y}'
    dna = V[f'dep_ppe_fy{y}'] + V[f'dep_rou_fy{y}'] + V[f'amort_fy{y}']
    rev, gp, op = V[f'rev_fy{y}'], V[f'gp_fy{y}'], V[f'op_fy{y}']
    cash_opex = V[f'da_exp_fy{y}'] - dna
    ebitda = gp - cash_opex + V[f'oi_fy{y}'] - V[f'imp_fy{y}']
    # tie-out: the reported operating profit must rebuild from its own components
    chk = gp - V[f'da_exp_fy{y}'] + V[f'oi_fy{y}'] - V[f'imp_fy{y}']
    assert abs(chk - op) < 0.01, f'{key} operating profit does not tie out: {chk} vs {op}'
    chk2 = op + V[f'intinc_fy{y}'] - V[f'fin_fy{y}']
    assert abs(chk2 - V[f'pbt_fy{y}']) < 0.01, f'{key} profit before tax does not tie out'
    assert abs((V[f'pbt_fy{y}'] - V[f'tax_fy{y}']) - V[f'np_fy{y}']) < 0.01, \
        f'{key} profit for the year does not tie out'
    assert abs(ebitda - (op + dna)) < 0.01, f'{key} EBITDA does not tie out'
    H[key] = dict(
        revenue=rev, direct_costs=V[f'dc_fy{y}'], gross_profit=gp,
        gross_margin=gp / rev, opex=V[f'da_exp_fy{y}'], dna=dna, cash_opex=cash_opex,
        other_income=V[f'oi_fy{y}'], impairments=V[f'imp_fy{y}'],
        ebitda=ebitda, ebitda_margin=ebitda / rev, ebit=op,
        interest_income=V[f'intinc_fy{y}'], finance_costs=V[f'fin_fy{y}'],
        pbt=V[f'pbt_fy{y}'], tax=V[f'tax_fy{y}'], tax_rate=V[f'tax_fy{y}'] / V[f'pbt_fy{y}'],
        net_profit=V[f'np_fy{y}'], nci=V[f'nci_fy{y}'],
        np_attributable=V[f'np_fy{y}'] - V[f'nci_fy{y}'], eps=V[f'eps_fy{y}'],
        ppe=V[f'ppe_fy{y}'], rou=V[f'rou_fy{y}'], goodwill_intangibles=V[f'gwi_fy{y}'],
        other_nca=V[f'onca_fy{y}'], inventories=V[f'inv_fy{y}'],
        receivables=V[f'tr_fy{y}'], due_from_rp=V[f'dfrp_fy{y}'],
        term_deposits=V[f'td_fy{y}'], cash=V[f'cash_fy{y}'], total_assets=V[f'ta_fy{y}'],
        equity_parent=V[f'eqp_fy{y}'], nci_equity=V[f'nciq_fy{y}'],
        total_equity=V[f'eqp_fy{y}'] + V[f'nciq_fy{y}'],
        borrowings=V[f'borr_fy{y}'], leases=V[f'lease_fy{y}'],
        payables=V[f'tp_fy{y}'], due_to_rp=V[f'dtrp_fy{y}'],
        ocf=V[f'ocf_fy{y}'], capex=V[f'capex_ppe_fy{y}'] + V[f'capex_adv_fy{y}'],
        dividends_paid=V[f'divpaid_fy{y}'],
        net_debt_company=V[f'borr_fy{y}'] - V[f'cash_fy{y}'] - V[f'td_fy{y}'],
        net_debt_incl_leases=(V[f'borr_fy{y}'] + V[f'lease_fy{y}']
                              - V[f'cash_fy{y}'] - V[f'td_fy{y}']),
    )
    H[key]['fcf'] = H[key]['ocf'] - H[key]['capex']
    H[key]['roce'] = H[key]['ebit'] / (H[key]['total_equity'] + H[key]['net_debt_company'])

# the company's own published net debt for FY2025 must reproduce
assert abs(H['FY2025']['net_debt_company'] - 2985.121) < 0.01, 'FY2025 net debt does not tie out'
assert abs(H['FY2025']['ebitda'] - 4281.550) < 0.02, 'FY2025 EBITDA does not tie out'

# ============================ UNIT BUILD ============================
# Revenue is volume x realised price; gross profit is volume x margin per litre.
# For a regulated fuel retailer these are different questions: the realised price
# is a pass-through of crude and moves revenue and direct cost together, while the
# margin per litre is what the business actually earns. Separating them is what
# makes the inventory-movement judgement visible instead of buried in a blended
# margin percentage.
UB = {}
UB['vol_retail_fy24'] = V['vol_retail_fy24']
UB['vol_retail_fy25'] = V['vol_retail_fy25']
UB['vol_comm_fy24'] = V['vol_comm_fy24']
UB['vol_comm_fy25'] = V['vol_comm_fy25']
UB['vol_total_fy25'] = V['vol_retail_fy25'] + V['vol_comm_fy25']
UB['vol_total_fy24'] = V['vol_retail_fy24'] + V['vol_comm_fy24']
UB['price_retail_fy25'] = V['rev_retfuel_fy25'] / V['vol_retail_fy25']
UB['price_retail_fy24'] = V['rev_retfuel_fy24'] / V['vol_retail_fy24']
UB['rev_comm_fy25'] = V['rev_corp_fy25'] + V['rev_avi_fy25']
UB['rev_comm_fy24'] = V['rev_corp_fy24'] + V['rev_avi_fy24']
UB['price_comm_fy25'] = UB['rev_comm_fy25'] / V['vol_comm_fy25']
UB['price_comm_fy24'] = UB['rev_comm_fy24'] / V['vol_comm_fy24']
UB['price_retail_h126'] = V['rev_retfuel_h126'] / V['vol_retail_h126']
UB['price_retail_h125'] = V['rev_retfuel_h125'] / V['vol_retail_h125']
UB['rev_comm_h126'] = V['rev_corp_h126'] + V['rev_avi_h126']
UB['rev_comm_h125'] = V['rev_corp_h125'] + V['rev_avi_h125']
UB['price_comm_h126'] = UB['rev_comm_h126'] / V['vol_comm_h126']
UB['price_comm_h125'] = UB['rev_comm_h125'] / V['vol_comm_h125']
UB['price_corp_h126'] = V['rev_corp_h126'] / V['vol_corp_h126']
UB['price_avi_h126'] = V['rev_avi_h126'] / V['vol_avi_h126']

# structural margin per litre — gross profit stripped of inventory movements
UB['gp_retfuel_struct_fy25'] = V['gp_retfuel_fy25'] - V['invgain_retfuel_fy25']
UB['gp_comm_struct_fy25'] = V['gp_comm_fy25'] - V['invgain_comm_fy25']
UB['margin_retail_fy25'] = UB['gp_retfuel_struct_fy25'] / V['vol_retail_fy25']
UB['margin_comm_fy25'] = UB['gp_comm_struct_fy25'] / V['vol_comm_fy25']
UB['gp_retfuel_struct_h126'] = V['gp_retfuel_h126'] - V['invgain_retfuel_h126']
UB['gp_comm_struct_h126'] = V['gp_comm_h126'] - V['invgain_comm_h126']
UB['margin_retail_h126'] = UB['gp_retfuel_struct_h126'] / V['vol_retail_h126']
UB['margin_comm_h126'] = UB['gp_comm_struct_h126'] / V['vol_comm_h126']
UB['margin_retail_h125'] = ((V['gp_retfuel_h125'] - V['invgain_retfuel_h125'])
                            / V['vol_retail_h125'])
UB['margin_comm_h125'] = (V['gp_comm_h125'] - V['invgain_comm_h125']) / V['vol_comm_h125']
UB['margin_retail_growth_h1'] = UB['margin_retail_h126'] / UB['margin_retail_h125'] - 1
UB['margin_comm_growth_h1'] = UB['margin_comm_h126'] / UB['margin_comm_h125'] - 1
UB['gm_nonfuel_fy25'] = V['gp_nonfuel_fy25'] / V['rev_nonfuel_fy25']
UB['gm_nonfuel_h126'] = V['gp_nonfuel_h126'] / V['rev_nonfuel_h126']

# ---- BOTTOM-UP UNIT ANCHORS (added 09-Aug-2026) -------------------------------------
# Every one of these is derived from two disclosed quantities, never asserted. Where the
# company does not disclose a split, the allocation is named and flagged rather than hidden.
#
# Retail throughput. The company discloses the station count and the retail volume, so the
# litres each station actually sells is arithmetic, not an assumption — and it is the number
# that shows retail growth is network-led: throughput per station fell 9.3% year on year
# while the network grew 11.3%.
UB['litres_per_station_fy25'] = V['vol_retail_fy25'] / V['stations_fy25']
UB['litres_per_station_h126'] = V['vol_retail_h126'] / V['stations_h126']
UB['litres_per_station_h125'] = V['vol_retail_h125'] / V['stations_h125']
UB['litres_per_station_growth_h1'] = (UB['litres_per_station_h126']
                                      / UB['litres_per_station_h125'] - 1)
UB['stations_growth_h1'] = V['stations_h126'] / V['stations_h125'] - 1

# Corporate and aviation volumes for FY2025. FLAGGED GAP: the company splits commercial
# VOLUME at the half year and commercial REVENUE at the full year, but does not split the
# full-year volume. It is allocated here on the DISCLOSED first-half-2025 volume ratio, and
# the allocation is checked against the disclosed full-year revenue: it implies a corporate
# realised price of about 2.28 and an aviation price of about 3.70 against first-half-2025
# disclosed prices of 2.27 and 3.52, so the allocation is consistent with the revenue split
# rather than merely convenient.
UB['corp_share_vol_h125'] = V['vol_corp_h125'] / (V['vol_corp_h125'] + V['vol_avi_h125'])
UB['vol_corp_fy25'] = V['vol_comm_fy25'] * UB['corp_share_vol_h125']
UB['vol_avi_fy25'] = V['vol_comm_fy25'] * (1 - UB['corp_share_vol_h125'])
UB['price_corp_fy25'] = V['rev_corp_fy25'] / UB['vol_corp_fy25']
UB['price_avi_fy25'] = V['rev_avi_fy25'] / UB['vol_avi_fy25']
UB['price_corp_h125'] = V['rev_corp_h125'] / V['vol_corp_h125']
UB['price_avi_h125'] = V['rev_avi_h125'] / V['vol_avi_h125']
UB['vol_corp_growth_h1'] = V['vol_corp_h126'] / V['vol_corp_h125'] - 1
UB['vol_avi_growth_h1'] = V['vol_avi_h126'] / V['vol_avi_h125'] - 1

# Non-fuel, built as transactions x basket. Fuel transactions for FY2025 are derived from
# the disclosed retail volume and the disclosed litres per fuel transaction, so the
# transaction base is arithmetic from two reported numbers.
UB['litres_per_txn_h126'] = V['vol_retail_h126'] / V['fueltxn_h126']
UB['fueltxn_fy25'] = V['vol_retail_fy25'] / UB['litres_per_txn_h126']
UB['conversion_h126'] = V['nonfueltxn_h126'] / V['fueltxn_h126']
UB['conversion_h125'] = V['nonfueltxn_h125'] / V['fueltxn_h125']
UB['conversion_fy25'] = UB['conversion_h125']
UB['basket_fy25'] = V['rev_nonfuel_fy25'] / (UB['fueltxn_fy25'] * UB['conversion_fy25'])
UB['basket_h126'] = V['rev_nonfuel_h126'] / V['nonfueltxn_h126']

# Depreciation and maintenance capital spending, measured off the audited history rather
# than pasted as five-year arrays.
UB['fixed_base_fy24'] = H['FY2024']['ppe'] + H['FY2024']['rou']
UB['fixed_base_fy25'] = H['FY2025']['ppe'] + H['FY2025']['rou']
UB['dep_rate_fy25'] = H['FY2025']['dna'] / UB['fixed_base_fy24']
# the segment gross profits must rebuild the reported total
_seg = V['gp_retfuel_fy25'] + V['gp_nonfuel_fy25'] + V['gp_comm_fy25']
assert abs(_seg - V['gp_fy25']) < 1.0, f'FY2025 segment gross profit {_seg} vs reported {V["gp_fy25"]}'
_segh = V['gp_retfuel_h126'] + V['gp_nonfuel_h126'] + V['gp_comm_h126']
assert abs(_segh - V['gp_h126']) < 1.5, 'first-half segment gross profit does not rebuild'
# the revenue disaggregation must rebuild the reported total
_rv = (V['rev_retfuel_fy25'] + V['rev_nonfuel_fy25'] + V['rev_corp_fy25'] + V['rev_avi_fy25'])
assert abs(_rv - V['rev_fy25']) < 0.01, 'FY2025 revenue disaggregation does not rebuild'
_rvh = (V['rev_retfuel_h126'] + V['rev_nonfuel_h126'] + V['rev_corp_h126'] + V['rev_avi_h126'])
assert abs(_rvh - V['rev_h126']) < 0.01, 'first-half revenue disaggregation does not rebuild'

# ============================ FORECAST ============================
# BUILT BOTTOM-UP, at the finest level the company actually discloses. Rebuilt 09-Aug-2026
# after an external audit showed the previous build blended corporate and aviation into one
# "commercial" leg while the company reports them separately — and that the unexplained +17%
# FY2026 margin step was sitting inside exactly that blend. Four legs now, each on its own
# physical driver:
#
#   retail fuel   = SERVICE STATIONS x LITRES PER STATION, both disclosed, then x margin/litre
#   corporate     = own volume x own realised price, own volume driver
#   aviation      = own volume x own realised price, own volume driver
#   non-fuel      = NON-FUEL TRANSACTIONS x BASKET, both disclosed, then x gross margin
#
# and two capital lines that were hardcoded arrays and are now derived from the asset base:
#
#   depreciation  = OPENING fixed and right-of-use base x a rate measured off the history
#   capital spend = maintenance (% of the opening base) + growth (stations added x unit cost)
#
# WHAT THIS EXPOSES, which the blended build hid: retail volume growth is NOT organic. The
# network grew 11.3% year on year while retail volume grew 1.0%, so litres per station fell
# 9.3%. The forecast now carries those two facts as separate drivers instead of netting them
# into one growth rate, because they have different futures — stations are a capital decision
# and throughput per station is a demand observation.
F = dict(years=YRS)

# ---- retail fuel: stations x litres per station -------------------------------------
# EVERY leg is anchored on the ANNUALISED DISCLOSED FIRST HALF of 2026, not on FY2025.
# Two quarters of the study year are already on the public record, and the sweep rule
# requires them swept in before the build. The first element of each driver array is
# therefore the SECOND-HALF SHAPE on that realised run rate; growth proper starts FY2027.
# An earlier version grew the FY2025 base instead and put aviation 24% BELOW its own
# realised half-year run rate — the forecast contradicted the disclosure it was built on.
sta, lps = [], []
_s, _l = V['stations_h126'], UB['litres_per_station_h126'] * 2
for i in range(N):
    _s *= (1 + V['stations_g'][i])
    _l *= (1 + V['litres_per_station_g'][i])
    sta.append(_s)
    lps.append(_l)
F['stations'] = sta
F['litres_per_station'] = lps
vol_r = [sta[i] * lps[i] for i in range(N)]
F['vol_retail'] = vol_r

# ---- corporate and aviation: separate legs, opposite volume directions --------------
vol_co, vol_av = [], []
_c, _a = V['vol_corp_h126'] * 2, V['vol_avi_h126'] * 2
for i in range(N):
    _c *= (1 + V['vol_corp_g'][i])
    _a *= (1 + V['vol_avi_g'][i])
    vol_co.append(_c)
    vol_av.append(_a)
F['vol_corp'] = vol_co
F['vol_avi'] = vol_av
vol_c = [vol_co[i] + vol_av[i] for i in range(N)]
F['vol_comm'] = vol_c
F['vol_total'] = [vol_r[i] + vol_c[i] for i in range(N)]

# ---- margins per litre --------------------------------------------------------------
m = UB['margin_retail_h126']
mr = []
for g in V['gp_retfuel_per_l_g']:
    m *= (1 + g)
    mr.append(m)
F['margin_retail'] = mr
# FLAGGED GAP: the company discloses commercial VOLUME split corporate/aviation and
# commercial REVENUE split, but NOT the gross-profit split between them. So the margin per
# litre is carried at the level it is disclosed — blended across the two legs — and the
# FY2026 step in it is carried BOTH WAYS below rather than asserted once.
m = UB['margin_comm_h126']
mc = []
for g in V['gp_comm_per_l_g']:
    m *= (1 + g)
    mc.append(m)
F['margin_comm'] = mc

F['price_retail'] = V['price_retfuel']
F['price_corp'] = V['price_corp']
F['price_avi'] = V['price_avi']
F['rev_retfuel'] = [vol_r[i] * F['price_retail'][i] for i in range(N)]
F['rev_corp'] = [vol_co[i] * F['price_corp'][i] for i in range(N)]
F['rev_avi'] = [vol_av[i] * F['price_avi'][i] for i in range(N)]
F['rev_comm'] = [F['rev_corp'][i] + F['rev_avi'][i] for i in range(N)]
F['price_comm'] = [F['rev_comm'][i] / vol_c[i] for i in range(N)]   # an OUTPUT of the mix

# ---- non-fuel: transactions x basket ------------------------------------------------
ftxn, ntxn, bask, rn = [], [], [], []
_f, _cv, _b = V['fueltxn_h126'] * 2, UB['conversion_h126'], UB['basket_h126']
for i in range(N):
    _f *= (1 + V['fueltxn_g'][i])
    _cv *= (1 + V['conversion_g'][i])
    _b *= (1 + V['basket_g'][i])
    ftxn.append(_f)
    ntxn.append(_f * _cv)
    bask.append(_b)
    rn.append(_f * _cv * _b)
F['fuel_txn'] = ftxn
F['nonfuel_txn'] = ntxn
F['basket'] = bask
F['rev_nonfuel'] = rn
F['revenue'] = [F['rev_retfuel'][i] + F['rev_comm'][i] + rn[i] for i in range(N)]

F['gp_retfuel_struct'] = [vol_r[i] * mr[i] for i in range(N)]
F['gp_comm_struct'] = [vol_c[i] * mc[i] for i in range(N)]
F['gp_nonfuel'] = [rn[i] * V['gm_nonfuel'][i] for i in range(N)]
F['gp_struct'] = [F['gp_retfuel_struct'][i] + F['gp_comm_struct'][i] + F['gp_nonfuel'][i]
                  for i in range(N)]
F['invmove_A'] = V['invmove_A']
F['invmove_B'] = V['invmove_B']
F['gross_profit_A'] = [F['gp_struct'][i] + F['invmove_A'][i] for i in range(N)]
F['gross_profit_B'] = [F['gp_struct'][i] + F['invmove_B'][i] for i in range(N)]
F['direct_costs_A'] = [F['revenue'][i] - F['gross_profit_A'][i] for i in range(N)]
F['direct_costs_B'] = [F['revenue'][i] - F['gross_profit_B'][i] for i in range(N)]

co = []
c = H['FY2025']['cash_opex']
for g in V['cash_opex_g']:
    c *= (1 + g)
    co.append(c)
F['cash_opex'] = co
oi = []
o = V['oi_fy25']
for g in V['other_income_g']:
    o *= (1 + g)
    oi.append(o)
F['other_income'] = oi
F['impairments'] = V['impair_norm']

# ---- depreciation and capital spending, DERIVED from the asset base -----------------
# Both were hardcoded five-year arrays. Depreciation is now the opening fixed and
# right-of-use base times a rate measured off the audited history; capital spending is
# maintenance on that base plus the cost of the stations actually being added. The station
# unit cost is backed out of the company's own FY2026 capital-spending guidance, so the
# FY2026 total still reconciles to guidance while FY2027-30 follow the network plan.
_open = V['ppe_fy25'] + V['rou_fy25']
_prev_sta = V['stations_fy25']
dna, cpx = [], []
for i in range(N):
    _d = _open * V['dep_rate']
    _maint = _open * V['maint_capex_rate']
    _adds = sta[i] - _prev_sta
    _growth = _adds * V['capex_per_station']
    dna.append(_d)
    cpx.append(_maint + _growth)
    _open = _open + _maint + _growth - _d
    _prev_sta = sta[i]
F['dna'] = dna
F['capex'] = cpx
F['fixed_base'] = None   # rolled inside the balance sheet, not double-kept here

for fr, gpk in (('A', 'gross_profit_A'), ('B', 'gross_profit_B')):
    F[f'ebitda_{fr}'] = [F[gpk][i] - co[i] + oi[i] - F['impairments'][i] for i in range(N)]
    F[f'ebit_{fr}'] = [F[f'ebitda_{fr}'][i] - F['dna'][i] for i in range(N)]
    F[f'ebitda_margin_{fr}'] = [F[f'ebitda_{fr}'][i] / F['revenue'][i] for i in range(N)]
    F[f'gross_margin_{fr}'] = [F[gpk][i] / F['revenue'][i] for i in range(N)]

# ---- working capital, from the disclosed conversion cycle ----
_rev25, _dc25 = V['rev_fy25'], V['dc_fy25']
WC = dict(
    dso_trade=V['tr_fy25'] / _rev25 * 365,
    dso_all=(V['tr_fy25'] + V['dfrp_fy25']) / _rev25 * 365,
    dio=V['inv_fy25'] / _dc25 * 365,
    dpo_trade=V['tp_fy25'] / _dc25 * 365,
    dpo_all=(V['tp_fy25'] + V['dtrp_fy25']) / _dc25 * 365,
)
WC['ccc_trade'] = WC['dso_trade'] + WC['dio'] - WC['dpo_trade']
WC['ccc_all'] = WC['dso_all'] + WC['dio'] - WC['dpo_all']
WC['nwc_fy25'] = (V['tr_fy25'] + V['dfrp_fy25'] + V['inv_fy25']
                  - V['tp_fy25'] - V['dtrp_fy25'])

# ONE working-capital path, used by both frames. Inventory and payables are driven by
# the physical cost base, and an inventory movement is a margin effect rather than a
# change in the stock held or the amounts owed. Letting the frames diverge here would
# make the contested judgement leak into working capital, where it does not belong.
_nwc, _prev, _dnwc = [], WC['nwc_fy25'], []
for i in range(N):
    rec = WC['dso_all'] / 365 * F['revenue'][i]
    inv = WC['dio'] / 365 * F['direct_costs_A'][i]
    pay = WC['dpo_all'] / 365 * F['direct_costs_A'][i]
    cur = rec + inv - pay
    _nwc.append(cur)
    _dnwc.append(cur - _prev)
    _prev = cur
for fr in ('A', 'B'):
    F[f'nwc_{fr}'] = list(_nwc)
    F[f'delta_nwc_{fr}'] = list(_dnwc)

# ============================ COST OF CAPITAL ============================
W = {}
W['rf_observed'] = V['rf_observed']
W['sov_spread'] = V['sov_spread']
W['rf_star'] = V['rf_observed'] - V['sov_spread']
W['erp'] = V['erp_total']
W['erp_mature'] = V['erp_mature']
W['crp'] = V['crp']
W['beta'] = V['beta']
W['ke'] = W['rf_star'] + W['beta'] * W['erp']
# Kd is MARGINAL and term-matched: the sovereign yield at the forecast tenor plus the
# company's OWN disclosed credit margin. It must sit above the sovereign.
W['kd_pretax'] = V['rf_observed'] + V['credit_margin']
W['kd_pretax_usd_basis'] = V['rf_observed'] + V['credit_margin_usd']
W['kd_floating_basis'] = V['cb_base_rate'] + V['credit_margin']
W['tax_statutory'] = V['tax_statutory']
W['tax_effective'] = V['tax_effective']
W['tax_fcff'] = V['tax_effective']   # the audited, reconciled effective rate
W['tax_dmtt'] = V['tax_dmtt']
# the interest tax shield takes the MARGINAL statutory rate, the cash flows take the
# effective rate the group actually pays — these are different questions
W['kd_aftertax'] = W['kd_pretax'] * (1 - W['tax_statutory'])
W['mcap'] = V['spot'] * V['shares_mn']
W['net_debt'] = H['FY2025']['net_debt_company']
W['net_debt_incl_leases'] = H['FY2025']['net_debt_incl_leases']
W['we'] = W['mcap'] / (W['mcap'] + W['net_debt'])
W['wd'] = 1 - W['we']
W['wacc'] = W['we'] * W['ke'] + W['wd'] * W['kd_aftertax']
# Terminal beta DERIVED from the measured beta, not pasted beside it.
# D4, 09-Aug-2026 — FLAT COST OF CAPITAL. The sliding schedule is scoped by the standing
# protocol to markets in monetary transition and is explicitly excluded for currency-pegged
# markets, where the risk-free rate already sits at its long-run norm: "for GCC names the
# sliding schedule does nothing... today is the terminal, so explicit = terminal and the
# glide collapses to flat." Neither leg of the previous glide was supported anyway. The beta
# drift of 0.389 toward the market was an unanchored input, and the 10% terminal debt weight
# contradicted this model's own forecast balance sheet, which DE-gears net debt from 2,985 to
# 409 by FY2030. Both are retired to the sensitivity table as priced constructions.
W['beta_drift_frac'] = 0.0
W['beta_terminal'] = W['beta']
W['ke_terminal'] = W['rf_star'] + W['beta_terminal'] * W['erp']
W['wd_terminal'] = W['wd']   # flat structure: explicit = terminal
W['wacc_terminal'] = ((1 - W['wd_terminal']) * W['ke_terminal']
                      + W['wd_terminal'] * W['kd_aftertax'])
# the discount rate glides from the year-one rate to the terminal rate in equal steps,
# so the fade in the business is priced rather than switched on at the terminal line
W['glide_frac'] = [(i + 1) / N for i in range(N)]
W['disc_rate'] = [W['wacc'] + (W['wacc_terminal'] - W['wacc']) * W['glide_frac'][i]
                  for i in range(N)]
df_, acc = [], 1.0
for i in range(N):
    acc *= (1 + W['disc_rate'][i])
    df_.append(1 / acc)
W['df'] = df_
W['cb_base_rate'] = V['cb_base_rate']
W['credit_margin'] = V['credit_margin']

assert W['kd_pretax'] > V['rf_observed'], 'marginal cost of debt sits below the sovereign'
assert W['kd_pretax'] <= W['kd_pretax_usd_basis'] + 1e-12, 'cost-of-debt integrity triple broken'
assert W['ke'] > W['rf_star'], 'cost of equity below the normalised risk-free rate'
assert all(W['disc_rate'][i] <= W['disc_rate'][i + 1] + 1e-12 for i in range(N - 1)), \
    'discount-rate glide is not ordered'

# ============================ DCF, BOTH FRAMES ============================
def build_dcf(frame):
    ebit = F[f'ebit_{frame}']
    dnwc = F[f'delta_nwc_{frame}']
    nopat = [ebit[i] * (1 - W['tax_fcff']) for i in range(N)]
    fcff = [nopat[i] + F['dna'][i] - F['capex'][i] - dnwc[i] for i in range(N)]
    pv = [fcff[i] * W['df'][i] for i in range(N)]
    pv_sum = sum(pv)
    g = V['g_terminal']
    roic = V['roic_terminal']
    reinvest = g / roic
    nopat_term = nopat[-1] * (1 + g)
    fcff_term = nopat_term * (1 - reinvest)
    tv = fcff_term / (W['wacc_terminal'] - g)
    pv_tv = tv * W['df'][-1]
    ev = pv_sum + pv_tv
    nd = H['FY2025']['net_debt_company']
    lease = V['lease_fy25']
    nci_ = V['nciq_fy25']
    equity = ev - nd - lease - nci_
    per_share = equity / V['shares_mn']
    return dict(
        ebitda=F[f'ebitda_{frame}'], ebit=ebit, dna=F['dna'], nopat=nopat,
        capex=F['capex'], delta_nwc=dnwc, fcff=fcff, df=W['df'], pv=pv,
        pv_sum=pv_sum, g=g, roic_term=roic, reinvest_rate=reinvest,
        nopat_term=nopat_term, fcff_term=fcff_term, tv=tv, pv_tv=pv_tv,
        ev=ev, tv_share=pv_tv / ev,
        net_debt=nd, leases=lease, nci=nci_, equity=equity, per_share=per_share,
        tax_rate=W['tax_fcff'],
    )


DCF = dict(frame_A=build_dcf('A'), frame_B=build_dcf('B'))
for fr in ('frame_A', 'frame_B'):
    d = DCF[fr]
    assert abs((d['ev'] - d['net_debt'] - d['leases'] - d['nci']) - d['equity']) < 1e-6, \
        f'{fr}: the enterprise-to-equity bridge does not close'
    assert 0.0 < d['tv_share'] < 0.95, f'{fr}: terminal share of enterprise value out of range'
    assert abs(d['reinvest_rate'] - d['g'] / d['roic_term']) < 1e-12, \
        f'{fr}: terminal reinvestment is not consistent with growth over return'
    assert abs(d['pv_sum'] + d['pv_tv'] - d['ev']) < 1e-9, f'{fr}: enterprise value does not sum'

# ============================ THE OTHER LENSES ============================
L = {}
# 2. book value and sustainable return
bv_ps = V['eqp_fy25'] / V['shares_mn']
roe_hist = [H[y]['np_attributable'] / H[y]['equity_parent'] for y in HYRS]
roe_sust = sum(roe_hist) / 3
just_pb = (roe_sust - V['g_terminal']) / (W['ke'] - V['g_terminal'])
L['bv_ps'] = bv_ps
L['roe_sust'] = roe_sust
L['roe_hist'] = roe_hist
L['just_pb'] = just_pb
L['book_ps'] = bv_ps * just_pb

# 3. relative multiples — the company's own history, since a UAE fuel-retail
#    peer set trades on different fuel-pricing regimes
own_pe = [V['spot'] / H[y]['eps'] for y in HYRS]
L['own_pe_history'] = own_pe
L['own_pe_mean'] = sum(own_pe) / 3
L['pe_now'] = V['spot'] / H['FY2025']['eps']
# Forward earnings per share, built the way the income statement builds it: profit
# before tax is EBIT plus interest income less finance costs, taxed at the effective
# rate, then the non-controlling share removed.
def _eps_fwd(frame):
    pbt = F[f'ebit_{frame}'][0] + V['intinc_fy25'] - V['fin_fy25']
    return (pbt * (1 - W['tax_fcff']) - V['nci_fy25']) / V['shares_mn']


eps_fwd_A = _eps_fwd('A')
eps_fwd_B = _eps_fwd('B')
L['eps_fwd_A'] = eps_fwd_A
L['eps_fwd_B'] = eps_fwd_B
# The reference multiple is TRIANGULATED from three independent readings rather than
# asserted, and the average is taken explicitly so a reader can see what went into it:
#   1. what the company's own shares trade at today on the last audited year
#   2. what they have averaged against each of the three audited years
#   3. what the company's own economics justify, from the dividend relation
#      payout x (1 + growth) / (cost of equity - growth)
# A peer median is deliberately NOT one of the three: the peer set spans fuel-pricing
# regimes that are not the same instrument as an administered monthly price.
L['pe_method_today'] = L['pe_now']
L['pe_method_own_mean'] = L['own_pe_mean']
# The justified multiple must use the POLICY floor the company actually committed to — a
# minimum of 75% of net profit — not the 92% it happened to pay. The 92% is a realised ratio
# and was being presented as a policy term in two places.
# The justified multiple must satisfy the SUSTAINABLE-GROWTH IDENTITY g = retention x ROE,
# for the same reason the terminal block must satisfy g = ROIC x RR. Plugging either the
# realised 92% payout or the 75% policy floor into the Gordon formula breaks it: at a return
# on equity of 80.8%, a 75% payout implies 20% growth, not 1.5%. The retention consistent
# with 1.5% growth is g / ROE, so the payout the multiple must use is 1 - g / ROE. Deriving it
# this way also removes the free parameter the critiques were right to object to.
L['pe_retention_implied'] = V['g_terminal'] / L['roe_sust']
L['pe_payout_implied'] = 1 - L['pe_retention_implied']
L['pe_method_justified'] = (L['pe_payout_implied'] * (1 + V['g_terminal'])
                            / (W['ke'] - V['g_terminal']))
# CHANGED 09-Aug-2026 after four independent audits made the same finding. The reference
# multiple was the average of three legs, two of which were THE TRADED PRICE divided by
# earnings — so a lens presented as independent evidence about value was two-thirds a
# restatement of the price it was being compared against. The traded multiples are retained
# and PUBLISHED as context, but the reference is now the fundamentals-derived leg alone.
L['pe_methods'] = [L['pe_method_today'], L['pe_method_own_mean'], L['pe_method_justified']]
L['pe_context'] = [L['pe_method_today'], L['pe_method_own_mean']]
L['just_fwd_pe'] = L['pe_method_justified']
L['rel_A'] = eps_fwd_A * L['just_fwd_pe']
L['rel_B'] = eps_fwd_B * L['just_fwd_pe']

# 4. normalised earnings power — structural gross profit only, no inventory movement
norm_ebitda = F['gp_struct'][0] - F['cash_opex'][0] + F['other_income'][0] - F['impairments'][0]
norm_ebit = norm_ebitda - F['dna'][0]
norm_nopat = norm_ebit * (1 - W['tax_fcff'])
L['norm_ebitda'] = norm_ebitda
L['norm_ebit'] = norm_ebit
L['norm_nopat'] = norm_nopat
# D2, 09-Aug-2026 — the terminal-reinvestment identity g = ROIC x RR governs EVERY
# perpetuity, not only the cash-flow model's terminal block. This lens previously capitalised
# a growing perpetuity with NO reinvestment charge — growth for free — which is precisely the
# defect that identity rule was adopted to prevent, and it was described three times as a
# zero-growth reading. Reinvestment is now forced to g / ROIC, the same charge the DCF makes
# for the same growth.
L['norm_reinvest'] = V['g_terminal'] / V['roic_terminal']
L['norm_ev'] = (norm_nopat * (1 - L['norm_reinvest'])
                / (W['wacc'] - V['g_terminal']))
L['norm_equity'] = (L['norm_ev'] - H['FY2025']['net_debt_company']
                    - V['lease_fy25'] - V['nciq_fy25'])
L['norm_ps'] = L['norm_equity'] / V['shares_mn']

# 5. dividend capitalisation — the shareholder's actual cash claim
L['dps'] = V['dps']
L['div_yield_now'] = V['dps'] / V['spot']
# The dividend is a FIXED policy commitment held flat from 2024 through 2030. Capitalising it
# as a growing perpetuity credited growth the policy explicitly does not promise. It is now
# valued as the flat commitment it is.
L['div_ps'] = V['dps'] / W['ke']
L['div_ps_grown'] = V['dps'] * (1 + V['g_terminal']) / (W['ke'] - V['g_terminal'])

# The four lenses of the study's own structure, in its order: the cash-flow model,
# book value and sustainable return, relative multiples, normalised earnings power.
# Dividend capitalisation is carried as an unweighted fifth reading because a fixed
# policy dividend answers a different question from the cash the business generates.
L['items_A'] = [
    dict(name='Discounted cash flow', value=DCF['frame_A']['per_share'], weight=0.40),
    dict(name='Normalised earnings power', value=L['norm_ps'], weight=0.25),
]
L['items_B'] = [
    dict(name='Discounted cash flow', value=DCF['frame_B']['per_share'], weight=0.40),
    dict(name='Normalised earnings power', value=L['norm_ps'], weight=0.25),
]
L['shared'] = [
    dict(name='Relative multiples', value=L['rel_A'], weight=0.20),
    dict(name='Book value and sustainable return', value=L['book_ps'], weight=0.15),
]
L['unweighted'] = [
    dict(name='Dividend capitalisation', value=L['div_ps'], weight=0.0),
]
L['centre_A'] = (sum(i['value'] * i['weight'] for i in L['items_A'])
                 + sum(i['value'] * i['weight'] for i in L['shared']))
_relB = dict(L['shared'][0]); _relB['value'] = L['rel_B']
L['shared_B'] = [_relB, L['shared'][1]]
L['centre_B'] = (sum(i['value'] * i['weight'] for i in L['items_B'])
                 + sum(i['value'] * i['weight'] for i in L['shared_B']))
_wt = sum(i['weight'] for i in L['items_A']) + sum(i['weight'] for i in L['shared'])
assert abs(_wt - 1.0) < 1e-12, 'the lens weights do not sum to one'
# CHANGED 09-Aug-2026. The published field was the two weighted centres times 0.85 and 1.15
# — an undisclosed +/-15% band presented as the spread of the methods, which it was not: it
# NARROWED the actual spread at both ends while the caption said it widened it, and the
# dividend reading fell outside the range it was said to lie within. The field is now the
# ACTUAL minimum and maximum of the readings, so "the spread between them IS the uncertainty"
# is true as written.
_readings = [DCF['frame_A']['per_share'], DCF['frame_B']['per_share'], L['norm_ps'],
             L['rel_A'], L['rel_B'], L['book_ps'], L['div_ps']]
L['readings_all'] = _readings
L['fair_bear'] = min(_readings)
L['fair_bull'] = max(_readings)
L['book_lens'] = L['book_ps']

# ============================ SENSITIVITY ============================
def revalue(wacc_t=None, g=None, beta=None, inv=None, volg=None, marg=None,
            tax=None, capexd=None, frame='A'):
    b = beta if beta is not None else W['beta']
    ke = W['rf_star'] + b * W['erp']
    w0 = W['we'] * ke + W['wd'] * W['kd_aftertax']
    # The terminal beta follows the SAME rule the model itself uses, not a fixed additive
    # shift. Under a flat pegged-market cost of capital that rule is the identity, so the
    # beta ladder now reproduces the model at every point instead of only at the base case.
    ket = W['rf_star'] + (b + W['beta_drift_frac'] * (1 - b)) * W['erp']
    wt = wacc_t if wacc_t is not None else (
        (1 - W['wd_terminal']) * ket + W['wd_terminal'] * W['kd_aftertax'])
    gg = g if g is not None else V['g_terminal']
    rates = [w0 + (wt - w0) * ((i + 1) / N) for i in range(N)]
    dfs, acc = [], 1.0
    for i in range(N):
        acc *= (1 + rates[i])
        dfs.append(1 / acc)
    # Volume sensitivity moves EVERY leg, which is what the text says it does. The previous
    # version moved retail only while the study described it as the whole volume path.
    vr, vc_ = F['vol_retail'], F['vol_comm']
    if volg is not None:
        vr, s0, l0 = [], V['stations_fy25'], UB['litres_per_station_fy25']
        for i in range(N):
            s0 *= (1 + V['stations_g'][i])
            l0 *= (1 + V['litres_per_station_g'][i] + volg)
            vr.append(s0 * l0)
        vc_, c0, a0 = [], UB['vol_corp_fy25'], UB['vol_avi_fy25']
        for i in range(N):
            c0 *= (1 + V['vol_corp_g'][i] + volg)
            a0 *= (1 + V['vol_avi_g'][i] + volg)
            vc_.append(c0 + a0)
    mr = F['margin_retail'] if marg is None else [m * (1 + marg) for m in F['margin_retail']]
    mc_ = F['margin_comm'] if marg is None else [m * (1 + marg) for m in F['margin_comm']]
    gps = [vr[i] * mr[i] + vc_[i] * mc_[i] + F['gp_nonfuel'][i] for i in range(N)]
    im = F[f'invmove_{frame}'] if inv is None else inv
    gpt = [gps[i] + im[i] for i in range(N)]
    ebitda = [gpt[i] - F['cash_opex'][i] + F['other_income'][i] - F['impairments'][i]
              for i in range(N)]
    ebit = [ebitda[i] - F['dna'][i] for i in range(N)]
    tr = tax if tax is not None else W['tax_fcff']
    nopat = [e * (1 - tr) for e in ebit]
    cx = F['capex'] if capexd is None else [c * (1 + capexd) for c in F['capex']]
    fcff = [nopat[i] + F['dna'][i] - cx[i] - F[f'delta_nwc_{frame}'][i] for i in range(N)]
    pvs = sum(fcff[i] * dfs[i] for i in range(N))
    reinv = gg / V['roic_terminal']
    tv = nopat[-1] * (1 + gg) * (1 - reinv) / (wt - gg)
    ev = pvs + tv * dfs[-1]
    eq = ev - H['FY2025']['net_debt_company'] - V['lease_fy25'] - V['nciq_fy25']
    return eq / V['shares_mn']


SENS = {}
SENS['wacc'] = [[r, revalue(wacc_t=r)] for r in
                [W['wacc_terminal'] + d for d in (-0.010, -0.005, 0.0, 0.005, 0.010)]]
SENS['g'] = [[gg, revalue(g=gg)] for gg in (0.005, 0.010, 0.015, 0.020, 0.025)]
SENS['beta'] = [[b, revalue(beta=b)] for b in (0.45, 0.55, 0.6494, 0.80, 1.00)]
SENS['volume'] = [[d, revalue(volg=d)] for d in (-0.010, -0.005, 0.0, 0.005, 0.010)]
SENS['margin'] = [[d, revalue(marg=d)] for d in (-0.10, -0.05, 0.0, 0.05, 0.10)]
SENS['inventory'] = [[lvl, revalue(inv=[F['invmove_A'][0]] + [lvl] * 4)]
                     for lvl in (0.0, 150.0, 295.0, 450.0, 600.0)]
SENS['tax'] = [[t, revalue(tax=t)] for t in (0.090, 0.1017, 0.120, 0.150, 0.180)]
SENS['capex'] = [[d, revalue(capexd=d)] for d in (-0.20, -0.10, 0.0, 0.10, 0.20)]
SENS['tax_dmtt_impact'] = revalue(tax=V['tax_dmtt']) - revalue(tax=V['tax_effective'])
SENS['grid_wacc'] = [W['wacc_terminal'] + d for d in (-0.010, -0.005, 0.0, 0.005, 0.010)]
SENS['grid_g'] = [0.005, 0.010, 0.015, 0.020, 0.025]
SENS['grid'] = [[revalue(wacc_t=w, g=gg) for gg in SENS['grid_g']] for w in SENS['grid_wacc']]
SENS['grid_lo'] = min(min(r) for r in SENS['grid'])
SENS['grid_hi'] = max(max(r) for r in SENS['grid'])

# ---- the crux: what does the market's price imply about the long run? ----
# Solving for the inventory contribution that reconciles the model to the market
# runs off the bottom of its range: even with inventory movements set to zero for
# every forecast year, the discounted cash flow sits above the traded price. The
# disagreement is therefore not about the windfall at all — it is about the long
# run, where 76% of the enterprise value sits. So the crux is solved as a reverse
# valuation on terminal growth, the variable an electric-vehicle transition
# actually threatens.
def _solve(fn, lo, hi, target):
    for _ in range(200):
        mid = (lo + hi) / 2
        if fn(mid) < target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


_g_implied = _solve(lambda g: revalue(g=g), -0.08, 0.030, V['spot'])
_wt_implied = _solve(lambda w: revalue(wacc_t=-w), -0.16, -0.045, V['spot'])
_wt_implied = -_wt_implied
_beta_implied = _solve(lambda b: revalue(beta=-b), -3.0, -0.2, V['spot'])
_beta_implied = -_beta_implied
CRUX = dict(
    spot=V['spot'],
    normalised_value=DCF['frame_A']['per_share'],
    throughcycle_value=DCF['frame_B']['per_share'],
    g_base=V['g_terminal'],
    g_implied=_g_implied,
    wacc_term_base=W['wacc_terminal'],
    wacc_term_implied=_wt_implied,
    beta_base=W['beta'],
    beta_implied=_beta_implied,
    tv_share=DCF['frame_A']['tv_share'],
    fy25_actual=V['invgain_fy25'],
    fy24_actual=V['invgain_fy24'],
    h126_actual=V['invgain_h126'],
    avg_24_25=(V['invgain_fy24'] + V['invgain_fy25']) / 2,
    inventory_floor_value=revalue(inv=[F['invmove_A'][0]] + [0.0] * 4),
    inventory_zero_all_years=revalue(inv=[0.0] * 5),
)
CRUX['ramp'] = [[gg, revalue(g=gg)] for gg in
                (-0.020, -0.010, 0.000, 0.010, V['g_terminal'])]
CRUX['inv_ramp'] = [[lvl, revalue(inv=[F['invmove_A'][0]] + [lvl] * 4)]
                    for lvl in (0.0, 150.0, 295.0, 500.0, 762.0)]

# ---- cost exposure: one escalator per driver class ----
CE = dict(
    commodity_share=(F['revenue'][0] - F['gp_struct'][0]) / F['revenue'][0],
    domestic_opex_share=F['cash_opex'][0] / F['revenue'][0],
    commodity_escalator='own crude-linked realised-price path',
    domestic_escalator='domestic inflation, about 2% a year',
    note=('The fuel itself is a globally-traded input and is escalated on its own '
          'crude-linked price path through the realised price per litre, never on a '
          'domestic inflation index. Staff, utilities, repairs and marketing are domestic '
          'service costs and take the domestic escalator. The regulated margin per litre '
          'is a domestic administered price and takes the domestic escalator as well.'),
)

# ==================== [R-ANCHOR-01] THE FORECAST ANCHOR ====================
# THE RECORD IS PRINTED WHETHER OR NOT IT FIRES, and this one fires. What it says about
# this study is that the forecast opens BELOW the period the company has just filed, and
# that the whole of the shortfall is ONE DISCLOSED ITEM which the company itself removes
# from its own run rate.
#
# THE LATEST REVIEWED PERIOD IS THE SIX MONTHS TO 30 JUNE 2026, not FY2025. The build is
# already anchored there — every volume, price and margin-per-litre leg starts from the
# annualised disclosed first half — which is what this rule asks for and what the
# FORECAST section above already does.
#
# WHICH RATE, AND THE CHOICE IS RECORDED RATHER THAN MADE QUIETLY. The company publishes
# an EBITDA margin as its own KPI at the half year and the full year; this study's
# reference pattern is the operating-company one, whose anchor record is the EBITDA
# margin; and the study's central contested judgement — whether the inventory movement is
# a windfall or a through-cycle feature — lands in gross profit and reaches value through
# EBITDA. THE GROSS MARGIN IS RECORDED BESIDE IT rather than instead of it, because on
# the gross margin this same forecast does NOT fire, and picking the rate that clears the
# check would be the move-the-number-to-satisfy-the-check offence in another costume.
#
# WHICH FRAME. Frame A — the branch that declines and therefore owes a mechanism. Frame B
# is recorded in other_framing rather than left out, because the two frames are the
# study's published contested judgement and neither is the answer on its own.
#
# EBITDA is the two filed lines, operating profit plus the depreciation and amortisation
# line of the distribution-and-administrative-expenses note. The company publishes the
# same figure as its own EBITDA KPI in the management discussion and analysis of the same
# date, so this is a disclosed rate rather than one constructed here.
_eb_h126 = V['op_h126'] + V['dna_h126']
# H1 2025 revenue is the four disclosed segment comparatives in the revenue note of that
# same reviewed interim, which are the components of its filed comparative total.
_rev_h125 = (V['rev_retfuel_h125'] + V['rev_nonfuel_h125']
             + V['rev_corp_h125'] + V['rev_avi_h125'])
_vol_h125 = V['vol_retail_h125'] + V['vol_comm_h125']
_vol_h126 = V['vol_retail_h126'] + V['vol_comm_h126']
# THE LIKE-FOR-LIKE MEASUREMENT IS THE CLAUSE THAT DOES THE WORK, and it is normalised by
# LITRES rather than by revenue on purpose: this company's revenue is a crude pass-through
# — the same reason the unit build separates realised price from margin per litre — so a
# share of revenue moves with the oil price whether or not anything about the company has
# changed. Both halves, both volumes and both inventory figures are disclosed.
_invgain_per_l_h125 = V['invgain_h125'] / _vol_h125
_invgain_per_l_h126 = V['invgain_h126'] / _vol_h126

FORECAST_ANCHOR = dict(
    rate_name='EBITDA margin, frame A (inventory movements normalised)',
    latest_reviewed_period='H1 2026, reviewed (six months ended 30 June 2026)',
    latest_reviewed_date='2026-06-30',
    latest_reviewed_rate=float(_eb_h126 / V['rev_h126']),
    latest_reviewed_source=(
        'Abu Dhabi National Oil Company for Distribution PJSC, reviewed interim condensed '
        'consolidated financial statements for the six months ended 30 June 2026: '
        'operating profit of AED %s million plus the depreciation and amortisation line of '
        'the distribution and administrative expenses note of AED %s million, over revenue '
        'of AED %s million. The company publishes the same EBITDA figure as its own KPI in '
        'the management discussion and analysis of 5 August 2026.'
        % (f"{V['op_h126']:,.0f}", f"{V['dna_h126']:,.0f}", f"{V['rev_h126']:,.0f}")),
    first_forecast_rate=float(F['ebitda_margin_A'][0]),
    # [R-ANCHOR-01] CLAUSE TWO — the whole explicit window, not only the opening year.
    forecast_path=[float(x) for x in F['ebitda_margin_A']],
    mechanism=dict(
        name='one_off_in_the_latest_period',
        disclosure=(
            'The management discussion and analysis for the second quarter and first half '
            'of 2026, published 5 August 2026, states inventory gains of AED %s million in '
            'H1 2026 against AED %s million in H1 2025, splits them by segment (AED %s '
            'million fuel retail and AED %s million commercial, against AED %s million and '
            'a loss of AED %s million a year earlier), and attributes the rise in half-year '
            'EBITDA to them. THE COMPANY ITSELF REMOVES THIS ITEM FROM ITS OWN RUN RATE: '
            'the same document defines underlying EBITDA as EBITDA excluding inventory '
            'movements and one-off items. The full-year figures on the same disclosure are '
            'AED %s million in FY2024 and AED %s million in FY2025, so a single half has '
            'just carried more than the two preceding years together. Frame A holds the '
            'realised first half and assumes nothing for the second half or beyond; frame B '
            'carries the through-cycle rate instead, and both are published.'
            % (f"{V['invgain_h126']:,.0f}", f"{V['invgain_h125']:,.0f}",
               f"{V['invgain_retfuel_h126']:,.0f}", f"{V['invgain_comm_h126']:,.0f}",
               f"{V['invgain_retfuel_h125']:,.0f}", f"{abs(V['invgain_comm_h125']):,.0f}",
               f"{V['invgain_fy24']:,.0f}", f"{V['invgain_fy25']:,.0f}")),
        like_for_like=dict(
            measures='inventory gains disclosed for the six months to 30 June, per litre of '
                     'fuel sold',
            period_a='H1 2025',
            period_b='H1 2026',
            value_a=float(_invgain_per_l_h125),
            value_b=float(_invgain_per_l_h126),
            higher_is_worse=True,
            note=(
                'THE DIRECTION: the larger the non-recurring gain sitting inside the latest '
                'reviewed period, the further a forecast that does not repeat it must open '
                'below that period. Measured in the same six months a year apart, on the '
                "company's own disclosed volumes, it went from AED %s to AED %s per litre — "
                '%.1f times larger — while the STRUCTURAL margins the forecast is actually '
                'built on moved the other way: retail fuel gross profit per litre excluding '
                'inventory movements rose %.1f%% year on year in the same pair and '
                'commercial rose %.1f%%. The mechanism and the filings agree, and they agree '
                'about a windfall rather than about the business.'
                % (f"{_invgain_per_l_h125:.4f}", f"{_invgain_per_l_h126:.4f}",
                   _invgain_per_l_h126 / _invgain_per_l_h125,
                   100 * UB['margin_retail_growth_h1'],
                   100 * UB['margin_comm_growth_h1'])),
        ),
    ),
    other_framing=dict(
        label='Frame B — inventory movements carried at the through-cycle rate',
        first_forecast_rate=float(F['ebitda_margin_B'][0]),
        forecast_path=[float(x) for x in F['ebitda_margin_B']],
        note=('Frame B opens %.2f%% relatively below the reviewed half against frame A\'s '
              '%.2f%%, and falls %.2f%% from its own opening year against frame A\'s %.2f%%. '
              'Neither clause of this rule would fire on it. The two frames are the study\'s '
              'central contested judgement and are published side by side, never averaged, '
              'so the anchor is recorded on the branch that makes the larger claim.'
              % (100 * abs(F['ebitda_margin_B'][0] / (_eb_h126 / V['rev_h126']) - 1),
                 100 * abs(F['ebitda_margin_A'][0] / (_eb_h126 / V['rev_h126']) - 1),
                 100 * abs(min(F['ebitda_margin_B']) / F['ebitda_margin_B'][0] - 1),
                 100 * abs(min(F['ebitda_margin_A']) / F['ebitda_margin_A'][0] - 1))),
    ),
    gross_margin_beside_it=dict(
        latest_reviewed_rate=float(V['gp_h126'] / V['rev_h126']),
        first_forecast_rate=float(F['gross_margin_A'][0]),
        forecast_path=[float(x) for x in F['gross_margin_A']],
        note=('Recorded because the choice of rate decides whether this record fires and '
              'the choice should be visible. On the gross margin frame A opens %.2f%% '
              'relatively below the reviewed half and falls %.2f%% from its own opening '
              'year, both inside the tolerance; on the EBITDA margin it opens %.2f%% below '
              'and falls %.2f%%. The difference is cash operating cost, which the forecast '
              'grows off FY2025 rather than off the realised half. The EBITDA margin is '
              'recorded as the governing rate because it is the one the company publishes '
              'as its own KPI, the one this study\'s reference pattern anchors on, and the '
              'one the contested judgement reaches value through.'
              % (100 * abs(F['gross_margin_A'][0] / (V['gp_h126'] / V['rev_h126']) - 1),
                 100 * abs(min(F['gross_margin_A']) / F['gross_margin_A'][0] - 1),
                 100 * abs(F['ebitda_margin_A'][0] / (_eb_h126 / V['rev_h126']) - 1),
                 100 * abs(min(F['ebitda_margin_A']) / F['ebitda_margin_A'][0] - 1))),
    ),
    note=(
        'THE FORECAST OPENS BELOW THE REVIEWED HALF AND THE WHOLE OF THE GAP IS THE '
        'INVENTORY MOVEMENT. The reviewed six months to 30 June 2026 carried an EBITDA '
        'margin of %.2f%%; frame A opens FY2026 at %.2f%%, %.2f%% relatively below it, and '
        'reaches its low of %.2f%% in FY2027 when the realised first-half gain stops being '
        'carried at all. THE UNIT RATES THE FORECAST IS ACTUALLY BUILT ON BOTH OPEN ABOVE '
        'THE REVIEWED HALF, which is the other half of this record and is printed because a '
        'gate that only catches declines would say nothing about it: structural retail fuel '
        'margin per litre opens %.1f%% above the realised half and structural commercial '
        'margin per litre %.1f%% above it, the second of those being an escalator the '
        'study sources to the disclosed first half, in which that same structural margin '
        'per litre rose %.1f%% year on year. So this is '
        'not a real cost drift and not a price step-down — the operating rate the business '
        'earns per litre is forecast to rise, and what falls out is a windfall the company '
        'itself excludes from underlying EBITDA. Frame B, which carries that windfall at '
        'the through-cycle rate instead of at zero, does not fire on either clause.'
        % (100 * _eb_h126 / V['rev_h126'], 100 * F['ebitda_margin_A'][0],
           100 * abs(F['ebitda_margin_A'][0] / (_eb_h126 / V['rev_h126']) - 1),
           100 * min(F['ebitda_margin_A']),
           100 * (F['margin_retail'][0] / UB['margin_retail_h126'] - 1),
           100 * (F['margin_comm'][0] / UB['margin_comm_h126'] - 1),
           100 * UB['margin_comm_growth_h1'])),
)


# ============================ OUTPUT ============================
def _load(name):
    p = os.path.join(HERE, name)
    return json.load(open(p)) if os.path.exists(p) else None


CAL = dict(step0=_load('step0_result.json'), backtest=_load('backtest_5y.json'),
           vol=_load('vol_diagnostic.json'), width=_load('width_diagnostic.json'))

OUT = dict(
    # THE ANSWER, WHERE THE SHARED READER LOOKS FOR IT. [R-GAP-01]'s gate reads a
    # study's own numbers for an answer and the spot it was struck at. This study
    # publishes TWO weighted centres and no single figure — deliberately, because the
    # contested judgement is carried both ways and the two are never averaged — and it
    # carried them at lenses.centre_A and lenses.centre_B, where the shared reader does
    # not look. So the gate could see nothing and this study sat on the unreadable
    # list. AN UNREADABLE STUDY IS NOT A CLEAN STUDY [R-ENF-04], and a TWO-SIDED answer
    # is READABLE rather than missing: read_branches() exists for exactly this shape.
    #
    # Nothing here is a new answer and nothing here endorses the weighted blend that
    # produces each centre — [R-LENS-03] retires that construction and this study stays
    # on the lens ratchet until it is rebuilt. What the gate audits is the answer a
    # reader actually receives, and this is that answer, in the listing currency the
    # price library carries.
    spot=V['spot'],
    central_two_sided=dict(
        question='Do inventory movements normalise to zero, or persist at the '
                 'through-cycle rate the company has actually reported?',
        decides='Whether the gross profit that compounds into the perpetuity carries '
                'the inventory contribution at all. The difference is overwhelmingly a '
                'TERMINAL effect, which is precisely why the two frames are published '
                'side by side and never averaged.',
        branches=[
            dict(label='Frame A — inventory movements normalised to zero from FY2027',
                 value=L['centre_A'],
                 condition='Inventory movements are a windfall of a rising oil price '
                           'and revert to nothing once prices stop rising. They were '
                           'AED 254 million in FY2024, AED 335 million in FY2025 and '
                           'AED 762 million in the first half of 2026 alone, against '
                           'fuel volume growth in that half of 1.6%.'),
            dict(label='Frame B — inventory movements carried at the FY2024-FY2025 '
                       'average of AED 294 million',
                 value=L['centre_B'],
                 condition='Inventory movements are a through-cycle feature of holding '
                           'fuel stock rather than a windfall, and the two-year average '
                           'is the company\'s own recent experience of them.'),
        ],
        why_not_averaged='A number between the two describes a world in which the '
                         'inventory contribution is half real. The dual-framing rule '
                         'forbids averaging such a pair, and this study takes the '
                         'further step of printing no average at all.',
    ),
    meta=dict(
        company='Abu Dhabi National Oil Company for Distribution PJSC',
        short='ADNOC Distribution', ticker='ADNOCDIST', market='AE',
        exchange='Abu Dhabi Securities Exchange', currency='AED',
        sector='Fuel retail, convenience retail and commercial fuel distribution',
        company_class='operating company',
        reference_pattern='operating company',
        study_date='2026-08-09', price_date='2026-08-07',
        fy_end='31 December', audited_years=HYRS, forecast_years=YRS,
        spot=V['spot'], shares_mn=V['shares_mn'], mcap=W['mcap'],
        listing_date='2017-12-13',
    ),
    inputs=INP, history=H, unit_build=UB, forecast=F, wacc=W, dcf=DCF, lenses=L,
    sensitivity=SENS, crux=CRUX, cost_exposure=CE, working_capital=WC, calibration=CAL,
    forecast_anchor=FORECAST_ANCHOR,
)

with open(os.path.join(HERE, 'study_numbers.json'), 'w') as f:
    json.dump(OUT, f, indent=1, default=float)

print(f"inputs {len(INP)} records, four-field complete")
print(f"FY2025 revenue {V['rev_fy25']:,.0f}  EBITDA {H['FY2025']['ebitda']:,.1f}  "
      f"net profit {V['np_fy25']:,.1f}")
print(f"WACC year one {W['wacc']*100:.2f}%  terminal {W['wacc_terminal']*100:.2f}%  "
      f"Ke {W['ke']*100:.2f}%  Kd after tax {W['kd_aftertax']*100:.2f}%")
for fr in ('frame_A', 'frame_B'):
    d = DCF[fr]
    print(f"{fr}: EV {d['ev']:,.0f}  terminal share {d['tv_share']*100:.1f}%  "
          f"equity {d['equity']:,.0f}  per share {d['per_share']:.2f}")
print(f"centre A {L['centre_A']:.2f}  centre B {L['centre_B']:.2f}  spot {V['spot']:.2f}")
print(f"crux (reverse valuation): the traded price implies terminal growth of "
      f"{CRUX['g_implied']*100:+.2f}% against the model's {V['g_terminal']*100:.2f}%, "
      f"or a terminal discount rate of {CRUX['wacc_term_implied']*100:.2f}% "
      f"against {W['wacc_terminal']*100:.2f}%, or a beta of "
      f"{CRUX['beta_implied']:.2f} against the measured {W['beta']:.2f}")
print(f"  with inventory movements set to zero in EVERY forecast year the model still "
      f"gives AED {CRUX['inventory_zero_all_years']:.2f} against a price of {V['spot']:.2f}")
print(f"  terminal value is {DCF['frame_A']['tv_share']*100:.1f}% of enterprise value")
print('wrote study_numbers.json')
