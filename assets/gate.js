/* TESTAHIL invite gate — 14-09-2026.
 *
 * The site is by invitation. A visitor arrives with the key in the URL
 * (https://testahil.com/?k=KEY); the key is verified against the SHA-256
 * below, remembered in this browser, and stripped out of the address bar so
 * the key is not left sitting in a screenshot or a shared tab title.
 *
 * WHAT THIS IS AND IS NOT. It is an access gate for the site's audience, not
 * a secret-keeper: the repository is public, so the pages themselves can be
 * read by anyone who goes looking for them on GitHub. Treat it as the velvet
 * rope it is. If the content itself must be unreadable without the key, the
 * repository has to go private and the hosting has to move to something that
 * can check the key on the server — say so and it gets done.
 *
 * The key's plaintext is deliberately NOT in this file.
 */
(function () {
  var HASH  = "f8cb1f9f885415a8a684697a59ae8a58f6daeef1bc0207503186ae494ad955cf";
  var STORE = "th_invite";
  var root  = document.documentElement;

  /* Hide synchronously, at parse time, so gated content never flashes.
     If JavaScript is off this line never runs and the page simply shows —
     an accepted limit of a client-side rope. */
  root.style.visibility = "hidden";

  function reveal() { root.style.visibility = ""; }

  function sha256Hex(s) {
    var bytes = new TextEncoder().encode(s);
    return crypto.subtle.digest("SHA-256", bytes).then(function (buf) {
      return Array.prototype.map
        .call(new Uint8Array(buf), function (b) { return b.toString(16).padStart(2, "0"); })
        .join("");
    });
  }

  function keyFromUrl() {
    try {
      var u = new URL(location.href);
      var k = u.searchParams.get("k");
      if (k) return k;
      var m = /[#&]k=([^&]+)/.exec(location.hash || "");
      return m ? decodeURIComponent(m[1]) : null;
    } catch (e) { return null; }
  }

  function stripKey() {
    try {
      var u = new URL(location.href);
      var touched = false;
      if (u.searchParams.has("k")) { u.searchParams.delete("k"); touched = true; }
      var hash = (u.hash || "").replace(/([#&])k=[^&]*/, "$1").replace(/[#&]$/, "");
      if (hash !== (u.hash || "")) { u.hash = hash; touched = true; }
      if (touched) {
        history.replaceState(null, "", u.pathname + (u.search || "") + (u.hash || ""));
      }
    } catch (e) {}
  }

  var DENY_HTML =
    '<div id="th-gate">' +
    '<div class="th-card">' +
    '<div class="th-mark">TESTAHIL</div>' +
    '<h1>By invitation</h1>' +
    '<p>This research is not published openly. Enter the access key you were sent, ' +
    'or ask for one.</p>' +
    '<form id="th-form" autocomplete="off">' +
    '<input id="th-key" type="text" placeholder="Access key" spellcheck="false" ' +
    'autocapitalize="characters" aria-label="Access key">' +
    '<button type="submit">Enter</button>' +
    '</form>' +
    '<p class="th-err" id="th-err" hidden>That key is not recognised.</p>' +
    '<p class="th-foot"><a href="mailto:sherifomarsaleh@gmail.com?subject=TESTAHIL%20access">' +
    'Request access</a></p>' +
    '</div></div>';

  var DENY_CSS =
    '#th-gate{position:fixed;inset:0;z-index:2147483647;display:flex;align-items:center;' +
    'justify-content:center;padding:24px;background:#0d1117;color:#e6edf3;' +
    'font:15px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}' +
    '#th-gate .th-card{width:100%;max-width:380px;text-align:center}' +
    '#th-gate .th-mark{letter-spacing:.34em;font-size:12px;color:#7d8590;margin-bottom:28px}' +
    '#th-gate h1{font-size:26px;font-weight:600;margin:0 0 12px}' +
    '#th-gate p{color:#9aa4ae;margin:0 0 22px}' +
    '#th-gate form{display:flex;gap:8px;flex-wrap:wrap;justify-content:center}' +
    '#th-gate input{flex:1 1 200px;min-width:0;padding:11px 13px;border-radius:8px;' +
    'border:1px solid #30363d;background:#161b22;color:#e6edf3;font-size:15px}' +
    '#th-gate input:focus{outline:none;border-color:#58a6ff}' +
    '#th-gate button{padding:11px 20px;border-radius:8px;border:0;background:#e6edf3;' +
    'color:#0d1117;font-size:15px;font-weight:600;cursor:pointer}' +
    '#th-gate .th-err{color:#ff7b72;margin:14px 0 0}' +
    '#th-gate .th-foot{margin:26px 0 0;font-size:13px}' +
    '#th-gate .th-foot a{color:#7d8590}';

  function deny() {
    function paint() {
      try { document.title = "TESTAHIL — by invitation"; } catch (e) {}
      var style = document.createElement("style");
      style.textContent = DENY_CSS;
      document.head.appendChild(style);
      document.body.innerHTML = DENY_HTML;
      reveal();
      var form = document.getElementById("th-form");
      var field = document.getElementById("th-key");
      var err = document.getElementById("th-err");
      field.focus();
      form.addEventListener("submit", function (ev) {
        ev.preventDefault();
        var typed = (field.value || "").trim();
        if (!typed) return;
        sha256Hex(typed).then(function (h) {
          if (h === HASH) {
            try { localStorage.setItem(STORE, h); } catch (e) {}
            location.reload();
          } else {
            err.hidden = false;
            field.select();
          }
        }).catch(function () { err.hidden = false; });
      });
    }
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", paint);
    } else {
      paint();
    }
  }

  try {
    if (localStorage.getItem(STORE) === HASH) { reveal(); return; }
  } catch (e) {}

  var fromUrl = keyFromUrl();
  if (!fromUrl) { deny(); return; }

  sha256Hex(fromUrl).then(function (h) {
    if (h === HASH) {
      try { localStorage.setItem(STORE, h); } catch (e) {}
      stripKey();
      reveal();
    } else {
      deny();
    }
  }).catch(function () { deny(); });
})();
