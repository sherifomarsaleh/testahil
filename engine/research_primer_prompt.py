#!/usr/bin/env python3
"""GENERATE THE RESEARCH-PRIMER PROMPT FOR ONE NAME, FROM WHAT THE REPOSITORY KNOWS.

    python3 engine/research_primer_prompt.py TICKER [--out FILE]

WHY THIS IS A GENERATOR AND NOT A TEMPLATE. The principal runs a deep-research pass on
each company before its study is built or re-issued, and the prompt for that pass has to
be specific to the company AND to the industry it operates in. Written by hand it goes
stale the moment a study records a new open question, and it omits exactly the gaps the
study itself has already declared it cannot close. Built here it carries three things
nothing typed by hand carries reliably:

  the company's own registered name in ENGLISH AND ARABIC, so the researcher can search in
  the language the source is written in. This is not a courtesy. A ministerial decision
  repealing Egypt's nitrogen-fertiliser export duty was searched three times in English,
  found nothing, and was reported back as not verifying; the decree register, the customs
  circular and the whole trade press are Arabic, the decision was real, and the study had
  been carrying five forecast years of a repealed levy on its largest line.

  the driver headings the INDUSTRY actually turns on, rather than a generic list. What
  moves a cement company is a production quota, a fuel mix and a tariff; what moves a bank
  is a policy rate and a reserve rule; asking one set about the other returns nothing and
  reads like it returned nothing because there was nothing.

  THIS STUDY'S OWN DECLARED OPEN QUESTIONS, read live out of its sweep register's negative
  searches. Those are the things the study went looking for, could not find, and recorded.
  They are the highest-value questions on the page and no template can know them.

WHAT COMES BACK IS A LEAD AND NEVER AN INPUT. Nothing from a research pass enters a model
until it is traced to the primary source it cites and read there. Historicals come from
the company's own issued financial statements and from nowhere else.

THIS MODULE IS THE GENERATOR [R-PRIME-01] CLAUSE TWO NAMES, and clause four — search in
the language the source is written in — is built into what it emits rather than left to
the researcher's memory: every generated prompt carries the company's registered name in
the local language beside the English one, and asks which languages were searched.
"""
import json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA_JS = os.path.join(ROOT, 'assets', 'data.js')
NODE_READ = ("const p=process.argv[1];const s=require('fs').readFileSync(p,'utf8');"
             "const m={};(0,eval)(s.replace(/^\\s*(const|let|var)\\s+/gm,'m.$1='"
             ".replace('$1','')));")

# ---------------------------------------------------------------- SECTOR MAP --
# One entry per covered name. A name that is NOT here is reported as unclassified and
# gets the general block plus a line saying so — an absent classification is not a clean
# one [R-ENF-04], and silently handing back a generic prompt would hide that.
SECTOR = {
    'ABUK': 'fertiliser', 'EGCH': 'fertiliser', 'FERTIGLB': 'fertiliser',
    'ARCC': 'cement', 'SCEM': 'cement',
    'ADIB': 'bank', 'ADIBUAE': 'bank', 'ADCB': 'bank', 'ALINMA': 'bank',
    'ALRAJHI': 'bank', 'COMI': 'bank', 'DIB': 'bank', 'ENBD': 'bank', 'FAB': 'bank',
    'QNB': 'bank', 'RIBL': 'bank', 'SNB': 'bank',
    'PHAR': 'pharma', 'RMDA': 'pharma',
    'ISPH': 'pharma_distribution',
    'CLHO': 'healthcare', 'BURJEEL': 'healthcare',
    'TMGH': 'realestate', 'PHDC': 'realestate', 'ALDAR': 'realestate',
    'EMAAR': 'realestate', 'EMAARDEV': 'realestate', 'EMFD': 'realestate',
    'HELI': 'realestate', 'OCDI': 'realestate', 'ORHD': 'realestate',
    'PRDC': 'realestate', 'MODON': 'realestate',
    'DU': 'telecom', 'EAND': 'telecom', 'ETEL': 'telecom', 'STC': 'telecom',
    'AMOC': 'refining',
    'ADNOCDRILL': 'oilfield_services', 'ADNOCLS': 'oilfield_services',
    'ADNOCDIST': 'fuel_retail', 'ADNOCGAS': 'gas', 'ARAMCO': 'oil_gas',
    'BOROUGE': 'petrochemicals', 'SABIC': 'petrochemicals', 'IQCD': 'petrochemicals',
    'GBCO': 'automotive', 'TMPV': 'automotive', 'TSLA': 'automotive',
    'DEWA': 'utility', 'EMPOWER': 'utility', 'ACWA': 'power_developer',
    'SWDY': 'cables', 'ELEC': 'cables', 'RIYADHCABLE': 'cables',
    'JUFO': 'food', 'EFID': 'food', 'AGTHIA': 'food', 'SAVOLA': 'food',
    'AMR': 'restaurants',
    'LULU': 'retail', 'EXTRA': 'retail',
    'ORWE': 'textiles', 'KABO': 'textiles', 'DSCW': 'textiles',
    'FWRY': 'fintech', 'EFIH': 'fintech', 'ELM': 'fintech',
    'HRHO': 'financials', 'BTFH': 'financials', 'CCAP': 'holding',
    'OIH': 'holding', 'RAYA': 'holding', 'IHC': 'holding',
    'ALPHADHABI': 'holding', '2POINTZERO': 'holding',
    'ORAS': 'construction',
    'MAADEN': 'mining', 'EGAL': 'mining',
    'AAPL': 'technology', 'NVDA': 'technology', 'INFY': 'it_services',
    'KAKAO': 'technology', 'SAMSUNG': 'technology', 'LGES': 'batteries',
    'QGTS': 'shipping', 'AIRARABIA': 'airline',
    'SALIK': 'concession', 'RELIANCE': 'conglomerate', 'LCSW': 'ceramics',
}

# ------------------------------------------------------- INDUSTRY DRIVER SETS --
# What each industry actually turns on. These are the headings the research pass is asked
# to fill; they are the questions a valuation of that industry cannot be built without.
BLOCKS = {
 'fertiliser': [
   "Announced or commissioning capacity — what is being built, what it produces, nameplate in tonnes per day and per year, sanctioned cost, financing, guided commissioning date, and any slippage against a previously guided date. Be precise about which product each unit makes.",
   "The natural-gas price the company pays as feedstock and as fuel — the announced USD per mmBtu for fertiliser producers, every change in the last 24 months, and any announced future change.",
   "Any subsidised or administered allocation — the tonnage owed to a ministry, the fixed price per tonne, and any revision.",
   "Export duties, levies, licences or quotas on the products, with the decree number and effective date of every imposition AND every repeal.",
   "Domestic free-market and export price references for the main products.",
   "Any announced gas-supply interruption or curtailment to the sector.",
 ],
 'cement': [
   "The competition authority's production-quota arrangement — current status, the percentage cut in force, the expiry date, any announced renewal or termination.",
   "Clinker and cement capacity, and any announced expansion, mothballing or restart, line by line.",
   "Alternative-fuel substitution — the percentage reached, the stated target, and any new waste-fuel supply agreement.",
   "The price and availability of coal, petcoke and mazut delivered to plants in this market.",
   "Domestic price references and export volumes.",
   "New entrants, and capacity coming on or leaving this market.",
 ],
 'bank': [
   # The policy rate, the currency and the general tax rate are MACRO and are asked for in
   # section A. This block asks only what is specific to banking, or the two sections
   # return the same answer twice and the researcher pads to fill both.
   "Prudential rules: announced changes to reserve requirements, the loan-to-deposit ratio, "
   "capital or liquidity requirements, provisioning rules, or the regulatory treatment of "
   "sovereign holdings — with the circular and its effective date.",
   "Any tax applied to BANKS specifically, where it differs from the general corporate rate, "
   "and any announced change to it.",
   "Directed-lending initiatives — programmes steering credit to named sectors, the "
   "subsidised rates attached, who bears the subsidy, and the size of each programme.",
   "Sector credit and deposit growth, and any published banking-sector aggregate, with the "
   "date and the body that published it.",
   "Competition: licences granted or withdrawn, banks entering or leaving this market, "
   "announced mergers or acquisitions among its named competitors, and digital-bank or "
   "fintech licensing that competes for the same deposits.",
   "Where the bank is Islamic or has an Islamic window: any change to the sharia-governance "
   "framework, sukuk market rules, or the regulatory treatment of Islamic instruments.",
   "Deposit-insurance, resolution or consumer-protection rules newly imposed on banks.",
 ],
 'pharma': [
   "Drug-regulator pricing decisions — every announced repricing round, which product classes, what percentage, the effective date, and whether it is adopted or still under study.",
   "Any new manufacturing facility — capacity, products, registration status, guided first-revenue date, and slippage. Distinguish a group capacity figure from a single plant's.",
   "New product registrations and approvals granted to the company, and to its named competitors in the same molecules.",
   "Export markets entered or lost, and any tender awards, with quantities and prices where stated.",
   "Announced changes to the import regime or to foreign-currency allocation for pharmaceutical raw materials.",
   "Capacity expansion at any plant, in packs, lines or units.",
   "Government or unified-procurement tender pricing that applies to the company's products, and the payment terms attached.",
 ],
 'pharma_distribution': [
   "Distribution margin regulation — the mandated pharmacy and distributor margins, and every announced change with its decree and date.",
   "Warehouse and logistics capacity added or announced, in square metres, lines or delivery points.",
   "Principal agreements won, lost or renewed, with the manufacturers named.",
   "Working-capital and payment-terms regulation, and any state arrears to the sector.",
   "Drug-regulator pricing rounds, since a distributor's revenue moves with the shelf price.",
   "Any announced expansion into new markets, formats or adjacent categories.",
 ],
 'healthcare': [
   "Bed capacity and occupancy — beds added, hospitals opened or acquired, with dates.",
   "Reimbursement and insurance regime changes, including any universal health-insurance rollout and its tariff schedule.",
   "Announced tariff or pricing regulation for private healthcare in this market.",
   "Medical-staff cost and availability, and any announced wage regulation.",
   "Announced acquisitions, greenfield projects and their capital cost and timing.",
   "Any regulator action, licence suspension or accreditation change.",
 ],
 'realestate': [
   "Land acquired or awarded in the last 18 months — location, area, the payment terms agreed with the land authority, and the instalment schedule.",
   "New project launches, with saleable area and guided delivery dates.",
   "The company's own published sales, backlog, collections and delivery guidance, with dates.",
   "The recurring-income portfolio — hotels, malls, offices — and any announced addition, refurbishment or disposal.",
   "Regional expansion — what has been signed, what is committed, and what is still a memorandum.",
   "Announced changes to instalment periods, mortgage-finance initiatives, or the registration and transfer-tax regime for property in this market.",
   "Any announced capital-structure change, securitisation, or subsidiary listing.",
 ],
 'telecom': [
   "Spectrum awards and licence renewals — bands, price paid, term, and the obligations attached.",
   "Regulated tariffs, interconnection rates and any announced change.",
   "Subscriber and ARPU disclosures the company itself published, with dates.",
   "Network capital programmes — fibre, 5G, data centres — with the announced spend and the years it covers.",
   "Any announced tower sale, infrastructure carve-out, or fintech subsidiary and its valuation.",
   "Competition entering or leaving, and any announced consolidation.",
 ],
 'refining': [
   "The feedstock allocation from the state oil company — the volume, the pricing formula, and any announced change.",
   "Plant capacity and utilisation, and any announced expansion, revamp or shutdown, with dates.",
   "The product slate and any announced change in the mix.",
   "Domestic pricing regulation for the products, and any announced revision.",
   "Export volumes, destinations, and any levy or restriction.",
   "International reference prices for the main products, and their recent direction.",
 ],
 'oilfield_services': [
   "Fleet or asset additions — rigs, vessels, units — with counts, delivery dates and the contracts attached.",
   "Contract awards and backlog, with counterparty, term and value where disclosed.",
   "Day rates and utilisation the company or its regulator has disclosed.",
   "The parent's capital programme, since it sets this company's demand.",
   "Any announced acquisition, joint venture or long-term charter.",
 ],
 'fuel_retail': [
   "Station count and network expansion, with targets and dates.",
   "Regulated fuel margins and any announced change to the pricing formula.",
   "Non-fuel retail expansion and its announced contribution.",
   "Any announced acquisition or entry into a new market.",
 ],
 'gas': [
   "Contracted volumes and their pricing formulae, with terms and counterparties.",
   "Processing and liquefaction capacity, and any announced expansion.",
   "Announced domestic gas price regulation and any change.",
   "Long-term supply agreements signed, with volume, term and start date.",
 ],
 'oil_gas': [
   "Production capacity and any announced change to the sustainable capacity target.",
   "Capital programme by segment, with announced spend and years.",
   "Announced pricing formulae, official selling prices, and any government take or royalty change.",
   "Downstream and chemicals projects, with capacity, cost and commissioning dates.",
 ],
 'petrochemicals': [
   "Capacity by product, and any announced expansion, debottlenecking or shutdown with dates.",
   "Feedstock pricing and allocation, and any announced change.",
   "Product price references — polyethylene, polypropylene, methanol, urea, whichever apply — and their direction.",
   "Announced joint ventures, offtake agreements and their volumes.",
   "Any announced antidumping duty or trade restriction affecting the products.",
 ],
 'automotive': [
   "The customs-tariff schedule for vehicles and components, and every announced change including any phase-in by origin.",
   "The national automotive industrial strategy — the incentive programme, its status, and what a local assembler must do to qualify.",
   "Brand agency agreements won, lost or renewed, and the models added.",
   "Assembly capacity in units, and any announced expansion.",
   "Any associated financing business — leasing, consumer finance — and regulatory changes affecting it.",
   "Announced restrictions on vehicle imports, on foreign-currency allocation for imports, or on registration.",
 ],
 'utility': [
   "The regulated tariff and every announced change, with the decree and effective date.",
   "The regulatory asset base, the allowed return, and any announced review.",
   "Capacity added or announced — megawatts, capacity tonnes, connections — with cost and dates.",
   "Any announced concession term, renewal or renegotiation.",
   "Announced fuel-cost pass-through arrangements.",
 ],
 'power_developer': [
   "Projects reaching financial close, with capacity, cost, tariff and offtaker.",
   "The announced project pipeline and its stated capacity by stage.",
   "Power-purchase agreement tariffs where disclosed, and their term.",
   "Any announced change in the equity stake held in a project.",
 ],
 'cables': [
   "The order backlog — the figure the company itself last published, its date, and its split by segment.",
   "New contract awards in the last 18 months, with counterparty, country and value.",
   "Manufacturing capacity added or announced — which plant, which country, which product, what capacity.",
   "The share of revenue earned outside the home market and any announced shift in that mix.",
   "Transmission, substation and grid capital programmes in the countries it sells into.",
   "Any announced change to export incentives, or to how it buys copper and aluminium.",
   "Announced disposals, listings or restructurings of subsidiaries.",
 ],
 'food': [
   "Capacity added or announced, by plant and product line, in tonnes or units.",
   "Input cost regulation and availability — wheat, sugar, oils, milk, whichever apply — and any announced subsidy or allocation change.",
   "Price regulation or any announced government intervention on the products.",
   "New product launches and category entries the company itself announced.",
   "Export markets entered or lost, and any duty or restriction.",
   "Announced distribution expansion, in outlets or routes.",
 ],
 'restaurants': [
   "Store count by brand and market, with openings and closures announced.",
   "Franchise and master-franchise agreements signed, renewed or lost, with the term.",
   "Announced expansion targets in store numbers and the capital attached.",
   "Input cost and any announced regulation on food inputs in the markets it operates in.",
 ],
 'retail': [
   "Store count and square metres, with openings, closures and announced targets.",
   "Like-for-like and category disclosures the company itself published.",
   "Any announced market entry, format launch or e-commerce investment with its capital.",
   "Import, customs and foreign-currency regulation affecting the goods sold.",
 ],
 'textiles': [
   "Capacity in looms, spindles, tonnes or pieces, and any announced expansion or closure.",
   "Export incentive and rebate programmes, their rates, and any announced change or arrears.",
   "Cotton, yarn and synthetic input prices and any allocation regime.",
   "Trade agreements, quotas and duties affecting the export markets it sells into.",
   "Announced contracts with named international buyers.",
 ],
 'fintech': [
   "Transaction volume and value disclosures the company itself published, with dates.",
   "Regulator rule changes on payments, lending, e-money or interchange, with decree and date.",
   "New licences granted or applied for, and their scope.",
   "Announced merchant, bank or government partnerships and what they cover.",
   "Any announced government mandate to digitise a payment flow.",
 ],
 'financials': [
   "Assets under management, brokerage share and any figure the company itself published.",
   "Regulator rule changes on capital markets, brokerage, or asset management in this market.",
   "Announced acquisitions, licences in new markets, and new business lines.",
 ],
 'holding': [
   "EVERY MATERIAL SUBSIDIARY AND ASSOCIATE BY NAME, the percentage held, and how the company itself values it.",
   "Every announced funding round, transaction or valuation event at any unlisted holding, with the amount, the pre- or post-money valuation, the investors and the date.",
   "Announced acquisitions and disposals, with consideration and completion date.",
   "Any announced intention to list, sell down, or revalue a holding.",
   "Debt at the holding-company level as distinct from the subsidiaries, and any announced refinancing.",
 ],
 'construction': [
   "The order backlog the company itself last published, its date, and its geographic split.",
   "New awards in the last 18 months, with counterparty, country and value.",
   "Any announced claim, arbitration or contract cancellation and the amount at issue.",
   "Announced joint ventures and the share held in each.",
   "Government infrastructure programmes in the countries it works in, with announced budgets.",
 ],
 'mining': [
   "Production capacity and output by mineral, and any announced expansion or new mine with cost and dates.",
   "Reserve and resource statements the company itself published, with the date and the classification standard.",
   "Royalty, tax and mining-licence regime changes.",
   "Commodity price references for the products and their direction.",
   "Energy and power supply arrangements to the operations, and any announced tariff change.",
 ],
 'technology': [
   "Product launches and the roadmap the company itself disclosed, with dates.",
   "Capacity, supply-chain and fabrication commitments announced, with the capital attached.",
   "Export controls, tariffs and trade restrictions affecting the products or the inputs.",
   "Any regulatory or antitrust action, with the jurisdiction and the remedy sought.",
 ],
 'it_services': [
   "Deal wins and total contract value the company itself disclosed.",
   "Headcount, attrition and utilisation disclosures, with dates.",
   "Visa, immigration and offshoring regulation affecting the delivery model.",
   "Announced acquisitions and new delivery centres.",
 ],
 'batteries': [
   "Capacity in gigawatt-hours by plant, and any announced expansion, delay or cancellation.",
   "Customer supply agreements announced, with volume, term and counterparty.",
   "Subsidy and local-content regimes in the markets it sells into, and any announced change.",
   "Raw material supply agreements — lithium, nickel, cobalt — with volumes and terms.",
 ],
 'shipping': [
   "Fleet composition, vessels ordered or delivered, and the charters attached to each.",
   "Charter rates and contract terms the company itself disclosed.",
   "Newbuild orders with yard, cost and delivery date.",
   "Any announced change to a long-term contract with a parent or offtaker.",
 ],
 'airline': [
   "Fleet orders and deliveries, with aircraft type, count and dates.",
   "Route launches and terminations, and any announced traffic-rights change.",
   "Capacity and load-factor disclosures the company itself published.",
   "Fuel hedging policy where disclosed, and airport charge changes.",
 ],
 'concession': [
   "The concession terms — duration, tariff, and any announced review or renegotiation.",
   "Traffic or volume disclosures the company itself published.",
   "Announced tariff changes and the regulatory mechanism behind them.",
   "Network expansion — new gates, lanes or points — with cost and dates.",
 ],
 'conglomerate': [
   "EVERY MATERIAL SEGMENT BY NAME, with the capacity, capital programme and announced projects of each.",
   "Announced capital expenditure by segment with the years it covers.",
   "Any announced listing, demerger, stake sale or investment round in a segment, with the valuation.",
   "Regulatory changes affecting each segment separately.",
 ],
 'ceramics': [
   "Capacity in square metres or pieces by plant, and any announced expansion or line closure.",
   "Energy cost — gas and electricity tariffs for industrial users — and any announced change.",
   "Export markets, volumes and any antidumping duty affecting them.",
   "Domestic construction demand indicators and any government housing programme.",
 ],
 'general': [
   "Announced capacity, capital programmes and projects — what is being built, at what cost, and when it is guided to start.",
   "The regulatory regime the company operates under and every announced change to it.",
   "Prices and tariffs it charges or pays that are set by anyone other than the company.",
   "Contracts, licences and concessions won, lost or renewed.",
   "Announced acquisitions, disposals, capital raises and changes in ownership.",
   "Competitors entering or leaving, and capacity coming on or off in this market.",
 ],
}

# ---- THE REGULATORS, BY NAME --------------------------------------------------
# Per instruction 10-09-2026. "The regulator concerned" is not an instruction a researcher
# can act on; a NAMED body is. These are resolved for the company's own market and then
# for its industry, so a cement company is pointed at the competition authority and a
# pharmaceutical company at the drug authority, rather than at a list of everything.
MARKET_REGULATORS = {
 'EGX': ["the Egyptian Exchange (EGX) disclosure portal", "the Financial Regulatory Authority (FRA)",
         "the Central Bank of Egypt", "the General Authority for Investment (GAFI)"],
 'ADX': ["the ADX disclosure portal", "the Securities and Commodities Authority (SCA)",
         "the Central Bank of the UAE"],
 'DFM': ["the DFM disclosure portal", "the Securities and Commodities Authority (SCA)",
         "the Central Bank of the UAE"],
 'TADAWUL': ["the Tadawul disclosure portal", "the Capital Market Authority (CMA)",
             "the Saudi Central Bank (SAMA)"],
 'QSE': ["the Qatar Stock Exchange disclosure portal",
         "the Qatar Financial Markets Authority (QFMA)", "the Qatar Central Bank"],
 'NSE': ["the NSE and BSE disclosure portals", "the Securities and Exchange Board of India (SEBI)",
         "the Reserve Bank of India"],
 'KRX': ["the DART electronic disclosure system", "the Financial Supervisory Service (FSS)",
         "the Financial Services Commission (FSC)"],
 'NASDAQ': ["SEC EDGAR", "the Securities and Exchange Commission"],
}
# Industry regulators, named per market where the body differs by country.
SECTOR_REGULATORS = {
 ('EGX', 'pharma'): ["the Egyptian Drug Authority (EDA)",
                     "the Egyptian Authority for Unified Procurement (UPA)"],
 ('EGX', 'pharma_distribution'): ["the Egyptian Drug Authority (EDA)",
                                  "the Egyptian Authority for Unified Procurement (UPA)"],
 ('EGX', 'healthcare'): ["the Egyptian Healthcare Authority",
                         "the General Authority for Healthcare Accreditation and Regulation"],
 ('EGX', 'cement'): ["the Egyptian Competition Authority (ECA)",
                     "the Ministry of Trade and Industry"],
 ('EGX', 'fertiliser'): ["the Ministry of Petroleum and Mineral Resources", "EGPC",
                         "the Ministry of Agriculture and Land Reclamation",
                         "the Egyptian Customs Authority (for export duties and their repeal)"],
 ('EGX', 'refining'): ["EGPC", "the Ministry of Petroleum and Mineral Resources"],
 ('EGX', 'realestate'): ["the New Urban Communities Authority (NUCA)",
                         "the Ministry of Housing, Utilities and Urban Communities"],
 ('EGX', 'telecom'): ["the National Telecommunications Regulatory Authority (NTRA)"],
 ('EGX', 'fintech'): ["the Central Bank of Egypt", "the Financial Regulatory Authority (FRA)"],
 ('EGX', 'bank'): ["the Central Bank of Egypt"],
 ('EGX', 'utility'): ["the Egyptian Electric Utility and Consumer Protection Regulatory Agency (EgyptERA)"],
 ('EGX', 'cables'): ["the Egyptian Electric Utility and Consumer Protection Regulatory Agency (EgyptERA)",
                     "the Ministry of Electricity and Renewable Energy"],
 ('EGX', 'mining'): ["the Egyptian Mineral Resources Authority (EMRA)"],
 ('EGX', 'textiles'): ["the Export Development Fund", "the Ministry of Trade and Industry"],
 ('EGX', 'automotive'): ["the Egyptian Customs Authority", "the Ministry of Trade and Industry",
                         "the Financial Regulatory Authority (FRA), for the financing arms"],
 ('ADX', 'oilfield_services'): ["ADNOC", "the Abu Dhabi Department of Energy"],
 ('ADX', 'gas'): ["ADNOC", "the Abu Dhabi Department of Energy"],
 ('ADX', 'fuel_retail'): ["ADNOC", "the Abu Dhabi Department of Energy"],
 ('ADX', 'telecom'): ["the Telecommunications and Digital Government Regulatory Authority (TDRA)"],
 ('DFM', 'telecom'): ["the Telecommunications and Digital Government Regulatory Authority (TDRA)"],
 ('DFM', 'utility'): ["the Dubai Supreme Council of Energy", "the Dubai Regulatory and Supervisory Bureau"],
 ('DFM', 'realestate'): ["the Dubai Land Department", "RERA"],
 ('ADX', 'realestate'): ["the Abu Dhabi Department of Municipalities and Transport"],
 ('TADAWUL', 'pharma'): ["the Saudi Food and Drug Authority (SFDA)"],
 ('TADAWUL', 'telecom'): ["the Communications, Space and Technology Commission (CST)"],
 ('TADAWUL', 'mining'): ["the Ministry of Industry and Mineral Resources"],
 ('TADAWUL', 'oil_gas'): ["the Ministry of Energy"],
 ('TADAWUL', 'power_developer'): ["the Water and Electricity Regulatory Authority (WERA)",
                                  "the Saudi Power Procurement Company"],
 ('NSE', 'pharma'): ["the Central Drugs Standard Control Organisation (CDSCO)",
                     "the National Pharmaceutical Pricing Authority (NPPA)"],
 ('NSE', 'automotive'): ["the Ministry of Heavy Industries"],
 ('NASDAQ', 'technology'): ["the Federal Trade Commission", "the Bureau of Industry and Security (export controls)"],
 ('NASDAQ', 'automotive'): ["the National Highway Traffic Safety Administration (NHTSA)"],
}


def regulators(exch, sector):
    """The bodies to name in the prompt, market first then industry, de-duplicated."""
    out = list(MARKET_REGULATORS.get(exch, []))
    for r in SECTOR_REGULATORS.get((exch, sector), []):
        if r not in out:
            out.append(r)
    return out


DISPLAY = {'bank': 'banking', 'pharma': 'pharmaceuticals',
           'fertiliser': 'fertilisers', 'cables': 'cables and electrical equipment',
           'refining': 'oil refining', 'holding': 'a holding company',
           'food': 'food and beverage', 'fintech': 'fintech and payments',
           'financials': 'financial services', 'airline': 'aviation',
           'utility': 'regulated utilities', 'telecom': 'telecoms',
           'conglomerate': 'a diversified group', 'gas': 'gas',
           'realestate': 'real estate', 'oil_gas': 'oil and gas',
           'it_services': 'IT services', 'pharma_distribution': 'pharmaceutical distribution',
           'oilfield_services': 'oilfield services', 'fuel_retail': 'fuel retail',
           'power_developer': 'power development', 'concession': 'infrastructure concession'}

# ---- PER-NAME ADDITIONS -------------------------------------------------------
# An industry block is right about the industry and can still miss where a PARTICULAR
# company's value actually sits. GB Corp assembles and sells vehicles, so the automotive
# block is correct; its largest single component is a minority stake in an unlisted
# fintech, which no automotive question would ever ask about. These are added to the
# industry block rather than replacing it.
EXTRA = {
 'GBCO': ["The unlisted minority holding — every announced funding round at MNT-Halan with "
          "the amount, the pre- or post-money valuation, the investors and the date, and "
          "this company's stated percentage after each; and any announced intention to "
          "list, sell down or revalue the stake."],
 'CCAP': ["Each portfolio company by name, the percentage held, and any announced "
          "transaction, valuation event or exit at any of them."],
 'ALPHADHABI': ["Each material holding by name, the percentage held, and any announced "
                "acquisition, disposal or valuation event."],
 'IHC': ["Each material holding by name, the percentage held, and any announced "
         "acquisition, disposal, listing or valuation event."],
 'SWDY': ["Any announced infrastructure or concession project the company holds equity in "
          "rather than merely builds, with the stake, the tariff and the term."],
 'TMGH': ["The hotel and recreation portfolio and any announced addition, refurbishment or "
          "disposal; and the Saudi and wider regional expansion — what is signed, what is "
          "committed, and what is still a memorandum."],
 'ARAMCO': ["Any announced change to the government's dividend expectation or to the "
            "royalty and tax terms the company pays."],
 'EGCH': ["Whether the new complex produces ammonia, nitric acid, ammonium nitrate, or more "
          "than one of those — quote the company's own words, because its own documents "
          "have described it three different ways."],
 'PHAR': ["Named competitors holding an approved biosimilar of any molecule in this "
          "company's pipeline, with the approval date and the regulator."],
}

# ---- THE MACRO BLOCK, PER MARKET ----------------------------------------------
# The country's own news, asked about the things that actually reach a company's numbers:
# the policy rate, the currency, administered energy, the tax regime, trade instruments.
# Market-specific because the instruments differ — an Egyptian company lives and dies by a
# fuel-price announcement and an IMF review; a US one does not.
MACRO = {
 'EGX': [
   "Central Bank of Egypt policy-rate decisions over the last 18 months, each with its date "
   "and the guidance given at the meeting.",
   "The exchange-rate regime and the pound's path, plus any announced change to how the rate "
   "is managed.",
   "Announced natural-gas and electricity tariffs for industrial users, by sector.",
   "Fuel-price announcements — gasoil, mazut, petcoke — with their dates.",
   "The corporate tax regime and any announced change, including sector-specific rates.",
   "Export levies, licences and quotas INTRODUCED OR REMOVED, with the decree number and "
   "effective date. Repeals matter as much as impositions.",
   "The IMF programme — review dates, disbursements, and the structural benchmarks touching "
   "energy pricing, subsidies or state ownership.",
   "Published official inflation prints and forecasts, and the central bank's own target "
   "path, with the date each was published.",
   "State-ownership policy and any announced divestment of a listed or listable asset.",
 ],
 'ADX': [
   "Central Bank of the UAE rate decisions and any divergence from the US Federal Reserve.",
   "Announced federal or emirate-level corporate tax changes and their effective dates.",
   "Announced changes to energy, utility or fuel pricing for industrial users.",
   "Federal and Abu Dhabi capital-spending programmes and any announced budget.",
   "Foreign-ownership, listing and free-zone rule changes.",
 ],
 'TADAWUL': [
   "Saudi Central Bank rate decisions and any divergence from the US Federal Reserve.",
   "Announced changes to zakat, corporate tax, or the levy on expatriate labour.",
   "Energy and feedstock pricing announcements for industrial users.",
   "Vision 2030 and Public Investment Fund programmes with announced budgets and dates.",
   "Local-content (IKTVA-type) rules and any announced change.",
 ],
 'QSE': [
   "Qatar Central Bank rate decisions.",
   "Announced corporate tax or fee changes.",
   "State capital programmes and announced budgets.",
   "Energy pricing and LNG expansion announcements that set the domestic economy's path.",
 ],
 'NSE': [
   "Reserve Bank of India policy decisions with dates and guidance.",
   "Union Budget measures affecting this company's sector, with effective dates.",
   "GST and customs-duty changes.",
   "Production-linked incentive schemes and any announced change.",
 ],
 'KRX': [
   "Bank of Korea rate decisions with dates and guidance.",
   "Announced corporate tax and subsidy changes.",
   "Export controls and trade measures affecting this company's sector.",
 ],
 'NASDAQ': [
   "Federal Reserve decisions and guidance.",
   "Tariffs, export controls and trade measures affecting this company's products or inputs.",
   "Announced federal subsidy, tax-credit or procurement programmes touching this sector.",
 ],
}
MACRO['DFM'] = MACRO['ADX']

# ---- THE COMPANY'S OWN FORWARD PLANS, EVERY NAME -------------------------------
# The sector block asks what the INDUSTRY turns on. This asks what THIS COMPANY has
# actually said it is going to do, which is a different question and is the same question
# whatever the industry.
COMPANY_FORWARD = [
 "Everything the company itself has announced and not yet finished — projects, plants, "
 "expansions, market entries. For each: what it is, the sanctioned cost, how it is "
 "financed, the guided completion or first-revenue date, and the percentage complete if "
 "stated.",
 "SLIPPAGE: any guided date that has MOVED, with the old date, the new date and the reason "
 "given. A project that slipped matters as much as one that landed.",
 "Any guidance the company itself published — volumes, backlog, deliveries, margins, "
 "capital expenditure — with the date it published it. NOT another analyst's forecast.",
 "Announced capital raises, debt issues, refinancings, dividend-policy statements, "
 "acquisitions, disposals, and any change in who controls the company.",
 "Management changes, board decisions and any dispute, claim or arbitration disclosed.",
]

# The language the local record is written in. Naming the LANGUAGE beats printing the
# company's name in it and hoping the researcher infers the instruction.
LANGUAGE = {'EGX': 'Arabic', 'ADX': 'Arabic', 'DFM': 'Arabic', 'TADAWUL': 'Arabic',
            'QSE': 'Arabic', 'KRX': 'Korean', 'NSE': 'Hindi and the regional languages'}

STUDY_DIR_ALIAS = {'SWDY': 'swdy_study', 'PHAR': 'phar_study', 'ADIB': 'adib_study'}


def _register():
    p = subprocess.run(['node', '-e',
                        "const fs=require('fs');const src=fs.readFileSync(process.argv[1],'utf8');"
                        "const sandbox={};const vm=require('vm');vm.createContext(sandbox);"
                        "vm.runInContext(src,sandbox);"
                        "console.log(JSON.stringify(sandbox.TICKERS||sandbox.tickers||{}));",
                        DATA_JS], capture_output=True, text=True)
    if p.returncode == 0 and p.stdout.strip() not in ('', '{}'):
        return json.loads(p.stdout)
    sys.path.insert(0, HERE)
    from campaign_queue import load_register
    return load_register()[0]


def _study_dir(tk):
    cand = STUDY_DIR_ALIAS.get(tk, tk.lower() + '_study')
    d = os.path.join(HERE, cand)
    return d if os.path.isdir(d) else None


def open_questions(tk):
    """The study's OWN declared open questions — its recorded negative searches.

    These are the things it went looking for, could not find, and wrote down. Nothing a
    template can know, and the most valuable lines on the page."""
    d = _study_dir(tk)
    if not d:
        return None, "no study directory, so no recorded negative searches — this is a first build"
    reg = os.path.join(d, 'sweep_register.json')
    if not os.path.exists(reg):
        return None, "a study directory exists but carries no sweep register, so its open questions are not recorded anywhere this can read"
    j = json.load(open(reg, encoding='utf-8'))
    out = []
    for f in j.get('findings', []):
        if f.get('klass') != 'NEGATIVE_SEARCH':
            continue
        h = f.get('headline', '')
        inner = (h[h.find('(') + 1:h.rfind(')')] if '(' in h else h).strip()
        # A register entry is written for the register: it carries the whole search
        # history and what it cost. A prompt has to carry the QUESTION. Take the first
        # sentence or so and say when there is more, rather than pasting an internal
        # note at a researcher and hoping they find the question inside it.
        if len(inner) > 320:
            cut = inner.rfind('. ', 0, 320)
            inner = (inner[:cut + 1] if cut > 120 else inner[:317].rstrip() + '…')
        out.append((f.get('source_date', ''), inner))
    return out, None


PART1_HEAD = """## PART 1 — paste this first, once per session

> You are a research assistant working on listed-equity valuation. I need
> **forward-looking, source-backed** information only. Follow these rules exactly, for
> every answer in this session.
>
> **1. Sources, in this order of preference:** the company's own investor-relations page,
> its earnings-call transcripts and presentations, its own press releases; then
> %REGULATORS%; then a named wire service. Never a forum, a blog, an aggregator, or another
> analyst's price target or rating.
>
> **2. SEARCH IN THE LANGUAGE THE SOURCE IS WRITTEN IN.** A ministerial decision, a decree
> register, a customs circular and the trade press that covers them are usually in the
> national language, not in English. Search in that language as well as in English, and
> tell me which languages you searched. If you searched only in English, say so — an
> English-only search that finds nothing has not established that nothing exists.
>
> **3. Every claim carries a date and a link.** If you cannot give me the date the thing
> was said and a link to where it was said, do not give me the claim.
>
> **4. Say when you found nothing.** "No announcement located" is a useful answer and I
> want it explicitly. Do not fill a gap with an estimate, an industry average, or a
> plausible-sounding number. An invented figure is worse than a blank, because I will spend
> a day tracing it.
>
> **5. Separate what was ANNOUNCED from what is UNDER STUDY from what a journalist
> SPECULATED.** Label every item with one of those three words. A proposal a regulator is
> examining is not a rule in force, and reporting it as one is the single most common error
> in this kind of research.
>
> **6. Do not give me historical financial-statement figures** — revenue, profit, margins,
> balance-sheet lines. I have those from the filings and I will not use yours. If a plan is
> quantified in a filing, quote the plan, not the accounts.
>
> **7. Quantify wherever the source does,** in the unit the source uses: tonnes, megawatts,
> units, feddans, square metres, beds, packs, branches, currency per unit. A capacity
> expansion without a number is half an answer.
>
> **8. Give me dates and stages.** Announced when, sanctioned when, mechanically complete
> when, commissioned when, first revenue when. A project that slipped matters as much as
> one that did not — say so if the guided date moved, and by how much.
>
> **9. Prefer the last 18 months.** Anything older, mark it clearly as older and tell me
> whether it is still live.
>
> **10. Distinguish a group figure from a single asset's figure.** If a capacity, a
> headcount or an output number covers more than the thing I asked about, say what it
> covers.
>
> Answer as a list of dated items, newest first, grouped under the headings I give you. No
> preamble and no closing summary."""


def build(tk):
    """ONE PROMPT, SHORT. Per instruction 10-09-2026: neither research tool takes a
    two-part prompt, and one of them degrades on long ones. So the rules are compressed to
    a line each and the SCOPE gets the room — the scope is the part that is specific to
    this company and is the reason to generate the prompt at all."""
    tk = tk.upper()
    reg = _register()
    rec = reg.get(tk)
    if rec is None:
        raise SystemExit("%s is not a covered name. This tool refuses rather than "
                         "returning a generic prompt for a ticker it does not hold." % tk)
    name = rec.get('name', tk)
    name_ar = rec.get('nameAr', '')
    code = rec.get('code', tk)
    exch = code.split(':')[0] if ':' in code else ''
    sector = SECTOR.get(tk)
    block = list(BLOCKS.get(sector or 'general', BLOCKS['general'])) + EXTRA.get(tk, [])
    negs, why = open_questions(tk)
    regs = regulators(exch, sector)
    lang = LANGUAGE.get(exch)
    ind = DISPLAY.get(sector, (sector or 'not classified').replace('_', ' '))

    Q = []
    Q.append("Research **%s** (%s%s) for a valuation I am building — it operates in %s. "
             "Forward-looking only."
             % (name, code, (', %s' % name_ar) if name_ar else '', ind))
    Q.append("")
    Q.append("**Rules.**")
    src = '; '.join(regs[:4]) if regs else "its exchange, its securities regulator and its industry regulator"
    Q.append("- Sources: the company's own filings, IR page, presentations and releases "
             "first; then %s; then a named wire service. No forums, blogs, aggregators or "
             "analyst price targets." % src)
    if len(regs) > 4:
        Q.append("- Also check: %s." % '; '.join(regs[4:]))
    Q.append("- Every item: a date and a link. No date or link, leave it out.")
    Q.append("- Found nothing? Say \"none located\". Never estimate or fill a gap.")
    Q.append("- Tag every item ANNOUNCED, UNDER STUDY or SPECULATED.")
    Q.append("- No historical revenue, profit, margins or balance-sheet lines — I have the "
             "filings.")
    Q.append("- Quantify in the source's own units, and say if a figure covers the whole "
             "group rather than one asset.")
    if lang:
        Q.append("- Search in %s as well as English, and tell me which languages you used."
                 % lang)
    Q.append("- Last 18 months preferred. Newest first. No preamble, no summary.")
    Q.append("")
    Q.append("**A. Macro — only where it reaches this company.**")
    macro = MACRO.get(exch)
    if macro:
        for q in macro:
            Q.append("- %s" % _tight(q))
    else:
        Q.append("- Policy rate and its path; currency regime; administered energy and fuel "
                 "prices; corporate tax; any duty, levy, quota or licence imposed OR "
                 "REMOVED. Name the body that set each.")
    Q.append("")
    Q.append("**B. Industry — %s.**" % ind)
    if not sector:
        Q.append("- (I have not classified this industry; say if these headings miss what "
                 "actually drives it.)")
    for q in block:
        Q.append("- %s" % _tight(q))
    Q.append("")
    Q.append("**C. The company's own plans.**")
    for q in COMPANY_FORWARD:
        Q.append("- %s" % _tight(q))
    if negs:
        Q.append("")
        Q.append("**D. Our own dead ends — we looked for each of these on the date shown "
                 "and found nothing. Has anything been published since? A plain \"still "
                 "nothing\" is a useful answer.**")
        for date, q in negs[:6]:
            Q.append("- [%s] %s" % (date or 'undated', _gap(q)))

    body = '\n'.join(Q)
    L = ["# Research primer — %s (%s)" % (name, code), "",
         "One prompt, one paste — into Perplexity and into Gemini separately. "
         "%d characters." % len(body), "",
         "---", "", body, "", "---", "",
         "*What comes back is a lead, not an input: every claim is traced to the primary "
         "source it cites before it moves anything, historicals come from the filings "
         "alone, and whatever does not survive tracing is recorded as a dated negative "
         "search rather than dropped.*"]
    return '\n'.join(L)


def _tight(q, cap=200):
    """Trim a heading's explanatory tail. The reasoning in these strings is for the analyst
    reading the source, not for the researcher reading the prompt, and one of the two tools
    degrades on length."""
    q = q.strip()
    if len(q) <= cap:
        return q
    cut = q.rfind('. ', 0, cap)
    if cut > 80:
        return q[:cut + 1].strip()
    cut = q.rfind(', ', 0, cap)
    return (q[:cut] if cut > 80 else q[:cap - 1].rstrip()) + '…'


def _gap(q, cap=170):
    """A register entry carries its whole search history and is written in the register's
    own voice — "Searched for X and found none". A researcher needs the ASK, so the voice
    is turned round here rather than pasted at them as an internal note."""
    q = q.strip()
    q = re.sub(r'^Searched for\s+', '', q)
    q = re.sub(r'^A\s+DISCLOSED\s+', 'a disclosed ', q)
    q = re.sub(r'^(A|AN|THE)\s+', '', q)
    m = re.search(r'\s+and (did not obtain|found no|was not)', q)
    if m and m.start() > 40:
        q = q[:m.start()]
    q = q.rstrip(' ,;')
    if len(q) <= cap:
        return q
    cut = q.rfind(', ', 0, cap)
    return (q[:cut] if cut > 60 else q[:cap - 1].rstrip()) + '…'



def build_generic():
    """The reusable half as ONE short prompt, the same shape as the per-name one.

    RESTORED 10-09-2026 after the single-prompt rewrite deleted it while main() went on
    calling it — a NameError that only fires when --generic is actually run, so the module
    imported cleanly and the per-name path passed every test. Import-not-parse catches a
    module that cannot load; it does not catch a branch nothing exercised.

    Shares the rule set and the forward-plans block with build() rather than carrying its
    own copy, so the two cannot drift — which is the whole reason this is a generator."""
    Q = ["Research **{COMPANY}** ({EXCHANGE}) for a valuation I am building. "
         "Forward-looking only.", "",
         "**Rules.**",
         "- Sources: the company's own filings, IR page, presentations and releases first; "
         "then its exchange's disclosure portal, its securities regulator, and the industry "
         "regulator concerned — NAME the ones you used; then a named wire service. No "
         "forums, blogs, aggregators or analyst price targets.",
         "- Every item: a date and a link. No date or link, leave it out.",
         '- Found nothing? Say "none located". Never estimate or fill a gap.',
         "- Tag every item ANNOUNCED, UNDER STUDY or SPECULATED.",
         "- No historical revenue, profit, margins or balance-sheet lines — I have the "
         "filings.",
         "- Quantify in the source's own units, and say if a figure covers the whole group "
         "rather than one asset.",
         "- If the regulator, decree register or trade press publishes in another language, "
         "search in it too and tell me which languages you used.",
         "- Last 18 months preferred. Newest first. No preamble, no summary.", "",
         "**A. Macro — only where it reaches this company.**",
         "- Policy rate and its path, with the guidance given at each decision.",
         "- Currency regime and any announced change to it.",
         "- Administered energy, fuel and electricity prices for industrial users.",
         "- Corporate tax, including any sector-specific rate.",
         "- Duties, levies, quotas and licences IMPOSED OR REMOVED, with the instrument and "
         "its effective date. Repeals matter as much as impositions.",
         "- Any IMF or state programme, and state-ownership or privatisation policy.", "",
         "**B. Industry.**",
         "- Capacity entering or leaving this market, and named competitors' announced "
         "expansions, entries, exits or mergers.",
         "- Prices, tariffs, quotas or subsidies set by anyone other than the company.",
         "- Regulation specific to this industry, and the body that made each change.",
         "- Input costs and supply — raw materials, energy, feedstock — with any "
         "disruption, curtailment, allocation regime or shortage.", "",
         "**C. The company's own plans.**"]
    for q in COMPANY_FORWARD:
        Q.append("- %s" % _tight(q))
    Q += ["- The order book or backlog: the figure the COMPANY last published, its date and "
          "its split by segment or geography. If it publishes none, say so.",
          "- New orders, contracts and tender awards, with counterparty, country, value and "
          "delivery period.",
          "- Any material stake in an unlisted company, every announced funding round or "
          "valuation event at it, and the percentage held after each."]
    body = "\n".join(Q)
    return "\n".join([
        "# Research primer — the generic prompt", "",
        "Any company, no waiting. Fill in the company and its exchange, then one paste into "
        "Perplexity and one into Gemini. %d characters." % len(body), "",
        "The company-specific version adds the named regulators for that market, the "
        "industry's own driver headings, and the questions our study has already recorded "
        "it could not answer. It does not replace this.", "",
        "---", "", body, "", "---", "",
        "*What comes back is a lead, not an input: traced to the primary source before it "
        "moves anything, historicals from the filings alone, and whatever does not survive "
        "tracing recorded as a dated negative search rather than dropped.*"])


def main(argv):
    if not argv or argv[0] in ('-h', '--help'):
        raise SystemExit(__doc__)
    if argv[0] == '--generic':
        text = build_generic()
        out = argv[argv.index('--out') + 1] if '--out' in argv else None
        if out:
            io_open = open(out, 'w', encoding='utf-8')
            io_open.write(text + "\n"); io_open.close()
            print("wrote %s (%d characters)" % (out, len(text)))
        else:
            print(text)
        return
    tk = argv[0]
    text = build(tk)
    out = None
    if '--out' in argv:
        out = argv[argv.index('--out') + 1]
    if out:
        with open(out, 'w', encoding='utf-8') as fh:
            fh.write(text + "\n")
        print("wrote %s (%d characters)" % (out, len(text)))
    else:
        print(text)


if __name__ == '__main__':
    main(sys.argv[1:])
