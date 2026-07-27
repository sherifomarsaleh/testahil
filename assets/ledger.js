/* Testahil Verified Ledger — reads window.TESTAHIL_CALLS / TESTAHIL_TRUST (assets/data.js).
   CALLS is the source of truth: every stat tile, the table, and the equity curve are computed from it. */
(function(){
  var CALLS = window.TESTAHIL_CALLS;
  var TRUST = window.TESTAHIL_TRUST;
  var ICONS = window.TESTAHIL_ICONS;
  var STATUS_LABEL = window.TESTAHIL_STATUS_LABEL;

  var currentFilter = 'all';
  var sortKey = 'date';
  var sortDir = 'desc';

  function fmtSigned(n, digits){
    var s = n.toFixed(digits === undefined ? 1 : digits);
    return (n > 0 ? '+' : '') + s;
  }

  function renderStats(){
    var closed = CALLS.filter(function(c){ return c.status === 'hit' || c.status === 'stopped'; });
    var hits = closed.filter(function(c){ return c.status === 'hit'; });
    var winRate = closed.length ? (hits.length / closed.length * 100) : 0;
    var avgR = CALLS.length ? (CALLS.reduce(function(s,c){ return s + c.r; }, 0) / CALLS.length) : 0;

    document.getElementById('statCount').textContent = CALLS.length;
    document.getElementById('statCountDelta').textContent = '▲ ' + hits.length + ' wins logged';
    document.getElementById('statWinRate').textContent = winRate.toFixed(0) + '%';
    document.getElementById('statWinDelta').textContent = hits.length + ' of ' + closed.length + ' closed';
    document.getElementById('statAvgR').textContent = fmtSigned(avgR, 1) + 'R';
    document.getElementById('statAvgDelta').textContent = 'across all logged calls';
  }

  function trustCategory(acc){
    if (acc >= 80) return { key:'good', label:'High reliability', color:'var(--good)', textColor:'var(--success-text)', icon:ICONS.shield };
    if (acc >= 60) return { key:'warn', label:'Medium reliability', color:'var(--warning)', textColor:'#7a5300', icon:ICONS.triangle };
    return { key:'crit', label:'Low reliability', color:'var(--critical)', textColor:'var(--critical)', icon:ICONS.xcircle };
  }

  function tickerHref(sym){
    // works from both /ledger.html and /tickers/*.html
    var inTickers = /\/tickers\//.test(window.location.pathname);
    return (inTickers ? '' : 'tickers/') + sym + '.html';
  }

  function renderTrust(){
    var el = document.getElementById('trustList');
    el.innerHTML = TRUST.map(function(t){
      var cat = trustCategory(t.accuracy);
      return '<div class="trust-item">' +
        '<div class="trust-top"><div class="tt-left">' +
        '<a class="sym" href="' + tickerHref(t.ticker) + '">' + t.ticker + '</a>' +
        '<span style="color:' + cat.color + '">' + cat.icon + '</span>' +
        '<span class="status-label" style="color:' + cat.textColor + '">' + cat.label + '</span>' +
        '</div><span class="pct">' + t.accuracy + '%</span></div>' +
        '<div class="meter-track"><div class="meter-fill" style="width:' + t.accuracy + '%; background:' + cat.color + ';"></div></div>' +
        '</div>';
    }).join('');
  }

  function renderFilters(){
    var el = document.getElementById('filterChips');
    var options = [
      { key:'all', label:'All' },
      { key:'hit', label:'Hit target' },
      { key:'open', label:'Open' },
      { key:'stopped', label:'Stopped' }
    ];
    el.innerHTML = options.map(function(o){
      return '<button type="button" class="chip' + (currentFilter === o.key ? ' active' : '') + '" data-filter="' + o.key + '">' + o.label + '</button>';
    }).join('');
    Array.prototype.forEach.call(el.querySelectorAll('.chip'), function(btn){
      btn.addEventListener('click', function(){
        currentFilter = btn.getAttribute('data-filter');
        renderFilters();
        renderTable();
      });
    });
  }

  function renderTable(){
    var rows = CALLS.slice();
    if (currentFilter !== 'all') rows = rows.filter(function(c){ return c.status === currentFilter; });

    rows.sort(function(a, b){
      var va = a[sortKey], vb = b[sortKey];
      if (sortKey === 'date') { va = new Date(a.date).getTime(); vb = new Date(b.date).getTime(); }
      if (va < vb) return sortDir === 'asc' ? -1 : 1;
      if (va > vb) return sortDir === 'asc' ? 1 : -1;
      return 0;
    });

    var body = document.getElementById('ledgerBody');
    body.innerHTML = rows.map(function(c){
      var rColor = c.r > 0 ? 'var(--success-text)' : (c.r < 0 ? 'var(--critical)' : 'var(--text-primary)');
      return '<tr>' +
        '<td><a class="sym" href="' + tickerHref(c.ticker) + '" style="color:var(--text-primary)">' + c.ticker + '</a><div class="sub">' + c.date + ' · ' + c.entry.toFixed(2) + '</div></td>' +
        '<td><div class="sub">' + c.horizon + ' ' + fmtSigned(c.pct) + '%</div></td>' +
        '<td><span class="status-chip ' + c.status + '">' + ICONS[c.status] + STATUS_LABEL[c.status] + '</span></td>' +
        '<td class="num" style="color:' + rColor + '">' + fmtSigned(c.r) + 'R</td>' +
        '</tr>';
    }).join('');

    Array.prototype.forEach.call(document.querySelectorAll('thead th'), function(th){
      th.classList.toggle('sorted', th.getAttribute('data-key') === sortKey);
    });
  }

  function renderEquity(){
    var closed = CALLS.filter(function(c){ return c.status !== 'open'; }).slice()
      .sort(function(a,b){ return new Date(a.date) - new Date(b.date); });

    var cum = 0;
    var points = closed.map(function(c){
      cum += c.r;
      return { date:c.date, ticker:c.ticker, cum:cum };
    });
    if (!points.length) return;

    var maxCum = Math.max(1, Math.max.apply(null, points.map(function(p){ return p.cum; })));
    var minCum = Math.min(0, Math.min.apply(null, points.map(function(p){ return p.cum; })));
    var x0 = 14, x1 = 280, y0 = 86, y1 = 10;

    function xAt(i){ return points.length === 1 ? x1 : x0 + (i / (points.length - 1)) * (x1 - x0); }
    function yAt(v){ return y0 - ((v - minCum) / (maxCum - minCum || 1)) * (y0 - y1); }

    var linePath = points.map(function(p,i){ return (i === 0 ? 'M' : 'L') + xAt(i) + ',' + yAt(p.cum); }).join(' ');
    var areaPath = linePath + ' L' + xAt(points.length-1) + ',' + y0 + ' L' + x0 + ',' + y0 + ' Z';

    document.getElementById('equityLine').setAttribute('d', linePath);
    document.getElementById('equityArea').setAttribute('d', areaPath);
    document.getElementById('equityEnd').setAttribute('cx', xAt(points.length-1));
    document.getElementById('equityEnd').setAttribute('cy', yAt(points[points.length-1].cum));
    document.getElementById('equityMaxLabel').textContent = '+' + maxCum.toFixed(0) + 'R';
    document.getElementById('equityStartLabel').textContent = points[0].date.slice(0,7);
    document.getElementById('equityEndLabel').textContent = points[points.length-1].date.slice(0,7);

    var ptsG = document.getElementById('equityPoints');
    ptsG.innerHTML = points.map(function(p,i){
      return '<circle cx="' + xAt(i) + '" cy="' + yAt(p.cum) + '" r="7" fill="transparent" data-i="' + i + '"/>';
    }).join('');

    var tooltip = document.getElementById('tooltip');
    var svg = document.getElementById('equitySvg');
    Array.prototype.forEach.call(ptsG.querySelectorAll('circle'), function(c){
      c.addEventListener('mouseenter', function(){
        var i = parseInt(c.getAttribute('data-i'), 10);
        var p = points[i];
        var rect = svg.getBoundingClientRect();
        var px = (parseFloat(c.getAttribute('cx')) / 300) * rect.width;
        var py = (parseFloat(c.getAttribute('cy')) / 110) * rect.height;
        tooltip.style.left = px + 'px';
        tooltip.style.top = py + 'px';
        tooltip.style.opacity = '1';
        tooltip.textContent = p.date + ' · ' + p.ticker + ' · ' + fmtSigned(p.cum) + 'R cumulative';
      });
      c.addEventListener('mouseleave', function(){ tooltip.style.opacity = '0'; });
    });
  }

  window.initLedger = function(){
    Array.prototype.forEach.call(document.querySelectorAll('thead th'), function(th){
      th.addEventListener('click', function(){
        var key = th.getAttribute('data-key');
        if (sortKey === key) { sortDir = sortDir === 'asc' ? 'desc' : 'asc'; }
        else { sortKey = key; sortDir = key === 'ticker' ? 'asc' : 'desc'; }
        renderTable();
      });
    });
    renderStats();
    renderTrust();
    renderFilters();
    renderTable();
    renderEquity();
  };
})();
