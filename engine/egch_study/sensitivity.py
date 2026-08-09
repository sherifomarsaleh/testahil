"""Whole-model re-run grid: value per share across the export-price / terminal-rate plane.
Each cell re-runs compute.py's own engine end to end — which is exactly why the grid is
pasted into the workbook and labelled as not redrawing."""
import json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import importlib.util
spec = importlib.util.spec_from_file_location("cmp", os.path.join(HERE, "compute.py"))
PRICES = [380.0, 420.0, 460.0, 500.0, 540.0]
WACCS = [0.17, 0.185, 0.204, 0.22, 0.24]
grid = []
for p in PRICES:
    row = []
    for w in WACCS:
        cmp = importlib.util.module_from_spec(spec)
        import io, contextlib
        with contextlib.redirect_stdout(io.StringIO()):
            spec.loader.exec_module(cmp)
            cmp.D['export_usd_path'] = [p + 90, p + 60, p + 30, p + 10, p]
            cmp.D['wacc_terminal'] = w
            rws = cmp.build("base")
            T = cmp.terminal(rws, "base")
            b = cmp.bridge(rws, T)
        row.append(b['per_share'])
    grid.append(row)
json.dump(dict(prices=PRICES, waccs=WACCS, grid=grid),
          open(os.path.join(HERE, 'sensitivity_grid.json'), 'w'), indent=1)
for p, row in zip(PRICES, grid):
    print(f"${p:.0f}/t: " + "  ".join(f"{v:7.2f}" for v in row))
