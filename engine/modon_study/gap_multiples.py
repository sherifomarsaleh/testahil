"""The multiple cross-check the gap review publishes, computed from the study's own
committed numbers rather than typed into a markdown file.

ONE BASIS THROUGHOUT, stated so a reader can reproduce it: enterprise value at the fair
value is the DCF's own enterprise value; enterprise value at the traded price is the
market capitalisation plus the SAME bridge items, taken as the difference between the
model's enterprise value and its attributable equity value. Using two different net-debt
definitions either side of the table is how a multiple comparison flatters one side.
"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, 'study_numbers.json')))
DCF, F, HI, M, R = D['dcf'], D['fcst'], D['hist_is'], D['meta'], D['rel']

bridge = DCF['ev'] - DCF['eq_attr']          # what the bridge subtracts, on the study's basis
ev_fv, ev_px = DCF['ev'], M['mktcap'] + bridge
eq_fv, eq_px = D['central'] * M['shares_mn'], D['spot'] * M['shares_mn']

ROWS = [('EV / FY2027E EBITDA',           ev_fv / F['ebitda'][1], ev_px / F['ebitda'][1]),
        ('EV / FY2028E EBITDA',           ev_fv / F['ebitda'][2], ev_px / F['ebitda'][2]),
        ('EV / FY2025A EBITDA',           ev_fv / HI['FY25']['ebitda'],
                                          ev_px / HI['FY25']['ebitda']),
        ('Equity / FY2025A attributable', eq_fv / HI['FY25']['npa'],
                                          eq_px / HI['FY25']['npa'])]

if __name__ == '__main__':
    print('| Basis | At the fair value | At the price |')
    print('|---|---|---|')
    for lab, a, b in ROWS:
        print('| %s | %.2fx | %.2fx |' % (lab, a, b))
    print()
    print('peers on attributable earnings: ' + ', '.join(
        '%s %.2fx' % (k, v['pe_attr']) for k, v in R['peers'].items()))
    print('central %.4f  spot %.2f  gap %+.1f%%'
          % (D['central'], D['spot'], 100 * (D['central'] / D['spot'] - 1)))
