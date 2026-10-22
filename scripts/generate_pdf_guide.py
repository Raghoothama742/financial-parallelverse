import os
import sys
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)

def create_guide_pdf():
    base_dir = Path(__file__).resolve().parent.parent
    pdf_path = base_dir / "Financial_Parallelverse_Execution_Guide.pdf"

    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    # Custom color palette (Midnight Navy & Emerald)
    c_primary = colors.HexColor("#0f172a")     # Midnight
    c_accent = colors.HexColor("#059669")      # Emerald
    c_secondary = colors.HexColor("#0284c7")   # Cyan/Blue
    c_dark = colors.HexColor("#1e293b")        # Slate Dark
    c_light = colors.HexColor("#f8fafc")       # Off-white
    c_muted = colors.HexColor("#64748b")       # Slate Muted
    c_border = colors.HexColor("#cbd5e1")      # Border gray

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=c_accent,
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=c_muted,
        spaceAfter=12
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=c_primary,
        spaceBefore=14,
        spaceAfter=6
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=c_secondary,
        spaceBefore=8,
        spaceAfter=4
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=c_dark,
        spaceAfter=6
    )

    code_style = ParagraphStyle(
        'Code_Custom',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor("#0f172a"),
        backColor=colors.HexColor("#f1f5f9"),
        borderPadding=4,
        spaceAfter=6
    )

    badge_style = ParagraphStyle(
        'Badge',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=10,
        textColor=colors.white
    )

    elements = []

    # =========================================================================
    # HEADER BANNER & METADATA
    # =========================================================================
    header_data = [
        [
            Paragraph("<b>HACK-O-WEEN — 2nd Edition (PES University)</b><br/>Track: <b>The Vampire's Ledger (FinTech)</b>", ParagraphStyle('H1', parent=body_style, textColor=colors.white, fontSize=9)),
            Paragraph("Team: <b>Dark_Knights</b><br/>Ratnala Aneesh | Raghoothama T R | Vatsal Soni", ParagraphStyle('H2', parent=body_style, textColor=colors.white, alignment=2, fontSize=9))
        ]
    ]
    header_table = Table(header_data, colWidths=[270, 260])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_primary),
        ('PADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    elements.append(header_table)
    elements.append(Spacer(1, 15))

    # Title & Tagline
    elements.append(Paragraph("Financial Parallelverse", title_style))
    elements.append(Paragraph("<b>Complete System Execution & Demonstration Manual</b> &mdash; Explore your financial futures before making a decision.", subtitle_style))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=c_accent, spaceBefore=2, spaceAfter=12))

    # Executive Overview
    elements.append(Paragraph("1. Executive Summary & Problem Solved", h1_style))
    elements.append(Paragraph(
        "Standard EMI calculators only compute flat repayments based on static assumptions. They fail to warn users what happens when real life strikes: a delayed paycheck, sudden hospital bills, or unexpected inflation. <b>Financial Parallelverse</b> solves this by running <b>5 concurrent deterministic simulations</b>, identifying financial breaking points, comparing purchase pathways (Cash vs. Save-and-Wait vs. Cheaper Alternative vs. EMI), and generating downloadable <b>iCalendar (.ics) reminders</b> for scheduled installments.",
        body_style
    ))

    # Architecture Table
    arch_data = [
        [Paragraph("<b>Component</b>", body_style), Paragraph("<b>Technology</b>", body_style), Paragraph("<b>Port / Location</b>", body_style), Paragraph("<b>Role</b>", body_style)],
        [Paragraph("FastAPI Backend", body_style), Paragraph("Python 3.13 / Uvicorn", body_style), Paragraph("http://localhost:8000", body_style), Paragraph("REST API & Simulation Logic", body_style)],
        [Paragraph("Interactive Dashboard", body_style), Paragraph("Streamlit + Plotly", body_style), Paragraph("http://localhost:8501", body_style), Paragraph("Primary Fintech User Interface", body_style)],
        [Paragraph("Database Engine", body_style), Paragraph("SQLite / SQLAlchemy 2.x", body_style), Paragraph("data/financial_parallelverse.db", body_style), Paragraph("Profile & Installment Persistence", body_style)],
        [Paragraph("Test Suite", body_style), Paragraph("Pytest", body_style), Paragraph("23 Automated Test Cases", body_style), Paragraph("Engine & API Reconciliation", body_style)],
    ]
    arch_table = Table(arch_data, colWidths=[110, 110, 130, 180])
    arch_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#e2e8f0")),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    elements.append(arch_table)
    elements.append(Spacer(1, 14))

    # =========================================================================
    # STEP-BY-STEP EXECUTION ORDER
    # =========================================================================
    elements.append(Paragraph("2. Step-by-Step Execution Order", h1_style))
    elements.append(Paragraph("Follow these steps sequentially to launch and verify the complete application:", body_style))

    steps = [
        ("Step 1: Open the Project Directory", "Open PowerShell or Command Prompt and navigate to the project directory on your desktop:", "cd \"C:\\Users\\Raghoothama T R\\Desktop\\Financial_Parallelverse\""),
        ("Step 2: Seed Demo Database", "Populate the SQLite database with realistic profile values and initial EMI installment plans:", "python scripts/seed_demo.py"),
        ("Step 3: Run the 23-Test Verification Suite", "Execute the comprehensive Pytest suite to mathematically verify all financial and EMI algorithms:", "python -m pytest backend/tests -v\n# Or double-click: run_tests.bat"),
        ("Step 4: Launch the FastAPI Backend Service", "Start the FastAPI application. Access OpenAPI documentation at <u>http://localhost:8000/api/docs</u>:", "python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload\n# Or double-click: run_backend.bat"),
        ("Step 5: Launch the Streamlit FinTech Application", "Open a second terminal window and start the primary Streamlit frontend:", "python -m streamlit run frontend_streamlit/app.py --server.port 8501\n# Or double-click: run_streamlit.bat"),
        ("ONE-CLICK LAUNCHER (Alternative)", "To automatically launch both the backend and frontend in separate dedicated windows, run:", "run_all.bat")
    ]

    for title, desc, code in steps:
        elements.append(Paragraph(f"<b>{title}</b>", h2_style))
        elements.append(Paragraph(desc, body_style))
        elements.append(Paragraph(code.replace("\n", "<br/>"), code_style))

    elements.append(PageBreak())

    # =========================================================================
    # FEATURE WALKTHROUGH FOR LIVE DEMO
    # =========================================================================
    elements.append(Paragraph("3. Feature Walkthrough & Hackathon Demonstration Guide", h1_style))
    elements.append(Paragraph(
        "Use this sequence during your presentation to demonstrate the novelty and polish of the application to the judges:",
        body_style
    ))

    features = [
        ("1. Overview Dashboard", "Displays key financial vitals: Monthly Free Cash Flow, Current Savings, Emergency Runway (Months), and Debt-to-Income (DTI). Features an interactive inflow/outflow donut chart showing exactly where monthly income goes."),
        ("2. Parallel Futures Simulator (Core Innovation)", "Simulates 5 parallel timelines across a 6–24 month horizon:<br/>"
         "&bull; <b>Baseline Reality</b>: Normal conditions.<br/>"
         "&bull; <b>Emergency Medical Shock</b>: Sudden ₹25,000 out-of-pocket expense in Month 3.<br/>"
         "&bull; <b>Delayed Salary Flow</b>: Timing shift where a paycheck is delayed for 1 month.<br/>"
         "&bull; <b>Cost of Living Inflation</b>: 15% increase in monthly essential & discretionary expenses.<br/>"
         "&bull; <b>Parallel Nightmare</b>: Triple adverse shock.<br/>"
         "Visualized using interactive multi-line Plotly graphs with the minimum emergency buffer line and automated breaking-point alerts."),
        ("3. Purchase Affordability Decision Matrix", "Evaluates acquiring a ₹70,000 laptop via 4 pathways: Buy Now with Cash, Save First & Buy Later, Buy a Cheaper Alternative (₹42,000), or Buy via EMI. Shows safety ratings, emergency buffer impact, and trade-off analysis."),
        ("4. Reducing-Balance EMI & Amortization Calculator", "Computes exact EMI using standard mathematical formulas. Reconciles monthly interest and principal down to ₹0.00 final balance, supporting zero-interest loans and early prepayments."),
        ("5. Installment Tracker & One-Click Calendar (.ICS) Reminders", "Displays active EMI plans with progress bars, due dates, and overdue status detection. Features a <b>Download Calendar (.ICS) Reminders</b> button to import reminders directly into Google Calendar, Apple Calendar, or Outlook."),
        ("6. Financial Profile Persistence", "Allows editing and saving monthly income, expenses, debts, and emergency targets with instant persistence to SQLite.")
    ]

    for title, desc in features:
        elements.append(Paragraph(f"<b>{title}</b>", h2_style))
        elements.append(Paragraph(desc, body_style))

    elements.append(Spacer(1, 10))

    # =========================================================================
    # FASTAPI ENDPOINTS SUMMARY
    # =========================================================================
    elements.append(Paragraph("4. Backend REST API Contract", h1_style))
    api_data = [
        [Paragraph("<b>Method</b>", body_style), Paragraph("<b>Endpoint</b>", body_style), Paragraph("<b>Description</b>", body_style)],
        [Paragraph("GET", body_style), Paragraph("/api/health", body_style), Paragraph("Health check & service status", body_style)],
        [Paragraph("GET / PUT", body_style), Paragraph("/api/profile", body_style), Paragraph("Retrieve and update user financial profile", body_style)],
        [Paragraph("POST", body_style), Paragraph("/api/scenarios/simulate", body_style), Paragraph("Execute 5-timeline parallel future simulation", body_style)],
        [Paragraph("POST", body_style), Paragraph("/api/purchases/evaluate", body_style), Paragraph("Evaluate 4-way purchase affordability options", body_style)],
        [Paragraph("POST", body_style), Paragraph("/api/emi/calculate", body_style), Paragraph("Calculate reducing-balance loan amortization", body_style)],
        [Paragraph("GET / POST", body_style), Paragraph("/api/installments", body_style), Paragraph("List all plans or create a new installment plan", body_style)],
        [Paragraph("PATCH", body_style), Paragraph("/api/installments/{id}/payments/{pid}", body_style), Paragraph("Mark installment payment as PAID or PENDING", body_style)],
        [Paragraph("GET", body_style), Paragraph("/api/installments/{id}/calendar", body_style), Paragraph("Generate and download .ics calendar reminder file", body_style)],
    ]
    api_table = Table(api_data, colWidths=[70, 200, 260])
    api_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#e2e8f0")),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('PADDING', (0,0), (-1,-1), 4.5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    elements.append(api_table)

    elements.append(Spacer(1, 14))

    # =========================================================================
    # VERIFICATION & TEST RESULTS
    # =========================================================================
    elements.append(Paragraph("5. Quality Assurance & Test Verification", h1_style))
    elements.append(Paragraph(
        "The application has been tested against 23 automated unit and integration tests covering: "
        "income-to-expense ratios, cash deficit breaking points, emergency fund depletion, zero-interest loans, reducing-balance mathematical reconciliation, month-end date clamping (Feb 28, Apr 30), and .ics calendar generation. "
        "<b>Result: 23 passed, 0 failed.</b>",
        body_style
    ))

    # Footer note
    elements.append(Spacer(1, 15))
    elements.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=4, spaceAfter=8))
    elements.append(Paragraph("<i>Financial Parallelverse &bull; Built for Hack-o-Ween 2026 &bull; Dark_Knights Team</i>", ParagraphStyle('Footer', parent=body_style, textColor=c_muted, alignment=1, fontSize=8)))

    doc.build(elements)
    print(f"PDF generated successfully at: {pdf_path}")

if __name__ == "__main__":
    create_guide_pdf()
