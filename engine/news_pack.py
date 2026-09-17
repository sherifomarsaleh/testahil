"""THE EXTERNAL-NEWS HAND-OVER PACK, BUILT FROM WHAT EACH STUDY ACTUALLY HOLDS.

Runbook step 3 stops: the session builds the search prompt and hands it over. At one name
that is a paragraph; at eight it is a pack, and the reason to batch is throughput -- a
wave's speed is set by how fast the packs come back, not by the modelling.

WHAT THE RUNBOOK REQUIRES EACH PROMPT TO CARRY, and how each is answered here:
  - the registered name in English AND in the local language;
  - the driver headings THE STUDY'S OWN driver list turns on, never a generic template;
  - the study's OWN DATED NEGATIVE SEARCHES, so the outside pass is told what has already
    been looked for and not found rather than rediscovering the same absences;
  - the period the information set already covers, so anything earlier is known consumed.

EVERY ONE OF THOSE IS READ, AND WHERE IT CANNOT BE READ THE PACK SAYS SO IN THE PROMPT
ITSELF. That is not politeness: a prompt claiming to carry a study's negative searches when
the study registers none would send a searcher looking for absences nobody established, and
the returns would come back looking like confirmation. Measured 17-09-2026 across the eight
names of this wave: four commit a sweep register (ARCC, EGCH, PHAR, SCEM) and four commit
none (AMOC, ELEC, SWDY, TMGH) -- which check_sweep_module already ratchets, and which the
pack states per name rather than averaging away.

THE ARABIC NAME IS NOT HELD ANYWHERE IN THIS REPOSITORY and is NOT invented here. A
transliteration this desk guessed could send a search at a different company, and a company
name is exactly the kind of fact a wrong guess makes invisible -- the search comes back
empty and reads like an absence. It is listed as the first thing to resolve, per name.

    python3 engine/news_pack.py                      the whole current wave
    python3 engine/news_pack.py --tickers AMOC,ARCC  an explicit list
    python3 engine/news_pack.py --out FILE
"""

import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENGINE = os.path.join(ROOT, 'engine')
DATA_JS = os.path.join(ROOT, 'assets', 'data.js')
if ENGINE not in sys.path:
    sys.path.insert(0, ENGINE)

NODE = r'''
const fs=require("fs"),vm=require("vm");const c={};vm.createContext(c);
vm.runInContext(fs.readFileSync(process.argv[1],"utf8")+";this.__T=TICKERS;",c);
console.log(JSON.stringify(c.__T));
'''


def site():
    p = subprocess.run(['node', '-e', NODE, DATA_JS], capture_output=True, text=True)
    if p.returncode != 0:
        raise SystemExit('FATAL: node could not load %s\n%s' % (DATA_JS, p.stderr.strip()))
    return json.loads(p.stdout)


def _read(tk, name):
    p = os.path.join(ENGINE, '%s_study' % tk.lower(), name)
    if not os.path.exists(p):
        return None
    try:
        return json.load(open(p, encoding='utf-8'))
    except Exception:
        return 'UNREADABLE'


def wave_tickers():
    """The names of the wave the board says is being worked."""
    import recalibration_run as R
    rows, _, _ = R.board()
    todo = [r for r in rows if r['state'] in (R.DESK, R.UNREADABLE)]
    if not todo:
        raise SystemExit('No name is the desk\'s move; there is no pack to build.')
    first = min((r['market'], r['wave']) for r in
                [(x) for x in todo] and [(r['market'], r['wave']) for r in todo])
    mk, wv = first
    return [r['ticker'] for r in rows
            if r['market'] == mk and r['wave'] == wv and r['state'] in (R.DESK, R.UNREADABLE)]


def block(tk, T):
    row = T.get(tk) or {}
    sw = _read(tk, 'sweep_register.json')
    nums = _read(tk, 'study_numbers.json')
    out = []
    out.append('## %s — %s' % (tk, row.get('name') or '(no name on the site register)'))
    out.append('')
    out.append('- **Exchange code:** `%s`' % (row.get('code') or 'unknown'))
    # ARABIC SEARCH TERMS THE STUDY HAS ALREADY USED, where its own register carries
    # any. They are a FACT about what was searched, not a company name, and they are
    # labelled as what they are: one study's negative searches quote 'كيما' because its
    # searcher used it, and that is worth handing on. A registered name is still not
    # invented from a fragment.
    ar = sorted({m.strip() for m in re.findall(
        r'[\u0600-\u06FF][\u0600-\u06FF \u064B-\u0652]{2,40}',
        json.dumps(sw, ensure_ascii=False))}) if isinstance(sw, dict) else []
    out.append('- **Registered Arabic name:** NOT HELD IN THIS REPOSITORY — resolve it '
               'first, from the company\'s own filings or the exchange\'s listing page, '
               'and search under it as well as under the English name. Half the record '
               'that matters on this exchange is not written in English.')
    if ar:
        out.append('    - Arabic search terms THIS STUDY HAS ALREADY USED, quoted from its '
                   'own register (they are search strings, not the registered name): %s'
                   % '; '.join('`%s`' % a for a in ar))

    anchor = (nums or {}).get('forecast_anchor') if isinstance(nums, dict) else None
    if isinstance(anchor, dict) and anchor.get('latest_reviewed_period'):
        out.append('- **The information set already covers** everything up to and '
                   'including %s (%s). Anything earlier is already consumed; what is '
                   'wanted is what came after.'
                   % (anchor['latest_reviewed_period'], anchor.get('latest_reviewed_date')))
    else:
        out.append('- **The information set\'s end is NOT committed by this study** — it '
                   'declares no latest-reviewed period, so nothing here tells you where '
                   'the already-consumed record stops. Treat the whole of 2026 as open '
                   'and say in the return what period each finding belongs to.')

    if sw == 'UNREADABLE':
        out.append('- **Sweep register:** present and WILL NOT PARSE. Nothing about what '
                   'has already been searched can be read for this name.')
    elif sw is None:
        out.append('- **Sweep register: NONE.** This study registers no dated searches at '
                   'all, so NOTHING is known to have been looked for and not found. '
                   'Nothing below tells you where not to look, and an empty result from '
                   'you is a first search rather than a second one.')
    else:
        negs = [f for f in sw.get('findings', [])
                if str(f.get('klass', '')).upper().startswith('NEGATIVE')]
        out.append('- **Sweep register:** %d findings, swept %s.'
                   % (len(sw.get('findings', [])), sw.get('sweep_date')))
        if negs:
            out.append('- **ALREADY SEARCHED AND NOT FOUND** — do not spend the pass '
                       'rediscovering these; if you DO find one, that is the most '
                       'valuable thing in the return:')
            for n in negs:
                out.append('    - *%s* — searched %s, in %s'
                           % (n.get('headline', '(no headline)'), n.get('source_date'),
                              n.get('source_name', 'unnamed source')))
        else:
            out.append('- **No dated negative search is registered**, so this study '
                       'records nothing as having been looked for and not found.')

    drivers = (sw or {}).get('drivers') if isinstance(sw, dict) else None
    out.append('')
    if drivers:
        out.append('**What this company\'s value actually turns on — its own driver list, '
                   'not a template. Look for anything that moves one of these:**')
        out.append('')
        for d in drivers:
            out.append('- **%s** (%s)' % (d.get('driver'), d.get('mode')))
    else:
        out.append('**No committed driver list.** This study registers no drivers through '
                   'the shared register, so the headings below cannot be given. Search the '
                   'ordinary operating record — volumes, prices, capacity, input costs, '
                   'debt and any corporate action — and let the study map the returns.')
    out.append('')
    return '\n'.join(out)


def build(tickers):
    T = site()
    missing = [t for t in tickers if t not in T]
    if missing:
        raise SystemExit('FATAL: %s not on the site register. A pack naming a company the '
                         'book does not carry is a search pointed at nothing.'
                         % ', '.join(missing))
    head = """# EXTERNAL NEWS RESEARCH — hand-over pack

**%d names, handed over together.** Runbook step 3: the session builds these and STOPS.
Run each on Perplexity AND on Claude, keep the two returns APART, and bring both back.

**THREE RULES THAT DECIDE WHETHER A RETURN CAN BE USED AT ALL.**

1. **What comes back is a LEAD and never an input.** Every claim is traced to the PRIMARY
   source and read there before it moves anything in a model. Historicals come from the
   company's own issued statements alone — never a vendor, a broker, or the press as a
   source of numbers.
2. **Keep the two returns apart.** Where they agree on something neither can source, that
   is two models agreeing, which is not evidence.
3. **An untraceable claim is not discarded, it is written back as a DATED NEGATIVE
   SEARCH.** A negative search is one somebody actually ran; inventing one to clear a
   coverage check is worse than the gap it clears.

**WHAT TO LOOK FOR, IN ONE SENTENCE:** what the filings do not carry — corporate actions,
capacity and plant news, contract awards and losses, regulatory and tariff decisions,
input-cost and currency events, management changes, litigation, and anything a competitor
or the regulator said about this company — dated, and attributed to a named source.

**WHAT NOT TO BRING BACK:** a price target, a broker's estimate, an aggregator's restated
financials, or any number presented as the company's own results that did not come from
the company's own filing.

---

""" % len(tickers)
    return head + '\n---\n\n'.join(block(t, T) for t in tickers)


def main(argv):
    if '--tickers' in argv:
        tickers = [t.strip().upper() for t in
                   argv[argv.index('--tickers') + 1].split(',') if t.strip()]
    else:
        tickers = wave_tickers()
    text = build(tickers)
    out = argv[argv.index('--out') + 1] if '--out' in argv else None
    if out:
        open(out, 'w', encoding='utf-8').write(text)
        print('wrote %s — %d name(s): %s' % (out, len(tickers), ', '.join(tickers)))
    else:
        print(text)
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
