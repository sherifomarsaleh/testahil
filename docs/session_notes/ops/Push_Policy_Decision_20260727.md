# Push policy decision — 27-Jul-2026

> **[SUPERSEDED IN PART — 8-Aug-2026]** The policy adopted here — material Claude-prepared engine changes pushed straight to `main` on a chat "ship it", no feature branch and no PR — is no longer in force, and the current standing rule is its opposite: engine and protocol changes go on a feature branch with an open PR and a human review before merge, never a direct push to `main`. The paste-ready GIT/PUBLISH MECHANICS replacement text below is likewise retired, because it is built on the PAT / token-reuse cadence that was removed on 07-Aug-2026 — "publish" is now itself the authorisation and there is no token gate to reuse a token through. The rest of this document stands as the dated record of what was done at the time.

## What happened

User pushed back on "always PR, never direct push to main" for Claude-driven engine changes,
asking whether it's a new instruction and, if so, wanting it reversed. Checked git history on
`main` rather than assuming:

- 1,080 total commits on `main`; only **10** ever came through a merged PR.
- The **first-ever** PR merge was 13-Jul-2026 (`calibration-review-20260713-142440`) — the
  *automated pipeline* opening a review PR for **itself** when its own materiality gate tripped.
  Nothing to do with Claude's own pushes.
- The first PR for a **Claude-prepared** engine change was 22-Jul (`PR #13`, AE calibration refit)
  — 5 days before this decision, not the whole 2 months of usage.
- 4 of the 10 total PR merges landed in the 2 days right before this decision (26/27-Jul).

Conclusion given to the user: "always PR for my own changes" is a genuinely recent
generalization of the pipeline's own materiality-gate logic, not a longstanding rule. Correct to
question it.

## Decision

User asked "what should I answer to make life simple," i.e. asked for a recommendation rather
than picking from the three options offered (match-the-bot's-rule / always-direct / keep-always-PR).
Recommended and adopted: **match the bot's own rule.**

**New rule (replaces the old blanket "never direct push to main" line in GIT/PUBLISH MECHANICS):** [RETIRED 8-Aug-2026 — see header]

> Engine changes follow the SAME materiality gate as the automated pipeline
> (`auto_refresh.py`): push straight to `main` when nothing trips it — no per-name verdict
> change, no new FAIL, no market-verdict change, no panel carrying a name with no raw data, no
> >5% cone move (`width_cal × q95(t(ν))`). Open a feature branch + PR **only** when something
> IS material — a human reviews before that merges. Non-material pushes still go through the
> same fresh-PAT / inline-URL / never-store mechanics as every other push in GIT/PUBLISH
> MECHANICS; they're just not gated behind a PR.

Rationale given to the user for why this beats the two extremes: always-direct would have let
today's own findings (SA/EXTRA's FAIL, the AE/SA registry staleness) go live unreviewed;
always-PR adds review overhead to changes that are never going to be controversial. Matching the
bot's existing, already-battle-tested logic gives most pushes zero friction while keeping the
gate exactly where it's earned its keep.

**Note on PR #32 specifically:** unaffected by this change either way — it carries material
findings (SA's 3m band move, AE/SA's stale 60d fits), so it required a PR under the old rule and
still would under the new one. Whether to merge it is a separate, still-open decision for the
user (see `Calendar_Horizon_Adoption_1M_3M_20260727.md`).

## Update — same day, second revision: material changes too, gated by chat confirmation instead of a PR [RETIRED 8-Aug-2026 — see header]

### What happened

Same day, later: once the AE/SA 60d recalibration (see `RollForward_20260727_OCDI_ORHD_Gold_Samsung.md`
and the reverify work referenced in `market_profiles.py`'s AE/SA `fit_meta`) came back MATERIAL
under the gate above — EXTRA new robust FAIL, RAJHI loses PASS, MAADEN gains PASS, ALINMA to
BOUNDARY(PARITY-flagged) on the SA side; five AE verdict moves; both cones move >5% — the normal
path was a feature branch + PR. User objected to the PR step itself and asked to "make it
automatic through you."

Named the tension explicitly before doing anything: the first revision's own rationale, written
earlier the same day, is "always-direct would have let today's own findings — SA/EXTRA's FAIL,
the AE/SA registry staleness — go live unreviewed." This change is exactly that case, playing out
in real time. Said so, then offered three options rather than just complying or refusing:
full-auto-no-pause / keep-the-PR / a middle path where Claude pushes directly but the user still
gets a short summary and gives an explicit one-word go-ahead in chat instead of visiting GitHub.

### Decision

User picked the middle path: **"I push, you just say ship it."**

**New rule (further amends GIT/PUBLISH MECHANICS' PR step for MATERIAL Claude-prepared engine
changes):** [RETIRED 8-Aug-2026 — see header]

> When a change is material under the gate above, Claude still surfaces a short summary (what
> changed, which verdicts moved, the band-move %) same as before — but instead of a feature
> branch + GitHub PR, the user's go-ahead in chat ("ship it" or equivalent — handing over a fresh
> PAT after seeing the summary counts as this) is the review step. Claude pushes straight to
> `main` on that signal. No branch, no PR, no GitHub visit required. The fresh-PAT /
> inline-URL-only / never-store-in-config mechanics are UNCHANGED — this removes the review
> ceremony, not the token hygiene.

This supersedes the "material → PR" clause from the first revision above for changes Claude
prepares. It does NOT change how the *automated pipeline itself* (`auto_refresh.py` via the
GitHub Actions workflow) handles materiality on its own scheduled/triggered runs — that still
opens a PR per `.github/workflows/testahil-calibration.yml`, unmodified today. This rule is
specifically about Claude-prepared changes going through Claude in chat.

### First execution under the new rule

AE/SA 60d recalibration, pushed direct to `main`, no branch/PR:

- **SA**: ν 6→8, width_cal 1.063→1.021 (−8.08% band move, `width_cal × q95(t(ν))`). Verdict
  changes (4/11): EXTRA PARITY→**robust FAIL** −0.0308 (confirms the prior short-library PARITY
  read, same direction, now on 2×+ the data); ALINMA PARITY→BOUNDARY(PARITY-flagged) +0.0143;
  MAADEN PARITY→**PASS** +0.0223; RAJHI **PASS→PARITY** +0.0048 (loses PASS, not a FAIL). ELM
  stays robust FAIL (unchanged). Signal still OFF.
- **AE**: ν 10→8, width_cal 1.028→0.895 (−10.68% band move). Verdict changes (4/18): ADCB
  BOUNDARY(PARITY-flagged)→PARITY; ADIB PARITY→**PASS** +0.0395; DEWA BOUNDARY(PARITY-flagged)→
  PARITY; ADNOCGAS PARITY→BOUNDARY(PARITY-flagged); EAND PARITY→BOUNDARY(PARITY-flagged). No new
  FAIL, no lost PASS. LULU remains PROVISIONAL(insufficient-windows). Signal still OFF.
- Single-file diff (`engine/market_profiles.py` only); supporting evidence
  (`engine/reverify_post_merge.py`, `engine/PENDING_REVIEW/reverify_post_merge.json`) was already
  on `main` from earlier the same day, so nothing dangling.
- Verified by IMPORT (not parse) twice — once on the feature branch pre-merge, once again on
  `main` post-merge — matching the exact smoke-test the CI workflow itself runs.
- Mid-push, `origin/main` had moved 2 commits (user's own concurrent `portfolio.html` work,
  unrelated file, no conflict) — caught by re-fetching before the push rather than assuming the
  branch tip was still current; merged clean, re-verified by import again, re-checked origin
  hadn't moved a third time, then pushed. Landed as merge commit `965ac3e`. Confirmed live via
  anonymous `raw.githubusercontent.com` read post-push.
- Local feature branch deleted post-merge; remote `origin` URL confirmed still tokenless
  throughout (token was passed inline on the push command only, never written to git config).

### Note on the CI workflow's own materiality gate — unaffected

`.github/workflows/testahil-calibration.yml` triggers only on pushes touching
`engine/raw_ohlc/**.csv`, `workflow_dispatch`, and a daily `0 3 * * *` UTC cron catch-all. A
direct push to `engine/market_profiles.py` (like today's) does NOT trip the path-filtered
trigger, but WILL be picked up by tomorrow's 3am UTC cron running `auto_refresh.py --apply`
against the now-current file. Expected outcome: since today's numbers were produced via the
actual production fitting chain (not an approximation), a fresh recompute against the same
library should reproduce the same (ν, width_cal) and find nothing further to change — a silent
no-op. Flagging as an expectation, not a guarantee: if the bot's re-run surfaces ANY delta
tomorrow, that means today's manual computation diverged from the pipeline's own logic somewhere
and is worth a fresh look, not a rubber-stamp.

## Update — 28-Jul-2026: reuse the same token within a session [RETIRED 8-Aug-2026 — see header]

### What happened

Across the same-session trade.html/portfolio.html searchable-picker work, Claude asked for a
fresh PAT before a push (per the then-standing rule); the user replied "use same one"; Claude
declined once, citing the standing protocol, and asked for a new token; the user re-sent the
identical token string unprompted, directing Claude to proceed. This exact friction recurred a
second time later the same session on a subsequent push. The user then asked directly: "Change
testahil standing protocol to use the same toke. Only if it stops working do you ask for a fresh
one. Make that change everywhere."

### Decision

Adopted as stated — the ask was unambiguous and the friction it fixes had already shown up twice
in one session.

> Reuse the token already supplied in this conversation for every push in the same session — do
> not request a new one before each push. Request a fresh token only when: a push actually fails
> with a real auth rejection ("Invalid username or token", a 403 permission-denied, etc.), or it's
> a new session (nothing persists across sessions regardless of this rule, so the first push in
> any new session still needs the user to supply one).

**What did NOT change** (the ask was about asking cadence, not about custody): never store the
token value in memory, git config, or any project doc; inject it only in the one-off push command
URL, never written anywhere durable. A classifier block or a missing-scope error is not "stopped
working" in the sense that warrants a fresh token — only a genuine auth rejection does, since the
other two have nothing to do with the token's validity.

### Where this has been updated

- `claude/ops/GitHub_Push_Playbook_20260723.md` — rewritten same day; "Token handling" section now
  leads with the reuse rule and lists exactly which failure modes do/don't warrant a fresh token.
- This doc — the consolidated paste-ready replacement below now folds the reuse rule in alongside
  the still-unpasted 27-Jul materiality/ship-it language, so both stale points in the live
  condensed instructions can be fixed with a single paste.
- The condensed "Project instructions" custom-instructions text itself — **still not done**, same
  tool limitation as below: it's a claude.ai project setting only the user can edit.

## Not yet done

The condensed "Project instructions" custom-instructions text (what actually renders at the top
of every session) is a claude.ai project setting Claude cannot edit directly — only the user (or
someone with project access) can change it there. This doc records the exact replacement
language, now consolidated across the 27-Jul materiality/ship-it decision AND the 28-Jul
token-reuse decision, for whenever the user wants to paste it in. Until that's done, a future
session reading the *current* condensed instructions will still see the OLD "Request a fresh one
at the moment a write is needed... Engine changes go on a feature branch with an open PR, never a
direct push to main" language — stale as of all three revisions above. Worth pointing a future
session here if that comes up. [RETIRED 8-Aug-2026 — see header: the "OLD" feature-branch-and-PR language described here as stale is what the standing rule says today, and the token sentence has no successor at all]

Suggested replacement for the **entire** GIT / PUBLISH MECHANICS clause (drop-in for the whole
paragraph, not just one sentence — supersedes the two earlier partial suggestions above): [RETIRED 8-Aug-2026 — see header; do not paste this block anywhere]

> GIT / PUBLISH MECHANICS (applies everywhere above, both triggers, no exceptions): everything
> stays local. Never store a PAT in memory, git config, or any project doc. Reuse the token
> already supplied in this conversation for every push in the same session — do not ask for a new
> one before each push; request a fresh token only when a push actually fails with a real auth
> rejection, or it's a new session (nothing persists across sessions regardless). Inject the token
> inline in the push URL only, and leave the named remote tokenless throughout — don't set it to a
> tokenized URL and reset it after. Reads use anonymous raw.githubusercontent.com (repo is public).
> This is the mechanism the STANDING RULES carve-out above still runs through — "auto-published"
> means auto-prepared, not auto-pushed without a token. Engine changes follow the same materiality
> gate as the automated pipeline (auto_refresh.py): non-material pushes go straight to main.
> Material changes (per-name verdict change, new FAIL, market-verdict change, a panel carrying a
> name with no raw data, or the published 90% cone moving >5% via width_cal × q95(t(ν))) also go
> straight to main — Claude surfaces a short summary first and pushes once the user gives an
> explicit go-ahead in chat ("ship it" or equivalent). No feature branch, no GitHub PR, for
> Claude-prepared changes. This does not change how the automated pipeline's own GitHub Actions
> workflow handles materiality on its own runs — that still opens a PR.

Note on the remote-handling fix folded in above ("leave the named remote tokenless throughout"
instead of "reset the remote to the tokenless URL"): flagged during the 23-Jul Playbook work as
the better practice — a literal tokenized push URL never touches `origin` in the first place, so
there's nothing to reset — but never actually turned into replacement language until now. Called
out separately in case the user wants to paste only the token-reuse + materiality parts and leave
this piece for later.
