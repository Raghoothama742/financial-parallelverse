export interface FinancialProfile {
  id: number;
  full_name: string;
  monthly_income: number;
  current_savings: number;
  essential_expenses: number;
  discretionary_expenses: number;
  existing_debt_emi: number;
  emergency_fund_target: number;
  planned_purchase_name: string;
  planned_purchase_amount: number;
  planned_purchase_month: number;
  free_cash_flow: number;
  savings_rate_pct: number;
  debt_to_income_pct: number;
  months_of_runway: number;
}

export interface ScenarioMonthItem {
  month: number;
  opening_savings: number;
  income_received: number;
  essential_expenses: number;
  discretionary_expenses: number;
  existing_emi: number;
  purchase_payment: number;
  unexpected_expense: number;
  total_outflows: number;
  net_cash_flow: number;
  closing_savings: number;
  emergency_shortfall: number;
  is_negative_cash: boolean;
  is_under_emergency_target: boolean;
}

export interface ScenarioResult {
  scenario_id: string;
  scenario_name: string;
  description: string;
  assumptions: string[];
  lowest_savings: number;
  lowest_savings_month: number;
  negative_cash_months: number;
  emergency_shortfall_months: number;
  breaking_point_detected: boolean;
  breaking_point_month?: number;
  breaking_point_reason?: string;
  resilience_score: number;
  risk_level: 'LOW' | 'MODERATE' | 'HIGH' | 'CRITICAL';
  final_savings: number;
  total_income: number;
  total_outflows: number;
  timeline: ScenarioMonthItem[];
}

export interface ScenarioSimulationResponse {
  scenarios: Record<string, ScenarioResult>;
  comparison_summary: Record<string, any>;
  recommendation: string;
}

export interface PurchaseOptionResult {
  option_id: string;
  option_title: string;
  upfront_cash_required: number;
  monthly_obligation: number;
  total_cost: number;
  remaining_savings_immediately: number;
  emergency_buffer_preserved_pct: number;
  safe_to_proceed: boolean;
  risk_rating: 'SAFE' | 'CAUTION' | 'HIGH_RISK';
  pros: string[];
  cons: string[];
  key_tradeoff: string;
}

export interface PurchaseEvaluationResponse {
  purchase_name: string;
  purchase_amount: number;
  baseline_free_cash_flow: number;
  emergency_fund_target: number;
  current_savings: number;
  options: PurchaseOptionResult[];
  recommended_option_id: string;
  verdict_explanation: string;
}

export interface InstallmentPayment {
  id: number;
  installment_number: number;
  due_date: string;
  emi_amount: number;
  principal_portion: number;
  interest_portion: number;
  remaining_balance: number;
  status: 'PENDING' | 'PAID' | 'OVERDUE';
  paid_at?: string;
  notes?: string;
}

export interface InstallmentPlan {
  id: number;
  purchase_name: string;
  category: string;
  total_amount: number;
  down_payment: number;
  principal_financed: number;
  annual_interest_rate: number;
  tenure_months: number;
  monthly_emi: number;
  total_repayment: number;
  total_interest: number;
  start_date: string;
  due_day: number;
  status: string;
  notes?: string;
  paid_installments_count: number;
  remaining_installments_count: number;
  total_paid_amount: number;
  outstanding_balance: number;
  next_due_date?: string;
  is_overdue: boolean;
  payments: InstallmentPayment[];
}
