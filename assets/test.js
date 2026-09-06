/* testahil / — shared chrome + math. Reads TICKERS/METALS/COMING/BANDS/LEDGER/CALC from ../assets/data.js */
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
window.pageFor = function(k){ return "/" + encodeURIComponent(k) + "/study/"; };

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


/* ---------- shared OHLC library access ---------- */
window.OHLC_BASE="https://raw.githubusercontent.com/sherifomarsaleh/testahil/main/engine/raw_ohlc/";
window.OHLC_PATH={DU:"AE/DU.csv",BOROUGE:"AE/BOROUGE.csv",EMPOWER:"AE/EMPOWER.csv","2POINTZERO":"AE/TWOPOINTZERO.csv",AAPL:"US/AAPL.csv",ABUK:"EG/ABUK.csv",ACWA:"SA/ACWA.csv",ADCB:"AE/ADCB.csv",ADNOCDRILL:"AE/ADNOCDRILL.csv",ADNOCDIST:"AE/ADNOCDIST.csv",ADIB:"EG/ADIB.csv",ADIBUAE:"AE/ADIB.csv",ADNOCGAS:"AE/ADNOCGAS.csv",ADNOCLS:"AE/ADNOCLS.csv",AGTHIA:"AE/AGTHIA.csv",ALDAR:"AE/ALDAR.csv",ALINMA:"SA/ALINMA.csv",AMOC:"EG/AMOC.csv",ARCC:"EG/ARCC.csv",ALPHADHABI:"AE/ALPHADHABI.csv",ALRAJHI:"SA/RAJHI.csv",ARAMCO:"SA/ARAMCO.csv",BTFH:"EG/BTFH.csv",BURJEEL:"AE/BURJEEL.csv",CCAP:"EG/CCAP.csv",CLHO:"EG/CLHO.csv",COMI:"EG/COMI.csv",DEWA:"AE/DEWA.csv",DIB:"AE/DIB.csv",DSCW:"EG/DSCW.csv",EAND:"AE/EAND.csv",ELEC:"EG/ELEC.csv",EFID:"EG/EFID.csv",EFIH:"EG/EFIH.csv",EGAL:"EG/EGAL.csv",ELM:"SA/ELM.csv",EMAAR:"AE/EMAAR.csv",EMAARDEV:"AE/EMAARDEV.csv",EMFD:"EG/EMFD.csv",ENBD:"AE/ENBD.csv",ETEL:"EG/ETEL.csv",EXTRA:"SA/EXTRA.csv",FAB:"AE/FAB.csv",FERTIGLB:"AE/FERTIGLB.csv",FWRY:"EG/FWRY.csv",GBCO:"EG/GBCO.csv",Gold:"XAU/GOLD.csv",HELI:"EG/HELI.csv",HRHO:"EG/HRHO.csv",IHC:"AE/IHC.csv",INFY:"IN/INFY.csv",IQCD:"QA/IQCD.csv",ISPH:"EG/ISPH.csv",JUFO:"EG/JUFO.csv",KABO:"EG/KABO.csv",Kakao:"KR/KAKAO.csv",LCSW:"EG/LCSW.csv",LGES:"KR/LGES.csv",LULU:"AE/LULU.csv",MAADEN:"SA/MAADEN.csv",MODON:"AE/MODON.csv",NVDA:"US/NVDA.csv",OCDI:"EG/OCDI.csv",OIH:"EG/OIH.csv",ORAS:"EG/ORAS.csv",ORHD:"EG/ORHD.csv",ORWE:"EG/ORWE.csv",AIRARABIA:"AE/AIRARABIA.csv",AMR:"AE/AMR.csv",PHAR:"EG/PHAR.csv",PHDC:"EG/PHDC.csv",PRDC:"EG/PRDC.csv",QGTS:"QA/QGTS.csv",QNB:"QA/QNB.csv",RAYA:"EG/RAYA.csv",RELIANCE:"IN/RELIANCE.csv",RIBL:"SA/RIBL.csv",RIYADHCABLE:"SA/RIYADHCABLE.csv",SAVOLA:"SA/SAVOLA.csv",RMDA:"EG/RMDA.csv",SABIC:"SA/SABIC.csv",SALIK:"AE/SALIK.csv",SCEM:"EG/SCEM.csv",EGCH:"EG/EGCH.csv",SNB:"SA/SNB.csv",STC:"SA/STC.csv",SWDY:"EG/SWDY.csv",Samsung:"KR/SAMSUNG.csv",Silver:"XAU/SILVER.csv",TMGH:"EG/TMGH.csv",TMPV:"IN/TMPV.csv",TSLA:"US/TSLA.csv",Platinum:"XPT/PLATINUM.csv"};
window.fetchOHLC=async function(instr){
  var p=OHLC_PATH[instr]||OHLC_PATH[instr.charAt(0)+instr.slice(1).toLowerCase()]; if(!p) return null;
  try{ var r=await fetch(OHLC_BASE+p); if(!r.ok) return null; var text=await r.text();
    var splitRow=function(l){ if(l.indexOf('"')!==-1){ var out=[],re=/"([^"]*)"/g,mm; while((mm=re.exec(l))) out.push(mm[1]); return out; } return l.split(","); };
    var toISO=function(d){ var mm=/(\d{1,2})\/(\d{1,2})\/(\d{4})/.exec(d); return mm?mm[3]+"-"+("0"+mm[1]).slice(-2)+"-"+("0"+mm[2]).slice(-2):null; };
    return text.split(/\r?\n/).slice(1).map(splitRow).filter(function(c){return c[0]&&c[1]})
      .map(function(c){return {iso:toISO(c[0]),price:parseFloat(String(c[1]).replace(/,/g,""))}})
      .filter(function(o){return o.iso&&isFinite(o.price)}).sort(function(a,b){return a.iso.localeCompare(b.iso)});
  }catch(e){ return null; }
};
/* ---------- formatting ---------- */
window.fmtPct = function(x,dp){ return (x*100).toFixed(dp==null?0:dp)+"%"; };
window.fmtSPct = function(x,dp){ var v=(x*100).toFixed(dp==null?0:dp); return (x>=0?"+":"")+v+"%"; };
window.fmtPx = function(v,ccy){
  var dp = v>=1000?0:(v>=100?1:2);
  return v.toLocaleString("en-US",{minimumFractionDigits:dp,maximumFractionDigits:dp})+(ccy?" "+ccy:"");
};
/* ---------- the price a comparison is made against ----------
   TICKERS[k].spot is the price a cone was STRUCK at, which is right for the
   forecast and wrong for a gap: a fair value is measured against the LATEST
   KNOWN price. PRICES carries the freshest price this repository holds for each
   name WITH ITS OWN DATE — prices are entered by hand, so they lag, and the
   honest answer is to print the date rather than to imply the number is today's.
   One route, so every surface agrees; falls back to the strike when a name is
   not in the block. */
window.latestPx = function(k, t){
  var p = (typeof PRICES !== "undefined") ? PRICES[k] : null;
  if(p && p.px > 0) return {px:p.px, date:p.date, src:p.src, strike:false};
  var d = (t && t.spotDate || "").replace(/^close\s+/i, "");
  return {px: t && t.spot, date: d, src: "strike", strike: true};
};
window.pxAge = function(iso){            /* whole days, or null if undated */
  if(!iso || !/^\d{4}-\d{2}-\d{2}$/.test(iso)) return null;
  return Math.max(0, Math.round((Date.now() - Date.parse(iso+"T00:00:00Z"))/864e5));
};
window.fmtPxDate = function(iso){        /* 2026-09-03 -> 3 Sep 2026 */
  if(!iso) return "";
  var m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(iso);
  if(!m) return iso;
  var M = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];
  return (+m[3]) + " " + M[(+m[2])-1] + " " + m[1];
};
window.gapOf = function(t, k){
  if(!(t && t.fair && t.fair.base)) return null;
  var px = (k ? latestPx(k, t).px : t.spot);
  return px > 0 ? t.fair.base/px - 1 : null;
};
window.verdictOf = function(t, k){
  var g = gapOf(t, k); if(g==null) return {label:"—", cls:"mut"};
  if(g >= 0.15) return {label:"looks cheap", cls:"good"};
  if(g <= -0.15) return {label:"looks expensive", cls:"bad"};
  return {label:"near fair value", cls:"mut"};
};
window.reachOf = function(t, k){ /* can the central fair value be reached inside the 3-month cone? */
  /* the percentiles stay on the CONE's own clock — it was built on the strike
     spot and does not move when a fresher price arrives; only the direction of
     the gap is taken from the latest price. Two clocks, kept apart on purpose. */
  var g = gapOf(t, k), d = t.dist && t.dist.t60; if(g==null || !d) return null;
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
window.tNum = function(x){ return x.toLocaleString("en-US"); };
window.renderChrome = function(active){
  var nav=document.querySelector(".t-nav");
  /* Funnel is a tab inside Tools, not a top-level destination, so Tools stays
     lit on every one of its tabs — including /tools.html#funnel. */
  function markNav(){
    if(!nav) return;
    nav.querySelectorAll("[data-p]").forEach(function(a){ a.classList.remove("on"); });
    var on = active && nav.querySelector('[data-p="'+active+'"]');
    if(on) on.classList.add("on");
  }
  markNav();
  try{ var bt=bandTotals();
    var n=document.getElementById("ts-n"); if(n) n.textContent=tNum(bt.n);
    var h=document.getElementById("ts-h"); if(h) h.textContent=tNum(bt.hits);
    var p=document.getElementById("ts-p"); if(p) p.textContent=Math.round(bt.pct*100)+"%";
  }catch(e){}
  try{ var u=document.getElementById("tf-upd"); if(u) u.textContent=SITE.updated; }catch(e){}
  initSearch(document.getElementById("t-q"), document.getElementById("t-qq"));
  var big=document.getElementById("t-bigq");
  if(big) initSearch(big, document.getElementById("t-bigqq"));
  document.querySelectorAll(".t-accordion>button").forEach(function(b){ b.setAttribute("aria-expanded", b.parentElement.classList.contains("open")?"true":"false"); });
  if(!window.__accWired){ window.__accWired=true;
    document.addEventListener("click", function(e){
      var b=e.target.closest&&e.target.closest(".t-accordion>button"); if(!b) return;
      var open=b.parentElement.classList.toggle("open");
      b.setAttribute("aria-expanded", open?"true":"false");
    });
  }
  var tf=document.querySelector(".t-testflag");
  if(tf){ var lastY=0;
    window.addEventListener("scroll",function(){ var y=window.scrollY||0; tf.classList.toggle("hid", y>160&&y>lastY); lastY=y; },{passive:true});
  }
};
/* search across stocks + metals + coming */
var AKA={OCDI:"SODIC",COMI:"CIB Commercial International Bank",HRHO:"EFG Hermes",EAND:"Etisalat e& eand",TMGH:"TMG Talaat Mostafa",SWDY:"Elsewedy El Sewedy",ADIBUAE:"ADIB Abu Dhabi",ADIB:"ADIB Egypt",LGES:"LG Energy Solution",ALRAJHI:"Al Rajhi",GOLD:"XAU dahab",SILVER:"XAG fadda",PLATINUM:"XPT",ARAMCO:"Saudi Aramco",PHDC:"Palm Hills"};
function searchIndex(){
  var ix = [];
  Object.keys(ALL).forEach(function(k){ var t=ALL[k];
    ix.push({k:k, name:t.name, ar:t.nameAr||"", code:t.code, sub:mktOf(t), aka:AKA[k]||"", href:pageFor(k)}); });
  (window.COMING||[]).forEach(function(c){
    if(c.status==="covered") return; /* covered ones already have TICKERS entries */
    ix.push({k:c.code, name:c.name, ar:c.nameAr||"", code:c.code, sub:"coming soon", href:null});
  });
  return ix;
}
window.initSearch = function(input, dd){
  if(!input || !dd) return;
  input.setAttribute("role","combobox"); input.setAttribute("aria-autocomplete","list"); input.setAttribute("aria-expanded","false");
  dd.setAttribute("role","listbox");
  var ix = searchIndex(), sel = -1, rows = [];
  function paint(q){
    q = q.trim().toLowerCase();
    var qs=q.replace(/\s+/g,"");
    var hits = !q ? [] : ix.filter(function(r){
      var hay=(r.name+" "+r.code+" "+r.k+" "+(r.aka||"")).toLowerCase();
      return hay.indexOf(q)>-1 || hay.replace(/\s+/g,"").indexOf(qs)>-1 || (r.ar && r.ar.indexOf(q)>-1);
    }).slice(0,9);
    rows = hits; sel = -1;
    var rowsHtml = hits.map(function(r,i){
      var inner = '<span class="t-code num">'+r.code+'</span><span class="t-nm">'+r.name+(r.ar?' <span style="color:var(--muted);font-size:var(--fs-caption)">'+r.ar+'</span>':'')+'</span><span class="t-sub">'+r.sub+'</span>';
      return r.href ? '<a href="'+r.href+'" data-i="'+i+'">'+inner+'</a>'
                    : '<a data-i="'+i+'" style="opacity:.55;cursor:default">'+inner+'</a>';
    }).join("");
    if(!rowsHtml && q) rowsHtml='<a style="cursor:default"><span class="t-nm" style="color:var(--muted)">No covered name matches “'+q.replace(/</g,"&lt;")+'”</span></a>';
    rowsHtml+='<a href="/coverage.html"><span class="t-nm" style="font-weight:600;color:var(--teal)">Browse all '+Object.keys(ALL).length+' names →</span></a>';
    dd.innerHTML=rowsHtml;
    dd.querySelectorAll("a").forEach(function(a){ a.setAttribute("role","option"); });
    dd.classList.add("open");
    input.setAttribute("aria-expanded","true");
  }
  input.addEventListener("input", function(){ paint(input.value); });
  input.addEventListener("focus", function(){ paint(input.value); });
  input.addEventListener("keydown", function(e){
    var as = dd.querySelectorAll("a[data-i]");
    if(e.key==="ArrowDown"||e.key==="ArrowUp"){ e.preventDefault();
      sel = e.key==="ArrowDown" ? Math.min(sel+1, as.length-1) : Math.max(sel-1, 0);
      as.forEach(function(a,i){ a.classList.toggle("sel", i===sel); });
    } else if(e.key==="Enter"){ var r = sel>-1 ? rows[sel] : rows.filter(function(x){return x.href})[0]; if(r && r.href) location.href = r.href; }
    else if(e.key==="Escape"){ dd.classList.remove("open"); input.setAttribute("aria-expanded","false"); input.blur(); }
  });
  document.addEventListener("click", function(e){ if(!input.parentElement.contains(e.target)){ dd.classList.remove("open"); input.setAttribute("aria-expanded","false"); } });
};
})();

/* Sensitivity bar: keep the bear/full/spot labels inside the card and clear of
   the bar. The shared renderer centres them on the bar's ends, which clips them
   at the card edge on the new study pages; nudge rather than fork the renderer. */
(function(){
  function fixLeverBar(){
    var host=document.getElementById("fl-lever-card");
    if(!host) return false;
    var bar=host.querySelector('div[style*="linear-gradient(90deg"]');
    if(!bar) return false;
    var wrap=bar.parentElement;
    wrap.style.margin="42px 6px 46px";
    var labels=[].slice.call(bar.children).filter(function(c){ return c.id!=="fl-marker"; });
    labels.forEach(function(c){
      c.style.lineHeight="1.25";
      c.style.whiteSpace="nowrap";
      var left=parseFloat(c.style.left);
      if(c.style.top.indexOf("-")===0){          /* the two end labels */
        c.style.top="-34px";
        if(left<=0){ c.style.transform="none"; c.style.textAlign="left"; }
        else if(left>=100){ c.style.transform="translateX(-100%)"; c.style.textAlign="right"; }
      } else {                                    /* the spot marker label */
        c.style.top="16px";
        if(left<8){ c.style.transform="none"; c.style.textAlign="left"; }
        else if(left>92){ c.style.transform="translateX(-100%)"; c.style.textAlign="right"; }
      }
    });
    return true;
  }
  var tries=0;
  var iv=setInterval(function(){ if(fixLeverBar()||++tries>40) clearInterval(iv); },100);
  document.addEventListener("DOMContentLoaded",fixLeverBar);
})();

/* Bucket range labels: the odds buckets were written with an ellipsis for "to"
   ("SMALL WIN 0…+10%"), which reads as truncated text rather than a range.
   Spell it out wherever those labels render — tools page and every study. */
(function(){
  function normaliseRangeLabels(){
    var n=0;
    [].slice.call(document.querySelectorAll(".t-bucket .lb")).forEach(function(e){
      if(e.textContent.indexOf("\u2026")>-1){
        e.textContent=e.textContent.replace(/\s*\u2026\s*/," to ");
        n++;
      }
    });
    return n;
  }
  var tries=0;
  var iv=setInterval(function(){ normaliseRangeLabels(); if(++tries>40) clearInterval(iv); },150);
  document.addEventListener("click",function(){ setTimeout(normaliseRangeLabels,60); });
  document.addEventListener("change",function(){ setTimeout(normaliseRangeLabels,60); });
})();

/* The study shell caps each prose paragraph inline at 78ch, which leaves a third
   of the card empty. Widen from JS as well as CSS so a cached stylesheet cannot
   leave the old look in place. */
(function(){
  function widenProse(){
    var h=document.getElementById("prose-body"); if(!h) return false;
    var ps=h.querySelectorAll("p"); if(!ps.length) return false;
    [].slice.call(ps).forEach(function(p){ p.style.maxWidth="none"; });
    return true;
  }
  var n=0, iv=setInterval(function(){ if(widenProse()||++n>60) clearInterval(iv); },100);
  document.addEventListener("DOMContentLoaded",widenProse);
})();
