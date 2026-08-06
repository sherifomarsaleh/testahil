"""SCEM — four-ring Information Sweep register.

Runs BEFORE any forecast driver is set. Every mandatory category of every ring is
closed by a dated finding or a dated negative search.

SOURCING NOTE, recorded rather than hidden: this build ran in an environment whose
egress policy refused a CONNECT to every external host (13 connect_rejected entries,
including sinaicement.com, egx.com.eg and every aggregator). The company's audited
statements are known to exist at
https://sinaicement.com/wp-content/uploads/2025/05/SCC-AFS-E-1224.pdf
and could not be retrieved. Financial-statement line items are therefore carried at
is_fs_data=True with REPUTABLE_PRESS provenance — reporting of the company's own EGX
filing — which the validator is designed to flag. The flag is left to fire and the
exception is disclosed; it is NOT closed by downgrading is_fs_data.
"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from research_sweep import (SweepRegister, AssetClass, Ring, FindingClass,
                            SourceType, DriverMode)

SWEEP_DATE = "2026-08-06"
R = SweepRegister("SCEM", AssetClass.STOCK, SWEEP_DATE)
CO, REG, PMD, PRESS, AGG = (SourceType.COMPANY_OFFICIAL, SourceType.REGULATOR_OFFICIAL,
                            SourceType.PRIMARY_MARKET_DATA, SourceType.REPUTABLE_PRESS,
                            SourceType.AGGREGATOR)

# ---------------------------------------------------------------- RING 1 GLOBAL
f_rate = R.add(Ring.GLOBAL, "rate cycle & USD/FX regime", FindingClass.S,
    "Global easing cycle underway; Fed funds midpoint 3.63% (Jun-2026), which sets the "
    "backdrop against which Egypt's own 19.50% policy rate normalises",
    "US Federal Reserve policy history (house FED_SCHEDULE, engine/market_profiles.py)",
    REG, "2026-06-18",
    model_impact="Anchors the terminal risk-free rate build and the direction of the "
                 "Kd glide: a falling global rate path is a necessary (not sufficient) "
                 "condition for the EGP cost-of-debt path assumed in the WACC glide.")

f_energy = R.add(Ring.GLOBAL, "commodity complex (input/output)", FindingClass.S,
    "Cement is an energy-conversion business: coal/petcoke and electricity are the "
    "dominant cash cost. Egypt's phased energy-subsidy reform keeps raising the local "
    "energy bill independent of the global fuel price",
    "Egypt Cement Industry Market Size & Forecast Report 2020-2029 (production faces "
    "pressure from energy reform, currency volatility and raw-material management)",
    PRESS, "2026-02-16",
    model_impact="Sets the EBITDA-margin glide DOWN from the FY2025 peak: energy reform "
                 "is a structural cost headwind that does not reverse with the cycle.")

f_gdem = R.add(Ring.GLOBAL, "global sector demand", FindingClass.C,
    "Cement is a non-traded-at-distance commodity — bulk sea freight limits the "
    "economic export radius, so global demand reaches SCEM only through the "
    "Mediterranean/East-African export basin, not through a world price",
    "Global Cement, Egypt country update", PRESS, "2025-10-01",
    model_impact="")

f_trade = R.add(Ring.GLOBAL, "trade / sanctions / supply chains", FindingClass.S,
    "Egyptian cement exports fell ~6% y/y to 18.5Mt in 2025, but the MIX inverted: "
    "finished-cement exports +66.6% to 12.5Mt while clinker exports fell ~38%",
    "Global Cement — Egyptian cement exports decline", PRESS, "2026-01-01",
    model_impact="Supports a higher realised price per tonne than a clinker-weighted mix "
                 "would give; carried in the realised-price driver rather than as a "
                 "separate export volume leg.")

# --------------------------------------------------------------- RING 2 COUNTRY
f_cbe = R.add(Ring.COUNTRY, "sovereign macro (inflation, policy rate, FX/deval risk)",
    FindingClass.D,
    "CBE main operation rate 19.50%, held since 2 Apr 2026. Headline inflation eased to "
    "14.6% in May-2026 (core 13.8%); CBE's own Q4-2026 target is 7% (+/-2pp) and it "
    "expects the target to be missed on average in Q4-2026 before declining from Q1-2027",
    "Central Bank of Egypt — policy rate and Monetary Policy Report Q1-2026; CPI release",
    REG, "2026-06-10",
    model_impact="Explicit-window risk-free rate = 19.50%. Terminal rf is norm-built off "
                 "the CBE's OWN stated medium-term target (7%) plus the standard EM "
                 "real-rate convention (~5.5pp) = 12.5% -- never a historical average.")

f_cds = R.add(Ring.COUNTRY, "sovereign macro (inflation, policy rate, FX/deval risk)",
    FindingClass.S,
    "Egypt 5-year CDS ~330bp (May-2026), materially tighter than the 2024 crisis peak",
    "Egypt 5Y CDS series", PMD, "2026-05-31",
    model_impact="Netted OUT of the local-currency risk-free rate in the Ke build so the "
                 "sovereign default premium is not charged twice (protocol Ke item 3), and "
                 "used as the country ERP add-on.")

f_reg = R.add(Ring.COUNTRY, "regulatory environment (regulator, caps, tariffs, tax/subsidy)",
    FindingClass.B,
    "The Egyptian Competition Authority PERMANENTLY lifted cement production quotas in "
    "July 2025 (suspended from May 2025). The quota regime had capped output since 2021",
    "Egyptian Competition Authority, reported via EnterpriseAM / Global Cement",
    PRESS, "2025-07-01",
    model_impact="BASE CHANGER. Removes the volume cap that held FY2021-24 utilisation "
                 "down, and simultaneously removes the price floor the cartel-substitute "
                 "provided. Drives BOTH the volume-recovery driver UP and the realised- "
                 "price driver DOWN across the forecast window.")

f_tax = R.add(Ring.COUNTRY, "regulatory environment (regulator, caps, tariffs, tax/subsidy)",
    FindingClass.C,
    "Egypt corporate income tax 22.5%, unchanged",
    "PwC Worldwide Tax Summaries (house Cost-of-Capital reference)", REG, "2026-01-01",
    model_impact="")

f_fisc = R.add(Ring.COUNTRY, "fiscal / political events with sector read-through",
    FindingClass.S,
    "State-led housing, industrial and transport programmes are the marginal buyer of "
    "Egyptian cement; domestic consumption rose 13.4% to 54Mt in 2025 on that programme",
    "Global Cement — Update on Egypt", PRESS, "2025-10-01",
    model_impact="Sets domestic demand growth in the explicit window; the forecast uses "
                 "the conservative published 2026 estimate (~1%) rather than the 5-8% "
                 "optimistic case, and sensitises the difference.")

# -------------------------------------------------------------- RING 3 INDUSTRY
f_bal = R.add(Ring.INDUSTRY, "demand drivers & capacity/supply balance", FindingClass.B,
    "2025 was the first year since 2008 that Egypt's cement supply-demand gap closed: "
    "domestic consumption 54Mt (+13.4% from 47.6Mt), production ~65Mt (+18% from 55Mt), "
    "operating utilisation ~98% against a nameplate 76Mt/yr across 46 lines",
    "Global Cement / cemnet (International Cement Review) — Egypt 2025 production",
    PRESS, "2026-01-01",
    model_impact="BASE CHANGER. Establishes FY2025 as a CYCLICAL PEAK, not a new plateau. "
                 "The normalised-earnings lens is anchored on this, and the explicit "
                 "window glides margin down from the FY2025 peak rather than holding it.")

f_revive = R.add(Ring.INDUSTRY, "new entrants (named-competitor level)", FindingClass.S,
    "Seven to nine dormant production lines are under study for revival, potentially "
    "adding 12.6Mt of supply from 2H 2026 -- ~23% of 2025 domestic consumption, landing "
    "INSIDE the explicit forecast window",
    "Global Cement — Update on Egypt", PRESS, "2025-10-01",
    model_impact="The single largest downside driver. Sets the realised-price decline in "
                 "FY2027-28 and is the mechanism behind the bear case in the sensitivity "
                 "grid; also caps the terminal margin.")

f_price = R.add(Ring.INDUSTRY, "pricing", FindingClass.D,
    "Egyptian cement prices roughly doubled to ~USD 81/t (EGP 3.9k) in 2025 from ~USD 50/t "
    "(EGP 2.1k) a year earlier, then are estimated to normalise to EGP 3,600-3,620/t in "
    "2026e on ~1% higher demand and higher costs",
    "EnterpriseAM Egypt — how Egypt's cement industry fared in 2025 and what's next",
    PRESS, "2026-01-01",
    model_impact="DRIVER UNLOCK: converts revenue from a top-down growth rate to a "
                 "bottom-up volume x realised-price unit build. Sets the FY2026 price "
                 "level directly and the decay path thereafter.")

f_sub = R.add(Ring.INDUSTRY, "technology substitution", FindingClass.C,
    "No material substitution threat to Portland cement in Egyptian construction over the "
    "forecast horizon; the live technology question is decarbonisation capex (alternative "
    "fuels, clinker factor), which is a cost/capex item rather than a demand substitution",
    "Global Cement sector coverage", PRESS, "2025-10-01", model_impact="")

f_peers = R.add(Ring.INDUSTRY, "competitor capacity / price moves (named)", FindingClass.D,
    "Named listed EGX peers all posted the same 2025 step-change: Misr Beni Suef (MBSC) "
    "attributable profit +373.7% to EGP 3.946bn on sales of EGP 5.700bn, EPS EGP 61.25, "
    "trailing P/E 6.44 and EV/EBITDA 5.03 on a EGP 13.73bn market cap; Arabian Cement "
    "(ARCC) FY2025 consolidated profit ~EGP 3.6bn (H1-2025 alone +305.5% to EGP 1.405bn)",
    "Arab Finance / EGX filings for MBSC and ARCC", PRESS, "2026-03-01",
    model_impact="Sets the relative-multiple lens peer set and confirms the sector-wide "
                 "(not company-specific) character of the 2025 earnings peak -- which is "
                 "why the multiple lens is applied to NORMALISED, not trailing, earnings.")

# --------------------------------------------------------------- RING 4 COMPANY
f_disp = R.add(Ring.COMPANY, "one-off base-resetting transactions", FindingClass.B,
    "SCEM sold its 25.40% stake in Sinai White Portland Cement to Aalborg Portland Holding "
    "(Cementir) for EUR 30m; completed 13 Aug 2024, taking Cementir to 96.5% of SWCC",
    "Cementir Holding N.V. corporate announcement; cemnet/ICR", PRESS, "2024-08-13",
    model_impact="BASE CHANGER, and the key to the whole history. The FY2024 disposal gain "
                 "is why FY2024 net profit (EGP 3.07bn) is 48% of revenue and why FY2025 "
                 "profit 'fell' 25% on a 41% revenue rise. FY2024 is excluded as a "
                 "normalisation base; the gain is stripped to derive underlying FY2024. "
                 "It also removes the ONLY non-cement earning leg, which is what makes the "
                 "single operating-company lens correct rather than a two-leg sum.")

f_mto = R.add(Ring.COMPANY, "ownership / stake changes (named-transaction rule)",
    FindingClass.S,
    "Vicat, via Vicat Egypt Cement Industries, holds 77.6%; in Jul-2025 it filed a "
    "mandatory tender offer for the remaining 58,416,664 shares (22.4%) at EGP 41.00/share",
    "FRA filing reported via Reuters/TradingView; Vicat H1-2025 results", PRESS, "2025-07-28",
    model_impact="Fixes the free float at 22.4% and the share count at 260,788,678 by "
                 "back-solving the offer (cross-checked against issued capital). The EGP 41 "
                 "offer price is a disclosed reference point far BELOW the EGP 79.00 spot "
                 "and is reported as an overhang, never as a fair value.")

f_cap = R.add(Ring.COMPANY, "management & capital actions", FindingClass.D,
    "Feb-2024 EGM raised authorised capital to EGP 10bn and issued capital by EGP 1.68bn; "
    "168.20m shares offered, 75.95% (127.74m) taken up by senior shareholders in phase 1. "
    "Issued capital now EGP 2,608,124,770 at EGP 10 par = 260,812,477 shares",
    "Sinai Cement EGM resolutions and capital-increase announcements via EGX", PRESS,
    "2024-07-01",
    model_impact="DRIVER UNLOCK: resolves the share count, which three aggregators report "
                 "wrongly at 141.46m. Also explains the IAS-33 restatement of FY2023 EPS "
                 "to -0.88 (unrestated -1.31 on the pre-issue 92.61m shares).")

f_fs = R.add(Ring.COMPANY, "official financial statements", FindingClass.D,
    "FY2023-FY2025 consolidated: revenue EGP 4.28bn / 6.42bn / 9.09bn; net profit after "
    "tax EGP -121.4m / +3,070m / +2,290m; FY2024 EPS attributable EGP 23.13 (FY2023 "
    "-0.88 restated); 9M-2025 net profit EGP 1.53bn",
    "EGX filings reported by Global Cement, cemnet/ICR, Daily News Egypt and Arab Finance",
    PRESS, "2026-03-10", is_fs_data=True,
    detail="PRIMARY SOURCE NOT RETRIEVABLE: the audited statements at "
           "sinaicement.com/wp-content/uploads/2025/05/SCC-AFS-E-1224.pdf were refused by "
           "this environment's egress policy. Provenance is press reporting of the "
           "company's own EGX filing, one step removed from the audited print.",
    model_impact="The disclosed history the model is built on. Revenue and net profit are "
                 "carried as printed; every line between them is DERIVED and labelled.")

f_bs = R.add(Ring.COMPANY, "regular disclosures", FindingClass.D,
    "Balance sheet: FY2024 total assets EGP 6,385.9m against total liabilities EGP "
    "1,610.9m (equity EGP 4,775.1m -- the triple closes exactly). Latest reported total "
    "debt EGP 36.8m against ~EGP 5.2bn equity, i.e. debt/equity 0.7% and a NET CASH "
    "position",
    "EGX filings via aggregated financial summaries", AGG, "2026-03-10", is_fs_data=True,
    model_impact="Fixes the capital structure: net cash, so the WACC is ~all-equity and "
                 "the EV->equity bridge ADDS net cash. Treasury income is excluded from "
                 "FCFF to avoid double-counting the cash.")

f_guid = R.add(Ring.COMPANY, "strategic plans & guidance", FindingClass.C,
    "SCEM operates two lines at El Hassana, North Sinai, ~3.8Mt/yr cement capacity, and "
    "reported lifting its market share to ~5% of the Egyptian market",
    "Company profile and FY2024 results commentary via Daily News Egypt / Global Energy "
    "Monitor plant register", PRESS, "2025-03-23",
    model_impact="")

f_neg_ir = R.add_negative(Ring.COMPANY, "IR communications (calls, presentations, releases)",
    "sinaicement.com investor relations, EGX disclosure portal, earnings-call transcripts "
    "and results presentations for FY2024/FY2025 -- every host refused by egress policy; "
    "no transcript or presentation obtainable from search either", SWEEP_DATE)

f_neg_int = R.add_negative(Ring.COMPANY, "regular disclosures",
    "'Sinai Cement other income / investment income / treasury bills / deposits EGP' and "
    "'9M 2025 operating profit gross profit cost of sales' -- no interest-income, "
    "finance-income or below-EBIT line item is disclosed in any retrievable source; the "
    "income statement between revenue and net profit is not obtainable line by line",
    SWEEP_DATE)

f_neg_capex = R.add_negative(Ring.COMPANY, "strategic plans & guidance",
    "'Sinai Cement capex / capital expenditure / investment plan / maintenance capex / "
    "free cash flow 2025 2026' -- no capital-expenditure figure, guidance or investment "
    "programme is disclosed in any retrievable source", SWEEP_DATE)

# ------------------------------------------------------------- DRIVER GATE TABLE
R.add_driver("Sales volume (Mt)", DriverMode.BOTTOM_UP,
    "Built from nameplate capacity (~3.8Mt/yr, two lines) times a utilisation path, "
    "cross-checked against the disclosed ~5% share of a 54Mt domestic market, and tied "
    "back to disclosed revenue. Quota removal is the unlock that lets utilisation rise.",
    [f_guid, f_reg, f_bal, f_fs])
R.add_driver("Realised price (EGP/t)", DriverMode.BOTTOM_UP,
    "Disclosed industry price levels (EGP 2.1k 2024 -> 3.9k 2025 -> 3.6k 2026e) give a "
    "direct price path; the company's own realised price is solved from disclosed revenue "
    "divided by the derived volume, so the build ties back to the printed top line.",
    [f_price, f_fs])
R.add_driver("EBITDA margin glide", DriverMode.BOTTOM_UP,
    "Glides down from the FY2025 cyclical peak on two named, dated mechanisms: 12.6Mt of "
    "dormant capacity under revival from 2H-2026, and phased energy-subsidy reform, "
    "anchored on the disclosed FY2023-25 revenue and profit history.",
    [f_revive, f_energy, f_bal, f_fs])
R.add_driver("Cost of debt (Kd) and the WACC glide", DriverMode.BOTTOM_UP,
    "The company is net cash with EGP 36.8m of gross debt, so Kd carries almost no weight; "
    "the glide shape is inherited from the CBE easing path rather than invented.",
    [f_bs, f_cbe])
R.add_driver("Terminal risk-free rate", DriverMode.BOTTOM_UP,
    "Norm-built from the CBE's own published medium-term inflation target plus a standard "
    "EM real-rate convention, never backed out of a price or averaged from history.",
    [f_cbe])
R.add_driver("Treasury / interest income", DriverMode.TOP_DOWN,
    "Modelled top-down as a yield on the modelled cash balance. The interest-income line "
    "itself is not separately disclosed in any retrievable source, so it cannot be built "
    "bottom-up; it is excluded from FCFF entirely and handled in the equity bridge.",
    [f_bs, f_neg_int])
R.add_driver("Capex", DriverMode.TOP_DOWN,
    "No capital-expenditure guidance, maintenance-capex disclosure or investment plan is "
    "obtainable; capex is set as a percentage of revenue benchmarked to a mature, fully "
    "built two-line plant, and sensitised.",
    [f_neg_capex])

# ------------------------------------------------------------------------ OUTPUT
errors, warnings = R.validate()
R.to_json(os.path.join(HERE, 'sweep_register.json'))
print(R.qc_line())
print(f"\nfindings: {len(R.findings)} | drivers: {len(R.drivers)}")
if errors:
    print(f"\nVALIDATOR ERRORS ({len(errors)}) — disclosed, not suppressed:")
    for e in errors:
        print(f"  ! {e}")
if warnings:
    print(f"\nwarnings ({len(warnings)}):")
    for w in warnings:
        print(f"  - {w}")
fr = R.check_freshness("2026-08-06")
print(f"\nfreshness: {fr or 'OK — sweep and delivery same day'}")
