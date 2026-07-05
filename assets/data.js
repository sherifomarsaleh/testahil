/* =========================================================
   testahil — the ONLY file you edit in the weekly ritual.
   ========================================================= */

const SITE = { updated: "2026-07-05" };

/* ---------- covered tickers ---------- */
const TICKERS = {
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
