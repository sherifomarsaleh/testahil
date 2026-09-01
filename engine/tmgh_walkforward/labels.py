"""Label aliases for TMGH's own line items, across nineteen years of wording.

TMG has renamed most of these at least once — "Revenues from units sold" became
"Development revenue" became "Real estate development revenue"; "Customers
Advances" became "Advances from customers" became "Contract liabilities". A
label table keeps the renaming visible instead of hiding it inside a regex, and
each alias is the company's own wording in some document it published.
"""

IS = {
    "dev_revenue": [
        r"Real estate development revenues?\b",
        r"Development revenue\b",
        r"Revenues? from units sold\b",
        r"Revenues? from sold units\b",
        r"Revenue from sold units\b",
        r"Real Estate revenues?\b",
    ],
    "dev_cost": [
        r"Real estate development costs?\b",
        r"Development cost\b",
        r"Cost of units sold\b",
        r"Real Estate (?:&|and) Construction Cost\b",
    ],
    "gp_dev": [
        r"Gross profit from real estate development business\b",
        r"Gross profit from development\b",
    ],
    # FY2017 and FY2018 report hospitality and other recurring as ONE line;
    # FY2011-FY2016 and FY2019 onward split them. That is a basis break, and
    # the combined line is captured under its own name so it cannot be read as
    # either half — which is what happened when the "other recurring" pattern
    # matched inside "Hospitality and other recurring revenue".
    "recurring_combined_revenue": [r"Hospitality and other recurring revenue\b"],
    "recurring_combined_cost": [r"Cost of hospitality and other recurring revenue\b"],
    "gp_recurring_combined": [r"Gross profit from hospitality and other recurring revenue\b"],
    "hosp_revenue": [
        r"^\s*Hospitality revenues?\b",
        r"Revenues? from [Hh]otels(?:'? operation)?\b",
        r"Revenue from hotels'? operation\b",
    ],
    "hosp_cost": [
        r"^\s*Hospitality costs?\b",
        r"Hotels? [Cc]ost\b",
        r"Cost of hotels'? operation\b",
    ],
    "gp_hosp": [
        r"Gross profit from hospitality (?:business|operations)\b",
    ],
    "other_revenue": [
        r"Revenues? from activities with periodic yields? and service activities\b",
        r"^\s*Other recurring revenue",
        r"^\s*Other revenues?\b",
    ],
    "other_cost": [
        r"Costs? of activities with periodic yields? and service activities\b",
        r"^\s*Cost of other recurring revenue\b",
        r"Services? Cost\b",
    ],
    "gp_other": [
        r"Gross profit of activities with periodic yield and service activities\b",
        r"Gross profit from other recurring operations\b",
    ],
    # anchored: "Gross profit" alone on its line. Without the anchor it
    # matches the head of "Gross profit from development" and silently
    # publishes one segment's margin as the group's.
    "total_revenue": [r"^\s*Total revenues?\s*$", r"^\s*Total consolidated revenue\s*$",
                      r"^\s*Total Revenue\s*$"],
    "gross_profit": [r"^\s*Total gross profit\s*$", r"^\s*Gross [Pp]rofit\s*$"],
    "sga": [
        r"General and administrative expenses\b",
        r"^\s*Administrative expenses\b",
        r"Selling, [Gg]eneral and [Aa]dministrative [Ee]xpenses\b",
    ],
    "marketing": [r"^\s*Marketing expenses\b", r"Selling and marketing expenses\b"],
    # From FY2022 TMG stops printing a single finance-cost line and prints
    # "Finance expenses" and "Bank charges" separately; the note then sums them.
    # Both are captured so the total can be rebuilt by identity rather than a
    # year going missing.
    "finance_cost": [
        r"^\s*Financing expenses\b", r"^\s*Finance costs?\b",
        r"^\s*[Ii]nterest expense\b",
    ],
    "finance_expenses": [r"^\s*Finance expenses\b"],
    "bank_charges": [r"^\s*Bank charges\b"],
    "finance_income": [
        r"Financing revenues\b", r"Finance income\b", r"[Ii]nterest income\b",
    ],
    "investment_income": [r"Investment income\b"],
    "da": [r"Depreciation and amorti[sz]ation\b", r"Depreciation & amorti[sz]ation\b"],
    "pbt": [
        r"Net profit for the year before taxes\b",
        r"Net income before tax and minority interest expense\b",
        r"Net profit .{0,40}before tax(?:es)?\b",
        r"^\s*Profit for the year before tax\b",
        r"Profit before tax\b",
    ],
    "tax": [r"Income [Tt]ax\b", r"Current income tax\b"],
    "deferred_tax": [r"Deferred tax\b"],
    "net_profit": [
        r"^\s*Net [Pp]rofit for the year\s*$",
        r"Net income before minority interest\b",
        r"^\s*Net [Pp]rofit for the year(?! before)",
    ],
    "npat_parent": [r"Shareholders of the Parent Company\b",
                    r"^\s*Attributable net income\b"],
    "nci": [r"^\s*Non-controlling interests?\b", r"^\s*Minority interest expense\b"],
    "operating_income": [r"^\s*Operating Income\b",
                         r"Income before depreciation and financing expense\b"],
    "eps": [r"Earnings per [Ss]hare\b"],
}

BS = {
    "ppe": [r"^\s*Property,? [Pp]lant and [Ee]quipment\b", r"^\s*Fixed assets\b"],
    "investment_properties": [r"^\s*Investment [Pp]ropert(?:ies|y)\b"],
    "puc": [r"^\s*Projects [Uu]nder [Cc]onstructions?\b",
            r"^\s*\|?\s*Assets under construction\b"],
    "goodwill": [r"^\s*\|?\s*Goodwill\b"],
    "associates": [r"^\s*\|?\s*Investments? in [Aa]ssociates\b"],
    "htm": [r"^\s*Investments? in [Ff]inancial [Aa]ssets [Hh]eld to [Mm]aturity\b",
            r"^\s*Financial investments held to maturity\b"],
    "time_deposits_nc": [r"^\s*Time deposits and financial assets at amorti[sz]ed cost - non"],
    "total_nca": [r"^\s*Total [Nn]on-?\s?[Cc]urrent [Aa]ssets\b"],
    # TMG renamed this line twice: "Development properties" to 2023, then
    # "Properties under development". Same balance, same note.
    "development_properties": [r"^\s*Development [Pp]ropert(?:ies|y)\b",
                               r"^\s*Properties under development\b"],
    "inventories": [r"^\s*Inventories\b"],
    "notes_receivable": [r"^\s*Notes [Rr]eceivable\b(?! for)",
                         r"^\s*Trade and notes receivables?\b"],
    "nr_undelivered": [r"^\s*Notes receivable for undelivered units\b"],
    "other_current_assets": [r"^\s*Other current assets\b",
                             r"^\s*Prepayments? and [Oo]ther [Dd]ebit [Bb]alances\b",
                             r"^\s*Prepaid expenses and other debit balances\b"],
    "time_deposits_c": [r"^\s*Time deposits and financial assets at amorti[sz]ed cost - current"],
    "cash": [r"^\s*Cash (?:on [Hh]and )?and (?:at [Bb]anks|cash equivalents)\b"],
    "total_ca": [r"^\s*Total [Cc]urrent [Aa]ssets\b"],
    "total_assets": [r"^\s*Total [Aa]ssets\b"],
    "paid_capital": [r"^\s*Issued and [Pp]aid[- ]?up [Cc]apital\b", r"^\s*Paid-in capital\b"],
    "retained_earnings": [r"^\s*Retained earnings\b"],
    "equity_parent": [r"TOTAL PARENT COMPANY SHAREHOLDERS",
                      r"^\s*\|?\s*Equity attributable to shareholders of the Holding"],
    "nci_equity": [r"^\s*Non-controlling interests\b"],
    "total_equity": [r"^\s*TOTAL SHAREHOLDERS'? EQUITY\b",
                     r"^\s*Total (?:shareholders'? )?equity\b"],
    # INTEREST-BEARING debt, kept strictly apart from the balances that bear no
    # interest. Advance payments from customers, suppliers and contractors and
    # obligations against notes receivable are all funding, and none of them
    # pays a coupon; dividing the finance charge by a total that includes them
    # understates the borrowing rate by a multiple and manufactures a bias.
    "lt_loans": [r"^\s*Long[- ]term loans?(?: and facilities)?\b",
                 r"^\s*Loans non-current portion\b",
                 r"^\s*Bank loans\b", r"^\s*Loans - non-current portion\b",
                 r"^\s*Loans\b(?!\s*-)"],
    "sukuk": [r"^\s*Sukuk Al-Ijarah\b(?!\s*-)"],
    "sukuk_current": [r"^\s*Sukuk Al-Ijarah - current portion\b"],
    "notes_payable": [r"^\s*Notes payable\b"],
    "current_loans": [r"^\s*Current [Pp]ortion of (?:bank )?[Ll]oans(?: and [Ff]acilities)?\b",
                      r"^\s*Loans - current portion\b"],
    "bank_facilities": [r"^\s*Bank [Ff]acilities\b", r"^\s*Credit facilities\b"],
    "overdraft": [r"^\s*Banks? [Oo]verdraft\b"],
    "lease_liab_nc": [r"^\s*Lease liability non-current portion\b",
                      r"^\s*Non-current lease liabilities\b"],
    "lease_liab_c": [r"^\s*Lease liability - current portion\b",
                     r"^\s*Current lease liabilities\b"],
    "other_nc_liab": [r"^\s*Other non-current liabilities\b",
                      r"^\s*Non-current [Ll]iabilities\b"],
    "deferred_tax_liab": [r"^\s*Deferred tax liabilit(?:y|ies)\b"],
    "total_nc_liab": [r"^\s*Total [Nn]on-?\s?[Cc]urrent [Ll]iabilities\b"],
    # the developer's two contract positions
    # the apostrophe is straight in some filings and curly in others; matching
    # only one silently lost three years of the largest liability on the sheet
    "customer_advances": [r"^\s*Customers['\u2019]? [Aa]dvances?(?: payments?)?\b",
                          r"^\s*Advance payments \(collected\)",
                          r"^\s*Advances? (?:payments? )?from customers\b",
                          r"^\s*Advance payments from customers\b",
                          r"^\s*Contract liabilit(?:y|ies)\b",
                          r"^\s*Advance payments\s*$"],
    "obligations_nr_undelivered": [r"^\s*Obligations against notes receivable",
                                   r"^\s*Liabilities against cheques received from customers",
                                   r"^\s*Advance payments \(checks\)"],
    "creditors": [r"^\s*Creditors and [Nn]otes [Pp]ayable\b",
                  r"^\s*Suppliers, contractors,? and notes payable\b",
                  r"^\s*Accrued expenses and other credit balances\b",
                  r"^\s*Creditors and other credit balances\b"],
    "provisions_bs": [r"^\s*Provisions\b"],
    "tax_payable": [r"^\s*Income tax payable\b"],
    "total_cl": [r"^\s*Total [Cc]urrent [Ll]iabilities\b"],
    "total_liab": [r"^\s*Total [Ll]iabilities\b"],
}

KPI = {
    "new_sales_value": [r"[Nn]ew sales", r"[Nn]et sales", r"[Cc]ontracted [Ss]ales"],
    "units_sold": [r"units? sold", r"representing some ([\d,]+) units"],
    "units_delivered": [r"units? deliver", r"deliver\w* of ([\d,]+) .{0,40}units"],
    "backlog": [r"[Bb]acklog"],
    "collections": [r"[Rr]emaining collections?"],
}
