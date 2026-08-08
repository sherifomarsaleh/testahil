"""Step 0 calibration gate for XPT (platinum) — run with the ACTUAL production
machinery (panel_refresh/backtest_v3/fit_nu_scale/robust_verdict), locally.

Design decisions (stated, per protocol):
 - XPT is a NEW single-instrument metal market (site precedent: silver raw parked
   at raw_ohlc/XAG/, pipeline maps only PROFILES codes). Its FIRST action per the
   standing per-market fit rule is a PROVISIONAL SELF-FIT on its own panel —
   flagged circular exactly like gold's.
 - Scored three ways: (a) provisional self-fit; (b) incumbent live METALS config
   (Gaussian/1.0) = borrowed; (c) DE-CIRCULARIZED cross-metal LONO: fit on
   GOLD+SILVER residuals, score XPT out-of-sample. (c) is the honest verdict.
 - Reproduction check: rebuild GOLD panel and confirm the LIVE registry numbers
   (67 windows, skill +0.0035, CI[-0.005,+0.013]) to prove the local chain IS
   production.
"""
import sys, os, json
sys.path.insert(0, os.path.abspath('repo/engine'))
import numpy as np, pandas as pd
from market_profiles import MarketProfile, PROFILES, FED_SCHEDULE
from mc_v2 import load_ohlc as raw_load
from data_quality import clean_ohlc
from mc_v3 import fit_nu_scale, shrink_cal, backtest_v3
from panel_refresh import fast_rescore, robust_verdict, verdict_ci, MIN_HISTORY

XPT = MarketProfile("XPT", "Platinum (USD)", FED_SCHEDULE, 0.0363,
    "USD cost-of-carry anchor: Fed funds midpoint schedule (q=0). Same documented "
    "assumption as METALS: carry-anchored null for a zero-yield USD store of value.",
    None, +1, 0.0, False, nu=None, width_cal=1.0, breaks=[])

def load(path, ticker, market=None):
    df, _ = clean_ohlc(raw_load(path), ticker, verbose=False, market=market)
    return df

def build_panel(df, profile):
    rows = backtest_v3(df, profile, horizon=60, nu=8.0, width_cal=1.0,
                       use_signal=profile.signal_active, n_paths=20000, seed=42,
                       min_history=MIN_HISTORY)
    r = pd.DataFrame(rows)
    r['origin_idx'] = MIN_HISTORY + np.arange(len(r)) * 60
    return r

def score(r, nu, cal, label):
    c = fast_rescore(r, nu, cal)
    cb = r['crps_b'].values; spot = r['spot'].values
    cn, cbn = c / spot, cb / spot
    sk = float(1 - cn.sum() / cbn.sum())
    sk_raw = float(1 - c.sum() / cb.sum())
    verd, detail = robust_verdict(cn, cbn)
    ci2 = detail[2][:2]
    cov = {k: float(r[k].mean()) for k in ('in50', 'in80', 'in90')}
    # NB stored coverage cols were computed at build baseline (nu=8, cal=1);
    # recompute coverage under (nu,cal) via u: P(|t|<q) — approximate by re-sim not needed:
    print(f"  [{label:34s}] nu={nu if nu<200 else 'Gauss':>5} cal={cal:.3f} "
          f"skill={sk:+.4f} (raw {sk_raw:+.4f}) CI2[{ci2[0]:+.3f},{ci2[1]:+.3f}] {verd}")
    return dict(nu=(nu if nu < 200 else 'Gaussian'), cal=round(cal,3), skill=round(sk,4),
                skill_raw=round(sk_raw,4), ci_block2=[round(float(ci2[0]),3), round(float(ci2[1]),3)],
                verdict=verd, detail={b: [round(float(x),4) for x in detail[b][:2]] + [detail[b][2]] for b in detail})

METALS = PROFILES['XAU']
print("=== building panels (production chain, baseline nu=8/cal=1.0, seed 42) ===")
xpt_df = load('XPT_USD.csv', 'PLATINUM', market=None)
gold_df = load('repo/engine/raw_ohlc/XAU/GOLD.csv', 'GOLD', market='XAU')
slv_df = load('repo/engine/raw_ohlc/XAG/SILVER.csv', 'SILVER', market=None)
rx = build_panel(xpt_df, XPT)
rg = build_panel(gold_df, METALS)
rs = build_panel(slv_df, XPT)  # silver: same carry profile (Fed, q=0), no breaks
print(f"windows: XPT {len(rx)}, GOLD {len(rg)}, SILVER {len(rs)}")
print(f"XPT window span: {rx['origin'].iloc[0]} -> {rx['origin'].iloc[-1]}")

# --- reproduction check vs live registry (gold under live Gaussian/1.0) ---
cg = fast_rescore(rg, 1e9, 1.0)
cbg = rg['crps_b'].values; sg = rg['spot'].values
skg = float(1 - (cg/sg).sum() / (cbg/sg).sum())
vg, dg = robust_verdict(cg/sg, cbg/sg)
print(f"\nREPRODUCTION CHECK gold under live (Gaussian,1.0): windows={len(rg)} "
      f"skill={skg:+.4f} CI2[{dg[2][0]:+.3f},{dg[2][1]:+.3f}] {vg}")
print("  live registry says: windows=67 skill=+0.0035 CI2[-0.005,+0.013] PARITY")

# --- fits ---
u_x = rx['u'].values; u_g = rg['u'].values; u_s = rs['u'].values
nu_self, s_self = fit_nu_scale(u_x); cal_self = shrink_cal(s_self)
nu_gs, s_gs = fit_nu_scale(np.concatenate([u_g, u_s])); cal_gs = shrink_cal(s_gs)
nu_pool3, s_pool3 = fit_nu_scale(np.concatenate([u_g, u_s, u_x])); cal_pool3 = shrink_cal(s_pool3)
print(f"\nXPT SELF-FIT (PROVISIONAL, single-name, circular): nu={nu_self if nu_self<200 else 'Gaussian'}, "
      f"mle_scale={s_self:.3f}, width_cal={cal_self:.3f}  [{len(u_x)} windows]")
print(f"GOLD+SILVER fit (XPT's LONO trainer): nu={nu_gs if nu_gs<200 else 'Gaussian'}, "
      f"mle_scale={s_gs:.3f}, width_cal={cal_gs:.3f}  [{len(u_g)+len(u_s)} windows]")
print(f"3-metal pooled (hypothetical joint panel): nu={nu_pool3 if nu_pool3<200 else 'Gaussian'}, "
      f"mle_scale={s_pool3:.3f}, width_cal={cal_pool3:.3f}  [{len(u_g)+len(u_s)+len(u_x)} windows]")

print("\n=== XPT scored under each config (scale-normalized gate, robust blocks {2,3,4}) ===")
res = {}
res['self_fit'] = score(rx, nu_self, cal_self, 'XPT self-fit (provisional)')
res['borrowed_live_metals'] = score(rx, 1e9, 1.0, 'borrowed live METALS (Gauss/1.0)')
res['lono_gold_silver'] = score(rx, nu_gs, cal_gs, 'LONO fit-on-gold+silver (OOS)')

print("\n=== last-5y subset (protocol 5-year walk-forward framing) ===")
cut = rx[pd.DatetimeIndex(rx['origin']) >= (pd.Timestamp('2026-07-20') - pd.DateOffset(years=5))].reset_index(drop=True)
print(f"windows in last 5y: {len(cut)}")
res['self_fit_5y'] = score(cut, nu_self, cal_self, 'XPT self-fit, 5y subset')
res['lono_5y'] = score(cut, nu_gs, cal_gs, 'LONO gold+silver, 5y subset')

# --- diagnostics under the ADOPTED (self-fit) config: coverage/PIT via exact rescale of u ---
from scipy import stats
def cov_pit(r, nu, cal):
    u = r['u'].values / cal
    if nu >= 200:
        pit = stats.norm.cdf(u)
    else:
        k = np.sqrt(nu / (nu - 2)); pit = stats.t.cdf(u * k, nu)
    q = lambda p: (stats.norm.ppf(p) if nu >= 200 else stats.t.ppf(p, nu) / np.sqrt(nu/(nu-2)))
    inb = lambda p: float(np.mean(np.abs(u) <= q(0.5 + p/2)))
    return dict(pit_mean=float(pit.mean()), cov50=inb(0.50), cov80=inb(0.80), cov90=inb(0.90))
print("\nXPT diagnostics under self-fit:", cov_pit(rx, nu_self, cal_self))
print("XPT diagnostics under LONO   :", cov_pit(rx, nu_gs, cal_gs))
print("GOLD diagnostics under live  :", cov_pit(rg, 1e9, 1.0))

# --- materiality framing (what auto_refresh would say) ---
from auto_refresh import band_halfwidth
bw_live = band_halfwidth(250.0, 1.0)
bw_self = band_halfwidth(nu_self, cal_self)
print(f"\nMATERIALITY: 90% cone half-width (units of sigma_h): live METALS {bw_live:.3f} vs "
      f"XPT self-fit {bw_self:.3f} -> rel diff {abs(bw_self-bw_live)/bw_live:+.1%}"
      f" (NB different market — no incumbent XPT config exists; shown for scale only)")

json.dump(dict(fits=dict(self_fit=dict(nu=nu_self if nu_self<200 else 250.0, mle_scale=round(s_self,3), width_cal=round(cal_self,3), windows=int(len(u_x))),
                          lono_gs=dict(nu=nu_gs if nu_gs<200 else 250.0, mle_scale=round(s_gs,3), width_cal=round(cal_gs,3), windows=int(len(u_g)+len(u_s))),
                          pooled3=dict(nu=nu_pool3 if nu_pool3<200 else 250.0, mle_scale=round(s_pool3,3), width_cal=round(cal_pool3,3))),
               scores=res,
               windows=dict(XPT=int(len(rx)), GOLD=int(len(rg)), SILVER=int(len(rs))),
               diag_self=cov_pit(rx, nu_self, cal_self), diag_lono=cov_pit(rx, nu_gs, cal_gs)),
          open('step0_results.json','w'), indent=1)
rx.to_csv('XPT_panel_60d.csv', index=False)
print("\nsaved step0_results.json, XPT_panel_60d.csv")
