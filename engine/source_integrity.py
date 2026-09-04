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


def is_dated_historical(key):
    """A reported figure for a named past period of the subject itself."""
    return bool(PERIOD.search(key) and STEM.match(key))


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
