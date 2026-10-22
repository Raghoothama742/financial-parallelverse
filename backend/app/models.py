from datetime import datetime, date
from sqlalchemy import (
    Column, Integer, String, Float, Boolean, DateTime, Date, ForeignKey, Text, JSON
)
from sqlalchemy.orm import relationship
from .database import Base

class FinancialProfile(Base):
    __tablename__ = "financial_profiles"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), default="Alex Johnson")
    monthly_income = Column(Float, nullable=False, default=75000.0)
    current_savings = Column(Float, nullable=False, default=120000.0)
    essential_expenses = Column(Float, nullable=False, default=32000.0)
    discretionary_expenses = Column(Float, nullable=False, default=15000.0)
    existing_debt_emi = Column(Float, nullable=False, default=8000.0)
    emergency_fund_target = Column(Float, nullable=False, default=150000.0)
    
    # Default active purchase planning
    planned_purchase_name = Column(String(150), default="MacBook Pro / Performance Laptop")
    planned_purchase_amount = Column(Float, default=70000.0)
    planned_purchase_month = Column(Integer, default=1)
    
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ScenarioSimulation(Base):
    __tablename__ = "scenario_simulations"

    id = Column(Integer, primary_key=True, index=True)
    simulation_name = Column(String(150), nullable=False)
    purchase_name = Column(String(150), default="")
    purchase_amount = Column(Float, default=0.0)
    purchase_mode = Column(String(50), default="EMI") # "CASH", "EMI", "SAVE_LATER"
    duration_months = Column(Integer, default=12)
    
    # Configuration inputs
    unexpected_expense_amount = Column(Float, default=25000.0)
    unexpected_expense_month = Column(Integer, default=3)
    salary_delay_months = Column(Integer, default=1)
    salary_delay_start_month = Column(Integer, default=2)
    expense_increase_pct = Column(Float, default=15.0)
    
    # Results stored as JSON
    results_summary = Column(JSON, nullable=True)
    full_projection = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class InstallmentPlan(Base):
    __tablename__ = "installment_plans"

    id = Column(Integer, primary_key=True, index=True)
    purchase_name = Column(String(150), nullable=False)
    category = Column(String(50), default="Electronics")
    total_amount = Column(Float, nullable=False)
    down_payment = Column(Float, nullable=False, default=0.0)
    principal_financed = Column(Float, nullable=False)
    annual_interest_rate = Column(Float, nullable=False, default=12.0)
    tenure_months = Column(Integer, nullable=False, default=12)
    monthly_emi = Column(Float, nullable=False)
    total_repayment = Column(Float, nullable=False)
    total_interest = Column(Float, nullable=False)
    start_date = Column(Date, nullable=False, default=date.today)
    due_day = Column(Integer, nullable=False, default=5)
    status = Column(String(50), default="ACTIVE") # ACTIVE, COMPLETED, CANCELLED
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    payments = relationship("InstallmentPayment", back_populates="plan", cascade="all, delete-orphan", order_by="InstallmentPayment.installment_number")

class InstallmentPayment(Base):
    __tablename__ = "installment_payments"

    id = Column(Integer, primary_key=True, index=True)
    installment_id = Column(Integer, ForeignKey("installment_plans.id", ondelete="CASCADE"), nullable=False)
    installment_number = Column(Integer, nullable=False)
    due_date = Column(Date, nullable=False)
    emi_amount = Column(Float, nullable=False)
    principal_portion = Column(Float, nullable=False)
    interest_portion = Column(Float, nullable=False)
    remaining_balance = Column(Float, nullable=False)
    status = Column(String(50), default="PENDING") # PENDING, PAID, OVERDUE
    paid_at = Column(DateTime, nullable=True)
    notes = Column(String(200), nullable=True)

    plan = relationship("InstallmentPlan", back_populates="payments")
