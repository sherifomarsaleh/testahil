#!/usr/bin/env python3
"""Generate lessons.html — the public register of what every study taught us.

WHY THIS EXISTS. The register held 305 entries and reached no reader. The file was
served only because the whole repository is, so testahil.com/engine/Lessons_Register.md
returned 200 to anybody who already knew the path — which is not publishing. There was
no lessons page, nothing in files/, and no link from anywhere.

That is a strange thing to hide. Every entry carries `overturned_by`: the condition
that would kill the lesson, written at the time it was adopted. A research house that
publishes what would prove each of its own rules wrong is publishing the opposite of
marketing, and it is the same discipline the forecast ledger already shows.

THE COUNTS ON THIS PAGE ARE GENERATED, NEVER TYPED. method.html carried
"Completed on 1 name to date" for long enough to become false by a factor of eleven,
because it was a status sentence a person had to remember to update [R-DOC-02]. The
numbers here are read from the register at build time, so the page cannot drift from
it: rebuild and they are right, fail to rebuild and the gate says so.

    python3 scripts/build_lessons_page.py          # writes lessons.html
    python3 scripts/build_lessons_page.py --check   # fails if the page is stale
"""
from __future__ import annotations

import html
import importlib.util
import os
import re
import sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "lessons.html")
REG = os.path.join(ROOT, "engine", "lessons_register.py")

SCOPES = [
    ("ALL", "Binds every study",
     "Applying one of these is not a judgement call. It is the standing method."),
    ("CLASS", "Binds a class of company",
     "True of businesses that work the same way, and not beyond them."),
    ("STOCK", "Binds one company only",
     "Applying one of these to another company is superstition, and is named as such."),
]


def lessons() -> list:
    spec = importlib.util.spec_from_file_location("lessons_register", REG)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return list(mod.LESSONS)


def esc(v) -> str:
    return html.escape(str(v or "").strip())


def card(x: dict) -> str:
    bits = [
        '<div class="t-card" style="margin-bottom:10px">',
        '<p style="margin:0 0 4px;font-size:var(--fs-small);font-weight:600;opacity:.75">'
        f'{esc(x.get("id"))}'
        + (f' · {esc(x.get("applies_to"))}'
           if x.get("applies_to") and str(x.get("applies_to")) != "None" else "")
        + f' · {esc(x.get("status"))}</p>',
        f'<h3 style="margin:0 0 6px">{esc(x.get("headline"))}</h3>',
    ]
    if x.get("plain"):
        bits.append(f'<p style="margin:0 0 8px">{esc(x["plain"])}</p>')
    if x.get("evidence"):
        bits.append('<p class="muted" style="margin:0 0 6px;font-size:var(--fs-small)">'
                    f'<b>What we measured.</b> {esc(x["evidence"])}</p>')
    if x.get("correction"):
        # MOST ENTRIES HERE ARE CORRECTIONS, not falsifiable claims — we built
        # something wrong, found it, fixed it. Where the fix is recorded, it is
        # shown, because "what we changed" is the useful half for a reader and it
        # stops the fix competing with the scope condition for one field.
        bits.append('<p style="margin:0 0 6px;font-size:var(--fs-small)">'
                    f'<b>What we changed.</b> {esc(x["correction"])}</p>')
    if x.get("overturned_by"):
        # A rule published without the condition that would retire it is an opinion
        # with a number next to it. The label says "overturn", not "falsify": for a
        # correction this field names where the rule is MOOT rather than where it is
        # WRONG, and the stronger word would be overselling it.
        bits.append('<p style="margin:0;font-size:var(--fs-small)">'
                    '<b>What would overturn it.</b> '
                    f'{esc(x["overturned_by"])}</p>')
    if x.get("recurred"):
        # A MISTAKE MADE ONCE GETS A NOTE. A MISTAKE MADE TWICE GETS A GATE.
        # This is the only thing on the card that is an ACCUSATION rather than a
        # record: it says we were told and did it anyway. It is rendered loudly on
        # purpose — a repeat that reads the same as a first occurrence is a repeat
        # nobody will act on.
        n = len(x["recurred"])
        bits.append('<p style="margin:6px 0 0;font-size:var(--fs-small);'
                    'border-inline-start:3px solid #C0A45F;padding-inline-start:8px">'
                    f'<b>MADE AGAIN — {n} time{"s" if n > 1 else ""} since.</b> '
                    + " · ".join(esc(r) for r in x["recurred"])
                    + ' <i>Twice earns a gate.</i></p>')
    if x.get("source"):
        bits.append('<p class="muted" style="margin:6px 0 0;font-size:var(--fs-small);'
                    f'opacity:.7">{esc(x["source"])}</p>')
    bits.append("</div>")
    return "".join(bits)


def build() -> str:
    L = lessons()
    by = Counter(x.get("scope") for x in L)
    st = Counter(x.get("status") for x in L)
    head = open(os.path.join(ROOT, "method.html"), encoding="utf-8").read()

    # CLONE THE SHELL, NEVER REBUILD IT — the same discipline the ticker pages use.
    shell = head[:head.index("<main")]
    shell = shell.replace(
        "<title>Method — how the studies work | testahil?</title>",
        "<title>Lessons — what every study taught us | testahil?</title>")
    shell = re.sub(r'<meta name="description" content="[^"]*"',
                   '<meta name="description" content="Every lesson our studies have '
                   'produced, with the condition that would overturn each one."', shell, 1)
    shell = shell.replace("https://testahil.com/method.html",
                          "https://testahil.com/lessons.html")
    shell = re.sub(r'<meta property="og:title" content="[^"]*"',
                   '<meta property="og:title" content="Lessons — what every study '
                   'taught us | testahil?"', shell, 1)

    parts = [shell, '<main class="wrap">\n',
             '<section class="t-sec" style="margin-top:26px">',
             "<h1>Lessons</h1>",
             '<p style="max-width:74ch"><b>This is the register of our own mistakes, '
             'kept so we do not make them twice.</b> Every study and every '
             'walk-forward leaves something behind — something we got wrong and '
             'fixed, or something we measured and learned. Each entry carries what we '
             'measured, what we changed where a change was needed, and the condition '
             'that would overturn it, written when the lesson was adopted rather than '
             'afterwards.</p>',
             '<p style="max-width:74ch" class="muted">Most of these are CORRECTIONS: '
             'we built something wrong, found it, and fixed it. A correction is not a '
             'falsifiable claim — it is either applied or it is not — so where an '
             'entry says nothing would overturn it, that is the honest answer rather '
             'than a missing one.</p>',
             '<p style="max-width:74ch" class="muted">A lesson is a RECORD and not a '
             'rule: it binds the studies we build, it is not advice, and nothing here '
             'is a recommendation. Fundamental lessons are marked <b>provisional</b> '
             'while the method still rests on few names — read them, do not cite them '
             'as authority.</p>',
             '<div style="display:flex;gap:8px 26px;flex-wrap:wrap;margin-top:14px;'
             'font-weight:600">',
             f'<span>{len(L)} lessons</span>',
             f'<span>{by.get("ALL",0)} bind every study</span>',
             f'<span>{by.get("CLASS",0)} bind a class</span>',
             f'<span>{by.get("STOCK",0)} bind one company</span>',
             f'<span>{st.get("adopted",0)} adopted · {st.get("provisional",0)} '
             f'provisional · {st.get("outstanding",0)} outstanding</span>',
             f'<span style="color:#8a6d2f">{sum(1 for x in L if x.get("recurred"))} '
             f'made again</span>',
             "</div>",
             '<p class="muted" style="max-width:74ch;margin-top:12px">'
             '<b>A mistake made once gets a note. A mistake made twice gets a gate.</b> '
             'Enforcing every lesson would tax every study forever to catch problems '
             'that may never occur, so we do not. We record when one actually happens '
             'again, and a repeat is what earns it an automatic check. The count above '
             'is the queue, ordered by what has bitten us rather than by what we '
             'guessed would.</p>',
             "</section>"]

    for key, title, blurb in SCOPES:
        rows = [x for x in L if x.get("scope") == key]
        if not rows:
            continue
        parts.append(f'<section class="t-sec" style="margin-top:30px">'
                     f'<h2 id="{key.lower()}">{title} — {len(rows)}</h2>'
                     f'<p class="muted" style="max-width:70ch">{blurb}</p>'
                     f'<div style="margin-top:12px">')
        parts.extend(card(x) for x in rows)
        parts.append("</div></section>")

    parts.append('<section class="t-sec" style="margin-top:30px">'
                 '<p class="muted" style="max-width:74ch">Generated from the register '
                 'itself by <code>scripts/build_lessons_page.py</code>. The counts above '
                 'are read at build time rather than typed, so this page cannot quietly '
                 'disagree with the register it describes.</p></section>')
    parts.append("</main>\n")

    # THE TAIL IS BUILT, NOT CLONED. method.html's tail runs two method-specific
    # blocks that write into #m-tally and friends; on a page without those elements
    # the first one throws "Cannot set properties of null" and every script after it
    # is dead, including the chrome. Cloning the shell is right — cloning behaviour
    # that depends on elements this page does not have is not. Found by rendering the
    # page and reading the console, which is the only way this class of defect shows.
    src = head[head.rindex("</main>") + len("</main>"):]
    footer = src[:src.index("<script")] if "<script" in src else src
    parts.append(footer)
    parts.append('<script src="../assets/data.js"></script>\n'
                 '<script src="assets/test.js"></script>\n'
                 '<script>renderChrome("lessons");</script>\n'
                 "</body>\n</html>\n")
    return "".join(parts)


def main(argv) -> int:
    page = build()
    if "--check" in argv:
        if not os.path.exists(OUT):
            print("FAIL — lessons.html does not exist. Run "
                  "scripts/build_lessons_page.py")
            return 1
        if open(OUT, encoding="utf-8").read() != page:
            print("FAIL — lessons.html disagrees with the register it is generated "
                  "from.\n  A page that states a count somebody has to remember to "
                  "update is the defect this page was built to replace [R-DOC-02].\n"
                  "  Rebuild: python3 scripts/build_lessons_page.py")
            return 1
        n = len(lessons())
        print(f"OK — lessons.html is current with the register ({n} lessons).")
        return 0
    open(OUT, "w", encoding="utf-8").write(page)
    L = lessons()
    by = Counter(x.get("scope") for x in L)
    print(f"wrote lessons.html — {len(L)} lessons "
          f"({by.get('ALL',0)} ALL / {by.get('CLASS',0)} CLASS / "
          f"{by.get('STOCK',0)} STOCK)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
