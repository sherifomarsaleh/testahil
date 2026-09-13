/* assets/levers.js — the per-stock sensitivity levers, one place.

   WHAT THIS IS. Each entry is the lever set for one study's "What could move it —
   sensitivity" panel: the slider bounds, the base position, how much a unit of the
   slider moves the published fair value (impact, in log space, per unit), the label at
   each end, and the prose the panel prints at the position the reader drags to.

   WHY IT IS HERE AND NOT IN THE PAGE. Until 13-Sep-2026 every one of these arrays was
   typed inside its own ticker page, 93 separate copies of the same structure. Two costs,
   both paid: a lever could only be changed by rewriting a published page, and a mistake
   in one copy was invisible from every other — which is how four levers shipped pointing
   the wrong way, and how CLHO ended up with a currency-path label ("sharp depreciation")
   on a cost-of-capital slider that three other pages carry verbatim from the same
   placeholder. One file can be read, checked and written in one place.

   THE SOURCE OF TRUTH IS THIS FILE. The pages read it and hold no lever of their own;
   scripts/check_lever_directions.py refuses a page that carries one again.

   impact is a LOG-SPACE coefficient: the panel computes
       fair = base * exp( sum over levers of impact * (value - def) / 100 )
   and each impact is sized from that study's own published variants for that input,
   scaled by the weight its cash-flow lens carries in the published central.

   Migrated verbatim from the 93 pages on 13-Sep-2026 — bounds, defaults, impacts,
   labels and fmt bodies were moved unchanged and asserted field by field against the
   pages they came from.
*/
const LEVERS = {
"2POINTZERO": [
  { name:'Trust in the portfolio marks (opacity discount)', min:0, max:40, step:1, def:15, impact:0.9,
    lo:'trust less / deeper haircut', hi:'trust more / thinner haircut',
    fmt:v=>(40-v)+'% haircut on the portfolio mark' },
  { name:'Unlisted-asset execution (Traverse / Mopani / Alphamin / ISEM)', min:-6, max:8, step:0.1, def:0.4, impact:1,
    lo:'weaker', hi:'stronger', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Fed / CBUAE policy-rate path (the peg imports it)', min:-6, max:6, step:0.1, def:0.1, impact:0.7,
    lo:'tighter / rate headwind', hi:'easier / rate tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Operating-margin delivery (ex-portfolio income)', min:-4, max:4, step:0.25, def:0, impact:1.4,
    lo:'margin slips', hi:'margin firms', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(2)+'pp vs the ~12% base' },
  { name:'Buyback / distribution support — probability', min:0, max:90, step:1, def:35, impact:0.05,
    lo:'unlikely', hi:'likely', fmt:v=>Math.round(v)+'% chance' }
],

"AAPL": [
  { name:'Services attach & AI-cycle drift', min:-8, max:10, step:0.5, def:1, impact:1,
    lo:'sharp depreciation', hi:'firm / tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Regulatory / antitrust hit — probability', min:0, max:55, step:1, def:30, impact:0.06,
    lo:'unlikely', hi:'likely', fmt:v=>Math.round(v)+'% chance' },
  { name:'AI upgrade / WWDC catalyst — probability', min:0, max:90, step:1, def:35, impact:0.05,
    lo:'unlikely', hi:'likely', fmt:v=>Math.round(v)+'% chance' },
  { name:'iPhone & hardware volume', min:-5, max:8, step:0.5, def:0, impact:1,
    lo:'weaker', hi:'stronger', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'US real-rate / Nasdaq-flow path', min:-6, max:8, step:0.5, def:-0.5, impact:1,
    lo:'weaker', hi:'stronger', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' }
],

"ABUK": [
  { name:'Gas-feedstock margin — subsidised vs. export parity', min:-25, max:10, step:0.5, def:-3, impact:1,
    lo:'margin squeeze', hi:'margin tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Urea / ammonia export price ($/t)', min:-30, max:30, step:1, def:0, impact:0.9,
    lo:'prices fall', hi:'prices rally', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'EGP / USD translation', min:-12, max:4, step:0.5, def:-2, impact:1,
    lo:'sharp depreciation', hi:'firm / tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'~9–10% dividend sustained — probability', min:0, max:95, step:1, def:80, impact:0.05,
    lo:'cut risk', hi:'held', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Plant utilisation / gas availability', min:-15, max:8, step:0.5, def:0, impact:0.8,
    lo:'curtailed', hi:'full run-rate', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' }
],

"ACWA": [
  { name:'Saudi / global rate path (the discount-rate driver)', min:-6, max:6, step:0.1, def:-1, impact:1,
    lo:'tighter / rate headwind', hi:'easier / rate tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Impairment / project delay / offtaker dispute — probability', min:0, max:55, step:1, def:28, impact:0.05,
    lo:'unlikely', hi:'likely', fmt:v=>Math.round(v)+'% chance' },
  { name:'New financial close / project award — probability', min:0, max:90, step:1, def:50, impact:0.05,
    lo:'unlikely', hi:'likely', fmt:v=>Math.round(v)+'% chance' },
  { name:'Vision 2030 / PIF pipeline momentum', min:-5, max:8, step:0.5, def:1.5, impact:1,
    lo:'weaker', hi:'stronger', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Oil price & Saudi fiscal impulse', min:-6, max:8, step:0.5, def:0.5, impact:1,
    lo:'weak / low liquidity', hi:'strong / ample liquidity', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' }
],

"ADCB": [
  { name:'CBUAE / Fed policy-rate path (the NIM driver)', min:-6, max:6, step:0.1, def:0.2, impact:1,
    lo:'tighter / rate headwind', hi:'easier / rate tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Oil / geopolitical / credit-event shock — probability', min:0, max:55, step:1, def:45, impact:0.06,
    lo:'high risk', hi:'calm', fmt:v=>Math.round(v)+'% chance' },
  { name:'Dividend declaration surprise — probability', min:0, max:90, step:1, def:30, impact:0.05,
    lo:'no surprise', hi:'upside surprise', fmt:v=>Math.round(v)+'% chance' },
  { name:'Non-oil GDP & diversification credit demand', min:-5, max:8, step:0.5, def:0.3, impact:1,
    lo:'demand softening', hi:'demand accelerating', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Oil price & fiscal impulse (system liquidity)', min:-6, max:8, step:0.5, def:0.1, impact:1,
    lo:'weak / low liquidity', hi:'strong / ample liquidity', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' }
],

"ADIB": [
  { name:'Nominal-repricing drift — fades vs. persists', min:-4, max:20, step:0.5, def:11, impact:1,
    lo:'weaker', hi:'stronger', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'ROE persistence through CBE easing', min:-6, max:6, step:0.5, def:0, impact:1,
    lo:'spread compresses', hi:'spread holds', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Financing book growth', min:-10, max:20, step:1, def:5, impact:0.6,
    lo:'contraction', hi:'rapid growth', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Cost of risk / provisioning', min:-8, max:4, step:0.5, def:0, impact:0.7,
    lo:'NPLs rise', hi:'benign', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Capital return / payout lift — probability', min:0, max:90, step:1, def:30, impact:0.05,
    lo:'hoards capital', hi:'returns it', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' }
],

"ADIBUAE": [
  { name:'CBUAE / Fed policy-rate path (the margin driver)', min:-6, max:6, step:0.1, def:0.1, impact:1,
    lo:'tighter / rate headwind', hi:'easier / rate tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Regional conflict — Strait of Hormuz re-escalation, probability', min:0, max:55, step:1, def:45, impact:0.06,
    lo:'high risk', hi:'calm', fmt:v=>Math.round(v)+'% chance' },
  { name:'UAE minimum-tax (DMTT) step landing in FY2027 — probability', min:0, max:90, step:1, def:40, impact:0.05,
    lo:'unlikely', hi:'likely', fmt:v=>Math.round(v)+'% chance' },
  { name:'UAE non-oil credit growth & financing demand', min:-5, max:8, step:0.5, def:0.3, impact:1,
    lo:'demand softening', hi:'demand accelerating', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Oil price & UAE fiscal impulse (system liquidity)', min:-6, max:8, step:0.5, def:0.1, impact:1,
    lo:'weak / low liquidity', hi:'strong / ample liquidity', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' }
],

"ADNOCDIST": [
  { name:"Biosimilar revenue by FY2030", min:0, max:120, step:10, def:0, impact:0.60,
    lo:"the plant sells nothing (the published case)", hi:"USD 120m a year",
    fmt:v=>"USD "+v.toFixed(0)+"m a year of revenue from the new plant by FY2030 \u2014 the study charges the plant's depreciation and its interest but credits it with ZERO revenue, so this is the single lever that is not in the published number at all. About USD "+120+"m closes the whole gap to the market price" },
  { name:"Credit-loss and provision charge", min:-2.75, max:1.5, step:0.25, def:0, impact:0.50,
    lo:"normalises to 2.5% of revenue", hi:"runs at the three-year mean 6.52%",
    fmt:v=>(5.25+v).toFixed(2)+"% of revenue \u2014 THE contested judgement, published both ways and never averaged. Frame A carries 5.25% permanently; Frame B decays to 2.5%. The first quarter of 2026 booked NO credit loss at all, which the auditor qualified, so the question is deferred rather than settled" },
  { name:"Terminal risk-free rate", min:-1.5, max:1.5, step:0.25, def:0, impact:0.85,
    lo:"9.0% \u2014 real rate at long-run GDP growth", hi:"12.0%",
    fmt:v=>(10.5+v).toFixed(2)+"% terminal risk-free rate \u2014 the widest single lever in the study and the one input still resting on an unsourced convention: a sourced 5% inflation target plus an asserted 5.5-point real rate, which sits above the United Arab Emirates's own long-run real growth" },
  { name:"Domestic price per pack \u2014 annual step", min:-3, max:3, step:0.5, def:0, impact:0.45,
    lo:"the administered price lags inflation", hi:"it keeps pace",
    fmt:v=>(v>=0?"+":"\u2212")+Math.abs(v).toFixed(1)+"pp on the forecast domestic price path. The company realised +12.59% on its own preparations in FY2025 \u2014 measured properly, after separating out product it manufactures under contract \u2014 against a domestic price the the United Arab Emiratesian Drug Authority administers" },
  { name:"Associate contribution", min:-200, max:100, step:25, def:0, impact:0.30,
    lo:"the quarter's run-rate (AED 52m)", hi:"the best disclosed year",
    fmt:v=>"AED "+(250+v).toFixed(0)+"m normalised \u2014 worth about AED "+((250+v)*11/168.75575).toFixed(2)+" a share in the bridge at 11x. The three disclosed years average 246; the first quarter of 2026 annualises to 52, but the auditor states two holdings' statements were not received, so that quarter is evidence rather than a run-rate" }
],

"ADNOCDRILL": [
  { name:"Biosimilar revenue by FY2030", min:0, max:120, step:10, def:0, impact:0.60,
    lo:"the plant sells nothing (the published case)", hi:"USD 120m a year",
    fmt:v=>"USD "+v.toFixed(0)+"m a year of revenue from the new plant by FY2030 \u2014 the study charges the plant's depreciation and its interest but credits it with ZERO revenue, so this is the single lever that is not in the published number at all. About USD "+120+"m closes the whole gap to the market price" },
  { name:"Credit-loss and provision charge", min:-2.75, max:1.5, step:0.25, def:0, impact:0.50,
    lo:"normalises to 2.5% of revenue", hi:"runs at the three-year mean 6.52%",
    fmt:v=>(5.25+v).toFixed(2)+"% of revenue \u2014 THE contested judgement, published both ways and never averaged. Frame A carries 5.25% permanently; Frame B decays to 2.5%. The first quarter of 2026 booked NO credit loss at all, which the auditor qualified, so the question is deferred rather than settled" },
  { name:"Terminal risk-free rate", min:-1.5, max:1.5, step:0.25, def:0, impact:0.85,
    lo:"9.0% \u2014 real rate at long-run GDP growth", hi:"12.0%",
    fmt:v=>(10.5+v).toFixed(2)+"% terminal risk-free rate \u2014 the widest single lever in the study and the one input still resting on an unsourced convention: a sourced 5% inflation target plus an asserted 5.5-point real rate, which sits above the United Arab Emirates's own long-run real growth" },
  { name:"Domestic price per pack \u2014 annual step", min:-3, max:3, step:0.5, def:0, impact:0.45,
    lo:"the administered price lags inflation", hi:"it keeps pace",
    fmt:v=>(v>=0?"+":"\u2212")+Math.abs(v).toFixed(1)+"pp on the forecast domestic price path. The company realised +12.59% on its own preparations in FY2025 \u2014 measured properly, after separating out product it manufactures under contract \u2014 against a domestic price the the United Arab Emiratesian Drug Authority administers" },
  { name:"Associate contribution", min:-200, max:100, step:25, def:0, impact:0.30,
    lo:"the quarter's run-rate (AED 52m)", hi:"the best disclosed year",
    fmt:v=>"AED "+(250+v).toFixed(0)+"m normalised \u2014 worth about AED "+((250+v)*11/168.75575).toFixed(2)+" a share in the bridge at 11x. The three disclosed years average 246; the first quarter of 2026 annualises to 52, but the auditor states two holdings' statements were not received, so that quarter is evidence rather than a run-rate" }
],

"ADNOCGAS": [
  { name:'Brent-linked export price path', min:-8, max:8, step:0.5, def:0.2, impact:1,
    lo:'sharp depreciation', hi:'firm / tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Regional-security / facilities event — probability', min:0, max:55, step:1, def:30, impact:0.09,
    lo:'high risk', hi:'calm', fmt:v=>Math.round(v)+'% chance' },
  { name:'New LNG / gas offtake agreement — probability', min:0, max:90, step:1, def:35, impact:0.05,
    lo:'unlikely', hi:'likely', fmt:v=>Math.round(v)+'% chance' },
  { name:'Global gas & LNG demand / price', min:-5, max:8, step:0.5, def:0.3, impact:1,
    lo:'demand softening', hi:'demand accelerating', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'US real rates (the dividend discount)', min:-6, max:8, step:0.5, def:-0.5, impact:1,
    lo:'tighter / rate headwind', hi:'easier / rate tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' }
],

"ADNOCLS": [
  { name:"Beta \u2014 how the market is measured", min:0.70, max:1.62, step:0.01, def:1.10, impact:-38.78,
    lo:"0.71 \u2014 equal-weight composite of the exchange", hi:"1.62 \u2014 top of the 90% interval",
    fmt:v=>"beta "+v.toFixed(2)+" \u2014 the widest lever in the study. The published figure is 1.1032, regressed weekly against the FTSE ADX General Index, the published index of the share\u0027s own exchange, over 159 observations (R\u00b2 0.181, standard error 0.315, 90% interval 0.59 to 1.62). The engine resolves that regressor; it is not an analyst\u0027s pick. Regressing against an equal-weight composite of the same exchange instead gives 0.71 and lifts the cash-flow value from AED 6.40 to 9.37, which is why both centres are published. A HIGHER beta is a higher cost of equity and a LOWER value, never the reverse" },
  { name:"Mid-cycle tanker rate anchor", min:-20, max:20, step:5, def:0, impact:0.32,
    lo:"20% below the study\u0027s anchor", hi:"20% above it",
    fmt:v=>(v>=0?"+":"\u2212")+Math.abs(v).toFixed(0)+"% on the mid-cycle day-rate anchor the forecast reverts to. The cash-flow value runs AED 5.38 at \u221220% to 7.43 at +20%. The base path reverts from an implied very-large-crude-carrier spot of 199,838 a day toward 47,924 by the terminal year \u2014 corroborated by a one-year time charter fixed at 76,900, well under spot, and an order book near 27% of the trading fleet" },
  { name:"Terminal growth", min:1.0, max:2.5, step:0.25, def:2.0, impact:2.72,
    lo:"1.0%", hi:"2.5%",
    fmt:v=>v.toFixed(2)+"% terminal growth. Across the study\u0027s own grid the cash-flow value runs AED 6.02 at 1.0% to 6.65 at 2.5% at the published beta. Terminal value is 75% of enterprise value, so this input carries more of the answer than any operating assumption below it" },
  { name:"Capital spending programme", min:-10, max:20, step:5, def:0, impact:-0.26,
    lo:"10% under the disclosed programme", hi:"20% over it",
    fmt:v=>(v>=0?"+":"\u2212")+Math.abs(v).toFixed(0)+"% on forecast capital spending \u2014 AED 6.81 at \u221210% to 5.59 at +20% on the cash-flow lens. The USD 1.3 billion, eleven-vessel purchase announced on 7 August 2026, the study\u0027s own anchor date \u2014 six very large crude carriers and five gas carriers \u2014 is already inside the published number, not an upside case sitting outside it" }
],

"AGTHIA": [
  { name:'Snacking margin reset — execution', min:-6, max:8, step:0.5, def:0.6, impact:1,
    lo:'sharp depreciation', hi:'firm / tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Regional geopolitical escalation — probability', min:0, max:55, step:1, def:40, impact:0.025,
    lo:'high risk', hi:'calm', fmt:v=>Math.round(v)+'% chance' },
  { name:'Re-rating catalyst — KSA award / ADQ action — probability', min:0, max:90, step:1, def:30, impact:0.05,
    lo:'unlikely', hi:'likely', fmt:v=>Math.round(v)+'% chance' },
  { name:'Input costs — coffee, wheat & resin', min:-6, max:4, step:0.5, def:-0.8, impact:1,
    lo:'weaker', hi:'stronger', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'GCC consumer & UAE tourism demand', min:-5, max:6, step:0.5, def:0.8, impact:1,
    lo:'demand softening', hi:'demand accelerating', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' }
],

"AIRARABIA": [
  { name:"Terminal kitchen margin", min:-2.1, max:1.0, step:0.1, def:0, impact:5.5,
    lo:"reverts to the audited average 22.8%", hi:"holds above the modelled peak",
    fmt:v=>(24.9+v).toFixed(1)+"% terminal operating-cash margin \u2014 THE contested judgement, published both ways and never averaged: structural gives AED 2.31, full reversion to the audited 22.8% average gives 1.98. The model itself peaks at 25.4% and eases to 24.9% as the delivery channel grows" },
  { name:"Return on new restaurant capital", min:-10, max:25, step:5, def:0, impact:0.25,
    lo:"20% \u2014 payback stretches past five years", hi:"55% \u2014 the forecast years\u2019 implied average",
    fmt:v=>(30+v).toFixed(0)+"% terminal return on new capital \u2014 the base 30% is anchored on the company\u2019s own disclosed ~3-year store payback; the 55% the forecast years imply is published as the bull case, not the base" },
  { name:"Cost of capital", min:-1, max:1, step:0.25, def:0, impact:-8,
    lo:"8.5% \u2014 the CDS-basis premium blend", hi:"10.5%",
    fmt:v=>(9.5+v).toFixed(2)+"% WACC \u2014 a 12-country revenue-weighted premium blend from the UAE to Egypt to Kazakhstan, published on both the rating and CDS bases" },
  { name:"Delivery cost per delivered dollar", min:-1, max:1, step:0.25, def:0, impact:-3.5,
    lo:"aggregator economics improve", hi:"aggregators take a bigger cut",
    fmt:v=>(14.1+v).toFixed(2)+"% of delivered sales \u2014 the channel is disclosed at 44 \u2192 48 \u2192 52% of revenue and rising, so every point of aggregator cost scales with it; this line is why the margin eases rather than expands" },
  { name:"Net store openings", min:-60, max:60, step:10, def:0, impact:0.05,
    lo:"expansion stalls", hi:"the Saudi and growth-brand pipeline accelerates",
    fmt:v=>"about "+(130+v).toFixed(0)+" net new restaurants a year \u2014 the brand build grows KFC, Pizza Hut, Hardee\u2019s, Krispy Kreme and the growth brands on the company\u2019s own disclosed opening mix" }
],

"ALDAR": [
  { name:'Dubai residential & off-plan absorption', min:-8, max:10, step:0.5, def:1, impact:1,
    lo:'sharp depreciation', hi:'firm / tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Dubai property correction / oversupply — probability', min:0, max:55, step:1, def:30, impact:0.06,
    lo:'unlikely', hi:'likely', fmt:v=>Math.round(v)+'% chance' },
  { name:'Backlog conversion / discount compression — probability', min:0, max:90, step:1, def:50, impact:0.05,
    lo:'unlikely', hi:'likely', fmt:v=>Math.round(v)+'% chance' },
  { name:'US rates via the dirham peg', min:-5, max:8, step:0.5, def:-0.5, impact:1,
    lo:'tighter / rate headwind', hi:'easier / rate tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Recurring retail & tourism trajectory', min:-6, max:8, step:0.5, def:0.3, impact:1,
    lo:'weaker', hi:'stronger', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' }
],

"ALINMA": [
  { name:'SAMA / Fed policy-rate path (the NIM driver)', min:-6, max:6, step:0.1, def:0.1, impact:1,
    lo:'tighter / rate headwind', hi:'easier / rate tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Oil / geopolitical / credit-event shock — probability', min:0, max:55, step:1, def:45, impact:0.07,
    lo:'high risk', hi:'calm', fmt:v=>Math.round(v)+'% chance' },
  { name:'Dividend declaration surprise — probability', min:0, max:90, step:1, def:30, impact:0.05,
    lo:'no surprise', hi:'upside surprise', fmt:v=>Math.round(v)+'% chance' },
  { name:'Non-oil GDP & Vision 2030 credit demand', min:-5, max:8, step:0.5, def:0.3, impact:1,
    lo:'demand softening', hi:'demand accelerating', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Oil price & fiscal impulse (system liquidity)', min:-6, max:8, step:0.5, def:0.1, impact:1,
    lo:'weak / low liquidity', hi:'strong / ample liquidity', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' }
],

"ALPHADHABI": [
  { name:'Fed / CBUAE policy-rate path (the peg imports it)', min:-6, max:6, step:0.1, def:0.1, impact:1,
    lo:'tighter / rate headwind', hi:'easier / rate tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Gulf-war stress — probability', min:0, max:55, step:1, def:35, impact:0.085,
    lo:'unlikely', hi:'likely', fmt:v=>Math.round(v)+'% chance' },
  { name:'Buyback / distribution support — probability', min:0, max:90, step:1, def:35, impact:0.05,
    lo:'unlikely', hi:'likely', fmt:v=>Math.round(v)+'% chance' },
  { name:'Abu Dhabi property & Aldar momentum', min:-5, max:8, step:0.1, def:0.7, impact:1,
    lo:'weaker', hi:'stronger', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'IHC deal flow & the FV-gain engine', min:-6, max:8, step:0.1, def:0.4, impact:1,
    lo:'weaker', hi:'stronger', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' }
],

"ALRAJHI": [
  { name:'SAMA / Fed policy-rate path (the NIM driver)', min:-6, max:6, step:0.1, def:0.4, impact:1,
    lo:'tighter / rate headwind', hi:'easier / rate tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Oil / geopolitical / credit shock — probability', min:0, max:55, step:1, def:35, impact:0.06,
    lo:'high risk', hi:'calm', fmt:v=>Math.round(v)+'% chance' },
  { name:'Dividend / payout surprise — probability', min:0, max:90, step:1, def:35, impact:0.05,
    lo:'no surprise', hi:'upside surprise', fmt:v=>Math.round(v)+'% chance' },
  { name:'Vision 2030 credit demand & financing growth', min:-5, max:8, step:0.5, def:0.5, impact:1,
    lo:'demand softening', hi:'demand accelerating', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Oil price & fiscal impulse (system liquidity)', min:-6, max:8, step:0.5, def:0.3, impact:1,
    lo:'weak / low liquidity', hi:'strong / ample liquidity', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' }
],

"AMOC": [
  { name:"Gross margin \u2014 the whole thesis", min:-150, max:150, step:25, def:0, impact:0.244,
    lo:"\u22121.5pp (below the worst filed quarter)", hi:"+1.5pp (above the best)",
    fmt:v=>(v>=0?"+":"\u2212")+Math.abs(v/100).toFixed(2)+"pp on the margin in EVERY forecast year \u2014 the dominant lever, and the one the filings cannot pin down: the record runs 5.05% to 10.19% across four consecutive periods and the margin is administered, not competed. Note where the slider has to sit for fair value to reach the market price" },
  { name:"Volume growth path", min:-100, max:100, step:10, def:0, impact:0.082,
    lo:"no growth at all (\u2212100%)", hi:"double the assumed path (+100%)",
    fmt:v=>(v>=0?"+":"\u2212")+Math.abs(v).toFixed(0)+"% on the assumed growth path across all eight product lines. Deliberately weaker than margin: incremental tonnage now COSTS capital at the plant\u2019s own EGP 1,948 per annual tonne, so volume no longer arrives free the way it did in the previous edition" },
  { name:"Realisation path \u2014 price per tonne", min:-10, max:10, step:1, def:0, impact:1.01,
    lo:"realisations 10% weaker", hi:"realisations 10% stronger",
    fmt:v=>(v>=0?"+":"\u2212")+Math.abs(v).toFixed(0)+"% on the assumed realisation path. Strong, because feedstock is allocated on net realisable value: a move in price per tonne widens the spread faster than it lifts the allocated feed cost" },
  { name:"Working-capital cycle", min:-50, max:50, step:10, def:0, impact:-0.259,
    lo:"cycle halves (\u221250%)", hi:"cycle lengthens 50%",
    fmt:v=>(v>=0?"+":"\u2212")+Math.abs(v).toFixed(0)+"% on the 24.3 / 7.3 / 13.1 day cycle SOLVED from the audited balance sheet \u2014 not assumed. The house registry had carried 14/14/24 days and no formula read any of them" },
  { name:"Beta \u2014 cost of capital", min:0.60, max:1.30, step:0.05, def:0.9405, impact:-21.9,
    lo:"\u03b2 0.60 (defensive)", hi:"\u03b2 1.30 (high-beta)",
    fmt:v=>"\u03b2 "+v.toFixed(2)+" \u2014 flowing to BOTH the explicit and terminal anchors, as the model wires it. Even at 0.60 the cash-flow lens reaches only 6.33: the discount rate cannot close the gap to the market price, which is why the study\u2019s case does not rest on it" }
],

"AMR": [
  { name:"Terminal kitchen margin", min:-2.1, max:1.0, step:0.1, def:0, impact:5.5,
    lo:"reverts to the audited average 22.8%", hi:"holds above the modelled peak",
    fmt:v=>(24.9+v).toFixed(1)+"% terminal operating-cash margin \u2014 THE contested judgement, published both ways and never averaged: structural gives AED 2.23, full reversion to the audited 22.8% average gives 1.92. The model itself peaks at 25.4% and eases to 24.9% as the delivery channel grows" },
  { name:"Return on new restaurant capital", min:-10, max:25, step:5, def:0, impact:0.25,
    lo:"20% \u2014 payback stretches past five years", hi:"55% \u2014 the forecast years\u2019 implied average",
    fmt:v=>(30+v).toFixed(0)+"% terminal return on new capital \u2014 the base 30% is anchored on the company\u2019s own disclosed ~3-year store payback; the 55% the forecast years imply is published as the bull case, not the base" },
  { name:"Cost of capital", min:-1, max:1, step:0.25, def:0, impact:-8,
    lo:"8.5% \u2014 the CDS-basis premium blend", hi:"10.5%",
    fmt:v=>(9.7+v).toFixed(2)+"% WACC \u2014 a 12-country revenue-weighted premium blend from the UAE to Egypt to Kazakhstan, published on both the rating and CDS bases" },
  { name:"Delivery cost per delivered dollar", min:-1, max:1, step:0.25, def:0, impact:-3.5,
    lo:"aggregator economics improve", hi:"aggregators take a bigger cut",
    fmt:v=>(14.1+v).toFixed(2)+"% of delivered sales \u2014 the channel is disclosed at 44 \u2192 48 \u2192 52% of revenue and rising, so every point of aggregator cost scales with it; this line is why the margin eases rather than expands" },
  { name:"Net store openings", min:-60, max:60, step:10, def:0, impact:0.05,
    lo:"expansion stalls", hi:"the Saudi and growth-brand pipeline accelerates",
    fmt:v=>"about "+(130+v).toFixed(0)+" net new restaurants a year \u2014 the brand build grows KFC, Pizza Hut, Hardee\u2019s, Krispy Kreme and the growth brands on the company\u2019s own disclosed opening mix" }
],

"ARAMCO": [
  { name:'Brent crude oil price path', min:-8, max:8, step:0.5, def:-1.5, impact:1,
    lo:'sharp depreciation', hi:'firm / tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Global recession / oil-demand shock — probability', min:0, max:55, step:1, def:47, impact:0.09,
    lo:'high risk', hi:'calm', fmt:v=>Math.round(v)+'% chance' },
  { name:'Geopolitical oil-supply spike — probability', min:0, max:90, step:1, def:22, impact:0.05,
    lo:'high risk', hi:'calm', fmt:v=>Math.round(v)+'% chance' },
  { name:'Global oil demand & refining margins', min:-5, max:8, step:0.5, def:0.3, impact:1,
    lo:'margin squeeze', hi:'margin tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'SAMA / Fed rate path (via the peg)', min:-6, max:8, step:0.5, def:0.6, impact:1,
    lo:'tighter / rate headwind', hi:'easier / rate tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' }
],

"ARCC": [
  { name:"Local cement price \u2014 FY2026 step", min:-6, max:10, step:1, def:0, impact:0.55,
    lo:"prices roll over (\u22126pp)", hi:"the Q4 run-rate extends (+10pp)",
    fmt:v=>(v>=0?"+":"\u2212")+Math.abs(v).toFixed(0)+"pp on the assumed +8.0% FY2026 local price step \u2014 the single largest lever, and the one the study anchors on a DISCLOSED exit rate: the fourth quarter of 2025 realised EGP 3,118 a tonne, 7.2% above the full-year average, so +8.0% is barely a point above prices simply stopping here" },
  { name:"Kiln utilisation", min:-6, max:6, step:1, def:0, impact:0.30,
    lo:"the kiln runs cooler (\u22126pp)", hi:"it runs harder (+6pp)",
    fmt:v=>(v>=0?"+":"\u2212")+Math.abs(v).toFixed(0)+"pp on the 91.7% disclosed kiln rate \u2014 THE volume driver in this build. The plant has run 92\u201394% in three of the last five years, so there is little room above and the lever is asymmetric" },
  { name:"Clinker retained rather than exported", min:-10, max:14, step:2, def:0, impact:0.22,
    lo:"more tonnes ship as raw clinker", hi:"more clinker is ground into cement",
    fmt:v=>(v>=0?"+":"\u2212")+Math.abs(v).toFixed(0)+"pp of clinker production diverted from export into domestic cement \u2014 the operating lever the single-product model could not see. Clinker and cement compete for the SAME kiln, and a tonne shipped raw realises about USD 30 against cement several times that" },
  { name:"CBE easing \u2014 cost of capital", min:0, max:3, step:0.25, def:0, impact:0.58,
    lo:"today\u2019s money (24.52% WACC)", hi:"3pp of easing (21.52%)",
    fmt:v=>(24.52-v).toFixed(2)+"% explicit WACC \u2014 easing "+v.toFixed(2)+"pp. The terminal rate matters more still, and the discount-rate axis dominates the growth axis on this name: four points of terminal growth move the value less than one point of rate" },
  { name:"EBITDA margin", min:-4, max:4, step:1, def:0, impact:0.52,
    lo:"the 2025 step gives back (\u22124pp)", hi:"it holds (+4pp)",
    fmt:v=>(v>=0?"+":"\u2212")+Math.abs(v).toFixed(0)+"pp on every forecast year \u2014 worth about EGP 5.95 a share for two points. The forecast glides the audited 39.3% down through the window; Q1-2026 printed a 42.9% gross margin against 40.6% for FY2025, so the near-term risk is that this is too cautious" }
],

"BOROUGE": [
  { name:"Terminal kitchen margin", min:-2.1, max:1.0, step:0.1, def:0, impact:5.5,
    lo:"reverts to the audited average 22.8%", hi:"holds above the modelled peak",
    fmt:v=>(24.9+v).toFixed(1)+"% terminal operating-cash margin \u2014 THE contested judgement, published both ways and never averaged: structural gives AED 2.31, full reversion to the audited 22.8% average gives 1.98. The model itself peaks at 25.4% and eases to 24.9% as the delivery channel grows" },
  { name:"Return on new restaurant capital", min:-10, max:25, step:5, def:0, impact:0.25,
    lo:"20% \u2014 payback stretches past five years", hi:"55% \u2014 the forecast years\u2019 implied average",
    fmt:v=>(30+v).toFixed(0)+"% terminal return on new capital \u2014 the base 30% is anchored on the company\u2019s own disclosed ~3-year store payback; the 55% the forecast years imply is published as the bull case, not the base" },
  { name:"Cost of capital", min:-1, max:1, step:0.25, def:0, impact:-8,
    lo:"8.5% \u2014 the CDS-basis premium blend", hi:"10.5%",
    fmt:v=>(9.5+v).toFixed(2)+"% WACC \u2014 a 12-country revenue-weighted premium blend from the UAE to Egypt to Kazakhstan, published on both the rating and CDS bases" },
  { name:"Delivery cost per delivered dollar", min:-1, max:1, step:0.25, def:0, impact:-3.5,
    lo:"aggregator economics improve", hi:"aggregators take a bigger cut",
    fmt:v=>(14.1+v).toFixed(2)+"% of delivered sales \u2014 the channel is disclosed at 44 \u2192 48 \u2192 52% of revenue and rising, so every point of aggregator cost scales with it; this line is why the margin eases rather than expands" },
  { name:"Net store openings", min:-60, max:60, step:10, def:0, impact:0.05,
    lo:"expansion stalls", hi:"the Saudi and growth-brand pipeline accelerates",
    fmt:v=>"about "+(130+v).toFixed(0)+" net new restaurants a year \u2014 the brand build grows KFC, Pizza Hut, Hardee\u2019s, Krispy Kreme and the growth brands on the company\u2019s own disclosed opening mix" }
],

"BTFH": [
  { name:'CBE easing tailwind vs. Baobab integration drag', min:-10, max:12, step:0.5, def:2, impact:1,
    lo:'weaker', hi:'stronger', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'ROE lift 11%→18% — probability', min:0, max:90, step:1, def:40, impact:0.1,
    lo:'stays ~11%', hi:'reaches ~18%', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Baobab microfinance accretion — probability', min:0, max:90, step:1, def:45, impact:0.06,
    lo:'dilutive', hi:'accretive', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Brokerage + AUM market flow', min:-12, max:15, step:1, def:3, impact:0.7,
    lo:'volumes dry', hi:'volumes surge', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Fairness / holdco discount narrowing', min:-10, max:12, step:1, def:0, impact:0.6,
    lo:'widens', hi:'narrows', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' }
],

"BURJEEL": [
  { name:'USD funding costs — sukuk & policy-rate path', min:-3, max:3, step:0.1, def:0, impact:1,
    lo:'tighter / rate headwind', hi:'easier / rate tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'DMTT exclusion or safe-harbour persists — FY2025 return (2026–27 filing)', min:0, max:90, step:1, def:0, impact:0.03,
    lo:'unlikely', hi:'likely', fmt:v=>Math.round(v)+'% chance' },
  { name:'Q3-2026 margin print confirms the recovery to 22%+', min:0, max:90, step:1, def:0, impact:0.05,
    lo:'unlikely', hi:'likely', fmt:v=>Math.round(v)+'% chance' },
  { name:'Receivables (DSO) normalization pace', min:-3, max:3, step:0.1, def:0, impact:1,
    lo:'weaker', hi:'stronger', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Margin mix — oncology growth vs. surgical recovery', min:-3, max:3, step:0.1, def:0, impact:1,
    lo:'margin squeeze', hi:'margin tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' }
],

"CCAP": [
  { name:'ERC refining margin — gasoil/fuel-oil crack', min:-8, max:10, step:0.5, def:0, impact:1,
    lo:'sharp depreciation', hi:'firm / tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Refining setback / going-concern flare — probability', min:0, max:55, step:1, def:30, impact:0.06,
    lo:'unlikely', hi:'likely', fmt:v=>Math.round(v)+'% chance' },
  { name:'Discount compression / value-up — probability', min:0, max:90, step:1, def:30, impact:0.05,
    lo:'unlikely', hi:'likely', fmt:v=>Math.round(v)+'% chance' },
  { name:'ERC de-levering — dividend resumption', min:-5, max:8, step:0.5, def:0, impact:1,
    lo:'weaker', hi:'stronger', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Egyptian pound — ERC USD-functional FX', min:-6, max:8, step:0.5, def:0, impact:1,
    lo:'sharp depreciation', hi:'firm / tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' }
],

"CLHO": [
  { name:'CBE facility-cost path (WACC glide)', min:-3, max:3, step:0.1, def:-0.7, impact:1,
    lo:'sharp depreciation', hi:'firm / tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Strategic-review / per-bed takeout interest — probability', min:0, max:60, step:1, def:15, impact:0.08,
    lo:'unlikely', hi:'likely', fmt:v=>Math.round(v)+'% chance' },
  { name:'New facility opening ahead of schedule — probability', min:5, max:70, step:1, def:30, impact:0.05,
    lo:'unlikely', hi:'likely', fmt:v=>Math.round(v)+'% chance' },
  { name:'Bed-capacity ramp execution (880→1,320 by 2027)', min:-3, max:3, step:0.1, def:0.5, impact:1,
    lo:'weaker', hi:'stronger', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'El Niño food-inflation drag on CBE easing', min:-3, max:3, step:0.1, def:-0.3, impact:1,
    lo:'disinflation', hi:'inflation / debasement', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' }
],

"COMI": [
  { name:'EGP/USD & carry — impact on COMI', min:-10, max:4, step:0.5, def:-1, impact:1,
    lo:'sharp depreciation', hi:'firm / tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Sovereign / policy stress — probability', min:0, max:55, step:1, def:35, impact:0.12,
    lo:'unlikely', hi:'likely', fmt:v=>Math.round(v)+'% chance' },
  { name:'Capital return & ROE defence — probability', min:0, max:90, step:1, def:40, impact:0.05,
    lo:'unlikely', hi:'likely', fmt:v=>Math.round(v)+'% chance' },
  { name:'ROE–CoE spread (~6pt) durability', min:-6, max:6, step:0.5, def:0, impact:1,
    lo:'spread compresses', hi:'spread widens', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Loan / balance-sheet growth', min:-10, max:18, step:1, def:5, impact:0.6,
    lo:'contraction', hi:'rapid growth', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' }
],

"DEWA": [
  { name:'CBUAE / Fed policy-rate path', min:-3, max:3, step:0.1, def:0.1, impact:1,
    lo:'tighter / rate headwind', hi:'easier / rate tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Post-2027 dividend policy — probability of a frozen-or-cut signal', min:0, max:47, step:1, def:40, impact:0.02,
    lo:'no surprise', hi:'upside surprise', fmt:v=>Math.round(v)+'% chance' },
  { name:'Post-2027 dividend policy — probability of a growth signal', min:5, max:60, step:1, def:20, impact:0.05,
    lo:'no surprise', hi:'upside surprise', fmt:v=>Math.round(v)+'% chance' },
  { name:'2030 clean-energy build pace', min:-3, max:3, step:0.1, def:0.1, impact:1,
    lo:'weaker', hi:'stronger', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Regulatory deferral account swing', min:-3, max:3, step:0.1, def:0, impact:1,
    lo:'weaker', hi:'stronger', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' }
],

"DIB": [
  { name:'Net profit margin path (the crux)', min:-2, max:2, step:0.1, def:0, impact:1,
    lo:'sharp depreciation', hi:'firm / tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Effective tax rate — path back toward 9%', min:-5, max:8, step:0.5, def:0, impact:1,
    lo:'weaker', hi:'stronger', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Cost of risk normalization pace', min:-6, max:6, step:0.5, def:0, impact:1,
    lo:'weaker', hi:'stronger', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Iran-war / Hormuz escalation — probability', min:0, max:55, step:1, def:40, impact:0.06,
    lo:'high risk', hi:'calm', fmt:v=>Math.round(v)+'% chance' },
  { name:'Dividend / capital signal — probability', min:0, max:90, step:1, def:25, impact:0.05,
    lo:'no surprise', hi:'upside surprise', fmt:v=>Math.round(v)+'% chance' }
],

"DSCW": [
  { name:"CBE policy rate", min:0, max:8.53, step:0.25, def:0, impact:4.13,
    lo:"today\u2019s rate (23.53%)", hi:"full easing (15.0%)",
    fmt:v=>(23.53-v).toFixed(2)+"% WACC \u2014 easing "+v.toFixed(1)+"pp, the single biggest driver here" },
  { name:"Cotton / input cost (gross margin)", min:-2, max:2, step:0.25, def:0, impact:8.0,
    lo:"cotton dearer / margin worse", hi:"cotton cheaper / margin better",
    fmt:v=>(v>=0?"+":"\u2212")+Math.abs(v).toFixed(2)+"pp gross margin vs the 22.5% FY26E base" },
  { name:"EGP/USD (export translation)", min:-4, max:8, step:0.5, def:0, impact:0.8,
    lo:"EGP firm / no further slide", hi:"faster depreciation (export tailwind)",
    fmt:v=>(v>=0?"+":"\u2212")+Math.abs(v).toFixed(1)+"% vs the FY26E path" },
  { name:"US / EU apparel-import demand", min:-10, max:10, step:1, def:0, impact:2.0,
    lo:"demand softens", hi:"demand firms",
    fmt:v=>(v>=0?"+":"\u2212")+Math.abs(v).toFixed(0)+"% export volume vs base" },
  { name:"Regional geopolitics / shipping lanes", min:0, max:60, step:5, def:15, impact:0.10,
    lo:"disruption / higher freight", hi:"calm / normal freight",
    fmt:v=>Math.round(60-v)+"% disruption risk priced in" }
],

"DU": [
  { name:"Terminal kitchen margin", min:-2.1, max:1.0, step:0.1, def:0, impact:5.5,
    lo:"reverts to the audited average 22.8%", hi:"holds above the modelled peak",
    fmt:v=>(24.9+v).toFixed(1)+"% terminal operating-cash margin \u2014 THE contested judgement, published both ways and never averaged: structural gives AED 2.31, full reversion to the audited 22.8% average gives 1.98. The model itself peaks at 25.4% and eases to 24.9% as the delivery channel grows" },
  { name:"Return on new restaurant capital", min:-10, max:25, step:5, def:0, impact:0.25,
    lo:"20% \u2014 payback stretches past five years", hi:"55% \u2014 the forecast years\u2019 implied average",
    fmt:v=>(30+v).toFixed(0)+"% terminal return on new capital \u2014 the base 30% is anchored on the company\u2019s own disclosed ~3-year store payback; the 55% the forecast years imply is published as the bull case, not the base" },
  { name:"Cost of capital", min:-1, max:1, step:0.25, def:0, impact:-8,
    lo:"8.5% \u2014 the CDS-basis premium blend", hi:"10.5%",
    fmt:v=>(9.5+v).toFixed(2)+"% WACC \u2014 a 12-country revenue-weighted premium blend from the UAE to Egypt to Kazakhstan, published on both the rating and CDS bases" },
  { name:"Delivery cost per delivered dollar", min:-1, max:1, step:0.25, def:0, impact:-3.5,
    lo:"aggregator economics improve", hi:"aggregators take a bigger cut",
    fmt:v=>(14.1+v).toFixed(2)+"% of delivered sales \u2014 the channel is disclosed at 44 \u2192 48 \u2192 52% of revenue and rising, so every point of aggregator cost scales with it; this line is why the margin eases rather than expands" },
  { name:"Net store openings", min:-60, max:60, step:10, def:0, impact:0.05,
    lo:"expansion stalls", hi:"the Saudi and growth-brand pipeline accelerates",
    fmt:v=>"about "+(130+v).toFixed(0)+" net new restaurants a year \u2014 the brand build grows KFC, Pizza Hut, Hardee\u2019s, Krispy Kreme and the growth brands on the company\u2019s own disclosed opening mix" }
],

"EAND": [
  { name:'CBUAE / Fed policy-rate path', min:-3, max:3, step:0.1, def:-0.2, impact:1,
    lo:'tighter / rate headwind', hi:'easier / rate tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'2027 UAE royalty regime — probability of an adverse outcome', min:0, max:55, step:1, def:45, impact:0.018,
    lo:'unlikely', hi:'likely', fmt:v=>Math.round(v)+'% chance' },
  { name:'Vodafone sale — probability of full, timely completion', min:40, max:95, step:1, def:75, impact:0.05,
    lo:'unlikely', hi:'likely', fmt:v=>Math.round(v)+'% chance' },
  { name:'UAE mobile competition intensity (du share, ARPU drift)', min:-3, max:3, step:0.1, def:-0.1, impact:1,
    lo:'weaker', hi:'stronger', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'International portfolio FX & margin (Maroc Telecom, PPF, Egypt, PTCL)', min:-3, max:5, step:0.1, def:0.3, impact:1,
    lo:'sharp depreciation', hi:'firm / tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' }
],

"EFID": [
  { name:'Price-point migration & disinflation tailwind vs. consumer squeeze', min:-10, max:12, step:0.5, def:0.5, impact:1,
    lo:'disinflation', hi:'inflation / debasement', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'EGP / USD translation', min:-12, max:4, step:0.5, def:-2, impact:1,
    lo:'sharp depreciation', hi:'firm / tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'34–35% gross margin defence', min:-8, max:5, step:0.5, def:0, impact:1,
    lo:'margin erodes', hi:'margin holds', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Pack volume growth', min:-8, max:15, step:1, def:5, impact:0.6,
    lo:'volumes fall', hi:'volumes surge', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Input / commodity cost (flour, oil, cocoa)', min:-10, max:8, step:0.5, def:0, impact:0.7,
    lo:'costs spike', hi:'costs ease', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' }
],

"EFIH": [
  { name:'EGP interest-rate path — impact on e-finance', min:-6, max:4, step:0.5, def:0, impact:1,
    lo:'tighter / rate headwind', hi:'easier / rate tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Regulatory / fee-cap shock — probability', min:0, max:35, step:1, def:20, impact:0.12,
    lo:'high risk', hi:'calm', fmt:v=>Math.round(v)+'% chance' },
  { name:'New government mandate / growth execution — probability', min:0, max:90, step:1, def:25, impact:0.05,
    lo:'unlikely', hi:'likely', fmt:v=>Math.round(v)+'% chance' },
  { name:'Transaction / e-payment volume growth', min:-12, max:20, step:1, def:8, impact:0.8,
    lo:'growth stalls', hi:'growth accelerates', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Blended take-rate / margin', min:-8, max:8, step:0.5, def:0, impact:1,
    lo:'compresses', hi:'expands', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' }
],

"EGAL": [
  { name:'Calibrated secular drift — fades vs. persists', min:-6, max:26, step:0.5, def:15, impact:1,
    lo:'weaker', hi:'stronger', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'LME aluminium price ($/t)', min:-25, max:25, step:1, def:0, impact:1,
    lo:'prices fall', hi:'prices rally', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'EGP / USD translation (LME in $)', min:-12, max:4, step:0.5, def:-2, impact:1,
    lo:'sharp depreciation', hi:'firm / tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Administered power contract holds — probability', min:0, max:95, step:1, def:75, impact:0.08,
    lo:'tariff reset up', hi:'contract holds', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Trafigura US$900m expansion signs — probability', min:0, max:90, step:1, def:55, impact:0.06,
    lo:'stalls', hi:'signs / doubles capacity', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' }
],

"EGCH": [
  { name:"EBITDA margin vs the kiln build", min:-4, max:4, step:0.5, def:0, impact:3.40,
    lo:"2pp worse than modelled", hi:"2pp better",
    fmt:v=>(v>=0?"+":"\u2212")+Math.abs(v).toFixed(1)+"pp on the built margin (FY2026E lands at 30.1% as an OUTPUT, not an input)" },
  { name:"Kiln utilisation, FY2027E", min:61.7, max:81.7, step:0.5, def:71.7, impact:2.00,
    lo:"62% \u2014 the revived capacity bites", hi:"82% \u2014 exports absorb the surplus",
    fmt:v=>v.toFixed(1)+"% of the 2.57Mt kiln \u2014 the build runs 71.0% in FY2025A to 79.1% by FY2030E" },
  { name:"Net cash on the balance sheet", min:3.43, max:6.43, step:0.25, def:4.93, impact:6.00,
    lo:"EGP 3.4bn", hi:"EGP 6.4bn",
    fmt:v=>"EGP "+v.toFixed(2)+"bn at the valuation date \u2014 43% of the market capitalisation, and the largest single sensitivity in the study" },
  { name:"CBE easing \u2014 cost of capital", min:0, max:4, step:0.25, def:0, impact:1.60,
    lo:"today\u2019s money (28.30% WACC)", hi:"4pp of easing (24.30%)",
    fmt:v=>(28.30-v).toFixed(2)+"% explicit WACC \u2014 easing "+v.toFixed(2)+"pp" },
  { name:"Terminal growth \u2014 runs BACKWARDS", min:3, max:7, step:0.25, def:5, impact:-1.75,
    lo:"3% terminal growth", hi:"7% terminal growth",
    fmt:v=>v.toFixed(2)+"% \u2014 more growth SUBTRACTS value here, because terminal ROIC of 9.3% sits below the 19.0% terminal cost of capital" }
],

"ELEC": [
  { name:"Working-capital collection (terminal NWC intensity)", min:0, max:36, step:2, def:0, impact:0.030,
    lo:"stays where it is (112% of revenue)", hi:"collects back to FY24 (76%)",
    fmt:v=>(112-v).toFixed(0)+"% of revenue \u2014 the crux; every 5pp is worth roughly EGP 0.15\u20130.20/share on the unfloored DCF" },
  { name:"Conversion EBITDA per tonne", min:-30, max:30, step:5, def:0, impact:0.032,
    lo:"trough persists (\u221230%)", hi:"windfall partly returns (+30%, \u2248175k EGP/t)",
    fmt:v=>(v>=0?"+":"\u2212")+Math.abs(v).toFixed(0)+"% vs the build\u2019s 135k EGP/t terminal" },
  { name:"CBE easing / cost of capital", min:0, max:6.53, step:0.25, def:0, impact:0.055,
    lo:"today\u2019s money (21.53% WACC)", hi:"full glide to the terminal (15.0%)",
    fmt:v=>(21.53-v).toFixed(2)+"% WACC \u2014 easing "+v.toFixed(1)+"pp" },
  { name:"LME copper", min:-20, max:20, step:2, def:0, impact:0.012,
    lo:"copper falls (frees working capital)", hi:"copper rises (traps working capital)",
    fmt:v=>"$"+Math.round(14000*(1+v/100)).toLocaleString()+"/t vs the $14,000 anchor \u2014 double-edged: higher copper lifts revenue but inflates the capital it must fund" },
  { name:"Net-debt anchor (triangulated, not disclosed)", min:-685, max:555, step:35, def:0, impact:-0.00030,
    lo:"low end of the range (9,120)", hi:"high end (10,360)",
    fmt:v=>"EGP "+Math.round(9805+v).toLocaleString()+" mn net debt" }
],

"ELM": [
  { name:'Discount-rate re-rating (β the market assigns Elm)', min:-6, max:6, step:0.1, def:0, impact:1,
    lo:'weaker', hi:'stronger', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Registry-exclusivity / margin shock — probability', min:0, max:55, step:1, def:48, impact:0.05,
    lo:'high risk', hi:'calm', fmt:v=>Math.round(v)+'% chance' },
  { name:'Platform-launch / contract-win surprise — probability', min:0, max:90, step:1, def:20, impact:0.05,
    lo:'unlikely', hi:'likely', fmt:v=>Math.round(v)+'% chance' },
  { name:'Government digital-spend growth (Vision 2030)', min:-5, max:8, step:0.5, def:0.3, impact:1,
    lo:'weaker', hi:'stronger', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Broader Tadawul / risk appetite', min:-6, max:8, step:0.5, def:0.1, impact:1,
    lo:'weaker', hi:'stronger', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' }
],

"EMAAR": [
  { name:'Dubai residential & off-plan absorption', min:-8, max:10, step:0.5, def:1, impact:1,
    lo:'sharp depreciation', hi:'firm / tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Dubai property correction / oversupply — probability', min:0, max:55, step:1, def:30, impact:0.06,
    lo:'unlikely', hi:'likely', fmt:v=>Math.round(v)+'% chance' },
  { name:'Backlog conversion / discount compression — probability', min:0, max:90, step:1, def:50, impact:0.05,
    lo:'unlikely', hi:'likely', fmt:v=>Math.round(v)+'% chance' },
  { name:'US rates via the dirham peg', min:-5, max:8, step:0.5, def:-0.5, impact:1,
    lo:'tighter / rate headwind', hi:'easier / rate tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Recurring retail & tourism trajectory', min:-6, max:8, step:0.5, def:0.3, impact:1,
    lo:'weaker', hi:'stronger', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' }
],

"EMAARDEV": [
  { name:'Dubai residential & off-plan absorption', min:-8, max:10, step:0.5, def:1, impact:1,
    lo:'sharp depreciation', hi:'firm / tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Dubai property correction / oversupply — probability', min:0, max:55, step:1, def:30, impact:0.06,
    lo:'unlikely', hi:'likely', fmt:v=>Math.round(v)+'% chance' },
  { name:'Backlog conversion / discount compression — probability', min:0, max:90, step:1, def:50, impact:0.05,
    lo:'unlikely', hi:'likely', fmt:v=>Math.round(v)+'% chance' },
  { name:'US rates via the dirham peg', min:-5, max:8, step:0.5, def:-0.5, impact:1,
    lo:'tighter / rate headwind', hi:'easier / rate tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Development margin & pricing trajectory', min:-6, max:8, step:0.5, def:0.3, impact:1,
    lo:'margin squeeze', hi:'margin tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' }
],

"EMFD": [
  { name:'EGP/USD — impact on EMFD', min:-12, max:2, step:0.5, def:-1.5, impact:1,
    lo:'sharp depreciation', hi:'firm / tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Regional security shock — probability', min:0, max:55, step:1, def:30, impact:0.1,
    lo:'high risk', hi:'calm', fmt:v=>Math.round(v)+'% chance' },
  { name:'Project launch & sales execution — probability', min:0, max:90, step:1, def:55, impact:0.05,
    lo:'unlikely', hi:'likely', fmt:v=>Math.round(v)+'% chance' },
  { name:'Instalment collection / handover pace', min:-10, max:12, step:1, def:0, impact:0.9,
    lo:'slips', hi:'ahead of schedule', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Marassi Red Sea JV crystallises — probability', min:0, max:90, step:1, def:40, impact:0.06,
    lo:'stalls', hi:'delivers', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' }
],

"EMPOWER": [
  { name:"Terminal kitchen margin", min:-2.1, max:1.0, step:0.1, def:0, impact:5.5,
    lo:"reverts to the audited average 22.8%", hi:"holds above the modelled peak",
    fmt:v=>(24.9+v).toFixed(1)+"% terminal operating-cash margin \u2014 THE contested judgement, published both ways and never averaged: structural gives AED 2.31, full reversion to the audited 22.8% average gives 1.98. The model itself peaks at 25.4% and eases to 24.9% as the delivery channel grows" },
  { name:"Return on new restaurant capital", min:-10, max:25, step:5, def:0, impact:0.25,
    lo:"20% \u2014 payback stretches past five years", hi:"55% \u2014 the forecast years\u2019 implied average",
    fmt:v=>(30+v).toFixed(0)+"% terminal return on new capital \u2014 the base 30% is anchored on the company\u2019s own disclosed ~3-year store payback; the 55% the forecast years imply is published as the bull case, not the base" },
  { name:"Cost of capital", min:-1, max:1, step:0.25, def:0, impact:-8,
    lo:"8.5% \u2014 the CDS-basis premium blend", hi:"10.5%",
    fmt:v=>(9.5+v).toFixed(2)+"% WACC \u2014 a 12-country revenue-weighted premium blend from the UAE to Egypt to Kazakhstan, published on both the rating and CDS bases" },
  { name:"Delivery cost per delivered dollar", min:-1, max:1, step:0.25, def:0, impact:-3.5,
    lo:"aggregator economics improve", hi:"aggregators take a bigger cut",
    fmt:v=>(14.1+v).toFixed(2)+"% of delivered sales \u2014 the channel is disclosed at 44 \u2192 48 \u2192 52% of revenue and rising, so every point of aggregator cost scales with it; this line is why the margin eases rather than expands" },
  { name:"Net store openings", min:-60, max:60, step:10, def:0, impact:0.05,
    lo:"expansion stalls", hi:"the Saudi and growth-brand pipeline accelerates",
    fmt:v=>"about "+(130+v).toFixed(0)+" net new restaurants a year \u2014 the brand build grows KFC, Pizza Hut, Hardee\u2019s, Krispy Kreme and the growth brands on the company\u2019s own disclosed opening mix" }
],

"ENBD": [
  { name:'Fed / CBUAE policy-rate path (the NIM driver)', min:-6, max:6, step:0.1, def:-0.2, impact:1,
    lo:'tighter / rate headwind', hi:'easier / rate tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Dubai RE / regional geopolitical / credit shock — probability', min:0, max:55, step:1, def:40, impact:0.07,
    lo:'high risk', hi:'calm', fmt:v=>Math.round(v)+'% chance' },
  { name:'Dividend / capital-return surprise — probability', min:0, max:90, step:1, def:25, impact:0.05,
    lo:'no surprise', hi:'upside surprise', fmt:v=>Math.round(v)+'% chance' },
  { name:'UAE non-oil GDP & private-credit growth (D33)', min:-5, max:8, step:0.5, def:1, impact:1,
    lo:'demand softening', hi:'demand accelerating', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Oil price & regional system liquidity', min:-6, max:8, step:0.5, def:0.3, impact:1,
    lo:'weak / low liquidity', hi:'strong / ample liquidity', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' }
],

"ETEL": [
  { name:'EGX secular repricing + CBE easing vs. an FX-regime turn', min:-6, max:20, step:0.5, def:13.5, impact:1,
    lo:'sharp depreciation', hi:'firm / tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Approved 13–15% tariff rises land — probability', min:0, max:95, step:1, def:70, impact:0.08,
    lo:'delayed', hi:'implemented', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Vodafone Egypt (45%) profit contribution', min:-10, max:15, step:1, def:4, impact:0.7,
    lo:'declines', hi:'grows fast', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Wrapper discount →15% fair — narrowing', min:-12, max:15, step:1, def:0, impact:0.8,
    lo:'widens', hi:'narrows to fair', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Leverage / capex intensity', min:-8, max:6, step:0.5, def:0, impact:0.6,
    lo:'debt-funded build', hi:'deleveraging', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' }
],

"EXTRA": [
  { name:'SAMA / Fed policy-rate path (demand + Tasheel spread)', min:-6, max:6, step:0.1, def:0.1, impact:1,
    lo:'tighter / rate headwind', hi:'easier / rate tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Consumer / regional demand shock — probability', min:0, max:55, step:1, def:45, impact:0.07,
    lo:'high risk', hi:'calm', fmt:v=>Math.round(v)+'% chance' },
  { name:'Dividend declaration surprise — probability', min:0, max:90, step:1, def:30, impact:0.05,
    lo:'no surprise', hi:'upside surprise', fmt:v=>Math.round(v)+'% chance' },
  { name:'Non-oil GDP & Vision-2030 consumption', min:-5, max:8, step:0.5, def:0.3, impact:1,
    lo:'demand softening', hi:'demand accelerating', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Consumer-finance regulation & provisioning', min:-6, max:8, step:0.5, def:0.1, impact:1,
    lo:'weaker', hi:'stronger', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' }
],

"FAB": [
  { name:'Fed policy-rate path via the peg (the NIM driver)', min:-6, max:6, step:0.1, def:0.4, impact:1,
    lo:'tighter / rate headwind', hi:'easier / rate tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Geopolitical / regional security shock — probability', min:0, max:55, step:1, def:30, impact:0.075,
    lo:'high risk', hi:'calm', fmt:v=>Math.round(v)+'% chance' },
  { name:'Dividend / distribution surprise — probability', min:0, max:90, step:1, def:35, impact:0.05,
    lo:'no surprise', hi:'upside surprise', fmt:v=>Math.round(v)+'% chance' },
  { name:'UAE non-oil credit demand & financing growth', min:-5, max:8, step:0.5, def:0.5, impact:1,
    lo:'demand softening', hi:'demand accelerating', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Oil price & Gulf sovereign liquidity', min:-6, max:8, step:0.5, def:0.3, impact:1,
    lo:'weak / low liquidity', hi:'strong / ample liquidity', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' }
],

"FERTIGLB": [
  { name:"Terminal kitchen margin", min:-2.1, max:1.0, step:0.1, def:0, impact:5.5,
    lo:"reverts to the audited average 22.8%", hi:"holds above the modelled peak",
    fmt:v=>(24.9+v).toFixed(1)+"% terminal operating-cash margin \u2014 THE contested judgement, published both ways and never averaged: structural gives AED 2.31, full reversion to the audited 22.8% average gives 1.98. The model itself peaks at 25.4% and eases to 24.9% as the delivery channel grows" },
  { name:"Return on new restaurant capital", min:-10, max:25, step:5, def:0, impact:0.25,
    lo:"20% \u2014 payback stretches past five years", hi:"55% \u2014 the forecast years\u2019 implied average",
    fmt:v=>(30+v).toFixed(0)+"% terminal return on new capital \u2014 the base 30% is anchored on the company\u2019s own disclosed ~3-year store payback; the 55% the forecast years imply is published as the bull case, not the base" },
  { name:"Cost of capital", min:-1, max:1, step:0.25, def:0, impact:-8,
    lo:"8.5% \u2014 the CDS-basis premium blend", hi:"10.5%",
    fmt:v=>(9.5+v).toFixed(2)+"% WACC \u2014 a 12-country revenue-weighted premium blend from the UAE to Egypt to Kazakhstan, published on both the rating and CDS bases" },
  { name:"Delivery cost per delivered dollar", min:-1, max:1, step:0.25, def:0, impact:-3.5,
    lo:"aggregator economics improve", hi:"aggregators take a bigger cut",
    fmt:v=>(14.1+v).toFixed(2)+"% of delivered sales \u2014 the channel is disclosed at 44 \u2192 48 \u2192 52% of revenue and rising, so every point of aggregator cost scales with it; this line is why the margin eases rather than expands" },
  { name:"Net store openings", min:-60, max:60, step:10, def:0, impact:0.05,
    lo:"expansion stalls", hi:"the Saudi and growth-brand pipeline accelerates",
    fmt:v=>"about "+(130+v).toFixed(0)+" net new restaurants a year \u2014 the brand build grows KFC, Pizza Hut, Hardee\u2019s, Krispy Kreme and the growth brands on the company\u2019s own disclosed opening mix" }
],

"FWRY": [
  { name:'CBE rate path — impact on the discount rate', min:-8, max:8, step:0.5, def:2, impact:1,
    lo:'tighter / rate headwind', hi:'easier / rate tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Transaction throughput growth', min:-12, max:20, step:1, def:8, impact:0.8,
    lo:'growth stalls', hi:'growth accelerates', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Blended take-rate / EBITDA margin', min:-8, max:8, step:0.5, def:0, impact:1,
    lo:'compresses', hi:'expands', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'New-product / banking-services mix', min:-6, max:12, step:1, def:3, impact:0.6,
    lo:'stagnant', hi:'scaling', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Competitive fee pressure', min:-10, max:5, step:0.5, def:0, impact:0.7,
    lo:'intense', hi:'benign', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' }
],

"GBCO": [
  { name:'CBE rate cuts — ≥100 bp by October', min:0, max:90, step:1, def:50, impact:0.008,
    lo:'no cut', hi:'cut delivered', fmt:v=>Math.round(v)+'% chance' },
  { name:'MNT-Halan second closing at ≥ USD 1.4 bn — probability', min:0, max:90, step:1, def:45, impact:0.05,
    lo:'unlikely', hi:'lands', fmt:v=>Math.round(v)+'% chance' },
  { name:'Regional escalation (Iraq / Jordan spillover) — probability', min:0, max:55, step:1, def:35, impact:0.05,
    lo:'high risk', hi:'calm', fmt:v=>Math.round(v)+'% chance' },
  { name:'Auto volumes / cycle (82k vs ~200k peak)', min:-10, max:20, step:1, def:5, impact:0.8,
    lo:'trough deepens', hi:'recovery', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'GB Capital financing-book quality', min:-8, max:10, step:1, def:2, impact:0.6,
    lo:'NPLs rise', hi:'clean growth', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' }
],

"GOLD": [
  { name:'Real rates / Fed path', min:-10, max:6, step:0.5, def:-2.5, impact:1,
    lo:'tighter / rate headwind', hi:'easier / rate tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'US dollar (DXY)', min:-9, max:5, step:0.5, def:-1, impact:1,
    lo:'strong dollar', hi:'weak dollar', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Inflation / debasement', min:-5, max:6, step:0.5, def:0, impact:1,
    lo:'disinflation', hi:'inflation / debasement', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Central-bank demand', min:0, max:90, step:1, def:30, impact:0.05,
    lo:'soft', hi:'strong', fmt:v=>Math.round(v)+'% chance' },
  { name:'Geopolitical / haven bid', min:0, max:90, step:1, def:25, impact:0.05,
    lo:'high risk', hi:'calm', fmt:v=>Math.round(v)+'% chance' }
],

"HELI": [
  { name:'EGP/USD — impact on HELI', min:-12, max:2, step:0.5, def:-2, impact:1,
    lo:'sharp depreciation', hi:'firm / tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Regional security shock — probability', min:0, max:55, step:1, def:30, impact:0.1,
    lo:'high risk', hi:'calm', fmt:v=>Math.round(v)+'% chance' },
  { name:'New partnership / JDA award — probability', min:0, max:90, step:1, def:45, impact:0.05,
    lo:'unlikely', hi:'likely', fmt:v=>Math.round(v)+'% chance' },
  { name:'Partnership collections on schedule — probability', min:0, max:95, step:1, def:60, impact:0.08,
    lo:'delayed', hi:'on schedule', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Land-bank re-mark / monetisation', min:-8, max:15, step:1, def:0, impact:0.7,
    lo:'marked down', hi:'re-marked up', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' }
],

"HRHO": [
  { name:'Holdco discount — narrowing vs. widening', min:-12, max:12, step:0.5, def:-2, impact:1,
    lo:'weaker', hi:'stronger', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Investment-bank revenue cycle', min:-12, max:15, step:1, def:3, impact:0.7,
    lo:'deal drought', hi:'deal surge', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Valu / NBFI book growth & ROE', min:-8, max:15, step:1, def:5, impact:0.6,
    lo:'contraction', hi:'rapid, profitable', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Bank NXT ramp — probability', min:0, max:90, step:1, def:45, impact:0.05,
    lo:'slow', hi:'scales', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Regional capital-markets flows', min:-12, max:12, step:1, def:0, impact:0.6,
    lo:'risk-off', hi:'risk-on', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' }
],

"IHC": [
  { name:'Oil & GCC sovereign liquidity', min:-8, max:8, step:0.5, def:0.6, impact:1,
    lo:'sharp depreciation', hi:'firm / tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Regional geopolitical / security shock — probability', min:0, max:55, step:1, def:35, impact:0.1,
    lo:'high risk', hi:'calm', fmt:v=>Math.round(v)+'% chance' },
  { name:'Large M&A / deal announcement — probability', min:0, max:90, step:1, def:45, impact:0.05,
    lo:'unlikely', hi:'lands', fmt:v=>Math.round(v)+'% chance' },
  { name:'AI / tech-capital re-rating', min:-5, max:8, step:0.5, def:0.5, impact:1,
    lo:'weaker', hi:'stronger', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'UAE / US rate path (Fed via the AED peg)', min:-6, max:8, step:0.5, def:-0.6, impact:1,
    lo:'tighter / rate headwind', hi:'easier / rate tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' }
],

"INFY": [
  { name:'US & Europe IT-spending cycle', min:-8, max:10, step:0.5, def:1.5, impact:1,
    lo:'sharp depreciation', hi:'firm / tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'US recession / demand-freeze — probability', min:0, max:55, step:1, def:40, impact:0.03,
    lo:'soft', hi:'strong', fmt:v=>Math.round(v)+'% chance' },
  { name:'Mega-deal win (&gt;$0.5bn TCV) — probability', min:0, max:90, step:1, def:45, impact:0.05,
    lo:'unlikely', hi:'lands', fmt:v=>Math.round(v)+'% chance' },
  { name:'GenAI effect on pricing & margin', min:-8, max:6, step:0.5, def:-1.2, impact:1,
    lo:'margin squeeze', hi:'margin tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'USD/INR — bills USD, reports INR', min:-6, max:8, step:0.5, def:0.8, impact:1,
    lo:'weaker', hi:'stronger', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' }
],

"IQCD": [
  { name:'Petrochemical & fertilizer prices', min:-8, max:8, step:0.5, def:0.6, impact:1,
    lo:'sharp depreciation', hi:'firm / tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Regional geopolitical / security shock — probability', min:0, max:55, step:1, def:35, impact:0.1,
    lo:'high risk', hi:'calm', fmt:v=>Math.round(v)+'% chance' },
  { name:'Ammonia-7 / petchem-recovery catalyst — probability', min:0, max:90, step:1, def:30, impact:0.05,
    lo:'unlikely', hi:'likely', fmt:v=>Math.round(v)+'% chance' },
  { name:'China / global polymer demand', min:-5, max:8, step:0.5, def:0.3, impact:1,
    lo:'demand softening', hi:'demand accelerating', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Qatar / US rate path (Fed via the QAR peg)', min:-6, max:8, step:0.5, def:-0.6, impact:1,
    lo:'tighter / rate headwind', hi:'easier / rate tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' }
],

"ISPH": [
  { name:'Drug re-pricing & EGP path — the top-line driver', min:-6, max:6, step:0.1, def:0.6, impact:1,
    lo:'sharp depreciation', hi:'firm / tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'CBE rate path — finance-cost leverage', min:-5, max:8, step:0.5, def:0.3, impact:1,
    lo:'tighter / rate headwind', hi:'easier / rate tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Pharma demand & market share', min:-6, max:8, step:0.5, def:0.5, impact:1,
    lo:'demand softening', hi:'demand accelerating', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'EGP devaluation step — probability', min:0, max:55, step:1, def:35, impact:0.03,
    lo:'unlikely', hi:'likely', fmt:v=>Math.round(v)+'% chance' },
  { name:'Re-pricing round / supplier deal — probability', min:0, max:90, step:1, def:40, impact:0.05,
    lo:'unlikely', hi:'lands', fmt:v=>Math.round(v)+'% chance' }
],

"JUFO": [
  { name:'Gas-feedstock margin — subsidised vs. export parity', min:-25, max:10, step:0.5, def:-3, impact:1,
    lo:'margin squeeze', hi:'margin tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'EGP / USD translation', min:-12, max:4, step:0.5, def:-2, impact:1,
    lo:'sharp depreciation', hi:'firm / tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Gross-margin post concentrate super-cycle', min:-10, max:8, step:0.5, def:0, impact:1,
    lo:'settles low', hi:'settles high', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Volume growth (dairy + juice)', min:-8, max:15, step:1, def:5, impact:0.6,
    lo:'volumes fall', hi:'volumes surge', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Egyptian rate path (finance-cost relief)', min:-6, max:8, step:0.5, def:1, impact:0.7,
    lo:'rates high', hi:'rates fall', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' }
],

"KABO": [
  { name:'EGP/USD path — impact on Kabo', min:-6, max:8, step:0.5, def:0.5, impact:1,
    lo:'sharp depreciation', hi:'firm / tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Input-cost / freight shock — probability', min:0, max:55, step:1, def:30, impact:0.1,
    lo:'high risk', hi:'calm', fmt:v=>Math.round(v)+'% chance' },
  { name:'Land re-mark / monetisation — probability', min:0, max:90, step:1, def:15, impact:0.05,
    lo:'unlikely', hi:'likely', fmt:v=>Math.round(v)+'% chance' },
  { name:'Alexandria land monetised — probability', min:0, max:90, step:1, def:30, impact:0.1,
    lo:'never crystallises', hi:'sold at mark', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Core clothing earnings recovery', min:-10, max:12, step:1, def:0, impact:0.6,
    lo:'stays depressed', hi:'recovers', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' }
],

"KAKAO": [
  { name:'Talk Biz — ad & commerce growth', min:-8, max:10, step:0.5, def:1, impact:1,
    lo:'sharp depreciation', hi:'firm / tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Ad-market / regulatory setback — probability', min:0, max:55, step:1, def:25, impact:0.06,
    lo:'unlikely', hi:'likely', fmt:v=>Math.round(v)+'% chance' },
  { name:'Discount compression / value-up — probability', min:0, max:90, step:1, def:35, impact:0.05,
    lo:'unlikely', hi:'likely', fmt:v=>Math.round(v)+'% chance' },
  { name:'AI traction — Kanana & ChatGPT', min:-5, max:8, step:0.5, def:0.5, impact:1,
    lo:'weaker', hi:'stronger', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Korean won — overseas content FX', min:-6, max:8, step:0.5, def:0, impact:1,
    lo:'sharp depreciation', hi:'firm / tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' }
],

"LCSW": [
  { name:'EGP/USD — impact on Lecico', min:-6, max:10, step:0.5, def:3.3, impact:1,
    lo:'sharp depreciation', hi:'firm / tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Energy cost — gas & diesel', min:-4, max:1.5, step:0.25, def:-0.8, impact:0.05,
    lo:'unlikely', hi:'likely', fmt:v=>Math.round(v)+'% chance' },
  { name:'Export demand & margin recovery', min:-3, max:6, step:0.25, def:1.2, impact:0.05,
    lo:'soft', hi:'strong', fmt:v=>Math.round(v)+'% chance' },
  { name:'Profit-to-cash conversion', min:-8, max:12, step:1, def:0, impact:0.8,
    lo:'deteriorates', hi:'improves', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Domestic construction / tile demand', min:-10, max:12, step:1, def:2, impact:0.6,
    lo:'weak', hi:'strong', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' }
],

"LGES": [
  { name:'EV-battery demand — volumes', min:-10, max:8, step:0.1, def:-2.2, impact:1,
    lo:'sharp depreciation', hi:'firm / tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'AMPC / IRA policy cut — probability', min:0, max:55, step:1, def:38, impact:0.15,
    lo:'no cut', hi:'cut delivered', fmt:v=>Math.round(v)+'% chance' },
  { name:'Major OEM / ESS supply win — probability', min:0, max:90, step:1, def:28, impact:0.05,
    lo:'unlikely', hi:'likely', fmt:v=>Math.round(v)+'% chance' },
  { name:'Energy storage & AI-datacentre demand', min:-5, max:10, step:0.1, def:2.2, impact:1,
    lo:'demand softening', hi:'demand accelerating', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Korean won — USD translation', min:-6, max:8, step:0.1, def:0.4, impact:1,
    lo:'weaker', hi:'stronger', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' }
],

"LULU": [
  { name:'Sales density — the crux', min:-6, max:6, step:0.1, def:0, impact:1,
    lo:'sharp depreciation', hi:'firm / tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Hormuz normalisation holds — deferred non-food demand returns', min:5, max:95, step:1, def:55, impact:0.025,
    lo:'soft', hi:'strong', fmt:v=>Math.round(v)+'% chance' },
  { name:'Interim dividend cut toward the 75%-of-earnings policy', min:5, max:95, step:1, def:25, impact:0.05,
    lo:'no surprise', hi:'upside surprise', fmt:v=>Math.round(v)+'% chance' },
  { name:'The mature-store cost programme', min:-3, max:3, step:0.1, def:0, impact:1,
    lo:'weaker', hi:'stronger', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'CBUAE / Fed policy-rate path — the carry', min:-3, max:3, step:0.1, def:0, impact:1,
    lo:'tighter / rate headwind', hi:'easier / rate tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' }
],

"MAADEN": [
  { name:'DAP / phosphate price path', min:-8, max:8, step:0.5, def:0.5, impact:1,
    lo:'sharp depreciation', hi:'firm / tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Global recession / demand shock — probability', min:0, max:55, step:1, def:40, impact:0.045,
    lo:'high risk', hi:'calm', fmt:v=>Math.round(v)+'% chance' },
  { name:'Commodity price spike (DAP / aluminium / gold) — probability', min:0, max:90, step:1, def:25, impact:0.05,
    lo:'unlikely', hi:'likely', fmt:v=>Math.round(v)+'% chance' },
  { name:'LME aluminium & gold (base-metals leg)', min:-5, max:8, step:0.5, def:0.5, impact:1,
    lo:'weaker', hi:'stronger', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'SAMA / Fed rate & China demand', min:-6, max:8, step:0.5, def:0, impact:1,
    lo:'tighter / rate headwind', hi:'easier / rate tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' }
],

"MODON": [
  { name:"Beta \u2014 how much the share moves with the market", min:-0.65, max:0.65, step:0.05, def:0, impact:-19.05,
    lo:"1.09 \u2014 the bottom of the measured 90% range", hi:"2.40 \u2014 the top of it",
    fmt:v=>(1.75+v).toFixed(2)+" beta \u2014 THE lever in this edition and the one that flipped the verdict. Measured against the exchange's official index at 1.75 (standard error 0.40, 253 weekly readings over 4.9 years), corrected for thin trading because 84.75% of the shares sit with one holder. The two earlier editions used 1.03 from a basket built out of our own coverage, and read the stock as cheap. The range here is wide because the measurement is: this is the honest uncertainty, not a decoration. Beta and value move in OPPOSITE directions: on the study\u0027s own beta grid the cash-flow lens falls about 21% for every half-point of beta, so the top of the measured range takes the answer DOWN" },
  { name:"Terminal cost of capital", min:-1.0, max:1.0, step:0.25, def:0, impact:-3.75,
    lo:"10.9% \u2014 a maturing, deleveraging developer", hi:"12.9%",
    fmt:v=>(11.92+v).toFixed(2)+"% terminal WACC \u2014 68.7% of enterprise value sits in the terminal block. The explicit-period rate is 11.14%; the terminal rate derives its debt weight (8.0%) from the model's own FY2030 balance sheet rather than assuming one. Note that terminal return on capital (8.5%) now sits BELOW this rate, so faster terminal growth SUBTRACTS value" },
  { name:"The sales machine \u2014 % of the base plan delivered", min:0, max:120, step:10, def:100, impact:0.006,
    lo:"run-off: nothing new is ever sold (AED 2.64)", hi:"120% of plan",
    fmt:v=>v.toFixed(0)+"% of the base new-sales path (AED 12\u219230\u219226\u219223\u219221bn) \u2014 THE contested judgement, computed both ways and never averaged. At 0% the DCF reads AED 2.64; the base plan reads 3.54" },
  { name:"Backlog conversion pace", min:-8, max:8, step:1, def:0, impact:0.025,
    lo:"24% a year by FY2030 \u2014 handovers slip", hi:"40% \u2014 handovers accelerate",
    fmt:v=>(32+v).toFixed(0)+"% terminal-year conversion of the opening backlog \u2014 the schedule that turns the AED 65.4bn contracted book into revenue. Faster conversion pulls cash forward but drains the terminal book that feeds the terminal year; the study prices both effects" },
  { name:"Receivable days", min:-60, max:60, step:10, def:0, impact:0.004,
    lo:"collections accelerate to ~310 days", hi:"stretch to ~430 days",
    fmt:v=>(370+v).toFixed(0)+" days of revenue in closing receivables by FY2030 \u2014 the H1-2026 balance sheet carries 440 days, and the study's working-capital build walks it down a disclosed-anchored path rather than assuming it away" },
  { name:"Development margin", min:-3, max:3, step:0.5, def:0, impact:0.14,
    lo:"35% \u2014 cost inflation eats the recognised book", hi:"41% \u2014 H1-2026 level holds",
    fmt:v=>(38+v).toFixed(1)+"% blended development gross margin by FY2030 \u2014 the recognised-revenue margin the model glides from the 41% H1-2026 actual as older, richer land inventory washes through" }
],

"NVDA": [
  { name:'AI data-center capex cycle', min:-8, max:8, step:0.5, def:0.5, impact:1,
    lo:'sharp depreciation', hi:'firm / tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'AI-capex fatigue / bubble scare — probability', min:0, max:55, step:1, def:30, impact:0.1,
    lo:'unlikely', hi:'likely', fmt:v=>Math.round(v)+'% chance' },
  { name:'Major partnership / mega-order — probability', min:0, max:90, step:1, def:45, impact:0.05,
    lo:'unlikely', hi:'likely', fmt:v=>Math.round(v)+'% chance' },
  { name:'Gross margin — Blackwell &rarr; Rubin pricing', min:-5, max:8, step:0.5, def:0.3, impact:1,
    lo:'margin squeeze', hi:'margin tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'US 10-year real yield / rate path', min:-6, max:8, step:0.5, def:0.6, impact:1,
    lo:'tighter / rate headwind', hi:'easier / rate tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' }
],

"OCDI": [
  { name:'EGP/USD — impact on OCDI', min:-12, max:2, step:0.5, def:-2, impact:1,
    lo:'sharp depreciation', hi:'firm / tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Regional security shock — probability', min:0, max:55, step:1, def:30, impact:0.1,
    lo:'high risk', hi:'calm', fmt:v=>Math.round(v)+'% chance' },
  { name:'Project launch & sales execution — probability', min:0, max:90, step:1, def:55, impact:0.05,
    lo:'unlikely', hi:'likely', fmt:v=>Math.round(v)+'% chance' },
  { name:'Collection pace / net-debt sensitivity', min:-12, max:12, step:1, def:0, impact:0.9,
    lo:'slips (debt bites)', hi:'ahead', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Eastvale + New Sphinx JV ramp — probability', min:0, max:90, step:1, def:45, impact:0.06,
    lo:'stalls', hi:'ramps', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' }
],

"OIH": [
  { name:'EGP/USD path — impact on OIH', min:-8, max:10, step:0.5, def:1, impact:1,
    lo:'sharp depreciation', hi:'firm / tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Geopolitical / tourism setback — probability', min:0, max:55, step:1, def:30, impact:0.12,
    lo:'high risk', hi:'calm', fmt:v=>Math.round(v)+'% chance' },
  { name:'Pyramids ramp / DPRK repatriation catalyst — probability', min:0, max:90, step:1, def:35, impact:0.05,
    lo:'unlikely', hi:'likely', fmt:v=>Math.round(v)+'% chance' },
  { name:'Holding-company discount narrowing', min:-12, max:15, step:1, def:0, impact:0.7,
    lo:'widens', hi:'narrows', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Pyramids concession DCF realisation — probability', min:0, max:90, step:1, def:45, impact:0.06,
    lo:'underdelivers', hi:'delivers', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' }
],

"ORAS": [
  { name:'US infrastructure & data-center capex — impact on ORAS', min:-8, max:10, step:0.5, def:0, impact:1,
    lo:'sharp depreciation', hi:'firm / tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Geopolitical / receivables setback — probability', min:0, max:55, step:1, def:30, impact:0.1,
    lo:'high risk', hi:'calm', fmt:v=>Math.round(v)+'% chance' },
  { name:'OCI deal / major contract award — probability', min:0, max:90, step:1, def:45, impact:0.05,
    lo:'unlikely', hi:'lands', fmt:v=>Math.round(v)+'% chance' },
  { name:'Annual contract-award pace ($bn)', min:-12, max:15, step:1, def:3, impact:0.8,
    lo:'awards shrink', hi:'awards grow', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Net cash genuinely distributable', min:-10, max:8, step:0.5, def:0, impact:0.7,
    lo:'more is bonding', hi:'more is free', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' }
],

"ORHD": [
  { name:'EGP/USD — impact on ORHD', min:-12, max:2, step:0.5, def:-1.5, impact:1,
    lo:'sharp depreciation', hi:'firm / tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Regional security shock — probability', min:0, max:55, step:1, def:30, impact:0.1,
    lo:'high risk', hi:'calm', fmt:v=>Math.round(v)+'% chance' },
  { name:'Project launch & sales execution — probability', min:0, max:90, step:1, def:55, impact:0.05,
    lo:'unlikely', hi:'likely', fmt:v=>Math.round(v)+'% chance' },
  { name:'El Gouna land-bank ascribed value', min:-8, max:18, step:1, def:0, impact:0.8,
    lo:'near zero', hi:'full RNAV', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Hotel + town-management NOI', min:-8, max:12, step:1, def:2, impact:0.6,
    lo:'soft season', hi:'strong recurring', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' }
],

"ORWE": [
  { name:'EGP path — devaluation vs. firm pound', min:-8, max:12, step:0.5, def:1.5, impact:1,
    lo:'sharp depreciation', hi:'firm / tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Export rebate phase-out', min:-8, max:4, step:0.5, def:-1, impact:0.8,
    lo:'cut deeper', hi:'retained', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'US tariff treatment', min:-10, max:6, step:0.5, def:0, impact:0.8,
    lo:'tariffs rise', hi:'tariffs ease', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Cash conversion (from ~58%)', min:-8, max:12, step:1, def:0, impact:0.7,
    lo:'deteriorates', hi:'improves', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Polypropylene / input cost', min:-8, max:8, step:0.5, def:0, impact:0.7,
    lo:'costs spike', hi:'costs ease', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' }
],

"PHAR": [
  { name:"Biosimilar revenue by FY2030", min:0, max:120, step:10, def:0, impact:0.60,
    lo:"the plant sells nothing (the published case)", hi:"USD 120m a year",
    fmt:v=>"USD "+v.toFixed(0)+"m a year of revenue from the new plant by FY2030 \u2014 the study charges the plant's depreciation and its interest but credits it with ZERO revenue, so this is the single lever that is not in the published number at all. About USD "+120+"m closes the whole gap to the market price" },
  { name:"Credit-loss and provision charge", min:-2.75, max:1.5, step:0.25, def:0, impact:0.50,
    lo:"normalises to 2.5% of revenue", hi:"runs at the three-year mean 6.52%",
    fmt:v=>(5.25+v).toFixed(2)+"% of revenue \u2014 THE contested judgement, published both ways and never averaged. Frame A carries 5.25% permanently; Frame B decays to 2.5%. The first quarter of 2026 booked NO credit loss at all, which the auditor qualified, so the question is deferred rather than settled" },
  { name:"Terminal risk-free rate", min:-1.5, max:1.5, step:0.25, def:0, impact:0.85,
    lo:"9.0% \u2014 real rate at long-run GDP growth", hi:"12.0%",
    fmt:v=>(10.5+v).toFixed(2)+"% terminal risk-free rate \u2014 the widest single lever in the study and the one input still resting on an unsourced convention: a sourced 5% inflation target plus an asserted 5.5-point real rate, which sits above Egypt's own long-run real growth" },
  { name:"Domestic price per pack \u2014 annual step", min:-3, max:3, step:0.5, def:0, impact:0.45,
    lo:"the administered price lags inflation", hi:"it keeps pace",
    fmt:v=>(v>=0?"+":"\u2212")+Math.abs(v).toFixed(1)+"pp on the forecast domestic price path. The company realised +12.59% on its own preparations in FY2025 \u2014 measured properly, after separating out product it manufactures under contract \u2014 against a domestic price the Egyptian Drug Authority administers" },
  { name:"Associate contribution", min:-200, max:100, step:25, def:0, impact:0.30,
    lo:"the quarter's run-rate (EGP 52m)", hi:"the best disclosed year",
    fmt:v=>"EGP "+(250+v).toFixed(0)+"m normalised \u2014 worth about EGP "+((250+v)*11/168.75575).toFixed(2)+" a share in the bridge at 11x. The three disclosed years average 246; the first quarter of 2026 annualises to 52, but the auditor states two holdings' statements were not received, so that quarter is evidence rather than a run-rate" }
],

"PHDC": [
  { name:"EGP/USD \u2014 impact on fair value", min:-6, max:2, step:0.5, def:-2.5, impact:1.8,
    lo:"sharp depreciation", hi:"EGP firm / tailwind",
    fmt:v=>(v>=0?"+":"\u2212")+Math.abs(v).toFixed(1)+"% / quarter" },
  { name:"Mortgage / financing rate", min:-3, max:3, step:0.5, def:0, impact:1.2,
    lo:"rates rising", hi:"rates easing",
    fmt:v=>(-v>=0?"+":"\u2212")+Math.abs(v).toFixed(1)+"pp this cycle" },
  { name:"Geopolitical risk", min:0, max:60, step:5, def:30, impact:0.12,
    lo:"high tension", hi:"calm",
    fmt:v=>Math.round(60-v)+"% risk \u00b7 \u221212% if it hits" },
  { name:"New launch lands", min:0, max:100, step:5, def:55, impact:0.08,
    lo:"unlikely", hi:"likely",
    fmt:v=>Math.round(v)+"% \u00b7 +8% if it lands" },
  { name:"Tourism / foreign demand", min:-15, max:15, step:1, def:0, impact:0.15,
    lo:"demand softening", hi:"demand accelerating",
    fmt:v=>(v>=0?"+":"\u2212")+Math.abs(v).toFixed(0)+"% YoY" }
],

"PLATINUM": [
  { name:'Real rates / Fed path', min:-10, max:6, step:0.5, def:-2.5, impact:1,
    lo:'tighter / rate headwind', hi:'easier / rate tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'US dollar (DXY)', min:-9, max:5, step:0.5, def:-1, impact:1,
    lo:'strong dollar', hi:'weak dollar', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Gold price / Pt-Au ratio', min:-5, max:8, step:0.5, def:2, impact:1,
    lo:'gold lower / ratio pinned', hi:'gold higher / ratio re-rates', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Reverse Pt\u2192Pd substitution accelerates', min:0, max:90, step:1, def:35, impact:0.05,
    lo:'high risk', hi:'calm', fmt:v=>Math.round(v)+'% chance' },
  { name:'SA supply shock / physical squeeze', min:0, max:90, step:1, def:30, impact:0.05,
    lo:'high risk', hi:'calm', fmt:v=>Math.round(v)+'% chance' }
],

"PRDC": [
  { name:'EGP/USD — impact on PRDC', min:-12, max:2, step:0.5, def:-2.1, impact:1,
    lo:'sharp depreciation', hi:'firm / tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Regional security shock — probability', min:0, max:55, step:1, def:30, impact:0.1,
    lo:'high risk', hi:'calm', fmt:v=>Math.round(v)+'% chance' },
  { name:'Land monetisation & sales velocity — probability', min:0, max:90, step:1, def:55, impact:0.05,
    lo:'unlikely', hi:'likely', fmt:v=>Math.round(v)+'% chance' },
  { name:'Holdco / minority discount narrowing', min:-12, max:15, step:1, def:0, impact:0.7,
    lo:'widens', hi:'narrows', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Collection / delivery pace', min:-10, max:12, step:1, def:0, impact:0.8,
    lo:'slips', hi:'ahead', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' }
],

"QGTS": [
  { name:'US / global rate path — the discount-rate driver', min:-6, max:6, step:0.1, def:0.3, impact:1,
    lo:'tighter / rate headwind', hi:'easier / rate tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'LNG demand growth & fleet utilisation', min:-5, max:8, step:0.5, def:0.3, impact:1,
    lo:'demand softening', hi:'demand accelerating', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Charter-market tone & Brent / energy complex', min:-6, max:8, step:0.5, def:0.2, impact:1,
    lo:'weaker', hi:'stronger', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Strait-of-Hormuz / geopolitical shock — probability', min:0, max:55, step:1, def:30, impact:0.016,
    lo:'high risk', hi:'calm', fmt:v=>Math.round(v)+'% chance' },
  { name:'Charter renewal / newbuild-award surprise — probability', min:0, max:90, step:1, def:30, impact:0.05,
    lo:'unlikely', hi:'likely', fmt:v=>Math.round(v)+'% chance' }
],

"QNB": [
  { name:'QCB policy-rate path (Fed-linked; the NIM driver)', min:-6, max:6, step:0.1, def:-0.6, impact:1,
    lo:'tighter / rate headwind', hi:'easier / rate tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Regional geopolitical / asset-quality shock — probability', min:0, max:55, step:1, def:35, impact:0.08,
    lo:'high risk', hi:'calm', fmt:v=>Math.round(v)+'% chance' },
  { name:'Dividend / capital-return surprise — probability', min:0, max:90, step:1, def:30, impact:0.05,
    lo:'no surprise', hi:'upside surprise', fmt:v=>Math.round(v)+'% chance' },
  { name:'Regional private-credit & balance-sheet growth', min:-5, max:8, step:0.5, def:0.5, impact:1,
    lo:'demand softening', hi:'demand accelerating', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Oil & LNG price / regional system liquidity', min:-6, max:8, step:0.5, def:0.5, impact:1,
    lo:'weak / low liquidity', hi:'strong / ample liquidity', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' }
],

"RAYA": [
  { name:'EGX flows & holdco re-rating', min:-8, max:10, step:0.5, def:0.4, impact:1,
    lo:'sharp depreciation', hi:'firm / tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'EGP devaluation step / FX shock — probability', min:0, max:55, step:1, def:35, impact:0.09,
    lo:'high risk', hi:'calm', fmt:v=>Math.round(v)+'% chance' },
  { name:'Aman capital raise / stake sale / IPO — probability', min:0, max:90, step:1, def:30, impact:0.05,
    lo:'unlikely', hi:'lands', fmt:v=>Math.round(v)+'% chance' },
  { name:'Aman & RIT growth — consumer & digital', min:-5, max:8, step:0.5, def:1, impact:1,
    lo:'weaker', hi:'stronger', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Egyptian pound — EGP/USD translation', min:-6, max:8, step:0.5, def:-1, impact:1,
    lo:'sharp depreciation', hi:'firm / tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' }
],

"RELIANCE": [
  { name:'Jio ARPU / tariff & 5G-broadband monetisation', min:-8, max:10, step:0.5, def:0.8, impact:1,
    lo:'sharp depreciation', hi:'firm / tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Geopolitical / crude-spike shock — probability', min:0, max:55, step:1, def:35, impact:0.03,
    lo:'high risk', hi:'calm', fmt:v=>Math.round(v)+'% chance' },
  { name:'Jio Platforms IPO / value-crystallisation — probability', min:0, max:90, step:1, def:55, impact:0.05,
    lo:'unlikely', hi:'likely', fmt:v=>Math.round(v)+'% chance' },
  { name:'O2C refining & petrochemical margin', min:-5, max:8, step:0.5, def:0.2, impact:1,
    lo:'margin squeeze', hi:'margin tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'India rate path / Nifty foreign-flow path', min:-6, max:8, step:0.5, def:-0.3, impact:1,
    lo:'tighter / rate headwind', hi:'easier / rate tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' }
],

"RIBL": [
  { name:'SAMA / Fed policy-rate path (the NIM driver)', min:-6, max:6, step:0.1, def:0.2, impact:1,
    lo:'tighter / rate headwind', hi:'easier / rate tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Oil / geopolitical / credit-event shock — probability', min:0, max:55, step:1, def:45, impact:0.06,
    lo:'high risk', hi:'calm', fmt:v=>Math.round(v)+'% chance' },
  { name:'Dividend declaration surprise — probability', min:0, max:90, step:1, def:30, impact:0.05,
    lo:'no surprise', hi:'upside surprise', fmt:v=>Math.round(v)+'% chance' },
  { name:'Non-oil GDP & Vision 2030 credit demand', min:-5, max:8, step:0.5, def:0.3, impact:1,
    lo:'demand softening', hi:'demand accelerating', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Oil price & fiscal impulse (system liquidity)', min:-6, max:8, step:0.5, def:0.1, impact:1,
    lo:'weak / low liquidity', hi:'strong / ample liquidity', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' }
],

"RIYADHCABLE": [
  { name:"Sustained gross margin \u2014 the crux", min:14.0, max:16.0, step:0.25, def:15.26, impact:31.1,
    lo:"14.0% \u2014 a further competitive squeeze", hi:"16.0% \u2014 the FY2025 peak holds",
    fmt:v=>v.toFixed(2)+"% sustained gross margin \u2014 the study\u0027s central contested judgement. The business is a metal converter, so the margin is an OUTPUT: the cash-flow value runs SAR 108.5 at 14.0% to SAR 139.6 at 16.0%, and on the reviewed H1-2026 actual of 15.26% it is 127.91. It moves the answer more than any operating input, which is why it is computed BOTH ways and never averaged" },
  { name:"Metal price path", min:-15, max:15, step:5, def:0, impact:-22.7,
    lo:"15% below the flat base path", hi:"15% above it",
    fmt:v=>(v>=0?"+":"\u2212")+Math.abs(v).toFixed(0)+"% on the copper/aluminium price path. A metal converter\u0027s margin DILUTES when metal rises \u2014 the spread is fixed per tonne over a bigger denominator \u2014 so the cash-flow value runs SAR 139.3 at \u221215% to SAR 116.6 at +15%. Metals are ~95% of the cost of sales and hedged, but a sustained move still moves the reported margin" },
  { name:"Terminal growth", min:2.0, max:6.0, step:0.5, def:4.0, impact:32.0,
    lo:"2.0%", hi:"6.0%",
    fmt:v=>v.toFixed(1)+"% terminal growth. Across the study\u0027s own grid the cash-flow value runs SAR 104.9 at 2.0% to SAR 176.7 at 6.0% at the published cost of capital. Terminal value is 81% of enterprise value, so this input carries more of the answer than most operating assumptions below it" },
  { name:"Cable volume growth", min:-10, max:10, step:5, def:0, impact:21.6,
    lo:"10% below the tonnage path", hi:"10% above it",
    fmt:v=>(v>=0?"+":"\u2212")+Math.abs(v).toFixed(0)+"% on the cable-tonnage volume path \u2014 SAR 117.1 at \u221210% to SAR 138.7 at +10% on the cash-flow lens. FY2026 volume growth near 10% is anchored on the reviewed H1-2026 disclosure that revenue rose 9.5% on volume, with metal prices roughly flat" }
],

"RMDA": [
  { name:'CBE facility-cost path (Kd glide)', min:-3, max:3, step:0.1, def:-0.7, impact:1,
    lo:'sharp depreciation', hi:'firm / tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'UCP/MEC receivable recovery — probability', min:0, max:60, step:1, def:20, impact:0.01,
    lo:'unlikely', hi:'likely', fmt:v=>Math.round(v)+'% chance' },
  { name:'New product-portfolio acquisition — probability', min:5, max:70, step:1, def:35, impact:0.05,
    lo:'unlikely', hi:'likely', fmt:v=>Math.round(v)+'% chance' },
  { name:'NWC normalisation speed', min:-3, max:3, step:0.1, def:0.5, impact:1,
    lo:'weaker', hi:'stronger', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Export & tender growth', min:-3, max:3, step:0.1, def:0.3, impact:1,
    lo:'weaker', hi:'stronger', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' }
],

"SABIC": [
  { name:'Product–feedstock (PE/naphtha) spread path', min:-8, max:8, step:0.5, def:0, impact:1,
    lo:'sharp depreciation', hi:'firm / tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Global recession / demand shock — probability', min:0, max:55, step:1, def:30, impact:0.06,
    lo:'high risk', hi:'calm', fmt:v=>Math.round(v)+'% chance' },
  { name:'China stimulus / capacity rationalisation — probability', min:0, max:90, step:1, def:30, impact:0.05,
    lo:'unlikely', hi:'likely', fmt:v=>Math.round(v)+'% chance' },
  { name:'Oil / naphtha & global industrial demand', min:-5, max:8, step:0.5, def:0, impact:1,
    lo:'demand softening', hi:'demand accelerating', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'SAMA / Fed rate path (via the peg)', min:-6, max:8, step:0.5, def:0, impact:1,
    lo:'tighter / rate headwind', hi:'easier / rate tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' }
],

"SALIK": [
  { name:'CBUAE / Fed policy-rate path', min:-3, max:3, step:0.1, def:-0.2, impact:1,
    lo:'tighter / rate headwind', hi:'easier / rate tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Hormuz re-escalation — probability the June MoU collapses', min:0, max:55, step:1, def:45, impact:0.04,
    lo:'high risk', hi:'calm', fmt:v=>Math.round(v)+'% chance' },
  { name:'The board trims the 100% payout to fund the RTA instalments', min:40, max:95, step:1, def:75, impact:0.05,
    lo:'no surprise', hi:'upside surprise', fmt:v=>Math.round(v)+'% chance' },
  { name:'Dubai traffic normalisation as the ceasefire holds', min:-3, max:3, step:0.1, def:-0.1, impact:1,
    lo:'weaker', hi:'stronger', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Dubai resident population & visitor arrivals', min:-3, max:5, step:0.1, def:0.3, impact:1,
    lo:'weaker', hi:'stronger', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' }
],

"SAMSUNG": [
  { name:'Memory pricing — DRAM / NAND ASPs', min:-15, max:20, step:0.5, def:5.2, impact:1,
    lo:'sharp depreciation', hi:'firm / tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Memory-oversupply scare — probability', min:0, max:55, step:1, def:30, impact:0.09,
    lo:'unlikely', hi:'likely', fmt:v=>Math.round(v)+'% chance' },
  { name:'HBM4 qualification & AI win — probability', min:0, max:90, step:1, def:45, impact:0.05,
    lo:'unlikely', hi:'likely', fmt:v=>Math.round(v)+'% chance' },
  { name:'AI datacentre capex — memory demand', min:-8, max:12, step:0.5, def:1.2, impact:1,
    lo:'demand softening', hi:'demand accelerating', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Korean won — USD / KRW translation', min:-6, max:8, step:0.5, def:0.5, impact:1,
    lo:'weaker', hi:'stronger', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' }
],

"SAVOLA": [
  { name:"Panda sales density \u2014 the crux", min:0, max:100, step:10, def:100, impact:0.109,
    lo:"0 \u2014 the erosion never fades (Framing B)", hi:"100 \u2014 density stabilises (Framing A)",
    fmt:v=>v.toFixed(0)+"% of the density recovery delivered. This is the study\u0027s central contested judgement and it is computed BOTH ways, never averaged: let density stabilise as the store-refresh programme and e-commerce mature and the cash-flow lens is SAR 24.99; hold the measured erosion forever \u2014 \u22126% then \u22123% a year \u2014 and it is 19.63" },
  { name:"Panda store cadence (net new stores a year)", min:8, max:20, step:2, def:20, impact:0.924,
    lo:"8 \u2014 the observed H1-2026 run-rate", hi:"20 \u2014 company guidance",
    fmt:v=>v.toFixed(0)+" net new stores a year. Company guidance is 20-plus and FY2025 delivered 18 net, but only 4 opened in the first half of 2026 \u2014 so the guidance base needs 16 in the second half. At the observed run-rate the cash-flow lens is SAR 19.53 against 24.99 on guidance; fewer stores also raise less lease debt, which the model carries" },
  { name:"Terminal growth", min:1.5, max:3.5, step:0.25, def:2.5, impact:3.10,
    lo:"1.5%", hi:"3.5%",
    fmt:v=>v.toFixed(2)+"% terminal growth. Across the study\u0027s own grid the cash-flow value runs SAR 23.50 at 1.5% to SAR 26.97 at 3.5% at the published cost of capital. Terminal value is 79% of enterprise value \u2014 higher than the first edition because charging the full lease additions back-loads the explicit years \u2014 so this input carries more of the answer than most operating assumptions" },
  { name:"Terminal return on capital", min:9.5, max:11.0, step:0.25, def:10.07, impact:2.07,
    lo:"9.5% \u2014 competition erodes the spread", hi:"11.0% \u2014 brands and shelf position hold",
    fmt:v=>v.toFixed(2)+"% terminal return on invested capital. The base is not assumed \u2014 it is COMPUTED from the model\u0027s own fifth forecast year (10.07%), which is why the first edition\u0027s 10.5% input was retired to a labelled variant worth SAR 25.49 on the cash-flow lens. A terminal return only modestly above the 8.42% terminal cost of capital is the honest reading" }
],

"SCEM": [
  { name:"EBITDA margin vs the kiln build", min:-4, max:4, step:0.5, def:0, impact:3.40,
    lo:"2pp worse than modelled", hi:"2pp better",
    fmt:v=>(v>=0?"+":"\u2212")+Math.abs(v).toFixed(1)+"pp on the built margin (FY2026E lands at 30.1% as an OUTPUT, not an input)" },
  { name:"Kiln utilisation, FY2027E", min:61.7, max:81.7, step:0.5, def:71.7, impact:2.00,
    lo:"62% \u2014 the revived capacity bites", hi:"82% \u2014 exports absorb the surplus",
    fmt:v=>v.toFixed(1)+"% of the 2.57Mt kiln \u2014 the build runs 71.0% in FY2025A to 79.1% by FY2030E" },
  { name:"Net cash on the balance sheet", min:3.43, max:6.43, step:0.25, def:4.93, impact:6.00,
    lo:"EGP 3.4bn", hi:"EGP 6.4bn",
    fmt:v=>"EGP "+v.toFixed(2)+"bn at the valuation date \u2014 43% of the market capitalisation, and the largest single sensitivity in the study" },
  { name:"CBE easing \u2014 cost of capital", min:0, max:4, step:0.25, def:0, impact:1.60,
    lo:"today\u2019s money (28.30% WACC)", hi:"4pp of easing (24.30%)",
    fmt:v=>(28.30-v).toFixed(2)+"% explicit WACC \u2014 easing "+v.toFixed(2)+"pp" },
  { name:"Terminal growth \u2014 runs BACKWARDS", min:3, max:7, step:0.25, def:5, impact:-1.75,
    lo:"3% terminal growth", hi:"7% terminal growth",
    fmt:v=>v.toFixed(2)+"% \u2014 more growth SUBTRACTS value here, because terminal ROIC of 9.3% sits below the 19.0% terminal cost of capital" }
],

"SILVER": [
  { name:'Real rates / Fed path', min:-10, max:6, step:0.5, def:-2.5, impact:1,
    lo:'tighter / rate headwind', hi:'easier / rate tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'US dollar (DXY)', min:-9, max:5, step:0.5, def:-1, impact:1,
    lo:'strong dollar', hi:'weak dollar', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Gold price / gold-silver ratio', min:-5, max:8, step:0.5, def:3, impact:1,
    lo:'disinflation', hi:'inflation / debasement', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Physical squeeze / inventory shock', min:0, max:90, step:1, def:25, impact:0.05,
    lo:'high risk', hi:'calm', fmt:v=>Math.round(v)+'% chance' },
  { name:'Geopolitical / haven bid', min:0, max:90, step:1, def:25, impact:0.05,
    lo:'high risk', hi:'calm', fmt:v=>Math.round(v)+'% chance' }
],

"SNB": [
  { name:'SAMA / Fed policy-rate path (the NIM driver)', min:-6, max:6, step:0.1, def:0.4, impact:1,
    lo:'tighter / rate headwind', hi:'easier / rate tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Oil / geopolitical / credit shock — probability', min:0, max:55, step:1, def:35, impact:0.06,
    lo:'high risk', hi:'calm', fmt:v=>Math.round(v)+'% chance' },
  { name:'Dividend / payout surprise — probability', min:0, max:90, step:1, def:35, impact:0.05,
    lo:'no surprise', hi:'upside surprise', fmt:v=>Math.round(v)+'% chance' },
  { name:'Vision 2030 credit demand & financing growth', min:-5, max:8, step:0.5, def:0.5, impact:1,
    lo:'demand softening', hi:'demand accelerating', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Oil price & fiscal impulse (system liquidity)', min:-6, max:8, step:0.5, def:0.3, impact:1,
    lo:'weak / low liquidity', hi:'strong / ample liquidity', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' }
],

"STC": [
  { name:'SAMA / Fed policy-rate path (the discount-rate channel)', min:-3, max:3, step:0.1, def:0.1, impact:1,
    lo:'tighter / rate headwind', hi:'easier / rate tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Competitive intensity / price-war risk — probability', min:0, max:45, step:1, def:35, impact:0.02,
    lo:'high risk', hi:'calm', fmt:v=>Math.round(v)+'% chance' },
  { name:'Dividend policy step-up — probability', min:0, max:70, step:1, def:25, impact:0.05,
    lo:'no surprise', hi:'upside surprise', fmt:v=>Math.round(v)+'% chance' },
  { name:'KSA consumer (CBU) ARPU & data monetization', min:-1, max:2, step:0.1, def:0.3, impact:1,
    lo:'weaker', hi:'stronger', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'5G/FTTH capex intensity (the dividend-cover swing)', min:-1.5, max:1.5, step:0.1, def:0, impact:1,
    lo:'weaker', hi:'stronger', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' }
],

"SWDY": [
  { name:"Working capital / revenue", min:17, max:23, step:0.5, def:19.9, impact:-1.07,
    lo:"collects to 17% of revenue", hi:"slips back to 23%",
    fmt:v=>v.toFixed(1)+"% of revenue \u2014 the cash the growth has to fund before any of it reaches an owner; 19.9% is the audited FY2025 level" },
  { name:"Segment margins", min:-15, max:15, step:1, def:0, impact:0.78,
    lo:"compression persists (\u221215%)", hi:"pricing power returns (+15%)",
    fmt:v=>(v>=0?"+":"\u2212")+Math.abs(v).toFixed(0)+"% on all three disclosed segment margins together" },
  { name:"CBE easing \u2014 cost of capital", min:0, max:3, step:0.25, def:0, impact:4.00,
    lo:"today\u2019s money (26.63% WACC)", hi:"3pp of easing (23.63%)",
    fmt:v=>(26.63-v).toFixed(2)+"% explicit WACC \u2014 easing "+v.toFixed(2)+"pp across both windows" },
  { name:"LME copper", min:-15, max:15, step:1, def:0, impact:0.17,
    lo:"copper falls 15%", hi:"copper rises 15%",
    fmt:v=>(v>=0?"+":"\u2212")+Math.abs(v).toFixed(0)+"% vs the held-flat curve \u2014 nearly a wash: Cables earns more pounds but the working capital that funds them grows with it" },
  { name:"EGP / USD path", min:-10, max:30, step:2, def:0, impact:0.17,
    lo:"pound holds (\u221210%)", hi:"pound weakens 30% faster",
    fmt:v=>(v>=0?"+":"\u2212")+Math.abs(v).toFixed(0)+"% on the assumed depreciation path \u2014 it lifts the copper-linked pound revenue, and the honest version of the currency question is the study\u2019s dollar-discounting alternative" }
],

"TMGH": [
  { name:'EGP/USD — impact on TMGH', min:-12, max:2, step:0.5, def:-2.5, impact:1,
    lo:'sharp depreciation', hi:'firm / tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Regional security shock — probability', min:0, max:55, step:1, def:30, impact:0.12,
    lo:'high risk', hi:'calm', fmt:v=>Math.round(v)+'% chance' },
  { name:'Project launch & sales execution — probability', min:0, max:90, step:1, def:55, impact:0.05,
    lo:'unlikely', hi:'likely', fmt:v=>Math.round(v)+'% chance' },
  { name:'Gulf-project execution — probability', min:0, max:90, step:1, def:45, impact:0.06,
    lo:'stalls', hi:'delivers', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'Hotel + recurring rental income', min:-8, max:12, step:1, def:2, impact:0.6,
    lo:'soft', hi:'strong', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' }
],

"TMPV": [
  { name:'JLR through-cycle operating margin', min:-3, max:3, step:0.25, def:0, impact:9,
    lo:'margin compresses', hi:'margin expands', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(2)+'pp vs the base case — the biggest single driver' },
  { name:'Conglomerate discount', min:0, max:35, step:1, def:20, impact:0.9,
    lo:'wider discount / trust the structure less', hi:'narrower discount / trust it more',
    fmt:v=>(35-v)+'% discount on the sum-of-the-parts' },
  { name:'India passenger-vehicle demand & EV traction', min:-6, max:8, step:0.1, def:0, impact:1.5,
    lo:'demand softens', hi:'demand firms', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / year' },
  { name:'GBP / INR & USD / INR (JLR earns abroad)', min:-6, max:6, step:0.5, def:0, impact:0.9,
    lo:'rupee strengthens / translation headwind', hi:'rupee weakens / translation tailwind',
    fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% vs the base path' },
  { name:'RBI policy-rate path', min:-4, max:4, step:0.25, def:0, impact:0.5,
    lo:'tighter / rate headwind', hi:'easier / rate tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(2)+'% vs base' }
],

"TSLA": [
  { name:'FSD / Robotaxi monetization ramp', min:-8, max:10, step:0.5, def:1.4, impact:1,
    lo:'sharp depreciation', hi:'firm / tailwind', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'China demand / price-war shock — probability', min:0, max:55, step:1, def:30, impact:0.07,
    lo:'high risk', hi:'calm', fmt:v=>Math.round(v)+'% chance' },
  { name:'Robotaxi / unsupervised-FSD milestone — probability', min:0, max:90, step:1, def:35, impact:0.05,
    lo:'unlikely', hi:'likely', fmt:v=>Math.round(v)+'% chance' },
  { name:'Delivery-volume trajectory', min:-5, max:8, step:0.5, def:1, impact:1,
    lo:'weaker', hi:'stronger', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' },
  { name:'US real-rate / Nasdaq-flow path', min:-6, max:8, step:0.5, def:-0.6, impact:1,
    lo:'weaker', hi:'stronger', fmt:v=>(v>=0?'+':'\u2212')+Math.abs(v).toFixed(1)+'% / quarter' }
]
};
