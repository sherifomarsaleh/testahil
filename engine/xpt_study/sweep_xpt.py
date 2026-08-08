"""Step 2A Information Sweep register for XPTUSD — built and VALIDATED with the
actual engine scaffold (engine/research_sweep.py). Emits sweep_register_xpt.json
+ Word-ready rows. Run BEFORE drivers were set (executed in-session in that order;
this file is the durable record)."""
import sys, os, json
sys.path.insert(0, os.path.abspath('repo/engine'))
from research_sweep import (SweepRegister, AssetClass, Ring, FindingClass as F,
                            SourceType as S, DriverMode as M)

r = SweepRegister('XPTUSD', AssetClass.METAL, '2026-07-20')

# ---- GLOBAL_MACRO ----
f_rr = r.add(Ring.GLOBAL_MACRO, "real rates & USD", F.S,
    "10Y TIPS real yield ~2.31% at the 18-Jul-2026 close (Treasury estimate via TipsWatch) — the highest 10-year real yield in ~18 years; rising path 1.99% (12-May, FRED) -> 2.07% (3-Jun, TE) -> 2.31%; firm dollar; hawkish 2026 repricing after hot CPI",
    "US Treasury est. via TipsWatch 19-Jul-2026 + FRED DFII10 trend", S.REGULATOR_OFFICIAL, "2026-07-18",
    detail="Hawkish regime caps a non-yielding metal near-term; 2027 easing is the re-rating option.",
    url="https://fred.stlouisfed.org/series/DFII10",
    model_impact="carry/opportunity-cost anchor: near-term tilt negative; sensitized via Expert 1 real-rate beta")
f_fed = r.add(Ring.GLOBAL_MACRO, "central-bank policy path", F.S,
    "Fed funds midpoint 3.63% held at the 16–17-Jun-2026 FOMC (statement 17 Jun; 3.50–3.75%); market pricing leans to hikes near-term, easing expected 2027",
    "federalreserve.gov FOMC statement 17-Jun-2026 + UBS 29-Jun-2026", S.REGULATOR_OFFICIAL, "2026-06-17",
    model_impact="rf_live=3.63% is the MC carry anchor (q=0); drift = ln(1.0363)·h/252")
f_off = r.add(Ring.GLOBAL_MACRO, "official-sector behavior", F.S,
    "WPIC reports PGMs 'fundamentally key' to China's 15th Five-Year Plan (AI/hydrogen) and frames platinum as a strategic metal — an INDUSTRY-COUNCIL characterization: China's official strategic-minerals catalogue is undisclosed and its reconstructed 2016/2021 lists carry NO PGMs; no central bank holds platinum reserves in size",
    "WPIC via Mining Weekly", S.REPUTABLE_PRESS, "2026-07-17",
    url="https://www.miningweekly.com/article/platinum-metals-fundamentally-key-to-chinas-five-year-plan-wpic-reports-2026-07-16",
    model_impact="supports the structural-demand leg of the balance anchor; no official-sector demand line added (none quantified)")

# ---- SUPPLY ----
f_mine = r.add(Ring.SUPPLY, "mine production", F.D,
    "WPIC Q1-2026 Quarterly: 2026f mine supply 5,551 koz flat (SA 4,005, Zim 508, Ru 646, NA 201, other 192); total supply 7,377 koz (+2%)",
    "WPIC Platinum Quarterly Q1 2026 (Metals Focus)", S.REGULATOR_OFFICIAL, "2026-05-18",
    url="https://platinuminvestment.com/files/634916/WPIC_Platinum_Quarterly_Q1_2026.pdf",
    model_impact="unlocks the bottom-up Appendix-A balance (the metal's 'financial statements')")
f_rec = r.add(Ring.SUPPLY, "recycling", F.D,
    "Recycling 1,826 koz 2026f (+9%): autocat 1,365, jewellery 373, industrial 88; recyclers working-capital-constrained at higher prices",
    "WPIC Platinum Quarterly Q1 2026", S.REGULATOR_OFFICIAL, "2026-05-18",
    model_impact="supply-response driver in the balance; the fastest-responding supply leg")
f_dis = r.add(Ring.SUPPLY, "disruptions", F.D,
    "Valterra Q2-2026: PGM M&C +1% YoY, Amandelbult +116% post-flood recovery, FY guidance unchanged 3.0–3.4 Moz; miners favour payouts over projects (S&P AISC 2026f $1,006/oz, +7.7%; SA electricity +900% since 2008); Valterra long-term planning $2,300–2,500",
    "Valterra Q2-2026 production report (Reuters) + Reuters/MarketScreener", S.REPUTABLE_PRESS, "2026-07-17",
    url="https://www.tradingview.com/news/reuters.com,2026-07-17:newsml_RSQ7965Ma:0-reg-valterra-platinum-ld-production-report-for-the-second-quarter-2026/",
    model_impact="unlocks the cost-floor/incentive anchor ($1,006 AISC; $2,300–2,500 incentive) and the no-supply-response assumption")

# ---- DEMAND ----
f_ind = r.add(Ring.DEMAND, "industrial demand", F.D,
    "Industrial 2,238 koz 2026f (+9%): chemical 612, glass 377, medical 332, electrical 119, petroleum 132, hydrogen 69 (from 22 in 2023; WPIC sees PEM electrolyser demand >500 koz p.a. within 10 years)",
    "WPIC Platinum Quarterly Q1 2026 + WPIC Perspectives", S.REGULATOR_OFFICIAL, "2026-05-18",
    model_impact="balance-anchor demand legs; hydrogen is the long-term accelerant, not a 2026 driver")
f_auto = r.add(Ring.DEMAND, "industrial demand", F.S,
    "Automotive 2,959 koz 2026f (−2%); Pt-for-Pd substitution (~700 koz embedded) flips: Pt now at a ~1.30× PREMIUM to Pd — reverse-substitution incentive live, but platform lock-in (~15% of models/yr, ~7-yr cycles) makes it slow",
    "WPIC Quarterly + WPIC substitution Perspectives (24-Jan-2024 mechanism) + spot cross-section 17-Jul-2026", S.REGULATOR_OFFICIAL, "2026-05-18",
    model_impact="THE crux driver (§1.7): reverse substitution sets the bear leg of the balance anchor; sensitized in real units (koz per 100 koz reversal)")
f_jew = r.add(Ring.DEMAND, "jewelry / consumer demand", F.S,
    "Jewellery 1,958 koz 2026f (−12%); China fabrication −42% YoY in Q1-2026 on price shock, weak sentiment, destocking and the 1-Nov-2025 removal of the 13% VAT rebate",
    "WPIC Platinum Quarterly Q1 2026", S.REGULATOR_OFFICIAL, "2026-05-18",
    model_impact="demand-destruction leg of the balance anchor; bear scenario driver")
f_inv = r.add(Ring.DEMAND, "investment / ETF flows", F.D,
    "Investment 519 koz 2026f: bars & coins 533 (+27%), China ≥500g bars 185, ETF −100, exchange stocks −100; China bar market grew <1t (2019) → ~13t (2025)",
    "WPIC Platinum Quarterly Q1 2026 + WPIC/Mining Weekly", S.REGULATOR_OFFICIAL, "2026-05-18",
    model_impact="investment leg of the balance; the price-sensitive marginal buyer")
f_offd = r.add(Ring.DEMAND, "official-sector purchases", F.NEG,
    "Negative search — nothing found (searched 'central bank platinum reserves purchases 2026', 'Gokhran platinum purchases 2026'; only China strategic-mineral classification and the historic Russian palladium precedent surfaced — no quantified official platinum buying)",
    "negative search", S.SEARCH, "2026-07-20")

# ---- MARKET_STRUCTURE ----
f_cot = r.add(Ring.MARKET_STRUCTURE, "positioning (COT)", F.C,
    "NYMEX managed-money net long ~+8.3k contracts (14-Jul-2026) — modestly long, far off extremes; palladium net short −6.2k",
    "CFTC COT via metalcharts.org", S.AGGREGATOR, "2026-07-14",
    url="https://metalcharts.org/cot")
f_lease = r.add(Ring.MARKET_STRUCTURE, "forward curve / lease rates", F.S,
    "Lease rates 'sky-high' through 2025 (physical squeeze; episodic spot backwardation in squeezes); elevated in Q1-2026 constraining bar fabrication, easing late-Q1 and 'falling' by late-June — the tightness premium partially unwound",
    "WPIC Quarterly + UBS 29-Jun-2026 + Bloomberg/MINING.COM (13-Nov-2025)", S.REPUTABLE_PRESS, "2026-06-29",
    model_impact="tightness premium in/out of the price; a lease-rate re-spike is a catalyst, normalization is the bear-carry state")
f_reg = r.add(Ring.MARKET_STRUCTURE, "regulatory treatment (e.g. Basel III)", F.S,
    "GFEX (Guangzhou) launched China's first platinum/palladium futures with stockpile publication — new price-discovery + transparency venue; US 2025 tariff-related dislocations have eased (UBS); China VAT-rebate removal (1-Nov-2025) reshaped jewellery flows",
    "Bloomberg/MINING.COM + UBS + WPIC", S.REPUTABLE_PRESS, "2026-06-29",
    model_impact="market-structure regime: GFEX adds a Chinese marginal-price setter; VAT change is in the jewellery driver")

# consensus/market-implied extras (color)
f_cons = r.add(Ring.MARKET_STRUCTURE, "forward curve / lease rates", F.D,
    "Forward anchors: UBS $1,700 (Sep/Dec-26) & $1,800 (Mar/Jun-27, 29-Jun-2026, spot $1,618); LBMA survey avg $2,222 (20-Jan-2026 — set at the record, stale-high); TE palladium model $1,554 12-mo",
    "UBS via Yahoo Finance + LBMA/Kitco", S.REPUTABLE_PRESS, "2026-06-29",
    url="https://uk.finance.yahoo.com/news/platinum-prices-forecast-lower-swiss-145800828.html",
    model_impact="unlocks the analyst-consensus forward anchor with the staleness axis (fresh post-crash vs stale peak-set)")

# ---- driver gate table ----
r.add_driver("2026 supply/demand balance (deficit 297 koz; AGS 1,747 koz ≈ 11 weeks)", M.BOTTOM_UP,
             "WPIC/Metals Focus Quarterly — the metal's official balance", [f_mine, f_rec, f_ind, f_auto, f_jew, f_inv])
r.add_driver("Analyst-consensus forward anchor ($1,700–1,800 fresh; $2,222 stale-high)", M.BOTTOM_UP,
             "published bank/survey targets, dated, staleness flagged", [f_cons])
r.add_driver("AISC cost floor $1,006/oz; incentive range $2,300–2,500", M.BOTTOM_UP,
             "S&P Global 2026 cost outlook + Valterra planning range", [f_dis])
neg_ratio = r.add_negative(Ring.MARKET_STRUCTURE, "positioning (COT)",
             "searched 'authoritative fair Pt/Au ratio level' — no market-standard neutral exists; house uses the post-2016-regime distribution of the attached series", "2026-07-20")
r.add_driver("Pt/Au neutral-ratio band (0.36–0.46, base = 5y mean 0.461… computed 0.461→base 1,831)", M.TOP_DOWN,
             "no authoritative neutral ratio exists; derived from the attached 2011–26 series, post-2016 regime, sensitized in §1.9", [neg_ratio, f_cons])
neg_q = r.add_negative(Ring.GLOBAL_MACRO, "central-bank policy path",
             "searched 'platinum holder yield / dividend' — none exists; lease rate is a borrow cost to users, not a holder yield", "2026-07-20")
r.add_driver("q_annual = 0 (no holder yield; METALS-profile precedent)", M.TOP_DOWN,
             "zero-yield store of value; carry = ln(1+rf) − ln(1+0)", [neg_q, f_fed])
neg_w = r.add_negative(Ring.DEMAND, "investment / ETF flows",
             "searched 'market-implied weighting of commodity fair-value anchors' — none exists; weights are a stated house judgment", "2026-07-20")
r.add_driver("Anchor weights 30/30/20/20 (ratio/consensus/balance/cost; carry = tilt)", M.TOP_DOWN,
             "house judgment, stated and logged to the Fundamental Driver Ledger; silver-study precedent 35/25/20/12/8", [neg_w])

errors, warnings = r.validate()
print("VALIDATE errors:", errors)
print("VALIDATE warnings:", warnings)
assert not errors, "sweep register failed validation"

payload = dict(ticker=r.ticker, asset_class=r.asset_class.value, sweep_date=r.sweep_date,
               findings=[dict(fid=f.fid, ring=f.ring.value, category=f.category, klass=f.klass.value,
                              headline=f.headline, source=f.source_name, source_type=f.source_type.value,
                              date=f.source_date, url=f.url, model_impact=f.model_impact) for f in r.findings],
               drivers=[dict(driver=x.driver, mode=x.mode.value, justification=x.justification,
                             refs=x.sweep_refs) for x in r.drivers])
json.dump(payload, open('sweep_register_xpt.json', 'w'), indent=1)
print(f"register: {len(r.findings)} findings, {len(r.drivers)} driver-gate rows -> sweep_register_xpt.json")
