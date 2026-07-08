"""Local web server: JSON API + static frontend. Stdlib only.

Run:  python3 app.py  →  http://127.0.0.1:8642
"""
import json
import os
import re
from datetime import date
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

import db
import engine
import pdf_report

STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
PORT = int(os.environ.get("DEBT_PORT", "8642"))
# Default: this machine only. Set DEBT_HOST=0.0.0.0 to reach the app from
# other devices on your home network (e.g. a phone browser).
HOST = os.environ.get("DEBT_HOST", "127.0.0.1")

DEBT_FIELDS = ["name", "kind", "balance", "apr", "promo_apr", "promo_end", "min_payment",
               "term_months", "origination_date", "original_principal", "payoff_plan"]
EVENT_FIELDS = ["name", "kind", "event_date", "amount", "allocate_debt_id", "allocate_amount"]
SCENARIO_FIELDS = ["name", "extra_monthly", "use_income_events", "is_plan", "notes"]

SENT = object()  # sentinel: route already wrote the response itself


def rows(cur):
    return [dict(r) for r in cur.fetchall()]


def load_all(conn):
    debts = rows(conn.execute("SELECT * FROM debts ORDER BY id"))
    settings = {r["key"]: r["value"] for r in conn.execute("SELECT * FROM settings")}
    events = rows(conn.execute("SELECT * FROM income_events ORDER BY event_date"))
    return debts, settings, events


def load_scenario(conn, sid):
    sc = conn.execute("SELECT * FROM scenarios WHERE id=?", (sid,)).fetchone()
    if not sc:
        return None
    sc = dict(sc)
    sc["lumps"] = rows(conn.execute(
        "SELECT * FROM scenario_lumps WHERE scenario_id=? ORDER BY lump_date", (sid,)))
    return sc


def plan_scenario(conn):
    row = conn.execute("SELECT id FROM scenarios WHERE is_plan=1 ORDER BY id LIMIT 1").fetchone()
    if row:
        return load_scenario(conn, row["id"])
    return dict(engine.baseline_scenario(), name="No plan set (minimums only)")


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):  # quieter console
        pass

    # ---------- plumbing ----------
    def send_json(self, obj, status=200):
        body = json.dumps(obj).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_bytes(self, body, ctype, status=200, download=None):
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        if download:
            self.send_header("Content-Disposition", f'attachment; filename="{download}"')
        self.end_headers()
        self.wfile.write(body)

    def read_body(self):
        length = int(self.headers.get("Content-Length") or 0)
        return json.loads(self.rfile.read(length) or b"{}")

    def handle_api(self, method):
        url = urlparse(self.path)
        path, query = url.path, parse_qs(url.query)
        conn = db.connect()
        try:
            result = self.route(conn, method, path, query)
            if result is SENT:
                conn.commit()
            elif result is None:
                self.send_json({"error": "not found"}, 404)
            else:
                conn.commit()
                self.send_json(result)
        except (ValueError, KeyError, json.JSONDecodeError) as e:
            self.send_json({"error": str(e)}, 400)
        finally:
            conn.close()

    def do_GET(self):
        if urlparse(self.path).path.startswith("/api/"):
            return self.handle_api("GET")
        return self.serve_static()

    def do_POST(self):
        return self.handle_api("POST")

    def do_PUT(self):
        return self.handle_api("PUT")

    def do_DELETE(self):
        return self.handle_api("DELETE")

    def serve_static(self):
        path = urlparse(self.path).path
        if path == "/":
            path = "/index.html"
        fpath = os.path.normpath(os.path.join(STATIC_DIR, path.lstrip("/")))
        if not fpath.startswith(STATIC_DIR) or not os.path.isfile(fpath):
            return self.send_json({"error": "not found"}, 404)
        ctype = {".html": "text/html", ".js": "text/javascript",
                 ".css": "text/css", ".svg": "image/svg+xml"}.get(
            os.path.splitext(fpath)[1], "application/octet-stream")
        with open(fpath, "rb") as f:
            self.send_bytes(f.read(), ctype)

    # ---------- routes ----------
    def route(self, conn, method, path, query):
        m = re.match(r"^/api/(\w+)(?:/(\d+))?$", path)
        if not m:
            return None
        resource, rid = m.group(1), m.group(2) and int(m.group(2))

        if resource == "settings":
            if method == "GET":
                return {r["key"]: r["value"] for r in conn.execute("SELECT * FROM settings")}
            if method == "PUT":
                for k, v in self.read_body().items():
                    conn.execute("INSERT INTO settings (key,value) VALUES (?,?) "
                                 "ON CONFLICT(key) DO UPDATE SET value=excluded.value", (k, str(v)))
                return {"ok": True}

        if resource == "debts":
            return self.crud(conn, method, rid, "debts", DEBT_FIELDS)
        if resource == "income_events":
            return self.crud(conn, method, rid, "income_events", EVENT_FIELDS)

        if resource == "scenarios":
            if method == "GET" and rid:
                return load_scenario(conn, rid)
            if method == "GET":
                return [load_scenario(conn, r["id"]) for r in
                        conn.execute("SELECT id FROM scenarios ORDER BY id")]
            body = self.read_body() if method in ("POST", "PUT") else {}
            lumps = body.pop("lumps", None)
            if body.get("is_plan"):
                conn.execute("UPDATE scenarios SET is_plan=0")
            result = self.crud(conn, method, rid, "scenarios", SCENARIO_FIELDS, body=body)
            sid = rid or (result or {}).get("id")
            if lumps is not None and sid:
                conn.execute("DELETE FROM scenario_lumps WHERE scenario_id=?", (sid,))
                for lump in lumps:
                    conn.execute(
                        "INSERT INTO scenario_lumps (scenario_id, lump_date, amount, debt_id) "
                        "VALUES (?,?,?,?)",
                        (sid, lump["lump_date"], lump["amount"], lump.get("debt_id")))
            return result

        if resource == "snapshots":
            if method == "GET":
                snaps = rows(conn.execute(
                    "SELECT s.*, d.name AS debt_name FROM snapshots s "
                    "JOIN debts d ON d.id=s.debt_id ORDER BY snap_date, debt_id"))
                cash = rows(conn.execute("SELECT * FROM cash_snapshots ORDER BY snap_date"))
                return {"debts": snaps, "cash": cash}
            if method == "POST":
                body = self.read_body()  # {snap_date, balances: {debt_id: bal}, cash}
                snap_date = body["snap_date"]
                for debt_id, bal in body.get("balances", {}).items():
                    conn.execute(
                        "INSERT INTO snapshots (snap_date, debt_id, balance) VALUES (?,?,?) "
                        "ON CONFLICT(snap_date, debt_id) DO UPDATE SET balance=excluded.balance",
                        (snap_date, int(debt_id), float(bal)))
                    conn.execute("UPDATE debts SET balance=? WHERE id=?", (float(bal), int(debt_id)))
                if body.get("cash") not in (None, ""):
                    conn.execute(
                        "INSERT INTO cash_snapshots (snap_date, cash) VALUES (?,?) "
                        "ON CONFLICT(snap_date) DO UPDATE SET cash=excluded.cash",
                        (snap_date, float(body["cash"])))
                    conn.execute("INSERT INTO settings (key,value) VALUES ('cash_on_hand',?) "
                                 "ON CONFLICT(key) DO UPDATE SET value=excluded.value",
                                 (f"{float(body['cash']):g}",))
                return {"ok": True}
            if method == "DELETE" and rid:
                conn.execute("DELETE FROM snapshots WHERE id=?", (rid,))
                return {"ok": True}

        if resource == "projection" and method == "GET":
            debts, settings, events = load_all(conn)
            sid = query.get("scenario_id", [None])[0]
            sc = load_scenario(conn, int(sid)) if sid else plan_scenario(conn)
            if not sc:
                return None
            return engine.simulate(debts, settings, sc, events)

        if resource == "compare" and method == "GET":
            debts, settings, events = load_all(conn)
            ids = [int(i) for i in query.get("ids", [""])[0].split(",") if i]
            if not ids:
                ids = [r["id"] for r in conn.execute("SELECT id FROM scenarios ORDER BY id")]
            scenarios = [s for s in (load_scenario(conn, i) for i in ids) if s]
            return engine.compare(debts, settings, scenarios, events)

        if resource == "dashboard" and method == "GET":
            return self.dashboard(conn)

        if resource == "report" and method == "GET":
            debts, settings, events = load_all(conn)
            plan = plan_scenario(conn)
            summary = engine.compare(debts, settings, [plan], events)["scenarios"][0]
            latest = {}
            for r in conn.execute(
                    "SELECT debt_id, snap_date, balance FROM snapshots "
                    "WHERE snap_date=(SELECT MAX(snap_date) FROM snapshots)"):
                latest[r["debt_id"]] = (r["snap_date"], r["balance"])
            body = pdf_report.build_report(debts, settings, summary, latest)
            fname = f"debt-status-{date.today().isoformat()}.pdf"
            self.send_bytes(body, "application/pdf", download=fname)
            return SENT

        return None

    def dashboard(self, conn):
        debts, settings, events = load_all(conn)
        plan = plan_scenario(conn)
        summary = engine.compare(debts, settings, [plan], events)["scenarios"][0]
        snaps = rows(conn.execute(
            "SELECT snap_date, SUM(balance) AS total FROM snapshots GROUP BY snap_date ORDER BY snap_date"))
        upcoming = [e for e in events if e["event_date"] >= date.today().isoformat()][:4]
        return {
            "debts": debts,
            "settings": settings,
            "plan": summary,
            "actual": snaps,
            "upcoming_events": upcoming,
            "total_debt": round(sum(d["balance"] for d in debts), 2),
        }

    # generic CRUD for flat tables
    def crud(self, conn, method, rid, table, fields, body=None):
        if method == "GET":
            if rid:
                r = conn.execute(f"SELECT * FROM {table} WHERE id=?", (rid,)).fetchone()
                return dict(r) if r else None
            return rows(conn.execute(f"SELECT * FROM {table} ORDER BY id"))
        if method == "POST":
            body = body if body is not None else self.read_body()
            cols = [f for f in fields if f in body]
            cur = conn.execute(
                f"INSERT INTO {table} ({','.join(cols)}) VALUES ({','.join('?' * len(cols))})",
                [body[c] for c in cols])
            return {"id": cur.lastrowid}
        if method == "PUT" and rid:
            body = body if body is not None else self.read_body()
            cols = [f for f in fields if f in body]
            if cols:
                conn.execute(
                    f"UPDATE {table} SET {','.join(c + '=?' for c in cols)} WHERE id=?",
                    [body[c] for c in cols] + [rid])
            return {"id": rid}
        if method == "DELETE" and rid:
            conn.execute(f"DELETE FROM {table} WHERE id=?", (rid,))
            return {"ok": True}
        return None


def main():
    db.init()
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"Debt Payoff Command Center → http://{'127.0.0.1' if HOST == '0.0.0.0' else HOST}:{PORT}"
          + (" (also reachable from other devices on your network)" if HOST == "0.0.0.0" else ""))
    server.serve_forever()


if __name__ == "__main__":
    main()
