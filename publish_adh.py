#!/usr/bin/env python3
import glob, shutil, sys, re

def rep(path, a, b, count=None):
    s = open(path).read()
    c = s.count(a)
    if c == 0:
        print('MISS in', path, ':', a[:80]); sys.exit(1)
    if count and c != count:
        print('COUNT', c, '!=', count, 'in', path, ':', a[:60]); sys.exit(1)
    open(path, 'w').write(s.replace(a, b))

# ---------- 1) data.js: SITE.latest + TICKERS entry + LEDGER rows ----------
TICKER = '''  ALPHADHABI: {
    name: "Alpha Dhabi Holding",
    nameAr: "ألفا ظبي القابضة",
    code: "ADX:ALPHADHABI",
    spot: 8.22,
    spotDate: "close 03 Jul 2026 — pre the 7–8 Jul war re-escalation, flagged in the study",
    ccy: "AED",
    fair: { bear: 6.08, base: 7.30, full: 8.82 },      // 10 Jul 2026 — weighted central 7.30 (−11% vs spot 8.22). Holdco SOTP/NAV primary: four listed stakes at ADX marks (Aldar 31.63% = AED 20.5bn, NMDC 76.68% = 14.4bn, PureHealth 35.06% = 8.6bn, NCTH 73.73% = 2.4bn) + Trojan 51% at the ADQ transaction mark (5.2bn) + residual audited book → NAV 7.44/sh at par, 6.32 at a 15% holdco discount (45% weight). Consolidated FCFF DCF 11.72 = a multi-year ceiling (80% TV, ΔWC absorption) at 15%; look-through relative 8.07 at 25%; dividend-policy DDM 4.55 at 15%. The crux: spot pays ~+10% ABOVE undiscounted NAV — the premium is the trade. bear/full = weighted bear/bull.
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
      study: "files/ALPHADHABI_Valuation_Study_10-07-2026_public.docx?v=0710e",
      model: "files/ALPHADHABI_Valuation_Model_10-07-2026_public.xlsx?v=0710e",
      pdf:   "files/ALPHADHABI_Valuation_Study_10-07-2026_public.pdf?v=0710e"
    }
  },
'''

NOTE = ("PARITY under the v3 carry-anchored gate. Name-level CRPS skill +0.006 vs a carry-anchored random-walk "
        "benchmark, bootstrap 90% CI [\\u22120.008, +0.016] spans zero (P(skill>0)=0.80), robust across block sizes "
        "{2,3,4}. The AE market fit is a 1-name PROVISIONAL (Gaussian innovations, width_cal 1.042, 14 non-overlapping "
        "60d windows on the post-2022 ADX workweek panel) \\u2014 per the QGTS precedent no AE name-level verdict is "
        "treated as more than provisional until a \\u22653-name panel exists. A calibrated distribution \\u2014 no "
        "single-name edge demonstrated, and none claimed. Carry-anchored drift: 3M EIBOR 3.93%, no ex-dividend date in "
        "the window (FY25 distribution paid Q1-26; q=0). TIMING FLAG: the anchor pre-dates the 7\\u20138 Jul ceasefire "
        "collapse \\u2014 this cohort will be graded inside the war-regime window; outlier-triggered out-of-cycle review "
        "applies if structurally surprising.")

L20 = f'''  {{
    instrument:"ALPHADHABI", asset_class:"other", cal:"matches",
    anchor_date:"2026-07-03", anchor_price:8.22, ccy:"AED",
    horizon_label:"T+20", grade_date:"2026-07-31", cycle_no:1, reanchor_from:null,
    anchor_vol:0.341, horizon_days:20,
    note:"{NOTE}",
    p5:7.04, p25:7.73, p50:8.24, p75:8.79, p95:9.67,
    touch:{{ "+5":54, "+10":27, "+15":12, "+20":5, "-5":50, "-10":21 }},
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }}
  }},
  {{
    instrument:"ALPHADHABI", asset_class:"other", cal:"matches",
    anchor_date:"2026-07-03", anchor_price:8.22, ccy:"AED",
    horizon_label:"T+60", grade_date:"2026-09-25", cycle_no:1, reanchor_from:null,
    anchor_vol:0.341, horizon_days:60,
    note:"{NOTE}",
    p5:6.30, p25:7.42, p50:8.29, p75:9.27, p95:10.93,
    touch:{{ "+5":73, "+10":54, "+15":38, "+20":26, "-5":69, "-10":46 }},
    realized_close:null, realized_high:null, realized_low:null,
    in_90:null, in_50:null, realized_quantile:null, median_err:null,
    touch_hit:{{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }}
  }},
'''

s = open('assets/data.js').read()
assert 'ALPHADHABI' not in s, 'already present'
s = s.replace('const SITE = { updated: "2026-07-10", latest: "EXTRA" };',
              'const SITE = { updated: "2026-07-10", latest: "ALPHADHABI" };', 1)
# insert TICKER right after the opening of TICKERS, i.e. before "  EXTRA: {"
i = s.find('  EXTRA: {')
assert i > 0
s = s[:i] + TICKER + s[i:]
# insert LEDGER rows before the first EXTRA ledger row
j = s.find('    instrument:"EXTRA"')
j = s.rfind('  {', 0, j)
assert j > 0
s = s[:j] + L20 + s[j:]
open('assets/data.js', 'w').write(s)
print('data.js updated')

# ---------- 2) coverage.js ----------
EN = ('  {tk:"ALPHADHABI", code:"ADX:ALPHADHABI", name:"Alpha Dhabi Holding", sector:"Diversified holding", '
      'sub:"IHC-ecosystem investment holding — listed stakes + construction", country:"UAE", cur:"AED", '
      'fair:"7.30", price:"8.22", gap:"\\u221211%", date:"10 Jul 2026", url:"alphadhabi.html", '
      'thesis:"Abu Dhabi\\u2019s second-largest listed holding, valued as what it is: a mark-to-market sum-of-the-parts — '
      'Aldar 31.63%, NMDC 76.68%, PureHealth 35.06% and NCTH 73.73% at ADX prices, Trojan 51% at the ADQ transaction '
      'mark, the residual audited book at carrying value — giving NAV of AED 7.44/share at par and 6.32 at a 15% holdco '
      'discount. Spot 8.22 pays ~+10% ABOVE undiscounted NAV: the premium is the whole trade, a bet that IHC deal flow '
      'and the FV-gain engine (+AED 3.2bn in FY25) outrun two straight years of falling attributable EPS. A consolidated '
      'DCF ceiling (11.72, 80% terminal) is weighted lightly; look-through P/E 8.07; the AED 2bn dividend policy '
      'discounts to 4.55. Weighted central 7.30 (\\u221211%). §3 Monte Carlo at parity on a provisional 1-name UAE '
      'calibration, honestly flagged; the 7\\u20138 Jul war re-escalation post-dates the price data and is carried as an '
      'explicit left-tail. The stake marks are observable daily — the inverse of a black-box conglomerate."},\n')
AR = ('  {tk:"ALPHADHABI", code:"ADX:ALPHADHABI", name:"ألفا ظبي القابضة", sector:"قابضة متنوعة", '
      'sub:"قابضة استثمارية في منظومة IHC — حصص مدرجة + مقاولات", country:"الإمارات", cur:"AED", '
      'fair:"7.30", price:"8.22", gap:"\\u221211%", date:"10 يوليو 2026", url:"alphadhabi.html", '
      'thesis:"ثاني أكبر شركة قابضة مدرجة في أبوظبي، نُقيّمها على حقيقتها: مجموع أجزاء بأسعار السوق — الدار 31.63٪ '
      'وNMDC 76.68٪ وبيور هيلث 35.06٪ والوطنية للفنادق 73.73٪ بأسعار سوق أبوظبي، وطروادة 51٪ بسعر صفقة ADQ الفعلية، '
      'وباقي الدفاتر المدقَّقة بقيمتها الدفترية — فتبلغ قيمة الأصول الصافية 7.44 درهم للسهم دون خصم و6.32 عند خصم قابض '
      '15٪. السعر 8.22 يدفع علاوة ~10٪ فوق القيمة دون خصم: العلاوة هي الصفقة كلها — رهانٌ على أن تدفق صفقات IHC ومحرك '
      'أرباح إعادة التقييم (+3.2 مليار درهم في 2025) يتفوقان على عامين متتاليين من تراجع ربحية السهم. المركز المرجّح '
      '7.30 (−11٪)؛ ومونت كارلو عند التعادل على معايرة إماراتية أولية باسم واحد مُعلَنة بصراحة، مع تنبيه صريح إلى أن '
      'انهيار الهدنة في 7–8 يوليو يقع بعد بيانات الأسعار ويُحمَل كذيل هبوطي حي."},\n')
c = open('assets/coverage.js').read()
assert 'ALPHADHABI' not in c
i = c.find('const COVERAGE_EN = [\n') + len('const COVERAGE_EN = [\n')
c = c[:i] + EN + c[i:]
j = c.find('const COVERAGE_AR = [\n') + len('const COVERAGE_AR = [\n')
c = c[:j] + AR + c[j:]
c = c.replace('EXTRA:"eXtra",', 'EXTRA:"eXtra", ALPHADHABI:"Alpha Dhabi",', 1)
open('assets/coverage.js', 'w').write(c)
print('coverage.js updated')

# ---------- 3) ledger.html HAS_BACKTEST ----------
rep('ledger.html', 'new Set(["AGTHIA","GBCO"', 'new Set(["ALPHADHABI","AGTHIA","GBCO"', 1)

# ---------- 4) Calibration_Ledger.md ----------
m = open('Calibration_Ledger.md').read()
m = m.replace('| **LCSW** | PASSED |',
    '| **ALPHADHABI** | PARITY (v3 gate) | CRPS skill +0.006, 90% CI [−0.008, +0.016] spans zero; robust across blocks {2,3,4}. AE fit is 1-name PROVISIONAL (Gaussian, width_cal 1.042) per the QGTS precedent. Published on the parity tier; anchor 03-Jul-26 pre-dates the 7–8 Jul ceasefire collapse (timing-flagged). |\n| **LCSW** | PASSED |', 1)
open('Calibration_Ledger.md', 'w').write(m)
print('Calibration_Ledger.md appended')

# ---------- 5) engine: panel + UAE profile ----------
shutil.copy('/home/claude/adh/AE_ADH_60d.csv', 'engine/panels/AE_ALPHADHABI_60d.csv')
p = open('engine/market_profiles.py').read()
OLD = '''UAE = MarketProfile("AE", "UAE (ADX/DFM)", [("2020-01-01", 0.0450)], 0.0450,
    "PLACEHOLDER — source AED federal bond; never UST (peg rule).", "rev_1m", -1, 0.06, False,
    breaks=["2022-01-01"], notes="Workweek switch Jan-2022: vol pool post-2022 only. "
    "Signal off until 5-name panel estimated (FAB/ENBD/EMAAR/ADNOCGAS/IHC available). "
    "IHC needs liquidity screen.")'''
NEW = '''UAE = MarketProfile("AE", "UAE (ADX/DFM)", [("2020-01-01", 0.0450), ("2026-07-01", 0.0393)], 0.0393,
    "3M EIBOR (CBUAE fixings; Fed-mirror via the peg) — never UST. Long rf for CoC: AED federal T-bond.",
    "rev_1m", -1, 0.06, False,
    nu=250.0, width_cal=1.042,
    fit_meta=("PROVISIONAL 1-NAME FIT 10-Jul-2026 on ALPHADHABI (14 non-overlapping 60d "
              "windows, post-2022 ADX-workweek panel, 2023-2026): MLE selected the "
              "Gaussian limit (nu=250 encodes normal), cal=1.042 (shrink 0.7). Backtest "
              "carry = CBUAE mirror of the Fed schedule. Name verdict PARITY +0.006 "
              "CI[-0.008,+0.016], P(skill>0)=0.80, robust blocks {2,3,4}. QGTS-precedent "
              "rule applies: single-name AE fit is provisional — no AE name-level FAIL "
              "is real, and this fit is re-estimated, once a >=3-name panel exists "
              "(FAB/ENBD/EMAAR/ADNOCGAS/ALDAR/IHC candidates; IHC needs a liquidity "
              "screen). Panel frame: engine/panels/AE_ALPHADHABI_60d.csv."),
    breaks=["2022-01-01"], notes="Workweek switch Jan-2022: vol pool post-2022 only. "
    "Signal off until 5-name panel estimated (FAB/ENBD/EMAAR/ADNOCGAS/IHC available). "
    "IHC needs liquidity screen.")'''
assert OLD in p, 'UAE block drifted'
p = p.replace(OLD, NEW, 1)
open('engine/market_profiles.py', 'w').write(p)
print('engine updated')

# ---------- 6) files + calibration asset ----------
for f in ['ALPHADHABI_Valuation_Study_10-07-2026_public.docx',
          'ALPHADHABI_Valuation_Model_10-07-2026_public.xlsx']:
    shutil.copy(f'/home/claude/adh/{f}', f'files/{f}')
shutil.copy('/home/claude/adh/ALPHADHABI_Valuation_Study_10-07-2026_public.pdf',
            'files/ALPHADHABI_Valuation_Study_10-07-2026_public.pdf')
shutil.copy('/home/claude/adh/calibration_ALPHADHABI.png', 'assets/calibration_ALPHADHABI.png')
print('files staged')

# ---------- 7) cache-bust bump ----------
n = 0
for f in glob.glob('*.html') + glob.glob('ar/*.html') + glob.glob('embed/*.html') + glob.glob('go/*.html') + glob.glob('news/*.html'):
    t = open(f).read()
    if 'v=20260710d' in t:
        open(f, 'w').write(t.replace('v=20260710d', 'v=20260710e'))
        n += 1
print('cache-bust bumped in', n, 'files')
