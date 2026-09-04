"""The source text of an input register, as an OUTSIDE READER receives it.

[R-ENF-01 EXTENDED 03-Sep-2026] A standing-rule identifier and a repository path leak by
SHAPE rather than by vocabulary, which is why a hand-maintained word list has never caught
them and why the gate that does catch them matches on shape. They leak into DELIVERED
documents through one route above all others: an input register's own justification text,
which legitimately names the rule the input obeys and the file the figure was read from —
that is what makes the register auditable from inside — and neither belongs in a document
written for somebody outside this house.

WHY THIS IS SHARED AND NOT COPIED. The first version of this lived inside one study's
bibliography builder. Porting it into the others by hand would produce one
hand-maintained stripper per study with one hole per study, which is [L-084] on the sweep
registers and the scrub-list finding of the same morning: A RULE THAT ONE STUDY IMPLEMENTS
IS A RULE THAT ONE STUDY OBEYS. Where a rule can be made arithmetic, making it arithmetic
ONCE, in a shared place, is the only way it survives everywhere.

The register keeps its provenance. Only the rendering loses it.
"""
from __future__ import annotations

import re

# a standing-rule identifier: [R-AREA-NN], optionally with AMENDED/EXTENDED and a date,
# and the connective that would otherwise be left dangling behind it
_RULE = re.compile(r'\s*[\[(]?R-[A-Z]+-\d+(?:\s+(?:AMENDED|EXTENDED)[^\])]*)?[\])]?'
                   r'(?:\s+(?:requires|says|refuses|forbids|names|asks|prohibits))?')
# a path inside this repository
_PATH = re.compile(r'\s*\b(?:engine|scripts|assets)/[\w./{}-]+')
_EMPTY_BRACKET = re.compile(r'\s*[\[(]\s*[\])]')


# WHERE THE IDENTIFIER IS THE SUBJECT OF A VERB, DELETING IT INVERTS THE SENTENCE.
# "the rate [R-COC-01] requires" becomes "the rate requires", which says the opposite of
# what it meant. A first draft did exactly that and its own test caught it. So the two
# grammatical shapes are handled apart: an identifier standing alone is removed, and one
# acting as a subject is replaced by a plain-English name for the same thing. The same
# applies to a repository path that is the object of "from" or "in" — deleting it leaves
# "read from rather than typed", which is not a sentence.
_RULE_SUBJECT = re.compile(
    r'[\[(]?R-[A-Z]+-\d+(?:\s+(?:AMENDED|EXTENDED)[^\])]*)?[\])]?'
    r'(?=\s+(?:requires|says|refuses|forbids|names|asks|prohibits|permits))')
_PATH_OBJECT = re.compile(r'\b(from|in|at) ((?:engine|scripts|assets)/[\w./{}-]+)')
_STANDING = "this house's standing method"
_RECORD = "this house's own committed record"


def outward(txt: str) -> str:
    """Strip what is ours from a source field, leaving what is the reader's."""
    t = str(txt or '')
    t = _PATH_OBJECT.sub(lambda m: '%s %s' % (m.group(1), _RECORD), t)
    t = _RULE_SUBJECT.sub(_STANDING, t)
    t = _RULE.sub('', t)
    t = _PATH.sub('', t)
    t = _EMPTY_BRACKET.sub('', t)
    t = re.sub(r'\s{2,}', ' ', t)
    t = re.sub(r'\s+([,.;])', r'\1', t)
    return t.strip().strip(',').strip()
