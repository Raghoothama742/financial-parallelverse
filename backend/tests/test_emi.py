import pytest
from backend.app.services.emi_calculator import EMICalculator

def test_zero_interest_loan():
    res = EMICalculator.calculate_emi(
        purchase_price=60000.0,
        down_payment=0.0,
        annual_interest_rate=0.0,
        tenure_months=6
    )
    assert res["principal_financed"] == 60000.0
    assert res["monthly_emi"] == 10000.0
    assert res["total_interest"] == 0.0
    assert res["total_repayment"] == 60000.0
    assert len(res["schedule"]) == 6
    assert res["schedule"][-1]["remaining_balance"] == 0.0

def test_positive_interest_reducing_balance():
    res = EMICalculator.calculate_emi(
        purchase_price=70000.0,
        down_payment=10000.0,
        annual_interest_rate=12.0,
        tenure_months=12
    )
    # Principal = 60,000, 12% per year = 1% per month, 12 months
    # Standard formula EMI for 60,000 at 1% for 12 months = approx 5,330.93
    assert res["principal_financed"] == 60000.0
    assert 5300.0 < res["monthly_emi"] < 5400.0
    assert res["total_interest"] > 0
    # Reconciliation test: Total repaid must match sum of principal + total interest
    assert abs(res["total_repayment"] - (res["principal_financed"] + res["total_interest"])) < 1.0
    # Final month balance must reconcile to 0
    assert res["schedule"][-1]["remaining_balance"] == 0.0

def test_one_month_tenure():
    res = EMICalculator.calculate_emi(
        purchase_price=20000.0,
        down_payment=5000.0,
        annual_interest_rate=12.0,
        tenure_months=1
    )
    assert res["principal_financed"] == 15000.0
    assert len(res["schedule"]) == 1
    # 1 month interest on 15000 at 1% = 150
    assert res["total_interest"] == 150.0
    assert res["total_repayment"] == 15150.0
    assert res["schedule"][0]["remaining_balance"] == 0.0

def test_invalid_principal_or_price():
    with pytest.raises(ValueError):
        EMICalculator.calculate_emi(purchase_price=0.0)
    with pytest.raises(ValueError):
        EMICalculator.calculate_emi(purchase_price=-1000.0)

def test_down_payment_exceeds_price():
    with pytest.raises(ValueError):
        EMICalculator.calculate_emi(purchase_price=50000.0, down_payment=50000.0)
    with pytest.raises(ValueError):
        EMICalculator.calculate_emi(purchase_price=50000.0, down_payment=60000.0)

def test_invalid_tenure():
    with pytest.raises(ValueError):
        EMICalculator.calculate_emi(purchase_price=50000.0, tenure_months=0)
