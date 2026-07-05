const fs = require('fs'), vm = require('vm');
const page = process.argv[2];
const html = fs.readFileSync(page, 'utf8');
// slider defaults
const sliders = {};
for (const m of html.matchAll(/<input type="range" id="([^"]+)" min="([^"]+)" max="([^"]+)" step="[^"]*" value="([^"]+)"/g))
  sliders[m[1]] = { min: m[2], max: m[3], value: m[4] };
// mc-lab inline script
const li = html.indexOf('id="mc-lab"');
const s1 = html.indexOf('<script>', li), s2 = html.indexOf('</script>', s1);
const script = html.slice(s1 + 8, s2);
const data = fs.readFileSync('assets/data.js', 'utf8');

const store = {};
function mk(id) {
  if (store[id]) return store[id];
  const o = { id, _tc:'', _ih:'',
    style: { setProperty(){} }, classList: { toggle(){} },
    setAttribute(){}, addEventListener(){}, appendChild(){},
    get textContent(){ return this._tc }, set textContent(v){ this._tc = String(v) },
    get innerHTML(){ return this._ih }, set innerHTML(v){ this._ih = String(v) },
    value: (sliders[id] || {}).value || "0",
    min: (sliders[id] || {}).min || "0",
    max: (sliders[id] || {}).max || "1" };
  store[id] = o; return o;
}
const sandbox = {
  console, Math, JSON, parseFloat, parseInt, isFinite, Infinity, NaN,
  requestAnimationFrame: () => 0,
  document: { readyState: 'complete', getElementById: mk, addEventListener(){},
    createElement: () => ({ style:{}, set textContent(v){}, appendChild(){} }) },
  window: {}
};
sandbox.globalThis = sandbox;
vm.createContext(sandbox);
try {
  vm.runInContext(data + '\n' + script, sandbox, { timeout: 10000 });
  const r = sandbox.window.__probRead;
  if (!r) { console.log(JSON.stringify({ page, error: 'no __probRead' })); process.exit(1); }
  r.page = page; console.log(JSON.stringify(r));
} catch (e) { console.log(JSON.stringify({ page, error: String(e).slice(0,120) })); process.exit(1); }
