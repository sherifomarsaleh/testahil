# AIRARABIA — self-audit, 10-Aug-2026, written BEFORE reading the critiques in detail

Caveat recorded up front: one of the four critique documents (the forensic audit,
"Claude_cowork.md") was auto-loaded into the session context before this list was
written. The other three documents are unread as of this list. Findings below that
overlap the already-visible document are marked [also in cowork]; the honest claim
is therefore "not anchored on the three unread documents", not "not anchored at all".

## Defects I know are in the delivered study (found by re-examining my own build)

SA-1  **Leased-fleet additions have no liability, no rental, no cash cost.** The
      +AED 300mn/yr of leased-fleet assets (Assumptions C50) enters invested capital
      with no incremental lease liability in the bridge, no rental in the cost stack,
      and no cash outflow in FCFF. Asymmetric IFRS-16 treatment; the only charge is
      via terminal ROIC. Genuine valuation defect, direction: overstates. [also in cowork]
SA-2  **Fare and ancillary paths have no stated anchor** while every cost line has a
      named escalator — and fare is the model's largest sensitivity. The implicit
      anchor (FY2025 realised fare, Q1-2026 yield print, then ~flat real) is real but
      unstated. [also in cowork]
SA-3  **Bare 0.8 factor inside Cash Flow!B14** (booked-vs-marginal debt cost) — a
      magic number outside the input layer; and interest is charged on FY2025 gross
      debt held constant while the model's own net debt swings to positive. [also in cowork]
SA-4  **Finance income enters the net-debt roll pre-tax; finance costs after-tax** —
      asymmetric inside one formula. I noticed this while porting compute.py and
      replicated it for recalc-consistency instead of fixing it. [also in cowork]
SA-5  **JV share of profit is taxed again at 15%** inside forecast PBT (equity-method
      income arrives net of the venture's own tax). Conservative but wrong; EPS
      understated ~2-3%. [also in cowork]
SA-6  **The "weighted central" bear/bull are MIN/MAX of lens extremes**, not weighted —
      the published 0.81–7.53 range is really the DCF lens's own scenario span. [also in cowork]
SA-7  **Appendix A.1 mixes cost bases in one row** (history depreciation-inclusive,
      forecast cash) — footnoted, but the audited columns don't foot top-to-bottom. [also in cowork]
SA-8  **Appendix A.2 doesn't articulate**: four independent roll-forwards under a
      "balance sheet" heading, no assets=liabilities+equity check. [also in cowork]
SA-9  **The normalised lens capitalises JV earnings at 13×** while the study claims the
      JV framings are "never averaged" — the base central quietly carries a
      capitalised JV leg at 20% weight. Self-contradiction. [also in cowork]
SA-10 **Relative lens applies the peer multiple to EBITDA incl. other income** — the
      peers' multiples aren't computed on that base. [also in cowork]
SA-11 **The peer multiples came from an aggregator** and the justified 7.5×/13× are
      anchored on them — in tension with "cross-check only, never a build source";
      Wizz suppressed as n/m though its EBITDA was disclosed and computable. [also in cowork]
SA-12 **rf* = 4.48% − 0.42% nets a rating-model spread out of a market yield whose own
      observed spread is 4bp** — under the peg this puts the AED risk-free below the
      tenor-matched UST. House-rule mechanics applied without the peg-floor check the
      profile itself hints at ("never-UST rule governs the valuation rf"). [also in cowork]
SA-13 Minorities deducted as profit-share × equity value (method shortcut; ~AED 3mn,
      trivially small here). [also in cowork]
SA-14 **The whole equity value, including AED ~3.85bn of cash/near-cash, is rolled to
      the anchor at the cost of equity** — cash should accrete at the cash yield. [also in cowork]
SA-15 **Two different backtest coverage prints published**: §3 quotes the full-history
      windows (79%/86%), the workbook's Monte Carlo note quotes the recent/production
      windows (83%/89%), neither labelled with its window set. Same statistic, two
      answers. [also in cowork]
SA-16 **"Roughly a fifth" in the headline is wrong on both framings** (market is +36%
      above the central; the central is −26% below the market — the very next table
      says −26%). [also in cowork]
SA-17 **Feb–March airspace closures**: the company's own release says March. [also in cowork]
SA-18 **UAE GDP macro line is a stale vintage**: I used the March-2026 CBUAE QER and a
      pre-conflict IMF print; my own research agent flagged "check the next QER for
      post-conflict revisions" and I did not. [also in cowork]
SA-19 **Group fleet paired with consolidated passengers**: the 90 aircraft / 219
      destinations are group-wide incl. the JV hubs; the consolidated (Sharjah+RAK)
      fleet is materially smaller, and §1.6's "90 → ~115" justification for the
      consolidated pax path conflates the two. [also in cowork]
SA-20 **The JV sensitivity row isn't centred on the base** — base (363) sits in the
      leftmost column while the caption says the middle column is the base. [also in cowork]
SA-21 **§2 levels are printed without their derivation rule** (they ARE computed —
      recency-weighted pivot clusters over the cleaned series — but the document
      doesn't say so, so they read as assertions). [also in cowork]
SA-22 **DCF bear/bull driver vectors are unpublished** — the two numbers that set the
      whole headline range are the only whole-model re-runs whose inputs appear
      nowhere. [also in cowork]
SA-23 **Expert tables omit the anchor-roll line** (E1: 0.325 × 13 ≠ 4.15 as printed);
      Expert 2's construction (half-cash haircut) is ad hoc and doesn't reconcile on
      the panel's shared convention. [also in cowork]
SA-24 **11.60% FY2025 effective tax** is note 27's tax-for-the-year basis (212.444);
      the income-statement charge (202.054, after a prior-period credit) gives 11.0%.
      Both true; the study quotes one and prints the other without reconciling. [also in cowork]
SA-25 **Company-overview revenue mix is wrong**: "79%" is the pax line alone though the
      sentence says fares plus baggage (80.3%); "11% ancillary/cargo/services" is
      ancillary alone; the printed decomposition doesn't sum to 100%. [also in cowork]
SA-26 **"Four consecutive 5-fil raises"**: FY2021's dividend was not 25-minus-… I never
      verified the FY2021 base; only three of the four steps are 5 fils. [also in cowork]
SA-27 Sharjah 19.5mn vs the authority's own "over 19.4" (19.48mn) — rounded past the
      source. [also in cowork]
SA-28 **Workbook ships without cached formula values** (openpyxl) — Excel recalculates
      on open, but some viewers show blanks/zeros until then. Delivery nit.
SA-29 **Q1-2026 reviewer attribution ("Grant Thornton UAE") was never verified** against
      the interim's signature page — I carried it from a secondary impression. Must be
      verified or removed. [cowork flags it UNVERIFIABLE]
SA-30 **Peer basis labels are sloppy**: "09-Aug-2026" is a Sunday (the pull date, not a
      close); Ryanair/easyJet are fiscal-year figures labelled "trailing"; Pegasus's
      "TRY statutory" caution was carried from the research agent unverified. [also in cowork]
SA-31 **Lens weights are asserted** with a one-line rationale. [also in cowork]
SA-32 **Share basis (basic; no dilutives) never stated**; and the FY2025 auditor's
      "purchased shares during the year" item (note 1) was noticed, logged in the
      research trail, and never resolved. [also in cowork]

## Things I checked again and believe are RIGHT (receipts held)

SR-1  The 17 leased-out aircraft: FY2025 filing, note 34, verbatim: "the Group has
      leased out 17 aircrafts (2024: 18) under non-cancellable operating lease
      agreements to related parties." (The audit marks this unverifiable — its OCR
      failed; mine did not.)
SR-2  The balance-sheet inputs (net cash 2,417.297, non-op 1,069.284, JV book 363.386,
      fleet 8,670.864, WC −5,186.8): all from the FY2025 filing's note 43 restated
      three-column statement of financial position, which HAS a text layer in the
      PDF I hold. Verifiable line by line.
SR-3  The engine arithmetic (WACC, glide, waterfall, terminal, bridge, lenses,
      sensitivity cells) — reproduced independently to six decimals by the audit
      itself; recalc.py 644/644.
SR-4  Beta's internal statistics cohere (t=13.08 ⇒ R²=0.40; CI = 0.949–1.223).

## What a failed self-audit would have looked like
Finding nothing. This one finds one valuation-plane defect (SA-1), one rate-plane
defect (SA-12), two self-contradictions (SA-9, SA-15/16), and a long tail of input
and narrative slips.
