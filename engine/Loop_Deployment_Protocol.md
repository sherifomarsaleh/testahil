# Loop Deployment Protocol

**Adopted 18-Aug-2026.** How recurring work is scheduled in this repo: which of the three
mechanisms owns which job, and why putting a job on the wrong one fails.

THIS FILE CONTAINS RULES AND COMMANDS, NEVER NUMBERS. Every count in it — covered names,
open ledger rows, cohorts maturing this month, panel sizes — is volatile and is READ LIVE
by the command shown, never quoted from here. The same discipline as
`PROJECT_INSTRUCTIONS_11-07-2026.md`.

---

## The three layers

Recurring work here splits by **who has to decide**, not by how often it runs.

| Layer | Mechanism | Owns | Survives the session ending? |
|---|---|---|---|
| Mechanical | **GitHub Actions** (`.github/workflows/`) | clean → panel rebuild → refit → LONO verdicts → materiality gate; SEO, feed, page-integrity, deploy | Yes — runs on GitHub |
| Recurring judgement | **Routine** (scheduled trigger, fresh session per firing) | metronome, gate review, disclosure watch | Yes — the scheduler re-creates the session |
| Within-session supervision | **`/loop`** | drive a publish to green, watch a PR, poll a long-running study | **No** — dies with the session |

The line between layer 1 and layer 2 is the line the unattended pipeline already draws:
**mechanical work is unattended; anything that would change a published verdict, imply a
signal change, or move a config beyond tolerance stops and asks a human.** A Routine is not
a way around that gate — it is a way to make sure someone shows up at it promptly.

### `/loop` is session-scoped, and that is the whole trap

`/loop` runs inside a live Claude Code session:

    /loop 30m /pulse          # interval mode — fires every 30 minutes
    /loop /pulse              # interval mode, default 10 minutes
    /loop watch PR #164 to green and tell me the moment it merges
                              # no interval given → dynamic mode: the agent picks
                              # each delay itself (60s–3600s) and stops when done

Interval mode repeats until stopped. Dynamic mode lets the agent pace itself against what
it is actually waiting for — a CI run gets one check sized to the run, not eight impatient
ones — and end the loop when the thing it was watching resolves.

**A `/loop` stops when its session stops.** In the web and remote environments the
container is reclaimed after inactivity, so a `/loop` left running overnight is simply gone
in the morning, with no error and no missed-run record. That is fine for supervision — the
thing being supervised finishes inside the session anyway — and disqualifying for anything
on a calendar. **Never put the metronome on a `/loop`.**

### Routines are the durable form

A Routine is a scheduled trigger that fires a prompt into a **fresh session** on a cron
(minimum hourly, expression evaluated in **UTC** — convert local times first). It survives
container death because the scheduler, not the session, holds the schedule.

Because each firing starts from nothing, a Routine's prompt must be a complete standalone
instruction. That is exactly why the jobs below are **repo slash commands** in
`.claude/commands/` rather than prose typed into a scheduler: one artifact, version
controlled, reviewed in a PR like any other engine change, and invoked identically from a
Routine, from a `/loop`, or by hand.

---

## The four standing jobs

| Command | Cadence | Writes? | Exists because |
|---|---|---|---|
| `/pulse` | every few hours | **no** | staleness is invisible until someone looks; a merge once silently reverted 9 technical blocks and nothing caught it |
| `/metronome` | daily, acts only when something matured | yes | the forecast is a calendar commitment, and grading is the one carve-out from "publishing needs an explicit ask" |
| `/gate-review` | daily | comments only, **never merges** | a material calibration change sitting unreviewed means production runs on the pre-change fit and nobody has decided |
| `/disclosure-watch` | weekly | no | a study was restruck the same day an external audit found a results release it had not swept |

### Why the metronome runs daily but is monthly work

The ledger is a rolling set of calendar commitments. Read what is due, live:

    node -e "const fs=require('fs');const {LEDGER}=new Function(fs.readFileSync('assets/data.js','utf8')+';return {LEDGER};')();const T=new Date().toISOString().slice(0,10);const open=LEDGER.filter(r=>r.realized_close==null);const due=open.filter(r=>r.grade_date<=T);const soon=open.filter(r=>r.grade_date>T);console.log('open',open.length,'| due now',due.length,'| next',soon.sort((a,b)=>a.grade_date<b.grade_date?-1:1).slice(0,5).map(r=>r.instrument+' '+r.horizon_label+' '+r.grade_date).join(', '));"

Maturities do not arrive in one monthly batch — they arrive on whichever calendar date each
cohort was struck plus one or three months, rolled to that exchange's first real trading
session. A monthly cron would grade some rows late by up to four weeks. A **daily** trigger
that reads the dates and does nothing when nothing is due grades every row on the day it
matures, and costs one cheap read on the days it is idle.

Steady state is four open rows per name; at full coverage the number of grade-and-restrike
events per month is large enough that doing them by hand is the single biggest repetitive
cost in the project. This is the job most worth automating and the one most dangerous to
automate carelessly — which is why `/metronome` runs the full market panel through Step 0.0
and the materiality gate before it strikes anything, and stops rather than striking on a fit
no human has accepted.

---

## Deploying

**Supervision, right now, in this session:**

    /loop 20m /pulse

**Durable, unattended** — create a Routine per job, fresh session per firing, cron in UTC:

| Job | Suggested cron (UTC) | Note |
|---|---|---|
| `/pulse` | `0 */6 * * *` | after the 03:00 calibration sweep has landed |
| `/metronome` | `0 6 * * 1-5` | weekdays; it no-ops when nothing matured |
| `/gate-review` | `0 7 * * *` | after the nightly refit could have opened a PR |
| `/disclosure-watch` | `0 8 * * 1` | Mondays |

Stagger them. Two jobs firing into the same repo minute will race on the working tree.

---

## Standing rules for anything run on a schedule

1. **A tick that found nothing says one line and ends.** A watch that narrates every quiet
   tick trains its reader to stop reading it, which is worse than not running it.
2. **Read volatile state live, every tick.** `market_profiles.py` is the single source of
   truth and refits whenever a stock is posted. A figure carried over from the previous tick
   is stale by construction — that is the failure mode these loops exist to catch, not one
   they may commit.
3. **Verify by import, not by parse** — Python modules and, for JS, `node --check` followed
   by actually LOADING `data.js` and asserting on the parsed objects.
4. **Count against a known total.** Never trust a tool's own "0 skipped": a regex matching
   unquoted object keys silently dropped `"2POINTZERO"` from three separate tools and each
   reported success.
5. **A watch does not repair.** `/pulse` and `/disclosure-watch` report; `/gate-review`
   recommends and never merges. Only `/metronome` writes, under an explicit standing
   carve-out, and it stops rather than striking on a fit a human has not accepted.
6. **Nothing merges to `main` unreviewed** except what the existing materiality gate already
   auto-commits as non-material. Scheduling changes nothing about that split.
7. **A schedule is not an authorisation.** `/loop` and Routines change *when* work happens,
   never *what may be published without asking*. Publishing still needs the explicit ask;
   grading a matured cohort still does not.
