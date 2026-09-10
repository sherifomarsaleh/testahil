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
import json, os, subprocess, sys

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
   "Announced electricity-tariff changes for industrial users.",
   "Domestic price references and export volumes.",
   "New entrants, and capacity coming on or leaving this market.",
 ],
 'bank': [
   "Central bank policy-rate decisions over the last 18 months, with dates and the guidance given at each.",
   "Announced changes to reserve requirements, loan-to-deposit rules, capital rules, or the treatment of sovereign holdings.",
   "The corporate tax rate applied to banks in this market, and any announced change.",
   "The bank's branch, digital and lending expansion plans, with numbers and target dates.",
   "Any announced capital raise, sukuk or bond issue, or dividend-policy statement.",
   "Regulatory initiatives directing lending to particular sectors, and the subsidised rates attached to them.",
   "Anything announced about a parent's intentions for this entity, or about a merger or acquisition.",
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
   "Any announced dividend policy, capital increase, or change in government shareholding.",
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
   "Any announced capital raise or change in ownership.",
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
   "Announced acquisitions and their consideration.",
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


DISPLAY = {'realestate': 'real estate', 'oil_gas': 'oil and gas',
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

    L = []
    L.append("# Research primer — %s (%s)" % (name, code))
    L.append("")
    L.append("Generated from the repository's own record of this name on the day it was run. "
             "Two parts: the rules, which are the same for every company and are pasted once "
             "per session, and the question set, which is specific to this company and to "
             "the industry it operates in. Paste PART 1 first, then PART 2 as a single "
             "message. Run it in Perplexity and in Gemini separately — they fail in "
             "different directions and the disagreements are informative.")
    L.append("")
    L.append("---")
    L.append("")
    regs = regulators(exch, sector)
    if regs:
        reg_text = ('; '.join(regs[:-1]) + '; and ' + regs[-1]) if len(regs) > 1 else regs[0]
    else:
        # NAMED OR DECLARED, NEVER SILENTLY GENERIC [R-ENF-04]. A prompt that says "the
        # regulator concerned" hands the researcher the job of working out which body that
        # is, which is the job the repository is better placed to do. Where it cannot, it
        # says so rather than emitting a generic phrase that reads like an instruction.
        reg_text = ("the regulators that govern this company — I could not resolve them "
                    "from my own records for this market and sector, so name the ones you "
                    "used")
    L.append(PART1_HEAD.replace('%REGULATORS%', reg_text))
    L.append("")
    L.append("---")
    L.append("")
    L.append("## PART 2 — the company")
    L.append("")
    L.append("> **Company:** %s" % name)
    if name_ar:
        L.append("> **Its own name in Arabic, for searching the local record:** %s" % name_ar)
    L.append("> **Listed on:** %s, ticker %s" % (exch or 'see code', tk))
    if sector:
        L.append("> **Industry:** %s" % DISPLAY.get(sector, sector.replace('_', ' ')))
    else:
        L.append("> **Industry: NOT CLASSIFIED in this repository.** The headings below are "
                 "the general set rather than an industry-specific one, and that is stated "
                 "here rather than hidden — an unclassified name should not receive a "
                 "generic prompt that looks tailored.")
    L.append(">")
    L.append("> Give me, for this company, under these headings:")
    L.append(">")
    for i, q in enumerate(block):
        L.append("> **(%s)** %s" % (chr(ord('a') + i), q))
    L.append("")

    L.append("## PART 3 — what our own study went looking for and could not find")
    L.append("")
    if negs:
        L.append("These are the highest-value questions on the page. Each one is something "
                 "this company's study searched for, failed to find, and recorded with the "
                 "date it searched. If a research pass closes any of them it is worth more "
                 "than everything in PART 2.")
        L.append("")
        L.append("> Separately from the above, I have specific gaps. For each, tell me "
                 "whether anything has been published since the date shown, and if not, say "
                 "so explicitly:")
        L.append(">")
        for date, q in negs:
            L.append("> - **[searched %s]** %s" % (date or 'undated', q))
        L.append("")
    else:
        L.append("*%s.*" % (why or 'no recorded negative searches'))
        L.append("")
        L.append("So there is nothing to add here yet. On a re-issue this section fills "
                 "itself from the study's own register.")
        L.append("")

    L.append("---")
    L.append("")
    L.append("## What happens to what comes back")
    L.append("")
    L.append("Anything a research pass returns is a **lead, not an input**. Before a number "
             "from it can enter a model it has to be traced to the primary source it cites "
             "and read there. Historical financial figures come from the company's own "
             "issued financial statements and from nowhere else, whatever a research pass "
             "says about them.")
    L.append("")
    L.append("Where the two passes disagree on a figure, the disagreement is itself the "
             "finding and it gets recorded: one of them made the number up, and a study that "
             "took the higher of two search results would have published it. Every claim "
             "that does not survive tracing is written into the study's sweep register as a "
             "dated negative search rather than quietly dropped — otherwise the next pass "
             "reports it again and it is investigated from scratch.")
    return "\n".join(L)


GENERIC_BLOCK = [
 "COMPANY NEWS — everything the company itself has said or had said about it, newest first. "
 "Results releases, board decisions, management changes, disputes, anything filed with its "
 "exchange.",
 "THE ORDER BOOK OR BACKLOG — the figure the company itself last published, the date it "
 "published it, and its split by segment, product or geography if it gave one. If it "
 "publishes no backlog, say so; some businesses have none and that is an answer.",
 "NEW ORDERS, CONTRACTS AND TENDER AWARDS in the last 18 months, with the counterparty "
 "named, the country, the value, and the delivery period.",
 "THE PROJECT PIPELINE — everything announced but not yet finished. For each: what it is, "
 "what it will produce, the sanctioned cost, how it is financed, the guided completion or "
 "first-revenue date, and the percentage complete if stated.",
 "FUTURE CAPACITY PLANS — capacity added, announced, mothballed or closed, in the unit the "
 "company uses: tonnes, megawatts, units, square metres, beds, packs, lines, branches, "
 "rooms, subscribers. Say whether a figure covers one asset or the whole group.",
 "SLIPPAGE — any project or capacity target whose guided date has MOVED, with the old date, "
 "the new date, and the reason given. A slipped project matters as much as a delivered one.",
 "THE INDUSTRY IT SITS IN — capacity entering or leaving this market, named competitors' "
 "announced expansions, and any consolidation, entry or exit.",
 "PRICES AND TARIFFS SET BY SOMEONE OTHER THAN THE COMPANY — administered prices, "
 "regulated tariffs, subsidies, quotas, export duties or levies, and every announced change "
 "with the instrument that made it and its effective date. Include repeals, not only "
 "impositions.",
 "REGULATION AND POLICY affecting this business, from the bodies that actually govern it. "
 "Label each item ANNOUNCED, UNDER STUDY or SPECULATED — a proposal a regulator is examining "
 "is not a rule in force.",
 "INPUT COSTS AND SUPPLY — the main raw materials, energy and feedstock, their announced "
 "prices or allocation regimes, and any disruption, curtailment or shortage.",
 "MONEY IN AND OUT — announced capital raises, debt issues, refinancings, dividend policy "
 "statements, acquisitions, disposals, and any change in who controls the company.",
 "STAKES IN THINGS NOT ON THE EXCHANGE — any material holding in an unlisted company, every "
 "announced funding round or valuation event at it, and the percentage held after each.",
]


def build_generic():
    """The reusable half, with no company resolved.

    The point of a generator is one source of truth: this shares PART 1 verbatim with the
    per-name prompt, so the rules cannot drift between the generic prompt and the specific
    one. Only the question set is general, and it asks for the ground that is worth asking
    about whatever the company does — news, backlog, pipeline, capacity, regulation."""
    L = ["# Research primer — the generic prompt",
         "",
         "Use this for any company, on its own, without waiting for the company-specific "
         "supplement. Fill in ONE thing: the company and its exchange. The company-specific "
         "prompt that follows later adds the industry's own driver headings and the "
         "questions our study has already recorded it could not answer — it does not "
         "replace this.",
         "", "---", "",
         PART1_HEAD.replace('%REGULATORS%',
             "the bodies that actually regulate this company — NAME THEM in your answer, "
             "including the exchange's own disclosure portal, the securities regulator, the "
             "central bank where it is a financial, and the industry regulator concerned"),
         "", "---", "",
         "## PART 2 — the company", "",
         "> **Company:** {COMPANY NAME}, listed on {EXCHANGE}.",
         ">",
         "> If the company's own regulator, decree register or trade press publishes in a "
         "language other than English, search in that language too and tell me which "
         "languages you used.",
         ">",
         "> Give me, under these headings:", ">"]
    for i, q in enumerate(GENERIC_BLOCK):
        L.append("> **(%d)** %s" % (i + 1, q))
    L += ["",
          "---", "",
          "## What happens to what comes back", "",
          "Anything a research pass returns is a **lead, not an input**. Before a number "
          "from it can enter a model it has to be traced to the primary source it cites and "
          "read there. Historical financial figures come from the company's own issued "
          "financial statements and from nowhere else, whatever a research pass says about "
          "them.", "",
          "Where two passes disagree on a figure, the disagreement is itself the finding: "
          "one of them made the number up, and a study that took the higher of two search "
          "results would have published it. Every claim that does not survive tracing is "
          "recorded as a dated negative search rather than quietly dropped."]
    return "\n".join(L)


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
