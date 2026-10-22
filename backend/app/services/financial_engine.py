from typing import Dict, Any
from .emi_calculator import round_curr

class FinancialEngine:
    @staticmethod
    def calculate_profile_metrics(
        monthly_income: float,
        current_savings: float,
        essential_expenses: float,
        discretionary_expenses: float,
        existing_debt_emi: float,
        emergency_fund_target: float
    ) -> Dict[str, Any]:
        """Calculates core baseline financial indicators."""
        total_monthly_outflows = round_curr(essential_expenses + discretionary_expenses + existing_debt_emi)
        free_cash_flow = round_curr(monthly_income - total_monthly_outflows)
        
        savings_rate = 0.0
        if monthly_income > 0:
            savings_rate = round_curr((free_cash_flow / monthly_income) * 100.0)
            
        debt_to_income = 0.0
        if monthly_income > 0:
            debt_to_income = round_curr((existing_debt_emi / monthly_income) * 100.0)
            
        burn_rate = essential_expenses + existing_debt_emi
        runway_months = round_curr(current_savings / burn_rate) if burn_rate > 0 else 99.0

        emergency_coverage_pct = 0.0
        if emergency_fund_target > 0:
            emergency_coverage_pct = round_curr((current_savings / emergency_fund_target) * 100.0)

        return {
            "free_cash_flow": free_cash_flow,
            "total_monthly_outflows": total_monthly_outflows,
            "savings_rate_pct": savings_rate,
            "debt_to_income_pct": debt_to_income,
            "months_of_runway": runway_months,
            "emergency_coverage_pct": emergency_coverage_pct,
            "is_cash_flow_positive": free_cash_flow >= 0
        }
