import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import date, datetime, timedelta
import sys
from pathlib import Path
import json

# Setup sys.path for local service imports
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from backend.app.services.financial_engine import FinancialEngine
from backend.app.services.scenario_engine import ScenarioEngine
from backend.app.services.affordability import AffordabilityPlanner
from backend.app.services.emi_calculator import EMICalculator
from backend.app.services.reminder_service import ReminderService
from backend.app.database import SessionLocal, init_db
from backend.app.models import FinancialProfile, InstallmentPlan, InstallmentPayment

# Initialize database
init_db()

# Page configuration
st.set_page_config(
    page_title="Financial Parallelverse | Multi-Future FinTech Simulator",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-End FinTech SaaS CSS Design System
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    /* Global Theme */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    .stApp {
        background: radial-gradient(circle at 10% 10%, #0d1527 0%, #080c16 60%, #050811 100%);
        color: #f1f5f9;
    }

    /* Top Navigation Banner */
    .top-banner {
        background: linear-gradient(90deg, rgba(16, 185, 129, 0.12) 0%, rgba(6, 182, 212, 0.12) 50%, rgba(99, 102, 241, 0.12) 100%);
        border: 1px solid rgba(16, 185, 129, 0.25);
        border-radius: 12px;
        padding: 0.65rem 1.25rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.5rem;
    }

    /* Gradient Typography */
    .gradient-header {
        background: linear-gradient(135deg, #ffffff 20%, #10b981 70%, #06b6d4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        letter-spacing: -0.03em;
    }

    .sub-gradient {
        background: linear-gradient(135deg, #10b981 0%, #06b6d4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
    }

    /* Glassmorphic FinTech Cards */
    .fin-card {
        background: linear-gradient(135deg, rgba(19, 29, 49, 0.7) 0%, rgba(13, 20, 36, 0.85) 100%);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 1.4rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.06);
        transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
        margin-bottom: 1.2rem;
        position: relative;
        overflow: hidden;
    }

    .fin-card:hover {
        transform: translateY(-2px);
        border-color: rgba(16, 185, 129, 0.35);
        box-shadow: 0 14px 35px rgba(0, 0, 0, 0.5), 0 0 20px rgba(16, 185, 129, 0.12);
    }

    .fin-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; height: 2px;
        background: linear-gradient(90deg, transparent, rgba(16, 185, 129, 0.6), transparent);
    }

    /* Stat Numbers & Labels */
    .stat-label {
        color: #94a3b8;
        font-size: 0.78rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 0.35rem;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    .stat-value {
        font-size: 1.95rem;
        font-weight: 800;
        color: #f8fafc;
        letter-spacing: -0.02em;
        font-feature-settings: "cv02", "cv03", "cv04", "cv11";
        line-height: 1.1;
    }

    .stat-footer {
        font-size: 0.78rem;
        margin-top: 0.45rem;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    .stat-positive { color: #10b981; }
    .stat-negative { color: #f43f5e; }
    .stat-warning { color: #f59e0b; }
    .stat-info { color: #38bdf8; }

    /* Scenario Timeline Pill Badges */
    .badge {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        padding: 0.28rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }
    .badge-success { background: rgba(16, 185, 129, 0.14); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.3); }
    .badge-warning { background: rgba(245, 158, 11, 0.14); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.3); }
    .badge-danger { background: rgba(244, 63, 94, 0.14); color: #fb7185; border: 1px solid rgba(244, 63, 94, 0.3); }
    .badge-info { background: rgba(6, 182, 212, 0.14); color: #38bdf8; border: 1px solid rgba(6, 182, 212, 0.3); }

    /* Alert Boxes */
    .alert-banner {
        border-radius: 12px;
        padding: 1rem 1.35rem;
        margin-bottom: 1.25rem;
        display: flex;
        align-items: flex-start;
        gap: 12px;
    }
    .alert-danger {
        background: linear-gradient(90deg, rgba(244, 63, 94, 0.15) 0%, rgba(225, 29, 72, 0.08) 100%);
        border: 1px solid rgba(244, 63, 94, 0.35);
        color: #fecdd3;
    }
    .alert-warning {
        background: linear-gradient(90deg, rgba(245, 158, 11, 0.15) 0%, rgba(217, 119, 6, 0.08) 100%);
        border: 1px solid rgba(245, 158, 11, 0.35);
        color: #fef3c7;
    }
    .alert-success {
        background: linear-gradient(90deg, rgba(16, 185, 129, 0.15) 0%, rgba(5, 150, 105, 0.08) 100%);
        border: 1px solid rgba(16, 185, 129, 0.35);
        color: #d1fae5;
    }

    /* Streamlit Sidebar Customization */
    section[data-testid="stSidebar"] {
        background: #090e1a !important;
        border-right: 1px solid rgba(255, 255, 255, 0.07);
    }

    section[data-testid="stSidebar"] .stRadio label {
        color: #94a3b8 !important;
        font-weight: 500;
        font-size: 0.92rem;
    }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: #041a11 !important;
        font-weight: 700;
        border: none;
        border-radius: 10px;
        padding: 0.55rem 1.4rem;
        box-shadow: 0 4px 14px rgba(16, 185, 129, 0.3);
        transition: all 0.25s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #34d399 0%, #10b981 100%);
        color: #02120b !important;
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.45);
        transform: translateY(-1px);
    }

    /* Inputs */
    div[data-baseweb="input"] {
        background-color: #0f172a !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 8px !important;
        color: #f8fafc !important;
    }

    /* Progress bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #10b981 0%, #06b6d4 100%);
        border-radius: 9999px;
    }
</style>
""", unsafe_allow_html=True)

# Database helper
def get_user_profile():
    db = SessionLocal()
    try:
        p = db.query(FinancialProfile).first()
        if not p:
            p = FinancialProfile(
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
            db.add(p)
            db.commit()
            db.refresh(p)
        return p
    finally:
        db.close()

# Sidebar Navigation & Demo Presets
with st.sidebar:
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 22px;">
        <div style="width: 44px; height: 44px; border-radius: 12px; background: linear-gradient(135deg, #10b981 0%, #06b6d4 100%); display: flex; align-items: center; justify-content: center; font-size: 1.5rem; box-shadow: 0 4px 15px rgba(16, 185, 129, 0.35);">
            🌌
        </div>
        <div>
            <h2 style="margin: 0; font-size: 1.2rem; font-weight: 800; color: #f8fafc; letter-spacing: -0.02em;">Parallelverse</h2>
            <p style="margin: 0; font-size: 0.74rem; color: #10b981; font-weight: 600;">FinTech Future Simulator</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "NAVIGATION",
        [
            "📊 Executive Dashboard",
            "🔮 Parallel Futures Simulator",
            "⚖️ Purchase Affordability Matrix",
            "🧮 Reducing-Balance EMI Engine",
            "📅 Installment Tracker & Reminders",
            "👤 Financial Profile & Presets"
        ],
        index=0
    )

    st.markdown("---")
    
    # Quick Preset Persona Switcher
    st.markdown("<p style='font-size: 0.72rem; color: #94a3b8; font-weight: 700; text-transform: uppercase;'>⚡ Quick Persona Presets</p>", unsafe_allow_html=True)
    c_p1, c_p2 = st.columns(2)
    with c_p1:
        if st.button("🎓 Student (₹25k)", use_container_width=True):
            db = SessionLocal()
            p = db.query(FinancialProfile).first()
            p.full_name = "Rohan Verma (Student)"
            p.monthly_income = 25000.0
            p.current_savings = 35000.0
            p.essential_expenses = 14000.0
            p.discretionary_expenses = 5000.0
            p.existing_debt_emi = 0.0
            p.emergency_fund_target = 45000.0
            p.planned_purchase_name = "OnePlus Nord Smartphone"
            p.planned_purchase_amount = 28000.0
            db.commit()
            st.rerun()
    with c_p2:
        if st.button("💼 Techie (₹75k)", use_container_width=True):
            db = SessionLocal()
            p = db.query(FinancialProfile).first()
            p.full_name = "Alex Johnson (Techie)"
            p.monthly_income = 75000.0
            p.current_savings = 120000.0
            p.essential_expenses = 32000.0
            p.discretionary_expenses = 15000.0
            p.existing_debt_emi = 8000.0
            p.emergency_fund_target = 150000.0
            p.planned_purchase_name = "MacBook Pro / Performance Laptop"
            p.planned_purchase_amount = 70000.0
            db.commit()
            st.rerun()

    st.markdown("---")
    profile = get_user_profile()
    metrics = FinancialEngine.calculate_profile_metrics(
        monthly_income=profile.monthly_income,
        current_savings=profile.current_savings,
        essential_expenses=profile.essential_expenses,
        discretionary_expenses=profile.discretionary_expenses,
        existing_debt_emi=profile.existing_debt_emi,
        emergency_fund_target=profile.emergency_fund_target
    )

    st.markdown(f"""
    <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.06); border-radius: 10px; padding: 0.8rem; font-size: 0.8rem;">
        <div style="color: #94a3b8; font-size: 0.72rem; text-transform: uppercase;">Active Profile</div>
        <div style="color: #f8fafc; font-weight: 700; font-size: 0.95rem; margin-bottom: 0.35rem;">{profile.full_name}</div>
        <div style="display: flex; justify-content: space-between; margin-top: 0.25rem;">
            <span style="color: #94a3b8;">Income:</span>
            <span style="color: #f8fafc; font-weight: 600;">₹{profile.monthly_income:,.0f}</span>
        </div>
        <div style="display: flex; justify-content: space-between; margin-top: 0.25rem;">
            <span style="color: #94a3b8;">Liquid Reserve:</span>
            <span style="color: #10b981; font-weight: 600;">₹{profile.current_savings:,.0f}</span>
        </div>
        <div style="display: flex; justify-content: space-between; margin-top: 0.25rem;">
            <span style="color: #94a3b8;">Net Surplus:</span>
            <span style="color: {'#10b981' if metrics['free_cash_flow'] >= 0 else '#f43f5e'}; font-weight: 600;">₹{metrics['free_cash_flow']:,.0f}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 1.5rem; font-size: 0.72rem; color: #64748b; text-align: center;'>🛡️ Hack-o-Ween PESU &bull; Team Dark_Knights</div>", unsafe_allow_html=True)

# Top Bar with Status Indicators
st.markdown("""
<div class="top-banner">
    <div style="display: flex; align-items: center; gap: 10px;">
        <span style="background: #10b981; width: 8px; height: 8px; border-radius: 50%; box-shadow: 0 0 10px #10b981; display: inline-block;"></span>
        <span style="font-size: 0.85rem; font-weight: 600; color: #f8fafc;">Deterministic Financial Parallelverse Engine &bull; Dual-Mode Live</span>
    </div>
    <div style="display: flex; align-items: center; gap: 15px; font-size: 0.8rem; color: #94a3b8;">
        <span>Backend: <b style="color: #10b981;">FastAPI :8000</b></span>
        <span>Storage: <b style="color: #38bdf8;">SQLite 3</b></span>
        <span>Reminders: <b style="color: #fbbf24;">RFC 5545 iCal</b></span>
    </div>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# PAGE 1: OVERVIEW DASHBOARD
# ==============================================================================
if page == "📊 Executive Dashboard":
    st.markdown("<h1 class='gradient-header' style='font-size: 2.3rem; margin-bottom: 0.2rem;'>Executive Financial Overview</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94a3b8; font-size: 0.95rem; margin-bottom: 1.8rem;'>Real-time capital structure, baseline cash flow dynamics, and financial vulnerability analysis.</p>", unsafe_allow_html=True)

    # 4 Executive Metric Cards
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class="fin-card">
            <div class="stat-label">💵 Monthly Free Cash Flow</div>
            <div class="stat-value {'stat-negative' if metrics['free_cash_flow'] < 0 else 'stat-positive'}">
                ₹{metrics['free_cash_flow']:,.0f}
            </div>
            <div class="stat-footer stat-info">
                <span>Savings Rate: <b>{metrics['savings_rate_pct']:.1f}%</b></span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="fin-card">
            <div class="stat-label">🏦 Total Liquid Savings</div>
            <div class="stat-value">₹{profile.current_savings:,.0f}</div>
            <div class="stat-footer {'stat-positive' if metrics['emergency_coverage_pct'] >= 100 else 'stat-warning'}">
                <span>Target Coverage: <b>{metrics['emergency_coverage_pct']:.0f}%</b></span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="fin-card">
            <div class="stat-label">🛡️ Emergency Runway</div>
            <div class="stat-value">{metrics['months_of_runway']:.1f} <span style="font-size: 1.1rem; color: #94a3b8;">Months</span></div>
            <div class="stat-footer stat-info">
                <span>Survival without salary</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        dti_color = 'stat-negative' if metrics['debt_to_income_pct'] > 40 else ('stat-warning' if metrics['debt_to_income_pct'] > 25 else 'stat-positive')
        st.markdown(f"""
        <div class="fin-card">
            <div class="stat-label">⚖️ Debt-to-Income (DTI)</div>
            <div class="stat-value {dti_color}">{metrics['debt_to_income_pct']:.1f}%</div>
            <div class="stat-footer {'stat-positive' if metrics['debt_to_income_pct'] <= 25 else 'stat-warning'}">
                <span>Safe Threshold: &lt; 35%</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Inflow vs Outflows Visual Breakdown
    st.markdown("<br>", unsafe_allow_html=True)
    col_chart, col_decision = st.columns([1.6, 1.1])

    with col_chart:
        st.markdown("<h3 style='font-size: 1.15rem; color: #f8fafc; font-weight: 700; margin-bottom: 0.8rem;'>💳 Inflows vs Outflows Allocation</h3>", unsafe_allow_html=True)
        
        breakdown_df = pd.DataFrame([
            {"Category": "Essential Living (Rent, Food, Bills)", "Amount": profile.essential_expenses, "Color": "#3b82f6"},
            {"Category": "Discretionary (Dining, Leisure)", "Amount": profile.discretionary_expenses, "Color": "#a855f7"},
            {"Category": "Existing Loan Obligations (EMIs)", "Amount": profile.existing_debt_emi, "Color": "#f43f5e"},
            {"Category": "Net Monthly Surplus (Free Cash Flow)", "Amount": max(0.0, metrics["free_cash_flow"]), "Color": "#10b981"}
        ])

        fig_pie = go.Figure(data=[go.Pie(
            labels=breakdown_df["Category"],
            values=breakdown_df["Amount"],
            hole=0.62,
            marker=dict(colors=breakdown_df["Color"]),
            textinfo='percent',
            hoverinfo='label+value',
            hovertemplate="<b>%{label}</b><br>Amount: ₹%{value:,.0f} (%{percent})<extra></extra>"
        )])

        fig_pie.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#f8fafc", family="Plus Jakarta Sans"),
            margin=dict(t=10, b=10, l=10, r=10),
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.25,
                xanchor="center",
                x=0.5,
                font=dict(size=11)
            ),
            annotations=[
                dict(
                    text=f"<b>₹{profile.monthly_income:,.0f}</b><br><span style='font-size: 10px; color: #94a3b8;'>TOTAL INCOME</span>",
                    x=0.5, y=0.5, font_size=15, showarrow=False, font_family="Plus Jakarta Sans"
                )
            ]
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_decision:
        st.markdown("<h3 style='font-size: 1.15rem; color: #f8fafc; font-weight: 700; margin-bottom: 0.8rem;'>🎯 Contemplated Purchase Commitment</h3>", unsafe_allow_html=True)
        
        # Calculate impact of purchase
        cash_depletion_pct = (profile.planned_purchase_amount / max(1.0, profile.current_savings)) * 100.0
        
        st.markdown(f"""
        <div class="fin-card" style="border: 1px solid rgba(6, 182, 212, 0.35);">
            <div style="font-size: 0.75rem; color: #06b6d4; font-weight: 700; text-transform: uppercase;">Active Purchase Evaluation</div>
            <h2 style="margin: 0.4rem 0 0.2rem 0; font-size: 1.35rem; color: #f8fafc;">{profile.planned_purchase_name}</h2>
            <div style="font-size: 2.1rem; font-weight: 800; color: #06b6d4; margin-bottom: 0.8rem;">
                ₹{profile.planned_purchase_amount:,.0f}
            </div>
            
            <div style="border-top: 1px solid rgba(255,255,255,0.08); padding-top: 0.8rem; font-size: 0.82rem; color: #94a3b8;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.4rem;">
                    <span>Upfront Cash Impact:</span>
                    <span style="color: {'#f43f5e' if cash_depletion_pct > 60 else '#fbbf24'}; font-weight: 700;">
                        Consumes {cash_depletion_pct:.0f}% of liquid savings
                    </span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.4rem;">
                    <span>Remaining Emergency Buffer:</span>
                    <span style="color: {'#f43f5e' if (profile.current_savings - profile.planned_purchase_amount) < profile.emergency_fund_target else '#10b981'}; font-weight: 700;">
                        ₹{max(0.0, profile.current_savings - profile.planned_purchase_amount):,.0f}
                    </span>
                </div>
            </div>

            <div style="margin-top: 1.2rem;">
                <p style="font-size: 0.8rem; color: #cbd5e1; line-height: 1.4;">
                    ⚠️ Buying this upfront without simulation risks depleting your safety net if you experience an unexpected salary delay or medical emergency.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# PAGE 2: PARALLEL FUTURES SIMULATOR
# ==============================================================================
elif page == "🔮 Parallel Futures Simulator":
    st.markdown("<h1 class='gradient-header' style='font-size: 2.3rem; margin-bottom: 0.2rem;'>Parallel Financial Futures Engine</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94a3b8; font-size: 0.95rem; margin-bottom: 1.8rem;'>Deterministic multi-timeline scenario simulation. Detect cash shortfalls and breaking points before committing.</p>", unsafe_allow_html=True)

    # Interactive Simulator Controls
    with st.container():
        st.markdown("""
        <div style="background: rgba(19, 29, 49, 0.4); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 14px; padding: 1.2rem 1.4rem; margin-bottom: 1.5rem;">
            <div style="font-weight: 700; font-size: 0.85rem; color: #10b981; text-transform: uppercase; margin-bottom: 0.75rem;">
                ⚡ Simulation Control Panel & Adverse Shock Matrix
            </div>
        </div>
        """, unsafe_allow_html=True)

        sc_c1, sc_c2, sc_c3, sc_c4 = st.columns(4)
        with sc_c1:
            dur = st.slider("Simulation Horizon (Months)", min_value=6, max_value=24, value=12, step=1)
            purch_mode = st.selectbox("Purchase Payment Channel", ["EMI", "CASH", "NONE"], index=0)
        with sc_c2:
            purch_amt = st.number_input("Purchase Price (₹)", min_value=1000.0, value=float(profile.planned_purchase_amount), step=5000.0)
            down_pay = st.number_input("Down Payment (₹)", min_value=0.0, max_value=purch_amt-1000.0, value=min(10000.0, purch_amt*0.2), step=2000.0)
        with sc_c3:
            unexp_amt = st.number_input("Emergency Shock Expense (₹)", min_value=0.0, value=25000.0, step=5000.0)
            unexp_month = st.slider("Emergency Month Occurs", min_value=1, max_value=dur, value=3)
        with sc_c4:
            delay_start = st.slider("Salary Delay Month", min_value=1, max_value=dur, value=2)
            inflation_pct = st.slider("Cost of Living Inflation (%)", min_value=0, max_value=40, value=15, step=5)

    # Run Simulation Engine
    sim_results = ScenarioEngine.simulate_all_scenarios(
        duration_months=dur,
        monthly_income=profile.monthly_income,
        current_savings=profile.current_savings,
        essential_expenses=profile.essential_expenses,
        discretionary_expenses=profile.discretionary_expenses,
        existing_debt_emi=profile.existing_debt_emi,
        emergency_fund_target=profile.emergency_fund_target,
        purchase_name=profile.planned_purchase_name,
        purchase_amount=purch_amt,
        purchase_month=1,
        purchase_mode=purch_mode,
        emi_down_payment=down_pay,
        emi_interest_rate=12.0,
        emi_tenure_months=12,
        unexpected_expense_amount=unexp_amt,
        unexpected_expense_month=unexp_month,
        salary_delay_months=1,
        salary_delay_start_month=delay_start,
        expense_increase_pct=inflation_pct
    )

    scenarios = sim_results["scenarios"]

    # Breaking Point Status Notification
    has_critical = any(s["risk_level"] == "CRITICAL" for s in scenarios.values())
    has_high = any(s["risk_level"] == "HIGH" for s in scenarios.values())

    if has_critical:
        st.markdown(f"""
        <div class="alert-banner alert-danger">
            <span style="font-size: 1.5rem;">🚨</span>
            <div>
                <b style="font-size: 0.95rem;">Catastrophic Breaking Point Detected!</b>
                <p style="margin: 0.2rem 0 0 0; font-size: 0.85rem;">{sim_results['recommendation']}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    elif has_high:
        st.markdown(f"""
        <div class="alert-banner alert-warning">
            <span style="font-size: 1.5rem;">⚠️</span>
            <div>
                <b style="font-size: 0.95rem;">Emergency Cushion Breach Detected:</b>
                <p style="margin: 0.2rem 0 0 0; font-size: 0.85rem;">{sim_results['recommendation']}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="alert-banner alert-success">
            <span style="font-size: 1.5rem;">🛡️</span>
            <div>
                <b style="font-size: 0.95rem;">Resilient Across All 5 Parallel Futures:</b>
                <p style="margin: 0.2rem 0 0 0; font-size: 0.85rem;">{sim_results['recommendation']}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Master Plotly Interactive Line Chart with Gradient Shading
    st.markdown("<h3 style='font-size: 1.15rem; color: #f8fafc; font-weight: 700; margin-top: 1rem;'>📈 Projected Savings Trajectory Across 5 Parallel Futures</h3>", unsafe_allow_html=True)

    fig_lines = go.Figure()

    colors = {
        "baseline": "#10b981",          # Emerald
        "unexpected_expense": "#f59e0b",# Amber
        "delayed_salary": "#06b6d4",    # Electric Cyan
        "increased_spending": "#a855f7",# Violet
        "combined_adverse": "#f43f5e"   # Rose/Crimson
    }

    # Add Safe Zone Shading (Green) & Danger Zone Shading (Red)
    max_val = max(max(m["closing_savings"] for m in s["timeline"]) for s in scenarios.values())
    min_val = min(min(m["closing_savings"] for m in s["timeline"]) for s in scenarios.values())

    for sc_id, sc_data in scenarios.items():
        months = [f"M{m['month']}" for m in sc_data["timeline"]]
        savings_vals = [m["closing_savings"] for m in sc_data["timeline"]]
        
        is_hero = sc_id in ("baseline", "combined_adverse")
        fig_lines.add_trace(go.Scatter(
            x=months,
            y=savings_vals,
            mode="lines+markers",
            name=f"{sc_data['scenario_name']}",
            line=dict(
                color=colors.get(sc_id, "#ffffff"),
                width=3.5 if is_hero else 2,
                shape='spline'
            ),
            marker=dict(size=7 if is_hero else 5),
            hovertemplate="<b>" + sc_data['scenario_name'] + "</b><br>Month: %{x}<br>Savings Balance: ₹%{y:,.0f}<extra></extra>"
        ))

    # Add Emergency Target Line
    fig_lines.add_hline(
        y=profile.emergency_fund_target,
        line_dash="dash",
        line_color="#fbbf24",
        line_width=1.5,
        annotation_text=f"Emergency Reserve Target (₹{profile.emergency_fund_target:,.0f})",
        annotation_position="top right",
        annotation_font=dict(color="#fbbf24", size=11)
    )

    # Add Zero Line (Catastrophic Overdraft)
    fig_lines.add_hline(
        y=0,
        line_dash="solid",
        line_color="#f43f5e",
        line_width=2,
        annotation_text="⚠️ Zero Cash Deficit Threshold",
        annotation_position="bottom right",
        annotation_font=dict(color="#f43f5e", size=11)
    )

    fig_lines.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#0c1220",
        font=dict(color="#f8fafc", family="Plus Jakarta Sans"),
        xaxis=dict(title="<b>Timeline (Months)</b>", gridcolor="rgba(255,255,255,0.06)", zeroline=False),
        yaxis=dict(title="<b>Liquid Savings Balance (₹)</b>", gridcolor="rgba(255,255,255,0.06)", zeroline=False),
        margin=dict(l=20, r=20, t=30, b=20),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.32,
            xanchor="center",
            x=0.5,
            font=dict(size=11)
        ),
        hovermode="x unified"
    )

    st.plotly_chart(fig_lines, use_container_width=True)

    # 5 Parallel Futures Comparison Cards
    st.markdown("<h3 style='font-size: 1.15rem; color: #f8fafc; font-weight: 700; margin-top: 1.5rem;'>🌌 Future Timelines Breakdown & Resilience Index</h3>", unsafe_allow_html=True)
    card_cols = st.columns(5)
    
    for i, (sc_id, sc_data) in enumerate(scenarios.items()):
        with card_cols[i]:
            risk_class = "danger" if sc_data["risk_level"] in ("HIGH", "CRITICAL") else ("warning" if sc_data["risk_level"] == "MODERATE" else "success")
            st.markdown(f"""
            <div class="fin-card" style="min-height: 290px; padding: 1.1rem; border-top: 3px solid {colors[sc_id]};">
                <div style="font-weight: 700; font-size: 0.92rem; color: #f8fafc; margin-bottom: 0.35rem;">{sc_data['scenario_name']}</div>
                <span class="badge badge-{risk_class}">{sc_data['risk_level']} RISK</span>
                
                <div style="margin-top: 1rem;">
                    <div style="font-size: 0.72rem; color: #94a3b8; text-transform: uppercase;">Lowest Savings Point:</div>
                    <div style="font-size: 1.25rem; font-weight: 800; color: {'#f43f5e' if sc_data['lowest_savings'] < 0 else '#f8fafc'};">
                        ₹{sc_data['lowest_savings']:,.0f}
                    </div>
                </div>

                <div style="margin-top: 0.6rem; font-size: 0.78rem; color: #94a3b8;">
                    <div>Resilience Score: <b style="color: #f8fafc;">{sc_data['resilience_score']}/100</b></div>
                    <div>Deficit Months: <b style="color: {'#f43f5e' if sc_data['negative_cash_months'] > 0 else '#10b981'};">{sc_data['negative_cash_months']}</b></div>
                </div>

                <div style="margin-top: 0.8rem; font-size: 0.74rem; color: #cbd5e1; border-top: 1px solid rgba(255,255,255,0.08); padding-top: 0.6rem;">
                    {sc_data['breaking_point_reason']}
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Detailed Table View
    with st.expander("📋 View Month-by-Month Projection Data Table"):
        selected_sc = st.selectbox("Select Scenario Timeline to inspect", list(scenarios.keys()), format_func=lambda k: scenarios[k]["scenario_name"])
        df_timeline = pd.DataFrame(scenarios[selected_sc]["timeline"])
        st.dataframe(df_timeline.style.format({
            "opening_savings": "₹{:,.2f}",
            "income_received": "₹{:,.2f}",
            "essential_expenses": "₹{:,.2f}",
            "discretionary_expenses": "₹{:,.2f}",
            "existing_emi": "₹{:,.2f}",
            "purchase_payment": "₹{:,.2f}",
            "unexpected_expense": "₹{:,.2f}",
            "total_outflows": "₹{:,.2f}",
            "net_cash_flow": "₹{:,.2f}",
            "closing_savings": "₹{:,.2f}",
            "emergency_shortfall": "₹{:,.2f}"
        }), use_container_width=True)

# ==============================================================================
# PAGE 3: PURCHASE AFFORDABILITY PLANNER
# ==============================================================================
elif page == "⚖️ Purchase Affordability Matrix":
    st.markdown("<h1 class='gradient-header' style='font-size: 2.3rem; margin-bottom: 0.2rem;'>Purchase Affordability Decision Matrix</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94a3b8; font-size: 0.95rem; margin-bottom: 1.8rem;'>Comprehensive 4-way financial pathway comparison: Cash vs Save-and-Wait vs Alternative vs EMI Financing.</p>", unsafe_allow_html=True)

    with st.container():
        p_c1, p_c2, p_c3 = st.columns(3)
        with p_c1:
            p_name = st.text_input("Contemplated Item", value=profile.planned_purchase_name)
            p_cost = st.number_input("Target Price (₹)", min_value=1000.0, value=float(profile.planned_purchase_amount), step=5000.0)
        with p_c2:
            alt_name = st.text_input("Cheaper Alternative Model", value="Mid-Range Laptop")
            alt_cost = st.number_input("Alternative Price (₹)", min_value=500.0, value=42000.0, step=2000.0)
        with p_c3:
            wait_m = st.slider("Wait & Save Duration (Months)", min_value=1, max_value=12, value=4)
            emi_months = st.selectbox("EMI Tenure (Months)", [3, 6, 9, 12, 18, 24], index=3)

    eval_result = AffordabilityPlanner.evaluate_purchase(
        monthly_income=profile.monthly_income,
        current_savings=profile.current_savings,
        essential_expenses=profile.essential_expenses,
        discretionary_expenses=profile.discretionary_expenses,
        existing_debt_emi=profile.existing_debt_emi,
        emergency_fund_target=profile.emergency_fund_target,
        purchase_name=p_name,
        purchase_amount=p_cost,
        cheaper_alternative_name=alt_name,
        cheaper_alternative_amount=alt_cost,
        wait_months=wait_m,
        emi_down_payment=min(10000.0, p_cost * 0.2),
        emi_interest_rate=12.0,
        emi_tenure_months=emi_months
    )

    # Recommendation Callout Banner
    st.markdown(f"""
    <div class="fin-card" style="border: 2px solid #10b981; background: linear-gradient(135deg, rgba(16, 185, 129, 0.12) 0%, rgba(13, 20, 36, 0.85) 100%); margin-top: 1rem;">
        <div style="color: #10b981; font-weight: 800; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em;">
            ⭐ Parallelverse Algorithmic Recommendation: {eval_result['recommended_option_id'].replace('_', ' ').upper()}
        </div>
        <div style="font-size: 1.05rem; color: #f8fafc; font-weight: 600; margin-top: 0.4rem;">
            {eval_result['verdict_explanation']}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 4 Visual Option Cards
    cols = st.columns(4)
    for i, opt in enumerate(eval_result["options"]):
        with cols[i]:
            badge_color = "success" if opt["risk_rating"] == "SAFE" else ("warning" if opt["risk_rating"] == "CAUTION" else "danger")
            is_rec = opt["option_id"] == eval_result["recommended_option_id"]
            
            st.markdown(f"""
            <div class="fin-card" style="min-height: 440px; border: {2 if is_rec else 1}px solid {'#10b981' if is_rec else 'rgba(255,255,255,0.08)'};">
                {f'<div style="color: #10b981; font-weight: 800; font-size: 0.75rem; margin-bottom: 0.35rem;">★ BEST FIT CHOICE</div>' if is_rec else ''}
                <div style="font-weight: 700; font-size: 1.05rem; color: #f8fafc;">{opt['option_title']}</div>
                <div style="margin: 0.6rem 0;">
                    <span class="badge badge-{badge_color}">{opt['risk_rating']}</span>
                </div>
                
                <div style="margin-top: 1rem; border-top: 1px solid rgba(255,255,255,0.08); padding-top: 0.8rem;">
                    <div style="font-size: 0.75rem; color: #94a3b8; text-transform: uppercase;">Upfront Cash Required</div>
                    <div style="font-size: 1.25rem; font-weight: 800; color: #f8fafc;">₹{opt['upfront_cash_required']:,.0f}</div>
                </div>

                <div style="margin-top: 0.5rem;">
                    <div style="font-size: 0.75rem; color: #94a3b8; text-transform: uppercase;">Monthly Obligation</div>
                    <div style="font-size: 1.25rem; font-weight: 800; color: #06b6d4;">₹{opt['monthly_obligation']:,.0f}<span style="font-size: 0.75rem; color: #94a3b8;">/mo</span></div>
                </div>

                <div style="margin-top: 0.5rem;">
                    <div style="font-size: 0.75rem; color: #94a3b8; text-transform: uppercase;">Emergency Reserve Retained</div>
                    <div style="font-size: 1.1rem; font-weight: 700; color: {'#10b981' if opt['emergency_buffer_preserved_pct'] >= 100 else '#f59e0b'};">
                        {opt['emergency_buffer_preserved_pct']:.0f}% <span style="font-size: 0.75rem; color: #94a3b8;">of safety target</span>
                    </div>
                </div>

                <div style="margin-top: 1rem; font-size: 0.76rem; color: #cbd5e1; border-top: 1px solid rgba(255,255,255,0.08); padding-top: 0.6rem;">
                    <b>Key Trade-off:</b><br>{opt['key_tradeoff']}
                </div>
            </div>
            """, unsafe_allow_html=True)

# ==============================================================================
# PAGE 4: EMI CALCULATOR
# ==============================================================================
elif page == "🧮 Reducing-Balance EMI Engine":
    st.markdown("<h1 class='gradient-header' style='font-size: 2.3rem; margin-bottom: 0.2rem;'>Precision Reducing-Balance EMI Calculator</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94a3b8; font-size: 0.95rem; margin-bottom: 1.8rem;'>Financial grade reducing-balance amortization schedules, interest totals reconciliation, and early repayment analysis.</p>", unsafe_allow_html=True)

    col_e1, col_e2, col_e3, col_e4 = st.columns(4)
    with col_e1:
        price = st.number_input("Purchase Amount (₹)", min_value=1000.0, value=70000.0, step=5000.0)
    with col_e2:
        down = st.number_input("Down Payment (₹)", min_value=0.0, max_value=price-500.0, value=10000.0, step=2000.0)
    with col_e3:
        rate = st.number_input("Annual Interest Rate (%)", min_value=0.0, max_value=40.0, value=12.0, step=0.5)
    with col_e4:
        tenure = st.number_input("Loan Tenure (Months)", min_value=1, max_value=60, value=12, step=1)

    extra_pay = st.number_input("Optional Monthly Extra Prepayment (₹)", min_value=0.0, value=0.0, step=500.0)

    emi_data = EMICalculator.calculate_emi(
        purchase_price=price,
        down_payment=down,
        annual_interest_rate=rate,
        tenure_months=tenure,
        extra_monthly_payment=extra_pay
    )

    # 4 Financial Result Tiles
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""
        <div class="fin-card">
            <div class="stat-label">💳 Monthly EMI</div>
            <div class="stat-value" style="color: #10b981;">₹{emi_data['monthly_emi']:,.2f}</div>
            <div class="stat-footer stat-info">For {tenure} months</div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div class="fin-card">
            <div class="stat-label">🏷️ Principal Financed</div>
            <div class="stat-value">₹{emi_data['principal_financed']:,.0f}</div>
            <div class="stat-footer stat-info">Excluding down payment</div>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
        <div class="fin-card">
            <div class="stat-label">🔥 Total Interest Cost</div>
            <div class="stat-value {'stat-warning' if emi_data['total_interest'] > 0 else 'stat-positive'}">₹{emi_data['total_interest']:,.2f}</div>
            <div class="stat-footer stat-info">Financing surcharge</div>
        </div>
        """, unsafe_allow_html=True)
    with m4:
        st.markdown(f"""
        <div class="fin-card">
            <div class="stat-label">💰 Total Repayment</div>
            <div class="stat-value">₹{emi_data['total_repayment']:,.2f}</div>
            <div class="stat-footer stat-positive">Reconciled to ₹0.00 balance</div>
        </div>
        """, unsafe_allow_html=True)

    # Charts & Schedule Table
    c_pie, c_table = st.columns([1, 1.8])
    with c_pie:
        st.markdown("<h3 style='font-size: 1.15rem; color: #f8fafc; font-weight: 700; margin-bottom: 0.8rem;'>🥧 Principal vs Interest Distribution</h3>", unsafe_allow_html=True)
        pie_df = pd.DataFrame([
            {"Component": "Principal Loan", "Value": emi_data["principal_financed"], "Color": "#10b981"},
            {"Component": "Interest Cost", "Value": emi_data["total_interest"], "Color": "#f43f5e"}
        ])
        fig_emi_pie = px.pie(
            pie_df, values="Value", names="Component", hole=0.62,
            color="Component",
            color_discrete_map={"Principal Loan": "#10b981", "Interest Cost": "#f43f5e"}
        )
        fig_emi_pie.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#f8fafc", family="Plus Jakarta Sans"),
            margin=dict(t=10, b=10, l=10, r=10),
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig_emi_pie, use_container_width=True)

    with c_table:
        st.markdown("<h3 style='font-size: 1.15rem; color: #f8fafc; font-weight: 700; margin-bottom: 0.8rem;'>📜 Month-by-Month Amortization Schedule</h3>", unsafe_allow_html=True)
        df_sched = pd.DataFrame(emi_data["schedule"])
        st.dataframe(df_sched.style.format({
            "payment_amount": "₹{:,.2f}",
            "principal_paid": "₹{:,.2f}",
            "interest_paid": "₹{:,.2f}",
            "remaining_balance": "₹{:,.2f}",
            "cumulative_interest": "₹{:,.2f}"
        }), use_container_width=True, height=350)

# ==============================================================================
# PAGE 5: INSTALLMENT TRACKER & REMINDERS
# ==============================================================================
elif page == "📅 Installment Tracker & Reminders":
    st.markdown("<h1 class='gradient-header' style='font-size: 2.3rem; margin-bottom: 0.2rem;'>Installment Tracker & Calendar Reminders</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94a3b8; font-size: 0.95rem; margin-bottom: 1.8rem;'>Monitor active EMI commitments, update payment statuses, and download one-click <b>RFC 5545 iCalendar (.ics)</b> reminders for your phone.</p>", unsafe_allow_html=True)

    db = SessionLocal()
    try:
        plans = db.query(InstallmentPlan).all()

        with st.expander("➕ Create New Installment Commitment", expanded=False):
            with st.form("new_plan_form"):
                f1, f2, f3 = st.columns(3)
                with f1:
                    new_name = st.text_input("Item / Loan Description", value="Sony PlayStation 5 Pro")
                    new_cat = st.selectbox("Category", ["Electronics", "Vehicles", "Education", "Appliances", "Furniture", "Other"])
                with f2:
                    new_tot = st.number_input("Total Purchase Price (₹)", min_value=1000.0, value=65000.0, step=2000.0)
                    new_down = st.number_input("Down Payment (₹)", min_value=0.0, max_value=new_tot-500.0, value=15000.0, step=2000.0)
                with f3:
                    new_rate = st.number_input("Annual Interest (%)", min_value=0.0, value=12.0, step=0.5)
                    new_ten = st.number_input("Tenure (Months)", min_value=1, max_value=48, value=12, step=1)
                    new_due_d = st.slider("Monthly Payment Due Day", min_value=1, max_value=28, value=5)

                submitted = st.form_submit_button("Create & Generate Installment Schedule")
                if submitted:
                    calc, pays = ReminderService.generate_installment_schedule(
                        purchase_name=new_name,
                        total_amount=new_tot,
                        down_payment=new_down,
                        annual_interest_rate=new_rate,
                        tenure_months=new_ten,
                        start_date=date.today(),
                        due_day=new_due_d
                    )
                    created_plan = InstallmentPlan(
                        purchase_name=new_name,
                        category=new_cat,
                        total_amount=new_tot,
                        down_payment=new_down,
                        principal_financed=calc["principal_financed"],
                        annual_interest_rate=new_rate,
                        tenure_months=new_ten,
                        monthly_emi=calc["monthly_emi"],
                        total_repayment=calc["total_repayment"],
                        total_interest=calc["total_interest"],
                        start_date=date.today(),
                        due_day=new_due_d,
                        status="ACTIVE"
                    )
                    db.add(created_plan)
                    db.flush()

                    for p in pays:
                        db.add(InstallmentPayment(
                            installment_id=created_plan.id,
                            installment_number=p["installment_number"],
                            due_date=p["due_date"],
                            emi_amount=p["emi_amount"],
                            principal_portion=p["principal_portion"],
                            interest_portion=p["interest_portion"],
                            remaining_balance=p["remaining_balance"],
                            status=p["status"],
                            notes=p["notes"]
                        ))
                    db.commit()
                    st.success(f"Plan '{new_name}' created successfully with {new_ten} calendar installments!")
                    st.rerun()

        # Display Active Plans
        if not plans:
            st.info("No active plans found. Click 'Create New Installment Commitment' above or seed demo data.")
        else:
            for plan in plans:
                today = date.today()
                ReminderService.update_overdue_statuses(plan.payments, today)
                db.commit()

                paid_c = sum(1 for p in plan.payments if p.status == "PAID")
                total_c = len(plan.payments)
                progress_pct = (paid_c / total_c) * 100.0 if total_c > 0 else 0
                has_overdue = any(p.status == "OVERDUE" for p in plan.payments)

                st.markdown(f"""
                <div class="fin-card" style="border-left: 5px solid {'#f43f5e' if has_overdue else '#10b981'};">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <span class="badge badge-info">{plan.category}</span>
                            <span class="badge badge-{'danger' if has_overdue else 'success'}" style="margin-left: 6px;">
                                {'OVERDUE DETECTED' if has_overdue else 'ACTIVE & ON TRACK'}
                            </span>
                            <h3 style="margin: 0.5rem 0 0.2rem 0; color: #f8fafc; font-size: 1.3rem;">{plan.purchase_name}</h3>
                            <div style="color: #94a3b8; font-size: 0.85rem;">
                                Financed: <b>₹{plan.principal_financed:,.0f}</b> | 
                                Monthly EMI: <b style="color: #10b981;">₹{plan.monthly_emi:,.2f}</b> | 
                                Due Day: <b>{plan.due_day}th of every month</b>
                            </div>
                        </div>
                        <div style="text-align: right;">
                            <div style="font-size: 0.75rem; color: #94a3b8; text-transform: uppercase;">Repayment Progress</div>
                            <div style="font-size: 1.4rem; font-weight: 800; color: #10b981;">{paid_c} / {total_c} Paid</div>
                            <div style="font-size: 0.8rem; color: #94a3b8;">({progress_pct:.0f}% Completed)</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                st.progress(progress_pct / 100.0)

                b_col1, b_col2, _ = st.columns([1.5, 1, 2])
                with b_col1:
                    ics_content = ReminderService.generate_ics_calendar(plan.purchase_name, plan.payments)
                    st.download_button(
                        label="📅 Download Calendar (.ICS) Reminders",
                        data=ics_content,
                        file_name=f"{plan.purchase_name.replace(' ', '_')}_Reminders.ics",
                        mime="text/calendar",
                        key=f"ics_btn_{plan.id}"
                    )
                with b_col2:
                    if st.button("🗑️ Delete Commitment", key=f"del_plan_{plan.id}"):
                        db.delete(plan)
                        db.commit()
                        st.warning("Commitment deleted.")
                        st.rerun()

                with st.expander(f"👁️ View & Mark Monthly Payments ({plan.purchase_name})"):
                    for p in plan.payments:
                        p_c1, p_c2, p_c3, p_c4, p_c5 = st.columns([1, 1.5, 1.5, 1.5, 1.5])
                        with p_c1:
                            st.write(f"**Installment #{p.installment_number}**")
                        with p_c2:
                            st.write(f"Due: **{p.due_date.strftime('%d %b %Y')}**")
                        with p_c3:
                            st.write(f"Amount: **₹{p.emi_amount:,.2f}**")
                        with p_c4:
                            st.markdown(f"<span class='badge badge-{'success' if p.status == 'PAID' else ('danger' if p.status == 'OVERDUE' else 'warning')}'>{p.status}</span>", unsafe_allow_html=True)
                        with p_c5:
                            if p.status != "PAID":
                                if st.button("Mark Paid", key=f"pay_btn_{p.id}"):
                                    p.status = "PAID"
                                    p.paid_at = datetime.utcnow()
                                    db.commit()
                                    st.rerun()
                            else:
                                if st.button("Revert", key=f"rev_btn_{p.id}"):
                                    p.status = "PENDING"
                                    p.paid_at = None
                                    db.commit()
                                    st.rerun()

    finally:
        db.close()

# ==============================================================================
# PAGE 6: FINANCIAL PROFILE
# ==============================================================================
elif page == "👤 Financial Profile & Presets":
    st.markdown("<h1 class='gradient-header' style='font-size: 2.3rem; margin-bottom: 0.2rem;'>Financial Profile & Scenario Parameters</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94a3b8; font-size: 0.95rem; margin-bottom: 1.8rem;'>Configure your actual baseline finances or test custom financial scenarios. Persists automatically to SQLite.</p>", unsafe_allow_html=True)

    db = SessionLocal()
    try:
        prof = db.query(FinancialProfile).first()

        with st.form("edit_profile_form"):
            c_f1, c_f2 = st.columns(2)
            with c_f1:
                st.markdown("<h3 style='font-size: 1.15rem; color: #f8fafc; font-weight: 700; margin-bottom: 0.8rem;'>💼 Cash Reserves & Income</h3>", unsafe_allow_html=True)
                name_val = st.text_input("Full Name", value=prof.full_name)
                inc_val = st.number_input("Monthly Take-Home Income (₹)", min_value=0.0, value=float(prof.monthly_income), step=5000.0)
                sav_val = st.number_input("Current Liquid Savings (₹)", min_value=0.0, value=float(prof.current_savings), step=10000.0)
                emerg_val = st.number_input("Target Emergency Reserve (₹)", min_value=0.0, value=float(prof.emergency_fund_target), step=10000.0)

            with c_f2:
                st.markdown("<h3 style='font-size: 1.15rem; color: #f8fafc; font-weight: 700; margin-bottom: 0.8rem;'>🏠 Monthly Expenditures & Commitments</h3>", unsafe_allow_html=True)
                ess_val = st.number_input("Essential Expenses (Rent, Food, Healthcare) (₹)", min_value=0.0, value=float(prof.essential_expenses), step=2000.0)
                disc_val = st.number_input("Discretionary Expenses (Dining, Leisure) (₹)", min_value=0.0, value=float(prof.discretionary_expenses), step=2000.0)
                debt_val = st.number_input("Existing Monthly Loan / EMI Payments (₹)", min_value=0.0, value=float(prof.existing_debt_emi), step=1000.0)

            st.markdown("<h3 style='font-size: 1.15rem; color: #f8fafc; font-weight: 700; margin: 1rem 0 0.8rem 0;'>🛍️ Active Contemplated Purchase</h3>", unsafe_allow_html=True)
            cp1, cp2 = st.columns(2)
            with cp1:
                plan_name_val = st.text_input("Item Name", value=prof.planned_purchase_name)
            with cp2:
                plan_amt_val = st.number_input("Item Price (₹)", min_value=0.0, value=float(prof.planned_purchase_amount), step=5000.0)

            btn_save = st.form_submit_button("💾 Save Profile to Database")
            if btn_save:
                prof.full_name = name_val
                prof.monthly_income = inc_val
                prof.current_savings = sav_val
                prof.emergency_fund_target = emerg_val
                prof.essential_expenses = ess_val
                prof.discretionary_expenses = disc_val
                prof.existing_debt_emi = debt_val
                prof.planned_purchase_name = plan_name_val
                prof.planned_purchase_amount = plan_amt_val
                prof.updated_at = datetime.utcnow()
                db.commit()
                st.success("✅ Profile successfully updated and saved in SQLite database!")
                st.rerun()

    finally:
        db.close()
