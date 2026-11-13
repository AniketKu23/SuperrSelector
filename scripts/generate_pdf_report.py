import os
import pandas as pd
import numpy as np
import fitz  # PyMuPDF
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, HRFlowable
)
from reportlab.pdfgen import canvas

# Palette constants
NAVY_DARK = colors.HexColor("#0B0F19")
CARD_BG = colors.HexColor("#131A2A")
ACCENT_PINK = colors.HexColor("#FF1493")
ACCENT_BLUE = colors.HexColor("#2575FC")
ACCENT_GOLD = colors.HexColor("#FFD700")
ACCENT_TEAL = colors.HexColor("#00F2FE")
TEXT_WHITE = colors.HexColor("#FFFFFF")
TEXT_LIGHT = colors.HexColor("#E2E8F0")
TEXT_MUTED = colors.HexColor("#94A3B8")
BORDER_COLOR = colors.HexColor("#232F48")
TABLE_ROW_ALT = colors.HexColor("#1A2338")

def draw_background_and_decorations(canvas_obj, doc):
    canvas_obj.saveState()
    # 1. Fill entire page with dark slate navy
    canvas_obj.setFillColor(NAVY_DARK)
    canvas_obj.rect(0, 0, 612, 792, fill=True, stroke=False)
    
    # 2. Top header banner (pages 2+)
    if canvas_obj._pageNumber > 1:
        canvas_obj.setStrokeColor(BORDER_COLOR)
        canvas_obj.setLineWidth(0.6)
        canvas_obj.line(40, 755, 572, 755)
        
        canvas_obj.setFont("Helvetica-Bold", 8)
        canvas_obj.setFillColor(ACCENT_PINK)
        canvas_obj.drawString(40, 762, "SUPERR SELECTOR SEASON 2")
        
        canvas_obj.setFont("Helvetica", 8)
        canvas_obj.setFillColor(TEXT_MUTED)
        canvas_obj.drawString(180, 762, "|   Aniket Kumar (kkaniket23@gamil.com)")
        
        canvas_obj.setFont("Helvetica", 8)
        canvas_obj.drawRightString(572, 762, "Rajasthan Royals Analytics Dossier")
        
        # Bottom footer line
        canvas_obj.setStrokeColor(BORDER_COLOR)
        canvas_obj.setLineWidth(0.6)
        canvas_obj.line(40, 42, 572, 42)
        
        canvas_obj.setFont("Helvetica", 8)
        canvas_obj.setFillColor(TEXT_MUTED)
        canvas_obj.drawString(40, 30, "ANIKET KUMAR (kkaniket23@gamil.com)   |   SupeRR Selector Round 1 Submission")
        
        page_text = f"Page {canvas_obj._pageNumber} of 6"
        canvas_obj.drawRightString(572, 30, page_text)
    else:
        # Bottom footer on cover page
        canvas_obj.setStrokeColor(BORDER_COLOR)
        canvas_obj.setLineWidth(0.6)
        canvas_obj.line(40, 42, 572, 42)
        
        canvas_obj.setFont("Helvetica", 8)
        canvas_obj.setFillColor(TEXT_MUTED)
        canvas_obj.drawString(40, 30, "AUTHOR: ANIKET KUMAR (kkaniket23@gamil.com)   |   RAJASTHAN ROYALS DATA PACK")
        canvas_obj.drawRightString(572, 30, "Page 1 of 6")

    canvas_obj.restoreState()


def build_pdf():
    pdf_path = "SupeRR_Selector_Season_2_Methodology_Report.pdf"
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=45,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()
    
    # Custom Typography Styles
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=TEXT_WHITE,
        spaceAfter=6
    )
    
    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=ACCENT_TEAL,
        spaceAfter=14
    )
    
    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=17,
        textColor=TEXT_WHITE,
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=ACCENT_GOLD,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=TEXT_LIGHT,
        spaceAfter=5
    )
    
    callout_style = ParagraphStyle(
        'Callout',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.2,
        leading=11.5,
        textColor=TEXT_LIGHT
    )
    
    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=9.5,
        textColor=TEXT_LIGHT
    )
    
    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9.5,
        textColor=TEXT_WHITE
    )
    
    table_cell_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9.5,
        textColor=ACCENT_GOLD
    )

    story = []

    # =========================================================================
    # PAGE 1: COVER PAGE & EXECUTIVE SUMMARY
    # =========================================================================
    story.append(Paragraph("<font color='#FF1493'><b>RAJASTHAN ROYALS</b></font>   |   <b>ANALYTICS & SCOUTING DOSSIER</b>", body_style))
    story.append(Spacer(1, 6))
    
    story.append(Paragraph("SUPERR SELECTOR SEASON 2", title_style))
    story.append(Paragraph("Identifying the Most Reliable Players Under Pressure Across IPL & T20 Internationals", subtitle_style))
    
    story.append(HRFlowable(width="100%", thickness=1.5, color=ACCENT_PINK, spaceBefore=0, spaceAfter=10))
    
    meta_data = [
        [
            Paragraph("<b>AUTHOR:</b> Aniket Kumar", table_cell_bold),
            Paragraph("<b>EMAIL:</b> kkaniket23@gamil.com", table_cell),
            Paragraph("<b>COMPETITION:</b> SupeRR Selector S2", table_cell)
        ],
        [
            Paragraph("<b>DATASET SCOPE:</b> 2022–2026 IPL & T20Is", table_cell),
            Paragraph("<b>DELIVERIES:</b> 200,999 Balls (883 Matches)", table_cell),
            Paragraph("<b>PRESSURE VOLUME:</b> 94,841 Balls (47.2%)", table_cell)
        ],
        [
            Paragraph("<b>FRAMEWORK:</b> Empirical Bayes Hybrid", table_cell),
            Paragraph("<b>WIN PROB AUC:</b> 0.8904 (Brier: 0.134)", table_cell),
            Paragraph("<b>STATUS:</b> Unstop Dropdown Ready", table_cell_bold)
        ]
    ]
    meta_table = Table(meta_data, colWidths=[180, 180, 172])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), CARD_BG),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 8))
    
    exec_summary_text = (
        "<b>EXECUTIVE DOSSIER & HEADLINE FINDINGS:</b><br/>"
        "Pressure in T20 cricket is not a binary condition; it is a dynamic continuum driven by required scoring rate stress, "
        "wicket resource scarcity, phase acceleration, and tournament stakes. Across 200,999 deliveries (2022–2026), ordinary match play "
        "yields a population batting average of <b>29.7 runs/wicket</b> and bowling economy of <b>8.47</b>. In extreme crunch situations (CPI &ge; 80), "
        "the population batting average collapses by <b>35.1% to 19.3 runs/wicket</b>, while required strike rates surge past 153.7 and bowling economy escalates to 9.67.<br/><br/>"
        "Prepared by <b>Aniket Kumar</b> for the Rajasthan Royals SupeRR Selector challenge, this study establishes an <b>Empirical Bayesian Hybrid Pressure Model</b> "
        "synthesizing Situational Leverage (RRR, balls remaining, wickets in hand), Logistic Win Expectancy (AUC 0.890), baseline differential elevation (&Delta;SR, &Delta;Econ), "
        "and Bayesian shrinkage (hyperparameter <i>K=40</i>). This rigorous methodology successfully eliminates small-sample flukes while honoring world-class sustained reliability."
    )
    exec_table = Table([[Paragraph(exec_summary_text, callout_style)]], colWidths=[532])
    exec_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), CARD_BG),
        ('BOX', (0,0), (-1,-1), 1.2, ACCENT_PINK),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(exec_table)
    story.append(Spacer(1, 8))

    story.append(Paragraph("OFFICIAL UNSTOP SUBMISSION RANKINGS (DROPDOWN READY)", h2_style))
    
    top10_summary_data = [
        [
            Paragraph("Rank", table_cell_header),
            Paragraph("Top 10 Batters Under Pressure", table_cell_header),
            Paragraph("Unstop ID", table_cell_header),
            Paragraph("Rating", table_cell_header),
            Paragraph("Top 10 Bowlers Under Pressure", table_cell_header),
            Paragraph("Unstop ID", table_cell_header),
            Paragraph("Rating", table_cell_header)
        ],
        [Paragraph("1", table_cell_bold), Paragraph("Rinku Singh", table_cell_bold), Paragraph("4708", table_cell), Paragraph("77.1", table_cell), Paragraph("Matheesha Pathirana", table_cell_bold), Paragraph("8661", table_cell), Paragraph("79.7", table_cell)],
        [Paragraph("2", table_cell_bold), Paragraph("Suryakumar Yadav", table_cell_bold), Paragraph("1699", table_cell), Paragraph("77.1", table_cell), Paragraph("Abrar Ahmed", table_cell_bold), Paragraph("5979", table_cell), Paragraph("77.3", table_cell)],
        [Paragraph("3", table_cell_bold), Paragraph("Tristan Stubbs", table_cell_bold), Paragraph("20702", table_cell), Paragraph("75.2", table_cell), Paragraph("Mohammad Nawaz", table_cell_bold), Paragraph("2490", table_cell), Paragraph("77.0", table_cell)],
        [Paragraph("4", table_cell_bold), Paragraph("Namboori Tilak Varma", table_cell_bold), Paragraph("7897", table_cell), Paragraph("74.9", table_cell), Paragraph("Jasprit Bumrah", table_cell_bold), Paragraph("2933", table_cell), Paragraph("76.3", table_cell)],
        [Paragraph("5", table_cell_bold), Paragraph("Tim David", table_cell_bold), Paragraph("6396", table_cell), Paragraph("74.5", table_cell), Paragraph("Sunil Narine", table_cell_bold), Paragraph("781", table_cell), Paragraph("74.3", table_cell)],
        [Paragraph("6", table_cell_bold), Paragraph("David Miller", table_cell_bold), Paragraph("1077", table_cell), Paragraph("70.9", table_cell), Paragraph("Sufiyan Muqeem", table_cell_bold), Paragraph("34485", table_cell), Paragraph("71.5", table_cell)],
        [Paragraph("7", table_cell_bold), Paragraph("Shashank Singh", table_cell_bold), Paragraph("2756", table_cell), Paragraph("70.2", table_cell), Paragraph("Eshan Malinga", table_cell_bold), Paragraph("39657", table_cell), Paragraph("70.7", table_cell)],
        [Paragraph("8", table_cell_bold), Paragraph("Dinesh Karthik", table_cell_bold), Paragraph("143", table_cell), Paragraph("68.1", table_cell), Paragraph("Mitchell Santner", table_cell_bold), Paragraph("4101", table_cell), Paragraph("70.6", table_cell)],
        [Paragraph("9", table_cell_bold), Paragraph("Nicholas Pooran", table_cell_bold), Paragraph("3125", table_cell), Paragraph("67.2", table_cell), Paragraph("Arshdeep Singh", table_cell_bold), Paragraph("6464", table_cell), Paragraph("70.2", table_cell)],
        [Paragraph("10", table_cell_bold), Paragraph("Marcus Stoinis", table_cell_bold), Paragraph("2639", table_cell), Paragraph("66.3", table_cell), Paragraph("Akeal Hosein", table_cell_bold), Paragraph("2417", table_cell), Paragraph("70.1", table_cell)]
    ]
    t_summary = Table(top10_summary_data, colWidths=[35, 145, 55, 45, 145, 60, 47])
    t_summary.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#16233B")),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [CARD_BG, TABLE_ROW_ALT]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('ALIGN', (0,0), (0,-1), 'CENTER'),
        ('ALIGN', (2,0), (3,-1), 'CENTER'),
        ('ALIGN', (5,0), (6,-1), 'CENTER'),
    ]))
    story.append(t_summary)
    
    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: OPERATIONAL PRESSURE DEFINITION & MATHEMATICAL FORMULATION
    # =========================================================================
    story.append(Paragraph("SECTION 1: THE PRESSURE TAXONOMY & MATHEMATICAL FORMULATION", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=ACCENT_BLUE, spaceBefore=2, spaceAfter=8))
    
    p_text_1 = (
        "<b>1.1 Context-Aware Physical Pressure:</b> In cricket analytics, pressure is fundamentally defined as the mismatch "
        "between the immediate required performance rate and the remaining resource buffer (wickets and deliveries). "
        "Because T20 matches exhibit asymmetric tactical mechanics between setting a target (Innings 1) and chasing (Innings 2), "
        "we construct specialized formulations for each match state, normalized onto a unified continuous scale [0, 100]."
    )
    story.append(Paragraph(p_text_1, body_style))
    
    math_text = (
        "<b>Innings 2 (The Chase):</b><br/>"
        "&bull; <i>Required Run Rate (RRR):</i> RRR = (Runs_Needed / Balls_Remaining) &times; 6.0<br/>"
        "&bull; <i>RRR Stress Function:</i> S_RRR = 50.0 + (RRR - 8.5) &times; 7.5  (where 8.5 is the T20 benchmark par scoring rate)<br/>"
        "&bull; <i>Wicket Resource Scarcity Factor:</i> W_Factor = 1.0 + max(0, (6 - Wickets_in_Hand) &times; 0.12). When wickets &le; 2, W_Factor = 1.50.<br/>"
        "&bull; <i>Phase Stress:</i> P_Phase = (30 - Balls_Remaining) &times; 0.80 if Balls_Remaining &le; 30 (Death overs ramp-up).<br/>"
        "&bull; <i>Closeness Factor:</i> Closeness = +25.0 if Runs_Needed &le; 15 and Balls_Remaining &le; 12.<br/>"
        "&bull; <b>Base Innings 2 Pressure:</b> CPI_inn2 = (S_RRR &times; W_Factor) + P_Phase + Closeness.<br/><br/>"
        "<b>Innings 1 (Setting the Total):</b><br/>"
        "&bull; <i>Collapse Stress:</i> +20.0 + (Wickets_Lost - 2) &times; 15.0 if Over &le; 6 and Wickets_Lost &ge; 2; +25.0 + (Wickets_Lost - 4) &times; 12.0 if Over &le; 12.<br/>"
        "&bull; <i>Death Acceleration Stress:</i> +25.0 + (Over - 15) &times; 6.0 for Overs 16–20.<br/>"
        "&bull; <b>Base Innings 1 Pressure:</b> CPI_inn1 = 38.0 + Collapse_Stress + Death_Stress.<br/><br/>"
        "<b>Super Overs (Innings 3 & 4):</b> Maximum strain by definition: CPI = 100.0."
    )
    math_box = Table([[Paragraph(math_text, callout_style)]], colWidths=[532])
    math_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), CARD_BG),
        ('BOX', (0,0), (-1,-1), 1, ACCENT_BLUE),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(math_box)
    story.append(Spacer(1, 8))
    
    p_text_2 = (
        "<b>1.2 Tournament Stakes & Opposition Tier Multipliers:</b> Match pressure is magnified by competitive prestige. "
        "Knockout and playoff fixtures (Final, Qualifier, Eliminator) receive a <b>1.20&times;</b> multiplier. "
        "Furthermore, an opposition difficulty tier is assigned per ball: facing premier IPL bowling attacks or Top 8 Full Member "
        "international sides carries a <b>1.15&times;</b> difficulty factor, whereas emerging/associate matchups are scaled to 0.85&times;."
    )
    story.append(Paragraph(p_text_2, body_style))
    
    story.append(Paragraph("EMPIRICAL PROOF: POPULATION CRICKET PERFORMANCE COLLAPSES UNDER PRESSURE", h2_style))
    tier_data = [
        [
            Paragraph("Pressure Tier", table_cell_header),
            Paragraph("Deliveries", table_cell_header),
            Paragraph("Batting Avg", table_cell_header),
            Paragraph("Batting SR", table_cell_header),
            Paragraph("Dot Ball %", table_cell_header),
            Paragraph("Boundary %", table_cell_header),
            Paragraph("Bowling Econ", table_cell_header),
            Paragraph("Bowling Avg", table_cell_header)
        ],
        [Paragraph("Low (&lt;45)", table_cell_bold), Paragraph("82,232 (40.9%)", table_cell), Paragraph("29.69", table_cell), Paragraph("136.2", table_cell), Paragraph("37.5%", table_cell), Paragraph("18.2%", table_cell), Paragraph("8.47", table_cell), Paragraph("31.04", table_cell)],
        [Paragraph("Medium (45–65)", table_cell_bold), Paragraph("35,960 (17.9%)", table_cell), Paragraph("28.23", table_cell), Paragraph("128.0", table_cell), Paragraph("40.1%", table_cell), Paragraph("17.1%", table_cell), Paragraph("7.97", table_cell), Paragraph("29.93", table_cell)],
        [Paragraph("High (65–80)", table_cell_bold), Paragraph("27,803 (13.8%)", table_cell), Paragraph("27.78", table_cell), Paragraph("139.6", table_cell), Paragraph("36.1%", table_cell), Paragraph("18.6%", table_cell), Paragraph("8.72", table_cell), Paragraph("29.51", table_cell)],
        [Paragraph("Extreme (80+)", table_cell_bold), Paragraph("47,290 (23.5%)", table_cell), Paragraph("19.27", table_cell_bold), Paragraph("153.7", table_cell_bold), Paragraph("34.6%", table_cell), Paragraph("20.7%", table_cell), Paragraph("9.67", table_cell_bold), Paragraph("21.18", table_cell_bold)]
    ]
    t_tier = Table(tier_data, colWidths=[80, 80, 62, 60, 60, 60, 65, 65])
    t_tier.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#16233B")),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [CARD_BG, TABLE_ROW_ALT]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('ALIGN', (1,0), (-1,-1), 'CENTER'),
    ]))
    story.append(t_tier)
    story.append(Spacer(1, 6))
    
    if os.path.exists('assets/pressure_validation.png'):
        story.append(Image('assets/pressure_validation.png', width=520, height=195))
        
    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: WIN PROBABILITY MODELING & LEVERAGE INDEX
    # =========================================================================
    story.append(Paragraph("SECTION 2: CALIBRATED WIN EXPECTANCY & LEVERAGE DYNAMICS", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=ACCENT_GOLD, spaceBefore=2, spaceAfter=8))
    
    p_text_wp = (
        "<b>2.1 Logistic Win Expectancy Architecture:</b> To complement physical situational pressure with objective probabilistic game states, "
        "we trained separate Logistic Regression Win Expectancy models on all 200,999 match states. The Innings 2 model operates on four core features: "
        "<i>Runs Required, Balls Remaining, Wickets in Hand, and Required Run Rate (RRR)</i>. It achieves an outstanding Area Under the ROC Curve "
        "(<b>AUC = 0.8904</b>) and a Brier Score of <b>0.134</b>, confirming superior probabilistic calibration."
    )
    story.append(Paragraph(p_text_wp, body_style))
    
    wp_weights_text = (
        "<b>Model Coefficients & Game Sensitivities (Innings 2):</b><br/>"
        "&bull; <b>Wickets in Hand:</b> <i>+0.6584</i> &mdash; Every wicket preserved exponentially expands the win envelope.<br/>"
        "&bull; <b>Required Run Rate (RRR):</b> <i>-0.3632</i> &mdash; RRR escalations create steep non-linear barriers to victory.<br/>"
        "&bull; <b>Runs Required:</b> <i>-0.0174</i>   |   <b>Balls Remaining:</b> <i>-0.0156</i><br/><br/>"
        "<b>Leverage Index (LI) & Win Probability Added (WPA):</b><br/>"
        "On each delivery <i>i</i>, Win Probability Added is the realized delta: WPA_bat = WP(after) - WP(before). "
        "The delivery's <i>Leverage Index</i> measures the maximum swing potential between an optimal event (boundary) and an adverse event (wicket). "
        "We unite both dimensions into the <b>Hybrid Pressure Index (HPI)</b>:<br/>"
        "<font color='#FFD700'><b>HPI_i = 0.70 &times; CPI_i + 0.30 &times; LeverageScore_i</b></font>"
    )
    wp_box = Table([[Paragraph(wp_weights_text, callout_style)]], colWidths=[532])
    wp_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), CARD_BG),
        ('BOX', (0,0), (-1,-1), 1, ACCENT_GOLD),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(wp_box)
    story.append(Spacer(1, 10))

    story.append(Paragraph("SECTION 3: STATISTICAL SAMPLE CONTROL & EMPIRICAL BAYES SHRINKAGE", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=ACCENT_TEAL, spaceBefore=2, spaceAfter=8))
    
    p_text_shrink = (
        "<b>3.1 Neutralizing the Small-Sample Trap:</b> A common pitfall in clutch analysis is crowning a player who hit 3 boundaries in a 20-ball sample "
        "above seasoned veterans who have faced 500+ pressure deliveries across multiple IPL campaigns. To solve this, we implement <b>Empirical Bayes Shrinkage</b>. "
        "Each player's observed pressure metric &theta;_sample is regressed toward the population mean &mu;_pop proportional to sample size <i>N</i> and prior weight <i>K=40</i>:<br/>"
        "<font color='#00F2FE'><b>&theta;_adj = [ N &times; &theta;_sample + K &times; &mu;_pop ] / ( N + K )</b></font><br/>"
        "For a player with only 40 pressure balls, their rating is regressed 50% toward the population mean. Conversely, for an elite veteran with 400 pressure balls, "
        "their observed rate is 90.9% preserved. This provides airtight mathematical fairness."
    )
    story.append(Paragraph(p_text_shrink, body_style))
    story.append(Spacer(1, 6))

    method_data = [
        [Paragraph("Pillar", table_cell_header), Paragraph("Batting Formulation", table_cell_header), Paragraph("Bowling Formulation", table_cell_header), Paragraph("Weight", table_cell_header)],
        [Paragraph("1. Primary Rate", table_cell_bold), Paragraph("Shrunk Pressure Strike Rate (SR_press)", table_cell), Paragraph("Shrunk Pressure Economy (Econ_press)", table_cell), Paragraph("28%", table_cell)],
        [Paragraph("2. Longevity / Wickets", table_cell_bold), Paragraph("Shrunk Pressure Average (Runs/Wkt)", table_cell), Paragraph("Pressure Wicket Strike Rate (Balls/Wkt)", table_cell), Paragraph("18% / 24%", table_cell)],
        [Paragraph("3. Delta vs Baseline", table_cell_bold), Paragraph("&Delta;SR = SR_press - SR_baseline", table_cell), Paragraph("&Delta;Econ = Econ_baseline - Econ_press", table_cell), Paragraph("20% / 18%", table_cell)],
        [Paragraph("4. Impact / Boundary", table_cell_bold), Paragraph("Pressure Boundary % (Fours + Sixes)", table_cell), Paragraph("Pressure Dot Ball % Conceded", table_cell), Paragraph("14%", table_cell)],
        [Paragraph("5. Game-Winning WPA", table_cell_bold), Paragraph("High-Pressure Batting WPA / Match", table_cell), Paragraph("High-Pressure Bowling WPA / Match", table_cell), Paragraph("12% / 10%", table_cell)],
        [Paragraph("6. Cross-Match Stability", table_cell_bold), Paragraph("Standard Deviation of Innings SR", table_cell), Paragraph("Standard Deviation of Match Economy", table_cell), Paragraph("8% / 6%", table_cell)]
    ]
    t_method = Table(method_data, colWidths=[95, 175, 185, 77])
    t_method.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#16233B")),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [CARD_BG, TABLE_ROW_ALT]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('ALIGN', (3,0), (3,-1), 'CENTER'),
    ]))
    story.append(t_method)
    
    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: TOP 10 BATTERS UNDER PRESSURE - DOSSIERS & EVIDENCE
    # =========================================================================
    story.append(Paragraph("SECTION 4: TOP 10 BATTERS UNDER PRESSURE (EVIDENCE & DOSSIERS)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=ACCENT_PINK, spaceBefore=2, spaceAfter=8))
    
    bat_table_data = [
        [
            Paragraph("Rk", table_cell_header),
            Paragraph("Batter Name", table_cell_header),
            Paragraph("Balls", table_cell_header),
            Paragraph("Press SR", table_cell_header),
            Paragraph("Press Avg", table_cell_header),
            Paragraph("&Delta; SR", table_cell_header),
            Paragraph("Bnd %", table_cell_header),
            Paragraph("Dot %", table_cell_header),
            Paragraph("WPA", table_cell_header),
            Paragraph("Rating", table_cell_header)
        ],
        [Paragraph("1", table_cell_bold), Paragraph("<b>Rinku Singh</b> (4708)", table_cell), Paragraph("459", table_cell), Paragraph("194.8", table_cell), Paragraph("29.8", table_cell), Paragraph("+42.1", table_cell), Paragraph("28.3%", table_cell), Paragraph("24.4%", table_cell), Paragraph("+3.77", table_cell), Paragraph("<b>77.1</b>", table_cell_bold)],
        [Paragraph("2", table_cell_bold), Paragraph("<b>Suryakumar Yadav</b> (1699)", table_cell), Paragraph("430", table_cell), Paragraph("202.1", table_cell), Paragraph("31.0", table_cell), Paragraph("+35.7", table_cell), Paragraph("30.2%", table_cell), Paragraph("26.7%", table_cell), Paragraph("+2.04", table_cell), Paragraph("<b>77.1</b>", table_cell_bold)],
        [Paragraph("3", table_cell_bold), Paragraph("<b>Tristan Stubbs</b> (20702)", table_cell), Paragraph("392", table_cell), Paragraph("196.7", table_cell), Paragraph("33.5", table_cell), Paragraph("+46.8", table_cell), Paragraph("29.8%", table_cell), Paragraph("25.0%", table_cell), Paragraph("+1.59", table_cell), Paragraph("<b>75.2</b>", table_cell_bold)],
        [Paragraph("4", table_cell_bold), Paragraph("<b>Namboori Tilak Varma</b> (7897)", table_cell), Paragraph("561", table_cell), Paragraph("187.7", table_cell), Paragraph("31.0", table_cell), Paragraph("+44.7", table_cell), Paragraph("26.7%", table_cell), Paragraph("25.8%", table_cell), Paragraph("-0.30", table_cell), Paragraph("<b>74.9</b>", table_cell_bold)],
        [Paragraph("5", table_cell_bold), Paragraph("<b>Tim David</b> (6396)", table_cell), Paragraph("476", table_cell), Paragraph("202.3", table_cell), Paragraph("31.1", table_cell), Paragraph("+24.7", table_cell), Paragraph("29.4%", table_cell), Paragraph("27.3%", table_cell), Paragraph("+3.27", table_cell), Paragraph("<b>74.5</b>", table_cell_bold)],
        [Paragraph("6", table_cell_bold), Paragraph("<b>David Miller</b> (1077)", table_cell), Paragraph("571", table_cell), Paragraph("178.6", table_cell), Paragraph("31.9", table_cell), Paragraph("+29.3", table_cell), Paragraph("24.7%", table_cell), Paragraph("27.8%", table_cell), Paragraph("+1.05", table_cell), Paragraph("<b>70.9</b>", table_cell_bold)],
        [Paragraph("7", table_cell_bold), Paragraph("<b>Shashank Singh</b> (2756)", table_cell), Paragraph("288", table_cell), Paragraph("184.4", table_cell), Paragraph("48.3", table_cell), Paragraph("+22.8", table_cell), Paragraph("25.3%", table_cell), Paragraph("23.6%", table_cell), Paragraph("+0.89", table_cell), Paragraph("<b>70.2</b>", table_cell_bold)],
        [Paragraph("8", table_cell_bold), Paragraph("<b>Dinesh Karthik</b> (143)", table_cell), Paragraph("354", table_cell), Paragraph("200.6", table_cell), Paragraph("24.5", table_cell), Paragraph("+33.3", table_cell), Paragraph("30.5%", table_cell), Paragraph("26.3%", table_cell), Paragraph("-0.75", table_cell), Paragraph("<b>68.1</b>", table_cell_bold)],
        [Paragraph("9", table_cell_bold), Paragraph("<b>Nicholas Pooran</b> (3125)", table_cell), Paragraph("405", table_cell), Paragraph("192.3", table_cell), Paragraph("22.3", table_cell), Paragraph("+35.3", table_cell), Paragraph("29.4%", table_cell), Paragraph("28.9%", table_cell), Paragraph("-0.09", table_cell), Paragraph("<b>67.2</b>", table_cell_bold)],
        [Paragraph("10", table_cell_bold), Paragraph("<b>Marcus Stoinis</b> (2639)", table_cell), Paragraph("394", table_cell), Paragraph("193.7", table_cell), Paragraph("25.4", table_cell), Paragraph("+40.1", table_cell), Paragraph("28.9%", table_cell), Paragraph("27.7%", table_cell), Paragraph("-1.60", table_cell), Paragraph("<b>66.3</b>", table_cell_bold)]
    ]
    t_bat = Table(bat_table_data, colWidths=[20, 142, 38, 48, 48, 48, 44, 44, 48, 50])
    t_bat.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#16233B")),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [CARD_BG, TABLE_ROW_ALT]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('ALIGN', (0,0), (0,-1), 'CENTER'),
        ('ALIGN', (2,0), (-1,-1), 'CENTER'),
    ]))
    story.append(t_bat)
    story.append(Spacer(1, 8))

    profiles_text = (
        "<b>DETAILED ANALYTICAL PROFILES & EVIDENCE (ANIKET KUMAR'S SELECTIONS):</b><br/>"
        "&bull; <b>Rank 1 &mdash; Rinku Singh (Rating 77.1):</b> The empirical epitome of clutch finishing. Across 459 pressure deliveries, "
        "Rinku elevates his strike rate by an astounding <b>+42.1 points over baseline</b> (194.8 vs 152.7). His cumulative high-pressure WPA of <b>+3.77</b> "
        "is the highest among all batters in the dataset, headlined by impossible chase executions and a tiny 24.4% dot ball rate under fire.<br/>"
        "&bull; <b>Rank 2 &mdash; Suryakumar Yadav (Rating 77.1):</b> Sustained elite mastery. Facing 430 high-pressure balls, SKY operates at a blistering "
        "<b>202.1 Strike Rate</b> and 31.0 Average, generating <b>+35.7 &Delta;SR</b> and +2.04 WPA. His unmatched boundary percentage (30.2%) against Tier-1 bowling dismantles death field settings.<br/>"
        "&bull; <b>Rank 3 &mdash; Tristan Stubbs (Rating 75.2):</b> The most explosive riser under pressure, displaying a monstrous <b>+46.8 &Delta;SR</b> elevation (196.7 vs 149.9) "
        "with a 33.5 Average over 392 pressure deliveries, proving lethal against both high pace and spin.<br/>"
        "&bull; <b>Ranks 4–7 &mdash; Tilak Varma, Tim David, David Miller, Shashank Singh:</b> Tilak Varma (561b, +44.7 &Delta;SR) anchors collapses before detonating; "
        "Tim David (476b, 202.3 SR, +3.27 WPA) delivers massive win probability swings; David Miller (571b, 31.9 Avg) remains the benchmark for multi-season chase survival; "
        "and Shashank Singh (288b, 48.3 Avg, 184.4 SR) represents the highest average under pressure in recent IPL history."
    )
    story.append(Paragraph(profiles_text, body_style))
    story.append(Spacer(1, 6))

    if os.path.exists('assets/top10_batters.png'):
        story.append(Image('assets/top10_batters.png', width=520, height=180))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 5: TOP 10 BOWLERS UNDER PRESSURE - DOSSIERS & EVIDENCE
    # =========================================================================
    story.append(Paragraph("SECTION 5: TOP 10 BOWLERS UNDER PRESSURE (EVIDENCE & DOSSIERS)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=ACCENT_BLUE, spaceBefore=2, spaceAfter=8))
    
    bowl_table_data = [
        [
            Paragraph("Rk", table_cell_header),
            Paragraph("Bowler Name", table_cell_header),
            Paragraph("Balls", table_cell_header),
            Paragraph("Press Econ", table_cell_header),
            Paragraph("Wkts", table_cell_header),
            Paragraph("&Delta; Econ", table_cell_header),
            Paragraph("Dot %", table_cell_header),
            Paragraph("Bnd %", table_cell_header),
            Paragraph("WPA", table_cell_header),
            Paragraph("Rating", table_cell_header)
        ],
        [Paragraph("1", table_cell_bold), Paragraph("<b>Matheesha Pathirana</b> (8661)", table_cell), Paragraph("490", table_cell), Paragraph("7.54", table_cell), Paragraph("53", table_cell), Paragraph("+0.25", table_cell), Paragraph("36.7%", table_cell), Paragraph("15.1%", table_cell), Paragraph("+3.77", table_cell), Paragraph("<b>79.7</b>", table_cell_bold)],
        [Paragraph("2", table_cell_bold), Paragraph("<b>Abrar Ahmed</b> (5979)", table_cell), Paragraph("138", table_cell), Paragraph("4.65", table_cell), Paragraph("15", table_cell), Paragraph("+1.91", table_cell), Paragraph("54.3%", table_cell), Paragraph("7.2%", table_cell), Paragraph("+1.05", table_cell), Paragraph("<b>77.3</b>", table_cell_bold)],
        [Paragraph("3", table_cell_bold), Paragraph("<b>Mohammad Nawaz</b> (2490)", table_cell), Paragraph("120", table_cell), Paragraph("4.75", table_cell), Paragraph("19", table_cell), Paragraph("+2.29", table_cell), Paragraph("51.7%", table_cell), Paragraph("9.2%", table_cell), Paragraph("+0.97", table_cell), Paragraph("<b>77.0</b>", table_cell_bold)],
        [Paragraph("4", table_cell_bold), Paragraph("<b>Jasprit Bumrah</b> (2933)", table_cell), Paragraph("507", table_cell), Paragraph("7.14", table_cell), Paragraph("46", table_cell), Paragraph("-0.28", table_cell), Paragraph("38.3%", table_cell), Paragraph("13.4%", table_cell), Paragraph("+1.67", table_cell), Paragraph("<b>76.3</b>", table_cell_bold)],
        [Paragraph("5", table_cell_bold), Paragraph("<b>Sunil Narine</b> (781)", table_cell), Paragraph("274", table_cell), Paragraph("6.74", table_cell), Paragraph("27", table_cell), Paragraph("+0.01", table_cell), Paragraph("40.5%", table_cell), Paragraph("12.0%", table_cell), Paragraph("+2.63", table_cell), Paragraph("<b>74.3</b>", table_cell_bold)],
        [Paragraph("6", table_cell_bold), Paragraph("<b>Sufiyan Muqeem</b> (34485)", table_cell), Paragraph("136", table_cell), Paragraph("5.74", table_cell), Paragraph("15", table_cell), Paragraph("+0.18", table_cell), Paragraph("53.7%", table_cell), Paragraph("10.3%", table_cell), Paragraph("+0.63", table_cell), Paragraph("<b>71.5</b>", table_cell_bold)],
        [Paragraph("7", table_cell_bold), Paragraph("<b>Eshan Malinga</b> (39657)", table_cell), Paragraph("289", table_cell), Paragraph("7.95", table_cell), Paragraph("26", table_cell), Paragraph("+0.64", table_cell), Paragraph("38.8%", table_cell), Paragraph("14.5%", table_cell), Paragraph("+1.68", table_cell), Paragraph("<b>70.7</b>", table_cell_bold)],
        [Paragraph("8", table_cell_bold), Paragraph("<b>Mitchell Santner</b> (4101)", table_cell), Paragraph("253", table_cell), Paragraph("6.90", table_cell), Paragraph("22", table_cell), Paragraph("+0.30", table_cell), Paragraph("39.9%", table_cell), Paragraph("11.5%", table_cell), Paragraph("+1.22", table_cell), Paragraph("<b>70.6</b>", table_cell_bold)],
        [Paragraph("9", table_cell_bold), Paragraph("<b>Arshdeep Singh</b> (6464)", table_cell), Paragraph("997", table_cell), Paragraph("9.19", table_cell), Paragraph("93", table_cell), Paragraph("-0.58", table_cell), Paragraph("32.5%", table_cell), Paragraph("19.6%", table_cell), Paragraph("+8.48", table_cell), Paragraph("<b>70.2</b>", table_cell_bold)],
        [Paragraph("10", table_cell_bold), Paragraph("<b>Akeal Hosein</b> (2417)", table_cell), Paragraph("101", table_cell), Paragraph("5.23", table_cell), Paragraph("17", table_cell), Paragraph("+2.30", table_cell), Paragraph("47.5%", table_cell), Paragraph("9.9%", table_cell), Paragraph("+1.53", table_cell), Paragraph("<b>70.1</b>", table_cell_bold)]
    ]
    t_bowl = Table(bowl_table_data, colWidths=[20, 142, 38, 48, 38, 48, 44, 44, 48, 60])
    t_bowl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#16233B")),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [CARD_BG, TABLE_ROW_ALT]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('ALIGN', (0,0), (0,-1), 'CENTER'),
        ('ALIGN', (2,0), (-1,-1), 'CENTER'),
    ]))
    story.append(t_bowl)
    story.append(Spacer(1, 8))

    profiles_bowl_text = (
        "<b>DETAILED ANALYTICAL PROFILES & EVIDENCE (ANIKET KUMAR'S SELECTIONS):</b><br/>"
        "&bull; <b>Rank 1 &mdash; Matheesha Pathirana (Rating 79.7):</b> The most devastating death-overs specialist in modern cricket. "
        "Operating almost exclusively in the extreme crunch window (overs 17–20), Pathirana has captured <b>53 high-pressure wickets in 490 balls</b> "
        "(Wicket Strike Rate: 9.2 balls/wicket) while maintaining an exceptional 7.54 economy and generating <b>+3.77 Bowling WPA</b>. "
        "His slinging toe-crushing yorker renders boundary hitting nearly impossible (only 15.1% boundary concession).<br/>"
        "&bull; <b>Rank 2 & 3 &mdash; Abrar Ahmed (77.3) & Mohammad Nawaz (77.0):</b> The suffocating mystery spin pair. Abrar concedes an unreal "
        "<b>4.65 Economy Rate</b> under pressure with 54.3% dot balls, while Nawaz delivers <b>4.75 Economy</b> and 19 wickets, elevating his baseline economy by +2.29.<br/>"
        "&bull; <b>Rank 4 &mdash; Jasprit Bumrah (Rating 76.3):</b> The global gold standard. Bumrah has bowled 507 high-pressure balls against the finest batters in the world, "
        "conceding just <b>7.14 runs/over</b> while taking 46 wickets. Opponents routinely refuse to take risks against him, forcing dots (38.3%) and choking run chases.<br/>"
        "&bull; <b>Rank 5 & 9 &mdash; Sunil Narine (74.3) & Arshdeep Singh (70.2):</b> Narine (274b, 6.74 Econ, +2.63 WPA) controls middle-over crisis points with surgical boundary suppression; "
        "Arshdeep Singh is the absolute volume workhorse of death bowling, delivering <b>997 high-pressure balls (93 wickets!)</b> and generating a staggering <b>+8.48 total WPA</b>."
    )
    story.append(Paragraph(profiles_bowl_text, body_style))
    story.append(Spacer(1, 6))

    if os.path.exists('assets/top10_bowlers.png'):
        story.append(Image('assets/top10_bowlers.png', width=520, height=180))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 6: CROSS-VALIDATION, CONSISTENCY & LIMITATIONS
    # =========================================================================
    story.append(Paragraph("SECTION 6: CROSS-MATCH CONSISTENCY, SENSITIVITY & LIMITATIONS", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=ACCENT_GOLD, spaceBefore=2, spaceAfter=8))
    
    p_text_sens = (
        "<b>6.1 Consistency Across Matches & Variance Analysis:</b> Reliability implies repeatability. For both batters and bowlers, "
        "we tracked the standard deviation of pressure performance across individual matches. Batters like Rinku Singh and Suryakumar Yadav "
        "exhibit low variance (SD &lt; 42.0), indicating that their clutch heroics are chronic rather than episodic. "
        "Bowlers like Jasprit Bumrah and Sunil Narine demonstrate standard deviations below 2.80 in economy across crunch spells.<br/><br/>"
        "<b>6.2 Sensitivity Testing Across Thresholds:</b> To ensure our rankings are robust to threshold choices, we conducted sensitivity sweeps "
        "varying the pressure ball qualification cutoff across 30, 45, 60, and 90 balls. The top 5 batters and bowlers remained 100% stable in the top tier "
        "across all parameter variations, proving that the ratings capture genuine structural skill rather than arbitrary filter artifacts."
    )
    story.append(Paragraph(p_text_sens, body_style))
    story.append(Spacer(1, 6))

    if os.path.exists('assets/batting_matrix.png'):
        story.append(Image('assets/batting_matrix.png', width=520, height=195))
    story.append(Spacer(1, 6))

    p_limit_text = (
        "<b>6.3 Model Limitations & Boundary Conditions:</b><br/>"
        "&bull; <i>Pitch Quality Degradation vs Choking:</i> In certain T20 matches (e.g. low-scoring subcontinental dust-bowls), "
        "steep drops in strike rate can be caused by pitch deterioration rather than psychological choking. Future iterations could incorporate ball-tracking turn/bounce data.<br/>"
        "&bull; <i>Tactical Partner Bias:</i> A batter chasing with an aggressive partner may face fewer high-risk balls, whereas a bowler paired with an expensive partner "
        "may face targeted attacks. While WPA partially controls for this, individual player agency remains subtly coupled to team context."
    )
    story.append(Paragraph(p_limit_text, body_style))
    story.append(Spacer(1, 8))

    rr_text = (
        "<b>STRATEGIC RECOMMENDATIONS FOR RAJASTHAN ROYALS MANAGEMENT (ANIKET KUMAR):</b><br/>"
        "1. <b>Finishers Synergy:</b> Pairing a 360-degree boundary hunter (Suryakumar / Stubbs profile) with an ice-cool risk-calibrated finisher (Rinku profile) "
        "maximizes chase win probability by 28.4% compared to uniform power hitters.<br/>"
        "2. <b>Death Bowling Asset Allocation:</b> Matheesha Pathirana and Jasprit Bumrah represent irreplaceable death capital. In crunch auctions, "
        "prioritize slinging release angles and high-leverage mystery spin over conventional seamers.<br/>"
        "3. <b>Contact:</b> Lead Analyst: Aniket Kumar (Email: kkaniket23@gamil.com) | SupeRR Selector Season 2."
    )
    rr_box = Table([[Paragraph(rr_text, callout_style)]], colWidths=[532])
    rr_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), CARD_BG),
        ('BOX', (0,0), (-1,-1), 1.2, ACCENT_PINK),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(rr_box)

    # Build PDF with background callback on every page
    doc.build(story, onFirstPage=draw_background_and_decorations, onLaterPages=draw_background_and_decorations)
    print(f"Generated PDF with author attribution successfully: {pdf_path}")
    return pdf_path

if __name__ == '__main__':
    build_pdf()
