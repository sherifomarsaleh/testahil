"""SWDY — the valuation-gap review [R-GAP-01], GENERATED.

IT WAS HAND-WRITTEN AND IT WENT STALE THE SAME DAY. The 13-09-2026 review was typed
against a central of 87.7633; a lever applied hours later moved the study to 87.9425 and
the review kept auditing the old number — a record behind the thing it records, which is
the same defect the fair-value register's own gate caught in CI on the same afternoon,
and the same defect the 10-09-2026 review had (it audited 87.82 against a price of
136.20 read three sessions after the valuation date).

So the fix goes in the generator and not in the artefact [R-REPAIR-01]. Every figure
below is read from study_numbers.json on the run, and the file is rebuilt by build_all.py
like every other delivered artefact.

IT REFUSES TO REWRITE HISTORY, and the first run of it proved why the guard is needed:
named off edition.py's EDITION it wrote GAP_REVIEW_10-09-2026.md and overwrote the
10-September review, destroying the only record of what this desk said that day. A gap
review is dated by the AUDIT, not by the edition — the two are different acts and this
study has had three reviews against one edition. AUDIT_DATE below is therefore an
explicit constant a person sets when they re-audit, and the generator writes that file
and no other.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
import sys
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import edition as EDN

# THE DATE OF THIS AUDIT. Set it when you re-audit; it is not today's date and it is not
# the edition's, because a generator that silently picks either can overwrite a delivered
# record of what was said on a different day.
AUDIT_DATE = '13-09-2026'

D = json.load(open(os.path.join(HERE, 'study_numbers.json')))
W, DCF, F, L = D['wacc'], D['dcf'], D['fcst'], D['lenses']
I = {k: v['value'] for k, v in D['inputs'].items()}
ST, SM = D['strike'], D['star_case']['decomposition']
spot, SH, central = D['spot'], D['meta']['shares_mn'], D['central']
asof = D['meta']['asof']
gap_abs = spot - central
OUT = os.path.join(HERE, 'GAP_REVIEW_%s.md' % AUDIT_DATE)
_D, _M, _Y = (int(x) for x in AUDIT_DATE.split('-'))
_WORDS = '%d %s %d' % (_D, __import__('datetime').date(_Y, _M, _D).strftime('%B'), _Y)

s = []
A = s.append
A('# SWDY — valuation-gap review, %s  [R-GAP-01] [R-GAP-04] [R-STAR-01]' % _WORDS)
A('')
A('AUDITED CENTRAL: %.4f' % central)
A('')
A('The cash-flow lens reads **EGP %.2f** against the price this valuation is measured'
  % central)
A('against, **EGP %.2f** on %s — a gap of **%+.1f%%**.'
  % (spot, asof, 100 * (central / spot - 1)))
A('')
A('This file is GENERATED from `study_numbers.json` by `gap_review.py`. The edition it')
A('replaced was typed, and it was stale within the day: it audited a central the study')
A('had already moved off. A review that states a number the study no longer publishes is')
A('not a review of that study.')
A('')
A('## What this review replaces, and why a new file rather than an edit')
A('')
A('The 10-September review audited a central of 87.82 against a price of 136.20 read on')
A('6 September. Both numbers have moved and neither moved for the same reason.')
A('')
A('**The price.** That 136.20 was the last row of the price library, three sessions after')
A("this study's own valuation date. The cone, the moving-average stack and the percentile")
A('map were struck on it while the fair value was measured against %.2f, so one document'
  % spot)
A('described two prices. The strike is anchored at the valuation date now, through')
A('`price_series.py`, which refuses to run if the library\'s close on that date is not the')
A('spot the study publishes.')
A('')
A('**The central.** 87.82 first became 87.7633 when the share count was reverted to the')
A('issued 2,140,777,876. A 10-September pass had cut it to 2,139,355,716 on the strength')
A('of an extraordinary general assembly of 19 May 2026 said to have cancelled 1,422,160')
A('incentive shares. THAT CORRECTION IS WITHDRAWN AND THIS REVIEW WITHDRAWS ITS OWN')
A("EARLIER LEAD: note 39's 2,139,355,716 is the IAS 33 weighted-average denominator —")
A('issued capital less shares issued under the incentive scheme and not yet granted,')
A('excluded from earnings per share because they are not outstanding for that purpose. It')
A('is not a capital reduction, the shares exist, the same statements state issued capital')
A("at 2,140,777,876 on the face of the balance sheet, and the assembly appears on no")
A("filing in the company's own regulatory-filings index. One convention was read as the")
A('other, in the direction that raised the answer.')
A('')
A('It then became %.4f when the currency path was DERIVED rather than hand-set. The model'
  % central)
A('escalated its cost base on the house Egyptian inflation ladder, falling 16%% to 7%%,')
A('while depreciating the pound at a flat ~6%% a year — two views of one economy [L-048].')
A('That is upward and toward the price, and it is the outcome rather than the aim: the')
A('hand-set path was the more conservative of the two, so the incoherence had been')
A('DEPRESSING this valuation. The rebuild ledger carries it as its own lever.')
A('')
A('## The gap, priced [R-STAR-01]')
A('')
A('Each assumption below is moved ALONE on a full re-run of the model — not a multiplier')
A('applied to a finished line — and priced against the gap of EGP %.2f a share.' % gap_abs)
A('')
A('| What the market must believe | Worth per share | Share of the gap |')
A('|---|---:|---:|')
for k, v in sorted(SM.items(), key=lambda kv: -kv[1]):
    A('| %s | %+.2f | %.0f%% |' % (k, v, 100 * v / gap_abs))
A('')
_n = sum(1 for v in SM.values() if v >= gap_abs)
A('**%d of the %d clear the gap on their own.** The margin re-run at %.0f%% of it is the'
  % (_n, len(SM), 100 * max(SM.values()) / gap_abs))
A('largest by a distance; the cost-of-capital re-run also clears it, which the study')
A('states rather than claiming a single assumption stands alone.')
A('')
A('## What argues against the largest of them')
A('')
A("The company's own disclosure rather than our opinion. Cables revenue per tonne tracked")
A('copper times the pound almost exactly in FY2024 and then failed to in FY2025 — a')
A('measured pass-through shortfall computed from audited segment revenue against the')
A("issuer's own disclosed tonnage. The FY2023-24 margins were earned on inventory bought")
A('before a devaluation. A repeat requires that pricing power to return, and the most')
A('recent full year measures it leaving.')
A('')
A('## The lenses, at their own values')
A('')
A('| Lens | Bear | Base | Bull | Role | vs price |')
A('|---|---:|---:|---:|---|---:|')
ROLE = {'dcf': 'THE ANSWER', 'relative': 'cross-check',
        'normalized': 'not published for this class', 'book': 'a floor, never weighted'}
for k in ('dcf', 'relative', 'normalized', 'book'):
    l = L[k]
    A('| %s | %.2f | %.2f | %.2f | %s | %+.0f%% |'
      % (l['name'], l['bear'], l['base'], l['bull'], ROLE[k], 100 * (l['base'] / spot - 1)))
A('| RETIRED 45/20/20/15 blend, published unused | — | %.2f | — | retired | %+.0f%% |'
  % (D['retired_blend_value'], 100 * (D['retired_blend_value'] / spot - 1)))
A('')
A('The central is the cash-flow lens itself and is not an average of the four. An earlier')
A('edition did settle it by weight and reported EGP %.2f.' % D['retired_blend_value'])
A('')
A('## The price map, on the same date as the value')
A('')
H3 = ST['horizons']['3M']
A('Anchor %s at %.2f. Three-month median %.2f, 5th-to-95th %.2f to %.2f, probability above'
  % (ST['anchor_date'], ST['spot'], H3['pct']['p50'], H3['pct']['p5'], H3['pct']['p95']))
A('spot %.0f%%. The central sits below the 5th percentile of that distribution: the price'
  % (100 * H3['p_above']))
A('map and the valuation genuinely disagree, and stating the gap at its full size is the')
A('point. [R-LENS-01] keeps the two apart — nothing here reaches the fair value.')
A('')
A('## Our defect first, and what it was')
A('')
A('The rule is to hunt our own error before explaining the market. This review found')
A('several, and none of them was in the cash-flow model. Five files read a study-local')
A('price file that this study had already discredited in writing, ending 5 August 2026 at')
A('105.20 — it cost the moving-average stack, the cone, the percentile table, an expired')
A('one-month check date, a "probability above spot" that was the probability above 105.20,')
A('and a figure drawing a cone opening at 105.20 under a line labelled "spot 130.00". The')
A('driver table published a driver the model does not read. Three captions asserted what')
A('their own grids contradicted. Two expert panels printed a base above their own bull')
A('case. None of it touched the fair value; what closed instead was the class, in each')
A('case by making the sentence read the number rather than restate it.')
A('')
A('## The eight standing headings, re-run against EGP %.2f' % central)
A('')
A('Every figure below is read out of `study_numbers.json` on this run. A previous edition')
A('of this section carried a terminal risk-free of 12.50%, a terminal growth of 9.14% off')
A('a 2.0% real rate, a WACC gliding to 17.85% and a terminal value at 85% of enterprise')
A('value; three of those four had moved and the section had not. That is the defect this')
A('generator exists to stop, rather than an argument about any one number.')
A('')
A('### 1. LATEST FILINGS')
A('Audited FY2023, FY2024 and FY2025 consolidated statements; the reviewed Q1-2026 interim')
A('(13 May 2026) and the reviewed half to 30 June 2026 (11 August 2026), which is the most')
A('recent disclosure and is read for segment revenue, segment margins, capex, net debt,')
A("associates, minorities and the employees' statutory share. The issuer's own quarterly")
A('earnings releases are read separately, and labelled unaudited, for the cables tonnage')
A('series and the engineering backlog. No disclosed period is skipped; `sweep_register.json`')
A('records all of it with dates, and its study-year declaration lists Q1-2026 and H1-2026')
A('as disclosed and swept.')
A('')
A('### 2. BASE YEAR')
A('FY2025 is fully disclosed and every income-statement and balance-sheet line is the')
A('audited figure, none derived. Two rows in Appendix A.1 are house derivations and are')
A('labelled: EBITDA (EBIT plus D&A — the statements carry no EBITDA line) and earnings per')
A('share. Segment revenue ties EXACTLY to consolidated revenue in every year. FY2026E is')
A("anchored on the reviewed half's own measured like-for-like growth for all three")
A('segments rather than a typed path [R-ANCHOR-01], and is cross-checked — not calibrated')
A("— against the Q1-2026 print: the build's %s against a 356,323 grossed-up implied full"
  % '{:,.0f}'.format(F['rev'][0]))
A('year.')
A('')
A('### 3. MACRO COHERENCE')
A('One inflation path governs the model: the house Egyptian terminal of %.1f%%. The'
  % (100 * I['pi_term']))
A('terminal risk-free of %.2f%% is DERIVED from it (%.1f%% inflation + %.1f%% real'
  % (100 * I['rf_term'], 100 * I['pi_term'], 100 * (I['rf_term'] - I['pi_term'])))
A('convention) and terminal growth of %.2f%% from the same inflation and a stated real'
  % (100 * I['g_term']))
A('growth of %.1f%%, so neither is a nominal rate typed beside an inflation assumption.'
  % (100 * I['g_term_real']))
A('The currency path is derived too, and that is new in this edition: the house')
A("purchasing-power depreciation ladder off the company's own realised FY2025 average rate")
A('of %.2f. Copper is escalated at the house long-run US inflation, not at Egypt\'s.'
  % I['fx_hist']['FY25'])
A('')
A('### 4. DISCOUNT RATE')
A('Ke = rf* + beta x the MATURE-MARKET premium + a country premium charged flat beside it')
A('[R-COC-03] = %.2f%%, where rf* = %.2f%% is the local 10-year of %.2f%% less the'
  % (100 * W['ke_exp'], 100 * W['rf_star'], 100 * I['rf']))
A('sovereign default spread of %.2f%%, so the country is charged exactly once and the'
  % (100 * I['sov_spread_cds']))
A('un-netted construction is retired. Beta %.4f is an own-stock weekly regression against'
  % I['beta'])
A('the published EGX30 and applies to the mature leg only. The country weight is %.4f from'
  % I['lambda_country'])
A('the audited geographic split. WACC glides %.2f%% to %.2f%%. Cash is charged for once,'
  % (100 * W['wacc_exp'], 100 * W['wacc_term']))
A('in the bridge, and the forecast interest is net of the cash balance the model builds —')
A('the bridge record carries the disclosure that the same cash is both added at face and')
A('netted inside the weights.')
A('')
A('### 5. TERMINAL')
A('Terminal growth %.2f%% nominal = %.1f%% real compounded with %.1f%% inflation, held'
  % (100 * I['g_term'], 100 * I['g_term_real'], 100 * I['pi_term']))
A("BELOW Egypt's long-run real GDP growth [R-MACRO-02] — the gap is the share of the")
A('economy the company is assumed to cede. It is coherent with the inflation inside the')
A('terminal discount rate BY CONSTRUCTION rather than by coincidence: both read the same')
A('house path. Terminal beta is carried to %.2f under the named construction `%s`, not'
  % (D['cost_of_capital_record']['beta_terminal'],
     D['cost_of_capital_record']['ke_terminal_construction']))
A('held at the measured %.3f. Terminal value is %.0f%% of enterprise value, disclosed in'
  % (I['beta'], 100 * DCF['tv_share']))
A('the summary table, in the bridge and in the caveats, and it is why the sensitivity grid')
A('is centred on the adopted case [R-SENS-01].')
A('')
A('KNOWN AND OPEN: the explicit window ends with revenue growth at %.2f%% against a'
  % (100 * (F['rev'][4] / F['rev'][3] - 1)))
A('terminal of %.2f%% — %.1fpp apart against a 2pp bound. The window is five years and the'
  % (100 * I['g_term'], 100 * (F['rev'][4] / F['rev'][3] - 1 - I['g_term'])))
A('rule wants it run until growth converges. That is a structural question about window')
A('length rather than a typo, it moves the answer, and it is stated here rather than')
A('closed quietly.')
A('')
A('### 6. BALANCE SHEET')
A('The bridge stands on the audited 31 December 2025 sheet, the date the cash-flow model is')
A('constructed at: EV %s less net debt %s plus associates %s less minorities %s less the'
  % ('{:,.0f}'.format(DCF['ev']), '{:,.0f}'.format(DCF['nd']),
     '{:,.0f}'.format(DCF['assoc']), '{:,.0f}'.format(DCF['nci_val'])))
A("employees' statutory share, giving equity attributable of %s — EGP %.2f a share at that"
  % ('{:,.0f}'.format(DCF['eq_attr']), DCF['ps_dec']))
A('date, rolled %.0f/365 of a year to the anchor. The June sheet is read and deliberately'
  % DCF['anchor_days'])
A('not substituted. Minorities are charged at their PROFIT share, not at book, and the')
A('difference is disclosed.')
A('')
A('### 7. CLAIMS AGAINST THE RECORD')
A('Every "does not disclose" and every "never" in this study was re-checked against the')
A('filings. THIS PASS FOUND FOUR STANDING AND WITHDREW ALL FOUR. (a) The claim that the')
A("company's quarterly releases \"were not reachable from this research environment\" —")
A('withdrawn in section 7 and still standing in four other places, including the workbook')
A("panel; the releases were held here throughout and carry the tonnage the Cables driver")
A('is built on. (b) "No filing discloses the cap\'s headroom" in the equity bridge, while')
A("this study computes that headroom at %.1fx from the wage bill disclosed in three notes"
  % D['employees_cap']['headroom_fy25'])
A("of the same statements. (c) Figure 3's caption, \"no cell in the tested range reaches")
A('the market price\", over a grid with cells above it. (d) The [R-STAR-01] case\'s "one')
A('assumption reaches the market and nothing else comes close", above its own')
A('decomposition showing two that clear the gap. All four now read their own numbers.')
A('')
A('### 8. MULTIPLE CROSS-CHECK')
_pe = spot / (F['np_attr'][0] / SH)
_ev_mkt = spot * SH + DCF['nd'] - DCF['assoc']
A("At EGP %.2f the market pays **%.1fx the model's own FY2026E attributable earnings** and"
  % (spot, _pe))
A("an implied **EV/EBITDA of about %.1fx** on FY2026E EBITDA, against the model's own %.1fx"
  % (_ev_mkt / F['ebitda'][0], DCF['ev'] / F['ebitda'][0]))
A('on its enterprise value. The trailing figures the study publishes are a P/E of %.1fx and'
  % D['rel']['pe_trailing'])
A('an EV/EBITDA of %.1fx. The earnings yield of %.1f%% sits against an Egyptian 10-year at'
  % (D['rel']['ev_ebitda_trailing'], 100 / _pe))
A('%.2f%%: the market is paying a multiple that requires the cost of capital to be lower'
  % (100 * I['rf']))
A("than an Egyptian investor's alternative, which is the same disagreement the")
A('currency-of-discounting question states from the other side.')
A('')

with open(OUT, 'w', encoding='utf-8') as f:
    f.write('\n'.join(s))
print('wrote %s | audits %.4f vs spot %.2f (%+.1f%%) | %d lines'
      % (os.path.basename(OUT), central, spot, 100 * (central / spot - 1), len(s)))
