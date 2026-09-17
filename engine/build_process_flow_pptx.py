"""THE PROCESS FLOW DECK, GENERATED FROM THE RUNBOOK RATHER THAN DRAWN BESIDE IT.

A deck describing a process is a SECOND COPY of that process, and a second copy stops
moving the moment the first is amended -- which is [R-DOC-01] in its plainest form and
what the revision stamps on both governing documents exist to catch. The first version of
this deck was drawn by hand while the runbook was at revision a; the runbook reached c the
same week and nothing about the deck would have said so.

So the step NUMBERS, TITLES and HAND-OFF MARKERS are read out of
`Recalibration_Runbook_*.md` at build time, and the deck carries the runbook's own
revision stamp on its face. If a step is renamed, added or removed, this deck changes on
the next build or it fails -- it cannot quietly disagree.

WHAT IS WRITTEN HERE AND NOT READ: the one-line gloss under each step. A slide cannot
carry a step's full prompt and choosing what to cut is an editorial judgement, not a
transformation -- so the glosses are written, marked as written, and kept to claims the
runbook itself makes. Anything a reader needs exactly belongs in the runbook, which is
named on the slide.

    python3 engine/build_process_flow_pptx.py
"""

import glob
import io
import os
import re
import sys

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Emu, Pt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENGINE = os.path.join(ROOT, 'engine')
OUT = os.path.join(ENGINE, 'Recalibration_Process_Flow_17-09-2026.pptx')

INK      = RGBColor(0x1A, 0x1A, 0x1A)
PAPER    = RGBColor(0xFA, 0xF9, 0xF6)
CARD     = RGBColor(0xFF, 0xFF, 0xFF)
RULE     = RGBColor(0xD8, 0xD4, 0xCC)
MUTED    = RGBColor(0x6B, 0x66, 0x5E)
ACCENT   = RGBColor(0x8C, 0x2F, 0x2F)   # the hand-off / hold colour
DESKBLUE = RGBColor(0x1F, 0x4E, 0x79)

EMU_IN = 914400
W, H = int(13.333 * EMU_IN), int(7.5 * EMU_IN)

# The gloss under each step. WRITTEN, not read -- see the module docstring.
GLOSS = {
    0: ("Freeze fair{} BEFORE anything moves it — a baseline taken afterwards is a "
        "fabricated zero. Ask for the latest price and its date, then route around it. "
        "Read what already binds on this name and its class."),
    1: ("Walk-forward on the company's own history. Drivers ground up — volume x price, "
        "cost per unit, margins as OUTPUTS. Terminal on a DISCLOSED asset life. One class "
        "primary IS the central; there is no blend."),
    2: ("The QC gate filled from OUTSIDE the study, evidence per row, never self-certified. "
        "Every CI gate run as CI runs it. More than 10% from price either way — the "
        "eight-heading gap review, BEFORE anything is staged."),
    3: ("The session BUILDS the prompt — registered name in English and the local language, "
        "the study's own driver headings, its dated negative searches — and STOPS. What "
        "comes back is a LEAD and never an input; every claim is traced to the primary "
        "source before it moves anything."),
    4: ("NO: say so, record which rings were re-run, move on — the commonest outcome. YES: "
        "score the prior study first, rebuild only what moved, and move every record, "
        "field name and sentence the lever touched IN THE SAME PASS, PDFs re-rendered."),
    5: ("The session hands you the document and the workbook and STOPS. Findings come back "
        "priced before judged, one row each, rejected only with receipts. Where no outside "
        "audit is run, the QC auditor stands in — from outside the study."),
    6: ("Three tests, all must pass. THE GAP: held only more than 10% BELOW price, released "
        "by a filed dissent. THE METHOD HOLD: Phase 1 must be proven. READABILITY: an "
        "unreadable study is held too. Publishing is a separate, explicit ask."),
}
HANDOFF = (3, 5)


def runbook():
    hits = sorted(glob.glob(os.path.join(ENGINE, 'Recalibration_Runbook_*.md')))
    if not hits:
        raise SystemExit('FATAL: no runbook on disk. This deck is generated FROM it; '
                         'drawing it without one is the second copy this file exists to '
                         'prevent.')
    return hits[-1]


def read_steps():
    """[(n, TITLE, hands_off)] read out of the runbook's own headings.

    REFUSES on a step it cannot read rather than skipping it: a deck silently missing a
    step is a process silently missing a step [R-ENF-04].
    """
    txt = io.open(runbook(), encoding='utf-8').read()
    rev = re.search(r'RUNBOOK REVISION ([0-9a-z\-]+)', txt)
    steps = []
    for m in re.finditer(r'^## STEP (\d+) [—-] (.+?)$', txt, re.M):
        n = int(m.group(1))
        rest = m.group(2)
        title = re.split(r'\s+·\s+', rest)[0].strip().rstrip('?').strip()
        steps.append((n, title.upper(), 'HANDS OFF' in rest.upper() or n in HANDOFF))
    if not steps:
        raise SystemExit('FATAL: the runbook exposed no "## STEP n" headings. An empty '
                         'read is not a clean read [R-ENF-04].')
    missing = sorted(set(GLOSS) - {n for n, _, _ in steps})
    extra = sorted({n for n, _, _ in steps} - set(GLOSS))
    if missing or extra:
        raise SystemExit('FATAL: the deck and the runbook disagree about which steps exist '
                         '— runbook is missing %s, deck has no gloss for %s. A deck that '
                         'can disagree with its own process quietly is the second copy '
                         'this file exists to prevent.' % (missing or 'none', extra or 'none'))
    return sorted(steps), (rev.group(1) if rev else '(unstamped)')


def _box(slide, x, y, w, h, fill=None, line=None):
    from pptx.enum.shapes import MSO_SHAPE
    sh = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h)
    sh.adjustments[0] = 0.06
    if fill is None:
        sh.fill.background()
    else:
        sh.fill.solid()
        sh.fill.fore_color.rgb = fill
    if line is None:
        sh.line.fill.background()
    else:
        sh.line.color.rgb = line
        sh.line.width = Pt(0.75)
    sh.shadow.inherit = False
    return sh


def _text(slide, x, y, w, h, s, size=11, bold=False, color=INK, align=PP_ALIGN.LEFT,
          space=0.95, caps=False):
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = MSO_ANCHOR.TOP
    p = tf.paragraphs[0]
    p.alignment = align
    p.line_spacing = space
    r = p.add_run()
    r.text = s.upper() if caps else s
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.color.rgb = color
    r.font.name = 'Georgia'
    return tb


def build():
    steps, rev = read_steps()
    prs = Presentation()
    prs.slide_width, prs.slide_height = Emu(W), Emu(H)
    blank = prs.slide_layouts[6]

    # ---------------------------------------------------------------- slide 1
    s1 = prs.slides.add_slide(blank)
    bg = _box(s1, 0, 0, Emu(W), Emu(H), fill=PAPER)
    bg.line.fill.background()
    _text(s1, Emu(int(0.6 * EMU_IN)), Emu(int(0.42 * EMU_IN)), Emu(int(11 * EMU_IN)),
          Emu(int(0.5 * EMU_IN)),
          'Fundamental recalibration — the process, end to end', size=26, bold=True)
    _text(s1, Emu(int(0.6 * EMU_IN)), Emu(int(0.95 * EMU_IN)), Emu(int(11.5 * EMU_IN)),
          Emu(int(0.35 * EMU_IN)),
          'ONE NAME AT A TIME, never in parallel — a defect found on the first usually '
          'changes how the second is built.   Publishing is a separate gate and it can '
          'refuse.', size=11.5, color=MUTED)

    # SEVEN CARDS ACROSS A 13-INCH SLIDE GIVES EACH 1.6 INCHES AND THE TITLES BREAK
    # MID-WORD -- "RECALIBRAT / E THE / FUNDAMENT / ALS" was the first draft, and the
    # gloss ran out of the bottom of the card into the hand-off badge. Rendering it and
    # LOOKING was what caught that, which is the same reason the depth bar makes reading
    # the rendered PDF a gate rather than a formality. Seven BANDS down the page give each
    # step the full width instead, and nothing wraps that should not.
    n = len(steps)
    left = 0.6 * EMU_IN
    band_w = W - 2 * left
    top, bh, bgap = 1.55 * EMU_IN, 0.60 * EMU_IN, 0.075 * EMU_IN

    for i, (num, title, hands) in enumerate(steps):
        y = int(top + i * (bh + bgap))
        _box(s1, Emu(int(left)), Emu(y), Emu(int(band_w)), Emu(int(bh)),
             fill=CARD, line=RULE)
        chip = 0.40 * EMU_IN
        c = _box(s1, Emu(int(left + 0.16 * EMU_IN)), Emu(int(y + (bh - chip) / 2)),
                 Emu(int(chip)), Emu(int(chip)), fill=ACCENT if hands else DESKBLUE)
        tf = c.text_frame
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        pp = tf.paragraphs[0]
        pp.alignment = PP_ALIGN.CENTER
        r = pp.add_run()
        r.text = str(num)
        r.font.size = Pt(14)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        r.font.name = 'Georgia'
        _text(s1, Emu(int(left + 0.68 * EMU_IN)), Emu(int(y + 0.115 * EMU_IN)),
              Emu(int(2.55 * EMU_IN)), Emu(int(0.4 * EMU_IN)),
              title, size=10.5, bold=True, space=0.92)
        gw = band_w - (3.35 * EMU_IN) - (1.55 * EMU_IN if hands else 0.2 * EMU_IN)
        _text(s1, Emu(int(left + 3.3 * EMU_IN)), Emu(int(y + 0.105 * EMU_IN)),
              Emu(int(gw)), Emu(int(bh - 0.16 * EMU_IN)),
              GLOSS[num], size=8.5, color=MUTED, space=1.08)
        if hands:
            _text(s1, Emu(int(left + band_w - 1.5 * EMU_IN)), Emu(int(y + 0.2 * EMU_IN)),
                  Emu(int(1.34 * EMU_IN)), Emu(int(0.3 * EMU_IN)),
                  'STOPS — HANDS OFF TO YOU', size=7.5, bold=True, color=ACCENT,
                  align=PP_ALIGN.RIGHT, space=0.95)

    foot = ('The two red steps STOP and wait for you — they are where a 90-name programme '
            'actually queues.   Expect step 6 to say HELD: most of the book is held on the '
            'METHOD until Phase 1 closes, and that is the gate working.')
    _text(s1, Emu(int(0.6 * EMU_IN)), Emu(int(6.32 * EMU_IN)), Emu(int(12.1 * EMU_IN)),
          Emu(int(0.6 * EMU_IN)), foot, size=10, color=INK, space=1.15)
    _text(s1, Emu(int(0.6 * EMU_IN)), Emu(int(7.02 * EMU_IN)), Emu(int(12.1 * EMU_IN)),
          Emu(int(0.32 * EMU_IN)),
          'Generated from engine/Recalibration_Runbook_17-09-2026.md, revision %s — the '
          'runbook is authoritative and this deck is a reading of it.' % rev,
          size=8.5, color=MUTED)

    # ---------------------------------------------------------------- slide 2
    s2 = prs.slides.add_slide(blank)
    bg2 = _box(s2, 0, 0, Emu(W), Emu(H), fill=PAPER)
    bg2.line.fill.background()
    _text(s2, Emu(int(0.6 * EMU_IN)), Emu(int(0.38 * EMU_IN)), Emu(int(12.2 * EMU_IN)),
          Emu(int(0.55 * EMU_IN)),
          'Ninety names through it — who does what', size=26, bold=True)
    _text(s2, Emu(int(0.6 * EMU_IN)), Emu(int(0.98 * EMU_IN)), Emu(int(12.2 * EMU_IN)),
          Emu(int(0.35 * EMU_IN)),
          'The page opposite is ONE name. This is the part that was missing: which name is '
          'touched next, what it is waiting for, and which of us is holding it.',
          size=11.5, color=MUTED)

    panels = [
        ('WHAT YOU DO — THREE THINGS', ACCENT,
         'ONE.  Say "start a recalibration on {TICKER}" — or "what is next" and take the '
         'name the board gives.\n\n'
         'TWO.  Answer the price question at the START. One line: the latest price and its '
         'date. It is the one input only you can supply; the work routes around it rather '
         'than waiting.\n\n'
         'THREE.  Take the two hand-off packs — the external news prompt at step 3 and the '
         'document plus workbook at step 5 — and bring back the answers.\n\n'
         'Nothing else is yours. You never type a command.'),
        ('WHAT THE SESSION DOES', DESKBLUE,
         'Reads the board, takes the next name in wave order, works steps 0 to 6 IN ORDER, '
         'stops at each stop condition and reports before moving on.\n\n'
         'Stops dead at 3 and 5 and hands over. Never runs two names at once.\n\n'
         'Never publishes without an explicit ask, never moves a fair value toward a '
         'price, never edits a gate to make something pass, never invents an input.\n\n'
         'Reports which names are sitting on YOUR desk, batched by market, so a pack goes '
         'out once rather than a name at a time.'),
        ('WHAT THE BOARD IS, AND WHY', MUTED,
         'engine/recalibration_run.py. Nothing is marked done and no step pointer is '
         'stored: each step is a PROBE over the artefacts that step produces, so a name '
         'sits wherever the probes stop.\n\n'
         'A board kept by hand goes stale the first busy afternoon — silently.\n\n'
         'ALL NINETY NAMES HAVE A DELIVERED STUDY. Twenty-three also commit a record the '
         'gates can read. A missing record is not a missing study, and reading it as one '
         'is what put "67 built from nothing" into the first version of this plan.\n\n'
         'WAVE 1: the 23 record-backed re-issues, EGX first. Then Phase 1. Then the 67.'),
    ]
    pw = (W - int(1.2 * EMU_IN) - int(0.34 * EMU_IN)) / 3
    for i, (head, col, body) in enumerate(panels):
        x = int(0.6 * EMU_IN + i * (pw + 0.17 * EMU_IN))
        _box(s2, Emu(x), Emu(int(1.62 * EMU_IN)), Emu(int(pw)), Emu(int(4.55 * EMU_IN)),
             fill=CARD, line=RULE)
        _text(s2, Emu(int(x + 0.26 * EMU_IN)), Emu(int(1.86 * EMU_IN)),
              Emu(int(pw - 0.52 * EMU_IN)), Emu(int(0.4 * EMU_IN)),
              head, size=11, bold=True, color=col)
        _text(s2, Emu(int(x + 0.26 * EMU_IN)), Emu(int(2.32 * EMU_IN)),
              Emu(int(pw - 0.52 * EMU_IN)), Emu(int(3.7 * EMU_IN)),
              body, size=9, color=MUTED, space=1.18)

    _text(s2, Emu(int(0.6 * EMU_IN)), Emu(int(6.42 * EMU_IN)), Emu(int(12.2 * EMU_IN)),
          Emu(int(0.7 * EMU_IN)),
          'WHY THE BOARD EXISTS, IN ONE SENTENCE: a probe that comes back empty has not '
          'found nothing — the first hypothesis is that the probe did not run. That is how '
          'sixty-seven delivered studies came to be reported as absent, and it is why every '
          'step is now read off an artefact rather than off anyone\'s memory.',
          size=10, color=INK, space=1.2)
    _text(s2, Emu(int(0.6 * EMU_IN)), Emu(int(7.06 * EMU_IN)), Emu(int(12.2 * EMU_IN)),
          Emu(int(0.32 * EMU_IN)),
          'Runbook: engine/Recalibration_Runbook_17-09-2026.md (revision %s).   Programme: '
          'engine/Recalibration_Campaign_Plan_17-09-2026.md.   Read every number live, '
          'never off this slide.' % rev, size=8.5, color=MUTED)

    prs.save(OUT)
    return OUT, steps, rev


if __name__ == '__main__':
    path, steps, rev = build()
    print('built %s' % os.path.relpath(path, ROOT))
    print('runbook revision %s, %d steps read from its own headings:' % (rev, len(steps)))
    for n, t, h in steps:
        print('  %d %-28s %s' % (n, t, 'HANDS OFF' if h else ''))
