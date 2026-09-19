# Machine-improvement brief — making TESTAHIL improve itself

**Written 17-09-2026, from a live code audit. Hand this to a new session as its
starting context.** It is a WORK BRIEF, not a standing rule: nothing here amends
the protocol, and nothing here may be cited as authority. Where it states a
measurement it also names the command that re-reads it, because a status sentence
in a document rots [R-DOC-02] and every number below was true only on the day it
was taken.

---

## 0. HOW TO USE THIS

Read `CLAUDE.md` first, then this. Then pick ONE numbered item from section 5 and
build it. Do not start two. Each item names its own acceptance test; an item is
finished when that test passes and not when the code looks right.

**Section 6 says which box each item repairs, roughly what it costs, and what to
run it on.** Read it before starting an item; its size and model columns are
ESTIMATES and say so.

**Re-verify before building.** Every figure in sections 3 and 5 carries the command
that produced it. Run the command. If it disagrees with this file, the command is
right and this file is stale — say so and carry on from the live number.

---

## 1. WHERE THIS SITS AGAINST THE STANDING PRIORITY

`CLAUDE.md` says the principal's number one priority is finishing the
fundamental-research framework, and that the characteristic failure of sessions in
this repo is drifting into adjacent work that is real, defensible, and not the
priority.

**This brief is adjacent work.** It was commissioned directly by the principal, so
it is not drift in the sense the rule guards against — but it does not advance the
framework's two adoption conditions either. If a session is ever choosing between
an item here and clearing a red gate that blocks
`engine/method_reassessment/criterion3.py`, the gate wins. Say so out loud rather
than quietly reordering.

One exception worth naming: **item 1 touches the lessons register**, which is part
of the fundamental framework's own machinery. It is the item most likely to earn
its place against the priority.

---

## 2. THE QUESTION THIS CAME FROM

The principal asked: *Testahil was improved — but is it SELF-improved, or does a
human have to effect every improvement?*

The honest answer, from reading the code rather than the claims: **Testahil is
broadly self-CORRECTING and narrowly self-IMPROVING.** Roughly 220 automated
checks across all three lenses catch the system's own mistakes and refuse to
publish. Exactly one loop changes its own behaviour without a person.

That distinction matters commercially. "Self-learning system" across all three
lenses would not survive a technical question. "The machine catches its own errors
and blocks itself" is true everywhere and is the stronger claim anyway.

---

## 3. THE AUDITED STATE — SIX BOXES

Rows are the three lenses. Columns are METHOD CHOICE (which approach won) and
INSIDE THE METHOD (how the winner keeps improving).

| | Method choice | Inside the method |
|---|---|---|
| **Monte Carlo** | HUMAN | **SELF** |
| **Technical** | HUMAN | MACHINE-POLICED (detects, does not fix) |
| **Fundamental** | HUMAN | HUMAN |

### 3.1 The one genuinely self-improving loop

`engine/auto_refresh.py` + `.github/workflows/testahil-calibration.yml`.

A CSV lands in `engine/raw_ohlc/{MARKET}/{TICKER}.csv` → data-quality gate →
panel rebuild → pooled (nu, width_cal) refit → **writes `market_profiles.py` in
place and pushes to `main`**. No pull request, no approval, material or not.

`auto_refresh.py:349` is the auto-commit path that rewrites the config. The
workflow runs `auto_refresh.py --apply` then `git push origin HEAD:main`.

The human approval gate was DELETED on 23-08-2026 and the reason is recorded in
`auto_refresh.py`'s own docstring: it had produced 66 unmerged review PRs and left
18 names running under no applied fit. The defect being guarded against — silence —
was attacked directly instead: a material change applies, and is announced in three
places (a `PENDING_REVIEW/` evidence file, the commit message, and the superseded
config stored under `superseded` in `fitted_configs.json`). `--halt-on-material`
restores the old behaviour.

**The carve-out.** `signal_active` — momentum on or off — is copied through
unchanged (`panel_refresh.py:549`). The machine refits its numbers; it never flips
its own switch.

### 3.2 What each box's human actually does

| Box | The human's actual verb | Why it is human |
|---|---|---|
| MC · method choice | Has a modelling idea, codes the variant, scores it against the carry-matched benchmark, edits the engine if it wins | **No candidate list.** Score and actuator both exist; nothing enumerates the options |
| MC · inside | Posts a CSV | *already SELF* |
| TECH · method choice | Designed the replay, the placebo, the bar | **No actuator.** Findings feed nothing downstream; there is no loop to close |
| TECH · inside | Re-runs the harvest when CI goes red on a hash mismatch | **No trigger.** Mechanical work, zero judgement, waiting on a person |
| FUND · method choice | Notices a defect, prices it, picks the replacement, rebuilds affected studies | **Genuinely human.** No score says "three lenses beat one" — the split IS the output |
| FUND · inside | Runs the walk-forward per name, drafts lessons, decides each scope | **No counter.** Scope is real judgement; the repeat trigger is never measured |

### 3.3 Commands that re-read the live state

```
python3 engine/method_reassessment/criterion3.py      # the framework's own blockers
grep -c '^\s*- name:' .github/workflows/*.yml | awk -F: '{s+=$2} END {print s}'   # 220 on 17-09-2026
python3 -c "import engine.site_data as sd; B=sd.read_object('BANDS'); \
  n=sum(v['n'] for v in B.values()); h=sum(v['hits'] for v in B.values()); \
  print(len(B),'names',n,'windows',round(100*h/n,1),'% in band')"
python3 -c "import importlib.util as u; s=u.spec_from_file_location('lr','engine/lessons_register.py'); \
  m=u.module_from_spec(s); s.loader.exec_module(m); L=m.LESSONS; \
  print(len(L),'lessons;',sum(1 for x in L if x.get('recurred')),'with recurred')"
```

---

## 4. THE PRINCIPLE

**A machine can improve what it can score. A human is needed where the score has
to be invented.**

Three tiers, and every box falls into one:

- **TUNE** — the parameter is fitted from data. Machine already.
- **CHOOSE** — the options are written down and a score exists. Machine, *provided
  the winner is confirmed on a holdout it was never tuned on*.
- **INVENT** — a new component, a new invariant, a new question. Human. But the
  *generalisation* of an invention across all 90 names is machine work.

Of the five human boxes, **four are human for an engineering reason** — no
trigger, no candidate list, no counter — not a research one. Only INVENT is
irreducible, and even there the human's job shrinks to discovery.

---

## 5. THE FIVE ITEMS, IN BUILD ORDER

### ITEM 1 — Instrument `recurred` · days · HIGHEST VALUE

**The problem.** The lessons page promises *"A mistake made once gets a note. A
mistake made twice gets a gate."* **That rule cannot currently fire.** Nothing in
the codebase ever writes the `recurred` field — it is only ever a hand-typed
argument to `L()` in `engine/lessons_register.py`.

**The evidence, as read 17-09-2026.** 305 lessons, `recurred` empty on all 305.
Yet SIX lessons describe a repeat in their own prose: **L-014, L-015, L-033,
L-036, L-096, L-282**. The page prints *0 made again* while six entries say in
words that they happened again. Re-verify:

```
python3 - <<'EOF'
import importlib.util as u
s=u.spec_from_file_location('lr','engine/lessons_register.py')
m=u.module_from_spec(s); s.loader.exec_module(m)
P=('headline','plain','evidence','source','correction','overturned_by')
W=('recurred','same species','happened again','made again','second time','twice now')
hits=[x for x in m.LESSONS if any(w in str(x.get(f,'')).lower() for f in P for w in W)]
print(len(m.LESSONS),'lessons;',sum(1 for x in m.LESSONS if x.get('recurred')),'with recurred;',
      len(hits),'whose prose admits a repeat:',[x['id'] for x in hits])
EOF
```

**What to build.** When a gate fails, fingerprint the failure and match it against
the lessons already in the register. On a match, increment that lesson's
`recurred` automatically with the date and the gate that caught it.

**The machinery already exists — do not rebuild it.** `engine/ratchet_shape.py`
`fingerprint(msg)` returns *"the CLAIM a failure message makes, with every live
figure removed"* [R-ENF-08]. That is exactly the matcher this needs. Lessons will
need a signature field or a derived one; prefer deriving from existing prose over
asking anyone to re-type 305 entries.

**Acceptance test.** Inject a failure whose shape matches a known lesson; the
lesson's `recurred` grows by one entry naming the date and the gate; the lessons
page rebuilds and prints a count above zero; and a failure that does NOT match any
lesson increments nothing. Both halves are required — a matcher that matches
everything is worse than none [R-ENF-04].

**Traps.** (a) `engine/lessons_register.py` is the SOURCE; `Lessons_Register.md`,
`.docx` and `lessons.html` are GENERATED — never hand-edit the outputs. (b) The
six named lessons above are a backlog: decide explicitly whether to backfill them
or to bind forward only, and say which. (c) Do not let the counter promote a
lesson to a gate on its own — the promotion is still a decision.

---

### ITEM 2 — Auto-heal the technical record · days · LOWEST RISK

**The problem.** `engine/tech_records.json` stores the sha256 of `technicals.py`
as harvested. When the read changes, `scripts/check_tech_calibration.py` goes RED
— correctly — and then waits for a person to re-run the harvest and commit. That
re-run involves no judgement whatsoever.

**What to build.** The job that detects the divergence runs the fix and commits.
Entry point is `python3 engine/tech_record.py`; the CI step is *"Technical
calibration gate"* in `.github/workflows/study-provenance.yml:494`. The pattern to
copy is `auto_refresh.py` — apply, announce in the commit message, never silently.

**THE TRAP THAT WILL BITE YOU.** `tech_record.py`'s `__main__` reads a cached
claims frame from `engine/lab/ta_calibration/claims_short.pkl` when it exists and
passes it to `build(claims=...)`, which then does NOT re-harvest. If
`technicals.py` has changed, that cache holds the OLD read's claims — so a naive
auto-heal would stamp the NEW hash onto the OLD grades and turn the gate green
while making it a lie. **The auto-heal must invalidate the cache and re-harvest
through `technicals.compute()`.** Add a check that the cache's provenance matches
the current read hash, or delete it unconditionally before rebuilding.

**Acceptance test.** Change a constant in `technicals.py`. CI goes red, re-harvests,
commits, and goes green — and the committed `tech_records.json` records grades that
actually differ from the previous ones where the change should have moved them. A
green light with identical grades means the cache trap fired.

---

### ITEM 3 — Sweep every new invariant across the whole book · weeks

**The problem.** We find a defect on one company, fix that company, and the other
89 go into a queue that a person has to work. The pattern is proven — see
`engine/build_depth_audit/outstanding.json`, which still carries **8 names**
queued from the single Fertiglobe beta discovery (seeded 23-08-2026). Proven, but
manual.

**What to build.** When an invariant is added (`assert_beta_provenance`,
`ke_reproduction`, `asset_base`, and their successors), it runs against all 90
names on the next push and produces a machine-readable failure list, not a memory.

**Acceptance test.** Add a deliberately failing invariant; every affected name
appears in the list with the reason; removing it empties the list. An empty result
must be distinguishable from an unrun one [R-ENF-04].

---

### ITEM 4 — The Monte Carlo component bake-off · weeks to months

**The problem.** A person has to think of the variant. Everything downstream of
that thought is already automatic.

**What to build.** Declare the engine's components as an explicit registry —
drift ∈ {carry, carry+signal, zero}, width ∈ {trailing-252, YZ-HAR, YZ-HAR-shrunk},
shape ∈ {Gaussian, t(ν fitted), …}, signal ∈ {mom_12_1, rev_1m, mom_combo, none} —
run the cross-product walk-forward, and adopt a winner automatically.

**Folding `signal_active` into the grid closes the carve-out in 3.1.**

**THE RISK, AND IT IS THE WHOLE ITEM.** Run 48 variants and one will beat the
incumbent by luck. The existing bars — robust across bootstrap blocks {2,3,4},
leave-one-name-out, calendar split-half — were built for ONE comparison, not for a
search. **A winner must additionally clear a pre-registered holdout it was never
tuned on.** Pre-register the grid and the holdout period BEFORE running, in a
committed file, so the holdout cannot be chosen after seeing the results. Without
that, this item manufactures false confidence and is worse than not building it.

**Acceptance test.** Seed the grid with a variant known to be junk; it must not
win. Then confirm the incumbent survives its own bake-off — if the current engine
loses to something on the in-sample score but not on the holdout, the holdout is
doing its job and that is the result to report.

---

### ITEM 5 — Technical: decide the actuator BEFORE building the loop · a decision, not code

**The problem.** The technical lens is measured with real care — 89,190 graded
claims across 92 libraries, 2011→2026, every published level scored against a
distance-matched placebo — and the findings then **feed nothing**. They render
nowhere. There is no downstream, so there is no loop to close and nothing to
automate.

**What is needed first.** A ruling from the principal: *what is a technical finding
allowed to change?* The read itself? The published levels? The wording only?
Nothing? Until that is answered, a parameter bake-off (cluster tolerance,
lookbacks, MA lengths) optimises toward a target that does not exist.

**Note the constraint.** [R-LENS-01] stands: no output of one lens is an input to
another. Whatever actuator is chosen must live inside the technical lens.

---

## 6. RUNNING THEM — WHICH BOX, HOW BIG, WHAT TO RUN IT ON

Three tables. The first is fact; the second and third are ESTIMATES and are
labelled as such — treat them the way this repository treats any unmeasured
figure.

### 6.1 Which item repairs which box

One item per box, and item 4 does double duty.

| Matrix box | Item | What it does there |
|---|---|---|
| **MC · method choice** | **4** | Builds the bake-off — the candidate list that box is missing |
| **MC · inside** | **4** | Box is already SELF; item 4 only closes the `signal_active` carve-out |
| **TECH · method choice** | **5** | Supplies the actuator. A ruling from the principal, not code |
| **TECH · inside** | **2** | Supplies the trigger — the job that detects also fixes |
| **FUND · method choice** | **3** | Sweeps each discovered defect across all 90 names |
| **FUND · inside** | **1** | Supplies the counter — `recurred` |

Read the other way: **1 → FUND·inside, 2 → TECH·inside, 3 → FUND·method,
4 → MC·both, 5 → TECH·method.** THE BUILD ORDER IS NOT MATRIX ORDER — the
matrix is organised by lens and the order is by value ÷ effort, so it starts at
the bottom-right cell and works back. The two boxes it reaches last are the two
hardest: the bake-off because the statistics are genuinely difficult, and the
technical actuator because it waits on a person rather than on work.

### 6.2 Relative size — ESTIMATED, NOT MEASURED

| Item | Relative size | Why |
|---|---|---|
| **2 · auto-heal tech record** | **1× (baseline)** | One workflow step, one entry point, one named trap. The smallest real unit of work here |
| **1 · instrument `recurred`** | **2–3×** | Schema change, matcher, negative control, page rebuild — but the matcher already exists |
| **3 · sweep invariants** | **4–6×** | Touches all 90 names; more iterations against gates |
| **4 · MC bake-off** | **10–20×** | Pre-registration, component registry, cross-product runs, and the statistical judgement about whether a winner is real |
| **5 · technical actuator** | **0** | A decision, not a session |

**THE COST DRIVER IN THIS REPOSITORY IS THE CONTEXT, NOT THE CODE.** `CLAUDE.md`
plus the ~55,000-character digest is read before any work starts, and the gate
suite is 220 steps. Items 1–3 are small edits wrapped in a large read-and-verify
cycle, which is why item 2 is not much cheaper than item 1 despite being simpler.

**CALIBRATE ON ITEM 2 RATHER THAN TRUSTING THIS COLUMN.** Run item 2 first, read
the session's own usage before and after, and multiply. One measurement replaces
the whole table — which is this repository's standing preference and the reason
these figures are labelled rather than quoted.

### 6.3 What to run each item on — as at 17-09-2026

| Item | Model | Effort | Why |
|---|---|---|---|
| **1 · instrument `recurred`** | `claude-opus-5` | **xhigh** | Well specified, acceptance test written, matcher already exists |
| **2 · auto-heal tech record** | `claude-opus-5` | **high** | Smallest item, proven pattern to copy, and its one trap is named below |
| **3 · sweep invariants** | `claude-opus-5` | **xhigh** | Multi-file, touches 90 names, needs care about population anchoring |
| **4 · MC bake-off** | `claude-fable-5-1`, or `claude-opus-5` at **max** | **max** | The only genuinely hard one — multiple testing, holdout design, judging whether a winner is real. Correctness matters more than cost |
| **5 · technical actuator** | — | — | A ruling, not a coding session |

Two standing points rather than preferences: long-horizon agentic work runs at
high or xhigh **with the full task spec given up front**, which is what this
document is for — point the session at this path in its first message rather
than drip-feeding it; and DO NOT DOWNGRADE THE MODEL TO SAVE COST on items 1–3,
which is a decision for the principal and not a default.

**THIS TABLE HAS A SHELF LIFE.** Model availability, effort levels and prices
move, and a recommendation is a claim about the world that rots [R-DOC-02].
Re-read the current guidance rather than this table before starting an item.

---

## 7. RULES THAT BIND ANY OF THIS WORK

- **[R-ENF-03]** one implementation, not two. Replay the shipped code; never
  re-implement it for testing. A replay that re-derives is scoring a different
  thing.
- **[R-ENF-04]** an empty result is not a clean result. Every new gate needs a
  negative control proving it can go red.
- **[R-ENF-01]** a self-attested boolean is never a check. Gates run over
  committed artefacts, from outside the builders.
- **[R-LENS-01]** no cross-lens feeding, in either direction.
- **Import, not parse.** Every module a commit relies on is verified by import
  (`nu=Gaussian` parses cleanly and only dies at import — that exact bug reached
  `main` once).
- **Generated files are never hand-edited.** `Lessons_Register.md/.docx`,
  `lessons.html`, `fitted_configs.json`, `Fundamental_Calibration_FV_Register.md`,
  `Technical_Lessons_Register.docx`.
- Any new standing rule goes into BOTH governing documents in the same commit, and
  the digest's full text is returned to the principal in chat.

---

## 8. OPEN ITEMS FOUND DURING THE AUDIT

Not part of the five, but found while reading and worth someone's attention.

1. **Stale header on the one autonomous loop.**
   `.github/workflows/testahil-calibration.yml` lines 6-11 still describe the
   pre-23-08-2026 behaviour — *"opens a PR … nothing merges without a human
   clicking merge"* — while the file below runs `--apply` and pushes to `main`.
   Doc rot on the single most important comment in the repo. One-line fix.

2. **A mislabelled row on the technical self-learning slide.** The row headed *"A
   fresh trigger beats an old one"* carries the RESISTANCE-TRIGGER numbers
   (6,076 firings, 24.4% vs 29.7% — a real level cleared versus an invented one).
   Fresh-versus-old is the GOLDEN CROSS finding (3,024 fresh crosses, 52.2% versus
   54.8% for an established one). The heading should read roughly *"Breaking
   resistance opens the next target."*

3. **`assets/editions.json` is missing SWDY's 13-09 edition**, so the archive page
   labels the superseded 05-08-2026 study as "Latest". 89 of 90 names are correct.
   A gate that stops a superseded edition falling out of the archive would close
   the class rather than the instance.

---

## 9. THE ONE-LINE SUMMARY

Four of the five human boxes are human because of a missing trigger, a missing
candidate list, or a missing counter — engineering gaps, not research ones. Items
1 and 2 are days of work each and would take the honest count from one
self-improving cell to three.
