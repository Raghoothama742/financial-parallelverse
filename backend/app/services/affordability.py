from typing import Dict, List, Any
from .emi_calculator import EMICalculator, round_curr

class AffordabilityPlanner:
    @staticmethod
    def evaluate_purchase(
        monthly_income: float,
        current_savings: float,
        essential_expenses: float,
        discretionary_expenses: float,
        existing_debt_emi: float,
        emergency_fund_target: float,
        purchase_name: str = "MacBook Pro / Performance Laptop",
        purchase_amount: float = 70000.0,
        cheaper_alternative_name: str = "Mid-Range Laptop",
        cheaper_alternative_amount: float = 42000.0,
        wait_months: int = 4,
        emi_down_payment: float = 10000.0,
        emi_interest_rate: float = 12.0,
        emi_tenure_months: int = 12
    ) -> Dict[str, Any]:
        """
        Evaluates 4 pathways for financing a planned purchase:
        1. Buy Immediately with Cash
        2. Save First & Buy Later
        3. Buy a Cheaper Alternative
        4. Finance with Reducing-Balance EMI
        """
        free_cash_flow = round_curr(monthly_income - (essential_expenses + discretionary_expenses + existing_debt_emi))
        options: List[Dict[str, Any]] = []

        # Option 1: Buy Immediately with Cash
        opt1_rem_savings = round_curr(current_savings - purchase_amount)
        opt1_buffer_pct = round_curr((opt1_rem_savings / emergency_fund_target * 100.0)) if emergency_fund_target > 0 else 100.0
        opt1_safe = opt1_rem_savings >= emergency_fund_target
        if opt1_rem_savings < 0:
            opt1_risk = "HIGH_RISK"
        elif opt1_rem_savings < emergency_fund_target:
            opt1_risk = "CAUTION"
        else:
            opt1_risk = "SAFE"

        options.append({
            "option_id": "buy_cash_now",
            "option_title": f"Buy Immediately with Cash (₹{purchase_amount:,.0f})",
            "upfront_cash_required": purchase_amount,
            "monthly_obligation": 0.0,
            "total_cost": purchase_amount,
            "remaining_savings_immediately": opt1_rem_savings,
            "emergency_buffer_preserved_pct": max(0.0, opt1_buffer_pct),
            "safe_to_proceed": opt1_safe,
            "risk_rating": opt1_risk,
            "pros": ["Zero interest charges or financing fees", "No monthly debt overhang or tracking required"],
            "cons": [f"Drains ₹{purchase_amount:,.0f} from liquid reserves immediately", f"Emergency reserve left at {opt1_buffer_pct:.0f}% of target"],
            "key_tradeoff": "Immediate ownership vs. immediate depletion of your liquid cash cushion."
        })

        # Option 2: Save First and Buy Later
        projected_savings_growth = round_curr(max(0.0, free_cash_flow) * wait_months)
        future_savings_before_buy = round_curr(current_savings + projected_savings_growth)
        opt2_rem_savings = round_curr(future_savings_before_buy - purchase_amount)
        opt2_buffer_pct = round_curr((opt2_rem_savings / emergency_fund_target * 100.0)) if emergency_fund_target > 0 else 100.0
        opt2_safe = opt2_rem_savings >= emergency_fund_target
        opt2_risk = "SAFE" if opt2_safe else ("CAUTION" if opt2_rem_savings >= 0 else "HIGH_RISK")

        options.append({
            "option_id": "save_and_wait",
            "option_title": f"Save First & Buy in {wait_months} Months",
            "upfront_cash_required": 0.0,
            "monthly_obligation": 0.0,
            "total_cost": purchase_amount,
            "remaining_savings_immediately": current_savings,
            "emergency_buffer_preserved_pct": max(0.0, opt2_buffer_pct),
            "safe_to_proceed": opt2_safe,
            "risk_rating": opt2_risk,
            "pros": ["Protects existing emergency reserves intact today", "Allows testing whether monthly savings habits hold"],
            "cons": [f"Purchase delayed by {wait_months} months", "Requires strict savings discipline"],
            "key_tradeoff": "Delayed gratification in exchange for absolute financial stability."
        })

        # Option 3: Cheaper Alternative
        opt3_rem_savings = round_curr(current_savings - cheaper_alternative_amount)
        opt3_buffer_pct = round_curr((opt3_rem_savings / emergency_fund_target * 100.0)) if emergency_fund_target > 0 else 100.0
        opt3_safe = opt3_rem_savings >= emergency_fund_target
        opt3_risk = "SAFE" if opt3_safe else ("CAUTION" if opt3_rem_savings >= 0 else "HIGH_RISK")

        options.append({
            "option_id": "cheaper_alternative",
            "option_title": f"Choose Alternative: {cheaper_alternative_name} (₹{cheaper_alternative_amount:,.0f})",
            "upfront_cash_required": cheaper_alternative_amount,
            "monthly_obligation": 0.0,
            "total_cost": cheaper_alternative_amount,
            "remaining_savings_immediately": opt3_rem_savings,
            "emergency_buffer_preserved_pct": max(0.0, opt3_buffer_pct),
            "safe_to_proceed": opt3_safe,
            "risk_rating": opt3_risk,
            "pros": [f"Saves ₹{purchase_amount - cheaper_alternative_amount:,.0f} compared to primary target", "Preserves more cash for sudden emergencies"],
            "cons": ["May sacrifice premium specifications or luxury features"],
            "key_tradeoff": "Satisfies functional utility while preserving greater financial resilience."
        })

        # Option 4: Buy via EMI
        opt4_emi = EMICalculator.calculate_emi(
            purchase_price=purchase_amount,
            down_payment=emi_down_payment,
            annual_interest_rate=emi_interest_rate,
            tenure_months=emi_tenure_months
        )
        opt4_rem_savings = round_curr(current_savings - emi_down_payment)
        opt4_buffer_pct = round_curr((opt4_rem_savings / emergency_fund_target * 100.0)) if emergency_fund_target > 0 else 100.0
        opt4_monthly_emi = opt4_emi["monthly_emi"]
        opt4_total_cost = round_curr(emi_down_payment + opt4_emi["total_repayment"])
        
        # Rule: EMI must be <= 50% of free cash flow AND remaining savings >= 70% emergency target
        emi_fits_cashflow = free_cash_flow >= (opt4_monthly_emi * 1.5)
        opt4_safe = emi_fits_cashflow and (opt4_rem_savings >= emergency_fund_target * 0.7)
        if (opt4_monthly_emi > free_cash_flow) or opt4_rem_savings < 0:
            opt4_risk = "HIGH_RISK"
        elif not emi_fits_cashflow or opt4_rem_savings < emergency_fund_target:
            opt4_risk = "CAUTION"
        else:
            opt4_risk = "SAFE"

        options.append({
            "option_id": "buy_via_emi",
            "option_title": f"Finance via {emi_tenure_months}M EMI (₹{opt4_monthly_emi:,.0f}/mo)",
            "upfront_cash_required": emi_down_payment,
            "monthly_obligation": opt4_monthly_emi,
            "total_cost": opt4_total_cost,
            "remaining_savings_immediately": opt4_rem_savings,
            "emergency_buffer_preserved_pct": max(0.0, opt4_buffer_pct),
            "safe_to_proceed": opt4_safe,
            "risk_rating": opt4_risk,
            "pros": [f"Low upfront outlay of ₹{emi_down_payment:,.0f}", f"Preserves ₹{opt4_rem_savings:,.0f} liquid cash buffer"],
            "cons": [f"Costs ₹{opt4_emi['total_interest']:,.0f} in interest", f"Locks ₹{opt4_monthly_emi:,.0f}/month cash flow for {emi_tenure_months} months"],
            "key_tradeoff": "Immediate possession with low upfront cash, paid for by future cash flow commitment & interest."
        })

        # Selection of recommended option
        if opt1_safe:
            recommended_id = "buy_cash_now"
            verdict = "Your current savings cover the full price while keeping your emergency fund 100% intact. Buying in cash is the cleanest, interest-free option."
        elif opt4_safe and opt4_rem_savings >= emergency_fund_target * 0.8:
            recommended_id = "buy_via_emi"
            verdict = "Buying in cash would aggressively deplete your emergency reserve. Financing through a structured EMI keeps your liquid cushion safe while comfortably fitting inside your monthly cash flow."
        elif opt3_safe:
            recommended_id = "cheaper_alternative"
            verdict = f"The ₹{purchase_amount:,.0f} model stretches your finances. The {cheaper_alternative_name} at ₹{cheaper_alternative_amount:,.0f} preserves your safety cushion while meeting your needs."
        else:
            recommended_id = "save_and_wait"
            verdict = f"All immediate purchase pathways present elevated financial risk. Deferring the purchase by {wait_months} months allows your monthly savings to safely accumulate without risk of overdraft."

        return {
            "purchase_name": purchase_name,
            "purchase_amount": purchase_amount,
            "baseline_free_cash_flow": free_cash_flow,
            "emergency_fund_target": emergency_fund_target,
            "current_savings": current_savings,
            "options": options,
            "recommended_option_id": recommended_id,
            "verdict_explanation": verdict
        }
