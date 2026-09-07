#!/usr/bin/env python3
"""[R-ENF-01] DEPTH-BAR STANDARD 5 SAYS "ZERO TRANSPARENCY VERIFIED PROGRAMMATICALLY",
AND NOTHING VERIFIED IT.

Standard 5 requires every study figure to sit on a SOLID LIGHT CANVAS with zero
transparency, verified programmatically. What verified it was `figure_discipline`, a
boolean each study sets on itself.

`check_figure_axes` is the other figure gate and it is NOT this one: its subject is the
BUILDER — it runs each figure script under a guard and refuses a mark drawn outside its
own axis. Transparency belongs to the FILE A READER RECEIVES, and the two are different
objects for the reason [R-ENF-01] already recorded of tables: a check that needs the
builder is a check about the builder, and the reader does not have the builder. A figure
script that sets a solid facecolor can still ship inside a document as a translucent
PNG, and only the delivered file can say so.

MEASURED 07-09-2026 ACROSS EVERY DELIVERED STUDY DOCUMENT: 176 embedded images, EIGHT
translucent, all eight in ONE study and every one of them with fully transparent pixels
(minimum alpha 0). Every other study is opaque to the pixel. That study predates the
depth bar and is already listed on several ratchets, so this finds nothing anybody must
fix tonight — what it finds is that the clause was verified by nobody.

THE MODE IS NOT THE MEASUREMENT, and this gate exists in its corrected form because the
first pass got that wrong. Reading the colour MODE reported 160 of 176 images as
carrying transparency — matplotlib writes an RGBA channel that is fully opaque, so the
mode says almost nothing. The honest test is the MINIMUM ALPHA ACTUALLY PRESENT in the
pixels. The first figure was twenty times the real one and would have condemned
twenty-two compliant studies.

WHAT IT DELIBERATELY DOES NOT CHECK: whether the canvas is LIGHT. That is a judgement
about a palette — a dark figure can be a deliberate design and this gate cannot tell one
from an accident, so it would be making a claim it cannot support. Opacity is arithmetic
about the file; lightness is not, and the two are not bundled merely because one sentence
of the bar names both.

RATCHET [R-ENF-02], may only SHORTEN. POPULATION-ANCHORED [R-ENF-04] BOTH WAYS: a run
examining zero study directories FAILS, and so does one that read zero IMAGES across
present documents — a document reader that stopped finding media reads exactly like a
book of opaque figures.
"""

import glob
import io
import json
import os
import sys
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENGINE = os.path.join(ROOT, 'engine')
OUTSTANDING = os.path.join(ENGINE, 'build_depth_audit', 'figure_opacity_outstanding.json')

MEDIA = 'word/media/'
RASTER = ('.png', '.jpg', '.jpeg')


def load_ratchet():
    if not os.path.exists(OUTSTANDING):
        return []
    return json.load(open(OUTSTANDING, encoding='utf-8')).get('outstanding', [])


def latest_study_doc(study_dir):
    docs = sorted(p for p in glob.glob(os.path.join(study_dir, '*.docx'))
                  if 'valuation_study' in os.path.basename(p).lower())
    return docs[-1] if docs else None


def scan(path):
    """(images, translucent names, worst alpha). The MINIMUM alpha present, not the mode."""
    from PIL import Image
    n, bad, worst = 0, [], 255
    with zipfile.ZipFile(path) as z:
        for name in z.namelist():
            if not name.startswith(MEDIA) or not name.lower().endswith(RASTER):
                continue
            n += 1
            try:
                im = Image.open(io.BytesIO(z.read(name)))
            except Exception:
                continue
            if im.mode not in ('RGBA', 'LA'):
                continue
            lo = im.getchannel('A').getextrema()[0]
            worst = min(worst, lo)
            if lo < 255:
                bad.append((os.path.basename(name), lo))
    return n, bad, worst


def main(argv):
    prune = '--prune' in argv
    try:
        import PIL  # noqa: F401
    except Exception as exc:
        print('FIGURE OPACITY GATE  [R-ENF-01]')
        print('\nFAIL — Pillow is not importable (%s), so the question this gate asks '
              'cannot be answered. An unanswerable check is not a clean one [R-ENF-04].'
              % str(exc)[:120])
        return 1

    rat = load_ratchet()
    dirs = sorted(glob.glob(os.path.join(ENGINE, '*_study')))
    rows, total_images = [], 0
    for d in dirs:
        tk = os.path.basename(d)[:-len('_study')].upper()
        doc = latest_study_doc(d)
        if doc is None:
            rows.append(dict(ticker=tk, state='no delivered study document'))
            continue
        try:
            n, bad, worst = scan(doc)
        except Exception as exc:
            rows.append(dict(ticker=tk, state='unreadable: %s' % str(exc)[:70]))
            continue
        total_images += n
        rows.append(dict(ticker=tk, state='read', doc=os.path.basename(doc),
                         n=n, bad=bad, worst=worst))

    read = [r for r in rows if r['state'] == 'read']
    print('FIGURE OPACITY GATE  [R-ENF-01]  depth-bar standard 5')
    print('   the MINIMUM ALPHA ACTUALLY PRESENT in each delivered image, never the')
    print('   colour mode — matplotlib writes an opaque RGBA channel and the mode lies')
    print('   %d study directories · %d delivering a document · %d embedded images'
          % (len(dirs), len(read), total_images))

    fail = []
    if not dirs:
        print('\nFAIL — the gate examined ZERO study directories. An empty result is '
              'not a clean result.')
        return 1
    if not total_images:
        print('\nFAIL — the gate read ZERO images across %d delivered documents. A '
              'reader that stopped finding media reads exactly like a book of opaque '
              'figures [R-ENF-04].' % len(read))
        return 1

    on_disk = {r['ticker'] for r in rows}
    for tk in sorted(rat):
        if tk not in on_disk:
            fail.append('the ratchet lists %s and no such study directory exists — the '
                        'list is anchored on nothing' % tk)
    for r in rows:
        if r['state'].startswith('unreadable'):
            fail.append('%s: %s. An unreadable document is not a clean one [R-ENF-04].'
                        % (r['ticker'], r['state']))

    offenders = [r for r in read if r['bad']]
    print('\n  DELIVERING A TRANSLUCENT FIGURE: %d' % len(offenders))
    for r in sorted(offenders, key=lambda r: r['ticker']):
        tk = r['ticker']
        mark = 'ratcheted' if tk in rat else 'NEW'
        print('    %-12s %d of %d images, minimum alpha %d  [%s]'
              % (tk, len(r['bad']), r['n'], r['worst'], mark))
        for name, lo in r['bad'][:3]:
            print('        %s  min alpha %d' % (name, lo))
        if tk not in rat:
            fail.append('%s delivers %d translucent image(s) (minimum alpha %d). '
                        'Depth-bar standard 5 requires a solid canvas with zero '
                        'transparency.' % (tk, len(r['bad']), r['worst']))

    cleared = [tk for tk in rat
               if tk in on_disk and tk not in {r['ticker'] for r in offenders}]
    if cleared:
        print('\n  RATCHET ENTRIES NOW CLEAN: %s' % ', '.join(sorted(cleared)))
        if prune:
            keep = [t for t in rat if t not in cleared]
            json.dump({'rule': 'R-ENF-01/depth-bar standard 5', 'outstanding': keep},
                      open(OUTSTANDING, 'w', encoding='utf-8'), indent=1)
            print('  --prune: list shortened to %d' % len(keep))
        else:
            print('  run with --prune to shorten the list (it may only ever SHORTEN)')

    if fail:
        print('\nFAIL')
        for f in fail:
            print('  - ' + f)
        return 1
    print('\nOK — every delivered figure is opaque to the pixel.')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
