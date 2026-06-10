/* global React, Mark, Wordmark, Check, Stars, Eyebrow, Stripe, SheetFrame, St, StarIcon */
// listing-cards-1.jsx — Etsy carousel images 01–05.
// Each card renders at 1080 × 1350 (4:5 portrait, Etsy-friendly).

const W = 1080, H = 1350;

function CardShell({ children, bg = "var(--paper)", pad = 76, style }) {
  return (
    <div style={{ width: W, height: H, background: bg, position: "relative", overflow: "hidden", fontFamily: "var(--sans)", ...style }}>
      <div style={{ position: "absolute", inset: 0, padding: pad, display: "flex", flexDirection: "column", height: "100%" }}>
        {children}
      </div>
    </div>
  );
}

function CardTop({ i, dark }) {
  return (
    <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", flex: "none" }}>
      <Wordmark size={19} sub={false} color={dark ? "var(--paper)" : "var(--navy)"} />
      <span className="mono" style={{ fontSize: 14, letterSpacing: ".16em", color: dark ? "rgba(250,247,241,.55)" : "var(--ink-40)" }}>
        {String(i).padStart(2, "0")} / 10
      </span>
    </div>
  );
}

// A small navy booklet cover for the PDF guide.
function GuideCover({ w = 300, label = true }) {
  const h = w * 1.29;
  return (
    <div style={{
      width: w, height: h, background: "linear-gradient(160deg,#27425d,#1a2e42)", borderRadius: 14,
      boxShadow: "var(--shadow-lg)", padding: w * 0.12, display: "flex", flexDirection: "column",
      color: "var(--paper)", position: "relative", overflow: "hidden", flex: "none",
    }}>
      <div style={{ position: "absolute", inset: 0, boxShadow: "inset 0 0 0 1px rgba(212,177,100,.35), inset 0 0 0 7px rgba(212,177,100,.12)", borderRadius: 14, margin: 9 }} />
      <Mark size={w * 0.2} />
      <div style={{ flex: 1 }} />
      {label && <div className="eyebrow" style={{ fontSize: w * 0.044, color: "var(--gold-soft)" }}>The companion guide</div>}
      <div className="serif" style={{ fontSize: w * 0.135, lineHeight: 1.04, marginTop: 10, fontWeight: 500 }}>
        The Executor's<br />First 30 Days
      </div>
      <div className="rule-gold" style={{ marginTop: 16, width: w * 0.22 }} />
      <div className="sans" style={{ fontSize: w * 0.05, color: "rgba(250,247,241,.7)", marginTop: 14, lineHeight: 1.4 }}>
        A calm, step-by-step walkthrough of the critical first month.
      </div>
    </div>
  );
}

/* ============================================================ 01 · HERO */
function Card01() {
  return (
    <CardShell pad={70}>
      <CardTop i={1} />
      <div style={{ marginTop: 38, flex: "none" }}>
        <Eyebrow>Instant digital download</Eyebrow>
        <h1 className="display" style={{ fontSize: 74, margin: "16px 0 0", maxWidth: 880 }}>
          The complete<br />executor system.
        </h1>
        <p className="lede" style={{ fontSize: 25, margin: "20px 0 0", maxWidth: 720 }}>
          A 12-tab workbook and a 30-day guide that give every task, document, dollar,
          and deadline a place to live — so nothing rests on your memory during the
          hardest month to rely on it.
        </p>
      </div>

      {/* device cluster */}
      <div style={{ position: "relative", flex: 1, marginTop: 26 }}>
        <div style={{ position: "absolute", left: -6, right: 150, top: 14, transform: "rotate(-1.2deg)" }}>
          <SheetFrame name="Executor_Estate_Kit.xlsx" active="First 30 Days"
            title="The First 30 Days" subtitle="Work top to bottom. Done and N/A both count as finished."
            bodyStyle={{ maxHeight: 300, overflow: "hidden" }}>
            <table className="grid">
              <thead><tr><th style={{ width: 96 }}>Priority</th><th>Task</th><th style={{ width: 132 }}>Status</th></tr></thead>
              <tbody>
                {[
                  ["Week 1", "Locate the original will & codicils", "done"],
                  ["Week 1", "Order 10–15 certified death certificates", "done"],
                  ["Week 2", "File petition for probate with the court", "prog"],
                  ["Week 2", "Open an estate checking account", "todo"],
                  ["Week 3–4", "Begin asset inventory at date-of-death value", "todo"],
                ].map(([p, t, s]) => (
                  <tr key={t}><td><span className="phase">{p}</span></td><td className="strong">{t}</td><td><St kind={s} /></td></tr>
                ))}
              </tbody>
            </table>
          </SheetFrame>
        </div>
        <div style={{ position: "absolute", right: -8, bottom: 6 }}>
          <GuideCover w={272} />
        </div>
      </div>

      {/* trust strip */}
      <div style={{ flex: "none", display: "flex", alignItems: "center", gap: 18, paddingTop: 18, borderTop: "1px solid var(--line)" }}>
        <Stars />
        <span className="sans" style={{ color: "var(--ink-70)", fontSize: 19, fontWeight: 600 }}>
          Excel&nbsp;+&nbsp;Google Sheets
        </span>
        <span style={{ width: 5, height: 5, borderRadius: 9, background: "var(--ink-40)" }} />
        <span className="sans" style={{ color: "var(--ink-70)", fontSize: 19, fontWeight: 600 }}>12-tab workbook + 30-day guide</span>
      </div>
    </CardShell>
  );
}

/* ============================================================ 02 · TAB OVERVIEW */
function Card02() {
  const tabs = [
    ["01", "First 30 Days", "What's urgent, what can wait"],
    ["02", "Task Log", "Every call & letter, documented"],
    ["03", "Key Contacts", "Everyone you'll call twice"],
    ["04", "Documents", "Where every paper lives"],
    ["05", "Notifications", "Who to tell + cert. copies"],
    ["06", "Assets", "Full date-of-death inventory"],
    ["07", "Debts", "Verified before a dollar is paid"],
    ["08", "Services", "Subscriptions to cancel"],
    ["09", "Estate Ledger", "Every dollar in and out"],
    ["10", "Distributions", "Who received what, signed"],
    ["11", "Final Accounting", "The court summary, automatic"],
    ["12", "Start Here", "Read-me + Google Sheets setup"],
  ];
  return (
    <CardShell>
      <CardTop i={2} />
      <div style={{ marginTop: 40, flex: "none", maxWidth: 820 }}>
        <Eyebrow>What's inside</Eyebrow>
        <h1 className="display" style={{ fontSize: 56, margin: "14px 0 0" }}>
          Twelve tabs, in the order the job actually happens.
        </h1>
      </div>
      <div style={{ marginTop: 40, flex: 1, display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16, alignContent: "start" }}>
        {tabs.map(([n, name, desc]) => (
          <div key={n} style={{ background: "var(--white)", borderRadius: 14, padding: "20px 22px", boxShadow: "var(--shadow-sm)", display: "flex", gap: 16, alignItems: "center" }}>
            <span className="serif" style={{ fontSize: 30, color: "var(--gold)", fontWeight: 500, width: 44, flex: "none" }}>{n}</span>
            <div>
              <div className="sans" style={{ fontSize: 21, fontWeight: 700, color: "var(--navy)" }}>{name}</div>
              <div className="sans" style={{ fontSize: 15.5, color: "var(--ink-55)", marginTop: 2 }}>{desc}</div>
            </div>
          </div>
        ))}
      </div>
    </CardShell>
  );
}

/* ============================================================ 03 · FIRST 30 DAYS SCREEN */
function Card03() {
  const rows = [
    ["Week 1", "Locate the original will (and any codicils)", "Check the safe, desk, attorney, bank box.", "done"],
    ["Week 1", "Order 10–15 certified death certificates", "Every institution wants its own copy.", "done"],
    ["Week 1", "Secure the home, vehicles & valuables", "You protect estate property from now on.", "done"],
    ["Week 2", "File the will & petition for probate", "Nothing official happens until you're appointed.", "prog"],
    ["Week 2", "Get an EIN, then open an estate account", "The estate is its own taxpayer.", "prog"],
    ["Week 2–3", "Notify SSA, employer, insurers & banks", "Benefits stop; accounts freeze or retitle.", "todo"],
    ["Week 3–4", "Begin the asset inventory", "Date-of-death values become your opening balance.", "todo"],
  ];
  return (
    <CardShell bg="var(--sage)">
      <CardTop i={3} />
      <div style={{ marginTop: 36, flex: "none", maxWidth: 840 }}>
        <Eyebrow>Tab 01 · First 30 Days</Eyebrow>
        <h1 className="display" style={{ fontSize: 56, margin: "14px 0 0" }}>
          Know what's urgent — and what can wait.
        </h1>
        <p className="lede" style={{ fontSize: 23, margin: "16px 0 0", maxWidth: 760 }}>
          Estate settlement is a sequence, not a pile. The checklist is ordered by
          priority, so you always know the one next right thing.
        </p>
      </div>
      <div style={{ marginTop: 30, flex: 1, display: "flex", alignItems: "flex-start" }}>
        <SheetFrame name="Executor_Estate_Kit.xlsx" active="First 30 Days" bodyStyle={{ maxHeight: 560, overflow: "hidden" }}>
          <table className="grid">
            <thead><tr><th style={{ width: 104 }}>Priority</th><th>Task</th><th>Why it matters</th><th style={{ width: 128 }}>Status</th></tr></thead>
            <tbody>
              {rows.map(([p, t, w, s]) => (
                <tr key={t}>
                  <td><span className="phase">{p}</span></td>
                  <td className="strong" style={{ maxWidth: 320 }}>{t}</td>
                  <td className="muted">{w}</td>
                  <td><St kind={s} /></td>
                </tr>
              ))}
            </tbody>
          </table>
        </SheetFrame>
      </div>
    </CardShell>
  );
}

/* ============================================================ 04 · FINAL ACCOUNTING (differentiator) */
function Card04() {
  const lines = [
    ["Beginning inventory", "at date-of-death value", "$842,300.00", false],
    ["＋ Receipts during administration", "asset sales, refunds, income", "$ 38,910.00", false],
    ["－ Disbursements", "debts, fees, taxes, upkeep", "$ 71,540.00", false],
    ["－ Distributions to beneficiaries", "with signed releases", "$ 305,000.00", false],
    ["Remaining estate balance", "matches the estate bank account", "$504,670.00", true],
  ];
  return (
    <CardShell bg="var(--navy)">
      <CardTop i={4} dark />
      <div style={{ marginTop: 36, flex: "none", maxWidth: 880 }}>
        <Eyebrow color="var(--gold-soft)">The part that actually trips people up</Eyebrow>
        <h1 className="display" style={{ fontSize: 60, margin: "14px 0 0", color: "var(--paper)" }}>
          The hardest report<br />writes itself.
        </h1>
        <p className="lede" style={{ fontSize: 23, margin: "16px 0 0", maxWidth: 770, color: "rgba(250,247,241,.72)" }}>
          Courts and beneficiaries are entitled to a formal accounting of every dollar.
          Fill in the tabs as you go and the Final Accounting builds itself — in the exact
          structure they expect.
        </p>
      </div>
      <div style={{ marginTop: "auto", flex: "none", position: "relative" }}>
        <div style={{ background: "var(--white)", borderRadius: 18, padding: "30px 34px", boxShadow: "var(--shadow-lg)" }}>
          <div className="sans" style={{ fontSize: 13, fontFamily: "var(--mono)", letterSpacing: ".14em", textTransform: "uppercase", color: "var(--ink-55)", marginBottom: 18 }}>
            Final Accounting Summary
          </div>
          {lines.map(([a, b, v, total]) => (
            <div key={a} style={{
              display: "flex", alignItems: "baseline", justifyContent: "space-between", gap: 20,
              padding: total ? "20px 18px 4px" : "13px 0", borderTop: total ? "2px solid var(--navy)" : "1px solid var(--line-soft)",
              marginTop: total ? 12 : 0, background: total ? "var(--sage)" : "transparent", borderRadius: total ? 12 : 0,
              paddingLeft: total ? 18 : 0, paddingRight: total ? 18 : 0, paddingBottom: total ? 20 : 13,
            }}>
              <div>
                <div className="sans" style={{ fontSize: total ? 24 : 20, fontWeight: total ? 800 : 600, color: "var(--navy)" }}>{a}</div>
                <div className="sans" style={{ fontSize: 14.5, color: "var(--ink-55)" }}>{b}</div>
              </div>
              <div className="money" style={{ fontSize: total ? 30 : 21, color: total ? "var(--navy)" : "var(--ink-70)" }}>{v}</div>
            </div>
          ))}
        </div>
        <div style={{ position: "absolute", top: -26, right: -10, transform: "rotate(3deg)", background: "var(--clay)", color: "#fff", padding: "12px 20px", borderRadius: 999, fontFamily: "var(--sans)", fontWeight: 800, fontSize: 18, boxShadow: "var(--shadow-md)" }}>
          calculates itself ✦
        </div>
      </div>
    </CardShell>
  );
}

/* ============================================================ 05 · GUIDE */
function Card05() {
  return (
    <CardShell bg="var(--paper-2)">
      <CardTop i={5} />
      <div style={{ marginTop: 36, flex: "none", maxWidth: 840 }}>
        <Eyebrow>The companion guide · PDF</Eyebrow>
        <h1 className="display" style={{ fontSize: 56, margin: "14px 0 0" }}>
          Start calm. A guide that sequences the whole job.
        </h1>
      </div>
      <div style={{ marginTop: 30, flex: 1, display: "flex", alignItems: "center", gap: 44 }}>
        <GuideCover w={340} />
        <div style={{ flex: 1 }}>
          <p className="lede" style={{ fontSize: 23, margin: 0, maxWidth: 440 }}>
            Most kits hand you empty tables. This one opens with a calm walkthrough of the
            critical first month — including:
          </p>
          <ul className="clist" style={{ marginTop: 26 }}>
            {[
              ["The three rules", "that protect you from personal liability"],
              ["Week-by-week sequence", "Week 1 protect & gather → appointment → notify → inventory"],
              ["The five mistakes", "that cost executors their own money"],
              ["When to get help", "and why the estate — not you — pays for it"],
            ].map(([a, b]) => (
              <li key={a}><span className="tick"><Check /></span><span className="ct"><b>{a}</b><span>{b}</span></span></li>
            ))}
          </ul>
        </div>
      </div>
    </CardShell>
  );
}

Object.assign(window, { CardShell, CardTop, GuideCover, Card01, Card02, Card03, Card04, Card05, LISTING_W: W, LISTING_H: H });
