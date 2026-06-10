/* global React */
// kit-primitives.jsx — shared building blocks for The Executor Kit design set.
// Exports to window so the listing + product card files can use them.

const TABS = [
  ["Start Here", "var(--gold)"],
  ["First 30 Days", "var(--navy)"],
  ["Task Log", "transparent"],
  ["Key Contacts", "transparent"],
  ["Documents", "transparent"],
  ["Notifications", "transparent"],
  ["Assets", "var(--gold)"],
  ["Debts", "transparent"],
  ["Services", "transparent"],
  ["Estate Ledger", "var(--gold)"],
  ["Distributions", "transparent"],
  ["Final Accounting", "#b00020"],
];

function Mark({ size = 44 }) {
  return (
    <span className="mark" style={{ width: size, height: size }}>
      <span className="star" />
    </span>
  );
}

function Wordmark({ size = 22, sub = true, color }) {
  return (
    <span className="wordmark" style={{ fontSize: size, color }}>
      <Mark size={size * 1.5} />
      <span style={{ display: "flex", flexDirection: "column", gap: 3, lineHeight: 1 }}>
        <span style={{ letterSpacing: "-.01em" }}>The Executor Kit</span>
        {sub && (
          <span className="wm-sub" style={{ fontSize: size * 0.34 }}>
            Estate settlement, organized
          </span>
        )}
      </span>
    </span>
  );
}

function Check({ s = 14, c = "currentColor" }) {
  return (
    <svg viewBox="0 0 24 24" width={s} height={s} fill="none" stroke={c} strokeWidth="3" strokeLinecap="round" strokeLinejoin="round">
      <polyline points="20 6 9 17 4 12" />
    </svg>
  );
}

function StarIcon({ s = 18 }) {
  return (
    <svg viewBox="0 0 24 24" width={s} height={s} fill="currentColor">
      <path d="M12 2l2.9 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77 5.82 21l1.18-6.88-5-4.87 7.1-1.01z" />
    </svg>
  );
}

function Stars({ n = 5 }) {
  return (
    <span className="stars">
      {Array.from({ length: n }).map((_, i) => <StarIcon key={i} />)}
    </span>
  );
}

function Eyebrow({ children, color, style }) {
  return <div className="eyebrow" style={{ color, ...style }}>{children}</div>;
}

function Stripe({ label, h = 160, style }) {
  return (
    <div className="stripe-ph" style={{ height: h, ...style }}>
      <span>{label}</span>
    </div>
  );
}

// The bottom tab strip of the workbook, with one tab marked active.
function TabStrip({ active = "Start Here" }) {
  return (
    <div className="tabs">
      {TABS.map(([name, color]) => (
        <div key={name} className={"tab" + (name === active ? " active" : "")}>
          <span className="swatch" style={{ background: color === "transparent" ? "var(--line)" : color }} />
          {name}
        </div>
      ))}
    </div>
  );
}

// A full "redesigned workbook" surface: chrome toolbar + title + children + tabs.
// fill=true makes the sheet expand to its container's height (tabs pinned to bottom).
function SheetFrame({ name, tag = "Excel · Google Sheets", title, subtitle, active, children, bodyStyle, width = "100%", fill }) {
  const outer = fill ? { width, height: "100%", display: "flex", flexDirection: "column" } : { width };
  const body = fill ? { flex: 1, minHeight: 0, ...bodyStyle } : bodyStyle;
  return (
    <div className="sheet" style={outer}>
      <div className="sheet-toolbar">
        <span className="dot" style={{ background: "#e6a39a" }} />
        <span className="dot" style={{ background: "#e8cf8f" }} />
        <span className="dot" style={{ background: "#a9cdaa" }} />
        <span className="sheet-name" style={{ marginLeft: 6 }}>{name}</span>
        <span className="grow" />
        <span className="sheet-tag">{tag}</span>
      </div>
      {title && (
        <div className="sheet-title">
          <h3>{title}</h3>
          {subtitle && <p>{subtitle}</p>}
        </div>
      )}
      <div style={body}>{children}</div>
      <TabStrip active={active} />
    </div>
  );
}

// A status chip
function St({ kind }) {
  const map = { done: ["st-done", "Done"], prog: ["st-prog", "In progress"], todo: ["st-todo", "Not started"] };
  const [cls, label] = map[kind] || map.todo;
  return <span className={"st " + cls}>{kind === "done" && <Check s={12} />}{label}</span>;
}

Object.assign(window, { TABS, Mark, Wordmark, Check, StarIcon, Stars, Eyebrow, Stripe, TabStrip, SheetFrame, St });
