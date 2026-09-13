#!/usr/bin/env python3
"""THE SENSITIVITY SLIDERS MUST MOVE THE ANSWER THE WAY THE STUDY SAYS THEY DO.

Enforced per [R-ENF-01]; population-anchored per [R-ENF-04]; ratcheted per
[R-ENF-02].

The defect. On 13-Sep-2026 a reader dragged the beta slider on the ADNOCLS
page to the top of the measured 90% interval and watched the fair value go
UP, from AED 7.05 to 8.43. A higher beta is a higher cost of equity and a
lower present value; there is no construction in this house where it is not.
The lever's own caption said so in words -- "regressing against an
equal-weight composite ... gives 0.71 and LIFTS the cash-flow value from AED
6.40 to 9.37" -- while the number beside it, impact:34.4, did the opposite.
The magnitude had been sized correctly off the study's published variants and
then shipped with the wrong sign.

Nothing caught it. check_page_integrity.py parses every one of these pages and
was green on all 93 the same morning: it checks the markup and the static
tables, and a lever array is neither. The panel is JavaScript that runs in the
reader's browser, so no gate in this repository had ever read what it computes.
A number that only exists after a drag is still a published number.

Three more of the same class fell out of the first sweep, none of them known:
MODON's beta lever (impact +1.0, also inverted, and so small it moved the
answer 0.65% across its whole range on a study whose own text calls beta "THE
lever ... that flipped the verdict"), MODON's terminal cost of capital
(+0.55, inverted), and ELEC's net-debt anchor (+0.00030, inverted).

What this gate holds the pages to:

  1. direction      -- for a lever whose variable IS a discount rate (beta,
                       cost of capital, cost of equity, WACC, required
                       return), the rate quoted at each end of its own slider
                       decides the sign: if the rate at `hi` is above the rate
                       at `lo`, impact must be negative, and the reverse.
                       This reads the page's own labels rather than the
                       lever's name, which is what keeps the five CBE-EASING
                       levers green -- their sliders run from today's money to
                       a LOWER rate, so a positive impact is correct there and
                       a name-matching gate would have called all five wrong.
  2. inert-lever    -- impact of exactly zero cannot move the answer at all.
                       Zero is not a small number here, it is a lever that
                       does nothing while presenting as one.
  3. unverifiable   -- a discount-rate lever whose own labels carry no
                       readable rate at either end FAILS rather than being
                       skipped. A silent skip is how check_artefact_currency
                       carried three holes for a month.

Magnitude is reported and NEVER gated. Across the 103 levers on the book the
full-slider effect runs from 0.36% to 260% with no gap anywhere in it, so any
cutoff would be a free parameter with no out-of-sample evidence, which the
PROMOTION RULE forbids. What is printed is the advisory list; what fails the
build is direction.

    python3 scripts/check_lever_directions.py
    python3 scripts/check_lever_directions.py --prune
"""
import glob
import json
import math
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTSTANDING_FILE = os.path.join(ROOT, "engine", "build_depth_audit", "lever_outstanding.json")

# a lever whose slider variable IS a discount rate: raise it, the value falls
RATE_NAME = re.compile(r"beta|cost of capital|cost of equity|discount rate|wacc|required return", re.I)

# "90% interval", "95% confidence" and friends are describing the MEASUREMENT,
# not the rate at that end of the slider
NOT_A_RATE = re.compile(r"\b(\d+(?:\.\d+)?)\s*%\s*(interval|range|confidence|ci\b)", re.I)
PERCENT = re.compile(r"(-?\d+(?:\.\d+)?)\s*%")
NUMBER = re.compile(r"(-?\d+(?:\.\d+)?)")

# the pages quote their lever strings both ways, and a first cut that knew only
# double quotes read 21 of the 93 panels and called the other 72 unreadable
QUOTED = r"(?:\"((?:[^\"\\]|\\.)*)\"|'((?:[^'\\]|\\.)*)')"
LEVER = re.compile(r"\{\s*name:\s*" + QUOTED + r"(?P<mid>.*?)\}\s*(?=,\s*\{|\])", re.S)
FIELD = {k: re.compile(k + r":\s*(-?\d+(?:\.\d+)?)") for k in ("min", "max", "step", "def", "impact")}
LABEL = {k: re.compile(k + r":\s*" + QUOTED) for k in ("lo", "hi")}


def first_group(m):
    """Whichever quote style this match used."""
    return m.group(1) if m.group(1) is not None else m.group(2)


def unescape(s):
    return re.sub(r"\\u([0-9a-fA-F]{4})", lambda m: chr(int(m.group(1), 16)), s).replace("\\'", "'")


def lever_block(src):
    """The array literal passed to renderFairLevers, or None."""
    i = src.find("renderFairLevers(")
    if i < 0:
        return None
    j = src.find("[", i)
    if j < 0:
        return None
    depth = 0
    for k in range(j, len(src)):
        if src[k] == "[":
            depth += 1
        elif src[k] == "]":
            depth -= 1
            if depth == 0:
                return src[j:k + 1]
    return None


def parse_levers(block):
    out = []
    for m in LEVER.finditer(block):
        mid = m.group("mid")
        lv = {"name": unescape(first_group(m))}
        for k, rx in FIELD.items():
            f = rx.search(mid)
            lv[k] = float(f.group(1)) if f else None
        for k, rx in LABEL.items():
            f = rx.search(mid)
            g = first_group(f) if f else None
            lv[k] = unescape(g) if g is not None else None
        out.append(lv)
    return out


def rate_at(label):
    """The rate this end of the slider stands for, read off the page's own label."""
    if not label:
        return None
    cleaned = NOT_A_RATE.sub(" ", label)
    pct = PERCENT.findall(cleaned)
    if pct:
        return float(pct[-1] if len(pct) > 1 else pct[0])
    num = NUMBER.search(cleaned)
    return float(num.group(1)) if num else None


# Some rate sliders are labelled in words rather than in basis points. The list is
# deliberately short and explicit: a word is here only because a page uses it to mean
# one direction of the policy rate and nothing else. Guessing from a longer vocabulary
# would be a gate inventing an interpretation the page never stated.
RATE_DOWN = re.compile(r"\beas(?:e|ier|ing)\b|\btailwind\b|\bcut(?:s)?\b|\bdovish\b", re.I)
RATE_UP = re.compile(r"\btighter\b|\btightening\b|\bheadwind\b|\bhike(?:s)?\b|\bhawkish\b", re.I)


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


def pages():
    found = {}
    for pat in ("*/study/index.html", "*.html", "*/*.html"):
        for p in glob.glob(os.path.join(ROOT, pat)):
            rel = os.path.relpath(p, ROOT)
            if rel.startswith("legacy" + os.sep):
                continue
            try:
                src = open(p, encoding="utf-8").read()
            except (OSError, UnicodeDecodeError):
                continue
            if "renderFairLevers(" in src:
                found[rel] = src
    return found


def check(rel, lv):
    """(state, detail) for one lever. state is 'ok', 'skip' or a failure string."""
    name = lv["name"]
    if lv["impact"] is None:
        return "no impact field", "%s — lever carries no impact and cannot be read" % name
    if lv["impact"] == 0:
        return "inert lever", "%s — impact is exactly 0: the slider cannot move the answer" % name
    if not RATE_NAME.search(name):
        return "skip", ""
    lo, hi = rate_at(lv["lo"]), rate_at(lv["hi"])
    if lo is None or hi is None or lo == hi:
        want = worded_direction(lv["lo"], lv["hi"])
        if want is None:
            return ("direction unverifiable",
                    "%s — a discount-rate lever whose own labels say neither a rate nor a "
                    "direction (lo=%r hi=%r)" % (name, lv["lo"], lv["hi"]))
        got = math.copysign(1.0, lv["impact"])
        if want != got:
            return ("wrong direction",
                    "%s — the labels run %r to %r, so the value must move %s and impact must be "
                    "%s; it is %+g" % (name, lv["lo"], lv["hi"], "UP" if want > 0 else "DOWN",
                                       "positive" if want > 0 else "negative", lv["impact"]))
        return "ok", "%s — %r→%r, impact %+g" % (name, lv["lo"], lv["hi"], lv["impact"])
    want = -1.0 if hi > lo else 1.0
    got = math.copysign(1.0, lv["impact"])
    if want != got:
        return ("wrong direction",
                "%s — the rate runs %.4g at the low end to %.4g at the high end, so the value must "
                "move %s and impact must be %s; it is %+g"
                % (name, lo, hi, "DOWN" if hi > lo else "UP",
                   "negative" if want < 0 else "positive", lv["impact"]))
    return "ok", "%s — rate %.4g→%.4g, impact %+g" % (name, lo, hi, lv["impact"])


def main():
    prune = "--prune" in sys.argv
    out = {"outstanding": []}
    if os.path.exists(OUTSTANDING_FILE):
        out = json.load(open(OUTSTANDING_FILE, encoding="utf-8"))
    known = {e["lever"] if isinstance(e, dict) else e for e in out.get("outstanding", [])}

    srcs = pages()
    if not srcs:
        print("FAIL — examined no pages at all. The population is empty, which is a broken "
              "gate rather than a clean book [R-ENF-04].")
        return 1

    ok, hard, still, fixed, advisory, unparsed = [], [], [], [], [], []
    n_levers = 0
    for rel in sorted(srcs):
        block = lever_block(srcs[rel])
        if block is None:
            unparsed.append(rel)
            continue
        levers = parse_levers(block)
        if not levers:
            unparsed.append(rel)
            continue
        for lv in levers:
            n_levers += 1
            key = "%s::%s" % (rel, lv["name"])
            state, detail = check(rel, lv)
            if state == "skip":
                pass
            elif state == "ok":
                (fixed if key in known else ok).append((rel, detail))
            else:
                (still if key in known else hard).append((rel, "%s: %s" % (state, detail)))
            if lv["impact"] and lv["min"] is not None and lv["max"] is not None:
                span = abs(lv["impact"]) * (lv["max"] - lv["min"]) / 100.0
                pct = (math.exp(span) - 1) * 100
                if pct < 1.0:
                    advisory.append((rel, "%s — moves the answer %.2f%% across its whole slider"
                                     % (lv["name"], pct)))

    print("pages with a lever panel: %d   levers read: %d   direction-checkable: %d   "
          "outstanding (allowed): %d"
          % (len(srcs), n_levers, len(ok) + len(fixed) + len(hard) + len(still), len(still)))
    for rel, detail in sorted(ok):
        print("   %-34s %s" % (rel, detail[:120]))

    if unparsed:
        print("\nFAIL — a page calls renderFairLevers and its lever array could not be read "
              "(%d). An unreadable panel is not a clean panel:" % len(unparsed))
        for rel in unparsed:
            print("   %s" % rel)

    if fixed:
        print("\nNOW PASSING — remove from the outstanding list (%d):" % len(fixed))
        for rel, detail in fixed:
            print("   %-34s %s" % (rel, detail[:120]))
    if still:
        print("\nstill outstanding, allowed for now (%d):" % len(still))
        for rel, detail in still:
            print("   %-34s %s" % (rel, detail[:200]))
    if advisory:
        print("\n[advisory] levers that barely move the answer (%d) — NOT gated, no threshold "
              "is defensible here; read them and decide:" % len(advisory))
        for rel, detail in sorted(advisory):
            print("   %-34s %s" % (rel, detail[:140]))
    if hard:
        print("\nFAIL — not on the outstanding list and pointing the wrong way (%d):" % len(hard))
        for rel, detail in hard:
            print("   %-34s %s" % (rel, detail[:400]))

    if prune:
        out["outstanding"] = sorted(known - {"%s::%s" % (r, d.split(" — ")[0]) for r, d in fixed})
        json.dump(out, open(OUTSTANDING_FILE, "w", encoding="utf-8"), indent=1)
        print("\npruned — now %d entries" % len(out["outstanding"]))
        return 0
    if hard or unparsed:
        return 1
    print("\nOK — every direction-checkable lever moves the answer the way its own labels say.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
