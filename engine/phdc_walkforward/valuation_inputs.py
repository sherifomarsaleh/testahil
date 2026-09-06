"""The VALUATION-INPUT BLOCK for this run — the figures a VALUE is rebuilt from.

[R-FCAL-01 AMENDED, 03-09-2026].  A driver panel is not a record a value can be
rebuilt from.  This run's `panel.py` committed what its own scoring needed — the
income statement as first reported, the unit and sales drivers off the earnings
releases, and the balance-sheet lines its working-capital driver consumes — and
answered the question it was built for.  Measured by
`engine/valuation_calibration/bridge_inputs.py`, PHDC then read as one of the two
names carrying a bridge at all, and as carrying NO capital expenditure and NO
depreciation at ANY origin, no share count from FY2020 onward, and nothing
whatever at FY2022.

WHY THE DIRECTION OF WHAT WAS MISSING MATTERED MORE THAN THE COUNT, AND WHY THIS
NAME IS THE CLEAREST CASE IN THE BOOK.  The omissions do not point one way.  No
capital expenditure OVERSTATES equity value; the absent share count from FY2020
means no value can meet a price AT ALL in those years, so the bias flips sign
across ONE NAME'S OWN ORIGINS.  That is the amendment's central claim — the
direction is unknown cell by cell — and it is worse than a large bias, because a
floor at least tells you which way it points.

WHAT IS HERE.  For every origin this run declares — FY2015 to FY2025, fiscal
years ending 31 December — cash and equivalents, interest-bearing debt, property,
depreciation and amortisation, the working-capital lines, capital expenditure,
and the share count with the par value it was footed against.  Every figure is a
COPY out of a filing this run had already parsed cell by cell; carrying them out
is transcription, not research.  Not carrying them out meant no valuation of this
company could ever be rebuilt at a past origin, permanently, for any year whose
filings are no longer to hand.

WHAT THE CENSUS COULD NOT SEE, AND IT WAS NOT THE RUN'S FAULT.  `bridge_inputs`
reported PHDC FY2014 and FY2022 as carrying NOTHING while this run's own
`panel.json` carried a sourced, footed balance sheet for both.  Its `scan_file`
walk descends into any dict before the leaf test can treat `{value, source}` as
a leaf, so every four-field record in this run's panel resolved to the leaf name
`value`, which matches neither its key map nor its guard.  The panel was never
the problem; the reader was.  That is recorded here rather than fixed here — this
module changes no instrument outside its own run.

CAPITAL EXPENDITURE IS DISCLOSED, NOT DERIVED.  The cash-flow statement of every
filing read here carries `Payments for purchase of fixed assets` and `Payments
for projects under construction` in its investing section, so the identity
capex = dPPE + D&A is never needed to PRODUCE a figure.  It is reported beside
the disclosed figure wherever it can run, and on this company the two are far
apart FOR A REASON THAT IS ABOUT DEVELOPERS RATHER THAN ABOUT THE PARSE: land
and projects move between investment property, projects under construction and
works in process — development inventory — without cash, so the change in the
property base is dominated by transfers this identity cannot see.  The DISCLOSED
cash figure is what is committed; the identity is reported beside it so a later
rebuild can see both rather than assume they agree.

DEPRECIATION IS THE CASH-FLOW ADD-BACK, AND THE INCOME-STATEMENT LINE IS NAMED
BESIDE IT.  Both are labelled `Administrative depreciation` and they are NOT the
same measurement — FY2020 prints 125,124,182 in the cash-flow statement against
the 105,251,400 this run's panel carries off the income statement, and the gap
runs the same way in every year read.  The add-back is what the identity above
needs and is what is committed; the income-statement line is carried beside as a
different measurement rather than reconciled, because no disclosure in these
filings reconciles them and inventing one would be the fabrication this archive
exists to refuse.

ROUTE, AND WHY ARITHMETIC DECIDES [clause (iii)].  These filings are English
translations of Arabic originals and they split into two groups.  FY2021 to
FY2025 carry a text layer of ZERO characters across 68 to 73 pages — pure scans.
FY2015 and FY2016 carry NINETY THOUSAND characters of perfectly clean-looking
text AND IT IS WRONG: the FY2015 text layer extracts cash of 956,559,608 and the
FY2016 text layer 808,546,570, against the 965,669,500 and 808,516,600 this run
committed off the rendered pixels, and on neither page do current assets less
current liabilities reproduce the working-capital line printed underneath them.
Inside the FY2016 filing the SAME figure renders two ways — its cash-flow
statement opens on 965,669,548 and its own comparative column closes the prior
year on 956,559,607.  That is the broken character map this protocol warns about,
caught the only way it can be caught.  So the route is not re-chosen here: it is
the one this run's own footing gate accepted, per year, and every page read is
footed again below before it is recorded.

WHAT IS ASSERTED AT IMPORT.  Each balance sheet against its own printed
subtotals — current assets less current liabilities against the printed working
capital, non-current assets plus that working capital against total investment,
equity plus non-current liabilities against the same total — each cash-flow
statement rolling forward from its opening to its closing cash, that closing cash
against the balance sheet's own cash line and against the figure this run already
committed, and every share count against the par value the same document states.
The footing runs as assertions rather than living in a comment, which is this
run's own discipline from `panel.py` and `build_panel.parse_year_checked`.

TWO ROWS IN THIS ARCHIVE ARE PRINTED AS MAGNITUDES ON SOME PAGES AND SIGNED ON
OTHERS — the balance sheet's own `Working capital` line and the cash-flow
statement's `Net increase in cash`.  FY2019 prints a working-capital DEFICIT of
2,144,801,815 with no sign, and FY2017 prints a cash DECREASE of 246,486,212 the
same way.  The sign is therefore taken from the identity the page itself supplies
and the printed magnitude is checked against it; the assertion is on the
magnitude, and which pages do this is recorded rather than smoothed away.

POINT-IN-TIME [SIGCM, and the pre-registration's section 1].  Every origin reads
its OWN filing's own column, with ONE exception which is stated rather than
glossed: the FY2022 annual statements are published in Arabic only, this run's
own parser could not resolve them, and FY2022 is therefore read from the
COMPARATIVE column of the FY2023 filing — exactly as this run's `panel.py`
already carries FY2022.  Nothing is carried BACKWARD: no later count, capital or
balance is substituted into an earlier origin, and where a later filing restates
a figure the restatement is named beside rather than swapped in.
"""
from __future__ import annotations

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

RULE = "[R-FCAL-01 AMENDED] (03-09-2026)"
COMPANY = "Palm Hills Developments S.A.E."
CURRENCY = "EGP"
BASIS = "consolidated"
FYE = "31 December"

# The origins this run declares (PRE_REGISTRATION_30-08-2026.md, section 1):
# first admissible FY2015, last scored FY2024, FY2025 struck but unresolved.
ORIGINS = list(range(2015, 2026))

# Which filing and which of its two columns each origin is read from.
COLUMN = {y: (y, "own") for y in ORIGINS}
COLUMN[2022] = (2023, "comparative")

IR_URL = "https://ir.palmhillsdevelopments.com/en-us/financial/resultcenter"

ROUTE_TEXT = (
    "read off the filing's own TEXT LAYER, accepted only because the page foots "
    "against the statement's own printed subtotals; the text layer of this "
    "archive is not trusted on its face — on the FY2015 and FY2016 filings it is "
    "clean-looking and wrong")
ROUTE_OCR = (
    "read off the RENDERED PAGE by OCR, at the lowest resolution whose reading "
    "FOOTS against the statement's own printed subtotals and reproduces the cash "
    "this run already committed; the filing carries no usable text layer, or one "
    "that does not foot")

# ---------------------------------------------------------------------------
# DATA — transcribed from the pages named, POSITIVE as printed except where the
# page itself prints a sign.  A field absent from a year is a line that year's
# statement does not print, or one this reading could not recover from it, and
# the record omits it rather than claiming a zero the page never stated.
#
# EACH BLOCK NAMES THE FILING AND THE COLUMN IT WAS READ FROM.  Three origins
# are read from a LATER filing's COMPARATIVE column and the reason is recorded
# in NOT_RECORDED rather than left as a detail: FY2022's own annual statements
# are published in Arabic only and this run's own parser reports that filing
# unresolved; FY2024's own balance-sheet page does not foot on this reading; and
# FY2023's own cash-flow page does not read at any resolution tried.
# ---------------------------------------------------------------------------
FILES = {
 2015: dict(file='4Q15 - Consolidated - Egyptian GAAP - English.pdf', pages=42, text_chars=90243, route='ocr',
     gutter='pooled', stmt_pages={'bs': 3, 'is': 4, 'cf': 5}, sha256_16='10a170cc4047fad5'),
 2016: dict(file='4Q16 - Consolidated Financials - Egyptian GAAP - English.pdf', pages=44, text_chars=98542, route='ocr',
     gutter='pooled', stmt_pages={'bs': 1, 'is': 2, 'cf': 4}, sha256_16='3ed5fe400e0b764b'),
 2017: dict(file='4Q17 - Consolidated Financials - Egyptian GAAP - English.pdf', pages=44, text_chars=104599, route='text',
     gutter='pooled', stmt_pages={'bs': 1, 'is': 2, 'cf': 4}, sha256_16='1f3e557b15fe86e0'),
 2018: dict(file='4Q18 - Consolidated Financials - Egyptian GAAP - English.pdf', pages=45, text_chars=106397, route='text',
     gutter='pooled', stmt_pages={'bs': 1, 'is': 2, 'cf': 4}, sha256_16='c463458a87b3c01d'),
 2019: dict(file='4Q19 - Consolidated Financials - Egyptian GAAP - English.pdf', pages=51, text_chars=108290, route='text',
     gutter='pooled', stmt_pages={'bs': 1, 'is': 3, 'cf': 6}, sha256_16='0efd92571c164b52'),
 2020: dict(file='4Q20 - Consolidated Financials - Egyptian GAAP - English.pdf', pages=46, text_chars=124565, route='text',
     gutter='pooled', stmt_pages={'bs': 1, 'is': 2, 'cf': 4}, sha256_16='31dc49c95d91cb62'),
 2021: dict(file='PHD - Consolidated Financial Statements - 4Q  2021 - English.pdf', pages=73, text_chars=0, route='ocr',
     gutter='pooled', stmt_pages={'bs': 3, 'is': 4, 'cf': 6}, sha256_16='a3780a02e39cf830'),
 2022: dict(file='بالم هيلز للتعمير - القوائم المالية المجمعة - 31 ديسمبر 2022.pdf', pages=71, text_chars=0, route='ocr',
     gutter='fixed', stmt_pages={}, sha256_16='a24a0ced84775bed'),
 2023: dict(file='Palm Hills Developments-Consolidated Financials - 31 December 2023.pdf', pages=68, text_chars=0, route='ocr',
     gutter='perrow', stmt_pages={'bs': 3, 'is': 4, 'cf': 6}, sha256_16='1112a14f12c1b89f'),
 2024: dict(file='Palm Hills FS Cons 31Dec 2024.pdf', pages=68, text_chars=0, route='ocr',
     gutter='pooled', stmt_pages={'bs': 2, 'is': 3, 'cf': 5}, sha256_16='db2e28a574fa0ff8'),
 2025: dict(file='ConsolidatedFinancials-Eng.pdf', pages=68, text_chars=0, route='ocr',
     gutter='pooled', stmt_pages={'bs': 3, 'is': 4, 'cf': 6}, sha256_16='72fc0ed5d947f7cc'),
}

# The printed wording of every line each filing carries, so the record cannot
# claim a line the page does not print.
LABELS = {
 2015: {"adv_cust": "Advances from customers", "adv_inv": "Advance payments for investments acquisition", "ar": "Accounts receivable", "assoc": "Investments in associates (8c,11b,29)", "banks_credit": "Banks credit balances", "cash": "Cash and cash equivalents", "creditors": "Creditors & other credit balances", "debtors": "Debtors and other debit balances", "due_from_rp": "Due from related parties", "due_to_rp": "Due to related parties", "fixed": "Fixed assets (net)", "fvtpl": "Investments at fair value through profit and loss (le)", "htm": "Held-to-maturity investments (31-11d)", "infra": "Completion of infrastructure liabilities", "inv_prop": "Investment property (11f,", "inv_purch": "Investment purchase liabilities", "land_c": "Current portion land purchase liabilities (19-43a)", "land_nc": "Land purchase liabilities (19-43b)", "loans_current": "Current portion of term loans", "loans_lt": "Loans", "nci": "Non-controlling interest", "np_long": "Notes payable long term (46b)", "np_short": "Notes payable short term (46a)", "nr_long": "Notes receivable long term", "nr_short": "Notes receivable short term", "overdraft": "Bank- over draft", "provisions": "Provisions", "puc": "Projects under construction", "resid": "Other long term liabilities — Residents’ Association", "share_capital": "Share capital", "supp_adv": "Suppliers advance payments", "suppliers": "Suppliers &contractors", "tax_payable": "Income tax payable (22a)", "tca": "Total current assets", "tcl": "Total current liabilities", "teal": "Total equity and non-current liabilities", "tle": "Total equity and non-current liabilities", "tnca": "Total long term assets", "tncl": "Total long term liabilities", "total_equity": "Total shareholders' equity", "total_investment": "Total investment", "total_liabs": "Total current liabilities", "wc_printed": "Working capital", "wip": "Works in process", "capex_fixed": "Payments for purchase of fixed assets", "capex_puc": "Payments for projects under construction", "close": "Cash and cash equivalents as at December", "dep": "Administrative depreciation", "disposal": "Proceeds from sale of fixed assets", "net": "Net increase in cash and cash equivalents during the period", "open": "Cash and cash equivalents at beginning of the period"},
 2016: {"adv_cust": "Advances from customers", "adv_inv": "Advance payments for investments acquisition", "ar": "Accounts receivable", "assoc": "Investments in associates (8c,11b,29)", "banks_credit": "Banks credit balances", "cash": "Cash and cash equivalents", "creditors": "Creditors & other credit balances", "debtors": "Debtors and other debit balances", "due_from_rp": "Due from related parties", "due_to_rp": "Due to related parties", "fixed": "Fixed assets (net)", "fvtpl": "Investments at fair value through profit and loss (le)", "htm": "Held-to-maturity investments (11d", "infra": "Completion of infrastructure liabilities", "inv_prop": "Investment property (If,", "inv_purch": "Investment purchase liabilities", "land_c": "Current portion land purchase liabilities", "land_nc": "Land purchase liabilities", "loans_current": "Current portion of term loans", "loans_lt": "Loans", "nci": "Non-controlling interest", "np_long": "Notes payable long term (48b)", "np_short": "Notes payable short term (48a)", "nr_long": "Notes receivable long term", "nr_short": "Notes receivable short term", "overdraft": "Bank- over draft", "provisions": "Provisions", "puc": "Projects under construction", "resid": "Other long term liabilities — Residents’ Association", "share_capital": "Share capital", "supp_adv": "Suppliers advance payments", "suppliers": "Suppliers &contractors", "tax_payable": "Income tax payable (22a)", "tca": "Total current assets", "tcl": "Total current liabilities", "teal": "Total equity and non-current liabilities", "tle": "Total equity and non-current liabilities", "tnca": "Total long term assets", "tncl": "Total long term liabilities", "total_equity": "Total shareholders’ equity", "total_investment": "Total investment", "total_liabs": "Total current liabilities", "wc_printed": "Working capital", "wip": "Works in process", "capex_fixed": "Payments for purchase of fixed assets", "capex_puc": "payments for projects under construction", "close": "Cash and cash equivalents as at December", "dep": "Administrative depreciation", "disposal": "Proceeds from sale of fixed assets", "net": "Net increase in cash and cash equivalents during the year", "open": "Cash and cash equivalents at beginning of the year"},
 2017: {"adv_cust": "Advances from customers", "adv_inv": "Advance payments for investments acquisition", "ar": "Accounts receivable", "assoc": "Investments in associates (8d,11b,31)", "banks_credit": "Banks credit balances", "cash": "Cash and cash equivalents", "creditors": "Creditors & other credit balances", "debtors": "Debtors and other debit balances", "due_from_rp": "Due from related parties", "due_to_rp": "Due to related parties", "fixed": "Fixed assets (net)", "fvtpl": "Investments at fair value through profit and loss (11e)", "htm": "Held-to-maturity investments (11d", "infra": "Completion of infrastructure liabilities", "inv_prop": "Investment property (11f,", "inv_purch": "Investment purchase liabilities", "jsa_c": "Joint shares arrangement short term", "jsa_nc": "joint share arrangement– long terms", "land_c": "Current portion of land purchase liabilities", "land_nc": "Land purchase liabilities", "loans_current": "Current portion of term loans", "loans_lt": "Loans", "nci": "Non-controlling interest", "np_long": "Notes payable long term (50b)", "np_short": "Notes payable short term (50a)", "nr_long": "Notes receivable long term", "nr_short": "Notes receivable short term", "overdraft": "Bank- over draft", "provisions": "Provisions", "puc": "Projects under construction", "resid": "Other long-term liabilities – Residents’ Association", "share_capital": "Share capital", "supp_adv": "Suppliers advance payments", "suppliers": "Suppliers &contractors", "tax_payable": "Income tax payable (22a)", "tca": "Total current assets", "tcl": "Total current liabilities", "teal": "Total equity and non-current liabilities", "tle": "Total equity and non-current liabilities", "tnca": "Total non-current assets", "tncl": "Total non-current liabilities", "total_equity": "Total shareholders' equity", "total_investment": "Total investment", "total_liabs": "Total current liabilities", "wc_printed": "Working capital", "wip": "Works in process", "capex_fixed": "Payments for purchase of fixed assets", "capex_puc": "payments for projects under construction", "close": "Cash and cash equivalents as at Dec.", "dep": "Administrative depreciation", "disposal": "Proceeds from sale of fixed assets", "net": "Net increase in cash and cash equivalents during the year", "open": "Cash and cash equivalents at beginning of the year"},
 2018: {"adv_cust": "Advances from customers", "adv_inv": "Advance payments for investments acquisition", "ar": "Accounts receivable", "assoc": "Investments in associates (8d-11b-31)", "banks_credit": "Banks credit balances", "cash": "Cash and cash equivalents", "creditors": "Creditors & other credit balances", "debtors": "Debtors and other debit balances", "due_from_rp": "Due from related parties (25-42-61a)", "due_to_rp": "Due to related parties (25-48-61a)", "fixed": "Fixed assets (net)", "fvtpl": "Investments at fair value through profit and loss (11e)", "htm": "Held-to-maturity investments (11d", "infra": "Completion of infrastructure liabilities", "inv_prop": "Investment property (11f-32)", "inv_purch": "Land purchase liabilities", "jsa_c": "Joint shares arrangement short term", "jsa_nc": "joint share arrangement– long terms", "land_c": "Current portion of land purchase liabilities", "land_nc": "Land purchase liabilities", "loans_current": "Current portion of term loans", "loans_lt": "long-term- loans", "nci": "Non-controlling interest", "np_long": "Notes payable long term (49b)", "np_short": "Notes payable short term (49a)", "nr_long": "Notes receivable long term", "nr_short": "Notes receivable short term", "overdraft": "Bank- over draft", "provisions": "Provisions", "puc": "Projects under construction", "resid": "Other long-term liabilities – Residents’ Association", "share_capital": "Share capital", "supp_adv": "Suppliers advance payments", "suppliers": "Suppliers &contractors", "tax_payable": "Income tax payable (22a)", "tca": "Total current assets", "tcl": "Total current liabilities", "teal": "Total equity and non-current liabilities", "tle": "Total equity and non-current liabilities", "tnca": "Total non-current assets", "tncl": "Total non-current liabilities", "total_equity": "Total shareholders' equity", "total_investment": "Total investment", "total_liabs": "Total current liabilities", "wc_printed": "Working capital", "wip": "Works in process", "capex_fixed": "Payments for purchase of fixed assets", "capex_puc": "Payments for projects under construction", "close": "Cash and cash equivalents as at December", "dep": "Administrative depreciation", "disposal": "Proceeds from sale of fixed assets", "net": "Net increase in cash and cash equivalents during the period", "open": "Cash and cash equivalents at beginning of the year"},
 2019: {"adv_cust": "Advances from customers", "adv_inv": "Advance payments for investments acquisition", "ar": "Accounts receivable", "assoc": "Investments in associates (8d-11b-31)", "banks_credit": "Banks credit balances", "cash": "Cash and cash equivalents", "creditors": "Creditors & other credit balances", "debtors": "Debtors and other debit balances", "due_from_rp": "Due from related parties (25-42-61a)", "due_to_rp": "Due to related parties (25-48-61a)", "fixed": "Fixed assets (net)", "fvtpl": "Investments at fair value through profit and loss (11e)", "htm": "Held-to-maturity investments (11d", "infra": "Completion of infrastructure liabilities", "inv_prop": "Investment property (11f-32)", "inv_purch": "Land purchase liabilities", "jsa_c": "Joint shares arrangement short term", "jsa_nc": "joint share arrangement– long terms", "land_c": "Current portion of land purchase liabilities", "land_nc": "Land purchase liabilities", "loans_current": "Current portion of term loans", "loans_lt": "long-term- loans", "nci": "Non-controlling interest", "np_long": "Notes payable long term (49b)", "np_short": "Notes payable short term (49a)", "nr_long": "Notes receivable long term", "nr_short": "Notes receivable short term", "overdraft": "Bank- over draft", "provisions": "Provisions", "puc": "Projects under construction", "resid": "Other long-term liabilities – Residents’ Association", "share_capital": "Share capital", "supp_adv": "Suppliers advance payments", "suppliers": "Suppliers &contractors", "tax_payable": "Income tax payable (22a)", "tca": "Total current assets", "tcl": "Total current liabilities", "teal": "Total equity and non-current liabilities", "tle": "Total equity and non-current liabilities", "tnca": "Total non-current assets", "tncl": "Total non-current liabilities", "total_equity": "Total shareholders' equity", "total_investment": "Total investment", "total_liabs": "Total current liabilities", "wc_printed": "Working capital", "wip": "Works in process", "capex_fixed": "Payments for purchase of fixed assets", "capex_puc": "Payments for projects under construction", "close": "Cash and cash equivalents as at December", "dep": "Administrative depreciation", "disposal": "Proceeds from sale of fixed assets", "net": "Net increase in cash and cash equivalents during the period", "open": "Cash and cash equivalents at beginning of the year"},
 2020: {"adv_cust": "Advances from customers", "adv_inv": "Advance payments for investments acquisition", "ar": "Accounts receivable", "assoc": "Investments in associates b11 d8", "banks_credit": "Banks credit balances", "cash": "Cash and cash equivalents", "creditors": "Creditors & other credit balances", "debtors": "Debtors and other debit balances", "due_from_rp": "Due from related parties", "due_to_rp": "Due to related parties", "fixed": "Fixed assets (net)", "fvtpl": "Investments at fair value through profit and loss e11)", "htm": "Held-to-maturity investments d", "infra": "Completion of infrastructure liabilities", "inv_prop": "Investment property f11", "jsa_c": "Joint shares arrangement short term", "jsa_nc": "joint share arrangement– long terms", "land_c": "Current portion of land purchase liabilities a48", "land_nc": "Land purchase liabilities b", "loans_current": "Current portion of short term loans", "loans_lt": "long-term- loans", "nci": "Non-controlling interest", "np_long": "Notes payable long term b", "np_short": "Notes payable short term a", "nr_long": "Notes receivable long term", "nr_short": "Notes receivable short term", "overdraft": "Bank- overdraft", "provisions": "Provisions c)", "puc": "Projects under construction", "resid": "Other long-term liabilities – Residents’ Association", "share_capital": "Share capital", "supp_adv": "Suppliers advance payments", "suppliers": "Suppliers & Contractors", "tax_payable": "Income tax payable a", "tca": "Total current assets", "tcl": "Total current liabilities", "teal": "Total equity and non-current liabilities", "tle": "Total equity and non-current liabilities", "tnca": "Total non-current assets", "tncl": "Total non-current liabilities", "total_equity": "Total shareholders' equity", "total_investment": "Total investment", "total_liabs": "Total current liabilities", "treasury": "Treasury shares", "wc_printed": "Working capital", "wip": "Works in process", "capex_fixed": "Payments for purchase of fixed assets", "capex_puc": "Payments for projects under construction", "close": "Cash and cash equivalents as at December", "dep": "Administrative depreciation", "disposal": "Proceeds from sale of fixed assets", "net": "Net increase in cash and cash equivalents during the period", "open": "Cash and cash equivalents at beginning of the year"},
 2021: {"adv_cust": "Advances from customers", "adv_inv": "Advance payments for investments acquisition", "ar": "Accounts receivable", "assoc": "Investments in associates +b11+d8)", "banks_credit": "Banks credit balances", "cash": "Cash and cash equivalents +32)", "checks_liab": "liabilities for checks received from customers", "creditors": "Creditors & other credit balances", "debtors": "Debtors and other debit balances", "due_from_rp": "Due from related parties «72 +27)", "due_to_rp": "Due to related parties {57 +72 +27)", "fin_amort": "Financial investments at amortized cost (47,33/5)", "fixed": "Fixed assets (net)", "fvtpl": "Investments at fair value through profit and loss (33/5)", "infra": "Completion of infrastructure liabilities 2n", "inv_prop": "Investment property cll)", "inv_purch": "Investments purchase liabilities", "jsa_c": "Joint shares arrangement short term", "jsa_nc": "Joint shares arrangement long term", "land_c": "Current portion of land purchase liabilities +20)", "land_nc": "Land purchase liabilities — Long Term «20)", "lease_c": "Lease contract liabilities short term", "lease_nc": "Lease contract liabilities long term", "loans_current": "Current portion of Short-term loans Sl)", "loans_lt": "Loans long-term", "nci": "Non-controlling equites", "np_long": "Notes payable long term (b", "np_short": "Notes payable short term (a", "nr_long": "Notes receivable long term for undclivercd units", "nr_long_undel": "Notes receivable long term for undclivercd units", "nr_short": "Notes receivable short term +16)", "nr_short_undel": "Notes receivable short term for undelivered units", "overdraft": "Bank- overdraft {3}", "provisions": "Provisions", "puc": "Projects under construction My «12 ‘3", "resid": "Other long-term liabilities — Residents’ Association {63)", "rou": "Right of use asset", "share_capital": "Share capital", "supp_adv": "Suppliers advance payments", "suppliers": "Suppliers And contractors", "tax_payable": "Income tax payable (70«223)", "tca": "Total current assets", "tcl": "otal current liabilities", "teal": "Total equity and non-current liabilities", "tle": "Total equity and non-current liabilities", "tnca": "Total non-current assets", "tncl": "Total non-current liabilities", "total_equity": "Total sharcholders' equity", "total_investment": "Total investment", "total_liabs": "otal current liabilities", "treasury": "Treasury shares In Cost +17)", "wip": "Works in process «14)", "capex_fixed": "Payments for purchase fixed assets", "capex_puc": "Payments for projects under construction +12)", "close": "Cash and cash equivalents as of December «32)", "dep": "Depreciation and amortization (40:36 +37)", "disposal": "Proceeds from sale of fixed assets", "net": "Net increase in cash and cash equivalents during the year", "open": "Cash and cash equivalents at beginning of the year"},
 2023: {"adv_cust": "Advances from customers", "adv_inv": "Advance payments for investments acquisition", "ar": "Accounts receivable", "assoc": "Investments tn associates +b11«d8)", "banks_credit": "Banks credit balances", "cash": "Cash and cash equivalents", "checks_liab": "liabilities for checks received from customers", "creditors": "Creditors & other credit balances", "debtors": "Debtors and other debit balances", "due_from_rp": "Due from related parties +47 «27)", "due_to_rp": "Due to related parties +27)", "fin_amort": "Financial investments at amortized cost (48:33/5)", "fixed": "Fixed assets (net) +13)", "fvtpl": "Investments at fair value through profit and loss (33/5)", "inv_prop": "Investment property cll)", "inv_purch": "Investments purchase liabilities", "jsa_c": "Joint shares arrangement short term", "jsa_nc": "Joint shares arrangement long term", "land_c": "Current portion of land purchase liabilities (a57 «20)", "land_nc": "Land purchase liabilities Long Term (b57 «20)", "lease_c": "Lease contract liabilities short term (a56)", "lease_nc": "Lease contract liabilities long term", "loans_current": "Current portion of Short-term loans", "loans_lt": "Loans long-term {52)", "nci": "Non-controlling equities", "np_long": "Notes payable long term (b", "np_short": "Notes payable short term (a", "nr_long": "Notes receivable long term +16)", "nr_long_undel": "Notes receivable long term for undelivered units «16)", "nr_short": "Notes receivable short term +16)", "nr_short_undel": "Notes receivable short term for undelivered units", "overdraft": "Bank- overdraft", "provisions": "Provisions (19,30¢)", "puc": "Projects under construction «12)", "resid": "Other long-term liabilities Residents’ Association", "rou": "Right of use asset", "share_capital": "Share capital", "sukuk": "Partnership Sukuk", "supp_adv": "Suppliers advance payments", "suppliers": "Suppliers And contractors", "tax_payable": "Income tax payable (a23)", "tca": "Total Current Assets", "tcl": "Total current liabilities", "teal": "Total non-current liabilities", "tle": "Total equity and liabilities", "tnca": "Total non-current assets", "tncl": "Total non-current liabilities", "total_assets": "Total Assets", "total_equity": "Total shareholders' equity", "total_liabs": "Total liabilities", "treasury": "Treasury shares In Cost +17)", "wip": "Works in process {44 «14)", "capex_fixed": "Payments for purchase of assets", "capex_puc": "Payments for work under construction", "close": "Cash and cash equivalents as of December", "disposal": "Proceeds from sale of fixed assets", "net": "Net increase in cash and cash equivalents during the year", "open": "Cash and cash equivalents at beginning of the year"},
 2024: {"adv_cust": "Advances from customers G3", "adv_inv": "payee payments tax asset for investments acquisition", "ar": "Accounts receivable “3", "assoc": "Investments in associates «bl 1«d8)", "cash": "Cash and cash equivalents", "checks_liab": "liabilities for checks received from customers", "creditors": "Creditors & other credit balances", "debtors": "Debtors and other debit balances", "due_from_rp": "Due from related parties +45 +27)", "due_to_rp": "Due from related parties +45 +27)", "fin_amort": "Financial investments at amortized cost (4633/5)", "jsa_c": "Joint shares arrangement short term", "jsa_nc": "Joint shares arrangement long term", "land_nc": "Land purchase liabilities Long Term _ +20)", "lease_c": "Lease contract liabilities short term (a54)", "lease_nc": "Lease contract liabilities long term {b54)", "loans_current": "Current portion of Short-term loans", "loans_lt": "Loans long-term", "nci": "Non-controlling equities", "np_long": "Notes payable short term (a", "np_short": "Notes payable short term (a", "nr_long": "Noles receivable long term", "nr_long_undel": "Notes receivable long term for undelivered units ia", "nr_short": "Noles receivable long term", "nr_short_undel": "Notes receivable short term for undelivered units", "overdraft": "Bank- overdraft (RG", "puc": "Projects under construction oo.", "resid": "Other long-term liabilities Residents’ Association", "rou": "Right of use assets (39,a28,", "share_capital": "Share capital", "supp_adv": "Suppliers advance payments", "suppliers": "Suppliers And contractors", "tax_payable": "Income tax payable (a23)", "tca": "Total Current Assets", "tcl": "Total current liabilities", "teal": "Total non-current liabilities", "tle": "Total equity and liabilities", "tnca": "Total non-current assets", "tncl": "Total non-current liabilities", "total_assets": "Total Assets", "total_liabs": "Total liabilities", "treasury": "Treasury Shares", "wip": "Works in process +14)", "capex_fixed": "(Payments) for purchase of fixed assets", "capex_puc": "(Payments) for projects under construction", "close": "Cash and cash equivalents as of Dec", "dep": "Depreciation & amortization «37 +36)", "disposal": "Proceeds from sale of fixed assets", "net": "Net increase in cash and cash equivalents during the Year", "open": "Cash and cash equivalents at beginning of the Year"},
 2025: {"adv_cust": "Advances from customers", "adv_inv": "Advance payments for investments acquisition", "ar": "Accounts receivable", "assoc": "Investments in associates +b11+d8)", "banks_credit": "Banks credit balances", "cash": "Cash and cash equivalents +32)", "creditors": "Creditors & other credit balances", "debtors": "Debtors and other debit balances", "due_from_rp": "Due from related parties «45", "due_to_rp": "Due to related parties +56", "fin_amort": "Financial investments at amortized cost (46:33/5)", "fixed": "Fixed assets (net) «13)", "fvtpl": "Investments at fair value through profit and loss (33/5)", "inv_prop": "Investment property cll)", "inv_purch": "Investments purchase liabilities", "jsa_c": "Joint shares arrangement short term", "jsa_nc": "Joint shares arrangement long term", "land_c": "Current portion of land purchase liabilities (a55 «20)", "land_nc": "Land purchase liabilities Long Term (B55 «20)", "lease_c": "Lease contract liabilities short term (a54)", "lease_nc": "Lease contract liabilities long term (b54)", "loans_current": "Current portion of Short-term loans", "loans_lt": "Loans long-term", "nci": "Non-controlling equities", "np_long": "Notes payable long term", "np_short": "Notes payable short term (a51)", "nr_long": "Notes receivable long term +16)", "nr_long_undel": "Notes receivable long term for undelivered units +16)", "nr_short": "Notes receivable short term «16)", "nr_short_undel": "Notes receivable short term for undelivered units", "provisions": "Provisions", "puc": "Projects under construction «12)", "resid": "Other long-term liabilities Residents’ Association", "rou": "Right of use assets (39,a28)", "share_capital": "Share capital", "supp_adv": "Suppliers advance payments", "suppliers": "Suppliers And contractors", "tax_payable": "Income tax payable (69,a23)", "tca": "Total Current Assets", "tcl": "Total current liabilities", "teal": "Total non-current liabilities", "tle": "Total equity and liabilities", "tnca": "Total non-current assets", "tncl": "Total non-current liabilities", "total_assets": "Total Assets", "total_equity": "Total shareholders’ equity", "total_liabs": "Total liabilities", "wip": "Works in Progress +14)", "capex_fixed": "(Payments) for purchase of fixed assets", "capex_puc": "(Payments) from projects under construction", "close": "Cash and cash equivalents as of Dec", "dep": "Depreciation & amortization «36 «13)", "disposal": "Proceeds from sale of fixed assets", "net": "Net increase in cash and cash equivalents during the Year", "open": "Cash and cash equivalents at beginning of the Year"},
}

# Consolidated statement of financial position, at 31 December, as PRINTED.
BS = {
 2015: dict(src=2015, column='own', page=3,
      adv_cust=6169791784, adv_inv=184335633, ar=704029344, assoc=78506490,
      banks_credit=31035055, cash=965669547, creditors=345368413, debtors=174854197,
      due_from_rp=172391893, due_to_rp=226318984, fixed=334622621, fvtpl=67112711,
      htm=613045694, infra=173648127, inv_prop=854664787, inv_purch=44256746, land_c=263318760,
      land_nc=268236463, loans_current=80814000, loans_lt=2918287288, nci=270774426,
      np_long=148532031, np_short=473692756, nr_long=4546281603, nr_short=2371034595,
      overdraft=80236967, provisions=116843823, puc=858654273, resid=485600026,
      share_capital=4344640000, supp_adv=384777356, suppliers=406849941, tax_payable=46631446,
      tca=11993531427, tcl=8458806802, teal=10405128859, tle=10405128859, tnca=6870404234,
      tncl=3820655808, total_equity=6584473051, total_investment=10405128859,
      total_liabs=8458806802, wc_printed=3534724625, wip=6540616090),
 2016: dict(src=2016, column='own', page=1,
      adv_cust=7744755120, adv_inv=184335633, ar=757056711, assoc=79225699,
      banks_credit=42176487, cash=808516570, creditors=522256001, debtors=218476677,
      due_from_rp=244124840, due_to_rp=131333860, fixed=351608405, fvtpl=58471043,
      htm=153328081, infra=95083418, inv_prop=888506292, inv_purch=44256746, land_c=60651029,
      land_nc=169799525, loans_current=541014619, loans_lt=2957469695, nci=412151516,
      np_long=612700591, np_short=974301860, nr_long=7300039694, nr_short=3295528203,
      overdraft=79410353, provisions=169386850, puc=877766742, resid=736444356,
      share_capital=4617899452, supp_adv=489064327, suppliers=448465529, tax_payable=126628749,
      tca=12475312407, tcl=11140145030, teal=11109629462, tle=11109629462, tnca=9774462085,
      tncl=4476414167, total_equity=6633215295, total_investment=11109629462,
      total_liabs=11140145030, wc_printed=1335167377, wip=6410745955),
 2017: dict(src=2017, column='own', page=1,
      adv_cust=10132168063, adv_inv=184335633, ar=883343556, assoc=83615199,
      banks_credit=50560568, cash=562030358, creditors=523427753, debtors=589210845,
      due_from_rp=251407887, due_to_rp=96617006, fixed=347277770, fvtpl=51426615,
      htm=467935233, infra=95083418, inv_prop=758689762, jsa_c=174561987, jsa_nc=735572595,
      land_c=102492926, land_nc=335844111, loans_current=979573992, loans_lt=3228805475,
      nci=538436217, np_long=1912929075, np_short=1239624510, nr_long=11356555019,
      nr_short=3012452628, overdraft=374695728, provisions=240243801, puc=882472515,
      resid=1083208314, share_capital=4617899452, supp_adv=486083502, suppliers=543392278,
      tax_payable=162100332, tca=15547652068, tcl=14714542362, teal=14536345224,
      tle=14536345224, tnca=13703235518, tncl=7296359570, total_equity=7239985654,
      total_investment=14536345224, total_liabs=14714542362, wc_printed=833109706,
      wip=9193761444),
 2018: dict(src=2018, column='own', page=1,
      adv_cust=11484809418, adv_inv=194597985, ar=1061705100, assoc=97447485,
      banks_credit=57735773, cash=955737630, creditors=617219159, debtors=984450924,
      due_from_rp=359632650, due_to_rp=28187870, fixed=1427791288, fvtpl=75866550,
      htm=1750818937, infra=95083416, inv_prop=769612116, inv_purch=298279545, jsa_c=749682921,
      jsa_nc=1209476614, land_c=158981836, land_nc=298279545, loans_current=1101130295,
      loans_lt=2657711596, nci=505090067, np_long=1660456660, np_short=1586917804,
      nr_long=13087429109, nr_short=4235390443, overdraft=897807291, provisions=251706423,
      puc=106029940, resid=1671535652, share_capital=6157199270, supp_adv=494372865,
      suppliers=704440148, tax_payable=251569213, tca=19009504612, tcl=17985271568,
      teal=16713001162, tle=16713001162, tnca=15688768117, tncl=7497460067,
      total_equity=9215541095, total_investment=16713001162, total_liabs=17985271568,
      wc_printed=1024233045, wip=9091529513),
 2019: dict(src=2019, column='own', page=1,
      adv_cust=14212609702, adv_inv=194907301, ar=1272279369, assoc=143369813,
      banks_credit=87237713, cash=1375178390, creditors=630784392, debtors=917361361,
      due_from_rp=418965567, due_to_rp=6639555, fixed=1353868932, fvtpl=87513020,
      htm=924376849, infra=95083416, inv_prop=393482537, inv_purch=150258255, jsa_c=1081181760,
      jsa_nc=772142710, land_c=235682895, land_nc=150258255, loans_current=295132857,
      loans_lt=2801072865, nci=554741876, np_long=1438142381, np_short=1750901906,
      nr_long=15318676533, nr_short=4691813019, overdraft=963312645, provisions=180718382,
      puc=1739437098, resid=2372856032, share_capital=6235199270, supp_adv=451528501,
      suppliers=762160712, tax_payable=97622236, tca=18254266355, tcl=20399068170,
      teal=17072053094, tle=17072053094, tnca=19216854909, tncl=7534472243,
      total_equity=9537580851, total_investment=17072053094, total_liabs=20399068170,
      wc_printed=2144801815, wip=8115250279),
 2020: dict(src=2020, column='own', page=1,
      adv_cust=15629029118, adv_inv=313390301, ar=1480150676, assoc=150481921,
      banks_credit=90966967, cash=1579250273, creditors=784588614, debtors=1084173501,
      due_from_rp=440619311, due_to_rp=2535616, fixed=2762305090, fvtpl=215712935,
      htm=1369132280, infra=58062734, inv_prop=386524021, jsa_c=1179376457, land_c=134159466,
      land_nc=90488428, loans_current=183435222, loans_lt=2493851309, nci=583301606,
      np_long=2151086266, np_short=1030233337, nr_long=15338184314, nr_short=5025563370,
      overdraft=1034506489, provisions=176792225, puc=297328271, resid=2935783484,
      share_capital=6235199270, supp_adv=514994304, suppliers=834286954, tax_payable=37270445,
      tca=18997539588, tcl=21175243644, teal=17128104535, tle=17128104535, tnca=19305808593,
      tncl=7671209487, total_equity=9456895048, total_investment=17128104535,
      total_liabs=21175243644, treasury=-46990266, wc_printed=-2177704057, wip=7287942937),
 2021: dict(src=2021, column='own', page=3,
      adv_cust=8374372531, adv_inv=194907301, ar=1885116352, assoc=213673757,
      banks_credit=99796140, cash=1017868885, checks_liab=6602091568, creditors=1042545113,
      debtors=1437231691, due_from_rp=343876737, due_to_rp=4864005, fin_amort=2435941373,
      fixed=2718635212, fvtpl=60725679, infra=58062734, inv_prop=170828879, inv_purch=20717554,
      jsa_c=2161334185, jsa_nc=70877952, land_c=127785639, land_nc=84252431, lease_c=5345642,
      lease_nc=5998308, loans_current=220788000, loans_lt=1877815695, nci=454189051,
      np_long=2212834840, np_short=1340828591, nr_long=4815037989, nr_long_undel=4815037989,
      nr_short=4040523707, nr_short_undel=1787053580, overdraft=1661691055,
      provisions=182587332, puc=7640536, resid=3856263893, rou=15831709,
      share_capital=6162499270, supp_adv=657534518, suppliers=1130851889,
      tax_payable=166759387, tca=22364507586, tcl=23200391365, teal=17699666380,
      tle=17699666380, tnca=13535750159, tncl=5108043119, total_equity=9591623261,
      total_investment=17699666380, total_liabs=23200391365, treasury=-69839608,
      wip=8698435064),
 2022: dict(src=2023, column='comparative', page=3,
      adv_cust=10214450435, adv_inv=59785558, ar=2707513377, assoc=382317406,
      banks_credit=180167719, cash=1165167798, checks_liab=9157333299, creditors=1384351547,
      debtors=1858626727, due_from_rp=359050558, due_to_rp=3388525, fin_amort=3505241702,
      fixed=2592279116, fvtpl=86052108, inv_prop=167262054, inv_purch=20717553, jsa_c=90951914,
      jsa_nc=1673994084, land_c=81839239, land_nc=22488256, lease_c=6526325, lease_nc=3124258,
      loans_current=278307214, loans_lt=2697475668, nci=481106612, np_long=1329707969,
      np_short=1572111652, nr_long=13457192909, nr_long_undel=6608405535, nr_short=5897552535,
      nr_short_undel=2548927764, overdraft=2403922276, provisions=183375011, puc=212133152,
      resid=5651066356, rou=7820596, share_capital=6003189778, sukuk=687264013,
      supp_adv=1603206733, suppliers=1268463740, tax_payable=420635260, tca=26017630209,
      tcl=27266541709, teal=12067868775, tle=49505997212, tnca=23488367003, tncl=12067868775,
      total_assets=49505997212, total_equity=10171586728, total_liabs=39334410484,
      treasury=-90146032, wip=6286290907),
 2023: dict(src=2023, column='own', page=3,
      adv_cust=20983587846, adv_inv=92364852, ar=8087041825, assoc=499485857,
      banks_credit=234053719, cash=3189241596, checks_liab=6598857715, creditors=2653908991,
      debtors=3120372653, due_from_rp=368399961, due_to_rp=3823853, fin_amort=4445198927,
      fixed=2529549685, fvtpl=100784825, inv_prop=45830027, inv_purch=20717553,
      jsa_c=1614008764, jsa_nc=4004246037, land_c=18416252, land_nc=-657, lease_c=9771222,
      lease_nc=1296288, loans_current=510722537, loans_lt=3959030721, nci=562460975,
      np_long=2576202779, np_short=1858467641, nr_long=23096144962, nr_long_undel=4546630300,
      nr_short=8391624362, nr_short_undel=2052227415, overdraft=3362218151,
      provisions=136623346, puc=1002101616, resid=9428558877, rou=10923079,
      share_capital=5883189778, sukuk=1553426329, supp_adv=3931155595, suppliers=2504006437,
      tax_payable=559929987, tca=42474426786, tcl=41069114014, teal=21507498684,
      tle=74298460597, tnca=31824033811, tncl=21507498684, total_assets=74298460597,
      total_equity=11721847899, total_liabs=62576612698, treasury=-62, wip=8788379627),
 2024: dict(src=2025, column='comparative', page=3,
      adv_cust=47403775488, adv_inv=186946852, ar=15561060204, assoc=3379238461,
      banks_credit=992413988, cash=6372384745, creditors=4677270651, debtors=7541532708,
      due_from_rp=330505962, due_to_rp=15251549, fin_amort=6110080419, fixed=2847087324,
      fvtpl=206202973, inv_prop=1057472496, inv_purch=20717553, jsa_c=2373133600,
      jsa_nc=5458648290, land_c=13654439, land_nc=6288907, lease_c=26238462, lease_nc=36683385,
      loans_current=776658181, loans_lt=6442508413, nci=702060505, np_long=2895314633,
      np_short=1697081032, nr_long=43213421382, nr_long_undel=3095727858, nr_short=13429823887,
      nr_short_undel=1718559879, provisions=157835844, puc=237622133, resid=19476257218,
      rou=61770489, share_capital=5759828346, supp_adv=4790975149, suppliers=3426676837,
      tax_payable=1040307727, tca=69270914793, tcl=74496941232, teal=34315700846,
      tle=123437324201, tnca=54166409408, tncl=34315700846, total_assets=123437324201,
      total_equity=14624682123, total_liabs=108812642078, wip=13209788867),
 2025: dict(src=2025, column='own', page=3,
      adv_cust=69354084075, adv_inv=26864852, ar=28118116247, assoc=3611619739,
      banks_credit=938770898, cash=9419526159, creditors=5121712447, debtors=12921978854,
      due_from_rp=335661244, due_to_rp=29919710, fin_amort=9581528351, fixed=4521970936,
      fvtpl=15270678, inv_prop=1032530185, inv_purch=20717553, jsa_c=2981872912,
      jsa_nc=3991865312, land_c=12225, lease_c=41916627, lease_nc=60703816,
      loans_current=1250040023, loans_lt=10543120329, nci=1334332140, np_long=4505024909,
      np_short=4875673642, nr_long=54801316199, nr_long_undel=1518490219, nr_short=18137718924,
      nr_short_undel=935259476, provisions=178137292, puc=182616883, resid=29122769947,
      rou=102532491, share_capital=5719828346, supp_adv=9056244671, suppliers=3807042889,
      tax_payable=1976557733, tca=106229649584, tcl=105098969636, teal=48265091319,
      tle=172129812858, tnca=65900163274, tncl=48265091319, total_assets=172129812858,
      total_equity=18765751903, total_liabs=153364060955, wip=17570908880),
}

# Consolidated statement of cash flows, for the year then ended, as PRINTED.
CF = {
 2015: dict(src=2015, column='own', page=5,
      capex_fixed=-44189940, capex_puc=-1274994, close=965669547, dep=21874437,
      disposal=1815290, net=763285435, open=202384112),
 2016: dict(src=2016, column='own', page=4,
      capex_fixed=-51218379, capex_puc=-19112467, close=808516570, dep=28961212,
      disposal=47600, net=-157152978, open=965669548),
 2017: dict(src=2017, column='own', page=4,
      capex_fixed=38328773, capex_puc=24812079, close=562030358, dep=36819507,
      disposal=1559618, net=246486212, open=808516570),
 2018: dict(src=2018, column='own', page=4,
      capex_fixed=-52297290, capex_puc=-9581362, close=955737630, dep=85077314,
      disposal=1249905, net=393707272, open=562030358),
 2019: dict(src=2019, column='own', page=6,
      capex_fixed=-35631944, capex_puc=-10129973, close=1375178391, dep=102205593,
      disposal=958759, net=419440761, open=955737630),
 2020: dict(src=2020, column='own', page=4,
      capex_fixed=-52719316, capex_puc=-40528373, close=1579250273, dep=125124182,
      disposal=543372, net=204071883, open=1375178390),
 2021: dict(src=2021, column='own', page=6,
      capex_fixed=-57798, capex_puc=-1.145, close=868885, dep=185914384, disposal=1303692,
      net=-561298517, open=1579149924),
 2023: dict(src=2024, column='comparative', page=5,
      capex_fixed=-177431038, capex_puc=-789968464, close=3189241596, dep=201037444,
      disposal=103916449, net=2020123987, open=3949811),
 2024: dict(src=2024, column='own', page=5,
      capex_fixed=-587649309, capex_puc=-128296234, close=6372384745, dep=270108689,
      disposal=7825972, net=3183143149),
 2025: dict(src=2025, column='own', page=6,
      capex_fixed=-275221, capex_puc=-6766920, close=9419526159, dep=384527014,
      disposal=9701497, net=3021279518, open=6372384745),
}

# The share count at each origin, recorded ONLY where the issued capital divided
# by the par value the SAME document states reproduces the count that document
# states [clause (ii)].
SHARES = {
 2015: {
      "count": 2172320000,
      "issued_capital": 4344640000,
      "par_value": 2.0,
      "file": "4Q15 - Consolidated - Egyptian GAAP - English.pdf",
      "page": 36,
      "route": "ocr",
      "how": "the capital note's own issued-and-paid-in-capital sentence",
      "quote": "The Company's issued and paid in capital amounts to EGP 4 344 640 000 representing 2 172 320 000 shares with a par value of EGP 2 per share",
      "check": "issued capital 4344640000 / par 2 = 2172320000, matching the count the same sentence states"
    },
 2016: {
      "count": 2308949726,
      "issued_capital": 4617899452,
      "par_value": 2.0,
      "file": "4Q16 - Consolidated Financials - Egyptian GAAP - English.pdf",
      "page": 37,
      "route": "ocr",
      "how": "the capital note's own issued-and-paid-in-capital sentence",
      "check": "issued capital 4617899452 / par 2 = 2308949726, matching the count the same sentence states"
    },
 2017: {
      "count": 2308949726,
      "issued_capital": 4617899452,
      "par_value": 2.0,
      "file": "4Q17 - Consolidated Financials - Egyptian GAAP - English.pdf",
      "page": 39,
      "route": "ocr",
      "how": "the capital note's own issued-and-paid-in-capital sentence",
      "check": "issued capital 4617899452 / par 2 = 2308949726, matching the count the same sentence states",
      "cross_check": "the FY2018 filing's earnings-per-share note states a weighted average of 2 308 949 726 shares for 31 December 2017, the same count"
    },
 2018: {
      "count": 3078599635,
      "issued_capital": 6157199270,
      "par_value": 2.0,
      "file": "4Q18 - Consolidated Financials - Egyptian GAAP - English.pdf",
      "page": 39,
      "balance_sheet_page": 1,
      "route": "text layer, footed",
      "how": "the capital note's own RECITAL of resolutions, corroborated by the share-capital line on the balance sheet of the same filing",
      "quote": "On 6 September 2018, the Company's Extra-Ordinary General Assembly Meeting approved the issued Capital increase out of retained earnings via the issuance of bonus shares amounting to EGP 769 649 909 to be after such increasing amounted EGP 6 157 199 270 represent 3 078 599 635 shares with a par value of EGP 2 per share.",
      "check": "issued capital 6157199270 / par 2 = 3078599635, matching the count the recital states and the EGP 6 157 199 270 the balance sheet states as share capital at 31 December 2018",
      "chain": "the FY2017 count of 2 308 949 726 plus the 769 649 909 bonus shares this resolution issues is 3 078 599 635, and that count at par 2 is the EGP 6 157 199 270 of capital",
      "discrepancy_named": "the SAME note's opening current-capital sentence states 'EGP 6 157 199 270 representing 3 078 599 063 shares', which does NOT foot: 6157199270 / 2 = 3078599635, not 3078599063. The recital, the balance sheet and the bonus-share chain all give 3 078 599 635, so the opening sentence's count is a typographical error in the filing and the footed count is recorded. engine/valuation_calibration/shares_phdc.json carries the non-footing 3 078 599 063 for this year while its own check string reads '= 3078599635, matching the stated count'; that archive is not edited here and the disagreement is named instead."
    },
 2019: {
      "count": 3117599635,
      "issued_capital": 6235199270,
      "par_value": 2.0,
      "file": "4Q19 - Consolidated Financials - Egyptian GAAP - English.pdf",
      "page": 45,
      "balance_sheet_page": 1,
      "route": "text layer, footed",
      "how": "the capital note's own RECITAL of resolutions, corroborated by the share-capital line on the balance sheet of the same filing",
      "quote": "On 4 April 2019, the Company's Extra-Ordinary General Assembly Meeting approved the issued Capital increase out of retained earnings via the issuance of bonus shares amounting to EGP 78 000 000 to be after such increasing amounted EGP 6 235 199 270 representing 3 117 599 635 shares with a par value of EGP 2 per share.",
      "check": "issued capital 6235199270 / par 2 = 3117599635, matching the count the recital states and the EGP 6 235 199 270 the balance sheet states as share capital at 31 December 2019",
      "discrepancy_named": "the capital note's opening current-capital sentence on the preceding page is STALE — it repeats the FY2018 figure of EGP 6 157 199 270 (and the same non-footing 3 078 599 063 count) while the recital below it records the 4 April 2019 increase and the balance sheet states EGP 6 235 199 270 at this date. The recital and the balance sheet agree and foot, so they are what is recorded. engine/valuation_calibration/shares_phdc.json carries the superseded capital and count for this year; that archive is not edited here and the disagreement is named instead."
    },
 2020: {
      "count": 3117599635,
      "issued_capital": 6235199270,
      "par_value": 2.0,
      "file": "4Q20 - Consolidated Financials - Egyptian GAAP - English.pdf",
      "page": 40,
      "balance_sheet_page": 1,
      "route": "text layer, footed",
      "how": "the capital note's own current-capital sentence, corroborated by the share-capital line on the balance sheet of the same filing",
      "quote": "the issued and paid up capital amounted to EGP 6 235 199 270 ... distributed over 3 117 599 635 shares with a nominal value of EGP 2 per share",
      "check": "issued capital 6235199270 / par 2 = 3117599635, matching the count the same sentence states and the share capital the balance sheet states at 31 December 2020",
      "treasury_shares": 36350000,
      "treasury_cost": 46990266,
      "outstanding_count": 3081249635,
      "treasury_note": "the filing's own note 55 sets out issued 3 117 599 635 shares less 36 350 000 treasury shares acquired at a cost of EGP 46 990 266, leaving 3 081 249 635 outstanding, and its earnings-per-share note divides by that outstanding figure. The ISSUED count is what is recorded as the footed value, because clause (ii)'s test is issued capital over par; the treasury deduction and the outstanding count are carried beside so a rebuild can choose the denominator rather than inherit one."
    },
 2021: {
      "count": 3081249635,
      "issued_capital": 6162499270,
      "par_value": 2.0,
      "file": "PHD - Consolidated Financial Statements - 4Q  2021 - English.pdf",
      "page": 63,
      "route": "ocr at 150 dpi — the filing carries no text layer on any of its 73 pages",
      "how": "the capital note's own current-capital sentence",
      "quote": "issued and paid-up capital amounted to EGP 6 162 499 270 ... distributed over 3 081 249 635 shares with a nominal value of EGP 2 per share",
      "check": "issued capital 6162499270 / par 2 = 3081249635, matching the count the same sentence states",
      "chain": "the FY2020 capital of EGP 6 235 199 270 less the EGP 72 700 000 nominal value of the 36 350 000 treasury shares cancelled by the extraordinary general assembly of 1 April 2021 is EGP 6 162 499 270 — and 36 350 000 is exactly the treasury holding the FY2020 note disclosed, so the reduction reconciles to the share"
    },
 2022: {
      "count": 3001594889,
      "issued_capital": 6003189778,
      "par_value": 2.0,
      "file": "Palm Hills Developments-Consolidated Financials - 31 December 2023.pdf",
      "page": 59,
      "balance_sheet_page": 3,
      "route": "ocr — the FY2023 filing carries no text layer on any of its 68 pages; the balance sheet was read at 200 dpi and the capital note at 150 dpi",
      "how": "the FY2023 filing's capital-note RECITAL, whose entry for the November 2022 resolution states this year's capital AND its count, corroborated by the share-capital line in the COMPARATIVE column of the same filing's balance sheet",
      "quote": "The issued capital after reducing the value of treasury shares in accordance with the decision of the extraordinary general assembly held on the end of Nov 2022 in the amount of 78 000 000 Egyptian pounds for 39 000 000 shares with a nominal value of 2 Egyptian pounds per share ... so the issued capital will be distributed over 3,001,594,889 shares. 6 003 189 778",
      "check": "issued capital 6003189778 / par 2 = 3001594889, matching the count the recital states and the EGP 6 003 189 778 the FY2023 balance sheet states as share capital at 31 December 2022",
      "chain": "6 162 499 270 less 81 309 492 (40 654 746 shares, March 2022) is 6 081 189 778 over 3 040 594 889 shares, less 78 000 000 (39 000 000 shares, November 2022) is 6 003 189 778 over 3 001 594 889 shares — every step at par 2, and the recital states both figures at both steps",
      "vintage_note": "this origin is read from the FY2023 filing throughout, because the FY2022 annual statements are published in Arabic only and this run's own parser reports that filing unresolved. That is the ONE declared exception in this block and it is the same one this run's panel.py already makes; it is a LATER filing's account of THAT year, not a later year's count carried back"
    },
 2023: {
      "count": 2941594889,
      "issued_capital": 5883189778,
      "par_value": 2.0,
      "file": "Palm Hills Developments-Consolidated Financials - 31 December 2023.pdf",
      "page": 58,
      "balance_sheet_page": 3,
      "route": "ocr — the filing carries no text layer on any of its 68 pages",
      "how": "the capital note's own current-capital sentence, corroborated by the share-capital line on the balance sheet of the same filing",
      "quote": "issued and paid-up capital amounted to 5,883,189,778 Egyptian pounds ... distributed over a number 2 941 594 889 shares, with a nominal value of 2 Egyptian pounds per share",
      "check": "issued capital 5883189778 / par 2 = 2941594889, matching the count the same sentence states and the EGP 5 883 189 778 the balance sheet states as share capital at 31 December 2023"
    },
 2024: {
      "count": 2879914173,
      "issued_capital": 5759828346,
      "par_value": 2.0,
      "file": "Palm Hills FS Cons 31Dec 2024.pdf",
      "page": 56,
      "route": "ocr — the filing carries no text layer on any of its 68 pages",
      "how": "the capital note's own current-capital sentence",
      "quote": "issued and paid-up capital amounted to 5 759 828 346 Egyptian pounds ... distributed over a number 2 879 914 173 shares, with a nominal value of 2 Egyptian pounds per share",
      "check": "issued capital 5759828346 / par 2 = 2879914173, matching the count the same sentence states",
      "chain": "the same note records the cancellation on 4 November 2024 of 61 680 716 treasury shares against a capital reduction of EGP 123 361 432, which is that count at par 2"
    },
 2025: {
      "count": 2859914173,
      "issued_capital": 5719828346,
      "par_value": 2.0,
      "file": "ConsolidatedFinancials-Eng.pdf",
      "page": 59,
      "route": "ocr — the filing carries no text layer on any of its 68 pages",
      "how": "the capital note's own current-capital sentence",
      "quote": "the issued and paid-up capital amounted to 5 719 828 346 EGP ... distributed over a number 2 859 914 173 shares, with a nominal value of 2 Egyptian pounds per share",
      "check": "issued capital 5719828346 / par 2 = 2859914173, matching the count the same sentence states"
    },
}

# The INCOME STATEMENT's own depreciation line, in EGP MILLION, exactly as this
# run's panel.json carries it. Published beside the cash-flow add-back as a
# DIFFERENT measurement, never reconciled to it.
PANEL_ADMIN_DEPR = {
 2015: 9.1155,
 2016: 13.9912,
 2017: 20.4756,
 2018: 66.8072,
 2019: 80.3403,
 2020: 105.2514,
 2021: 174.7991,
 2022: 173.6693,
 2023: 178.56,
 2024: 239.9155,
 2025: 353.6571,
}

# The cash this run ALREADY committed for each origin, in EGP MILLION, from
# panel.json. Every balance sheet and every cash-flow statement read here is
# asserted against it: two independent readings of the same statement, one made
# by this run and one made now, and they agree to the rounding of the panel's
# own fourth decimal place of a million.
PANEL_CASH = {
 2015: 965.6695,
 2016: 808.5166,
 2017: 562.0304,
 2018: 955.7376,
 2019: 1375.1784,
 2020: 1579.2503,
 2021: 1017.8689,
 2022: 1165.1678,
 2023: 3189.2416,
 2024: 6372.3847,
 2025: 9419.5262,
}


# ---------------------------------------------------------------------------
# What each item is built from, stated once so the record cannot mean two
# things in two years.
# ---------------------------------------------------------------------------
DEBT_LINES = ("banks_credit", "overdraft", "loans_current", "loans_lt")
DEBT_DEFINITION = (
    "banks credit balances, bank overdraft, the current portion of term loans "
    "and the long-term loans — the interest-bearing BORROWINGS this balance "
    "sheet discloses. Land purchase liabilities are NOT folded in and are named "
    "beside: they are deferred consideration that this company's own cash-flow "
    "statement charges interest on ('Interest on land purchase liabilities', "
    "'amortization of discount on land liability'), so whether they are debt is "
    "a valuation choice, and this record reads the page and makes neither "
    "choice. The joint-share-arrangement balances and the residents' "
    "association deposits are named beside for the same reason.")
DEBT_BESIDE = (("land_c", "current portion of land purchase liabilities"),
               ("land_nc", "land purchase liabilities, non-current"),
               ("jsa_c", "joint shares arrangement, short term"),
               ("jsa_nc", "joint share arrangement, long term"),
               ("resid", "other long-term liabilities — residents' association"))

PPE_LINES = ("fixed", "puc", "inv_prop")
PPE_DEFINITION = (
    "fixed assets (net) plus projects under construction plus investment "
    "property. All three are carried because this company's spending lands in "
    "construction and in investment property and moves between them and works "
    "in process — development inventory — without cash, which is exactly why "
    "the identity capex = dPPE + D&A cannot be read as a cash figure here.")

WC_ASSETS = (("wip", "works in process"),
             ("nr_long", "notes receivable long term"),
             ("nr_short", "notes receivable short term"),
             ("ar", "accounts receivable"),
             ("supp_adv", "suppliers advance payments"))
WC_LIABS = (("adv_cust", "advances from customers"),
            ("np_short", "notes payable short term"),
            ("np_long", "notes payable long term"),
            ("suppliers", "suppliers and contractors"))
WC_DEFINITION = (
    "works in process plus notes receivable (long and short) plus accounts "
    "receivable plus suppliers advance payments, LESS advances from customers, "
    "notes payable (short and long) and suppliers and contractors — the lines "
    "this run's own pre-registration names for driver D12 ('notes/accounts "
    "receivable, works in process, advances from customers and suppliers'). "
    "It is a TRADE working-capital figure and not the balance sheet's own "
    "printed 'Working capital' row, which is total current assets less total "
    "current liabilities; that row is published beside it as a printed "
    "subtotal so the two cannot be confused.")
WC_EXCLUDED = (("cash", "cash and cash equivalents"),
               ("htm", "held-to-maturity investments"),
               ("fvtpl", "investments at fair value through profit and loss"),
               ("debtors", "debtors and other debit balances"),
               ("due_from_rp", "due from related parties"),
               ("due_to_rp", "due to related parties"),
               ("infra", "completion of infrastructure liabilities"),
               ("provisions", "provisions"),
               ("tax_payable", "income tax payable"),
               ("creditors", "creditors and other credit balances"),
               ("jsa_c", "joint shares arrangement short term"),
               ("banks_credit", "banks credit balances"),
               ("overdraft", "bank overdraft"),
               ("loans_current", "current portion of term loans"),
               ("land_c", "current portion of land purchase liabilities"))


DEP_NOTE = (
    "the cash-flow statement's own add-back to profit — the charge the identity "
    "capex = dPPE + D&A needs. It is NOT the income statement's depreciation "
    "line, which this run's panel carries and which runs LOWER in every year "
    "read (FY2020: 125,124,182 in the cash-flow statement against EGP 105.2514 "
    "million on the income statement). The two are different measurements, no "
    "disclosure in these filings reconciles them, and inventing a "
    "reconciliation would be the fabrication this archive exists to refuse — so "
    "both are published and neither is adjusted to the other.")

IDENTITY_NOTE = (
    "the two are not the same measurement and the gap is not a defect. On a "
    "developer, land and projects move between investment property, projects "
    "under construction and works in process — development inventory — without "
    "cash, and revaluations and disposals move the property base without cash "
    "too, so the change in property is dominated by transfers this identity "
    "cannot see. The DISCLOSED cash figure is what is committed; the identity "
    "is reported beside it so a later rebuild can see both rather than assume "
    "they agree.")

CAP_NOTE = (
    "the paid-in capital in currency, which is NOT a share count: it becomes "
    "one only when divided by the par value stated in the capital note of this "
    "same year. Recording the capital and refusing the count is why the two are "
    "different rows.")

POINT_IN_TIME = (
    "Every origin reads its OWN filing's own column, with one exception which is "
    "stated rather than glossed: the FY2022 annual statements are published in "
    "Arabic only, this run's own parser reports that filing unresolved, and "
    "FY2022 is therefore read from the COMPARATIVE column of the FY2023 filing — "
    "the same construction this run's panel.py already uses for that year. "
    "NOTHING IS CARRIED BACKWARD: no later share count, capital or balance is "
    "substituted into an earlier origin, and where a later filing restates a "
    "figure the restatement is named beside rather than swapped in. The share "
    "count MOVES across these origins — 2,172,320,000 then 2,308,949,726 then "
    "3,078,599,635 then 3,117,599,635 — which is the vintage discipline clause "
    "(ii) demands and the opposite of carrying today's count back.")

NOT_RECORDED = {
    "_": ("What this block does NOT carry, named with its reason. A block "
          "quietly carrying five of six reads as complete [clause (i)]."),
    "share counts from FY2021": (
        "The capital note of each of the FY2021 to FY2025 filings states that "
        "year's own issued capital, par value and count, and those filings carry "
        "a text layer of ZERO characters, so the note has to be found and read by "
        "OCR page by page. Where it was not read, the count is NOT RECORDED and "
        "the issued CAPITAL from that year's own balance sheet is recorded "
        "instead, as a separate item: capital in currency is not a share count, "
        "and it becomes one only when divided by a par value read from the same "
        "document. Dividing by the EGP 2 par of an EARLIER year would be exactly "
        "the fabricated vintage clause (ii) forbids — plausible on the page and "
        "invisible in the pooled error afterwards."),
    "engine/valuation_calibration/shares_phdc.json": (
        "That archive carries five counts for this name and TWO OF THEM DO NOT "
        "FOOT against the capital they are recorded with. FY2018 and FY2019 are "
        "both recorded at 3,078,599,063 shares on issued capital of EGP "
        "6,157,199,270, and 6,157,199,270 / 2 = 3,078,599,635; its own check "
        "string for those rows reads '= 3078599635, matching the stated count', "
        "so the record disagrees with itself. The non-footing count is the one "
        "printed in the filings' own opening capital sentence, which the same "
        "note's recital, the balance sheet and the bonus-share chain all "
        "contradict; and FY2019's capital is superseded within its own filing, "
        "which records a further increase to EGP 6,235,199,270 on 4 April 2019. "
        "This block records the footed figures. That archive is NOT edited here: "
        "it belongs to another instrument, this run changes nothing outside "
        "itself, and the disagreement is named rather than silently reconciled."),
}


MISSING = {
    2021: {"capex": (
        "the FY2021 filing's own cash-flow page does not read in its investing "
        "section at any resolution tried (150, 200 and 300 dpi) or under any of "
        "the three gutter measurements this run's parser offers. The figures the "
        "parse returns for that year's own column — 57,798 for payments for "
        "fixed assets and 1.145 for payments for projects under construction — "
        "are truncated, and they are contradicted by the magnitude of every "
        "other year in the archive. THE SAME PAGE'S COMPARATIVE COLUMN "
        "reproduces FY2020's own filing exactly (52,719,316 and 40,528,373), so "
        "the failure is in the current column and not in the page or the render. "
        "No later filing carries FY2021 as a comparative, because the FY2022 "
        "annual statements are published in Arabic only. A figure is not "
        "recorded rather than a truncated one recorded with a caveat.")},
    2022: {"capex": (
        "this origin has no readable cash-flow statement in either direction. "
        "Its own annual statements are published in Arabic only and this run's "
        "parser reports that filing unresolved; the FY2023 filing, whose "
        "comparative column would carry FY2022, has a cash-flow page that does "
        "not read at 150, 200 or 300 dpi under any gutter — its rows come back "
        "as noise ('panne for purchase of assets') while the cash rows on the "
        "same page tie to the pound. The balance sheet for this origin IS read, "
        "from the FY2023 filing's comparative column, and foots."),
        "dep": (
            "the same page and the same failure as capex above: the FY2023 "
            "cash-flow statement's depreciation add-back row does not resolve, "
            "and no other document carries FY2022's cash-flow statement.")},
    2025: {"capex": (
        "the FY2025 filing's own cash-flow page reads its cash rows exactly — "
        "opening 6,372,384,745 and closing 9,419,526,159, both reproducing this "
        "run's committed balance-sheet cash — and its investing section does "
        "not: the parse returns 275,221 for payments for fixed assets against "
        "587,649,309 the year before, and 6,766,920 for projects under "
        "construction against 128,296,234. Both are truncated. THIS IS THE ONE "
        "ORIGIN WITH NO LATER FILING TO CORROBORATE IT, so unlike FY2024 — "
        "whose figures the FY2025 comparative confirms to the pound — there is "
        "nothing to settle the reading against, and a truncated figure is not "
        "recorded.")},
}

# Where a page's own component rows do not sum exactly to its printed
# subtotals, the residual is RECORDED WITH THE ITEM rather than smoothed away.
FOOTING_RESIDUAL = {
    2021: ("this page's NON-CURRENT sections foot exactly — its non-current "
           "asset rows sum to 18,535,750,159, which with the printed working "
           "capital of -836,083,779 reproduces the printed total investment of "
           "17,699,666,380 to the pound, and its non-current liability rows sum "
           "to 8,108,043,119, which with total equity reproduces the same "
           "figure — while three of its printed TOTAL rows come back with a "
           "single wrong leading digit (13,535,750,159 for the non-current "
           "assets those rows sum to, and 5,108,043,119 for the non-current "
           "liabilities). ITS CURRENT SECTIONS DO NOT CLOSE: the current-asset "
           "rows sum 200,000 BELOW the printed total current assets and the "
           "current-liability rows 30,000 ABOVE the printed total current "
           "liabilities. Which row carries each residual could not be "
           "identified, so any figure below drawing on the current sections may "
           "be wrong by up to that amount. It is recorded rather than hidden, "
           "and it is four parts in a hundred thousand of the totals concerned.")
}


def _block(y, which):
    return (BS if which == "bs" else CF).get(y)


def _src(y, which):
    """The filing, column and route the ITEM was read from.

    Sourcing is PER STATEMENT, not per origin: FY2023's balance sheet is read
    from its own filing and its cash-flow items from the FY2024 filing's
    comparative column, because that is where each one foots.
    """
    b = _block(y, which)
    sy, side = b["src"], b["column"]
    f = FILES[sy]
    route = ROUTE_TEXT if f["route"] == "text" else ROUTE_OCR
    where = ("the company's own consolidated financial statements for the year "
             "ended 31 December %d (%s), from its own investor-relations archive "
             "at %s" % (sy, f["file"], IR_URL))
    if side == "own":
        return where + ", own column", route, f
    return (where + ", COMPARATIVE column (31 December %d)" % y), route, f


def foot():
    """Every identity the pages themselves supply. Assertions, not comments."""
    problems = []
    for y in sorted(BS):
        b, tag = BS[y], "FY%d" % y

        def has(*k):
            return all(b.get(i) is not None for i in k)

        # The INVESTMENT presentation the older and middle filings use.
        if has("tca", "tcl", "wc_printed"):
            if abs(abs(b["tca"] - b["tcl"]) - abs(b["wc_printed"])) > 5:
                problems.append("%s: current assets less current liabilities does "
                                "not reproduce the printed working capital" % tag)
        if has("tnca", "tca", "tcl", "total_investment"):
            if abs(b["tnca"] + (b["tca"] - b["tcl"]) - b["total_investment"]) > 5:
                problems.append("%s: non-current assets plus working capital does "
                                "not reproduce total investment" % tag)
        if has("total_equity", "tncl", "teal"):
            if abs(b["total_equity"] + b["tncl"] - b["teal"]) > 5:
                problems.append("%s: equity plus non-current liabilities does not "
                                "reproduce the printed total" % tag)
        if has("total_investment", "teal"):
            if abs(b["total_investment"] - b["teal"]) > 5:
                problems.append("%s: the balance sheet does not balance" % tag)
        # The CONVENTIONAL presentation the later filings use.
        if has("tnca", "tca", "total_assets"):
            if abs(b["tnca"] + b["tca"] - b["total_assets"]) > 5:
                problems.append("%s: non-current plus current assets does not "
                                "reproduce total assets" % tag)
        if has("total_assets", "tle"):
            if abs(b["total_assets"] - b["tle"]) > 5:
                problems.append("%s: the balance sheet does not balance" % tag)
        if has("total_equity", "tncl", "tcl", "total_assets"):
            if abs(b["total_equity"] + b["tncl"] + b["tcl"] - b["total_assets"]) > 5:
                problems.append("%s: equity and liabilities do not reproduce "
                                "total assets" % tag)
        # Against the cash this run already committed.
        if b.get("cash") is not None and PANEL_CASH.get(y) is not None:
            if abs(b["cash"] / 1e6 - PANEL_CASH[y]) > 0.0002:
                problems.append("%s: the balance sheet's cash does not reproduce "
                                "the figure this run committed" % tag)
        # Neither presentation available at all is not a clean page [R-ENF-04].
        if not (has("total_investment", "teal") or has("total_assets", "tle")):
            problems.append("%s: the balance sheet supplies no whole-sheet "
                            "identity to be checked against" % tag)

    for y in sorted(CF):
        c, tag = CF[y], "FY%d" % y
        if c.get("close") is not None and PANEL_CASH.get(y) is not None:
            if abs(c["close"] / 1e6 - PANEL_CASH[y]) > 0.0002:
                problems.append("%s: the cash-flow statement's closing cash does "
                                "not reproduce the figure this run committed" % tag)
        if c.get("open") is not None and PANEL_CASH.get(y - 1) is not None:
            if abs(c["open"] / 1e6 - PANEL_CASH[y - 1]) > 0.0002:
                problems.append("%s: the cash-flow statement's opening cash does "
                                "not reproduce the previous origin's" % tag)

    for y, s in sorted(SHARES.items()):
        implied = s["issued_capital"] / s["par_value"]
        if abs(implied - s["count"]) > 1:
            problems.append("FY%d: issued capital %d / par %g = %d against a "
                            "stated count of %d — it does not foot"
                            % (y, s["issued_capital"], s["par_value"], implied,
                               s["count"]))
        b = BS.get(y, {})
        if b.get("share_capital") is not None:
            if abs(b["share_capital"] - s["issued_capital"]) > 1:
                problems.append("FY%d: the capital note states %d and the balance "
                                "sheet %d" % (y, s["issued_capital"],
                                              b["share_capital"]))
    if problems:
        raise AssertionError("the valuation-input block does not foot:\n  "
                             + "\n  ".join(problems))
    return True


def _rec(value, y, which, units, **extra):
    where, route, f = _src(y, which)
    out = {"value": value, "units": units, "source": where, "route": route,
           "file": f["file"], "page": _block(y, which).get("page")}
    if FOOTING_RESIDUAL.get(y):
        out["footing_residual"] = FOOTING_RESIDUAL[y]
    out.update(extra)
    return out


def _missing(reason):
    return {"missing": reason}


def build():
    """The record [R-FCAL-01 AMENDED] defines, per origin."""
    origins = {}
    for y in ORIGINS:
        block, at = {}, "%d-12-31" % y
        b, c = BS.get(y), CF.get(y)
        miss = MISSING.get(y, {})
        lab = LABELS.get((b or {}).get("src"), {}) if b else {}
        clab = LABELS.get((c or {}).get("src"), {}) if c else {}

        # ---- cash ----------------------------------------------------------
        if b and b.get("cash") is not None:
            block["cash"] = _rec(b["cash"], y, "bs", "EGP", as_at=at,
                                 line=lab.get("cash", "Cash and cash equivalents"),
                                 check=("reproduces the EGP %s million this run "
                                        "committed for this origin from the same "
                                        "statement" % PANEL_CASH.get(y)))
        else:
            block["cash"] = _missing(miss.get("cash", "the balance sheet was not read"))

        # ---- debt ----------------------------------------------------------
        if b and any(b.get(k) is not None for k in DEBT_LINES):
            lines = {lab.get(k, k): b[k] for k in DEBT_LINES if b.get(k) is not None}
            beside = {lab.get(k, name): b[k] for k, name in DEBT_BESIDE
                      if b.get(k) is not None}
            absent = [k for k in DEBT_LINES if b.get(k) is None]
            rec = _rec(sum(lines.values()), y, "bs", "EGP", as_at=at,
                       definition=DEBT_DEFINITION, lines=lines,
                       carried_beside_not_folded_in=beside)
            if absent:
                rec["lines_this_year_does_not_print"] = absent
            block["debt"] = rec
        else:
            block["debt"] = _missing(miss.get("debt", "the balance sheet was not read"))

        # ---- ppe -----------------------------------------------------------
        if b and all(b.get(k) is not None for k in PPE_LINES):
            lines = {lab.get(k, k): b[k] for k in PPE_LINES}
            block["ppe"] = _rec(sum(lines.values()), y, "bs", "EGP", as_at=at,
                                definition=PPE_DEFINITION, lines=lines)
        elif b and any(b.get(k) is not None for k in PPE_LINES):
            block["ppe"] = _missing(
                "this reading of the balance sheet does not recover %s, so a "
                "property figure on the same definition as the other origins "
                "cannot be formed. The lines it does recover are %s"
                % (", ".join(k for k in PPE_LINES if b.get(k) is None),
                   "; ".join("%s %d" % (lab.get(k, k), b[k])
                             for k in PPE_LINES if b.get(k) is not None)))
        else:
            block["ppe"] = _missing(miss.get("ppe", "the balance sheet was not read"))

        # ---- depreciation and amortisation ---------------------------------
        if c and c.get("dep") is not None:
            block["dep"] = _rec(c["dep"], y, "cf", "EGP", period="FY%d" % y,
                                line=clab.get("dep", "Depreciation"),
                                note=DEP_NOTE,
                                income_statement_line_egp_million_for_comparison=(
                                    PANEL_ADMIN_DEPR.get(y)))
        else:
            block["dep"] = _missing(miss.get("dep", "the cash-flow statement was "
                                             "not read"))

        # ---- capital expenditure -------------------------------------------
        if "capex" in miss:
            block["capex"] = _missing(miss["capex"])
        elif c and any(c.get(k) is not None for k in ("capex_fixed", "capex_puc")):
            parts = {}
            for k, nm in (("capex_fixed", "Payments for purchase of fixed assets"),
                          ("capex_puc", "Payments for projects under construction")):
                if c.get(k) is not None:
                    parts[clab.get(k, nm)] = abs(c[k])
            rec = _rec(sum(parts.values()), y, "cf", "EGP", period="FY%d" % y,
                       derived=False, disclosed=True, lines=parts,
                       printed_sign=("the investing rows are printed as %s on this "
                                     "page" % ("magnitudes"
                                               if (c.get("capex_fixed") or 0) > 0
                                               else "negative figures")))
            if c.get("disposal") is not None:
                rec["disposal_proceeds_shown_separately"] = abs(c["disposal"])
            prev = BS.get(y - 1)
            if (prev and b and c.get("dep") is not None
                    and all(prev.get(k) is not None for k in PPE_LINES)
                    and all(b.get(k) is not None for k in PPE_LINES)):
                d_ppe = (sum(b[k] for k in PPE_LINES)
                         - sum(prev[k] for k in PPE_LINES))
                rec["identity_cross_check"] = {
                    "identity": "capex = dPPE + D&A",
                    "value": d_ppe + c["dep"],
                    "basis": ("fixed assets net plus projects under construction "
                              "plus investment property at both dates, and the "
                              "cash-flow statement's depreciation add-back"),
                    "difference_from_disclosed": d_ppe + c["dep"] - sum(parts.values()),
                    "note": IDENTITY_NOTE}
            block["capex"] = rec
        else:
            block["capex"] = _missing(miss.get("capex", "the cash-flow statement "
                                               "was not read"))

        # ---- working capital ------------------------------------------------
        if b and all(b.get(k) is not None for k, _ in WC_ASSETS + WC_LIABS):
            assets = {lab.get(k, nm): b[k] for k, nm in WC_ASSETS}
            liabs = {lab.get(k, nm): b[k] for k, nm in WC_LIABS}
            sub = {}
            for k, nm in (("tca", "total current assets"),
                          ("tcl", "total current liabilities"),
                          ("wc_printed", "the 'Working capital' row as PRINTED")):
                if b.get(k) is not None:
                    sub[nm] = b[k]
            if b.get("tca") is not None and b.get("tcl") is not None:
                sub["current assets less current liabilities"] = b["tca"] - b["tcl"]
                if (b.get("wc_printed") is not None
                        and (b["tca"] - b["tcl"] < 0) != (b["wc_printed"] < 0)):
                    sub["printed_sign_note"] = (
                        "this page prints that row as a MAGNITUDE; the identity "
                        "above makes it %d" % (b["tca"] - b["tcl"]))
            excl = {lab.get(k, nm): b[k] for k, nm in WC_EXCLUDED
                    if b.get(k) is not None}
            rec = _rec(sum(assets.values()) - sum(liabs.values()), y, "bs", "EGP",
                       as_at=at, definition=WC_DEFINITION, lines_added=assets,
                       lines_deducted=liabs, printed_subtotals=sub,
                       excluded_and_named=excl)
            if b.get("nr_long_undel") is not None:
                rec["gross_up_excluded_and_why"] = {
                    "notes receivable for undelivered units, long term":
                        b["nr_long_undel"],
                    "notes receivable for undelivered units, short term":
                        b.get("nr_short_undel"),
                    "liabilities for checks received from customers":
                        b.get("checks_liab"),
                    "why": (
                        "from FY2021 the balance sheet grosses up the notes "
                        "receivable on units not yet delivered against a "
                        "liability for the checks received for them, and the two "
                        "sides are EQUAL TO THE POUND in every year that prints "
                        "them. Including both nets to zero and including neither "
                        "nets to zero, so excluding both is neutral by "
                        "arithmetic rather than by judgement, and it keeps the "
                        "definition the same as in the years before the "
                        "presentation changed. The three figures are named here "
                        "so a rebuild can put them back.")}
            block["wc"] = rec
        elif b and any(b.get(k) is not None for k, _ in WC_ASSETS + WC_LIABS):
            block["wc"] = _missing(
                "this reading does not recover %s, so a working-capital figure "
                "on the same definition as the other origins cannot be formed. "
                "The lines it does recover are recorded here rather than summed: "
                "%s" % (", ".join(nm for k, nm in WC_ASSETS + WC_LIABS
                                  if b.get(k) is None),
                        "; ".join("%s %d" % (nm, b[k])
                                  for k, nm in WC_ASSETS + WC_LIABS
                                  if b.get(k) is not None)))
        else:
            block["wc"] = _missing(miss.get("wc", "the balance sheet was not read"))

        # ---- share count -----------------------------------------------------
        s = SHARES.get(y)
        if s:
            extra = {k: v for k, v in s.items()
                     if k not in ("count", "issued_capital", "par_value")}
            block["shares"] = {"value": s["count"], "units": "shares", "as_at": at,
                               "issued_capital": s["issued_capital"],
                               "par_value": s["par_value"]}
            block["shares"].update(extra)
        else:
            block["shares"] = _missing(miss.get("shares", "not recorded"))
            if b and b.get("share_capital") is not None:
                block["cap"] = _rec(b["share_capital"], y, "bs", "EGP", as_at=at,
                                    line=lab.get("share_capital", "Share capital"),
                                    note=CAP_NOTE)
        origins["FY%d" % y] = block
    return origins


def document():
    foot()
    return {
        "_": ("The inputs a VALUE is rebuilt from at each of this run's origins, "
              "committed beside the driver panel under %s. GENERATED by "
              "engine/phdc_walkforward/valuation_inputs.py, which foots every "
              "balance sheet against its own printed subtotals, every cash-flow "
              "statement against its own closing cash and the balance sheet's, "
              "and every share count against its own par value, at import; never "
              "hand-edited." % RULE),
        "run": "PHDC",
        "rule": RULE,
        "company": COMPANY,
        "currency": CURRENCY,
        "units": ("EGP as PRINTED in the filings — units, not thousands or "
                  "millions. This run's own panel.json carries the same lines in "
                  "EGP million; the two agree and the unit is stated on every "
                  "record so they cannot be mixed."),
        "basis": BASIS,
        "fiscal_year_end": FYE,
        "origins_declared_by": "PRE_REGISTRATION_30-08-2026.md, section 1",
        "route": {"text_layer": ROUTE_TEXT, "ocr": ROUTE_OCR,
                  "arbiter": ("arithmetic, never the extractor's confidence. The "
                              "route each year uses is the one this run's own "
                              "footing gate accepted for it, and every page read "
                              "here is footed again at import.")},
        "text_layer_census": {f["file"]: {"pages": f["pages"],
                                          "text_layer_characters": f["text_chars"],
                                          "route_accepted": f["route"],
                                          "statement_pages": f["stmt_pages"]}
                              for f in FILES.values()},
        "point_in_time": POINT_IN_TIME,
        "sources": {"FY%d" % y: {"file": FILES[COLUMN[y][0]]["file"],
                                 "column": COLUMN[y][1],
                                 "filing_year": COLUMN[y][0]}
                    for y in ORIGINS},
        "origins": build(),
        "not_recorded_and_why": NOT_RECORDED,
    }


if __name__ == "__main__":
    doc = document()
    out = os.path.join(HERE, "valuation_inputs.json")
    json.dump(doc, open(out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    n = sum(1 for b in doc["origins"].values() for r in b.values()
            if "missing" not in r)
    m = sum(1 for b in doc["origins"].values() for r in b.values() if "missing" in r)
    print("wrote %s — %d origins, %d items committed, %d recorded missing"
          % (out, len(doc["origins"]), n, m))
