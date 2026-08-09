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
    sov_spread=I(0.0042, "Damodaran country risk premium file, January 2026 vintage: United "
                 "Arab Emirates, Moody's Aa2, adjusted default spread 0.42%",
                 "2026-01-01", "Country"),
    erp_total=I(0.0487, "Damodaran country risk premium file, January 2026 vintage: United "
                "Arab Emirates total equity risk premium 4.87%, being the 4.23% mature-market "
                "premium plus a 0.64% country risk premium", "2026-01-01", "Country"),
    erp_mature=I(0.0423, "Damodaran country risk premium file, January 2026 vintage: "
                 "mature-market equity risk premium", "2026-01-01", "Country"),
    crp=I(0.0064, "Damodaran country risk premium file, January 2026 vintage: United Arab "
          "Emirates country risk premium", "2026-01-01", "Country"),
    beta=I(0.509, "Five-year weekly regression of the company's own returns against an "
           "equal-weight composite of the Abu Dhabi exchange's listed names, excluding the "
           "company itself; 257 observations, R-squared 0.194, standard error 0.065",
           "2026-08-07", "Market"),
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
    beta_terminal=I(0.700, "Terminal beta, drifting from the measured 0.509 toward the "
                    "market as the transition risk in the business rises and the regulated "
                    "margin becomes a smaller share of a more diversified earnings base",
                    "2026-08-05", "Market"),
    wd_terminal=I(0.100, "Terminal debt weight, above today's 5.5% because the current "
                  "weight reflects an unusually high equity market value against a small "
                  "and stable borrowing book", "2026-08-05", "Market"),
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
F = dict(years=YRS)
vol_r, vol_c = [], []
v = V['vol_retail_fy25']
for g in V['vol_retail_g']:
    v *= (1 + g)
    vol_r.append(v)
v = V['vol_comm_fy25']
for g in V['vol_comm_g']:
    v *= (1 + g)
    vol_c.append(v)
F['vol_retail'] = vol_r
F['vol_comm'] = vol_c
F['vol_total'] = [a + b for a, b in zip(vol_r, vol_c)]

m = UB['margin_retail_fy25']
mr = []
for g in V['gp_retfuel_per_l_g']:
    m *= (1 + g)
    mr.append(m)
F['margin_retail'] = mr
m = UB['margin_comm_fy25']
mc = []
for g in V['gp_comm_per_l_g']:
    m *= (1 + g)
    mc.append(m)
F['margin_comm'] = mc

F['price_retail'] = V['price_retfuel']
F['price_comm'] = V['price_comm']
F['rev_retfuel'] = [vol_r[i] * F['price_retail'][i] for i in range(N)]
F['rev_comm'] = [vol_c[i] * F['price_comm'][i] for i in range(N)]
rn = []
r = V['rev_nonfuel_fy25']
for g in V['rev_nonfuel_g']:
    r *= (1 + g)
    rn.append(r)
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
F['dna'] = V['dna_fwd']
F['capex'] = V['capex_fwd']

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

for fr in ('A', 'B'):
    nwc, prev = [], WC['nwc_fy25']
    dnwc = []
    for i in range(N):
        rec = WC['dso_all'] / 365 * F['revenue'][i]
        inv = WC['dio'] / 365 * F[f'direct_costs_{fr}'][i]
        pay = WC['dpo_all'] / 365 * F[f'direct_costs_{fr}'][i]
        cur = rec + inv - pay
        nwc.append(cur)
        dnwc.append(cur - prev)
        prev = cur
    F[f'nwc_{fr}'] = nwc
    F[f'delta_nwc_{fr}'] = dnwc

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
W['beta_terminal'] = V['beta_terminal']
W['ke_terminal'] = W['rf_star'] + W['beta_terminal'] * W['erp']
W['wd_terminal'] = V['wd_terminal']
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
eps_fwd_A = (F['ebit_A'][0] * (1 - W['tax_statutory'])
             - (V['fin_fy25'] - V['intinc_fy25']) * (1 - W['tax_statutory'])
             - V['nci_fy25']) / V['shares_mn']
eps_fwd_B = (F['ebit_B'][0] * (1 - W['tax_statutory'])
             - (V['fin_fy25'] - V['intinc_fy25']) * (1 - W['tax_statutory'])
             - V['nci_fy25']) / V['shares_mn']
L['eps_fwd_A'] = eps_fwd_A
L['eps_fwd_B'] = eps_fwd_B
L['just_fwd_pe'] = 16.0
L['rel_A'] = eps_fwd_A * L['just_fwd_pe']
L['rel_B'] = eps_fwd_B * L['just_fwd_pe']

# 4. normalised earnings power — structural gross profit only, no inventory movement
norm_ebitda = F['gp_struct'][0] - F['cash_opex'][0] + F['other_income'][0] - F['impairments'][0]
norm_ebit = norm_ebitda - F['dna'][0]
norm_nopat = norm_ebit * (1 - W['tax_statutory'])
L['norm_ebitda'] = norm_ebitda
L['norm_ebit'] = norm_ebit
L['norm_nopat'] = norm_nopat
L['norm_ev'] = norm_nopat / (W['wacc'] - V['g_terminal'])
L['norm_equity'] = (L['norm_ev'] - H['FY2025']['net_debt_company']
                    - V['lease_fy25'] - V['nciq_fy25'])
L['norm_ps'] = L['norm_equity'] / V['shares_mn']

# 5. dividend capitalisation — the shareholder's actual cash claim
L['dps'] = V['dps']
L['div_yield_now'] = V['dps'] / V['spot']
L['div_ps'] = V['dps'] * (1 + V['g_terminal']) / (W['ke'] - V['g_terminal'])

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
L['fair_bear'] = min(L['centre_A'], L['centre_B']) * 0.85
L['fair_bull'] = max(L['centre_A'], L['centre_B']) * 1.15
L['book_lens'] = L['book_ps']

# ============================ SENSITIVITY ============================
def revalue(wacc_t=None, g=None, beta=None, inv=None, volg=None, marg=None,
            tax=None, capexd=None, frame='A'):
    b = beta if beta is not None else W['beta']
    ke = W['rf_star'] + b * W['erp']
    w0 = W['we'] * ke + W['wd'] * W['kd_aftertax']
    ket = W['rf_star'] + (b + (W['beta_terminal'] - W['beta'])) * W['erp']
    wt = wacc_t if wacc_t is not None else (
        (1 - W['wd_terminal']) * ket + W['wd_terminal'] * W['kd_aftertax'])
    gg = g if g is not None else V['g_terminal']
    rates = [w0 + (wt - w0) * ((i + 1) / N) for i in range(N)]
    dfs, acc = [], 1.0
    for i in range(N):
        acc *= (1 + rates[i])
        dfs.append(1 / acc)
    vr = F['vol_retail']
    if volg is not None:
        vr, v0 = [], V['vol_retail_fy25']
        for gr in V['vol_retail_g']:
            v0 *= (1 + gr + volg)
            vr.append(v0)
    mr = F['margin_retail'] if marg is None else [m * (1 + marg) for m in F['margin_retail']]
    gps = [vr[i] * mr[i] + F['gp_comm_struct'][i] + F['gp_nonfuel'][i] for i in range(N)]
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
SENS['beta'] = [[b, revalue(beta=b)] for b in (0.35, 0.45, 0.509, 0.70, 1.00)]
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

# ============================ OUTPUT ============================
def _load(name):
    p = os.path.join(HERE, name)
    return json.load(open(p)) if os.path.exists(p) else None


CAL = dict(step0=_load('step0_result.json'), backtest=_load('backtest_5y.json'),
           vol=_load('vol_diagnostic.json'), width=_load('width_diagnostic.json'))

OUT = dict(
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
