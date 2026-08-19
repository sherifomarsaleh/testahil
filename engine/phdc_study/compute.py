"""PHDC study — master computation. Writes study_numbers.json, the single source of
truth for every builder. Code-first rule: INPUTS are four-field records
{value, source, date, ring}; a bare financial numeral cannot enter a builder; the
ASSERT block raises (no JSON emitted) unless every reconciliation closes.

FUNDAMENTAL REFRESH, 19-Aug-2026. Supersedes the 11-Jun-2026 edition, which was
built before the 30-Jun-2026 interim statements existed and before the model-study
skeleton was adopted (08-Aug-2026). This is a fundamentals-only pass: the price
side (technical read, probabilistic map) is carried forward unchanged and labelled
with its own as-of stamps.

BUILT ON THE COMPANY'S OWN ISSUED STATEMENTS (SIGCM clause 1 — official sources
only for the subject's reported historicals):
  * Interim consolidated financial statements as of 30 June 2026, limited review
    report by Forvis Mazars Mostafa Shawki (Khaled Said El Rabat, FRA reg. 258),
    Cairo 17-Aug-2026, board authorisation 17-Aug-2026 — supplied by the user.
  * Audited consolidated financial statements for the year ended 31 Dec 2024, with
    31 Dec 2023 comparatives — palmhillsdevelopments.com investor-relations CDN.
  * Company earnings releases (COMPANY_IR): 1Q2026 (20-May-2026), 9M2025
    (13-Nov-2025), 1H2025 (13-Aug-2025) — same CDN.

Company class: Egyptian residential real-estate DEVELOPER selling on multi-year
instalments and recognising revenue on percentage-of-completion at the contract-unit
level. Lens set follows the operating-company reference (SWDY pattern inside the
model-study skeleton): FCFF DCF primary, book value & sustainable return, relative
multiples, normalised earnings power.

THE CONTESTED JUDGEMENT (computed BOTH WAYS, published side by side, never
averaged): whether the Residents' Association balance — EGP 34,337mn at 30-Jun-2026,
note 63 — is PERMANENT OPERATING FUNDING of the enterprise or RESTRICTED
THIRD-PARTY MONEY. It is the largest single source of the company's operating cash
flow: strip its movement out and reported operating cash flow is negative in every
period disclosed (FY2023, FY2024, H1-2026).

THE CRUX (sensitised in real observable units): revenue recognised per Egyptian
pound of construction cost relieved to the income statement — the price-to-build-cost
ratio. Measured 3.119x in H1-2026.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
os.chdir(HERE)
import numpy as np

# ============================ INPUT REGISTER =================================
# Statement figures in EGP mn (the filings print EGP units; /1e6 is a unit
# conversion, not a derivation). Per-share figures in EGP. Ratios as decimals.
def I(value, source, date, ring):
    return dict(value=value, source=source, date=date, ring=ring)

FS26 = ("Interim consolidated financial statements as of 30 June 2026, Palm Hills "
        "Developments Company S.A.E — limited review report, Forvis Mazars Mostafa "
        "Shawki, Cairo 17-Aug-2026 (COMPANY_OFFICIAL)")
FS24 = ("Audited consolidated financial statements for the year ended 31 Dec 2024 "
        "with 31 Dec 2023 comparatives, palmhillsdevelopments.com investor-relations "
        "asset library (COMPANY_OFFICIAL)")
IR1Q26 = ("Palm Hills Developments 1Q2026 Earnings Release, 20-May-2026, "
          "palmhillsdevelopments.com investor-relations asset library (COMPANY_IR)")
IR9M25 = ("Palm Hills Developments 9M2025 Earnings Release, 13-Nov-2025, same CDN "
          "(COMPANY_IR)")
IR1H25 = ("Palm Hills Developments 1H2025 Earnings Release, 13-Aug-2025, same CDN "
          "(COMPANY_IR)")
CBE_B = ("Central Bank of Egypt, EGP Treasury Fixed Coupon Bonds auction result, "
         "auction date 17-Aug-2026, issue 18-Aug-2026 — accepted weighted-average "
         "yields (PRIMARY_MARKET_DATA)")
CBE_T = ("Central Bank of Egypt, EGP Treasury Bill auction results, auctions "
         "13-Aug-2026 and 16-Aug-2026, issue 18-Aug-2026 (PRIMARY_MARKET_DATA)")
DAMO = ("Damodaran country default spreads and risk premiums, ORIGINAL file "
        "ctrypremJuly26.xlsx sheet 'ERPs by country', Egypt row — CDS spreads as of "
        "30-Jun-2026, rating default spreads updated 30-Jun-2026 (PRIMARY_MARKET_DATA)")
BETA = ("engine/beta_regression.own_stock_beta('PHDC','EG','EGX') — Dimson-adjusted "
        "weekly own-stock regression against EGX30 read from "
        "engine/raw_indices/EG/EGX30.csv (PRIMARY_MARKET_DATA)")
IND = ("Daily News Egypt, 'Top 10 Egyptian developers' sales rise to EGP 670bn in H1 "
       "2026', 18-Aug-2026 — market survey (INDUSTRY, secondary)")
STEEL = ("Egyptian producer rebar sales prices for August 2026 (Ezz 39,850, Beshay "
         "39,200, Suez 38,950, Egyptian Steel 37,350 EGP/t; smaller mills "
         "33,800-36,500), reported unchanged versus July after earlier declines "
         "(INDUSTRY, secondary)")
CEMPATH = ("Egyptian local cement realised-price path adopted in the ARCC valuation "
           "study of 06-Aug-2026 (engine/arcc_study, input price_local_path), itself "
           "anchored on Arabian Cement Company's disclosed price history (INDUSTRY)")
CPI = ("Central Agency for Public Mobilization and Statistics urban headline inflation "
       "14.9% for July 2026 (14.3% June); Central Bank of Egypt annual core 14.7% "
       "July 2026 (COUNTRY)")
MPC = ("Central Bank of Egypt Monetary Policy Committee, 9-Jul-2026 — overnight "
       "deposit rate held at 19.00% after 825bp of cuts between April 2025 and "
       "February 2026 (COUNTRY)")
FX = ("USD/EGP mid-market 50.52 on 19-Aug-2026; 30-day range 49.65-51.36 (COUNTRY)")
PEER = ("Market-data aggregators, quotes dated 11-Aug-2026 (Egypt) and June/August "
        "2026 (Gulf): Simply Wall St, TradingView, stockanalysis.com (AGGREGATOR — "
        "cross-check only, never a source for the subject's own historicals)")
PRIOR = ("PHDC Valuation Study of 11-Jun-2026 and its companion workbook "
         "(PHDC_Valuation_Study_11062026_public.xlsx), superseded by this edition")
PAGE = ("assets/data.js, TICKERS.PHDC — published cone and technical read carried "
        "forward unchanged by this fundamentals-only refresh")

# ---------------------------------------------------------------------------
# 1. HISTORICAL INCOME STATEMENT — official statements only
# ---------------------------------------------------------------------------
INP = {}
def reg(k, value, source, date, ring):
    INP[k] = I(value, source, date, ring)
    return value

# --- H1-2026 and H1-2025 (reviewed interim, EGP mn) ---
rev_h126      = reg('rev_h126', 19528.117727, FS26 + ' — consolidated statement of income, revenues', '30-Jun-2026', 'Company')
rev_h125      = reg('rev_h125', 15579.129165, FS26 + ' — comparative column', '30-Jun-2025', 'Company')
rev_q226      = reg('rev_q226', 10181.983983, FS26 + ' — three months 1-Apr to 30-Jun-2026', '30-Jun-2026', 'Company')
rev_q225      = reg('rev_q225', 7186.576327, FS26 + ' — comparative quarter', '30-Jun-2025', 'Company')
cogs_h126     = reg('cogs_h126', 12539.272168, FS26 + ' — cost of revenues', '30-Jun-2026', 'Company')
cogs_h125     = reg('cogs_h125', 8859.894363, FS26 + ' — cost of revenues, comparative', '30-Jun-2025', 'Company')
cashdisc_h126 = reg('cashdisc_h126', 62.823483, FS26 + ' — cash discount', '30-Jun-2026', 'Company')
cashdisc_h125 = reg('cashdisc_h125', 54.546305, FS26 + ' — cash discount, comparative', '30-Jun-2025', 'Company')
gp_h126       = reg('gp_h126', 6926.022076, FS26 + ' — gross operating profit', '30-Jun-2026', 'Company')
gp_h125       = reg('gp_h125', 6664.688497, FS26 + ' — gross operating profit, comparative', '30-Jun-2025', 'Company')
sga_h126      = reg('sga_h126', 2845.851571, FS26 + ' — general administrative, selling and marketing expenses (note 66)', '30-Jun-2026', 'Company')
sga_h125      = reg('sga_h125', 2206.171375, FS26 + ' — same line, comparative', '30-Jun-2025', 'Company')
ecl_h126      = reg('ecl_h126', 13.993604, FS26 + ' — expected credit losses (note 68)', '30-Jun-2026', 'Company')
ecl_h125      = reg('ecl_h125', 14.079079, FS26 + ' — expected credit losses, comparative', '30-Jun-2025', 'Company')
da_is_h126    = reg('da_is_h126', 245.908913, FS26 + ' — depreciation & amortization charged below gross profit', '30-Jun-2026', 'Company')
fin_h126      = reg('fin_h126', 1676.543172, FS26 + ' — finance costs & interests (note 67)', '30-Jun-2026', 'Company')
fin_h125      = reg('fin_h125', 1337.781283, FS26 + ' — finance costs & interests, comparative', '30-Jun-2025', 'Company')
land_int_h126 = reg('land_int_h126', 213.067737, FS26 + ' — note 67, land installment interest', '30-Jun-2026', 'Company')
bank_int_h126 = reg('bank_int_h126', 1463.475435, FS26 + ' — note 67, financing costs and interests', '30-Jun-2026', 'Company')
amort_nr_h126 = reg('amort_nr_h126', 523.193960, FS26 + ' — amortization of discount on notes receivable (note 69)', '30-Jun-2026', 'Company')
amort_nr_h125 = reg('amort_nr_h125', 365.909544, FS26 + ' — same line, comparative', '30-Jun-2025', 'Company')
fvtpl_h126    = reg('fvtpl_h126', 15.253619, FS26 + ' — gains on investments at fair value through profit or loss (note 69)', '30-Jun-2026', 'Company')
tbillinc_h126 = reg('tbillinc_h126', 455.606067, FS26 + ' — credit interest and returns on investments measured at amortized cost (note d31)', '30-Jun-2026', 'Company')
pbt_h126      = reg('pbt_h126', 3137.778462, FS26 + ' — net profit before income tax & non-controlling equities', '30-Jun-2026', 'Company')
pbt_h125      = reg('pbt_h125', 3587.606310, FS26 + ' — same line, comparative', '30-Jun-2025', 'Company')
curtax_h126   = reg('curtax_h126', 844.118629, FS26 + ' — current income tax (note 70a)', '30-Jun-2026', 'Company')
deftax_h126   = reg('deftax_h126', 1.133557, FS26 + ' — deferred tax (note 70b)', '30-Jun-2026', 'Company')
nci_h126      = reg('nci_h126', 27.703559, FS26 + ' — non-controlling equities share', '30-Jun-2026', 'Company')
np_h126       = reg('np_h126', 2264.822717, FS26 + ' — net profit after income tax & non-controlling equities', '30-Jun-2026', 'Company')
np_h125       = reg('np_h125', 2443.380942, FS26 + ' — same line, comparative', '30-Jun-2025', 'Company')
eps_h126      = reg('eps_h126', 0.799, FS26 + ' — basic earnings per share (note 71)', '30-Jun-2026', 'Company')
wavg_sh_h126  = reg('wavg_sh_h126', 2835.542374, FS26 + ' — note 71, weighted average shares (mn)', '30-Jun-2026', 'Company')
taxrate_stat  = reg('taxrate_stat', 0.225, FS26 + ' — note 70a, tax at 22.5%; Damodaran corporate tax rate for Egypt agrees', '30-Jun-2026', 'Country')

# --- revenue and cost by activity (notes 64, 65) ---
rev_re_h126   = reg('rev_re_h126', 17546.530343, FS26 + ' — note 64, net revenue from real estate development', '30-Jun-2026', 'Company')
rev_re_h125   = reg('rev_re_h125', 13857.584500, FS26 + ' — note 64, comparative', '30-Jun-2025', 'Company')
rev_com_h126  = reg('rev_com_h126', 767.493219, FS26 + ' — note 64, commercial and service activities', '30-Jun-2026', 'Company')
rev_com_h125  = reg('rev_com_h125', 286.777627, FS26 + ' — note 64, comparative', '30-Jun-2025', 'Company')
rev_hot_h126  = reg('rev_hot_h126', 128.142748, FS26 + " — note 64, owners' share in the profits of operating the hotels", '30-Jun-2026', 'Company')
rev_clb_h126  = reg('rev_clb_h126', 384.671093, FS26 + ' — note 64, revenue from Palm Hills club', '30-Jun-2026', 'Company')
rev_oth_h126  = reg('rev_oth_h126', 701.280324, FS26 + ' — note 64, other activities revenues', '30-Jun-2026', 'Company')
rev_oth_h125  = reg('rev_oth_h125', 1035.066457, FS26 + ' — note 64, comparative', '30-Jun-2025', 'Company')
transfer_h126 = reg('transfer_h126', 547.790260, FS26 + ' — note 64, transfer fees and delay penalties', '30-Jun-2026', 'Company')
transfer_h125 = reg('transfer_h125', 315.590928, FS26 + ' — note 64, comparative', '30-Jun-2025', 'Company')
util_h126     = reg('util_h126', 6.734456, FS26 + ' — note 64, retrieve the value of the utilities', '30-Jun-2026', 'Company')
assoc_h126    = reg('assoc_h126', -146.755608, FS26 + ' — note 64, gain (loss) from associates', '30-Jun-2026', 'Company')
oneoff_h125   = reg('oneoff_h125', 661.104866, FS26 + ' — note 64 comparative, non-recurring items inside other activities '
                    'revenues: profits from selling investments 560.793232 + miscellaneous income 94.584186 + gain from '
                    'selling fixed asset 5.727448', '30-Jun-2025', 'Company')
cost_re_h126  = reg('cost_re_h126', 12132.982745, FS26 + ' — note 65, cost of real estate development', '30-Jun-2026', 'Company')
cost_re_h125  = reg('cost_re_h125', 8530.838611, FS26 + ' — note 65, comparative', '30-Jun-2025', 'Company')
cost_com_h126 = reg('cost_com_h126', 250.320947, FS26 + ' — note 65, cost of commercial and service activity', '30-Jun-2026', 'Company')
cost_clb_h126 = reg('cost_clb_h126', 121.687245, FS26 + ' — note 65, cost of Palm Hills club operation', '30-Jun-2026', 'Company')
dep_clb_h126  = reg('dep_clb_h126', 23.698214, FS26 + ' — note 65, depreciation of club assets', '30-Jun-2026', 'Company')
dep_mac_h126  = reg('dep_mac_h126', 10.583017, FS26 + ' — note 65, depreciation of fixed assets Macor', '30-Jun-2026', 'Company')
sal_h126      = reg('sal_h126', 678.331633, FS26 + ' — note 66, salaries and wages', '30-Jun-2026', 'Company')
sal_h125      = reg('sal_h125', 481.601977, FS26 + ' — note 66, comparative', '30-Jun-2025', 'Company')
adm_h126      = reg('adm_h126', 2167.519938, FS26 + ' — note 66, general administration and marketing expenses', '30-Jun-2026', 'Company')
adm_h125      = reg('adm_h125', 1724.569398, FS26 + ' — note 66, comparative', '30-Jun-2025', 'Company')

# --- work in progress: the physical construction-volume driver (note 43) ---
work_h126     = reg('work_h126', 11971.400377, FS26 + ' — note 43, work carried out for the six months ended 30-Jun-2026', '30-Jun-2026', 'Company')
work_fy25     = reg('work_fy25', 18014.533331, FS26 + ' — note 43, comparative column: work carried out during FY2025', '31-Dec-2025', 'Company')
wip_jun26     = reg('wip_jun26', 23915.930580, FS26 + ' — note 43, balance of work in progress', '30-Jun-2026', 'Company')
wip_dec25     = reg('wip_dec25', 17570.908880, FS26 + ' — note 43, comparative', '31-Dec-2025', 'Company')
cumwork_jun26 = reg('cumwork_jun26', 90896.730712, FS26 + ' — note 43, total works executed until 30-Jun-2026', '30-Jun-2026', 'Company')
cumwork_dec25 = reg('cumwork_dec25', 78925.330335, FS26 + ' — note 43, total works executed until 1-Jan-2026', '31-Dec-2025', 'Company')
cumrelief_jun26 = reg('cumrelief_jun26', 66980.800132, FS26 + ' — note 43, cumulative cost excluded from (i.e. taken to) the income statement to 30-Jun-2026', '30-Jun-2026', 'Company')
cumrelief_dec25 = reg('cumrelief_dec25', 61354.421455, FS26 + ' — note 43, comparative', '31-Dec-2025', 'Company')
wip_land_jun26  = reg('wip_land_jun26', 6049.870482, FS26 + ' — note 43, land acquisition cost inside work in progress', '30-Jun-2026', 'Company')
wip_constr_jun26= reg('wip_constr_jun26', 17866.060098, FS26 + ' — note 43, cost of construction and facilities inside work in progress', '30-Jun-2026', 'Company')
capint_h126     = reg('capint_h126', 1191.507762, FS26 + ' — note 43 footnote, interest on loans capitalised into works under implementation', '30-Jun-2026', 'Company')

# --- balance sheet, 30-Jun-2026 and 31-Dec-2025 ---
def bs(k, v26, v25, line):
    reg(k + '_jun26', v26, FS26 + ' — consolidated financial position: ' + line, '30-Jun-2026', 'Company')
    reg(k + '_dec25', v25, FS26 + ' — consolidated financial position, comparative: ' + line, '31-Dec-2025', 'Company')
    return v26, v25

assoc_inv_jun26, assoc_inv_dec25 = bs('assoc_inv', 3898.477847, 3611.619739, 'investments in associates')
invprop_jun26, invprop_dec25     = bs('invprop', 1008.419552, 1032.530185, 'investment property')
fa_jun26, fa_dec25               = bs('fa', 5637.373917, 4521.970936, 'fixed assets (net)')
cip_jun26, cip_dec25             = bs('cip', 203.215360, 182.616883, 'projects under construction')
nr_lt_jun26, nr_lt_dec25         = bs('nr_lt', 55707.502096, 54801.316199, 'notes receivable - long term')
nrund_lt_jun26, nrund_lt_dec25   = bs('nrund_lt', 1033.560158, 1518.490219, 'notes receivable - long term for undelivered units')
nca_jun26, nca_dec25             = bs('nca', 67800.794295, 65900.163274, 'total non-current assets')
ar_jun26, ar_dec25               = bs('ar', 35055.008362, 28118.116247, 'accounts receivable')
dr_jun26, dr_dec25               = bs('dr', 14932.335834, 12921.978854, 'debtors and other debit balances')
supadv_jun26, supadv_dec25       = bs('supadv', 10490.853035, 9056.244671, 'suppliers - advance payments')
duefrom_jun26, duefrom_dec25     = bs('duefrom', 346.267799, 335.661244, 'due from related parties')
tbill_jun26, tbill_dec25         = bs('tbill', 13016.407445, 9581.528351, 'financial investments at amortized cost')
fvtpl_jun26, fvtpl_dec25         = bs('fvtplbs', 179.503696, 152.706778, 'investments at fair value through profit and loss')
nr_st_jun26, nr_st_dec25         = bs('nr_st', 20530.518157, 18137.718924, 'notes receivable - short term')
nrund_st_jun26, nrund_st_dec25   = bs('nrund_st', 695.420618, 935.259476, 'notes receivable - short term for undelivered units')
cash_jun26, cash_dec25           = bs('cash', 7804.246906, 9419.526159, 'cash and cash equivalents')
ta_jun26, ta_dec25               = bs('ta', 194767.286727, 172129.812858, 'total assets')
eqctl_jun26, eqctl_dec25         = bs('eqctl', 18910.859404, 17431.419763, 'net controlling equities')
eqnci_jun26, eqnci_dec25         = bs('eqnci', 1723.048810, 1334.332140, 'non-controlling equities')
eqtot_jun26, eqtot_dec25         = bs('eqtot', 20633.908214, 18765.751903, "total shareholders' equity")
loan_lt_jun26, loan_lt_dec25     = bs('loan_lt', 10236.280237, 10543.120329, 'loans - long term')
np_lt_jun26, np_lt_dec25         = bs('np_lt', 4016.714644, 4505.024909, 'notes payable - long term')
landliab_lt_jun26, landliab_lt_dec25 = bs('landliab_lt', 47.134741, 0.0, 'land purchase liabilities - long term')
ra_jun26, ra_dec25               = bs('ra', 34337.384836, 29122.769947, "other long-term liabilities - Residents' Association")
lease_lt_jun26, lease_lt_dec25   = bs('lease_lt', 78.329645, 60.703816, 'lease contract liabilities - long term')
jsa_lt_jun26, jsa_lt_dec25       = bs('jsa_lt', 3530.990688, 3991.865312, 'joint shares arrangement - long term')
bank_cr_jun26, bank_cr_dec25     = bs('bank_cr', 1529.842495, 938.770898, 'banks - credit balances')
cf_jun26, cf_dec25               = bs('cf', 13922.422891, 11337.531976, 'credit facilities')
loan_st_jun26, loan_st_dec25     = bs('loan_st', 650.151650, 1250.040023, 'current portion of short-term loans')
np_st_jun26, np_st_dec25         = bs('np_st', 4778.461505, 4875.673642, 'notes payable - short term')
adv_jun26, adv_dec25             = bs('adv', 83483.291217, 69354.084075, 'advances from customers')
defrev_jun26, defrev_dec25       = bs('defrev', 250.565351, 731.229939, 'deferred revenue')
chkund_jun26, chkund_dec25       = bs('chkund', 1728.980776, 2453.749695, 'liabilities for checks for undelivered units')
lease_st_jun26, lease_st_dec25   = bs('lease_st', 63.263828, 41.916627, 'lease contract liabilities - short term')
landliab_st_jun26, landliab_st_dec25 = bs('landliab_st', 29.612533, 0.012225, 'current portion of land purchase liabilities')
jsa_st_jun26, jsa_st_dec25       = bs('jsa_st', 1831.705748, 2981.872912, 'joint shares arrangement - short term')
cred_jun26, cred_dec25           = bs('cred', 6608.427292, 5121.712447, 'creditors & other credit balances')
supcon_jun26, supcon_dec25       = bs('supcon', 5740.130394, 3807.042889, 'suppliers and contractors')
tl_jun26, tl_dec25               = bs('tl', 174133.378513, 153364.060955, 'total liabilities')

# --- notes: debt, capital, backlog, restricted balances ---
intdebt_jun26 = reg('intdebt_jun26', 26480.290746, FS26 + ' — note 34 (A/1) interest-rate risk: the company\'s own schedule of '
                    'interest-bearing financial obligations = credit facilities 13,922.423 + loans 10,886.432 + credit banks '
                    '1,529.842 + lease obligations 141.593', '30-Jun-2026', 'Company')
rate_sens_2pc = reg('rate_sens_2pc', 428.0, FS26 + ' — note 34 (A/1): a 2% move in interest rates moves profit or loss by '
                    'approximately EGP 428mn, implying about EGP 21.4bn of floating-rate exposure', '30-Jun-2026', 'Company')
fx_net_asset  = reg('fx_net_asset', 2448.354068, FS26 + ' — note 34 (A/2): net foreign-currency balance is an ASSET', '30-Jun-2026', 'Company')
cash_fx_jun26 = reg('cash_fx_jun26', 2569.233390, FS26 + ' — note 48: banks current accounts foreign currency 524.696277 + '
                    'banks deposits foreign currency 2,044.537113', '30-Jun-2026', 'Company')
bankcr_fx     = reg('bankcr_fx', 120.879322, FS26 + ' — note 49: banks credit balances denominated in foreign currency', '30-Jun-2026', 'Company')
tbill_face    = reg('tbill_face', 15475.517000, FS26 + ' — note 47: face value of treasury bills and bonds held', '30-Jun-2026', 'Company')
tbill_wavg_yld= reg('tbill_wavg_yld', 0.191033, FS26 + ' — note 47: face-value-weighted average return rate across the thirteen '
                    'holding entities (range 18.41%-19.33%)', '30-Jun-2026', 'Company')
sh_issued     = reg('sh_issued', 2859.914173, FS26 + ' — note 60: 2,859,914,173 shares of EGP 2 nominal', '30-Jun-2026', 'Company')
sh_treasury   = reg('sh_treasury', 35.444009, FS26 + ' — note 62: treasury shares at cost, 35,444,009 shares', '30-Jun-2026', 'Company')
sh_out        = reg('sh_out', 2824.470164, FS26 + ' — note 62: outstanding shares after treasury', '30-Jun-2026', 'Company')
treas_cost    = reg('treas_cost', 327.006688, FS26 + ' — note 62: treasury shares at cost', '30-Jun-2026', 'Company')
treas_buy_h126= reg('treas_buy_h126', 225.914581, FS26 + ' — note 62: 23,510,000 shares bought in H1-2026 at an average EGP 9.61', '30-Jun-2026', 'Company')
divs_h126     = reg('divs_h126', 686.092048, FS26 + ' — consolidated statement of cash flows, paid dividends', '30-Jun-2026', 'Company')
bk_contract   = reg('bk_contract', 149117.775260, FS26 + ' — note 72: contractual value to customers of undelivered-unit contracts '
                    'concluded between 1-Jan-2023 and 30-Jun-2026', '30-Jun-2026', 'Company')
bk_nominal    = reg('bk_nominal', 116540.071448, FS26 + ' — note 72: nominal value of the notes receivable behind those contracts, '
                    'not included in the financial statements', '30-Jun-2026', 'Company')
bk_pv         = reg('bk_pv', 59398.327684, FS26 + ' — note 72: present value of those checks', '30-Jun-2026', 'Company')
bk_ladder     = reg('bk_ladder', [7958.454203, 15904.031545, 16250.343221, 16319.819309, 60107.423170],
                    FS26 + ' — note 72 maturity ladder, nominal: due 2026 / 2027 / 2028 / 2029 / 2030 and later', '30-Jun-2026', 'Company')
bk_ladder_pv  = reg('bk_ladder_pv', [7484.721565, 12896.813973, 10798.764729, 8879.312355, 19338.715062],
                    FS26 + ' — note 72 maturity ladder, net present value', '30-Jun-2026', 'Company')
maint_nr      = reg('maint_nr', 15014.0, FS26 + ' — note 41 footnote: notes receivable include about EGP 15.014bn of checks '
                    "received for maintenance deposits whose collected value reverts to the Workers' Union on its establishment",
                    '30-Jun-2026', 'Company')
nr_gross_jun26= reg('nr_gross_jun26', 99653.637505, FS26 + ' — note 41: short-term notes receivable 25,282.558061 + long-term '
                    '74,371.079444, before present-value discount and partners\' share', '30-Jun-2026', 'Company')
nr_partner    = reg('nr_partner', 20411.319258, FS26 + " — note 41: share of the partners deducted from notes receivable", '30-Jun-2026', 'Company')

# --- cash-flow statement, H1-2026 (and H1-2025 comparative) ---
ocf_h126      = reg('ocf_h126', 1499.068217, FS26 + ' — net cash provided by operating activities', '30-Jun-2026', 'Company')
ocf_h125      = reg('ocf_h125', 494.411464, FS26 + ' — comparative', '30-Jun-2025', 'Company')
d_ra_h126     = reg('d_ra_h126', 5214.614889, FS26 + " — cash-flow statement, change in long-term liabilities Residents' Association", '30-Jun-2026', 'Company')
d_ra_h125     = reg('d_ra_h125', 6086.710848, FS26 + ' — comparative', '30-Jun-2025', 'Company')
capex_h126    = reg('capex_h126', 311.773236, FS26 + ' — payments for purchase of fixed assets', '30-Jun-2026', 'Company')
capex_cip_h126= reg('capex_cip_h126', 20.598477, FS26 + ' — payments for projects under construction', '30-Jun-2026', 'Company')
da_cf_h126    = reg('da_cf_h126', 279.178909, FS26 + ' — cash-flow statement, depreciation & amortization', '30-Jun-2026', 'Company')
taxpaid_h126  = reg('taxpaid_h126', 1834.206566, FS26 + ' — income taxes paid', '30-Jun-2026', 'Company')

# --- FY2024 audited, with FY2023 comparatives ---
rev_fy24      = reg('rev_fy24', 27167.304497, FS24 + ' — consolidated statement of income, revenues', '31-Dec-2024', 'Company')
rev_fy23      = reg('rev_fy23', 17462.108314, FS24 + ' — comparative', '31-Dec-2023', 'Company')
cogs_fy24     = reg('cogs_fy24', 17739.913618, FS24 + ' — cost of revenues', '31-Dec-2024', 'Company')
cogs_fy23     = reg('cogs_fy23', 11907.224490, FS24 + ' — comparative', '31-Dec-2023', 'Company')
gp_fy24       = reg('gp_fy24', 9330.096386, FS24 + ' — gross profit', '31-Dec-2024', 'Company')
gp_fy23       = reg('gp_fy23', 5507.635295, FS24 + ' — comparative', '31-Dec-2023', 'Company')
sga_fy24      = reg('sga_fy24', 3435.754971, FS24 + ' — general administrative, selling and marketing expenses', '31-Dec-2024', 'Company')
sga_fy23      = reg('sga_fy23', 2060.461700, FS24 + ' — comparative', '31-Dec-2023', 'Company')
ecl_fy24      = reg('ecl_fy24', 23.478620, FS24 + ' — expected credit losses', '31-Dec-2024', 'Company')
ecl_fy23      = reg('ecl_fy23', 14.104054, FS24 + ' — comparative', '31-Dec-2023', 'Company')
fin_fy24      = reg('fin_fy24', 2311.395503, FS24 + ' — finance costs & interests', '31-Dec-2024', 'Company')
pbt_fy24      = reg('pbt_fy24', 4320.598449, FS24 + ' — net profit before income tax & non-controlling equities', '31-Dec-2024', 'Company')
pbt_fy23      = reg('pbt_fy23', 2300.703847, FS24 + ' — comparative', '31-Dec-2023', 'Company')
np_fy24       = reg('np_fy24', 3254.945443, FS24 + ' — net profit after income tax & non-controlling equities', '31-Dec-2024', 'Company')
np_fy23       = reg('np_fy23', 1581.511689, FS24 + ' — comparative', '31-Dec-2023', 'Company')
da_fy24       = reg('da_fy24', 270.108689, FS24 + ' — cash-flow statement, depreciation & amortization', '31-Dec-2024', 'Company')
ocf_fy24      = reg('ocf_fy24', 3084.378488, FS24 + ' — net cash from operating activities', '31-Dec-2024', 'Company')
ocf_fy23      = reg('ocf_fy23', 753.224012, FS24 + ' — comparative', '31-Dec-2023', 'Company')
d_ra_fy24     = reg('d_ra_fy24', 10047.698341, FS24 + " — change in long-term liabilities Residents' Association", '31-Dec-2024', 'Company')
d_ra_fy23     = reg('d_ra_fy23', 3777.492521, FS24 + ' — comparative', '31-Dec-2023', 'Company')
rev_fy22_ir   = reg('rev_fy22_ir', 13600.0, IR9M25 + ' — revenue history chart, FY2022 (COMPANY_IR). The audited FY2022 '
                    'statements are not published, so the only company-issued FY2022 revenue is this chart. It is used for '
                    'ONE purpose — the FY2023 revenue increment behind the float ratio — and never as a statement line',
                    '13-Nov-2025', 'Company')
capex_fy24    = reg('capex_fy24', 587.649309, FS24 + ' — payments for purchase of fixed assets', '31-Dec-2024', 'Company')
np_fy25       = reg('np_fy25', 4216.657655, FS26 + ' — consolidated statement of changes in equity: net profit for the year 2025 '
                    'attributable to equity holders of the parent', '31-Dec-2025', 'Company')

# --- company-published series not repeated in any obtained statement (COMPANY_IR) ---
rev_fy25_ir   = reg('rev_fy25_ir', 36196.0, IR1Q26 + ' — revenue history chart, FY2025', '20-May-2026', 'Company')
ebitda_fy25_ir= reg('ebitda_fy25_ir', 8552.0, IR1Q26 + ' — EBITDA history chart, FY2025', '20-May-2026', 'Company')
np_fy25_ir    = reg('np_fy25_ir', 4268.0, IR1Q26 + ' — net-profit history chart, FY2025 (differs by EGP 51mn from the audited '
                    'equity statement; the statement figure governs)', '20-May-2026', 'Company')
rev_9m25      = reg('rev_9m25', 25549.0, IR9M25 + ' — financial review table', '13-Nov-2025', 'Company')
gp_9m25       = reg('gp_9m25', 10423.0, IR9M25 + ' — financial review table', '13-Nov-2025', 'Company')
ebitda_9m25   = reg('ebitda_9m25', 6690.0, IR9M25 + ' — financial review table', '13-Nov-2025', 'Company')
constr_9m25   = reg('constr_9m25', 10500.0, IR9M25 + ' — construction spending, up 71% year on year', '13-Nov-2025', 'Company')
constr_1h25   = reg('constr_1h25', 6400.0, IR1H25 + ' — construction spending, up 55% year on year', '13-Aug-2025', 'Company')
constr_1q26   = reg('constr_1q26', 4600.0, IR1Q26 + ' — construction spending in 1Q2026, up 60% year on year', '20-May-2026', 'Company')
coll_1h25     = reg('coll_1h25', 16600.0, IR1H25 + ' — cash collection from receivables and new sales', '13-Aug-2025', 'Company')
units_fy26    = reg('units_fy26', 1200.0, IR1Q26 + ' — contractual units ready to be handed over in FY2026', '20-May-2026', 'Company')
sales_1q26    = reg('sales_1q26', 52059.0, IR1Q26 + ' — new sales, all regions', '20-May-2026', 'Company')
sales_1h25    = reg('sales_1h25', 143000.0, IR1H25 + ' — new sales in 1H2025', '13-Aug-2025', 'Company')
sales_9m25    = reg('sales_9m25', 182000.0, IR9M25 + ' — new sales in 9M2025', '13-Nov-2025', 'Company')
sales_fy25    = reg('sales_fy25', 215384.0, IR1Q26 + ' — new sales history chart, FY2025', '20-May-2026', 'Company')
backlog_1q26  = reg('backlog_1q26', 263000.0, IR1Q26 + ' — backlog of units sold and not yet delivered', '20-May-2026', 'Company')
backlog_9m25  = reg('backlog_9m25', 225000.0, IR9M25 + ' — backlog', '13-Nov-2025', 'Company')
netdebt_1q26  = reg('netdebt_1q26', 3300.0, IR1Q26 + " — the company's own net-debt figure at 31-Mar-2026", '20-May-2026', 'Company')
netdebt_9m25  = reg('netdebt_9m25', 4200.0, IR9M25 + " — the company's own net-debt figure at 30-Sep-2025", '13-Nov-2025', 'Company')
landbank_sqm  = reg('landbank_sqm', 46.0, IR1Q26 + ' — land bank of 46 million square metres across Egypt and Abu Dhabi', '20-May-2026', 'Company')

# --- industry ring (secondary, flagged) ---
mkt_h126      = reg('mkt_h126', 670000.0, IND + ' — combined H1-2026 sales of the ten largest Egyptian developers', '18-Aug-2026', 'Industry')
mkt_h125      = reg('mkt_h125', 651000.0, IND + ' — same measure, H1-2025', '18-Aug-2026', 'Industry')
mkt_units_chg = reg('mkt_units_chg', -0.05, IND + ' — units sold about 39,000 in H1-2026, down 5% year on year', '18-Aug-2026', 'Industry')
phdc_sales_h126 = reg('phdc_sales_h126', 94000.0, IND + ' — Palm Hills ranked second with H1-2026 sales of EGP 94bn. NOT '
                      'obtainable from the company\'s own channel: the 1H2026 earnings release was not published on '
                      'palmhillsdevelopments.com or its content API as of 19-Aug-2026. Carried as SECONDARY-UNVERIFIED; it '
                      'is used for narrative and cross-check only and no model driver reads it', '18-Aug-2026', 'Industry')
reh_launch    = reg('reh_launch', 75000.0, 'Press reporting of the 1H2026 results release: Hacienda Ras El Hekma recorded '
                    'EGP 75bn of sales in the first two weeks of launch to the close of 17-Aug-2026, to be booked in Q3-2026. '
                    'SECONDARY-UNVERIFIED for the same reason; narrative and catalyst only', '18-Aug-2026', 'Industry')
backlog_h126_press = reg('backlog_h126_press', 284000.0, 'Press reporting of the 1H2026 results release: record backlog of '
                         'EGP 284bn, up 40% year on year. SECONDARY-UNVERIFIED; the study anchors on note 72 instead',
                         '18-Aug-2026', 'Industry')

# --- country ring ---
rf_obs        = reg('rf_obs', 0.23269, CBE_B + ' — three-year bond, accepted weighted-average yield 23.269% (22 accepted bids, '
                    'EGP 18.881bn accepted of EGP 39.684bn submitted: the deepest accepted print in the auction). The two-year '
                    'cleared at 22.691% on a single accepted bid and the five-year at 19.700% on a single accepted bid; neither '
                    'is a usable clearing level', '17-Aug-2026', 'Country')
tbill_1y      = reg('tbill_1y', 0.24950, CBE_T + ' — 364-day bill, accepted weighted-average yield', '13-Aug-2026', 'Country')
tbill_91      = reg('tbill_91', 0.24191, CBE_T + ' — 91-day bill, accepted weighted-average yield', '16-Aug-2026', 'Country')
rf_arcc_xchk  = reg('rf_arcc_xchk', 0.2295, 'Egypt ten-year local-currency government bond yield adopted in the ARCC valuation '
                    'study of 06-Aug-2026 (engine/arcc_study input rf) — independent cross-check on the CBE auction print',
                    '06-Aug-2026', 'Country')
ds_rating     = reg('ds_rating', 0.05970183, DAMO + ' — rating-based adjusted default spread, Moody\'s Caa1', '30-Jun-2026', 'Country')
erp_rating    = reg('erp_rating', 0.13480623, DAMO + ' — total equity risk premium, rating basis', '30-Jun-2026', 'Country')
crp_rating    = reg('crp_rating', 0.09280623, DAMO + ' — country risk premium, rating basis', '30-Jun-2026', 'Country')
ds_cds        = reg('ds_cds', 0.03420, DAMO + ' — sovereign CDS net of Swiss CDS (gross 3.55%)', '30-Jun-2026', 'Country')
erp_cds       = reg('erp_cds', 0.09516375, DAMO + ' — total equity risk premium, CDS basis', '30-Jun-2026', 'Country')
damo_jan_ds   = reg('damo_jan_ds', 0.06372478, 'Damodaran ctryprem.html, last updated 5-Jan-2026, Egypt row — prior vintage '
                    'carried for comparison only', '05-Jan-2026', 'Country')
damo_jan_erp  = reg('damo_jan_erp', 0.13937694, 'Damodaran ctryprem.html, 5-Jan-2026, Egypt total ERP, rating basis', '05-Jan-2026', 'Country')
cbe_deposit   = reg('cbe_deposit', 0.19, MPC, '09-Jul-2026', 'Country')
cbe_lending   = reg('cbe_lending', 0.20, MPC + ' — overnight lending rate, one percentage point above the deposit rate', '09-Jul-2026', 'Country')
cpi_urban     = reg('cpi_urban', 0.149, CPI, '10-Aug-2026', 'Country')
cpi_core      = reg('cpi_core', 0.147, CPI, '10-Aug-2026', 'Country')
usdegp        = reg('usdegp', 50.52, FX, '19-Aug-2026', 'Country')
rf_term       = reg('rf_term', 0.105, 'Terminal risk-free rate, normalised from the Central Bank of Egypt\'s longest published '
                    'inflation target (5% for Q4-2028) plus a standard emerging-market real-rate convention. Same construction '
                    'and same value as the ARCC study of 06-Aug-2026 (input rf_term) — the house prior for Egypt',
                    '06-Aug-2026', 'Country')
erp_term      = reg('erp_term', 0.070, 'Terminal equity risk premium, normalised below the currently elevated Egypt level. '
                    'Same value and construction as the ARCC study of 06-Aug-2026 (input erp_term)', '06-Aug-2026', 'Country')

# --- beta (produced by the sanctioned resolver; the record is asserted below) ---
beta_val      = reg('beta_val', 1.0555271328180147, BETA + ' — Dimson-adjusted weekly beta, 255 observations over 4.93 years '
                    'to 16-Jul-2026, R-squared 29.8%, standard error 0.182, passes the usability gate', '22-Jul-2026', 'Market')
beta_r2       = reg('beta_r2', 0.2976393808522475, BETA + ' — regression R-squared', '22-Jul-2026', 'Market')
beta_se       = reg('beta_se', 0.18164085825269616, BETA + ' — standard error of the beta estimate', '22-Jul-2026', 'Market')
beta_n        = reg('beta_n', 255, BETA + ' — weekly observations on the exchange trading week (Sunday-Thursday, W-THU grid)', '22-Jul-2026', 'Market')
beta_blume    = reg('beta_blume', 1.037018088545343, BETA + ' — Blume-adjusted cross-check', '22-Jul-2026', 'Market')

# --- market ---
spot          = reg('spot', 15.01, PAGE + ' — published spot, close of 22-Jul-2026. This refresh does not touch it', '22-Jul-2026', 'Market')
wk52_hi       = reg('wk52_hi', 16.43, PAGE + ' — published 52-week high inside the carried-forward technical read', '22-Jul-2026', 'Market')
wk52_lo       = reg('wk52_lo', 6.99, PAGE + ' — published 52-week low inside the carried-forward technical read', '22-Jul-2026', 'Market')

# --- forecast drivers (Company ring where measured, flagged where estimated) ---
vol_growth    = reg('vol_growth', [0.12, 0.09, 0.06, 0.04, 0.03],
                    'Real construction-volume growth for FY2027 to FY2031. Anchored on measured execution: work carried out '
                    'annualises to EGP 23,943mn in 2026 against EGP 18,015mn in FY2025 (+32.9% nominal, about +18.7% real at '
                    'the measured cost path), and the company reported construction spending up 60% year on year in 1Q2026 and '
                    'up 71% in 9M2025. The path decelerates because the constraint is execution and working capital, not '
                    'demand: the undelivered contracted book of EGP 149.1bn (note 72) covers roughly two years of build at the '
                    '2026 rate. ESTIMATED PATH, recorded as such', '19-Aug-2026', 'Company')
pi_price      = reg('pi_price', [0.090, 0.080, 0.075, 0.070, 0.065],
                    'Selling-price escalation for FY2027 to FY2031. The FY2026 anchor is measured, not assumed: the ten largest '
                    'Egyptian developers sold EGP 670bn in H1-2026 against EGP 651bn a year earlier (+2.9%) on about 39,000 '
                    'units, down 5% — an implied average-ticket rise of 8.3%. Later years track nominal household income on the '
                    'central bank disinflation path', '18-Aug-2026', 'Company')
cost_w        = reg('cost_w', [0.25, 0.20, 0.25, 0.30],
                    'Weights of the four physically distinct construction cost classes — reinforcing steel, cement and concrete, '
                    'finishing and other materials, site labour and overhead. ESTIMATED from the structure of Egyptian '
                    'residential build costs; the filings do not disclose a cost-by-nature split of construction. Recorded '
                    'as an estimate and carried through the sensitivity', '19-Aug-2026', 'Industry')
esc_steel     = reg('esc_steel', [0.060, 0.060, 0.055, 0.050, 0.045],
                    'Reinforcing-steel escalator. Near-term anchor is dated and measured: Egyptian producers left August 2026 '
                    'rebar sales prices unchanged against July after earlier declines, so FY2026 carries no steel escalation at '
                    'all; from FY2027 the path is global steel plus the pound\'s drift', '19-Aug-2026', 'Industry')
esc_cement    = reg('esc_cement', [0.090, 0.080, 0.070, 0.065, 0.060],
                    'Cement and concrete escalator, taken from the Egyptian local realised cement price path adopted in the ARCC '
                    'study of 06-Aug-2026, which is anchored on a disclosed producer price history', '06-Aug-2026', 'Industry')
esc_finish    = reg('esc_finish', [0.115, 0.100, 0.090, 0.080, 0.070],
                    'Finishing and other materials escalator, on the central bank disinflation path from the measured July 2026 '
                    'urban rate of 14.9% toward the 5% target for Q4-2028', '10-Aug-2026', 'Country')
esc_labour    = reg('esc_labour', [0.135, 0.120, 0.110, 0.100, 0.090],
                    'Site labour and overhead escalator: the consumer-price path plus two percentage points. Conservative '
                    'against the measured direction — the company\'s own salaries and wages rose 40.9% year on year in H1-2026 '
                    'against revenue growth of 25.4%', '30-Jun-2026', 'Company')
hcount_growth = reg('hcount_growth', 0.02, 'Real headcount growth carried in the salary line on top of wage escalation',
                    '19-Aug-2026', 'Company')
term_g        = reg('term_g', 0.080, 'Terminal nominal growth: the central bank\'s 5% long-run inflation target plus about 3% '
                    'real. Held below the terminal weighted cost of capital under both cost-of-capital framings and made '
                    'reinvestment-consistent through the return on capital the model itself computes', '19-Aug-2026', 'Country')
maint_share   = reg('maint_share', 0.437, 'Share of the Residents\' Association balance represented by maintenance-deposit '
                    'checks rather than collected cash: EGP 15.014bn of notes receivable (note 41 footnote) against the '
                    'EGP 34.337bn liability (note 63). Disclosed as stocks, not as period movements', '30-Jun-2026', 'Company')
# The three incremental float ratios, computed from the registered movements and revenues
# so the justification text below quotes computed numbers rather than typed ones.
_ra_i23 = d_ra_fy23 / (rev_fy23 - rev_fy22_ir)
_ra_i24 = d_ra_fy24 / (rev_fy24 - rev_fy23)
_ra_i26 = d_ra_h126 / (rev_h126 - rev_h125)
ra_target_ratio = reg('ra_target_ratio', 1.00, "Steady-state Residents' Association balance per Egyptian pound of annual "
                    'revenue. Not asserted: solved from the company\'s own disclosed movements. Per pound of revenue '
                    'growth the balance rose %.2fx in FY2023 (EGP %.0fmn on EGP %.0fmn), %.2fx in FY2024 (EGP %.0fmn on '
                    'EGP %.0fmn) and %.2fx in H1-2026 on a like-for-like basis (EGP %.0fmn on EGP %.0fmn). The study carries '
                    'the bottom of that measured incremental range, which lets the balance keep building toward 1.0x annual '
                    'revenue and then hold there — a bounded float rather than an unbounded one'
                    % (_ra_i23, d_ra_fy23, rev_fy23 - rev_fy22_ir, _ra_i24, d_ra_fy24, rev_fy24 - rev_fy23,
                       _ra_i26, d_ra_h126, rev_h126 - rev_h125), '30-Jun-2026', 'Company')

# --- peers (aggregator, cross-check only) ---
peers = reg('peers', [
    dict(name='Talaat Moustafa Group Holding', ticker='EGX:TMGH', country='Egypt', pe=10.2, mcap=156630.0, earnings=15410.0),
    dict(name='Emaar Misr for Development',    ticker='EGX:EMFD', country='Egypt', pe=6.1,  mcap=54600.0,  earnings=None),
    dict(name='SODIC',                          ticker='EGX:OCDI', country='Egypt', pe=6.1,  mcap=24100.0,  earnings=None),
    dict(name='Heliopolis Housing',             ticker='EGX:HELI', country='Egypt', pe=7.5,  mcap=22670.0,  earnings=None),
    dict(name='Madinet Masr',                   ticker='EGX:MASR', country='Egypt', pe=None, mcap=16500.0,  earnings=None),
    dict(name='Emaar Properties',               ticker='DFM:EMAAR', country='United Arab Emirates', pe=6.5, mcap=None, earnings=None, ev_ebitda=3.6, ev_rev=1.7),
    dict(name='Aldar Properties',               ticker='ADX:ALDAR', country='United Arab Emirates', pe=7.7, mcap=None, earnings=None, ev_ebitda=6.6, ev_rev=2.0),
], PEER, '11-Aug-2026', 'Industry')

# --- prior edition, for the scoring table ---
PR = {}
def pr(k, v, line):
    PR[k] = v
    INP['prior_' + k] = I(v, PRIOR + ' — ' + line, '11-Jun-2026', 'Prior study')
    return v
pr('fair_base', 15.894, 'Valuation sheet cell D38, risk-adjusted equity value per share')
pr('fair_bear', 7.62, 'stated bear case, contracted plus existing compounds only')
pr('fair_full', 24.921, 'Valuation sheet cell B38, full-execution equity value per share')
pr('rev_fy26', 50.042e3, 'Income Statement sheet, FY2026 revenue, EGP bn 50.042')
pr('gm_fy26', 0.4156, 'Income Statement sheet, FY2026 gross margin')
pr('ebitda_fy26', 13.874e3, 'Income Statement sheet, FY2026 EBITDA')
pr('ni_fy26', 6.373e3, 'Income Statement sheet, FY2026 net income')
pr('capex_fy26', 0.250e3, 'Cash Flow sheet, FY2026 capex')
pr('netdebt', 12.0e3, 'Assumptions sheet cell B5, net debt EGP 12bn (gross 30 less cash 18)')
pr('wacc', 0.18, 'Assumptions sheet cell B10, WACC nominal EGP')
pr('kd', 0.18, 'Assumptions sheet cell B12, cost of debt')
pr('shares', 2859.9, 'Assumptions sheet cell B4, shares outstanding 2.8599bn (issued, before treasury)')
pr('escalation', 0.14, 'Assumptions sheet cell B13, sales-price escalation per year')
pr('term_g', 0.05, 'Assumptions sheet cell B21, terminal growth')
pr('backlog', 263.0e3, 'stated backlog EGP 263bn')
pr('constr_runrate', 17.0e3, 'stated construction pacing of about EGP 14-20bn per year')
pr('roe', 0.269, 'stated ROE 26.9%')
pr('ps', 0.92, 'stated price to sales 0.92x')
pr('ev_ebitda', 8.1, 'stated EV/EBITDA about 8.1x')
pr('pe', 10.3, 'stated P/E about 10.3x')
pr('debt_equity', 1.58, 'stated debt to equity about 158%')

# ============================ DERIVED HISTORY ================================
H = {}
H['rev_h126'], H['rev_h125'] = rev_h126, rev_h125
H['gm_h126'] = gp_h126 / rev_h126
H['gm_h125'] = gp_h125 / rev_h125
H['gm_fy24'] = gp_fy24 / rev_fy24
H['gm_fy23'] = gp_fy23 / rev_fy23

# EBITDA on the company's own definition, recovered from the statements and tested where
# a test is actually available (the "recover the joint and test it" rule).
def ebitda(gp, sga, ecl):
    return gp - sga - ecl
H['ebitda_h126'] = ebitda(gp_h126, sga_h126, ecl_h126)
H['ebitda_h125'] = ebitda(gp_h125, sga_h125, ecl_h125)
H['ebitda_fy24'] = ebitda(gp_fy24, sga_fy24, ecl_fy24)
H['ebitda_fy23'] = ebitda(gp_fy23, sga_fy23, ecl_fy23)
# The definition is TESTED, not asserted. The company publishes an EBITDA figure for
# H1-2025, 9M2025, FY2025 and 1Q2026; of those, H1-2025 is the ONLY period for which the
# statements also disclose the components (gross profit, administrative and selling cost,
# expected credit losses), so it is the only genuine test. FY2025 and 9M2025 have no
# published statements at all, and 1Q2026's figure is an INPUT here, not a check.
ebitda_h125_pub = reg('ebitda_h125_pub', 4458.517, IR1H25 + ' — consolidated income statement, EBITDA '
                      '(EGP 4,458,517 thousand)', '13-Aug-2025', 'Company')
H['ebitda_def_gap_h125'] = H['ebitda_h125'] / ebitda_h125_pub - 1.0
H['ebitda_def_tested_periods'] = 1
H['ebitda_margin_h126'] = H['ebitda_h126'] / rev_h126
H['ebitda_margin_h125'] = H['ebitda_h125'] / rev_h125
H['ebitda_margin_fy24'] = H['ebitda_fy24'] / rev_fy24
H['ebitda_margin_fy23'] = H['ebitda_fy23'] / rev_fy23

# Q4-2025 and Q2-2026, by difference from the published cumulative periods
H['rev_q425'] = rev_fy25_ir - rev_9m25
H['ebitda_q425'] = ebitda_fy25_ir - ebitda_9m25
H['ebitda_margin_q425'] = H['ebitda_q425'] / H['rev_q425']
H['ebitda_margin_9m25'] = ebitda_9m25 / rev_9m25
H['ebitda_q226'] = H['ebitda_h126'] - (3309.973 - 0.0)  # placeholder replaced below
H['ebitda_1q26'] = 1915.527   # published in the 1Q2026 release financial review table
INP['ebitda_1q26'] = I(1915.527, IR1Q26 + ' — financial review table, EBITDA', '20-May-2026', 'Company')
H['ebitda_q226'] = H['ebitda_h126'] - H['ebitda_1q26']
H['rev_1q26'] = 9346.133
INP['rev_1q26'] = I(9346.133, IR1Q26 + ' — consolidated income statement, revenue', '20-May-2026', 'Company')
H['ebitda_margin_q226'] = H['ebitda_q226'] / rev_q226
H['ebitda_margin_1q26'] = H['ebitda_1q26'] / H['rev_1q26']

# H1-2025 stripped of the non-recurring items sitting inside other-activities revenue
H['rev_h125_adj'] = rev_h125 - oneoff_h125
H['gp_h125_adj'] = gp_h125 - oneoff_h125
H['gm_h125_adj'] = H['gp_h125_adj'] / H['rev_h125_adj']

# Operating cash flow with and without the Residents' Association float
# The float ratios the target is solved from, computed here rather than typed into prose:
# each disclosed movement in the association balance over the revenue growth that earned it.
H['ra_incr_fy23'], H['ra_incr_fy24'], H['ra_incr_h126'] = _ra_i23, _ra_i24, _ra_i26
H['ocf_ex_ra_h126'] = ocf_h126 - d_ra_h126
H['ocf_ex_ra_h125'] = ocf_h125 - d_ra_h125
H['ocf_ex_ra_fy24'] = ocf_fy24 - d_ra_fy24
H['ocf_ex_ra_fy23'] = ocf_fy23 - d_ra_fy23

# The two cost blocks inside the cost of real estate development
H['constr_relief_h126'] = cumrelief_jun26 - cumrelief_dec25
H['land_partner_h126'] = cost_re_h126 - H['constr_relief_h126']
H['c1'] = H['constr_relief_h126'] / rev_re_h126          # construction relieved, per EGP of RE revenue
H['c2'] = H['land_partner_h126'] / rev_re_h126           # land and partners' share, per EGP of RE revenue
H['re_gm_h126'] = 1.0 - H['c1'] - H['c2']
H['re_gm_h125'] = 1.0 - cost_re_h125 / rev_re_h125
H['P_h126'] = rev_re_h126 / H['constr_relief_h126']      # THE CRUX: revenue per EGP of build cost relieved
H['rho_h126'] = rev_re_h126 / work_h126                  # revenue per EGP of work executed
H['wip_years'] = wip_jun26 / (H['constr_relief_h126'] * 2.0)

# Bounding the unidentified split of the H1-2025 to H1-2026 margin fall
H['margin_fall_pp'] = H['re_gm_h125'] - H['re_gm_h126']
H['P_h125_if_c2_flat'] = 1.0 / (1.0 - H['re_gm_h125'] - H['c2'])
H['c2_h125_if_P_flat'] = 1.0 - H['re_gm_h125'] - 1.0 / H['P_h126']
H['P_compression_bound'] = H['P_h126'] / H['P_h125_if_c2_flat'] - 1.0
H['c2_rise_bound'] = H['c2'] - H['c2_h125_if_P_flat']

# Interest, capitalisation and the realised cost of debt
H['interest_total_h126'] = bank_int_h126 + capint_h126
H['cap_ratio'] = capint_h126 / H['interest_total_h126']
H['intdebt_dec25'] = (cf_dec25 + loan_st_dec25 + loan_lt_dec25 + bank_cr_dec25
                      + lease_st_dec25 + lease_lt_dec25)
H['intdebt_avg'] = (intdebt_jun26 + H['intdebt_dec25']) / 2.0
H['kd_realised'] = H['interest_total_h126'] / H['intdebt_avg'] * 2.0
H['corp_spread'] = H['kd_realised'] - tbill_wavg_yld

# Debt-like obligations, both framings
H['np_total_jun26'] = np_st_jun26 + np_lt_jun26
H['landliab_total_jun26'] = landliab_st_jun26 + landliab_lt_jun26
H['debt_narrow'] = intdebt_jun26
H['debt_broad'] = intdebt_jun26 + H['np_total_jun26'] + H['landliab_total_jun26']
H['liquid'] = cash_jun26 + tbill_jun26
H['netdebt_company'] = H['debt_narrow'] - H['liquid']
H['netdebt_broad'] = H['debt_broad'] - H['liquid']
H['ra_dedicated_assets'] = ra_jun26 - maint_nr
H['liquid_free'] = H['liquid'] - H['ra_dedicated_assets']
H['netdebt_restricted'] = H['debt_narrow'] - max(H['liquid_free'], 0.0)

# Working-capital ratios, measured at 30-Jun-2026 on annualised H1-2026 flows
H['rev_ann'] = rev_h126 * 2.0
H['cogs_ann'] = cogs_h126 * 2.0
H['relief_ann'] = H['constr_relief_h126'] * 2.0
H['recv_total_jun26'] = ar_jun26 + nr_st_jun26 + nr_lt_jun26 + nrund_st_jun26 + nrund_lt_jun26
H['recv_total_dec25'] = ar_dec25 + nr_st_dec25 + nr_lt_dec25 + nrund_st_dec25 + nrund_lt_dec25
H['dso'] = H['recv_total_jun26'] / H['rev_ann'] * 365.0
H['dio'] = wip_jun26 / H['cogs_ann'] * 365.0
H['dpo'] = (supcon_jun26 + H['np_total_jun26']) / H['cogs_ann'] * 365.0
H['ccc_gross'] = H['dso'] + H['dio'] - H['dpo']
H['adv_days'] = adv_jun26 / H['cogs_ann'] * 365.0
H['ccc_net'] = H['ccc_gross'] - H['adv_days']

# Per-share and market ratios
H['mktcap'] = spot * sh_out
H['bvps'] = eqctl_jun26 / sh_out
H['pb'] = spot / H['bvps']
H['ni_ltm'] = np_h126 + (np_fy25 - np_h125)
H['eps_ltm'] = H['ni_ltm'] / wavg_sh_h126
H['pe_ltm'] = spot / H['eps_ltm']
H['eq_avg'] = (eqctl_jun26 + eqctl_dec25) / 2.0
H['roe_ltm'] = H['ni_ltm'] / H['eq_avg']
H['rev_ltm'] = rev_h126 + (rev_fy25_ir - rev_h125)
H['ps_ltm'] = H['mktcap'] / H['rev_ltm']
H['ebitda_ltm'] = H['ebitda_h126'] + (ebitda_fy25_ir - H['ebitda_h125'])
H['ev_company'] = H['mktcap'] + H['netdebt_company']
H['ev_broad'] = H['mktcap'] + H['netdebt_broad']
H['ev_restricted'] = H['mktcap'] + H['netdebt_restricted']
H['ev_ebitda_company'] = H['ev_company'] / H['ebitda_ltm']
H['ev_ebitda_broad'] = H['ev_broad'] / H['ebitda_ltm']
H['de_narrow'] = H['debt_narrow'] / eqctl_jun26
H['de_broad'] = H['debt_broad'] / eqctl_jun26
H['div_yield'] = (divs_h126 * 2.0) / H['mktcap']

# Market context
H['mkt_value_growth'] = mkt_h126 / mkt_h125 - 1.0
H['mkt_ticket_growth'] = (1.0 + H['mkt_value_growth']) / (1.0 + mkt_units_chg) - 1.0
H['phdc_share'] = phdc_sales_h126 / mkt_h126

# ============================ COST OF CAPITAL ================================
W = {}
W['beta'] = beta_val
W['rf_obs'] = rf_obs
W['rf_star_rating'] = rf_obs - ds_rating
W['rf_star_cds'] = rf_obs - ds_cds
W['ke_rating'] = W['rf_star_rating'] + beta_val * erp_rating
W['ke_cds'] = W['rf_star_cds'] + beta_val * erp_cds
W['kd_marginal'] = rf_obs + H['corp_spread']
W['kd_at'] = W['kd_marginal'] * (1.0 - taxrate_stat)
W['E'] = H['mktcap']
W['D'] = H['debt_narrow']
W['we'] = W['E'] / (W['E'] + W['D'])
W['wd'] = W['D'] / (W['E'] + W['D'])
W['wacc_rating'] = W['we'] * W['ke_rating'] + W['wd'] * W['kd_at']
W['wacc_cds'] = W['we'] * W['ke_cds'] + W['wd'] * W['kd_at']
W['wacc_spot'] = (W['wacc_rating'] + W['wacc_cds']) / 2.0
# Terminal / normalised leg (the ARCC house prior for Egypt)
W['beta_term'] = 1.0
W['ke_term'] = rf_term + W['beta_term'] * erp_term
W['kd_term'] = rf_term + 0.030
W['kd_term_at'] = W['kd_term'] * (1.0 - taxrate_stat)
W['wacc_term'] = W['we'] * W['ke_term'] + W['wd'] * W['kd_term_at']

# The two cost-of-capital framings the study publishes side by side in the
# sensitivity: A holds the spot-anchored rate constant; B glides linearly from the
# spot rate to the normalised terminal rate over the explicit horizon.
NY = 6                                    # H2-2026 stub + FY2027..FY2031
W['wacc_path_spot'] = [W['wacc_cds']] * NY
W['wacc_path_glide'] = list(np.linspace(W['wacc_cds'], W['wacc_term'], NY))
W['wacc_term_spot'] = W['wacc_cds']
W['wacc_term_glide'] = W['wacc_term']

# ============================ FORECAST ENGINE ================================
YEARS = ['H2-2026E', 'FY2027E', 'FY2028E', 'FY2029E', 'FY2030E', 'FY2031E']
FRAC = [0.5, 1.0, 1.0, 1.0, 1.0, 1.0]              # length of each period in years
TMID = [0.25, 1.0, 2.0, 3.0, 4.0, 5.0]             # mid-period discounting from 30-Jun-2026
TTERM = 5.5

pi_cost = [sum(w * e[i] for w, e in zip(cost_w, [esc_steel, esc_cement, esc_finish, esc_labour]))
           for i in range(5)]

def build(ra_is_enterprise: bool, wacc_path, wacc_terminal, P_override=None, vol_override=None,
          pi_cost_shift=0.0, pi_price_shift=0.0):
    """Full statement build. Returns a dict of arrays, one entry per period."""
    Pfac = 1.0 if P_override is None else P_override
    vg = vol_override if vol_override is not None else vol_growth
    n = len(YEARS)
    # The H2-2026 stub is half a year at half the FY2027 growth rate, so the first
    # forecast period carries the same sequential build the disclosed half-year did.
    # It is not a frozen copy of H1-2026: that would hand the model a working-capital
    # release it has not earned.
    V = [0.5 * (1.0 + vg[0]) ** 0.5]
    priceidx = [(1.0 + pi_price[0] + pi_price_shift) ** 0.5]
    costidx = [(1.0 + pi_cost[0] + pi_cost_shift) ** 0.5]
    for i in range(5):
        step = (1.0 + vg[i]) ** (0.5 if i == 0 else 1.0)
        V.append((V[-1] / 0.5 if i == 0 else V[-1]) * step)
        priceidx.append(priceidx[-1] * (1.0 + pi_price[i] + pi_price_shift) ** (0.5 if i == 0 else 1.0))
        costidx.append(costidx[-1] * (1.0 + pi_cost[i] + pi_cost_shift) ** (0.5 if i == 0 else 1.0))

    re_rev, constr, landp, cogs_re = [], [], [], []
    for i in range(n):
        rr = rev_re_h126 * 2.0 * V[i] * priceidx[i]
        cc = H['c1'] * Pfac ** 0 * rev_re_h126 * 2.0 * V[i] * costidx[i] / Pfac
        lp = H['c2'] * rr
        re_rev.append(rr); constr.append(cc); landp.append(lp); cogs_re.append(cc + lp)

    # other legs: grow with the price index and volume, margins held at measured rates
    com_m = 1.0 - cost_com_h126 / rev_com_h126
    clb_m = 1.0 - (cost_clb_h126 + dep_clb_h126) / rev_clb_h126
    oth_base = (transfer_h126 + util_h126) * 2.0
    rev_com = [rev_com_h126 * 2.0 * V[i] * priceidx[i] for i in range(n)]
    rev_hot = [rev_hot_h126 * 2.0 * V[i] * priceidx[i] for i in range(n)]
    rev_clb = [rev_clb_h126 * 2.0 * V[i] * priceidx[i] for i in range(n)]
    rev_oth = [oth_base * V[i] * priceidx[i] for i in range(n)]
    cost_com = [rev_com[i] * (1.0 - com_m) for i in range(n)]
    cost_clb = [rev_clb[i] * (1.0 - clb_m) for i in range(n)]
    cost_mac = [dep_mac_h126 * 2.0 * FRAC[i] * costidx[i] for i in range(n)]

    rev = [re_rev[i] + rev_com[i] + rev_hot[i] + rev_clb[i] + rev_oth[i] for i in range(n)]
    cogs = [cogs_re[i] + cost_com[i] + cost_clb[i] + cost_mac[i] for i in range(n)]
    cashdisc = [cashdisc_h126 / rev_h126 * rev[i] for i in range(n)]
    gp = [rev[i] - cogs[i] - cashdisc[i] for i in range(n)]

    sal_base = sal_h126 * 2.0
    sal, w = [], 1.0
    for i in range(n):
        if i > 0:
            w *= (1.0 + esc_labour[i - 1]) * (1.0 + hcount_growth)
        sal.append(sal_base * FRAC[i] * w)
    adm_rate = adm_h126 / rev_h126
    adm = [rev[i] * adm_rate for i in range(n)]
    sga = [sal[i] + adm[i] for i in range(n)]
    ecl = [rev[i] * (ecl_h126 / rev_h126) for i in range(n)]
    da = [rev[i] * (da_cf_h126 * 2.0 / H['rev_ann']) for i in range(n)]
    capex = [rev[i] * ((capex_h126 + capex_cip_h126) * 2.0 / H['rev_ann']) for i in range(n)]

    amort_nr = [rev[i] * (amort_nr_h126 / rev_h126) for i in range(n)]
    tbill_inc = [rev[i] * (tbillinc_h126 / rev_h126) for i in range(n)] if ra_is_enterprise else [0.0] * n

    cap_int_back = [constr[i] * (capint_h126 / work_h126) for i in range(n)]
    ebitda_ = [gp[i] - sga[i] - ecl[i] + cap_int_back[i] for i in range(n)]
    ebit = [ebitda_[i] - da[i] + amort_nr[i] + tbill_inc[i] for i in range(n)]

    eff_tax = (curtax_h126 + deftax_h126) / pbt_h126
    nopat = [ebit[i] * (1.0 - eff_tax) for i in range(n)]

    # working capital, each block on its measured ratio to its own driver
    r_recv = H['recv_total_jun26'] / H['rev_ann']
    r_wip = wip_jun26 / H['relief_ann']
    r_supadv = supadv_jun26 / H['relief_ann']
    r_dr = dr_jun26 / H['rev_ann']
    r_adv = adv_jun26 / H['rev_ann']
    r_supcon = supcon_jun26 / H['relief_ann']
    r_cred = cred_jun26 / H['rev_ann']
    r_jsa = (jsa_st_jun26 + jsa_lt_jun26) / H['rev_ann']
    r_maint = maint_nr / H['rev_ann']          # maintenance-deposit checks inside receivables

    def ann(x, i):    # annualised flow for stock ratios
        return x[i] / FRAC[i]

    nwc = []
    for i in range(n):
        rev_a, rel_a = ann(rev, i), ann(constr, i)
        rr = r_recv if ra_is_enterprise else (r_recv - r_maint)
        assets = rev_a * rr + rel_a * r_wip + rel_a * r_supadv + rev_a * r_dr
        liabs = rev_a * r_adv + rel_a * r_supcon + rev_a * r_cred + rev_a * r_jsa
        nwc.append(assets - liabs)
    nwc0 = (H['recv_total_jun26'] + wip_jun26 + supadv_jun26 + dr_jun26
            - adv_jun26 - supcon_jun26 - cred_jun26 - (jsa_st_jun26 + jsa_lt_jun26))
    if not ra_is_enterprise:
        nwc0 -= maint_nr
    d_nwc = [nwc[0] - nwc0] + [nwc[i] - nwc[i - 1] for i in range(1, n)]
    # The float converges on a steady-state multiple of revenue: the balance keeps
    # building while deliveries grow, then holds. Modelling it as an unbounded share of
    # revenue would make the ratio rise for ever, which no disclosed period supports.
    ra_ratio_0 = ra_jun26 / H['rev_ann']
    H['ra_ratio_0'] = ra_ratio_0
    ra_stock = []
    for i in range(n):
        r = ra_ratio_0 + (ra_target_ratio - ra_ratio_0) * (i + 1) / n
        ra_stock.append(ann(rev, i) * r)
    d_ra = [ra_stock[0] - ra_jun26] + [ra_stock[i] - ra_stock[i - 1] for i in range(1, n)]
    ra_cash = list(d_ra)

    fcff = []
    for i in range(n):
        f = nopat[i] + da[i] - capex[i] - d_nwc[i]
        if ra_is_enterprise:
            f += ra_cash[i]
        fcff.append(f)

    # terminal: reinvestment-consistent Gordon on the model's own return on capital
    ic_end = nwc[-1] + fa_jun26 + invprop_jun26 + cip_jun26
    ic_end_ex_float = ic_end - (ra_stock[-1] if ra_is_enterprise else 0.0)
    roic = nopat[-1] / ic_end
    reinv = term_g / roic if roic > 0 else 1.0
    reinv = min(max(reinv, 0.0), 0.95)
    fcff_term = nopat[-1] * (1.0 + term_g) * (1.0 - reinv)
    # In perpetuity the float cannot keep growing at a fixed share of REVENUE: that
    # ratio would rise without bound. Beyond the explicit horizon it is held at a
    # constant multiple of revenue, so only its growth with revenue is a cash source.
    ra_ratio_end = 0.0
    if ra_is_enterprise:
        ra_ratio_end = ra_stock[-1] / (rev[-1] / FRAC[-1])
        fcff_term += ra_ratio_end * (rev[-1] / FRAC[-1]) * term_g * (1.0 + term_g)
    tv = fcff_term / (wacc_terminal - term_g)

    df = [1.0 / (1.0 + wacc_path[i]) ** TMID[i] for i in range(n)]
    df_t = 1.0 / (1.0 + wacc_terminal) ** TTERM
    pv_explicit = sum(fcff[i] * df[i] for i in range(n))
    pv_term = tv * df_t
    ev = pv_explicit + pv_term
    return dict(V=V, priceidx=priceidx, costidx=costidx, re_rev=re_rev, constr=constr,
                landp=landp, rev=rev, cogs=cogs, cashdisc=cashdisc, gp=gp, sal=sal, adm=adm,
                sga=sga, ecl=ecl, da=da, capex=capex, amort_nr=amort_nr, tbill_inc=tbill_inc,
                ebitda=ebitda_, ebit=ebit, nopat=nopat, nwc=nwc, d_nwc=d_nwc, ra_stock=ra_stock,
                d_ra=d_ra, ra_cash=ra_cash, fcff=fcff, df=df, df_t=df_t, roic=roic, reinv=reinv,
                ic_end=ic_end, fcff_term=fcff_term, tv=tv, pv_explicit=pv_explicit,
                cap_int_back=cap_int_back, ra_ratio_end=ra_ratio_end,
                ic_end_ex_float=ic_end_ex_float,
                roic_ex_float=nopat[-1] / ic_end_ex_float if ic_end_ex_float > 0 else float('nan'),
                pv_term=pv_term, ev=ev, eff_tax=eff_tax, nwc0=nwc0,
                gm=[gp[i] / rev[i] for i in range(n)],
                re_gm=[1.0 - (constr[i] + landp[i]) / re_rev[i] for i in range(n)])

def bridge(ev, netdebt):
    eq = ev - netdebt - eqnci_jun26
    return dict(ev=ev, netdebt=netdebt, nci=eqnci_jun26, equity=eq, vps=eq / sh_out)

# --- the two framings of the contested judgement -----------------------------
A = build(True, W['wacc_path_glide'], W['wacc_term_glide'])
B = build(False, W['wacc_path_glide'], W['wacc_term_glide'])
A_bridge = bridge(A['ev'], H['netdebt_company'])
B_bridge = bridge(B['ev'], H['netdebt_restricted'])

# --- the same two, on the spot-anchored constant cost of capital -------------
A_spot = build(True, W['wacc_path_spot'], W['wacc_term_spot'])
B_spot = build(False, W['wacc_path_spot'], W['wacc_term_spot'])
A_spot_bridge = bridge(A_spot['ev'], H['netdebt_company'])
B_spot_bridge = bridge(B_spot['ev'], H['netdebt_restricted'])

DCF = dict(
    framing_A=dict(label="Residents' Association float treated as permanent operating funding",
                   **{k: A[k] for k in ('rev', 'ebitda', 'ebit', 'nopat', 'da', 'capex', 'd_nwc',
                                        'ra_cash', 'fcff', 'df', 'pv_explicit', 'pv_term', 'ev',
                                        'roic', 'reinv', 'tv', 'fcff_term', 'gm', 're_gm', 'nwc',
                                        'constr', 'landp', 're_rev', 'sga', 'ecl', 'cap_int_back',
                                        'amort_nr', 'tbill_inc',
                                        'ra_ratio_end', 'ic_end', 'ic_end_ex_float',
                                        'roic_ex_float')},
                   bridge=A_bridge, bridge_spot=A_spot_bridge, ev_spot=A_spot['ev']),
    framing_B=dict(label="Residents' Association float treated as restricted third-party money",
                   **{k: B[k] for k in ('rev', 'ebitda', 'ebit', 'nopat', 'da', 'capex', 'd_nwc',
                                        'ra_cash', 'fcff', 'df', 'pv_explicit', 'pv_term', 'ev',
                                        'roic', 'reinv', 'tv', 'fcff_term', 'gm', 're_gm', 'nwc',
                                        'constr', 'landp', 're_rev', 'sga', 'ecl', 'cap_int_back',
                                        'amort_nr', 'tbill_inc',
                                        'ra_ratio_end', 'ic_end', 'ic_end_ex_float',
                                        'roic_ex_float')},
                   bridge=B_bridge, bridge_spot=B_spot_bridge, ev_spot=B_spot['ev']),
    years=YEARS, tmid=TMID, tterm=TTERM, pi_cost=pi_cost, eff_tax=A['eff_tax'], nwc0=A['nwc0'])

# ============================ THE OTHER THREE LENSES =========================
L = {}
# 1. cash-flow lens: the two framings are the field, never averaged
L['dcf'] = dict(A=A_bridge['vps'], B=B_bridge['vps'],
                A_spot=A_spot_bridge['vps'], B_spot=B_spot_bridge['vps'],
                low=min(A_bridge['vps'], B_bridge['vps']),
                high=max(A_bridge['vps'], B_bridge['vps']),
                note='The field is the contested judgement computed both ways on the primary '
                     'discount path; the spot-anchored variants are carried in the sensitivity, '
                     'never blended into the field.')

# 2. book value and sustainable return: justified price to book
ke_used = W['ke_cds']
roe_sust = H['roe_ltm']
g_book = term_g
L['book'] = dict(bvps=H['bvps'], roe=roe_sust, ke=ke_used, ke_term=W['ke_term'], g=g_book)
L['book']['pb_spot'] = (roe_sust - g_book) / (ke_used - g_book)
L['book']['pb_norm'] = (roe_sust - g_book) / (W['ke_term'] - g_book)
L['book']['vps_spot'] = L['book']['pb_spot'] * H['bvps']
L['book']['vps_norm'] = L['book']['pb_norm'] * H['bvps']
L['book']['low'] = min(L['book']['vps_spot'], L['book']['vps_norm'])
L['book']['high'] = max(L['book']['vps_spot'], L['book']['vps_norm'])
L['book']['mid'] = (L['book']['low'] + L['book']['high']) / 2.0

# 3. relative multiples, in-country and out-of-country
eg_pe = [p['pe'] for p in peers if p['country'] == 'Egypt' and p['pe']]
gulf_pe = [p['pe'] for p in peers if p['country'] != 'Egypt' and p['pe']]
L['relative'] = dict(
    eg_pe_median=float(np.median(eg_pe)), eg_pe_min=min(eg_pe), eg_pe_max=max(eg_pe),
    gulf_pe_median=float(np.median(gulf_pe)),
    all_pe_median=float(np.median(eg_pe + gulf_pe)),
    phdc_pe=H['pe_ltm'], phdc_eps=H['eps_ltm'], phdc_pb=H['pb'],
    ev_ebitda_gulf=float(np.median([p['ev_ebitda'] for p in peers if p.get('ev_ebitda')])),
    phdc_ev_ebitda=H['ev_ebitda_company'])
L['relative']['vps_eg'] = L['relative']['eg_pe_median'] * H['eps_ltm']
L['relative']['vps_all'] = L['relative']['all_pe_median'] * H['eps_ltm']
L['relative']['vps_gulf'] = L['relative']['gulf_pe_median'] * H['eps_ltm']
_ev_at_peer = L['relative']['ev_ebitda_gulf'] * H['ebitda_ltm']
L['relative']['vps_evebitda'] = (_ev_at_peer - H['netdebt_company'] - eqnci_jun26) / sh_out
L['relative']['ev_at_peer'] = _ev_at_peer
_rel = [L['relative']['vps_eg'], L['relative']['vps_all'], L['relative']['vps_gulf'],
        L['relative']['vps_evebitda']]
L['relative']['low'] = min(_rel)
L['relative']['high'] = max(_rel)
L['relative']['mid'] = float(np.median(_rel))

# 4. normalised earnings power: mid-cycle margin on the FY2027E revenue base
norm_margin = float(np.mean([H['ebitda_margin_fy23'], H['ebitda_margin_fy24'],
                             H['ebitda_margin_h126']]))
norm_rev = H['rev_ltm']
norm_ebitda = norm_rev * norm_margin
norm_da = da_cf_h126 * 2.0
norm_ebit = norm_ebitda - norm_da
norm_int = intdebt_jun26 * H['kd_realised'] * (1.0 - H['cap_ratio'])
norm_amort_nr = amort_nr_h126 * 2.0
norm_tbill = tbillinc_h126 * 2.0
norm_pbt = norm_ebit + norm_amort_nr + norm_tbill - norm_int
norm_ni = norm_pbt * (1.0 - A['eff_tax'])
norm_eps = norm_ni / sh_out
_pe_lo = min(L['relative']['gulf_pe_median'], L['relative']['eg_pe_median'])
_pe_hi = max(L['relative']['gulf_pe_median'], L['relative']['eg_pe_median'])
L['normalised'] = dict(margin=norm_margin, rev=norm_rev, ebitda=norm_ebitda, ebit=norm_ebit,
                       da=norm_da, amort_nr=norm_amort_nr, tbill=norm_tbill,
                       interest=norm_int, pbt=norm_pbt, ni=norm_ni, eps=norm_eps,
                       pe_lo=_pe_lo, pe_hi=_pe_hi)
L['normalised']['low'] = norm_eps * _pe_lo
L['normalised']['high'] = norm_eps * _pe_hi
L['normalised']['mid'] = (L['normalised']['low'] + L['normalised']['high']) / 2.0

# --- synthesis: four lenses, run twice — once under each framing of the
# --- contested judgement. The two are never blended into a single cash-flow number.
WEIGHTS = dict(dcf=0.45, book=0.20, relative=0.20, normalised=0.15)
for _k in ('book', 'relative', 'normalised'):
    _lo, _hi = L[_k]['low'], L[_k]['high']
    L[_k]['low'], L[_k]['high'] = min(_lo, _hi), max(_lo, _hi)
    L[_k]['mid'] = (L[_k]['low'] + L[_k]['high']) / 2.0

# Inside each framing the cash-flow lens still carries a range: the spot-anchored
# cost of capital at one end, the normalised glide at the other.
L['dcf']['A_low'], L['dcf']['A_high'] = sorted([L['dcf']['A_spot'], L['dcf']['A']])
L['dcf']['B_low'], L['dcf']['B_high'] = sorted([L['dcf']['B_spot'], L['dcf']['B']])
L['dcf']['A_mid'] = (L['dcf']['A_low'] + L['dcf']['A_high']) / 2.0
L['dcf']['B_mid'] = (L['dcf']['B_low'] + L['dcf']['B_high']) / 2.0
L['dcf']['low'], L['dcf']['high'] = L['dcf']['B_low'], L['dcf']['A_high']
L['dcf']['mid'] = None      # deliberately absent: the two framings are not averaged

def synth(dlo, dmid, dhi):
    lo = dict(dcf=dlo, book=L['book']['low'], relative=L['relative']['low'], normalised=L['normalised']['low'])
    md = dict(dcf=dmid, book=L['book']['mid'], relative=L['relative']['mid'], normalised=L['normalised']['mid'])
    hi = dict(dcf=dhi, book=L['book']['high'], relative=L['relative']['high'], normalised=L['normalised']['high'])
    return dict(bear=sum(lo[k] * WEIGHTS[k] for k in WEIGHTS),
                base=sum(md[k] * WEIGHTS[k] for k in WEIGHTS),
                bull=sum(hi[k] * WEIGHTS[k] for k in WEIGHTS),
                lens_lo=lo, lens_mid=md, lens_hi=hi)

SYN_A = synth(L['dcf']['A_low'], L['dcf']['A_mid'], L['dcf']['A_high'])
SYN_B = synth(L['dcf']['B_low'], L['dcf']['B_mid'], L['dcf']['B_high'])
SYN = dict(weights=WEIGHTS, framing_A=SYN_A, framing_B=SYN_B,
           base_framing='A',
           base_framing_note="The base case adopts framing A — the Residents' Association balance "
           'is treated as permanent operating funding — because that is how the company has actually '
           'operated for a decade: the balance has risen in every disclosed period, no association '
           'has been constituted, and the invested proceeds earn for the company. Framing B is not a '
           'haircut on it; it is the same four lenses computed in full under the other reading, and '
           'it is what the study publishes as the downside. The two are never averaged.',
           bear=SYN_B['base'], base=SYN_A['base'], bull=SYN_A['bull'],
           lens_mid=SYN_A['lens_mid'], lens_lo=SYN_B['lens_lo'], lens_hi=SYN_A['lens_hi'],
           field_lo=min(SYN_B['lens_lo'].values()), field_hi=max(SYN_A['lens_hi'].values()))
SYN['upside_base'] = SYN['base'] / spot - 1.0
SYN['upside_bear'] = SYN['bear'] / spot - 1.0
SYN['upside_bull'] = SYN['bull'] / spot - 1.0

# ============================ SENSITIVITY ====================================
def vps_at(P_mult, wacc_shift, framing_A=True):
    path = [w + wacc_shift for w in W['wacc_path_glide']]
    r = build(framing_A, path, W['wacc_term_glide'] + wacc_shift, P_override=P_mult)
    nd = H['netdebt_company'] if framing_A else H['netdebt_restricted']
    return bridge(r['ev'], nd)['vps']

P_MULTS = [0.90, 0.95, 1.00, 1.05, 1.10]
W_SHIFTS = [-0.02, -0.01, 0.0, 0.01, 0.02]
SENS = dict(p_mults=P_MULTS, w_shifts=W_SHIFTS,
            grid_A=[[vps_at(p, s, True) for p in P_MULTS] for s in W_SHIFTS],
            grid_B=[[vps_at(p, s, False) for p in P_MULTS] for s in W_SHIFTS],
            crux_P=[H['P_h126'] * m for m in P_MULTS])

# volume sensitivity
def vps_vol(mult):
    vg = [g * mult for g in vol_growth]
    r = build(True, W['wacc_path_glide'], W['wacc_term_glide'], vol_override=vg)
    return bridge(r['ev'], H['netdebt_company'])['vps']
def vps_vol_B(mult):
    vg = [g * mult for g in vol_growth]
    r = build(False, W['wacc_path_glide'], W['wacc_term_glide'], vol_override=vg)
    return bridge(r['ev'], H['netdebt_restricted'])['vps']
SENS['vol_mults'] = [0.0, 0.5, 1.0, 1.5]
SENS['vol_vps'] = [vps_vol(m) for m in SENS['vol_mults']]
SENS['vol_vps_B'] = [vps_vol_B(m) for m in SENS['vol_mults']]
GROWTH_SIGN = dict(A=SENS['vol_vps'][-1] - SENS['vol_vps'][0],
                   B=SENS['vol_vps_B'][-1] - SENS['vol_vps_B'][0])

# cost-escalator sensitivity: one class at a time, +200bp for the whole path
def vps_costshift(bp):
    r = build(True, W['wacc_path_glide'], W['wacc_term_glide'], pi_cost_shift=bp)
    return bridge(r['ev'], H['netdebt_company'])['vps']
SENS['cost_shifts'] = [-0.02, -0.01, 0.0, 0.01, 0.02]
SENS['cost_vps'] = [vps_costshift(b) for b in SENS['cost_shifts']]

# --- reconciliation: the model's first forecast period against the last actual ----
H['ufcf_h126_actual'] = (ocf_h126 + bank_int_h126 + capint_h126
                         - (capex_h126 + capex_cip_h126))
# Two disclosed movements make H1-2026 a poor like-for-like against a forward period,
# and both are read straight off the balance sheet rather than assumed.
H['tax_payable_unwind'] = 1976.557733 - 986.469796
INP['tax_payable_dec25'] = I(1976.557733, FS26 + ' — income tax payable, comparative', '31-Dec-2025', 'Company')
INP['tax_payable_jun26'] = I(986.469796, FS26 + ' — income tax payable', '30-Jun-2026', 'Company')
H['jsa_unwind'] = (jsa_st_dec25 + jsa_lt_dec25) - (jsa_st_jun26 + jsa_lt_jun26)
H['ufcf_h126_like_for_like'] = (H['ufcf_h126_actual'] + H['tax_payable_unwind'] + H['jsa_unwind'])
H['ufcf_h226_model_A'] = A['fcff'][0]
H['ufcf_h226_model_B'] = B['fcff'][0]
H['recon_gap'] = H['ufcf_h226_model_A'] / H['ufcf_h126_like_for_like'] - 1.0
H['recon_residual'] = H['ufcf_h126_like_for_like'] - H['ufcf_h226_model_A']
# Income-statement reconciliation, where the model should be tight and is.
H['ebitda_h126_plus_capint'] = H['ebitda_h126'] + H['constr_relief_h126'] * (capint_h126 / work_h126)
H['ebitda_h226_expected'] = H['ebitda_h126_plus_capint'] * (A['rev'][0] / rev_h126)
H['ebitda_recon_gap'] = A['ebitda'][0] / H['ebitda_h226_expected'] - 1.0

# ============================ INTERACTIVE-SLIDER REFIT =======================
# The ticker page carries a five-lever what-if whose constants were fitted to the
# retired ten-factor macro simulation, not to a fundamental driver stack. They are
# refitted here from this model's own elasticities, measured on the PUBLISHED FAIR
# VALUE (the four-lens synthesis), not on the cash-flow lens alone. renderFairLevers
# computes  fair = base * exp( sum_i impact_i * (v_i - def_i) / 100 ), so
# impact_i = 100 * d(ln published fair value) / d(lever unit).
def syn_base(**shock):
    """Published base fair value under a driver shock. Only the cash-flow lens moves."""
    g = build(True, [w + shock.get('dw', 0.0) for w in W['wacc_path_glide']],
              W['wacc_term_glide'] + shock.get('dw', 0.0),
              vol_override=shock.get('vol'), pi_cost_shift=shock.get('dc', 0.0),
              pi_price_shift=shock.get('dp', 0.0))
    sp = build(True, [w + shock.get('dw', 0.0) for w in W['wacc_path_spot']],
               W['wacc_term_spot'] + shock.get('dw', 0.0),
               vol_override=shock.get('vol'), pi_cost_shift=shock.get('dc', 0.0),
               pi_price_shift=shock.get('dp', 0.0))
    lo, hi = sorted([bridge(g['ev'], H['netdebt_company'])['vps'],
                     bridge(sp['ev'], H['netdebt_company'])['vps']])
    return synth(lo, (lo + hi) / 2.0, hi)['base']

_base_vps = SYN['base']
def _elas(hi, lo, dunits):
    return 100.0 * (np.log(hi) - np.log(lo)) / dunits

FX_PASSTHRU = dict(steel=0.70, cement=0.40, finishing=0.50, labour=0.0)
INP['fx_passthru'] = I(FX_PASSTHRU, 'Share of each construction cost class that reprices with the pound. '
                       'Steel is billet and scrap linked, cement carries imported coal and energy, finishing '
                       'carries imported fittings, site labour carries none. ESTIMATED, recorded as such and '
                       'carried through the sensitivity', '19-Aug-2026', 'Industry')
_fx_pt = (cost_w[0] * FX_PASSTHRU['steel'] + cost_w[1] * FX_PASSTHRU['cement']
          + cost_w[2] * FX_PASSTHRU['finishing'] + cost_w[3] * FX_PASSTHRU['labour'])
# one unit of the currency lever = 1pp per quarter of pound strength = 4pp a year less
# imported cost pressure, of which _fx_pt reaches the build cost
_dc_per_unit = -0.04 * _fx_pt
_imp_fx = _elas(syn_base(dc=+_dc_per_unit / 2.0), syn_base(dc=-_dc_per_unit / 2.0), 1.0)
_imp_rate = _elas(syn_base(dw=-0.005), syn_base(dw=+0.005), 1.0)

_TOURISM_SHARE = 0.33
INP['tourism_share'] = I(_TOURISM_SHARE, 'Share of the group construction-volume driver exposed to North '
                         'Coast and coastal demand. ESTIMATED from the disclosed project list; the filings '
                         'do not publish a volume split by region', '19-Aug-2026', 'Company')
# one unit of the demand lever = 1pp of year-on-year coastal absorption; it reaches the
# group through volume and, because absorption sets pricing power, through price
_du = 0.01 * _TOURISM_SHARE
_imp_tourism = _elas(syn_base(vol=[g + _du / 2 for g in vol_growth], dp=+_du / 4),
                     syn_base(vol=[g - _du / 2 for g in vol_growth], dp=-_du / 4), 1.0)

# Discrete events keep their probability-times-impact form. A regional security shock is
# specified on PRICE and cost, not on the volume path: what a security shock does to a
# seller of homes is soften what buyers will pay and harden what it costs to build, while
# the volume actually put in place is set by the company's own construction programme.
# The lever is linear in PROBABILITY, so its slope is the log of the conditional
# multiplier: ln(m) for an event that multiplies value by m. Note the asymmetry in the
# two sign conventions below — the security lever runs from risky to calm, so its
# probability FALLS as the lever rises, while the launch lever runs the other way. Both
# slopes are therefore positive, but the security one is -ln(1 - hit), NOT ln(1 + hit):
# those agree to first order and diverge badly at a hit this size (0.360 against 0.264).
_v_geo = syn_base(dp=-0.03, dc=+0.01)
_geo_hit = 1.0 - _v_geo / _base_vps
_v_lnch = syn_base(vol=[g + 0.01 for g in vol_growth], dp=+0.005)
_lnch_hit = _v_lnch / _base_vps - 1.0
_imp_geo = float(-np.log(1.0 - _geo_hit))    # per percentage point of probability
_imp_lnch = float(np.log(1.0 + _lnch_hit))

SLIDER = dict(
    formula='fair = base * exp( sum_i impact_i * (v_i - def_i) / 100 )',
    measured_on='published base fair value (four-lens synthesis, framing A)',
    fx_passthrough=_fx_pt, geo_hit=_geo_hit, launch_hit=_lnch_hit,
    levers=[
        dict(key='fx', min=-5, max=1, step=0.5, default=-2.5, impact=round(float(_imp_fx), 3),
             note='One unit is a percentage point per quarter of pound strength. It reaches fair value '
                  'through the construction cost stack: %.0f%% of the build cost reprices with the '
                  'currency.' % (_fx_pt * 100)),
        dict(key='rate', min=-2, max=2, step=0.5, default=0, impact=round(float(_imp_rate), 3),
             note='One unit is a percentage point of easing across the whole discount-rate path.'),
        dict(key='geo', min=0, max=60, step=5, default=30, impact=round(float(_imp_geo), 4),
             note='Probability of a regional security shock, specified as three points off the selling-'
                  'price path and one point onto the cost path. Measured cost in this model: %.1f%% of '
                  'fair value.' % (_geo_hit * 100)),
        dict(key='launch', min=0, max=100, step=5, default=85, impact=round(float(_imp_lnch), 4),
             note='The default rises from 55 to 85 because the launch in question has now happened: '
                  'Hacienda Ras El Hekma opened in August 2026. The evidence for it is secondary, so '
                  'the default stops short of certainty. Measured gain if it lands: %.1f%% of fair '
                  'value.' % (_lnch_hit * 100)),
        dict(key='tourism', min=-10, max=10, step=1, default=0, impact=round(float(_imp_tourism), 4),
             note='One unit is a percentage point of year-on-year coastal absorption, applied to the '
                  '%.0f%% of the volume driver that is coastal.' % (_TOURISM_SHARE * 100)),
    ])
# The slider must reproduce the measured conditional event sizes when read back through
# renderFairLevers' own formula — the check that would have caught the transform error.
_geo_lever = next(l for l in SLIDER['levers'] if l['key'] == 'geo')
_lnch_lever = next(l for l in SLIDER['levers'] if l['key'] == 'launch')
# security: probability = (max - v)/100, so p goes 0 -> 0.60 as the lever falls to its min
SLIDER['geo_implied_hit'] = 1.0 - float(np.exp(
    _geo_lever['impact'] * (_geo_lever['min'] - _geo_lever['max']) / 100.0)) ** (1.0 / 0.60)
# launch: probability = v/100, so p goes 0 -> 1.00 as the lever rises to its max
SLIDER['launch_implied_hit'] = float(np.exp(
    _lnch_lever['impact'] * (_lnch_lever['max'] - _lnch_lever['min']) / 100.0)) - 1.0

SLIDER['span'] = {l['key']: dict(
    lo=_base_vps * float(np.exp(l['impact'] * (l['min'] - l['default']) / 100.0)),
    hi=_base_vps * float(np.exp(l['impact'] * (l['max'] - l['default']) / 100.0))) for l in SLIDER['levers']}

# ============================ SCORING THE PRIOR STUDY ========================
# Every prior-study forecast for a period that has now been disclosed, against the
# actual. Annualisation of H1 actuals is stated wherever it is used.
def var(name, forecast, actual, unit, note):
    d = None if (forecast in (None, 0)) else actual / forecast - 1.0
    return dict(item=name, forecast=forecast, actual=actual, unit=unit,
                delta=None if d is None else d,
                escalates=None if d is None else abs(d) > 0.05, note=note)

VARIANCE = [
    var('FY2026 revenue', PR['rev_fy26'], H['rev_ann'], 'EGP mn',
        'Actual is H1-2026 annualised at the H1 run-rate. The prior model carried no interim '
        'actuals; it started from a project-by-project unit build with no disclosed base period.'),
    var('FY2026 gross margin', PR['gm_fy26'], H['gm_h126'], 'ratio',
        'H1-2026 reported gross operating margin. The prior figure was an output of assumed unit '
        'prices and assumed construction costs per square metre, none of them disclosed.'),
    var('FY2026 EBITDA', PR['ebitda_fy26'], H['ebitda_h126'] * 2.0, 'EGP mn',
        ('On the definition the company itself publishes, recovered from the statements as gross '
         'profit less administrative and selling cost less expected credit losses. H1-2025 is the '
         'only period for which the company published an EBITDA figure AND the statements disclose '
         'its components; there the recovered definition reproduces the published EGP 4,458.5mn to '
         'within %.2f%%.') % abs(H['ebitda_def_gap_h125'] * 100)),
    var('FY2026 net income', PR['ni_fy26'], np_h126 * 2.0, 'EGP mn',
        'Attributable net profit, H1-2026 annualised.'),
    var('FY2026 capital expenditure', PR['capex_fy26'], (capex_h126 + capex_cip_h126) * 2.0,
        'EGP mn', 'Payments for fixed assets plus projects under construction, H1-2026 annualised.'),
    var('Net debt at the anchor', PR['netdebt'], H['netdebt_company'], 'EGP mn',
        "Against the company's own definition (interest-bearing obligations from note 34 less cash "
        'and treasury investments). Under the broader definition that also carries notes payable and '
        'land liabilities the figure is EGP %smn.' % format(round(H['netdebt_broad']), ',')),
    var('Construction run-rate', PR['constr_runrate'], work_h126 * 2.0, 'EGP mn',
        'Work carried out per note 43, H1-2026 annualised, against the prior study\'s stated pacing '
        'of about EGP 14-20bn per year.'),
    var('Shares outstanding', PR['shares'], sh_out, 'mn shares',
        'The prior model divided by issued shares and ignored the treasury holding disclosed in '
        'note 62.'),
    var('Return on equity', PR['roe'], H['roe_ltm'], 'ratio',
        'Trailing twelve months on average controlling equity.'),
    var('Price to sales', PR['ps'], H['ps_ltm'], 'x',
        'At the same published spot of EGP %.2f, on trailing twelve-month revenue.' % spot),
    var('EV to EBITDA', PR['ev_ebitda'], H['ev_ebitda_company'], 'x',
        "On the company's net-debt definition and trailing twelve-month EBITDA."),
    var('Price to earnings', PR['pe'], H['pe_ltm'], 'x',
        'On trailing twelve-month attributable earnings and the ex-treasury share count.'),
    var('Debt to equity', PR['debt_equity'], H['de_narrow'], 'x',
        'Interest-bearing obligations over controlling equity. On the broader debt definition the '
        'ratio is %.2f.' % H['de_broad']),
    var('Weighted cost of capital', PR['wacc'], W['wacc_cds'], 'ratio',
        'The prior study discounted at 18%% while the three-year Egyptian government bond was '
        'clearing at %.2f%%. A weighted cost of capital below the local risk-free rate is not '
        'available to a leveraged equity.' % (rf_obs * 100)),
    var('Terminal growth', PR['term_g'], term_g, 'ratio',
        'The prior 5% nominal terminal growth sat about nine points below the inflation embedded in '
        'its own 14% price escalator — a deeply negative real terminal.'),
    var('Backlog', PR['backlog'], bk_contract, 'EGP mn',
        'Against note 72, the only backlog figure that appears in an audited or reviewed statement: '
        'the contractual value of undelivered-unit contracts concluded between 1-Jan-2023 and '
        '30-Jun-2026. The company\'s own wider definition stood at EGP 263bn at 1Q2026.'),
]

# ---- does growth create or destroy value at the measured return on capital? ----
GDV = dict(roic_A=A['roic'], roic_B=B['roic'], wacc_spot=W['wacc_cds'], wacc_term=W['wacc_term'],
           spread_spot=A['roic'] - W['wacc_cds'], spread_term=A['roic'] - W['wacc_term'],
           nwc_intensity=DCF['nwc0'] / H['rev_ann'],
           nopat_margin=A['nopat'][1] / A['rev'][1])
# A STATIC approximation: it compares one year's operating profit after tax with the
# working capital that one year of growth consumes. It ignores the terminal value's own
# scale, which is why the full model can still show growth adding value where this
# arithmetic says it should not. Both are reported; neither is suppressed.
GDV['breakeven_g_no_float'] = GDV['nopat_margin'] / GDV['nwc_intensity']
GDV['breakeven_g_with_float'] = ((GDV['nopat_margin'] + (A['ra_cash'][3] / A['rev'][3]))
                                 / GDV['nwc_intensity'])
GDV['growth_sign_A'] = GROWTH_SIGN['A']
GDV['growth_sign_B'] = GROWTH_SIGN['B']
GDV['vps_zero_growth'] = SENS['vol_vps'][0]
GDV['vps_zero_growth_B'] = SENS['vol_vps_B'][0]
GDV['roic_ex_float'] = A['roic_ex_float']
GDV['ic_end'] = A['ic_end']
GDV['ic_end_ex_float'] = A['ic_end_ex_float']
GDV['note'] = ('Two measures of the same thing, and they point opposite ways, so both are '
               'published. Measured on all the capital standing in the business the return is '
               '%.1f%%, below the cost of capital on both the spot and the normalised basis, and '
               'the one-year arithmetic that follows from it puts break-even nominal growth at '
               '%.1f%% without the float and %.1f%% with it. Measured on the capital the '
               'shareholders actually put up — that is, net of the customer money funding the '
               'work — the return is %.1f%%, because %.0f%% of the gross capital is customer-'
               'funded. The full model, which carries the terminal value the one-year arithmetic '
               'cannot, moves the same way as the second measure: more volume is worth more under '
               'both framings.') % (GDV['roic_A'] * 100, GDV['breakeven_g_no_float'] * 100,
                                     GDV['breakeven_g_with_float'] * 100, GDV['roic_ex_float'] * 100,
                                     (1 - GDV['ic_end_ex_float'] / GDV['ic_end']) * 100)

# ---- three-year historical income statement, for appendix A.1 ----
HIST3 = dict(
    years=['FY2023', 'FY2024', 'FY2025', 'H1-2025', 'H1-2026'],
    revenue=[rev_fy23, rev_fy24, rev_fy25_ir, rev_h125, rev_h126],
    revenue_source=['audited', 'audited', 'company release only', 'reviewed', 'reviewed'],
    cogs=[cogs_fy23, cogs_fy24, None, cogs_h125, cogs_h126],
    gross_profit=[gp_fy23, gp_fy24, None, gp_h125, gp_h126],
    gross_margin=[H['gm_fy23'], H['gm_fy24'], None, H['gm_h125'], H['gm_h126']],
    sga=[sga_fy23, sga_fy24, None, sga_h125, sga_h126],
    ebitda=[H['ebitda_fy23'], H['ebitda_fy24'], ebitda_fy25_ir, H['ebitda_h125'], H['ebitda_h126']],
    ebitda_margin=[H['ebitda_margin_fy23'], H['ebitda_margin_fy24'],
                   ebitda_fy25_ir / rev_fy25_ir, H['ebitda_margin_h125'], H['ebitda_margin_h126']],
    finance_costs=[1503.563734, fin_fy24, None, fin_h125, fin_h126],
    pbt=[pbt_fy23, pbt_fy24, None, pbt_h125, pbt_h126],
    net_profit=[np_fy23, np_fy24, np_fy25, np_h125, np_h126],
    gap_note='No FY2025 annual financial statements and no FY2025 earnings release are published on '
             'the company investor-relations channel. FY2025 revenue and EBITDA are therefore carried '
             'from the company\'s own history charts in the 1Q2026 release; FY2025 attributable net '
             'profit comes from the audited statement of changes in equity inside the 30-Jun-2026 '
             'filing. FY2025 gross profit, cost of revenues and finance costs are NOT AVAILABLE from '
             'any obtained official document and are shown blank rather than estimated.')

# ---- quarterly margin path, the evidence behind the crux ----
QPATH = dict(labels=['FY2023', 'FY2024', '9M2025', 'Q4-2025', 'Q1-2026', 'Q2-2026'],
             ebitda_margin=[H['ebitda_margin_fy23'], H['ebitda_margin_fy24'], H['ebitda_margin_9m25'],
                            H['ebitda_margin_q425'], H['ebitda_margin_1q26'], H['ebitda_margin_q226']])

# ---- segment table, H1-2026 versus H1-2025 ----
SEG = dict(
    lines=['Real estate development', 'Commercial and service activities', "Owners' share, hotels",
           'Palm Hills club', 'Other activities', 'Depreciation of fixed assets, Macor'],
    rev_h126=[rev_re_h126, rev_com_h126, rev_hot_h126, rev_clb_h126, rev_oth_h126, 0.0],
    rev_h125=[rev_re_h125, rev_com_h125, 92.024925, 307.675656, rev_oth_h125, 0.0],
    cost_h126=[cost_re_h126, cost_com_h126, 0.0, cost_clb_h126 + dep_clb_h126, 0.0, dep_mac_h126],
    cost_h125=[cost_re_h125, 203.994948, 0.0, 101.076042 + 17.593841, 0.0, 6.390921])
INP['dep_mac_h125'] = I(6.390921, FS26 + ' — note 65 comparative, depreciation of fixed assets Macor',
                        '30-Jun-2025', 'Company')
SEG['margin_h126'] = [1.0 - SEG['cost_h126'][i] / SEG['rev_h126'][i] if SEG['rev_h126'][i] else 0.0
                      for i in range(len(SEG['lines']))]
SEG['margin_h125'] = [1.0 - SEG['cost_h125'][i] / SEG['rev_h125'][i] if SEG['rev_h125'][i] else 0.0
                      for i in range(len(SEG['lines']))]
INP['rev_hot_h125'] = I(92.024925, FS26 + " — note 64 comparative, owners' share hotels", '30-Jun-2025', 'Company')
INP['rev_clb_h125'] = I(307.675656, FS26 + ' — note 64 comparative, Palm Hills club', '30-Jun-2025', 'Company')
INP['cost_com_h125'] = I(203.994948, FS26 + ' — note 65 comparative, commercial and service activity', '30-Jun-2025', 'Company')
INP['cost_clb_h125'] = I(101.076042, FS26 + ' — note 65 comparative, Palm Hills club operation', '30-Jun-2025', 'Company')
INP['dep_clb_h125'] = I(17.593841, FS26 + ' — note 65 comparative, depreciation of club assets', '30-Jun-2025', 'Company')
INP['fin_fy23'] = I(1503.563734, FS24 + ' — comparative finance costs and interests', '31-Dec-2023', 'Company')

# ============================ EXPERT PANEL ===================================
EXP = {}
EXP['e1'] = dict(
    method='Discounted cash flow on the construction-execution driver',
    roic=A['roic'], wacc=W['wacc_cds'], wacc_term=W['wacc_term'],
    vps_A=A_bridge['vps'], vps_B=B_bridge['vps'],
    ev=A['ev'], pv_explicit=A['pv_explicit'], pv_term=A['pv_term'],
    term_share=A['pv_term'] / A['ev'])
EXP['e2'] = dict(
    method='Contracted-book run-off, present value of the disclosed instalment ladder',
    pv_ladder=bk_pv, contract_value=bk_contract, nominal=bk_nominal,
    onbs_nr=nr_st_jun26 + nr_lt_jun26, ar=ar_jun26,
    gross_margin=H['re_gm_h126'])
# expert 2's construction, shown line by line
e2_pv_book = bk_pv                                     # note 72 present value, off balance sheet
e2_onbs = nr_st_jun26 + nr_lt_jun26 + ar_jun26         # already-recognised receivables at PV
e2_cost_to_complete = bk_contract * H['c1']            # build cost still to be spent on that book
e2_landp_to_come = bk_contract * H['c2']
e2_net = e2_pv_book + e2_onbs - adv_jun26 - e2_cost_to_complete * 0.5 - e2_landp_to_come * 0.5
EXP['e2'].update(pv_book=e2_pv_book, onbs=e2_onbs, cost_to_complete=e2_cost_to_complete,
                 landp_to_come=e2_landp_to_come, advances=adv_jun26)
EXP['e2']['equity'] = e2_net - H['netdebt_company'] - eqnci_jun26
EXP['e2']['vps'] = EXP['e2']['equity'] / sh_out
EXP['e3'] = dict(
    method='Return on equity against cost of equity, the book lens taken to its limit',
    roe=H['roe_ltm'], ke=W['ke_cds'], ke_term=W['ke_term'], bvps=H['bvps'],
    pb_spot=L['book']['pb_spot'], pb_norm=L['book']['pb_norm'],
    vps_spot=L['book']['vps_spot'], vps_norm=L['book']['vps_norm'])
EXP['divergence'] = dict(
    e1_vs_e3=EXP['e1']['vps_A'] - EXP['e3']['vps_norm'],
    e1_vs_e2=EXP['e1']['vps_A'] - EXP['e2']['vps'],
    driver='cost of capital and the treatment of the float')

# ============================ ASSERTS ========================================
LOG = []
def A_(cond, msg):
    if not cond:
        raise AssertionError(msg)
    LOG.append('OK  ' + msg)

A_(abs((rev_h126 - cogs_h126 - cashdisc_h126) - gp_h126) < 1e-6,
   'H1-2026 income statement foots: revenue less cost of revenues less cash discount equals gross operating profit')
A_(abs((rev_h125 - cogs_h125 - cashdisc_h125) - gp_h125) < 1e-6,
   'H1-2025 comparative income statement foots to the reported gross operating profit')
A_(abs((rev_fy24 - cogs_fy24 - 97.294493) - gp_fy24) < 1e-5,
   'FY2024 audited income statement foots to the reported gross profit')
A_(abs((rev_re_h126 + rev_com_h126 + rev_hot_h126 + rev_clb_h126 + rev_oth_h126) - rev_h126) < 1e-6,
   'Note 64 revenue by activity foots exactly to the face of the income statement')
A_(abs((cost_re_h126 + cost_com_h126 + cost_clb_h126 + dep_clb_h126 + dep_mac_h126) - cogs_h126) < 1e-6,
   'Note 65 cost of sales by activity foots exactly to the face of the income statement')
A_(abs((sal_h126 + adm_h126) - sga_h126) < 1e-6,
   'Note 66 foots exactly to general administrative, selling and marketing expenses')
A_(abs((land_int_h126 + bank_int_h126) - fin_h126) < 1e-6,
   'Note 67 foots exactly to finance costs and interests')
A_(abs((cumwork_jun26 - cumrelief_jun26) - wip_jun26) < 1e-5,
   'Note 43 foots: total works executed less the cumulative charge to the income statement equals work in progress')
A_(abs((cumwork_dec25 - cumrelief_dec25) - wip_dec25) < 1e-5,
   'Note 43 comparative column foots on the same identity')
A_(abs((cumwork_dec25 + work_h126) - cumwork_jun26) < 1e-5,
   'Work carried out in H1-2026 reconciles the two cumulative works-executed balances')
A_(abs((wip_land_jun26 + wip_constr_jun26) - wip_jun26) < 1e-5,
   'Work in progress splits exactly into land acquisition cost and cost of construction and facilities')
A_(abs((eqtot_jun26 - eqctl_jun26) - eqnci_jun26) < 1e-6,
   'Equity splits exactly into controlling and non-controlling interests')
A_(abs((tl_jun26 + eqtot_jun26) - ta_jun26) < 1e-5,
   'The 30-Jun-2026 balance sheet balances: total liabilities plus equity equals total assets')
A_(abs((tl_dec25 + eqtot_dec25) - ta_dec25) < 1e-5,
   'The 31-Dec-2025 comparative balance sheet balances on the same identity')
A_(abs((sh_issued - sh_treasury) - sh_out) < 1e-6,
   'Note 62 foots: issued shares less treasury shares equals outstanding shares')
A_(abs((cf_jun26 + (loan_st_jun26 + loan_lt_jun26) + bank_cr_jun26 + (lease_st_jun26 + lease_lt_jun26))
       - intdebt_jun26) < 1e-3,
   "Note 34's interest-bearing obligations rebuild exactly from the four balance-sheet debt lines")
A_(abs((np_st_jun26 + np_lt_jun26) - H['np_total_jun26']) < 1e-9,
   'Notes payable rebuild from their short and long-term halves')
A_(abs(sum(bk_ladder) - bk_nominal) < 1.0,
   'The note 72 maturity ladder foots to the nominal value of the off-balance-sheet notes receivable')
A_(abs(sum(bk_ladder_pv) - bk_pv) < 1.0,
   'The note 72 present-value ladder foots to the disclosed present value')
A_(abs((np_h126 + nci_h126) - (pbt_h126 - curtax_h126 - deftax_h126)) < 1e-5,
   'Attributable profit plus the non-controlling share equals profit after tax')
A_(abs(np_h126 / wavg_sh_h126 - eps_h126) < 5e-4,
   'Reported earnings per share reproduce from attributable profit and the weighted average share count')
A_(H['constr_relief_h126'] > 0 and H['land_partner_h126'] > 0,
   'Both cost blocks inside the cost of real estate development are economically possible (each strictly positive)')
A_(abs((H['constr_relief_h126'] + H['land_partner_h126']) - cost_re_h126) < 1e-6,
   'The two cost blocks foot exactly to the disclosed cost of real estate development')
A_(abs(H['re_gm_h126'] - (1.0 - H['c1'] - H['c2'])) < 1e-12,
   'The real-estate gross margin is an output of the two cost rates, not an input')
for lbl, comp, pub in (('FY2023', H['ebitda_fy23'], 3440.0), ('FY2024', H['ebitda_fy24'], 5894.0),
                       ('H1-2025', H['ebitda_h125'], 4459.0), ('H1-2026', H['ebitda_h126'], 4100.0)):
    A_(abs(comp / pub - 1.0) < 0.012,
       'The recovered EBITDA definition reproduces the company\'s own published %s figure to within 1.2%%' % lbl)
A_(W['kd_marginal'] > rf_obs,
   'The marginal cost of debt sits above the local sovereign yield, as the cost-of-capital rule requires')
A_(W['rf_star_rating'] < rf_obs and W['rf_star_cds'] < rf_obs,
   'The risk-free rate is normalised downward by the sovereign default spread on both bases')
A_(abs(erp_rating - crp_rating - (erp_cds - (erp_cds - 0.0421))) < 0.02,
   'The two equity risk premium bases imply the same mature-market premium to within two decimal points')
A_(W['we'] + W['wd'] == 1.0 or abs(W['we'] + W['wd'] - 1.0) < 1e-12,
   'The capital-structure weights sum to one')
A_(A['ev'] > B['ev'],
   'The framing that treats the float as enterprise funding values the firm above the framing that does not')
A_(all(f > 0 for f in DCF['framing_A']['df']),
   'Every discount factor is positive')
A_(term_g < W['wacc_term_glide'] and term_g < W['wacc_term_spot'],
   'Terminal growth sits below the terminal cost of capital under both cost-of-capital framings')
A_(0.0 <= A['reinv'] <= 0.95,
   'The terminal reinvestment rate implied by the model\'s own return on capital is inside its bounds')
A_(abs(H['mktcap'] - spot * sh_out) < 1e-9,
   'Market capitalisation is the published spot times the ex-treasury share count')

# beta provenance, inspected on the record rather than trusted from a flag
import beta_regression, research_protocol
_beta_rec = beta_regression.own_stock_beta('PHDC', 'EG', 'EGX')
research_protocol.assert_beta_provenance(_beta_rec)
A_(abs(_beta_rec['beta'] - beta_val) < 1e-12,
   'The beta in the register is the value the sanctioned resolver returns, not a transcription')
A_('raw_indices/' in _beta_rec['index_file'],
   'The regressor is the published exchange index read from raw_indices, not a constituent composite')
A_(_beta_rec['interim_note'] is None,
   'No interim-index disclosure applies to the Egyptian Exchange')
A_(_beta_rec['usable'] and _beta_rec['conforming'],
   'The own-stock regression clears the usability gate, so tier 1 stands and no fallback is needed')
LOG.append('OK  beta provenance asserted on the resolver record: %s, as of %s'
           % (_beta_rec['index_file'], _beta_rec['index_asof']))

A_(abs(H['ebitda_def_gap_h125']) < 0.005,
   'The EBITDA definition recovered from the statements (gross profit less administrative and selling '
   'cost less expected credit losses) reproduces the only published figure whose components the '
   'statements disclose — H1-2025 — to within half a percentage point')
A_(abs(H['ebitda_recon_gap']) < 0.05,
   'The model\'s first forecast period reproduces the last reported half-year at the income-statement '
   'level to within 5%%, once the disclosed capitalised interest is added back and the modelled '
   'sequential growth is applied')
A_(H['ufcf_h126_actual'] < H['ufcf_h126_like_for_like'],
   'Both bridging items are cash outflows in the reported half-year, so the like-for-like figure is the higher one')
A_(H['ufcf_h226_model_A'] > 0 and H['ufcf_h126_actual'] > 0,
   'Unlevered cash flow is positive both in the reported half-year and in the first forecast period '
   'under the base framing')
A_(DCF['framing_A']['pv_term'] / DCF['framing_A']['ev'] < 0.80,
   'The terminal value is under four-fifths of enterprise value in the base framing')
A_(GDV['spread_spot'] < 0,
   'Measured on all the capital standing in the business, the return sits below the spot cost of '
   'capital — the study publishes that figure rather than only the flattering one')
A_(GDV['roic_ex_float'] > GDV['wacc_term'],
   'Measured net of the customer money funding the work, the return sits above the normalised cost '
   'of capital — the other half of the same fact, published beside it')
A_(GDV['growth_sign_A'] > 0 and GDV['growth_sign_B'] > 0,
   'The full model, which carries the terminal value the one-year break-even arithmetic cannot, '
   'values more volume higher under BOTH framings — the direction the prose states')
A_(GDV['ic_end_ex_float'] < GDV['ic_end'] * 0.5,
   'Over half the capital in the business is customer money, which is why the two return measures '
   'differ so widely')
A_(abs(SLIDER['geo_implied_hit'] - SLIDER['geo_hit']) < 5e-4,
   'Reading the security lever back through the page\'s own formula recovers the conditional '
   'event size the model measured, so the lever is not merely plausible but arithmetically right')
A_(abs(SLIDER['launch_implied_hit'] - SLIDER['launch_hit']) < 5e-4,
   'The launch lever recovers its measured conditional gain on the same round trip')
A_(abs(sum(SEG['rev_h126']) - rev_h126) < 1e-6,
   'The segment revenue table foots exactly to the face of the income statement')
A_(abs(sum(SEG['cost_h126']) - cogs_h126) < 1e-6,
   'The segment cost table foots exactly to the face of the income statement, including the '
   'depreciation line note 65 carries separately from the five activities')
A_(abs(sum(SEG['cost_h125']) - cogs_h125) < 1e-6,
   'The comparative segment cost table foots on the same identity')

# every input carries all four fields
for k, v in INP.items():
    A_(set(v) == {'value', 'source', 'date', 'ring'} and v['source'] and v['date'] and v['ring'],
       'Register entry %s is four-field complete' % k) if False else None
_bad = [k for k, v in INP.items() if set(v) != {'value', 'source', 'date', 'ring'}
        or not v['source'] or not v['date'] or not v['ring']]
A_(not _bad, 'Every one of the %d register entries is four-field complete (value, source, date, layer)' % len(INP))

# ============================ EMIT ===========================================
OUT = dict(
    meta=dict(ticker='PHDC', name='Palm Hills Developments Company S.A.E', exchange='EGX',
              code='EGX:PHDC', ccy='EGP', units='EGP mn unless stated',
              edition='Fundamental refresh, 19-Aug-2026', supersedes='11-Jun-2026 edition',
              valuation_date='2026-06-30', publication_date='2026-08-19',
              spot=spot, spot_date='22-Jul-2026', shares_out=sh_out, shares_issued=sh_issued,
              mktcap=H['mktcap'], auditor='Forvis Mazars Mostafa Shawki',
              review_date='17-Aug-2026'),
    inputs=INP, hist=H, wacc=W, dcf=DCF, lenses=L, synthesis=SYN, sens=SENS,
    published_fair=dict(bear=SYN['bear'], base=SYN['base'], full=SYN['bull'],
                        bear_source='four-lens synthesis under framing B (float restricted)',
                        base_source='four-lens synthesis under framing A (float is operating funding)',
                        full_source='four-lens upper bound under framing A'),
    variance=VARIANCE, experts=EXP, peers=peers, prior=PR,
    gdv=GDV, hist3=HIST3, qpath=QPATH, segments=SEG, slider=SLIDER,
    beta_record=_beta_rec, assert_log=LOG,
    carry_forward=dict(
        note='Sections 2 and 3 reproduce the last published technical read and probabilistic map '
             'unchanged. This refresh touches fundamentals only.',
        asof_mc_data='2026-07-22', asof_mc_computed='2026-07-28',
        asof_tech_data='2026-07-22', asof_tech_computed='2026-08-17',
        spot=15.01, spot_date='close 22 Jul 2026',
        dist=dict(t20=dict(label='1 month', p5=12.89, p25=14.32, p50=15.23, p75=16.22, p95=18.01,
                           resolve='2026-08-23'),
                  t60=dict(label='3 months', p5=11.52, p25=14.01, p50=15.72, p75=17.59, p95=21.39,
                           resolve='2026-10-22')),
        touch=[[20.00, 1, 15], [18.50, 5, 28], [17.50, 12, 42], [16.50, 31, 62], [15.55, 66, 83]],
        levels=dict(res=[16.08, 16.43, 17.0], sup=[14.85, 14.34, 13.01]),
        tech=dict(trend='Trading above the whole moving-average stack, on a rising 200-day')),
)

def _jsonable(o):
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    raise TypeError(str(type(o)))

with open('study_numbers.json', 'w') as f:
    json.dump(OUT, f, indent=1, default=_jsonable)

print('study_numbers.json written — %d register entries, %d asserts passed' % (len(INP), len(LOG)))
print('  H1-2026 revenue %.0f  gross margin %.2f%%  EBITDA %.0f (%.2f%%)'
      % (rev_h126, H['gm_h126'] * 100, H['ebitda_h126'], H['ebitda_margin_h126'] * 100))
print('  crux P = %.4f  c1 = %.4f  c2 = %.4f  RE gross margin %.2f%%'
      % (H['P_h126'], H['c1'], H['c2'], H['re_gm_h126'] * 100))
print('  beta %.4f  rf %.3f%%  rf* %.3f%%/%.3f%%  Ke %.2f%%/%.2f%%  Kd %.2f%%'
      % (beta_val, rf_obs * 100, W['rf_star_rating'] * 100, W['rf_star_cds'] * 100,
         W['ke_rating'] * 100, W['ke_cds'] * 100, W['kd_marginal'] * 100))
print('  WACC spot %.2f%% (rating) / %.2f%% (CDS)   terminal %.2f%%'
      % (W['wacc_rating'] * 100, W['wacc_cds'] * 100, W['wacc_term'] * 100))
print('  DCF  A glide %.2f  B glide %.2f  |  A spot %.2f  B spot %.2f'
      % (A_bridge['vps'], B_bridge['vps'], A_spot_bridge['vps'], B_spot_bridge['vps']))
print('  lenses  dcf %.2f-%.2f  book %.2f-%.2f  rel %.2f-%.2f  norm %.2f-%.2f'
      % (L['dcf']['low'], L['dcf']['high'], L['book']['low'], L['book']['high'],
         L['relative']['low'], L['relative']['high'], L['normalised']['low'], L['normalised']['high']))
print('  synthesis A  bear %.2f base %.2f bull %.2f | synthesis B  bear %.2f base %.2f bull %.2f'
      % (SYN_A['bear'], SYN_A['base'], SYN_A['bull'], SYN_B['bear'], SYN_B['base'], SYN_B['bull']))
print('  PUBLISHED  bear %.2f  base %.2f  full %.2f   (spot %.2f, base %+.1f%%)'
      % (SYN['bear'], SYN['base'], SYN['bull'], spot, SYN['upside_base'] * 100))
print('  reconciliation: EBITDA gap %.2f%%; H1-2026 actual unlevered cash flow %.0f, like-for-like %.0f, '
      'H2-2026E model A %.0f (residual %.0f)'
      % (H['ebitda_recon_gap'] * 100, H['ufcf_h126_actual'], H['ufcf_h126_like_for_like'],
         H['ufcf_h226_model_A'], H['recon_residual']))
print('  slider refit: ' + ' | '.join('%s def %.4g imp %+.5g' % (l['key'], l['default'], l['impact']) for l in SLIDER['levers']))
print('  growth: ROIC %.2f%% gross / %.2f%% ex-float vs spot WACC %.2f%% and terminal WACC %.2f%%; '
      'static break-even %.1f%% without the float, %.1f%% with it; full-model growth sign A %+.2f B %+.2f'
      % (GDV['roic_A'] * 100, GDV['roic_ex_float'] * 100, GDV['wacc_spot'] * 100,
         GDV['wacc_term'] * 100, GDV['breakeven_g_no_float'] * 100,
         GDV['breakeven_g_with_float'] * 100, GDV['growth_sign_A'], GDV['growth_sign_B']))
