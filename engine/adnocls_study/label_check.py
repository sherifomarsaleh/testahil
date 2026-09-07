"""External-reader scrub for the delivered ADNOCLS study: scan every paragraph and every
table cell of the .docx for internal-procedure vocabulary. Zero hits required."""
import re, sys
from docx import Document

BANNED = [
    (r'\bstep\s*0\b', 'step 0'),
    (r'\bstep\s*2a\b', 'step 2A'),
    (r'\bstep\s*\d', 'step + number'),
    (r'\bfour[- ]ring\b', 'four-ring'),
    (r'\brings?\b', 'ring'),
    (r'\binformation sweep\b', 'information sweep'),
    (r'\bsweep\b', 'sweep'),
    (r'\bgates?\b', 'gate'),
    (r'\bpromotion rule\b', 'promotion rule'),
    (r'\bstanding research protocol\b', 'standing research protocol'),
    (r'\bmc_v3\b', 'mc_v3'),
    (r'\bmarket_profiles\b', 'market_profiles'),
    (r'\bfitted_configs\b', 'fitted_configs'),
    (r'\bstudy_numbers\b', 'study_numbers'),
    (r'compute\.py', 'compute.py'),
    (r'\bdata_quality\b', 'data_quality'),
    (r'\bwacc_builder\b', 'wacc_builder'),
    (r'\bLONO\b', 'LONO'),
    (r'\bCRPS\b', 'CRPS'),
    (r'\bPIT\b', 'PIT'),
    (r'\bwidth_cal\b', 'width_cal'),
    (r'\bbootstrap block\b', 'bootstrap block'),
    (r'\bscale[- ]normali[sz]ed\b', 'scale-normalised'),
    (r'\bPARITY\b', 'PARITY'),
    (r'\bBOUNDARY\b', 'BOUNDARY'),
    (r'\bFAIL\b', 'FAIL'),
    (r'\bpersonas?\b', 'persona'),
    (r'\bprice target\b', 'price target'),
    (r'\bexpert persona library\b', 'expert persona library'),
]
CASE_SENSITIVE = {'LONO', 'CRPS', 'PIT', 'PARITY', 'BOUNDARY', 'FAIL'}


def cells(doc):
    for i, p in enumerate(doc.paragraphs):
        if p.text.strip():
            yield f'paragraph {i}', p.text
    for ti, t in enumerate(doc.tables):
        for ri, row in enumerate(t.rows):
            for ci, c in enumerate(row.cells):
                if c.text.strip():
                    yield f'table {ti} r{ri}c{ci}', c.text


def xlsx_cells(path):
    """String cells only, formulas skipped — modelled on engine/stc_study/scrub.py [L-350]."""
    import openpyxl
    wb = openpyxl.load_workbook(path, data_only=False, read_only=True)
    for ws in wb.worksheets:
        for ri, row in enumerate(ws.iter_rows(values_only=True), start=1):
            for ci, v in enumerate(row, start=1):
                if isinstance(v, str) and not v.startswith('=') and v.strip():
                    yield f'{ws.title}!r{ri}c{ci}', v
    wb.close()


# TWO ORDINARY SENSES, EACH DECLARED WITH ITS REASON AND ITS OWN CONTEXT TEST. A false
# positive on a word list is fixed by RE-POINTING it, never by deleting the sentence from
# the study — the standing discipline for every instrument here. Both were firing on text
# a reader needs, and neither can be reached by a mention of the procedure, because the
# context test is what admits them:
#
#   "price target" — occurs ONLY inside the standing disclaimer, whose whole purpose is to
#     say the values are NOT one. Admitted only where the same sentence carries a
#     negation, so a study that actually published a target would still be caught.
#   "gate"        — the beta regression's usability test is DISCLOSED to a reader under
#     that name and its result is a fact the reader is entitled to. Admitted only in that
#     exact collocation, so every procedural sense of the word still fires.
#
# THE TEST IS ON THE SENTENCE, NOT ON THE 45-CHARACTER WINDOW the report prints: a window
# is an arbitrary slice that can cut a negation in half, which is exactly what the first
# draft of this did.
ALLOWED = {
    'price target': (r'\b(?:not|never|nor|no)\b',
                     'the standing disclaimer, which exists to deny it'),
    'gate': (r'\busability\s+gate\b',
             "the disclosed name of the beta regression's own usability test"),
}
SENT_SPLIT = re.compile(r'(?<=[.!?])\s+')


def admitted(label, text, at):
    """True where this occurrence sits in a sentence the declaration admits."""
    rule = ALLOWED.get(label)
    if not rule:
        return False
    pos = 0
    for s in SENT_SPLIT.split(text):
        nxt = pos + len(s)
        if pos <= at <= nxt:
            return re.search(rule[0], s, re.IGNORECASE) is not None
        pos = nxt + 1
    return re.search(rule[0], text, re.IGNORECASE) is not None


def main(path):
    if path.lower().endswith(('.xlsx', '.xlsm')):
        blocks = list(xlsx_cells(path))
        hits = []
        for where, text in blocks:
            for pat, label in BANNED:
                flags = 0 if label in CASE_SENSITIVE else re.IGNORECASE
                for mt in re.finditer(pat, text, flags):
                    if admitted(label, text, mt.start()):
                        continue
                    s = max(0, mt.start() - 45)
                    hits.append((label, where, text[s:mt.end() + 45].replace('\n', ' ')))
        if hits:
            print(f'{len(hits)} HITS')
            for label, where, ctx in hits:
                print(f'  [{label}] {where}: ...{ctx}...')
            return 1
        print(f'scrub clean: 0 hits across {len(blocks)} workbook string cells')
        return 0
    doc = Document(path)
    hits = []
    for where, text in cells(doc):
        for pat, label in BANNED:
            flags = 0 if label in CASE_SENSITIVE else re.IGNORECASE
            for mt in re.finditer(pat, text, flags):
                s = max(0, mt.start() - 45)
                if admitted(label, text, mt.start()):
                    continue
                hits.append((label, where, text[s:mt.end() + 45].replace('\n', ' ')))
    # a bare "rating" is allowed only where it plainly means a sovereign credit rating
    for where, text in cells(doc):
        # A HYPHEN IS A WORD BOUNDARY AND \b THEREFORE MATCHES INSIDE "re-rating", which is
        # a market term for a change in the multiple a company trades on and is not a
        # rating of anything. Re-pointed rather than admitted by context [R-COC-01]: the
        # defect is in what the pattern matches, not in the sentence it matched.
        for mt in re.finditer(r'(?<![-\w])rating\b', text, re.IGNORECASE):
            s = max(0, mt.start() - 60)
            ctx = text[s:mt.end() + 60].lower()
            # 'rating basis' names the AGENCY-RATING construction of the country risk
            # premium, published beside the swap basis under this house's cost-of-capital
            # method — a thing about the sovereign, not a view on the stock, which is what
            # the unqualified-rating rule exists to catch. The collocation is what admits
            # it: a bare rating of the company still fires.
            if not any(k in ctx for k in ('sovereign', 'credit', 'agency', 'moody',
                                          'rating basis')):
                hits.append(('rating (unqualified)', where,
                             text[s:mt.end() + 60].replace('\n', ' ')))
    if hits:
        print(f'{len(hits)} HITS')
        for label, where, ctx in hits:
            print(f'  [{label}] {where}: ...{ctx}...')
        return 1
    print('scrub clean: 0 hits across '
          f'{len(doc.paragraphs)} paragraphs and {len(doc.tables)} tables')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
