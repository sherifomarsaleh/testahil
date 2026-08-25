#!/usr/bin/env python3
"""Regenerate every published calibration figure, resilient to a single failure.

Written after a bare `metal_backtest.py KEY1 KEY2 ...` run aborted at figure 50
of 93 on one unresolvable key and silently left 43 figures carrying the retired
verdict caption. Two things it fixes:

  * KEY CASE. The figure FILENAME is not always the resolver's key. Metals
    resolve through PANELS under GOLD/SILVER/PLATINUM but write Gold/Silver/
    Platinum; the Korean names are keyed SAMSUNG/KAKAO in TICKERS while the
    ledger requests calibration_Samsung.png. Both are mapped here explicitly.
  * ONE FAILURE MUST NOT COST THE OTHER 92. Each key is attempted in its own
    try/except and the run reports what failed at the end, rather than exiting
    on the first SystemExit.
"""
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.dirname(HERE)
ASSETS = os.path.join(ROOT, 'assets')

# figure filename -> (resolver key, output filename the site actually requests)
SPECIAL = {
    'Gold': ('GOLD', 'Gold'), 'Silver': ('SILVER', 'Silver'),
    'Platinum': ('PLATINUM', 'Platinum'),
    'Samsung': ('SAMSUNG', 'Samsung'), 'Kakao': ('KAKAO', 'Kakao'),
}


def main():
    import metal_backtest as mb
    names = sorted(re.sub(r'^calibration_|\.png$', '', f)
                   for f in os.listdir(ASSETS)
                   if f.startswith('calibration_') and f.endswith('.png'))
    only = set(sys.argv[1:])
    done, failed = [], []
    for fig in names:
        if only and fig not in only:
            continue
        key, want = SPECIAL.get(fig, (fig, fig))
        try:
            res = mb.build(key)
        except BaseException as e:                            # noqa: BLE001
            failed.append((fig, str(e)[:120]))
            print(f'  FAIL {fig}: {str(e)[:110]}', flush=True)
            continue
        # build() names the file from the resolved panel key; make sure the file
        # the site asks for is the one that got the new caption.
        produced = res.get('out') if isinstance(res, dict) else None
        target = os.path.join(ASSETS, f'calibration_{want}.png')
        if produced and os.path.abspath(produced) != os.path.abspath(target):
            shutil.copyfile(produced, target)
        done.append(fig)
        print(f'  ok   {fig}  ({res.get("windows")} windows, '
              f'cov90 {res.get("cov90")})', flush=True)

    print(f'\n{len(done)} regenerated, {len(failed)} failed')
    for f, e in failed:
        print(f'  {f}: {e}')
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
