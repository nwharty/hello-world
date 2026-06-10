/* global React, Mark, Wordmark, Check, Eyebrow, SheetFrame, St, GuideCover, TabStrip */
// product-cards.jsx — the redesigned PRODUCT: workbook tabs + the guide.

/* ---------- Start Here (onboarding read-me, redesigned) ---------- */
function ProdStartHere() {
  const tabs = [
    ["First 30 Days", "var(--navy)"], ["Task Log", null], ["Key Contacts", null],
    ["Documents", null], ["Notifications", null], ["Assets", "var(--gold)"],
    ["Debts", null], ["Services", null], ["Estate Ledger", "var(--gold)"],
    ["Distributions", null], ["Final Accounting", "#b00020"],
  ];
  const steps = [
    "Read the companion guide first — it tells you what's urgent and what can wait.",
    "Work the First 30 Days tab, top to bottom. You don't have to do everything at once.",
    "Log every call, email, and letter. Months from now, this record protects you.",
    "Record each asset, debt, and document as you find them. Values can come later.",
    "Track every dollar in the Estate Ledger. Final Accounting totals it for you.",
  ];
  return (
    <SheetFrame name="Executor_Estate_Kit.xlsx" active="Start Here" fill bodyStyle={{ padding: 0 }}>
      <div style={{ display: "grid", gridTemplateColumns: "1.25fr 1fr", minHeight: 600 }}>
        <div style={{ padding: "38px 40px", borderRight: "1px solid var(--line-soft)" }}>
          <Mark size={50} />
          <h2 className="serif" style={{ fontSize: 38, fontWeight: 500, color: "var(--navy)", margin: "22px 0 8px", letterSpacing: "-.01em" }}>
            Executor &amp; Estate<br />Settlement Kit
          </h2>
          <p className="sans" style={{ fontSize: 18, color: "var(--ink-55)", margin: 0 }}>A calm, complete system for settling an estate — one tab at a time.</p>
          <div className="eyebrow" style={{ marginTop: 34, marginBottom: 18 }}>How to use this kit</div>
          <ol style={{ margin: 0, padding: 0, listStyle: "none", display: "flex", flexDirection: "column", gap: 15 }}>
            {steps.map((s, i) => (
              <li key={i} style={{ display: "flex", gap: 15, alignItems: "flex-start" }}>
                <span style={{ flex: "none", width: 28, height: 28, borderRadius: 8, background: "var(--sage)", color: "var(--sage-ink)", display: "grid", placeItems: "center", fontFamily: "var(--serif)", fontWeight: 600, fontSize: 16 }}>{i + 1}</span>
                <span className="sans" style={{ fontSize: 16.5, color: "var(--navy)", lineHeight: 1.45, paddingTop: 3 }}>{s}</span>
              </li>
            ))}
          </ol>
        </div>
        <div style={{ padding: "38px 40px", background: "var(--paper)" }}>
          <div className="eyebrow" style={{ marginBottom: 18 }}>The tabs</div>
          <div style={{ display: "flex", flexDirection: "column", gap: 4 }}>
            {tabs.map(([name, c]) => (
              <div key={name} style={{ display: "flex", alignItems: "center", gap: 12, padding: "10px 12px", borderRadius: 9, background: c ? "rgba(255,253,249,.8)" : "transparent" }}>
                <span style={{ width: 9, height: 9, borderRadius: 3, background: c || "var(--line)", flex: "none" }} />
                <span className="sans" style={{ fontSize: 16.5, fontWeight: c ? 700 : 500, color: c ? "var(--navy)" : "var(--ink-70)" }}>{name}</span>
              </div>
            ))}
          </div>
          <div style={{ marginTop: 22, padding: "16px 18px", background: "var(--sage)", borderRadius: 12 }}>
            <span className="mono" style={{ fontSize: 12.5, color: "var(--sage-ink)", lineHeight: 1.5, display: "block" }}>
              GOOGLE SHEETS — upload at sheets.google.com via File &gt; Import. Every formula works.
            </span>
          </div>
        </div>
      </div>
    </SheetFrame>
  );
}

/* ---------- Assets tab (data entry, totals) ---------- */
function ProdAssets() {
  const rows = [
    ["Bank account", "First National · checking ··4821", "Sole name", "$ 38,210.00", "Valued"],
    ["Investment", "Vanguard brokerage ··0394", "TOD", "$ 412,880.00", "Located"],
    ["Retirement", "Fidelity IRA ··7720", "Sole name", "$ 196,400.00", "Located"],
    ["Real estate", "128 Linden Ave — primary home", "Joint", "$ 415,000.00", "Valued"],
    ["Vehicle", "2019 Subaru Outback", "Sole name", "$ 18,900.00", "Valued"],
    ["Life insurance", "MetLife policy ··1102", "Joint", "$ 250,000.00", "Located"],
    ["Personal property", "Furnishings & jewelry (appraised)", "Sole name", "$ 22,400.00", "Valued"],
  ];
  return (
    <SheetFrame name="Executor_Estate_Kit.xlsx" active="Assets" fill
      title="Asset Inventory" subtitle="Every asset, valued as of the date of death — the foundation of the inventory filing and final accounting.">
      <table className="grid">
        <thead><tr><th style={{ width: 150 }}>Category</th><th>Institution / Description</th><th style={{ width: 120 }}>How titled</th><th style={{ width: 170 }}>Value at death</th><th style={{ width: 120 }}>Status</th></tr></thead>
        <tbody>
          {rows.map(([cat, desc, titled, val, st]) => (
            <tr key={desc}>
              <td><span style={{ display: "inline-flex", alignItems: "center", gap: 7, fontWeight: 600, color: "var(--navy)" }}>
                <span style={{ width: 8, height: 8, borderRadius: 2, background: "var(--gold)" }} />{cat}
              </span></td>
              <td className="muted" style={{ color: "var(--ink-70)" }}>{desc}</td>
              <td><span className="st st-todo" style={{ background: "#eef1f4" }}>{titled}</span></td>
              <td className="money">{val}</td>
              <td><span className="st st-prog" style={{ background: "var(--sage)", color: "var(--sage-ink)" }}>{st}</span></td>
            </tr>
          ))}
          <tr>
            <td colSpan={3} style={{ textAlign: "right", fontWeight: 800, color: "var(--navy)", background: "var(--sage)", fontSize: 15 }}>TOTAL — beginning inventory</td>
            <td className="money" style={{ background: "var(--sage)", fontSize: 18 }}>$ 1,353,790.00</td>
            <td style={{ background: "var(--sage)" }}></td>
          </tr>
        </tbody>
      </table>
    </SheetFrame>
  );
}

/* ---------- Estate Ledger (money in / out) ---------- */
function ProdLedger() {
  const rows = [
    ["03/14", "in", "Asset sale proceeds", "Subaru Outback — sold", "$ 18,900.00"],
    ["03/20", "out", "Funeral expense", "Restland Funeral Home", "$ 9,420.00"],
    ["03/28", "in", "Refunds", "Annual insurance refund", "$ 612.00"],
    ["04/02", "out", "Attorney / CPA fees", "Probate filing + counsel", "$ 2,150.00"],
    ["04/11", "out", "Debt payment", "Chase credit card ··6610", "$ 4,318.00"],
    ["04/19", "in", "Interest / dividends", "Vanguard brokerage", "$ 1,204.00"],
    ["05/01", "out", "Property upkeep", "Lawn, utilities, insurance", "$ 1,070.00"],
  ];
  return (
    <SheetFrame name="Executor_Estate_Kit.xlsx" active="Estate Ledger" fill
      title="Estate Ledger — Money In / Money Out" subtitle="Every transaction in the estate account. Final Accounting totals this automatically.">
      <table className="grid">
        <thead><tr><th style={{ width: 80 }}>Date</th><th style={{ width: 130 }}>Type</th><th style={{ width: 210 }}>Category</th><th>Payer / Payee</th><th style={{ width: 150 }}>Amount</th><th style={{ width: 110 }}>Receipt</th></tr></thead>
        <tbody>
          {rows.map(([d, type, cat, payee, amt]) => (
            <tr key={d + payee}>
              <td className="mono" style={{ fontSize: 13, color: "var(--ink-55)" }}>{d}</td>
              <td><span className="st" style={{ background: type === "in" ? "var(--sage)" : "#f6e8e3", color: type === "in" ? "var(--sage-ink)" : "#a05a3e" }}>
                {type === "in" ? "Money in" : "Money out"}</span></td>
              <td className="muted" style={{ color: "var(--ink-70)" }}>{cat}</td>
              <td className="strong">{payee}</td>
              <td className="money" style={{ color: type === "in" ? "var(--ok)" : "var(--navy)" }}>{type === "in" ? "+ " : "– "}{amt.replace("$ ", "")}</td>
              <td><span style={{ display: "inline-flex", alignItems: "center", gap: 6, color: "var(--sage-ink)", fontWeight: 600, fontSize: 13 }}><Check s={13} /> Kept</span></td>
            </tr>
          ))}
        </tbody>
      </table>
    </SheetFrame>
  );
}

/* ---------- Guide cover (full booklet) ---------- */
function ProdGuideCover() {
  return (
    <div style={{ width: "100%", height: "100%", background: "linear-gradient(165deg,#27425d,#172838)", color: "var(--paper)", padding: 64, display: "flex", flexDirection: "column", position: "relative", overflow: "hidden", fontFamily: "var(--sans)" }}>
      <div style={{ position: "absolute", inset: 22, borderRadius: 8, boxShadow: "inset 0 0 0 1px rgba(212,177,100,.4), inset 0 0 0 6px rgba(212,177,100,.10)" }} />
      <div style={{ position: "relative", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <Mark size={56} />
        <span className="mono" style={{ fontSize: 13, letterSpacing: ".18em", color: "rgba(250,247,241,.55)" }}>PDF GUIDE</span>
      </div>
      <div style={{ flex: 1 }} />
      <div className="eyebrow" style={{ color: "var(--gold-soft)", position: "relative" }}>The companion guide</div>
      <h1 className="serif" style={{ fontSize: 64, fontWeight: 500, lineHeight: 1.03, margin: "16px 0 0", position: "relative" }}>
        The Executor's<br />First 30 Days
      </h1>
      <div className="rule-gold" style={{ marginTop: 26, position: "relative" }} />
      <p className="sans" style={{ fontSize: 21, color: "rgba(250,247,241,.74)", marginTop: 24, maxWidth: 440, lineHeight: 1.5, position: "relative" }}>
        A calm, step-by-step guide for the person who has just been handed the hardest
        job nobody trains you for.
      </p>
      <div style={{ flex: 1 }} />
      <div className="sans" style={{ position: "relative", fontSize: 14, color: "rgba(250,247,241,.5)" }}>Companion to the 12-tab Estate Workbook</div>
    </div>
  );
}

/* ---------- Guide interior spread ---------- */
function ProdGuideSpread() {
  const Page = ({ children }) => (
    <div style={{ flex: 1, background: "var(--white)", padding: "52px 50px", display: "flex", flexDirection: "column" }}>{children}</div>
  );
  return (
    <div style={{ width: "100%", height: "100%", display: "flex", gap: 2, background: "var(--line)", boxShadow: "var(--shadow-md)", fontFamily: "var(--sans)" }}>
      <Page>
        <div className="eyebrow">Before anything else</div>
        <h2 className="serif" style={{ fontSize: 34, fontWeight: 500, color: "var(--navy)", margin: "14px 0 18px", lineHeight: 1.08 }}>Three rules before you do anything</h2>
        <p className="sans" style={{ fontSize: 16, color: "var(--ink-70)", lineHeight: 1.6, margin: 0 }}>
          Almost every serious, personally costly executor mistake is a violation of one of these
          three rules. Read them now, and re-read them any time you feel pressured.
        </p>
        <div style={{ display: "flex", flexDirection: "column", gap: 16, marginTop: 24 }}>
          {[
            ["1", "Never mix estate money with your own.", "Commingling funds is the fastest way to become personally liable."],
            ["2", "Distribute nothing until debts and taxes are settled.", "If the money runs short later, the difference can come from your pocket."],
            ["3", "Write everything down.", "Beneficiaries are entitled to an accounting you can't rebuild from memory."],
          ].map(([n, t, d]) => (
            <div key={n} style={{ display: "flex", gap: 16 }}>
              <span className="serif" style={{ fontSize: 30, color: "var(--gold)", fontWeight: 500, lineHeight: 1, flex: "none", width: 30 }}>{n}</span>
              <div>
                <div className="sans" style={{ fontSize: 17, fontWeight: 700, color: "var(--navy)" }}>{t}</div>
                <div className="sans" style={{ fontSize: 15, color: "var(--ink-55)", marginTop: 3, lineHeight: 1.5 }}>{d}</div>
              </div>
            </div>
          ))}
        </div>
        <div style={{ flex: 1 }} />
        <div className="mono" style={{ fontSize: 12, color: "var(--ink-40)", marginTop: 20 }}>2 — The Executor's First 30 Days</div>
      </Page>
      <Page>
        <div className="eyebrow">Week 1 · Protect and gather</div>
        <h2 className="serif" style={{ fontSize: 34, fontWeight: 500, color: "var(--navy)", margin: "14px 0 18px", lineHeight: 1.08 }}>Nothing this week needs the court</h2>
        <ul className="clist" style={{ gap: 16 }}>
          {[
            ["Find the original will.", "Check the safe, desk, attorney, and bank safe-deposit box."],
            ["Order 10–15 certified death certificates.", "Nearly every institution demands its own copy."],
            ["Secure the property.", "Lock the home, garage and vehicles; re-key if needed."],
            ["Forward the mail.", "Incoming mail surfaces accounts and debts no one knew about."],
          ].map(([a, b]) => (
            <li key={a}><span className="tick"><Check /></span><span className="ct" style={{ fontSize: 16 }}><b>{a}</b><span style={{ fontSize: 14.5 }}>{b}</span></span></li>
          ))}
        </ul>
        <div style={{ marginTop: 24, padding: "18px 20px", background: "var(--sage)", borderRadius: 12 }}>
          <div className="sans" style={{ fontSize: 15, color: "var(--sage-ink)", lineHeight: 1.55 }}>
            <b>The truth that makes this manageable:</b> estate settlement is a sequence, not a pile.
            A few things are genuinely urgent. Most of the rest waits politely until the court appoints you.
          </div>
        </div>
        <div style={{ flex: 1 }} />
        <div className="mono" style={{ fontSize: 12, color: "var(--ink-40)", marginTop: 20, textAlign: "right" }}>The Executor's First 30 Days — 3</div>
      </Page>
    </div>
  );
}

Object.assign(window, { ProdStartHere, ProdAssets, ProdLedger, ProdGuideCover, ProdGuideSpread });
