from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import FinancialProfile
from ..schemas import FinancialProfileUpdate, FinancialProfileResponse
from ..services.financial_engine import FinancialEngine

router = APIRouter(prefix="/profile", tags=["Financial Profile"])

def _ensure_profile(db: Session) -> FinancialProfile:
    profile = db.query(FinancialProfile).first()
    if not profile:
        profile = FinancialProfile(
            full_name="Alex Johnson",
            monthly_income=75000.0,
            current_savings=120000.0,
            essential_expenses=32000.0,
            discretionary_expenses=15000.0,
            existing_debt_emi=8000.0,
            emergency_fund_target=150000.0,
            planned_purchase_name="MacBook Pro / Performance Laptop",
            planned_purchase_amount=70000.0,
            planned_purchase_month=1
        )
        db.add(profile)
        db.commit()
        db.refresh(profile)
    return profile

@router.get("", response_model=FinancialProfileResponse)
def get_profile(db: Session = Depends(get_db)):
    profile = _ensure_profile(db)
    metrics = FinancialEngine.calculate_profile_metrics(
        monthly_income=profile.monthly_income,
        current_savings=profile.current_savings,
        essential_expenses=profile.essential_expenses,
        discretionary_expenses=profile.discretionary_expenses,
        existing_debt_emi=profile.existing_debt_emi,
        emergency_fund_target=profile.emergency_fund_target
    )
    
    return FinancialProfileResponse(
        id=profile.id,
        full_name=profile.full_name,
        monthly_income=profile.monthly_income,
        current_savings=profile.current_savings,
        essential_expenses=profile.essential_expenses,
        discretionary_expenses=profile.discretionary_expenses,
        existing_debt_emi=profile.existing_debt_emi,
        emergency_fund_target=profile.emergency_fund_target,
        planned_purchase_name=profile.planned_purchase_name,
        planned_purchase_amount=profile.planned_purchase_amount,
        planned_purchase_month=profile.planned_purchase_month,
        free_cash_flow=metrics["free_cash_flow"],
        savings_rate_pct=metrics["savings_rate_pct"],
        debt_to_income_pct=metrics["debt_to_income_pct"],
        months_of_runway=metrics["months_of_runway"],
        updated_at=profile.updated_at
    )

@router.put("", response_model=FinancialProfileResponse)
def update_profile(data: FinancialProfileUpdate, db: Session = Depends(get_db)):
    profile = _ensure_profile(db)
    
    profile.full_name = data.full_name
    profile.monthly_income = data.monthly_income
    profile.current_savings = data.current_savings
    profile.essential_expenses = data.essential_expenses
    profile.discretionary_expenses = data.discretionary_expenses
    profile.existing_debt_emi = data.existing_debt_emi
    profile.emergency_fund_target = data.emergency_fund_target
    profile.planned_purchase_name = data.planned_purchase_name
    profile.planned_purchase_amount = data.planned_purchase_amount
    profile.planned_purchase_month = data.planned_purchase_month
    
    db.commit()
    db.refresh(profile)

    metrics = FinancialEngine.calculate_profile_metrics(
        monthly_income=profile.monthly_income,
        current_savings=profile.current_savings,
        essential_expenses=profile.essential_expenses,
        discretionary_expenses=profile.discretionary_expenses,
        existing_debt_emi=profile.existing_debt_emi,
        emergency_fund_target=profile.emergency_fund_target
    )

    return FinancialProfileResponse(
        id=profile.id,
        full_name=profile.full_name,
        monthly_income=profile.monthly_income,
        current_savings=profile.current_savings,
        essential_expenses=profile.essential_expenses,
        discretionary_expenses=profile.discretionary_expenses,
        existing_debt_emi=profile.existing_debt_emi,
        emergency_fund_target=profile.emergency_fund_target,
        planned_purchase_name=profile.planned_purchase_name,
        planned_purchase_amount=profile.planned_purchase_amount,
        planned_purchase_month=profile.planned_purchase_month,
        free_cash_flow=metrics["free_cash_flow"],
        savings_rate_pct=metrics["savings_rate_pct"],
        debt_to_income_pct=metrics["debt_to_income_pct"],
        months_of_runway=metrics["months_of_runway"],
        updated_at=profile.updated_at
    )
