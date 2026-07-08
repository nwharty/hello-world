"""One-page monthly status PDF, written with a minimal pure-Python PDF writer
(no dependencies). Letter-size, Helvetica only."""
from datetime import date

PAGE_W, PAGE_H = 612, 792  # US Letter, points
MARGIN = 54


class MiniPDF:
    """Just enough PDF: text in Helvetica/Helvetica-Bold, lines, one page."""

    def __init__(self):
        self.ops = []

    _ASCII = {"—": "-", "–": "-", "→": "->", "’": "'", "‘": "'",
              "“": '"', "”": '"', "≈": "~", "…": "...", "★": "*"}

    def _esc(self, s):
        for k, v in self._ASCII.items():
            s = s.replace(k, v)
        return (s.replace("\\", r"\\").replace("(", r"\(").replace(")", r"\)")
                 .encode("latin-1", "replace").decode("latin-1"))

    def text(self, x, y, s, size=10, bold=False, gray=0.0):
        font = "/F2" if bold else "/F1"
        self.ops.append(
            f"BT {gray:.2f} {gray:.2f} {gray:.2f} rg {font} {size} Tf "
            f"{x:.1f} {y:.1f} Td ({self._esc(str(s))}) Tj ET"
        )

    def line(self, x1, y1, x2, y2, width=0.75, gray=0.8):
        self.ops.append(
            f"{gray:.2f} {gray:.2f} {gray:.2f} RG {width} w "
            f"{x1:.1f} {y1:.1f} m {x2:.1f} {y2:.1f} l S"
        )

    def render(self):
        stream = "\n".join(self.ops).encode("latin-1", "replace")
        objects = [
            b"<< /Type /Catalog /Pages 2 0 R >>",
            b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
            (f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {PAGE_W} {PAGE_H}] "
             f"/Resources << /Font << /F1 4 0 R /F2 5 0 R >> >> /Contents 6 0 R >>").encode(),
            b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
            b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>",
            b"<< /Length " + str(len(stream)).encode() + b" >>\nstream\n" + stream + b"\nendstream",
        ]
        out = bytearray(b"%PDF-1.4\n")
        offsets = []
        for i, body in enumerate(objects, start=1):
            offsets.append(len(out))
            out += f"{i} 0 obj\n".encode() + body + b"\nendobj\n"
        xref_at = len(out)
        out += f"xref\n0 {len(objects) + 1}\n0000000000 65535 f \n".encode()
        for off in offsets:
            out += f"{off:010d} 00000 n \n".encode()
        out += (f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
                f"startxref\n{xref_at}\n%%EOF\n").encode()
        return bytes(out)


def money(v):
    return f"${v:,.0f}" if v is not None else "—"


def build_report(debts, settings, plan_summary, snapshots_latest):
    """plan_summary: a `_summary` dict for the plan scenario (from engine.compare).
    snapshots_latest: {debt_id: (snap_date, balance)} from the most recent snapshot."""
    pdf = MiniPDF()
    y = PAGE_H - MARGIN

    pdf.text(MARGIN, y, "Debt Payoff — Monthly Status", 20, bold=True); y -= 16
    pdf.text(MARGIN, y, f"Generated {date.today().isoformat()}", 9, gray=0.4); y -= 24

    total = sum(d["balance"] for d in debts)
    pdf.text(MARGIN, y - 14, money(total), 30, bold=True)
    pdf.text(MARGIN + 170, y - 14, "total debt today", 10, gray=0.4)
    y -= 44
    pdf.line(MARGIN, y, PAGE_W - MARGIN, y); y -= 18

    # Debt table
    pdf.text(MARGIN, y, "DEBTS", 9, bold=True, gray=0.4); y -= 14
    cols = [MARGIN, MARGIN + 170, MARGIN + 250, MARGIN + 330, MARGIN + 430]
    for cx, head in zip(cols, ["Name", "Balance", "APR", "Promo ends", "Projected payoff"]):
        pdf.text(cx, y, head, 8, gray=0.45)
    y -= 4; pdf.line(MARGIN, y, PAGE_W - MARGIN, y, gray=0.85); y -= 12
    for d in debts:
        res = plan_summary["debts"].get(str(d["id"]), {})
        rate = f"0% → {d['apr']:g}%" if d["promo_end"] else f"{d['apr']:g}%"
        vals = [d["name"], money(d["balance"]), rate, d["promo_end"] or "—",
                res.get("payoff_month") or "not within horizon"]
        for cx, v in zip(cols, vals):
            pdf.text(cx, y, v, 10)
        y -= 15
    y -= 8

    # Goals
    pdf.text(MARGIN, y, "GOALS (under current plan)", 9, bold=True, gray=0.4); y -= 14
    for g in plan_summary["goals"]:
        mark = "ON TRACK" if g["on_track"] else "AT RISK"
        pdf.text(MARGIN, y, f"[{mark}]", 10, bold=True, gray=0.0 if g["on_track"] else 0.0)
        pdf.text(MARGIN + 70, y,
                 f"{g['goal']} by {g['due']} — projected {g['projected'] or 'beyond horizon'}", 10)
        y -= 15
    y -= 8

    # Alerts
    alerts = plan_summary["promo_alerts"]
    violations = plan_summary["buffer_violations"]
    pdf.text(MARGIN, y, "ALERTS", 9, bold=True, gray=0.4); y -= 14
    if not alerts and not violations:
        pdf.text(MARGIN, y, "None — promos covered and cash stays above the floor.", 10, gray=0.3)
        y -= 15
    for a in alerts:
        pdf.text(MARGIN, y, f"[{a['level'].upper()}] {a['message']}"[:110], 9); y -= 13
    if violations:
        first = violations[0]
        pdf.text(MARGIN, y,
                 f"[BUFFER] Cash dips below {money(first['floor'])} in {len(violations)} month(s), "
                 f"first {first['month']} at {money(first['cash'])}.", 9)
        y -= 13
    y -= 8

    # Plan vs actual (latest snapshot)
    pdf.text(MARGIN, y, "PLAN VS ACTUAL", 9, bold=True, gray=0.4); y -= 14
    if snapshots_latest:
        snap_date = next(iter(snapshots_latest.values()))[0]
        actual = sum(v[1] for v in snapshots_latest.values())
        planned = None
        mk = snap_date[:7]
        for row in plan_summary["monthly"]:
            if row["month"] <= mk:
                planned = row["total_balance"]
        if planned is not None:
            diff = actual - planned
            direction = "behind" if diff > 0 else "ahead of"
            pdf.text(MARGIN, y, f"Latest snapshot {snap_date}: {money(actual)} actual vs "
                                f"{money(planned)} planned — {money(abs(diff))} {direction} plan.", 10)
        else:
            pdf.text(MARGIN, y, f"Latest snapshot {snap_date}: {money(actual)} total.", 10)
        y -= 15
    else:
        pdf.text(MARGIN, y, "No snapshots recorded yet — add one on the Snapshots screen.", 10, gray=0.3)
        y -= 15
    y -= 8

    # Plan numbers
    pdf.text(MARGIN, y, "PLAN SUMMARY", 9, bold=True, gray=0.4); y -= 14
    lines = [
        f"Debt-free: {plan_summary['debt_free_month'] or 'beyond horizon'}",
        f"Total interest under plan: {money(plan_summary['total_interest'])}",
        f"Interest saved vs minimums only: {money(plan_summary['interest_saved'])}",
        f"Months cut vs minimums only: {plan_summary['months_cut']}",
        f"Lowest projected cash: {money(plan_summary['min_cash'])} "
        f"(floor {money(float(settings.get('emergency_floor', 0) or 0))})",
    ]
    for ln in lines:
        pdf.text(MARGIN, y, ln, 10); y -= 15

    pdf.line(MARGIN, MARGIN - 6, PAGE_W - MARGIN, MARGIN - 6)
    pdf.text(MARGIN, MARGIN - 20, "Generated locally by Debt Payoff Command Center", 8, gray=0.5)
    return pdf.render()
