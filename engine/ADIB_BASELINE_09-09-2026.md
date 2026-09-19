# ADIB — the pre-campaign fair value, preserved outside the register

**09-09-2026 · internal · nothing here reaches the live site**

A fundamental walk-forward on ADIB (EGX, ADIB-Egypt) was started this evening. The
run directory was created before the baseline was frozen, which is the wrong order:
[R-FCAL-01] and the campaign prompt both require `fv_movement.py snapshot` FIRST,
because the rebuild is the one sanctioned thing that moves `TICKERS.ADIB.fair` and
`assets/data.js` carries no date or standard stamp — so a baseline taken afterwards
is a fabricated zero rather than a measurement.

**The loss had not happened.** `assets/data.js` still carried the pre-campaign
numbers and the run directory held only downloaded filings, so the old fair value
was recovered intact and is written down here:

| field | value |
|---|---|
| bear | 31.6 |
| base | 54.3 |
| full | 95.3 |
| currency | EGP |
| fairAsof (the close the fair value is struck on, per the study) | 2026-07-01 |
| spot carried in data.js | 54.40, close 23 Aug 2026 |
| built to | delivered 03-07-2026; no engine directory |

## Why this is a note and not a register entry

The baseline WAS frozen into `fv_movement.json` the moment the risk was seen, and it
was then **withdrawn**, because committing it would have made the register red on
every other checkout for a reason that is not a defect: `engine/adib_walkforward/`
contains only `filings/`, which `.gitignore` excludes, so the run directory exists on
this machine and on no other. `fv_movement.py check` anchors on the run directories
on disk, so a committed baseline with no committed run behind it reads exactly like
the KABO failure of earlier this session — *"carries a record with no walk-forward run
directory behind it"*. That entry was withdrawn rather than the check weakened, and
the same answer applies here.

**The check is right both times.** A baseline is a claim that a run is under way, and
a run nobody else can see is not a run. What the rule protects is the NUMBER, and the
number is protected here.

## What the next session does

Re-freeze it when the run has something committed behind it:

    python3 engine/fv_movement.py snapshot ADIB

If `assets/data.js` has by then been rewritten with a new ADIB fair value, that
command will capture the NEW number as though it were the old one, which is the
fabricated zero the rule exists to stop. In that case take the baseline from the
table above instead, and say in the register entry that it came from this note.

## The ordering fault itself

Recorded rather than tidied away: the run was begun before the snapshot. The
instruction given to the runner did say to snapshot first, so this is not a gap in the
instruction. It is worth knowing that the campaign's own gates caught it within
minutes — `fv_movement.py check` and `build_publish_queue.py --check` both fired, and
they fired while the number was still recoverable, which is the whole design.
