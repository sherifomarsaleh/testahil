/* testahil /test/ — shared chrome + math. Reads TICKERS/METALS/COMING/BANDS/LEDGER/CALC from ../assets/data.js */
(function(){
"use strict";
/* ---------- instrument map: stocks + metals in one shape ---------- */
window.ALL = {};
Object.keys(TICKERS).forEach(function(k){ ALL[k] = TICKERS[k]; });
Object.keys(METALS).forEach(function(k){ var m = METALS[k]; if(m && m.dist) ALL[k] = m; });
window.mktOf = function(t){
  var ex = (t.code||"").split(":")[0].split("/")[0];
  return ({EGX:"Egypt", ADX:"UAE", DFM:"UAE", TADAWUL:"Saudi", QSE:"Qatar", KRX:"Korea", NSE:"India",
    NASDAQ:"US", NYSE:"US", XAU:"Metals", XAG:"Metals", XPT:"Metals"})[ex] || (t.unitEn ? "Metals" : "Other");
};
window.keyOf = function(t){ for(var k in ALL){ if(ALL[k]===t) return k; } return null; };
window.pageFor = function(k){ return "study.html?t=" + encodeURIComponent(k); };

/* ---------- math (ported verbatim in spirit from trade.html / portfolio.html) ---------- */
window.invCDF = function(d){
  var pts = [[0.05,d.p5],[0.25,d.p25],[0.50,d.p50],[0.75,d.p75],[0.95,d.p95]];
  return function(p){
    if(p <= pts[0][0]){ var p1=pts[0][0],v1=pts[0][1],p2=pts[1][0],v2=pts[1][1];
      return Math.max(v1-(v2-v1)*((p1-p)/(p2-p1)), v1*0.80); }
    if(p >= pts[4][0]){ var p1b=pts[3][0],v1b=pts[3][1],p2b=pts[4][0],v2b=pts[4][1];
      return v2b+(v2b-v1b)*((p-p2b)/(p2b-p1b)); }
    for(var i=0;i<pts.length-1;i++){ var pa=pts[i][0],va=pts[i][1],pb=pts[i+1][0],vb=pts[i+1][1];
      if(p>=pa&&p<=pb) return va+(vb-va)*((p-pa)/(pb-pa)); }
    return d.p50;
  };
};
window.probAbove = function(d, price){
  var f = invCDF(d);
  if(price <= f(0.001)) return 0.99;
  for(var p=0.002;p<=0.999;p+=0.001){ if(f(p) >= price) return Math.min(0.99, Math.max(0.01, 1-p)); }
  return 0.01;
};
window.BIG_PCT = 10;
window.computeBuckets = function(d, spot){
  var up = probAbove(d, spot*(1+BIG_PCT/100));
  var aboveSpot = probAbove(d, spot);
  var down = probAbove(d, spot*(1-BIG_PCT/100));
  var bigGain = Math.max(0, up), bigLoss = Math.max(0, 1-down);
  var smallGain = Math.max(0, aboveSpot-up), smallLoss = Math.max(0, (1-aboveSpot)-bigLoss);
  var s = bigGain+smallGain+smallLoss+bigLoss || 1;
  return { bigGain:bigGain/s, smallGain:smallGain/s, smallLoss:smallLoss/s, bigLoss:bigLoss/s, up:aboveSpot };
};
window.retQ = function(t, which, p){ return invCDF(t.dist[which])(p)/t.spot - 1; };
window.normCdf = function(x){
  var t = 1/(1+0.2316419*Math.abs(x));
  var d = 0.3989423*Math.exp(-x*x/2);
  var p = d*t*(0.3193815+t*(-0.3565638+t*(1.781478+t*(-1.821256+t*1.330274))));
  return x>0 ? 1-p : p;
};
/* co-movement assumption — same figures and rationale as portfolio.html */
window.RHO_SAME = 0.55; window.RHO_CROSS = 0.25;
window.mulberry32 = function(a){ return function(){ a|=0; a=a+0x6D2B79F5|0; var t=Math.imul(a^a>>>15,1|a); t=t+Math.imul(t^t>>>7,61|t)^t; return ((t^t>>>14)>>>0)/4294967296; }; };

/* ---------- formatting ---------- */
window.fmtPct = function(x,dp){ return (x*100).toFixed(dp==null?0:dp)+"%"; };
window.fmtSPct = function(x,dp){ var v=(x*100).toFixed(dp==null?0:dp); return (x>=0?"+":"")+v+"%"; };
window.fmtPx = function(v,ccy){
  var dp = v>=1000?0:(v>=100?1:2);
  return v.toLocaleString("en-US",{minimumFractionDigits:dp,maximumFractionDigits:dp})+(ccy?" "+ccy:"");
};
window.gapOf = function(t){ return (t.fair && t.fair.base) ? t.fair.base/t.spot - 1 : null; };
window.verdictOf = function(t){
  var g = gapOf(t); if(g==null) return {label:"—", cls:"mut"};
  if(g >= 0.15) return {label:"looks cheap", cls:"good"};
  if(g <= -0.15) return {label:"looks expensive", cls:"bad"};
  return {label:"near fair value", cls:"mut"};
};
window.reachOf = function(t){ /* can the central fair value be reached inside the 3-month cone? */
  var g = gapOf(t), d = t.dist && t.dist.t60; if(g==null || !d) return null;
  var fv = t.fair.base;
  if(g >= 0){ if(fv <= d.p75) return {label:"IN REACH", cls:"good", rank:0};
    if(fv <= d.p95) return {label:"STRETCH", cls:"warn", rank:1};
    return {label:"OUT OF REACH", cls:"bad", rank:2}; }
  if(fv >= d.p25) return {label:"IN REACH", cls:"good", rank:0};
  if(fv >= d.p5) return {label:"STRETCH", cls:"warn", rank:1};
  return {label:"OUT OF REACH", cls:"bad", rank:2};
};
window.bandTotals = function(){
  var n=0, hits=0; Object.keys(BANDS).forEach(function(k){ n+=BANDS[k].n; hits+=BANDS[k].hits; });
  return {n:n, hits:hits, pct:hits/n};
};

/* ---------- shared chrome ---------- */
function el(html){ var d=document.createElement("div"); d.innerHTML=html; return d.firstElementChild; }
window.tNum = function(x){ return x.toLocaleString("en-US"); };
window.renderChrome = function(active){
  var bt = bandTotals();
  var nav = el('<div>'+
    '<header class="nav t-nav"><div class="wrap">'+
      '<a class="brand" href="index.html">testahil?</a>'+
      '<nav>'+
        '<a href="coverage.html" data-p="coverage">Coverage</a>'+
        '<a href="tools.html" data-p="tools">Tools</a>'+
        '<a href="savings.html" data-p="savings">Savings check</a>'+
        '<a href="record.html" data-p="record">Track record</a>'+
        '<a href="method.html" data-p="method">Method</a>'+
      '</nav>'+
      '<div class="t-right">'+
        '<div class="t-search"><input id="t-q" type="search" placeholder="🔍 Search a stock…" autocomplete="off"><div class="t-dd" id="t-qq"></div></div>'+
        '<button class="t-theme" id="theme-toggle" title="Light / dark" aria-label="Toggle theme">◐</button>'+
      '</div>'+
    '</div></header>'+
    '<a class="t-strip" href="record.html"><span class="wrap"><b>Track record:</b>&nbsp;<span class="num">'+tNum(bt.n)+'</span>&nbsp;3-month windows checked ·&nbsp;<span class="num">'+tNum(bt.hits)+'</span>&nbsp;inside the 90% band ('+Math.round(bt.pct*100)+'%) → every one dated, right or wrong</span></a>'+
  '</div>');
  document.body.insertBefore(nav, document.body.firstChild);
  var on = nav.querySelector('[data-p="'+active+'"]'); if(on) on.classList.add("on");
  initSearch(document.getElementById("t-q"), document.getElementById("t-qq"));
  var big = document.getElementById("t-bigq");
  if(big) initSearch(big, document.getElementById("t-bigqq"));
  document.body.appendChild(el('<footer class="t-footer"><div class="wrap">'+
    '<span>Educational studies, not investment advice — not licensed by Egypt’s FRA. <a href="method.html#disclaimer">Full disclaimer</a></span>'+
    '<span>Data: <span class="num">'+SITE.updated+'</span> · <a href="../index.html">current site ↗</a></span>'+
  '</div></footer>'));
  document.body.appendChild(el('<div class="t-testflag">TEST PREVIEW — new structure, live data</div>'));
};
/* search across stocks + metals + coming */
function searchIndex(){
  var ix = [];
  Object.keys(ALL).forEach(function(k){ var t=ALL[k];
    ix.push({k:k, name:t.name, ar:t.nameAr||"", code:t.code, sub:mktOf(t), href:pageFor(k)}); });
  (window.COMING||[]).forEach(function(c){
    if(c.status==="covered") return; /* covered ones already have TICKERS entries */
    ix.push({k:c.code, name:c.name, ar:c.nameAr||"", code:c.code, sub:"coming soon", href:null});
  });
  return ix;
}
window.initSearch = function(input, dd){
  if(!input || !dd) return;
  var ix = searchIndex(), sel = -1, rows = [];
  function paint(q){
    q = q.trim().toLowerCase();
    var hits = !q ? [] : ix.filter(function(r){
      return r.name.toLowerCase().indexOf(q)>-1 || r.code.toLowerCase().indexOf(q)>-1 ||
             (r.k+"").toLowerCase().indexOf(q)>-1 || (r.ar && r.ar.indexOf(q)>-1);
    }).slice(0,9);
    rows = hits; sel = -1;
    dd.innerHTML = hits.map(function(r,i){
      var inner = '<span class="t-code num">'+r.code+'</span><span class="t-nm">'+r.name+'</span><span class="t-sub">'+r.sub+'</span>';
      return r.href ? '<a href="'+r.href+'" data-i="'+i+'">'+inner+'</a>'
                    : '<a data-i="'+i+'" style="opacity:.55;cursor:default">'+inner+'</a>';
    }).join("") || (q ? '<a style="cursor:default"><span class="t-nm" style="color:var(--muted)">No covered name matches “'+q.replace(/</g,"&lt;")+'”</span></a>' : "");
    dd.classList.toggle("open", !!dd.innerHTML);
  }
  input.addEventListener("input", function(){ paint(input.value); });
  input.addEventListener("focus", function(){ paint(input.value); });
  input.addEventListener("keydown", function(e){
    var as = dd.querySelectorAll("a[data-i]");
    if(e.key==="ArrowDown"||e.key==="ArrowUp"){ e.preventDefault();
      sel = e.key==="ArrowDown" ? Math.min(sel+1, as.length-1) : Math.max(sel-1, 0);
      as.forEach(function(a,i){ a.classList.toggle("sel", i===sel); });
    } else if(e.key==="Enter"){ var r = rows[sel>-1?sel:0]; if(r && r.href) location.href = r.href; }
    else if(e.key==="Escape"){ dd.classList.remove("open"); input.blur(); }
  });
  document.addEventListener("click", function(e){ if(!input.parentElement.contains(e.target)) dd.classList.remove("open"); });
};
})();
