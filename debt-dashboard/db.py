"""SQLite schema, connection helpers, and first-run seed data.

All seeded numbers are editable placeholders — the Config screen is the
source of truth. Nothing in the engine reads these constants directly.
"""
import os
import sqlite3

DB_PATH = os.environ.get(
    "DEBT_DB", os.path.join(os.path.dirname(os.path.abspath(__file__)), "debt.db")
)

SCHEMA = """
CREATE TABLE IF NOT EXISTS settings (
    key   TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS debts (
    id                 INTEGER PRIMARY KEY,
    name               TEXT NOT NULL,
    kind               TEXT NOT NULL CHECK (kind IN ('card','loan')),
    balance            REAL NOT NULL,
    apr                REAL NOT NULL,            -- regular / post-promo APR, percent
    promo_apr          REAL,                     -- promo APR (usually 0), NULL = no promo
    promo_end          TEXT,                     -- YYYY-MM-DD, NULL = no promo
    min_payment        REAL,                     -- fixed monthly minimum; NULL on loans = computed annuity
    term_months        INTEGER,                  -- loans only
    origination_date   TEXT,                     -- loans only, YYYY-MM-DD
    original_principal REAL,                     -- loans only
    payoff_plan        TEXT                      -- freeform note, e.g. "Aug 2026 RSU vest"
);

CREATE TABLE IF NOT EXISTS income_events (
    id               INTEGER PRIMARY KEY,
    name             TEXT NOT NULL,
    kind             TEXT NOT NULL CHECK (kind IN ('rsu','bonus','other')),
    event_date       TEXT NOT NULL,              -- YYYY-MM-DD
    amount           REAL NOT NULL,              -- net cash received
    allocate_debt_id INTEGER REFERENCES debts(id) ON DELETE SET NULL,
    allocate_amount  REAL                        -- portion sent to the debt; rest lands in cash
);

CREATE TABLE IF NOT EXISTS scenarios (
    id                INTEGER PRIMARY KEY,
    name              TEXT NOT NULL,
    extra_monthly     REAL NOT NULL DEFAULT 0,   -- extra principal each month (loan first, then avalanche)
    use_income_events INTEGER NOT NULL DEFAULT 1,
    is_plan           INTEGER NOT NULL DEFAULT 0,-- exactly one scenario is "the plan"
    notes             TEXT
);

CREATE TABLE IF NOT EXISTS scenario_lumps (
    id          INTEGER PRIMARY KEY,
    scenario_id INTEGER NOT NULL REFERENCES scenarios(id) ON DELETE CASCADE,
    lump_date   TEXT NOT NULL,                   -- YYYY-MM-DD
    amount      REAL NOT NULL,
    debt_id     INTEGER REFERENCES debts(id) ON DELETE SET NULL  -- NULL = loan, then avalanche
);

CREATE TABLE IF NOT EXISTS snapshots (
    id        INTEGER PRIMARY KEY,
    snap_date TEXT NOT NULL,                     -- YYYY-MM-DD
    debt_id   INTEGER NOT NULL REFERENCES debts(id) ON DELETE CASCADE,
    balance   REAL NOT NULL,
    UNIQUE (snap_date, debt_id)
);

CREATE TABLE IF NOT EXISTS cash_snapshots (
    id        INTEGER PRIMARY KEY,
    snap_date TEXT NOT NULL UNIQUE,
    cash      REAL NOT NULL
);
"""

DEFAULT_SETTINGS = {
    "cash_on_hand": "20000",          # editable placeholder
    "emergency_floor": "15000",       # baby buffer floor
    "monthly_surplus": "3000",        # cash left after all regular bills & minimums
    "monthly_surplus_after_baby": "1500",
    "baby_date": "2026-11-01",
    "cc_goal_date": "2026-09-16",     # credit cards to $0
    "loan_goal_date": "2029-09-30",   # home equity loan to $0
}


def connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init(conn=None):
    own = conn is None
    if own:
        conn = connect()
    conn.executescript(SCHEMA)
    for k, v in DEFAULT_SETTINGS.items():
        conn.execute("INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)", (k, v))
    if conn.execute("SELECT COUNT(*) FROM debts").fetchone()[0] == 0:
        seed(conn)
    conn.commit()
    if own:
        conn.close()


def seed(conn):
    """First-run data matching the household's stated situation.

    APRs on the cards' post-promo rates and income-event amounts are guesses —
    edit them on the Config screen.
    """
    debts = [
        # name, kind, balance, apr, promo_apr, promo_end, min_pay, term, orig, principal, plan
        ("Card 1 (BoA)", "card", 11300, 24.99, 0.0, "2026-10-01", 115, None, None, None,
         "Pay off with August 2026 RSU vest"),
        ("Card 2", "card", 10000, 24.99, 0.0, "2027-07-01", 100, None, None, None,
         "Pay off with September 2026 bonus"),
        ("Home equity loan", "loan", 110000, 7.44, None, None, None, 240, "2026-05-01", 110000,
         "Extra principal + lump sums; goal Sept 2029"),
    ]
    conn.executemany(
        """INSERT INTO debts (name, kind, balance, apr, promo_apr, promo_end, min_payment,
                              term_months, origination_date, original_principal, payoff_plan)
           VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
        debts,
    )
    card1 = conn.execute("SELECT id FROM debts WHERE name LIKE 'Card 1%'").fetchone()[0]
    card2 = conn.execute("SELECT id FROM debts WHERE name LIKE 'Card 2%'").fetchone()[0]
    events = [
        ("August RSU vest", "rsu", "2026-08-15", 12000, card1, 11300),
        ("September bonus", "bonus", "2026-09-15", 11000, card2, 10000),
    ]
    conn.executemany(
        """INSERT INTO income_events (name, kind, event_date, amount, allocate_debt_id, allocate_amount)
           VALUES (?,?,?,?,?,?)""",
        events,
    )
    scenarios = [
        ("Plan: lump sums at vest/bonus", 0, 1, 1,
         "Cards cleared by RSU vest and bonus; loan on minimums."),
        ("Plan + $500/mo extra to loan", 500, 1, 0, None),
        ("Plan + $1,000/mo extra to loan", 1000, 1, 0, None),
    ]
    conn.executemany(
        "INSERT INTO scenarios (name, extra_monthly, use_income_events, is_plan, notes) VALUES (?,?,?,?,?)",
        scenarios,
    )


if __name__ == "__main__":
    init()
    print(f"initialized {DB_PATH}")
