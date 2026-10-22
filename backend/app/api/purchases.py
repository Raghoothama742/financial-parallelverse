from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import FinancialProfile
from ..schemas import PurchaseEvaluationRequest, PurchaseEvaluationResponse
from ..services.affordability import AffordabilityPlanner

router = APIRouter(prefix="/purchases", tags=["Purchase Affordability"])

@router.post("/evaluate", response_model=PurchaseEvaluationResponse)
def evaluate_purchase(req: PurchaseEvaluationRequest, db: Session = Depends(get_db)):
    profile = db.query(FinancialProfile).first()
    
    inc = profile.monthly_income if profile else 75000.0
    sav = profile.current_savings if profile else 120000.0
    ess = profile.essential_expenses if profile else 32000.0
    disc = profile.discretionary_expenses if profile else 15000.0
    debt = profile.existing_debt_emi if profile else 8000.0
    emerg = profile.emergency_fund_target if profile else 150000.0

    result = AffordabilityPlanner.evaluate_purchase(
        monthly_income=inc,
        current_savings=sav,
        essential_expenses=ess,
        discretionary_expenses=disc,
        existing_debt_emi=debt,
        emergency_fund_target=emerg,
        purchase_name=req.purchase_name,
        purchase_amount=req.purchase_amount,
        cheaper_alternative_name=req.cheaper_alternative_name,
        cheaper_alternative_amount=req.cheaper_alternative_amount,
        wait_months=req.wait_months,
        emi_down_payment=req.emi_down_payment,
        emi_interest_rate=req.emi_interest_rate,
        emi_tenure_months=req.emi_tenure_months
    )

    return result
