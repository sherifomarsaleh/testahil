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
      .end{fill:#8A9A98}.mid{fill:#1B5E5E}.tod{fill:#C98A2D}
      .band{fill:#1B5E5E;font-size:${fBand}px}
      .dat{font:500 ${fDate}px 'IBM Plex Mono',monospace;fill:#8A9A98}
    </style>
    <!-- wide range 5–95% -->
    <line x1="${X(d.p5)}" x2="${X(d.p95)}" y1="${y}" y2="${y}" stroke="#CFE0DE" stroke-width="12" stroke-linecap="round"/>
    <!-- middle half 25–75% -->
    <line x1="${X(d.p25)}" x2="${X(d.p75)}" y1="${y}" y2="${y}" stroke="#2A8F8F" stroke-width="22" stroke-linecap="round" opacity=".55"/>
    <!-- middle outcome mark -->
    <line x1="${X(d.p50)}" x2="${X(d.p50)}" y1="${y-20}" y2="${y+20}" stroke="#1B5E5E" stroke-width="6" stroke-linecap="round"/>
    <!-- latest-price mark -->
    <circle cx="${X(spot)}" cy="${y}" r="11" fill="#fff" stroke="#C98A2D" stroke-width="4"/>
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
    <span><i class="sw" style="background:#2A8F8F;opacity:.55;border-radius:3px"></i> where it lands half the time</span>
    <span><i class="sw" style="background:#CFE0DE;border-radius:3px"></i> almost the whole range (9 times in 10)</span>
    <span><i class="sw" style="background:#fff;border:3px solid #C98A2D"></i> latest price</span>
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
    return `<tr><td class="num">${r.anchor_date}</td><td>${r.instrument}</td><td class="num">${r.horizon_label}</td>
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
  const soon = COMING.filter(c=>c.status!=="covered").map(c=>({
    code:c.code.replace("EGX:",""), name:c.name, url:c.code.replace("EGX:","").toLowerCase()+".html", status:"Coming soon"
  }));
  const index = [...live, ...soon];

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
    <style>.g{font:600 ${fG}px 'IBM Plex Mono',monospace}.gsm{font:600 ${fGsm}px 'IBM Plex Mono',monospace}.gdt{font:500 ${fGdt}px 'IBM Plex Mono',monospace}.gmut{fill:#8A9A98}.gink{fill:var(--ink)}.gbase{fill:#1B5E5E}</style>
    <defs><linearGradient id="vg" gradientUnits="userSpaceOnUse" x1="${X(min)}" y1="0" x2="${X(max)}" y2="0">
      <stop offset="0" stop-color="#2E7D5B"/><stop offset="0.25" stop-color="#6FA85C"/><stop offset="0.5" stop-color="#C98A2D"/><stop offset="0.75" stop-color="#D06A2C"/><stop offset="1" stop-color="#C0392B"/>
    </linearGradient></defs>
    <rect x="${X(min)}" y="${y-6}" width="${X(max)-X(min)}" height="12" rx="6" fill="url(#vg)"/>
    <!-- our value mark + label ABOVE -->
    <line x1="${X(base)}" x2="${X(base)}" y1="${y-16}" y2="${y+16}" stroke="#1B5E5E" stroke-width="5"/>
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
  const soon = COMING.filter(c=>c.status!=="covered").map(c=>({code:c.code.replace("EGX:",""), name:c.name, url:c.code.replace("EGX:","").toLowerCase()+".html", status:"Coming soon"}));
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
      <td class="num">${F(t.spot)}</td>
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
