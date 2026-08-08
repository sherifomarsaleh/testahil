"""
grade_shadow_cohort.py -- Round 8, part D: the grading script for Shadow
Cohort #1, built and tested NOW (23-Jul) so nothing needs inventing later --
October just means re-running this against updated raw_ohlc.

For each of the 30 names in shadow_cohort_20260723.json:
  1. Load the ticker's CURRENT raw_ohlc, count ACTUAL trading rows elapsed
     since anchor_date (the standing grading rule: count real sessions, not
     calendar days -- Sun-Thu EGX weekmask has no holiday awareness if you
     go by calendar).
  2. If >= grade_after_sessions (60) rows have elapsed: pull the close at
     EXACTLY anchor_idx + 60 as realized_close, regenerate both the prod and
     shadow sample paths (same spot/sigma_h/drift/nu/seed -- deterministic,
     so this reproduces the original quantiles bit-for-bit; checked below),
     and score both: CRPS (raw price AND log-price space), which quantile
     band contains the realized close, and PIT.
  3. If not yet 60 sessions: report progress (sessions elapsed / remaining)
     and leave it ungraded -- no partial-credit scoring, no peeking early.

Today this will show 0/30 graded (all anchors are 15-30 sessions old, none
near 60) -- that is the CORRECT and expected output, not a bug. Re-run this
same script unmodified once real time has passed; do not touch the scoring
logic to "check in on" a name early.
"""
import sys, os, json
import numpy as np
import pandas as pd

sys.path.insert(0, '/home/claude/testahil_repo/engine')
from mc_v2 import load_ohlc, yz_variance_proxy, crps_sample
from mc_v3 import simulate_terminal_v3
from data_quality import clean_ohlc

RAW_DIR = '/home/claude/testahil_repo/engine/raw_ohlc/EG'
COHORT_PATH = '/home/claude/labwork/shadow_cohort_20260723.json'


def load_ticker_df(ticker):
    df = load_ohlc(os.path.join(RAW_DIR, f'{ticker}.csv'))
    df, _ = clean_ohlc(df, ticker, verbose=False, market='EG')
    return df.sort_values('Date').reset_index(drop=True)


def grade_row(row, df):
    anchor = pd.Timestamp(row['anchor_date'])
    after = df[df['Date'] > anchor].reset_index(drop=True)
    sessions_elapsed = len(after)
    need = row['grade_after_sessions']

    if sessions_elapsed < need:
        return dict(**row, graded=False, sessions_elapsed=sessions_elapsed,
                     sessions_remaining=need - sessions_elapsed)

    realized_close = float(after['Price'].iloc[need - 1])
    realized_date = str(after['Date'].iloc[need - 1].date())

    out = dict(**row, graded=True, sessions_elapsed=sessions_elapsed,
               sessions_remaining=0, realized_close=realized_close,
               realized_date=realized_date)

    for label in ('prod', 'shadow'):
        drift = row['carry_drift'] if label == 'prod' else row['shadow_drift']
        samp = simulate_terminal_v3(row['spot'], row['sigma_h'], drift,
                                     nu=row['nu'], n_paths=row['n_paths'],
                                     seed=row['seed'])
        # sanity check: regenerated quantiles must match the stored ones
        # (deterministic seed) -- proves this is a faithful re-score, not a
        # fresh/different draw.
        q_check = np.percentile(samp, [5, 25, 50, 75, 95])
        stored = [row[f'{label}_p5'], row[f'{label}_p25'], row[f'{label}_p50'],
                  row[f'{label}_p75'], row[f'{label}_p95']]
        if not np.allclose(q_check, stored, rtol=5e-3):
            out[f'{label}_reproduction_MISMATCH'] = True

        out[f'{label}_crps'] = float(crps_sample(samp, realized_close))
        out[f'{label}_crps_log'] = float(crps_sample(np.log(samp), np.log(realized_close)))
        out[f'{label}_pit'] = float(np.mean(samp <= realized_close))
        p5, p25, p50, p75, p95 = q_check
        out[f'{label}_in50'] = bool(p25 <= realized_close <= p75)
        out[f'{label}_in90'] = bool(p5 <= realized_close <= p95)

    out['crps_delta_log'] = out['shadow_crps_log'] - out['prod_crps_log']  # negative = shadow better
    return out


def main():
    cohort = json.load(open(COHORT_PATH))
    graded, pending = [], []
    for row in cohort['rows']:
        df = load_ticker_df(row['ticker'])
        g = grade_row(row, df)
        (graded if g['graded'] else pending).append(g)

    pending.sort(key=lambda r: r['sessions_remaining'])
    print(f"=== Shadow Cohort #1 grading run -- {len(graded)}/{len(cohort['rows'])} graded ===\n")

    if pending:
        print("Not yet gradeable (sessions elapsed / needed):")
        for r in pending:
            print(f"  {r['ticker']:8s} anchor {r['anchor_date']}  "
                  f"{r['sessions_elapsed']:2d}/{r['grade_after_sessions']} sessions  "
                  f"({r['sessions_remaining']} to go)")

    if graded:
        print("\nGraded:")
        mism = 0
        for r in graded:
            flag = ''
            if r.get('prod_reproduction_MISMATCH') or r.get('shadow_reproduction_MISMATCH'):
                flag = '  [REPRODUCTION MISMATCH -- investigate before trusting]'
                mism += 1
            print(f"  {r['ticker']:8s} realized {r['realized_close']:.2f} on {r['realized_date']}  "
                  f"CRPS(log) prod={r['prod_crps_log']:.4f} shadow={r['shadow_crps_log']:.4f}  "
                  f"delta={r['crps_delta_log']:+.4f}{flag}")
        deltas = [r['crps_delta_log'] for r in graded]
        wins = sum(d < 0 for d in deltas)
        print(f"\n  Pooled (n={len(deltas)}): shadow beats prod on {wins}/{len(deltas)} names, "
              f"mean delta {np.mean(deltas):+.4f} (negative favors shadow)")
        print("  NOTE: this is Cohort #1 alone. Per the promotion protocol, a verdict needs "
              ">=3 non-overlapping cohorts, block-bootstrapped BY COHORT -- do not treat a "
              "single cohort's sign, however it lands, as a promote/reject decision.")
        if mism:
            print(f"\n  WARNING: {mism} name(s) failed the reproduction sanity check -- "
                  "the stored quantiles don't match a fresh re-simulation at the same seed. "
                  "Do not trust deltas until this is root-caused.")
    else:
        print(f"\nNothing gradeable yet. Earliest name reaches T+60 in "
              f"{min(r['sessions_remaining'] for r in pending)} sessions "
              f"(~{min(r['sessions_remaining'] for r in pending) // 5} EGX weeks from today).")

    out_path = COHORT_PATH.replace('.json', '_grading_status.json')
    with open(out_path, 'w') as f:
        json.dump(dict(run_date='2026-07-23', graded=graded, pending=pending), f, indent=1, default=float)
    print(f"\nsaved -> {out_path}")


if __name__ == '__main__':
    main()
