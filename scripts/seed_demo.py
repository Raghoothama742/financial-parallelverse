import os
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from backend.app.database import SessionLocal, init_db
from backend.app.models import FinancialProfile, InstallmentPlan, InstallmentPayment
from backend.app.services.reminder_service import ReminderService

def seed():
    print("Initializing database...")
    init_db()
    db = SessionLocal()

    try:
        # 1. Seed or Update Financial Profile
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
            print("Created default Financial Profile.")
        else:
            print("Financial Profile already exists.")

        # 2. Seed Installment Plans if empty
        existing_plans = db.query(InstallmentPlan).count()
        if existing_plans == 0:
            today = date.today()

            # Plan 1: Smartphone (12 Months, 12% APR)
            p1_start = today - timedelta(days=120) # Started ~4 months ago
            p1_calc, p1_payments = ReminderService.generate_installment_schedule(
                purchase_name="iPhone 15 Pro",
                total_amount=84000.0,
                down_payment=20000.0,
                annual_interest_rate=12.0,
                tenure_months=12,
                start_date=p1_start,
                due_day=5
            )

            plan1 = InstallmentPlan(
                purchase_name="iPhone 15 Pro",
                category="Smartphones",
                total_amount=84000.0,
                down_payment=20000.0,
                principal_financed=p1_calc["principal_financed"],
                annual_interest_rate=12.0,
                tenure_months=12,
                monthly_emi=p1_calc["monthly_emi"],
                total_repayment=p1_calc["total_repayment"],
                total_interest=p1_calc["total_interest"],
                start_date=p1_start,
                due_day=5,
                status="ACTIVE",
                notes="Purchased during Diwali festival sale on 12-month tenure."
            )
            db.add(plan1)
            db.flush()

            for i, p in enumerate(p1_payments):
                st = "PAID" if i < 4 else ("OVERDUE" if p["due_date"] < today else "PENDING")
                paid_time = datetime.utcnow() if i < 4 else None
                payment = InstallmentPayment(
                    installment_id=plan1.id,
                    installment_number=p["installment_number"],
                    due_date=p["due_date"],
                    emi_amount=p["emi_amount"],
                    principal_portion=p["principal_portion"],
                    interest_portion=p["interest_portion"],
                    remaining_balance=p["remaining_balance"],
                    status=st,
                    paid_at=paid_time,
                    notes=p["notes"]
                )
                db.add(payment)

            # Plan 2: Ergonomic Chair (6 Months, 0% APR)
            p2_start = today - timedelta(days=60)
            p2_calc, p2_payments = ReminderService.generate_installment_schedule(
                purchase_name="Ergonomic Workstation Chair",
                total_amount=18000.0,
                down_payment=3000.0,
                annual_interest_rate=0.0,
                tenure_months=6,
                start_date=p2_start,
                due_day=15
            )

            plan2 = InstallmentPlan(
                purchase_name="Ergonomic Workstation Chair",
                category="Furniture",
                total_amount=18000.0,
                down_payment=3000.0,
                principal_financed=p2_calc["principal_financed"],
                annual_interest_rate=0.0,
                tenure_months=6,
                monthly_emi=p2_calc["monthly_emi"],
                total_repayment=p2_calc["total_repayment"],
                total_interest=p2_calc["total_interest"],
                start_date=p2_start,
                due_day=15,
                status="ACTIVE",
                notes="Zero-cost financing for home office setup."
            )
            db.add(plan2)
            db.flush()

            for i, p in enumerate(p2_payments):
                st = "PAID" if i < 2 else ("OVERDUE" if p["due_date"] < today else "PENDING")
                paid_time = datetime.utcnow() if i < 2 else None
                payment = InstallmentPayment(
                    installment_id=plan2.id,
                    installment_number=p["installment_number"],
                    due_date=p["due_date"],
                    emi_amount=p["emi_amount"],
                    principal_portion=p["principal_portion"],
                    interest_portion=p["interest_portion"],
                    remaining_balance=p["remaining_balance"],
                    status=st,
                    paid_at=paid_time,
                    notes=p["notes"]
                )
                db.add(payment)

            print("Seeded 2 active demo installment plans.")
        else:
            print(f"Database already contains {existing_plans} installment plan(s).")

        db.commit()
        print("Demo seed completed successfully!")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
