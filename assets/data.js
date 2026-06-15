/* =========================================================
   testahil — the ONLY file you edit in the weekly ritual.
   ========================================================= */

const SITE = { updated: "2026-06-15" };

/* ---------- covered tickers ---------- */
const TICKERS = {
  PHDC: {
    name: "Palm Hills Developments",
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
    code: "EGX:TMGH",
    spot: 95.68,
    spotDate: "close 14 Jun 2026",
    ccy: "EGP",
    fair: { bear: 83.6, base: 147.12, full: 189.6 },
    dist: {
      t20: { label:"1 month (T+20)",  p5:81.42, p25:91.17, p50:98.31,  p75:106.10, p95:119.24, resolve:"2026-07-14" },
      t60: { label:"3 months (T+60)", p5:75.58, p25:91.20, p50:103.93, p75:118.41, p95:142.75, resolve:"2026-09-08" }
    },
    touch: [ /* descending high → low */
      [126, 2, 24], [118, 8, 39], [110, 24, 58], [100, 66, 85], [88, 29, 48], [83, 11, 29]
    ],
    levels: { res:[101.40, 99.45, 96.10], sup:[92.16, 91.55, 86.56] },
    tech: {
      trend: "Recovering — bounce off the 50-day on rising volume",
      summary: "After a pullback, the price found a floor at its rising 50-day average and bounced back on the heaviest buying in two weeks. Momentum is turning back up (RSI recovering, the daily MACD narrowing), and the price has reclaimed its short-term average — a correction that's resolving back upward inside an intact uptrend.",
      bull: "A daily close above 97.40 confirms the recovery is back on.",
      bear: "A close below 91.55 reopens the lower supports at 88 and 83."
    },
    files: {
      study: "files/TMGH_Valuation_Study_15-06-2026_public.docx?v=1506",
      model: "files/TMGH_Valuation_Study_15-06-2026_public.xlsx?v=1506",
      pdf:   "files/TMGH_Valuation_Study_15-06-2026_public.pdf?v=1506"
    }
  }
};

/* coming-soon cards (home page coverage section) */
const COMING = [
  { code:"EGX:TMGH", name:"Talaat Moustafa Group",        url:"tmgh.html", status:"covered" },
  { code:"EGX:ORAS", name:"Orascom Construction",          url:null,        status:"soon" },
  { code:"EGX:COMI", name:"Commercial International Bank", url:null,        status:"soon" },
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
const LEDGER = [
  { pub:"2026-06-09", inst:"PHDC", horizon:"T+20", median:15.44, lo:11.93, hi:19.99, band:"90%", resolve:"2026-07-07", status:"open", realized:null },
  { pub:"2026-06-09", inst:"PHDC", horizon:"T+60", median:16.37, lo:10.53, hi:25.35, band:"90%", resolve:"2026-09-02", status:"open", realized:null },
  { pub:"2026-06-11", inst:"PHDC", horizon:"T+20", median:14.92, lo:11.53, hi:19.32, band:"90%", resolve:"2026-07-09", status:"open", realized:null },
  { pub:"2026-06-11", inst:"PHDC", horizon:"T+60", median:15.83, lo:10.18, hi:24.50, band:"90%", resolve:"2026-09-03", status:"open", realized:null },
  { pub:"2026-06-15", inst:"TMGH", horizon:"T+20", median:98.31,  lo:81.42, hi:119.24, band:"90%", resolve:"2026-07-14", status:"open", realized:null },
  { pub:"2026-06-15", inst:"TMGH", horizon:"T+60", median:103.93, lo:75.58, hi:142.75, band:"90%", resolve:"2026-09-08", status:"open", realized:null }
];

/* ---------- calculator data ----------
   Verified 11 Jun 2026 (end-of-year values). Sources:
   usdEgp: CBE / FocusEconomics (2023:30.93, 2024:50.83, 2025:~47.45)
   egx30: EGX official annual table via Wikipedia (1996-2023) + 31 Dec 2025 close 41,828.97; 2024 ~29,661 (+19.5%)
   inflation: CAPMAS/CBE annual average urban headline (2024:28.3, 2025:~14.0 per CBE)
   gold21g: local sagha quotes; 31 Dec 2025 = 5,910 EGP/g (Dostor). 2022-23 embed the
            parallel-FX premium (that's what buyers actually paid). Pre-2024 values are
            best-effort archival reconstructions (+/-5%).
   cdRate: best available 1-yr fixed CD per year (NBE/BM announcements) - archival approx. */
const CALC = {
  verified: true,
  years: [2015,2016,2017,2018,2019,2020,2021,2022,2023,2024,2025],
  usdEgp:   [7.83, 18.12, 17.78, 17.92, 16.05, 15.73, 15.72, 24.72, 30.93, 50.83, 47.45],
  gold21g:  [234, 587, 652, 646, 685, 840, 809, 1640, 3200, 3760, 5910],   // EGP per gram, 21k
  egx30:    [7089, 12345, 15019, 13036, 13962, 10845, 11949, 14599, 24833, 29661, 41829],
  cdRate:   [12.5, 20.0, 20.0, 17.0, 15.0, 11.0, 11.0, 18.0, 22.5, 27.0, 21.5],  // best annual CD %
  inflation:[10.4, 13.8, 29.5, 14.4, 9.4, 5.1, 5.2, 13.9, 33.9, 28.3, 14.0]      // % avg per year
};
