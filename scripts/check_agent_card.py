#!/usr/bin/env python3
"""The agent card must name exactly the agents that exist.  [R-ENF-01] [R-ENF-04]

WHY THIS EXISTS
    docs/agent_card/ documents the committed subagents in .claude/agents/ — what to say
    to reach each one, what it hands back, where it stops. It therefore states a fact
    that MOVES, and on 06-Sep-2026 it had already moved: the card said eight subagents
    while .claude/agents/ held nine, testahil-answer-challenger having landed with
    [R-GAP-02] five days after the card was written. Nothing noticed; the count was
    caught by eye while committing the card.

    The first draft of the card's README said plainly that there was no gate and the
    document was kept true by hand. That is exactly the shape [R-ENF-01] forbids where a
    test is possible, and here one is trivially possible: the population is a directory
    listing and the assertion is a substring search. So the class is closed rather than
    the instance, and the README now points here.

WHAT IT CHECKS
    1. every agent in .claude/agents/ appears in BOTH card sources (the HTML and the
       generator) — a row added to one and not the other is the drift this closes
    2. no card source names an agent that does not exist — a removed agent leaves a row
       telling the reader to invoke something that is gone
    3. the prose count ("nine subagents", "all nine") equals the real count
    4. the built .docx is present and newer than its generator, so the committed
       document is not one edit behind the script that makes it

THE POPULATION IS ANCHORED ELSEWHERE  [R-ENF-04]
    The agent list comes from the .claude/agents/ directory, not from the card, so a
    card that named nothing at all would FAIL rather than pass vacuously; a run that
    finds zero agents FAILS outright.

USAGE
    python3 scripts/check_agent_card.py
"""
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AGENTS = os.path.join(ROOT, '.claude', 'agents')
CARD = os.path.join(ROOT, 'docs', 'agent_card')
SOURCES = ['agent_card.html', 'build_card_docx.js']
DOCX = 'TESTAHIL_Agent_Card.docx'

WORDS = {1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five', 6: 'six', 7: 'seven',
         8: 'eight', 9: 'nine', 10: 'ten', 11: 'eleven', 12: 'twelve'}


def agent_names():
    """Every committed subagent, from the directory rather than from the card."""
    out = []
    for path in sorted(glob.glob(os.path.join(AGENTS, '*.md'))):
        head = open(path, encoding='utf-8').read(2048)
        m = re.match(r'^---\n(.*?)\n---\n', head, re.S)
        if not m:
            continue                      # not an agent definition
        name = re.search(r'^name:\s*(\S+)\s*$', m.group(1), re.M)
        if name:
            out.append(name.group(1))
    return out


def main():
    fails = []
    names = agent_names()
    if not names:
        print('FAIL — no agent definitions under .claude/agents/. The population this '
              'check is measured against is empty, so a clean result would mean nothing.')
        return 1

    n = len(names)
    print(f'{n} agent(s) in .claude/agents/: ' + ', '.join(names))

    for src in SOURCES:
        path = os.path.join(CARD, src)
        if not os.path.exists(path):
            fails.append(f'{src} is missing from docs/agent_card/')
            continue
        text = open(path, encoding='utf-8').read()
        # the HTML breaks the shared prefix for wrapping, so compare on the stem
        flat = text.replace('<wbr>', '')

        missing = [a for a in names if a not in flat]
        if missing:
            fails.append(f'{src} does not name: {", ".join(missing)} — every agent needs '
                         f'a row in every card source, or the card sends the reader to '
                         f'an agent it never mentions')

        cited = set(re.findall(r'testahil-[a-z][a-z-]+', flat))
        ghosts = sorted(c for c in cited if c not in names)
        if ghosts:
            fails.append(f'{src} names {", ".join(ghosts)}, which no longer exists in '
                         f'.claude/agents/ — a row for a removed agent tells the reader '
                         f'to invoke something that is gone')

        word = WORDS.get(n)
        if word:
            # only COUNTING contexts — "· four rings" is a ring count, not an agent count
            ws = '|'.join(WORDS.values())
            hits = re.findall(rf'\b(?:all|of)\s+({ws})\b|\b({ws})\s+subagents\b', flat)
            wrong = sorted({w for pair in hits for w in pair if w} - {word})
            if wrong:
                fails.append(f'{src} counts the agents as {", ".join(wrong)} — there are '
                             f'{n} ({word})')

    docx = os.path.join(CARD, DOCX)
    gen = os.path.join(CARD, 'build_card_docx.js')
    if not os.path.exists(docx):
        fails.append(f'{DOCX} is missing — the built card is the deliverable')
    elif os.path.exists(gen) and os.path.getmtime(docx) < os.path.getmtime(gen):
        fails.append(f'{DOCX} is older than build_card_docx.js — the committed document '
                     f'is behind the generator that makes it; re-run the builder')

    if fails:
        print(f'\nFAIL ({len(fails)}):')
        for f in fails:
            print('  - ' + f)
        print('\nSee docs/agent_card/README.md for what to update when an agent changes.')
        return 1
    print(f'OK — the agent card names exactly the {n} committed agents, counts them '
          f'correctly, and its document is not behind its generator.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
