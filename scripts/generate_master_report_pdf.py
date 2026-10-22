import os
import sys
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)

def build_master_pdf():
    base_dir = Path(__file__).resolve().parent.parent
    pdf_path = base_dir / "Financial_Parallelverse_Master_Report.pdf"
    desktop_path = Path("C:/Users/Raghoothama T R/Desktop/Financial_Parallelverse_Master_Report.pdf")

    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    # Brand Colors
    c_primary = colors.HexColor("#090e1a")     # Deep Obsidian Navy
    c_emerald = colors.HexColor("#059669")     # Vibrant Emerald
    c_cyan = colors.HexColor("#0284c7")        # Cyan Blue
    c_dark = colors.HexColor("#1e293b")        # Slate Text
    c_light = colors.HexColor("#f8fafc")       # Off-White
    c_muted = colors.HexColor("#64748b")       # Secondary Slate
    c_border = colors.HexColor("#cbd5e1")      # Border Gray
    c_danger = colors.HexColor("#e11d48")      # Rose Danger

    # Typography Styles
    title_style = ParagraphStyle(
        'MainTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=c_emerald,
        spaceAfter=3
    )

    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=c_cyan,
        spaceAfter=10
    )

    meta_style = ParagraphStyle(
        'Meta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=c_muted,
        spaceAfter=12
    )

    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12.5,
        leading=16.5,
        textColor=c_primary,
        spaceBefore=12,
        spaceAfter=5
    )

    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13.5,
        textColor=c_emerald,
        spaceBefore=7,
        spaceAfter=3
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.8,
        leading=12.5,
        textColor=c_dark,
        spaceAfter=5
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=c_dark,
        leftIndent=12,
        spaceAfter=3
    )

    code_style = ParagraphStyle(
        'Code',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#0f172a"),
        backColor=colors.HexColor("#f1f5f9"),
        borderPadding=3,
        spaceAfter=5
    )

    elements = []

    # =========================================================================
    # HEADER BANNER
    # =========================================================================
    header_data = [
        [
            Paragraph("<b>HACK-O-WEEN 2nd Edition &bull; PES UNIVERSITY</b><br/>Track: <b>The Vampire's Ledger (FinTech)</b>", ParagraphStyle('Hdr1', parent=body_style, textColor=colors.white, fontSize=8.5)),
            Paragraph("Team: <b>Dark_Knights</b><br/>Ratnala Aneesh &bull; Raghoothama T R &bull; Vatsal Soni", ParagraphStyle('Hdr2', parent=body_style, textColor=colors.white, alignment=2, fontSize=8.5))
        ]
    ]
    hdr_table = Table(header_data, colWidths=[270, 270])
    hdr_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_primary),
        ('PADDING', (0,0), (-1,-1), 7),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    elements.append(hdr_table)
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("Financial Parallelverse", title_style))
    elements.append(Paragraph("Complete Project Architecture, Engineering & Mathematical Deep-Dive", subtitle_style))
    elements.append(Paragraph("<b>Product Vision:</b> Explore your financial futures before making a decision &mdash; Deterministic Multi-Timeline Simulation Engine.", meta_style))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=c_emerald, spaceBefore=0, spaceAfter=10))

    # =========================================================================
    # 1. THE PROBLEM & NOVELTY
    # =========================================================================
    elements.append(Paragraph("1. Executive Summary & Problem Solved", h1_style))
    elements.append(Paragraph(
        "<b>The FinTech Problem:</b> Most young professionals, college students, and first-time loan applicants evaluate affordability solely on whether the monthly EMI fits within their current monthly salary. This creates a critical blind spot known in finance as <i>tail-risk vulnerability</i>. If a person commits to an EMI of ₹5,686/month for a ₹70,000 laptop, standard calculators confirm they have sufficient salary today. But what happens if their company delays salaries by 30 days? What if a medical emergency demands ₹25,000 in Month 3? What if inflation increases daily living expenses by 15%? Conventional calculators cannot answer these life-altering questions.",
        body_style
    ))
    elements.append(Paragraph(
        "<b>The Innovation (Financial Parallelverse):</b> Our application takes a user's real or hypothetical financial situation and simultaneously projects <b>5 concurrent deterministic futures</b> over a 6 to 24 month timeline. It introduces <b>Financial Breaking-Point Detection</b> (which identifies the exact month when savings turn negative or dip below emergency thresholds), evaluates <b>4 distinct purchase pathways</b>, and generates <b>downloadable iCalendar (.ics) reminders</b> for scheduled installments.",
        body_style
    ))

    # Architecture Overview Table
    tech_data = [
        [Paragraph("<b>Layer</b>", body_style), Paragraph("<b>Technology</b>", body_style), Paragraph("<b>Key Responsibilities</b>", body_style)],
        [Paragraph("<b>Backend API</b>", body_style), Paragraph("Python 3.13 / FastAPI / Uvicorn", body_style), Paragraph("REST API endpoints, Pydantic request validation, CORS, OpenAPI docs.", body_style)],
        [Paragraph("<b>Financial Engine</b>", body_style), Paragraph("Deterministic Python Algorithms", body_style), Paragraph("Reducing-balance EMI formula, free cash flow, breaking point detection.", body_style)],
        [Paragraph("<b>Primary UI</b>", body_style), Paragraph("Streamlit + Plotly + Custom CSS", body_style), Paragraph("High-end Midnight/Emerald SaaS theme, interactive multi-line charts.", body_style)],
        [Paragraph("<b>Alternative UI</b>", body_style), Paragraph("React 18 + TypeScript + Vite", body_style), Paragraph("Full enterprise client code in frontend_react/ connecting to REST API.", body_style)],
        [Paragraph("<b>Database</b>", body_style), Paragraph("SQLite + SQLAlchemy 2.x", body_style), Paragraph("Persistent profiles, active loan plans, and month-by-month payment tracking.", body_style)],
        [Paragraph("<b>Calendar Sync</b>", body_style), Paragraph("Python RFC 5545 iCalendar (.ics)", body_style), Paragraph("Exportable calendar files with VALARM notifications for phones/Google Cal.", body_style)],
    ]
    t_table = Table(tech_data, colWidths=[90, 150, 300])
    t_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('PADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    elements.append(t_table)
    elements.append(Spacer(1, 10))

    # =========================================================================
    # 2. MATHEMATICAL & FINANCIAL FORMULAS
    # =========================================================================
    elements.append(Paragraph("2. Mathematical Formulations & Financial Algorithms", h1_style))
    elements.append(Paragraph(
        "Unlike AI wrappers that hallucinate numbers, all calculations in Financial Parallelverse are <b>100% deterministic</b>, mathematically verified, and reproducible:",
        body_style
    ))

    formulas = [
        ("A. Reducing-Balance EMI Formula", 
         "For a financed principal <i>P</i> (Purchase Price &minus; Down Payment), monthly interest rate <i>r = (Annual Rate / 12) / 100</i>, and tenure of <i>n</i> months:<br/>"
         "<b>EMI = P &times; r &times; (1 + r)<sup>n</sup> / ((1 + r)<sup>n</sup> &minus; 1)</b><br/>"
         "When <i>r = 0</i> (Zero-Cost EMI): <b>EMI = P / n</b>.<br/>"
         "In each month <i>m</i>: Interest Portion = Balance &times; r; Principal Paid = EMI &minus; Interest Portion. Final month balance reconciles to exactly ₹0.00."),
        
        ("B. Cash Flow Dynamics & Runway Metrics",
         "&bull; <b>Monthly Free Cash Flow:</b> Income &minus; (Essential Expenses + Discretionary Expenses + Existing Debt EMIs)<br/>"
         "&bull; <b>Savings Rate %:</b> (Free Cash Flow / Monthly Income) &times; 100<br/>"
         "&bull; <b>Emergency Runway (Months):</b> Liquid Savings / (Essential Expenses + Existing Debt EMIs)<br/>"
         "&bull; <b>Debt-to-Income (DTI) %:</b> (Existing Loan EMIs / Monthly Income) &times; 100 (Safe threshold: &lt; 35%)"),
        
        ("C. Month-by-Month Deterministic Simulation Order",
         "1. Opening Savings(m) = Closing Savings(m &minus; 1) [Month 1 Opening = Current Savings]<br/>"
         "2. Income Received(m): Set to ₹0 if salary is delayed; double income arrives upon catch-up.<br/>"
         "3. Routine Expenses(m): (Essential + Discretionary) &times; Inflation Multiplier.<br/>"
         "4. Debt & Purchase Outflows(m): Existing EMI + New Purchase Payment (Down payment in M1, EMI thereafter).<br/>"
         "5. Emergency Shock(m): Charged exclusively in the specified shock month (e.g. Month 3).<br/>"
         "6. Closing Savings(m) = Opening + Inflows &minus; All Outflows.<br/>"
         "7. Breaking Point: Triggered immediately if Closing Savings &lt; 0 (Deficit) or &lt; Emergency Target.")
    ]

    for title, text in formulas:
        elements.append(Paragraph(f"<b>{title}</b>", h2_style))
        elements.append(Paragraph(text, body_style))

    elements.append(PageBreak())

    # =========================================================================
    # 3. DEEP DIVE INTO THE 5 PARALLEL FUTURES
    # =========================================================================
    elements.append(Paragraph("3. Deep-Dive: The 5 Simulated Parallel Timelines", h1_style))
    elements.append(Paragraph(
        "The flagship feature of Financial Parallelverse is simulating five concurrent realities to evaluate resilience:",
        body_style
    ))

    scenarios_info = [
        ("Timeline 1: Baseline Reality (The Control)", "Green (#10b981)", "Assumes steady income received on time, routine expenses, and no unforeseen financial shocks. Demonstrates normal capital accumulation."),
        ("Timeline 2: Emergency Medical / Appliance Shock", "Amber (#f59e0b)", "Simulates a sudden out-of-pocket expense (default ₹25,000) in Month 3. Tests whether liquid reserves absorb the shock without breaching the emergency target."),
        ("Timeline 3: Delayed Salary Timing Shift", "Cyan (#06b6d4)", "Simulates a delayed paycheck in Month 2 where income received is ₹0. Living costs and loan EMIs must still be paid out of reserves. Double pay arrives in Month 3 upon resolution."),
        ("Timeline 4: Cost of Living Inflation (+15%)", "Violet (#a855f7)", "Applies a permanent 15% increase to all essential and discretionary expenses, reflecting sudden inflation, rent hikes, or utility price increases."),
        ("Timeline 5: Parallel Nightmare (Combined Adversity)", "Crimson (#f43f5e)", "The ultimate stress test: Salary delayed in Month 2, sudden ₹25,000 emergency in Month 3, and 15% inflation running simultaneously. Exposes catastrophic breaking points.")
    ]

    for name, col_label, desc in scenarios_info:
        elements.append(Paragraph(f"<b>&bull; {name}</b> &mdash; <i>{col_label}</i>", h2_style))
        elements.append(Paragraph(desc, body_style))

    elements.append(Spacer(1, 10))

    # =========================================================================
    # 4. PURCHASE AFFORDABILITY 4-WAY MATRIX
    # =========================================================================
    elements.append(Paragraph("4. Purchase Affordability Decision Matrix (₹70,000 Laptop Example)", h1_style))
    elements.append(Paragraph(
        "When evaluating a major purchase (e.g. ₹70,000 laptop), the platform presents 4 clear pathways with automated trade-off scoring:",
        body_style
    ))

    p_data = [
        [Paragraph("<b>Option</b>", body_style), Paragraph("<b>Upfront Cash</b>", body_style), Paragraph("<b>Monthly Drag</b>", body_style), Paragraph("<b>Safety Assessment & Trade-off</b>", body_style)],
        [Paragraph("<b>1. Buy Now with Cash</b>", body_style), Paragraph("₹70,000", body_style), Paragraph("₹0/mo", body_style), Paragraph("Zero interest fees, but instantly depletes liquid emergency reserve by 58%.", body_style)],
        [Paragraph("<b>2. Save & Buy Later</b>", body_style), Paragraph("₹0 today", body_style), Paragraph("₹0/mo", body_style), Paragraph("Protects liquid reserve 100%. Purchases using surplus savings in 4 months.", body_style)],
        [Paragraph("<b>3. Cheaper Alternative</b>", body_style), Paragraph("₹42,000", body_style), Paragraph("₹0/mo", body_style), Paragraph("Satisfies 90% of functional requirements while keeping reserves above target.", body_style)],
        [Paragraph("<b>4. Finance via EMI</b>", body_style), Paragraph("₹10,000 (Down)", body_style), Paragraph("₹5,330/mo", body_style), Paragraph("Preserves liquid cushion; costs ₹3,971 in interest over 12 months.", body_style)],
    ]
    p_table = Table(p_data, colWidths=[120, 80, 80, 260])
    p_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('PADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    elements.append(p_table)
    elements.append(Spacer(1, 10))

    # =========================================================================
    # 5. ALL FILES & CODEBASE STRUCTURE
    # =========================================================================
    elements.append(Paragraph("5. Complete Project File Directory & Components", h1_style))
    elements.append(Paragraph(
        "All code was created and committed into a clean, modular structure inside <code>C:\\Users\\Raghoothama T R\\Desktop\\Financial_Parallelverse</code>:",
        body_style
    ))

    file_tree = [
        ("backend/app/services/financial_engine.py", "Core baseline formulas: Free cash flow, savings rate, runway months, and DTI ratio."),
        ("backend/app/services/scenario_engine.py", "Flagship multi-timeline simulation engine projecting all 5 futures with breaking point alerts."),
        ("backend/app/services/affordability.py", "4-way purchase decision evaluator (Cash vs Save vs Cheaper vs EMI)."),
        ("backend/app/services/emi_calculator.py", "Reducing-balance amortization calculator supporting zero interest and extra repayments."),
        ("backend/app/services/reminder_service.py", "Installment scheduler, month-end date clamping, and RFC 5545 .ics iCalendar generator."),
        ("backend/app/api/", "FastAPI REST routers: health.py, profile.py, scenarios.py, purchases.py, emi.py, installments.py."),
        ("backend/app/main.py", "FastAPI app factory, CORS middleware, and automatic database initialization."),
        ("backend/tests/", "Comprehensive Pytest suite with 23 passing tests covering all calculations and API routes."),
        ("frontend_streamlit/app.py", "Ultra-polished Streamlit UI with Plotly charts, dark obsidian theme, persona presets, and .ics export."),
        ("frontend_react/", "Full React 18, TypeScript, and Vite source tree with modular page components."),
        ("scripts/seed_demo.py", "Seeds database with realistic Indian Rupee data (Alex Johnson profile & 2 active EMI plans)."),
        ("run_all.bat", "1-Click launcher starting both FastAPI Backend (port 8000) and Streamlit UI (port 8501).")
    ]

    for fpath, fdesc in file_tree:
        elements.append(Paragraph(f"&bull; <b>{fpath}</b>: {fdesc}", bullet_style))

    elements.append(PageBreak())

    # =========================================================================
    # 6. REST API SPECIFICATION
    # =========================================================================
    elements.append(Paragraph("6. FastAPI Backend REST API Contract", h1_style))
    api_spec = [
        [Paragraph("<b>Method</b>", body_style), Paragraph("<b>Endpoint Path</b>", body_style), Paragraph("<b>Request / Response Role</b>", body_style)],
        [Paragraph("GET", body_style), Paragraph("/api/health", body_style), Paragraph("System status, service version, and server timestamp.", body_style)],
        [Paragraph("GET / PUT", body_style), Paragraph("/api/profile", body_style), Paragraph("Retrieve and update user financial profile in SQLite.", body_style)],
        [Paragraph("POST", body_style), Paragraph("/api/scenarios/simulate", body_style), Paragraph("Execute 5-timeline simulation with custom shock inputs.", body_style)],
        [Paragraph("POST", body_style), Paragraph("/api/purchases/evaluate", body_style), Paragraph("Compare 4 purchase pathways with risk scoring.", body_style)],
        [Paragraph("POST", body_style), Paragraph("/api/emi/calculate", body_style), Paragraph("Calculate loan EMI, interest totals, and full amortization schedule.", body_style)],
        [Paragraph("GET / POST", body_style), Paragraph("/api/installments", body_style), Paragraph("List all active commitments or create a new loan plan.", body_style)],
        [Paragraph("PATCH", body_style), Paragraph("/api/installments/{id}/payments/{pid}", body_style), Paragraph("Toggle payment status between PAID and PENDING.", body_style)],
        [Paragraph("GET", body_style), Paragraph("/api/installments/{id}/calendar", body_style), Paragraph("Download RFC 5545 .ics iCalendar file for calendar sync.", body_style)],
    ]
    a_table = Table(api_spec, colWidths=[70, 200, 270])
    a_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('PADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    elements.append(a_table)
    elements.append(Spacer(1, 10))

    # =========================================================================
    # 7. HOW TO EXECUTE & RUN
    # =========================================================================
    elements.append(Paragraph("7. Step-by-Step Execution Guide", h1_style))
    elements.append(Paragraph(
        "To run the complete system on Windows:",
        body_style
    ))
    
    exec_steps = [
        ("Step 1: Automated Test Suite", "cd \"C:\\Users\\Raghoothama T R\\Desktop\\Financial_Parallelverse\"\n.\\run_tests.bat\n# Or: python -m pytest backend/tests -v"),
        ("Step 2: Seed Demo Data", "python scripts/seed_demo.py"),
        ("Step 3: Launch Both Servers (1-Click)", ".\\run_all.bat\n# Opens FastAPI Backend (:8000) and Streamlit FinTech UI (:8501)")
    ]
    for stitle, scmd in exec_steps:
        elements.append(Paragraph(f"<b>{stitle}</b>", h2_style))
        elements.append(Paragraph(scmd.replace("\n", "<br/>"), code_style))

    # =========================================================================
    # 8. HACKATHON LIVE DEMO SCRIPT
    # =========================================================================
    elements.append(Paragraph("8. Live Hackathon Pitch & Judge Demonstration Script", h1_style))
    elements.append(Paragraph(
        "Deliver this exact 3-minute pitch to the judges during your live demonstration:",
        body_style
    ))
    demo_script = (
        "<b>Minute 1 (The Hook):</b> 'Good evening judges! We are Team Dark_Knights presenting Financial Parallelverse for The Vampire's Ledger track. Today, millions make big financial decisions—like buying a ₹70,000 laptop—using standard EMI calculators that only tell them if their current paycheck can make month 1's installment. But life isn't static. A delayed salary or a medical emergency can instantly drain their reserves.'<br/><br/>"
        "<b>Minute 2 (The Simulator Demo):</b> 'Watch what happens when we input a ₹70,000 laptop into our Parallel Futures Engine. We simulate 5 simultaneous realities. In Baseline, savings grow steadily. But in Timeline 2, an unexpected ₹25,000 hospital bill breaches our emergency fund. In Timeline 5—the combined nightmare—our engine flags an exact breaking point in Month 3 where cash drops negative. No standard tool does this!'<br/><br/>"
        "<b>Minute 3 (Action & Reminders):</b> 'Next, our Purchase Matrix compares 4 options: cash, waiting, a cheaper ₹42k model, or structured EMI. Finally, in our Installment Tracker, users can download an official .ics iCalendar file with one click to sync due-date alarms right to their phone. Everything is backed by FastAPI, SQLite, and 23 verified mathematical tests. Thank you!'"
    )
    elements.append(Paragraph(demo_script, body_style))

    elements.append(Spacer(1, 10))
    elements.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=4, spaceAfter=8))
    elements.append(Paragraph("<i>Financial Parallelverse &bull; Complete Master Report &bull; Team Dark_Knights &bull; Hack-o-Ween PES University</i>", ParagraphStyle('Foot', parent=body_style, textColor=c_muted, alignment=1, fontSize=8)))

    doc.build(elements)
    print(f"Master PDF generated at: {pdf_path}")

    # Copy to Desktop
    import shutil
    shutil.copyfile(str(pdf_path), str(desktop_path))
    print(f"Master PDF copied to Desktop at: {desktop_path}")

if __name__ == "__main__":
    build_master_pdf()
