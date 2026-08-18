---
description: Read-only health sweep of the live engine, ledger and published surfaces. Report only what changed.
argument-hint: "[optional: market code or ticker to narrow the sweep]"
allowed-tools: Bash, Read, Grep, Glob, WebFetch
---

# TESTAHIL pulse — the read-only watch

You are one tick of a standing watch. **Touch nothing.** No commits, no writes to
`assets/data.js`, no engine runs that mutate state. Your entire job is to look, compare
against the previous tick, and speak only when something is different or wrong.

Narrow the sweep to `$ARGUMENTS` if given; otherwise sweep everything.

## Read the live state FIRST — never from memory, never from a document

    python3 - <<'PY'
    import sys; sys.path.insert(0,'engine')
    import market_profiles as MP
    for c,p in sorted(MP.PROFILES.items()):
        print(c, 'nu=',p.nu, 'width_cal=',p.width_cal,
              'signal=',getattr(p,'signal_active',None),
              'width_overlay=',getattr(p,'width_overlay_active',None))
    PY

`market_profiles.py` is the single source of truth; `fitted_configs.json` is a derived
mirror. Every (ν, width_cal) refits whenever a stock is posted — quoting one from the
last tick is the exact staleness this watch exists to catch.

## The six checks

1. **Engine imports.** `python3 -c "import sys;sys.path.insert(0,'engine');import market_profiles,mc_v3,panel_refresh,data_quality,horizons,technicals,apply_technicals,ta_chart,wacc_builder,research_protocol,beta_regression,adaptive_width,rollforward_one"` — by IMPORT, never by parse. `nu=Gaussian` parses cleanly and only dies at import; that bug once reached `main` while a regex check called the file intact.

2. **JS surfaces load.** `node --check assets/data.js && node --check assets/app.js`, then actually load `data.js` and assert on the parsed objects — count `TICKERS` keys and `LEDGER` rows against the previous tick's total. A stitch point (a missing comma before an appended LEDGER row) is valid-looking text and invalid JavaScript, and counting containers cannot see fields vanishing from inside them.

3. **Maturity horizon.** List every open LEDGER row whose `grade_date` has arrived or lands inside the next 7 days:

       node -e "const fs=require('fs');const {LEDGER}=new Function(fs.readFileSync('assets/data.js','utf8')+';return {LEDGER};')();const T=new Date().toISOString().slice(0,10);const open=LEDGER.filter(r=>r.realized_close==null);const due=open.filter(r=>r.grade_date<=T);console.log('open',open.length,'| DUE NOW',due.length);due.forEach(r=>console.log(' DUE',r.instrument,r.horizon_label,r.grade_date));"

   Anything DUE NOW is a `/metronome` job, not a pulse job. Name it and stop there.

4. **Lifecycle invariant.** Exactly one open latest-anchor row per (instrument, horizon). A second one means a strike wrote twice.

5. **Freshness and staleness.** Run `python3 scripts/check_data_freshness.py`. Separately, flag any name where `asof.mc.data` is OLDER than `asof.tech.data` — the published cone is then stale relative to its own library. **Report it; never reconcile it silently.** Also list libraries whose newest session is more than 21 days behind that exchange's calendar.

6. **Review backlog.** `ls -t engine/PENDING_REVIEW/*.md` and the open `calibration-review-*` PRs. A material calibration change sitting unreviewed means production is running on the pre-change fit and nobody has decided.

## Output contract

- **Nothing changed since the last tick →** say so in one line. Nothing else.
- **Something changed →** lead with it, in the order above, with the numbers you actually read this tick beside the previous tick's. Three or four sentences.
- **A gate failed →** state the failure, the command that produced it, and the one next action. Do not fix it inside a pulse tick; a watch that repairs things silently is how a bad state becomes invisible.

Never quote a rating or a price target — fair-value ranges and distributions only.
