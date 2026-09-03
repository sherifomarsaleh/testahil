"""The terminal-value census — [R-TERM-01]'s measurement, and it runs before any treatment.

WHY THIS EXISTS. Every study in this book discounts an explicit window and then
capitalises a terminal, and most of them build that terminal from the reinvestment
identity g = rr x ROIC:

    rr = g / ROIC,   ROIC = NOPAT / IC,   TV = NOPAT (1 - rr) / (W - g)

Substitute and the reinvestment charge collapses to a constant that does not depend on
ROIC at all:

    TV = [ NOPAT - g . IC ] / (W - g)

So the construction charges g x IC every year for ever. THE IDENTITY IS A STATEMENT
ABOUT REAL GROWTH. Where g is a nominal rate whose real component is zero — which is
what the house macro path returns for every terminal it builds [R-MACRO-01] — the charge
buys no capacity at all, and the model is paying for what inflation supplies free.

THE DIAGNOSTIC THAT MAKES IT VISIBLE. Read the charge as a capital-maintenance
programme and ask how long it takes to replace the asset base:

    implied replacement cycle  =  IC / charge  =  IC / (g . IC)  =  1 / g

The implied asset life is THE RECIPROCAL OF THE INFLATION RATE. It has nothing to do
with the asset. At 7% terminal inflation it is 14.3 years; at 15% it is 6.7. A cement
kiln does not get younger because the currency got worse. That single number is what this
census computes, name by name, and it is why the defect is a class and not an accident:
the higher a market's inflation, the more brutal the charge, which is the exact opposite
of prudence.

THE FLOOR, which needs no opinion at all. A company can always decline to invest beyond
maintenance and pay the rest out. So a terminal can never be worth less than a no-growth
perpetuity on the same profit:

    TV  >=  NOPAT_last / W

That is a dominance argument, not a judgement: it has no parameters, so there is nothing
in it to tune. A terminal below its own floor is dominated by a policy the company can
choose unilaterally, and the study has published the worse of two worlds.

THE DIRECTION OF THE DEFECT IS SET BY THE MARKET'S INFLATION RATE, AND THAT EXPLAINS THE
WHOLE PHENOMENON THIS REASSESSMENT WAS CALLED OVER.

The implied life is 1/g, so it is SHORT where terminal inflation is high and LONG where it
is low. A real industrial asset life sits somewhere near 20-40 years. So one construction
over-charges in a high-inflation market and UNDER-charges in a low-inflation one, and the
same formula is pessimistic in Cairo and generous in Abu Dhabi:

  ticker           g   implied life   charge   EV at L=20   EV at L=30   EV at L=40
  AMOC          7.0%      14.3 y      23.1%       +4.8%        +8.8%       +10.8%
  SWDY          5.0%      20.0 y      24.5%        0.0%        +9.2%       +13.8%
  RIYADHCABLE   4.0%      25.0 y      15.9%       -3.8%        +2.5%        +5.7%
  AMR           3.0%      33.3 y      10.0%       -5.5%        -0.9%        +1.4%
  AIRARABIA     2.5%      40.0 y      17.5%      -20.2%        -6.7%         0.0%
  DU            2.5%      40.0 y       9.1%       -8.4%        -2.8%         0.0%
  MODON         2.5%      40.0 y      29.4%      -28.6%        -9.5%         0.0%
  SAVOLA        2.5%      40.0 y      24.8%      -26.2%        -8.7%         0.0%
  ADNOCLS       2.0%      50.0 y      18.1%      -24.9%       -11.1%        -4.1%
  FERTIGLOBE    2.0%      50.0 y      14.8%      -14.4%        -6.4%        -2.4%
  ADNOCDIST     1.5%      66.7 y       6.0%      -11.2%        -5.8%        -3.2%

CORRECTING THIS PROPERLY WOULD LOWER MOST OF THE BOOK. At a 30-year life three of eleven
names rise and eight fall, median -5.8%. It raises the EGYPTIAN names — which is exactly
where the pessimism complaint came from — and lowers the Gulf names, whose 1.5% to 2.5%
terminal inflations bought them a forty- to sixty-seven-year replacement cycle nobody ever
argued for and no accounting-policies note supports.

A CORRECTION THAT MOVES MOST OF THE BOOK DOWN IS NOT A REASON TO RECONSIDER THE CORRECTION.
It is the reason this census had to exist before anything was fixed: measured one name at a
time, from the direction of the complaint, the obvious move was to loosen the terminal
everywhere. Measured across the book, that would have been right on two names and wrong on
eight, and it would have looked like progress on both counts because nobody was comparing.

THE GENERAL LESSON: A DEFECT WHOSE DIRECTION DEPENDS ON A MARKET PARAMETER WILL LOOK LIKE A
HOUSE BIAS IN WHICHEVER MARKET YOU HAPPEN TO BE LOOKING AT. The complaint was true, its
attribution was not, and only the census could tell the two apart.

READING THIS OUTPUT. It measures; it does not correct. Every figure is resolved from each
study's OWN committed numbers file and the census RECORDS THE KEY THAT ANSWERED, so a
study whose terminal cannot be read comes back UNREADABLE rather than clean — an empty
result is not a clean result [R-ENF-04]. Nothing here is an input to any study.

RESOLUTION IS FRAME-COHERENT, AND THE FIRST VERSION WAS NOT. Several studies publish two
or more framings of the same company — dcf_A and dcf_B, a base case and a scenario, a
tax-regime pair. The first resolver took each field from whichever container answered
first, and on FERTIGLOBE it read the terminal value and terminal rate from FRAME A and the
last explicit NOPAT from FRAME B. THE RESULT WAS A PLAUSIBLE NUMBER AND A FABRICATED
BREACH: a floor of 8,174 against frame A's real 5,347, reported as 30.7% below its own
floor when the study sits 6.0% above it.

So a terminal is now read from ONE container. Whichever holds the terminal value fixes the
frame, every other field is sought there first, and a field that had to be found elsewhere
is RECORDED with the container it came from so the mixing is visible rather than silent.
That is the same defect this whole rule is about, one level up: A CHECK POINTED AT THE
WRONG MEASUREMENT PRODUCES A CONFIDENT WRONG ANSWER, and it was found by asking whether a
study the census condemned actually deserved it.
"""
from __future__ import annotations

import json
import math
import os
import re
from glob import glob

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Candidate keys, in preference order. A study is read through the FIRST one present and
# the census reports which — a resolver that silently guesses is the species of defect
# [R-ENF-04] exists to close.
CAND = {
    'tv':        ('tv', 'terminal_value', 'tv_value'),
    'pv_tv':     ('pv_tv', 'pv_terminal'),
    'tv_share':  ('tv_share', 'tv_pct'),
    'wacc_term': ('wacc_term', 'wacc_terminal', 'wacc_T'),
    # 'g' is where studies diverge most: some name it in the DCF, some only in the macro
    # record, some only in a case's inputs. Every route is listed and the census reports
    # WHICH answered, because a resolver that guesses is the defect [R-ENF-04] closes.
    'g':         ('g_term', 'g_terminal', 'terminal_g', 'terminal_growth',
                  'growth_at_horizon_end', 'TERMINAL_GROWTH', 'tg', 'g'),
    'nopat_term':('nopat_term', 'nopat_T', 'nopat_t1', 'nopat_next',
                  'terminal_nopat'),
    'ic':        ('ic_repl', 'ic_replacement', 'ic_terminal', 'ic_T', 'invested_capital',
                  'ic_replacement_cost'),
    'rr_term':   ('rr_term', 'rr_T', 'rr_repl', 'reinv_rate', 'reinvest'),
    'roic_term': ('roic_term', 'roic_T', 'roic_terminal', 'terminal_roc'),
    'df_tv':     ('df_tv', 'dftv'),
    'equity':    ('equity', 'eq_val', 'eq_attr', 'eq'),
    'fv':        ('fv', 'ps', 'per_share', 'fv_aed'),
}
# Where a study nests its DCF under a case or framing rather than a bare 'dcf'.
DCF_HOLDERS = ('dcf', 'dcf_A', 'dcf_B', 'dcf.frame_A', 'dcf.base_ct', 'cases.base',
               'framings.normalisation', 'wacc', 'macro_record',
               'cost_of_capital_record', 'model_parameters')


def _flat(o, path='', out=None):
    """Every numeric leaf, keyed by dotted path. Lists are indexed."""
    out = {} if out is None else out
    if isinstance(o, dict):
        for k, v in o.items():
            p = f'{path}.{k}' if path else k
            if isinstance(v, (int, float)) and not isinstance(v, bool):
                out[p] = float(v)
            elif isinstance(v, (dict, list)):
                _flat(v, p, out)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            p = f'{path}[{i}]'
            if isinstance(v, (int, float)) and not isinstance(v, bool):
                out[p] = float(v)
            elif isinstance(v, (dict, list)):
                _flat(v, p, out)
    return out


def _resolve(flat, names, prefer=DCF_HOLDERS):
    """First candidate present, preferring a DCF-ish container. Returns (value, key)."""
    for n in names:
        # a container-qualified hit first, so dcf.tv beats sensitivity.rows[3].tv
        for pre in prefer:
            k = f'{pre}.{n}'
            if k in flat:
                return flat[k], k
        # then any leaf whose FINAL segment is exactly this name
        hits = [k for k in flat if k.split('.')[-1] == n]
        if len(hits) == 1:
            return flat[hits[0]], hits[0]
        if hits:
            # deterministic: shortest path wins, ties broken lexically
            hits.sort(key=lambda k: (k.count('.'), len(k), k))
            return flat[hits[0]], hits[0]
    return None, None


def _last_explicit(flat, field):
    """The last explicit-window value of a forecast row (forecast.nopat[-1] and kin)."""
    if not isinstance(field, str):          # a candidate tuple: try each in order
        for f in field:
            v, k = _last_explicit(flat, f)
            if v is not None:
                return v, k
        return None, None
    idx = [(int(k.split('[')[-1].rstrip(']')), k) for k in flat
           if k.split('[')[0].split('.')[-1] == field and k.endswith(']')]
    if not idx:
        return None, None
    idx.sort()
    return flat[idx[-1][1]], idx[-1][1]


def _frame_of(key):
    """The container a resolved key sits in — everything before its final segment."""
    return key.rsplit('.', 1)[0] if '.' in key else ''


# A study's frame identity is not one container. FERTIGLOBE keys its terminal under dcf_A,
# its forecast rows under frame_A and its bridge under bridge_A; PHDC uses cases.base and
# cases.low_conversion. So the FRAME TAG is what has to match, not the container name.
_TAG_RX = re.compile(r'(?:^|[._])(A|B|C|base|bull|bear|low_conversion|high_conversion|'
                     r'base_ct|base_dmtt|ct|dmtt|frame_A|frame_B|normalisation|prolonged)'
                     r'(?:$|[._\[])')


def _tag_of(key):
    """The frame tag a key belongs to, or '' where it belongs to none."""
    m = _TAG_RX.search(_frame_of(key))
    if not m:
        return ''
    t = m.group(1)
    return t[-1] if t in ('frame_A', 'frame_B') else t


def read_study(d):
    """One study's terminal, read from ONE frame, or a stated reason it cannot be read."""
    tk = os.path.basename(d)[:-6].upper()
    f = os.path.join(d, 'study_numbers.json')
    rec = {'ticker': tk, 'dir': os.path.relpath(d, REPO), 'routes': {}, 'off_frame': []}
    if not os.path.exists(f):
        rec['unreadable'] = 'no committed numbers file'
        return rec
    try:
        n = json.load(open(f))
    except Exception as e:
        rec['unreadable'] = f'numbers file will not parse: {e}'
        return rec
    flat = _flat(n)

    # THE TERMINAL VALUE FIXES THE FRAME. Everything else is sought inside it first, and
    # anything found outside it is recorded rather than silently mixed in.
    tv, tvk = _resolve(flat, CAND['tv'])
    if tv is None:
        rec['unreadable'] = 'the terminal exposes no tv'
        return rec
    # THE TERMINAL VALUE MUST COME FROM A TERMINAL, not from wherever a key called `tv`
    # happens to sit. Measured across the book, every legitimate route carries either a
    # segment beginning `dcf` or a segment `terminal`: dcf.tv, dcf_A.tv, dcf.frame_A.tv,
    # cases.base.terminal.tv, statements.dcf_a.terminal_value. A sensitivity row carries
    # neither — and the negative control caught this by removing a study's real terminal
    # and watching the resolver find a substitute in a sensitivity table, which read as a
    # perfectly clean result. AN ABSENT ANSWER WEARING THE COSTUME OF A CLEAN ONE, one more
    # time, in the resolver rather than in the gate.
    # THE PATH MUST NAME A TERMINAL, in its container OR in its leaf. The first cut asked
    # only about the container and refused cases.A.terminal_value and
    # framings.normalisation.terminal_value — two studies whose leaf names the terminal as
    # plainly as any container could. That is a false positive of this reader's own making,
    # and [R-COC-01]'s rule applies to it: RE-POINT the test, never widen it arbitrarily.
    # What is still refused is a BARE `tv` outside any terminal container, because `tv`
    # alone is ambiguous and a sensitivity row carries one.
    _segs = tvk.split('.')
    _leaf = _segs[-1]
    if not (any(x.startswith('dcf') or x == 'terminal' for x in _segs)
            or _leaf.startswith('terminal_value')):
        rec['unreadable'] = ('the only terminal value on offer is %s, whose path names no '
                             'terminal in either its container or its leaf' % tvk)
        return rec
    rec['tv'], rec['routes']['tv'] = tv, tvk
    frame = _frame_of(tvk)
    tag = _tag_of(tvk)
    rec['frame'] = frame or '(top level)'
    rec['frame_tag'] = tag or '(none)'
    # In-frame means SAME TAG, not same container — a two-framing study spreads one frame
    # across a dcf_X, a frame_X and a bridge_X, and reading across them is exactly the
    # mixing that manufactured FERTIGLOBE's breach.
    if tag:
        inframe = {k: v for k, v in flat.items() if _tag_of(k) == tag}
    elif frame:
        inframe = {k: v for k, v in flat.items() if _frame_of(k) == frame}
    else:
        inframe = {}

    def pick(name, cands, last=False):
        getter = _last_explicit if last else None
        if inframe:
            if last:
                v, k = _last_explicit(inframe, cands)
            else:
                v, k = _resolve(inframe, cands, prefer=())
            if v is not None:
                rec[name], rec['routes'][name] = v, k
                return
        if last:
            v, k = _last_explicit(flat, cands)
        else:
            v, k = _resolve(flat, cands)
        if v is not None:
            rec[name], rec['routes'][name] = v, k
            other = _tag_of(k)
            if tag and other and other != tag:
                rec['off_frame'].append(f'{name} <- {k}  (frame {other}, not {tag})')

    for name, cands in CAND.items():
        if name != 'tv':
            pick(name, cands)
    for field in ('nopat', 'dna', 'capex', 'dwc', 'fcff'):
        pick(f'{field}_last', field, last=True)
    if 'wacc_term' not in rec:
        pick('wacc_term', 'fwd_wacc', last=True)

    # TWO IDENTITIES BEFORE DECLARING A STUDY UNREADABLE, EACH LABELLED AS DERIVED.
    # [ADDED 03-Sep-2026.] Nine of twenty-four studies read as unreadable, and inspecting
    # them one by one showed the census was looking for names rather than for QUANTITIES:
    # SCEM publishes the reinvestment rate, the return on capital, replacement-cost invested
    # capital, terminal NOPAT and the terminal value, and simply never writes down g or the
    # terminal rate — both of which follow from what it does publish, by the identities its
    # own construction is built on. Deriving them is not guessing: rr = g / ROIC is the very
    # relation [R-TERM-01] is about, and TV = NOPAT(1-rr)/(W-g) is the formula that produced
    # the number. What would be guessing is filling a gap with a neighbour's figure, and
    # that is not done anywhere here. Every derivation records its route, so a reader can
    # see which cells are read and which are reconstructed.
    if 'g' not in rec and rec.get('rr_term') is not None and rec.get('roic_term'):
        rec['g'] = rec['rr_term'] * rec['roic_term']
        rec['routes']['g'] = 'rr_term x roic_term  [derived: rr = g / ROIC]'
    if 'wacc_term' not in rec and rec.get('g') is not None \
            and rec.get('nopat_term') and rec.get('rr_term') is not None and rec.get('tv'):
        # TV = NOPAT (1 - rr) / (W - g)  =>  W = NOPAT (1 - rr) / TV + g
        rec['wacc_term'] = rec['nopat_term'] * (1.0 - rec['rr_term']) / rec['tv'] + rec['g']
        rec['routes']['wacc_term'] = ('nopat_term (1 - rr_term) / tv + g  '
                                      '[derived from the study\'s own terminal]')

    # A STUDY WITH ONE RATE FOR EVERY YEAR HAS NO TERMINAL RATE, AND THAT IS A FINDING
    # RATHER THAN AN ABSENCE. GBCO discounts a five-year forecast and a perpetuity alike at
    # 22.944% and publishes no wacc_term because there is not one to publish — which is
    # exactly the flat-rate construction [R-COC-01] was adopted to end. Reading that as
    # "unreadable" filed a defect under ignorance and hid it from the census's own totals.
    if 'wacc_term' not in rec and rec.get('g') is not None:
        v, k = _resolve(flat, ('wacc',))
        if v is not None and 0.0 < v < 1.0:
            rec['wacc_term'] = v
            rec['routes']['wacc_term'] = k + '  [FLAT RATE: this study has no terminal rate]'
            rec['flat_rate'] = ('discounts the explicit window and the perpetuity at the '
                                'same %.3f%% — the construction [R-COC-01] ends' % (100 * v))

    missing = [x for x in ('wacc_term', 'g') if x not in rec]
    if missing:
        rec['unreadable'] = 'the terminal exposes no ' + ', '.join(missing)
        return rec
    W, g, tv = rec['wacc_term'], rec['g'], rec['tv']
    if not (0.0 < W < 1.0):
        rec['unreadable'] = f'terminal rate {W} is not a rate'
        return rec
    if g >= W:
        rec['unreadable'] = f'terminal growth {g:.4f} is not below the terminal rate {W:.4f}'
        return rec

    # The numerator the published terminal actually capitalises.
    rec['fcff_term_implied'] = tv * (W - g)
    N = rec.get('nopat_term')
    if N is None and 'nopat_last' in rec:
        N = rec['nopat_last'] * (1.0 + g)
        rec['nopat_term'] = N
        rec['routes']['nopat_term'] = rec['routes']['nopat_last'] + f' x (1+g)  [derived]'
    if N is not None and N > 0:
        # A study may expose the REINVESTMENT RATE and not the return it came from. They
        # are the same statement — rr = g/ROIC — so the return is DERIVED rather than the
        # study being called unreadable. EGCH exposes reinv_rate and no roic, and without
        # this it fell out of the census entirely while carrying the construction exactly.
        if 'roic_term' not in rec and rec.get('rr_term') and g > 0:
            rec['roic_term'] = g / float(rec['rr_term'])
            rec['routes']['roic_term'] = (rec['routes'].get('rr_term', 'rr') +
                                          '  -> g/rr  [derived]')
        rec['charge'] = N - rec['fcff_term_implied']
        rec['charge_share_of_nopat'] = rec['charge'] / N
        # THE CYCLE IS COMPUTED ON THE CAPITAL BASE THE CHARGE ACTUALLY USES, which the
        # study's own terminal ROIC defines: IC = NOPAT / ROIC. Dividing by whichever ic_*
        # field happened to be present measures a different base and gives a cycle that is
        # neither 1/g nor anything else — FERTIGLOBE came out at 97 years against a real 50,
        # because its terminal ROIC is not its replacement-cost ROIC.
        #
        # And the algebra is exact: charge = NOPAT x g/ROIC = g x (NOPAT/ROIC), so
        # cycle = IC/charge = 1/g WHENEVER the construction is the reinvestment identity.
        # That makes this a clean detector rather than an estimate.
        roic = rec.get('rr_term') and rec.get('charge') and None
        if rec.get('roic_term') and rec['charge'] > 0:
            rec['ic_implied'] = N / rec['roic_term']
            rec['implied_cycle_years'] = rec['ic_implied'] / rec['charge']
            # THE BASE THE CHARGE USES AND THE BASE THE STUDY COMMITS ARE NOT ALWAYS THE
            # SAME, and the difference decides what the cycle can be used FOR. The signature
            # test is algebra on whatever base the charge uses, so it holds either way. But
            # PRICING a disclosed asset life needs the real capital, and reading the implied
            # base as though it were the committed one overstated one name's correction by
            # two thirds before this line existed. ADNOCLS agrees to (1+g) exactly — the
            # return is struck on terminal profit against a valuation-date base — while AMR
            # sets a terminal return of exactly 30.0000%, A ROUND NUMBER THAT IS A CHOICE
            # AND NOT A MEASUREMENT, against its own NOPAT/IC of 50.8%.
            if rec.get('ic'):
                rec['ic_ratio'] = rec['ic_implied'] / rec['ic']
                # TWO LEGITIMATE CONVENTIONS, and the check accepts both while NAMING which.
                # A terminal return may be struck on the terminal year's own profit (ratio
                # 1.00) or on the next year's (ratio 1+g); they differ by exactly one year of
                # growth and neither is wrong. What is not a convention is a ratio that is
                # neither — that is a return chosen against some other base.
                if abs(rec['ic_ratio'] - 1.0) < 0.02:
                    rec['base_agrees'] = True
                    rec['base_convention'] = "terminal-year profit on the committed capital"
                elif abs(rec['ic_ratio'] / (1.0 + g) - 1.0) < 0.02:
                    rec['base_agrees'] = True
                    rec['base_convention'] = "next-year profit on the committed capital"
                else:
                    rec['base_agrees'] = False
                if not rec['base_agrees']:
                    rec['base_note'] = (
                        'the terminal return is struck on a base %.2fx the committed '
                        'invested capital, so the implied cycle diagnoses the CONSTRUCTION '
                        'and the committed base is what a disclosed asset life must be '
                        'priced against' % rec['ic_ratio'])
            else:
                rec['base_note'] = ('no invested capital is committed, so a disclosed asset '
                                    'life cannot be priced from what this study publishes')
        elif rec.get('ic') and rec['charge'] > 0:
            rec['implied_cycle_years'] = rec['ic'] / rec['charge']
            rec['cycle_basis_note'] = ('computed on a committed ic_* field, not on the base '
                                       'the charge uses — the study exposes no terminal ROIC')
        rec['one_over_g'] = 1.0 / g if g > 0 else math.inf
        # the floor: zero nominal growth, maintenance at book D&A, full payout
        base = rec.get('nopat_last', N / (1.0 + g))
        rec['floor'] = base / W
        rec['tv_vs_floor'] = tv / rec['floor'] - 1.0
        rec['below_floor'] = tv < rec['floor']
    return rec


def census():
    return [read_study(d) for d in sorted(glob(os.path.join(REPO, 'engine', '*_study')))]


def _fv_at(rec, tv_new):
    """What the study's own fair value becomes at a different terminal, all else equal."""
    if not all(k in rec for k in ('df_tv', 'equity', 'fv')) or not rec['fv']:
        return None
    sh = rec['equity'] / rec['fv']
    return (rec['equity'] + (tv_new - rec['tv']) * rec['df_tv']) / sh


def report():
    rows = census()
    read = [r for r in rows if 'unreadable' not in r]
    dark = [r for r in rows if 'unreadable' in r]
    print('THE TERMINAL-VALUE CENSUS  [R-TERM-01]')
    print('   every study\'s own committed terminal, re-expressed as the charge it levies')
    print(f'   {len(rows)} study directories · {len(read)} readable · {len(dark)} not\n')

    scored = [r for r in read if 'charge' in r]
    # EVERY DIRECTORY IS ACCOUNTED FOR IN ONE OF THREE BUCKETS, AND THE THREE SUM TO THE
    # TOTAL. [ADDED 03-Sep-2026.] This printed a "readable" count and then a table of the
    # SCORED ones, and the difference appeared nowhere: on the run that widened the reader,
    # 19 read and 15 were tabulated, so GBCO and EMPOWER moved from being named as
    # unreadable to not being named at all — which is worse, because the first state is a
    # tracked gap and the second is a silent one. COUNT AGAINST A KNOWN TOTAL [R-ENF-04].
    gap = [r for r in read if 'charge' not in r]
    print(f"  {'ticker':<12}{'g':>7}{'W':>8}{'charge/NOPAT':>13}{'cycle yrs':>11}{'1/g':>7}"
          f"{'TV vs floor':>13}")
    print('  ' + '-' * 71)
    for r in sorted(scored, key=lambda r: r.get('tv_vs_floor', 9e9)):
        cyc = r.get('implied_cycle_years')
        print(f"  {r['ticker']:<12}{r['g']:>6.1%}{r['wacc_term']:>8.2%}"
              f"{r['charge_share_of_nopat']:>12.1%}"
              f"{(f'{cyc:.1f}' if cyc else '—'):>11}{r['one_over_g']:>7.1f}"
              f"{r['tv_vs_floor']:>+12.1%}"
              f"{'  BELOW ITS OWN FLOOR' if r.get('below_floor') else ''}")

    if gap:
        print(f'\n  READ BUT NOT SCORED ({len(gap)}) — the terminal resolves and the charge '
              f'it levies does not, so these sit in neither table above:')
        for r in sorted(gap, key=lambda r: r['ticker']):
            why = []
            for f in ('nopat_term', 'ic', 'tv'):
                if r.get(f) is None:
                    why.append('no ' + f)
            print(f"    {r['ticker']:<12}{r.get('g', 0):>6.1%} at "
                  f"{r.get('wacc_term', 0):>7.2%}   {', '.join(why) or 'charge not derivable'}")
    assert len(scored) + len(gap) + len(dark) == len(rows), (
        'the three buckets must account for every directory')

    flat = [r for r in read if r.get('flat_rate')]
    if flat:
        print(f'\n  ONE RATE FOR EVERY YEAR ({len(flat)}) — no terminal rate exists to '
              f'read, which is the construction [R-COC-01] ends, not an absence:')
        for r in sorted(flat, key=lambda r: r['ticker']):
            print(f"    {r['ticker']:<12}{r['flat_rate']}")

    below = [r for r in scored if r.get('below_floor')]
    print(f'\n  BELOW THE FLOOR — a terminal worth less than not investing at all: '
          f'{len(below)} of {len(scored)}')
    for r in sorted(below, key=lambda r: r['tv_vs_floor']):
        fv0, fv1 = r.get('fv'), _fv_at(r, r['floor'])
        px = f'   {fv0:.2f} -> {fv1:.2f} at the floor' if (fv0 and fv1) else ''
        print(f"    {r['ticker']:<12}{r['tv_vs_floor']:>+8.1%}{px}")

    cyc = [r for r in scored if r.get('implied_cycle_years')]
    print(f'\n  THE IMPLIED REPLACEMENT CYCLE IS 1/g, NOT AN ASSET FACT — '
          f'{len(cyc)} studies expose both:')
    for r in sorted(cyc, key=lambda r: r['implied_cycle_years']):
        d = r['implied_cycle_years'] / r['one_over_g'] - 1.0
        print(f"    {r['ticker']:<12}{r['implied_cycle_years']:>7.1f} years against 1/g of "
              f"{r['one_over_g']:>5.1f}   ({d:+.1%})")

    if dark:
        print(f'\n  NOT READABLE ({len(dark)}) — tracked, because an unreadable answer is '
              f'not a clean one [R-ENF-04]:')
        for r in dark:
            print(f"    {r['ticker']:<12}{r['unreadable']}")
    return rows


if __name__ == '__main__':
    report()
