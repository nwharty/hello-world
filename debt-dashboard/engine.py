"""Projection engine: joint month-by-month simulation of all debts plus cash.

Model assumptions (documented on the Config screen too):
- Monthly compounding at APR/12; interest accrues on the running balance,
  then payments are applied.
- `monthly_surplus` is cash left over each month AFTER regular bills and all
  minimum payments, so minimums never move the cash track; only extra
  principal and ad-hoc lump sums draw cash down.
- Income events add (amount - allocate_amount) to cash; the allocated part
  goes straight to the target debt in the event's month.
- Extra monthly principal targets the loan first; once a target is paid off,
  the freed-up amount rolls to the highest-APR remaining debt (avalanche).
"""
from datetime import date

MAX_MONTHS = 600


def parse_date(s):
    return date.fromisoformat(s) if s else None


def month_start(d):
    return date(d.year, d.month, 1)


def add_months(d, n):
    m = d.month - 1 + n
    return date(d.year + m // 12, m % 12 + 1, 1)


def month_key(d):
    return f"{d.year:04d}-{d.month:02d}"


def annuity_payment(principal, apr, term_months):
    r = apr / 100.0 / 12.0
    if r == 0:
        return principal / term_months
    return principal * r / (1 - (1 + r) ** -term_months)


def scheduled_payment(debt, balance, rate):
    """Contractual monthly payment for a debt in the current month.

    Loans: fixed annuity payment. Cards: issuer-style minimum — interest plus
    1% of the balance, floored at the configured dollar minimum — so the
    minimum-payments baseline actually amortizes instead of growing forever."""
    if debt["kind"] == "loan":
        if debt["min_payment"] is not None:
            return debt["min_payment"]
        if debt["term_months"]:
            principal = debt["original_principal"] or debt["balance"]
            return annuity_payment(principal, debt["apr"], debt["term_months"])
    floor = debt["min_payment"] if debt["min_payment"] is not None else 25.0
    return max(floor, balance * (0.01 + rate))


def monthly_rate(debt, month):
    """Rate in effect for a given month, honoring a promo window."""
    promo_end = parse_date(debt["promo_end"])
    if promo_end and debt["promo_apr"] is not None and month < month_start(promo_end):
        return debt["promo_apr"] / 100.0 / 12.0
    return debt["apr"] / 100.0 / 12.0


def simulate(debts, settings, scenario, income_events, start=None):
    """Run one scenario. Returns per-debt payoff results, a monthly series
    for charting, buffer violations, and totals."""
    start = month_start(start or date.today())
    floor = float(settings.get("emergency_floor", 0) or 0)
    surplus = float(settings.get("monthly_surplus", 0) or 0)
    surplus_after = float(settings.get("monthly_surplus_after_baby", surplus) or surplus)
    baby_month = parse_date(settings.get("baby_date"))
    baby_month = month_start(baby_month) if baby_month else None

    balances = {d["id"]: float(d["balance"]) for d in debts}
    interest_paid = {d["id"]: 0.0 for d in debts}
    payoff_month = {d["id"]: None for d in debts}
    by_id = {d["id"]: d for d in debts}
    cash = float(settings.get("cash_on_hand", 0) or 0)

    events_by_month = {}
    if scenario.get("use_income_events"):
        for ev in income_events:
            m = month_key(month_start(parse_date(ev["event_date"])))
            events_by_month.setdefault(m, []).append(ev)
    lumps_by_month = {}
    for lump in scenario.get("lumps", []):
        m = month_key(month_start(parse_date(lump["lump_date"])))
        lumps_by_month.setdefault(m, []).append(lump)

    extra_monthly = float(scenario.get("extra_monthly", 0) or 0)
    monthly = []
    violations = []
    loan_ids = [d["id"] for d in debts if d["kind"] == "loan"]

    def pay_towards(debt_id, amount):
        """Apply up to `amount` and return what was actually applied."""
        if debt_id is None or balances.get(debt_id, 0) <= 0:
            return 0.0
        applied = min(amount, balances[debt_id])
        balances[debt_id] -= applied
        return applied

    def avalanche_targets(preferred=None):
        """Preferred target first, then unpaid debts by APR descending."""
        order = sorted(
            (i for i in balances if balances[i] > 0.005),
            key=lambda i: -by_id[i]["apr"],
        )
        if preferred is not None and preferred in order:
            order.remove(preferred)
            order.insert(0, preferred)
        return order

    for step in range(MAX_MONTHS):
        month = add_months(start, step)
        mk = month_key(month)
        interest_this_month = 0.0

        # 1. Accrue interest, then contractual payments.
        for d in debts:
            i = d["id"]
            if balances[i] <= 0.005:
                continue
            rate = monthly_rate(d, month)
            pre_interest_balance = balances[i]
            interest = pre_interest_balance * rate
            balances[i] += interest
            interest_paid[i] += interest
            interest_this_month += interest
            pay_towards(i, scheduled_payment(d, pre_interest_balance, rate))

        # 2. Extra monthly principal (from cash): loan first, then avalanche.
        extra_paid = 0.0
        remaining = extra_monthly
        for target in avalanche_targets(preferred=loan_ids[0] if loan_ids else None):
            if remaining <= 0:
                break
            applied = pay_towards(target, remaining)
            remaining -= applied
            extra_paid += applied

        # 3. Income events this month: allocation to debt, remainder to cash.
        for ev in events_by_month.get(mk, []):
            alloc = min(float(ev["allocate_amount"] or 0), float(ev["amount"]))
            applied = pay_towards(ev["allocate_debt_id"], alloc)
            cash += float(ev["amount"]) - applied

        # 4. Scenario-specific ad-hoc lump sums (paid from cash).
        lump_paid = 0.0
        for lump in lumps_by_month.get(mk, []):
            remaining = float(lump["amount"])
            for target in avalanche_targets(preferred=lump["debt_id"] or (loan_ids[0] if loan_ids else None)):
                if remaining <= 0:
                    break
                applied = pay_towards(target, remaining)
                remaining -= applied
                lump_paid += applied

        # 5. Cash track and buffer check.
        cash += (surplus_after if baby_month and month >= baby_month else surplus)
        cash -= extra_paid + lump_paid
        if cash < floor:
            violations.append({"month": mk, "cash": round(cash, 2), "floor": floor})

        for i in balances:
            if balances[i] <= 0.005 and payoff_month[i] is None:
                balances[i] = 0.0
                payoff_month[i] = mk

        monthly.append({
            "month": mk,
            "total_balance": round(sum(balances.values()), 2),
            "balances": {str(i): round(b, 2) for i, b in balances.items()},
            "cash": round(cash, 2),
            "interest": round(interest_this_month, 2),
        })
        if all(b <= 0.005 for b in balances.values()):
            break

    debt_results = {}
    for d in debts:
        i = d["id"]
        debt_results[str(i)] = {
            "name": d["name"],
            "payoff_month": payoff_month[i],   # None = not paid within MAX_MONTHS
            "total_interest": round(interest_paid[i], 2),
        }
    return {
        "scenario": {k: scenario.get(k) for k in ("id", "name", "extra_monthly", "use_income_events")},
        "start_month": month_key(start),
        "debts": debt_results,
        "monthly": monthly,
        "buffer_violations": violations,
        "totals": {
            "total_interest": round(sum(interest_paid.values()), 2),
            "months": len(monthly),
            "debt_free_month": monthly[-1]["month"] if monthly and monthly[-1]["total_balance"] <= 0.005 else None,
        },
    }


def baseline_scenario():
    return {"id": None, "name": "Minimum payments only", "extra_monthly": 0,
            "use_income_events": 0, "lumps": []}


def promo_alerts(debts, sim):
    """Flag 0% balances that won't reach $0 before the promo expires, under
    the given (plan) simulation. Warn when payoff lands in the promo month."""
    alerts = []
    by_month = {row["month"]: row for row in sim["monthly"]}
    for d in debts:
        if not d["promo_end"] or d["promo_apr"] is None:
            continue
        promo_month = month_key(month_start(parse_date(d["promo_end"])))
        payoff = sim["debts"][str(d["id"])]["payoff_month"]
        # Balance at the end of the month BEFORE the promo lapses.
        last_promo_row = None
        for row in sim["monthly"]:
            if row["month"] < promo_month:
                last_promo_row = row
        residual = (last_promo_row or {"balances": {}})["balances"].get(str(d["id"]))
        if residual is None:  # promo ends before/at sim start: use current balance
            residual = float(d["balance"])
        if payoff is None or payoff >= promo_month:
            monthly_interest = residual * d["apr"] / 100.0 / 12.0
            alerts.append({
                "level": "critical",
                "debt_id": d["id"], "debt": d["name"],
                "promo_end": d["promo_end"],
                "projected_residual": round(residual, 2),
                "post_promo_monthly_interest": round(monthly_interest, 2),
                "message": (f"{d['name']}: projected ${residual:,.0f} still owed when the "
                            f"0% promo ends {d['promo_end']} — interest would start at "
                            f"~${monthly_interest:,.0f}/mo at {d['apr']}% APR."),
            })
        elif add_months(month_start(parse_date(payoff + "-01")), 1) >= month_start(parse_date(d["promo_end"])):
            alerts.append({
                "level": "warning",
                "debt_id": d["id"], "debt": d["name"],
                "promo_end": d["promo_end"],
                "message": (f"{d['name']}: payoff lands {payoff}, the last month before the "
                            f"promo deadline {d['promo_end']} — no slack if the plan slips."),
            })
    return alerts


def goal_status(debts, settings, sim):
    """Credit-cards-to-zero and loan-payoff goals vs. the plan simulation."""
    out = []
    cc_goal = settings.get("cc_goal_date")
    if cc_goal:
        card_payoffs = [sim["debts"][str(d["id"])]["payoff_month"]
                        for d in debts if d["kind"] == "card"]
        goal_m = month_key(month_start(parse_date(cc_goal)))
        met = card_payoffs and all(p is not None and p <= goal_m for p in card_payoffs)
        latest = max((p for p in card_payoffs if p), default=None)
        out.append({"goal": "Credit cards at $0", "due": cc_goal,
                    "projected": latest, "on_track": bool(met)})
    loan_goal = settings.get("loan_goal_date")
    if loan_goal:
        loan_payoffs = [sim["debts"][str(d["id"])]["payoff_month"]
                        for d in debts if d["kind"] == "loan"]
        goal_m = month_key(month_start(parse_date(loan_goal)))
        met = loan_payoffs and all(p is not None and p <= goal_m for p in loan_payoffs)
        latest = max((p for p in loan_payoffs if p), default=None)
        out.append({"goal": "Home equity loan paid off", "due": loan_goal,
                    "projected": latest, "on_track": bool(met)})
    return out


def compare(debts, settings, scenarios, income_events, start=None):
    """Side-by-side summaries; baseline (minimums only) is always included."""
    base = simulate(debts, settings, baseline_scenario(), income_events, start)
    base_interest = base["totals"]["total_interest"]
    base_months = base["totals"]["months"]
    rows = [_summary(base, base_interest, base_months, debts, settings)]
    for sc in scenarios:
        sim = simulate(debts, settings, sc, income_events, start)
        rows.append(_summary(sim, base_interest, base_months, debts, settings))
    return {"baseline": rows[0], "scenarios": rows[1:]}


def _summary(sim, base_interest, base_months, debts, settings):
    return {
        "scenario": sim["scenario"],
        "debts": sim["debts"],
        "total_interest": sim["totals"]["total_interest"],
        "interest_saved": round(base_interest - sim["totals"]["total_interest"], 2),
        "months": sim["totals"]["months"],
        "months_cut": base_months - sim["totals"]["months"],
        "debt_free_month": sim["totals"]["debt_free_month"],
        "buffer_violations": sim["buffer_violations"],
        "min_cash": min((m["cash"] for m in sim["monthly"]), default=None),
        "promo_alerts": promo_alerts(debts, sim),
        "goals": goal_status(debts, settings, sim),
        "monthly": [{"month": m["month"], "total_balance": m["total_balance"], "cash": m["cash"]}
                    for m in sim["monthly"]],
    }
