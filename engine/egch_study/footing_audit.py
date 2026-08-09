"""EGCH — does the balance sheet foot?

An external critique footed the four reported balance sheets and found assets and
equity-plus-liabilities differing by 0.27 to 2.6 EGP million. No gate of this study ever
added the columns up. This one does, at every reported date.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE); sys.path.insert(0, HERE)
from inputs import V

TOL = 0.05          # EGP million; anything above this is a transcription error, not rounding

# NOT YET WIRED INTO run_all.py. Adding the two omitted asset lines made FY2023/24,
# FY2024/25 and the March 2026 interim foot to the pound. FY2022/23 still carries +0.055,
# which is a real unresolved transcription difference in the earliest year, not rounding.
# The tolerance is NOT widened to swallow it: a gate that is loosened until it passes has
# stopped being a gate. Wire this in once that year is re-read against the filing.
ASSETS = ['bs_fixed', 'bs_cwip', 'bs_invprop', 'bs_fvoci', 'bs_intang', 'bs_inventory',
          'bs_receivables', 'bs_cash', 'bs_otherfin', 'bs_loansext']
CLAIMS = ['bs_capital', 'bs_reserves', 'bs_debt_lt', 'bs_debt_holdco', 'bs_dtl',
          'bs_provisions', 'bs_payables', 'bs_debt_cur']
DATES = ['FY2223', 'FY2324', 'FY2425', 'M9FY2526']

bad = []
print("balance-sheet footing (EGP million)")
for d in DATES:
    a = sum(V(f'{k}_{d}') for k in ASSETS)
    c = sum(V(f'{k}_{d}') for k in CLAIMS)
    gap = a - c
    flag = "" if abs(gap) <= TOL else "   <-- DOES NOT FOOT"
    print(f"  {d:10s} assets {a:12,.3f}   claims {c:12,.3f}   gap {gap:+8.3f}{flag}")
    if abs(gap) > TOL:
        bad.append((d, gap))
if bad:
    sys.exit(f"FAIL: {len(bad)} of {len(DATES)} reported balance sheets do not foot")
print("PASS: every reported balance sheet foots within " + str(TOL) + " EGP million")
