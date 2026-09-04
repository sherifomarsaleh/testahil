# ELEC — the reason recorded for the source breach is wrong, and the breach stands anyway

**04-Sep-2026 · internal · this study is HELD and nothing here reaches the live site**

`scripts/check_source_integrity.py` reports ELEC as the one study in the book in
plain breach: **11 dated historicals sourced outside the filings.** The study says
why, in its own research note, first paragraph:

> "The research environment's egress proxy blocked direct page fetches of EGX,
> Mubasher, Zawya, Arab Finance, stockanalysis.com, simplywall.st, Investing.com,
> TradingView, WSJ and the company website (ececables.com)."

That sentence has been the study's standing justification since 05-Aug-2026. It was
re-run today, in full, because **[R-ENF-04] says a probe whose failure is relied on
is re-run — an empty result is first evidence the probe did not run.**

## What the re-run found

| Route | Result today |
|---|---|
| `https://www.ececables.com/` | **HTTP 200.** Reachable. |
| `…/financial-statements-2/` | **HTTP 200.** An index of ~60 audited statements, one click from the homepage. |
| `…/investor-relations/`, `…/shareholder-structure/`, `…/affiliate-investments/` | **HTTP 200** |
| WordPress media API, `/wp-json/wp/v2/media` | **HTTP 200**, 86 PDFs enumerated with their canonical URLs |
| Every statement PDF (FY2023, FY2024, Q1/H1/9M-2025) | **HTTP 404** |
| A non-Arabic PDF in the same tree (`ECE-Company-Profile-2025…`) | **HTTP 404** — so it is not a character-encoding problem |
| A 2020-vintage asset in the same tree (`favicon.png`) | **HTTP 200** — so the host serves that path |
| Legacy host `ece.allmediaegypt.com` (carries the 2015-2020 statements) | **DNS does not resolve.** Dead. |
| `www.egx.com.eg`, `disclosure.egx.com.eg`, `mist.com.eg` | tunnel closed mid-exchange, repeatably, on nine attempts. Reported, not routed around. |
| Every live ref of this repository (22) | no ELEC filing on any of them |

**The company's website is reachable. The company's website does not serve its own
financial statements.** Everything uploaded after August 2020 returns 404 while the
index goes on listing it, and the host that held the older ones no longer exists.

## Why the correction matters even though the answer does not change

The documents are still unobtainable, so **SIGCM clause 1 still binds and this study
is still not deliverable on its own sources.** What changes is the reason, and the
reason is the part a future session acts on:

* *"the proxy blocked the company website"* is a fact about **our environment**, and
  the honest response to it is to try again later — which is what the study implicitly
  assumed and what nobody did for a month.
* *"the company lists its statements and serves none of them"* is a fact about **the
  world**, and the honest response is to stop trying that route and ask for the
  documents, which is what has now been registered.

The SCEM precedent, which this repository already carries, is the opposite case and is
worth naming beside it: there the statements *were* on the company's own website, six
PDFs one click from the homepage, and the study used Global Cement and an aggregator's
carry of S&P Global anyway. **The two cases share the failure and not the fact.** In
both, a sourcing claim was written once and never re-tested; in one the documents were
there all along and in the other they never were, and no amount of care inside either
study could tell which without running the probe again.

## What the study's own numbers say, and what they cannot say

The measurements below use only ELEC's committed numbers file. They are recorded because
they price the defects, not because they repair the study — every input underneath them
is vendor-sourced and therefore cannot carry a delivered figure.

**The published answer.** Enterprise value EGP 3,813mn against net debt of 9,805mn,
so equity is **−5,992mn**, floored to zero, published as EGP 0.01 per share against a
traded 2.19. The market pays EGP 7,257mn for the equity, i.e. an enterprise value of
**17,062mn: the model's enterprise value is 22% of the one the market pays.**

**The terminal carries the retired construction.** `tv = NOPAT(1+g)(1−g/ROIC)/(W−g)`
— the g×IC form [R-TERM-01] retired outright — with a terminal return on capital of
**9.17% against a terminal cost of capital of 15.00%, 583bp below it**, and a
reinvestment rate of **54.5% of terminal profit committed to that destroying spread in
perpetuity.** It is ARCC's defect exactly. The model's own console output says so in
as many words — *"spread NEGATIVE: growth subtracts value; the g-grid gradient inverts
by construction"* — and the study shipped.

**And correcting it does not rescue the answer, which is the finding.** Holding the
explicit window and the discount factor and moving only the terminal:

| Terminal construction | Enterprise value | Equity | Per share |
|---|---:|---:|---:|
| As published (g×IC charged, rr = 0.545) | 3,813 | −5,992 | −1.81 |
| NOPAT perpetuity at book depreciation (the labelled floor) | 5,049 | −4,756 | −1.44 |
| Growth kept and **no reinvestment charged at all** — not a legitimate construction, shown as a bound | 7,552 | −2,253 | −0.68 |

Even the bound that charges nothing for growth leaves the equity negative. **On the most
extreme name in the book the terminal correction accounts for at most a third of the gap
and the answer stays absurd** — which is [R-TERM-01 CLAUSE TWO CORRECTED]'s own rule
working in the direction nobody wants: the size is measured per name and never predicted.

**The terminal growth rate is a real decline nothing states.** `g_term` = 5.0% nominal
against the house EG terminal inflation of 7.0% is **−1.87% real**, in perpetuity, with
no sentence anywhere saying so. It is the third name found carrying that exact figure
today, after PHAR and SWDY, and the census that found the other two could not see this
one — ELEC's numbers file carries no `meta` block, so its market resolves to nothing and
it lands in the unreadable bucket. **The worst instance of the thing being measured was
invisible to the instrument measuring it.**

**Terminal invested capital is a typed constant.** `compute.py:370` reads

    ic_T = rows[-1]['nwc'] + 0.05 * rows[-1]['rev']       # invested capital ~ NWC + light PP&E

The 0.05 is chosen by this desk, sourced nowhere, and it sets the terminal return, hence
the reinvestment rate, hence 82% of enterprise value. ELEC manufactures cable on a
370,000 m² site; 5% of revenue is not a description of that company. The direction is
one-way and the constant sits at the optimistic end:

| PP&E as % of revenue | Invested capital | Terminal ROIC | Reinvestment rate |
|---:|---:|---:|---:|
| 5% *(as published)* | 16,325 | 9.17% | 0.545 |
| 15% | 18,081 | 8.28% | 0.604 |
| 30% | 20,714 | 7.23% | 0.692 |
| 40% | 22,469 | 6.66% | 0.750 |

Working capital dominates it either way — 15,447 against revenue of 17,554, **88% of
revenue** — which is itself a figure no filing in this repository supports.

**The reverse read the study never published.** Under its own construction the traded
price implies a terminal NOPAT of **7,858 against the study's 1,497 — 5.25×** — or a
terminal return on capital of **26.9% against the study's 9.2%.** On ARCC the same
question was settled by opening the filed accounts and reading returns on book capital
of 43.9%, 44.3% and 60.6%. **Here that instrument does not exist, and its absence is the
whole finding: the check that caught the identical defect on another name cannot be run
on this one, for the same reason the study should never have issued.**

## Disposition

This study is **HELD** under [R-GAP-02] and stays held. Nothing here changes a delivered
figure, because changing one would mean building further on the vendor base rather than
replacing it. The primary documents are registered as escalation `ELEC-primary-financial-statements`
with the routes above and a default that fires on 2026-10-04: **if the filings have not
arrived by then, ELEC is withdrawn from coverage rather than re-issued on aggregator
data** — a study nobody can source is not a study with a wide range, it is not a study.

## A measurement attempted and abandoned, recorded because it would have looked like evidence

L-299 says the unreadable bucket is where the worst cases go. That is a testable claim,
and the obvious cheap test is to count how many ratchets each study sits on and compare
the four studies with no `meta` block against the rest. It was run. **It gives 8.5
against 6.6, it points the right way, and it is not evidence, so it is not quoted.**

Two reasons, and the second is the one that matters:

* **The harvest was wrong in both directions.** It counted studies listed as
  *conforming at adoption* as though they were outstanding, and it missed real entries
  — ADNOCLS greps into three ratchet files and the harvest scored it zero. Either error
  alone would move the comparison.
* **The ratchet count is an AGE measure wearing a severity label.** A ratchet lists work
  that predates a standard, so a study accumulates entries by being old and sheds them
  by being rebuilt. SCEM sits on one entry while in plain breach of SIGCM clause 1;
  ADNOCLS, the exemplar, was outstanding on eight ratchets this morning and is the
  document every other study is modelled on. The number measures conformance work done,
  not defects present.

This is [L-289] again — a ratio between two quantities defined differently is not
evidence about either — arriving one day later in a different costume, and it computed
cleanly and sorted the book plausibly both times. **L-299's evidence is therefore the
ELEC case alone**: a single decisive instance, where the worst terminal in the book was
invisible to the census built to find exactly that defect. One instance is not a rate,
and the register says so rather than borrowing a number that would have made it look
like one.
