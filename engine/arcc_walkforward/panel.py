"""ARCC fundamental walk-forward — the panel, with four-field provenance.

EVERY FIGURE IS TIER A: read off Arabian Cement Company's OWN documents,
downloaded from arabiancementcompany.com (see fetch_attempts.json for the URL,
timestamp and sha256 of each).  No aggregator, no broker, no press appears
anywhere in this chain -- SIGCM clause 1.

THE ROUTE EACH FIGURE CAME BY IS RECORDED, because the two routes have
different failure modes [R-FCAL-01 §1]:

  OCR   every audited consolidated filing is a PURE SCAN -- eleven fiscal years
        and zero characters of text layer between them -- so the statements were
        rendered at 300dpi and read off the pixels.  ARITHMETIC IS THE ARBITER,
        NOT THE EXTRACTOR'S CONFIDENCE: every statement below is asserted to
        foot against its own subtotals, and that check has already earned its
        keep (FY2016 income tax OCR'd as 224 683 515; the footing forced it to
        124 683 515, which the FY2017 filing's comparative column then confirmed).
  TEXT   the earnings releases and IR decks carry a real text layer and supply
        the OPERATING drivers -- volumes, revenue per ton, cash cost per ton --
        that no financial statement discloses.

AND THE TWO SOURCES DO NOT AGREE ON REVENUE, WHICH IS A FINDING, NOT A NUISANCE.
The release's "Total Revenues" is EGP 8,585mn for FY2024 against audited net
sales of EGP 8,729.8mn.  Note 36 (operating segments) resolves it exactly:
revenue from external customers, cement production segment = 8,585,462,048, with
ready-mix concrete and alternative fuels making up the rest.  THE RELEASE
REPORTS THE CEMENT SEGMENT AND THE STATEMENTS REPORT THE GROUP.  So the volumes
and per-ton metrics below belong to the CEMENT segment and the income statement
belongs to the GROUP, and dividing one by the other without saying so would be
L-010's error in a new costume.  Where a per-ton figure is used, it is used
against the segment revenue it actually describes.

POINT-IN-TIME.  Each year's figures are AS THAT YEAR'S OWN FILING REPORTED THEM.
Where a later filing restated a line, the restatement is recorded BESIDE it in
`restated`, never substituted -- an origin may only see what had been published
by its own date.
"""

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

# --------------------------------------------------------------------------
# GROUP INCOME STATEMENT, as each year's own audited consolidated filing
# reported it.  EGP.  Route: OCR off the rendered pixels of a scanned filing.
# --------------------------------------------------------------------------
IS = {
    2014: dict(src='FY2015_cons', page=5, sales=2520586769, cogs=1784610553,
               gp=735976216, ga=91030115, fin=94560609, fx=-25856362,
               pbt=524314491, tax=-149591732, npat=374722759),
    2015: dict(src='FY2015_cons', page=5, sales=2273300139, cogs=1718039515,
               gp=555260624, ga=81018505, fin=89563808, fx=-44003603,
               pbt=327193180, tax=-49964253, npat=277228927,
               restated=dict(by='FY2016_cons', sales=2256645854, cogs=1702399822,
                             gp=554246033, pbt=326988832, npat=277228927)),
    2016: dict(src='FY2016_cons', page=7, sales=2350034092, cogs=1655408051,
               gp=694626040, ga=78212056, fin=6816924, fx=-245925656,
               pbt=369699646, tax=-124683515, npat=245016131),
    2017: dict(src='FY2017_cons', page=7, sales=2647337474, cogs=2268506723,
               gp=378830751, ga=106722754, fin=104201990, fx=30780197,
               pbt=192592059, tax=23018600, npat=215610659),
    2018: dict(src='FY2018_cons', page=7, sales=3274705803, cogs=2826502704,
               gp=448203099, ga=108388819, fin=111059969, fx=-3896880,
               pbt=239076638, tax=-7434476, npat=231642162,
               restated=dict(by='FY2019_cons', cogs=2821949633, gp=452756170,
                             ga=112941890)),
    2019: dict(src='FY2019_cons', page=7, sales=3101527489, cogs=2894882469,
               gp=206645020, ga=103266465, fin=137158211, fx=66332750,
               pbt=36870099, tax=-7931515, npat=28938584,
               restated=dict(by='FY2020_cons', cogs=2899331819, gp=202195670,
                             ga=98817115)),
    2020: dict(src='FY2020_cons', page=7, sales=2481182477, cogs=2455463159,
               gp=25719318, ga=95464653, fin=81107274, fx=12322680,
               pbt=-137411687, tax=14623637, npat=-122788050),
    2021: dict(src='FY2021_cons', page=7, sales=2448631353, cogs=2281083584,
               gp=167547769, ga=81070460, fin=70126214, fx=-1060989,
               pbt=55178070, tax=-20988687, npat=34189383),
    2022: dict(src='FY2022_cons', page=6, sales=4675002824, cogs=3789816211,
               gp=885186613, ga=114977983, fin=58081220, fx=None,
               pbt=521863563, tax=-162877642, npat=358985921),
    2023: dict(src='FY2023_cons', page=6, sales=6042831338, cogs=4759815212,
               gp=1283016126, ga=183940276, fin=76979253, fx=None,
               pbt=930231432, tax=-232732802, npat=697498630),
    2024: dict(src='FY2024_cons', page=6, sales=8729782821, cogs=6642972487,
               gp=2086810334, ga=267798104, fin=91188916, fx=-243812127,
               pbt=1505866118, tax=-345730996, npat=1160135122),
    2025: dict(src='FY2025_cons', page=6, sales=12447320081, cogs=7389054416,
               gp=5058265665, ga=384332833, fin=49841733, fx=-101578240,
               pbt=4725157878, tax=-1125467657, npat=3599690221),
}

# --------------------------------------------------------------------------
# CEMENT-SEGMENT OPERATING DRIVERS, from ARCC's own earnings releases and IR
# decks.  Volumes in thousand tonnes; money in EGP million.  Route: TEXT.
#
# TWO TRAPS LIVE IN THESE DOCUMENTS AND BOTH ARE HANDLED HERE, NOT DISCOVERED
# LATER:
#  (i)  THE UNIT LABEL IS UNRELIABLE.  The FY2016 release heads its money rows
#       "K EGP" and means thousands; the FY2020 and FY2021 releases head them
#       "K EGP" and mean MILLIONS; the FY2017 release heads D&A "MM EGP" and
#       means thousands.  Magnitude is the arbiter, and every figure below is
#       normalised to EGP million and cross-checked against the audited series.
#  (ii) ROWS WITHOUT THE "ACC" PREFIX ARE THE NATIONAL MARKET, NOT THIS COMPANY.
#       "Domestic Sales 12,417 K tons" is Egypt; ACC's own is "ACC Domestic
#       Sales Volume 938".  A parser that took the first matching row would
#       overstate this company's volume by a factor of thirteen.
# --------------------------------------------------------------------------
OPS = {
    2014: dict(src='ER_FY2015', vol_total=4130.418, rev_seg=2498.734,
               cash_cost=1558.936, ebitda=833.336, dna=190.650, sga=106.483,
               basis='standalone'),
    2015: dict(src='ER_FY2015', vol_total=4271.201, rev_seg=2236.128,
               cash_cost=1466.358, ebitda=668.864, dna=196.521, sga=92.890,
               basis='standalone'),
    2016: dict(src='ER_FY2016', vol_total=4040.0, rev_seg=2287.315,
               cash_cost=1367.571, ebitda=820.298, dna=204.330, sga=99.446),
    2017: dict(src='ER_FY2017', vol_total=4114.0, vol_local=3714.0, vol_exp=401.0,
               rev_seg=2567.0, cash_cost=1933.0, ebitda=507.0, dna=234.707,
               sga=127.0),
    2018: dict(src='ER_FY2018', vol_total=4461.0, vol_local=3858.0, vol_exp=602.0,
               rev_seg=3160.0, cash_cost=2437.0, ebitda=588.0, dna=248.0,
               sga=135.0),
    2019: dict(src='ER_FY2019', vol_total=4557.0, vol_local=3944.0, vol_exp=614.0,
               rev_seg=2972.0, cash_cost=2487.0, ebitda=359.0, dna=252.0,
               sga=125.0),
    2020: dict(src='ER_FY2020', vol_total=4078.0, vol_local=3714.0, vol_exp=364.0,
               rev_seg=2410.0, cash_cost=2109.0, ebitda=183.0, dna=247.0,
               sga=119.0),
    2021: dict(src='ER_FY2021', vol_total=3208.0, vol_local=2711.0, vol_exp=497.0,
               rev_seg=2343.0, cash_cost=1899.0, ebitda=378.0, dna=253.0,
               sga=112.0),
    2022: dict(src='ER_FY2022', vol_total=4561.0, vol_local=3218.0, vol_exp=1002.0,
               rev_seg=4549.0, cash_cost=3409.0, ebitda=1092.0, dna=237.0,
               sga=152.0),
    2023: dict(src='ER_FY2023', vol_total=4376.1, vol_local=2674.9, vol_exp=1701.2,
               rev_seg=5933.0, rev_local=3880.0, rev_export=2054.0,
               cash_cost=4363.0, ebitda=1354.0, dna=242.0, sga=229.0),
    2024: dict(src='ER_FY2024', vol_total=5054.3, vol_local=2618.3, vol_exp=2436.0,
               rev_seg=8585.0, rev_local=4739.0, rev_export=3846.0,
               cash_cost=6196.0, ebitda=2037.0, dna=247.0, sga=352.0),
    2025: dict(src='IR_FY2025', vol_total=4853.6, vol_local=2923.6, vol_exp=1930.0,
               rev_seg=12320.0, rev_local=8505.0, rev_export=3815.0,
               cash_cost=6887.0, ebitda=4988.0, dna=283.0, sga=499.0),
}

# Clinker and cement production, and the utilisation the volume driver is
# capacity-checked against.  K tonnes / per cent.  Route: TEXT.
PRODUCTION = {
    2015: dict(clinker=3534.4, cement=4259.8, clk_util=0.84, cem_util=0.85),
    2016: dict(clinker=3620.0, cement=4019.0, clk_util=0.86, cem_util=0.86),
    2017: dict(clinker=3434.0, cement=4144.0, clk_util=0.82, cem_util=0.88),
    2018: dict(clinker=4123.0, cement=4289.0, clk_util=0.98, cem_util=0.91),
    2019: dict(clinker=3853.0, cement=4322.0, clk_util=0.92, cem_util=0.92),
    2020: dict(clinker=3237.0, cement=4069.0, clk_util=0.77, cem_util=0.87),
    2021: dict(clinker=3189.0, cement=2796.0, clk_util=0.76, cem_util=0.59),
    2022: dict(clinker=3808.0, cement=3254.0, clk_util=0.91, cem_util=0.69),
    2024: dict(clinker=3606.7, cement=2935.4, clk_util=0.86),
    2025: dict(clinker=3851.6, cement=3480.6, clk_util=0.92),
}

# The EXOGENOUS volume anchor [R-FCAL-01 §3: "never on the company's own trend
# alone"].  Egypt's national DOMESTIC cement market and ACC's domestic cement
# volume, both from ARCC's own releases.  K tonnes.
#
# DOMESTIC, NOT TOTAL, AND THE REASON IS A DATA FACT.  The releases report the
# national market as domestic + export up to FY2020 and as "Cement Domestic
# Sales" from FY2021, so a total-market series is not consistently sourceable
# across the window while a domestic one is.  Amendment A-1 to the
# pre-registration records this; it was made before any error was computed and
# for a sourcing reason, not a results one.
#
# ACC's share is computed here as its own domestic CEMENT volume over the
# national domestic market, and reproduces the share the releases print to
# within a tenth of a point (FY2019 8.14% vs 8.1%, FY2021 5.58% vs 5.6%,
# FY2022 6.29% vs 6.3%) -- which is the check that the two series describe the
# same thing.  Local clinker sales are deliberately outside it: including them
# breaks the reproduction (FY2022 6.95% against a printed 6.3%), and a
# denominator that does not reproduce the company's own published ratio is the
# wrong denominator.
MARKET = {
    2014: dict(national=52233.7, src='ER_FY2015'),
    2015: dict(national=53800.2, src='ER_FY2015'),
    2016: dict(national=56498.0, src='ER_FY2017'),
    2017: dict(national=53440.0, src='ER_FY2017'),
    2018: dict(national=50475.0, src='ER_FY2018'),
    2019: dict(national=48448.0, src='ER_FY2020'),
    2020: dict(national=45955.0, src='ER_FY2020'),
    2021: dict(national=48570.0, src='ER_FY2021'),
    2022: dict(national=51193.0, src='ER_FY2022'),
    2023: dict(national=47560.6, src='ER_FY2023'),
    2024: dict(national=47686.0, src='IR_FY2024'),
    2025: dict(national=53992.9, src='IR_FY2025'),
}

# ACC's own domestic CEMENT volume and everything that is not domestic cement
# (exports, plus local clinker where disclosed).  K tonnes.
ACC_VOL = {
    2016: dict(dom=3989.0, rest=51.0,   src='ER_FY2017'),
    2017: dict(dom=3714.0, rest=400.0,  src='ER_FY2017'),
    2018: dict(dom=3858.0, rest=603.0,  src='ER_FY2018'),
    2019: dict(dom=3944.0, rest=613.0,  src='ER_FY2019'),
    2020: dict(dom=3714.0, rest=364.0,  src='ER_FY2020'),
    2021: dict(dom=2711.0, rest=497.0,  src='ER_FY2021'),
    2022: dict(dom=3218.0, rest=1343.0, src='ER_FY2022'),
    2023: dict(dom=2674.9, rest=1701.2, src='ER_FY2023'),
    2024: dict(dom=2618.3, rest=2436.0, src='ER_FY2024'),
    2025: dict(dom=2923.6, rest=1930.0, src='IR_FY2025'),
}

# COST STACK from note 5 of the audited filings -- what each escalator class is
# actually worth.  EGP.  ONE ESCALATOR PER DRIVER CLASS [L-009, L-110]: raw
# materials carry the imported, USD-linked inputs; transportation and overheads
# are domestic.  `overheads` is DERIVED as the residual and asserted to foot.
COST_STACK = {
    2024: dict(src='FY2025_cons', page=26, raw=5225344010, mfg_dep=217717204,
               amort_lic=28156249, amort_rou=7082414, transport=792242214,
               total=6642972487),
    2025: dict(src='FY2025_cons', page=26, raw=5698184715, mfg_dep=254765548,
               amort_lic=28156249, amort_rou=2525364, transport=764279332,
               total=7389054416),
}

# INTEREST-BEARING BORROWINGS ONLY -- note 25.  [L-002] The finance charge is
# divided by the debt that ACTUALLY BEARS IT, never by a broader liabilities
# total: trade payables, creditors and tax liabilities pay no interest, and
# dividing by them understates the rate by a multiple and manufactures a bias
# that looks exactly like evidence.
DEBT = {
    2024: dict(src='FY2025_cons', page=34, facilities=615044229,
               loans_current=25481075, loans_noncurrent=120392380, total=760917684),
    2025: dict(src='FY2025_cons', page=34, facilities=99916937,
               loans_current=145493141, loans_noncurrent=888522538, total=1133932616),
}
# Outstanding debt as the releases reported it, EGP million -- the only series
# that spans the whole window.  Route: TEXT.
DEBT_SERIES = {2014: 1200.242, 2015: 1050.702, 2016: 1244.278, 2017: 1267.0,
               2018: 1108.0, 2019: 657.0, 2020: 487.0, 2021: 394.0, 2022: 341.0,
               2023: 0.0, 2024: 760.918, 2025: 1133.933}

# Egypt macro.  EXOGENOUS, and the only series here not sourced from ARCC.
MACRO_SRC = os.path.join(os.path.dirname(HERE), 'phdc_walkforward', 'macro_eg.json')


def macro():
    d = json.load(open(MACRO_SRC, encoding='utf-8'))
    return {'cpi_pct': {int(k): v for k, v in d['cpi_pct'].items()},
            'egp_usd': {int(k): v for k, v in d['egp_usd'].items()},
            'population': {int(k): v for k, v in d['population'].items()},
            'source': d['cpi_pct_source'] + ' ; ' + d['egp_usd_source'],
            'retrieved': d['_retrieved']}


def check():
    """ARITHMETIC IS THE ARBITER.  Every statement foots or the panel refuses."""
    bad = []
    for y, r in sorted(IS.items()):
        if abs((r['sales'] - r['cogs']) - r['gp']) > 2:
            bad.append('%d: sales - cogs != gross profit' % y)
        if abs((r['pbt'] + r['tax']) - r['npat']) > 2:
            bad.append('%d: pbt + tax != npat' % y)
    for y, c in sorted(COST_STACK.items()):
        named = c['raw'] + c['mfg_dep'] + c['amort_lic'] + c['amort_rou'] + c['transport']
        if named > c['total']:
            bad.append('%d: named cost lines exceed total cost of sales' % y)
    for y, v in sorted(ACC_VOL.items()):
        if abs(v['dom'] + v['rest'] - OPS[y]['vol_total']) > 1.5:
            bad.append('%d: domestic + rest != ACC total volume' % y)
    for y, d in sorted(DEBT.items()):
        if abs(d['facilities'] + d['loans_current'] + d['loans_noncurrent'] - d['total']) > 2:
            bad.append('%d: borrowings note does not foot' % y)
    if bad:
        raise SystemExit('PANEL REFUSES:\n  ' + '\n  '.join(bad))
    return True


def overheads(y):
    """DERIVED = total cost of sales less every line note 5 names.  Recorded as
    derived with its formula, never as a disclosed figure."""
    c = COST_STACK[y]
    return c['total'] - (c['raw'] + c['mfg_dep'] + c['amort_lic']
                         + c['amort_rou'] + c['transport'])


YEARS = sorted(IS)

if __name__ == '__main__':
    check()
    print('panel OK — %d audited fiscal years %d..%d, all footing'
          % (len(YEARS), YEARS[0], YEARS[-1]))
    print('%-6s %12s %12s %10s %10s %9s %8s' %
          ('FY', 'sales(EGPm)', 'cogs(EGPm)', 'npat(EGPm)', 'vol(kt)',
           'seg rev', 'grp-seg'))
    for y in YEARS:
        o = OPS.get(y, {})
        seg = o.get('rev_seg')
        print('%-6d %12.1f %12.1f %10.1f %10.1f %9s %8s' %
              (y, IS[y]['sales'] / 1e6, IS[y]['cogs'] / 1e6, IS[y]['npat'] / 1e6,
               o.get('vol_total', float('nan')),
               ('%.1f' % seg) if seg else '-',
               ('%.1f' % (IS[y]['sales'] / 1e6 - seg)) if seg else '-'))
    for y in sorted(COST_STACK):
        print('overheads %d (derived residual): EGP %.1fmn' % (y, overheads(y) / 1e6))
