#!/usr/bin/env python3
"""Is a scanned filing safe to read at all? [adopted 09-09-2026]

THE CASE THIS WAS WRITTEN FROM. FWRY's FY2021 statements are a Xerox WorkCentre 5330 scan.
That device family is subject to the 2013 JBIG2 SYMBOL-SUBSTITUTION DEFECT: to compress,
the scanner clusters visually similar glyphs and stores ONE bitmap per cluster, then
replays it wherever a member occurred. A 6 can be replayed where an 8 was printed. The
substitution happens AT SCAN TIME, so the pixels in the file are already wrong and NO
RE-READ AT ANY RESOLUTION CAN RECOVER THE TRUTH -- re-rendering at 600 dpi returns the
same wrong digit, sharper. Xerox confirmed it in 2013; German and Swiss authorities
withdrew affected devices from official use.

WHY THIS MATTERS HERE AND NOT ONLY IN THEORY. Seven glyph errors were caught across five
Egyptian companies in one night by re-adding a column against its own printed subtotal,
and the remedy in every case was to re-read at higher resolution. That remedy is CORRECT
only if the pixels are trustworthy. If a file carries symbol-substituted glyphs, the same
method produces a confident wrong answer that foots -- because the substitution is
consistent, so a wrongly-replayed digit appears identically everywhere and a subtotal
computed from those digits agrees with them.

THE TEST IS CHEAP AND IT IS DEFINITIVE. JBIG2 encodes in segment types. A file that
carries only IMMEDIATE GENERIC REGION segments (type 36/38/39) is coded losslessly at the
pixel level and cannot substitute symbols. A file carrying a SYMBOL DICTIONARY (type 0)
with TEXT REGIONS (type 4/6/7) is using the mode the defect lives in. That is a fact about
the bytes, not a judgement, and it is available before a single figure is read.

WHAT TO DO WITH THE ANSWER, which is the point of running it:
  generic only          -> the pixels are what the scanner saw. Extraction errors are the
                           extractor's, and re-reading at higher resolution is the correct
                           and sufficient remedy.
  symbol dictionary     -> STOP. Do not read figures off this file at any resolution. Get
                           the document by another route, or read it from a source that is
                           not a JBIG2 scan. A footing check CANNOT save you here: the
                           substituted digit is consistent, so the column foots on the
                           wrong number.
  not JBIG2             -> this test says nothing; the ordinary footing discipline applies.

    python3 engine/scanned_filing_integrity.py FILE.pdf [FILE.pdf ...]
"""
from __future__ import annotations

import os
import re
import sys
import zlib

# JBIG2 segment types that matter. The defect needs a symbol dictionary AND a text region:
# the dictionary holds the clustered bitmaps and the text region places them.
SYMBOL_DICTIONARY = 0
TEXT_REGION = {4, 6, 7}
GENERIC_REGION = {36, 38, 39}


def _segments(data: bytes):
    """Yield (type, page) for each JBIG2 segment header in an embedded stream.

    The header is: 4-byte number, 1-byte flags (low 6 bits are the type), a
    referred-to field whose length is variable, then a 1- or 4-byte page number.
    Only the type is needed here, and the walk stops at the first malformed header
    rather than guessing past it — a parser that guesses reports a clean file it
    never actually read [L-355].
    """
    i, n = 0, len(data)
    while i + 11 <= n:
        flags = data[i + 4]
        seg_type = flags & 0x3F
        page_assoc_4 = bool(flags & 0x40)
        rt = data[i + 5]
        count = rt >> 5
        if count == 7:                      # long form
            long_count = int.from_bytes(data[i + 5:i + 9], 'big') & 0x1FFFFFFF
            j = i + 9 + (long_count + 8) // 8
            count = long_count
        else:
            j = i + 6
        # referred-to segment numbers: size depends on this segment's own number
        seg_num = int.from_bytes(data[i:i + 4], 'big')
        ref_size = 1 if seg_num <= 256 else (2 if seg_num <= 65536 else 4)
        j += count * ref_size
        j += 4 if page_assoc_4 else 1
        if j + 4 > n:
            break
        length = int.from_bytes(data[j:j + 4], 'big')
        yield seg_type
        j += 4
        if length == 0xFFFFFFFF:            # unknown length: cannot walk further, honestly
            break
        i = j + length


def inspect(path: str) -> dict:
    """What this PDF's JBIG2 streams are, if any. Reads bytes; runs nothing."""
    raw = open(path, 'rb').read()
    out = {'path': path, 'jbig2_streams': 0, 'types': set(), 'producer': None}
    m = re.search(rb'/Producer\s*\((.{0,120}?)\)', raw, re.S)
    if m:
        out['producer'] = m.group(1).decode('latin-1', 'replace')
    for m in re.finditer(rb'/JBIG2Decode', raw):
        # the stream for this image follows its dictionary; find the next stream..endstream
        s = raw.find(b'stream', m.end())
        e = raw.find(b'endstream', s) if s != -1 else -1
        if s == -1 or e == -1:
            continue
        body = raw[s + 6:e].lstrip(b'\r\n')
        out['jbig2_streams'] += 1
        try:
            body = zlib.decompress(body)
        except Exception:                                              # noqa: BLE001
            pass                                                       # usually raw already
        for t in _segments(body):
            out['types'].add(t)
    return out


def verdict(info: dict):
    """(safe_to_read, headline, what_to_do). Never 'probably'."""
    if not info['jbig2_streams']:
        return None, 'not a JBIG2 scan', ('this test says nothing about this file; the '
                                          'ordinary footing discipline applies')
    t = info['types']
    if SYMBOL_DICTIONARY in t and (t & TEXT_REGION):
        return False, 'SYMBOL DICTIONARY PRESENT — do not read figures off this file', (
            'the scanner may have substituted digit bitmaps at scan time, so no re-read at '
            'any resolution recovers the truth AND A FOOTING CHECK CANNOT SAVE YOU: the '
            'substitution is consistent, so the column foots on the wrong number. Get the '
            'document by another route.')
    if t & GENERIC_REGION:
        return True, 'generic region only — the pixels are what the scanner saw', (
            'extraction errors are the extractor\'s; re-reading at higher resolution is the '
            'correct and sufficient remedy')
    return None, 'JBIG2 present but no region segment was parsed', (
        'the header walk stopped early rather than guessing past a malformed segment. '
        'Treat as UNKNOWN, not as safe.')


def main(argv):
    if not argv:
        print(__doc__)
        return 1
    bad = 0
    for path in argv:
        if not os.path.exists(path):
            print('%-52s MISSING' % path[-52:])
            bad += 1
            continue
        info = inspect(path)
        safe, headline, todo = verdict(info)
        mark = {True: 'SAFE   ', False: 'REFUSE ', None: 'UNKNOWN'}[safe]
        print('%s %s' % (mark, os.path.basename(path)))
        print('        %s' % headline)
        print('        streams %d   segment types %s   producer %r'
              % (info['jbig2_streams'], sorted(info['types']) or '-',
                 (info['producer'] or '')[:60]))
        print('        %s' % todo)
        if safe is False:
            bad += 1
    return 1 if bad else 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))
