"""SWDY -- the [R-ANCHOR-01] forecast anchor, measured rather than asserted.

Adds `forecast_anchor` to study_numbers.json. IT CHANGES NO DRIVER, NO RATE AND NO
VALUE: every figure is either read back out of the committed numbers file or derived
by an identity from two figures that are, and the record's only job is to state what
the forecast claims against what the company has just filed.

WHAT THE RATE IS. The forecast is built segment by segment -- Cables, Constructions
and infrastructure, Electrical products and digital solutions -- each on its own
margin driver, and those three aggregate to the group SEGMENT-PROFIT MARGIN, which
is what the committed path publishes as `bottomup.gp_margin` and what the model
carries forward to the corporate-load bridge. That is the rate the anchor governs.

IT IS SEGMENT PROFIT AND NOT GROSS PROFIT, and saying so is not pedantry: the key is
named `gp` and holds note 16 segment profit -- gross profit LESS selling and
distribution expenses -- while the face of the income statement carries a gross
profit on the row above. FY2025 cables segment profit is 21,016.4 against a gross
profit of 25,197.5 on that other row. A ratio between two quantities defined
differently is not evidence about either; this study's own re-issue note records a
first draft of this very comparison reaching 20.6% on the wrong basis and being
corrected. Everything below is on ONE basis, the forecast's own.

WHY THE ANCHOR IS THE REVIEWED HALF AND NOT THE AUDITED YEAR. That is the rule: a
near-term reviewed actual outranks a stale full-year rate. The study holds the
reviewed condensed interim consolidated statements for the six months ended 30 June
2026, approved for issuance on 11 August 2026, and they are the latest reviewed
period. Against the audited FY2025 year the forecast opens 1.56% relatively below
and nothing fires; against the reviewed half it opens 13.69% below and it fires.
The audited year is the flattering comparison, which is why the rule names the other
one, and the flattering one is not the one recorded here.

WHY NO MECHANISM IS NAMED, WHICH IS THE FINDING. All six of the closed list were
tested against the filings this study holds and none is supported -- the reasoning
and the measured figures are in the note, which is written by the arithmetic below
rather than typed. The gap is a HALF-AGAINST-YEAR basis difference on an issuer
whose own filed halves are 3.33 points apart, and "the latest reviewed period is a
half" is not on the closed list. An open list would let any study opt out by
inventing a reason, so nothing is invented here: the record is committed as it
measures, and the study stays on the ratchet with the reason printed.

ARITHMETIC IS THE ARBITER. Both segment tables are asserted to reproduce the
consolidated revenue line the same filing prints, and the historical corporate-load
bridge is asserted to reproduce the audited operating profit, before any of it is
used for anything.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(HERE, 'study_numbers.json')
D = json.load(open(PATH, encoding='utf-8'))
V = {k: x['value'] for k, x in D['inputs'].items()}

SEG = ('cables', 'construct', 'elecprod')
NAME = dict(cables='Cables and accessories',
            construct='Constructions and infrastructure',
            elecprod='Electrical products and digital solutions')


def tot(block):
    return sum(float(block[s]) for s in SEG)


# ---- the periods, all on the note-5-3 external revenue / note-16 segment profit
#      basis the forecast is built on --------------------------------------------
R_H126, P_H126 = tot(V['seg_rev_h1_26']), tot(V['seg_profit_h1_26'])
R_H125, P_H125 = tot(V['seg_rev_h1_25']), tot(V['seg_profit_h1_25'])
R_FY25, P_FY25 = tot(V['seg_rev_hist']['FY25']), tot(V['seg_profit_hist']['FY25'])

# ARITHMETIC IS THE ARBITER -- each segment table must reproduce the consolidated
# revenue line its own filing prints, from its own components, before it is used.
assert abs(R_H126 - float(V['h1_26_rev'])) < 1.0, ('H1-2026 segments do not sum to the '
                                                   'reviewed revenue line', R_H126)
assert abs(R_FY25 - float(V['rev_fy25'])) < 1.0, ('FY2025 segments do not sum to the '
                                                  'audited revenue line', R_FY25)
# and the corporate-load bridge must reproduce the audited operating profit
_ebit_fy25 = P_FY25 + float(V['seg_unalloc_fy25']) - float(V['corp_load_hist']['FY25']) * R_FY25
assert abs(_ebit_fy25 - float(V['op_fy25'])) < 1.0, ('the FY2025 bridge does not reach the '
                                                     'audited operating profit', _ebit_fy25)

M_H126 = P_H126 / R_H126                       # THE LATEST REVIEWED RATE
M_H125 = P_H125 / R_H125
M_FY25 = P_FY25 / R_FY25
# the same half on the wider basis, published so the basis choice cannot be accused of
# sizing the breach: including the unallocated column makes the gap SMALLER, and the
# narrower like-for-like figure is the one recorded.
M_H126_INCL = (P_H126 + float(V['seg_unalloc_h1_26'])) / R_H126

# ---- the forecast, read back out of the committed numbers file -----------------
FPATH = [float(x) for x in D['bottomup']['gp_margin']]
FIRST = FPATH[0]
R_FY26, P_FY26 = float(D['fcst']['rev'][0]), float(D['bottomup']['gp'][0])
assert abs(P_FY26 / R_FY26 - FIRST) < 1e-12, 'the committed path is not this build'

GAP = FIRST - M_H126
GAP_REL = GAP / abs(M_H126)
GAP_REL_FY25 = (FIRST - M_FY25) / abs(M_FY25)
PATH_DROP_REL = (min(FPATH) - FPATH[0]) / abs(FPATH[0])

# ---- WHERE THE CLAIM ACTUALLY SITS --------------------------------------------
# The first forecast year already CONTAINS the filed half, so the only part of it
# still in question is the half not yet filed. Both second halves are derived by the
# same identity -- a full year less its own filed first half, on one basis -- and are
# LABELLED derived, because an identity is not an assumption and the label is what
# keeps the two apart.
R_H225, P_H225 = R_FY25 - R_H125, P_FY25 - P_H125
M_H225 = P_H225 / R_H225
R_H226, P_H226 = R_FY26 - R_H126, P_FY26 - P_H126
M_H226 = P_H226 / R_H226

REL_H1 = (M_H126 - M_H125) / abs(M_H125)       # filed half against filed half
REL_H2 = (M_H226 - M_H225) / abs(M_H225)       # implied half against filed half
REL_FY = (FIRST - M_FY25) / abs(M_FY25)        # forecast year against audited year
SEASON_FILED = M_H225 / M_H125                 # the company's own filed H2:H1 shape
SEASON_FCST = M_H226 / M_H126

# ---- the closed list, tested one by one ----------------------------------------
# (1) mix. Held constant so that mix is not doing the work: the forecast rates
# applied to the reviewed half's own revenue mix.
MIXHELD = sum(float(V['seg_rev_h1_26'][s]) * float(V[s + '_margin'][0]) for s in SEG) / R_H126
MIX_REL = (MIXHELD - M_H126) / abs(M_H126)
MIX_SHARE = FIRST - MIXHELD                    # how much of the gap mix carries
# and the direction the filings actually show, on the highest-margin segment
EP_SHARE = {y: float(V['seg_rev_hist'][y]['elecprod']) / tot(V['seg_rev_hist'][y])
            for y in ('FY23', 'FY24', 'FY25')}
EP_SHARE['H1-2026'] = float(V['seg_rev_h1_26']['elecprod']) / R_H126
EP_M_H126 = float(V['seg_profit_h1_26']['elecprod']) / float(V['seg_rev_h1_26']['elecprod'])

# (2) input cost outpacing price. The group measure the rule's own worked cases use.
CUR_H125, CUR_H126 = 1.0 - M_H125, 1.0 - M_H126
CUR_DRIFT = CUR_H126 - CUR_H125
# what the model actually projects: every segment margin flat for five years, and the
# three measured half-on-half directions disagreeing with each other
SEG_MOVE = {s: (float(V['seg_profit_h1_26'][s]) / float(V['seg_rev_h1_26'][s])
                - float(V['seg_profit_h1_25'][s]) / float(V['seg_rev_h1_25'][s]))
            for s in SEG}
SEG_FLAT = {s: (max(V[s + '_margin']) - min(V[s + '_margin'])) for s in SEG}

# (3) a one-off inside the latest reviewed period. One is disclosed and it sits
# outside this rate entirely.
ONEOFF = float(V['h1_26_assoc_oneoff'])

D['forecast_anchor'] = dict(
    rate_name='group segment-profit margin',
    latest_reviewed_period='H1-2026, six months ended 30 June 2026, reviewed condensed '
                           'interim consolidated statements',
    latest_reviewed_date='2026-06-30',
    latest_reviewed_rate=M_H126,
    first_forecast_rate=FIRST,
    forecast_path=FPATH,
    note=(
        "MEASURED, NOT ASSERTED, AND NO MECHANISM IS NAMED BECAUSE NONE ON THE CLOSED "
        "LIST IS SUPPORTED BY THIS COMPANY'S FILINGS. The rate is the group "
        "segment-profit margin -- note 16 segment profit, which is gross profit less "
        "selling and distribution expenses, over the note 5-3 external revenue the "
        "same filings disclose -- and it is the basis the forecast is built on, not "
        "the gross-profit row above it. The forecast opens at %.4f%% against a "
        "reviewed half of %.4f%%, %.4f points and %.2f%% relatively below, and it "
        "fires. On the wider basis that includes the unallocated column the half runs "
        "%.4f%% and the gap is %.2f%%; the narrower like-for-like figure is recorded "
        "because it is the one the forecast is comparable to and because it makes the "
        "breach LARGER rather than smaller. Against the audited FY2025 year of %.4f%% "
        "the forecast opens only %.2f%% low and nothing would fire -- the stale "
        "full-year rate is the flattering comparison, which is why it is not the one "
        "this record is struck on. "
        "THE PATH DOES NOT DECLINE: %s, so the opening year is the low point of the "
        "explicit window and the second clause does not fire. "
        "WHERE THE CLAIM ACTUALLY SITS, AND IT IS THE REASON NO MECHANISM FITS. The "
        "first forecast year already CONTAINS the filed half, so the only part still "
        "in question is the half not yet filed, and every like-for-like comparison "
        "this company's own filings permit is inside the tolerance: the filed half "
        "against its own filed comparative half, %.4f%% against %.4f%%, %+.2f%%; the "
        "implied second half against the company's own filed second half a year "
        "earlier, %.4f%% against %.4f%%, %+.2f%%; the forecast year against the "
        "audited year, %+.2f%%. What separates them is that THE HALVES ARE NOT ALIKE: "
        "on its own filed figures this issuer earned %.4f%% in the first half of "
        "FY2025 and %.4f%% in the second, %.4f points apart, the second half running "
        "at %.4fx the first, and the forecast carries essentially that same shape at "
        "%.4fx. Both second halves are DERIVED by one identity -- a full year less "
        "its own filed first half, on a single basis -- and are labelled derived "
        "rather than presented as filed periods. So the %.2f%% this record reports is "
        "a half measured against a year on an issuer with a %.4f-point seasonal step, "
        "and 'the latest reviewed period is a half' is not on the closed list. "
        "THE SIX MECHANISMS, TESTED AND REFUSED ONE BY ONE. (a) MIX. Holding mix "
        "constant -- the forecast rates applied to the reviewed half's own revenue "
        "mix -- gives %.4f%% against the realised %.4f%%, so mix carries %.4f points "
        "of the %.4f-point gap and %.2f%% relative survives it. It is refused anyway "
        "because the direction is wrong in the filings: the highest-margin segment, "
        "Electrical products and digital solutions at %.4f%% in the half, has been "
        "GAINING share -- %.2f%% of revenue in FY2023, %.2f%% in FY2024, %.2f%% in "
        "FY2025, %.2f%% in the reviewed half -- so a disclosed shift toward lower "
        "margin is contradicted by the record. (b) INPUT COST OUTPACING PRICE. This "
        "is the candidate that would have cleared the check and it is the one worth "
        "recording as refused: group cost per unit of revenue rose from %.4f%% to "
        "%.4f%% across the two comparable halves, +%.4f points, so the direction test "
        "would pass. It is not claimed, for three reasons that are facts about the "
        "model rather than opinions about the company. The model projects no such "
        "drift at all -- all three segment margins are held FLAT across the whole "
        "explicit window, with a spread of %.6f, %.6f and %.6f between their highest "
        "and lowest forecast years. The three measured half-on-half directions "
        "DISAGREE with each other -- %s %+.4f points, %s %+.4f points, %s %+.4f "
        "points -- so there is no group trend to project and the study's own driver "
        "registration says so. And the measured drift is %.4f points of revenue "
        "against the %.4f points the claim would have to carry, %.1f%% of it. A "
        "mechanism the model does not run, asserted on a measurement seven per cent "
        "the size of the step it is offered to explain, is the assumption wearing "
        "one. (c) A ONE-OFF IN THE LATEST REVIEWED PERIOD. One is disclosed and "
        "quantified -- EGP %.3fmn of gains on sale and revaluation of "
        "equity-accounted investees, note 20-3, on its own line with no comparative "
        "-- and it sits on the associate line BELOW operating profit, outside segment "
        "profit entirely, so it moves this rate by nothing. The disclosure exists and "
        "does not establish the mechanism. (d) CONTRACTED PRICE STEP-DOWN, (e) "
        "SUBSIDY OR LEVY WITHDRAWAL, (f) CAPACITY COMMISSIONING DRAG: nothing in the "
        "filings this study holds discloses any of them. No order book or backlog "
        "figure is disclosed anywhere in the audited statements or either interim, "
        "which is the same absence the constructions growth driver already records. "
        "WHAT THIS RECORD IS THEREFORE SAYING: the forecast is not declining away "
        "from what this company has filed -- on the company's own halves it is "
        "roughly flat, in both of them -- and it cannot be cleared through this gate, "
        "because the arithmetic the gap needs is seasonal and the list is closed. "
        "That is reported rather than resolved: the list is not extended from inside "
        "a study."
        % (100 * FIRST, 100 * M_H126, -100 * GAP, -100 * GAP_REL,
           100 * M_H126_INCL, -100 * (FIRST - M_H126_INCL) / abs(M_H126_INCL),
           100 * M_FY25, -100 * GAP_REL_FY25,
           ' -> '.join('%.4f%%' % (100 * m) for m in FPATH),
           100 * M_H126, 100 * M_H125, 100 * REL_H1,
           100 * M_H226, 100 * M_H225, 100 * REL_H2,
           100 * REL_FY,
           100 * M_H125, 100 * M_H225, 100 * (M_H125 - M_H225), SEASON_FILED, SEASON_FCST,
           -100 * GAP_REL, 100 * (M_H125 - M_H225),
           100 * MIXHELD, 100 * M_H126, -100 * MIX_SHARE, -100 * GAP, -100 * MIX_REL,
           100 * EP_M_H126, 100 * EP_SHARE['FY23'], 100 * EP_SHARE['FY24'],
           100 * EP_SHARE['FY25'], 100 * EP_SHARE['H1-2026'],
           100 * CUR_H125, 100 * CUR_H126, 100 * CUR_DRIFT,
           SEG_FLAT['cables'], SEG_FLAT['construct'], SEG_FLAT['elecprod'],
           NAME['cables'], 100 * SEG_MOVE['cables'],
           NAME['construct'], 100 * SEG_MOVE['construct'],
           NAME['elecprod'], 100 * SEG_MOVE['elecprod'],
           100 * CUR_DRIFT, -100 * GAP, 100 * CUR_DRIFT / (-100 * GAP) * 100,
           ONEOFF)),
)

with open(PATH, 'w', encoding='utf-8') as f:
    json.dump(D, f, indent=1, default=float)

print('forecast_anchor written for SWDY')
print('  rate                    group segment-profit margin (note 16 / note 5-3)')
print('  latest reviewed         H1-2026 (30-Jun-2026, reviewed)   %.6f' % M_H126)
print('  first forecast year     FY2026E                           %.6f' % FIRST)
print('  gap                     %+.6f  (%+.4f%% relative)' % (GAP, 100 * GAP_REL))
print('  path                    %s  (drop from opening %+.4f%%)'
      % (' -> '.join('%.4f%%' % (100 * m) for m in FPATH), 100 * PATH_DROP_REL))
print('  vs audited FY2025       %.6f  (%+.4f%% relative)' % (M_FY25, 100 * GAP_REL_FY25))
print('  like-for-like halves    H1 %+.4f%%   implied H2 %+.4f%%   FY %+.4f%%'
      % (100 * REL_H1, 100 * REL_H2, 100 * REL_FY))
print('  filed seasonal step     H1-2025 %.6f  H2-2025 %.6f (derived)  ratio %.6f'
      % (M_H125, M_H225, SEASON_FILED))
print('  mechanism               NONE - no closed-list mechanism is supported')
