from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from typing import List
from datetime import date, datetime
from ..database import get_db
from ..models import InstallmentPlan, InstallmentPayment
from ..schemas import (
    InstallmentPlanCreate, InstallmentPlanUpdate, InstallmentPlanResponse,
    InstallmentPaymentResponse, InstallmentPaymentUpdate
)
from ..services.reminder_service import ReminderService, round_curr

router = APIRouter(prefix="/installments", tags=["Installments & Reminders"])

def _hydrate_plan_response(plan: InstallmentPlan) -> InstallmentPlanResponse:
    today = date.today()
    ReminderService.update_overdue_statuses(plan.payments, today)

    paid_count = sum(1 for p in plan.payments if p.status == "PAID")
    rem_count = len(plan.payments) - paid_count
    total_paid = sum(p.emi_amount for p in plan.payments if p.status == "PAID")
    
    # Outstanding balance = principal_financed - principal_paid_so_far
    principal_paid = sum(p.principal_portion for p in plan.payments if p.status == "PAID")
    outstanding = max(0.0, plan.principal_financed - principal_paid)
    
    # Next upcoming due date
    next_due = None
    has_overdue = False
    for p in plan.payments:
        if p.status == "OVERDUE":
            has_overdue = True
        if p.status in ("PENDING", "OVERDUE") and next_due is None:
            next_due = p.due_date

    payment_responses = [
        InstallmentPaymentResponse(
            id=p.id,
            installment_number=p.installment_number,
            due_date=p.due_date,
            emi_amount=p.emi_amount,
            principal_portion=p.principal_portion,
            interest_portion=p.interest_portion,
            remaining_balance=p.remaining_balance,
            status=p.status,
            paid_at=p.paid_at,
            notes=p.notes
        )
        for p in plan.payments
    ]

    return InstallmentPlanResponse(
        id=plan.id,
        purchase_name=plan.purchase_name,
        category=plan.category,
        total_amount=plan.total_amount,
        down_payment=plan.down_payment,
        principal_financed=plan.principal_financed,
        annual_interest_rate=plan.annual_interest_rate,
        tenure_months=plan.tenure_months,
        monthly_emi=plan.monthly_emi,
        total_repayment=plan.total_repayment,
        total_interest=plan.total_interest,
        start_date=plan.start_date,
        due_day=plan.due_day,
        status=plan.status,
        notes=plan.notes,
        paid_installments_count=paid_count,
        remaining_installments_count=rem_count,
        total_paid_amount=round_curr(total_paid),
        outstanding_balance=round_curr(outstanding),
        next_due_date=next_due,
        is_overdue=has_overdue,
        payments=payment_responses
    )

@router.get("", response_model=List[InstallmentPlanResponse])
def get_installment_plans(db: Session = Depends(get_db)):
    plans = db.query(InstallmentPlan).all()
    res = []
    for plan in plans:
        res.append(_hydrate_plan_response(plan))
    return res

@router.post("", response_model=InstallmentPlanResponse)
def create_installment_plan(data: InstallmentPlanCreate, db: Session = Depends(get_db)):
    start_d = data.start_date or date.today()
    try:
        emi_calc, payments_data = ReminderService.generate_installment_schedule(
            purchase_name=data.purchase_name,
            total_amount=data.total_amount,
            down_payment=data.down_payment,
            annual_interest_rate=data.annual_interest_rate,
            tenure_months=data.tenure_months,
            start_date=start_d,
            due_day=data.due_day
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    plan = InstallmentPlan(
        purchase_name=data.purchase_name,
        category=data.category,
        total_amount=data.total_amount,
        down_payment=data.down_payment,
        principal_financed=emi_calc["principal_financed"],
        annual_interest_rate=data.annual_interest_rate,
        tenure_months=data.tenure_months,
        monthly_emi=emi_calc["monthly_emi"],
        total_repayment=emi_calc["total_repayment"],
        total_interest=emi_calc["total_interest"],
        start_date=start_d,
        due_day=data.due_day,
        status="ACTIVE",
        notes=data.notes
    )
    db.add(plan)
    db.flush()

    for p in payments_data:
        payment = InstallmentPayment(
            installment_id=plan.id,
            installment_number=p["installment_number"],
            due_date=p["due_date"],
            emi_amount=p["emi_amount"],
            principal_portion=p["principal_portion"],
            interest_portion=p["interest_portion"],
            remaining_balance=p["remaining_balance"],
            status=p["status"],
            notes=p["notes"]
        )
        db.add(payment)

    db.commit()
    db.refresh(plan)
    return _hydrate_plan_response(plan)

@router.get("/{plan_id}", response_model=InstallmentPlanResponse)
def get_installment_plan(plan_id: int, db: Session = Depends(get_db)):
    plan = db.query(InstallmentPlan).filter(InstallmentPlan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Installment plan not found.")
    return _hydrate_plan_response(plan)

@router.patch("/{plan_id}", response_model=InstallmentPlanResponse)
def update_installment_plan(plan_id: int, data: InstallmentPlanUpdate, db: Session = Depends(get_db)):
    plan = db.query(InstallmentPlan).filter(InstallmentPlan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Installment plan not found.")

    if data.purchase_name is not None:
        plan.purchase_name = data.purchase_name
    if data.category is not None:
        plan.category = data.category
    if data.status is not None:
        plan.status = data.status
    if data.notes is not None:
        plan.notes = data.notes

    db.commit()
    db.refresh(plan)
    return _hydrate_plan_response(plan)

@router.delete("/{plan_id}")
def delete_installment_plan(plan_id: int, db: Session = Depends(get_db)):
    plan = db.query(InstallmentPlan).filter(InstallmentPlan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Installment plan not found.")

    db.delete(plan)
    db.commit()
    return {"status": "success", "message": f"Plan #{plan_id} deleted successfully."}

@router.patch("/{plan_id}/payments/{payment_id}", response_model=InstallmentPaymentResponse)
def update_payment_status(plan_id: int, payment_id: int, data: InstallmentPaymentUpdate, db: Session = Depends(get_db)):
    payment = db.query(InstallmentPayment).filter(
        InstallmentPayment.id == payment_id,
        InstallmentPayment.installment_id == plan_id
    ).first()

    if not payment:
        raise HTTPException(status_code=404, detail="Payment record not found.")

    if data.status.upper() == "PAID":
        payment.status = "PAID"
        payment.paid_at = datetime.utcnow()
    elif data.status.upper() == "PENDING":
        payment.status = "PENDING"
        payment.paid_at = None
        if payment.due_date < date.today():
            payment.status = "OVERDUE"
    else:
        raise HTTPException(status_code=400, detail="Status must be PAID or PENDING.")

    if data.notes is not None:
        payment.notes = data.notes

    db.commit()
    db.refresh(payment)
    return payment

@router.get("/{plan_id}/calendar")
def download_calendar_reminders(plan_id: int, db: Session = Depends(get_db)):
    plan = db.query(InstallmentPlan).filter(InstallmentPlan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Installment plan not found.")

    ics_data = ReminderService.generate_ics_calendar(plan.purchase_name, plan.payments)
    filename = f"{plan.purchase_name.replace(' ', '_')}_EMI_Reminders.ics"
    
    return Response(
        content=ics_data,
        media_type="text/calendar",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
