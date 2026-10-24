from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import FinancialProfile, ScenarioSimulation
from ..schemas import ScenarioSimulationRequest, ScenarioSimulationResponse
from ..services.scenario_engine import ScenarioEngine

router = APIRouter(prefix="/scenarios", tags=["Scenario Engine"])

@router.post("/simulate", response_model=ScenarioSimulationResponse)
def simulate_scenarios(req: ScenarioSimulationRequest, db: Session = Depends(get_db)):
    # Fallback to saved profile if values are not provided
    profile = db.query(FinancialProfile).first()
    
    inc = req.monthly_income if req.monthly_income is not None else (profile.monthly_income if profile else 75000.0)
    sav = req.current_savings if req.current_savings is not None else (profile.current_savings if profile else 120000.0)
    ess = req.essential_expenses if req.essential_expenses is not None else (profile.essential_expenses if profile else 32000.0)
    disc = req.discretionary_expenses if req.discretionary_expenses is not None else (profile.discretionary_expenses if profile else 15000.0)
    debt = req.existing_debt_emi if req.existing_debt_emi is not None else (profile.existing_debt_emi if profile else 8000.0)
    emerg = req.emergency_fund_target if req.emergency_fund_target is not None else (profile.emergency_fund_target if profile else 150000.0)

    result = ScenarioEngine.simulate_all_scenarios(
        duration_months=req.duration_months,
        monthly_income=inc,
        current_savings=sav,
        essential_expenses=ess,
        discretionary_expenses=disc,
        existing_debt_emi=debt,
        emergency_fund_target=emerg,
        purchase_name=req.purchase_name,
        purchase_amount=req.purchase_amount,
        purchase_month=req.purchase_month,
        purchase_mode=req.purchase_mode,
        emi_down_payment=req.emi_down_payment,
        emi_interest_rate=req.emi_interest_rate,
        emi_tenure_months=req.emi_tenure_months,
        unexpected_expense_amount=req.unexpected_expense_amount,
        unexpected_expense_month=req.unexpected_expense_month,
        salary_delay_months=req.salary_delay_months,
        salary_delay_start_month=req.salary_delay_start_month,
        expense_increase_pct=req.expense_increase_pct,
        income_reduction_pct=req.income_reduction_pct,
        recurring_emergency_cost=req.recurring_emergency_cost,
        recurring_cost_start_month=req.recurring_cost_start_month,
        monthly_inflation_pct=req.monthly_inflation_pct,
        investment_return_pct=req.investment_return_pct
    )

    # Optionally persist simulation record
    sim_record = ScenarioSimulation(
        simulation_name=f"Simulation {req.purchase_name} ({req.purchase_mode})",
        purchase_name=req.purchase_name,
        purchase_amount=req.purchase_amount,
        purchase_mode=req.purchase_mode,
        duration_months=req.duration_months,
        unexpected_expense_amount=req.unexpected_expense_amount,
        unexpected_expense_month=req.unexpected_expense_month,
        salary_delay_months=req.salary_delay_months,
        salary_delay_start_month=req.salary_delay_start_month,
        expense_increase_pct=req.expense_increase_pct,
        results_summary=result["comparison_summary"]
    )
    db.add(sim_record)
    db.commit()

    return result

@router.get("")
def list_simulations(db: Session = Depends(get_db)):
    records = db.query(ScenarioSimulation).order_by(ScenarioSimulation.created_at.desc()).limit(20).all()
    return [
        {
            "id": r.id,
            "simulation_name": r.simulation_name,
            "purchase_name": r.purchase_name,
            "purchase_amount": r.purchase_amount,
            "purchase_mode": r.purchase_mode,
            "duration_months": r.duration_months,
            "results_summary": r.results_summary,
            "created_at": r.created_at
        }
        for r in records
    ]
