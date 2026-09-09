# KABO's supplied price is wrong, and the question reaches further than KABO

**Raised 9 September 2026 by the principal, in these terms: "Noo Kabo is not 34 EGP."**
Recorded here because an answer that lives only in a conversation binds nothing — the
container is rebuilt from the repository, and the next session cannot see the chat.

## What the two records say

| Source | Price | Date |
|---|---:|---|
| `engine/raw_ohlc/EG/KABO.csv`, last row | **9.120** | 23 August 2026 |
| `engine/prices/SUPPLIED_03-09-2026.json` | **34.06** | 3 September 2026 |

That is +273% in eight trading sessions. The principal states the 34.06 is not the
price. The library number is the one with a series behind it.

## Why it was noticed

KABO was first in the rebuild queue ordered by gap to the latest traded price, at
**−93.0%**, entirely because of the 34.06. Against the library's 9.12 the same fair
value of 2.39 is **−73.8%**, which moves it well down that ordering. The queue position
was an artefact of the price, not of the valuation.

## THE PART THAT IS NOT ABOUT KABO

The supplied price file is what the **traded-price gate** reads, and that gate is Phase
1's acceptance criterion 4 — the one that decides which names pass and which are
REFERRED to the principal. A wrong price there does not produce a wrong fair value, but
it produces a wrong ROUTING: a name can be referred that should have passed, or pass
when it should have been referred.

Nothing was published on this price and no fair value was moved by it. KABO's baseline
was frozen at bear 1.42 / base 2.39 / full 3.52 against the LIBRARY spot of 9.12, so the
snapshot is unaffected.

## What has NOT been done, deliberately

The price has not been changed. A valuation input is sourced, never adjusted to make two
records agree, and which of the two is right is a sourcing question rather than an edit.
The principal asked to return to this later.

## What to check when it is taken up

1. Whether `SUPPLIED_03-09-2026.json` carries other prices that disagree with the
   library, and by how much — the same comparison across every covered name.
2. Whether any name's traded-price-gate routing changes when the library price is used
   instead.
3. Where the supplied file's KABO figure came from, since a 273% move is either a real
   corporate event with a disclosure behind it or a bad row.

## The baseline was taken and then withdrawn, and why that is not a loss

`fv_movement.py snapshot KABO` was run before the price question surfaced, freezing bear
1.42 / base 2.39 / full 3.52 against the library spot of 9.12. The register check then
refused it, correctly: **`KABO carries a record with no walk-forward run directory behind
it`.** A baseline is frozen so the campaign cannot overwrite an old number it is about to
move — it is meaningless without a run that moves it, and a record standing alone is a
claim about work nobody did.

So the entry was removed rather than the check weakened. The append-only rule on baselines
exists to stop one being RE-CAPTURED after the campaign has already moved the number; that
danger does not arise here, because nothing touched KABO's fair value. The numbers are
preserved in this file and in the commit that added them, and a fresh snapshot when the run
actually starts will read the same unmoved `data.js` figures.

**The frozen values, kept here so the withdrawal costs nothing:**
bear **1.42** / base **2.39** / full **3.52**, spot **9.12** at the close of 23 August 2026,
captured 9 September 2026, `built_to` reported as "(no study)" — which is itself wrong, per
the note above.

---

## MEASURED ACROSS ALL NINETY, LATER THE SAME DAY — KABO IS NOT ALONE

The section above says the question "reaches further than KABO". It does, and the reach is
now measured rather than asserted. `scripts/check_supplied_prices.py` holds every supplied
price against that name's own OHLC library, and asks not "how big is the difference" but
**"is a move this big, over this many sessions, something this stock has ever done"** — so
there is no threshold to argue about. Four names sit outside their own record:

| name | supplied | library | library date | implies | the name's own 99.5th pct |
|---|---:|---:|---|---:|---:|
| KABO | 34.060 | 9.120 | 23-Aug | **+273.5%** over 8 sessions | 37.5% |
| SABIC | 81.400 | 50.100 | 01-Sep | **+62.5%** over 1 session | 7.1% |
| IQCD | 13.170 | 9.965 | 01-Sep | **+32.2%** over 1 session | 6.7% |
| QGTS | 4.850 | 4.310 | 01-Sep | **+12.5%** over 1 session | 7.1% |

All four come from `SUPPLIED_03-09-2026.json`. SABIC's is the one to look at after KABO:
+62.5% in a single session, against a library that ends two days before the supplied date
and has never moved more than 10.1% in a day in its whole recorded history.

**What each one changes, if the library is right.** SABIC shows on the pipeline as REFERRED
at −31.8%; on the library price the same fair value is about **+10.8%** and it would CLEAR.
IQCD shows REFERRED at −17.2%; on the library price about **+9.4%**, and it would CLEAR.
That is the wrong-routing consequence this note predicted, now with names on it.

**Nothing has been changed.** All four are on the gate's ratchet, which may only shorten,
because which record is right is a sourcing question for the principal and not an edit.

## A SEPARATE DEFECT, IN OUR OWN DATA

Building that gate surfaced something that is nobody's supplied figure. **The Qatari
libraries carry unadjusted corporate actions**: IQCD's largest single-session move reads
**894.7%** and QGTS's **908.3%**, against 99.5th percentiles of 6.7% and 7.1%. A price
series does not do that; a split recorded as a price change does.

It matters beyond tidiness. The first cut of the gate used each name's LARGEST historical
move as its bar — which sounds like the strictest possible empirical test and is close to
the most permissive one, because a bar of 894.7% is a bar no supplied price could ever
exceed. **The gate could not have fired on either Qatari name, whatever was supplied.**
That is why the bar is a percentile. The artefacts are named in the gate and are NOT fixed
there: adjusting a price series is a sourcing job, not a gate's.
