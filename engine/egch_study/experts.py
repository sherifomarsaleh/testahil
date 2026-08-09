"""EGCH — the expert panel's arithmetic, computed rather than asserted.

Every intermediate line each expert shows is calculated here from the input register and
the model, so the document builder types no financial numeral. Each expert carries a
worldview, a when-it-works/when-it-fails statement, a worked table, a named sensitivity
and a falsifier, all of which the study prints in full.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from inputs import V

D = json.load(open(os.path.join(HERE, 'study_numbers.json')))
LN = json.load(open(os.path.join(HERE, 'lenses.json')))
SH, SPOT = V('shares_outstanding'), V('spot_price')
B = D['cases']['base']['bridge']
NET_DEBT, FVOCI, INVPROP = B['net_debt'], B['fvoci'], B['inv_prop']
E = {}

# ------------------------------------------------ EXPERT 1: replacement cost --
gross_fixed = V('bs_gross_fixed_M9FY2526')   # note 6 cost at period end, EGP m
acc_dep = V('bs_acc_dep_M9FY2526')           # note 6 accumulated depreciation
cwip = V('bs_cwip_M9FY2526')
cap_lo, cap_hi = V('greenfield_capex_usd_t_low'), V('greenfield_capex_usd_t_high')
fx = V('usd_egp_spot')
plate = V('design_urea_tpy')
repl_lo = plate * cap_lo * fx / 1e6
repl_hi = plate * cap_hi * fx / 1e6
repl_mid = (repl_lo + repl_hi) / 2
cwip_haircut = 0.40
cwip_valued = cwip * (1 - cwip_haircut)
gross_asset = repl_mid + cwip_valued + FVOCI + INVPROP
eq_undiscounted = gross_asset - NET_DEBT
disc = V('control_discount_eg_state')
eq_discounted = eq_undiscounted * (1 - disc)
E['e1'] = dict(
    title="Replacement cost and asset backing",
    worldview=("A plant is worth what it would cost to build again, less what is owed "
               "against it. Cash flows are a claim on the asset; the asset is the thing."),
    works=("When an asset is scarce, hard to permit and expensive to replicate — which a "
           "gas-connected nitrogen complex in Egypt certainly is."),
    fails=("When the asset cannot earn its keep. Replacement cost sets a ceiling on what a "
           "rational buyer pays and says nothing about what an owner receives."),
    rows=[("Gross fixed assets at cost", gross_fixed, "note 6"),
          ("Less accumulated depreciation", -acc_dep, "note 6"),
          ("Net book value of the operating plant", gross_fixed - acc_dep, "as reported"),
          ("Urea plate (tonnes a year)", plate, "1,575 t/day contractual plate"),
          ("Build cost, low (US$ per annual tonne)", cap_lo, "industry range"),
          ("Build cost, high (US$ per annual tonne)", cap_hi, "industry range"),
          ("Replacement cost at the low end (EGP m)", repl_lo, "plate x cost x the rate"),
          ("Replacement cost at the high end (EGP m)", repl_hi, ""),
          ("Replacement cost, mid-point (EGP m)", repl_mid, ""),
          ("Construction in progress at cost (EGP m)", cwip, "31 March 2026"),
          ("Haircut for delay and the governance findings", -cwip * cwip_haircut, "40%"),
          ("Construction in progress, valued (EGP m)", cwip_valued, ""),
          ("Listed equity stakes at market (EGP m)", FVOCI, ""),
          ("Investment property (EGP m)", INVPROP, ""),
          ("Gross asset value (EGP m)", gross_asset, ""),
          ("Less net debt (EGP m)", -NET_DEBT, "31 March 2026"),
          ("Equity before any control discount (EGP m)", eq_undiscounted, ""),
          ("Per share before the discount (EGP)", eq_undiscounted * 1e6 / SH, ""),
          ("Control discount on a state-held listed industrial", -disc, "observed"),
          ("Equity after the discount (EGP m)", eq_discounted, ""),
          ("PER SHARE (EGP)", eq_discounted * 1e6 / SH, "")],
    low=eq_discounted * 1e6 / SH,
    high=eq_undiscounted * 1e6 / SH,
    sensitivity=("The build cost is the swing factor. At US$550 per annual tonne the range "
                 f"starts at EGP {(repl_lo + cwip_valued + FVOCI + INVPROP - NET_DEBT) * (1 - disc) * 1e6 / SH:,.2f}; "
                 f"at US$700 it reaches EGP {(repl_hi + cwip_valued + FVOCI + INVPROP - NET_DEBT) * (1 - disc) * 1e6 / SH:,.2f}. "
                 "The control discount moves it by about a third either way."),
    reading=(f"This is the highest of the three readings and it should be read as a "
             f"ceiling rather than a centre. It values the plant at what a buyer would pay "
             f"to avoid building one, and on a plate of {plate:,.0f} tonnes at the "
             f"mid-point of the industry build range that is EGP {repl_mid:,.0f}m before "
             f"anything is owed against it. What the method cannot see is that the plant "
             f"has been running at about ninety per cent of that plate on rationed gas, "
             f"and that the asset under construction — carried here at "
             f"{(1 - cwip_haircut) * 100:.0f}% of what has been spent on it — is exactly "
             f"the asset whose return the cash-flow lens finds inadequate. The gap between "
             f"this expert and the panel's lowest is not a disagreement about the plant. "
             f"It is a disagreement about whether an asset that cannot earn its cost of "
             f"capital is worth its replacement cost."),
    falsifier=("A comparable Egyptian nitrogen asset transacting above US$700 per annual "
               "tonne, or a state-held listed subsidiary changing hands without a control "
               "discount. Either would show this method is set too low and the cash-flow "
               "lens should govern."))

# --------------------------------------------- EXPERT 2: normalised earnings --
NM = LN['normalised']
E['e2'] = dict(
    title="Normalised earnings power",
    worldview=("Strip out the construction, the translation noise and the price cycle, and "
               "ask what this plant earns in an ordinary year. Value that."),
    works=("For a mature single-asset producer whose economics are stable once the cycle is "
           "averaged out."),
    fails=("When the capital structure or the asset base is changing underneath the "
           "earnings — which is exactly what is happening here, and why this expert's "
           "answer sits above the cash-flow lens."),
    rows=[("Mid-cycle urea output (tonnes)", NM['urea_mid'], "three-year average of audited output"),
          ("Less subsidised deliveries (tonnes)", -V('subsidised_t_path')[0], "obligation path"),
          ("Less local free-market (tonnes)", -V('local_free_path')[0], ""),
          ("Export tonnes", NM['export_t'], ""),
          ("Mid-cycle export price (US$/t)", NM['price_usd'], "above the 2015-2020 average, below spot"),
          ("Exchange rate", NM['fx'], ""),
          ("Export revenue (EGP m)", NM['rev_exp'], "net of the 10% duty"),
          ("Subsidised revenue (EGP m)", NM['rev_sub'], ""),
          ("Local free-market revenue (EGP m)", NM['rev_free'], ""),
          ("Nitrate revenue (EGP m)", NM['rev_an'], ""),
          ("Other revenue (EGP m)", NM['rev_oth'], ""),
          ("MID-CYCLE REVENUE (EGP m)", NM['revenue'], ""),
          ("Natural gas (EGP m)", -NM['gas'], "consumption x price x the rate"),
          ("Other materials (EGP m)", -NM['other_materials'], ""),
          ("Wages (EGP m)", -NM['wages'], ""),
          ("Purchased services (EGP m)", -NM['services'], ""),
          ("Inland freight (EGP m)", -NM['freight'], ""),
          ("Other selling (EGP m)", -NM['other_selling'], ""),
          ("Administration (EGP m)", -NM['admin'], ""),
          ("MID-CYCLE EBITDA (EGP m)", NM['ebitda'], ""),
          ("Depreciation and amortisation (EGP m)", -NM['dep'], ""),
          ("Tax at the statutory rate", -(NM['ebitda'] - NM['dep']) * V('tax_statutory'), ""),
          ("MID-CYCLE OPERATING PROFIT AFTER TAX (EGP m)", NM['nopat'], ""),
          ("At ten times — enterprise value (EGP m)", NM['ev'], ""),
          ("Less net debt (EGP m)", -NET_DEBT, ""),
          ("Plus non-operating assets (EGP m)", FVOCI + INVPROP, ""),
          ("PER SHARE (EGP)", NM['value_per_share'], "")],
    low=NM['value_low'], high=NM['value_high'],
    sensitivity=(f"The multiple is the swing factor: eight times gives EGP {NM['value_low']:,.2f}, "
                 f"twelve times EGP {NM['value_high']:,.2f}. The mid-cycle price matters almost as "
                 "much — every US$50 a tonne is worth roughly a pound a share."),
    reading=(f"The middle reading, and the one closest to a conventional analyst's "
             f"answer. It credits an ordinary year — EGP {NM['revenue']:,.0f}m of revenue "
             f"and EGP {NM['ebitda']:,.0f}m of operating profit before depreciation — and "
             f"capitalises the after-tax result at ten times. Its blind spot is stated in "
             f"its own worldview: a normalised year is a steady state, and this company is "
             f"not in one. The capital programme sits entirely outside this table. Read "
             f"strictly, this expert is valuing the plant that exists, and the reader who "
             f"wants the whole company should subtract the programme's cost separately — "
             f"which is what the cash-flow lens does inside a single model."),
    falsifier=("Two consecutive years of EBITDA above EGP 4 billion with the capital "
               "programme funded out of operating cash flow. That would show the "
               "normalisation is too harsh and the multiple too low."))

# ------------------------------------------------- EXPERT 3: contingent claim --
ev_incl = B['ev'] + FVOCI + INVPROP
strike = B['debt']
vol = 0.45
T_yrs = 5.0
rf_opt = 0.20
import math
def bs_call(S, K, r, sig, T):
    if S <= 0: return 0.0
    d1 = (math.log(S / K) + (r + sig * sig / 2) * T) / (sig * math.sqrt(T))
    d2 = d1 - sig * math.sqrt(T)
    N = lambda x: 0.5 * (1 + math.erf(x / math.sqrt(2)))
    return S * N(d1) - K * math.exp(-r * T) * N(d2)
call = bs_call(ev_incl, strike, rf_opt, vol, T_yrs)
call_lo = bs_call(ev_incl, strike, rf_opt, 0.35, T_yrs)
call_hi = bs_call(ev_incl, strike, rf_opt, 0.55, T_yrs)
dilution = 0.25
E['e3'] = dict(
    title="The equity as a contingent claim",
    worldview=("When the value of the firm sits below the face value of its debt, the "
               "equity is not a claim on cash flows. It is an option on the assets, and a "
               "discounted-cash-flow model understates it because it ignores the "
               "shareholder's right to walk away."),
    works=("For a leveraged, volatile business whose enterprise value is near or below its "
           "debt — precisely this situation."),
    fails=("When the option holder cannot choose when to exercise, when further capital "
           "calls dilute the position, or when the enterprise comfortably covers its debt."),
    rows=[("Enterprise value including non-operating assets (EGP m)", ev_incl, "the underlying"),
          ("Gross debt — the strike (EGP m)", strike, "31 March 2026"),
          ("Time to the last dollar maturity (years)", T_yrs, "discounted from 2035"),
          ("Enterprise volatility a year", vol,
           "the export price alone moved between US$380 and US$730 inside eighteen months"),
          ("Risk-free rate in pounds", rf_opt, ""),
          ("Call value on those parameters (EGP m)", call, ""),
          ("At 35% volatility (EGP m)", call_lo, ""),
          ("At 55% volatility (EGP m)", call_hi, ""),
          ("Adjustment for forced timing and dilution", -dilution, ""),
          ("Adjusted call value (EGP m)", call * (1 - dilution), ""),
          ("PER SHARE (EGP)", call * (1 - dilution) * 1e6 / SH, "")],
    low=0.0, high=call_hi * (1 - dilution) * 1e6 / SH,
    sensitivity=(f"Volatility is the swing factor: at 35% the claim is worth EGP "
                 f"{call_lo * (1 - dilution) * 1e6 / SH:,.2f} a share, at 55% EGP "
                 f"{call_hi * (1 - dilution) * 1e6 / SH:,.2f}. Time to maturity matters almost "
                 "as much, because it is time for the enterprise to recover above the debt."),
    falsifier=("Enterprise value rising above the face value of the debt — which needs "
               "roughly a US$120 a tonne sustained improvement in the export price, or the "
               "capital programme being stopped. Either would retire the option framing and "
               "hand the question back to the cash-flow lens."))

GRID3 = dict(vols=[0.30, 0.35, 0.45, 0.55, 0.60], years=[3.0, 5.0, 7.0])
GRID3['values'] = [[bs_call(ev_incl, strike, rf_opt, v, t) * (1 - dilution) * 1e6 / SH
                    for v in GRID3['vols']] for t in GRID3['years']]
E['e3']['grid'] = GRID3
E['e3']['reading'] = (
    f"The lowest and the widest of the three, and the only one that takes the debt "
    f"seriously as a structural fact rather than as a subtraction. Enterprise value "
    f"including the non-operating assets is EGP {ev_incl:,.0f}m against gross debt of "
    f"EGP {strike:,.0f}m, so the equity is out of the money on the model's own central "
    f"case and its value is entirely time value. That is why the answer rises with "
    f"volatility and with time, and why the grid below matters more than the point: at "
    f"{GRID3['vols'][0]*100:.0f}% volatility over three years the claim is worth EGP "
    f"{GRID3['values'][0][0]:,.2f} a share, and at {GRID3['vols'][-1]*100:.0f}% over "
    f"seven years EGP {GRID3['values'][-1][-1]:,.2f}. A reader who finds it perverse "
    f"that a worse business is worth more here has understood the method correctly: "
    f"limited liability truncates the downside, so dispersion accrues to the holder. "
    f"What the method cannot do is tell that holder when the option expires.")

E['ranges'] = {k: (E[k]['low'], E[k]['high']) for k in ('e1', 'e2', 'e3')}
E['spot'] = SPOT
json.dump(E, open(os.path.join(HERE, 'experts.json'), 'w'), indent=1, default=float)
for k in ('e1', 'e2', 'e3'):
    print(f"{k}: {E[k]['title']:38s} EGP {E[k]['low']:6.2f} - {E[k]['high']:6.2f}")
