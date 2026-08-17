# DU — response to four external critiques, 17-Aug-2026

Critiques: `Claude_code.docx` (29 findings) · `Claude_cowork.md` (23) · `Gemini_think.docx` (5) ·
`Gemini_research.docx` (4). **61 raised, 61 answered, 0 unaddressed.** Plus 7 defects found by
self-audit that no critique raised.

**Nothing in this document is implemented.** `study_numbers.json` is at base (DCF 18.7444 /
central 14.7674, byte-identical to the committed build); recalc 729/729, driver test 22/22,
SIGCM + model-study bar, and the document QC scrub all still pass. The only code change is an
inert `DU_OVERRIDE` hook in `compute.py` used to PRICE findings on the real chain rather than on
a re-implementation; with the variable unset it is a no-op, proven by re-running every gate.

## Headline

The DCF arithmetic is intact — three critiques rebuilt it independently and all reproduced
18.744 to the fils. What broke was the inputs at its edges, plus one research failure.

| | central | vs spot 12.30 |
|---|---|---|
| As published | 14.77 | +20.1% |
| All 7 accepted corrections | **13.79** | **+12.1%** |
| + the no-arbitrage rf floor (decision D1) | 13.15 | +6.9% |

## The seven accepted value-moving corrections

| # | Correction | Δ central |
|---|---|---|
| 1 | Justified P/E 15.5 → 12.9 (re-derived from issuer filings) | −0.84 |
| 2 | Interim AED 0.26 stripped from every lens (ex-date 31-Jul-2026) | −0.26 |
| 3 | Staff FY26E 985 → 1,035.2 (true H2/H1 seasonal ratio 1.196, not 1.09) | −0.12 |
| 4 | Lease-replacement charge dropped (leases-as-debt) | +0.24 |
| 5 | Beta grid re-run on the netted basis | 0.00 (grid +0.90…+2.61/sh) |
| 6 | Book-lens bear on a single g | 0.00 (bear 9.60 → 10.47) |
| 7 | Framing B on its own reinvestment rate | 0.00 (B 15.95 → 15.82) |

Corrected beta grid: [23.05, 18.84, 16.02, 15.49, 13.27] — base cell now equals the headline
DCF exactly (the published grid's base cell contradicted it by AED 1.77).

## The two escalations (>5% of central → full primary re-derivation)

### 1. The justified multiple — 15.5x does not exist at the anchor
Re-derived from issuer filings at the 6-Aug-2026 anchor:

| Company | Price | TTM EPS | P/E | Yield | Grade |
|---|---|---|---|---|---|
| Mobily (7020) | SAR 61.30 | 4.76 | **12.88–12.93x** | 4.89% | primary, both routes tie |
| e& (EAND) | AED 20.98 | 1.33 | **15.7–15.8x** | 4.50% | primary, reported attributable |
| stc (7010) | SAR 43.38 | 2.94 | 14.75x | 5.07% | aggregator, TTM legs unsourced |
| Ooredoo | QAR 13.04 (17-Aug) | 1.18 | 11.19x | 5.70% | aggregator, off-anchor |
| Omantel | unsourced | 0.123 | 11.96x | 6.66% | aggregator, internally contradictory |
| Zain | KD 0.611 | unsourced | **refused** (provider returned 11365x) | 6.70% | unusable |

Mobily 12.89x is confirmed two ways (per-share 61.30/4.76; market-cap 47,048/3,650). My 15.5x
was a **January-2026 aggregator read on FY2024 earnings**, published as an "08/09-Aug-2026
aggregator read" — a staleness AND dating error, and my own sweep trail records it as such. A
stale FY2024 EPS of 4.03 reproduces 15.21x, which is what the rival "14.0–15.6x aggregator"
band was carrying.

**Only two of six peers survive as clean observations, so a "peer median" is not supportable at
all.** Drop the median language; defend Mobily as the single closest structural analogue at
12.89x. The 5-name median coincidentally also lands on 12.89x, but that is NOT independent
corroboration: Omantel's provider P/E and yield are mutually contradictory, Zain's is corrupt,
and Omantel holds ~21.9% of Zain, so they are not independent observations in any median.

Two forward traps to carry: e&'s EPS is basis-sensitive (its own H1-2026 release quotes the
H1-2025 comparative as *adjusted* 0.67, which fabricates a 12.56x); and e&'s Vodafone disposal
(AED 21.9bn proceeds, 4.8bn gain) completed in Q3-2026, so its reported TTM EPS inflates and
its apparent P/E falls from Q3 onward. Also: `raw_ohlc/AE/EAND.csv` ends 24-Jul-2026 and
`SA/STC.csv` 26-Jul-2026, and there is no Mobily file — the house library could not corroborate
any peer price.

Consequence for framing: on corrected figures du at 18–19x trailing sits **above every Gulf
peer**, not "above the bracket's middle, below the top names" as §1.3 says.

### 2. The contested judgement was never contested — my failure
**du disclosed the royalty extension itself on 24 July 2026**: "Extension of Federal Royalty
Scheme for the Period 2027–2029", du-branded, covering 1-Jan-2027 to 31-Dec-2029, floor
expressly retained — *"The aggregate annual amount of Federal Royalty and Corporate Tax payable
by the Company shall not be lower than AED 1.8 billion."* That is **sixteen days before my
09-Aug sweep date**. The study states du had not yet disclosed it and logs a dated negative
search to that effect. **That negative search is false.** The base value does not move (Framing
A was always the base), but the study's spine does: the contested judgement the report is built
around, headlines, and uses to satisfy depth-bar item 8 was already settled in du's own filings.
Framing B is a post-2029 tail, not a live 50/50.

Separately confirmed: the interim dividend timetable from du's own DFM filing (Ref RME/14/2026)
— **ex-date 31-Jul-2026**, record 3-Aug, payment 21-Aug. DU had traded ex for six sessions
before the anchor, so "stays in the share" is wrong on every lens.

Also confirmed: the TDRA licence renewal (12-Aug-2026, 20 years, effective 9-Aug-2026)
POST-dates the study — that dated negative search was honest. But the announcement is **silent
on fee and revenue-share terms**, so "renewal on comparable terms" must be reclassified from an
assumption presented as near-fact to an open item.

## Contradictions between critiques, arbitrated by coherence test

1. **Lease treatment** — two say double-count, one calls it "institutionally rigorous". The two
   win: terminal invested capital already includes the ROU asset and terminal reinvestment
   maintains it, so perpetual renewal IS charged in the terminal; charging replacement in the
   explicit window as well double-bills ~1,450 of PV. Worth +0.24 (value UP).
2. **Sovereign netting** — one praises it, three attack it. Both partly right: the netting
   PRINCIPLE is correct (failing to net inflates Ke to 6.86%), but rf* 4.06% sits ~26bp below
   the matched-tenor UST, which a hard peg cannot support. Note the whole controversy spans only
   9bp of Ke (6.44% rating / 6.50% at 25bp / 6.53% at 4bp) — which is what the same-basis rule
   exists to deliver. The 11.7% swing one critique reports comes entirely from breaking it.
3. **Mobily's multiple** — 12.9x vs "14.0–15.6x". Primary filings settle it at 12.88x.
4. **FY2026 guidance** — one says 5–7% with no cut, one says the cut is real. du's own Q2-2026
   deck, slide 16: **"Revenue growth 4% – 6%"** under "Guidance confirmed for EBITDA margin and
   slightly adjusted for revenue growth". The study is right.

## Findings rejected with receipts

Guidance cut denial (du's slide 16) · Note 38 unverifiable (AR2025 p.166 prints "38 Segment
analysis" and the Gross Margin definition verbatim) · Mobily 14–15.6x (stale FY2024 EPS) ·
"20.7 is e&'s share price mistranscribed" (3–7 Aug closes were 20.30/21.00/21.00/20.98/20.50 —
no session printed 20.70, two providers agreeing to the fil; my own trail records 20.7 as a
*normalized* P/E, so the defect is a basis mislabel) · "longest AED tenor is worth −1.01/share"
(the actual Feb-2033 print at 3.779% moves value **+12.8%**; the 4.48% choice is conservative) ·
"Table 8's shown inputs don't give shown outputs" (same-basis is correct; the row fails to SHOW
the second change) · 682k re-dated to FY2023 (unproven; my series has Q4-2024=682 and the deck
confirms Q2-2025=706) · "a point estimate is a price target" (the house standard mandates a
summary table with a weighted central, published beside bear/bull and four lens reads) ·
"Framing B variance is floating point" (it is structural — B inherited A's reinvestment rate) ·
"CRITICAL FAILURES: NONE DETECTED / CLEARED AS SUBMITTED" (it cleared a beta grid contradicting
its own headline by 1.77, a false median label, a 7-month-stale multiple and an ex-dividend
error) · "terminal reinvestment too aggressive" (terminal RR 9.45% EXCEEDS explicit-window net
reinvestment of 6.33%; terminal implied capex 2,937 vs FY2030E actual 2,860 — no capex cliff).

## Seven defects no critique raised (self-audit)

1. **Implied terminal exit multiple of 10.24x vs du's own trailing 7.56x — a +36% re-rating.**
   Pricing the terminal at du's own current multiple gives a central of 12.85 (−13.0%). Larger
   than any finding any critique raised; all four said "85% TV is risky", none converted it into
   an exit multiple. Recommend disclosing as a cross-check, not re-basing.
2. **30 financial numerals typed into `build_xlsx_du.py`** — the QC evidence for depth-bar item 3
   ("every builder reads the committed numbers file exclusively, no financial numeral typed into
   a builder") is FALSE as written. This is the ROOT CAUSE of six critique findings: the peer
   block escaped both the traceability gate and the date discipline.
3. Framing B inherits Framing A's reinvestment rate (ROIC_B 22.87% → RR_B 10.93% vs 9.37%
   applied) — B overstated by 0.24.
4. The AED 0.511 investees carrying value is not in the four-field register and `assoc_val` is
   dead nonsense code — the four-field completeness assertion passed vacuously.
5. Expert 3's high bound is described as "the rate-tenor bull" but is actually base × 1.12.
6. Staff-cost note claims the H2-2025 seasonal ratio but uses 1.09 against a true 1.196.
7. Dead code (`if False`, `if True else`) shipped in the delivered builders.

## Decision branches, priced

| Branch | central | Recommendation |
|---|---|---|
| A (the 7 accepted) | 13.79 | implement |
| D1 rf* floored at matched-tenor UST 4.32% | 13.15 | **take it** — closes the only real no-arbitrage hole |
| D2 switch to the 4bp market-spread basis | 13.54 | publish as priced alternative, keep rating basis primary |
| D3 mid-year discounting | 14.81 (+0.04) | disclose the convention, keep year-end |
| D4 disclose the implied exit multiple | base unchanged; cross-check reads 12.85 at 7.56x | **take it** |
| D5 collapse relative+normalised into one 45% lens | 0.00 | collapse and relabel |

## Standing-rule consequences

- **Peer multiples and every market-data comparable must enter the four-field register**, dated,
  with the basis (trailing/normalised/adjusted) stated — never typed into a builder. The
  numeric-traceability gate must assert on builder source text, not just on the register.
- **A dated negative search must be re-run against the issuer's own disclosure feed** before it
  is published as a negative result. Mine was 16 days stale on the single most important item.
- **Fair-value roll must net every dividend whose EX-date falls in the window**, not every
  dividend PAID in the window.
- **A single-driver sensitivity grid must return the base case at the base parameter**, asserted
  in code.
