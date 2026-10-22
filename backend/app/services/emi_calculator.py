import math
from typing import List, Dict, Any

def round_curr(val: float) -> float:
    """Consistently round currency values to 2 decimal places."""
    return round(float(val) + 1e-9, 2)

class EMICalculator:
    @staticmethod
    def calculate_emi(
        purchase_price: float,
        down_payment: float = 0.0,
        annual_interest_rate: float = 0.0,
        tenure_months: int = 12,
        extra_monthly_payment: float = 0.0
    ) -> Dict[str, Any]:
        """
        Calculates loan EMI and returns full month-by-month amortization schedule.
        Validates inputs and handles zero-interest as well as early repayments.
        """
        if purchase_price <= 0:
            raise ValueError("Purchase price must be greater than zero.")
        if down_payment < 0:
            raise ValueError("Down payment cannot be negative.")
        if down_payment >= purchase_price:
            raise ValueError("Down payment cannot equal or exceed purchase price.")
        if tenure_months < 1:
            raise ValueError("Tenure must be at least 1 month.")
        if annual_interest_rate < 0:
            raise ValueError("Annual interest rate cannot be negative.")
        if extra_monthly_payment < 0:
            raise ValueError("Extra monthly payment cannot be negative.")

        principal = round_curr(purchase_price - down_payment)
        
        # Monthly interest rate
        monthly_r = (annual_interest_rate / 100.0) / 12.0
        
        if monthly_r == 0.0:
            # Zero-interest financing
            base_emi = round_curr(principal / tenure_months)
        else:
            factor = math.pow(1.0 + monthly_r, tenure_months)
            base_emi = round_curr(principal * monthly_r * factor / (factor - 1.0))

        schedule: List[Dict[str, Any]] = []
        remaining_balance = principal
        cumulative_interest = 0.0
        total_paid = 0.0

        for m in range(1, tenure_months + 1):
            if remaining_balance <= 0:
                break
                
            interest_portion = round_curr(remaining_balance * monthly_r) if monthly_r > 0 else 0.0
            planned_payment = base_emi + extra_monthly_payment
            
            # If final month or extra payment exceeds balance
            if m == tenure_months or (remaining_balance + interest_portion) <= planned_payment:
                actual_payment = round_curr(remaining_balance + interest_portion)
                principal_portion = round_curr(remaining_balance)
                remaining_balance = 0.0
            else:
                principal_portion = round_curr(planned_payment - interest_portion)
                if principal_portion > remaining_balance:
                    principal_portion = round_curr(remaining_balance)
                    actual_payment = round_curr(principal_portion + interest_portion)
                    remaining_balance = 0.0
                else:
                    actual_payment = planned_payment
                    remaining_balance = round_curr(remaining_balance - principal_portion)

            cumulative_interest = round_curr(cumulative_interest + interest_portion)
            total_paid = round_curr(total_paid + actual_payment)

            schedule.append({
                "month": m,
                "payment_amount": actual_payment,
                "principal_paid": principal_portion,
                "interest_paid": interest_portion,
                "remaining_balance": remaining_balance,
                "cumulative_interest": cumulative_interest
            })

        return {
            "purchase_price": round_curr(purchase_price),
            "down_payment": round_curr(down_payment),
            "principal_financed": principal,
            "annual_interest_rate": round(annual_interest_rate, 2),
            "tenure_months": tenure_months,
            "monthly_emi": base_emi,
            "total_interest": cumulative_interest,
            "total_repayment": total_paid,
            "schedule": schedule
        }
