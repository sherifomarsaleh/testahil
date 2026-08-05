# SELECTION ENGINE — STATE & STANDING ORDERS
*(last updated 27-Jul-2026; the reorientation doc — read this first in any session)*

## What the final product is

A ranked stock list for testahil.com — "of the 59 covered names in EG/AE/SA, the ones
most likely to beat their market over the next 3 months" — refreshed quarterly,
with a public forward-scored ledger. **Nothing ships until a factor passes the signed
pre-registration's §6 five-rule adoption gate.** No factor has passed yet.

## Where things stand (27-Jul-2026)

- Pre-registration **SIGNED** (`Selection_Engine_PreRegistration_v1_20260726.md`,
  §11 + Sign-off Record + F5 addendum). Spec is FROZEN; changes only via §10.
- **Full-power pooled test run** on 15-yr EG + long AE/SA
  (`claude/Pooled_FullPower_Test_20260727.md`, next to the interim run). Result:
  **no adoption.** F6 (52w-high) is the lead — passes rules 2-5, misses the
  Bonferroni IC bar by 0.0040. F4 demoted (SA sign flip, rule-5 breach). F1
  sign-correct but sub-bar (EG-negative / Gulf-positive split recorded). F2
  wrong-signed (0-for-3). F3 right-signed, not detected at 28% power.
- **F5 RETIRED — UNTESTABLE ON THIS DATA** (sponsor-signed; §11 addendum +
  `claude/F5_Volume_Forensics_20260727.md`). Bonferroni divisor stays 6. Never quote
  an F5 IC. Revival = value-traded data + §10 re-registration.
- **Shadow Selection Cohort #1 filed** (`claude/Shadow_Selection_Cohorts.md`),
  unpublished, grades ~late Oct 2026.
- Data: EG 15-yr on repo `main` (`cd68546`); AE 18 + SA 11 long exports gated clean
  (`claude/AE_Export_Gate_20260727.md`, `claude/SA_Export_Gate_20260727.md`); a
  one-action commit bundle was handed to Sherif to put them on `main`.
  **UPDATE 28-Jul-2026: that bundle is now on `main` (commit `108ab4f`)** — the long
  AE/SA libraries (2011→2026) and the pooled scripts are committed; step 3 is unblocked.

## Standing orders (autonomous cycle — Sherif wants minimal involvement)

A monthly scheduled task runs a fresh session that must:

1. Read this file first. Clone `github.com/sherifomarsaleh/testahil`.
2. **Shadow cohorts:** for any PENDING cohort in `claude/Shadow_Selection_Cohorts.md`
   whose three markets have reached the 3-month calendar mark past their anchors (use repo data,
   Step 0.0-gated), grade per the ledger's fixed spec, APPEND results (never edit
   existing entries), and file the next cohort at the then-latest anchors.
3. **Backtest re-run:** count EG majority-quorum sessions after 2026-04-20 (the last
   full-power anchor). If ≥60 new sessions AND the long AE/SA libraries are on
   `main` (AE files reaching 2011): re-run the frozen pipeline (scripts in project
   files `claude/*_pooled.py`, mirrored in repo `engine/selection/`), critical values
   re-simulated at the new real dimensions, §6 five-rule checklist per factor,
   report written next to the prior runs. If long AE/SA are NOT on `main`, say so in
   one line and skip the re-run — do not run at interim dimensions again.
4. **If any factor passes all five rules: DO NOT publish.** Write the adoption
   record draft and notify Sherif prominently — adoption and publication are his
   sign-off, always.
5. Discipline: spec frozen; §7 verdict language (`NOT DETECTED at this power`, never
   `no signal`); wrong-sign clearances are refutations; both-specs reporting for any
   §10 change (make none); survivorship-bias line in every report; never touch
   `market_profiles.py`, the MC engine, or the live site.
6. End with a ≤5-line summary (this becomes the notification Sherif sees).

Separate one-shot reminder (15-Oct-2026): FV Shadow Cohort #1 (pre-reg §9) reaches
first maturity — grade it if its files are reachable, else tell Sherif it is due.

## What still needs Sherif (nothing else does)

1. ~~**One git push** of the prepared bundle (long AE/SA + scripts + docs).~~
   **DONE 28-Jul-2026 (`108ab4f`)** — the bundle is on `main`; monthly re-runs are no
   longer blocked at step 3, and shadow grading now runs against the long libraries.
2. **Adoption sign-off and publication**, if and when a factor clears the gate.
3. Optional: value-traded data sourcing if F5 is ever to be revived.


> NAMING MIGRATION (29-Jul-2026): horizon wording updated from the retired session-count form to the calendar form ('3 months', per the 27/28-Jul calendar-only adoption). The horizon's DEFINITION is unchanged — the pre-registered test itself is not altered, only its name.

> CYCLE NOTE (02-Aug-2026): step 3 re-run reproduced for the 01-Aug firing — same 58
> anchors (grid still ends 2026-04-20, libraries not yet rolled forward), no adoption,
> F6 still one rule short (misses Bonf IC bar by 0.0037). Full repro:
> `docs/Pooled_FullPower_Test_ReRun_20260802.md`. Next answer-changing run needs the
> libraries rolled past ~mid-Oct 2026 to resolve a new anchor.
