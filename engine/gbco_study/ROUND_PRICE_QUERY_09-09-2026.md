# GBCO — the upper branch rests on a number GB Corp has never published

**09-09-2026 · internal · nothing here reaches the live site · no fair value moved**

## The contradiction, in this study's own file

| line | what it says |
|---|---|
| `compute.py:88` | `("MNT-Halan second closing ≥ $1.4bn", 0.45, 0.015)` — a **45%-likely FUTURE event** in the study's own discrete-scenario list |
| `compute.py:459` | `mnt_halan_round_usd = 1400.0` — the same number as a **completed round price**, feeding the upper branch |

One model treats one number as both a probability-weighted future event and a realised
fact. Nothing in the study reconciles the two.

## What the company has actually filed

The study's evidence field says, in capitals: **"BOTH ENDS ARE THE COMPANY'S OWN
DISCLOSURES AND NEITHER IS THIS DESK'S"** (`compute.py:876`). The low end is note 34 to
the 30-June-2026 reviewed statements and that half is true. The high end is not.

- **The 9 June 2026 press release the study cites is NOT IN THIS REPOSITORY.** There is no
  press release, no `PRL`, no MNT document anywhere under `engine/gbco_study/`. The number
  carrying the entire upper branch cites a document this desk does not hold.
- **Searched every dollar valuation in the annual reports this study DOES hold.** AR2022
  carries `USD 800 million` — the 2022 transaction, "sold a share by 7.5% in the MNT BV
  group ... accordingly it lost control ... after that the company re-evaluate the
  remaining shares at fair value". AR2025's two `USD 1.7 billion` figures are **MNT-Halan's
  LOAN BOOK at 31 December 2025** and a lifetime disbursement total — neither is a
  valuation of the company.
- **So the only MNT valuation GB Corp has ever filed, in the documents held here, is USD
  800 million.** USD 1.4bn is neither that nor anything else on the record.

## Why this is not a small labelling point

The two branches are 41.3484 (associate at reviewed carrying value) and 52.3453 (associate
at the round price). **The gap between them, EGP 11.00 a share, is the whole of what the
round price buys**, and it rests on a figure that:

* the repository cannot show,
* the annual reports contradict at the only comparable point, and
* the study's own scenario list rates at 45% likely and not yet happened.

## What has NOT been done, and why it is recorded rather than acted on tonight

The number has not been changed and the branch has not been retired. Both are real
options and they are different studies:

* **Retire the upper branch** — GBCO becomes single-sided at the carrying value, and the
  published answer stops depending on an unpublished number.
* **Re-base it on the filed USD 800 million** — keeps a two-sided answer on a disclosed
  figure, at the cost of anchoring a 2026 branch to a 2022 transaction, which is its own
  defect.

Neither is a judgement to make at speed on the largest single line in the file, and
[R-GAP-04] requires the search to be recorded with what each candidate is worth. It is
recorded. **What would settle it: an EGX or FRA disclosure, or an MNT primary document,
stating a USD 1.4bn valuation on or about 9 June 2026 — and if one exists it belongs in
`engine/gbco_study/src/` where every other source in this study sits.**

## Found only because the answer was challenged

No gate caught any of this. Every gate in this repository reads the committed
`study_numbers.json`, and that file was correct-by-construction for the numbers it held.
The finding required reading what the study CLAIMS about its sources against what the
sources say — which is [R-GAP-04](3), and it is why that clause is in the rule.
