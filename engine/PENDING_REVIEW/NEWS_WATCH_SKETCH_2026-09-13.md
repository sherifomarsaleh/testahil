# News watch layer — design sketch

**Status: PROPOSAL, NOT ADOPTED.** Nothing here is a standing rule. No rule is amended by this
file; adoption of any of it goes through the protocol scribe in both governing documents, in one
commit, as usual. Written 13-Sep-2026 in answer to "is there a way to scan news every day and
adjust possible price movement based on news".

## 1. What it is, and what it is not

It is a **dated what-if marker on the existing sensitivity rail** — the panel already shipped on
every study page, the one whose own caption reads "not a re-run DCF, and it never touches the
Monte Carlo section below".

It is **not a fourth lens**. It produces no forecast, no drift, no width, no fair value. It reads
the study's published outputs and feeds nothing back, which is the same standing `fv_overlay`
already has. That is the whole reason it can exist at all:

- [R-LENS-01] bars any lens output from being an input to another, and bars MC direction from
  coming from anything but a price-native signal fitted in the engine's own signal socket. News
  is not price-native. So news can never reach the cone. Displaying a what-if beside the study is
  not feeding it.
- [R-LENS-01] also extends to calibration records. A news record is not an input to anything.

The rejected alternative, for the record: a "Bayesian update of discrete event probabilities" has
nothing in this repo to attach to. `engine/mc_v3.py` carries no jump term, no factor array and no
discrete-event machinery — it is a Student-t diffusion with a per-market (nu, width_cal) and one
signal socket. There is no 16-factor engine and there are no 9 event buckets to update.

## 2. Prerequisite — lift the levers out of the page HTML

Today each study page carries its own lever array inline (`SAVOLA/study/index.html:256`), passed
straight to `renderFairLevers(elId, T, levers)` in `assets/app.js:1154`. Each lever is:

    { name, min, max, step, def, impact, lo, hi, fmt }

`fmt` is an arrow function returning the study's own prose for that position, so the array is not
pure JSON.

**Move it to data, not prose.** A `levers` key on the TICKERS record (data.js is JavaScript, so
`fmt` survives as a function), or `assets/levers/{TICKER}.js`. The page then calls:

    renderFairLevers("fl-lever-card", T, T.levers);

Two reasons this comes first:

1. Otherwise a daily job is rewriting published study pages every day. Pages are generated
   artefacts under the publish protocol; a robot editing them daily is the wrong blast radius.
2. `def` and `impact` are study constants. Once they are in data, a gate can assert they are
   unchanged — which is what stops the news layer drifting into the study.

**Gate to add** (`page-integrity.yml` already exists and is the right home): every study page with
a lever card resolves a lever array, and every `def`/`impact` matches the study's committed value.
Red, not warn.

## 3. The daily job

`.github/workflows/news-watch.yml`, one run a day, plus `engine/news_watch.py`:

**a. Fetch.** Per covered name, in SIGCM order — the company's own IR/disclosure channel first
(EGX, Tadawul, ADX, DFM, QSE, NSE, KRX, SEC as applicable), then wires. Reuse
`research_sweep.py`'s provenance fields rather than inventing a second provenance vocabulary.
Attempted-and-failed is logged either way, as in the sweep.

**b. Classify — deliberately narrow.** Two questions per item, and only two:

1. Does it name one of **this study's** levers? The lever list is closed per name. SAVOLA has
   exactly four: Panda density, store cadence, terminal growth, terminal ROIC.
2. Does it carry a **number**?

Everything else is logged and dropped. No sentiment score, no free-text impact estimate, no
"unmodelled tail shock" bucket — a classifier allowed to invent a factor is a classifier that
will. If a real event has no lever (a rights issue, a CEO exit, a regulatory ban), the correct
output is a **flag for a human**, not a slider position.

**c. Map.** item -> lever index + proposed slider position + the quote and number that justify it.
The mapping is arithmetic where it can be: "9 net new stores to end-August" is a cadence position,
not an opinion.

**d. Write.** Append to `engine/news_watch/{TICKER}.json`. Nothing else is written.

## 4. The ledger (append-only)

    {
      "ts": "2026-09-13T06:00:00Z",
      "ticker": "SAVOLA",
      "lever": 1,
      "lever_name": "Panda store cadence (net new stores a year)",
      "source_url": "https://...",
      "source_type": "company_ir",
      "published": "2026-09-11",
      "extracted": "9 net new stores opened to end-August 2026",
      "prior_pos": 20,
      "proposed_pos": 8,
      "base_fv": 27.20,
      "implied_fv": 19.53,
      "at_grid_edge": true,
      "confirmed": true,
      "half_life_days": null,
      "expires": null
    }

- `confirmed: true` only for the company's own disclosure. A wire-only item carries a half-life
  (3-5 trading days is a sensible default) and decays back to `def` if no filing follows. This is
  the one idea worth keeping from the outside answer, and it matters: unconfirmed narrative
  mean-reverts fast, and a marker that does not expire becomes a permanent unaudited claim.
- Append-only. A correction is a new row, never an edit. Same discipline as the band record.
- Nothing is ever deleted, so the layer can be graded later (section 6).

## 5. What the page shows

- A second, **muted** marker on the same rail: "news-implied 19.53 — 13-Sep", with the source link.
- The base-case diamond **stays exactly where the study put it**. The published fair value on the
  page does not change.
- The marker is display-only. It does not move the sliders, and "Reset to base case" is unchanged.
- If `at_grid_edge` is true, it is labelled as such — see below.

## 6. Standing limits (the part that is not negotiable)

1. **Never** touches MC drift, width, nu, the signal socket, the touch ladder or the band record
   [R-LENS-01].
2. **Never** writes `fair{bear,base,full}` in `data.js`. That number moves only in a study rebuild,
   and `fv_movement.py snapshot` exists precisely to catch a fair value that moved without one.
3. **Never** writes `def` or `impact`. `impact` is sized from the study's *published variants*, so
   the rail is only honest inside the grid the study actually re-ran. A position at `min` or `max`
   is the edge of the evidence, not a valuation — hence `at_grid_edge`, shown to the reader.
4. **Never** a rating or a price target. Ranges and distributions only, as everywhere else.
5. The news layer is not a study input. Nothing it writes may be cited in a study, a sweep register
   or a lessons entry — those need primary sources under SIGCM, which the ledger's `source_url` is
   not a substitute for.

## 7. Calibration — because it is a claim

Every news-implied marker is a dated, frozen claim, so it gets graded like one. When the driver
realises (the H2 store count prints, the density number lands), score whether the news-implied
position was closer to the realised driver than the study's `def` was. That is a small register of
the same species as the three the system already carries — and note there are three, so any
document describing this must say *which* walk-forward it means.

Until that register has a record, the marker ships **labelled uncalibrated**. And if the layer were
ever to move a number rather than display one, it clears the promotion rule first, on out-of-sample
evidence — the same bar that stopped the free parameter in the band record.

## 8. Build order

| Step | What | Output | Risk |
|---|---|---|---|
| 1 | Lift levers into data + page-integrity assert | Mechanical refactor, gated | Low; useful on its own |
| 2 | `news_watch.py` + ledger, SAVOLA only, run by hand for two weeks | Ledger file. Nothing on the site | None — writes no published surface |
| 3 | Read the ledger. Did it catch anything a human reading IR wouldn't have? | A verdict | — |
| 4 | Only then: the page marker, labelled uncalibrated | Site change, publish protocol applies | Real; gated |

**Step 3 can legitimately end the project.** If two weeks of scanning produces nothing that the
existing sweep wouldn't have caught on the next update, that is a finding, and the honest response
is to stop at step 1 and keep the lever refactor.
