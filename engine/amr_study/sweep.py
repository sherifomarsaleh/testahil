"""AMR — the four-ring information sweep, run before any forecast driver was set.

Uses the shared register in engine/research_sweep.py rather than a study-local
re-implementation, so the coverage, provenance, consequence, gate-linkage, primary-access,
financial-statement-depth, study-year-quarter and investor-relations invariants are all
enforced by the same code every study is held to.
"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from research_sweep import (SweepRegister, AssetClass, Ring, FindingClass, SourceType,
                            DriverMode)

R = SweepRegister(ticker='AMR', asset_class=AssetClass.STOCK, sweep_date='2026-08-09')
R.declare_study_year('2026', ['Q1-2026', 'Q2-2026'])

SITE = 'https://www.americanarestaurants.com/investors/financial-information/'
R.record_primary_access(SITE, True, '2026-08-09',
                        'The company investor-relations library was reachable and served every '
                        'document used here directly: the audited consolidated financial '
                        'statements for 2022 through 2025, the reviewed interim statements for '
                        'the first quarter and first half of 2026, the 2025 annual report and '
                        'the full run of earnings presentations and releases. No aggregator was '
                        'used for any company figure.')
R.record_primary_access('https://www.adx.ae/en/main-market/company-profile/overview?symbols=AMR',
                        False, '2026-08-09',
                        'The Abu Dhabi Securities Exchange company page returned 403 to an '
                        'automated request from this environment. It was not needed: every '
                        'document the exchange would carry was obtained from the company '
                        'investor-relations library itself, which is the issuer\'s own '
                        'publication of the same filings.')

# ---------------------------------------------------------------- GLOBAL ring
F_RATES = R.add(Ring.GLOBAL, 'rate cycle & USD/FX regime', FindingClass.S,
                'The US ten-year Treasury yields 4.66% and the Federal Reserve has eased to a '
                '3.50–3.75% policy target; the dirham and riyal are pegged to the dollar, so '
                'this is the group\'s own rate cycle, not a foreign one',
                'US Treasury constant-maturity yield, close of 7 August 2026; Federal Reserve '
                'policy target', SourceType.PRIMARY_MARKET_DATA, '2026-08-07',
                model_impact='Sets the risk-free rate in the cost of capital at 4.66% less the '
                             'US sovereign default spread, and the terminal rate at 4.30%.')
F_FOOD = R.add(Ring.GLOBAL, 'commodity complex (input/output)', FindingClass.S,
               'Food and packaging input costs fell as a share of revenue through 2025 and into '
               '2026 — 29.2% of sales in the first half of 2025 against 27.4% a year later — '
               'which the company attributes to procurement and menu work rather than to prices',
               'H1 2026 earnings presentation, cost of inventory evolution',
               SourceType.COMPANY_IR, '2026-07-28', fiscal_period='Q2-2026',
               model_impact='Anchors the food and packaging cost line at 27.4% of revenue and '
                            'makes the structural-versus-cyclical reading of that fall the '
                            'study\'s central contested judgement, computed both ways.')
R.add(Ring.GLOBAL, 'global sector demand', FindingClass.C,
      'Listed quick-service comparators outside the region trade on a wide spread of enterprise '
      'value to EBITDA, with franchisors at the top of the range and operator-franchisees well '
      'below it — the structural split that governs where this company belongs',
      'Peer market data, retrieved 9 August 2026, used as a cross-check only',
      SourceType.AGGREGATOR, '2026-08-09')
R.add_negative(Ring.GLOBAL, 'trade / sanctions / supply chains',
               'searched the 2025 annual report, the FY2025 and H1 2026 filings and both '
               'earnings releases for supply-chain interruption, sanctions exposure and import '
               'restriction disclosures; the filings note higher input costs arising from the '
               'regional geopolitical situation but disclose no interruption to supply',
               '2026-08-09')

# --------------------------------------------------------------- COUNTRY ring
F_TAX = R.add(Ring.COUNTRY, 'regulatory environment (regulator, caps, tariffs, tax/subsidy)',
              FindingClass.S,
              'The OECD Pillar Two global minimum tax now bites: the group booked USD 14.0 '
              'million of domestic minimum top-up tax in FY2025, and the legislation was '
              'effective at the reporting date in the United Arab Emirates, Kuwait, Qatar, '
              'Bahrain and Oman',
              'Audited consolidated financial statements for the year ended 31 December 2025, '
              'note 28', SourceType.COMPANY_OFFICIAL, '2026-02-06',
              model_impact='Sets the effective tax rate path from 14.5% to 16.0%, converging on '
                           'the 15% minimum plus withholding and non-deductible drag. The rate '
                           'was 4% as recently as FY2023.')
F_MACRO = R.add(Ring.COUNTRY, 'sovereign macro (inflation, policy rate, FX/deval risk)',
                FindingClass.S,
                'The IMF projects about 2% inflation from 2028 in the pegged Gulf markets that '
                'produce most of the revenue, against 5–6% in Egypt and 5–9% in Kazakhstan, the '
                'two large non-pegged exposures',
                'IMF World Economic Outlook, retrieved through the IMF DataMapper API',
                SourceType.REGULATOR_OFFICIAL, '2026-08-09',
                model_impact='Sets the currency drag on US dollar revenue per restaurant — zero '
                             'in the pegged markets, 2.5% a year in Egypt and 1.5% in the '
                             'Kazakhstan-led segment — and anchors terminal growth at 3.0%.')
F_CRP = R.add(Ring.COUNTRY, 'fiscal / political events with sector read-through', FindingClass.S,
              'Sovereign risk across the twelve operating countries spans an equity risk premium '
              'of 4.87% in the United Arab Emirates and Qatar to 13.94% in Egypt and Iraq and '
              '30.89% in Lebanon',
              'Country default spreads and risk premiums, Aswath Damodaran, NYU Stern, read from '
              'the original data file', SourceType.REGULATOR_OFFICIAL, '2026-01-05',
              model_impact='The blended equity risk premium is revenue-weighted across all twelve '
                           'countries and comes out at 6.31% on the ratings basis and 5.95% on '
                           'the credit-default-swap basis; both are published.')

# -------------------------------------------------------------- INDUSTRY ring
F_STORES = R.add(Ring.INDUSTRY, 'demand drivers & capacity/supply balance', FindingClass.D,
                 'The restaurant estate is disclosed country by country and brand by brand at '
                 'each period end — 2,590 at the end of 2024, 2,749 at the end of 2025 and 2,746 '
                 'at 30 June 2026 — which is what makes a volume-times-price build possible '
                 'rather than a single growth rate',
                 'FY 2024, FY 2025 and H1 2026 earnings presentations, portfolio evolution '
                 'appendices', SourceType.COMPANY_IR, '2026-07-28', fiscal_period='Q2-2026',
                 model_impact='Converts revenue from a top-down growth rate into restaurants '
                              'times revenue per restaurant across seven market units, with the '
                              'restaurant count and the revenue per restaurant each grown on '
                              'their own driver.')
F_PRICE = R.add(Ring.INDUSTRY, 'pricing', FindingClass.S,
                'Like-for-like sales grew 9.7% in FY2025 and 6.3% in the first half of 2026, and '
                'management guides to mid-single-digit like-for-like growth for the full year',
                'FY 2025 earnings presentation; H1 2026 earnings release',
                SourceType.COMPANY_IR, '2026-07-28', fiscal_period='Q2-2026',
                model_impact='Sets the price side of the unit build: revenue per restaurant grows '
                             '5.5% in FY2026 and tapers to 3.5%, converging on long-run inflation '
                             'in the pegged markets.')
R.add(Ring.INDUSTRY, 'new entrants (named-competitor level)', FindingClass.C,
      'The company entered the premium retail category with the launch of carpo in Qatar and '
      'acquired the Malak Al Tawouk business in the United Arab Emirates and Saudi Arabia, '
      'moving into the Arabic category where local independents dominate',
      'H1 2026 earnings release and presentation', SourceType.COMPANY_IR, '2026-07-28',
      fiscal_period='Q2-2026')
R.add(Ring.INDUSTRY, 'technology substitution', FindingClass.C,
      'Home delivery is now 52% of revenue against 44% two years ago, and the company reports '
      'improving unit economics in the channel through its own ordering application rather than '
      'third-party platforms',
      'FY 2025 and H1 2026 earnings presentations, channel mix',
      SourceType.COMPANY_IR, '2026-07-28', fiscal_period='Q2-2026')
F_NEG_COMP = R.add_negative(Ring.INDUSTRY, 'competitor capacity / price moves (named)',
               'searched for disclosed capacity or price actions by named regional quick-service '
               'competitors — Alamar Foods, Herfy Food Services and the unlisted local operators '
               '— in company filings and the regional listed peers\' own published results; '
               'nothing is disclosed at a level that would change a driver here',
               '2026-08-09')

# --------------------------------------------------------------- COMPANY ring
F_FY25 = R.add(Ring.COMPANY, 'official financial statements', FindingClass.B,
               'Audited consolidated financial statements for the year ended 31 December 2025: '
               'revenue USD 2,508.8 million, EBITDA USD 595.6 million, profit attributable to '
               'shareholders USD 219.1 million, total assets USD 1,734.1 million',
               'Audited consolidated financial statements for the year ended 31 December 2025, '
               'audited by Deloitte & Touche (M.E.) LLP, signed 6 February 2026',
               SourceType.COMPANY_OFFICIAL, '2026-02-06', is_fs_data=True, fiscal_period='FY2025',
               url=SITE,
               model_impact='The entire historical income statement, balance sheet and cash flow '
                            'for FY2025, and the base the forecast is struck from.')
F_FY24 = R.add(Ring.COMPANY, 'official financial statements', FindingClass.B,
               'Audited consolidated financial statements for the year ended 31 December 2024: '
               'revenue USD 2,196.8 million, EBITDA USD 483.7 million, profit attributable to '
               'shareholders USD 158.8 million',
               'Audited consolidated financial statements for the year ended 31 December 2024, '
               'audited by Deloitte & Touche (M.E.) LLP',
               SourceType.COMPANY_OFFICIAL, '2025-02-11', is_fs_data=True, fiscal_period='FY2024',
               url=SITE,
               model_impact='The FY2024 historical column, and the comparative source for every '
                            'FY2023 balance-sheet line.')
F_FY23 = R.add(Ring.COMPANY, 'official financial statements', FindingClass.B,
               'Audited consolidated financial statements for the year ended 31 December 2023: '
               'revenue USD 2,413.1 million, EBITDA USD 546.0 million, profit attributable to '
               'shareholders USD 259.5 million — the peak year the two that followed fell short of',
               'Audited consolidated financial statements for the year ended 31 December 2023',
               SourceType.COMPANY_OFFICIAL, '2024-02-15', is_fs_data=True, fiscal_period='FY2023',
               url=SITE,
               model_impact='The FY2023 historical column; establishes that revenue FELL in '
                            'FY2024 and has only just regained the FY2023 level, which is why '
                            'the margin question is framed against a three-year average rather '
                            'than a single prior year.')
F_FY22 = R.add(Ring.COMPANY, 'official financial statements', FindingClass.B,
               'Audited consolidated financial statements for the year ended 31 December 2022, '
               'carried as the comparative column of the FY2023 filing: revenue USD 2,378.5 '
               'million, operating profit USD 292.6 million, profit attributable to shareholders '
               'USD 259.2 million, and revenue by country for the United Arab Emirates, Saudi '
               'Arabia, Kuwait and Egypt',
               'Audited consolidated financial statements for the year ended 31 December 2023, '
               'comparative column and note 34 — the company\'s own audited figures for FY2022',
               SourceType.COMPANY_OFFICIAL, '2024-02-15', is_fs_data=True, fiscal_period='FY2022',
               url=SITE,
               model_impact='Establishes the four-year revenue and margin arc the central '
                            'contested judgement is framed against, and shows that FY2023 was '
                            'itself only marginally above FY2022.')
F_NEG_NSO = R.add_negative(Ring.COMPANY, 'split of planned restaurant openings by market',
                           'searched the H1 2026 and FY 2025 earnings presentations, both '
                           'earnings releases and the 2025 annual report for a country-level '
                           'breakdown of the 120-130 net new restaurants guided for 2026; the '
                           'guidance is given at group level and by brand pipeline stage only, '
                           'never by country',
                           '2026-08-09')
F_Q1 = R.add(Ring.COMPANY, 'regular disclosures', FindingClass.B,
             'Reviewed condensed consolidated interim financial statements for the three months '
             'ended 31 March 2026: revenue USD 649.7 million',
             'Reviewed condensed consolidated interim financial statements, three months ended '
             '31 March 2026', SourceType.COMPANY_OFFICIAL, '2026-04-28', is_fs_data=True,
             fiscal_period='Q1-2026', url=SITE,
             model_impact='The first of the two disclosed quarters of the study year, swept in '
                          'before the build.')
F_H1 = R.add(Ring.COMPANY, 'regular disclosures', FindingClass.B,
             'Reviewed condensed consolidated interim financial statements for the six months '
             'ended 30 June 2026: revenue USD 1,364.5 million, up 12.1%; EBITDA USD 348.2 '
             'million at a 25.5% margin, up 290 basis points; profit attributable to '
             'shareholders USD 147.2 million, up 59.2%',
             'Reviewed condensed consolidated interim financial statements, six months ended '
             '30 June 2026, review report by Deloitte & Touche (M.E.) LLP dated 28 July 2026',
             SourceType.COMPANY_OFFICIAL, '2026-07-28', is_fs_data=True, fiscal_period='Q2-2026',
             url=SITE,
             model_impact='Resets the FY2026 base: the forecast year is half actual, and the '
                          'margin and the food-cost ratio are anchored on disclosed outturn '
                          'rather than on an assumption.')
F_GUIDE = R.add(Ring.COMPANY, 'strategic plans & guidance', FindingClass.S,
                'Management guides to 120–130 net new restaurants in 2026, mid-single-digit '
                'like-for-like growth, and net income margin expansion of 100 to 150 basis '
                'points against 2025',
                'H1 2026 earnings release and presentation', SourceType.COMPANY_IR, '2026-07-28',
                fiscal_period='Q2-2026',
                model_impact='Sets the volume driver directly — the net-new-restaurant path '
                             'starts at the 125 midpoint — and bounds the margin path.')
F_IR = R.add(Ring.COMPANY, 'IR communications (calls, presentations, releases)', FindingClass.D,
             'The company publishes average capital expenditure per restaurant by brand (USD 402 '
             'thousand across 356 gross openings, three-year average payback), four-wall EBITDA, '
             'net working capital, channel mix and the free-cash-flow bridge — none of which '
             'appears in any financial statement',
             'H1 2026 earnings presentation, key metrics by restaurant and the appendix',
             SourceType.COMPANY_IR, '2026-07-28', fiscal_period='Q2-2026',
             model_impact='Turns capital expenditure into a ground-up driver: gross openings '
                          'times the disclosed cost per restaurant, plus a maintenance charge '
                          'derived as the residual against actual FY2025 spend.')
F_MAT = R.add(Ring.COMPANY, 'one-off base-resetting transactions', FindingClass.B,
              'Two named acquisitions: the Pizza Hut business in Oman, bought on 23 January 2025 '
              'for USD 10.6 million net of cash acquired and adding 40 net restaurants, and Malak '
              'Al Tawouk, whose United Arab Emirates franchisee (7 restaurants) consolidated in '
              'the first half of 2026 with the Saudi acquisition completing on 9 July 2026',
              'Audited consolidated financial statements for the year ended 31 December 2025, '
              'note 36; H1 2026 earnings presentation',
              SourceType.COMPANY_OFFICIAL, '2026-02-06', fiscal_period='FY2025',
              model_impact='Explains why the FY2025 restaurant count rose by 159 against 119 '
                           'organic net additions, and why the FY2026 forecast is built on the '
                           'organic guidance rather than on the reported change.')
F_OWN = R.add(Ring.COMPANY, 'ownership / stake changes (named-transaction rule)', FindingClass.C,
              'Adeptio AD Investments holds 66.03% of the company. Adeptio AD Holdings, its '
              'parent, is owned equally by Mohamed Ali Rashed Alabbar and the Saudi Company for '
              'Gulf Food Investments, a subsidiary of the Public Investment Fund of Saudi Arabia. '
              'The named stake was searched for and read off the filing rather than estimated',
              'Audited consolidated financial statements for the year ended 31 December 2025, '
              'note 1; confirmed unchanged in the interim statements to 30 June 2026',
              SourceType.COMPANY_OFFICIAL, '2026-07-28', fiscal_period='FY2025')
F_CAP = R.add(Ring.COMPANY, 'management & capital actions', FindingClass.S,
              'The board declared USD 201.6 million against FY2025 — 91.99% of net profit — and '
              'has already declared a USD 100.8 million interim, USD 0.012 a share, against 2026. '
              'It holds 25 million treasury shares against a long-term incentive plan. The chief '
              'financial officer changed between the FY2025 and H1 2026 filings',
              'FY 2025 earnings presentation; H1 2026 earnings release; signature pages of the '
              'FY2025 and H1 2026 statements', SourceType.COMPANY_IR, '2026-07-28',
              fiscal_period='Q2-2026',
              model_impact='Sets the dividend yield inside the carry anchor of the price '
                           'distribution at 3.95%, and the forecast payout ratio at 85%.')

# ---------------------------------------------------------- per-driver gate
R.add_driver('Revenue — restaurant count by market unit', DriverMode.BOTTOM_UP,
             'The restaurant estate is published country by country at each period end, and '
             'segment revenue before eliminations is published for the same units, so revenue is '
             'built as restaurants times revenue per restaurant across seven units. The build '
             'reproduces reported revenue exactly in all three audited years.',
             [F_STORES, F_FY25, F_FY24, F_FY23])
R.add_driver('Revenue — revenue per restaurant', DriverMode.BOTTOM_UP,
             'The price side is anchored on disclosed like-for-like sales growth, with a currency '
             'drag applied only to the two non-pegged exposures.',
             [F_PRICE, F_MACRO, F_H1])
R.add_driver('Food and packaging cost', DriverMode.BOTTOM_UP,
             'Escalated on a traded food basket and anchored on the 27.4% of revenue actually '
             'recorded in the first half of 2026 — a disclosed, dated figure, not a macro proxy.',
             [F_FOOD, F_H1])
R.add_driver('Royalties', DriverMode.BOTTOM_UP,
             'A contractual percentage of branded sales, read off the expense note in each of '
             'the three audited years and held flat rather than escalated.',
             [F_FY25, F_FY24])
R.add_driver('Staff cost', DriverMode.BOTTOM_UP,
             'Wage escalation against a falling headcount per restaurant, both disclosed: '
             '37,207 full-time equivalents across 2,749 restaurants in FY2025 against 41,575 '
             'across 2,435 in FY2023.', [F_FY25, F_FY24])
R.add_driver('Delivery and transportation cost', DriverMode.BOTTOM_UP,
             'Driven by delivery-channel volume and fuel — its own driver class, not the wage '
             'index — with the channel share disclosed each half.', [F_FY25, F_IR])
R.add_driver('Capital expenditure', DriverMode.BOTTOM_UP,
             'Gross openings times the company\'s own published average cost per restaurant, '
             'plus a maintenance charge derived as the residual against actual FY2025 spend.',
             [F_IR, F_FY25])
R.add_driver('Effective tax rate', DriverMode.BOTTOM_UP,
             'Built from the disclosed Pillar Two position and the jurisdiction-by-jurisdiction '
             'rate table the company publishes, not from a single assumed rate.',
             [F_TAX, F_H1])
R.add_driver('Cost of debt', DriverMode.BOTTOM_UP,
             'The group\'s own incremental borrowing rate, read out of its lease accounting: '
             'lease finance cost over the average lease liability. It carries no bank debt.',
             [F_FY25, F_FY24])
R.add_driver('Competitor capacity and pricing', DriverMode.TOP_DOWN,
             'No named regional competitor discloses capacity or price actions at a level that '
             'would change a driver here, so the industry ring contributes context rather than a '
             'number. Closed by a dated negative search.',
             [F_NEG_COMP])
R.add_driver('Allocation of net new restaurants across markets', DriverMode.TOP_DOWN,
             'The total is the company\'s own guidance, but it does not publish the split by '
             'market. The allocation follows where the estate has actually grown over the last '
             'eighteen months. Flagged as an estimate at the allocation step only.',
             [F_NEG_NSO, F_GUIDE])

errors, warnings = R.validate()
print(R.qc_line())
for e in errors:
    print('  ERROR:', e)
for w in warnings:
    print('  warning:', w)
R.to_json(os.path.join(HERE, 'sweep_register.json'))
assert not errors, f'{len(errors)} sweep-register errors'
print('wrote sweep_register.json')
