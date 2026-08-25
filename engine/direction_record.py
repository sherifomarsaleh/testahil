"""direction_record.py — the per-name direction ledger, computed from the LEDGER.

[R-DRIFT-01] says every covered name's forecast states a direction call and every
call is graded at its maturity; [R-ENF-01] says a rule that can be checked must be
checked from outside the thing it governs. This is that check for the direction
record: it reads assets/data.js (the published ledger — never a side copy),
takes every GRADED row that carries a recorded signal_z, scores the call —
UP/DOWN by the sign of the stock's own momentum z at strike, WEAK-flagged inside
the dead zone but still a call — against the realized close vs the anchor, and
prints the per-name and pooled hit record. Nothing here re-derives a call:
signal_z was frozen at strike by strike_cohorts/rollforward_one, and grading
appended the outcome. This script only joins the two, so it can be run at every
grading pass and by the standing out-of-cycle review.

Usage:  python3 engine/direction_record.py            # pooled + per-name table
        python3 engine/direction_record.py --json     # machine-readable
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_JS = os.path.join(os.path.dirname(HERE), "assets", "data.js")
DEAD_ZONE = 0.25          # matches the socket knob: |z| < dead -> WEAK (tilt 0), still a call


def load_ledger():
    out = subprocess.run(
        ["node", "-e",
         "const fs=require('fs'),vm=require('vm');"
         "let s=fs.readFileSync(process.argv[1],'utf8');"
         "s+='\\n;globalThis.__L=LEDGER;';const c={window:{}};"
         "vm.createContext(c);vm.runInContext(s,c);"
         "console.log(JSON.stringify(c.__L));",
         DATA_JS], capture_output=True, text=True, check=True)
    return json.loads(out.stdout)


def record(rows):
    scored, pending = [], 0
    for r in rows:
        z = r.get("signal_z")
        if z is None:
            continue                     # struck before the committed-drift adoption
        if r.get("realized_close") is None:
            pending += 1
            continue
        call = "UP" if z > 0 else ("DOWN" if z < 0 else "FLAT")
        realized = "UP" if r["realized_close"] > r["anchor_price"] else (
            "DOWN" if r["realized_close"] < r["anchor_price"] else "FLAT")
        scored.append(dict(
            instrument=r["instrument"], horizon=r.get("horizon_label"),
            anchor_date=r.get("anchor_date"), grade_date=r.get("grade_date"),
            z=round(float(z), 3), weak=abs(float(z)) < DEAD_ZONE,
            call=call, realized=realized, hit=call == realized))
    return scored, pending


def main():
    rows = load_ledger()
    scored, pending = record(rows)
    if "--json" in sys.argv:
        print(json.dumps(dict(scored=scored, pending_calls=pending), indent=1))
        return
    n_call = sum(1 for r in rows if r.get("signal_z") is not None)
    print(f"ledger rows: {len(rows)} | rows carrying a recorded call: {n_call} | "
          f"calls graded: {len(scored)} | calls still open: {pending}")
    if not scored:
        print("No graded calls yet — the first strikes that carry a call mature "
              "at their own grade dates; the record accrues from there. "
              "(Rows graded so far were struck before the committed-drift adoption.)")
        return
    hits = sum(s["hit"] for s in scored)
    strong = [s for s in scored if not s["weak"]]
    print(f"pooled: {hits}/{len(scored)} calls right "
          f"({hits/len(scored):.0%}); strong calls (outside the dead zone): "
          f"{sum(s['hit'] for s in strong)}/{len(strong)}")
    per = {}
    for s in scored:
        per.setdefault(s["instrument"], []).append(s)
    print(f"{'name':14s}{'graded':>7s}{'right':>6s}{'strong right':>13s}")
    for name in sorted(per):
        g = per[name]
        st = [s for s in g if not s["weak"]]
        print(f"{name:14s}{len(g):7d}{sum(s['hit'] for s in g):6d}"
              f"{(str(sum(s['hit'] for s in st)) + '/' + str(len(st))) if st else '—':>13s}")


if __name__ == "__main__":
    main()
