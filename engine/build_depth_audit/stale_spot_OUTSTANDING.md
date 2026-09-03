# Studies published against a price older than the latest known one

**03-Sep-2026.** [R-GAP-01 AMENDED] says no study is delivered against a stale price: the
central is put against the LATEST KNOWN price before any delivery, and the spot the study
publishes is that same latest price with its date beside it.

`scripts/check_valuation_gap.py` deliberately audits each study against **its own strike
price**, which remains the honest test of whether the answer was audited before it shipped.
Nothing compares that strike price to the latest known one. `engine/prices/gap_today.py`
prints both columns and is the instrument; it is read live, never from a document.

## Why this is a list and not a same-pass fix

A study's spot is not one number. Section 1 quotes it as the price the valuation is
compared against; section 3 draws the published probability cone, which is anchored on the
close the cone was STRUCK at and lives in `assets/data.js`; and the technical read carries
its own two-part stamp. Those are **three clocks**, and the protocol is explicit that a
mid-cycle price arrival refreshes the displayed cone only through the roll-forward path.

Moving `meta.spot` on its own would leave section 1 and section 3 quoting different last
closes on facing pages — a NEW defect of exactly the kind this pass exists to remove, and
one no gate would catch. Re-striking honestly means the roll-forward: merge the library,
Step 0.0, the materiality gate on the full market panel, strike the cone, refresh the
technical read and the chart. That is its own operation.

## Measured on 03-Sep-2026

`python3 engine/prices/gap_today.py` — read it live, never from this file. On the day this
was written, six of nineteen studies with a readable spot sat more than ten per cent behind
the market, and the gap moved a study across the ten-per-cent trigger in three cases.

| study | struck at | latest known | drift |
|---|---|---|---|
| TMGH 02-09 | 97.80 (23-Aug) | 96.60 (02-Sep) | −1.2% |

TMGH is listed because it was re-issued in this pass and the spot was *not* moved with it.
Its gap is −4.9% against the latest price and −6.1% against its strike, so nothing is
gated either way and no eight-heading review is triggered on either number — which is
precisely why it is recorded rather than quietly left.

## What closes an entry

The name's next roll-forward, which strikes the cone and the technical read on the same
library and lets the study's own spot move with them.
