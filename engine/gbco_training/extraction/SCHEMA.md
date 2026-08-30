# Extraction schema — GB Auto / GB Corp annual report text files
Source txts are `pdftotext -layout` output of the company's own annual reports (audited consolidated FS embedded near "Consolidated Balance Sheet" / "Consolidated Statement of Financial Position" / "Consolidated Income Statement"). Money figures in the FS are mostly "EGP 000s" — record units EXACTLY as the document states them. MD&A sections quote EGP mn/bn. Statement pages show TWO numeric columns: FIRST = report's own fiscal year, SECOND = prior-year comparative. Some lines wrap; read carefully.

For EACH assigned fiscal year write ONE JSON file FY<YEAR>.json into the output dir, shaped:
{
 "fy": 2011, "source_doc": "<pdf filename>", "source_url": "https://ir.gb-corporation.com/media/annual_reports/files/<name>.pdf",
 "units_note": "consolidated FS in EGP 000s unless stated",
 "is": {"revenue": {"v": 123, "q": "<verbatim line from txt>"}, ...},
 "bs": {...}, "cf": {...},
 "segments": [{"name": "...", "revenue": {...}, "gross_profit": {...}, "volume_units": {...}}],
 "kpis": {...}, "guidance": [{"q": "<verbatim outlook/expectation quote>", "where": "section"}],
 "accounting_changes": ["<verbatim notes on newly applied standards / policy changes>"],
 "restatement_notes": ["<any 'restated'/'reclassified' comparative notes>"],
 "oddities": ["<anything ambiguous>"]
}
Every numeric value MUST carry "q": the verbatim text line it came from (trim whitespace runs to single spaces). If a line is absent in the document use null and add a note in oddities. NEVER compute, infer, or fill a missing figure. Do not convert units.

IS keys (consolidated, the year's own column): revenue, cogs, gross_profit, distribution_exp, admin_exp, other_income, other_expense, op_profit, finance_income, finance_cost, associates_income, pbt, income_tax, np_total, np_parent, np_nci. (If the document nets lines — e.g. one "selling, general and administrative" — put the net under the nearest key and say so in oddities.)
BS keys: ppe_net, investments_associates, inventory, trade_notes_receivable, debtors_other, cash, total_current_assets, total_assets, borrowings_current, borrowings_noncurrent, trade_notes_payable, total_liabilities, equity_parent, nci_equity, total_equity, provisions.
CF keys: cfo, capex_ppe, dep_amort_addback, interest_paid, cfi, cff.
segments: the consolidated segment-reporting note AND/OR the MD&A per-line-of-business figures (revenue, gross profit, unit volumes: passenger cars, motorcycles & three-wheelers, commercial vehicles & construction equipment, tires, after-sales, financing businesses, regional/Iraq). Volumes are units (count), record as printed.
kpis: market size / market share (AMIC quotes), GB Capital portfolio size, anything volume-price relevant, as {"name": {"v":..., "q":"..."}}.
guidance: management's forward expectations for the NEXT year(s), verbatim (Chairman/CEO letter, Outlook).
