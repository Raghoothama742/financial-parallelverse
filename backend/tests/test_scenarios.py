import pytest
from backend.app.services.scenario_engine import ScenarioEngine

def test_baseline_scenario_flow():
    res = ScenarioEngine.simulate_all_scenarios(
        duration_months=6,
        monthly_income=70000.0,
        current_savings=100000.0,
        essential_expenses=30000.0,
        discretionary_expenses=10000.0,
        existing_debt_emi=5000.0,
        emergency_fund_target=80000.0,
        purchase_mode="NONE"
    )
    baseline = res["scenarios"]["baseline"]
    assert len(baseline["timeline"]) == 6
    # Monthly free cash flow = 70000 - 45000 = +25000
    # After 6 months: 100000 + 6*25000 = 250000
    assert baseline["timeline"][0]["net_cash_flow"] == 25000.0
    assert baseline["timeline"][-1]["closing_savings"] == 250000.0
    assert baseline["negative_cash_months"] == 0
    assert baseline["resilience_score"] == 100

def test_unexpected_expense_in_month_3():
    res = ScenarioEngine.simulate_all_scenarios(
        duration_months=6,
        monthly_income=60000.0,
        current_savings=50000.0,
        essential_expenses=30000.0,
        discretionary_expenses=15000.0,
        existing_debt_emi=5000.0,
        emergency_fund_target=60000.0,
        purchase_mode="NONE",
        unexpected_expense_amount=35000.0,
        unexpected_expense_month=3
    )
    unexp = res["scenarios"]["unexpected_expense"]
    m3 = unexp["timeline"][2] # Month 3 (index 2)
    assert m3["unexpected_expense"] == 35000.0
    # Free cash flow in month 3 is 60k - (50k + 35k) = -25000
    assert m3["net_cash_flow"] == -25000.0
    # Other months have unexpected_expense == 0
    assert unexp["timeline"][0]["unexpected_expense"] == 0.0
    assert unexp["timeline"][1]["unexpected_expense"] == 0.0
    assert unexp["timeline"][3]["unexpected_expense"] == 0.0

def test_delayed_salary_timing():
    res = ScenarioEngine.simulate_all_scenarios(
        duration_months=6,
        monthly_income=50000.0,
        current_savings=80000.0,
        essential_expenses=25000.0,
        discretionary_expenses=10000.0,
        existing_debt_emi=5000.0,
        emergency_fund_target=60000.0,
        purchase_mode="NONE",
        salary_delay_months=1,
        salary_delay_start_month=2
    )
    delayed = res["scenarios"]["delayed_salary"]
    # In month 2, salary is delayed -> income received is 0
    m2 = delayed["timeline"][1]
    assert m2["income_received"] == 0.0
    # In month 3, salary catches up -> double salary (50,000 + 50,000 = 100,000)
    m3 = delayed["timeline"][2]
    assert m3["income_received"] == 100000.0

def test_negative_cash_balance_and_breaking_point():
    res = ScenarioEngine.simulate_all_scenarios(
        duration_months=6,
        monthly_income=30000.0,
        current_savings=10000.0,
        essential_expenses=35000.0,
        discretionary_expenses=10000.0,
        existing_debt_emi=5000.0,
        emergency_fund_target=50000.0,
        purchase_mode="CASH",
        purchase_amount=25000.0,
        purchase_month=1
    )
    baseline = res["scenarios"]["baseline"]
    assert baseline["breaking_point_detected"] is True
    assert baseline["negative_cash_months"] > 0
    assert baseline["lowest_savings"] < 0
