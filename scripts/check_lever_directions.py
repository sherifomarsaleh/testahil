#!/usr/bin/env python3
"""THE SENSITIVITY SLIDERS MUST MOVE THE ANSWER THE WAY THE STUDY SAYS THEY DO.

Enforced per [R-ENF-01]; read through a real parse per [R-ENF-03]; population-anchored
per [R-ENF-04]; ratcheted per [R-ENF-02].

The defect. On 13-Sep-2026 a reader dragged the beta slider on the ADNOCLS page to the
top of the measured 90% interval and watched the fair value go UP, from AED 7.05 to 8.43.
A higher beta is a higher cost of equity and a lower present value; there is no
construction in this house where it is not. The lever's own caption said so in words --
"regressing against an equal-weight composite ... gives 0.71 and LIFTS the cash-flow
value from AED 6.40 to 9.37" -- while the number beside it, impact:34.4, did the
opposite. The magnitude had been sized correctly off the study's published variants and
then shipped with the wrong sign.

Nothing caught it. check_page_integrity.py parses every one of these pages and was green
on all 93 the same morning: it checks the markup and the static tables, and a lever is
neither. The panel is JavaScript that runs in the reader's browser, so no gate in this
repository had ever read what it computes. A number that only exists after a drag is
still a published number.

Three more of the same class fell out of the first sweep, none of them known: MODON's
beta lever (+1.0, also inverted, and so small it moved the answer 0.65% across its whole
range on a study whose own text calls beta "THE lever ... that flipped the verdict"),
MODON's terminal cost of capital (+0.55, inverted), and ELEC's net-debt anchor
(+0.00030, inverted).

WHERE THE LEVERS LIVE [MOVED 13-Sep-2026]. They were typed inside the 93 ticker pages,
one copy each. They now live in assets/levers.js and the pages read it. That move is why
this gate reads ONE file through a real JavaScript evaluation instead of regexing
markup -- and why it also holds the pages to the move: a page that carries a lever of its
own again has re-created the 93 copies this file exists to end.

What this gate holds the book to:

  1. direction      -- for a lever whose variable IS a discount rate (beta, cost of
                       capital, cost of equity, WACC, required return), the rate quoted
                       at each end of its own slider decides the sign: if the rate at
                       `hi` is above the rate at `lo`, impact must be negative, and the
                       reverse. This reads the lever's own labels rather than its name,
                       which is what keeps the five CBE-EASING levers green -- their
                       sliders run from today's money to a LOWER rate, so a positive
                       impact is correct there and a name-matching gate would have
                       called all five wrong.
  2. inert-lever    -- impact of exactly zero cannot move the answer at all. Zero is not
                       a small number here, it is a lever that does nothing while
                       presenting as one.
  3. unverifiable   -- a discount-rate lever whose own labels carry neither a rate nor a
                       direction FAILS rather than being skipped. A silent skip is how
                       check_artefact_currency carried three holes for a month.
  4. page wiring    -- every study page loads assets/levers.js, names a key that exists
                       in it, and carries no inline lever array of its own.

Magnitude is reported and NEVER gated. Across the 463 levers on the book the full-slider
effect runs from 0.28% to 260% with no gap anywhere in it, so any cutoff would be a free
parameter with no out-of-sample evidence, which the PROMOTION RULE forbids. What is
printed is the advisory list; what fails the build is direction and wiring.

    python3 scripts/check_lever_directions.py
    python3 scripts/check_lever_directions.py --prune
"""
import glob
import json
import math
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEVERS_JS = os.path.join(ROOT, "assets", "levers.js")
OUTSTANDING_FILE = os.path.join(ROOT, "engine", "build_depth_audit", "lever_outstanding.json")

# a lever whose slider variable IS a discount rate: raise it, the value falls
RATE_NAME = re.compile(r"beta|cost of capital|cost of equity|discount rate|wacc|required return", re.I)

# "90% interval", "95% confidence" and friends describe the MEASUREMENT, not the rate at
# that end of the slider
NOT_A_RATE = re.compile(r"\b(\d+(?:\.\d+)?)\s*%\s*(interval|range|confidence|ci\b)", re.I)
PERCENT = re.compile(r"(-?\d+(?:\.\d+)?)\s*%")
NUMBER = re.compile(r"(-?\d+(?:\.\d+)?)")

# Some rate sliders are labelled in words rather than in basis points. The list is
# deliberately short and explicit: a word is here only because a page uses it to mean one
# direction of the policy rate and nothing else. Guessing from a longer vocabulary would
# be a gate inventing an interpretation the page never stated.
RATE_DOWN = re.compile(r"\beas(?:e|ier|ing)\b|\btailwind\b|\bcut(?:s)?\b|\bdovish\b", re.I)
RATE_UP = re.compile(r"\btighter\b|\btightening\b|\bheadwind\b|\bhike(?:s)?\b|\bhawkish\b", re.I)

# a page carrying a lever of its own again
INLINE_LEVER = re.compile(r"renderFairLevers\([^)]*\[\s*\{\s*name\s*:", re.S)

# levers.js is READ THROUGH A REAL JAVASCRIPT EVALUATION, never a regular expression
# [R-ENF-03]. fmt is a function and does not survive JSON, so it is reduced here to what
# it prints at four probe positions -- enough for a reader to see the prose and for a
# later check to compare it, without pretending a function is data.
DUMP_JS = r"""
const fs = require('fs'), vm = require('vm');
const src = fs.readFileSync(process.argv[1], 'utf8');
const ctx = {}; vm.createContext(ctx);
vm.runInContext(src + ';globalThis.__L = LEVERS;', ctx);
const out = {};
for (const tk of Object.keys(ctx.__L)) {
  out[tk] = ctx.__L[tk].map(l => {
    const probe = {};
    if (typeof l.fmt === 'function') {
      for (const [k, v] of [['def', l.def], ['min', l.min], ['max', l.max]]) {
        try { probe[k] = String(l.fmt(v)); } catch (e) { probe[k] = 'ERR:' + e.message; }
      }
    }
    return {name: l.name, min: l.min, max: l.max, step: l.step, def: l.def,
            impact: l.impact, lo: l.lo, hi: l.hi,
            has_fmt: typeof l.fmt === 'function', probe: probe};
  });
}
process.stdout.write(JSON.stringify(out));
"""


def load_levers():
    """assets/levers.js, evaluated. Raises rather than returning a half-read book."""
    if not os.path.exists(LEVERS_JS):
        raise RuntimeError("assets/levers.js does not exist — the levers have no home")
    try:
        p = subprocess.run(["node", "-e", DUMP_JS, LEVERS_JS],
                           capture_output=True, text=True, timeout=120)
    except FileNotFoundError:
        raise RuntimeError(
            "node is not on PATH. This gate evaluates assets/levers.js rather than "
            "regexing it [R-ENF-03], so it cannot run without node — and it refuses "
            "rather than reporting a book it did not read.")
    if p.returncode != 0:
        raise RuntimeError("assets/levers.js did not evaluate:\n%s" % p.stderr.strip()[:2000])
    return json.loads(p.stdout)


def rate_at(label):
    """The rate this end of the slider stands for, read off the lever's own label."""
    if not label:
        return None
    cleaned = NOT_A_RATE.sub(" ", label)
    pct = PERCENT.findall(cleaned)
    if pct:
        return float(pct[-1] if len(pct) > 1 else pct[0])
    num = NUMBER.search(cleaned)
    return float(num.group(1)) if num else None


def worded_direction(lo, hi):
    """+1 if the high end is the LOWER rate (value rises), -1 if higher, else None."""
    if not lo or not hi:
        return None
    lo_d, lo_u = bool(RATE_DOWN.search(lo)), bool(RATE_UP.search(lo))
    hi_d, hi_u = bool(RATE_DOWN.search(hi)), bool(RATE_UP.search(hi))
    if lo_u and hi_d and not (lo_d or hi_u):
        return 1.0
    if lo_d and hi_u and not (lo_u or hi_d):
        return -1.0
    return None


def check(lv):
    """(state, detail) for one lever. state is 'ok', 'skip' or a failure string."""
    name = lv.get("name") or "(unnamed lever)"
    impact = lv.get("impact")
    if impact is None:
        return "no impact field", "%s — lever carries no impact and cannot be read" % name
    if impact == 0:
        return "inert lever", "%s — impact is exactly 0: the slider cannot move the answer" % name
    if not RATE_NAME.search(name):
        return "skip", ""
    lo, hi = rate_at(lv.get("lo")), rate_at(lv.get("hi"))
    if lo is None or hi is None or lo == hi:
        want = worded_direction(lv.get("lo"), lv.get("hi"))
        if want is None:
            return ("direction unverifiable",
                    "%s — a discount-rate lever whose own labels say neither a rate nor a "
                    "direction (lo=%r hi=%r)" % (name, lv.get("lo"), lv.get("hi")))
        if want != math.copysign(1.0, impact):
            return ("wrong direction",
                    "%s — the labels run %r to %r, so the value must move %s and impact must "
                    "be %s; it is %+g" % (name, lv.get("lo"), lv.get("hi"),
                                          "UP" if want > 0 else "DOWN",
                                          "positive" if want > 0 else "negative", impact))
        return "ok", "%s — %r→%r, impact %+g" % (name, lv.get("lo"), lv.get("hi"), impact)
    want = -1.0 if hi > lo else 1.0
    if want != math.copysign(1.0, impact):
        return ("wrong direction",
                "%s — the rate runs %.4g at the low end to %.4g at the high end, so the value "
                "must move %s and impact must be %s; it is %+g"
                % (name, lo, hi, "DOWN" if hi > lo else "UP",
                   "negative" if want < 0 else "positive", impact))
    return "ok", "%s — rate %.4g→%.4g, impact %+g" % (name, lo, hi, impact)


def page_ticker(rel):
    """TICKER/study/index.html -> TICKER; legacy/ticker.html -> TICKER."""
    parts = rel.split(os.sep)
    if parts[0] == "legacy":
        return os.path.splitext(parts[-1])[0].upper()
    return parts[0]


def check_pages(levers):
    """Every study page reads levers.js, names a key it holds, and carries no lever itself.

    BOTH SURFACES, because the duplication was 186 copies and not 93: the legacy site
    carries its own page for every one of these names and it is still served. All four
    inverted levers were live there too, and would have stayed live if this gate had held
    only the new IA.
    """
    findings = []
    pages = sorted(glob.glob(os.path.join(ROOT, "*", "study", "index.html"))
                   + glob.glob(os.path.join(ROOT, "legacy", "*.html")))
    for p in pages:
        rel = os.path.relpath(p, ROOT)
        tk = page_ticker(rel)
        src = open(p, encoding="utf-8").read()
        if "renderFairLevers(" not in src:
            continue
        if INLINE_LEVER.search(src):
            findings.append((rel, "carries an inline lever array again — the levers live in "
                                  "assets/levers.js and a page copy re-creates the 93 copies "
                                  "that move ended"))
            continue
        if "assets/levers.js" not in src:
            findings.append((rel, "calls renderFairLevers but never loads assets/levers.js — "
                                  "the panel renders empty"))
            continue
        m = re.search(r"LEVERS\[[\"']([^\"']+)[\"']\]", src)
        if not m:
            findings.append((rel, "calls renderFairLevers with no readable LEVERS key"))
            continue
        if m.group(1) not in levers:
            findings.append((rel, "reads LEVERS[%r], which assets/levers.js does not hold"
                             % m.group(1)))
        elif m.group(1) != tk:
            findings.append((rel, "reads LEVERS[%r] on the %s page" % (m.group(1), tk)))
        if src.index("assets/levers.js") > src.index("renderFairLevers("):
            findings.append((rel, "loads assets/levers.js AFTER it calls renderFairLevers"))
    return len(pages), findings


def main():
    prune = "--prune" in sys.argv
    out = {"outstanding": []}
    if os.path.exists(OUTSTANDING_FILE):
        out = json.load(open(OUTSTANDING_FILE, encoding="utf-8"))
    known = {e["lever"] if isinstance(e, dict) else e for e in out.get("outstanding", [])}

    try:
        levers = load_levers()
    except RuntimeError as exc:
        print("FAIL — %s" % exc)
        return 1

    if not levers:
        print("FAIL — assets/levers.js holds no lever at all. An empty book is a broken gate "
              "rather than a clean one [R-ENF-04].")
        return 1

    n_pages, page_findings = check_pages(levers)
    if not n_pages:
        print("FAIL — found no page to hold against assets/levers.js [R-ENF-04].")
        return 1

    ok, hard, still, fixed, advisory = [], [], [], [], []
    n_levers = 0
    for tk in sorted(levers):
        for lv in levers[tk]:
            n_levers += 1
            key = "%s::%s" % (tk, lv.get("name"))
            state, detail = check(lv)
            if state == "skip":
                pass
            elif state == "ok":
                (fixed if key in known else ok).append((tk, detail))
            else:
                (still if key in known else hard).append((tk, "%s: %s" % (state, detail)))
            if lv.get("impact") and lv.get("min") is not None and lv.get("max") is not None:
                span = abs(lv["impact"]) * (lv["max"] - lv["min"]) / 100.0
                pct = (math.exp(span) - 1) * 100
                if pct < 1.0:
                    advisory.append((tk, "%s — moves the answer %.2f%% across its whole slider"
                                     % (lv.get("name"), pct)))
            if not lv.get("has_fmt"):
                hard.append((tk, "no caption: %s — the lever prints nothing at the position the "
                                 "reader drags to" % lv.get("name")))

    print("tickers in assets/levers.js: %d   levers: %d   pages held to it: %d   "
          "direction-checkable: %d   outstanding (allowed): %d"
          % (len(levers), n_levers, n_pages,
             len(ok) + len(fixed) + len(hard) + len(still), len(still)))
    for tk, detail in sorted(ok):
        print("   %-12s %s" % (tk, detail[:130]))

    if fixed:
        print("\nNOW PASSING — remove from the outstanding list (%d):" % len(fixed))
        for tk, detail in fixed:
            print("   %-12s %s" % (tk, detail[:130]))
    if still:
        print("\nstill outstanding, allowed for now (%d):" % len(still))
        for tk, detail in still:
            print("   %-12s %s" % (tk, detail[:220]))
    if advisory:
        print("\n[advisory] levers that barely move the answer (%d) — NOT gated, no threshold "
              "is defensible here; read them and decide:" % len(advisory))
        for tk, detail in sorted(advisory):
            print("   %-12s %s" % (tk, detail[:150]))
    if page_findings:
        print("\nFAIL — a study page is not wired to assets/levers.js (%d):" % len(page_findings))
        for rel, detail in page_findings:
            print("   %-34s %s" % (rel, detail[:300]))
    if hard:
        print("\nFAIL — not on the outstanding list and pointing the wrong way (%d):" % len(hard))
        for tk, detail in hard:
            print("   %-12s %s" % (tk, detail[:400]))

    if prune:
        out["outstanding"] = sorted(known - {"%s::%s" % (t, d.split(" — ")[0]) for t, d in fixed})
        json.dump(out, open(OUTSTANDING_FILE, "w", encoding="utf-8"), indent=1)
        print("\npruned — now %d entries" % len(out["outstanding"]))
        return 0
    if hard or page_findings:
        return 1
    print("\nOK — every direction-checkable lever moves the answer the way its own labels say, "
          "and every page reads them from one file.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
