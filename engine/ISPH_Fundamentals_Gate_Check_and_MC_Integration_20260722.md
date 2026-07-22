> ## ⚠️ CORRECTION APPENDED 22-Jul-2026 (later same day) — supersedes finding #1 below
>
> **The "immaterial prose imprecision" call in finding #1 was WRONG. It was the same
> material off-by-one WACC bug later found and fixed in ORHD, and it has now been
> corrected in ISPH too.**
>
> What changed the reading: after this gate-check was written, a deep-dive on ORHD
> (user-driven) established the standing convention that **year-1 (FY26E) of the declining
> schedule must use the FULL current normalized rf\* (15.94%)**, i.e. multiplier `*0`, not
> `*1`. The ORHD corrected Fig 13 and `Cost_of_Capital_Reference.md` both anchor 2026 rf\*
> at 15.94%. Two EGX names forecast from the same base date cannot use different year-1
> risk-free rates, and the near-term (current-year) cash flows must be discounted at
> today's rate, not one already stepped down 1.4pp.
>
> Inspecting the ISPH model confirmed the identical formula bug: `DCF & WACC!B13` = `=$C$3-$C$5*1`
> (rf\*) and `B14` = `=$C$4-$C$5*1` (Kd) — FY26E already one step down (14.54% / 24.60%)
> instead of the base (15.94% / 26.00%). Fig 14 of the note presented "22.31% − 6.37% =
> 14.54%", which is arithmetically wrong (= 15.94%) — the same tell as ORHD's note.
>
> **Fix:** changed the multipliers to `*0..*4` in rows 13–14. Rebuilt a Python replica of the
> full DCF chain, verified **bit-exact** against the corrected xlsx recalc (FV 18.1578816249
> to 10 dp; terminal WACC 0.207343..., ΣPV 9697.448 — all match).
>
> **Corrected numbers (were → now):**
> - Fair value / share: EGP 20.86 → **18.16** (buggy model recalc'd 20.89; corrected 18.16)
> - Upside vs spot 11.67: 79% → **56%**
> - Year-1 rf\*: 14.54% → **15.94%**; Kd yr1: 24.60% → **26.00%**; Ke yr1: 27.38% → **28.78%**
> - WACC path: 24.65%→19.43% became **25.95%→20.73%** (terminal WACC +1.30pp)
> - Fig 12 grid recentred on terminal WACC 20.73% (rows 18.73–22.73%); box span EGP 15.0–32.2 → **14.6–24.6**
> - Bear/Base/Bull (Fig 12 diagonal): 17.5 / 20.9 / 25.4 → **16.2 / 18.16 / 20.8**
> - Also synced the pre-existing FY27E FCFF drift (3,082 → 3,127, finding #2) so the reissued
>   docx and xlsx now agree exactly.
>
> **Deliverables reissued 22-Jul-2026:** corrected `ISPH_ThreeStatement_Model.xlsx` (formulas
> fixed, 0 recalc errors) and `ISPH_Valuation_Note_TESTAHIL.docx` (79 position-verified edits
> in the user's own file, format untouched, XSD-validated, page-by-page visually checked).
> The MC/TA + fundamentals 1-page and 2-page combination reports were regenerated with the
> corrected Bear/Base/Bull (16.2/18.16/20.8) and a redrawn cone chart. Nothing pushed to the
> repo; local deliverables only.
>
> **Integration-table impact (below):** the P(touch) table and CAGR columns used the OLD
> levels 17.5/20.9/25.4. Corrected touch-probabilities at spot 11.77:
> Bear 16.2 → 51/74/84% (1/2/3y); Base 18.16 → 35/62/76%; Bull 20.8 → 22/49/65%.
> The "~2–3 year hinge" synthesis still holds qualitatively but is now WEAKER: with lower
> fair values, only Bull's year-1 EV (23%) clearly beats the 19.5% cash rate, Base barely
> (20% yr1), and nothing beats cash by year 2 — the case for holding over cash is thinner
> than the original table implied.
>
> **Lesson:** a declining-rate schedule whose year-1 multiplier starts at `*1` is the
> fingerprint of this bug. Check FY26E == full normalized rf\*, not one step down, on every
> EGX declining-WACC model. The original "immaterial" call happened because the base cell
> (C3=0.1594) looked correct in isolation; the bug only shows when you ask what the FIRST
> forecast year actually discounts at.
>
> ---
> *Original 22-Jul-2026 gate-check preserved below unaltered (append-only). Finding #1's
> "immaterial" conclusion is retracted by the above; findings #2 (FCFF drift, now fixed) and
> #3 (single ERP basis, still open) stand.*

# ISPH fundamentals gate-check + fair-value/MC integration (22-Jul-2026)

Source: user-uploaded `ISPH_Valuation_Note_TESTAHIL.docx` + `ISPH_ThreeStatement_Model.xlsx`,
dated 21-Jul-2026. Not present in the project's canon of studies (project_search found no
matching ISPH doc) — treated as external input, gate-checked before use.

## Gate-check findings
**Historicals — verified, not just claimed.** Spot-checked FY25/FY24 revenue and net income
against independent reporting (Zawya/MarketScreener, sourced to the company's own release):
revenue 76,597 / 55,842 EGP mn and net income 952 / 615 EGP mn (both years) match the model
exactly. The SIGCM "official sources only" claim holds up on this check.

**Model mechanics — clean.** Recalculated (LibreOffice, `recalc.py`): 211 formulas, 0 errors.
Genuine driver→IS→BS→CF→DCF structure (Drivers sheet inputs, every downstream sheet is a
formula), invested-capital identity closes (NOA = equity + net debt, plug on net debt).

**WACC — correctly follows the v2 hierarchy on the pieces checked.** rf* = Egypt 10Y (22.31%)
− Egypt's own default spread (6.37%) = 15.94% base, declining 1.4%/yr — consistent with the
standing "normalize by the sovereign's OWN spread, count country risk once" rule. Beta is
tier-1 (own-stock 5yr weekly vs EGX30, n=261, R²≈20.5%, SE≈0.11 — passes the usability gate).
Kd (26% base) sits above the sovereign yield, as required. Weights are market-value equity.
[RETRACTED IN PART — see correction at top: the schedule declines from the WRONG year-1
anchor because FY26E used multiplier `*1` not `*0`; the base 15.94% is right but the forecast
never actually uses it in year 1.]

**Three real issues found:**
1. Minor prose imprecision: the summary paragraph calls 14.54% "the normalised risk-free
   rate" — that's actually the model's FY26E (year-1, already-stepped) rf*, not the base
   rate the same sentence's own arithmetic implies (22.31−6.37=15.94%, which is what's in
   the model as the base). Correctly labeled "(yr 1)" in Fig 13 later in the document —
   just imprecise in the opening summary. Immaterial to the number, worth tightening.
   **[RETRACTED — this was the material off-by-one bug, now fixed. See correction at top.]**
2. Small docx/model drift: recalculating the live model gives fair value EGP 20.89/share,
   not the stated EGP 20.86. Traced to one cell — the docx's printed FY27E unlevered FCFF
   (3,082) doesn't match what the formulas actually compute (3,127); every downstream
   difference (ΣPV FCFF, EV, equity value, fair value/share) is fully explained by that one
   input, confirming the docx was drafted from a slightly earlier model iteration. ~0.16%
   effect on the headline number — immaterial to the conclusion, but the docx and the
   delivered xlsx are not currently in sync. **[FIXED in the 22-Jul reissue — FY27E synced to 3,127.]**
3. Single ERP basis shown (Damodaran rating-basis only). The standing WACC protocol requires
   publishing both ERP bases (rating-basis and CDS-basis) since the CRP subtracted from rf*
   must match the basis added back in the ERP. Only one basis appears here. **[STILL OPEN.]**

**Format:** this is a lighter "fair-value note," not a full TMPV-format 16-section study —
single DCF lens, no expert-persona appendix, no Step-2A four-ring sweep register shown, no
dual ERP basis. Six-clause disclaimer and no-rating/no-target framing both correctly match
house style. ORAS fundamentals were referenced ("both stocks") but never uploaded — gap.

## The integration: fair value as a second, longer-horizon reference level
Chart S/R levels (route 1, established earlier) and DCF fair value are not the same kind of
object and don't collapse into one bracket: fair value (EGP 17.5–25.4 bear/bull, 20.9 base,
vs spot 11.77 — a 49–116% distance) is roughly 5–10x the size of any move route 1 was pricing
over 10–30 sessions. They sit at different timescales and answer different questions: TA+MC
(weeks) prices near-term chart-level odds; fundamentals (years) is the reason to hold at all.
The honest way to combine them: feed the fair-value band into the SAME calibrated MC
distribution as additional levels, at MULTI-YEAR horizons, to ask "given only the market's own
historical vol and carry — no fundamental information, no signal — how ordinary or extreme
would reaching fair value be, and on what timescale?" This is diagnostic, not predictive: it
does NOT get injected into the engine's drift (a single point-in-time DCF isn't a repeatable,
LONO-testable signal the way a mechanical indicator is — that would need a systematic,
historically-consistent value-factor panel across many names/dates, a much larger undertaking,
not what a single current DCF provides).

Method: same production chain as route 1 (fit_har_v3 → har_forecast_v3 → carry_log_h →
simulate_paths_v3; nu=4, width_cal=0.972, seed 42, 50k paths), extended to horizons out to
4 years. HAR variance forecast uses the engine's native ≤1y forecast convention, held flat
beyond 1y (explicit, stated simplification — the engine has no >1y variance term structure).

| horizon | P(touch bear 17.5) | P(touch base 20.9) | P(touch bull 25.4) | implied CAGR (bear/base/bull) |
|---|---|---|---|---|
| 1.0y (h=240) | 40% | 22% | 10% | 48.7 / 77.6 / 115.8% |
| 1.5y (h=375) | 56% | 37% | 21% | — |
| 2.0y (h=500) | 66% | 48% | 32% | 21.9 / 33.3 / 46.9% |
| 3.0y (h=750) | 78% | 65% | 50% | 14.1 / 21.1 / 29.2% |
| 4.0y (h=1000)| 85% | 75% | 63% | — |

(Full 8-horizon table incl. 0.24y/0.48y/0.71y/5y CAGR in the companion script output.)
**[NOTE: table above uses the pre-correction levels 17.5/20.9/25.4. Corrected P(touch) for
16.2/18.16/20.8 at 1/2/3y: Bear 51/74/84%, Base 35/62/76%, Bull 22/49/65%. See correction at top.]**

**Synthesis.** Two independent cuts converge on the same ~2–3 year hinge: the MC engine's own
historical vol says ~2 years is roughly the halfway point for reaching fair value by pure
chance (no re-rating needed); separately, the DCF's own implied CAGR stops clearly beating the
19.5% EGP risk-free rate right around that same 2–3 year mark (bear/base CAGR at 3y: 14.1%/
21.1%, both at or below cash; at 1–2y, all three scenarios clear cash comfortably). Read
together: if the fundamental thesis needs materially more than ~2–3 years to play out, it stops
being obviously better than EGP cash even if it's directionally right — the case for holding
rests on believing convergence happens on the faster end of this range (i.e., on a genuine
re-rating/catalyst, not just drift), which is exactly the kind of claim this MC engine cannot
price (it has no fundamental input) and that the fundamental note itself cannot validate
out-of-sample (a single DCF is a thesis, not a backtested signal).

## What this does and doesn't establish
Does: gives a concrete, calibrated timescale for reading the fundamental thesis against the
stock's own historical vol, and an honest apples-to-apples return comparison vs cash — same
discipline as the TA-ablation and cash-comparison work earlier in this session. Doesn't:
validate the DCF's own assumptions (declining WACC path is self-flagged by the note as "the
single most important, most debatable" input; no flat-WACC alternative shown), doesn't get
promoted into the engine (no LONO test exists for a one-off point estimate), doesn't cover
ORAS (file never arrived), doesn't replace the near-term route-1 bracket pricing already built.

Scripts: fv_convergence.py. Engine not modified; nothing promoted; repo untouched.

---
*Committed to `engine/` in the public repo on 22-Jul-2026 as version-controlled documentation
(this audit note only). The reissued deliverables (xlsx/docx/PDFs) and the engine code/forecasts
were NOT pushed — the "repo untouched" line above refers to the engine forecasts/code, which
remain untouched. Reads are anonymous; any future engine write still needs a fresh token.*
