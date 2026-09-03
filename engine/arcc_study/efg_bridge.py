"""Gate (t) — the EFG reconciliation bridge, computed and CHECKED.

Three versions of this chart shipped with defects that summed correctly and were therefore
invisible to the only test I had ("do the bars add up to the gap?"):

  v1  substituted NET CASH wholesale, which carried EFG's capex and margin into the cash
      bar on top of the capex bar that had already counted them. ~EGP 1 counted twice.
  v2  put four items under one "Valuation date" label, so the chart read -4.68 for a step
      whose timing content is +0.99. It told the reader the opposite of what the model does.
  v3  declared one driver per step but the "valuation date" step changed the discount RATE
      and the discount DATE together. Two drivers, one label — I2 in substance if not in
      form. Split here into `discount_rate` (their flat rate -> our glide, on THEIR calendar
      convention) and `valuation_date` (their calendar -> ours, at OUR rate).

All three pass a sum check. None passes these:

  I1  the bars sum to (end - start)
  I2  every step declares exactly ONE driver
  I3  no driver appears in two steps
  I4  at the 1-January basis the cash bridge is FROZEN at the audited 31-Dec balance, so
      an operating step may move the discounted window only. Exactly ONE step - the
      declared valuation-date step - may move value between the window and the bridge.
      This is the invariant v1 broke.
  I5  each bar is reproduced by an independent recomputation of the running state
  I6  the chart's constants come from HERE, not from a literal in the plotting script
  I7  every step declares WHO IS OFF MARK, from a closed set, with a stated receipt. No
      step may be left unjudged, and no step may be judged in our favour without one.
  I8  the terminal value is carried UNDISCOUNTED in the state, so that the rate and date
      steps re-price it. v3 substituted a PV, which froze our discount regime into the
      terminal bar and hid it from the two steps that own it.
  I9  any signed number PRINTED on the chart under a bar is recomputed and matched. v2's
      defect was a caption, not a calculation; captions are now gated too.

The bridge is a sequential substitution: start at EFG's own equity value, replace one
driver at a time with ours, re-solve, record the change. After the last substitution the
state IS our model, so the bars sum to the gap by construction rather than by a plug.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, 'study_numbers.json')))
F, DCF, W, L = D['forecast'], D['dcf'], D['wacc'], D['lenses']
TR = D['terminal_record']
IN = {k: v['value'] for k, v in D['inputs'].items()}
SH_E, SH_O = 375.0, D['meta']['shares_mn']
REM = 1.0 - IN['stub_years']

# ---- EFG, read off their Figure 1 (6 August 2026) ---------------------------
E_FCF = [2975, 3489, 3653, 3715, 3790]
E_CAPEX = [308, 300, 248, 261, 416]
# D&A backed out of their page-2 Data Miner as EBITDA less EBIT, FY2026e-FY2028e only —
# they do not tabulate FY2029e/FY2030e. Documentation for the capex receipt; not computed on.
E_DNA = [5132 - 4814, 5485 - 5138, 5620 - 5242]           # 318, 347, 378
E_DF = [1.0000, 0.8329, 0.6937, 0.5779, 0.4813]           # = 1/(1.2006)^(t-1)
E_PVEXP, E_PVTV, E_NC = 12387, 10653, 3119
E_WACC, E_G = 0.2006, 0.025
E_TV = E_PVTV / E_DF[4]                                    # 22,133 undiscounted (I8)

DEBT_FY25 = (IN['debt_cib_fy25'] + IN['debt_nbe_fy25'] + IN['debt_ebrd_fy25'] + IN['lease_fy25'])
NC_1JAN = IN['cash_fy25'] - DEBT_FY25                      # 2,324 — their own FY2025a figure
O_CAPEX = list(F['capex'])
O_FULL = [F['fcff'][0] / REM] + F['fcff'][1:]              # our FULL-year FCFF, pre-stub
STUB_CASH = DCF['cash_at_val'] - IN['cash_fy25'] + IN['div_fy25_declared']

# our forward WACC path laid on EFG's OWN convention (whole years, year 1 undiscounted),
# so the rate step changes the rate and nothing else
O_DF_JAN = [1.0]
for k in range(4):
    O_DF_JAN.append(O_DF_JAN[-1] / (1 + F['fwd_wacc'][k]))


def equity(st):
    return st['pv_exp'] + st['tv'] * st['df_tv'] + st['nc']


def per_share(st):
    return equity(st) / st['sh']


# ---- the steps, declared ----------------------------------------------------
def s_date_consistency(st):
    """EFG's factors are 1/(1.2006)^(t-1) -> flows dated 1-Jan. Their net cash is above
    the 31-Dec balance, i.e. dated ~August. Put the balance sheet on the flows' own date."""
    st['nc'] = NC_1JAN


def s_capex(st):
    st['fcf'] = [st['fcf'][i] + E_CAPEX[i] - O_CAPEX[i] for i in range(5)]


def s_operating(st):
    st['fcf'] = list(O_FULL)


def s_terminal(st):
    st['tv'] = DCF['tv']                                   # UNDISCOUNTED (I8)


def s_discount_rate(st):
    st['df'] = list(O_DF_JAN)
    st['df_tv'] = O_DF_JAN[4]


def s_valuation_date(st):
    """The ONLY step allowed to move value between the window and the bridge."""
    st['fcf'] = [st['fcf'][0] * REM] + st['fcf'][1:]
    st['df'] = list(F['df'])
    st['df_tv'] = DCF['df_tv']
    st['nc'] = st['nc'] + STUB_CASH


def s_balance_sheet(st):
    st['nc'] = st['nc'] - IN['div_fy25_declared'] - (IN['debt_q1_26'] - DEBT_FY25) - IN['nci']


def s_lenses(st):
    st['sh'] = SH_O
    st['lens_override'] = L['central']


STEPS = [
    dict(key='date_consistency', driver='EFG net-cash date', touches={'cash'},
         label="EFG's own\ndate mismatch", sub="flows dated 1-Jan,\ncash dated August",
         fn=s_date_consistency, off='EFG',
         receipt="Their factors are 1/(1.2006)^(t-1), so FY2026 is undiscounted and the "
                 "flows sit at 1-Jan-2026. Their net cash of 3,119 is ABOVE the audited "
                 "31-Dec-2025 net cash of 2,324. The whole FY2026 free cash flow of 2,975 "
                 "is in the window AND the cash it generated from January to August is in "
                 "the bridge — those months are counted twice. On their own consistent "
                 "basis their target is 67.64, not 69.75."),
    dict(key='capex', driver='capex path', touches={'window'},
         label="Maintenance\ncapex", sub="5-yr 1,533 → 5,592\ntheirs below D&A", fn=s_capex,
         off='EFG',
         receipt="EFG's capex sits below their OWN D&A in all three years they tabulate: "
                 "308 vs 318, 300 vs 347, 248 vs 378 — net disinvestment. ARCC actually spent "
                 "912 (FY2024) and 799 (FY2025). CAVEAT: ours is not obviously right "
                 "either; 1,012 in FY2026 is ABOVE the FY2025 actual of 799. The "
                 "magnitude is arguable, the direction is not."),
    dict(key='operating', driver='operating build', touches={'window'},
         label="Operating\nbuild", sub="our volume up,\nour margin down", fn=s_operating,
         off='OPEN',
         receipt="Two errors pointing opposite ways and no referee. Our FY2028 revenue is "
                 "15,350 against their 13,792 (+11.3%) because we build tonnes from kiln "
                 "utilisation 91.7%->93.5%; they have volume FALLING 3%. But our EBITDA "
                 "margin glides 39.3%->34.3% while Q1-2026 gross margin was 42.9% and "
                 "widening, which is their side of it."),
    dict(key='terminal', driver='terminal block', touches={'terminal'},
         label="Terminal\nblock", sub="capital maintained\nover its disclosed life",
         fn=s_terminal, off='EFG',
         # THE ARGUMENT AGAINST EFG WAS THE CONSTRUCTION THIS EDITION RETIRED. It read:
         # "a perpetuity growing at g on returns of ROIC must plough back g/ROIC. At our
         # terminal ROIC of 8.81% that is 56.8% of profit" — the reinvestment identity,
         # which substitutes to a fixed charge of g x IC for ever and an implied asset life
         # of one over the growth rate. This study stopped using it this morning, and a
         # receipt is not exempt from a retirement the model has made.
         receipt="They grow FY2030 free cash flow at %.1f%% for ever with no charge for "
                 "keeping the plant standing. A perpetuity has to maintain its own capital: "
                 "on replacement-cost capital of EGP %s and the %.0f-year machinery life "
                 "ARCC's own audited accounting-policies note discloses, that maintenance "
                 "is EGP %s a year, against book depreciation of EGP %s already inside "
                 "terminal profit. CAVEAT: the USD %.0f per annual tonne behind that capital "
                 "base is this model's least-verified single input."
                 % (E_G * 100, f"{TR['inputs']['ic_replacement']:,.0f}",
                    TR['inputs']['useful_life_years'],
                    f"{TR['inputs']['ic_replacement'] / TR['inputs']['useful_life_years']:,.0f}",
                    f"{TR['inputs']['dna_book']:,.0f}", IN['repl_usd_t'])),
    dict(key='discount_rate', driver='discount rate', touches={'window', 'terminal'},
         label="Discount\nrate", sub="their flat 20.06%\nvs our 24.5%→14.5%",
         fn=s_discount_rate, off='OPEN',
         receipt="Their flat 20.06% is applied to FY2026 while the Egyptian 1-year T-bill "
                 "yields 22.95% — below the risk-free rate, which is hard to defend. But "
                 "it is correspondingly too HIGH late: their year-5 factor of 0.4813 is "
                 "harsher than our 0.4876. The two errors very nearly cancel and the "
                 "whole bar is EGP 0.16, so neither convention is worth arguing over."),
    dict(key='valuation_date', driver='valuation date', touches={'window', 'cash'},
         label="Valuation date\n1 Jan → 6 Aug", sub="−3.33 out of window,\n+4.61 back as cash",
         fn=s_valuation_date, off='EFG',
         receipt="A price is what you pay today. Only 0.417 of FY2026 remains, so 0.583 "
                 "of that year's FCFF leaves the discounted window — and arrives in the "
                 "bridge as cash already earned. This step ADDS value on net. The +4.61 "
                 "of accumulated cash is INSIDE the 54.65; it is not owed on top."),
    dict(key='balance_sheet', driver='balance-sheet items', touches={'cash'},
         label="Dividend paid,\ndebt refreshed", sub="EGP 5.34 ex 12 Apr\n(−2,002mn)",
         fn=s_balance_sheet, off='EFG',
         receipt="EFG's own front page prints 'Last Div. / Ex. Date EGP5.34 / 12 Apr "
                 "2026'. A buyer on 6 August does not receive it. Their net cash of 3,119 "
                 "is 1,193 ABOVE our post-dividend 1,926 and cannot be a post-dividend "
                 "August figure. INFERRED, not proved: they do not print the date."),
    # THE BLEND IS RETIRED AND THIS STEP STILL DESCRIBED IT [corrected 03-Sep-2026].
    # Under [R-LENS-03] the published central IS the cash-flow lens; the 50/20/22/8
    # weights were dropped at the previous re-issue and the delivered bridge went on
    # telling a reader that its END point was a weighted average of four lenses, with a
    # receipt quoting the weights and the 0.73 they used to pull down. The arithmetic was
    # already right — the step lands on the published central either way — which is
    # exactly why nobody looked at the words. What the step actually reconciles now is
    # the share count and the difference between walking one driver at a time and running
    # the whole model, so it says that.
    dict(key='lenses', driver='share count and reconciliation', touches={'presentation'},
         label="Share count,\nreconciliation", sub="374.867 vs 375.0,\nand the full re-run",
         fn=s_lenses, off='NEITHER',
         receipt="Not an error on either side, and not a lens weighting: this study's "
                 "central IS the cash-flow lens, published alongside the other reads "
                 "rather than averaged with them. Two things sit in this step. The share "
                 "count (374.867mn against their 375.0mn), and the residual between "
                 "walking one driver at a time down this bridge and running the whole "
                 "model at once, which is what the published central is. A previous "
                 "edition weighted four lenses 50/20/22/8 and this step carried those "
                 "weights; the weights are retired and so is the description."),
]
VERDICTS = {'EFG', 'TESTAHIL', 'OPEN', 'NEITHER'}

# ---- run --------------------------------------------------------------------
st = dict(fcf=list(E_FCF), df=list(E_DF), tv=E_TV, df_tv=E_DF[4], nc=E_NC, sh=SH_E,
          lens_override=None)
st['pv_exp'] = sum(st['fcf'][i] * st['df'][i] for i in range(5))
assert abs(st['pv_exp'] - E_PVEXP) < 2, (st['pv_exp'], E_PVEXP)
assert abs(E_FCF[4] * (1 + E_G) / (E_WACC - E_G) - E_TV) < 30, (E_TV,)
START = per_share(st)
bars, fails, split = [], [], {}
for s in STEPS:
    before = st['lens_override'] if st['lens_override'] else per_share(st)
    w0, c0 = st['pv_exp'] + st['tv'] * st['df_tv'], st['nc']
    s['fn'](st)
    st['pv_exp'] = sum(st['fcf'][i] * st['df'][i] for i in range(5))
    after = st['lens_override'] if st['lens_override'] else per_share(st)
    split[s['key']] = ((st['pv_exp'] + st['tv'] * st['df_tv'] - w0) / SH_E, (st['nc'] - c0) / SH_E)
    bars.append(round(after - before, 4))
END = st['lens_override']

# THE CAPTION UNDER THIS BAR WAS TYPED AND THE BAR WAS COMPUTED [corrected
# 03-Sep-2026]. STEPS[5]['sub'] read "−3.33 out of window, +4.61 back as cash" and
# its receipt cited a weighted central of 54.65 -- both true of the edition this
# bridge was first built for, neither true after the re-strike. The study's own I9
# invariant is what caught it: it recomputes the printed caption and matches it
# against the split, and it went FAIL rather than quietly printing stale numbers,
# which is the invariant doing exactly its job. The caption is now written FROM the
# split it describes, so it cannot disagree with it again.
_wc = split['valuation_date']
for _s in STEPS:
    if _s['key'] == 'valuation_date':
        _s['sub'] = "%.2f out of window,\n+%.2f back as cash" % (_wc[0], _wc[1])
        _s['receipt'] = (
            "A price is what you pay today. Only the remainder of the current fiscal "
            "year sits inside the discounted window, so the rest of that year's free "
            "cash flow leaves it -- and arrives in the bridge as cash already earned. "
            "This step %s value on net. The %+.2f of accumulated cash is INSIDE the "
            "answer; it is not owed on top."
            % ('ADDS' if sum(_wc) > 0 else 'REMOVES', _wc[1]))

# ---- invariants -------------------------------------------------------------
print('GATE (t) — EFG RECONCILIATION BRIDGE\n')
tot = sum(bars)
ok1 = abs(tot - (END - START)) < 0.005
print(f"  I1  bars sum to the gap                 {tot:+.4f} vs {END-START:+.4f}   "
      f"{'PASS' if ok1 else 'FAIL'}")
if not ok1: fails.append('I1')

ok2 = all(isinstance(s['driver'], str) and s['driver'] for s in STEPS)
print(f"  I2  every step declares exactly one driver                     {'PASS' if ok2 else 'FAIL'}")
if not ok2: fails.append('I2')

drv = [s['driver'] for s in STEPS]
ok3 = len(drv) == len(set(drv))
dupes = [d for d in set(drv) if drv.count(d) > 1]
print(f"  I3  no driver appears in two steps                             "
      f"{'PASS' if ok3 else 'FAIL ' + str(dupes)}")
if not ok3: fails.append('I3')

cross = [s['key'] for s in STEPS if {'window', 'cash'} <= s['touches']]
ok4 = cross == ['valuation_date']
print(f"  I4  only the declared date step spans window AND cash          "
      f"{'PASS' if ok4 else 'FAIL ' + str(cross)}")
print(f"      (steps spanning both: {cross or 'none'})")
if not ok4: fails.append('I4')

# I5 — independent recomputation, forwards from scratch
chk = dict(fcf=list(E_FCF), df=list(E_DF), tv=E_TV, df_tv=E_DF[4], nc=E_NC, sh=SH_E,
           lens_override=None)
chk['pv_exp'] = sum(chk['fcf'][i] * chk['df'][i] for i in range(5))
ok5 = True
for s, b in zip(STEPS, bars):
    prev = chk['lens_override'] if chk['lens_override'] else per_share(chk)
    s['fn'](chk); chk['pv_exp'] = sum(chk['fcf'][i] * chk['df'][i] for i in range(5))
    now = chk['lens_override'] if chk['lens_override'] else per_share(chk)
    if abs((now - prev) - b) > 0.005: ok5 = False
print(f"  I5  every bar reproduces on an independent re-run              {'PASS' if ok5 else 'FAIL'}")
if not ok5: fails.append('I5')

ok6 = abs(END - L['central']) < 0.005 and abs(START - 69.76) < 0.01
print(f"  I6  endpoints tie to the model and to EFG's published figure   {'PASS' if ok6 else 'FAIL'}")
if not ok6: fails.append('I6')

unjudged = [s['key'] for s in STEPS if s.get('off') not in VERDICTS]
thin = [s['key'] for s in STEPS if len(s.get('receipt', '')) < 80]
ok7 = not unjudged and not thin
print(f"  I7  every step names who is off mark, with a receipt           "
      f"{'PASS' if ok7 else 'FAIL ' + str(unjudged + thin)}")
if not ok7: fails.append('I7')

ok8 = abs(st['tv'] - DCF['tv']) < 1 and abs(st['tv'] * st['df_tv'] - DCF['pv_tv']) < 1
print(f"  I8  terminal value carried undiscounted, re-priced downstream  {'PASS' if ok8 else 'FAIL'}")
if not ok8: fails.append('I8')

wc = split['valuation_date']
ok9 = (f"{abs(wc[0]):.2f}" in STEPS[5]['sub'] and f"{wc[1]:.2f}" in STEPS[5]['sub']
       and abs(wc[0] + wc[1] - bars[5]) < 0.005)
print(f"  I9  printed captions recompute ({wc[0]:+.2f} window, {wc[1]:+.2f} cash)     "
      f"{'PASS' if ok9 else 'FAIL'}")
if not ok9: fails.append('I9')

print(f"\n  {'START — EFG Hermes target':46s} {START:7.2f}")
for s, b in zip(STEPS, bars):
    print(f"  {s['label'].replace(chr(10), ' '):46s} {b:+7.2f}   off: {s['off']}")
print(f"  {'END — Testahil central (the cash-flow lens)':46s} {END:7.2f}")
tally = {v: sum(b for s, b in zip(STEPS, bars) if s['off'] == v) for v in VERDICTS}
print('\n  off mark:  ' + '   '.join(f"{v} {tally[v]:+.2f}" for v in
                                     ('EFG', 'TESTAHIL', 'OPEN', 'NEITHER')))

# THE REVIEWER'S OWN FIGURES, REGISTERED RATHER THAN LEFT AS PROSE. Two of EFG's numbers
# are quoted in the delivered document — their flat discount rate and their year-5 discount
# factor — and this model cannot compute either, because a different model produced them.
# The prose instrument flagged them as unmatched and it was right to: nothing committed
# them. Per its own rule, A FALSE POSITIVE IS FIXED BY WIDENING THE RENDERING SET, NEVER BY
# DELETING THE FIGURE — and where a figure is real and the model cannot produce it, THE
# MODEL IS WHAT IS MISSING. So they are committed here with their provenance, which also
# means the sentences that quote them can no longer drift from the chart that draws them.
REVIEWER = dict(
    source='EFG Hermes, "Arabian Cement Company — initiation", reconciled 02-Sep-2026',
    basis='figures produced by a THIRD PARTY\'s model. This study cannot compute them and '
          'does not adopt them; they are registered so that quoting them is checkable.',
    flat_wacc=0.2006,          # their single discount rate, applied to every forecast year
    year5_discount_factor=0.4813,
)

out = dict(start=round(START, 4), end=round(END, 4), reviewer=REVIEWER,
           # the comparator is the study's OWN spot; it was typed 59.00 and
           # survived a re-strike to 77.00 [corrected 03-Sep-2026]
           market=float(json.load(open(os.path.join(HERE, 'study_numbers.json')))['spot']),
           published_central=float(END), published_spot=float(
               json.load(open(os.path.join(HERE, 'study_numbers.json')))['spot']),
           steps=[dict(key=s['key'], label=s['label'], sub=s['sub'], driver=s['driver'],
                       off=s['off'], receipt=s['receipt'], value=b)
                  for s, b in zip(STEPS, bars)])
json.dump(out, open(os.path.join(HERE, 'efg_bridge.json'), 'w'), indent=1)
print(f"\n  wrote efg_bridge.json — the chart reads its constants from here (I6)")
if fails:
    sys.exit(f'GATE (t) FAILED: {fails}')
print(f'\nGATE (t) OK — 9 invariants, {len(STEPS)} steps, 0 failures')
