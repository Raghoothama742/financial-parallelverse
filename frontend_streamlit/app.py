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
    page_title="Financial Parallelverse | FinTech Simulator",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Fintech CSS Design System
st.markdown("""
<style>
    /* Dark Theme Fintech Colors */
    :root {
        --bg-main: #0a0f1d;
        --card-bg: #131b2e;
        --card-border: #1e293b;
        --accent-emerald: #10b981;
        --accent-cyan: #06b6d4;
        --accent-amber: #f59e0b;
        --accent-rose: #ef4444;
        --text-primary: #f8fafc;
        --text-secondary: #94a3b8;
    }
    
    .stApp {
        background-color: #0b0f19;
        color: #f1f5f9;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    /* Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, #131d31 0%, #0f172a 100%);
        border: 1px solid #1e293b;
        border-radius: 12px;
        padding: 1.25rem 1.5rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.25);
        margin-bottom: 1rem;
    }
    .metric-title {
        color: #94a3b8;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.35rem;
    }
    .metric-value {
        color: #f8fafc;
        font-size: 1.85rem;
        font-weight: 700;
    }
    .metric-subtitle {
        font-size: 0.8rem;
        color: #10b981;
        margin-top: 0.25rem;
    }
    .metric-danger {
        color: #ef4444 !important;
    }
    .metric-warning {
        color: #f59e0b !important;
    }
    
    /* Scenario comparison box */
    .scenario-card {
        background-color: #131b2e;
        border-radius: 10px;
        border-left: 5px solid #10b981;
        padding: 1.2rem;
        margin-bottom: 1rem;
        border-top: 1px solid #1e293b;
        border-right: 1px solid #1e293b;
        border-bottom: 1px solid #1e293b;
    }
    .scenario-card.critical {
        border-left-color: #ef4444;
    }
    .scenario-card.warning {
        border-left-color: #f59e0b;
    }
    
    /* Tag pill badges */
    .badge {
        display: inline-block;
        padding: 0.25rem 0.65rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
    }
    .badge-success { background-color: rgba(16, 185, 129, 0.15); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.3); }
    .badge-warning { background-color: rgba(245, 158, 11, 0.15); color: #f59e0b; border: 1px solid rgba(245, 158, 11, 0.3); }
    .badge-danger { background-color: rgba(239, 68, 68, 0.15); color: #ef4444; border: 1px solid rgba(239, 68, 68, 0.3); }
    .badge-info { background-color: rgba(6, 182, 212, 0.15); color: #06b6d4; border: 1px solid rgba(6, 182, 212, 0.3); }

    /* Custom Streamlit adjustments */
    div[data-testid="stSidebar"] {
        background-color: #0d1322;
        border-right: 1px solid #1e293b;
    }
    .stButton>button {
        background-color: #10b981;
        color: #0a0f1d;
        font-weight: 600;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.2rem;
        transition: all 0.2s;
    }
    .stButton>button:hover {
        background-color: #059669;
        color: #ffffff;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# Helper functions for database access
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

# Sidebar Navigation
with st.sidebar:
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 20px;">
        <span style="font-size: 2rem;">🌌</span>
        <div>
            <h2 style="margin: 0; font-size: 1.25rem; font-weight: 700; color: #10b981;">Parallelverse</h2>
            <p style="margin: 0; font-size: 0.75rem; color: #94a3b8;">FinTech Future Simulator</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "Navigation",
        [
            "📊 Overview Dashboard",
            "🔮 Parallel Futures Simulator",
            "⚖️ Purchase Affordability Planner",
            "🧮 EMI Amortization Calculator",
            "📅 Installment Tracker & Reminders",
            "👤 Financial Profile"
        ],
        index=0
    )

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

    st.markdown(f"**User**: {profile.full_name}")
    st.markdown(f"**Monthly Income**: ₹{profile.monthly_income:,.0f}")
    st.markdown(f"**Liquid Savings**: ₹{profile.current_savings:,.0f}")
    st.markdown(f"**Monthly Net Flow**: ₹{metrics['free_cash_flow']:,.0f}")
    
    st.markdown("---")
    st.caption("🛡️ Track: The Vampire's Ledger | Dark_Knights")

# ==============================================================================
# PAGE 1: OVERVIEW DASHBOARD
# ==============================================================================
if page == "📊 Overview Dashboard":
    st.markdown("# 📊 Financial Health & Overview")
    st.markdown("Monitor your current baseline cash flow, emergency resilience runway, and active commitments before testing parallel futures.")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Monthly Free Cash Flow</div>
            <div class="metric-value {'metric-danger' if metrics['free_cash_flow'] < 0 else ''}">₹{metrics['free_cash_flow']:,.0f}</div>
            <div class="metric-subtitle">Net monthly surplus</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Current Liquid Savings</div>
            <div class="metric-value">₹{profile.current_savings:,.0f}</div>
            <div class="metric-subtitle">{metrics['emergency_coverage_pct']:.0f}% of Emergency Target</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Emergency Runway</div>
            <div class="metric-value">{metrics['months_of_runway']:.1f} Mo</div>
            <div class="metric-subtitle">Survival without income</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Debt-to-Income (DTI)</div>
            <div class="metric-value {'metric-warning' if metrics['debt_to_income_pct'] > 30 else ''}">{metrics['debt_to_income_pct']:.1f}%</div>
            <div class="metric-subtitle">Target: Under 35%</div>
        </div>
        """, unsafe_allow_html=True)

    # Cash Flow Breakdown Chart
    st.markdown("### 💳 Monthly Inflow vs Outflow Allocation")
    c_chart1, c_chart2 = st.columns([1.5, 1])

    with c_chart1:
        outflows_df = pd.DataFrame([
            {"Category": "Essential Expenses", "Amount": profile.essential_expenses},
            {"Category": "Discretionary Spending", "Amount": profile.discretionary_expenses},
            {"Category": "Existing Loan EMIs", "Amount": profile.existing_debt_emi},
            {"Category": "Surplus (Free Cash Flow)", "Amount": max(0.0, metrics["free_cash_flow"])}
        ])
        fig_donut = px.pie(
            outflows_df, 
            values="Amount", 
            names="Category",
            hole=0.6,
            color="Category",
            color_discrete_map={
                "Essential Expenses": "#3b82f6",
                "Discretionary Spending": "#a855f7",
                "Existing Loan EMIs": "#ef4444",
                "Surplus (Free Cash Flow)": "#10b981"
            }
        )
        fig_donut.update_layout(
            margin=dict(t=10, b=10, l=10, r=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#f8fafc"),
            legend=dict(orientation="h", yanchor="bottom", y=-0.2)
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    with c_chart2:
        st.markdown("#### 🎯 Active Planned Decision")
        st.markdown(f"""
        <div style="background-color: #131b2e; border: 1px solid #1e293b; border-radius: 10px; padding: 1.25rem;">
            <div style="font-size: 0.9rem; color: #94a3b8;">Contemplated Purchase:</div>
            <h3 style="margin-top: 0.2rem; color: #f8fafc;">{profile.planned_purchase_name}</h3>
            <div style="font-size: 1.5rem; font-weight: 700; color: #06b6d4;">₹{profile.planned_purchase_amount:,.0f}</div>
            <p style="font-size: 0.85rem; color: #94a3b8; margin-top: 0.5rem;">
                Evaluating whether this purchase will break your emergency runway during a salary delay or medical emergency.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 Enter Parallel Futures Simulator", use_container_width=True):
            st.session_state["nav_page"] = "🔮 Parallel Futures Simulator"
            st.rerun()

# ==============================================================================
# PAGE 2: PARALLEL FUTURES SIMULATOR
# ==============================================================================
elif page == "🔮 Parallel Futures Simulator":
    st.markdown("# 🔮 Parallel Financial Futures Engine")
    st.markdown("Stress test your financial resilience by simulating multiple concurrent futures under realistic adverse shocks.")

    # Control parameters
    with st.expander("⚙️ Configure Simulation Parameters & Shocks", expanded=True):
        sc_col1, sc_col2, sc_col3, sc_col4 = st.columns(4)
        with sc_col1:
            dur = st.slider("Simulation Horizon (Months)", min_value=6, max_value=24, value=12, step=1)
            purch_mode = st.selectbox("Purchase Mode", ["EMI", "CASH", "NONE"], index=0)
        with sc_col2:
            purch_amt = st.number_input("Purchase Price (₹)", min_value=1000.0, value=float(profile.planned_purchase_amount), step=5000.0)
            down_pay = st.number_input("Down Payment (₹)", min_value=0.0, max_value=purch_amt-1000.0, value=min(10000.0, purch_amt*0.2), step=2000.0)
        with sc_col3:
            unexp_amt = st.number_input("Emergency Shock Expense (₹)", min_value=0.0, value=25000.0, step=5000.0)
            unexp_month = st.slider("Emergency Month", min_value=1, max_value=dur, value=3)
        with sc_col4:
            delay_start = st.slider("Salary Delay Starts (Month)", min_value=1, max_value=dur, value=2)
            inflation_pct = st.slider("Cost Inflation (%)", min_value=0, max_value=40, value=15, step=5)

    # Execute simulation
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

    # Breaking point banners
    has_critical = any(s["risk_level"] == "CRITICAL" for s in scenarios.values())
    has_high = any(s["risk_level"] == "HIGH" for s in scenarios.values())
    
    if has_critical:
        st.error(f"🚨 **Critical Breaking Point Detected!** In the worst-case scenario, your liquid savings drop below zero. {sim_results['recommendation']}")
    elif has_high:
        st.warning(f"⚠️ **Emergency Reserve Warning:** In adverse scenarios, savings dip below your ₹{profile.emergency_fund_target:,.0f} safety reserve. {sim_results['recommendation']}")
    else:
        st.success(f"✅ **High Financial Resilience:** Across all 5 parallel futures, your cash reserves remain positive. {sim_results['recommendation']}")

    # Plotly Visualizations: Interactive Line Chart of Savings Over Time
    st.markdown("### 📈 Projected Savings Trajectory Across Parallel Futures")
    
    fig_lines = go.Figure()

    colors = {
        "baseline": "#10b981",
        "unexpected_expense": "#f59e0b",
        "delayed_salary": "#06b6d4",
        "increased_spending": "#a855f7",
        "combined_adverse": "#ef4444"
    }

    for sc_id, sc_data in scenarios.items():
        months = [f"M{m['month']}" for m in sc_data["timeline"]]
        savings_vals = [m["closing_savings"] for m in sc_data["timeline"]]
        fig_lines.add_trace(go.Scatter(
            x=months,
            y=savings_vals,
            mode="lines+markers",
            name=f"{sc_data['scenario_name']} (Score: {sc_data['resilience_score']})",
            line=dict(color=colors.get(sc_id, "#ffffff"), width=3 if sc_id in ("baseline", "combined_adverse") else 2),
            marker=dict(size=6)
        ))

    # Add Emergency Target Line
    fig_lines.add_hline(
        y=profile.emergency_fund_target,
        line_dash="dot",
        line_color="#e11d48",
        annotation_text=f"Emergency Fund Target (₹{profile.emergency_fund_target:,.0f})",
        annotation_position="bottom right"
    )

    # Add Zero Line
    fig_lines.add_hline(
        y=0,
        line_dash="solid",
        line_color="#475569",
        annotation_text="Zero Cash Deficit Line",
        annotation_position="bottom left"
    )

    fig_lines.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#0d1424",
        font=dict(color="#f8fafc"),
        xaxis=dict(title="Timeline (Months)", gridcolor="#1e293b"),
        yaxis=dict(title="Savings Balance (₹)", gridcolor="#1e293b"),
        margin=dict(l=20, r=20, t=30, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=-0.35)
    )

    st.plotly_chart(fig_lines, use_container_width=True)

    # Scenario Summary Cards
    st.markdown("### 🌌 Parallel Timelines Breakdown")
    card_cols = st.columns(len(scenarios))
    for i, (sc_id, sc_data) in enumerate(scenarios.items()):
        with card_cols[i]:
            risk_class = "danger" if sc_data["risk_level"] in ("HIGH", "CRITICAL") else ("warning" if sc_data["risk_level"] == "MODERATE" else "success")
            st.markdown(f"""
            <div class="scenario-card {'critical' if risk_class == 'danger' else ('warning' if risk_class == 'warning' else '')}">
                <div style="font-weight: 700; font-size: 0.95rem; margin-bottom: 0.25rem;">{sc_data['scenario_name']}</div>
                <span class="badge badge-{risk_class}">{sc_data['risk_level']} RISK</span>
                <div style="margin-top: 0.75rem;">
                    <div style="font-size: 0.75rem; color: #94a3b8;">Lowest Savings:</div>
                    <div style="font-size: 1.1rem; font-weight: 700; color: {'#ef4444' if sc_data['lowest_savings'] < 0 else '#f8fafc'};">₹{sc_data['lowest_savings']:,.0f}</div>
                </div>
                <div style="margin-top: 0.5rem; font-size: 0.8rem; color: #94a3b8;">
                    <strong>Resilience:</strong> {sc_data['resilience_score']}/100<br>
                    <strong>Deficit Months:</strong> {sc_data['negative_cash_months']}
                </div>
                <div style="margin-top: 0.5rem; font-size: 0.75rem; color: #cbd5e1; border-top: 1px solid #1e293b; padding-top: 0.5rem;">
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
elif page == "⚖️ Purchase Affordability Planner":
    st.markdown("# ⚖️ Purchase Affordability Decision Matrix")
    st.markdown("Compare 4 distinct execution paths for acquiring your target purchase without gambling your financial security.")

    with st.container():
        p_c1, p_c2, p_c3 = st.columns(3)
        with p_c1:
            p_name = st.text_input("Target Purchase", value=profile.planned_purchase_name)
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

    st.markdown("---")
    st.markdown(f"### 💡 Parallelverse Verdict: **{eval_result['recommended_option_id'].replace('_', ' ').upper()}**")
    st.info(f"**Recommendation Analysis:** {eval_result['verdict_explanation']}")

    # 4-Option Visual Comparison Cards
    cols = st.columns(4)
    for i, opt in enumerate(eval_result["options"]):
        with cols[i]:
            badge_color = "success" if opt["risk_rating"] == "SAFE" else ("warning" if opt["risk_rating"] == "CAUTION" else "danger")
            is_rec = opt["option_id"] == eval_result["recommended_option_id"]
            
            st.markdown(f"""
            <div style="background-color: #131b2e; border: {2 if is_rec else 1}px solid {'#10b981' if is_rec else '#1e293b'}; border-radius: 12px; padding: 1.25rem; min-height: 420px;">
                {f'<div style="color: #10b981; font-weight: 700; font-size: 0.8rem; margin-bottom: 0.25rem;">⭐ RECOMMENDED</div>' if is_rec else ''}
                <div style="font-weight: 700; font-size: 1.05rem; color: #f8fafc;">{opt['option_title']}</div>
                <div style="margin: 0.5rem 0;">
                    <span class="badge badge-{badge_color}">{opt['risk_rating']}</span>
                </div>
                <div style="margin-top: 1rem; border-top: 1px solid #1e293b; padding-top: 0.75rem;">
                    <div style="font-size: 0.8rem; color: #94a3b8;">Upfront Cash Required:</div>
                    <div style="font-size: 1.15rem; font-weight: 700; color: #f8fafc;">₹{opt['upfront_cash_required']:,.0f}</div>
                </div>
                <div style="margin-top: 0.5rem;">
                    <div style="font-size: 0.8rem; color: #94a3b8;">Monthly Obligation:</div>
                    <div style="font-size: 1.15rem; font-weight: 700; color: #06b6d4;">₹{opt['monthly_obligation']:,.0f}/mo</div>
                </div>
                <div style="margin-top: 0.5rem;">
                    <div style="font-size: 0.8rem; color: #94a3b8;">Liquid Reserve Preserved:</div>
                    <div style="font-size: 1.05rem; font-weight: 600; color: {'#10b981' if opt['emergency_buffer_preserved_pct'] >= 100 else '#f59e0b'};">
                        {opt['emergency_buffer_preserved_pct']:.0f}% of target
                    </div>
                </div>
                <div style="margin-top: 1rem; font-size: 0.8rem; color: #94a3b8; border-top: 1px solid #1e293b; padding-top: 0.5rem;">
                    <strong>Trade-off:</strong> {opt['key_tradeoff']}
                </div>
            </div>
            """, unsafe_allow_html=True)

# ==============================================================================
# PAGE 4: EMI & AMORTIZATION CALCULATOR
# ==============================================================================
elif page == "🧮 EMI Amortization Calculator":
    st.markdown("# 🧮 Standard Reducing-Balance EMI Calculator")
    st.markdown("Precision loan amortization with zero-interest support, interest total reconciliation, and prepayment simulations.")

    col_e1, col_e2, col_e3, col_e4 = st.columns(4)
    with col_e1:
        price = st.number_input("Purchase Amount (₹)", min_value=1000.0, value=70000.0, step=5000.0)
    with col_e2:
        down = st.number_input("Down Payment (₹)", min_value=0.0, max_value=price-500.0, value=10000.0, step=2000.0)
    with col_e3:
        rate = st.number_input("Annual Interest Rate (%)", min_value=0.0, max_value=40.0, value=12.0, step=0.5)
    with col_e4:
        tenure = st.number_input("Loan Tenure (Months)", min_value=1, max_value=60, value=12, step=1)

    extra_pay = st.number_input("Optional Extra Prepayment per Month (₹)", min_value=0.0, value=0.0, step=500.0)

    emi_data = EMICalculator.calculate_emi(
        purchase_price=price,
        down_payment=down,
        annual_interest_rate=rate,
        tenure_months=tenure,
        extra_monthly_payment=extra_pay
    )

    # Top Metric Tiles
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Monthly EMI</div>
            <div class="metric-value">₹{emi_data['monthly_emi']:,.2f}</div>
            <div class="metric-subtitle">For {tenure} months</div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Principal Financed</div>
            <div class="metric-value">₹{emi_data['principal_financed']:,.0f}</div>
            <div class="metric-subtitle">Net loan amount</div>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Total Interest</div>
            <div class="metric-value {'metric-warning' if emi_data['total_interest'] > 0 else ''}">₹{emi_data['total_interest']:,.2f}</div>
            <div class="metric-subtitle">Finance cost</div>
        </div>
        """, unsafe_allow_html=True)
    with m4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Total Repayment</div>
            <div class="metric-value">₹{emi_data['total_repayment']:,.2f}</div>
            <div class="metric-subtitle">Principal + Interest</div>
        </div>
        """, unsafe_allow_html=True)

    # Chart & Table
    ch_col, tab_col = st.columns([1, 1.8])
    with ch_col:
        st.markdown("### 🥧 Principal vs Interest Ratio")
        pie_df = pd.DataFrame([
            {"Part": "Principal", "Value": emi_data["principal_financed"]},
            {"Part": "Total Interest", "Value": emi_data["total_interest"]}
        ])
        fig_emi_pie = px.pie(
            pie_df, 
            values="Value", 
            names="Part", 
            hole=0.6,
            color="Part",
            color_discrete_map={"Principal": "#10b981", "Total Interest": "#ef4444"}
        )
        fig_emi_pie.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#f8fafc"),
            margin=dict(t=10, b=10, l=10, r=10)
        )
        st.plotly_chart(fig_emi_pie, use_container_width=True)

    with tab_col:
        st.markdown("### 📜 Amortization Schedule")
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
    st.markdown("# 📅 Installment Tracker & Calendar Reminders")
    st.markdown("Track active EMIs, mark payments as paid, detect overdue bills, and export one-click **iCalendar (.ics)** reminders for your phone.")

    db = SessionLocal()
    try:
        plans = db.query(InstallmentPlan).all()

        # Add New Plan Expander
        with st.expander("➕ Create New Installment Plan"):
            with st.form("new_plan_form"):
                f1, f2, f3 = st.columns(3)
                with f1:
                    new_name = st.text_input("Purchase / Loan Name", value="OnePlus 12 Smartphone")
                    new_cat = st.selectbox("Category", ["Electronics", "Appliances", "Vehicles", "Education", "Personal", "Other"])
                with f2:
                    new_tot = st.number_input("Total Amount (₹)", min_value=1000.0, value=65000.0, step=2000.0)
                    new_down = st.number_input("Down Payment (₹)", min_value=0.0, max_value=new_tot-500.0, value=15000.0, step=2000.0)
                with f3:
                    new_rate = st.number_input("Annual Interest (%)", min_value=0.0, value=12.0, step=0.5)
                    new_ten = st.number_input("Tenure (Months)", min_value=1, max_value=48, value=12, step=1)
                    new_due_d = st.slider("Due Day of Month", min_value=1, max_value=28, value=5)
                
                submitted = st.form_submit_button("Create Installment Plan")
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
                    st.success(f"Plan '{new_name}' created successfully!")
                    st.rerun()

        # Display Existing Plans
        if not plans:
            st.info("No installment plans found. Click 'Create New Installment Plan' above or run demo seeding.")
        else:
            for plan in plans:
                today = date.today()
                ReminderService.update_overdue_statuses(plan.payments, today)
                db.commit()

                paid_c = sum(1 for p in plan.payments if p.status == "PAID")
                total_c = len(plan.payments)
                progress_pct = (paid_c / total_c) * 100.0 if total_c > 0 else 0
                has_overdue = any(p.status == "OVERDUE" for p in plan.payments)

                with st.container():
                    st.markdown(f"""
                    <div style="background-color: #131b2e; border: 1px solid {'#ef4444' if has_overdue else '#1e293b'}; border-radius: 12px; padding: 1.5rem; margin-bottom: 1.5rem;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <span class="badge badge-info">{plan.category}</span>
                                <span class="badge badge-{'danger' if has_overdue else 'success'}" style="margin-left: 8px;">
                                    {'OVERDUE DETECTED' if has_overdue else 'ON TRACK'}
                                </span>
                                <h3 style="margin: 0.5rem 0 0.2rem 0; color: #f8fafc;">{plan.purchase_name}</h3>
                                <p style="color: #94a3b8; font-size: 0.85rem; margin: 0;">Total Financed: ₹{plan.principal_financed:,.0f} | EMI: ₹{plan.monthly_emi:,.2f}/mo | Due Day: {plan.due_day}th</p>
                            </div>
                            <div style="text-align: right;">
                                <div style="font-size: 0.85rem; color: #94a3b8;">Repayment Progress</div>
                                <div style="font-size: 1.25rem; font-weight: 700; color: #10b981;">{paid_c} / {total_c} Paid ({progress_pct:.0f}%)</div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    st.progress(progress_pct / 100.0)

                    # Action buttons: Download .ics calendar and delete plan
                    col_btn1, col_btn2, col_spacer = st.columns([1.5, 1, 3])
                    with col_btn1:
                        # Calendar .ics export
                        ics_content = ReminderService.generate_ics_calendar(plan.purchase_name, plan.payments)
                        st.download_button(
                            label="📅 Download Calendar (.ICS) Reminders",
                            data=ics_content,
                            file_name=f"{plan.purchase_name.replace(' ', '_')}_Reminders.ics",
                            mime="text/calendar",
                            key=f"ics_{plan.id}"
                        )
                    with col_btn2:
                        if st.button(f"🗑️ Delete Plan", key=f"del_{plan.id}"):
                            db.delete(plan)
                            db.commit()
                            st.warning(f"Plan deleted.")
                            st.rerun()

                    # Month-by-month payment items
                    with st.expander(f"👁️ View & Update Installment Schedule ({plan.purchase_name})"):
                        for p in plan.payments:
                            p_col1, p_col2, p_col3, p_col4, p_col5 = st.columns([1, 1.5, 1.5, 1.5, 1.5])
                            with p_col1:
                                st.write(f"**#{p.installment_number}**")
                            with p_col2:
                                st.write(f"Due: **{p.due_date.strftime('%d %b %Y')}**")
                            with p_col3:
                                st.write(f"Amount: **₹{p.emi_amount:,.2f}**")
                            with p_col4:
                                st.markdown(f"<span class='badge badge-{'success' if p.status == 'PAID' else ('danger' if p.status == 'OVERDUE' else 'warning')}'>{p.status}</span>", unsafe_allow_html=True)
                            with p_col5:
                                if p.status != "PAID":
                                    if st.button("Mark Paid", key=f"pay_{p.id}"):
                                        p.status = "PAID"
                                        p.paid_at = datetime.utcnow()
                                        db.commit()
                                        st.rerun()
                                else:
                                    if st.button("Revert", key=f"rev_{p.id}"):
                                        p.status = "PENDING"
                                        p.paid_at = None
                                        db.commit()
                                        st.rerun()
    finally:
        db.close()

# ==============================================================================
# PAGE 6: FINANCIAL PROFILE
# ==============================================================================
elif page == "👤 Financial Profile":
    st.markdown("# 👤 Financial Profile Settings")
    st.markdown("Update your real or hypothetical baseline financial situation. All changes persist automatically to the SQLite database.")

    db = SessionLocal()
    try:
        prof = db.query(FinancialProfile).first()

        with st.form("profile_form"):
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                st.markdown("### 💼 Income & Cash Reserves")
                name_in = st.text_input("Full Name", value=prof.full_name)
                inc_in = st.number_input("Monthly Take-Home Income (₹)", min_value=0.0, value=float(prof.monthly_income), step=5000.0)
                sav_in = st.number_input("Current Liquid Savings (₹)", min_value=0.0, value=float(prof.current_savings), step=10000.0)
                emerg_in = st.number_input("Emergency Reserve Target (₹)", min_value=0.0, value=float(prof.emergency_fund_target), step=10000.0)

            with col_f2:
                st.markdown("### 🏠 Monthly Outflows & Debts")
                ess_in = st.number_input("Essential Expenses (Rent, Food, Utilities) (₹)", min_value=0.0, value=float(prof.essential_expenses), step=2000.0)
                disc_in = st.number_input("Discretionary Expenses (Dining, Leisure) (₹)", min_value=0.0, value=float(prof.discretionary_expenses), step=2000.0)
                debt_in = st.number_input("Existing Monthly Debt / EMI Commitments (₹)", min_value=0.0, value=float(prof.existing_debt_emi), step=1000.0)
                
            st.markdown("### 🛍️ Contemplated Target Purchase")
            c_p1, c_p2 = st.columns(2)
            with c_p1:
                plan_name_in = st.text_input("Planned Purchase Name", value=prof.planned_purchase_name)
            with c_p2:
                plan_amt_in = st.number_input("Planned Purchase Cost (₹)", min_value=0.0, value=float(prof.planned_purchase_amount), step=5000.0)

            saved = st.form_submit_button("💾 Save Profile Changes")
            if saved:
                prof.full_name = name_in
                prof.monthly_income = inc_in
                prof.current_savings = sav_in
                prof.emergency_fund_target = emerg_in
                prof.essential_expenses = ess_in
                prof.discretionary_expenses = disc_in
                prof.existing_debt_emi = debt_in
                prof.planned_purchase_name = plan_name_in
                prof.planned_purchase_amount = plan_amt_in
                prof.updated_at = datetime.utcnow()
                db.commit()
                st.success("✅ Profile updated successfully in SQLite database!")
                st.rerun()

    finally:
        db.close()
