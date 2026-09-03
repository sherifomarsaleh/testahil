#!/usr/bin/env python3
"""PHDC — the reverse read [R-ENF-05], COMPUTED rather than remembered.

WHY THIS FILE EXISTS. diagnostics.json was committed, read by an outside gate, and
WRITTEN BY NOTHING -- no generator existed anywhere in the repository. It froze at
`as_of 2026-09-02, spot 15.20` and stayed there through a re-strike to 14.40, while
the delivered document published a re-solved 7.31% beside it.

That is the third instance of one defect found in a single day: AMOC's
case_adversarial.json, ARCC's efg_bridge.json caption, and this. AN ARTEFACT EVERY
BUILDER READS AND NOTHING WRITES IS A NUMBER FROZEN AT THE DATE SOMEBODY LAST TYPED
IT, and [R-ENF-06] exists because of it.

THE QUANTITY IS THE CRUX OF THIS CLASS. A developer's value turns on how quickly
contracted sales become operating cash, and that rate is something a reader can
check against the company's own filed cash-flow statements. The solve holds every
other driver at its published value and moves only that rate.

IT IS A DIAGNOSTIC AND NOTHING READS IT BACK. A quantity solved from a price and
then used in the valuation is the reverse-engineered rate the protocol prohibits
outright, arriving through a side door; assert_reverse_dcf() refuses any study
whose builders read this file.

    python3 diagnostics_phdc.py      writes diagnostics.json
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))


def main():
    N = json.load(open(os.path.join(HERE, 'study_numbers.json'), encoding='utf-8'))
    import valuation_v2 as V2

    spot = float(N['spot'])
    central = float(N['central'])
    lr = N['lens_record']['primary']
    lo, hi = lr['range_basis']['low'], lr['range_basis']['high']
    forecast = V2.lenses()['cfo']['mid']

    # SOLVED ON THE STUDY'S OWN MODEL, at the CURRENT price, through the same
    # function the study uses -- not re-implemented here, which would grade
    # something other than what ships.
    implied = V2.implied_conversion(spot, V2.SCHEDULES['cds'])

    _in = 'inside' if lo <= implied <= hi else 'OUTSIDE'
    diag = {
        'ticker': 'PHDC',
        'as_of': N['meta'].get('edition', ''),
        'spot': spot,
        'spot_date': N['meta'].get('spot_date', ''),
        # [R-ENF-06] the vintage this artefact was built against
        'published_central': central,
        'published_spot': spot,
        'why_this_file': (
            'The reverse read — what the traded price must believe — is a DIAGNOSTIC and '
            'lives outside the numbers file every builder reads. A quantity solved from a '
            'price and then used anywhere in the valuation is the reverse-engineered rate '
            'the protocol prohibits outright, arriving through a side door. Nothing in '
            'this file is an input to anything. It is COMPUTED by diagnostics_phdc.py; an '
            'earlier version of it was committed with no generator at all and froze at a '
            'spot of 15.20 through a re-strike to 14.40.'),
        'implied': {
            'quantity': 'the rate at which contracted sales become operating cash',
            'value': float(implied),
            'study_value': float(forecast),
            'study_value_range': [float(lo), float(hi)],
            'solved_on': (
                "this study's own model through valuation_v2.implied_conversion, on the "
                "adopted CDS cost-of-capital schedule, holding every driver at its "
                "published value and varying only cash conversion until the model "
                "reproduces the traded price"),
            'reading': (
                'At EGP %.2f the price is paying for a cash-conversion rate of %.2f%%, '
                'against this study\'s forecast of %.2f%% and a range of %.2f%% to %.2f%% '
                'that the company\'s own filed cash-flow statements actually show. The '
                'market\'s implied figure sits %s that filed range. The disagreement is '
                '%.0f basis points on ONE driver a reader can check, which is a more '
                'useful statement than "the study is %+.1f%% against the price".'
                % (spot, 100 * implied, 100 * forecast, 100 * lo, 100 * hi, _in,
                   abs(10000 * (forecast - implied)), 100 * (central / spot - 1))),
        },
    }
    json.dump(diag, open(os.path.join(HERE, 'diagnostics.json'), 'w', encoding='utf-8'),
              indent=1, ensure_ascii=False)
    print('diagnostics.json COMPUTED at spot %.2f (central %.4f)' % (spot, central))
    print('  ' + diag['implied']['reading'])
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
