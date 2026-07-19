/* testahil — app.js : quantile-dotplot strip + plain-language odds + ledger + calculator */

const F = n => Number(n).toLocaleString("en-US",{maximumFractionDigits:2});

/* ---------- percentile helpers ----------
   We store p5/p25/p50/p75/p95. To draw the dotplot and to state plain-language
   odds we build a piecewise-linear inverse-CDF from those five anchors and
   sample evenly-spaced quantiles. An approximation of the full Monte Carlo,
   which is all five summary points allow — the caption is honest about that. */
function invCDF(d){
  const pts = [[0.05,d.p5],[0.25,d.p25],[0.50,d.p50],[0.75,d.p75],[0.95,d.p95]];
  return p => {
    if(p <= pts[0][0]){ const [p1,v1]=pts[0],[p2,v2]=pts[1];
      return Math.max(v1-(v2-v1)*((p1-p)/(p2-p1)), v1*0.80); }
    if(p >= pts[4][0]){ const [p1,v1]=pts[3],[p2,v2]=pts[4];
      return v2+(v2-v1)*((p-p2)/(p2-p1)); }
    for(let i=0;i<pts.length-1;i++){ const [pa,va]=pts[i],[pb,vb]=pts[i+1];
      if(p>=pa&&p<=pb) return va+(vb-va)*((p-pa)/(pb-pa)); }
    return d.p50;
  };
}
function probAbove(d, price){
  const f = invCDF(d);
  if(price <= f(0.001)) return 0.99;
  for(let p=0.002;p<=0.999;p+=0.001){
    if(f(p) >= price) return Math.min(0.99, Math.max(0.01, 1-p));
  }
  return 0.01;
}

/* ---------- plain-language odds sentence (natural-frequency framing) ---------- */
function plainOdds(d, spot){
  const pa = probAbove(d, spot);
  const up10 = Math.round(pa*10), down10 = 10-up10;
  let lead;
  if(pa >= 0.60)      lead = "More likely to rise than fall";
  else if(pa <= 0.40) lead = "More likely to fall than rise";
  else                lead = "Could go either way";
  return {
    lead,
    sentence: `Out of 10 possible outcomes, about <b>${up10}</b> end higher than the latest price and about <b>${down10}</b> end lower.`,
    pa
  };
}

/* ---------- probability strip → horizontal range bar (signature element) ----------
   A simple slider: the thin bar is the wide "almost-anything" range (5%–95%),
   the thick bar is the most-likely middle half (25%–75%), the upright mark is
   the middle outcome, and the gold dot is today's price. Plain words sit under
   the ends. No statistics jargon on the face of it. */
function renderStrip(elId, d, spot, opts={}){
  const el = document.getElementById(elId); if(!el) return;
  const asof = opts.asof;
  const min = Math.min(d.p5, spot) - (Math.max(d.p95,spot)-Math.min(d.p5,spot))*0.06;
  const max = Math.max(d.p95, spot) + (Math.max(d.p95,spot)-Math.min(d.p5,spot))*0.06;
  const mob = (typeof window!=="undefined" && window.innerWidth < 640);
  const fLab = mob ? 30 : 19, fBand = mob ? 26 : 16, fDate = mob ? 20 : 13;
  // vertical positions: spread the label rows further apart on mobile (bigger text)
  const W = 1000;
  const H = mob ? 204 : 152, y = mob ? 92 : 72;
  const topY = mob ? y-78 : y-54;   // extremes + middle row
  const bandY = mob ? y-40 : y-26;  // 25/75 row
  const todY = mob ? y+58 : y+44;   // latest-price row
  const dateY = mob ? y+92 : y+62;  // as-of date row
  const X = v=>40+(v-min)/(max-min)*(W-80);

  el.innerHTML = `<svg viewBox="0 0 ${W} ${H}" xmlns="http://www.w3.org/2000/svg" role="img"
      aria-label="Likely price range. The latest price is ${F(spot)}; the middle outcome is ${F(d.p50)}. Half of outcomes fall between ${F(d.p25)} and ${F(d.p75)}.">
    <style>
      .lab{font:600 ${fLab}px 'IBM Plex Mono',monospace}
      .end{fill:#8A9A98}.mid{fill:#12796B}.tod{fill:#C0A45F}
      .band{fill:#12796B;font-size:${fBand}px}
      .dat{font:500 ${fDate}px 'IBM Plex Mono',monospace;fill:#8A9A98}
    </style>
    <!-- wide range 5–95% -->
    <line x1="${X(d.p5)}" x2="${X(d.p95)}" y1="${y}" y2="${y}" stroke="#D9E4E2" stroke-width="12" stroke-linecap="round"/>
    <!-- middle half 25–75% -->
    <line x1="${X(d.p25)}" x2="${X(d.p75)}" y1="${y}" y2="${y}" stroke="#178A76" stroke-width="22" stroke-linecap="round" opacity=".55"/>
    <!-- middle outcome mark -->
    <line x1="${X(d.p50)}" x2="${X(d.p50)}" y1="${y-20}" y2="${y+20}" stroke="#12796B" stroke-width="6" stroke-linecap="round"/>
    <!-- latest-price mark -->
    <circle cx="${X(spot)}" cy="${y}" r="11" fill="#fff" stroke="#C0A45F" stroke-width="4"/>
    <!-- TOP row above the bar: rare extremes + middle outcome -->
    <text x="${X(d.p50)}" y="${topY}" text-anchor="middle" class="lab mid">middle ${F(d.p50)}</text>
    <text x="${X(d.p5)}" y="${topY}" text-anchor="middle" class="lab end">${F(d.p5)}</text>
    <text x="${X(d.p95)}" y="${topY}" text-anchor="middle" class="lab end">${F(d.p95)}</text>
    <!-- LOWER row, just above the bar: the 25%–75% middle-half edges -->
    <text x="${X(d.p25)}" y="${bandY}" text-anchor="middle" class="lab band">${F(d.p25)}</text>
    <text x="${X(d.p75)}" y="${bandY}" text-anchor="middle" class="lab band">${F(d.p75)}</text>
    <!-- latest price below the bar -->
    <text x="${X(spot)}" y="${todY}" text-anchor="middle" class="lab tod">latest ${F(spot)}</text>
    ${asof?`<text x="${X(spot)}" y="${dateY}" text-anchor="middle" class="dat">${asof}</text>`:""}
  </svg>`;
}

function stripLegend(){
  return `<div class="legend">
    <span><i class="sw" style="background:#178A76;opacity:.55;border-radius:3px"></i> where it lands half the time</span>
    <span><i class="sw" style="background:#D9E4E2;border-radius:3px"></i> almost the whole range (9 times in 10)</span>
    <span><i class="sw" style="background:#fff;border:3px solid #C0A45F"></i> latest price</span>
  </div>`;
}

/* "plain answer + dotplot + sentence" block — identical everywhere it's used */
function renderPlain(containerId, d, spot, horizonLabel, asof){
  const c = document.getElementById(containerId); if(!c) return;
  const o = plainOdds(d, spot);
  c.innerHTML = `
    <p class="odds-sentence">${o.sentence}</p>
    <div class="strip" id="${containerId}-strip"></div>
    <p class="muted strip-note">The teal band is where the price lands most of the time ${horizonLabel}. The thin band is the rare extremes. The gold dot is the latest price.</p>
  `;
  renderStrip(`${containerId}-strip`, d, spot, {asof});
}

/* ---------- public ledger helper (kept) ---------- */
/* derived status from the universal ledger row: open until graded */
function ledgerStatus(r){ return (r.realized_close==null) ? "open" : "graded"; }

function buildLedger(tbodyId, summaryId){
  const tb=document.getElementById(tbodyId); if(!tb) return;
  let hit=0, scored=0;
  // newest anchor first, then longer horizon first
  const rows=[...LEDGER].sort((a,b)=> b.anchor_date.localeCompare(a.anchor_date) || b.horizon_label.localeCompare(a.horizon_label));
  tb.innerHTML = rows.map(r=>{
    let res;
    if(ledgerStatus(r)==="open"){
      const d=new Date(r.grade_date).toLocaleDateString('en-GB',{day:'numeric',month:'short',year:'numeric'});
      res = `<span class="chip">waiting — we'll know on ${d}</span>`;
    } else {
      scored++; const inBand = (r.in_90!=null) ? r.in_90 : (r.realized_close>=r.p5 && r.realized_close<=r.p95); if(inBand) hit++;
      res = `<span class="num">${F(r.realized_close)}</span> ${inBand?'<span class="ok">landed in range ✓</span>':'<span class="bad">outside range ✗</span>'}`;
    }
    const _slug = String(r.instrument).toLowerCase();
    const _inst = `<a class="ledger-link" href="${_slug}.html#mc-lab">${r.instrument}</a>`;
    return `<tr><td class="num">${r.anchor_date}</td><td>${_inst}</td><td class="num">${r.horizon_label}</td>
      <td class="num">${F(r.p50)}</td><td class="num">${F(r.p5)} – ${F(r.p95)}</td><td>${res}</td></tr>`;
  }).join("");
  const sm=document.getElementById(summaryId);
  const firstGrade=[...LEDGER].sort((a,b)=>a.grade_date.localeCompare(b.grade_date))[0].grade_date;
  if(sm) sm.textContent = scored
    ? `Our range contained the real price in ${hit} of ${scored} forecasts we've graded so far.`
    : `Nothing graded yet — first forecast comes due on ${new Date(firstGrade).toLocaleDateString('en-GB',{day:'numeric',month:'short',year:'numeric'})}. Everything we publish stays here, right or wrong.`;
}

/* ---------- calculator ---------- */
function runCalc(){
  const amt=+document.getElementById("c-amt").value||0;
  const y1=+document.getElementById("c-from").value, y2=+document.getElementById("c-to").value;
  const out=document.getElementById("c-out");
  if(y2<=y1){out.innerHTML='<p class="bad">End year must be after start year.</p>';return;}
  const i1=CALC.years.indexOf(y1), i2=CALC.years.indexOf(y2);
  let cpi=1; for(let k=i1+1;k<=i2;k++) cpi*=1+CALC.inflation[k]/100;
  let cd=amt; for(let k=i1+1;k<=i2;k++) cd*=1+CALC.cdRate[k]/100;
  let usdGrow=1; for(let k=i1+1;k<=i2;k++) usdGrow*=1+(CALC.usdRate[k]||0)/100;   // USD deposit interest, compounded
  const usd = amt*CALC.usdEgp[i2]/CALC.usdEgp[i1]*usdGrow;   // buy USD, earn USD interest, convert back to EGP
  const gold= amt*CALC.gold21g[i2]/CALC.gold21g[i1];
  const egx = amt*CALC.egx30[i2]/CALC.egx30[i1];
  const rows=[["Egyptian pound CD",cd],["US-dollar CD",usd],["Gold (21k)",gold],["EGX30 index",egx]]
    .sort((a,b)=>b[1]-a[1]);
  const maxV=rows[0][1];
  out.innerHTML = `<table><thead><tr><th>Where you put it</th><th class="num">What you'd have</th><th class="num">Really worth</th><th style="width:38%"></th></tr></thead><tbody>`+
    rows.map(([n,v])=>{const real=v/cpi; const pct=Math.max(4,v/maxV*100);
      return `<tr><td>${n}</td><td class="num">${F(v)}</td><td class="num">${F(real)}</td>
      <td><div style="background:${real>=amt?'#2E7D5B':'#B5483A'};opacity:.85;height:14px;border-radius:7px;width:${pct}%"></div></td></tr>`;}).join("")+
    `</tbody></table>
    <p class="muted">A red bar means that even though the number grew, it bought less than when you started.</p>`;
  const rc=document.getElementById("real-chart");
  if(rc){
    const rr=rows.map(([n,v])=>[n,(v/cpi/amt-1)*100]).sort((a,b)=>b[1]-a[1]);
    const maxAbs=Math.max(...rr.map(x=>Math.abs(x[1])),1);
    rc.innerHTML = `<table><thead><tr><th>Where you put it</th><th class="num">After inflation</th><th style="width:46%"></th></tr></thead><tbody>`+
      rr.map(([n,p])=>{const w=Math.max(4,Math.abs(p)/maxAbs*100); const c=p>=0?'#2E7D5B':'#B5483A';
        return `<tr><td>${n}</td><td class="num">${p>=0?'+':'−'}${F(Math.abs(p))}%</td><td><div style="background:${c};opacity:.85;height:14px;border-radius:7px;width:${w}%"></div></td></tr>`;}).join("")+
      `</tbody></table><p class="muted">Each bar is the real return — what the money gained (green) or lost (red) in buying power, after inflation of ${F((cpi-1)*100)}% over end-${y1} to end-${y2}.</p>`;
  }
}
function initCalc(){
  const from=document.getElementById("c-from"), to=document.getElementById("c-to");
  if(!from) return;
  CALC.years.forEach(y=>{from.add(new Option(y,y)); to.add(new Option(y,y));});
  from.value=CALC.years[0]; to.value=CALC.years.at(-1);
  if(!CALC.verified){ const w=document.getElementById("c-warn"); if(w) w.style.display="block"; }
  runCalc();
}
document.addEventListener("DOMContentLoaded",()=>{ initCalc(); });

/* ============================================================
   BEST-IN-CLASS LAYER — search, valuation gauge, "how to read",
   glossary tooltips, peer comparison
   ============================================================ */

/* ---------- ticker search (works on any page; default ids #tk-search + #tk-results) ---------- */
function initSearch(inputId="tk-search", resultsId="tk-results"){
  const input = document.getElementById(inputId);
  const box   = document.getElementById(resultsId);
  if(!input || !box) return;

  // Build the searchable index from data.js
  const live = Object.entries(TICKERS).map(([code,t])=>({
    code, name:t.name, url:code.toLowerCase()+".html", status:"Covered"
  }));
  const index = [...live];   // search lists covered stocks only — no coming-soon

  function render(q){
    q = q.trim().toLowerCase();
    if(!q){ box.innerHTML=""; box.classList.remove("open"); return; }
    const hits = index.filter(x =>
      x.code.toLowerCase().includes(q) || x.name.toLowerCase().includes(q));
    if(!hits.length){
      box.innerHTML = `<div class="tk-empty">No match. We cover EGX stocks, selected global names, and metals.</div>`;
      box.classList.add("open"); return;
    }
    box.innerHTML = hits.map(x => x.url
      ? `<a class="tk-hit" href="${x.url}"><span><b>${x.code}</b> · ${x.name}</span><span class="tk-tag">${x.status}</span></a>`
      : `<div class="tk-hit tk-hit-soon"><span><b>${x.code}</b> · ${x.name}</span><span class="tk-tag warn">${x.status}</span></div>`
    ).join("");
    box.classList.add("open");
  }
  input.addEventListener("input", e=>render(e.target.value));
  input.addEventListener("focus", e=>render(e.target.value));
  document.addEventListener("click", e=>{
    if(!input.contains(e.target) && !box.contains(e.target)) box.classList.remove("open");
  });
  // keyboard: Enter jumps to first hit
  input.addEventListener("keydown", e=>{
    if(e.key==="Enter"){ const first=box.querySelector("a.tk-hit"); if(first) location.href=first.getAttribute("href"); }
  });
}

/* ---------- valuation gauge ----------
   Shows where the latest price sits versus our fair value: a simple
   "looks cheap / about right / looks expensive" reading, no buy/sell call. */
function valuationVerdict(spot, base){
  const gap = (base - spot)/spot;            // how far below fair value we are
  if(gap >=  0.15) return {label:"Looks cheap vs our estimate",   tone:"cheap",   gap};
  if(gap <= -0.15) return {label:"Looks expensive vs our estimate", tone:"rich",  gap};
  return {label:"About fairly priced vs our estimate", tone:"fair", gap};
}
function renderGauge(elId, spot, fair, asof){
  const el=document.getElementById(elId); if(!el) return;
  const {bear,base,full}=fair;
  const lo=Math.min(bear,spot), hi=Math.max(full,spot);
  const pad=(hi-lo)*0.04, min=lo-pad, max=hi+pad;
  const mob = (typeof window!=="undefined" && window.innerWidth < 640);
  const fG = mob ? 28 : 18, fGsm = mob ? 24 : 15, fGdt = mob ? 20 : 13;
  const W=1000, H = mob ? 184 : 138, y = mob ? 62 : 46;
  const valY = mob ? y-34 : y-24, todY = mob ? y+44 : y+30, dateY = mob ? y+74 : y+50, endY = mob ? y+104 : y+74;
  const X=v=>30+(v-min)/(max-min)*(W-60);
  const v=valuationVerdict(spot,base);
  // half-width-aware clamp: keep each label fully inside the 0..W viewBox (IBM Plex Mono ≈ 0.62em advance)
  const labHalf = (s, fs) => s.length * fs * 0.31 + 8;
  const todHalf = labHalf("latest "+F(spot), fG);
  const todayX  = Math.max(todHalf, Math.min(W-todHalf, X(spot)));
  const valHalf = labHalf("our value "+F(base), fG);
  const baseX   = Math.max(valHalf, Math.min(W-valHalf, X(base)));
  el.innerHTML = `<svg viewBox="0 0 ${W} ${H}" xmlns="http://www.w3.org/2000/svg" role="img"
      aria-label="Latest price ${F(spot)} versus our fair value ${F(base)}.">
    <style>.g{font:600 ${fG}px 'IBM Plex Mono',monospace}.gsm{font:600 ${fGsm}px 'IBM Plex Mono',monospace}.gdt{font:500 ${fGdt}px 'IBM Plex Mono',monospace}.gmut{fill:#8A9A98}.gink{fill:var(--ink)}.gbase{fill:#12796B}</style>
    <defs><linearGradient id="vg" gradientUnits="userSpaceOnUse" x1="${X(min)}" y1="0" x2="${X(max)}" y2="0">
      <stop offset="0" stop-color="#2E7D5B"/><stop offset="0.25" stop-color="#6FA85C"/><stop offset="0.5" stop-color="#C0A45F"/><stop offset="0.75" stop-color="#D06A2C"/><stop offset="1" stop-color="#C0392B"/>
    </linearGradient></defs>
    <rect x="${X(min)}" y="${y-6}" width="${X(max)-X(min)}" height="12" rx="6" fill="url(#vg)"/>
    <!-- our value mark + label ABOVE -->
    <line x1="${X(base)}" x2="${X(base)}" y1="${y-16}" y2="${y+16}" stroke="#12796B" stroke-width="5"/>
    <text x="${baseX}" y="${valY}" text-anchor="middle" class="g gbase">our value ${F(base)}</text>
    <!-- today mark + label BELOW -->
    <circle cx="${X(spot)}" cy="${y}" r="10" fill="#fff" stroke="#0E2726" stroke-width="4"/>
    <text x="${todayX}" y="${todY}" text-anchor="middle" class="g gink">latest ${F(spot)}</text>
    ${asof?`<text x="${todayX}" y="${dateY}" text-anchor="middle" class="gdt gmut">${asof}</text>`:""}
    <!-- end labels on the lowest row -->
    <text x="30" y="${endY}" class="gsm gmut">← cheap</text>
    <text x="${W-30}" y="${endY}" text-anchor="end" class="gsm gmut">expensive →</text>
  </svg>
  <p class="gauge-verdict ${v.tone}">${v.label} <span class="muted">(${v.gap>=0?'+':''}${Math.round(v.gap*100)}% to our value)</span></p>`;
}

/* ---------- "How to read this" modal ---------- */
function initHowto(){
  const open = document.getElementById("howto-open");
  const modal= document.getElementById("howto-modal");
  if(!open || !modal) return;
  const close = ()=> modal.classList.remove("open");
  open.addEventListener("click", ()=> modal.classList.add("open"));
  modal.addEventListener("click", e=>{ if(e.target===modal || e.target.closest("[data-close]")) close(); });
  document.addEventListener("keydown", e=>{ if(e.key==="Escape") close(); });
}

/* ---------- peer comparison (covered stocks side by side) ---------- */
function renderPeers(elId, currentCode){
  const el=document.getElementById(elId); if(!el) return;
  const rows = Object.entries(TICKERS)
    .sort((a,b)=> a[1].name.localeCompare(b[1].name))
    .map(([code,t])=>{
    const o = plainOdds(t.dist.t60, t.spot);
    const v = valuationVerdict(t.spot, t.fair.base);
    const up = Math.round(o.pa*10);
    const here = code===currentCode;
    return `<tr${here?' class="peer-here"':''}>
      <td>${here?'<b>':''}<a href="${code.toLowerCase()}.html">${t.name}</a>${here?'</b>':''} <span class="muted num">${t.code}</span></td>
      <td class="num">${F(t.spot)}</td>
      <td class="num">${F(t.fair.base)}</td>
      <td><span class="pill ${v.tone}">${v.tone==='cheap'?'Looks cheap':v.tone==='rich'?'Looks expensive':'About right'}</span></td>
      <td class="num">${up} in 10 up</td>
    </tr>`;
  }).join("");
  el.innerHTML = `<table><thead><tr>
    <th>Stock</th><th class="num">Latest</th><th class="num">Our value</th><th>Price view</th><th class="num">3-month odds</th>
  </tr></thead><tbody>${rows}</tbody></table>`;
}

/* ---------- nav search overlay (every page) ---------- */
function initNavSearch(){
  const btn = document.getElementById("nav-search-btn");
  const overlay = document.getElementById("nav-search-overlay");
  if(!btn || !overlay) return;
  const input = overlay.querySelector("#tk-search");
  const box   = overlay.querySelector("#tk-results");

  // reuse the same index logic as initSearch
  const live = Object.entries(TICKERS).map(([code,t])=>({code, name:t.name, url:code.toLowerCase()+".html", status:"Covered"}));
  const index=[...live];   // covered stocks only — no coming-soon

  function render(q){
    q=q.trim().toLowerCase();
    if(!q){ box.innerHTML=""; return; }
    const hits=index.filter(x=>x.code.toLowerCase().includes(q)||x.name.toLowerCase().includes(q));
    box.classList.add("open");
    box.innerHTML = hits.length ? hits.map(x=>x.url
      ? `<a class="tk-hit" href="${x.url}"><span><b>${x.code}</b> · ${x.name}</span><span class="tk-tag">${x.status}</span></a>`
      : `<div class="tk-hit tk-hit-soon"><span><b>${x.code}</b> · ${x.name}</span><span class="tk-tag warn">${x.status}</span></div>`
    ).join("") : `<div class="tk-empty">No match. We cover Egyptian Exchange (EGX) stocks.</div>`;
  }
  function open(){ overlay.classList.add("open"); setTimeout(()=>input.focus(),50); }
  function close(){ overlay.classList.remove("open"); input.value=""; box.innerHTML=""; }

  btn.addEventListener("click", open);
  overlay.addEventListener("click", e=>{ if(e.target===overlay) close(); });
  input.addEventListener("input", e=>render(e.target.value));
  input.addEventListener("keydown", e=>{
    if(e.key==="Escape") close();
    if(e.key==="Enter"){ const first=box.querySelector("a.tk-hit"); if(first) location.href=first.getAttribute("href"); }
  });
  document.addEventListener("keydown", e=>{
    // "/" opens search from anywhere (unless typing in a field)
    if(e.key==="/" && !/input|textarea/i.test(document.activeElement.tagName)){ e.preventDefault(); open(); }
  });
}

/* ---------- first-visit "how to read this" (stock pages) ---------- */
function initFirstRunHowto(){
  const modal = document.getElementById("howto-modal");
  if(!modal) return;
  // auto-popup disabled — the "How to read this" button opens it on demand instead
  return;
}

/* boot the global bits */
document.addEventListener("DOMContentLoaded",()=>{ initSearch(); initFirstRunHowto(); initShare(); });

/* ---------- track-record badge (honest: shows scored hit-rate, or "awaiting" if none yet) ---------- */
function trackRecord(){
  const scored = LEDGER.filter(r=>ledgerStatus(r)==="graded");
  const inrange = scored.filter(r=> (r.in_90!=null) ? r.in_90 : (r.realized_close>=r.p5 && r.realized_close<=r.p95)).length;
  const open = LEDGER.filter(r=>ledgerStatus(r)==="open").length;
  // next grade date among open forecasts
  const nextDate = LEDGER.filter(r=>ledgerStatus(r)==="open").map(r=>r.grade_date).sort()[0] || null;
  return { total:LEDGER.length, scored:scored.length, inrange, open, nextDate };
}
function renderTrackBadge(elId){
  const el=document.getElementById(elId); if(!el) return;
  const t=trackRecord();
  let inner;
  if(t.scored>0){
    inner=`<a href="ledger.html" class="track-badge">
      <span class="tb-num">${t.inrange}/${t.scored}</span>
      <span class="tb-txt">past forecasts got it right so far → <u>see how we did</u></span></a>`;
  } else {
    inner=`<a href="ledger.html" class="track-badge">
      <span class="tb-num">${t.total}</span>
      <span class="tb-txt">past forecasts you can check later to see if we were right → <u>see them</u></span></a>`;
  }
  el.innerHTML=inner;
}

/* ---------- full compare table (compare.html) ---------- */
function renderCompare(elId, market){
  const el=document.getElementById(elId); if(!el) return;
  market = market || "all";
  const _isEgx = (t)=> (t.code||"").indexOf("EGX:")===0;
  const _entries = Object.entries(TICKERS).filter(function(e){ if(market==="intl") return !_isEgx(e[1]); if(market==="egx") return _isEgx(e[1]); return true; });
  const rows = _entries.map(([code,t])=>{
    const o60=plainOdds(t.dist.t60, t.spot);
    const v=valuationVerdict(t.spot, t.fair.base);
    const up60=Math.round(o60.pa*10);
    const fvGap = Math.round((t.fair.base-t.spot)/t.spot*100);
    const trend = (t.tech&&t.tech.trend) ? t.tech.trend : "—";
    return `<tr>
      <td><a href="${code.toLowerCase()}.html"><b>${t.name}</b></a><br><span class="muted num" style="font-size:.8rem">${t.code} &middot; ${t.ccy}</span></td>
      <td class="num">${F(t.spot)}</td>
      <td class="num">${F(t.fair.base)}<br><span class="muted" style="font-size:.8rem">${fvGap>=0?'+':''}${fvGap}%</span></td>
      <td><span class="pill ${v.tone}">${v.tone==='cheap'?'Looks cheap':v.tone==='rich'?'Looks expensive':'About right'}</span></td>
      <td class="num">${F(t.dist.t60.p50)}</td>
      <td class="num">${up60} in 10</td>
      <td style="font-size:.85rem">${trend}</td>
    </tr>`;
  }).join("");
  el.innerHTML = `<table class="compare-table"><thead><tr>
    <th>Stock</th><th class="num">Latest</th><th class="num">Our value</th><th>Price view</th>
    <th class="num">3-mo middle</th><th class="num">Odds up (3-mo)</th><th>Chart trend</th>
  </tr></thead><tbody>${rows}</tbody></table>`;
}

/* ---------- compare picker: populate a <select> + render two chosen rows ---------- */
function _compareRowHTML(code, t){
  const o60  = plainOdds(t.dist.t60, t.spot);
  const v    = valuationVerdict(t.spot, t.fair.base);
  const up60 = Math.round(o60.pa*10);
  const fvGap= Math.round((t.fair.base-t.spot)/t.spot*100);
  const trend= (t.tech&&t.tech.trend) ? t.tech.trend : "—";
  return `<tr>
      <td><a href="${code.toLowerCase()}.html"><b>${t.name}</b></a><br><span class="muted num" style="font-size:.8rem">${t.code} &middot; ${t.ccy}</span></td>
      <td class="num">${F(t.spot)}<br><span class="muted" style="font-size:.8rem">${(t.spotDate||"").replace(/^close\s+/i,"")}</span></td>
      <td class="num">${F(t.fair.base)}<br><span class="muted" style="font-size:.8rem">${fvGap>=0?'+':''}${fvGap}%</span></td>
      <td><span class="pill ${v.tone}">${v.tone==='cheap'?'Looks cheap':v.tone==='rich'?'Looks expensive':'About right'}</span></td>
      <td class="num">${F(t.dist.t60.p50)}</td>
      <td class="num">${up60} in 10</td>
      <td style="font-size:.85rem">${trend}</td>
    </tr>`;
}
/* fill a <select> with every covered ticker, grouped Egypt / International, marking `selected` */
function fillCompareSelect(sel, selected){
  if(!sel) return;
  const _isEgx = (t)=> (t.code||"").indexOf("EGX:")===0;
  const ents = Object.entries(TICKERS);
  const egx  = ents.filter(e=> _isEgx(e[1]));
  const intl = ents.filter(e=> !_isEgx(e[1]));
  const opt  = ([code,t])=> `<option value="${code}"${code===selected?" selected":""}>${t.name} (${t.code})</option>`;
  let html="";
  if(egx.length)  html += `<optgroup label="Egypt (EGX)">${egx.map(opt).join("")}</optgroup>`;
  if(intl.length) html += `<optgroup label="International">${intl.map(opt).join("")}</optgroup>`;
  sel.innerHTML = html;
}
/* searchable combobox: type to filter OR click to open the full grouped list */
function makeCompareCombo(mount, opts){
  opts = opts || {};
  const onChange = opts.onChange || function(){};
  const _isEgx = (t)=> (t.code||"").indexOf("EGX:")===0;
  const ents = Object.entries(TICKERS);
  const groups = [
    ["Egypt (EGX)",  ents.filter(e=> _isEgx(e[1]))],
    ["International", ents.filter(e=> !_isEgx(e[1]))]
  ].filter(g=> g[1].length);

  let selected = TICKERS[opts.selected] ? opts.selected : (ents[0]||[])[0];
  let open=false, activeCode=null, flat=[];

  mount.classList.add("cmp-combo");
  mount.innerHTML =
    '<input class="cmp-combo-input" type="text" role="combobox" aria-expanded="false" aria-autocomplete="list" autocomplete="off" placeholder="Search or pick a stock\u2026">' +
    '<span class="cmp-combo-caret" aria-hidden="true">\u25BE</span>' +
    '<div class="cmp-combo-panel" role="listbox" hidden></div>';
  const input = mount.querySelector(".cmp-combo-input");
  const panel = mount.querySelector(".cmp-combo-panel");
  if(opts.label) input.setAttribute("aria-label", opts.label);

  const labelFor = code => { const t=TICKERS[code]; return t ? t.name : ""; };

  function matches(q){
    q=(q||"").trim().toLowerCase();
    if(!q) return groups.map(g=>[g[0], g[1].slice()]);
    const f = ([code,t])=> t.name.toLowerCase().indexOf(q)>=0 || (t.code||"").toLowerCase().indexOf(q)>=0 || code.toLowerCase().indexOf(q)>=0;
    return groups.map(g=>[g[0], g[1].filter(f)]).filter(g=>g[1].length);
  }
  function renderPanel(){
    const showAll = input.value===labelFor(selected);
    const gs = matches(showAll ? "" : input.value);
    flat=[]; let html="";
    if(!gs.length) html='<div class="cmp-combo-empty">No match</div>';
    gs.forEach(([gname,list])=>{
      html+='<div class="cmp-combo-group">'+gname+'</div>';
      list.forEach(([code,t])=>{ flat.push(code);
        html+='<div class="cmp-combo-opt'+(code===selected?' sel':'')+(code===activeCode?' active':'')+'" role="option" data-code="'+code+'" aria-selected="'+(code===selected)+'">'+
                '<span class="cmp-combo-name">'+t.name+'</span><span class="muted num cmp-combo-code">'+t.code+'</span></div>';
      });
    });
    panel.innerHTML=html;
    if(flat.indexOf(activeCode)<0) activeCode = flat[0]||null;
  }
  function scrollActive(){ const a=panel.querySelector(".cmp-combo-opt.active"); if(a&&a.scrollIntoView) a.scrollIntoView({block:"nearest"}); }
  function openPanel(){ open=true; panel.hidden=false; input.setAttribute("aria-expanded","true"); activeCode=selected; renderPanel(); scrollActive(); }
  function closePanel(restore){ open=false; panel.hidden=true; input.setAttribute("aria-expanded","false"); if(restore!==false) input.value=labelFor(selected); }
  function choose(code){ if(!TICKERS[code]) return; selected=code; input.value=labelFor(code); closePanel(false); onChange(code); }
  function move(dir){ if(!flat.length) return; let i=flat.indexOf(activeCode); i = i<0?0:i+dir; i=Math.max(0,Math.min(flat.length-1,i)); activeCode=flat[i]; renderPanel(); scrollActive(); }

  input.value = labelFor(selected);
  input.addEventListener("focus", ()=>{ input.select(); openPanel(); });
  input.addEventListener("click", ()=>{ if(!open) openPanel(); });
  input.addEventListener("input", ()=>{ open=true; panel.hidden=false; input.setAttribute("aria-expanded","true"); activeCode=null; renderPanel(); scrollActive(); });
  input.addEventListener("keydown", e=>{
    if(e.key==="ArrowDown"){ e.preventDefault(); if(!open){openPanel();} else move(1); }
    else if(e.key==="ArrowUp"){ e.preventDefault(); if(open) move(-1); }
    else if(e.key==="Enter"){ if(open && activeCode){ e.preventDefault(); choose(activeCode); } }
    else if(e.key==="Escape"){ if(open){ e.preventDefault(); closePanel(true); input.blur&&input.blur(); } }
  });
  panel.addEventListener("mousedown", e=>{ const o=e.target.closest&&e.target.closest(".cmp-combo-opt"); if(o){ e.preventDefault(); choose(o.getAttribute("data-code")); } });
  document.addEventListener("click", e=>{ if(!mount.contains(e.target)) closePanel(true); });

  renderPanel();
  return { get value(){ return selected; }, set(code){ if(TICKERS[code]){ selected=code; input.value=labelFor(code); } } };
}

/* render exactly two chosen tickers as two rows, one above the other */
function renderComparePair(elId, codeA, codeB){
  const el=document.getElementById(elId); if(!el) return;
  const a=TICKERS[codeA], b=TICKERS[codeB];
  const rows=[];
  if(a) rows.push(_compareRowHTML(codeA, a));
  if(b) rows.push(_compareRowHTML(codeB, b));
  const same = codeA===codeB ? `<p class="muted" style="margin:10px 0 0">Both rows show the same stock — pick a different one in either box to compare.</p>` : "";
  el.innerHTML = `<table class="compare-table"><thead><tr>
    <th>Stock</th><th class="num">Latest</th><th class="num">Our value</th><th>Price view</th>
    <th class="num">3-mo middle</th><th class="num">Odds up (3-mo)</th><th>Chart trend</th>
  </tr></thead><tbody>${rows.join("")}</tbody></table>${same}`;
}

/* ---------- searchable combobox for the compare picker (type to search OR open full list) ---------- */
function initCompareCombo(opts){
  const input  = document.getElementById(opts.input);
  const list   = document.getElementById(opts.list);
  const toggle = opts.toggle ? document.getElementById(opts.toggle) : null;
  if(!input || !list) return null;
  const _isEgx = t => (t.code||"").indexOf("EGX:")===0;
  const index = Object.entries(TICKERS).map(([code,t])=>({
    code, name:t.name, label:`${t.name} (${t.code})`, tag:t.code, group:_isEgx(t)?"Egypt (EGX)":"International"
  }));
  let current = TICKERS[opts.initial] ? opts.initial : index[0].code;
  let active  = -1;     // keyboard-highlighted row
  let hits    = [];
  const labelFor = code => { const x=index.find(i=>i.code===code); return x?x.label:""; };
  const isOpen   = () => list.classList.contains("open");

  function close(){ list.classList.remove("open"); input.setAttribute("aria-expanded","false"); active=-1; }
  function commit(code){
    if(!TICKERS[code]) return;
    current = code; input.value = labelFor(code); input.dataset.code = code;
    close(); if(opts.onChange) opts.onChange(code);
  }
  function rowsHTML(){
    if(!hits.length) return `<div class="tk-empty">No match — try a code like PHDC or a name.</div>`;
    let html="", lastGroup=null;
    hits.forEach((h,i)=>{
      if(h.group!==lastGroup){ html+=`<div class="combo-group">${h.group}</div>`; lastGroup=h.group; }
      const sel=h.code===current?" is-current":"", act=i===active?" is-active":"";
      html+=`<div class="tk-hit combo-item${sel}${act}" role="option" data-code="${h.code}" aria-selected="${h.code===current}"><span>${h.name}</span><span class="tk-tag">${h.tag}</span></div>`;
    });
    return html;
  }
  function open(q){
    const s=(q==null?"":q).trim().toLowerCase();
    hits = s ? index.filter(i=> i.code.toLowerCase().includes(s) || i.name.toLowerCase().includes(s)) : index.slice();
    active=-1; list.innerHTML=rowsHTML(); list.classList.add("open"); input.setAttribute("aria-expanded","true");
  }
  function move(d){
    if(!isOpen()) open("");
    if(!hits.length) return;
    active=(active+d+hits.length)%hits.length; list.innerHTML=rowsHTML();
    const el=list.querySelector(".combo-item.is-active"); if(el) el.scrollIntoView({block:"nearest"});
  }

  input.addEventListener("focus", ()=>{ input.select(); open(""); });
  input.addEventListener("input", ()=> open(input.value));
  input.addEventListener("keydown", e=>{
    if(e.key==="ArrowDown"){ e.preventDefault(); move(1); }
    else if(e.key==="ArrowUp"){ e.preventDefault(); move(-1); }
    else if(e.key==="Enter"){ if(isOpen() && active>=0){ e.preventDefault(); commit(hits[active].code); } }
    else if(e.key==="Escape"){ close(); input.value=labelFor(current); input.blur(); }
  });
  list.addEventListener("mousedown", e=>{ const it=e.target.closest(".combo-item"); if(!it) return; e.preventDefault(); commit(it.dataset.code); });
  if(toggle) toggle.addEventListener("mousedown", e=>{ e.preventDefault(); if(isOpen()){ close(); } else { input.focus(); open(""); } });
  input.addEventListener("blur", ()=> setTimeout(()=>{ if(!isOpen()){ input.value=labelFor(current); } close(); }, 120));
  document.addEventListener("click", e=>{ if(!list.parentNode.contains(e.target)) close(); });

  input.value=labelFor(current); input.dataset.code=current;
  return { get value(){ return input.dataset.code; }, set(code){ commit(code); } };
}

/* ---------- share button (native share on mobile, copy link on desktop) ---------- */
function initShare(){
  document.querySelectorAll("[data-share]").forEach(btn=>{
    btn.addEventListener("click", async ()=>{
      const url = location.href;
      const title = document.title;
      const text = btn.getAttribute("data-share") || title;
      if(navigator.share){
        try{ await navigator.share({title, text, url}); }catch(e){}
      } else {
        try{
          await navigator.clipboard.writeText(url);
          const old=btn.textContent; btn.textContent="Link copied ✓";
          setTimeout(()=>btn.textContent=old, 1800);
        }catch(e){
          prompt("Copy this link:", url);
        }
      }
    });
  });
}
/* ============================================================
   RELATED STUDIES — cross-links every study page to its siblings
   Reads TICKERS (+ METALS for Gold). No per-page editing: each
   study page carries <div id="related" data-ticker="PHDC"></div>
   and this renders 4 sibling cards, same-sector first.
   ============================================================ */
(function(){
  // sector map (data.js has no sector field; fixed lookup, extend as coverage grows)
  var SECTOR = {
    PHDC:"egx-realestate", TMGH:"egx-realestate", EMFD:"egx-realestate",
    OCDI:"egx-realestate", ORHD:"egx-realestate", EMAAR:"egx-realestate",
    ORAS:"egx-industrial", CCAP:"egx-holding", COMI:"egx-bank",
    SAMSUNG:"intl-tech", KAKAO:"intl-tech", LGES:"intl-industrial",
    TMPV:"intl-industrial", ARAMCO:"intl-energy", TSLA:"intl-industrial",
    GOLD:"metal"
  };
  // page url + display fields, pulling from TICKERS then METALS
  function rec(key){
    var t = (typeof TICKERS!=="undefined") && TICKERS[key];
    if(t) return { name:t.name, code:t.code, url:key.toLowerCase()+".html" };
    var m = (typeof METALS!=="undefined") && METALS[key];
    if(m) return { name:m.name||key, code:m.code||"", url:key.toLowerCase()+".html" };
    return null;
  }
  function build(el){
    var me = (el.getAttribute("data-ticker")||"").toUpperCase();
    if(!me) return;
    var mySector = SECTOR[me];
    // universe = every key we can resolve to a page, minus self
    var universe = Object.keys(SECTOR).filter(function(k){ return k!==me && rec(k); });
    // same sector first (keep data.js order within each bucket), then the rest
    var same = universe.filter(function(k){ return SECTOR[k]===mySector; });
    var rest = universe.filter(function(k){ return SECTOR[k]!==mySector; });
    var pick = same.concat(rest).slice(0,4);
    if(!pick.length) return;
    var cards = pick.map(function(k){
      var r = rec(k);
      return '<a class="rel-card" href="'+r.url+'">'
           +   '<span class="rel-code num">'+ (r.code||k) +'</span>'
           +   '<span class="rel-name">'+ r.name +'</span>'
           +   '<span class="rel-go" aria-hidden="true">Read the study →</span>'
           + '</a>';
    }).join("");
    el.innerHTML =
      '<div class="rel-head">'
      +  '<h2 class="rel-title">Keep reading</h2>'
      +  '<a class="rel-all" href="stocks.html">All studies →</a>'
      + '</div>'
      + '<div class="rel-grid">'+ cards +'</div>';
    el.setAttribute("data-built","1");
  }
  function run(){
    var nodes = document.querySelectorAll('#related[data-ticker]');
    for(var i=0;i<nodes.length;i++){ if(!nodes[i].getAttribute("data-built")) build(nodes[i]); }
  }
  if(document.readyState==="loading") document.addEventListener("DOMContentLoaded",run);
  else run();
})();

/* rds panels: open on anchor nav + resize charts on open */
(function(){
  function openTo(hash){ if(!hash) return; var el=document.getElementById(hash.replace('#','')); while(el){ if(el.tagName==='DETAILS' && !el.open){ el.open=true; } el=el.parentElement; } setTimeout(function(){ window.dispatchEvent(new Event('resize')); },30); }
  document.addEventListener('click',function(e){ var a=e.target.closest&&e.target.closest('a[href^="#"]'); if(a) openTo(a.getAttribute('href')); });
  window.addEventListener('hashchange',function(){ openTo(location.hash); });
  document.addEventListener('DOMContentLoaded',function(){ document.querySelectorAll('details.rds').forEach(function(d){ d.addEventListener('toggle',function(){ if(d.open){ setTimeout(function(){ window.dispatchEvent(new Event('resize')); },30); } }); }); if(location.hash){ setTimeout(function(){ openTo(location.hash); },60); } });
})();

/* ============ static MC fan (Fundamental/Technical/MC redesign) ============ */
function fitPowerLaw(spot, t20, t60){
  const out = {};
  ["p5","p25","p50","p75","p95"].forEach(function(q){
    const y20 = Math.log(t20[q]/spot), y60 = Math.log(t60[q]/spot);
    const b = Math.log(Math.abs(y60)/Math.abs(y20)) / Math.log(3);
    const a = y20 / Math.pow(20, b);
    out[q] = [a, b];
  });
  return out;
}
function fanVal(fit, spot, q, t){
  if (t === 0) return spot;
  const a = fit[q][0], b = fit[q][1];
  return spot * Math.exp(a * Math.pow(t, b));
}
function renderStaticFan(elId, T){
  const el = document.getElementById(elId); if (!el) return;
  const spot = T.spot, t20 = T.dist.t20, t60 = T.dist.t60;
  const fit = fitPowerLaw(spot, t20, t60);
  const W = 760, H = 300, ML = 46, MR = 54, MT = 16, MB = 30;
  const X0 = ML, X1 = W - MR, Y0 = H - MB, Y1 = MT, AX = 60;
  const allT = []; for (let t = 0; t <= 60; t += 2) allT.push(t);
  let lo = Infinity, hi = -Infinity;
  allT.forEach(function(t){
    ["p5","p95"].forEach(function(q){
      const v = fanVal(fit, spot, q, t);
      if (v < lo) lo = v; if (v > hi) hi = v;
    });
  });
  const pad = (hi - lo) * 0.08; const PMIN = lo - pad, PMAX = hi + pad;
  const xpx = t => X0 + (t / AX) * (X1 - X0);
  const ypx = p => Y0 + (p - PMIN) / (PMAX - PMIN) * (Y1 - Y0);
  function bandPath(qHi, qLo){
    let d = "";
    allT.forEach(function(t, i){ const v = fanVal(fit, spot, qHi, t); d += (i ? "L" : "M") + xpx(t).toFixed(1) + "," + ypx(v).toFixed(1) + " "; });
    for (let i = allT.length - 1; i >= 0; i--){ const t = allT[i]; const v = fanVal(fit, spot, qLo, t); d += "L" + xpx(t).toFixed(1) + "," + ypx(v).toFixed(1) + " "; }
    return d + "Z";
  }
  function linePath(q){
    let d = "";
    allT.forEach(function(t, i){ const v = fanVal(fit, spot, q, t); d += (i ? "L" : "M") + xpx(t).toFixed(1) + "," + ypx(v).toFixed(1) + " "; });
    return d;
  }
  // magnitude-aware step: always ~7 gridlines, never a runaway loop on high-priced names
  const _rng = PMAX - PMIN;
  const _raw = _rng / 7;
  const _mag = Math.pow(10, Math.floor(Math.log(_raw) / Math.LN10));
  const _n = _raw / _mag;
  const niceStep = (_n >= 5 ? 5 : _n >= 2 ? 2 : 1) * _mag;
  const _gdec = niceStep < 1 ? (niceStep < 0.5 ? 2 : 1) : 0;
  let grid = ""; for (let g = Math.ceil(PMIN / niceStep) * niceStep; g <= PMAX; g += niceStep){
    const y = ypx(g);
    grid += '<line x1="' + X0 + '" x2="' + X1 + '" y1="' + y.toFixed(1) + '" y2="' + y.toFixed(1) + '" stroke="var(--line,#dce4e2)" stroke-width="1" opacity=".5"/>';
    grid += '<text x="' + (X0 - 8) + '" y="' + (y + 3).toFixed(1) + '" text-anchor="end" font-size="10" fill="var(--muted,#6b7c78)" font-family="IBM Plex Mono,monospace">' + g.toFixed(_gdec) + '</text>';
  }
  let xt = ""; [0,10,20,30,40,50,60].forEach(function(t){
    xt += '<text x="' + xpx(t).toFixed(1) + '" y="' + (Y0 + 18) + '" text-anchor="middle" font-size="10" fill="var(--muted,#6b7c78)" font-family="IBM Plex Mono,monospace">' + (t === 0 ? "latest" : "T+" + t) + '</text>';
  });
  const cols = {p95:"var(--teal2,#2A8F8F)",p75:"var(--teal,#12796B)",p50:"var(--gold,#C0A45F)",p25:"var(--teal,#12796B)",p5:"var(--teal2,#2A8F8F)"};
  let rows = ["p5","p25","p50","p75","p95"].map(function(q){ return [fanVal(fit, spot, q, 60), q]; });
  rows.sort(function(a,b){ return b[0]-a[0]; });
  let endLabels = "", prevY = null;
  rows.forEach(function(r){
    let y = ypx(r[0]);
    if (prevY !== null && y - prevY < 12) y = prevY + 12;
    prevY = y;
    endLabels += '<circle cx="' + X1.toFixed(1) + '" cy="' + y.toFixed(1) + '" r="' + (r[1]==="p50"?3.5:2.5) + '" fill="' + cols[r[1]] + '"/>';
    endLabels += '<text x="' + (X1+8).toFixed(1) + '" y="' + (y+3.5).toFixed(1) + '" font-size="10.5" font-family="IBM Plex Mono,monospace" fill="' + cols[r[1]] + '">' + F(r[0]) + '</text>';
  });
  const touchRows = (T.touch||[]).map(function(r){
    return '<tr><td class="num">' + r[0].toFixed(2) + '</td><td class="num">' + r[1] + '%</td><td class="num">' + r[2] + '%</td></tr>';
  }).join("");
  el.innerHTML =
    '<svg id="' + elId + '-svg" viewBox="0 0 ' + W + ' ' + (Y0+40) + '" width="100%" role="img" aria-label="90% and 50% probability bands from latest to T+60" style="touch-action:none">' +
      grid +
      '<path d="' + bandPath("p95","p5") + '" fill="var(--teal,#12796B)" opacity=".16"/>' +
      '<path d="' + bandPath("p75","p25") + '" fill="var(--teal,#12796B)" opacity=".34"/>' +
      '<path d="' + linePath("p50") + '" fill="none" stroke="var(--gold,#C0A45F)" stroke-width="1.8"/>' +
      xt + endLabels +
      '<g id="' + elId + '-hover" style="display:none;pointer-events:none">' +
        '<line id="' + elId + '-hline" y1="' + Y1 + '" y2="' + Y0 + '" stroke="var(--muted,#6b7c78)" stroke-width="1" stroke-dasharray="3 3" opacity=".8"/>' +
        '<circle id="' + elId + '-hdot-p95" r="2.6" fill="var(--teal2,#2A8F8F)"/>' +
        '<circle id="' + elId + '-hdot-p75" r="2.6" fill="var(--teal,#12796B)"/>' +
        '<circle id="' + elId + '-hdot-p50" r="3.2" fill="var(--gold,#C0A45F)"/>' +
        '<circle id="' + elId + '-hdot-p25" r="2.6" fill="var(--teal,#12796B)"/>' +
        '<circle id="' + elId + '-hdot-p5" r="2.6" fill="var(--teal2,#2A8F8F)"/>' +
      '</g>' +
      '<rect id="' + elId + '-hit" x="' + X0 + '" y="' + Y1 + '" width="' + (X1-X0) + '" height="' + (Y0-Y1) + '" fill="transparent" style="cursor:crosshair"/>' +
    '</svg>' +
    '<div id="' + elId + '-tip" style="display:none;font-family:\'IBM Plex Mono\',monospace;font-size:12px;background:var(--card,#15302D);border:1px solid var(--line,#2a4b46);border-radius:8px;padding:8px 10px;margin-top:8px;line-height:1.7"></div>' +
    '<div style="display:flex;gap:18px;flex-wrap:wrap;font-size:var(--fs-small);color:var(--muted);margin:10px 0 4px">' +
      '<span><span style="display:inline-block;width:14px;height:10px;border-radius:2px;background:var(--teal,#12796B);opacity:.34;margin-right:5px"></span>50% band (25th\u201375th)</span>' +
      '<span><span style="display:inline-block;width:14px;height:10px;border-radius:2px;background:var(--teal,#12796B);opacity:.16;margin-right:5px"></span>90% band (5th\u201395th)</span>' +
      '<span><span style="display:inline-block;width:14px;height:2px;background:var(--gold,#C0A45F);margin-right:5px;vertical-align:middle"></span>median path</span>' +
    '</div>' +
    '<table class="mc-ladder" style="margin-top:14px"><thead><tr><th>Level</th><th>P(touch) T+20</th><th>P(touch) T+60</th></tr></thead><tbody>' + touchRows + '</tbody></table>' +
    '<p class="muted" style="font-size:var(--fs-small);margin-top:12px">t20 and t60 are the published calibration exactly as saved. The curve between them is a smooth fit using the real Student-t shape for this market through those two points \u2014 not a fresh simulation at every day, and not adjustable \u2014 so it always agrees with the published numbers at the two horizons that matter.</p>';

  // ---- hover read-out: move over the cone to read the bands at that horizon ----
  var svgEl = document.getElementById(elId + '-svg');
  var hit = document.getElementById(elId + '-hit');
  var hov = document.getElementById(elId + '-hover');
  var tip = document.getElementById(elId + '-tip');
  var hline = document.getElementById(elId + '-hline');
  if (svgEl && hit && hov && tip){
    var moveTo = function(clientX){
      var r = svgEl.getBoundingClientRect();
      var sx = W / r.width;                       // viewBox units per screen px
      var vx = (clientX - r.left) * sx;           // x in viewBox coords
      vx = Math.max(X0, Math.min(X1, vx));
      var t = (vx - X0) / (X1 - X0) * AX;          // horizon in days
      t = Math.max(0, Math.min(AX, Math.round(t)));
      var px = xpx(t);
      hov.style.display = '';
      hline.setAttribute('x1', px.toFixed(1)); hline.setAttribute('x2', px.toFixed(1));
      ['p95','p75','p50','p25','p5'].forEach(function(q){
        var v = fanVal(fit, spot, q, t);
        var dot = document.getElementById(elId + '-hdot-' + q);
        dot.setAttribute('cx', px.toFixed(1)); dot.setAttribute('cy', ypx(v).toFixed(1));
      });
      var vp5 = fanVal(fit, spot, 'p5', t), vp25 = fanVal(fit, spot, 'p25', t),
          vp50 = fanVal(fit, spot, 'p50', t), vp75 = fanVal(fit, spot, 'p75', t),
          vp95 = fanVal(fit, spot, 'p95', t);
      var when = (t === 0) ? 'now' : 'in ' + t + ' trading day' + (t===1?'':'s');
      var pctMove = ((vp50 / spot - 1) * 100);
      var sign = pctMove >= 0 ? '+' : '';
      tip.style.display = '';
      tip.innerHTML =
        '<b>T+' + t + '</b> \u00b7 ' + when +
        '<br><span style="color:var(--gold,#C0A45F)">median ' + F(vp50) + '</span> (' + sign + pctMove.toFixed(1) + '% vs spot)' +
        '<br><span style="color:var(--muted)">50% band</span> ' + F(vp25) + ' \u2013 ' + F(vp75) +
        '<br><span style="color:var(--muted)">90% band</span> ' + F(vp5) + ' \u2013 ' + F(vp95);
    };
    var hide = function(){ hov.style.display = 'none'; tip.style.display = 'none'; };
    hit.addEventListener('mousemove', function(e){ moveTo(e.clientX); });
    hit.addEventListener('mouseleave', hide);
    hit.addEventListener('touchstart', function(e){ if(e.touches[0]) moveTo(e.touches[0].clientX); }, {passive:true});
    hit.addEventListener('touchmove', function(e){ if(e.touches[0]) moveTo(e.touches[0].clientX); }, {passive:true});
  }
}

/* ============ fair-value sensitivity (Lens 2) ============ */
function renderFairLevers(elId, T, levers){
  const el = document.getElementById(elId); if (!el || !levers || !levers.length) return;
  const bear = T.fair.bear, base = T.fair.base, full = T.fair.full, spot = T.spot;
  const range = full - bear;
  const pct = v => Math.max(0, Math.min(100, (v - bear) / range * 100));
  const leverHtml = levers.map(function(lv, i){
    return '<div class="fl-lever" style="margin-bottom:14px">' +
      '<div style="display:flex;justify-content:space-between;font-size:var(--fs-small);margin-bottom:5px">' +
        '<span>' + lv.name + '</span><span class="num" id="fl-val-' + i + '" style="color:var(--gold)"></span></div>' +
      '<input type="range" id="fl-' + i + '" min="' + lv.min + '" max="' + lv.max + '" step="' + lv.step + '" value="' + lv.def + '" style="width:100%">' +
      '<div style="display:flex;justify-content:space-between;font-size:10.5px;color:var(--muted)"><span>' + lv.lo + '</span><span>' + lv.hi + '</span></div>' +
    '</div>';
  }).join("");
  el.innerHTML =
    '<div class="card">' +
    '<p class="qhead">What could move it \u2014 sensitivity</p>' +
    '<p class="muted">A simple weighted what-if off the published fair value. Not a re-run DCF, and it never touches the Monte Carlo section below.</p>' +
    '<div style="position:relative;margin:30px 6px 6px">' +
      '<div style="position:relative;height:6px;border-radius:3px;background:linear-gradient(90deg,#B5483A,#4A4A3A,#178A76)">' +
        '<div style="position:absolute;left:0%;top:-20px;transform:translateX(-50%);text-align:center;font-family:\'IBM Plex Mono\',monospace;font-size:11px;color:var(--muted)">' + F(bear) + '<span style="display:block;font-size:9.5px">bear</span></div>' +
        '<div style="position:absolute;left:100%;top:-20px;transform:translateX(-50%);text-align:center;font-family:\'IBM Plex Mono\',monospace;font-size:11px;color:var(--muted)">' + F(full) + '<span style="display:block;font-size:9.5px">full</span></div>' +
        '<div style="position:absolute;left:' + pct(spot).toFixed(1) + '%;top:14px;transform:translateX(-50%);text-align:center;font-family:\'IBM Plex Mono\',monospace;font-size:10.5px;color:var(--muted)">\u25B2<span style="display:block;font-size:9.5px">spot ' + F(spot) + '</span></div>' +
        '<div id="fl-marker" style="position:absolute;left:' + pct(base).toFixed(1) + '%;top:50%;width:13px;height:13px;transform:translate(-50%,-50%) rotate(45deg);background:var(--gold);border:2px solid var(--bg,#0d1f1d)"></div>' +
      '</div>' +
    '</div>' +
    '<p style="font-family:\'IBM Plex Mono\',monospace;font-size:14px;margin:26px 0 18px">Fair value: <b id="fl-fair" style="color:var(--gold);font-size:17px"></b> <span class="muted" id="fl-delta"></span></p>' +
    leverHtml +
    '<button type="button" id="fl-reset" class="btn-ghost" style="font-size:12px;padding:6px 12px">Reset to base case</button>' +
    '</div>';
  function render(){
    let effect = 0;
    levers.forEach(function(lv, i){
      const v = parseFloat(document.getElementById("fl-" + i).value);
      effect += lv.impact * (v - lv.def) / 100;
      document.getElementById("fl-val-" + i).textContent = lv.fmt(v);
    });
    const fair = base * Math.exp(effect);
    document.getElementById("fl-marker").style.left = pct(fair) + "%";
    document.getElementById("fl-fair").textContent = (T.ccy || "") + " " + F(fair);
    const d = (fair / spot - 1) * 100;
    document.getElementById("fl-delta").textContent = "(" + (d >= 0 ? "+" : "\u2212") + Math.abs(d).toFixed(1) + "% vs spot)";
  }
  levers.forEach(function(lv, i){ document.getElementById("fl-" + i).addEventListener("input", render); });
  document.getElementById("fl-reset").addEventListener("click", function(){
    levers.forEach(function(lv, i){ document.getElementById("fl-" + i).value = lv.def; });
    render();
  });
  render();
}

/* ============ technical reference lines (Lens 3) ============ */
function injectLevels(svgId, res, sup){
  const svg = document.getElementById(svgId); if (!svg) return;
  const labels = Array.prototype.slice.call(svg.querySelectorAll('text')).filter(function(t){
    return /var\(--muted/.test(t.getAttribute("fill") || "") && /^-?[\d,]+(\.\d+)?$/.test((t.textContent||"").trim());
  });
  if (labels.length < 2) return;
  const pts = labels.map(function(t){ return [parseFloat(t.getAttribute("y")), parseFloat((t.textContent||"").replace(/,/g,""))]; });
  const n = pts.length, sy = pts.reduce((s,p)=>s+p[0],0)/n, sp = pts.reduce((s,p)=>s+p[1],0)/n;
  let num=0, den=0; pts.forEach(function(p){ num += (p[0]-sy)*(p[1]-sp); den += (p[0]-sy)*(p[0]-sy); });
  const slope = num/den, intercept = sp - slope*sy;
  const priceToY = price => (price - intercept) / slope;
  // derive the plot's actual x-span from its own gridlines, so this always matches
  // whatever margin the chart was baked with (no hardcoded geometry).
  const gridLines = Array.prototype.slice.call(svg.querySelectorAll('line')).filter(function(ln){
    return /var\(--line/.test(ln.getAttribute("stroke") || "");
  });
  const x0 = gridLines.length ? parseFloat(gridLines[0].getAttribute("x1")) : 46;
  const x1 = gridLines.length ? parseFloat(gridLines[0].getAttribute("x2")) : 700;
  const ns = "http://www.w3.org/2000/svg";
  // draw all the dashed lines first, and collect label positions for a collision pass
  const labelRows = [];
  function addLine(price, color, label){
    const y = priceToY(price);
    const line = document.createElementNS(ns, "line");
    line.setAttribute("x1", x0); line.setAttribute("x2", x1);
    line.setAttribute("y1", y.toFixed(1)); line.setAttribute("y2", y.toFixed(1));
    line.setAttribute("stroke", color); line.setAttribute("stroke-width", "1");
    line.setAttribute("stroke-dasharray", "4 3"); line.setAttribute("opacity", ".7");
    svg.appendChild(line);
    labelRows.push({ y: y, color: color, label: label });
  }
  (res||[]).forEach(function(p){ addLine(p, "var(--amber-text,#854F0B)", F(p)); });
  (sup||[]).forEach(function(p){ addLine(p, "var(--red,#B5483A)", F(p)); });
  // collision pass: sort by y and push labels at least 12px apart so none overlap
  labelRows.sort(function(a,b){ return a.y - b.y; });
  const minGap = 12;
  for (let i=1; i<labelRows.length; i++){
    if (labelRows[i].y - labelRows[i-1].y < minGap) labelRows[i].y = labelRows[i-1].y + minGap;
  }
  // keep inside the plot bottom (294); if pushed past, pull the stack up from the bottom
  for (let i=labelRows.length-1; i>=0; i--){
    if (labelRows[i].y > 291) labelRows[i].y = (i===labelRows.length-1 ? 291 : labelRows[i+1].y - minGap);
  }
  // labels sit OUTSIDE the plot, in the right margin -- same placement as the zoom
  // chart's reference labels -- so they never sit on top of the price/MA lines.
  labelRows.forEach(function(r){
    const text = document.createElementNS(ns, "text");
    text.setAttribute("x", (x1 + 6).toFixed(1)); text.setAttribute("y", (r.y + 3.2).toFixed(1));
    text.setAttribute("font-size", "9.5");
    text.setAttribute("font-family", "IBM Plex Mono,monospace"); text.setAttribute("fill", r.color);
    text.textContent = r.label;
    svg.appendChild(text);
  });
}
function renderLevelList(elId, res, sup){
  const el = document.getElementById(elId); if (!el) return;
  const col = (arr, label) => '<div><p class="qhead" style="font-size:11px;text-transform:uppercase;letter-spacing:.4px;color:var(--muted)">' + label + '</p>' +
    arr.map(function(p,i){ return '<div style="display:flex;justify-content:space-between;font-family:\'IBM Plex Mono\',monospace;font-size:13px;padding:4px 0;border-bottom:1px solid var(--line)"><span>' + label[0] + (i+1) + '</span><span>' + F(p) + '</span></div>'; }).join("") + '</div>';
  el.innerHTML = '<div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:16px">' + col(res,"Resistance") + col(sup,"Support") + '</div>';
}

/* ============ technical zoom panel (recent window magnified) ============ */
function renderZoomChart(sourceSvgId, targetElId, res, sup, defaultSessions){
  const src = document.getElementById(sourceSvgId); if (!src) return;
  const host = document.getElementById(targetElId); if (!host) return;

  const labels = Array.prototype.slice.call(src.querySelectorAll("text")).filter(function(t){
    return /var\(--muted/.test(t.getAttribute("fill") || "") && /^-?[\d,]+(\.\d+)?$/.test((t.textContent||"").trim());
  });
  if (labels.length < 2) return;
  const cal = labels.map(function(t){ return [parseFloat(t.getAttribute("y")), parseFloat((t.textContent||"").replace(/,/g,""))]; });
  const n0 = cal.length, sy = cal.reduce((s,p)=>s+p[0],0)/n0, sp = cal.reduce((s,p)=>s+p[1],0)/n0;
  let num=0, den=0; cal.forEach(function(p){ num += (p[0]-sy)*(p[1]-sp); den += (p[0]-sy)*(p[0]-sy); });
  const slope = num/den, intercept = sp - slope*sy;
  const priceOfY = y => intercept + slope*y;
  const yOfPrice = p => (p - intercept) / slope;

  const strokes = { price:"var(--ink,#12211e)", ma50:"var(--teal,#12796B)", ma200:"var(--brass,#896F36)" };
  function pointsOf(strokeVal){
    const el = Array.prototype.slice.call(src.querySelectorAll("polyline")).find(function(pl){ return pl.getAttribute("stroke") === strokeVal; });
    if (!el) return [];
    return el.getAttribute("points").trim().split(/\s+/).map(function(s){
      const xy = s.split(","); return [parseFloat(xy[0]), parseFloat(xy[1])];
    });
  }
  const priceAll = pointsOf(strokes.price), ma50All = pointsOf(strokes.ma50), ma200All = pointsOf(strokes.ma200);
  if (!priceAll.length) return;
  const xAll = priceAll.map(p=>p[0]);
  const xMax = Math.max.apply(null, xAll), xMin = Math.min.apply(null, xAll);
  const pxPerSession = (xMax - xMin) / (priceAll.length - 1);
  const totalSessions = priceAll.length;

  const OPTIONS = [30, 60, 90, 180].filter(function(s){ return s <= totalSessions; });
  if (OPTIONS[OPTIONS.length-1] !== totalSessions && OPTIONS.length < 5) OPTIONS.push(totalSessions);
  let sessions = OPTIONS.indexOf(defaultSessions) >= 0 ? defaultSessions : OPTIONS[Math.min(2, OPTIONS.length-1)];

  const btns = OPTIONS.map(function(s){
    const lbl = (s >= totalSessions) ? "All" : s + "d";
    return '<button type="button" class="zoom-win-btn" data-s="'+s+'" style="'+
      'font-family:\'IBM Plex Mono\',monospace;font-size:12px;padding:4px 12px;border:1px solid var(--line);'+
      'background:transparent;color:var(--muted);border-radius:6px;cursor:pointer">'+lbl+'</button>';
  }).join("");

  host.innerHTML =
    '<div style="display:flex;align-items:baseline;justify-content:space-between;gap:12px;flex-wrap:wrap;margin-bottom:2px">'+
      '<p class="qhead" style="margin:0">Zoomed \u2014 recent window vs the levels</p>'+
      '<div id="'+targetElId+'-btns" style="display:flex;gap:6px">'+btns+'</div>'+
    '</div>'+
    '<p class="muted" style="font-size:var(--fs-small);margin:0 0 8px">Same price, 50-day MA and 200-day MA lines as the chart above, magnified so the support and resistance levels are readable against current price action. Pick a window.</p>'+
    '<div id="'+targetElId+'-svg"></div>';

  function draw(){
    const xThresh = xMax - (sessions - 1) * pxPerSession;
    function tail(arr){ return arr.filter(function(p){ return p[0] >= xThresh - 1e-6; }); }
    const priceT = tail(priceAll), ma50T = tail(ma50All), ma200T = tail(ma200All);
    if (priceT.length < 2) return;

    const allY = priceT.concat(ma50T).concat(ma200T).map(p=>p[1]);
    let yLo = Math.min.apply(null, allY), yHi = Math.max.apply(null, allY);
    // pixel space: larger y = lower price. Convert the pixel extremes to prices and
    // order them low->high (priceOfY(yHi) is the LOWEST price, priceOfY(yLo) the highest).
    const pA = priceOfY(yHi), pB = priceOfY(yLo);
    let pLo = Math.min(pA, pB), pHi = Math.max(pA, pB);
    // widen to include any reference level that falls in the window
    (res||[]).concat(sup||[]).forEach(function(p){ if (p < pLo) pLo = p; if (p > pHi) pHi = p; });
    const padP = (pHi - pLo) * 0.08 || 0.4;
    pLo -= padP; pHi += padP;

    const W = 760, H = 300, ML = 46, MR = 60, MT = 14, MB = 26;
    const X0 = ML, X1 = W - MR, Y0 = H - MB, Y1 = MT;
    const xLo = priceT[0][0], xHi = priceT[priceT.length-1][0];
    const xr = v => X0 + (v - xLo) / (xHi - xLo) * (X1 - X0);
    const yr = p => Y0 + (pHi - p) / (pHi - pLo) * (Y1 - Y0);

    function pathOf(arr){ return arr.map(function(p,i){ return (i?"L":"M") + xr(p[0]).toFixed(1) + "," + yr(priceOfY(p[1])).toFixed(1); }).join(" "); }

    // auto-fit ~7 nice gridlines for the current price window
    const rng = pHi - pLo;
    const raw = rng / 7;
    const mag = Math.pow(10, Math.floor(Math.log(raw)/Math.LN10));
    const norm = raw / mag;
    const stepN = norm >= 5 ? 5 : norm >= 2 ? 2 : norm >= 1 ? 1 : 0.5;
    const step = stepN * mag;
    const gdec = step < 1 ? (step < 0.5 ? 2 : 1) : 0;
    let grid = "";
    for (let g = Math.ceil(pLo/step)*step; g <= pHi; g += step){
      const y = yr(g);
      grid += '<line x1="'+X0+'" x2="'+X1+'" y1="'+y.toFixed(1)+'" y2="'+y.toFixed(1)+'" stroke="var(--line,#dce4e2)" stroke-width="1" opacity=".45"/>';
      grid += '<text x="'+(X0-8)+'" y="'+(y+3).toFixed(1)+'" text-anchor="end" font-size="10" fill="var(--muted,#6b7c78)" font-family="IBM Plex Mono,monospace">'+g.toFixed(gdec)+'</text>';
    }

    // reference lines, with collision-avoided right-edge labels
    const refRows = [];
    (res||[]).forEach(function(p){ if (p>=pLo && p<=pHi) refRows.push({p:p, y:yr(p), col:"var(--amber-text,#854F0B)"}); });
    (sup||[]).forEach(function(p){ if (p>=pLo && p<=pHi) refRows.push({p:p, y:yr(p), col:"var(--red,#B5483A)"}); });
    let refLines = "";
    refRows.forEach(function(r){
      refLines += '<line x1="'+X0+'" x2="'+X1+'" y1="'+r.y.toFixed(1)+'" y2="'+r.y.toFixed(1)+'" stroke="'+r.col+'" stroke-width="1.2" stroke-dasharray="5 3" opacity=".85"/>';
    });
    // label y-positions: sort, then push apart so none overlap (min 12px)
    const lab = refRows.map(function(r){ return {ly:r.y, col:r.col, txt:F(r.p)}; }).sort(function(a,b){ return a.ly-b.ly; });
    const minGap = 12;
    for (let i=1;i<lab.length;i++){ if (lab[i].ly - lab[i-1].ly < minGap) lab[i].ly = lab[i-1].ly + minGap; }
    // keep inside the plot
    for (let i=lab.length-1;i>=0;i--){ if (lab[i].ly > Y0) lab[i].ly = (i===lab.length-1? Y0 : lab[i+1].ly - minGap); }
    let refLabels = "";
    lab.forEach(function(l){
      refLabels += '<text x="'+(X1+6)+'" y="'+(l.ly+3.5).toFixed(1)+'" font-size="10.5" font-family="IBM Plex Mono,monospace" fill="'+l.col+'">'+l.txt+'</text>';
    });

    const lastPrice = priceOfY(priceT[priceT.length-1][1]);
    const dot = '<circle cx="'+xr(priceT[priceT.length-1][0]).toFixed(1)+'" cy="'+yr(lastPrice).toFixed(1)+'" r="3.5" fill="var(--gold,#C0A45F)"/>';

    // x tick labels (a few evenly spaced session offsets, counting back from latest)
    let xt = "";
    const nT = priceT.length;
    [0, Math.floor(nT*0.25), Math.floor(nT*0.5), Math.floor(nT*0.75), nT-1].forEach(function(idx){
      const back = (nT-1) - idx;
      const x = xr(priceT[idx][0]);
      xt += '<text x="'+x.toFixed(1)+'" y="'+(Y0+18)+'" text-anchor="middle" font-size="10" fill="var(--muted,#6b7c78)" font-family="IBM Plex Mono,monospace">'+(back===0?"latest":"-"+back)+'</text>';
    });

    document.getElementById(targetElId+"-svg").innerHTML =
      '<svg viewBox="0 0 '+W+' '+H+'" width="100%" role="img" aria-label="Zoomed recent price action against support and resistance">'+
        grid + refLines +
        '<path d="'+pathOf(ma200T)+'" fill="none" stroke="var(--brass,#896F36)" stroke-width="1.6" opacity=".85"/>'+
        '<path d="'+pathOf(ma50T)+'" fill="none" stroke="var(--teal,#12796B)" stroke-width="1.6" opacity=".85"/>'+
        '<path d="'+pathOf(priceT)+'" fill="none" stroke="var(--ink,#12211e)" stroke-width="1.6" opacity=".95"/>'+
        refLabels + xt + dot +
      '</svg>'+
      '<div style="display:flex;gap:16px;flex-wrap:wrap;font-size:12px;color:var(--muted,#6b7c78);margin-top:6px;font-family:\'IBM Plex Mono\',monospace">'+
        '<span style="display:inline-flex;align-items:center;gap:6px"><span style="width:14px;height:2px;background:var(--ink,#12211e);display:inline-block"></span> Price</span>'+
        '<span style="display:inline-flex;align-items:center;gap:6px"><span style="width:14px;height:2px;background:var(--teal,#12796B);display:inline-block"></span> 50-day MA</span>'+
        '<span style="display:inline-flex;align-items:center;gap:6px"><span style="width:14px;height:2px;background:var(--brass,#896F36);display:inline-block"></span> 200-day MA</span>'+
        '<span style="display:inline-flex;align-items:center;gap:6px"><span style="width:14px;height:0;border-top:1.2px dashed var(--amber-text,#854F0B);display:inline-block"></span> Resistance</span>'+
        '<span style="display:inline-flex;align-items:center;gap:6px"><span style="width:14px;height:0;border-top:1.2px dashed var(--red,#B5483A);display:inline-block"></span> Support</span>'+
      '</div>';

    // active-button styling
    Array.prototype.forEach.call(document.querySelectorAll("#"+targetElId+"-btns .zoom-win-btn"), function(b){
      const on = parseInt(b.getAttribute("data-s"),10) === sessions;
      b.style.borderColor = on ? "var(--teal,#12796B)" : "var(--line)";
      b.style.color = on ? "var(--teal,#12796B)" : "var(--muted)";
      b.style.fontWeight = on ? "600" : "400";
    });
  }

  host.querySelector("#"+targetElId+"-btns").addEventListener("click", function(e){
    const b = e.target.closest(".zoom-win-btn"); if (!b) return;
    sessions = parseInt(b.getAttribute("data-s"),10);
    draw();
  });
  draw();
}
