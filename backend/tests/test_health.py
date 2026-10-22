import pytest

def test_health_check(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["version"] == "1.0.0"

def test_profile_api(client):
    # Test GET profile
    res = client.get("/api/profile")
    assert res.status_code == 200
    data = res.json()
    assert "free_cash_flow" in data
    assert "monthly_income" in data

    # Test PUT profile
    update_payload = {
        "full_name": "Test User",
        "monthly_income": 90000.0,
        "current_savings": 150000.0,
        "essential_expenses": 35000.0,
        "discretionary_expenses": 15000.0,
        "existing_debt_emi": 5000.0,
        "emergency_fund_target": 180000.0,
        "planned_purchase_name": "Test Laptop",
        "planned_purchase_amount": 65000.0,
        "planned_purchase_month": 1
    }
    res_put = client.put("/api/profile", json=update_payload)
    assert res_put.status_code == 200
    updated = res_put.json()
    assert updated["full_name"] == "Test User"
    assert updated["monthly_income"] == 90000.0
    # 90000 - (35000 + 15000 + 5000) = 35000
    assert updated["free_cash_flow"] == 35000.0

def test_emi_api(client):
    payload = {
        "purchase_price": 50000.0,
        "down_payment": 5000.0,
        "annual_interest_rate": 10.0,
        "tenure_months": 12
    }
    res = client.post("/api/emi/calculate", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["principal_financed"] == 45000.0
    assert len(data["schedule"]) == 12

def test_scenario_simulate_api(client):
    payload = {
        "duration_months": 12,
        "monthly_income": 80000.0,
        "current_savings": 100000.0,
        "essential_expenses": 30000.0,
        "discretionary_expenses": 15000.0,
        "existing_debt_emi": 5000.0,
        "emergency_fund_target": 120000.0,
        "purchase_name": "Laptop",
        "purchase_amount": 70000.0,
        "purchase_mode": "EMI"
    }
    res = client.post("/api/scenarios/simulate", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "scenarios" in data
    assert "baseline" in data["scenarios"]
    assert "combined_adverse" in data["scenarios"]
