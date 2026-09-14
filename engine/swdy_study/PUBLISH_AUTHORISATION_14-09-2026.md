# SWDY — PUBLISH AUTHORISATION

AUTHORISED BY: Testahil.com
AUTHORISED AT GAP: -35.4%

Date: 14-09-2026

## What is authorised

Publication of the SWDY study at a central of **EGP 87.94** against a last known
price of **EGP 136.20** (2026-09-06) — a gap of **-35.4%**, past the 10%
publication limit that [R-GAP-02] holds a study at.

This authorisation covers the gap only. It does not waive any other gate, and it
does not authorise a number other than the one above.

## What it rests on

- `MARKET_DISSENT_14-09-2026.md` — the case, argued at the same -35.4%. Its
  mechanism is that the whole gap is the reinvestment charge; its reverse read
  narrows the disagreement to one driver, whether the FY2023-24 segment EBITDA
  margin returns; its falsifier is a FY2026 full-year segment EBITDA margin at or
  above 12.63% while capex continues.
- Phase 1 acceptance, proven for SWDY on all six criteria per [R-GAP-02 CLAUSE
  FIVE], which resolves acceptance per name rather than book-wide.
- An adversarial audit that hunted our own defect first and priced twenty-three
  candidates in both directions. Taking every upward correction and none of the
  downward ones gives 110.88 — still -18.6% below the price. The defensible
  central is EGP 83-90.

## Recorded against the study, not hidden from it

Three record defects are disclosed in the dissent and none of them moves the
central: `etr_h1_25` carries H1-2026's rate under an H1-2025 key, and on the true
figure the study's own like-for-like method gives a tax rate of 34.03% rather
than the adopted 24.5% — which runs AGAINST this number; the terminal risk-free
note is stale and now asserts the opposite of the truth; and `rebuild_ledger.json`
names its own unrecorded +102% stretch.

Also recorded: the largest single driver of the move from the prior published
69.73 to 87.94 was a house-wide change to the real-rate convention on 10-Sep-2026
(commit `67b9b9652`), worth +21.33 per share. That is a change to the house path,
not a discovery about SWDY.

## Standing

The gap tolerance is 3.0 percentage points [R-GAP-02 CLAUSE FOUR]. This
authorisation goes stale with the case it approves: if the gap moves more than
3.0pp from -35.4%, both this file and the dissent must be re-argued before the
study publishes again.
