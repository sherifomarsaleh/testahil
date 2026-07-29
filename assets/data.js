/* =========================================================
   testahil — the ONLY file you edit in the weekly ritual.
   ========================================================= */

const SITE = { updated: "2026-07-29", latest: "DSCW" };  // latest = the LAST-PUBLISHED study (drives the homepage hero); set this on every publish

/* ---------- covered tickers ----------
   HORIZON FIELDS (see the HORIZON CONVENTION block above the LEDGER):
     dist.t20 / dist.t60   the two published cones. The KEY NAMES are historical
                           (they date from the retired session-count convention)
                           and are kept so every ticker page keeps working — read
                           them as "near horizon" and "far horizon", not as a
                           claim about 20 and 60 sessions. dist.*.label carries
                           the human horizon name.
     hz                    OPTIONAL, set on a cohort struck under the calendar
                           convention (27-Jul-2026 onward):
                             hz:{ h1:21, h3:63, l1:"1 month", l3:"3 months", cal:true }
                           h1/h3 are the session counts the cones were actually
                           simulated over, from engine/horizons.py resolve().
                           app.js (hzOf) reads it for the fan axis, the touch
                           ladder headers and the hover read-out. ABSENT means
                           legacy cohorts, struck on the retired session count. Do not add
                           hz to a ticker whose cones are still legacy — the
                           label would then misstate what was simulated.
   ------------------------------------- */
const TICKERS = {
  CLHO: {
    name: "Cleopatra Hospitals Group",
    nameAr: "\u0645\u062c\u0645\u0648\u0639\u0629 \u0645\u0633\u062a\u0634\u0641\u064a\u0627\u062a \u0643\u0644\u064a\u0648\u0628\u0627\u062a\u0631\u0627",
    code: "EGX:CLHO",
    spot: 16.90,
    spotDate: "close 22 Jul 2026",
    ccy: "EGP",
    fair: { bear: 6.51, base: 9.21, full: 11.05 },      // 13 Jul 2026 \u2014 four-lens weighted central EGP 9.21 (\u221244% vs spot 16.31). Lenses: rate-path FCFF DCF (40%) 7.17; relative multiples, FY27E EPS discounted back to today (25%) 13.21; normalized earnings power, interest re-priced not deleted (20%) 8.37; EV per operational bed, re-anchored to CLHO\u2019s own build cost and discounted from 2027 (15%) 9.08. THIS RANGE WAS REBUILT UNDER EXTERNAL AUDIT (13-Jul-2026): the prior version (central 13.29) capitalised terminal value directly (implied terminal ROIC 34.2%, above anything CLHO has ever earned), deducted minority interests at book value instead of fair value, and blended two forward-dated lenses into a same-day estimate without discounting them back \u2014 all three biased the same direction, upward. Corrected: terminal value now forces reinvestment to g/ROIC (ROIC 18%, inside CLHO\u2019s realized 17\u201323% range); non-controlling interest is a Cairo Specialized Hospital mini-SOTP at fair value (~EGP 782mn vs EGP 453mn book); both forward lenses are discounted to a present value. Discount rate: WACC 25.15% explicit \u2192 17.87% terminal, a sliding schedule glide-shaped off the CBE easing calendar, with the sovereign CDS spread netted out of the risk-free rate and beta floored at the house band minimum (0.80, vs a weak, wide-CI 0.446 regression). Cost of debt is audited, not assumed: CLHO\u2019s own FY2024 accounts show 28.90% contractual on loans against a 28.25% CBE corridor \u2014 a +65bp spread confirmed at two year-ends \u2014 and the debt book is 100% EGP, zero FX exposure. SPOT IS RICH ON EVERY FUNDAMENTAL LENS BUT ONE (EV/bed bull, which requires a takeout-style re-rating): the DCF bull case alone (8.12) is barely half of spot, so the market is pricing something closer to a strategic-review / per-bed transaction outcome than standalone cash-flow generation. Revenue itself is rebuilt bottom-up from disclosed KPI volumes and ARPs (77% of FY25 revenue, incl. laboratory and radiology), fading from each line\u2019s own FY24\u2192FY25 growth rate as the group\u2019s bed-capacity ramp (880\u21921,320 by 2027) completes \u2014 reaching 2.07\u00d7 FY2028E vs FY2025, almost exactly management\u2019s own \u201cmore than double by 2028\u201d guidance. Risk flagged but not yet in the base case: a developing 2026-27 El Ni\u00f1o carries a 96% NOAA probability and could keep global food inflation elevated into 2028 (Goldman Sachs, UniCredit), which would prevent the CBE easing this valuation\u2019s terminal WACC assumes.",
    levels: { res:[17.29, 17.90, 19], sup:[13.90, 13.02, 12.10] },   // 19 Jul 2026 — computed from own OHLC (SMA20/50/200, 52w range, swing points); technical-only
    dist: {
      t20: { label:"1 month",   p5:13.75, p25:15.80, p50:17.15, p75:18.63, p95:21.41, resolve:"2026-08-23" },
      t60: { label:"3 months",  p5:11.93, p25:15.30, p50:17.70, p75:20.43, p95:26.18, resolve:"2026-10-22" }
    },
    hz: { h1:20, h3:61, l1:"1 month", l3:"3 months", cal:true },
    touch: [ /* descending high -> low; P(touch) 1-month %, 3-month % */
      [22.00, 5, 27], [21.00, 10, 35], [20.00, 18, 47], [19.00, 33, 61], [18.00, 56, 77], [17.00, 86, 93], [16.00, 52, 68], [15.00, 25, 46], [14.00, 11, 29], [13.00, 4, 17], [12.00, 2, 10], [11.00, 1, 5]
    ],
    levels: { res:[16.85, 17.19, 17.39], sup:[16.09, 15.46, 14.04] },
    tech: {
      trend: "Trading above the whole moving-average stack, on a rising 200-day",
      summary: "The price closed 16.90 above a rising 20-day (16.51), a rising 50-day (15.90) and a rising 200-day (13.27). Momentum is firm: RSI(14) is ~60 and the daily ATR near 0.60 (~3.5%) points to a lively tape. MACD (12\u00b726\u00b79) is positive and rising (+0.30 / +0.29 / +0.01). Over the last year it has ranged 7.90\u201317.90; the last close sits 6% below that high and 114% above that low.",
      bull: "A daily close back above 17.29 would clear the nearest resistance and open the 19.00 zone.",
      bear: "A close below 13.90 would break the nearest support and open the 12.10 zone."
    },
    asof: {
      mc:   { data:"2026-07-22", computed:"2026-07-28" },
      tech: { data:"2026-07-22", computed:"2026-07-29" }
    },
    files: {
      study: "files/CLHO_Valuation_Study_13-07-2026_public.docx?v=20260713d",
      model: "files/CLHO_Valuation_Model_13072026_public.xlsx?v=20260713d"
    }
  },
  RMDA: {
    name: "Rameda Pharmaceuticals",
    nameAr: "\u0631\u0627\u0645\u064a\u062f\u0627 \u0644\u0644\u0623\u062f\u0648\u064a\u0629",
    code: "EGX:RMDA",
    spot: 4.98,
    spotDate: "close 22 Jul 2026",
    ccy: "EGP",
    fair: { bear: 2.11, base: 2.77, full: 3.48 },      // 13 Jul 2026 \u2014 four-lens weighted central EGP 2.77 (\u221245% vs spot 5.00). Lenses: FCFF DCF (35%) 1.73; relative EV/EBITDA on RMDA\u2019s own trading band (25%) 4.40; normalized earnings power (25%) 3.65; dividend discount (15%) 1.00. bear/full = weighted bear/bull. THE DIVERGENCE IS THE FINDING AND WE REFUSE TO BLEND IT AWAY: the cash-flow lens discounted at Egypt\u2019s SOURCED cost of capital says 1.73, while the lenses that price the engine at market multiples say 3.65\u20134.40. A price of 5.00 is the market asserting that Egyptian discount rates normalise AND the balance sheet deleverages \u2014 both plausible, neither yet in the sourced numbers. WHY REVENUE DOUBLED, AND WHY IT WILL NOT DOUBLE AGAIN: FY23\u2192FY25 revenue went 1,922 \u2192 4,096 (+113%), but the decomposition says that was THREE ONE-OFFS stacked on a real engine \u2014 (1) the EDA pricing catch-up regime (40\u201350% approvals, now ~82% of market SKUs complete), (2) a shortage-driven private volume spike (2Q25 units +56% because rivals could not supply), and (3) export resumption from literally ZERO (the Iraq suspension made FY24 exports nil). The 1Q26 print is the proof the regime is over: revenue +23% but volumes ex-toll only +7% and PRIVATE VOLUMES \u22125%, with management stating growth came \u2018with limited reliance on pricing actions\u2019. None of the three repeats, so the forward path tapers +19% \u2192 +9%, it does not re-double. THE COST OF DEBT WAS AUDITED, NOT ASSUMED: the facility book is 100% EGP-denominated (Note 20 lists all 11 banks in EGP; FX exposure sits in import payables, not debt \u2014 there is no cheap-dollar blend available), and the rate Rameda ACTUALLY PAYS is 24.0% annualised in 1Q26 (interest \u00f7 average facilities), not the 20.5% midpoint of the disclosed contractual range \u2014 a 350bp understatement we caught and corrected. THE DISCOUNT RATE SLIDES, IT IS NOT FLAT: 26.6% in FY26E easing to a norm-built 18.8% terminal, on the same CBE calendar already used for the interest forecast \u2014 one price of time per date, so the terminal value is never quietly discounted at a rate the explicit years are denied. THE CRUX IS THE RATE PATH, IN REAL UNITS: every 100bp off the facility cost is EGP 21mn of pre-tax profit, and at a flat ~12.5% WACC the same cash flows are worth spot. This is a pharmaceutical manufacturer wearing the costume of a leveraged bet on Egyptian monetary policy, and the study says so in numbers rather than adjectives.
    levels: { res:[5.03, 5.17, 5.38], sup:[4.93, 3.52, 3.24] },   // 19 Jul 2026 — computed from own OHLC (SMA20/50/200, 52w range, swing points); technical-only
    dist: {
      t20: { label:"1 month",   p5:4.39, p25:4.80, p50:5.05, p75:5.33, p95:5.82, resolve:"2026-08-23" },
      t60: { label:"3 months",  p5:3.89, p25:4.68, p50:5.21, p75:5.80, p95:6.98, resolve:"2026-10-22" }
    },
    hz: { h1:20, h3:61, l1:"1 month", l3:"3 months", cal:true },
    touch: [ /* descending high -> low; P(touch) 1-month %, 3-month % */
      [6.50, 1, 16], [6.00, 4, 31], [5.75, 10, 43], [5.50, 23, 59], [5.25, 49, 76], [4.75, 40, 63], [4.50, 14, 39], [4.25, 5, 23], [4.00, 2, 13]
    ],
    levels: { res:[5.02, 5.29, 5.38], sup:[4.96, 4.63, 3.92] },
    tech: {
      trend: "Mixed against the moving-average stack, above a rising 200-day",
      summary: "The price closed 4.98 above a falling 20-day (4.98) and a rising 200-day (3.99), but below a rising 50-day (5.03). Momentum is neutral: RSI(14) is ~49 and the daily ATR near 0.09 (~1.9%) points to a normal tape. MACD (12\u00b726\u00b79) is negative and still falling (\u22120.01 / \u22120.00 / \u22120.00). Over the last year it has ranged 3.02\u20135.38; the last close sits 7% below that high and 65% above that low.",
      bull: "A daily close back above 5.03 would clear the nearest resistance and open the 5.38 zone.",
      bear: "A close below 4.93 would break the nearest support and open the 3.24 zone."
    },
    asof: {
      mc:   { data:"2026-07-22", computed:"2026-07-28" },
      tech: { data:"2026-07-22", computed:"2026-07-29" }
    },
    files: {
      study: "files/RMDA_Valuation_Study_13-07-2026_public.docx?v=20260713c",
      model: "files/RMDA_Valuation_Model_13072026_public.xlsx?v=20260713c",
      pdf:   "files/RMDA_Valuation_Study_13-07-2026_public.pdf?v=20260713c",
      biblio:"files/RMDA_Source_Register_13-07-2026.docx?v=20260713c"
    }
  },
  DEWA: {
    name: "DEWA (Dubai Electricity and Water Authority)",
    nameAr: "هيئة كهرباء ومياه دبي",
    code: "DFM:DEWA",
    spot: 2.67,
    spotDate: "close 24 Jul 2026",
    ccy: "AED",
    fair: { bear: 2.18, base: 3.32, full: 4.92 },      // 12 Jul 2026 -- four-lens weighted central 3.32 (+19.1% vs spot 2.79). Lenses: dividend discount (policy lens, primary, 35%) 3.83 off the AED 6.2bn/yr floor to Oct-2027, FCFF DCF (20%, ceiling -- 87% of EV is terminal value, disclosed) 3.36, relative EV/EBITDA vs GCC utility peers (25%) 2.93, justified P/B off the regulated return spread (20%) 2.91. bear/full = weighted bear/bull. The crux is the post-Oct-2027 dividend-policy signal (undecided): market-implied perpetual growth is just 1.3-2.3%, well below the DCF's 2.5% terminal assumption. Beta 0.50 used vs 0.42 regressed (equal-weight 14-name UAE proxy, DFM General Index not programmatically retrievable), sensitised 0.40-0.70. WACC 6.24%/6.27% (rating/CDS ERP basis).
    dist: {
      t20: { label:"1 month",   p5:2.41, p25:2.57, p50:2.68, p75:2.79, p95:2.97, resolve:"2026-08-24" },
      t60: { label:"3 months",  p5:2.24, p25:2.51, p50:2.70, p75:2.89, p95:3.25, resolve:"2026-10-26" }
    },
    hz: { h1:20, h3:63, l1:"1 month", l3:"3 months", cal:true },
    touch: [ /* descending high -> low; P(touch) 1-month %, 3-month % */
      [3.30, 0, 7], [3.20, 1, 11], [3.10, 2, 17], [3.00, 6, 28], [2.90, 15, 43], [2.80, 37, 63], [2.70, 76, 87], [2.60, 55, 73], [2.50, 22, 46], [2.40, 7, 27]
    ],
    levels: { res:[2.73, 2.82, 3.14], sup:[2.61, 2.55, 2.46] },
    tech: {
      trend: "Trading below the whole moving-average stack, under a flat 200-day",
      summary: "The price closed 2.67 below a falling 20-day (2.74), a flat 50-day (2.71) and a flat 200-day (2.79). Momentum is neutral: RSI(14) is ~43 and the daily ATR near 0.05 (~2.1%) points to a normal tape. MACD (12\u00b726\u00b79) is negative and still falling (\u22120.02 / \u22120.01 / \u22120.01). Over the last year it has ranged 2.47\u20133.15; the last close sits 15% below that high and 8% above that low.",
      bull: "A daily close back above 2.73 would clear the nearest resistance and open the 3.14 zone.",
      bear: "A close below 2.61 would break the nearest support and open the 2.46 zone."
    },
    asof: {
      mc:   { data:"2026-07-24", computed:"2026-07-28" },
      tech: { data:"2026-07-24", computed:"2026-07-29" }
    },
    files: {
      study: "files/DEWA_Valuation_Study_11-07-2026_public.docx?v=20260713b",
      model: "files/DEWA_Valuation_Model_11072026_public.xlsx?v=20260713b",
      pdf:   "files/DEWA_Valuation_Study_11-07-2026_public.pdf?v=20260713b"
    }
  },
  LULU: {
    name: "Lulu Retail Holdings",
    nameAr: "\u0644\u0648\u0644\u0648 \u0644\u0644\u062a\u062c\u0632\u0626\u0629",
    code: "ADX:LULU",
    spot: 0.96,
    spotDate: "close 24 Jul 2026",
    ccy: "AED",
    fair: { bear: 0.78, base: 1.28, full: 1.74 },      // 12 Jul 2026 (v3) — four-lens weighted central 1.28 (+36% vs spot 0.94). Lenses: FCFF DCF, segment-built from six country models (30%) 1.54; relative EV/EBITDA (30%) 1.18; dividend discount (25%) 1.15; normalized earnings (15%) 1.16. bear/full = weighted bear/bull. THE COMPANY DOES NOT REPORT SALES DENSITY, SO WE BUILT IT. Revenue per square metre fell -1.4% in FY2025 and roughly -8% in Q1-2026 (bounded -4.3% to -9.4% — one input, Q1-2025 floor space, is not disclosed). Lulu is adding space into falling productivity. THE ENGINE: operating cost tracks SPACE; revenue tracks SPACE x DENSITY. So the EBITDA margin is flat only when density growth equals mature-store cost inflation — a break-even that is DERIVED, not assumed, and which ties on both periods we can test. It reproduces the Q1 margin bridge with nothing modelled: 10.23% -> 9.50%, of which -65bp is OPERATING DELEVERAGE (revenue -2.9%, cash opex +1.1% — both disclosed) and only -7bp is gross margin. The margin is not a lever management pulls; it falls out of the density. TWO MORE FINDINGS. (1) SAUDI: we rebuilt segment floor space from the company's own hypermarket/express split and its disclosed 9,200 sqm average hypermarket — it reconstructs the disclosed 1.380m sqm estate to 0.6%. Saudi sells US$4,489 per sqm against Qatar's US$9,027. Its stores are not small: 46% are hypermarkets, the same share as the group. They are UNPRODUCTIVE, which is why Saudi opex runs 22.1% of revenue against the UAE's 14.5% and its EBITDA margin is 4.66%. (2) THE DIVIDEND: 7 fils is 96% of EARNINGS but 1.33x covered by CASH (after charging working capital — the 12-Jul revision omitted it and printed 1.40x), because depreciation (US$388mn) is nearly three times capex (US$139mn) — the leases ARE the capex. A cash-covered 7.45% yield is a very different proposition from an uncovered one. AND THE HONEST CAVEAT: at 7.15x EV/EBITDAaL (after lease payments) Lulu is NOT cheap on an absolute basis. It is cheap RELATIVE to how its peers are quoted, because every peer multiple is struck on the same post-IFRS-16 basis. Two different claims; we make only the second. REVISION r1 (13-Jul-2026, build e9fc9b7dba6a): twelve corrections after two external audits, listed in full at the end of the study. The most important CUTS AGAINST US — the 12-Jul revision claimed a -6% density year puts the central at spot; its own grid says the central is 1.12 there, and density alone NEVER reaches spot. The market is pricing lost density AND a terminal de-rating AND a higher cost of capital AND a dividend cut. The crux was overclaimed. Also corrected: the beta diagnostics (mutually impossible as printed), a circular debt cross-check (withdrawn), the dividend cover (now charges working capital: 1.40x -> 1.33x), FY2024 stores (247 -> 250, per the company release), and Pillar Two / UAE DMTT (15% floor, in force since FY2025) is now modelled and in the risk register. THE REGISTERED FORECAST BELOW IS UNCHANGED: the Monte-Carlo drift is carry plus the event ledger, and no correction touches either. The study is revised; the forecast is not.
    dist: {
      t20: { label:"1 month",   p5:0.84, p25:0.91, p50:0.96, p75:1.02, p95:1.10, resolve:"2026-08-24" },
      t60: { label:"3 months",  p5:0.75, p25:0.88, p50:0.97, p75:1.07, p95:1.26, resolve:"2026-10-26" }
    },
    hz: { h1:20, h3:63, l1:"1 month", l3:"3 months", cal:true },
    touch: [ /* descending high -> low; P(touch) 1-month %, 3-month %. The UAE market cone is OVER-COVERED, so read these as UPPER BOUNDS. */
      [1.30, 0, 6], [1.20, 1, 14], [1.10, 9, 35], [1.05, 23, 52], [1.00, 53, 74], [0.90, 34, 59], [0.85, 11, 35], [0.80, 3, 19], [0.75, 1, 9]
    ],
    levels: { res:[1.08, 1.16, 1.21], sup:[0.95, 0.93, 0.91] },
    tech: {
      trend: "Mixed against the moving-average stack, below a falling 200-day",
      summary: "The price closed 0.96 below a falling 50-day (0.97) and a falling 200-day (1.07), but above a falling 20-day (0.94). Momentum is neutral: RSI(14) is ~53 and the daily ATR near 0.02 (~1.6%) points to a normal tape. MACD (12\u00b726\u00b79) is below zero but turning up (\u22120.01 / \u22120.01 / +0.00). Over the last year it has ranged 0.91\u20131.27; the last close sits 24% below that high and 5% above that low.",
      bull: "A daily close back above 1.08 would clear the nearest resistance and open the 1.21 zone.",
      bear: "A close below 0.95 would break the nearest support and open the 0.91 zone."
    },
    asof: {
      mc:   { data:"2026-07-24", computed:"2026-07-28" },
      tech: { data:"2026-07-24", computed:"2026-07-29" }
    },
    files: {
      study: "files/LULU_Valuation_Study_13-07-2026_public.docx?v=20260713b",
      model: "files/LULU_Valuation_Model_13072026_public.xlsx?v=20260713b",
      pdf:   "files/LULU_Valuation_Study_13-07-2026_public.pdf?v=20260713b",
      biblio:"files/LULU_Source_Register_13-07-2026.docx?v=20260713b"
    }
  },

  BURJEEL: {
    name: "Burjeel Holdings PLC",
    nameAr: "\u0628\u0631\u062c\u064a\u0644 \u0627\u0644\u0642\u0627\u0628\u0636\u0629",
    code: "ADX:BURJEEL",
    spot: 1.20,
    spotDate: "close 24 Jul 2026",
    ccy: "AED",
    fair: { bear: 1.14, base: 1.85, full: 2.35 },      // 12 Jul 2026 (rev. 2 reissue) — four-lens weighted central 1.85 (+67% vs spot 1.11). bear/full = weighted bear/bull. Lenses: FCFF DCF (primary, 35%) 2.64, relative EV/EBITDA (25%) 1.89 at a 11.5x base — a deliberate discount to the verified GCC hospital-peer FLOOR (MEH ~13x; Al Habib 24-34x, Dallah 22-26x, Mouwasat 18-19x, Hammadi 17.5x — Bloomberg/U Capital, MarketScreener, multiples.vc, dated), normalized earnings (25%) 1.49 at 17x clean FY26E EPS, dividend discount (15%) 0.56 reflecting the FY2025 payout cut. TAX REBUILT ON MECHANICS, NOT THE HEADLINE: the UAE's 15% DMTT top-up applies only to income above a substance-based income exclusion (9.4% of payroll + 7.4% of tangible assets in 2026, stepping to 5%/5% by 2033) — Burjeel's own FY2025 effective rate was 7.0% (tax 38 on PBT 541), consistent with a 10-to-13% modelled path rather than a flat 15%; the transitional CbCR safe harbour can deem the top-up zero outright for FYs starting pre-2027. Flat 15% is kept as the bear rung only. THE CRUX IS CASH, NOT THE STORY: FY2025 absorbed AED 649mn of operating surplus into working capital before it reached cash (DSO 135 days, rising), which is why the marginal sukuk priced at 7.00%/5yr (BB+) against a ~3.9% sovereign, and why the dividend was cut. Spot 1.11 sits just BELOW the weighted bear case (1.14): the market prices a margin stuck in the high-teens, the full 15% assessed with no substance relief, receivables never normalizing, Saudi staying a rounding error, and zero credit for a management team that guided a 23.5% margin and delivered 18.1% — then discounts a little further. Genuinely thin float (~11%; some 2024-25 buyback execution undisclosed) keeps idiosyncratic volatility high. Calibration: PARITY on the production UAE panel (11 non-overlapping 60-day windows, CRPS skill +0.85%, 90% CI [-1.7%, +2.5%], robust across bootstrap block sizes) — a calibrated, market-panel-validated distribution with no single-name edge claimed.
    dist: {
      t20: { label:"1 month",   p5:1.03, p25:1.13, p50:1.20, p75:1.28, p95:1.41, resolve:"2026-08-24" },
      t60: { label:"3 months",  p5:0.91, p25:1.09, p50:1.21, p75:1.35, p95:1.61, resolve:"2026-10-26" }
    },
    hz: { h1:20, h3:63, l1:"1 month", l3:"3 months", cal:true },
    touch: [ /* descending high -> low; P(touch) 1-month %, 3-month %. */
      [1.30, 33, 59], [1.25, 58, 76], [1.20, 100, 100], [1.15, 54, 72], [1.05, 12, 35], [1.00, 5, 22], [0.95, 2, 13], [0.90, 1, 7]
    ],
    levels: { res:[1.29, 1.35, 1.43], sup:[1.09, 1.03, 1] },
    tech: {
      trend: "Mixed against the moving-average stack, below a falling 200-day",
      summary: "The price closed 1.20 above a falling 20-day (1.12) and a flat 50-day (1.09), but below a falling 200-day (1.22). Momentum is firm: RSI(14) is ~66 and the daily ATR near 0.04 (~3.0%) points to a lively tape. MACD (12\u00b726\u00b79) is positive and rising (+0.02 / +0.00 / +0.01). Over the last year it has ranged 1.00\u20131.57; the last close sits 24% below that high and 20% above that low.",
      bull: "A daily close back above 1.29 would clear the nearest resistance and open the 1.43 zone.",
      bear: "A close below 1.09 would break the nearest support and open the 1.00 zone."
    },
    asof: {
      mc:   { data:"2026-07-24", computed:"2026-07-28" },
      tech: { data:"2026-07-24", computed:"2026-07-29" }
    },
    files: {
      study: "files/BURJEEL_Valuation_Study_11-07-2026_public.docx?v=20260713b",
      model: "files/BURJEEL_Valuation_Model_11072026_public.xlsx?v=20260713b",
      pdf:   "files/BURJEEL_Valuation_Study_11-07-2026_public.pdf?v=20260713b"
    }
  },
  SALIK: {
    name: "Salik Company",
    nameAr: "\u0633\u0627\u0644\u0643",
    code: "DFM:SALIK",
    spot: 5.47,
    spotDate: "close 24 Jul 2026",
    ccy: "AED",
    fair: { bear: 3.32, base: 4.62, full: 7.05 },      // 12 Jul 2026 (v3) — four-lens weighted central 4.62 (-19% vs spot 5.70). Lenses: FCFF DCF (primary, 45%) 4.49, normalized earnings power (20%) 5.44, relative P/E which with a 100% payout IS the dividend yield (20%) 4.89, dividend discount (15%) 3.55 — the DDM is a structural FLOOR because the payout is 100% of PROFIT but only 93% of CASH. bear/full = weighted bear/bull. BETA IS MEASURED, NOT ASSUMED: weekly regression vs an equal-weighted 14-name UAE market portfolio (both exchanges) gives β 0.637 (n=195, t=6.1, R² 16%) — the gate PASSES; we publish the Blume-adjusted 0.76. THE CRUX: SALIK's beta was 0.47 BEFORE the war and 1.00 DURING it. The war cut Q1 chargeable trips 7.7% AND doubled the discount rate's risk loading — numerator and denominator at once. Spot implies β 0.52, inside our measured 95% CI [0.43, 0.84] and almost exactly the PRE-WAR reading: the market is pricing Salik as though the war is already over. TWO OTHER FINDINGS: (1) the 8 gates the RTA HANDED Salik at the IPO earn 32% ROIC; the 2 it SOLD Salik in 2024 for AED 2,734mn earn 9.5% against an 8.1% WACC — growth by acquiring gates is not free growth. (2) 84% of FY2025's +35% revenue growth was two one-offs (gate count 8→10; tariff flat→variable). And a senior claim sits in front of the dividend: AED 455.7mn/yr to the RTA until Nov-2030 against a retained wedge of only AED 116mn.
    dist: {
      t20: { label:"1 month",   p5:4.83, p25:5.22, p50:5.49, p75:5.76, p95:6.22, resolve:"2026-08-24" },
      t60: { label:"3 months",  p5:4.34, p25:5.04, p50:5.52, p75:6.06, p95:7.03, resolve:"2026-10-26" }
    },
    hz: { h1:20, h3:63, l1:"1 month", l3:"3 months", cal:true },
    touch: [ /* descending high -> low; P(touch) 1-month %, 3-month %. NOTE: the calibration back-test cone is OVER-COVERED, so read these as UPPER BOUNDS. */
      [7.00, 0, 9], [6.50, 3, 21], [6.25, 7, 33], [6.00, 19, 48], [5.50, 83, 91], [5.25, 48, 69], [5.00, 18, 45], [4.50, 1, 14]
    ],
    levels: { res:[5.77, 6.01, 6.26], sup:[5.34, 5.23, 4.98] },
    tech: {
      trend: "Trading below the whole moving-average stack, under a falling 200-day",
      summary: "The price closed 5.47 below a falling 20-day (5.67), a falling 50-day (5.69) and a falling 200-day (5.94). Momentum is neutral: RSI(14) is ~40 and the daily ATR near 0.13 (~2.3%) points to a normal tape. MACD (12\u00b726\u00b79) is negative and still falling (\u22120.08 / \u22120.05 / \u22120.03). Over the last year it has ranged 4.96\u20136.96; the last close sits 21% below that high and 10% above that low.",
      bull: "A daily close back above 5.77 would clear the nearest resistance and open the 6.26 zone.",
      bear: "A close below 5.34 would break the nearest support and open the 4.98 zone."
    },
    asof: {
      mc:   { data:"2026-07-24", computed:"2026-07-28" },
      tech: { data:"2026-07-24", computed:"2026-07-29" }
    },
    files: {
      study: "files/SALIK_Valuation_Study_11-07-2026_public.docx?v=20260713b",
      model: "files/SALIK_Valuation_Model_11072026_public.xlsx?v=20260713b",
      pdf:   "files/SALIK_Valuation_Study_11-07-2026_public.pdf?v=20260713b",
      biblio:"files/SALIK_Source_Register_11-07-2026.docx?v=20260713b"
    }
  },
  DIB: {
    name: "Dubai Islamic Bank",
    nameAr: "بنك دبي الإسلامي",
    code: "DFM:DIB",
    spot: 7.35,
    spotDate: "close 24 Jul 2026",
    ccy: "AED",
    fair: { bear: 8.14, base: 10.18, full: 11.20 },      // 11 Jul 2026 — five-lens weighted central 10.18 (+32% vs spot 7.72). Lenses: DDM (primary, 30%) 10.90, residual income (20%) 11.20, FCFE equity DCF (15%) 10.44, relative multiples same-day-anchored on ADCB (20%) 8.14, normalized through-cycle (15%) 9.86. bear/full = relative lens / residual-income lens. Ke 10.57% (rf 4.70% + β1.00×ERP4.87% + 1.0pt war adder). MONTE CARLO FAILED calibration on this name (skill score −0.025 vs random walk, robust across every resampling scheme; study §3.1) — §3 is an illustrative volatility map only, no forecast published. Swing factors: the net profit margin path, the pace of cost-of-risk normalization off a tripled Q1-26 print, and whether the Iran-war ceasefire holds. UAE's largest Islamic bank; dividend cut 45→35 fils Feb-2026.
    dist: {
      t20: { label:"1 month",   p5:6.65, p25:7.09, p50:7.37, p75:7.67, p95:8.16, resolve:"2026-08-24" },
      t60: { label:"3 months",  p5:6.13, p25:6.90, p50:7.42, p75:7.98, p95:8.99, resolve:"2026-10-26" }
    },
    hz: { h1:20, h3:63, l1:"1 month", l3:"3 months", cal:true },
    touch: [ /* descending high -> low; illustrative only, calibration FAILED */
      [8.88, 1, 10], [10.20, 0, 1], [8.63, 1, 16], [7.76, 32, 60], [7.59, 52, 73], [7.40, 81, 90], [7.09, 44, 66]
    ],
    levels: { res:[7.71, 7.97, 9.33], sup:[7.19, 6.91, 6.08] },
    tech: {
      trend: "Trading below the whole moving-average stack, under a falling 200-day",
      summary: "The price closed 7.35 below a falling 20-day (7.53), a rising 50-day (7.48) and a falling 200-day (8.48). Momentum is neutral: RSI(14) is ~44 and the daily ATR near 0.15 (~2.0%) points to a normal tape. MACD (12\u00b726\u00b79) is negative and still falling (\u22120.05 / \u22120.02 / \u22120.03). Over the last year it has ranged 6.97\u201310.20; the last close sits 28% below that high and 5% above that low.",
      bull: "A daily close back above 7.71 would clear the nearest resistance and open the 9.33 zone.",
      bear: "A close below 7.19 would break the nearest support and open the 6.08 zone."
    },
    asof: {
      mc:   { data:"2026-07-24", computed:"2026-07-28" },
      tech: { data:"2026-07-24", computed:"2026-07-29" }
    },
    files: {
      study: "files/DIB_Valuation_Study_11-07-2026_public.docx?v=0711g",
      model: "files/DIB_Valuation_Model_11072026_public.xlsx?v=0711g",
      pdf:   "files/DIB_Valuation_Study_11-07-2026_public.pdf?v=0711g"
    }
  },
  "2POINTZERO": {
    name: "Two Point Zero Group",
    nameAr: "مجموعة تو بوينت زيرو",
    code: "ADX:2POINTZERO",
    spot: 2.06,
    spotDate: "close 24 Jul 2026",
    ccy: "AED",
    fair: { bear: 1.55, base: 1.91, full: 2.27 },      // 11 Jul 2026 — four-lens weighted central 1.91 (-11.7% vs spot 2.16). Lenses: sum-of-the-parts (primary, 45%) 1.95 — operating businesses marked on their own earnings, investment portfolio at management's mark less a 25% opacity discount, cash at par, less a 7.5% structural discount; DCF on the operating legs + portfolio (ceiling, 15%) 2.39 (TV 81% of operating EV, disclosed); relative on reported earnings with a normalised mark contribution (25%) 1.85; underlying earnings, no marks at all (floor, 15%) 1.39. THE CRUX: the AED 58.7bn investment portfolio is carried against AED 48.0bn invested — a AED 10.7bn gain. But the 7.29% TAQA stake sold on 11-Jun-2026 (9,095,702,934 shares at AED 2.37) was worth ~AED 21.6bn against AED 10bn paid. Strip it out and the REST of the portfolio — now entirely unlisted — is carried AED 0.9bn BELOW cost. The entire mark-up was one listed stake, and it has been sold, with ~AED 14.4bn of the proceeds redeployed into unlisted assets (Traverse, Mopani, Alphamin, ISEM). Operating economics are disclosed and modest: gross margin 30%, G&A 18% of revenue → ~12% operating margin — NOT the 25% that a blended adjusted-EBITDA figure implies, because that figure has AED 1.2bn/qtr of portfolio income inside it. Tax modelled at the statutory 15% DMTT floor (no phase-in exists). Attributable ratio 84.2%, derived from the PUBLISHED Q1-26 EPS of AED 0.056. Beta assumed 1.0 (regression failed our usability test; no downloadable ADX index series), sensitised 0.8–1.3.
    dist: {
      t20: { label:"1 month",   p5:1.75, p25:1.94, p50:2.07, p75:2.20, p95:2.43, resolve:"2026-08-24" },
      t60: { label:"3 months",  p5:1.53, p25:1.85, p50:2.08, p75:2.34, p95:2.84, resolve:"2026-10-26" }
    },
    hz: { h1:20, h3:63, l1:"1 month", l3:"3 months", cal:true },
    touch: [ /* descending high -> low; P(touch) 1-month %, 3-month % */
      [2.60, 2, 19], [2.40, 10, 37], [2.20, 42, 67], [2.00, 65, 80], [1.90, 32, 58], [1.80, 13, 38]
    ],
    levels: { res:[2.09, 2.15, 2.26], sup:[1.95, 1.92, 1.87] },
    tech: {
      trend: "Trading below the whole moving-average stack, under a falling 200-day",
      summary: "The price closed 2.06 below a falling 20-day (2.13), a flat 50-day (2.13) and a falling 200-day (2.36). Momentum is soft: RSI(14) is ~39 and the daily ATR near 0.05 (~2.4%) points to a normal tape. MACD (12\u00b726\u00b79) is negative and still falling (\u22120.02 / \u22120.01 / \u22120.01). Over the last year it has ranged 1.63\u20133.42; the last close sits 40% below that high and 26% above that low.",
      bull: "A daily close back above 2.09 would clear the nearest resistance and open the 2.26 zone.",
      bear: "A close below 1.95 would break the nearest support and open the 1.87 zone."
    },
    asof: {
      mc:   { data:"2026-07-24", computed:"2026-07-29" },
      tech: { data:"2026-07-24", computed:"2026-07-29" }
    },
    files: {
      study: "files/2POINTZERO_Valuation_Study_11-07-2026_public.docx?v=20260711f",
      model: "files/2POINTZERO_Valuation_Model_11072026_public.xlsx?v=20260711f",
      pdf:   "files/2POINTZERO_Valuation_Study_11-07-2026_public.pdf?v=20260711f",
      biblio:"files/2POINTZERO_Bibliography_11-07-2026.docx?v=20260711f"
    }
  },
  EAND: {
    name: "e& (Emirates Telecommunications Group)",
    nameAr: "إي آند (مجموعة الإمارات للاتصالات)",
    code: "ADX:EAND",
    spot: 20.08,
    spotDate: "close 24 Jul 2026",
    ccy: "AED",
    fair: { bear: 17.61, base: 22.72, full: 28.75 },      // 11 Jul 2026 — four-lens weighted central 22.72 (+15.5% vs spot 19.66). Lenses: FCFF DCF + sourced stakes-and-claims bridge (primary, 35%) 28.38 (TV 79% of EV, disclosed; core EV under the production UAE Monte-Carlo panel fit does not feed this lens), dividend discount (policy lens, 25%) 17.03, relative EV/EBITDA through the same bridge (20%) 23.72, normalized earnings (20%) 18.90. bear/full = weighted bear/bull. The crux is the 2027 UAE federal royalty reset (current 38%+9% regime expires 31-Dec-2026, undecided): each 4pp of royalty ≈ AED 1.1/share. Same-day event: 10-Jul-2026 e& agreed to sell its entire Vodafone stake for AED 21.8bn gross (~4.7bn net cash), pending regulatory approvals — carried at deal value, dual-framed against the undisturbed mark. Beta assumed 1.0 (regression inaccessible; no downloadable ADX General Index series found after two independent attempts), sensitised 0.8–1.3.
    dist: {
      t20: { label:"1 month",   p5:18.20, p25:19.37, p50:20.14, p75:20.94, p95:22.25, resolve:"2026-08-24" },
      t60: { label:"3 months",  p5:16.98, p25:18.94, p50:20.27, p75:21.70, p95:24.23, resolve:"2026-10-26" }
    },
    hz: { h1:20, h3:63, l1:"1 month", l3:"3 months", cal:true },
    touch: [ /* descending high -> low; P(touch) 1-month %, 3-month % */
      [22.00, 11, 37], [21.00, 39, 64], [20.00, 82, 89], [19.00, 27, 51], [18.00, 6, 23], [17.00, 1, 9]
    ],
    levels: { res:[20.52, 20.91, 21.53], sup:[19.32, 18.88, 17.32] },
    tech: {
      trend: "Trading above the whole moving-average stack, on a rising 200-day; fresh golden-cross",
      summary: "The price closed 20.08 above a rising 20-day (19.93), a rising 50-day (19.26) and a rising 200-day (19.19). Momentum is neutral: RSI(14) is ~56 and the daily ATR near 0.40 (~2.0%) points to a normal tape. MACD (12\u00b726\u00b79) is above zero but rolling over (+0.24 / +0.28 / \u22120.05). The 50-day crossed above the 200-day 7 sessions ago \u2014 a fresh golden-cross, a momentum-regime change rather than noise inside an intact trend. Over the last year it has ranged 17.40\u201321.60; the last close sits 7% below that high and 15% above that low.",
      bull: "A daily close back above 20.52 would clear the nearest resistance and open the 21.53 zone.",
      bear: "A close below 19.32 would break the nearest support and open the 17.32 zone."
    },
    asof: {
      mc:   { data:"2026-07-24", computed:"2026-07-28" },
      tech: { data:"2026-07-24", computed:"2026-07-29" }
    },
    files: {
      study: "files/EAND_Valuation_Study_10-07-2026_public.docx?v=0711a",
      model: "files/EAND_Valuation_Model_10072026_public.xlsx?v=0711a",
      pdf:   "files/EAND_Valuation_Study_10-07-2026_public.pdf?v=0711a"
    }
  },
  ADCB: {
    name: "Abu Dhabi Commercial Bank",
    nameAr: "بنك أبوظبي التجاري",
    code: "ADX:ADCB",
    spot: 14.42,
    spotDate: "close 24 Jul 2026",
    ccy: "AED",
    fair: { bear: 14.3, base: 19.7, full: 23.3 },      // 10 Jul 2026 — five-lens weighted central 19.7 (+31% vs spot 15.10). Lenses: DDM (primary, 30%) 21.2, residual income (multi-period, 20%) 22.7, FCFE equity DCF (15%) 23.3, relative multiples (20%) 15.9, normalized through-cycle (15%) 14.3. bear/full = normalized floor / FCFE ceiling. War-adjusted Ke 10.57% (rf 4.70% + β1.0×ERP4.87% + 1.0pt war adder). Swing factors: the NIM path through the CBUAE/Fed easing cycle, whether the ~16% ROE persists, and Gulf de-escalation. Third-largest UAE bank; AED 6.1bn rights issue closed Dec-2025.
    dist: {
      t20: { label:"1 month",   p5:12.55, p25:13.70, p50:14.46, p75:15.27, p95:16.63, resolve:"2026-08-24" },
      t60: { label:"3 months",  p5:11.36, p25:13.24, p50:14.56, p75:16.01, p95:18.69, resolve:"2026-10-26" }
    },
    hz: { h1:20, h3:63, l1:"1 month", l3:"3 months", cal:true },
    touch: [ /* descending high -> low; P(touch) 1-month %, 3-month % */
      [17.20, 4, 22], [16.40, 11, 36], [15.80, 23, 50], [14.40, 86, 92], [13.90, 55, 72], [13.30, 26, 50]
    ],
    levels: { res:[15.07, 15.29, 15.77], sup:[14.13, 13.42, 12.85] },
    tech: {
      trend: "Consolidating below the near-term moving averages, above a flat 200-day",
      summary: "The price closed 14.42 above a rising 50-day (14.17) and a flat 200-day (14.28), but below a falling 20-day (14.55). Momentum is neutral: RSI(14) is ~50 and the daily ATR near 0.38 (~2.6%) points to a normal tape. MACD (12\u00b726\u00b79) is above zero but rolling over (+0.00 / +0.07 / \u22120.07). Over the last year it has ranged 11.58\u201316.60; the last close sits 13% below that high and 25% above that low.",
      bull: "A daily close back above 15.07 would clear the nearest resistance and open the 15.77 zone.",
      bear: "A close below 14.13 would break the nearest support and open the 12.85 zone."
    },
    asof: {
      mc:   { data:"2026-07-24", computed:"2026-07-28" },
      tech: { data:"2026-07-24", computed:"2026-07-29" }
    },
    files: {
      study: "files/ADCB_Valuation_Study_10-07-2026_public.docx?v=0711a",
      model: "files/ADCB_Valuation_Model_10072026_public.xlsx?v=0711a",
      pdf:   "files/ADCB_Valuation_Study_10-07-2026_public.pdf?v=0711a"
    }
  },
  ELM: {
    name: "Elm Company",
    nameAr: "شركة علم",
    code: "TADAWUL:7203",
    spot: 666.00,
    spotDate: "close 26 Jul 2026",
    ccy: "SAR",
    fair: { bear: 530, base: 620, full: 720 },      // 10 Jul 2026 — weighted central ~620 (−5.8% vs spot 658.50): roughly fairly valued, a slight premium. Lenses: DCF (primary, β=1.0 neutral, WACC 10.5%, g 4%, 40%) 576, forward P/E (24× 2025e EPS 28.6, 30%) 686, EV/EBITDA (18–20× 2025e, 25%) ~625, MC 3-month median 664. bear/full = football-field range 530–720. The crux is the discount rate: 77% of DCF value is terminal, so a low-beta government-defensive read (β 0.7, WACC 9%) gives ~750, neutral (β 1.0) ~576, and a high-beta post-crash re-rate (β 1.6, WACC 13.5%) ~396. Second swing: registry-exclusivity durability behind the ~46%-margin Digital Business.
    dist: {
      t20: { label:"1 month",   p5:557.58, p25:622.90, p50:667.90, p75:716.95, p95:801.78, resolve:"2026-08-26" },
      t60: { label:"3 months",  p5:500.81, p25:600.12, p50:673.56, p75:755.15, p95:905.12, resolve:"2026-10-26" }
    },
    hz: { h1:22, h3:62, l1:"1 month", l3:"3 months", cal:true },
    touch: [ /* descending high -> low */
      [757.30, 20, 43], [724.40, 37, 59], [691.40, 64, 79], [625.60, 47, 64], [592.60, 22, 43], [559.70, 9, 26]
    ],
    levels: { res:[676.22, 724.44, 883.07], sup:[659.50, 632, 562.50] },
    tech: {
      trend: "Mixed against the moving-average stack, below a falling 200-day",
      summary: "The price closed 666.00 below a rising 50-day (685.68) and a falling 200-day (715.77), but above a falling 20-day (663.67). Momentum is neutral: RSI(14) is ~49 and the daily ATR near 16.28 (~2.4%) points to a normal tape. MACD (12\u00b726\u00b79) is below zero but turning up (\u22125.32 / \u22127.43 / +2.11). Over the last year it has ranged 504.50\u2013972.00; the last close sits 31% below that high and 32% above that low.",
      bull: "A daily close back above 676.22 would clear the nearest resistance and open the 883.07 zone.",
      bear: "A close below 659.50 would break the nearest support and open the 562.50 zone."
    },
    asof: {
      mc:   { data:"2026-07-26", computed:"2026-07-28" },
      tech: { data:"2026-07-26", computed:"2026-07-29" }
    },
    files: {
      study: "files/Elm_Valuation_Study_10-07-2026_public.docx?v=0710b",
      model: "files/Elm_Valuation_Model_10-07-2026_public.xlsx?v=0710b",
      pdf:   "files/Elm_Valuation_Study_10-07-2026_public.pdf?v=0710b"
    }
  },
  ALPHADHABI: {
    name: "Alpha Dhabi Holding",
    nameAr: "ألفا ظبي القابضة",
    code: "ADX:ALPHADHABI",
    spot: 7.30,
    spotDate: "close 24 Jul 2026",
    ccy: "AED",
    fair: { bear: 5.95, base: 7.13, full: 8.63 },      // 10 Jul 2026, reweighted 11 Jul 2026 — weighted central 7.13 (−13% vs spot 8.22). Holdco SOTP/NAV primary: four listed stakes at ADX marks (Aldar 31.63% = AED 20.5bn, NMDC 76.68% = 14.4bn, PureHealth 35.06% = 8.6bn, NCTH 73.73% = 2.4bn) + Trojan 51% at the ADQ transaction buyer-outlay mark (5.2bn; seller-note framing 3.71bn carried as a sensitivity) + residual audited book → NAV 7.44/sh at par, 6.32 at a 15% holdco discount (55% weight, raised from 45% on 11 Jul 2026). Consolidated FCFF DCF 11.72 = a multi-year ceiling (80% TV, ΔWC absorption) at 15%; look-through relative 8.07 cut to 15% weight (from 25%, external-audit double-count flag upheld); dividend-policy DDM 4.55 at 15%. The crux: spot pays ~+10% ABOVE undiscounted NAV — the premium is the trade. bear/full = weighted bear/bull.
    dist: {
      t20: { label:"1 month",   p5:6.35, p25:6.93, p50:7.32, p75:7.73, p95:8.42, resolve:"2026-08-24" },
      t60: { label:"3 months",  p5:5.69, p25:6.67, p50:7.37, p75:8.14, p95:9.57, resolve:"2026-10-26" }
    },
    hz: { h1:20, h3:63, l1:"1 month", l3:"3 months", cal:true },
    touch: [ /* descending high -> low */
      [9.50, 1, 9], [8.84, 3, 20], [8.50, 7, 30], [7.44, 72, 85], [7.00, 51, 71], [6.58, 17, 42]
    ],
    levels: { res:[8.30, 8.55, 9.03], sup:[7.14, 7, 6.84] },
    tech: {
      trend: "Trading below the whole moving-average stack, under a falling 200-day",
      summary: "The price closed 7.30 below a falling 20-day (7.79), a flat 50-day (7.62) and a falling 200-day (8.64). Momentum is soft: RSI(14) is ~35 and the daily ATR near 0.19 (~2.6%) points to a normal tape. MACD (12\u00b726\u00b79) is negative and still falling (\u22120.12 / \u22120.03 / \u22120.09). Over the last year it has ranged 6.75\u201312.60; the last close sits 42% below that high and 8% above that low.",
      bull: "A daily close back above 8.30 would clear the nearest resistance and open the 9.03 zone.",
      bear: "A close below 7.14 would break the nearest support and open the 6.84 zone."
    },
    asof: {
      mc:   { data:"2026-07-24", computed:"2026-07-28" },
      tech: { data:"2026-07-24", computed:"2026-07-29" }
    },
    files: {
      study: "files/ALPHADHABI_Valuation_Study_10-07-2026_public.docx?v=0711c",
      model: "files/ALPHADHABI_Valuation_Model_10-07-2026_public.xlsx?v=0711c",
      pdf:   "files/ALPHADHABI_Valuation_Study_10-07-2026_public.pdf?v=0711c"
    }
  },
  EXTRA: {
    name: "United Electronics Company (eXtra)",
    nameAr: "الشركة المتحدة للإلكترونيات (إكسترا)",
    code: "TADAWUL:4003",
    spot: 68.50,
    spotDate: "close 26 Jul 2026",
    ccy: "SAR",
    fair: { bear: 66, base: 81, full: 92 },      // 10 Jul 2026 — weighted central 81 (+19% vs spot 68.10). Split-legs SOTP: retail operating-co DCF (SAR 65/sh, net-cash, Ke ~9.5%) + Tasheel, the 68.75%-owned captive consumer-finance lender (SAR 25/sh, equity book × justified P/B). SOTP 90 (primary), relative P/E 12× 75, Monte-Carlo 3-month median 68. bear/full = weighted bear/bull of the football field. Crux: the retail discount rate (regressed β 0.55 on a short window → 0.80 base, sensitized 0.55–1.0) and the Tasheel multiple. At a 52-week low with RSI 27.
    dist: {
      t20: { label:"1 month",   p5:61.75, p25:65.93, p50:68.71, p75:71.65, p95:76.54, resolve:"2026-08-26" },
      t60: { label:"3 months",  p5:56.29, p25:63.88, p50:69.25, p75:75.01, p95:85.14, resolve:"2026-10-26" }
    },
    hz: { h1:22, h3:62, l1:"1 month", l3:"3 months", cal:true },
    touch: [ /* descending high -> low */
      [81.70, 1, 15], [74.90, 14, 44], [71.50, 44, 69], [64.70, 29, 55], [61.30, 6, 30], [54.50, 0, 6]
    ],
    levels: { res:[79.36, 81.02, 86.37], sup:[67.50, 66, 64] },
    tech: {
      trend: "Trading below the whole moving-average stack, under a falling 200-day",
      summary: "The price closed 68.50 below a falling 20-day (70.19), a falling 50-day (74.02) and a falling 200-day (82.87). Momentum is soft: RSI(14) is ~34 and the daily ATR near 0.98 (~1.4%) points to an orderly tape. MACD (12\u00b726\u00b79) is below zero but turning up (\u22121.74 / \u22121.84 / +0.10). Over the last year it has ranged 67.50\u201393.50; the last close sits 27% below that high and 1% above that low.",
      bull: "A daily close back above 79.36 would clear the nearest resistance and open the 86.37 zone.",
      bear: "A close below 67.50 would break the nearest support and open the 64.00 zone."
    },
    asof: {
      mc:   { data:"2026-07-26", computed:"2026-07-28" },
      tech: { data:"2026-07-26", computed:"2026-07-29" }
    },
    files: {
      study: "files/eXtra_Valuation_Study_10-07-2026_public.docx?v=0710d",
      model: "files/eXtra_Valuation_Model_10-07-2026_public.xlsx?v=0710d",
      pdf:   "files/eXtra_Valuation_Study_10-07-2026_public.pdf?v=0710d"
    }
  },
  ALINMA: {
    name: "Alinma Bank",
    nameAr: "مصرف الإنماء",
    code: "TADAWUL:1150",
    spot: 23.80,
    spotDate: "close 26 Jul 2026",
    ccy: "SAR",
    fair: { bear: 19.90, base: 27.32, full: 31.23 },      // 10 Jul 2026 — weighted central 27.32 (+13.8% vs spot 24.00). Lenses: DDM (primary, terminal payout forced consistent 1−g/ROE_t, 35%) 31.23, residual income (multi-period build, 20%) 28.41, FCFE (equity DCF, 15%) 23.79, relative multiples (20%) 25.68, normalized floor (β=1, CDS ERP, 10%) 19.90. bear/full = normalized floor / DDM ceiling. The crux is the cost of equity: regressed β 0.74 (short window) → Ke 8.5–9.0%; β=1.0 → 9.8–10.5%; base Ke 9.46% is the disclosed four-corner mean, and the market's ~2.1× common book implies ~9.2% — inside the band. Second swing: the NIM glide (3.55% FY25 → 3.40%) through the SAMA/Fed easing cycle.
    dist: {
      t20: { label:"1 month",   p5:21.87, p25:23.08, p50:23.87, p75:24.71, p95:26.09, resolve:"2026-08-26" },
      t60: { label:"3 months",  p5:20.33, p25:22.53, p50:24.05, p75:25.67, p95:28.45, resolve:"2026-10-26" }
    },
    hz: { h1:22, h3:62, l1:"1 month", l3:"3 months", cal:true },
    touch: [ /* descending high -> low */
      [27.60, 1, 14], [26.40, 5, 29], [25.20, 24, 55], [22.80, 32, 57], [21.60, 5, 26], [20.40, 1, 9]
    ],
    levels: { res:[24.36, 25.39, 26.04], sup:[23.26, 22.06, 20.19] },
    tech: {
      trend: "Consolidating below the near-term moving averages, above a rising 200-day",
      summary: "The price closed 23.80 below a falling 20-day (24.16) and a flat 50-day (24.31), but above a rising 200-day (22.88). Momentum is neutral: RSI(14) is ~42 and the daily ATR near 0.32 (~1.3%) points to an orderly tape. MACD (12\u00b726\u00b79) is negative and still falling (\u22120.19 / \u22120.13 / \u22120.06). Over the last year it has ranged 19.95\u201325.53; the last close sits 7% below that high and 19% above that low.",
      bull: "A daily close back above 24.36 would clear the nearest resistance and open the 26.04 zone.",
      bear: "A close below 23.26 would break the nearest support and open the 20.19 zone."
    },
    asof: {
      mc:   { data:"2026-07-26", computed:"2026-07-28" },
      tech: { data:"2026-07-26", computed:"2026-07-29" }
    },
    files: {
      study: "files/Alinma_Valuation_Study_10-07-2026_public.docx?v=0710a",
      model: "files/Alinma_Valuation_Model_10072026_public.xlsx?v=0710a",
      pdf:   "files/Alinma_Valuation_Study_10-07-2026_public.pdf?v=0710a"
    }
  },
  GBCO: {
    name: "GB Corp (Ghabbour)",
    nameAr: "جي بي كورب (غبور)",
    code: "EGX:GBCO",
    spot: 31.31,
    spotDate: "close 22 Jul 2026",
    ccy: "EGP",
    fair: { bear: 23.3, base: 35.7, full: 51.0 },      // AMENDED 09 Jul 2026 (replaces the prior 08-Jul draft; same study cycle, corrected leg build) — weighted central 35.7 (+14% vs spot 31.25). GB Corp's own 9-June-2026 press release ("MNT-Halan ... Closes Capital Increase Round Led by Al Ahly Capital Holding") confirms the current stake directly: "GB Corp's ownership stake in MNT-Halan will be adjusted to 41.61%, compared to 42.58% prior to the transaction" — a dated, current, company-confirmed figure, replacing both the original unsourced ~20% placeholder and the interim 42.58% correction. Four lenses: split-the-legs SOTP (primary) 38.4 (Auto FCFF DCF + GB Capital adjusted book ×1.0 + MNT-Halan at the confirmed 41.61% × the Jun-26 USD 1.4bn round, less a 10% complexity discount), pre-discount NAV 42.6, relative multiples 28.9 (floor, stake-blind), normalized mid-cycle earnings 32.9 (also stake-blind); blend 40/15/20/25. THE REAL OPEN QUESTION: with the stake now confirmed, applying it to the round's valuation implies MNT-Halan alone is worth ~73% of GB Corp's entire market cap — a genuine puzzle, not a sourcing gap. Either the market applies a far steeper discount to this private mark than this study's 10%, or GB Corp is meaningfully mispriced. Treat 35.7 as the read if the round's valuation holds at face value; the stake-blind relative/normalized lenses (28.9–32.9) are the more conservative anchor if you believe the market's skepticism is warranted. Swing factors, in order: the discount applied to the MNT-Halan mark (the stake itself is no longer in question), Auto working-capital release, the CBE rate path. MC PASSES the calibration back-test with the secular drift ON (CRPS skill +3.2% non-overlapping, +9.6% monthly; zero drift FAILED) — entirely unaffected by any of this, since the engine prices the stock's own path, not the SOTP.
    levels: { res:[31.61, 32.49, 34.20], sup:[28.64, 25.36, 23.99] },   // 19 Jul 2026 — computed from own OHLC (SMA20/50/200, 52w range, swing points); technical-only
    dist: {
      t20: { label:"1 month",   p5:25.55, p25:29.31, p50:31.78, p75:34.47, p95:39.54, resolve:"2026-08-23" },
      t60: { label:"3 months",  p5:22.08, p25:28.34, p50:32.80, p75:37.86, p95:48.54, resolve:"2026-10-22" }
    },
    hz: { h1:20, h3:61, l1:"1 month", l3:"3 months", cal:true },
    touch: [ /* level, P(touch) 1-month %, 3-month % — descending; up-levels then down-levels */
      [40.00, 7, 30], [38.00, 13, 40], [36.00, 25, 54], [34.00, 46, 71], [32.00, 78, 89], [30.00, 59, 73], [28.00, 27, 48], [26.00, 11, 30]
    ],
    levels: { res:[31.70, 32.30, 33.40], sup:[29.96, 28.20, 26.73] },
    tech: {
      trend: "Consolidating below the near-term moving averages, above a rising 200-day",
      summary: "The price closed 31.31 above a rising 50-day (29.25) and a rising 200-day (27.25), but below a rising 20-day (31.67). Momentum is neutral: RSI(14) is ~53 and the daily ATR near 1.23 (~3.9%) points to a lively tape. MACD (12\u00b726\u00b79) is above zero but rolling over (+0.81 / +0.95 / \u22120.14). Over the last year it has ranged 19.10\u201334.20; the last close sits 8% below that high and 64% above that low.",
      bull: "A daily close back above 31.61 would clear the nearest resistance and open the 34.20 zone.",
      bear: "A close below 28.64 would break the nearest support and open the 23.99 zone."
    },
    asof: {
      mc:   { data:"2026-07-22", computed:"2026-07-28" },
      tech: { data:"2026-07-22", computed:"2026-07-29" }
    },
    files: {
      study: "files/GBCO_Valuation_Study_08-07-2026_public.docx?v=0709c",
      model: "files/GBCO_Valuation_Model_08072026_public.xlsx?v=0709c",
      pdf:   "files/GBCO_Valuation_Study_08-07-2026_public.pdf?v=0709c"
    }
  },
  EMAARDEV: {
    name: "Emaar Development PJSC",
    nameAr: "إعمار للتطوير",
    code: "DFM:EMAARDEV",
    spot: 13.16,
    spotDate: "close 24 Jul 2026",
    ccy: "AED",
    fair: { bear: 12.88, base: 17.29, full: 22.76 },      // 08 Jul 2026 — weighted central 17.29 (+21% vs spot 14.26). Four lenses: RNAV / split-NAV (primary) 17.56, going-concern DCF (exit-multiple terminal, not Gordon) 18.43, relative multiples 15.75 (floor), property-cycle earnings 16.88; blend 40/20/15/25. bear/full = weighted bear/bull of the football field. Development legs carry no terminal value; swing factors are the Dubai property cycle, the sustainable development margin and the net-cash mark. A naive Gordon-perpetuity DCF would imply ~27 (disclosed, not used). MC INDICATIVE: the §3 engine (run drift-on for this name) MATCHES — ties — its zero-drift random-walk benchmark in the calibration back-test (CRPS skill ≈ 0, CI spans zero) with a well-calibrated PIT; no demonstrated edge, but not a failed calibration.
    dist: {
      t20: { label:"1 month",   p5:11.46, p25:12.50, p50:13.20, p75:13.94, p95:15.16, resolve:"2026-08-24" },
      t60: { label:"3 months",  p5:10.16, p25:11.99, p50:13.29, p75:14.73, p95:17.41, resolve:"2026-10-26" }
    },
    hz: { h1:20, h3:63, l1:"1 month", l3:"3 months", cal:true },
    touch: [ /* descending high -> low; P(touch) 1-month %, 3-month % */
      [18.00, 0, 6], [17.00, 1, 11], [16.00, 2, 21], [15.00, 10, 38], [14.00, 39, 65], [13.00, 77, 87], [12.00, 21, 48]
    ],
    levels: { res:[13.81, 14.42, 15.41], sup:[13.01, 12.02, 11] },
    tech: {
      trend: "Trading below the whole moving-average stack, under a falling 200-day",
      summary: "The price closed 13.16 below a falling 20-day (13.63), a falling 50-day (13.91) and a falling 200-day (15.14). Momentum is neutral: RSI(14) is ~40 and the daily ATR near 0.35 (~2.7%) points to a normal tape. MACD (12\u00b726\u00b79) is negative and still falling (\u22120.31 / \u22120.24 / \u22120.06). Over the last year it has ranged 12.05\u201320.70; the last close sits 36% below that high and 9% above that low.",
      bull: "A daily close back above 13.81 would clear the nearest resistance and open the 15.41 zone.",
      bear: "A close below 13.01 would break the nearest support and open the 11.00 zone."
    },
    asof: {
      mc:   { data:"2026-07-24", computed:"2026-07-28" },
      tech: { data:"2026-07-24", computed:"2026-07-29" }
    },
    files: {
      study: "files/EMAARDEV_Valuation_Study_08-07-2026_public.docx?v=0708a",
      model: "files/EMAARDEV_Valuation_Model_08072026_public.xlsx?v=0708a",
      pdf:   "files/EMAARDEV_Valuation_Study_08-07-2026_public.pdf?v=0708a"
    }
  },
  ISPH: {
    name: "Ibnsina Pharma",
    nameAr: "\u0627\u0628\u0646 \u0633\u064a\u0646\u0627 \u0641\u0627\u0631\u0645\u0627",
    code: "EGX:ISPH",
    spot: 11.73,
    spotDate: "close 22 Jul 2026",
    ccy: "EGP",
    fair: { bear: 12.85, base: 17.78, full: 22.68 },      // 7 Jul 2026 \u2014 weighted central 17.78 (+52% vs spot 11.67). Four lenses: DCF (primary) 19.79, relative EV/EBITDA 16.71, normalized earnings 17.98, dividend-yield floor 11.00; blend 45/25/20/10. bear/full = weighted bear/bull of the football field. Swing: the thin net margin normalising as the CBE rate path eases finance costs and the drug-re-pricing cycle feeds through \u2014 on ~EGP 76.6bn FY25 revenue at an ~8% gross / ~5% EBITDA / ~1.2% net margin with a near-zero cash-conversion cycle. INDICATIVE: the \u00a73 Monte-Carlo engine did NOT beat its zero-drift random-walk benchmark in the calibration back-test (CRPS skill < 0 on every scheme) \u2014 the price map is illustrative only, not a skill-validated forecast.
    dist: {
      t20: { label:"1 month",   p5:10.01, p25:11.16, p50:11.90, p75:12.70, p95:14.16, resolve:"2026-08-23" },
      t60: { label:"3 months",  p5:8.89, p25:10.90, p50:12.28, p75:13.81, p95:16.92, resolve:"2026-10-22" }
    },
    hz: { h1:20, h3:61, l1:"1 month", l3:"3 months", cal:true },
    touch: [ /* descending high -> low; P(touch) 1-month %, 3-month % */
      [13.50, 16, 47], [12.75, 38, 67], [12.25, 61, 81], [12.00, 75, 88], [11.50, 69, 80], [11.00, 38, 58], [10.50, 19, 40]
    ],
    levels: { res:[12.21, 12.72, 13.72], sup:[11.33, 10.60, 10.05] },
    tech: {
      trend: "Mixed against the moving-average stack, above a rising 200-day",
      summary: "The price closed 11.73 above a falling 20-day (11.59) and a rising 200-day (11.29), but below a rising 50-day (11.78). Momentum is neutral: RSI(14) is ~52 and the daily ATR near 0.29 (~2.5%) points to a normal tape. MACD (12\u00b726\u00b79) is below zero but turning up (\u22120.07 / \u22120.08 / +0.01). Over the last year it has ranged 9.37\u201313.72; the last close sits 15% below that high and 25% above that low.",
      bull: "A daily close back above 12.21 would clear the nearest resistance and open the 13.72 zone.",
      bear: "A close below 11.33 would break the nearest support and open the 10.05 zone."
    },
    asof: {
      mc:   { data:"2026-07-22", computed:"2026-07-28" },
      tech: { data:"2026-07-22", computed:"2026-07-29" }
    },
    files: {
      study: "files/ISPH_Valuation_Study_07-07-2026_public.docx?v=0707a",
      model: "files/ISPH_Valuation_Model_07072026_public.xlsx?v=0707a",
      pdf:   "files/ISPH_Valuation_Study_07-07-2026_public.pdf?v=0707a"
    }
  },
  RELIANCE: {
    name: "Reliance Industries Limited",
    nameAr: "ريلاينس إندستريز",
    code: "NSE:RELIANCE",
    spot: 1272,
    spotDate: "close 28 Jul 2026",
    ccy: "INR",
    fair: { bear: 1112, base: 1395, full: 1719 },      // 6 Jul 2026 — weighted central 1,395 (+6% vs spot 1,321.30). Four lenses: sum-of-the-parts (primary) 1,342, consolidated DCF 1,359, relative multiples 1,322 (floor), normalized earnings 1,552 (ceiling); weights 40/20/15/25. bear/full = weighted bear/bull of the football field. Swing: crystallising the unlisted digital (Jio) and retail value via the Jio Platforms IPO (DRHP filed 19 Jun 2026), the O2C refining/petrochemical margin cycle, and the ~5% holding-company discount.
    dist: {
    t20: { label: "1 month", p5: 1144.56, p25: 1227.46, p50: 1278.17, p75: 1331.34, p95: 1427.61, resolve: "2026-08-28" },
    t60: { label: "3 months", p5: 1060.54, p25: 1201.62, p50: 1293.19, p75: 1390.72, p95: 1576.35, resolve: "2026-10-28" }
  },
    hz: { h1:22, h3:62, l1:"1 month", l3:"3 months", cal:true },
    touch: [[1550,1,10],[1500,2,16],[1450,5,25],[1400,13,39],[1350,31,58],[1300,66,82],[1250,66,78],[1200,27,49],[1150,9,28]],
    levels: { res:[1366, 1418, 1592], sup:[1303, 1259, 1200] },
    tech: {
      trend: "Below the 50-, 100- and 200-day moving averages but holding the 20-day; RSI neutral, MACD turning up — a corrective tape stabilising off the low",
      summary: "The tape is corrective but stabilising rather than trending down. Reliance has retraced from a January-2026 high near \u20b91,600 to the low-\u20b91,300s and sits below its 50-day (\u20b91,341), 100-day (\u20b91,366) and 200-day (\u20b91,418) moving averages, but has reclaimed the 20-day (\u20b91,303). RSI(14) near 52 is neutral; MACD is negative but the histogram has turned positive (\u22125.90 line / \u22128.69 signal / +2.79 histogram) as the MACD line crosses back above its signal \u2014 an early momentum turn off the correction low. Realized 252-day volatility is about 21%, and the YZ-HAR engine reads the current 60-day regime near 25%.",
      bull: "A daily close back above the \u20b91,341 fifty-day and the \u20b91,366 hundred-day would confirm the turn and open the \u20b91,418 two-hundred-day; reclaiming \u20b91,592 would need the Jio IPO to crystallise or an O2C-margin surprise.",
      bear: "A close back below the \u20b91,303 twenty-day and the \u20b91,259 fifty-two-week low would reopen the downtrend toward the \u20b91,200 shelf, the main driver of the left tail being an O2C-margin squeeze or a crude-spike shock."
    },
    files: {
      study: "files/RELIANCE_Valuation_Study_06-07-2026_public.docx?v=0706i",
      model: "files/RELIANCE_Valuation_Model_06-07-2026_public.xlsx?v=0706i",
      pdf:   "files/RELIANCE_Valuation_Study_06-07-2026_public.pdf?v=0706i"
    }
  },
  NVDA: {
    name: "NVIDIA Corporation",
    nameAr: "\u0625\u0646\u0641\u064a\u062f\u064a\u0627",
    code: "NASDAQ:NVDA",
    spot: 196.51,
    spotDate: "close 27 Jul 2026",
    ccy: "USD",
    fair: { bear: 147, base: 204, full: 287 },      // 6 Jul 2026 \u2014 weighted central 204 (+3.9% vs spot 196.44). Lenses: DCF 5-yr FCFF 189 (primary, TV ~79% of EV), relative multiples 200, forward-earnings power 230. bear/full = weighted bear/bull of the football field. Swing: how many years AI data-center capex sustains super-normal growth; China export controls; customer concentration. \u00a73 Monte Carlo PASSED its calibration back-test (CRPS skill +2.7% vs a random-walk cone) \u2014 an honest, skill-validated probability map. International name: zero secular drift, DCF-primary lens.
    dist: {
      t20: { label:"1 month",   p5:157.05, p25:179.56, p50:196.99, p75:216.37, p95:247.97, resolve:"2026-08-27" },
      t60: { label:"3 months",  p5:132.59, p25:168.27, p50:198.69, p75:234.29, p95:298.15, resolve:"2026-10-27" }
    },
    hz: { h1:22, h3:64, l1:"1 month", l3:"3 months", cal:true },
    touch: [ /* descending high -> low */
      [240.00, 13, 39], [230.00, 22, 49], [220.00, 36, 61], [210.00, 56, 74], [200.00, 81, 89], [190.00, 71, 83], [180.00, 45, 66], [170.00, 24, 50], [160.00, 11, 35]
    ],
    levels: { res:[209.67, 202.37, 197.06], sup:[191.14, 180.00, 170.00] },
    tech: {
      trend: "Below the 20-, 50- and 100-day averages but holding above a rising 200-day; consolidating after a pullback",
      summary: "The tape is soft but not broken. Price ($196.44) sits below the 20-day ($202.37), 50-day ($209.67) and 100-day ($197.06) moving averages, but above a rising 200-day line ($191.14) \u2014 a mid-range consolidation after a pullback from the high-$230s, not a breakdown. RSI(14) near 43 is neutral, tilted soft; the daily MACD is mildly negative (\u22124.06 line / \u22123.28 signal / \u22120.78 histogram). The trailing-year range is $158.24\u2013$235.74, and price sits mid-range. Realized 252-day volatility near 35% is elevated but typical for the name.",
      bull: "A daily close back above the $202\u2013210 moving-average cluster would signal the consolidation is resolving up, opening the $220 band and, above it, the 52-week high near $236.",
      bear: "A sustained close below the rising 200-day at $191 opens the $180 shelf and, beneath it, the $170 level."
    },
    files: {
      study: "files/NVDA_Valuation_Study_06-07-2026_public.docx?v=0706",
      model: "files/NVDA_Valuation_Model_06-07-2026_public.xlsx?v=0706",
      pdf:   "files/NVDA_Valuation_Study_06-07-2026_public.pdf?v=0706"
    }
  },
  KABO: {
    name: "El Nasr Clothing & Textiles (Kabo)",
    nameAr: "النصر للملابس والمنسوجات (كابو)",
    code: "EGX:KABO",
    spot: 8.80,
    spotDate: "close 22 Jul 2026",
    ccy: "EGP",
    fair: { bear: 1.42, base: 2.39, full: 3.52 },      // 6 Jul 2026 — weighted central 2.39 (\u221266% vs spot 7.00). Four lenses: revalued NAV (primary) 3.28, going-concern DCF 0.54 (floor), relative price-to-book 2.65, normalized earnings 1.24. bear/full = weighted bear/bull of the football field. Swing: the realizable value of the legacy Alexandria land against a ~95%-collapsed earnings base — at 7.00 the market prices a ~EGP 2.8bn land re-mark that has not been disclosed or monetised. Note: \u00a73 Monte Carlo FAILED its calibration back-test on this name (CRPS skill \u22120.010 vs a random-walk cone; study Appendix B) — no probabilistic price forecast is published; the distribution is an illustrative volatility map only.
    dist: {
      t20: { label:"1 month",   p5:7.29, p25:8.28, p50:8.93, p75:9.64, p95:10.95, resolve:"2026-08-23" },
      t60: { label:"3 months",  p5:6.29, p25:8.00, p50:9.22, p75:10.59, p95:13.46, resolve:"2026-10-22" }
    },
    hz: { h1:20, h3:61, l1:"1 month", l3:"3 months", cal:true },
    touch: [ /* descending high -> low; illustrative only */
      [9.00, 77, 89], [8.30, 47, 66], [7.70, 18, 40], [7.13, 6, 24], [6.65, 3, 14], [6.30, 1, 10], [5.60, 0, 4], [4.80, 0, 2]
    ],
    levels: { res:[8.90, 9.10, 9.30], sup:[7.11, 6.26, 5.95] },
    tech: {
      trend: "Trading above the whole moving-average stack, on a rising 200-day",
      summary: "The price closed 8.80 above a rising 20-day (7.24), a rising 50-day (6.61) and a rising 200-day (6.31). Momentum is stretched: RSI(14) is ~91 and the daily ATR near 0.27 (~3.1%) points to a lively tape. MACD (12\u00b726\u00b79) is positive and rising (+0.56 / +0.41 / +0.15). Over the last year it has ranged 4.63\u20138.80; the last close sits 0% below that high and 90% above that low.",
      bull: "A daily close back above 8.90 would clear the nearest resistance and open the 9.30 zone.",
      bear: "A close below 7.11 would break the nearest support and open the 5.95 zone."
    },
    asof: {
      mc:   { data:"2026-07-22", computed:"2026-07-28" },
      tech: { data:"2026-07-22", computed:"2026-07-29" }
    },
    files: {
      study: "files/KABO_Valuation_Study_06-07-2026_public.docx?v=0706",
      model: "files/KABO_Valuation_Model_06072026_public.xlsx?v=0706",
      pdf:   "files/KABO_Valuation_Study_06-07-2026_public.pdf?v=0706"
    }
  },

  IQCD: {
    name: "Industries Qatar",
    nameAr: "صناعات قطر",
    code: "QSE:IQCD",
    spot: 10.7,
    spotDate: "close 28 Jul 2026",
    ccy: "QAR",
    fair: { bear: 6.9, base: 10.9, full: 15.0 },      // 5 Jul 2026 — weighted central 10.9 (−2% vs spot 11.07). Five lenses: holdco SOTP (primary) 10.38, consolidated DCF 11.0-11.4, relative multiples 11.02, normalized earnings 11.02, dividend-discount 11.07. bear/full = weighted bear/bull of the football field. Swing factor: petrochemical (QAPCO/QAFAC) margin normalisation from its early-2026 trough (Q1-26 segment NI just QR4mn) plus the Ammonia-7 (Q2-26) and Ras Laffan pipeline; QAFCO fertilizers are the cash anchor, steel a restart option. ~6% dividend yield, debt-free, ~QR8.5bn net cash, QatarEnergy ~51%.
    dist: {
    t20: { label: "1 month", p5: 9.8144, p25: 10.37, p50: 10.73, p75: 11.11, p95: 11.74, resolve: "2026-08-30" },
    t60: { label: "3 months", p5: 9.237, p25: 10.18, p50: 10.81, p75: 11.48, p95: 12.67, resolve: "2026-10-28" }
  },
    touch: [[12.5,1,11],[12,4,22],[11.5,16,43],[11,54,73],[10.5,61,75],[10,15,37],[9.5,3,15]],
    levels: { res:[11.37, 11.94, 12.77], sup:[10.46, 10, 9] },
    tech: {
      trend: "Trading below the whole moving-average stack, under a falling 200-day",
      summary: "The price closed 11.07 below a falling 20-day (11.37), a falling 50-day (11.85) and a falling 200-day (12.07). Momentum is soft: RSI(14) is ~36 and the daily ATR near 0.21 (~1.9%) points to a normal tape. MACD (12\u00b726\u00b79) is negative and still falling (\u22120.24 / \u22120.22 / \u22120.02). Over the last year it has ranged 10.46\u201313.48; the last close sits 18% below that high and 6% above that low.",
      bull: "A daily close back above 11.37 would clear the nearest resistance and open the 12.77 zone.",
      bear: "A close below 10.46 would break the nearest support and open the 9.00 zone."
    },
    asof: {
      mc:   { data:"2026-07-05", computed:"2026-07-05" },
      tech: { data:"2026-07-05", computed:"2026-07-29" }
    },
    files: {
      study: "files/IQCD_Valuation_Study_05-07-2026_public.docx?v=0705g",
      model: "files/IQCD_Valuation_Model_05072026_public.xlsx?v=0705g",
      pdf:   "files/IQCD_Valuation_Study_05-07-2026_public.pdf?v=0705g"
    }
  },
  RAYA: {
    name: "Raya Holding",
    nameAr: "راية القابضة",
    code: "EGX:RAYA",
    spot: 7.76,
    spotDate: "close 22 Jul 2026",
    ccy: "EGP",
    fair: { bear: 4.77, base: 5.56, full: 8.22 },
    dist: {
      t20: { label:"1 month",   p5:6.53, p25:7.35, p50:7.88, p75:8.45, p95:9.51, resolve:"2026-08-23" },
      t60: { label:"3 months",  p5:5.73, p25:7.14, p50:8.13, p75:9.23, p95:11.49, resolve:"2026-10-22" }
    },
    hz: { h1:20, h3:61, l1:"1 month", l3:"3 months", cal:true },
    touch: [ [10.01, 12, 38], [8.85, 38, 62], [8.09, 70, 83], [7.31, 68, 81], [6.54, 30, 55], [5.39, 4, 22] ],
    levels: { res:[8, 8.20, 8.49], sup:[7.67, 6.94, 6.02] },
    tech: {
      trend: "Consolidating below the near-term moving averages, above a rising 200-day",
      summary: "The price closed 7.76 above a rising 50-day (7.48) and a rising 200-day (4.94), but below a rising 20-day (7.80). Momentum is neutral: RSI(14) is ~52 and the daily ATR near 0.31 (~4.0%) points to a lively tape. MACD (12\u00b726\u00b79) is above zero but rolling over (+0.13 / +0.19 / \u22120.06). Over the last year it has ranged 2.58\u20138.49; the last close sits 9% below that high and 201% above that low.",
      bull: "A daily close back above 8.00 would clear the nearest resistance and open the 8.49 zone.",
      bear: "A close below 7.67 would break the nearest support and open the 6.02 zone."
    },
    asof: {
      mc:   { data:"2026-07-22", computed:"2026-07-28" },
      tech: { data:"2026-07-22", computed:"2026-07-29" }
    },
    files: {
      study: "files/RAYA_Valuation_Study_01-07-2026_public.docx?v=0703",
      model: "files/RAYA_Valuation_Model_01-07-2026_public.xlsx?v=0703",
      pdf:   "files/RAYA_Valuation_Study_01-07-2026_public.pdf?v=0703"
    }
  },
  EFIH: {
    name: "e-finance for Digital & Financial Investments",
    nameAr: "إي فاينانس للاستثمارات المالية والرقمية",
    code: "EGX:EFIH",
    spot: 23.39,
    spotDate: "close 22 Jul 2026",
    ccy: "EGP",
    fair: { bear: 10.20, base: 14.16, full: 23.60 },          // 03 Jul 2026 valuation — weighted four-lens central
    dist: {
      t20: { label:"1 month",   p5:20.06, p25:22.30, p50:23.74, p75:25.28, p95:28.10, resolve:"2026-08-23" },
      t60: { label:"3 months",  p5:17.82, p25:21.78, p50:24.49, p75:27.49, p95:33.57, resolve:"2026-10-22" }
    },
    hz: { h1:20, h3:61, l1:"1 month", l3:"3 months", cal:true },
    touch: [ /* level, P(touch) 1-month %, 3-month % — descending */
      [26.00, 26, 58], [24.00, 73, 87], [23.00, 71, 82], [22.00, 38, 59], [21.00, 18, 40]
    ],
    levels: { res:[23.70, 25, 26], sup:[22.80, 21.60, 20.08] },
    tech: {
      trend: "Trading above the whole moving-average stack, on a rising 200-day",
      summary: "The price closed 23.39 above a rising 20-day (21.87), a rising 50-day (21.74) and a rising 200-day (19.03). Momentum is firm: RSI(14) is ~64 and the daily ATR near 0.64 (~2.7%) points to a normal tape. MACD (12\u00b726\u00b79) is positive and rising (+0.38 / +0.27 / +0.12). Over the last year it has ranged 11.87\u201323.70; the last close sits 1% below that high and 97% above that low.",
      bull: "A daily close back above 23.70 would clear the nearest resistance and open the 26.00 zone.",
      bear: "A close below 22.80 would break the nearest support and open the 20.08 zone."
    },
    asof: {
      mc:   { data:"2026-07-22", computed:"2026-07-28" },
      tech: { data:"2026-07-22", computed:"2026-07-29" }
    },
    files: {
      study: "files/EFIH_Valuation_Study_03-07-2026_public.docx?v=0307",
      model: "files/EFIH_Valuation_Study_03-07-2026_public.xlsx?v=0307",
      pdf:   "files/EFIH_Valuation_Study_03-07-2026_public.pdf?v=0307"
    }
  },
  JUFO: {
    name: "Juhayna Food Industries",
    nameAr: "جهينة للصناعات الغذائية",
    code: "EGX:JUFO",
    spot: 28.90,
    spotDate: "close 22 Jul 2026",
    ccy: "EGP",
    fair: { bear: 22, base: 26, full: 33 },
    dist: {
      t20: { label:"1 month",   p5:24.68, p25:27.51, p50:29.33, p75:31.29, p95:34.87, resolve:"2026-08-23" },
      t60: { label:"3 months",  p5:21.92, p25:26.87, p50:30.26, p75:34.02, p95:41.66, resolve:"2026-10-22" }
    },
    hz: { h1:20, h3:61, l1:"1 month", l3:"3 months", cal:true },
    touch: [ [35.99, 8, 34], [32.99, 31, 63], [31.49, 58, 80], [28.49, 40, 55], [26.99, 16, 32], [23.99, 2, 10] ],
    levels: { res:[29.97, 31.20, 31.99], sup:[26.66, 24.79, 23.72] },
    tech: {
      trend: "Consolidating below the near-term moving averages, above a rising 200-day",
      summary: "The price closed 28.90 below a falling 20-day (30.04) and a rising 50-day (29.68), but above a rising 200-day (26.84). Momentum is neutral: RSI(14) is ~41 and the daily ATR near 0.80 (~2.8%) points to a normal tape. MACD (12\u00b726\u00b79) is negative and still falling (\u22120.20 / +0.05 / \u22120.25). Over the last year it has ranged 20.27\u201332.30; the last close sits 11% below that high and 43% above that low.",
      bull: "A daily close back above 29.97 would clear the nearest resistance and open the 31.99 zone.",
      bear: "A close below 26.66 would break the nearest support and open the 23.72 zone."
    },
    asof: {
      mc:   { data:"2026-07-22", computed:"2026-07-28" },
      tech: { data:"2026-07-22", computed:"2026-07-29" }
    },
    files: {
      study: "files/JUFO_Valuation_Study_01-07-2026_public.docx?v=0704",
      model: "files/JUFO_Valuation_Study_01-07-2026_public.xlsx?v=0704",
      pdf:   "files/JUFO_Valuation_Study_01-07-2026_public.pdf?v=0704"
    }
  },
  EGAL: {
    name: "Egypt Aluminum",
    nameAr: "مصر للألومنيوم",
    code: "EGX:EGAL",
    spot: 301.12,
    spotDate: "close 22 Jul 2026",
    ccy: "EGP",
    fair: { bear: 183, base: 250, full: 358 },
    dist: {
      t20: { label:"1 month",   p5:263.16, p25:289.12, p50:305.61, p75:323.17, p95:355.02, resolve:"2026-08-23" },
      t60: { label:"3 months",  p5:230.79, p25:280.98, p50:315.30, p75:353.10, p95:429.59, resolve:"2026-10-22" }
    },
    hz: { h1:20, h3:61, l1:"1 month", l3:"3 months", cal:true },
    touch: [ [343.1, 15, 54], [314.5, 45, 78], [300.2, 69, 89], [271.6, 41, 53], [257.3, 19, 32], [228.7, 4, 11] ],
    levels: { res:[313.98, 321, 327.40], sup:[290, 281.13, 272.28] },
    tech: {
      trend: "Mixed against the moving-average stack, above a rising 200-day",
      summary: "The price closed 301.12 above a falling 20-day (293.62) and a rising 200-day (254.14), but below a flat 50-day (306.55). Momentum is neutral: RSI(14) is ~52 and the daily ATR near 6.97 (~2.3%) points to a normal tape. MACD (12\u00b726\u00b79) is positive and rising (+0.30 / \u22121.55 / +1.86). Over the last year it has ranged 151.00\u2013344.99; the last close sits 13% below that high and 99% above that low.",
      bull: "A daily close back above 313.98 would clear the nearest resistance and open the 327.40 zone.",
      bear: "A close below 290.00 would break the nearest support and open the 272.28 zone."
    },
    asof: {
      mc:   { data:"2026-07-22", computed:"2026-07-28" },
      tech: { data:"2026-07-22", computed:"2026-07-29" }
    },
    files: {
      study: "files/EGAL_Valuation_Study_03-07-2026_public.docx?v=0703",
      model: "files/EGAL_Valuation_Model_03072026_public.xlsx?v=0703",
      pdf:   "files/EGAL_Valuation_Study_03-07-2026_public.pdf?v=0703"
    }
  },
  EFID: {
    name: "Edita Food Industries",
    nameAr: "إيديتا للصناعات الغذائية",
    code: "EGX:EFID",
    spot: 27.70,
    spotDate: "close 22 Jul 2026",
    ccy: "EGP",
    fair: { bear: 16.41, base: 27.68, full: 42.78 },
    dist: {
      t20: { label:"1 month",   p5:23.72, p25:26.40, p50:28.11, p75:29.95, p95:33.33, resolve:"2026-08-23" },
      t60: { label:"3 months",  p5:20.81, p25:25.66, p50:29.01, p75:32.72, p95:40.32, resolve:"2026-10-22" }
    },
    hz: { h1:20, h3:61, l1:"1 month", l3:"3 months", cal:true },
    touch: [ /* descending high -> low */
      [32.81, 10, 40], [30.07, 38, 68], [28.71, 66, 84], [25.97, 37, 59], [24.61, 16, 39], [21.87, 2, 15]
    ],
    levels: { res:[28.11, 29.18, 30.98], sup:[27.06, 25.39, 24.94] },
    tech: {
      trend: "Consolidating below the near-term moving averages, above a rising 200-day",
      summary: "The price closed 27.70 below a flat 20-day (27.78) and a falling 50-day (28.19), but above a rising 200-day (26.68). Momentum is neutral: RSI(14) is ~47 and the daily ATR near 0.65 (~2.3%) points to a normal tape. MACD (12\u00b726\u00b79) is negative and still falling (\u22120.08 / \u22120.07 / \u22120.01). Over the last year it has ranged 13.51\u201332.50; the last close sits 15% below that high and 105% above that low.",
      bull: "A daily close back above 28.11 would clear the nearest resistance and open the 30.98 zone.",
      bear: "A close below 27.06 would break the nearest support and open the 24.94 zone."
    },
    asof: {
      mc:   { data:"2026-07-22", computed:"2026-07-28" },
      tech: { data:"2026-07-22", computed:"2026-07-29" }
    },
    files: {
      study: "files/EFID_Valuation_Study_03-07-2026_public.docx?v=0704",
      model: "files/EFID_Valuation_Model_03072026_public.xlsx?v=0704",
      pdf:   "files/EFID_Valuation_Study_03-07-2026_public.pdf?v=0704"
    }
  },
  BTFH: {
    name: "Beltone Financial Holding",
    nameAr: "بلتون المالية القابضة",
    code: "EGX:BTFH",
    spot: 3.09,
    spotDate: "close 22 Jul 2026",
    ccy: "EGP",
    fair: { bear: 1.89, base: 2.88, full: 4.13 },
    dist: {
      t20: { label:"1 month",   p5:2.70, p25:2.97, p50:3.14, p75:3.31, p95:3.64, resolve:"2026-08-23" },
      t60: { label:"3 months",  p5:2.43, p25:2.91, p50:3.24, p75:3.59, p95:4.29, resolve:"2026-10-22" }
    },
    hz: { h1:20, h3:61, l1:"1 month", l3:"3 months", cal:true },
    touch: [ [3.56, 9, 27], [3.27, 30, 51], [3.12, 53, 70], [2.82, 55, 75], [2.67, 30, 57], [2.38, 7, 27] ],
    levels: { res:[3.17, 3.34, 3.65], sup:[2.98, 2.93, 2.38] },
    tech: {
      trend: "Trading above the whole moving-average stack, on a flat 200-day",
      summary: "The price closed 3.09 above a rising 20-day (3.05), a rising 50-day (3.08) and a flat 200-day (3.08). Momentum is neutral: RSI(14) is ~53 and the daily ATR near 0.07 (~2.2%) points to a normal tape. MACD (12\u00b726\u00b79) is positive and rising (+0.01 / +0.01 / +0.01). Over the last year it has ranged 2.65\u20133.67; the last close sits 16% below that high and 17% above that low.",
      bull: "A daily close back above 3.17 would clear the nearest resistance and open the 3.65 zone.",
      bear: "A close below 2.98 would break the nearest support and open the 2.38 zone."
    },
    asof: {
      mc:   { data:"2026-07-22", computed:"2026-07-28" },
      tech: { data:"2026-07-22", computed:"2026-07-29" }
    },
    files: {
      study: "files/BTFH_Valuation_Study_03-07-2026_public.docx?v=0703",
      model: "files/BTFH_Valuation_Model_03072026_public.xlsx?v=0703",
      pdf:   "files/BTFH_Valuation_Study_03-07-2026_public.pdf?v=0703"
    }
  },
  ETEL: {
    name: "Telecom Egypt",
    nameAr: "المصرية للاتصالات",
    code: "EGX:ETEL",
    spot: 103.28,
    spotDate: "close 22 Jul 2026",
    ccy: "EGP",
    fair: { bear: 82, base: 118, full: 160 },
    dist: {
      t20: { label:"1 month",   p5:88.52, p25:98.45, p50:104.82, p75:111.65, p95:124.16, resolve:"2026-08-23" },
      t60: { label:"3 months",  p5:80.11, p25:96.80, p50:108.14, p75:120.57, p95:145.58, resolve:"2026-10-22" }
    },
    hz: { h1:20, h3:61, l1:"1 month", l3:"3 months", cal:true },
    touch: [ [111.13, 14, 54], [101.87, 43, 78], [97.24, 68, 89], [87.98, 37, 49], [83.35, 16, 28], [74.09, 3, 8] ],
    levels: { res:[110, 112.98, 120], sup:[101.68, 97.03, 89.30] },
    tech: {
      trend: "Trading above the whole moving-average stack, on a rising 200-day",
      summary: "The price closed 103.28 above a rising 20-day (96.57), a rising 50-day (95.71) and a rising 200-day (78.34). Momentum is firm: RSI(14) is ~70 and the daily ATR near 2.84 (~2.7%) points to a normal tape. MACD (12\u00b726\u00b79) is positive and rising (+2.00 / +1.25 / +0.75). Over the last year it has ranged 36.99\u2013112.98; the last close sits 9% below that high and 179% above that low.",
      bull: "A daily close back above 110.00 would clear the nearest resistance and open the 120.00 zone.",
      bear: "A close below 101.68 would break the nearest support and open the 89.30 zone."
    },
    asof: {
      mc:   { data:"2026-07-22", computed:"2026-07-28" },
      tech: { data:"2026-07-22", computed:"2026-07-29" }
    },
    files: {
      study: "files/ETEL_Valuation_Study_03-07-2026_public.docx?v=0704",
      model: "files/ETEL_Valuation_Model_03072026_public.xlsx?v=0704",
      pdf:   "files/ETEL_Valuation_Study_03-07-2026_public.pdf?v=0704"
    }
  },
  FWRY: {
    name: "Fawry",
    nameAr: "فوري",
    code: "EGX:FWRY",
    spot: 19.30,
    spotDate: "close 22 Jul 2026",
    ccy: "EGP",
    fair: { bear: 11.5, base: 14.7, full: 20.3 },
    dist: {
      t20: { label:"1 month",   p5:16.96, p25:18.57, p50:19.59, p75:20.67, p95:22.64, resolve:"2026-08-23" },
      t60: { label:"3 months",  p5:15.10, p25:18.14, p50:20.21, p75:22.46, p95:26.98, resolve:"2026-10-22" }
    },
    hz: { h1:20, h3:61, l1:"1 month", l3:"3 months", cal:true },
    touch: [ [22.08, 10, 40], [20.24, 37, 65], [19.32, 61, 80], [17.48, 47, 65], [16.56, 23, 44], [14.72, 4, 16] ],
    levels: { res:[19.47, 20.71, 21.62], sup:[19.02, 16.10, 13.80] },
    tech: {
      trend: "Trading above the whole moving-average stack, on a rising 200-day",
      summary: "The price closed 19.30 above a rising 20-day (18.95), a falling 50-day (19.29) and a rising 200-day (17.38). Momentum is neutral: RSI(14) is ~54 and the daily ATR near 0.45 (~2.3%) points to a normal tape. MACD (12\u00b726\u00b79) is positive and rising (+0.03 / \u22120.02 / +0.05). Over the last year it has ranged 12.21\u201321.66; the last close sits 11% below that high and 58% above that low.",
      bull: "A daily close back above 19.47 would clear the nearest resistance and open the 21.62 zone.",
      bear: "A close below 19.02 would break the nearest support and open the 13.80 zone."
    },
    asof: {
      mc:   { data:"2026-07-22", computed:"2026-07-28" },
      tech: { data:"2026-07-22", computed:"2026-07-29" }
    },
    files: {
      study: "files/FWRY_Valuation_Study_01-07-2026_public.docx?v=0703",
      model: "files/FWRY_Valuation_Study_01-07-2026_public.xlsx?v=0703",
      pdf:   "files/FWRY_Valuation_Study_01-07-2026_public.pdf?v=0703"
    }
  },
  ABUK: {
    name: "Abu Kir Fertilizers",
    nameAr: "أبو قير للأسمدة",
    code: "EGX:ABUK",
    spot: 72.30,
    spotDate: "close 22 Jul 2026",
    ccy: "EGP",
    fair: { bear: 50, base: 60, full: 72 },
    dist: {
      t20: { label:"1 month",   p5:62.48, p25:69.13, p50:73.38, p75:77.92, p95:86.21, resolve:"2026-08-23" },
      t60: { label:"3 months",  p5:56.17, p25:67.80, p50:75.70, p75:84.36, p95:101.76, resolve:"2026-10-22" }
    },
    hz: { h1:20, h3:61, l1:"1 month", l3:"3 months", cal:true },
    touch: [ [81.56, 20, 45], [74.77, 46, 66], [71.37, 66, 79], [64.57, 66, 80], [61.17, 44, 67], [54.38, 14, 40] ],
    levels: { res:[78, 79.75, 91.65], sup:[53.91, 51.34, 48.54] },
    tech: {
      trend: "Mixed against the moving-average stack, above a rising 200-day",
      summary: "The price closed 72.30 above a falling 20-day (70.50) and a rising 200-day (66.12), but below a falling 50-day (76.82). Momentum is neutral: RSI(14) is ~48 and the daily ATR near 2.09 (~2.9%) points to a normal tape. MACD (12\u00b726\u00b79) is below zero but turning up (\u22120.67 / \u22121.50 / +0.83). Over the last year it has ranged 45.18\u201395.00; the last close sits 24% below that high and 60% above that low.",
      bull: "A daily close back above 78.00 would clear the nearest resistance and open the 91.65 zone.",
      bear: "A close below 53.91 would break the nearest support and open the 48.54 zone."
    },
    asof: {
      mc:   { data:"2026-07-22", computed:"2026-07-28" },
      tech: { data:"2026-07-22", computed:"2026-07-29" }
    },
    files: {
      study: "files/ABUK_Valuation_Study_01-07-2026_public.docx?v=0703",
      model: "files/ABUK_Valuation_Study_01-07-2026_public.xlsx?v=0703",
      pdf:   "files/ABUK_Valuation_Study_01-07-2026_public.pdf?v=0703"
    }
  },
  ADIB: {
    name: "ADIB-Egypt",
    nameAr: "مصرف أبوظبي الإسلامي – مصر",
    code: "EGX:ADIB",
    spot: 49.30,
    spotDate: "close 22 Jul 2026",
    ccy: "EGP",
    fair: { bear: 31.6, base: 54.3, full: 95.3 },
    dist: {
      t20: { label:"1 month",   p5:42.43, p25:47.07, p50:50.03, p75:53.21, p95:59.02, resolve:"2026-08-23" },
      t60: { label:"3 months",  p5:37.52, p25:45.88, p50:51.62, p75:57.96, p95:70.84, resolve:"2026-10-22" }
    },
    hz: { h1:20, h3:61, l1:"1 month", l3:"3 months", cal:true },
    touch: [ [55, 21, 55], [52, 39, 70], [50, 57, 81], [48, 78, 91], [45, 56, 68], [42, 25, 42] ],
    levels: { res:[50.04, 51, 52], sup:[48.24, 44.06, 41.71] },
    tech: {
      trend: "Trading above the whole moving-average stack, on a rising 200-day",
      summary: "The price closed 49.30 above a rising 20-day (46.79), a rising 50-day (46.85) and a rising 200-day (36.49). Momentum is firm: RSI(14) is ~61 and the daily ATR near 1.31 (~2.7%) points to a normal tape. MACD (12\u00b726\u00b79) is positive and rising (+0.47 / +0.22 / +0.24). Over the last year it has ranged 20.01\u201350.08; the last close sits 2% below that high and 146% above that low.",
      bull: "A daily close back above 50.04 would clear the nearest resistance and open the 52.00 zone.",
      bear: "A close below 48.24 would break the nearest support and open the 41.71 zone."
    },
    asof: {
      mc:   { data:"2026-07-22", computed:"2026-07-28" },
      tech: { data:"2026-07-22", computed:"2026-07-29" }
    },
    files: {
      study: "files/ADIB_Valuation_Study_03-07-2026_public.docx?v=0703",
      model: "files/ADIB_Valuation_Study_03-07-2026_public.xlsx?v=0703",
      pdf:   "files/ADIB_Valuation_Study_03-07-2026_public.pdf?v=0703"
    }
  },
  ADIBUAE: {
    name: "Abu Dhabi Islamic Bank",
    nameAr: "مصرف أبوظبي الإسلامي",
    code: "ADX:ADIB",
    spot: 21.24,
    spotDate: "close 24 Jul 2026",
    ccy: "AED",
    fair: { bear: 17.73, base: 21.23, full: 24.63 },      // 11 Jul 2026 — five-lens weighted central 21.23 (-2.4% vs spot 21.76). Lenses: DDM (primary, 30%) 22.54, residual income (20%) 22.54, FCFE equity DCF (15%) 23.48, relative multiples ROE-adjusted (20%) 17.94, normalized through-cycle (15%) 19.00. bear = renewed-Hormuz-closure lower reference (2.5pt conflict adder); full = plan-delivered-at-peacetime-Ke upper reference. War-adjusted Ke 10.57% (rf 4.70% + β1.0×ERP4.87% + 1.0pt). The load-bearing tension is durability: a bank earning 28.8% ROE, with the terminal ROE (20% base) the swing input. Backtest PARITY (CRPS skill +0.009, 14 UAE windows). UAE's largest listed Islamic bank; 3,632.0mn shares.
    dist: {
      t20: { label:"1 month",   p5:18.50, p25:20.18, p50:21.30, p75:22.49, p95:24.47, resolve:"2026-08-24" },
      t60: { label:"3 months",  p5:16.73, p25:19.50, p50:21.45, p75:23.59, p95:27.53, resolve:"2026-10-26" }
    },
    hz: { h1:20, h3:63, l1:"1 month", l3:"3 months", cal:true },
    touch: [ /* descending high -> low; P(touch) 1-month %, 3-month % */
      [24.63, 7, 29], [23.30, 22, 49], [22.10, 55, 74], [20.75, 67, 80], [20.00, 38, 60], [18.80, 11, 34]
    ],
    levels: { res:[21.45, 21.99, 23.23], sup:[20.35, 18.70, 16.57] },
    tech: {
      trend: "Mixed against the moving-average stack, below a falling 200-day",
      summary: "The price closed 21.24 below a falling 20-day (21.27) and a falling 200-day (21.77), but above a falling 50-day (20.59). Momentum is neutral: RSI(14) is ~52 and the daily ATR near 0.56 (~2.6%) points to a normal tape. MACD (12\u00b726\u00b79) is above zero but rolling over (+0.01 / +0.10 / \u22120.09). Over the last year it has ranged 18.28\u201327.96; the last close sits 24% below that high and 16% above that low.",
      bull: "A daily close back above 21.45 would clear the nearest resistance and open the 23.23 zone.",
      bear: "A close below 20.35 would break the nearest support and open the 16.57 zone."
    },
    asof: {
      mc:   { data:"2026-07-24", computed:"2026-07-28" },
      tech: { data:"2026-07-24", computed:"2026-07-29" }
    },
    files: {
      study: "files/ADIB_Valuation_Study_11-07-2026_public.docx?v=0719a",
      model: "files/ADIB_Valuation_Model_11072026_public.xlsx?v=0719a"
    }
  },
  HRHO: {
    name: "EFG Holding",
    nameAr: "المجموعة المالية هيرميس القابضة",
    code: "EGX:HRHO",
    spot: 26.95,
    spotDate: "close 22 Jul 2026",
    ccy: "EGP",
    fair: { bear: 23, base: 27.7, full: 33.6 },
    dist: {
      t20: { label:"1 month",   p5:24.01, p25:26.06, p50:27.35, p75:28.72, p95:31.16, resolve:"2026-08-23" },
      t60: { label:"3 months",  p5:22.22, p25:25.83, p50:28.21, p75:30.76, p95:35.74, resolve:"2026-10-22" }
    },
    hz: { h1:20, h3:61, l1:"1 month", l3:"3 months", cal:true },
    touch: [ [32.2, 11, 33], [29.51, 36, 58], [28.17, 58, 74], [25.49, 60, 78], [24.15, 35, 62], [21.46, 9, 33] ],
    levels: { res:[27.25, 28.94, 30.04], sup:[26.01, 25.29, 24.61] },
    tech: {
      trend: "Mixed against the moving-average stack, below a flat 200-day",
      summary: "The price closed 26.95 below a falling 50-day (27.19) and a flat 200-day (27.18), but above a falling 20-day (26.76). Momentum is neutral: RSI(14) is ~51 and the daily ATR near 0.49 (~1.8%) points to a normal tape. MACD (12\u00b726\u00b79) is below zero but turning up (\u22120.06 / \u22120.11 / +0.05). Over the last year it has ranged 23.05\u201331.50; the last close sits 14% below that high and 17% above that low.",
      bull: "A daily close back above 27.25 would clear the nearest resistance and open the 30.04 zone.",
      bear: "A close below 26.01 would break the nearest support and open the 24.61 zone."
    },
    asof: {
      mc:   { data:"2026-07-22", computed:"2026-07-28" },
      tech: { data:"2026-07-22", computed:"2026-07-29" }
    },
    files: {
      study: "files/HRHO_Valuation_Study_01-07-2026_public.docx?v=0703",
      model: "files/HRHO_Valuation_Study_01-07-2026_public.xlsx?v=0703",
      pdf:   "files/HRHO_Valuation_Study_01-07-2026_public.pdf?v=0703"
    }
  },
  ORWE: {
    name: "Oriental Weavers",
    nameAr: "النساجون الشرقيون",
    code: "EGX:ORWE",
    spot: 23.12,
    spotDate: "close 22 Jul 2026",
    ccy: "EGP",
    fair: { bear: 16.7, base: 20.9, full: 29.7 },
    dist: {
      t20: { label:"1 month",   p5:21.01, p25:22.52, p50:23.46, p75:24.45, p95:26.21, resolve:"2026-08-23" },
      t60: { label:"3 months",  p5:19.41, p25:22.30, p50:24.20, p75:26.22, p95:30.12, resolve:"2026-10-22" }
    },
    hz: { h1:20, h3:61, l1:"1 month", l3:"3 months", cal:true },
    touch: [ [26.81, 2, 18], [24.57, 18, 47], [23.46, 43, 69], [21.22, 33, 55], [20.11, 10, 30], [17.87, 1, 5] ],
    levels: { res:[23.44, 24.64, 25.11], sup:[22.80, 21.60, 20.80] },
    tech: {
      trend: "Trading above the whole moving-average stack, on a rising 200-day",
      summary: "The price closed 23.12 above a falling 20-day (22.78), a flat 50-day (23.00) and a rising 200-day (22.91). Momentum is neutral: RSI(14) is ~53 and the daily ATR near 0.37 (~1.6%) points to a normal tape. MACD (12\u00b726\u00b79) is positive and rising (+0.04 / \u22120.02 / +0.06). Over the last year it has ranged 20.80\u201325.11; the last close sits 8% below that high and 11% above that low.",
      bull: "A daily close back above 23.44 would clear the nearest resistance and open the 25.11 zone.",
      bear: "A close below 22.80 would break the nearest support and open the 20.80 zone."
    },
    asof: {
      mc:   { data:"2026-07-22", computed:"2026-07-28" },
      tech: { data:"2026-07-22", computed:"2026-07-29" }
    },
    files: {
      study: "files/ORWE_Valuation_Study_01-07-2026_public.docx?v=0703",
      model: "files/ORWE_Valuation_Study_01-07-2026_public.xlsx?v=0703",
      pdf:   "files/ORWE_Valuation_Study_01-07-2026_public.pdf?v=0703"
    }
  },
  LCSW: {
    name: "Lecico Egypt (S.A.E.)",
    nameAr: "ليسيكو مصر",
    code: "EGX:LCSW",
    spot: 33.83,
    spotDate: "close 21 Jul 2026",
    ccy: "EGP",
    fair: { bear: 26, base: 37, full: 51 },      // 6 Jul 2026 — weighted central 37 (+26% vs spot 29.45). Lenses: FCFF DCF 37 (primary), relative multiples 39, normalized earnings 39, FCFE/owner-earnings 32 (floor), asset/reproduction 36. bear/full = weighted bear/bull of the football field. Swing factor: the EGP/USD path and whether booked earnings convert to cash.
    dist: {
      t20: { label:"1 month",   p5:26.69, p25:31.26, p50:34.33, p75:37.74, p95:44.21, resolve:"2026-08-23" },
      t60: { label:"3 months",  p5:23.00, p25:30.21, p50:35.44, p75:41.47, p95:54.42, resolve:"2026-10-21" }
    },
    hz: { h1:21, h3:61, l1:"1 month", l3:"3 months", cal:true },
    touch: [ /* descending high -> low */
      [36.80, 50, 72], [33.90, 88, 94], [31.50, 49, 65], [28.90, 20, 40], [26.50, 8, 24], [24.40, 3, 14], [22.10, 1, 7]
    ],
    levels: { res:[34.84, 35.43, 36], sup:[31.52, 28.38, 23.32] },
    tech: {
      trend: "Trading above the whole moving-average stack, on a rising 200-day",
      summary: "The price closed 33.83 above a rising 20-day (30.40), a rising 50-day (28.56) and a rising 200-day (26.38). Momentum is firm: RSI(14) is ~68 and the daily ATR near 1.39 (~4.1%) points to a lively tape. MACD (12\u00b726\u00b79) is positive and rising (+1.57 / +1.22 / +0.35). Over the last year it has ranged 22.82\u201335.43; the last close sits 5% below that high and 48% above that low.",
      bull: "A daily close back above 34.84 would clear the nearest resistance and open the 36.00 zone.",
      bear: "A close below 31.52 would break the nearest support and open the 23.32 zone."
    },
    asof: {
      mc:   { data:"2026-07-21", computed:"2026-07-28" },
      tech: { data:"2026-07-21", computed:"2026-07-29" }
    },
    files: {
      study: "files/LCSW_Valuation_Study_06-07-2026_public.docx?v=0706",
      model: "files/LCSW_Valuation_Model_06-07-2026_public.xlsx?v=0706",
      pdf:   "files/LCSW_Valuation_Study_06-07-2026_public.pdf?v=0706"
    }
  },
  DSCW: {
    name: "Dice For Ready-Made Garments",
    nameAr: "دايس للملابس الجاهزة (دايس سبورت آند كاجوال وير)",
    code: "EGX:DSCW",
    spot: 1.96,
    spotDate: "close 22 Jul 2026",
    ccy: "EGP",
    fair: { bear: 0.59, base: 0.88, full: 1.20 },          // 20 Jul 2026 revision — terminal g set to 5% (explicit conservative override, below all reconciliation anchors, disclosed §1.7). weighted central: 35% FCFF DCF (floored at 0; raw −0.51 at sourced WACC 23.53%, TV 94% of EV) / 35% normalized earnings power (7.5% through-cycle margin) / 30% relative EV/EBITDA. full = weighted bull central.
    dist: {
      t20: { label:"1 month",   p5:1.70, p25:1.88, p50:1.99, p75:2.11, p95:2.33, resolve:"2026-08-23" },
      t60: { label:"3 months",  p5:1.50, p25:1.83, p50:2.05, p75:2.30, p95:2.79, resolve:"2026-10-22" }
    },
    hz: { h1:20, h3:61, l1:"1 month", l3:"3 months", cal:true },
    touch: [ /* level, P(touch) 1-month %, 3-month % — descending */
      [2.40, 5, 29], [2.20, 21, 54], [2.00, 76, 89], [1.80, 24, 48], [1.60, 3, 17]
    ],
    levels: { res:[2.01, 2.07, 2.14], sup:[1.88, 1.78, 1.68] },
    tech: {
      trend: "Trading above the whole moving-average stack, on a rising 200-day",
      summary: "The price closed 1.96 above a rising 20-day (1.82), a falling 50-day (1.83) and a rising 200-day (1.80). Momentum is firm: RSI(14) is ~68 and the daily ATR near 0.05 (~2.3%) points to a normal tape. MACD (12\u00b726\u00b79) is positive and rising (+0.04 / +0.02 / +0.02). Over the last year it has ranged 1.45\u20132.23; the last close sits 12% below that high and 35% above that low.",
      bull: "A daily close back above 2.01 would clear the nearest resistance and open the 2.14 zone.",
      bear: "A close below 1.88 would break the nearest support and open the 1.68 zone."
    },
    asof: {
      mc:   { data:"2026-07-22", computed:"2026-07-28" },
      tech: { data:"2026-07-22", computed:"2026-07-29" }
    },
    files: {
      study: "files/DSCW_Valuation_Study_19-07-2026_public.docx?v=1907",
      model: "files/DSCW_Valuation_Study_19-07-2026_public.xlsx?v=1907",
      pdf:   "files/DSCW_Valuation_Study_19-07-2026_public.pdf?v=1907"
    }
  },
  PHDC: {
    name: "Palm Hills Developments",
    nameAr: "بالم هيلز للتعمير",
    code: "EGX:PHDC",
    spot: 15.01,
    spotDate: "close 22 Jul 2026",
    ccy: "EGP",
    fair: { bear: 7.62, base: 15.89, full: 24.92 },          // 9 Jun 2026 valuation — UNCHANGED: fundamental fair value is a separate clock from the MC price refresh (two-clocks rule); needs its own study cycle, not touched by a raw-OHLC roll-forward
    dist: {
      t20: { label:"1 month",   p5:12.89, p25:14.32, p50:15.23, p75:16.22, p95:18.01, resolve:"2026-08-23" },
      t60: { label:"3 months",  p5:11.52, p25:14.01, p50:15.72, p75:17.59, p95:21.39, resolve:"2026-10-22" }
    },
    hz: { h1:20, h3:61, l1:"1 month", l3:"3 months", cal:true },
    touch: [ /* level, P(touch) 1-month %, 3-month % — descending */
      [20.00, 1, 15], [18.50, 5, 28], [17.50, 12, 42], [16.50, 31, 62], [15.55, 66, 83]
    ],
    levels: { res:[16.08, 16.43, 17], sup:[14.85, 14.34, 13.01] },
    tech: {
      trend: "Trading above the whole moving-average stack, on a rising 200-day",
      summary: "The price closed 15.01 above a falling 20-day (14.85), a rising 50-day (14.77) and a rising 200-day (10.16). Momentum is neutral: RSI(14) is ~54 and the daily ATR near 0.46 (~3.1%) points to a lively tape. MACD (12\u00b726\u00b79) is above zero but rolling over (+0.08 / +0.12 / \u22120.04). Over the last year it has ranged 6.99\u201316.43; the last close sits 9% below that high and 115% above that low.",
      bull: "A daily close back above 16.08 would clear the nearest resistance and open the 17.00 zone.",
      bear: "A close below 14.85 would break the nearest support and open the 13.01 zone."
    },
    asof: {
      mc:   { data:"2026-07-22", computed:"2026-07-28" },
      tech: { data:"2026-07-22", computed:"2026-07-29" }
    },
    files: {
      study: "files/PHDC_Valuation_Study_11-06-2026_public.docx?v=1106",
      model: "files/PHDC_Valuation_Study_11-06-2026_public.xlsx?v=1106",
      pdf:   "files/PHDC_Valuation_Study_11-06-2026_public.pdf?v=1106"
    }
  },
  TMGH: {
    name: "Talaat Moustafa Group Holding",
    nameAr: "مجموعة طلعت مصطفى القابضة",
    code: "EGX:TMGH",
    spot: 100.50,
    spotDate: "close 22 Jul 2026",
    ccy: "EGP",
    fair: { bear: 83.6, base: 147.12, full: 189.6 },          // 9 Jun 2026 valuation — unchanged; separate clock, not touched by the 19 Jul roll-forward
    dist: {
      t20: { label:"1 month",   p5:88.26, p25:96.67, p50:102.00, p75:107.67, p95:117.92, resolve:"2026-08-23" },
      t60: { label:"3 months",  p5:80.66, p25:95.38, p50:105.21, p75:115.86, p95:136.92, resolve:"2026-10-22" }
    },
    hz: { h1:20, h3:61, l1:"1 month", l3:"3 months", cal:true },
    touch: [ /* descending high → low — same absolute levels, reprobabilised on the 19 Jul cycle-2 paths */
      [126.00, 2, 19], [118.00, 7, 34], [110.00, 28, 59], [100.00, 80, 87], [88.00, 8, 25], [83.00, 3, 13]
    ],
    levels: { res:[103.87, 110, 120], sup:[92.39, 80.96, 74.19] },
    tech: {
      trend: "Trading above the whole moving-average stack, on a rising 200-day",
      summary: "The price closed 100.50 above a rising 20-day (97.56), a rising 50-day (96.88) and a rising 200-day (81.79). Momentum is neutral: RSI(14) is ~59 and the daily ATR near 2.39 (~2.4%) points to a normal tape. MACD (12\u00b726\u00b79) is positive and rising (+1.52 / +1.14 / +0.37). Over the last year it has ranged 52.25\u2013103.87; the last close sits 3% below that high and 92% above that low.",
      bull: "A daily close back above 103.87 would clear the nearest resistance and open the 120.00 zone.",
      bear: "A close below 92.39 would break the nearest support and open the 74.19 zone."
    },
    asof: {
      mc:   { data:"2026-07-22", computed:"2026-07-28" },
      tech: { data:"2026-07-22", computed:"2026-07-29" }
    },
    files: {
      study: "files/TMGH_Valuation_Study_17-06-2026_public.docx?v=1706b",
      model: "files/TMGH_Valuation_Study_17-06-2026_public.xlsx?v=1706b",
      pdf:   "files/TMGH_Valuation_Study_17-06-2026_public.pdf?v=1706b"
    }
  },
  EMFD: {
    name: "Emaar Misr for Development",
    nameAr: "إعمار مصر للتنمية",
    code: "EGX:EMFD",
    spot: 11.53,
    spotDate: "close 28 Jul 2026",
    ccy: "EGP",
    fair: { bear: 13.71, base: 19.84, full: 23.43 },          // 17 Jun 2026 valuation — unchanged; separate clock, not touched by the 28 Jul roll-forward
    dist: {
      t20: { label:"1 month",   p5:10.12, p25:11.09, p50:11.70, p75:12.36, p95:13.54, resolve:"2026-08-30" },
      t60: { label:"3 months",  p5:9.19, p25:10.91, p50:12.07, p75:13.34, p95:15.85, resolve:"2026-10-28" }
    },
    hz: { h1:21, h3:62, l1:"1 month", l3:"3 months", cal:true },
    touch: [ /* descending high → low — same absolute levels, reprobabilised on the 28-Jul cycle-4 paths; ladder still sits entirely above spot and wants a human re-pick */
      [17.00, 0, 4], [16.00, 0, 7], [15.00, 1, 14], [14.00, 4, 26], [13.00, 16, 49]
    ],
    levels: { res:[12, 12.22, 12.65], sup:[11.25, 9.48, 8.92] },
    tech: {
      trend: "Consolidating below the near-term moving averages, above a rising 200-day",
      summary: "The price closed 11.53 below a falling 20-day (11.72) and a rising 50-day (11.56), but above a rising 200-day (9.99). Momentum is neutral: RSI(14) is ~47 and the daily ATR near 0.31 (~2.6%) points to a normal tape. MACD (12\u00b726\u00b79) is above zero but rolling over (+0.02 / +0.07 / \u22120.05). Over the last year it has ranged 7.92\u201312.70; the last close sits 9% below that high and 46% above that low.",
      bull: "A daily close back above 12.00 would clear the nearest resistance and open the 12.65 zone.",
      bear: "A close below 11.25 would break the nearest support and open the 8.92 zone."
    },
    asof: {
      mc:   { data:"2026-07-28", computed:"2026-07-28" },
      tech: { data:"2026-07-28", computed:"2026-07-29" }
    },
    files: {
      study: "files/EMFD_Valuation_Study_17-06-2026_public.docx?v=1706",
      model: "files/EMFD_Valuation_Study_17-06-2026_public.xlsx?v=1706",
      pdf:   "files/EMFD_Valuation_Study_17-06-2026_public.pdf?v=1706"
    }
  },
  OCDI: {
    name: "Sixth of October Development & Investment",
    nameAr: "السادس من أكتوبر للتنمية والاستثمار (سوديك)",
    code: "EGX:OCDI",
    spot: 27.48,
    spotDate: "close 27 Jul 2026",
    ccy: "EGP",
    fair: { bear: 16.72, base: 26.43, full: 30.77 },          // 24 Jun 2026 valuation — SOTP/RNAV risk-adjusted base; full execution 30.77; four-method synthesis ~27.7
    dist: {
      t20: { label:"1 month",   p5:22.80, p25:25.87, p50:27.89, p75:30.08, p95:34.14, resolve:"2026-08-27" },
      t60: { label:"3 months",  p5:20.11, p25:25.20, p50:28.78, p75:32.82, p95:41.15, resolve:"2026-10-27" }
    },
    hz: { h1:21, h3:62, l1:"1 month", l3:"3 months", cal:true },
    touch: [ /* descending high -> low */
      [30.00, 41, 67], [28.00, 79, 90], [27.00, 74, 83], [25.00, 30, 50], [24.00, 17, 37], [19.50, 1, 7]
    ],
    levels: { res:[28, 28.70, 30], sup:[26.20, 20.09, 18.79] },
    tech: {
      trend: "Trading above the whole moving-average stack, on a rising 200-day",
      summary: "The price closed 27.48 above a rising 20-day (26.67), a rising 50-day (23.76) and a rising 200-day (19.93). Momentum is firm: RSI(14) is ~63 and the daily ATR near 0.94 (~3.4%) points to a lively tape. MACD (12\u00b726\u00b79) is above zero but rolling over (+1.17 / +1.30 / \u22120.13). Over the last year it has ranged 14.60\u201328.70; the last close sits 4% below that high and 88% above that low.",
      bull: "A daily close back above 28.00 would clear the nearest resistance and open the 30.00 zone.",
      bear: "A close below 26.20 would break the nearest support and open the 18.79 zone."
    },
    asof: {
      mc:   { data:"2026-07-27", computed:"2026-07-27" },
      tech: { data:"2026-07-27", computed:"2026-07-29" }
    },
    files: {
      study: "files/OCDI_Valuation_Study_24-06-2026_public.docx?v=2406",
      model: "files/OCDI_Valuation_Study_24-06-2026_public.xlsx?v=2406",
      pdf:   "files/OCDI_Valuation_Study_24-06-2026_public.pdf?v=2406"
    }
  },
  ORHD: {
    name: "Orascom Development Egypt",
    nameAr: "أوراسكوم للتنمية مصر",
    code: "EGX:ORHD",
    spot: 40.16,
    spotDate: "close 27 Jul 2026",
    ccy: "EGP",
    fair: { bear: 22.5, base: 53.79, full: 70.52 },          // 24 Jun 2026 valuation — SOTP/RNAV risk-adjusted base; full execution 70.52; four-method synthesis ~55.8
    dist: {
      t20: { label:"1 month",   p5:34.82, p25:38.44, p50:40.76, p75:43.24, p95:47.74, resolve:"2026-08-27" },
      t60: { label:"3 months",  p5:31.10, p25:37.61, p50:42.05, p75:46.97, p95:56.82, resolve:"2026-10-27" }
    },
    hz: { h1:21, h3:62, l1:"1 month", l3:"3 months", cal:true },
    touch: [ /* descending high -> low */
      [50.00, 3, 24], [48.00, 7, 34], [46.00, 15, 47], [44.00, 30, 62], [42.00, 58, 80], [33.60, 5, 20]
    ],
    levels: { res:[40.80, 42, 43], sup:[39.66, 31.90, 26.13] },
    tech: {
      trend: "Trading above the whole moving-average stack, on a rising 200-day",
      summary: "The price closed 40.16 above a rising 20-day (38.96), a rising 50-day (37.52) and a rising 200-day (28.36). Momentum is firm: RSI(14) is ~61 and the daily ATR near 1.01 (~2.5%) points to a normal tape. MACD (12\u00b726\u00b79) is above zero but rolling over (+0.70 / +0.72 / \u22120.02). Over the last year it has ranged 20.38\u201340.80; the last close sits 2% below that high and 97% above that low.",
      bull: "A daily close back above 40.80 would clear the nearest resistance and open the 43.00 zone.",
      bear: "A close below 39.66 would break the nearest support and open the 26.13 zone."
    },
    asof: {
      mc:   { data:"2026-07-27", computed:"2026-07-27" },
      tech: { data:"2026-07-27", computed:"2026-07-29" }
    },
    files: {
      study: "files/ORHD_Valuation_Study_25-06-2026_public.docx?v=2506",
      model: "files/ORHD_Valuation_Study_25-06-2026_public.xlsx?v=2506",
      pdf:   "files/ORHD_Valuation_Study_25-06-2026_public.pdf?v=2506"
    }
  },
  COMI: {
    name: "Commercial International Bank",
    nameAr: "البنك التجاري الدولي",
    code: "EGX:COMI",
    spot: 142.00,
    spotDate: "close 28 Jul 2026",
    ccy: "EGP",
    fair: { bear: 90.86, base: 123.30, full: 169.70 },          // 29 Jun 2026 — justified-P/B / residual-income primary; weighted central 123.3 (-5% vs spot); bear = excess-return DCF (spread fades without capital return) 90.9; full = RI bull 169.7. Deeper RI-bear ~53.5 (ROE≈CoE) covered in the study text.
    dist: {
      t20: { label:"1 month",   p5:128.40, p25:138.05, p50:144.12, p75:150.51, p95:161.84, resolve:"2026-08-30" },
      t60: { label:"3 months",  p5:120.37, p25:137.46, p50:148.62, p75:160.56, p95:183.42, resolve:"2026-10-28" }
    },
    hz: { h1:21, h3:62, l1:"1 month", l3:"3 months", cal:true },
    touch: [ /* descending high -> low — same absolute levels, reprobabilised on the 28-Jul cycle-3 paths */
      [150.00, 41, 71], [140.00, 66, 77], [135.00, 30, 48], [120.00, 2, 10], [110.00, 0, 3], [100.00, 0, 1]
    ],
    levels: { res:[144.63, 150, 160], sup:[137.30, 132.25, 126.58] },
    tech: {
      trend: "Trading above the whole moving-average stack, on a rising 200-day",
      summary: "The price closed 142.00 above a rising 20-day (134.94), a flat 50-day (134.21) and a rising 200-day (120.53). Momentum is firm: RSI(14) is ~64 and the daily ATR near 2.62 (~1.8%) points to a normal tape. MACD (12\u00b726\u00b79) is positive and rising (+1.91 / +1.16 / +0.76). Over the last year it has ranged 79.59\u2013145.01; the last close sits 2% below that high and 78% above that low.",
      bull: "A daily close back above 144.63 would clear the nearest resistance and open the 160.00 zone.",
      bear: "A close below 137.30 would break the nearest support and open the 126.58 zone."
    },
    asof: {
      mc:   { data:"2026-07-28", computed:"2026-07-28" },
      tech: { data:"2026-07-28", computed:"2026-07-29" }
    },
    files: {
      study: "files/COMI_Valuation_Study_29-06-2026_public.docx?v=2906",
      model: "files/COMI_Valuation_Study_29-06-2026_public.xlsx?v=2906",
      pdf:   "files/COMI_Valuation_Study_29-06-2026_public.pdf?v=2906"
    }
  },
  SAMSUNG: {
    name: "Samsung Electronics Co., Ltd.",
    nameAr: "سامسونج للإلكترونيات",
    code: "KRX:005930",
    spot: 220000,
    spotDate: "close 28 Jul 2026",
    ccy: "KRW",
    fair: { bear: 214800, base: 296502, full: 410754 },      // 26 Jun 2026 — weighted central 296,502 (-13% vs spot); bear = consolidated DCF cross-check 214,800; full = supercycle/bull 410,754. Deeper SOTP cycle-reversion bear ~95,000 covered in the study text.
    dist: {
    t20: { label: "1 month", p5: 154820.6, p25: 193612.78, p50: 220362.84, p75: 251038.64, p95: 313821.44, resolve: "2026-08-28" },
    t60: { label: "3 months", p5: 129392.31, p25: 181881.54, p50: 222199.19, p75: 270912.64, p95: 381214.94, resolve: "2026-10-28" }
  },
    hz: { h1:22, h3:62, l1:"1 month", l3:"3 months", cal:true },
    touch: [[440000,1,4],[400000,1,7],[360000,3,11],[286000,17,35],[250000,44,62]],
    levels: { res:[362500, 350000, 344000], sup:[334675, 320000, 286320] },
    tech: {
      trend: "Extended uptrend, well above every moving average",
      summary: "The price is in a powerful, stretched advance — about 485% above its 52-week low and roughly 6% below its 362,500 all-time high, riding a correctly-stacked, rising set of moving averages (20-day above 50-day above 200-day). Momentum is firm but not yet stretched: RSI(14) is ~55, short of the 70 overbought line, so the trend has room. But realized 60-day volatility near 82% — far above the long-run ~33% — and strongly fat-tailed returns mean the same energy that drove the melt-up can also produce violent two-way moves.",
      bull: "A daily close above the 362,500 all-time high opens blue-sky continuation toward the 400,000 bull-case zone.",
      bear: "A close below the 50-day near 286,000 breaks the rising structure and opens the cycle-reversion zone toward the base-SOTP area."
    },
    files: {
      study: "files/Samsung_Valuation_Study_27-06-2026_public.docx?v=2706",
      model: "files/Samsung_Valuation_Study_27-06-2026_public.xlsx?v=2706",
      pdf:   "files/Samsung_Valuation_Study_27-06-2026_public.pdf?v=2706"
    }
  },
  KAKAO: {
    name: "Kakao Corp.",
    nameAr: "كاكاو",
    code: "KRX:035720",
    spot: 35650,
    spotDate: "close 28 Jul 2026",
    ccy: "KRW",
    fair: { bear: 24517, base: 34258, full: 46401 },      // 28 Jun 2026 — weighted central 34,258 (+3% vs spot); bear = consolidated DCF 24,517 (excludes stakes, conservative floor); full = discount-compression / SOTP bull 46,401. Gross net-asset value ~51,788 at no discount; deeper SOTP bear ~21,745 at a wide discount, covered in the study text.
    dist: {
    t20: { label: "1 month", p5: 27814.21, p25: 32498.94, p50: 35717.27, p75: 39311.86, p95: 45869.23, resolve: "2026-08-28" },
    t60: { label: "3 months", p5: 23978.91, p25: 30817.91, p50: 35986.62, p75: 41993.13, p95: 53885.8, resolve: "2026-10-28" }
  },
    hz: { h1:22, h3:62, l1:"1 month", l3:"3 months", cal:true },
    touch: [[44000,13,34],[40000,36,58],[37000,71,82],[32000,38,57],[28000,9,26],[24000,1,9]],
    levels: { res:[42949, 38888, 37000], sup:[32250, 30000, 28000] },
    tech: {
      trend: "Extended downtrend, below every moving average",
      summary: "The price is in a sustained decline — sitting at its 52-week low, about 36% below where it traded a year ago and roughly 53% off its 52-week high, beneath a correctly-stacked, falling set of moving averages (20-day below 50-day below 200-day). Momentum is washed out rather than stretched: RSI(14) is ~27, in oversold territory, which often precedes a bounce — but in a sustained downtrend a bounce need not hold. Realized 60-day volatility near 51% — far above quieter periods — and fat-tailed returns mean the same energy that drove the decline can also produce sharp two-way moves.",
      bull: "A reclaim of the falling 20-day near 38,900 would be the first sign the downtrend is stalling; a push toward 44,000 would need the holding-company discount to compress.",
      bear: "A daily close below the 32,250 52-week low opens the wide-discount zone toward the DCF / stale-marks area near 24,000–28,000."
    },
    files: {
      study: "files/Kakao_Valuation_Study_28-06-2026_public.docx?v=2806",
      model: "files/Kakao_Valuation_Study_28-06-2026_public.xlsx?v=2806",
      pdf:   "files/Kakao_Valuation_Study_28-06-2026_public.pdf?v=2806"
    }
  },
  LGES: {
    name: "LG Energy Solution, Ltd.",
    nameAr: "إل جي إنرجي سوليوشن",
    code: "KRX:373220",
    spot: 314000,
    spotDate: "close 28 Jul 2026",
    ccy: "KRW",
    fair: { bear: 150000, base: 248000, full: 415000 },      // 28 Jun 2026 — weighted central 248,000 (-25% vs spot); bear = AMPC-cut / EV-weak 150,000; full = recovery / ESS-AI supercycle 415,000. Going-concern DCF parent floor ~146,000 covered in the study text.
    dist: {
    t20: { label: "1 month", p5: 239661.03, p25: 283872.78, p50: 314576.54, p75: 349157.25, p95: 412942.73, resolve: "2026-08-28" },
    t60: { label: "3 months", p5: 203112.53, p25: 267452.66, p50: 317026.47, p75: 375503.78, p95: 493606.95, resolve: "2026-10-28" }
  },
    hz: { h1:22, h3:62, l1:"1 month", l3:"3 months", cal:true },
    touch: [[450000,3,16],[410000,9,28],[370000,25,48],[300000,67,79],[270000,28,49],[240000,8,26]],
    levels: { res:[423510, 407345, 399725], sup:[300000, 288000, 270000] },
    tech: {
      trend: "Downtrend, below every moving average",
      summary: "The price is in a sustained decline — sitting about 15% above its 52-week low and roughly 36% below its 514,000 52-week high, beneath a falling cluster of moving averages (the 20-, 50- and 200-day all sit between ~400,000 and ~424,000, with price below all three). Momentum is washed out rather than stretched: RSI(14) is ~33, approaching oversold, which often precedes a bounce — but in a downtrend a bounce need not hold. Realized 60-day volatility near 61% — well above the long-run ~55% — and right-skewed, fat-tailed returns mean the same energy that drove the ~21% three-month slide can also produce sharp two-way moves.",
      bull: "A reclaim of the falling 20-day near 400,000 would be the first sign the downtrend is stalling; a push toward 450,000 would need EV-demand fears to ease and the margin recovery to gain traction.",
      bear: "A daily close below the 288,000 52-week low opens the downside toward the DCF / bear-case zone near 240,000–270,000."
    },
    files: {
      study: "files/LG_Energy_Solution_Valuation_Study_28-06-2026_public.docx?v=2806",
      model: "files/LG_Energy_Solution_Valuation_Study_28-06-2026_public.xlsx?v=2806",
      pdf:   "files/LG_Energy_Solution_Valuation_Study_28-06-2026_public.pdf?v=2806"
    }
  },
  TMPV: {
    name: "Tata Motors Passenger Vehicles Ltd.",
    nameAr: "تاتا موتورز للسيارات (الركاب)",
    code: "NSE:TMPV",
    spot: 324.15,
    spotDate: "close 28 Jul 2026",
    ccy: "INR",
    fair: { bear: 236, base: 378, full: 579 },      // 30 Jun 2026 — weighted central 378 (+7% vs spot 352.20). Lenses: SOTP 376, consolidated DCF 376, relative 324 (floor), normalized earnings 416 (ceiling). bear/full = weighted bear/bull of the football field. Swing factor: JLR through-cycle margin and the conglomerate discount.
    dist: {
    t20: { label: "1 month", p5: 287.2, p25: 310.33, p50: 325.75, p75: 342.21, p95: 369.77, resolve: "2026-08-28" },
    t60: { label: "3 months", p5: 261.85, p25: 301.8, p50: 329.67, p75: 359.96, p95: 413.98, resolve: "2026-10-28" }
  },
    hz: { h1:22, h3:62, l1:"1 month", l3:"3 months", cal:true },
    touch: [[420,0,7],[400,1,13],[380,4,24],[360,15,43],[340,47,70],[320,74,84],[300,23,46]],
    levels: { res:[375, 365, 356], sup:[340, 320, 294] },
    tech: {
      trend: "Below every major moving average; oversold but still corrective",
      summary: "The tape is the mirror image of the fundamentals. The price trades below all four major moving averages (the 20-, 50-, 100- and 200-day cluster between ~356 and ~375, just overhead), the daily MACD histogram is firmly negative, and RSI(14) sits in the low-30s — near, but not yet at, oversold. The structure is a post-demerger de-rating that carried price from the high-440s to the low-350s, with the 52-week low at 294 as the visible floor. Realized 252-day volatility near 31% is elevated, and the same energy that drove the slide can produce sharp two-way moves.",
      bull: "A daily close back above the 365–375 moving-average cluster would be the first sign the downtrend is stalling; a push toward 400 would need JLR margin recovery to gain traction.",
      bear: "A daily close below 340 reopens the lower supports toward the 294 fifty-two-week low."
    },
    files: {
      study: "files/TMPV_Valuation_Study_30-06-2026_public.docx?v=3006",
      model: "files/TMPV_Valuation_Model_30-06-2026_public.xlsx?v=3006",
      pdf:   "files/TMPV_Valuation_Study_30-06-2026_public.pdf?v=3006"
    }
  },
  INFY: {
    name: "Infosys Limited",
    nameAr: "إنفوسيس",
    code: "NSE:INFY",
    spot: 1105,
    spotDate: "close 28 Jul 2026",
    ccy: "INR",
    fair: { bear: 995, base: 1242, full: 1556 },      // 6 Jul 2026 — weighted central 1,242 (+19% vs spot 1,042.20). Four lenses: intrinsic DCF (primary) 1,143 (floor), owner-earnings / shareholder-yield 1,267, relative multiples 1,284, normalized earnings power 1,368 (ceiling). bear/full = weighted bear/bull of the football field. Swing factor: the GenAI effect on the labour-arbitrage margin — whether Infosys cannibalises its own hours and keeps the margin, or AI deflates pricing faster than it cuts cost. Net-cash (~₹43,000 cr), ~33% ROE, >100% FCF conversion, >₹37,500 cr returned to owners in FY26.
    dist: {
      t20: { label:"1 month",   p5:959, p25:1046, p50:1110, p75:1180, p95:1289, resolve:"2026-08-28" },
      t60: { label:"3 months",  p5:882, p25:1017, p50:1124, p75:1241, p95:1431, resolve:"2026-10-28" }
    },
    hz: { h1:22, h3:62, l1:"1 month", l3:"3 months", cal:true },
    touch: [ /* descending high -> low; P(touch) 1M %, 3M % */
      [1250, 15, 40], [1200, 32, 57], [1150, 60, 76], [1100, 84, 90], [1050, 47, 64], [1000, 20, 41], [950, 6, 24], [900, 1, 12]
    ],
    levels: { res:[1085, 1138, 1230], sup:[985, 950, 900] },
    tech: {
      trend: "Below all four major moving averages; RSI in the mid-30s, MACD negative — a clear downtrend near the lower end of a wide 52-week range",
      summary: "The tape is the mirror image of the fundamentals. Infosys trades below its 20-day (₹1,085), 50-day (₹1,138), 100-day (₹1,230) and 200-day (₹1,395) moving averages — a full bearish stack — well down from the ₹1,689.80 fifty-two-week high toward the ₹985.30 low. RSI(14) near 37 is approaching oversold without being washed out; MACD is negative (−39.64 line / −37.90 signal / −1.75 histogram), so momentum is soft but no longer accelerating hard. Realized 252-day volatility is about 29%, and the YZ-HAR engine reads the current 60-day regime near 27% — a large-cap that can still move sharply on results or a GenAI headline.",
      bull: "A daily close back above the ₹1,085 twenty-day and the ₹1,138 fifty-day cluster would be the first sign the de-rating is stalling; a push toward the ₹1,230 hundred-day would need a demand-cycle recovery or an AI-margin surprise to gain traction.",
      bear: "A daily close below the ₹985 fifty-two-week-low shelf opens the simulated lower quartile toward ₹950 and ₹900, the main driver of the left tail being a US/EU discretionary-spend freeze or a GenAI pricing shock."
    },
    files: {
      study: "files/INFY_Valuation_Study_06-07-2026_public.docx?v=0706",
      model: "files/INFY_Valuation_Model_06-07-2026_public.xlsx?v=0706",
      pdf:   "files/INFY_Valuation_Study_06-07-2026_public.pdf?v=0706"
    }
  },

  ALDAR: {
    name: "Aldar Properties PJSC",
    nameAr: "الدار العقارية",
    code: "ADX:ALDAR",
    spot: 7.61,
    spotDate: "close 24 Jul 2026",
    ccy: "AED",
    fair: { bear: 7.95, base: 10.18, full: 11.77 },      // 08 Jul 2026 — weighted central 10.18 (+23% vs spot 8.30). Lenses: split-legs SOTP/RNAV 10.14 (primary), going-concern DCF (exit-multiple terminal) 9.81, relative 9.45, full-execution SOTP 11.29. bear/full = weighted bear/bull of the football field. Swing factors: the development-franchise value beyond backlog and the recurring cap rate. Gross asset value ~11.22/share; the market prices a discount at spot.
    dist: {
      t20: { label:"1 month",   p5:6.64, p25:7.24, p50:7.63, p75:8.05, p95:8.75, resolve:"2026-08-24" },
      t60: { label:"3 months",  p5:5.95, p25:6.97, p50:7.69, p75:8.48, p95:9.95, resolve:"2026-10-26" }
    },
    hz: { h1:20, h3:63, l1:"1 month", l3:"3 months", cal:true },
    touch: [ /* descending high -> low */
      [9.90, 0, 9], [9.50, 1, 14], [9.00, 4, 25], [8.60, 12, 39], [8.00, 46, 70], [7.50, 74, 85], [7.00, 24, 50]
    ],
    levels: { res:[7.71, 8.70, 9.22], sup:[7.48, 7.30, 7.07] },
    tech: {
      trend: "Trading below the whole moving-average stack, under a falling 200-day",
      summary: "The price closed 7.61 below a falling 20-day (7.96), a falling 50-day (7.92) and a falling 200-day (8.74). Momentum is soft: RSI(14) is ~38 and the daily ATR near 0.20 (~2.6%) points to a normal tape. MACD (12\u00b726\u00b79) is negative and still falling (\u22120.14 / \u22120.08 / \u22120.05). Over the last year it has ranged 7.03\u201311.80; the last close sits 36% below that high and 8% above that low.",
      bull: "A daily close back above 7.71 would clear the nearest resistance and open the 9.22 zone.",
      bear: "A close below 7.48 would break the nearest support and open the 7.07 zone."
    },
    asof: {
      mc:   { data:"2026-07-24", computed:"2026-07-28" },
      tech: { data:"2026-07-24", computed:"2026-07-29" }
    },
    files: {
      study: "files/Aldar_Valuation_Study_08-07-2026_public.docx?v=0709b",
      model: "files/Aldar_Valuation_Model_08-07-2026_public.xlsx?v=0709b",
      pdf:   "files/Aldar_Valuation_Study_08-07-2026_public.pdf?v=0709b"
    }
  },
  EMAAR: {
    name: "Emaar Properties PJSC",
    nameAr: "إعمار العقارية",
    code: "DFM:EMAAR",
    spot: 11.08,
    spotDate: "close 24 Jul 2026",
    ccy: "AED",
    fair: { bear: 11.08, base: 14.80, full: 18.75 },      // 01 Jul 2026 — weighted central 14.80 (+22% vs spot 12.14). Lenses: RNAV/SOTP 14.12 (primary), going-concern DCF 14.74, relative 15.53, normalized earnings 15.27. bear/full = weighted bear/bull of the football field. Swing factors: the recurring EV/EBITDA multiple and the NAV/conglomerate discount. Gross NAV ~17.6/share; the market prices a ~31% discount at spot.
    dist: {
      t20: { label:"1 month",   p5:9.82, p25:10.60, p50:11.11, p75:11.66, p95:12.56, resolve:"2026-08-24" },
      t60: { label:"3 months",  p5:8.85, p25:10.22, p50:11.19, p75:12.24, p95:14.17, resolve:"2026-10-26" }
    },
    hz: { h1:20, h3:63, l1:"1 month", l3:"3 months", cal:true },
    touch: [ /* descending high -> low */
      [15.50, 0, 3], [14.00, 1, 10], [13.00, 3, 24], [11.50, 53, 74], [10.50, 37, 61], [9.50, 3, 22], [8.50, 0, 5]
    ],
    levels: { res:[12.75, 13.04, 13.81], sup:[10.91, 10.15, 8.71] },
    tech: {
      trend: "Trading below the whole moving-average stack, under a falling 200-day",
      summary: "The price closed 11.08 below a falling 20-day (11.65), a falling 50-day (11.74) and a falling 200-day (13.31). Momentum is soft: RSI(14) is ~34 and the daily ATR near 0.27 (~2.4%) points to a normal tape. MACD (12\u00b726\u00b79) is negative and still falling (\u22120.24 / \u22120.17 / \u22120.08). Over the last year it has ranged 10.15\u201317.25; the last close sits 36% below that high and 9% above that low.",
      bull: "A daily close back above 12.75 would clear the nearest resistance and open the 13.81 zone.",
      bear: "A close below 10.91 would break the nearest support and open the 8.71 zone."
    },
    asof: {
      mc:   { data:"2026-07-24", computed:"2026-07-28" },
      tech: { data:"2026-07-24", computed:"2026-07-29" }
    },
    files: {
      study: "files/Emaar_Valuation_Study_01-07-2026_public.docx?v=0107b",
      model: "files/Emaar_Valuation_Model_01-07-2026_public.xlsx?v=0107",
      pdf:   "files/Emaar_Valuation_Study_01-07-2026_public.pdf?v=0107b"
    }
  },
  CCAP: {
    name: "Qalaa Holdings",
    nameAr: "القلعة القابضة",
    code: "EGX:CCAP",
    spot: 5.51,
    spotDate: "close 22 Jul 2026",
    ccy: "EGP",
    fair: { bear: 3.296, base: 5.89, full: 8.601 },      // 30 Jun 2026 — weighted central 5.89 (+23% vs spot); bear = consolidated bottom-up DCF 3.296 (excludes asset marks, conservative floor); full = discount-compression / SOTP bull 8.601. Gross net-asset value ~8.48 at no discount; market prices a ~44% discount, covered in the study text.
    dist: {
      t20: { label:"1 month",   p5:4.56, p25:5.18, p50:5.59, p75:6.04, p95:6.87, resolve:"2026-08-23" },
      t60: { label:"3 months",  p5:3.99, p25:5.03, p50:5.77, p75:6.60, p95:8.33, resolve:"2026-10-22" }
    },
    hz: { h1:20, h3:61, l1:"1 month", l3:"3 months", cal:true },
    touch: [ /* descending high -> low */
      [5.70, 70, 85], [5.20, 48, 65], [6.30, 24, 54], [4.50, 7, 24], [4.00, 2, 10], [3.50, 0, 4]
    ],
    levels: { res:[5.66, 5.78, 5.90], sup:[4.93, 4.08, 3.88] },
    tech: {
      trend: "Trading above the whole moving-average stack, on a rising 200-day",
      summary: "The price closed 5.51 above a rising 20-day (5.19), a rising 50-day (5.17) and a rising 200-day (3.86). Momentum is firm: RSI(14) is ~62 and the daily ATR near 0.17 (~3.1%) points to a lively tape. MACD (12\u00b726\u00b79) is positive and rising (+0.12 / +0.09 / +0.03). Over the last year it has ranged 2.20\u20135.78; the last close sits 5% below that high and 150% above that low.",
      bull: "A daily close back above 5.66 would clear the nearest resistance and open the 5.90 zone.",
      bear: "A close below 4.93 would break the nearest support and open the 3.88 zone."
    },
    asof: {
      mc:   { data:"2026-07-22", computed:"2026-07-28" },
      tech: { data:"2026-07-22", computed:"2026-07-29" }
    },
    files: {
      study: "files/Qalaa_Holdings_Valuation_Study_30-06-2026_public.docx?v=3006",
      model: "files/Qalaa_Holdings_Valuation_Study_30062026_public.xlsx?v=3006",
      pdf:   "files/Qalaa_Holdings_Valuation_Study_30-06-2026_public.pdf?v=3006"
    }
  },
  OIH: {
    name: "Orascom Investment Holding",
    nameAr: "أوراسكوم للاستثمار القابضة",
    code: "EGX:OIH",
    spot: 1.47,
    spotDate: "close 22 Jul 2026",
    ccy: "EGP",
    fair: { bear: 0.53, base: 0.78, full: 1.70 },           // 03 Jul 2026 study — four-lens weighted central 0.78 (−45% vs spot 1.41). Lenses: holdco NAV 0.81 (primary), consolidated DCF 0.48 (floor), relative P/NAV 0.72, normalized earnings 1.03 (ceiling). bear = weighted bear; full = weighted bull (DPRK cash recovered + OPE at maturity). USD marks at EGP/USD 49.09.
    dist: {
      t20: { label:"1 month",   p5:1.28, p25:1.41, p50:1.49, p75:1.58, p95:1.74, resolve:"2026-08-23" },
      t60: { label:"3 months",  p5:1.15, p25:1.38, p50:1.54, p75:1.71, p95:2.06, resolve:"2026-10-22" }
    },
    hz: { h1:20, h3:61, l1:"1 month", l3:"3 months", cal:true },
    touch: [ /* descending high → low; P(touch) 1-month %, 3-month % */
      [1.80, 4, 27], [1.60, 32, 64], [1.50, 76, 88], [1.30, 11, 32], [1.20, 3, 15], [1.10, 1, 7]
    ],
    levels: { res:[1.49, 1.56, 1.61], sup:[1.43, 1.13, 1.01] },
    tech: {
      trend: "Trading above the whole moving-average stack, on a rising 200-day",
      summary: "The price closed 1.47 above a rising 20-day (1.42), a falling 50-day (1.44) and a rising 200-day (1.26). Momentum is firm: RSI(14) is ~62 and the daily ATR near 0.03 (~1.8%) points to a normal tape. MACD (12\u00b726\u00b79) is positive and rising (+0.01 / +0.00 / +0.01). Over the last year it has ranged 0.98\u20131.66; the last close sits 11% below that high and 50% above that low.",
      bull: "A daily close back above 1.49 would clear the nearest resistance and open the 1.61 zone.",
      bear: "A close below 1.43 would break the nearest support and open the 1.01 zone."
    },
    asof: {
      mc:   { data:"2026-07-22", computed:"2026-07-28" },
      tech: { data:"2026-07-22", computed:"2026-07-29" }
    },
    files: {
      study: "files/OIH_Valuation_Study_03-07-2026_public.docx?v=0407",
      model: "files/OIH_Valuation_Model_03072026_public.xlsx?v=0407",
      pdf:   "files/OIH_Valuation_Study_03-07-2026_public.pdf?v=0407"
    }
  },
  ORAS: {
    name: "Orascom Construction",
    nameAr: "أوراسكوم للإنشاءات",
    code: "EGX:ORAS",
    spot: 713.50,
    spotDate: "close 22 Jul 2026",
    ccy: "EGP",
    fair: { bear: 740, base: 928, full: 1272 },              // 30 Jun 2026 study — 5-lens weighted central 928 (+29% vs spot 720); bear = normalized-earnings low lens 740; full = SOTP bull 1272. USD fundamentals at USD/EGP 49.2.
    dist: {
      t20: { label:"1 month",   p5:626.04, p25:686.07, p50:724.14, p75:764.62, p95:837.88, resolve:"2026-08-23" },
      t60: { label:"3 months",  p5:563.24, p25:673.02, p50:746.99, p75:827.58, p95:988.28, resolve:"2026-10-22" }
    },
    hz: { h1:20, h3:61, l1:"1 month", l3:"3 months", cal:true },
    touch: [ /* descending high → low; P(touch) 1-month %, 3-month % */
      [850.00, 6, 32], [800.00, 18, 52], [760.00, 43, 72], [680.00, 41, 61], [640.00, 13, 35], [600.00, 4, 19]
    ],
    levels: { res:[725, 762, 812.50], sup:[680, 535.12, 503.13] },
    tech: {
      trend: "Mixed against the moving-average stack, above a rising 200-day",
      summary: "The price closed 713.50 above a falling 20-day (708.47) and a rising 200-day (535.12), but below a rising 50-day (719.30). Momentum is neutral: RSI(14) is ~51 and the daily ATR near 17.75 (~2.5%) points to a normal tape. MACD (12\u00b726\u00b79) is below zero but turning up (\u22123.43 / \u22123.93 / +0.50). Over the last year it has ranged 357.00\u2013812.50; the last close sits 12% below that high and 100% above that low.",
      bull: "A daily close back above 725.00 would clear the nearest resistance and open the 812.50 zone.",
      bear: "A close below 680.00 would break the nearest support and open the 503.13 zone."
    },
    asof: {
      mc:   { data:"2026-07-22", computed:"2026-07-28" },
      tech: { data:"2026-07-22", computed:"2026-07-29" }
    },
    files: {
      study: "files/ORAS_Valuation_Study_30-06-2026_public.docx?v=3006",
      model: "files/ORAS_Valuation_Study_30-06-2026_public.xlsx?v=3006",
      pdf:   "files/ORAS_Valuation_Study_30-06-2026_public.pdf?v=3006"
    }
  },
  ARAMCO: {
    name: "Saudi Aramco",
    nameAr: "أرامكو السعودية",
    code: "TADAWUL:2222",
    spot: 26.60,
    spotDate: "close 26 Jul 2026",
    ccy: "SAR",
    fair: { bear: 20, base: 25.04, full: 31 },      // 1 Jul 2026 — weighted central 25.04 (−4.6% vs spot 26.24). Lenses: DCF (5-yr FCFF) 23.47, dividend-yield 26.09, relative 21.48 (floor), reserves-NAV 29.63 (ceiling), normalized 23.24. bear/full = weighted bear/bull of the football field. Swing factor: the oil-price path and the base dividend's free-cash coverage.
    dist: {
      t20: { label:"1 month",   p5:24.68, p25:25.89, p50:26.68, p75:27.51, p95:28.87, resolve:"2026-08-26" },
      t60: { label:"3 months",  p5:23.52, p25:25.52, p50:26.88, p75:28.30, p95:30.71, resolve:"2026-10-26" }
    },
    hz: { h1:22, h3:62, l1:"1 month", l3:"3 months", cal:true },
    touch: [ /* descending high -> low */
      [30.00, 2, 14], [29.00, 7, 28], [28.00, 24, 51], [27.00, 68, 82], [25.00, 13, 34], [24.00, 2, 14], [23.00, 0, 5]
    ],
    levels: { res:[26.94, 27.96, 29], sup:[25.90, 24.30, 23.04] },
    tech: {
      trend: "Mixed against the moving-average stack, above a rising 200-day",
      summary: "The price closed 26.60 above a rising 20-day (26.51) and a rising 200-day (25.95), but below a falling 50-day (26.89). Momentum is neutral: RSI(14) is ~49 and the daily ATR near 0.29 (~1.1%) points to an orderly tape. MACD (12\u00b726\u00b79) is positive and rising (+0.00 / \u22120.04 / +0.04). Over the last year it has ranged 23.04\u201327.96; the last close sits 5% below that high and 15% above that low.",
      bull: "A daily close back above 26.94 would clear the nearest resistance and open the 29.00 zone.",
      bear: "A close below 25.90 would break the nearest support and open the 23.04 zone."
    },
    asof: {
      mc:   { data:"2026-07-26", computed:"2026-07-28" },
      tech: { data:"2026-07-26", computed:"2026-07-29" }
    },
    files: {
      study: "files/Aramco_Valuation_Study_01-07-2026_public.docx?v=0107b",
      model: "files/Aramco_Valuation_Model_01-07-2026_public.xlsx?v=0107b",
      pdf:   "files/Aramco_Valuation_Study_01-07-2026_public.pdf?v=0107b"
    }
  },
  SABIC: {
    name: "Saudi Basic Industries Corp",
    nameAr: "الشركة السعودية للصناعات الأساسية (سابك)",
    code: "TADAWUL:2010",
    spot: 52.25,
    spotDate: "close 26 Jul 2026",
    ccy: "SAR",
    fair: { bear: 43, base: 55.5, full: 66 },      // 7 Jul 2026 — weighted central 55.5 (+7% vs spot 51.80). Four lenses: DCF (5-yr FCFF, mid-cycle) 60.3 (40%), dividend-yield 56.4 (25%), EV/EBITDA relative 47.8 (20%, floor), P/B asset-replacement 51.5 (15%). bear/full = weighted bear/bull of the football field. Swing factor: the product–feedstock spread in $/t and the timing of the margin-cycle recovery.
    dist: {
      t20: { label:"1 month",   p5:47.72, p25:50.55, p50:52.41, p75:54.37, p95:57.62, resolve:"2026-08-26" },
      t60: { label:"3 months",  p5:44.44, p25:49.38, p50:52.81, p75:56.45, p95:62.73, resolve:"2026-10-26" }
    },
    hz: { h1:22, h3:62, l1:"1 month", l3:"3 months", cal:true },
    touch: [ /* descending high -> low */
      [58.00, 6, 30], [56.00, 19, 48], [54.00, 49, 72], [52.00, 81, 89], [50.00, 34, 57], [48.00, 10, 33], [46.00, 2, 16]
    ],
    levels: { res:[53.87, 58.97, 61.71], sup:[51.54, 50.30, 48.20] },
    tech: {
      trend: "Mixed against the moving-average stack, below a falling 200-day; fresh death-cross",
      summary: "The price closed 52.25 below a falling 50-day (54.73) and a falling 200-day (56.40), but above a falling 20-day (52.18). Momentum is neutral: RSI(14) is ~44 and the daily ATR near 0.79 (~1.5%) points to a normal tape. MACD (12\u00b726\u00b79) is below zero but turning up (\u22120.53 / \u22120.78 / +0.25). The 50-day crossed beneath the 200-day 16 sessions ago \u2014 a fresh death-cross, a momentum-regime change rather than noise inside an intact trend. Over the last year it has ranged 48.20\u201364.00; the last close sits 18% below that high and 8% above that low.",
      bull: "A daily close back above 53.87 would clear the nearest resistance and open the 61.71 zone.",
      bear: "A close below 51.54 would break the nearest support and open the 48.20 zone."
    },
    asof: {
      mc:   { data:"2026-07-26", computed:"2026-07-28" },
      tech: { data:"2026-07-26", computed:"2026-07-29" }
    },
    files: {
      study: "files/SABIC_Valuation_Study_07-07-2026_public.docx?v=0707",
      model: "files/SABIC_Valuation_Model_07-07-2026_public.xlsx?v=0707",
      pdf:   "files/SABIC_Valuation_Study_07-07-2026_public.pdf?v=0707"
    }
  },
  MAADEN: {
    name: "Saudi Arabian Mining Company (Ma'aden)",
    nameAr: "شركة التعدين العربية السعودية (معادن)",
    code: "TADAWUL:1211",
    spot: 58.20,
    spotDate: "close 26 Jul 2026",
    ccy: "SAR",
    fair: { bear: 27, base: 42, full: 57 },      // 5 Jul 2026 — weighted central 42 (−29% vs spot 58.80). Lenses: SOTP 44 (primary), consolidated DCF (5-yr FCFF) 47, relative 26 (floor), mid-cycle earnings 42. bear/full = weighted bear/bull of the football field. Swing: the commodity deck (DAP/aluminium/gold) and whether the growth capex earns its cost of capital. Note: §3 Monte Carlo showed no CRPS skill vs a random-walk cone (see study Appendix B) — the distribution is an honest probability map, not a skill-validated forecast.
    dist: {
      t20: { label:"1 month",   p5:50.75, p25:55.30, p50:58.37, p75:61.67, p95:67.25, resolve:"2026-08-26" },
      t60: { label:"3 months",  p5:45.87, p25:53.40, p50:58.85, p75:64.79, p95:75.44, resolve:"2026-10-26" }
    },
    hz: { h1:22, h3:62, l1:"1 month", l3:"3 months", cal:true },
    touch: [ /* descending high -> low */
      [80.00, 0, 4], [72.00, 2, 15], [66.00, 12, 37], [62.00, 39, 63], [58.00, 85, 91], [54.00, 29, 53], [50.00, 6, 25], [46.00, 1, 9]
    ],
    levels: { res:[58.67, 64.75, 73.42], sup:[56.14, 54.11, 51.45] },
    tech: {
      trend: "Mixed against the moving-average stack, below a falling 200-day; fresh death-cross",
      summary: "The price closed 58.20 below a falling 50-day (60.65) and a falling 200-day (64.93), but above a falling 20-day (58.13). Momentum is neutral: RSI(14) is ~46 and the daily ATR near 1.30 (~2.2%) points to a normal tape. MACD (12\u00b726\u00b79) is below zero but turning up (\u22120.95 / \u22121.19 / +0.24). The 50-day crossed beneath the 200-day 22 sessions ago \u2014 a fresh death-cross, a momentum-regime change rather than noise inside an intact trend. Over the last year it has ranged 49.78\u201379.90; the last close sits 27% below that high and 17% above that low.",
      bull: "A daily close back above 58.67 would clear the nearest resistance and open the 73.42 zone.",
      bear: "A close below 56.14 would break the nearest support and open the 51.45 zone."
    },
    asof: {
      mc:   { data:"2026-07-26", computed:"2026-07-28" },
      tech: { data:"2026-07-26", computed:"2026-07-29" }
    },
    files: {
      study: "files/Maaden_Valuation_Study_05-07-2026_public.docx?v=0507",
      model: "files/Maaden_Valuation_Model_05-07-2026_public.xlsx?v=0507",
      pdf:   "files/Maaden_Valuation_Study_05-07-2026_public.pdf?v=0507"
    }
  },
  ADNOCGAS: {
    name: "ADNOC Gas",
    nameAr: "أدنوك للغاز",
    code: "ADX:ADNOCGAS",
    spot: 3.34,
    spotDate: "close 24 Jul 2026",
    ccy: "AED",
    fair: { bear: 3.30, base: 3.79, full: 4.60 },      // 4 Jul 2026 — weighted five-lens central 3.79 (+10% vs spot 3.44). Lenses: DCF (5-yr FCFF) 4.50 (ceiling), DDM (committed dividend, split-Ke 8.25%) 3.41, relative EV/EBITDA 3.83, justified P/E 3.62, dividend yield 3.83. bear/full = weighted bear/bull of the football field. Swing: Brent-linked export pricing and the gap between enterprise cash flow and the distributed dividend.
    dist: {
      t20: { label:"1 month",   p5:3.08, p25:3.24, p50:3.35, p75:3.46, p95:3.64, resolve:"2026-08-24" },
      t60: { label:"3 months",  p5:2.88, p25:3.17, p50:3.37, p75:3.58, p95:3.96, resolve:"2026-10-26" }
    },
    hz: { h1:20, h3:63, l1:"1 month", l3:"3 months", cal:true },
    touch: [ /* descending high -> low; P(touch) 1-month %, 3-month % */
      [3.90, 1, 11], [3.75, 3, 22], [3.65, 7, 33], [3.55, 20, 49], [3.35, 85, 92], [3.25, 47, 68], [3.15, 18, 44]
    ],
    levels: { res:[3.42, 3.49, 3.72], sup:[3.29, 3.20, 3.11] },
    tech: {
      trend: "Trading below the whole moving-average stack, under a flat 200-day",
      summary: "The price closed 3.34 below a falling 20-day (3.39), a flat 50-day (3.37) and a flat 200-day (3.41). Momentum is neutral: RSI(14) is ~44 and the daily ATR near 0.05 (~1.5%) points to a normal tape. MACD (12\u00b726\u00b79) is negative and still falling (\u22120.01 / \u22120.01 / \u22120.01). Over the last year it has ranged 3.12\u20133.76; the last close sits 11% below that high and 7% above that low.",
      bull: "A daily close back above 3.42 would clear the nearest resistance and open the 3.72 zone.",
      bear: "A close below 3.29 would break the nearest support and open the 3.11 zone."
    },
    asof: {
      mc:   { data:"2026-07-24", computed:"2026-07-28" },
      tech: { data:"2026-07-24", computed:"2026-07-29" }
    },
    files: {
      study: "files/ADNOC_Gas_Valuation_Study_04-07-2026_public.docx?v=0704",
      model: "files/ADNOC_Gas_Valuation_Model_04-07-2026_public.xlsx?v=0704",
      pdf:   "files/ADNOC_Gas_Valuation_Study_04-07-2026_public.pdf?v=0704"
    }
  },
  ALRAJHI: {
    name: "Al Rajhi Bank",
    nameAr: "مصرف الراجحي",
    code: "TADAWUL:1120",
    spot: 64.50,
    spotDate: "close 26 Jul 2026",
    ccy: "SAR",
    fair: { bear: 58, base: 70, full: 80 },      // 2 Jul 2026 — weighted central 70.1 (+6.2% vs spot 66.00). Lenses: DDM (primary) 58.2, residual income 76.8, FCFE (DCF) 79.5, justified P/B 75.7, normalized 65.3. bear/full = weighted bear/bull of the football field. Swing factors: the NIM path through the SAMA easing cycle and whether retained capital (~23% ROE) is valued on the dividend or the excess return.
    dist: {
      t20: { label:"1 month",   p5:58.58, p25:62.26, p50:64.70, p75:67.27, p95:71.54, resolve:"2026-08-26" },
      t60: { label:"3 months",  p5:54.40, p25:60.76, p50:65.19, p75:69.91, p95:78.09, resolve:"2026-10-26" }
    },
    hz: { h1:22, h3:62, l1:"1 month", l3:"3 months", cal:true },
    touch: [ /* descending high -> low */
      [74.00, 3, 20], [72.00, 6, 29], [70.00, 15, 43], [68.00, 33, 60], [64.00, 78, 87], [62.00, 40, 62], [60.00, 17, 41]
    ],
    levels: { res:[65.73, 67.55, 72.88], sup:[62.93, 59.36, 53.98] },
    tech: {
      trend: "Trading below the whole moving-average stack, under a flat 200-day; fresh death-cross",
      summary: "The price closed 64.50 below a falling 20-day (65.11), a falling 50-day (66.08) and a flat 200-day (67.88). Momentum is neutral: RSI(14) is ~42 and the daily ATR near 0.75 (~1.2%) points to an orderly tape. MACD (12\u00b726\u00b79) is negative and still falling (\u22120.62 / \u22120.59 / \u22120.03). The 50-day crossed beneath the 200-day 20 sessions ago \u2014 a fresh death-cross, a momentum-regime change rather than noise inside an intact trend. Over the last year it has ranged 60.10\u201375.33; the last close sits 14% below that high and 7% above that low.",
      bull: "A daily close back above 65.73 would clear the nearest resistance and open the 72.88 zone.",
      bear: "A close below 62.93 would break the nearest support and open the 53.98 zone."
    },
    asof: {
      mc:   { data:"2026-07-26", computed:"2026-07-28" },
      tech: { data:"2026-07-26", computed:"2026-07-29" }
    },
    files: {
      study: "files/Al_Rajhi_Valuation_Study_02-07-2026_public.docx?v=0207a",
      model: "files/Al_Rajhi_Valuation_Model_02-07-2026_public.xlsx?v=0207a",
      pdf:   "files/Al_Rajhi_Valuation_Study_02-07-2026_public.pdf?v=0207a"
    }
  },
  STC: {
    name: "stc Group (Saudi Telecom)",
    nameAr: "شركة الاتصالات السعودية",
    code: "TADAWUL:7010",
    spot: 43.10,
    spotDate: "close 26 Jul 2026",
    ccy: "SAR",
    fair: { bear: 36.2, base: 47.11, full: 59.1 },      // 09 Jul 2026 — weighted central 47.11 (+8.1% vs spot 43.58). Four lenses: FCFF DCF (primary, 35%) 50.12, DDM (25%) 45.88, relative EV/EBITDA (20%) 47.21, normalized earnings power (20%) 43.29. bear/full = weighted bear/bull of the football field. Swing factors: 5G/FTTH capex intensity vs. the dividend-cover math (FCF/dividend ~0.93x at the base FY26E 16.5%-of-revenue capex plan, tightening to ~0.86x at the top of guidance), the KSA consumer (CBU) ARPU/data-monetization path, and whether the international-subsidiary drag keeps fading.
    dist: {
      t20: { label:"1 month",   p5:40.36, p25:42.10, p50:43.23, p75:44.42, p95:46.35, resolve:"2026-08-26" },
      t60: { label:"3 months",  p5:38.19, p25:41.38, p50:43.55, p75:45.82, p95:49.65, resolve:"2026-10-26" }
    },
    hz: { h1:22, h3:62, l1:"1 month", l3:"3 months", cal:true },
    touch: [ /* descending high -> low; P(touch) 1-month %, 3-month % */
      [50.00, 0, 7], [48.00, 2, 18], [46.00, 11, 40], [44.00, 55, 76], [42.00, 42, 64], [40.00, 5, 26], [38.00, 0, 8], [36.00, 0, 2]
    ],
    levels: { res:[43.99, 45.38, 46.45], sup:[41.44, 40.20, 39] },
    tech: {
      trend: "Trading below the whole moving-average stack, under a flat 200-day",
      summary: "The price closed 43.10 below a falling 20-day (43.39), a flat 50-day (43.65) and a flat 200-day (43.41). Momentum is neutral: RSI(14) is ~42 and the daily ATR near 0.32 (~0.7%) points to an orderly tape. MACD (12\u00b726\u00b79) is negative and still falling (\u22120.14 / \u22120.12 / \u22120.02). Over the last year it has ranged 40.20\u201345.38; the last close sits 5% below that high and 7% above that low.",
      bull: "A daily close back above 43.99 would clear the nearest resistance and open the 46.45 zone.",
      bear: "A close below 41.44 would break the nearest support and open the 39.00 zone."
    },
    asof: {
      mc:   { data:"2026-07-26", computed:"2026-07-28" },
      tech: { data:"2026-07-26", computed:"2026-07-29" }
    },
    files: {
      study: "files/STC_Valuation_Study_09-07-2026_public.docx?v=0709a",
      model: "files/STC_Valuation_Model_09072026_public.xlsx?v=0709a",
      pdf:   "files/STC_Valuation_Study_09-07-2026_public.pdf?v=0709a"
    }
  },
  RIBL: {
    name: "Riyad Bank",
    nameAr: "مصرف الرياض",
    code: "TADAWUL:1010",
    spot: 20.92,
    spotDate: "close 26 Jul 2026",
    ccy: "SAR",
    fair: { bear: 20.85, base: 26.61, full: 33.24 },      // 09 Jul 2026 — weighted central 26.61 (+31.5% vs spot 20.23). Lenses: DDM (primary, 30%) 23.62, residual income (multi-period build, 20%) 33.24, FCFE (equity DCF, 15%) 32.18, relative multiples (20%) 24.62, normalized earnings power (15%) 20.85. bear/full = normalized floor / residual-income ceiling. Swing factors: the NIM path through the SAMA/Fed easing cycle and whether Riyad Bank's ~16% ROE persists (excess-return lenses) or fades toward the ~10.3% cost of equity (the market's implied ~1.2x book read).
    dist: {
      t20: { label:"1 month",   p5:19.08, p25:20.23, p50:20.98, p75:21.78, p95:23.11, resolve:"2026-08-26" },
      t60: { label:"3 months",  p5:17.84, p25:19.79, p50:21.14, p75:22.58, p95:25.04, resolve:"2026-10-26" }
    },
    hz: { h1:22, h3:62, l1:"1 month", l3:"3 months", cal:true },
    touch: [ /* descending high -> low */
      [23.26, 6, 28], [22.25, 24, 52], [21.24, 71, 84], [19.22, 10, 32], [18.21, 2, 13], [17.20, 0, 5]
    ],
    levels: { res:[21.41, 22.41, 24.01], sup:[20.57, 19.47, 18.98] },
    tech: {
      trend: "Trading above the whole moving-average stack, on a flat 200-day; fresh death-cross",
      summary: "The price closed 20.92 above a flat 20-day (20.50), a flat 50-day (20.50) and a flat 200-day (20.58). Momentum is neutral: RSI(14) is ~56 and the daily ATR near 0.30 (~1.4%) points to an orderly tape. MACD (12\u00b726\u00b79) is positive and rising (+0.13 / +0.06 / +0.08). The 50-day crossed beneath the 200-day 11 sessions ago \u2014 a fresh death-cross, a momentum-regime change rather than noise inside an intact trend. Over the last year it has ranged 18.98\u201322.41; the last close sits 7% below that high and 10% above that low.",
      bull: "A daily close back above 21.41 would clear the nearest resistance and open the 24.01 zone.",
      bear: "A close below 20.57 would break the nearest support and open the 18.98 zone."
    },
    asof: {
      mc:   { data:"2026-07-26", computed:"2026-07-28" },
      tech: { data:"2026-07-26", computed:"2026-07-29" }
    },
    files: {
      study: "files/RIBL_Valuation_Study_09-07-2026_public.docx?v=0709d",
      model: "files/RIBL_Valuation_Model_09072026_public.xlsx?v=0709d",
      pdf:   "files/RIBL_Valuation_Study_09-07-2026_public.pdf?v=0709d"
    }
  },
  SNB: {
    name: "The Saudi National Bank",
    nameAr: "البنك الأهلي السعودي",
    code: "TADAWUL:1180",
    spot: 39.92,
    spotDate: "close 26 Jul 2026",
    ccy: "SAR",
    fair: { bear: 36, base: 45, full: 55 },      // 2 Jul 2026 — weighted central 45.3 (+16% vs spot 38.96). Lenses: DDM (primary) 44.2, DCF (FCFF) 44.9, relative P/E-and-P/B 46.1, justified P/B (sustainable ROE) 46.9. bear/full = weighted bear/bull of the football field. Swing factor: the net interest margin through the SAMA easing cycle (a 74%-fixed investment book repricing slowly) and the Turkiye / legacy international drag.
    dist: {
      t20: { label:"1 month",   p5:35.32, p25:38.15, p50:40.04, p75:42.06, p95:45.45, resolve:"2026-08-26" },
      t60: { label:"3 months",  p5:32.25, p25:36.98, p50:40.36, p75:44.01, p95:50.47, resolve:"2026-10-26" }
    },
    hz: { h1:22, h3:62, l1:"1 month", l3:"3 months", cal:true },
    touch: [ /* descending high -> low; P(touch) 1-month %, 3-month % */
      [46.00, 6, 27], [44.00, 17, 44], [42.00, 43, 67], [40.00, 87, 93], [38.00, 41, 62], [36.00, 13, 36], [34.00, 3, 18]
    ],
    levels: { res:[40.52, 41.60, 42.88], sup:[38.22, 35.75, 33.83] },
    tech: {
      trend: "Mixed against the moving-average stack, below a flat 200-day; fresh death-cross",
      summary: "The price closed 39.92 above a falling 20-day (38.68) and a falling 50-day (39.36), but below a flat 200-day (39.96). Momentum is neutral: RSI(14) is ~58 and the daily ATR near 0.64 (~1.6%) points to a normal tape. MACD (12\u00b726\u00b79) is below zero but turning up (\u22120.10 / \u22120.32 / +0.23). The 50-day crossed beneath the 200-day 16 sessions ago \u2014 a fresh death-cross, a momentum-regime change rather than noise inside an intact trend. Over the last year it has ranged 33.30\u201345.24; the last close sits 12% below that high and 20% above that low.",
      bull: "A daily close back above 40.52 would clear the nearest resistance and open the 42.88 zone.",
      bear: "A close below 38.22 would break the nearest support and open the 33.83 zone."
    },
    asof: {
      mc:   { data:"2026-07-26", computed:"2026-07-28" },
      tech: { data:"2026-07-26", computed:"2026-07-29" }
    },
    files: {
      study: "files/SNB_Valuation_Study_04-07-2026_public.docx?v=0407j",
      model: "files/SNB_Valuation_Model_04072026_public.xlsx?v=0407j",
      pdf:   "files/SNB_Valuation_Study_04-07-2026_public.pdf?v=0407j"
    }
  },
  ENBD: {
    name: "Emirates NBD Bank",
    nameAr: "بنك الإمارات دبي الوطني",
    code: "DFM:EMIRATESNBD",
    spot: 30.22,
    spotDate: "close 24 Jul 2026",
    ccy: "AED",
    fair: { bear: 25, base: 32.3, full: 43.2 },      // 3 Jul 2026 — weighted central 32.3 (+5.4% vs spot 30.64). Lenses: DDM/residual income (primary) 32.9, FCFE (DCF) 31.1, relative P/TBV-and-P/E 33.4, normalized through-cycle 31.4. bear/full = weighted bear/bull of the football field. Swing factors: sustainable ROTE as the Fed/CBUAE ease the pegged dirham (NIM 3.46% off a 4.0% peak, CASA-cushioned) and the through-cycle cost of risk normalising off a ~0.2% recovery-flattered trough.
    dist: {
      t20: { label:"1 month",   p5:25.93, p25:28.55, p50:30.31, p75:32.19, p95:35.34, resolve:"2026-08-24" },
      t60: { label:"3 months",  p5:23.07, p25:27.41, p50:30.52, p75:33.97, p95:40.44, resolve:"2026-10-26" }
    },
    hz: { h1:20, h3:63, l1:"1 month", l3:"3 months", cal:true },
    touch: [ /* descending high -> low; P(touch) 1-month %, 3-month % */
      [37.00, 3, 21], [35.00, 10, 35], [33.00, 28, 56], [31.00, 69, 83], [30.00, 82, 89], [29.00, 54, 73], [27.00, 17, 42]
    ],
    levels: { res:[31, 31.72, 37.40], sup:[27.80, 24.14, 20.28] },
    tech: {
      trend: "Consolidating below the near-term moving averages, above a rising 200-day",
      summary: "The price closed 30.22 above a rising 50-day (29.18) and a rising 200-day (29.10), but below a falling 20-day (30.25). Momentum is neutral: RSI(14) is ~52 and the daily ATR near 0.86 (~2.9%) points to a normal tape. MACD (12\u00b726\u00b79) is above zero but rolling over (+0.08 / +0.20 / \u22120.12). Over the last year it has ranged 24.00\u201337.40; the last close sits 19% below that high and 26% above that low.",
      bull: "A daily close back above 31.00 would clear the nearest resistance and open the 37.40 zone.",
      bear: "A close below 27.80 would break the nearest support and open the 20.28 zone."
    },
    asof: {
      mc:   { data:"2026-07-24", computed:"2026-07-28" },
      tech: { data:"2026-07-24", computed:"2026-07-29" }
    },
    files: {
      study: "files/ENBD_Valuation_Study_03-07-2026_public.docx?v=0307a",
      model: "files/ENBD_Valuation_Model_03072026_public.xlsx?v=0307a",
      pdf:   "files/ENBD_Valuation_Study_03-07-2026_public.pdf?v=0307a"
    }
  },
  QNB: {
    name: "QNB Group",
    nameAr: "\u0645\u062c\u0645\u0648\u0639\u0629 QNB",
    code: "QSE:QNBK",
    spot: 17.54,
    spotDate: "close 5 Jul 2026",
    ccy: "QAR",
    fair: { bear: 14.0, base: 18.76, full: 28.5 },      // 5 Jul 2026 — weighted central 18.76 (+7.0% vs spot 17.54). Lenses: two-stage DDM on actual policy (primary) 18.7, FCFE/distributable-capital 20.2 (full-capacity ceiling 22.0), relative P/B-RoTE + peer 18.2, normalized through-cycle 17.6. bear/full = weighted bear/bull of the football field. Swing factors: the permanent Pillar-Two tax step (FY25 net profit +1.7% on ~+10% pre-tax), the 2026 rate-cut path through NIM (the pegged riyal), and how much of a 19.3%-capitalised balance sheet is returned rather than retained.
    dist: {
      t20: { label:"1 month",  p5:15.35, p25:16.74, p50:17.48, p75:18.19, p95:19.55, resolve:"2026-08-02" },
      t60: { label:"3 months", p5:13.96, p25:15.91, p50:17.24, p75:18.60, p95:20.91, resolve:"2026-09-27" }
    },
    touch: [ /* descending high -> low; P(touch) 1-month %, 3-month % */
      [19.5, 8, 26], [19.0, 15, 36], [18.5, 28, 50], [18.0, 51, 69], [17.0, 49, 72], [16.5, 28, 56], [15.5, 8, 30]
    ],
    levels: { res:[18.05, 18.60, 20.43], sup:[16.78, 15.98, 14.80] },
    tech: {
      trend: "Trading below the whole moving-average stack, under a flat 200-day",
      summary: "The price closed 17.54 below a rising 20-day (17.67), a falling 50-day (17.62) and a flat 200-day (18.43). Momentum is neutral: RSI(14) is ~48 and the daily ATR near 0.34 (~1.9%) points to a normal tape. MACD (12\u00b726\u00b79) is negative and still falling (\u22120.01 / +0.03 / \u22120.04). Over the last year it has ranged 16.34\u201320.49; the last close sits 14% below that high and 7% above that low.",
      bull: "A daily close back above 18.05 would clear the nearest resistance and open the 20.43 zone.",
      bear: "A close below 16.78 would break the nearest support and open the 14.80 zone."
    },
    asof: {
      mc:   { data:"2026-07-05", computed:"2026-07-05" },
      tech: { data:"2026-07-05", computed:"2026-07-29" }
    },
    files: {
      study: "files/QNB_Valuation_Study_05-07-2026_public.docx?v=0705a",
      model: "files/QNB_Valuation_Model_05072026_public.xlsx?v=0705a",
      pdf:   "files/QNB_Valuation_Study_05-07-2026_public.pdf?v=0705a"
    }
  },
  QGTS: {
    name: "Nakilat",
    nameAr: "\u0646\u0627\u0642\u0644\u0627\u062a",
    code: "QSE:QGTS",
    spot: 4.165,
    spotDate: "close 28 Jul 2026",
    ccy: "QAR",
    fair: { bear: 2.71, base: 4.29, full: 6.40 },      // 5 Jul 2026 \u2014 weighted central 4.29 (\u22120.7% vs spot 4.319). Four lenses: DCF on the contracted fleet (primary) 4.90, two-stage dividend-discount 3.56, relative EV/EBITDA & P/E 4.00, fleet-replacement NAV 4.06; blend 40/20/15/25. bear/full = weighted bear/bull of the football field. Swing factor: the discount rate on a bond-like ~20-year QatarEnergy charter stream (\u22487.5% base) and how much credit the newbuild programme (69\u2192112 vessels, first delivery end-2026) earns above its cost of capital. Note: the \u00a73 Monte-Carlo engine ties \u2014 does not beat \u2014 its random-walk benchmark for this unusually stable name (Appendix B), so the price map is illustrative only.
    dist: {
    t20: { label: "1 month", p5: 3.6712, p25: 3.9842, p50: 4.1774, p75: 4.3814, p95: 4.7543, resolve: "2026-08-30" },
    t60: { label: "3 months", p5: 3.3721, p25: 3.881, p50: 4.2096, p75: 4.5655, p95: 5.2533, resolve: "2026-10-28" }
  },
    touch: [[4.9,4,20],[4.7,10,32],[4.55,21,46],[4.4,39,63],[4.2,81,89],[4.05,59,74],[3.9,29,51]],
    levels: { res:[4.56, 4.74, 4.94], sup:[4.23, 4.12, 3.80] },
    tech: {
      trend: "Trading below the whole moving-average stack, under a falling 200-day",
      summary: "The price closed 4.32 below a rising 20-day (4.32), a flat 50-day (4.33) and a falling 200-day (4.50). Momentum is neutral: RSI(14) is ~49 and the daily ATR near 0.10 (~2.3%) points to a normal tape. MACD (12\u00b726\u00b79) is negative and still falling (\u22120.00 / +0.01 / \u22120.01). Over the last year it has ranged 3.80\u20135.00; the last close sits 14% below that high and 14% above that low.",
      bull: "A daily close back above 4.56 would clear the nearest resistance and open the 4.94 zone.",
      bear: "A close below 4.23 would break the nearest support and open the 3.80 zone."
    },
    asof: {
      mc:   { data:"2026-07-05", computed:"2026-07-05" },
      tech: { data:"2026-07-05", computed:"2026-07-29" }
    },
    files: {
      study: "files/Nakilat_QGTS_Valuation_Study_05-07-2026_public.docx?v=0705a",
      model: "files/Nakilat_QGTS_Valuation_Model_05072026_public.xlsx?v=0705a",
      pdf:   "files/Nakilat_QGTS_Valuation_Study_05-07-2026_public.pdf?v=0705a"
    }
  },
  FAB: {
    name: "First Abu Dhabi Bank",
    nameAr: "بنك أبوظبي الأول",
    code: "ADX:FAB",
    spot: 18.66,
    spotDate: "close 24 Jul 2026",
    ccy: "AED",
    fair: { bear: 17.1, base: 19.9, full: 22.4 },      // 3 Jul 2026 — weighted central 19.9 (+14% vs spot 17.40). Lenses: DDM (primary) 19.81, FCFE-DCF 20.70, relative P/B-ROE & peer P/E 18.78, normalized ROTE 19.90. bear/full = weighted bear/bull of the football field. Swing factor: the NIM through the Fed easing cycle (imported via the AED-USD peg) and the normalization of a benign ~49bps cost of risk.
    dist: {
      t20: { label:"1 month",   p5:16.48, p25:17.82, p50:18.71, p75:19.65, p95:21.20, resolve:"2026-08-24" },
      t60: { label:"3 months",  p5:15.06, p25:17.29, p50:18.84, p75:20.53, p95:23.61, resolve:"2026-10-26" }
    },
    hz: { h1:20, h3:63, l1:"1 month", l3:"3 months", cal:true },
    touch: [ /* descending high -> low; P(touch) 1-month %, 3-month % */
      [20.00, 30, 57], [19.00, 72, 84], [18.50, 79, 88], [18.00, 52, 70], [17.00, 16, 40], [16.00, 4, 20], [15.00, 1, 8]
    ],
    levels: { res:[19.04, 20.09, 20.74], sup:[18.18, 16.31, 13.18] },
    tech: {
      trend: "Trading above the whole moving-average stack, on a rising 200-day; fresh death-cross",
      summary: "The price closed 18.66 above a rising 20-day (17.77), a flat 50-day (17.35) and a rising 200-day (17.65). Momentum is firm: RSI(14) is ~63 and the daily ATR near 0.44 (~2.3%) points to a normal tape. MACD (12\u00b726\u00b79) is positive and rising (+0.26 / +0.18 / +0.09). The 50-day crossed beneath the 200-day 22 sessions ago \u2014 a fresh death-cross, a momentum-regime change rather than noise inside an intact trend. Over the last year it has ranged 15.32\u201320.74; the last close sits 10% below that high and 22% above that low.",
      bull: "A daily close back above 19.04 would clear the nearest resistance and open the 20.74 zone.",
      bear: "A close below 18.18 would break the nearest support and open the 13.18 zone."
    },
    asof: {
      mc:   { data:"2026-07-24", computed:"2026-07-28" },
      tech: { data:"2026-07-24", computed:"2026-07-29" }
    },
    files: {
      study: "files/FAB_Valuation_Study_03-07-2026_public.docx?v=0705",
      model: "files/FAB_Valuation_Model_03072026_public.xlsx?v=0705",
      pdf:   "files/FAB_Valuation_Study_03-07-2026_public.pdf?v=0705"
    }
  },
  ACWA: {
    name: "ACWA Power Company",
    nameAr: "شركة أكوا باور",
    code: "TADAWUL:2082",
    spot: 191.20,
    spotDate: "close 26 Jul 2026",
    ccy: "SAR",
    fair: { bear: 129, base: 195, full: 299 },      // 5 Jul 2026 — weighted central 195.3 (+0.7% vs spot 193.90). Lenses: SOTP/NAV (primary) 215.3, consolidated DCF (normalized attributable FCFF) 184.2, relative P/E-P/B-EV/EBITDA blend 158.1, pipeline-maturation earnings 197.1. bear/full = weighted bear/bull of the football field. Swing factor: whether Vision-2030 growth capital earns above its cost (ROIC vs Ke) as the SAR 100bn-plus under-construction book reaches commercial operation.
    dist: {
      t20: { label:"1 month",   p5:161.06, p25:179.25, p50:191.75, p75:205.33, p95:228.76, resolve:"2026-08-26" },
      t60: { label:"3 months",  p5:142.09, p25:171.50, p50:193.38, p75:217.80, p95:262.95, resolve:"2026-10-26" }
    },
    hz: { h1:22, h3:62, l1:"1 month", l3:"3 months", cal:true },
    touch: [ /* descending high -> low; P(touch) 1-month %, 3-month % */
      [250.00, 2, 14], [230.00, 7, 29], [210.00, 31, 57], [195.00, 76, 86], [180.00, 47, 66], [165.00, 12, 35], [150.00, 2, 15]
    ],
    levels: { res:[193.90, 201.03, 207.57], sup:[187.40, 182.34, 174.82] },
    tech: {
      trend: "Trading above the whole moving-average stack, on a falling 200-day; fresh golden-cross",
      summary: "The price closed 191.20 above a falling 20-day (190.49), a rising 50-day (191.13) and a falling 200-day (189.69). Momentum is neutral: RSI(14) is ~51 and the daily ATR near 4.84 (~2.5%) points to a normal tape. MACD (12\u00b726\u00b79) is below zero but turning up (\u22120.87 / \u22120.89 / +0.02). The 50-day crossed above the 200-day 4 sessions ago \u2014 a fresh golden-cross, a momentum-regime change rather than noise inside an intact trend. Over the last year it has ranged 149.40\u2013252.60; the last close sits 24% below that high and 28% above that low.",
      bull: "A daily close back above 193.90 would clear the nearest resistance and open the 207.57 zone.",
      bear: "A close below 187.40 would break the nearest support and open the 174.82 zone."
    },
    asof: {
      mc:   { data:"2026-07-26", computed:"2026-07-28" },
      tech: { data:"2026-07-26", computed:"2026-07-29" }
    },
    files: {
      study: "files/ACWA_Valuation_Study_05-07-2026_public.docx?v=0705a",
      model: "files/ACWA_Valuation_Model_05072026_public.xlsx?v=0705a",
      pdf:   "files/ACWA_Valuation_Study_05-07-2026_public.pdf?v=0705a"
    }
  },
  AGTHIA: {
    name: "Agthia Group PJSC",
    nameAr: "مجموعة أغذية",
    code: "ADX:AGTHIA",
    spot: 3.20,
    spotDate: "close 24 Jul 2026",
    ccy: "AED",
    fair: { bear: 3.05, base: 4.37, full: 6.09 },      // 06 Jul 2026 — four-lens weighted central 4.37 (+25% vs spot 3.51). Lenses: consolidated DCF 4.60 (primary; sleeve-built WACC ~10.6%, TV 70% of EV disclosed), segment SOTP 4.24, relative EV/EBITDA 3.83 (floor), normalized earnings 4.51; weights 35/25/15/25. FY25 optics (EPS 0.103, EBITDA −32%) carry AED 143mn of ring-fenced provisions; underlying EBITDA margin held 12.5% and Q1-26 turned. Swing: the Snacking margin reset (green coffee + EGP) and the KSA protein ramp. §3 Monte Carlo TIES its calibration back-test benchmark (PARITY — calibrated, honest, no single-name edge; the earlier FAILED banner used the superseded skill<0 rule, now corrected under the fitted 9-name UAE market profile).
    dist: {
      t20: { label:"1 month",   p5:2.86, p25:3.07, p50:3.21, p75:3.36, p95:3.59, resolve:"2026-08-24" },
      t60: { label:"3 months",  p5:2.60, p25:2.97, p50:3.23, p75:3.51, p95:4.02, resolve:"2026-10-26" }
    },
    hz: { h1:20, h3:63, l1:"1 month", l3:"3 months", cal:true },
    touch: [ /* descending high -> low; P(touch) 1-month %, 3-month % */
      [4.40, 0, 2], [4.20, 0, 5], [4.00, 0, 9], [3.70, 4, 24], [3.40, 32, 60], [3.20, 100, 100], [3.00, 26, 53]
    ],
    levels: { res:[3.64, 3.79, 4.03], sup:[3.17, 3.10, 3] },
    tech: {
      trend: "Trading below the whole moving-average stack, under a falling 200-day",
      summary: "The price closed 3.20 below a falling 20-day (3.39), a falling 50-day (3.50) and a falling 200-day (3.69). Momentum is washed out: RSI(14) is ~24 and the daily ATR near 0.06 (~1.8%) points to a normal tape. MACD (12\u00b726\u00b79) is negative and still falling (\u22120.09 / \u22120.07 / \u22120.02). Over the last year it has ranged 3.17\u20134.41; the last close sits 27% below that high and 1% above that low.",
      bull: "A daily close back above 3.64 would clear the nearest resistance and open the 4.03 zone.",
      bear: "A close below 3.17 would break the nearest support and open the 3.00 zone."
    },
    asof: {
      mc:   { data:"2026-07-24", computed:"2026-07-28" },
      tech: { data:"2026-07-24", computed:"2026-07-29" }
    },
    files: {
      study: "files/Agthia_Valuation_Study_06-07-2026_public.docx?v=0607a",
      model: "files/Agthia_Valuation_Model_06-07-2026_public.xlsx?v=0607a",
      pdf:   "files/Agthia_Valuation_Study_06-07-2026_public.pdf?v=0607a"
    }
  },
  AAPL: {
    name: "Apple Inc.",
    nameAr: "أبل",
    code: "NASDAQ:AAPL",
    spot: 336.91,
    spotDate: "close 27 Jul 2026",
    ccy: "USD",
    fair: { bear: 182, base: 208, full: 244 },      // 06 Jul 2026 — four-lens weighted central 208 (spot 313.09 = +51% above central). Lenses: consolidated DCF 152 (primary/floor), segment sum-of-the-parts 184, forward multiples 249, normalized earnings 253; DCF & relative weighted 30% each, normalized & SOTP 20% each. The ~$90 DCF-vs-multiple spread is the story — the durability/Services annuity the explicit cash flows do not capitalise; a football field, never a rating. Swing: Services attach-rate, gross-margin trajectory, the AI upgrade cycle.
    dist: {
    t20: { label: "1 month", p5: 294.17, p25: 320.62, p50: 337.8, p75: 356.2, p95: 387.93, resolve: "2026-08-27" },
    t60: { label: "3 months", p5: 267.37, p25: 310.49, p50: 340.32, p75: 372.83, p95: 434.07, resolve: "2026-10-27" }
  },
    hz: { h1:22, h3:64, l1:"1 month", l3:"3 months", cal:true },
    touch: [[376,15,41],[360,35,60],[344,71,83],[329,66,79],[297,10,31],[282,3,17],[266,1,9],[250,0,4]],
    levels: { res:[329, 344, 376], sup:[297, 282, 250] },
    tech: {
      trend: "Above a rising moving-average stack — constructive and extended",
      summary: "The tape is the mirror image of the fundamentals. Price sits above a rising 50/100/200-day stack (≈294 / 277 / 271) and just under the 52-week high near 315, with RSI(14) around 64 (firm, not yet overbought) and a daily MACD (12·26·9) that has crossed above its signal (+0.91 line / −0.58 signal / +1.49 histogram) — a bullish posture. Trailing realized volatility is in the mid-20s% while the gap-aware cone volatility is ≈28%. Nearest support is the 50-day around 294, then 282 and the 100/200-day cluster near 271–277; nearest resistance is the 52-week high near 315, then the +5% / +10% levels at 329 and 344.",
      bull: "A clean break above the 52-week high (315) into the 329–344 zone would extend the uptrend toward the one-month upper quartile.",
      bear: "A daily close back below the 50-day (≈294) reopens 282, then the 271–277 moving-average cluster."
    },
    files: {
      study: "files/AAPL_Valuation_Study_06-07-2026_public.docx?v=20260706j",
      model: "files/AAPL_Valuation_Model_06-07-2026_public.xlsx?v=20260706j",
      pdf:   "files/AAPL_Valuation_Study_06-07-2026_public.pdf?v=20260706j"
    }
  },
  TSLA: {
    name: "Tesla, Inc.",
    nameAr: "تسلا",
    code: "NASDAQ:TSLA",
    spot: 309.22,
    spotDate: "close 27 Jul 2026",
    ccy: "USD",
    fair: { bear: 105, base: 254, full: 350 },      // 01 Jul 2026 — five-lens weighted central 254 (−40% vs spot 420.60). Lenses: SOTP 230 (primary), consolidated DCF 90 (floor), relative 172, normalized earnings 130, and autonomy-at-scale (SOTP bull) 560 carrying a full 25% weight. bear = operating-only floor / cash-returns 105; full = scenario real-options / weighted football bull ~350; autonomy-at-scale reaches 560. Swing factor: the FSD/Robotaxi/Optimus autonomy option.
    dist: {
    t20: { label: "1 month", p5: 233.26, p25: 275.93, p50: 309.92, p75: 348.65, p95: 413.66, resolve: "2026-08-27" },
    t60: { label: "3 months", p5: 192.65, p25: 256.31, p50: 312.78, p75: 381.08, p95: 508.68, resolve: "2026-10-27" }
  },
    hz: { h1:22, h3:64, l1:"1 month", l3:"3 months", cal:true },
    touch: [[540,0,5],[500,0,9],[485,1,12],[460,2,16],[380,20,45],[360,33,57],[320,76,85]],
    levels: { res:[466, 490, 541], sup:[405, 360, 294] },
    tech: {
      trend: "Above a compressed moving-average stack; constructive but extended",
      summary: "The tape is the mirror image of the fundamentals. Price has recovered to sit just above a compressed 20/50/200-day cluster (~400–419), roughly 14% below the 52-week high at 489.88, with RSI(14) near 58 (neutral) and a daily MACD still below zero but with a positive histogram (−3.3 line / −4.4 signal / +1.1 histogram) — a bullish crossover forming. Realized volatility near 46% and an elevated ATR mean moves in either direction can be violent. Nearest support is the moving-average cluster around 400–405, then the range lows near 294; nearest resistance is the 52-week high near 490.",
      bull: "A push through the 466–490 zone (the one-month upper quartile into the 52-week high) would open the autonomy-re-rating extension toward 500+.",
      bear: "A daily close below the 400–405 moving-average cluster reopens the lower supports toward 360, then the 294 range low."
    },
    files: {
      study: "files/TSLA_Valuation_Study_30-06-2026_public.docx?v=0108",
      model: "files/TSLA_Valuation_Model_30-06-2026_public.xlsx?v=0108",
      pdf:   "files/TSLA_Valuation_Study_30-06-2026_public.pdf?v=0108"
    }
  },
  IHC: {
    name: "International Holding Company",
    nameAr: "الشركة العالمية القابضة",
    code: "ADX:IHC",
    spot: 380.00,
    spotDate: "close 24 Jul 2026",
    ccy: "AED",
    fair: { bear: 78, base: 104.5, full: 150 },      // 4 Jul 2026 — five-lens weighted central 104.5 (−73% vs spot 382.30). Lenses: look-through SOTP/NAV 120 (primary), consolidated operating DCF 81 (floor), relative multiples 102, normalized earnings 91; weights 45/15/20/20. Swing: the premium the market pays over reconstructable NAV — IHC trades at ~3.2x look-through NAV / ~5.5x attributable book, the inverse of the usual holdco discount.
    dist: {
      t20: { label:"1 month",   p5:365.12, p25:374.90, p50:381.13, p75:387.49, p95:397.56, resolve:"2026-08-24" },
      t60: { label:"3 months",  p5:348.92, p25:369.87, p50:383.54, p75:397.68, p95:421.81, resolve:"2026-10-26" }
    },
    hz: { h1:20, h3:63, l1:"1 month", l3:"3 months", cal:true },
    touch: [ /* descending high -> low; P(touch) 1-month %, 3-month % */
      [459.00, 0, 1], [440.00, 0, 2], [421.00, 0, 9], [405.00, 2, 27], [394.00, 15, 52], [371.00, 25, 55], [359.00, 2, 23], [344.00, 0, 6], [325.00, 0, 1]
    ],
    levels: { res:[387.22, 394.19, 400.18], sup:[370, 360, 350] },
    tech: {
      trend: "Trading below the whole moving-average stack, under a flat 200-day",
      summary: "The price closed 380.00 below a falling 20-day (381.02), a falling 50-day (385.12) and a flat 200-day (394.19). Momentum is soft: RSI(14) is ~39 and the daily ATR near 1.69 (~0.4%) points to an orderly tape. MACD (12\u00b726\u00b79) is below zero but turning up (\u22121.61 / \u22121.72 / +0.12). Over the last year it has ranged 379.00\u2013404.00; the last close sits 6% below that high and 0% above that low.",
      bull: "A daily close back above 387.22 would clear the nearest resistance and open the 400.18 zone.",
      bear: "A close below 370.00 would break the nearest support and open the 350.00 zone."
    },
    asof: {
      mc:   { data:"2026-07-24", computed:"2026-07-28" },
      tech: { data:"2026-07-24", computed:"2026-07-29" }
    },
    files: {
      study: "files/IHC_Valuation_Study_04-07-2026_public.docx?v=0407",
      model: "files/IHC_Valuation_Model_04-07-2026_public.xlsx?v=0407",
      pdf:   "files/IHC_Valuation_Study_04-07-2026_public.pdf?v=0407"
    }
  },
  HELI: {
    name: "Heliopolis Housing",
    nameAr: "مصر الجديدة للإسكان والتعمير",
    code: "EGX:HELI",
    spot: 8.27,
    spotDate: "close 22 Jul 2026",
    ccy: "EGP",
    fair: { bear: 5.20, base: 8.40, full: 11.82 },          // 3 Jul 2026 valuation — weighted central 8.40 (RNAV 8.30 primary / DCF 8.30 / relative 7.45 / normalized 9.25; 40/20/15/25). bear 5.20, bull 11.82. Swing: partnership-annuity marks & the RNAV/state discount.
    dist: {
      t20: { label:"1 month",   p5:7.12, p25:7.90, p50:8.39, p75:8.92, p95:9.89, resolve:"2026-08-23" },
      t60: { label:"3 months",  p5:6.37, p25:7.73, p50:8.66, p75:9.68, p95:11.74, resolve:"2026-10-22" }
    },
    hz: { h1:20, h3:61, l1:"1 month", l3:"3 months", cal:true },
    touch: [ /* level, P(touch) 1-month %, 3-month % — descending */
      [8.00, 57, 72], [7.50, 21, 42], [7.00, 6, 23], [6.75, 4, 16], [6.10, 1, 7], [5.75, 0, 4]
    ],
    levels: { res:[8.40, 8.60, 8.80], sup:[7.20, 6.87, 6.32] },
    tech: {
      trend: "Trading above the whole moving-average stack, on a rising 200-day",
      summary: "The price closed 8.27 above a rising 20-day (7.17), a rising 50-day (6.84) and a rising 200-day (4.83). Momentum is stretched: RSI(14) is ~79 and the daily ATR near 0.25 (~3.0%) points to a normal tape. MACD (12\u00b726\u00b79) is positive and rising (+0.44 / +0.31 / +0.13). Over the last year it has ranged 3.11\u20138.40; the last close sits 2% below that high and 166% above that low.",
      bull: "A daily close back above 8.40 would clear the nearest resistance and open the 8.80 zone.",
      bear: "A close below 7.20 would break the nearest support and open the 6.32 zone."
    },
    asof: {
      mc:   { data:"2026-07-22", computed:"2026-07-28" },
      tech: { data:"2026-07-22", computed:"2026-07-29" }
    },
    files: {
      study: "files/HELI_Valuation_Study_03-07-2026_public.docx?v=0307",
      model: "files/HELI_Valuation_Study_03-07-2026_public.xlsx?v=0307",
      pdf:   "files/HELI_Valuation_Study_03-07-2026_public.pdf?v=0307"
    }
  },
  PRDC: {
    name: "Pioneers Properties for Urban Development",
    nameAr: "بايونيرز بروبرتيز للتنمية العمرانية",
    code: "EGX:PRDC",
    spot: 9.80,
    spotDate: "close 22 Jul 2026",
    ccy: "EGP",
    fair: { bear: 5.92, base: 8.23, full: 11.51 },          // 6 Jul 2026 valuation — split-leg RNAV primary lens
    dist: {
      t20: { label:"1 month",   p5:7.84, p25:9.11, p50:9.95, p75:10.87, p95:12.62, resolve:"2026-08-23" },
      t60: { label:"3 months",  p5:7.02, p25:8.92, p50:10.26, p75:11.78, p95:14.95, resolve:"2026-10-22" }
    },
    hz: { h1:20, h3:61, l1:"1 month", l3:"3 months", cal:true },
    touch: [ /* level, P(touch) 1-month %, 3-month % — descending */
      [10.76, 44, 67], [9.94, 83, 91], [9.11, 46, 60], [8.69, 28, 44], [7.87, 9, 22], [7.45, 5, 15], [6.62, 1, 6]
    ],
    levels: { res:[9.90, 10.10, 10.40], sup:[9.70, 9, 8.46] },
    tech: {
      trend: "Trading above the whole moving-average stack, on a rising 200-day",
      summary: "The price closed 9.80 above a rising 20-day (8.46), a rising 50-day (7.08) and a rising 200-day (4.84). Momentum is firm: RSI(14) is ~66 and the daily ATR near 0.58 (~5.9%) points to a volatile tape. MACD (12\u00b726\u00b79) is positive and rising (+0.81 / +0.74 / +0.08). Over the last year it has ranged 3.04\u201310.40; the last close sits 6% below that high and 222% above that low.",
      bull: "A daily close back above 9.90 would clear the nearest resistance and open the 10.40 zone.",
      bear: "A close below 9.70 would break the nearest support and open the 8.46 zone."
    },
    asof: {
      mc:   { data:"2026-07-22", computed:"2026-07-28" },
      tech: { data:"2026-07-22", computed:"2026-07-29" }
    },
    files: {
      study: "files/PRDC_Valuation_Study_06-07-2026_public.docx?v=0706",
      model: "files/PRDC_Valuation_Study_06-07-2026_public.xlsx?v=0706",
      pdf:   "files/PRDC_Valuation_Study_06-07-2026_public.pdf?v=0706"
    }
  }
};

/* coming-soon cards (home page coverage section) */
const COMING = [
  { code:"EGX:TMGH", name:"Talaat Moustafa Group",        url:"tmgh.html", status:"covered" },
  { code:"EGX:EMFD", name:"Emaar Misr for Development",        url:"emfd.html", status:"covered" },
  { code:"EGX:OCDI", name:"SODIC",                            url:"ocdi.html", status:"covered" },
  { code:"EGX:ORHD", name:"Orascom Development",          url:"orhd.html", status:"covered" },
  { code:"EGX:ORAS", name:"Orascom Construction",          url:"oras.html", status:"covered" },
  { code:"EGX:OIH",  name:"Orascom Investment Holding",    url:"oih.html",  status:"covered" },
  { code:"EGX:COMI", name:"Commercial International Bank", url:"comi.html", status:"covered" },
  { code:"EGX:HELI", name:"Heliopolis Housing",              url:"heli.html", status:"covered" },
  { code:"EGX:EGAL", name:"Egypt Aluminum",                   url:"egal.html", status:"covered" },
  { code:"EGX:BTFH", name:"Beltone Financial Holding",        url:"btfh.html", status:"covered" },
  { code:"EGX:MFPC", name:"MOPCO",                            url:null,        status:"soon" },
  { code:"EGX:ETEL", name:"Telecom Egypt",                    url:"etel.html", status:"covered" },
];

/* ---------- public ledger ----------
   Append a row whenever a distribution is published.
   On resolve date: set realized + status:"scored". NEVER delete a row. */
/* ============================================================================
   CALIBRATION LEDGER — universal, security-agnostic schema.
   Keyed off `instrument` + `asset_class` (equity | metal | other), NOT EGX- or
   stock-specific. Every future study (any exchange, any asset class) inherits
   this exact structure. Anchor fields are logged at publication; grade_* fields
   stay null until grade_date, then filled with the realized outcome.
   Relative touch bands (touch_*) store the model's P(touch ±X% from anchor)
   within the horizon; touch_hit_* are filled at grade time (true/false/null).
   ----------------------------------------------------------------------------
   Field reference (per row):
     instrument        ticker/symbol, e.g. "PHDC", "XAGUSD"
     asset_class        "equity" | "metal" | "other"
     anchor_date        ISO date the forecast was struck (study anchor)
     anchor_price       price at anchor
     ccy                currency of price
     horizon_label      the cohort's horizon, and the record of WHICH CONVENTION
                        it was struck under. See HORIZON CONVENTION below.
                          "1 month" / "3 months"  calendar-anchored (from 27-Jul-2026)
                          "1 month" / "3 months"         retired session count (before that)
                          "12 months"             annual metals cohort
     grade_date         ISO date the horizon matures / is graded
     cycle_no           rolling-cycle number for this instrument (1,2,3…)
     reanchor_from      anchor_date of the prior cycle this supersedes, or null
     p5..p95            predicted percentile path values at the horizon
     touch              relative touch-probability bands from anchor:
                          { "+5":%, "+10":%, "+15":%, "+20":%, "-5":%, "-10":% }
     --- grade-time (null until graded) ---
     realized_close     close at grade_date
     realized_high      highest close reached within the horizon window
     realized_low       lowest close reached within the horizon window
     in_90              realized_close within [p5,p95]?            (bool|null)
     in_50              realized_close within [p25,p75]?           (bool|null)
     realized_quantile  empirical quantile of realized_close in the dist (0..1)
     median_err         realized_close − p50 (signed)
     touch_hit          per-band hit flags filled at grade time:
                          { "+5":bool, "+10":bool, "+15":bool, "+20":bool,
                            "-5":bool, "-10":bool }
   ----------------------------------------------------------------------------
   HORIZON CONVENTION — CHANGED 27-JUL-2026. READ BEFORE ADDING A ROW.
   ----------------------------------------------------------------------------
   Cohorts struck ON OR AFTER 27-Jul-2026 are CALENDAR-anchored:

     target_date = anchor_date + 1 (or 3) calendar months, month-end clamped
                   (31-Jan +1M -> 28/29-Feb).
     grade_date  = the first REAL trading session on or after target_date on
                   that exchange's own calendar. Weekend/holiday rolls FORWARD,
                   never back.
     horizon_days = the session count that maps onto that calendar span. It is
                   NOT a constant: 18-24 sessions for a month and 55-67 for a
                   quarter, depending on market and anchor. At publish time it
                   is projected from the exchange's own realized calendar by
                   engine/horizons.py (resolve()); at GRADE time the real
                   calendar decides and the projection is discarded.

   Cohorts struck BEFORE 27-Jul-2026 are session-counted: horizon_days was
   fixed at exactly 20 or 60 and grade_date was a projected Sun-Thu target with
   no holiday awareness (which is why several carry grade_date_projected +
   grade_note corrections). THOSE ROWS ARE NOT RE-LABELLED AND NOT RE-STRUCK.
   The register is append-only: every legacy cohort grades on the horizon it
   was issued on and counts in the score exactly as before. Both conventions
   coexist here, and horizon_label is what tells them apart.

   Why the change: "1 month" is roughly a month and "3 months" roughly a quarter, but
   only roughly, and the drift was in the check DATE — every public holiday
   pushed it, so the published grade_date was regularly 2 sessions wrong and
   needed a manual correction note. A calendar target cannot drift; only which
   session it lands on can, and by at most a few days.
   ========================================================================== */
const LEDGER = [
  // ---- XPTUSD · metal (spot platinum, USD) · cycle 1 (20 Jul 2026 published study; PARITY — own provisional self-fit, first metals name with a de-circularized cross-check) ----
  { instrument:"XPTUSD", asset_class:"metal", anchor_date:"2026-07-20", anchor_price:1608.37, ccy:"USD",
    horizon_label:"1 month", grade_date:"2026-08-20", grade_basis:"projected", cycle_no:1, reanchor_from:null,
    anchor_vol:0.3356, horizon_days:23,
    note:"PARITY single-instrument Step-0, own OHLC, under platinum\u2019s own PROVISIONAL self-fit (mc_v3 carry-anchored YZ-HAR-t: nu=Gaussian, cone width 0.853 \u2014 the MLE scale was 0.790 and the house clip floor bound it at 0.853; single-name fit, flagged circular exactly as gold\u2019s first fit was). 62 non-overlapping 60-session windows, origins 05-Jan-2012 \u2192 13-Feb-2026, after the Step-0.0 data-quality gate (4,041 \u2192 4,032 rows; 260.0 rows/yr = the metals Mon\u2013Fri calendar; zero corporate-action repairs). Scale-normalized CRPS skill \u22120.04% vs a CARRY-ANCHORED lognormal random-walk benchmark, robust verdict PARITY across bootstrap blocks {2,3,4} (block-2 CI [\u22120.9%, +0.9%]). De-circularized cross-check \u2014 fit trained on gold+silver only, platinum fully out-of-sample: \u22121.14%, CI [\u22123.2%, +0.9%], PARITY. Borrowed live METALS config (Gaussian/1.0): \u22120.94%, PARITY. Platinum does NOT arrive failing (materiality-gate criterion). Coverage 50/80/90% = 48/81/93.5% (mildly over-covered at the tails); PIT mean 0.489 \u2014 centred. Reproduction check: this session\u2019s chain reproduced the live gold registry EXACTLY (67 windows, +0.35%, CI[\u22120.5%,+1.3%], PARITY). Carry = Fed funds midpoint 3.63% (held, statement 17-Jun-2026), q = 0 (zero-yield store of value; the lease rate is a user\u2019s borrow cost, not a holder yield) \u2014 metals run CARRY-ONLY, no signal, no factor drift. METALS REMAIN THE WEAKEST CALIBRATION IN THE SYSTEM (gold self-fit; silver borrows gold\u2019s; platinum provisional until the metals panel pools \u2014 the pooled 3-metal fit, nu\u224820/width 0.965 on 148 windows, is the likely future config, not adopted). The cone is a 1/3-month object and is NEVER blended with the undated fair-value zone. See study \u00a73, Appendix B, and the Calibration Ledger.",
    p5:1381.97, p25:1514.01, p50:1612.84, p75:1718.44, p95:1881.84,
    touch:{ "+5":53, "+10":26, "+15":11, "+20":4, "-5":49, "-10":21 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  ,
    grade_note:"Grade-date corrected on 2026-07-29: stored value (2026-08-17) was computed by the retired session-projection method at publish time; recomputed via the live calendar-target rule (horizons.resolve, anchor + calendar month(s), first real session on/after). Cohort not yet matured -- forecast (p5-p95, touch) unchanged."
  },
  { instrument:"XPTUSD", asset_class:"metal", anchor_date:"2026-07-20", anchor_price:1608.37, ccy:"USD",
    horizon_label:"3 months", grade_date:"2026-10-20", grade_basis:"projected", cycle_no:1, reanchor_from:null,
    anchor_vol:0.3395, horizon_days:66,
    note:"PARITY single-instrument Step-0, own OHLC, under platinum\u2019s own PROVISIONAL self-fit (mc_v3 carry-anchored YZ-HAR-t: nu=Gaussian, cone width 0.853 \u2014 the MLE scale was 0.790 and the house clip floor bound it at 0.853; single-name fit, flagged circular exactly as gold\u2019s first fit was). 62 non-overlapping 60-session windows, origins 05-Jan-2012 \u2192 13-Feb-2026, after the Step-0.0 data-quality gate (4,041 \u2192 4,032 rows; 260.0 rows/yr = the metals Mon\u2013Fri calendar; zero corporate-action repairs). Scale-normalized CRPS skill \u22120.04% vs a CARRY-ANCHORED lognormal random-walk benchmark, robust verdict PARITY across bootstrap blocks {2,3,4} (block-2 CI [\u22120.9%, +0.9%]). De-circularized cross-check \u2014 fit trained on gold+silver only, platinum fully out-of-sample: \u22121.14%, CI [\u22123.2%, +0.9%], PARITY. Borrowed live METALS config (Gaussian/1.0): \u22120.94%, PARITY. Platinum does NOT arrive failing (materiality-gate criterion). Coverage 50/80/90% = 48/81/93.5% (mildly over-covered at the tails); PIT mean 0.489 \u2014 centred. Reproduction check: this session\u2019s chain reproduced the live gold registry EXACTLY (67 windows, +0.35%, CI[\u22120.5%,+1.3%], PARITY). Carry = Fed funds midpoint 3.63% (held, statement 17-Jun-2026), q = 0 (zero-yield store of value; the lease rate is a user\u2019s borrow cost, not a holder yield) \u2014 metals run CARRY-ONLY, no signal, no factor drift. METALS REMAIN THE WEAKEST CALIBRATION IN THE SYSTEM (gold self-fit; silver borrows gold\u2019s; platinum provisional until the metals panel pools \u2014 the pooled 3-metal fit, nu\u224820/width 0.965 on 148 windows, is the likely future config, not adopted). The cone is a 1/3-month object and is NEVER blended with the undated fair-value zone. See study \u00a73, Appendix B, and the Calibration Ledger.",
    p5:1238.91, p25:1452.81, p50:1623.02, p75:1813.36, p95:2128.49,
    touch:{ "+5":73, "+10":53, "+15":38, "+20":26, "-5":69, "-10":46 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  ,
    grade_note:"Grade-date corrected on 2026-07-29: stored value (2026-10-12) was computed by the retired session-projection method at publish time; recomputed via the live calendar-target rule (horizons.resolve, anchor + calendar month(s), first real session on/after). Cohort not yet matured -- forecast (p5-p95, touch) unchanged."
  },
  // ---- DSCW · equity (EGX Egypt) · cycle 1 (19 Jul 2026 published study; BOUNDARY(PARITY-flagged) — own fitted verdict, first-coverage name) ----
  // ---- CLHO \u00b7 equity (EGX Egypt) \u00b7 cycle 1 (13 Jul 2026 published study; PARITY \u2014 own fitted verdict, 29-name EG panel) ----
  // ---- RMDA \u00b7 equity (EGX Egypt) \u00b7 cycle 1 (13 Jul 2026 published study; MC PASS \u2014 own fitted verdict, 28-name EG panel) ----
  // ---- DEWA · other (DFM UAE) · cycle 1 (12 Jul 2026 published study; MC BOUNDARY, PARITY-flagged -- calibrated, no single-name edge) ----
  // ---- LULU · other (ADX UAE) · cycle 1 (12 Jul 2026 published study v3; NO NAME-LEVEL CALIBRATION — market-panel validated only) ----

  // ---- BURJEEL \u00b7 other (ADX UAE) \u00b7 cycle 1 (11 Jul 2026 published study, v4 reissued 12 Jul 2026; MC PARITY -- calibrated, no single-name edge) ----

  // ---- SALIK · other (DFM UAE) · cycle 1 (12 Jul 2026 published study v3; MC PARITY -- calibrated, no single-name edge) ----
  // ---- DIB · other (DFM UAE) · cycle 1 (11 Jul 2026 published study; MC FAILED calibration — indicative only) ----

  // ---- 2POINTZERO · other (ADX UAE) · cycle 1 (11 Jul 2026 published study; production UAE panel constituent, PARITY / matches benchmark) ----
  // ---- EAND · other (ADX UAE) · cycle 1 (11 Jul 2026 published study; production UAE panel fit, PARITY) ----
  // ---- ADCB · other (ADX UAE) · cycle 1 (10 Jul 2026 published study; MC PASSES benchmark robustly, carry drift) ----
  // ---- AGTHIA · other (ADX UAE) · cycle 1 (8 Jul 2026 published study; MC FAILS the calibration back-test — indicative only) ----
  // ---- GBCO · equity (EGX Egypt) · cycle 1 (8 Jul 2026 published study; MC PASSES benchmark, secular drift ON) ----
  // ---- RIBL · other (TADAWUL Saudi Arabia) · cycle 1 (09 Jul 2026 published study; MC PASSES benchmark marginally, zero drift) ----
  // ---- STC · equity (TADAWUL Saudi Arabia) · cycle 1 (09 Jul 2026 published study; MC PASSES benchmark, zero drift) ----
  // ---- ALDAR · other (ADX UAE) · cycle 1 (8 Jul 2026 published study; MC PASSES benchmark) ----
  // ---- EMAARDEV · other (DFM UAE) · cycle 1 (8 Jul 2026 published study; MC matches benchmark, indicative) ----
  // ---- ISPH \u00b7 equity (EGX Egypt) \u00b7 cycle 1 (7 Jul 2026 published study; MC FAILED benchmark, indicative) ----


  // ---- INFY · other (NSE India) · cycle 1 (6 Jul 2026 published study) ----



  // ---- PHDC · equity · cycle 2 (11 Jun 2026 published study) ----
  {
    instrument:"PHDC", asset_class:"equity",
    anchor_date:"2026-06-11", anchor_price:14.50, ccy:"EGP",
    horizon_label:"1 month", grade_date:"2026-07-13", cycle_no:2, reanchor_from:"2026-06-09",
    grade_date_projected:"2026-07-09", grade_note:"Projected grade_date (Sun\u2013Thu calendar, no holiday awareness) landed on only the 18th real trading session, 2 short of a true 1-month; graded instead on the actual 20th session close.",
    p5:11.53, p25:13.42, p50:14.92, p75:16.56, p95:19.32,
    touch:{ "+5":62, "+10":38, "+15":21, "+20":12, "-5":55, "-10":33 },
    realized_close:14.85, realized_high:16.43, realized_low:14.26,
    in_90:true, in_50:true, realized_quantile:0.488, median_err:-0.0047,
    touch_hit:{ "+5":true, "+10":true, "+15":false, "+20":false, "-5":false, "-10":false }
  },
  // ---- TMGH · equity · cycle 1 (15 Jun 2026 published study) ----
  {
    instrument:"TMGH", asset_class:"equity",
    anchor_date:"2026-06-15", anchor_price:95.68, ccy:"EGP",
    horizon_label:"1 month", grade_date:"2026-07-15", cycle_no:1, reanchor_from:null,
    grade_date_projected:"2026-07-13", grade_note:"Projected grade_date (Sun\u2013Thu calendar, no holiday awareness) fell 2 sessions short of a true 1-month; graded on the actual 20th session close.",
    p5:81.42, p25:91.17, p50:98.31, p75:106.10, p95:119.24,
    touch:{ "+5":66, "+10":24, "+15":8, "+20":2, "-5":29, "-10":11 },
    realized_close:101.01, realized_high:101.99, realized_low:92.10,
    in_90:true, in_50:true, realized_quantile:0.587, median_err:0.0275,
    touch_hit:{ "+5":true, "+10":false, "+15":false, "+20":false, "-5":false, "-10":false }
  },
  // ---- EMFD · equity · cycle 1 (17 Jun 2026 published study) ----
  {
    instrument:"EMFD", asset_class:"equity",
    anchor_date:"2026-06-17", anchor_price:12.44, ccy:"EGP",
    horizon_label:"1 month", grade_date:"2026-07-19", cycle_no:1, reanchor_from:null,
    grade_date_projected:"2026-07-15", grade_note:"Projected grade_date (Sun\u2013Thu calendar, no holiday awareness) fell 2 sessions short of a true 1-month; graded on the actual 20th session close.",
    p5:10.50, p25:11.80, p50:12.75, p75:13.78, p95:15.46,
    touch:{ "+5":64, "+10":41, "+15":24, "+20":13, "-5":49, "-10":23 },
    realized_close:11.70, realized_high:12.57, realized_low:11.24,
    in_90:true, in_50:false, realized_quantile:0.235, median_err:-0.0824,
    touch_hit:{ "+5":false, "+10":false, "+15":false, "+20":false, "-5":true, "-10":false }
  },

  // ---- OCDI · equity · cycle 1 (24 Jun 2026 published study) ----
  {
    instrument:"OCDI", asset_class:"equity",
    anchor_date:"2026-06-23", anchor_price:22.80, ccy:"EGP",
    horizon_label:"1 month", grade_date:"2026-07-22", cycle_no:1, reanchor_from:null,
    anchor_date_stated:"2026-06-24",
    grade_date_projected:"2026-07-21",
    grade_note:"Two stacked corrections. (1) anchor_date was mislabeled by one session at original publish (24-Jun-2026 study): anchor_price 22.80 is EGX's 23-Jun close, not 24-Jun (which closed 24.23) — confirmed via the carry-anchored 1-month drift, spot 22.80 reproduces the published p50 (23.21) to within 0.4% while spot 24.23 misses by +5.9%, so the cohort was genuinely struck off the 23-Jun close. p5–p95 and touch probabilities are computed off that spot and are unchanged. (2) Because the true anchor session moves a day earlier, the true 1-month (20th actual trading row from 23-Jun) is 22-Jul close 27.50, not 26-Jul close 27.10 as this cohort was first graded earlier in this same session — that grading incorrectly counted 20 sessions from the STATED 24-Jun label. Corrected to the 22-Jul close; the naive Sun–Thu calendar projection (grade_date_projected, holiday-blind either way) is left as originally computed.",
    p5:18.31, p25:21.08, p50:23.21, p75:25.56, p95:29.35,
    touch:{ "+5":66, "+10":45, "+15":28, "+20":17, "-5":56, "-10":32 },
    realized_close:27.5, realized_high:28.7, realized_low:22.86,
    in_90:true, in_50:false, realized_quantile:0.852, median_err:0.1848,
    touch_hit:{ "+5":true, "+10":true, "+15":true, "+20":true, "-5":false, "-10":false }
  },
  // ---- ORHD · equity · cycle 1 (25 Jun 2026 published study; anchored 24 Jun) ----
  {
    instrument:"ORHD", asset_class:"equity",
    anchor_date:"2026-06-24", anchor_price:39.30, ccy:"EGP",
    horizon_label:"1 month", grade_date:"2026-07-26", cycle_no:1, reanchor_from:null,
    grade_date_projected:"2026-07-21",
    grade_note:"Projected grade_date (Sun–Thu calendar, no holiday awareness) fell 3 sessions short of a true 1-month — EGX was closed 2 Jul and 23 Jul (Revolution Day); graded on the actual 20th session close.",
    p5:32.54, p25:36.93, p50:40.22, p75:43.82, p95:49.64,
    touch:{ "+5":60, "+10":43, "+15":28, "+20":16, "-5":48, "-10":28 },
    realized_close:39.9, realized_high:40.8, realized_low:37,
    in_90:true, in_50:true, realized_quantile:0.476, median_err:-0.008,
    touch_hit:{ "+5":false, "+10":false, "+15":false, "+20":false, "-5":true, "-10":false }
  },
  // ---- COMI · equity · cycle 1 (29 Jun 2026 published study) ----
  {
    instrument:"COMI", asset_class:"equity",
    anchor_date:"2026-06-29", anchor_price:126.89, ccy:"EGP",
    anchor_price_published:129.25, anchor_note:"Anchor corrected 28-Jul-2026: the published anchor_price was captured MID-SESSION (inside that day\u2019s range) rather than at the close. Corrected to the actual close. The forecast itself is untouched \u2014 p5..p95, the touch probabilities and the grade are exactly as published; only the anchor field was wrong. Re-striking was rejected: today\u2019s fit runs on 15-year libraries that did not exist at the anchor date, so it would re-grade a published forecast with hindsight.",
    horizon_label:"1 month", grade_date:"2026-07-28", grade_basis:"actual", cycle_no:1, reanchor_from:null,
    grade_date_projected:"2026-07-27", grade_note:"Graded as of 2026-07-28, the latest available close, at the owner's direction. This is session 19 from the 29-Jun anchor; the full 1-month session and the 1-month calendar target both fall on 2026-07-29. Recorded on 19 of 20 sessions -- the band verdict is unaffected (142.00 sits well inside 103.44-159.92) but realized_quantile, median_err and the +10%/+15% touch outcomes are measured one session early.",
    p5:103.44, p25:117.89, p50:128.87, p75:140.85, p95:159.92,
    touch:{ "+5":61, "+10":40, "+15":23, "+20":13, "-5":62, "-10":38 },
    realized_close:142.00, realized_high:142.55, realized_low:126.89,
    in_90:true, in_50:false, realized_quantile:0.762, median_err:0.1019,
    touch_hit:{ "+5":true, "+10":true, "+15":false, "+20":false, "-5":false, "-10":false }
  },
  {
    instrument:"Gold", asset_class:"metal",
    anchor_date:"2026-06-25", anchor_price:3989.85, ccy:"USD",
    horizon_label:"1 month", grade_date:"2026-07-23", cycle_no:1, reanchor_from:null,
    p5:3431, p25:3754, p50:3975, p75:4214, p95:4598,
    touch:{ "+5":49, "+10":22, "+15":9, "+20":3, "-5":50, "-10":20 },
    realized_close:4048.78, realized_high:4202.67, realized_low:3944.23,
    in_90:true, in_50:true, realized_quantile:0.577, median_err:0.0186,
    touch_hit:{ "+5":true, "+10":false, "+15":false, "+20":false, "-5":false, "-10":false }
  },
  {
    instrument:"Gold", asset_class:"metal",
    anchor_date:"2026-06-25", anchor_price:3989.85, ccy:"USD",
    horizon_label:"12 months", grade_date:"2027-06-25", cycle_no:1, reanchor_from:null,
    p5:2624, p25:3515, p50:4295, p75:5246, p95:7026,
    touch:{ "+5":88, "+10":77, "+15":67, "+20":57, "-5":76, "-10":59 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"Gold", asset_class:"metal",
    anchor_date:"2026-07-27", anchor_price:4090.87, ccy:"USD",
    horizon_label:"1 month", grade_date:"2026-08-27", grade_basis:"projected", horizon_days:23, cycle_no:2, reanchor_from:"2026-06-25",
    note:"Cycle 2 roll-forward, 27-Jul-2026. Production chain, no approximation: Step 0.0 data-quality gate \u2192 YZ variance proxy \u2192 fit_har_v3 \u2192 har_forecast_v3 \u2192 carry drift ln(1+rf_live)\u2212ln(1+q) \u2192 simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED \u2014 house convention; drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). Metals live fit nu=20, width_cal=1.035; rf_live 3.63% (USD carry, q=0 by construction for a zero-yield metal). METALS REMAINS THE WEAKEST CALIBRATION IN THE SYSTEM \u2014 a 2-name panel, read the cone accordingly.",
    p5:3725, p25:3948, p50:4102, p75:4263, p95:4516,
    touch:{ "+5":34, "+10":9, "+15":2, "+20":0, "-5":30, "-10":5 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  ,
    grade_note:"Grade-date corrected on 2026-07-29: stored value (2026-08-24) was computed by the retired session-projection method at publish time; recomputed via the live calendar-target rule (horizons.resolve, anchor + calendar month(s), first real session on/after). Cohort not yet matured -- forecast (p5-p95, touch) unchanged."
  },
  {
    instrument:"Gold", asset_class:"metal",
    anchor_date:"2026-07-27", anchor_price:4090.87, ccy:"USD",
    horizon_label:"3 months", grade_date:"2026-10-27", grade_basis:"projected", horizon_days:66, cycle_no:2, reanchor_from:"2026-06-25",
    note:"Cycle 2 roll-forward, 27-Jul-2026. Production chain, no approximation: Step 0.0 data-quality gate \u2192 YZ variance proxy \u2192 fit_har_v3 \u2192 har_forecast_v3 \u2192 carry drift ln(1+rf_live)\u2212ln(1+q) \u2192 simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED \u2014 house convention; drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). Metals live fit nu=20, width_cal=1.035; rf_live 3.63% (USD carry, q=0 by construction for a zero-yield metal). METALS REMAINS THE WEAKEST CALIBRATION IN THE SYSTEM \u2014 a 2-name panel, read the cone accordingly.",
    p5:3493, p25:3862, p50:4127, p75:4410, p95:4880,
    touch:{ "+5":60, "+10":33, "+15":16, "+20":7, "-5":53, "-10":23 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  ,
    grade_note:"Grade-date corrected on 2026-07-29: stored value (2026-10-19) was computed by the retired session-projection method at publish time; recomputed via the live calendar-target rule (horizons.resolve, anchor + calendar month(s), first real session on/after). Cohort not yet matured -- forecast (p5-p95, touch) unchanged."
  },
  // ---- Silver (XAG/USD) · metal · cycle 1 (05 Jul 2026 published study; anchored 03 Jul close) ----
  {
    instrument:"Silver", asset_class:"metal",
    anchor_date:"2026-07-03", anchor_price:62.43, ccy:"USD",
    horizon_label:"1 month", grade_date:"2026-08-03", grade_basis:"projected", horizon_days:22, cycle_no:1, reanchor_from:null,
    p5:50, p25:58, p50:63, p75:68, p95:78,
    touch:{ "+5":61, "+10":38, "+15":23, "+20":14, "-5":56, "-10":31 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  ,
    grade_note:"Grade-date corrected on 2026-07-29: stored value (2026-07-31) was computed by the retired session-projection method at publish time; recomputed via the live calendar-target rule (horizons.resolve, anchor + calendar month(s), first real session on/after). Cohort not yet matured -- forecast (p5-p95, touch) unchanged."
  },
  {
    instrument:"Silver", asset_class:"metal",
    anchor_date:"2026-07-03", anchor_price:62.43, ccy:"USD",
    horizon_label:"3 months", grade_date:"2026-10-05", grade_basis:"projected", horizon_days:66, cycle_no:1, reanchor_from:null,
    p5:44, p25:56, p50:63, p75:72, p95:91,
    touch:{ "+5":76, "+10":60, "+15":46, "+20":35, "-5":71, "-10":51 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  ,
    grade_note:"Grade-date corrected on 2026-07-29: stored value (2026-09-25) was computed by the retired session-projection method at publish time; recomputed via the live calendar-target rule (horizons.resolve, anchor + calendar month(s), first real session on/after). Cohort not yet matured -- forecast (p5-p95, touch) unchanged."
  },
  {
    instrument:"Silver", asset_class:"metal",
    anchor_date:"2026-07-03", anchor_price:62.43, ccy:"USD",
    horizon_label:"12 months", grade_date:"2027-07-05", grade_basis:"projected", horizon_days:260, cycle_no:1, reanchor_from:null,
    p5:34, p25:52, p50:67, p75:86, p95:135,
    touch:{ "+5":89, "+10":80, "+15":72, "+20":65, "-5":83, "-10":70 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  ,
    grade_note:"Grade-date corrected on 2026-07-29: stored value (2027-07-02) was computed by the retired session-projection method at publish time; recomputed via the live calendar-target rule (horizons.resolve, anchor + calendar month(s), first real session on/after). Cohort not yet matured -- forecast (p5-p95, touch) unchanged."
  },
  // ---- Samsung Electronics (KRX:005930) · other / international · cycle 1 (27 Jun 2026 published study; anchored 26 Jun close) ----
  {
    instrument:"Samsung", asset_class:"other",
    anchor_date:"2026-06-26", anchor_price:339500, ccy:"KRW",
    horizon_label:"1 month", grade_date:"2026-07-27", cycle_no:1, reanchor_from:null,
    grade_date_projected:"2026-07-24",
    grade_note:"Projected grade_date (Mon–Fri calendar, no holiday awareness) fell 1 session short of a true 1-month — KRX was closed 17 Jul (reinstated Constitution Day); graded on the actual 20th session close. Closed BELOW the published p5, so realized_quantile is left-censored (<0.05) and recorded null rather than extrapolated.",
    p5:277676, p25:316898, p50:346091, p75:378203, p95:430413,
    touch:{ "+5":68, "+10":48, "+15":31, "+20":18, "-5":72, "-10":44 },   // interpolated from the study's absolute touch ladder — replace with the model's exact relative barrier-hit probabilities before these bands are graded
    realized_close:254000, realized_high:343000, realized_low:240000,
    in_90:false, in_50:false, realized_quantile:null, median_err:-0.2661,
    touch_hit:{ "+5":false, "+10":false, "+15":false, "+20":false, "-5":true, "-10":true }
  },
  {
    instrument:"Samsung", asset_class:"other",
    anchor_date:"2026-07-27", anchor_price:254000, ccy:"KRW",
    horizon_label:"1 month", grade_date:"2026-08-27", grade_basis:"projected", horizon_days:22, cycle_no:2, reanchor_from:"2026-06-26",
    config_note:"Corrected 29-Jul-2026: this cycle was originally struck with the prior market-default fit; the per-name override decided the same day (see engine/fit_overrides.json) genuinely improves this specific name's own LONO verdict, so the anchor/grade dates are unchanged but the distribution was recomputed under the correct config.",
    note:"Cycle 2 roll-forward, 27-Jul-2026. Production chain, no approximation: Step 0.0 data-quality gate \u2192 YZ variance proxy \u2192 fit_har_v3 \u2192 har_forecast_v3 \u2192 carry drift ln(1+rf_live)\u2212ln(1+q) \u2192 simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED \u2014 house convention; drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). KR live fit nu=Gaussian, width_cal=1.154; rf_live 3.00% (placeholder KTB anchor). STRUCK ON THE INCUMBENT FIT BY DESIGN: the 15-year Samsung history ingested this session refits KR to nu=12/width_cal=1.105 (published 90% cone \u22125.3%), which trips the materiality gate and is therefore held on a feature branch pending PR review, not applied to production.",
    p5:154820.6, p25:193612.78, p50:220362.84, p75:251038.64, p95:313821.44,
    touch:{ "+5":71, "+10":55, "+15":41, "+20":30, "-5":69, "-10":50 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  ,
    grade_note:"Grade-date corrected on 2026-07-29: stored value (2026-08-24) was computed by the retired session-projection method at publish time; recomputed via the live calendar-target rule (horizons.resolve, anchor + calendar month(s), first real session on/after). Cohort not yet matured -- forecast (p5-p95, touch) unchanged."
  },
  {
    instrument:"Samsung", asset_class:"other",
    anchor_date:"2026-07-27", anchor_price:254000, ccy:"KRW",
    horizon_label:"3 months", grade_date:"2026-10-27", grade_basis:"projected", horizon_days:62, cycle_no:2, reanchor_from:"2026-06-26",
    config_note:"Corrected 29-Jul-2026: this cycle was originally struck with the prior market-default fit; the per-name override decided the same day (see engine/fit_overrides.json) genuinely improves this specific name's own LONO verdict, so the anchor/grade dates are unchanged but the distribution was recomputed under the correct config.",
    note:"Cycle 2 roll-forward, 27-Jul-2026. Production chain, no approximation: Step 0.0 data-quality gate \u2192 YZ variance proxy \u2192 fit_har_v3 \u2192 har_forecast_v3 \u2192 carry drift ln(1+rf_live)\u2212ln(1+q) \u2192 simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED \u2014 house convention; drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). KR live fit nu=Gaussian, width_cal=1.154; rf_live 3.00% (placeholder KTB anchor). STRUCK ON THE INCUMBENT FIT BY DESIGN: the 15-year Samsung history ingested this session refits KR to nu=12/width_cal=1.105 (published 90% cone \u22125.3%), which trips the materiality gate and is therefore held on a feature branch pending PR review, not applied to production.",
    p5:129392.31, p25:181881.54, p50:222199.19, p75:270912.64, p95:381214.94,
    touch:{ "+5":82, "+10":70, "+15":59, "+20":50, "-5":80, "-10":66 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  ,
    grade_note:"Grade-date corrected on 2026-07-29: stored value (2026-10-19) was computed by the retired session-projection method at publish time; recomputed via the live calendar-target rule (horizons.resolve, anchor + calendar month(s), first real session on/after). Cohort not yet matured -- forecast (p5-p95, touch) unchanged."
  },
  // ---- Kakao Corp. (KRX:035720) · other / international · cycle 1 (28 Jun 2026 published study; anchored 26 Jun close) ----
  {
    instrument:"Kakao", asset_class:"other",
    anchor_date:"2026-06-26", anchor_price:33150, ccy:"KRW",
    horizon_label:"1 month", grade_date:"2026-07-27", grade_basis:"actual", cycle_no:1, reanchor_from:null,
    grade_date_projected:"2026-07-24", grade_note:"Projected grade_date (weekday calendar target, no holiday awareness) fell 3 sessions short of a true 1-month; graded on the actual 20th session close.",
    p5:25404, p25:29799, p50:33294, p75:37199, p95:43634,
    touch:{ "+5":68, "+10":49, "+15":34, "+20":22, "-5":65, "-10":43 },   // relative barrier-hit probabilities from the published model (reflection principle, discrete-monitoring correction)
    realized_close:37050, realized_high:37500, realized_low:32600,
    in_90:true, in_50:true, realized_quantile:0.74, median_err:0.1128,
    touch_hit:{ "+5":true, "+10":true, "+15":false, "+20":false, "-5":false, "-10":false }
  },
  // ---- LG Energy Solution (KRX:373220) · other / international · cycle 1 (28 Jun 2026 published study; anchored 26 Jun close) ----
  {
    instrument:"LGES", asset_class:"other",
    anchor_date:"2026-06-26", anchor_price:331500, ccy:"KRW",
    horizon_label:"1 month", grade_date:"2026-07-27", grade_basis:"actual", cycle_no:1, reanchor_from:null,
    grade_date_projected:"2026-07-24", grade_note:"Projected grade_date (weekday calendar target, no holiday awareness) fell 3 sessions short of a true 1-month; graded on the actual 20th session close.",
    p5:268200, p25:304400, p50:332400, p75:363000, p95:411900,
    touch:{ "+5":62, "+10":40, "+15":24, "+20":13, "-5":60, "-10":34 },   // relative barrier-hit probabilities from the published 50,000-path model (reflection principle, discrete-monitoring correction)
    realized_close:333000, realized_high:400500, realized_low:309500,
    in_90:true, in_50:true, realized_quantile:0.505, median_err:0.0018,
    touch_hit:{ "+5":true, "+10":true, "+15":true, "+20":true, "-5":true, "-10":false }
  },
  // ---- OIH · equity · cycle 1 (03 Jul 2026 published study) ----
  // ---- ORAS · equity · cycle 1 (30 Jun 2026 published study) ----
  // ---- TMPV · other (NSE India) · cycle 1 (30 Jun 2026 published study) ----
  {
    instrument:"TMPV", asset_class:"other",
    anchor_date:"2026-06-30", anchor_price:352.20, ccy:"INR",
    horizon_label:"1 month", grade_date:"2026-07-28", cycle_no:1, reanchor_from:null,
    p5:294, p25:327, p50:353, p75:379, p95:422,
    touch:{ "+5":57, "+10":33, "+15":17, "+20":7, "-5":56, "-10":30 },
    realized_close:324.15, realized_high:354.6, realized_low:318.25,
    in_90:true, in_50:false, realized_quantile:0.233, median_err:-8.17,
    touch_hit:{ "+5":false, "+10":false, "+15":false, "+20":false, "-5":true, "-10":false }
  },
  // ---- ARAMCO · other (TADAWUL Saudi Arabia) · cycle 1 (1 Jul 2026 published study) ----
  // ---- ADNOCGAS · other (ADX Abu Dhabi) · cycle 1 (4 Jul 2026 published study) ----
  // ---- ALRAJHI · other (TADAWUL Saudi Arabia) · cycle 1 (2 Jul 2026 published study) ----
  // ---- SNB · other (TADAWUL Saudi Arabia) · cycle 1 (2 Jul 2026 published study) ----
  // ---- ENBD · other (DFM UAE) · cycle 1 (3 Jul 2026 published study) ----
  // ---- ACWA · other (TADAWUL Saudi Arabia) · cycle 1 (5 Jul 2026 published study) ----
  // ---- FAB · other (ADX Abu Dhabi) · cycle 1 (3 Jul 2026 published study) ----
  // ---- EMAAR · other (DFM Dubai) · cycle 1 (01 Jul 2026 published study) ----
  // ---- TSLA · other (NASDAQ US) · cycle 1 (01 Jul 2026 published study) ----
  // ---- HELI · equity · cycle 1 (3 Jul 2026 published study) ----
  // ---- IHC · other (ADX Abu Dhabi) · cycle 1 (4 Jul 2026 published study) ----
  // ---- QNB \u00b7 other (QSE Qatar) \u00b7 cycle 1 (5 Jul 2026 published study) ----
  {
    instrument:"QNB", asset_class:"other",
    anchor_date:"2026-07-05", anchor_price:17.54, ccy:"QAR",
    horizon_label:"1 month", grade_date:"2026-08-05", grade_basis:"projected", cycle_no:1, reanchor_from:null,
    anchor_vol:0.18, horizon_days:22,
    p5:15.35, p25:16.74, p50:17.48, p75:18.19, p95:19.55,
    touch:{ "+5":30, "+10":11, "+15":4, "+20":1, "-5":34, "-10":12 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  ,
    grade_note:"Grade-date corrected on 2026-07-29: stored value (2026-08-02) was computed by the retired session-projection method at publish time; recomputed via the live calendar-target rule (horizons.resolve, anchor + calendar month(s), first real session on/after). Cohort not yet matured -- forecast (p5-p95, touch) unchanged."
  },
  {
    instrument:"QNB", asset_class:"other",
    anchor_date:"2026-07-05", anchor_price:17.54, ccy:"QAR",
    horizon_label:"3 months", grade_date:"2026-10-05", grade_basis:"projected", cycle_no:1, reanchor_from:null,
    anchor_vol:0.18, horizon_days:63,
    p5:13.96, p25:15.91, p50:17.24, p75:18.60, p95:20.91,
    touch:{ "+5":54, "+10":31, "+15":17, "+20":8, "-5":61, "-10":36 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  ,
    grade_note:"Grade-date corrected on 2026-07-29: stored value (2026-09-27) was computed by the retired session-projection method at publish time; recomputed via the live calendar-target rule (horizons.resolve, anchor + calendar month(s), first real session on/after). Cohort not yet matured -- forecast (p5-p95, touch) unchanged."
  },
  // ---- QGTS \u00b7 other (QSE Qatar) \u00b7 cycle 1 (5 Jul 2026 published study; MC ties benchmark, illustrative) ----

  // ---- 28-Jul-2026 MARKET-WIDE RE-STRIKE — EG/AE/SA onto the
  //      15-year calibration libraries + the calendar 1M/3M horizon
  //      convention. Append-only: every cohort above keeps the
  //      horizon and percentiles it was published with.
  {
    instrument:"ABUK", asset_class:"equity",
    anchor_date:"2026-07-22", anchor_price:72.3, ccy:"EGP",
    horizon_label:"1 month", grade_date:"2026-08-23", grade_basis:"projected", horizon_days:20,
    cycle_no:2, reanchor_from:"2026-07-01", anchor_vol:0.3824,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). EG live fit nu=6.0, width_cal=0.951; rf_live 19.50% CBE main operation rate. Horizon resolved by horizons.resolve() on EG's own realized calendar, not a session count.",
    p5:62.48, p25:69.13, p50:73.38, p75:77.92, p95:86.21,
    touch:{ "+5":55, "+10":29, "+15":14, "+20":7, "-5":43, "-10":18 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"ABUK", asset_class:"equity",
    anchor_date:"2026-07-22", anchor_price:72.3, ccy:"EGP",
    horizon_label:"3 months", grade_date:"2026-10-22", grade_basis:"projected", horizon_days:61,
    cycle_no:2, reanchor_from:"2026-07-01", anchor_vol:0.4019,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). EG live fit nu=6.0, width_cal=0.951; rf_live 19.50% CBE main operation rate. Horizon resolved by horizons.resolve() on EG's own realized calendar, not a session count.",
    p5:56.17, p25:67.8, p50:75.7, p75:84.36, p95:101.76,
    touch:{ "+5":78, "+10":60, "+15":45, "+20":33, "-5":61, "-10":38 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"ACWA", asset_class:"equity",
    anchor_date:"2026-07-26", anchor_price:191.2, ccy:"SAR",
    horizon_label:"1 month", grade_date:"2026-08-26", grade_basis:"projected", horizon_days:22,
    cycle_no:2, reanchor_from:"2026-07-05", anchor_vol:0.3434,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). SA live fit nu=12.0, width_cal=1.07; rf_live 4.25% SAMA repo-anchored estimate. Horizon resolved by horizons.resolve() on SA's own realized calendar, not a session count.",
    p5:161.06, p25:179.25, p50:191.75, p75:205.33, p95:228.76,
    touch:{ "+5":56, "+10":31, "+15":15, "+20":8, "-5":52, "-10":25 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"ACWA", asset_class:"equity",
    anchor_date:"2026-07-26", anchor_price:191.2, ccy:"SAR",
    horizon_label:"3 months", grade_date:"2026-10-26", grade_basis:"projected", horizon_days:62,
    cycle_no:2, reanchor_from:"2026-07-05", anchor_vol:0.3573,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). SA live fit nu=12.0, width_cal=1.07; rf_live 4.25% SAMA repo-anchored estimate. Horizon resolved by horizons.resolve() on SA's own realized calendar, not a session count.",
    p5:142.09, p25:171.5, p50:193.38, p75:217.8, p95:262.95,
    touch:{ "+5":74, "+10":56, "+15":41, "+20":29, "-5":70, "-10":48 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"ADCB", asset_class:"equity",
    anchor_date:"2026-07-24", anchor_price:14.42, ccy:"AED",
    horizon_label:"1 month", grade_date:"2026-08-24", grade_basis:"projected", horizon_days:20,
    cycle_no:2, reanchor_from:"2026-07-03", anchor_vol:0.3177,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). AE live fit nu=10.0, width_cal=0.979; rf_live 3.65% CBUAE base rate (AED peg -> Fed path). Horizon resolved by horizons.resolve() on AE's own realized calendar, not a session count.",
    p5:12.55, p25:13.7, p50:14.46, p75:15.27, p95:16.63,
    touch:{ "+5":48, "+10":21, "+15":8, "+20":3, "-5":44, "-10":16 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"ADCB", asset_class:"equity",
    anchor_date:"2026-07-24", anchor_price:14.42, ccy:"AED",
    horizon_label:"3 months", grade_date:"2026-10-26", grade_basis:"projected", horizon_days:63,
    cycle_no:2, reanchor_from:"2026-07-03", anchor_vol:0.3143,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). AE live fit nu=10.0, width_cal=0.979; rf_live 3.65% CBUAE base rate (AED peg -> Fed path). Horizon resolved by horizons.resolve() on AE's own realized calendar, not a session count.",
    p5:11.36, p25:13.24, p50:14.56, p75:16.01, p95:18.69,
    touch:{ "+5":70, "+10":48, "+15":32, "+20":21, "-5":64, "-10":39 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"ADIB", asset_class:"equity",
    anchor_date:"2026-07-22", anchor_price:49.3, ccy:"EGP",
    horizon_label:"1 month", grade_date:"2026-08-23", grade_basis:"projected", horizon_days:20,
    cycle_no:2, reanchor_from:"2026-07-01", anchor_vol:0.392,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). EG live fit nu=6.0, width_cal=0.951; rf_live 19.50% CBE main operation rate. Horizon resolved by horizons.resolve() on EG's own realized calendar, not a session count.",
    p5:42.43, p25:47.07, p50:50.03, p75:53.21, p95:59.02,
    touch:{ "+5":56, "+10":30, "+15":15, "+20":7, "-5":44, "-10":18 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"ADIB", asset_class:"equity",
    anchor_date:"2026-07-22", anchor_price:49.3, ccy:"EGP",
    horizon_label:"3 months", grade_date:"2026-10-22", grade_basis:"projected", horizon_days:61,
    cycle_no:2, reanchor_from:"2026-07-01", anchor_vol:0.43,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). EG live fit nu=6.0, width_cal=0.951; rf_live 19.50% CBE main operation rate. Horizon resolved by horizons.resolve() on EG's own realized calendar, not a session count.",
    p5:37.52, p25:45.88, p50:51.62, p75:57.96, p95:70.84,
    touch:{ "+5":79, "+10":62, "+15":47, "+20":35, "-5":64, "-10":41 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"ADIBUAE", asset_class:"equity",
    anchor_date:"2026-07-24", anchor_price:21.24, ccy:"AED",
    horizon_label:"1 month", grade_date:"2026-08-24", grade_basis:"projected", horizon_days:20,
    cycle_no:2, reanchor_from:null, anchor_vol:0.3158,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). AE live fit nu=10.0, width_cal=0.979; rf_live 3.65% CBUAE base rate (AED peg -> Fed path). Horizon resolved by horizons.resolve() on AE's own realized calendar, not a session count.",
    p5:18.5, p25:20.18, p50:21.3, p75:22.49, p95:24.47,
    touch:{ "+5":48, "+10":21, "+15":8, "+20":3, "-5":43, "-10":16 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"ADIBUAE", asset_class:"equity",
    anchor_date:"2026-07-24", anchor_price:21.24, ccy:"AED",
    horizon_label:"3 months", grade_date:"2026-10-26", grade_basis:"projected", horizon_days:63,
    cycle_no:2, reanchor_from:null, anchor_vol:0.3143,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). AE live fit nu=10.0, width_cal=0.979; rf_live 3.65% CBUAE base rate (AED peg -> Fed path). Horizon resolved by horizons.resolve() on AE's own realized calendar, not a session count.",
    p5:16.73, p25:19.5, p50:21.45, p75:23.59, p95:27.53,
    touch:{ "+5":70, "+10":48, "+15":32, "+20":21, "-5":64, "-10":39 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"ADNOCGAS", asset_class:"equity",
    anchor_date:"2026-07-24", anchor_price:3.34, ccy:"AED",
    horizon_label:"1 month", grade_date:"2026-08-24", grade_basis:"projected", horizon_days:20,
    cycle_no:2, reanchor_from:"2026-07-03", anchor_vol:0.1913,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). AE live fit nu=10.0, width_cal=0.979; rf_live 3.65% CBUAE base rate (AED peg -> Fed path). Horizon resolved by horizons.resolve() on AE's own realized calendar, not a session count.",
    p5:3.08, p25:3.24, p50:3.35, p75:3.46, p95:3.64,
    touch:{ "+5":29, "+10":6, "+15":1, "+20":0, "-5":23, "-10":3 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"ADNOCGAS", asset_class:"equity",
    anchor_date:"2026-07-24", anchor_price:3.34, ccy:"AED",
    horizon_label:"3 months", grade_date:"2026-10-26", grade_basis:"projected", horizon_days:63,
    cycle_no:2, reanchor_from:"2026-07-03", anchor_vol:0.2009,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). AE live fit nu=10.0, width_cal=0.979; rf_live 3.65% CBUAE base rate (AED peg -> Fed path). Horizon resolved by horizons.resolve() on AE's own realized calendar, not a session count.",
    p5:2.88, p25:3.17, p50:3.37, p75:3.58, p95:3.96,
    touch:{ "+5":58, "+10":30, "+15":14, "+20":7, "-5":49, "-10":20 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"AGTHIA", asset_class:"equity",
    anchor_date:"2026-07-24", anchor_price:3.2, ccy:"AED",
    horizon_label:"1 month", grade_date:"2026-08-24", grade_basis:"projected", horizon_days:20,
    cycle_no:2, reanchor_from:"2026-07-06", anchor_vol:0.2585,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). AE live fit nu=10.0, width_cal=0.979; rf_live 3.65% CBUAE base rate (AED peg -> Fed path). Horizon resolved by horizons.resolve() on AE's own realized calendar, not a session count.",
    p5:2.86, p25:3.07, p50:3.21, p75:3.36, p95:3.59,
    touch:{ "+5":40, "+10":14, "+15":4, "+20":1, "-5":36, "-10":10 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"AGTHIA", asset_class:"equity",
    anchor_date:"2026-07-24", anchor_price:3.2, ccy:"AED",
    horizon_label:"3 months", grade_date:"2026-10-26", grade_basis:"projected", horizon_days:63,
    cycle_no:2, reanchor_from:"2026-07-06", anchor_vol:0.2743,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). AE live fit nu=10.0, width_cal=0.979; rf_live 3.65% CBUAE base rate (AED peg -> Fed path). Horizon resolved by horizons.resolve() on AE's own realized calendar, not a session count.",
    p5:2.6, p25:2.97, p50:3.23, p75:3.51, p95:4.02,
    touch:{ "+5":66, "+10":43, "+15":26, "+20":15, "-5":60, "-10":34 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"ALDAR", asset_class:"equity",
    anchor_date:"2026-07-24", anchor_price:7.61, ccy:"AED",
    horizon_label:"1 month", grade_date:"2026-08-24", grade_basis:"projected", horizon_days:20,
    cycle_no:2, reanchor_from:"2026-07-03", anchor_vol:0.3119,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). AE live fit nu=10.0, width_cal=0.979; rf_live 3.65% CBUAE base rate (AED peg -> Fed path). Horizon resolved by horizons.resolve() on AE's own realized calendar, not a session count.",
    p5:6.64, p25:7.24, p50:7.63, p75:8.05, p95:8.75,
    touch:{ "+5":47, "+10":21, "+15":8, "+20":3, "-5":43, "-10":15 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"ALDAR", asset_class:"equity",
    anchor_date:"2026-07-24", anchor_price:7.61, ccy:"AED",
    horizon_label:"3 months", grade_date:"2026-10-26", grade_basis:"projected", horizon_days:63,
    cycle_no:2, reanchor_from:"2026-07-03", anchor_vol:0.3246,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). AE live fit nu=10.0, width_cal=0.979; rf_live 3.65% CBUAE base rate (AED peg -> Fed path). Horizon resolved by horizons.resolve() on AE's own realized calendar, not a session count.",
    p5:5.95, p25:6.97, p50:7.69, p75:8.48, p95:9.95,
    touch:{ "+5":70, "+10":50, "+15":33, "+20":22, "-5":65, "-10":41 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"ALINMA", asset_class:"equity",
    anchor_date:"2026-07-26", anchor_price:23.8, ccy:"SAR",
    horizon_label:"1 month", grade_date:"2026-08-26", grade_basis:"projected", horizon_days:22,
    cycle_no:2, reanchor_from:"2026-07-07", anchor_vol:0.1725,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). SA live fit nu=12.0, width_cal=1.07; rf_live 4.25% SAMA repo-anchored estimate. Horizon resolved by horizons.resolve() on SA's own realized calendar, not a session count.",
    p5:21.87, p25:23.08, p50:23.87, p75:24.71, p95:26.09,
    touch:{ "+5":31, "+10":7, "+15":1, "+20":0, "-5":25, "-10":4 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"ALINMA", asset_class:"equity",
    anchor_date:"2026-07-26", anchor_price:23.8, ccy:"SAR",
    horizon_label:"3 months", grade_date:"2026-10-26", grade_basis:"projected", horizon_days:62,
    cycle_no:2, reanchor_from:"2026-07-07", anchor_vol:0.1951,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). SA live fit nu=12.0, width_cal=1.07; rf_live 4.25% SAMA repo-anchored estimate. Horizon resolved by horizons.resolve() on SA's own realized calendar, not a session count.",
    p5:20.33, p25:22.53, p50:24.05, p75:25.67, p95:28.45,
    touch:{ "+5":60, "+10":33, "+15":16, "+20":8, "-5":51, "-10":23 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"ALPHADHABI", asset_class:"equity",
    anchor_date:"2026-07-24", anchor_price:7.3, ccy:"AED",
    horizon_label:"1 month", grade_date:"2026-08-24", grade_basis:"projected", horizon_days:20,
    cycle_no:2, reanchor_from:"2026-07-03", anchor_vol:0.3188,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). AE live fit nu=10.0, width_cal=0.979; rf_live 3.65% CBUAE base rate (AED peg -> Fed path). Horizon resolved by horizons.resolve() on AE's own realized calendar, not a session count.",
    p5:6.35, p25:6.93, p50:7.32, p75:7.73, p95:8.42,
    touch:{ "+5":48, "+10":22, "+15":9, "+20":3, "-5":44, "-10":16 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"ALPHADHABI", asset_class:"equity",
    anchor_date:"2026-07-24", anchor_price:7.3, ccy:"AED",
    horizon_label:"3 months", grade_date:"2026-10-26", grade_basis:"projected", horizon_days:63,
    cycle_no:2, reanchor_from:"2026-07-03", anchor_vol:0.3289,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). AE live fit nu=10.0, width_cal=0.979; rf_live 3.65% CBUAE base rate (AED peg -> Fed path). Horizon resolved by horizons.resolve() on AE's own realized calendar, not a session count.",
    p5:5.69, p25:6.67, p50:7.37, p75:8.14, p95:9.57,
    touch:{ "+5":70, "+10":50, "+15":34, "+20":22, "-5":66, "-10":41 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"ALRAJHI", asset_class:"equity",
    anchor_date:"2026-07-26", anchor_price:64.5, ccy:"SAR",
    horizon_label:"1 month", grade_date:"2026-08-26", grade_basis:"projected", horizon_days:22,
    cycle_no:2, reanchor_from:"2026-07-02", anchor_vol:0.1956,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). SA live fit nu=12.0, width_cal=1.07; rf_live 4.25% SAMA repo-anchored estimate. Horizon resolved by horizons.resolve() on SA's own realized calendar, not a session count.",
    p5:58.58, p25:62.26, p50:64.7, p75:67.27, p95:71.54,
    touch:{ "+5":36, "+10":10, "+15":2, "+20":1, "-5":30, "-10":6 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"ALRAJHI", asset_class:"equity",
    anchor_date:"2026-07-26", anchor_price:64.5, ccy:"SAR",
    horizon_label:"3 months", grade_date:"2026-10-26", grade_basis:"projected", horizon_days:62,
    cycle_no:2, reanchor_from:"2026-07-02", anchor_vol:0.2098,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). SA live fit nu=12.0, width_cal=1.07; rf_live 4.25% SAMA repo-anchored estimate. Horizon resolved by horizons.resolve() on SA's own realized calendar, not a session count.",
    p5:54.4, p25:60.76, p50:65.19, p75:69.91, p95:78.09,
    touch:{ "+5":62, "+10":36, "+15":19, "+20":10, "-5":54, "-10":26 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"ARAMCO", asset_class:"equity",
    anchor_date:"2026-07-26", anchor_price:26.6, ccy:"SAR",
    horizon_label:"1 month", grade_date:"2026-08-26", grade_basis:"projected", horizon_days:22,
    cycle_no:2, reanchor_from:"2026-07-01", anchor_vol:0.1536,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). SA live fit nu=12.0, width_cal=1.07; rf_live 4.25% SAMA repo-anchored estimate. Horizon resolved by horizons.resolve() on SA's own realized calendar, not a session count.",
    p5:24.68, p25:25.89, p50:26.68, p75:27.51, p95:28.87,
    touch:{ "+5":26, "+10":5, "+15":1, "+20":0, "-5":20, "-10":2 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"ARAMCO", asset_class:"equity",
    anchor_date:"2026-07-26", anchor_price:26.6, ccy:"SAR",
    horizon_label:"3 months", grade_date:"2026-10-26", grade_basis:"projected", horizon_days:62,
    cycle_no:2, reanchor_from:"2026-07-01", anchor_vol:0.1548,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). SA live fit nu=12.0, width_cal=1.07; rf_live 4.25% SAMA repo-anchored estimate. Horizon resolved by horizons.resolve() on SA's own realized calendar, not a session count.",
    p5:23.52, p25:25.52, p50:26.88, p75:28.3, p95:30.71,
    touch:{ "+5":53, "+10":23, "+15":9, "+20":3, "-5":42, "-10":14 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"BTFH", asset_class:"equity",
    anchor_date:"2026-07-22", anchor_price:3.09, ccy:"EGP",
    horizon_label:"1 month", grade_date:"2026-08-23", grade_basis:"projected", horizon_days:20,
    cycle_no:2, reanchor_from:"2026-07-01", anchor_vol:0.3519,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). EG live fit nu=6.0, width_cal=0.951; rf_live 19.50% CBE main operation rate. Horizon resolved by horizons.resolve() on EG's own realized calendar, not a session count.",
    p5:2.7, p25:2.97, p50:3.14, p75:3.31, p95:3.64,
    touch:{ "+5":53, "+10":26, "+15":12, "+20":5, "-5":39, "-10":15 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"BTFH", asset_class:"equity",
    anchor_date:"2026-07-22", anchor_price:3.09, ccy:"EGP",
    horizon_label:"3 months", grade_date:"2026-10-22", grade_basis:"projected", horizon_days:61,
    cycle_no:2, reanchor_from:"2026-07-01", anchor_vol:0.3828,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). EG live fit nu=6.0, width_cal=0.951; rf_live 19.50% CBE main operation rate. Horizon resolved by horizons.resolve() on EG's own realized calendar, not a session count.",
    p5:2.43, p25:2.91, p50:3.24, p75:3.59, p95:4.29,
    touch:{ "+5":77, "+10":59, "+15":43, "+20":31, "-5":60, "-10":36 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"BURJEEL", asset_class:"equity",
    anchor_date:"2026-07-24", anchor_price:1.2, ccy:"AED",
    horizon_label:"1 month", grade_date:"2026-08-24", grade_basis:"projected", horizon_days:20,
    cycle_no:2, reanchor_from:"2026-07-10", anchor_vol:0.3584,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). AE live fit nu=10.0, width_cal=0.979; rf_live 3.65% CBUAE base rate (AED peg -> Fed path). Horizon resolved by horizons.resolve() on AE's own realized calendar, not a session count.",
    p5:1.03, p25:1.13, p50:1.2, p75:1.28, p95:1.41,
    touch:{ "+5":52, "+10":26, "+15":12, "+20":5, "-5":48, "-10":20 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"BURJEEL", asset_class:"equity",
    anchor_date:"2026-07-24", anchor_price:1.2, ccy:"AED",
    horizon_label:"3 months", grade_date:"2026-10-26", grade_basis:"projected", horizon_days:63,
    cycle_no:2, reanchor_from:"2026-07-10", anchor_vol:0.3558,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). AE live fit nu=10.0, width_cal=0.979; rf_live 3.65% CBUAE base rate (AED peg -> Fed path). Horizon resolved by horizons.resolve() on AE's own realized calendar, not a session count.",
    p5:0.91, p25:1.09, p50:1.21, p75:1.35, p95:1.61,
    touch:{ "+5":72, "+10":53, "+15":37, "+20":25, "-5":68, "-10":45 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"CCAP", asset_class:"equity",
    anchor_date:"2026-07-22", anchor_price:5.51, ccy:"EGP",
    horizon_label:"1 month", grade_date:"2026-08-23", grade_basis:"projected", horizon_days:20,
    cycle_no:2, reanchor_from:"2026-06-30", anchor_vol:0.4872,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). EG live fit nu=6.0, width_cal=0.951; rf_live 19.50% CBE main operation rate. Horizon resolved by horizons.resolve() on EG's own realized calendar, not a session count.",
    p5:4.56, p25:5.18, p50:5.59, p75:6.04, p95:6.87,
    touch:{ "+5":62, "+10":38, "+15":22, "+20":13, "-5":52, "-10":27 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"CCAP", asset_class:"equity",
    anchor_date:"2026-07-22", anchor_price:5.51, ccy:"EGP",
    horizon_label:"3 months", grade_date:"2026-10-22", grade_basis:"projected", horizon_days:61,
    cycle_no:2, reanchor_from:"2026-06-30", anchor_vol:0.4979,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). EG live fit nu=6.0, width_cal=0.951; rf_live 19.50% CBE main operation rate. Horizon resolved by horizons.resolve() on EG's own realized calendar, not a session count.",
    p5:3.99, p25:5.03, p50:5.77, p75:6.6, p95:8.33,
    touch:{ "+5":80, "+10":66, "+15":52, "+20":41, "-5":68, "-10":48 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"CLHO", asset_class:"equity",
    anchor_date:"2026-07-22", anchor_price:16.9, ccy:"EGP",
    horizon_label:"1 month", grade_date:"2026-08-23", grade_basis:"projected", horizon_days:20,
    cycle_no:2, reanchor_from:"2026-07-12", anchor_vol:0.5259,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). EG live fit nu=6.0, width_cal=0.951; rf_live 19.50% CBE main operation rate. Horizon resolved by horizons.resolve() on EG's own realized calendar, not a session count.",
    p5:13.75, p25:15.8, p50:17.15, p75:18.63, p95:21.41,
    touch:{ "+5":63, "+10":41, "+15":25, "+20":15, "-5":54, "-10":30 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"CLHO", asset_class:"equity",
    anchor_date:"2026-07-22", anchor_price:16.9, ccy:"EGP",
    horizon_label:"3 months", grade_date:"2026-10-22", grade_basis:"projected", horizon_days:61,
    cycle_no:2, reanchor_from:"2026-07-12", anchor_vol:0.5317,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). EG live fit nu=6.0, width_cal=0.951; rf_live 19.50% CBE main operation rate. Horizon resolved by horizons.resolve() on EG's own realized calendar, not a session count.",
    p5:11.93, p25:15.3, p50:17.7, p75:20.43, p95:26.18,
    touch:{ "+5":81, "+10":67, "+15":54, "+20":43, "-5":70, "-10":50 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"DEWA", asset_class:"equity",
    anchor_date:"2026-07-24", anchor_price:2.67, ccy:"AED",
    horizon_label:"1 month", grade_date:"2026-08-24", grade_basis:"projected", horizon_days:20,
    cycle_no:2, reanchor_from:"2026-07-10", anchor_vol:0.2332,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). AE live fit nu=10.0, width_cal=0.979; rf_live 3.65% CBUAE base rate (AED peg -> Fed path). Horizon resolved by horizons.resolve() on AE's own realized calendar, not a session count.",
    p5:2.41, p25:2.57, p50:2.68, p75:2.79, p95:2.97,
    touch:{ "+5":36, "+10":11, "+15":3, "+20":1, "-5":31, "-10":7 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"DEWA", asset_class:"equity",
    anchor_date:"2026-07-24", anchor_price:2.67, ccy:"AED",
    horizon_label:"3 months", grade_date:"2026-10-26", grade_basis:"projected", horizon_days:63,
    cycle_no:2, reanchor_from:"2026-07-10", anchor_vol:0.2357,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). AE live fit nu=10.0, width_cal=0.979; rf_live 3.65% CBUAE base rate (AED peg -> Fed path). Horizon resolved by horizons.resolve() on AE's own realized calendar, not a session count.",
    p5:2.24, p25:2.51, p50:2.7, p75:2.89, p95:3.25,
    touch:{ "+5":62, "+10":37, "+15":20, "+20":11, "-5":55, "-10":27 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"DIB", asset_class:"equity",
    anchor_date:"2026-07-24", anchor_price:7.35, ccy:"AED",
    horizon_label:"1 month", grade_date:"2026-08-24", grade_basis:"projected", horizon_days:20,
    cycle_no:2, reanchor_from:"2026-07-03", anchor_vol:0.2307,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). AE live fit nu=10.0, width_cal=0.979; rf_live 3.65% CBUAE base rate (AED peg -> Fed path). Horizon resolved by horizons.resolve() on AE's own realized calendar, not a session count.",
    p5:6.65, p25:7.09, p50:7.37, p75:7.67, p95:8.16,
    touch:{ "+5":36, "+10":10, "+15":3, "+20":1, "-5":31, "-10":7 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"DIB", asset_class:"equity",
    anchor_date:"2026-07-24", anchor_price:7.35, ccy:"AED",
    horizon_label:"3 months", grade_date:"2026-10-26", grade_basis:"projected", horizon_days:63,
    cycle_no:2, reanchor_from:"2026-07-03", anchor_vol:0.241,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). AE live fit nu=10.0, width_cal=0.979; rf_live 3.65% CBUAE base rate (AED peg -> Fed path). Horizon resolved by horizons.resolve() on AE's own realized calendar, not a session count.",
    p5:6.13, p25:6.9, p50:7.42, p75:7.98, p95:8.99,
    touch:{ "+5":63, "+10":38, "+15":21, "+20":11, "-5":56, "-10":28 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"DSCW", asset_class:"equity",
    anchor_date:"2026-07-22", anchor_price:1.96, ccy:"EGP",
    horizon_label:"1 month", grade_date:"2026-08-23", grade_basis:"projected", horizon_days:20,
    cycle_no:2, reanchor_from:"2026-07-19", anchor_vol:0.3789,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). EG live fit nu=6.0, width_cal=0.951; rf_live 19.50% CBE main operation rate. Horizon resolved by horizons.resolve() on EG's own realized calendar, not a session count.",
    p5:1.7, p25:1.88, p50:1.99, p75:2.11, p95:2.33,
    touch:{ "+5":55, "+10":29, "+15":14, "+20":7, "-5":42, "-10":17 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"DSCW", asset_class:"equity",
    anchor_date:"2026-07-22", anchor_price:1.96, ccy:"EGP",
    horizon_label:"3 months", grade_date:"2026-10-22", grade_basis:"projected", horizon_days:61,
    cycle_no:2, reanchor_from:"2026-07-19", anchor_vol:0.4182,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). EG live fit nu=6.0, width_cal=0.951; rf_live 19.50% CBE main operation rate. Horizon resolved by horizons.resolve() on EG's own realized calendar, not a session count.",
    p5:1.5, p25:1.83, p50:2.05, p75:2.3, p95:2.79,
    touch:{ "+5":78, "+10":61, "+15":46, "+20":34, "-5":63, "-10":40 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"EAND", asset_class:"equity",
    anchor_date:"2026-07-24", anchor_price:20.08, ccy:"AED",
    horizon_label:"1 month", grade_date:"2026-08-24", grade_basis:"projected", horizon_days:20,
    cycle_no:2, reanchor_from:"2026-07-09", anchor_vol:0.2271,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). AE live fit nu=10.0, width_cal=0.979; rf_live 3.65% CBUAE base rate (AED peg -> Fed path). Horizon resolved by horizons.resolve() on AE's own realized calendar, not a session count.",
    p5:18.2, p25:19.37, p50:20.14, p75:20.94, p95:22.25,
    touch:{ "+5":35, "+10":10, "+15":3, "+20":1, "-5":30, "-10":6 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"EAND", asset_class:"equity",
    anchor_date:"2026-07-24", anchor_price:20.08, ccy:"AED",
    horizon_label:"3 months", grade_date:"2026-10-26", grade_basis:"projected", horizon_days:63,
    cycle_no:2, reanchor_from:"2026-07-09", anchor_vol:0.2242,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). AE live fit nu=10.0, width_cal=0.979; rf_live 3.65% CBUAE base rate (AED peg -> Fed path). Horizon resolved by horizons.resolve() on AE's own realized calendar, not a session count.",
    p5:16.98, p25:18.94, p50:20.27, p75:21.7, p95:24.23,
    touch:{ "+5":61, "+10":35, "+15":18, "+20":9, "-5":53, "-10":25 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"EFID", asset_class:"equity",
    anchor_date:"2026-07-22", anchor_price:27.7, ccy:"EGP",
    horizon_label:"1 month", grade_date:"2026-08-23", grade_basis:"projected", horizon_days:20,
    cycle_no:2, reanchor_from:"2026-07-01", anchor_vol:0.4039,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). EG live fit nu=6.0, width_cal=0.951; rf_live 19.50% CBE main operation rate. Horizon resolved by horizons.resolve() on EG's own realized calendar, not a session count.",
    p5:23.72, p25:26.4, p50:28.11, p75:29.95, p95:33.33,
    touch:{ "+5":57, "+10":31, "+15":16, "+20":8, "-5":45, "-10":19 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"EFID", asset_class:"equity",
    anchor_date:"2026-07-22", anchor_price:27.7, ccy:"EGP",
    horizon_label:"3 months", grade_date:"2026-10-22", grade_basis:"projected", horizon_days:61,
    cycle_no:2, reanchor_from:"2026-07-01", anchor_vol:0.4474,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). EG live fit nu=6.0, width_cal=0.951; rf_live 19.50% CBE main operation rate. Horizon resolved by horizons.resolve() on EG's own realized calendar, not a session count.",
    p5:20.81, p25:25.66, p50:29.01, p75:32.72, p95:40.32,
    touch:{ "+5":79, "+10":63, "+15":49, "+20":37, "-5":65, "-10":43 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"EFIH", asset_class:"equity",
    anchor_date:"2026-07-22", anchor_price:23.39, ccy:"EGP",
    horizon_label:"1 month", grade_date:"2026-08-23", grade_basis:"projected", horizon_days:20,
    cycle_no:2, reanchor_from:"2026-07-01", anchor_vol:0.4001,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). EG live fit nu=6.0, width_cal=0.951; rf_live 19.50% CBE main operation rate. Horizon resolved by horizons.resolve() on EG's own realized calendar, not a session count.",
    p5:20.06, p25:22.3, p50:23.74, p75:25.28, p95:28.1,
    touch:{ "+5":57, "+10":31, "+15":16, "+20":8, "-5":44, "-10":19 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"EFIH", asset_class:"equity",
    anchor_date:"2026-07-22", anchor_price:23.39, ccy:"EGP",
    horizon_label:"3 months", grade_date:"2026-10-22", grade_basis:"projected", horizon_days:61,
    cycle_no:2, reanchor_from:"2026-07-01", anchor_vol:0.4283,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). EG live fit nu=6.0, width_cal=0.951; rf_live 19.50% CBE main operation rate. Horizon resolved by horizons.resolve() on EG's own realized calendar, not a session count.",
    p5:17.82, p25:21.78, p50:24.49, p75:27.49, p95:33.57,
    touch:{ "+5":79, "+10":62, "+15":47, "+20":35, "-5":63, "-10":41 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"EGAL", asset_class:"equity",
    anchor_date:"2026-07-22", anchor_price:301.12, ccy:"EGP",
    horizon_label:"1 month", grade_date:"2026-08-23", grade_basis:"projected", horizon_days:20,
    cycle_no:2, reanchor_from:"2026-07-01", anchor_vol:0.3557,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). EG live fit nu=6.0, width_cal=0.951; rf_live 19.50% CBE main operation rate. Horizon resolved by horizons.resolve() on EG's own realized calendar, not a session count.",
    p5:263.16, p25:289.12, p50:305.61, p75:323.17, p95:355.02,
    touch:{ "+5":53, "+10":26, "+15":12, "+20":5, "-5":40, "-10":15 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"EGAL", asset_class:"equity",
    anchor_date:"2026-07-22", anchor_price:301.12, ccy:"EGP",
    horizon_label:"3 months", grade_date:"2026-10-22", grade_basis:"projected", horizon_days:61,
    cycle_no:2, reanchor_from:"2026-07-01", anchor_vol:0.4203,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). EG live fit nu=6.0, width_cal=0.951; rf_live 19.50% CBE main operation rate. Horizon resolved by horizons.resolve() on EG's own realized calendar, not a session count.",
    p5:230.79, p25:280.98, p50:315.3, p75:353.1, p95:429.59,
    touch:{ "+5":78, "+10":62, "+15":46, "+20":34, "-5":63, "-10":40 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"ELM", asset_class:"equity",
    anchor_date:"2026-07-26", anchor_price:666.0, ccy:"SAR",
    horizon_label:"1 month", grade_date:"2026-08-26", grade_basis:"projected", horizon_days:22,
    cycle_no:2, reanchor_from:"2026-07-07", anchor_vol:0.3555,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). SA live fit nu=12.0, width_cal=1.07; rf_live 4.25% SAMA repo-anchored estimate. Horizon resolved by horizons.resolve() on SA's own realized calendar, not a session count.",
    p5:557.58, p25:622.9, p50:667.9, p75:716.95, p95:801.78,
    touch:{ "+5":57, "+10":32, "+15":17, "+20":8, "-5":53, "-10":26 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"ELM", asset_class:"equity",
    anchor_date:"2026-07-26", anchor_price:666.0, ccy:"SAR",
    horizon_label:"3 months", grade_date:"2026-10-26", grade_basis:"projected", horizon_days:62,
    cycle_no:2, reanchor_from:"2026-07-07", anchor_vol:0.3436,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). SA live fit nu=12.0, width_cal=1.07; rf_live 4.25% SAMA repo-anchored estimate. Horizon resolved by horizons.resolve() on SA's own realized calendar, not a session count.",
    p5:500.81, p25:600.12, p50:673.56, p75:755.15, p95:905.12,
    touch:{ "+5":74, "+10":55, "+15":40, "+20":28, "-5":69, "-10":47 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"EMAAR", asset_class:"equity",
    anchor_date:"2026-07-24", anchor_price:11.08, ccy:"AED",
    horizon_label:"1 month", grade_date:"2026-08-24", grade_basis:"projected", horizon_days:20,
    cycle_no:2, reanchor_from:"2026-06-29", anchor_vol:0.2784,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). AE live fit nu=10.0, width_cal=0.979; rf_live 3.65% CBUAE base rate (AED peg -> Fed path). Horizon resolved by horizons.resolve() on AE's own realized calendar, not a session count.",
    p5:9.82, p25:10.6, p50:11.11, p75:11.66, p95:12.56,
    touch:{ "+5":43, "+10":16, "+15":6, "+20":2, "-5":39, "-10":12 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"EMAAR", asset_class:"equity",
    anchor_date:"2026-07-24", anchor_price:11.08, ccy:"AED",
    horizon_label:"3 months", grade_date:"2026-10-26", grade_basis:"projected", horizon_days:63,
    cycle_no:2, reanchor_from:"2026-06-29", anchor_vol:0.2973,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). AE live fit nu=10.0, width_cal=0.979; rf_live 3.65% CBUAE base rate (AED peg -> Fed path). Horizon resolved by horizons.resolve() on AE's own realized calendar, not a session count.",
    p5:8.85, p25:10.22, p50:11.19, p75:12.24, p95:14.17,
    touch:{ "+5":68, "+10":46, "+15":29, "+20":18, "-5":63, "-10":37 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"EMAARDEV", asset_class:"equity",
    anchor_date:"2026-07-24", anchor_price:13.16, ccy:"AED",
    horizon_label:"1 month", grade_date:"2026-08-24", grade_basis:"projected", horizon_days:20,
    cycle_no:2, reanchor_from:"2026-07-03", anchor_vol:0.316,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). AE live fit nu=10.0, width_cal=0.979; rf_live 3.65% CBUAE base rate (AED peg -> Fed path). Horizon resolved by horizons.resolve() on AE's own realized calendar, not a session count.",
    p5:11.46, p25:12.5, p50:13.2, p75:13.94, p95:15.16,
    touch:{ "+5":48, "+10":21, "+15":8, "+20":3, "-5":43, "-10":16 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"EMAARDEV", asset_class:"equity",
    anchor_date:"2026-07-24", anchor_price:13.16, ccy:"AED",
    horizon_label:"3 months", grade_date:"2026-10-26", grade_basis:"projected", horizon_days:63,
    cycle_no:2, reanchor_from:"2026-07-03", anchor_vol:0.3395,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). AE live fit nu=10.0, width_cal=0.979; rf_live 3.65% CBUAE base rate (AED peg -> Fed path). Horizon resolved by horizons.resolve() on AE's own realized calendar, not a session count.",
    p5:10.16, p25:11.99, p50:13.29, p75:14.73, p95:17.41,
    touch:{ "+5":71, "+10":51, "+15":35, "+20":23, "-5":66, "-10":43 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"ENBD", asset_class:"equity",
    anchor_date:"2026-07-24", anchor_price:30.22, ccy:"AED",
    horizon_label:"1 month", grade_date:"2026-08-24", grade_basis:"projected", horizon_days:20,
    cycle_no:2, reanchor_from:"2026-07-03", anchor_vol:0.3498,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). AE live fit nu=10.0, width_cal=0.979; rf_live 3.65% CBUAE base rate (AED peg -> Fed path). Horizon resolved by horizons.resolve() on AE's own realized calendar, not a session count.",
    p5:25.93, p25:28.55, p50:30.31, p75:32.19, p95:35.34,
    touch:{ "+5":51, "+10":25, "+15":11, "+20":5, "-5":47, "-10":20 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"ENBD", asset_class:"equity",
    anchor_date:"2026-07-24", anchor_price:30.22, ccy:"AED",
    horizon_label:"3 months", grade_date:"2026-10-26", grade_basis:"projected", horizon_days:63,
    cycle_no:2, reanchor_from:"2026-07-03", anchor_vol:0.3542,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). AE live fit nu=10.0, width_cal=0.979; rf_live 3.65% CBUAE base rate (AED peg -> Fed path). Horizon resolved by horizons.resolve() on AE's own realized calendar, not a session count.",
    p5:23.07, p25:27.41, p50:30.52, p75:33.97, p95:40.44,
    touch:{ "+5":72, "+10":53, "+15":37, "+20":25, "-5":68, "-10":45 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"ETEL", asset_class:"equity",
    anchor_date:"2026-07-22", anchor_price:103.28, ccy:"EGP",
    horizon_label:"1 month", grade_date:"2026-08-23", grade_basis:"projected", horizon_days:20,
    cycle_no:2, reanchor_from:"2026-07-01", anchor_vol:0.4019,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). EG live fit nu=6.0, width_cal=0.951; rf_live 19.50% CBE main operation rate. Horizon resolved by horizons.resolve() on EG's own realized calendar, not a session count.",
    p5:88.52, p25:98.45, p50:104.82, p75:111.65, p95:124.16,
    touch:{ "+5":57, "+10":31, "+15":16, "+20":8, "-5":45, "-10":19 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"ETEL", asset_class:"equity",
    anchor_date:"2026-07-22", anchor_price:103.28, ccy:"EGP",
    horizon_label:"3 months", grade_date:"2026-10-22", grade_basis:"projected", horizon_days:61,
    cycle_no:2, reanchor_from:"2026-07-01", anchor_vol:0.404,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). EG live fit nu=6.0, width_cal=0.951; rf_live 19.50% CBE main operation rate. Horizon resolved by horizons.resolve() on EG's own realized calendar, not a session count.",
    p5:80.11, p25:96.8, p50:108.14, p75:120.57, p95:145.58,
    touch:{ "+5":78, "+10":61, "+15":45, "+20":33, "-5":61, "-10":38 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"EXTRA", asset_class:"equity",
    anchor_date:"2026-07-26", anchor_price:68.5, ccy:"SAR",
    horizon_label:"1 month", grade_date:"2026-08-26", grade_basis:"projected", horizon_days:22,
    cycle_no:2, reanchor_from:"2026-07-09", anchor_vol:0.2101,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). SA live fit nu=12.0, width_cal=1.07; rf_live 4.25% SAMA repo-anchored estimate. Horizon resolved by horizons.resolve() on SA's own realized calendar, not a session count.",
    p5:61.75, p25:65.93, p50:68.71, p75:71.65, p95:76.54,
    touch:{ "+5":39, "+10":12, "+15":3, "+20":1, "-5":33, "-10":8 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"EXTRA", asset_class:"equity",
    anchor_date:"2026-07-26", anchor_price:68.5, ccy:"SAR",
    horizon_label:"3 months", grade_date:"2026-10-26", grade_basis:"projected", horizon_days:62,
    cycle_no:2, reanchor_from:"2026-07-09", anchor_vol:0.2402,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). SA live fit nu=12.0, width_cal=1.07; rf_live 4.25% SAMA repo-anchored estimate. Horizon resolved by horizons.resolve() on SA's own realized calendar, not a session count.",
    p5:56.29, p25:63.88, p50:69.25, p75:75.01, p95:85.14,
    touch:{ "+5":66, "+10":42, "+15":24, "+20":14, "-5":59, "-10":32 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"FAB", asset_class:"equity",
    anchor_date:"2026-07-24", anchor_price:18.66, ccy:"AED",
    horizon_label:"1 month", grade_date:"2026-08-24", grade_basis:"projected", horizon_days:20,
    cycle_no:2, reanchor_from:"2026-07-03", anchor_vol:0.2846,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). AE live fit nu=10.0, width_cal=0.979; rf_live 3.65% CBUAE base rate (AED peg -> Fed path). Horizon resolved by horizons.resolve() on AE's own realized calendar, not a session count.",
    p5:16.48, p25:17.82, p50:18.71, p75:19.65, p95:21.2,
    touch:{ "+5":44, "+10":17, "+15":6, "+20":2, "-5":40, "-10":12 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"FAB", asset_class:"equity",
    anchor_date:"2026-07-24", anchor_price:18.66, ccy:"AED",
    horizon_label:"3 months", grade_date:"2026-10-26", grade_basis:"projected", horizon_days:63,
    cycle_no:2, reanchor_from:"2026-07-03", anchor_vol:0.2838,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). AE live fit nu=10.0, width_cal=0.979; rf_live 3.65% CBUAE base rate (AED peg -> Fed path). Horizon resolved by horizons.resolve() on AE's own realized calendar, not a session count.",
    p5:15.06, p25:17.29, p50:18.84, p75:20.53, p95:23.61,
    touch:{ "+5":67, "+10":44, "+15":28, "+20":17, "-5":61, "-10":35 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"FWRY", asset_class:"equity",
    anchor_date:"2026-07-22", anchor_price:19.3, ccy:"EGP",
    horizon_label:"1 month", grade_date:"2026-08-23", grade_basis:"projected", horizon_days:20,
    cycle_no:2, reanchor_from:"2026-07-01", anchor_vol:0.3432,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). EG live fit nu=6.0, width_cal=0.951; rf_live 19.50% CBE main operation rate. Horizon resolved by horizons.resolve() on EG's own realized calendar, not a session count.",
    p5:16.96, p25:18.57, p50:19.59, p75:20.67, p95:22.64,
    touch:{ "+5":52, "+10":25, "+15":11, "+20":5, "-5":38, "-10":14 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"FWRY", asset_class:"equity",
    anchor_date:"2026-07-22", anchor_price:19.3, ccy:"EGP",
    horizon_label:"3 months", grade_date:"2026-10-22", grade_basis:"projected", horizon_days:61,
    cycle_no:2, reanchor_from:"2026-07-01", anchor_vol:0.3928,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). EG live fit nu=6.0, width_cal=0.951; rf_live 19.50% CBE main operation rate. Horizon resolved by horizons.resolve() on EG's own realized calendar, not a session count.",
    p5:15.1, p25:18.14, p50:20.21, p75:22.46, p95:26.98,
    touch:{ "+5":78, "+10":60, "+15":44, "+20":32, "-5":60, "-10":37 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"GBCO", asset_class:"equity",
    anchor_date:"2026-07-22", anchor_price:31.31, ccy:"EGP",
    horizon_label:"1 month", grade_date:"2026-08-23", grade_basis:"projected", horizon_days:20,
    cycle_no:2, reanchor_from:"2026-07-07", anchor_vol:0.5186,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). EG live fit nu=6.0, width_cal=0.951; rf_live 19.50% CBE main operation rate. Horizon resolved by horizons.resolve() on EG's own realized calendar, not a session count.",
    p5:25.55, p25:29.31, p50:31.78, p75:34.47, p95:39.54,
    touch:{ "+5":63, "+10":40, "+15":25, "+20":15, "-5":54, "-10":29 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"GBCO", asset_class:"equity",
    anchor_date:"2026-07-22", anchor_price:31.31, ccy:"EGP",
    horizon_label:"3 months", grade_date:"2026-10-22", grade_basis:"projected", horizon_days:61,
    cycle_no:2, reanchor_from:"2026-07-07", anchor_vol:0.5327,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). EG live fit nu=6.0, width_cal=0.951; rf_live 19.50% CBE main operation rate. Horizon resolved by horizons.resolve() on EG's own realized calendar, not a session count.",
    p5:22.08, p25:28.34, p50:32.8, p75:37.86, p95:48.54,
    touch:{ "+5":81, "+10":67, "+15":54, "+20":43, "-5":70, "-10":50 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"HELI", asset_class:"equity",
    anchor_date:"2026-07-22", anchor_price:8.27, ccy:"EGP",
    horizon_label:"1 month", grade_date:"2026-08-23", grade_basis:"projected", horizon_days:20,
    cycle_no:2, reanchor_from:"2026-07-03", anchor_vol:0.3905,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). EG live fit nu=6.0, width_cal=0.951; rf_live 19.50% CBE main operation rate. Horizon resolved by horizons.resolve() on EG's own realized calendar, not a session count.",
    p5:7.12, p25:7.9, p50:8.39, p75:8.92, p95:9.89,
    touch:{ "+5":56, "+10":30, "+15":15, "+20":7, "-5":44, "-10":18 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"HELI", asset_class:"equity",
    anchor_date:"2026-07-22", anchor_price:8.27, ccy:"EGP",
    horizon_label:"3 months", grade_date:"2026-10-22", grade_basis:"projected", horizon_days:61,
    cycle_no:2, reanchor_from:"2026-07-03", anchor_vol:0.4131,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). EG live fit nu=6.0, width_cal=0.951; rf_live 19.50% CBE main operation rate. Horizon resolved by horizons.resolve() on EG's own realized calendar, not a session count.",
    p5:6.37, p25:7.73, p50:8.66, p75:9.68, p95:11.74,
    touch:{ "+5":78, "+10":61, "+15":46, "+20":34, "-5":62, "-10":39 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"HRHO", asset_class:"equity",
    anchor_date:"2026-07-22", anchor_price:26.95, ccy:"EGP",
    horizon_label:"1 month", grade_date:"2026-08-23", grade_basis:"projected", horizon_days:20,
    cycle_no:2, reanchor_from:"2026-07-01", anchor_vol:0.3097,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). EG live fit nu=6.0, width_cal=0.951; rf_live 19.50% CBE main operation rate. Horizon resolved by horizons.resolve() on EG's own realized calendar, not a session count.",
    p5:24.01, p25:26.06, p50:27.35, p75:28.72, p95:31.16,
    touch:{ "+5":49, "+10":21, "+15":9, "+20":3, "-5":34, "-10":11 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"HRHO", asset_class:"equity",
    anchor_date:"2026-07-22", anchor_price:26.95, ccy:"EGP",
    horizon_label:"3 months", grade_date:"2026-10-22", grade_basis:"projected", horizon_days:61,
    cycle_no:2, reanchor_from:"2026-07-01", anchor_vol:0.3214,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). EG live fit nu=6.0, width_cal=0.951; rf_live 19.50% CBE main operation rate. Horizon resolved by horizons.resolve() on EG's own realized calendar, not a session count.",
    p5:22.22, p25:25.83, p50:28.21, p75:30.76, p95:35.74,
    touch:{ "+5":75, "+10":54, "+15":37, "+20":24, "-5":53, "-10":28 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"IHC", asset_class:"equity",
    anchor_date:"2026-07-24", anchor_price:380.0, ccy:"AED",
    horizon_label:"1 month", grade_date:"2026-08-24", grade_basis:"projected", horizon_days:20,
    cycle_no:2, reanchor_from:"2026-07-03", anchor_vol:0.0962,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). AE live fit nu=10.0, width_cal=0.979; rf_live 3.65% CBUAE base rate (AED peg -> Fed path). Horizon resolved by horizons.resolve() on AE's own realized calendar, not a session count.",
    p5:365.12, p25:374.9, p50:381.13, p75:387.49, p95:397.56,
    touch:{ "+5":6, "+10":0, "+15":0, "+20":0, "-5":4, "-10":0 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"IHC", asset_class:"equity",
    anchor_date:"2026-07-24", anchor_price:380.0, ccy:"AED",
    horizon_label:"3 months", grade_date:"2026-10-26", grade_basis:"projected", horizon_days:63,
    cycle_no:2, reanchor_from:"2026-07-03", anchor_vol:0.1197,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). AE live fit nu=10.0, width_cal=0.979; rf_live 3.65% CBUAE base rate (AED peg -> Fed path). Horizon resolved by horizons.resolve() on AE's own realized calendar, not a session count.",
    p5:348.92, p25:369.87, p50:383.54, p75:397.68, p95:421.81,
    touch:{ "+5":39, "+10":11, "+15":3, "+20":1, "-5":27, "-10":5 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"ISPH", asset_class:"equity",
    anchor_date:"2026-07-22", anchor_price:11.73, ccy:"EGP",
    horizon_label:"1 month", grade_date:"2026-08-23", grade_basis:"projected", horizon_days:20,
    cycle_no:2, reanchor_from:"2026-07-07", anchor_vol:0.4122,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). EG live fit nu=6.0, width_cal=0.951; rf_live 19.50% CBE main operation rate. Horizon resolved by horizons.resolve() on EG's own realized calendar, not a session count.",
    p5:10.01, p25:11.16, p50:11.9, p75:12.7, p95:14.16,
    touch:{ "+5":57, "+10":32, "+15":16, "+20":9, "-5":46, "-10":20 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"ISPH", asset_class:"equity",
    anchor_date:"2026-07-22", anchor_price:11.73, ccy:"EGP",
    horizon_label:"3 months", grade_date:"2026-10-22", grade_basis:"projected", horizon_days:61,
    cycle_no:2, reanchor_from:"2026-07-07", anchor_vol:0.4348,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). EG live fit nu=6.0, width_cal=0.951; rf_live 19.50% CBE main operation rate. Horizon resolved by horizons.resolve() on EG's own realized calendar, not a session count.",
    p5:8.89, p25:10.9, p50:12.28, p75:13.81, p95:16.92,
    touch:{ "+5":79, "+10":62, "+15":48, "+20":36, "-5":64, "-10":42 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"JUFO", asset_class:"equity",
    anchor_date:"2026-07-22", anchor_price:28.9, ccy:"EGP",
    horizon_label:"1 month", grade_date:"2026-08-23", grade_basis:"projected", horizon_days:20,
    cycle_no:2, reanchor_from:"2026-07-01", anchor_vol:0.4108,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). EG live fit nu=6.0, width_cal=0.951; rf_live 19.50% CBE main operation rate. Horizon resolved by horizons.resolve() on EG's own realized calendar, not a session count.",
    p5:24.68, p25:27.51, p50:29.33, p75:31.29, p95:34.87,
    touch:{ "+5":57, "+10":32, "+15":16, "+20":8, "-5":45, "-10":20 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"JUFO", asset_class:"equity",
    anchor_date:"2026-07-22", anchor_price:28.9, ccy:"EGP",
    horizon_label:"3 months", grade_date:"2026-10-22", grade_basis:"projected", horizon_days:61,
    cycle_no:2, reanchor_from:"2026-07-01", anchor_vol:0.4343,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). EG live fit nu=6.0, width_cal=0.951; rf_live 19.50% CBE main operation rate. Horizon resolved by horizons.resolve() on EG's own realized calendar, not a session count.",
    p5:21.92, p25:26.87, p50:30.26, p75:34.02, p95:41.66,
    touch:{ "+5":79, "+10":62, "+15":47, "+20":36, "-5":64, "-10":42 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"KABO", asset_class:"equity",
    anchor_date:"2026-07-22", anchor_price:8.8, ccy:"EGP",
    horizon_label:"1 month", grade_date:"2026-08-23", grade_basis:"projected", horizon_days:20,
    cycle_no:2, reanchor_from:"2026-07-06", anchor_vol:0.4835,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). EG live fit nu=6.0, width_cal=0.951; rf_live 19.50% CBE main operation rate. Horizon resolved by horizons.resolve() on EG's own realized calendar, not a session count.",
    p5:7.29, p25:8.28, p50:8.93, p75:9.64, p95:10.95,
    touch:{ "+5":61, "+10":38, "+15":22, "+20":13, "-5":51, "-10":26 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"KABO", asset_class:"equity",
    anchor_date:"2026-07-22", anchor_price:8.8, ccy:"EGP",
    horizon_label:"3 months", grade_date:"2026-10-22", grade_basis:"projected", horizon_days:61,
    cycle_no:2, reanchor_from:"2026-07-06", anchor_vol:0.5148,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). EG live fit nu=6.0, width_cal=0.951; rf_live 19.50% CBE main operation rate. Horizon resolved by horizons.resolve() on EG's own realized calendar, not a session count.",
    p5:6.29, p25:8.0, p50:9.22, p75:10.59, p95:13.46,
    touch:{ "+5":81, "+10":66, "+15":53, "+20":42, "-5":69, "-10":49 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"LCSW", asset_class:"equity",
    anchor_date:"2026-07-21", anchor_price:33.83, ccy:"EGP",
    horizon_label:"1 month", grade_date:"2026-08-23", grade_basis:"projected", horizon_days:21,
    cycle_no:2, reanchor_from:"2026-07-06", anchor_vol:0.5834,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). EG live fit nu=6.0, width_cal=0.951; rf_live 19.50% CBE main operation rate. Horizon resolved by horizons.resolve() on EG's own realized calendar, not a session count.",
    p5:26.69, p25:31.26, p50:34.33, p75:37.74, p95:44.21,
    touch:{ "+5":66, "+10":45, "+15":30, "+20":20, "-5":59, "-10":35 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"LCSW", asset_class:"equity",
    anchor_date:"2026-07-21", anchor_price:33.83, ccy:"EGP",
    horizon_label:"3 months", grade_date:"2026-10-21", grade_basis:"projected", horizon_days:61,
    cycle_no:2, reanchor_from:"2026-07-06", anchor_vol:0.5827,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). EG live fit nu=6.0, width_cal=0.951; rf_live 19.50% CBE main operation rate. Horizon resolved by horizons.resolve() on EG's own realized calendar, not a session count.",
    p5:23.0, p25:30.21, p50:35.44, p75:41.47, p95:54.42,
    touch:{ "+5":82, "+10":69, "+15":57, "+20":46, "-5":72, "-10":54 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"LULU", asset_class:"equity",
    anchor_date:"2026-07-24", anchor_price:0.96, ccy:"AED",
    horizon_label:"1 month", grade_date:"2026-08-24", grade_basis:"projected", horizon_days:20,
    cycle_no:2, reanchor_from:"2026-07-10", anchor_vol:0.3107,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). AE live fit nu=10.0, width_cal=0.979; rf_live 3.65% CBUAE base rate (AED peg -> Fed path). Horizon resolved by horizons.resolve() on AE's own realized calendar, not a session count.",
    p5:0.84, p25:0.91, p50:0.96, p75:1.02, p95:1.1,
    touch:{ "+5":47, "+10":20, "+15":8, "+20":3, "-5":43, "-10":15 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"LULU", asset_class:"equity",
    anchor_date:"2026-07-24", anchor_price:0.96, ccy:"AED",
    horizon_label:"3 months", grade_date:"2026-10-26", grade_basis:"projected", horizon_days:63,
    cycle_no:2, reanchor_from:"2026-07-10", anchor_vol:0.3272,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). AE live fit nu=10.0, width_cal=0.979; rf_live 3.65% CBUAE base rate (AED peg -> Fed path). Horizon resolved by horizons.resolve() on AE's own realized calendar, not a session count.",
    p5:0.75, p25:0.88, p50:0.97, p75:1.07, p95:1.26,
    touch:{ "+5":70, "+10":50, "+15":34, "+20":22, "-5":65, "-10":41 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"MAADEN", asset_class:"equity",
    anchor_date:"2026-07-26", anchor_price:58.2, ccy:"SAR",
    horizon_label:"1 month", grade_date:"2026-08-26", grade_basis:"projected", horizon_days:22,
    cycle_no:2, reanchor_from:"2026-07-05", anchor_vol:0.2754,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). SA live fit nu=12.0, width_cal=1.07; rf_live 4.25% SAMA repo-anchored estimate. Horizon resolved by horizons.resolve() on SA's own realized calendar, not a session count.",
    p5:50.75, p25:55.3, p50:58.37, p75:61.67, p95:67.25,
    touch:{ "+5":49, "+10":22, "+15":9, "+20":3, "-5":44, "-10":16 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"MAADEN", asset_class:"equity",
    anchor_date:"2026-07-26", anchor_price:58.2, ccy:"SAR",
    horizon_label:"3 months", grade_date:"2026-10-26", grade_basis:"projected", horizon_days:62,
    cycle_no:2, reanchor_from:"2026-07-05", anchor_vol:0.2889,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). SA live fit nu=12.0, width_cal=1.07; rf_live 4.25% SAMA repo-anchored estimate. Horizon resolved by horizons.resolve() on SA's own realized calendar, not a session count.",
    p5:45.87, p25:53.4, p50:58.85, p75:64.79, p95:75.44,
    touch:{ "+5":70, "+10":49, "+15":32, "+20":21, "-5":65, "-10":40 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"OCDI", asset_class:"equity",
    anchor_date:"2026-07-27", anchor_price:27.48, ccy:"EGP",
    horizon_label:"1 month", grade_date:"2026-08-27", grade_basis:"projected", horizon_days:21,
    cycle_no:3, reanchor_from:"2026-07-27", anchor_vol:0.4669,
    note:"Cycle 3 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). EG live fit nu=6.0, width_cal=0.951; rf_live 19.50% CBE main operation rate. Horizon resolved by horizons.resolve() on EG's own realized calendar, not a session count. RE-ISSUE AT AN UNCHANGED ANCHOR: this name was already re-struck at this same 2026-07-27 close (cycle 2), so reanchor_from equals this row's own anchor_date. Nothing was re-anchored — the cycle exists only because the cone itself changed: cycle 2 was struck on the retired session-counted 1-month/3-month convention under the then-live fit, and this row re-issues the same anchor on the calendar 1M/3M convention under the current fit. Cycle 2 keeps its published percentiles and grades exactly as issued.",
    p5:22.8, p25:25.87, p50:27.89, p75:30.08, p95:34.14,
    touch:{ "+5":61, "+10":38, "+15":22, "+20":12, "-5":52, "-10":26 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"OCDI", asset_class:"equity",
    anchor_date:"2026-07-27", anchor_price:27.48, ccy:"EGP",
    horizon_label:"3 months", grade_date:"2026-10-27", grade_basis:"projected", horizon_days:62,
    cycle_no:3, reanchor_from:"2026-07-27", anchor_vol:0.4796,
    note:"Cycle 3 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). EG live fit nu=6.0, width_cal=0.951; rf_live 19.50% CBE main operation rate. Horizon resolved by horizons.resolve() on EG's own realized calendar, not a session count. RE-ISSUE AT AN UNCHANGED ANCHOR: this name was already re-struck at this same 2026-07-27 close (cycle 2), so reanchor_from equals this row's own anchor_date. Nothing was re-anchored — the cycle exists only because the cone itself changed: cycle 2 was struck on the retired session-counted 1-month/3-month convention under the then-live fit, and this row re-issues the same anchor on the calendar 1M/3M convention under the current fit. Cycle 2 keeps its published percentiles and grades exactly as issued.",
    p5:20.11, p25:25.2, p50:28.78, p75:32.82, p95:41.15,
    touch:{ "+5":80, "+10":65, "+15":51, "+20":40, "-5":67, "-10":47 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"OIH", asset_class:"equity",
    anchor_date:"2026-07-22", anchor_price:1.47, ccy:"EGP",
    horizon_label:"1 month", grade_date:"2026-08-23", grade_basis:"projected", horizon_days:20,
    cycle_no:2, reanchor_from:"2026-07-01", anchor_vol:0.3619,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). EG live fit nu=6.0, width_cal=0.951; rf_live 19.50% CBE main operation rate. Horizon resolved by horizons.resolve() on EG's own realized calendar, not a session count.",
    p5:1.28, p25:1.41, p50:1.49, p75:1.58, p95:1.74,
    touch:{ "+5":54, "+10":27, "+15":13, "+20":6, "-5":40, "-10":16 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"OIH", asset_class:"equity",
    anchor_date:"2026-07-22", anchor_price:1.47, ccy:"EGP",
    horizon_label:"3 months", grade_date:"2026-10-22", grade_basis:"projected", horizon_days:61,
    cycle_no:2, reanchor_from:"2026-07-01", anchor_vol:0.3929,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). EG live fit nu=6.0, width_cal=0.951; rf_live 19.50% CBE main operation rate. Horizon resolved by horizons.resolve() on EG's own realized calendar, not a session count.",
    p5:1.15, p25:1.38, p50:1.54, p75:1.71, p95:2.06,
    touch:{ "+5":78, "+10":60, "+15":44, "+20":32, "-5":61, "-10":37 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"ORAS", asset_class:"equity",
    anchor_date:"2026-07-22", anchor_price:713.5, ccy:"EGP",
    horizon_label:"1 month", grade_date:"2026-08-23", grade_basis:"projected", horizon_days:20,
    cycle_no:2, reanchor_from:"2026-06-30", anchor_vol:0.3462,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). EG live fit nu=6.0, width_cal=0.951; rf_live 19.50% CBE main operation rate. Horizon resolved by horizons.resolve() on EG's own realized calendar, not a session count.",
    p5:626.04, p25:686.07, p50:724.14, p75:764.62, p95:837.88,
    touch:{ "+5":53, "+10":25, "+15":11, "+20":5, "-5":38, "-10":14 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"ORAS", asset_class:"equity",
    anchor_date:"2026-07-22", anchor_price:713.5, ccy:"EGP",
    horizon_label:"3 months", grade_date:"2026-10-22", grade_basis:"projected", horizon_days:61,
    cycle_no:2, reanchor_from:"2026-06-30", anchor_vol:0.3803,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). EG live fit nu=6.0, width_cal=0.951; rf_live 19.50% CBE main operation rate. Horizon resolved by horizons.resolve() on EG's own realized calendar, not a session count.",
    p5:563.24, p25:673.02, p50:746.99, p75:827.58, p95:988.28,
    touch:{ "+5":77, "+10":59, "+15":43, "+20":30, "-5":59, "-10":36 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"ORHD", asset_class:"equity",
    anchor_date:"2026-07-27", anchor_price:40.16, ccy:"EGP",
    horizon_label:"1 month", grade_date:"2026-08-27", grade_basis:"projected", horizon_days:21,
    cycle_no:3, reanchor_from:"2026-07-27", anchor_vol:0.3648,
    note:"Cycle 3 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). EG live fit nu=6.0, width_cal=0.951; rf_live 19.50% CBE main operation rate. Horizon resolved by horizons.resolve() on EG's own realized calendar, not a session count. RE-ISSUE AT AN UNCHANGED ANCHOR: this name was already re-struck at this same 2026-07-27 close (cycle 2), so reanchor_from equals this row's own anchor_date. Nothing was re-anchored — the cycle exists only because the cone itself changed: cycle 2 was struck on the retired session-counted 1-month/3-month convention under the then-live fit, and this row re-issues the same anchor on the calendar 1M/3M convention under the current fit. Cycle 2 keeps its published percentiles and grades exactly as issued.",
    p5:34.82, p25:38.44, p50:40.76, p75:43.24, p95:47.74,
    touch:{ "+5":55, "+10":28, "+15":14, "+20":6, "-5":42, "-10":17 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"ORHD", asset_class:"equity",
    anchor_date:"2026-07-27", anchor_price:40.16, ccy:"EGP",
    horizon_label:"3 months", grade_date:"2026-10-27", grade_basis:"projected", horizon_days:62,
    cycle_no:3, reanchor_from:"2026-07-27", anchor_vol:0.4038,
    note:"Cycle 3 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). EG live fit nu=6.0, width_cal=0.951; rf_live 19.50% CBE main operation rate. Horizon resolved by horizons.resolve() on EG's own realized calendar, not a session count. RE-ISSUE AT AN UNCHANGED ANCHOR: this name was already re-struck at this same 2026-07-27 close (cycle 2), so reanchor_from equals this row's own anchor_date. Nothing was re-anchored — the cycle exists only because the cone itself changed: cycle 2 was struck on the retired session-counted 1-month/3-month convention under the then-live fit, and this row re-issues the same anchor on the calendar 1M/3M convention under the current fit. Cycle 2 keeps its published percentiles and grades exactly as issued.",
    p5:31.1, p25:37.61, p50:42.05, p75:46.97, p95:56.82,
    touch:{ "+5":78, "+10":61, "+15":46, "+20":33, "-5":62, "-10":39 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"ORWE", asset_class:"equity",
    anchor_date:"2026-07-22", anchor_price:23.12, ccy:"EGP",
    horizon_label:"1 month", grade_date:"2026-08-23", grade_basis:"projected", horizon_days:20,
    cycle_no:2, reanchor_from:"2026-07-01", anchor_vol:0.2627,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). EG live fit nu=6.0, width_cal=0.951; rf_live 19.50% CBE main operation rate. Horizon resolved by horizons.resolve() on EG's own realized calendar, not a session count.",
    p5:21.01, p25:22.52, p50:23.46, p75:24.45, p95:26.21,
    touch:{ "+5":44, "+10":16, "+15":5, "+20":2, "-5":27, "-10":7 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"ORWE", asset_class:"equity",
    anchor_date:"2026-07-22", anchor_price:23.12, ccy:"EGP",
    horizon_label:"3 months", grade_date:"2026-10-22", grade_basis:"projected", horizon_days:61,
    cycle_no:2, reanchor_from:"2026-07-01", anchor_vol:0.2973,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). EG live fit nu=6.0, width_cal=0.951; rf_live 19.50% CBE main operation rate. Horizon resolved by horizons.resolve() on EG's own realized calendar, not a session count.",
    p5:19.41, p25:22.3, p50:24.2, p75:26.22, p95:30.12,
    touch:{ "+5":74, "+10":52, "+15":34, "+20":21, "-5":50, "-10":25 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"PHDC", asset_class:"equity",
    anchor_date:"2026-07-22", anchor_price:15.01, ccy:"EGP",
    horizon_label:"1 month", grade_date:"2026-08-23", grade_basis:"projected", horizon_days:20,
    cycle_no:4, reanchor_from:"2026-07-19", anchor_vol:0.3976,
    note:"Cycle 4 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). EG live fit nu=6.0, width_cal=0.951; rf_live 19.50% CBE main operation rate. Horizon resolved by horizons.resolve() on EG's own realized calendar, not a session count.",
    p5:12.89, p25:14.32, p50:15.23, p75:16.22, p95:18.01,
    touch:{ "+5":57, "+10":31, "+15":15, "+20":8, "-5":44, "-10":19 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"PHDC", asset_class:"equity",
    anchor_date:"2026-07-22", anchor_price:15.01, ccy:"EGP",
    horizon_label:"3 months", grade_date:"2026-10-22", grade_basis:"projected", horizon_days:61,
    cycle_no:4, reanchor_from:"2026-07-19", anchor_vol:0.4188,
    note:"Cycle 4 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). EG live fit nu=6.0, width_cal=0.951; rf_live 19.50% CBE main operation rate. Horizon resolved by horizons.resolve() on EG's own realized calendar, not a session count.",
    p5:11.52, p25:14.01, p50:15.72, p75:17.59, p95:21.39,
    touch:{ "+5":78, "+10":61, "+15":46, "+20":34, "-5":63, "-10":40 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"PRDC", asset_class:"equity",
    anchor_date:"2026-07-22", anchor_price:9.8, ccy:"EGP",
    horizon_label:"1 month", grade_date:"2026-08-23", grade_basis:"projected", horizon_days:20,
    cycle_no:2, reanchor_from:"2026-07-06", anchor_vol:0.5651,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). EG live fit nu=6.0, width_cal=0.951; rf_live 19.50% CBE main operation rate. Horizon resolved by horizons.resolve() on EG's own realized calendar, not a session count.",
    p5:7.84, p25:9.11, p50:9.95, p75:10.87, p95:12.62,
    touch:{ "+5":65, "+10":44, "+15":28, "+20":17, "-5":57, "-10":32 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"PRDC", asset_class:"equity",
    anchor_date:"2026-07-22", anchor_price:9.8, ccy:"EGP",
    horizon_label:"3 months", grade_date:"2026-10-22", grade_basis:"projected", horizon_days:61,
    cycle_no:2, reanchor_from:"2026-07-06", anchor_vol:0.5108,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). EG live fit nu=6.0, width_cal=0.951; rf_live 19.50% CBE main operation rate. Horizon resolved by horizons.resolve() on EG's own realized calendar, not a session count.",
    p5:7.02, p25:8.92, p50:10.26, p75:11.78, p95:14.95,
    touch:{ "+5":81, "+10":66, "+15":53, "+20":42, "-5":69, "-10":49 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"RAYA", asset_class:"equity",
    anchor_date:"2026-07-22", anchor_price:7.76, ccy:"EGP",
    horizon_label:"1 month", grade_date:"2026-08-23", grade_basis:"projected", horizon_days:20,
    cycle_no:2, reanchor_from:"2026-07-01", anchor_vol:0.4468,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). EG live fit nu=6.0, width_cal=0.951; rf_live 19.50% CBE main operation rate. Horizon resolved by horizons.resolve() on EG's own realized calendar, not a session count.",
    p5:6.53, p25:7.35, p50:7.88, p75:8.45, p95:9.51,
    touch:{ "+5":60, "+10":35, "+15":19, "+20":10, "-5":49, "-10":23 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"RAYA", asset_class:"equity",
    anchor_date:"2026-07-22", anchor_price:7.76, ccy:"EGP",
    horizon_label:"3 months", grade_date:"2026-10-22", grade_basis:"projected", horizon_days:61,
    cycle_no:2, reanchor_from:"2026-07-01", anchor_vol:0.4707,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). EG live fit nu=6.0, width_cal=0.951; rf_live 19.50% CBE main operation rate. Horizon resolved by horizons.resolve() on EG's own realized calendar, not a session count.",
    p5:5.73, p25:7.14, p50:8.13, p75:9.23, p95:11.49,
    touch:{ "+5":80, "+10":64, "+15":50, "+20":39, "-5":66, "-10":45 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"RIBL", asset_class:"equity",
    anchor_date:"2026-07-26", anchor_price:20.92, ccy:"SAR",
    horizon_label:"1 month", grade_date:"2026-08-26", grade_basis:"projected", horizon_days:22,
    cycle_no:2, reanchor_from:"2026-07-07", anchor_vol:0.1875,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). SA live fit nu=12.0, width_cal=1.07; rf_live 4.25% SAMA repo-anchored estimate. Horizon resolved by horizons.resolve() on SA's own realized calendar, not a session count.",
    p5:19.08, p25:20.23, p50:20.98, p75:21.78, p95:23.11,
    touch:{ "+5":34, "+10":9, "+15":2, "+20":0, "-5":29, "-10":5 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"RIBL", asset_class:"equity",
    anchor_date:"2026-07-26", anchor_price:20.92, ccy:"SAR",
    horizon_label:"3 months", grade_date:"2026-10-26", grade_basis:"projected", horizon_days:62,
    cycle_no:2, reanchor_from:"2026-07-07", anchor_vol:0.1968,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). SA live fit nu=12.0, width_cal=1.07; rf_live 4.25% SAMA repo-anchored estimate. Horizon resolved by horizons.resolve() on SA's own realized calendar, not a session count.",
    p5:17.84, p25:19.79, p50:21.14, p75:22.58, p95:25.04,
    touch:{ "+5":60, "+10":33, "+15":17, "+20":8, "-5":51, "-10":23 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"RMDA", asset_class:"equity",
    anchor_date:"2026-07-22", anchor_price:4.98, ccy:"EGP",
    horizon_label:"1 month", grade_date:"2026-08-23", grade_basis:"projected", horizon_days:20,
    cycle_no:2, reanchor_from:"2026-07-12", anchor_vol:0.3364,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). EG live fit nu=6.0, width_cal=0.951; rf_live 19.50% CBE main operation rate. Horizon resolved by horizons.resolve() on EG's own realized calendar, not a session count.",
    p5:4.39, p25:4.8, p50:5.05, p75:5.33, p95:5.82,
    touch:{ "+5":52, "+10":24, "+15":11, "+20":5, "-5":37, "-10":13 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"RMDA", asset_class:"equity",
    anchor_date:"2026-07-22", anchor_price:4.98, ccy:"EGP",
    horizon_label:"3 months", grade_date:"2026-10-22", grade_basis:"projected", horizon_days:61,
    cycle_no:2, reanchor_from:"2026-07-12", anchor_vol:0.3955,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). EG live fit nu=6.0, width_cal=0.951; rf_live 19.50% CBE main operation rate. Horizon resolved by horizons.resolve() on EG's own realized calendar, not a session count.",
    p5:3.89, p25:4.68, p50:5.21, p75:5.8, p95:6.98,
    touch:{ "+5":78, "+10":60, "+15":44, "+20":32, "-5":61, "-10":38 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"SABIC", asset_class:"equity",
    anchor_date:"2026-07-26", anchor_price:52.25, ccy:"SAR",
    horizon_label:"1 month", grade_date:"2026-08-26", grade_basis:"projected", horizon_days:22,
    cycle_no:2, reanchor_from:"2026-07-07", anchor_vol:0.1844,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). SA live fit nu=12.0, width_cal=1.07; rf_live 4.25% SAMA repo-anchored estimate. Horizon resolved by horizons.resolve() on SA's own realized calendar, not a session count.",
    p5:47.72, p25:50.55, p50:52.41, p75:54.37, p95:57.62,
    touch:{ "+5":34, "+10":8, "+15":2, "+20":0, "-5":28, "-10":5 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"SABIC", asset_class:"equity",
    anchor_date:"2026-07-26", anchor_price:52.25, ccy:"SAR",
    horizon_label:"3 months", grade_date:"2026-10-26", grade_basis:"projected", horizon_days:62,
    cycle_no:2, reanchor_from:"2026-07-07", anchor_vol:0.2001,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). SA live fit nu=12.0, width_cal=1.07; rf_live 4.25% SAMA repo-anchored estimate. Horizon resolved by horizons.resolve() on SA's own realized calendar, not a session count.",
    p5:44.44, p25:49.38, p50:52.81, p75:56.45, p95:62.73,
    touch:{ "+5":61, "+10":34, "+15":17, "+20":8, "-5":52, "-10":24 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"SALIK", asset_class:"equity",
    anchor_date:"2026-07-24", anchor_price:5.47, ccy:"AED",
    horizon_label:"1 month", grade_date:"2026-08-24", grade_basis:"projected", horizon_days:20,
    cycle_no:2, reanchor_from:"2026-07-10", anchor_vol:0.2878,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). AE live fit nu=10.0, width_cal=0.979; rf_live 3.65% CBUAE base rate (AED peg -> Fed path). Horizon resolved by horizons.resolve() on AE's own realized calendar, not a session count.",
    p5:4.83, p25:5.22, p50:5.49, p75:5.76, p95:6.22,
    touch:{ "+5":44, "+10":18, "+15":6, "+20":2, "-5":40, "-10":13 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"SALIK", asset_class:"equity",
    anchor_date:"2026-07-24", anchor_price:5.47, ccy:"AED",
    horizon_label:"3 months", grade_date:"2026-10-26", grade_basis:"projected", horizon_days:63,
    cycle_no:2, reanchor_from:"2026-07-10", anchor_vol:0.3043,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). AE live fit nu=10.0, width_cal=0.979; rf_live 3.65% CBUAE base rate (AED peg -> Fed path). Horizon resolved by horizons.resolve() on AE's own realized calendar, not a session count.",
    p5:4.34, p25:5.04, p50:5.52, p75:6.06, p95:7.03,
    touch:{ "+5":69, "+10":47, "+15":30, "+20":19, "-5":63, "-10":38 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"SNB", asset_class:"equity",
    anchor_date:"2026-07-26", anchor_price:39.92, ccy:"SAR",
    horizon_label:"1 month", grade_date:"2026-08-26", grade_basis:"projected", horizon_days:22,
    cycle_no:2, reanchor_from:"2026-07-02", anchor_vol:0.2468,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). SA live fit nu=12.0, width_cal=1.07; rf_live 4.25% SAMA repo-anchored estimate. Horizon resolved by horizons.resolve() on SA's own realized calendar, not a session count.",
    p5:35.32, p25:38.15, p50:40.04, p75:42.06, p95:45.45,
    touch:{ "+5":45, "+10":18, "+15":6, "+20":2, "-5":40, "-10":12 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"SNB", asset_class:"equity",
    anchor_date:"2026-07-26", anchor_price:39.92, ccy:"SAR",
    horizon_label:"3 months", grade_date:"2026-10-26", grade_basis:"projected", horizon_days:62,
    cycle_no:2, reanchor_from:"2026-07-02", anchor_vol:0.26,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). SA live fit nu=12.0, width_cal=1.07; rf_live 4.25% SAMA repo-anchored estimate. Horizon resolved by horizons.resolve() on SA's own realized calendar, not a session count.",
    p5:32.25, p25:36.98, p50:40.36, p75:44.01, p95:50.47,
    touch:{ "+5":68, "+10":45, "+15":28, "+20":17, "-5":61, "-10":35 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"STC", asset_class:"equity",
    anchor_date:"2026-07-26", anchor_price:43.1, ccy:"SAR",
    horizon_label:"1 month", grade_date:"2026-08-26", grade_basis:"projected", horizon_days:22,
    cycle_no:2, reanchor_from:"2026-07-07", anchor_vol:0.1353,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). SA live fit nu=12.0, width_cal=1.07; rf_live 4.25% SAMA repo-anchored estimate. Horizon resolved by horizons.resolve() on SA's own realized calendar, not a session count.",
    p5:40.36, p25:42.1, p50:43.23, p75:44.42, p95:46.35,
    touch:{ "+5":21, "+10":3, "+15":0, "+20":0, "-5":15, "-10":1 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"STC", asset_class:"equity",
    anchor_date:"2026-07-26", anchor_price:43.1, ccy:"SAR",
    horizon_label:"3 months", grade_date:"2026-10-26", grade_basis:"projected", horizon_days:62,
    cycle_no:2, reanchor_from:"2026-07-07", anchor_vol:0.1524,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). SA live fit nu=12.0, width_cal=1.07; rf_live 4.25% SAMA repo-anchored estimate. Horizon resolved by horizons.resolve() on SA's own realized calendar, not a session count.",
    p5:38.19, p25:41.38, p50:43.55, p75:45.82, p95:49.65,
    touch:{ "+5":52, "+10":23, "+15":9, "+20":3, "-5":41, "-10":13 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"TMGH", asset_class:"equity",
    anchor_date:"2026-07-22", anchor_price:100.5, ccy:"EGP",
    horizon_label:"1 month", grade_date:"2026-08-23", grade_basis:"projected", horizon_days:20,
    cycle_no:3, reanchor_from:"2026-07-19", anchor_vol:0.3441,
    note:"Cycle 3 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). EG live fit nu=6.0, width_cal=0.951; rf_live 19.50% CBE main operation rate. Horizon resolved by horizons.resolve() on EG's own realized calendar, not a session count.",
    p5:88.26, p25:96.67, p50:102.0, p75:107.67, p95:117.92,
    touch:{ "+5":52, "+10":25, "+15":11, "+20":5, "-5":38, "-10":14 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"TMGH", asset_class:"equity",
    anchor_date:"2026-07-22", anchor_price:100.5, ccy:"EGP",
    horizon_label:"3 months", grade_date:"2026-10-22", grade_basis:"projected", horizon_days:61,
    cycle_no:3, reanchor_from:"2026-07-19", anchor_vol:0.3579,
    note:"Cycle 3 roll-forward, 28-Jul-2026 — market-wide re-strike of EG/AE/SA onto the 15-year calibration libraries and the calendar horizon convention. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). EG live fit nu=6.0, width_cal=0.951; rf_live 19.50% CBE main operation rate. Horizon resolved by horizons.resolve() on EG's own realized calendar, not a session count.",
    p5:80.66, p25:95.38, p50:105.21, p75:115.86, p95:136.92,
    touch:{ "+5":77, "+10":57, "+15":41, "+20":28, "-5":57, "-10":33 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },

  // ---- 28-Jul-2026 roll-forward: COMI/EMFD re-struck on freshly-posted OHLC
  //      (supersedes the same-day 22-Jul market-wide strike for these two names);
  //      Kakao/LGES first roll-forward since their 28-Jun studies. ----
  {
    instrument:"COMI", asset_class:"equity",
    anchor_date:"2026-07-28", anchor_price:142.0, ccy:"EGP",
    horizon_label:"1 month", grade_date:"2026-08-30", grade_basis:"projected", horizon_days:21,
    cycle_no:3, reanchor_from:"2026-07-22", anchor_vol:0.2676,
    note:"Cycle 3 roll-forward, 28-Jul-2026 — struck on the 28-Jul close from freshly-posted OHLC. CORRECTION 28-Jul-2026: originally struck the same day off an INTRADAY 28-Jul bar (COMI 141.50 / EMFD 11.59); re-struck here at the true session closes (COMI 142.00 / EMFD 11.53) and replaced in place before any resolution. Percentiles and touch ladder below are the corrected ones. Supersedes the same-day market-wide re-strike anchored 22-Jul, which predated this data by 3 EGX sessions; that cohort stays open and graded on its own terms (append-only ledger). Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). EG live fit nu=6.0, width_cal=0.951; rf_live 19.50% CBE main operation rate. Horizon resolved by horizons.resolve() on EG's own realized calendar, not a session count.",
    p5:128.4, p25:138.05, p50:144.12, p75:150.51, p95:161.84,
    touch:{ "+5":46, "+10":17, "+15":6, "+20":2, "-5":29, "-10":8 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"COMI", asset_class:"equity",
    anchor_date:"2026-07-28", anchor_price:142.0, ccy:"EGP",
    horizon_label:"3 months", grade_date:"2026-10-28", grade_basis:"projected", horizon_days:62,
    cycle_no:3, reanchor_from:"2026-07-22", anchor_vol:0.2822,
    note:"Cycle 3 roll-forward, 28-Jul-2026 — struck on the 28-Jul close from freshly-posted OHLC. CORRECTION 28-Jul-2026: originally struck the same day off an INTRADAY 28-Jul bar (COMI 141.50 / EMFD 11.59); re-struck here at the true session closes (COMI 142.00 / EMFD 11.53) and replaced in place before any resolution. Percentiles and touch ladder below are the corrected ones. Supersedes the same-day market-wide re-strike anchored 22-Jul, which predated this data by 3 EGX sessions; that cohort stays open and graded on its own terms (append-only ledger). Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). EG live fit nu=6.0, width_cal=0.951; rf_live 19.50% CBE main operation rate. Horizon resolved by horizons.resolve() on EG's own realized calendar, not a session count.",
    p5:120.37, p25:137.46, p50:148.62, p75:160.56, p95:183.42,
    touch:{ "+5":74, "+10":51, "+15":32, "+20":19, "-5":48, "-10":23 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"EMFD", asset_class:"equity",
    anchor_date:"2026-07-28", anchor_price:11.53, ccy:"EGP",
    horizon_label:"1 month", grade_date:"2026-08-30", grade_basis:"projected", horizon_days:21,
    cycle_no:4, reanchor_from:"2026-07-22", anchor_vol:0.3367,
    note:"Cycle 4 roll-forward, 28-Jul-2026 — struck on the 28-Jul close from freshly-posted OHLC. CORRECTION 28-Jul-2026: originally struck the same day off an INTRADAY 28-Jul bar (COMI 141.50 / EMFD 11.59); re-struck here at the true session closes (COMI 142.00 / EMFD 11.53) and replaced in place before any resolution. Percentiles and touch ladder below are the corrected ones. Supersedes the same-day market-wide re-strike anchored 22-Jul, which predated this data by 3 EGX sessions; that cohort stays open and graded on its own terms (append-only ledger). Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). EG live fit nu=6.0, width_cal=0.951; rf_live 19.50% CBE main operation rate. Horizon resolved by horizons.resolve() on EG's own realized calendar, not a session count.",
    p5:10.12, p25:11.09, p50:11.7, p75:12.36, p95:13.54,
    touch:{ "+5":53, "+10":25, "+15":11, "+20":5, "-5":39, "-10":14 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"EMFD", asset_class:"equity",
    anchor_date:"2026-07-28", anchor_price:11.53, ccy:"EGP",
    horizon_label:"3 months", grade_date:"2026-10-28", grade_basis:"projected", horizon_days:62,
    cycle_no:4, reanchor_from:"2026-07-22", anchor_vol:0.3653,
    note:"Cycle 4 roll-forward, 28-Jul-2026 — struck on the 28-Jul close from freshly-posted OHLC. CORRECTION 28-Jul-2026: originally struck the same day off an INTRADAY 28-Jul bar (COMI 141.50 / EMFD 11.59); re-struck here at the true session closes (COMI 142.00 / EMFD 11.53) and replaced in place before any resolution. Percentiles and touch ladder below are the corrected ones. Supersedes the same-day market-wide re-strike anchored 22-Jul, which predated this data by 3 EGX sessions; that cohort stays open and graded on its own terms (append-only ledger). Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). EG live fit nu=6.0, width_cal=0.951; rf_live 19.50% CBE main operation rate. Horizon resolved by horizons.resolve() on EG's own realized calendar, not a session count.",
    p5:9.19, p25:10.91, p50:12.07, p75:13.34, p95:15.85,
    touch:{ "+5":77, "+10":58, "+15":42, "+20":29, "-5":58, "-10":34 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"Kakao", asset_class:"other",
    anchor_date:"2026-07-28", anchor_price:35650, ccy:"KRW",
    horizon_label:"1 month", grade_date:"2026-08-28", grade_basis:"projected", horizon_days:22,
    cycle_no:2, reanchor_from:"2026-06-26",
    config_note:"Corrected 29-Jul-2026: this cycle was originally struck with the prior market-default fit; the per-name override decided the same day (see engine/fit_overrides.json) genuinely improves this specific name's own LONO verdict, so the anchor/grade dates are unchanged but the distribution was recomputed under the correct config.", anchor_vol:0.4749,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — first roll-forward since the 28-Jun published study, struck on the 28-Jul close from freshly-posted OHLC. The 26-Jun cycle-1 1-month matured and is graded in this same update. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). KR live fit nu=10.0, width_cal=1.063; rf_live 3.00% BOK base rate. Horizon resolved by horizons.resolve() on KRX's own realized calendar, not a session count.",
    p5:27814.21, p25:32498.94, p50:35717.27, p75:39311.86, p95:45869.23,
    touch:{ "+5":65, "+10":44, "+15":28, "+20":18, "-5":62, "-10":39 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"Kakao", asset_class:"other",
    anchor_date:"2026-07-28", anchor_price:35650, ccy:"KRW",
    horizon_label:"3 months", grade_date:"2026-10-28", grade_basis:"projected", horizon_days:62,
    cycle_no:2, reanchor_from:"2026-06-26",
    config_note:"Corrected 29-Jul-2026: this cycle was originally struck with the prior market-default fit; the per-name override decided the same day (see engine/fit_overrides.json) genuinely improves this specific name's own LONO verdict, so the anchor/grade dates are unchanged but the distribution was recomputed under the correct config.", anchor_vol:0.4599,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — first roll-forward since the 28-Jun published study, struck on the 28-Jul close from freshly-posted OHLC. The 26-Jun cycle-1 1-month matured and is graded in this same update. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). KR live fit nu=10.0, width_cal=1.063; rf_live 3.00% BOK base rate. Horizon resolved by horizons.resolve() on KRX's own realized calendar, not a session count.",
    p5:23978.91, p25:30817.91, p50:35986.62, p75:41993.13, p95:53885.8,
    touch:{ "+5":78, "+10":64, "+15":51, "+20":40, "-5":76, "-10":58 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"LGES", asset_class:"other",
    anchor_date:"2026-07-28", anchor_price:314000, ccy:"KRW",
    horizon_label:"1 month", grade_date:"2026-08-28", grade_basis:"projected", horizon_days:22,
    cycle_no:2, reanchor_from:"2026-06-26",
    config_note:"Corrected 29-Jul-2026: this cycle was originally struck with the prior market-default fit; the per-name override decided the same day (see engine/fit_overrides.json) genuinely improves this specific name's own LONO verdict, so the anchor/grade dates are unchanged but the distribution was recomputed under the correct config.", anchor_vol:0.5327,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — first roll-forward since the 28-Jun published study, struck on the 28-Jul close from freshly-posted OHLC. The 26-Jun cycle-1 1-month matured and is graded in this same update. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). KR live fit nu=10.0, width_cal=1.063; rf_live 3.00% BOK base rate. Horizon resolved by horizons.resolve() on KRX's own realized calendar, not a session count.",
    p5:239661.03, p25:283872.78, p50:314576.54, p75:349157.25, p95:412942.73,
    touch:{ "+5":67, "+10":47, "+15":32, "+20":21, "-5":64, "-10":42 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"LGES", asset_class:"other",
    anchor_date:"2026-07-28", anchor_price:314000, ccy:"KRW",
    horizon_label:"3 months", grade_date:"2026-10-28", grade_basis:"projected", horizon_days:62,
    cycle_no:2, reanchor_from:"2026-06-26",
    config_note:"Corrected 29-Jul-2026: this cycle was originally struck with the prior market-default fit; the per-name override decided the same day (see engine/fit_overrides.json) genuinely improves this specific name's own LONO verdict, so the anchor/grade dates are unchanged but the distribution was recomputed under the correct config.", anchor_vol:0.5169,
    note:"Cycle 2 roll-forward, 28-Jul-2026 — first roll-forward since the 28-Jun published study, struck on the 28-Jul close from freshly-posted OHLC. The 26-Jun cycle-1 1-month matured and is graded in this same update. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). KR live fit nu=10.0, width_cal=1.063; rf_live 3.00% BOK base rate. Horizon resolved by horizons.resolve() on KRX's own realized calendar, not a session count.",
    p5:203112.53, p25:267452.66, p50:317026.47, p75:375503.78, p95:493606.95,
    touch:{ "+5":80, "+10":66, "+15":54, "+20":44, "-5":77, "-10":61 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },

  // ---- 29-Jul-2026 single-name roll-forward: 2POINTZERO, struck on its own
  //      latest library close. Append-only.
  {
    instrument:"2POINTZERO", asset_class:"equity",
    anchor_date:"2026-07-24", anchor_price:2.06, ccy:"AED",
    horizon_label:"1 month", grade_date:"2026-08-24", grade_basis:"projected", horizon_days:20,
    cycle_no:2, reanchor_from:"2026-07-03", anchor_vol:0.3682,
    note:"Cycle 2 roll-forward, 29-Jul-2026 — struck on the 24-Jul-2026 close, the latest session in this name’s library. This name was NOT in the 28-Jul-2026 market-wide EG/AE/SA re-strike, so its published cone had been anchored 2026-07-03 against a library that had already moved on — the gap the as-of stamps adopted 29-Jul-2026 made visible. Cycle 1 stays OPEN and grades on its own terms; nothing retro-edited. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). AE live fit nu=10.0, width_cal=0.979; rf_live 3.65% CBUAE base rate (AED peg -> Fed path). Horizon resolved by horizons.resolve() on AE’s own realized calendar, not a session count. This cohort also brings the name onto the calendar 1M/3M convention it had never been migrated to.",
    p5:1.75, p25:1.94, p50:2.07, p75:2.2, p95:2.43,
    touch:{ "+5":53, "+10":27, "+15":13, "+20":6, "-5":49, "-10":22 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"2POINTZERO", asset_class:"equity",
    anchor_date:"2026-07-24", anchor_price:2.06, ccy:"AED",
    horizon_label:"3 months", grade_date:"2026-10-26", grade_basis:"projected", horizon_days:63,
    cycle_no:2, reanchor_from:"2026-07-03", anchor_vol:0.3892,
    note:"Cycle 2 roll-forward, 29-Jul-2026 — struck on the 24-Jul-2026 close, the latest session in this name’s library. This name was NOT in the 28-Jul-2026 market-wide EG/AE/SA re-strike, so its published cone had been anchored 2026-07-03 against a library that had already moved on — the gap the as-of stamps adopted 29-Jul-2026 made visible. Cycle 1 stays OPEN and grades on its own terms; nothing retro-edited. Production chain, no approximation: Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 → har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → simulate_paths_v3, 50,000 paths, seed 42, signal OFF. q_annual=0 (FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND price carry and overstates the centre by roughly the yield). AE live fit nu=10.0, width_cal=0.979; rf_live 3.65% CBUAE base rate (AED peg -> Fed path). Horizon resolved by horizons.resolve() on AE’s own realized calendar, not a session count. This cohort also brings the name onto the calendar 1M/3M convention it had never been migrated to.",
    p5:1.53, p25:1.85, p50:2.08, p75:2.34, p95:2.84,
    touch:{ "+5":74, "+10":56, "+15":41, "+20":29, "-5":70, "-10":48 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  }
,
  {
    instrument:"INFY", asset_class:"equity",
    anchor_date:"2026-07-28", anchor_price:1105, ccy:"INR",
    horizon_label:"1 month", grade_date:"2026-08-28", cycle_no:2, reanchor_from:"2026-07-06",
    p5:959.15, p25:1045.89, p50:1110.42, p75:1179.88, p95:1288.55,
    touch:{ "+5":53, "+10":26, "+15":10, "+20":4, "-5":47, "-10":18 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"INFY", asset_class:"equity",
    anchor_date:"2026-07-28", anchor_price:1105, ccy:"INR",
    horizon_label:"3 months", grade_date:"2026-10-28", cycle_no:2, reanchor_from:"2026-07-06",
    p5:882.46, p25:1017.23, p50:1123.94, p75:1241.11, p95:1431.22,
    touch:{ "+5":72, "+10":51, "+15":34, "+20":22, "-5":64, "-10":39 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"RELIANCE", asset_class:"equity",
    anchor_date:"2026-07-28", anchor_price:1271.8, ccy:"INR",
    horizon_label:"1 month", grade_date:"2026-08-28", cycle_no:2, reanchor_from:"2026-07-06",
    config_note:"Corrected 29-Jul-2026: this cycle was originally struck with the prior market-default fit; the per-name override decided the same day (see engine/fit_overrides.json) genuinely improves this specific name's own LONO verdict, so the anchor/grade dates are unchanged but the distribution was recomputed under the correct config.",
    p5:1144.56, p25:1227.46, p50:1278.17, p75:1331.34, p95:1427.61,
    touch:{ "+5":39, "+10":13, "+15":4, "+20":2, "-5":32, "-10":8 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"RELIANCE", asset_class:"equity",
    anchor_date:"2026-07-28", anchor_price:1271.8, ccy:"INR",
    horizon_label:"3 months", grade_date:"2026-10-28", cycle_no:2, reanchor_from:"2026-07-06",
    config_note:"Corrected 29-Jul-2026: this cycle was originally struck with the prior market-default fit; the per-name override decided the same day (see engine/fit_overrides.json) genuinely improves this specific name's own LONO verdict, so the anchor/grade dates are unchanged but the distribution was recomputed under the correct config.",
    p5:1060.54, p25:1201.62, p50:1293.19, p75:1390.72, p95:1576.35,
    touch:{ "+5":65, "+10":40, "+15":23, "+20":13, "-5":53, "-10":27 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"TMPV", asset_class:"equity",
    anchor_date:"2026-07-28", anchor_price:324.15, ccy:"INR",
    horizon_label:"1 month", grade_date:"2026-08-28", cycle_no:2, reanchor_from:"2026-06-30",
    config_note:"Corrected 29-Jul-2026: this cycle was originally struck with the prior market-default fit; the per-name override decided the same day (see engine/fit_overrides.json) genuinely improves this specific name's own LONO verdict, so the anchor/grade dates are unchanged but the distribution was recomputed under the correct config.",
    p5:287.2, p25:310.33, p50:325.75, p75:342.21, p95:369.77,
    touch:{ "+5":46, "+10":18, "+15":6, "+20":2, "-5":39, "-10":12 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"TMPV", asset_class:"equity",
    anchor_date:"2026-07-28", anchor_price:324.15, ccy:"INR",
    horizon_label:"3 months", grade_date:"2026-10-28", cycle_no:2, reanchor_from:"2026-06-30",
    config_note:"Corrected 29-Jul-2026: this cycle was originally struck with the prior market-default fit; the per-name override decided the same day (see engine/fit_overrides.json) genuinely improves this specific name's own LONO verdict, so the anchor/grade dates are unchanged but the distribution was recomputed under the correct config.",
    p5:261.85, p25:301.8, p50:329.67, p75:359.96, p95:413.98,
    touch:{ "+5":69, "+10":47, "+15":30, "+20":18, "-5":60, "-10":34 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"AAPL", asset_class:"equity",
    anchor_date:"2026-07-27", anchor_price:336.91, ccy:"USD",
    horizon_label:"1 month", grade_date:"2026-08-27", cycle_no:2, reanchor_from:"2026-07-06",
    config_note:"Corrected 29-Jul-2026: this cycle was originally struck with the prior market-default fit; the per-name override decided the same day (see engine/fit_overrides.json) genuinely improves this specific name's own LONO verdict, so the anchor/grade dates are unchanged but the distribution was recomputed under the correct config.",
    p5:294.17, p25:320.62, p50:337.8, p75:356.2, p95:387.93,
    touch:{ "+5":47, "+10":20, "+15":8, "+20":3, "-5":43, "-10":15 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"AAPL", asset_class:"equity",
    anchor_date:"2026-07-27", anchor_price:336.91, ccy:"USD",
    horizon_label:"3 months", grade_date:"2026-10-27", cycle_no:2, reanchor_from:"2026-07-06",
    config_note:"Corrected 29-Jul-2026: this cycle was originally struck with the prior market-default fit; the per-name override decided the same day (see engine/fit_overrides.json) genuinely improves this specific name's own LONO verdict, so the anchor/grade dates are unchanged but the distribution was recomputed under the correct config.",
    p5:267.37, p25:310.49, p50:340.32, p75:372.83, p95:434.07,
    touch:{ "+5":69, "+10":47, "+15":30, "+20":19, "-5":63, "-10":38 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"NVDA", asset_class:"equity",
    anchor_date:"2026-07-27", anchor_price:196.51, ccy:"USD",
    horizon_label:"1 month", grade_date:"2026-08-27", cycle_no:2, reanchor_from:"2026-07-06",
    p5:157.05, p25:179.56, p50:196.99, p75:216.37, p95:247.97,
    touch:{ "+5":65, "+10":43, "+15":27, "+20":16, "-5":62, "-10":38 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"NVDA", asset_class:"equity",
    anchor_date:"2026-07-27", anchor_price:196.51, ccy:"USD",
    horizon_label:"3 months", grade_date:"2026-10-27", cycle_no:2, reanchor_from:"2026-07-06",
    p5:132.59, p25:168.27, p50:198.69, p75:234.29, p95:298.15,
    touch:{ "+5":79, "+10":66, "+15":54, "+20":43, "-5":77, "-10":61 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"TSLA", asset_class:"equity",
    anchor_date:"2026-07-27", anchor_price:309.22, ccy:"USD",
    horizon_label:"1 month", grade_date:"2026-08-27", cycle_no:2, reanchor_from:"2026-06-30",
    config_note:"Corrected 29-Jul-2026: this cycle was originally struck with the prior market-default fit; the per-name override decided the same day (see engine/fit_overrides.json) genuinely improves this specific name's own LONO verdict, so the anchor/grade dates are unchanged but the distribution was recomputed under the correct config.",
    p5:233.26, p25:275.93, p50:309.92, p75:348.65, p95:413.66,
    touch:{ "+5":70, "+10":51, "+15":37, "+20":25, "-5":67, "-10":47 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"TSLA", asset_class:"equity",
    anchor_date:"2026-07-27", anchor_price:309.22, ccy:"USD",
    horizon_label:"3 months", grade_date:"2026-10-27", cycle_no:2, reanchor_from:"2026-06-30",
    config_note:"Corrected 29-Jul-2026: this cycle was originally struck with the prior market-default fit; the per-name override decided the same day (see engine/fit_overrides.json) genuinely improves this specific name's own LONO verdict, so the anchor/grade dates are unchanged but the distribution was recomputed under the correct config.",
    p5:192.65, p25:256.31, p50:312.78, p75:381.08, p95:508.68,
    touch:{ "+5":82, "+10":70, "+15":60, "+20":50, "-5":80, "-10":66 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  }
,
  {
    instrument:"QGTS", asset_class:"equity",
    anchor_date:"2026-07-28", anchor_price:4.165, ccy:"QAR",
    horizon_label:"1 month", grade_date:"2026-08-30", cycle_no:2, reanchor_from:"2026-07-05",
    config_note:"First roll-forward since the per-name fit override adopted this name's improved (nu, width_cal) on 29-Jul-2026 (see engine/fit_overrides.json); struck via the standard production chain, no shortcut.",
    p5:3.671, p25:3.984, p50:4.177, p75:4.381, p95:4.754,
    touch:{ "+5":44, "+10":18, "+15":7, "+20":3, "-5":39, "-10":13 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"QGTS", asset_class:"equity",
    anchor_date:"2026-07-28", anchor_price:4.165, ccy:"QAR",
    horizon_label:"3 months", grade_date:"2026-10-28", cycle_no:2, reanchor_from:"2026-07-05",
    config_note:"First roll-forward since the per-name fit override adopted this name's improved (nu, width_cal) on 29-Jul-2026 (see engine/fit_overrides.json); struck via the standard production chain, no shortcut.",
    p5:3.372, p25:3.881, p50:4.21, p75:4.566, p95:5.253,
    touch:{ "+5":66, "+10":43, "+15":26, "+20":16, "-5":59, "-10":33 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"IQCD", asset_class:"equity",
    anchor_date:"2026-07-28", anchor_price:10.7, ccy:"QAR",
    horizon_label:"1 month", grade_date:"2026-08-30", cycle_no:2, reanchor_from:"2026-07-05",
    config_note:"First roll-forward since the per-name fit override adopted this name's improved (nu, width_cal) on 29-Jul-2026 (see engine/fit_overrides.json); struck via the standard production chain, no shortcut.",
    p5:9.814, p25:10.369, p50:10.733, p75:11.115, p95:11.743,
    touch:{ "+5":32, "+10":7, "+15":2, "+20":0, "-5":26, "-10":4 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"IQCD", asset_class:"equity",
    anchor_date:"2026-07-28", anchor_price:10.7, ccy:"QAR",
    horizon_label:"3 months", grade_date:"2026-10-28", cycle_no:2, reanchor_from:"2026-07-05",
    config_note:"First roll-forward since the per-name fit override adopted this name's improved (nu, width_cal) on 29-Jul-2026 (see engine/fit_overrides.json); struck via the standard production chain, no shortcut.",
    p5:9.237, p25:10.178, p50:10.812, p75:11.483, p95:12.666,
    touch:{ "+5":58, "+10":30, "+15":14, "+20":6, "-5":48, "-10":20 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  }
];

/* ==========================================================================
   BACKTEST — historical coverage replay of the PUBLISHED model on past windows.
   SEPARATE from the forward LEDGER above and NOT counted in the "were we right?"
   score. Each row is a past anchor whose horizon already elapsed (realized_* known).
   evidence: "quasi-OOS"  (calibrated class, different name, e.g. PHDC)
             "in-sample"  (TMGH — the class was calibrated from it; plumbing only)
             "illustrative" (uncalibrated class — shape only, not a record)
   fields: instrument, asset_class, anchor_date, anchor_price, horizon_label,
           p5,p25,p50,p75,p95, realized_close, realized_high, realized_low,
           in_90, in_50, evidence
   ========================================================================== */
const BACKTEST = [
  {anchor_date:"2021-06-01", instrument:"PHDC", horizon_label:"3 months", p5:1.184, p50:1.832, p95:2.837, realized_close:1.995, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2021-09-01", instrument:"PHDC", horizon_label:"3 months", p5:1.407, p50:2.179, p95:3.373, realized_close:1.766, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2021-11-28", instrument:"PHDC", horizon_label:"3 months", p5:1.246, p50:1.928, p95:2.985, realized_close:1.614, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2022-02-22", instrument:"PHDC", horizon_label:"3 months", p5:1.138, p50:1.762, p95:2.729, realized_close:1.169, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2022-05-26", instrument:"PHDC", horizon_label:"3 months", p5:0.825, p50:1.277, p95:1.976, realized_close:1.4, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2022-08-28", instrument:"PHDC", horizon_label:"3 months", p5:0.988, p50:1.529, p95:2.367, realized_close:1.649, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2022-11-21", instrument:"PHDC", horizon_label:"3 months", p5:1.163, p50:1.801, p95:2.788, realized_close:2.16, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2023-02-16", instrument:"PHDC", horizon_label:"3 months", p5:1.524, p50:2.359, p95:3.652, realized_close:1.843, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2023-05-22", instrument:"PHDC", horizon_label:"3 months", p5:1.3, p50:2.013, p95:3.116, realized_close:1.962, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2023-08-23", instrument:"PHDC", horizon_label:"3 months", p5:1.384, p50:2.142, p95:3.317, realized_close:2.87, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2023-11-19", instrument:"PHDC", horizon_label:"3 months", p5:2.024, p50:3.134, p95:4.852, realized_close:3.69, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2024-02-14", instrument:"PHDC", horizon_label:"3 months", p5:2.603, p50:4.029, p95:6.238, realized_close:3.32, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2024-05-19", instrument:"PHDC", horizon_label:"3 months", p5:2.342, p50:3.625, p95:5.613, realized_close:5.2, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2024-08-21", instrument:"PHDC", horizon_label:"3 months", p5:3.668, p50:5.678, p95:8.791, realized_close:5.7, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2024-11-17", instrument:"PHDC", horizon_label:"3 months", p5:4.021, p50:6.224, p95:9.636, realized_close:6.1, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2025-02-11", instrument:"PHDC", horizon_label:"3 months", p5:4.303, p50:6.661, p95:10.312, realized_close:6.79, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2025-05-18", instrument:"PHDC", horizon_label:"3 months", p5:4.789, p50:7.415, p95:11.479, realized_close:7.96, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2025-08-19", instrument:"PHDC", horizon_label:"3 months", p5:5.615, p50:8.692, p95:13.457, realized_close:8.18, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2025-11-13", instrument:"PHDC", horizon_label:"3 months", p5:5.77, p50:8.932, p95:13.829, realized_close:8.89, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2026-02-10", instrument:"PHDC", horizon_label:"3 months", p5:6.271, p50:9.708, p95:15.029, realized_close:14.0, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2021-06-01", instrument:"TMGH", horizon_label:"3 months", p5:4.516, p50:6.224, p95:8.579, realized_close:7.43, in_90:true, evidence:"in-sample"},
  {anchor_date:"2021-09-01", instrument:"TMGH", horizon_label:"3 months", p5:5.845, p50:8.057, p95:11.105, realized_close:7.99, in_90:true, evidence:"in-sample"},
  {anchor_date:"2021-11-28", instrument:"TMGH", horizon_label:"3 months", p5:6.286, p50:8.664, p95:11.942, realized_close:9.5, in_90:true, evidence:"in-sample"},
  {anchor_date:"2022-02-22", instrument:"TMGH", horizon_label:"3 months", p5:7.474, p50:10.302, p95:14.199, realized_close:7.55, in_90:true, evidence:"in-sample"},
  {anchor_date:"2022-05-26", instrument:"TMGH", horizon_label:"3 months", p5:5.94, p50:8.187, p95:11.284, realized_close:7.73, in_90:true, evidence:"in-sample"},
  {anchor_date:"2022-08-28", instrument:"TMGH", horizon_label:"3 months", p5:6.081, p50:8.382, p95:11.553, realized_close:8.53, in_90:true, evidence:"in-sample"},
  {anchor_date:"2022-11-21", instrument:"TMGH", horizon_label:"3 months", p5:6.711, p50:9.25, p95:12.749, realized_close:9.99, in_90:true, evidence:"in-sample"},
  {anchor_date:"2023-02-16", instrument:"TMGH", horizon_label:"3 months", p5:7.859, p50:10.833, p95:14.931, realized_close:8.54, in_90:true, evidence:"in-sample"},
  {anchor_date:"2023-05-22", instrument:"TMGH", horizon_label:"3 months", p5:6.719, p50:9.261, p95:12.764, realized_close:10.3, in_90:true, evidence:"in-sample"},
  {anchor_date:"2023-08-23", instrument:"TMGH", horizon_label:"3 months", p5:8.103, p50:11.169, p95:15.395, realized_close:24.86, in_90:false, evidence:"in-sample"},
  {anchor_date:"2023-11-19", instrument:"TMGH", horizon_label:"3 months", p5:19.558, p50:26.957, p95:37.156, realized_close:44.42, in_90:false, evidence:"in-sample"},
  {anchor_date:"2024-02-14", instrument:"TMGH", horizon_label:"3 months", p5:34.946, p50:48.168, p95:66.391, realized_close:60.9, in_90:true, evidence:"in-sample"},
  {anchor_date:"2024-05-19", instrument:"TMGH", horizon_label:"3 months", p5:47.912, p50:66.038, p95:91.023, realized_close:55.92, in_90:true, evidence:"in-sample"},
  {anchor_date:"2024-08-21", instrument:"TMGH", horizon_label:"3 months", p5:43.994, p50:60.638, p95:83.58, realized_close:60.7, in_90:true, evidence:"in-sample"},
  {anchor_date:"2024-11-17", instrument:"TMGH", horizon_label:"3 months", p5:47.754, p50:65.821, p95:90.724, realized_close:50.9, in_90:true, evidence:"in-sample"},
  {anchor_date:"2025-02-11", instrument:"TMGH", horizon_label:"3 months", p5:40.044, p50:55.194, p95:76.077, realized_close:53.0, in_90:true, evidence:"in-sample"},
  {anchor_date:"2025-05-18", instrument:"TMGH", horizon_label:"3 months", p5:41.696, p50:57.472, p95:79.215, realized_close:55.21, in_90:true, evidence:"in-sample"},
  {anchor_date:"2025-08-19", instrument:"TMGH", horizon_label:"3 months", p5:43.435, p50:59.868, p95:82.518, realized_close:71.6, in_90:true, evidence:"in-sample"},
  {anchor_date:"2025-11-13", instrument:"TMGH", horizon_label:"3 months", p5:56.329, p50:77.641, p95:107.015, realized_close:88.97, in_90:true, evidence:"in-sample"},
  {anchor_date:"2026-02-10", instrument:"TMGH", horizon_label:"3 months", p5:69.995, p50:96.476, p95:132.977, realized_close:97.51, in_90:true, evidence:"in-sample"},
  {anchor_date:"2021-06-01", instrument:"EMFD", horizon_label:"3 months", p5:1.684, p50:2.335, p95:3.238, realized_close:2.46, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2021-09-01", instrument:"EMFD", horizon_label:"3 months", p5:1.909, p50:2.647, p95:3.67, realized_close:2.58, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2021-11-28", instrument:"EMFD", horizon_label:"3 months", p5:2.002, p50:2.776, p95:3.849, realized_close:2.74, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2022-02-22", instrument:"EMFD", horizon_label:"3 months", p5:2.126, p50:2.948, p95:4.088, realized_close:2.63, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2022-05-26", instrument:"EMFD", horizon_label:"3 months", p5:2.041, p50:2.83, p95:3.924, realized_close:2.7, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2022-08-28", instrument:"EMFD", horizon_label:"3 months", p5:2.095, p50:2.905, p95:4.029, realized_close:2.66, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2022-11-21", instrument:"EMFD", horizon_label:"3 months", p5:2.064, p50:2.862, p95:3.969, realized_close:3.15, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2023-02-16", instrument:"EMFD", horizon_label:"3 months", p5:2.444, p50:3.389, p95:4.7, realized_close:2.79, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2023-05-22", instrument:"EMFD", horizon_label:"3 months", p5:2.165, p50:3.002, p95:4.163, realized_close:2.98, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2023-08-23", instrument:"EMFD", horizon_label:"3 months", p5:2.312, p50:3.206, p95:4.446, realized_close:3.75, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2023-11-19", instrument:"EMFD", horizon_label:"3 months", p5:2.91, p50:4.035, p95:5.595, realized_close:6.55, in_90:false, evidence:"quasi-OOS"},
  {anchor_date:"2024-02-14", instrument:"EMFD", horizon_label:"3 months", p5:5.083, p50:7.048, p95:9.773, realized_close:5.95, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2024-05-19", instrument:"EMFD", horizon_label:"3 months", p5:4.617, p50:6.402, p95:8.878, realized_close:6.99, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2024-08-21", instrument:"EMFD", horizon_label:"3 months", p5:5.424, p50:7.521, p95:10.429, realized_close:8.29, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2024-11-17", instrument:"EMFD", horizon_label:"3 months", p5:6.433, p50:8.92, p95:12.369, realized_close:6.68, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2025-02-11", instrument:"EMFD", horizon_label:"3 months", p5:5.183, p50:7.188, p95:9.967, realized_close:9.1, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2025-05-18", instrument:"EMFD", horizon_label:"3 months", p5:7.061, p50:9.792, p95:13.578, realized_close:8.47, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2025-08-19", instrument:"EMFD", horizon_label:"3 months", p5:6.572, p50:9.114, p95:12.638, realized_close:10.0, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2025-11-13", instrument:"EMFD", horizon_label:"3 months", p5:7.76, p50:10.76, p95:14.921, realized_close:9.7, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2026-02-10", instrument:"EMFD", horizon_label:"3 months", p5:7.527, p50:10.437, p95:14.473, realized_close:11.1, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2022-02-22", instrument:"PRDC", horizon_label:"3 months", p5:1.417, p50:2.047, p95:2.929, realized_close:1.71, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2022-05-26", instrument:"PRDC", horizon_label:"3 months", p5:1.136, p50:1.717, p95:2.565, realized_close:1.83, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2022-08-28", instrument:"PRDC", horizon_label:"3 months", p5:1.215, p50:1.837, p95:2.747, realized_close:1.83, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2022-11-21", instrument:"PRDC", horizon_label:"3 months", p5:1.361, p50:1.835, p95:2.455, realized_close:2.15, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2023-02-16", instrument:"PRDC", horizon_label:"3 months", p5:1.537, p50:2.157, p95:3.0, realized_close:1.96, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2023-05-22", instrument:"PRDC", horizon_label:"3 months", p5:1.397, p50:1.966, p95:2.743, realized_close:2.01, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2023-08-23", instrument:"PRDC", horizon_label:"3 months", p5:1.398, p50:2.017, p95:2.882, realized_close:2.14, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2023-11-19", instrument:"PRDC", horizon_label:"3 months", p5:1.547, p50:2.146, p95:2.954, realized_close:3.24, in_90:false, evidence:"quasi-OOS"},
  {anchor_date:"2024-02-14", instrument:"PRDC", horizon_label:"3 months", p5:2.248, p50:3.251, p95:4.657, realized_close:2.5, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2024-05-19", instrument:"PRDC", horizon_label:"3 months", p5:1.726, p50:2.509, p95:3.611, realized_close:3.04, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2024-08-21", instrument:"PRDC", horizon_label:"3 months", p5:2.133, p50:3.05, p95:4.321, realized_close:3.4, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2024-11-17", instrument:"PRDC", horizon_label:"3 months", p5:2.459, p50:3.421, p95:4.718, realized_close:3.18, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2025-02-11", instrument:"PRDC", horizon_label:"3 months", p5:2.334, p50:3.189, p95:4.323, realized_close:3.32, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2025-05-18", instrument:"PRDC", horizon_label:"3 months", p5:2.511, p50:3.332, p95:4.389, realized_close:3.35, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2025-08-19", instrument:"PRDC", horizon_label:"3 months", p5:2.501, p50:3.364, p95:4.491, realized_close:3.85, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2025-11-13", instrument:"PRDC", horizon_label:"3 months", p5:2.827, p50:3.9, p95:5.334, realized_close:4.27, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2026-02-10", instrument:"PRDC", horizon_label:"3 months", p5:3.091, p50:4.349, p95:6.066, realized_close:5.73, in_90:true, evidence:"quasi-OOS"},
];

/* ---------- calculator data ----------
   Verified 11 Jun 2026 (end-of-year values). Sources:
   usdEgp: CBE / FocusEconomics (2023:30.93, 2024:50.83, 2025:~47.45)
   egx30: EGX official annual table via Wikipedia (1996-2023) + 31 Dec 2025 close 41,828.97; 2024 ~29,661 (+19.5%)
   inflation: CAPMAS/CBE annual average urban headline (2024:28.3, 2025:~14.0 per CBE)
   gold21g: local sagha quotes; 31 Dec 2025 = 5,910 EGP/g (Dostor). 2022-23 embed the
            parallel-FX premium (that's what buyers actually paid). Pre-2024 values are
            best-effort archival reconstructions (+/-5%).
   cdRate: best available 1-yr fixed CD per year (NBE/BM announcements) - archival approx.
   usdRate: best available 1-yr USD deposit/CD per year to an Egyptian saver (NBE/BM FX certificates) - archival approx. */
const CALC = {
  verified: true,
  years: [2015,2016,2017,2018,2019,2020,2021,2022,2023,2024,2025],
  usdEgp:   [7.83, 18.12, 17.78, 17.92, 16.05, 15.73, 15.72, 24.72, 30.93, 50.83, 47.45],
  gold21g:  [234, 587, 652, 646, 685, 840, 809, 1640, 3200, 3760, 5910],   // EGP per gram, 21k
  egx30:    [7089, 12345, 15019, 13036, 13962, 10845, 11949, 14599, 24833, 29661, 41829],
  cdRate:   [12.5, 20.0, 20.0, 17.0, 15.0, 11.0, 11.0, 18.0, 22.5, 27.0, 21.5],  // best annual EGP CD %
  usdRate:  [2.5,  2.5,  2.0,  2.5,  2.5,  1.5,  1.5,  3.5,  5.0,  5.0,  4.0],     // best annual USD deposit/CD % to an Egyptian saver (archival approx, +/-)
  inflation:[10.4, 13.8, 29.5, 14.4, 9.4, 5.1, 5.2, 13.9, 33.9, 28.3, 14.0]      // % avg per year
};

/* =========================================================================
   METALS — single source for non-EGX, USD-denominated instruments (gold, ...),
   mirroring TICKERS for equities. Drives BOTH the metal page (window.GOLDDATA
   is assigned from METALS.GOLD after data.js loads) AND the RSS feed
   (scripts/generate_feed.js emits USD/oz items). Separate from TICKERS so the
   equity UI (app.js / index.html, which iterate TICKERS) is unaffected.
   ========================================================================= */
const METALS = {
  GOLD: {
    slug: "gold",
    unit: "دولار للأونصة",   // Arabic unit (AR feed)
    unitEn: "USD/oz",         // English unit (EN feed)
    nameAr: "الذهب",          // Arabic display name (AR feed)
 name:"Gold", code:"XAU/USD", spot:4090.87, spotDate:"close 28 Jul 2026", ccy:"USD",
 fair:{ bear:4200, base:4600, full:5000 },
 dist:{
   t20:{ label:"1 month",  p5:3731.05, p25:3954.13, p50:4103.08, p75:4258.48, p95:4514.88, resolve:"2026-08-27" },
   t60:{ label:"3 months", p5:3516.74, p25:3876.91, p50:4129.38, p75:4397.44, p95:4852.47, resolve:"2026-10-27" },
   t252:{ label:"12 months", p5:3139.64, p25:3778.26, p50:4241.75, p75:4761.14, p95:5721.35, resolve:"2027-06-25" }
 },
 touch:[[4800,1,11],[4600,4,22],[4500,9,31],[4300,33,58],[4200,57,75],[3800,15,36],[3700,6,23],[3600,2,14],[3500,1,8]],
 levels: { res:[4230, 4382, 4577], sup:[3967, 3420, 3270] },
 tech: {
   trend: "Mixed against the moving-average stack, below a flat 200-day; fresh death-cross",
   summary: "The price closed 4091 below a falling 50-day (4206) and a flat 200-day (4494), but above a falling 20-day (4077). Momentum is neutral: RSI(14) is ~48 and the daily ATR near 86 (~2.1%) points to a normal tape. MACD (12\u00b726\u00b79) is below zero but turning up (\u221234 / \u221250 / +16). The 50-day crossed beneath the 200-day 24 sessions ago \u2014 a fresh death-cross, a momentum-regime change rather than noise inside an intact trend. Over the last year it has ranged 3311\u20135595; the last close sits 27% below that high and 24% above that low.",
   bull: "A daily close back above 4230 would clear the nearest resistance and open the 4577 zone.",
   bear: "A close below 3967 would break the nearest support and open the 3270 zone."
 },
 asof: {
   mc:   { data:"2026-07-27", computed:"2026-07-29" },
   tech: { data:"2026-07-27", computed:"2026-07-29" }
 },
 files:{
   study:"files/XAUUSD_Valuation_Study_25-06-2026_public.docx?v=2506",
   model:"files/XAUUSD_Valuation_Study_25-06-2026_public.xlsx?v=2506",
   pdf:"files/XAUUSD_Valuation_Study_25-06-2026_public.pdf?v=2506"
 }
  },
  SILVER: {
    slug: "silver",
    unit: "دولار للأونصة",   // Arabic unit (AR feed)
    unitEn: "USD/oz",         // English unit (EN feed)
    nameAr: "الفضة",          // Arabic display name (AR feed)
 name:"Silver", code:"XAG/USD", spot:57.207, spotDate:"close 28 Jul 2026", ccy:"USD",
 fair:{ bear:58, base:68, full:78 },
 dist:{
   t20:{ label:"1 month",  p5:46.19, p25:52.73, p50:57.38, p75:62.46, p95:71.38, resolve:"2026-08-28" },
   t60:{ label:"3 months", p5:40.19, p25:50.1, p50:57.78, p75:66.6, p95:83.21, resolve:"2026-10-28" },
   t252:{ label:"12 months", p5:30.8, p25:46.12, p50:59.36, p75:76.36, p95:113.99, resolve:"2027-07-02" }
 },
 touch:[[85,1,7],[78,2,15],[72,7,27],[68,15,39],[58,82,89],[55,66,78],[50,24,46],[45,5,22]],
 levels: { res:[64.06, 71.23, 83.31], sup:[61.27, 55.62, 54.45] },
 tech: {
   trend: "Trading below the whole moving-average stack, under a rising 200-day",
   summary: "The price closed 62.42 below a falling 20-day (63.15), a falling 50-day (71.04) and a rising 200-day (70.20). Momentum is neutral: RSI(14) is ~44 and the daily ATR near 3.49 (~5.6%) points to a volatile tape. MACD (12\u00b726\u00b79) is below zero but turning up (\u22123.37 / \u22123.67 / +0.30). Over the last year it has ranged 36.21\u2013121.67; the last close sits 49% below that high and 72% above that low.",
   bull: "A daily close back above 64.06 would clear the nearest resistance and open the 83.31 zone.",
   bear: "A close below 61.27 would break the nearest support and open the 54.45 zone."
 },
 asof: {
   mc:   { data:"2026-07-28", computed:"2026-07-29" },
   tech: { data:"2026-07-28", computed:"2026-07-29" }
 },
 files:{
   study:"files/XAGUSD_Combined_1-3-12M_Valuation_Study_05-07-2026_public.docx?v=2607",
   model:"files/XAGUSD_Combined_1-3-12M_Valuation_Model_05-07-2026_public.xlsx?v=2607",
   pdf:"files/XAGUSD_Combined_1-3-12M_Valuation_Study_05-07-2026_public.pdf?v=2607"
 }
  },
  PLATINUM: {
    slug: "platinum",
    unit: "دولار للأونصة",   // Arabic unit (AR feed)
    unitEn: "USD/oz",         // English unit (EN feed)
    nameAr: "البلاتين",       // Arabic display name (AR feed)
 name:"Platinum", code:"XPT/USD", spot:1608.37, spotDate:"close 20 Jul 2026", ccy:"USD",
 fair:{ bear:1310, base:1634, full:2139 },
 dist:{
   t20:{ label:"1 month",  p5:1382, p25:1514, p50:1613, p75:1718, p95:1882, resolve:"2026-08-17" },
   t60:{ label:"3 months", p5:1239, p25:1453, p50:1623, p75:1813, p95:2128, resolve:"2026-10-12" },
   t252:{ label:"12 months", p5:961, p25:1333, p50:1669, p75:2086, p95:2897, resolve:"2027-07-07" }
 },
 touch:[ [2400,0,1], [2222,0,5], [1990,2,19], [1750,32,58], [1700,49,70], [1540,55,72], [1500,38,61], [1348,4,24], [1200,0,6] ],
 levels: { res:[1640, 1670, 1726], sup:[1513, 1440, 1350] },
 tech: {
   trend: "Trading below the whole moving-average stack, under a flat 200-day; fresh death-cross",
   summary: "The price closed 1608 below a falling 20-day (1611), a falling 50-day (1758) and a flat 200-day (1926). Momentum is neutral: RSI(14) is ~44 and the daily ATR near 62 (~3.8%) points to a lively tape. MACD (12\u00b726\u00b79) is below zero but turning up (\u221237 / \u221246 / +9). The 50-day crossed beneath the 200-day 20 sessions ago \u2014 a fresh death-cross, a momentum-regime change rather than noise inside an intact trend. Over the last year it has ranged 1260\u20132924; the last close sits 45% below that high and 28% above that low.",
   bull: "A daily close back above 1640 would clear the nearest resistance and open the 1726 zone.",
   bear: "A close below 1513 would break the nearest support and open the 1350 zone."
 },
 asof: {
   mc:   { data:"2026-07-20", computed:"2012-01-05" },
   tech: { data:"2026-07-20", computed:"2026-07-29" }
 },
 files:{
   study:"files/XPTUSD_Valuation_Study_20-07-2026_public.docx?v=2007",
   model:"files/XPTUSD_Valuation_Model_20072026_public.xlsx?v=2007",
   pdf:"files/XPTUSD_Valuation_Study_20-07-2026_public.pdf?v=2007"
 }
  }
};
