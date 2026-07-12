/* =========================================================
   testahil — the ONLY file you edit in the weekly ritual.
   ========================================================= */

const SITE = { updated: "2026-07-12", latest: "BURJEEL" };  // latest = the LAST-PUBLISHED study (drives the homepage hero); set this on every publish

/* ---------- covered tickers ---------- */
const TICKERS = {
  BURJEEL: {
    name: "Burjeel Holdings PLC",
    nameAr: "\u0628\u0631\u062c\u064a\u0644 \u0627\u0644\u0642\u0627\u0628\u0636\u0629",
    code: "ADX:BURJEEL",
    spot: 1.11,
    spotDate: "close 10 Jul 2026",
    ccy: "AED",
    fair: { bear: 1.14, base: 1.85, full: 2.35 },      // 12 Jul 2026 (rev. 2 reissue) — four-lens weighted central 1.85 (+67% vs spot 1.11). bear/full = weighted bear/bull. Lenses: FCFF DCF (primary, 35%) 2.64, relative EV/EBITDA (25%) 1.89 at a 11.5x base — a deliberate discount to the verified GCC hospital-peer FLOOR (MEH ~13x; Al Habib 24-34x, Dallah 22-26x, Mouwasat 18-19x, Hammadi 17.5x — Bloomberg/U Capital, MarketScreener, multiples.vc, dated), normalized earnings (25%) 1.49 at 17x clean FY26E EPS, dividend discount (15%) 0.56 reflecting the FY2025 payout cut. TAX REBUILT ON MECHANICS, NOT THE HEADLINE: the UAE's 15% DMTT top-up applies only to income above a substance-based income exclusion (9.4% of payroll + 7.4% of tangible assets in 2026, stepping to 5%/5% by 2033) — Burjeel's own FY2025 effective rate was 7.0% (tax 38 on PBT 541), consistent with a 10-to-13% modelled path rather than a flat 15%; the transitional CbCR safe harbour can deem the top-up zero outright for FYs starting pre-2027. Flat 15% is kept as the bear rung only. THE CRUX IS CASH, NOT THE STORY: FY2025 absorbed AED 649mn of operating surplus into working capital before it reached cash (DSO 135 days, rising), which is why the marginal sukuk priced at 7.00%/5yr (BB+) against a ~3.9% sovereign, and why the dividend was cut. Spot 1.11 sits just BELOW the weighted bear case (1.14): the market prices a margin stuck in the high-teens, the full 15% assessed with no substance relief, receivables never normalizing, Saudi staying a rounding error, and zero credit for a management team that guided a 23.5% margin and delivered 18.1% — then discounts a little further. Genuinely thin float (~11%; some 2024-25 buyback execution undisclosed) keeps idiosyncratic volatility high. Calibration: PARITY on the production UAE panel (11 non-overlapping 60-day windows, CRPS skill +0.85%, 90% CI [-1.7%, +2.5%], robust across bootstrap block sizes) — a calibrated, market-panel-validated distribution with no single-name edge claimed.
    dist: {
      t20: { label:"1 month (T+20)",  p5:0.94, p25:1.04, p50:1.11, p75:1.18, p95:1.31, resolve:"2026-08-07" },
      t60: { label:"3 months (T+60)", p5:0.84, p25:1.00, p50:1.11, p75:1.24, p95:1.49, resolve:"2026-10-02" }
    },
    touch: [ /* descending high -> low; P(touch) T+20 %, T+60 %. */
      [1.30, 8, 31], [1.25, 18, 43], [1.20, 34, 59], [1.15, 61, 78], [1.05, 46, 67], [1.00, 22, 47], [0.95, 9, 30], [0.90, 3, 18]
    ],
    levels: { res:[1.13, 1.23, 1.57], sup:[1.09, 1.05, 1.00] },
    tech: {
      trend: "Sits just above the 50-day (AED 1.09) but below the 20-, 100- and 200-day averages (1.13 / 1.13 / 1.23) \u2014 a matted average stack, not a clean trend; RSI-14 at 49.7 is neutral",
      summary: "Burjeel at AED 1.11 sits inside a flattened moving-average stack: just above the 50-day (1.09) but below the 20-day (1.13), the 100-day (1.13) and the 200-day (1.23). RSI(14) near 49.7 is neutral \u2014 no oversold signal. The daily MACD (12\u00b726\u00b79) reads 0.006 line vs 0.0121 signal, histogram -0.0061 \u2014 the line sits below its signal, a mildly bearish read. The 52-week range is AED 1.00\u20131.57 and spot sits near the lower quarter of it, down 24.5% over the trailing year and 68.7% off its all-time high. Realised volatility is high (~31% annualized) on a genuinely thin (~11%) float \u2014 idiosyncratic risk, not a market-wide read.",
      bull: "A daily close back above the 100-day near AED 1.13 opens the 200-day at 1.23 and then the 52-week high at 1.57.",
      bear: "Losing the 50-day near AED 1.09 exposes the 52-week low at AED 1.00, a level touched 7-Apr-2026."
    },
    files: {
      study: "files/BURJEEL_Valuation_Study_11-07-2026_public.docx?v=20260712b",
      model: "files/BURJEEL_Valuation_Model_11072026_public.xlsx?v=20260712b",
      pdf:   "files/BURJEEL_Valuation_Study_11-07-2026_public.pdf?v=20260712b"
    }
  },
  SALIK: {
    name: "Salik Company",
    nameAr: "\u0633\u0627\u0644\u0643",
    code: "DFM:SALIK",
    spot: 5.70,
    spotDate: "close 10 Jul 2026",
    ccy: "AED",
    fair: { bear: 3.32, base: 4.62, full: 7.05 },      // 12 Jul 2026 (v3) — four-lens weighted central 4.62 (-19% vs spot 5.70). Lenses: FCFF DCF (primary, 45%) 4.49, normalized earnings power (20%) 5.44, relative P/E which with a 100% payout IS the dividend yield (20%) 4.89, dividend discount (15%) 3.55 — the DDM is a structural FLOOR because the payout is 100% of PROFIT but only 93% of CASH. bear/full = weighted bear/bull. BETA IS MEASURED, NOT ASSUMED: weekly regression vs an equal-weighted 14-name UAE market portfolio (both exchanges) gives β 0.637 (n=195, t=6.1, R² 16%) — the gate PASSES; we publish the Blume-adjusted 0.76. THE CRUX: SALIK's beta was 0.47 BEFORE the war and 1.00 DURING it. The war cut Q1 chargeable trips 7.7% AND doubled the discount rate's risk loading — numerator and denominator at once. Spot implies β 0.52, inside our measured 95% CI [0.43, 0.84] and almost exactly the PRE-WAR reading: the market is pricing Salik as though the war is already over. TWO OTHER FINDINGS: (1) the 8 gates the RTA HANDED Salik at the IPO earn 32% ROIC; the 2 it SOLD Salik in 2024 for AED 2,734mn earn 9.5% against an 8.1% WACC — growth by acquiring gates is not free growth. (2) 84% of FY2025's +35% revenue growth was two one-offs (gate count 8→10; tariff flat→variable). And a senior claim sits in front of the dividend: AED 455.7mn/yr to the RTA until Nov-2030 against a retained wedge of only AED 116mn.
    dist: {
      t20: { label:"1 month (T+20)",  p5:4.94, p25:5.40, p50:5.70, p75:6.02, p95:6.57, resolve:"2026-08-07" },
      t60: { label:"3 months (T+60)", p5:4.42, p25:5.17, p50:5.69, p75:6.28, p95:7.34, resolve:"2026-10-02" }
    },
    touch: [ /* descending high -> low; P(touch) T+20 %, T+60 %. NOTE: the calibration back-test cone is OVER-COVERED, so read these as UPPER BOUNDS. */
      [7.00, 2, 15], [6.50, 11, 33], [6.25, 23, 47], [6.00, 46, 66], [5.50, 58, 75], [5.25, 27, 52], [5.00, 10, 33], [4.50, 1, 10]
    ],
    levels: { res:[5.87, 6.00, 6.85], sup:[5.72, 5.25, 4.99] },
    tech: {
      trend: "Below every moving average in the stack (20/50/100/200-day) — the stock broke down in the March war selloff and has not reclaimed it; RSI-14 at 46 is neutral, with no oversold bounce signal",
      summary: "The tape is mildly negative and it is not saying anything the fundamentals are not already saying. Salik at AED 5.70 sits below its 20-day (AED 5.87), 50-day (5.72), 100-day (5.74) and 200-day (5.96) — the opposite of a repaired uptrend. RSI(14) near 46 is neutral. The daily MACD (12·26·9) reads 0.006 line vs 0.043 signal, histogram -0.037 — the line has crossed BELOW its signal. The 52-week range is AED 4.99–6.85 and spot sits about 38% up it. Realised 252-day volatility is 28% — high, and roughly twice the UAE market portfolio's; but 88% of that risk is IDIOSYNCRATIC, which is exactly how a 26%-volatility stock carries a 0.64 beta. Volatility and beta are not the same thing, and for Salik they point in opposite directions.",
      bull: "A daily close back above the 20-day near AED 5.87 opens AED 6.00 and then the 52-week high at 6.85.",
      bear: "Losing the 50-day near AED 5.72 exposes AED 5.25 and then the 52-week low at 4.99."
    },
    files: {
      study: "files/SALIK_Valuation_Study_11-07-2026_public.docx?v=20260712b",
      model: "files/SALIK_Valuation_Model_11072026_public.xlsx?v=20260712b",
      pdf:   "files/SALIK_Valuation_Study_11-07-2026_public.pdf?v=20260712b",
      biblio:"files/SALIK_Source_Register_11-07-2026.docx?v=20260712b"
    }
  },
  DIB: {
    name: "Dubai Islamic Bank",
    nameAr: "بنك دبي الإسلامي",
    code: "DFM:DIB",
    spot: 7.72,
    spotDate: "close 03 Jul 2026",
    ccy: "AED",
    fair: { bear: 8.14, base: 10.18, full: 11.20 },      // 11 Jul 2026 — five-lens weighted central 10.18 (+32% vs spot 7.72). Lenses: DDM (primary, 30%) 10.90, residual income (20%) 11.20, FCFE equity DCF (15%) 10.44, relative multiples same-day-anchored on ADCB (20%) 8.14, normalized through-cycle (15%) 9.86. bear/full = relative lens / residual-income lens. Ke 10.57% (rf 4.70% + β1.00×ERP4.87% + 1.0pt war adder). MONTE CARLO FAILED calibration on this name (skill score −0.025 vs random walk, robust across every resampling scheme; study §3.1) — §3 is an illustrative volatility map only, no forecast published. Swing factors: the net profit margin path, the pace of cost-of-risk normalization off a tripled Q1-26 print, and whether the Iran-war ceasefire holds. UAE's largest Islamic bank; dividend cut 45→35 fils Feb-2026.
    dist: {
      t20: { label:"1 month (T+20)",  p5:6.97, p25:7.45, p50:7.72, p75:7.99, p95:8.55, resolve:"2026-08-05" },
      t60: { label:"3 months (T+60)", p5:6.46, p25:7.25, p50:7.71, p75:8.19, p95:9.18, resolve:"2026-10-02" }
    },
    touch: [ /* descending high -> low; illustrative only, calibration FAILED */
      [8.88, 9, 33], [10.20, 18, 44], [8.63, 34, 55], [7.76, 45, 66], [7.59, 44, 64], [7.40, 33, 54], [7.09, 12, 30]
    ],
    levels: { res:[7.76, 8.63, 10.20], sup:[7.59, 7.40, 7.09] },
    tech: {
      trend: "Above the 20- and 50-day averages but below the 100- and 200-day — a base building after the war leg, not yet a repaired trend",
      summary: "Price at AED 7.72 sits above the 20-day (AED 7.59) and 50-day (7.40) but below the 100-day (7.76) and 200-day (8.63) — the opposite stack from a fully repaired uptrend. RSI-14 near 57 is neutral. MACD (12,26,9) reads 0.055 / 0.063 / -0.008: the line is above zero but the histogram is marginally negative — momentum pausing, not accelerating. The stock is 24% below its 9-Feb all-time high of AED 10.20 and only 9% above its 23-Apr 52-week low of AED 7.09.",
      bull: "A daily close back above AED 7.76 opens the 200-day near 8.63; clearing that puts the AED 10.20 all-time high back in range.",
      bear: "Losing the 20-day near AED 7.59 exposes the 50-day at 7.40; below that, the AED 7.09 52-week low is the next shelf."
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
    spot: 2.16,
    spotDate: "close 03 Jul 2026",
    ccy: "AED",
    fair: { bear: 1.55, base: 1.91, full: 2.27 },      // 11 Jul 2026 — four-lens weighted central 1.91 (-11.7% vs spot 2.16). Lenses: sum-of-the-parts (primary, 45%) 1.95 — operating businesses marked on their own earnings, investment portfolio at management's mark less a 25% opacity discount, cash at par, less a 7.5% structural discount; DCF on the operating legs + portfolio (ceiling, 15%) 2.39 (TV 81% of operating EV, disclosed); relative on reported earnings with a normalised mark contribution (25%) 1.85; underlying earnings, no marks at all (floor, 15%) 1.39. THE CRUX: the AED 58.7bn investment portfolio is carried against AED 48.0bn invested — a AED 10.7bn gain. But the 7.29% TAQA stake sold on 11-Jun-2026 (9,095,702,934 shares at AED 2.37) was worth ~AED 21.6bn against AED 10bn paid. Strip it out and the REST of the portfolio — now entirely unlisted — is carried AED 0.9bn BELOW cost. The entire mark-up was one listed stake, and it has been sold, with ~AED 14.4bn of the proceeds redeployed into unlisted assets (Traverse, Mopani, Alphamin, ISEM). Operating economics are disclosed and modest: gross margin 30%, G&A 18% of revenue → ~12% operating margin — NOT the 25% that a blended adjusted-EBITDA figure implies, because that figure has AED 1.2bn/qtr of portfolio income inside it. Tax modelled at the statutory 15% DMTT floor (no phase-in exists). Attributable ratio 84.2%, derived from the PUBLISHED Q1-26 EPS of AED 0.056. Beta assumed 1.0 (regression failed our usability test; no downloadable ADX index series), sensitised 0.8–1.3.
    dist: {
      t20: { label:"1 month (T+20)",  p5:1.80, p25:2.02, p50:2.17, p75:2.33, p95:2.59, resolve:"2026-07-31" },
      t60: { label:"3 months (T+60)", p5:1.59, p25:1.93, p50:2.18, p75:2.46, p95:3.00, resolve:"2026-09-25" }
    },
    touch: [ /* descending high -> low; P(touch) T+20 %, T+60 % */
      [2.60, 8, 29], [2.40, 28, 53], [2.20, 76, 87], [2.00, 38, 60], [1.90, 18, 42], [1.80, 8, 27]
    ],
    levels: { res:[2.42, 2.43, 3.26], sup:[2.07, 2.00, 1.65] },
    tech: {
      trend: "Recovery inside a downtrend — price above the 20/50/100-day averages but 11% below the 200-day; RSI neutral near 37",
      summary: "The tape is unresolved. 2POINTZERO trades above its 20-day (AED 2.19), 50-day (2.12) and 100-day (2.07) averages, but sits 11% below the 200-day (2.42) — the signature of a bounce inside a downtrend, not a new uptrend. The 52-week range is AED 1.65–3.26 and spot sits in the lower third of it. RSI(14) at 37 is dead neutral, and the daily MACD (12·26·9) has just rolled over (0.0139 line vs 0.0289 signal, histogram -0.0151) — the post-trough impulse is spent. Realised 252-day volatility is about 39%, which is why the §3 cone is wide.",
      bull: "A daily close back above AED 2.46 (the Monte-Carlo T+60 75th percentile) opens the 200-day at 2.42 and then par book at 2.43.",
      bear: "Losing the 20-day near AED 2.19 exposes the T+60 25th percentile at 1.93 and then the war low at 1.65."
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
    spot: 19.66,
    spotDate: "close 09 Jul 2026",
    ccy: "AED",
    fair: { bear: 17.61, base: 22.72, full: 28.75 },      // 11 Jul 2026 — four-lens weighted central 22.72 (+15.5% vs spot 19.66). Lenses: FCFF DCF + sourced stakes-and-claims bridge (primary, 35%) 28.38 (TV 79% of EV, disclosed; core EV under the production UAE Monte-Carlo panel fit does not feed this lens), dividend discount (policy lens, 25%) 17.03, relative EV/EBITDA through the same bridge (20%) 23.72, normalized earnings (20%) 18.90. bear/full = weighted bear/bull. The crux is the 2027 UAE federal royalty reset (current 38%+9% regime expires 31-Dec-2026, undecided): each 4pp of royalty ≈ AED 1.1/share. Same-day event: 10-Jul-2026 e& agreed to sell its entire Vodafone stake for AED 21.8bn gross (~4.7bn net cash), pending regulatory approvals — carried at deal value, dual-framed against the undisturbed mark. Beta assumed 1.0 (regression inaccessible; no downloadable ADX General Index series found after two independent attempts), sensitised 0.8–1.3.
    dist: {
      t20: { label:"1 month (T+20)",  p5:17.84, p25:19.05, p50:19.72, p75:20.43, p95:21.81, resolve:"2026-08-06" },
      t60: { label:"3 months (T+60)", p5:16.70, p25:18.68, p50:19.86, p75:21.09, p95:23.59, resolve:"2026-10-02" }
    },
    touch: [ /* descending high -> low; P(touch) T+20 %, T+60 % */
      [22.00, 6, 24], [21.00, 21, 46], [20.00, 66, 81], [19.00, 42, 62], [18.00, 10, 28], [17.00, 3, 12]
    ],
    levels: { res:[20.50, 21.09, 21.60], sup:[19.43, 18.99, 17.40] },
    tech: {
      trend: "Fully bullish-ordered moving-average stack (price above the 20/50/100/200-day averages); RSI in the high-50s (constructive, not overbought)",
      summary: "The tape is constructive. e& trades above its 20-day (AED 19.43), 50-day (18.99), 100-day (19.33) and 200-day (19.09) averages — a bullish stack — with the 52-week range at AED 17.40–21.60 (spot sits about 54% up that range). RSI(14) near 58 is firm but not overbought, and the daily MACD (12·26·9) shows a mildly positive histogram (0.195 line vs 0.182 signal, +0.013) — quiet, constructive momentum. Realised 252-day volatility is about 22%, in line with the production UAE market-panel calibration (ν=4, cone width 1.07).",
      bull: "A daily close back above AED 20.50 opens the 21.09 (the Monte-Carlo T+60 75th percentile) and then the 52-week high at 21.60.",
      bear: "Losing the 20-day near AED 19.43 exposes the 50-day (18.99) and then the 52-week low at 17.40."
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
    spot: 15.10,
    spotDate: "close 03 Jul 2026",
    ccy: "AED",
    fair: { bear: 14.3, base: 19.7, full: 23.3 },      // 10 Jul 2026 — five-lens weighted central 19.7 (+31% vs spot 15.10). Lenses: DDM (primary, 30%) 21.2, residual income (multi-period, 20%) 22.7, FCFE equity DCF (15%) 23.3, relative multiples (20%) 15.9, normalized through-cycle (15%) 14.3. bear/full = normalized floor / FCFE ceiling. War-adjusted Ke 10.57% (rf 4.70% + β1.0×ERP4.87% + 1.0pt war adder). Swing factors: the NIM path through the CBUAE/Fed easing cycle, whether the ~16% ROE persists, and Gulf de-escalation. Third-largest UAE bank; AED 6.1bn rights issue closed Dec-2025.
    dist: {
      t20: { label:"1 month (T+20)",  p5:13.28, p25:14.43, p50:15.09, p75:15.79, p95:17.20, resolve:"2026-08-05" },
      t60: { label:"3 months (T+60)", p5:12.04, p25:13.95, p50:15.09, p75:16.32, p95:18.87, resolve:"2026-10-02" }
    },
    touch: [ /* descending high -> low; P(touch) T+20 %, T+60 % */
      [17.20, 7, 29], [16.40, 23, 49], [15.80, 47, 68], [14.40, 46, 67], [13.90, 23, 49], [13.30, 8, 31]
    ],
    levels: { res:[15.79, 16.42, 16.54], sup:[14.40, 14.26, 13.90] },
    tech: {
      trend: "Above all four major moving averages; RSI in the mid-60s (firm, not overbought) — a constructive tape holding the upper half of its range",
      summary: "The tape is firm. ADCB trades above its 20-day (AED 14.40), 50-day (13.90), 100-day (13.92) and 200-day (14.26) averages — a bullish stack — with price about 8% below the January all-time high of 16.54. RSI(14) near 65 is firm but not yet overbought, while the daily MACD (12·26·9) shows a mild bearish cross (0.287 line vs 0.304 signal, histogram −0.018) — a pause within an uptrend, not a reversal. The 52-week band is AED 11.98–16.42; realized 60-day volatility is calm for a single name and the gap-aware cone reads the regime near 26%.",
      bull: "A daily close back above AED 15.80 opens the January high near 16.42–16.54; clearing that would put the round 17.00+ in play.",
      bear: "Losing the 20-day near AED 14.40 exposes the 200-day at 14.26 and the 13.90 shelf; below that, 13.30 is the next support."
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
    spot: 658.50,
    spotDate: "close 07 Jul 2026",
    ccy: "SAR",
    fair: { bear: 530, base: 620, full: 720 },      // 10 Jul 2026 — weighted central ~620 (−5.8% vs spot 658.50): roughly fairly valued, a slight premium. Lenses: DCF (primary, β=1.0 neutral, WACC 10.5%, g 4%, 40%) 576, forward P/E (24× 2025e EPS 28.6, 30%) 686, EV/EBITDA (18–20× 2025e, 25%) ~625, MC T+60 median 664. bear/full = football-field range 530–720. The crux is the discount rate: 77% of DCF value is terminal, so a low-beta government-defensive read (β 0.7, WACC 9%) gives ~750, neutral (β 1.0) ~576, and a high-beta post-crash re-rate (β 1.6, WACC 13.5%) ~396. Second swing: registry-exclusivity durability behind the ~46%-margin Digital Business.
    dist: {
      t20: { label:"1 month (T+20)",  p5:543, p25:610, p50:660, p75:715, p95:803, resolve:"2026-08-04" },
      t60: { label:"3 months (T+60)", p5:471, p25:577, p50:664, p75:763, p95:934, resolve:"2026-09-29" }
    },
    touch: [ /* descending high -> low */
      [757.3, 19, 46], [724.4, 35, 60], [691.4, 58, 76], [625.6, 55, 73], [592.6, 29, 54], [559.7, 13, 37]
    ],
    levels: { res:[695, 730, 795], sup:[593, 546, 510] },
    tech: {
      trend: "Below all four moving averages (20/50/100/200) after a ~49% de-rate from the Jan-2025 peak; RSI mid-30s (oversold-leaning), MACD negative but flattening — a washed-out downtrend near support",
      summary: "Elm crashed from an all-time high of SAR 1,289 (P/E ~56×) in January 2025 to SAR 658.5 (P/E ~24×), and trades below its 20-day (SAR 695), 50-day (670), 100-day (634) and 200-day (730) averages — a clean downtrend, not a top being made. RSI(14) near 37 is oversold-leaning and the MACD histogram is negative but flattening; price sits in the lower third of a 52-week band of SAR 510–983. The v3 engine reads current 60-day regime width at ~33% annualised — about two-thirds wider than a Saudi bank like Alinma, reflecting Elm's growth-stock volatility.",
      bull: "A daily close back above the SAR 695–730 moving-average cluster would end the downtrend; fundamentally the case re-rates up if the market prices Elm as the low-beta government compounder it has historically been (β ~0.4 → WACC ~8% → DCF ~750–900).",
      bear: "A daily close below SAR 590 opens 546 and then the 52-week-low shelf near SAR 510; fundamentally, a high-beta post-crash re-rate (β ~1.6 → WACC ~13.5%) or any erosion of registry exclusivity drops fair value toward the mid-400s."
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
    spot: 8.22,
    spotDate: "close 03 Jul 2026 — pre the 7–8 Jul war re-escalation, flagged in the study",
    ccy: "AED",
    fair: { bear: 5.95, base: 7.13, full: 8.63 },      // 10 Jul 2026, reweighted 11 Jul 2026 — weighted central 7.13 (−13% vs spot 8.22). Holdco SOTP/NAV primary: four listed stakes at ADX marks (Aldar 31.63% = AED 20.5bn, NMDC 76.68% = 14.4bn, PureHealth 35.06% = 8.6bn, NCTH 73.73% = 2.4bn) + Trojan 51% at the ADQ transaction buyer-outlay mark (5.2bn; seller-note framing 3.71bn carried as a sensitivity) + residual audited book → NAV 7.44/sh at par, 6.32 at a 15% holdco discount (55% weight, raised from 45% on 11 Jul 2026). Consolidated FCFF DCF 11.72 = a multi-year ceiling (80% TV, ΔWC absorption) at 15%; look-through relative 8.07 cut to 15% weight (from 25%, external-audit double-count flag upheld); dividend-policy DDM 4.55 at 15%. The crux: spot pays ~+10% ABOVE undiscounted NAV — the premium is the trade. bear/full = weighted bear/bull.
    dist: {
      t20: { label:"1 month (T+20)",  p5:7.04, p25:7.73, p50:8.24, p75:8.79, p95:9.67, resolve:"2026-07-31" },
      t60: { label:"3 months (T+60)", p5:6.30, p25:7.42, p50:8.29, p75:9.27, p95:10.93, resolve:"2026-09-25" }
    },
    touch: [ /* descending high -> low */
      [9.50, 11, 36], [8.84, 39, 63], [8.50, 64, 80], [7.44, 23, 48], [7.00, 7, 28], [6.58, 1, 14]
    ],
    levels: { res:[8.50, 8.84, 9.50], sup:[7.80, 7.40, 6.84] },
    tech: {
      trend: "Post-war-trough recovery inside a longer downtrend: above the 20/50/100-day averages, still ~7% below the 200-day",
      summary: "The tape is a recovery inside a downtrend. Alpha Dhabi slid from the AED 9–12 shelf to an intraday 6.84 on 31 Mar 2026 as Hormuz closed, then retraced on the April ceasefire; at 8.22 it sits above its 20-day (7.84), 50-day (7.54) and 100-day (7.85) averages but below the 200-day (8.84) — the classic signature of a bounce that has not yet become a new uptrend. RSI(14) at 64 is warm but not overbought, and the MACD histogram has flattened to ~0: the post-trough momentum impulse is spent and price is deciding at the middle of its 52-week range (6.84–12.58). One-year return −33%. Note the data ends 3 Jul — the 7–8 Jul ceasefire collapse post-dates every level here.",
      bull: "A daily close above the 200-day (~8.84) that holds would turn the recovery into a trend and re-open the 9.5–10.3 zone (the Monte-Carlo 75th–90th).",
      bear: "Losing the 7.4–7.8 congestion shelf targets par NAV (7.44) and then the discounted-NAV zone; the war low at 6.84 is the line under everything."
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
    spot: 68.10,
    spotDate: "close 09 Jul 2026",
    ccy: "SAR",
    fair: { bear: 66, base: 81, full: 92 },      // 10 Jul 2026 — weighted central 81 (+19% vs spot 68.10). Split-legs SOTP: retail operating-co DCF (SAR 65/sh, net-cash, Ke ~9.5%) + Tasheel, the 68.75%-owned captive consumer-finance lender (SAR 25/sh, equity book × justified P/B). SOTP 90 (primary), relative P/E 12× 75, Monte-Carlo T+60 median 68. bear/full = weighted bear/bull of the football field. Crux: the retail discount rate (regressed β 0.55 on a short window → 0.80 base, sensitized 0.55–1.0) and the Tasheel multiple. At a 52-week low with RSI 27.
    dist: {
      t20: { label:"1 month (T+20)",  p5:59.2, p25:64.6, p50:67.9, p75:71.4, p95:78.2, resolve:"2026-08-06" },
      t60: { label:"3 months (T+60)", p5:53.3, p25:62.0, p50:67.6, p75:73.8, p95:86.2, resolve:"2026-10-04" }
    },
    touch: [ /* descending high -> low */
      [81.7, 3, 16], [74.9, 18, 40], [71.5, 42, 63], [64.7, 42, 65], [61.3, 16, 39], [54.5, 2, 11]
    ],
    levels: { res:[73.4, 76.7, 79.7], sup:[68.1, 65.0, 62.0] },
    tech: {
      trend: "At a 52-week low, below all four major moving averages; oversold and stretched to the downside",
      summary: "The tape is oversold and at its lows. eXtra sits at a 52-week low of SAR 68.1, below its 20-day (SAR 73.4), 50-day (76.7), 100-day (79.7) and 200-day (83.9) averages — a clean downtrend after a slide from the SAR 80–105 range. RSI(14) near 27 is firmly oversold and the MACD histogram is negative. Realized 252-day volatility is ~32% after the Saudi cone width. For a defensive, high-dividend name, a 52-week low with a sub-30 RSI is the kind of setup where price often runs ahead of any change in fundamentals.",
      bull: "A daily close back above the SAR 73–77 moving-average cluster would signal the de-rating is pausing; reclaiming the high-70s needs a consumer-finance stabilisation or a dividend surprise.",
      bear: "There is little chart support below a 52-week low — a sustained break opens the low-60s (the Monte-Carlo 25th percentile) toward the mid-50s tail."
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
    spot: 24.00,
    spotDate: "close 07 Jul 2026",
    ccy: "SAR",
    fair: { bear: 19.90, base: 27.32, full: 31.23 },      // 10 Jul 2026 — weighted central 27.32 (+13.8% vs spot 24.00). Lenses: DDM (primary, terminal payout forced consistent 1−g/ROE_t, 35%) 31.23, residual income (multi-period build, 20%) 28.41, FCFE (equity DCF, 15%) 23.79, relative multiples (20%) 25.68, normalized floor (β=1, CDS ERP, 10%) 19.90. bear/full = normalized floor / DDM ceiling. The crux is the cost of equity: regressed β 0.74 (short window) → Ke 8.5–9.0%; β=1.0 → 9.8–10.5%; base Ke 9.46% is the disclosed four-corner mean, and the market's ~2.1× common book implies ~9.2% — inside the band. Second swing: the NIM glide (3.55% FY25 → 3.40%) through the SAMA/Fed easing cycle.
    dist: {
      t20: { label:"1 month (T+20)",  p5:22.1, p25:23.31, p50:24.00, p75:24.7, p95:26.09, resolve:"2026-08-04" },
      t60: { label:"3 months (T+60)", p5:20.76, p25:22.82, p50:24.00, p75:25.24, p95:27.7, resolve:"2026-09-29" }
    },
    touch: [ /* descending high -> low */
      [27.60, 2, 10], [26.40, 6, 21], [25.20, 23, 47], [22.80, 22, 45], [21.60, 4, 18], [20.40, 1, 7]
    ],
    levels: { res:[25.30, 26.60, 27.80], sup:[23.30, 22.10, 20.40] },
    tech: {
      trend: "Below the 20/50/100-day averages with the 200-day still underfoot; RSI mid-40s — a corrective tape inside an intact long advance",
      summary: "The tape is digesting a strong 2025 run, not breaking down. Alinma sits below its 20-day (SAR 24.77), 50-day (24.32) and 100-day (24.12) averages but above the rising 200-day (22.72). RSI(14) near 11 is neutral-soft and the MACD histogram is negative but flattening — momentum bleeding out rather than accelerating. Price sits mid-range in a 52-week band of SAR 20.05–25.47; the v3 engine reads current 60-day regime width at ~20% annualised.",
      bull: "A daily close back above the SAR 24.6–25.3 moving-average cluster would end the correction; reclaiming the 52-week high near SAR 25.47 needs a NIM-resilience or payout surprise.",
      bear: "A daily close below SAR 23.3 opens 22.1 and then the MA200/20.4 shelf — the line between digestion and a trend change."
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
    spot: 31.25,
    spotDate: "close 7 Jul 2026",
    ccy: "EGP",
    fair: { bear: 23.3, base: 35.7, full: 51.0 },      // AMENDED 09 Jul 2026 (replaces the prior 08-Jul draft; same study cycle, corrected leg build) — weighted central 35.7 (+14% vs spot 31.25). GB Corp's own 9-June-2026 press release ("MNT-Halan ... Closes Capital Increase Round Led by Al Ahly Capital Holding") confirms the current stake directly: "GB Corp's ownership stake in MNT-Halan will be adjusted to 41.61%, compared to 42.58% prior to the transaction" — a dated, current, company-confirmed figure, replacing both the original unsourced ~20% placeholder and the interim 42.58% correction. Four lenses: split-the-legs SOTP (primary) 38.4 (Auto FCFF DCF + GB Capital adjusted book ×1.0 + MNT-Halan at the confirmed 41.61% × the Jun-26 USD 1.4bn round, less a 10% complexity discount), pre-discount NAV 42.6, relative multiples 28.9 (floor, stake-blind), normalized mid-cycle earnings 32.9 (also stake-blind); blend 40/15/20/25. THE REAL OPEN QUESTION: with the stake now confirmed, applying it to the round's valuation implies MNT-Halan alone is worth ~73% of GB Corp's entire market cap — a genuine puzzle, not a sourcing gap. Either the market applies a far steeper discount to this private mark than this study's 10%, or GB Corp is meaningfully mispriced. Treat 35.7 as the read if the round's valuation holds at face value; the stake-blind relative/normalized lenses (28.9–32.9) are the more conservative anchor if you believe the market's skepticism is warranted. Swing factors, in order: the discount applied to the MNT-Halan mark (the stake itself is no longer in question), Auto working-capital release, the CBE rate path. MC PASSES the calibration back-test with the secular drift ON (CRPS skill +3.2% non-overlapping, +9.6% monthly; zero drift FAILED) — entirely unaffected by any of this, since the engine prices the stock's own path, not the SOTP.
    dist: {
      t20: { label:"1 month (T+20)",  p5:26.09, p25:29.96, p50:32.47, p75:35.12, p95:40.53, resolve:"2026-08-04" },
      t60: { label:"3 months (T+60)", p5:23.97, p25:30.62, p50:34.98, p75:40.13, p95:51.08, resolve:"2026-09-29" }
    },
    touch: [ /* level, P(touch) T+20 %, T+60 % — descending; up-levels then down-levels */
      [40.00, 8, 37], [38.00, 15, 50], [36.00, 29, 64], [34.00, 51, 79], [32.00, 82, 93], [30.00, 53, 64], [28.00, 22, 37], [26.00, 9, 20]
    ],
    levels: { res:[31.70, 32.30, 33.40], sup:[29.96, 28.20, 26.73] },
    tech: {
      trend: "Strong uptrend — above all four moving averages, six percent from the all-time high",
      summary: "The advance has come in stair-steps: a February spike to the EGP 33.40 all-time high, a two-month pullback that held near 24, and a renewed leg that has carried price back above every major average. Momentum is positive but not stretched — RSI sits in the low-60s and the MACD histogram has just re-crossed positive. Unusually, the tape is more bullish than the fundamental work: price has led the cash-conversion proof.",
      bull: "A daily close above 32.50 opens a retest of the 33.40 all-time high.",
      bear: "A close below 29.95 (the 20-day) says the leg is tiring; below 28.20 the uptrend structure itself is in question."
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
    spot: 14.26,
    spotDate: "close 3 Jul 2026",
    ccy: "AED",
    fair: { bear: 12.88, base: 17.29, full: 22.76 },      // 08 Jul 2026 — weighted central 17.29 (+21% vs spot 14.26). Four lenses: RNAV / split-NAV (primary) 17.56, going-concern DCF (exit-multiple terminal, not Gordon) 18.43, relative multiples 15.75 (floor), property-cycle earnings 16.88; blend 40/20/15/25. bear/full = weighted bear/bull of the football field. Development legs carry no terminal value; swing factors are the Dubai property cycle, the sustainable development margin and the net-cash mark. A naive Gordon-perpetuity DCF would imply ~27 (disclosed, not used). MC INDICATIVE: the §3 engine (run drift-on for this name) MATCHES — ties — its zero-drift random-walk benchmark in the calibration back-test (CRPS skill ≈ 0, CI spans zero) with a well-calibrated PIT; no demonstrated edge, but not a failed calibration.
    dist: {
      t20: { label:"1 month (T+20)",  p5:12.42, p25:13.78, p50:14.60, p75:15.49, p95:17.18, resolve:"2026-07-31" },
      t60: { label:"3 months (T+60)", p5:11.59, p25:13.87, p50:15.34, p75:16.97, p95:20.33, resolve:"2026-09-25" }
    },
    touch: [ /* descending high -> low; P(touch) T+20 %, T+60 % */
      [18, 4, 23], [17, 9, 37], [16, 23, 57], [15, 57, 81], [14, 65, 75], [13, 19, 35], [12, 5, 15]
    ],
    levels: { res:[14.37, 15.29, 20.00], sup:[13.87, 12.65, 11.59] },
    tech: {
      trend: "Consolidating in the mid-14s after a ~30% correction from the AED 20 high; around the short averages, below the 100/200-day",
      summary: "The tape is corrective and mid-range, not stretched. EMAARDEV has pulled back from a 52-week high near AED 20.00 to the mid-14s and is consolidating: it trades just around its 20-day (14.19) and 50-day (14.37) but below the 100-day (15.29) and 200-day (15.19) — a post-correction pause rather than a breakdown. Momentum is neutral: RSI(14) is ~51 and the daily MACD histogram is marginally negative (−0.04 line / −0.02 signal / −0.02 histogram). Price sits in the lower third of a 52-week band of AED 12.65–20.00; realized 252-day volatility is ~37%, and the YZ-HAR engine reads the current 60-day regime near the same level.",
      bull: "A daily close back above the ~15.2 hundred/two-hundred-day band would signal the correction is stalling; a push toward the AED 17 RNAV/DCF zone, then the AED 20 prior high, would need the Dubai sales pace and margin to hold.",
      bear: "A close below the AED 13.87 shelf, then the AED 12.65 fifty-two-week low, opens the downside as the property cycle and development margin normalise faster than assumed."
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
    spot: 11.67,
    spotDate: "close 7 Jul 2026",
    ccy: "EGP",
    fair: { bear: 12.85, base: 17.78, full: 22.68 },      // 7 Jul 2026 \u2014 weighted central 17.78 (+52% vs spot 11.67). Four lenses: DCF (primary) 19.79, relative EV/EBITDA 16.71, normalized earnings 17.98, dividend-yield floor 11.00; blend 45/25/20/10. bear/full = weighted bear/bull of the football field. Swing: the thin net margin normalising as the CBE rate path eases finance costs and the drug-re-pricing cycle feeds through \u2014 on ~EGP 76.6bn FY25 revenue at an ~8% gross / ~5% EBITDA / ~1.2% net margin with a near-zero cash-conversion cycle. INDICATIVE: the \u00a73 Monte-Carlo engine did NOT beat its zero-drift random-walk benchmark in the calibration back-test (CRPS skill < 0 on every scheme) \u2014 the price map is illustrative only, not a skill-validated forecast.
    dist: {
      t20: { label:"1 month (T+20)",  p5:10.16, p25:11.14, p50:11.75, p75:12.39, p95:13.52, resolve:"2026-08-04" },
      t60: { label:"3 months (T+60)", p5:9.29,  p25:10.85, p50:11.91, p75:13.06, p95:15.18, resolve:"2026-09-29" }
    },
    touch: [ /* descending high -> low; P(touch) T+20 %, T+60 % */
      [13.50, 8, 30], [12.75, 25, 52], [12.25, 48, 70], [12.00, 64, 81], [11.50, 72, 82], [11.00, 35, 56], [10.50, 15, 36]
    ],
    levels: { res:[11.96, 12.75, 13.52], sup:[11.39, 11.23, 9.09] },
    tech: {
      trend: "Just below the two short moving averages and above the two long \u2014 a consolidating, range-bound tape; RSI ~40 neutral-to-soft, MACD mildly negative",
      summary: "The tape is quiet and range-bound. ISPH trades at EGP 11.67, just below its 20-day (11.96) and 50-day (11.68) averages but above the 100-day (11.39) and 200-day (11.23) \u2014 a tight, bunched stack consistent with consolidation after the 2024\u201325 re-rating. RSI(14) near 40 is neutral-to-soft; MACD is mildly negative (\u22120.038 line / 0.047 signal / \u22120.086 histogram). Price sits mid-range in a 52-week band of EGP 9.09\u201312.75; realized 252-day volatility is ~35% and the YZ-HAR engine reads the current 60-day regime near ~29%.",
      bull: "A daily close back above the EGP 11.96 twenty-day and the EGP 12.75 fifty-two-week high would confirm a turn; sustaining it toward EGP 13.50 would need CBE rate relief or a re-pricing surprise feeding the margin.",
      bear: "A daily close below the EGP 11.23 two-hundred-day opens the EGP 11.00 shelf; beneath it the distribution thins toward the EGP 9.09 fifty-two-week low on an FX or receivables shock."
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
    spot: 1321.30,
    spotDate: "close 6 Jul 2026",
    ccy: "INR",
    fair: { bear: 1112, base: 1395, full: 1719 },      // 6 Jul 2026 — weighted central 1,395 (+6% vs spot 1,321.30). Four lenses: sum-of-the-parts (primary) 1,342, consolidated DCF 1,359, relative multiples 1,322 (floor), normalized earnings 1,552 (ceiling); weights 40/20/15/25. bear/full = weighted bear/bull of the football field. Swing: crystallising the unlisted digital (Jio) and retail value via the Jio Platforms IPO (DRHP filed 19 Jun 2026), the O2C refining/petrochemical margin cycle, and the ~5% holding-company discount.
    dist: {
      t20: { label:"1 month (T+20)",  p5:1160, p25:1266, p50:1331, p75:1400, p95:1526, resolve:"2026-08-03" },
      t60: { label:"3 months (T+60)", p5:1067, p25:1235, p50:1351, p75:1478, p95:1707, resolve:"2026-09-28" }
    },
    touch: [ /* level, P(touch) T+20 %, T+60 % — descending */
      [1550, 6, 25], [1500, 11, 36], [1450, 21, 49], [1400, 39, 65], [1350, 68, 83], [1300, 68, 80], [1250, 34, 55], [1200, 15, 36], [1150, 7, 23]
    ],
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
    spot: 196.44,
    spotDate: "close 6 Jul 2026",
    ccy: "USD",
    fair: { bear: 147, base: 204, full: 287 },      // 6 Jul 2026 \u2014 weighted central 204 (+3.9% vs spot 196.44). Lenses: DCF 5-yr FCFF 189 (primary, TV ~79% of EV), relative multiples 200, forward-earnings power 230. bear/full = weighted bear/bull of the football field. Swing: how many years AI data-center capex sustains super-normal growth; China export controls; customer concentration. \u00a73 Monte Carlo PASSED its calibration back-test (CRPS skill +2.7% vs a random-walk cone) \u2014 an honest, skill-validated probability map. International name: zero secular drift, DCF-primary lens.
    dist: {
      t20: { label:"1 month (T+20)",  p5:155.90, p25:179.63, p50:195.34, p75:212.20, p95:244.04, resolve:"2026-08-03" },
      t60: { label:"3 months (T+60)", p5:131.56, p25:166.88, p50:193.31, p75:223.35, p95:282.86, resolve:"2026-09-28" }
    },
    touch: [ /* descending high -> low */
      [240, 10, 29], [230, 17, 39], [220, 29, 52], [210, 48, 67], [200, 76, 85], [190, 69, 82], [180, 41, 64], [170, 22, 48], [160, 10, 34]
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
    spot: 7.00,
    spotDate: "close 6 Jul 2026",
    ccy: "EGP",
    fair: { bear: 1.42, base: 2.39, full: 3.52 },      // 6 Jul 2026 — weighted central 2.39 (\u221266% vs spot 7.00). Four lenses: revalued NAV (primary) 3.28, going-concern DCF 0.54 (floor), relative price-to-book 2.65, normalized earnings 1.24. bear/full = weighted bear/bull of the football field. Swing: the realizable value of the legacy Alexandria land against a ~95%-collapsed earnings base — at 7.00 the market prices a ~EGP 2.8bn land re-mark that has not been disclosed or monetised. Note: \u00a73 Monte Carlo FAILED its calibration back-test on this name (CRPS skill \u22120.010 vs a random-walk cone; study Appendix B) — no probabilistic price forecast is published; the distribution is an illustrative volatility map only.
    dist: {
      t20: { label:"1 month (T+20)",  p5:5.58, p25:6.46, p50:7.03, p75:7.67, p95:8.92, resolve:"2026-08-03" },
      t60: { label:"3 months (T+60)", p5:4.79, p25:6.12, p50:7.12, p75:8.28, p95:10.68, resolve:"2026-09-28" }
    },
    touch: [ /* descending high -> low; illustrative only */
      [9.0, 7, 26], [8.3, 17, 43], [7.7, 39, 63], [7.13, 78, 88], [6.65, 57, 73], [6.3, 33, 55], [5.6, 8, 27], [4.8, 1, 9]
    ],
    levels: { res:[7.13, 7.70, 8.30], sup:[6.30, 6.15, 5.60] },
    tech: {
      trend: "Above all four major moving averages; RSI in the high-70s, MACD positive — a strong, overbought uptrend near an all-time high",
      summary: "The tape is strong and stretched to the upside, the mirror image of the fundamentals. Price sits above the 20-day (EGP 6.30), 50-day (6.19), 100-day (6.14) and 200-day (6.15) moving averages — a full bullish stack — a hair below the EGP 7.13 fifty-two-week high after a run to an all-time high of EGP 7.30 in November 2025. RSI(14) near 78 is overbought; MACD is positive (+0.093 line / +0.040 signal / +0.053 histogram). Realized 252-day volatility is about 35%, and the YZ-HAR engine reads the current 60-day regime near 47% — a thin, jumpy small-cap.",
      bull: "A clean hold above the EGP 7.13 fifty-two-week high on volume would open fresh highs, though the overbought oscillators argue for a pause first.",
      bear: "A daily close back below the EGP 6.30 moving-average cluster would relieve the overbought pressure toward the EGP 6.15 two-hundred-day and, beneath it, the EGP 5.60 shelf."
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
    spot: 11.07,
    spotDate: "close 5 Jul 2026",
    ccy: "QAR",
    fair: { bear: 6.9, base: 10.9, full: 15.0 },      // 5 Jul 2026 — weighted central 10.9 (−2% vs spot 11.07). Five lenses: holdco SOTP (primary) 10.38, consolidated DCF 11.0-11.4, relative multiples 11.02, normalized earnings 11.02, dividend-discount 11.07. bear/full = weighted bear/bull of the football field. Swing factor: petrochemical (QAPCO/QAFAC) margin normalisation from its early-2026 trough (Q1-26 segment NI just QR4mn) plus the Ammonia-7 (Q2-26) and Ras Laffan pipeline; QAFCO fertilizers are the cash anchor, steel a restart option. ~6% dividend yield, debt-free, ~QR8.5bn net cash, QatarEnergy ~51%.
    dist: {
      t20: { label:"1 month (T+20)",  p5:9.62, p25:10.60, p50:11.13, p75:11.68, p95:12.73, resolve:"2026-08-02" },
      t60: { label:"3 months (T+60)", p5:8.84, p25:10.24, p50:11.21, p75:12.25, p95:14.08, resolve:"2026-09-27" }
    },
    touch: [ /* descending high -> low; P(touch) T+20 %, T+60 % */
      [12.5, 13, 42], [12.0, 27, 58], [11.5, 53, 77], [11.0, 77, 84], [10.5, 30, 50], [10.0, 12, 29], [9.5, 5, 16]
    ],
    levels: { res:[11.37, 11.85, 13.41], sup:[10.60, 10.00, 9.13] },
    tech: {
      trend: "Below all four major moving averages; RSI in the mid-30s, MACD mildly negative — a weak, corrective tape near the 52-week low",
      summary: "The tape is weak and has been for a year. Industries Qatar trades below its 20-day (QAR 11.37), 50-day (11.85), 100-day (11.79) and 200-day (12.07) averages — a full bearish stack — sitting near the floor of a QAR 10.60-13.41 fifty-two-week range. RSI(14) near 36 is approaching oversold without being washed out; MACD is mildly negative (−0.24 line / −0.22 signal / −0.02 histogram), so momentum is soft but no longer accelerating down. Realized 252-day volatility is about 20%, and the YZ-HAR engine reads the current 60-day regime near 22%.",
      bull: "A daily close back above the QAR 11.37 twenty-day and the QAR 11.85 moving-average cluster would ease the corrective read; reclaiming the QAR 13.41 fifty-two-week high would need a petrochemical-margin recovery or an Ammonia-7 earnings surprise.",
      bear: "A daily close below the QAR 10.60 fifty-two-week low opens the gap toward the QAR 10.00 round level and, beneath it, the simulated lower quartile — the main driver of the left tail being regional-conflict disruption of Gulf logistics."
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
    spot: 7.70,
    spotDate: "close 1 Jul 2026",
    ccy: "EGP",
    fair: { bear: 4.77, base: 5.56, full: 8.22 },
    dist: {
      t20: { label:"1 month (T+20)", p5:5.68, p25:6.90, p50:7.74, p75:8.66, p95:10.48, resolve:"2026-07-29" },
      t60: { label:"3 months (T+60)", p5:4.60, p25:6.40, p50:7.79, p75:9.45, p95:13.06, resolve:"2026-09-23" }
    },
    touch: [ [10.01, 12, 38], [8.85, 38, 62], [8.09, 70, 83], [7.31, 68, 81], [6.54, 30, 55], [5.39, 4, 22] ],
    levels: { res:[8.0, 8.47, 9.24], sup:[7.31, 6.93, 6.54] },
    tech: {
      trend: "Near the all-time high, above every moving average",
      summary: "Price sits above all four moving averages, stacked in bullish order (20>50>100>200), a hair below the 8.00 all-time high after a run from 2.55 over the past year. RSI ~67 is elevated but not yet overbought; MACD is positive with the histogram flattening. A strong momentum leader — extended, but the trend is intact.",
      bull: "A clean break of 8.00 opens fresh highs toward the mid-8s.",
      bear: "A close back below the ~7.0 shelf relieves the overbought pressure toward the 6.9 fifty-day."
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
    spot: 20.74,
    spotDate: "close 01 Jul 2026",
    ccy: "EGP",
    fair: { bear: 10.20, base: 14.16, full: 23.60 },          // 03 Jul 2026 valuation — weighted four-lens central
    dist: {
      t20: { label:"1 month (T+20)",   p5:16.58, p25:19.13, p50:20.74, p75:22.48, p95:25.94, resolve:"2026-07-29" },
      t60: { label:"3 months (T+60)",  p5:14.08, p25:18.04, p50:20.74, p75:23.85, p95:30.56, resolve:"2026-09-23" }
    },
    touch: [ /* level, P(touch) T+20 %, T+60 % — descending */
      [26.00, 8, 26], [24.00, 21, 44], [23.00, 33, 57], [22.00, 54, 72], [21.00, 81, 89]
    ],
    levels: { res:[21.06, 21.31, 23.28], sup:[20.00, 18.32, 17.50] },
    tech: {
      trend: "Mild pullback, holding above the 200-day",
      summary: "The price eased back below its short-term moving averages after a strong recovery off the 11.20 low, but it is still well above the rising 200-day line. Momentum is neutral (RSI ~46) and the daily MACD is mildly negative, so the pullback may have a little further to run — the larger recovery structure is intact.",
      bull: "A daily close back above the 21.3 50-day line would say the pullback is done.",
      bear: "A close below 20.00 would open the door back toward the 200-day near 18.30."
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
    spot: 29.99,
    spotDate: "close 1 Jul 2026",
    ccy: "EGP",
    fair: { bear: 22, base: 26, full: 33 },
    dist: {
      t20: { label:"1 month (T+20)", p5:26.04, p25:28.92, p50:30.67, p75:32.54, p95:36.15, resolve:"2026-07-29" },
      t60: { label:"3 months (T+60)", p5:24.17, p25:28.96, p50:32.07, p75:35.46, p95:42.63, resolve:"2026-09-23" }
    },
    touch: [ [35.99, 8, 34], [32.99, 31, 63], [31.49, 58, 80], [28.49, 40, 55], [26.99, 16, 32], [23.99, 2, 10] ],
    levels: { res:[30.3, 31.8, 33.0], sup:[29.2, 28.3, 26.2] },
    tech: {
      trend: "Constructive uptrend near 52-week highs — a mild momentum cooling",
      summary: "Price trades above its 50-, 100- and 200-day averages and near the top of its 52-week range, with only a shallow pause — it has slipped just below the 20-day and the MACD histogram has turned mildly negative, while RSI near 51 is neutral. The rising 200-day (~EGP 26) is the visible trend floor; for once the tape agrees with the secular story rather than fighting it.",
      bull: "A daily close back above the 20-day (~EGP 30.3) and the 52-week high near EGP 31.8 would say the pause is over.",
      bear: "A close below the rising 200-day (~EGP 26) would break the trend and open the low-EGP-20s."
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
    spot: 285.88,
    spotDate: "close 1 Jul 2026",
    ccy: "EGP",
    fair: { bear: 183, base: 250, full: 358 },
    dist: {
      t20: { label:"1 month (T+20)", p5:244.5, p25:277.8, p50:298.8, p75:321.2, p95:362.0, resolve:"2026-07-29" },
      t60: { label:"3 months (T+60)", p5:231.5, p25:287.5, p50:326.3, p75:369.4, p95:451.7, resolve:"2026-09-23" }
    },
    touch: [ [343.1, 15, 54], [314.5, 45, 78], [300.2, 69, 89], [271.6, 41, 53], [257.3, 19, 32], [228.7, 4, 11] ],
    levels: { res:[300, 320, 338], sup:[270, 250, 244] },
    tech: {
      trend: "Strong primary uptrend, six weeks into a consolidation",
      summary: "Price sits below the 20- and 50-day averages (301/307) and fractionally under the 100-day, but ~17% above a rising 200-day at 244 — a pause inside a 25-fold five-year advance. RSI 39 is soft, not oversold; the MACD histogram is negative and shallowing. The March high at 338 caps the range; the 240–250 shelf — which coincides with our fair value — is the support that matters.",
      bull: "A daily close back above the 300–307 average cluster resumes the advance toward the 338 high.",
      bear: "A close below the 244–250 shelf (the 200-day) would put the 52-week low regime back in play."
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
    spot: 27.34,
    spotDate: "close 1 Jul 2026",
    ccy: "EGP",
    fair: { bear: 16.41, base: 27.68, full: 42.78 },
    dist: {
      t20: { label:"1 month (T+20)", p5:22.35, p25:25.48, p50:27.48, p75:29.62, p95:33.56, resolve:"2026-07-29" },
      t60: { label:"3 months (T+60)", p5:19.4, p25:24.4, p50:27.82, p75:31.65, p95:38.98, resolve:"2026-09-23" }
    },
    touch: [
      [32.81, 20, 34],
      [30.07, 34, 60],
      [28.71, 43, 76],
      [25.97, 36, 70],
      [24.61, 26, 50],
      [21.87, 12, 22]
    ],
    levels: { res:[28.31, 28.55, 32.50], sup:[25.86, 25.50, 23.95] },
    tech: {
      trend: "A pause inside a completed re-rating — holding above a rising 200-day",
      summary: "From the split-adjusted 2022 low the shares six-folded to an all-time high of 32.50 in February 2026, then spent five months consolidating. At 27.34 the price sits below the 50- and 100-day averages (28.55 / 28.31) but above a rising 200-day (25.86); RSI 46 and a mildly negative MACD read as a stall, not distribution — flat year-to-date, still +106% over twelve months.",
      bull: "A daily close back above the 28.3–28.6 average cluster turns the stack from ceiling into floor and re-opens the February high at 32.50.",
      bear: "Losing the 25.5–25.9 zone (the rising 200-day plus the June swing low) opens 24.6, then the 22.00 shelf."
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
    spot: 2.97,
    spotDate: "close 1 Jul 2026",
    ccy: "EGP",
    fair: { bear: 1.89, base: 2.88, full: 4.13 },
    dist: {
      t20: { label:"1 month (T+20)", p5:2.39, p25:2.74, p50:2.95, p75:3.17, p95:3.58, resolve:"2026-07-29" },
      t60: { label:"3 months (T+60)", p5:2.04, p25:2.53, p50:2.89, p75:3.29, p95:4.04, resolve:"2026-09-23" }
    },
    touch: [ [3.56, 9, 27], [3.27, 30, 51], [3.12, 53, 70], [2.82, 55, 75], [2.67, 30, 57], [2.38, 7, 27] ],
    levels: { res:[3.02, 3.08, 3.30], sup:[2.80, 2.65, 2.40] },
    tech: {
      trend: "Sideways drift below a flat average stack — waiting for proof",
      summary: "Price sits just below all four major averages (the 20/50/100/200-day cluster at 3.02–3.08) after a year spent digesting two record rights issues. RSI 43 and a mildly negative MACD read as soft momentum, not stress — down ~5% over twelve months against a stronger EGX, the tape is waiting for the same ROE proof the valuation is.",
      bull: "A daily close above the 3.02–3.08 average cluster would turn the stack from ceiling into floor.",
      bear: "A close below 2.80 opens the 52-week low at 2.65, then the 2.40 shelf."
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
    spot: 92.61,
    spotDate: "close 1 Jul 2026",
    ccy: "EGP",
    fair: { bear: 82, base: 118, full: 160 },
    dist: {
      t20: { label:"1 month (T+20)", p5:80.7, p25:90.5, p50:96.9, p75:103.7, p95:116.5, resolve:"2026-07-29" },
      t60: { label:"3 months (T+60)", p5:77.5, p25:94.3, p50:106.3, p75:119.4, p95:145.3, resolve:"2026-09-23" }
    },
    touch: [ [111.13, 14, 54], [101.87, 43, 78], [97.24, 68, 89], [87.98, 37, 49], [83.35, 16, 28], [74.09, 3, 8] ],
    levels: { res:[94.6, 105, 113], sup:[91.3, 85, 80] },
    tech: {
      trend: "Consolidating just under the short averages inside a powerful primary uptrend",
      summary: "Price sits a fraction below the 20- and 50-day (93.3/94.6) but above the 100-day and far above a rising 200-day at 74.7, after a ~148% twelve-month run to the February all-time high of 112.98 and an 18% spring correction. RSI 47 and a fractionally negative MACD read as digestion, not distribution — a high-volatility range in the low-to-mid 90s.",
      bull: "A daily close back above the 93.3–94.6 average cluster reopens 105, then the 112.98 high.",
      bear: "A close below the 100-day at 91.3 opens the 85 shelf, then 80."
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
    spot: 18.4,
    spotDate: "close 1 Jul 2026",
    ccy: "EGP",
    fair: { bear: 11.5, base: 14.7, full: 20.3 },
    dist: {
      t20: { label:"1 month (T+20)", p5:15.45, p25:17.37, p50:18.76, p75:20.22, p95:22.56, resolve:"2026-07-29" },
      t60: { label:"3 months (T+60)", p5:14.05, p25:16.97, p50:19.38, p75:22.09, p95:26.64, resolve:"2026-09-23" }
    },
    touch: [ [22.08, 10, 40], [20.24, 37, 65], [19.32, 61, 80], [17.48, 47, 65], [16.56, 23, 44], [14.72, 4, 16] ],
    levels: { res:[18.9, 19.5, 20.0], sup:[17.5, 17.0, 16.0] },
    tech: {
      trend: "Consolidating in the upper third of a strong uptrend",
      summary: "Price sits just under the 20- and 50-day and on the 100-day, but well above a rising 200-day — a pause inside a strong 12-month advance. RSI ~55 is neutral. Pullbacks to the rising 200-day have been bought all year.",
      bull: "A daily close back above the 19.5 fifty-day resumes the advance toward 20+.",
      bear: "A close below the 17.0–17.5 shelf would change the read."
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
    spot: 67.97,
    spotDate: "close 1 Jul 2026",
    ccy: "EGP",
    fair: { bear: 50, base: 60, full: 72 },
    dist: {
      t20: { label:"1 month (T+20)", p5:51.67, p25:60.72, p50:67.7, p75:75.45, p95:88.03, resolve:"2026-07-29" },
      t60: { label:"3 months (T+60)", p5:42.38, p25:55.61, p50:66.96, p75:80.83, p95:105.78, resolve:"2026-09-23" }
    },
    touch: [ [81.56, 20, 45], [74.77, 46, 66], [71.37, 66, 79], [64.57, 66, 80], [61.17, 44, 67], [54.38, 14, 40] ],
    levels: { res:[75.0, 79.1, 81.3], sup:[64.8, 61.0, 60.0] },
    tech: {
      trend: "Sharp correction inside a longer uptrend — deeply oversold",
      summary: "Price fell hard from its high and now sits below the 20/50/100-day averages but above a rising 200-day. RSI near 19 is deeply oversold — a reading that has marked exhaustion in ABUK's tape before, though it is a timing signal, not a value one.",
      bull: "A daily close back above the 79–81 average cluster would say the correction is spent.",
      bear: "A close below the rising 200-day (~65) opens the recent low near 60."
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
    spot: 46.64,
    spotDate: "close 1 Jul 2026",
    ccy: "EGP",
    fair: { bear: 31.6, base: 54.3, full: 95.3 },
    dist: {
      t20: { label:"1 month (T+20)", p5:38.5, p25:44.5, p50:48.2, p75:52.2, p95:59.7, resolve:"2026-07-29" },
      t60: { label:"3 months (T+60)", p5:35.3, p25:44.7, p50:51.5, p75:59.3, p95:74.4, resolve:"2026-09-23" }
    },
    touch: [ [55, 21, 55], [52, 39, 70], [50, 57, 81], [48, 78, 91], [45, 56, 68], [42, 25, 42] ],
    levels: { res:[48.0, 49.6, 52.0], sup:[46.3, 43.0, 40.0] },
    tech: {
      trend: "Strong bull stack — above all four moving averages",
      summary: "A twelve-month double that has paused just under its 49.60 high: price holds above the 20/50-day shelf at ~46.3 with the 100- and 200-day rising far below. RSI ~51 is neutral after June's consolidation; realized vol ~40% is high for a bank — a crowded, contested EGX leader.",
      bull: "A daily close above ~49.6 opens the EGP 52 zone toward fair value.",
      bear: "A close below the ~46.3 shelf targets the 100-day at 43.0."
    },
    files: {
      study: "files/ADIB_Valuation_Study_03-07-2026_public.docx?v=0703",
      model: "files/ADIB_Valuation_Study_03-07-2026_public.xlsx?v=0703",
      pdf:   "files/ADIB_Valuation_Study_03-07-2026_public.pdf?v=0703"
    }
  },
  HRHO: {
    name: "EFG Holding",
    nameAr: "المجموعة المالية هيرميس القابضة",
    code: "EGX:HRHO",
    spot: 26.83,
    spotDate: "close 1 Jul 2026",
    ccy: "EGP",
    fair: { bear: 23, base: 27.7, full: 33.6 },
    dist: {
      t20: { label:"1 month (T+20)", p5:21.22, p25:24.36, p50:26.65, p75:29.06, p95:32.99, resolve:"2026-07-29" },
      t60: { label:"3 months (T+60)", p5:17.87, p25:22.4, p50:26.1, p75:30.33, p95:37.71, resolve:"2026-09-23" }
    },
    touch: [ [32.2, 11, 33], [29.51, 36, 58], [28.17, 58, 74], [25.49, 60, 78], [24.15, 35, 62], [21.46, 9, 33] ],
    levels: { res:[27.5, 29.0, 30.86], sup:[26.5, 25.0, 24.0] },
    tech: {
      trend: "Tight coil — all four moving averages converged",
      summary: "Price sits fractionally below four moving averages compressed into a two-point band — a textbook coil after a 52-week round trip. RSI ~59 is neutral-firm. No trend to lean on; the tape will follow the next catalyst.",
      bull: "A daily close above ~29 opens the 30.86 high.",
      bear: "A close below ~24 would break the coil lower."
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
    spot: 22.34,
    spotDate: "close 1 Jul 2026",
    ccy: "EGP",
    fair: { bear: 16.7, base: 20.9, full: 29.7 },
    dist: {
      t20: { label:"1 month (T+20)", p5:19.84, p25:21.46, p50:22.53, p75:23.66, p95:25.6, resolve:"2026-07-29" },
      t60: { label:"3 months (T+60)", p5:18.42, p25:21.01, p50:22.91, p75:25.01, p95:28.48, resolve:"2026-09-23" }
    },
    touch: [ [26.81, 2, 18], [24.57, 18, 47], [23.46, 43, 69], [21.22, 33, 55], [20.11, 10, 30], [17.87, 1, 5] ],
    levels: { res:[22.8, 23.1, 24.92], sup:[21.0, 20.0, 19.0] },
    tech: {
      trend: "Tight one-year coil, grinding at its lower edge",
      summary: "Price sits below four flattened moving averages inside a 12-month sideways range, now at its lower edge. RSI ~33 approaches oversold without confirming. Soft but compressed — a low-energy drift awaiting a policy or earnings catalyst.",
      bull: "A daily close back above the ~23 average cluster relieves the pressure.",
      bear: "A close below 21 opens the range floor toward 20."
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
    spot: 29.45,
    spotDate: "close 6 Jul 2026",
    ccy: "EGP",
    fair: { bear: 26, base: 37, full: 51 },      // 6 Jul 2026 — weighted central 37 (+26% vs spot 29.45). Lenses: FCFF DCF 37 (primary), relative multiples 39, normalized earnings 39, FCFE/owner-earnings 32 (floor), asset/reproduction 36. bear/full = weighted bear/bull of the football field. Swing factor: the EGP/USD path and whether booked earnings convert to cash.
    dist: {
      t20: { label:"1 month (T+20)",  p5:24.29, p25:27.76, p50:29.99, p75:32.38, p95:36.98, resolve:"2026-08-03" },
      t60: { label:"3 months (T+60)", p5:21.69, p25:27.07, p50:31.01, p75:35.54, p95:44.37, resolve:"2026-09-28" }
    },
    touch: [ /* descending high -> low */
      [36.8, 8, 32], [33.9, 23, 53], [31.5, 52, 75], [28.9, 70, 80], [26.5, 26, 46], [24.4, 9, 25], [22.1, 2, 11]
    ],
    levels: { res:[29.72, 31.0, 33.0], sup:[27.6, 26.0, 24.4] },
    tech: {
      trend: "Above every major moving average; a firm short-term uptrend, not yet overbought",
      summary: "The tape agrees with the fundamentals' direction for once. The price trades above all four major moving averages (the 20-, 50-, 100- and 200-day cluster between ~26.0 and ~27.6, now support), the daily MACD histogram is positive, and RSI(14) sits in the low-60s — firm but not yet overbought. The structure is a steady grind higher off the ~22 area, with the 52-week high at 29.72 the immediate overhead level; the last session closed up 3.7% on above-average volume. Realized 252-day volatility near 30% is moderate and calmer than the stock's multi-year history.",
      bull: "A daily close above the 29.72 fifty-two-week high would open room toward the 31–34 normalized/DCF cluster; it needs a weaker pound feeding export margins to sustain.",
      bear: "A daily close back below the 27.6 moving-average support reopens the 26.0 (200-day) and 24.4 levels."
    },
    files: {
      study: "files/LCSW_Valuation_Study_06-07-2026_public.docx?v=0706",
      model: "files/LCSW_Valuation_Model_06-07-2026_public.xlsx?v=0706",
      pdf:   "files/LCSW_Valuation_Study_06-07-2026_public.pdf?v=0706"
    }
  },
  PHDC: {
    name: "Palm Hills Developments",
    nameAr: "بالم هيلز للتعمير",
    code: "EGX:PHDC",
    spot: 14.50,
    spotDate: "close 11 Jun 2026",
    ccy: "EGP",
    fair: { bear: 7.62, base: 15.89, full: 24.92 },          // 9 Jun 2026 valuation — unchanged in the 11 Jun price refresh
    dist: {
      t20: { label:"1 month (T+20)",   p5:11.53, p25:13.42, p50:14.92, p75:16.56, p95:19.32, resolve:"2026-07-09" },
      t60: { label:"3 months (T+60)",  p5:10.18, p25:13.22, p50:15.83, p75:18.95, p95:24.50, resolve:"2026-09-03" }
    },
    touch: [ /* level, P(touch) T+20 %, T+60 % — descending */
      [20.00, 5, 30], [18.50, 12, 44], [17.50, 23, 55], [16.50, 40, 68], [15.55, 62, 81]
    ],
    levels: { res:[16.08, 15.70, 15.00], sup:[14.49, 14.06, 13.90] },
    tech: {
      trend: "Correcting inside a longer uptrend",
      summary: "The price pulled back from its recent high and is now testing a rising floor. Momentum has cooled and the daily MACD is still negative, so the dip isn't over yet — but the bigger uptrend is intact, and the selling has come on fading volume rather than heavy panic.",
      bull: "A daily close back above 15.00 would say the dip is done.",
      bear: "A close below 13.90 would break the rising structure and open the door to 13.40."
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
    spot: 96.80,
    spotDate: "close 17 Jun 2026",
    ccy: "EGP",
    fair: { bear: 83.6, base: 147.12, full: 189.6 },          // 9 Jun 2026 valuation — unchanged in the 17 Jun price refresh
    dist: {
      t20: { label:"1 month (T+20)",  p5:82.37, p25:92.24, p50:99.46,  p75:107.34, p95:120.63, resolve:"2026-07-16" },
      t60: { label:"3 months (T+60)", p5:76.47, p25:92.27, p50:105.14, p75:119.80, p95:144.42, resolve:"2026-09-10" }
    },
    touch: [ /* descending high → low */
      [126, 3, 27], [118, 10, 42], [110, 28, 61], [100, 73, 88], [88, 25, 44], [83, 9, 26]
    ],
    levels: { res:[101.40, 99.27, 97.40], sup:[95.26, 92.78, 86.56] },
    tech: {
      trend: "Recovering — pullback held the 50-day, bounce extended on heavy volume",
      summary: "The pullback off the recent high held at the rising 50-day average and the recovery has extended on the heaviest volume in the sample, reclaiming the 20-day average and tagging a new intraday high. Momentum has turned back up (RSI back above its moving average, the daily MACD histogram narrowing) — a correction resolving back upward inside an intact uptrend.",
      bull: "A daily close above the 97.4–98.0 swing-high cluster confirms the resumption toward 100–101.4.",
      bear: "A close below the 92.78 fifty-day reopens the lower supports at 88 and 83."
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
    spot: 12.44,
    spotDate: "close 17 Jun 2026",
    ccy: "EGP",
    fair: { bear: 13.71, base: 19.84, full: 23.43 },          // 17 Jun 2026 valuation — SOTP/RNAV risk-adjusted base; full execution 23.43; four-method synthesis ~19.5
    dist: {
      t20: { label:"1 month (T+20)",  p5:10.50, p25:11.80, p50:12.75, p75:13.78, p95:15.46, resolve:"2026-07-16" },
      t60: { label:"3 months (T+60)", p5:9.64,  p25:11.71, p50:13.39, p75:15.29, p95:18.47, resolve:"2026-09-13" }
    },
    touch: [ /* descending high → low */
      [17.00, 1, 18], [16.00, 4, 28], [15.00, 12, 44], [14.00, 31, 63], [13.00, 67, 84]
    ],
    levels: { res:[15.00, 13.00, 12.50], sup:[11.40, 10.62, 9.82] },
    tech: {
      trend: "Strong uptrend, stretched at resistance",
      summary: "The price closed 12.44 just under the 12.50 period high after a ~40% run, riding above a rising stack of moving averages (20- above 50- above 150-day). Momentum is firm but extended — RSI(14) is ~64 on Wilder's method, approaching but not at the 70 overbought line — on a thin ~11% float that amplifies moves both ways.",
      bull: "A daily close above 12.50 confirms continuation into blue-sky territory.",
      bear: "A rejection at 12.50 with RSI rolling over opens a mean-reversion pullback toward the 11.4–10.6 moving-average supports."
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
    spot: 22.80,
    spotDate: "close 23 Jun 2026",
    ccy: "EGP",
    fair: { bear: 16.72, base: 26.43, full: 30.77 },          // 24 Jun 2026 valuation — SOTP/RNAV risk-adjusted base; full execution 30.77; four-method synthesis ~27.7
    dist: {
      t20: { label:"1 month (T+20)",  p5:18.31, p25:21.08, p50:23.21, p75:25.56, p95:29.35, resolve:"2026-07-21" },
      t60: { label:"3 months (T+60)", p5:16.08, p25:20.38, p50:24.03, p75:28.30, p95:35.79, resolve:"2026-09-22" }
    },
    touch: [ /* descending high -> low */
      [30.00, 5, 30], [28.00, 14, 44], [27.00, 22, 52], [25.00, 48, 72], [24.00, 66, 82], [19.50, 19, 41]
    ],
    levels: { res:[27.00, 24.00, 23.14], sup:[21.46, 21.30, 19.50] },
    tech: {
      trend: "Strong uptrend, stretched near the 52-week high",
      summary: "The price closed 22.80 just under the 23.14 period high after a ~28% three-month run, riding above a rising stack of moving averages (20- above 50- above 150- above 200-day, all rising). Momentum is firm but extended — RSI(14) is ~62, approaching but short of the 70 overbought line — on a thin ~14.5% float that amplifies moves both ways.",
      bull: "A daily close that holds above the 23.14 period high opens blue-sky continuation toward the 24–27 zone.",
      bear: "A rejection here with RSI rolling over risks a mean-reversion pullback toward the 21.5–21.3 moving-average supports."
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
    spot: 39.30,
    spotDate: "close 24 Jun 2026",
    ccy: "EGP",
    fair: { bear: 22.5, base: 53.79, full: 70.52 },          // 24 Jun 2026 valuation — SOTP/RNAV risk-adjusted base; full execution 70.52; four-method synthesis ~55.8
    dist: {
      t20: { label:"1 month (T+20)",  p5:32.54, p25:36.93, p50:40.22, p75:43.82, p95:49.64, resolve:"2026-07-21" },
      t60: { label:"3 months (T+60)", p5:29.42, p25:36.38, p50:42.10, p75:48.74, p95:59.97, resolve:"2026-09-22" }
    },
    touch: [ /* descending high -> low */
      [50.00, 7, 34], [48.00, 12, 43], [46.00, 22, 54], [44.00, 37, 66], [42.00, 57, 78], [33.60, 13, 33]
    ],
    levels: { res:[46.00, 42.00, 39.60], sup:[37.73, 33.59, 26.54] },
    tech: {
      trend: "Strong uptrend, pinned at the all-time high",
      summary: "The price closed 39.30 a whisker below its 39.60 all-time high, riding above a rising, correctly-stacked set of moving averages (SMA-50 above SMA-200, both rising) — the signature of a strong, intact uptrend. Momentum is firm but extended — RSI(14) is ~65 on Wilder's method, elevated but short of the 70 overbought line — and above the all-time high is blue-sky territory with no overhead supply.",
      bull: "A daily close that clears the 39.60 all-time high opens blue-sky continuation toward the 42 round level and the 42–46 re-rating zone.",
      bear: "A rejection here with RSI rolling over risks a pullback toward the 37.73 (SMA-20) support; below it the 33.6 structure level opens."
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
    spot: 129.25,
    spotDate: "close 29 Jun 2026",
    ccy: "EGP",
    fair: { bear: 90.86, base: 123.30, full: 169.70 },          // 29 Jun 2026 — justified-P/B / residual-income primary; weighted central 123.3 (-5% vs spot); bear = excess-return DCF (spread fades without capital return) 90.9; full = RI bull 169.7. Deeper RI-bear ~53.5 (ROE≈CoE) covered in the study text.
    dist: {
      t20: { label:"1 month (T+20)",  p5:103.44, p25:117.89, p50:128.87, p75:140.85, p95:159.92, resolve:"2026-07-27" },
      t60: { label:"3 months (T+60)", p5:87.93,  p25:109.91, p50:127.83, p75:148.88, p95:185.40, resolve:"2026-09-21" }
    },
    touch: [ /* descending high -> low */
      [150.00, 20, 45], [140.00, 45, 65], [135.00, 63, 78], [120.00, 49, 70], [110.00, 18, 45], [100.00, 5, 24]
    ],
    levels: { res:[135.15, 132.82, 129.50], sup:[120.00, 116.04, 110.00] },
    tech: {
      trend: "Consolidating below the moving-average stack, above a rising 200-day",
      summary: "The price closed 129.25 below a falling 20-day (132.8) and 50-day (135.2) but well above a rising 200-day (116.0) — a pullback inside a longer uptrend rather than a breakdown. Momentum is neutral: RSI(14) is ~48 and the daily ATR near 2.2 (~1.7%) points to an orderly tape. The whole equity case rests on the spread between a ~30% return on equity and a ~24% cost of equity, not on the chart.",
      bull: "A daily close back above the 132.8\u2013135.2 moving-average cluster would say the pullback is over and reopen the highs.",
      bear: "A close below the 120 round level and the rising 200-day near 116 would break the structure and open the 110 zone."
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
    spot: 339500,
    spotDate: "close 26 Jun 2026",
    ccy: "KRW",
    fair: { bear: 214800, base: 296502, full: 410754 },      // 26 Jun 2026 — weighted central 296,502 (-13% vs spot); bear = consolidated DCF cross-check 214,800; full = supercycle/bull 410,754. Deeper SOTP cycle-reversion bear ~95,000 covered in the study text.
    dist: {
      t20: { label:"1 month (T+20)",  p5:277676, p25:316898, p50:346091, p75:378203, p95:430413, resolve:"2026-07-24" },
      t60: { label:"3 months (T+60)", p5:246827, p25:308298, p50:359482, p75:418176, p95:520627, resolve:"2026-09-18" }
    },
    touch: [ /* descending high -> low */
      [440000, 5, 30], [400000, 21, 51], [360000, 61, 80], [286000, 12, 33], [250000, 1, 11]
    ],
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
    spot: 33150,
    spotDate: "close 26 Jun 2026",
    ccy: "KRW",
    fair: { bear: 24517, base: 34258, full: 46401 },      // 28 Jun 2026 — weighted central 34,258 (+3% vs spot); bear = consolidated DCF 24,517 (excludes stakes, conservative floor); full = discount-compression / SOTP bull 46,401. Gross net-asset value ~51,788 at no discount; deeper SOTP bear ~21,745 at a wide discount, covered in the study text.
    dist: {
      t20: { label:"1 month (T+20)",  p5:25404, p25:29799, p50:33294, p75:37199, p95:43634, resolve:"2026-07-24" },
      t60: { label:"3 months (T+60)", p5:21022, p25:27714, p50:33584, p75:40697, p95:53651, resolve:"2026-09-18" }
    },
    touch: [ /* descending high -> low */
      [44000, 7, 30], [40000, 21, 48], [37000, 43, 66], [32000, 72, 83], [28000, 24, 49], [24000, 3, 21]
    ],
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
    spot: 331500,
    spotDate: "close 26 Jun 2026",
    ccy: "KRW",
    fair: { bear: 150000, base: 248000, full: 415000 },      // 28 Jun 2026 — weighted central 248,000 (-25% vs spot); bear = AMPC-cut / EV-weak 150,000; full = recovery / ESS-AI supercycle 415,000. Going-concern DCF parent floor ~146,000 covered in the study text.
    dist: {
      t20: { label:"1 month (T+20)",  p5:268200, p25:304400, p50:332400, p75:363000, p95:411900, resolve:"2026-07-24" },
      t60: { label:"3 months (T+60)", p5:230500, p25:286900, p50:334200, p75:389200, p95:484500, resolve:"2026-09-18" }
    },
    touch: [ /* descending high -> low */
      [450000, 2, 16], [410000, 8, 32], [370000, 33, 59], [300000, 35, 59], [270000, 9, 31], [240000, 1, 13]
    ],
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
    spot: 352.20,
    spotDate: "close 30 Jun 2026",
    ccy: "INR",
    fair: { bear: 236, base: 378, full: 579 },      // 30 Jun 2026 — weighted central 378 (+7% vs spot 352.20). Lenses: SOTP 376, consolidated DCF 376, relative 324 (floor), normalized earnings 416 (ceiling). bear/full = weighted bear/bull of the football field. Swing factor: JLR through-cycle margin and the conglomerate discount.
    dist: {
      t20: { label:"1 month (T+20)",  p5:294, p25:327, p50:353, p75:379, p95:422, resolve:"2026-07-28" },
      t60: { label:"3 months (T+60)", p5:258, p25:310, p50:352, p75:400, p95:481, resolve:"2026-09-22" }
    },
    touch: [ /* descending high -> low */
      [420, 8, 32], [400, 20, 46], [380, 41, 63], [360, 74, 85], [340, 65, 79], [320, 31, 56], [300, 11, 36]
    ],
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
    spot: 1042.20,
    spotDate: "close 6 Jul 2026",
    ccy: "INR",
    fair: { bear: 995, base: 1242, full: 1556 },      // 6 Jul 2026 — weighted central 1,242 (+19% vs spot 1,042.20). Four lenses: intrinsic DCF (primary) 1,143 (floor), owner-earnings / shareholder-yield 1,267, relative multiples 1,284, normalized earnings power 1,368 (ceiling). bear/full = weighted bear/bull of the football field. Swing factor: the GenAI effect on the labour-arbitrage margin — whether Infosys cannibalises its own hours and keeps the margin, or AI deflates pricing faster than it cuts cost. Net-cash (~₹43,000 cr), ~33% ROE, >100% FCF conversion, >₹37,500 cr returned to owners in FY26.
    dist: {
      t20: { label:"1 month (T+20)",  p5:918, p25:998, p50:1047, p75:1099, p95:1193, resolve:"2026-08-03" },
      t60: { label:"3 months (T+60)", p5:845, p25:972, p50:1058, p75:1151, p95:1326, resolve:"2026-09-28" }
    },
    touch: [ /* descending high -> low; P(touch) T+20 %, T+60 % */
      [1250, 3, 17], [1200, 7, 27], [1150, 17, 43], [1100, 40, 65], [1050, 82, 90], [1000, 45, 64], [950, 16, 38], [900, 5, 20]
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
    spot: 8.30,
    spotDate: "close 3 Jul 2026",
    ccy: "AED",
    fair: { bear: 7.95, base: 10.18, full: 11.77 },      // 08 Jul 2026 — weighted central 10.18 (+23% vs spot 8.30). Lenses: split-legs SOTP/RNAV 10.14 (primary), going-concern DCF (exit-multiple terminal) 9.81, relative 9.45, full-execution SOTP 11.29. bear/full = weighted bear/bull of the football field. Swing factors: the development-franchise value beyond backlog and the recurring cap rate. Gross asset value ~11.22/share; the market prices a discount at spot.
    dist: {
      t20: { label:"1 month (T+20)",  p5:7.02, p25:7.86, p50:8.37, p75:8.92, p95:9.91, resolve:"2026-07-31" },
      t60: { label:"3 months (T+60)", p5:6.36, p25:7.60, p50:8.50, p75:9.48, p95:11.29, resolve:"2026-09-25" }
    },
    touch: [ /* descending high -> low */
      [9.9, 8, 30], [9.5, 15, 42], [9.0, 35, 61], [8.6, 61, 79], [8.0, 54, 71], [7.5, 21, 44], [7.0, 8, 24]
    ],
    levels: { res:[8.62, 8.87, 11.80], sup:[8.00, 7.60, 7.03] },
    tech: {
      trend: "Two-sided and mid-recovery; above the short averages, below the long stack",
      summary: "The tape mirrors a name that has round-tripped: after running to AED 11.80 and falling to AED 7.03, price at AED 8.30 sits above the rising 20- and 50-day (about 8.16 and 7.98) but below the 100/150/200-day stack (about 8.62, 8.72, 8.87), which now acts as overhead resistance. Momentum is neutral: RSI(14) near 53.5 and the daily MACD histogram has just rolled marginally negative. Realized 252-day volatility near 34% (about 41% over 60 days) with right-skewed tails means the same energy behind the round-trip can drive sharp two-way moves.",
      bull: "A daily close back above the 8.6–8.9 moving-average stack would signal the recovery is resuming; a push toward the AED 11.80 prior high would need the market to credit more of the development franchise and a firmer recurring cap rate.",
      bear: "A close below the 8.00 shelf, then 7.60, opens the way toward the 7.03 fifty-two-week low."
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
    spot: 12.14,
    spotDate: "close 29 Jun 2026",
    ccy: "AED",
    fair: { bear: 11.08, base: 14.80, full: 18.75 },      // 01 Jul 2026 — weighted central 14.80 (+22% vs spot 12.14). Lenses: RNAV/SOTP 14.12 (primary), going-concern DCF 14.74, relative 15.53, normalized earnings 15.27. bear/full = weighted bear/bull of the football field. Swing factors: the recurring EV/EBITDA multiple and the NAV/conglomerate discount. Gross NAV ~17.6/share; the market prices a ~31% discount at spot.
    dist: {
      t20: { label:"1 month (T+20)",  p5:9.98, p25:11.22, p50:12.18, p75:13.22, p95:14.86, resolve:"2026-07-27" },
      t60: { label:"3 months (T+60)", p5:8.64, p25:10.62, p50:12.24, p75:14.11, p95:17.32, resolve:"2026-09-21" }
    },
    touch: [ /* descending high -> low */
      [15.5, 3, 23], [14.0, 20, 47], [13.0, 49, 70], [11.5, 55, 73], [10.5, 18, 44], [9.5, 3, 21], [8.5, 0, 8]
    ],
    levels: { res:[13.04, 13.53, 17.25], sup:[11.50, 10.50, 10.15] },
    tech: {
      trend: "Consolidating after a ~29% correction; above the short averages, below the long",
      summary: "The tape is the mirror image of the fundamentals — undervalued, but the price has corrected about 29% from its high and is digesting the move. It trades just above the 20- and 50-day (clustered near 11.9–12.0) yet below the 100- and 200-day (about 13.0 and 13.5, overhead) — a post-run consolidation rather than a breakdown. Momentum is neutral-to-improving: RSI(14) is around 51 and the daily MACD histogram has turned slightly positive. Realized 252-day volatility near 36% (about 46% over 60 days) with fat, right-skewed tails means the same energy that drove the slide can produce sharp two-way moves.",
      bull: "A daily close back above the 13.0–13.5 moving-average band would signal the correction is stalling; a push toward the 17.25 prior high would need the NAV discount to start compressing.",
      bear: "A close below the 11.50 shelf, then 10.50, opens the wide-discount zone toward the 10.15 fifty-two-week low."
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
    spot: 4.77,
    spotDate: "close 30 Jun 2026",
    ccy: "EGP",
    fair: { bear: 3.296, base: 5.89, full: 8.601 },      // 30 Jun 2026 — weighted central 5.89 (+23% vs spot); bear = consolidated bottom-up DCF 3.296 (excludes asset marks, conservative floor); full = discount-compression / SOTP bull 8.601. Gross net-asset value ~8.48 at no discount; market prices a ~44% discount, covered in the study text.
    dist: {
      t20: { label:"1 month (T+20)",  p5:3.771, p25:4.36, p50:4.809, p75:5.312, p95:6.126, resolve:"2026-07-28" },
      t60: { label:"3 months (T+60)", p5:3.224, p25:4.126, p50:4.889, p75:5.789, p95:7.391, resolve:"2026-09-22" }
    },
    touch: [ /* descending high -> low */
      [5.7, 20, 47],[5.2, 49, 70],[6.3, 5, 27],[4.5, 57, 74],[4, 17, 41],[3.5, 2, 17]
    ],
    levels: { res:[5.7, 5.2, 4.87], sup:[4.87, 4.5, 4] },
    tech: {
      trend: "Strong uptrend, pulling back to the rising 20- and 50-day",
      summary: "The price is in a strong uptrend taking a sharp breather — up roughly 84% over the past year and only about 16% below its 52-week high, but recently pulled back from EGP 5.70 to sit just under a still-rising 20- and 50-day, with the 200-day far below. Momentum is oversold rather than broken: RSI(14) is ~27, which often precedes a bounce — though a stock that has run this far can still correct further. Realized 60-day volatility near 52% and fat right-skewed tails mean the same energy that drove the run can produce sharp two-way moves.",
      bull: "A reclaim above the 20-day near EGP 5.20 would signal the pullback is stalling; a push toward the EGP 5.70 high would need the holding-company discount to start compressing.",
      bear: "A daily close below the rising 50-day near EGP 4.87, then EGP 4.50, opens the wide-discount zone toward the DCF / stale-marks area near EGP 3.50–4.00."
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
    spot: 1.41,
    spotDate: "close 1 Jul 2026",
    ccy: "EGP",
    fair: { bear: 0.53, base: 0.78, full: 1.70 },           // 03 Jul 2026 study — four-lens weighted central 0.78 (−45% vs spot 1.41). Lenses: holdco NAV 0.81 (primary), consolidated DCF 0.48 (floor), relative P/NAV 0.72, normalized earnings 1.03 (ceiling). bear = weighted bear; full = weighted bull (DPRK cash recovered + OPE at maturity). USD marks at EGP/USD 49.09.
    dist: {
      t20: { label:"1 month (T+20)",  p5:1.18, p25:1.35, p50:1.46, p75:1.58, p95:1.80, resolve:"2026-07-29" },
      t60: { label:"3 months (T+60)", p5:1.09, p25:1.36, p50:1.57, p75:1.80, p95:2.23, resolve:"2026-09-23" }
    },
    touch: [ /* descending high → low; P(touch) T+20 %, T+60 % */
      [1.80, 7, 36], [1.60, 31, 66], [1.50, 59, 83], [1.30, 30, 46], [1.20, 11, 25], [1.10, 4, 12]
    ],
    levels: { res:[1.50, 1.58, 1.60], sup:[1.37, 1.30, 1.20] },
    tech: {
      trend: "Uptrend, consolidating just under the 50-day after a strong run",
      summary: "The tape is the mirror image of the fundamentals: strong, extended and orderly. OIH has advanced ~74% over twelve months and ~22% year-to-date, sits above the 20-, 100- and 200-day averages, and is consolidating a hair under the 50-day (EGP 1.47) after a pullback from the March high of EGP 1.58. RSI(14) near 62 is constructive without being overbought, the daily MACD histogram has just crossed back positive, and turnover of ~51m shares a day marks this as one of the exchange's liquidity bellwethers. Realized 252-day volatility near 42% is high — a retail-flow counter. Nothing in the price structure is broken, which is precisely the tension of this study.",
      bull: "A daily close back above the 50-day near EGP 1.47 reopens the March high at 1.58, then the round 1.60.",
      bear: "A close below the EGP 1.37 twenty-day cluster opens a retracement toward 1.30, then the 1.20 shelf."
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
    spot: 720.00,
    spotDate: "close 30 Jun 2026",
    ccy: "EGP",
    fair: { bear: 740, base: 928, full: 1272 },              // 30 Jun 2026 study — 5-lens weighted central 928 (+29% vs spot 720); bear = normalized-earnings low lens 740; full = SOTP bull 1272. USD fundamentals at USD/EGP 49.2.
    dist: {
      t20: { label:"1 month (T+20)",  p5:575, p25:658, p50:719, p75:785, p95:893,  resolve:"2026-07-28" },
      t60: { label:"3 months (T+60)", p5:488, p25:611, p50:714, p75:834, p95:1040, resolve:"2026-09-22" }
    },
    touch: [ /* descending high → low; P(touch) T+20 %, T+60 % */
      [850, 16, 41], [800, 35, 58], [760, 58, 75], [680, 57, 75], [640, 31, 57], [600, 14, 40]
    ],
    levels: { res:[749, 785, 800], sup:[686, 658, 640] },
    tech: {
      trend: "Uptrend, consolidating below the 20-day after a strong run",
      summary: "Orascom has run roughly eight-fold off its 2021 lows and sits in the upper quartile of its 52-week range. The moving-average stack is bullish — the 20-, 50- and 200-day are in rising order — but spot has slipped just below the 20-day in a near-term pause. Momentum is cooling (the daily MACD histogram is negative) and RSI is neutral near 50 — a healthy consolidation inside an intact uptrend, not a breakdown.",
      bull: "A daily close back above the 749 twenty-day reopens the prior-high zone near 800.",
      bear: "A close below the 686 fifty-day opens a deeper retracement toward 640."
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
    spot: 26.24,
    spotDate: "close 1 Jul 2026",
    ccy: "SAR",
    fair: { bear: 20, base: 25.04, full: 31 },      // 1 Jul 2026 — weighted central 25.04 (−4.6% vs spot 26.24). Lenses: DCF (5-yr FCFF) 23.47, dividend-yield 26.09, relative 21.48 (floor), reserves-NAV 29.63 (ceiling), normalized 23.24. bear/full = weighted bear/bull of the football field. Swing factor: the oil-price path and the base dividend's free-cash coverage.
    dist: {
      t20: { label:"1 month (T+20)",  p5:23.80, p25:25.33, p50:26.23, p75:27.13, p95:28.57, resolve:"2026-07-29" },
      t60: { label:"3 months (T+60)", p5:21.99, p25:24.47, p50:26.12, p75:27.78, p95:30.35, resolve:"2026-09-23" }
    },
    touch: [ /* descending high -> low */
      [30, 1, 11], [29, 4, 22], [28, 15, 40], [27, 47, 67], [25, 27, 54], [24, 9, 31], [23, 3, 16]
    ],
    levels: { res:[27.16, 26.64, 26.24], sup:[25.74, 24.50, 23.13] },
    tech: {
      trend: "Below the 20- and 50-day averages but holding above a rising 200-day; quiet and range-bound",
      summary: "The tape is quiet for a $1.7tn mega-cap. Price sits just under the 20-day (SAR 26.64) and 50-day (SAR 27.16) moving averages but above a rising 200-day line (SAR 25.74) — a mild near-term drift within a longer-term base, not a breakdown. RSI(14) near 31 is approaching, but not yet at, oversold, and price sits mid-range in a tight 52-week band of SAR 23.13–27.96. Realized 252-day volatility of only ~15% is a fraction of a typical single stock; the market is not currently excited in either direction.",
      bull: "A daily close back above the SAR 26.6–27.2 moving-average cluster would signal the near-term soft patch is over; reclaiming the 52-week high near SAR 28 would need an oil re-rating.",
      bear: "A daily close below the rising 200-day at SAR 25.74 opens the lower band toward SAR 24 and the 52-week low at SAR 23.13."
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
    spot: 51.80,
    spotDate: "close 7 Jul 2026",
    ccy: "SAR",
    fair: { bear: 43, base: 55.5, full: 66 },      // 7 Jul 2026 — weighted central 55.5 (+7% vs spot 51.80). Four lenses: DCF (5-yr FCFF, mid-cycle) 60.3 (40%), dividend-yield 56.4 (25%), EV/EBITDA relative 47.8 (20%, floor), P/B asset-replacement 51.5 (15%). bear/full = weighted bear/bull of the football field. Swing factor: the product–feedstock spread in $/t and the timing of the margin-cycle recovery.
    dist: {
      t20: { label:"1 month (T+20)",  p5:45.16, p25:49.46, p50:51.85, p75:54.26, p95:58.79, resolve:"2026-08-04" },
      t60: { label:"3 months (T+60)", p5:41.26, p25:47.42, p50:51.74, p75:56.35, p95:64.22, resolve:"2026-09-29" }
    },
    touch: [ /* descending high -> low */
      [58, 10, 32], [56, 21, 47], [54, 43, 65], [52, 83, 91], [50, 47, 69], [48, 22, 48], [46, 10, 31]
    ],
    levels: { res:[53.56, 56.72, 62.80], sup:[49.74, 47.42, 44.30] },
    tech: {
      trend: "Below all four moving averages after a long slide; oversold-leaning within a wide base",
      summary: "SABIC trades below its 20-, 50-, 100- and 200-day moving averages (SAR 53.56 / 56.72 / 57.12 / 56.95) after a multi-year decline from the 2022 highs, and sits in the lower half of a 52-week SAR 49.74–62.80 band. RSI(14) near 31 is approaching, but not yet at, oversold, and the daily MACD histogram is mildly negative — a weak, below-trend tape rather than a fresh breakdown. Realized 252-day volatility of ~19% is modest for a single stock; the market is priced for a cyclical trough, not a crisis.",
      bull: "A daily close back above the SAR 53.6 twenty-day, then the 56.7–57.1 moving-average cluster, would signal the downtrend is stalling; reclaiming the 52-week high near SAR 63 would need the petrochemical spread to turn.",
      bear: "A daily close below the 52-week low at SAR 49.74 opens the lower band toward SAR 47.4, and in a deeper risk-off toward SAR 44."
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
    spot: 58.80,
    spotDate: "close 5 Jul 2026",
    ccy: "SAR",
    fair: { bear: 27, base: 42, full: 57 },      // 5 Jul 2026 — weighted central 42 (−29% vs spot 58.80). Lenses: SOTP 44 (primary), consolidated DCF (5-yr FCFF) 47, relative 26 (floor), mid-cycle earnings 42. bear/full = weighted bear/bull of the football field. Swing: the commodity deck (DAP/aluminium/gold) and whether the growth capex earns its cost of capital. Note: §3 Monte Carlo showed no CRPS skill vs a random-walk cone (see study Appendix B) — the distribution is an honest probability map, not a skill-validated forecast.
    dist: {
      t20: { label:"1 month (T+20)",  p5:50.7, p25:55.6, p50:59.2, p75:63.1, p95:69.1, resolve:"2026-08-02" },
      t60: { label:"3 months (T+60)", p5:46.1, p25:53.9, p50:60.1, p75:67.1, p95:78.4, resolve:"2026-09-27" }
    },
    touch: [ /* descending high -> low */
      [80, 0, 6], [72, 3, 22], [66, 20, 48], [62, 52, 73], [58, 76, 85], [54, 28, 51], [50, 6, 25], [46, 1, 9]
    ],
    levels: { res:[60.99, 63.22, 66.63], sup:[54.00, 51.10, 46.00] },
    tech: {
      trend: "Below all four major moving averages; corrective, near the lower third of the 52-week range",
      summary: "The tape is weak and stretched to the downside, and for once it agrees with the fundamentals. Price sits below the 20-day (SAR 61.0), 50-day (SAR 63.2), 100-day (SAR 66.6) and 200-day (SAR 65.1) moving averages — a corrective de-rating from the high-70s. RSI(14) near 34 is approaching, but not yet at, oversold; the MACD histogram is negative. Realized 252-day volatility is ~32%, moderately elevated. The trailing-year range is SAR 51.1–79.5, and price sits in its lower third.",
      bull: "A daily close back above the SAR 61–63 moving-average cluster would signal the near-term de-rating is pausing; reclaiming the mid-60s would need a stronger commodity deck.",
      bear: "A sustained close below the SAR 54 shelf opens the trailing-year low near SAR 51 and the lower band toward SAR 46."
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
    spot: 3.44,
    spotDate: "close 3 Jul 2026",
    ccy: "AED",
    fair: { bear: 3.30, base: 3.79, full: 4.60 },      // 4 Jul 2026 — weighted five-lens central 3.79 (+10% vs spot 3.44). Lenses: DCF (5-yr FCFF) 4.50 (ceiling), DDM (committed dividend, split-Ke 8.25%) 3.41, relative EV/EBITDA 3.83, justified P/E 3.62, dividend yield 3.83. bear/full = weighted bear/bull of the football field. Swing: Brent-linked export pricing and the gap between enterprise cash flow and the distributed dividend.
    dist: {
      t20: { label:"1 month (T+20)",  p5:3.05, p25:3.32, p50:3.45, p75:3.59, p95:3.86, resolve:"2026-07-31" },
      t60: { label:"3 months (T+60)", p5:2.83, p25:3.22, p50:3.48, p75:3.75, p95:4.21, resolve:"2026-09-25" }
    },
    touch: [ /* descending high -> low; P(touch) T+20 %, T+60 % */
      [3.90, 5, 25], [3.75, 14, 40], [3.65, 27, 55], [3.55, 49, 71], [3.35, 49, 68], [3.25, 25, 49], [3.15, 13, 34]
    ],
    levels: { res:[3.55, 3.65, 3.72], sup:[3.34, 3.25, 3.14] },
    tech: {
      trend: "Flat and range-bound, sitting on its 20- and 200-day averages",
      summary: "The tape is quiet, as befits a low-beta income name. Price (AED 3.44) sits almost exactly on its 20-day (3.42) and 200-day (3.42) moving averages and just above the 50-day (3.34) — a flat, coiled structure with no trend. RSI(14) near 56 is neutral; MACD is marginally positive on the line with the histogram just below zero, i.e. momentum flat-to-fading. The 52-week range is narrow (3.14–3.72) and realized volatility of ~17% is a fraction of a typical single stock.",
      bull: "A daily close above the 3.55–3.65 shelf opens the way toward the 3.72 fifty-two-week high; a re-rating would need a firmer oil/gas tape.",
      bear: "A close below the 3.35 support opens 3.25, then the 3.14 fifty-two-week low."
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
    spot: 66.00,
    spotDate: "close 2 Jul 2026",
    ccy: "SAR",
    fair: { bear: 58, base: 70, full: 80 },      // 2 Jul 2026 — weighted central 70.1 (+6.2% vs spot 66.00). Lenses: DDM (primary) 58.2, residual income 76.8, FCFE (DCF) 79.5, justified P/B 75.7, normalized 65.3. bear/full = weighted bear/bull of the football field. Swing factors: the NIM path through the SAMA easing cycle and whether retained capital (~23% ROE) is valued on the dividend or the excess return.
    dist: {
      t20: { label:"1 month (T+20)",  p5:58.70, p25:63.53, p50:66.08, p75:68.62, p95:73.15, resolve:"2026-07-30" },
      t60: { label:"3 months (T+60)", p5:54.27, p25:61.32, p50:65.95, p75:70.75, p95:78.70, resolve:"2026-09-24" }
    },
    touch: [ /* descending high -> low */
      [74, 6, 24], [72, 12, 35], [70, 24, 50], [68, 49, 70], [64, 46, 67], [62, 23, 48], [60, 12, 33]
    ],
    levels: { res:[67.92, 67.39, 66.66], sup:[64.50, 62.00, 60.67] },
    tech: {
      trend: "Below all four major moving averages but only mildly; RSI in the low-40s — a soft, corrective tape, not a breakdown",
      summary: "The tape is soft, not washed out. Al Rajhi sits below its 20-day (SAR 66.66), 50-day (67.39), 100-day (68.55) and 200-day (67.92) averages, about 2.8% under the 200-day — a mild drift lower after the post-bonus consolidation. RSI(14) near 41 is neutral-to-weak but not oversold, and MACD is modestly negative with the histogram below zero. Price sits at the 42nd percentile of a tight 52-week band of SAR 60.67–73.33; realized 252-day volatility near 20% is calm for a single name, and the YZ-HAR engine reads the current regime tighter still at ~17.8%.",
      bull: "A daily close back above the SAR 66.7–68.0 moving-average cluster would signal the soft patch is over; reclaiming the 52-week high near SAR 73 would need a margin-resilience or dividend surprise.",
      bear: "A daily close below recent support around SAR 64.5 opens the lower band toward SAR 62 and the 52-week low at SAR 60.67."
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
    spot: 43.58,
    spotDate: "close 07 Jul 2026",
    ccy: "SAR",
    fair: { bear: 36.2, base: 47.11, full: 59.1 },      // 09 Jul 2026 — weighted central 47.11 (+8.1% vs spot 43.58). Four lenses: FCFF DCF (primary, 35%) 50.12, DDM (25%) 45.88, relative EV/EBITDA (20%) 47.21, normalized earnings power (20%) 43.29. bear/full = weighted bear/bull of the football field. Swing factors: 5G/FTTH capex intensity vs. the dividend-cover math (FCF/dividend ~0.93x at the base FY26E 16.5%-of-revenue capex plan, tightening to ~0.86x at the top of guidance), the KSA consumer (CBU) ARPU/data-monetization path, and whether the international-subsidiary drag keeps fading.
    dist: {
      t20: { label:"1 month (T+20)",  p5:40.79, p25:42.61, p50:43.69, p75:44.80, p95:46.81, resolve:"2026-08-04" },
      t60: { label:"3 months (T+60)", p5:39.00, p25:42.03, p50:43.91, p75:45.85, p95:49.51, resolve:"2026-09-29" }
    },
    touch: [ /* descending high -> low; P(touch) T+20 %, T+60 % */
      [50.00, 1, 7], [48.00, 3, 16], [46.00, 15, 41], [44.00, 71, 85], [42.00, 26, 48], [40.00, 4, 16], [38.00, 1, 5], [36.00, 0, 2]
    ],
    levels: { res:[43.93, 44.88, 45.38], sup:[43.30, 42.46, 40.20] },
    tech: {
      trend: "Tightly bunched moving-average stack just below the 20-day — a quiet, consolidating tape after a slow multi-month grind higher; RSI near neutral",
      summary: "The tape is unusually quiet. stc sits at SAR 43.58, just below its 20-day average (43.93) but above its 50-day (43.56), 200-day (43.41) and 100-day (43.25) — the four averages sit within about SAR 0.7 of each other, a classic low-volatility coil. RSI(14) at ~48 is neutral, and the MACD histogram is mildly negative (-0.086) on a soft bearish cross, consistent with the 20-day change (-1.3%) fading a 60-day gain (+3.8%). Realized 252-day volatility of ~13% is low even by telecom standards — among the calmest names on the site. Price sits in the upper-middle of a 52-week band of SAR 40.20-45.38.",
      bull: "A daily close back above the SAR 43.93 twenty-day average would reopen the SAR 44.88 recent swing high (17 Jun), then the SAR 45.38 fifty-two-week high.",
      bear: "A daily close below the SAR 43.30 recent higher-low (7 Jun) opens the SAR 42.46 April low; beneath it the fifty-two-week low at SAR 40.20 comes into view."
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
    spot: 20.23,
    spotDate: "close 07 Jul 2026",
    ccy: "SAR",
    fair: { bear: 20.85, base: 26.61, full: 33.24 },      // 09 Jul 2026 — weighted central 26.61 (+31.5% vs spot 20.23). Lenses: DDM (primary, 30%) 23.62, residual income (multi-period build, 20%) 33.24, FCFE (equity DCF, 15%) 32.18, relative multiples (20%) 24.62, normalized earnings power (15%) 20.85. bear/full = normalized floor / residual-income ceiling. Swing factors: the NIM path through the SAMA/Fed easing cycle and whether Riyad Bank's ~16% ROE persists (excess-return lenses) or fades toward the ~10.3% cost of equity (the market's implied ~1.2x book read).
    dist: {
      t20: { label:"1 month (T+20)",  p5:18.27, p25:19.49, p50:20.22, p75:20.99, p95:22.43, resolve:"2026-08-04" },
      t60: { label:"3 months (T+60)", p5:16.95, p25:18.97, p50:20.22, p75:21.57, p95:24.19, resolve:"2026-09-29" }
    },
    touch: [ /* descending high -> low */
      [23.26, 3, 15], [22.25, 10, 29], [21.24, 32, 55], [19.22, 30, 54], [18.21, 8, 25], [17.20, 2, 11]
    ],
    levels: { res:[20.99, 20.59, 20.49], sup:[19.49, 19.14, 18.21] },
    tech: {
      trend: "Below all four major moving averages; RSI in the high-20s (oversold) — a soft, range-bound tape, not a breakdown",
      summary: "The tape is soft and oversold, not washed out. Riyad Bank sits below its 20-day (SAR 20.49), 50-day (20.59), 100-day (20.99) and 200-day (20.54) averages. RSI(14) near 27 is oversold (sub-30), and MACD is mildly negative with the histogram below zero. Price sits in the lower third of a tight 52-week band of SAR 19.14-22.35; realized 60-day volatility near 16% is calm for a single name, and the YZ-HAR engine reads the current regime at ~23%.",
      bull: "A daily close back above the SAR 20.5-21.0 moving-average cluster would signal the soft patch is over; reclaiming the 52-week high near SAR 22.35 would need a margin-resilience or dividend surprise.",
      bear: "A daily close below recent support around SAR 19.5 opens the lower band toward the 52-week low at SAR 19.14."
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
    spot: 38.96,
    spotDate: "close 2 Jul 2026",
    ccy: "SAR",
    fair: { bear: 36, base: 45, full: 55 },      // 2 Jul 2026 — weighted central 45.3 (+16% vs spot 38.96). Lenses: DDM (primary) 44.2, DCF (FCFF) 44.9, relative P/E-and-P/B 46.1, justified P/B (sustainable ROE) 46.9. bear/full = weighted bear/bull of the football field. Swing factor: the net interest margin through the SAMA easing cycle (a 74%-fixed investment book repricing slowly) and the Turkiye / legacy international drag.
    dist: {
      t20: { label:"1 month (T+20)",  p5:33.75, p25:37.10, p50:39.03, p75:40.93, p95:44.44, resolve:"2026-07-30" },
      t60: { label:"3 months (T+60)", p5:30.81, p25:35.62, p50:39.00, p75:42.56, p95:48.66, resolve:"2026-09-24" }
    },
    touch: [ /* descending high -> low; P(touch) T+20 %, T+60 % */
      [46, 3, 18], [44, 9, 31], [42, 24, 50], [40, 59, 76], [38, 57, 75], [36, 23, 48], [34, 8, 27]
    ],
    levels: { res:[39.76, 40.21, 41.01], sup:[38.00, 36.00, 33.68] },
    tech: {
      trend: "Below all four major moving averages but only mildly; RSI in the low-40s — a soft, corrective tape, not a breakdown",
      summary: "The tape is mildly soft rather than distressed. SNB sits below its 20-day (SAR 40.21), 50-day (39.76), 100-day (41.01) and 200-day (39.76) averages, about 2% under the 200-day. RSI(14) near 41 is neutral-to-weak but not oversold, and MACD is modestly negative (-0.22 line / +0.03 signal / -0.25 histogram). Price sits in the lower-middle of a 52-week band of SAR 33.68-45.00; realized 252-day volatility near 24% is moderate for a large-cap bank, and the YZ-HAR engine reads the current 60-day regime near 21%.",
      bull: "A daily close back above the SAR 39.8-41.0 moving-average cluster would signal the soft patch is over; reclaiming the 52-week high near SAR 45 would need a margin-resilience or dividend surprise.",
      bear: "A daily close below support around SAR 38 opens the lower band toward SAR 36 and the 52-week low at SAR 33.68."
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
    spot: 30.64,
    spotDate: "close 3 Jul 2026",
    ccy: "AED",
    fair: { bear: 25, base: 32.3, full: 43.2 },      // 3 Jul 2026 — weighted central 32.3 (+5.4% vs spot 30.64). Lenses: DDM/residual income (primary) 32.9, FCFE (DCF) 31.1, relative P/TBV-and-P/E 33.4, normalized through-cycle 31.4. bear/full = weighted bear/bull of the football field. Swing factors: sustainable ROTE as the Fed/CBUAE ease the pegged dirham (NIM 3.46% off a 4.0% peak, CASA-cushioned) and the through-cycle cost of risk normalising off a ~0.2% recovery-flattered trough.
    dist: {
      t20: { label:"1 month (T+20)",  p5:23.69, p25:28.14, p50:31.04, p75:34.23, p95:40.59, resolve:"2026-07-31" },
      t60: { label:"3 months (T+60)", p5:22.31, p25:27.97, p50:31.81, p75:36.15, p95:45.24, resolve:"2026-09-25" }
    },
    touch: [ /* descending high -> low; P(touch) T+20 %, T+60 % */
      [37, 20, 35], [35, 33, 49], [33, 55, 68], [31, 82, 88], [30, 74, 79], [29, 58, 66], [27, 31, 42]
    ],
    levels: { res:[31.30, 33.00, 35.00], sup:[29.52, 28.72, 22.80] },
    tech: {
      trend: "Above all four major moving averages; RSI in the high-50s, MACD mildly positive — a constructive, trending tape",
      summary: "The tape is constructive and aligned with the fundamentals for once. Emirates NBD trades above its 20-day (AED 29.52), 50-day (28.96), 100-day (30.10) and 200-day (28.72) averages, with the rising 200-day as the visible trend floor. RSI(14) near 58 is neutral-to-firm — not overbought — and MACD is mildly positive (+0.55 line / +0.53 signal / +0.01 histogram). Price sits in the upper-middle of a wide 52-week band of AED 22.80-37.00; realized 252-day volatility near 38% is elevated after a turbulent first half of 2026 (a genuine ~10% single session in April), and the YZ-HAR engine reads the current 60-day regime wider still at ~45%.",
      bull: "A daily close above the AED 33 shelf toward the AED 35 prior resistance would extend the uptrend; reclaiming the AED 37 fifty-two-week high would need a margin-resilience or dividend/RBL surprise.",
      bear: "A daily close below the AED 29.5 moving-average cluster opens the AED 28.7 two-hundred-day and, beneath it, the wide gap toward the AED 22.80 fifty-two-week low."
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
      t20: { label:"1 month (T+20)",  p5:15.35, p25:16.74, p50:17.48, p75:18.19, p95:19.55, resolve:"2026-08-02" },
      t60: { label:"3 months (T+60)", p5:13.96, p25:15.91, p50:17.24, p75:18.60, p95:20.91, resolve:"2026-09-27" }
    },
    touch: [ /* descending high -> low; P(touch) T+20 %, T+60 % */
      [19.5, 8, 26], [19.0, 15, 36], [18.5, 28, 50], [18.0, 51, 69], [17.0, 49, 72], [16.5, 28, 56], [15.5, 8, 30]
    ],
    levels: { res:[17.67, 18.05, 18.43], sup:[17.00, 16.68, 15.50] },
    tech: {
      trend: "Below all four major moving averages; RSI in the high-30s, MACD below signal — a soft, range-bound tape",
      summary: "The tape is soft and range-bound rather than distressed. QNB trades below its 20-day (QAR 17.67), 50-day (17.62), 100-day (18.05) and 200-day (18.43) averages, a slow post-peak drift. RSI(14) near 38 is weak but not oversold, and MACD is mildly negative (-0.01 line / +0.03 signal / -0.04 histogram). Price sits in the lower half of a 52-week band of QAR 16.68-20.40; realized 252-day volatility near 20% is moderate for a large-cap bank, and the YZ-HAR engine reads the current 60-day regime a touch tighter at ~18%.",
      bull: "A daily close back above the QAR 18.05-18.43 moving-average cluster would neutralise the downtrend; reclaiming the QAR 19.5 shelf toward the QAR 20.40 fifty-two-week high would need a capital-return or NIM-resilience surprise.",
      bear: "A daily close below QAR 17.00 opens the QAR 16.68 fifty-two-week low; beneath it the distribution thins toward the QAR 15.5 stress zone."
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
    spot: 4.319,
    spotDate: "close 5 Jul 2026",
    ccy: "QAR",
    fair: { bear: 2.71, base: 4.29, full: 6.40 },      // 5 Jul 2026 \u2014 weighted central 4.29 (\u22120.7% vs spot 4.319). Four lenses: DCF on the contracted fleet (primary) 4.90, two-stage dividend-discount 3.56, relative EV/EBITDA & P/E 4.00, fleet-replacement NAV 4.06; blend 40/20/15/25. bear/full = weighted bear/bull of the football field. Swing factor: the discount rate on a bond-like ~20-year QatarEnergy charter stream (\u22487.5% base) and how much credit the newbuild programme (69\u2192112 vessels, first delivery end-2026) earns above its cost of capital. Note: the \u00a73 Monte-Carlo engine ties \u2014 does not beat \u2014 its random-walk benchmark for this unusually stable name (Appendix B), so the price map is illustrative only.
    dist: {
      t20: { label:"1 month (T+20)",  p5:3.86, p25:4.16, p50:4.34, p75:4.54, p95:4.88, resolve:"2026-08-02" },
      t60: { label:"3 months (T+60)", p5:3.60, p25:4.08, p50:4.40, p75:4.74, p95:5.36, resolve:"2026-09-27" }
    },
    touch: [ /* descending high -> low; P(touch) T+20 %, T+60 % */
      [4.90, 7, 28], [4.70, 18, 45], [4.55, 37, 63], [4.40, 68, 83], [4.20, 52, 69], [4.05, 24, 45], [3.90, 10, 28]
    ],
    levels: { res:[4.42, 4.50, 4.70], sup:[4.20, 4.05, 4.03] },
    tech: {
      trend: "Just below a tightly-clustered moving-average stack; RSI near 49, MACD marginally below signal \u2014 a flat, range-bound tape",
      summary: "The tape is quiet and balanced rather than trending. QGTS trades just below its 20-day (QAR 4.32) and 50-day (4.33) averages and further below the 100-day (4.42) and 200-day (4.50) \u2014 a mild post-peak drift. RSI(14) near 49 is neutral, and MACD is marginally negative (-0.002 line / +0.007 signal / -0.009 histogram). Price sits mid-range in a 52-week band of QAR 4.03-4.97; realized 252-day volatility near 23% is low for a shipping name, and the YZ-HAR engine reads the current 60-day regime at a similar ~23%.",
      bull: "A daily close back above the QAR 4.42-4.50 moving-average cluster would neutralise the mild downtrend; reclaiming the QAR 4.70 shelf toward the QAR 4.97 fifty-two-week high would need rate relief or a charter-extension surprise.",
      bear: "A daily close below QAR 4.20 opens the QAR 4.05 income-lens floor; beneath it the distribution thins toward the QAR 4.03 fifty-two-week low."
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
    spot: 17.40,
    spotDate: "close 3 Jul 2026",
    ccy: "AED",
    fair: { bear: 17.1, base: 19.9, full: 22.4 },      // 3 Jul 2026 — weighted central 19.9 (+14% vs spot 17.40). Lenses: DDM (primary) 19.81, FCFE-DCF 20.70, relative P/B-ROE & peer P/E 18.78, normalized ROTE 19.90. bear/full = weighted bear/bull of the football field. Swing factor: the NIM through the Fed easing cycle (imported via the AED-USD peg) and the normalization of a benign ~49bps cost of risk.
    dist: {
      t20: { label:"1 month (T+20)",  p5:14.97, p25:16.44, p50:17.32, p75:18.18, p95:19.75, resolve:"2026-07-31" },
      t60: { label:"3 months (T+60)", p5:13.37, p25:15.53, p50:17.05, p75:18.59, p95:21.45, resolve:"2026-09-25" }
    },
    touch: [ /* descending high -> low; P(touch) T+20 %, T+60 % */
      [20, 6, 22], [19, 18, 40], [18.5, 30, 52], [18, 51, 68], [17, 64, 81], [16, 24, 52], [15, 8, 29]
    ],
    levels: { res:[17.52, 18.00, 20.70], sup:[17.00, 16.50, 15.48] },
    tech: {
      trend: "Neutral and balanced — on its 20-, 50- and 200-day averages, below the 100-day; RSI near 49, a consolidation not a breakdown",
      summary: "The tape is neutral and balanced. FAB sits essentially on its 20-day (AED 17.33), 50-day (17.34) and 200-day (17.52) averages and just below its 100-day (18.00). RSI(14) near 49 is mid-range, and MACD is marginally negative (0.04 line / 0.06 signal / -0.03 histogram). Price sits in the middle of a 52-week band of AED 15.48-20.70; realized 252-day volatility near 29% is moderate for a large-cap bank, and the YZ-HAR engine reads the current 60-day regime near 24%.",
      bull: "A daily close above the AED 18.00 hundred-day and the AED 18.5 shelf would signal the consolidation is resolving up; reclaiming the 52-week high near AED 20.70 would need a margin-resilience or dividend surprise.",
      bear: "A daily close below support around AED 17.00 opens the lower band toward AED 16.00 and the 52-week low at AED 15.48."
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
    spot: 193.90,
    spotDate: "close 5 Jul 2026",
    ccy: "SAR",
    fair: { bear: 129, base: 195, full: 299 },      // 5 Jul 2026 — weighted central 195.3 (+0.7% vs spot 193.90). Lenses: SOTP/NAV (primary) 215.3, consolidated DCF (normalized attributable FCFF) 184.2, relative P/E-P/B-EV/EBITDA blend 158.1, pipeline-maturation earnings 197.1. bear/full = weighted bear/bull of the football field. Swing factor: whether Vision-2030 growth capital earns above its cost (ROIC vs Ke) as the SAR 100bn-plus under-construction book reaches commercial operation.
    dist: {
      t20: { label:"1 month (T+20)",  p5:158.5, p25:180.4, p50:194.1, p75:208.7, p95:235.2, resolve:"2026-08-02" },
      t60: { label:"3 months (T+60)", p5:136.9, p25:171.0, p50:194.2, p75:220.0, p95:268.4, resolve:"2026-09-27" }
    },
    touch: [ /* descending high -> low; P(touch) T+20 %, T+60 % */
      [250, 5, 19], [230, 13, 34], [210, 30, 52], [195, 49, 66], [180, 63, 74], [165, 32, 52], [150, 14, 35]
    ],
    levels: { res:[197.30, 210.00, 235.00], sup:[191.20, 185.50, 179.40] },
    tech: {
      trend: "Consolidating on the 200-day; above the 50/100-day, just below the 20-day — a balanced, base-building tape after the bounce off the SAR 157 low",
      summary: "The tape is neutral and consolidating. ACWA trades right on its 200-day average (SAR 191), above the 50-day (185.5) and 100-day (179.4) but just below the 20-day (197.3). RSI(14) near 51 sits at the midline, and MACD is mildly negative (2.15 line / 3.46 signal / -1.31 histogram) — momentum cooling after a bounce. Price sits in the lower-middle of a 52-week band of SAR 156.6-266.0; realized 252-day volatility near 37% is moderate, and the YZ-HAR engine reads the current 60-day regime near 41%.",
      bull: "A daily close back above the SAR 197 20-day, then the SAR 210 area, would signal the consolidation is resolving up; reclaiming the SAR 235-266 zone would need proof that the Vision-2030 build is converting to earnings.",
      bear: "A daily close below the SAR 185 50-day and SAR 179 100-day opens the lower band toward the SAR 157 52-week low."
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
    spot: 3.51,
    spotDate: "close 6 Jul 2026",
    ccy: "AED",
    fair: { bear: 3.05, base: 4.37, full: 6.09 },      // 06 Jul 2026 — four-lens weighted central 4.37 (+25% vs spot 3.51). Lenses: consolidated DCF 4.60 (primary; sleeve-built WACC ~10.6%, TV 70% of EV disclosed), segment SOTP 4.24, relative EV/EBITDA 3.83 (floor), normalized earnings 4.51; weights 35/25/15/25. FY25 optics (EPS 0.103, EBITDA −32%) carry AED 143mn of ring-fenced provisions; underlying EBITDA margin held 12.5% and Q1-26 turned. Swing: the Snacking margin reset (green coffee + EGP) and the KSA protein ramp. §3 Monte Carlo TIES its calibration back-test benchmark (PARITY — calibrated, honest, no single-name edge; the earlier FAILED banner used the superseded skill<0 rule, now corrected under the fitted 9-name UAE market profile).
    dist: {
      t20: { label:"1 month (T+20)",  p5:3.11, p25:3.36, p50:3.51, p75:3.67, p95:3.95, resolve:"2026-08-03" },
      t60: { label:"3 months (T+60)", p5:2.85, p25:3.26, p50:3.52, p75:3.79, p95:4.31, resolve:"2026-09-28" }
    },
    touch: [ /* descending high -> low; P(touch) T+20 %, T+60 % */
      [4.40, 1, 7], [4.20, 2, 13], [4.00, 6, 24], [3.70, 36, 59], [3.40, 54, 72], [3.20, 15, 38], [3.00, 4, 17]
    ],
    levels: { res:[3.70, 4.00, 4.20], sup:[3.40, 3.20, 3.00] },
    tech: {
      trend: "Below the full 20/50/100/200-day stack — soft, corrective",
      summary: "The tape sold the FY25 print in March and has not yet paid for the Q1 turn. Price sits below all four moving averages (≈3.57 / 3.59 / 3.64 / 3.73), RSI(14) is near 43 (neutral-weak, no washout), and the daily MACD (12·26·9) holds below its signal (−0.022 line / −0.011 signal / −0.012 histogram) — a bearish but flattening posture. Trailing realized volatility is ~22% while the gap-aware cone volatility is ≈26%. Nearest resistance is the 20/50-day cluster at 3.57–3.59, then the 200-day near 3.73 and the round 4.00; nearest support is the recent floor at 3.40, then the 52-week low 3.34 and 3.20.",
      bull: "A daily close above the 20/50-day cluster (≈3.59) opens the 200-day near 3.73 — the first repair signal.",
      bear: "Losing 3.40 exposes the 52-week low at 3.34; below that, the 3.00–3.20 zone is the bear-case shelf."
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
    spot: 313.09,
    spotDate: "close 6 Jul 2026",
    ccy: "USD",
    fair: { bear: 182, base: 208, full: 244 },      // 06 Jul 2026 — four-lens weighted central 208 (spot 313.09 = +51% above central). Lenses: consolidated DCF 152 (primary/floor), segment sum-of-the-parts 184, forward multiples 249, normalized earnings 253; DCF & relative weighted 30% each, normalized & SOTP 20% each. The ~$90 DCF-vs-multiple spread is the story — the durability/Services annuity the explicit cash flows do not capitalise; a football field, never a rating. Swing: Services attach-rate, gross-margin trajectory, the AI upgrade cycle.
    dist: {
      t20: { label:"1 month (T+20)",  p5:267, p25:293, p50:310, p75:327, p95:356, resolve:"2026-08-03" },
      t60: { label:"3 months (T+60)", p5:237, p25:276, p50:303, p75:333, p95:386, resolve:"2026-09-28" }
    },
    touch: [ /* descending high -> low; P(touch) T+20 %, T+60 % */
      [376, 3, 13], [360, 7, 23], [344, 18, 38], [329, 41, 60], [297, 47, 72], [282, 21, 50], [266, 7, 29], [250, 2, 15]
    ],
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
    spot: 420.60,
    spotDate: "close 30 Jun 2026",
    ccy: "USD",
    fair: { bear: 105, base: 254, full: 350 },      // 01 Jul 2026 — five-lens weighted central 254 (−40% vs spot 420.60). Lenses: SOTP 230 (primary), consolidated DCF 90 (floor), relative 172, normalized earnings 130, and autonomy-at-scale (SOTP bull) 560 carrying a full 25% weight. bear = operating-only floor / cash-returns 105; full = scenario real-options / weighted football bull ~350; autonomy-at-scale reaches 560. Swing factor: the FSD/Robotaxi/Optimus autonomy option.
    dist: {
      t20: { label:"1 month (T+20)",  p5:325, p25:379, p50:420, p75:466, p95:541, resolve:"2026-07-28" },
      t60: { label:"3 months (T+60)", p5:270, p25:350, p50:419, p75:501, p95:647, resolve:"2026-09-22" }
    },
    touch: [ /* descending high -> low; P(touch) T+20 %, T+60 % */
      [540, 8, 30], [500, 21, 46], [485, 29, 54], [460, 47, 68], [380, 42, 65], [360, 25, 51], [320, 6, 28]
    ],
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
    spot: 382.30,
    spotDate: "close 3 Jul 2026",
    ccy: "AED",
    fair: { bear: 78, base: 104.5, full: 150 },      // 4 Jul 2026 — five-lens weighted central 104.5 (−73% vs spot 382.30). Lenses: look-through SOTP/NAV 120 (primary), consolidated operating DCF 81 (floor), relative multiples 102, normalized earnings 91; weights 45/15/20/20. Swing: the premium the market pays over reconstructable NAV — IHC trades at ~3.2x look-through NAV / ~5.5x attributable book, the inverse of the usual holdco discount.
    dist: {
      t20: { label:"1 month (T+20)",  p5:340.6, p25:376.0, p50:384.4, p75:397.1, p95:427.9, resolve:"2026-07-31" },
      t60: { label:"3 months (T+60)", p5:322.6, p25:364.8, p50:391.3, p75:418.2, p95:462.3, resolve:"2026-09-25" }
    },
    touch: [ /* descending high -> low; P(touch) T+20 %, T+60 % */
      [459, 1, 8], [440, 3, 17], [421, 10, 33], [405, 21, 51], [394, 35, 67], [371, 23, 47], [359, 14, 34], [344, 8, 20], [325, 2, 9]
    ],
    levels: { res:[384.9, 388.2, 391.5], sup:[380.0, 371.0, 359.0] },
    tech: {
      trend: "Below every major moving average in a descending stack; a soft, low-volatility drift",
      summary: "The tape is soft and, above all, tight. IHC sits below all four major moving averages, arranged in a stepwise-descending stack (200-day AED 395.65 > 100-day 391.46 > 50-day 388.23 > 20-day 384.85 > price 382.30) — the classic signature of a mild, orderly downtrend. RSI(14) near 42.9 is neutral-to-soft and the daily MACD is modestly below its signal (−1.95 line / −1.62 signal / −0.33 histogram). What stands out is the range: a 52-week band of barely 6% (AED 380–404), reflecting very low turnover and buy-and-hold ownership — the same thinness that makes the observed −0.24 beta a float artifact rather than a true low-risk signal.",
      bull: "A daily close back above the 385–392 moving-average cluster would signal the soft patch is over; reclaiming the 52-week high near AED 404 would need a positive catalyst — a deal, the pending Multiply/2PointZero/Ghitha merger, or index / flow support.",
      bear: "A daily close below the 52-week low at AED 380 opens the lower band toward AED 371, then 359."
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
    spot: 6.43,
    spotDate: "close 1 Jul 2026",
    ccy: "EGP",
    fair: { bear: 5.20, base: 8.40, full: 11.82 },          // 3 Jul 2026 valuation — weighted central 8.40 (RNAV 8.30 primary / DCF 8.30 / relative 7.45 / normalized 9.25; 40/20/15/25). bear 5.20, bull 11.82. Swing: partnership-annuity marks & the RNAV/state discount.
    dist: {
      t20: { label:"1 month (T+20)",   p5:5.37, p25:6.09, p50:6.54, p75:7.01, p95:7.89, resolve:"2026-07-29" },
      t60: { label:"3 months (T+60)",  p5:4.84, p25:5.95, p50:6.74, p75:7.60, p95:9.27, resolve:"2026-09-24" }
    },
    touch: [ /* level, P(touch) T+20 %, T+60 % — descending */
      [8.00, 6, 28], [7.50, 16, 44], [7.00, 39, 67], [6.75, 59, 79], [6.10, 46, 63], [5.75, 21, 41]
    ],
    levels: { res:[6.75, 6.60, 6.51], sup:[6.10, 5.75, 5.40] },
    tech: {
      trend: "Consolidating inside a strong uptrend",
      summary: "The stock has nearly doubled since January and is now digesting the run — sitting on its 20- and 50-day averages, comfortably above the 100- and 200-day. Momentum has cooled to neutral (RSI ~49) and the daily MACD is flat, so this reads as a pause inside an intact uptrend rather than a top, with the rising 200-day far below as trend support.",
      bull: "A daily close back above the 6.75 range-top clears the way toward the 7.08 high.",
      bear: "A close below 6.10 breaks the two-month range and opens 5.75, then 5.40."
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
    spot: 8.28,
    spotDate: "close 6 Jul 2026",
    ccy: "EGP",
    fair: { bear: 5.92, base: 8.23, full: 11.51 },          // 6 Jul 2026 valuation — split-leg RNAV primary lens
    dist: {
      t20: { label:"1 month (T+20)",   p5:6.63, p25:7.74, p50:8.45,  p75:9.24,  p95:10.68, resolve:"2026-08-03" },
      t60: { label:"3 months (T+60)",  p5:5.86, p25:7.55, p50:8.81,  p75:10.25, p95:13.17, resolve:"2026-09-28" }
    },
    touch: [ /* level, P(touch) T+20 %, T+60 % — descending */
      [10.76, 7, 30], [9.94, 18, 47], [9.11, 44, 70], [8.69, 66, 83], [7.87, 54, 69], [7.45, 30, 50], [6.62, 8, 23]
    ],
    levels: { res:[8.55, 8.75, 9.11], sup:[8.02, 7.55, 7.08] },
    tech: {
      trend: "Strong uptrend — extended above every major average",
      summary: "The stock has nearly tripled off its 52-week low to a June high and sits above the 20-, 50-, 100- and 200-day averages, with RSI near 70 and a positive MACD. It is a powerful post-discount re-rating that has run into overbought territory — momentum is still up but stretched, and pullbacks from here read as mean-reversion inside an intact trend rather than a break.",
      bull: "A daily close above the 8.75 high extends the breakout toward the 9-handle.",
      bear: "A close back below the rising 20-day near 7.08 would signal the overbought move is unwinding toward 6.1."
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
     horizon_label      free text, e.g. "T+20", "T+60", "3M"
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
   ========================================================================== */
const LEDGER = [
  // ---- BURJEEL \u00b7 other (ADX UAE) \u00b7 cycle 1 (11 Jul 2026 published study, v4 reissued 12 Jul 2026; MC PARITY -- calibrated, no single-name edge) ----
  {
    instrument:"BURJEEL", asset_class:"other", cal:"matches",
    anchor_date:"2026-07-10", anchor_price:1.11, ccy:"AED",
    horizon_label:"T+20", grade_date:"2026-08-07", cycle_no:1, reanchor_from:null,
    anchor_vol:0.308, horizon_days:20,
    note:"MATCHES BENCHMARK (PARITY) under the production UAE market profile (live panel: production nu/width_cal, signal OFF). BURJEEL's own tape replayed under production parameters gives CRPS skill +0.85% over 11 non-overlapping 60-day windows, with a 90% bootstrap CI [-1.69%, +2.53%] and ROBUST across bootstrap block sizes 2/3/4 -- a calibrated, market-panel-validated distribution with no single-name edge demonstrated or claimed. Coverage 46/91/91% against 50/80/90 targets. Carry is the AED risk-free anchor less a trailing dividend-yield proxy. This is the v4 reissue (12-Jul-2026): the underlying study rebuilt the tax path on Pillar-Two SBIE mechanics and recalibrated relative multiples to verified peer marks -- the MC engine, this calibration verdict, and the grading dates are UNCHANGED from the original 11-Jul-2026 anchor. See study S1.7/B.4.",
    p5:0.94, p25:1.04, p50:1.11, p75:1.18, p95:1.31,
    touch:{ "+5":52, "+10":26, "+15":12, "+20":5, "-5":49, "-10":21 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"BURJEEL", asset_class:"other", cal:"matches",
    anchor_date:"2026-07-10", anchor_price:1.11, ccy:"AED",
    horizon_label:"T+60", grade_date:"2026-10-02", cycle_no:1, reanchor_from:null,
    anchor_vol:0.308, horizon_days:60,
    note:"MATCHES BENCHMARK (PARITY) under the production UAE market profile (live panel: production nu/width_cal, signal OFF). BURJEEL's own tape replayed under production parameters gives CRPS skill +0.85% over 11 non-overlapping 60-day windows, with a 90% bootstrap CI [-1.69%, +2.53%] and ROBUST across bootstrap block sizes 2/3/4 -- a calibrated, market-panel-validated distribution with no single-name edge demonstrated or claimed. Coverage 46/91/91% against 50/80/90 targets. Carry is the AED risk-free anchor less a trailing dividend-yield proxy. This is the v4 reissue (12-Jul-2026): the underlying study rebuilt the tax path on Pillar-Two SBIE mechanics and recalibrated relative multiples to verified peer marks -- the MC engine, this calibration verdict, and the grading dates are UNCHANGED from the original 11-Jul-2026 anchor. See study S1.7/B.4.",
    p5:0.84, p25:1.00, p50:1.11, p75:1.24, p95:1.49,
    touch:{ "+5":71, "+10":52, "+15":36, "+20":25, "-5":69, "-10":46 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },

  // ---- SALIK · other (DFM UAE) · cycle 1 (12 Jul 2026 published study v3; MC PARITY -- calibrated, no single-name edge) ----
  {
    instrument:"SALIK", asset_class:"other", cal:"matches",
    anchor_date:"2026-07-10", anchor_price:5.70, ccy:"AED",
    horizon_label:"T+20", grade_date:"2026-08-07", cycle_no:1, reanchor_from:null,
    anchor_vol:0.285, horizon_days:20,
    note:"MATCHES BENCHMARK (PARITY) under the production UAE market profile (14-name ADX/DFM panel: tail parameter 10, cone width 1.049, signal OFF). SALIK's own tape replayed under these production parameters gives CRPS skill -1.82% over 11 non-overlapping 60-day windows, with a 90% bootstrap CI straddling zero [-7.72%, +1.67%] and ROBUST across bootstrap block sizes 2/3/4 -- a calibrated, market-panel-validated distribution with no single-name edge demonstrated or claimed. TWO HONESTY FLAGS. (1) Only 11 windows: SALIK listed 29-Sep-2022, so the five-year walk-forward truncates to 3.8 years. (2) The cone is OVER-COVERED -- coverage 55/91/100% against 50/80/90 targets, and it runs 1.26x as wide as the benchmark. Read the bands, and ESPECIALLY the touch probabilities, as UPPER BOUNDS: an over-wide cone lets a path graze a level it would not otherwise reach. Carry = CBUAE Base Rate 3.63% less the trailing declared dividend yield 3.886%; they nearly cancel, which is why the median is an EXPLAINED flat. NOTE: the 7-8 Jul Hormuz re-escalation sits three days before the anchor and INSIDE the T+60 window. See study S3.",
    p5:4.94, p25:5.40, p50:5.70, p75:6.02, p95:6.57,
    touch:{ "+5":48, "+10":22, "+15":9, "+20":3, "-5":46, "-10":17 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"SALIK", asset_class:"other", cal:"matches",
    anchor_date:"2026-07-10", anchor_price:5.70, ccy:"AED",
    horizon_label:"T+60", grade_date:"2026-10-02", cycle_no:1, reanchor_from:null,
    anchor_vol:0.285, horizon_days:60,
    note:"MATCHES BENCHMARK (PARITY) under the production UAE market profile (14-name ADX/DFM panel: tail parameter 10, cone width 1.049, signal OFF). SALIK's own tape replayed under these production parameters gives CRPS skill -1.82% over 11 non-overlapping 60-day windows, with a 90% bootstrap CI straddling zero [-7.72%, +1.67%] and ROBUST across bootstrap block sizes 2/3/4 -- a calibrated, market-panel-validated distribution with no single-name edge demonstrated or claimed. TWO HONESTY FLAGS. (1) Only 11 windows: SALIK listed 29-Sep-2022, so the five-year walk-forward truncates to 3.8 years. (2) The cone is OVER-COVERED -- coverage 55/91/100% against 50/80/90 targets, and it runs 1.26x as wide as the benchmark. Read the bands, and ESPECIALLY the touch probabilities, as UPPER BOUNDS: an over-wide cone lets a path graze a level it would not otherwise reach. Carry = CBUAE Base Rate 3.63% less the trailing declared dividend yield 3.886%; they nearly cancel, which is why the median is an EXPLAINED flat. NOTE: the 7-8 Jul Hormuz re-escalation sits three days before the anchor and INSIDE the T+60 window. See study S3.",
    p5:4.42, p25:5.17, p50:5.69, p75:6.28, p95:7.34,
    touch:{ "+5":68, "+10":46, "+15":30, "+20":19, "-5":67, "-10":42 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  // ---- DIB · other (DFM UAE) · cycle 1 (11 Jul 2026 published study; MC FAILED calibration — indicative only) ----
  {
    instrument:"DIB", asset_class:"other",
    anchor_date:"2026-07-03", anchor_price:7.72, ccy:"AED",
    horizon_label:"T+20", grade_date:"2026-08-05", cycle_no:1, reanchor_from:null,
    p5:6.97, p25:7.45, p50:7.72, p75:7.99, p95:8.55,
    touch:{ "+5":38, "+10":15, "+15":5, "+20":2, "-5":36, "-10":13 },
    anchor_vol:0.225, horizon_days:20,
    note:"No CRPS skill vs random-walk benchmark (indicative only) — see study §3.1.",
    realized_close:null, realized_high:null, realized_low:null, in_90:null, in_50:null,
    realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"DIB", asset_class:"other",
    anchor_date:"2026-07-03", anchor_price:7.72, ccy:"AED",
    horizon_label:"T+60", grade_date:"2026-10-02", cycle_no:1, reanchor_from:null,
    p5:6.46, p25:7.25, p50:7.71, p75:8.19, p95:9.18,
    touch:{ "+5":58, "+10":33, "+15":18, "+20":9, "-5":54, "-10":29 },
    anchor_vol:0.225, horizon_days:60,
    note:"No CRPS skill vs random-walk benchmark (indicative only) — see study §3.1.",
    realized_close:null, realized_high:null, realized_low:null, in_90:null, in_50:null,
    realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },

  // ---- 2POINTZERO · other (ADX UAE) · cycle 1 (11 Jul 2026 published study; production UAE panel constituent, PARITY / matches benchmark) ----
  {
    instrument:"2POINTZERO", asset_class:"other", cal:"matches",
    anchor_date:"2026-07-03", anchor_price:2.16, ccy:"AED",
    horizon_label:"T+20", grade_date:"2026-07-31", cycle_no:1, reanchor_from:null,
    anchor_vol:0.383, horizon_days:20,
    note:"MATCHES BENCHMARK under the production UAE market profile (14-name ADX/DFM panel, refit 11-Jul-2026: nu=10, cone width 1.049; 2POINTZERO is a panel constituent and scores PARITY). A replay of its own tape under these production parameters gives CRPS skill +0.18% over 14 non-overlapping 60-day windows, with a 90% bootstrap CI straddling zero and coverage of 50/79/93% against 50/80/90 targets -- a calibrated, market-panel-validated distribution with no single-name edge demonstrated or claimed. Carry = CBUAE Base Rate 3.65%; no dividend declared, so q=0. NOTE: the price history ends 3-Jul-2026 and the 7-8 Jul US-Iran ceasefire collapse post-dates it -- read the downside percentiles as floors. See study S3.",
    p5:1.80, p25:2.02, p50:2.17, p75:2.33, p95:2.59,
    touch:{ "+5":56, "+10":32, "+15":16, "+20":8, "-5":53, "-10":26 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"2POINTZERO", asset_class:"other", cal:"matches",
    anchor_date:"2026-07-03", anchor_price:2.16, ccy:"AED",
    horizon_label:"T+60", grade_date:"2026-09-25", cycle_no:1, reanchor_from:null,
    anchor_vol:0.383, horizon_days:60,
    note:"MATCHES BENCHMARK under the production UAE market profile (14-name ADX/DFM panel, refit 11-Jul-2026: nu=10, cone width 1.049; 2POINTZERO is a panel constituent and scores PARITY). A replay of its own tape under these production parameters gives CRPS skill +0.18% over 14 non-overlapping 60-day windows, with a 90% bootstrap CI straddling zero and coverage of 50/79/93% against 50/80/90 targets -- a calibrated, market-panel-validated distribution with no single-name edge demonstrated or claimed. Carry = CBUAE Base Rate 3.65%; no dividend declared, so q=0. NOTE: the price history ends 3-Jul-2026 and the 7-8 Jul US-Iran ceasefire collapse post-dates it -- read the downside percentiles as floors. See study S3.",
    p5:1.59, p25:1.93, p50:2.18, p75:2.46, p95:3.00,
    touch:{ "+5":74, "+10":57, "+15":42, "+20":30, "-5":71, "-10":50 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  // ---- EAND · other (ADX UAE) · cycle 1 (11 Jul 2026 published study; production UAE panel fit, PARITY) ----
  {
    instrument:"EAND", asset_class:"other",
    anchor_date:"2026-07-09", anchor_price:19.66, ccy:"AED",
    horizon_label:"T+20", grade_date:"2026-08-06", cycle_no:1, reanchor_from:null,
    anchor_vol:0.233, horizon_days:20,
    note:"PARITY under the production UAE market profile (10-name ADX/DFM panel, fitted 10-Jul-2026: nu=4, cone width 1.070; panel-level CRPS skill -2.1%, bootstrap 90% CI robust across block sizes 2/3/4). A diagnostic replay of e&'s own five-year tape under these production parameters gives CRPS skill -2.0% (n=18 non-overlapping 60-day windows), closely tracking the panel: a calibrated, market-panel-validated distribution, no single-name edge demonstrated or claimed. e& is not yet a panel constituent (first publish) -- carry = CBUAE Base Rate 3.65% less the forward dividend yield. See study S3.",
    p5:17.84, p25:19.05, p50:19.72, p75:20.43, p95:21.81,
    touch:{ "+5":32, "+10":10, "+15":3, "+20":1, "-5":27, "-10":7 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"EAND", asset_class:"other",
    anchor_date:"2026-07-09", anchor_price:19.66, ccy:"AED",
    horizon_label:"T+60", grade_date:"2026-10-02", cycle_no:1, reanchor_from:null,
    anchor_vol:0.233, horizon_days:60,
    note:"PARITY under the production UAE market profile (10-name ADX/DFM panel, fitted 10-Jul-2026: nu=4, cone width 1.070; panel-level CRPS skill -2.1%, bootstrap 90% CI robust across block sizes 2/3/4). A diagnostic replay of e&'s own five-year tape under these production parameters gives CRPS skill -2.0% (n=18 non-overlapping 60-day windows), closely tracking the panel: a calibrated, market-panel-validated distribution, no single-name edge demonstrated or claimed. e& is not yet a panel constituent (first publish) -- carry = CBUAE Base Rate 3.65% less the forward dividend yield. See study S3.",
    p5:16.70, p25:18.68, p50:19.86, p75:21.09, p95:23.59,
    touch:{ "+5":57, "+10":31, "+15":16, "+20":9, "-5":49, "-10":22 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  // ---- ADCB · other (ADX UAE) · cycle 1 (10 Jul 2026 published study; MC PASSES benchmark robustly, carry drift) ----
  {
    instrument:"ADCB", asset_class:"other",
    anchor_date:"2026-07-03", anchor_price:15.10, ccy:"AED",
    horizon_label:"T+20", grade_date:"2026-08-05", cycle_no:1, reanchor_from:null,
    anchor_vol:0.275, horizon_days:20,
    note:"Beats the naive carry-anchored random-walk benchmark on CRPS skill (+2.3%, n=14 non-overlapping 60-day windows) with PIT mean 0.54 and coverage near nominal — passes calibration robustly: the 90% bootstrap CI sits above zero across block sizes 2/3/4 ([+0.4%,+3.5%] / [+0.2%,+4.0%] / [+0.3%,+3.2%]). Fitted under the UAE market profile (fat-tailed t, 4 d.o.f.; width calibration 1.07) estimated on a 9-name ADX/DFM panel — ADCB is the first UAE name with a demonstrated single-name edge. See study §3.",
    p5:13.28, p25:14.43, p50:15.09, p75:15.79, p95:17.2,
    touch:{ "+5":44, "+10":17, "+15":5, "+20":1, "-5":43, "-10":14 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"ADCB", asset_class:"other",
    anchor_date:"2026-07-03", anchor_price:15.10, ccy:"AED",
    horizon_label:"T+60", grade_date:"2026-10-02", cycle_no:1, reanchor_from:null,
    anchor_vol:0.275, horizon_days:60,
    note:"Beats the naive carry-anchored random-walk benchmark on CRPS skill (+2.3%, n=14 non-overlapping 60-day windows) with PIT mean 0.54 and coverage near nominal — passes calibration robustly: the 90% bootstrap CI sits above zero across block sizes 2/3/4 ([+0.4%,+3.5%] / [+0.2%,+4.0%] / [+0.3%,+3.2%]). Fitted under the UAE market profile (fat-tailed t, 4 d.o.f.; width calibration 1.07) estimated on a 9-name ADX/DFM panel — ADCB is the first UAE name with a demonstrated single-name edge. See study §3.",
    p5:12.04, p25:13.95, p50:15.09, p75:16.32, p95:18.87,
    touch:{ "+5":66, "+10":43, "+15":26, "+20":15, "-5":65, "-10":39 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  // ---- AGTHIA · other (ADX UAE) · cycle 1 (8 Jul 2026 published study; MC FAILS the calibration back-test — indicative only) ----
  {
    instrument:"AGTHIA", asset_class:"other",
    anchor_date:"2026-07-06", anchor_price:3.51, ccy:"AED",
    horizon_label:"T+20", grade_date:"2026-08-03", cycle_no:1, reanchor_from:null,
    anchor_vol:0.223, horizon_days:20,
    cal:"matches",
    note:"Ties the naive carry-anchored random-walk benchmark on CRPS skill (−0.4%, n=14 non-overlapping 60-day windows) with the 90% bootstrap CI spanning zero (robust across block sizes 2/3/4) and a well-calibrated PIT — PARITY, not a failed calibration: an honest, market-panel-validated probability map with no demonstrated single-name edge. Re-scored under the fitted UAE market profile (9-name ADX/DFM panel, fat-tailed t/4 d.o.f., width 1.07); the earlier FAILED banner used the superseded skill<0 rule. See study §3.",
    p5:3.11, p25:3.36, p50:3.51, p75:3.67, p95:3.95,
    touch:{ "+5":39, "+10":14, "+15":5, "+20":2, "-5":37, "-10":11 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"AGTHIA", asset_class:"other",
    anchor_date:"2026-07-06", anchor_price:3.51, ccy:"AED",
    horizon_label:"T+60", grade_date:"2026-09-28", cycle_no:1, reanchor_from:null,
    anchor_vol:0.223, horizon_days:60,
    cal:"matches",
    note:"Ties the naive carry-anchored random-walk benchmark on CRPS skill (−0.4%, n=14 non-overlapping 60-day windows) with the 90% bootstrap CI spanning zero (robust across block sizes 2/3/4) and a well-calibrated PIT — PARITY, not a failed calibration: an honest, market-panel-validated probability map with no demonstrated single-name edge. Re-scored under the fitted UAE market profile (9-name ADX/DFM panel, fat-tailed t/4 d.o.f., width 1.07); the earlier FAILED banner used the superseded skill<0 rule. See study §3.",
    p5:2.85, p25:3.26, p50:3.52, p75:3.79, p95:4.31,
    touch:{ "+5":62, "+10":37, "+15":21, "+20":12, "-5":59, "-10":32 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  // ---- GBCO · equity (EGX Egypt) · cycle 1 (8 Jul 2026 published study; MC PASSES benchmark, secular drift ON) ----
  {
    instrument:"GBCO", asset_class:"equity",
    anchor_date:"2026-07-07", anchor_price:31.25, ccy:"EGP",
    horizon_label:"T+20", grade_date:"2026-08-04", cycle_no:1, reanchor_from:null,
    anchor_vol:0.50, horizon_days:20,
    note:"Beats the zero-drift random-walk benchmark on CRPS skill (+0.032 non-overlapping, +0.096 monthly origins) with a roughly uniform PIT — passes calibration with the EGX secular drift ON (zero drift failed; first EGX non-developer with the drift, adopted empirically). See study Appendix B.",
    p5:26.09, p25:29.96, p50:32.47, p75:35.12, p95:40.53,
    touch:{ "+5":69, "+10":46, "+15":29, "+20":18, "-5":47, "-10":23 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"GBCO", asset_class:"equity",
    anchor_date:"2026-07-07", anchor_price:31.25, ccy:"EGP",
    horizon_label:"T+60", grade_date:"2026-09-29", cycle_no:1, reanchor_from:null,
    anchor_vol:0.50, horizon_days:60,
    note:"Beats the zero-drift random-walk benchmark on CRPS skill (+0.032 non-overlapping, +0.096 monthly origins) with a roughly uniform PIT — passes calibration with the EGX secular drift ON (zero drift failed; first EGX non-developer with the drift, adopted empirically). See study Appendix B.",
    p5:23.97, p25:30.62, p50:34.98, p75:40.13, p95:51.08,
    touch:{ "+5":87, "+10":76, "+15":64, "+20":53, "-5":59, "-10":38 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  // ---- RIBL · other (TADAWUL Saudi Arabia) · cycle 1 (09 Jul 2026 published study; MC PASSES benchmark marginally, zero drift) ----
  {
    instrument:"RIBL", asset_class:"other",
    anchor_date:"2026-07-07", anchor_price:20.23, ccy:"SAR",
    horizon_label:"T+20", grade_date:"2026-08-04", cycle_no:1, reanchor_from:null,
    anchor_vol:0.233, horizon_days:20,
    note:"Beats the zero-drift random-walk benchmark on CRPS skill (+0.36%, n=18 non-overlapping 60-day windows) with PIT mean 0.464 — passes calibration, but marginally on a thin sample (below the ~20-window 'decent validation' bar), a property of RIBL's ~5-year listed history. Zero drift (GCC-pegged bank, per our standing rule).",
    p5:18.27, p25:19.49, p50:20.22, p75:20.99, p95:22.43,
    touch:{ "+5":32, "+10":10, "+15":3, "+20":1, "-5":30, "-10":8 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"RIBL", asset_class:"other",
    anchor_date:"2026-07-07", anchor_price:20.23, ccy:"SAR",
    horizon_label:"T+60", grade_date:"2026-09-29", cycle_no:1, reanchor_from:null,
    anchor_vol:0.233, horizon_days:60,
    note:"Beats the zero-drift random-walk benchmark on CRPS skill (+0.36%, n=18 non-overlapping 60-day windows) with PIT mean 0.464 — passes calibration, but marginally on a thin sample (below the ~20-window 'decent validation' bar), a property of RIBL's ~5-year listed history. Zero drift (GCC-pegged bank, per our standing rule).",
    p5:16.95, p25:18.97, p50:20.22, p75:21.57, p95:24.19,
    touch:{ "+5":55, "+10":29, "+15":15, "+20":7, "-5":54, "-10":25 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  // ---- STC · equity (TADAWUL Saudi Arabia) · cycle 1 (09 Jul 2026 published study; MC PASSES benchmark, zero drift) ----
  {
    instrument:"STC", asset_class:"other",
    anchor_date:"2026-07-07", anchor_price:43.58, ccy:"SAR",
    horizon_label:"T+20", grade_date:"2026-08-04", cycle_no:1, reanchor_from:null,
    anchor_vol:0.151, horizon_days:20,
    note:"Beats the zero-drift random-walk benchmark on CRPS skill (+0.63%, n=18 non-overlapping 60-day windows) with PIT mean 0.499 — passes calibration (bootstrap 90% CI [-1.1%, +2.8%], P(skill>0)~71%). Zero drift (non-EGX international name, per our standing rule); the EGX-style secular-drift scheme was tested and failed (CRPS skill -4.8%), confirming zero drift is the right adopted scheme for this name.",
    p5:40.79, p25:42.61, p50:43.69, p75:44.80, p95:46.81,
    touch:{ "+5":19, "+10":3, "+15":1, "+20":0, "-5":15, "-10":2 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"STC", asset_class:"other",
    anchor_date:"2026-07-07", anchor_price:43.58, ccy:"SAR",
    horizon_label:"T+60", grade_date:"2026-09-29", cycle_no:1, reanchor_from:null,
    anchor_vol:0.151, horizon_days:60,
    note:"Beats the zero-drift random-walk benchmark on CRPS skill (+0.63%, n=18 non-overlapping 60-day windows) with PIT mean 0.499 — passes calibration (bootstrap 90% CI [-1.1%, +2.8%], P(skill>0)~71%). Zero drift (non-EGX international name, per our standing rule); the EGX-style secular-drift scheme was tested and failed (CRPS skill -4.8%), confirming zero drift is the right adopted scheme for this name.",
    p5:39.00, p25:42.03, p50:43.91, p75:45.85, p95:49.51,
    touch:{ "+5":44, "+10":17, "+15":6, "+20":2, "-5":35, "-10":11 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  // ---- ALDAR · other (ADX UAE) · cycle 1 (8 Jul 2026 published study; MC PASSES benchmark) ----
  {
    instrument:"ALDAR", asset_class:"other",
    anchor_date:"2026-07-03", anchor_price:8.30, ccy:"AED",
    horizon_label:"T+20", grade_date:"2026-07-31", cycle_no:1, reanchor_from:null,
    anchor_vol:0.34, horizon_days:20,
    cal:"matches",
    note:"Ties the naive carry-anchored random-walk benchmark on CRPS skill (−0.4%, n=14 non-overlapping 60-day windows) with the 90% bootstrap CI spanning zero (robust across block sizes 2/3/4) and a roughly uniform PIT — PARITY, not a demonstrated edge: an honest, well-calibrated map. Re-scored under the fitted UAE market profile (9-name ADX/DFM panel, fat-tailed t/4 d.o.f., width 1.07); the earlier +1.8% 'beats' reading was against the superseded zero-drift benchmark. See study §3.",
    p5:7.02, p25:7.86, p50:8.37, p75:8.92, p95:9.91,
    touch:{ "+5":52, "+10":28, "+15":14, "+20":7, "-5":44, "-10":20 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"ALDAR", asset_class:"other",
    anchor_date:"2026-07-03", anchor_price:8.30, ccy:"AED",
    horizon_label:"T+60", grade_date:"2026-09-25", cycle_no:1, reanchor_from:null,
    anchor_vol:0.34, horizon_days:60,
    cal:"matches",
    note:"Ties the naive carry-anchored random-walk benchmark on CRPS skill (−0.4%, n=14 non-overlapping 60-day windows) with the 90% bootstrap CI spanning zero (robust across block sizes 2/3/4) and a roughly uniform PIT — PARITY, not a demonstrated edge: an honest, well-calibrated map. Re-scored under the fitted UAE market profile (9-name ADX/DFM panel, fat-tailed t/4 d.o.f., width 1.07); the earlier +1.8% 'beats' reading was against the superseded zero-drift benchmark. See study §3.",
    p5:6.36, p25:7.60, p50:8.50, p75:9.48, p95:11.29,
    touch:{ "+5":74, "+10":56, "+15":41, "+20":28, "-5":64, "-10":42 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  // ---- EMAARDEV · other (DFM UAE) · cycle 1 (8 Jul 2026 published study; MC matches benchmark, indicative) ----
  {
    instrument:"EMAARDEV", asset_class:"other",
    anchor_date:"2026-07-03", anchor_price:14.26, ccy:"AED",
    horizon_label:"T+20", grade_date:"2026-07-31", cycle_no:1, reanchor_from:null,
    anchor_vol:0.369, horizon_days:20, cal:"matches",
    note:"Matches (ties) the zero-drift random-walk benchmark — no demonstrated CRPS edge; distribution well-calibrated (indicative). See study Appendix B.",
    p5:12.42, p25:13.78, p50:14.60, p75:15.49, p95:17.18,
    touch:{ "+5":57, "+10":40, "+15":18, "+20":9, "-5":40, "-10":14 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"EMAARDEV", asset_class:"other",
    anchor_date:"2026-07-03", anchor_price:14.26, ccy:"AED",
    horizon_label:"T+60", grade_date:"2026-09-25", cycle_no:1, reanchor_from:null,
    anchor_vol:0.369, horizon_days:60, cal:"matches",
    note:"Matches (ties) the zero-drift random-walk benchmark — no demonstrated CRPS edge; distribution well-calibrated (indicative). See study Appendix B.",
    p5:11.59, p25:13.87, p50:15.34, p75:16.97, p95:20.33,
    touch:{ "+5":81, "+10":64, "+15":49, "+20":37, "-5":53, "-10":30 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  // ---- ISPH \u00b7 equity (EGX Egypt) \u00b7 cycle 1 (7 Jul 2026 published study; MC FAILED benchmark, indicative) ----
  {
    instrument:"ISPH", asset_class:"equity",
    anchor_date:"2026-07-07", anchor_price:11.67, ccy:"EGP",
    horizon_label:"T+20", grade_date:"2026-08-04", cycle_no:1, reanchor_from:null,
    anchor_vol:0.29, horizon_days:20,
    note:"No CRPS skill vs random-walk benchmark (indicative only) \u2014 see study \u00a73.",
    p5:10.16, p25:11.14, p50:11.75, p75:12.39, p95:13.52,
    touch:{ "+5":48, "+10":22, "+15":9, "+20":4, "-5":40, "-10":15 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"ISPH", asset_class:"equity",
    anchor_date:"2026-07-07", anchor_price:11.67, ccy:"EGP",
    horizon_label:"T+60", grade_date:"2026-09-29", cycle_no:1, reanchor_from:null,
    anchor_vol:0.29, horizon_days:60,
    note:"No CRPS skill vs random-walk benchmark (indicative only) \u2014 see study \u00a73.",
    p5:9.29, p25:10.85, p50:11.91, p75:13.06, p95:15.18,
    touch:{ "+5":70, "+10":49, "+15":32, "+20":21, "-5":60, "-10":36 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"SABIC", asset_class:"other",
    anchor_date:"2026-07-07", anchor_price:51.80, ccy:"SAR",
    horizon_label:"T+20", grade_date:"2026-08-04", cycle_no:1, reanchor_from:null,
    p5:45.16, p25:49.46, p50:51.85, p75:54.26, p95:58.79,
    touch:{ "+5":37, "+10":15, "+15":6, "+20":2, "-5":35, "-10":13 },
    anchor_vol:0.1927, horizon_days:20,
    realized_close:null, realized_high:null, realized_low:null, in_90:null, in_50:null,
    realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"SABIC", asset_class:"other",
    anchor_date:"2026-07-07", anchor_price:51.80, ccy:"SAR",
    horizon_label:"T+60", grade_date:"2026-09-29", cycle_no:1, reanchor_from:null,
    p5:41.26, p25:47.42, p50:51.74, p75:56.35, p95:64.22,
    touch:{ "+5":61, "+10":39, "+15":23, "+20":13, "-5":60, "-10":36 },
    anchor_vol:0.1927, horizon_days:60,
    realized_close:null, realized_high:null, realized_low:null, in_90:null, in_50:null,
    realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },

  {
    instrument:"RELIANCE", asset_class:"other",
    anchor_date:"2026-07-06", anchor_price:1321.30, ccy:"INR",
    horizon_label:"T+20", grade_date:"2026-08-03", cycle_no:1, reanchor_from:null,
    p5:1160, p25:1266, p50:1331, p75:1400, p95:1526,
    touch:{ "+5":45, "+10":20, "+15":8, "+20":4, "-5":37, "-10":13 },
    anchor_vol:0.2073, horizon_days:20,
    realized_close:null, realized_high:null, realized_low:null, in_90:null, in_50:null,
    realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"RELIANCE", asset_class:"other",
    anchor_date:"2026-07-06", anchor_price:1321.30, ccy:"INR",
    horizon_label:"T+60", grade_date:"2026-09-28", cycle_no:1, reanchor_from:null,
    p5:1067, p25:1235, p50:1351, p75:1478, p95:1707,
    touch:{ "+5":69, "+10":48, "+15":31, "+20":20, "-5":57, "-10":33 },
    anchor_vol:0.2073, horizon_days:60,
    realized_close:null, realized_high:null, realized_low:null, in_90:null, in_50:null,
    realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },

  // ---- INFY · other (NSE India) · cycle 1 (6 Jul 2026 published study) ----
  {
    instrument:"INFY", asset_class:"other",
    anchor_date:"2026-07-06", anchor_price:1042.20, ccy:"INR",
    horizon_label:"T+20", grade_date:"2026-08-03", cycle_no:1, reanchor_from:null,
    p5:918, p25:998, p50:1047, p75:1099, p95:1193,
    touch:{ "+5":44, "+10":18, "+15":7, "+20":3, "-5":37, "-10":12 },
    anchor_vol:0.2702, horizon_days:20,
    realized_close:null, realized_high:null, realized_low:null, in_90:null, in_50:null,
    realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"INFY", asset_class:"other",
    anchor_date:"2026-07-06", anchor_price:1042.20, ccy:"INR",
    horizon_label:"T+60", grade_date:"2026-09-28", cycle_no:1, reanchor_from:null,
    p5:845, p25:972, p50:1058, p75:1151, p95:1326,
    touch:{ "+5":67, "+10":44, "+15":28, "+20":17, "-5":58, "-10":33 },
    anchor_vol:0.2702, horizon_days:60,
    realized_close:null, realized_high:null, realized_low:null, in_90:null, in_50:null,
    realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"NVDA", asset_class:"other",
    anchor_date:"2026-07-06", anchor_price:196.44, ccy:"USD",
    horizon_label:"T+20", grade_date:"2026-08-03", cycle_no:1, reanchor_from:null,
    p5:155.90, p25:179.63, p50:195.34, p75:212.20, p95:244.04,
    touch:{ "+5":76, "+10":48, "+15":29, "+20":17, "-5":50, "-10":41 },
    anchor_vol:0.3512, horizon_days:20,
    realized_close:null, realized_high:null, realized_low:null, in_90:null, in_50:null,
    realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"NVDA", asset_class:"other",
    anchor_date:"2026-07-06", anchor_price:196.44, ccy:"USD",
    horizon_label:"T+60", grade_date:"2026-09-28", cycle_no:1, reanchor_from:null,
    p5:131.56, p25:166.88, p50:193.31, p75:223.35, p95:282.86,
    touch:{ "+5":85, "+10":67, "+15":52, "+20":39, "-5":64, "-10":59 },
    anchor_vol:0.3512, horizon_days:60,
    realized_close:null, realized_high:null, realized_low:null, in_90:null, in_50:null,
    realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },

  {
    instrument:"LCSW", asset_class:"equity",
    anchor_date:"2026-07-06", anchor_price:29.45, ccy:"EGP",
    horizon_label:"T+20", grade_date:"2026-08-03", cycle_no:1, reanchor_from:null,
    p5:24.29, p25:27.76, p50:29.99, p75:32.38, p95:36.98,
    touch:{ "+5":62, "+10":39, "+15":23, "+20":14, "-5":50, "-10":26 },
    anchor_vol:0.4191, horizon_days:20,
    realized_close:null, realized_high:null, realized_low:null, in_90:null, in_50:null,
    realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"LCSW", asset_class:"equity",
    anchor_date:"2026-07-06", anchor_price:29.45, ccy:"EGP",
    horizon_label:"T+60", grade_date:"2026-09-28", cycle_no:1, reanchor_from:null,
    p5:21.69, p25:27.07, p50:31.01, p75:35.54, p95:44.37,
    touch:{ "+5":80, "+10":66, "+15":53, "+20":41, "-5":66, "-10":46 },
    anchor_vol:0.4191, horizon_days:60,
    realized_close:null, realized_high:null, realized_low:null, in_90:null, in_50:null,
    realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },

  {
    instrument:"KABO", asset_class:"equity",
    anchor_date:"2026-07-06", anchor_price:7.00, ccy:"EGP",
    horizon_label:"T+20", grade_date:"2026-08-03", cycle_no:1, reanchor_from:null,
    p5:5.58, p25:6.46, p50:7.03, p75:7.67, p95:8.92,
    touch:{ "+5":60, "+10":39, "+15":24, "+20":15, "-5":57, "-10":33 },
    anchor_vol:0.345, horizon_days:20,
    note:"No CRPS skill vs random-walk benchmark (indicative only) — see study Appendix B.",
    realized_close:null, realized_high:null, realized_low:null, in_90:null, in_50:null,
    realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"KABO", asset_class:"equity",
    anchor_date:"2026-07-06", anchor_price:7.00, ccy:"EGP",
    horizon_label:"T+60", grade_date:"2026-09-28", cycle_no:1, reanchor_from:null,
    p5:4.79, p25:6.12, p50:7.12, p75:8.28, p95:10.68,
    touch:{ "+5":77, "+10":63, "+15":50, "+20":40, "-5":73, "-10":55 },
    anchor_vol:0.345, horizon_days:60,
    note:"No CRPS skill vs random-walk benchmark (indicative only) — see study Appendix B.",
    realized_close:null, realized_high:null, realized_low:null, in_90:null, in_50:null,
    realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },

  {
    instrument:"IQCD", asset_class:"equity",
    anchor_date:"2026-07-05", anchor_price:11.07, ccy:"QAR",
    horizon_label:"T+20", grade_date:"2026-08-02", cycle_no:1, reanchor_from:null,
    p5:9.62, p25:10.60, p50:11.13, p75:11.68, p95:12.73,
    touch:{ "+5":30, "+10":13, "+15":6, "+20":3, "-5":50, "-10":29 },
    anchor_vol:0.2178, horizon_days:20,
    realized_close:null, realized_high:null, realized_low:null, in_90:null, in_50:null,
    realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"IQCD", asset_class:"equity",
    anchor_date:"2026-07-05", anchor_price:11.07, ccy:"QAR",
    horizon_label:"T+60", grade_date:"2026-09-27", cycle_no:1, reanchor_from:null,
    p5:8.84, p25:10.24, p50:11.21, p75:12.25, p95:14.08,
    touch:{ "+5":58, "+10":42, "+15":29, "+20":20, "-5":77, "-10":50 },
    anchor_vol:0.2178, horizon_days:60,
    realized_close:null, realized_high:null, realized_low:null, in_90:null, in_50:null,
    realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"EFIH", asset_class:"equity",
    anchor_date:"2026-07-01", anchor_price:20.74, ccy:"EGP",
    horizon_label:"T+20", grade_date:"2026-07-29", cycle_no:1, reanchor_from:null,
    p5:16.58, p25:19.13, p50:20.74, p75:22.48, p95:25.94,
    touch:{ "+5":59, "+10":37, "+15":22, "+20":13, "-5":57, "-10":32 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"EFIH", asset_class:"equity",
    anchor_date:"2026-07-01", anchor_price:20.74, ccy:"EGP",
    horizon_label:"T+60", grade_date:"2026-09-23", cycle_no:1, reanchor_from:null,
    p5:14.08, p25:18.04, p50:20.74, p75:23.85, p95:30.56,
    touch:{ "+5":76, "+10":59, "+15":46, "+20":35, "-5":74, "-10":56 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  { instrument:"JUFO", asset_class:"equity", anchor_date:"2026-07-01", anchor_price:29.99, ccy:"EGP",
    horizon_label:"T+20", grade_date:"2026-07-29", cycle_no:1, reanchor_from:null,
    p5:26.04, p25:28.92, p50:30.67, p75:32.54, p95:36.15,
    touch:{ "+5":58, "+10":31, "+15":16, "+20":8, "-5":40, "-10":16 },
    anchor_vol:0.3735, horizon_days:20,
    realized_close:null, realized_high:null, realized_low:null, in_90:null, in_50:null,
    realized_quantile:null, median_err:null, touch_hit:null },
  { instrument:"JUFO", asset_class:"equity", anchor_date:"2026-07-01", anchor_price:29.99, ccy:"EGP",
    horizon_label:"T+60", grade_date:"2026-09-23", cycle_no:1, reanchor_from:null,
    p5:24.17, p25:28.96, p50:32.07, p75:35.46, p95:42.63,
    touch:{ "+5":80, "+10":63, "+15":47, "+20":34, "-5":55, "-10":32 },
    anchor_vol:0.3735, horizon_days:60,
    realized_close:null, realized_high:null, realized_low:null, in_90:null, in_50:null,
    realized_quantile:null, median_err:null, touch_hit:null },
  { instrument:"EFID", asset_class:"equity", anchor_date:"2026-07-01", anchor_price:27.34, ccy:"EGP",
    horizon_label:"T+20", grade_date:"2026-07-29", cycle_no:1, reanchor_from:null,
    p5:22.35, p25:25.48, p50:27.48, p75:29.62, p95:33.56,
    touch:{ "+5":76, "+10":60, "+15":46, "+20":34, "-5":70, "-10":50 },
    anchor_vol:0.4127, horizon_days:20,
    realized_close:null, realized_high:null, realized_low:null, in_90:null, in_50:null,
    realized_quantile:null, median_err:null, touch_hit:null },
  { instrument:"EFID", asset_class:"equity", anchor_date:"2026-07-01", anchor_price:27.34, ccy:"EGP",
    horizon_label:"T+60", grade_date:"2026-09-23", cycle_no:1, reanchor_from:null,
    p5:19.4, p25:24.4, p50:27.82, p75:31.65, p95:38.98,
    touch:{ "+5":76, "+10":60, "+15":46, "+20":34, "-5":70, "-10":50 },
    anchor_vol:0.4127, horizon_days:60,
    realized_close:null, realized_high:null, realized_low:null, in_90:null, in_50:null,
    realized_quantile:null, median_err:null, touch_hit:null },
  // ---- PHDC · equity · cycle 2 (11 Jun 2026 published study) ----
  {
    instrument:"PHDC", asset_class:"equity",
    anchor_date:"2026-06-11", anchor_price:14.50, ccy:"EGP",
    horizon_label:"T+20", grade_date:"2026-07-09", cycle_no:2, reanchor_from:"2026-06-09",
    p5:11.53, p25:13.42, p50:14.92, p75:16.56, p95:19.32,
    touch:{ "+5":62, "+10":38, "+15":21, "+20":12, "-5":55, "-10":33 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"PHDC", asset_class:"equity",
    anchor_date:"2026-06-11", anchor_price:14.50, ccy:"EGP",
    horizon_label:"T+60", grade_date:"2026-09-03", cycle_no:2, reanchor_from:"2026-06-09",
    p5:10.18, p25:13.10, p50:15.83, p75:19.40, p95:24.50,
    touch:{ "+5":72, "+10":55, "+15":41, "+20":30, "-5":61, "-10":44 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  // ---- TMGH · equity · cycle 1 (15 Jun 2026 published study) ----
  {
    instrument:"TMGH", asset_class:"equity",
    anchor_date:"2026-06-15", anchor_price:95.68, ccy:"EGP",
    horizon_label:"T+20", grade_date:"2026-07-14", cycle_no:1, reanchor_from:null,
    p5:81.42, p25:91.17, p50:98.31, p75:106.10, p95:119.24,
    touch:{ "+5":66, "+10":24, "+15":8, "+20":2, "-5":29, "-10":11 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"TMGH", asset_class:"equity",
    anchor_date:"2026-06-15", anchor_price:95.68, ccy:"EGP",
    horizon_label:"T+60", grade_date:"2026-09-08", cycle_no:1, reanchor_from:null,
    p5:75.58, p25:91.20, p50:103.93, p75:118.41, p95:142.75,
    touch:{ "+5":85, "+10":58, "+15":39, "+20":24, "-5":48, "-10":29 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  }
,
  // ---- EMFD · equity · cycle 1 (17 Jun 2026 published study) ----
  {
    instrument:"EMFD", asset_class:"equity",
    anchor_date:"2026-06-17", anchor_price:12.44, ccy:"EGP",
    horizon_label:"T+20", grade_date:"2026-07-16", cycle_no:1, reanchor_from:null,
    p5:10.50, p25:11.80, p50:12.75, p75:13.78, p95:15.46,
    touch:{ "+5":64, "+10":41, "+15":24, "+20":13, "-5":49, "-10":23 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"EMFD", asset_class:"equity",
    anchor_date:"2026-06-17", anchor_price:12.44, ccy:"EGP",
    horizon_label:"T+60", grade_date:"2026-09-13", cycle_no:1, reanchor_from:null,
    p5:9.64, p25:11.71, p50:13.39, p75:15.29, p95:18.47,
    touch:{ "+5":83, "+10":70, "+15":57, "+20":45, "-5":64, "-10":43 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  // ---- OCDI · equity · cycle 1 (24 Jun 2026 published study) ----
  {
    instrument:"OCDI", asset_class:"equity",
    anchor_date:"2026-06-24", anchor_price:22.80, ccy:"EGP",
    horizon_label:"T+20", grade_date:"2026-07-21", cycle_no:1, reanchor_from:null,
    p5:18.31, p25:21.08, p50:23.21, p75:25.56, p95:29.35,
    touch:{ "+5":66, "+10":45, "+15":28, "+20":17, "-5":56, "-10":32 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"OCDI", asset_class:"equity",
    anchor_date:"2026-06-24", anchor_price:22.80, ccy:"EGP",
    horizon_label:"T+60", grade_date:"2026-09-22", cycle_no:1, reanchor_from:null,
    p5:16.08, p25:20.38, p50:24.03, p75:28.30, p95:35.79,
    touch:{ "+5":83, "+10":71, "+15":59, "+20":49, "-5":72, "-10":53 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  // ---- ORHD · equity · cycle 1 (25 Jun 2026 published study; anchored 24 Jun) ----
  {
    instrument:"ORHD", asset_class:"equity",
    anchor_date:"2026-06-24", anchor_price:39.30, ccy:"EGP",
    horizon_label:"T+20", grade_date:"2026-07-21", cycle_no:1, reanchor_from:null,
    p5:32.54, p25:36.93, p50:40.22, p75:43.82, p95:49.64,
    touch:{ "+5":60, "+10":43, "+15":28, "+20":16, "-5":48, "-10":28 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"ORHD", asset_class:"equity",
    anchor_date:"2026-06-24", anchor_price:39.30, ccy:"EGP",
    horizon_label:"T+60", grade_date:"2026-09-22", cycle_no:1, reanchor_from:null,
    p5:29.42, p25:36.38, p50:42.10, p75:48.74, p95:59.97,
    touch:{ "+5":80, "+10":70, "+15":58, "+20":47, "-5":62, "-10":46 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  // ---- COMI · equity · cycle 1 (29 Jun 2026 published study) ----
  {
    instrument:"COMI", asset_class:"equity",
    anchor_date:"2026-06-29", anchor_price:129.25, ccy:"EGP",
    horizon_label:"T+20", grade_date:"2026-07-27", cycle_no:1, reanchor_from:null,
    p5:103.44, p25:117.89, p50:128.87, p75:140.85, p95:159.92,
    touch:{ "+5":61, "+10":40, "+15":23, "+20":13, "-5":62, "-10":38 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"COMI", asset_class:"equity",
    anchor_date:"2026-06-29", anchor_price:129.25, ccy:"EGP",
    horizon_label:"T+60", grade_date:"2026-09-21", cycle_no:1, reanchor_from:null,
    p5:87.93, p25:109.91, p50:127.83, p75:148.88, p95:185.40,
    touch:{ "+5":76, "+10":60, "+15":47, "+20":37, "-5":78, "-10":62 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"Gold", asset_class:"metal",
    anchor_date:"2026-06-25", anchor_price:3989.85, ccy:"USD",
    horizon_label:"1 month", grade_date:"2026-07-23", cycle_no:1, reanchor_from:null,
    p5:3431, p25:3754, p50:3975, p75:4214, p95:4598,
    touch:{ "+5":49, "+10":22, "+15":9, "+20":3, "-5":50, "-10":20 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"Gold", asset_class:"metal",
    anchor_date:"2026-06-25", anchor_price:3989.85, ccy:"USD",
    horizon_label:"3 months", grade_date:"2026-09-17", cycle_no:1, reanchor_from:null,
    p5:3064, p25:3560, p50:3944, p75:4369, p95:5074,
    touch:{ "+5":68, "+10":47, "+15":31, "+20":19, "-5":71, "-10":48 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
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
  // ---- Silver (XAG/USD) · metal · cycle 1 (05 Jul 2026 published study; anchored 03 Jul close) ----
  {
    instrument:"Silver", asset_class:"metal",
    anchor_date:"2026-07-03", anchor_price:62.43, ccy:"USD",
    horizon_label:"1 month", grade_date:"2026-07-31", cycle_no:1, reanchor_from:null,
    p5:50, p25:58, p50:63, p75:68, p95:78,
    touch:{ "+5":61, "+10":38, "+15":23, "+20":14, "-5":56, "-10":31 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"Silver", asset_class:"metal",
    anchor_date:"2026-07-03", anchor_price:62.43, ccy:"USD",
    horizon_label:"3 months", grade_date:"2026-09-25", cycle_no:1, reanchor_from:null,
    p5:44, p25:56, p50:63, p75:72, p95:91,
    touch:{ "+5":76, "+10":60, "+15":46, "+20":35, "-5":71, "-10":51 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"Silver", asset_class:"metal",
    anchor_date:"2026-07-03", anchor_price:62.43, ccy:"USD",
    horizon_label:"12 months", grade_date:"2027-07-02", cycle_no:1, reanchor_from:null,
    p5:34, p25:52, p50:67, p75:86, p95:135,
    touch:{ "+5":89, "+10":80, "+15":72, "+20":65, "-5":83, "-10":70 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  // ---- Samsung Electronics (KRX:005930) · other / international · cycle 1 (27 Jun 2026 published study; anchored 26 Jun close) ----
  {
    instrument:"Samsung", asset_class:"other",
    anchor_date:"2026-06-26", anchor_price:339500, ccy:"KRW",
    horizon_label:"T+20", grade_date:"2026-07-24", cycle_no:1, reanchor_from:null,
    p5:277676, p25:316898, p50:346091, p75:378203, p95:430413,
    touch:{ "+5":68, "+10":48, "+15":31, "+20":18, "-5":72, "-10":44 },   // interpolated from the study's absolute touch ladder — replace with the model's exact relative barrier-hit probabilities before these bands are graded
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"Samsung", asset_class:"other",
    anchor_date:"2026-06-26", anchor_price:339500, ccy:"KRW",
    horizon_label:"T+60", grade_date:"2026-09-18", cycle_no:1, reanchor_from:null,
    p5:246827, p25:308298, p50:359482, p75:418176, p95:520627,
    touch:{ "+5":83, "+10":70, "+15":58, "+20":47, "-5":79, "-10":58 },   // interpolated from the study's absolute touch ladder — replace with the model's exact relative barrier-hit probabilities before these bands are graded
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  // ---- Kakao Corp. (KRX:035720) · other / international · cycle 1 (28 Jun 2026 published study; anchored 26 Jun close) ----
  {
    instrument:"Kakao", asset_class:"other",
    anchor_date:"2026-06-26", anchor_price:33150, ccy:"KRW",
    horizon_label:"T+20", grade_date:"2026-07-24", cycle_no:1, reanchor_from:null,
    p5:25404, p25:29799, p50:33294, p75:37199, p95:43634,
    touch:{ "+5":68, "+10":49, "+15":34, "+20":22, "-5":65, "-10":43 },   // relative barrier-hit probabilities from the published model (reflection principle, discrete-monitoring correction)
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"Kakao", asset_class:"other",
    anchor_date:"2026-06-26", anchor_price:33150, ccy:"KRW",
    horizon_label:"T+60", grade_date:"2026-09-18", cycle_no:1, reanchor_from:null,
    p5:21022, p25:27714, p50:33584, p75:40697, p95:53651,
    touch:{ "+5":81, "+10":69, "+15":59, "+20":49, "-5":79, "-10":64 },   // relative barrier-hit probabilities from the published model (reflection principle, discrete-monitoring correction)
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  // ---- LG Energy Solution (KRX:373220) · other / international · cycle 1 (28 Jun 2026 published study; anchored 26 Jun close) ----
  {
    instrument:"LGES", asset_class:"other",
    anchor_date:"2026-06-26", anchor_price:331500, ccy:"KRW",
    horizon_label:"T+20", grade_date:"2026-07-24", cycle_no:1, reanchor_from:null,
    p5:268200, p25:304400, p50:332400, p75:363000, p95:411900,
    touch:{ "+5":62, "+10":40, "+15":24, "+20":13, "-5":60, "-10":34 },   // relative barrier-hit probabilities from the published 50,000-path model (reflection principle, discrete-monitoring correction)
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"LGES", asset_class:"other",
    anchor_date:"2026-06-26", anchor_price:331500, ccy:"KRW",
    horizon_label:"T+60", grade_date:"2026-09-18", cycle_no:1, reanchor_from:null,
    p5:230500, p25:286900, p50:334200, p75:389200, p95:484500,
    touch:{ "+5":78, "+10":63, "+15":50, "+20":39, "-5":75, "-10":58 },   // relative barrier-hit probabilities from the published 50,000-path model (reflection principle, discrete-monitoring correction)
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"CCAP", asset_class:"equity", anchor_date:"2026-06-30", anchor_price:4.77, ccy:"EGP",
    horizon_label:"T+20", grade_date:"2026-07-28", cycle_no:1, reanchor_from:null,
    p5:3.771, p25:4.36, p50:4.809, p75:5.312, p95:6.126,
    touch:{ "+5":66, "+10":45, "+15":30, "+20":19, "-5":61, "-10":38 },   // barrier-hit probabilities from the published 50,000-path model (reflection principle, discrete-monitoring correction)
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"CCAP", asset_class:"equity", anchor_date:"2026-06-30", anchor_price:4.77, ccy:"EGP",
    horizon_label:"T+60", grade_date:"2026-09-22", cycle_no:1, reanchor_from:null,
    p5:3.224, p25:4.126, p50:4.889, p75:5.789, p95:7.391,
    touch:{ "+5":81, "+10":68, "+15":56, "+20":46, "-5":76, "-10":60 },   // barrier-hit probabilities from the published 50,000-path model (reflection principle, discrete-monitoring correction)
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  // ---- OIH · equity · cycle 1 (03 Jul 2026 published study) ----
  {
    instrument:"OIH", asset_class:"equity",
    anchor_date:"2026-07-01", anchor_price:1.41, ccy:"EGP", anchor_vol:0.383, horizon_days:20,
    horizon_label:"T+20", grade_date:"2026-07-29", cycle_no:1, reanchor_from:null,
    p5:1.18, p25:1.35, p50:1.46, p75:1.58, p95:1.80,
    touch:{ "+5":68, "+10":46, "+15":29, "+20":16, "-5":49, "-10":24 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"OIH", asset_class:"equity",
    anchor_date:"2026-07-01", anchor_price:1.41, ccy:"EGP", anchor_vol:0.383, horizon_days:60,
    horizon_label:"T+60", grade_date:"2026-09-23", cycle_no:1, reanchor_from:null,
    p5:1.09, p25:1.36, p50:1.57, p75:1.80, p95:2.23,
    touch:{ "+5":86, "+10":75, "+15":63, "+20":52, "-5":63, "-10":41 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  // ---- ORAS · equity · cycle 1 (30 Jun 2026 published study) ----
  {
    instrument:"ORAS", asset_class:"equity",
    anchor_date:"2026-06-30", anchor_price:720.00, ccy:"EGP",
    horizon_label:"T+20", grade_date:"2026-07-28", cycle_no:1, reanchor_from:null,
    p5:575, p25:658, p50:719, p75:785, p95:893,
    touch:{ "+5":61, "+10":39, "+15":23, "+20":13, "-5":60, "-10":35 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"ORAS", asset_class:"equity",
    anchor_date:"2026-06-30", anchor_price:720.00, ccy:"EGP",
    horizon_label:"T+60", grade_date:"2026-09-22", cycle_no:1, reanchor_from:null,
    p5:488, p25:611, p50:714, p75:834, p95:1040,
    touch:{ "+5":77, "+10":61, "+15":48, "+20":37, "-5":77, "-10":60 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  // ---- TMPV · other (NSE India) · cycle 1 (30 Jun 2026 published study) ----
  {
    instrument:"TMPV", asset_class:"other",
    anchor_date:"2026-06-30", anchor_price:352.20, ccy:"INR",
    horizon_label:"T+20", grade_date:"2026-07-28", cycle_no:1, reanchor_from:null,
    p5:294, p25:327, p50:353, p75:379, p95:422,
    touch:{ "+5":57, "+10":33, "+15":17, "+20":7, "-5":56, "-10":30 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"TMPV", asset_class:"other",
    anchor_date:"2026-06-30", anchor_price:352.20, ccy:"INR",
    horizon_label:"T+60", grade_date:"2026-09-22", cycle_no:1, reanchor_from:null,
    p5:258, p25:310, p50:352, p75:400, p95:481,
    touch:{ "+5":74, "+10":57, "+15":42, "+20":31, "-5":73, "-10":55 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  // ---- ARAMCO · other (TADAWUL Saudi Arabia) · cycle 1 (1 Jul 2026 published study) ----
  {
    instrument:"ARAMCO", asset_class:"other",
    anchor_date:"2026-07-01", anchor_price:26.24, ccy:"SAR",
    horizon_label:"T+20", grade_date:"2026-07-29", cycle_no:1, reanchor_from:null,
    p5:23.80, p25:25.33, p50:26.23, p75:27.13, p95:28.57,
    touch:{ "+5":26, "+10":5, "+15":1, "+20":0, "-5":25, "-10":6 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"ARAMCO", asset_class:"other",
    anchor_date:"2026-07-01", anchor_price:26.24, ccy:"SAR",
    horizon_label:"T+60", grade_date:"2026-09-23", cycle_no:1, reanchor_from:null,
    p5:21.99, p25:24.47, p50:26.12, p75:27.78, p95:30.35,
    touch:{ "+5":51, "+10":24, "+15":10, "+20":3, "-5":52, "-10":25 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"MAADEN", asset_class:"other",
    anchor_date:"2026-07-05", anchor_price:58.80, ccy:"SAR",
    horizon_label:"T+20", grade_date:"2026-08-02", cycle_no:1, reanchor_from:null,
    p5:50.7, p25:55.6, p50:59.2, p75:63.1, p95:69.1,
    touch:{ "+5":54, "+10":34, "+15":18, "+20":9, "-5":45, "-10":22 },
    anchor_vol:0.324, horizon_days:20,
    note:"No CRPS skill vs random-walk benchmark (indicative only) — see study Appendix B.",
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"MAADEN", asset_class:"other",
    anchor_date:"2026-07-05", anchor_price:58.80, ccy:"SAR",
    horizon_label:"T+60", grade_date:"2026-09-27", cycle_no:1, reanchor_from:null,
    p5:46.1, p25:53.9, p50:60.1, p75:67.1, p95:78.4,
    touch:{ "+5":73, "+10":55, "+15":40, "+20":28, "-5":62, "-10":40 },
    anchor_vol:0.324, horizon_days:60,
    note:"No CRPS skill vs random-walk benchmark (indicative only) — see study Appendix B.",
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  // ---- ADNOCGAS · other (ADX Abu Dhabi) · cycle 1 (4 Jul 2026 published study) ----
  {
    instrument:"ADNOCGAS", asset_class:"other",
    anchor_date:"2026-07-03", anchor_price:3.44, ccy:"AED",
    horizon_label:"T+20", grade_date:"2026-07-31", cycle_no:1, reanchor_from:null,
    p5:3.05, p25:3.32, p50:3.45, p75:3.59, p95:3.86,
    touch:{ "+5":34, "+10":12, "+15":4, "+20":1, "-5":28, "-10":9 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"ADNOCGAS", asset_class:"other",
    anchor_date:"2026-07-03", anchor_price:3.44, ccy:"AED",
    horizon_label:"T+60", grade_date:"2026-09-25", cycle_no:1, reanchor_from:null,
    p5:2.83, p25:3.22, p50:3.48, p75:3.75, p95:4.21,
    touch:{ "+5":61, "+10":36, "+15":20, "+20":11, "-5":52, "-10":28 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  // ---- ALRAJHI · other (TADAWUL Saudi Arabia) · cycle 1 (2 Jul 2026 published study) ----
  {
    instrument:"ALRAJHI", asset_class:"other",
    anchor_date:"2026-07-02", anchor_price:66.00, ccy:"SAR",
    horizon_label:"T+20", grade_date:"2026-07-30", cycle_no:1, reanchor_from:null,
    anchor_vol:0.1781, horizon_days:20,
    p5:58.70, p25:63.53, p50:66.08, p75:68.62, p95:73.15,
    touch:{ "+5":32, "+10":9, "+15":3, "+20":1, "-5":29, "-10":9 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"ALRAJHI", asset_class:"other",
    anchor_date:"2026-07-02", anchor_price:66.00, ccy:"SAR",
    horizon_label:"T+60", grade_date:"2026-09-24", cycle_no:1, reanchor_from:null,
    anchor_vol:0.1781, horizon_days:60,
    p5:54.27, p25:61.32, p50:65.95, p75:70.75, p95:78.70,
    touch:{ "+5":57, "+10":31, "+15":16, "+20":8, "-5":54, "-10":29 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  // ---- SNB · other (TADAWUL Saudi Arabia) · cycle 1 (2 Jul 2026 published study) ----
  {
    instrument:"SNB", asset_class:"other",
    anchor_date:"2026-07-02", anchor_price:38.96, ccy:"SAR",
    horizon_label:"T+20", grade_date:"2026-07-30", cycle_no:1, reanchor_from:null,
    anchor_vol:0.2118, horizon_days:20,
    p5:33.75, p25:37.10, p50:39.03, p75:40.93, p95:44.44,
    touch:{ "+5":40, "+10":16, "+15":6, "+20":2, "-5":37, "-10":15 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"SNB", asset_class:"other",
    anchor_date:"2026-07-02", anchor_price:38.96, ccy:"SAR",
    horizon_label:"T+60", grade_date:"2026-09-24", cycle_no:1, reanchor_from:null,
    anchor_vol:0.2118, horizon_days:60,
    p5:30.81, p25:35.62, p50:39.00, p75:42.56, p95:48.66,
    touch:{ "+5":63, "+10":41, "+15":25, "+20":15, "-5":60, "-10":37 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  // ---- ENBD · other (DFM UAE) · cycle 1 (3 Jul 2026 published study) ----
  {
    instrument:"ENBD", asset_class:"other",
    anchor_date:"2026-07-03", anchor_price:30.64, ccy:"AED",
    horizon_label:"T+20", grade_date:"2026-07-31", cycle_no:1, reanchor_from:null,
    anchor_vol:0.45, horizon_days:20,
    p5:23.69, p25:28.14, p50:31.04, p75:34.23, p95:40.59,
    touch:{ "+5":66, "+10":46, "+15":31, "+20":21, "-5":59, "-10":38 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"ENBD", asset_class:"other",
    anchor_date:"2026-07-03", anchor_price:30.64, ccy:"AED",
    horizon_label:"T+60", grade_date:"2026-09-25", cycle_no:1, reanchor_from:null,
    anchor_vol:0.45, horizon_days:60,
    p5:22.31, p25:27.97, p50:31.81, p75:36.15, p95:45.24,
    touch:{ "+5":76, "+10":61, "+15":47, "+20":36, "-5":67, "-10":48 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  // ---- ACWA · other (TADAWUL Saudi Arabia) · cycle 1 (5 Jul 2026 published study) ----
  {
    instrument:"ACWA", asset_class:"other",
    anchor_date:"2026-07-05", anchor_price:193.90, ccy:"SAR",
    horizon_label:"T+20", grade_date:"2026-08-02", cycle_no:1, reanchor_from:null,
    anchor_vol:0.4116, horizon_days:20,
    p5:158.5, p25:180.4, p50:194.1, p75:208.7, p95:235.2,
    touch:{ "+5":56, "+10":32, "+15":17, "+20":9, "-5":54, "-10":28 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"ACWA", asset_class:"other",
    anchor_date:"2026-07-05", anchor_price:193.90, ccy:"SAR",
    horizon_label:"T+60", grade_date:"2026-09-27", cycle_no:1, reanchor_from:null,
    anchor_vol:0.4116, horizon_days:60,
    p5:136.9, p25:171.0, p50:194.2, p75:220.0, p95:268.4,
    touch:{ "+5":73, "+10":56, "+15":42, "+20":30, "-5":72, "-10":52 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  // ---- FAB · other (ADX Abu Dhabi) · cycle 1 (3 Jul 2026 published study) ----
  {
    instrument:"FAB", asset_class:"other",
    anchor_date:"2026-07-03", anchor_price:17.40, ccy:"AED",
    horizon_label:"T+20", grade_date:"2026-07-31", cycle_no:1, reanchor_from:null,
    anchor_vol:0.2404, horizon_days:20,
    p5:14.97, p25:16.44, p50:17.32, p75:18.18, p95:19.75,
    touch:{ "+5":37, "+10":14, "+15":5, "+20":2, "-5":40, "-10":16 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"FAB", asset_class:"other",
    anchor_date:"2026-07-03", anchor_price:17.40, ccy:"AED",
    horizon_label:"T+60", grade_date:"2026-09-25", cycle_no:1, reanchor_from:null,
    anchor_vol:0.2404, horizon_days:60,
    p5:13.37, p25:15.53, p50:17.05, p75:18.59, p95:21.45,
    touch:{ "+5":59, "+10":36, "+15":21, "+20":12, "-5":66, "-10":43 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  // ---- EMAAR · other (DFM Dubai) · cycle 1 (01 Jul 2026 published study) ----
  {
    instrument:"EMAAR", asset_class:"other",
    anchor_date:"2026-06-29", anchor_price:12.14, ccy:"AED",
    horizon_label:"T+20", grade_date:"2026-07-27", cycle_no:1, reanchor_from:null,
    p5:9.98, p25:11.22, p50:12.18, p75:13.22, p95:14.86,
    touch:{ "+5":60, "+10":36, "+15":20, "+20":11, "-5":56, "-10":30 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"EMAAR", asset_class:"other",
    anchor_date:"2026-06-29", anchor_price:12.14, ccy:"AED",
    horizon_label:"T+60", grade_date:"2026-09-21", cycle_no:1, reanchor_from:null,
    p5:8.64, p25:10.62, p50:12.24, p75:14.11, p95:17.32,
    touch:{ "+5":77, "+10":61, "+15":48, "+20":37, "-5":74, "-10":56 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  // ---- TSLA · other (NASDAQ US) · cycle 1 (01 Jul 2026 published study) ----
  {
    instrument:"TSLA", asset_class:"other",
    anchor_date:"2026-06-30", anchor_price:420.60, ccy:"USD",
    horizon_label:"T+20", grade_date:"2026-07-28", cycle_no:1, reanchor_from:null,
    p5:325, p25:379, p50:420, p75:466, p95:541,
    touch:{ "+5":60, "+10":46, "+15":30, "+20":20, "-5":58, "-10":43 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"TSLA", asset_class:"other",
    anchor_date:"2026-06-30", anchor_price:420.60, ccy:"USD",
    horizon_label:"T+60", grade_date:"2026-09-22", cycle_no:1, reanchor_from:null,
    p5:270, p25:350, p50:419, p75:501, p95:647,
    touch:{ "+5":74, "+10":67, "+15":55, "+20":46, "-5":72, "-10":65 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  { instrument:"FWRY", asset_class:"equity", anchor_date:"2026-07-01", anchor_price:18.4, ccy:"EGP",
    horizon_label:"T+20", grade_date:"2026-07-29", cycle_no:1, reanchor_from:null,
    p5:15.45, p25:17.37, p50:18.76, p75:20.22, p95:22.56,
    touch:{ "+5":80, "+10":65, "+15":52, "+20":40, "-5":65, "-10":44 },
    anchor_vol:0.3332, horizon_days:20,
    realized_close:null, realized_high:null, realized_low:null, in_90:null, in_50:null,
    realized_quantile:null, median_err:null, touch_hit:null },
  { instrument:"FWRY", asset_class:"equity", anchor_date:"2026-07-01", anchor_price:18.4, ccy:"EGP",
    horizon_label:"T+60", grade_date:"2026-09-23", cycle_no:1, reanchor_from:null,
    p5:14.05, p25:16.97, p50:19.38, p75:22.09, p95:26.64,
    touch:{ "+5":80, "+10":65, "+15":52, "+20":40, "-5":65, "-10":44 },
    anchor_vol:0.3332, horizon_days:60,
    realized_close:null, realized_high:null, realized_low:null, in_90:null, in_50:null,
    realized_quantile:null, median_err:null, touch_hit:null },
  { instrument:"ABUK", asset_class:"equity", anchor_date:"2026-07-01", anchor_price:67.97, ccy:"EGP",
    horizon_label:"T+20", grade_date:"2026-07-29", cycle_no:1, reanchor_from:null,
    p5:51.67, p25:60.72, p50:67.7, p75:75.45, p95:88.03,
    touch:{ "+5":79, "+10":66, "+15":55, "+20":45, "-5":80, "-10":67 },
    anchor_vol:0.3624, horizon_days:20,
    realized_close:null, realized_high:null, realized_low:null, in_90:null, in_50:null,
    realized_quantile:null, median_err:null, touch_hit:null },
  { instrument:"ADIB", asset_class:"equity", anchor_date:"2026-07-01", anchor_price:46.64, ccy:"EGP",
    horizon_label:"T+20", grade_date:"2026-07-29", cycle_no:1, reanchor_from:null,
    p5:38.5, p25:44.5, p50:48.2, p75:52.2, p95:59.7,
    touch:{ "+5":67, "+10":45, "+15":28, "+20":17, "-5":47, "-10":25 },
    anchor_vol:0.4040, horizon_days:20,
    realized_close:null, realized_high:null, realized_low:null, in_90:null, in_50:null,
    realized_quantile:null, median_err:null, touch_hit:null },
  { instrument:"ADIB", asset_class:"equity", anchor_date:"2026-07-01", anchor_price:46.64, ccy:"EGP",
    horizon_label:"T+60", grade_date:"2026-09-23", cycle_no:1, reanchor_from:null,
    p5:35.3, p25:44.7, p50:51.5, p75:59.3, p95:74.4,
    touch:{ "+5":86, "+10":74, "+15":62, "+20":51, "-5":61, "-10":41 },
    anchor_vol:0.4040, horizon_days:60,
    realized_close:null, realized_high:null, realized_low:null, in_90:null, in_50:null,
    realized_quantile:null, median_err:null, touch_hit:null },
  { instrument:"ABUK", asset_class:"equity", anchor_date:"2026-07-01", anchor_price:67.97, ccy:"EGP",
    horizon_label:"T+60", grade_date:"2026-09-23", cycle_no:1, reanchor_from:null,
    p5:42.38, p25:55.61, p50:66.96, p75:80.83, p95:105.78,
    touch:{ "+5":79, "+10":66, "+15":55, "+20":45, "-5":80, "-10":67 },
    anchor_vol:0.3624, horizon_days:60,
    realized_close:null, realized_high:null, realized_low:null, in_90:null, in_50:null,
    realized_quantile:null, median_err:null, touch_hit:null },
  { instrument:"HRHO", asset_class:"equity", anchor_date:"2026-07-01", anchor_price:26.83, ccy:"EGP",
    horizon_label:"T+20", grade_date:"2026-07-29", cycle_no:1, reanchor_from:null,
    p5:21.22, p25:24.36, p50:26.65, p75:29.06, p95:32.99,
    touch:{ "+5":74, "+10":58, "+15":44, "+20":34, "-5":78, "-10":62 },
    anchor_vol:0.2955, horizon_days:20,
    realized_close:null, realized_high:null, realized_low:null, in_90:null, in_50:null,
    realized_quantile:null, median_err:null, touch_hit:null },
  { instrument:"HRHO", asset_class:"equity", anchor_date:"2026-07-01", anchor_price:26.83, ccy:"EGP",
    horizon_label:"T+60", grade_date:"2026-09-23", cycle_no:1, reanchor_from:null,
    p5:17.87, p25:22.4, p50:26.1, p75:30.33, p95:37.71,
    touch:{ "+5":74, "+10":58, "+15":44, "+20":34, "-5":78, "-10":62 },
    anchor_vol:0.2955, horizon_days:60,
    realized_close:null, realized_high:null, realized_low:null, in_90:null, in_50:null,
    realized_quantile:null, median_err:null, touch_hit:null },
  { instrument:"ORWE", asset_class:"equity", anchor_date:"2026-07-01", anchor_price:22.34, ccy:"EGP",
    horizon_label:"T+20", grade_date:"2026-07-29", cycle_no:1, reanchor_from:null,
    p5:19.84, p25:21.46, p50:22.53, p75:23.66, p95:25.6,
    touch:{ "+5":69, "+10":47, "+15":30, "+20":18, "-5":55, "-10":30 },
    anchor_vol:0.2248, horizon_days:20,
    realized_close:null, realized_high:null, realized_low:null, in_90:null, in_50:null,
    realized_quantile:null, median_err:null, touch_hit:null },
  { instrument:"ORWE", asset_class:"equity", anchor_date:"2026-07-01", anchor_price:22.34, ccy:"EGP",
    horizon_label:"T+60", grade_date:"2026-09-23", cycle_no:1, reanchor_from:null,
    p5:18.42, p25:21.01, p50:22.91, p75:25.01, p95:28.48,
    touch:{ "+5":69, "+10":47, "+15":30, "+20":18, "-5":55, "-10":30 },
    anchor_vol:0.2248, horizon_days:60,
    realized_close:null, realized_high:null, realized_low:null, in_90:null, in_50:null,
    realized_quantile:null, median_err:null, touch_hit:null },
  { instrument:"EGAL", asset_class:"equity", anchor_date:"2026-07-01", anchor_price:285.88, ccy:"EGP",
    horizon_label:"T+20", grade_date:"2026-07-29", cycle_no:1, reanchor_from:null,
    p5:244.5, p25:277.8, p50:298.8, p75:321.2, p95:362.0,
    touch:{ "+5":69, "+10":45, "+15":27, "+20":15, "-5":41, "-10":19 },
    anchor_vol:0.4236, horizon_days:20,
    realized_close:null, realized_high:null, realized_low:null, in_90:null, in_50:null,
    realized_quantile:null, median_err:null, touch_hit:null },
  { instrument:"EGAL", asset_class:"equity", anchor_date:"2026-07-01", anchor_price:285.88, ccy:"EGP",
    horizon_label:"T+60", grade_date:"2026-09-23", cycle_no:1, reanchor_from:null,
    p5:231.5, p25:287.5, p50:326.3, p75:369.4, p95:451.7,
    touch:{ "+5":89, "+10":78, "+15":66, "+20":54, "-5":53, "-10":32 },
    anchor_vol:0.4236, horizon_days:60,
    realized_close:null, realized_high:null, realized_low:null, in_90:null, in_50:null,
    realized_quantile:null, median_err:null, touch_hit:null },
  { instrument:"BTFH", asset_class:"equity", anchor_date:"2026-07-01", anchor_price:2.97, ccy:"EGP",
    horizon_label:"T+20", grade_date:"2026-07-29", cycle_no:1, reanchor_from:null,
    p5:2.39, p25:2.74, p50:2.95, p75:3.17, p95:3.58,
    touch:{ "+5":70, "+10":51, "+15":37, "+20":27, "-5":75, "-10":57 },
    anchor_vol:0.3448, horizon_days:20,
    realized_close:null, realized_high:null, realized_low:null, in_90:null, in_50:null,
    realized_quantile:null, median_err:null, touch_hit:null },
  { instrument:"BTFH", asset_class:"equity", anchor_date:"2026-07-01", anchor_price:2.97, ccy:"EGP",
    horizon_label:"T+60", grade_date:"2026-09-23", cycle_no:1, reanchor_from:null,
    p5:2.04, p25:2.53, p50:2.89, p75:3.29, p95:4.04,
    touch:{ "+5":70, "+10":51, "+15":37, "+20":27, "-5":75, "-10":57 },
    anchor_vol:0.3448, horizon_days:60,
    realized_close:null, realized_high:null, realized_low:null, in_90:null, in_50:null,
    realized_quantile:null, median_err:null, touch_hit:null },
  { instrument:"ETEL", asset_class:"equity", anchor_date:"2026-07-01", anchor_price:92.61, ccy:"EGP",
    horizon_label:"T+20", grade_date:"2026-07-29", cycle_no:1, reanchor_from:null,
    p5:80.7, p25:90.5, p50:96.9, p75:103.7, p95:116.5,
    touch:{"+5": 89, "+10": 78, "+15": 66, "+20": 54, "-5": 49, "-10": 28},
    anchor_vol:0.3830, horizon_days:20,
    realized_close:null, realized_high:null, realized_low:null, in_90:null, in_50:null,
    realized_quantile:null, median_err:null, touch_hit:null },
  { instrument:"ETEL", asset_class:"equity", anchor_date:"2026-07-01", anchor_price:92.61, ccy:"EGP",
    horizon_label:"T+60", grade_date:"2026-09-23", cycle_no:1, reanchor_from:null,
    p5:77.5, p25:94.3, p50:106.3, p75:119.4, p95:145.3,
    touch:{"+5": 89, "+10": 78, "+15": 66, "+20": 54, "-5": 49, "-10": 28},
    anchor_vol:0.3830, horizon_days:60,
    realized_close:null, realized_high:null, realized_low:null, in_90:null, in_50:null,
    realized_quantile:null, median_err:null, touch_hit:null },
  // ---- HELI · equity · cycle 1 (3 Jul 2026 published study) ----
  { instrument:"HELI", asset_class:"equity", anchor_date:"2026-07-03", anchor_price:6.43, ccy:"EGP",
    horizon_label:"T+20", grade_date:"2026-07-29", cycle_no:1, reanchor_from:null,
    p5:5.37, p25:6.09, p50:6.54, p75:7.01, p95:7.89,
    touch:{ "+5":59, "+10":37, "+15":19, "+20":11, "-5":46, "-10":21 },
    anchor_vol:0.382, horizon_days:20,
    realized_close:null, realized_high:null, realized_low:null, in_90:null, in_50:null,
    realized_quantile:null, median_err:null, touch_hit:null },
  { instrument:"HELI", asset_class:"equity", anchor_date:"2026-07-03", anchor_price:6.43, ccy:"EGP",
    horizon_label:"T+60", grade_date:"2026-09-24", cycle_no:1, reanchor_from:null,
    p5:4.84, p25:5.95, p50:6.74, p75:7.60, p95:9.27,
    touch:{ "+5":79, "+10":65, "+15":47, "+20":35, "-5":63, "-10":41 },
    anchor_vol:0.382, horizon_days:60,
    realized_close:null, realized_high:null, realized_low:null, in_90:null, in_50:null,
    realized_quantile:null, median_err:null, touch_hit:null },
  { instrument:"RAYA", asset_class:"equity", anchor_date:"2026-07-01", anchor_price:7.70, ccy:"EGP",
    horizon_label:"T+20", grade_date:"2026-07-29", cycle_no:1, reanchor_from:null,
    p5:5.68, p25:6.90, p50:7.74, p75:8.66, p95:10.48,
    touch:{ "+5":70, "+10":53, "+15":38, "+20":27, "-5":68, "-10":48 },
    anchor_vol:0.6310, horizon_days:20,
    realized_close:null, realized_high:null, realized_low:null, in_90:null, in_50:null,
    realized_quantile:null, median_err:null, touch_hit:null },
  { instrument:"RAYA", asset_class:"equity", anchor_date:"2026-07-01", anchor_price:7.70, ccy:"EGP",
    horizon_label:"T+60", grade_date:"2026-09-23", cycle_no:1, reanchor_from:null,
    p5:4.60, p25:6.40, p50:7.79, p75:9.45, p95:13.06,
    touch:{ "+5":83, "+10":72, "+15":62, "+20":53, "-5":81, "-10":68 },
    anchor_vol:0.6310, horizon_days:60,
    realized_close:null, realized_high:null, realized_low:null, in_90:null, in_50:null,
    realized_quantile:null, median_err:null, touch_hit:null },
  // ---- IHC · other (ADX Abu Dhabi) · cycle 1 (4 Jul 2026 published study) ----
  {
    instrument:"IHC", asset_class:"other",
    anchor_date:"2026-07-03", anchor_price:382.30, ccy:"AED",
    horizon_label:"T+20", grade_date:"2026-07-31", cycle_no:1, reanchor_from:null,
    anchor_vol:0.061, horizon_days:20,
    p5:340.6, p25:376.0, p50:384.4, p75:397.1, p95:427.9,
    touch:{ "+5":27, "+10":10, "+15":3, "+20":1, "-5":19, "-10":8 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"IHC", asset_class:"other",
    anchor_date:"2026-07-03", anchor_price:382.30, ccy:"AED",
    horizon_label:"T+60", grade_date:"2026-09-25", cycle_no:1, reanchor_from:null,
    anchor_vol:0.061, horizon_days:60,
    p5:322.6, p25:364.8, p50:391.3, p75:418.2, p95:462.3,
    touch:{ "+5":58, "+10":33, "+15":17, "+20":8, "-5":42, "-10":20 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  // ---- QNB \u00b7 other (QSE Qatar) \u00b7 cycle 1 (5 Jul 2026 published study) ----
  {
    instrument:"QNB", asset_class:"other",
    anchor_date:"2026-07-05", anchor_price:17.54, ccy:"QAR",
    horizon_label:"T+20", grade_date:"2026-08-02", cycle_no:1, reanchor_from:null,
    anchor_vol:0.18, horizon_days:20,
    p5:15.35, p25:16.74, p50:17.48, p75:18.19, p95:19.55,
    touch:{ "+5":30, "+10":11, "+15":4, "+20":1, "-5":34, "-10":12 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"QNB", asset_class:"other",
    anchor_date:"2026-07-05", anchor_price:17.54, ccy:"QAR",
    horizon_label:"T+60", grade_date:"2026-09-27", cycle_no:1, reanchor_from:null,
    anchor_vol:0.18, horizon_days:60,
    p5:13.96, p25:15.91, p50:17.24, p75:18.60, p95:20.91,
    touch:{ "+5":54, "+10":31, "+15":17, "+20":8, "-5":61, "-10":36 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  // ---- QGTS \u00b7 other (QSE Qatar) \u00b7 cycle 1 (5 Jul 2026 published study; MC ties benchmark, illustrative) ----
  {
    instrument:"QGTS", asset_class:"other",
    anchor_date:"2026-07-05", anchor_price:4.319, ccy:"QAR",
    horizon_label:"T+20", grade_date:"2026-08-02", cycle_no:1, reanchor_from:null,
    anchor_vol:0.23, horizon_days:20,
    note:"No CRPS skill vs random-walk benchmark (indicative only) — see study Appendix B.",
    p5:3.86, p25:4.16, p50:4.34, p75:4.54, p95:4.88,
    touch:{ "+5":42, "+10":17, "+15":7, "+20":3, "-5":39, "-10":13 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"QGTS", asset_class:"other",
    anchor_date:"2026-07-05", anchor_price:4.319, ccy:"QAR",
    horizon_label:"T+60", grade_date:"2026-09-27", cycle_no:1, reanchor_from:null,
    anchor_vol:0.23, horizon_days:60,
    note:"No CRPS skill vs random-walk benchmark (indicative only) — see study Appendix B.",
    p5:3.60, p25:4.08, p50:4.40, p75:4.74, p95:5.36,
    touch:{ "+5":65, "+10":41, "+15":25, "+20":16, "-5":60, "-10":34 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"PRDC", asset_class:"equity",
    anchor_date:"2026-07-06", anchor_price:8.28, ccy:"EGP",
    horizon_label:"T+20", grade_date:"2026-08-03", cycle_no:1, reanchor_from:null,
    p5:6.63, p25:7.74, p50:8.45, p75:9.24, p95:10.68,
    touch:{ "+5":65, "+10":44, "+15":28, "+20":18, "-5":54, "-10":30 },
    anchor_vol:0.4463, horizon_days:20,
    realized_close:null, realized_high:null, realized_low:null, in_90:null, in_50:null,
    realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"PRDC", asset_class:"equity",
    anchor_date:"2026-07-06", anchor_price:8.28, ccy:"EGP",
    horizon_label:"T+60", grade_date:"2026-09-28", cycle_no:1, reanchor_from:null,
    p5:5.86, p25:7.55, p50:8.81, p75:10.25, p95:13.17,
    touch:{ "+5":83, "+10":70, "+15":58, "+20":47, "-5":68, "-10":50 },
    anchor_vol:0.4463, horizon_days:60,
    realized_close:null, realized_high:null, realized_low:null, in_90:null, in_50:null,
    realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  { instrument:"AAPL", asset_class:"other", anchor_date:"2026-07-06", anchor_price:313.09, ccy:"USD",
    horizon_label:"T+20", grade_date:"2026-08-03", cycle_no:1, reanchor_from:null,
    p5:267, p25:293, p50:310, p75:327, p95:356,
    touch:{ "+5":41, "+10":18, "+15":7, "+20":3, "-5":47, "-10":21 },
    anchor_vol:0.2843, horizon_days:20,
    realized_close:null, realized_high:null, realized_low:null, in_90:null, in_50:null,
    realized_quantile:null, median_err:null, touch_hit:null },
  { instrument:"AAPL", asset_class:"other", anchor_date:"2026-07-06", anchor_price:313.09, ccy:"USD",
    horizon_label:"T+60", grade_date:"2026-09-28", cycle_no:1, reanchor_from:null,
    p5:237, p25:276, p50:303, p75:333, p95:386,
    touch:{ "+5":60, "+10":38, "+15":23, "+20":13, "-5":72, "-10":50 },
    anchor_vol:0.2843, horizon_days:60,
    realized_close:null, realized_high:null, realized_low:null, in_90:null, in_50:null,
    realized_quantile:null, median_err:null, touch_hit:null },
  {
    instrument:"ALINMA", asset_class:"other", cal:"matches",
    anchor_date:"2026-07-07", anchor_price:24.00, ccy:"SAR",
    horizon_label:"T+20", grade_date:"2026-08-04", cycle_no:1, reanchor_from:null,
    anchor_vol:0.196, horizon_days:20,
    note:"PARITY under the v3 carry-anchored gate: CRPS skill \u22120.009 vs a carry-anchored random-walk benchmark, bootstrap 90% CI [\u22120.026, +0.018] spans zero, PIT mean 0.485 (n=18 non-overlapping 60-day windows). A calibrated, market-panel-validated distribution \u2014 no single-name edge demonstrated, and none claimed. Carry-anchored drift: rf \u2248 dividend yield, so the expected total return arrives as dividend and the price path is an explained flat. Saudi names run carry-only until the Tadawul panel reaches ~5 names.",
    p5:22.1, p25:23.31, p50:24.00, p75:24.7, p95:26.09,
    touch:{ "+5":23, "+10":6, "+15":2, "+20":1, "-5":22, "-10":4 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"ALINMA", asset_class:"other", cal:"matches",
    anchor_date:"2026-07-07", anchor_price:24.00, ccy:"SAR",
    horizon_label:"T+60", grade_date:"2026-09-29", cycle_no:1, reanchor_from:null,
    anchor_vol:0.196, horizon_days:60,
    note:"PARITY under the v3 carry-anchored gate: CRPS skill \u22120.009 vs a carry-anchored random-walk benchmark, bootstrap 90% CI [\u22120.026, +0.018] spans zero, PIT mean 0.485 (n=18 non-overlapping 60-day windows). A calibrated, market-panel-validated distribution \u2014 no single-name edge demonstrated, and none claimed. Carry-anchored drift: rf \u2248 dividend yield, so the expected total return arrives as dividend and the price path is an explained flat. Saudi names run carry-only until the Tadawul panel reaches ~5 names.",
    p5:20.76, p25:22.82, p50:24.00, p75:25.24, p95:27.7,
    touch:{ "+5":47, "+10":21, "+15":10, "+20":5, "-5":45, "-10":18 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"ELM", asset_class:"other", cal:"matches",
    anchor_date:"2026-07-07", anchor_price:658.50, ccy:"SAR",
    horizon_label:"T+20", grade_date:"2026-08-04", cycle_no:1, reanchor_from:null,
    anchor_vol:0.3338, horizon_days:20,
    note:"PARITY under the v3 carry-anchored gate on Saudi-fitted shape/width (ν=5, cone width 1.28): CRPS skill \u22120.003 vs a carry-anchored random-walk benchmark, bootstrap 90% CI [\u22120.028, +0.016] spans zero, 0.77 band-90 coverage on n=13 non-overlapping 60-day windows. A calibrated, market-panel-validated distribution \u2014 no single-name edge demonstrated, and none claimed. Saudi shape/width was FITTED on the Tadawul panel (Alinma+Ma\u0027aden), not borrowed from another market \u2014 the borrowed-Egypt archetype had manufactured a false FAIL. Carry-anchored drift (rf 4.60% 1yr Sah govt sukuk \u2212 1.3% dividend yield); Saudi names run carry-only until the Tadawul panel reaches ~5 names.",
    p5:543, p25:610, p50:660, p75:715, p95:803,
    touch:{ "+5":58, "+10":35, "+15":19, "+20":10, "-5":55, "-10":29 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"ELM", asset_class:"other", cal:"matches",
    anchor_date:"2026-07-07", anchor_price:658.50, ccy:"SAR",
    horizon_label:"T+60", grade_date:"2026-09-29", cycle_no:1, reanchor_from:null,
    anchor_vol:0.3338, horizon_days:60,
    note:"PARITY under the v3 carry-anchored gate on Saudi-fitted shape/width (ν=5, cone width 1.28): CRPS skill \u22120.003 vs a carry-anchored random-walk benchmark, bootstrap 90% CI [\u22120.028, +0.016] spans zero, 0.77 band-90 coverage on n=13 non-overlapping 60-day windows. A calibrated, market-panel-validated distribution \u2014 no single-name edge demonstrated, and none claimed. Saudi shape/width was FITTED on the Tadawul panel (Alinma+Ma\u0027aden), not borrowed from another market \u2014 the borrowed-Egypt archetype had manufactured a false FAIL. Carry-anchored drift (rf 4.60% 1yr Sah govt sukuk \u2212 1.3% dividend yield); Saudi names run carry-only until the Tadawul panel reaches ~5 names.",
    p5:471, p25:577, p50:664, p75:763, p95:934,
    touch:{ "+5":76, "+10":60, "+15":46, "+20":35, "-5":73, "-10":54 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"ALPHADHABI", asset_class:"other", cal:"matches",
    anchor_date:"2026-07-03", anchor_price:8.22, ccy:"AED",
    horizon_label:"T+20", grade_date:"2026-07-31", cycle_no:1, reanchor_from:null,
    anchor_vol:0.341, horizon_days:20,
    cal:"matches",
    note:"PARITY under the fitted UAE market profile (9-name ADX/DFM panel, fat-tailed t/4 d.o.f., cone width 1.07). Name-level CRPS skill roughly +0.7\u20130.9% vs a carry-anchored random-walk benchmark with the bootstrap 90% CI spanning zero, robust across block sizes {2,3,4} \u2014 a calibrated distribution, no single-name edge demonstrated or claimed. This name was folded in as the 10th panel member (its OHLC supplied 10-Jul), which CONFIRMS the fit at nu=4/cal=1.077; it supersedes the provisional 1-name Gaussian self-fit (cone width 1.042) the study was published under. Carry-anchored drift: 3M EIBOR 3.93%, no ex-dividend date in the window (q=0). TIMING FLAG: the anchor pre-dates the 7\u20138 Jul ceasefire collapse \u2014 this cohort will be graded inside the war-regime window; outlier-triggered out-of-cycle review applies if structurally surprising.",
    p5:7.04, p25:7.73, p50:8.24, p75:8.79, p95:9.67,
    touch:{ "+5":54, "+10":27, "+15":12, "+20":5, "-5":50, "-10":21 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"ALPHADHABI", asset_class:"other", cal:"matches",
    anchor_date:"2026-07-03", anchor_price:8.22, ccy:"AED",
    horizon_label:"T+60", grade_date:"2026-09-25", cycle_no:1, reanchor_from:null,
    anchor_vol:0.341, horizon_days:60,
    cal:"matches",
    note:"PARITY under the fitted UAE market profile (9-name ADX/DFM panel, fat-tailed t/4 d.o.f., cone width 1.07). Name-level CRPS skill roughly +0.7\u20130.9% vs a carry-anchored random-walk benchmark with the bootstrap 90% CI spanning zero, robust across block sizes {2,3,4} \u2014 a calibrated distribution, no single-name edge demonstrated or claimed. This name was folded in as the 10th panel member (its OHLC supplied 10-Jul), which CONFIRMS the fit at nu=4/cal=1.077; it supersedes the provisional 1-name Gaussian self-fit (cone width 1.042) the study was published under. Carry-anchored drift: 3M EIBOR 3.93%, no ex-dividend date in the window (q=0). TIMING FLAG: the anchor pre-dates the 7\u20138 Jul ceasefire collapse \u2014 this cohort will be graded inside the war-regime window; outlier-triggered out-of-cycle review applies if structurally surprising.",
    p5:6.30, p25:7.42, p50:8.29, p75:9.27, p95:10.93,
    touch:{ "+5":73, "+10":54, "+15":38, "+20":26, "-5":69, "-10":46 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"EXTRA", asset_class:"other", cal:"matches",
    anchor_date:"2026-07-09", anchor_price:68.10, ccy:"SAR",
    horizon_label:"T+20", grade_date:"2026-08-06", cycle_no:1, reanchor_from:null,
    anchor_vol:0.316, horizon_days:20,
    note:"PARITY under the v3 carry-anchored gate. Name-level CRPS skill −0.050 vs a carry-anchored random-walk benchmark, bootstrap 90% CI [−0.140, +0.007] spans zero; the Saudi market panel (Alinma + Ma'aden + eXtra, n=54) is PARITY at −0.021, CI [−0.050, +0.005], PIT 0.500. A calibrated, market-panel-validated distribution — no single-name edge demonstrated, and none claimed. Carry-anchored drift: the ~6.9% dividend yield exceeds the ~4.25% risk-free, so the price median is an explained flat (slightly below spot), with the return delivered as dividend. Saudi shape/width fitted on the Tadawul panel (ν=5, cone width=1.28); carry-only until ~5 names.",
    p5:59.2, p25:64.6, p50:67.9, p75:71.4, p95:78.2,
    touch:{ "+5":42, "+10":18, "+15":7, "+20":3, "-5":42, "-10":16 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
  {
    instrument:"EXTRA", asset_class:"other", cal:"matches",
    anchor_date:"2026-07-09", anchor_price:68.10, ccy:"SAR",
    horizon_label:"T+60", grade_date:"2026-10-04", cycle_no:1, reanchor_from:null,
    anchor_vol:0.316, horizon_days:60,
    note:"PARITY under the v3 carry-anchored gate. Name-level CRPS skill −0.050 vs a carry-anchored random-walk benchmark, bootstrap 90% CI [−0.140, +0.007] spans zero; the Saudi market panel (Alinma + Ma'aden + eXtra, n=54) is PARITY at −0.021, CI [−0.050, +0.005], PIT 0.500. A calibrated, market-panel-validated distribution — no single-name edge demonstrated, and none claimed. Carry-anchored drift: the ~6.9% dividend yield exceeds the ~4.25% risk-free, so the price median is an explained flat (slightly below spot), with the return delivered as dividend. Saudi shape/width fitted on the Tadawul panel (ν=5, cone width=1.28); carry-only until ~5 names.",
    p5:53.3, p25:62.0, p50:67.6, p75:73.8, p95:86.2,
    touch:{ "+5":63, "+10":40, "+15":25, "+20":16, "-5":65, "-10":39 },
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }
  },
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
  {anchor_date:"2021-06-01", instrument:"PHDC", horizon_label:"T+60", p5:1.184, p50:1.832, p95:2.837, realized_close:1.995, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2021-09-01", instrument:"PHDC", horizon_label:"T+60", p5:1.407, p50:2.179, p95:3.373, realized_close:1.766, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2021-11-28", instrument:"PHDC", horizon_label:"T+60", p5:1.246, p50:1.928, p95:2.985, realized_close:1.614, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2022-02-22", instrument:"PHDC", horizon_label:"T+60", p5:1.138, p50:1.762, p95:2.729, realized_close:1.169, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2022-05-26", instrument:"PHDC", horizon_label:"T+60", p5:0.825, p50:1.277, p95:1.976, realized_close:1.4, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2022-08-28", instrument:"PHDC", horizon_label:"T+60", p5:0.988, p50:1.529, p95:2.367, realized_close:1.649, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2022-11-21", instrument:"PHDC", horizon_label:"T+60", p5:1.163, p50:1.801, p95:2.788, realized_close:2.16, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2023-02-16", instrument:"PHDC", horizon_label:"T+60", p5:1.524, p50:2.359, p95:3.652, realized_close:1.843, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2023-05-22", instrument:"PHDC", horizon_label:"T+60", p5:1.3, p50:2.013, p95:3.116, realized_close:1.962, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2023-08-23", instrument:"PHDC", horizon_label:"T+60", p5:1.384, p50:2.142, p95:3.317, realized_close:2.87, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2023-11-19", instrument:"PHDC", horizon_label:"T+60", p5:2.024, p50:3.134, p95:4.852, realized_close:3.69, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2024-02-14", instrument:"PHDC", horizon_label:"T+60", p5:2.603, p50:4.029, p95:6.238, realized_close:3.32, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2024-05-19", instrument:"PHDC", horizon_label:"T+60", p5:2.342, p50:3.625, p95:5.613, realized_close:5.2, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2024-08-21", instrument:"PHDC", horizon_label:"T+60", p5:3.668, p50:5.678, p95:8.791, realized_close:5.7, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2024-11-17", instrument:"PHDC", horizon_label:"T+60", p5:4.021, p50:6.224, p95:9.636, realized_close:6.1, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2025-02-11", instrument:"PHDC", horizon_label:"T+60", p5:4.303, p50:6.661, p95:10.312, realized_close:6.79, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2025-05-18", instrument:"PHDC", horizon_label:"T+60", p5:4.789, p50:7.415, p95:11.479, realized_close:7.96, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2025-08-19", instrument:"PHDC", horizon_label:"T+60", p5:5.615, p50:8.692, p95:13.457, realized_close:8.18, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2025-11-13", instrument:"PHDC", horizon_label:"T+60", p5:5.77, p50:8.932, p95:13.829, realized_close:8.89, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2026-02-10", instrument:"PHDC", horizon_label:"T+60", p5:6.271, p50:9.708, p95:15.029, realized_close:14.0, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2021-06-01", instrument:"TMGH", horizon_label:"T+60", p5:4.516, p50:6.224, p95:8.579, realized_close:7.43, in_90:true, evidence:"in-sample"},
  {anchor_date:"2021-09-01", instrument:"TMGH", horizon_label:"T+60", p5:5.845, p50:8.057, p95:11.105, realized_close:7.99, in_90:true, evidence:"in-sample"},
  {anchor_date:"2021-11-28", instrument:"TMGH", horizon_label:"T+60", p5:6.286, p50:8.664, p95:11.942, realized_close:9.5, in_90:true, evidence:"in-sample"},
  {anchor_date:"2022-02-22", instrument:"TMGH", horizon_label:"T+60", p5:7.474, p50:10.302, p95:14.199, realized_close:7.55, in_90:true, evidence:"in-sample"},
  {anchor_date:"2022-05-26", instrument:"TMGH", horizon_label:"T+60", p5:5.94, p50:8.187, p95:11.284, realized_close:7.73, in_90:true, evidence:"in-sample"},
  {anchor_date:"2022-08-28", instrument:"TMGH", horizon_label:"T+60", p5:6.081, p50:8.382, p95:11.553, realized_close:8.53, in_90:true, evidence:"in-sample"},
  {anchor_date:"2022-11-21", instrument:"TMGH", horizon_label:"T+60", p5:6.711, p50:9.25, p95:12.749, realized_close:9.99, in_90:true, evidence:"in-sample"},
  {anchor_date:"2023-02-16", instrument:"TMGH", horizon_label:"T+60", p5:7.859, p50:10.833, p95:14.931, realized_close:8.54, in_90:true, evidence:"in-sample"},
  {anchor_date:"2023-05-22", instrument:"TMGH", horizon_label:"T+60", p5:6.719, p50:9.261, p95:12.764, realized_close:10.3, in_90:true, evidence:"in-sample"},
  {anchor_date:"2023-08-23", instrument:"TMGH", horizon_label:"T+60", p5:8.103, p50:11.169, p95:15.395, realized_close:24.86, in_90:false, evidence:"in-sample"},
  {anchor_date:"2023-11-19", instrument:"TMGH", horizon_label:"T+60", p5:19.558, p50:26.957, p95:37.156, realized_close:44.42, in_90:false, evidence:"in-sample"},
  {anchor_date:"2024-02-14", instrument:"TMGH", horizon_label:"T+60", p5:34.946, p50:48.168, p95:66.391, realized_close:60.9, in_90:true, evidence:"in-sample"},
  {anchor_date:"2024-05-19", instrument:"TMGH", horizon_label:"T+60", p5:47.912, p50:66.038, p95:91.023, realized_close:55.92, in_90:true, evidence:"in-sample"},
  {anchor_date:"2024-08-21", instrument:"TMGH", horizon_label:"T+60", p5:43.994, p50:60.638, p95:83.58, realized_close:60.7, in_90:true, evidence:"in-sample"},
  {anchor_date:"2024-11-17", instrument:"TMGH", horizon_label:"T+60", p5:47.754, p50:65.821, p95:90.724, realized_close:50.9, in_90:true, evidence:"in-sample"},
  {anchor_date:"2025-02-11", instrument:"TMGH", horizon_label:"T+60", p5:40.044, p50:55.194, p95:76.077, realized_close:53.0, in_90:true, evidence:"in-sample"},
  {anchor_date:"2025-05-18", instrument:"TMGH", horizon_label:"T+60", p5:41.696, p50:57.472, p95:79.215, realized_close:55.21, in_90:true, evidence:"in-sample"},
  {anchor_date:"2025-08-19", instrument:"TMGH", horizon_label:"T+60", p5:43.435, p50:59.868, p95:82.518, realized_close:71.6, in_90:true, evidence:"in-sample"},
  {anchor_date:"2025-11-13", instrument:"TMGH", horizon_label:"T+60", p5:56.329, p50:77.641, p95:107.015, realized_close:88.97, in_90:true, evidence:"in-sample"},
  {anchor_date:"2026-02-10", instrument:"TMGH", horizon_label:"T+60", p5:69.995, p50:96.476, p95:132.977, realized_close:97.51, in_90:true, evidence:"in-sample"},
  {anchor_date:"2021-06-01", instrument:"EMFD", horizon_label:"T+60", p5:1.684, p50:2.335, p95:3.238, realized_close:2.46, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2021-09-01", instrument:"EMFD", horizon_label:"T+60", p5:1.909, p50:2.647, p95:3.67, realized_close:2.58, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2021-11-28", instrument:"EMFD", horizon_label:"T+60", p5:2.002, p50:2.776, p95:3.849, realized_close:2.74, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2022-02-22", instrument:"EMFD", horizon_label:"T+60", p5:2.126, p50:2.948, p95:4.088, realized_close:2.63, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2022-05-26", instrument:"EMFD", horizon_label:"T+60", p5:2.041, p50:2.83, p95:3.924, realized_close:2.7, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2022-08-28", instrument:"EMFD", horizon_label:"T+60", p5:2.095, p50:2.905, p95:4.029, realized_close:2.66, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2022-11-21", instrument:"EMFD", horizon_label:"T+60", p5:2.064, p50:2.862, p95:3.969, realized_close:3.15, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2023-02-16", instrument:"EMFD", horizon_label:"T+60", p5:2.444, p50:3.389, p95:4.7, realized_close:2.79, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2023-05-22", instrument:"EMFD", horizon_label:"T+60", p5:2.165, p50:3.002, p95:4.163, realized_close:2.98, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2023-08-23", instrument:"EMFD", horizon_label:"T+60", p5:2.312, p50:3.206, p95:4.446, realized_close:3.75, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2023-11-19", instrument:"EMFD", horizon_label:"T+60", p5:2.91, p50:4.035, p95:5.595, realized_close:6.55, in_90:false, evidence:"quasi-OOS"},
  {anchor_date:"2024-02-14", instrument:"EMFD", horizon_label:"T+60", p5:5.083, p50:7.048, p95:9.773, realized_close:5.95, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2024-05-19", instrument:"EMFD", horizon_label:"T+60", p5:4.617, p50:6.402, p95:8.878, realized_close:6.99, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2024-08-21", instrument:"EMFD", horizon_label:"T+60", p5:5.424, p50:7.521, p95:10.429, realized_close:8.29, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2024-11-17", instrument:"EMFD", horizon_label:"T+60", p5:6.433, p50:8.92, p95:12.369, realized_close:6.68, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2025-02-11", instrument:"EMFD", horizon_label:"T+60", p5:5.183, p50:7.188, p95:9.967, realized_close:9.1, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2025-05-18", instrument:"EMFD", horizon_label:"T+60", p5:7.061, p50:9.792, p95:13.578, realized_close:8.47, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2025-08-19", instrument:"EMFD", horizon_label:"T+60", p5:6.572, p50:9.114, p95:12.638, realized_close:10.0, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2025-11-13", instrument:"EMFD", horizon_label:"T+60", p5:7.76, p50:10.76, p95:14.921, realized_close:9.7, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2026-02-10", instrument:"EMFD", horizon_label:"T+60", p5:7.527, p50:10.437, p95:14.473, realized_close:11.1, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2022-02-22", instrument:"PRDC", horizon_label:"T+60", p5:1.417, p50:2.047, p95:2.929, realized_close:1.71, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2022-05-26", instrument:"PRDC", horizon_label:"T+60", p5:1.136, p50:1.717, p95:2.565, realized_close:1.83, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2022-08-28", instrument:"PRDC", horizon_label:"T+60", p5:1.215, p50:1.837, p95:2.747, realized_close:1.83, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2022-11-21", instrument:"PRDC", horizon_label:"T+60", p5:1.361, p50:1.835, p95:2.455, realized_close:2.15, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2023-02-16", instrument:"PRDC", horizon_label:"T+60", p5:1.537, p50:2.157, p95:3.0, realized_close:1.96, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2023-05-22", instrument:"PRDC", horizon_label:"T+60", p5:1.397, p50:1.966, p95:2.743, realized_close:2.01, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2023-08-23", instrument:"PRDC", horizon_label:"T+60", p5:1.398, p50:2.017, p95:2.882, realized_close:2.14, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2023-11-19", instrument:"PRDC", horizon_label:"T+60", p5:1.547, p50:2.146, p95:2.954, realized_close:3.24, in_90:false, evidence:"quasi-OOS"},
  {anchor_date:"2024-02-14", instrument:"PRDC", horizon_label:"T+60", p5:2.248, p50:3.251, p95:4.657, realized_close:2.5, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2024-05-19", instrument:"PRDC", horizon_label:"T+60", p5:1.726, p50:2.509, p95:3.611, realized_close:3.04, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2024-08-21", instrument:"PRDC", horizon_label:"T+60", p5:2.133, p50:3.05, p95:4.321, realized_close:3.4, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2024-11-17", instrument:"PRDC", horizon_label:"T+60", p5:2.459, p50:3.421, p95:4.718, realized_close:3.18, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2025-02-11", instrument:"PRDC", horizon_label:"T+60", p5:2.334, p50:3.189, p95:4.323, realized_close:3.32, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2025-05-18", instrument:"PRDC", horizon_label:"T+60", p5:2.511, p50:3.332, p95:4.389, realized_close:3.35, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2025-08-19", instrument:"PRDC", horizon_label:"T+60", p5:2.501, p50:3.364, p95:4.491, realized_close:3.85, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2025-11-13", instrument:"PRDC", horizon_label:"T+60", p5:2.827, p50:3.9, p95:5.334, realized_close:4.27, in_90:true, evidence:"quasi-OOS"},
  {anchor_date:"2026-02-10", instrument:"PRDC", horizon_label:"T+60", p5:3.091, p50:4.349, p95:6.066, realized_close:5.73, in_90:true, evidence:"quasi-OOS"},
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
 name:"Gold", code:"XAU/USD", spot:3989.85, spotDate:"close 25 Jun 2026", ccy:"USD",
 fair:{ bear:4200, base:4600, full:5000 },
 dist:{
   t20:{ label:"1 month (T+20)",  p5:3431, p25:3754, p50:3975, p75:4214, p95:4598, resolve:"2026-07-23" },
   t60:{ label:"3 months (T+60)", p5:3064, p25:3560, p50:3944, p75:4369, p95:5074, resolve:"2026-09-17" },
   t252:{ label:"12 months (T+252)", p5:2624, p25:3515, p50:4295, p75:5246, p95:7026, resolve:"2027-06-25" }
 },
 touch:[ [4800,3,19], [4600,8,30], [4500,13,37], [4300,32,55], [4200,47,66], [3800,52,72], [3700,35,60], [3600,21,49], [3500,12,39] ],
 levels:{ res:[4200,4470,4487], sup:[3700,3600,3500] },
 tech:{
   trend:"Broken below both averages \u2014 oversold, with a fresh death-cross",
   summary:"Gold closed $3,989.85 after a ~29% correction from a $5,595 all-time high in January 2026. Price sits ~11% below both the 50- and 200-day moving averages, MACD (12\u00b726\u00b79) is negative (\u2212121.3 / \u2212105.0 / \u221216.3) and RSI(14) is ~30 \u2014 oversold. Crucially the 50-day has just crossed beneath the 200-day for the first time this cycle: a fresh death-cross and a momentum-regime change, not a pullback inside an intact uptrend.",
   bull:"Stabilising real rates and a structural central-bank bid lift gold back toward the $4,200\u20134,600 consensus zone; reclaiming the $4,470 / $4,487 averages would confirm.",
   bear:"A confirmed September Fed hike and a stronger dollar extend the correction toward $3,700 \u2192 $3,600 \u2192 $3,500 and the $3,268 52-week low."
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
 name:"Silver", code:"XAG/USD", spot:62.43, spotDate:"close 03 Jul 2026", ccy:"USD",
 fair:{ bear:58, base:68, full:78 },
 dist:{
   t20:{ label:"1 month (T+20)",  p5:50, p25:58, p50:63, p75:68, p95:78, resolve:"2026-07-31" },
   t60:{ label:"3 months (T+60)", p5:44, p25:56, p50:63, p75:72, p95:91, resolve:"2026-09-25" },
   t252:{ label:"12 months (T+252)", p5:34, p25:52, p50:67, p75:86, p95:135, resolve:"2027-07-02" }
 },
 touch:[ [85,3,14], [78,9,26], [72,22,45], [68,42,63], [58,45,62], [55,25,44], [50,8,22], [45,2,10] ],
 levels:{ res:[68,71,78], sup:[58,55,50] },
 tech:{
   trend:"Corrective below all major averages \\u2014 RSI recovering from oversold, a death-cross approaching",
   summary:"Silver closed $62.43 after the most violent year in its modern history \\u2014 a run from the high-$30s to an intraday all-time high near $121 in late January 2026, then a halving back to the low-$60s as the war premium unwound and the Fed turned hawkish. Price sits ~12% below both the 50- and 200-day moving averages, MACD (12\\u00b726\\u00b79) is negative (\\u22123.37 / \\u22123.67 / +0.30) but its histogram has just turned up, and RSI(14) is ~44 \\u2014 neutral, off oversold. The 50-day is still fractionally above the 200-day, but with price well below both and the halving so recent, a death-cross is the more likely next structural event.",
   bull:"Gold-silver ratio compression toward 55\\u201350\\u00d7 and a gold reversion toward its own consensus zone lift silver toward $72\\u201380; reclaiming the ~$71 (SMA50) average would confirm.",
   bear:"A confirmed Fed hike and a stronger dollar, plus a positioning/ETF unwind, extend the fall toward $55 \\u2192 $50 \\u2192 the mid-$40s (J.P. Morgan flags $50)."
 },
 files:{
   study:"files/XAGUSD_Combined_1-3-12M_Valuation_Study_05-07-2026_public.docx?v=2607",
   model:"files/XAGUSD_Combined_1-3-12M_Valuation_Model_05-07-2026_public.xlsx?v=2607",
   pdf:"files/XAGUSD_Combined_1-3-12M_Valuation_Study_05-07-2026_public.pdf?v=2607"
 }
  }
};
