"""Emit a data.js-format ticker block from one config file.
fair.base is computed from the SOTP I own; dist/touch use the published study
figures (byte-consistent with the downloadable PDF). The MC engine is run only
to VALIDATE that the owned 10 factors reproduce those published figures.
Usage: python pipeline/gen_datajs.py data/PHDC.yaml > output/PHDC.data.js"""
import sys, yaml
from pathlib import Path
import montecarlo

ROOT = Path(__file__).resolve().parent.parent


def fmt(x):
    s = f"{x:.2f}".rstrip("0").rstrip(".")
    return s


def main(cfg_path):
    cfg = yaml.safe_load(open(cfg_path))
    v, s = cfg["valuation"], cfg["site"]
    # base derivation, most-specific first:
    #  1) explicit base (reconciled to the published study), else
    #  2) signed-component bridge (holding cos: + segments + net cash − minority), else
    #  3) PHDC-style: sum of SOTP rows − net debt
    if v.get("base") is not None:
        base = round(v["base"], 2)
    elif v.get("components"):
        base = round(sum(c["value"] for c in v["components"]), 2)
    else:
        base = round(sum(p["value"] for p in v["sotp"]) - v["net_debt_per_share"], 2)

    # --- validation: do my 10 factors reproduce the published distribution? ---
    mc = montecarlo.run(cfg)
    pub = cfg["published_dist"]
    drift = max(abs(mc["percentiles"][60][50] - pub["t60"]["p50"]),
                abs(mc["percentiles"][20][50] - pub["t20"]["p50"]))
    sys.stderr.write(f"[validate] engine vs published median drift = {drift:.2f} EGP\n")

    d20, d60 = pub["t20"], pub["t60"]
    touch = ",\n      ".join(f"[{fmt(l)}, {a}, {b}]" for l, a, b in cfg["published_touch"])
    res = ", ".join(fmt(x) for x in s["levels"]["res"])
    sup = ", ".join(fmt(x) for x in s["levels"]["sup"])
    t = s["tech"]

    block = f"""  {cfg['ticker']}: {{
    name: "{cfg['name']}",
    code: "{cfg['exchange']}:{cfg['ticker']}",
    spot: {fmt(s['spot'])},
    spotDate: "{s['spot_date']}",
    ccy: "{cfg['currency']}",
    fair: {{ bear: {fmt(v['bear'])}, base: {fmt(base)}, full: {fmt(v['full_execution'])} }},
    dist: {{
      t20: {{ label:"1 month (T+20)",  p5:{fmt(d20['p5'])}, p25:{fmt(d20['p25'])}, p50:{fmt(d20['p50'])}, p75:{fmt(d20['p75'])}, p95:{fmt(d20['p95'])}, resolve:"{s['resolve_t20']}" }},
      t60: {{ label:"3 months (T+60)", p5:{fmt(d60['p5'])}, p25:{fmt(d60['p25'])}, p50:{fmt(d60['p50'])}, p75:{fmt(d60['p75'])}, p95:{fmt(d60['p95'])}, resolve:"{s['resolve_t60']}" }}
    }},
    touch: [
      {touch}
    ],
    levels: {{ res:[{res}], sup:[{sup}] }},
    tech: {{
      trend: "{t['trend']}",
      summary: "{t['summary']}",
      bull: "{t['bull']}",
      bear: "{t['bear']}"
    }},
    files: {{
      study: "{s['files']['study']}",
      model: "{s['files']['model']}",
      pdf:   "{s['files']['pdf']}"
    }},
    page: {{
      floor: "{cfg['page']['floor']}",
      resDetail: "{cfg['page']['resDetail']}",
      supDetail: "{cfg['page']['supDetail']}",
      atr: "{cfg['page']['atr']}",
      breakBelow: "{cfg['page']['breakBelow']}"
    }}
  }}"""
    print(block)


if __name__ == "__main__":
    main(sys.argv[1])
