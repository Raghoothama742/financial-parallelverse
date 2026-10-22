from fastapi import APIRouter, HTTPException
from ..schemas import EMICalculationRequest, EMICalculationResponse
from ..services.emi_calculator import EMICalculator

router = APIRouter(prefix="/emi", tags=["EMI Calculator"])

@router.post("/calculate", response_model=EMICalculationResponse)
def calculate_emi(req: EMICalculationRequest):
    try:
        res = EMICalculator.calculate_emi(
            purchase_price=req.purchase_price,
            down_payment=req.down_payment,
            annual_interest_rate=req.annual_interest_rate,
            tenure_months=req.tenure_months,
            extra_monthly_payment=req.extra_monthly_payment
        )
        return res
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
