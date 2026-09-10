"""Content part A: masthead → §2.

REBUILT 07-09-2026, SECOND PASS. The study this file was written against published a
weighted blend of four lenses, a single central, a typed complexity discount and a
normalised-earnings read. All four are retired. The class primary IS the answer, and on
this name the answer has TWO SIDES, because GB Corp's largest single component is carried
two ways in GB Corp's own disclosures and the filings do not decide between them.

Every financial numeral is READ from the study's committed record (depth-bar standard 3).
Nothing in this file is an input to the model: the two figures solved from the traded price
are computed here, from committed outputs, for the reader's benefit and are used nowhere.
"""
import os as _os
import sys as _sys

_HERE = _os.path.dirname(_os.path.abspath(__file__))
_sys.path.insert(0, _HERE)
_sys.path.insert(0, _os.path.join(_HERE, '..'))

from docx_base import *                                              # noqa: F401,F403
import table_residual as TR                                          # noqa: E402
from outward_source import outward as _outward                       # noqa: E402

pr = D['mc']['prob_read']; q20, q60 = D['mc']['q20'], D['mc']['q60']
tech = D['tech']; dcf = D['dcf']; sotp = D['sotp']
COC = D['cost_of_capital_record']; MAC = D['macro']; LI = D['lens_inputs']
HIS = D['history']['income_statement']; DRV = D['disclosed_drivers']
spot = D['spot']; spot_date_iso = D['spot_date']; SH = D['shares']
EDITION = D['edition']
# THE TECHNICAL READ SITS ON A DIFFERENT CLOCK FROM THE PRICE AND THE DOCUMENT SAYS SO.
# The averages, the oscillators and the 52-week range are computed on the exchange
# library's own last session; the valuation is struck on the latest price the repository
# knows. Quoting one against the other is a two-clocks error.
TA_CLOSE = D['valuation_gap']['mc_anchor']
TA_DATE = D['valuation_gap']['mc_anchor_date']

_MONTHS = ('January', 'February', 'March', 'April', 'May', 'June', 'July',
           'August', 'September', 'October', 'November', 'December')


def longdate(iso):
    y, m, dd = (int(x) for x in iso.split('-'))
    return '%d %s %d' % (dd, _MONTHS[m - 1], y)


SPOT_DATE = longdate(spot_date_iso)
TA_DATE_L = longdate(TA_DATE)
EDITION_L = longdate(EDITION)
EDITION_STAMP = '%s-%s-%s' % tuple(EDITION.split('-')[::-1])

# ---- the answer -------------------------------------------------------------
B_LO, B_HI = BRANCHES[0], BRANCHES[1]        # carrying value, June-2026 round
V_LO, V_HI = B_LO['value'], B_HI['value']
GAP_LO, GAP_HI = V_LO / spot - 1.0, V_HI / spot - 1.0
MARK_LO, MARK_HI = MARKS[0], MARKS[1]        # the associate holding, EGP mn
EQ_LO, EQ_HI = branch_equity(MARK_LO), branch_equity(MARK_HI)
REL = CROSS['relative_multiple']
BOOK = CROSS['book_value']
# THE EQUITY THE BOOK VALUE PER SHARE IS ACTUALLY STRUCK ON, recovered from the committed
# cross-check rather than taken from the nearest-looking balance-sheet input. The inputs
# register carries TOTAL equity at the same date, which INCLUDES minority interests, and a
# reader dividing that by the share count reaches a different number from the one printed.
BOOK_EQUITY = BOOK['value'] * SH
CAP = LI['capital']
STAKE = sotp['mnt_halan_stake']
STAKE_PRIOR = sotp['mnt_halan_stake_prior']
# The ownership pair GB Corp's own REVIEWED STATEMENTS give for the same transaction, most
# likely a different level of the structure. NEITHER FIGURE IS TYPED HERE. The model
# registers both and the numbers file does not carry them forward, so they are read from
# the model's own committed constants — and the regex RAISES rather than defaulting if
# either ever stops being registered, because a percentage nobody can trace is not
# evidence. The value the lower figure produces is asserted against the committed
# judgements record beside it, so the two cannot silently disagree.
import json as _json                                                 # noqa: E402
import re as _re                                                     # noqa: E402
_CJ = _json.load(open(_os.path.join(_HERE, 'contested_judgements.json'), encoding='utf-8'))
CJ = _CJ                                   # the appendices read the same record
LIVES = _json.load(open(_os.path.join(_HERE, 'useful_lives.json'), encoding='utf-8'))
outward = _outward                         # one stripper, shared, never copied
_STAKE_FORK = [j for j in _CJ['judgements']
               if j['name'] == 'the ownership percentage applied to the round'][0]
_MODEL_SRC = open(_os.path.join(_HERE, 'compute.py'), encoding='utf-8').read()


def _model_constant(name):
    return float(_re.search(r'^%s\s*=\s*([0-9.]+)' % name, _MODEL_SRC, _re.M).group(1))


STAKE_STATEMENTS = _model_constant('mnt_stake_statements')
STAKE_STATEMENTS_PRIOR = _model_constant('mnt_stake_statements_prior')
_check = ((_STAKE_FORK['value_alternative_round_branch'] * SH
           - sotp['auto_eq'] - sotp['cap_val'] - sotp['other_assoc'])
          / (sotp['mnt_halan_round_usd'] * sotp['egp_usd']))
assert abs(_check - STAKE_STATEMENTS) < 1e-6, (
    'the ownership figure the model registers and the one the judgements record prices '
    'have diverged: %r against %r' % (STAKE_STATEMENTS, _check))
# The reviewers' own words and the figure they could not verify, READ from the committed
# judgements record rather than typed. If the record ever stops carrying it this raises,
# which is the point: a quotation nobody can trace is not evidence.
QUALIFICATION = _CJ['two_sided_judgement']['basis_b']['against_it']
SHARE_OF_PROFIT = float(_re.search(r'EGP\s*([\d,.]+)\s*mn share of profit',
                                   QUALIFICATION).group(1).replace(',', ''))

# ---- what the traded price must believe, solved on this study's own model ----
# COMPUTED HERE AND USED NOWHERE. A quantity solved from a price and fed back into a
# valuation is the reverse-engineered figure this house prohibits outright; these two are
# read forward only, so a reader can see the disagreement measured rather than described.
# TWO DIFFERENT RESIDUALS AND THEY ARE NOT INTERCHANGEABLE. What the market capitalisation
# leaves once the two OPERATING legs are taken at this study's marks is what the price pays
# for ALL the associates; taking the smaller holdings at their carrying value as well leaves
# what it pays for MNT-Halan ALONE, which is the line the two branches differ in.
PRICE_ASSOC = spot * SH - sotp['auto_eq'] - sotp['cap_val']
PRICE_MARK = PRICE_ASSOC - sotp['other_assoc']
PRICE_MNT_USD = PRICE_MARK / (STAKE * sotp['egp_usd'])
MNT_USD_AT_CARRYING = MARK_LO / (STAKE * sotp['egp_usd'])
OPERATING_EQ = sotp['auto_eq'] + sotp['cap_val']


def _price_implied_rate(mark):
    """The first-year cost of capital on the auto leg that reproduces the traded price,
    every other line held at its published value. The whole ladder moves together."""
    lo, hi = -0.10, 0.60
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        v = sotp_per_share(mark, mid)
        if v is None or v > spot:
            lo = mid
        else:
            hi = mid
    return dcf['forward_wacc'][0] + 0.5 * (lo + hi)


RATE_HI = _price_implied_rate(MARK_HI)       # on the round-price branch
RATE_LO = _price_implied_rate(MARK_LO)       # on the carrying-value branch


def pc(x, d=1):
    return f'{x*100:.{d}f}%'


def sgn(x, d=0):
    return f'{x*100:+.{d}f}%'


def n0(x):
    return f'{x:,.0f}'


def n1(x):
    return f'{x:,.1f}'


def paren(x):
    return f'({abs(x):,.0f})'


# ---------------- Masthead / title / anchor --------------------------------
masthead()
P('Independent Valuation Study — Educational Analysis', size=12, bold=True, space_before=4, space_after=2)
P('GB Corp S.A.E. (EGX: GBCO)', size=17, bold=True, space_after=2)
rich([('Fundamental analysis · Technical analysis · Monte Carlo simulation — one integrated read', dict(italic=True, color=GREY)),
      ('   ·   edition %s   ·   %s' % (EDITION_STAMP, EDITION_L), dict(italic=True, color=GREY))],
     size=10.5, space_after=8)
rich([('Anchor: ', dict(bold=True)),
      (f'EGP {spot:.2f} ({SPOT_DATE} close) · {n1(SH)} mn shares · market capitalisation EGP '
       f'{D["mktcap"]/1000:,.1f} bn · the continuing listed entity of the former GB Auto '
       '(Ghabbour), renamed GB Corp in 2023, housing ', {}),
      ('GB Auto', dict(bold=True)),
      (' (passenger cars, commercial vehicles & construction equipment, tires & trading, light mobility; Egypt · Iraq · Jordan), ', {}),
      ('GB Capital', dict(bold=True)),
      (' (leasing, factoring, consumer finance, SME lending) and associate stakes led by ', {}),
      ('MNT-Halan', dict(bold=True)),
      (f' · the price cone and the technical read are computed on the exchange library’s own '
       f'last session, EGP {TA_CLOSE:.2f} on {TA_DATE_L}, and the valuation is struck on the '
       'later price above — two clocks, both dated · the valuation lens is the sum of the '
       'parts (an assembler-distributor, a captive lender and an unlisted associate, each '
       'marked on its own basis) · the basis on which that associate is marked is the whole '
       'of the disagreement in this study, and the answer is published on both.', {})],
     size=9.8, space_after=10)

# ---------------- READ FIRST box --------------------------------------------
box([
 ('READ FIRST — what this document is, and is not.', ''),
 ('', 'This study is a valuation exercise and an expression of personal analytical opinion, published free of charge for '
      'educational purposes: it shows how one analyst applies fundamental, technical and probabilistic methods to a listed '
      'company, and invites scrutiny of that methodology. It is NOT investment advice, NOT a recommendation or solicitation '
      'to buy, sell or hold any security, and NOT directed at the circumstances of any reader. The preparer is not licensed '
      'by any securities regulator in any jurisdiction, holds no Egyptian (FRA) or other brokerage or advisory authorisation, '
      'provides no financial consultancy, manages no money, and accepts no fees, funds or clients. See the Disclosure & '
      'Disclaimer at the end.'),
 ('', 'THIS STUDY PUBLISHES TWO ANSWERS AND NOT ONE, and that is deliberate. GB Corp’s largest single component is a '
      'minority interest in an unlisted company, and GB Corp itself puts two different numbers on it — the value carried '
      'in its own reviewed balance sheet, and the price of the funding round it announced in June 2026. The filings do not '
      'decide between them, so neither does this study: both are carried through to the end and published side by side. '
      'They are never averaged. A figure between them would be a number nobody computed.'),
 ('', 'All values are model outputs presented as ranges and distributions because no single number should be relied on. '
      'Reported financials are the company’s own disclosure — the FY2023, FY2024 and FY2025 earnings releases and '
      'the reviewed consolidated statements to 30 June 2026; forward-looking inputs — the basis for the associate mark, '
      'the mark on the lending arm, the multiples, the cash-flow model and the simulation’s factor probabilities — are '
      'the preparer’s judgments and are flagged throughout. The far forecast years are published as ranges rather than '
      'points, taken from how wrong this method has been on this company’s own history; Appendix A carries the table and '
      'the count behind each band. A note on identity: GB Corp S.A.E. is the renamed GB Auto S.A.E. (Ghabbour Auto); the '
      'EGX ticker is GBCO and the price history continues the former AUTO listing. Consult a licensed financial advisor '
      'before any investment decision.'),
])

# ---------------- Headline ---------------------------------------------------
H2('Headline')
rich([('The operating businesses are worth roughly what the whole company trades for, and everything above that is one '
       'unlisted stake nobody can price from the outside. ',
       dict(bold=True)),
      (f'At EGP {spot:.2f} the shares sit below both readings of the sum of the parts: EGP '
       f'{V_LO:.2f} with MNT-Halan at the value GB Corp’s own reviewed balance sheet carries '
       f'it at ({sgn(GAP_LO)}), and EGP {V_HI:.2f} with MNT-Halan at the price of the June-2026 '
       f'funding round ({sgn(GAP_HI)}). Those two branches differ in one input and in nothing '
       f'else: the auto leg, the lender and the residual associates are identical in both. '
       'Everything else in this study is agreed between them. ', {}),
      (f'Take the operating businesses alone — GB Auto at its cash-flow value of EGP '
       f'{OPERATING_EQ/1000:.1f} bn and GB Capital at the value its own disclosed return '
       f'supports — and they come to {pc(OPERATING_EQ/D["mktcap"],0)} of the entire traded '
       f'market capitalisation before a single pound of associate value. What the price leaves '
       f'for the associates is EGP {PRICE_ASSOC/1000:.1f} bn, against EGP '
       f'{(MARK_LO+sotp["other_assoc"])/1000:.1f} bn carried on the reviewed balance sheet. '
       'On GB Corp’s stated holding that values MNT-Halan as a whole at about US$'
       f'{PRICE_MNT_USD:,.0f} mn, against the US${sotp["mnt_halan_round_usd"]:,.0f} mn its '
       f'June-2026 round was struck at and the US${MNT_USD_AT_CARRYING:,.0f} mn the company’s '
       'own carrying value implies. The price is below both bases the company itself discloses, '
       'and not narrowly. ', {}),
      ('Read the other way round, the same gap is far less dramatic and this study says so: ', {}),
      (f'ask instead what discount rate the price implies on the auto leg, holding every other '
       f'line where it is published, and the answer is {pc(RATE_HI,2)} against this study’s '
       f'{pc(dcf["wacc"],2)} on the round-price branch — a stretch — but only {pc(RATE_LO,2)} '
       'on the carrying-value branch, which is an ordinary disagreement about the cost of '
       'capital in this market. The associate mark is the quantity the branches actually differ '
       'in; it is not the only way to read the gap. ', {}),
      (f'The tape is not the counter-argument it once was. On the library’s last session the '
       f'price sat below its twenty- and fifty-day averages with the oscillator at '
       f'{tech["rsi"]:.0f} and the convergence histogram negative — a stock that has come off '
       f'rather than one that is extended. Over three months the simulation places the '
       f'fifth-to-ninety-fifth percentile band at roughly EGP {q60["5"]:.0f}–{q60["95"]:.0f} '
       f'with a median near EGP {q60["50"]:.0f}; that engine prices the stock’s own path and is '
       'untouched by anything above.', {})],
     space_after=8)

# ---------------- Valuation summary table -----------------------------------
H2('Valuation summary — every read at a glance')
P('One table for the reads that follow. The sum of the parts is the primary lens for this class and it IS the answer; the '
  'other fundamental reads are published beside it as cross-checks and are never averaged into it. Then what the tape is '
  'doing, where price could travel over three months, and how three independent expert methods land. Every row is '
  'developed in the sections and appendices below.', size=9.8)
E = D['experts']
_epanel = [E['e1']['base'], E['e2']['base'], E['e3']['base']]
rows = [
 ['Lens / read', 'What it measures', 'Output', 'Against the price'],
 ['FUNDAMENTAL — the class primary, and it is the answer', '', '', ''],
 ['Sum-of-the-parts · carrying-value branch', 'Auto cash-flow model + lender on residual income + associates at the reviewed carrying value', f"EGP {V_LO:.2f}", sgn(GAP_LO)],
 ['Sum-of-the-parts · round-price branch', 'The same three legs, associates at the June-2026 round price', f"EGP {V_HI:.2f}", sgn(GAP_HI)],
 ['FUNDAMENTAL — cross-checks, published beside the answer and never blended into it', '', '', ''],
 ['Relative multiple', f"FY2026E earnings per share × {REL['multiple']:.2f}×, the median of GB Corp’s own trailing multiple at its last three year-end closes", f"EGP {REL['value']:.2f}", sgn(REL['value']/spot-1)],
 ['Disclosed book value', 'Shareholders’ equity before minority interests at 30 June 2026, per share — a floor, not a value', f"EGP {BOOK['value']:.2f}", sgn(BOOK['value']/spot-1)],
 ['TECHNICAL — what the tape is doing (timing, not value)', '', '', ''],
 ['Trend', f"Close EGP {TA_CLOSE:.2f} against the 20/50/100/200-day averages", 'Below the two short, above the two long', 'Trend intact, momentum lost'],
 ['Momentum / range', 'Relative strength · convergence · 52-week range', f"RSI {tech['rsi']:.0f} · histogram {tech['macd']['hist']:+.2f} · {tech['lo52']:.2f}–{tech['hi52']:.2f}", 'Soft, not oversold'],
 ['SIMULATION — where price could go in 3 months (paths from the anchor)', '', '', ''],
 ['1 month', '50,000 paths · sixteen factors', f"p5 {q20['5']:.1f} · p50 {q20['50']:.1f} · p95 {q20['95']:.1f}", 'Median above the anchor'],
 ['3 months', 'same engine, longer horizon', f"p5 {q60['5']:.1f} · p50 {q60['50']:.1f} · p95 {q60['95']:.1f}", 'Wide, right-skewed'],
 ['EXPERT PANEL — three independent methods (Appendix C)', '', '', ''],
 ['Expert 1 — split-legs net asset value', 'Marks each leg; argues the wrapper discount', f"EGP {E['e1']['base']:.2f}", 'Most bullish'],
 ['Expert 2 — residual income on the whole group', 'What the group’s own reported return justifies against book', f"EGP {E['e2']['base']:.2f}", 'Most conservative'],
 ['Expert 3 — cash returns (return on capital vs its cost)', 'Economic profit on capital employed', f"EGP {E['e3']['base']:.2f}", 'In between'],
 ['Panel spread', 'The spread is the associate mark and the lender basis', f"EGP {min(_epanel):.2f}–{max(_epanel):.2f}", f"Middle read EGP {sorted(_epanel)[1]:.2f}"],
]
table(rows, [2.15, 2.35, 1.45, 1.15], band_rows=[1, 4, 7, 10, 13], first_col_bold=False, size=8.9)
rich([('Bottom line. ', dict(bold=True)),
      (f"There is no single central estimate in this table and there is not supposed to be. The primary lens reads EGP "
       f"{V_LO:.2f} on one of GB Corp’s own disclosures about its associate and EGP {V_HI:.2f} on the other, "
       f"{sgn(GAP_LO)} and {sgn(GAP_HI)} against the price; the cross-checks sit either side of the price, the earnings "
       f"multiple at EGP {REL['value']:.2f} and the disclosed book floor at EGP {BOOK['value']:.2f} — and the shares "
       f"trade BELOW their own book. The three experts span EGP {min(_epanel):.2f} to {max(_epanel):.2f}, and what "
       "separates them is the same one line. Strip the associate out and this is an operating group priced at about what "
       "it earns; put it back at either of the company's own two bases and the shares look cheap. The three-month "
       "distribution is indifferent either way: it prices the stock's own measured path, and its median sits above the "
       "anchor because that drift is what this stock's own history measures rather than what anybody hopes for. How "
       "often the bands built around it have actually held is published at the end of \u00a73, with the count beside "
       "the percentage.", {})], size=9.8, space_after=8)

# ---------------- Company overview -------------------------------------------
H2('Company overview — GB Corp at a glance')
_h25, _h24 = HIS['2025'], HIS['2024']
rows = [
 ['Item', 'Value'],
 ['Listed entity', 'GB Corp S.A.E. (EGX: GBCO; formerly GB Auto / Ghabbour Auto, AUTO)'],
 ['What it owns', 'GB Auto (passenger-car assembly & distribution, commercial vehicles & construction equipment, tires & trading, light mobility) · GB Capital (Drive Finance, GB Lease & Factoring, rentals, Kredit) · associates: MNT-Halan, Bedaya, Kaf'],
 ['Price / date', f"EGP {spot:.2f} · {SPOT_DATE} close"],
 ['Shares · market capitalisation', f"{n1(SH)} mn · EGP {D['mktcap']/1000:,.1f} bn"],
 ['FY2025 revenue / net profit', f"EGP {n1(_h25['revenue'])} mn ({sgn(_h25['revenue']/_h24['revenue']-1)} year on year) · EGP {n1(_h25['net_profit'])} mn ({pc(_h25['net_profit']/_h25['revenue'],1)} of revenue)"],
 ['1H2026 revenue / net profit', f"EGP {n1(D['inputs']['rev_h1_2026']['value'])} mn · EGP {n1(D['inputs']['ni_h1_2026']['value'])} mn (reviewed, six months to 30 June 2026)"],
 ['Group gross margin, FY2023 / FY2024 / FY2025', f"{pc(HIS['2023']['gross_profit']/HIS['2023']['revenue'],2)} / {pc(HIS['2024']['gross_profit']/HIS['2024']['revenue'],2)} / {pc(HIS['2025']['gross_profit']/HIS['2025']['revenue'],2)}"],
 ['GB Auto gross margin, reviewed half to 30 June 2026', f"{pc(D['forecast_anchor']['latest_reviewed_rate'],2)} — the segment revenue and gross profit the release prints for the half"],
 ['Auto net debt · group equity (30 June 2026)', f"EGP {n1(dcf['auto_nd'])} mn · EGP {n1(D['inputs']['eq_jun2026']['value'])} mn"],
 ['Book value per share (30 June 2026)', f"EGP {BOOK['value']:.2f} — the shares trade {sgn(spot/BOOK['value']-1)} against it"],
 ['52-week range (library, %s)' % TA_DATE_L, f"EGP {tech['lo52']:.2f} – {tech['hi52']:.2f}"],
 ['MNT-Halan stake', f"{pc(STAKE,2)}, stated by the company on 9 June 2026 against {pc(STAKE_PRIOR,2)} before that transaction — while its reviewed statements give {pc(STAKE_STATEMENTS,2)} from {pc(STAKE_STATEMENTS_PRIOR,2)} for the same transaction; §1.1 carries both"],
]
table(rows, [1.9, 5.2], first_col_bold=True)
caption('Source: the company’s own FY2023, FY2024 and FY2025 earnings releases; its 2Q/1H2026 release of 13 August 2026 '
        'and the reviewed consolidated statements to 30 June 2026; the MNT-Halan transaction release of 9 June 2026; and the '
        'exchange price library. Every figure in this table is read from the study’s committed record.')

# ================= §1 Fundamental ===========================================
H1('1  Fundamental valuation')

# [R-DOC-03] THE TWO DATES, AT THE TOP, LABELLED. Resolved by engine/doc_dates.py and
# never from a file's modification time.
import sys as _sys_dd
import os as _os_dd
_sys_dd.path.insert(0, _os_dd.path.dirname(_os_dd.path.dirname(_os_dd.path.abspath(__file__))))
import doc_dates as _DD
P(_DD.header_line('GBCO'), size=8, color=GREY)

P('We value GB Corp as an operating company with a captive finance arm and split the legs: blending an auto '
  'assembler-distributor, a leveraged lender and an unlisted fintech associate into one multiple would blur three different '
  'economics. The primary lens for this class is therefore a sum of the parts — the Auto operating leg on a free-cash-flow '
  'model; GB Capital on the residual income its own disclosed return supports, against its own operating equity; and the '
  'associate stakes on the two bases GB Corp itself discloses. That lens is the answer. A relative-multiple read and the '
  'disclosed book value are published beside it as cross-checks and carry no weight in it: a number produced by averaging '
  'several methods is a new method with parameters nobody tested, wearing the appearance of caution.')

H2('1.1  The sum of the parts — the primary lens, and both of its branches')
P(f'Each leg is marked on the basis that fits it. The Auto leg takes the §1.2 cash-flow value. GB Capital is marked by '
  f'residual income in its terminal form — the return the segment earns above the cost of that equity, capitalised — on '
  f'the segment’s own shareholders’ equity before minority interests LESS the associate holdings carried inside it, so the '
  f'stake this table adds back at its own mark is not also funding the lender. On a reviewed return of '
  f'{pc(CAP["roe_adopted"],2)} against a terminal cost of equity of {pc(CAP["ke_terminal"],2)} that justifies '
  f'{CAP["justified_pb"]:.2f}× of the EGP {n0(CAP["operating_equity"])} mn operating equity. The associates are the '
  f'branch: MNT-Halan is carried at EGP {n0(MARK_LO)} mn in the reviewed balance sheet at 30 June 2026 and marks at EGP '
  f'{n0(MARK_HI)} mn on GB Corp’s stated {pc(STAKE,2)} of the US${sotp["mnt_halan_round_usd"]:,.0f} mn June-2026 round at '
  f'EGP/USD {sotp["egp_usd"]:.1f}. Both are the company’s own numbers. NOTHING IS DEDUCTED FOR COMPLEXITY: a conglomerate '
  'discount is a parameter with nothing observable behind it, and the uncertainty it used to stand in for is in the '
  'associate line, where it is now published as two branches rather than smuggled into one.')
rows = [
 ['Leg', 'Basis', 'Carrying-value branch (EGP mn)', 'Round-price branch (EGP mn)'],
 ['GB Auto operating leg', 'Free-cash-flow model (§1.2), after the leg’s own net debt and minority interests', n0(sotp['auto_eq']), n0(sotp['auto_eq'])],
 ['Plus GB Capital lending leg', 'Residual income on the segment’s own operating equity (the multiple and the base are in the paragraph above)', n0(sotp['cap_val']), n0(sotp['cap_val'])],
 ['Plus associate — MNT-Halan', 'Reviewed carrying value · the June-2026 round at the stated stake', n0(MARK_LO), n0(MARK_HI)],
 ['Plus other associates (Bedaya, Kaf)', 'Residual carrying value, identical in both branches', n0(sotp['other_assoc']), n0(sotp['other_assoc'])],
 ['Sum of the parts — equity value', 'no discount is applied to either branch', n0(EQ_LO), n0(EQ_HI)],
 ['Equity value per share (EGP)', 'the two answers this study publishes', f"{V_LO:.2f}", f"{V_HI:.2f}"],
 ['Against the price', f"EGP {spot:.2f}, {SPOT_DATE}", sgn(GAP_LO), sgn(GAP_HI)],
]
table(rows, [2.0, 2.9, 1.15, 1.15], first_col_bold=True, band_rows=[5, 6])
# THE PAGE GIVES A READER AN INSTRUCTION AND THE INSTRUCTION HAS TO WORK. Both columns of
# the table above are asserted to reach the equity value they print, from the rows printed
# above them and nothing else.
for _mk, _eq, _lbl in ((MARK_LO, EQ_LO, 'carrying-value branch'), (MARK_HI, EQ_HI, 'round-price branch')):
    TR.waterfall(sotp['auto_eq'],
                 [('Plus GB Capital lending leg', sotp['cap_val']),
                  ('Plus associate — MNT-Halan', _mk),
                  ('Plus other associates (Bedaya, Kaf)', sotp['other_assoc'])],
                 _eq, dp=0, what='§1.1 sum of the parts, %s' % _lbl)
rich([(f"Two answers, EGP {V_LO:.2f} and {V_HI:.2f} per share", dict(bold=True)),
      (f", and no number between them. The gap between the branches is EGP "
       f"{(MARK_HI-MARK_LO)/1000:.1f} bn, {pc((MARK_HI-MARK_LO)/EQ_HI,1)} of the higher answer. "
       "Averaging them would produce a figure neither of GB Corp's disclosures supports, and "
       "applying a discount to bridge them would be the free parameter this edition removed "
       "arriving under a new name. What the market does with the same line is the subject of "
       "§1.7 and §7.", {})])

H2('The ownership percentage — two figures for one transaction, and both are printed')
P(f'GB Corp’s press release of 9 June 2026 states the holding directly: {pc(STAKE,2)}, against {pc(STAKE_PRIOR,2)} '
  f'before that transaction. Its own reviewed statements to 30 June 2026, and the review report on them, give '
  f'{pc(STAKE_STATEMENTS,2)} from {pc(STAKE_STATEMENTS_PRIOR,2)} for what is plainly the same transaction — most likely a '
  f'different level of the structure, the intermediate holding vehicle rather than the operating group. This study adopts '
  f'{pc(STAKE,2)}, because it is the figure the round it is applied to was announced with, and prints the other rather '
  f'than leaving it out. The difference is worth {pc(_STAKE_FORK["moves_the_round_branch_by"],2)} of the round-price '
  'branch and exactly nothing on the carrying-value branch, whose mark is a pound figure off a pound balance sheet.',
  size=9.8)

H2('What the associate mark is worth inside this valuation')
P('Because this single line carries the whole disagreement, here is its exact footprint on both of the company’s own '
  'bases:', size=9.8, space_after=4)
rows = [
 ['MNT-Halan inside the GBCO valuation', 'Carrying-value branch', 'Round-price branch'],
 ['The mark (EGP mn)', n0(MARK_LO), n0(MARK_HI)],
 ['MNT-Halan as a whole, implied (US$ mn)', f"{MNT_USD_AT_CARRYING:,.0f}", f"{sotp['mnt_halan_round_usd']:,.0f}"],
 ['Per share (EGP)', f"{MARK_LO/SH:.2f}", f"{MARK_HI/SH:.2f}"],
 ['Share of the equity value on that branch', pc(MARK_LO/EQ_LO, 0), pc(MARK_HI/EQ_HI, 0)],
 [f"Share of the traded market capitalisation (EGP {D['mktcap']/1000:,.1f} bn)", pc(MARK_LO/D['mktcap'], 0), pc(MARK_HI/D['mktcap'], 0)],
 ['What the traded price leaves for ALL the associates (EGP mn)', n0(PRICE_ASSOC), n0(PRICE_ASSOC)],
 ['— that is a discount to this branch’s associates line of', pc(1 - PRICE_ASSOC/(MARK_LO+sotp['other_assoc']), 1), pc(1 - PRICE_ASSOC/sotp['assoc'], 1)],
 ['What it leaves for MNT-Halan alone, the others held at carrying value (EGP mn)', n0(PRICE_MARK), n0(PRICE_MARK)],
]
table(rows, [3.2, 1.95, 1.95], first_col_bold=True, size=9.0)
caption('The last three rows are the same arithmetic read backwards and they are a DIAGNOSTIC, not an input: the market '
        'capitalisation less this study’s marks on the two operating legs is what the price leaves over for the associates. '
        'Nothing solved from the price enters the valuation above it.')

H2('The mark ladder — what each level of the associate mark is worth per share')
P('The stake itself is not the open question; the company has stated it. What is open is the basis on which a minority '
  'interest in an unlisted company should be carried. The ladder below prices that question directly, holding every other '
  'line at its published value:', size=9.8)
_ladder = {MARK_LO: 'the reviewed carrying value at 30 June 2026 — the LOWER published branch',
           MARK_HI: 'the June-2026 round at the stated stake — the HIGHER published branch',
           PRICE_MARK: 'what the traded price leaves for MNT-Halan alone, the other associates held at carrying value'}
for _f in (0.25, 0.50, 0.75):
    _ladder.setdefault(MARK_HI * _f, '')
_ladder = sorted(_ladder.items())
rows = [['MNT-Halan mark (EGP mn)', 'MNT-Halan as a whole (US$ mn)', 'Sum of the parts (EGP/share)', 'Note']]
for _m, _note in _ladder:
    rows.append([n0(_m), f"{_m/(STAKE*sotp['egp_usd']):,.0f}",
                 f"{sotp_per_share(_m):.2f}", _note])
table(rows, [1.55, 1.6, 1.5, 2.45], first_col_bold=True, size=8.8)
caption('Every row recomputes the whole sum of the parts at that mark; the auto leg, the lender and the other associates '
        'are held exactly where §1.2 and this section publish them. The two published branches are the two rows the note '
        'column names, and the top row is the mark the traded price itself implies — which is why it reproduces the '
        'traded price exactly.')

H2('1.2  The Auto-leg cash-flow model')
_cs = DRV['cost_stack']
P(f'The Auto leg is built bottom-up on disclosed units × average selling price per line of business: volumes and '
  f'revenue are published per line, so the price is arithmetic rather than an assumption, and the driver table is in §1.6 '
  f'and Appendix A. Gross margin opens at {pc(_cs["gross_margin"][0],2)} and settles at '
  f'{pc(_cs["gross_margin"][-1],2)}; selling and administrative cost holds near {pc(_cs["gsa_pct"][0],1)} of revenue; '
  f'capital expenditure follows the EGP {_cs["capex"][0]:,.0f} mn guided for the first year and then normalises; and the '
  f'crux — net working capital — glides from {pc(_cs["working_capital_pct"][0],1)} of revenue to '
  f'{pc(_cs["working_capital_pct"][-1],1)} as the payables re-extension completes and the Sadat stock build unwinds. The '
  'cost of capital is not one crisis rate held for ever: it is a schedule, built through the house cost-of-capital module '
  f'from a normalised risk-free rate of {pc(COC["rf_star"],2)}, a regression beta of {COC["beta"]:.4f} and an equity risk '
  f'premium of {pc(COC["erp"],2)}, gliding from {pc(COC["wacc_exp"],2)} in the first forecast year to a norm-built terminal '
  f'of {pc(COC["wacc_terminal"],2)}. Terminal growth is stored as a REAL rate of '
  f'{pc(MAC["terminal_growth_real"],1)} on the house Egyptian inflation path and recomputes to '
  f'{pc(MAC["terminal_growth_nominal"],2)} nominal; it is not a typed nominal figure. §1.8 carries the whole build.')
rows = [['EGP mn'] + [r['year'] for r in dcf['rows']]]
labels = [('rev', 'Auto revenue'), ('ebitda', 'Operating profit before depreciation'),
          ('dna', 'Depreciation & amortisation'), ('ebit', 'Operating profit'),
          ('nopat', f"Operating profit after tax at {pc(_cs['tax_rate'],0)}"),
          ('dna', 'Plus depreciation & amortisation'), ('capex', 'Less capital expenditure'),
          ('dwc', 'Less increase in working capital'), ('fcff', 'Free cash flow to the firm'),
          ('df', 'Discount factor'), ('pv', 'Present value of free cash flow')]
for key, lbl in labels:
    row = [lbl]
    for rrow in dcf['rows']:
        v = rrow[key]
        if key == 'df':
            row.append(f"{v:.3f}")
        elif key in ('capex', 'dwc'):
            row.append(paren(v))
        elif key == 'dna' and lbl.startswith('Depreciation'):
            row.append(paren(v))
        else:
            row.append(n0(v))
    rows.append(row)
table(rows, [2.1, 1.0, 1.0, 1.0, 1.0, 1.0], first_col_bold=True, size=8.9)
for _r in dcf['rows']:
    TR.waterfall(_r['nopat'],
                 [('Plus depreciation & amortisation', _r['dna']),
                  ('Less capital expenditure', _r['capex']),
                  ('Less increase in working capital', _r['dwc'])],
                 _r['fcff'], dp=0, what='§1.2 free cash flow, %s' % _r['year'])
caption('The discount factors are the cost-of-capital schedule’s own cumulative factors, one forward rate per year; '
        'they are not a single rate compounded. Deductions are printed as magnitudes in brackets and the labels state the '
        'operation, so the column can be followed from operating profit after tax to free cash flow.')

rows = [
 ['Bridge to the Auto leg’s equity value', 'EGP mn'],
 ['Σ present value of explicit free cash flow', n0(dcf['pv_sum'])],
 [f"Terminal value at {pc(MAC['terminal_growth_nominal'],2)} nominal growth", n0(dcf['tv'])],
 ['Present value of the terminal value', n0(dcf['pv_tv'])],
 ['Enterprise value — Auto leg', n0(dcf['ev'])],
 ['Terminal value as a share of enterprise value', pc(dcf['tv_pct'], 0)],
 ['less: Auto net debt', paren(dcf['auto_nd'])],
 ['less: Auto non-controlling interests', paren(dcf['auto_nci'])],
 ['Auto equity value', n0(dcf['auto_eq'])],
]
table(rows, [4.0, 1.6], first_col_bold=True)
TR.waterfall(dcf['ev'],
             [('less: Auto net debt', dcf['auto_nd']),
              ('less: Auto non-controlling interests', dcf['auto_nci'])],
             dcf['auto_eq'], dp=0, what='§1.2 enterprise-to-equity bridge')
P(f"Two honesty notes. First, {pc(dcf['tv_pct'],0)} of the enterprise value sits in the terminal value — this is a "
  "growth-and-rates bet dressed as a five-year model, which is why §1.9 sensitises the discount-rate and terminal-growth "
  f"grid rather than hiding it. Second, the explicit-period cash flow is thin in the first year (EGP "
  f"{dcf['rows'][0]['fcff']:,.0f} mn) precisely because growth consumes working capital; the value is in the steady state, "
  "not the ramp. Both are disclosed rather than blended away.")
P('A third note, and it is a refusal rather than a caveat. The house standard is that a terminal rests on a DISCLOSED '
  'asset life, and no usable life could be sourced for this company: the accounting-policy note discloses rate RANGES by '
  'asset class rather than a scalar, and the identity route — recovering an implied life from the property, plant and '
  'equipment note — returns a span that depends on an undisclosed land split and produces per-class rates that '
  'contradict the disclosed bands. A life this desk chose would not be a disclosed life, so none was chosen; the terminal '
  'is carried on the construction described above and the refusal is recorded rather than papered over. Appendix B\u2019s '
  'research register carries that search among this study\u2019s negative results.', size=9.6)

H2('1.3  Relative multiples — a cross-check, on the company’s own history')
_r = LI['relative']
P(f"On the model's own forward build — group net profit attributable of EGP {n0(_r['np_fy26e'])} mn in the first "
  f"forecast year, earnings per share of EGP {_r['eps_fy26e']:.2f} — GB Corp trades at "
  f"{_r['traded_pe']:.2f}× forward earnings. The multiple applied here is NOT that one, and the distinction is the whole "
  f"point of the lens: a multiple taken off the current price values the company at what it already trades at. It is the "
  f"MEDIAN of GB Corp’s own trailing multiple at its last three year-end closes — "
  f"{' · '.join('%.2f×' % v for v in _r['pe_observed'])} — which is {_r['pe']:.2f}×. "
  f"THAT IS {_r['observations']} OBSERVATIONS, and the count is published with the median because a median of three is a "
  "thin statistic and a reader is entitled to know how thin. The lens returns one value rather than a range, because a "
  "range around a median of three would be an invented spread.")
rows = [
 ['Relative basis', 'Value'],
 ['FY2026E group net profit attributable (EGP mn)', n0(_r['np_fy26e'])],
 ['Divided by shares in issue (mn)', n1(SH)],
 ['Earnings per share (EGP)', f"{_r['eps_fy26e']:.2f}"],
 ['Times the multiple applied — the median of the company’s own three year-end closes', f"{_r['pe']:.2f}×"],
 ['Fair value per share (EGP)', f"{REL['value']:.2f}"],
 ['Memo — the multiple the traded price implies on the same earnings', f"{_r['traded_pe']:.2f}×"],
]
table(rows, [4.3, 1.8], first_col_bold=True)
TR.waterfall(_r['np_fy26e'], [('Divided by shares in issue (mn)', SH)],
             _r['eps_fy26e'], dp=2, what='§1.3 earnings per share')
TR.waterfall(_r['eps_fy26e'], [('Times the multiple applied', _r['pe'])],
             REL['value'], dp=2, what='§1.3 relative fair value')
rich([(f"Relative cross-check EGP {REL['value']:.2f}", dict(bold=True)),
      (f' — {sgn(REL["value"]/spot-1)} against the price, and the most conservative read in the study: it pays for one '
       "year's earnings on the company's own historical rating and gives nothing at all for the working-capital release "
       f"or the associate stake. It is a CROSS-CHECK. It carries no weight in the answer, and the reason is that the "
       "largest asset on GB Corp's balance sheet contributes to its earnings only through an equity-accounted share of "
       "profit that the reviewers of those very statements could not verify.", {})])

H2('1.4  Earnings power — why this class carries no normalised-earnings lens, and the book floor instead')
P('A normalised-earnings read — mid-cycle profit times a through-cycle multiple — is a lens this study does NOT carry, '
  'and the reason is specific to this issuer rather than a matter of taste. Normalising earnings means averaging out the '
  'cycle to find the level a business can sustain. GB Corp’s reported earnings do not swing with an operating cycle '
  'alone: they swing with what its associates are marked at.', size=10.5)
P(f'The company’s own filed record makes the point. Its share of associates’ results ran EGP {n1(HIS["2023"]["associates"])} mn, '
  f'{n1(HIS["2024"]["associates"])} mn and {n1(HIS["2025"]["associates"])} mn in FY2023, FY2024 and FY2025 — that is '
  f'{pc(HIS["2023"]["associates"]/HIS["2023"]["net_profit"],0)}, {pc(HIS["2024"]["associates"]/HIS["2024"]["net_profit"],0)} '
  f'and {pc(HIS["2025"]["associates"]/HIS["2025"]["net_profit"],0)} of profit attributable to the parent in those years, '
  'and the quarterly figures behind them move by a large multiple from one quarter to the next. On top of that sits a '
  'revaluation booked on deconsolidating an associate, which GB Corp itself strips out of its own return measure. '
  'A mid-cycle average of a series driven by that is an average of marks, not of trading. Normalising earnings that swing '
  'on associate marks normalises noise, and a lens built on it would look precise and mean nothing.', size=10.5)
P('What is published in its place is the figure that needs no normalisation at all, because the company discloses it '
  'directly:', size=9.8, space_after=4)
rows = [
 ['The disclosed book floor', 'Value'],
 ['Shareholders’ equity before minority interests, 30 June 2026 (EGP mn)', n1(BOOK_EQUITY)],
 ['Divided by shares in issue (mn)', n1(SH)],
 ['Book value per share (EGP)', f"{BOOK['value']:.2f}"],
 ['Memo — total equity including minority interests, same date (EGP mn)', n1(D['inputs']['eq_jun2026']['value'])],
 ['The traded price against book', f"EGP {spot:.2f}, {sgn(spot/BOOK['value']-1)}"],
]
table(rows, [4.3, 1.8], first_col_bold=True)
TR.waterfall(BOOK_EQUITY, [('Divided by shares in issue (mn)', SH)],
             BOOK['value'], dp=2, what='§1.4 book value per share')
rich([(f"Book value EGP {BOOK['value']:.2f} per share, and the shares trade below it", dict(bold=True)),
      (f' — {sgn(spot/BOOK["value"]-1)}. This is a DISCLOSED FLOOR and it carries no weight in any answer above; book is '
       'struck at historical cost and says nothing about what a business earns. It is worth printing for one reason: a '
       'reader who distrusts every forecast in this document, every multiple and both bases for the associate mark can '
       'still observe that the market is paying less than the accounting value of the equity — and that book value '
       'itself contains the associate at the lower of the two marks, not the higher.', {})])

H2('1.5  Synthesis — one primary, two branches, and the cross-checks beside them')
P('There is no weighted blend in this study and no central estimate. The class primary is the sum of the parts and it IS '
  'the answer; the relative multiple and the disclosed book value are cross-checks, published in the same table so a '
  'reader can see the disagreement rather than an average of it. The primary has two branches because one input has two '
  'company-published values and the filings do not choose; the branches are carried to the end and printed side by side. '
  'The envelope below is the RANGE OF THE READS on one clock — the two branches and the relative multiple — and it is '
  'not a spread invented around a central, because there is no central to invent one around.')
rows = [['Read', 'Role', 'EGP per share', 'Against the price'],
 ['Sum of the parts — carrying-value branch', 'Class primary — the answer', f"{V_LO:.2f}", sgn(GAP_LO)],
 ['Sum of the parts — round-price branch', 'Class primary — the answer', f"{V_HI:.2f}", sgn(GAP_HI)],
 ['Relative multiple on FY2026E earnings', 'Cross-check', f"{REL['value']:.2f}", sgn(REL['value']/spot-1)],
 ['Disclosed book value', 'Cross-check — a floor', f"{BOOK['value']:.2f}", sgn(BOOK['value']/spot-1)],
 ['Envelope of the present-value reads', 'the range, never an average', f"{ENVELOPE['low']:.2f} – {ENVELOPE['high']:.2f}", f"{sgn(ENVELOPE['low']/spot-1)} to {sgn(ENVELOPE['high']/spot-1)}"],
]
table(rows, [2.5, 1.7, 1.35, 1.35], first_col_bold=True, band_rows=[5])
caption('The envelope spans the present-value reads — both branches of the primary and the relative multiple. The '
        'disclosed book value is a floor and is deliberately not in it: a floor is not a valuation.')
figure('fig1_football.png', 6.3, 'Figure 1 — Valuation football field. The primary lens is drawn as the span between its '
       'two branches with a brass tick on each; the cross-checks are single marks; the gold band is the envelope of the '
       'present-value reads; the ink line is the price.')
rich([(f"The answer is EGP {V_LO:.2f} on one of the company’s disclosures and EGP {V_HI:.2f} on the other", dict(bold=True)),
      (f", {sgn(GAP_LO)} and {sgn(GAP_HI)} against the price. The width of this picture is not four independent methods "
       f"converging or failing to converge. Two of the marks — the primary’s branches — differ only in the associate "
       f"line, and the two cross-checks do not touch that line at all: the earnings multiple reads EGP {REL['value']:.2f} "
       f"and the disclosed book floor EGP {BOOK['value']:.2f}, both within {max(abs(REL['value']/spot-1), abs(BOOK['value']/spot-1))*100:.0f}% "
       "of the traded price. That split is itself the finding, and it is the same finding on either branch: strip the "
       "associate out and this is an operating group priced about where its own earnings and its own book say it should "
       "be; put it back at either company-published mark and the shares look cheap.", {})])

H2('1.6  The legs, and the units × price driver table')
rows = [
 ['Leg', 'Cyclicality', 'Margin / return trend', 'Capital intensity', 'Swing role'],
 ['GB Auto — passenger cars', 'High (rates, currency, imports)', f"Auto gross margin {pc(D['forecast_anchor']['latest_reviewed_rate'],2)} in the reviewed half; the forecast opens at {pc(_cs['gross_margin'][0],2)}", 'Very high (working capital)', 'Dominant'],
 ['GB Auto — commercial vehicles, trading, mobility', 'Moderate', 'Bus exports scaling', 'Moderate', 'Diversifier'],
 ['GB Capital', 'Credit cycle', f"Reviewed return on operating equity {pc(CAP['roe_adopted'],2)}", 'Leveraged by construction', 'Compounder'],
 ['Associates (MNT-Halan and others)', 'Venture-like', 'Two company-published marks; no public price', 'Off balance sheet', 'The whole disagreement'],
]
table(rows, [1.9, 1.2, 1.9, 1.35, 0.85], first_col_bold=True, size=8.7)
P('The bottom-up build. Every historical figure below is the company’s own disclosure; the forecast columns are the '
  'model’s own driver path:', size=9.8)
fc = D['forecast']
_pcv = DRV['pc_volume_units']; _pcr = DRV['pc_revenue']; _pca = DRV['pc_asp']
rows = [['Driver', 'FY2023', 'FY2024', 'FY2025', 'FY2026E', 'FY2030E'],
 ['Passenger-car volume (units)', f"{_pcv['FY23']:,}", f"{_pcv['FY24']:,}", f"{_pcv['FY25']:,}", f"{fc['FY26E']['pc_vol']:,.0f}", f"{fc['FY30E']['pc_vol']:,.0f}"],
 ['Passenger-car price (EGP mn/unit)', f"{_pca['FY23']:.2f}", f"{_pca['FY24']:.2f}", f"{_pca['FY25']:.2f}", f"{fc['FY26E']['pc_asp']:.2f}", f"{fc['FY30E']['pc_asp']:.2f}"],
 ['Passenger-car revenue (EGP mn)', n0(_pcr['FY23']), n0(_pcr['FY24']), n0(_pcr['FY25']), n0(fc['FY26E']['pc_rev']), n0(fc['FY30E']['pc_rev'])],
 ['Commercial vehicles & equipment', '—', '—', n0(DRV['cv_revenue']['FY25']), n0(fc['FY26E']['cv_rev']), n0(fc['FY30E']['cv_rev'])],
 ['Light mobility', '—', '—', n0(DRV['lm_revenue']['FY25']), n0(fc['FY26E']['lm_rev']), n0(fc['FY30E']['lm_rev'])],
 ['Trading (tires and parts)', '—', '—', n0(DRV['trading_revenue']['FY25']), n0(fc['FY26E']['tr_rev']), n0(fc['FY30E']['tr_rev'])],
 ['GB Auto total revenue', '—', '—', n0(DRV['auto_revenue_fy2025']), n0(fc['FY26E']['auto_rev']), n0(fc['FY30E']['auto_rev'])],
]
table(rows, [2.2, 0.95, 0.95, 0.95, 1.0, 1.0], first_col_bold=True, size=8.9)
caption('Sources: the company’s own FY2023, FY2024 and FY2025 earnings releases, segment volume and revenue tables. '
        'A dash marks a line the study’s committed record does not carry for that year rather than a nil figure — '
        'the segment split is disclosed for the base year and this study does not reconstruct the earlier years it did not '
        'source. The forecast columns are the model’s own driver path.')

H2('1.7  The crux: the basis of the associate mark, then cash conversion and the rate path')
P(f'Three judgments drive this valuation, in order of size. First and by a wide margin: not what GB Corp’s MNT-Halan '
  f'stake IS — the company stated it — but on what BASIS a minority interest in an unlisted company should be carried. '
  f'The two the company itself publishes are EGP {n0(MARK_LO)} mn and EGP {n0(MARK_HI)} mn, a difference of '
  f'{pc((MARK_HI-MARK_LO)/EQ_HI,1)} of the higher answer, and this study does not choose between them. '
  f'What the traded price implies for that line is EGP {n0(PRICE_ASSOC)} mn for ALL the associates together — a discount '
  f'of {pc(1-PRICE_ASSOC/(MARK_LO+sotp["other_assoc"]),1)} to the reviewed carrying value and '
  f'{pc(1-PRICE_ASSOC/sotp["assoc"],1)} to the round-price read. A discount of that size to a private round is arguable; '
  'a discount of that size to a figure a reviewing accountant has signed a balance sheet on is a different claim, and it '
  'is the one the market is making. Second, where Auto working-capital intensity settles: it is modelled from '
  f'{pc(_cs["working_capital_pct"][0],1)} of revenue down to {pc(_cs["working_capital_pct"][-1],1)}, and because the auto '
  'leg’s free cash flow is a thin residual, that path moves it directly — §1.9 prices the grid rather than a single '
  f'point estimate. Third, the Egyptian nominal-rate path: the schedule glides from {pc(COC["wacc_exp"],2)} to '
  f'{pc(COC["wacc_terminal"],2)} against terminal growth of {pc(MAC["terminal_growth_nominal"],2)}, a terminal real '
  f'spread of {pc(COC["wacc_terminal"]-MAC["terminal_growth_nominal"],2)}. A fourth exposure is regional: part of '
  'passenger-car revenue is Iraq and Jordan, where conflict has already cut volumes, and this study does not hold a '
  'sourced split of that revenue for the reviewed half, so it is named as an exposure and not priced.')
rich([('And the same gap asked of a different input does not look nearly so stark. ', dict(bold=True)),
      (f'The paragraph above solves the price for the associate mark, which is the input the two branches actually differ '
       f'in. Solve it instead for the auto leg’s cost of capital, holding every other line at its published value, and the '
       f'traded price implies {pc(RATE_HI,2)} against this study’s {pc(dcf["wacc"],2)} on the round-price branch — '
       f'{(RATE_HI-dcf["wacc"])*100:.1f} points, a stretch on a leg worth less than half the sum of the parts — but only '
       f'{pc(RATE_LO,2)} on the carrying-value branch, {(RATE_LO-dcf["wacc"])*100:.1f} points, which is an ordinary '
       'disagreement about the cost of capital in this market. A reader is entitled to both readings, and on the branch '
       'this study can most easily defend the market is not making an extraordinary claim at all. Neither figure is used '
       'anywhere in the valuation; both are solved from it.', {})], size=9.8)

H2('1.8  Macro and country — rates, the pound, and the cost of capital')
P(f'GB Corp is a leveraged play on Egyptian nominal normalisation. Every cut lowers GB Capital’s funding cost on a '
  f'fixed-rate lending book, lowers the customer’s instalment, and compresses the discount rate this study applies. '
  f'The pound sets assembly input costs and the pound value of the MNT-Halan round-price mark; a step devaluation is the '
  f'single nastiest macro scenario for both margin and multiple. The cost-of-capital build below is produced by the house '
  f'module rather than assembled by hand, and the whole schedule is published — not one rate held for ever:', size=10.5)
rows = [
 ['Cost-of-capital build', 'Value', 'Source'],
 ['Observed risk-free rate', pc(COC['rf_observed'], 2), 'Egypt 10-year local-currency government bond yield, house macro path'],
 ['less: Egypt’s own sovereign default spread', pc(COC['default_spread'], 2), 'so country risk is counted exactly once, inside the premium below'],
 ['Normalised risk-free rate', pc(COC['rf_star'], 2), 'the difference of the two rows above'],
 ['Equity beta', f"{COC['beta']:.4f}", 'own-stock weekly regression against the published EGX30 index'],
 ['Equity risk premium (market basis, adopted)', pc(COC['erp'], 2), 'the sovereign’s own row, read for this country'],
 ['Equity risk premium (rating basis, alternative)', pc(D['cost_of_capital_rating_basis']['erp'], 2), 'same source, rating-based column; published beside the adopted basis'],
 ['Cost of equity, explicit window', pc(COC['ke_exp'], 2), f"reproduces from the normalised rate plus beta times the premium; {pc(D['cost_of_capital_rating_basis']['ke_exp'],2)} on the rating basis"],
 ['Cost of equity, terminal', pc(COC['ke_terminal'], 2), 'the rate the lender’s residual income is capitalised at in §1.1'],
 ['Pre-tax cost of debt', pc(COC['kd_pretax'], 2), 'the company’s own effective borrowing rate, computed on the borrowings that actually bear the interest'],
 ['After-tax cost of debt', pc(COC['kd_aftertax'], 2), 'debt is entirely local-currency on the disclosed facility note'],
 ['Weights (equity / debt)', f"{pc(COC['weight_equity'],1)} / {pc(COC['weight_debt'],1)}", 'market capitalisation against disclosed borrowings'],
 ['Weighted cost of capital, first forecast year', pc(COC['wacc_exp'], 2), f"{pc(D['cost_of_capital_rating_basis']['wacc_exp'],2)} on the rating-based alternative"],
 ['Weighted cost of capital, terminal', pc(COC['wacc_terminal'], 2), 'norm-built, reached by a glide inherited from the policy-rate path'],
 ['Terminal growth (real, then nominal)', f"{pc(MAC['terminal_growth_real'],1)} → {pc(MAC['terminal_growth_nominal'],2)}", 'stored as a real rate on the house inflation path and recomputed; never typed as a nominal figure'],
]
table(rows, [2.6, 1.3, 3.0], first_col_bold=True, size=8.7)
P('Three honesty notes on this build. First, the beta is the stock’s own regression against the published index of '
  f'the exchange it is listed on — {COC["beta"]:.4f}, on weekly observations over nearly five years, clearing the '
  'minimum sample, explanatory power and precision required before a regression beta may be used at all — and it '
  'replaces an assumed unit beta the superseded edition carried because an earlier attempt on five annual observations '
  'was unusable. Second, the country risk enters exactly once: the observed local yield is reduced '
  'by this sovereign’s own default spread and the premium added back carries the country risk, rather than the raw '
  'yield being combined with a country-loaded premium. Third, both premium bases are published and the market basis is '
  'named as the adopted one; the rating basis is shown beside it rather than averaged into it.', size=9.6)
_stale = MAC.get('anchor_staleness_accepted')
if _stale:
    P('Disclosed staleness of the macro anchors: ' + _outward(_stale), size=9.2,
      italic=True, color=GREY)

H2('1.9  Sensitivity — the mark, the rate path, and terminal growth')
P('The crux is priced first, and on its own axes. The grid below re-prices the whole sum of the parts across the two '
  'things this study cannot settle from the filings: what MNT-Halan is worth, and what the auto leg’s operations should '
  'be discounted at. Every other line is held exactly where it is published. There is no complexity-discount axis, '
  'because this study applies no complexity discount — the uncertainty that a discount used to stand in for is the '
  'vertical axis of this grid.')
_wshift = [-0.02, -0.01, 0.0, 0.01, 0.02]
_mfrac = [0.25, 0.50, 0.75, 1.00]
_mark_rows = sorted({MARK_LO, MARK_HI} | {MARK_HI * f for f in _mfrac})
rows = [['MNT-Halan mark (EGP mn) \\ first-year cost of capital']
        + [pc(dcf['forward_wacc'][0] + s, 1) for s in _wshift]]
for _m in _mark_rows:
    row = [n0(_m) + ('  ‡' if abs(_m - MARK_LO) < 1 or abs(_m - MARK_HI) < 1 else '')]
    for s in _wshift:
        v = sotp_per_share(_m, s)
        row.append('n.m.' if v is None else f'{v:.1f}')
    rows.append(row)
table(rows, [2.35, 0.85, 0.85, 0.85, 0.85, 0.85], first_col_bold=True, size=8.8)
_cells = [sotp_per_share(_m, s) for _m in _mark_rows for s in _wshift]
_cells = [c for c in _cells if c is not None]
caption(f"Sum-of-the-parts fair value, EGP per share, spanning EGP {min(_cells):.1f} to {max(_cells):.1f} across the grid. "
        f"The two rows marked ‡ are the study’s two published branches; the centre column is the model’s own first-year "
        f"cost of capital of {pc(dcf['wacc'],2)}. The rate axis shifts the WHOLE schedule, explicit years and terminal "
        f"together, because moving one rate and not the others would price one date at two prices.")
figure('fig2_sens.png', 5.6,
       'Figure 2 — the same grid drawn. Rows are the MNT-Halan mark, columns the first-year cost of capital on the auto '
       'leg; the two published branches are the marked rows.')
import numpy as np                                                   # noqa: E402
fcffs = [r['fcff'] for r in dcf['rows']]
base_wacc = dcf['wacc']
_TG = MAC['terminal_growth_nominal']
_gs = [_TG - 0.02, _TG - 0.01, _TG, _TG + 0.01, _TG + 0.02]
P('The second grid holds the associate at the round-price branch and moves the rate path against terminal growth:',
  size=9.8, space_before=6)
wg_rows = [['Cost of capital \\ terminal growth'] + [pc(g, 1) for g in _gs]]
for s in _wshift:
    row = [pc(base_wacc + s, 1)]
    for g in _gs:
        v = sotp_per_share(MARK_HI, s, tg=g)
        row.append('n.m.' if v is None else f'{v:.1f}')
    wg_rows.append(row)
table(wg_rows, [1.9, 0.95, 0.95, 0.95, 0.95, 0.95], first_col_bold=True, size=9.0)
caption(f"Sum-of-the-parts fair value on the round-price branch, EGP per share. The centre cell, {pc(base_wacc,1)} against "
        f"{pc(_TG,1)}, is EGP {V_HI:.1f} — the published branch. Both axes are centred on the model's own build rather "
        f"than on round numbers. On the carrying-value branch every cell is EGP "
        f"{(MARK_HI-MARK_LO)/SH:.2f} lower, because the branches differ by a constant.")

# ================= §2 Technical ==============================================
H1('2  Technical and price structure')
_above = [n for n in ('20', '50', '100', '200') if TA_CLOSE > tech['sma'][n]]
_below = [n for n in ('20', '50', '100', '200') if TA_CLOSE <= tech['sma'][n]]
P(f'The technical read is computed on the exchange library’s own last session — EGP {TA_CLOSE:.2f} on '
  f'{TA_DATE_L} — which is a different and older clock than the price the valuation is struck on. On that session the '
  f'price sat below the {"- and ".join(_below)}-day averages and above the {"- and ".join(_above)}-day averages: the long '
  f'trend is intact and the short one has rolled over. The oscillator reads {tech["rsi"]:.1f}, below neutral and well above '
  f'oversold; the convergence histogram is {tech["macd"]["hist"]:+.2f}, so short-term momentum is negative. The 52-week '
  f'range runs EGP {tech["lo52"]:.2f} to {tech["hi52"]:.2f}, and the session sits '
  f'{pc((TA_CLOSE-tech["lo52"])/(tech["hi52"]-tech["lo52"]),0)} of the way up it.')
rows = [
 ['Indicator', 'Reading', 'Signal'],
 ['Close the read is computed on', f"EGP {TA_CLOSE:.2f} ({TA_DATE_L})", '—'],
 ['20-day / 50-day average', f"EGP {tech['sma']['20']:.2f} / {tech['sma']['50']:.2f}", f"Price {sgn(TA_CLOSE/tech['sma']['20']-1,1)} / {sgn(TA_CLOSE/tech['sma']['50']-1,1)} — short-term down"],
 ['100-day / 200-day average', f"EGP {tech['sma']['100']:.2f} / {tech['sma']['200']:.2f}", f"Price {sgn(TA_CLOSE/tech['sma']['100']-1,1)} / {sgn(TA_CLOSE/tech['sma']['200']-1,1)} — long trend intact"],
 ['Relative strength (14)', f"{tech['rsi']:.1f}", 'Below neutral, above oversold'],
 ['Convergence (12,26,9)', f"line {tech['macd']['line']:+.2f} / signal {tech['macd']['signal']:+.2f} / histogram {tech['macd']['hist']:+.2f}", 'Negative — momentum has rolled'],
 ['52-week range', f"EGP {tech['lo52']:.2f} – {tech['hi52']:.2f}", f"{pc((TA_CLOSE-tech['lo52'])/(tech['hi52']-tech['lo52']),0)} of the way up the range"],
 ['Realised volatility (252 sessions)', pc(tech['rv252'], 1), 'Elevated but off crisis highs'],
]
table(rows, [2.0, 2.6, 2.5], first_col_bold=True)
figure('fig3_ma.png', 6.4, 'Figure 3 — Price versus the moving-average stack, last 260 sessions of the exchange library.')
P('For the probabilistic work this matters in one way. A tape that has come off its short averages with negative momentum '
  'thins the near-term upside tail rather than thickening it. The technical and fundamental pictures still disagree — '
  'the fundamental work says value has been reached on either branch and the tape says the market is not yet interested '
  '— and §6 reads the resulting probability zones without forcing a reconciliation between them.')
