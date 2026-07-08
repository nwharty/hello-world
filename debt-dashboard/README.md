# Debt Payoff Command Center

A local, single-household web app for planning and tracking debt payoff.
**Zero dependencies** — Python 3 standard library + SQLite + vanilla JS. All
data stays in a local `debt.db` file; nothing leaves your machine.

## Run

```bash
cd debt-dashboard
python3 app.py
# → http://127.0.0.1:8642
```

First run creates and seeds `debt.db` with the household's starting numbers
(two 0% promo cards, the home equity loan, the August RSU vest and September
bonus). **Every seeded number is editable on the Config screen** — post-promo
APRs and income amounts are placeholders, so set them first.

Run the engine tests with `python3 test_engine.py`.

## Screens

- **Dashboard** — total debt hero, goal tiles (cards at $0 by the goal date,
  loan payoff, interest saved, lowest projected cash), promo-expiration and
  baby-buffer alerts, and the actual-vs-plan trajectory chart.
- **Scenarios** — build scenarios (extra monthly principal, lump sums at
  vest/bonus dates, ad-hoc lumps) and compare up to three side by side against
  the always-included "minimum payments only" baseline: payoff date, total
  interest, interest saved, months cut, goal checkmarks, buffer flags. Mark
  one scenario ★ as *the plan*; it drives the dashboard and the PDF.
- **Snapshots** — enter real balances (and cash) each month; history is logged
  and charted against the plan. Re-saving a date overwrites that snapshot.
- **Config** — household settings (cash, emergency floor, monthly surplus
  before/after the baby, goal dates), debts, and income events (RSU vests,
  bonuses). Nothing is hardcoded.
- **Export PDF** — the header button downloads a one-page monthly status
  report (`/api/report`).

## Model assumptions

- Monthly compounding at APR/12; interest accrues, then payments apply.
- Card minimums are issuer-style — interest + 1% of balance, floored at the
  configured dollar minimum — so the baseline actually amortizes. Loans use
  the fixed annuity payment (or a fixed override).
- A 0% promo rate applies through the month before `promo_end`; the regular
  APR starts that month.
- **Monthly surplus is cash left after all regular bills *and minimum
  payments***. Only extra principal and ad-hoc lumps draw the cash buffer
  down; income events add `amount − allocated` to cash.
- Extra monthly principal goes to the loan first; freed-up payments roll to
  the highest-APR remaining debt (avalanche).
- The buffer check flags any month projected cash drops below the emergency
  floor; the surplus switches to the post-baby value from the baby date.

## Data model (SQLite)

| Table | Purpose |
|---|---|
| `settings` | key/value household config (cash, floor, surpluses, dates) |
| `debts` | balances, APRs, promo windows, minimums, loan terms |
| `income_events` | dated RSU vests / bonuses with an optional debt allocation |
| `scenarios` | extra-monthly amount, income-event toggle, ★ plan flag |
| `scenario_lumps` | ad-hoc one-off lump sums per scenario |
| `snapshots` | monthly per-debt balance history (unique per date+debt) |
| `cash_snapshots` | monthly cash-on-hand history |

## API

`GET/PUT /api/settings` · `GET/POST/PUT/DELETE /api/debts[/id]`,
`/api/income_events[/id]`, `/api/scenarios[/id]` (lumps nested) ·
`GET/POST /api/snapshots` · `GET /api/projection?scenario_id=` ·
`GET /api/compare?ids=1,2` · `GET /api/dashboard` · `GET /api/report` (PDF)
