"""reverify_post_merge.py — redo the 60d-vs-3M comparison for every market whose
raw library moved on main while the calendar-horizon branch was in flight
(concurrent 'Selection engine' long-history AE/SA ingest + KR 15yr Samsung +
OCDI/ORHD roll-forward + a GOLD refresh). IN/QA/US/XPT did not move and are
left as originally computed.

Cheapest first, so partial progress is useful if this gets interrupted.
Writes one JSON per market pair to PENDING_REVIEW/ and appends a line to
reverify_log.txt after each market so progress can be tailed.
"""
import glob
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from auto_refresh import band_halfwidth                                # noqa: E402
from market_profiles import PROFILES                                    # noqa: E402
from panel_refresh import refresh_market                                # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, 'raw_ohlc')
OUT = os.path.join(HERE, 'PENDING_REVIEW')
LOG = os.path.join(HERE, 'reverify_log.txt')

# market -> (touched names this session, or None for "all names in the library")
TOUCHED = {
    'XAU': ['GOLD'],
    'EG':  ['OCDI', 'ORHD'],
    'KR':  ['SAMSUNG'],
    'AE':  None,   # every AE name was re-ingested with long history
    'SA':  None,   # every SA name was re-ingested with long history
}


def log(msg):
    line = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    with open(LOG, 'a') as f:
        f.write(line + "\n")


def all_files(market):
    return {os.path.splitext(os.path.basename(f))[0]: f
            for f in sorted(glob.glob(os.path.join(RAW, market, '*.csv')))}


def run_one(market, tag):
    files = all_files(market)
    touched_names = TOUCHED[market]
    new_csvs = files if touched_names is None else {n: files[n] for n in touched_names}
    t0 = time.time()
    r = refresh_market(market, new_csvs, files, update_registry=False, tag=tag)
    r['_elapsed_s'] = round(time.time() - t0, 1)
    return r


def main():
    os.makedirs(OUT, exist_ok=True)
    open(LOG, 'a').write(f"\n=== reverify run start {time.strftime('%F %T')} ===\n")
    results = {}
    for market in ['XAU', 'EG', 'KR', 'AE', 'SA']:      # cheapest first
        for tag in ['60d', '3m']:
            log(f"{market} [{tag}] starting ({len(all_files(market))} names in library)...")
            try:
                r = run_one(market, tag)
            except Exception as e:
                log(f"{market} [{tag}] FAILED: {type(e).__name__}: {e}")
                continue
            results.setdefault(market, {})[tag] = r
            prof = PROFILES[market]
            if tag == '60d':
                bw_note = "(fresh 60d baseline on current library)"
            else:
                old_bw = band_halfwidth(prof.nu if prof.nu else 8.0, prof.width_cal)
                new_nu = 250.0 if isinstance(r['nu'], str) else r['nu']
                new_bw = band_halfwidth(new_nu, r['width_cal'])
                bw_note = f"(vs PRODUCTION incumbent nu={prof.nu},cal={prof.width_cal}: {(new_bw/old_bw-1)*100:+.2f}%)"
            log(f"{market} [{tag}] DONE nu={r['nu']} cal={r['width_cal']} "
                f"verdict={r['market_verdict']} skill={r['market_skill']:+.4f} "
                f"CI={r['market_ci90']} windows={r['windows']}/{len(r['panel_names'])}n "
                f"{bw_note} [{r['_elapsed_s']}s]")
            with open(os.path.join(OUT, 'reverify_post_merge.json'), 'w') as f:
                json.dump(results, f, indent=2, default=str)
    log("=== reverify run complete ===")


if __name__ == '__main__':
    main()
