#!/usr/bin/env python3
"""SCEM walk-forward — the VALUATION-INPUT BLOCK, per origin [R-FCAL-01 AMENDED].

A driver panel is not a record a value can be rebuilt from, and the difference stays
invisible until something tries. Cash and equivalents, interest-bearing debt, PP&E,
depreciation and amortisation, the working-capital lines, the share count with the par
value it was footed against, and capital expenditure — from the same statements, under
the same point-in-time discipline as every other figure in this run.

BUILT AS THE RUN GOES, not retro-fitted. Every figure here is a copy out of a filing
this run has already parsed cell by cell for the driver panel.

WHAT IS MISSING IS RECORDED AS MISSING, with its reason, never omitted — a block
quietly carrying six of seven reads as complete.
"""
import json
import os

import panel as P

HERE = os.path.dirname(os.path.abspath(__file__))

ROUTE = ("OCR off the rendered pixels at 150dpi grayscale (tesseract, eng); all six of "
         "this issuer's filings are image-only scans with no usable text layer, and "
         "every figure is footed against a subtotal the filing itself prints")


def _src(y, statement):
    s = P.SOURCES[P.BS[y]['src']]
    return "%s — %s, %s (%s column)" % (s['file'], s['label'], statement,
                                        P.BS[y]['column'])


def block(y):
    b, c, i = P.BS[y], P.CF[y], P.IS[y]
    d = P.derived()[y]
    cash = b['cash'] + b['cash_blocked']
    ibd = (b['bank_facilities'] + b['lt_loans'] + b['st_loans_affiliates']
           + b['lease_lt'] + b['lease_st'])
    wc = (b['inventories'] + b['debtors'] + b['due_from_affiliates']
          + b['sundry_debtors'] + b['other_debit'] - b['suppliers'] - b['other_credit'])
    capex_disclosed = c['capex_ppe'] + c['capex_cwip']
    out = {
        "cash": dict(
            value=cash,
            source=_src(y, "balance sheet, cash at hand and in banks"
                           + (" plus cash blocked under the capital increase"
                              if b['cash_blocked'] else "")),
            route=ROUTE,
            note=("EGP %d of the total is blocked under the capital increase and is "
                  "shown separately on the face of the sheet" % b['cash_blocked'])
            if b['cash_blocked'] else "no blocked balance in this year"),
        "debt": dict(
            value=ibd,
            source=_src(y, "balance sheet, bank facilities + long-term loans + short-"
                           "term loans from affiliated companies + lease liabilities"),
            route=ROUTE,
            note=("INTEREST-BEARING ONLY [R-FCAL-01 trap (i)]. Suppliers, other credit "
                  "accounts, provisions and the deferred-tax liability pay no interest "
                  "and are excluded; total liabilities that year were EGP %d, which is "
                  "%.1fx this figure and is the denominator that manufactures a bias "
                  "looking exactly like evidence."
                  % (b['total_liabilities'], b['total_liabilities'] / ibd)
                  if ibd else "no interest-bearing borrowings")),
        "ppe": dict(
            value=b['ppe'],
            source=_src(y, "balance sheet, fixed assets (net), note 4"),
            route=ROUTE,
            note="construction work in process of EGP %d is carried separately and is "
                 "NOT included here" % b['cwip']),
        "dep": dict(
            value=c['depreciation'] + c['amortisation'],
            source=_src(y, "cash-flow statement, depreciation plus amortisation"),
            route=ROUTE,
            note="agrees with note 4's own charge for the year"),
        "capex": dict(
            value=capex_disclosed,
            source=_src(y, "cash-flow statement, payment for purchase of fixed assets "
                           "plus payment to construction works in progress"),
            route=ROUTE,
            derived=False,
            note=("DISCLOSED, not derived. The identity capex = dPP&E + D&A gives EGP "
                  "%.0f against this disclosed EGP %.0f; the two are cross-checked and "
                  "the disclosed figure is what is committed."
                  % (d.get('capex_identity', float('nan')) * 1e6, capex_disclosed)
                  if 'capex_identity' in d else
                  "DISCLOSED, not derived. FY2021 has no prior year in this panel, so "
                  "the identity cross-check is not computable and that is recorded "
                  "rather than the identity being run off a fabricated opening PP&E.")),
        "wc": dict(
            value=wc,
            source=_src(y, "balance sheet — inventories + debtors and notes receivable "
                           "+ due from affiliated companies + sundry debtors + other "
                           "debit accounts, less suppliers/creditors/notes payable and "
                           "other credit accounts"),
            route=ROUTE,
            components=dict(inventories=b['inventories'], debtors=b['debtors'],
                            due_from_affiliates=b['due_from_affiliates'],
                            sundry_debtors=b['sundry_debtors'],
                            other_debit=b['other_debit'], suppliers=b['suppliers'],
                            other_credit=b['other_credit']),
            note="OPERATING lines only: cash, debt, provisions and the deferred-tax "
                 "balances are excluded, so this is not a current-assets-less-current-"
                 "liabilities figure and does not pretend to be"),
        "shares": dict(
            value=b['capital'] / P.PAR_VALUE,
            issued_capital=b['capital'],
            par_value=P.PAR_VALUE,
            source=_src(y, "balance sheet, issued and paid-in capital, at the EGP 10 "
                           "par value note 27 states"),
            route=ROUTE,
            note=("FOOTED TWO WAYS. Issued capital over par gives %.0f shares, and that "
                  "count reproduces this year's PRINTED earnings per share of %.2f to "
                  "%.4f. TODAY'S COUNT IS NEVER CARRIED BACK: this company's count is "
                  "68,058,443 at FY2021, 133,065,867 at FY2022-FY2024 and 260,812,477 "
                  "at FY2025, and a carried count would be fabricated in vintage, "
                  "plausible on the page and invisible in the pooled error afterwards."
                  % (b['capital'] / P.PAR_VALUE, i['eps'],
                     i['pat'] / (b['capital'] / P.PAR_VALUE))) if y != "FY2025" else
                 ("FOOTED. Issued capital EGP 2,608,124,770 over the EGP 10 par gives "
                  "260,812,477 shares at 31-Dec-2025. The PRINTED EPS of 10.29 is "
                  "struck on a WEIGHTED-AVERAGE 222.0mn because the capital increase "
                  "converted during the year (note 27 states the 111/254-day split), so "
                  "the closing count deliberately does not reproduce it — and the "
                  "reviewed Q1-2026 EPS of 4.27 does reproduce on it, which is what "
                  "makes the reading unambiguous rather than a tolerance.")),
    }
    return out


def build():
    return {
        "_rule": "[R-FCAL-01 AMENDED 03-Sep-2026] — every fundamental walk-forward "
                 "commits a valuation-input block beside its driver panel, per origin, "
                 "from the same statements and under the same point-in-time discipline.",
        "_run": "SCEM fundamental walk-forward, 07-09-2026",
        "_scope": "LIGHT — five sourceable fiscal years, origins FY2021-FY2025, "
                  "horizons 1-3",
        "_route": ROUTE,
        "prior_year_anchor": {
            "FY2020": {
                "cash": dict(
                    value=17_035_796,
                    source="SCC-AFS-E-1222.pdf — audited financial statements for the "
                           "year ended 31 December 2022, cash-flow statement, "
                           "comparative column: 'Cash & cash equivalent at the "
                           "beginning of the period' for FY2021",
                    route=ROUTE,
                    note="THE ONLY FY2020 FIGURE THIS RUN CAN SOURCE. It is committed "
                         "here rather than as an origin because the run does not test "
                         "FY2020 and recording it as an origin would misstate what was "
                         "tested."),
                "everything_else": dict(
                    missing="The FY2021 filing is ARABIC and its figures are Eastern "
                            "Arabic numerals which no OCR route available here reads, "
                            "so FY2020's comparative column cannot be obtained. The "
                            "year is left out and the window shortened rather than "
                            "estimated; see fetch_attempts.json."),
            }
        },
        "origins": {y: block(y) for y in P.YEARS},
    }


if __name__ == '__main__':
    P.verify()
    rec = build()
    json.dump(rec, open(os.path.join(HERE, 'valuation_inputs.json'), 'w'), indent=1)
    print('valuation-input block: %d origins' % len(rec['origins']))
    print('%-8s %12s %12s %12s %10s %11s %12s %12s'
          % ('origin', 'cash', 'debt', 'PP&E', 'D&A', 'capex', 'WC', 'shares'))
    for y in P.YEARS:
        b = rec['origins'][y]
        print('%-8s %12.1f %12.1f %12.1f %10.1f %11.1f %12.1f %12.0f'
              % (y, b['cash']['value'] / 1e6, b['debt']['value'] / 1e6,
                 b['ppe']['value'] / 1e6, b['dep']['value'] / 1e6,
                 b['capex']['value'] / 1e6, b['wc']['value'] / 1e6,
                 b['shares']['value']))
