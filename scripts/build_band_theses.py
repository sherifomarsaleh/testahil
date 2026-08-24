#!/usr/bin/env python3
"""[R-CAL-02] Rewrite the calibration clause in every coverage.js thesis.

The coverage index carried a one-line skill verdict per name -- "the calibration
is PARITY, not skill", "a ROBUST FAIL", "TIES its calibration back-test" -- in
twenty-odd hand-written forms, each with its own frozen statistics. Those are the
wrong object for a reader (see engine/band_record.py) and they were drifting: the
figures beside them were typed once and never revisited.

This replaces each such sentence with ONE generated sentence carrying the name's
live band record. Where a thesis explained a genuine mechanism -- thin trading,
an explained flat -- that clause is on the ticker page, which has room for it;
the index line is one sentence and the record is the sentence worth having.

Run:  python3 scripts/build_band_theses.py --write
"""
import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import band_record as br  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COVERAGE = os.path.join(ROOT, "assets", "coverage.js")

MARKET_LABEL = {"AE": "UAE", "EG": "Egyptian", "SA": "Saudi", "QA": "Qatari",
                "KR": "Korean", "IN": "Indian", "US": "US",
                "XAU": "precious-metals", "XPT": "precious-metals"}

# A sentence in a thesis is a calibration sentence if it carries any of these.
VERDICT = re.compile(
    r"PARITY|CRPS|matches benchmark|failed calibration|ROBUST FAIL|BOUNDARY"
    r"|calibration gate|calibration back-?test|carry-anchored random walk"
    r"|ties,? not beats|TIES its|ILLUSTRATIVE ONLY|illustrative only"
    r"|no skill is claimed|skill-validated|single-name edge|the part that passes"
    r"|classification technicality|over-cover|OVER-COVERED|five-year (?:back-test|requirement)"
    r"|panel-validated|bootstrap|straddles zero|PIT\b", re.I)
# The Arabic thesis carries the same claim in Arabic.
VERDICT_AR = re.compile(r"مونت كارلو|المعايرة|CRPS")


def pct(v):
    return f"{v * 100:.0f}%"


def sentence(r, arabic=False):
    if r.strength == "market-only":
        m = br.market_record(r.market)
        lab = MARKET_LABEL.get(r.market, r.market)
        if arabic:
            return (f"§3 لم يُغلق سوى {r.n} توقعاً ربع سنوياً خاصاً بهذا السهم — أقل من أن "
                    f"يُحكم به عليه وحده، لذا فالنطاقات هي نطاقات السوق: {m['n']} توقعاً عبر "
                    f"{m['names']} اسماً أنهت داخل نطاق الـ90% بنسبة {pct(m['cov90'])}.")
        return (f"§3 Only {r.n} three-month forecast{'s' if r.n != 1 else ''} of its own "
                f"ha{'ve' if r.n != 1 else 's'} resolved — too few to judge this name alone, "
                f"so the bands are its market's: {m['n']} resolved forecasts across the "
                f"{m['names']} names in the {lab} panel finished inside their 90% bands "
                f"{pct(m['cov90'])} of the time.")
    if arabic:
        return (f"§3 عبر {r.n} توقعاً ربع سنوياً مُنجزاً، أنهى السعر داخل نطاق الـ90% بنسبة "
                f"{pct(r.cov90)} من المرات، مقابل الـ90% المستهدفة.")
    s = (f"§3 Over {r.n} resolved three-month forecasts the price finished inside the 90% "
         f"band {pct(r.cov90)} of the time, against the 90% it aims at")
    if r.flag == "narrow":
        return s + " — short of that, so read the range as a floor on how far price can travel, not a ceiling."
    if r.flag == "wide":
        return s + " — more than that, so the real spread of outcomes has been tighter than the cone shows."
    return s + "."


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()
    src = open(COVERAGE, encoding="utf-8").read()
    records = br.by_key()

    # Operate ONLY on the contents of each thesis string literal. The first cut of
    # this script sliced entries by "next {tk:" and rejoined sentences, which ate
    # the closing '"},' of any entry whose LAST sentence was a calibration one and
    # left the file unparseable. A thesis is a JS string; scan it as one.
    out, changed, skipped = [], 0, []
    for m in re.finditer(r'\{tk:"([A-Za-z0-9]+)"', src):
        tk = m.group(1)
        nxt = src.find('{tk:"', m.end())
        entry_end = nxt if nxt > 0 else len(src)
        tm = re.search(r'thesis:"', src[m.start():entry_end])
        if not tm:
            continue
        i = m.start() + tm.end()          # first char INSIDE the literal
        j, esc = i, False
        while j < len(src):               # find the unescaped closing quote
            c = src[j]
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == '"':
                break
            j += 1
        body = src[i:j]
        try:
            r = br.resolve(tk, records)
        except KeyError:
            skipped.append(tk)
            continue
        arabic = bool(re.search(r'[؀-ۿ]|\\u06|\\u064', body))
        pat = VERDICT_AR if arabic else VERDICT
        parts = re.split(r'(?<=[.!?۔])\s+', body)
        hits = [k for k, p in enumerate(parts) if pat.search(p)]
        if not hits:
            continue
        keep = []
        for k, p in enumerate(parts):
            if k == hits[0]:
                keep.append(sentence(r, arabic))
            elif k in hits:
                continue
            else:
                keep.append(p)
        new_body = " ".join(keep).strip()
        if '"' in new_body.replace('\\"', ''):
            raise AssertionError(f"{tk}: generated thesis would break the literal")
        if new_body != body:
            out.append((i, j, new_body))
            changed += 1
            print(f"  {tk:12s} {r.strength}{', ' + r.flag if r.flag else ''}"
                  f"  ({len(hits)} sentence{'s' if len(hits) != 1 else ''} removed)")

    res = []
    last = 0
    for s0, e0, txt in out:
        res.append(src[last:s0]); res.append(txt); last = e0
    res.append(src[last:])
    new = "".join(res)
    br.assert_no_verdict_tokens(
        "\n".join(re.findall(r'thesis:"[^"]*"', new)), "coverage.js theses")
    print(f"{changed} thesis clause(s) rewritten"
          + (f"; no panel for {skipped}" if skipped else ""))
    if a.write:
        open(COVERAGE, "w", encoding="utf-8").write(new)
        print(f"wrote {COVERAGE}")
    else:
        print("(dry run)")


if __name__ == "__main__":
    main()
