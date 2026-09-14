"""Does the forecasting method beat doing nothing?  [R-FCAL-01]

THE RULE ALREADY DEMANDS THIS AND NOTHING WAS ASKING IT BOOK-WIDE. [R-FCAL-01]
says in terms: "A METHOD THAT CANNOT BEAT 'NO CHANGE' HAS NOT EARNED THE PRECISION
IT DISPLAYS — that is not a figure of speech and where it happens the study says
so." Each run scores its own two naive benchmarks and reports its own answer. No
instrument pooled them, so the question was answered five times and never once.

WHY IT WAS ASKED. A route out of the reassessment proposed INVERTING THE FLAT-LINE
DEFAULT — project every driver on its own measured history and require a mechanism
to hold it still — on the reasoning that a discipline of holding rates flat, in an
economy growing and inflating at Egyptian rates, is a forecast of decline. That is
a hypothesis about which of three constructions forecasts best, and all three are
already scored. It should be read before it is adopted, not after.

FOUR SCORE SHAPES, NOT ONE, AND THAT IS THE READ'S OWN TRAP. The five runs write
their benchmark comparison four different ways — detail.skill with mae/mae_bench,
drivers[d].skill_vs_* with mae/mae_bench, the same with model_mae/bench_mae, and a
detail keyed setting|driver|scope. A first cut handled two of them and scored EGCH
0 of 14 on a key-name difference alone, which reads exactly like a run whose model
never beats anything. PHDC commits NO benchmark at all and is REPORTED ABSENT
rather than counted as a loss: a run that does not score the benchmark has not lost
to it [R-ENF-04].

MAE IS NOT THE MEASURE THAT MATTERS HERE AND THE MODULE SAYS SO WHEREVER IT PRINTS
ONE. MAE is a precision measure; a five-year discounted cash flow INTEGRATES the
drift and averages out the noise, so what reaches a valuation is BIAS. A method
with slightly worse MAE and no bias produces better valuations than one with
tighter MAE that leans. Only one of the five runs commits a per-setting BIAS in a
readable shape, so the direction question — the one the whole reassessment is
about — is answerable on one name of five. That absence is the finding, printed
rather than worked around.

Read it live. Nothing quotes a figure from it.
"""
from __future__ import annotations

import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.dirname(HERE)


def _mae_pair(v):
    """(model, benchmark) out of whichever key names this run happens to use."""
    if not isinstance(v, dict):
        return None, None
    m = v.get("mae") if v.get("mae") is not None else v.get("model_mae")
    b = v.get("mae_bench") if v.get("mae_bench") is not None else v.get("bench_mae")
    return m, b


def read(path):
    """[(driver, mae_model, mae_freeze, mae_trend)] in whichever shape this run wrote."""
    j = json.load(open(path, encoding="utf-8"))
    out = []

    det = j.get("detail")
    sk = det.get("skill") if isinstance(det, dict) else None
    if isinstance(sk, dict) and sk:
        for d, v in sk.items():
            m, f = _mae_pair(v.get("vs_freeze"))
            _, t = _mae_pair(v.get("vs_trend"))
            if m is not None:
                out.append((d, m, f, t))
        if out:
            return out, "detail.skill"

    drv = j.get("drivers")
    if isinstance(drv, dict) and drv and isinstance(next(iter(drv.values())), dict) \
            and "skill_vs_freeze" in next(iter(drv.values())):
        for d, v in drv.items():
            m, f = _mae_pair(v.get("skill_vs_freeze"))
            _, t = _mae_pair(v.get("skill_vs_trend"))
            if m is None:
                m = (v.get("overall") or {}).get("mae")
            if m is not None:
                out.append((d, m, f, t))
        if out:
            return out, "drivers[].skill_vs_*"

    if isinstance(det, dict) and any("|" in k for k in det):
        acc = {}
        for k, v in det.items():
            parts = k.split("|")
            if len(parts) == 3 and parts[2] == "all":
                acc.setdefault(parts[1], {})[parts[0]] = v.get("mae")
        for d, v in acc.items():
            if v.get("asknown") is not None:
                out.append((d, v["asknown"], v.get("freeze"), v.get("trend")))
        if out:
            return out, "detail[setting|driver|scope]"

    return [], None


def bias(path):
    """{setting: (mean bias, n)} where a run commits it — most do not."""
    j = json.load(open(path, encoding="utf-8"))
    det = j.get("detail")
    if not (isinstance(det, dict) and any("|" in k for k in det)):
        return {}
    acc = {}
    for k, v in det.items():
        parts = k.split("|")
        if len(parts) == 3 and parts[2] == "all" and v.get("bias") is not None:
            acc.setdefault(parts[0], []).append(v["bias"])
    return {s: (sum(x) / len(x), len(x)) for s, x in acc.items()}


def report():
    paths = sorted(glob.glob(os.path.join(ENGINE, "*_walkforward", "scores.json")))
    if not paths:
        raise SystemExit("REFUSED: no run committed a scores.json. An empty census "
                         "is not a clean census [R-ENF-04].")
    print("DOES THE METHOD BEAT DOING NOTHING?  [R-FCAL-01]\n")
    print("  freeze = every line flat at the last actual.  trend = the trailing")
    print("  three-year growth rate carried forward.  Both are the run's own.\n")
    print("  %-7s %8s %14s %14s %10s %9s %9s"
          % ("name", "drivers", "beats FREEZE", "beats TREND", "MAE model",
             "freeze", "trend"))
    tot = [0, 0, 0, 0.0, 0.0, 0.0]
    absent, shapes = [], {}
    for p in paths:
        tk = os.path.basename(os.path.dirname(p)).replace("_walkforward", "").upper()
        rows, shape = read(p)
        if not rows:
            absent.append(tk)
            continue
        shapes[tk] = shape
        n = len(rows)
        bf = sum(1 for _, m, f, _ in rows if f is not None and m < f)
        bt = sum(1 for _, m, _, t in rows if t is not None and m < t)
        mm = sum(m for _, m, _, _ in rows) / n
        mf = ([f for _, _, f, _ in rows if f is not None] or [0])
        mt = ([t for _, _, _, t in rows if t is not None] or [0])
        print("  %-7s %8d %10d/%-3d %10d/%-3d %10.3f %9.3f %9.3f"
              % (tk, n, bf, n, bt, n, mm, sum(mf) / len(mf), sum(mt) / len(mt)))
        tot[0] += n; tot[1] += bf; tot[2] += bt
        tot[3] += mm * n; tot[4] += sum(mf); tot[5] += sum(mt)
    if not tot[0]:
        raise SystemExit("REFUSED: no run committed a readable benchmark comparison. "
                         "That is an unread question, not a passed one [R-ENF-04].")
    print("  %-7s %8d %10d/%-3d %10d/%-3d %10.3f %9.3f %9.3f"
          % ("POOLED", tot[0], tot[1], tot[0], tot[2], tot[0],
             tot[3] / tot[0], tot[4] / tot[0], tot[5] / tot[0]))
    for tk in absent:
        print("\n  %-7s NO BENCHMARK IN ITS SCORES — reported absent, never counted "
              "as a loss" % tk)

    print("\n  the method beats HOLDING EVERYTHING FLAT on %d of %d drivers (%.0f%%)"
          % (tot[1], tot[0], 100 * tot[1] / tot[0]))
    print("  the method beats a TRAILING THREE-YEAR TREND on %d of %d (%.0f%%)"
          % (tot[2], tot[0], 100 * tot[2] / tot[0]))

    print("\n  AND THE DIRECTION, WHICH IS WHAT A VALUATION INTEGRATES:")
    any_bias = False
    for p in paths:
        tk = os.path.basename(os.path.dirname(p)).replace("_walkforward", "").upper()
        b = bias(p)
        if not b:
            continue
        any_bias = True
        f = lambda s: ("%+.4f (%d)" % b[s]) if s in b else "—"
        print("    %-7s model %s   freeze %s   trend %s"
              % (tk, f("asknown"), f("freeze"), f("trend")))
    if not any_bias:
        print("    NO RUN commits a per-setting bias in a readable shape.")
    print("    THE OTHER RUNS COMMIT MAE FOR THE BENCHMARKS AND NOT BIAS, so the")
    print("    question the whole reassessment is about — does the method reduce the")
    print("    DIRECTIONAL error against doing nothing — is answerable on the names")
    print("    above and nowhere else. That is a gap in what the runs commit, of the")
    print("    same class the valuation-input block closed, and it is printed rather")
    print("    than worked around.")
    return tot


if __name__ == "__main__":
    report()
