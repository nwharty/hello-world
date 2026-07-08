/* Debt Payoff Command Center — vanilla JS + SVG, no dependencies. */
"use strict";

// ---------- helpers ----------
const $ = (sel, el = document) => el.querySelector(sel);
const api = {
  get: (p) => fetch(p).then(ok),
  post: (p, body) => fetch(p, { method: "POST", body: JSON.stringify(body) }).then(ok),
  put: (p, body) => fetch(p, { method: "PUT", body: JSON.stringify(body) }).then(ok),
  del: (p) => fetch(p, { method: "DELETE" }).then(ok),
};
async function ok(res) {
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || res.statusText);
  return data;
}
const fmtMoney = (v) =>
  v == null ? "—" : (v < 0 ? "-$" : "$") + Math.abs(Math.round(v)).toLocaleString("en-US");
const fmtMonth = (mk) => {
  if (!mk) return "—";
  const [y, m] = mk.split("-").map(Number);
  return new Date(y, m - 1, 1).toLocaleDateString("en-US", { month: "short", year: "numeric" });
};
const esc = (s) =>
  String(s ?? "").replace(/[&<>"']/g, (c) =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const cssVar = (name) => getComputedStyle(document.documentElement).getPropertyValue(name).trim();
const seriesColors = () => [cssVar("--series-1"), cssVar("--series-2"), cssVar("--series-3")];
const num = (v) => (v === "" || v == null ? null : Number(v));

function toast(msg) {
  const t = $("#toast");
  t.textContent = msg;
  t.hidden = false;
  clearTimeout(toast._t);
  toast._t = setTimeout(() => (t.hidden = true), 2200);
}

// ---------- SVG line chart with crosshair + tooltip ----------
// series: [{name, color, points: Map(monthKey -> value), markers?: bool}]
function lineChart(container, { series, yFmt = fmtMoney, height = 300, floor = null }) {
  container.innerHTML = "";
  const months = [...new Set(series.flatMap((s) => [...s.points.keys()]))].sort();
  if (!months.length) {
    container.innerHTML = '<p class="hint">No data yet.</p>';
    return;
  }
  const W = 960, H = height, padL = 64, padR = 16, padT = 14, padB = 30;
  const iw = W - padL - padR, ih = H - padT - padB;
  const allVals = series.flatMap((s) => [...s.points.values()]).filter((v) => v != null);
  let yMax = Math.max(...allVals, floor ?? 0, 1);
  const yTickStep = niceStep(yMax / 4);
  yMax = Math.ceil(yMax / yTickStep) * yTickStep;
  const x = (i) => padL + (months.length === 1 ? iw / 2 : (i / (months.length - 1)) * iw);
  const y = (v) => padT + ih - (v / yMax) * ih;

  const svgNS = "http://www.w3.org/2000/svg";
  const svg = document.createElementNS(svgNS, "svg");
  svg.setAttribute("viewBox", `0 0 ${W} ${H}`);
  const add = (parent, tag, attrs, text) => {
    const el = document.createElementNS(svgNS, tag);
    for (const [k, v] of Object.entries(attrs)) el.setAttribute(k, v);
    if (text != null) el.textContent = text;
    parent.appendChild(el);
    return el;
  };

  // gridlines + y ticks (hairline, solid, recessive)
  for (let v = 0; v <= yMax; v += yTickStep) {
    add(svg, "line", { x1: padL, x2: W - padR, y1: y(v), y2: y(v),
      stroke: cssVar("--grid"), "stroke-width": 1 });
    add(svg, "text", { x: padL - 8, y: y(v) + 4, "text-anchor": "end",
      "font-size": 11, fill: cssVar("--muted"),
      style: "font-variant-numeric: tabular-nums" }, yFmt(v));
  }
  // x ticks: ~6 labels
  const xEvery = Math.max(1, Math.round(months.length / 6));
  months.forEach((mk, i) => {
    const last = i === months.length - 1;
    if (i % xEvery !== 0 && !last) return;
    if (last && months.length > 1 && (months.length - 1) % xEvery < xEvery / 2 && i % xEvery !== 0) return;
    add(svg, "text", { x: x(i), y: H - 8,
      "text-anchor": last ? "end" : i === 0 ? "start" : "middle",
      "font-size": 11, fill: cssVar("--muted") }, fmtMonth(mk));
  });
  // baseline axis
  add(svg, "line", { x1: padL, x2: W - padR, y1: y(0), y2: y(0),
    stroke: cssVar("--axis"), "stroke-width": 1 });
  // emergency floor reference (labeled, not color-alone)
  if (floor != null && floor > 0 && floor < yMax) {
    add(svg, "line", { x1: padL, x2: W - padR, y1: y(floor), y2: y(floor),
      stroke: cssVar("--axis"), "stroke-width": 1 });
    add(svg, "text", { x: W - padR, y: y(floor) - 5, "text-anchor": "end",
      "font-size": 11, fill: cssVar("--muted") }, `floor ${yFmt(floor)}`);
  }

  // series lines (2px, round) + markers with 2px surface ring
  for (const s of series) {
    let d = "", pen = false;
    months.forEach((mk, i) => {
      const v = s.points.get(mk);
      if (v == null) { pen = false; return; }
      d += `${pen ? "L" : "M"}${x(i).toFixed(1)},${y(v).toFixed(1)}`;
      pen = true;
    });
    add(svg, "path", { d, fill: "none", stroke: s.color, "stroke-width": 2,
      "stroke-linejoin": "round", "stroke-linecap": "round" });
    if (s.markers) {
      months.forEach((mk, i) => {
        const v = s.points.get(mk);
        if (v == null) return;
        add(svg, "circle", { cx: x(i), cy: y(v), r: 4, fill: s.color,
          stroke: cssVar("--surface"), "stroke-width": 2 });
      });
    }
  }

  // crosshair + tooltip
  const cross = add(svg, "line", { y1: padT, y2: padT + ih,
    stroke: cssVar("--axis"), "stroke-width": 1, visibility: "hidden" });
  const hover = add(svg, "rect", { x: padL, y: padT, width: iw, height: ih,
    fill: "transparent", style: "cursor: crosshair" });
  const tip = $("#tooltip");
  const showTip = (evt) => {
    const rect = svg.getBoundingClientRect();
    const px = ((evt.clientX - rect.left) / rect.width) * W;
    const i = Math.max(0, Math.min(months.length - 1,
      Math.round(((px - padL) / iw) * (months.length - 1))));
    cross.setAttribute("x1", x(i));
    cross.setAttribute("x2", x(i));
    cross.setAttribute("visibility", "visible");
    tip.innerHTML = "";
    const title = document.createElement("div");
    title.className = "tt-title";
    title.textContent = fmtMonth(months[i]);
    tip.appendChild(title);
    for (const s of series) {
      const v = s.points.get(months[i]);
      if (v == null) continue;
      const row = document.createElement("div");
      row.className = "tt-row";
      const key = document.createElement("span");
      key.className = "swatch";
      key.style.background = s.color;
      const name = document.createElement("span");
      name.className = "tt-name";
      name.textContent = s.name; // untrusted → textContent
      const val = document.createElement("span");
      val.className = "tt-val";
      val.textContent = yFmt(v);
      row.append(key, name, val);
      tip.appendChild(row);
    }
    tip.hidden = false;
    const tw = tip.offsetWidth;
    const left = evt.clientX + 14 + tw > window.innerWidth ? evt.clientX - tw - 14 : evt.clientX + 14;
    tip.style.left = left + "px";
    tip.style.top = Math.max(8, evt.clientY - 20) + "px";
  };
  hover.addEventListener("pointermove", showTip);
  hover.addEventListener("pointerleave", () => {
    tip.hidden = true;
    cross.setAttribute("visibility", "hidden");
  });

  container.appendChild(svg);
  if (series.length >= 2) {
    const legend = document.createElement("div");
    legend.className = "legend";
    for (const s of series) {
      const key = document.createElement("span");
      key.className = "key";
      const sw = document.createElement("span");
      sw.className = "swatch";
      sw.style.background = s.color;
      const label = document.createElement("span");
      label.textContent = s.name;
      key.append(sw, label);
      legend.appendChild(key);
    }
    container.appendChild(legend);
  }
}
function niceStep(raw) {
  const mag = Math.pow(10, Math.floor(Math.log10(Math.max(raw, 1))));
  for (const m of [1, 2, 2.5, 5, 10]) if (raw <= m * mag) return m * mag;
  return 10 * mag;
}

// ---------- tabs ----------
$("#tabs").addEventListener("click", (e) => {
  const btn = e.target.closest("button[data-tab]");
  if (!btn) return;
  for (const b of $("#tabs").children) b.classList.toggle("active", b === btn);
  for (const s of document.querySelectorAll(".tab"))
    s.classList.toggle("active", s.id === "tab-" + btn.dataset.tab);
  loadTab(btn.dataset.tab);
});
function loadTab(name) {
  ({ dashboard: renderDashboard, scenarios: renderScenarios,
     snapshots: renderSnapshots, config: renderConfig }[name])();
}

// ---------- dashboard ----------
async function renderDashboard() {
  const d = await api.get("/api/dashboard");
  $("#hero-total").textContent = fmtMoney(d.total_debt);

  // alerts
  const box = $("#alerts");
  box.innerHTML = "";
  const alerts = [...d.plan.promo_alerts];
  if (d.plan.buffer_violations.length) {
    const first = d.plan.buffer_violations[0];
    alerts.push({
      level: "warning",
      message: `Baby buffer: planned payments drop cash below ${fmtMoney(first.floor)} in ` +
        `${d.plan.buffer_violations.length} month(s) — first ${fmtMonth(first.month)} at ${fmtMoney(first.cash)}.`,
    });
  }
  for (const g of d.plan.goals.filter((g) => !g.on_track)) {
    alerts.push({
      level: "critical",
      message: `Goal at risk: ${g.goal} by ${g.due} — projected ${fmtMonth(g.projected) || "beyond horizon"}.`,
    });
  }
  if (!alerts.length)
    alerts.push({ level: "good", message: "All clear — promos covered, goals on track, cash above the floor." });
  for (const a of alerts) {
    const el = document.createElement("div");
    el.className = "alert " + a.level;
    const badge = document.createElement("span");
    badge.className = "badge";
    badge.textContent = { critical: "⚠ ALERT", warning: "△ WATCH", good: "✓ ON TRACK" }[a.level];
    const msg = document.createElement("span");
    msg.textContent = a.message;
    el.append(badge, msg);
    box.appendChild(el);
  }

  // stat tiles
  const goals = d.plan.goals;
  const cc = goals.find((g) => g.goal.includes("cards"));
  const loan = goals.find((g) => g.goal.includes("loan"));
  const tiles = [
    cc && { label: `Cards at $0 (goal ${cc.due})`, value: fmtMonth(cc.projected),
            delta: cc.on_track ? "on track" : "past goal", good: cc.on_track },
    loan && { label: `Loan paid off (goal ${loan.due})`, value: fmtMonth(loan.projected),
              delta: loan.on_track ? "on track" : "past goal", good: loan.on_track },
    { label: "Interest saved vs minimums", value: fmtMoney(d.plan.interest_saved),
      delta: `${d.plan.months_cut} months cut`, good: d.plan.interest_saved > 0 },
    { label: "Lowest projected cash", value: fmtMoney(d.plan.min_cash),
      delta: `floor ${fmtMoney(Number(d.settings.emergency_floor))}`,
      good: d.plan.min_cash >= Number(d.settings.emergency_floor) },
  ].filter(Boolean);
  $("#tiles").innerHTML = tiles.map((t) => `
    <div class="tile">
      <div class="label">${esc(t.label)}</div>
      <div class="value">${esc(t.value)}</div>
      <div class="delta ${t.good ? "good" : "bad"}">${esc(t.delta)}</div>
    </div>`).join("");

  // trajectory chart: plan projection vs actual snapshots
  const [c1, c2] = seriesColors();
  const planPts = new Map(d.plan.monthly.map((m) => [m.month, m.total_balance]));
  const actualPts = new Map(d.actual.map((s) => [s.snap_date.slice(0, 7), s.total]));
  const series = [{ name: "Plan (projected total debt)", color: c1, points: planPts }];
  if (actualPts.size)
    series.push({ name: "Actual (snapshots)", color: c2, points: actualPts, markers: true });
  lineChart($("#trajectory-chart"), { series });

  // debt table
  $("#debt-summary").innerHTML = `
    <tr><th>Debt</th><th class="num">Balance</th><th>Rate</th><th>Promo ends</th><th>Payoff (plan)</th></tr>` +
    d.debts.map((debt) => {
      const res = d.plan.debts[debt.id] || {};
      const rate = debt.promo_end ? `0% → ${debt.apr}%` : `${debt.apr}%`;
      return `<tr>
        <td>${esc(debt.name)}</td>
        <td class="num">${fmtMoney(debt.balance)}</td>
        <td>${esc(rate)}</td>
        <td>${debt.promo_end ? fmtMonth(debt.promo_end.slice(0, 7)) : "—"}</td>
        <td>${fmtMonth(res.payoff_month)}</td>
      </tr>`;
    }).join("");

  // upcoming events
  $("#upcoming-events").innerHTML = d.upcoming_events.length
    ? `<tr><th>Event</th><th>Date</th><th class="num">Amount</th><th class="num">To debt</th></tr>` +
      d.upcoming_events.map((e) => `<tr>
        <td>${esc(e.name)}</td><td>${esc(e.event_date)}</td>
        <td class="num">${fmtMoney(e.amount)}</td>
        <td class="num">${fmtMoney(e.allocate_amount)}</td>
      </tr>`).join("")
    : `<tr><td class="hint">None scheduled — add RSU vests and bonuses on the Config tab.</td></tr>`;
}

// ---------- scenarios ----------
let scenarioSelection = null;
async function renderScenarios() {
  const scenarios = await api.get("/api/scenarios");
  if (scenarioSelection == null)
    scenarioSelection = new Set(scenarios.slice(0, 3).map((s) => s.id));

  const picker = $("#scenario-picker");
  picker.innerHTML = "";
  const palette = seriesColors();
  const colorOf = (id) => {
    const idx = [...scenarioSelection].sort((a, b) => a - b).indexOf(id);
    return idx >= 0 && idx < palette.length ? palette[idx] : cssVar("--muted");
  };
  for (const s of scenarios) {
    const chip = document.createElement("span");
    chip.className = "chip" + (scenarioSelection.has(s.id) ? " on" : "");
    const sw = document.createElement("span");
    sw.className = "swatch";
    sw.style.background = scenarioSelection.has(s.id) ? colorOf(s.id) : "transparent";
    const label = document.createElement("span");
    label.textContent = s.name + (s.is_plan ? " ★" : "");
    chip.append(sw, label);
    chip.addEventListener("click", () => {
      if (scenarioSelection.has(s.id)) scenarioSelection.delete(s.id);
      else if (scenarioSelection.size >= 3) return toast("Compare up to 3 scenarios (plus baseline).");
      else scenarioSelection.add(s.id);
      renderScenarios();
    });
    picker.appendChild(chip);
  }

  const ids = [...scenarioSelection].sort((a, b) => a - b);
  const cmp = await api.get("/api/compare?ids=" + ids.join(","));
  const rows = [cmp.baseline, ...cmp.scenarios];

  // chart: total balance curves; baseline in muted ink, scenarios in slots
  const series = rows.map((r, i) => ({
    name: r.scenario.name,
    color: i === 0 ? cssVar("--muted") : palette[i - 1],
    points: new Map(r.monthly.map((m) => [m.month, m.total_balance])),
  }));
  lineChart($("#compare-chart"), { series, height: 320 });

  // comparison table
  $("#compare-table").innerHTML = `
    <tr><th>Scenario</th><th>Debt-free</th><th class="num">Total interest</th>
        <th class="num">Interest saved</th><th class="num">Months cut</th>
        <th>Cards by ${esc(fmtMonth((rows[0].goals.find((g) => g.goal.includes("cards")) || {}).due?.slice(0, 7)))}</th>
        <th>Loan by ${esc(fmtMonth((rows[0].goals.find((g) => g.goal.includes("loan")) || {}).due?.slice(0, 7)))}</th>
        <th class="num">Min cash</th><th>Buffer / promo flags</th></tr>` +
    rows.map((r, i) => {
      const cc = r.goals.find((g) => g.goal.includes("cards"));
      const loan = r.goals.find((g) => g.goal.includes("loan"));
      const flags = [];
      if (r.buffer_violations.length)
        flags.push(`cash < floor in ${r.buffer_violations.length} mo (first ${fmtMonth(r.buffer_violations[0].month)})`);
      for (const a of r.promo_alerts)
        flags.push(`${a.level === "critical" ? "⚠" : "△"} ${a.debt} promo`);
      const mark = (g) => g ? (g.on_track
        ? `<span class="ok-mark">✓ ${fmtMonth(g.projected)}</span>`
        : `<span class="risk-mark">✗ ${fmtMonth(g.projected) || "never"}</span>`) : "—";
      return `<tr>
        <td><span class="swatch" style="background:${i === 0 ? cssVar("--muted") : palette[i - 1]}"></span>${esc(r.scenario.name)}</td>
        <td>${fmtMonth(r.debt_free_month)}</td>
        <td class="num">${fmtMoney(r.total_interest)}</td>
        <td class="num">${i === 0 ? "—" : fmtMoney(r.interest_saved)}</td>
        <td class="num">${i === 0 ? "—" : r.months_cut}</td>
        <td>${mark(cc)}</td><td>${mark(loan)}</td>
        <td class="num">${fmtMoney(r.min_cash)}</td>
        <td>${flags.length ? esc(flags.join("; ")) : '<span class="ok-mark">none</span>'}</td>
      </tr>`;
    }).join("");

  renderScenarioEditor(scenarios);
}

async function renderScenarioEditor(scenarios) {
  const debts = await api.get("/api/debts");
  const debtOptions = (sel) =>
    `<option value="">Loan first, then highest APR</option>` +
    debts.map((d) => `<option value="${d.id}" ${sel === d.id ? "selected" : ""}>${esc(d.name)}</option>`).join("");
  const box = $("#scenario-editor");
  box.innerHTML = "";
  for (const s of scenarios) {
    const fs = document.createElement("fieldset");
    fs.className = "scenario-block";
    fs.innerHTML = `
      <legend>${esc(s.name)}</legend>
      <div class="form-grid">
        <div class="field"><label>Name</label><input name="name" value="${esc(s.name)}"></div>
        <div class="field"><label>Extra monthly principal ($)</label>
          <input name="extra_monthly" type="number" step="50" min="0" value="${s.extra_monthly}"></div>
        <div class="field"><label>Apply income events</label>
          <select name="use_income_events">
            <option value="1" ${s.use_income_events ? "selected" : ""}>Yes — lumps at vests/bonuses</option>
            <option value="0" ${!s.use_income_events ? "selected" : ""}>No</option>
          </select></div>
        <div class="field"><label>This is the plan</label>
          <select name="is_plan">
            <option value="0" ${!s.is_plan ? "selected" : ""}>No</option>
            <option value="1" ${s.is_plan ? "selected" : ""}>Yes ★ (drives dashboard)</option>
          </select></div>
      </div>
      <div class="lump-list"></div>
      <div class="row-actions">
        <button class="btn small ghost" data-act="add-lump">+ Ad-hoc lump sum</button>
        <button class="btn small" data-act="save">Save</button>
        <button class="btn small danger" data-act="delete">Delete</button>
      </div>`;
    const lumpList = $(".lump-list", fs);
    const addLumpRow = (lump = {}) => {
      const row = document.createElement("div");
      row.className = "lump-row";
      row.innerHTML = `
        <div class="field"><label>Date</label><input name="lump_date" type="date" value="${esc(lump.lump_date || "")}"></div>
        <div class="field"><label>Amount ($)</label><input name="amount" type="number" step="100" min="0" value="${lump.amount ?? ""}"></div>
        <div class="field"><label>Toward</label><select name="debt_id">${debtOptions(lump.debt_id)}</select></div>
        <button class="btn small danger" data-act="rm-lump">✕</button>`;
      lumpList.appendChild(row);
    };
    (s.lumps || []).forEach(addLumpRow);
    fs.addEventListener("click", async (e) => {
      const act = e.target.dataset?.act;
      if (!act) return;
      e.preventDefault();
      if (act === "add-lump") return addLumpRow();
      if (act === "rm-lump") return e.target.closest(".lump-row").remove();
      if (act === "delete") {
        if (!confirm(`Delete scenario "${s.name}"?`)) return;
        await api.del(`/api/scenarios/${s.id}`);
        scenarioSelection.delete(s.id);
        toast("Scenario deleted");
        return renderScenarios();
      }
      if (act === "save") {
        const val = (n) => $(`[name="${n}"]`, fs).value;
        const lumps = [...lumpList.children].map((row) => ({
          lump_date: $('[name="lump_date"]', row).value,
          amount: num($('[name="amount"]', row).value),
          debt_id: num($('[name="debt_id"]', row).value),
        })).filter((l) => l.lump_date && l.amount);
        await api.put(`/api/scenarios/${s.id}`, {
          name: val("name"), extra_monthly: num(val("extra_monthly")) || 0,
          use_income_events: Number(val("use_income_events")),
          is_plan: Number(val("is_plan")), lumps,
        });
        toast("Scenario saved");
        renderScenarios();
      }
    });
    box.appendChild(fs);
  }
  const addBtn = document.createElement("button");
  addBtn.className = "btn ghost";
  addBtn.textContent = "+ New scenario";
  addBtn.addEventListener("click", async () => {
    await api.post("/api/scenarios", {
      name: "New scenario", extra_monthly: 0, use_income_events: 1, is_plan: 0, lumps: [],
    });
    renderScenarios();
  });
  box.appendChild(addBtn);
}

// ---------- snapshots ----------
async function renderSnapshots() {
  const [debts, snaps, settings] = await Promise.all([
    api.get("/api/debts"), api.get("/api/snapshots"), api.get("/api/settings")]);
  const form = $("#snapshot-form");
  const today = new Date().toISOString().slice(0, 10);
  form.innerHTML = `
    <div class="field"><label>Snapshot date</label><input name="snap_date" type="date" value="${today}"></div>` +
    debts.map((d) => `
      <div class="field"><label>${esc(d.name)} balance</label>
        <input name="debt-${d.id}" type="number" step="0.01" min="0" value="${d.balance}"></div>`).join("") + `
    <div class="field"><label>Cash on hand</label>
      <input name="cash" type="number" step="100" min="0" value="${esc(settings.cash_on_hand || "")}"></div>
    <div class="field"><button class="btn" type="submit">Save snapshot</button></div>`;
  form.onsubmit = async (e) => {
    e.preventDefault();
    const balances = {};
    for (const d of debts) balances[d.id] = num($(`[name="debt-${d.id}"]`, form).value) ?? d.balance;
    await api.post("/api/snapshots", {
      snap_date: $('[name="snap_date"]', form).value,
      balances,
      cash: num($('[name="cash"]', form).value),
    });
    toast("Snapshot saved — balances updated");
    renderSnapshots();
  };

  // history pivot: one row per date
  const byDate = new Map();
  for (const s of snaps.debts) {
    if (!byDate.has(s.snap_date)) byDate.set(s.snap_date, {});
    byDate.get(s.snap_date)[s.debt_id] = s.balance;
  }
  const cashByDate = new Map(snaps.cash.map((c) => [c.snap_date, c.cash]));
  const dates = [...new Set([...byDate.keys(), ...cashByDate.keys()])].sort().reverse();
  $("#snapshot-history").innerHTML = dates.length
    ? `<tr><th>Date</th>${debts.map((d) => `<th class="num">${esc(d.name)}</th>`).join("")}
       <th class="num">Total debt</th><th class="num">Cash</th></tr>` +
      dates.map((dt) => {
        const row = byDate.get(dt) || {};
        const total = Object.values(row).reduce((a, b) => a + b, 0);
        return `<tr><td>${esc(dt)}</td>` +
          debts.map((d) => `<td class="num">${row[d.id] != null ? fmtMoney(row[d.id]) : "—"}</td>`).join("") +
          `<td class="num"><strong>${Object.keys(row).length ? fmtMoney(total) : "—"}</strong></td>
           <td class="num">${cashByDate.has(dt) ? fmtMoney(cashByDate.get(dt)) : "—"}</td></tr>`;
      }).join("")
    : `<tr><td class="hint">No snapshots yet. Save one above — re-saving the same date overwrites it.</td></tr>`;
}

// ---------- config ----------
const SETTING_FIELDS = [
  ["cash_on_hand", "Cash on hand ($)", "number"],
  ["emergency_floor", "Emergency fund floor ($)", "number"],
  ["monthly_surplus", "Monthly surplus ($)", "number"],
  ["monthly_surplus_after_baby", "Monthly surplus after baby ($)", "number"],
  ["baby_date", "Baby date", "date"],
  ["cc_goal_date", "Cards-at-$0 goal date", "date"],
  ["loan_goal_date", "Loan payoff goal date", "date"],
];
async function renderConfig() {
  const [settings, debts, events] = await Promise.all([
    api.get("/api/settings"), api.get("/api/debts"), api.get("/api/income_events")]);

  const sf = $("#settings-form");
  sf.innerHTML = SETTING_FIELDS.map(([k, label, type]) => `
    <div class="field"><label>${esc(label)}</label>
      <input name="${k}" type="${type}" ${type === "number" ? 'step="100"' : ""} value="${esc(settings[k] || "")}"></div>`)
    .join("") + `<div class="field"><button class="btn" type="submit">Save settings</button></div>`;
  sf.onsubmit = async (e) => {
    e.preventDefault();
    const body = {};
    for (const [k] of SETTING_FIELDS) body[k] = $(`[name="${k}"]`, sf).value;
    await api.put("/api/settings", body);
    toast("Settings saved");
  };

  renderDebtsEditor(debts);
  renderEventsEditor(events, debts);
}

function renderDebtsEditor(debts) {
  const box = $("#debts-editor");
  box.innerHTML = "";
  const field = (label, name, type, value, extra = "") => `
    <div class="field"><label>${esc(label)}</label>
      <input name="${name}" type="${type}" ${extra} value="${value ?? ""}"></div>`;
  for (const d of debts) {
    const fs = document.createElement("fieldset");
    fs.className = "scenario-block";
    fs.innerHTML = `
      <legend>${esc(d.name)}</legend>
      <div class="form-grid">
        ${field("Name", "name", "text", esc(d.name))}
        <div class="field"><label>Kind</label>
          <select name="kind">
            <option value="card" ${d.kind === "card" ? "selected" : ""}>Credit card</option>
            <option value="loan" ${d.kind === "loan" ? "selected" : ""}>Loan</option>
          </select></div>
        ${field("Current balance ($)", "balance", "number", d.balance, 'step="0.01"')}
        ${field("APR % (post-promo)", "apr", "number", d.apr, 'step="0.01"')}
        ${field("Promo APR % (blank = none)", "promo_apr", "number", d.promo_apr, 'step="0.01"')}
        ${field("Promo end date", "promo_end", "date", d.promo_end)}
        ${field("Min payment $ (blank = computed)", "min_payment", "number", d.min_payment, 'step="1"')}
        ${field("Term (months, loans)", "term_months", "number", d.term_months)}
        ${field("Origination date (loans)", "origination_date", "date", d.origination_date)}
        ${field("Original principal (loans)", "original_principal", "number", d.original_principal, 'step="100"')}
        ${field("Payoff plan note", "payoff_plan", "text", esc(d.payoff_plan))}
      </div>
      <div class="row-actions">
        <button class="btn small" data-act="save">Save</button>
        <button class="btn small danger" data-act="delete">Delete</button>
      </div>`;
    fs.addEventListener("click", async (e) => {
      const act = e.target.dataset?.act;
      if (!act) return;
      e.preventDefault();
      if (act === "delete") {
        if (!confirm(`Delete "${d.name}" and its snapshot history?`)) return;
        await api.del(`/api/debts/${d.id}`);
        toast("Debt deleted");
        return renderConfig();
      }
      const val = (n) => $(`[name="${n}"]`, fs).value;
      await api.put(`/api/debts/${d.id}`, {
        name: val("name"), kind: val("kind"),
        balance: num(val("balance")) || 0, apr: num(val("apr")) || 0,
        promo_apr: num(val("promo_apr")), promo_end: val("promo_end") || null,
        min_payment: num(val("min_payment")), term_months: num(val("term_months")),
        origination_date: val("origination_date") || null,
        original_principal: num(val("original_principal")),
        payoff_plan: val("payoff_plan") || null,
      });
      toast("Debt saved");
      renderConfig();
    });
    box.appendChild(fs);
  }
  const addBtn = document.createElement("button");
  addBtn.className = "btn ghost";
  addBtn.textContent = "+ New debt";
  addBtn.addEventListener("click", async () => {
    await api.post("/api/debts", { name: "New debt", kind: "card", balance: 0, apr: 0 });
    renderConfig();
  });
  box.appendChild(addBtn);
}

function renderEventsEditor(events, debts) {
  const box = $("#events-editor");
  box.innerHTML = "";
  const debtOptions = (sel) =>
    `<option value="">— none (all to cash)</option>` +
    debts.map((d) => `<option value="${d.id}" ${sel === d.id ? "selected" : ""}>${esc(d.name)}</option>`).join("");
  for (const ev of events) {
    const fs = document.createElement("fieldset");
    fs.className = "scenario-block";
    fs.innerHTML = `
      <legend>${esc(ev.name)}</legend>
      <div class="form-grid">
        <div class="field"><label>Name</label><input name="name" value="${esc(ev.name)}"></div>
        <div class="field"><label>Kind</label>
          <select name="kind">
            ${["rsu", "bonus", "other"].map((k) =>
              `<option value="${k}" ${ev.kind === k ? "selected" : ""}>${k.toUpperCase()}</option>`).join("")}
          </select></div>
        <div class="field"><label>Date</label><input name="event_date" type="date" value="${esc(ev.event_date)}"></div>
        <div class="field"><label>Net amount ($)</label>
          <input name="amount" type="number" step="100" value="${ev.amount}"></div>
        <div class="field"><label>Allocate to</label>
          <select name="allocate_debt_id">${debtOptions(ev.allocate_debt_id)}</select></div>
        <div class="field"><label>Amount to debt ($)</label>
          <input name="allocate_amount" type="number" step="100" value="${ev.allocate_amount ?? ""}"></div>
      </div>
      <div class="row-actions">
        <button class="btn small" data-act="save">Save</button>
        <button class="btn small danger" data-act="delete">Delete</button>
      </div>`;
    fs.addEventListener("click", async (e) => {
      const act = e.target.dataset?.act;
      if (!act) return;
      e.preventDefault();
      if (act === "delete") {
        if (!confirm(`Delete event "${ev.name}"?`)) return;
        await api.del(`/api/income_events/${ev.id}`);
        toast("Event deleted");
        return renderConfig();
      }
      const val = (n) => $(`[name="${n}"]`, fs).value;
      await api.put(`/api/income_events/${ev.id}`, {
        name: val("name"), kind: val("kind"), event_date: val("event_date"),
        amount: num(val("amount")) || 0,
        allocate_debt_id: num(val("allocate_debt_id")),
        allocate_amount: num(val("allocate_amount")),
      });
      toast("Event saved");
      renderConfig();
    });
    box.appendChild(fs);
  }
  const addBtn = document.createElement("button");
  addBtn.className = "btn ghost";
  addBtn.textContent = "+ New income event";
  addBtn.addEventListener("click", async () => {
    await api.post("/api/income_events", {
      name: "New event", kind: "bonus",
      event_date: new Date().toISOString().slice(0, 10), amount: 0,
    });
    renderConfig();
  });
  box.appendChild(addBtn);
}

renderDashboard();
