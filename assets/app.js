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
    sentence: `Out of 10 possible outcomes, about <b>${up10}</b> end higher than today and about <b>${down10}</b> end lower.`,
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
  const min = Math.min(d.p5, spot) - (Math.max(d.p95,spot)-Math.min(d.p5,spot))*0.06;
  const max = Math.max(d.p95, spot) + (Math.max(d.p95,spot)-Math.min(d.p5,spot))*0.06;
  const mob = (typeof window!=="undefined" && window.innerWidth < 640);
  const fLab = mob ? 30 : 19, fBand = mob ? 26 : 16;
  // vertical positions: spread the label rows further apart on mobile (bigger text)
  const W = 1000;
  const H = mob ? 168 : 128, y = mob ? 92 : 72;
  const topY = mob ? y-78 : y-54;   // extremes + middle row
  const bandY = mob ? y-40 : y-26;  // 25/75 row
  const todY = mob ? y+58 : y+44;   // today row
  const X = v=>40+(v-min)/(max-min)*(W-80);

  el.innerHTML = `<svg viewBox="0 0 ${W} ${H}" xmlns="http://www.w3.org/2000/svg" role="img"
      aria-label="Likely price range. Today's price is ${F(spot)}; the middle outcome is ${F(d.p50)}. Half of outcomes fall between ${F(d.p25)} and ${F(d.p75)}.">
    <style>
      .lab{font:600 ${fLab}px 'IBM Plex Mono',monospace}
      .end{fill:#8A9A98}.mid{fill:#1B5E5E}.tod{fill:#C98A2D}
      .band{fill:#2A8F8F;font-size:${fBand}px}
    </style>
    <!-- wide range 5–95% -->
    <line x1="${X(d.p5)}" x2="${X(d.p95)}" y1="${y}" y2="${y}" stroke="#CFE0DE" stroke-width="12" stroke-linecap="round"/>
    <!-- middle half 25–75% -->
    <line x1="${X(d.p25)}" x2="${X(d.p75)}" y1="${y}" y2="${y}" stroke="#2A8F8F" stroke-width="22" stroke-linecap="round" opacity=".55"/>
    <!-- middle outcome mark -->
    <line x1="${X(d.p50)}" x2="${X(d.p50)}" y1="${y-20}" y2="${y+20}" stroke="#1B5E5E" stroke-width="6" stroke-linecap="round"/>
    <!-- today mark -->
    <circle cx="${X(spot)}" cy="${y}" r="11" fill="#fff" stroke="#C98A2D" stroke-width="4"/>
    <!-- TOP row above the bar: rare extremes + middle outcome -->
    <text x="${X(d.p50)}" y="${topY}" text-anchor="middle" class="lab mid">middle ${F(d.p50)}</text>
    <text x="${X(d.p5)}" y="${topY}" text-anchor="middle" class="lab end">${F(d.p5)}</text>
    <text x="${X(d.p95)}" y="${topY}" text-anchor="middle" class="lab end">${F(d.p95)}</text>
    <!-- LOWER row, just above the bar: the 25%–75% middle-half edges -->
    <text x="${X(d.p25)}" y="${bandY}" text-anchor="middle" class="lab band">${F(d.p25)}</text>
    <text x="${X(d.p75)}" y="${bandY}" text-anchor="middle" class="lab band">${F(d.p75)}</text>
    <!-- today below the bar -->
    <text x="${X(spot)}" y="${todY}" text-anchor="middle" class="lab tod">today ${F(spot)}</text>
  </svg>`;
}

function stripLegend(){
  return `<div class="legend">
    <span><i class="sw" style="background:#2A8F8F;opacity:.55;border-radius:3px"></i> where it lands half the time</span>
    <span><i class="sw" style="background:#CFE0DE;border-radius:3px"></i> almost the whole range (9 times in 10)</span>
    <span><i class="sw" style="background:#fff;border:3px solid #C98A2D"></i> today's price</span>
  </div>`;
}

/* "plain answer + dotplot + sentence" block — identical everywhere it's used */
function renderPlain(containerId, d, spot, horizonLabel){
  const c = document.getElementById(containerId); if(!c) return;
  const o = plainOdds(d, spot);
  c.innerHTML = `
    <p class="odds-sentence">${o.sentence}</p>
    <div class="strip" id="${containerId}-strip"></div>
    <p class="muted strip-note">The teal band is where the price lands most of the time ${horizonLabel}. The thin band is the rare extremes. The gold dot is today.</p>
  `;
  renderStrip(`${containerId}-strip`, d, spot);
}

/* ---------- public ledger helper (kept) ---------- */
function buildLedger(tbodyId, summaryId){
  const tb=document.getElementById(tbodyId); if(!tb) return;
  let hit=0, scored=0;
  tb.innerHTML = LEDGER.map(r=>{
    let res;
    if(r.status==="open"){ res = `<span class="chip">waiting — we'll know on ${r.resolve}</span>`; }
    else { scored++; const inBand=r.realized>=r.lo&&r.realized<=r.hi; if(inBand) hit++;
      res = `<span class="num">${F(r.realized)}</span> ${inBand?'<span class="ok">landed in range ✓</span>':'<span class="bad">outside range ✗</span>'}`;}
    return `<tr><td class="num">${r.pub}</td><td>${r.inst}</td><td class="num">${r.horizon}</td>
      <td class="num">${F(r.median)}</td><td class="num">${F(r.lo)} – ${F(r.hi)}</td><td>${res}</td></tr>`;
  }).join("");
  const sm=document.getElementById(summaryId);
  if(sm) sm.textContent = scored
    ? `Our range contained the real price in ${hit} of ${scored} forecasts we've graded so far.`
    : `Nothing graded yet — first forecast comes due on ${LEDGER[0].resolve}. Everything we publish stays here, right or wrong.`;
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
  const usd = amt*CALC.usdEgp[i2]/CALC.usdEgp[i1];
  const gold= amt*CALC.gold21g[i2]/CALC.gold21g[i1];
  const egx = amt*CALC.egx30[i2]/CALC.egx30[i1];
  const rows=[["Bank CDs",cd],["US dollar",usd],["Gold (21k)",gold],["EGX30 index",egx]]
    .sort((a,b)=>b[1]-a[1]);
  const maxV=rows[0][1];
  out.innerHTML = `<table><thead><tr><th>Where you put it</th><th class="num">What you'd have</th><th class="num">Really worth*</th><th style="width:38%"></th></tr></thead><tbody>`+
    rows.map(([n,v])=>{const real=v/cpi; const pct=Math.max(4,v/maxV*100);
      return `<tr><td>${n}</td><td class="num">${F(v)}</td><td class="num">${F(real)}</td>
      <td><div style="background:${real>=amt?'#2E7D5B':'#B5483A'};opacity:.85;height:14px;border-radius:7px;width:${pct}%"></div></td></tr>`;}).join("")+
    `</tbody></table>
    <p class="muted">* After prices rose ${F((cpi-1)*100)}% over the period. Starting from EGP ${F(amt)}, end-${y1} to end-${y2}.</p>
    <p class="muted">A red bar means that even though the number grew, it bought less than when you started.</p>`;
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
  const soon = COMING.filter(c=>c.status!=="covered").map(c=>({
    code:c.code.replace("EGX:",""), name:c.name, url:null, status:"Coming soon"
  }));
  const index = [...live, ...soon];

  function render(q){
    q = q.trim().toLowerCase();
    if(!q){ box.innerHTML=""; box.classList.remove("open"); return; }
    const hits = index.filter(x =>
      x.code.toLowerCase().includes(q) || x.name.toLowerCase().includes(q));
    if(!hits.length){
      box.innerHTML = `<div class="tk-empty">No match. We currently cover Egyptian Exchange (EGX) stocks.</div>`;
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
   Shows where today's price sits versus our fair value: a simple
   "looks cheap / about right / looks expensive" reading, no buy/sell call. */
function valuationVerdict(spot, base){
  const gap = (base - spot)/spot;            // how far below fair value we are
  if(gap >=  0.15) return {label:"Looks cheap vs our estimate",   tone:"cheap",   gap};
  if(gap <= -0.15) return {label:"Looks expensive vs our estimate", tone:"rich",  gap};
  return {label:"About fairly priced vs our estimate", tone:"fair", gap};
}
function renderGauge(elId, spot, fair){
  const el=document.getElementById(elId); if(!el) return;
  const {bear,base,full}=fair;
  const lo=Math.min(bear,spot), hi=Math.max(full,spot);
  const pad=(hi-lo)*0.04, min=lo-pad, max=hi+pad;
  const mob = (typeof window!=="undefined" && window.innerWidth < 640);
  const fG = mob ? 28 : 18, fGsm = mob ? 24 : 15;
  const W=1000, H = mob ? 168 : 124, y = mob ? 62 : 46;
  const valY = mob ? y-34 : y-24, todY = mob ? y+46 : y+32, endY = mob ? y+82 : y+58;
  const X=v=>30+(v-min)/(max-min)*(W-60);
  const v=valuationVerdict(spot,base);
  const todayX = Math.max(70, Math.min(W-70, X(spot)));
  el.innerHTML = `<svg viewBox="0 0 ${W} ${H}" xmlns="http://www.w3.org/2000/svg" role="img"
      aria-label="Today's price ${F(spot)} versus our fair value ${F(base)}.">
    <style>.g{font:600 ${fG}px 'IBM Plex Mono',monospace}.gsm{font:600 ${fGsm}px 'IBM Plex Mono',monospace}.gmut{fill:#8A9A98}.gink{fill:#0E2726}.gbase{fill:#1B5E5E}</style>
    <defs><linearGradient id="vg" x1="0" x2="1">
      <stop offset="0" stop-color="#B5483A"/><stop offset="0.5" stop-color="#C98A2D"/><stop offset="1" stop-color="#2E7D5B"/>
    </linearGradient></defs>
    <line x1="${X(min)}" x2="${X(max)}" y1="${y}" y2="${y}" stroke="url(#vg)" stroke-width="12" stroke-linecap="round" opacity=".85"/>
    <!-- our value mark + label ABOVE -->
    <line x1="${X(base)}" x2="${X(base)}" y1="${y-16}" y2="${y+16}" stroke="#1B5E5E" stroke-width="5"/>
    <text x="${X(base)}" y="${valY}" text-anchor="middle" class="g gbase">our value ${F(base)}</text>
    <!-- today mark + label BELOW -->
    <circle cx="${X(spot)}" cy="${y}" r="10" fill="#fff" stroke="#0E2726" stroke-width="4"/>
    <text x="${todayX}" y="${todY}" text-anchor="middle" class="g gink">today ${F(spot)}</text>
    <!-- end labels on the lowest row -->
    <text x="30" y="${endY}" class="gsm gmut">← expensive</text>
    <text x="${W-30}" y="${endY}" text-anchor="end" class="gsm gmut">cheap →</text>
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
  const rows = Object.entries(TICKERS).map(([code,t])=>{
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
    <th>Stock</th><th class="num">Today</th><th class="num">Our value</th><th>Price view</th><th class="num">3-month odds</th>
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
  const soon = COMING.filter(c=>c.status!=="covered").map(c=>({code:c.code.replace("EGX:",""), name:c.name, url:null, status:"Coming soon"}));
  const index=[...live,...soon];

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
document.addEventListener("DOMContentLoaded",()=>{ initSearch(); initFirstRunHowto(); });

/* ---------- track-record badge (honest: shows scored hit-rate, or "awaiting" if none yet) ---------- */
function trackRecord(){
  const scored = LEDGER.filter(r=>r.status==="scored" && r.realized!=null);
  const inrange = scored.filter(r=>r.realized>=r.lo && r.realized<=r.hi).length;
  const open = LEDGER.filter(r=>r.status==="open").length;
  // next resolve date among open forecasts
  const nextDate = LEDGER.filter(r=>r.status==="open").map(r=>r.resolve).sort()[0] || null;
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
function renderCompare(elId){
  const el=document.getElementById(elId); if(!el) return;
  const rows = Object.entries(TICKERS).map(([code,t])=>{
    const o60=plainOdds(t.dist.t60, t.spot);
    const v=valuationVerdict(t.spot, t.fair.base);
    const up60=Math.round(o60.pa*10);
    const fvGap = Math.round((t.fair.base-t.spot)/t.spot*100);
    const trend = (t.tech&&t.tech.trend) ? t.tech.trend : "—";
    return `<tr>
      <td><a href="${code.toLowerCase()}.html"><b>${t.name}</b></a><br><span class="muted num" style="font-size:.8rem">${t.code}</span></td>
      <td class="num">${F(t.spot)}</td>
      <td class="num">${F(t.fair.base)}<br><span class="muted" style="font-size:.8rem">${fvGap>=0?'+':''}${fvGap}%</span></td>
      <td><span class="pill ${v.tone}">${v.tone==='cheap'?'Looks cheap':v.tone==='rich'?'Looks expensive':'About right'}</span></td>
      <td class="num">${F(t.dist.t60.p50)}</td>
      <td class="num">${up60} in 10</td>
      <td style="font-size:.85rem">${trend}</td>
    </tr>`;
  }).join("");
  // coming-soon rows (names only)
  const soon = COMING.filter(c=>c.status!=="covered").map(c=>
    `<tr class="cmp-soon"><td><b>${c.name}</b><br><span class="muted num" style="font-size:.8rem">${c.code}</span></td>
     <td colspan="6" class="muted">Coming soon — <a href="${c.code.replace('EGX:','').toLowerCase()}.html">get notified</a></td></tr>`
  ).join("");
  el.innerHTML = `<table class="compare-table"><thead><tr>
    <th>Stock</th><th class="num">Today</th><th class="num">Our value</th><th>Price view</th>
    <th class="num">3-mo middle</th><th class="num">Odds up (3-mo)</th><th>Chart trend</th>
  </tr></thead><tbody>${rows}${soon}</tbody></table>`;
}
