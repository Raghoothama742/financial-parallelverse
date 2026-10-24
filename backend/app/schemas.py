from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Dict, Any
from datetime import date, datetime

class HealthResponse(BaseModel):
    status: str = "ok"
    version: str = "1.0.0"
    timestamp: datetime = Field(default_factory=datetime.utcnow)

# Financial Profile Schemas
class FinancialProfileBase(BaseModel):
    full_name: str = "Alex Johnson"
    monthly_income: float = Field(..., ge=0, description="Monthly take-home income")
    current_savings: float = Field(..., ge=0, description="Current total liquid savings")
    essential_expenses: float = Field(..., ge=0, description="Groceries, rent, bills, healthcare")
    discretionary_expenses: float = Field(..., ge=0, description="Dining, shopping, subscriptions")
    existing_debt_emi: float = Field(default=0.0, ge=0, description="Existing ongoing loan & credit card EMIs")
    emergency_fund_target: float = Field(default=150000.0, ge=0, description="Safety reserve target (e.g. 3-6 months)")
    planned_purchase_name: str = Field(default="Laptop", description="Item user intends to purchase")
    planned_purchase_amount: float = Field(default=70000.0, ge=0, description="Cost of planned purchase")
    planned_purchase_month: int = Field(default=1, ge=1, le=60, description="Month number when purchase occurs")

class FinancialProfileUpdate(FinancialProfileBase):
    pass

class FinancialProfileResponse(FinancialProfileBase):
    id: int
    free_cash_flow: float
    savings_rate_pct: float
    debt_to_income_pct: float
    months_of_runway: float
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# EMI Schemas
class EMICalculationRequest(BaseModel):
    purchase_price: float = Field(..., gt=0, description="Total purchase price")
    down_payment: float = Field(default=0.0, ge=0, description="Upfront down payment")
    annual_interest_rate: float = Field(..., ge=0, le=100, description="Annual nominal interest rate in %")
    tenure_months: int = Field(..., ge=1, le=360, description="Loan tenure in months")
    extra_monthly_payment: float = Field(default=0.0, ge=0, description="Optional extra prepayment per month")

    @field_validator("down_payment")
    @classmethod
    def validate_down_payment(cls, v, values):
        return v

class EMIAmortizationMonth(BaseModel):
    month: int
    payment_amount: float
    principal_paid: float
    interest_paid: float
    remaining_balance: float
    cumulative_interest: float

class EMICalculationResponse(BaseModel):
    purchase_price: float
    down_payment: float
    principal_financed: float
    annual_interest_rate: float
    tenure_months: int
    monthly_emi: float
    total_interest: float
    total_repayment: float
    schedule: List[EMIAmortizationMonth]

# Scenario Simulation Schemas
class ScenarioSimulationRequest(BaseModel):
    duration_months: int = Field(default=12, ge=6, le=36)
    
    # Financial profile overrides (if not using saved DB profile)
    monthly_income: Optional[float] = Field(default=None, ge=0)
    current_savings: Optional[float] = Field(default=None, ge=0)
    essential_expenses: Optional[float] = Field(default=None, ge=0)
    discretionary_expenses: Optional[float] = Field(default=None, ge=0)
    existing_debt_emi: Optional[float] = Field(default=None, ge=0)
    emergency_fund_target: Optional[float] = Field(default=None, ge=0)
    
    # Purchase details
    purchase_name: str = "Laptop"
    purchase_amount: float = Field(default=70000.0, ge=0)
    purchase_month: int = Field(default=1, ge=1)
    purchase_mode: str = Field(default="EMI", description="CASH, EMI, or NONE")
    
    # EMI configuration if purchase_mode is EMI
    emi_down_payment: float = Field(default=10000.0, ge=0)
    emi_interest_rate: float = Field(default=12.0, ge=0)
    emi_tenure_months: int = Field(default=12, ge=1)
    
    # Stress parameters
    unexpected_expense_amount: float = Field(default=25000.0, ge=0)
    unexpected_expense_month: int = Field(default=3, ge=1)
    salary_delay_months: int = Field(default=1, ge=0)
    salary_delay_start_month: int = Field(default=2, ge=1)
    expense_increase_pct: float = Field(default=15.0, ge=0, le=300)
    income_reduction_pct: float = Field(default=25.0, ge=0, le=100, description="Income reduction in the combined stress scenario")
    recurring_emergency_cost: float = Field(default=5000.0, ge=0, description="Recurring unexpected monthly cost during the combined stress scenario")
    recurring_cost_start_month: int = Field(default=3, ge=1, le=36)
    monthly_inflation_pct: float = Field(default=1.0, ge=0, le=25, description="Additional month-on-month expense growth in the inflation scenarios")
    investment_return_pct: float = Field(default=0.0, ge=-100, le=100, description="Optional monthly savings return assumption, expressed as an annual percentage")

class ScenarioMonthItem(BaseModel):
    month: int
    opening_savings: float
    income_received: float
    essential_expenses: float
    discretionary_expenses: float
    existing_emi: float
    purchase_payment: float
    unexpected_expense: float
    total_outflows: float
    net_cash_flow: float
    closing_savings: float
    emergency_shortfall: float
    is_negative_cash: bool
    is_under_emergency_target: bool

class ScenarioResult(BaseModel):
    scenario_id: str
    scenario_name: str
    description: str
    assumptions: List[str]
    lowest_savings: float
    lowest_savings_month: int
    negative_cash_months: int
    emergency_shortfall_months: int
    breaking_point_detected: bool
    breaking_point_month: Optional[int] = None
    breaking_point_reason: Optional[str] = None
    resilience_score: int # 0 to 100
    risk_level: str # LOW, MODERATE, HIGH, CRITICAL
    final_savings: float
    total_income: float
    total_outflows: float
    timeline: List[ScenarioMonthItem]

class ScenarioSimulationResponse(BaseModel):
    scenarios: Dict[str, ScenarioResult]
    comparison_summary: Dict[str, Any]
    recommendation: str

# Purchase Affordability Schemas
class PurchaseEvaluationRequest(BaseModel):
    purchase_name: str = "MacBook Pro / Performance Laptop"
    purchase_amount: float = Field(default=70000.0, gt=0)
    cheaper_alternative_name: str = Field(default="Mid-Range Laptop", description="Alternative model")
    cheaper_alternative_amount: float = Field(default=42000.0, gt=0)
    wait_months: int = Field(default=4, ge=1, le=24)
    emi_down_payment: float = Field(default=10000.0, ge=0)
    emi_interest_rate: float = Field(default=12.0, ge=0)
    emi_tenure_months: int = Field(default=12, ge=1)

class PurchaseOptionResult(BaseModel):
    option_id: str
    option_title: str
    upfront_cash_required: float
    monthly_obligation: float
    total_cost: float
    remaining_savings_immediately: float
    emergency_buffer_preserved_pct: float
    safe_to_proceed: bool
    risk_rating: str # SAFE, CAUTION, HIGH_RISK
    pros: List[str]
    cons: List[str]
    key_tradeoff: str

class PurchaseEvaluationResponse(BaseModel):
    purchase_name: str
    purchase_amount: float
    baseline_free_cash_flow: float
    emergency_fund_target: float
    current_savings: float
    options: List[PurchaseOptionResult]
    recommended_option_id: str
    verdict_explanation: str

# Installment Schemas
class InstallmentPaymentResponse(BaseModel):
    id: int
    installment_number: int
    due_date: date
    emi_amount: float
    principal_portion: float
    interest_portion: float
    remaining_balance: float
    status: str
    paid_at: Optional[datetime] = None
    notes: Optional[str] = None

    class Config:
        from_attributes = True

class InstallmentPlanCreate(BaseModel):
    purchase_name: str
    category: str = "Electronics"
    total_amount: float = Field(..., gt=0)
    down_payment: float = Field(default=0.0, ge=0)
    annual_interest_rate: float = Field(..., ge=0)
    tenure_months: int = Field(..., ge=1, le=360)
    start_date: Optional[date] = None
    due_day: int = Field(default=5, ge=1, le=31)
    notes: Optional[str] = None

class InstallmentPlanUpdate(BaseModel):
    purchase_name: Optional[str] = None
    category: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None

class InstallmentPlanResponse(BaseModel):
    id: int
    purchase_name: str
    category: str
    total_amount: float
    down_payment: float
    principal_financed: float
    annual_interest_rate: float
    tenure_months: int
    monthly_emi: float
    total_repayment: float
    total_interest: float
    start_date: date
    due_day: int
    status: str
    notes: Optional[str] = None
    paid_installments_count: int = 0
    remaining_installments_count: int = 0
    total_paid_amount: float = 0.0
    outstanding_balance: float = 0.0
    next_due_date: Optional[date] = None
    is_overdue: bool = False
    payments: List[InstallmentPaymentResponse] = []

    class Config:
        from_attributes = True

class InstallmentPaymentUpdate(BaseModel):
    status: str = Field(..., description="PAID or PENDING")
    notes: Optional[str] = None
