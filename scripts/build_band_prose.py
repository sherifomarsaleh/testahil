#!/usr/bin/env python3
"""[R-CAL-02] Write the band-record paragraph onto ticker pages, from the panels.

Ticker pages used to carry a hand-written calibration paragraph naming the skill
verdict. Two problems, and the second is why this is a generator and not an edit:
the verdict does not belong on a public surface at all, and the numbers beside it
went stale silently. On 24-Aug-2026 riyadhcable.html claimed "13 non-overlapping
three-month windows have resolved" and "coverage ran 85% / 92%" while its own
committed panel held 10 windows at 70% / 90% — nobody had touched the prose since
it was typed.

So the paragraph is GENERATED, and the volatile clause is additionally wrapped in
<span data-band-record="TK"> so app.js refreshes it in the browser from BANDS.
Belt and braces: the static text is correct at build time, and correct again at
render time even if a refit lands before this script is re-run.

Run:  python3 scripts/build_band_prose.py --write [--only TK]
"""
import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import band_record as br  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Reader-facing market names. The panel code is an internal key; a page says
# "the Abu Dhabi panel", never "the AE panel".
MARKET_LABEL = {
    "AE": "Abu Dhabi and Dubai", "EG": "Egyptian", "SA": "Saudi", "QA": "Qatari",
    "KR": "Korean", "IN": "Indian", "US": "US", "XAU": "precious-metals",
    "XPT": "precious-metals",
}
# Ticker page filename -> the ledger instrument whose record it carries.
PAGES = {
    "adnocls.html": "ADNOCLS", "savola.html": "SAVOLA",
    "riyadhcable.html": "RIYADHCABLE", "platinum.html": "Platinum",
}


def pct(v):
    return f"{v * 100:.0f}%"


def record_clause(r):
    """The volatile sentence — the one app.js also refreshes at render time."""
    if r.strength == "market-only":
        m = br.market_record(r.market)
        lab = MARKET_LABEL.get(r.market, r.market)
        return (f"Only {r.n} three-month forecast{'s' if r.n != 1 else ''} of its own "
                f"ha{'ve' if r.n != 1 else 's'} resolved so far — too few to say anything "
                f"reliable about this name specifically, so no name-level claim is made. "
                f"The bands are the market&rsquo;s: across the {m['names']} names in the "
                f"{lab} panel, {m['n']} resolved forecasts finished inside their 90% bands "
                f"{pct(m['cov90'])} of the time.")
    s = (f"Over {r.n} resolved three-month forecasts, the price finished inside the 90% "
         f"band {pct(r.cov90)} of the time, against the 90% that band aims at — and inside "
         f"the 80% and 50% bands {pct(r.cov80)} and {pct(r.cov50)} of the time.")
    if r.flag == "narrow":
        s += (" That is short of what the bands promise: they have been running narrower "
              "than the evidence supports, so read the range as a floor on how far price "
              "can travel, not a ceiling.")
    elif r.flag == "wide":
        s += (" That is more than the bands promise: the real spread of outcomes has been "
              "tighter than the cone shows — the safer direction to be wrong in, but still "
              "a miss.")
    return s


def paragraph(r):
    lead = ("Honestly: this name&rsquo;s own record is still short. "
            if r.strength == "market-only"
            else "Honestly: what this cone offers is a range, not a call. ")
    tail = (" Read the bands as a well-behaved but lightly-evidenced estimate of dispersion."
            if r.strength == "market-only" else
            (f" The record is short — {r.n} forecasts is enough to read but not enough to be "
             f"precise about." if r.strength == "short" else "") +
            " Read the bands as a well-behaved estimate of dispersion, not as an edge.")
    return (f'      <p class="muted">{lead}'
            f'<span data-band-record="{r.instrument}">{record_clause(r)}</span>'
            f'{tail}</p>')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--only")
    a = ap.parse_args()
    records = br.by_key()
    changed = 0
    for page, name in sorted(PAGES.items()):
        if a.only and a.only != name:
            continue
        path = os.path.join(ROOT, page)
        src = open(path, encoding="utf-8").read()
        r = br.resolve(name, records)
        new_p = paragraph(r)

        # The paragraph is the one opening "Honestly:" — matched whole, so a
        # partial match cannot leave half the old text behind.
        pat = re.compile(r'^ *<p class="muted">Honestly:.*?</p>$', re.M | re.S)
        hits = pat.findall(src)
        if len(hits) != 1:
            print(f"  {page}: {len(hits)} 'Honestly:' paragraphs — SKIPPED, needs a look")
            continue
        out = pat.sub(lambda _: new_p, src, count=1)

        # And the one-line pointer earlier in the page.
        out = re.sub(r'The calibration behind the cone is [^.<]*?(?:PARITY|parity)[^.<]*?\.',
                     'How the bands have actually held is set out below.', out)
        out = re.sub(r'\s*Step 0 verdict PARITY vs a carry-anchored random walk', '', out)
        br.assert_no_verdict_tokens(
            "\n".join(re.findall(r'<p class="muted">Honestly:.*?</p>', out, re.S)), page)
        if out != src:
            changed += 1
            print(f"  {page}: {name} — {r.strength}"
                  + (f", flag {r.flag}" if r.flag else ""))
            if a.write:
                open(path, "w", encoding="utf-8").write(out)
    print(f"{changed} page(s) {'rewritten' if a.write else 'would change'}")


if __name__ == "__main__":
    main()
