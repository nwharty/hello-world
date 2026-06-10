/* global React, CardShell, CardTop, GuideCover, Mark, Wordmark, Check, Stars, Eyebrow, SheetFrame, St */
// listing-cards-2.jsx — Etsy carousel images 06–10.

/* ============================================================ 06 · WHAT'S INCLUDED */
function Card06() {
  const MiniSheet = () => (
    <div style={{ background: "var(--white)", borderRadius: 10, overflow: "hidden", boxShadow: "var(--shadow-sm)", border: "1px solid var(--line-soft)" }}>
      <div style={{ height: 26, background: "var(--navy)" }} />
      {Array.from({ length: 6 }).map((_, i) => (
        <div key={i} style={{ display: "flex", gap: 8, padding: "9px 12px", background: i % 2 ? "rgba(244,237,225,.5)" : "#fff" }}>
          <div style={{ width: "38%", height: 9, borderRadius: 3, background: "var(--line)" }} />
          <div style={{ width: "44%", height: 9, borderRadius: 3, background: "var(--line-soft)" }} />
          <div style={{ width: 34, height: 9, borderRadius: 3, background: i < 3 ? "var(--sage-deep)" : "var(--gold-pale)" }} />
        </div>
      ))}
    </div>
  );
  const Tile = ({ label, title, children, span }) => (
    <div style={{ gridColumn: span ? "span 2" : "span 1", background: "var(--white)", borderRadius: 16, padding: 24, boxShadow: "var(--shadow-sm)", display: "flex", flexDirection: "column", gap: 14 }}>
      <div className="eyebrow" style={{ fontSize: 12 }}>{label}</div>
      <div className="serif" style={{ fontSize: 26, color: "var(--navy)", fontWeight: 500, lineHeight: 1.1 }}>{title}</div>
      {children}
    </div>
  );
  return (
    <CardShell bg="var(--sage)">
      <CardTop i={6} />
      <div style={{ marginTop: 36, flex: "none", maxWidth: 840 }}>
        <Eyebrow>Instant download · nothing ships</Eyebrow>
        <h1 className="display" style={{ fontSize: 56, margin: "14px 0 0" }}>Everything you get, the moment you buy.</h1>
      </div>
      <div style={{ marginTop: 30, flex: 1, display: "grid", gridTemplateColumns: "1fr 1fr", gridAutoRows: "min-content", gap: 16, alignContent: "start" }}>
        <Tile label="The workbook" title="12-tab Estate Workbook" span>
          <MiniSheet />
        </Tile>
        <Tile label="The guide" title="The Executor's First 30 Days">
          <div style={{ display: "flex", justifyContent: "center", paddingTop: 4 }}><GuideCover w={150} label={false} /></div>
        </Tile>
        <Tile label="Both formats — one purchase" title="Excel + Google Sheets">
          <div style={{ display: "flex", gap: 10, flexWrap: "wrap" }}>
            <span className="pill pill-navy" style={{ padding: "8px 16px", fontSize: 16 }}>Excel .xlsx</span>
            <span className="pill pill-line" style={{ padding: "8px 16px", fontSize: 16 }}>Google Sheets</span>
          </div>
        </Tile>
        <Tile label="The differentiator" title="Automatic Final Accounting">
          <p className="sans" style={{ margin: 0, fontSize: 16, color: "var(--ink-55)", lineHeight: 1.45 }}>The court-ready summary totals itself as you go.</p>
        </Tile>
        <Tile label="Setup" title="Works in minutes">
          <p className="sans" style={{ margin: 0, fontSize: 16, color: "var(--ink-55)", lineHeight: 1.45 }}>Open in Excel, or upload to Google Sheets — free, instructions included.</p>
        </Tile>
      </div>
    </CardShell>
  );
}

/* ============================================================ 07 · THREE RULES (liability) */
function Card07() {
  const rules = [
    ["01", "Never mix estate money with your own", "Commingling funds is the fastest way to become personally liable — even with perfect intentions."],
    ["02", "Distribute nothing until debts & taxes are settled", "If the money later runs short, the difference can come out of your pocket. The law puts creditors first."],
    ["03", "Write everything down", "Every call, letter, and dollar. Beneficiaries are entitled to an accounting you can't rebuild from memory."],
  ];
  return (
    <CardShell bg="var(--navy)">
      <CardTop i={7} dark />
      <div style={{ marginTop: 38, flex: "none", maxWidth: 900 }}>
        <Eyebrow color="var(--gold-soft)">What attorneys say actually burns executors</Eyebrow>
        <h1 className="display" style={{ fontSize: 60, margin: "14px 0 0", color: "var(--paper)" }}>
          Three rules that protect<br />you personally.
        </h1>
        <p className="lede" style={{ fontSize: 22, margin: "16px 0 0", maxWidth: 720, color: "rgba(250,247,241,.7)" }}>
          Almost every costly executor mistake breaks one of these. The guide opens with them — so you're protected from page one.
        </p>
      </div>
      <div style={{ marginTop: "auto", flex: "none", display: "flex", flexDirection: "column", gap: 16 }}>
        {rules.map(([n, t, d]) => (
          <div key={n} style={{ display: "flex", gap: 26, alignItems: "flex-start", background: "rgba(250,247,241,.06)", border: "1px solid rgba(212,177,100,.22)", borderRadius: 16, padding: "26px 30px" }}>
            <span className="serif" style={{ fontSize: 46, color: "var(--gold-soft)", fontWeight: 500, lineHeight: 1, flex: "none", width: 70 }}>{n}</span>
            <div>
              <div className="serif" style={{ fontSize: 28, color: "var(--paper)", fontWeight: 500, lineHeight: 1.12 }}>{t}</div>
              <div className="sans" style={{ fontSize: 18, color: "rgba(250,247,241,.66)", marginTop: 8, lineHeight: 1.45, maxWidth: 760 }}>{d}</div>
            </div>
          </div>
        ))}
      </div>
    </CardShell>
  );
}

/* ============================================================ 08 · DEATH CERTIFICATE TRACKER */
function Card08() {
  const rows = [
    ["Social Security Admin.", "Yes", "1", "done"],
    ["Life insurance company", "Yes", "2", "done"],
    ["Banks — each account", "Yes", "4", "done"],
    ["Brokerage / investments", "Yes", "2", "prog"],
    ["DMV — vehicle titles", "Yes", "1", "prog"],
    ["Employer / HR", "Unsure", "1", "todo"],
  ];
  return (
    <CardShell bg="var(--paper-2)">
      <CardTop i={8} />
      <div style={{ marginTop: 36, flex: "none", maxWidth: 860 }}>
        <Eyebrow>Notifications tab · no competitor tracks this</Eyebrow>
        <h1 className="display" style={{ fontSize: 56, margin: "14px 0 0" }}>The one thing every executor runs out of.</h1>
        <p className="lede" style={{ fontSize: 22, margin: "16px 0 0", maxWidth: 720 }}>
          You'll need 10–15 certified death certificates, and every institution wants its own. The tracker
          shows exactly where each copy went — and how many you have left.
        </p>
      </div>
      <div style={{ marginTop: 28, flex: 1, display: "flex", alignItems: "flex-start", gap: 22 }}>
        <SheetFrame name="Executor_Estate_Kit.xlsx" active="Notifications" width={620} bodyStyle={{ maxHeight: 430, overflow: "hidden" }}>
          <table className="grid">
            <thead><tr><th>Who to notify</th><th style={{ width: 120 }}>Cert. copy?</th><th style={{ width: 96 }}>Copies used</th><th style={{ width: 120 }}>Status</th></tr></thead>
            <tbody>
              {rows.map(([who, req, n, s]) => (
                <tr key={who}>
                  <td className="strong">{who}</td>
                  <td className="muted">{req}</td>
                  <td className="money" style={{ textAlign: "center" }}>{n}</td>
                  <td><St kind={s} /></td>
                </tr>
              ))}
            </tbody>
          </table>
        </SheetFrame>
        <div style={{ flex: 1, alignSelf: "stretch", display: "flex", flexDirection: "column", gap: 16, justifyContent: "center" }}>
          <div style={{ background: "var(--navy)", color: "var(--paper)", borderRadius: 18, padding: 26, boxShadow: "var(--shadow-md)" }}>
            <div className="eyebrow" style={{ color: "var(--gold-soft)", fontSize: 12 }}>Certified copies used</div>
            <div className="serif" style={{ fontSize: 64, fontWeight: 500, lineHeight: 1, marginTop: 10 }}>
              11<span style={{ color: "rgba(250,247,241,.5)", fontSize: 34 }}> / 15</span>
            </div>
            <div style={{ height: 10, borderRadius: 99, background: "rgba(250,247,241,.18)", marginTop: 16, overflow: "hidden" }}>
              <div style={{ width: "73%", height: "100%", background: "var(--gold-soft)" }} />
            </div>
            <div className="sans" style={{ fontSize: 15, color: "rgba(250,247,241,.7)", marginTop: 12 }}>Reorder before you hit zero — running out stalls everything for weeks.</div>
          </div>
        </div>
      </div>
    </CardShell>
  );
}

/* ============================================================ 09 · BOTH FORMATS */
function Card09() {
  const Rows = ({ accent }) => (
    <div>
      {Array.from({ length: 7 }).map((_, i) => (
        <div key={i} style={{ display: "flex", gap: 10, padding: "10px 16px", background: i % 2 ? "rgba(244,237,225,.5)" : "#fff", borderBottom: "1px solid var(--line-soft)" }}>
          <div style={{ width: "40%", height: 10, borderRadius: 3, background: "var(--line)" }} />
          <div style={{ width: "36%", height: 10, borderRadius: 3, background: "var(--line-soft)" }} />
          <div style={{ width: 40, height: 10, borderRadius: 3, background: i < 4 ? accent : "var(--gold-pale)" }} />
        </div>
      ))}
    </div>
  );
  const Frame = ({ chrome, badge, accent }) => (
    <div style={{ flex: 1, background: "var(--white)", borderRadius: 16, overflow: "hidden", boxShadow: "var(--shadow-md)", border: "1px solid var(--line-soft)" }}>
      <div style={{ display: "flex", alignItems: "center", gap: 8, height: 44, padding: "0 16px", background: "var(--paper)", borderBottom: "1px solid var(--line)" }}>
        <span style={{ width: 11, height: 11, borderRadius: 9, background: "#e6a39a" }} />
        <span style={{ width: 11, height: 11, borderRadius: 9, background: "#e8cf8f" }} />
        <span style={{ width: 11, height: 11, borderRadius: 9, background: "#a9cdaa" }} />
        <span style={{ marginLeft: 8, fontFamily: "var(--mono)", fontSize: 12.5, color: "var(--ink-55)" }}>{chrome}</span>
      </div>
      <div style={{ height: 30, background: accent, display: "flex", alignItems: "center", paddingLeft: 16 }}>
        <span style={{ fontFamily: "var(--sans)", fontWeight: 700, fontSize: 13, color: "#fff" }}>{badge}</span>
      </div>
      <Rows accent={accent} />
    </div>
  );
  return (
    <CardShell>
      <CardTop i={9} />
      <div style={{ marginTop: 38, flex: "none", maxWidth: 860 }}>
        <Eyebrow>One purchase · two formats</Eyebrow>
        <h1 className="display" style={{ fontSize: 58, margin: "14px 0 0" }}>Excel and Google Sheets. Both included.</h1>
        <p className="lede" style={{ fontSize: 23, margin: "16px 0 0", maxWidth: 740 }}>
          Most sellers split these into two listings and charge you twice. Here, the same workbook
          opens natively in Excel and uploads cleanly to Google Sheets — every formula intact.
        </p>
      </div>
      <div style={{ marginTop: 36, flex: 1, display: "flex", gap: 26, alignItems: "center" }}>
        <Frame chrome="Executor_Estate_Kit.xlsx" badge="MICROSOFT EXCEL" accent="#3a7150" />
        <span className="serif" style={{ fontSize: 30, color: "var(--ink-40)", fontWeight: 500, flex: "none" }}>+</span>
        <Frame chrome="sheets.google.com" badge="GOOGLE SHEETS" accent="#2f7d5a" />
      </div>
      <div style={{ flex: "none", marginTop: 26, display: "flex", justifyContent: "center" }}>
        <span className="pill pill-sage" style={{ padding: "12px 22px", fontSize: 18 }}>
          <Check s={16} /> Free to upload · all formulas work in both
        </span>
      </div>
    </CardShell>
  );
}

/* ============================================================ 10 · TRUST / CLOSING */
function Card10() {
  const steps = [
    ["1", "Purchase", "Instant download — no physical item ships."],
    ["2", "Open it your way", "Use in Excel, or upload to Google Sheets (free)."],
    ["3", "Start with the guide", "Then the First 30 Days tab. The workbook organizes the rest."],
  ];
  return (
    <CardShell bg="var(--paper-2)">
      <CardTop i={10} />
      <div style={{ marginTop: 36, flex: "none", maxWidth: 880 }}>
        <Eyebrow>Why this one</Eyebrow>
        <h1 className="display" style={{ fontSize: 54, margin: "14px 0 0" }}>
          Built with a finance background, for real executors.
        </h1>
      </div>

      <div style={{ marginTop: 32, flex: "none", display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 16 }}>
        {steps.map(([n, t, d]) => (
          <div key={n} style={{ background: "var(--white)", borderRadius: 16, padding: 24, boxShadow: "var(--shadow-sm)" }}>
            <span style={{ width: 40, height: 40, borderRadius: 11, background: "var(--navy)", color: "var(--gold-soft)", display: "grid", placeItems: "center", fontFamily: "var(--serif)", fontSize: 22, fontWeight: 600 }}>{n}</span>
            <div className="sans" style={{ fontSize: 21, fontWeight: 700, color: "var(--navy)", marginTop: 16 }}>{t}</div>
            <div className="sans" style={{ fontSize: 16, color: "var(--ink-55)", marginTop: 6, lineHeight: 1.45 }}>{d}</div>
          </div>
        ))}
      </div>

      <div style={{ marginTop: 26, flex: 1, minHeight: 150, position: "relative" }}>
        <image-slot id="lifestyle-close" style={{ width: "100%", height: "100%", display: "block" }} shape="rounded" radius="18"
          placeholder="Optional — drop a warm lifestyle photo (sunlit desk, hands & coffee, an open notebook)"></image-slot>
      </div>

      <div style={{ flex: "none", marginTop: 24, paddingTop: 22, borderTop: "1px solid var(--line)", display: "flex", alignItems: "center", justifyContent: "space-between", gap: 20 }}>
        <div>
          <Stars />
          <div className="serif" style={{ fontSize: 27, color: "var(--navy)", fontWeight: 500, marginTop: 10, maxWidth: 560 }}>
            “Calmly. Completely. In the order that matters.”
          </div>
          <div className="sans" style={{ fontSize: 13.5, color: "var(--ink-40)", marginTop: 12, maxWidth: 620, lineHeight: 1.4 }}>
            An organizational tool, not legal or tax advice — rules vary by state. Designed to keep you so organized
            that when you do need an attorney or CPA, they bill fewer hours.
          </div>
        </div>
        <Wordmark size={18} />
      </div>
    </CardShell>
  );
}

Object.assign(window, { Card06, Card07, Card08, Card09, Card10 });
