"""TMGH walk-forward — labelled-line extraction from the primary documents.

Two document families carry the group's own numbers, and both are used:

  * the CONSOLIDATED FINANCIAL STATEMENTS (FY2020-FY2025 and every 2021-2026
    interim), which are the audited/reviewed source and win any disagreement;
  * the FULL-YEAR EARNINGS RELEASES (FY2007-FY2025), which are the company's
    own documents and are the only source reaching back before 2020. From
    FY2018 they carry a complete consolidated income statement and balance
    sheet in the same three-segment shape as the statements.

Nothing here trusts an extractor's confidence. ARITHMETIC IS THE ARBITER: every
year is footed against the identities the statement itself asserts, and a year
that does not foot is reported rather than kept. The route each figure came by
(text layer or OCR) travels with it, because those two do not carry the same
confidence — a broken character map yields figures that look perfectly clean
and are wrong.
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.environ.get("TMGH_SCRATCH",
    "/tmp/claude-0/-home-user-testahil/ba35918b-2c34-5691-9e47-05ae974e86f1/scratchpad/tmgh_src")
TEXT = os.path.join(SRC, "text")

NUM = re.compile(r"\(?-?\d[\d,.]*\)?")

# OCR of a scanned statement splits a thousands group at the comma
# ("18,188, 184,098") or drops the comma for a space ("22,096 469,058").
# Both are repaired before tokenising, and both repairs are safe by shape: a
# real figure never ENDS in a comma, and a free-standing three-digit group
# never follows one. The foot check, not this repair, decides whether the
# reading survives.
# Only the comma-adjacent split is repaired. A rule that also joined two
# space-separated three-digit groups was tried and REMOVED: it merged the two
# genuinely separate columns of "1,572,121,295  541,675,444" into one figure,
# doing more damage than the artefact it fixed. Where a thousands group is
# split by a bare space and no comma survives, the foot check drops the cell
# rather than guessing at it.
OCR_SPLIT = [(re.compile(r"(\d),[ \t]+(\d)"), r"\1,\2"),
             (re.compile(r"(\d)[ \t]+,(\d)"), r"\1,\2")]


def repair_ocr(s):
    for rx, rep in OCR_SPLIT:
        s = rx.sub(rep, s)
    return s


def to_num(tok):
    """A number token as a float, or None. Parentheses mean negative."""
    t = tok.strip()
    neg = t.startswith("(") and t.endswith(")")
    t = t.strip("()").replace(" ", "")
    # dots used as thousands separators ("4.823.984") — an OCR reading of the
    # comma, distinguishable by shape: every group after the first is exactly
    # three digits and there is more than one of them
    if re.fullmatch(r"\d{1,3}(?:\.\d{3}){2,}", t):
        t = t.replace(".", "")
    t = t.replace(",", "")
    if t in ("", "-", ".", "‐"):
        return None
    # a stray decimal point inside an integer group is an OCR artefact; the
    # foot check is what decides whether the reading survives, not this guess
    try:
        v = float(t)
    except ValueError:
        return None
    return -v if neg else v


def page_of(text, idx):
    """Page number and route for a character offset into an extracted file."""
    hdr = None
    for m in re.finditer(r"<<<PAGE (\d+) route=(\S+)>>>", text[:idx]):
        hdr = m
    return (int(hdr.group(1)), hdr.group(2)) if hdr else (None, "?")


def numbers_after(text, m, want, window=260):
    """The first `want` numeric tokens following a label match."""
    tail = text[m.end(): m.end() + window]
    out = []
    for t in NUM.finditer(tail):
        v = to_num(t.group())
        if v is None:
            continue
        out.append(v)
        if len(out) >= want:
            break
    return out


def find(text, patterns, want=2, window=260, skip_pct=True):
    """Every match of any pattern, with its numbers, page and route."""
    hits = []
    for pat in patterns:
        for m in re.finditer(pat, text, re.I):
            # a percentage column immediately after the label is a share, not a
            # value; the era-2011 releases interleave them
            nums = numbers_after(text, m, want + 3, window)
            pg, route = page_of(text, m.start())
            hits.append({"label": m.group(0).strip()[:60], "nums": nums,
                         "page": pg, "route": route, "at": m.start()})
    return hits


def load(name):
    p = os.path.join(TEXT, name if name.endswith(".txt") else name + ".txt")
    return open(p).read()


def docs():
    return sorted(n for n in os.listdir(TEXT) if n.endswith(".txt"))


if __name__ == "__main__":
    t = load(sys.argv[1])
    for h in find(t, [sys.argv[2]], want=int(sys.argv[3]) if len(sys.argv) > 3 else 3):
        print("p%-3s %-6s %-55s %s" % (h["page"], h["route"], h["label"], h["nums"][:6]))
