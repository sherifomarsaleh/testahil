"""direction_score.py — Phase B of the Fundamental / Monte-Carlo Integration Protocol.

Canonical spec: engine/Fundamental_MC_Integration_Protocol.md §7 test 2.

WHY THIS EXISTS
---------------
Every gate in this system scores CRPS. CRPS is a DISTRIBUTIONAL loss dominated by
the width term, so it is close to blind to direction: a signal with genuine
information moves the median by a fraction of sigma and barely registers. That is
not a hypothesis. It is the recorded cause of the last signal ablation —
`market_profiles.EGYPT.fit_meta`:

    "the empirical IC of rev_1m is +0.018 ... carry-only +0.0252 beats signal-ON
     +0.0211 ... paired bootstrap P(signal helps)=0.31"

A signal was rejected on a distributional metric without its DIRECTIONAL content
ever being scored on its own axis. This module is that axis. Nothing here replaces
CRPS — the two answer different questions and both must be reported.

WHAT IT SCORES
--------------
Given a signal and a realized forward return, per observation:

  IC          Spearman rank correlation, signal vs forward excess return.
              Block-bootstrapped to the house standard (blocks {2,3,4},
              5/95 percentiles, PASS/FAIL/PARITY/BOUNDARY per robust_verdict).
  hit rate    sign agreement, with a Wilson interval. The null is 50%.
  pinball@50  median-quantile loss of a signal-shifted median against the
              carry-only median. Skill = 1 - loss_signal / loss_carry.
  LONO        leave-one-NAME-out IC, so a single name cannot carry a verdict.

POWER IS PART OF THE OUTPUT, NOT A FOOTNOTE
-------------------------------------------
An IC point estimate on a handful of observations is noise with a decimal point.
`required_n()` reports how many observations would be needed to resolve a given
IC, and `score()` returns verdict INSUFFICIENT-POWER below `MIN_N` regardless of
what the bootstrap says. A wide CI that happens to exclude zero on n=6 is not
evidence, and this module will not report it as such.
"""
from __future__ import annotations

import math

import numpy as np
from scipy import stats

# Below this, no directional verdict is issued at all. 100 is not a power
# guarantee — it is the floor under which a rank correlation is not worth
# printing. See required_n() for what actually resolving a given IC costs.
MIN_N = 100

BOOT_BLOCKS = (2, 3, 4)     # house robust standard
N_BOOT = 3000
SEED = 42


# --------------------------------------------------------------------- power
def required_n(ic: float, power: float = 0.80, alpha: float = 0.05) -> int:
    """Observations needed to distinguish `ic` from zero, via the Fisher-z test."""
    if ic <= 0 or ic >= 1:
        return -1
    za = stats.norm.ppf(1 - alpha / 2)
    zb = stats.norm.ppf(power)
    return int(math.ceil(((za + zb) / math.atanh(ic)) ** 2 + 3))


def required_periods(ic: float, n_per_period: int, power: float = 0.80,
                     alpha: float = 0.05) -> int:
    """Cross-sections needed, via the Fundamental Law framing.

    The pooled `required_n` treats every name-date as one observation. The
    standard equity-factor alternative computes a CROSS-SECTIONAL IC each period
    and tests the mean of that series, where the sampling SD of a per-period IC
    on N names is ~1/sqrt(N-1). The two must agree, and they do: at N=31 this
    returns 26 periods = 810 name-observations against required_n(0.10)=783.
    Kept as an independent check on the headline number, not a replacement.
    """
    if ic <= 0 or n_per_period < 3:
        return -1
    t = stats.norm.ppf(1 - alpha / 2) + stats.norm.ppf(power)
    sd = 1.0 / math.sqrt(n_per_period - 1)
    return int(math.ceil((t * sd / ic) ** 2))


def accrual_eta(n_have: int, n_per_month: float, ic_target: float = 0.10):
    """Months until the sample can resolve `ic_target`, at a given accrual rate.

    A new observation needs a new MEASUREMENT DATE, not a new study: the gap
    moves whenever the price moves, so carrying the latest fair value forward and
    re-measuring monthly is a valid (and standard) way to accrue. Counting only
    dates when a fresh study lands gives an accrual rate near zero on the
    observed cadence, and an ETA of never.
    """
    need = required_n(ic_target)
    if n_per_month <= 0:
        return {"required_n": need, "months": None, "note": "never at this rate"}
    return {"required_n": need,
            "months": max(0.0, (need - n_have) / n_per_month),
            "months_to_min_n": max(0.0, (MIN_N - n_have) / n_per_month)}


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    """Wilson score interval for a proportion — behaves at small n, unlike normal."""
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return ((c - h) / d, (c + h) / d)


# ------------------------------------------------------------------ bootstrap
def _ic_ci(sig: np.ndarray, ret: np.ndarray, block: int,
           n_boot: int = N_BOOT, seed: int = SEED):
    """Block-bootstrap CI for Spearman IC. Mirrors fit_markets_20260710.verdict_ci."""
    n = len(sig)
    if n < block + 1:
        return float("nan"), float("nan"), "NOBLOCK"
    rng = np.random.default_rng(seed)
    boot = []
    for _ in range(n_boot):
        starts = rng.integers(0, n - block + 1, size=int(np.ceil(n / block)))
        idx = np.concatenate([np.arange(s, s + block) for s in starts])[:n]
        s, r = sig[idx], ret[idx]
        if np.std(s) == 0 or np.std(r) == 0:
            continue
        boot.append(stats.spearmanr(s, r).statistic)
    if not boot:
        return float("nan"), float("nan"), "NOBLOCK"
    lo, hi = np.percentile(boot, [5, 95])
    v = "PASS" if lo > 0 else ("FAIL" if hi < 0 else "PARITY")
    return float(lo), float(hi), v


def robust_ic_verdict(sig: np.ndarray, ret: np.ndarray):
    """House robust rule applied to IC: FAIL only if every block agrees."""
    detail = {b: _ic_ci(sig, ret, b) for b in BOOT_BLOCKS}
    verds = [detail[b][2] for b in BOOT_BLOCKS]
    if "NOBLOCK" in verds:
        return "PROVISIONAL(insufficient-windows)", detail
    if all(v == "FAIL" for v in verds):
        return "FAIL", detail
    if len(set(verds)) > 1:
        return "BOUNDARY(PARITY-flagged)", detail
    return verds[0], detail


# ---------------------------------------------------------------------- score
def score(signal, fwd_excess, names=None, ic_for_pinball: float | None = None,
          sigma=None, min_n: int = MIN_N):
    """Score a directional signal.

    signal      the standardized signal at the origin (e.g. G, or a z-score).
    fwd_excess  realized forward log return MINUS the carry drift — excess over
                the model's own null, not raw return. Scoring against raw return
                would credit the signal for the risk-free rate.
    names       per-observation name labels, for the leave-one-name-out pass.
    ic_for_pinball / sigma
                optional: build the signal-shifted median as alpha = ic*sigma*z
                (the Grinold form the engine already uses at mc_v3.py:114) and
                score its pinball@50 against the carry-only median. Omitted ->
                pinball is skipped rather than faked with an in-sample IC.
    """
    sig = np.asarray(signal, dtype=float)
    ret = np.asarray(fwd_excess, dtype=float)
    ok = np.isfinite(sig) & np.isfinite(ret)
    sig, ret = sig[ok], ret[ok]
    nm = np.asarray(names)[ok] if names is not None else None
    n = len(sig)

    out = {"n": n, "min_n": min_n}
    if n < 3 or np.std(sig) == 0 or np.std(ret) == 0:
        out["verdict"] = "INSUFFICIENT-POWER"
        out["note"] = f"n={n}: no rank correlation is defined"
        return out

    sp = stats.spearmanr(sig, ret)
    out["ic_spearman"] = float(sp.statistic)
    out["ic_p"] = float(sp.pvalue)
    out["ic_pearson"] = float(np.corrcoef(sig, ret)[0, 1])

    # hit rate — does the signal's sign match the realized excess move?
    nz = sig != 0
    hits = int(np.sum(np.sign(sig[nz]) == np.sign(ret[nz])))
    out["hit_rate"] = hits / max(int(nz.sum()), 1)
    out["hit_n"] = int(nz.sum())
    out["hit_ci"] = wilson(hits, int(nz.sum()))

    # pinball@50 vs the carry-only median (which predicts zero excess)
    if ic_for_pinball is not None and sigma is not None:
        sg = np.asarray(sigma, dtype=float)[ok]
        alpha = ic_for_pinball * sg * np.clip(sig, -2.0, 2.0)   # Grinold, clipped as engine does
        loss_sig = np.mean(np.abs(ret - alpha)) / 2.0
        loss_car = np.mean(np.abs(ret)) / 2.0
        out["pinball50_signal"] = float(loss_sig)
        out["pinball50_carry"] = float(loss_car)
        out["pinball50_skill"] = float(1 - loss_sig / loss_car) if loss_car else float("nan")

    verdict, detail = robust_ic_verdict(sig, ret)
    out["ic_ci_by_block"] = {b: {"lo": detail[b][0], "hi": detail[b][1],
                                 "verdict": detail[b][2]} for b in BOOT_BLOCKS}
    out["bootstrap_verdict"] = verdict

    # leave-one-NAME-out: no single name may carry the result
    if nm is not None and len(set(nm.tolist())) > 2:
        lono = {}
        for name in sorted(set(nm.tolist())):
            m = nm != name
            if m.sum() >= 3 and np.std(sig[m]) > 0 and np.std(ret[m]) > 0:
                lono[name] = float(stats.spearmanr(sig[m], ret[m]).statistic)
        if lono:
            v = list(lono.values())
            out["lono_ic"] = {"min": min(v), "max": max(v), "spread": max(v) - min(v),
                              "sign_stable": all(x > 0 for x in v) or all(x < 0 for x in v),
                              "by_name": lono}

    # the power gate overrides the bootstrap, always
    if n < min_n:
        out["verdict"] = "INSUFFICIENT-POWER"
        # Quote the sample size a REALISTIC IC needs, never the observed one. At
        # small n the observed |IC| is inflated by noise, so required_n(|IC_obs|)
        # flatters the sample — on n=5 an IC of -0.60 would "need n=20", which
        # reads as almost-there and is an artefact of the estimate it is derived
        # from. An equity value signal that survives is a 0.05-0.10 effect.
        out["note"] = (
            f"n={n} < {min_n}. IC {out['ic_spearman']:+.3f} is DESCRIPTIVE ONLY and "
            f"must not be promoted: at n={n} an estimate this large is far more "
            f"likely sampling noise than signal. Resolving a realistic value-signal "
            f"IC of 0.10 at 80% power needs n≈{required_n(0.10)} "
            f"(n≈{required_n(0.05)} at IC 0.05)."
        )
    else:
        out["verdict"] = verdict
    out["required_n_at_ic"] = {f"{x:.2f}": required_n(x) for x in (0.05, 0.10, 0.15, 0.20)}
    return out


def format_report(res: dict, title: str = "Direction score") -> str:
    L = [f"### {title}", ""]
    if "ic_spearman" not in res:
        return "\n".join(L + [f"- **{res['verdict']}** — {res.get('note','')}", ""])
    lo2 = res["ic_ci_by_block"][2]
    L += [f"- n = **{res['n']}**",
          f"- IC (Spearman) = **{res['ic_spearman']:+.3f}**  (p={res['ic_p']:.3f}, "
          f"Pearson {res['ic_pearson']:+.3f})",
          f"- IC 90% CI, block 2 = [{lo2['lo']:+.3f}, {lo2['hi']:+.3f}] → {lo2['verdict']}",
          f"- bootstrap verdict (blocks {list(BOOT_BLOCKS)}) = **{res['bootstrap_verdict']}**",
          f"- hit rate = **{res['hit_rate']:.1%}** on {res['hit_n']} "
          f"(95% CI {res['hit_ci'][0]:.1%}–{res['hit_ci'][1]:.1%}, null 50%)"]
    if "pinball50_skill" in res:
        L.append(f"- pinball@50 skill vs carry = **{res['pinball50_skill']:+.4f}**")
    if "lono_ic" in res:
        l = res["lono_ic"]
        L.append(f"- LONO IC range [{l['min']:+.3f}, {l['max']:+.3f}], "
                 f"sign stable: {l['sign_stable']}")
    L += [f"- **VERDICT: {res['verdict']}**"]
    if res.get("note"):
        L.append(f"  - {res['note']}")
    L += ["", "Observations needed to resolve an IC at 80% power: "
          + ", ".join(f"{k}→{v}" for k, v in res["required_n_at_ic"].items()), ""]
    return "\n".join(L)


if __name__ == "__main__":
    # self-check: a planted IC must be recovered, and pure noise must not pass
    rng = np.random.default_rng(0)
    n = 400
    s = rng.standard_normal(n)
    r = 0.15 * s + rng.standard_normal(n)          # planted IC ~0.15
    print(format_report(score(s, r, names=[f"N{i%20}" for i in range(n)]),
                        "self-check: planted IC 0.15"))
    r0 = rng.standard_normal(n)                    # pure noise
    print(format_report(score(s, r0, names=[f"N{i%20}" for i in range(n)]),
                        "self-check: pure noise"))
