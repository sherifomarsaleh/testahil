"""Run one study end-to-end: config -> Monte Carlo -> rendered markdown.
Usage: python pipeline/run.py data/PHDC.yaml"""
import sys, datetime, yaml
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
import montecarlo

ROOT = Path(__file__).resolve().parent.parent


def main(cfg_path):
    cfg = yaml.safe_load(open(cfg_path))
    mc = montecarlo.run(cfg)

    v = cfg["valuation"]
    sotp_gross = sum(p["value"] for p in v["sotp"])
    net_debt = v["net_debt_per_share"]
    base = round(sotp_gross - net_debt, 2)
    anchor = cfg["market"]["anchor"]
    base_pct = f"{(base/anchor-1)*100:+.0f}%"

    env = Environment(loader=FileSystemLoader(ROOT / "templates"),
                      trim_blocks=True, lstrip_blocks=True)
    html = env.get_template("study.md.j2").render(
        name=cfg["name"], ticker=cfg["ticker"], exchange=cfg["exchange"],
        ccy=cfg["currency"], anchor=anchor, shares_bn=cfg["market"]["shares_bn"],
        close_date=cfg["market"]["close_date"],
        today=datetime.date.today().isoformat(),
        sotp=v["sotp"], sotp_gross=sotp_gross, net_debt=net_debt,
        base_value=base, base_pct=base_pct,
        full_exec=v["full_execution"], bear=v["bear"],
        mc=mc, paths=cfg["montecarlo"]["paths"], seed=cfg["montecarlo"]["seed"],
        horizons=cfg["montecarlo"]["horizons_days"],
        touch_levels=cfg["touch_levels"],
    )
    out = ROOT / "studies" / f"{cfg['ticker']}.md"
    out.write_text(html)
    print(f"wrote {out}")


if __name__ == "__main__":
    main(sys.argv[1])
