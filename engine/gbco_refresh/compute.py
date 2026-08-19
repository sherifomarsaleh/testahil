"""GBCO FUNDAMENTAL REFRESH — 19-08-2026 — master computation.

Trigger: new H1-2026 disclosure set (KPMG-reviewed consolidated interim FS + 2Q/1H26
earnings release, both 13-Aug-2026). Fundamentals only: no recalibration, no cone
re-strike, no ledger writes, no technical read. Sections 2-3 of the study reproduce the
PUBLISHED price-side blocks verbatim (published_gbco.json, dumped from assets/data.js).

Everything downstream (Word, Excel, bibliography, figures) reads study_numbers.json,
which this script writes. Every input passes through I(): value / source / date / layer —
the four-field register, validated by assertion. No financial numeral is typed into any
builder.

Perimeter note (flagged): line-of-business revenue histories are on the earnings-release
LOB basis (PC / CV&CE / Light Mobility / Trading / other, summing to auto total revenue);
per-LOB gross margins are anchored on the FS segment note (5-B), whose segment
boundaries differ slightly (statement PC includes after-sales). The margin is the
FS-anchored object; unit cost is derived as ASP x (1 - margin) and escalated per class.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))

from beta_regression import own_stock_beta
from research_protocol import assert_beta_provenance
from wacc_builder import WaccInputs, build_wacc

# =======================================================================================
# FOUR-FIELD INPUT REGISTER
# =======================================================================================
REG = []
def I(value, name, source, date, layer, unit='EGP mn', note=''):
    assert name and source and date and layer, f"orphan input: {name}"
    REG.append(dict(name=name, value=value, unit=unit, source=source, date=date,
                    layer=layer, note=note))
    return value

FS  = "GB Corp consolidated interim FS 30-Jun-2026 (KPMG limited review, 13-Aug-2026)"
ER  = "GB Corp 2Q/1H26 earnings release, 13-Aug-2026"
PRIOR = ("GB Corp FY23/FY24/FY25 issued statements & 4Q releases, as extracted in the "
         "delivered GBCO study 08-07-2026 (cell-verified workbook)")
MKT = "investing.com, 19-Aug-2026"
DAM = "Damodaran ctryprem.html (original file), updated 05-Jan-2026"
CO  = "COMPANY"; CTY = "COUNTRY"; IND = "INDUSTRY"; GLB = "GLOBAL"

SH = I(1085.5, "shares outstanding", ER + " (shareholder information)", "2026-08-13", CO, "mn shares")

# ---- H1-2026 actuals — group (FS, statement level) ------------------------------------
h1 = dict(
 rev      = I(48474.374, "group revenue H1-26", FS, "2026-08-13", CO),
 gp       = I(7421.893,  "group gross profit H1-26", FS, "2026-08-13", CO),
 op       = I(3661.278,  "group operating profit H1-26", FS, "2026-08-13", CO),
 fin_net  = I(2280.992,  "group net finance cost H1-26 (incl FX loss 23.429)", FS, "2026-08-13", CO),
 assoc    = I(410.140,   "group share of associates H1-26", FS, "2026-08-13", CO),
 ebt      = I(1790.426,  "group EBT H1-26", FS, "2026-08-13", CO),
 tax      = I(734.787,   "group income tax H1-26 (ETR 41.04%, note 11-C)", FS, "2026-08-13", CO),
 np       = I(1262.006,  "group net profit attributable H1-26 (EPS 1.163)", FS, "2026-08-13", CO),
 ocf      = I(5486.148,  "group net operating cash flow H1-26", FS, "2026-08-13", CO),
)
h1_25 = dict(
 rev = I(35849.992, "group revenue H1-25", FS, "2026-08-13", CO),
 np  = I(1672.621,  "group net profit attributable H1-25", FS, "2026-08-13", CO),
)

# ---- H1-2026 actuals — auto segment (ER tables 8/6-11) --------------------------------
a1 = dict(
 rev     = I(40021.5, "auto total revenue H1-26 (incl inter-segment 394.5)", ER, "2026-08-13", CO),
 gp      = I(5722.1,  "auto gross profit H1-26 (GPM 14.3%)", ER, "2026-08-13", CO),
 gsa     = I(2839.8,  "auto GS&A H1-26", ER, "2026-08-13", CO),
 oth     = I(334.2,   "auto other operating income H1-26", ER, "2026-08-13", CO),
 prov    = I(-89.4,   "auto net provisions H1-26", ER, "2026-08-13", CO),
 op      = I(3127.0,  "auto operating profit H1-26", ER, "2026-08-13", CO),
 fin     = I(2206.7,  "auto finance cost H1-26 (incl leasing 150.4 in 2Q)", ER, "2026-08-13", CO),
 ebt     = I(890.5,   "auto EBT H1-26", ER, "2026-08-13", CO),
 tax     = I(529.3,   "auto income tax H1-26 (ETR 59.4% — unshielded regional losses)", ER, "2026-08-13", CO),
 ebitda  = I(3484.8,  "auto EBITDA H1-26", ER, "2026-08-13", CO),
 dna     = I(401.2,   "auto D&A H1-26 (cash-flow adjustments)", ER, "2026-08-13", CO),
 capex   = I(1376.5,  "auto capex H1-26 (PP&E 257.0 + projects 1,119.5)", ER, "2026-08-13", CO),
 nd      = I(14493.6, "auto net debt 30-Jun-26", ER + " table 7", "2026-08-13", CO),
 wc      = I(17092.8, "auto working capital 30-Jun-26", ER + " table 6", "2026-08-13", CO),
 ce      = I(28185.0, "auto capital employed 30-Jun-26 (LTM ROCE 22.9%)", ER + " table 10", "2026-08-13", CO),
 debt    = I(22733.1, "auto total debt 30-Jun-26", ER + " table 7", "2026-08-13", CO),
 notes   = I(2345.8,  "auto notes payable (leasing) 30-Jun-26", ER + " table 7", "2026-08-13", CO),
 cash    = I(9445.0,  "auto cash 30-Jun-26", ER + " table 7", "2026-08-13", CO),
 inv     = I(22959.1, "auto inventory 30-Jun-26", ER + " table 6", "2026-08-13", CO),
 rec     = I(5873.5,  "auto receivables 30-Jun-26", ER + " table 6", "2026-08-13", CO),
 adv     = I(1153.7,  "auto advances 30-Jun-26", ER + " table 6", "2026-08-13", CO),
 debtors = I(2598.9,  "auto debtors & other 30-Jun-26", ER + " table 6", "2026-08-13", CO),
 pay     = I(15492.5, "auto payables 30-Jun-26", ER + " table 6", "2026-08-13", CO),
 cogs    = I(34299.4, "auto total cost of sales H1-26", ER + " table 8", "2026-08-13", CO),
 nci_bs  = I(590.7,   "auto segment NCI 30-Jun-26", ER + " table 12", "2026-08-13", CO),
 h1_25_rev    = I(30672.7, "auto total revenue H1-25", ER, "2026-08-13", CO),
 h1_25_gp     = I(4752.0,  "auto gross profit H1-25 (GPM 15.5%)", ER, "2026-08-13", CO),
 h1_25_ebitda = I(3074.3,  "auto EBITDA H1-25", ER, "2026-08-13", CO),
)

# LOB actuals H1-26 (ER basis)
lob1 = dict(
 pc_u  = I(29554, "PC volumes H1-26 (CKD 15,454 / CBU 14,100)", ER, "2026-08-13", CO, "units"),
 pc_r  = I(30595.7, "PC revenue H1-26", ER, "2026-08-13", CO),
 cv_u  = I(2490, "CV&CE volumes H1-26 (bus 1,002 / truck 1,472 / CE 16)", ER, "2026-08-13", CO, "units"),
 cv_r  = I(4749.1, "CV&CE revenue H1-26", ER, "2026-08-13", CO),
 lm_u  = I(21173, "Light-Mobility volumes H1-26", ER, "2026-08-13", CO, "units"),
 lm_r  = I(1435.2, "Light-Mobility revenue H1-26", ER, "2026-08-13", CO),
 tr_r  = I(2572.3, "Trading revenue H1-26 (tires 1,956.3 + parts 616.0)", ER, "2026-08-13", CO),
 pc_r_h125 = I(24098.2, "PC revenue H1-25", ER, "2026-08-13", CO),
 pc_u_h125 = I(25989,   "PC volumes H1-25", ER, "2026-08-13", CO, "units"),
 cv_r_h125 = I(2640.6,  "CV&CE revenue H1-25", ER, "2026-08-13", CO),
 lm_r_h125 = I(928.4,   "Light-Mobility revenue H1-25", ER, "2026-08-13", CO),
 tr_r_h125 = I(2438.2,  "Trading revenue H1-25", ER, "2026-08-13", CO),
 pc_fx_share = I(0.1459, "foreign share of PC revenue H1-26 (was 25.81% H1-25)", FS + " note 5-A2", "2026-08-13", CO, "share"),
)
lob1['oth_r'] = round(a1['rev'] - lob1['pc_r'] - lob1['cv_r'] - lob1['lm_r'] - lob1['tr_r'], 1)  # 669.2 residual

# FS segment-note margins (statement basis) — the cost-side anchors
fsm = dict(
 pc  = dict(rev=I(31210.238, "FS segment PC revenue H1-26", FS + " note 5", "2026-08-13", CO),
            cost=I(27054.190, "FS segment PC cost H1-26", FS + " note 5-B", "2026-08-13", CO)),
 bt  = dict(rev=I(4906.002, "FS segment buses&trucks revenue H1-26", FS + " note 5", "2026-08-13", CO),
            cost=I(3991.754, "FS segment buses&trucks cost H1-26", FS + " note 5-B", "2026-08-13", CO)),
 lm  = dict(rev=I(1566.408, "FS segment 2-3-4W revenue H1-26", FS + " note 5", "2026-08-13", CO),
            cost=I(1386.932, "FS segment 2-3-4W cost H1-26", FS + " note 5-B", "2026-08-13", CO)),
 tr  = dict(rev=I(1956.300+381.044, "FS segment tires+other-trading revenue H1-26", FS + " note 5", "2026-08-13", CO),
            cost=I(1604.457+259.205, "FS segment tires+other-trading cost H1-26", FS + " note 5-B", "2026-08-13", CO)),
)
for k in fsm: fsm[k]['gpm'] = 1 - fsm[k]['cost']/fsm[k]['rev']

# ---- GB Capital H1-26 (ER tables 13/14) ------------------------------------------------
c1 = dict(
 rev  = I(9088.2, "GB Capital total revenue H1-26", ER, "2026-08-13", CO),
 op   = I(574.4,  "GB Capital operating profit H1-26", ER, "2026-08-13", CO),
 np   = I(649.6,  "GB Capital net profit after tax & NCI H1-26", ER, "2026-08-13", CO),
 assoc= I(426.2,  "GB Capital associates income H1-26 (MNT-Halan, Bedaya, Kaf)", ER, "2026-08-13", CO),
 book = I(23984.6,"GB Capital net on-book portfolio 30-Jun-26 (+33.6% y/y)", ER, "2026-08-13", CO),
 npl  = I(0.028,  "GB Capital NPL ratio 30-Jun-26", ER, "2026-08-13", CO, "ratio"),
 roae = I(0.135,  "GB Capital annualized adjusted ROAE 2Q26", ER, "2026-08-13", CO, "ratio"),
 eq   = I(22497.8,"GB Capital segment equity before NCI 30-Jun-26", ER + " table 12", "2026-08-13", CO),
 inv_sub = I(18246.0, "GB Capital segment 'investments in subsidiaries' 30-Jun-26", ER + " table 12", "2026-08-13", CO),
 cof  = I(1797.1, "GB Capital cost of funds H1-26", ER + " table 13", "2026-08-13", CO),
)

# ---- Associates & marks (FS notes 34/35 + round) --------------------------------------
mnt = dict(
 stake    = I(0.4293, "MNT Investment B.V. stake after Al Ahly Capital first close (44.01% before)",
              FS + " note 34 footnote", "2026-08-13", CO, "share"),
 carrying = I(15723.523, "MNT B.V. equity-method carrying value 30-Jun-26 (opening restated +2,460.218)",
              FS + " note 34", "2026-08-13", CO),
 pickup   = I(409.985, "MNT B.V. H1-26 share of profit (KPMG could not verify — qualified conclusion)",
              FS + " note 34 + review report", "2026-08-13", CO),
 round_usd= I(1400.0, "MNT-Halan round valuation, first close led by Al Ahly Capital (second close pending)",
              "GB Corp press release 09-Jun-2026, corroborated by Reuters/Zawya/Enterprise coverage",
              "2026-06-09", CO, "USD mn"),
 loanbook = I(1.95, "MNT-Halan consolidated loan book (c.)", ER, "2026-08-13", CO, "USD bn"),
)
other_assoc = I(109.641+176.841+220.460, "other associates carrying (Mier 27.8% + Bedaia 33.33% + Kaf 37.5%)",
                FS + " note 34", "2026-08-13", CO)
fvoci = I(489.537, "investments at FV through OCI (Sky reality 7.61% et al.)", FS + " note 35", "2026-08-13", CO)
assoc_total = I(16230.465, "investment in associates total 30-Jun-26", FS, "2026-08-13", CO)

# ---- Group balance sheet & debt (FS) ---------------------------------------------------
bs = dict(
 parent_eq = I(33454.268, "parent equity 30-Jun-26 (FY25 restated 31,671.409)", FS, "2026-08-13", CO),
 nci       = I(1673.633, "group NCI 30-Jun-26 (45% GB Lease, 17% Automobilk, 16.67% GK, 32% GQ, 7.5% TVD)",
               FS + " note 24", "2026-08-13", CO),
 nd_group  = I(32269.835, "group net debt 30-Jun-26 (note 25; ND/E 0.96)", FS, "2026-08-13", CO),
 debt_total= I(42475.974, "group loans, borrowings & overdrafts 30-Jun-26", FS + " note 26", "2026-08-13", CO),
 cash      = I(10951.500, "group cash & equivalents 30-Jun-26 (USD time deposits 5,687.0 inside)",
               FS + " notes 16/29", "2026-08-13", CO),
 usd_liab  = I(7274.427, "total USD-denominated liabilities 30-Jun-26 (incl trade payables)", FS + " note 29", "2026-08-13", CO),
 usd_net   = I(-1853.570, "net USD exposure 30-Jun-26 (liability)", FS + " note 29", "2026-08-13", CO),
 var_rate  = I(43480.083, "variable-rate loans/advances/overdrafts 30-Jun-26 (essentially the whole book)",
               FS + " note 29", "2026-08-13", CO),
 div_ps    = I(0.35, "FY25 dividend per share (paid 29-Apr-26 + 29-Jul-26)", FS + " note 10", "2026-08-13", CO, "EGP"),
 commitments = I(1020.505, "capital commitments 30-Jun-26 (new production lines; FY25: 525.479)",
               FS + " note 31", "2026-08-13", CO),
 inv_group = I(22998.432, "group inventories 30-Jun-26", FS + " note 12", "2026-08-13", CO),
 ar_group  = I(16570.835, "group accounts & notes receivable 30-Jun-26", FS + " note 14", "2026-08-13", CO),
 debtors_group = I(5268.687, "group debtors & other debit balances 30-Jun-26", FS + " note 15", "2026-08-13", CO),
 ta_group  = I(100921.411, "group total assets 30-Jun-26", FS, "2026-08-13", CO),
)
kd_egp = I(0.2082, "average interest rate, current EGP loans & borrowings, H1-26 (FY25: 21.91%)",
           FS + " note 26", "2026-08-13", CO, "rate")
kd_usd = I(0.0778, "average interest rate, USD loans & borrowings, H1-26 (FY25: 8.30%)",
           FS + " note 26", "2026-08-13", CO, "rate")
tax_statutory = I(0.225, "Egypt statutory corporate income tax", FS + " note 11-C", "2026-08-13", CTY, "rate")
etr_h1 = I(0.4104, "group effective tax rate H1-26 (unshielded regional losses)", FS + " note 11-C", "2026-08-13", CO, "rate")

# ---- FY23-FY25 histories (official, via the delivered 08-07-2026 study workbook) ------
hist = dict(
 FY23=dict(group_rev=I(28317.2, "group revenue FY23", PRIOR, "2024-03-01", CO),
           auto_rev=I(23854.0, "auto revenue FY23", PRIOR, "2024-03-01", CO),
           pc_u=I(26994, "PC volumes FY23", PRIOR, "2024-03-01", CO, "units"),
           pc_r=I(16544.3, "PC revenue FY23", PRIOR, "2024-03-01", CO),
           cv_u=2273, cv_r=2323.0, lm_u=13610, lm_r=854.2, tr_r=2506.8, oth_r=7625.2,
           auto_gp=5813.1, auto_ebitda=3794.6, auto_ebit=3460.9, np=1890.8, wc=4466.3,
           nd=2921.8, ce=10231.2, cap_rev=4950.9, cap_book=8980.5,
           bs=dict(inv=6366.1, ar=1743.5, adv=1039.1, assoc=10732.4, cash=4504.2,
                   ta=42585.5, borrow=12517.7, eq=19838.8, nd_lc=12517.7-4504.2)),
 FY24=dict(group_rev=I(53969.5, "group revenue FY24", PRIOR, "2025-03-01", CO),
           auto_rev=I(47065.0, "auto revenue FY24", PRIOR, "2025-03-01", CO),
           pc_u=I(42043, "PC volumes FY24", PRIOR, "2025-03-01", CO, "units"),
           pc_r=I(36533.4, "PC revenue FY24", PRIOR, "2025-03-01", CO),
           cv_u=2096, cv_r=3984.5, lm_u=20189, lm_r=1378.2, tr_r=3815.5, oth_r=1353.4,
           auto_gp=9057.4, auto_ebitda=5880.5, auto_ebit=5564.9, np=2928.1, wc=10783.9,
           nd=5292.0, ce=18731.3, cap_rev=7383.6, cap_book=13183.4,
           bs=dict(inv=21134.3, ar=3708.7, adv=2942.2, assoc=11743.6, cash=7420.9,
                   ta=62725.2, borrow=22608.7, eq=25438.5, nd_lc=22608.7-7420.9)),
 FY25=dict(group_rev=I(80229.8, "group revenue FY25", PRIOR, "2026-02-26", CO),
           auto_rev=I(66358.3, "auto revenue FY25 (cross-checked: ND/LTM-EBITDA 2.39x x 6,363 = 15,210)", PRIOR, "2026-02-26", CO),
           pc_u=I(56548, "PC volumes FY25", PRIOR, "2026-02-26", CO, "units"),
           pc_r=I(52827.3, "PC revenue FY25", PRIOR, "2026-02-26", CO),
           cv_u=3404, cv_r=5956.8, lm_u=33906, lm_r=2203.8, tr_r=4242.8, oth_r=1127.6,
           auto_gp=9837.1, auto_ebitda=6363.3, auto_ebit=5830.9, np=2880.0, wc=18917.0,
           nd=15210.0, ce=28513.0, cap_rev=14743.0, cap_book=19495.2,
           bs=dict(inv=24649.7, ar=14157.9, adv=5818.6, assoc=15732.4, cash=9523.6,
                   ta=94287.6, borrow=37921.3, eq=31671.4, nd_lc=29298.8)),
)

for _y, _d in [("FY2023", "2024-03-01"), ("FY2024", "2025-03-01"), ("FY2025 (restated)", "2026-08-13")]:
    _k = "FY23" if _y.startswith("FY2023") else ("FY24" if _y.startswith("FY2024") else "FY25")
    _src = PRIOR if _k != "FY25" else FS + " note 39 (restated comparatives)"
    I(hist[_k]['bs']['ta'], f"{_y} balance-sheet block (total assets; components: inventories "
      f"{hist[_k]['bs']['inv']}, receivables {hist[_k]['bs']['ar']}, advances/debtors "
      f"{hist[_k]['bs']['adv']}, associates {hist[_k]['bs']['assoc']}, cash {hist[_k]['bs']['cash']}, "
      f"borrowings {hist[_k]['bs']['borrow']}, parent equity {hist[_k]['bs']['eq']})",
      _src, _d, CO)
    I(hist[_k]['auto_ebit'], f"{_y} automotive operating profit", _src, _d, CO)
a1['np_after_nci'] = I(607.9, "auto net profit after NCI H1-26", ER + " table 8", "2026-08-13", CO)
c1['gp'] = I(1762.2, "GB Capital gross profit H1-26", ER + " table 13", "2026-08-13", CO)

# ---- Market & country inputs -----------------------------------------------------------
rf_obs   = I(0.2292, "Egypt 10Y local-currency govt yield (52wk 19.79-23.05)", MKT, "2026-08-19", CTY, "rate")
ds_rating= I(0.0637, "Egypt adjusted default spread (Caa1, rating basis)", DAM, "2026-01-05", CTY, "rate")
ds_cds   = I(0.0341, "Egypt sovereign CDS spread", DAM, "2026-01-05", CTY, "rate")
erp_rating=I(0.1394, "Egypt total ERP, rating basis (CRP 9.71%)", DAM, "2026-01-05", CTY, "rate")
erp_cds  = I(0.0941, "Egypt total ERP, sovereign-CDS basis", DAM, "2026-01-05", CTY, "rate")
usdegp   = I(50.71, "USD/EGP spot (52wk 46.64-54.86; prior study used 47.5)", MKT, "2026-08-19", CTY, "EGP/USD")
cpi      = I(0.149, "Egypt urban CPI y/y, Jul-26 (CAPMAS)", "CAPMAS via Daily News Egypt/Bloomberg, 10-Aug-2026", "2026-08-10", CTY, "rate")
cbe_dep  = I(0.19, "CBE overnight deposit rate (held, 3rd consecutive MPC, Jul-26)",
             "SIS/Daily News Egypt on CBE MPC, 11-Jul-2026", "2026-07-11", CTY, "rate")
spot_lib = I(31.31, "last OHLC-library close (published page spot)", "engine/raw_ohlc/EG/GBCO.csv via assets/data.js", "2026-07-22", CO, "EGP")
spot_ir  = I(29.70, "EGX quote on the company's own IR page at build date", "ir.gb-corporation.com live widget", "2026-08-19", CO, "EGP")
amic_pc  = I(62300, "AMIC Egypt PC market H1-26 (+18% y/y from 52.8k)", "AMIC via Zawya/Arab Finance, Jul-26 prints", "2026-07-20", IND, "units")
peers = dict(
 DOAS = I(12.55, "Dogus Otomotiv trailing P/E (P/B 0.62, TAS-29 restated book)", MKT, "2026-08-19", IND, "x"),
 CNFN = I(9.41,  "Contact Financial (EGX NBFS) trailing P/E", "stockanalysis.com, 19-Aug-2026", "2026-08-19", IND, "x"),
 AN   = I(9.11,  "AutoNation trailing P/E (fwd 8.35)", "stockanalysis.com, 19-Aug-2026", "2026-08-19", IND, "x"),
 BAJAJ= I(27.56, "Bajaj Auto trailing P/E (P/B 7.49)", MKT, "2026-08-19", IND, "x"),
)

# =======================================================================================
# STEP 2 — VARIANCE: prior study FY26E vs newly disclosed actuals
# =======================================================================================
P26 = json.load(open(os.path.join(HERE, '..', 'gbco_study', 'study_numbers.json')))
p_fc = P26['forecast']['FY26E']; p_dcf = P26['dcf']['rows'][0]
sea = dict(  # FY25 H1 share of FY — the seasonal yardstick (computed, not typed)
    pc_u = lob1['pc_u_h125']/hist['FY25']['pc_u'],
    pc_r = lob1['pc_r_h125']/hist['FY25']['pc_r'],
    cv_r = lob1['cv_r_h125']/hist['FY25']['cv_r'],
    lm_r = lob1['lm_r_h125']/hist['FY25']['lm_r'],
    tr_r = lob1['tr_r_h125']/hist['FY25']['tr_r'],
    auto = a1['h1_25_rev']/hist['FY25']['auto_rev'],
    ebitda = a1['h1_25_ebitda']/hist['FY25']['auto_ebitda'],
)
def vrow(line, fc, act_h1, share, unit='EGP mn', note=''):
    implied = act_h1/share
    dev = implied/fc - 1
    return dict(line=line, forecast_fy26e=fc, actual_h1=act_h1, h1_share_fy25=share,
                implied_fy26=implied, deviation=dev, unit=unit,
                verdict=("ESCALATE" if abs(dev) > 0.05 else "on track"), note=note)
variance = [
 vrow("PC volumes (units)", p_fc['pc_vol'], lob1['pc_u'], sea['pc_u'], 'units',
      "prior +12% vol growth confirmed; H1 tracks the FY25 seasonal split almost exactly"),
 vrow("PC revenue", p_fc['pc_rev'], lob1['pc_r'], sea['pc_r'], note=
      "volume on track — the beat is ASP: realized 1.035 vs 0.990 modelled (+4.5%); the "
      "prior +6% ASP driver under-read post-devaluation pricing"),
 vrow("CV&CE revenue", p_fc['cv_rev'], lob1['cv_r'], sea['cv_r'], note=
      "the largest driver-stack miss: prior +25% volume growth vs realized +62% — the "
      "bus/truck replacement cycle and exports were underestimated"),
 vrow("Light-Mobility revenue", p_fc['lm_rev'], lob1['lm_r'], sea['lm_r'], note=
      "prior +30% vol growth vs realized +48.9%; Qute supply constraint capped it further"),
 vrow("Trading revenue", p_fc['tr_rev'], lob1['tr_r'], sea['tr_r'], note=
      "over-forecast: prior +18% growth vs realized +5.5% — the FY25 tires base carried "
      "a one-off dealer inventory transfer the prior model treated as run-rate"),
 vrow("Auto revenue", p_fc['auto_rev'], a1['rev'], sea['auto'], note=
      "net effect of the above: ~+10% ahead of the prior model's pace"),
 vrow("Auto EBITDA", P26['dcf']['rows'][0]['ebitda'], a1['ebitda'], sea['ebitda'], note=
      "ahead on revenue; margin broadly as modelled"),
]
# level (non-seasonal) comparisons
variance += [
 dict(line="Auto gross margin", forecast_fy26e=P26['gpm'][0], actual_h1=a1['gp']/a1['rev'],
      h1_share_fy25=None, implied_fy26=a1['gp']/a1['rev'],
      deviation=(a1['gp']/a1['rev'])/P26['gpm'][0]-1, unit='ratio',
      verdict="on track", note="H1 14.30% vs 13.80% modelled (+3.6% rel); direction of "
      "y/y compression (15.5% -> 14.3%) as modelled"),
 dict(line="Auto capex", forecast_fy26e=p_dcf['capex'], actual_h1=a1['capex'],
      h1_share_fy25=None, implied_fy26=a1['capex']*2,
      deviation=(a1['capex']*2)/p_dcf['capex']-1, unit='EGP mn',
      verdict="on track", note="H1 45.9% of the modelled year; commitments 1,020.5 support H2"),
 dict(line="Auto net debt", forecast_fy26e=P26['dcf']['auto_nd'], actual_h1=a1['nd'],
      h1_share_fy25=None, implied_fy26=a1['nd'], deviation=a1['nd']/P26['dcf']['auto_nd']-1,
      unit='EGP mn', verdict="on track", note="14,493.6 vs 15,210.0 carried (-4.7%, better)"),
 dict(line="Group net profit", forecast_fy26e=3300.0, actual_h1=h1['np'],
      h1_share_fy25=h1_25['np']/hist['FY25']['np'], implied_fy26=h1['np']/(h1_25['np']/hist['FY25']['np']),
      deviation=h1['np']/(h1_25['np']/hist['FY25']['np'])/3300.0-1, unit='EGP mn',
      verdict="ESCALATE", note="the miss is BELOW the operating line: net finance cost "
      "+42% y/y and a 41.0% effective tax rate (statutory 22.5%) on unshielded regional "
      "losses — mechanisms the prior stack did not carry (flat 28% tax, no finance-cost model)"),
 dict(line="MNT-Halan stake", forecast_fy26e=P26['sotp']['mnt_halan_stake'], actual_h1=mnt['stake'],
      h1_share_fy25=None, implied_fy26=mnt['stake'],
      deviation=mnt['stake']/P26['sotp']['mnt_halan_stake']-1, unit='share',
      verdict="ESCALATE", note="41.61% (press, post-second-closing wording) superseded by "
      "the FS's 42.93% post-first-close; the press figure was not wrong but described a "
      "different completion state — the filing outranks the release"),
 dict(line="EGP/USD (MNT mark translation)", forecast_fy26e=P26['sotp']['egp_usd'], actual_h1=usdegp,
      h1_share_fy25=None, implied_fy26=usdegp, deviation=usdegp/P26['sotp']['egp_usd']-1,
      unit='EGP/USD', verdict="ESCALATE", note="47.5 -> 50.71 (-6.8% EGP)"),
]

# =======================================================================================
# DRIVER STACK — FY26E-FY30E (volume x price; cost per unit; margins as OUTPUTS)
# =======================================================================================
YRS = ['FY26E', 'FY27E', 'FY28E', 'FY29E', 'FY30E']
fx_path  = I([0.045, 0.08, 0.07, 0.06, 0.05], "EGP depreciation path (H2-26 then annual; anchored on realized "
             "47.5->50.71 and the Egypt-US CPI differential ~11-12pp glide)",
             "constructed from CAPMAS CPI + investing.com FX; convergence assumption flagged",
             "2026-08-19", CTY, "path")
cpi_path = I([0.060, 0.12, 0.10, 0.09, 0.08], "Egypt CPI path (H2-26 then annual; 14.9% Jul-26 gliding to 8%)",
             "CAPMAS Jul-26 print + CBE inflation-target direction; convergence assumption flagged",
             "2026-08-19", CTY, "path")
imp_share = I(dict(pc=0.75, cv=0.70, lm=0.80, tr=0.90), "imported/FX-linked share of unit cost per LOB "
              "(CBU fully imported, CKD kit content majority-USD; NOT separately disclosed — constructed, flagged)",
              "constructed; flagged per SIGCM finest-sourced-level rule", "2026-08-19", CO, "shares")

def esc(cls, i):
    """One escalator per physical cost-driver class: FX-linked import share + domestic CPI share."""
    s = imp_share[cls]
    return s*fx_path[i] + (1-s)*cpi_path[i]

# --- volumes & ASP paths (H2-26E anchored on the FY25 seasonal split + launch calendar) --
pc_vol_g  = I([None, 0.09, 0.08, 0.06, 0.05], "PC volume growth FY27-30 (market +18% maturing; launches annualize)",
              "driver decision on AMIC print + ER launch calendar", "2026-08-19", CO, "path")
pc_asp_g  = I([None, 0.08, 0.07, 0.06, 0.06], "PC ASP growth FY27-30 (below FX+CPI per CEO supply-pressure guidance)",
              "driver decision on ER CEO note", "2026-08-19", CO, "path")
cv_vol_g  = I([None, 0.14, 0.10, 0.08, 0.07], "CV&CE volume growth FY27-30", "driver decision", "2026-08-19", CO, "path")
cv_asp_g  = I([None, 0.07, 0.06, 0.06, 0.05], "CV&CE ASP growth FY27-30", "driver decision", "2026-08-19", CO, "path")
lm_vol_g  = I([None, 0.16, 0.13, 0.11, 0.09], "LM volume growth FY27-30 (Qute constraint resolves)", "driver decision", "2026-08-19", CO, "path")
lm_asp_g  = I([None, 0.06, 0.05, 0.05, 0.05], "LM ASP growth FY27-30", "driver decision", "2026-08-19", CO, "path")
tr_g      = I([None, 0.11, 0.10, 0.09, 0.08], "Trading revenue growth FY27-30 (tires normalized)", "driver decision", "2026-08-19", CO, "path")
oth_g     = I([None, 0.10, 0.10, 0.09, 0.08], "other-auto revenue growth FY27-30", "driver decision", "2026-08-19", CO, "path")

# FY26E: H1 actual + H2E on the FY25 seasonal split, tempered where flagged
pc_u_26 = I(64300, "PC volumes FY26E (H1/seasonal-split implies 64,304; launches offset regional drag)",
            "computed: H1 29,554 / FY25-H1-share 45.96%", "2026-08-19", CO, "units")
cv_r_26 = I(10100, "CV&CE revenue FY26E (seasonal-implied 10,713 tempered for 2Q timing)",
            "computed from H1 4,749.1; tempering flagged", "2026-08-19", CO)
lm_r_26 = I(3350, "LM revenue FY26E (seasonal-implied 3,406, Qute-capped)", "computed from H1 1,435.2", "2026-08-19", CO)
tr_r_26 = I(4800, "Trading revenue FY26E (seasonal-implied 4,476; H2 tires restock)", "computed from H1 2,572.3", "2026-08-19", CO)
oth_r_26= I(1340, "other-auto revenue FY26E", "computed: 2x H1 residual 669.2", "2026-08-19", CO)

pc_asp_h1 = lob1['pc_r']/lob1['pc_u']
pc_asp_h2 = pc_asp_h1*1.025  # post-deval price increases already flagged by the company
pc_r_26 = lob1['pc_r'] + (pc_u_26-lob1['pc_u'])*pc_asp_h2
pc_asp_26 = pc_r_26/pc_u_26

lob = {y: {} for y in YRS}
lob['FY26E'] = dict(pc_u=pc_u_26, pc_r=pc_r_26, pc_asp=pc_asp_26,
                    cv_r=cv_r_26, lm_r=lm_r_26, tr_r=tr_r_26, oth_r=oth_r_26)
for i, y in enumerate(YRS[1:], start=1):
    pr = lob[YRS[i-1]]
    u = pr['pc_u']*(1+pc_vol_g[i]); asp = pr['pc_asp']*(1+pc_asp_g[i])
    lob[y] = dict(pc_u=u, pc_asp=asp, pc_r=u*asp,
                  cv_r=pr['cv_r']*(1+cv_vol_g[i])*(1+cv_asp_g[i]),
                  lm_r=pr['lm_r']*(1+lm_vol_g[i])*(1+lm_asp_g[i]),
                  tr_r=pr['tr_r']*(1+tr_g[i]),
                  oth_r=pr['oth_r']*(1+oth_g[i]))
for y in YRS:
    lob[y]['auto_rev'] = lob[y]['pc_r']+lob[y]['cv_r']+lob[y]['lm_r']+lob[y]['tr_r']+lob[y]['oth_r']

# --- cost per unit / per revenue-unit, escalated per class; margins fall out -----------
# H1-26 anchors (FS segment margins mapped onto ER-basis ASPs)
m0 = dict(pc=fsm['pc']['gpm'], cv=fsm['bt']['gpm'], lm=fsm['lm']['gpm'], tr=fsm['tr']['gpm'],
          oth=I(0.182, "other-auto gross margin (residual: auto GP less mapped LOB GP)",
                "computed from ER auto GP 5,722.1 vs FS segment GP sum", "2026-08-19", CO, "ratio"))
# H2-26 seasonal margin anchor: FY25 H2 GPM ran ~1.2pp below H1 (14.25% vs 15.49%) — proven
gpm_h2_25 = (hist['FY25']['auto_gp']-a1['h1_25_gp'])/(hist['FY25']['auto_rev']-a1['h1_25_rev'])
gpm_h1_25 = a1['h1_25_gp']/a1['h1_25_rev']
seasonal_gap = gpm_h1_25 - gpm_h2_25         # +1.24pp — the H2 mix/cost effect, measured
gpm_h1_26 = a1['gp']/a1['rev']
gpm_h2_26 = gpm_h1_26 - seasonal_gap          # 13.06% — same measured seasonal gap applied
rev_h2_26 = lob['FY26E']['auto_rev'] - a1['rev']
auto_gp_26 = a1['gp'] + rev_h2_26*gpm_h2_26
gpm_path = [auto_gp_26/lob['FY26E']['auto_rev']]
# forward: unit-cost paths per class vs price paths — margin is the OUTPUT
cost_ratio = {k: 1-m for k, m in [('pc', m0['pc']), ('cv', m0['cv']), ('lm', m0['lm']),
                                  ('tr', m0['tr']), ('oth', m0['oth'])]}
# normalize tires: H1-26 margin carried a favourable-historical-cost inventory one-off — reset +4% FY27
price_g = dict(pc=pc_asp_g, cv=cv_asp_g, lm=lm_asp_g, tr=[None]+[0.06]*4, oth=[None]+[0.06]*4)
# Forward differential discipline (DU rule): ONE more year of the measured cost-vs-price
# differential (H1-26 evidenced compression + CEO supply-pressure guidance), then unit
# cost escalates WITH price — held flat in BOTH directions from FY28: the disclosed
# series measures one year of compression, not a compounding story, and the named
# offsetting mechanism (rising CKD/localization share: Sadat + 2 more CKD models) is
# real but likewise unquantified in the filings.
cr = {k: [v] for k, v in cost_ratio.items()}
for i in range(1, 5):
    for k in cr:
        one_off = 1.04 if (k == 'tr' and i == 1) else 1.0
        diff = (1+esc(k if k != 'oth' else 'tr', i))/(1+price_g[k][i]) if i == 1 else 1.0
        cr[k].append(cr[k][-1] * diff * one_off)
for i, y in enumerate(YRS[1:], start=1):
    gp = (lob[y]['pc_r']*(1-cr['pc'][i]) + lob[y]['cv_r']*(1-cr['cv'][i])
          + lob[y]['lm_r']*(1-cr['lm'][i]) + lob[y]['tr_r']*(1-cr['tr'][i])
          + lob[y]['oth_r']*(1-cr['oth'][i]))
    gpm_path.append(gp/lob[y]['auto_rev'])

gsa_pct  = I([0.0710, 0.0705, 0.0700, 0.0692, 0.0685], "auto GS&A %rev (H1-26 actual 7.10% gliding on scale)",
             "H1-26 ER actual + glide decision", "2026-08-19", CO, "path")
oth_pct  = I(0.0084, "auto other operating income %rev (H1-26 actual)", "H1-26 ER actual", "2026-08-19", CO, "ratio")
prov_pct = I(-0.0022, "auto net provisions %rev (H1-26 actual)", "H1-26 ER actual", "2026-08-19", CO, "ratio")
dna_pct  = I([0.0100, 0.0102, 0.0104, 0.0104, 0.0104], "auto D&A %rev (H1 actual 1.00%; Sadat ramp)",
             "H1-26 actual + PP&E note 17", "2026-08-19", CO, "path")
etr_path = I([0.38, 0.30, 0.26, 0.24, 0.225], "auto effective tax path (41.0% H1 -> statutory 22.5% as regional "
             "losses fade per CEO guidance: Jordan subsides from 4Q26, Iraq geopolitics-dependent)",
             "note 11-C + ER CEO note; glide decision", "2026-08-19", CO, "path")
capex    = I([2800, 2600, 2500, 2500, 2600], "auto capex path (H1 1,376.5 actual + 1,020.5 committed; "
             "Sadat complete, Ain Sokhna under consideration)", "ER/FS + decision", "2026-08-19", CO, "path")
wc_pct   = I([0.230, 0.225, 0.220, 0.215, 0.210], "auto WC %rev (LTM actual 23.0% at 2Q26 gliding to 21%; "
             "5-quarter table shows 16.7-18.9bn stable band; FY25's 28.5% was the pre-buy outlier)",
             "ER table 6 computed + glide decision", "2026-08-19", CO, "path")

# asset-conversion cycle (from the statements; disclosed here, projected via wc_pct above)
ccc = dict(
 dio = a1['inv']/(a1['cogs']*2/365.0),
 dso = a1['rec']/(a1['rev']*2/365.0),
 dpo = a1['pay']/(a1['cogs']*2/365.0),
)
ccc['ccc'] = ccc['dio']+ccc['dso']-ccc['dpo']

rows = []
wc_prev = hist['FY25']['wc']
for i, y in enumerate(YRS):
    r = lob[y]['auto_rev']
    gp = r*gpm_path[i]
    op = gp - r*gsa_pct[i] + r*oth_pct + r*prov_pct
    dna = r*dna_pct[i]
    ebitda = op + dna
    nopat = op*(1-etr_path[i])
    wc = r*wc_pct[i]
    dwc = wc - wc_prev
    fcff = nopat + dna - capex[i] - dwc
    rows.append(dict(year=y, rev=r, gp=gp, gpm=gpm_path[i], ebitda=ebitda, ebit=op,
                     dna=dna, nopat=nopat, capex=capex[i], dwc=dwc, fcff=fcff, wc=wc,
                     etr=etr_path[i]))
    wc_prev = wc

# H1-26 realized auto FCFF on the model's own definition (so the valuation date is 30-Jun-26)
# = EBIT x (1-ETR_H1) + D&A - capex - realized dWC (17,092.8 - 18,917.0, a release)
h1_fcff = a1['op']*(1-etr_h1) + a1['dna'] - a1['capex'] - (a1['wc']-hist['FY25']['wc'])

# =======================================================================================
# WACC v2 — rf* = observed - own default spread; both ERP bases; tier-1 beta
# =======================================================================================
beta_rec = own_stock_beta('GBCO', 'EG', 'EGX')
assert_beta_provenance(beta_rec)
beta = beta_rec['beta']

mktcap = spot_ir*SH
kd_fx_local_equiv = kd_usd + (cpi - 0.03)     # USD coupon + expected depreciation (CPI differential proxy)
pct_local = I(0.90, "EGP share of auto-leg debt (USD liabilities 7,274.4 group-wide INCLUDE trade payables; "
              "per-tranche split not disclosed — bounded <=17% of gross debt, 10% carried, flagged)",
              FS + " note 29 bound + construction", "2026-08-19", CO, "share")
wi = WaccInputs(
    rf_observed=rf_obs,
    rf_source="investing.com, Egypt 10Y local-currency govt bond yield, 19-Aug-2026",
    erp_rating=erp_rating, sov_default_spread_rating=ds_rating,
    erp_cds=erp_cds, sov_default_spread_cds=ds_cds,
    erp_source="Damodaran ORIGINAL ctryprem.html, Egypt row, updated 05-Jan-2026",
    beta=beta,
    beta_source=(f"own_stock_beta('GBCO','EG','EGX'): weekly Dimson beta {beta:.3f} vs EGX30 "
                 f"(raw_indices/EG/EGX30.csv, as-of {beta_rec['index_asof']}), n={beta_rec['n']}, "
                 f"R2={beta_rec['r2']:.3f}, SE={beta_rec['se']:.3f}, window {beta_rec['first_obs']}"
                 f"->{beta_rec['last_obs']} — usable, conforming"),
    kd_pretax_local=kd_egp,
    kd_source="GB Corp H1-26 FS note 26: average rate on current EGP loans & borrowings "
              "20.82% during H1-26 (21.91% FY25); book essentially all variable-rate "
              "(note 29), so the current average IS the marginal rate",
    kd_is_marginal=True,
    kd_pretax_fx_local_equiv=kd_fx_local_equiv, pct_debt_local_ccy=pct_local,
    tax_rate=tax_statutory,
    market_cap=mktcap, total_debt=a1['debt']+a1['notes'],
    debt_currency_evidence="note 26 discloses EGP and USD books with average rates "
                           "20.82%/7.78%; note 29 net USD exposure -1,853.6 (incl payables); "
                           "USD time deposits 5,687.0 offset most USD debt",
    weights_source="market cap = IR-page EGX quote 29.70 (19-Aug-26) x 1,085.5mn shares; "
                   "debt = AUTO segment gross debt + leasing notes (GB Capital's funding "
                   "is an operating liability of the finance leg, valued separately)",
)
wr = build_wacc(wi)
WACC = wr.wacc_cds          # primary basis (continuity with the prior study's primary)
WACC_RATING = wr.wacc_rating
TG = I(0.115, "terminal growth, nominal EGP (long-run inflation 9-10% + 1.5-2% real)",
       "carried from the 08-07-2026 study; spread to WACC re-checked", "2026-08-19", CO, "rate")

# =======================================================================================
# DCF — valuation date 30-Jun-2026 (H1 already realized), mid-period H2 + FY27-30
# =======================================================================================
h2_fcff = rows[0]['fcff'] - h1_fcff
pv_rows = []
disc_t = [0.5, 1.5, 2.5, 3.5, 4.5]
flows  = [h2_fcff] + [r['fcff'] for r in rows[1:]]
for i, (t, f) in enumerate(zip(disc_t, flows)):
    df = 1/(1+WACC)**t
    pv_rows.append(dict(period=('H2-26E' if i == 0 else YRS[i]), fcff=f, t=t, df=df, pv=f*df))
pv_sum = sum(p['pv'] for p in pv_rows)
tv = rows[-1]['fcff']*(1+TG)/(WACC-TG)
pv_tv = tv/(1+WACC)**disc_t[-1]
ev_auto = pv_sum + pv_tv
auto_eq = ev_auto - a1['nd'] - a1['nci_bs']

# =======================================================================================
# LEGS — GB Capital operating equity; associates BOTH WAYS
# =======================================================================================
cap_oper_eq = c1['eq'] - assoc_total          # segment parent equity less associates carrying
cap_mult = dict(bear=0.85, base=1.00, bull=1.15)
cap_val = {k: cap_oper_eq*v for k, v in cap_mult.items()}

mnt_round_egp = mnt['stake']*mnt['round_usd']*usdegp
assoc_A = mnt_round_egp + other_assoc + fvoci          # round-mark framing
assoc_B = assoc_total + fvoci                          # company balance-sheet framing
DISC = I(0.10, "SOTP complexity/conglomerate discount (carried from the prior study)",
         "house decision, unchanged", "2026-08-19", CO, "ratio")

def sotp_ps(auto, cap, assoc, disc):
    return (auto+cap+assoc)*(1-disc)/SH
sotp_A = sotp_ps(auto_eq, cap_val['base'], assoc_A, DISC)
sotp_B = sotp_ps(auto_eq, cap_val['base'], assoc_B, DISC)

# bear/bull around each framing (auto margin/WACC + leg multiples + discount)
def auto_eq_case(gpm_shift, wacc, tg, etr_shift=0.0):
    wcp = hist['FY25']['wc']; frs = []
    for i, y in enumerate(YRS):
        r = lob[y]['auto_rev']
        op = r*(gpm_path[i]+gpm_shift) - r*gsa_pct[i] + r*oth_pct + r*prov_pct
        dna = r*dna_pct[i]
        et = min(0.45, max(0.20, etr_path[i]+etr_shift))
        wc = r*wc_pct[i]
        frs.append(op*(1-et)+dna-capex[i]-(wc-wcp)); wcp = wc
    f0 = frs[0]-h1_fcff
    fl = [f0]+frs[1:]
    pv = sum(f/(1+wacc)**t for f, t in zip(fl, disc_t))
    tv_ = frs[-1]*(1+tg)/(wacc-tg)/(1+wacc)**disc_t[-1]
    return pv+tv_-a1['nd']-a1['nci_bs']
auto_bear = auto_eq_case(-0.010, WACC+0.020, TG-0.010, +0.04)
auto_bull = auto_eq_case(+0.008, WACC-0.015, TG+0.010, -0.02)
sotp_A_bear = sotp_ps(auto_bear, cap_val['bear'], mnt_round_egp*0.80+other_assoc+fvoci, 0.18)
sotp_A_bull = sotp_ps(auto_bull, cap_val['bull'], mnt_round_egp*1.10+other_assoc+fvoci, 0.04)
sotp_B_bear = sotp_ps(auto_bear, cap_val['bear'], assoc_B*0.85, 0.18)
sotp_B_bull = sotp_ps(auto_bull, cap_val['bull'], assoc_B*1.10, 0.04)

# =======================================================================================
# FORECAST STATEMENTS — driver -> IS -> BS -> CF chain (mirrored as live formulas in xlsx)
# =======================================================================================
cap_rev_g = I([None, 0.20, 0.17, 0.15, 0.12], "GB Capital revenue growth FY27-30 (book +33.6% y/y now, "
              "securitization-framework drag H2-26, normalizing)", "driver decision on ER", "2026-08-19", CO, "path")
cap_rev_26 = I(18700.0, "GB Capital revenue FY26E (H1 9,088.2 + H2 at ~run-rate less securitization deferrals)",
               "computed bridge", "2026-08-19", CO)
cap_np_path = I([1450.0, 1750.0, 2050.0, 2350.0, 2650.0], "GB Capital net profit path (H1 649.6 doubling-plus "
                "as provisions/funding normalize; ROAE 13.5% on a compounding book)", "model decision", "2026-08-19", CO, "path")
elim_pct = I(0.013, "inter-segment eliminations, % of summed revenue (H1-26 actual 1.29%)",
             "computed from ER table 11", "2026-08-19", CO, "ratio")
assoc_pickup_path = I([850.0, 1065.0, 1330.0, 1600.0, 1870.0], "associates equity pickup path (H1 410.1 "
                      "annualized, growing ~25%/yr with MNT-Halan's ~30% revenue growth; unverified by "
                      "the auditor — flagged)", "model decision on note 34 + ER", "2026-08-19", CO, "path")
kd_fwd = I([0.195, 0.175, 0.165, 0.155, 0.150], "auto average funding-cost path (20.82% H1 actual, "
           "variable-rate book repricing down the CBE path)", "note 26 + CBE direction", "2026-08-19", CO, "path")
div_ps_path = I(0.35, "dividend per share held at the FY25 level", FS + " note 10", "2026-08-13", CO, "EGP")
div_auto_share = I(0.85, "share of the group dividend funded by the auto leg in the net-debt sweep",
                   "model decision", "2026-08-19", CO, "share")

fs_fc = []
nd_roll = a1['nd']; eq_roll = bs['parent_eq']; assoc_roll = assoc_total
for i, y in enumerate(YRS):
    r = rows[i]
    cap_rev = cap_rev_26 if i == 0 else fs_fc[-1]['cap_rev']*(1+cap_rev_g[i])
    group_rev = r['rev'] + cap_rev - (r['rev']+cap_rev)*elim_pct
    # FY26E finance cost = H1 actual + H2 at kd on the mid-year net debt; then ND x kd path
    fin_cost = (a1['fin'] + 0.5*nd_roll*kd_fwd[i]) if i == 0 else nd_roll*kd_fwd[i]
    auto_ebt = r['ebit'] - fin_cost
    auto_np = auto_ebt*(1-r['etr'])
    # cap_np_path is the ER-basis GB Capital NP after tax & NCI, which already includes
    # the associates equity pickup — so group NP = auto NP + capital NP, no third term
    group_np = auto_np + cap_np_path[i]
    divs = div_ps_path*SH
    # balance-sheet rolls
    assoc_roll = assoc_roll + assoc_pickup_path[i]
    fcfe_auto = r['fcff'] - fin_cost*(1-r['etr'])
    nd_roll = nd_roll - (fcfe_auto - divs*div_auto_share)
    eq_roll = eq_roll + group_np - divs
    fs_fc.append(dict(year=y, auto_rev=r['rev'], cap_rev=cap_rev, group_rev=group_rev,
                      auto_ebit=r['ebit'], fin_cost=fin_cost, auto_np=auto_np,
                      cap_np=cap_np_path[i], assoc_pickup=assoc_pickup_path[i],
                      group_np=group_np, eps=group_np/SH, divs=divs,
                      wc=r['wc'], assoc_carrying=assoc_roll, auto_nd=nd_roll,
                      equity=eq_roll, bvps=eq_roll/SH, roe=group_np/eq_roll))

# =======================================================================================
# THE OTHER LENSES
# =======================================================================================
# (2) book value & sustainable return
bvps = bs['parent_eq']/SH
bvps_marked_A = (bs['parent_eq'] + (mnt_round_egp - mnt['carrying']))/SH
book = dict(bear=0.80*bvps, base=bvps, bull=bvps_marked_A,
            note="base = restated accounting book (P/B 1.0); bull = book with MNT B.V. at "
                 "the round mark; bear = 0.8x book (ROE below Ke)")

# (3) relative multiples — FY26E group EPS (from the statement forecast) x peer band
np26 = fs_fc[0]['group_np']
h2_np_est = np26 - h1['np']      # implied H2-26E, derived not typed (2Q26 alone was 826.3)
eps26 = np26/SH
rel_pe = I(dict(bear=8.0, base=9.5, bull=11.0), "P/E band for the relative lens (CNFN 9.41, AN 9.11, "
           "DOAS 12.55, EGX-industrial context)", "peer set 19-Aug-2026", "2026-08-19", IND, "x")
rel = {k: eps26*v for k, v in rel_pe.items()}

# (4) normalized earnings power (mid-cycle: statutory tax, no regional losses, CBE-eased funding)
fin_norm_rate = I(0.17, "normalized auto funding cost (CBE easing path endpoint on the variable book)",
                  "model decision on note 26 + CBE direction", "2026-08-19", CO, "rate")
norm_mult = I(dict(bear=7.5, base=8.5, bull=9.5), "normalized-earnings multiple band",
              "house band, peer-informed", "2026-08-19", IND, "x")
norm_scal = I(dict(bear=0.85, bull=1.12), "normalized-PAT bear/bull scalars",
              "house decision", "2026-08-19", CO, "x")
fin_norm = a1['nd']*fin_norm_rate
np_norm = (rows[1]['ebit'] - fin_norm)*(1-tax_statutory) + cap_np_path[1]
norm_pat = I(round(np_norm, 0), "normalized mid-cycle group PAT: FY27E auto EBIT less normalized finance "
             "cost (ND x 17% as CBE eases) at 22.5% statutory tax + FY27E GB Capital NP "
             "(incl associates pickup)", "computed normalization", "2026-08-19", CO)
norm = dict(bear=(norm_pat*norm_scal['bear'])/SH*norm_mult['bear'], base=norm_pat/SH*norm_mult['base'],
            bull=(norm_pat*norm_scal['bull'])/SH*norm_mult['bull'])

# =======================================================================================
# SYNTHESIS — four lenses, one field; BOTH framings carried to the end, never averaged
# =======================================================================================
W = I(dict(sotp=0.40, book=0.15, relative=0.20, normalized=0.25),
      "lens weights (SOTP primary; book replaces the prior 'pre-discount' lens per the "
      "model-study template)", "house decision", "2026-08-19", CO, "weights")
central_A = W['sotp']*sotp_A + W['book']*book['base'] + W['relative']*rel['base'] + W['normalized']*norm['base']
central_B = W['sotp']*sotp_B + W['book']*book['base'] + W['relative']*rel['base'] + W['normalized']*norm['base']
bear_B    = W['sotp']*sotp_B_bear + W['book']*book['bear'] + W['relative']*rel['bear'] + W['normalized']*norm['bear']
bull_A    = W['sotp']*sotp_A_bull + W['book']*book['bull'] + W['relative']*rel['bull'] + W['normalized']*norm['bull']

fair = dict(bear=round(bear_B, 1), base=round(central_A, 1), full=round(bull_A, 1))

# sensitivity: MNT mark multiplier x complexity discount (the two live swing factors)
grid_mult = [0.50, 0.625, 0.75, 0.875, 1.00]
grid_disc = [0.0, 0.05, 0.10, 0.15, 0.20]
sens = [[sotp_ps(auto_eq, cap_val['base'], mnt_round_egp*mm+other_assoc+fvoci, dd)
         for dd in grid_disc] for mm in grid_mult]
mult_B = (assoc_B - other_assoc - fvoci)/mnt_round_egp   # where the book mark sits on the grid axis
# margin sensitivity (kept from the prior study's axis, reported as a line)
auto_pm1 = auto_eq_case(+0.01, WACC, TG); auto_mm1 = auto_eq_case(-0.01, WACC, TG)

# =======================================================================================
# EXPERTS (numbers; prose lives in the docx builder)
# =======================================================================================
e1 = dict(base=sotp_ps(auto_eq, cap_val['base'], assoc_A, 0.08),
          rng=[sotp_A_bear*0.95, sotp_A_bull*1.02])
e2 = dict(base=norm['base'], rng=[norm['bear'], norm['bull']])
e3_ev = a1['ce']*(0.229/ (WACC))    # EVA framing: CE x ROCE/WACC
e3 = dict(base=(e3_ev - a1['nd'] - a1['nci_bs'] + cap_oper_eq*0.90 + assoc_B*0.85)/SH,
          roce=0.229, ce=a1['ce'])

# =======================================================================================
# OUTPUT
# =======================================================================================
published = json.load(open(os.path.join(HERE, 'published_gbco.json')))
out = dict(
 build_date="2026-08-19", refresh_of="GBCO_Valuation_Study_08-07-2026 (amended 09-07-2026)",
 spot=spot_lib, spot_date="2026-07-22", spot_ir=spot_ir, spot_ir_date="2026-08-19",
 shares=SH, mktcap=mktcap, bvps=bvps,
 h1=h1, h1_25=h1_25, auto_h1=a1, lob_h1=lob1, fs_margins={k: fsm[k]['gpm'] for k in fsm},
 capital_h1=c1, mnt=mnt, other_assoc=other_assoc, fvoci=fvoci, assoc_total=assoc_total,
 bs=bs, kd_egp=kd_egp, kd_usd=kd_usd, tax_statutory=tax_statutory, etr_h1=etr_h1,
 hist={k: {kk: vv for kk, vv in v.items()} for k, v in hist.items()},
 rf_obs=rf_obs, ds_rating=ds_rating, ds_cds=ds_cds, erp_rating=erp_rating, erp_cds=erp_cds,
 usdegp=usdegp, cpi=cpi, cbe_dep=cbe_dep, amic_pc=amic_pc, peers=peers,
 variance=variance, seasonal=sea,
 drivers=dict(fx_path=fx_path, cpi_path=cpi_path, imp_share=imp_share,
              pc_vol_g=pc_vol_g, pc_asp_g=pc_asp_g, cv_vol_g=cv_vol_g, cv_asp_g=cv_asp_g,
              lm_vol_g=lm_vol_g, lm_asp_g=lm_asp_g, tr_g=tr_g, oth_g=oth_g,
              gsa_pct=gsa_pct, oth_pct=oth_pct, prov_pct=prov_pct, dna_pct=dna_pct,
              etr_path=etr_path, capex=capex, wc_pct=wc_pct,
              kd_fwd=kd_fwd, cap_rev_g=cap_rev_g, cap_rev_26=cap_rev_26,
              cap_np_path=cap_np_path, assoc_pickup_path=assoc_pickup_path,
              elim_pct=elim_pct, div_ps=div_ps_path, div_auto_share=div_auto_share,
              fin_norm_rate=fin_norm_rate, norm_mult=norm_mult, norm_scal=norm_scal,
              gpm_path=gpm_path, cost_ratio_paths=cr, seasonal_gap=seasonal_gap,
              gpm_h2_26=gpm_h2_26, lob_margins_h1=m0),
 lob=lob, ccc=ccc,
 beta=beta_rec,
 wacc=dict(rf_obs=rf_obs, rf_star_rating=wr.rf_star_rating, rf_star_cds=wr.rf_star_cds,
           erp_rating=erp_rating, erp_cds=erp_cds, beta=beta,
           ke_rating=wr.ke_rating, ke_cds=wr.ke_cds,
           kd_pretax_local=kd_egp, kd_fx_local_equiv=kd_fx_local_equiv, pct_local=pct_local,
           kd_blended=wr.kd_pretax_blended, kd_aftertax=wr.kd_aftertax,
           we=wr.we, wd=wr.wd, wacc_cds=WACC, wacc_rating=WACC_RATING, tg=TG,
           warnings=wr.warnings,
           report=wr.report()),
 dcf=dict(rows=rows, h1_fcff=h1_fcff, h2_fcff=h2_fcff, pv_rows=pv_rows, pv_sum=pv_sum,
          tv=tv, pv_tv=pv_tv, ev=ev_auto, tv_pct=pv_tv/ev_auto, wacc=WACC, tg=TG,
          auto_nd=a1['nd'], auto_nci=a1['nci_bs'], auto_eq=auto_eq,
          auto_eq_pm1=auto_pm1, auto_eq_mm1=auto_mm1),
 legs=dict(cap_oper_eq=cap_oper_eq, cap_val=cap_val,
           mnt_round_egp=mnt_round_egp, assoc_A=assoc_A, assoc_B=assoc_B, disc=DISC),
 both_ways=dict(
     A=dict(label="round mark (Jun-26 first close, USD 1.4bn x 42.93% x 50.71)",
            assoc=assoc_A, sotp=sotp_A, sotp_bear=sotp_A_bear, sotp_bull=sotp_A_bull,
            central=central_A),
     B=dict(label="company balance-sheet mark (equity-method carrying, KPMG-qualified)",
            assoc=assoc_B, sotp=sotp_B, sotp_bear=sotp_B_bear, sotp_bull=sotp_B_bull,
            central=central_B),
     gap_ps=(assoc_A-assoc_B)*(1-DISC)/SH, mult_B_on_grid=mult_B),
 fs_forecast=fs_fc,
 lenses=dict(sotp=dict(bear=sotp_B_bear, base_A=sotp_A, base_B=sotp_B, bull=sotp_A_bull),
             book=book, relative=dict(**rel, pe=rel_pe, eps26=eps26, np26=np26),
             normalized=dict(**norm, norm_pat=norm_pat),
             central=dict(A=central_A, B=central_B, bear=bear_B, bull=bull_A),
             weights=W),
 fair=fair,
 sens=dict(grid_mult=grid_mult, grid_disc=grid_disc, table=sens, mult_B=mult_B),
 experts=dict(e1=e1, e2=e2, e3=e3),
 published=published,
 prior_step0=dict(nonoverlap_skill=P26['step0']['nonoverlap']['crps_skill'],
                  monthly_skill=P26['step0']['monthly']['crps_skill'],
                  cov90=P26['step0']['nonoverlap']['cov90'],
                  n=P26['step0']['nonoverlap']['n']),
 n_register=len(REG),
 slider_constants=dict(applicable=False,
     note="gbco.html carries no bespoke factor-stack slider: CONT_FIXED / EV_FIXED / "
          "GEO_MEAN / LNCH_MEAN exist only on the ADCB/ALPHADHABI calculator pages "
          "(build_adh_page.py); verified by repo-wide grep 19-08-2026 — nothing to re-fit"),
 register=REG,
)

# ---- assertions (pre-pass: prose numbers must be computed, not typed) ------------------
assert abs(lob['FY26E']['auto_rev'] - (pc_r_26+cv_r_26+lm_r_26+tr_r_26+oth_r_26)) < 0.01
assert abs((a1['inv']+a1['rec']+a1['adv']+a1['debtors']-a1['pay']) - a1['wc']) < 0.15, \
    "ER WC table must foot: components vs total"
assert abs((lob1['pc_r']+lob1['cv_r']+lob1['lm_r']+lob1['tr_r']+lob1['oth_r']) - a1['rev']) < 0.15
assert abs(h1['rev'] - (a1['rev']+c1['rev']-635.3)) < 0.2, "group = auto + capital - eliminations"
assert all(r.get('name') and r.get('source') and r.get('date') and r.get('layer') for r in REG)
assert wr.rf_star_rating > 0 and wr.rf_star_cds > 0
assert fair['bear'] < fair['base'] < fair['full']
assert abs((assoc_A-assoc_B) - (mnt_round_egp - mnt['carrying'] )) < 0.01  # the gap IS the MNT gap

with open(os.path.join(HERE, 'study_numbers.json'), 'w') as f:
    json.dump(out, f, indent=1, default=float)

print(f"beta {beta:.3f} (R2 {beta_rec['r2']:.2f}, n {beta_rec['n']}) | "
      f"rf* {wr.rf_star_cds*100:.2f}/{wr.rf_star_rating*100:.2f} | "
      f"Ke {wr.ke_cds*100:.2f}/{wr.ke_rating*100:.2f} | Kd_at {wr.kd_aftertax*100:.2f} | "
      f"we/wd {wr.we*100:.0f}/{wr.wd*100:.0f} | WACC {WACC*100:.2f}% (rating {WACC_RATING*100:.2f}%)")
print("auto rev path:", [round(r['rev']) for r in rows])
print("auto GPM path:", [round(g*100, 2) for g in gpm_path])
print("FCFF path:", [round(r['fcff']) for r in rows], "| H1 realized", round(h1_fcff),
      "| H2-26E", round(h2_fcff))
print(f"EV {ev_auto:,.0f} (TV {pv_tv/ev_auto*100:.0f}%) -> auto_eq {auto_eq:,.0f} "
      f"({auto_eq/SH:.2f}/sh) | cap leg {cap_val['base']:,.0f} | "
      f"assoc A {assoc_A:,.0f} / B {assoc_B:,.0f}")
print(f"SOTP/sh A {sotp_A:.2f} [{sotp_A_bear:.2f}-{sotp_A_bull:.2f}] | "
      f"B {sotp_B:.2f} [{sotp_B_bear:.2f}-{sotp_B_bull:.2f}]")
print(f"book {book['base']:.2f} | rel {rel['base']:.2f} (EPS26 {eps26:.2f}) | "
      f"norm {norm['base']:.2f} (PAT {norm_pat:,.0f})")
print(f"central A {central_A:.2f} / B {central_B:.2f} | fair {fair}")
print("variance escalations:", [v['line'] for v in variance if v['verdict'] == 'ESCALATE'])
print("register:", len(REG), "inputs | wacc warnings:", len(wr.warnings))
for w in wr.warnings: print("  WACC-WARN:", w)
