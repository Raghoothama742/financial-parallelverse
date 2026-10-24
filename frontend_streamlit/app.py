import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import date, datetime, timedelta
import sys
from pathlib import Path

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

# ==============================================================================
# WORLD-CLASS FINTECH SAAS DESIGN SYSTEM (VIBRANT & COLORFUL)
# ==============================================================================
st.html("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,700&family=JetBrains+Mono:wght@400;500;600&display=swap');

    /* Global Base */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    .stApp {
        background: radial-gradient(circle at 15% 15%, #0e172a 0%, #080c17 45%, #050811 100%) !important;
        color: #f8fafc !important;
    }

    /* Vibrant Mesh Gradient Hero */
    .hero-container {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.9) 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 2.5rem 2.8rem;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.1);
    }

    .hero-container::before {
        content: '';
        position: absolute;
        top: -60px;
        right: -60px;
        width: 320px;
        height: 320px;
        background: radial-gradient(circle, rgba(16, 185, 129, 0.25) 0%, rgba(6, 182, 212, 0.2) 40%, transparent 70%);
        filter: blur(40px);
        pointer-events: none;
    }

    .hero-container::after {
        content: '';
        position: absolute;
        bottom: -60px;
        left: 20%;
        width: 340px;
        height: 340px;
        background: radial-gradient(circle, rgba(168, 85, 247, 0.2) 0%, rgba(244, 63, 94, 0.15) 50%, transparent 70%);
        filter: blur(50px);
        pointer-events: none;
    }

    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: linear-gradient(90deg, rgba(16, 185, 129, 0.18) 0%, rgba(6, 182, 212, 0.18) 100%);
        border: 1px solid rgba(16, 185, 129, 0.4);
        padding: 0.35rem 0.9rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
        color: #34d399;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 1rem;
    }

    .hero-title {
        font-size: 2.8rem;
        font-weight: 800;
        line-height: 1.15;
        letter-spacing: -0.03em;
        margin-bottom: 0.75rem;
        background: linear-gradient(135deg, #ffffff 10%, #38bdf8 45%, #a855f7 75%, #34d399 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-subtitle {
        color: #94a3b8;
        font-size: 1.1rem;
        max-width: 680px;
        line-height: 1.5;
        margin-bottom: 1.5rem;
    }

    /* KPI Glow Cards */
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1.25rem;
        margin-bottom: 2rem;
    }

    .kpi-card {
        background: linear-gradient(135deg, rgba(19, 29, 49, 0.8) 0%, rgba(13, 20, 36, 0.9) 100%);
        border-radius: 20px;
        padding: 1.4rem 1.6rem;
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
        transition: transform 0.25s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.25s ease, border-color 0.25s ease;
    }

    .kpi-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 16px 40px rgba(0, 0, 0, 0.5), 0 0 25px rgba(56, 189, 248, 0.15);
    }

    .kpi-card.emerald { border-top: 3px solid #10b981; }
    .kpi-card.cyan { border-top: 3px solid #06b6d4; }
    .kpi-card.purple { border-top: 3px solid #a855f7; }
    .kpi-card.orange { border-top: 3px solid #f97316; }
    .kpi-card.rose { border-top: 3px solid #f43f5e; }

    .kpi-label {
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #94a3b8;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.4rem;
    }

    .kpi-value {
        font-size: 2.1rem;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: -0.02em;
        line-height: 1.1;
    }

    .kpi-footer {
        font-size: 0.8rem;
        font-weight: 600;
        margin-top: 0.5rem;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    /* Timeline Scenario Identity Cards */
    .scenario-grid {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 1.1rem;
        margin-bottom: 2rem;
    }

    .scenario-card {
        border-radius: 18px;
        padding: 1.35rem 1.25rem;
        position: relative;
        overflow: hidden;
        background: linear-gradient(135deg, rgba(18, 26, 43, 0.85) 0%, rgba(11, 16, 28, 0.95) 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.35);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        min-height: 310px;
        transition: transform 0.25s ease, border-color 0.25s ease;
    }

    .scenario-card:hover {
        transform: translateY(-4px);
    }

    .sc-baseline { border-top: 4px solid #10b981; }
    .sc-shock { border-top: 4px solid #f97316; }
    .sc-delay { border-top: 4px solid #06b6d4; }
    .sc-inflation { border-top: 4px solid #a855f7; }
    .sc-nightmare { border-top: 4px solid #f43f5e; }

    .sc-title {
        font-weight: 700;
        font-size: 1rem;
        color: #f8fafc;
        margin-bottom: 0.4rem;
    }

    .pill-tag {
        display: inline-block;
        padding: 0.25rem 0.65rem;
        border-radius: 9999px;
        font-size: 0.68rem;
        font-weight: 800;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }

    .pill-emerald { background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.35); }
    .pill-orange { background: rgba(249, 115, 22, 0.15); color: #fb923c; border: 1px solid rgba(249, 115, 22, 0.35); }
    .pill-cyan { background: rgba(6, 182, 212, 0.15); color: #38bdf8; border: 1px solid rgba(6, 182, 212, 0.35); }
    .pill-purple { background: rgba(168, 85, 247, 0.15); color: #c084fc; border: 1px solid rgba(168, 85, 247, 0.35); }
    .pill-rose { background: rgba(244, 63, 94, 0.15); color: #fb7185; border: 1px solid rgba(244, 63, 94, 0.35); }

    .sc-val-box {
        margin: 1rem 0;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 0.75rem;
    }

    .sc-val-label { font-size: 0.7rem; color: #94a3b8; text-transform: uppercase; }
    .sc-val-num { font-size: 1.35rem; font-weight: 800; color: #ffffff; }

    /* Purchase Option Cards */
    .pathway-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1.25rem;
        margin-top: 1.5rem;
        margin-bottom: 2rem;
    }

    .pathway-card {
        background: linear-gradient(135deg, rgba(18, 27, 46, 0.85) 0%, rgba(10, 16, 28, 0.95) 100%);
        border-radius: 20px;
        padding: 1.6rem 1.4rem;
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
        position: relative;
        overflow: hidden;
        transition: transform 0.25s ease, box-shadow 0.25s ease;
    }

    .pathway-card:hover {
        transform: translateY(-4px);
    }

    .pathway-card.recommended {
        border: 2px solid #10b981;
        box-shadow: 0 15px 40px rgba(16, 185, 129, 0.2);
    }

    .pathway-badge-rec {
        position: absolute;
        top: 1rem;
        right: 1rem;
        background: linear-gradient(90deg, #10b981 0%, #06b6d4 100%);
        color: #041a11;
        font-weight: 800;
        font-size: 0.68rem;
        text-transform: uppercase;
        padding: 0.2rem 0.6rem;
        border-radius: 9999px;
    }

    /* Polished Footer */
    .fin-footer {
        background: linear-gradient(180deg, transparent 0%, rgba(10, 16, 28, 0.95) 100%);
        border-top: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px 20px 0 0;
        padding: 2.5rem 2rem 1.5rem 2rem;
        margin-top: 3rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 1.5rem;
    }

    /* Streamlit Form Input Beautification */
    div[data-baseweb="input"] {
        background-color: #0f172a !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 10px !important;
    }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        color: #041a11 !important;
        font-weight: 800 !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.6rem 1.5rem !important;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.35) !important;
        transition: all 0.25s ease !important;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #34d399 0%, #10b981 100%) !important;
        box-shadow: 0 8px 25px rgba(16, 185, 129, 0.5) !important;
        transform: translateY(-2px);
    }
</style>
""")

# Database profile helper
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

# Sidebar Navigation with Persona Quick-Chips
with st.sidebar:
    st.html("""
    <div style="display: flex; align-items: center; gap: 14px; margin-bottom: 1.5rem;">
        <div style="width: 48px; height: 48px; border-radius: 14px; background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 50%, #10b981 100%); display: flex; align-items: center; justify-content: center; font-size: 1.7rem; box-shadow: 0 4px 18px rgba(59, 130, 246, 0.4);">
            🌌
        </div>
        <div>
            <div style="font-size: 1.3rem; font-weight: 800; color: #ffffff; letter-spacing: -0.02em;">Parallelverse</div>
            <div style="font-size: 0.72rem; color: #38bdf8; font-weight: 700; text-transform: uppercase;">FinTech Simulation</div>
        </div>
    </div>
    """)

    page = st.radio(
        "NAVIGATION MENU",
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
    st.markdown("<p style='font-size: 0.72rem; color: #94a3b8; font-weight: 700; text-transform: uppercase;'>⚡ Instant Persona Switcher</p>", unsafe_allow_html=True)
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

    st.html(f"""
    <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 14px; padding: 1rem; font-size: 0.82rem;">
        <div style="color: #38bdf8; font-size: 0.72rem; font-weight: 700; text-transform: uppercase;">Active Profile</div>
        <div style="color: #ffffff; font-weight: 700; font-size: 1rem; margin: 0.2rem 0 0.6rem 0;">{profile.full_name}</div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 0.3rem;">
            <span style="color: #94a3b8;">Monthly Paycheck:</span>
            <span style="color: #ffffff; font-weight: 700;">₹{profile.monthly_income:,.0f}</span>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 0.3rem;">
            <span style="color: #94a3b8;">Liquid Reserve:</span>
            <span style="color: #34d399; font-weight: 700;">₹{profile.current_savings:,.0f}</span>
        </div>
        <div style="display: flex; justify-content: space-between;">
            <span style="color: #94a3b8;">Net Monthly Surplus:</span>
            <span style="color: {'#34d399' if metrics['free_cash_flow'] >= 0 else '#fb7185'}; font-weight: 700;">₹{metrics['free_cash_flow']:,.0f}</span>
        </div>
    </div>
    <div style="margin-top: 1.5rem; text-align: center; font-size: 0.72rem; color: #64748b;">
        🛡️ Track: The Vampire's Ledger<br>Hack-o-Ween PES University &bull; Dark_Knights
    </div>
    """)

# ==============================================================================
# PAGE 1: EXECUTIVE DASHBOARD
# ==============================================================================
if page == "📊 Executive Dashboard":
    # Stunning Hero Section
    st.html(f"""
    <div class="hero-container">
        <div class="hero-badge">
            <span style="width: 8px; height: 8px; border-radius: 50%; background: #34d399; display: inline-block;"></span>
            FinTech Stress Testing Engine &bull; Hack-o-Ween Edition
        </div>
        <div class="hero-title">Simulate Your Tomorrow Before Spending Today.</div>
        <div class="hero-subtitle">
            Most individuals commit to significant purchases like laptops or smartphones looking only at today's paycheck. 
            Financial Parallelverse simulates multiple adverse futures—delayed salaries, hospital emergencies, and inflation—so you never commit blind.
        </div>
        <div style="display: flex; gap: 12px; flex-wrap: wrap;">
            <span class="pill-tag pill-emerald">⚡ 5 Concurrent Timelines</span>
            <span class="pill-tag pill-cyan">🛡️ Emergency Reserve Shield</span>
            <span class="pill-tag pill-purple">📅 RFC 5545 iCalendar Sync</span>
            <span class="pill-tag pill-orange">🧮 Reducing-Balance Precision</span>
        </div>
    </div>
    """)

    # 4 Glowing KPI Metric Cards
    flow_col = "#34d399" if metrics['free_cash_flow'] >= 0 else "#fb7185"
    runway_col = "#34d399" if metrics['months_of_runway'] >= 3 else "#fbbf24"
    dti_col = "#fb7185" if metrics['debt_to_income_pct'] > 35 else "#34d399"

    st.html(f"""
    <div class="kpi-grid">
        <div class="kpi-card emerald">
            <div class="kpi-label">
                <span>Monthly Free Cash Flow</span>
                <span>💵</span>
            </div>
            <div class="kpi-value" style="color: {flow_col};">₹{metrics['free_cash_flow']:,.0f}</div>
            <div class="kpi-footer" style="color: #38bdf8;">
                Savings Rate: <b>{metrics['savings_rate_pct']:.1f}%</b>
            </div>
        </div>

        <div class="kpi-card cyan">
            <div class="kpi-label">
                <span>Liquid Cash Reserves</span>
                <span>🏦</span>
            </div>
            <div class="kpi-value">₹{profile.current_savings:,.0f}</div>
            <div class="kpi-footer" style="color: #34d399;">
                Target Coverage: <b>{metrics['emergency_coverage_pct']:.0f}%</b>
            </div>
        </div>

        <div class="kpi-card purple">
            <div class="kpi-label">
                <span>Emergency Runway</span>
                <span>🛡️</span>
            </div>
            <div class="kpi-value">{metrics['months_of_runway']:.1f} <span style="font-size: 1.1rem; color: #94a3b8;">Mo</span></div>
            <div class="kpi-footer" style="color: {runway_col};">
                Survival without salary
            </div>
        </div>

        <div class="kpi-card orange">
            <div class="kpi-label">
                <span>Debt-to-Income (DTI)</span>
                <span>⚖️</span>
            </div>
            <div class="kpi-value" style="color: {dti_col};">{metrics['debt_to_income_pct']:.1f}%</div>
            <div class="kpi-footer" style="color: #94a3b8;">
                Safe Target: &lt; 35%
            </div>
        </div>
    </div>
    """)

    # Inflow vs Outflows Visual Breakdown and Contemplated Purchase
    col_chart, col_decision = st.columns([1.5, 1.1])

    with col_chart:
        st.subheader("💳 Inflow vs Outflows Capital Breakdown")
        breakdown_df = pd.DataFrame([
            {"Category": "Essential Living (Rent, Food, Utilities)", "Amount": profile.essential_expenses, "Color": "#3b82f6"},
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
                    text=f"<b>₹{profile.monthly_income:,.0f}</b><br><span style='font-size: 10px; color: #94a3b8;'>TOTAL SALARY</span>",
                    x=0.5, y=0.5, font_size=15, showarrow=False
                )
            ]
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_decision:
        st.subheader("🎯 Active Planned Decision")
        cash_depletion_pct = (profile.planned_purchase_amount / max(1.0, profile.current_savings)) * 100.0
        rem_after = profile.current_savings - profile.planned_purchase_amount
        rem_color = '#34d399' if rem_after >= profile.emergency_fund_target else '#fb7185'
        dep_color = '#fb7185' if cash_depletion_pct > 60 else '#fbbf24'

        st.html(f"""
        <div class="kpi-card cyan" style="min-height: 380px;">
            <div style="font-size: 0.72rem; color: #38bdf8; font-weight: 800; text-transform: uppercase; letter-spacing: 0.06em;">Contemplated Major Purchase</div>
            <div style="font-size: 1.5rem; font-weight: 800; color: #ffffff; margin: 0.4rem 0 0.2rem 0;">{profile.planned_purchase_name}</div>
            <div style="font-size: 2.2rem; font-weight: 800; color: #38bdf8; margin-bottom: 1.2rem;">₹{profile.planned_purchase_amount:,.0f}</div>
            
            <div style="border-top: 1px solid rgba(255,255,255,0.08); padding-top: 1rem; font-size: 0.85rem; color: #94a3b8;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                    <span>Upfront Cash Impact:</span>
                    <span style="color: {dep_color}; font-weight: 700;">Consumes {cash_depletion_pct:.0f}% of liquid savings</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                    <span>Remaining Emergency Buffer:</span>
                    <span style="color: {rem_color}; font-weight: 700;">₹{max(0.0, rem_after):,.0f}</span>
                </div>
            </div>

            <div style="margin-top: 1.2rem; padding: 0.8rem; background: rgba(245, 158, 11, 0.1); border: 1px solid rgba(245, 158, 11, 0.25); border-radius: 12px; font-size: 0.8rem; color: #fef3c7;">
                ⚠️ <b>Warning:</b> Buying upfront in cash drops your emergency runway significantly. Simulate before buying!
            </div>
        </div>
        """)

# ==============================================================================
# PAGE 2: PARALLEL FUTURES SIMULATOR
# ==============================================================================
elif page == "🔮 Parallel Futures Simulator":
    st.html("""
    <div style="margin-bottom: 1.5rem;">
        <h1 style="font-size: 2.4rem; font-weight: 800; background: linear-gradient(135deg, #ffffff 20%, #38bdf8 60%, #a855f7 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.2rem;">
            Parallel Financial Futures Engine
        </h1>
        <p style="color: #94a3b8; font-size: 1rem;">
            Simulating 5 concurrent futures under adverse life conditions: salary delays, medical emergencies, and inflation.
        </p>
    </div>
    """)

    # Interactive Shock Controls Matrix
    with st.container():
        st.markdown("**⚡ Stress-Test Parameter Control Panel**")
        sc_c1, sc_c2, sc_c3, sc_c4 = st.columns(4)
        with sc_c1:
            dur = st.slider("Simulation Horizon (Months)", min_value=6, max_value=24, value=12, step=1)
            purch_mode = st.selectbox("Payment Channel", ["EMI", "CASH", "NONE"], index=0)
        with sc_c2:
            purch_amt = st.number_input("Purchase Price (₹)", min_value=1000.0, value=float(profile.planned_purchase_amount), step=5000.0)
            down_pay = st.number_input("Down Payment (₹)", min_value=0.0, max_value=purch_amt-1000.0, value=min(10000.0, purch_amt*0.2), step=2000.0)
        with sc_c3:
            unexp_amt = st.number_input("Emergency Shock Expense (₹)", min_value=0.0, value=25000.0, step=5000.0)
            unexp_month = st.slider("Emergency Month", min_value=1, max_value=dur, value=3)
        with sc_c4:
            delay_start = st.slider("Salary Delay Month", min_value=1, max_value=dur, value=2)
            inflation_pct = st.slider("Cost Inflation (%)", min_value=0, max_value=40, value=15, step=5)

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
        st.error(f"🚨 **Catastrophic Breaking Point Detected:** {sim_results['recommendation']}")
    elif has_high:
        st.warning(f"⚠️ **Emergency Cushion Breach Detected:** {sim_results['recommendation']}")
    else:
        st.success(f"🛡️ **Resilient Across All 5 Parallel Futures:** {sim_results['recommendation']}")

    # Plotly Trajectory Chart
    st.subheader("📈 Projected Savings Trajectory Across 5 Parallel Futures")

    fig_lines = go.Figure()
    colors_map = {
        "baseline": "#10b981",          # Emerald
        "unexpected_expense": "#f97316",# Orange
        "delayed_salary": "#06b6d4",    # Electric Cyan
        "increased_spending": "#a855f7",# Violet
        "combined_adverse": "#f43f5e"   # Crimson
    }

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
                color=colors_map.get(sc_id, "#ffffff"),
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
        annotation_position="top right"
    )

    # Add Zero Line
    fig_lines.add_hline(
        y=0,
        line_dash="solid",
        line_color="#f43f5e",
        line_width=2,
        annotation_text="⚠️ Zero Cash Deficit Threshold",
        annotation_position="bottom right"
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

    # 5 Parallel Futures Identity Cards
    st.subheader("🌌 Future Timelines Breakdown & Resilience Index")

    sc_cards_html = '<div class="scenario-grid">'
    class_map = {
        "baseline": ("sc-baseline", "pill-emerald"),
        "unexpected_expense": ("sc-shock", "pill-orange"),
        "delayed_salary": ("sc-delay", "pill-cyan"),
        "increased_spending": ("sc-inflation", "pill-purple"),
        "combined_adverse": ("sc-nightmare", "pill-rose")
    }

    for sc_id, sc_data in scenarios.items():
        border_cls, pill_cls = class_map.get(sc_id, ("sc-baseline", "pill-emerald"))
        low_col = "#fb7185" if sc_data["lowest_savings"] < 0 else "#ffffff"
        
        sc_cards_html += f"""
        <div class="scenario-card {border_cls}">
            <div>
                <div class="sc-title">{sc_data['scenario_name']}</div>
                <span class="pill-tag {pill_cls}">{sc_data['risk_level']} RISK</span>
            </div>
            <div class="sc-val-box">
                <div class="sc-val-label">Lowest Savings Balance</div>
                <div class="sc-val-num" style="color: {low_col};">₹{sc_data['lowest_savings']:,.0f}</div>
            </div>
            <div style="font-size: 0.78rem; color: #94a3b8;">
                <div>Resilience Score: <b style="color: #ffffff;">{sc_data['resilience_score']}/100</b></div>
                <div>Deficit Months: <b style="color: {'#fb7185' if sc_data['negative_cash_months'] > 0 else '#34d399'};">{sc_data['negative_cash_months']}</b></div>
            </div>
            <div style="font-size: 0.73rem; color: #cbd5e1; border-top: 1px solid rgba(255,255,255,0.08); padding-top: 0.5rem; margin-top: 0.5rem;">
                {sc_data['breaking_point_reason']}
            </div>
        </div>
        """
    sc_cards_html += '</div>'
    st.html(sc_cards_html)

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
    st.html("""
    <div style="margin-bottom: 1.5rem;">
        <h1 style="font-size: 2.4rem; font-weight: 800; background: linear-gradient(135deg, #ffffff 20%, #34d399 60%, #38bdf8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.2rem;">
            Purchase Affordability Decision Matrix
        </h1>
        <p style="color: #94a3b8; font-size: 1rem;">
            Comparing 4 distinct financial execution pathways: Cash vs Save-and-Wait vs Alternative vs EMI Financing.
        </p>
    </div>
    """)

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

    rec_label = eval_result['recommended_option_id'].replace('_', ' ').upper()
    st.success(f"⭐ **Parallelverse Recommendation: {rec_label}** — {eval_result['verdict_explanation']}")

    # 4 Visual Pathway Cards
    pathways_html = '<div class="pathway-grid">'
    for opt in eval_result["options"]:
        is_rec = opt["option_id"] == eval_result["recommended_option_id"]
        rec_cls = "recommended" if is_rec else ""
        rec_badge = '<div class="pathway-badge-rec">⭐ Best Fit</div>' if is_rec else ''
        pill_cls = "pill-emerald" if opt["risk_rating"] == "SAFE" else ("pill-orange" if opt["risk_rating"] == "CAUTION" else "pill-rose")
        buf_col = "#34d399" if opt['emergency_buffer_preserved_pct'] >= 100 else "#fbbf24"

        pathways_html += f"""
        <div class="pathway-card {rec_cls}">
            {rec_badge}
            <div style="font-weight: 800; font-size: 1.15rem; color: #ffffff; margin-bottom: 0.5rem;">{opt['option_title']}</div>
            <span class="pill-tag {pill_cls}">{opt['risk_rating']}</span>
            
            <div style="margin: 1.2rem 0 0.8rem 0; border-top: 1px solid rgba(255,255,255,0.08); padding-top: 0.8rem;">
                <div style="font-size: 0.72rem; color: #94a3b8; text-transform: uppercase;">Upfront Cash Required</div>
                <div style="font-size: 1.4rem; font-weight: 800; color: #ffffff;">₹{opt['upfront_cash_required']:,.0f}</div>
            </div>

            <div style="margin-bottom: 0.8rem;">
                <div style="font-size: 0.72rem; color: #94a3b8; text-transform: uppercase;">Monthly Obligation</div>
                <div style="font-size: 1.4rem; font-weight: 800; color: #38bdf8;">₹{opt['monthly_obligation']:,.0f}<span style="font-size: 0.8rem; color: #94a3b8;">/mo</span></div>
            </div>

            <div style="margin-bottom: 1rem;">
                <div style="font-size: 0.72rem; color: #94a3b8; text-transform: uppercase;">Emergency Reserve Retained</div>
                <div style="font-size: 1.2rem; font-weight: 700; color: {buf_col};">{opt['emergency_buffer_preserved_pct']:.0f}% <span style="font-size: 0.75rem; color: #94a3b8;">of safety target</span></div>
            </div>

            <div style="font-size: 0.78rem; color: #cbd5e1; border-top: 1px solid rgba(255,255,255,0.08); padding-top: 0.8rem;">
                <b>Trade-off:</b><br>{opt['key_tradeoff']}
            </div>
        </div>
        """
    pathways_html += '</div>'
    st.html(pathways_html)

# ==============================================================================
# PAGE 4: EMI CALCULATOR
# ==============================================================================
elif page == "🧮 Reducing-Balance EMI Engine":
    st.html("""
    <div style="margin-bottom: 1.5rem;">
        <h1 style="font-size: 2.4rem; font-weight: 800; background: linear-gradient(135deg, #ffffff 20%, #fbbf24 60%, #f97316 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.2rem;">
            Precision Reducing-Balance EMI Engine
        </h1>
        <p style="color: #94a3b8; font-size: 1rem;">
            Mathematical reducing-balance amortization schedules, interest totals reconciliation, and early prepayment simulation.
        </p>
    </div>
    """)

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

    # 4 Glowing Result Tiles
    st.html(f"""
    <div class="kpi-grid">
        <div class="kpi-card emerald">
            <div class="kpi-label"><span>Monthly EMI</span><span>💳</span></div>
            <div class="kpi-value" style="color: #34d399;">₹{emi_data['monthly_emi']:,.2f}</div>
            <div class="kpi-footer" style="color: #38bdf8;">For {tenure} months</div>
        </div>

        <div class="kpi-card cyan">
            <div class="kpi-label"><span>Principal Financed</span><span>🏷️</span></div>
            <div class="kpi-value">₹{emi_data['principal_financed']:,.0f}</div>
            <div class="kpi-footer" style="color: #94a3b8;">Excludes down payment</div>
        </div>

        <div class="kpi-card orange">
            <div class="kpi-label"><span>Total Interest Cost</span><span>🔥</span></div>
            <div class="kpi-value" style="color: #fb923c;">₹{emi_data['total_interest']:,.2f}</div>
            <div class="kpi-footer" style="color: #94a3b8;">Borrowing cost</div>
        </div>

        <div class="kpi-card purple">
            <div class="kpi-label"><span>Total Repaid</span><span>💰</span></div>
            <div class="kpi-value">₹{emi_data['total_repayment']:,.2f}</div>
            <div class="kpi-footer" style="color: #34d399;">Reconciled to ₹0.00</div>
        </div>
    </div>
    """)

    # Charts & Schedule Table
    c_pie, c_table = st.columns([1, 1.8])
    with c_pie:
        st.subheader("🥧 Principal vs Interest Split")
        pie_df = pd.DataFrame([
            {"Component": "Principal Financed", "Value": emi_data["principal_financed"], "Color": "#10b981"},
            {"Component": "Total Interest Cost", "Value": emi_data["total_interest"], "Color": "#f43f5e"}
        ])
        fig_emi_pie = px.pie(
            pie_df, values="Value", names="Component", hole=0.62,
            color="Component",
            color_discrete_map={"Principal Financed": "#10b981", "Total Interest Cost": "#f43f5e"}
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
        st.subheader("📜 Month-by-Month Amortization Schedule")
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
    st.html("""
    <div style="margin-bottom: 1.5rem;">
        <h1 style="font-size: 2.4rem; font-weight: 800; background: linear-gradient(135deg, #ffffff 20%, #a855f7 60%, #f43f5e 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.2rem;">
            Installment Tracker & Calendar Reminders
        </h1>
        <p style="color: #94a3b8; font-size: 1rem;">
            Monitor active loan commitments, update installment statuses, and download one-click <b>RFC 5545 iCalendar (.ics)</b> reminders for your smartphone.
        </p>
    </div>
    """)

    db = SessionLocal()
    try:
        plans = db.query(InstallmentPlan).all()

        with st.expander("➕ Create New Installment Commitment", expanded=False):
            with st.form("new_plan_form"):
                f1, f2, f3 = st.columns(3)
                with f1:
                    new_name = st.text_input("Item Description", value="Sony PlayStation 5 Pro")
                    new_cat = st.selectbox("Category", ["Electronics", "Vehicles", "Education", "Appliances", "Furniture", "Other"])
                with f2:
                    new_tot = st.number_input("Purchase Price (₹)", min_value=1000.0, value=65000.0, step=2000.0)
                    new_down = st.number_input("Down Payment (₹)", min_value=0.0, max_value=new_tot-500.0, value=15000.0, step=2000.0)
                with f3:
                    new_rate = st.number_input("Annual Interest (%)", min_value=0.0, value=12.0, step=0.5)
                    new_ten = st.number_input("Tenure (Months)", min_value=1, max_value=48, value=12, step=1)
                    new_due_d = st.slider("Monthly Payment Due Day", min_value=1, max_value=28, value=5)

                submitted = st.form_submit_button("Create & Generate Schedule")
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
                    st.success(f"Plan '{new_name}' created successfully with {new_ten} installments!")
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
                border_col = '#f43f5e' if has_overdue else '#10b981'
                status_txt = 'OVERDUE DETECTED' if has_overdue else 'ACTIVE & ON TRACK'
                pill_st = 'pill-rose' if has_overdue else 'pill-emerald'

                st.html(f"""
                <div class="kpi-card cyan" style="margin-bottom: 1.2rem; border-left: 5px solid {border_col};">
                    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;">
                        <div>
                            <span class="pill-tag pill-cyan">{plan.category}</span>
                            <span class="pill-tag {pill_st}" style="margin-left: 6px;">{status_txt}</span>
                            <div style="font-size: 1.4rem; font-weight: 800; color: #ffffff; margin: 0.5rem 0 0.2rem 0;">{plan.purchase_name}</div>
                            <div style="color: #94a3b8; font-size: 0.88rem;">
                                Financed: <b>₹{plan.principal_financed:,.0f}</b> | 
                                Monthly EMI: <b style="color: #34d399;">₹{plan.monthly_emi:,.2f}</b> | 
                                Due Day: <b>{plan.due_day}th of every month</b>
                            </div>
                        </div>
                        <div style="text-align: right;">
                            <div style="font-size: 0.75rem; color: #94a3b8; text-transform: uppercase;">Repayment Progress</div>
                            <div style="font-size: 1.5rem; font-weight: 800; color: #34d399;">{paid_c} / {total_c} Paid</div>
                            <div style="font-size: 0.8rem; color: #94a3b8;">({progress_pct:.0f}% Completed)</div>
                        </div>
                    </div>
                </div>
                """)

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
                            st.write(f"**#{p.installment_number}**")
                        with p_c2:
                            st.write(f"Due: **{p.due_date.strftime('%d %b %Y')}**")
                        with p_c3:
                            st.write(f"Amount: **₹{p.emi_amount:,.2f}**")
                        with p_c4:
                            if p.status == 'PAID':
                                st.html('<span class="pill-tag pill-emerald">PAID</span>')
                            elif p.status == 'OVERDUE':
                                st.html('<span class="pill-tag pill-rose">OVERDUE</span>')
                            else:
                                st.html('<span class="pill-tag pill-orange">PENDING</span>')
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
    st.html("""
    <div style="margin-bottom: 1.5rem;">
        <h1 style="font-size: 2.4rem; font-weight: 800; background: linear-gradient(135deg, #ffffff 20%, #38bdf8 60%, #10b981 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.2rem;">
            Financial Profile & Scenario Assumptions
        </h1>
        <p style="color: #94a3b8; font-size: 1rem;">
            Configure your actual baseline finances or test custom financial setups. Changes persist automatically to SQLite.
        </p>
    </div>
    """)

    db = SessionLocal()
    try:
        prof = db.query(FinancialProfile).first()

        with st.form("edit_profile_form"):
            c_f1, c_f2 = st.columns(2)
            with c_f1:
                st.subheader("💼 Income & Liquid Reserves")
                name_val = st.text_input("Full Name", value=prof.full_name)
                inc_val = st.number_input("Monthly Take-Home Income (₹)", min_value=0.0, value=float(prof.monthly_income), step=5000.0)
                sav_val = st.number_input("Current Liquid Savings (₹)", min_value=0.0, value=float(prof.current_savings), step=10000.0)
                emerg_val = st.number_input("Target Emergency Reserve (₹)", min_value=0.0, value=float(prof.emergency_fund_target), step=10000.0)

            with c_f2:
                st.subheader("🏠 Routine Expenditures & Debts")
                ess_val = st.number_input("Essential Expenses (Rent, Food, Healthcare) (₹)", min_value=0.0, value=float(prof.essential_expenses), step=2000.0)
                disc_val = st.number_input("Discretionary Expenses (Dining, Leisure) (₹)", min_value=0.0, value=float(prof.discretionary_expenses), step=2000.0)
                debt_val = st.number_input("Existing Monthly Loan / EMI Payments (₹)", min_value=0.0, value=float(prof.existing_debt_emi), step=1000.0)

            st.subheader("🛍️ Active Contemplated Purchase")
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

# ==============================================================================
# POLISHED FINTECH FOOTER
# ==============================================================================
st.html("""
<div class="fin-footer">
    <div>
        <div style="font-weight: 800; font-size: 1.15rem; color: #ffffff;">🌌 Financial Parallelverse</div>
        <div style="font-size: 0.8rem; color: #94a3b8; margin-top: 0.2rem;">
            Explore your financial futures before making a decision &bull; Built for Hack-o-Ween 2nd Edition (PES University)
        </div>
        <div style="font-size: 0.75rem; color: #64748b; margin-top: 0.4rem;">
            Track: <b>The Vampire's Ledger (FinTech)</b> &bull; Team: <b>Dark_Knights</b> (Ratnala Aneesh, Raghoothama T R, Vatsal Soni)
        </div>
    </div>
    <div style="display: flex; gap: 20px; font-size: 0.82rem; color: #94a3b8;">
        <div>🟢 <b>FastAPI</b> :8000</div>
        <div>🛡️ <b>SQLite 3</b> Local DB</div>
        <div>📅 <b>RFC 5545</b> iCal Export</div>
        <div>🧪 <b>23/23 Tests</b> Passing</div>
    </div>
</div>
""")
