import pytest
from backend.app.services.affordability import AffordabilityPlanner

def test_purchase_evaluation_healthy_finances():
    res = AffordabilityPlanner.evaluate_purchase(
        monthly_income=100000.0,
        current_savings=250000.0,
        essential_expenses=35000.0,
        discretionary_expenses=15000.0,
        existing_debt_emi=5000.0,
        emergency_fund_target=120000.0,
        purchase_name="MacBook Pro",
        purchase_amount=70000.0
    )
    assert len(res["options"]) == 4
    # With 250,000 savings and 120,000 emergency fund, 250k - 70k = 180k remaining >= 120k emergency fund
    cash_opt = next(o for o in res["options"] if o["option_id"] == "buy_cash_now")
    assert cash_opt["safe_to_proceed"] is True
    assert cash_opt["risk_rating"] == "SAFE"
    assert res["recommended_option_id"] == "buy_cash_now"

def test_purchase_evaluation_stretched_finances():
    res = AffordabilityPlanner.evaluate_purchase(
        monthly_income=50000.0,
        current_savings=75000.0,
        essential_expenses=30000.0,
        discretionary_expenses=12000.0,
        existing_debt_emi=5000.0,
        emergency_fund_target=100000.0,
        purchase_name="Gaming Laptop",
        purchase_amount=70000.0,
        cheaper_alternative_amount=35000.0
    )
    cash_opt = next(o for o in res["options"] if o["option_id"] == "buy_cash_now")
    # 75k - 70k = 5k left, far below 100k emergency target!
    assert cash_opt["safe_to_proceed"] is False
    assert cash_opt["risk_rating"] == "CAUTION"
    # Should recommend save_and_wait or cheaper_alternative
    assert res["recommended_option_id"] in ("save_and_wait", "cheaper_alternative")
