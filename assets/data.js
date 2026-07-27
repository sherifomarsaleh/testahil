/* Testahil shared sample data — replace with your live MC engine / ledger output to go live.
   Every page on this site reads from this one file. Nothing is hardcoded per-page. */

window.TESTAHIL_TICKERS = {
  PHDC: { name:'Palm Hills Developments', price:4.82, changePct:1.3,
           p10:4.10, p15:4.55, p30:4.68, median:4.95, p75:5.35, p90:5.70, prob:68 },
  TMGH: { name:'TMG Holding', price:8.05, changePct:0.6,
           p10:7.35, p15:7.70, p30:7.90, median:8.35, p75:8.95, p90:9.40, prob:63 },
  EMFD: { name:'Emaar Misr', price:11.40, changePct:-0.4,
           p10:10.20, p15:10.85, p30:11.05, median:11.85, p75:12.70, p90:13.35, prob:55 },
  QNBK: { name:'QNB Group', price:41.50, changePct:0.9,
           p10:38.60, p15:39.80, p30:40.40, median:42.30, p75:44.60, p90:46.80, prob:71 },
  DSCW: { name:'Dice Sport & Casual Wear', price:1.94, changePct:-2.1,
           p10:1.55, p15:1.68, p30:1.78, median:1.92, p75:2.05, p90:2.18, prob:41 },
  ORAS: { name:'Orascom Construction', price:920.00, changePct:0.8,
           p10:850.00, p15:878.00, p30:895.00, median:935.00, p75:985.00, p90:1040.00, prob:66 }
};

window.TESTAHIL_TICKER_ORDER = ['PHDC', 'TMGH', 'EMFD', 'QNBK', 'DSCW', 'ORAS'];

window.TESTAHIL_CALLS = [
  { ticker:'PHDC', date:'2026-06-12', entry:4.55,  horizon:'T+20', pct:9.2,  status:'hit',     r:2.1 },
  { ticker:'TMGH', date:'2026-06-18', entry:8.20,  horizon:'T+20', pct:3.4,  status:'open',    r:0.6 },
  { ticker:'EMFD', date:'2026-06-02', entry:12.10, horizon:'T+20', pct:-4.8, status:'stopped', r:-1.0 },
  { ticker:'QNBK', date:'2026-05-25', entry:41.00, horizon:'T+60', pct:14.6, status:'hit',     r:2.6 },
  { ticker:'DSCW', date:'2026-07-19', entry:1.94,  horizon:'T+20', pct:-11.2,status:'stopped', r:-1.0 },
  { ticker:'PHDC', date:'2026-05-05', entry:4.20,  horizon:'T+60', pct:12.1, status:'hit',     r:2.3 },
  { ticker:'TMGH', date:'2026-04-20', entry:7.60,  horizon:'T+60', pct:8.9,  status:'hit',     r:1.9 },
  { ticker:'EMFD', date:'2026-04-08', entry:11.50, horizon:'T+20', pct:2.1,  status:'hit',     r:1.2 },
  { ticker:'QNBK', date:'2026-03-15', entry:39.80, horizon:'T+20', pct:-3.5, status:'stopped', r:-1.0 },
  { ticker:'DSCW', date:'2026-02-22', entry:2.10,  horizon:'T+60', pct:-6.0, status:'stopped', r:-1.0 },
  { ticker:'ORAS', date:'2026-07-10', entry:895.00,horizon:'T+20', pct:5.1,  status:'open',    r:0.9 },
  { ticker:'ORAS', date:'2026-04-15', entry:860.00,horizon:'T+60', pct:9.4,  status:'hit',     r:2.0 }
];

window.TESTAHIL_TRUST = [
  { ticker:'PHDC', accuracy:85 },
  { ticker:'TMGH', accuracy:91 },
  { ticker:'EMFD', accuracy:72 },
  { ticker:'QNBK', accuracy:88 },
  { ticker:'DSCW', accuracy:58 },
  { ticker:'ORAS', accuracy:79 }
];

window.TESTAHIL_ICONS = {
  hit: '<svg viewBox="0 0 20 20" fill="none"><path d="M5.5 10.5l2.7 2.7L15 6.5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
  open: '<svg viewBox="0 0 20 20" fill="none"><circle cx="10" cy="10" r="6" stroke="currentColor" stroke-width="2"/></svg>',
  stopped: '<svg viewBox="0 0 20 20" fill="none"><line x1="6.5" y1="6.5" x2="13.5" y2="13.5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><line x1="13.5" y1="6.5" x2="6.5" y2="13.5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>',
  shield: '<svg viewBox="0 0 20 20" fill="none"><path d="M10 2.5l6 2.2v4.6c0 4-2.6 6.9-6 8.2-3.4-1.3-6-4.2-6-8.2V4.7L10 2.5z" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/></svg>',
  triangle: '<svg viewBox="0 0 20 20" fill="none"><path d="M10 3l7.5 13H2.5L10 3z" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/><line x1="10" y1="9" x2="10" y2="12.2" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/><circle cx="10" cy="14.4" r="0.9" fill="currentColor"/></svg>',
  xcircle: '<svg viewBox="0 0 20 20" fill="none"><circle cx="10" cy="10" r="7.2" stroke="currentColor" stroke-width="1.4"/><line x1="7.3" y1="7.3" x2="12.7" y2="12.7" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/><line x1="12.7" y1="7.3" x2="7.3" y2="12.7" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/></svg>'
};

window.TESTAHIL_STATUS_LABEL = { hit:'Hit target', open:'Open', stopped:'Stopped' };
