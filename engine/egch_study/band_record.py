"""The published band record for EGCH, read from assets/data.js — the ONE calibration figure a
reader is shown [R-CAL-02]. Parsed through node so the object the page renders is the object
read (a regex over the file would model the parser, [R-ENF-03]); the count is written beside the
percentages and no verdict vocabulary is carried."""
import json, os, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
JS = ("const fs=require('fs');const vm=require('vm');const src=fs.readFileSync(%r,'utf8');"
      "const ctx=vm.createContext({});vm.runInContext(src+';globalThis.__B=BANDS;',ctx);"
      "const b=ctx.__B.EGCH;if(!b)throw new Error('no BANDS.EGCH');"
      "console.log(JSON.stringify({n:b.n,hits:b.hits,c50:b.c50,c80:b.c80,c90:b.c90,strength:b.strength,flag:b.flag}));"
      % os.path.join(ROOT, 'assets', 'data.js'))
out = subprocess.run(['node', '-e', JS], capture_output=True, text=True, check=True).stdout
rec = json.loads(out)
assert rec['n'] > 0 and 0 < rec['c90'] <= 1
json.dump(rec, open(os.path.join(HERE, 'band_record.json'), 'w'), indent=1)
print("band record: n=%d c50=%.4f c80=%.4f c90=%.4f flag=%s" % (rec['n'], rec['c50'], rec['c80'], rec['c90'], rec['flag']))
