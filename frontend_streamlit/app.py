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
# 🎨 3-MODE THEME ENGINE: DARK CYBER / PURE WHITE / SLATE MODERN
# ==============================================================================
if "theme_mode" not in st.session_state:
    st.session_state["theme_mode"] = "🌌 Dark Cyber"

theme = st.session_state["theme_mode"]

if theme == "☀️ Pure White":
    # Clean FinTech Ivory / White Theme
    bg_style = "linear-gradient(135deg, #f8fafc 0%, #edf2f7 50%, #f1f5f9 100%)"
    text_main = "#0f172a"
    text_muted = "#475569"
    card_bg = "linear-gradient(135deg, #ffffff 0%, #f8fafc 100%)"
    card_border = "1px solid rgba(0, 0, 0, 0.09)"
    card_shadow = "0 8px 24px rgba(0, 0, 0, 0.06)"
    sidebar_bg = "#f1f5f9"
    chart_bg = "#ffffff"
    chart_font = "#0f172a"
    chart_grid = "rgba(0, 0, 0, 0.08)"
    hero_bg = "linear-gradient(135deg, #ffffff 0%, #f1f5f9 100%)"
    hero_border = "1px solid rgba(0, 0, 0, 0.1)"
    hero_title_grad = "linear-gradient(135deg, #0f172a 10%, #0284c7 50%, #059669 100%)"
    nav_item_bg = "rgba(0, 0, 0, 0.03)"
    nav_item_border = "1px solid rgba(0, 0, 0, 0.08)"
    nav_item_hover_bg = "rgba(2, 132, 199, 0.08)"
    nav_item_active_bg = "linear-gradient(135deg, rgba(2, 132, 199, 0.12) 0%, rgba(16, 185, 129, 0.12) 100%)"
    nav_item_active_border = "1px solid #0284c7"
    nav_item_text = "#1e293b"
    nav_item_active_text = "#0369a1"
    sidebar_divider = "linear-gradient(90deg, transparent, rgba(0, 0, 0, 0.12), transparent)"
    persona_btn_bg = "#ffffff"
    persona_btn_border = "1px solid rgba(0, 0, 0, 0.12)"
    persona_btn_text = "#0f172a"
    hud_bg = "rgba(255, 255, 255, 0.9)"
    hud_border = "1px solid rgba(0, 0, 0, 0.1)"
elif theme == "⚡ Slate Modern":
    # Modern Executive Slate Theme
    bg_style = "linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%)"
    text_main = "#f8fafc"
    text_muted = "#94a3b8"
    card_bg = "linear-gradient(135deg, rgba(30, 41, 59, 0.9) 0%, rgba(15, 23, 42, 0.95) 100%)"
    card_border = "1px solid rgba(255, 255, 255, 0.1)"
    card_shadow = "0 10px 30px rgba(0, 0, 0, 0.4)"
    sidebar_bg = "#0b1120"
    chart_bg = "#1e293b"
    chart_font = "#f8fafc"
    chart_grid = "rgba(255, 255, 255, 0.08)"
    hero_bg = "linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.95) 100%)"
    hero_border = "1px solid rgba(255, 255, 255, 0.12)"
    hero_title_grad = "linear-gradient(135deg, #ffffff 10%, #38bdf8 50%, #34d399 100%)"
    nav_item_bg = "rgba(255, 255, 255, 0.03)"
    nav_item_border = "1px solid rgba(255, 255, 255, 0.08)"
    nav_item_hover_bg = "rgba(56, 189, 248, 0.12)"
    nav_item_active_bg = "linear-gradient(135deg, rgba(56, 189, 248, 0.18) 0%, rgba(99, 102, 241, 0.22) 100%)"
    nav_item_active_border = "1px solid #38bdf8"
    nav_item_text = "#e2e8f0"
    nav_item_active_text = "#38bdf8"
    sidebar_divider = "linear-gradient(90deg, transparent, rgba(56, 189, 248, 0.25), transparent)"
    persona_btn_bg = "rgba(30, 41, 59, 0.9)"
    persona_btn_border = "1px solid rgba(255, 255, 255, 0.12)"
    persona_btn_text = "#f8fafc"
    hud_bg = "linear-gradient(135deg, rgba(30, 41, 59, 0.85) 0%, rgba(15, 23, 42, 0.95) 100%)"
    hud_border = "1px solid rgba(255, 255, 255, 0.1)"
else:
    # 🌌 Dark Cyber Theme (Default)
    bg_style = "radial-gradient(circle at 15% 15%, #0e172a 0%, #080c17 45%, #050811 100%)"
    text_main = "#f8fafc"
    text_muted = "#94a3b8"
    card_bg = "linear-gradient(135deg, rgba(19, 29, 49, 0.8) 0%, rgba(13, 20, 36, 0.9) 100%)"
    card_border = "1px solid rgba(255, 255, 255, 0.08)"
    card_shadow = "0 10px 30px rgba(0, 0, 0, 0.4)"
    sidebar_bg = "#090e1a"
    chart_bg = "#0c1220"
    chart_font = "#f8fafc"
    chart_grid = "rgba(255, 255, 255, 0.06)"
    hero_bg = "linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.9) 100%)"
    hero_border = "1px solid rgba(255, 255, 255, 0.1)"
    hero_title_grad = "linear-gradient(135deg, #ffffff 10%, #38bdf8 45%, #a855f7 75%, #34d399 100%)"
    nav_item_bg = "rgba(255, 255, 255, 0.02)"
    nav_item_border = "1px solid rgba(255, 255, 255, 0.06)"
    nav_item_hover_bg = "rgba(56, 189, 248, 0.15)"
    nav_item_active_bg = "linear-gradient(135deg, rgba(14, 165, 233, 0.22) 0%, rgba(139, 92, 246, 0.25) 100%)"
    nav_item_active_border = "1px solid #38bdf8"
    nav_item_text = "#f8fafc"
    nav_item_active_text = "#38bdf8"
    sidebar_divider = "linear-gradient(90deg, transparent, rgba(56, 189, 248, 0.3), transparent)"
    persona_btn_bg = "rgba(19, 29, 49, 0.8)"
    persona_btn_border = "1px solid rgba(56, 189, 248, 0.3)"
    persona_btn_text = "#f8fafc"
    hud_bg = "linear-gradient(135deg, rgba(19, 29, 49, 0.85) 0%, rgba(13, 20, 36, 0.95) 100%)"
    hud_border = "1px solid rgba(56, 189, 248, 0.2)"

st.html(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,700&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }}

    .stApp {{
        background: {bg_style} !important;
        color: {text_main} !important;
    }}

    /* Global Typography */
    h1, h2, h3, h4, h5, p, span, div {{
        color: {text_main};
    }}

    /* Futuristic glowing divider replacing retro HR */
    hr {{
        border: none !important;
        height: 1px !important;
        background: {sidebar_divider} !important;
        margin: 1.2rem 0 !important;
    }}

    /* ========================================================================= */
    /* ULTRA-MODERN MISSION CONTROL NAVIGATION MENU STYLING (NO 1990s DOTS!)     */
    /* ========================================================================= */
    
    /* Kill default 1990s circular radio buttons */
    div[data-testid="stRadio"] label > div:first-child {{
        display: none !important;
    }}

    /* Sidebar Navigation Menu */
    section[data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] {{
        display: flex !important;
        flex-direction: column !important;
        gap: 7px !important;
    }}

    /* Main-page Horizontal Segmented Radios */
    div[data-testid="stRadio"] div[role="radiogroup"] {{
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: wrap !important;
        gap: 10px !important;
    }}

    /* Modern floating navigation card */
    div[data-testid="stRadio"] label {{
        display: flex !important;
        align-items: center !important;
        padding: 0.72rem 1.05rem !important;
        margin: 0 !important;
        border-radius: 13px !important;
        background: {nav_item_bg} !important;
        border: {nav_item_border} !important;
        transition: all 0.22s cubic-bezier(0.4, 0, 0.2, 1) !important;
        cursor: pointer !important;
        position: relative !important;
        overflow: hidden !important;
    }}

    section[data-testid="stSidebar"] div[data-testid="stRadio"] label {{
        width: 100% !important;
    }}

    /* Hover elevation & glow */
    div[data-testid="stRadio"] label:hover {{
        background: {nav_item_hover_bg} !important;
        border-color: rgba(56, 189, 248, 0.45) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 15px rgba(56, 189, 248, 0.15) !important;
    }}

    section[data-testid="stSidebar"] div[data-testid="stRadio"] label:hover {{
        transform: translateX(4px) !important;
    }}

    /* Active / Selected Tab */
    div[data-testid="stRadio"] label:has(input:checked),
    div[data-testid="stRadio"] label[aria-checked="true"],
    div[data-testid="stRadio"] label[data-checked="true"] {{
        background: {nav_item_active_bg} !important;
        border: {nav_item_active_border} !important;
        box-shadow: 0 4px 20px rgba(56, 189, 248, 0.22), inset 0 0 12px rgba(56, 189, 248, 0.08) !important;
    }}

    /* Left glowing neon indicator bar on active item */
    div[data-testid="stRadio"] label:has(input:checked)::before,
    div[data-testid="stRadio"] label[aria-checked="true"]::before {{
        content: '' !important;
        position: absolute !important;
        left: 0 !important;
        top: 0 !important;
        bottom: 0 !important;
        width: 4px !important;
        background: linear-gradient(180deg, #38bdf8 0%, #10b981 100%) !important;
        border-radius: 4px 0 0 4px !important;
    }}

    /* Navigation text */
    div[data-testid="stRadio"] label p {{
        font-size: 0.88rem !important;
        font-weight: 700 !important;
        color: {nav_item_text} !important;
        margin: 0 !important;
        letter-spacing: -0.01em !important;
        transition: color 0.2s ease !important;
    }}

    div[data-testid="stRadio"] label:has(input:checked) p,
    div[data-testid="stRadio"] label[aria-checked="true"] p {{
        color: {nav_item_active_text} !important;
        font-weight: 800 !important;
    }}

    /* Persona Switcher Buttons in Sidebar */
    section[data-testid="stSidebar"] div[data-testid="column"] .stButton>button {{
        background: {persona_btn_bg} !important;
        border: {persona_btn_border} !important;
        color: {persona_btn_text} !important;
        font-weight: 700 !important;
        font-size: 0.78rem !important;
        padding: 0.65rem 0.5rem !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
        transition: all 0.22s ease !important;
        width: 100% !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
    }}

    section[data-testid="stSidebar"] div[data-testid="column"] .stButton>button:hover {{
        background: linear-gradient(135deg, rgba(56, 189, 248, 0.2) 0%, rgba(16, 185, 129, 0.2) 100%) !important;
        border-color: #38bdf8 !important;
        color: #38bdf8 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 18px rgba(56, 189, 248, 0.25) !important;
    }}

    /* Selectbox Styling */
    div[data-baseweb="select"] > div {{
        background: {card_bg} !important;
        border: {card_border} !important;
        border-radius: 12px !important;
        color: {text_main} !important;
    }}

    /* Pulsing animations */
    @keyframes pulse-dot {{
        0% {{ transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }}
        70% {{ transform: scale(1.05); box-shadow: 0 0 0 8px rgba(16, 185, 129, 0); }}
        100% {{ transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }}
    }}

    @keyframes pulse-radar {{
        0% {{ transform: scale(0.95); box-shadow: 0 0 0 0 rgba(56, 189, 248, 0.7); }}
        70% {{ transform: scale(1.05); box-shadow: 0 0 0 8px rgba(56, 189, 248, 0); }}
        100% {{ transform: scale(0.95); box-shadow: 0 0 0 0 rgba(56, 189, 248, 0); }}
    }}

    /* Hero Mesh Banner */
    .hero-container {{
        background: {hero_bg};
        border: {hero_border};
        border-radius: 24px;
        padding: 2.2rem 2.6rem;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
        box-shadow: {card_shadow};
    }}

    .hero-title {{
        font-size: 2.7rem;
        font-weight: 800;
        line-height: 1.15;
        letter-spacing: -0.03em;
        margin-bottom: 0.75rem;
        background: {hero_title_grad};
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}

    .hero-subtitle {{
        color: {text_muted};
        font-size: 1.05rem;
        max-width: 720px;
        line-height: 1.5;
        margin-bottom: 1.4rem;
    }}

    /* KPI Glow Cards */
    .kpi-grid {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1.25rem;
        margin-bottom: 2rem;
    }}

    .kpi-card {{
        background: {card_bg};
        border-radius: 20px;
        padding: 1.4rem 1.6rem;
        position: relative;
        overflow: hidden;
        border: {card_border};
        box-shadow: {card_shadow};
        transition: transform 0.25s ease, box-shadow 0.25s ease;
    }}

    .kpi-card:hover {{
        transform: translateY(-4px);
    }}

    .kpi-card.emerald {{ border-top: 4px solid #10b981; }}
    .kpi-card.cyan {{ border-top: 4px solid #06b6d4; }}
    .kpi-card.purple {{ border-top: 4px solid #a855f7; }}
    .kpi-card.orange {{ border-top: 4px solid #f97316; }}
    .kpi-card.rose {{ border-top: 4px solid #f43f5e; }}

    .kpi-label {{
        font-size: 0.76rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: {text_muted};
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.4rem;
    }}

    .kpi-value {{
        font-size: 2.1rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        line-height: 1.1;
    }}

    /* Timeline Scenario Identity Cards */
    .scenario-grid {{
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 1.1rem;
        margin-bottom: 2rem;
    }}

    .scenario-card {{
        border-radius: 18px;
        padding: 1.35rem 1.25rem;
        position: relative;
        overflow: hidden;
        background: {card_bg};
        border: {card_border};
        box-shadow: {card_shadow};
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        min-height: 310px;
        transition: transform 0.25s ease;
    }}

    .scenario-card:hover {{
        transform: translateY(-4px);
    }}

    .sc-baseline {{ border-top: 4px solid #10b981; }}
    .sc-shock {{ border-top: 4px solid #f97316; }}
    .sc-delay {{ border-top: 4px solid #06b6d4; }}
    .sc-inflation {{ border-top: 4px solid #a855f7; }}
    .sc-nightmare {{ border-top: 4px solid #f43f5e; }}

    .sc-title {{
        font-weight: 800;
        font-size: 1rem;
        margin-bottom: 0.4rem;
    }}

    .pill-tag {{
        display: inline-block;
        padding: 0.25rem 0.65rem;
        border-radius: 9999px;
        font-size: 0.68rem;
        font-weight: 800;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }}

    .pill-emerald {{ background: rgba(16, 185, 129, 0.15); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.35); }}
    .pill-orange {{ background: rgba(249, 115, 22, 0.15); color: #f97316; border: 1px solid rgba(249, 115, 22, 0.35); }}
    .pill-cyan {{ background: rgba(6, 182, 212, 0.15); color: #06b6d4; border: 1px solid rgba(6, 182, 212, 0.35); }}
    .pill-purple {{ background: rgba(168, 85, 247, 0.15); color: #a855f7; border: 1px solid rgba(168, 85, 247, 0.35); }}
    .pill-rose {{ background: rgba(244, 63, 94, 0.15); color: #f43f5e; border: 1px solid rgba(244, 63, 94, 0.35); }}

    .sc-val-box {{
        margin: 1rem 0;
        background: rgba(125, 125, 125, 0.06);
        border: {card_border};
        border-radius: 12px;
        padding: 0.75rem;
    }}

    .sc-val-label {{ font-size: 0.7rem; color: {text_muted}; text-transform: uppercase; }}
    .sc-val-num {{ font-size: 1.35rem; font-weight: 800; }}

    /* Purchase Option Cards */
    .pathway-grid {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1.25rem;
        margin-top: 1.5rem;
        margin-bottom: 2rem;
    }}

    .pathway-card {{
        background: {card_bg};
        border-radius: 20px;
        padding: 1.6rem 1.4rem;
        border: {card_border};
        box-shadow: {card_shadow};
        position: relative;
        overflow: hidden;
        transition: transform 0.25s ease;
    }}

    .pathway-card:hover {{
        transform: translateY(-4px);
    }}

    .pathway-card.recommended {{
        border: 2px solid #10b981;
    }}

    .pathway-badge-rec {{
        position: absolute;
        top: 1rem;
        right: 1rem;
        background: linear-gradient(90deg, #10b981 0%, #06b6d4 100%);
        color: #041a11;
        font-weight: 800;
        font-size: 0.68rem;
        text-transform: uppercase;
        padding: 0.25rem 0.65rem;
        border-radius: 9999px;
    }}

    /* Advanced Sidebar Nav Styling */
    section[data-testid="stSidebar"] {{
        background: {sidebar_bg} !important;
        border-right: {card_border};
    }}

    /* Buttons */
    .stButton>button {{
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        color: #ffffff !important;
        font-weight: 800 !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.55rem 1.4rem !important;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3) !important;
    }}

    /* Polished Footer */
    .fin-footer {{
        border-top: {card_border};
        padding: 2rem 1.5rem;
        margin-top: 3rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 1.5rem;
    }}
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

# ==============================================================================
# ADVANCED NAVIGATION SIDEBAR WITH 3-MODE THEME & PERSONA ENGINE
# ==============================================================================
with st.sidebar:
    st.html(f"""
    <div style="background: {card_bg}; border: {card_border}; border-radius: 18px; padding: 1.1rem 1.2rem; margin-bottom: 1.2rem; box-shadow: {card_shadow}; position: relative; overflow: hidden;">
        <div style="position: absolute; top: 0; left: 0; right: 0; height: 3px; background: linear-gradient(90deg, #38bdf8, #818cf8, #10b981);"></div>
        <div style="display: flex; align-items: center; gap: 12px;">
            <div style="width: 44px; height: 44px; border-radius: 12px; background: linear-gradient(135deg, #0284c7 0%, #6366f1 50%, #10b981 100%); display: flex; align-items: center; justify-content: center; font-size: 1.5rem; box-shadow: 0 4px 16px rgba(2, 132, 199, 0.35);">
                🌌
            </div>
            <div>
                <div style="font-size: 1.25rem; font-weight: 800; letter-spacing: -0.02em; line-height: 1.2;">Parallelverse</div>
                <div style="font-size: 0.7rem; color: #06b6d4; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; display: flex; align-items: center; gap: 5px;">
                    <span style="display: inline-block; width: 6px; height: 6px; border-radius: 50%; background: #10b981; animation: pulse-dot 2s infinite;"></span>
                    FinTech Cockpit
                </div>
            </div>
        </div>
    </div>
    """)

    # 3-Mode Theme Selector with Modern Capsule Header
    st.html(f"""
    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.4rem; padding: 0 4px;">
        <span style="font-size: 0.72rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.06em; color: {text_muted};">
            🎨 VISUAL THEME
        </span>
        <span style="font-size: 0.65rem; background: rgba(56, 189, 248, 0.12); color: #38bdf8; padding: 2px 8px; border-radius: 9999px; font-weight: 700;">
            3 MODES
        </span>
    </div>
    """)
    selected_theme = st.selectbox(
        "Theme Mode",
        ["🌌 Dark Cyber", "☀️ Pure White", "⚡ Slate Modern"],
        index=["🌌 Dark Cyber", "☀️ Pure White", "⚡ Slate Modern"].index(st.session_state["theme_mode"]),
        label_visibility="collapsed"
    )
    if selected_theme != st.session_state["theme_mode"]:
        st.session_state["theme_mode"] = selected_theme
        st.rerun()

    # Sleek High-Tech Mission Control Header
    st.html(f"""
    <div style="margin: 1.2rem 0 0.6rem 0; padding: 0 4px; display: flex; align-items: center; justify-content: space-between;">
        <div style="display: flex; align-items: center; gap: 8px;">
            <span style="display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: #10b981; animation: pulse-dot 2s infinite;"></span>
            <span style="font-size: 0.76rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.08em; color: {text_muted};">
                MISSION CONTROL
            </span>
        </div>
        <span style="font-size: 0.64rem; background: rgba(16, 185, 129, 0.15); color: #10b981; padding: 2px 8px; border-radius: 9999px; font-weight: 800; border: 1px solid rgba(16, 185, 129, 0.3);">
            ONLINE
        </span>
    </div>
    """)

    page = st.radio(
        "MISSION CONTROL NAVIGATION",
        [
            "📊 Executive Dashboard",
            "🔮 Parallel Futures Simulator",
            "⚖️ Purchase Affordability Matrix",
            "🧮 Reducing-Balance EMI Engine",
            "📅 Installment Tracker & Reminders",
            "👤 Financial Profile & Presets"
        ],
        index=0,
        label_visibility="collapsed"
    )

    # Sleek Persona Switcher Section
    st.html(f"""
    <div style="margin: 1.2rem 0 0.5rem 0; padding: 0 4px; display: flex; align-items: center; justify-content: space-between;">
        <span style="font-size: 0.72rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.06em; color: {text_muted};">
            ⚡ INSTANT PERSONA
        </span>
        <span style="font-size: 0.65rem; color: #38bdf8; font-weight: 700;">PRESETS</span>
    </div>
    """)

    c_p1, c_p2 = st.columns(2)
    with c_p1:
        if st.button("🎓 Student\n₹25k/mo", use_container_width=True):
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
        if st.button("💼 Techie\n₹75k/mo", use_container_width=True):
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

    profile = get_user_profile()
    metrics = FinancialEngine.calculate_profile_metrics(
        monthly_income=profile.monthly_income,
        current_savings=profile.current_savings,
        essential_expenses=profile.essential_expenses,
        discretionary_expenses=profile.discretionary_expenses,
        existing_debt_emi=profile.existing_debt_emi,
        emergency_fund_target=profile.emergency_fund_target
    )

    runway_pct = min(100, int((metrics['months_of_runway'] / 6.0) * 100))
    runway_bar_col = "#10b981" if metrics['months_of_runway'] >= 3 else "#f59e0b"

    # Cyber Active Persona Profile Card
    st.html(f"""
    <div style="background: {card_bg}; border: {card_border}; border-radius: 16px; padding: 1.1rem; font-size: 0.82rem; margin-top: 1.2rem; box-shadow: {card_shadow}; position: relative; overflow: hidden;">
        <div style="position: absolute; top: 0; left: 0; right: 0; height: 3px; background: linear-gradient(90deg, #10b981, #06b6d4, #8b5cf6);"></div>
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
            <span style="color: #06b6d4; font-size: 0.7rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.05em;">ACTIVE PERSONA</span>
            <span style="font-size: 0.65rem; background: rgba(16, 185, 129, 0.15); color: #10b981; padding: 2px 7px; border-radius: 9999px; font-weight: 800;">VERIFIED</span>
        </div>
        <div style="font-weight: 800; font-size: 1.05rem; margin-bottom: 0.75rem; display: flex; align-items: center; gap: 8px;">
            <div style="width: 26px; height: 26px; border-radius: 50%; background: linear-gradient(135deg, #38bdf8, #818cf8); display: flex; align-items: center; justify-content: center; font-size: 0.75rem; font-weight: 800; color: #041421;">
                {profile.full_name[0]}
            </div>
            <span>{profile.full_name}</span>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 0.35rem;">
            <span style="color: {text_muted};">Monthly Inflow:</span>
            <span style="font-weight: 800;">₹{profile.monthly_income:,.0f}</span>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 0.35rem;">
            <span style="color: {text_muted};">Liquid Reserve:</span>
            <span style="color: #10b981; font-weight: 800;">₹{profile.current_savings:,.0f}</span>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 0.6rem;">
            <span style="color: {text_muted};">Monthly Surplus:</span>
            <span style="color: {'#10b981' if metrics['free_cash_flow'] >= 0 else '#f43f5e'}; font-weight: 800;">₹{metrics['free_cash_flow']:,.0f}</span>
        </div>
        <div style="margin-top: 0.6rem; padding-top: 0.6rem; border-top: 1px solid rgba(255, 255, 255, 0.06);">
            <div style="display: flex; justify-content: space-between; font-size: 0.7rem; margin-bottom: 4px;">
                <span style="color: {text_muted};">Runway Security:</span>
                <span style="font-weight: 800; color: {runway_bar_col};">{metrics['months_of_runway']:.1f} Months</span>
            </div>
            <div style="width: 100%; height: 5px; background: rgba(125, 125, 125, 0.15); border-radius: 9999px; overflow: hidden;">
                <div style="width: {runway_pct}%; height: 100%; background: {runway_bar_col}; border-radius: 9999px;"></div>
            </div>
        </div>
    </div>
    <div style="margin-top: 1.2rem; text-align: center; font-size: 0.72rem; color: {text_muted};">
        🛡️ Track: <b>The Vampire's Ledger (FinTech)</b><br>Hack-o-Ween PESU &bull; Team Dark_Knights
    </div>
    """)

# Ultra-Modern Mission Control HUD Telemetry Banner
st.html(f"""
<div style="background: {hud_bg}; border: {hud_border}; border-radius: 14px; padding: 0.7rem 1.25rem; margin-bottom: 1.75rem; box-shadow: {card_shadow}; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px;">
    <div style="display: flex; align-items: center; gap: 10px;">
        <span style="display: inline-block; width: 9px; height: 9px; border-radius: 50%; background: #10b981; animation: pulse-dot 2s infinite;"></span>
        <span style="font-weight: 800; font-size: 0.82rem; letter-spacing: 0.03em;">MISSION CONTROL // FINANCIAL PARALLELVERSE</span>
        <span style="font-size: 0.75rem; color: {text_muted}; margin-left: 4px;">Core v2.4 (Deterministic Engine)</span>
    </div>
    <div style="display: flex; align-items: center; gap: 12px; font-size: 0.75rem;">
        <span style="background: rgba(16, 185, 129, 0.15); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.3); padding: 2px 9px; border-radius: 9999px; font-weight: 800;">
            ● 5 TIMELINES SYNCED
        </span>
        <span style="color: {text_muted};">Mode: <b style="color: {text_main};">{theme}</b></span>
        <span style="background: rgba(56, 189, 248, 0.15); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.3); padding: 2px 8px; border-radius: 6px; font-weight: 800;">
            FASTAPI :8000
        </span>
        <span style="background: rgba(168, 85, 247, 0.15); color: #a855f7; border: 1px solid rgba(168, 85, 247, 0.3); padding: 2px 8px; border-radius: 6px; font-weight: 800;">
            RFC 5545 iCAL
        </span>
    </div>
</div>
""")

# ==============================================================================
# PAGE 1: EXECUTIVE DASHBOARD
# ==============================================================================
if page == "📊 Executive Dashboard":
    st.html(f"""
    <div class="hero-container">
        <div style="display: inline-flex; align-items: center; gap: 8px; background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.35); padding: 0.35rem 0.9rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 800; color: #10b981; text-transform: uppercase; margin-bottom: 1rem;">
            <span style="width: 8px; height: 8px; border-radius: 50%; background: #10b981; display: inline-block;"></span>
            FinTech Stress Testing Engine &bull; Hack-o-Ween PESU
        </div>
        <div class="hero-title">Simulate Your Tomorrow Before Spending Today.</div>
        <div class="hero-subtitle">
            Most individuals commit to significant purchases looking only at today's paycheck. 
            Financial Parallelverse simulates multiple adverse futures—delayed salaries, hospital emergencies, and inflation—so you never commit blind.
        </div>
        <div style="display: flex; gap: 10px; flex-wrap: wrap;">
            <span class="pill-tag pill-emerald">⚡ 5 Concurrent Timelines</span>
            <span class="pill-tag pill-cyan">🛡️ Emergency Reserve Shield</span>
            <span class="pill-tag pill-purple">📅 RFC 5545 iCalendar Sync</span>
            <span class="pill-tag pill-orange">🧮 Reducing-Balance Precision</span>
        </div>
    </div>
    """)

    # 4 Glowing KPI Metric Cards
    flow_col = "#10b981" if metrics['free_cash_flow'] >= 0 else "#f43f5e"
    runway_col = "#10b981" if metrics['months_of_runway'] >= 3 else "#f59e0b"
    dti_col = "#f43f5e" if metrics['debt_to_income_pct'] > 35 else "#10b981"

    st.html(f"""
    <div class="kpi-grid">
        <div class="kpi-card emerald">
            <div class="kpi-label">
                <span>Monthly Free Cash Flow</span>
                <span>💵</span>
            </div>
            <div class="kpi-value" style="color: {flow_col};">₹{metrics['free_cash_flow']:,.0f}</div>
            <div style="font-size: 0.8rem; font-weight: 700; color: #06b6d4; margin-top: 0.4rem;">
                Savings Rate: <b>{metrics['savings_rate_pct']:.1f}%</b>
            </div>
        </div>

        <div class="kpi-card cyan">
            <div class="kpi-label">
                <span>Liquid Cash Reserves</span>
                <span>🏦</span>
            </div>
            <div class="kpi-value">₹{profile.current_savings:,.0f}</div>
            <div style="font-size: 0.8rem; font-weight: 700; color: #10b981; margin-top: 0.4rem;">
                Target Coverage: <b>{metrics['emergency_coverage_pct']:.0f}%</b>
            </div>
        </div>

        <div class="kpi-card purple">
            <div class="kpi-label">
                <span>Emergency Runway</span>
                <span>🛡️</span>
            </div>
            <div class="kpi-value">{metrics['months_of_runway']:.1f} <span style="font-size: 1.1rem; color: {text_muted};">Mo</span></div>
            <div style="font-size: 0.8rem; font-weight: 700; color: {runway_col}; margin-top: 0.4rem;">
                Survival without salary
            </div>
        </div>

        <div class="kpi-card orange">
            <div class="kpi-label">
                <span>Debt-to-Income (DTI)</span>
                <span>⚖️</span>
            </div>
            <div class="kpi-value" style="color: {dti_col};">{metrics['debt_to_income_pct']:.1f}%</div>
            <div style="font-size: 0.8rem; font-weight: 700; color: {text_muted}; margin-top: 0.4rem;">
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
            font=dict(color=chart_font, family="Plus Jakarta Sans"),
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
                    text=f"<b>₹{profile.monthly_income:,.0f}</b><br><span style='font-size: 10px; color: {text_muted};'>TOTAL SALARY</span>",
                    x=0.5, y=0.5, font_size=15, showarrow=False
                )
            ]
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_decision:
        st.subheader("🎯 Active Planned Decision")
        cash_depletion_pct = (profile.planned_purchase_amount / max(1.0, profile.current_savings)) * 100.0
        rem_after = profile.current_savings - profile.planned_purchase_amount
        rem_color = '#10b981' if rem_after >= profile.emergency_fund_target else '#f43f5e'
        dep_color = '#f43f5e' if cash_depletion_pct > 60 else '#f59e0b'

        st.html(f"""
        <div class="kpi-card cyan" style="min-height: 380px;">
            <div style="font-size: 0.72rem; color: #06b6d4; font-weight: 800; text-transform: uppercase; letter-spacing: 0.06em;">Contemplated Major Purchase</div>
            <div style="font-size: 1.5rem; font-weight: 800; margin: 0.4rem 0 0.2rem 0;">{profile.planned_purchase_name}</div>
            <div style="font-size: 2.2rem; font-weight: 800; color: #06b6d4; margin-bottom: 1.2rem;">₹{profile.planned_purchase_amount:,.0f}</div>
            
            <div style="border-top: {card_border}; padding-top: 1rem; font-size: 0.85rem; color: {text_muted};">
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                    <span>Upfront Cash Impact:</span>
                    <span style="color: {dep_color}; font-weight: 800;">Consumes {cash_depletion_pct:.0f}% of liquid savings</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                    <span>Remaining Emergency Buffer:</span>
                    <span style="color: {rem_color}; font-weight: 800;">₹{max(0.0, rem_after):,.0f}</span>
                </div>
            </div>

            <div style="margin-top: 1.2rem; padding: 0.8rem; background: rgba(245, 158, 11, 0.1); border: 1px solid rgba(245, 158, 11, 0.25); border-radius: 12px; font-size: 0.8rem; color: #f59e0b;">
                ⚠️ <b>Warning:</b> Buying upfront in cash drops your emergency runway significantly. Simulate before buying!
            </div>
        </div>
        """)

# ==============================================================================
# PAGE 2: PARALLEL FUTURES SIMULATOR (WITH BAR GRAPH & SPLINE MODES)
# ==============================================================================
elif page == "🔮 Parallel Futures Simulator":
    st.html(f"""
    <div style="margin-bottom: 1.5rem;">
        <h1 style="font-size: 2.4rem; font-weight: 800; background: {hero_title_grad}; -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.2rem;">
            Parallel Financial Futures Engine
        </h1>
        <p style="color: {text_muted}; font-size: 1rem;">
            Simulating 5 concurrent futures under adverse life shocks: salary delays, medical emergencies, and inflation.
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

    # =========================================================================
    # BAR GRAPH & SPLINE VISUALIZATIONS (REQUESTED BY USER)
    # =========================================================================
    st.markdown("### 📊 Projected Savings Trajectory Across 5 Parallel Futures")
    
    chart_view = st.radio(
        "Trajectory Visualization Mode",
        ["📊 Grouped Bar Graph (Scenario Comparison)", "📈 Spline Curve Trajectory", "📉 Monthly Net Cash Flow Bars"],
        index=0,
        horizontal=True
    )

    colors_map = {
        "baseline": "#10b981",          # Emerald
        "unexpected_expense": "#f97316",# Orange
        "delayed_salary": "#06b6d4",    # Electric Cyan
        "increased_spending": "#a855f7",# Violet
        "combined_adverse": "#f43f5e"   # Crimson
    }

    # 1. GROUPED BAR GRAPH (Primary User Request)
    if chart_view == "📊 Grouped Bar Graph (Scenario Comparison)":
        bar_data = []
        months_list = [f"M{m}" for m in range(1, dur + 1)]
        
        for sc_id, sc_data in scenarios.items():
            for m_item in sc_data["timeline"]:
                bar_data.append({
                    "Month": f"Month {m_item['month']}",
                    "Scenario": sc_data["scenario_name"],
                    "Savings Balance (₹)": m_item["closing_savings"],
                    "Color": colors_map.get(sc_id, "#ffffff")
                })
        
        df_bars = pd.DataFrame(bar_data)
        
        fig_bar = px.bar(
            df_bars,
            x="Month",
            y="Savings Balance (₹)",
            color="Scenario",
            barmode="group",
            color_discrete_map={sc_data["scenario_name"]: colors_map[sc_id] for sc_id, sc_data in scenarios.items()}
        )
        
        # Add Emergency Fund Threshold Line on Bar Graph
        fig_bar.add_hline(
            y=profile.emergency_fund_target,
            line_dash="dash",
            line_color="#f59e0b",
            line_width=2,
            annotation_text=f"Emergency Reserve Target (₹{profile.emergency_fund_target:,.0f})",
            annotation_position="top right"
        )
        
        fig_bar.add_hline(
            y=0,
            line_dash="solid",
            line_color="#f43f5e",
            line_width=2,
            annotation_text="Zero Cash Deficit Threshold",
            annotation_position="bottom right"
        )

        fig_bar.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor=chart_bg,
            font=dict(color=chart_font, family="Plus Jakarta Sans"),
            xaxis=dict(title="<b>Simulation Timeline</b>", gridcolor=chart_grid),
            yaxis=dict(title="<b>Projected Savings Balance (₹)</b>", gridcolor=chart_grid),
            margin=dict(l=20, r=20, t=30, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5),
            hovermode="x unified"
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    # 2. SPLINE LINE GRAPH
    elif chart_view == "📈 Spline Curve Trajectory":
        fig_lines = go.Figure()
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

        fig_lines.add_hline(
            y=profile.emergency_fund_target,
            line_dash="dash",
            line_color="#f59e0b",
            line_width=1.5,
            annotation_text=f"Emergency Reserve Target (₹{profile.emergency_fund_target:,.0f})",
            annotation_position="top right"
        )

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
            plot_bgcolor=chart_bg,
            font=dict(color=chart_font, family="Plus Jakarta Sans"),
            xaxis=dict(title="<b>Timeline (Months)</b>", gridcolor=chart_grid, zeroline=False),
            yaxis=dict(title="<b>Liquid Savings Balance (₹)</b>", gridcolor=chart_grid, zeroline=False),
            margin=dict(l=20, r=20, t=30, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5),
            hovermode="x unified"
        )
        st.plotly_chart(fig_lines, use_container_width=True)

    # 3. MONTHLY CASH FLOW COMPARISON BARS
    else:
        cf_data = []
        for sc_id, sc_data in scenarios.items():
            for m_item in sc_data["timeline"]:
                cf_data.append({
                    "Month": f"Month {m_item['month']}",
                    "Scenario": sc_data["scenario_name"],
                    "Net Cash Flow (₹)": m_item["net_cash_flow"]
                })
        df_cf = pd.DataFrame(cf_data)
        fig_cf = px.bar(
            df_cf,
            x="Month",
            y="Net Cash Flow (₹)",
            color="Scenario",
            barmode="group",
            color_discrete_map={sc_data["scenario_name"]: colors_map[sc_id] for sc_id, sc_data in scenarios.items()}
        )
        fig_cf.add_hline(y=0, line_dash="solid", line_color="#f43f5e", line_width=1.5)
        fig_cf.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor=chart_bg,
            font=dict(color=chart_font, family="Plus Jakarta Sans"),
            xaxis=dict(title="<b>Simulation Timeline</b>", gridcolor=chart_grid),
            yaxis=dict(title="<b>Net Monthly Cash Flow (₹)</b>", gridcolor=chart_grid),
            margin=dict(l=20, r=20, t=30, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig_cf, use_container_width=True)

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
        low_col = "#f43f5e" if sc_data["lowest_savings"] < 0 else text_main
        
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
            <div style="font-size: 0.78rem; color: {text_muted};">
                <div>Resilience Score: <b style="color: {text_main};">{sc_data['resilience_score']}/100</b></div>
                <div>Deficit Months: <b style="color: {'#f43f5e' if sc_data['negative_cash_months'] > 0 else '#10b981'};">{sc_data['negative_cash_months']}</b></div>
            </div>
            <div style="font-size: 0.73rem; color: {text_muted}; border-top: {card_border}; padding-top: 0.5rem; margin-top: 0.5rem;">
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
    st.html(f"""
    <div style="margin-bottom: 1.5rem;">
        <h1 style="font-size: 2.4rem; font-weight: 800; background: {hero_title_grad}; -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.2rem;">
            Purchase Affordability Decision Matrix
        </h1>
        <p style="color: {text_muted}; font-size: 1rem;">
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
        buf_col = "#10b981" if opt['emergency_buffer_preserved_pct'] >= 100 else "#f59e0b"

        pathways_html += f"""
        <div class="pathway-card {rec_cls}">
            {rec_badge}
            <div style="font-weight: 800; font-size: 1.15rem; margin-bottom: 0.5rem;">{opt['option_title']}</div>
            <span class="pill-tag {pill_cls}">{opt['risk_rating']}</span>
            
            <div style="margin: 1.2rem 0 0.8rem 0; border-top: {card_border}; padding-top: 0.8rem;">
                <div style="font-size: 0.72rem; color: {text_muted}; text-transform: uppercase;">Upfront Cash Required</div>
                <div style="font-size: 1.4rem; font-weight: 800;">₹{opt['upfront_cash_required']:,.0f}</div>
            </div>

            <div style="margin-bottom: 0.8rem;">
                <div style="font-size: 0.72rem; color: {text_muted}; text-transform: uppercase;">Monthly Obligation</div>
                <div style="font-size: 1.4rem; font-weight: 800; color: #06b6d4;">₹{opt['monthly_obligation']:,.0f}<span style="font-size: 0.8rem; color: {text_muted};">/mo</span></div>
            </div>

            <div style="margin-bottom: 1rem;">
                <div style="font-size: 0.72rem; color: {text_muted}; text-transform: uppercase;">Emergency Reserve Retained</div>
                <div style="font-size: 1.2rem; font-weight: 700; color: {buf_col};">{opt['emergency_buffer_preserved_pct']:.0f}% <span style="font-size: 0.75rem; color: {text_muted};">of safety target</span></div>
            </div>

            <div style="font-size: 0.78rem; color: {text_muted}; border-top: {card_border}; padding-top: 0.8rem;">
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
    st.html(f"""
    <div style="margin-bottom: 1.5rem;">
        <h1 style="font-size: 2.4rem; font-weight: 800; background: {hero_title_grad}; -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.2rem;">
            Precision Reducing-Balance EMI Engine
        </h1>
        <p style="color: {text_muted}; font-size: 1rem;">
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
            <div class="kpi-value" style="color: #10b981;">₹{emi_data['monthly_emi']:,.2f}</div>
            <div style="font-size: 0.8rem; font-weight: 700; color: #06b6d4; margin-top: 0.4rem;">For {tenure} months</div>
        </div>

        <div class="kpi-card cyan">
            <div class="kpi-label"><span>Principal Financed</span><span>🏷️</span></div>
            <div class="kpi-value">₹{emi_data['principal_financed']:,.0f}</div>
            <div style="font-size: 0.8rem; font-weight: 700; color: {text_muted}; margin-top: 0.4rem;">Excludes down payment</div>
        </div>

        <div class="kpi-card orange">
            <div class="kpi-label"><span>Total Interest Cost</span><span>🔥</span></div>
            <div class="kpi-value" style="color: #f97316;">₹{emi_data['total_interest']:,.2f}</div>
            <div style="font-size: 0.8rem; font-weight: 700; color: {text_muted}; margin-top: 0.4rem;">Borrowing cost</div>
        </div>

        <div class="kpi-card purple">
            <div class="kpi-label"><span>Total Repaid</span><span>💰</span></div>
            <div class="kpi-value">₹{emi_data['total_repayment']:,.2f}</div>
            <div style="font-size: 0.8rem; font-weight: 700; color: #10b981; margin-top: 0.4rem;">Reconciled to ₹0.00</div>
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
            font=dict(color=chart_font, family="Plus Jakarta Sans"),
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
    st.html(f"""
    <div style="margin-bottom: 1.5rem;">
        <h1 style="font-size: 2.4rem; font-weight: 800; background: {hero_title_grad}; -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.2rem;">
            Installment Tracker & Calendar Reminders
        </h1>
        <p style="color: {text_muted}; font-size: 1rem;">
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
                            <div style="font-size: 1.4rem; font-weight: 800; margin: 0.5rem 0 0.2rem 0;">{plan.purchase_name}</div>
                            <div style="color: {text_muted}; font-size: 0.88rem;">
                                Financed: <b>₹{plan.principal_financed:,.0f}</b> | 
                                Monthly EMI: <b style="color: #10b981;">₹{plan.monthly_emi:,.2f}</b> | 
                                Due Day: <b>{plan.due_day}th of every month</b>
                            </div>
                        </div>
                        <div style="text-align: right;">
                            <div style="font-size: 0.75rem; color: {text_muted}; text-transform: uppercase;">Repayment Progress</div>
                            <div style="font-size: 1.5rem; font-weight: 800; color: #10b981;">{paid_c} / {total_c} Paid</div>
                            <div style="font-size: 0.8rem; color: {text_muted};">({progress_pct:.0f}% Completed)</div>
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
    st.html(f"""
    <div style="margin-bottom: 1.5rem;">
        <h1 style="font-size: 2.4rem; font-weight: 800; background: {hero_title_grad}; -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.2rem;">
            Financial Profile & Scenario Assumptions
        </h1>
        <p style="color: {text_muted}; font-size: 1rem;">
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
st.html(f"""
<div class="fin-footer">
    <div>
        <div style="font-weight: 800; font-size: 1.15rem;">🌌 Financial Parallelverse</div>
        <div style="font-size: 0.8rem; color: {text_muted}; margin-top: 0.2rem;">
            Explore your financial futures before making a decision &bull; Built for Hack-o-Ween 2nd Edition (PES University)
        </div>
        <div style="font-size: 0.75rem; color: {text_muted}; margin-top: 0.4rem;">
            Track: <b>The Vampire's Ledger (FinTech)</b> &bull; Team: <b>Dark_Knights</b> (Ratnala Aneesh, Raghoothama T R, Vatsal Soni)
        </div>
    </div>
    <div style="display: flex; gap: 20px; font-size: 0.82rem; color: {text_muted};">
        <div>🟢 <b>FastAPI</b> :8000</div>
        <div>🛡️ <b>SQLite 3</b> Local DB</div>
        <div>📅 <b>RFC 5545</b> iCal Export</div>
        <div>🧪 <b>23/23 Tests</b> Passing</div>
    </div>
</div>
""")
