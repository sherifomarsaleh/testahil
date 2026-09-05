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
_LIVES_F = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'disclosed_lives.json')
_LIVES = json.load(open(_LIVES_F)) if os.path.exists(_LIVES_F) else {}

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


# A BRANCH THAT IS NOT THE BASE ANSWER MUST NEVER SUPPLY ONE [ADDED 05-Sep-2026].
# ELEC found this. Its terminal growth is 0.05, committed in its own four-field input
# register as inputs.g_term.value; the resolver could not see that shape (see below) and
# fell through the alias list to the bare name `g`, which it found at
# `scenarios.bear.knobs.g` — the BEAR CASE's knob, 0.04. Everything downstream was then
# computed on a growth rate the study does not publish: 1/g reads 25.0 years instead of
# 20.0, and the implied terminal cash flow misses the study's own by 10%.
#
# A resolver that guesses is the defect [R-ENF-04] closes, and this file's own comment on
# the `g` aliases says exactly that. Falling back to ANY leaf with the right final segment
# is the guess; what makes it dangerous is that a sensitivity grid, a bear case and a
# scenario knob all carry the same field names as the base answer and are numerically
# plausible, so the wrong one reads as clean. These segments are refused in the FALLBACK
# search only — a study that genuinely keys its base terminal under a container named
# below would be found by the qualified pass first.
NOT_THE_BASE = ('bear', 'bull', 'downside', 'upside', 'low', 'high', 'scenario',
                'scenarios', 'sens', 'sensitivity', 'grid', 'alt', 'alternative',
                'stress', 'adversarial', 'halt', 'placebo')


def _resolve(flat, names, prefer=DCF_HOLDERS):
    """First candidate present, preferring a DCF-ish container. Returns (value, key)."""
    for n in names:
        # a container-qualified hit first, so dcf.tv beats sensitivity.rows[3].tv
        for pre in prefer:
            k = f'{pre}.{n}'
            if k in flat:
                return flat[k], k
            # THE FOUR-FIELD INPUT REGISTER IS A DICT, NOT A NUMBER [ADDED 05-Sep-2026].
            # Depth-bar standard 2 requires every input to carry value/source/date/layer,
            # so a study that commits its terminal growth properly stores
            # {"value": 0.05, "source": ..., "date": ..., "ring": ...} and _flat() emits
            # `inputs.g_term.value`, whose final segment is `value`. The resolver looked
            # for a leaf named `g_term` and there is none — SO THE BETTER-DOCUMENTED A
            # STUDY'S INPUT WAS, THE LESS VISIBLE IT WAS TO THIS READER, which is exactly
            # backwards.
            if f'{pre}.{n}.value' in flat:
                return flat[f'{pre}.{n}.value'], f'{pre}.{n}.value'
        # then any leaf whose FINAL segment is exactly this name, or a four-field
        # register entry of that name — never one inside a branch that is not the base
        hits = [k for k in flat
                if (k.split('.')[-1] == n
                    or (k.endswith('.value') and k.split('.')[-2] == n))
                and not any(seg in NOT_THE_BASE for seg in k.split('.')[:-1])]
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


def numbers_file(d):
    """A study's committed numbers file, however that study happens to name it.

    THE HOUSE NAME IS study_numbers.json AND THREE OF TWENTY-FOUR STUDIES DO NOT USE IT.
    This census resolved the name literally and reported those three "no committed numbers
    file" — an ABSENT answer wearing a clean one's costume [R-ENF-04], and worse than a
    failure because a study reported unreadable is a study nobody looks at again. Every
    other gate in this repository already globs; this one did not, and the divergence was
    invisible because the studies it missed were also missing from everything the census
    feeds. Preference order first so the house name always wins where both exist.
    """
    for name in ('study_numbers.json', 'numbers.json'):
        p = os.path.join(d, name)
        if os.path.exists(p):
            return p
    cands = sorted(g for g in glob(os.path.join(d, '*.json'))
                   if 'numbers' in os.path.basename(g).lower())
    return cands[0] if cands else None


def read_study(d):
    """One study's terminal, read from ONE frame, or a stated reason it cannot be read."""
    tk = os.path.basename(d)[:-6].upper()
    f = numbers_file(d)
    rec = {'ticker': tk, 'dir': os.path.relpath(d, REPO), 'routes': {}, 'off_frame': []}
    if not f:
        rec['unreadable'] = 'no committed numbers file'
        return rec
    try:
        n = json.load(open(f))
    except Exception as e:
        rec['unreadable'] = f'numbers file will not parse: {e}'
        return rec
    flat = _flat(n)
    # THE COMMITTED TERMINAL RECORD, WHEREVER IT SITS. A study rebuilt through the
    # sanctioned builder commits one; it may be at the top level or inside the frame
    # that owns the terminal, and reading only one depth is the flat-resolver
    # assumption this file exists to avoid.
    _found = []

    def _walk(o):
        if not isinstance(o, dict):
            return
        for _k, _v in o.items():
            # THE SANCTIONED TERMINAL IS RECOGNISED BY WHAT IT IS, NOT BY THE KEY IT
            # HAPPENS TO SIT UNDER [WIDENED 05-Sep-2026]. terminal_value.build() returns a
            # block stamped rule='R-TERM-01' carrying its inputs and the disclosed life;
            # most studies commit it as `terminal_record`, and EMPOWER commits two of them
            # as `terminal_stage1` and `terminal_stage2` because its terminal is staged.
            # Matching only the KEY made a correctly-rebuilt study read as though it had
            # never been rebuilt — the same defect as a scrub keyed on a word list, one
            # level down.
            if (isinstance(_v, dict) and _v.get('inputs')
                    and (_k == 'terminal_record'
                         or (_v.get('rule') == 'R-TERM-01'
                             and (_v.get('inputs') or {}).get('useful_life_years')))):
                _found.append(_v)
            else:
                _walk(_v)
    _walk(n)
    # A TWO-FRAMING STUDY COMMITS ONE RECORD PER FRAMING AND THAT IS NOT AMBIGUITY.
    # A first cut required exactly one and returned nothing on the first two-sided
    # study it met, so that study kept reporting the metric this change exists to
    # stop reporting. WHAT MATTERS IS WHETHER THE RECORDS AGREE ON THE FIGURE BEING
    # READ, not how many there are: the framings differ in prices and volumes, not in
    # how long a plant lasts. Where they disagree, that IS ambiguity and nothing is
    # read — the census does not pick a life on a study's behalf.
    if _found:
        _lives = {round(float((x.get('inputs') or {}).get('useful_life_years') or 0), 6)
                  for x in _found}
        rec['_terminal_record'] = _found[0] if len(_lives) == 1 else None
        if len(_lives) > 1:
            rec['cycle_basis_note'] = ('this study commits %d terminal records and they '
                                       'disagree on the useful life, so none is read'
                                       % len(_found))
    else:
        rec['_terminal_record'] = None

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
    # A STUDY MAY EXPOSE THE REINVESTMENT RATE AND THE TERMINAL CASH FLOW AND NOT THE
    # PROFIT BETWEEN THEM [ADDED 05-Sep-2026]. The reinvestment construction is
    # fcff = NOPAT x (1 - rr), so the profit is the cash flow grossed back up — an
    # identity on the study's OWN terminal, not a proxy, and strictly better than the
    # nopat_last route above, which is why it is tried only when that one found nothing
    # and can therefore change no study that already scores.
    #
    # ELEC is why it exists. Its terminal is the retired identity in plain sight —
    # roic_T = nop_T/ic_T, rr_T = g/roic_T, tv = nop_T(1+g)(1-rr_T)/(W-g) — and the
    # census could not score the charge, so the 1/g gate reported "no new terminal
    # carries the construction" while that one did. A GATE BLIND TO THE EXACT THING IT
    # EXISTS TO FIND IS THE [R-ENF-04] FAILURE IN ITS USUAL COSTUME.
    # NOT ON A TERMINAL THAT HAS ALREADY BEEN CORRECTED. A study rebuilt through
    # terminal_value.py keeps its retired construction beside the new one for the record —
    # EMPOWER commits `tv_retired` alongside its staged R-TERM-01 terminals — so its
    # `rr_term` describes the construction that was RETIRED. Grossing the corrected cash
    # flow up by a retired reinvestment rate mixes the two and manufactures a 1/g reading
    # on a study that no longer carries one. The first draft of this derivation did
    # exactly that and flagged a correctly-rebuilt name.
    if N is None and rec.get('rr_term') is not None and not rec.get('_terminal_record'):
        _rr = float(rec['rr_term'])
        if 0.0 <= _rr < 1.0 and rec['fcff_term_implied'] > 0:
            N = rec['fcff_term_implied'] / (1.0 - _rr)
            rec['nopat_term'] = N
            rec['routes']['nopat_term'] = (
                'tv (W - g) / (1 - %s)  [derived: fcff = NOPAT (1 - rr)]'
                % rec['routes'].get('rr_term', 'rr'))
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
        # A CORRECTED TERMINAL IS NOT MEASURED BY THIS METRIC, and reporting it as
        # though it were makes a rebuilt study look WORSE than the one it replaced.
        # The cycle above is IC/charge, which equals 1/g exactly under the retired
        # reinvestment identity — that is what makes it a clean DETECTOR of that
        # construction. The corrected construction charges maintenance GROSS at
        # replacement cost and ADDS BOOK D&A BACK, so its net charge is small by
        # design and IC/charge comes out far LONGER than the life it actually charges
        # maintenance over. Measured on the first name rebuilt: the census read 69.3
        # years against a life of 22.04 committed in the study's own record.
        #
        # This is [R-TERM-01 CLAUSE TWO CORRECTED] one layer down — the same mistake
        # of reading a ratio built for one construction as a fact about another. Where
        # a study COMMITS its terminal, the committed life is what is reported and the
        # basis says so.
        # TWO QUANTITIES, TWO FIELDS — and a first pass put them in one, which broke
        # the detector this whole file exists to be. Overwriting implied_cycle_years
        # with the committed life stopped the signature test firing on a terminal put
        # BACK onto g x IC, and the negative control caught it on the case labelled
        # "the one that matters". THE DETECTOR MUST KEEP COMPUTING IC/charge, because
        # that ratio equalling 1/g IS the algebra that identifies the retired identity;
        # what the committed life changes is only what a READER should be shown.
        _tr = (rec.get('_terminal_record') or {})
        _life = (_tr.get('inputs') or {}).get('useful_life_years')
        if _life:
            rec['committed_life_years'] = float(_life)
            rec['corrected_terminal'] = True
            rec['cycle_basis_note'] = ('IC/charge is kept as the detector; the life '
                                       'REPORTED is the one this study commits through '
                                       'the sanctioned builder, because IC/charge is '
                                       'net of a book-D&A add-back on a corrected '
                                       'terminal and means something else there')
        rec['one_over_g'] = 1.0 / g if g > 0 else math.inf
        # the floor: zero nominal growth, maintenance at book D&A, full payout
        base = rec.get('nopat_last', N / (1.0 + g))
        rec['floor'] = base / W
        rec['tv_vs_floor'] = tv / rec['floor'] - 1.0
        rec['below_floor'] = tv < rec['floor']
    return rec


def census():
    return [read_study(d) for d in sorted(glob(os.path.join(REPO, 'engine', '*_study')))]


def disclosed_life(ticker):
    """THE DISCLOSED USEFUL LIFE FOR A NAME, FROM BOTH PLACES THAT CARRY IT.

    Two sources, and reading only one produces a false negative that has already
    happened once: ARCC read "not sourced" on this census's first run while carrying
    a 20-year life quoted to its own audited note, because a study rebuilt through
    terminal_value.py commits the life under terminal_record.inputs and the flat
    resolver never looks there.

    Returns one of:
      (life, None, source)      a study has COMMITTED a single life to its own record
      (lo, hi, source)          a life is SOURCED into disclosed_lives.json as the
                                band its policy note actually discloses, not yet
                                collapsed — that is a different state from committed,
                                and the one that says the next rebuild can proceed
      (None, None, None)        genuinely not sourced

    THE BAND IS NOT COLLAPSED HERE. A policy note gives a range per asset class and
    picking one figure out of it is this desk choosing a life under cover of a
    citation, which [R-TERM-01] refuses outright (SIGCM clause 1). The weighted life
    a terminal needs comes from the property, plant and equipment note's own
    composition — a further sourcing step, and the caller is told which state it has.
    """
    nf = numbers_file(os.path.join(REPO, 'engine', '%s_study' % ticker.lower()))
    if nf:
        try:
            rec = (json.load(open(nf)).get('terminal_record') or {}).get('inputs', {})
            v = rec.get('useful_life_years')
            if isinstance(v, (int, float)) and v > 0:
                return float(v), None, (rec.get('useful_life_source')
                                        or 'the study\'s own committed terminal record')
        except Exception:                                            # noqa: BLE001
            pass
    band = (_LIVES.get('lives') or {}).get(ticker)
    if band and band.get('shortest_years') and band.get('longest_years'):
        return (float(band['shortest_years']), float(band['longest_years']),
                band.get('source') or 'disclosed_lives.json')
    return None, None, None


def _fv_at(rec, tv_new):
    """What the study's own fair value becomes at a different terminal, all else equal.

    THIS HELPER COULD NEVER FIRE AND NOTHING SAID SO. It required a `df_tv` key that
    read_study does not set and never has, so it returned None for every record in
    the book — a function that looks like an instrument and answers nothing, which
    is [R-ENF-04]'s own shape one level down: an absent answer wearing the costume
    of a clean one. Found 04-Sep-2026 by a caller that wanted it.

    The factor is exactly pv_tv / tv and is DERIVED rather than demanded. A record
    exposing a terminal and its present value already carries it; requiring a third
    key nobody writes is asking the record to repeat itself.
    """
    for k in ('tv', 'pv_tv', 'equity', 'fv'):
        if not rec.get(k):
            return None
    df = rec['pv_tv'] / rec['tv']
    return (rec['equity'] + (tv_new - rec['tv']) * df) / (rec['equity'] / rec['fv'])


def implied_lives():
    """EVERY IMPLIED ASSET LIFE A MODEL CARRIES, PRINTED SIDE BY SIDE. No pricing claim.

    A model states an asset life in three places without ever writing one down, and
    [R-TERM-01]'s worked case found the three disagreeing by 2.8x inside one document:

      the TERMINAL charge      g x IC gives a replacement cycle of 1/g
      the EXPLICIT window      its own terminal-year capex against the same IC
      the ACCOUNTING POLICIES  the company's own disclosed useful life

    Only the third is a fact about the asset. This prints the first two for every readable
    terminal, because both come from figures a study already publishes; the third has to be
    sourced from that company's own note, one name at a time, and is quoted here only where
    a study has committed it.

    WHY THIS FUNCTION DOES NOT PRICE THE CORRECTION, AND THE REASON IS THE INTERESTING PART.
    [R-TERM-01] names TWO errors — the charge, and a terminal that never adds book D&A back
    though NOPAT is already net of it — and it is tempting to price the SECOND alone,
    because it needs nothing sourced: add book D&A to the published terminal and see what
    moves. A first draft of this module did exactly that and reported the pooled terminal
    rising 69.6%. IT IS WRONG, AND IT IS WRONG IN A WAY THAT LOOKS LIKE ARITHMETIC.

    g x IC IS A NET INVESTMENT FIGURE — the new capital needed to grow at g — so a
    construction charging it has ALREADY netted depreciation, and adding book D&A on top
    double-counts. The corrected construction charges maintenance GROSS, at replacement
    cost over a disclosed life, which is why it must add book D&A back first. The two
    charges are on different bases and the halves do not separate. Checked against the one
    worked case rather than reasoned about: on ARCC the add-back-alone gives 2,445.3
    against the module's own 3,310.1, 26% short.

    THE GENERAL POINT, WHICH IS NOT ABOUT DEPRECIATION: two corrections to one formula are
    not two independent corrections when they sit on different bases. Pricing one of them
    with the other left at its old value produces a number that is neither the old
    construction nor the new one, and it will look perfectly reasonable.
    """
    rows = [r for r in census() if 'charge' in r and r.get('g')]
    if not rows:
        raise SystemExit('no readable terminal exposes a charge — an empty result is not a '
                         'clean result [R-ENF-04]')
    print('\n  WHAT EACH TERMINAL CHARGES, AGAINST WHAT ITS OWN ACCOUNTS DEPRECIATE')
    print('  {:<12}{:>9}{:>12}{:>12}{:>12}   {}'.format(
        'ticker', '1/g', 'charge', 'book D&A', 'charge/D&A', 'disclosed life'))
    print('  ' + '-' * 76)
    under = []
    for r in sorted(rows, key=lambda r: r['ticker']):
        dna, ch = r.get('dna_last'), r['charge']
        ratio = (ch / dna) if dna else None
        if ratio is not None and ratio < 1.0:
            under.append(r['ticker'])
        # THE DISCLOSED LIFE IS READ FROM THE STUDY'S OWN FILE, not from the census
        # record, because a study that has been rebuilt through terminal_value.py commits
        # it under terminal_record.inputs and the census's flat resolver never looks there.
        # ARCC read 'not sourced' on the first run while carrying a 20-year life quoted to
        # its own audited note — the census reporting a gap that had already been closed.
        lo_l, hi_l, _src = disclosed_life(r['ticker'])
        if lo_l is None:
            disc = None
        elif hi_l is None:
            disc = lo_l                       # a study has committed one life
        else:
            disc = 'sourced %g-%g yrs' % (lo_l, hi_l)
        print('  {:<12}{:>9.1f}{:>12,.0f}{:>12}{:>12}   {}'.format(
            r['ticker'], 1.0 / r['g'], ch,
            ('{:,.0f}'.format(dna)) if dna else '—',
            ('%.2fx' % ratio) if ratio is not None else '—',
            (('%.0f yrs' % disc) if isinstance(disc, (int, float))
             else (disc or 'not sourced'))))
    print('\n    1/g IS A FACT ABOUT A CURRENCY, NOT ABOUT AN ASSET: 14.3 years at a 7%')
    print('    terminal inflation and 66.7 at 1.5%, so the same plant is charged four and')
    print('    a half times as hard for being in Egypt rather than the Emirates.')
    print()
    print('    THIS RATIO IS A FLAG, NOT AN INFERENCE, AND THAT IS A CORRECTION [04-Sep].')
    print('    It read: a terminal charging LESS than its own book depreciation cannot be')
    print('    maintaining the asset base, since book depreciation sits on HISTORICAL cost')
    print('    and replacement costs more — so those terminals are over-valued. THE FIRST')
    print('    NAME ACTUALLY REBUILT DISPROVED IT: the correction RAISED that value by about')
    print('    5%, on a name reading 0.26x here.')
    print()
    print('    THE TWO FIGURES ARE NOT LIKE FOR LIKE. The retired charge is g x IC — a NET')
    print('    growth charge on an IMPLIED capital base (nopat_term / a blended terminal')
    print('    ROIC), with maintenance assumed equal to depreciation and cancelled out of')
    print('    the arithmetic entirely. Book D&A is a GROSS charge on the historical base.')
    print('    The corrected construction charges maintenance GROSS at replacement cost and')
    print('    ADDS BOOK D&A BACK, so what decides the sign is the wedge between those two')
    print('    minus the retired growth charge — and on the worked case replacement cost ran')
    print('    only 16% above book depreciation while the implied base was HALF the')
    print('    replacement base. Both differences push the same way and neither is visible')
    print('    in this column.')
    print()
    print('    SO THE SIGN IS MEASURED PER NAME, NEVER READ OFF THIS RATIO. What the ratio')
    print('    does is flag a terminal whose charge is worth rebuilding. On this book %d of %d'
          % (len(under), len([r for r in rows if r.get('dna_last')])))
    print('    charge less than their own book depreciation: %s.'
          % ', '.join(under))
    return rows


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
        cyc = r.get('committed_life_years') or r.get('implied_cycle_years')
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
    # A CORRECTED TERMINAL DOES NOT BELONG IN THIS COMPARISON. The section exists to
    # show IC/charge landing exactly on 1/g, which is the signature of the retired
    # identity. On a rebuilt terminal IC/charge is net of a book-D&A add-back and lands
    # wherever it lands, so printing it beside 1/g invites the reader to compare two
    # numbers that mean different things — and on the first rebuilt name it read 69.3
    # against 50.0, which looks like the rebuild made matters worse and is not what
    # happened. They are listed separately with the life they actually commit.
    _fixed = [r for r in cyc if r.get('corrected_terminal')]
    cyc = [r for r in cyc if not r.get('corrected_terminal')]
    for r in sorted(cyc, key=lambda r: r['implied_cycle_years']):
        d = r['implied_cycle_years'] / r['one_over_g'] - 1.0
        print(f"    {r['ticker']:<12}{r['implied_cycle_years']:>7.1f} years against 1/g of "
              f"{r['one_over_g']:>5.1f}   ({d:+.1%})")
    if _fixed:
        print('\n    REBUILT THROUGH THE SANCTIONED BUILDER — the life each COMMITS, and')
        print('    IC/charge is not comparable to 1/g on these:')
        for r in sorted(_fixed, key=lambda r: r['committed_life_years']):
            print('      %-12s %5.1f years committed   (IC/charge reads %.1f, a net '
                  'figure)' % (r['ticker'], r['committed_life_years'],
                               r['implied_cycle_years']))

    if dark:
        print(f'\n  NOT READABLE ({len(dark)}) — tracked, because an unreadable answer is '
              f'not a clean one [R-ENF-04]:')
        for r in dark:
            print(f"    {r['ticker']:<12}{r['unreadable']}")
    return rows


if __name__ == '__main__':
    report()
    implied_lives()
