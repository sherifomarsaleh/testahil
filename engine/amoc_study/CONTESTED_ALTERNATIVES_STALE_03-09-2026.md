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
two sit on different bridges — so the comparison measures the bridge as much as
the judgement.

The alternatives can be re-based onto the DELIVERED bridge exactly, because the
helper's own output inverts to an enterprise value and the delivered bridge is a
closed-form function of it:

```
ev_alt      = (ps_helper x shares + net_debt) / (1 - nci_share_enterprise)
ps_delivered = ((ev_alt - net_debt) x (1 - NCI_OP) - provisions - dividend
                + investments) / shares
```

`NCI_OP` is **2.9628%** — the minority's share of gross EQUITY value, recovered
from the delivered bridge's own lines — against the **4.6446%** share of
ENTERPRISE value the helper applies. Run on the study's own enterprise value the
identity returns **EGP 9.9142**, the delivered figure to four decimals, which is
what makes the re-basing a reconstruction of this study's bridge rather than a
second opinion about it.

| contested choice | as published | like-for-like on the delivered bridge | vs the headline 9.9142 |
|---|---:|---:|---:|
| rating-basis cost of capital, not CDS | 8.7990 | **8.3330** | **−15.9%** |
| gross-debt rather than net-debt weights | 10.8586 | **10.4289** | **+5.2%** |
| discounting the export leg in dollars | 10.6473 | **10.2139** | +3.0% |
| minority share doubled to 6% | 10.7359 | *not computable here* | — |

The last row is left blank deliberately. "6%" is a share of ENTERPRISE value in
the helper's construction, and what it becomes in a bridge that charges the
minority against gross equity is a judgement about the alternative itself, not an
arithmetic conversion. Filling it by analogy would be inventing the number this
note exists to complain about.

**What changes on the correct basis.** As published, three of four choices clear
the 5%-of-value materiality line. Like-for-like, of the three that convert
exactly, **two do — one down and one up** — so the sign test on this study is a
one-all draw rather than the three-nothing it would have read as. The direction of
the error is not constant either: the rating-basis row gets *larger* on the
correct bridge (−11.2% to −15.9%) while the currency row falls out of materiality
altogether (+7.4% to +3.0%). A single correction factor could not have fixed this.

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
