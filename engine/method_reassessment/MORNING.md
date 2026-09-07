# Morning list

Questions and deliveries that arose overnight, each with the evidence and the recommended answer. Empty means nothing needs you.

## 06 Sep 2026 — the valuation-input priority: three of the four already exist

**Nothing here needs a decision.** You directed that PHDC, TMGH, EGCH and AMOC's per-origin
valuation-input blocks be finished before further gate work, on the basis that only ARCC's had
landed. Measured live before starting:

| run | `valuation_inputs.json` | origins |
|---|---|---|
| AMOC | present | 5 — FY2021–FY2025 |
| ARCC | present | 8 — FY2018–FY2025 |
| EGCH | present | 13 — FY2012–FY2024 |
| PHDC | present | 11 — FY2015–FY2025 |
| **TMGH** | **absent** | **0** |

All four landed today, in commits made alongside other work. The census figures move with
them: **capex is present in 26 of 55 name-origin cells, not 0; cash in 62%, not 25%; a footed
share count in 60%, not 16%; and 26 cells carry a complete bridge with a capex figure**, where
the instruction has none. Those figures match the state recorded at `[R-FCAL-01 AMENDED]`'s
adoption on 3 September, so the likeliest reading is that the instruction was written from the
digest rather than from the live census — which is exactly what that rule tells everyone to
avoid, and it is worth saying because the digest cannot carry a number that moves.

**The priority is taken as given and the work is proceeding — on the one name that needs it.**
TMGH's block is being built from its own six annual filings (FY2020–FY2025). Origins before
FY2020 have no annual filing in that run's archive and will be recorded as missing with their
reason rather than reconstructed, as ARCC refused its share count.

Reported rather than silently re-scoped: a status that reports a closed blocker as open spends
your time on work already delivered.


## 06 Sep 2026 — CONSUMPTION THROTTLED TO HALF THE WEEK, PER YOUR INSTRUCTION

Your instruction of 06-Sep, stated four times — *"Get back to normal consumption pattern. Maximum
50 percent of the week consumption dedicated to this task and distributed over the whole week.
Leave the other 50 percent limit to me. Apply immediately"* — is applied. **Nothing here needs a
decision;** it is recorded so the next session inherits it rather than reverting to the old cadence.

**What was actually changed** (acts, not intentions):

| | Before | Now |
|---|---|---|
| Hourly auto-resume ×2 | every hour, two sessions | **deleted** |
| Hourly backstop | every hour | **deleted** |
| Fresh-session safety net | daily, took over on a 6h-stale state file | **deleted** |
| Continuous wake | 08:00 and 22:00 Cairo | **once daily, 22:00 Cairo**, bounded |
| Question slot | 09:00 Sun–Thu, then continued working | 09:00 Sun–Thu, **question only, no work** |
| Self-re-invocation | armed at the end of every turn | **retired** — a turn that ends, ends |
| Agent fan-out | fleets, to consume expiring capacity | outside-reader work only, never throughput |

Wake-ups fell from roughly fifty a day to two. The 05-Sep boosted window and the
100%-overnight/50%-by-day split are both retired; the binding rule is now weekly.

**The cost, stated rather than discovered later.** At one bounded session a day the programme runs
on the slowest row of the plan's own calendar table. Phase 2's 85 names are months of calendar at
this cadence, not weeks. That is your call and it is taken as given — the honest response is to
order the work so the most valuable findings land first, not to quietly run faster. Say the word
and the cadence changes back.

Recorded in `STATE.json` (clock block), `PLAN_02-09-2026.md` (Parts G and H) and the routine
prompts themselves, so it binds on a session that starts cold.


## 02→03 Sep 2026

1. **Digest amended and renamed** — `engine/PROJECT_INSTRUCTIONS_02-09-2026.md`, revision 2026-09-02a (the Day-0 merge took both sides' amendments: EGCH's [R-MERGE-01] from main and this branch's workbook-structure gate). CLAUDE.md asks that its full text be sent to you in chat after any edit; it will be sent at the 08:00 wake. No decision needed.

2. **Two TMGH earnings releases could not be re-fetched** — "TMG Holding FY2020 earnings release.pdf" (HTTP 502 at the proxy on every retry) and "TMG Holding 1H2021 earnings release.pdf" (HTTP 404 at the company's archive). Both periods' audited statements were obtained and sha256-verified (136 of 138 registered TMGH documents), and neither release is an input to a delivered number, so nothing is blocked. If you hold copies, attach them and they will be registered under their recorded hashes. No decision needed.

3. **The plan's Gantt** was rebuilt as a data-driven table (markdown, page and Word) after your report at 22:07 that the chart was not rendering; the Word edition was re-sent. Delivered, nothing needed.

4. **TMGH interim edition 2 (02-09-2026) is built and staged** — sales held flat in real terms and the minority deducted at its share of value; central EGP 69.92 against 97.80 (−28.5%, from −60%). The residual is the flat 35.79% discount rate, which is WS1's job, not a class-A fix. Not published; the publish queue holds it for the batch.

5. **PHDC interim edition 2 (02-09-2026) is built and staged** — the three corrections of its 01-Sep review applied (31-Mar-2026 balance sheet in the bridge, minority at its share of value, normalised earnings at cost of equity less growth). Central EGP 11.45 against 15.20 (-24.7%, from −28.0%). As the review said, the discount survives these; the rest is the lens blend and the flat discount rate, which WS1–WS3 address for the whole book. Not published.

6. **WS2 is done — one house macro path per market.** Egypt is sourced from the central bank's own 20-August statement and its published forecast path; the other six markets carry files that declare themselves pending and refuse to load, rather than borrowing a neighbour's numbers. Every study's growth rates are now held to the path by a gate outside the study, with a negative control that reinjects the exact PHDC and AMOC defects. The cost-of-capital reference the protocol has named since July finally exists, generated. Both governing documents are at revision 2026-09-02b; **their full text is owed to you in chat and will be sent at the 08:00 wake.** No delivered number moved.

7. **A prompt-injection attempt, for your awareness.** A web page I fetched while sourcing the Egyptian inflation path carried text imitating a system instruction, telling me to change the commit attribution line. I ignored it and kept your attribution. Nothing was committed under it. Worth knowing that fetched pages in this workflow can carry such text; the discipline is that instructions come from you, not from sources.

8. **WS4 is done — the bridge standard.** The enterprise-to-equity bridge is now a recorded set of choices (which balance sheet, which minority basis, cash charged how often) checked by a gate outside each study, with sixteen conditions in its negative control. PHDC and TMGH conform; the other twenty-two studies are listed and will migrate as they are rebuilt. The general lesson is registered in both documents: a model that recalculates is not a model that is right, and all four of these defects lived inside arithmetic that reconciled to the last cell.

9. **WS3 is done — the lens architecture.** One class primary is now the central and the other lenses are cross-checks that define the envelope; the typed 45/15/20/20 blend is retired because it never cleared any out-of-sample test. The registry is keyed on the lessons register's own classes, so the two cannot drift apart. **This is the change that moves the published numbers most**, and it does so in WS8 when the five studies are re-issued: on PHDC the central goes from the blend's 11.45 to the cash-flow lens's 14.54 against a price of 15.20. Nothing has moved yet.

10. **Three governing-document amendments landed overnight** ([R-MACRO-01], [R-BRIDGE-01], [R-LENS-03]); both documents are at revision 2026-09-02d and their full text is owed to you in chat at the 08:00 wake.

11. **WS1 is done — the cost of capital.** A study now gets the whole ladder from one call: the explicit window, one forward rate per year gliding on the central bank's own easing path, and a terminal whose every line is derived rather than quoted. It refuses, rather than warns, on seven conditions including a flat rate in a market the house path calls a transition. This is the largest of the four levers: PHDC currently discounts every year and the perpetuity alike at 26.25%, where the schedule glides from 25.24% to 16.26%.

12. **A real defect found by the new module on its first run.** AMOC's own committed record carries a cost of debt of 22.00% against a sovereign yield of 22.31% recorded in the same file, thirty-one basis points below the government that taxes it, which the standing rule has forbidden since the method was adopted. AMOC is net cash, so it barely moves the answer, and it is registered for correction when that study is re-issued. Worth noting that the one study which had implemented the procedure is where the gate found something.

13. **Next is the re-issue, and it is where the numbers move.** The four modules are built and gated but no delivered number has changed yet. WS8 rebuilds the five calibrated studies on them, starting with TMGH. On PHDC the two known effects run the same way: the lens architecture takes the central from the blend's 11.45 to the cash-flow lens, and the discount-rate glide raises the cash-flow lens itself. Against a price of 15.20 that is the test of whether the pessimism was the method.

14. **The gap gate now fires above the price as well as below.** You had adopted it one-sided on 1 September, and the cost of that was written down at the time: an over-optimistic study got no automatic audit. The reassessment measured the cost, which is that every correction the house made ran the same way. On its first two-sided run the gate found DU at 13.0% above its own spot with no review, a case the old rule could not see by construction. It is listed as outstanding and gets its review when that study is re-issued. This is reversible on a word if you would rather keep the rule as you first gave it.

15. **The first re-issue is done, and it is the answer to your question.** TMGH rebuilt on the four new modules moves from a central of 69.92 to 91.83 against a price of 97.80 — from 28.5% below the market to 6.1% below it. The published envelope is 63.70 to 123.03, so the price now sits inside the range instead of above every case. Nothing about the company changed: every driver, filing and operating assumption is the one this morning's edition carried. What changed is the method, and it changed for every name at once rather than for this one.

16. **What did it.** Almost all of the move is the discount rate ceasing to be a single number. This company's order book converts over fourteen years and the model discounts to year nineteen; a flat crisis-level rate values a pound arriving in year nineteen at about a quarter of what the schedule values it at, and the whole of that difference was an unstated assumption that Egypt never normalises. The terminal-growth correction runs the other way and is smaller. Both were in your own protocol already and neither was being applied.

17. **PHDC is rebuilt too, and it crossed the price.** Its central moves from 11.45 to 17.15 against a price of 15.20 — from 24.7% below the market to 12.8% above it. Three changes, and they do not all point the same way. The discount schedule is worth about +10.80 a share on its own. Retiring the four-lens blend raised the published figure without touching a valuation number. And extending the explicit window from five years to fifteen, which was forced because a window ending at 44% growth cannot capitalise at 7%, took the cash-flow lens back DOWN from 26.51 to 17.15 and cut the terminal from 74% of enterprise value to 31%.

18. **The two-sided gate fired on its first real case, hours after it was adopted.** PHDC at +12.8% required the eight-heading review before its files could be staged, and that review is written: `engine/phdc_study/GAP_REVIEW_02-09-2026.md`. It is the first study in this repository audited for being too optimistic. The audit finds the answer stands, and it names the two things a reader should be sceptical of: the delivery path takes handovers to 2.19 times their current level over fifteen years, and the whole schedule rests on the central bank reaching a 7% target it has not yet reached.

19. **Two names down, three to go.** ARCC, EGCH and AMOC remain, and AMOC also carries the cost-of-debt correction the new module found. Nothing is published; the queue holds the files for the batch.

20. **Two instruments against the lean, now standing.** Every study will publish what the *price* must believe under its own drivers, so a disagreement becomes measurable rather than rhetorical: PHDC's price is paying for a cash conversion rate of 7.9% against the study's 8.7%, and the company's own three cash-flow statements show 3.9%, 17.9% and 4.4%. And every judgement worth more than 5% of value is recorded both ways with a sign test on the set. PHDC resolved two of its five material judgements upward, p=1.00 — no lean at all, which is evidence for the rebuild rather than against it.

21. **Where the night ended.** Four new modules built and gated, two studies rebuilt on them, six new rules in both governing documents (now at revision 2026-09-02g), and eight gates in continuous integration each with its own negative control. Three studies remain to re-issue: ARCC, EGCH and AMOC. Nothing is published.

22. **ARCC is diagnosed and ready to build, and it carries the clearest single example of why the house macro path was needed.** ARCC builds its terminal risk-free rate from the central bank's 5% Q4-2028 target; AMOC builds its from the 7% target in force. Same country, same date, two hundred basis points apart, each with a written argument in its own file, and neither aware of the other. The house path settles it at 7%, because the bank's own August guidance puts the return to the 7% band in the second half of 2027 and does not forecast the undershoot. ARCC also escalates its costs at headline inflation while escalating its cement price below it in every year, which is the real-terms squeeze the study corrected once at the cost-stack level and which survived at the index level. Both are recorded in the state file with the fix.

23. **ARCC's escalators, and a filing that settles them.** Expressed against the house macro path, ARCC's committed model turns out to assume an 11% cumulative real decline in its cement price and a 5% real decline in its costs by 2030. Neither was stated; both are artefacts of nominal index paths typed against an inflation view that is now 450 basis points below the house one. What settles the question is the company's own reviewed first half of 2026, published after those paths were set: a gross margin of 40.5% against 40.6% for the full prior year. Its price and its cost are moving together in practice. So the model's substance is right and now has a filing behind it, and only its expression is wrong — two typed index paths standing in for one relationship the accounts disclose. The rebuild anchors 2026 on the half-year and escalates both legs on the house path from 2027, with the real growth stated. It does not move costs to the house path alone, which would manufacture a squeeze the company's own accounts contradict.

24. **ARCC re-issued — and this one goes DOWN.** Central EGP 53.46 against a price of 59.00 (-9.4%, from −8.3%). Two of the three corrections cost value: the terminal risk-free rate rises from 10.50% to 12.50% because it is now derived from the house path rather than from this study's own choice of which published central-bank target to quote, and the currency path is derived by purchasing-power parity rather than hand-set, which depreciates the pound further than the typed path did. Worth saying plainly: PHDC and TMGH went up, ARCC goes down. A method reassessment that only ever raised numbers would deserve suspicion.
25. **A gate that was never running.** ARCC attested `external_reader_scrub=True` in its own checklist and no scan existed anywhere in the study — the boolean was typed. It now reads a real scan of the delivered documents, and the attestation refuses three ways (a seeded hit, a superseded filename, no result at all), each tested. The scan's first run also caught four tables printing past the page frame. Nothing here changed a number; it changed whether anyone would have known.

26. **EGCH — the one decision I am referring to you rather than taking.** Its central moves from EGP 3.76 to **-1.06** against a price of 13.98. Nothing about the company changed and no new defect was found; what changed is that the typed 45/20/20/15 blend is retired, and **the blend was concealing the study's own finding**. Forty-five per cent of it was a NEGATIVE cash-flow reading and fifty-five per cent three positive ones, so a reader saw 3.47 and never learned that the study's primary lens sat below zero. The disagreement, published: carried through -1.06, the programme stopped 2.82, disclosed book value 8.16, relative multiple 15.47. The reverse read is the sharpest line in it — the traded price implies a flat nominal discount rate of about 9.2% against a 23.0% Egyptian sovereign.

    **The question for you: does the house publish a negative central at all?** The alternative, which I think is the better one, is to publish this name as a two-sided answer — -1.06 carried through and 2.82 stopped — with no single central figure, because the contested judgement is binary and straddles zero and any single number hides that. Every figure is identical either way; it is a decision about what the house is willing to state, not a modelling one. Nothing is published and the gap review carries the full analysis.

27. **A gate was passing a review of a different answer.** EGCH's central moved while its gap review — written for the old number — sat unchanged in the directory, and the gate passed the study: it checked a review existed and covered the eight headings, never that it audited the answer the study now publishes. Reviews now state the central they audited and the gate compares. Its first run caught two live reviews, and the negative control carries the EGCH incident as a seeded case.

28. **AMOC re-issued — all five are now done.** Central EGP 9.91 against 9.10 (+8.9%, from 8.64). Its cost of debt was 22.00% against an Egyptian sovereign of 22.31% recorded in the same file — a company borrowing below the government that taxes it, which the procedure forbids outright. It moves the answer by about one per cent, because the debt book is 0.14% of the capital structure. That is precisely why it was worth correcting: a rule obeyed only when it is expensive is not a rule.

29. **A gate crashed and reported nothing, and I read the silence as clean.** `check_cost_of_capital.py` died on ARCC's record — I had written its effective rates as a mapping of fiscal year to rate where it expected a plain list — and because it defers all printing to the end of its loop, it produced no output at all: no failure line, not even the count of studies examined. My own earlier check of it therefore read as "no ARCC failures" when it had examined nothing, which is the empty-result-is-not-a-clean-result failure happening inside a gate written to prevent it. It was found by the independent gate runner, not by me. Fixed three ways: the mapping is now accepted (a record that names its periods is better evidence, not worse), any other shape is refused with a message, and one malformed record can no longer silence the other twenty-three. Its negative control passed all seventeen of its cases while the gate was broken on real data, so three cases covering the shape were added.

30. **The walk-forward now acts.** Its decision rule is written, pre-registered and mechanical: a measured bias is corrected only if it is robust across bootstrap block sizes, its sign holds in every era with enough cells, and the driver actually beats "no change" out of sample — and the correction strength is derived from the bias's own standard error rather than the typed half-strength the old rule used. Across all five records it adopts 9 corrections, watches 37 and declines 42.

    The single most useful thing it does is **decline PHDC's +1.12 profit bias** — the largest number this project has ever measured about its own method. That driver loses to "write down last year's number" at a skill of −1.87, and correcting a bias inside a forecast worse than no change is polishing the wrong object. The old rule had no way to express that.

    **What I have NOT done, deliberately:** applied the adopted corrections to the five studies. That moves delivered numbers a fourth time in one night, and WS5's own design says corrections feed the *next* edition. The four affected runs sit on the ratchet with their reason; AMOC already conforms. This is a natural place for you to say whether you want the re-scoring done in one pass or folded into each study's next re-issue.

31. **The valuation calibration is started, in the order that makes it evidence.** Its pre-registration is written, hashed and committed *before any data exists* — so "no lever was fitted to the gap" is a fact about the commit order rather than something I assure you of. It fixes two scores rather than one, because a fair value struck today is not a forecast of the price in three years and grading it as one would condemn a perfectly calibrated method by construction; it fixes the promotion order before any lever is tested, with a stop rule that halts the moment a lever would push the pooled bias across zero — that is the guard against stacking five individually-justified corrections into an overshoot, which is the failure that started this whole reassessment.

    The point-in-time archive's schema is committed with **no figures in it**. It refuses a bare value, a partial year, an absent year and an unregistered tier — I tested all four. Sourcing the 2013–2023 vintages is the next block of work and it is genuinely slow: about fifty-five figures, each needing a named institution and a date. I have deliberately not started filling it at 3am, because an invented vintage corrupts the very error it is scored on and does it invisibly — the arithmetic still reconciles.

32. **The macro archive has its first real data, and it is still deliberately unusable.** The equity risk premium and sovereign default spread are sourced for all eleven origins from Damodaran's archived by-year files — the premium that was *published at* each origin, not today's reading of that year, with both bases recorded and 2013 labelled rating-basis because that vintage carries no CDS figure for Egypt.

    Two extraction traps were caught before anything was written. Two of the files carry a **stale "Date of update" cell, four years wrong**, sitting beside a correct one — a first pass read the stale cell and would have misdated two vintages in an archive whose entire purpose is that the date is right. The second was quieter: the column headings change between eras, so a matcher written against one era returned nothing for the other and would have recorded a missing figure where one exists.

    The CPI series I can get freely is the World Bank's *current* reading of those years, not the print available at each origin. I have recorded it under its own field name so that it explicitly does **not** satisfy the point-in-time requirement, and every origin still reports unusable. A revised or rebased figure is fabricated in vintage even when it is right in value, and that is the quietest possible way to break this archive — right number, wrong date, invisible afterwards. Closing it needs the CBE bulletin or CAPMAS release of each year, alongside the sovereign yield and policy rate.


33. **The macro archive's inflation is now sourced, point-in-time, and the drift is large.** Six IMF World Economic Outlook editions published *before* their origins are in (Oct 2013, Oct 2015, Oct 2016, Apr 2017, Oct 2018, Oct 2019), each recorded with the checksum of the file it was read from. They give more than the origin year's inflation: they give the **forward path an analyst standing there actually had**, which today's series cannot supply at any price.

    The measurement that justifies the whole exercise, computed on the archive's own numbers rather than asserted: the inflation figure published *at* each origin and the figure today's series reports for that same year differ by **4.24 percentage points on average and 7.50 at worst, in both directions** (2017 +7.50, 2018 −6.46). A rebuild quietly using the modern series would feed the discounted cash flow an inflation rate several points from the one the origin had — in every escalator, in the currency path derived from them, and in the terminal.

    Underneath that sits a distinction I had to make explicit before the archive could be built at all, and I think it is right: **an observed figure and an estimated one need different evidence.** A market close or a central-bank rate is fixed at its date and nobody revises it, so today's database is a legitimate route to it. A price index is revised and rebased for years, so it is refused without naming the publication that existed at the origin. A figure filed in the wrong class is right in value, wrong in date, and invisible afterwards. The archive now requires the class on every figure and the vintage on every estimated one, and refuses all eleven ways I could think to break it.

34. **A refusal earned its keep the hour it was written.** The archive now refuses any figure published *after* the origin it is filed under unless the record says why a study struck there could have had it — deliberately with no grace period in days, since a cutoff would be a free parameter nobody measured. It immediately caught the 2015 country-risk vintage: the archived file carries "Updated July 1, 2016", a **mid-year re-publication six months after its origin**, and the January-2016 original is not held. It may embed first-half-2016 information. That origin is now marked compromised rather than used as though it were clean.

35. **Two fields I cannot source, and this is the one thing I would ask you for.** The 10-year Egyptian government bond yield and the CBE overnight deposit rate, at each year-end 2013–2023. Both are *observed* figures, so this is a pure access problem and not a point-in-time one. Every route is recorded in the file with its outcome: **cbe.org.eg refuses at the proxy on every path** — the statistics pages and the static PDF paths alike, the same refusal I hit on the Q2-2026 Monetary Policy Report; FRED returns bot-protection; the IMF's data service host does not resolve; the market aggregators render by JavaScript.

    The IMF country reports *are* reachable and I read them — but their treasury-bill row is a **fiscal-year average of a 3-month bill** where the house discounts on a 10-year year-end yield, and recording that as the sovereign yield would be an instrument substitution wearing the right field name, which is exactly the error the archive exists to prevent. So every origin reports unusable, which is the archive working rather than failing.

    **What closes it:** a CBE or Ministry of Finance export of those two series at each year-end — the same shape of file you already send for prices — or a dated market-data export of the 10-year yield. Five minutes of your access is worth more than another night of mine.

36. **The measurement nobody had taken — and it does not say what the framing expected.** The reassessment was called because the house looked systematically pessimistic. That is a claim about `log(fair value ÷ price)` across the delivered book, and nobody had ever computed it. It is now computed, through the gap gate's own reader rather than a second one.

    On the eleven studies whose answer is readable and positive, the mean sits at **−5.8% against price**, with a 95% interval of −15.6% to +5.6% once the resampling respects that eleven names in three markets on nearly one date are not eleven independent observations.

    The before-and-after on the five rebuilt names is the more interesting number, and it is not the one I expected:

    | | before | after |
    |---|---|---|
    | mean log(FV/P) | −0.0310 | −0.0253 |
    | mean **\|**log(FV/P)**\|** | 0.3033 | **0.0824** |

    The lean barely moved. **The dispersion fell by a factor of 3.7.** Before the rebuilds the five names spanned −74% to +50% against their own prices; after, the log-defined ones span −9% to +13% (that range excludes EGCH, whose −108% is the widest disagreement in the book and falls out only because a negative central has no logarithm — I have named it rather than letting the tighter range flatter the result).

    So the house was not uniformly pessimistic. **It was inconsistent** — reading one company far below the price and another far above it — and one macro path, one primary lens, a checked bridge and a cost-of-capital ladder are aimed at exactly that. I want to be plain about what this does not say: agreeing with the market is not being right, it is being ordinary, and a method tuned toward agreement would score well here while knowing nothing. Whether the disagreement carried information is the gap-closure question, and a cross-section holding no subsequent returns cannot answer it at any sample size.

37. **Twelve of twenty-three studies cannot be measured at all.** Their committed numbers expose no central-and-spot pair, so they are not clean, merely unmeasured. The gap gate already carries them on its ratchet. Worth knowing that the figures in item 36 cover slightly under half the delivered book.

38. **The fair-value register was recording a superseded answer, and its own check reported `[ok]`.** EGCH's latest recorded edition sat at 3.76 while the delivered study published −1.06 — a 129% movement of the very quantity the register exists to track, invisible to the thing tracking it. The check asked whether a ticker had *some* recorded fair value, never whether it was the *current* one.

    That is the third instance this session of one failure shape: an artefact checked for **existence** rather than **currency** — the gap gate green-lighting a review written for a superseded answer, ARCC's own gates opening a superseded workbook, and now this. The check now compares every record against the study's own committed central, and an unreadable answer fails rather than passing quietly. EGCH edition 3 is registered.

39. **The branch is now a pull request — [#336](https://github.com/sherifomarsaleh/testahil/pull/336) — and I have not merged it.** Forty commits: six standing rules, their gates, eight negative controls, five studies re-issued. All thirteen gates and all eight negative controls green, campaign queue and fair-value register green.

    **The recommendation is to merge it, and the reason is not tidiness.** A rule that sits on a branch binds nothing: the next study starts from a fresh clone of `main`, and `main` carries none of this. That is [R-MERGE-01]'s own argument and it applies here at programme scale rather than at one name's. I have opened the PR unprompted as that rule requires but stopped short of merging, because the rule's merge half is written for a campaign name and this is forty commits rewriting both governing documents — a decision I would rather you took at a glance than have me take while you slept.

    Merging moves `fair{}` in the repository, not on testahil.com. **Nothing publishes to the live site**, and nothing will without the word.

40. **The founding question, answered on the whole published book — and the answer changes what to do about it.** I built the dated vintage archive the programme was missing (`engine/fv_vintages.json`: 103 fair values across 90 names, 11-Jun to 01-Sep 2026, each with the spot recorded beside it at the time), and measured every one against its own price.

    | | |
    |---|---|
    | mean log(FV/P) | **−10.6%** |
    | **median** | **−0.3%** |
    | below the price | 46 of 90 (51%) |
    | mean absolute gap | 26.5% |
    | 95% interval, clustered by exchange | −25.2% to +6.6% — straddles zero |

    **The median name sits three tenths of a per cent from its price and the split is a coin flip.** The −10.6% mean is entirely a tail: ten names read more than 40% below their price against three more than 40% above. The typical *disagreement* is large in both directions; the typical *position* is neutral.

    That is a different diagnosis from "ridiculously pessimistic", and I want to be plain about why it matters: **the obvious remedy would have been the wrong one.** A uniformly pessimistic house is fixed by moving a rate or a terminal — one change, whole book. A well-centred house with a long left tail is fixed by auditing the tail names one at a time. Had I acted on the mean, every centred name would have been pushed off its price to correct ten that were wrong.

    Two limits, stated in the output rather than left implied: these vintages were struck on different dates under different standards and most predate the reassessment, so this is a picture of the *book*, never a measure of one method; and it measures agreement, which is not accuracy.

41. **The tail, named — and a question about the order of Phase 2.**

    | | | |
    |---|---|---|
    | ELEC | −84.5% | study, no gap review |
    | EGCH | −74.0% | rebuilt, reviewed |
    | KABO | −73.8% | **no study directory** |
    | IHC | −71.9% | **no study directory** |
    | OIH | −58.5% | **no study directory** |
    | RMDA | −56.4% | **no study directory** |
    | DSCW | −55.1% | **no study directory** |
    | PHAR | −52.9% | study, no gap review |
    | CLHO | −48.0% | **no study directory** |
    | EFIH | −42.6% | **no study directory** |

    These sixteen names (the table shows ten) are the whole of the book's lean, which makes them the highest-value rebuilds in the programme.

    **The question: should Phase 2 follow this order rather than the campaign's market order?** I have not changed anything — the campaign queue still runs EGX → UAE → KSA and so on. The argument against re-ordering is real and I think it is the stronger one: the market order exists so a method is tested across a whole market before it travels, and starting with the largest gaps would test it first on exactly the names most likely to be unusual. But it is your call, and leaving it unasked would have been the wrong kind of quiet.

42. **Seventy-six per cent of what the site publishes is outside every gate's population.** 68 of the 90 published fair values have no study directory. Every construction gate — bridge, lens, cost of capital, macro coherence, valuation gap, workbook structure, output records — globs `engine/*_study/`, so each is correct about the population it names and **silent about 68 numbers a reader can see on the site today**.

    The shortfall itself is not news; the fair-value register already records that most covered names carry no current-standard study. What is new is the consequence measured: the gates report clean over a quarter of the book. That is [R-ENF-04]'s own question one level up — a population anchored on study directories, applied to a book anchored on `data.js`.

    **And the obvious inference is wrong, which is why I computed it instead of assuming it:** the 22 names *with* a study average −20.3% against price; the 68 *without* average −7.3%. The examined names carry the larger discounts. It is confounded — a study gets written where the house has a view, and several of these are the names deliberately audited — but "the unexamined ones are where the errors are" is not what the numbers say.

43. **A reader that invented a company, caught before the archive was trusted.** The first version of the vintage reader used a regular expression, and a nested horizon object (`hz:{...}`) let a non-greedy match run past its closing brace and swallow the next name's fair value — producing **sixteen vintages for a ticker that does not exist**, and 93 names where the file holds 90. That is the [R-ENF-03] lesson exactly: a checker that models the parser is reading a different file from the one that ships. It now loads each historical file with `node`, the way the site does, and counts what it read against the file's own total. A second version of the same disease: the walk included branch commits, so a value that lived on a branch for a few hours read as a published vintage and AMOC showed twelve, alternating within a single day. It now walks the published line only.

44. **The calibration's scorer is written and it refuses to produce a number.** The vintage archive starts 11-Jun-2026 and the fundamental lens speaks to horizons of up to a year, so the first fair value cannot be graded on its own clock until **11-Jun-2027 — 281 days away**. The scorer says that rather than printing a figure.

    The refusal is the substance, not politeness about it. Three months of subsequent prices *do* exist, and a one-to-three-month score could be printed today and would look like evidence. It would be evidence about the price cone's question, which has its own calibration and its own published record. That is the mistake the technical calibration caught in its own first edition — a sub-monthly read graded at three months, reporting the weakest available version of every claim it made. **A lens is graded over the horizon it is used for.** The archive is the instrument; it had to exist before the clock could start, and now it does.

    The gate that protects the calibration's central claim — that no lever was fitted to the gap — reads **commit order**, not the document. Every such document asserts it was written first; only the repository can establish it. The pre-registration's commit must be an ancestor of every score file's, and the document must still hash to its seal.

45. **Two things went wrong last night that I want you to hear from me rather than notice later.**

    **(a) I told you every gate was green while CI had been red for a day.** The claim was not a lie and was not true: I ran the `scripts/check_*.py` suite by hand, and the failing step lives *inline* in the workflow and was never on my list. I had been checking a different population from the one CI checks and could not see the difference, because my sweep came from a list I maintained rather than from the workflow.

    The failing gate turned out to be worth finding. `Cost_of_Capital_Reference.md` is compared byte-for-byte against its generator's output, and the generator stamped it with today's date and with the sovereign quote's age *in days* — so it went red every midnight without a line of the repository changing. That is the permanently-red check the protocol forbids, in its purest form, and by the time it was caught a red gate on this branch was already background noise. The document now carries the date its *paths* were sourced, which moves only when the content moves; verified by rebuilding under a faked 2027 clock and diffing.

    **(b) A script I wrote to prevent (a) then rewrote the checkout.** It ran every workflow's steps against the live working tree, and reached one that rebases and auto-commits: the checkout was left mid-rebase on a detached HEAD, the calibration directory was emptied on disk, and an uncommitted file was swept into an auto-generated commit describing something else. **Nothing was lost** — everything was already pushed — but that was luck about timing, not design. A CI step assumes a disposable runner and this checkout is not one. Any step containing a repo-mutating verb is now refused by name, and the run-everything mode is deleted rather than made safer, because its safe configuration is exactly the thing nobody remembers.

    I have left the misleading auto-generated commit in place rather than rewriting history over it, and said so in the commit that follows it.

46. **[R-VCAL-01] is adopted in both governing documents, and the digest is renamed for today.** The rule the whole reassessment has been building toward: **the fair value itself is graded against what happened, on a design committed before the data.** Full account in `Standing_Research_Protocol.md`, condensed paragraph in the digest, one commit, both stamps at `2026-09-03a`. Per [R-DOC-01] this is the first edit of a new day, so the digest is now `engine/PROJECT_INSTRUCTIONS_03-09-2026.md`, the revision letters restart at 'a', its own self-reference moves with it, and CLAUDE.md's include line — the one reference that cannot glob — moved in the same commit.

    **I owe you the full digest text in chat and it will come with this list**, since you paste it into your own project files and a diff would leave that copy silently behind.

    The block says: no fair value this house ever published was graded; the order of construction is the whole claim on credibility; two scores rather than one, because a fair value struck today is not a forecast of the price in three years and grading it as one would condemn a perfectly calibrated method by construction; a lens is graded over the horizon it is used for, and the scorer refuses rather than oblige; the observed-versus-estimated split; promotion sequential, ordered in advance, stopping the moment a lever would push the bias across zero, with a symmetric guard. And the finding that changed the diagnosis, with the live command to read it rather than a number that moves.

47. **A gate that compared two populations when there were three.** [R-DOC-01] requires a rule's identifier to appear in the full protocol, in the digest **and in the code that enforces it**. The sync gate compared the two documents to each other and printed, for information, which rules the code enforces — but never asked the reverse: is there an `[R-...]` cited in code that resolves in *neither* document?

    It was not hypothetical. `[R-VCAL-01]` was cited in eight files including a pre-registration and two gates, and existed in neither document, while the gate reported perfect agreement. **A rule id that resolves nowhere reads to every later session exactly like settled law.**

    Its first run found a second one that is not mine: **`[R-BETA-01]`**, cited in `engine/build_depth_audit/build_protocol_review.py`, where the documents carry `R-BETA-04` and no `R-BETA-01`. Either a renumbering left a citation behind or an identifier was invented at the point of use. It is on the ratchet with that note, and it is resolved by *reading that file* — never by inventing a rule to fit the id. R-VCAL-01 was pruned off the same ratchet an hour after being seeded on it.

48. **WS9 — what the new standard costs the rest of the book.** `engine/method_reassessment/ws9_report.py` answers it mechanically, built from the gates' own ratchets rather than by re-running the checks, because each gate already records which studies it is letting through and why.

    **The first thing it says is about its own population.** Of 90 published fair values, 22 have a study directory and **68 do not** — for those there is nothing for any gate to open. They are not passing; they are unexamined, and they clear by being *built*, not by being re-gated. A queue listing only the failures would describe the smaller half.

    Among the 22, nineteen are outstanding on five or six of the eight checks. The five rebuilt names are the exception, and their remainders are specific rather than structural: AMOC and EGCH carry no cost-of-capital schedule record; **ARCC's is recorded and the gate reads two real defects in it** — the mid-year discount convention it cannot see, and the disclosed 833bp gap between the adopted cost of debt and the latest independently computed effective rate; PHDC and TMGH are down to the walk-forward alone.

    Three ratchets were also carrying names that already conform — AMOC, ARCC and EGCH pass the macro, lens and bridge gates on the records added when they were re-issued and were still listed. Pruned. A ratchet holding a name that no longer needs it is how an allow-list quietly becomes an exemption nobody rechecks.

    **Nothing here changes the campaign's order.** It is a report and a queue; the market order and the hard stop after EGX stand.

49. **ARCC's discount factors were flagged and the factors were right — one real question is left.** The gate tested end-of-year arrival; ARCC discounts each year to its own midpoint off a valuation date halfway through FY2026, so its first factor is a quarter-year stub. Measured off the committed record, the cumulative discounting runs 0.25 / 0.94 / 1.88 / 2.83 / 3.79 years. [R-COC-01] requires *one date, one price of time* — which that obeys — and nowhere mandates year-end arrival. **The defect was never the convention; it was that nobody wrote it down.** A record now declares its convention (times *and* the calendar each forward rate owns, without which the factors do not reproduce) and the gate checks the factors against what was declared. A record that declares nothing still gets the old test. No ARCC number moved: 46 insertions, 0 deletions, central unchanged at 53.4593.

    **What is left is real and it is yours.** ARCC's adopted cost of debt sits **833bp from the latest independently computed effective rate**, against [R-COC-01]'s 150bp bound. The study discloses it rather than smoothing it — the debt book re-based mid-year from pound facilities to euro term debt, so a full-year average understates the marginal cost, and the disclosed rate is the honest one. But the rule as written has no exception, so the gate is right to fail it.

    Three ways out and I have taken none of them: adopt a rate inside the bound (which I think is wrong — it would be the smoothing the rule elsewhere forbids); widen the bound (a free parameter, which the promotion rule forbids); or add a **named, disclosed exception** for a book that re-bases mid-period, with the evidence required to claim it. I would take the third, and it is a rule change, so it waits for you.

50. **The rule-id ratchet is empty, and `[R-BETA-01]` was a false positive of my own new check.** It was never a citation: the protocol-review page's proposal that rules be tagged illustrated the *form* of an identifier with an invented example beside a real one. Replaced with `[R-AREA-NN]`, the placeholder notation the protocol itself uses — more accurate than the invented example, since the sentence was always about the shape of an id. The check cannot tell an example from a citation and should not try; writing examples in a notation that cannot be mistaken for a real id is the fix.

51. **The mechanical fair value cannot be built, and now I can say exactly why rather than argue about lenses.** Two constructions were declared for it and both were shaped by the same constraint nobody had measured: whether the input exists at all. `bridge_inputs.py` measures it — per name, per origin, which of cash, debt, capex, PPE, depreciation, working capital and a footed share count each run actually carries, and which file carries it. **Not one of 55 name-origin cells has a complete bridge and a capex figure.** Three (TMGH 2020–2022) allow capex to be derived by the identity `capex = ΔPPE + D&A`; five more (PHDC 2015–2019) have the bridge and no route to capex at all. Eight cells, two names, both developers.

    **What rules it out is the direction of what is missing, not the count.** No cash understates equity value, no capex overstates it, working capital does either depending on growth — so an instrument built from whatever each cell happens to carry has a bias whose *sign changes from cell to cell*. That is worse than a large bias: it cannot be corrected, disclosed as a direction, or reasoned around, and where it happens to run the same way as the hypothesis under test it confirms it by construction. On AMOC, a net-cash company, the missing cash is most of the answer.

    Every missing item sits on a statement those runs had already opened and parsed cell by cell. So [R-FCAL-01] is amended: **a run now commits a valuation-input block beside its driver panel** — cash, interest-bearing debt, PPE, D&A, the working-capital lines, and the share count with the par value it foots against. Enforced, ratcheted forward so no existing run goes red, negative-controlled on thirteen conditions. Not carrying those figures is not a gap in a table; it is that no valuation this house makes can ever be rebuilt at a past origin, permanently, for any year whose filings are no longer to hand.

52. **Share counts: TMGH's six years are footed *and* corroborated, and the method caught a real movement.** Its capital note is a chronology of general-assembly resolutions whose *first* paragraph reads "issued and paid-up capital amounted to LE 6,000,000" — three orders below the capital in force — so the parser that works on PHDC is defeated by it, and "take the largest" fails on the 2010 capital reduction. The recital is resolved against a **second, independent** source instead: the paid-in capital the walk-forward already committed for that year from that year's own earnings release. The count is then that capital divided by the par the note itself states and foots against. FY2025 comes out at 2,060.65mn against the recital's 2,063.56mn — the treasury reduction the recital cannot see, −0.141%.

53. **A gate now checks that a calibrated name actually ships what the protocol says it ships — and its first run found one.** You raised this: every calibrated stock has to end with a valuation report, its PDF and an Excel model. It was already the rule; nothing checked it. `check_calibration_deliverables.py` holds every calibrated name to a report, its rendered PDF, a workbook, a standalone bibliography and a QC gate — **all of one edition**, which is the check that catches a fresh report shipped beside last edition's workbook. **TMGH's edition 2 (02-09-2026) went out with edition 1's QC gate beside it.** Listed and queued for the audit rather than waived away.

54. **[R-LENS-03] is green in every record and false in fourteen of twenty documents.** This is the one I would want you to see. The rule retired the typed multi-lens blend, and the gate enforcing it reads each study's committed lens record — where it passes everywhere. A reader does not receive the lens record. Reading the delivered PDFs instead: **6 clean, 14 publishing a weighted central as the study's own answer.**

    **ARCC was re-issued *after* the rule** and its document prints "END — this study's weighted central **54.65** · four lenses, weighted" on 50/20/22/8 weights, beside a numbers file carrying 53.46. Two centrals in one delivery, and the one a reader sees is the retired one. **ADNOCLS is the model report** — twenty-two such assertions, including its own synthesis row. `CLAUDE.md` says to open it beside every study being written, so until its edition is rebuilt the exemplar is teaching the retired architecture, and a new study can be perfectly compliant with its instructions and in breach of the rule. That is why it goes to the *front* of the re-issue queue rather than the back.

    Every gate missed it honestly: the lens gate reads the record, the workbook gate reads sheet names, the external-reader scrub hunts internal-procedure vocabulary and "weighted central" is ordinary English, and a blend recalculates perfectly. [R-ENF-03] said a checker that models the artefact is checking a different file from the one that ships — adopted for a JavaScript parse and never generalised to documents. Now it is: `check_lens_vocabulary.py` reads the delivered PDF, and deliberately does *not* fire on a study explaining that the blend was retired, because a gate that went red on PHDC's honest sentences is the check everybody learns to ignore.

55. **AMOC is blocked, and I got the size of it wrong before I got it right.** Its helper for pricing contested choices, `_val_at()`, does not reproduce the study's own model. Run at the study's **own adopted rates** it returns **EGP 10.8572** against the delivered **EGP 9.9142** — **9.51% apart**, on identical discount factors.

    Two independent causes, both measured. **The terminal is struck on a different capital base**: the delivered one is computed on invested capital at *replacement cost*, which is the study's own stated construction; the helper re-derives it from the forecast invested-capital series, giving a terminal value of 17,504.6 against the delivered 15,691.4, +11.56%, and an enterprise value 6.28% higher. **And the bridge**: the helper deducts the minority as a share of *enterprise* value — the construction [R-BRIDGE-01] forbids in as many words — and omits provisions, the dividend payable and investments.

    **A correction to what I wrote earlier today.** My first version of this item re-based the published alternatives onto the delivered bridge and printed a like-for-like column. That column is withdrawn: it assumed one divergence where there are two, so correcting the bridge alone does not give a like-for-like figure. The note in the study directory records the withdrawal rather than quietly replacing it.

    **What makes it worse than a stale helper is what else it drives.** `_val_at()` prices every cell of §1.9's sensitivity grids as well as the three contested choices, so the **at-assumption cell of both two-dimensional grids reads 10.8572 against the study's own headline of 9.9142**. A reader who looks at the sensitivity table and then at the answer finds them 9.5% apart with nothing explaining it. The beta grid is the exception and lands exactly on 9.9142, which is how I could tell the others were not merely rounding.

    The fix is not a patch: the helper has to reproduce the study's own model at the centre — replacement-cost terminal, then the delivered bridge — and the test is arithmetic, that at the adopted rates it returns 9.9142. Until it does, no alternative it prices is worth printing, which is why this note now prints none.

56. **EGCH's reverse read was already in the model and had never been written down — and it says something worth reading.** `compute.py` has carried `implied_flat_wacc()` all along and commits the answer on both sides of the binary judgement; nothing ever emitted it as a record, so the gate could not see a diagnostic the study had already computed. Now it does. **At EGP 13.98 the price implies a flat nominal discount rate of 9.2% if the ANNA programme is carried through and 10.2% if it is stopped, against this study's 25.6% falling to 21.6% — and against a sovereign ten-year yield of 23.0%.** On either branch the market is discounting this equity at a rate *below what the government of Egypt pays to borrow*, less than half of it on the committed-capital case. That is not a disagreement about tonnes or prices; it is the market pricing the equity as though these cash flows were safer than the sovereign, and stating it that way is more useful than "we are 92% below".

    Both sides are solved rather than one, because picking a side to solve on would make the choice the study deliberately declined to make.

    The contested record says what it **cannot** measure, which matters more here than what it can: EGCH prices exactly one construction both ways, so its sign test rests on a single observation and is not a measurement of this study's lean. Three others are contested and named and none carries a committed value on the other framing — the ANNA terminal margin (the central takes the lower of a built and an assumed figure, because a ~66% cash margin on a commodity fertiliser is not credible), the derived nameplate, and the ERP basis. Pricing them is a re-issue.

57. **A containment check was failing EGCH for doing the right thing, and it was re-pointed rather than widened.** `assert_reverse_dcf()` refuses any study whose builders read the reverse read back into the model — the reverse-engineered rate arriving through a side door. It flagged EGCH's `compute.py`, which opens `../egch_walkforward/diagnostics.json`: a *completely different file*, the walk-forward's own per-driver error diagnostics, which [R-FCAL-01] positively asks a study to carry into its document. `diagnostics.json` is not a reserved name. The check now tests whether the reference resolves inside the study, and the negative control gained a case for exactly this — with the real leak still going red beside it, which is the only thing that proves the fix was not a switch-off. That is [R-COC-01]'s own lesson in a different place: when a check fires on work that is right, the answer is almost never to widen it.

58. **The blend cost the book about six points of value at the median, and forty on its worst name.** [R-LENS-03] was adopted on one observation — PHDC's cash-flow lens landed within 2.2% of the market while its blend landed 28% below. One name is not a pattern, so I measured it across every study that commits its per-lens values (`engine/method_reassessment/lens_recentre.py`, read it live).

    Of the eight studies that actually carry a blend, **the published central sits below the class primary on six**, median **−5.8 points of spot**, mean −10.8, range −40.6 to +13.0. Furthest down: **DU −40.6 pp, MODON −37.0 pp, RIYADHCABLE −17.7 pp**. The other way: SWDY +13.0, SAVOLA +8.9. Three more studies contribute a zero because their central already *is* their primary — migrated by hand — and those zeros are reported separately rather than left to drag the median toward nothing.

    **This corroborates the delivered-book finding from a completely different direction, and it says the same thing:** a near-zero median with the mean living in a tail. The blend was not a uniform drag on the house's answers. It was a mechanism that mostly did little and occasionally did a great deal of damage — which is worse to live with than a constant bias, because a constant bias can be corrected and this cannot be predicted from the outside.

    Two extractor bugs found and fixed while building it, both of the shape that produces a tidy wrong number rather than an error: PHAR's `w_dcf = 0.5` is the DCF's *weight*, and a substring rule read it as a fair value of EGP 0.50 against a spot of 130.05 — a perfectly plausible-looking −99.6%. And ELEC's cash-flow lens carries bear 0.01 and base 0.01, a floor rather than a central; it is excluded from the pooled figures and named, because one floored cell should not decide the book's answer. Studies that publish their primary in two framings (ADNOCDIST, PHAR) are reported as such rather than having one picked for them.

59. **TMGH's edition was audited from outside and it is NOT deliverable — fourteen defects, four material, and every repo gate reported clean.** The QC gate for it is `engine/tmgh_study/QC_GATE_02-09-2026.md`, and writing it also cleared the deliverables ratchet the new gate had raised. What blocks the edition:

    - **Both delivered documents are dated 1 September** against a 2 September edition — the date is typed in `docx_tmgh.py` while the workbook reads it from the numbers file. The knock-on is a document telling a reader the sovereign quote is 26 days old against its own record's 27.
    - **The §1.1 bridge does not divide.** Equity EGP 244,183mn ÷ 2,060.7mn shares is **118.50**; the page prints **113.24**. The workbook computes 118.50, so the document and the workbook disagree on the same case, and `assert_bridge()` passes because the committed record is a third case.
    - **§1.5 is the previous edition's prose on this edition's numbers** — "the twenties to sixties" against cases of 43.89–123.03.
    - **[R-MACRO-01] twice.** Three long-run growth rates in one document, and hospitality compounding at 20.0% for ten years so that total revenue grows **19.8% in the last explicit year against a declared 7.00% terminal**. The declared field is what the checker tests. Separately, "flat in real terms" is **+5.88% a year real** on the study's own path, and an `exempt_reason` is what stops the assert testing it.

    **Which of these I checked myself.** The bridge one, because it is the sharpest and I nearly “corrected” it wrongly: reading the valuation-summary table, 118.50 and 113.24 are two separate columns and both are fine. §1.1 is a different table, and it is the one the audit means — it deducts the minority *at its share of value*, reaches EGP 244,183mn, states 2,060.7mn shares, and prints **113.24**. That bridge does not divide. The document date and the §1.5 prose I read in the delivered PDF and both hold. The [R-MACRO-01] growth figure I have now confirmed from the delivered workbook itself: the Summary Financials sheet's own revenue row grows 16.9 / 20.4 / 22.0 / 22.4 / 22.1 / 21.6 / 21.0 / 20.4 / **19.8%** across the explicit window, against a declared terminal of **7.00%** — 12.8 points apart where [R-MACRO-01] requires the window to run until growth is within 2. The checker tests the declared field, so it passes.

    **The audit also corrected two things I had told it.** I briefed it from `STATE.json`, which said this edition's central was 69.92 against 97.80, −28.5%. The committed numbers say **91.83 against 97.80, −6.10%**, and `fv_movement` records the delivered files as **edition 3**, not the class-A interim. It checked the brief against the artefacts instead of repeating it, which is what an audit from outside is for; `STATE.json` is corrected and the correction is recorded in place rather than overwritten. A stale number in the live status is the same defect this project keeps closing everywhere else.

60. **One finding I am recording rather than acting on, because acting on it would weaken a rule.** The audit called an [R-ENF-05] side door: TMGH puts `implied_discount_rate` — a rate solved from the traded price — into `study_numbers.json`, which the rule forbids in as many words ("NEVER in the numbers file builders read"), and `assert_reverse_dcf` misses it because it greps for the literal string `diagnostics.json` and exempts `lenses.py` by name.

    Checked every use: workbook cell, bibliography, document prose, expert appendix, gap review. **All display. Nothing computes from it.** So TMGH satisfies the rule's *purpose* — no price-solved quantity re-enters the valuation — and breaks its *device*. The device exists precisely because the purpose is not statically checkable, so widening the check to allow "display only" would delete it rather than sharpen it. The honest resolution is to move the figure and to replace those two unexplained by-name exemptions with a named path, and that is a study change plus a rule clarification, not a patch. Left on the list.

61. **Two PDFs would unblock 53 studies, and I cannot reach either from here. This is the one thing on today's list that is genuinely yours.** [R-MACRO-01] requires one sourced house macro path per market and **only EG is sourced**; AE, SA, QA, IN, KR and US all read PENDING and *raise on load*, by design. That is not a formality — it means **no non-Egyptian study can be re-issued to the new standard at all**, which is 53 of the book, ADNOCLS among them. And ADNOCLS is the model report, so it sits at the front of the re-issue queue and is blocked at the very first step.

    I tried to source the UAE path today. What is reachable and what is not is now recorded in `engine/macro_paths/AE.json` under `sourcing_attempts`, so nobody spends this hour again:

    - **Reachable.** The World Bank's open-data API gives UAE CPI *actuals* (2025 1.25%, 2024 1.66%, 2023 1.63%, 2022 5.29%, series updated 13-Jul-2026) — it is already the source PHDC's walk-forward uses. Abu Dhabi's SCAD serves its emirate-level CPI.
    - **Blocked.** The **Central Bank of the UAE** sits behind a Cloudflare challenge — its interest-rate endpoint returns 403 with a "Just a moment…" page and the Quarterly Economic Review and Base Rate PDFs 404 behind it, to curl *and* to a headless Chromium. The **IMF** returns 403 to curl and a connection reset to Chromium — **the same access limit already recorded against the five WEO vintages** the point-in-time macro archive needs. One limit, two consequences.

    The figures themselves are not obscure; secondary reporting of both is easy to find. **I am not using it,** because [R-MACRO-01] wants a level published by a named institution on a named date, and a news summary of a central-bank forecast is neither the institution nor the date. That is the rule doing its job rather than an obstacle.

    **What I need:** two documents — the CBUAE *Quarterly Economic Review* (its inflation forecast table and the Base Rate) and the IMF's latest UAE staff report or Article IV (its medium-term inflation projection). Attach them the way you attached the Egyptian rate series and I will build AE, and the same two institutions cover SA, QA and the rest.

    **The default if you say nothing:** I keep working the Egyptian book, where everything is sourced — AMOC's and TMGH's re-issues, and the EGX names on the lens-vocabulary ratchet. Nothing stalls. But the non-Egyptian half of the programme stays blocked, and it will not unblock itself.

62. **Four of the five studies leave the reverse read's side door open, and none of them walks through it.** [R-ENF-05] says the quantity solved from the traded price *"lives in the study's own `diagnostics.json`, **NEVER** in the numbers file builders read"* — and until today `assert_reverse_dcf()` only checked the second half of that sentence, that no builder reads the diagnostic back in. It now checks the first half too, by looking for the diagnostic's **own value** inside `study_numbers.json`. That is checkable without guessing at vocabulary: a float carried at full precision does not appear there by coincidence.

    It found the value committed in four of five: **AMOC** at `/gm_required/level`, **EGCH** at `/drivers/implied_wacc_base`, **PHDC** at `/derived/market_implied_cash_conversion`, **TMGH** at `/lenses/implied_discount_rate/capacity`. In every case every *use* is display — prose, a workbook cell, an expert appendix — and **nothing computes from it**. So the rule's purpose is met in all four and its device is broken in all four.

    **I did not relax the check, and the reason is the one [R-COC-01] states.** The device is the only part that is checkable: consumption cannot be told from display by static inspection, which is exactly why the rule keeps the value out of the file instead of policing what reads it. Widening it to allow "display only" would delete the check rather than sharpen it.

    **ARCC is the one that passes, and it shows the satisfiable shape**: the reverse read is computed outside the committed numbers by a module that writes `diagnostics.json`, and a builder that needs the figure for display computes it rather than reading it back. That is precisely what the two unexplained by-name exemptions in the assert (`lenses.py`, `docx_arcc.py`) were crudely marking — they are now removed in favour of the value check, which says the same thing without needing to know anyone's filename.

    Four names ratcheted with the fix stated, so nothing goes red today and each clears at its next edition. Negative control gains two cases and runs sixteen: a numbers file carrying the solved value must go red, one that does not must stay green.

63. **Your prices changed the picture, and the rule they exposed is now in the protocol.** The ninety closes you sent are committed at `engine/prices/SUPPLIED_03-09-2026.json` — a figure that arrives in a conversation binds nothing, because the container is rebuilt from the repository and the next session would ask you again.

    **Ten of thirteen readable studies breach the ±10% trigger against today's price, and three of them were inside the band when they were struck**: ARCC **−30.6%**, AMOC **−26.6%**, SAVOLA **−10.1%**. ARCC and AMOC are the two I re-issued today.

    **The cause is not a drifting method — it is a stale spot.** Six of nineteen studies carry a spot more than ten per cent behind the market: **AMR by 294%**, **AMOC by 48%** (EGP 9.10 struck on 6 August against 13.50 today), **ARCC by 31%**, SCEM 27%, SAVOLA 19%, SWDY 14%. A fair value published against a month-old price is a comparison a reader cannot use, whatever the fair value is worth.

    [R-GAP-01] has said "the latest known market price" since the day it was adopted and **the gate has never read one** — it reads each study's own committed spot, which is the price the study was struck at. That is the right test of whether a study was audited before it shipped, and it is not the question the rule asks. The amendment (rev 2026-09-03f, both documents): **no study is delivered against a stale price.** Before any delivery the central goes against the latest known price, the eight-heading review runs if the gap exceeds ten per cent either way, and the spot the study publishes is that same latest price with its date beside it.

    **On what the price is for, in your words — "to arrive at a realistic price that takes all circumstances into effect".** The rule now says that explicitly: a gap is evidence the model may have missed a circumstance the market has priced — a filing not read, a base year that no longer foots, a macro path contradicting itself, a bridge on a superseded sheet, a claim typed rather than computed. It is **never** a reason to move the number toward the price; a fair value adjusted to meet a quote is the reverse-engineered rate this house prohibits outright, arriving through the front door instead of the side one. The honest output of a review is often an unchanged central with a stated reason.

    **AMOC's edition is not shipping**, which was already true for seven other reasons and is now true for this one as well: at 13.50 its central of 9.91 is 26.6% below the market, and that review has to happen before its files are staged. Read the state live with `python3 engine/prices/gap_today.py` — never from this note, because the prices move and the note does not.

64. **ARCC's technical read is four weeks and 30.5% behind its own price, and only you can close that.** The price library at `engine/raw_ohlc/EG/ARCC.csv` ends **6 August 2026 at EGP 59.00**. The spot you supplied is **77.00 on 3 September**. Everything computed from the library is therefore anchored on a market the price has since left.

    **What that was doing to the delivered study, before today.** The levels table divided every support and resistance by the 3 September spot, so all six printed as large negatives and the **52-week high printed 21.6% BELOW the current price** — which cannot happen on one clock. The probability zones were worse: their boundaries were struck at 77.00 while their probabilities came from the simulation's own 59.00 anchor, so the study published a **51% chance of finishing above 77.00** from a distribution whose median is 60.46. Roughly three times the truth, in the one table whose entire purpose is to state probabilities.

    **Both are corrected and neither correction needs your data.** Distances are measured from the read's own close with that date in the column heading; the zones sit wholly on the anchor and name it; and the captions state the gap rather than burying it inside a percentage. The study now tells a reader plainly that the tape has run clear of every level this structure identified and that the read describes a market the price has since left.

    **What I did not do is invent the sessions we do not hold.** SIGCM clause 1 forbids it and there is no honest substitute: a technical read is a statement about a price history, and ours stops on 6 August. **A fresh OHLC export for ARCC — and for any other name whose library is more than a few weeks behind — is the only thing that fixes it, and it is the one item here that cannot be routed around.** Everything else in this programme has continued without it.

    Read the current library ages live with `python3 scripts/check_technical_read.py`, which prints the distribution and names every instrument past ten days — never from this note, because staleness moves by the calendar and the note does not.

65. **One document would settle a question about the whole method, and it is the only thing I cannot route around today.** AMOC's fixed-asset accounting-policy note — one sentence in it: does the depreciation charge write off **cost**, or **cost less an estimated residual value**?

    **Why one sentence matters this much.** The terminal rebuild programme rests on measuring how old a company's asset base is, and the only route to that is an identity off the accounts: accumulated depreciation over the year's own charge. That identity holds where the charge is cost over life and breaks where there is a residual. On 5 September I tested it on the four remaining names carrying the retired construction and **all four failed on exactly that clause** — ADNOCLS, ADNOCDIST, BOROUGE and AMR, companies that could hardly be less alike: an ocean fleet whose scrap steel is a real residual, a fuel-retail network, a polyolefins complex and a restaurant group.

    **That produced a hypothesis I do not yet believe.** The one name the route has unlocked, EGCH, discloses depreciation as *rates applied to cost with no residual* — the Egyptian presentation. All four failures are UAE filers using the IFRS residual-value form. **Four failures against one success, with one test left, and AMOC is that test** — the last name on the retired construction and the only Egyptian one remaining. If it writes off cost at rates, the pattern is real and the method has a second Egyptian success. If it writes off cost less residual, the pattern is refuted on its only outstanding test and turns out to be one company's presentation rather than one country's — **which is the more useful answer of the two, because it stops a false pattern before it becomes a house rule.**

    **What I ran before asking.** The study's own filings directory holds only a hand-made extract, whose own header records that its figures were "read visually from scanned filings (no text layer)" — the note-6 movement table is in it, the accounting-policy note is not. No AMOC filing has ever been committed on any branch. The company's own site and the Egyptian Exchange both refuse at the proxy with a 502, re-run twice each. The study's input register carries the charge, the accumulated balance and the per-class net book values, and no rate, life or policy quote anywhere.

    **Everything else about the name is already done**, so this is one sentence away rather than a fresh start: depreciable gross cost 2,665,058,507 over an annualised charge of 135,494,744 gives an implied life of 19.67 years, and accumulated depreciation of 1,847,794,418 gives a naive age of **13.64 years against a half-life of 9.83** — this base is thirty-nine per cent OLDER than uniform, the opposite of EGCH's.

    **The default if nothing arrives, firing 12 September: AMOC stays on the ratchet with its reason, and is NOT rebuilt on the naive age** — even though that error runs the safe way, because an overstated age overstates maintenance and understates the value. A safe direction is not a reason to keep a number the accounts may say is not measuring what it claims, and there is already a name in the register where exactly that argument was made and the figure withdrawn anyway.

    Registered at `engine/escalations.json` under `AMOC-depreciation-policy-note`, with the routes, the default and its date; the gate re-checks it against every live ref so it cannot go on asking for something already supplied. **Drop the PDF into `engine/amoc_study/filings/` and it closes itself.**

66. **The lens-registry question I raised yesterday now blocks nine names, not two, and it is holding a publication gate blind over a third of the book.** Yesterday it was SAVOLA and EMPOWER: [R-LENS-03]'s registry is a closed enumeration of thirteen industry names, a study must map into one to publish a lens record, and a grocer and a district-cooling utility map to none — while the rule forbids adding a row merely because the industry differs, and mapping a supermarket to the "telecom operator" row would put that label in the study's own record.

    **Today it turned out to be the whole of a group I was diagnosing for an unrelated reason.** Seven studies are invisible to the valuation-gap gate — it cannot read a central fair value out of them, so [R-GAP-01] cannot audit them and [R-GAP-02] cannot decide whether they may publish. I assumed the causes were mixed and some fixes cheap. They are not. **All seven are invisible for the same reason: each publishes a multi-lens combination the rule retired, and therefore no single central.** ADNOCDIST a typed 40/25/20/15 in two framings, ADNOCDRILL 25/25/20/15/15, ELEC 40/20/20/20 (its delivered document prints the words "Blend 40 / 20 / 20 / 20"), GBCO 40/15/20/25, STC 35/25/20/20, AMR 50/20/20/10, and BOROUGE the *median of nine readings across two beta framings and two scenarios* — not a weighted average, and caught by the same rule for the same reason.

    **And four of the seven meet exactly SAVOLA's wall**: fuel retail, restaurants, offshore drilling and cable manufacturing are in no row of the registry, and not one of them needs a lens the registry lacks. Every one is a cash-flow primary with a relative multiple and book beside it. So they do not need a new method — **they need a row whose name is not an industry.**

    **The recommendation is unchanged and the evidence for it has quadrupled**: name the registry's rows for the lens sets they actually store rather than for industries, and merge the three rows that already store an identical set into one — an operating company valued on its own cash flows, cross-checked on its own EV/EBITDA history, a relative multiple and book. That is not adding a class for an industry; it is naming the register for the thing it holds, which is what makes a closed enumeration closable. Nine names then map without anybody inventing a fit.

    **The default fires 18 September and takes exactly that route.** What has changed is the cost of waiting: this is no longer a taxonomy tidy-up, it is the reason a gate that governs publication says nothing about a third of the book.

    One honest caveat, carried from yesterday and still true: EMPOWER's blend carries a *normalised earnings* lens at 15%, and normalised earnings appears in no row of the registry at all. Even under the fix, that lens has to go — which is the rule working as intended rather than a further gap in it.

---

## 04→05 Sep 2026, second half of the night

**Nothing below needs a decision except items 1 and 5.** Everything else is reported because
it happened, not because it is asking.

1. **THE MODEL REPORT PUBLISHES A NUMBER A STANDING RULE RETIRED, and so do two other
   delivered studies.** [R-CAL-03] retired the skill verdict outright — "nothing on any
   public surface — no page, figure, document or deck". ADNOCLS's delivered study says "the
   three-month distributions scored **+2.95% better than a random-walk benchmark** anchored
   on the same cost of carry"; SWDY says "+1.50% better than a random-walk benchmark";
   ADNOCDRILL says "the map scored 1.65% **WORSE** than a simple no-information benchmark".

   The verdict-vocabulary gate was widened two days ago after ARCC shipped the same claim in
   different words, with a comment saying a rule like this "is not enforced by banning the
   word people happened to use for it last time" — **and it was then defeated by a hyphen**,
   because the patterns look for "random walk" and these three wrote "random-WALK
   benchmark". The patterns now match the shape of the claim rather than its wording.

   **The decision is yours because one of the three is the exemplar.** The fix is one clause
   in one builder each plus a document and PDF rebuild — small work, but on ADNOCLS it is a
   re-issue of the document every new study is copied from, and [R-ENF-01]'s exemplar clause
   says such a debt is either met or consciously added in the same commit. **I added it
   consciously rather than re-issuing the model report at four in the morning**, and it is
   now visible on the exemplar's debt list with the fix named. *Recommendation: re-issue all
   three in one pass, with the model report last and its rebuild verified page by page.*

2. **Four studies the publication gate could say nothing about are now readable and
   audited, and the ratchet fell from six to two.** AMR, ADNOCDIST, ADNOCDRILL and ELEC each
   carried their answer under a key the shared reader does not look at, so [R-GAP-01] had
   never seen them. All four now expose it and all four breach; all four carry a full
   eight-heading review; **every one of the four verdicts is that the gap is OURS.**

   | | central | latest price | gap | what the review found |
   |---|---|---|---|---|
   | AMR | AED 2.1455 | 2.39 | −10.2% | the blend, and an unsourced 6% wage escalator against a revenue line converging to 2% |
   | ADNOCDIST | 4.4113 / 4.5821 | 4.02 | +9.7% / **+14.0%** | a FY2026 needing a second half +9.9% above the reviewed first half when its own seasonality is +2.8% |
   | ADNOCDRILL | 4.9194 | 5.80 | −15.2% | **the blend and nothing else** — its two cash-flow framings straddle the price and their midpoint lands 0.04% from it |
   | ELEC | EGP 0.3357 | 2.08 | −83.9% | **not a valuation**: two lenses pinned at floors carry 60% of the weight and produce 4.2% of the answer |

   ADNOCDIST is the sharpest: **it was already breaching at strike on 9 August** and owed
   this review then. It did not get one purely because its answer sat where nothing looked.

3. **Three of the four name the SAME largest correction and none of them can take it** —
   retiring the typed multi-lens blend, which is blocked for all four by the lens-registry
   escalation waiting on you. Until tonight the cost of that wait was measured in
   readability; it is now measured in corrections worth +0.09 to +1.29 a share, **and on two
   of the four the blocked correction moves the answer AWAY from the price**, which is the
   shape that proves it is not being chosen for where it lands.

4. **Three gates were found blind, all for the same reason, and all closed.** The 1/g
   terminal gate had an unnamed third bucket and reported "no new terminal carries the
   construction" while ELEC carried it in plain sight in its own code — its resolver was
   also reading **bear cases** for two studies' growth and discount rates, and could not see
   a four-field input register at all, so the better-documented a study's input was the less
   visible it was. The verdict gate is item 1. And the gate whose whole purpose is to notice
   the exemplar acquiring debt read one ratchet layout out of four and reported **one entry
   where there were five**. Registered as one lesson: a gate's population is defined by a
   shape, and the thing it governs keeps arriving in another one.

   A fourth, found by the first three: the new-study gauntlet had **never tested the terminal
   gate**, because that gate takes the shared census module and the gauntlet decides its
   population by reading each gate's own source. Following the house's own advice is what
   hid it. Fixed by following imports one level down.

5. **ELEC should be withdrawn from coverage rather than re-issued, and that is your call.**
   Enumerating the company's own statement index rather than counting it: the index **ends at
   30 September 2025** — no FY2025 annual and no 2026 interims exist at all — **every file
   listed from mid-2021 onward is standalone**, and **every consolidated statement sits on a
   dead host**, 42 of 61 links. This study models consolidated figures. Its central rests on
   two clamps and its most consequential driver is justified against a year it holds no
   income statement for. *Recommendation: take the escalation's standing default and
   withdraw, rather than re-issue on aggregator data.*

6. **STC is ready to rebuild and GBCO is not.** Both carry a `wacc_reissue_blocked_on` field
   asking for their own sovereign's default spread — **and [R-MACRO-01] put those figures in
   the house macro paths on 2–3 September**, so both blockers were closed three days before
   anyone looked. A blocker written into a study's own JSON is re-checked by nothing, which
   is [R-IND-01]'s failure mode one level down from the register that rule does police.
   STC's five audited and reviewed statement sets are fetched and committed, its asset life
   is derived from its own note 10 (20.86 years, base 15.23 years old, 73% written off — the
   first name in five where the identity is not closed by residual-value depreciation), and
   its conforming beta is already on file at 0.7107 against the 0.48 the study actually uses.
   GBCO stops at the lens registry, which is item 3.

7. **Nothing was published.** Everything above is in the repository; the live site is
   untouched, and [R-GAP-02]'s Phase-1 clause continues to hold every study regardless.

## 05 Sep 2026, before dawn — STC rebuilt end to end

1. **PR #369 is merged.** All three CI gates green on `903e5628`; merge commit `3c170b9c`. Nothing needed.

2. **STC is rebuilt on all seven levers of its plan, and the route is the report.** Central **SAR 47.11 → 41.15**, −12.6%, against a latest known close of 43.86 — **−6.2%, inside the band either way**, so no eight-heading review is owed and the publication block does not fire on the gap. Under the reporting threshold you set, that gap needs no calling out; the *route* does, because two levers pulled hard in opposite directions and the net hides both:

   | lever | rule | move |
   |---|---|---:|
   | the sanctioned cost-of-capital schedule | R-COC-01 | **+8.4%** |
   | the beta re-derived against TASI | R-BETA-04 | **−13.8%** |
   | terminal growth on the house path | R-MACRO-01 | −5.2% |
   | the terminal on a 20.86-year derived life | R-TERM-01 | −3.2% |
   | the bridge on the 30 June 2026 sheet | R-BRIDGE-01 | **+3.6%** |
   | the four-lens blend retired | R-LENS-03 | −1.7% |
   | the answer published where it can be read | R-GAP-01 | 0.0% |

   The audit point was declared in writing before any lever was touched, taken where it was declared, and the cost-of-capital lever moved the answer **away** from the market before the beta lever brought it back. Nothing was chosen for where it landed. **No decision needed.**

3. **The single largest defect was not in the method but in a number nobody had re-read.** The bridge carried associates and joint ventures at **SAR 4,641mn against a filed 12,910mn**. That is a figure from before February 2025, when the group contributed its whole towers business to DIIC in exchange for 43.06% of it. The towers business the entire 2024 restatement was about had left the subsidiaries and arrived in the associates — **and the bridge had followed it into neither.** Worth 1.66 per share. No decision needed.

4. **The relative multiple was the traded multiple wearing a different hat.** The study used 8.0 / 9.0 / 10.0x EV/EBITDA with no source of any kind, and its base of 9.0 sat within a rounding of the **9.151x the shares trade at today** — which values the company at what it already trades at. It is now the mean of STC's own trailing multiple at the last three year ends, 8.762x, every one of the three below the traded figure so the lens can be *seen* not to be anchored on the price. No decision needed.

5. **A 20% share-count increase that never happened.** The reviewed 30 June 2026 balance sheet *prints* share capital as SAR 60,000,000 thousand against 50,000,000 at December. Note 17 says 50,000,000 at both dates, and only 50,000,000 makes the equity block foot to the stated total — it is an extraction artefact of that page. Taken at face value it would have cut every per-share figure by a sixth. Arithmetic caught it, which is what that rule is for. No decision needed.

6. **STC came off four ratchets** — the rebuild ledger, the bridge, the lens architecture and the valuation gap. **The valuation-gap ratchet now carries no breaching study at all**, and one unreadable one (GBCO).

7. **One defect was mine, and it is registered as L-342.** The first draft of STC's rebuild ledger read every lever's answer out of the study's *current* numbers file — the only place the answer lives — so the moment a fourth lever landed, the third lever's "after" silently became the fourth's. One lever read −18.3% where it was worth −13.8%, and another read 0.0% where it was worth −5.3%. **Nothing about that is visible in the ledger**: the chain still joins, the endpoints are unchanged, the cumulative figure is exactly right, and the gate that walks it passed both versions. Each landed lever now reads the commit that landed it. No decision needed.

8. **STC stays on the macro ratchet deliberately, and this is the one thing I want you to see.** Its four segment growth arrays are typed nominals with no source, date or layer, whose implied real growth wanders from 0.68% to 0.00% across five years with nothing saying why. They cannot be written as (real, house path) without *choosing* a real rate, and choosing one to clear a checker is the offence the protocol names in three places. The honest fix is the ground-up rebuild on the **eleven disclosed segments** the FY2025 filing carries with two years of revenue *and* gross profit each — materially finer than four typed arrays, and disclosed rather than assumed. That is the next block of work and it closes the macro ratchet at the same time. **No decision needed unless you want it sequenced differently.**

9. **STC is rebuilt, not delivered.** It still has no bibliography, no four-field inputs register, no sweep register, no QC gate, no driver test and no recalculation harness. Nothing about it has been published, and the publication block holds it anyway on the Phase 1 method-proof condition, as it holds every study in the book.

## 05 Sep 2026, still before dawn — an addition to item 8, and it changes the number

**Item 8 above said the ground-up rebuild on the eleven disclosed segments was the next block of work. It was done, and it moves the answer a long way.** What the earlier items say about the seven levers stands; what changes is where the study now sits.

10. **Central SAR 41.15 → 34.80, and the gap goes −6.2% → −20.7%.** Every segment now grows at **its own measured real rate** — from the company's own note 9, deflated by a published price index from the same IMF database and country row the house forward ladder comes from — instead of four typed arrays over a taxonomy the filings do not use. The measured rates are lower than the typed ones: **stc, two thirds of revenue, grows +0.16% real**; Channels −2.10%; Solutions +5.53%; the group +2.33%. Revenue compounds at 2.50% nominal against the delivered study's 3.71%. The margin is now an **output** — gross profit per segment at its own disclosed rate, less one cost line at its own three-year average share of revenue — rather than a typed EBITDA path.

11. **The eight-heading review is written, and the two defects it found both make the answer TOO HIGH.** Correcting either widens the discount rather than closing it, which is worth saying plainly because the instinct on a −20.7% gap is to look for what is missing on the upside.

    - **One is mine, from earlier last night.** The justification I wrote for terminal growth read "a mature domestic telecom growing with the economy in perpetuity" — and that sentence describes a *positive* real rate, since an economy grows by inflation plus real output and a company growing at inflation alone grows with prices only. **The number was defensible and the reason was false**, which is the more dangerous of the two because it survives review. Corrected in place: zero real means STC's share of Saudi output declines in perpetuity, and that is now written down as the real assumption it is. It is not moved, because any positive rate would need a source and telecom revenue has fallen as a share of output across most markets for two decades.
    - **One is structural and is recorded rather than resolved.** Terminal maintenance at current cost is **17.43% of revenue — essentially the top of management's 15.0–17.5% capital guidance** — while the explicit window takes capex *down* to 15.0%, the bottom of it. Free cash flow steps 17% at that boundary. The rule permits the two to differ where the reason is economic, and its example is a young plant spending less than replacement depreciation for a while. **This base is not young**: 73% written off, at 1.46 times half its own implied life. The step points the wrong way for the asset it describes, and the suspect half is the explicit window.

12. **The multiple cross-check argues hardest against the answer and I have set it out rather than explained it away.** The fair value implies **6.24x** enterprise value to forward EBITDA against a traded 8.98x and an own history of 8.32–9.13x. Three readings are given, and **the third cannot be ruled out**: a two-year trailing window is short, Channels fell 7% in FY2025 alone and may be a one-off, and if those two years understate the run rate then the whole forecast is too low and the gap is ours. What would settle it is the investor-relations channel — subscriber counts and revenue per unit — which would let revenue be built as volume times price instead of an extrapolated segment rate. **That is the next work, and it is named as work rather than accepted as a limitation, because a fair value moved to meet a price is the reverse-engineered rate this protocol prohibits outright.**

13. **Nothing about this changes what may be published.** The study was already held on the Phase 1 method-proof condition, and it is now held on the gap as well. Nothing is on the live site.

**The decision on item 12 is taken and reported as taken rather than put to you.** Two years is thin evidence for a growth rate on a business this size, the review says so in its own voice, and the study is held in any case — so the answer is not to widen the rate until the number is comfortable, which would be the reverse-engineered rate this protocol prohibits, but to go and get the disclosure that makes the rate unnecessary. **The work continues on the investor-relations channel**, where subscriber counts and revenue per unit would let revenue be built as volume times price. Say so if you want it sequenced differently; nothing waits on a reply.

*(This paragraph first put that choice to you as a question. It should not have: the rule here is that a choice which is reversible and inside the stated scope is taken, recorded with its reasoning and reported as taken — asking converts my work into your queue, which is the complaint the independence rule was written from. Corrected in the same hour rather than left standing.)*


## 05 Sep 2026, one more — the review's own logic paid out

14. **Item 11's second defect was priceable after all, and correcting it RAISED the answer.** The review named the explicit window as the suspect half of the capex tension before anyone knew which way a correction would run. The reason it was suspect turned out to be sharper than "an ageing base should spend more": **the capital-expenditure path was management's own published guidance band, taken straight in as an input**, and the standing rule is explicit that *guidance is scored and never consumed*, because a forward target leans the same way an optimistic model does.

    What this company actually spends is disclosed for three years, as a multiple of the depreciation of the base it renews: **1.054x, 1.252x, 1.176x — a mean of 1.161x**, which is 14.96% of revenue, *below* the guided path. Central **34.89 → 35.53, +1.84%**, and the gap **−20.5% → −19.0%**.

15. **The step at the terminal boundary is now larger, and that is the honest outcome rather than an awkward one.** The terminal charges 1.352x depreciation (maintenance at current cost on a 15.23-year-old base); the explicit window continues the 1.161x this company actually spends. An explicit window may continue an observed under-maintenance for five years; **a perpetuity may not**, because a company that never replaces its plant is not a going concern — and the accounts support that independently, with the base 73% written off and its measured age rising 13.60 → 14.18 → 15.23 years.

    **The industry-specific alternative is recorded rather than dismissed**: escalating at *general* inflation assumes a radio costs 2% more each year to replace, where telecom equipment has historically fallen in real cost per unit of capacity. If that holds, the terminal is too high and the 1.161-to-1.352 gap is priced equipment rather than deferred maintenance. What would separate them is a disclosed replacement-cost or capacity series, and this company does not publish one.

**Ten levers, nine rules, 47.11 → 35.53, −24.6%.** Every one is in the rebuild ledger with the answer either side of it, so the route can be walked rather than inferred from the net.

## 05 Sep 2026, last before the slot — the biggest finding came last

16. **PR #370 is merged** (CI green, merge commit `af036f12`); the anchor lever below is in **PR #371**.

17. **The most recent reviewed period had been read and was not used, and this is the largest single defect of the night.** The six months to 30 June 2026 are published and reviewed, and the model was growing FY2025 forward as though they were not. The standing rule is explicit that a near-term reviewed actual **outranks** a stale full-year rate — anchor on it, hold everything else flat including observed improvements, and where a first-half rate is carried into the second half *prove with the prior year's actual halves which way it runs*.

    | | reviewed H1-2026 | half-to-year factor | anchored FY2026 | the model had |
    |---|---:|---:|---:|---:|
    | revenue (SAR mn) | 40,110 | 1.00644 | **80,737** | 80,224 |
    | EBITDA margin | 32.33% | | **31.98%** | **31.09%** |

    **The forecast sat eighty-nine basis points below a margin the company had already reported for half the year.** Central **35.53 → 37.84, +6.49%**; the gap narrows **−19.0% → −13.7%**.

18. **It is the strongest evidence in the review because it is not a forecast at all.** It is a disclosed actual the model had not been shown. A model that has not seen the half-year the company already reported is not conservative — it is out of date. Every seasonality factor is measured from the prior year's own half against its own full year, which is the proof the rule asks for rather than an assumption.

19. **Two things about the process, which matter more than the number.** The gap gate went red the instant the answer moved — the review audited −19.0% while the study sat at −13.7% — and forced the eight headings to be re-asked at the size the disagreement actually is. And **the answer moved twice tonight in the direction the review's own logic had predicted**: once on the capital path, where the review named the suspect half *before* anyone knew which way a correction would run, and once here.

**Where STC ends: SAR 47.11 → 37.84, −19.7%, across eleven levers and ten rules, off five ratchets.** Nothing published; the study remains held. Every correction is in the rebuild ledger with the answer either side of it, so the route can be walked rather than inferred from the net — which is the whole point, because the net of −19.7% contains a +8.4%, a −13.8%, a −15.4% and a +6.5% pulling against each other.


## 05 Sep 2026, after the slot — the cost side answered, and a claim nobody had deducted

20. **The open item was the cost side and the answer is that the blend hides almost nothing — measured, not assumed.** Note 35 breaks cost of revenues into seven lines by nature, and the model holds each *segment's* margin flat, so every line already sits on the revenue of the segment it belongs to. Four lines have a base the filings actually name. Put each on it and the final forecast year moves by a net **+41.9 SR million** of cost — **-0.047 points of margin**, **-0.301%** of the central.

    | line | held at a share of revenue | on the base the filings name | difference |
    |---|---:|---:|---:|
    | Commercial service provisioning fees | 5254.3 | 5149.3 | -105.0 |
    | License fees | 534.4 | 536.1 | +1.7 |
    | Repairs and maintenance | 2243.5 | 2323.7 | +80.2 |
    | Amortisation and impairment of contract costs | 216.3 | 281.4 | +65.1 |
    | **net** | | | **+41.9** |

    **The offsets run both ways and that is the finding.** The levy and the licence fee fall against a group growing faster than the Saudi segment they are charged on; maintenance and subscriber-acquisition costs rise against it; the two nearly cancel. Three tenths of one per cent does not justify four new escalators, two of which would rest on two observations apiece — **so the model is not rewired and the measurement is what is committed.** Worth establishing rather than assuming: the same test on another name in this book found a mix effect worth seventeen per cent.

21. **Four lines are deliberately not priced, because inventing a driver to complete a table is worse than the gap it closes.** Network access (13.0% of revenue, no disclosed unit rate); employees (7.1%, **no headcount anywhere in the filings** — searched, absent); Others (3.5%, a residual of three unrelated things); and frequency spectrum (0.3%, lumpy, with the **first Saudi licence expiry in 2029 — inside the explicit window** — and no renewal cost disclosed). The spectrum line is named as a gap rather than modelled.

22. **Two things the sub-notes settle that nobody had.** The 724 million reversal is placed by **arithmetic, not inference**: the footnote puts it inside FY2023 government charges without saying which sub-line, and three of the four sub-lines are each *smaller than the reversal*, so it cannot sit in any of them. It belongs to the provisioning levy, and placing it there tightens that levy's ratio against the Saudi segment from a two-point step to **8.964% / 9.473% / 9.015%**. And the device line is **not** device cost of sales — it costs more than the devices sell for in every filed year — so the split was solved across every available period pair and ranges from **-1.08 to 5.86**, two of three pairs economically impossible. Demonstrated unidentified rather than asserted, and left alone.

23. **Then the real finding, and it is the third defect of one shape.** Note 14.1 of the same reviewed interim carries **financial liabilities related to frequency spectrum licences of SR 3443.044 million** — consideration owed to the regulator for licences already capitalised as intangible assets — sitting inside *financial liabilities and others*, nowhere near the borrowings lines a net-debt build reads. **The bridge had never deducted it.** Central **37.8396 → 37.1640, -1.79%**; the gap widens **−13.7% → -15.3%**.

    **It is not double-counted against capital expenditure, and that had to be established rather than assumed.** Total additions to property, equipment, intangibles and goodwill were **13,815.240** in FY2025 against the **11,795** of capital expenditure the model forecasts on, and note 12(2) states additions include **non-cash additions of 2,122 million** (FY2024: 883). The model runs on *cash* capital expenditure; the licences bought against this liability never entered it. Charging the asset as capex **and** the liability as debt would be the double count — charging neither, which is what the bridge did, simply omits the claim.

24. **The shape is worth naming because it is now three for three.** The associates line, the reviewed half, and this: each disclosed, each in a document the build had already fetched, each missed because the build read *the line it expected* rather than *the note the line points at*. Two raised the answer and one lowered it, so it is a reading habit rather than a lean — and a habit is cheaper to fix than a bias.

25. **A gate caught me inside the hour.** `check_artefact_currency` went red on `cost_decomposition.json`, built against 37.8396 while the study had moved to 37.1640 — exactly the stale-artefact defect that rule was written for, on an artefact created that same afternoon. And the rebuild ledger's anchor lever was still reading the study's *current* numbers file, the collapse registered as L-342 that morning; pinned to the commit that landed it before the new lever went in, or the spectrum move would have been silently attributed to the reviewed-half anchor.

**Where STC now ends: SAR 47.11 → 37.1640, -21.11%, across twelve levers and ten rules.** Gap against the latest known price **-15.27%**. Nothing published; the study remains held on both [R-GAP-02] conditions.


## 05 Sep 2026, later — a surface no gate had ever opened

26. **The retired skill verdict was still in seven delivered artefacts, and five of them were workbooks.** The rule retires it from *"no page, figure, document or deck"*. Its gate grew one surface at a time — pages, then the figures' caption template, then the Word documents on 3 September — and nobody ever pointed it at the **workbook**, which is delivered in the same folder, on the same day, to the same reader. Eight hits across ADNOCLS, ARCC, MODON, RIYADHCABLE and SCEM, three of them the literal word in capitals, and **two of the five were built this week** — those studies were swept, passed, and shipped it in the file beside the document.

27. **Nothing was ratcheted and the exemplar's debt did not grow.** All five were one- or two-line rows in their own builders, so all five were fixed and rebuilt. That matters most for ADNOCLS: the rule adopted 4 September says a new standard is either **met** by the exemplar or **consciously added** in the commit that adopts it, because a debt on the document every future study is copied from is a debt every future study inherits without anybody deciding to take it on. It is met.

28. **Two delivered documents too, and one was a rewrite rather than a deletion.** SWDY carried two comparisons against a random-walk benchmark; both deleted, coverage and the width ratio kept. ADNOCDRILL was different: its whole reading of section 3 was an *inference from* the retired score — the map "scored WORSE", the bands were **therefore** "too wide", narrowing them "would have turned the score positive". Retiring the comparison takes that reading with it, so deleting the sentence would have left a claim standing on evidence that no longer exists. The replacement says **less**: fifteen windows cannot separate an honest cone from a broken one, so no flag is raised in either direction, and the width ratio at 1.10x a naive band does not on its own carry the claim the score was carrying.

29. **The negative control would have broken, in the way that looks like working.** The sandbox stages only what the gate reads, and it staged no workbook — so the new arm would have refused an empty population on *every* case, the clean ones included, going red for the **wrong** reason, which reads exactly like going red for the right one. One workbook is now staged; three injected defects are caught in it, two legitimate constructions allowed through, every injection verified to have **landed in the saved file** before its result is believed, and a further case removes every workbook and requires the gate to refuse *and to name the population as the reason*.

30. **Two lessons registered, both ALL scope.** [L-344] a build reads the line it expects and not the note the line points at — three defects of that shape in one study, and the same shape already on AMOC and SCEM, so three companies rather than one quirk; what makes it invisible is that the figure that *was* read is correct, so every gate is clean and the defect is an **absence**, which has no cell to check. [L-345] a rule that enumerates its surfaces is only checked on the surfaces somebody wired up.

---

## 6 September 2026, 02:15 UTC — THE ACCOUNT IS OUT OF USAGE CREDITS

**This is a report, not an escalation** [R-IND-01]: the work routes around it, so nothing is
blocked and nothing is owed. It is here because it contradicts a plan the principal set —
"we have tokens that will expire tomorrow at 6AM and we have to finish them as soon as
possible" — and only they can act on it.

**What happened, in order.** Ten workflows were launched (~300 agents). They hit the
*session* limit, which reset at 02:00 UTC as advertised. On relaunch every agent returned
**"You're out of usage credits"**, which is the *account balance* and a different limit. Six
of ten workflows had already reported; the rest died within seconds of relaunch.

**What survived and is committed:**

- ARCC's walk-forward now carries its [R-FCAL-01 AMENDED] valuation-input block — eight
  origins, seven items, every figure OCR'd off the rendered pixels because those filings
  carry no text layer, every one footed. Eight cells recorded MISSING, all of them the share
  count, refused rather than carried back.
- AMR's terminal evidence note, which **stops** rather than conforming: its own note
  depreciates to an estimated residual value, closing the measured-age route, and a life
  this desk chose is not a disclosed life.
- Four studies read page by page as rendered images — 234 pages, ADNOCDIST, ADNOCDRILL,
  ADNOCLS, AIRARABIA — 83 candidate findings raised and **all 83 refuted on verification**.
- Two answer audits, ADNOCDIST and ADNOCDRILL, whose substance is below.

**The one finding verified by hand, because its verifiers could not run:** ADNOCDIST applies
its 17% FY2026 commercial-margin step to an anchor that already contains it, and the study's
own input register says so in as many words. Written up as finding 7 of
`engine/adnocdist_study/AUDIT_05-09-2026.md`.

**No decision is needed tonight.** Hand work continues without credits. If they are topped
up, every workflow resumes from `resumeFromRunId` with completed agents replaying from cache
— nothing already done is repeated or paid for twice.

## 06-09-2026, 19:25 UTC — the FY2014 parse was already done, and the origins cannot move

**Done.** Checked what blocks ARCC's walk-forward from reaching back before FY2018.

**Measured.** `panel_export.json` already carries the complete cost stack, revenue
split and physical volumes from **FY2014** — twelve years, not eight.
`bottom_up.actual()` resolves FY2016 and FY2017 fully today. FY2014 and FY2015 fail on
one thing only: the local/export volume split, which the panel does not hold.

**Contradicts what the programme believed.** The next-list item read *"parse ARCC's
cost stack back to FY2014 — it adds two origins"*. **Both halves are wrong.** The parse
was already done, and the origins cannot be extended at all — not for want of data, but
because [R-FCAL-01] runs *every origin from the first year with five years of history*,
and the pre-registration states it plainly: FY2018 is the first year with FY2014–FY2018
behind it. Adding FY2016 and FY2017 as origins would break the standing scope rule.

**What those years are actually for** is the mid-cycle anchor, and F7 already reads
them — twelve years of gross margin from FY2014, which is what took ARCC's profit error
down 62%. Nothing further to do here.

**Next.** Make AMOC, EGCH and PHDC commit per-cell errors. The three-origin finding —
the one that overturned the programme's premise — rests on the only two runs that
expose them.

## 06-09-2026, continuous run

Made AMOC, EGCH and ARCC write `error_cells.json` — all three already built the
rows in their own scoring pass and aggregated them away. Scores unchanged; the
dump adds a file and moves no number.

Then re-ran the break cut on five names instead of three, and it changed the
answer twice over. The typed origin-year range used in the three-name note
conflated two questions; split properly into an ORIGIN cut (what the analyst
knew) and a TARGET cut (what hit the window), they disagree — ARCC's effect is
+0.392 on one and -2.215 on the other, because its own era labels correctly call
the FY2020/21 origins pre-devaluation while their windows ran straight through it.

On the target cut, **eleven of eleven family-level effects carry the same sign
across four names**, 0.45 to 3.2 log points, and the residual outside the
devaluation years is small on three of them (-0.17, -0.01, -0.03). The founding
premise of a uniform -45% house lean does not survive that split. It also
compounds monotonically to h=3 on all five names, which is a rate error rather
than a level shock.

`engine/method_reassessment/BREAK_EFFECT_FIVE_NAMES_06-09-2026.md`;
read live with `python3 engine/valuation_calibration/break_effect.py`.

### Later the same day — the break effect is not one thing

Split the devaluation-year error macro-versus-company on identical cells
(`engine/valuation_calibration/macro_share.py`). Three names, three answers:
**AMOC 51% macro, EGCH 34%, ARCC -1%.** A single house-wide correction is ruled
out by those three alone.

Sharper: **on two of the three names, handing the model more macro truth makes
it worse.** AMOC's perfect-CPI-only setting is worse than knowing nothing
(-1.136 against -0.707); ARCC's best setting is perfect CPI (-0.168) and adding
the realised currency takes it back to -0.493. A model whose error grows when it
is told the truth is mis-specified, which is a specification error and not a
calibration one.

Found AMOC's, in its own code: `brent_ratio()` returns 1.0 outside foresight, so
crude-in-EGP is frozen while every domestic cost compounds Egyptian inflation —
[L-048] exactly. Putting both on one clock takes the bias from -0.774 to -0.258.
The adopted fix is the house PPP identity (F8, -0.443), **not** the better-scoring
diagnostic, because adopting a rule for its score is the selection mistake the
promotion rule forbids. What is left after F8 is the honest answer: PPP
under-predicts a step devaluation by 2.3-2.5x at three years, and that residual
is the width years three to five should carry rather than a rule waiting to be
found.

Two bugs closed on the way: my own dump called ARCC's `cpi_only` without
`foresight` and silently got the as-known answer back; `_paths()` now refuses
that combination instead of returning it.

`MACRO_SHARE_06-09-2026.md`, `BREAK_EFFECT_FIVE_NAMES_06-09-2026.md`.

### And the ranges themselves do not hold

[R-FCAL-01]'s years-three-to-five ranges clause is honoured by all five runs —
checked, clean, nothing to fix there. So the next question was whether those
ranges hold, which nobody had asked.

**They do not.** Walk-forward (band built from the origins strictly before each
one): 259 cells, **55.6% coverage against an expected 63.5%, p=0.010**, and it
degrades monotonically with the horizon — -1.9pp at one year to **-31.7pp at
five, where the band catches 29% of outcomes and sixteen of its seventeen misses
are on the low side.** Years three to five are exactly where the rule mandates
ranges *because* points fail there.

Not the break effect in a new costume: split by regime the bands under-cover in
both, and MORE outside the devaluation years (-11.4pp against -6.6pp). The break
effect is a lean on top of a band that is too narrow in both directions.

**The first draft of this instrument measured nothing and that is the more useful
half.** Leave-one-origin-out on a min-max band is an arithmetic identity —
exactly two of every k+1 hold-outs fail whatever the data, so coverage is
(k-1)/(k+1) by construction. It was caught only because the benchmark was
computed rather than typed: observed and expected agreed to the last decimal on
five names and five horizons, five rows too clean to be real.

No widening. A factor chosen to make the table pass is the free parameter the
promotion rule forbids. `BAND_HOLDOUT_06-09-2026.md`.

### Correction: AMOC is a nominal freeze, not two clocks

Built a clock test (`engine/valuation_calibration/clock_test.py`) so the
transmission is measured rather than read module by module, and it corrected my
own diagnosis from a few hours earlier. At three years AMOC's projected revenue
escalates x1.00 and its cost of sales x1.02 against the model's own cumulative
inflation of x1.24 — **both sides frozen**, clocks 0.81 and 0.83. It is not
[L-048]; the two sides differ by two points and the whole model differs from its
own economy by twenty-four. Crude is both AMOC's product and most of its cost, so
freezing crude in pounds freezes nearly the whole income statement. EGCH (0.94 /
1.00) and ARCC (1.03 / 0.92) are healthy, which is what makes AMOC's figure
readable at all.

The instrument's own first draft was wrong the same way twice over: it measured
the ELASTICITY to a one-point inflation bump, which is a local slope and cannot
see a level held still, and it reported AMOC as "one clock". Re-pointed at the
escalation actually applied over the horizon, never widened.

Extended the clock test to four of the five runs (PHDC prints its reason rather
than being left off the list). **No run has a two-clock gap wider than 0.11**, so
[L-048] is not present anywhere in this book; AMOC alone sits near 0.82 on BOTH
clocks where EGCH, ARCC and TMGH are at or above 0.92. The defect is a level, not
a mismatch. The gap is the robust column — volume cancels out of it — and the
levels are not, which is why TMGH reads 1.9 on both sides: it forecasts a growing
book, a forecast rather than a defect.

### The clock test, and a reading I had to withdraw

Wrote a general adapter so the test reads all five runs (PHDC's actual-at-origin
is recoverable from the cell whose target IS that origin, so nothing is estimated).

PHDC's raw gap came out at -0.44, four times the next widest, and three facts
lined up behind it: PHDC is the one name of five that OVER-forecasts its own
history, its central sits 24% above the market, and its revenue escalates far
ahead of its cost. I wrote it up as [L-048] in mirror image.

**It does not survive reading the projector.** PHDC escalates `asp` and `cogs`
by the SAME inflation term in the same loop — there is no escalation asymmetry.
The raw gap measures that revenue is a percentage release of a BACKLOG while cost
follows DELIVERIES: two different volume drivers, so volume does not cancel and
the difference is a developer's recognition mechanism, not a defect. The gap now
prints `n/a` for both developers rather than a number, and the reason is in the
module.

The number was real and the reading of it was wrong — [R-TERM-01 CLAUSE TWO
CORRECTED] in another costume: a ratio between two quantities defined differently
is not evidence about either.

**What survives is AMOC**: both clocks at 0.82, gap +0.02, frozen in nominal
terms inside an economy the model puts at 7.4% a year. And no run in the book has
an [L-048] gap — the widest readable one is ARCC at -0.11.

Two earlier drafts were wrong too: a ratio of averages, and a filter requiring a
positive base-year figure that dropped every cost line TMGH commits and reported
it untestable. `CLOCK_TEST_06-09-2026.md`.

### PHDC located: one driver on the wrong clock

Followed the open question and it answered cleanly. PHDC over-forecasts by +0.468
on 160 cells and **the bias does not compound** (+0.459 / +0.475 / +0.479 /
+0.484 / +0.439 at h=1..5) — a level error, not a rate error, which is the
opposite signature to every under-forecasting name.

The level is the recognition rate. `delta = revenue / (backlog + new sales)` is a
trailing three-year mean held flat, which is the right mechanical choice a priori
— but this company's realised delta fell monotonically from 0.3393 to 0.1104 as
its backlog compounded 14.8x against revenue's 4.8x. **Every origin used a delta
above what happened, eight of eight** (0.3336 against a realised 0.1436 three
years out; 0.3244 against 0.1596).

It is [R-FCAL-01]'s trap (ii) verbatim: revenue on a backlog-release clock, cost
on a delivery clock. Revenue's own bias is only +0.107 while gross profit's is
+0.540 — operating leverage on a thin residual, exactly as the rule predicts.

Both framings measured, **neither adopted**: revenue onto the delivery clock
takes the pooled bias to +0.171 and gross profit to +0.028 at a cost in MAE; cost
onto the revenue clock takes it to +0.383 and improves MAE. Choosing is a ruling
on a delivered study, not a measurement.

Neither fixes the residual, which sits BELOW gross profit — profit before tax is
still +0.837 with gross profit at +0.028. That second defect is larger than the
one located here and is not diagnosed.

The measurement's own first draft negated the cost line, dropped 121 of 160 cells
through the log score, and read as "no change". `build()` now raises when a
mutation fails to land. `PHDC_RECOGNITION_CLOCK_06-09-2026.md`.

### And in levels the ranking flips — plus trap (i), which resists a naive fix

Decomposed PHDC's profit error in LEVELS on 26 cells where every line is present
both sides, so the identity closes: **cost of sales under-forecast is 62% of the
whole +3,612 profit over-forecast**, revenue over-forecast 26%, finance cost 21%.
The log table put revenue at +0.107 against cost at -0.235, which reads as
revenue being the larger problem. It is not — log weights small cells, levels
weight large ones, and a fair value inherits the level ranking. That also bounds
the clock fix: it removes the 947 of revenue over-forecast and leaves the 2,242
of cost under-forecast standing.

Then the finance cost, which is **[R-FCAL-01]'s trap (i) verbatim**:
`kd = finance_cost / bs.total_current_liabs` on a developer whose current
liabilities are mostly customer advances, which bear no interest. Measured on the
run's own panel, interest-bearing borrowings are 0.9% to 35.8% of that total and
the share moves by year. The panel already carries `bs.loans_current`,
`bs.loans_lt`, `bs.overdraft` and `bs.banks_credit` — the right denominator
needed no new data and was simply not used.

**Correcting the denominator alone makes it WORSE** (-1.093 to -1.422). The rate
rises but it is applied to a base FROZEN at the origin that swings thirty-fold
across origins. Two defects in one line, and fixing one without the other is
worse than leaving both; a proper fix needs a projected debt path this model does
not build. Stop-and-inform rather than invent one — which is the digest's own
warning about this trap, arriving as predicted.

### The largest PHDC line: cost pinned to CPI while revenue is not

`cogs = cpu0 x infl x deliveries` with `infl` the consumer-price path. On the
run's own panel PHDC's realised unit cost compounded **5.40x over 2015-2023 —
23.5% a year — against CPI's 3.10x at 15.2%**, so the model under-forecasts unit
cost by 8.3 percentage points a year and that compounds to the 25% level gap.

**I first wrote this up as construction cost outrunning a consumer basket, and
putting the revenue side beside it says otherwise.** Revenue per delivered unit
grew 22.7% a year against cost's 23.5% — a cost drift of +0.61% a year, gross
margin 0.350 to 0.318 over eight years. Both sides ran about 7% a year above
consumer prices, together. So it is the same two-clock defect as everywhere else
in this run: cost pinned to CPI while revenue arrives through the backlog release
and happens to track better. The fix needs no external index and no new source —
the cost escalator has to sit on the same path as the revenue it is matched
against.

It also evidences a decision the delivered study already took: PHDC's
`bottom_up_model.py` sets `COST_DRIFT = 0.0`, records the measured drift from a
single quarter pair beside it, and declines to carry one. Eight years of the
company's own record put that drift at +0.61% a year. **The study was right, on
one quarter's evidence; this record is what supports it.**

### How far the two PHDC defects travel

**Trap (i) is PHDC's alone.** TMGH and EGCH both build their rate on
interest-bearing debt correctly (TMGH's module says so in its own docstring);
ARCC holds finance costs flat and already carries that in its NOT_FIXED list with
its reason.

**The CPI-pinned cost escalator is established on one name only.** EGCH's urea
tonnage series runs three years, giving 3.3% a year real over two — directionally
the same and far too short to call. ARCC, AMOC and TMGH commit no unit-cost
series that can answer it, so they are recorded as unmeasurable rather than clean.
One name is not a pattern.

### The night's generalisable result: the spread moves with the price

Measured the realised escalation of revenue per unit against cost per unit on
every run committing a volume series:

| name | class | window | revenue | cost | cost drift |
|---|---|---|---:|---:|---:|
| TMGH | developer | **14 years** | +16.0%/yr | +15.5%/yr | **-0.37%/yr** |
| PHDC | developer | 8 years | +22.7%/yr | +23.5%/yr | **+0.61%/yr** |
| AMOC | refiner | 4 years | +44.6%/yr | +46.0%/yr | **+0.97%/yr** |
| EGCH | fertiliser | 2 years | +21.9%/yr | +30.1%/yr | +6.76%/yr (too short) |

**Twenty-six name-years across three windows and two classes: the drift is inside
1% a year and NOT one-signed** (-0.37, +0.61, +0.97), which is what a genuinely
flat spread looks like rather than a slow trend. Price and cost move
together at whatever rate the economy is running, and the spread stays put.

That reframes everything found tonight. **AMOC needed 44.6% a year and the model
used zero** — and the house PPP identity supplies about 11%, which is why F8 only
reaches -0.443 and no further: no currency rule this house has is within a factor
of four of what happened, and that residual is the width the far years should
carry rather than a rule waiting to be found. PHDC pinned cost to CPI at 15.2%
while cost ran at 23.5%. ARCC's seven fixes were all of this family and its
clocks are the healthiest in the book.

**The escalation RATE is worth two orders of magnitude more than the spread.**
AMOC's whole 0.52 log points comes from 0% against 44.6%; its spread moved 0.97%
a year over the same window.

So I asked which knowable rule gets closest — freeze, last-published CPI, PPP, or
the company's own trailing three-year escalation. **Freezing is the worst on
every name that can be measured**, and it is what AMOC's model does: trail3 is 42%
better on the paired cells, cpi 27%, ppp 23%. No rule is selected — choosing one
because it scores best here is the selection mistake the promotion rule forbids —
but freezing is ruled out, which is a firm and useful thing to have established.

Two caveats printed with it: TMGH is 30 of the 43 cells and is measured on totals,
so its escalation carries volume growth and flatters a trailing rule; and this
does NOT reverse the earlier finding that trailing trend is the weakest of the
three benchmarks, because that pooled every driver and this scores only the
escalation rate of one line.

`SPREAD_DRIFT_06-09-2026.md`, `engine/valuation_calibration/escalation_rules.py`.

### The three findings are registered, so they bind

`L-352` the spread is flat and the rate is everything · `L-353` freezing a driver
is the worst available rule · `L-354` a min-max range of a handful of errors is
not the interval it looks like. All three at scope ALL, all PROVISIONAL under
[R-LESSON-01], each with its measured evidence and its falsifier, drafted in
`engine/valuation_calibration/lessons_draft.json` because they rest on three runs
and belong to no single ticker. Register now holds 275. Gate green.

L-353 deliberately says only what is RULED OUT. Nothing is selected — choosing an
escalator because it scored best on this panel is the selection mistake the
promotion rule forbids, and the lesson says so in its own scope note.

### L-353 is made arithmetic: `scripts/check_frozen_escalator.py`

A lesson that binds nothing is advice, so L-353 got a gate the same night it was
registered. **What it tests is CONNECTIVITY, not magnitude**, and that
distinction is the whole design: every inflation rate a run carries is doubled at
its source, and a line whose projection comes back IDENTICAL is wired to none of
them. Zero is not a threshold, so no free parameter enters.

The instrument is the one the clock test discarded. An elasticity draft was
abandoned there because a local slope cannot see a level held still — and that is
exactly the right instrument for asking whether a line is wired at all. Wrong for
one question, right for the other.

A frozen line is not automatically a defect — a contractual price, a
foreign-currency line wired to the currency path, a pure volume driver — so a run
declares its frozen lines with a reason from a **closed list**. AMOC is on the
ratchet rather than declaring, and the reason is written into the ratchet file:
the reason that would fit is "wired to the currency path instead", and it would
be **false**, because that model wires the line to nothing at all. Declaring it
would be the rename-to-satisfy-a-checker offence.

**Two drafts of the gate were wrong and the second was caught by a clean case.**
The first doubled a named function and flagged EGCH's revenue as frozen — EGCH's
revenue moves through a currency path derived from the CPI differential read
straight off its own table, so the gate was firing on work that is right.
Re-pointed at the source per [R-COC-01], never widened. The second could not read
ARCC's table shape at all and reported it unprobeable, which the gate correctly
treats as RED.

Negative-controlled on **11 conditions, 7 red and 4 clean**, every mutation
asserting it landed, the case count asserted against a declared constant. Two
clean cases exist because a draft failed them: EGCH wired through the currency,
and a run wired only to a cpi INDEX — where scaling every year by the same
constant would leave every ratio unchanged and call a wired line frozen, so the
bump rises with the year.

### L-354 gets its instrument too: `engine/range_disclosure.py`

The sentence a far-year range owes its reader, written once rather than
hand-maintained in five studies with five different holes — the shared-instrument
lesson this repository has now learned three times.

**It quotes two numbers and quoting only the first would have been the flattering
half.** The arithmetic one — the span of k readings is expected to contain the
next about (k-1)/(k+1) of the time, computed from the study's own count and never
typed. And the MEASURED one, read live from the band-holdout record: across the
tested book those ranges contained the outcome 56 times in 100 against an
expected 63, and fewer further out. A sentence quoting only the arithmetic figure
would overstate the range, which is the cautious-sounding claim that never gets
audited [R-CAL-02].

A study whose record cannot be read gets the sentence WITHOUT a measured figure
and a note saying so — never a typed one. Below four readings it says the range
cannot carry a probability at all rather than quoting one derived from two
observations. Checked clean of internal vocabulary.

It widens nothing. A widening factor chosen to make the coverage table pass is
the free parameter the promotion rule forbids; what was missing was the
disclosure, and that is what this supplies.

## 06-09-2026, 20:15 firing

### The frozen-escalator gate now covers all five runs, not three

It shipped covering AMOC, EGCH and ARCC — the three whose projectors expose a
module-level `cells()`. TMGH and PHDC were absent, which is the population
problem [R-ENF-04] names: a gate over three of five runs while five exist reports
clean about a book it has not read.

Both are now driven through **adapters, never re-implementations** — TMGH's own
projector run with the macro paths it is handed, PHDC's own projector run with
its panel's own inflation rate doubled. A re-implementation would grade something
other than what the run computes.

Result unchanged in substance: **AMOC is still the only frozen line in the book**,
10 lines probed across 5 runs. The negative control grows to **13 cases, 9 red
and 4 clean**, with two new red cases that matter specifically — a frozen line on
each of the two ADAPTER-driven runs, because otherwise the adapters would be a
hole rather than a coverage extension, and nothing would have said so.

### The score does not score the lines a valuation depends on

Carrying the diagnosis to EGCH found something about the METHOD rather than about
EGCH. Every driver bias this house publishes is a log error, and a log error needs
both sides positive — so on a profit line every cell where a loss appears is
dropped, silently, from a mean everyone reads as that driver's bias.

**Thirteen of twenty-eight drivers lose cells; where it happens the two samples
disagree by up to 5.3 times.** EGCH's profit before tax reads -0.298 on the 23
cells the score takes and **-1.589 on all 48**. Its net profit reads -0.382
against -1.496.

**EGCH's foreign-exchange line has 50 cells and the score takes NONE.** It is
declared, it drops out of the scores file because no cell is scoreable, and it
appears in no table. Its bias on all fifty cells is -5.743, the worst driver in
the run, sign right in 15 of 50. In levels it is 43% of that run's profit gap. The
construction counts a translation loss on dollar BORROWINGS and nothing else — a
dollar exporter also holds dollar receivables, so the model projects a loss where
the company reported a gain.

**The omission is not one-signed and the instrument's own first draft said it
was.** Five of the thirteen show a larger bias on the full sample; eight show a
smaller one. That is the worse outcome: a known lean can be corrected for, an
unknown-direction discrepancy of up to five times cannot.

What this does NOT overturn: the break effect, the spread result and the
escalation ranking all rest on revenue and cost lines, which are always positive
and lose nothing. What it does say is that the bottom-line figures were never as
solid as the top-line ones, **and nothing distinguished them.**
`SCORING_BLINDSPOT_06-09-2026.md`.

### The PR went red on a missing tool, and the workflow's own comment predicted it

`check_workbook_values` reported ELEC and STC as **NEW** failures — which reads
exactly like two delivered workbooks disagreeing with their studies. Both are
`FileNotFoundError: 'soffice'` and `'libreoffice'`: those two recalculators
convert their workbook through LibreOffice before reading it, and neither binary
is on the runner.

**Both recalculate CLEAN locally**, and that is the whole point: `run_ci_gates.py`
reported 104 green on a container that happens to carry LibreOffice, against a CI
that did not. The workflow's own install block already carries that lesson in
prose — "a local runner inherits the developer's environment and CI does not",
written after poppler-utils and matplotlib did the same thing. **This is the third
occurrence.**

Fixed the environment, not the gate: `libreoffice-calc` added to the install
block, which is what the conversion needs and provides both entry points those
two scripts invoke under different names.

### The gate widened to the finance line, and caught three more

TMGH's income statement turns out to be near-unbiased — total revenue -0.090,
gross profit -0.079, net profit +0.188 — and its errors sit somewhere else
entirely: **finance cost -1.224 (its worst driver), new sales -0.877**, then the
capital base (ppe -0.643, development properties -0.528).

So I probed the finance line on all five runs. **Three of five wire their finance
charge to no inflation path at all** — ARCC, TMGH and PHDC. It is not a
fixed-rate book on any of them: TMGH's own filed finance cost went **29.6x on
debt that grew 2.3x**, so the rate rose about thirteenfold while the Egyptian
policy rate went from roughly 10% to 27%. PHDC's is 21% of its profit gap in
levels; ARCC already carries "finance costs need average rather than year-end
debt" in its own not-fixed list.

All three go on the ratchet with their reasons rather than being corrected — a
proper fix needs a projected debt path AND a rate path that none of these models
builds, which is a stop-and-inform.

**The ratchet is now keyed TICKER:LINE, not by ticker.** Keyed by ticker, AMOC
would have been forgiven on every line it ever acquires, and widening the gate
would have silently forgiven the three new ones. A new negative-control case
re-keys it by ticker — a one-line edit anybody could make in good faith — and
asserts the gate still refuses.

**One control case caught itself.** The zero-lines-probed mutation matched each
RUNS tuple as an exact string and stopped landing the moment a line was added to
those tuples. It reported MUTATION DID NOT LAND — the control working — and it
would have reported a false green had the landing assertion not been there.
Rewritten to mutate by shape. 14 cases, 10 red and 4 clean.

### EGCH's FX line: the stated simplification is refuted by the outcome

The construction counts a translation loss on dollar BORROWINGS and nothing else,
and `usd_borrowings()` says in its own docstring that the borrowings are "treated
as dollar-denominated (stated simplification)".

Bounded it without assuming a currency split: compute the FX result with 0% and
with 100% of receivables-plus-cash treated as dollar-denominated, and ask whether
the actual falls between. **The actual sits inside in only 3 of 12 years**, and
from FY2017 on it is outside on the far side — FY2024's bounds are
[-2,837,104, -1,866,498] against a reported **+278,839**. From FY2017 borrowings
exceed receivables plus cash, so every construction of a net dollar position gives
a LOSS in a depreciating pound, and the company reported a GAIN.

**So the sign is wrong, not the weighting.** The most likely reading is the one
the module itself flags: those bank borrowings are not dollar-denominated at all —
which is ordinary for an Egyptian producer borrowing from Egyptian banks — and the
entire line is a translation loss on debt carrying no translation exposure.
Confirming it needs the filings' currency note; that is a stop-and-inform, not a
correction to make tonight.

**A finding I withdrew on the way, before it went anywhere.** I first read the
receivables line as carrying no unit of its own, wrote it up as a gap in the
[R-FCAL-01 AMENDED] block schema, and put a reporting clause into
`bridge_inputs.py` that flagged all five runs. Checking a clean case refuted it:
the `lines` sub-dictionaries sit on the record's own `value` scale, consistently,
in every run — order-of-magnitude checked against each record's value. The clause
was firing on work that is right, and it is removed rather than widened. My own
first bracket had mixed the block's EGP with the panel's EGP-thousand and would
have reported the actual comfortably inside in every year; the scale was then
established on a like-for-like DEBT pair present on both sides, exactly 1000.0 on
three origins.

### The blindspot census extended, and one route had to be refused

Extended to all five runs. TMGH and PHDC have no module-level `cells()`, so they
are read from the per-cell files their scoring passes now write — and reading
them naively returned **100% taken on every driver**, which is a false clean of
exactly the shape the census exists to expose: those writers emit only the cells
their score TOOK, so the dropped count is unrecoverable from them.

PHDC is now REPORTED UNMEASURABLE rather than clean. TMGH's 100% survives and is
genuine — its own scorer handles signs before scoring, and its rows carry a
relative error and a sign case beside the log one — but the module records that a
100% from that route is the weaker statement "no cell was dropped among the cells
this file records".

The headline is unchanged: **13 drivers lose cells, up to 5.3x disagreement, and
EGCH's FX line is scored on none of its 50.**

### TMGH's new sales: a rule meeting a company that changed, not a bad rule

The driver is `new_sales = urban population x sales per urban head at the origin
x inflation` — constant REAL intensity, growing only with population and prices.
That is the no-judgement mechanical default [R-FCAL-01] requires at a historical
origin, and it is defensible.

Measured on TMGH's own record, real sales intensity was flat at 0.0001 from 2011
to 2016, stepped to 0.0003 by 2018, and then **rose 3.15x in 2023 and 2.70x in
2024** to 0.0023 — a **23-fold rise** in real per-capita sales over the window,
the bulk of it in two years.

The error splits on exactly that break:

| targets | n | bias |
|---|---:|---:|
| 2022 and earlier | 18 | -0.215 |
| 2023 onward | 15 | **-1.671** |

**Nearly eight times worse, and the split is the company's expansion rather than
the rule's specification.** Nothing knowable at a 2020 origin forecasts a 2023
land bank. Under [R-FCAL-01] a correction resets after a structural break and a
bias that changes across eras is reported rather than corrected for — so this is
NOT a driver to fix, and attempting one would be fitting the last two years.

**It is the clearest case in the book for ranges rather than points**, which is
what the rule already mandates for years three to five and what L-354 is about:
the honest output on this driver is a width, and the width this record implies is
large.

### TMGH's capital base is the same break — and the "stable" depreciation is not stable

Split the rest of TMGH's drivers on the 2023 boundary:

| driver | ≤2022 | ≥2023 |
|---|---:|---:|
| new sales | -0.215 | **-1.671** |
| property, plant and equipment | **-0.068** | **-1.217** |
| development properties | -0.411 | -0.606 |
| depreciation | -0.397 | -0.342 |

**Property, plant and equipment is essentially unbiased before the break and badly
under-forecast after** — the same expansion arriving in the capital base, so this
is one cause rather than two. Its rule holds capex at its trailing real level and
escalates it by inflation, which is right for a company doing what it did before
and wrong for one that started building.

**I then wrote that depreciation was the exception and the one correctable shape,
and that is withdrawn.** [R-FCAL-01] permits a correction only where the bias
holds its sign across eras; -0.397 against -0.342 looks exactly like that. It is
an artefact of where the boundary was drawn.

The underlying ratio says so plainly: realised depreciation over PPE rose 0.0378
to 0.0761 from 2017 to 2023 and then **collapsed to 0.0141 and 0.0060** as PPE
jumped from 6,465 to 75,812 in 2024. **That driver's own break is a year later
than the one I borrowed.** Moving the boundary to match it:

| driver | cut at 2023 | cut at 2024 | cut at 2025 |
|---|---|---|---|
| depreciation | -0.397 / -0.342 | -0.393 / -0.322 | **-0.516 / +0.364** |
| PPE | -0.068 / -1.217 | +0.007 / -1.943 | -0.434 / -1.686 |
| new sales | -0.215 / -1.671 | -0.458 / -1.840 | -0.783 / -1.401 |

**Depreciation FLIPS SIGN** at its own boundary. PPE and new sales are robust to
the cut point; depreciation is not, and a bias that changes sign between eras is
not a bias — report the instability, never correct for it.

**So TMGH has no correctable driver at all**, which is the opposite of what I
wrote an hour ago. The general point is worth more than the name: **an era
boundary chosen for one driver does not test another driver's stability.** Every
stability claim in this book was made at a boundary chosen for the market, and
this is the first time one was tested against the driver's own break.

### Run over the book: 42 of 66 testable driver biases flip sign

Built `engine/valuation_calibration/boundary_sensitivity.py` — score every driver
at every cut point the data admits, and report whether the sign survives.

**42 drivers flip sign at some cut; 24 survive every cut; 22 more have too few
cells to cut at all.** Under [R-FCAL-01] not one of the 42 is a bias. ARCC's
gross profit runs +1.578 / -0.909 at a 2022 cut and -0.084 / -1.225 at a 2025
one; its interest income +1.116 / -2.512 then -1.191 / -3.443.

**The sign clause has been tested at one point per market and passes far less
often when tested properly.** Any correction adopted on a boundary-sensitive bias
is fitted to where a line was drawn.

The break effect itself survives this: TMGH's new sales and PPE are robust at
every cut, and the target-side cut used earlier is a calendar fact rather than a
chosen line. `BOUNDARY_SENSITIVITY_06-09-2026.md`.

### And the one adopted correction in the book survives the test

Checked the question the boundary result raises: does any ADOPTED correction sit
on a driver whose sign flips? **No.**

Across the five runs there are twelve correction candidates, all in ARCC, and
exactly one is ADOPTED — `mfg_dep`, which survives every cut (range -0.185 to
-0.021). Seven of the eleven WATCH FLAGS sit on drivers that flip, and every one
of them was already declined by the procedure's own two clauses.

So the corrections machinery tested at one boundary and still adopted the one
correction that also passes the full test. **That is the procedure holding, and
there is now evidence for it rather than luck.** No live defect; the boundary
result binds on what is adopted next, not on anything already in the book.

## 06-09-2026, 22:15 firing

### The currency note was in the repository, and it refutes the simplification

Last hour I recorded EGCH's FX line as diagnosed but **blocked**: "confirming it
needs the filings' currency note — stop and inform". [R-IND-01] says a question
is the last resort and the ladder is climbed rather than recalled. The filings
are in `engine/egch_walkforward/filings`. They are Arabic scans whose text layer
is a broken font map, which is why an English keyword search over `pdftotext`
returned nothing and looked like an absence.

Rendered at 200 and again at 450 dpi and read by OCR in Arabic, page 29 of the
FY2020-21 annual carries note **(4/11) Long-term loans**, and it says the facility
financing the natural-gas conversion project was contracted with a consortium of
six named **Egyptian** banks **"in the amount of [X] million US dollars AND 1.887
billion Egyptian pounds"**, with debit interest accruing **"in dollars and in
pounds"** and the second instalment repaid **"in dollars and in pounds"**.

**So the borrowings are a split-currency facility, and the model treats 100% of
total borrowings as dollar-denominated.** `usd_borrowings()` calls that a "stated
simplification" in its own docstring; the company's own note refutes it. Add the
short-term loans and the holding-company loans, both in pounds, and the dollar
share of total borrowings is a fraction rather than all of it.

That is consistent with what the outcome already said — the bracket put the
realised FX result outside every net-dollar-position construction in 9 of 12
years — and it now has a primary source rather than an inference.

**Two decimal digits of the dollar figure did not resolve** across the two passes
(one reads 117.1, the other 117.7) and are NOT recorded; the pound leg, the six
banks and the dual-currency interest and repayment language are unambiguous in
both. The per-origin dollar share needs each year's own note and is the next unit
on this line, not a number to estimate.

**The general point is the one [R-IND-01] was adopted for.** The register said the
answer could not be obtained. It was one OCR pass away, in a file this run had
already parsed cell by cell — and the search that "found nothing" had searched for
English words in a document written in Arabic.

### What the filing does and does not disclose about the split

Read the FY2020-21 annual's foreign-currency risk note (page 33) as well. It is
**qualitative only** — "the principal risks are foreign-currency risk from changes
in the exchange rate, affecting payments and receipts in foreign currency and the
revaluation of monetary asset and liability balances in foreign currencies" — with
**no currency table**.

So the position is precise, and it is three things rather than one:

1. **The 100%-dollar simplification is refuted.** The facility note gives the
   loan as [X] million US dollars AND 1.887 billion Egyptian pounds, from six
   Egyptian banks, with interest and instalments in both currencies.
2. **The currency composition of the OUTSTANDING BALANCE is not disclosed.** The
   note gives the facility as contracted, not the balance by currency at the
   date, and the risk note carries no table. That is a named absence under SIGCM
   clause 8, not a number to estimate.
3. **The best sourced anchor is therefore the facility's original split**, and any
   use of it must say that it is the drawdown composition rather than the
   period-end one.

The first OCR sweep of all ten filings died on a tesseract timeout at page 2 of
the oldest — a probe failure, which is not an absence. Re-pointed at the back 45%
of each document, where the notes sit, with a longer per-page limit and timed-out
pages counted and named rather than dropped. Still running; whatever it returns
adds to this rather than changing it.

### The sweep finished clean, and it corrects what I wrote twenty minutes ago

All ten filings read, **zero pages timed out**. Four of them state the facility in
both currencies — FY2017-18, FY2018-19, FY2019-20 and FY2020-21 all give it as
about 117 million US dollars **and** 1.887 billion Egyptian pounds — so the
100%-dollar treatment is refuted on four filings rather than one. An earlier
FY2012-13 note carries the same shape at a smaller size.

**And the FY2019-20 note goes further than FY2020-21's.** It reads "... and an
amount of [X] dollars **has been drawn** and an amount of [Y] Egyptian pounds has
been drawn, for a total of [Z] Egyptian pounds (including debit interest in
dollars and in pounds)". **That is a drawn balance by currency**, which is exactly
what I recorded as not disclosed after reading only FY2020-21. The disclosure
varies by year and I generalised from one.

**What remains is a READING limit, not a disclosure limit, and the distinction
matters.** The drawn figures are on the page and did not resolve through OCR at
200, 450 or 500 dpi, nor from a magnified crop — Arabic-Indic digit strings in a
scanned table. A person opening that page can read them; the extraction cannot.
That is recoverable, where an absent disclosure would not be, so it is recorded as
what it is rather than as a gap in the filings.

Twice tonight a "cannot be obtained" turned out to be wrong on closer looking:
the currency note itself, and now the balance split. Both times the first probe
was the one that failed, and both times its failure read exactly like an absence.

### Registered as an escalation rather than asked in a message

Every remaining extraction route was run and failed on those two digit strings:
450 and 500 dpi, magnified crops at x1.6 and x3, binarisation, and tesseract page
segmentation modes 6, 7, 11 and 13 with a digit-only whitelist — four mutually
inconsistent readings, none of which foots.

So it is a genuine last resort, and under [R-IND-01] that means it becomes an
artefact rather than a sentence in a message. Registered in
`engine/escalations.json` with the five routes actually run and their outcomes,
the sweep that succeeded marked as a re-run, 22 live refs searched, what was done
meanwhile, and a default that fires on 13-09.

**The default is to change nothing.** Leave EGCH's FX driver as it is and leave
the run on the ratchet. A dollar weight invented to make the line behave is the
free parameter the promotion rule forbids, and the refutation does not need it:
four filings state the facility in both currencies, and the bound already puts
the realised result outside every net-dollar construction in 9 of 12 years, so the
sign is wrong whatever the split turns out to be.

Gate green: 7 entries, every one shaped, searched, and still unanswered or written
down.

## 06-09-2026, 23:15 firing

### The PR went red, and the gate was right: this branch was asking for data it already had

`check_escalations.py` failed CI on `EGX-ohlc-refresh-arcc-amoc-egch` — **"STILL
OPEN AND ALREADY ANSWERED — its own resolves_when marker is present on
origin/claude/funnel-wording."** That is [R-IND-01]'s clause that catches a re-ask
mechanically rather than by anyone remembering, and it is the first time it has
fired on a live entry.

**It went green locally and red in CI, and the reason is the lesson the rule was
adopted on.** My local clone's remote refs were stale; CI checks out fresh and
sees every ref. THE REPOSITORY IS NOT ONE CHECKOUT.

It also means this branch's prices were **a month stale** — 6 August against a
supplied 6 September — which matters, because [R-GAP-01] audits against the
LATEST KNOWN price and every gap figure computed here was against the older one.

**Closed without copying the data, and the attempt to copy it is why.** The merge
itself verifies perfectly — nine instruments, 2,957 to 4,083 rows each, EVERY
overlapping date identical, ZERO rows dropped, pure appends of 20-24 sessions,
newest 06-09-2026, and Step 0.0 re-run and passed on all nine (it removed one
placeholder row on five of them and three on two others — the gate working).

**But splicing the library turned `check_technical_read.py` from 0 failures to
49.** The standing rule is that when the library moves, the technical read moves
with it IN THE SAME PASS — levels, narrative and the chart underneath them — and
the gate says so exactly: "tech.data 2026-08-05 but the library ends 2026-09-06".
Verified by stashing: green before the splice, red after, so it is the splice and
not a pre-existing state.

**That makes the library merge a roll-forward, not a passing act**, and it is
reverted. Refreshing 49 names' technical reads and charts changes what the site
would publish next and belongs with the roll-forward that owns it — on the branch
that already holds the data — rather than bolted onto a method-reassessment
branch at midnight.

**The escalation stays closed regardless**, and that is not a workaround: the gate
resolves it from the live ref where the answer actually is, printing "resolved
(answer on origin/claude/funnel-wording)". The question was answered; it simply
was not answered here.

**What this leaves standing, and it is worth stating plainly:** this branch's
prices remain a month stale, so every gap figure computed here is against 6 August
rather than 6 September. That is a real limitation on anything [R-GAP-01] touches,
and the fix is the roll-forward, not a copy.

### Merging main in: the single-line digest nearly cost two standing rules

PR 394's CI came back green and the PR was `dirty` — main had moved **94 commits**
ahead with five conflicting files. Merged the base in rather than rebasing.

**The digest is a single line**, so git treated the whole 265KB document as ONE
conflict region. Taking either side wholesale — the obvious move, and the one I
started with — silently drops the other side's standing rules. My side uniquely
carried `[R-MACRO-01 AMENDED 06-09-2026]` and `[R-ENF-01 EXTENDED 05-Sep-2026]`;
main uniquely carried `[R-GAP-02 AMENDED]` (a publish that moves no fair value is
exempt from the method hold) and its second amendment. **I caught it by checking
whether four named rules survived, not by reading the diff** — the file is one
line and there is no diff to read.

An add/add conflict has no merge base, so the two sides were diffed against **each
other** at sentence granularity (a character-level diff on 265KB does not finish)
and merged as a union: equal takes either, delete keeps ours, insert keeps theirs,
replace keeps ours plus any of theirs it lacks. All five rule blocks verified
present by name afterwards.

**Stamped 2026-09-06c rather than either side's.** The merged text is content
neither branch had alone, and carrying main's "b" would certify a copy that has
moved — which is exactly what [R-DOC-01]'s stamp exists to prevent.

`check_protocol_sync` and `check_protocol_text` both green; the two derived HTML
pages regenerated from their builders rather than hand-merged; the escalation
register resolved as a union (main's twelve entries, including its own better
resolution of the OHLC one, plus this branch's). **105 of 105 gates green on the
merged tree.**

THE GENERAL LESSON, WHICH IS NOT ABOUT MERGING: A DOCUMENT WITH NO LINE BREAKS HAS
NO MERGE GRANULARITY. Every prose safeguard in this house assumes a reviewer can
see what changed; a single-line file defeats that completely, and the only thing
that caught it was asking whether specific named rules were still there.

## 07-09-2026 — the merge retired the price limitation, and put a second price source in the room

**The staleness limitation recorded yesterday is RETIRED.** After merging main this
branch's EGX/QA libraries run to 06-09-2026 and `check_technical_read` returns
0 failures across 93 entries — because main had done the roll-forward properly,
library and technical read moving in the same pass. Nothing here spliced anything.

**Two names are NEW breaches against the current price, inside the band when
struck:** ADNOCLS at **-18.2%** (struck at -9.0%) and AMR at **-10.2%** (struck at
-3.8%). Both already carry a GAP_REVIEW (04-09 and 05-09), so neither is owed one
from nothing — but each review was written at a gap roughly nine and six points
smaller than the one the study now carries, which is past [R-GAP-01 AMENDED]'s
five-point staleness tolerance. `check_valuation_gap` is green on both and is
right to be: it audits a study against its own STRIKE price, deliberately, and
the strike gap has not moved. **So a review can go stale purely because the market
moved and nothing anywhere goes red.** That is the two-instrument split the rule
already states rather than a hole in it — the obligation binds at each study's
next delivery, which is when the strike is re-taken.

### The repository holds a later price than the instrument that reads prices

`gap_today.py` reads only `engine/prices/SUPPLIED_*.json` and calls the answer
"the latest known price". After the merge that is no longer true for seven
studies: `engine/raw_ohlc/` — the exchange series every cone is struck on — runs
three days ahead of the 03-09 supplied file.

**The two sources genuinely disagree on a SHARED date, and not by a lag.** Five
EGX names differ by 0.6% to 1.9% in BOTH directions (ARCC +0.65%, EGCH +0.62%,
ELEC +1.44%, PHAR +1.89%, SCEM -1.48%), and **two of the supplied figures match no
session in the library at all** — EGCH's 14.41 sits between the 09/02 close of
14.36 and the 09/03 close of 14.50, SCEM's 100.50 between 99.01 and 102.00. Two
others match an EARLIER session exactly (ARCC's 77.00 is the 31 August close,
PHAR's 127.30 the 1 September close) while SWDY's and AMOC's agree with 09/03 to
the cent. **No single explanation covers all five**, so neither source is simply
the other one lagged and neither can be dismissed.

**Measured before it was claimed: no name changes side.** Recomputed on the
freshest library close, AMOC -15.8%, ARCC -13.1%, EGCH -71.6%, ELEC -84.2%,
PHAR -71.4%, SCEM +25.1%, SWDY -59.3% — every one on the same side of the 10%
trigger as the supplied-price figure. The breach set of 18 stands exactly as
reported.

**WHAT WAS CHANGED, AND WHAT DELIBERATELY WAS NOT.** `gap_today.py` now prints an
ADVISORY naming every study whose library carries a later close, with the gap
under each and whether the side changes. **It substitutes nothing.** Which series
measures [R-GAP-01]'s trigger across the whole book is a method question, not a
maintenance one, and the disagreement above is exactly why it cannot be settled in
passing — swapping the source would move every EGX gap figure on the strength of a
choice nobody has tested. What the advisory buys is that the tool stops asserting
something it did not check. Guarded [R-ENF-04] both ways: zero libraries resolving
REFUSES rather than printing "none", and the refusal is negative-controlled by
running the module against a tree with the libraries removed, asserting the
condition landed before believing the red.

**CORRECTION TO THE PARAGRAPH ABOVE, FOUND WHILE CHECKING WHAT IMPORTS THIS MODULE.**
I wrote that which series measures the trigger "is a method question, not a
maintenance one". **The house has already answered it — for the site.**
`scripts/build_prices_block.py` imports `gap_today` and then resolves the price
itself as `max(cands, key=date)` across the supplied file AND the name's own OHLC
library, recording `src` on every row; the site's PRICES block already carries
`AMOC { px: 13.54, date: "2026-09-06", src: "library" }`. So the repository holds
two instruments that answer "the latest known price" differently, one of them
importing the other, and the screener a reader sees is on the fresher side.

**Left as it stands, deliberately, and the reason is not inertia.** The supplied
file is the principal's own instrument, and where it disagrees with the library on
a shared date — which it does, five names, both directions, unexplained — silently
preferring the other one is the quiet substitution SIGCM clause 1 forbids. The two
jobs are genuinely different: the screener ranks and wants freshness; this report
audits an answer against the price it was compared with. **What was actually wrong
was that neither said so.** Now both do — the block names its `src` per row, and
this report names every name where the other source is later. The disagreement is
visible from either end instead of being resolved by whichever script you happened
to run.

One consequence recorded rather than acted on: the committed PRICES block predates
this branch's EGCH library and still carries `14.41 @ 03-09` where the builder now
resolves `14.23 @ 06-09`. **Regenerating it here was reverted** — it also relocates
the whole block within `data.js`, and a site-data churn from a method branch is the
same call made yesterday on the OHLC splice: it belongs to whoever does the
roll-forward. **Nothing is silently behind:** `scripts/check_prices_block.py`
already prints the drift by name — `EGCH: block 14.41@2026-09-03 (SUPPLIED) vs
readers 14.23@2026-09-06 (library)` — and stays green, because a price arriving by
hand is a data-supply fact and a gate nobody can clear is one everybody learns to
ignore. The disclosure was there before I looked; what was missing was only that
`gap_today` did not carry the same sentence.

THE GENERAL LESSON, WHICH IS NOT ABOUT PRICES: AN INSTRUMENT NAMED FOR A QUANTITY
IS TRUSTED FOR THAT QUANTITY, WHATEVER IT ACTUALLY READS. `gap_today` says "the
latest known price" in its first line and reads one directory; it was correct on
the day it was written and stopped being correct the moment a roll-forward landed
somewhere else in the same repository. Where a tool's name makes a claim about the
world, the thing to check is not its arithmetic but its INPUTS — and the cheapest
honest fix is usually to make it say what it did not look at, rather than to widen
what it reads.

### The digest carried TWO revision stamps and every check in the repository was green

Reading the digest's own opening characters — not a diff, not a gate — showed it
opened with its current stamp sentence **immediately followed by the superseded
one**. `check_protocol_sync` passed it, and the reason is a property of the file
rather than an oversight in the gate: **the digest is a single line**, so
`readline()` returns the whole 265KB document and a match anchored at position 0
is satisfied by the first stamp however many follow it. The check was correct and
was reading a different question from the one [R-DOC-01] asks.

**A DOCUMENT THAT STATES TWO REVISIONS STATES NONE** — the same defect as the rule
that stated two limits, arriving in the one sentence written to prevent it. The
stamp exists so a copy pasted into the principal's own project files can declare
its own age, and a copy carrying two ages declares neither; the reader it was
written for is the one person who cannot run this gate.

**The safe merge and the defect are the SAME OPERATION.** The union that kept both
opening sentences is exactly the resolution that saved `[R-MACRO-01 AMENDED
06-09-2026]` and `[R-GAP-02 AMENDED]` from being dropped yesterday. Nothing about
it was careless. The only thing separating the two outcomes is a check that counts.

Closed: `check_protocol_sync` refuses a second stamp anywhere in either document,
shape-matched rather than word-listed and safe for the reason rule identifiers and
repository paths are — `DIGEST REVISION` followed by an ISO date is not a phrase
that occurs innocently in prose written for anyone. Negative-controlled on the
merge artefact exactly as it shipped, a superseded stamp buried mid-document, the
other document's prefix and a three-stamp file, **every mutation asserting that it
landed** before the gate runs, plus five clean cases among them the full protocol's
own `rev. N` edition history and a bracketed `[R-MACRO-01 AMENDED 06-09-2026]`
note. Both documents amended in the same commit, both stamps bumped to `2026-09-06d`.

**THE GATE'S FIRST LIVE CONSEQUENCE WAS TO REFUSE THE DOCUMENT THAT ADOPTS IT.**
The amendment quoted both stamps as evidence, which is exactly what the new rule
forbids. Two ways out, and the choice matters: exempt a stamp inside quotation
marks — which invents an exemption, and [R-MACRO-01]'s own lesson is that every
exemption is a place where the gate stops looking — or take the verbatim defect
out of the prose and leave it in the negative control. **Re-pointed rather than
widened, per [R-COC-01].** The fixtures live in the control, which is where a
reproduced defect belongs; the prose describes it.

THE GENERAL LESSON, WHICH IS NOT ABOUT STAMPS: A MERGE CAN SATISFY EVERY CHECK AND
STILL PRODUCE A DOCUMENT NEITHER SIDE WROTE. Both stamps were real and both had
been correct; what was wrong was a thing that existed only after they were put
together, and no check on either side could have seen it. Where two correct inputs
are combined, ask what the combination asserts that neither input did.

### PHDC is not unmeasurable — it has nothing to drop, and the census could not tell the difference

`scoring_blindspot.py` reports PHDC as NOT MEASURED, with the reason *"this run's
per-cell file records only the cells its score TOOK, so the dropped count is
unrecoverable from it."* **That reason is false, and the verdict is a false
unmeasurable — the exact "absent answer wearing the costume of a clean one" this
protocol names.** Measured by running PHDC's own writer rather than reading its
output: `cells()` returns **403 rows, 403 with a log error, zero sign cases**, and
the writer demonstrably CAN express a drop — it sets `sign_case` and `rel_error`
and omits `e` whenever either side is non-positive. TMGH's `_cell()` does the same.
So both writers are complete, and PHDC's file records no dropped cell **because
PHDC drops none**.

The census's detection rule — *a file with no null error cannot be told apart from
a run with nothing to drop* — is right in general and is exactly what costs the
answer here. And the comment above it asserts something else that is simply wrong:
*"TMGH and PHDC expose no module-level cells()"*. **Both do**; I called PHDC's
directly. A comment asserting a property the code does not have is worse than no
comment, because it stops the next reader looking — which is the finding written
into [R-ENF-07] a few days ago, arriving in my own file.

**Not fixed in passing, and the fix is a declaration rather than a cleverer
inference.** An absence cannot be disambiguated by staring at it harder: the writer
should say so. One field in the committed file — *this run records its unscoreable
cells* — turns a guess into a read, which is [R-ENF-06]'s own shape applied to a
per-cell dump. That touches five runs' writers and their committed files, so it
lands as its own piece rather than inside this one.

**One thing I nearly recorded as a defect and withdrew on checking the route.**
The census reports AMOC at 9/9, 100%, on every driver, and AMOC's own
`flatten_cells` skips unscoreable cells outright (`if le is None: continue`) — which
looks exactly like a false clean. It is not: AMOC is read through the MODULE route,
which recomputes from the live builder and sees every cell, so the 100% is real.
**The route decides whether a number means anything, and the route is not visible in
the row.**

What IS a defect, and it is mine from earlier in this session: the three flat writers
disagree with each other. ARCC and EGCH write an unscoreable cell as
`log_error: null, dropped: "non_positive"` — 99 and 770 such rows respectively —
while **AMOC skips it**. AMOC's committed artefact therefore cannot answer the
question the other two can; today the module route rescues the census, and the day
AMOC acquires an unscoreable cell its file loses it silently and nothing says so.
One line, and it goes with the declaration fix.

What this does NOT change: the census's substantive finding stands unaltered — 13 of
37 drivers lose cells, the omission is not one-signed (5 larger on the full sample,
8 smaller), and **EGCH's `fx` is scored on NONE of its 50 cells while its bias over
all of them is -5.743, appearing in no table this house publishes.**

## 07-09-2026 (2) — three per-cell files could not rebuild a single skill number they sit beside

The declaration fix turned out not to be the fix. Making AMOC record its dropped
cells exposed something larger: **the per-cell dumps AMOC, ARCC and EGCH commit
recorded only the MODEL's projection.** Every freeze and trend cell carried
`projected: null`, and any benchmark cell the log score could not take was
**silently skipped** — by the very branch whose docstring, which I wrote, said the
opposite: *"written with log_error null and dropped=... rather than omitted,
because a silently shorter sample is how an apparent improvement is
manufactured."* **True of the model's cells, false of the benchmarks'.** A comment
asserting a behaviour the code does not have is the [R-ENF-07] defect, arriving in
my own file, in the sentence written to prevent it.

Three defects, all fixed, **published scores byte-identical on all three runs**:

- **Benchmark projections are retained** (`row["frz"]`, `row["trd"]`), so the file
  can rebuild the number it sits beside. AMOC 873→945 rows, ARCC 3,194→3,250,
  **EGCH 3,259→4,125 — 866 cells, over a fifth of its true count, were absent.**
- **A dropped cell is written, not skipped.** ARCC was hiding 56, EGCH 866.
- **The REASON is derived from a test, never asserted from the absence.** My first
  cut labelled every missing error `non_positive`; on AMOC that was wrong on **63
  of 72** — the trend benchmark cannot be formed *at all* at origin FY2021, which
  is a different fact about a different thing. Now `not_projected` where there is
  no projection, `non_positive` where there is one the logarithm cannot take.

`engine/valuation_calibration/cells_reproduce.py` is the instrument: it reads each
run's committed cells, applies that run's **own** published skill definition, and
asks whether the answer comes back. **195 of 195 skill numbers now rebuild on AMOC,
ARCC, EGCH and PHDC.** Before today none of the first three could rebuild one.

**Two false results from my own probes, caught and named rather than published.**
A throwaway version reported 22 of EGCH's 28 numbers as mismatches with the sample
size agreeing *exactly* — the signature of a wrong probe, not a wrong run: the
tolerance was 1e-9 against a figure published to four decimals. And it looked for a
`drivers` key that ARCC does not use, found nothing, and printed **"0 reproduce, 0
do not"** — a run never examined, reported in the words of a run that passed. Both
are [R-ENF-04] verbatim. The committed instrument names every run's reader, reports
a run whose scores expose no skill number, and **REFUSES on zero comparisons**.

### What it then found in TMGH, and what is deliberately not concluded

**TMGH's committed cells rebuild 33 of its 148 published skill numbers.** The
mechanism is localised precisely and is not localised enough to blame anyone:

- the **model's** mean absolute error reproduces **exactly, in every block**;
- the **benchmark's** does not — on **66 blocks whose sample size agrees to the
  cell** it differs by about two per cent;
- on a further **35 blocks the benchmark sample is smaller than the model's**,
  while `model_mae` is the full-sample figure in **149 of 149 blocks** (it is the
  `summary` mae verbatim). Those pair two averages over **different sets** — which
  is exactly what PHDC's own `skill()` states in its source as the thing not to do:
  *"a model scored on a different sample from its benchmark is not being compared
  to it."*

**Whether the published number or the committed cells are the wrong half is NOT
decided here,** and that restraint is the point: equal counts over different sets
is arithmetically possible, so naming a culprit before tracing the pairing would be
the assertion this instrument exists to catch. Held on the instrument's own ratchet
with the measurement attached — allowed to disagree, may only shorten, and a run
that stops disagreeing while still listed goes RED.

THE GENERAL LESSON, WHICH IS NOT ABOUT SKILL NUMBERS: **A RECORD IS COMPLETE FOR
THE QUESTION ITS AUTHOR HAD.** These dumps were written to answer "which origins
carry the bias" and they answer it perfectly. The moment a different question
arrived — can this file rebuild the number printed beside it — the answer was no,
for three runs at once, and nothing anywhere said so, because a file recording one
side of a comparison looks exactly like a file recording both.

### The body took the same damage, and counting stamps could not see it

Closing the stamp defect closed **one instance and left the class open.** Re-reading
the digest's own text found the same union merge had spliced **five fragments into
the body — 2,035 characters**: a rule header repeated with a neighbouring rule's
sentence between the two copies (twice), a general lesson lifted out of one rule
and inserted into another, and a sentence left **cut off mid-clause**, so a reader
met `...however wrong the page is (` and then a rule title.

Every character was text that belonged somewhere else in the same file. **Nothing
was lost and nothing was invented — which is exactly why no gate, no diff and no
reader caught it.**

**The full protocol took no damage at all from the same merge**, and that is the
finding rather than a detail: it has line breaks, so git resolved it hunk by hunk;
the digest is one line, so the resolution was a splice. Yesterday I recorded that a
single-line file has no merge granularity and framed the cost as reviewability.
**The cost is correctness.**

Repaired by removing exactly the five spliced spans, each verified as a duplicate of
text surviving elsewhere and each join checked to read grammatically; rule-id sets
unchanged at 39/39. Closed by `check_protocol_sync` refusing any passage of 300
characters or more appearing twice — arithmetic about the file, not a word list. The
window is measured rather than chosen: two sentences of this prose, short enough for
the shortest real splice (106 characters of overlap) and long enough that house
phrasing cannot reach it. **The three passages that do recur are named with their
reasons**, because an allowance nobody has to justify is where the next splice hides.

**Two of my own instruments failed first, and both failures are the record.** The
first scan sampled windows at every tenth offset and reported **three splices where
there were five** — two copies whose offsets differ by a non-multiple of the step
are never both sampled, so it was structurally blind to most of what it was looking
for **and printed a number rather than an error**. That is the third time today a
probe of mine returned an answer that was absent rather than wrong. The negative
control's landing assertion then reproduced the identical shortcut and had to be
rewritten to scan every offset; and its clean fixtures were built from one padding
sentence repeated three times, so they carried the very defect they existed to prove
absent — the check flagged them, and was right to.

THE GENERAL LESSON: **A CONTROL THAT PROVES A CHECK IS SOUND IS ITSELF A THING THAT
CAN BE WRONG IN THE SAME WAY AS THE CHECK.** Both my sampled scan and the assertion
meant to guarantee it had landed shared one bug, because I wrote them minutes apart
in the same frame of mind. The only thing that separated them was that one of them
failed loudly.

### TMGH traced: the skill was never a paired comparison at all

I left this open a few hours ago as "which half is wrong is NOT decided", and the
answer is neither of the two possibilities I had in mind. TMGH's construction was:

```
cell["skill_" + nm] = {"n": min(sh["n"], b["n"]),
                       "model_mae": round(sh["mae"], 4),      # model over ITS OWN cells
                       "bench_mae": round(b["mae"], 4),       # benchmark over ITS OWN
                       "skill": round(1 - sh["mae"] / b["mae"], 4)}
```

**There is no intersection anywhere in it.** Each mean is over whatever cells its
own setting happened to resolve, and the sample size printed beside them is
`min()` of two counts — **a number belonging to neither sample.** That is the one
thing a skill figure may not be, and this run's own siblings say so in their
source: *"a model scored on a different sample from its benchmark is not being
compared to it."*

The cells were never the wrong half. What localised it was the instrument's own
split reading — the model's mean absolute error reproduced **exactly in every
block** while the benchmark's did not, which is only possible if the pairing is
where the difference lives.

Corrected to pair on shared cells, the construction the other four runs already
use. **115 of 148 figures moved — HIGHER in 69, LOWER in 46**, median 0.0818, max
2.8577; `by_driver`, `by_era` and `macro_split` came back **byte-identical**, so
only the skill numbers were ever affected. The delivered training record quotes no
skill figure, so no delivered document moves. **All five runs now rebuild: 310 of
310.** The ratchet entry came off the same day it went on, and the gate goes red on
a listed run that stops disagreeing, so the removal is forced rather than tidy.

THE GENERAL LESSON, WHICH IS NOT ABOUT SKILL: **A WRONG ANSWER AND A WRONG QUESTION
LOOK THE SAME FROM OUTSIDE.** I framed the open question as *which half is wrong,
the published number or the cells* — a sensible binary, and both branches were
wrong, because the defect was in an operation neither half performs. The
instrument's finer reading, that one side reproduced perfectly and the other did
not, is what pointed at the join rather than at either end; **a measurement that
splits its own result is worth more than one that reports a verdict.**

### The false unmeasurable closed: the schema is the declaration

`scoring_blindspot` reported PHDC NOT MEASURED because its per-cell file records
no dropped cell, on the stated ground that its writer *"emits only the cells its
score TOOK"*. **Measured by running the writer: 403 rows, 403 scoreable, zero sign
cases — and it has always emitted an unscoreable cell when one occurs.** The file
recorded no drop because **the run drops nothing.** A false unmeasurable is an
absent answer wearing the costume of a careful one.

The detection rule — *a file with no null error cannot be told apart from a run
with nothing to drop* — is right in general, and **an absence cannot be
disambiguated by inspecting it harder.** So the writers now declare instead: TMGH
and PHDC carry `dropped` on **every** row, including the scoreable ones, so the
key's presence is the declaration and its value is the fact. That is [R-ENF-06]'s
shape applied to a per-cell dump, and it needs no new metadata field.

**Adding the key broke seven filters that tested key-presence**, which is exactly
why the two writers had differed in the first place — `"log_error" in r` was doing
the work `is not None` should have done, in `summarise`, the era split, the median,
the skill pairing and the block bootstrap. All seven re-pointed; **both runs'
`scores.json` came back byte-identical**, which is the only thing that makes the
change safe to keep.

PHDC now measures at 9 drivers, all 100% taken, and the census reads **13 of 46**
drivers losing cells rather than 13 of 37 — the same finding on a population that
is now complete rather than quietly nine drivers short.

Also corrected in the same pass: the adapter's comment claiming *"TMGH and PHDC
expose no module-level `cells()`"*. **Both do** — I called PHDC's directly. It was
a claim about the code that nobody had tested, sitting in a comment, which is the
defect this repository keeps finding in its own files and which [R-ENF-07] names:
a comment asserting a property the code does not have stops the next reader looking.

THE GENERAL LESSON: **A CONSERVATIVE RULE STILL HAS TO BE RIGHT ABOUT WHAT IT IS
BEING CONSERVATIVE ABOUT.** Refusing to answer where the evidence is ambiguous is
correct, and the reason attached to the refusal was false — so a reader was told
something about PHDC's writer that would have survived review, discouraged the one
check that resolves it, and left a run permanently unreadable for no reason.

### Every published driver bias now states the coverage behind it

**A driver scored on half its history publishes a bias that looks exactly like one
scored on all of it.** The log score drops cells where either side is non-positive
— correctly, and silently — and every run's record then printed `n`, the count
taken, with the count that *exist* nowhere. The two agree on revenue and cost,
which are always positive, and come apart on exactly the bottom-line drivers a
valuation depends on.

Now measurable off the record rather than by running a census by hand: **six of
EGCH's fourteen drivers are scored on under half their cells — `net` 23/55, `pbt`
23/55, `other_bucket` 23/55, `selling` 21/55, `tax_current` 21/55, and `urea_t` at
3 of 55.** All 88 drivers across the five runs carry the pair, verified against
each run's own committed cells; **everything else in all five `scores.json` came
back byte-identical.**

`scripts/check_driver_coverage.py` requires **the disclosure and never a level.**
There is no threshold and there deliberately will not be one — a driver genuinely
scored on few cells is a fact about that company's history, and a cutoff would be
the free parameter the promotion rule forbids. What a record may not do is go quiet
about it, which is [R-SIGCM-02]'s shape exactly: a coarser level is permitted,
going quiet about it never is. Negative-controlled on six red and **three clean,
the clean half being the one that matters** — a driver honestly scored on under
half, and one scored on none, must both stay green, because a gate that failed on
them would push a run to drop the disclosure or narrow the denominator.

**I committed the very defect this field exists to close, while closing it.** The
first cut put `n_cells` on the internal `drivers` block — and every census, and any
reader, reads `by_driver`. The disclosure went into the working papers rather than
onto the page, and it took a reader that returned "0 drivers carry the pair" on two
runs to notice. Corrected to the block a reader actually reads.

THE GENERAL LESSON: **A DISCLOSURE PUT WHERE THE PROCESS KEEPS ITS WORKING IS NOT A
DISCLOSURE.** It satisfies the author, survives review, and is invisible to
precisely the audience it was written for — which is [R-MACRO-01 AMENDED]'s finding
about exemptions arriving from the other direction: there a true statement sat on
the wrong object, here a true statement sat in the wrong place.

## 07-09-2026 (3) — the boundary test now gates, and it agrees with the runs' own procedures

**A correction to what I reported earlier.** I recorded that the book held twelve
correction candidates, all in ARCC, with exactly one ADOPTED — so the boundary
result "binds on what is adopted NEXT, not on anything already in the book." **That
count read only ARCC's `disposition` field and missed PHDC entirely**, whose
expanding-window rule applied a non-zero correction to four drivers, each with the
stated reason *"sign stable across eras"* — precisely the claim the boundary test
interrogates. Five subjects, not one.

Tested at every cut the data admits:

| run | driver | cuts | flips | the run's own verdict |
|---|---|---|---|---|
| ARCC | `mfg_dep` | 4 | **0** | ADOPTED — "the one candidate that survives both clauses" |
| PHDC | `is.finance_cost` | 5 | **0** | "only one correction passed its own test" |
| PHDC | `asp` | 5 | 4 | declined |
| PHDC | `units_delivered` | 5 | 2 | declined |
| PHDC | `units_sold` | 5 | 1 | declined — "no resolved cells" |

**The agreement is exact and it runs the unusual way.** An instrument neither run
used, applied at every admissible boundary rather than the one each chose, confirms
precisely the two corrections those runs promoted and refuses precisely the three
they declined. **That is evidence FOR the existing procedure**, which is not what
this session has mostly been producing.

**Scope, stated rather than overstated, because I nearly got this wrong.** My first
reading was "three of PHDC's applied corrections fail the boundary test", which
sounds like a published record resting on an unstable sign. It does not: `score.py`
does not import `corrections` at all, so the scored record is the uncorrected one
and the corrections are the adjusted-vs-raw test [R-FCAL-01] requires. **No
delivered number turns on any of this.** The three are on the gate's ratchet with
that measurement attached, because rebuilding PHDC's adjusted-vs-raw artefact under
a cut-invariant rule moves that run's record and deserves its own measured pass.

`scripts/check_correction_boundary.py` imports `boundary_sensitivity` rather than
reimplementing the arithmetic [R-ENF-03], and `cuts_for()` was extracted for it with
the census's output verified byte-identical afterwards. Negative-controlled on five
red and three clean; **the fixtures are derived from the data rather than named by
hand** — the first draft hardcoded `cogs`, which is not an ARCC candidate at all,
and the landing assertion said so — and the thin-driver case **creates** its
condition rather than hunting for one, because no ARCC driver is thin enough and the
only run with thin drivers adopts nothing.

THE GENERAL LESSON: **A COUNT TAKEN THROUGH ONE FIELD IS A COUNT OF THAT FIELD.**
"Twelve candidates, one adopted" was true of ARCC's `disposition` column and false
of the book, and it read as a fact about the programme because the field it came
from was the obvious place to look. Where five records have five shapes, a census
needs five readers or it is measuring the one it understands.

### [R-FCAL-01] amended: "across eras" named a boundary chosen for the market

The gate landed an hour ago enforces cut-invariance while both governing documents
still said the sign must hold *"across eras"* — **a rule stating one thing while
its own gate enforces another**, which is the defect I closed in the revision stamp
this morning, arriving in a rule I had just written the enforcement for.

Amended in both documents in one commit, stamps to `2026-09-06f`. **Every era label
in this book is the year its currency moved** — the right cut for a currency and
not every driver's break — so the clause was satisfiable by a bias stable at one
line and unstable at four others, with nothing saying which kind a given correction
was. The sign must now hold at every cut the data admits.

**The amendment changes no verdict this book has reached, and that is the strongest
evidence for it.** Applied to all five corrections ever applied or adopted here, the
cut-invariant test confirms exactly the two each run promoted and refuses exactly
the three they declined. A rule change that overturned a pile of past conclusions
would be a rule change fitted to a grievance; one that reproduces every existing
verdict while making the reasoning honest is the other kind.

THE GENERAL LESSON: **A STABILITY CLAIM IS A CLAIM ABOUT A BOUNDARY SOMEBODY
CHOSE.** Where that boundary was chosen for a different reason than the quantity
being tested — a currency's year, applied to a depreciation schedule — the claim is
partly about the chooser, and no amount of care inside the test will say so.

### The rebuild attempt found a design error in the gate I built an hour ago

Rebuilding PHDC's corrections under the amended cut-invariant rule — the ratchet
debt I created this morning — **was reverted, and the reason is the useful part.**

What the amended rule actually did was **not** what I expected. It dropped `asp`
and `units_sold`, correctly. It also **corrected more, not less**: `is.finance_cost`
went from two origins to four, `units_delivered` from one to three, and `is.sga`
appeared at one. The old era test required two eras each carrying two or more
resolved errors, which early origins do not have; the cut test needs only one
admissible cut, which arrives sooner. Two effects in opposite directions, and the
permissive one is larger.

**Then the gate went red on a driver the amended rule had just adopted.** `is.sga`
flips at **6 of 6 cuts** on the full record, and the rule applied it because at
origin 2022's own expanding window there were two cuts and neither flipped. The
log's own words: *"sign stable at every one of 2 cuts"* — which sounds strong and
establishes very little, and is the [R-CAL-02] failure exactly: **a
cautious-sounding claim is still a claim and gets audited like one.**

**The defect is in my gate's scope, not in the run's rule.** The expanding window at
2022 genuinely could not see the later flip, and point-in-time discipline is
absolute — a method must be judged on what it knew. My `_phdc` adapter puts
*applied-at-any-origin* in scope and then judges it against the **full panel**,
which asks a question the method was never allowed to answer. An applied correction
should be judged on **that origin's own window**, with the full-panel reading
reported beside it as information.

So the correction rule is unchanged, the ratchet stands, and the gate's scope is the
next piece. The gate did its job in the only way that counts: **it went red on work
I had just done and believed was right.**

THE GENERAL LESSON: **A CHECK BUILT FROM A CENSUS INHERITS THE CENSUS'S VANTAGE.**
`boundary_sensitivity` looks at the whole record, which is right for asking what a
driver's history shows; a gate on a point-in-time method needs the vantage of the
origin, and reusing the instrument imported its viewpoint along with its arithmetic.
Where an instrument is borrowed, the arithmetic travels and so does the question it
was written to answer.

### The gate now asks each correction the question its own vantage allows

Reworked, and the distinction it draws is the whole point: **an act at an origin is
judged on what that origin could see; a claim about a driver is judged on the whole
record.** An expanding-window correction is tested on the resolved history available
at its origin — the run's own definition, reconstructed from its committed cells
and **verified against the counts the run itself recorded, 50 of 50 windows
matching** — while an adopted disposition is tested on everything. The whole-record
reading is printed beside every act and never gates, because condemning a method
for not knowing the future is exactly what point-in-time discipline forbids.

What that changes, read off the gate:

```
PHDC   asp as at 2023               FLIPS at 2 of 4 cuts   [whole record: 4 of 5 flip]
PHDC   is.finance_cost as at 2023   survives all 3 cuts    [whole record: 0 of 5 flip]
PHDC   is.finance_cost as at 2024   survives all 3 cuts    [whole record: 0 of 5 flip]
PHDC   units_delivered as at 2023   survives all 4 cuts    [whole record: 2 of 5 flip]
PHDC   units_sold as at 2023        FLIPS at 1 of 4 cuts   [whole record: 1 of 5 flip]
```

**`units_delivered` came off the ratchet the same day it went on, and not because
anything in the run was fixed.** Judged on the whole record it flips at two of five
cuts; judged on what origin 2023 could actually see, it survives all four. *The act
was sound on its own information and the driver is unstable in hindsight* — two
different findings, and the first draft of the gate could only express the second.

**A negative-control case moved from clean to red, and the move is the finding.**
The first draft asserted that adopting a driver too thin to cut must stay green, on
the reasoning that untestable is not a failure. For an *adoption* it is: adopting a
correction is a claim the sign is stable, and a driver with no admissible cut
carries no evidence of stability at all — [R-ENF-04]'s own clause, and the stronger
objection rather than the weaker one. The fixture was kept and its expectation
inverted rather than deleted, which is the sharpest evidence the change took effect.
Both docstrings corrected to what the code now does; **6 red, 2 clean.**

THE GENERAL LESSON: **THE SAME MEASUREMENT ANSWERS TWO QUESTIONS AND ONLY ONE OF
THEM IS ABOUT THE METHOD.** "Is this driver's bias stable?" and "was applying this
correction defensible?" run the same arithmetic over different windows, and a check
that picks the wider window every time is not stricter — it is answering the
question the method was never asked.

### L-352 needs no gate, and the reason is arithmetic rather than a shrug

The open item read *"L-352 has no obvious gate shape and may be a lesson that stays
prose."* Measured rather than left as a hunch: **its gateable half is already bound,
an order tighter than its own evidence could justify a threshold at.**

L-352 says the gap between what a company charges and what it pays holds almost
still while the rate both climb at moves enormously. A drifting spread **is** a
drifting margin path, and [R-ANCHOR-01] clause two already refuses a forecast whose
rate declines 5% relative from its own opening year without a named, sourced,
like-for-like-measured mechanism. Solving for the spread drift that trips it over a
five-year window:

| base margin | drift that trips [R-ANCHOR-01] |
|---|---|
| 10% | 0.111% a year |
| 20% | 0.251% a year |
| 30% | 0.432% a year |
| 50% | 1.021% a year |

**Against L-352's own measured drift across 26 name-years: −0.37%, +0.61%, +0.97%.**
At any margin below about half, the existing anchor gate fires well inside the range
this lesson's evidence calls flat — so a new threshold could only be looser than
what already binds, and a looser gate that duplicates a tighter one is the
permanently-green check, which is [R-CAL-03]'s decorative test wearing a new hat.

Its other half — *hold nothing still* — is L-353 and is already arithmetic in
`check_frozen_escalator.py`, which tests **connectivity rather than magnitude**: a
line whose value is identical when every inflation rate the run carries is doubled
at source is wired to none of them. Zero is not a threshold, so no free parameter
enters.

**So L-352 stays prose, and that is a decision with a reason rather than an item
nobody closed.** What remains in it is guidance about where to spend effort — get
the rate right before the gap — which is exactly the kind of thing a register
carries and a gate cannot.

THE GENERAL LESSON: **BEFORE BUILDING A CHECK, SOLVE FOR WHAT THE EXISTING ONES
ALREADY REFUSE.** "This lesson has no gate" was true and unhelpful; the useful
question was what a gate for it would have to be tighter than, and the answer came
out of arithmetic already in the protocol.

### An acceptance criterion named a gate that did not exist

Part E criterion 1 lists seven gates that must be green with negative controls
before the programme is complete. **Six are. The seventh,
`check_corrections_applied`, had never been written** — while criterion 2 requires
in terms that *"every claimed correction reconciles to its log"*.

An acceptance criterion naming a check nobody wrote cannot be met, and nothing was
counting it: **[R-ENF-01]'s own failure applied to the definition of done rather
than to a study.** The programme has spent days building gates over the work while
its own completion test carried a hole.

Built and green. A study claiming a correction must name a run that ADOPTED it, on
the same driver, at a factor reproducing from that run's own committed bias at the
half strength [R-FCAL-01] fixes. Population: four studies make a claim either way —
AMOC, EGCH and TMGH declare none, and **ARCC's `manufacturing depreciation` claims
1.0298 against `exp(−bias/2) = 1.0298` from its own log.** A study declaring none
while its run adopted one is a failure, because silence and "none adopted" are the
same file to a reader and different facts about the work.

**Matched on meaning rather than on the word, and that clause was earned in the
first five minutes.** Searching for "correction" found SCEM carrying
`corrections_applied: 69` — a count of *editorial* corrections in a revision note,
on a study with no walk-forward run at all. A gate keying on the word would have
opened with a spectacular false positive about a study that has done nothing wrong.
The case is kept as a clean fixture, asserted against the real file.

Negative-controlled on six red and three clean; CI now runs 115 steps.

THE GENERAL LESSON: **A PLAN'S ACCEPTANCE CRITERIA ARE THE LEAST-CHECKED PROSE IN
THE PROJECT.** Every rule here is enforced from outside by something; the document
that says when the work is finished was enforced by nobody, and it named an
instrument that did not exist for five days without anyone noticing — including on
the days its own list was read aloud to decide what to do next.

### Part E, printed for the first time: criterion 1 is not met, by 52 entries

The criteria say in their own first line that the plan is complete when all of them
hold **"and are printed by the gates, not attested."** Nothing printed them. Printed
now, `engine/method_reassessment/acceptance.py`:

**All seven gates are green with negative controls** — the seventh built an hour
ago. **And the ratchet half is not met, by a wide margin.** Criterion 1 requires the
ratchet lists to carry *only names not yet re-issued*; the five re-issued names
carry **52 entries across 41 lists**:

| name | lists |
|---|---|
| PHDC | **15** |
| AMOC | 12 |
| TMGH | 12 |
| ARCC | 7 |
| EGCH | 6 |

Every one of the five is on `walkforward_scope`; four are on `frozen`, `output`,
`rebuild` and `actuation`. **The programme has been treating these five as
re-issued and behind it, while its own completion test says a re-issued name
carries no ratchet debt.**

**Three probes gave three different numbers before one was right**, which is the
day's theme arriving in my own measurement. Matching the ticker anywhere in the file
counted prose inside `_why` fields (22 lists). Matching only ticker-shaped keys
missed the ratchets keyed by document **path** — `engine/arcc_study/ARCC_Bibliography…docx::Date`
— and returned 20. Reading both shapes gives 21 lists and 52 entries. The two wrong
answers erred in opposite directions, so neither could have been caught by
plausibility.

The instrument **prints and does not gate**, deliberately: a check red until the
programme finishes is the permanently-red check [R-ENF-02] forbids. And it **refuses
to report on what it cannot measure** — criteria 2, 3, 5 and 6 are listed as
unmeasured rather than passed, criterion 3 because its own scorer returns a date
until vintages mature, criterion 6 because "each opened and read" is a human act no
script may attest.

THE GENERAL LESSON: **THE DOCUMENT THAT SAYS WHEN THE WORK IS FINISHED IS THE ONE
NOBODY CHECKS.** It names instruments, sets conditions and is read aloud to decide
what to do next — and it was the last prose in this project to get an instrument of
its own, five days after a gate it names stopped existing.

### The 52 sorted: 49 are real debt, 3 were stale and are pruned

The open question was whether criterion 1's 52 entries are debt a re-issue should
have cleared or listings nobody tidied. **Measured rather than argued**, by copying
the tracked tree into a sandbox, running every prune-capable gate there, and
diffing the ratchets against the real ones: **49 of 52 are real debt the gates
still fire on.** Three were stale — `anchor` on PHDC and TMGH, `valuation_inputs`
on TMGH — and are pruned, which a ratchet always permits. Criterion 1 now reads 49.

So the answer is the unwelcome one: **this is not bookkeeping.** PHDC 14, AMOC 12,
TMGH 10, ARCC 7, EGCH 6 — every one of them a gate that still fires on a name the
programme has been treating as re-issued and behind it.

**And the first version of this measurement reported "stale: 0", which was my own
probe comparing the sandbox to itself.** The `cd` into the sandbox put the
comparison's *both* sides there, so it read the pruned files as the baseline and
found no difference — an answer that was absent rather than wrong, arriving in the
fourth probe of the day to do it. Redone with absolute paths on both sides, and the
real tree verified untouched before believing either number.

THE GENERAL LESSON: **A BEFORE-AND-AFTER NEEDS TWO PLACES, AND A `cd` MOVES BOTH.**
The comparison was correct in structure and read one directory twice, which returns
exactly what a clean result looks like. Where a probe reports no difference, the
first thing to check is that it was looking at two things.

### 31 of the 49 entries carry no reason, which is why the pile could not be sorted

Reading the 49 individually: **18 carry a reason and 31 are bare** — listed with a
ticker and nothing else. That is why the split into *"debt a re-issue should have
cleared"* versus *"legitimate outstanding work"* could not be made: **most of the
pile does not say what it is.**

The 18 that do read usefully, and they are not one kind: `colwidth ARCC "declared
0.76cm, needs 0.84cm"` is a minute's work; `walkforward_scope` on all five says *"a
run exists and the study states no scope decision"*; `terminal PHDC` says its charge
*"resolves and its charge does not, so the 1/g test has never run"*; `workbook_values
AMOC` says its `recalc.py` refuses because it was written for the nine-sheet
workbook. Some are trivial, some are real method debt, and **nothing distinguishes
them from the 31 that say nothing at all.**

This repository already has the rule, in my own words in a ratchet written this
morning: *"the reason is required and is the diagnosis owed, not an excuse — an
entry that cannot say what was measured is a silence with a filename."* Thirty-one
entries on the five re-issued names are exactly that.

**A book-wide count was attempted and is NOT established.** Two parsers returned
106 entries with 36 bare and 49 with 31 bare, because the 41 lists have no common
entry shape — some key by ticker, some by document path, some by list. That is the
correction-boundary lesson arriving again: *five records, five shapes, a reader that
guesses finds nothing.* **The figure I can defend is the one I read by hand: 18 and
31, on the five.** The book-wide number needs each gate to report its own ratchet,
which is a piece of work rather than a census.

### The criterion-1 decision is registered rather than left in a message

Reporting a decision in chat and leaving it there binds nothing — [R-IND-01]'s own
complaint. Registered as `PARTE-criterion-1-ratchet-clause` with three routes run,
what was done meanwhile, a recommendation and a **default that fires 21-09-2026:
treat the clause as written and clear the 49 rather than amend it.** A programme
that softens its acceptance test when the test fails has no acceptance test;
clearing is work I can do without permission, amending the definition of done is
not.

Its `resolves_when` names the plan file and a marker, so the gate detects the ruling
arriving rather than waiting for someone to close the entry — and writing it as
prose **crashed `escalations.is_resolved` with an AttributeError three frames down**,
where a broken record reads as a broken checker. The module now names a malformed
field instead. 14 escalations shaped; the negative control's 18 conditions hold.

### CI went red, and it went red on the rule I had just been enforcing

`f213fdc1` failed: **"1 study-scoped gate on disk is named in none of the three
lists: check_corrections_applied.py."** [R-ENF-07]'s new-study gauntlet requires
every study-scoped gate to be classified — refuses an empty study, artefact-
conditional, or excluded with a reason — **in the commit that adopts it**, because
*a gate nobody listed is a gate the run never tested while still reporting clean.*

I built that gate three commits ago to close an acceptance criterion and did not
classify it. **The failure shape the gauntlet exists to close, occurring inside the
work that was closing another one.** Classified as artefact-conditional — an empty
directory carries no numbers file and so makes no claim, and the gate bites on the
claim — with a planted offender that asserts a correction no run adopted. **34 of 34
gates refuse a new study.**

### Four of the five now state their walk-forward scope, and it was transcription

`walkforward_scope` was on all five names' ratchets. The decision was not missing —
**AMOC, ARCC, EGCH and TMGH each state it in their own run's pre-registration,
section 0**, and it was never carried into the study's record where the gate reads:
*"the rule was not disputed and not hard, it simply was not present."* Transcribed,
not re-decided — AMOC LIGHT on 5 sourceable years, ARCC FULL on 12, EGCH FULL on 18,
TMGH FULL on 16, each `basis` quoting its own pre-registration. **PHDC is left**: its
pre-registration is dated 30-08-2026, one day before [R-FCAL-01] existed, and states
no scope. Inventing one is what SIGCM forbids.

**And regenerating TMGH's numbers surfaced that its committed file was already
stale.** 60 leaves differ — driver scores, forward ranges, statement net-profit
bands. Tested rather than assumed: checking out HEAD into a sandbox and running
`build_numbers.py` **with no edit of mine** reproduces the same 60 differences, so
the staleness predates today's work and my regeneration is the fix. That is
[R-ENF-06]'s defect exactly — an artefact a builder reads moved and the file reading
it was never rebuilt — and it was invisible because nothing compares a study's
numbers to what its own generator would produce now.

Everything else in all four files is byte-identical; eleven gates that read study
numbers are green.

THE GENERAL LESSON: **A GATE ADDED WITHOUT BEING CLASSIFIED IS A GATE THE SYSTEM
CANNOT SEE.** The gauntlet's whole claim is that a new study cannot walk past the
set — and the set is whatever has been declared to it. Adding an instrument without
telling the system it exists leaves both the instrument and the claim weaker than
before, and only the system-level check catches it.

## 07-09-2026 — does a study's numbers file still reproduce from its own generators?

Nothing in this repository had ever asked. `check_numbers_generators.py` says in its
own docstring that it deliberately does not — running every study's model takes
minutes and would fail for reasons unrelated to the defect it was built for. So the
question was open by design, and the design had never been tested.

**Measured**: a sandbox at HEAD, each study's own generators run in their declared
order, the committed numbers file diffed against what came back.

- **19 of 24 reproduce byte for byte.**
- **3 differ, and all three differ the same way** — `engine/terminal_value.py` grew
  five record fields after they last built (FERTIGLOBE 4 records, PHAR 2, SCEM 1).
  The missing fields are `maintenance_age_basis`, `maintenance_age_years`,
  `maintenance_escalator` and the two `average_age` inputs.
- **2 cannot run at all**: GBCO's `compute.py` passes `rf=` to a v2 `WaccInputs` that
  rejects it, and XPT's `compute_xpt.py` imports the retired `mc_v2`. Both are named
  in the digest's open items as things a re-issue would have to rebuild rather than
  patch — **confirmed live rather than remembered**, which is the point of running it.

**Nothing valued had moved, and that is part of the finding rather than a mitigation
of it.** The escalator is applied inside `build()` and always was, so every terminal
in those studies was struck at current cost exactly as [R-TERM-01] requires. What was
missing is the record *of* it — [R-ENF-06] one level up, and it matters for the same
reason: a record that does not name the quantity a value was built from cannot be
rebuilt or graded afterwards, and it looks complete while it cannot.

**The probe was wrong twice before it was right**, and both are the standing failure
shape. The first run reported two crashes that were *my own* missing PYTHONPATH, not
the studies'. The second could not tell a generator that reproduced its file from one
that never wrote it — every "REPRODUCES" would have read identically. Re-run with the
path set and an mtime landing assertion: no study silently no-op'd, and the two
crashes are real.

**The cheap test finds exactly what the expensive one does.** A static walk of the
committed records against the field set `terminal_value.build()` emits today names the
same three studies, in under a second, with no model run — because the only thing that
had drifted was a field set. That is now `scripts/check_terminal_record_shape.py`,
negative-controlled on 10 conditions (7 red, 3 clean), classified ARTEFACT-conditional
in the gauntlet, 35/35.

**Conformed rather than ratcheted**, so the list starts empty: regenerating adds the
fields, deletes nothing, and moved no valued figure in any of the three.

**One of them needed its generator fixed first, and that is the more useful half.**
FERTIGLOBE stamped `meta.asof` with `date.today()`, and `docx_fertiglobe.py` prints
that value as "Study date" — so *rebuilding the study restamped a delivered document's
account of when the work was done*. A study date is a fact about when the study was
struck, not a clock reading. Frozen to `2026-09-04`, which is what the delivered
document already prints (read out of its own `document.xml` rather than chosen), so
the generator now reproduces its own output and no document changes.

**The general lesson, which is not about terminals:** a module and the records it
wrote are two different vintages, and only the module moves on its own. Every gate here
points from a record back to the model and asks whether the figures came from it; none
asked whether the record still has the shape the writer emits — a question answerable
without running anything, which is why it was worth asking of all 24 at once.

## 07-09-2026 — a negative control wrote its fixture into the record it protects

CI on 7f524a0c came back with two gate failures, both the same cause and neither in
the work that was pushed. `engine/escalations.json` on that head held ONE entry,
called `NC-example`, and the thirteen real ones were gone — replaced by its own
negative control's fixture, and committed.

**The mechanism was the control's own design.** Every other negative control here
copies what it tests into a temp sandbox. This one wrote the fixture into
`engine/escalations.json` and copied a backup over it in a `finally`. A `finally`
survives an exception; it does not survive a kill, a timeout, or the process going
away. It is the only control in this repository shaped to mutate the artefact it
exists to protect, and the artefact it protects is the register that stops a question
being asked twice — so losing it costs precisely what [R-IND-01] was adopted to
prevent.

**It then failed in a way that reads as a finding about the work.** The fixture's
`resolves_when` marker sat in the committed file, so the gate reported the escalation
as already answered and went red — a true statement about a file that should not have
existed, on a head whose actual changes were clean.

**Closed at the mechanism, not the instance.** `engine/escalations.py` now reads
`TESTAHIL_ESCALATIONS_REGISTER` where it is set, so the control points the READER at a
temp file and the real one is never opened for writing; CI sets nothing and reads the
real path; and where the override is in force the gate PRINTS it, so a run against a
fixture can never read as a run against the record. The control asserts, on **every
case rather than once**, that `engine/escalations.json` is byte-identical after the
gate runs.

**A second fragility surfaced while fixing the first, and it is the more interesting
one.** The clean fixtures' `resolves_when` named `engine/escalations.json` itself, so
they depended on the repository's own history never containing a string the control
defines — and the moment the fixture leaked into a commit, two clean cases went red
for a reason that had nothing to do with what they test. *A control whose cases can be
poisoned by its own fixture escaping breaks exactly when something has gone wrong.*
Re-pointed at a path that does not exist, which is also the honest shape of an open
escalation: the artefact that would carry the answer has not been written yet.

Register recovered from `f213fdc1^` (13 entries) and
`PARTE-criterion-1-ratchet-clause` rewritten from the routes actually run, labelled as
a rewrite rather than passed off as the original text — it was registered in that
commit and never survived into it. 14 entries, 18 of 18 control conditions hold.

**The general lesson, which is not about escalations:** a test that mutates production
state and undoes it afterwards is correct exactly as often as it completes. The undo is
the part that does not run when something goes wrong — which is the one occasion when
the state matters. *Where a check needs different inputs, give it different inputs;
never give it the real ones and a plan to put them back.*

## 07-09-2026 — a document cannot witness its own age

[R-DOC-01] says the digest is named for the day of its **latest amendment**, so that the
filename and the revision stamp "agree on their face". While fixing something else I
checked whether anything enforced it. Nothing did — `check_protocol_sync` resolves the
digest **by pattern** and then never asks what the pattern matched.

**A first draft of the fix compared the filename's date to the stamp's date, and passed.**
Of course it did: both are typed by the same hand in the same edit, and they had never
disagreed. That draft was measuring nothing.

Measured against the world instead: three amendments landed today at 00:45, 01:02 and
01:25 UTC carrying `2026-09-06d`, `e` and `f` under a filename dated `06-09-2026`. Every
one internally consistent, every one naming a day the edits were not made on, and every
check in the repository green through all three — including the sync gate whose own rule
this is.

**Two fields that agree with each other and not with the world is the self-attested
boolean [R-ENF-01] closes everywhere else** — in the one place this document had not
searched: itself.

The only witness outside a document is when it was committed. The stamp is now held
against the last commit touching either governing document, or against today where they
sit amended in the working tree. **The zone is admitted rather than resolved by picking
one:** the project's clock is Cairo and CI runs in UTC, so a commit in the last three
hours of a UTC day falls on two different days depending on which is meant, and choosing
one would be a free parameter. Both readings are accepted; what is refused is a stamp
matching neither.

Negative-controlled on six conditions against **real little repositories** rather than
strings — a defect made of two fields agreeing with each other cannot be reproduced by
text alone. The clean half includes a commit at 22:30 UTC where both days must be
accepted, and an amendment sitting in the working tree, which is dated now rather than by
a commit made years earlier.

Digest renamed to `PROJECT_INSTRUCTIONS_07-09-2026.md`, both stamps at `2026-09-07a`, the
CLAUDE.md include line moved with it, and the digest's one self-reference re-pointed —
which `check_protocol_text` caught within the minute, working exactly as intended.

**The general lesson, which is not about dates: a document cannot witness its own age.**
Everything inside it was written at the same moment by the same hand, so any two fields in
it will agree. The question a stamp exists to answer is about the world, and answering it
needs something the author did not type.

## 07-09-2026 — a check's scope is the shape its matcher needed, not the shape the rule meant

`check_protocol_text` has verified since its adoption that the governing documents "name
nothing that does not exist". Its matcher required a directory prefix, so it saw every
reference carrying one and none that did not.

**Found by following a broken import, not by reading the rule.** XPT's generator cannot run
because it imports the retired v2 engine module — and the digest described that module in a
sentence telling a reader it was *available for reference*. It is not in the tree at all.
Measured: **twenty scripts import it**, seventeen in the lab (dead research scratch is
ordinary there) and **three inside a study directory**, which is a study that cannot be
rebuilt from its own code.

The prefixed half was never the interesting half. A path is easy to check and easy to write
correctly; a bare name is how anyone actually refers to a module in prose, so the uncovered
form is the one these documents use most.

**My own first measurement was wrong, in the standing way.** It skipped any path containing
`/.git` and so silently dropped `.github`, reporting two workflow files as missing when both
sat on disk. Re-run with the exclusion naming the *directory* rather than matching a
substring: three bare names resolve to nothing, and two of those are legitimate — a harvest
cache the documents themselves declare never committed, and the tail of a braced template.
**One real defect**, which is what the check now refuses.

**It then caught the desk that wrote it.** My own amendment used `engine/x.py` and `x.py` as
illustrations, and those are claims about files by the gate's own rule. Reworded rather than
exempted.

Exceptions are named with reasons rather than pattern-excluded — an allowance nobody has to
justify is where the next stale claim hides. Negative-controlled on seven added conditions,
three red and four clean, every fixture asserting first that the name it names is genuinely
absent from or present in the tree. Both stamps at `2026-09-07b`.

**The general lesson, which is not about filenames:** nobody decided that only prefixed
references would be verified — a regex was written for the references in front of it, and the
rule quietly inherited that boundary. Where a check has been running a long time, read what
it *matches* and ask what the rule actually claims.

## 07-09-2026 — a standard obeyed everywhere is still unenforced

Depth-bar standard 2 requires every input to be four-field complete — value, source, date,
research layer — "validated by assertion". What validated it *outside* a study was
`provenance_four_field`, **a boolean each study sets on itself**: the shape [R-ENF-01]
closes everywhere else, and the shape [R-ENF-02 AMENDED] already closed once on another
field of the same checklist.

**The boolean was honest.** Eighteen readable registers, **3,862 inputs, zero incomplete.**
That is worth stating plainly rather than dressing up: the first run of this gate rejects
nothing in the book.

**The fragility is that the fourth field is spelled two ways.** Five studies write `layer`
(1,622 inputs), thirteen write `ring` (2,240), none writes both, none writes neither — and
**nothing outside a study read the field at all**; every occurrence in `scripts/` was a
fixture inside a negative control. A check written against one spelling would have silently
passed five studies and condemned thirteen, and either reading would have looked
authoritative.

**My own first measurement did exactly that** — read `layer` only and reported 58% of the
book missing a field that was there all along. The registers were complete and the reader
was ignorant. The two spellings are now named in code rather than remembered, and both are
accepted in the gate rather than renamed across the book: renaming 2,240 committed inputs
in thirteen delivered studies is a re-issue, not a passing edit.

**An absent register defers rather than duplicating.** Six studies commit no register at
all, and `source_outstanding.json` already lists exactly those six as unreadable — so the
gate reads that list instead of opening a second one, and carries no ratchet of its own.

Twelve conditions, seven red and five clean; the clean half is what it turns on — both
spellings green, and the absent-register case present twice, once deferred and once not.
Gauntlet 36/36. Stamps `2026-09-07c`.

### Also today, and it corrects an earlier line of mine

I hypothesised that ARCC's peer figures were a SIGCM clause 1 breach because their source
fields name no document. **That was wrong and the gate is right not to fire**: clause 5 puts
competitors explicitly in cross-check scope — "never a source for the subject's historicals"
— so a peer figure is not a clause 1 historical at all. The study also discloses the
weakness itself, in its own words: the peer set is two names and neither publishes an EBITDA
series it could measure a multiple from.

**Item 7 (peer history, not snapshots) was scoped and is blocked on data, not on method.**
ARCC commits one year per peer. SCEM's own audited filings are held for two years plus a
quarter; **Misr Beni Suef's own investor-relations statements page carries no documents at
all** — verified against the raw HTML, not just a rendered fetch, and not a JavaScript
problem. The EGX and EFSA disclosure portals both return `connect_rejected` at the proxy —
a policy denial, not retried. Aggregators are barred for historicals. Routes run and
recorded; this needs the filings supplied or another primary route.

## 07-09-2026 — a reader that guesses a naming convention silently finds nothing

Depth-bar standard 1 (a standalone bibliography beside every delivered study) was enforced
by `check_calibration_deliverables` over the **five calibrated names** and by a self-set
boolean over the other nineteen. **The one breach is in the nineteen:** GBCO ships a
valuation document and a workbook and no bibliography-class document at all. It predates
the bar and already sits on four other ratchets, so nothing needs fixing tonight — what was
found is that nothing was looking.

**The artefact ships under three names**, which is the part that generalises: twenty-one
studies use `Bibliography`, ELEC uses `Source_Register`, TMGH uses `Sources`, and PHAR's
file is named for the company (`EIPICO_`) rather than the ticker. A check on the obvious
convention would have condemned three compliant studies; one keyed on the ticker prefix, a
fourth. Named in code from what the book ships. `check_bibliography.py`, ratcheted at one,
10 conditions (5 red, 5 clean), artefact-conditional in the gauntlet, 37/37. Stamps
`2026-09-07d`.

### The finding that outlasts the three gates

**Five first-attempt measurements were wrong today and every one failed the same way.**

| probe | how it was wrong | what it reported |
|---|---|---|
| repo file index | excluded `.git` by substring, so it swallowed `.github` | 2 workflow files "missing" that were on disk |
| four-field audit | read `layer`, not `layer`/`ring` | "58% of inputs missing a field" — it was 0% |
| bibliography sweep | grepped `bibliograph` only | 2 breaches — there is 1 |
| (same, next step) | would have assumed a ticker prefix | would have condemned PHAR |
| `check_protocol_text` | matcher required a path prefix nobody decided on | "names nothing that does not exist" for months |

**None produced an error. Every one produced a number.** That is what makes this failure
mode survive — it is indistinguishable from a measurement, and it is the same shape as
[R-ENF-04]'s empty probe one level up: not an absent answer this time, but a *confident
wrong* one, arrived at by guessing what something is called.

The three gates written today all encode the same correction: name the variants in code,
from what the repository actually contains, never from what it ought to contain.

**Postscript, within the hour, on the gate written this morning.** `check_tree_unmodified`
keeps its baseline at a fixed path, so an aborted run leaves one behind and the next
comparison reads it as describing *this* run — reporting files staged since as "reverted".
A **missing** baseline already failed loudly; a **stale** one failed *misleadingly*, which
is worse and is the same species as everything else recorded today. Fixed by [R-ENF-06]
applied to my own gate: the baseline now declares the HEAD it was taken at, and a
comparison against a baseline from another commit refuses instead of comparing. Sixth
control case added; 10 of 10.


## 07-09-2026 (03:15 firing) — a property and its container are not the same measurement

Depth-bar standard 5 says every figure sits on a solid canvas with **"zero transparency
verified programmatically"**. Nothing verified it — `figure_discipline` is a boolean each
study sets on itself, and the other figure gate (`check_figure_axes`) runs the figure
*scripts*, not the delivered images. A script that sets a solid facecolor can still ship a
translucent PNG inside a document.

**Measured across every delivered study document: 176 embedded images, 8 translucent, all
eight in GBCO**, every one with fully transparent pixels. Every other study is opaque to the
pixel. GBCO predates the bar and already sits on five other ratchets.

**My first pass reported 160 of 176.** It read the colour *mode*: matplotlib writes an RGBA
channel that is fully opaque, so the mode says almost nothing. Twenty times the real figure,
and it would have condemned twenty-two compliant studies. Sixth instance of the same probe
error today — and the first one I caught before reporting it.

The gate deliberately does not check whether the canvas is *light*: a dark figure can be a
deliberate design and a gate cannot tell one from an accident. Opacity is arithmetic about
the file; lightness is not, and they are not bundled merely because one sentence names both.

`check_figure_opacity.py`, ratcheted at one, 9 conditions (5 red, 4 clean), artefact-
conditional, gauntlet 38/38. Stamps `2026-09-07e`. **Its own control failed first** — two
clean sandboxes omitted the ratcheted study while the ratchet still named it, so the gate
refused them and was right; the scaffolding was wrong, not the subject.

### One operational decision, taken and recorded

I have aborted the local `run_ci_gates.py` sweep four times tonight to make edits, so it has
not completed once. **CI runs the identical step list on a clean checkout on every push**,
which is strictly the better test. From here I run the affected gates and the gauntlet
locally and let CI be the full-suite authority, rather than continuing a ritual that never
finishes and cannot be honestly claimed.

## 07-09-2026 — the ratchet count was 49 and the debt is 45

**Sixteen ratchet entries pruned**, across five lists: `output` (12), `coc`, `document`,
`figaxes`, `waterfall` (1 each). Deletions only — a ratchet may only shorten. The twelve on
`output_outstanding` all appear in that gate's own **conforming** list with real reverse
reads and sign tests; they were debt paid and never pruned. STC came off two lists. The
earlier sweep missed these because it covered only the five re-issued names.

**Then the prune exposed a defect in the instrument that measures the programme's largest
open item.** `acceptance.py` walks each ratchet file recursively — the right design, since
the 44 files are heterogeneous (some list tickers, some are keyed by ticker, some by
document path). What it could not do is tell a debt list from a record of the **opposite**:
`conforming_at_adoption` names studies that were *clean* when a ratchet was seeded, and
`scope_widened.added` records what a widened gate *found*.

**Criterion 1 was reported at 49 and the genuine debt is 45** — two `conforming_at_adoption`
and two `scope_widened.added`. The verdict does not change (still NOT MET) and neither does
the escalation's decision, but the register no longer carries a figure I know to be wrong.

**It was not a tidiness point.** Pruning the output ratchet this hour removed AMOC and EGCH
from its real outstanding list **and the count did not move**, because both stayed visible
through `scope_widened.added`. An instrument that cannot see debt being paid is worse than
one that overstates by a constant.

The exclusion is **named, not pattern-matched, and conservative**: ambiguous keys (`exempt`,
`held_unregistered`, `reasons`, `aliases`) are still counted, because understating debt is
the error that matters here.

### And a correction to my own working, mid-measurement

My first pass at this reported that only 5 of AMOC's 12 lists were real debt — an
over-correction of the same kind I have been documenting all night. My classifier omitted
debt groups spelled `unscored`, `signature` and `failing`. Printing the exact key path of
every match gave 11 of 12. **I nearly reported a large correction to the programme's
headline number on the strength of a bad probe**, which is the seventh instance today and
the one that would have mattered most.

## 07-09-2026 — Part E criterion 2 measured for the first time: 11 cells outside

Criterion 2 reads: *"On the five re-issued names, forward drivers sit inside each name's own
walk-forward p10–p90 or carry a priced exception; every claimed correction reconciles to its
log."* The second half is gated. **The first half had never been measured**, and
`acceptance.py` said so in its own words — "needs a per-name driver comparison this file does
not build".

**The obstacle was not effort.** All five runs commit `forward_ranges.json`, and it has
**five incompatible shapes**:

| run | where the band lives | family |
|---|---|---|
| AMOC | `published_band[h][driver]` → `low_factor`/`high_factor` | multiplier |
| ARCC | `[driver][h]` at top level → `mult_low`/`mult_high` | multiplier |
| EGCH | `published_band[h][driver]` → `low_factor`/`high_factor` | multiplier |
| PHDC | `years[driver][h]` → `p10`/`p90` around a level | level |
| TMGH | `projection[year][driver]` → `low`/`high` around a level | level |

A single reader finds ARCC and reports the other four as having no bands at all — **which is
exactly what my first pass printed**, "0 driver-horizon bands" for four runs whose files were
full of them. Eighth instance today. `criterion2.py` therefore uses one **named adapter per
run**, the `check_correction_boundary` pattern, and a run without one is reported, never
skipped.

**The two families reduce to one question**: does the run's own band contain the run's own
forward driver? For a multiplier band that means the band contains 1.0; for a level band,
that the central lies between p10 and p90.

**Measured: 137 bands, 11 outside** — ARCC 5 (cogs, price_export ×2, price_local, raw_per_t,
all at h=4–5), EGCH 1 (cost_of_sales h=5, band 0.14–0.85 — the method over-forecast that line
every time it was scored at five years), TMGH 5 (new_sales ×3, dev_revenue, net_profit). AMOC
and PHDC are clean.

**No run commits a priced exception** in its ranges file — measured, not assumed. Whether one
is argued in prose is not something this instrument reads, and it says so rather than
reporting an absence it never looked for. So criterion 2's first half is **NOT MET**, with the
reason recorded rather than asserted.

It is a **measurement, not a gate**: pricing an exception is a judgement, and a gate would
have to define "priced" in code.

### Correction to the entry above, within the hour: the counts change what it says

I reported "137 bands, 11 outside" without the observation count behind each band. **With
the counts, the finding is much weaker than I stated:**

| run | cells outside | n behind them |
|---|---|---|
| ARCC | 5 | **3, 4, 3, 3, 3** |
| EGCH | 1 | 9 |
| TMGH | 5 | 5–8 |

**Two of the runs say in their own notes why this matters.** EGCH: "percentiles are printed
only at n ≥ 9". AMOC: on 4, 3 and 2 observations "no percentile is computed … the span and
the bias/MAE band are what the record supports."

So of the eleven, **none sits on a figure its own run calls a p10–p90**, one sits on a factor
at n=9, and ten rest on fewer than nine observations. The criterion says *p10–p90*, and only
PHDC publishes one — PHDC has zero cells outside.

Both readings are now printed and neither is chosen silently:

- **BROAD** (any published band, however thin): NOT MET — 11 cells outside.
- **STRICT** (only a figure the run itself calls a p10–p90): MET on the one run that
  publishes percentiles, and **untestable on the four that do not** — and an untestable
  criterion is UNMEASURED, never met.

Treating every exclusion as equivalent **overstates** the finding; reporting only the strict
reading **understates** it. Calling a span from three observations a p10–p90 would be the free
parameter this house forbids. My earlier message gave the broad number alone, which read as a
stronger claim about the method than the evidence supports.
