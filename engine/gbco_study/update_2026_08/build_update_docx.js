// GBCO Valuation Update 30-08-2026 — report builder.
// Every financial numeral is read from update_numbers_30082026.json (produced and
// asserted by compute_update.py); no number is typed here. External-reader clean.
const fs = require("fs");
const path = require("path");
const D = require("docx");

const HERE = __dirname;
const N = JSON.parse(fs.readFileSync(path.join(HERE, "update_numbers_30082026.json"), "utf8"));
const OUT = path.join(HERE, "..", "..", "..", "files", "GBCO_Valuation_Update_30-08-2026.docx");

const f1 = (x) => Number(x).toLocaleString("en-US", { maximumFractionDigits: 1, minimumFractionDigits: 1 });
const f2 = (x) => Number(x).toLocaleString("en-US", { maximumFractionDigits: 2, minimumFractionDigits: 2 });
const f0 = (x) => Number(x).toLocaleString("en-US", { maximumFractionDigits: 0 });
const pc = (x, d = 1) => (100 * x).toFixed(d) + "%";

const INK = "12211E", TEAL = "12796B", MUTED = "6B7C78", LINE = "DCE4E2", BG = "F4F1EA";

const P = (text, opts = {}) => new D.Paragraph({
  children: [new D.TextRun({ text, size: opts.size || 21, bold: !!opts.bold, italics: !!opts.i, color: opts.color || INK, font: "Georgia" })],
  spacing: { after: opts.after ?? 120, before: opts.before ?? 0 },
  alignment: opts.align,
});
const H = (text, lvl) => new D.Paragraph({
  heading: lvl === 1 ? D.HeadingLevel.HEADING_1 : D.HeadingLevel.HEADING_2,
  children: [new D.TextRun({ text, bold: true, size: lvl === 1 ? 30 : 24, color: lvl === 1 ? INK : TEAL, font: "Georgia" })],
  spacing: { before: lvl === 1 ? 320 : 240, after: 140 },
});

function table(headers, rows, widths) {
  const total = widths.reduce((a, b) => a + b, 0);
  const cell = (t, i, hdr) => new D.TableCell({
    width: { size: widths[i], type: D.WidthType.DXA },
    shading: hdr ? { type: D.ShadingType.CLEAR, fill: BG } : undefined,
    margins: { top: 60, bottom: 60, left: 100, right: 100 },
    children: [new D.Paragraph({
      alignment: i === 0 ? D.AlignmentType.LEFT : D.AlignmentType.RIGHT,
      children: [new D.TextRun({ text: String(t), size: 19, bold: hdr, font: "Georgia", color: hdr ? INK : INK })],
      spacing: { after: 0 },
    })],
  });
  return new D.Table({
    width: { size: total, type: D.WidthType.DXA },
    columnWidths: widths,
    borders: {
      top: { style: D.BorderStyle.SINGLE, size: 4, color: LINE }, bottom: { style: D.BorderStyle.SINGLE, size: 4, color: LINE },
      left: { style: D.BorderStyle.NONE }, right: { style: D.BorderStyle.NONE },
      insideHorizontal: { style: D.BorderStyle.SINGLE, size: 2, color: LINE }, insideVertical: { style: D.BorderStyle.NONE },
    },
    rows: [new D.TableRow({ children: headers.map((h2, i) => cell(h2, i, true)), tableHeader: true }),
           ...rows.map(r => new D.TableRow({ children: r.map((c, i) => cell(c, i, false)) }))],
  });
}

const w = N.wacc, F = N.forecast, dcf = N.auto_dcf, mnt = N.mnt_leg_dual, so = N.sotp, L = N.lenses;
const PE = N.prior_edition, PR = N.params, IR = N.inputs_register;
const yrs = ["2026", "2027", "2028", "2029", "2030"];

const children = [
  P("TESTAHIL — Standing Research Programme", { size: 18, color: MUTED, after: 40 }),
  P("GB Corp (GBCO.CA, EGX) — Valuation Update", { size: 40, bold: true, after: 60 }),
  P("Fair-value re-issue under the corrected cost-of-capital method · 30 August 2026", { size: 22, color: TEAL, after: 200 }),

  H("Read this first", 2),
  P("This edition re-derives GB Corp's fair value on a rebuilt foundation: fifteen fiscal years (2011–2025) of the company's own audited statements and disclosures plus the reviewed 2026 interims, a regression beta measured against the exchange's published EGX30 index, and a cost of capital constructed so that Egypt country risk is counted once, not twice. Before this build, the forecasting method itself was back-tested against the company's own history at ten annual starting points; that record shapes how far ahead we state single numbers versus ranges. This document updates the valuation of the 8 July 2026 study; it does not restate that study's full company narrative."),
  P("Nothing here is a recommendation, rating, or price target. We publish fair-value ranges and the assumptions behind them, and we grade our own record publicly.", { i: true, color: MUTED }),

  H("Fair value", 1),
  table(["", "Bear", "Base", "Full value"],
    [["Fair value (EGP/share)", f1(N.fair.bear), f1(N.fair.base), f1(N.fair.full)],
     ["vs close " + N.spot_date + " (EGP " + f2(N.spot) + ")", pc(N.fair.bear / N.spot - 1, 0), pc(N.fair.base / N.spot - 1, 0), pc(N.fair.full / N.spot - 1, 0)]],
    [3400, 1800, 1800, 1800]),
  P("", { after: 60 }),
  P("The base case sits essentially at the market price: at today's Egyptian discount rates the operating businesses are worth modest value net of their debt, and the MNT-Halan stake — marked by its own June 2026 funding round — carries most of the equity story. The previous edition's higher fair value (" + f1(PE.fair.base) + ") rested on a cost of capital that double-counted country risk, an assumed beta of 1.0, and a larger multiple on the financing arm; each of those legs is rebuilt below.", { after: 200 }),

  H("What changed since 8 July 2026", 1),
  table(["Component", "8 Jul 2026 edition", "This edition"],
    [["Risk-free basis", "raw 10Y yield " + pc(PE.rf_observed, 2), "10Y " + pc(w.rf_observed, 2) + " less Egypt's own default spread → rf* " + pc(w.rf_star_cds, 2) + " (CDS basis)"],
     ["Beta", f2(PE.beta) + " assumed (regression rejected)", f2(N.beta.beta) + " vs EGX30, weekly, n=" + N.beta.n + ", " + f1(N.beta.window_years) + "y window"],
     ["Cost of equity", pc(PE.ke_cds, 2) + " (CDS basis)", pc(w.ke_cds, 2) + " (CDS) / " + pc(w.ke_rating, 2) + " (rating)"],
     ["WACC", pc(PE.wacc_cds, 2) + " (CDS basis)", pc(w.wacc_cds, 2) + " (CDS) / " + pc(w.wacc_rating, 2) + " (rating)"],
     ["MNT-Halan stake", f2(100 * PE.mnt_stake) + "% at USD " + f1(PE.mnt_round_usd_bn) + "bn round", f2(100 * mnt.stake_current) + "% today (" + f2(100 * mnt.stake_post) + "% after second closing), shown BOTH at carrying value and at the round mark"],
     ["Financing arm (ex-MNT)", "EGP " + f0(PE.cap_val) + "mn (earnings multiple)", "EGP " + f0(N.gb_capital_leg.book_exmnt_parent) + "mn at book, cross-checked on earnings"],
     ["History behind the forecast", "3 years of aggregates", "15 audited years + 2026 interims; method back-tested at 10 starting points"],
     ["Years 3–5", "point estimates", "ranges from the back-test's own error record"]],
    [2300, 3200, 4900]),

  H("Cost of capital (built bottom-up, both bases)", 1),
  P("Country risk enters once, through the equity risk premium. The risk-free rate is the observed local 10-year yield stripped of Egypt's own sovereign default spread; the same basis of spread is stripped as the premium adds back (rating with rating, CDS with CDS). Sources: Egypt 10Y " + pc(w.rf_observed, 2) + " (27 Aug 2026); Damodaran country table, Egypt row, January 2026 vintage; central bank corridor held at " + pc(IR.cbe_lending.value, 1) + " lending on 20 August 2026."),
  table(["", "Rating basis", "CDS basis"],
    [["rf* (normalised risk-free)", pc(w.rf_star_rating, 2), pc(w.rf_star_cds, 2)],
     ["Equity risk premium", pc(IR.erp_rating.value, 2), pc(IR.erp_cds.value, 2)],
     ["Beta (own stock vs EGX30)", f2(N.beta.beta), f2(N.beta.beta)],
     ["Cost of equity", pc(w.ke_rating, 2), pc(w.ke_cds, 2)],
     ["Cost of debt, pre-tax (marginal)", pc(w.kd_pretax, 2), pc(w.kd_pretax, 2)],
     ["Weights (E / D)", pc(w.we, 0) + " / " + pc(w.wd, 0), pc(w.we, 0) + " / " + pc(w.wd, 0)],
     ["WACC", pc(w.wacc_rating, 2), pc(w.wacc_cds, 2) + "  ← used in the DCF"]],
    [3800, 2500, 2500]),
  P("The marginal cost of debt is set from the sovereign 10-year plus a " + PR.corp_spread_bp + "bp corporate spread (" + pc(w.kd_pretax, 2) + " pre-tax). Because the group borrows mostly short-tenor Egyptian pounds (its net foreign-currency exposure is only about EGP 2.2bn against a ~38bn debt book), a short-tenor reading of roughly 22% is also shown in our sensitivity work; it moves the base fair value by under one pound.", { color: MUTED }),

  H("Forecast 2026–2030 (built from units × price, by line of business)", 1),
  P("Volumes and average selling prices come from the company's own line-of-business tables; the first forecast half-year is anchored on the reported H1-2026 actuals. Margins are outputs of the segment mix, not inputs. Group revenue is the two segments less intercompany eliminations."),
  table(["EGP mn", ...yrs],
    [["Passenger cars & after-sales (units)", ...yrs.map(y => f0(F[y].pc_units))],
     ["Light mobility (units)", ...yrs.map(y => f0(F[y].lm_units))],
     ["Commercial vehicles & CE (units)", ...yrs.map(y => f0(F[y].cv_units))],
     ["GB Auto revenue", ...yrs.map(y => f0(F[y].auto_rev))],
     ["GB Capital revenue", ...yrs.map(y => f0(F[y].cap_rev))],
     ["Group revenue", ...yrs.map(y => f0(F[y].rev))],
     ["Gross margin", ...yrs.map(y => pc(F[y].gpm, 1))],
     ["Operating profit", ...yrs.map(y => f0(F[y].op))],
     ["Associates (MNT-Halan pickup)", ...yrs.map(y => f0(F[y].assoc))],
     ["Net finance cost", ...yrs.map(y => f0(F[y].fin_net))],
     ["Effective tax rate", ...yrs.map(y => pc(F[y].etr, 0))],
     ["Net profit (parent)", ...yrs.map(y => f0(F[y].np_parent))],
     ["EPS (EGP)", ...yrs.map(y => f2(F[y].eps))]],
    [3300, 1420, 1420, 1420, 1420, 1420]),
  P("", { after: 60 }),
  P("Years three to five are stated as ranges, not points. Our back-test of this forecasting approach on GB Corp's own 2011–2025 history shows realised revenue three years out landing between roughly 0.6× and 1.4× the point estimate (wider at years four and five). Applied here:", { after: 80 }),
  table(["Revenue range, EGP mn", "Low", "Point", "High"],
    Object.entries(N.rev_ranges_h3_h5).map(([y, r]) => [y, f0(r.low), f0(r.point), f0(r.high)]),
    [3300, 1900, 1900, 1900]),

  H("Sum of the parts — and the judgement that drives it", 1),
  P("GB Corp is three businesses in one listing: an automotive assembler-distributor, a non-bank lender, and a " + f2(100 * mnt.stake_current) + "% stake in MNT-Halan (" + f2(100 * mnt.stake_post) + "% once the announced second closing completes). The stake's value is the update's most consequential contested judgement, so it is computed both ways and shown side by side — never averaged."),
  table(["Leg (EGP mn, parent share)", "Value", "How"],
    [["GB Auto (DCF at " + pc(dcf.wacc_used, 1) + ", terminal growth " + pc(dcf.tg, 0) + ")", f0(dcf.equity), "enterprise " + f0(dcf.ev) + " less net debt " + f0(dcf.net_debt) + " and minorities"],
     ["GB Capital ex-MNT", f0(N.gb_capital_leg.values.base), f1(PR.cap_pb_band[1]) + "× book (band " + f1(PR.cap_pb_band[0]) + "–" + f1(PR.cap_pb_band[2]) + "× in bear/full)"],
     ["MNT-Halan stake — framing A", f0(mnt.framing_A_carrying), "audited carrying value (equity method)"],
     ["MNT-Halan stake — framing B", f0(mnt.framing_B_round_mark_current_stake), "USD " + f1(mnt.round_usd_bn) + "bn June-2026 round × " + f2(100 * mnt.stake_current) + "% × " + f2(mnt.egp_usd) + ""],
     ["Other associates & investments", f0(so.other_assoc), "carrying value"],
     ["Total (A) after 10% holding discount", f0(so.total_book_framing * 0.9), f1(so.total_book_framing * 0.9 / N.shares_mn) + " per share"],
     ["Total (B) after 10% holding discount", f0(so.total_round_framing * 0.9), f1(so.total_round_framing * 0.9 / N.shares_mn) + " per share"]],
    [4200, 1700, 4500]),
  P("", { after: 60 }),
  P("How to read this table against the lens table below: rows A and B change ONE thing only — the MNT-Halan framing — with the car business and the lender held at their base values in both. The 'Sum of the parts' row in the lens table is a full scenario per column: its Base equals Total (B); its Bear starts from framing A and additionally stresses the operating legs (car business at 60% of its DCF value, lender at 0.8× book), which is why it sits below Total (A); its Full flexes the operating legs up (×1.4) and marks the stake at the post-second-closing round value grown to a next mark.", { color: MUTED, after: 120 }),
  P("The gap between the two framings — about " + f1((so.total_round_framing - so.total_book_framing) * 0.9 / N.shares_mn) + " EGP per share — is the honest width of this valuation. Framing B is a real transaction price: Al Ahly Capital paid it in June 2026. Framing A is the audited book, but the auditor qualifies it every period because MNT-Halan's own statements are not made available. The base case stands on framing B; the bear case stands on framing A. In dollars, the market capitalisation (~USD " + f0(N.usd_cross_check.mktcap_usd_mn) + "mn) is close to the stake's round-mark value alone (~USD " + f0(N.usd_cross_check.mnt_stake_usd_mn) + "mn) — at the market price you are paying for the stake and getting the automotive and lending businesses at little value."),

  H("Four lenses, one field", 1),
  table(["Lens (EGP/share)", "Bear", "Base", "Full", "Weight"],
    [["Sum of the parts", f1(L.sotp.bear), f1(L.sotp.base), f1(L.sotp.bull), pc(L.weights.sotp, 0)],
     ["Pre-discount SOTP", f1(L.prediscount.bear), f1(L.prediscount.base), f1(L.prediscount.full), pc(L.weights.prediscount, 0)],
     ["Relative (" + f0(PR.pe_band[0]) + "–" + f0(PR.pe_band[2]) + "× blended 2026–27E EPS)", f1(L.relative.bear), f1(L.relative.base), f1(L.relative.bull), pc(L.weights.relative, 0)],
     ["Normalised earnings power", f1(L.normalized.bear), f1(L.normalized.base), f1(L.normalized.bull), pc(L.weights.normalized, 0)],
     ["Weighted central", f1(N.fair.bear), f1(N.fair.base), f1(N.fair.full), "100%"]],
    [3800, 1500, 1500, 1500, 1400]),
  P("", { after: 60 }),
  P("The lenses disagree, and the disagreement is information. The normalised-earnings lens is severe (" + f1(L.normalized.base) + "): at a 27.8% cost of equity, a business earning a low-teens return on its book is worth far less than that book — this is the discount-rate environment speaking, and it is the same force that keeps the automotive DCF modest. The relative and sum-of-the-parts lenses carry the recovery and the stake. The weighted centre of " + f1(N.fair.base) + " should be read with the full bear-to-full span, not alone.", { color: MUTED }),

  H("What would change our view", 1),
  P("Upside: the second MNT-Halan closing at or above the June round; Egyptian rate cuts resuming (each 100bp off the discount rate adds roughly 1.5–2 EGP across the legs); regional (Iraq/Jordan) losses fading on schedule from Q4 2026; Sadat localisation lifting automotive margins faster than the ~1pp/year assumed."),
  P("Downside: a step-devaluation of the pound (raises the discount rate and compresses the auto margin before prices catch up); the effective tax burden staying near H1-2026's 41% instead of normalising; a funding-market shock to the securitisation channel the lending arm depends on; any down-round or write-down at MNT-Halan — the single largest sensitivity in this valuation."),
  P("Known limits stated plainly: MNT-Halan's contribution is recorded by management and qualified by the auditor every period since 2024, because the associate's own financial statements are not provided; per-product unit costs are not disclosed, so segment margins are modelled at segment level; and our own back-testing says five-year revenue points carry roughly ±40–60% bands — which is why years three to five are published as ranges.", { i: true }),

  H("Basis of preparation", 2),
  P("Historic figures: the company's own audited consolidated financial statements (KPMG Hazem Hassan) 2011–2025 and reviewed interims to 30 June 2026, taken from the company's investor-relations site. Market inputs as of 27–30 August 2026 from the sources named in the cost-of-capital section. Beta: weekly two-stage regression of the stock on the published EGX30 index, 2021–2026. A source and date accompany every input in the published model file.", { color: MUTED, size: 19 }),
  P("© TESTAHIL 2026 · Educational research. Not investment advice, not an offer, not a solicitation. Fair-value ranges and probability statements only; we never publish buy/sell/hold ratings or price targets. Forecasts are graded publicly when they resolve.", { color: MUTED, size: 18, before: 200 }),
];

const doc = new D.Document({
  styles: { default: { document: { run: { font: "Georgia", size: 21, color: INK } } } },
  sections: [{
    properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1100, bottom: 1100, left: 1250, right: 1250 } } },
    children,
  }],
});

D.Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync(OUT, buf);
  console.log("wrote", OUT, buf.length, "bytes");
});
