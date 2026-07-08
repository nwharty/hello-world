"""Sanity tests for the projection engine.  Run: python3 test_engine.py"""
from datetime import date

import engine


def make_debts():
    return [
        {"id": 1, "name": "Card 1", "kind": "card", "balance": 11300.0, "apr": 24.99,
         "promo_apr": 0.0, "promo_end": "2026-10-01", "min_payment": 115.0,
         "term_months": None, "origination_date": None, "original_principal": None},
        {"id": 2, "name": "Card 2", "kind": "card", "balance": 10000.0, "apr": 24.99,
         "promo_apr": 0.0, "promo_end": "2027-07-01", "min_payment": 100.0,
         "term_months": None, "origination_date": None, "original_principal": None},
        {"id": 3, "name": "Loan", "kind": "loan", "balance": 110000.0, "apr": 7.44,
         "promo_apr": None, "promo_end": None, "min_payment": None,
         "term_months": 240, "origination_date": "2026-05-01", "original_principal": 110000.0},
    ]


SETTINGS = {"cash_on_hand": "20000", "emergency_floor": "15000",
            "monthly_surplus": "3000", "monthly_surplus_after_baby": "1500",
            "baby_date": "2026-11-01", "cc_goal_date": "2026-09-16",
            "loan_goal_date": "2029-09-30"}

EVENTS = [
    {"name": "Aug RSU", "kind": "rsu", "event_date": "2026-08-15", "amount": 12000.0,
     "allocate_debt_id": 1, "allocate_amount": 11400.0},
    {"name": "Sep bonus", "kind": "bonus", "event_date": "2026-09-15", "amount": 11000.0,
     "allocate_debt_id": 2, "allocate_amount": 10100.0},
]

START = date(2026, 7, 1)


def approx(a, b, tol):
    assert abs(a - b) <= tol, f"{a} !~ {b} (tol {tol})"


def test_annuity():
    # 110k @ 7.44% over 240 months → ~$882/mo (standard amortization formula)
    p = engine.annuity_payment(110000, 7.44, 240)
    approx(p, 882, 2)


def test_minimum_only_loan_runs_full_term():
    sim = engine.simulate(make_debts(), SETTINGS, engine.baseline_scenario(), EVENTS, start=START)
    loan = sim["debts"]["3"]
    # 240 scheduled payments remain → payoff ~June 2046 from a July 2026 start
    assert loan["payoff_month"] == "2046-06", loan
    # Total loan interest on minimums ≈ payment*240 - principal ≈ 101.7k
    approx(loan["total_interest"], 882 * 240 - 110000, 900)


def test_promo_alert_fires_without_lumps():
    sim = engine.simulate(make_debts(), SETTINGS, engine.baseline_scenario(), EVENTS, start=START)
    alerts = engine.promo_alerts(make_debts(), sim)
    crit = [a for a in alerts if a["level"] == "critical"]
    assert {a["debt"] for a in crit} == {"Card 1", "Card 2"}, alerts


def test_plan_clears_cards_before_promos():
    plan = {"id": 1, "name": "plan", "extra_monthly": 0, "use_income_events": 1, "lumps": []}
    sim = engine.simulate(make_debts(), SETTINGS, plan, EVENTS, start=START)
    assert sim["debts"]["1"]["payoff_month"] == "2026-08"
    assert sim["debts"]["2"]["payoff_month"] == "2026-09"
    assert engine.promo_alerts(make_debts(), sim) == []
    goals = engine.goal_status(make_debts(), SETTINGS, sim)
    cc = next(g for g in goals if "cards" in g["goal"].lower())
    assert cc["on_track"] is True


def test_extra_monthly_cuts_loan():
    base = engine.simulate(make_debts(), SETTINGS, engine.baseline_scenario(), EVENTS, start=START)
    plan = {"id": 2, "name": "x", "extra_monthly": 1000, "use_income_events": 1, "lumps": []}
    sim = engine.simulate(make_debts(), SETTINGS, plan, EVENTS, start=START)
    assert sim["totals"]["months"] < base["totals"]["months"] - 80
    assert sim["totals"]["total_interest"] < base["totals"]["total_interest"] - 40000


def test_buffer_violation_flagged():
    # $2,600/mo extra on $1,500 post-baby surplus must eventually breach the floor.
    plan = {"id": 3, "name": "x", "extra_monthly": 2600, "use_income_events": 1, "lumps": []}
    sim = engine.simulate(make_debts(), SETTINGS, plan, EVENTS, start=START)
    assert sim["buffer_violations"], "expected cash to dip below the floor"
    first = sim["buffer_violations"][0]
    assert first["cash"] < first["floor"]


def test_lump_sum_applies():
    plan = {"id": 4, "name": "x", "extra_monthly": 0, "use_income_events": 1,
            "lumps": [{"lump_date": "2027-03-15", "amount": 20000.0, "debt_id": 3}]}
    base = engine.simulate(make_debts(), SETTINGS,
                           {"id": 0, "name": "b", "extra_monthly": 0,
                            "use_income_events": 1, "lumps": []}, EVENTS, start=START)
    sim = engine.simulate(make_debts(), SETTINGS, plan, EVENTS, start=START)
    assert sim["debts"]["3"]["total_interest"] < base["debts"]["3"]["total_interest"] - 15000
    mar = next(m for m in sim["monthly"] if m["month"] == "2027-03")
    base_mar = next(m for m in base["monthly"] if m["month"] == "2027-03")
    approx(base_mar["balances"]["3"] - mar["balances"]["3"], 20000, 1)


def test_compare_shape():
    scenarios = [{"id": 1, "name": "plan", "extra_monthly": 500,
                  "use_income_events": 1, "is_plan": 1, "lumps": []}]
    out = engine.compare(make_debts(), SETTINGS, scenarios, EVENTS, start=START)
    assert out["baseline"]["scenario"]["name"] == "Minimum payments only"
    s = out["scenarios"][0]
    assert s["interest_saved"] > 0 and s["months_cut"] > 0
    assert s["debt_free_month"] < out["baseline"]["debt_free_month"]


if __name__ == "__main__":
    failures = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print(f"PASS {name}")
            except AssertionError as e:
                failures += 1
                print(f"FAIL {name}: {e}")
    raise SystemExit(1 if failures else 0)
