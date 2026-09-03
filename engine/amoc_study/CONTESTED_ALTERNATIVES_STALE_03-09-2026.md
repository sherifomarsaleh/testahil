# AMOC — the contested-choice alternatives are computed on a superseded bridge

**3 September 2026.** Found while building this study's [R-ENF-05] output records.
No delivered number moves; the headline fair value is unaffected. What is affected
is every figure this study publishes as *"the other way of doing it"*.

## What was found

`compute.py`'s `_val_at()` — the helper that prices each contested construction —
ends:

```python
return (_ev * (1 - nci_) - nd_cy25) / SH
```

The delivered headline does not come from that. It comes from the bridge in
`bridge_record`, which is six lines:

| line | EGP mn |
|---|---:|
| Enterprise value | 10,874.15 |
| less net debt (net cash, so this **adds**) | +3,001.54 |
| less provisions | −996.86 |
| less dividend payable | −258.30 |
| plus investments | +594.78 |
| less non-controlling interests | −411.11 |
| **equity value** | **12,804.21** |
| ÷ 1,291.5 mn shares | **EGP 9.9142** |

`_val_at()` on the same enterprise value returns **EGP 10.3528**. It differs in
two ways, and the second is the one that matters:

1. it omits provisions, the dividend payable and investments — three bridge lines
   worth −EGP 660.4mn together;
2. **it deducts the minority as a share of ENTERPRISE value** (10,874.15 × 4.645%
   = 505.05) where the delivered bridge deducts a share of EQUITY value (411.11).
   That is the construction [R-BRIDGE-01] (ii) forbids in as many words —
   *"deducted from EQUITY value, NEVER from enterprise value (an equity share on
   an enterprise number hands the minority growth assets it does not own)"* — and
   the two differ by exactly EGP 93.9mn, which is the whole gap between the two
   per-share figures once the three omitted lines are accounted for.

The delivered bridge is **right**. The helper was left on the construction the
bridge migration replaced.

## Why it matters, and it is not cosmetic

Every alternative this study publishes is compared against the headline, and the
two do not come from the same model.

## CORRECTION — an earlier version of this note got the size of that wrong

The first version of this section re-based the published alternatives onto the
delivered bridge and printed a "like-for-like" column. **That column is withdrawn.**
It assumed the helper differed from the delivered model in ONE way — the bridge —
and it differs in TWO, so re-basing only the bridge does not produce a
like-for-like figure. The correction is recorded here rather than quietly edited,
on the same append-only discipline the ledgers keep.

## The two divergences, both measured

Run `_val_at()` at the study's **own** adopted rates — `wacc_exp` 27.4543%,
`wacc_term` 18.1386%, `g` 7% — and it returns **EGP 10.8572** against the
delivered **EGP 9.9142**. That is **9.51%**, on identical discount factors
(verified: the helper's factor chain reproduces `fcst.df` exactly).

**(1) The terminal is struck on a different capital base.** The delivered terminal
return is computed on invested capital at **REPLACEMENT cost** — working capital
plus the asset base at gross cost — which is the study's own stated construction
and the reason its terminal reinvestment rate is what it is. `_val_at()` re-derives
`roic` from the FORECAST invested-capital series instead:

```python
_roic = nopat[-1] * (1 + g_) / ic[-1]      # forecast IC, not replacement cost
_rr   = min(g_ / _roic, 0.95)
_tv   = nopat[-1] * (1 + g_) * (1 - _rr) / max(wt_ - g_, 0.02)
```

At the centre that gives a terminal value of **17,504.6** against the delivered
**15,691.4** — **+11.56%** — and an enterprise value **+6.28%** above the
delivered one.

**(2) The bridge.** `_val_at()` ends `(EV × (1 − nci) − net_debt) / shares`. The
delivered headline comes from a six-line bridge that also carries provisions
(−996.9), a dividend payable (−258.3) and investments (+594.8), and that deducts
the minority as a share of **EQUITY** value (2.9628% of gross equity, 411.1)
rather than of **ENTERPRISE** value (4.6446%, 505.1). The second is the
construction [R-BRIDGE-01] (ii) forbids in as many words — *"deducted from EQUITY
value, NEVER from enterprise value"*.

## Why it is worse than a stale helper: it drives the sensitivity section too

`_val_at()` prices the three contested choices **and every cell of §1.9's
sensitivity grids** (`grid_wacc_g`, `grid_exp_term`, `grid_beta`). The
at-assumption cell of both two-dimensional grids reads **10.8572** against the
study's own headline of **9.9142**. A reader who looks at the sensitivity table
and then at the answer finds them 9.5% apart with nothing explaining it.

The beta grid is the exception and it is instructive: its centre reads exactly
9.9142, because that row is built by passing the study's own weights and rates
through and lands on the same point by construction.

## What the fix is, and it is not a patch

`_val_at()` has to reproduce the study's own model at the centre before any
alternative it prices means anything: the replacement-cost terminal, then the
delivered bridge. The test is arithmetic and unambiguous — at the adopted rates it
must return **9.9142**. Until it does, no number this note could compute for the
alternatives would be worth printing, which is why none is printed here now.

## What is NOT concluded here

The right column is **indicative, not the record**. It re-bases the alternatives
onto `_val_at()`'s own construction, which is the superseded one; the honest fix
is the reverse — re-run each alternative through the DELIVERED bridge — and that
is a study re-issue, not a note. AMOC therefore stays on the `output_outstanding`
ratchet and its [R-ENF-05] records are not published on a construction I cannot
stand behind.

There is also a plain contradiction in the study's own text, recorded here rather
than resolved: `compute.py` describes gross-debt weights as *"the construction
this study rejects because it counts the cash pile twice"*, while `bridge_record`
records `weights_basis: "gross"` as adopted and names the NET-weighted rate as the
defect a previous edition carried. One of those two sentences is stale. The
numbers say the bridge record is the current one — `wacc_exp` equals `ke_exp`
exactly, which is what a book of 0.14% debt produces — so the prose in
`compute.py` is what needs correcting at the next re-issue.

## What would overturn this

If `_val_at()` turns out never to reach a delivered document — if every published
alternative is computed somewhere else — then this is a dead helper and not a
defect. The check is a grep for these four keys in the builders, and they do
reach the workbook: `build_xlsx_amoc.py` writes `ccy_alt_ps`, `ps_rating_basis`
and `ps_gross_basis` into the fair-value sheet.
