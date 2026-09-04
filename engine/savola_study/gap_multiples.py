"""The multiple cross-check the gap review publishes, computed from the study's own
committed numbers rather than typed into a markdown file.

ONE BASIS THROUGHOUT, stated so a reader can reproduce it: enterprise value at the fair
value is the model's own; at the traded price it is the market capitalisation plus the
SAME bridge, taken as the difference between the model's enterprise value and the equity
value it produces. Using two different net-debt definitions either side of a multiple
table is how a comparison flatters one side.
"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, 'study_numbers.json')))
DCF, F, HI, M = D['dcf'], D['fcst'], D['hist_is'], D['meta']
IN = {k: v['value'] for k, v in D['inputs'].items()}

sh = IN['shares_val_mn']
bridge = DCF['ev'] - DCF['eq_val']
ev_fv, ev_px = DCF['ev'], M['spot'] * sh + bridge

ROWS = [('EV / FY2027E EBITDA', ev_fv / F['ebitda'][1], ev_px / F['ebitda'][1]),
        ('EV / FY2028E EBITDA', ev_fv / F['ebitda'][2], ev_px / F['ebitda'][2]),
        ('EV / FY2025A EBITDA', ev_fv / HI['FY25']['ebitda'], ev_px / HI['FY25']['ebitda']),
        ('Price / FY2026E earnings', D['central'] / F['eps'][0], M['spot'] / F['eps'][0]),
        ('Price / FY2027E earnings', D['central'] / F['eps'][1], M['spot'] / F['eps'][1])]

if __name__ == '__main__':
    print('| Basis | At the fair value | At the price |')
    print('|---|---|---|')
    for lab, a, b in ROWS:
        print('| %s | %.2fx | %.2fx |' % (lab, a, b))
    print()
    print('peers on trailing earnings: ' + ', '.join(
        '%s %.2fx' % (k, v) for k, v in D['peers']['pe'].items() if v))
    print('central %.4f  spot %.2f (%s)  gap %+.1f%%'
          % (D['central'], M['spot'], M['spot_date'], 100 * (D['central'] / M['spot'] - 1)))
    print('cash-flow lens %.2f (gap %+.1f%%)  life variant %.2f'
          % (DCF['ps'], 100 * (DCF['ps'] / M['spot'] - 1), DCF['ps_life_variant']))
