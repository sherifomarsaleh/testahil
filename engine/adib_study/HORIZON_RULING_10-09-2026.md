# ADIB — the forecast horizon stays at five years, by instruction

**10 September 2026.** Recorded because the next session will find the same red gate and
should not re-open a question the principal has already answered.

## What was found

`scripts/check_macro_coherence.py` refuses this study: it carries no macro record, and the
record it needs would fail on its own terms. [R-MACRO-01] requires the explicit window to
run until growth is within two points of the terminal, or "the terminal capitalises a
growth rate the model never reached and takes most of the value with it". This study ends
FY2030 with net financing to customers growing **12.0%** and hands straight to a **7.00%**
terminal. Five points, switched off in one step.

The five points are not share gain — the study's own note has share drift reaching zero by
FY2030 — they are credit deepening, in an economy whose private credit is 26% of GDP.

## What was built and then reverted

The window was extended to FY2032 on one principle: by FY2031 the economy is at its
terminal state on the house path, so every ratio holds at its FY2030 level and only the two
things still converging keep converging — the financing book's real spread over terminal
inflation, halved each year (5.0pp → 2.5pp → 1.25pp), and administrative cost growth. That
reaches the window and the macro gate went green.

**It moved the central from EGP 44.4610 to EGP 41.8291, and the gap to the latest known
price from −14.6% to −19.6%.** The direction is informative rather than an artefact: two
explicit years at 9.5% and 8.25% growth, discounted at a near-term cost of equity in the
high twenties, are worth less than the two years of terminal value they replaced. Read
plainly, that says the five-year model was overstating by handing off early.

## The ruling

The principal instructed: **"do not extend horizon beyond 5 years."** The instruction was
given after being shown the number, the direction, and the reason the gate exists.

**This is a decision, not a finding, and it is recorded as one.** No number was moved
toward or away from any price. The study publishes EGP 44.4610 on a five-year window, and
`check_macro_coherence` stays RED on this name. It is not on the outstanding ratchet and
cannot be added to it — that list may only ever shorten — so the failure stands in the
open rather than being excused.

## What would settle it properly

The terminal itself. Seven per cent is terminal inflation at ZERO real growth: the bank
stops taking share AND stops participating in credit deepening the moment the window
closes, in an economy growing 4.5% real. If a terminal real growth of about 3% were
evidenced, terminal nominal growth would be near 10.2% and the FY2030 handoff would clear
the two-point window with no extension at all — and it would raise the answer rather than
lower it. That is a real question and it is open. It is NOT a way of getting 44.46 back,
and it must be argued from evidence about this bank and this credit market or not at all.
