from typing import Dict, List, Any, Optional
from .emi_calculator import EMICalculator, round_curr

class ScenarioEngine:
    @staticmethod
    def simulate_all_scenarios
(
        duration_months: int,
        monthly_income: float,
        current_savings: float,
        essential_expenses: float,
        discretionary_expenses: float,
        existing_debt_emi: float,
        emergency_fund_target: float,
        purchase_name: str = "Laptop",
        purchase_amount: float = 70000.0,
        purchase_month: int = 1,
        purchase_mode: str = "EMI", # "CASH", "EMI", "NONE"
        emi_down_payment: float = 10000.0,
        emi_interest_rate: float = 12.0,
        emi_tenure_months: int = 12,
        unexpected_expense_amount: float = 25000.0,
        unexpected_expense_month: int = 3,
        salary_delay_months: int = 1,
        salary_delay_start_month: int = 2,
        expense_increase_pct: float = 15.0
    ) -> Dict[str, Any]:
        """
        Executes deterministic multi-timeline financial simulation across:
        1. Baseline
        2. Unexpected Emergency Expense
        3. Delayed Salary Timing Shift
        4. Increased Spending / Inflation
        5. Combined Adverse Stress Test
        """
        # Precompute EMI schedule if in EMI mode
        emi_details = None
        if purchase_mode == "EMI" and purchase_amount > emi_down_payment:
            emi_details = EMICalculator.calculate_emi(
                purchase_price=purchase_amount,
                down_payment=emi_down_payment,
                annual_interest_rate=emi_interest_rate,
                tenure_months=emi_tenure_months
            )

        def run_single_timeline(
            scenario_id: str,
            scenario_name: str,
            description: str,
            assumptions: List[str],
            has_unexpected_expense: bool = False,
            has_salary_delay: bool = False,
            expense_multiplier: float = 1.0
        ) -> Dict[str, Any]:
            timeline: List[Dict[str, Any]] = []
            current_bal = current_savings
            lowest_savings = current_savings
            lowest_savings_month = 1
            negative_months_count = 0
            shortfall_months_count = 0
            breaking_point_detected = False
            breaking_point_month = None
            breaking_point_reason = None
            total_income_sum = 0.0
            total_outflows_sum = 0.0

            # Salary delay tracker: queue of delayed salaries
            delayed_pay_in_month: Dict[int, float] = {}

            for m in range(1, duration_months + 1):
                opening_savings = current_bal
                
                # 1. Income calculation
                inc = monthly_income
                if has_salary_delay and m == salary_delay_start_month:
                    # Salary delayed!
                    inc = 0.0
                    resume_month = m + salary_delay_months
                    delayed_pay_in_month[resume_month] = delayed_pay_in_month.get(resume_month, 0.0) + monthly_income

                # Add any delayed pay arriving this month
                if m in delayed_pay_in_month:
                    inc += delayed_pay_in_month[m]

                # 2. Expenses with inflation/multiplier
                ess_exp = round_curr(essential_expenses * expense_multiplier)
                disc_exp = round_curr(discretionary_expenses * expense_multiplier)
                exist_emi = round_curr(existing_debt_emi)

                # 3. Purchase payment
                purch_pay = 0.0
                if purchase_mode == "CASH":
                    if m == purchase_month:
                        purch_pay = purchase_amount
                elif purchase_mode == "EMI" and emi_details:
                    # Down payment in purchase_month
                    if m == purchase_month:
                        purch_pay += emi_details["down_payment"]
                    
                    # EMI payments occur starting in purchase_month through loan tenure
                    emi_month_idx = m - purchase_month
                    if 0 <= emi_month_idx < len(emi_details["schedule"]):
                        purch_pay += emi_details["schedule"][emi_month_idx]["payment_amount"]

                # 4. Unexpected emergency expense
                unexp = 0.0
                if has_unexpected_expense and m == unexpected_expense_month:
                    unexp = unexpected_expense_amount

                # 5. Outflows & Balances
                total_outflows = round_curr(ess_exp + disc_exp + exist_emi + purch_pay + unexp)
                net_cash_flow = round_curr(inc - total_outflows)
                closing_savings = round_curr(opening_savings + net_cash_flow)
                current_bal = closing_savings

                total_income_sum = round_curr(total_income_sum + inc)
                total_outflows_sum = round_curr(total_outflows_sum + total_outflows)

                # Emergency fund analysis
                shortfall = round_curr(max(0.0, emergency_fund_target - closing_savings))
                is_negative = closing_savings < 0.0
                is_under_emergency = closing_savings < emergency_fund_target

                if is_negative:
                    negative_months_count += 1
                if is_under_emergency:
                    shortfall_months_count += 1

                # Breaking point detection (first catastrophic event)
                if not breaking_point_detected:
                    if is_negative:
                        breaking_point_detected = True
                        breaking_point_month = m
                        breaking_point_reason = f"Savings depleted to negative cash balance (₹{closing_savings:,.2f}) in Month {m}."
                    elif is_under_emergency and opening_savings >= emergency_fund_target:
                        breaking_point_detected = True
                        breaking_point_month = m
                        breaking_point_reason = f"Emergency reserve breached below target ₹{emergency_fund_target:,.2f} in Month {m}."

                if closing_savings < lowest_savings:
                    lowest_savings = closing_savings
                    lowest_savings_month = m

                timeline.append({
                    "month": m,
                    "opening_savings": opening_savings,
                    "income_received": round_curr(inc),
                    "essential_expenses": ess_exp,
                    "discretionary_expenses": disc_exp,
                    "existing_emi": exist_emi,
                    "purchase_payment": round_curr(purch_pay),
                    "unexpected_expense": round_curr(unexp),
                    "total_outflows": total_outflows,
                    "net_cash_flow": net_cash_flow,
                    "closing_savings": closing_savings,
                    "emergency_shortfall": shortfall,
                    "is_negative_cash": is_negative,
                    "is_under_emergency_target": is_under_emergency
                })

            # Calculate Resilience Score (0 to 100)
            score = 100
            if negative_months_count > 0:
                score -= min(60, negative_months_count * 20)
            if lowest_savings < 0:
                score -= 25
            elif lowest_savings < emergency_fund_target:
                deficit_ratio = (emergency_fund_target - lowest_savings) / max(1.0, emergency_fund_target)
                score -= int(deficit_ratio * 30)

            score = max(5, min(100, score))

            if score >= 80:
                risk_level = "LOW"
            elif score >= 55:
                risk_level = "MODERATE"
            elif score >= 30:
                risk_level = "HIGH"
            else:
                risk_level = "CRITICAL"

            return {
                "scenario_id": scenario_id,
                "scenario_name": scenario_name,
                "description": description,
                "assumptions": assumptions,
                "lowest_savings": lowest_savings,
                "lowest_savings_month": lowest_savings_month,
                "negative_cash_months": negative_months_count,
                "emergency_shortfall_months": shortfall_months_count,
                "breaking_point_detected": breaking_point_detected,
                "breaking_point_month": breaking_point_month,
                "breaking_point_reason": breaking_point_reason or "No breaking point detected; reserves held positive.",
                "resilience_score": score,
                "risk_level": risk_level,
                "final_savings": current_bal,
                "total_income": total_income_sum,
                "total_outflows": total_outflows_sum,
                "timeline": timeline
            }

        # 1. Baseline
        baseline = run_single_timeline(
            scenario_id="baseline",
            scenario_name="Baseline Reality",
            description="All financial flows occur strictly according to standard expectations.",
            assumptions=["Income received on time every month", "Expenses remain steady", "No unpredicted financial shocks"]
        )

        # 2. Unexpected Expense
        unexpected = run_single_timeline(
            scenario_id="unexpected_expense",
            scenario_name="Medical / Emergency Shock",
            description=f"A sudden unexpected expense of ₹{unexpected_expense_amount:,.0f} strikes in Month {unexpected_expense_month}.",
            assumptions=[f"Unplanned out-of-pocket payment of ₹{unexpected_expense_amount:,.0f} in Month {unexpected_expense_month}", "Normal income and routine expenses continue"],
            has_unexpected_expense=True
        )

        # 3. Delayed Salary
        delayed = run_single_timeline(
            scenario_id="delayed_salary",
            scenario_name="Delayed Salary Flow",
            description=f"Salary is delayed for {salary_delay_months} month(s) starting in Month {salary_delay_start_month}.",
            assumptions=[f"Zero salary received in Month {salary_delay_start_month}", f"Double salary arrives in Month {salary_delay_start_month + salary_delay_months}", "Fixed living expenses & EMIs must still be paid"],
            has_salary_delay=True
        )

        # 4. Increased Spending / Inflation
        inflation = run_single_timeline(
            scenario_id="increased_spending",
            scenario_name="Cost of Living Inflation (+15%)",
            description=f"Routine living and discretionary expenses climb by {expense_increase_pct:.0f}%.",
            assumptions=[f"Essential & discretionary outlays elevated by {expense_increase_pct:.0f}% every month", "Salary remains fixed"],
            expense_multiplier=1.0 + (expense_increase_pct / 100.0)
        )

        # 5. Combined Adverse Scenario
        combined = run_single_timeline(
            scenario_id="combined_adverse",
            scenario_name="Parallel Nightmare (Combined Stress Test)",
            description="Triple storm: Delayed paycheck, unexpected emergency expense, and rising living costs strike together.",
            assumptions=[
                f"₹{unexpected_expense_amount:,.0f} emergency in Month {unexpected_expense_month}",
                f"Salary delayed by {salary_delay_months} month(s) starting Month {salary_delay_start_month}",
                f"Expenses inflated by {expense_increase_pct:.0f}%"
            ],
            has_unexpected_expense=True,
            has_salary_delay=True,
            expense_multiplier=1.0 + (expense_increase_pct / 100.0)
        )

        scenarios = {
            "baseline": baseline,
            "unexpected_expense": unexpected,
            "delayed_salary": delayed,
            "increased_spending": inflation,
            "combined_adverse": combined
        }

        # Global comparison & recommendation
        lowest_overall = min(s["lowest_savings"] for s in scenarios.values())
        has_any_deficit = any(s["negative_cash_months"] > 0 for s in scenarios.values())
        
        if lowest_overall < 0:
            rec = f"Caution: In adverse scenarios, savings drop to a deficit (lowest ₹{lowest_overall:,.2f}). Financing or deferring the purchase is strongly advised unless an additional safety buffer is built."
        elif lowest_overall < emergency_fund_target:
            rec = f"Sustainable with caution: You remain cash-flow positive, but emergency reserves dip to ₹{lowest_overall:,.2f} (below target ₹{emergency_fund_target:,.2f}). Maintain discretionary spending discipline."
        else:
            rec = f"Robust Affordability: Across all 5 parallel futures, your savings stay comfortably above the ₹{emergency_fund_target:,.2f} emergency target. This commitment is resilient."

        return {
            "scenarios": scenarios,
            "comparison_summary": {
                "lowest_overall_savings": lowest_overall,
                "has_cash_deficit_risk": has_any_deficit,
                "safest_scenario": "baseline",
                "most_vulnerable_scenario": "combined_adverse"
            },
            "recommendation": rec
        }
