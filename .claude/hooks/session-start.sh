#!/bin/bash
#
# TESTAHIL — SessionStart hook.
#
# TWO JOBS, AND IT MUST NEVER DO A THIRD.
#
#   1. INSTALL WHAT THIS CONTAINER SHIPS WITHOUT.  The remote container has no
#      numpy, pandas, scipy or python-docx, and no node_modules — so every
#      session begins by installing them by hand. On 01-Sep-2026 the operator's
#      own prompt had to carry a "Setup first: pip install ..." line to get the
#      campaign started, and scripts/check_ta_chart_overlay.js could not run at
#      all until npm install was done mid-session. Neither belongs in a person's
#      instructions: a written reminder to do what a machine can do is the
#      species of defect [R-ENF-01] exists to close. The package list here is
#      the one .github/workflows installs, so a session and CI cannot drift.
#
#   2. REPORT THE CAMPAIGN'S POSITION AND ITS GATES.  Both campaign gates anchor
#      on the run directories on disk, so a chat that created
#      engine/{tk}_walkforward/ and stopped before registering a lesson leaves
#      them RED — correctly, and invisibly until someone pushes. This prints that
#      state as the first thing in the next session instead.
#
# WHAT IT IS NOT.  It is a smoke alarm, not a lock. It cannot finish a run, and
# it cannot make the scope judgement — ALL / CLASS / STOCK is a decision with a
# cost in both directions and lessons_add.py refuses anything unconfirmed by
# design. ENFORCEMENT STAYS IN CI. This only moves discovery earlier.
#
# AND IT NEVER BLOCKS A SESSION. A red gate is information, not a reason to
# refuse to start work — an unclearable gate is the failure [R-CAL-01] was
# amended to close. So: no `set -e`, every command tolerated, exit 0 always.

set -uo pipefail

cd "${CLAUDE_PROJECT_DIR:-$(dirname "$(dirname "$(dirname "$(readlink -f "$0")")")")}" || exit 0

# ---------------------------------------------------------------------------
# 1 — dependencies, in the remote container only. A local checkout has its own
#     environment and this hook has no business reinstalling into it.
# ---------------------------------------------------------------------------
if [ "${CLAUDE_CODE_REMOTE:-}" = "true" ]; then
  python3 -c "import numpy, pandas, scipy, docx" 2>/dev/null \
    || pip install --quiet --disable-pip-version-check \
         numpy pandas scipy python-docx >/dev/null 2>&1
  [ -d node_modules ] || npm install --silent --no-audit --no-fund >/dev/null 2>&1
fi

python3 -c "import numpy, pandas, scipy, docx" 2>/dev/null \
  && echo "deps: numpy pandas scipy python-docx OK" \
  || echo "deps: MISSING — run: pip install numpy pandas scipy python-docx"

# ---------------------------------------------------------------------------
# 2 — where the campaign is, and whether the last session left it clean.
#     Each gate prints one line when green and its own FAIL lines when not.
# ---------------------------------------------------------------------------
echo
echo "── TESTAHIL campaign ──────────────────────────────────────────────"

python3 engine/campaign_queue.py --next 2>&1 | sed 's/^/  /' \
  || echo "  queue: could not be read"

gate () {          # $1 = label, $2... = command
  local label="$1"; shift
  local out rc
  out="$("$@" 2>&1)"; rc=$?
  if [ "$rc" -eq 0 ]; then
    printf '  %-18s OK\n' "$label:"
  else
    printf '  %-18s NEEDS ATTENTION\n' "$label:"
    # Catch the header AND the bullet lines under it. The first cut matched only
    # /FAIL|FATAL/ and printed "FAILED — 3 problem(s):" while naming none of the
    # three — a report that counts a defect and hides it is the same species as
    # the empty result that reads as a clean one [R-ENF-04]. Capped so a badly
    # broken tree cannot flood the session's first message.
    printf '%s\n' "$out" | grep -E "FAIL|FATAL|^[[:space:]]*- " \
      | head -12 | sed 's/^[[:space:]]*/      /'
  fi
}

gate "lessons register" python3 scripts/check_lessons_register.py
gate "fair-value record" python3 engine/fv_movement.py check
gate "parked names"     python3 scripts/check_campaign_parked.py

echo "───────────────────────────────────────────────────────────────────"
echo "  A red gate above is a half-finished run, not a broken repo:"
echo "  harvest the lessons and record the fair value for the name named."

exit 0
