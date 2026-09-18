"""SIGCM clause 1, made arithmetic: a company's own reported figures come from its own
filings, and a source that names a data vendor or a news outlet says they did not.

WHY THIS EXISTS
    SIGCM clause 1 has been a HARD GATE since July 2026 and says it in terms: "HISTORICALS
    = OFFICIAL SOURCES ONLY ... no data vendors, brokers, press-as-a-numbers-source, or
    third-party estimates for the subject's reported historicals. If required official data
    is inaccessible, STOP AND INFORM — never substitute unofficial data; NEVER issue a
    report based on unofficial company information." A violation is a hard fail: do not
    issue.

    assert_sigcm() has checked a BOOLEAN a study sets on itself, which is the composite-beta
    shape [R-ENF-01] closed everywhere else. On 04-Sep-2026 two studies were issued in plain
    breach of it, and one of them was measured: SCEM took its revenue, profit and
    balance-sheet figures from Global Cement, cemnet, Daily News Egypt, Arab Finance and an
    aggregator's carry of S&P Global Market Intelligence — WHILE ITS AUDITED STATEMENTS SAT
    ON THE COMPANY'S OWN WEBSITE, six PDFs one click from the homepage, no authentication.
    Fetched and read, they put shareholders' equity at EGP 6,020.3mn against the study's
    5,240.0mn, cash at 4,762.3mn against a reported 3,850.0mn, and the year's depreciation
    at EGP 122.5mn against the study's 418.1mn. Every one of those errors understates the
    company.

WHAT IT MATCHES, AND WHY THAT SHAPE IS SAFE
    A NAMED COMMERCIAL DATA VENDOR OR NEWS OUTLET in the source field of a DATED HISTORICAL,
    where the source also relays ("reported by", "as carried by", "per") or names no company
    document at all. Three things make that narrow enough to be a gate:

      * a proper noun cannot occur innocently in a source field the way a concept can — this
        is the shape-matching argument [R-ENF-01 EXTENDED] made for rule identifiers and
        repository paths, where a word list could not be complete and a shape could;
      * the RELAY PHRASE is the whole of SIGCM's point. "EGX filing reported by Global
        Cement" names an official document and did not read it. A study that names a
        vendor BESIDE its own document ("Modon H1-2026 results announcement") read the
        document, and passes;
      * a DATED historical only. Three earlier drafts fired on forecast ratios (dna_pct,
        capex_pct, payout) and on commodity benchmarks quoted inside a company's own MD&A,
        at 156 and then 83 hits across sixteen studies — measuring the regex rather than the
        studies. Re-pointed rather than widened, per [R-COC-01], it finds two.

    THE VENDOR LIST IS INCOMPLETE AND THAT IS STATED RATHER THAN HIDDEN, exactly as the
    shape-matching vocabulary gate states it: this does not replace a study's own source
    discipline or the sweep register's primary-access invariant, both of which catch what a
    list of names cannot. Adding a vendor is cheap; a missing one is a gap, not a false claim.
"""
import re

# NAMED VENDORS AND OUTLETS. Proper nouns only — never a concept, because a concept in a
# source field has innocent readings and a vendor's name does not.
VENDOR = re.compile(
    r'\b(s&p global(?: market intelligence)?|capital ?iq|refinitiv|bloomberg|factset|'
    r'marketscreener|mubasher|simply ?wall ?st|investing\.com|tradingview|argaam|zawya|'
    r'arab ?finance|gurufocus|stockanalysis|macrotrends|wsj|barron\'?s|'
    r'global cement|cemnet|international cement review|daily news egypt|'
    r'reuters|associated press|bloomberg terminal|morningstar|koyfin|tikr)\b', re.I)

# A RELAY says the desk read the vendor, not the document.
RELAY = re.compile(r'\b(reported by|as carried by|as reported (?:in|by)|carried by|'
                   r'according to|via|per)\b', re.I)

# A COMPANY DOCUMENT the desk actually held.
OWN_DOC = re.compile(
    r'(audited|reviewed|annual report|financial statements|interim (?:statements|financial)|'
    r'statement of (?:profit|financial position|cash)|note \d|balance sheet|income statement|'
    r'cash[- ]flow statement|results (?:announcement|release)|investor presentation|'
    r'earnings (?:call|presentation)|MD&A|management (?:report|discussion)|prospectus|'
    r'FS_|AR20\d\d|disclosure)', re.I)

# A DATED HISTORICAL: a reported figure for a NAMED past period, never a forward ratio.
PERIOD = re.compile(r'_(fy|h[12]|q[1-4]|dec|jun|mar|sep)_?\d{2,4}$', re.I)
STEM = re.compile(r'^(rev|sales|ebitda|ebit|pat|profit|ni|eq|cash|debt|dna|dep|capex|'
                  r'nwc|inv|recv|pay|assets|liab|eps|dps|opex|cogs|sga|gp|gross|net)', re.I)


# THE STEM LIST WAS INCOMPLETE AND THE GAP WAS MEASURED RATHER THAN GUESSED. The list
# above is the re-pointing that three earlier drafts of this gate earned: matching every
# dated key fired on 156 then 83 items that were all work that was RIGHT — forecast
# ratios, commodity benchmarks quoted inside a company's own MD&A, balance-sheet lines
# naming the line rather than the document — so the check was narrowed to keys whose stem
# names a financial-statement line. That was correct and it stopped short.
#
# MEASURED 7 SEPTEMBER 2026 across every committed register: 1,445 dated keys carry a
# stem this list does not know, over 229 distinct prefixes. Most are operating or market
# quantities — volumes, day rates, rig counts, benchmark prices — which are a different
# class and are RIGHTLY excluded. The stems below are not: each names a line that appears
# on a face financial statement, exactly like the ones already listed. Two real breaches
# were invisible behind the gap and both are the shape the rule calls out by name — total
# assets and total liabilities sourced to "EGX filing reported by Global Cement", where a
# VENUE IS NOT A DOCUMENT, while the audited statements sat in that study's own filings
# directory.
#
# THE BOUNDARY IS NOT DECORATION. These stems are short enough to collide: a bare `ca`
# swallows capacity_fy24, a bare `ga` swallows gas_price_fy24, a bare `imp` swallows
# import_price_fy24 — and every one of those is an operating quantity this gate must not
# touch. Requiring the stem to end at an underscore or at the period suffix keeps the
# widening to the lines it names. The list above deliberately keeps its own looser form,
# because `rev` must reach `revenue` and re-pointing a working matcher is not part of
# this change.
STEM_LINE = re.compile(
    r'^(ta|tl|np|npa|pbt|ppe|nci|ocf|intang|assoc|lease|rou|tax|div|imp|ecl|'
    r'fincost|othinc|ga|cl|ca|equity|retained)(?=_)', re.I)


def is_dated_historical(key):
    """A reported figure for a named past period of the subject itself."""
    return bool(PERIOD.search(key) and (STEM.match(key) or STEM_LINE.match(key)))


def violation(key, source):
    """The reason this input breaches SIGCM clause 1, or '' where it does not."""
    if not is_dated_historical(key):
        return ''
    s = str(source or '')
    m = VENDOR.search(s)
    if not m:
        return ''
    # A COMPANY DOCUMENT NAMED ANYWHERE IN THE SOURCE CLEARS IT, and the relay phrase only
    # refines the message. The first draft condemned any relay phrase and so condemned
    # "Modon H1-2026 results announcement, as also reported by Reuters" — a study naming
    # its own release and a vendor as corroboration, which is right and must pass. Whether
    # a relay applies to the document or to the vendor is not decidable from the text, and
    # a study writing "audited statements" without holding them is lying, which is not
    # something any checker catches.
    if OWN_DOC.search(s):
        return ''
    if RELAY.search(s):
        return ('relayed through %s and naming no company document — the source names a '
                'venue the desk did not read' % m.group(0))
    return 'sourced to %s and to no company document' % m.group(0)


def audit(inputs):
    """[(key, reason, source), ...] for one study's input register."""
    out = []
    for k, v in (inputs or {}).items():
        if not isinstance(v, dict):
            continue
        why = violation(k, v.get('source', ''))
        if why:
            out.append((k, why, str(v.get('source', ''))[:90]))
    return sorted(out)


# ---------------------------------------------------------------------------
# THE DELIVERED BIBLIOGRAPHY, WHICH NOTHING READ [A7, 18-09-2026]
#
# audit() above reads a study's COMMITTED INPUT REGISTER, where the sources all name
# filings — and every study passes. The claim a READER receives is in the delivered
# bibliography's own sources table, which that population never reached. Measured on
# AMOC's delivered bibliography of 03-09-2026, row 2 of 228:
#
#     "Company financial summary pages | stockanalysis.com; Investing.com;
#      TradingView | Aug 2026 | Shares outstanding, market capitalisation, TOTAL
#      ASSETS, TOTAL LIABILITIES, CASH AND EQUIVALENTS, TOTAL DEBT, dividend per
#      share and payout ratio"
#
# Four balance-sheet lines of the subject, sourced to three aggregators and to no
# company document, in a document delivered to a reader, while the gate reported the
# study clean. This is [R-ENF-01]'s own species — the rule was enforced on the
# artefact somebody had built a reader for.
#
# THE SUBJECT VOCABULARY IS IN PROSE, WHICH IS WHY THIS IS NARROWER THAN audit().
# A register key is an identifier and a bibliography row is a sentence, so the
# in-scope test cannot be the PERIOD/STEM machinery above. What makes a word list
# safe HERE is the direction it runs: it decides what is IN SCOPE, so a name it
# misses is a gap and never a false accusation — the same argument VENDOR already
# makes about itself, one level up. The list is built from FACE-STATEMENT LINES
# only, because an operating or market quantity (a volume, a day rate, a share
# price, a market capitalisation) is legitimately sourced outside the filings and
# condemning one would be a claim this gate cannot support.
FACE_LINE = re.compile(
    r'\b(total assets|total liabilities|total equity|shareholders.? equity|'
    r'total debt|net debt|gross debt|borrowings|cash and (?:cash )?equivalents|'
    r'cash and bank|total revenue|revenues?\b|net sales|turnover|'
    r'gross profit|operating profit|net profit|profit for the (?:year|period)|'
    r'net income|ebitda|ebit\b|depreciation|amortisation|capital expenditure|capex|'
    r'working capital|inventor(?:y|ies)|receivables|payables|'
    r'earnings per share|dividend per share|shares outstanding|share capital)\b', re.I)

# A PAST PERIOD NAMED IN PROSE. A bibliography row about the future is not a
# historical, and the rule is about reported history.
PROSE_PERIOD = re.compile(
    r'\b(fy\s?20\d\d(?:/\d\d)?|20\d\d/\d\d|[1-4]q\s?20\d\d|q[1-4]\s?20\d\d|'
    r'h[12]\s?20\d\d|(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s?20\d\d|'
    r'\b20(?:1\d|2[0-6])\b)', re.I)


# TWO KINDS OF ROW ARE OUT OF SCOPE BY THE RULE ITSELF, AND BOTH WERE FOUND BY
# MEASURING RATHER THAN ANTICIPATED. A first draft flagged 34 rows across six studies
# and the largest class was PEER MULTIPLES — nine in one study, five in another — every
# one of them work that is RIGHT: SIGCM clause 5 says in terms to study competitors for
# operating KPIs and valuation multiples, and clause 1 forbids a vendor only for THE
# SUBJECT'S OWN reported historicals. A peer's market capitalisation read off an
# aggregator is the sanctioned construction, not a breach of it. The second class was
# rows declaring a NON-COMPANY sweep ring — Global, Country or Industry — which are
# external context by definition.
#
# Per [R-COC-01]: WHEN A CHECK FIRES ON WORK THAT IS RIGHT, RE-POINT IT. Both exclusions
# rest on the study's OWN declaration in its own row, which is the same footing OWN_DOC
# already stands on: a study labelling its own revenue row a peer multiple is lying, and
# no checker catches that.
# A THIRD EXCLUSION, ALSO MEASURED: a row about a TARGET, BUDGET, GUIDANCE or PLAN is
# forward-looking, and SIGCM clause 1 governs REPORTED HISTORICALS. AMOC's row "AMOC
# approves FY2025/26 planning budget ... the approved capital budget and the FY2025/26
# REVENUE TARGET" matched on the word revenue inside a forward target, which is not a
# figure this clause reaches at all — and [R-FCAL-01] is separately explicit that
# guidance is SCORED and never consumed. A study could in principle hide a historical
# behind the word "target"; that is the same exposure OWN_DOC and PEER_ROW already
# carry, and it is stated rather than papered over.
FORWARD_ROW = re.compile(r'\b(target|targets|budget|budgeted|guidance|plan(?:ned|ning)?|'
                         r'forecast|projection|outlook)\b', re.I)

PEER_ROW = re.compile(r'\b(peer|peers|comparable|comparables|comp set|cross[- ]check|'
                      r'benchmark compan|multiples? —|competitor)\b', re.I)
CONTEXT_RING = re.compile(r'(^|\|\s*)(global|country|industry)\s*\|', re.I)


def document_row_violation(cells):
    """The reason one delivered bibliography row breaches SIGCM clause 1, or ''.

    `cells` is that row's cells in printed order. The whole row is judged together,
    because a sources table splits the subject, the source and the period across
    columns and no one cell carries the claim.
    """
    joined = ' | '.join(str(c) for c in cells)
    if (PEER_ROW.search(joined) or CONTEXT_RING.search(joined)
            or FORWARD_ROW.search(joined)):
        return ''      # another company, a non-Company ring, or a forward claim
    if not FACE_LINE.search(joined):
        return ''                       # not a claim about a reported statement line
    if not PROSE_PERIOD.search(joined):
        return ''                       # not dated, so not a dated historical
    m = VENDOR.search(joined)
    if not m:
        return ''
    if OWN_DOC.search(joined):
        return ''                       # a company document named anywhere clears it
    if RELAY.search(joined):
        return ('relayed through %s and naming no company document' % m.group(0))
    return 'sourced to %s and to no company document' % m.group(0)


def audit_document(rows):
    """[(row_text, reason), ...] for one delivered document's extracted table rows."""
    out = []
    for cells in rows or []:
        why = document_row_violation(cells)
        if why:
            out.append((' | '.join(str(c) for c in cells)[:160], why))
    return out
