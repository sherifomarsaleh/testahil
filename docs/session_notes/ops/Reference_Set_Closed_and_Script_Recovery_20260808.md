# Reference set closed · 48 uncommitted scripts recovered — 8-Aug-2026

Two things happened in one pass. The second was found only because the first prompted an audit.

## 1. The reference set is CLOSED at three names

Per Sherif's instruction: **SWDY** (the model study — structure, sheet list, depth bar, and the operating-company lens pattern), **ADCB** (bank), **ALPHADHABI** (holdco). Every other company was removed from the reference layer *outright*, not demoted to a retired or secondary entry.

Removed: TMPV (structural template), EAND (operating-co exemplar), RIBL (secondary bank exemplar), and the legacy GBCO / Kakao / EMFD-PHDC framing wherever it survived.

Reasoning on the record: a study named as "the old template" is still a name a future build can reach for, and a secondary exemplar of a class whose primary already covers it is redundant by construction.

**Enforced in code, not prose.** `REFERENCE_SET` in `engine/research_protocol.py` asserts on exactly `SWDY / ADCB / ALPHADHABI` at import. A fourth exemplar cannot be added without displacing one of the three and failing the import first — expanding the set is a protocol decision, not a documentation edit.

**Scope boundary, stated so nobody re-scopes it later.** This closes the REFERENCE layer only. Company names remain throughout the protocol as EVIDENCE for a rule (the CLHO terminal-value audit, the RMDA Kd miss, the ARCC cost stack, the COMI chart defect) and as coverage facts (stale-library list, calibration record). Stripping those would convert measured findings into unsourced assertions and breach append-only.

Surfaces updated: `Standing_Research_Protocol.md` (repo + project copy), `engine/PROJECT_INSTRUCTIONS_11-07-2026.md`, `engine/Study_Initiation_Prompt.md`, `engine/research_protocol.py`, `CLAUDE.md`, memory, and the live project-instructions block (owner paste).

Also corrected in the same pass: `claude/studies/ELEC_Study_State_20260805.md` had EAND/TMPV as its build target; it now targets SWDY, and three other stale items in it were fixed (missing standalone bibliography, gate items (a)–(o) rather than (a)–(r) + depth bar, the retired "PAT only on request" note).

Deleted: `claude/Source_Integrity_and_Ground_Up_Mandate.md` — an older competing copy of a HARD GATE whose beta clause read "regressed against the EGX30 history" flat, which is only correct for Egyptian names. The canonical top-level file says "its own local index." A stale second copy of a binding rule is worse than a duplicate.

## 2. 48 scripts existed ONLY in project files — including two published studies

An audit of project knowledge found 48 `.py`/`.json`/`.csv` files in the `claude/` namespace. Checked by filename against the full repo tree with a positive control: **zero of 48 were committed anywhere.**

The serious ones are study builds. **STC (Tadawul 7010) and XPTUSD (platinum) are PUBLISHED** — their .docx/.xlsx/.pdf sit in `files/`, `stc.html` is live, their `raw_ohlc` libraries and panels are committed — but no `engine/stc_study/` or `engine/xpt_study/` ever existed. Two standing guarantees were therefore unenforceable for those names:

- the QC gate's script-built-vs-delivered cell-by-cell diff, and
- the rule that post-delivery corrections fold back into the build scripts, not onto the delivered file.

The rest is `engine/lab/` — the code behind experiments the protocol cites as do-not-revive evidence (MC v4 arms, equation-lab rounds 5–8, the shrinkage work that became `adaptive_width.py`, the EG technical-signal ablation). **A rejection that cannot be re-run is an assertion, not a result.**

Recovered to `engine/stc_study/` (13), `engine/xpt_study/` (11), `engine/lab/` (24), each with a README. Verified: count asserted against the known total of 48; every `.py` parses, every `.json` loads; content byte-faithful (trailing-newline and ASCII-escape state preserved). Then, and only then, the 48 project copies were deleted.

### STANDING LESSON

**The plan before the check was to delete all 48 as redundant noise.** They looked exactly like clutter — build scripts sitting in a knowledge base. Deleting them would have permanently destroyed the only copy of the code behind two live published studies.

The rule this earns, and it is the same rule as COUNT AGAINST A KNOWN TOTAL and VERIFY BY IMPORT, NOT BY PARSE, applied to deletion:

> **Never delete on the assumption that a copy exists elsewhere. Verify the copy, with a positive control on the verification itself, then delete.**

A check that reports "not found" is worthless unless you have also proved it can report "found."

Corollary for the project knowledge base: project files are not a backup. Anything that is genuinely load-bearing belongs in the repo, and the presence of a file in project knowledge is evidence of nothing about the repo.

## State at close of pass

Branch `claude/swdy-model-research-protocol-xslnk3` @ `b725fc9`, three commits ahead of main, pushed and verified by fresh re-clone plus a live import of `research_protocol.py`. **No PR existed for this branch** — it had been pushed 6-Aug and left open-ended. A PR is still required before merge: the standing rule that engine and protocol changes get human review before reaching main was NOT retired by the 07-Aug publish-token change, which covered site publishing only.

`claude/` namespace: 127 items → 78.
