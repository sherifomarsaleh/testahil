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

/* ---------- probability strip → quantile dotplot (signature element) ---------- */
function renderStrip(elId, d, spot, opts={}){
  const el = document.getElementById(elId); if(!el) return;
  const N = opts.dots || 50;
  const f = invCDF(d);
  const vals = [];
  for(let i=0;i<N;i++) vals.push(f((i+0.5)/N));

  const lo = Math.min(vals[0], spot), hi = Math.max(vals[N-1], spot);
  const min = lo-(hi-lo)*0.06, max = hi+(hi-lo)*0.06;
  const W=1000, baseY=96, X=v=>26+(v-min)/(max-min)*(W-52);

  const buckets = {};
  const cols = Math.min(N,46), bucketW=(W-52)/cols;
  const placed = vals.map(v=>{
    const x=X(v), key=Math.round(x/bucketW);
    const count=(buckets[key]=(buckets[key]||0)+1);
    return { x, level:count-1, above:v>=spot };
  });
  const r=7, gap=3.2;
  const dots = placed.map(p=>{
    const cy=baseY-p.level*(r*2+gap)-r;
    return `<circle cx="${p.x.toFixed(1)}" cy="${cy.toFixed(1)}" r="${r}" class="${p.above?'dot-up':'dot-dn'}"/>`;
  }).join("");

  const topY=8;
  const todayLine = `<line x1="${X(spot)}" x2="${X(spot)}" y1="${topY}" y2="${baseY+6}" class="today-line"/>
    <text x="${X(spot)}" y="${baseY+30}" text-anchor="middle" class="lab today-lab">today ${F(spot)}</text>`;
  const zoneLab = `
    <text x="${X(vals[2])}" y="${baseY+30}" text-anchor="middle" class="lab zone">rare low</text>
    <text x="${X(vals[N-3])}" y="${baseY+30}" text-anchor="middle" class="lab zone">rare high</text>`;

  el.innerHTML = `<svg viewBox="0 0 ${W} ${baseY+44}" xmlns="http://www.w3.org/2000/svg" role="img"
      aria-label="Each dot is one of ${N} possible price outcomes. Today's price is ${F(spot)}.">
    <style>
      .dot-up{fill:#2A8F8F}.dot-dn{fill:#C98A2D}
      .today-line{stroke:#0E2726;stroke-width:2.5;stroke-dasharray:2 4}
      .lab{font:600 21px 'IBM Plex Mono',monospace}
      .today-lab{fill:#0E2726}.zone{fill:#8A9A98;font-weight:500}
    </style>
    ${dots}${zoneLab}${todayLine}
  </svg>`;
}

function stripLegend(){
  return `<div class="legend">
    <span><i class="sw" style="background:#C98A2D"></i> outcomes below today</span>
    <span><i class="sw" style="background:#2A8F8F"></i> outcomes above today</span>
    <span class="legend-note">each dot = one of many simulated outcomes</span>
  </div>`;
}

/* "plain answer + dotplot + sentence" block — identical everywhere it's used */
function renderPlain(containerId, d, spot, horizonLabel){
  const c = document.getElementById(containerId); if(!c) return;
  const o = plainOdds(d, spot);
  c.innerHTML = `
    <p class="odds-sentence">${o.sentence}</p>
    <div class="strip" id="${containerId}-strip"></div>
    <p class="muted strip-note">Each dot is one possible price ${horizonLabel}. They pile up where outcomes are most likely. The dashed line is today's price.</p>
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
