import pytest
from backend.app.services.financial_engine import FinancialEngine

def test_income_greater_than_expenses():
    metrics = FinancialEngine.calculate_profile_metrics(
        monthly_income=80000.0,
        current_savings=150000.0,
        essential_expenses=30000.0,
        discretionary_expenses=15000.0,
        existing_debt_emi=5000.0,
        emergency_fund_target=100000.0
    )
    assert metrics["free_cash_flow"] == 30000.0
    assert metrics["is_cash_flow_positive"] is True
    assert metrics["savings_rate_pct"] == 37.5
    assert metrics["debt_to_income_pct"] == 6.25
    assert metrics["emergency_coverage_pct"] == 150.0

def test_expenses_greater_than_income():
    metrics = FinancialEngine.calculate_profile_metrics(
        monthly_income=40000.0,
        current_savings=50000.0,
        essential_expenses=30000.0,
        discretionary_expenses=15000.0,
        existing_debt_emi=5000.0,
        emergency_fund_target=100000.0
    )
    assert metrics["free_cash_flow"] == -10000.0
    assert metrics["is_cash_flow_positive"] is False
    assert metrics["savings_rate_pct"] == -25.0

def test_zero_income():
    metrics = FinancialEngine.calculate_profile_metrics(
        monthly_income=0.0,
        current_savings=60000.0,
        essential_expenses=20000.0,
        discretionary_expenses=10000.0,
        existing_debt_emi=0.0,
        emergency_fund_target=100000.0
    )
    assert metrics["free_cash_flow"] == -30000.0
    assert metrics["savings_rate_pct"] == 0.0
    assert metrics["months_of_runway"] == 3.0

def test_zero_savings():
    metrics = FinancialEngine.calculate_profile_metrics(
        monthly_income=60000.0,
        current_savings=0.0,
        essential_expenses=30000.0,
        discretionary_expenses=15000.0,
        existing_debt_emi=5000.0,
        emergency_fund_target=120000.0
    )
    assert metrics["months_of_runway"] == 0.0
    assert metrics["emergency_coverage_pct"] == 0.0
