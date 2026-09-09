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
