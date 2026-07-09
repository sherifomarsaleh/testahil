"""
Testahil — study runner (orchestrator).

Given a ticker and its OHLC CSV, runs the deterministic spine of the Standing Research Protocol
end-to-end:

  1. load OHLC, classify the ticker, split the factor set
  2. Step 0 calibration backtest with the CLASS-DEFAULT drift; if it fails the CRPS gate, apply the
     protocol's recalibration lever (flip the asset-class secular drift off) and re-run, adopting
     whichever configuration has the higher skill — and FLAG if neither beats the benchmark
  3. full mc_v2 run (50,000 paths, seed 42) at the last close, with the adopted drift
  4. probability read + percentile table + touch levels
  5. house figures (fan / distributions / touch ladder / PIT / MA-stack)
  6. Excel model (16 sheets, Assumptions-linked, wired DCF) + LibreOffice recalculation
  7. Word study skeleton (quantitative tables wired; narrative left for the analyst / model)
  8. machine-run QC gate -> filled evidence table

What the runner does NOT do (this is the honest vendor-dependency line): pull the financials from
filings (Step 2) and author the §1 narrative and the three-expert appendix. Those are the analyst /
model layer that sits on top of this spine. The runner produces the quantitative study, the linked
model, the figures, and the scaffolded document + an honest QC table showing exactly what remains.

CLI:  python study_runner.py <ohlc_csv> <TICKER> [out_dir] [shares_mn]
"""
from __future__ import annotations
import os, sys, subprocess
import numpy as np

import data_io, factor_library as fl, mc_v2, step0_backtest as s0
import house_figures as hf, model_builder as mb, report_builder as rb, qc_gate as qc

RE_CLASSES = {"egx_developer"}
F_CLASSES = {"egx_payments", "egx_holdco", "egx_contractor"}


def _exch_for(cls):
    return "EGX" if cls.startswith("egx_") else ("METAL" if cls == "metals" else "—")


def _prob_read(res):
    col = res.paths[:, -1]; spot = res.anchor
    p_up = float((col > spot).mean()); p10 = float((col > spot*1.1).mean()); pm10 = float((col < spot*0.9).mean())
    med = float(np.percentile(col, 50))
    lo, hi = float(np.percentile(col, 25)), float(np.percentile(col, 75))
    odds = (p10 / pm10) if pm10 > 0 else float("inf")
    return [
        ("P(price > spot)", f"{p_up:.0%}"),
        ("P(+10%) vs P(−10%)", f"{p10:.0%} vs {pm10:.0%}  (odds {odds:.2f}×)"),
        ("Median level / % move", f"{med:.2f}  ({med/spot-1:+.1%})"),
        ("50% band (25th–75th)", f"{lo:.2f} – {hi:.2f}  ({(hi-lo)/spot:.0%} of spot)"),
        ("Touch +10% / −10%", f"{res.touch_probability(spot*1.1, res.horizon):.0%} / "
                              f"{res.touch_probability(spot*0.9, res.horizon):.0%}"),
    ]


def _technicals(close):
    c = np.asarray(close, float)
    def sma(n): return float(c[-n:].mean()) if len(c) >= n else float("nan")
    last = float(c[-1])
    def sig(ma): return "above" if last > ma else "below"
    rows = []
    for n in (20, 50, 100, 200):
        ma = sma(n); rows.append([f"Price vs SMA{n}", f"{last:.2f} vs {ma:.2f}", sig(ma)])
    # simple RSI(14)
    d = np.diff(c[-15:]) if len(c) >= 15 else np.array([0.0])
    up = d[d > 0].sum(); dn = -d[d < 0].sum()
    rsi = 100 - 100 / (1 + (up / dn)) if dn > 0 else 100.0
    rows.append(["RSI (14)", f"{rsi:.0f}", "overbought" if rsi > 70 else "oversold" if rsi < 30 else "neutral"])
    return rows


def _recalc(xlsx_path):
    """Recalculate formulas with LibreOffice so cached values populate and errors are checkable."""
    for cand in ("/mnt/skills/public/xlsx/scripts/recalc.py",):
        if os.path.exists(cand):
            try:
                subprocess.run([sys.executable, cand, xlsx_path], check=True,
                               capture_output=True, timeout=180)
                return True
            except Exception as e:
                print(f"  [recalc] skill script failed ({e}); values compute on open.")
                return False
    return False


def run_study(ticker, csv_path, out_dir, shares_mn=1000.0):
    os.makedirs(out_dir, exist_ok=True)
    ohlc = data_io.load_ohlc(csv_path)
    cls, factors = fl.for_ticker(ticker)
    cont, events = fl.split(factors)
    spot = float(ohlc["close"][-1]); close_date = ohlc["date"][-1].strftime("%d %b %Y")
    exch = _exch_for(cls)
    print(f"\n{ticker}  ({exch}) — class {cls} — spot {spot:.2f} @ {close_date} — "
          f"{len(ohlc['close'])} sessions\n")

    # ---- Step 0 with auto-recalibration of the drift lever ----
    default_ac = cls if cls in mc_v2._SECULAR_DRIFT_CLASSES else None
    r_default = s0.run_step0(ticker, ohlc, cont, asset_class=default_ac)
    drift_on = cls in mc_v2._SECULAR_DRIFT_CLASSES
    chosen = r_default; chosen_ac = default_ac; note = f"class-default drift ({'on' if drift_on else 'off'})"
    if drift_on and not r_default.passed:
        r_off = s0.run_step0(ticker, ohlc, cont, asset_class=None)
        if r_off.crps_skill > r_default.crps_skill:
            chosen, chosen_ac = r_off, None
            note = ("class-default secular drift FAILED Step 0; recalibration lever applied "
                    "(secular drift OFF) — the higher-skill configuration")
    print(step0_line := chosen.summary())
    print(f"  [calibration] {note}")
    if not chosen.passed:
        print("  [FLAG] Neither configuration beats the RW benchmark — flag to analyst before publishing.")

    # ---- full run at spot ----
    res = mc_v2.run(anchor=spot, realized_vol=0.0, continuous=cont, events=events,
                    horizon=60, n_paths=50_000, seed=42, ohlc=ohlc, asset_class=chosen_ac)
    levels = [round(spot * m, 2) for m in (0.8, 0.9, 1.0, 1.1, 1.2, 1.3)]

    # ---- figures ----
    figs = {
        "fan": hf.fan_chart(res, levels, os.path.join(out_dir, f"{ticker}_fan.png"), ticker),
        "dist": hf.dist_figs(res, os.path.join(out_dir, f"{ticker}_dist.png")),
        "ladder": hf.touch_ladder(res, levels, os.path.join(out_dir, f"{ticker}_ladder.png")),
        "pit": hf.pit_hist(chosen.pit, os.path.join(out_dir, f"{ticker}_pit.png")),
        "ma": hf.ma_stack(ohlc["close"], os.path.join(out_dir, f"{ticker}_ma.png"), ticker),
    }

    # ---- Excel ----
    xlsx_path = os.path.join(out_dir, f"{ticker}_model.xlsx")
    mb.build_model(xlsx_path, ticker, spot, shares_mn, res)
    _recalc(xlsx_path)

    # ---- Word ----
    docx_path = os.path.join(out_dir, f"{ticker}_study.docx")
    ctx = {
        "ticker": ticker, "exch": exch, "company": ticker, "spot": spot, "close_date": close_date,
        "shares": shares_mn, "mkt_cap": f"{spot*shares_mn:,.0f} (spot × shares)",
        "thesis": "educational fair-value & probability study", "asset_class": cls,
        "prob_read": _prob_read(res), "technicals": _technicals(ohlc["close"]),
        "mc_percentiles": res.percentile_table(), "step0": chosen, "figures": figs,
    }
    rb.build_report(docx_path, ctx)

    # ---- QC ----
    rows, ok = qc.run_qc(docx_path, xlsx_path, chosen, is_re=(cls in RE_CLASSES),
                         is_f_class=(cls in F_CLASSES))
    print("\n" + qc.format_table(rows))
    print(f"\n  Artifacts written to {out_dir}:")
    for f in sorted(os.listdir(out_dir)):
        print("   ", f)
    print("\n  Note: financials (Step 2) and the §1 narrative + three-expert appendix are the "
          "analyst/model layer authored on top of this spine.")
    return {"step0": chosen, "mc": res, "docx": docx_path, "xlsx": xlsx_path, "qc": rows}


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("usage: python study_runner.py <ohlc_csv> <TICKER> [out_dir] [shares_mn]")
        sys.exit(1)
    csv = sys.argv[1]; tk = sys.argv[2].upper()
    out = sys.argv[3] if len(sys.argv) > 3 else f"./out_{tk}"
    sh = float(sys.argv[4]) if len(sys.argv) > 4 else 1000.0
    run_study(tk, csv, out, sh)
