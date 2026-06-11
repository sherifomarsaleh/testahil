/* testahil — app.js : strip renderer + ledger + calculator */

const F = n => Number(n).toLocaleString("en-US",{maximumFractionDigits:2});

/* ---------- probability strip (signature element) ---------- */
function renderStrip(elId, d, spot){
  const el = document.getElementById(elId); if(!el) return;
  const min = Math.min(d.p5, spot)*0.97, max = Math.max(d.p95, spot)*1.03;
  const W=1000, H=84, y=46, X=v=>20+(v-min)/(max-min)*(W-40);
  const tag=(x,txt,cls,anchor="middle")=>`<text x="${x}" y="${y-26}" text-anchor="${anchor}" class="t ${cls}">${txt}</text>`;
  el.innerHTML = `<svg viewBox="0 0 ${W} ${H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="probability distribution">
  <style>.t{font:600 22px 'IBM Plex Mono',monospace;fill:#5B7270}.t.md{fill:#1B5E5E}.t.sp{fill:#C98A2D}</style>
  <line x1="${X(d.p5)}" x2="${X(d.p95)}" y1="${y}" y2="${y}" stroke="#BFD3D0" stroke-width="6" stroke-linecap="round"/>
  <line x1="${X(d.p25)}" x2="${X(d.p75)}" y1="${y}" y2="${y}" stroke="#2A8F8F" stroke-width="14" stroke-linecap="round" opacity=".55"/>
  <line x1="${X(d.p50)}" x2="${X(d.p50)}" y1="${y-15}" y2="${y+15}" stroke="#1B5E5E" stroke-width="5"/>
  <circle cx="${X(spot)}" cy="${y}" r="8" fill="#C98A2D"/>
  ${tag(X(d.p5), F(d.p5),"" ,"start")}${tag(X(d.p95), F(d.p95),"","end")}
  ${tag(X(d.p50), F(d.p50),"md")}
  <text x="${X(spot)}" y="${y+34}" text-anchor="middle" class="t sp">${F(spot)}</text>
  </svg>`;
}
function stripLegend(){return `<div class="legend">
  <span><i style="background:#C98A2D;border-radius:50%;width:10px;height:10px"></i> current price</span>
  <span><i style="background:#1B5E5E"></i> median (50%)</span>
  <span><i style="background:#2A8F8F;opacity:.55"></i> 50% of paths</span>
  <span><i style="background:#BFD3D0"></i> 90% of paths</span></div>`;}

/* ---------- public ledger ---------- */
function buildLedger(tbodyId, summaryId){
  const tb=document.getElementById(tbodyId); if(!tb) return;
  let hit=0, scored=0;
  tb.innerHTML = LEDGER.map(r=>{
    let res;
    if(r.status==="open"){ res = `<span class="chip">open — resolves ${r.resolve}</span>`; }
    else { scored++; const inBand = r.realized>=r.lo && r.realized<=r.hi; if(inBand) hit++;
      res = `<span class="num">${F(r.realized)}</span> ${inBand?'<span class="ok">inside band ✓</span>':'<span class="bad">outside band ✗</span>'}`;}
    return `<tr><td class="num">${r.pub}</td><td>${r.inst}</td><td class="num">${r.horizon}</td>
      <td class="num">${F(r.median)}</td><td class="num">${F(r.lo)} – ${F(r.hi)} <span class="muted">(${r.band})</span></td><td>${res}</td></tr>`;
  }).join("");
  const sm=document.getElementById(summaryId);
  if(sm) sm.textContent = scored
    ? `Published bands contained the realized price in ${hit} of ${scored} resolved forecasts.`
    : `No resolved forecasts yet — first resolution on ${LEDGER[0].resolve}. Everything published stays here, right or wrong.`;
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
  out.innerHTML = `<table><thead><tr><th>Asset</th><th class="num">Nominal value</th><th class="num">Real value*</th><th style="width:38%"></th></tr></thead><tbody>`+
    rows.map(([n,v])=>{const real=v/cpi; const pct=Math.max(4,v/maxV*100);
      return `<tr><td>${n}</td><td class="num">${F(v)}</td><td class="num">${F(real)}</td>
      <td><div style="background:${real>=amt?'#2E7D5B':'#B5483A'};opacity:.8;height:12px;border-radius:6px;width:${pct}%"></div></td></tr>`;}).join("")+
    `</tbody></table>
    <p class="muted">* Real value = after cumulative inflation of ${F((cpi-1)*100)}% over the period. EGP ${F(amt)} from end-${y1} to end-${y2}.</p>
    <p class="muted">A red real value means the asset failed to preserve your purchasing power even though its nominal number grew.</p>`;
}
function initCalc(){
  const from=document.getElementById("c-from"), to=document.getElementById("c-to");
  if(!from) return;
  CALC.years.forEach(y=>{from.add(new Option(y,y)); to.add(new Option(y,y));});
  from.value=CALC.years[0]; to.value=CALC.years.at(-1);
  if(!CALC.verified) document.getElementById("c-warn").style.display="block";
  runCalc();
}
document.addEventListener("DOMContentLoaded",()=>{ initCalc(); });
