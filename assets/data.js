/* =========================================================
   testahil — the ONLY file you edit in the weekly ritual.
   ========================================================= */

const SITE = { updated: "2026-06-29" };

/* ---------- covered tickers ---------- */
const TICKERS = {
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
  }
};

/* coming-soon cards (home page coverage section) */
const COMING = [
  { code:"EGX:TMGH", name:"Talaat Moustafa Group",        url:"tmgh.html", status:"covered" },
  { code:"EGX:EMFD", name:"Emaar Misr for Development",        url:"emfd.html", status:"covered" },
  { code:"EGX:OCDI", name:"SODIC",                            url:"ocdi.html", status:"covered" },
  { code:"EGX:ORHD", name:"Orascom Development",          url:"orhd.html", status:"covered" },
  { code:"EGX:ORAS", name:"Orascom Construction",          url:null,        status:"soon" },
  { code:"EGX:COMI", name:"Commercial International Bank", url:"comi.html", status:"covered" },
  { code:"EGX:CCAP", name:"Citadel Capital",                 url:null,        status:"soon" },
  { code:"EGX:FWRY", name:"Fawry",                            url:null,        status:"soon" },
  { code:"EGX:HELI", name:"Heliopolis Housing",              url:null,        status:"soon" },
  { code:"EGX:BTFH", name:"Beltone",                          url:null,        status:"soon" },
  { code:"EGX:ABUK", name:"Abu Kir Fertilizers",             url:null,        status:"soon" },
  { code:"EGX:EFID", name:"Edita",                            url:null,        status:"soon" },
  { code:"EGX:HRHO", name:"EFG Holding",                      url:null,        status:"soon" },
  { code:"EGX:MFPC", name:"MOPCO",                            url:null,        status:"soon" },
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
  }
};
