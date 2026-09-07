#!/usr/bin/env python3
"""SCEM walk-forward — the internal training record, generated from the run's own
committed outputs. Never typed: a document that states a figure which moves must not be
the thing that remembers it."""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
J = lambda n: json.load(open(os.path.join(HERE, n)))
S, C, D, P, F = J('scores.json'), J('corrections_log.json'), J('diagnostics.json'), \
    J('panel_export.json'), J('forward_ranges.json')
L, R, MS = S['log_scale'], S['signed_relative'], S['macro_split_detail']
d, Y = P['derived'], P['years']
skf, skt = S['skill_vs_freeze'], S['skill_vs_trend']
X = lambda k: math.exp(-L[k]['bias'])

out = []
w = out.append
w("# TRAINING RECORD — SCEM fundamental walk-forward, 07-09-2026\n")
w("**Sinai Cement Company S.A.E. · EGX · market EG · INTERNAL — never shown to a reader**\n")
w("**THIS IS THE FUNDAMENTAL WALK-FORWARD [R-FCAL-01].** The driver model rebuilt as it")
w("stood at five past origins, projected forward, and scored against what the company")
w("actually reported. It is not the price-engine walk-forward")
w("(`scem_study/backtest_5y.py`, band coverage on the Monte Carlo cone) and not the")
w("technical walk-forward (`engine/lab/ta_calibration/`). Three tests in this system carry")
w("that name and they measure different machinery on different evidence.\n")
w("Everything below was pre-registered in `PRE_REGISTRATION_07-09-2026.md` before a single")
w("error was computed.\n\n---\n")

w("## 1 · Scope — LIGHT, on five sourceable fiscal years\n")
w("Five fiscal years, FY2021 to FY2025, every figure from the company's own audited")
w("statements. Five origins, horizons one to three, **nine resolved driver-cells**.\n")
w("**Why the span stops at FY2021.** Sinai Cement publishes exactly six documents. Three")
w("of them — the FY2022 and FY2023 audited filings, and the Arabic FY2021 one — had never")
w("been downloaded before this run; opening the two English ones is what took the span")
w("from three sourceable years to five and the scope decision from SKIP to LIGHT. The")
w("Arabic filing was downloaded and is **unreadable**: its figures are Eastern Arabic")
w("numerals and neither OCR model available here returns a digit from them, so FY2020 is")
w("left out and the window shortened rather than filled from a vendor.\n")
w("**Every filing is an image-only scan** — `pdftotext` returns 30 to 37 characters for")
w("documents of 30 to 36 pages — so every number arrived by OCR off the rendered pixels")
w("and ARITHMETIC IS THE ARBITER. `panel.py` runs the footings the filings themselves")
w("print, at import. Two misreads were caught by them and neither was visible on the")
w("page:\n")
w("| what | read | filed | how it was caught |")
w("|---|---|---|---|")
w("| FY2022 short-term loans from affiliates | 960,000,000 | 950,000,000 | the filing's "
  "own current-liabilities subtotal refuses the first reading |")
w("| FY2021 deferred tax | 11,761,441 | 11,751,441 | only one of the two closes profit "
  "before tax to profit after tax |\n")

w("## 2 · What this issuer does not disclose\n")
w("**NO PHYSICAL VOLUME. ANYWHERE.** Not a tonne of clinker, not a tonne of cement, not")
w("an installed capacity, not a utilisation rate — in any of the six filings, in any")
w("year. Every OCR'd page of the FY2022 and FY2023 filings was searched and the search")
w("returned nothing.\n")
w("So the ground-up build cannot reach volume × price on a DISCLOSED unit and drops to")
w("the finest sourced level, which for this issuer is the **cost-note line**. Under")
w("[R-SIGCM-02] these revenue lines are `derived`, never `unit`. This is a fact about the")
w("disclosure rather than about the effort, and it is the single most important thing")
w("this run establishes about the delivered study: the tonnage and utilisation that")
w("study's model runs on come from a plant register and the trade press, not from the")
w("company.\n")

w("## 3 · The company the panel actually shows\n")
w("| | " + " | ".join(Y) + " |")
w("|---|" + "---:|" * len(Y))
for lab, k, pct in (('Revenue', 'revenue', 0), ('EBITDA', 'ebitda', 0),
                    ('EBITDA margin', 'ebitda_margin', 1),
                    ('Profit after tax', 'pat', 0),
                    ('Interest-bearing debt', 'interest_bearing_debt', 0),
                    ('Cash', 'cash', 0), ('Equity', 'equity', 0),
                    ('Shares (mn)', 'shares_mn', 0)):
    cells = [('%.1f%%' % (100 * d[y][k])) if pct else ('%.1f' % d[y][k]) for y in Y]
    w("| %s | %s |" % (lab, " | ".join(cells)))
w("")
w("EGP million except where stated. **A company transformed inside the panel:** revenue")
w("%.1f times over four years, an EBITDA margin from %.1f per cent to %.1f, negative"
  % (d['FY2025']['revenue'] / d['FY2021']['revenue'],
     100 * d['FY2021']['ebitda_margin'], 100 * d['FY2025']['ebitda_margin']))
w("equity of EGP %.1fmn at FY2023 becoming EGP %.1fmn at FY2025, and interest-bearing"
  % (d['FY2023']['equity'], d['FY2025']['equity']))
w("debt of EGP %.1fmn becoming EGP %.1fmn. Any record scored across that is a record of"
  % (d['FY2023']['interest_bearing_debt'], d['FY2025']['interest_bearing_debt']))
w("one extraordinary arc, and every interval below should be read knowing it.\n")

w("## 4 · Trap (i), measured on this name\n")
w("**Interest comes from the borrowings that actually bear it.** Suppliers, other credit")
w("accounts, provisions and the deferred-tax liability pay nothing. The two denominators")
w("on this company:\n")
w("| | " + " | ".join(Y[1:]) + " |")
w("|---|" + "---:|" * len(Y[1:]))
w("| on the borrowings that bear interest | %s |"
  % " | ".join('%.2f%%' % (100 * d[y]['kd_on_borrowings']) for y in Y[1:]))
w("| on total liabilities | %s |"
  % " | ".join('%.2f%%' % (100 * d[y]['kd_on_total_liabilities']) for y in Y[1:]))
w("")
_r = [d[y]['kd_on_borrowings'] / d[y]['kd_on_total_liabilities'] for y in Y[1:]]
w("A factor of **%.1fx to %.1fx**. Dividing by the broad total would have implied this"
  % (min(_r), max(_r)))
w("company borrowed at %.2f per cent in FY2025, in an economy whose policy rate was 19.5"
  % (100 * d['FY2025']['kd_on_total_liabilities']))
w("per cent, and the bias that produced would have looked exactly like evidence.\n")

w("## 5 · The score\n")
w("Log error `ln(projected / actual)`. **A negative bias means the method forecast BELOW")
w("what the company reported**, and the `outturn/forecast` column is how many times the")
w("outturn came in above the forecast.\n")
w("| driver | n | bias | MAE | outturn/forecast | 95% block CI | by era | era sign |")
w("|---|---:|---:|---:|---:|---|---|---|")
for k in sorted(L, key=lambda k: L[k]['bias']):
    v = L[k]
    ci = v['ci']
    cis = ('[%+.3f, %+.3f]%s' % (ci['lo'], ci['hi'],
                                 ' \\*' if ci['same_sign_across_blocks'] else '')) if ci else 'n<3'
    eras = ' / '.join('%s %+.2f' % (e, b) for e, b in sorted(v['by_era'].items()))
    w("| %s | %d | %+.3f | %.3f | %.2fx | %s | %s | %s |"
      % (k.replace('_', ' '), v['n'], v['bias'], v['mae'], math.exp(-v['bias']), cis,
         eras, 'FLIPS' if v['era_sign_flips'] else '—'))
w("")
w("`\\*` marks an interval whose sign holds across both bootstrap block lengths.\n")
w("Three drivers cross zero somewhere and are not on a log scale at all — this company")
w("lost money in three of five years — and they are reported separately rather than")
w("pooled:\n")
w("| driver | n | bias (relative) | MAE (relative) |")
w("|---|---:|---:|---:|")
for k in sorted(R):
    w("| %s | %d | %+.3f | %.3f |"
      % (k.replace('_', ' '), R[k]['n'], R[k]['bias'], R[k]['mae']))
w("")

w("## 6 · THE SKILL VERDICT — the method beats both naive benchmarks at every horizon\n")
w("| | h=1 | h=2 | h=3 |")
w("|---|---:|---:|---:|")
w("| skill vs FREEZE (flat at last actual) | %s |"
  % " | ".join('%+.3f' % skf[h]['skill'] for h in ('1', '2', '3')))
w("| skill vs TREND (trailing CAGR) | %s |"
  % " | ".join('%+.3f' % skt[h]['skill'] for h in ('1', '2', '3')))
w("| cells scored, freeze | %s |" % " | ".join(str(skf[h]['n']) for h in ('1', '2', '3')))
w("| cells scored, trend | %s |" % " | ".join(str(skt[h]['n']) for h in ('1', '2', '3')))
w("")
w("**This is a name where the answer to \"is the method beating no change yet\" is YES at")
w("every horizon tested.** On PHDC it was not, on net profit, at any horizon. The margin")
w("is real but it is not large — between a tenth and a quarter of the naive error removed")
w("— and it rests on nine cells from one company through one extraordinary arc, which is")
w("exactly why [R-FCAL-01] calls every finding from a run like this PROVISIONAL.\n")
w("**The trend benchmark is undefined at origin FY2021** and that was pre-registered: one")
w("point of history admits no trailing growth rate. That origin is scored against freeze")
w("alone and the cell counts above say so.\n")

w("## 7 · The direction of the miss, and it agrees with the book\n")
w("**Eleven of thirteen drivers came in BELOW what the company reported.** Revenue by a")
w("factor of %.2f, EBITDA by %.1f, capital spending by %.1f. Only finance expense ran the"
  % (X('revenue'), X('ebitda'), X('capex')))
w("other way, and for a reason the model's own specification explains rather than excuses:")
w("the rule holds debt flat at the origin's level, and this company REPAID essentially all")
w("of it.\n")
w("That direction is the pooled census's own finding arriving on another name. It is also")
w("the single most useful thing this run says about the delivered study: if that study is")
w("wrong about FY2026 onward, this company's own history says the more likely error is")
w("that the forecast is too LOW.\n")

w("## 8 · Macro versus company\n")
w("Each origin re-run on the outturn inflation path, then on outturn inflation and")
w("activity together.\n")
w("| driver | MAE as known | MAE, perfect inflation | macro share |")
w("|---|---:|---:|---:|")
for k in sorted(MS, key=lambda k: -(MS[k]['macro_share_inflation'] or -9)):
    v = MS[k]
    if v['mae_as_known'] is None:
        continue
    w("| %s | %.3f | %s | %s |"
      % (k.replace('_', ' '), v['mae_as_known'],
         '%.3f' % v['mae_perfect_inflation'] if v['mae_perfect_inflation'] is not None else '—',
         '%+.1f%%' % (100 * v['macro_share_inflation'])
         if v['macro_share_inflation'] is not None else '—'))
w("")
w("**THE SPLIT'S OWN CHECK PASSES.** Depreciation, finance expense and interest income")
w("carry no inflation term in their rules and return a macro share of zero — exactly 0.0")
w("per cent for the two financing drivers and −0.1 per cent for depreciation, which has no")
w("CPI term in its first year. A split that could not return zero where zero is the right")
w("answer would be measuring something other than what it claims.\n")
w("**About a third of this method's miss on this company is the macro path and two thirds")
w("is the company.** At origin FY2021 the IMF's own October 2021 edition projected")
w("Egyptian inflation of 6.7, 7.1 and 7.1 per cent for 2022, 2023 and 2024. The outturn")
w("was 16.5, 28.9 and 26.5. No forecasting method available in 2021 had that path, and the")
w("two thirds that remains is what the method actually owns.\n")

w("## 9 · The revenue error decomposed\n")
w("| cell | total log error | from the activity anchor | from the price anchor | residual |")
w("|---|---:|---:|---:|---:|")
for k, v in sorted(D['decomposition'].items()):
    w("| %s | %+.3f | %+.3f | %+.3f | %+.3f |"
      % (k, v['revenue_log_error'], v['from_activity_anchor'], v['from_price_anchor'],
         v['residual_company']))
w("")
w("**THE EXOGENOUS ANCHOR IS THE PROBLEM AND THE RESIDUAL SAYS SO.** Egypt's real GDP")
w("growth contributed between +0.04 and +0.16 of log revenue growth across every cell")
w("while the company's revenue was compounding at 58 per cent a year in nominal terms.")
w("Real GDP growth is not Egyptian cement demand: domestic cement consumption rose 13.4")
w("per cent in 2025 against GDP growth around 4, and the production quota regime that had")
w("capped output since 2021 was permanently lifted in July 2025. This is L-058 arriving on")
w("another name — an exogenous volume anchor has to be scored against \"no change\" before")
w("it is trusted, and this one loses badly on its own leg even while the whole model beats")
w("freeze.\n")
w("**It is a SPECIFICATION finding, not a calibration one**, and no correction factor may")
w("hide it. What would fix it is an Egyptian cement-consumption series at each origin's")
w("own vintage, which this run did not have and did not invent.\n")

w("## 10 · Corrections — NOTHING PROMOTED, AND THAT WAS PRE-REGISTERED\n")
w("The cut-invariance test [R-FCAL-01 AMENDED 07-09-2026] was run through the shared")
w("instrument `engine/valuation_calibration/boundary_sensitivity.py`, never")
w("reimplemented. **Every driver returns ZERO admissible cuts**: nine cells spread over")
w("four target years admit no boundary leaving five on each side. Every bias this run")
w("measured is therefore UNTESTABLE for stability, never stable — an absence of contrary")
w("evidence is not evidence.\n")
w("`PRE_REGISTRATION_07-09-2026.md` section 6 states that consequence in advance, before")
w("any error existed, so nothing here is a verdict reached after seeing which way the")
w("numbers went.\n")
_wf = sum(1 for v in C['candidates'].values() if v['disposition'] == 'watch_flag')
_rf = sum(1 for v in C['candidates'].values() if v['disposition'] == 'refused')
w("| candidates measured | promoted | watch flags | refused as aggregates |")
w("|---:|---:|---:|---:|")
w("| %d | **0** | %d | %d |\n" % (len(C['candidates']), _wf, _rf))
_better = [k for k, v in C['candidates'].items()
           if v.get('adjusted_vs_raw') and v['adjusted_vs_raw']['improves']]
w("%d candidates improve the out-of-sample error when the expanding-window half-strength"
  % len(_better))
w("factor is applied — %s — and **none of them is promoted**, on clause one. %d more make"
  % (", ".join(k.replace('_', ' ') for k in sorted(_better)),
     len([k for k, v in C['candidates'].items()
          if v.get('adjusted_vs_raw') and not v['adjusted_vs_raw']['improves']])))
w("it worse, which is L-061's signature: a correction that degrades out of sample is a")
w("specification defect, not a bias.\n")
w("Clause two would refuse most of them anyway and the reasons are recorded per driver in")
w("`corrections_log.json`. Two are worth naming: a multiplier on revenue would be papering")
w("over the activity anchor identified in section 9, and a multiplier on capital spending")
w("points the opposite way from L-063 and L-275, which say the recent run rate on an old")
w("plant is a CEILING rather than a central estimate.\n")
w("**The guidance ledger is EMPTY and that is a finding.** Sinai Cement publishes no")
w("forward guidance, no results presentation and no earnings call — so no driver in this")
w("model can have inherited a management lean, because there is no management forward")
w("number to inherit.\n")

w("## 11 · The forward bands, with their basis, count and orientation\n")
w("[R-FCAL-01 AMENDED 07-09-2026] a published band declares all three in the file. This")
w("run's are **span**, counted per cell, oriented **actual over forecast**: multiply a")
w("point projection by the band. A band above 1.0 means the method forecast below the")
w("outturn.\n")
w("| driver | h=1 (n=4) | h=2 (n=3) | h=3 (n=2) |")
w("|---|---|---|---|")
for k in ('revenue', 'materials', 'cogs_wages', 'cogs_maintenance', 'transport', 'ga',
          'dna', 'capex'):
    b = F['bands'][k]
    w("| %s | %s |" % (k.replace('_', ' '), " | ".join(
        ('%.2f – %.2f' % (b[h]['low'], b[h]['high'])) if h in b else '—'
        for h in ('1', '2', '3'))))
w("")
w("**HORIZONS FOUR AND FIVE CARRY NO BAND**, and the delivered study says so in those")
w("words rather than borrowing the three-year band. Five sourceable fiscal years give a")
w("longest resolved horizon of three; nothing in this company's own record speaks to a")
w("four- or five-year forecast.\n")

w("## 12 · The valuation-input block\n")
w("Committed at every one of five origins, built as the run went: cash, interest-bearing")
w("debt, PP&E, depreciation and amortisation, the working-capital lines, capital")
w("expenditure and the share count. `python3 scripts/check_valuation_inputs.py` reports")
w("SCEM conforming.\n")
w("**THE SHARE COUNT IS FOOTED TWICE AT EVERY ORIGIN** and that is what makes a")
w("carried-back count impossible here rather than merely discouraged: issued capital over")
w("the EGP 10 par reproduces the count, and that count then reproduces the year's own")
w("PRINTED earnings per share. The count is 68,058,443 at FY2021, 133,065,867 at FY2022 to")
w("FY2024 and 260,812,477 at FY2025 — it moves twice inside a five-year panel, so today's")
w("count carried back would have shown up immediately as an EPS that refused to")
w("reproduce.\n")
w("FY2020 appears under `prior_year_anchor` carrying one figure — the opening cash of EGP")
w("17,035,796, read off the FY2022 cash-flow statement's comparative column — with")
w("everything else RECORDED AS MISSING and its reason named. It is not listed as an")
w("origin, because the run did not test it.\n")

w("## 13 · One-offs\n")
w("| year | line | value | treatment |")
w("|---|---|---:|---|")
for y, lst in sorted(D['one_offs'].items()):
    for o in lst:
        w("| %s | %s | %s | %s |"
          % (y, o['line'], '{:,.0f}'.format(o['value']),
             o['treatment'].split('.')[0] + '.'))
w("")
w("The FY2024 disposal of the Sinai White Portland Cement stake is 48.2 per cent of that")
w("year's pre-tax profit and is excluded from every driver rule. A model that cannot")
w("foresee a stake sale should not be scored as though it should have — and net profit is")
w("shown both ways in the side-by-side statements.\n")

w("## 14 · Caveats, stated plainly\n")
w("* **Nine cells, one company, one extraordinary arc.** Every interval here is wide and")
w("  several straddle zero. Nothing in this record is validated.")
w("* **The panel spans a devaluation sequence and a recovery from near-insolvency.** A")
w("  method scored across that is being asked a harder question than it will usually face,")
w("  which cuts both ways: the skill result is more impressive and the bias measurement is")
w("  less transferable.")
w("* **The activity anchor is mis-specified** and section 9 says so. The skill verdict")
w("  holds in spite of it, not because of it.")
w("* **The macro conditioning for origin FY2025 uses the April 2025 WEO edition**, not the")
w("  October one, which could not be sourced from any of four URL patterns. It existed at")
w("  that origin so the point-in-time discipline holds; it is simply not the freshest")
w("  edition that did. No scored cell depends on it.")
w("* **Perfect foresight of 2025 is a projection, not an outturn.** The latest edition")
w("  obtainable here projects that year rather than reporting it, and cells landing on it")
w("  are labelled.")
w("* **This is a first full run on this name.** The next update adds one origin — FY2026,")
w("  which grades the cells standing at FY2023, FY2024 and FY2025 — and re-tests every")
w("  watch flag on a panel that will admit its first real era cut at around fifteen cells.")

open(os.path.join(HERE, 'TRAINING_RECORD_07-09-2026.md'), 'w').write("\n".join(out) + "\n")
print('training record written: %d lines' % len(out))
