# AMOC — the synthetic-open escalation: DEFAULT TAKEN

**SYNTHETIC-OPEN DEFAULT TAKEN, 17 September 2026.**

`engine/escalations.json` → `AMOC-real-open-ohlc-export`, opened 6 September, default date
**13 September**. The date passed and no real-open export arrived. [R-IND-01] is explicit that
a gate with no release is a stall and that **when the date arrives the default is taken and
the entry closed**, so it is taken here rather than left open to be asked again.

## What the default is, verbatim from the register

> AMOC's cohort is NOT struck on the synthetic-open bars. Measured two independent ways, they
> understate the origin variance enough to publish a 90% band 16–19% too narrow (close-to-close
> route) or 13–16% (open-free Parkinson route) — past [R-CAL-01]'s own 5% materiality line, and
> a LEDGER row is permanent. The cone therefore stays at its 2026-08-06 strike.

## What that means in practice, and it is nothing new

**No artefact changes.** The cone already sits at its 2026-08-06 strike; taking the default
means confirming that it stays there, not moving it. The divergence between `asof.mc.data` and
the library's last session stands and is reported rather than reconciled silently, which is
what the as-of stamps exist to make visible.

**THE LIBRARY IS NOT MARKED AND THAT IS DELIBERATE.** The register's own note planned for the
marker to go in a comment line at the top of `engine/raw_ohlc/EG/AMOC.csv`. That was written
for the case where the real export ARRIVES. Writing `REAL-OPEN EXPORT RECEIVED` into that file
now would be a false statement in the repository about a document nobody has supplied — and
the library is a plain CSV with no comment convention, read by `pandas.read_csv` with no
comment character, so a leading `#` line would be parsed as data. The marker is here instead.

## What would reopen this

A vendor export for AMOC carrying **real opening prices** for the twenty sessions from
2026-08-07 to 2026-09-06. On arrival: splice, re-run Step 0.0, and re-strike the cone on the
corrected series — at which point the 16–19% band understatement this default exists to avoid
no longer applies. **The measurement is not withdrawn by this default; only the waiting is.**
