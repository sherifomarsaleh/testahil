#!/usr/bin/env python3
"""Show the statement lines of an OCR'd filing, both passes, for hand-transcription.

The two passes disagree on individual digits; the transcription is settled by the
statement's OWN arithmetic, and where that is not decisive by the comparative column
of the FOLLOWING year's filing. Nothing is taken from a single unverified read.
"""
import re, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
PAT = re.compile(sys.argv[2] if len(sys.argv) > 2 else
    r'(Total assets|Total liabilit|Total equity|Total shareholder|Customers|Due to banks|'
    r'Cash and due|Murabaha|Cost of deposits|Net income from funds|NET REVENUE|Net revenue|'
    r'Fees and commission|Administrative|Impairment|profit before|PROFIT BEFORE|Tax|Taxes|'
    r'Net profit|Paid|financing (and facilities )?to customers|Financing and facilities|'
    r'Treasury|Subordinated|Non-controlling|Dividend|trading|Other operating)', re.I)
t = open(os.path.join(HERE, 'pages', sys.argv[1] + '.txt'), encoding='utf-8').read()
for blk in t.split('===== PAGE ')[1:]:
    head = blk.split('\n')[0]
    subs = blk.split('--- pass ')
    body = subs[1:] if len(subs) > 1 else [' (text layer)\n' + blk]
    out = []
    for sub in body:
        hd = sub.split('\n')[0]
        ls = [' '.join(l.split()) for l in sub.split('\n')
              if PAT.search(l) and sum(c.isdigit() for c in l) > 4]
        if ls:
            out.append('  -- %s' % hd)
            out += ['     ' + l for l in ls]
    if out:
        print('##### PAGE %s' % head)
        print('\n'.join(out))
