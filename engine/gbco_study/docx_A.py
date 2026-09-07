"""Content part A: masthead → §2.

REBUILT 07-09-2026. Every financial numeral is READ from study_numbers.json (depth-bar
standard 3); the superseded edition typed its spot, its whole cost-of-capital table, its
terminal growth, its bridge deductions and three history columns straight into this file,
and the rebuild had moved every one of them.
"""
from docx_base import *

pr = D['mc']['prob_read']; q20, q60 = D['mc']['q20'], D['mc']['q60']
L = D['lenses']; tech = D['tech']; dcf = D['dcf']; sotp = D['sotp']
COC = D['cost_of_capital_record']; MAC = D['macro']; LI = D['lens_inputs']
HIS = D['history']['income_statement']; DRV = D['disclosed_drivers']
spot = D['spot']; spot_date_iso = D['spot_date']; SH = D['shares']
EDITION = D['edition']
# THE TECHNICAL READ SITS ON A DIFFERENT CLOCK FROM THE PRICE AND THE DOCUMENT SAYS SO.
# The averages, the oscillators and the 52-week range are computed on the exchange
# library's own last session; the valuation is struck on the latest price the repository
# knows. Quoting one against the other is the two-clocks error [R-ENF-03] names.
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

GAP = L['central']['base'] / spot - 1.0
STAKE = sotp['mnt_halan_stake']
STAKE_PRIOR = sotp['mnt_halan_stake_prior']


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
       f'later price above — two clocks, both dated · primary lens: split-the-legs '
       'sum-of-the-parts (operating company + captive lender) · the MNT-Halan stake mark '
       'remains the dominant swing factor, ahead of Auto cash conversion and the Egyptian '
       'nominal-rate path.', {})],
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
 ('', 'All values are model outputs presented as ranges and distributions because no single number should be relied on. '
      'Reported financials are the company’s own disclosure — the FY2023, FY2024 and FY2025 earnings releases and '
      'the reviewed consolidated statements to 30 June 2026; forward-looking inputs — the marks on GB Capital and the '
      'MNT-Halan stake, the complexity discount, the multiples, the cash-flow model and the simulation’s factor '
      'probabilities — are the preparer’s judgments and are flagged throughout. The far forecast years are '
      'published as ranges rather than points, taken from how wrong this method has been on this company’s own history; '
      'Appendix A carries the table and the count behind each band. A note on identity: GB Corp S.A.E. is the renamed GB '
      'Auto S.A.E. (Ghabbour Auto); the EGX ticker is GBCO and the price history continues the former AUTO listing. Consult '
      'a licensed financial advisor before any investment decision.'),
])

# ---------------- Headline ---------------------------------------------------
H2('Headline')
rich([('The model reads GB Corp below its central estimate, and the whole of that distance sits in one line nobody can trade. ',
       dict(bold=True)),
      (f'At EGP {spot:.2f} the shares sit {abs(GAP)*100:.0f}% below a central estimate of EGP '
       f'{L["central"]["base"]:.2f}. The four reads spread wider than usual: the split-the-legs '
       f'sum-of-the-parts lands at EGP {L["sotp"]["base"]:.2f} after a {pc(sotp["disc"],0)} complexity '
       f'discount (pre-discount EGP {sotp["prediscount_ps"]:.2f}); a relative read on forward earnings '
       f'marks EGP {L["relative"]["base"]:.2f}, essentially the traded price; and a normalised '
       f'mid-cycle read sits at EGP {L["normalized"]["base"]:.2f}. The disagreement is not four '
       'methods arguing about an operating business. It is two reads that carry GB Corp’s '
       'associate stake and two that do not. ', {}),
      (f'GB Corp’s own 9 June 2026 press release states its MNT-Halan holding directly — '
       f'{pc(sotp["mnt_halan_stake"],2)}, against {pc(STAKE_PRIOR,2)} before that transaction. Applied to the '
       f'round’s USD {sotp["mnt_halan_round_usd"]/1000:.1f} bn valuation at EGP/USD '
       f'{sotp["egp_usd"]:.1f}, the stake alone marks at EGP {sotp["mnt_halan_value"]/1000:.1f} bn — '
       f'{pc(sotp["mnt_halan_value"]/D["mktcap"],0)} of GB Corp’s entire market capitalisation. '
       'That is a confirmed, dated, company-stated figure rather than a sourcing gap, and it is what '
       'makes this study awkward rather than simply bullish: taken at face value it implies the market '
       'pays close to nothing for a profitable auto business that turned over EGP '
       f'{HIS["2025"]["revenue"]/1000:.1f} bn last year. Either the market applies a far steeper '
       f'discount to that private mark than this study’s {pc(sotp["disc"],0)}, or GB Corp is '
       'mispriced. This study does not settle which; §7 returns to it. ', {}),
      (f'The tape is no longer the counter-argument it was. On the library’s last session the price '
       f'sat below its twenty- and fifty-day averages, with the oscillator at {tech["rsi"]:.0f} and the '
       'moving-average convergence histogram negative — a stock that has come off, not one that is '
       f'extended. Over three months the simulation places the fifth-to-ninety-fifth percentile band at '
       f'roughly EGP {q60["5"]:.0f}–{q60["95"]:.0f} with a median near EGP {q60["50"]:.0f}; that '
       'engine prices the stock’s own path and is untouched by anything in the paragraph above.', {})],
     space_after=8)

# ---------------- Valuation summary table -----------------------------------
H2('Valuation summary — every read at a glance')
P('One table for the reads that follow — what the business is worth (fundamental), what the tape is doing (technical), '
  'where price could travel over three months (the simulation), and how three independent expert methods land. Every row is '
  'developed in the sections and appendices below.', size=9.8)
E = D['experts']
_epanel = [E['e1']['base'], E['e2']['base'], E['e3']['base']]
rows = [
 ['Lens / read', 'What it measures', 'Output', 'Against the price'],
 ['FUNDAMENTAL — what the business is worth (the anchor)', '', '', ''],
 ['Split-legs sum-of-the-parts (primary)', 'Auto cash-flow model + lender book + associate marks, less the discount', f"EGP {L['sotp']['base']:.2f}", sgn(L['sotp']['base']/spot-1)],
 ['Pre-discount net asset value', 'The same legs, no complexity discount', f"EGP {sotp['prediscount_ps']:.2f}", sgn(sotp['prediscount_ps']/spot-1)],
 ['Relative multiples', 'FY2026E earnings per share × a justified multiple', f"EGP {L['relative']['base']:.2f}", sgn(L['relative']['base']/spot-1)],
 ['Normalised earnings', 'Mid-cycle profit × a through-cycle multiple', f"EGP {L['normalized']['base']:.2f}", sgn(L['normalized']['base']/spot-1)],
 ['Weighted central', f"Blend {pc(L['weights']['sotp'],0)} / {pc(L['weights']['prediscount'],0)} / {pc(L['weights']['relative'],0)} / {pc(L['weights']['normalized'],0)}", f"EGP {L['central']['base']:.2f}", f"{sgn(GAP)} vs EGP {spot:.2f}"],
 ['TECHNICAL — what the tape is doing (timing, not value)', '', '', ''],
 ['Trend', f"Close EGP {TA_CLOSE:.2f} against the 20/50/100/200-day averages", 'Below the two short, above the two long', 'Trend intact, momentum lost'],
 ['Momentum / range', 'Relative strength · convergence · 52-week range', f"RSI {tech['rsi']:.0f} · histogram {tech['macd']['hist']:+.2f} · {tech['lo52']:.2f}–{tech['hi52']:.2f}", 'Soft, not oversold'],
 ['SIMULATION — where price could go in 3 months (paths from the anchor)', '', '', ''],
 ['1 month', '50,000 paths · sixteen factors', f"p5 {q20['5']:.1f} · p50 {q20['50']:.1f} · p95 {q20['95']:.1f}", 'Median above the anchor'],
 ['3 months', 'same engine, longer horizon', f"p5 {q60['5']:.1f} · p50 {q60['50']:.1f} · p95 {q60['95']:.1f}", 'Wide, right-skewed'],
 ['EXPERT PANEL — three independent methods (Appendix D)', '', '', ''],
 ['Expert 1 — split-legs net asset value', 'Marks each leg; argues the discount', f"EGP {E['e1']['base']:.2f}", 'Most bullish'],
 ['Expert 2 — normalised earnings power', 'Mid-cycle profit × multiple, stake-blind', f"EGP {E['e2']['base']:.2f}", 'Most conservative'],
 ['Expert 3 — cash returns (return on capital vs its cost)', 'Economic profit on capital employed', f"EGP {E['e3']['base']:.2f}", 'In between'],
 ['Panel range', 'The spread is the MNT-Halan mark', f"EGP {min(_epanel):.2f}–{max(_epanel):.2f}", f"Middle read EGP {sorted(_epanel)[1]:.2f}"],
]
table(rows, [2.15, 2.35, 1.45, 1.15], band_rows=[1, 7, 10, 13], first_col_bold=False, size=8.9)
rich([('Bottom line. ', dict(bold=True)),
      (f"Every disagreement in that table traces to one question, and it is not what GB Corp owns. "
       f"The central sits at EGP {L['central']['base']:.2f} against EGP {spot:.2f}, {sgn(GAP)}; the "
       f"three experts span EGP {min(_epanel):.2f} to {max(_epanel):.2f}; and the two reads that never "
       f"touch the associate stake — relative at EGP {L['relative']['base']:.2f} and normalised at "
       f"EGP {L['normalized']['base']:.2f} — sit within "
       f"{max(abs(L['relative']['base']/spot-1), abs(L['normalized']['base']/spot-1))*100:.0f}% of the "
       "traded price. Strip the stake out and this is an operator priced about right. Put it back in at "
       "the round's own valuation and the shares look materially cheap. The three-month distribution is "
       "indifferent either way: it prices the stock's own measured path, and its median sits above the "
       "anchor only because that measured drift survived the calibration test in Appendix B, by a "
       "margin that appendix states rather than flatters.", {})], size=9.8, space_after=8)

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
 ['52-week range (library, %s)' % TA_DATE_L, f"EGP {tech['lo52']:.2f} – {tech['hi52']:.2f}"],
 ['MNT-Halan stake', f"{pc(sotp['mnt_halan_stake'],2)}, stated by the company on 9 June 2026, against {pc(STAKE_PRIOR,2)} before that transaction"],
]
table(rows, [1.9, 5.2], first_col_bold=True)
caption('Source: the company’s own FY2023, FY2024 and FY2025 earnings releases; its 2Q/1H2026 release of 13 August 2026 '
        'and the reviewed consolidated statements to 30 June 2026; the MNT-Halan transaction release of 9 June 2026; and the '
        'exchange price library. Every figure in this table is read from the study’s committed record.')

# ================= §1 Fundamental ===========================================
H1('1  Fundamental valuation')
P('We value GB Corp as an operating company with a captive finance arm and split the legs: blending an auto '
  'assembler-distributor, a leveraged lender and an unlisted fintech associate into one multiple would blur three different '
  'economics. The primary lens is therefore a split-legs sum-of-the-parts — the Auto operating leg on a free-cash-flow '
  'model; GB Capital on its adjusted operating book times a return-justified multiple; the MNT-Halan-led associate stakes at '
  'GB Corp’s own stated ownership applied to the June 2026 funding round. A relative-multiple read and a normalised '
  'mid-cycle read complete the set. The weights and the football field are in §1.5, and §1.5 also states plainly what those '
  'weights are and are not.')

H2('1.1  Split-the-legs sum-of-the-parts — the primary lens')
P(f'Each leg is marked on the basis that fits it. The Auto leg takes the §1.2 cash-flow value. GB Capital is marked on the '
  f'company’s own adjusted-return equity base — the disclosure that strips the MNT-Halan revaluation out of the '
  f'equity denominator — at EGP {n0(sotp["cap_val"])} mn, one times book, the return-justified multiple for a '
  f'mid-teens-return lender whose margin benefits from the easing cycle. The associates are marked by applying GB Corp’s '
  f'own stated stake to the June 2026 funding round: USD {sotp["mnt_halan_round_usd"]/1000:.1f} bn × '
  f'{pc(sotp["mnt_halan_stake"],2)} × EGP/USD {sotp["egp_usd"]:.1f}. Within the associates line MNT-Halan is '
  f'{pc(sotp["mnt_halan_value"]/sotp["assoc"],0)} of the value, with Bedaya and Kaf the EGP {n0(sotp["other_assoc"])} mn '
  f'residual. From the sum we deduct a {pc(sotp["disc"],0)} complexity discount for the wrapper: an auto operator, a '
  'non-bank lender and an unlisted fintech in one listing will not trade at the clean sum of its parts.')
rows = [
 ['Leg (base case)', 'Basis', 'Value (EGP mn)'],
 ['GB Auto operating leg', f"Free-cash-flow model (§1.2): enterprise value {n0(dcf['ev'])} less net debt {n0(dcf['auto_nd'])} less minority {n0(dcf['auto_nci'])}", n0(sotp['auto_eq'])],
 ['GB Capital lending leg', f"Adjusted operating book {n0(sotp['cap_val'])} × 1.0×", n0(sotp['cap_val'])],
 [f"Associate — MNT-Halan ({pc(sotp['mnt_halan_stake'],2)}, stated 9 June 2026)", f"USD {sotp['mnt_halan_round_usd']/1000:.1f} bn June-2026 round × {pc(sotp['mnt_halan_stake'],2)} × {sotp['egp_usd']:.1f} EGP/USD", n0(sotp['mnt_halan_value'])],
 ['Other associates (Bedaya, Kaf)', 'Residual carrying value', n0(sotp['other_assoc'])],
 ['Σ Equity value (pre-discount)', f"= EGP {sotp['prediscount_ps']:.2f} / share", n0(sotp['total'])],
 ['less: complexity / conglomerate discount', pc(sotp['disc'], 0), paren(sotp['total']*sotp['disc'])],
 ['Sum-of-the-parts equity value', f"= EGP {sotp['ps']:.2f} / share", n0(sotp['eq'])],
]
table(rows, [2.5, 3.1, 1.5], first_col_bold=True)
rich([(f"Sum-of-the-parts base EGP {sotp['ps']:.2f} per share", dict(bold=True)),
      (f", with a bear–bull span of EGP {sotp['bear']:.2f}–{sotp['bull']:.2f} — driven mainly by the discount "
       f"applied to the MNT-Halan mark and by the Auto margin and working-capital path (§1.9). The market-implied read "
       f"is a puzzle rather than a sourcing question: market capitalisation less the lender and the associates at the stated "
       f"stake implies a deeply negative value for the Auto leg, which is impossible for a profitable business turning over "
       f"EGP {DRV['auto_revenue_fy2025']/1000:.1f} bn. The honest readings are that the market applies a much steeper "
       f"discount to this private mark than this study’s {pc(sotp['disc'],0)}, that it does not accept the round’s "
       "valuation as transferring to a minority holder, or that GB Corp is mispriced. §7 discusses which is most plausible.", {})])

H2('What the MNT-Halan stake is worth inside this valuation')
P('Because this single line dominates the whole valuation, here is its exact footprint, on the company’s own stated '
  'figure:', size=9.8, space_after=4)
rows = [
 ['MNT-Halan in the GBCO valuation', 'Value'],
 [f"Value at the June-2026 round ({pc(sotp['mnt_halan_stake'],2)} stake)", f"USD {sotp['mnt_halan_round_usd']/1000:.1f} bn × {pc(sotp['mnt_halan_stake'],2)} × {sotp['egp_usd']:.1f} = EGP {n0(sotp['mnt_halan_value'])} mn"],
 ['Per share, pre-discount', f"EGP {sotp['mnt_halan_value']/SH:.2f} — {pc(sotp['mnt_halan_value']/sotp['total'],0)} of the EGP {sotp['prediscount_ps']:.2f} pre-discount net asset value"],
 [f"Per share, after the {pc(sotp['disc'],0)} discount", f"EGP {sotp['mnt_halan_value']*(1-sotp['disc'])/SH:.2f} — the same {pc(sotp['mnt_halan_value']/sotp['total'],0)} share of the EGP {sotp['ps']:.2f} sum-of-the-parts"],
 [f"As a share of the market price (EGP {spot:.2f})", f"{pc(sotp['mnt_halan_value']*(1-sotp['disc'])/D['mktcap'],0)} of market capitalisation — the puzzle, stated"],
 ['Every 5 percentage points of stake', f"EGP {0.05*sotp['mnt_halan_round_usd']*sotp['egp_usd']*(1-sotp['disc'])/SH:.2f} per share of sum-of-the-parts value"],
]
table(rows, [2.7, 4.4], first_col_bold=True, size=9.0)

H2('The market-cap puzzle — what the stated stake actually implies')
P('The stake is a stated number; the residual uncertainty sits in the mark and the discount. The table below prices the '
  'stake question anyway, because it shows the slope a reader is arguing about:', size=9.8)
rows = [['GB stake in MNT-Halan', 'MNT-Halan value (EGP mn)', 'Fair value per share', 'Note']]
stakes_notes = [
 (0.20, 'a placeholder used in an early draft — superseded'),
 (0.25, ''),
 (0.30, ''),
 (0.35, ''),
 (0.40, ''),
 (STAKE_PRIOR, 'the pre-transaction figure, superseded'),
 (sotp['mnt_halan_stake'], 'stated by the company, 9 June 2026 — base case'),
]
for st, note in stakes_notes:
    val = st * sotp['mnt_halan_round_usd'] * sotp['egp_usd']
    ps = (val + sotp['auto_eq'] + sotp['cap_val'] + sotp['other_assoc']) * (1 - sotp['disc']) / SH
    rows.append([pc(st, 2), n0(val), f"{ps:.2f}", note])
table(rows, [1.5, 1.7, 1.3, 2.6], first_col_bold=True, size=8.8)
rich([('In plain terms: ', dict(bold=True)),
      (f"the open question is not what GB Corp owns but what that ownership is worth, and why the market does not price it "
       f"at face value. A {pc(sotp['mnt_halan_stake'],2)} stake in a company marked at USD "
       f"{sotp['mnt_halan_round_usd']/1000:.1f} bn is worth {pc(sotp['mnt_halan_value']*(1-sotp['disc'])/D['mktcap'],0)} of "
       "GB Corp’s entire market capitalisation — either the market applies a private-mark discount this study’s "
       f"{pc(sotp['disc'],0)} does not capture, or GB Corp is mispriced. The bear case in §1.5 reflects the former through a "
       "much heavier discount on the stake; the base case takes the stated number at the round’s valuation. §7 returns "
       "to this as the study’s central open question.", {})], size=9.8)

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
          ('dna', '+ Depreciation & amortisation'), ('capex', '− Capital expenditure'),
          ('dwc', '− Change in working capital'), ('fcff', 'Free cash flow to the firm'),
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
caption('The discount factors are the cost-of-capital schedule’s own cumulative factors, one forward rate per year; '
        'they are not a single rate compounded.')

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
  'is carried on the construction described above and the refusal is recorded rather than papered over. Appendix B states '
  'what that leaves open.', size=9.6)

H2('1.3  Relative multiples')
_r = LI['relative']
P(f"On the model's own forward build — group net profit attributable of EGP {n0(_r['np_fy26e'])} mn in the first "
  f"forecast year, earnings per share of EGP {_r['eps_fy26e']:.2f} — GB Corp trades at "
  f"{spot/_r['eps_fy26e']:.1f}× forward earnings. A justified multiple for the blend — an emerging-market auto "
  f"distributor plus a mid-teens-return non-bank lender, with an unlisted fintech kicker — is taken at "
  f"{_r['pe']['bear']:.1f}–{_r['pe']['bull']:.1f}×. The lens is marked on the forward earnings per share.")
rows = [
 ['Relative basis', 'Bear', 'Base', 'Bull'],
 ['FY2026E net profit (EGP mn)', n0(_r['np_fy26e']), n0(_r['np_fy26e']), n0(_r['np_fy26e'])],
 ['Earnings per share (EGP)', f"{_r['eps_fy26e']:.2f}", f"{_r['eps_fy26e']:.2f}", f"{_r['eps_fy26e']:.2f}"],
 ['Justified multiple', f"{_r['pe']['bear']:.1f}×", f"{_r['pe']['base']:.1f}×", f"{_r['pe']['bull']:.1f}×"],
 ['Fair value (EGP/share)', f"{L['relative']['bear']:.2f}", f"{L['relative']['base']:.2f}", f"{L['relative']['bull']:.2f}"],
]
table(rows, [2.6, 1.3, 1.3, 1.3], first_col_bold=True)
rich([(f"Relative base EGP {L['relative']['base']:.2f}", dict(bold=True)),
      (f' — the most conservative read, {sgn(L["relative"]["base"]/spot-1)} against the price, and probably where a '
       'sceptic anchors: it pays for this year’s earnings and gives nothing for the working-capital release or the '
       'associate stake.', {})])

H2('1.4  Normalised earnings power — where this sits in the cycle')
_n = LI['normalized']
_pcv = DRV['pc_volume_units']
P(f"Cycle position first. The passenger-car volume disclosed for FY2025, {_pcv['FY25']:,} units, is "
  f"{_pcv['FY25']/_pcv['FY23']:.1f} times the FY2023 figure of {_pcv['FY23']:,} — a recovery that is mid-cycle rather "
  f"than late-cycle. Margins are past their peak, and the company's own filed record says so: group gross margin ran "
  f"{pc(HIS['2023']['gross_profit']/HIS['2023']['revenue'],2)} in FY2023 and "
  f"{pc(HIS['2024']['gross_profit']/HIS['2024']['revenue'],2)} in FY2024, both carrying an import-scarcity windfall, "
  f"against {pc(HIS['2025']['gross_profit']/HIS['2025']['revenue'],2)} in FY2025; on the auto leg alone the reviewed half "
  f"to 30 June 2026 ran {pc(D['forecast_anchor']['latest_reviewed_rate'],2)}. Mid-cycle earnings power therefore blends "
  f"recovering volumes with normalised margins at EGP {n0(_n['pat']['base'])} mn of group profit after tax, against the "
  f"EGP {n1(HIS['2025']['net_profit'])} mn reported for FY2025.")
rows = [
 ['Normalised-earnings basis', 'Bear', 'Base', 'Bull'],
 ['Mid-cycle profit after tax (EGP mn)', n0(_n['pat']['bear']), n0(_n['pat']['base']), n0(_n['pat']['bull'])],
 ['Earnings per share (EGP)', f"{_n['eps']['bear']:.2f}", f"{_n['eps']['base']:.2f}", f"{_n['eps']['bull']:.2f}"],
 ['Justified multiple', f"{_n['pe']['bear']:.1f}×", f"{_n['pe']['base']:.1f}×", f"{_n['pe']['bull']:.1f}×"],
 ['Fair value (EGP/share)', f"{L['normalized']['bear']:.2f}", f"{L['normalized']['base']:.2f}", f"{L['normalized']['bull']:.2f}"],
]
table(rows, [2.6, 1.3, 1.3, 1.3], first_col_bold=True)
rich([(f"Normalised base EGP {L['normalized']['base']:.2f}", dict(bold=True)),
      (f' — {sgn(L["normalized"]["base"]/spot-1)} against the price: in effect the bet that the volume recovery '
       'completes while margins hold the post-windfall floor. Like the relative read, it never touches the associate stake.', {})])

H2('1.5  Synthesis — the four reads, and what the weights are not')
P('The sum-of-the-parts carries the heaviest weight because it respects the differing economics of the legs; the '
  'pre-discount net asset value carries the discount-narrowing case; the relative read anchors the floor; normalised '
  'earnings carries the recovery. That is the construction this edition publishes, and the honest thing to say about it is '
  'that the weights were chosen and written down and have never been tested out of sample against any alternative. Two of '
  'the four reads value this group off reported and mid-cycle earnings and do not touch the associate stake at all, so '
  f"{pc(L['weights']['relative']+L['weights']['normalized'],0)} of the weight sits in reads that are structurally blind to "
  'the largest asset on the page. A reader who wants the number that is not a blend should take the primary read, '
  f"EGP {L['sotp']['base']:.2f}, and treat the rest of the table as cross-checks; the difference is "
  f"{pc(L['sotp']['base']/L['central']['base']-1,1)} of the central and it is recorded rather than argued away.")
rows = [['Lens', 'Weight', 'Bear', 'Base', 'Bull'],
 ['Split-legs sum-of-the-parts', pc(L['weights']['sotp'], 0), f"{L['sotp']['bear']:.2f}", f"{L['sotp']['base']:.2f}", f"{L['sotp']['bull']:.2f}"],
 ['Pre-discount net asset value', pc(L['weights']['prediscount'], 0), f"{L['prediscount']['bear']:.2f}", f"{L['prediscount']['base']:.2f}", f"{L['prediscount']['bull']:.2f}"],
 ['Relative multiples', pc(L['weights']['relative'], 0), f"{L['relative']['bear']:.2f}", f"{L['relative']['base']:.2f}", f"{L['relative']['bull']:.2f}"],
 ['Normalised earnings', pc(L['weights']['normalized'], 0), f"{L['normalized']['bear']:.2f}", f"{L['normalized']['base']:.2f}", f"{L['normalized']['bull']:.2f}"],
 ['Weighted central', '', f"{L['central']['bear']:.2f}", f"{L['central']['base']:.2f}", f"{L['central']['bull']:.2f}"],
]
table(rows, [2.4, 0.9, 1.1, 1.1, 1.1], first_col_bold=True, band_rows=[5])
figure('fig1_football.png', 6.3, 'Figure 1 — Valuation football field. Bars span bear to bull per lens; the brass tick is each '
       'base case; the gold band is the blended central range; the ink line is the price.')
rich([(f"Central fair value EGP {L['central']['base']:.2f} per share", dict(bold=True)),
      (f", {sgn(GAP)} against the price. The width here is not four independent views converging. The sum-of-the-parts and "
       f"pre-discount reads (EGP {L['sotp']['base']:.2f} and {sotp['prediscount_ps']:.2f}) both carry the same MNT-Halan "
       f"mark and move together with it, while the relative and normalised reads (EGP {L['relative']['base']:.2f} and "
       f"{L['normalized']['base']:.2f}) do not touch it and sit close to the price. That split is itself the finding: strip "
       "the associate stake out and this is a fairly-priced operator; put it back in at the round’s valuation and it "
       "looks materially cheap.", {})])

H2('1.6  The legs, and the units × price driver table')
rows = [
 ['Leg', 'Cyclicality', 'Margin / return trend', 'Capital intensity', 'Swing role'],
 ['GB Auto — passenger cars', 'High (rates, currency, imports)', f"Auto gross margin {pc(D['forecast_anchor']['latest_reviewed_rate'],2)} in the reviewed half; the forecast opens at {pc(_cs['gross_margin'][0],2)}", 'Very high (working capital)', 'Dominant'],
 ['GB Auto — commercial vehicles, trading, mobility', 'Moderate', 'Bus exports scaling', 'Moderate', 'Diversifier'],
 ['GB Capital', 'Credit cycle', 'Adjusted return on equity in the mid teens', 'Leveraged by construction', 'Compounder'],
 ['Associates (MNT-Halan and others)', 'Venture-like', 'Private marks; no public price', 'Off balance sheet', 'The swing factor'],
]
table(rows, [1.9, 1.2, 1.9, 1.35, 0.85], first_col_bold=True, size=8.7)
P('The bottom-up build. Every historical figure below is the company’s own disclosure; the forecast columns are the '
  'model’s own driver path:', size=9.8)
fc = D['forecast']
_pcr = DRV['pc_revenue']; _pca = DRV['pc_asp']
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

H2('1.7  The crux: the mark and its discount, then cash conversion and the rate path')
P(f'Three judgments drive this valuation, in order of size. First and by a wide margin: not what GB Corp’s MNT-Halan '
  f'stake is — the company stated it — but what a private mark that large should be discounted by, given that '
  f'taking it at face value makes the stake worth {pc(sotp["mnt_halan_value"]*(1-sotp["disc"])/D["mktcap"],0)} of the '
  f'entire market capitalisation. This study applies a {pc(sotp["disc"],0)} complexity discount uniformly across all three '
  'legs; a reader who believes the market applies a much steeper illiquidity and minority discount specifically to that '
  'mark should treat the bear case, not the base case, as the more realistic anchor. Second, where Auto working-capital '
  f'intensity settles: it is modelled from {pc(_cs["working_capital_pct"][0],1)} of revenue down to '
  f'{pc(_cs["working_capital_pct"][-1],1)}, and each point of steady-state intensity moves the operating leg materially '
  f'— §1.9 prices the whole grid rather than a single point estimate of that effect. Third, the Egyptian nominal-rate '
  f'path: the schedule glides from {pc(COC["wacc_exp"],2)} to {pc(COC["wacc_terminal"],2)} against terminal growth of '
  f'{pc(MAC["terminal_growth_nominal"],2)}, a terminal real spread of '
  f'{pc(COC["wacc_terminal"]-MAC["terminal_growth_nominal"],2)}, and every 100 basis points the easing cycle takes out of '
  'that spread is worth what the §1.9 grid shows. A fourth exposure is regional: part of passenger-car revenue is Iraq and '
  'Jordan, where conflict has already cut volumes, and this study does not hold a sourced split of that revenue for the '
  'reviewed half, so it is named as an exposure and not priced.')

H2('1.8  Macro and country — rates, the pound, and the cost of capital')
P(f'GB Corp is a leveraged play on Egyptian nominal normalisation. Every cut lowers GB Capital’s funding cost on a '
  f'fixed-rate lending book, lowers the customer’s instalment, and compresses the discount rate this study applies. '
  f'The pound sets assembly input costs and the pound value of the MNT-Halan mark; a step devaluation is the single '
  f'nastiest macro scenario for both margin and multiple. The cost-of-capital build below is produced by the house module '
  f'rather than assembled by hand, and the whole schedule is published — not one rate held for ever:', size=10.5)
rows = [
 ['Cost-of-capital build', 'Value', 'Source'],
 ['Observed risk-free rate', pc(COC['rf_observed'], 2), 'Egypt 10-year local-currency government bond yield, house macro path'],
 ['less: Egypt’s own sovereign default spread', pc(COC['default_spread'], 2), 'so country risk is counted exactly once, inside the premium below'],
 ['Normalised risk-free rate', pc(COC['rf_star'], 2), 'the difference of the two rows above'],
 ['Equity beta', f"{COC['beta']:.4f}", 'own-stock weekly regression against the published EGX30 index'],
 ['Equity risk premium (market basis, adopted)', pc(COC['erp'], 2), 'the sovereign’s own row, read for this country'],
 ['Equity risk premium (rating basis, alternative)', pc(D['cost_of_capital_rating_basis']['erp'], 2), 'same source, rating-based column; published beside the adopted basis'],
 ['Cost of equity, explicit window', pc(COC['ke_exp'], 2), f"reproduces from the normalised rate plus beta times the premium; {pc(D['cost_of_capital_rating_basis']['ke_exp'],2)} on the rating basis"],
 ['Pre-tax cost of debt', pc(COC['kd_pretax'], 2), 'the company’s own effective borrowing rate, computed on the borrowings that actually bear the interest'],
 [f"After-tax cost of debt", pc(COC['kd_aftertax'], 2), 'debt is entirely local-currency on the disclosed facility note'],
 ['Weights (equity / debt)', f"{pc(COC['weight_equity'],1)} / {pc(COC['weight_debt'],1)}", 'market capitalisation against disclosed borrowings'],
 ['Weighted cost of capital, first forecast year', pc(COC['wacc_exp'], 2), f"{pc(D['cost_of_capital_rating_basis']['wacc_exp'],2)} on the rating-based alternative"],
 ['Weighted cost of capital, terminal', pc(COC['wacc_terminal'], 2), 'norm-built, reached by a glide inherited from the policy-rate path'],
 ['Terminal growth (real, then nominal)', f"{pc(MAC['terminal_growth_real'],1)} → {pc(MAC['terminal_growth_nominal'],2)}", 'stored as a real rate on the house inflation path and recomputed; never typed as a nominal figure'],
]
table(rows, [2.6, 1.3, 3.0], first_col_bold=True, size=8.7)
P('Three honesty notes on this build. First, the beta is the stock’s own regression against the published index of '
  f'the exchange it is listed on — {COC["beta"]:.4f}, on weekly observations over nearly five years, passing the '
  'usability gate — and it replaces an assumed unit beta the superseded edition carried because an earlier attempt on '
  'five annual observations was unusable. Second, the country risk enters exactly once: the observed local yield is reduced '
  'by this sovereign’s own default spread and the premium added back carries the country risk, rather than the raw '
  'yield being combined with a country-loaded premium. Third, both premium bases are published and the market basis is '
  'named as the adopted one; the rating basis is shown beside it rather than averaged into it.', size=9.6)
# THE RECORD KEEPS ITS PROVENANCE; THE DELIVERED DOCUMENT DOES NOT PRINT IT. This note is
# written for an internal reader and names the standing rule it borrows its shape from; a
# rule identifier leaks by SHAPE and does not belong in a document written for somebody
# outside this house, so the shared stripper renders it rather than a local copy.
import sys as _sys
_sys.path.insert(0, __import__('os').path.join(
    __import__('os').path.dirname(__import__('os').path.abspath(__file__)), '..'))
from outward_source import outward as _outward                       # noqa: E402
_stale = MAC.get('anchor_staleness_accepted')
if _stale:
    P('Disclosed staleness of the macro anchors: ' + _outward(_stale), size=9.2,
      italic=True, color=GREY)

H2('1.9  Sensitivity — the margin, the discount, and the rate spread')
P('Holding the lender and associate marks fixed, the first grid re-prices the sum-of-the-parts across the Auto '
  'gross-margin path and the complexity discount; the second across the cost of capital and terminal growth. The stake is '
  'not the open question in either — what matters is the discount applied to its mark, priced in the §1.1 table, '
  'which dominates both of these grids combined.')
_near = any(abs(v - spot) < 1.6 for rowv in D['sens']['table'] for v in rowv)
figure('fig2_sens.png', 5.6,
       ('Figure 2 — Sum-of-the-parts fair value (EGP/share) across the Auto gross-margin shift and the complexity discount. '
        + (f'Bold cells sit nearest the EGP {spot:.2f} price.' if _near
           else f'No cell in the grid reaches the EGP {spot:.2f} price; the nearest is EGP '
                f'{min((v for rowv in D["sens"]["table"] for v in rowv), key=lambda v: abs(v-spot)):.1f}.')))
import numpy as np
fcffs = [r['fcff'] for r in dcf['rows']]
base_wacc = dcf['wacc']
_TG = MAC['terminal_growth_nominal']
_gs = [_TG - 0.02, _TG - 0.01, _TG, _TG + 0.01, _TG + 0.02]
wg_rows = [['Cost of capital \\ terminal growth'] + [pc(g, 1) for g in _gs]]
wacc_steps = [base_wacc - 0.02, base_wacc - 0.01, base_wacc, base_wacc + 0.01, base_wacc + 0.02]
_fwd0 = dcf['forward_wacc']
_wt0 = dcf['wacc_terminal']
for w in wacc_steps:
    row = [pc(w, 1)]
    _shift = w - base_wacc
    _fac, _c = [], 1.0
    for r in _fwd0:
        _c /= (1 + r + _shift)
        _fac.append(_c)
    for g in _gs:
        if (_wt0 + _shift) - g < 0.045:
            row.append('n.m.')
            continue
        pv = sum(f * _fac[i] for i, f in enumerate(fcffs))
        tv = fcffs[-1] * (1 + g) / ((_wt0 + _shift) - g) * _fac[-1]
        ps = ((pv + tv - dcf['auto_nd'] - dcf['auto_nci'] + sotp['cap_val'] + sotp['assoc'])
              * (1 - sotp['disc'])) / SH
        row.append(f'{ps:.1f}')
    wg_rows.append(row)
table(wg_rows, [1.9, 0.95, 0.95, 0.95, 0.95, 0.95], first_col_bold=True, size=9.0)
caption(f"Sum-of-the-parts fair value (EGP/share, after the complexity discount) across the cost of capital and terminal "
        f"growth. The centre cell, {pc(base_wacc,1)} against {pc(_TG,1)}, is EGP {sotp['ps']:.1f}. Both axes are centred on "
        f"the model's own build rather than on round numbers: the rate axis shifts the WHOLE schedule, explicit years and "
        f"terminal together, because moving one rate and not the others would price one date at two prices. This grid holds "
        f"the MNT-Halan mark fixed and is not the dominant sensitivity in this study.")

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
P('For the probabilistic work this matters in one way, and it is the opposite of what the superseded edition said. A tape '
  'that has come off its short averages with negative momentum thins the near-term upside tail rather than thickening it. '
  'The technical and fundamental pictures still disagree — the fundamental work says value has been reached and the '
  'tape says the market is not yet interested — and §6 reads the resulting probability zones without forcing a '
  'reconciliation between them.')
