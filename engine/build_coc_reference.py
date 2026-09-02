"""Generate engine/Cost_of_Capital_Reference.md from the house macro paths.

The protocol has referenced this file since July 2026 — `wacc_builder.py` and
`market_profiles.py` both name it — and it has never existed. It is written now,
and it is GENERATED, never typed: a document that states a fact which moves must
not be the thing that remembers it, the same rule the as-of stamps and the band
records obey. Every number here resolves from engine/macro_paths/*.json at build
time, so a stale figure fails the build instead of printing.

    python3 engine/build_coc_reference.py
"""
import datetime as dt
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import macro_path as MP                                          # noqa: E402

OUT = os.path.join(HERE, "Cost_of_Capital_Reference.md")


def main():
    L = []
    w = L.append
    w("# Cost of capital — the reference tables, generated\n")
    w("**GENERATED from `engine/macro_paths/*.json` by `engine/build_coc_reference.py`. "
      "Never hand-edited.** Every figure below resolves from a committed macro path at "
      "build time; a number whose source has moved fails the build rather than printing "
      "stale. To change a figure, change the path file and re-run this.\n")
    w("Rebuilt %s. Read the live state, never this file from memory — it is regenerated "
      "whenever a path is re-sourced.\n" % dt.date.today().isoformat())
    w("\n## What is held\n")
    w("| Market | State | Regime | Currency |")
    w("|---|---|---|---|")
    for m, state in MP.held().items():
        try:
            p = MP.load(m)
            w("| %s | sourced, as of %s | %s | %s |" % (m, p.as_of, p.regime, p.currency))
        except MP.MacroPathError:
            w("| %s | **pending** | — | — |" % m)
    w("\nA market reading **pending** RAISES on load. There is no fallback to a "
      "neighbouring market, a region or a global average: an empty answer is not a clean "
      "answer, and the cost of a missing path is a study that stops, not a study built on "
      "a number nobody sourced.\n")

    for m in MP.MARKETS:
        try:
            p = MP.load(m)
        except MP.MacroPathError as e:
            continue
        n = len(p.inflation_path)
        w("\n---\n\n## %s — %s\n" % (p.market, p.currency))
        w("Regime: **%s**. %s\n" % (p.regime, p.raw.get("regime_note", "")))
        w("\n### Inflation\n")
        w("| Year | Rate | Basis |")
        w("|---|---:|---|")
        for r in p.raw["inflation"]["path"]:
            w("| %d | %.2f%% | %s |" % (r["year"], 100 * r["value"], r["basis"]))
        w("| terminal | %.2f%% | %s |"
          % (100 * p.terminal_inflation, "the target band midpoint in force"))
        w("\nLatest print: **%.2f%%** (%s). Target: **%.1f%% ± %.1fpp**, %s.\n"
          % (100 * p.inflation_latest, p.raw["inflation"]["latest"]["period"],
             100 * p.target["value"], 100 * p.target.get("band", 0), p.target["horizon"]))
        w("\n### Rates\n")
        w("| | Value | As of |")
        w("|---|---:|---|")
        w("| Policy rate | %.2f%% | %s |"
          % (100 * p.policy_rate, p.raw["policy_rate"]["current"]["date"]))
        w("| Sovereign 10-year | %.2f%% | %s (%d days old) |"
          % (100 * p.sovereign_10y, p.sovereign_asof, p.sovereign_age_days()))
        w("| Default spread, rating basis | %.2f%% | |" % (100 * p.default_spread("rating")))
        w("| Default spread, swap basis | %.2f%% | |" % (100 * p.default_spread("cds")))
        w("| Terminal cost of debt | %.2f%% | long-run corporate norm |" % (100 * p.kd_terminal))
        w("| Terminal equity risk premium | %.2f%% | normalised |" % (100 * p.erp_terminal))
        w("\n**Policy-rate path** (the SHAPE input for the cost-of-capital glide, never a "
          "second free parameter): " + " → ".join("%.2f%%" % (100 * x) for x in p.policy_path) + "\n")
        w("\n### The derived terminal\n")
        w("Nothing in this block is a quote. Each line is an identity on the numbers above, "
          "because a terminal rate reverse-engineered from a price is the quietest lever "
          "there is.\n")
        w("| | Identity | Value |")
        w("|---|---|---:|")
        w("| Terminal risk-free | terminal inflation + real-rate convention (%.2f%%) | **%.2f%%** |"
          % (100 * p.real_rate_convention, 100 * p.terminal_rf))
        w("| Terminal growth, zero real | terminal inflation + stated real growth (0.00%%) | **%.2f%%** |"
          % (100 * p.terminal_growth()))
        w("\n### The currency, derived\n")
        w("Relative purchasing-power parity on this path's own inflation against long-run "
          "United States inflation of %.2f%%. A study may not set this by hand.\n"
          % (100 * p.us_inflation_lt))
        w("| Year | Depreciation | %s |" % ("USD/%s" % p.currency))
        w("|---|---:|---:|")
        for i, (d_, f_) in enumerate(zip(p.depreciation_path(n), p.fx_path(n))):
            w("| %d | %.2f%% | %.2f |" % (p.inflation_years[i], 100 * d_, f_))
        w("\n### Sources\n")
        for k, v in p.sources().items():
            w("- **%s** — %s" % (k, v))

    w("\n---\n")
    w("\n## The rules these tables serve\n")
    w("- **One economy, one inflation.** Every growth rate in a model is stored as a real "
      "rate against a path id and recomputes to its nominal; a typed nominal rate is "
      "unfalsifiable and is refused. [L-048]")
    w("- **Terminal growth agrees with the inflation inside the terminal discount rate.** "
      "Growth below it is a perpetual real decline, which may be assumed but must be "
      "stated as the real number it is. [L-055]")
    w("- **The terminal risk-free rate is derived, never quoted.**")
    w("- **The explicit window runs until growth has converged on terminal** (within 2pp), "
      "so the terminal does not capitalise a rate the model never reached.")
    w("- **A sovereign quote older than %d days is re-sourced before a strike.**"
      % MP.SOVEREIGN_STALE_DAYS)
    w("\nEnforced from outside by `scripts/check_macro_coherence.py`, negative-controlled by "
      "`scripts/check_macro_coherence_negative_control.py`, both in CI. [R-MACRO-01], [R-ENF-01]\n")

    open(OUT, "w", encoding="utf-8").write("\n".join(L))
    print("wrote %s (%d lines)" % (os.path.relpath(OUT, os.path.dirname(HERE)), len(L)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
