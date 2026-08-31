# -*- coding: utf-8 -*-
"""Render the protocol review — are the two governing documents self-enforcing?"""
import os, json
HERE = os.path.dirname(os.path.abspath(__file__))

FIND = [
 ("The hole the protocol already diagnosed is still open in eight places",
  "critical",
  """The protocol says this about itself, in the beta section: <em>&ldquo;<code>SIGCMChecklist.beta_own_history_vs_egx30</code>
  is a flag a study sets itself, and every study set it <code>True</code> while regressing on a
  composite. A self-attestation cannot catch that.&rdquo;</em> That diagnosis is exactly right, and it was
  acted on &mdash; <code>assert_beta_provenance()</code> now inspects the actual beta record instead of
  trusting the flag.<br><br>But <code>SIGCMChecklist</code> has nine clauses and <strong>only that one
  was fixed.</strong> The other eight are still plain booleans the study sets on itself, including
  <code>forecast_ground_up</code> &mdash; the ground-up construction rule. The build-depth audit found
  63 of 90 studies are not built ground-up. The same hole, one clause over, and nothing has been
  looking through it."""),

 ("No rule anywhere requires a study to run the checks",
  "critical",
  """Searched both governing documents for any requirement that a study call
  <code>assert_sigcm()</code>, <code>assert_beta_provenance()</code> or
  <code>assert_model_study()</code>. There is none. The QC gate says a violation is a hard fail, but
  nothing says the study must look. 13 of the 21 study directories accordingly call nothing, and
  until today no automated job ran any of them. A study passed by not checking itself."""),

 ("The beta record has no required shape, so the gate can only inspect what happens to be there",
  "high",
  """Across the 21 study directories the regressor is recorded four different ways: a full
  <code>raw_indices/</code> path, a bare filename, a prose name with no file at all, and nothing.
  <code>assert_beta_provenance()</code> is only as strong as the record it reads, so the weakest
  shape silently defeats it. Three studies this audit first read as clean fail the stricter test
  for exactly this reason."""),

 ("&ldquo;Never hand-roll a study-local beta script&rdquo; is prose with nothing behind it",
  "high",
  """The rule is unambiguous and it postdates the composite correction. Two studies written after it
  still carry a <code>beta_reg.py</code> that runs its own <code>np.linalg.lstsq</code> regression
  rather than calling <code>beta_regression.own_stock_beta()</code>, and one of them still builds a
  composite alongside it as a &ldquo;corroboration&rdquo;. Nothing was watching."""),

 ("There is no version on the standard, so no study can say what it was built to",
  "high",
  """Nothing in either document stamps a study with the standard it was written against. That is why
  the question &ldquo;is this study finished or provisionally finished?&rdquo; has no answer in the
  repository, and why a name re-issued in September could need re-issuing again in November. A
  <code>standard_version</code> in every study record, and a stated current version in the protocol,
  turns the rebuild queue from an open-ended obligation into a finite one."""),

 ("The index registry is not canonical, so a duplicate could sit in it unnoticed",
  "medium",
  """<code>ADXGENERAL.csv</code> and <code>FADGI.csv</code> are the same series under two names; only
  one is registered. Two studies regressed against the unregistered copy, which means the right
  number with provenance that cannot resolve. No rule says a file under <code>raw_indices/</code>
  must be either registered or removed, so nothing objected."""),

 ("The two governing documents are kept in sync by hand, and the project memory says that fails",
  "medium",
  """<code>CLAUDE.md</code> records that the digest &ldquo;has gone stale three times already this
  session from exactly this drift.&rdquo; The remedy currently in place is a written instruction to
  remember. Nothing checks it. Giving every standing rule a stable identifier and checking that both
  files carry the same set of identifiers would make the drift impossible to ship rather than
  merely discouraged."""),
]

PROPOSE = [
 ("A meta-rule, so the next gap closes itself",
  """<strong>Adopt one general rule rather than another specific one:</strong> <em>a standing rule that
  can be checked must be checked by something outside the thing it governs, and a self-attested
  boolean is never a check.</em> Every failure in this repository&rsquo;s history is an instance of
  this &mdash; the composite beta, the technical read that went stale behind a rule protecting it, the
  digest drift, and now the eight unchecked SIGCM clauses. The protocol has learned the lesson three
  times in particular and never once in general."""),

 ("Turn <code>forecast_ground_up</code> into a record, exactly as beta was",
  """Require a <code>driver_record.json</code> naming, for every revenue line: the physical unit, the
  disclosed source it came from, the price or rate, and the cost-per-unit basis &mdash; or an explicit
  flagged gap with its reason where the disclosure genuinely stops. Then
  <code>assert_ground_up()</code> inspects the record. The studies already write all of this in prose
  in section 1.6; this only asks them to write it once more in a form a machine can refuse. Repeat
  for the other seven clauses in the order they matter."""),

 ("Write the rule that makes the gates compulsory",
  """Add to both documents: <em>every study must call <code>assert_sigcm()</code>,
  <code>assert_beta_provenance()</code> and <code>assert_model_study()</code> in its own committed
  code, and a repository-level job verifies that it did.</em> The job now exists
  (<code>scripts/check_study_provenance.py</code>, in CI as a ratchet); the rule needs to say so, or
  the next study will not know it applies."""),

 ("Specify the beta record&rsquo;s schema and reject anything else",
  """Mandate the fields <code>assert_beta_provenance()</code> needs &mdash; regressor file as a
  <code>raw_indices/</code> path, index as-of date, n, R², standard error, the usability verdict, the
  tier landed on, and the interim note where one applies. A record missing a field fails, rather than
  passing on the strength of what it happens to contain."""),

 ("Stamp the standard version on every study",
  """Declare a current standard version in the protocol; require each study to record the version it
  was built to; have the gate report any study built to an older one. This is what lets you answer
  &ldquo;the technique is better now&rdquo; with a list instead of a feeling, and it is what makes a
  re-issued study finished rather than finished-for-now."""),

 ("Make the index directory self-policing",
  """One index, one filename, registered. A <code>.csv</code> under <code>raw_indices/</code> that is
  not in <code>EXCHANGE_INDEX</code> must be either registered or deleted &mdash; with the single
  documented exception now in place for the Dubai series, which is held deliberately and says so."""),

 ("Give every standing rule an identifier, and check both files carry it",
  """Tag each rule (<code>[R-BETA-01]</code>, <code>[R-SIGCM-02]</code> and so on) in both documents,
  cite the tag from the code that enforces it and from the QC gate that reports it, and add a check
  that the two files hold the same set of tags. It makes the hand-sync verifiable, lets a QC gate cite
  the rule it is testing, and gives an amendment one obvious place to land."""),
]

def esc(s): return s

sev = {'critical':('var(--crit)','var(--crit-s)','Critical'),
       'high':('var(--high)','var(--high-s)','High'),
       'medium':('var(--med)','var(--med-s)','Medium')}

finds = ''.join(
  f'<div class="f"><div class="fh"><span class="sev" style="color:{sev[s][0]};background:{sev[s][1]}">{sev[s][2]}</span>'
  f'<h3>{t}</h3></div><p>{b}</p></div>' for t, s, b in FIND)

props = ''.join(
  f'<div class="pr"><h3>{t}</h3><p>{b}</p></div>' for t, b in PROPOSE)

HTML = f"""<title>Does the Protocol Hold?</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,600;1,6..72,400&family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600&display=swap">
<style>
:root{{
  --ground:#F2F4F7; --surface:#FFFFFF; --sunk:#E8EBF0;
  --ink:#141C26; --ink2:#3D4855; --muted:#697687; --line:#D8DDE5; --line2:#EBEEF3;
  --a:#0E6B5E; --a2:#12897A;
  --crit:#8C2F2A; --crit-s:#F5E2E0; --high:#9A5A2B; --high-s:#F3E6D9;
  --med:#7A6A33; --med-s:#F0EBD8;
  --shadow:0 1px 2px rgba(20,28,38,.05),0 8px 24px -14px rgba(20,28,38,.18);
}}
@media (prefers-color-scheme:dark){{ :root:not([data-theme="light"]){{
  --ground:#0F141A; --surface:#161D25; --sunk:#1E262F;
  --ink:#E9EDF2; --ink2:#C2CAD4; --muted:#8D99A8; --line:#2A343F; --line2:#212A34;
  --a:#5CC9B4; --a2:#7FD8C6;
  --crit:#E39490; --crit-s:#3A1F1E; --high:#D9A16A; --high-s:#38271A;
  --med:#CBBE7E; --med-s:#302C1A;
  --shadow:0 1px 2px rgba(0,0,0,.4),0 8px 28px -16px rgba(0,0,0,.7);
}} }}
:root[data-theme="dark"]{{
  --ground:#0F141A; --surface:#161D25; --sunk:#1E262F;
  --ink:#E9EDF2; --ink2:#C2CAD4; --muted:#8D99A8; --line:#2A343F; --line2:#212A34;
  --a:#5CC9B4; --a2:#7FD8C6;
  --crit:#E39490; --crit-s:#3A1F1E; --high:#D9A16A; --high-s:#38271A;
  --med:#CBBE7E; --med-s:#302C1A;
  --shadow:0 1px 2px rgba(0,0,0,.4),0 8px 28px -16px rgba(0,0,0,.7);
}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--ground);color:var(--ink);
  font-family:"IBM Plex Sans",ui-sans-serif,system-ui,sans-serif;font-size:15.5px;line-height:1.62;
  -webkit-font-smoothing:antialiased}}
.wrap{{max-width:820px;margin:0 auto;padding:clamp(22px,4vw,54px) clamp(15px,3vw,30px) 80px}}
h1,h2{{font-family:Newsreader,ui-serif,Georgia,serif;font-weight:600;text-wrap:balance;margin:0}}
h1{{font-size:clamp(31px,5vw,50px);line-height:1.05;letter-spacing:-.015em}}
h2{{font-size:clamp(21px,2.6vw,28px);letter-spacing:-.01em}}
h3{{font-family:"IBM Plex Sans",sans-serif;font-size:15.5px;font-weight:600;margin:0;line-height:1.35}}
p{{margin:0}}
.eyebrow{{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:11px;letter-spacing:.15em;
  text-transform:uppercase;color:var(--muted)}}
header{{display:flex;flex-direction:column;gap:15px;padding-bottom:26px;border-bottom:1px solid var(--line)}}
.lede{{font-size:18px;color:var(--ink2);max-width:63ch}}
.verdict{{background:var(--surface);border:1px solid var(--line);border-left:3px solid var(--a);
  border-radius:3px;padding:22px 24px;margin-top:28px;box-shadow:var(--shadow);
  display:flex;flex-direction:column;gap:12px}}
.verdict p{{color:var(--ink2);max-width:64ch}}
.verdict strong{{color:var(--ink)}}
.sec{{margin-top:50px;display:flex;flex-direction:column;gap:14px}}
.sec>p{{max-width:66ch;color:var(--ink2)}}
.f{{background:var(--surface);border:1px solid var(--line2);border-radius:3px;padding:17px 19px;
  display:flex;flex-direction:column;gap:9px}}
.fh{{display:flex;align-items:baseline;gap:11px;flex-wrap:wrap}}
.sev{{font-family:"IBM Plex Mono",monospace;font-size:10px;letter-spacing:.11em;text-transform:uppercase;
  padding:3px 8px;border-radius:3px;font-weight:600;white-space:nowrap}}
.f h3{{flex:1 1 320px}}
.f p{{color:var(--ink2);font-size:14.5px;max-width:70ch}}
.pr{{background:var(--surface);border:1px solid var(--line2);border-left:3px solid var(--a);
  border-radius:3px;padding:16px 19px;display:flex;flex-direction:column;gap:7px}}
.pr h3{{color:var(--a)}}
.pr p{{color:var(--ink2);font-size:14.5px;max-width:70ch}}
.grid{{display:grid;gap:12px}}
.good{{background:var(--sunk);border-radius:3px;padding:17px 19px;display:flex;
  flex-direction:column;gap:8px;margin-top:8px}}
.good p{{color:var(--ink2);font-size:14.5px;max-width:68ch}}
code{{font-family:"IBM Plex Mono",monospace;font-size:.87em;background:var(--sunk);
  padding:1px 5px;border-radius:3px}}
.pr code,.f code{{background:rgba(127,127,127,.14)}}
footer{{margin-top:54px;padding-top:20px;border-top:1px solid var(--line);font-size:12.5px;
  color:var(--muted);max-width:74ch}}
@media (prefers-reduced-motion:reduce){{*{{transition:none!important;animation:none!important}}}}
</style>

<div class="wrap">
<header>
  <p class="eyebrow">TESTAHIL &middot; 23 Aug 2026 &middot; review of the governing documents</p>
  <h1>Are the rules enough to stop this happening again?</h1>
  <p class="lede">A read of <code>Standing_Research_Protocol.md</code> and
  the condensed digest against the failures they were written to prevent
  &mdash; and against what the repository actually does today.</p>
</header>

<div class="verdict">
  <p class="eyebrow">the answer</p>
  <p><strong>Clear: yes. Preventive: no &mdash; not yet.</strong> As written rules these two documents
  are better than anything I would suggest replacing them with. Every rule carries the failure that
  produced it, which is rare and worth protecting. Nothing important is missing from the <em>text</em>.</p>
  <p><strong>What they lack is teeth.</strong> They are addressed to a careful reader, and every
  failure in this repository&rsquo;s history happened to a careful reader &mdash; not to someone who
  disagreed with a rule, but to someone who never met it at the moment it bound. The composite beta
  spread through the entire book <em>while the rule against it was already written down</em>. That is
  the whole problem in one sentence, and it is still true of eight of the nine SIGCM clauses today.</p>
</div>

<section class="sec">
  <h2>What is actually wrong</h2>
  <p>Seven findings, each checked against the repository rather than inferred from the text.</p>
  <div class="grid">{finds}</div>
</section>

<section class="sec">
  <h2>What I would change</h2>
  <p>Seven amendments, in the order I would make them. The first is the only one that matters in the
  long run; the rest are instances of it.</p>
  <div class="grid">{props}</div>
</section>

<section class="sec">
  <h2>What not to change</h2>
  <div class="good">
    <p><strong>The reasons.</strong> Almost every rule in the protocol names the failure it came from
    &mdash; FERTIGLB&rsquo;s inverted valuation, COMI&rsquo;s spot of 142 beside a narrative reading
    129.25, <code>nu=Gaussian</code> parsing cleanly and dying at import. That is why the rules are
    obeyed when they are met at all, and it is the single most unusual thing about this repository.
    Every amendment above should arrive with its own reason attached, in the same voice.</p>
    <p><strong>The dual-framing discipline, and stop-and-inform.</strong> Both are rules about honesty
    rather than method, and both are working: the studies that fall short of the standard say so, in
    the delivered document, in plain language. The audit found the non-conforming studies mostly by
    reading their own confessions.</p>
  </div>
</section>

<footer>
  Findings verified against <code>engine/research_protocol.py</code>,
  <code>engine/wacc_builder.py</code>, the 21 study directories, <code>.github/workflows/</code> and
  both governing documents, on 23 Aug 2026. The claim that no rule requires a study to call the gates,
  the claim that no standard-version stamp exists, and the claim that nothing checks the two documents
  against each other were each established by search, not assumed.
</footer>
</div>
"""
p = os.path.join(HERE, 'protocol_review.html')
open(p, 'w', encoding='utf-8').write(HTML)
print('wrote', p, len(HTML), 'chars |', len(FIND), 'findings |', len(PROPOSE), 'proposals')
