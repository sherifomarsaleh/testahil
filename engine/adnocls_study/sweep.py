"""ADNOCLS — the study's information register, built on engine/research_sweep.py.

Four rings, outside in. Every finding carries a named source, a date, a class and what it
does to the model; every forecast driver names the findings it rests on and declares
whether it is built from the ground up or from the top down. The register's own invariants
are what fail the build, not a checklist in prose.

Written to sweep_register.json, which the bibliography document reads.
"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from research_sweep import (SweepRegister, AssetClass, Ring, FindingClass, SourceType,
                            DriverMode)

R = SweepRegister(ticker='ADNOCLS', asset_class=AssetClass.STOCK, sweep_date='2026-08-09')

CO = SourceType.COMPANY_OFFICIAL
IR = SourceType.COMPANY_IR
REG = SourceType.REGULATOR_OFFICIAL
MKT = SourceType.PRIMARY_MARKET_DATA
PRESS = SourceType.REPUTABLE_PRESS

# ---------------------------------------------------------------------------
# Primary access — the company's own site, logged whether it worked or not
# ---------------------------------------------------------------------------
R.record_primary_access('https://adnocls.ae/en/investors/results-reports', True,
                        '2026-08-09',
                        'Reachable. Audited statements for 2022-2025, every 2026 interim '
                        'released to date, management commentary, investor presentations '
                        'and earnings-call transcripts were all downloaded from the '
                        "company's own investor pages.")
R.record_primary_access('https://adnocls.ae/en/investors/annual-reports', True,
                        '2026-08-09',
                        'Reachable. Annual Report and Accounts for 2023, 2024 and 2025 '
                        'downloaded, which is where the audited statements appear as '
                        'machine-readable text where the standalone filing is an image.')
R.record_primary_access('https://adnocls.ae/en/investors/reports-and-presentations', False,
                        '2026-08-09',
                        'Returned a 503 from this environment. The same documents were '
                        'reached through the results-reports and annual-reports pages, so '
                        'nothing was lost; logged because a failed attempt is still a fact '
                        'about how the record was assembled.')
R.declare_study_year('FY2026', ['Q1 2026'])

# =============================== GLOBAL ====================================
F = {}
F['G1'] = R.add(
    Ring.GLOBAL, 'rate cycle & USD/FX regime', FindingClass.S,
    'The secured overnight financing rate stood at 3.65% in early August 2026, and the UAE '
    'central bank base rate has tracked it to the same level. The dirham is hard-pegged to '
    'the dollar at 3.6725, unchanged since 1997.',
    'Federal Reserve Bank of New York published rate; Central Bank of the UAE base-rate '
    'decision', REG, '2026-08-06',
    url='https://www.newyorkfed.org/markets/reference-rates/sofr',
    model_impact='Sets the floating-rate base for every one of the group\'s debt '
                 'instruments, all of which are priced off that rate, and is why a dollar '
                 'valuation needs no currency path at all.')
F['G2'] = R.add(
    Ring.GLOBAL, 'commodity complex (input/output)', FindingClass.D,
    'Crude and product tanker rates rose extraordinarily through the study year. The '
    'company\'s own fleet earned about USD 145,000 a day on its very large crude carriers '
    'in the first quarter of 2026, 268% above the same quarter of 2025, and the second '
    'quarter was crossing about USD 260,000 a day at the time of the results call. Product '
    'tanker classes moved with it: long-range-two about USD 58,000 rising toward USD '
    '95,000, long-range-one about USD 36,000 toward USD 55,000, and medium-range about USD '
    '30,000 toward USD 44,000.',
    'ADNOC L&S first-quarter 2026 earnings-call transcript', IR, '2026-05-14',
    model_impact='This is the single largest driver in the study. The shipping leg is built '
                 'vessel by vessel at these rates, and where they settle after 2026 is the '
                 'question the whole valuation turns on.',
    fiscal_period='Q1 2026')
F['G3'] = R.add(
    Ring.GLOBAL, 'global sector demand', FindingClass.S,
    'The parent group is expanding crude capacity toward five million barrels a day, adding '
    'refining capacity and growing petrochemical and liquefied-gas output, and has '
    'contracted the subject to move a large share of it.',
    'ADNOC L&S investor presentation, April 2026', IR, '2026-04-30',
    model_impact='Underwrites the contracted logistics revenue that the forecast grows on, '
                 'and is why the logistics leg is modelled on fleet deployment rather than '
                 'on a market growth rate.')
F['G4'] = R.add(
    Ring.GLOBAL, 'trade / sanctions / supply chains', FindingClass.D,
    'Heightened geopolitical disruption re-routed seaborne trade during the study year, '
    'lengthening voyages and tightening effective tanker supply. The company attributes its '
    'first-quarter shipping strength directly to it, and separately disclosed that one of '
    'its crude carriers was struck by drones off Oman on 4 May 2026 with no cargo aboard '
    'and no injuries.',
    'ADNOC L&S management commentary, first quarter 2026; interim financial information, '
    'events after the reporting period', CO, '2026-05-14',
    model_impact='Explains why the rate spike is happening and is the reason the study runs '
                 'a sustained-strength path alongside a reversion path rather than assuming '
                 'one of them. Also the source of the operational risk noted in the caveats.',
    fiscal_period='Q1 2026')

# =============================== COUNTRY ===================================
F['C1'] = R.add(
    Ring.COUNTRY, 'sovereign macro (inflation, policy rate, FX/deval risk)', FindingClass.D,
    'The UAE federal government\'s dirham treasury bond maturing January 2031 cleared its '
    'July 2026 auction at a 4.48% yield to maturity. The sovereign is rated Aa2 and carries '
    'an adjusted default spread of 0.42% and a total equity risk premium of 4.87%, against '
    'a mature-market premium of 4.23%.',
    'UAE Ministry of Finance treasury auction result as reported by the Emirates News '
    'Agency; Damodaran country risk file, January 2026 edition', REG, '2026-07-30',
    url='https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/ctryprem.html',
    model_impact='The observed government yield less the sovereign\'s own default spread is '
                 'the normalised risk-free rate in the cost of equity, so country risk is '
                 'charged once through the premium rather than twice.')
F['C2'] = R.add(
    Ring.COUNTRY, 'regulatory environment (regulator, caps, tariffs, tax/subsidy)',
    FindingClass.D,
    'UAE corporate tax applies at 9% above the threshold, but income from the international '
    'transport of goods and passengers is relieved. The company\'s own segment disclosure '
    'shows the effect precisely: its logistics units bore about 9% on their profit before '
    'tax in 2025 while its tanker unit bore 0.6%.',
    'UAE Federal Decree-Law 47 of 2022 on the taxation of corporations and businesses; '
    'ADNOC L&S 2025 financial statements, operating segments note', REG, '2023-06-01',
    model_impact='The forecast taxes each business unit at its own disclosed rate, so the '
                 'group effective rate is an OUTPUT of the earnings mix rather than an '
                 'assumption — and it falls as shipping grows.',
    is_fs_data=False)
F['C3'] = R.add(
    Ring.COUNTRY, 'fiscal / political events with sector read-through', FindingClass.S,
    'The company is majority-owned by the national oil company. A secondary placement in '
    'August 2025 raised the free float by three percentage points to 22% and preceded '
    'inclusion in a major emerging-market index.',
    'ADNOC L&S investor presentation, April 2026', IR, '2026-04-30',
    model_impact='Bears on the beta estimate — a 22% float traded largely by local and '
                 'index money is part of why the stock\'s measured co-movement is with its '
                 'home market rather than with global shipping equities.')

# =============================== INDUSTRY ==================================
F['I1'] = R.add(
    Ring.INDUSTRY, 'demand drivers & capacity/supply balance', FindingClass.D,
    'The company\'s owned shipping fleet at the end of 2025 was 87 vessels: 53 crude and '
    'product tankers, 20 gas carriers, 11 dry-bulk vessels and three container feeders. '
    'Twenty-two more are on order, and remaining committed capital expenditure on them is '
    'about USD 3.2 billion.',
    'ADNOC L&S investor presentation, April 2026; capital commitments note in the 2025 '
    'financial statements', IR, '2026-04-30',
    model_impact='The vessel counts are the volume side of the unit build; the order book '
                 'is what the capital-expenditure path is set from.',
    fiscal_period='FY2025')
F['I2'] = R.add(
    Ring.INDUSTRY, 'pricing', FindingClass.D,
    'Time-charter equivalents by vessel class are disclosed quarterly back to the start of '
    '2024, and the company also publishes the twelve charters it has fixed out, with each '
    'vessel\'s rate and expiry — from USD 19,750 a day on a long-range-one tanker to USD '
    '72,500 on a very large crude carrier.',
    'ADNOC L&S investor presentation, April 2026', IR, '2026-04-30',
    model_impact='Lets the fleet be split between the 45 vessels carrying rate risk and the '
                 'eight already fixed, and priced separately, instead of averaged.',
    fiscal_period='FY2025')
F['I3'] = R.add(
    Ring.INDUSTRY, 'competitor capacity / price moves (named)', FindingClass.C,
    'Comparable listed operators trade on a wide spread of enterprise multiples: Qatar Gas '
    'Transport, whose fleet is almost entirely on long-term charter, at about 12.3 times '
    'earnings before interest, tax, depreciation and amortisation; Frontline at about 9.0 '
    'times and International Seaways at about 8.1 times, both trading their fleets at spot.',
    'Company statistics pages at stockanalysis.com and valueinvesting.io', PRESS,
    '2026-08-09',
    model_impact='The relative lens weights the contracted multiple and the spot multiple by '
                 'the company\'s OWN disclosed split of earnings between contracted and '
                 'spot exposure, rather than picking a single peer.')
F['I4'] = R.add(
    Ring.INDUSTRY, 'technology substitution', FindingClass.C,
    'The order book is weighted to dual-fuel and gas-carrying tonnage — liquefied natural '
    'gas carriers, ethane carriers and ammonia carriers — which is the industry\'s response '
    'to emissions rules rather than a substitution threat to the existing fleet.',
    'ADNOC L&S Annual Report and Accounts 2025; investor presentation, April 2026', CO,
    '2026-04-30',
    model_impact='No substitution risk is priced into the terminal value; the fleet renewal '
                 'it implies is inside the capital-expenditure path.')
F['I5'] = R.add_negative(
    Ring.INDUSTRY, 'new entrants (named-competitor level)',
    'Searched for named new entrants into UAE offshore marine logistics and into the '
    'jack-up barge and offshore support vessel market serving the parent group. Nothing '
    'found: the work is let under long-term contracts by a single dominant customer, and '
    'the barriers are the contracts themselves rather than capital. Recorded as a negative '
    'result rather than left silent.', '2026-08-09')

# =============================== COMPANY ===================================
F['P1'] = R.add(
    Ring.COMPANY, 'official financial statements', FindingClass.S,
    'Audited consolidated financial statements for 2022, 2023, 2024 and 2025, each signed '
    'by the auditor, together with the Annual Report and Accounts for 2023, 2024 and 2025. '
    'Four complete audited financial years were obtained, against a floor of two and a '
    'target of four.',
    'ADNOC L&S consolidated financial statements, read from the filings themselves', CO,
    '2026-02-10', model_impact='Every historical figure in the study comes from these and '
                              'from nothing else.',
    is_fs_data=True, fiscal_period='FY2025')
F['P2'] = R.add(
    Ring.COMPANY, 'official financial statements', FindingClass.S,
    'The 2024 statements, and the 2023 comparatives they carry, give the third and second '
    'historical years of the income statement, balance sheet and cash flow.',
    'ADNOC L&S consolidated financial statements 2024 and Annual Report and Accounts 2024',
    CO, '2025-02-11', model_impact='Supplies the three-year historical statements.',
    is_fs_data=True, fiscal_period='FY2024')
F['P2b'] = R.add(
    Ring.COMPANY, 'official financial statements', FindingClass.S,
    'The 2023 statements and their 2022 comparatives extend the record back a fourth year '
    'and carry the segment schedule under the earlier reporting structure.',
    'ADNOC L&S consolidated financial statements 2023', CO, '2024-02-01',
    model_impact='Used for the longer-run margin and segment history and to identify the '
                 'two reorganisations that make the segment series non-comparable.',
    is_fs_data=True, fiscal_period='FY2023')
F['P3'] = R.add(
    Ring.COMPANY, 'regular disclosures', FindingClass.D,
    'Reviewed interim financial information for the three months to 31 March 2026 — the '
    'only quarter of the study year disclosed at the time of writing; the second-quarter '
    'results were scheduled for 11 August 2026. It gives revenue of USD 1,083 million, '
    'earnings of USD 368 million, net profit of USD 222 million, net debt of USD 420 '
    'million and a full segment schedule.',
    'ADNOC L&S condensed consolidated interim financial information, three months ended '
    '31 March 2026', CO, '2026-05-14',
    model_impact='Every forecast unit is anchored on its own first-quarter outcome '
                 'annualised, and the balance sheet at that date is the valuation date.',
    is_fs_data=True, fiscal_period='Q1 2026')
F['P4'] = R.add(
    Ring.COMPANY, 'strategic plans & guidance', FindingClass.D,
    'Guidance for 2026 was raised on 14 May 2026: group earnings growth moved from low-to-'
    'mid single digit to mid-to-high single digit and net profit from low-to-mid single '
    'digit to mid-to-high teens, with shipping earnings guidance moving from high-single-'
    'digit growth to mid-to-high 50% growth and logistics from flat to a mid-to-high 20% '
    'reduction. Management states the shipping assumptions sit well below prevailing spot '
    'rates and the logistics guidance at minimum activity levels. Medium-term growth is '
    'guided in the mid-to-high single digits a year to 2029.',
    'ADNOC L&S management commentary, first quarter 2026', CO, '2026-05-14',
    model_impact='Used as a reconciliation, not as the forecast. The build sits above the '
                 'guided figure and the gap is reported explicitly, with management\'s own '
                 'statement of conservatism as the explanation.',
    fiscal_period='Q1 2026')
F['P5'] = R.add(
    Ring.COMPANY, 'IR communications (calls, presentations, releases)', FindingClass.D,
    'Investor presentations and earnings-call transcripts for the 2025 full year and the '
    'first quarter of 2026. These are the only source for the rates each vessel class '
    'earned, the split of the fleet between spot and fixed employment, jack-up barge and '
    'support-vessel counts and utilisation, cargo tonnage, the order-book delivery '
    'schedule, the contracted-revenue run-off and the disclosed sensitivity of earnings to '
    'a change of USD 1,000 a day in the rate.',
    'ADNOC L&S investor presentations and earnings-call transcripts', IR, '2026-05-14',
    model_impact='Supplies every unit driver in the shipping and logistics builds. Without '
                 'it the forecast could only be a growth rate applied to a segment.',
    fiscal_period='Q1 2026')
F['P6'] = R.add(
    Ring.COMPANY, 'one-off base-resetting transactions', FindingClass.B,
    'An 80% interest in a tanker owner and commercial manager was acquired on 7 January '
    '2025 for USD 999.3 million in cash, bringing 32 vessels and a pooling and bunkering '
    'platform. It contributed USD 1,245 million of revenue and USD 65 million of net profit '
    'in 2025 and produced a bargain purchase gain of USD 12.1 million. The remaining 20% is '
    'contracted for mid-2027 at between USD 335 million and USD 450 million, carried at '
    'present value as a liability against a negative reserve in equity.',
    'ADNOC L&S 2025 financial statements, business combinations note', CO, '2026-02-10',
    model_impact='This is why 2025 is not comparable with 2024 on the shipping line and why '
                 'the deferred consideration is treated as debt-like in the equity bridge. '
                 'Modelled explicitly, never smoothed into a growth rate.',
    is_fs_data=True, fiscal_period='FY2025')
F['P7'] = R.add(
    Ring.COMPANY, 'management & capital actions', FindingClass.D,
    'USD 2.0 billion of perpetual capital securities were issued during 2025 through a '
    'subsidiary, priced at the overnight financing rate plus 125 basis points, perpetual, '
    'with coupons payable solely at the group\'s discretion and therefore classified as '
    'equity. Coupons and fees go straight to retained earnings and never touch the income '
    'statement. Separately, a USD 2.0 billion revolving facility with the parent, priced at '
    'that rate plus 80 basis points, replaced the earlier facilities in January 2026.',
    'ADNOC L&S 2025 financial statements and first-quarter 2026 interim information',
    CO, '2026-05-14',
    model_impact='The securities rank ahead of the ordinary shares whichever way they are '
                 'classified, so they are deducted in the equity bridge, and earnings '
                 'available to ordinary holders are struck after their coupon. The facility '
                 'rates are the primary evidence in the cost-of-debt table.',
    is_fs_data=True, fiscal_period='Q1 2026')
F['P8'] = R.add(
    Ring.COMPANY, 'ownership / stake changes (named-transaction rule)', FindingClass.S,
    'The parent placed USD 317 million of stock in August 2025, lifting the free float to '
    '22%. The 20% minority in the acquired tanker business is the other named stake '
    'movement, contracted for mid-2027.',
    'ADNOC L&S investor presentation, April 2026; 2025 financial statements, '
    'non-controlling interests note', IR, '2026-04-30',
    model_impact='Fixes the share count and the non-controlling interest deducted in the '
                 'bridge; the future 20% purchase is the deferred consideration already '
                 'carried as debt-like.')
F['P9'] = R.add(
    Ring.COMPANY, 'regular disclosures', FindingClass.D,
    'Long-term contracted revenue of about USD 25 billion, of which USD 2.5 billion falls '
    'in 2026, USD 6.4 billion across 2027-2029 and USD 16.4 billion from 2030. About 53% of '
    '2026 revenue is already contracted. The company also discloses the share of group '
    'earnings exposed to spot shipping rates: 31% in 2026, falling to 23% by 2029.',
    'ADNOC L&S investor presentation, April 2026', IR, '2026-04-30',
    model_impact='The spot share is used directly as the weight between the contracted and '
                 'spot peer multiples in the relative lens, so that weighting is the '
                 'company\'s own disclosure rather than a judgement.')

F['P2c'] = R.add(
    Ring.COMPANY, 'official financial statements', FindingClass.S,
    'The 2022 audited statements complete a four-year record and carry the segment schedule '
    'from before the group was reorganised, which is what makes the two later '
    'reclassifications visible rather than invisible.',
    'ADNOC L&S consolidated financial statements 2022, signed', CO, '2023-02-01',
    model_impact='Extends the margin and segment history to four years and evidences that '
                 'the segment series is not comparable across the whole span.',
    is_fs_data=True, fiscal_period='FY2022')
F['N1'] = R.add_negative(
    Ring.INDUSTRY, 'pricing',
    'Searched for a published forward curve or third-party forecast of crude and product '
    'tanker rates beyond 2026 that could be cited. None is obtainable here. The company '
    'says it sets its own guidance from a third-party forecasting house and deliberately '
    'below prevailing spot, but does not publish the path. Where rates settle after 2026 is '
    'therefore an unevidenced judgement and is treated as one — computed both ways and '
    'published side by side rather than resolved.', '2026-08-09')
F['N2'] = R.add_negative(
    Ring.COMPANY, 'strategic plans & guidance',
    'Searched the annual report, every investor presentation and both earnings-call '
    'transcripts for an engineering and construction award pipeline or tender book beyond '
    'the 2026 revenue range and the one project still completing. Nothing is disclosed. The '
    'recovery in that line after 2026 is a judgement with no source behind it and is named '
    'as such in the study.', '2026-08-09')

# ---------------------------------------------------------------------------
# Driver gate — what each forecast driver rests on
# ---------------------------------------------------------------------------
R.add_driver('Tanker earnings', DriverMode.BOTTOM_UP,
             'Built vessel by vessel: 45 spot-exposed vessels at the time-charter '
             'equivalent disclosed for each class, eight chartered-out vessels at their own '
             'fixed rates until each expires, less a running cost per vessel per day. The '
             'running cost is solved so that the same construction reproduces reported 2025 '
             'segment earnings exactly, which is what makes it a calibration rather than an '
             'assumption.', [F['I1'], F['I2'], F['G2']])
R.add_driver('Where tanker rates settle after 2026', DriverMode.TOP_DOWN,
             'No source can give this. It is the study\'s central contested judgement and '
             'is therefore computed both ways and published side by side — reverting to the '
             'average of the 2024 and 2025 outcomes, or settling 30% above that — never '
             'averaged into a single number.', [F['G2'], F['G4'], F['I2'], F['N1']])
R.add_driver('Gas carrier earnings', DriverMode.BOTTOM_UP,
             'Consolidated vessel-years read off the published contract table quarter by '
             'quarter to 2029, at an average revenue per vessel per day implied by reported '
             '2025 revenue over 2025 vessel-years. Per-vessel rates are not disclosed, so '
             'the implied group average is the finest level the disclosure supports and the '
             'gap is flagged.', [F['I1'], F['P5']])
R.add_driver('Offshore contracting and offshore services', DriverMode.BOTTOM_UP,
             'Each unit anchored on its own first-quarter 2026 revenue annualised, then '
             'grown on the fleet deployment the company has disclosed. Margins are set from '
             'the first quarter\'s own outcome before the one-off receivable provision.',
             [F['P3'], F['P5']])
R.add_driver('Engineering and construction revenue', DriverMode.TOP_DOWN,
             'The company\'s own stated range of USD 100-150 million for 2026 after the '
             'large island project completed. Beyond that no award pipeline is disclosed, '
             'so the recovery is a judgement and is named as the least visible line in the '
             'model.', [F['P4'], F['P5'], F['N2']])
R.add_driver('Capital expenditure', DriverMode.BOTTOM_UP,
             'The company\'s own published path for 2026 to 2028, which totals about USD 7 '
             'billion across the programme and matches the disclosed order book and '
             'remaining committed spend. Beyond 2028 it falls toward the stated USD 100-150 '
             'million a year of maintenance spending plus continuing fleet renewal.',
             [F['I1'], F['P4']])
R.add_driver('Tax rate', DriverMode.BOTTOM_UP,
             'Each business unit is taxed at the rate its own segment disclosure shows it '
             'bore in 2025 — about 9% in logistics, well under 1% in shipping under the '
             'international transport relief. The group rate is the output of the mix.',
             [F['C2'], F['P1']])
R.add_driver('Working capital', DriverMode.BOTTOM_UP,
             'Days sales outstanding, days inventory and days payable computed from the '
             '2025 statements and held, so the balance sheet and the cash flow are '
             'projected from the conversion cycle rather than plugged.', [F['P1']])
R.add_driver('Cost of equity', DriverMode.BOTTOM_UP,
             'The normalised risk-free rate is the observed dirham government bond yield '
             'less the sovereign\'s own default spread, so country risk is charged once '
             'through the equity premium. Beta is the stock\'s own weekly regression '
             'against an index of its home market over its full listed history. Because '
             'that history is short and the float small, the study also publishes the whole '
             'valuation at an asset-risk beta of 1.0.', [F['C1'], F['C3']])
R.add_driver('Cost of debt', DriverMode.BOTTOM_UP,
             'Three constructions averaged in the workbook rather than asserted: the '
             'marginal drawdown rate on the parent facility, the weighted blend of the '
             'instruments actually outstanding, and the midpoint of the disclosed '
             'third-party bank-loan range. The result sits above the local sovereign yield, '
             'as it must.', [F['P7'], F['C1']])
R.add_driver('Terminal growth', DriverMode.BOTTOM_UP,
             'Taken from the company\'s own goodwill value-in-use test, which projects cash '
             'flows beyond its plan at a rate equal to an estimated 2% inflation, and '
             'sensitised from 1.0% to 2.5%.', [F['P1']])
R.add_driver('Relative multiple weighting', DriverMode.BOTTOM_UP,
             'The weight between a contracted-fleet multiple and a spot-fleet multiple is '
             'the company\'s own disclosed share of earnings exposed to spot rates, not a '
             'judgement about which peer looks closest.', [F['P9'], F['I3']])

errors, warnings = R.validate()
for e in errors:
    print('  ERROR', e)
for w in warnings:
    print('  note ', w)
assert not errors, errors
R.to_json(os.path.join(HERE, 'sweep_register.json'))
c = R.counts()
print(f"register valid — {sum(c.values())} findings {c}, {len(R.drivers)} drivers")
print(R.qc_line())
