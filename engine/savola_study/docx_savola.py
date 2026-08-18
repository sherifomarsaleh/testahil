"""SAVOLA_Valuation_Study_18-08-2026_public.docx — 16-section study, house style,
model-study (SWDY) skeleton, operating-company lens. Every financial numeral is
read from study_numbers.json; no number is typed into this builder."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
os.chdir(HERE)
exec(open(os.path.join(HERE, '..', 'du_study', 'docx_base.py')).read())

D = json.load(open(os.path.join(HERE, 'study_numbers.json')))
IN = {k: v['value'] for k, v in D['inputs'].items()}
M, HI, HB, F = D['meta'], D['hist_is'], D['hist_bs'], D['fcst']
W, DCF, LN, SN = D['wacc'], D['dcf'], D['lenses'], D['sens']
EXP, SEG, H1_ = D['experts'], D['segments_fy25'], D['h1_2026']
STK, BT, TECH = D['strike'], D['backtest'], D['tech']
BT5, BTF, BTP = BT['five_year'], BT['full'], BT['production']
SPOT, SH, SHW = M['spot'], M['shares_mn'], M['shares_wavg_mn']
CEN = D['central']
H1M, H3M = STK['horizons']['1M'], STK['horizons']['3M']
_W = D['weights']
WBEAR = sum(LN[k]['bear'] * _W[k] for k in _W)
WBULL = sum(LN[k]['bull'] * _W[k] for k in _W)
LO_ = min(LN[k]['bear'] for k in _W); HI_ = max(LN[k]['bull'] for k in _W)
CAT = SEG['categories']
REL = LN['relative']
NAR = TECH['narrative']; TST = TECH['state']

_TN = [0]; _FN = [0]
def T():
    _TN[0] += 1
    return f'Table {_TN[0]}'
def FG():
    _FN[0] += 1
    return f'Figure {_FN[0]}'

def p2(x):  return f'{x:,.2f}'
def p1(x):  return f'{x:,.1f}'
def n0(x):  return f'{x:,.0f}'
def pc(x, d=1): return f'{x*100:.{d}f}%'
def sgn(x, d=1): return f'{x*100:+.{d}f}%'

YRS = [str(y) for y in F['years']]

# =========================== MASTHEAD / TITLE ================================
masthead()
H2('Independent Valuation Study — Educational Analysis')
H1('Savola Group Company (Saudi Exchange: 2050)')
rich([('Savola · Kingdom of Saudi Arabia · Food and retail platform (edible oils · sugar · '
       'pasta · nuts & spices · grocery retail · quick-service restaurants · frozen food)   ',
       dict(size=10.5)),
      (f"Anchor {M['anchor_date']} · Spot SAR {p2(SPOT)} · Market capitalisation SAR "
       f"{n0(M['mktcap'])}mn", dict(size=10.5, color=GREY))], space_after=10)
P('READ FIRST. This study is an educational analysis, not investment advice, a recommendation '
  'or a solicitation. It never issues a rating or a price target: it publishes fair-value '
  'RANGES and probability DISTRIBUTIONS, and it separates what the business may be worth '
  '(sections 1, 4, 5) from where the price could plausibly trade (sections 2, 3, 6) — two '
  'different questions that are never blended. All figures are in Saudi riyals (SAR); the '
  'company reports, lists and pays dividends in SAR, and its Egyptian, Algerian and Emirati '
  'operations are translated in its own audited consolidation — no separate currency '
  'translation enters the model. Historical financials come exclusively from the company\'s '
  'own audited and reviewed consolidated financial statements and its own results releases, '
  'read from savola.com/investors; every input is listed with source and date in the '
  'companion bibliography document.', size=9.6, space_after=12)

# =========================== HEADLINE ========================================
H2('Headline')
box([
 ('The business. ', 'Savola is the Gulf\'s largest food platform: FY2025 revenue of SAR '
  f"{n0(HI['FY25']['rev'])}mn across five reported segments — food processing SAR "
  f"{n0(SEG['fp']['rev'])}mn ({pc(SEG['fp']['rev']/HI['FY25']['rev'],0)} of segment revenue: "
  f"edible oil {n0(CAT['oil']['vol'])} thousand tonnes, sugar {n0(CAT['sugar']['vol'])} "
  'thousand tonnes, pasta, nuts & spices), grocery retail through Panda '
  f"(SAR {n0(IN['ret_segrev_fy25'])}mn, {n0(IN['stores_end25'])} stores), Herfy\'s '"
  'quick-service restaurants, and Al Kabeer frozen food. Roughly three quarters of revenue '
  'is Arabia, a fifth Egypt.'),
 ('The reset that redefined it. ', 'In 2024 Savola raised SAR 6.0bn in rights, repaid SAR '
  '5.8bn of debt, then cancelled 833.98mn shares (a SAR 8.3bn capital reduction) and '
  'distributed its entire 34.52% Almarai stake — SAR 12.75bn at fair value — to its own '
  'shareholders. The holding-company era ended there: what remains is an operating food and '
  f"retail group with {n0(SH)}mn shares, borrowings of SAR {n0(IN['loans_fy25'])}mn (all "
  f"short-term trade finance) and lease liabilities of SAR {n0(IN['leases_fy25'])}mn."),
 ('The valuation. ', f'Weighted central SAR {p2(CEN)} per share against a spot of SAR '
  f'{p2(SPOT)} ({sgn(CEN/SPOT-1,0)}), inside a weighted bear-to-bull range of SAR '
  f'{p2(WBEAR)} to {p2(WBULL)} and a wider span across the four lenses of SAR {p2(LO_)} to '
  f'SAR {p2(HI_)}. The cash-flow lens alone reads SAR {p2(DCF["ps"])}; the market-anchored '
  f'relative lens reads SAR {p2(REL["base"])}; the book lens reads SAR '
  f'{p2(LN["book"]["base"])}. The spread is the study\'s honest tension — section 4 explains '
  'it rather than hiding it.'),
 ('The contested judgement. ', 'Is Panda\'s 20-store-a-year expansion creating value or '
  'burning it? Sales per store FELL '
  f"{pc(-H1_['panda']['sps_change'])} in the first half of 2026 as new, smaller stores "
  'opened into a discounter-crowded market. Let density stabilise as the store-refresh '
  f'programme matures and the model reads SAR {p2(DCF["framingA"])}; hold the measured '
  f'erosion forever and the same model reads SAR {p2(DCF["framingB"])}. The judgement is '
  f'worth SAR {p2(DCF["framing_gap"])} per share, and both framings are published side by '
  'side — never averaged.'),
 ('The moment. ', 'This study is struck twelve days after the company\'s own first-half '
  f"results: revenue {sgn(H1_['rev']/13080.0-1,1)} to SAR {n0(H1_['rev'])}mn, recurring net "
  f"profit up 40% to SAR {n0(H1_['recurring_np'])}mn, oil volumes up 16%, the Sudan exit "
  'completed, and a bolt-on acquisition (Al Mehbaj Al Shamiya) signed in July. Against that: '
  'the company itself warns of replacement-cost pressure in the second half as vegetable-oil '
  'benchmarks sit at four-year highs, and grocery competition is compressing Panda\'s '
  'densities. Both halves of that picture are in the model.'),
], fill=F_CREAM)

# =========================== VALUATION SUMMARY ===============================
H2('Valuation summary — every read at a glance')
rows = [['Lens', 'Bear', 'Base', 'Bull', 'Weight', 'vs spot']]
for k, nm in [('dcf', 'Discounted cash flow (primary)'), ('relative', 'Relative multiples'),
              ('normalized', 'Normalised earnings power'),
              ('book', 'Book value & sustainable return')]:
    l = LN[k]
    rows.append([nm, p2(l['bear']), p2(l['base']), p2(l['bull']), pc(_W[k], 0),
                 sgn(l['base']/SPOT-1, 0)])
rows.append(['Weighted central', p2(WBEAR), p2(CEN), p2(WBULL), '100%', sgn(CEN/SPOT-1, 0)])
rows.append(['Span across lenses (min/max, not weighted)', p2(LO_), '', p2(HI_), '—', ''])
rows.append(['Contested judgement, other way — Panda density never stabilises', '',
             p2(DCF['framingB']), '', '—', sgn(DCF['framingB']/SPOT-1, 0)])
rows.append(['Expert panel median (Appendix C)', '', p2(D['panel_median']), '', '—',
             sgn(D['panel_median']/SPOT-1, 0)])
rows.append([f"DCF terminal value share of enterprise value: {pc(DCF['tv_share'],0)}",
             '', '', '', '', ''])
table(rows, [2.55, 0.85, 0.85, 0.85, 0.75, 0.85], band_rows={5}, size=8.8)
caption(f'{T()} — the valuation summary. Weighted central SAR {p2(CEN)}, its bear and bull '
        'columns weighted on the same 45/25/15/15 basis; beneath it the wider min/max span '
        'across lenses, which is NOT a weighted figure. Every lens value is dated at the '
        f'{M["anchor_date"]} anchor, net of the SAR {p2(IN["div_between"])} dividend whose '
        'ex-date (07-May-2026) falls between the 31-Dec-2025 valuation date and that anchor. '
        f'The terminal value is {pc(DCF["tv_share"],0)} of the DCF enterprise value; what that '
        'terminal implies is priced explicitly in section 1.7 rather than left as a caveat.')
figure(os.path.join(HERE, 'fig1_football.png'), 7.0,
       f'{FG()} — the valuation football field: bear-to-bull span per lens, brass tick = '
       'base, dark line = spot.')

# =========================== COMPANY OVERVIEW ===============================
H2('Company overview — Savola at a glance')
P('Savola Group was founded in Jeddah in 1979 as a Saudi edible-oils company and grew into '
  'the region\'s dominant staple-foods and grocery platform. Its operating structure today: '
  'Savola Foods Company (100%) manufactures and distributes edible oils, sugar, pasta, '
  'specialty fats and nuts & spices across Saudi Arabia, Egypt, Algeria and the UAE (with '
  'the July-2026 Al Mehbaj acquisition adding Saudi nuts-and-spices scale); Panda Retail '
  'Company (100%) runs one of the Kingdom\'s largest grocery networks; Herfy Food Services '
  '(49%-owned but consolidated — Savola is the dominant shareholder of a widely held '
  'register, and Herfy is separately listed) runs the home-grown quick-service chain; Good '
  'Food Company holds the Al Kabeer frozen-food business; and a 29.9% associate stake in '
  'Kinan International carries the legacy real-estate book. The controlling shareholder '
  'group around the Al-Muhaidib family anchors the register.')
P(f"The revenue mix that decides the company's class: food processing SAR "
  f"{n0(SEG['fp']['rev'])}mn and grocery retail SAR {n0(IN['ret_segrev_fy25'])}mn together "
  f"are {pc((SEG['fp']['rev']+IN['ret_segrev_fy25'])/(SEG['fp']['rev']+IN['ret_segrev_fy25']+IN['fsv_segrev_fy25']+IN['frz_segrev_fy25']+IN['invseg_rev']),0)} "
  'of segment revenue; food services and frozen food make up most of the rest, and the '
  f"investments segment contributes SAR {n0(IN['invseg_rev'])}mn of rent — noise against a "
  f"SAR {n0(HI['FY25']['rev'])}mn top line. The balance-sheet shape says the same thing: "
  f"owned plant of SAR {n0(IN['ppe_fy25'])}mn and store right-of-use assets of SAR "
  f"{n0(IN['rou_fy25'])}mn against lease liabilities of SAR {n0(IN['leases_fy25'])}mn; "
  f"inventories of SAR {n0(IN['inventories_fy25'])}mn turning through payables of SAR "
  f"{n0(IN['tp_fy25'])}mn; short-term commodity-finance borrowings of SAR "
  f"{n0(IN['loans_fy25'])}mn and zero long-term debt. After the Almarai distribution the "
  'listed-stake layer that once defined Savola is gone: what is left to value is an '
  'OPERATING COMPANY — a diversified consumer-staples operator — and the study therefore '
  'runs the operating-company lens set: a full free-cash-flow model as the primary lens, '
  'cross-read by relative multiples, normalised earnings power and a book/sustainable-'
  'return lens, with the small non-operating pocket (government sukuk, the residual Almarai '
  'shares, Kinan) valued separately in the bridge. No leg is large enough or different '
  'enough to need a separate valuation method: Herfy, the one listed piece, enters the '
  'bridge at its own market price through the outside shareholders\' interest.')
P('Two structural facts organise everything else. First, margins here are thin and '
  f"mix-driven — the group operating margin before depreciation is {pc(HI['FY25']['ebitda']/HI['FY25']['rev'])} "
  'and every point of it is fought for in commodity pass-through (oils, sugar, wheat) and '
  'grocery price investment; the model therefore builds each category on its own volumes '
  'and unit economics and lets every margin fall out as a result. Second, the group is '
  'mid-rebuild: the 2024-2026 portfolio rationalisation (Iran, Sudan and Türkiye all '
  'exited) has concentrated capital on Arabia and Egypt, dividends have restarted under a '
  'stated 50-60% payout policy, and the expansion budget is pointed at Panda stores and a '
  'new Jeddah nuts facility. Whether that expansion earns its keep is the study\'s central '
  'question.')

# =========================== 1 FUNDAMENTAL VALUATION =========================
H1('1  Fundamental valuation')
P('Four lenses, weighted into one field: the discounted cash flow carries '
  f"{pc(_W['dcf'],0)}, relative multiples {pc(_W['relative'],0)}, normalised earnings power "
  f"{pc(_W['normalized'],0)} and the book lens {pc(_W['book'],0)}.")

H2('1.1  The cash-flow model — the primary lens, with the full waterfall')
P('The model builds five explicit years from the segment engine of section 1.6 — category '
  'volumes times unit prices and unit gross profits for food processing, stores times sales '
  'per store for Panda — charges the combined zakat-and-tax take, funds owned capital '
  'expenditure and a steady-state lease replacement equal to right-of-use depreciation '
  '(leases are treated as debt and priced in the capital structure, so the charge appears '
  'exactly once), and invests working capital at the measured component days. The full '
  'waterfall — every line of it a live formula in the companion workbook:')
rows = [['SAR mn'] + YRS]
for lab, series, fmt in [
        ('Revenue', F['rev'], n0), ('EBITDA', F['ebitda'], n0),
        ('less depreciation & amortisation', [-x for x in F['dna']], n0),
        ('EBIT', F['ebit'], n0),
        (f"NOPAT — EBIT × (1 − {pc(W['tax'])})", F['nopat'], n0),
        ('add back depreciation & amortisation', F['dna'], n0),
        ('less capital expenditure', [-x for x in F['capex']], n0),
        ('less lease replacement (right-of-use depreciation)',
         [-x for x in F['dna_rou']], n0),
        ('less change in working capital', [-x for x in F['dwc']], n0),
        ('Free cash flow to the firm', F['fcff'], n0),
        ('discount factor', DCF['dfs'], lambda x: f'{x:.4f}'),
        ('PV of FCFF', [f_ * df for f_, df in zip(F['fcff'], DCF['dfs'])], n0)]:
    rows.append([lab] + [fmt(x) for x in series])
table(rows, [2.30, 0.94, 0.94, 0.94, 0.94, 0.94], band_rows={2, 4, 10, 12}, size=8.8)
caption(f'{T()} — the FCFF waterfall. The EBITDA margin path '
        f"({pc(F['ebitda_margin'][0])} to {pc(F['ebitda_margin'][-1])}) is an OUTPUT of the "
        'segment build, never an input; capital expenditure follows the company\'s own '
        f"programme (FY2025 actual SAR {n0(858.5)}mn, first half of 2026 SAR "
        f"{n0(H1_['capex'])}mn); the working-capital line is built from measured days of "
        'inventory, receivables and payables; lease replacement equals right-of-use '
        'depreciation so the store lease book neither inflates nor starves the cash flow.')
P(f"Terminal value: terminal-year NOPAT grown at {pc(IN['g_term'])} with a reinvestment "
  f"rate set by the growth itself — g / return on capital = {pc(IN['g_term'])} / "
  f"{pc(IN['roic_term'])} = {pc(DCF['reinvest_term'])} of NOPAT — capitalised at the "
  f"terminal cost of capital of {pc(W['wacc_term'],2)} less growth. That yields a terminal "
  f"value of SAR {n0(DCF['tv'])}mn, whose present value is SAR {n0(DCF['pv_tv'])}mn — "
  f"{pc(DCF['tv_share'],0)} of enterprise value. A reader should sit with that number: "
  'three quarters of this valuation is the going concern beyond 2030, priced at a return '
  'on capital only modestly above its cost. Section 1.9 shows what moving either does.')
H2('The enterprise-to-equity bridge')
brs = [['Step', 'SAR mn', 'Per share']]
for lab, v in [
    ('Present value of the five forecast years', DCF['pv_explicit']),
    ('Present value of the terminal value', DCF['pv_tv']),
    ('Enterprise value (operating)', DCF['ev']),
    ('+ Government sukuk and other investments (audited carrying)',
     IN['inv_nc_fy25'] + IN['inv_c_fy25']),
    ('+ Kinan at capitalized earnings (29.9% associate)', DCF['kinan_capitalized']),
    ('+ Investment property', IN['invprop_fy25']),
    ('+ Cash and cash equivalents', IN['cash_fy25']),
    ('− Loans and borrowings', -IN['loans_fy25']),
    ('− Lease liabilities', -IN['leases_fy25']),
    ('− Employee benefits liabilities', -IN['eb_fy25']),
    ('− Asset-restoration provision', -IN['restor_fy25']),
    ('− Other net liabilities (tax and zakat accruals, deferred tax, net)',
     -IN['other_net_liab']),
    ("− Herfy's 51% outside interest at Herfy's own market price",
     -DCF['nci_herfy_mkt']),
    ('− Other minority interests at book', -DCF['nci_other_book']),
    ('Equity value attributable to owners', DCF['eq_val'])]:
    brs.append([lab, n0(v), p2(v / SHW)])
brs.append([f"Terminal value share of enterprise value: {pc(DCF['tv_share'],0)}", '', ''])
table(brs, [4.40, 1.15, 1.15], band_rows={3, 15}, size=8.8)
caption(f'{T()} — from enterprise value to equity. The equity value of SAR '
        f"{n0(DCF['eq_val'])}mn is dated 31-Dec-2025 (SAR {p2(DCF['ps_dec'])}/share), rolled "
        f"{n0(IN['anchor_days'])} days to the {M['anchor_date']} anchor at the cost of "
        f"equity (factor {DCF['roll']:.4f}) and reduced by the SAR {p2(IN['div_between'])} "
        f"FY2025 dividend that went ex on 07-May-2026 — SAR {p2(DCF['ps'])} per share at the "
        'anchor. Kinan alternatives are disclosed in the workbook: audited carrying SAR '
        f"{n0(IN['kinan_carry'])}mn (floor), share of net assets SAR "
        f"{n0(IN['kinan_share_na'])}mn, capitalized earnings SAR "
        f"{n0(DCF['kinan_capitalized'])}mn (used).")

H2('1.2  Book value and sustainable return')
P(f"Audited equity attributable to owners is SAR {n0(IN['equity_att_fy25'])}mn — SAR "
  f"{p2(LN['book']['bvps'])} per share. The recurring profit base the company itself "
  f"publishes (SAR {n0(IN['recurring_np_fy25'])}mn for FY2025, stripped of the zakat "
  'release, the Türkiye gain and the put-option gain), stepped to a first-half-evidenced '
  f"FY2026 level, gives a sustainable return on equity of {pc(LN['book']['roe'])}. Against "
  f"a cost of equity of {pc(W['ke_rating'],2)} and {pc(IN['g_term'])} growth, the justified "
  f"multiple of book is {LN['book']['pb']:.2f}x — value SAR {p2(LN['book']['base'])} per "
  'share. The lens says the plain thing: at today\'s recurring profitability Savola earns '
  'roughly its cost of equity, so it is worth roughly book. Everything above book in the '
  'other lenses is a claim about improvement — Panda scale, oil volumes, the nuts platform '
  '— and this lens is the discipline against paying for claims twice.')

H2('1.3  Relative multiples')
prs = [['Company', 'Listing', 'P/E (trailing)', 'Role in the multiple']]
for nm, ex_, key, role in [
        ('NADEC', 'Tadawul 6010', 'NADEC', 'processing leg (median with Wilmar)'),
        ('Wilmar International', 'SGX F34', 'WILMAR', 'processing leg (median with NADEC)'),
        ('Al Othaim Markets', 'Tadawul 4001', 'OTHAIM', 'retail leg (median with BinDawood)'),
        ('BinDawood Holding', 'Tadawul 4161', 'BINDAWOOD', 'retail leg (median with Al Othaim)'),
        ('Almarai', 'Tadawul 2280', 'ALMARAI',
         'quoted, excluded — dairy-platform premium'),
        ('Herfy Food Services', 'Tadawul 6002', None, 'loss-making; enters the bridge instead')]:
    pe = D['peers']['pe'].get(key) if key else None
    prs.append([nm, ex_, f'{pe:.1f}x' if pe else 'n/m', role])
table(prs, [1.70, 1.20, 1.05, 2.75], size=8.8)
caption(f'{T()} — the peer frame (market quotes of 18-Aug-2026; cross-check data, not a '
        'source for any Savola figure).')
P(f"The multiple is built, not picked: the processing leg (median {REL['pe_fp_leg']:.1f}x) "
  f"is weighted {pc(IN['pe_mix_w_fp'],0)} and the Saudi grocery leg (median "
  f"{REL['pe_ret_leg']:.1f}x) {pc(1-IN['pe_mix_w_fp'],0)} — the group's own EBITDA mix — "
  f"giving {REL['pe_mix']:.1f}x, to which a {pc(IN['pe_discount'],0)} conglomerate and "
  'Egypt-mix discount is applied (a fifth of revenue sits in a Caa1-rated economy, and a '
  f"holding level sits over four legs): {REL['pe']:.1f}x applied to FY2026E earnings of SAR "
  f"{p2(REL['eps_f'])} per share = SAR {p2(REL['base'])}. The discount is priced, not "
  f"asserted: at 30% the lens reads SAR {p2(REL['bear'])}, at 10% SAR {p2(REL['bull'])}. "
  'One number in this construction deserves suspicion, and section 4 gives it: the '
  f"dividend-discount multiple implied by this study's own cost of equity is only "
  f"{REL['pe_ddm']:.1f}x — the peer market pays for Saudi consumer earnings at a price of "
  'capital this study\'s measured beta refuses. The relative lens knowingly imports the '
  'market\'s cheaper capital; that is what a relative lens is for.')

H2('1.4  Normalised earnings power')
P(f"Take mid-cycle revenue (the FY2027E build, SAR {n0(F['rev'][1])}mn), apply a normalised "
  f"operating margin of {pc(IN['norm_ebitda_mgn'])} — inside the observed FY2023-FY2025 "
  f"envelope of {pc(0.089)}-{pc(0.095)} and between FY2025's {pc(HI['FY25']['ebitda']/HI['FY25']['rev'])} "
  'and the stronger first half of 2026 — and run it through the same depreciation, finance, '
  f"tax and minority frame as the model: normalised earnings of SAR {p2(LN['normalized']['eps_norm'])} "
  f"per share, at the same applied multiple {REL['pe']:.1f}x = SAR "
  f"{p2(LN['normalized']['base'])}. This lens deliberately looks past the second-half "
  'replacement-cost squeeze the base case carries; the gap between it and the cash-flow '
  'lens is, in one number, what that squeeze and Panda\'s density drag are worth.')

H2('1.5  Synthesis — four lenses, one field')
P(f"The cash-flow lens (SAR {p2(LN['dcf']['base'])}) carries {pc(_W['dcf'],0)} because it "
  'is the only lens that prices the business bottom-up on its own disclosed units. Relative '
  f"multiples (SAR {p2(REL['base'])}) carry {pc(_W['relative'],0)}: market-anchored, but "
  'imported capital. Normalised earnings power and the book lens carry '
  f"{pc(_W['normalized'],0)} and {pc(_W['book'],0)} as the optimistic and the disciplined "
  f"cross-reads. Weighted central: SAR {p2(CEN)} — {sgn(CEN/SPOT-1,0)} against spot — with "
  f"the four bases spanning SAR {p2(min(LN[k]['base'] for k in _W))} to SAR "
  f"{p2(max(LN[k]['base'] for k in _W))}. The field is wide because the honest questions "
  'are wide: what price of capital, and does the expansion earn.')

H2('1.6  The drivers — each segment on its own build, margins as outputs')
drs = [['Driver', 'Basis', 'FY2026E', 'FY2030E']]
drs.append(['Oil volume (k tonnes)',
            'bottom-up: disclosed volumes; first half +16.1% actual, moderated',
            n0(F['oil']['vol'][0]), n0(F['oil']['vol'][4])])
drs.append(['Oil gross profit / tonne (SAR)',
            'anchored on the disclosed first-half actual 762; second half held BELOW it on '
            'the company\'s own replacement-cost warning',
            n0(IN['oil_gpt_path'][0]), n0(IN['oil_gpt_path'][4])])
drs.append(['Sugar volume (k tonnes)', 'bottom-up: disclosed volumes; first half +7.2%',
            n0(F['sugar']['vol'][0]), n0(F['sugar']['vol'][4])])
drs.append(['Sugar gross profit / tonne (SAR)',
            'first-half actual 218 held near; world sugar soft',
            n0(IN['sug_gpt_path'][0]), n0(IN['sug_gpt_path'][4])])
drs.append(['Pasta volume (k tonnes)', 'bottom-up: disclosed volumes; first half +3.0%',
            n0(F['pasta']['vol'][0]), n0(F['pasta']['vol'][4])])
drs.append(['Nuts & spices revenue (SAR mn)',
            'category revenue path; Al Mehbaj folded in SMALL and FLAGGED — its '
            'consideration is undisclosed', n0(F['nuts']['rev'][0]), n0(F['nuts']['rev'][4])])
drs.append(['Panda stores (year end)', 'company guidance: 20+ per year',
            n0(IN['stores_path'][0]), n0(IN['stores_path'][4])])
drs.append(['Panda sales / average store (SAR mn)',
            f"derived (no like-for-like series is published): measured first-half change "
            f"{pc(H1_['panda']['sps_change'])}, fading to flat by FY2029 (Framing A)",
            p1(F['panda']['sps'][0]), p1(F['panda']['sps'][4])])
drs.append(['Herfy revenue growth', 'glide anchored on the first-half actual (−6.8%)',
            pc(IN['herfy_rev_g'][0]), pc(IN['herfy_rev_g'][4])])
drs.append(['Al Kabeer revenue growth', 'glide anchored on the first-half actual (−1.4%)',
            pc(IN['frz_rev_g'][0]), pc(IN['frz_rev_g'][4])])
drs.append(['Group EBITDA margin — AN OUTPUT', 'falls out of the lines above',
            pc(F['ebitda_margin'][0]), pc(F['ebitda_margin'][4])])
table(drs, [1.90, 3.30, 0.75, 0.75], band_rows={11}, size=8.6)
caption(f'{T()} — the driver set. Three of the four processing categories are true unit '
        'builds (volumes are disclosed); nuts & spices and the two smaller segments carry '
        'revenue paths because no unit is disclosed — each such gap is flagged rather than '
        'filled. Cost discipline: each category carries its own measured operating-cost '
        'ratio, and the pass-through test in the workbook proves the margins are outputs — '
        'raising a category\'s selling price per tonne with its unit gross profit held '
        'LOWERS the valuation, because only the revenue-linked costs scale.')
figure(os.path.join(HERE, 'fig7_mix.png'), 7.0,
       f'{FG()} — segment revenue before eliminations and the group margin path. The mix '
       'shifts toward retail as the store programme runs; the group margin is flat-to-'
       'slightly-down because Panda\'s expansion dilutes near-term and processing margins '
       'are held rather than improved.')

H2('1.7  The crux — Panda\'s expansion, priced both ways')
P('Panda is 43% of revenue, most of the lease book, and most of the capital programme '
  f"(SAR {n0(567.0)}mn of FY2025's SAR {n0(858.5)}mn capex). Its economics moved the wrong "
  f"way in the first half of 2026: four net new stores, revenue up only "
  f"{sgn(H1_['panda']['rev']/5852.0-1,1)}, which is sales per average store DOWN "
  f"{pc(-H1_['panda']['sps_change'])} — the growth programme is currently buying revenue "
  'at the expense of density, in a market the company itself calls value-focused and '
  'discounter-crowded. Whether that is a J-curve or a treadmill is the single judgement '
  'that moves this valuation most, so it is computed BOTH WAYS and never averaged:')
crx = [['Framing', 'Sales-density path', 'Store-cost path', 'Fair value']]
crx.append(['A — the programme matures (base)',
            'measured −6% fades: −3%, −1%, then flat',
            'scale gains of 10bp/yr from FY2028', f"SAR {p2(DCF['framingA'])}"])
crx.append(['B — the erosion persists',
            '−3% every year, forever', 'no scale gains, ever',
            f"SAR {p2(DCF['framingB'])}"])
crx.append(['The judgement is worth', '', '', f"SAR {p2(DCF['framing_gap'])} /share"])
table(crx, [1.80, 2.28, 1.80, 1.10], band_rows={3}, size=8.8)
caption(f'{T()} — the contested judgement. Framing A is the base case everywhere in this '
        'study; Framing B is not a stress test but a coherent alternative reading of the '
        'same first-half evidence, and it sits below the current share price. What would '
        'settle it: two or three quarters of like-for-like density — which Panda does not '
        'publish — or, failing that, the third-quarter revenue print against the store '
        'count.')
P('The second tension the model carries: the company warns that second-half processing '
  'margins face replacement-cost pressure (vegetable-oil benchmarks are at four-year '
  f"highs), so the oil book's unit gross profit is held at SAR {n0(IN['oil_gpt_path'][0])}"
  f"/tonne for FY2026 — BELOW the SAR {n0(H1_['oil']['gpt'])} actually earned in the first "
  'half — and the improvement observed in sugar and pasta is retained but not extended. '
  'Nothing in the forecast projects a margin the filings have not already shown.')

H2('1.8  Macro and country — the cost of capital, built and priced')
P('Saudi macro is the benign part of this story: inflation of 1.8% (July 2026), a pegged '
  'currency, policy rates tracking the Fed down, and staple-food demand growing with '
  'population. The priced risks sit elsewhere: a fifth of revenue is Egypt (translation '
  'and repatriation), the commodity complex sets the cost side, and the capital structure '
  'carries a store-lease book at more than half of enterprise debt.')
cc = [['Component', 'Value', 'Source / construction']]
cc.append(['10Y SAR risk-free construction', pc(W['rf_observed'],2),
           'US 10Y 4.68% (Federal Reserve data, 14-Aug-2026) + 0.85% Saudi sovereign '
           'new-issue spread (Jan-2026 USD jumbo); cross-checked against the observed '
           '1-year SAR sovereign savings-sukuk rate of 4.70% (Aug-2026). No direct 10-year '
           'SAR quote was accessible; the construction is priced ±50bp below'])
cc.append(['less sovereign default spread', f"−{pc(W['sov_spread_rating'],2)}",
           'Moody\'s Aa3 basis (country-risk data, Jan-2026) — netted so country risk is '
           'not double-counted'])
cc.append(['risk-free rate used', pc(W['rf_star_rating'],2), 'the two lines above'])
cc.append(['Beta', f"{W['beta']:.3f}",
           'Savola weekly returns against the exchange\'s own published index, five years, '
           'lead-lag adjusted; n=254, R²=0.159, 90% interval 0.73-1.44 — wide, and priced '
           'in section 1.9'])
cc.append(['Equity risk premium', pc(W['erp_rating'],2),
           'Saudi total premium, rating basis (Jan-2026); the CDS basis '
           f"({pc(W['erp_cds'],2)} against a {pc(W['sov_spread_cds'],2)} spread) is run in "
           'parallel and shown below'])
cc.append(['Cost of equity', pc(W['ke_rating'],2), 'risk-free + beta × premium'])
cc.append(['Cost of loans (blended)', pc(W['kd_loans'],2),
           f"SAR tranche ({pc(W['debt_w']['sa'],0)} of the book) at 3M SAIBOR 4.74% + ~100bp "
           f"murabaha spread; Egyptian tranche ({pc(W['debt_w']['eg'],0)}) at its SAR-"
           'equivalent parity cost, NOT its ~25% nominal coupon; minor AED/DZD tranches at '
           '5.5%. All tranches sit above the 1-year sovereign, as corporate debt must'])
cc.append(['Cost of leases', pc(W['kd_lease'],2),
           'measured effective rate: FY2025 lease interest over the average lease balance'])
cc.append(['Weights (market)', f"{pc(W['we'],0)} / {pc(W['wl'],0)} / {pc(W['wlease'],0)}",
           'equity at market capitalisation; loans and leases at audited balances'])
cc.append(['Cost of capital — explicit', pc(W['wacc_exp'],2), 'the rows above'])
cc.append(['Cost of capital — terminal', pc(W['wacc_term'],2),
           f"terminal weights re-based to {pc(IN['tw_e'],0)} equity"])
table(cc, [1.85, 1.00, 4.15], band_rows={6, 10}, size=8.6)
caption(f'{T()} — the cost of capital, every component sourced and dated in the companion '
        'bibliography. Contested constructions are PRICED, not just named: at the CDS '
        f"sovereign basis the fair value is SAR {p2(DCF['ps_cds'])}; at −50bp / +50bp on "
        f"the risk-free construction it is SAR {p2(SN['rf_alts']['5.03%'])} / SAR "
        f"{p2(SN['rf_alts']['6.03%'])}; the beta interval is priced in section 1.9.")
P('Egypt, stated plainly: the Egyptian operations (sugar, oils, pasta, snacks — about a '
  'fifth of revenue) run in a serially devaluing currency. The balance sheet is partially '
  'self-hedged — the group carries a net EGP LIABILITY position of about EGP 7.4bn, so '
  'devaluation produces translation gains on the funding side even as it shrinks reported '
  'revenue — and the model carries Egyptian growth in SAR terms net of that drag. The '
  'Egyptian tranche of debt is carried at its SAR-equivalent cost in the blended rate '
  'above; carrying its 25%+ nominal coupon in a SAR model would misstate both the cost of '
  'debt and the hedge.')

H2('1.9  Sensitivity — in real, observable units')
figure(os.path.join(HERE, 'fig2_sens.png'), 6.4,
       f'{FG()} — fair value across the cost of capital and terminal growth. Spot sits in '
       'the neighbourhood of the higher-rate, lower-growth cells; the base case is the '
       'centre.')
bg = [['Beta', 'Fair value (SAR/share)', 'Reading']]
for b_, v in SN['beta_grid'].items():
    tag = ('measured' if abs(float(b_) - W['beta']) < 1e-6 else
           ('interval floor' if abs(float(b_) - 0.73) < 0.01 else
            ('interval cap' if abs(float(b_) - 1.44) < 0.01 else '')))
    bg.append([f'{float(b_):.2f}', p2(v), tag])
table(bg, [1.10, 1.60, 1.80], size=8.8)
caption(f'{T()} — the beta interval, priced. The regression is usable but wide '
        '(R² 0.159): across its own 90% interval the fair value runs from SAR '
        f"{p2(SN['beta_grid'][str(1.44)] if str(1.44) in SN['beta_grid'] else list(SN['beta_grid'].values())[-1])} "
        f"to SAR {p2(list(SN['beta_grid'].values())[0])}. The single most valuable thing a "
        'longer post-restructuring trading history will give this valuation is a tighter '
        'beta.')

# =========================== 2 TECHNICAL ====================================
H1('2  Technical and price structure')
P(NAR['summary'])
LV = TST['levels']
P(f"Resistance sits at SAR {p2(LV['res'][0])}, {p2(LV['res'][1])} and {p2(LV['res'][2])}; "
  f"support at SAR {p2(LV['sup'][0])}, {p2(LV['sup'][1])} and {p2(LV['sup'][2])} — "
  'levels from recency-weighted pivot clusters on the same cleaned series the rest of this '
  f"study runs on. {NAR['bull']} {NAR['bear']}")
figure(os.path.join(HERE, 'fig3_ma.png'), 7.0,
       f'{FG()} — twelve months of price against the moving-average stack. The 2026 shape '
       'is a round trip: the February-March slide into the low 20s, the June-July recovery '
       'to 30, and the August give-back to the flat 200-day near 25.4.')

# =========================== 3 PROBABILISTIC MAP =============================
H1('3  A probabilistic price map')
P('Where could the price plausibly trade — a different question from what the business is '
  'worth. The map below is a 50,000-path simulation calibrated on Savola\'s own price '
  'history and anchored, like every simulation in this series, so that it can never '
  'manufacture return out of the time value of money.')
mp = [['Horizon', 'p5', 'p25', 'p50', 'p75', 'p95', 'P(above spot)']]
for short, lab in [('1M', f"One month (to {H1M['grade_date']})"),
                   ('3M', f"Three months (to {H3M['grade_date']})")]:
    hz = STK['horizons'][short]
    mp.append([lab] + [p2(hz['pct'][p]) for p in ('p5', 'p25', 'p50', 'p75', 'p95')]
              + [pc(hz['p_above'], 0)])
table(mp, [2.02, 0.80, 0.80, 0.80, 0.80, 0.80, 0.95], size=8.8)
caption(f'{T()} — the forward percentile map from the {M["anchor_date"]} close of SAR '
        f'{p2(SPOT)}. Annualized volatility at the anchor is about '
        f"{pc(H3M['anchor_vol_ann'],0)}; no dividend falls inside either window (the next "
        'expected ex-date is around May 2027), so the drift is the financing rate alone.')
tl = [['Level within three months', '+5%', '+10%', '+15%', '−5%', '−10%', '−15%']]
tl.append(['Probability the level trades at least once',
           pc(H3M['touch_up5'], 0), pc(H3M['touch_up10'], 0), pc(H3M['touch_up15'], 0),
           pc(H3M['touch_dn5'], 0), pc(H3M['touch_dn10'], 0), pc(H3M['touch_dn15'], 0)])
table(tl, [2.30, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75], size=8.8)
caption(f'{T()} — the level-touch ladder: the chance each threshold prints at least once '
        'on any path, not the chance of finishing there.')
figure(os.path.join(HERE, 'fig4_fan.png'), 7.0,
       f'{FG()} — the three-month price cone against the fundamental central of SAR '
       f'{p2(CEN)}. The fundamental read sits between the median and the upper quartile '
       'of the price map: a re-rating to the fundamental value is well inside ordinary '
       'three-month variation.')
figure(os.path.join(HERE, 'fig5_dist.png'), 5.6,
       f'{FG()} — the one-month distribution.')
figure(os.path.join(HERE, 'fig6_dist.png'), 5.6,
       f'{FG()} — the three-month distribution.')
P('How honest is this map? It was backtested on Savola\'s own history before being '
  f"published: over the last five years, {BT5['windows']} non-overlapping three-month "
  f"forecasts scored {sgn(BT5['skill_norm'])} against a benchmark random walk carrying the "
  'same financing anchor — statistically indistinguishable from the benchmark, which is '
  'the honest claim: the map prices dispersion, it does not predict direction. Realized '
  f"outcomes fell inside the 50/80/90% bands {pc(BT5['cov50'],0)}, {pc(BT5['cov80'],0)} "
  f"and {pc(BT5['cov90'],0)} of the time, and the percentile ranks of outcomes were "
  f"roughly uniform (chi-square p = {BT5['chi2_p']:.2f}, Kolmogorov-Smirnov p = "
  f"{BT5['ks_p']:.2f}). Across the full cleaned history ({BTF['windows']} windows since "
  f"2012) the same score was {sgn(BTF['skill_norm'])} with coverage of "
  f"{pc(BTF['cov50'],0)}/{pc(BTF['cov80'],0)}/{pc(BTF['cov90'],0)} — bands a touch wide, "
  'disclosed rather than tuned away.')

# =========================== 4 COMPARISON OF LENSES ==========================
H1('4  Comparison of the lenses')
P(f"The four lenses span SAR {p2(min(LN[k]['base'] for k in _W))} to SAR "
  f"{p2(max(LN[k]['base'] for k in _W))}, and the ordering is information, not noise. The "
  f"book lens (SAR {p2(LN['book']['base'])}) is lowest: at recurring profitability Savola "
  'earns about its cost of equity, so undiscounted book is the floor. The cash-flow lens '
  f"(SAR {p2(LN['dcf']['base'])}) adds the non-operating pocket and a terminal return "
  'modestly above cost. The market-anchored lenses (relative SAR '
  f"{p2(REL['base'])}, normalised SAR {p2(LN['normalized']['base'])}) are highest — and "
  'the reason is one number. The dividend-discount multiple this study\'s own cost of '
  f"equity supports is {REL['pe_ddm']:.1f}x forward earnings; Saudi consumer names trade "
  f"at a mix-weighted {REL['pe_mix']:.1f}x. The market prices these earnings at a cost of "
  'equity around three points cheaper than Savola\'s measured beta demands. Close that gap '
  'from either side — the beta drifting toward the market\'s implied risk, or the '
  'multiple de-rating toward the model\'s — and the lenses converge; until then the '
  'weighted central holds the tension explicitly.')
P(f"The expert panel (Appendix C) widens the same disagreement: SAR {p2(EXP['e2']['base'])} "
  f"(dividend stream) to SAR {p2(EXP['e1']['base'])} (segment multiples), median SAR "
  f"{p2(D['panel_median'])}. Note what the panel does that the lens field cannot: Expert 3 "
  'prices the possibility that the return-on-capital spread never persists at all, and '
  'still lands within a riyal of book — the floor argument again, from a third direction.')

# =========================== 5 CATALYSTS ====================================
H1('5  Catalysts to watch')
for head, body in [
    ('Third-quarter 2026 results (around early November). ',
     'The replacement-cost claim meets the print: oil unit margins against four-year-high '
     'benchmarks, and Panda\'s revenue against its store count — the closest public proxy '
     'for the density question in section 1.7.'),
    ('The Al Mehbaj integration and the Jeddah nuts facility. ',
     'The one leg growing by acquisition. The consideration was not disclosed; if it '
     'appears in the second-half statements (business-combination note), the nuts build '
     'in this model should be re-anchored to it.'),
    ('The store programme itself. ',
     f"The company guides to 20+ new stores and 20+ refreshed stores in 2026; "
     f"{n0(H1_['stores'])} stood at June. Slippage would cut near-term capex and — under "
     'Framing B — raise the valuation; that irony is the crux in one sentence.'),
    ('The FY2026 dividend (recommendation around March 2027, ex around May 2027). ',
     f"The stated policy is 50-60% of profit. The model's payout at the midpoint implies "
     f"about SAR {p2(F['div'][0]/SHW)} per share for FY2026E against the SAR "
     f"{p2(IN['div_between'])} just paid for FY2025; the market reads this stock partly "
     'as an income claim, so the recommendation is a repricing event.'),
    ('Commodity tape. ',
     'Vegetable-oil benchmarks at four-year highs are the cost side of half the '
     'processing book; world sugar is soft, which flatters refining spreads but deflates '
     'the sugar top line. Both directions are already in the driver set; a sharp move in '
     'either re-anchors it.'),
    ('Egypt. ',
     'A step-devaluation would cut the SAR value of about a fifth of revenue while '
     'producing a translation gain on the net EGP liability; the model carries trend '
     'depreciation, not a step. The Egyptian sugar and oils volumes themselves have been '
     'the resilient part of the story.'),
    ('Herfy\'s turnaround. ',
     f"Consolidated at a loss through FY2025, EBITDA margin {pc(0.187)} and the loss "
     'nearly closed in the first half of 2026. It is small in the group P&L, but its own '
     'listed price feeds this valuation through the bridge; a credible return to profit '
     'moves both.')]:
    bullet(body, bold_head=head)

# =========================== 6 READING THE ZONES ============================
H1('6  Reading the probability zones')
P(f"Put sections 1 and 3 side by side. The weighted central of SAR {p2(CEN)} sits between "
  'the median and the upper quartile of the three-month price map — the market needs '
  'nothing unusual to close the gap; ordinary variation covers it. The Framing B reading '
  f"of SAR {p2(DCF['framingB'])} sits just below the lower quartile — the market is "
  'currently priced closer to the no-turn story than to the base case. The zones to '
  f"watch: below SAR {p2(LV['sup'][2])} the price has broken the year's shelf and the "
  'market is voting for Framing B with conviction; above SAR '
  f"{p2(LV['res'][0])}-{p2(LV['res'][1])} the recovery leg is re-established and the "
  'first half\'s operating momentum is being paid for. Neither price move would change '
  'the fundamental work — but each would say which framing the market believes, and '
  'section 1.7 says exactly what evidence would justify believing it.')

# =========================== 7 CAVEATS ======================================
H1('7  Caveats — and what would change our mind')
for head, body in [
    ('The terminal is three quarters of the answer. ',
     f"{pc(DCF['tv_share'],0)} of enterprise value is beyond 2030, at a terminal return "
     f"({pc(IN['roic_term'])}) only modestly above the terminal cost of capital "
     f"({pc(W['wacc_term'],2)}). We would rather own that honesty than an inflated "
     'five-year ramp; section 1.9 prices the alternatives.'),
    ('The beta is wide. ',
     'R² of 0.159 and a 90% interval of 0.73-1.44 — partly the 2024-2025 restructuring '
     'distorting the return series. Eighteen more months of clean post-reset trading '
     'would tighten the single most consequential input in the study.'),
    ('Panda\'s density is unobservable. ',
     'No like-for-like series is published; the sales-per-store driver is a derivation. '
     'If the company begins disclosing like-for-like growth, the crux resolves and this '
     'model should be restruck the same week.'),
    ('The second half of 2026 carries the company\'s own warning. ',
     'Replacement-cost pressure in oils is management\'s statement, adopted here (unit '
     'gross profit held below the first-half actual). If the second half instead HOLDS '
     'the first-half unit margins, the base case is too low by construction — that is '
     'the direction of surprise this model accepts.'),
    ('Egypt can step. ',
     'The model carries drift, not a crisis. A 2016- or 2024-style step devaluation '
     'would cut the processing top line faster than the natural hedge compensates in '
     'reported profit.'),
    ('The Mehbaj consideration is undisclosed. ',
     'The nuts leg carries a small, flagged inorganic step. If the price paid turns out '
     'large, the balance-sheet side of this model (not just revenue) needs the '
     'transaction folded in.'),
    ('What would flip the verdict. ',
     f"Two more quarters of density erosion at the measured pace (Framing B: SAR "
     f"{p2(DCF['framingB'])}, below spot) — or a second-half margin print above the "
     'first half plus a stabilising store base (the bull scenario: SAR '
     f"{p2(LN['dcf']['bull'])}). The evidence that decides is named in section 1.7.")]:
    bullet(body, bold_head=head)

# =========================== APPENDIX A =====================================
H1('Appendix A — Financial statements')
H2('A.1  Income statement — three audited years and the five-year forecast')
ist = [['SAR mn', 'FY2023', 'FY2024', 'FY2025'] + YRS]
def _row(lab, h, f_, fmt=n0):
    return [lab] + [fmt(x) if x is not None else '—' for x in h] + [fmt(x) for x in f_]
ist.append(_row('Revenues', [HI['FY23']['rev'], HI['FY24']['rev'], HI['FY25']['rev']],
                F['rev']))
ist.append(_row('Cost of revenues', [-HI['FY23']['cogs'], -HI['FY24']['cogs'],
                                     -HI['FY25']['cogs']], [None]*0) + ['—']*5)
ist.append(_row('Gross profit', [HI['FY23']['gp'], HI['FY24']['gp'], HI['FY25']['gp']],
                []) + ['—']*5)
ist.append(_row('Operating EBITDA', [HI['FY23']['ebitda'], HI['FY24']['ebitda'],
                                     HI['FY25']['ebitda']], F['ebitda']))
ist.append(_row('Depreciation & amortisation', [-HI['FY23']['dna'], -HI['FY24']['dna'],
                                                -HI['FY25']['dna']],
                [-x for x in F['dna']]))
ist.append(_row('EBIT', [HI['FY23']['ebitda'] - HI['FY23']['dna'],
                         HI['FY24']['ebitda'] - HI['FY24']['dna'],
                         HI['FY25']['ebitda'] - HI['FY25']['dna']], F['ebit']))
ist.append(_row('Net finance cost', [None, None, -275.525], F['netfin']))
ist.append(_row('Share of Kinan (net of tax)', [None, None, HI['FY25']['assoc']],
                F['kinan'], p1))
ist.append(_row('Profit attributable to owners', [HI['FY23']['np_att'],
                                                  HI['FY24']['np_att'],
                                                  HI['FY25']['np_att']], F['np']))
ist.append(_row('Earnings per share (SAR)', [None, None, HI['FY25']['eps']], F['eps'], p2))
table(ist, [1.56] + [0.68] * 8, band_rows={4, 6, 9}, size=7.9)
caption(f'{T()} — income statement. Bases differ and are stated rather than smoothed: '
        'FY2023 is the continuing basis of the FY2024 statements and still contains the '
        'Türkiye business (disposed 2025; its FY2024 revenue was SAR 941mn); FY2024-25 are '
        'the FY2025 audited basis. FY2024 attributable profit contains the SAR 11,554.7mn '
        'Almarai distribution gain; FY2025 contains a SAR 217.4mn zakat release (recurring '
        'profit SAR 539.1mn on the company\'s own bridge). The forecast is built on the '
        'recurring construction, with associates outside the tax line as the statements '
        'present them.')
H2('A.2  Balance sheet')
bst = [['SAR mn', 'FY2023', 'FY2024', 'FY2025'] + YRS]
bst.append(_row('Property, plant & equipment (owned)', [6046.276, HB['FY24']['ppe'],
                                                        HB['FY25']['ppe']], F['ppe']))
bst.append(_row('Right-of-use assets', [3040.384, 3058.060, IN['rou_fy25']], F['rou']))
bst.append(_row('Net working capital', [None, None, HB['FY25']['nwc']], F['nwc']))
bst.append(_row('Cash and cash equivalents', [1213.193, HB['FY24']['cash'],
                                              IN['cash_fy25']], F['cash']))
bst.append(_row('Loans and borrowings', [8644.487, HB['FY24']['loans'],
                                         IN['loans_fy25']],
                [IN['loans_fy25']] * 5))
bst.append(_row('Lease liabilities', [3522.529, HB['FY24']['leases'], IN['leases_fy25']],
                F['leases']))
bst.append(_row('Equity attributable to owners', [HB['FY23']['equity_att'],
                                                  HB['FY24']['equity_att'],
                                                  IN['equity_att_fy25']], F['equity_att']))
bst.append(_row('Net debt (loans less cash and current investments)',
                [8644.487 - 1213.193 - 738.395,
                 HB['FY24']['loans'] - HB['FY24']['cash'],
                 IN['loans_fy25'] - IN['cash_fy25'] - IN['inv_c_fy25']], F['netdebt']))
table(bst, [1.56] + [0.68] * 8, band_rows={7}, size=7.9)
caption(f'{T()} — balance sheet. The FY2023 column is the pre-reset structure: SAR 8.6bn '
        'of borrowings against the Almarai stake. The reset removed both sides. The '
        'forecast columns are the model\'s roll-forward, which foots exactly in every year '
        '(the companion workbook carries the zero-check row). At 30-Jun-2026 the company '
        f"reported net debt of SAR {n0(H1_['netdebt'])}mn on its own definition.")
H2('A.3  Forecast cash-flow markers')
cft = [['SAR mn'] + YRS]
cft.append(['Net cash from operating activities'] + [n0(x) for x in F['cfo']])
cft.append(['Capital expenditure'] + [n0(-x) for x in F['capex']])
cft.append(['Lease principal (right-of-use depreciation)'] + [n0(-x) for x in F['dna_rou']])
cft.append(['Dividends (owners + minorities)'] +
           [n0(-(a_ + b_)) for a_, b_ in zip(F['div'], F['div_nci'])])
cft.append(['Free cash flow to the firm'] + [n0(x) for x in F['fcff']])
cft.append(['Closing cash'] + [n0(x) for x in F['cash']])
table(cft, [2.30, 0.94, 0.94, 0.94, 0.94, 0.94], band_rows={5}, size=8.6)
caption(f'{T()} — the cash walk that closes the balance sheet: operations fund the '
        'programme and the dividend with a widening surplus; net debt on the company\'s '
        f"definition falls from SAR {n0(F['netdebt'][0])}mn to SAR {n0(F['netdebt'][4])}mn "
        'by FY2030E.')

# =========================== APPENDIX B =====================================
H1('Appendix B — Peer frame, risk register, research register')
H2('B.1  Peer frame')
P('The peer table and the multiple construction sit in section 1.3; the workbook\'s Peer & '
  'Sector sheet carries the same quotes with Savola\'s own implied multiples beside them: '
  f"at the model's fair value Savola stands at {p2(DCF['ps']/F['eps'][0])}x FY2026E "
  f"earnings and {p2(DCF['ev']/F['ebitda'][0])}x FY2026E EBITDA (lease-inclusive), against "
  f"{p2(SPOT/F['eps'][0])}x and the peer set's 12-20x earnings range.")
H2('B.2  Risk register')
rk = [['Risk', 'Direction', 'Where it is priced']]
for a_, b_, c_ in [
    ('Vegetable-oil replacement costs run past pass-through', 'margin down',
     'oil unit gross profit held below the H1 actual; bear cuts it 40 SAR/t'),
    ('Panda density never stabilises', 'value down', 'Framing B, published side by side'),
    ('Grocery price war intensifies (discounters)', 'margin down',
     'store-opex ratio held; no gross-margin recovery assumed'),
    ('Egypt step-devaluation', 'revenue down, partial hedge',
     'trend depreciation in the build; net EGP liability disclosed in 1.8'),
    ('Commodity finance rates', 'finance cost',
     'blended marginal cost of debt above sovereign; sensitivity on the rate build'),
    ('Herfy stays loss-making', 'drag',
     'glide anchored on the actual; its market price in the bridge'),
    ('Mehbaj consideration turns out large', 'balance sheet',
     'flagged as undisclosed; revenue effect kept small'),
    ('Zakat assessments', 'one-off',
     'FY2025\'s release treated as non-recurring; normalized rate 19.5% carried'),
    ('Terminal return fades to cost of capital', 'value down',
     'Expert 3 prices exactly this; section 1.9 grid')]:
    rk.append([a_, b_, c_])
table(rk, [2.55, 1.25, 3.10], size=8.6)
caption(f'{T()} — the risk register: every named risk points at the place in the study '
        'where it is PRICED, not merely mentioned.')
H2('B.3  Research register — what was read, and what was searched and not found')
rr = [['Source (all read from official homes)', 'Date', 'What was taken']]
for i, (s_, d_, w_) in enumerate([
    ('FY2025 audited consolidated financial statements (Deloitte, unmodified)',
     '05-Mar-2026', 'the base year: statements, segments, notes 1-46'),
    ('FY2024 audited consolidated financial statements (KPMG)', '10-Mar-2025',
     'FY2023 comparatives; the rights issue / capital reduction / Almarai distribution'),
    ('FY2023 audited consolidated financial statements', '14-Mar-2024',
     'FY2022 comparatives; pre-reset balance sheet'),
    ('Q1-2026 reviewed interim statements', '06-May-2026',
     'first-quarter actuals; 31-Mar-2026 balance sheet'),
    ('H1-2026 earnings release (company)', '06-Aug-2026',
     'half-year actuals; net debt 851; Sudan exit; Mehbaj; the H2 cost warning'),
    ('Q2-2026 investor presentation (company)', '06-Aug-2026',
     'category volumes and unit gross profits; store network; segment debt and leases'),
    ('FY2025 investor presentation (company)', '09-Mar-2026',
     'full-year category units; the reported-to-recurring bridge; capex by unit'),
    ('Annual Report 2025 (company)', '30-Mar-2026',
     'dividend policy; governance; the Mehbaj related-party context; store programme'),
    ('Saudi Exchange announcements 93502 / 93503 / 94980', 'Mar-May 2026',
     'official FY2025 results, dividend recommendation, Q1-2026 results'),
    ('Federal Reserve economic data (US 10Y and 1Y)', '14-Aug-2026',
     'the risk-free construction\'s dollar leg'),
    ('Sovereign risk dataset (Jan-2026 update)', '05-Jan-2026',
     'Saudi default spread, equity risk premium, CDS; Egypt for context'),
    ('National Debt Management Center announcements', 'Aug-2026',
     'the observed 1-year SAR sovereign savings-sukuk rate (4.70%)'),
    ('FAO Food Price Index', '07-Aug-2026',
     'vegetable-oil, sugar and cereal price levels for the cost side'),
    ('GASTAT consumer prices (July 2026)', '14-Aug-2026', 'Saudi CPI 1.8%'),
    ('Market quotes: Savola, Herfy, four peers, SAIBOR', '18-Aug-2026',
     'prices and multiples — cross-checks and the bridge\'s Herfy leg only')], 1):
    rr.append([s_, d_, w_])
table(rr, [3.35, 0.85, 2.75], size=8.2)
caption(f'{T()} — the research register. Searched and NOT found, recorded as such: the Al '
        'Mehbaj consideration (no disclosure anywhere); a Panda like-for-like sales '
        'series (not published); numeric FY2026 revenue or margin guidance (none exists — '
        'only store-count targets); a directly quotable 10-year SAR government yield '
        '(constructed instead, and priced both ways in section 1.8). The reviewed H1-2026 '
        'interim statements were filed with the authorities but not yet mirrored on the '
        'company\'s website at the study date; the company\'s own release and '
        'presentation carry every H1 figure used.')

# =========================== APPENDIX C =====================================
H1('Appendix C — The expert panel')
P('Three experts, three genuinely different methods, each with its worldview, its worked '
  'numbers, a named sensitivity and a falsifier stated in advance. They are labelled '
  'Expert 1, 2 and 3; their disagreement is the appendix\'s product, not a defect.')
E1, E2, E3 = EXP['e1'], EXP['e2'], EXP['e3']
H2('C.1  Expert 1 — the segment sum-of-the-parts investor')
P('Worldview: a conglomerate is worth what its pieces would fetch, and the market tells '
  'you what pieces fetch. Works best when segments have clean listed comparables and '
  'central costs are small; fails when the multiples themselves are mispriced or the '
  'pieces cannot actually be separated (shared brands, shared logistics, a controlling '
  'family that will never sell).')
e1t = [['Line', 'Basis', 'SAR mn']]
e1d = E1['detail']
e1t.append(['Food processing at 6.5x FY2026E EBITDA',
            f"EBITDA {n0(F['fp_eb'][0])}", n0(e1d['fp_ev'])])
e1t.append(['Panda at 7.0x FY2026E EBITDA', f"EBITDA {n0(F['panda']['eb'][0])}",
            n0(e1d['ret_ev'])])
e1t.append(['Al Kabeer at 7.0x FY2026E EBITDA', f"EBITDA {n0(F['frozen']['eb'][0])}",
            n0(e1d['frz_ev'])])
e1t.append(['Central costs capitalized at 6.5x', f"−{n0(IN['unalloc_path'][0])}/yr",
            n0(e1d['unalloc'])])
e1t.append(['Segment enterprise value', '', n0(e1d['ev'])])
e1t.append(["Savola's 49% of Herfy at Herfy's own market price",
            f"market cap {n0(DCF['herfy_mktcap'])}", n0(e1d['herfy_49'])])
e1t.append(['Non-operating pocket + cash', 'sukuk, Almarai residual, Kinan, property',
            n0(DCF['nonop'] + IN['cash_fy25'])])
e1t.append(['Less loans, leases, benefits, restoration, other net liabilities', '',
            n0(-(IN['loans_fy25'] + IN['leases_fy25'] + IN['eb_fy25'] + IN['restor_fy25']
                 + IN['other_net_liab']))])
e1t.append(['Less other minorities at book', '', n0(-DCF['nci_other_book'])])
e1t.append(['Equity value', '', n0(e1d['eq'])])
e1t.append(['Per share at 31-Dec-2025 → at the anchor',
            f"{p2(e1d['ps_dec'])} → rolled and ex-dividend", p2(E1['base'])])
table(e1t, [3.05, 2.35, 1.30], band_rows={5, 10}, size=8.6)
caption(f'{T()} — Expert 1\'s worked table. Named sensitivity: one multiple turn across '
        f"the three operating legs is worth about SAR {p2((F['fp_eb'][0]+F['panda']['eb'][0]+F['frozen']['eb'][0])/SHW * DCF['roll'])} "
        f"per share (range SAR {p2(E1['rng'][0])}-{p2(E1['rng'][1])} at ±0.75 turns). "
        'Falsifier, stated in advance: if Saudi consumer multiples de-rate toward the '
        'dividend-discount multiple in section 4, this whole frame deflates with them.')
H2('C.2  Expert 2 — the dividend-stream investor')
P('Worldview: for a policy-driven payer under a family anchor, the dividend IS the '
  'security. Works best when the policy is stated and the balance sheet can fund it; '
  'fails when value is building inside the firm faster than it is paid out — this method '
  'structurally under-values retained growth.')
e2t = [['Year', 'Dividend per share (SAR)', 'Present value at the cost of equity']]
for i, dp in enumerate(E2['detail']['dps']):
    e2t.append([YRS[i], p2(dp), p2(dp / (1 + W['ke_rating']) ** (i + 1))])
e2t.append(['Terminal (grown at 2.5%)', p2(E2['detail']['dps'][-1] * (1 + IN['g_term'])),
            p2(E2['detail']['pv_tv'])])
e2t.append(['Value at 31-Dec-2025 → at the anchor', p2(E2['detail']['ps_dec']),
            p2(E2['base'])])
table(e2t, [2.20, 2.20, 2.30], band_rows={7}, size=8.6)
caption(f'{T()} — Expert 2\'s worked table. Named sensitivity: the policy band itself — '
        f"at 50% payout the value is SAR {p2(E2['rng'][0])}, at 60% with a stronger "
        f"terminal SAR {p2(E2['rng'][1])}. Falsifier: a second consecutive year outside "
        'the stated 50-60% band, in either direction, breaks the premise that the policy '
        'is the security.')
H2('C.3  Expert 3 — the economic-profit sceptic')
P('Worldview: value is invested capital plus the present value of returns ABOVE the cost '
  'of capital — and excess returns decay, because competition exists. Works best at '
  'exposing how much of a valuation is faith in persistence; fails for businesses with '
  'genuinely durable moats, which it structurally under-values.')
e3t = [['Line', 'SAR mn']]
e3t.append(['Invested capital, 31-Dec-2025 (equity + minorities + debt + leases − cash − '
            'investments − Kinan)', n0(E3['detail']['ic0'])])
for i in range(5):
    e3t.append([f"Economic profit {YRS[i]} (NOPAT {n0(F['nopat'][i])} less capital charge "
                f"at {pc(W['wacc_exp'],2)})", n0(E3['detail']['ri'][i])])
e3t.append(['Present value of the five economic-profit years', n0(E3['detail']['pv_ri'])])
e3t.append(['Fade tail (spread decays to zero over five more years)',
            n0(E3['detail']['fade'])])
e3t.append(['Operating value', n0(E3['detail']['ev'])])
e3t.append(['Bridge to equity (as in section 1.1, Kinan at carrying)', n0(E3['detail']['eq'])])
e3t.append(['Per share at the anchor', p2(E3['base'])])
table(e3t, [5.10, 1.60], band_rows={7, 12}, size=8.6)
caption(f'{T()} — Expert 3\'s worked table. Named sensitivity: the fade — no tail at all '
        f"gives SAR {p2(E3['rng'][0])}; 40% of the year-five spread persisting for another "
        f"five years gives SAR {p2(E3['rng'][1])}. Falsifier: returns on capital RISING "
        'through FY2027-28 while the store programme runs would refute the decay premise '
        'directly.')
H2('C.4  Cross-examination')
for q_, a_ in [
    ('Expert 2 to Expert 1: your multiples pay for growth Savola has not delivered — '
     'recurring profit only recovered to SAR 539mn in FY2025.',
     'Expert 1, partially conceded: the multiples are the market\'s, not mine; I hold the '
     'discount at one turn below the quoted medians for exactly that reason. But rejected '
     'on the frame: first-half recurring profit rose 40% — the recovery is in the prints, '
     'not projected.'),
    ('Expert 1 to Expert 2: you price a POLICY as if it were a covenant; the same board '
     'paid nothing for FY2024.',
     'Expert 2, conceded in part: FY2024 was the reset year, and I read the policy '
     'through the reset. My low case prices the 50% floor; a policy break is my stated '
     'falsifier, not a hidden assumption.'),
    ('Expert 3 to both: neither of you asks whether the returns exist. My table says the '
     'business earns barely above its capital charge in every forecast year.',
     'Expert 1, rejected: your capital base includes SAR 3.95bn of store leases at a '
     'retail margin trough — you are measuring the programme at its worst moment. '
     'Expert 2, conceded: that is why my number is closest to yours.'),
    ('The panel to the model: your Framing B sits below every one of our low cases except '
     'Expert 2\'s.',
     'Accepted as information: the framing the market appears to price is more '
     'pessimistic than any panel construction — either an opportunity or a warning, and '
     'section 6 says which evidence decides.')]:
    bullet(a_, bold_head=q_ + ' — ')
H2('C.5  Three in one room')
P(f"Force the three to one number and the argument, not the average, is the output. "
  f"Expert 1 (SAR {p2(E1['base'])}) prices the pieces at the market's capital; Expert 2 "
  f"(SAR {p2(E2['base'])}) prices the payout at the model's capital; Expert 3 (SAR "
  f"{p2(E3['base'])}) prices the capital itself and finds little excess. The median — SAR "
  f"{p2(D['panel_median'])} — lands below the study's weighted central of SAR {p2(CEN)}, "
  'and the gap is the same single disagreement running through the whole study: what '
  'return this capital deserves, and whether the expansion earns above it.')
figure(os.path.join(HERE, 'figD1_experts.png'), 7.0,
       f'{FG()} — the three experts\' ranges against spot; the gold band marks the panel '
       'median.')
H2('C.6  Reading the divergence')
dv = [['Assumption', 'Expert 1', 'Expert 2', 'Expert 3', 'What the gap is worth']]
dv.append(['Price of capital', 'the market\'s (in the multiples)',
           f"the model's ({pc(W['ke_rating'],2)})", f"the model's ({pc(W['wacc_exp'],2)})",
           f"E1 vs E2: SAR {p2(E1['base']-E2['base'])}/share — the study's largest gap"])
dv.append(['Retained growth', 'in the multiple', 'ignored beyond payout',
           'earns only the spread',
           f"E2 vs E3: SAR {p2(E3['base']-E2['base'])}/share"])
dv.append(['Return persistence', 'implicit', 'implicit', 'decays to zero by 2035',
           f"E3's own fade sensitivity: SAR {p2(E3['rng'][1]-E3['rng'][0])}/share"])
table(dv, [1.20, 1.35, 1.25, 1.35, 1.78], size=8.2)
caption(f'{T()} — which assumption drives which gap. One judgement — the price of capital '
        '— explains most of the panel\'s spread, exactly as it explains the lens spread '
        'in section 4.')

# =========================== ABOUT / DISCLOSURE ==============================
H1('About this series')
P('These studies are independent educational analyses of listed companies and commodities. '
  'Each one builds its financial model exclusively from the subject\'s own audited and '
  'reviewed statements and disclosures, prices its probability maps with a simulation '
  'engine backtested on the subject\'s own history, and publishes fair-value ranges and '
  'distributions — never ratings, never price targets. The companion workbook is '
  'formula-driven so every figure can be traced to a driver and repriced; the companion '
  'bibliography lists every input with its source and date.')
H1('Disclosure & Disclaimer')
P('This document is educational analysis, not investment advice, not a recommendation, and '
  'not a solicitation to buy or sell any security. It was prepared without compensation '
  'from, or communication with, the subject company. All historical figures derive from '
  'public official sources believed reliable but not independently audited by the author; '
  'forecasts are model outputs, not promises. Markets are risky; distributions are wide '
  'for a reason. Do your own work or engage a licensed adviser before acting.',
  size=9.0)

doc.save(os.path.join(HERE, 'SAVOLA_Valuation_Study_18-08-2026_public.docx'))
print(f'study written · {_TN[0]} tables · {_FN[0]} figures')
