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
      study: "files/TMGH_Valuation_Study_15-06-2026_public.docx?v=1506b",
      model: "files/TMGH_Valuation_Study_15-06-2026_public.xlsx?v=1506b",
      pdf:   "files/TMGH_Valuation_Study_15-06-2026_public.pdf?v=1506b"
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
  { code:"EGX:EMFM", name:"Emaar Misr",                       url:null,        status:"soon" },
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
