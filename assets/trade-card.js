/* Testahil Trade Card — shared engine for every ticker page. Reads window.TESTAHIL_TICKERS (assets/data.js).
   Wiring for a dev: replace assets/data.js's TICKERS with your live MC output (current price, daily % change,
   and P10/P15/P30/median/P75/P90 30-day percentiles per ticker). Everything below recomputes from that object —
   chart geometry, entry/target/stop, R:R, the confidence pill, and the calculator. No page-level markup changes
   are needed to add a ticker: add a key to data.js and a page in /tickers/. */
(function(){
  var TICKERS = window.TESTAHIL_TICKERS;
  var currentSym = null;
  var navigateOnSwitch = false;

  function fmt2(n){ return n.toFixed(2); }
  function fmtMoney(n){ return Math.round(n).toLocaleString('en-US'); }

  function priceToY(price, lo, hi){
    var t = (price - lo) / (hi - lo);
    t = Math.max(-0.15, Math.min(1.15, t));
    return 130 - t * 110;
  }

  function render(){
    var t = TICKERS[currentSym];
    var entryMid = (t.p15 + t.p30) / 2;
    var stop = t.p10;
    var target = t.p75;
    var riskPerShare = entryMid - stop;
    var rewardPerShare = target - entryMid;
    var rr = riskPerShare > 0 ? (rewardPerShare / riskPerShare) : 0;

    document.title = currentSym + ' Trade Card — Testahil (concept preview)';
    document.getElementById('outSym').textContent = currentSym;
    document.getElementById('outName').textContent = t.name;
    document.getElementById('outPrice').textContent = 'EGP ' + fmt2(t.price);
    var deltaEl = document.getElementById('outDelta');
    var up = t.changePct >= 0;
    deltaEl.className = 'delta ' + (up ? 'up' : 'down');
    deltaEl.textContent = (up ? '▲ +' : '▼ ') + fmt2(Math.abs(t.changePct)) + '% today';

    document.getElementById('outEntry').textContent = fmt2(t.p15) + '–' + fmt2(t.p30);
    document.getElementById('outTarget').textContent = fmt2(target);
    document.getElementById('outStop').textContent = fmt2(stop);
    document.getElementById('outRR').textContent = '1 : ' + rr.toFixed(1);

    var rrPct = Math.max(6, Math.min(100, (rr / 4) * 100));
    document.getElementById('rrFill').style.width = rrPct + '%';
    document.getElementById('rrFill').style.background = rr >= 1.5 ? 'var(--good)' : (rr >= 1 ? 'var(--warning)' : 'var(--critical)');

    var pill = document.getElementById('confPill');
    var confText = document.getElementById('confText');
    if (t.prob >= 55) {
      pill.className = 'pill';
      confText.textContent = t.prob + '% of simulated paths hit target before stop';
    } else {
      pill.className = 'pill low';
      confText.textContent = 'Only ' + t.prob + '% of simulated paths hit target before stop — weak setup';
    }

    document.getElementById('outInvalidation').textContent =
      'Invalidated if ' + currentSym + ' closes below EGP ' + fmt2(stop) + ' for 2 consecutive sessions.';

    var lo = t.p10 * 0.97, hi = t.p90 * 1.03;
    var yNow = priceToY(t.price, lo, hi);
    var yMedian = priceToY(t.median, lo, hi);
    var yUpper = priceToY(t.p90, lo, hi);
    var yLower = priceToY(t.p10, lo, hi);
    var yTarget = priceToY(target, lo, hi);
    var yStop = priceToY(stop, lo, hi);
    var yEntryHi = priceToY(t.p30, lo, hi);
    var yEntryLo = priceToY(t.p15, lo, hi);

    document.getElementById('coneNow').setAttribute('cy', yNow);
    document.getElementById('coneMedian').setAttribute('d',
      'M20,' + yNow + ' C 90,' + (yNow + (yMedian - yNow) * 0.35) + ' 150,' + (yNow + (yMedian - yNow) * 0.75) +
      ' 200,' + (yNow + (yMedian - yNow) * 0.9) + ' C 230,' + yMedian + ' 260,' + yMedian + ' 282,' + yMedian);
    document.getElementById('coneBand').setAttribute('d',
      'M20,' + yNow + ' C 90,' + (yNow + (yUpper - yNow) * 0.3) + ' 150,' + (yNow + (yUpper - yNow) * 0.7) +
      ' 200,' + (yUpper + 8) + ' C 230,' + (yUpper - 4) + ' 260,' + (yUpper - 8) + ' 282,' + yUpper +
      ' L282,' + yLower +
      ' C260,' + (yLower + 8) + ' 230,' + (yLower + 4) + ' 200,' + (yLower - 8) +
      ' C150,' + (yNow + (yLower - yNow) * 0.7) + ' 90,' + (yNow + (yLower - yNow) * 0.3) + ' 20,' + yNow + ' Z');

    document.getElementById('targetLine').setAttribute('y1', yTarget);
    document.getElementById('targetLine').setAttribute('y2', yTarget);
    var targetLabel = document.getElementById('targetLabel');
    targetLabel.setAttribute('x', 284); targetLabel.setAttribute('y', yTarget - 4);
    targetLabel.textContent = 'Target ' + fmt2(target);

    document.getElementById('stopLine').setAttribute('y1', yStop);
    document.getElementById('stopLine').setAttribute('y2', yStop);
    var stopLabel = document.getElementById('stopLabel');
    stopLabel.setAttribute('x', 284); stopLabel.setAttribute('y', yStop + 12);
    stopLabel.textContent = 'Stop ' + fmt2(stop);

    var entryBand = document.getElementById('entryBand');
    entryBand.setAttribute('y', Math.min(yEntryHi, yEntryLo));
    entryBand.setAttribute('height', Math.abs(yEntryLo - yEntryHi) || 4);
    var entryLabel = document.getElementById('entryLabel');
    entryLabel.setAttribute('x', 20); entryLabel.setAttribute('y', Math.max(yEntryHi, yEntryLo) + 12);
    entryLabel.textContent = 'Entry ' + fmt2(t.p15) + '–' + fmt2(t.p30);

    // keep the ticker-nav chip row in sync
    Array.prototype.forEach.call(document.querySelectorAll('.ticker-nav a'), function(a){
      a.classList.toggle('active', a.getAttribute('data-sym') === currentSym);
    });
    var sel = document.getElementById('tickerSelect');
    if (sel) sel.value = currentSym;

    recalcPosition();
  }

  function recalcPosition(){
    var t = TICKERS[currentSym];
    var entryMid = (t.p15 + t.p30) / 2;
    var stop = t.p10;
    var riskPerShare = entryMid - stop;

    var portfolio = parseFloat(document.getElementById('portfolioInput').value) || 0;
    var riskPct = parseFloat(document.getElementById('riskInput').value) || 0;
    var riskAmount = portfolio * (riskPct / 100);
    var shares = riskPerShare > 0 ? Math.floor(riskAmount / riskPerShare) : 0;
    var positionValue = shares * entryMid;
    var positionPct = portfolio > 0 ? (positionValue / portfolio * 100) : 0;

    var out = document.getElementById('outPosition');
    var warn = document.getElementById('outWarn');
    if (portfolio <= 0 || riskPct <= 0) {
      out.textContent = 'Enter a portfolio size and risk % to size the trade.';
      warn.style.display = 'none';
    } else {
      out.textContent = 'EGP ' + fmtMoney(positionValue) + ' · ' + shares.toLocaleString('en-US') +
        ' shares (' + positionPct.toFixed(1) + '% of portfolio)';
      if (positionPct > 25) {
        warn.style.display = 'block';
        warn.textContent = 'That is a large single-name concentration — consider trimming size.';
      } else {
        warn.style.display = 'none';
      }
    }
  }

  function wireHover(){
    var svg = document.getElementById('coneChart');
    var tooltip = document.getElementById('tooltip');
    var catcher = document.getElementById('hoverCatcher');
    if (!catcher) return;
    catcher.addEventListener('mousemove', function(evt){
      var pt = svg.createSVGPoint();
      pt.x = evt.clientX; pt.y = evt.clientY;
      var loc = pt.matrixTransform(svg.getScreenCTM().inverse());
      var t = TICKERS[currentSym];
      var lo = t.p10 * 0.97, hi = t.p90 * 1.03;
      var dayFrac = Math.max(0, Math.min(1, (loc.x - 20) / (282 - 20)));
      var days = Math.round(dayFrac * 30);
      var yNow = priceToY(t.price, lo, hi);
      var yMedian = priceToY(t.median, lo, hi);
      var yAtX = yNow + (yMedian - yNow) * dayFrac;
      var priceAtX = hi - ((130 - yAtX) / 110) * (hi - lo);

      var rect = svg.getBoundingClientRect();
      var px = ((loc.x) / 300) * rect.width;
      var py = ((yAtX) / 150) * rect.height;
      tooltip.style.left = px + 'px';
      tooltip.style.top = py + 'px';
      tooltip.style.opacity = '1';
      tooltip.textContent = '+' + days + 'd · median ≈ EGP ' + fmt2(priceAtX);
    });
    catcher.addEventListener('mouseleave', function(){ tooltip.style.opacity = '0'; });
  }

  // initTradeCard(defaultSym, opts) — call once per page after the DOM is ready.
  // opts.navigate=true makes the <select> jump to that ticker's own page (used on multi-page site);
  // opts.navigate=false (default when omitted) re-renders in place without changing the URL.
  window.initTradeCard = function(defaultSym, opts){
    opts = opts || {};
    currentSym = defaultSym;
    navigateOnSwitch = !!opts.navigate;

    var sel = document.getElementById('tickerSelect');
    if (sel) {
      sel.innerHTML = window.TESTAHIL_TICKER_ORDER.map(function(sym){
        return '<option value="' + sym + '"' + (sym === defaultSym ? ' selected' : '') + '>' + sym + '</option>';
      }).join('');
      sel.addEventListener('change', function(e){
        if (navigateOnSwitch) {
          window.location.href = e.target.value + '.html';
        } else {
          currentSym = e.target.value;
          render();
        }
      });
    }
    document.getElementById('portfolioInput').addEventListener('input', recalcPosition);
    document.getElementById('riskInput').addEventListener('input', recalcPosition);
    wireHover();
    render();
  };
})();
