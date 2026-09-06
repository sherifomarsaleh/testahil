# A lens read that does not move is a BOUND, and the book carries four of them

**Dated 6 September 2026.** Measured, not argued: `study_numbers.json` across all 24 study
directories, every scenario triple the committed numbers expose. Reproduce with the probe at
the foot of this file.

---

## Where this came from

`engine/elec_study/AUDIT_06-09-2026.md` closed with a rule-extension candidate stated but not
adopted: **"no floor of any kind enters a weighted answer — not book, not a limited-liability
clamp, not a lens pinned to its own minimum."**

**Half of that candidate is already law and needed no amendment.** `assert_lens_design()`
fails any record carrying weights at all, on the primary or on any cross-check, and fails
`book_value` carrying a weight specifically. A floor cannot enter a weighted answer in a study
whose record declares its weights, because no weighted answer may be declared.

What the candidate names that nothing covers is the other half: **a bound is not a valuation,
and averaging is not the only thing that can be done wrongly with one.** A bound published in
a cross-check table, or setting the end of an envelope, is the same category error with no
weight anywhere near it — and ELEC's own case is the proof, because retiring its blend leaves
`relative` reading 0.0500 in bear, base and bull with nothing saying it is a clamp.

## The measurement

**80 scenario triples across the book. Four do not move.**

| study | path | bear / base / bull | what it is |
|---|---|---|---|
| ELEC | `/lenses/relative` | 0.05 / 0.05 / 0.05 | **`max(…, 0.05)`** — a clamp, unlabelled |
| ELEC | `/lenses/dcf` | 0.01 / 0.01 / 1.0111 | **`max(…, 0.01)`** — a clamp binding in two of three, unlabelled |
| SCEM | `/lens_ranges/Book value (disclosed floor)` | 27.1186 ×3 | a bound, **LABELLED in its own key. CLEAN.** |
| SCEM | `/lens_ranges/DCF (cash flow)` | 23.6201 / 123.2717 / 123.2717 | **not a bound at all** — `bull=fv_dcf`, the base repeated |

### Three classes, and the fourth row is why this is not one rule

**(1) An unlabelled clamp.** ELEC's two. `compute.py:386-388` and `:480` are explicit
`max()` calls the study's own comments describe correctly — nothing is hidden — and the
committed numbers then present the results as lens reads beside three that are valuations.
A reader of the cross-check table cannot tell which two are answers and which two are bounds.

**(2) A labelled bound.** SCEM's book value, flat in all three and saying so in the key a
reader sees. This is the rule working and **it must not fire.** [R-LENS-03] already names book
a disclosed floor published as such; SCEM does exactly that.

**(3) A corner that is not a corner.** SCEM's DCF sets `bull = fv_dcf`, so the envelope is
one-sided: the margin is flexed DOWN from the base and never up, and the bull column repeats
the base. That is not a clamp and not a floor — it is a range with one real end — and the
arithmetic cannot tell it apart from class (1) without knowing what the builder did.

## What the measurement decides about the instrument

**THE FLAT SIGNATURE IS AN ADVISORY AND NEVER A GATE, on its own evidence, both ways at once.**

- It **UNDER-DETECTS.** ELEC's `dcf` is clamped and moves in the bull, so a strict
  identical-across-three test misses the study's own primary lens and catches only the
  cross-check beside it. The number a bound takes is not required to be the same number in
  every scenario; a clamp binds where it binds.
- It **OVER-DETECTS.** One of its two three-way hits is SCEM's correctly disclosed floor. A
  gate firing there would be the permanently-red check [R-ENF-02] forbids, and re-pointing it
  by pattern-matching the word "floor" in a key would be a check on a caption.

So the detectable half and the enforceable half are different objects, which is
[R-ENF-01 EXTENDED 04-Sep-2026]'s waterfall finding arriving again: **where the page cannot
say enough for the test to work, the test moves to whoever knows rather than being weakened
until it passes.** The builder knows it wrote `max()`. Nobody else can.

## The rule as it should be written — narrower than the candidate, and true

**A LENS READ THAT IS A BOUND SAYS SO, AND A BOUND IS NEVER PRESENTED AS A VALUATION.**

- A lens whose committed value is its own clamp declares `bound: {clamped_at, reason}`, from
  the builder, at every scenario where the clamp binds.
- A declared bound may not be the primary and may not be the central — a floor is a
  *constraint on* a value, not a *reading of* one, and [R-LENS-03]'s "one class primary IS
  the central" already forbids the central being anything but a read.
- A declared bound may set an envelope end only labelled as a bound, because an envelope end
  a reader takes for a valuation is the same error the cross-check table makes.
- The flat-across-scenarios probe stays as an **advisory** that names candidates for the
  declaration, and its two failure directions are published beside it rather than hidden.

**NOT ADOPTED IN THIS PASS.** It is a rule amendment: both governing documents in one commit,
an identifier, enforcement from outside and a negative control whose clean cases are SCEM's
labelled floor and SCEM's one-sided corner. Recorded here with its arithmetic so the
amendment is written against a measurement rather than against an anecdote.

**Nothing is corrected here.** ELEC's blend is a re-issue with a rebuild ledger
[R-REBUILD-01], and its deeper defect is the one its own audit found afterwards: a terminal
margin forecast at 12.30% against a filed record of 25.33–30.68%, which is [R-ANCHOR-01]
territory and is what actually produces the negative equity the clamps then hide.

---

## The probe

```python
import json, glob, os
# THE SCENARIO ORDER IS PART OF THE READING, so the triples are TUPLES and never
# a set's iteration order: a first draft of this probe printed ELEC's clamped cash-flow
# lens as [0.01, 1.0111, 0.01] and a reader would have taken the BULL for the clamp.
SCEN = (('bear', 'base', 'bull'), ('bear', 'base', 'full'), ('low', 'base', 'high'))
def walk(o, path=''):
    if isinstance(o, dict):
        for s in SCEN:
            if all(k in o and isinstance(o[k], (int, float)) for k in s):
                yield path, s, [float(o[k]) for k in s]
        for k, x in o.items(): yield from walk(x, path + '/' + str(k))
    elif isinstance(o, list):
        for i, x in enumerate(o): yield from walk(x, path + '[%d]' % i)

for p in sorted(glob.glob('engine/*_study/study_numbers.json')):
    tk = os.path.basename(os.path.dirname(p)).replace('_study', '').upper()
    for path, names, v in walk(json.load(open(p))):
        u = len(set(round(x, 10) for x in v))
        if u < 3:
            print(tk, path, '/'.join(names), v, 'flat in %d of 3' % (4 - u))
```
