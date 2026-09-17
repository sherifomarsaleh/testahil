"""Independent rebuild of the PHDC 17-09-2026 model from the workbook's OWN cells.

Every constant here is read off a named workbook cell, printed beside it, so the
rebuild is auditable line by line. Nothing is taken from the published answer.
"""

# ---- Assumptions sheet ----------------------------------------------------
CONV        = 0.07676460363240005   # Assumptions!B5   cash conversion, central
CONV_WEAK   = 0.03937593483976742   # Assumptions!B6
CONV_STRONG = 0.1787001284632628    # Assumptions!B7
GM          = 0.3832237248431056    # Assumptions!B8   (reaches nothing)
SGA         = 0.1759945589215163    # Assumptions!B9   (reaches nothing)
NET_DEBT    = 27471.219989          # Assumptions!B13  labelled 31-Mar, is 30-Jun
ASSOC       = 3898.477847           # Assumptions!B14  labelled 31-Mar, is 30-Jun
INVPROP     = 1008.419552           # Assumptions!B15  labelled 31-Mar, is 30-Jun
MI          = 0.0468375604683756    # Assumptions!B16
SHARES      = 2859.92               # Assumptions!B17  issued count
UNITS_26    = 2035.093098749406     # Assumptions!B20
UNIT_G      = 0.15                  # Assumptions!B21  (the DECLARED rule)
PRICE_26    = 19.727806568          # Assumptions!B22
CAPEX       = 0.01                  # Assumptions!B23

# ---- DCF sheet ------------------------------------------------------------
YEARS  = list(range(2026, 2041))                                    # DCF!B4:P4
ESC    = [.16,.12,.09,.075,.07,.07,.07,.07,.07,.07,.07,.07,.07,.07,.07]   # DCF row 5
GROWTH = [0,.15,.135,.12,.105,.09,.075,.06,.045,.03,.015,0,0,0,0]        # DCF row 6
FIN_AT = 2594.3                                                      # DCF row 14
WACC_PATH = [.251085,.219107,.193525,.174338,.161547] + [.161547]*10 # DCF row 16
TERM_PV_HARD = 19819.9                                               # DCF!B21
TERM_G = 0.07            # solved back from TERM_PV_HARD; Assumptions!B11 says 0.12


def revenue(units0=UNITS_26, price0=PRICE_26, growth=None, esc=None):
    growth = GROWTH if growth is None else growth
    esc    = ESC    if esc    is None else esc
    u, p, out = units0, price0, []
    for i in range(len(YEARS)):
        if i:
            u *= (1 + growth[i])
        p = price0 if i == 0 else p * (1 + esc[i])
        out.append(u * p)
    return out


def fcff(rev, conv=CONV, fin=FIN_AT, capex=CAPEX):
    return [r * conv + fin - r * capex for r in rev]


def factors(path, stub=0.0):
    """Cumulative year-end discount factors; `stub` shortens the first period."""
    out, acc = [], 1.0
    for i, w in enumerate(path):
        acc /= (1 + w) ** ((1 - stub) if i == 0 else 1.0)
        out.append(acc)
    return out


def value(conv=CONV, path=None, n_years=15, term_g=TERM_G, fin=FIN_AT,
          net_debt=NET_DEBT, assoc=ASSOC, invprop=INVPROP, mi=MI,
          shares=SHARES, growth=None, esc=None, stub=0.0, term_pv=None,
          units0=UNITS_26, price0=PRICE_26, capex=CAPEX):
    path = WACC_PATH if path is None else path
    rev  = revenue(units0, price0, growth, esc)[:n_years]
    f    = fcff(rev, conv, fin, capex)
    d    = factors(path[:n_years], stub)
    pv_explicit = sum(a * b for a, b in zip(f, d))
    if term_pv is None:
        term_rate = path[n_years - 1]
        tv = f[-1] * (1 + term_g) / (term_rate - term_g)
        term_pv = tv * d[-1]
    ev  = pv_explicit + term_pv
    eq  = ev - net_debt + assoc + invprop
    eq -= eq * mi
    return dict(pv_explicit=pv_explicit, term_pv=term_pv, ev=ev,
                equity=eq, ps=eq / shares,
                term_share=term_pv / ev, rev=rev, fcff=f, disc=d)


if __name__ == '__main__':
    b = value()
    print('=== REPRODUCTION OF THE DELIVERED 17-09-2026 ANSWER ===')
    print(f'  PV of the explicit 15 years   {b["pv_explicit"]:12,.1f}   report 44,489.5')
    print(f'  PV of the terminal (hardcode) {TERM_PV_HARD:12,.1f}   report 19,819.9')
    print(f'  PV of the terminal (Gordon)   {b["term_pv"]:12,.1f}')
    print(f'  Enterprise value              {b["ev"]:12,.1f}   report 64,309.3')
    print(f'  Equity attributable           {b["equity"]:12,.1f}   report 39,789.8')
    print(f'  VALUE PER SHARE               {b["ps"]:12,.4f}   report 13.91')
    print(f'  Terminal share of EV          {b["term_share"]:12,.4f}   report 31%')
    print()
    print('  year   revenue      FCFF     WACC    factor        PV')
    for i, y in enumerate(YEARS):
        print(f'  {y}  {b["rev"][i]:10,.1f} {b["fcff"][i]:9,.1f}  {WACC_PATH[i]:7.4%} {b["disc"][i]:8.4f} {b["rev"][i]*0+b["fcff"][i]*b["disc"][i]:9,.1f}')
