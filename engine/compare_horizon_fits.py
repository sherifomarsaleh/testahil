"""compare_horizon_fits.py — 60d gate vs calendar-3M gate, same library.

Reads the two PENDING_REVIEW result files written by refit_calendar_horizon.py
(tag='3m') and the matched 60d baseline, and prints the only comparison that
isolates the horizon change: SAME raw library, SAME names, SAME engine — only
the window definition differs.

Why a fresh 60d baseline rather than the numbers in market_profiles.fit_meta:
those were fitted on smaller panels at earlier dates (EG's headline +0.0270 is
a 27-name/351-window fit; the library is 30 names / 494 windows now). Diffing
against them would attribute library growth to the horizon change.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from auto_refresh import band_halfwidth, BAND_TOL, _nu_bucket, _verdict_key  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
NEW = os.path.join(HERE, 'PENDING_REVIEW', 'calendar_horizon_refit_3m.json')
OLD = os.path.join(HERE, 'PENDING_REVIEW', 'baseline_60d_samelibrary.json')


def _nu(v):
    return 250.0 if isinstance(v, str) else float(v)


def main():
    new = json.load(open(NEW))
    old = json.load(open(OLD))

    print("MARKET PANELS — 60d gate vs calendar-3M gate (identical library)\n")
    hdr = (f"{'mkt':4} {'nu':>14} {'width_cal':>18} {'90% band':>9}  "
           f"{'verdict 60d -> 3M':<26} {'skill 60d -> 3M':>22} {'windows':>12}")
    print(hdr); print('-' * len(hdr))
    material = []
    for m in sorted(new):
        a, b = old.get(m), new[m]
        if not a or 'error' in b:
            print(f"{m:4} -- no matched baseline --"); continue
        bw = band_halfwidth(_nu(b['nu']), b['width_cal']) / \
             band_halfwidth(_nu(a['nu']), a['width_cal']) - 1
        vchg = _verdict_key(a['market_verdict']) != _verdict_key(b['market_verdict'])
        flag = []
        if abs(bw) > BAND_TOL:
            flag.append(f"BAND {bw*100:+.1f}%")
        if vchg:
            flag.append("VERDICT")
        print(f"{m:4} {str(a['nu'])+' -> '+str(b['nu']):>14} "
              f"{str(a['width_cal'])+' -> '+str(b['width_cal']):>18} "
              f"{bw*100:>+8.2f}% "
              f"{a['market_verdict']+' -> '+b['market_verdict']:<26} "
              f"{a['market_skill']:+.4f} -> {b['market_skill']:+.4f}  "
              f"{str(a['windows'])+' -> '+str(b['windows']):>12}"
              + ("   <<< " + ", ".join(flag) if flag else ""))
        if flag:
            material.append((m, flag))

    print("\nPER-NAME VERDICTS — only names that MOVED\n")
    moved = fails = 0
    for m in sorted(new):
        a, b = old.get(m), new[m]
        if not a or 'error' in b:
            continue
        for n in sorted(set(a.get('per_name', {})) | set(b.get('per_name', {}))):
            va = (a.get('per_name', {}).get(n) or {}).get('verdict')
            vb = (b.get('per_name', {}).get(n) or {}).get('verdict')
            if va == vb:
                continue
            moved += 1
            if vb and 'FAIL' in vb:
                fails += 1
            sa = (a.get('per_name', {}).get(n) or {}).get('skill')
            sb = (b.get('per_name', {}).get(n) or {}).get('skill')
            mark = "  <<< FAIL" if (vb and 'FAIL' in vb) else ""
            print(f"  {m}/{n:<12} {str(va):<24} -> {str(vb):<24} "
                  f"skill {sa if sa is None else f'{sa:+.4f}'} -> "
                  f"{sb if sb is None else f'{sb:+.4f}'}{mark}")
    if not moved:
        print("  (none)")

    print(f"\nSUMMARY: {len(material)} market(s) past the materiality gate, "
          f"{moved} per-name verdict change(s), {fails} name(s) now FAILING.")
    print("Materiality: " + (", ".join(f"{m} [{'; '.join(f)}]"
                                       for m, f in material) or "none"))
    return 0


if __name__ == '__main__':
    sys.exit(main())
