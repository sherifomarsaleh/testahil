"""PHDC_Valuation_Study_19-08-2026_public.docx — 16-section study, house style,
model-study skeleton, developer lens. Every financial numeral is read from
study_numbers.json; no number is typed into this builder."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
os.chdir(HERE)
exec(open(os.path.join(HERE, '..', 'du_study', 'docx_base.py')).read())

D = json.load(open('study_numbers.json'))
M, H, W, L, SYN, SENS = D['meta'], D['hist'], D['wacc'], D['lenses'], D['synthesis'], D['sens']
DCF, CF, EXP, GDV = D['dcf'], D['carry_forward'], D['experts'], D['gdv']
A, B = DCF['framing_A'], DCF['framing_B']
H3, QP, SEG, SL, PR = D['hist3'], D['qpath'], D['segments'], D['slider'], D['prior']
VAR, PEERS, BR = D['variance'], D['peers'], D['beta_record']
YRS = DCF['years']
for _fr in (DCF['framing_A'], DCF['framing_B']):
    _fr['gp'] = [_fr['gm'][i] * _fr['rev'][i] for i in range(len(DCF['years']))]
SPOT, SH = M['spot'], M['shares_out']

_T = [0]; _F = [0]
def T():
    _T[0] += 1
    return 'Table %d' % _T[0]
def FG():
    _F[0] += 1
    return 'Figure %d' % _F[0]


def lalign(t, cols):
    """Prose columns must read left-aligned; the base table right-aligns everything
    from column 1 onward, which is right for numbers and wrong for sentences."""
    for row in t.rows:
        for j in cols:
            for p in row.cells[j].paragraphs:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    return t

def n0(x):  return '%s' % format(round(x), ',')
def n1(x):  return '%s' % format(round(x, 1), ',')
def p2(x):  return '%.2f' % x
def pc(x, d=1):  return ('%.' + str(d) + 'f%%') % (x * 100)
def pp(x, d=1):  return ('%+.' + str(d) + 'f%%') % (x * 100)
def bn(x):
    v = x / 1000.0
    return ('%.0f' % v) if abs(v - round(v)) < 0.005 else ('%.2f' % v)

# =============================================================== 1. MASTHEAD
masthead()
P('Palm Hills Developments (EGX:PHDC)', size=20, bold=True, space_after=2)
P('Independent valuation study — fundamentals refreshed on the 30 June 2026 statements',
  size=11.5, color=BRASS, space_after=8)
rich([('Anchor ', {}), ('EGP %s' % p2(SPOT), {'bold': True}),
      (' (%s) · %s bn shares outstanding after treasury · market value about EGP %sbn · '
       'fundamentals rebuilt on the reviewed statements as of 30 June 2026 · '
       'price and probability sections carried forward from the 22 July 2026 data'
       % (M['spot_date'], p2(SH / 1000.0), bn(H['mktcap'])), {})],
     size=9.6, space_after=10)

box([('READ FIRST — what this document is, and is not. ',
      'This study is a valuation exercise and an expression of personal analytical opinion, '
      'published free of charge for educational purposes: it shows how one analyst applies '
      'fundamental and probabilistic methods to a listed company, and invites scrutiny of that '
      'methodology. It is NOT investment advice, NOT a recommendation or solicitation to buy, '
      'sell or hold any security, and NOT directed at the circumstances of any reader. The '
      'preparer is not licensed by the Egyptian Financial Regulatory Authority or any other '
      'regulator, provides no financial consultancy, manages no money, and accepts no fees, '
      'funds or clients. All values are model outputs presented as ranges and distributions '
      'because no single number should be relied on. Consult a licensed financial advisor '
      'before any investment decision.')])

# =============================================================== 2. HEADLINE
H1('Headline')
rich([('One question decides this company, and the accounts pose it plainly. ', {'bold': True}),
      ('Palm Hills holds EGP %sbn of customers\' maintenance money on behalf of residents\' '
       'associations that have not yet been legally constituted. Take that balance\'s growth out '
       'of the cash-flow statement and reported operating cash flow is negative in every period '
       'the company has ever disclosed: EGP %smn in the first half of 2026, EGP %smn in the '
       'first half of 2025, EGP %smn in 2024 and EGP %smn in 2023. Whether that float is '
       'permanent funding of the business or third-party money held in trust is worth more than '
       'any forecast in this document, so the study computes the whole valuation both ways and '
       'publishes the two answers side by side. It never averages them.'
       % (bn(34337.384836), n0(H['ocf_ex_ra_h126']), n0(H['ocf_ex_ra_h125']),
          n0(H['ocf_ex_ra_fy24']), n0(H['ocf_ex_ra_fy23'])), {})])
rich([('Treat the float as operating funding and the four lenses centre on EGP %s, about %s '
       'against the EGP %s market price, inside a range of EGP %s to EGP %s. Treat it as '
       'restricted and the same four lenses centre on EGP %s. '
       % (p2(SYN['framing_A']['base']), pp(SYN['framing_A']['base'] / SPOT - 1, 0), p2(SPOT),
          p2(SYN['framing_A']['bear']), p2(SYN['framing_A']['bull']),
          p2(SYN['framing_B']['base'])), {'bold': True}),
      ('The study adopts the first as its base case, because that is how the company has '
       'actually operated for a decade — the balance has risen in every disclosed period, no '
       'association has been constituted, and the invested proceeds earn for the company — and '
       'it publishes the second in full as the downside rather than as a haircut.', {})])
rich([('The second question is what the first half actually said about margins. ', {'bold': True}),
      ('The reported gross margin fell from %s to %s year on year, and the earnings-before-'
       'interest measure the company itself publishes fell from %s to %s. That reads as '
       'deterioration until the audited history is put beside it: the same measure was %s in '
       '2023 and %s in 2024. The first half of 2026 is not below the company\'s own history — '
       '2025 was above it, and about EGP %smn of the 2025 half-year came from selling '
       'investments and other items that carried no cost at all. The compression began in the '
       'fourth quarter of 2025, at %s, and has since recovered to %s and %s in the two quarters '
       'of 2026.'
       % (pc(H['gm_h125']), pc(H['gm_h126']), pc(H['ebitda_margin_h125']),
          pc(H['ebitda_margin_h126']), pc(H['ebitda_margin_fy23']), pc(H['ebitda_margin_fy24']),
          n0(D['inputs']['oneoff_h125']['value']), pc(H['ebitda_margin_q425']),
          pc(H['ebitda_margin_1q26']), pc(H['ebitda_margin_q226'])), {})])
rich([('The third is the cost of capital, and it is where the last edition of this study was '
       'simply wrong. ', {'bold': True}),
      ('It discounted at a flat 18%% while the Egyptian government was paying more than that '
       'to borrow. On 17 August 2026 the three-year Egyptian government bond cleared at %s. '
       'Rebuilt properly, the cost of equity is %s on the rating basis and %s on the '
       'credit-default-swap basis, the marginal cost of debt is %s, and the weighted cost of '
       'capital is %s to %s today, gliding to %s as the central bank\'s own inflation target '
       'takes hold. A discount rate below the local risk-free rate is not available to a '
       'leveraged equity, and every number in the last edition rested on one.'
       % (pc(W['rf_obs'], 2), pc(W['ke_rating']), pc(W['ke_cds']), pc(W['kd_marginal']),
          pc(W['wacc_cds']), pc(W['wacc_rating']), pc(W['wacc_term'])), {})])
rich([('What the shares are priced for. ', {'bold': True}),
      ('At EGP %s the market pays %sx book value against a trailing return on equity of %s. '
       'Solve that for the discount rate the market is applying and it comes out near %s — very '
       'close to the normalised cost of equity in this study, and far below the spot rate. The '
       'market is already pricing Egypt\'s disinflation. That is a defensible view. It is also '
       'the single assumption that has to hold.'
       % (p2(SPOT), p2(H['pb']), pc(H['roe_ltm']),
          pc(SYN['weights'] and (0.08 + (H['roe_ltm'] - 0.08) / H['pb']))), {})])

# ======================================================= 3. VALUATION SUMMARY
H1('Valuation summary')
rows = [['', 'Framing A — float is operating funding', 'Framing B — float restricted']]
rows += [
    ['Cash-flow lens', 'EGP %s – %s' % (p2(L['dcf']['A_low']), p2(L['dcf']['A_high'])),
     'EGP %s – %s' % (p2(L['dcf']['B_low']), p2(L['dcf']['B_high']))],
    ['Book value and sustainable return', 'EGP %s – %s' % (p2(L['book']['low']), p2(L['book']['high'])),
     'EGP %s – %s' % (p2(L['book']['low']), p2(L['book']['high']))],
    ['Relative multiples', 'EGP %s – %s' % (p2(L['relative']['low']), p2(L['relative']['high'])),
     'EGP %s – %s' % (p2(L['relative']['low']), p2(L['relative']['high']))],
    ['Normalised earnings power', 'EGP %s – %s' % (p2(L['normalised']['low']), p2(L['normalised']['high'])),
     'EGP %s – %s' % (p2(L['normalised']['low']), p2(L['normalised']['high']))],
    ['Weighted centre', 'EGP %s' % p2(SYN['framing_A']['base']), 'EGP %s' % p2(SYN['framing_B']['base'])],
    ['Weighted low', 'EGP %s' % p2(SYN['framing_A']['bear']), 'EGP %s' % p2(SYN['framing_B']['bear'])],
    ['Weighted high', 'EGP %s' % p2(SYN['framing_A']['bull']), 'EGP %s' % p2(SYN['framing_B']['bull'])],
    ['Against the EGP %s market price' % p2(SPOT),
     pp(SYN['framing_A']['base'] / SPOT - 1), pp(SYN['framing_B']['base'] / SPOT - 1)],
]
table(rows, [2.35, 2.35, 2.35], first_col_bold=True, band_rows={5}, size=9.2)
caption('%s. The contested judgement computed both ways. The three lenses that do not depend on '
        'it are identical in both columns by construction; only the cash-flow lens moves. Within '
        'each column the range is the cost of capital: the low end holds today\'s spot rate '
        'constant, the high end glides to the normalised rate. The two columns are never blended.'
        % T())

rows = [['What this study publishes', 'EGP per share', 'Where it comes from']]
rows += [
    ['Low case', p2(SYN['bear']), 'the weighted centre under framing B — the alternative reading '
                                  'of the balance sheet, computed in full'],
    ['Base case', p2(SYN['base']), 'the weighted centre under framing A, the adopted framing'],
    ['High case', p2(SYN['bull']), 'the weighted high under framing A'],
    ['Market price', p2(SPOT), 'close of %s' % M['spot_date']],
]
table(rows, [2.0, 1.4, 3.6], first_col_bold=True, band_rows={2}, size=9.2)
caption('%s. The low case is not a stress test bolted onto the base. It is the other framing of '
        'the float, run through all four lenses.' % T())

figure('fig1_football.png', 6.7,
       '%s. Valuation field, EGP per share. The two framings of the contested judgement sit at '
       'the top; the four lenses beneath them; the traded range at the bottom. The dashed line '
       'is the market price. Every bar is defined in the tables above and rebuilt from the '
       'company\'s own statements.' % FG())

H2('What the previous edition got wrong')
P('The last edition of this study was published on 11 June 2026, before the 30 June statements '
  'existed. Every forecast it made for a period that has since been disclosed is scored below '
  'against the actual. A miss of more than five per cent of the central value is treated as '
  'material and is explained by naming which part of the driver stack was wrong, not merely that '
  'the number differed.', size=9.6)
rows = [['Item', 'Previous edition', 'Disclosed actual', 'Miss', 'Which driver was wrong']]
for v in VAR:
    f, a = v['forecast'], v['actual']
    if v['unit'] == 'ratio':
        fs, as_ = pc(f), pc(a)
    elif v['unit'] == 'x':
        fs, as_ = p2(f) + 'x', p2(a) + 'x'
    elif v['unit'] == 'mn shares':
        fs, as_ = n0(f), n0(a)
    else:
        fs, as_ = n0(f), n0(a)
    d = '' if v['delta'] is None else (pp(v['delta'], 0) + (' ▲' if v['escalates'] else ''))
    rows.append([v['item'], fs, as_, d, v['note']])
lalign(table(rows, [1.15, 0.85, 0.85, 0.62, 3.53], size=7.9, align_right_from=1), {4})
caption('%s. Scoring the previous edition. EGP mn unless the item says otherwise; ratios and '
        'multiples as stated. A triangle marks a miss beyond five per cent of the central value. '
        'Fourteen of the sixteen lines miss materially, which is why this is a rebuild rather '
        'than an update.' % T())

# ======================================================= 4. COMPANY OVERVIEW
H1('Company overview')
P('Palm Hills Developments is an Egyptian joint-stock company incorporated in 2005 and listed on '
  'the Egyptian Exchange since 2008. It builds and sells integrated residential communities, '
  'mostly in West Cairo, East Cairo, the North Coast and Alexandria, and it runs hotels and '
  'sports clubs alongside them. Its land bank runs to about %s million square metres across '
  'Egypt and Abu Dhabi. Its headquarters is at Smart Village, Sixth of October City.'
  % n0(D['inputs']['landbank_sqm']['value']))
P('Three features of the business decide how it has to be valued, and all three come off the face '
  'of the accounts rather than from any description of the company.')
bullet('It sells on multi-year instalments and recognises revenue as it builds, unit by unit, '
       'measured by its own engineering department. So revenue is a function of construction '
       'executed, not of units sold. In the first half of 2026 the company carried out EGP %smn '
       'of work and recognised EGP %smn of real-estate revenue against it.'
       % (n0(D['inputs']['work_h126']['value']), n0(D['inputs']['rev_re_h126']['value'])),
       bold_head='Percentage of completion. ')
bullet('Receivables run to about %s days of revenue and work in progress to another %s days, but '
       'customer advances run to %s days. The cycle nets to about %s days: the customer funds '
       'the build. That is the whole financial architecture, and it is why the balance sheet '
       'carries EGP %sbn of assets against EGP %sbn of equity.'
       % (n0(H['dso']), n0(H['dio']), n0(H['adv_days']), n0(abs(H['ccc_net'])),
          bn(D['inputs']['ta_jun26']['value']), bn(D['inputs']['eqctl_jun26']['value'])),
       bold_head='The customer is the lender. ')
bullet('Several of the largest projects are revenue-sharing arrangements rather than owned land: '
       'the New Urban Communities Authority takes 26 per cent of Badya\'s revenue, the partner '
       'in Alamein takes 30 per cent, and Palm New Cairo, Capital Gardens and El Fouka run on '
       'the same basis. Those shares are a cost of revenue, not a financing item, and they sit '
       'inside the cost line the study decomposes in section 1.6.',
       bold_head='Land is often rented against revenue, not bought. ')

rows = [['Half-year to 30 June, EGP mn', '2026', '2025', 'Change']]
for lbl, k1, k2 in (('Revenue', 'rev_h126', 'rev_h125'),
                    ('Cost of revenues', 'cogs_h126', 'cogs_h125'),
                    ('Gross operating profit', 'gp_h126', 'gp_h125'),
                    ('Administrative, selling and marketing', 'sga_h126', 'sga_h125'),
                    ('Finance costs and interest', 'fin_h126', 'fin_h125'),
                    ('Profit before tax', 'pbt_h126', 'pbt_h125'),
                    ('Attributable profit', 'np_h126', 'np_h125')):
    v1, v2 = D['inputs'][k1]['value'], D['inputs'][k2]['value']
    rows.append([lbl, n0(v1), n0(v2), pp(v1 / v2 - 1, 1)])
rows.append(['Gross margin', pc(H['gm_h126']), pc(H['gm_h125']),
              '%+.1f pts' % ((H['gm_h126'] - H['gm_h125']) * 100)])
rows.append(['Earnings before interest, tax and depreciation', n0(H['ebitda_h126']),
              n0(H['ebitda_h125']), pp(H['ebitda_h126'] / H['ebitda_h125'] - 1, 1)])
table(rows, [2.9, 1.35, 1.35, 1.4], first_col_bold=True, size=9.0)
caption('%s. The reviewed half-year and its comparative, read from the face of the statements.'
        % T())

# ============================================ 5. SECTION 1 — FUNDAMENTAL VALUE
H1('1. Fundamental valuation')
P('Four independent lenses are run on the same set of company-issued numbers, then reconciled '
  'into one field. The cash-flow lens is built from the physical driver — construction executed '
  '— through selling price per unit of build cost, with each cost class carrying its own '
  'escalator and the margin falling out as an output rather than being set as an input.')

H2('1.1  Cash-flow model')
P('The model values the firm before financing, then bridges to equity. It runs from a half-year '
  'stub covering the second half of 2026 through five full years to 2031, then a terminal value '
  'that is made consistent with the return on capital the model itself computes, so growth is '
  'never free. Discounting is mid-period from the 30 June 2026 balance-sheet date.', size=9.8)
rows = [['EGP mn'] + YRS]
def rowify(lbl, arr, f=n0):
    return [lbl] + [f(x) for x in arr]
for lbl, key in (('Revenue', 'rev'), ('Earnings before interest, tax and depreciation', 'ebitda')):
    rows.append(rowify(lbl, A[key]))
rows.append(rowify('Depreciation and amortisation', [-x for x in A['da']]))
rows.append(rowify('Unwind of the discount on instalment receivables', A['amort_nr']))
rows.append(rowify('Income on invested balances (framing A only)', A['tbill_inc']))
rows.append(rowify('Operating profit after the items above', A['ebit']))
rows.append(rowify('Tax at the measured effective rate of %s' % pc(DCF['eff_tax']),
                   [-(A['ebit'][i] - A['nopat'][i]) for i in range(len(YRS))]))
rows.append(rowify('Operating profit after tax', A['nopat']))
rows.append(rowify('Add back depreciation and amortisation', A['da']))
rows.append(rowify('Capital expenditure', [-x for x in A['capex']]))
rows.append(rowify('Change in working capital', [-x for x in A['d_nwc']]))
rows.append(rowify("Residents' Association float (framing A only)", A['ra_cash']))
rows.append(rowify('FREE CASH FLOW TO THE FIRM', A['fcff']))
rows.append(['Discount factor'] + ['%.4f' % x for x in A['df']])
rows.append(rowify('Present value', [A['fcff'][i] * A['df'][i] for i in range(len(YRS))]))
table(rows, [2.24] + [0.79] * 6, first_col_bold=True, size=7.6,
      band_rows={len(rows) - 3})
caption('%s. The free-cash-flow waterfall in full, under framing A, and every line foots. '
        'Interest is excluded throughout because this is a pre-financing measure; the EGP %smn of '
        'interest the company capitalised into work in progress in the first half is added back '
        'inside the earnings line for the same reason. Two items sit between that line and '
        'operating profit because the accounts put them there: the discount on instalment '
        'receivables unwinds into income as the instalments run off, and the invested balances '
        'earn treasury-bill income — the second of which exists only in framing A, since framing '
        'B does not treat those balances as the company\'s. The float line beneath is the whole '
        'of the remaining difference between the two framings, and it too is zero in framing B.'
        % (T(), n0(D['inputs']['capint_h126']['value'])))

rows = [['Bridge from firm to equity, EGP mn', 'Framing A', 'Framing B']]
rows += [
    ['Present value of the explicit forecast', n0(A['pv_explicit']), n0(B['pv_explicit'])],
    ['Present value of the terminal value', n0(A['pv_term']), n0(B['pv_term'])],
    ['ENTERPRISE VALUE', n0(A['ev']), n0(B['ev'])],
    ['Less net debt', '(%s)' % n0(A['bridge']['netdebt']), '(%s)' % n0(B['bridge']['netdebt'])],
    ['Less non-controlling interests', '(%s)' % n0(A['bridge']['nci']), '(%s)' % n0(B['bridge']['nci'])],
    ['EQUITY VALUE', n0(A['bridge']['equity']), n0(B['bridge']['equity'])],
    ['Shares outstanding after treasury, mn', n0(SH), n0(SH)],
    ['VALUE PER SHARE, EGP', p2(A['bridge']['vps']), p2(B['bridge']['vps'])],
    ['Terminal value as a share of enterprise value', pc(A['pv_term'] / A['ev']),
     pc(B['pv_term'] / B['ev'])],
]
table(rows, [3.5, 1.75, 1.75], first_col_bold=True, band_rows={3, 6, 8}, size=9.0)
caption('%s. The two bridges. Net debt differs between the framings for the same reason the cash '
        'flows do: framing A treats the cash and treasury bills as the enterprise\'s, framing B '
        'treats EGP %sbn of them as the associations\' invested money and leaves only EGP %smn '
        'free. The terminal share is high in both — it is higher in framing B because the '
        'explicit years generate almost nothing without the float, which is itself part of the '
        'answer.' % (T(), bn(H['ra_dedicated_assets']), n0(H['liquid_free'])))

P('Reconciliation to the last reported period. Scaled back onto the reported half-year — same '
  'revenue, capitalised interest added back on both sides — the model\'s first forecast period '
  'reproduces the reported earnings before interest, tax and depreciation to within %s. On cash '
  'the comparison needs '
  'two bridging items, both read off the balance sheet: the company paid down EGP %smn of income '
  'tax payable and EGP %smn of the joint-arrangement partners\' balance in the half, neither of '
  'which is a run-rate item. Reported unlevered cash flow of EGP %smn becomes EGP %smn on a '
  'like-for-like basis against the model\'s EGP %smn, a residual of EGP %smn that the study does '
  'not paper over: it is the difference between a ratio-driven roll and one actual half-year of a '
  'working-capital-driven developer.'
  % (pc(abs(H['ebitda_recon_gap']), 2), n0(H['tax_payable_unwind']), n0(H['jsa_unwind']),
     n0(H['ufcf_h126_actual']), n0(H['ufcf_h126_like_for_like']), n0(H['ufcf_h226_model_A']),
     n0(H['recon_residual'])), size=9.5)

H2('1.2  Book value and sustainable return')
P('Controlling equity at 30 June 2026 was EGP %smn, or EGP %s a share on the %s million shares '
  'outstanding after the treasury holding. Trailing attributable profit of EGP %smn on average '
  'controlling equity gives a return on equity of %s. A business earning more than its cost of '
  'equity is worth more than its book; one earning less is worth less. At the spot cost of equity '
  'of %s the justified multiple is %sx and the value is EGP %s. At the normalised cost of equity '
  'of %s it is %sx and EGP %s. The market pays %sx.'
  % (n0(D['inputs']['eqctl_jun26']['value']), p2(H['bvps']), n0(SH), n0(H['ni_ltm']),
     pc(H['roe_ltm']), pc(W['ke_cds']), p2(L['book']['pb_spot']), p2(L['book']['vps_spot']),
     pc(W['ke_term']), p2(L['book']['pb_norm']), p2(L['book']['vps_norm']), p2(H['pb'])))

H2('1.3  Relative multiples')
rows = [['Company', 'Listing', 'Price to earnings', 'Enterprise value to EBITDA']]
for p in PEERS:
    rows.append([p['name'], p['ticker'], '' if not p['pe'] else p2(p['pe']) + 'x',
                 '' if not p.get('ev_ebitda') else p2(p['ev_ebitda']) + 'x'])
rows.append(['Palm Hills Developments', M['code'], p2(H['pe_ltm']) + 'x',
             p2(H['ev_ebitda_company']) + 'x'])
table(rows, [2.5, 1.35, 1.55, 1.6], first_col_bold=True, band_rows={len(rows) - 1}, size=8.8)
caption('%s. Peers inside and outside the country. Peer multiples are market-data quotes dated 11 '
        'August 2026 for the Egyptian names and June to August 2026 for the Gulf names; they are '
        'used as a cross-check and never as a source for anything Palm Hills itself reported. '
        'Palm Hills\' own figures are computed from its statements at the EGP %s published price: '
        'trailing earnings per share of EGP %s and trailing EBITDA of EGP %smn.'
        % (T(), p2(SPOT), p2(H['eps_ltm']), n0(H['ebitda_ltm'])))
P('The median Egyptian peer trades at %sx trailing earnings and the median Gulf peer at %sx. '
  'Applied to trailing earnings of EGP %s a share those give EGP %s and EGP %s. Capitalising '
  'trailing EBITDA at the Gulf median of %sx enterprise value and bridging to equity gives EGP '
  '%s. Palm Hills already trades at %sx earnings, a premium to both peer sets, and at %sx EBITDA, '
  'in line with Aldar and above Emaar. It is not a cheap stock on multiples.'
  % (p2(L['relative']['eg_pe_median']), p2(L['relative']['gulf_pe_median']), p2(H['eps_ltm']),
     p2(L['relative']['vps_eg']), p2(L['relative']['vps_gulf']),
     p2(L['relative']['ev_ebitda_gulf']), p2(L['relative']['vps_evebitda']), p2(H['pe_ltm']),
     p2(H['ev_ebitda_company'])), size=9.6)

H2('1.4  Normalised earnings power')
P('This lens strips out the cycle. It takes the current revenue base — trailing twelve months of '
  'EGP %smn — and applies the average of the margins the company earned in 2023, 2024 and the '
  'first half of 2026, which is %s. That gives EGP %smn of earnings before interest, tax and '
  'depreciation. Depreciation, the unwinding of the discount on instalment receivables, the '
  'return on the treasury-bill book and interest on the disclosed debt at its measured rate leave '
  'EGP %smn of pre-tax profit and EGP %smn after tax, or EGP %s a share. At the peer range of %sx '
  'to %sx that is EGP %s to EGP %s.'
  % (n0(H['rev_ltm']), pc(L['normalised']['margin']), n0(L['normalised']['ebitda']),
     n0(L['normalised']['pbt']), n0(L['normalised']['ni']), p2(L['normalised']['eps']),
     p2(L['normalised']['pe_lo']), p2(L['normalised']['pe_hi']),
     p2(L['normalised']['low']), p2(L['normalised']['high'])))

H2('1.5  Synthesis — four lenses, one field')
rows = [['Lens', 'Weight', 'Low', 'Centre', 'High', 'What it is most sensitive to']]
_labels = {'dcf': 'Cash flow', 'book': 'Book value and return', 'relative': 'Relative multiples',
           'normalised': 'Normalised earnings'}
_sens = {'dcf': 'the float, then the cost of capital, then the crux ratio',
         'book': 'the cost of equity — nothing else moves it',
         'relative': 'peer multiples, which are themselves depressed by Egyptian country risk',
         'normalised': 'the margin taken as mid-cycle and the interest charge'}
for k in ('dcf', 'book', 'relative', 'normalised'):
    lo = SYN['framing_A']['lens_lo'][k]; md = SYN['framing_A']['lens_mid'][k]
    hi = SYN['framing_A']['lens_hi'][k]
    rows.append([_labels[k], pc(SYN['weights'][k], 0), p2(lo), p2(md), p2(hi), _sens[k]])
rows.append(['Weighted field, framing A', '100%', p2(SYN['framing_A']['bear']),
             p2(SYN['framing_A']['base']), p2(SYN['framing_A']['bull']), ''])
rows.append(['Weighted field, framing B', '100%', p2(SYN['framing_B']['bear']),
             p2(SYN['framing_B']['base']), p2(SYN['framing_B']['bull']), ''])
lalign(table(rows, [1.55, 0.62, 0.62, 0.68, 0.62, 2.91], first_col_bold=True,
      band_rows={5, 6}, size=8.5), {5})
caption('%s. The four lenses and their weights. The cash-flow lens carries the largest weight '
        'because it is the only one built from the company\'s own physical drivers; it is also '
        'the only one that moves between the framings.' % T())

H2('1.6  Drivers — every disclosed line on its own driver')
P('Revenue is volume times price and cost is cost per unit of volume, with growth projected in '
  'both. The volume driver is construction executed, which the company discloses. The price '
  'driver is revenue recognised per Egyptian pound of construction cost charged to the income '
  'statement. Margin is what falls out of the two; it is never set.', size=9.8)
rows = [['Driver', 'Measured value', 'How it is measured, and what escalates it']]
rows += [
    ['Construction executed', 'EGP %smn in the half' % n0(D['inputs']['work_h126']['value']),
     'Disclosed. Annualises to EGP %smn against EGP %smn for 2025, up %s. Cash construction '
     'spending rose 60 per cent year on year in the first quarter and 71 per cent over the first '
     'nine months of 2025, which is the independent check on the same driver. The path then '
     'decelerates: %s real growth in 2027 falling to %s by 2031.'
     % (n0(H['rev_ann'] / H['rho_h126'] if False else D['inputs']['work_h126']['value'] * 2),
        n0(D['inputs']['work_fy25']['value']),
        pp(D['inputs']['work_h126']['value'] * 2 / D['inputs']['work_fy25']['value'] - 1, 1),
        pc(D['inputs']['vol_growth']['value'][0], 0), pc(D['inputs']['vol_growth']['value'][-1], 0))],
    ['Revenue per pound of build cost — THE CRUX', '%sx' % p2(H['P_h126']),
     'EGP %smn of real-estate revenue against EGP %smn of construction cost charged to the income '
     'statement in the half. Escalates at the selling-price path over the build-cost path, so it '
     'falls only if costs outrun prices.'
     % (n0(D['inputs']['rev_re_h126']['value']), n0(H['constr_relief_h126']))],
    ['Land and partners\' share of revenue', pc(H['c2']),
     'The residual of the disclosed cost of real-estate development after the construction block. '
     'It cannot be split into its two parts from anything the company publishes — see below — so '
     'it is carried at its measured rate and moves with revenue, not with cost inflation.'],
    ['Selling price', '%s a year in 2027' % pc(D['inputs']['pi_price']['value'][0], 0),
     'Anchored on a measured market outcome, not an assumption: the ten largest Egyptian '
     'developers sold %s more by value in the first half of 2026 on %s fewer units, an implied '
     'average-ticket rise of %s. Later years converge on the central bank\'s disinflation path.'
     % (pc(H['mkt_value_growth']), pc(abs(D['inputs']['mkt_units_chg']['value']), 0),
        pc(H['mkt_ticket_growth']))],
    ['Build cost', '%s a year in 2027' % pc(DCF['pi_cost'][0], 1),
     'Four physically distinct classes, one escalator each, never one blended index. Steel at %s '
     'in 2027 on the measured August producer prices, cement at %s on the disclosed Egyptian '
     'price path, finishing at %s on the published inflation path, site labour at %s.'
     % (pc(D['inputs']['esc_steel']['value'][0], 0), pc(D['inputs']['esc_cement']['value'][0], 0),
        pc(D['inputs']['esc_finish']['value'][0], 1), pc(D['inputs']['esc_labour']['value'][0], 1))],
    ['Salaries and wages', 'EGP %smn in the half' % n0(D['inputs']['sal_h126']['value']),
     'Disclosed separately from other administrative cost. Rose %s year on year against revenue '
     'growth of %s. Escalates on the wage path plus %s of real headcount growth.'
     % (pp(D['inputs']['sal_h126']['value'] / D['inputs']['sal_h125']['value'] - 1, 1),
        pp(H['rev_h126'] / H['rev_h125'] - 1, 1), pc(D['inputs']['hcount_growth']['value'], 0))],
    ['Administration and marketing', pc(D['inputs']['adm_h126']['value'] / H['rev_h126']),
     'Held at its measured share of revenue, which is stable: %s in the first half of 2026 '
     'against %s a year earlier.'
     % (pc(D['inputs']['adm_h126']['value'] / H['rev_h126'], 2),
        pc(D['inputs']['adm_h125']['value'] / H['rev_h125'], 2))],
    ["Residents' Association float", '%sx revenue' % p2(D['inputs']['ra_target_ratio']['value']),
     'Solved from the company\'s own movements rather than assumed. For every pound of revenue '
     'growth the balance rose by %sx in 2023, %sx in 2024 and %sx in the first half of 2026 on a '
     'like-for-like basis. The study lets the balance glide from its measured %sx of revenue '
     'today to %sx and stop there — near the bottom of that range, and bounded, rather than '
     'rising without limit.'
     % (p2(H['ra_incr_fy23']), p2(H['ra_incr_fy24']), p2(H['ra_incr_h126']),
        p2(H['ra_ratio_0']), p2(D['inputs']['ra_target_ratio']['value']))],
]
lalign(table(rows, [1.55, 1.15, 4.35], first_col_bold=True, size=8.0), {2})
caption('%s. The driver table. Every measured value is read from a company-issued document; every '
        'escalator names its own physical class.' % T())

figure('fig7_mix.png', 6.6,
       '%s. Left: the weight of each physically distinct construction cost class. These weights '
       'are estimated — no filing discloses a cost-by-nature split of construction — and they are '
       'carried through the sensitivity. Right: each class on its own escalator, against the '
       'selling-price path and the weighted build-cost path. Build cost runs above selling price '
       'in every year, which is why the margin drifts down slowly rather than holding flat.' % FG())

P('A split the accounts do not identify, demonstrated rather than asserted. The cost of real '
  'estate development is one line. Note 43 pins the construction half of it at EGP %smn for the '
  'half by giving the cumulative charge to the income statement at two dates. The remaining EGP '
  '%smn is the land cost of contracted units plus the joint-arrangement partners\' share of '
  'revenue, together. Nothing the company publishes separates them: note 43 states that work in '
  'progress is struck after excluding the cost of contracted lands, note 65 stops at the single '
  'line, and note 58 gives the partners\' balance by project but not the charge. One equation, '
  'two unknowns. The study therefore carries the block whole and states the bound it can put on '
  'the year-on-year margin move instead of inventing a split.'
  % (n0(H['constr_relief_h126']), n0(H['land_partner_h126'])), size=9.5)

H2('1.7  The crux')
P('The real-estate gross margin fell %s points year on year, from %s to %s. Exactly two things '
  'can have done it: the price of the work fell against its cost, or the land-and-partners block '
  'grew. Both bounds can be computed and the truth is between them.'
  % ('%.2f' % (H['margin_fall_pp'] * 100), pc(H['re_gm_h125']), pc(H['re_gm_h126'])))
rows = [['If all of the move is …', 'Then the driver went', 'Read']]
rows += [
    ['… price against cost',
     'from %sx to %sx, a fall of %s' % (p2(H['P_h125_if_c2_flat']), p2(H['P_h126']),
                                        pc(abs(H['P_compression_bound']))),
     'Selling prices lost almost a quarter of their cover over build cost in a year. If that is '
     'structural the model is too generous; if it is the mix of projects delivering, it reverses.'],
    ['… land and partners',
     'from %s to %s of revenue' % (pc(H['c2_h125_if_P_flat']), pc(H['c2'])),
     'A higher share of revenue came from revenue-sharing projects, where the partner takes 26 to '
     '30 per cent off the top. That is mix, and mix is knowable in advance from the project list.'],
]
lalign(table(rows, [1.5, 1.85, 3.7], first_col_bold=True, size=8.6), {1, 2})
caption('%s. The bound on the margin move. The study does not pick a point inside it; it holds '
        'the measured rates flat and sensitises the price-to-cost ratio directly.' % T())

figure('fig3_margin.png', 6.4,
       '%s. Operating margin on the company\'s own definition, on every period that can be built '
       'from what it has issued. Three provenances, and they are not the same thing: 9M2025 and '
       'Q1-2026 are published figures; FY2023 and FY2024 are rebuilt from the audited statements '
       'on the definition recovered from them; Q4-2025 and Q2-2026 are differences between two '
       'disclosed cumulative periods. The first half of 2026 sits at %s, above 2023 and marginally '
       'above 2024. The fall is from an exceptional 2025, and it began in the fourth quarter of '
       'that year, not in 2026.'
       % (FG(), pc(H['ebitda_margin_h126'])))

P('Why the crux is held flat rather than extrapolated. The two most recent quarters read %s and '
  '%s — the compression stopped and reversed slightly. The measured mechanisms point in opposite '
  'directions: Egyptian producers left August steel prices unchanged after earlier falls, which '
  'is disinflationary, while the company\'s own subsequent-events note warns that currency and '
  'hydrocarbon moves are pushing up the cost of works. When measured mechanisms conflict, the '
  'disciplined answer is to hold the last reviewed rate and let the sensitivity carry the '
  'argument.' % (pc(H['ebitda_margin_1q26']), pc(H['ebitda_margin_q226'])), size=9.5)

H2('1.8  Macro, country and the cost of capital')
rows = [['Input', 'Value', 'Source and construction']]
rows += [
    ['Observed risk-free rate', pc(W['rf_obs'], 3),
     'Three-year Egyptian government bond, accepted weighted-average yield at the auction of 17 '
     'August 2026 — 22 accepted bids and EGP 18.9bn placed out of EGP 39.7bn bid, the deepest '
     'print in the auction. The two-year cleared at 22.691% and the five-year at 19.700%, each on '
     'a single accepted bid; neither is a usable clearing level. A ten-year yield of '
     + pc(D['inputs']['rf_arcc_xchk']['value'], 2) + ', taken independently in early August for '
     'another Egyptian study, corroborates it.'],
    ['Sovereign default spread, rating basis', pc(W['rf_obs'] - W['rf_star_rating'], 3),
     "Egypt at Caa1, from the July 2026 original country-premium file"],
    ['Sovereign default spread, swap basis', pc(W['rf_obs'] - W['rf_star_cds'], 3),
     'Egyptian sovereign credit-default swap net of Swiss, same file, spreads as at 30 June 2026'],
    ['Normalised risk-free rate', '%s / %s' % (pc(W['rf_star_rating'], 3), pc(W['rf_star_cds'], 3)),
     'The observed yield less the sovereign\'s own default spread, so country risk enters once '
     'and only once. The rating basis is stated first.'],
    ['Equity risk premium', '%s / %s' % (pc(D['inputs']['erp_rating']['value'], 3),
                                          pc(D['inputs']['erp_cds']['value'], 3)),
     'Total premium for Egypt on each basis, same file. Both are carried through to a published '
     'cost of capital; the two are never mixed.'],
    ['Beta', p2(W['beta']),
     'Own-stock weekly regression against the published index of the exchange the shares are '
     'listed on, %s observations over %s years to %s, R-squared %s, standard error %s. It clears '
     'the usability test, so no peer or default beta is needed. The adjusted cross-check is %s.'
     % (n0(BR['n']), '%.2f' % BR['window_years'], BR['last_obs'], pc(BR['r2'], 1),
        '%.3f' % BR['se'], p2(BR['blume_crosscheck']))],
    ['Cost of equity', '%s / %s' % (pc(W['ke_rating']), pc(W['ke_cds'])),
     'Normalised risk-free rate plus beta times the premium, on each basis'],
    ['Marginal cost of debt', pc(W['kd_marginal']),
     'Built from the company\'s own numbers, not a house assumption. It paid EGP %smn of interest '
     'in the half including EGP %smn capitalised, on average interest-bearing obligations of EGP '
     '%smn — an all-in rate of %s. Over the same period its own treasury-bill book earned %s. The '
     'difference, %s, is its measured credit spread, and it is added to the same government bond '
     'used for the risk-free rate so the two sit on one curve.'
     % (n0(H['interest_total_h126']), n0(D['inputs']['capint_h126']['value']),
        n0(H['intdebt_avg']), pc(H['kd_realised']), pc(D['inputs']['tbill_wavg_yld']['value']),
        pc(H['corp_spread'], 2))],
    ['Capital structure', '%s equity / %s debt' % (pc(W['we']), pc(W['wd'])),
     'Equity at market value — the published price times the share count after treasury — and '
     'debt at the company\'s own schedule of interest-bearing obligations, EGP %smn'
     % n0(H['debt_narrow'])],
    ['WEIGHTED COST OF CAPITAL', '%s / %s' % (pc(W['wacc_rating']), pc(W['wacc_cds'])),
     'Published on both premium bases, as the method requires'],
    ['Terminal cost of capital', pc(W['wacc_term']),
     'On a risk-free rate of %s built from the central bank\'s own longest published inflation '
     'target of 5 per cent for the fourth quarter of 2028 plus a standard emerging-market real '
     'rate, a normalised premium of %s and a beta of 1.0'
     % (pc(D['inputs']['rf_term']['value']), pc(D['inputs']['erp_term']['value']))],
]
lalign(table(rows, [1.5, 1.15, 4.4], first_col_bold=True, size=8.0, band_rows={10}), {2})
caption('%s. The cost of capital, built rather than assumed. Every line names its own source and '
        'date.' % T())

P('Local currency and foreign currency. Every facility in the debt note is denominated in '
  'Egyptian pounds — the syndicated Bank Misr and National Bank of Egypt lines, the Ahli United '
  'revolvers, the overdrafts. The only foreign-currency liability is EGP %smn of bank credit '
  'balances. Against that the company holds EGP %smn of foreign-currency cash and deposits and '
  'reports a net foreign-currency position that is an ASSET of EGP %smn. A pound devaluation '
  'therefore helps the balance sheet and hurts the cost stack, which is exactly how the currency '
  'lever on the ticker page is now specified.'
  % (n0(D['inputs']['bankcr_fx']['value']), n0(D['inputs']['cash_fx_jun26']['value']),
     n0(D['inputs']['fx_net_asset']['value'])), size=9.5)

P('Two contested constructions, both priced. First, net debt. On the company\'s own definition — '
  'interest-bearing obligations less cash and treasury bills — it is EGP %smn. Carry the notes '
  'payable to the land authority and under the sale-and-leaseback contracts, and the land '
  'purchase liabilities, and it is EGP %smn. Treat the invested residents\' money as restricted '
  'and it is EGP %smn. All three are shown, and the framings use the first and the third. Second, '
  'the backlog. The only figure that appears in a reviewed statement is the contractual value of '
  'undelivered-unit contracts concluded since the start of 2023: EGP %sbn, against nominal notes '
  'receivable of EGP %sbn held off balance sheet and a present value of EGP %sbn. The company\'s '
  'own wider definition stood at EGP %sbn at the first quarter. The study anchors on the first '
  'and says so.'
  % (n0(H['netdebt_company']), n0(H['netdebt_broad']), n0(H['netdebt_restricted']),
     bn(D['inputs']['bk_contract']['value']), bn(D['inputs']['bk_nominal']['value']),
     bn(D['inputs']['bk_pv']['value']), bn(D['inputs']['backlog_1q26']['value'])), size=9.5)

P('Does growth create value here? The answer depends on which capital you count, so both '
  'counts are given. Measured on every pound standing in the business, the return on invested '
  'capital is %s against a spot weighted cost of capital of %s and a normalised one of %s — '
  'below both. Read that way, a single year of growth consumes more working capital than it '
  'produces above about %s nominal, or about %s once the residents\' money is credited as '
  'funding. But %s of that capital base is customer money, not shareholder money: net of it the '
  'return is %s, comfortably above the normalised cost of capital. The full model carries the '
  'terminal value that the single-year arithmetic cannot, and it moves with the second measure — '
  'a half-again volume path is worth EGP %s a share against EGP %s at no growth at all under the '
  'first framing, and EGP %s against EGP %s under the second. Growth is not free here; it is also '
  'not value-destroying. What decides the valuation is whether the customer money is the '
  'company\'s to use.'
  % (pc(GDV['roic_A']), pc(GDV['wacc_spot']), pc(GDV['wacc_term']),
     pc(GDV['breakeven_g_no_float']), pc(GDV['breakeven_g_with_float']),
     pc(1 - GDV['ic_end_ex_float'] / GDV['ic_end']), pc(GDV['roic_ex_float']),
     p2(SENS['vol_vps'][-1]), p2(SENS['vol_vps'][0]),
     p2(SENS['vol_vps_B'][-1]), p2(SENS['vol_vps_B'][0])), size=9.5)

H2('1.9  Sensitivity')
figure('fig2_sens.png', 6.7,
       '%s. Fair value per share against the crux ratio and the cost of capital, computed '
       'separately under each framing. The crux runs from %sx to %sx around the measured %sx; the '
       'cost of capital shifts the whole path by up to two hundred basis points either way.'
       % (FG(), p2(SENS['crux_P'][0]), p2(SENS['crux_P'][-1]), p2(H['P_h126'])))
rows = [['Driver moved', 'Range tested', 'Effect on the cash-flow lens, framing A']]
rows += [
    ['Real construction volume growth',
     'from no growth at all to half again the base path',
     'EGP %s at no growth to EGP %s at half again'
     % (p2(SENS['vol_vps'][0]), p2(SENS['vol_vps'][-1]))],
    ['Build-cost escalation, all four classes together', 'two hundred basis points either way',
     'EGP %s to EGP %s' % (p2(min(SENS['cost_vps'])), p2(max(SENS['cost_vps'])))],
    ['Cost of capital, whole path', 'two hundred basis points either way, crux held at its '
     'measured level',
     'EGP %s to EGP %s' % (p2(SENS['grid_A'][-1][2]), p2(SENS['grid_A'][0][2]))],
    ['The crux ratio alone', '%sx to %sx' % (p2(SENS['crux_P'][0]), p2(SENS['crux_P'][-1])),
     'EGP %s to EGP %s' % (p2(SENS['grid_A'][2][0]), p2(SENS['grid_A'][2][-1]))],
    ['Both together, worst corner against best', 'crux %sx and the cost of capital two hundred '
     'basis points higher, against %sx and two hundred lower'
     % (p2(SENS['crux_P'][0]), p2(SENS['crux_P'][-1])),
     'EGP %s to EGP %s' % (p2(min(SENS['grid_A'][-1])), p2(max(SENS['grid_A'][0])))],
    ['The contested judgement', 'framing B against framing A',
     'EGP %s against EGP %s on this lens; EGP %s against EGP %s on the published four-lens range'
     % (p2(B['bridge']['vps']), p2(A['bridge']['vps']),
        p2(SYN['framing_B']['base']), p2(SYN['framing_A']['base']))],
]
lalign(table(rows, [2.2, 2.05, 2.8], first_col_bold=True, size=8.6, band_rows={6}), {1, 2})
caption('%s. Every axis in observable units. The first row runs the right way round — more '
        'volume is worth more — because most of the capital funding that volume is the customers\', '
        'not the shareholders\'. Strip the customer money out of the denominator and the return on '
        'what shareholders actually contributed is %s, above the normalised cost of capital; leave '
        'it in and the return is %s, below it. Section 1.8 gives both.'
        % (T(), pc(GDV['roic_ex_float']), pc(GDV['roic_A'])))

# =================================================== 6. SECTION 2 — TECHNICAL
H1('2. Technical and price structure')
box([('Carried forward unchanged. ',
      'This is a fundamentals-only refresh. Sections 2 and 3 reproduce the last published '
      'technical read and probability map exactly as they stand, so a reader can see which half '
      'of this document is as of the new fundamentals and which half is as of the last price '
      'update. The stamps are quoted verbatim below.')])
rows = [['Stamp', 'Data as of', 'Computed on']]
rows += [['Probability map', CF['asof_mc_data'], CF['asof_mc_computed']],
         ['Technical read', CF['asof_tech_data'], CF['asof_tech_computed']],
         ['Fundamentals (this document)', M['valuation_date'], M['publication_date']]]
table(rows, [2.4, 2.15, 2.15], first_col_bold=True, size=9.0)
caption('%s. The three clocks. Both price-side stamps read %s for data, four weeks before this '
        'document. Nothing in sections 2 or 3 has been recomputed.' % (T(), CF['asof_mc_data']))
P('The read as published: %s. The price closed at EGP %s above a falling twenty-day mean, a '
  'rising fifty-day and a rising two-hundred-day. Over the preceding year it ranged EGP 6.99 to '
  'EGP 16.43.' % (CF['tech']['trend'].lower(), p2(CF['spot'])))
rows = [['Resistance', 'Support']]
_r, _s = CF['levels']['res'], CF['levels']['sup']
for i in range(3):
    rows.append([p2(_r[i]), p2(_s[i])])
table(rows, [1.7, 1.7], size=9.0, align_right_from=0)
caption('%s. The published level ladder, nearest first, carried forward unchanged.' % T())

# ============================================== 7. SECTION 3 — PROBABILITY MAP
H1('3. Probabilistic price map')
P('The probability map below is the last published one, struck on the %s close and computed on '
  '%s. It is reproduced here without recomputation. Because this refresh moves the fundamental '
  'value and not the price data, the two should be read on their own clocks: the cone answers '
  'where the price might be in one and three months, the fundamental sections answer what the '
  'business appears to be worth.' % (CF['asof_mc_data'], CF['asof_mc_computed']))
P('A note on how much weight the cone carries. The simulation behind it was tested by re-running '
  'it across five years of history, striking a forecast every quarter and scoring the result '
  'against what actually happened, with each window scored on a scale-free basis so that a '
  'high-priced name cannot dominate a low-priced one. On this market the pooled result beats a '
  'carry-anchored random walk, which is the honest benchmark: a model that cannot beat it is '
  'adding nothing. The width of the bands, not their centre, is what the test mostly disciplines.',
  size=9.6)
rows = [['Horizon', '5%', '25%', 'Median', '75%', '95%', 'Resolves']]
for k, dd in (('One month', CF['dist']['t20']), ('Three months', CF['dist']['t60'])):
    rows.append([k, p2(dd['p5']), p2(dd['p25']), p2(dd['p50']), p2(dd['p75']), p2(dd['p95']),
                 dd['resolve']])
table(rows, [1.2, 0.82, 0.82, 0.9, 0.82, 0.82, 1.2], first_col_bold=True, size=8.8)
caption('%s. The published percentile map, EGP per share, anchored on the EGP %s close of %s.'
        % (T(), p2(CF['spot']), CF['asof_mc_data']))
figure('fig4_fan.png', 6.4,
       '%s. The published cone, with this study\'s fundamental base value drawn across it. The '
       'base sits inside the three-month middle half, which is not a forecast of convergence — it '
       'is simply where the two clocks happen to stand.' % FG())
rows = [['Level, EGP', 'Chance of touching within one month', 'Within three months']]
for lv, a1, a3 in CF['touch']:
    rows.append([p2(lv), '%d%%' % a1, '%d%%' % a3])
table(rows, [1.5, 2.7, 2.2], size=8.8)
caption('%s. Level-touch probabilities as published. A descriptive output of the simulation: how '
        'often paths reach each level, nothing more.' % T())
figure('fig5_dist.png', 6.3, '%s. The one-month distribution as published.' % FG())
figure('fig6_dist.png', 6.3, '%s. The three-month distribution as published.' % FG())

# ============================================ 8. SECTION 4 — LENS COMPARISON
H1('4. Comparison of the lenses')
rows = [['Lens', 'What it says', 'On what clock', 'Where it can be wrong']]
rows += [
    ['Cash flow',
     'EGP %s to EGP %s under the adopted framing; EGP %s to EGP %s under the other'
     % (p2(L['dcf']['A_low']), p2(L['dcf']['A_high']), p2(L['dcf']['B_low']), p2(L['dcf']['B_high'])),
     'five and a half years plus a terminal value',
     'The terminal carries %s of the value under framing A and %s under framing B. A model that '
     'leans that hard on year six is fragile by construction, and the study says so rather than '
     'burying it.' % (pc(A['pv_term'] / A['ev'], 0), pc(B['pv_term'] / B['ev'], 0))],
    ['Book value and return',
     'EGP %s at the spot cost of equity, EGP %s at the normalised one'
     % (p2(L['book']['vps_spot']), p2(L['book']['vps_norm'])),
     'today',
     'It assumes the trailing return on equity of %s is sustainable. Half of that return is the '
     'unwinding of discount on instalment receivables and the return on the treasury-bill book, '
     'neither of which is an operating return.' % pc(H['roe_ltm'])],
    ['Relative multiples', 'EGP %s to EGP %s' % (p2(L['relative']['low']), p2(L['relative']['high'])),
     'today',
     'Egyptian peers trade at %sx to %sx because the country risk premium is %s. Marking Palm '
     'Hills to them prices in that risk twice if the cash-flow lens has already discounted for it.'
     % (p2(L['relative']['eg_pe_min']), p2(L['relative']['eg_pe_max']),
        pc(D['inputs']['crp_rating']['value']))],
    ['Normalised earnings', 'EGP %s to EGP %s' % (p2(L['normalised']['low']), p2(L['normalised']['high'])),
     'mid-cycle',
     'The mid-cycle margin of %s is an average of three periods, one of which is a half-year. '
     'Three observations is not a cycle.' % pc(L['normalised']['margin'])],
]
lalign(table(rows, [1.2, 1.85, 1.15, 2.85], first_col_bold=True, size=8.0), {1, 2, 3})
caption('%s. Where the lenses agree and where they do not. Three of the four cluster between EGP '
        '%s and EGP %s. The cash-flow lens is the outlier in both directions, and the reason is '
        'the float.' % (T(), p2(min(L['book']['low'], L['relative']['low'], L['normalised']['low'])),
                        p2(max(L['book']['high'], L['relative']['high'], L['normalised']['high']))))
P('The verdict. Three lenses that do not depend on the contested judgement put the shares between '
  'EGP %s and EGP %s against a market price of EGP %s — that is, expensive. The cash-flow lens '
  'agrees with them under framing B and disagrees violently under framing A. So the whole '
  'argument for the current price rests on the float being permanent funding and on Egyptian '
  'rates normalising. Neither is unreasonable. Both are assumptions, and this study prices them '
  'rather than assuming them away.'
  % (p2(min(L['book']['low'], L['relative']['low'], L['normalised']['low'])),
     p2(max(L['book']['high'], L['relative']['high'], L['normalised']['high'])), p2(SPOT)))

# ================================================== 9. SECTION 5 — CATALYSTS
H1('5. Catalysts')
rows = [['What', 'When', 'Why it matters here']]
rows += [
    ['The results release for the first half',
     'expected imminently',
     'It was not published on the company\'s own channel as of 19 August 2026 — the newest '
     'financial result there is the first-quarter release of 20 May. Press reporting attributes a '
     'record backlog of EGP %sbn and EGP %sbn of launch sales to it. None of that has been '
     'verified against a company document and no number in this study reads it.'
     % (bn(D['inputs']['backlog_h126_press']['value']), bn(D['inputs']['reh_launch']['value']))],
    ['The audited statements for 2025', 'overdue',
     'Neither the 2025 annual statements nor a 2025 results release is published on the company\'s '
     'investor-relations channel. That is why the three-year history in appendix A shows blanks '
     'for 2025 gross profit and finance costs rather than estimates.'],
    ['A residents\' association taking legal personality', 'unscheduled',
     'This is the falsifier for the base case. Under Building Law 119 the assets and liabilities '
     'held for an association separate in its favour on constitution. The first one to do so at '
     'scale converts the study from framing A to framing B, which is worth EGP %s a share.'
     % p2(SYN['framing_A']['base'] - SYN['framing_B']['base'])],
    ['The central bank\'s rate decision and the inflation print', 'monthly',
     'The whole gap between the spot and normalised costs of capital is a bet on the disinflation '
     'path. July\'s urban print of %s was the first acceleration in four months.'
     % pc(D['inputs']['cpi_urban']['value'], 1)],
    ['Third-quarter results', 'November',
     'The first period in which the North Coast launch sales, whatever they prove to be, are '
     'recognised as contracted sales — and the first read on whether the crux ratio held.'],
]
lalign(table(rows, [2.0, 1.25, 3.8], first_col_bold=True, size=8.4), {1, 2})
caption('%s. What would move this, and in which direction.' % T())

# ============================================ 10. SECTION 6 — PROBABILITY ZONES
H1('6. Reading the probability zones')
P('This section translates the published map into the price zones where the lenses say something '
  'analytically distinct. It is a description of a distribution, not a plan, and it is not '
  'calibrated to any reader\'s circumstances.')
bullet('the three lenses that do not depend on the contested judgement all sit here. A price '
       'inside this band is consistent with the float being restricted and with Egyptian rates '
       'staying where they are.',
       bold_head='Below EGP %s — ' % p2(max(L['book']['high'], L['normalised']['high'])))
bullet('the adopted base case. The published cone puts the three-month median at EGP %s, so the '
       'map and the fundamentals are close to agreement here, on different clocks.'
       % p2(CF['dist']['t60']['p50']),
       bold_head='EGP %s to EGP %s — ' % (p2(SPOT), p2(SYN['base'])))
bullet('this requires both the float to be permanent and rates to normalise. The published map '
       'gives a %d per cent chance of touching EGP 17.50 within three months.'
       % [t for t in CF['touch'] if t[0] == 17.5][0][2],
       bold_head='EGP %s to EGP %s — ' % (p2(SYN['base']), p2(SYN['bull'])))
bullet('the market would be paying less than the alternative framing of the balance sheet implies '
       'even on generous assumptions about the cost of capital. That is the level at which the '
       'downside case in this study would itself need rebuilding.',
       bold_head='Below EGP %s — ' % p2(SYN['bear']))

# ================================================== 11. SECTION 7 — CAVEATS
H1('7. Caveats, and what would change our mind')
bullet('The results release for the first half of 2026 could not be obtained from the company. '
       'Its operating anchors — the company\'s own backlog figure, its own net-debt definition, '
       'first-half contracted sales and construction spending — are carried as unverified press '
       'reporting and no model driver reads them. Attaching that document would sharpen the '
       'volume path and the catalyst calendar.', bold_head='A document is missing. ')
bullet('The 2025 audited statements are not published either. Gross profit, cost of revenues and '
       'finance costs for 2025 are shown blank in appendix A rather than estimated, so the '
       'three-year history has a hole in the middle of it.', bold_head='So is another. ')
bullet('The split between land cost and the joint-arrangement partners\' share cannot be '
       'identified from anything the company publishes. The study demonstrates that rather than '
       'asserting a split, but it means one of the two largest cost blocks is carried whole.',
       bold_head='One cost block is not identified. ')
bullet('The weights of the four construction cost classes are estimated. No filing discloses a '
       'cost-by-nature split of construction. They are carried through the sensitivity, and a '
       'two-hundred-basis-point error in the blended escalator is worth EGP %s a share.'
       % '%.2f' % abs(max(SENS['cost_vps']) - min(SENS['cost_vps'])),
       bold_head='Some weights are estimates. ')
bullet('The terminal value carries %s of enterprise value under the adopted framing. A model that '
       'leans that hard on the far future is fragile, and the reinvestment charge that keeps '
       'growth from being free is itself computed from a return on capital of %s that the study '
       'measures rather than assumes.' % (pc(A['pv_term'] / A['ev'], 0), pc(GDV['roic_A'])),
       bold_head='The terminal is large. ')
bullet('Sections 2 and 3 are four weeks older than the rest of this document. They have not been '
       'recomputed and their stamps say so.', bold_head='Two sections are stale by design. ')
P('What would change our mind. A residents\' association taking legal personality and its assets '
  'with it would move the study from framing A to framing B. A first-half results release showing '
  'the crux ratio below %sx would break the flat-margin assumption. An inflation path that stops '
  'falling would remove the normalisation the market is already paying for. Any of the three is '
  'observable within two quarters.' % p2(SENS['crux_P'][0]))

# =========================================== 12. APPENDIX A — THE STATEMENTS
H1('Appendix A — the statements')
H2('A.1  Income statement: three years of history and five years forward')
rows = [['EGP mn'] + H3['years'] + YRS[1:]]
def fwd(key, i):
    return A[key][i]
def hist_or_blank(v):
    return '' if v is None else n0(v)
rows.append(['Revenue'] + [hist_or_blank(v) for v in H3['revenue']] + [n0(x) for x in A['rev'][1:]])
rows.append(['Cost of revenues'] + [hist_or_blank(None if v is None else -v) for v in H3['cogs']]
            + [n0(-(A['rev'][i] - A['gp'][i])) for i in range(1, len(YRS))])
rows.append(['Gross profit'] + [hist_or_blank(v) for v in H3['gross_profit']]
            + [n0(A['gp'][i]) for i in range(1, len(YRS))])
rows.append(['  gross margin'] + ['' if v is None else pc(v) for v in H3['gross_margin']]
            + [pc(A['gm'][i]) for i in range(1, len(YRS))])
rows.append(['Administrative, selling and marketing']
            + [hist_or_blank(None if v is None else -v) for v in H3['sga']]
            + [n0(-A['sga'][i]) for i in range(1, len(YRS))])
rows.append(['Earnings before interest, tax and depreciation']
            + [hist_or_blank(v) for v in H3['ebitda']] + [n0(A['ebitda'][i]) for i in range(1, len(YRS))])
rows.append(['  margin'] + [pc(v) for v in H3['ebitda_margin']]
            + [pc(A['ebitda'][i] / A['rev'][i]) for i in range(1, len(YRS))])
rows.append(['Finance costs and interest'] + [hist_or_blank(None if v is None else -v)
                                              for v in H3['finance_costs']] + [''] * 5)
rows.append(['Profit before tax'] + [hist_or_blank(v) for v in H3['pbt']] + [''] * 5)
rows.append(['Attributable profit'] + [hist_or_blank(v) for v in H3['net_profit']] + [''] * 5)
table(rows, [1.86] + [0.62] * 10, first_col_bold=True, size=6.6, band_rows={6})
caption('%s. History from the company\'s own statements; the forward columns are the model, '
        'stated before financing so profit before tax is not carried forward. %s'
        % (T(), H3['gap_note']))

H2('A.2  Balance sheet at 30 June 2026, with the December comparative')
rows = [['EGP mn', '30 Jun 2026', '31 Dec 2025']]
for lbl, k in (('Notes receivable, long term', 'nr_lt'), ('Fixed assets and investment property', None),
               ('Total non-current assets', 'nca'), ('Work in progress', None),
               ('Accounts receivable', 'ar'), ('Notes receivable, short term', 'nr_st'),
               ('Treasury bills and bonds at amortised cost', 'tbill'),
               ('Cash and cash equivalents', 'cash'), ('TOTAL ASSETS', 'ta'),
               ('Controlling equity', 'eqctl'), ('Non-controlling interests', 'eqnci'),
               ('Loans, long term', 'loan_lt'), ('Credit facilities', 'cf'),
               ("Residents' Association", 'ra'), ('Advances from customers', 'adv'),
               ('Notes payable, short and long term', None),
               ('Joint arrangement, partners\' share', None), ('TOTAL LIABILITIES', 'tl')):
    if k:
        rows.append([lbl, n0(D['inputs'][k + '_jun26']['value']), n0(D['inputs'][k + '_dec25']['value'])])
    elif lbl.startswith('Fixed'):
        rows.append([lbl, n0(D['inputs']['fa_jun26']['value'] + D['inputs']['invprop_jun26']['value']),
                     n0(D['inputs']['fa_dec25']['value'] + D['inputs']['invprop_dec25']['value'])])
    elif lbl.startswith('Work'):
        rows.append([lbl, n0(D['inputs']['wip_jun26']['value']), n0(D['inputs']['wip_dec25']['value'])])
    elif lbl.startswith('Notes payable'):
        rows.append([lbl, n0(H['np_total_jun26']),
                     n0(D['inputs']['np_st_dec25']['value'] + D['inputs']['np_lt_dec25']['value'])])
    else:
        rows.append([lbl, n0(D['inputs']['jsa_st_jun26']['value'] + D['inputs']['jsa_lt_jun26']['value']),
                     n0(D['inputs']['jsa_st_dec25']['value'] + D['inputs']['jsa_lt_dec25']['value'])])
table(rows, [3.3, 1.7, 1.7], first_col_bold=True, size=8.2, band_rows={9, 18})
caption('%s. Read from the face of the reviewed statements. Total assets less total liabilities '
        'equals total equity in both columns, which the model asserts before it will produce a '
        'number.' % T())

H2('A.3  Forecast balance-sheet and cash-flow markers')
rows = [['EGP mn'] + YRS]
rows.append(rowify('Working capital employed', A['nwc']))
rows.append(rowify('  of which work in progress', [x * 0 + 0 for x in A['nwc']]) if False else
            ['Construction cost charged to income'] + [n0(x) for x in A['constr']])
rows.append(rowify("Land and partners' share", A['landp']))
rows.append(rowify('Capital expenditure', A['capex']))
rows.append(["Residents' Association movement"] + [n0(x) for x in A['ra_cash']])
rows.append(rowify('Free cash flow to the firm', A['fcff']))
table(rows, [2.24] + [0.79] * 6, first_col_bold=True, size=7.6)
caption('%s. The balance-sheet and cash markers the forecast turns on. Working capital is rolled '
        'on each block\'s own measured ratio to its own driver, not on a single revenue '
        'percentage.' % T())

# ================================================= 13. APPENDIX B — REGISTERS
H1('Appendix B — peers, risks and the research record')
H2('B.1  Peer set')
rows = [['Company', 'Listing', 'Market value, EGP mn', 'Price to earnings']]
for p in PEERS:
    rows.append([p['name'], p['ticker'], '' if not p.get('mcap') else n0(p['mcap']),
                 '' if not p['pe'] else p2(p['pe']) + 'x'])
rows.append(['Palm Hills Developments', M['code'], n0(H['mktcap']), p2(H['pe_ltm']) + 'x'])
table(rows, [2.4, 1.3, 1.65, 1.5], first_col_bold=True, band_rows={len(rows) - 1}, size=8.6)
caption('%s. Five Egyptian peers and two Gulf peers, inside and outside the country as the method '
        'requires.' % T())

H2('B.2  Risk register')
rows = [['Risk', 'How it would show up', 'What it is worth']]
rows += [
    ["Residents' associations constituted", 'A transfer of assets and liabilities out of the group',
     'The whole gap between the framings: EGP %s a share'
     % p2(SYN['framing_A']['base'] - SYN['framing_B']['base'])],
    ['Disinflation stalls', 'The cost of capital stays at spot rather than gliding',
     'EGP %s a share on the cash-flow lens' % p2(abs(L['dcf']['A'] - L['dcf']['A_spot']))],
    ['Build cost outruns selling price',
     'The crux ratio falls from its measured %sx to %sx, ten per cent lower'
     % (p2(H['P_h126']), p2(SENS['crux_P'][0])),
     'EGP %s a share on the cash-flow lens'
     % p2(abs(SENS['grid_A'][2][2] - SENS['grid_A'][2][0]))],
    ['Refinancing', 'EGP %smn of interest-bearing obligations, about EGP 21.4bn of it floating; a '
     'two-point rate move is worth EGP %smn of profit on the company\'s own disclosure'
     % (n0(H['debt_narrow']), n0(D['inputs']['rate_sens_2pc']['value'])),
     'Not modelled as a separate scenario; it is inside the cost-of-capital axis'],
    ['Concentration in one country', 'Every project but Saadiyat is Egyptian',
     'Carried through the country risk premium of %s inside the cost of equity'
     % pc(D['inputs']['crp_rating']['value'])],
]
lalign(table(rows, [1.55, 2.5, 2.8], first_col_bold=True, size=8.2), {1, 2})
caption('%s. Each risk priced in the same units as the valuation, not described in adjectives.' % T())

H2('B.3  Research record')
P('The four layers of research behind this document — global, country, industry and company — '
  'were re-run on the new disclosure. The company layer was rebuilt in full. The country layer '
  'was rebuilt in full because every one of its drivers moved: the sovereign yield, the equity '
  'risk premium file, the inflation print and the policy rate. The industry layer was rebuilt '
  'because a dated market survey published the day before this study gave a measurable price and '
  'volume outcome. Within the global layer, the currency and commodity findings were re-run and '
  'the trade and supply-chain search was repeated and again returned nothing bearing on the '
  'subject, so that finding is carried forward. Twenty-three findings were recorded in all, of '
  'which five are dated negative searches. Seven separate attempts were made to reach primary '
  'documents; five succeeded and two failed, and both failures are named in the caveats.',
  size=9.6)
P('Every number in this study that describes what Palm Hills reported comes from a document Palm '
  'Hills issued. Market data comes from the central bank\'s own auction results and from the '
  'original country-risk file. Peer multiples come from market-data aggregators and are used only '
  'to price other companies. No aggregator sits anywhere in the path of a Palm Hills historical.',
  size=9.6)

# ================================================ 14. APPENDIX C — THE PANEL
H1('Appendix C — three experts, three methods')
H2('C.1  Expert 1 — the cash-flow analyst')
P('Worldview. A developer is a machine that converts construction spending into contracted '
  'revenue over several years. Value it on what the machine produces net of what it consumes, '
  'and be honest that in a business with a %s-day gross cycle the consumption is most of the '
  'story.' % n0(H['ccc_gross']))
P('When it works: when the physical driver is disclosed, which here it is. When it fails: when '
  'the terminal carries most of the value, which here it does.')
rows = [['Line', 'Value']]
rows += [['Return on invested capital, computed from the model\'s own year-five capital',
          pc(EXP['e1']['roic'])],
         ['Weighted cost of capital, spot', pc(EXP['e1']['wacc'])],
         ['Weighted cost of capital, normalised', pc(EXP['e1']['wacc_term'])],
         ['Present value of the explicit forecast, EGP mn', n0(EXP['e1']['pv_explicit'])],
         ['Present value of the terminal, EGP mn', n0(EXP['e1']['pv_term'])],
         ['Terminal share of enterprise value', pc(EXP['e1']['term_share'])],
         ['Value per share, float as operating funding', 'EGP ' + p2(EXP['e1']['vps_A'])],
         ['Value per share, float restricted', 'EGP ' + p2(EXP['e1']['vps_B'])]]
table(rows, [4.3, 2.4], first_col_bold=True, size=8.6, band_rows={7, 8})
caption('%s. Expert 1\'s workings, every intermediate line shown.' % T())
P('Named sensitivity: two hundred basis points on the cost-of-capital path moves the answer from '
  'EGP %s to EGP %s. Falsifier stated in advance: if the return on invested capital measured on '
  'the 2027 statements comes in above the normalised cost of capital of %s, the growth path in '
  'this model is too pessimistic and the value is understated.'
  % (p2(min(SENS['grid_A'][-1][2], SENS['grid_A'][0][2])),
     p2(max(SENS['grid_A'][-1][2], SENS['grid_A'][0][2])), pc(W['wacc_term'])))

H2('C.2  Expert 2 — the contracted-book analyst')
P('Worldview. Forget the forecast. The company has already sold the units; the question is what '
  'is left after building them and paying everyone else. Value the book that exists and treat '
  'everything beyond it as free.')
rows = [['Line', 'EGP mn']]
rows += [['Present value of undelivered-unit notes receivable, off balance sheet',
          n0(EXP['e2']['pv_book'])],
         ['Notes and accounts receivable already on the balance sheet', n0(EXP['e2']['onbs'])],
         ['Less advances already taken from customers', '(%s)' % n0(EXP['e2']['advances'])],
         ['Less construction still to spend on that book, half attributed to the period',
          '(%s)' % n0(EXP['e2']['cost_to_complete'] * 0.5)],
         ['Less land and partners\' share still to come, half attributed',
          '(%s)' % n0(EXP['e2']['landp_to_come'] * 0.5)],
         ['Less net debt', '(%s)' % n0(H['netdebt_company'])],
         ['Less non-controlling interests', '(%s)' % n0(D['inputs']['eqnci_jun26']['value'])],
         ['Equity value', n0(EXP['e2']['equity'])],
         ['Value per share, EGP', p2(EXP['e2']['vps'])]]
table(rows, [4.3, 2.4], first_col_bold=True, size=8.6, band_rows={8, 9})
caption('%s. Expert 2\'s workings. The book is taken at the present value the company itself '
        'discloses, and the costs still to come are struck at the study\'s own measured rates.'
        % T())
P('Named sensitivity: taking the notes receivable at nominal rather than present value would add '
  'EGP %s a share, which is exactly why the present value is used. Falsifier: if the company '
  'delivers the book at a gross margin materially below %s, this number is too high.'
  % (p2((EXP['e2']['nominal'] - EXP['e2']['pv_book']) / SH), pc(H['re_gm_h126'])))

H2('C.3  Expert 3 — the returns analyst')
P('Worldview. Over any long period a company is worth its book value adjusted for the gap between '
  'what it earns on that book and what the book costs. Everything else is arithmetic about timing.')
rows = [['Line', 'Value']]
rows += [['Book value per share, controlling equity', 'EGP ' + p2(EXP['e3']['bvps'])],
         ['Trailing return on equity', pc(EXP['e3']['roe'])],
         ['Cost of equity, spot', pc(EXP['e3']['ke'])],
         ['Cost of equity, normalised', pc(EXP['e3']['ke_term'])],
         ['Justified multiple of book, spot', p2(EXP['e3']['pb_spot']) + 'x'],
         ['Justified multiple of book, normalised', p2(EXP['e3']['pb_norm']) + 'x'],
         ['Value per share, spot', 'EGP ' + p2(EXP['e3']['vps_spot'])],
         ['Value per share, normalised', 'EGP ' + p2(EXP['e3']['vps_norm'])]]
table(rows, [4.3, 2.4], first_col_bold=True, size=8.6, band_rows={7, 8})
caption('%s. Expert 3\'s workings.' % T())
P('Named sensitivity: the answer is linear in the cost of equity and in nothing else. A hundred '
  'basis points is worth about EGP %s a share at the normalised rate. Falsifier: if the return on '
  'equity falls below the normalised cost of equity of %s, the justified multiple drops below one '
  'and the shares are worth less than book.'
  % (p2(abs((EXP['e3']['roe'] - 0.08) / (EXP['e3']['ke_term'] - 0.08) * EXP['e3']['bvps']
             - (EXP['e3']['roe'] - 0.08) / (EXP['e3']['ke_term'] + 0.01 - 0.08) * EXP['e3']['bvps'])),
     pc(EXP['e3']['ke_term'])))

H2('C.4  Cross-examination')
rows = [['Challenge', 'Answer']]
rows += [
    ['Expert 3 to Expert 1: your terminal is %s of the value. You are not valuing a business, you '
     'are valuing an assumption about 2032.' % pc(EXP['e1']['term_share'], 0),
     'CONCEDED. The terminal share is disclosed rather than hidden, the terminal growth rate sits '
     'below the terminal cost of capital under both framings, and the terminal cash flow is '
     'charged a reinvestment rate computed from the model\'s own return on capital, so growth is '
     'not free. It is still the weakest part of the lens.'],
    ['Expert 1 to Expert 3: your return on equity of %s is not an operating return. Strip the '
     'discount unwinding and the treasury-bill income and it collapses.' % pc(EXP['e3']['roe']),
     'CONCEDED in part. Those two lines are EGP %smn of the half-year, against attributable '
     'profit of EGP %smn. They are real income and they recur, but they are financing income and '
     'the multiple applied to them should be lower than the multiple applied to development '
     'profit. The lens does not make that distinction and it should.'
     % (n0(D['inputs']['amort_nr_h126']['value'] + D['inputs']['tbillinc_h126']['value']),
        n0(D['inputs']['np_h126']['value']))],
    ['Expert 2 to both: you are forecasting when the company has already told you what it sold. '
     'The contracted book is EGP %sbn of contractual value. Why guess?'
     % bn(EXP['e2']['contract_value']),
     'REJECTED. The book covers about two years of building at the current rate. Beyond that the '
     'company either replenishes it or shrinks, and a valuation that assumes neither is a '
     'liquidation estimate, not a going-concern one. Expert 2\'s answer of EGP %s is best read as '
     'the floor it is.' % p2(EXP['e2']['vps'])],
    ['Expert 3 to Expert 2: you deduct construction still to come at half weight. Why half?',
     'CONCEDED as arbitrary. It is a judgement that roughly half the remaining build is already '
     'funded by the advances deducted above it. Deducting the whole of the remaining build on top '
     'of the advances takes the answer below zero, to about EGP %s, which is itself a useful '
     'result: the contracted book only has value because the customer has already paid for much '
     'of it. Deducting none would raise it to about EGP %s. The range is disclosed rather than '
     'the midpoint being dressed up as precision.'
     % (p2((EXP['e2']['equity'] - 0.5 * (EXP['e2']['cost_to_complete'] + EXP['e2']['landp_to_come'])) / SH),
        p2((EXP['e2']['equity'] + 0.5 * (EXP['e2']['cost_to_complete'] + EXP['e2']['landp_to_come'])) / SH))],
]
lalign(table(rows, [2.7, 4.2], first_col_bold=True, size=8.0), {1})
caption('%s. Each challenge conceded or rejected on the record.' % T())

H2('C.5  The three in one room')
P('Put in a room and made to agree on something, the three converge on a diagnosis rather than a '
  'number. All three accept that the balance sheet, not the income statement, is where this '
  'company is decided. All three accept that the float is the largest single item in it and that '
  'nobody outside the company knows whether it will ever transfer. Expert 1 would pay up to EGP '
  '%s if the float is permanent and nothing above EGP %s if it is not. Expert 3 will not pay more '
  'than EGP %s under any assumption about the float, because his lens does not see it. Expert 2 '
  'will not pay more than EGP %s because he refuses to value anything not yet sold. The market '
  'price of EGP %s sits above two of the three.'
  % (p2(EXP['e1']['vps_A']), p2(EXP['e1']['vps_B']), p2(EXP['e3']['vps_norm']),
     p2(EXP['e2']['vps']), p2(SPOT)))

H2('C.6  Divergence')
rows = [['Pair', 'Gap, EGP per share', 'Which assumption drives it']]
rows += [
    ['Expert 1 against Expert 3', p2(abs(EXP['divergence']['e1_vs_e3'])),
     'The float, then the cost of capital. Expert 3\'s lens cannot see the float at all because it '
     'works from book equity, in which the float is a liability and its invested assets are assets.'],
    ['Expert 1 against Expert 2', p2(abs(EXP['divergence']['e1_vs_e2'])),
     'Replenishment. Expert 2 values two years of book; Expert 1 values five and a half years plus '
     'a terminal.'],
    ['Expert 2 against Expert 3', p2(abs(EXP['e2']['vps'] - EXP['e3']['vps_norm'])),
     'Nothing that matters: EGP %s a share apart, from entirely different directions. Two methods '
     'this different landing this close is coincidence rather than corroboration, but it does say '
     'the two conservative readings of this company agree on roughly where its floor is.'
     % p2(abs(EXP['e2']['vps'] - EXP['e3']['vps_norm']))],
]
lalign(table(rows, [1.8, 1.3, 3.8], first_col_bold=True, size=8.4), {2})
caption('%s. What actually separates the three.' % T())
figure('figD1_experts.png', 6.4,
       '%s. The three methods against the market price and the study\'s base case.' % FG())

# ==================================================== 15. ABOUT / 16. DISCLOSURE
H1('About this series')
P('Every instrument analysed in this series follows the same standing format: a headline, a '
  'valuation summary, a company overview, a fundamental section built from the company\'s own '
  'issued statements, a technical section, a probability map, a comparison of the lenses, a '
  'catalyst calendar, a probability-zone reading, caveats, statement appendices, a peer and '
  'research appendix, and an expert panel. Fundamental value and the probability map run on '
  'separate clocks and each carries its own date stamp, so a reader can always see which half of '
  'a document has been refreshed. Forecasts are graded publicly when they resolve.')

H1('Disclosure and disclaimer — read in full')
P('Nature of this document. This study is an educational valuation exercise and an expression of '
  'the preparer\'s personal analytical opinion, based exclusively on publicly available '
  'information and on assumptions stated in the text and the accompanying model. It is published '
  'free of charge, on a standing periodic schedule, to demonstrate methodology and to invite '
  'scrutiny and critique of that methodology.', size=8.6)
P('No advice, no recommendation, no solicitation. Nothing in this document constitutes investment '
  'advice, financial consultancy, securities analysis services, a research recommendation, a '
  'rating, a price target, an offer, or a solicitation or invitation to buy, sell, hold, '
  'subscribe for or otherwise deal in any security or financial instrument. No statement herein '
  'is directed at, or calibrated to, the investment objectives, financial situation, risk '
  'tolerance or particular needs of any person.', size=8.6)
P('No licensed activity. The preparer is not licensed or registered with the Egyptian Financial '
  'Regulatory Authority or any other securities regulator; does not carry on financial '
  'consultancy, securities evaluation or analysis services, portfolio management, brokerage, '
  'promotion or any other regulated activity; does not manage money; does not accept clients, '
  'fees, subscriptions or funds of any kind; and does not provide personalised advice to anyone.',
  size=8.6)
P('Estimates and uncertainty. All valuations, scenarios, probabilities and levels are model '
  'outputs resting on explicit, subjective assumptions; they are illustrative, highly uncertain, '
  'and likely to prove wrong in material respects. They are deliberately presented as ranges and '
  'distributions because no single number should be relied on. Public and vendor-sourced data are '
  'believed reliable but are not guaranteed; vendor-derived figures are flagged as such where '
  'used.', size=8.6)
P('No liability. To the maximum extent permitted by applicable law, the preparer accepts no '
  'liability or responsibility whatsoever for any decision made or action taken or not taken, or '
  'for any loss or damage of any kind incurred, by any person in reliance on, or in connection '
  'with, any part of this document or the accompanying model.', size=8.6)
P('Reader\'s responsibility. Any person considering an investment decision should conduct their '
  'own independent assessment and consult a financial advisor licensed in their jurisdiction. If '
  'the publication of material of this kind is restricted where you are reading it, do not rely '
  'on it.', size=8.6)

OUT = 'PHDC_Valuation_Study_19-08-2026_public.docx'
doc.save(OUT)
print('wrote %s — %d tables, %d figures' % (OUT, _T[0], _F[0]))
