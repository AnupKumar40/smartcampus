"""
generate_docx_report.py
Generates a formal, publication-standard academic & industry Project Report
for 'Smart Campus: AI-Driven Campus ERP, Placement Readiness & ATS Resume Analytics System'
in Microsoft Word (.docx) format.
"""

import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    """Sets background color of a table cell."""
    shading_xml = f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>'
    cell._tc.get_or_add_tcPr().append(parse_xml(shading_xml))

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Sets inner padding for table cell."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_callout(doc, title, text, bg_hex="F1F5F9", border_hex="2563EB"):
    """Adds a stylish callout blockquote box."""
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = table.cell(0, 0)
    set_cell_background(cell, bg_hex)
    set_cell_margins(cell, top=140, bottom=140, left=200, right=200)

    # Set left border thick
    tcPr = cell._tc.get_or_add_tcPr()
    borders_xml = f'''
    <w:tcBorders {nsdecls("w")}>
        <w:top w:val="none"/>
        <w:left w:val="single" w:sz="36" w:space="0" w:color="{border_hex}"/>
        <w:bottom w:val="none"/>
        <w:right w:val="none"/>
    </w:tcBorders>
    '''
    tcPr.append(parse_xml(borders_xml))

    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(4)
    run_t = p.add_run(f"📌 {title.upper()}\n")
    run_t.font.name = "Calibri"
    run_t.font.size = Pt(10.5)
    run_t.font.bold = True
    run_t.font.color.rgb = RGBColor(30, 64, 175)

    run_b = p.add_run(text)
    run_b.font.name = "Calibri"
    run_b.font.size = Pt(10)
    run_b.font.color.rgb = RGBColor(51, 65, 85)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

def format_row(row, bg_hex, text_color, is_bold=False, font_size=9.5):
    """Helper to style an entire table row."""
    for cell in row.cells:
        set_cell_background(cell, bg_hex)
        set_cell_margins(cell, top=100, bottom=100, left=140, right=140)
        for p in cell.paragraphs:
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            for r in p.runs:
                r.font.name = "Calibri"
                r.font.size = Pt(font_size)
                r.font.bold = is_bold
                r.font.color.rgb = text_color

def create_project_report():
    doc = Document()

    # Page Margins (1 inch)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Styling helper variables
    COLOR_NAVY = RGBColor(15, 23, 42)    # Slate 900
    COLOR_BLUE = RGBColor(37, 99, 235)   # Blue 600
    COLOR_DARK = RGBColor(51, 65, 85)    # Slate 700
    COLOR_MUTED = RGBColor(100, 116, 139)# Slate 500

    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(22)
        p.paragraph_format.space_after = Pt(8)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = "Calibri"
        run.font.size = Pt(18)
        run.font.bold = True
        run.font.color.rgb = COLOR_NAVY
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = "Calibri"
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = COLOR_BLUE
        return p

    def add_h3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = "Calibri"
        run.font.size = Pt(11.5)
        run.font.bold = True
        run.font.color.rgb = COLOR_NAVY
        return p

    def add_body(text, space_after=6):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.15
        run = p.add_run(text)
        run.font.name = "Calibri"
        run.font.size = Pt(11)
        run.font.color.rgb = COLOR_DARK
        return p

    def add_bullet(bold_prefix, text):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        
        r_bold = p.add_run(bold_prefix + ": ")
        r_bold.font.name = "Calibri"
        r_bold.font.size = Pt(11)
        r_bold.font.bold = True
        r_bold.font.color.rgb = COLOR_NAVY

        r_text = p.add_run(text)
        r_text.font.name = "Calibri"
        r_text.font.size = Pt(11)
        r_text.font.color.rgb = COLOR_DARK
        return p

    # =========================================================================
    # TITLE PAGE
    # =========================================================================
    p_title_space = doc.add_paragraph()
    p_title_space.paragraph_format.space_before = Pt(60)

    p_proj = doc.add_paragraph()
    p_proj.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_proj = p_proj.add_run("PROJECT REPORT")
    r_proj.font.name = "Calibri"
    r_proj.font.size = Pt(14)
    r_proj.font.bold = True
    r_proj.font.color.rgb = COLOR_BLUE

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(12)
    p_title.paragraph_format.space_after = Pt(8)
    r_title = p_title.add_run("SMART CAMPUS:\nAI-DRIVEN CAMPUS ERP, PLACEMENT READINESS & ATS RESUME ANALYTICS SYSTEM")
    r_title.font.name = "Calibri"
    r_title.font.size = Pt(24)
    r_title.font.bold = True
    r_title.font.color.rgb = COLOR_NAVY

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(40)
    r_sub = p_sub.add_run("An Integrated Web Platform Unifying Academic Operations, Machine Learning Placement Forecasting & NLP-Powered Career Screening")
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(12)
    r_sub.font.color.rgb = COLOR_MUTED

    p_box = doc.add_paragraph()
    p_box.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_box.paragraph_format.space_before = Pt(80)
    p_box.paragraph_format.space_after = Pt(4)
    r_box = p_box.add_run("SUBMITTED IN PARTIAL FULFILLMENT OF THE REQUIREMENTS FOR\nTHE DEGREE OF BACHELOR OF TECHNOLOGY / COMPUTER SCIENCE & ENGINEERING")
    r_box.font.name = "Calibri"
    r_box.font.size = Pt(10)
    r_box.font.bold = True
    r_box.font.color.rgb = COLOR_DARK

    p_subm = doc.add_paragraph()
    p_subm.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_subm.paragraph_format.space_before = Pt(40)
    r_subm = p_subm.add_run("Academic Year: 2026\nSmart Campus Core Engineering & Placement Division")
    r_subm.font.name = "Calibri"
    r_subm.font.size = Pt(11)
    r_subm.font.color.rgb = COLOR_NAVY

    doc.add_page_break()

    # =========================================================================
    # CERTIFICATE & DECLARATION
    # =========================================================================
    add_h1("CERTIFICATE OF AUTHENTICITY")
    add_body(
        "This is to certify that the project entitled 'SMART CAMPUS: AI-DRIVEN CAMPUS ERP, "
        "PLACEMENT READINESS & ATS RESUME ANALYTICS SYSTEM' is a bona fide record of work carried out under "
        "academic supervision in partial fulfillment of the requirements for the award of the Degree of Bachelor "
        "of Technology in Computer Science & Engineering."
    )
    add_body(
        "The project demonstrates exceptional execution in combining Web Application Architecture (Python Flask, SQLite3), "
        "Supervised Machine Learning (Random Forest Classification on 15,000 engineering student placement records), "
        "and Natural Language Processing (PyPDF2, python-docx, TF-IDF Vectorization, Cosine Similarity ATS Engine)."
    )

    p_sig = doc.add_paragraph()
    p_sig.paragraph_format.space_before = Pt(60)
    p_sig.paragraph_format.space_after = Pt(20)
    r_sig = p_sig.add_run(
        "____________________________                  ____________________________\n"
        "Project Supervisor / Guide                    Head of Department / Placement Officer\n"
        "Department of Computer Science                Training & Placement Cell"
    )
    r_sig.font.name = "Calibri"
    r_sig.font.size = Pt(10)
    r_sig.font.color.rgb = COLOR_DARK

    doc.add_page_break()

    # =========================================================================
    # EXECUTIVE SUMMARY / ABSTRACT
    # =========================================================================
    add_h1("ABSTRACT")
    add_body(
        "In modern higher education institutions, a significant gap exists between daily academic operational management "
        "and the career placement outcomes of graduating engineering students. Conventional Campus ERP systems are traditionally "
        "restricted to isolated silos of attendance calculation, fee billing, and static timetable publication. Meanwhile, students "
        "frequently realize their skill deficiencies—such as insufficient Data Structures & Algorithms (DSA) practice, weak aptitude scores, "
        "or non-ATS-optimized resumes—late in their final academic year when corporate recruitment drives commence."
    )
    add_body(
        "To resolve this fundamental disconnect, this project develops 'Smart Campus': a comprehensive, full-stack, AI-driven institutional "
        "ecosystem engineered in Python Flask, SQLite, Scikit-Learn, and modern responsive web technologies. The platform is architected "
        "around three integrated pillars: (1) An Academic Operations ERP managing dynamic weekly scheduling, subject-wise attendance tracking "
        "with statutory cutoff compliance, faculty directories, and student master ledgers; (2) A Predictive Placement Intelligence Engine "
        "utilizing a Random Forest Classifier trained on 15,000 authentic Indian engineering student records, evaluating 8 critical predictive "
        "dimensions (DSA, CGPA, Communication, Attendance, Aptitude, Internships, Projects, Certifications) with 76.27% test accuracy and "
        "explainable recommendation generation; and (3) An Intelligent ATS Resume Analyzer parsing PDF and DOCX documents via PyPDF2 and python-docx, "
        "executing TF-IDF vectorization, cosine semantic similarity matching against corporate job descriptions, curated technical and soft skill "
        "taxonomies, action verb density measurement, and automated keyword gap diagnostics."
    )
    add_body(
        "Furthermore, Smart Campus integrates an end-to-end Corporate Recruitment and Application Tracking System (ATS), enabling placement officers "
        "to schedule company drives, enforce automatic CGPA eligibility barriers, and track student candidate pipelines across hiring stages. "
        "Experimental validation confirms that the platform provides institutional decision-makers with actionable diagnostic visibility while "
        "significantly empowering students to bridge their skill deficits well before corporate interview cycles."
    )

    add_callout(
        doc,
        "Key System Performance Highlights",
        "• Machine Learning Dataset: 15,000 Engineering Placement Records (2026 Benchmark)\n"
        "• Placement Prediction Accuracy: 89.43% Training Accuracy, 76.27% Test Accuracy\n"
        "• Top Placement Drivers: DSA Problems Solved (34.11%), CGPA (16.02%), Communication Score (11.21%)\n"
        "• Natural Language Processing: TF-IDF Vectorization, Cosine Similarity, Curated 80+ Skill Catalog\n"
        "• Database Scale: 15,000 Student Records, Company Drives, Application Tracking Pipeline in SQLite"
    )

    doc.add_page_break()

    # =========================================================================
    # TABLE OF CONTENTS
    # =========================================================================
    add_h1("TABLE OF CONTENTS")
    
    toc_items = [
        ("1. INTRODUCTION & BACKGROUND", "1"),
        ("   1.1 Context and Motivation", "1"),
        ("   1.2 Problem Statement & Industry Gaps", "2"),
        ("   1.3 Project Objectives", "3"),
        ("   1.4 Scope and Boundaries", "4"),
        ("2. LITERATURE SURVEY & RELATED WORK", "5"),
        ("   2.1 Evolution of Campus Information Systems", "5"),
        ("   2.2 Educational Data Mining & Employability Prediction", "6"),
        ("   2.3 Automated Resume Screening & ATS Technologies", "7"),
        ("   2.4 Comparative Solution Matrix", "8"),
        ("3. SYSTEM REQUIREMENTS & FEASIBILITY ANALYSIS", "9"),
        ("   3.1 Functional Requirements", "9"),
        ("   3.2 Non-Functional Requirements", "10"),
        ("   3.3 Hardware & Software Prerequisites", "11"),
        ("   3.4 Feasibility Study", "12"),
        ("4. SYSTEM ARCHITECTURE & DESIGN", "13"),
        ("   4.1 Four-Tier High-Level Architecture", "13"),
        ("   4.2 Entity-Relationship & Relational Database Design", "15"),
        ("   4.3 Data Flow & Execution Pipelines", "17"),
        ("5. CORE FUNCTIONAL MODULES", "19"),
        ("   5.1 Academic ERP & Dynamic Timetable Engine", "19"),
        ("   5.2 Machine Learning Placement Prediction Engine", "21"),
        ("   5.3 Intelligent ATS Resume Analyzer (NLP Engine)", "23"),
        ("   5.4 Corporate Recruitment & Application Tracking ATS", "25"),
        ("   5.5 Placement Officer (TPO) Command Dashboard", "27"),
        ("6. MACHINE LEARNING PIPELINE & EMPIRICAL EVALUATION", "29"),
        ("   6.1 Dataset Profile & Preprocessing", "29"),
        ("   6.2 Model Architecture & Hyperparameter Tuning", "30"),
        ("   6.3 Confusion Matrix & Performance Metrics", "31"),
        ("   6.4 Feature Importance & Explainable AI Insights", "33"),
        ("7. VERIFICATION, SECURITY & QUALITY ASSURANCE", "35"),
        ("   7.1 Verification & Validation Methodology", "35"),
        ("   7.2 Security, Role Separation & Data Protection", "36"),
        ("8. CONCLUSION, SOCIETAL IMPACT & FUTURE SCOPE", "37"),
        ("   8.1 Summary of Contributions", "37"),
        ("   8.2 Limitations & Constraints", "38"),
        ("   8.3 Future Enhancement Roadmap", "39"),
        ("9. REFERENCES & BIBLIOGRAPHY", "41")
    ]
    
    t_toc = doc.add_table(rows=len(toc_items), cols=2)
    t_toc.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_toc.autofit = False
    t_toc.columns[0].width = Inches(5.4)
    t_toc.columns[1].width = Inches(1.1)

    for i, (title, page) in enumerate(toc_items):
        cell_t = t_toc.cell(i, 0)
        cell_p = t_toc.cell(i, 1)
        set_cell_margins(cell_t, top=40, bottom=40, left=60, right=60)
        set_cell_margins(cell_p, top=40, bottom=40, left=60, right=60)

        p_t = cell_t.paragraphs[0]
        p_t.paragraph_format.space_before = Pt(1)
        p_t.paragraph_format.space_after = Pt(1)
        r_t = p_t.add_run(title)
        r_t.font.name = "Calibri"
        r_t.font.size = Pt(10)
        if title.strip().startswith(("1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9.")):
            r_t.font.bold = True
            r_t.font.color.rgb = COLOR_NAVY
        else:
            r_t.font.color.rgb = COLOR_DARK

        p_p = cell_p.paragraphs[0]
        p_p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p_p.paragraph_format.space_before = Pt(1)
        p_p.paragraph_format.space_after = Pt(1)
        r_p = p_p.add_run(page)
        r_p.font.name = "Calibri"
        r_p.font.size = Pt(10)
        r_p.font.color.rgb = COLOR_MUTED

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 1: INTRODUCTION
    # =========================================================================
    add_h1("CHAPTER 1: INTRODUCTION & BACKGROUND")
    
    add_h2("1.1 Context and Motivation")
    add_body(
        "Higher education engineering colleges operate in an increasingly competitive environment where institutional "
        "prestige and student career trajectories are primarily judged by campus placement success. According to national "
        "employability surveys across Indian engineering institutions, while thousands of engineering graduates enter the "
        "workforce annually, a significant percentage fail to secure relevant technical employment. A primary reason for this "
        "phenomenon is not the absolute absence of student aptitude, but the lack of early diagnostic intervention and the "
        "inability of traditional campus administrative tools to correlate daily academic participation with corporate hiring expectations."
    )
    add_body(
        "In a conventional university framework, administrative tasks such as timetable scheduling, attendance recording, "
        "course catalogs, and examination marksheets operate as static records. Students navigate their degree semesters without "
        "real-time awareness of how their attendance regularity, cumulative grade point average (CGPA), coding problem practice, "
        "and project portfolios stack up against actual industry hiring cutoffs. When campus recruitment drives open during "
        "the pre-final and final semesters, students are abruptly exposed to rigorous screening mechanisms: quantitative aptitude tests, "
        "live coding assessments, Applicant Tracking System (ATS) resume filters, and technical interviews. Remedial action at that late stage "
        "is rarely successful."
    )
    add_body(
        "The motivation behind 'Smart Campus' is to bridge this foundational divide. By combining operational collegiate ERP functionalities "
        "with predictive machine learning analytics and natural language resume processing, Smart Campus converts a passive institutional "
        "record-keeping system into an active, intelligent career readiness platform."
    )

    add_h2("1.2 Problem Statement & Industry Gaps")
    add_body(
        "The development of Smart Campus addresses four prominent deficiencies observed in existing campus management systems:"
    )
    add_bullet("Siloed Administrative Systems", "Existing campus ERP software packages focus exclusively on transactional activities—marking attendance, collecting fees, and posting grades. They completely isolate student academic performance from placement preparation.")
    add_bullet("Absence of Early Predictive Signals", "Students and academic mentors lack quantitative predictive tools to estimate the likelihood of placement before placement drives commence. Early warnings regarding insufficient problem-solving practice (DSA) or low aptitude scores are absent.")
    add_bullet("High ATS Resume Rejection Rates", "Over 75% of resumes uploaded to corporate hiring portals are rejected by automated ATS screening software due to formatting anomalies, missing domain-specific technical keywords, and weak action verb usage.")
    add_bullet("Manual Placement Coordination Overhead", "Training and Placement Officers (TPOs) spend immense manual effort maintaining offline spreadsheets, calculating CGPA cutoffs, notifying candidates, and tracking multi-round interview results.")

    add_h2("1.3 Project Objectives")
    add_body(
        "The primary engineering and functional objectives established for the Smart Campus system include:"
    )
    add_bullet("Objective 1 (Academic Hub)", "Deliver an intuitive, responsive student portal providing dynamic weekly timetable scheduling with live active-class detection, subject-wise attendance tracking against statutory 75% cutoffs, course catalogs, and faculty directories.")
    add_bullet("Objective 2 (ML Placement Predictor)", "Implement a supervised Machine Learning pipeline (Random Forest Classification) trained on 15,000 engineering student records to predict placement probability based on 8 core dimensions and output tailored recommendations.")
    add_bullet("Objective 3 (NLP ATS Resume Analyzer)", "Develop a document parsing and Natural Language Processing engine capable of ingesting PDF/DOCX resumes, computing cosine semantic similarity against job descriptions via TF-IDF vectorization, and auditing technical and soft skills.")
    add_bullet("Objective 4 (Recruitment ATS Portal)", "Establish an end-to-end recruitment management portal featuring automated CGPA eligibility checks, 1-click applications, and transparent hiring status progression (Applied, Shortlisted, Interview, Placed).")
    add_bullet("Objective 5 (TPO Command & Analytics Center)", "Equip institutional administrators and placement officers with real-time placement KPIs, departmental breakdown analytics, dynamic drive creation, and student application status update workflows.")

    add_h2("1.4 Scope and Boundaries")
    add_body(
        "The project scope encompasses all undergraduate and postgraduate engineering departments. The system provides role-based "
        "interfaces for Students and Administrators. The machine learning model is trained on a comprehensive benchmark dataset "
        "of 15,000 engineering student profiles reflecting real-world placement distributions. The ATS resume analyzer supports both "
        "standard PDF and DOCX document formats. The current scope utilizes SQLite as an embedded relational database for zero-config "
        "deployment, with architectural readiness to transition to PostgreSQL or MySQL in enterprise multi-server environments."
    )

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 2: LITERATURE SURVEY
    # =========================================================================
    add_h1("CHAPTER 2: LITERATURE SURVEY & RELATED WORK")

    add_h2("2.1 Evolution of Campus Information Systems & ERPs")
    add_body(
        "Campus Information Systems (CIS) and Enterprise Resource Planning (ERP) software in universities have progressed "
        "through three distinct generations over the past three decades. The first generation (1990s–early 2000s) comprised "
        "isolated desktop databases used primarily by registrars and accountants to store student demographics and financial records. "
        "The second generation (2010s) introduced web-enabled portals facilitating student grade viewing and online course registration. "
        "However, these systems remained purely transactional, recording what had already transpired without offering predictive or "
        "advisory capabilities."
    )
    add_body(
        "The emerging third generation—to which Smart Campus belongs—integrates cognitive technologies, machine learning, and data "
        "science directly into the institutional workflow. Rather than treating academic data as dead history, modern platforms mine "
        "academic and behavioral patterns to provide proactive student guidance."
    )

    add_h2("2.2 Machine Learning in Educational Data Mining (EDM)")
    add_body(
        "Educational Data Mining (EDM) and Learning Analytics have emerged as active research fields. Numerous academic investigations "
        "have evaluated different machine learning classifiers to forecast student academic retention, semester GPA, and final employment. "
        "Research in engineering employability demonstrates that while academic performance (CGPA) remains a primary baseline threshold, "
        "it alone cannot guarantee placement. Studies indicate that technical problem solving—specifically Data Structures and Algorithms "
        "(DSA) competence—and verbal communication scores are paramount in distinguishing placed candidates from non-placed candidates."
    )
    add_body(
        "Ensemble classification techniques, particularly Random Forest Classifiers, consistently outperform standalone Decision Trees, "
        "Naïve Bayes, and Logistic Regression models in employability prediction tasks due to their resilience to feature collinearity, "
        "ability to capture non-linear decision boundaries, and intrinsic feature importance estimation."
    )

    add_h2("2.3 Automated Resume Screening & ATS Technologies")
    add_body(
        "Modern corporate recruitment relies heavily on Applicant Tracking Systems (ATS) to filter candidate pipelines. Academic literature "
        "highlights that modern ATS software utilizes Natural Language Processing (NLP) techniques, including Term Frequency-Inverse "
        "Document Frequency (TF-IDF) vectorization, keyword ontology matching, and semantic vector similarity. Candidates whose resumes lack "
        "explicit domain keywords or fail basic optical structure standards are discarded before human recruiter inspection. Research underscores "
        "the necessity of providing students with self-assessment ATS tools during their college tenure so they can iteratively refine their "
        "resumes against target industry job descriptions."
    )

    add_h2("2.4 Comparative Solution Matrix")
    add_body(
        "The following matrix summarizes how Smart Campus compares with conventional university ERPs, standalone placement portals, "
        "and commercial resume screening tools:"
    )

    comp_table = doc.add_table(rows=5, cols=4)
    comp_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    comp_table.autofit = False
    col_widths = [Inches(2.0), Inches(1.5), Inches(1.5), Inches(1.5)]
    for row in comp_table.rows:
        for idx, width in enumerate(col_widths):
            row.cells[idx].width = width

    headers = ["Feature Dimension", "Traditional ERP", "Commercial ATS", "Smart Campus (Our System)"]
    for idx, name in enumerate(headers):
        comp_table.cell(0, idx).paragraphs[0].text = name
    format_row(comp_table.rows[0], "1E293B", RGBColor(255, 255, 255), is_bold=True, font_size=10)

    rows_data = [
        ("Daily Academic Operations (Timetable, Attendance)", "Comprehensive (Static)", "None", "Fully Integrated & Dynamic"),
        ("Placement Likelihood ML Prediction", "Not Available", "Not Available", "Random Forest (8 Factors, 76.3% Acc)"),
        ("ATS Resume & JD Match Engine", "Not Available", "Expensive Commercial Tool", "Integrated TF-IDF + Cosine NLP"),
        ("End-to-End Corporate Recruitment Portal", "Isolated or Third-Party", "Standalone Job Board", "Unified Student-TPO ATS Pipeline")
    ]
    for r_idx, r_vals in enumerate(rows_data):
        row = comp_table.rows[r_idx + 1]
        for c_idx, val in enumerate(r_vals):
            row.cells[c_idx].paragraphs[0].text = val
        bg = "F8FAFC" if r_idx % 2 == 0 else "FFFFFF"
        format_row(row, bg, COLOR_NAVY, is_bold=(c_idx == 3), font_size=9)

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 3: SYSTEM REQUIREMENTS & FEASIBILITY
    # =========================================================================
    add_h1("CHAPTER 3: SYSTEM REQUIREMENTS & FEASIBILITY ANALYSIS")

    add_h2("3.1 Functional Requirements")
    add_body("The system architecture fulfills the following explicit functional capabilities:")
    add_bullet("FR-1: Authentication & Role Management", "Secure credential-based authentication supporting distinct Student and Administrator sessions with route protection.")
    add_bullet("FR-2: Dynamic Timetable & Academic Scheduler", "Real-time daily scheduling with active lecture detection and JSON API endpoints (/api/timetable/<day>).")
    add_bullet("FR-3: Attendance & Statutory Compliance", "Multi-subject attendance tracking calculating classes attended versus scheduled, highlighting attendance under 75%.")
    add_bullet("FR-4: Placement Prediction Inference", "Interactive calculation of placement probability using trained Random Forest model with actionable guidance.")
    add_bullet("FR-5: Resume Parsing & ATS Scoring", "Ingestion and text extraction of PDF and DOCX files, computing skill match, action verb density, and TF-IDF similarity.")
    add_bullet("FR-6: Corporate Drives & Eligibility Validation", "Listing corporate drives, enforcing CGPA thresholds programmatically, and recording 1-click applications.")
    add_bullet("FR-7: Administrator Management & Analytics", "Posting new company recruitment drives, updating application stages, and analyzing branch-level placement metrics.")

    add_h2("3.2 Non-Functional Requirements")
    add_bullet("NFR-1: Performance & Response Time", "Server-side page rendering and ML inference must execute in under 150 milliseconds for optimal user experience.")
    add_bullet("NFR-2: Usability & Responsiveness", "User interfaces must follow a modern dark/light glassmorphic aesthetic that adapts seamlessly across desktops, tablets, and smartphones.")
    add_bullet("NFR-3: Security & Data Integrity", "Uploaded resumes must undergo filename sanitization (secure_filename) and extension validation. Database operations must use parameterized SQL queries to prevent SQL injection vulnerabilities.")
    add_bullet("NFR-4: Scalability", "Relational database schema and indexed queries must maintain high throughput with over 15,000 active student records.")

    add_h2("3.3 Hardware & Software Prerequisites")
    add_body(
        "Smart Campus is engineered with minimal infrastructure overhead, enabling deployment on local servers, institutional intranets, or cloud compute instances:"
    )

    req_table = doc.add_table(rows=7, cols=3)
    req_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    req_table.autofit = False
    for row in req_table.rows:
        row.cells[0].width = Inches(2.2)
        row.cells[1].width = Inches(2.2)
        row.cells[2].width = Inches(2.1)

    r_headers = ["Component", "Minimum Requirement", "Recommended Specification"]
    for idx, name in enumerate(r_headers):
        req_table.cell(0, idx).paragraphs[0].text = name
    format_row(req_table.rows[0], "1E293B", RGBColor(255, 255, 255), is_bold=True, font_size=10)

    specs = [
        ("Host Processor (CPU)", "Dual-Core 2.0 GHz x86/ARM", "Quad-Core Intel i5/i7 or AMD Ryzen 5+"),
        ("System Memory (RAM)", "4 GB DDR4", "8 GB - 16 GB DDR4"),
        ("Storage Drive", "2 GB Free Storage (SSD preferred)", "10 GB NVMe Storage"),
        ("Operating System", "Windows 10/11, Ubuntu 20.04+, macOS", "Ubuntu Server 22.04 LTS / Windows Server"),
        ("Python Runtime", "Python 3.9+", "Python 3.10 or 3.11 64-bit"),
        ("Client Web Browser", "Chrome 90+, Edge 90+, Firefox 88+", "Latest Modern Chromium/Firefox Browser")
    ]
    for r_idx, r_vals in enumerate(specs):
        row = req_table.rows[r_idx + 1]
        for c_idx, val in enumerate(r_vals):
            row.cells[c_idx].paragraphs[0].text = val
        bg = "F8FAFC" if r_idx % 2 == 0 else "FFFFFF"
        format_row(row, bg, COLOR_NAVY, font_size=9)

    add_h2("3.4 Feasibility Study")
    add_body(
        "A tripartite feasibility assessment confirmed the project's viability: (1) Technical Feasibility: The utilization "
        "of established, high-performance open-source libraries (Flask, Scikit-Learn, PyPDF2, SQLite) ensures complete technical "
        "support and maintenance without proprietary vendor lock-in. (2) Economic Feasibility: As an open-source Python stack, "
        "the software incurs zero licensing costs, resulting in tremendous institutional savings compared to commercial ERP and ATS suites. "
        "(3) Operational Feasibility: The intuitive UI design, requiring zero user training, ensures rapid adoption among both engineering "
        "students and placement administration staff."
    )

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 4: SYSTEM ARCHITECTURE & DESIGN
    # =========================================================================
    add_h1("CHAPTER 4: SYSTEM ARCHITECTURE & DESIGN")

    add_h2("4.1 Four-Tier High-Level Architecture")
    add_body(
        "Smart Campus is architected according to a clean four-tier modular architectural pattern designed for high separation "
        "of concerns, maintainability, and horizontal scalability:"
    )
    add_bullet("Tier 1: Presentation & Client Interface", "Consists of responsive HTML5 templates, custom Vanilla CSS3 utilizing CSS Grid and Flexbox for high-performance rendering, and asynchronous JavaScript for live DOM updates and Chart.js visualizations.")
    add_bullet("Tier 2: Application Logic & Routing Controller", "The Python Flask web framework acts as the centralized controller. It routes incoming HTTP requests, enforces session-based role-based access control (RBAC), manages file upload handling, and formats template context dictionaries.")
    add_bullet("Tier 3: AI & Machine Learning Inference Core", "Houses the pre-trained Scikit-Learn Random Forest model (placement_model.pkl) for real-time placement forecasting, the Scikit-Learn TfidfVectorizer and cosine_similarity engines for resume ATS matching, and the rule-based recommendation generator.")
    add_bullet("Tier 4: Data & Persistence Layer", "Employs an embedded SQLite3 relational database (smart_campus.db) containing structured tables for students, corporate recruiters, student job applications, and administrative credentials. Also oversees persistent resume file storage.")

    add_h2("4.2 Relational Database Schema & Entity Design")
    add_body(
        "The relational database schema is normalized and structured to balance transaction integrity with high-speed query execution. "
        "The smart_campus.db database consists of four primary relational tables:"
    )

    add_h3("Table 1: students (Master Student Academic & Employability Ledger)")
    add_body(
        "Stores the master profile, academic standings, technical problem-solving scores, and demographic data for all 15,000 students. "
        "Key fields include: student_id (TEXT PRIMARY KEY), password (TEXT), name (TEXT), course (TEXT), semester (INTEGER), "
        "attendance (REAL), cgpa (REAL), aptitude_score (REAL), coding_score (REAL, mapped from DSA problems solved), "
        "projects (INTEGER), internships (INTEGER), skill_count (INTEGER), communication_score (REAL), placement_status (TEXT), "
        "fees (REAL), skills (TEXT), branch (TEXT), gender (TEXT), state (TEXT), college_tier (TEXT), and package_lpa (REAL)."
    )

    add_h3("Table 2: companies (Campus Recruitment Drives Registry)")
    add_body(
        "Maintains active and upcoming on-campus recruitment drives. Schema includes: id (INTEGER PRIMARY KEY AUTOINCREMENT), "
        "name (TEXT NOT NULL), role (TEXT NOT NULL), package (TEXT NOT NULL), min_cgpa (REAL NOT NULL), required_skills (TEXT NOT NULL), "
        "location (TEXT NOT NULL), deadline (TEXT NOT NULL), description (TEXT), and openings (INTEGER DEFAULT 5)."
    )

    add_h3("Table 3: applications (Candidate Recruitment Pipeline)")
    add_body(
        "Tracks the real-time application lifecycle of students across company drives. Schema includes: id (INTEGER PRIMARY KEY AUTOINCREMENT), "
        "student_id (TEXT NOT NULL, FOREIGN KEY referencing students), company_id (INTEGER NOT NULL, FOREIGN KEY referencing companies), "
        "status (TEXT NOT NULL DEFAULT 'Applied'), applied_date (TEXT NOT NULL), and notes (TEXT). Enforces a UNIQUE(student_id, company_id) "
        "constraint to guarantee idempotency and prevent duplicate applications."
    )

    add_h3("Table 4: admins (Administrative & TPO Credentials)")
    add_body(
        "Provides role-based authentication for placement officers. Schema includes: id (INTEGER PRIMARY KEY AUTOINCREMENT), "
        "username (TEXT UNIQUE NOT NULL), password (TEXT NOT NULL), name (TEXT NOT NULL), role (TEXT NOT NULL), and email (TEXT NOT NULL)."
    )

    add_callout(
        doc,
        "Entity Relationship Summary",
        "• Relationship: 1 Student can submit M Applications (1-to-Many)\n"
        "• Relationship: 1 Company Drive receives N Applications (1-to-Many)\n"
        "• Associative Entity: 'applications' resolves the Many-to-Many relationship between students and companies\n"
        "• Cascade Logic: When an application status is promoted to 'Placed', an automated database trigger updates the student's master placement_status to 'Placed'."
    )

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 5: CORE FUNCTIONAL MODULES
    # =========================================================================
    add_h1("CHAPTER 5: CORE FUNCTIONAL MODULES & IMPLEMENTATION")

    add_h2("5.1 Academic ERP & Dynamic Timetable Engine")
    add_body(
        "The academic operations portal consolidates daily collegiate routines into a streamlined dashboard. "
        "The timetable engine, implemented in timetable_data.py, maintains weekly schedules across weekdays (Monday through Friday). "
        "Each class record defines time slots (e.g., '09:15 - 10:10'), assigned academic faculty, lecture room/lab numbers (e.g., 'CR-21', 'LT-21-B'), "
        "and classification type (Lecture, Lab, Elective, Language). The system automatically evaluates the current client day and highlights "
        "ongoing, completed, and upcoming lectures. A dedicated RESTful endpoint (/api/timetable/<day>) allows asynchronous dynamic switching "
        "without triggering full-page browser reloads."
    )
    add_body(
        "The Subject Attendance module evaluates attendance records across 11 engineering subjects (such as Computer Architecture, "
        "Java Programming, Python Programming, Data Structures, Operating Systems, and Behavioural Science). The application "
        "calculates sessions attended versus total conducted lectures and provides visual progress bars. Where attendance dips below the "
        "mandatory 75% threshold, visual danger alerts appear, prompting immediate remedial attendance."
    )

    add_h2("5.2 Placement Readiness & ML Prediction Module")
    add_body(
        "The placement prediction subsystem provides students with an empirical forecast of their campus placement likelihood. "
        "The interface automatically pre-populates the student's verified academic metrics (CGPA, Attendance, Aptitude, Coding Score, "
        "Projects, Internships, Certifications, Communication Score). Students can test 'what-if' scenarios by modifying parameters "
        "(e.g., observing how increasing their DSA problem count or completing an additional internship shifts their placement probability)."
    )
    add_body(
        "When the form is submitted, the Flask backend constructs an 8-dimensional feature vector, formats it into a Pandas DataFrame "
        "matching training column signatures, and passes it to rf_model.predict_proba(). The resulting probability percentage is rendered "
        "via a color-coded gauge. Concurrently, an explainable recommendation generator inspects individual feature scores against benchmark "
        "thresholds, producing actionable bullet points (e.g., advising students with CGPA < 7.5 to push their grade index or recommending "
        "active problem-solving on LeetCode if their coding score is below 75)."
    )

    add_h2("5.3 Intelligent ATS Resume Analyzer (NLP Engine)")
    add_body(
        "The ATS Resume Analyzer is one of the project's most sophisticated technical innovations. Designed to overcome the 75% automated "
        "rejection rate prevalent in modern hiring, the module accepts resume uploads in PDF and DOCX formats. Text extraction is handled "
        "by extract_resume_text() in app.py utilizing PyPDF2 for PDF page parsing and python-docx for Word paragraph iteration."
    )
    add_body(
        "Once raw text is extracted, the engine executes four distinct analytical pipelines in resume_parser.py:"
    )
    add_bullet("1. Curated Skill Catalog Mining", "Scans text against curated dictionaries containing 64+ technical skills (Python, Java, C++, React, Docker, Kubernetes, AWS, Machine Learning, DSA, Microservices) and 16+ soft skills (Leadership, Teamwork, Critical Thinking).")
    add_bullet("2. Action Verb Density Analysis", "Detects high-impact action verbs (e.g., 'Architected', 'Spearheaded', 'Optimized', 'Deployed', 'Engineered') that indicate quantifiable ownership in past projects.")
    add_bullet("3. TF-IDF & Cosine Similarity Alignment", "Computes n-gram TF-IDF vector embeddings for both the resume and the target corporate job description. Measures mathematical cosine similarity between the two document vectors.")
    add_bullet("4. Composite ATS Scoring", "Calculates a weighted composite ATS score out of 100: Skills Match (50%) + Semantic Cosine Similarity (30%) + Formatting & Contact Details (10%) + Action Verb Strength (10%). Generates an explicit list of missing keywords required to maximize shortlisting.")

    add_h2("5.4 Corporate Recruitment Portal & Application ATS")
    add_body(
        "The corporate placement hub (/companies) displays on-campus hiring drives with real-time openings, packages (up to 18 LPA), "
        "eligibility criteria, and locations. When a student initiates an application, the backend programmatically executes an eligibility "
        "check: if student['cgpa'] < company['min_cgpa'], the submission is blocked with an informative alert, safeguarding recruiters "
        "from non-compliant candidate lists. Eligible submissions create a timestamped application record. Students monitor their application "
        "lifecycle on the /applications view across four progressive stages: 'Applied' ➔ 'Shortlisted' ➔ 'Interview' ➔ 'Placed'."
    )

    add_h2("5.5 Placement Officer (TPO) Command Dashboard")
    add_body(
        "Administrative users access the portal via /admin/login. The executive dashboard provides comprehensive oversight: "
        "total registered students (15,000), total placed students, average placed package (8.45 LPA), and highest secured package (18.0 LPA). "
        "TPO coordinators can search and filter students by branch, placement status, or keywords; post new company hiring drives; and update "
        "student application statuses directly. Marking a candidate 'Placed' automatically updates the student master database."
    )

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 6: MACHINE LEARNING PIPELINE
    # =========================================================================
    add_h1("CHAPTER 6: MACHINE LEARNING PIPELINE & EMPIRICAL RESULTS")

    add_h2("6.1 Dataset Profile & Preprocessing")
    add_body(
        "The model is trained on the 'Indian Engineering Placement Dataset 2026' (indian_engineering_placement_2026.csv), "
        "comprising 15,000 authentic engineering student records across 32 academic, coding, demographic, and recruitment attributes. "
        "The target variable Placement_Status is binarized into 1 (Placed) and 0 (Not Placed)."
    )
    add_body(
        "Eight independent numerical features were selected based on correlation analysis and domain expertise: "
        "CGPA, Attendance_Percentage, Aptitude_Score, DSA_Problems_Solved, Projects_Count, Internships_Count, "
        "Certifications_Count, and Communication_Score. The dataset was partitioned using an 80:20 stratified split into 12,000 training "
        "samples and 3,000 test samples to preserve the exact class ratio."
    )

    add_h2("6.2 Model Architecture & Hyperparameters")
    add_body(
        "A Random Forest Classifier was selected for the final production model due to its superior generalization capabilities and "
        "resistance to overfitting compared to single decision trees. Hyperparameters were configured as follows: n_estimators=100, "
        "max_depth=12, min_samples_split=4, random_state=42. The trained model was serialized into placement_model.pkl via Joblib."
    )

    add_h2("6.3 Performance Metrics & Confusion Matrix")
    add_body(
        "The model achieved an exceptional Training Accuracy of 89.43% and a robust Test Accuracy of 76.27% on 3,000 completely unseen "
        "student test records. The detailed performance metrics across classes are presented below:"
    )

    # Insert Performance Metrics Table
    m_table = doc.add_table(rows=3, cols=5)
    m_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    m_table.autofit = False
    for row in m_table.rows:
        row.cells[0].width = Inches(1.8)
        row.cells[1].width = Inches(1.2)
        row.cells[2].width = Inches(1.2)
        row.cells[3].width = Inches(1.2)
        row.cells[4].width = Inches(1.1)

    m_heads = ["Class Label", "Precision (%)", "Recall (%)", "F1-Score (%)", "Test Support"]
    for idx, name in enumerate(m_heads):
        m_table.cell(0, idx).paragraphs[0].text = name
    format_row(m_table.rows[0], "1E293B", RGBColor(255, 255, 255), is_bold=True, font_size=10)

    class_data = [
        ("Not Placed (0)", "68.68%", "58.70%", "63.30%", "1,046"),
        ("Placed (1)", "79.49%", "85.67%", "82.46%", "1,954")
    ]
    for r_idx, r_vals in enumerate(class_data):
        row = m_table.rows[r_idx + 1]
        for c_idx, val in enumerate(r_vals):
            row.cells[c_idx].paragraphs[0].text = val
        bg = "F8FAFC" if r_idx % 2 == 0 else "FFFFFF"
        format_row(row, bg, COLOR_NAVY, is_bold=(c_idx == 0), font_size=9.5)

    add_body("", space_after=8)

    # Insert Confusion Matrix Image
    cm_img_path = "report_assets/confusion_matrix.png"
    if os.path.exists(cm_img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(4)
        run_img = p_img.add_run()
        run_img.add_picture(cm_img_path, width=Inches(4.2))

        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(14)
        r_cap = p_cap.add_run("Figure 6.1: Confusion Matrix Heatmap on Unseen Test Dataset (N = 3,000)")
        r_cap.font.name = "Calibri"
        r_cap.font.size = Pt(9.5)
        r_cap.font.italic = True
        r_cap.font.color.rgb = COLOR_MUTED

    add_h2("6.4 Feature Importance Analysis")
    add_body(
        "A major advantage of the Random Forest model is its intrinsic explainability via Gini importance (mean decrease in impurity). "
        "The relative weighting of all 8 predictive features is detailed below:"
    )

    # Insert Feature Importance Image
    fi_img_path = "report_assets/feature_importance.png"
    if os.path.exists(fi_img_path):
        p_img2 = doc.add_paragraph()
        p_img2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img2.paragraph_format.space_before = Pt(8)
        p_img2.paragraph_format.space_after = Pt(4)
        run_img2 = p_img2.add_run()
        run_img2.add_picture(fi_img_path, width=Inches(5.5))

        p_cap2 = doc.add_paragraph()
        p_cap2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap2.paragraph_format.space_after = Pt(14)
        r_cap2 = p_cap2.add_run("Figure 6.2: Random Forest Feature Importance Distribution in Placement Prediction")
        r_cap2.font.name = "Calibri"
        r_cap2.font.size = Pt(9.5)
        r_cap2.font.italic = True
        r_cap2.font.color.rgb = COLOR_MUTED

    add_body(
        "Key Analytical Insights from the Feature Importance Distribution:"
    )
    add_bullet("1. DSA Problem Count is the Decisive Factor (34.11%)", "Data Structures & Algorithms problem practice is the single most influential variable. Candidates with over 180 solved DSA problems exhibit an overwhelmingly higher likelihood of selection during technical interview rounds.")
    add_bullet("2. CGPA Acts as the Gatekeeper (16.02%)", "Academic CGPA represents the second highest weight. While high CGPA alone does not guarantee hiring without coding competence, it is the primary filter used by top firms (e.g., Microsoft 8.5, Infosys 7.5) to prune initial applicant pools.")
    add_bullet("3. Communication Skills Determine Final Conversion (11.21%)", "Communication score is the third largest determinant. In managerial and HR interview rounds, interpersonal fluency and technical articulation distinguish successful candidates from rejected applicants.")
    add_bullet("4. Attendance and Aptitude Form the Foundation (9.69% and 9.21%)", "Attendance percentage reflects discipline and consistency, while aptitude scores govern first-round written test clearance rates.")

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 7: VERIFICATION, TESTING & SECURITY
    # =========================================================================
    add_h1("CHAPTER 7: VERIFICATION, TESTING & SECURITY")

    add_h2("7.1 Testing Strategy")
    add_body(
        "The system underwent rigorous multi-stage verification to ensure operational stability, inference accuracy, "
        "and data integrity:"
    )
    add_bullet("Unit Testing", "Independent functions in resume_parser.py (tokenization, cosine similarity math, dictionary skill mapping) and timetable_data.py were tested with isolated input assertions.")
    add_bullet("Integration Testing", "End-to-end user workflows—from student login, timetable lookup, resume file upload, ML prediction submission, to company drive application—were validated under active session states.")
    add_bullet("Boundary & Edge-Case Testing", "Evaluated behavior under boundary conditions: empty resumes, unsupported file extensions (.exe, .zip), CGPA values below cutoffs, and simultaneous duplicate applications.")

    add_h2("7.2 Security Architecture & Data Protection")
    add_bullet("Session Security & RBAC", "Implemented cryptographically signed cookie sessions with secret keys. Administrative routes (/admin/*) strictly verify session['is_admin'] before exposing endpoints, preventing privilege escalation.")
    add_bullet("SQL Injection Prevention", "All database transactions utilize parameterized SQL queries (e.g., cursor.execute('SELECT * FROM students WHERE student_id=?', (id,))), completely mitigating SQL injection attack vectors.")
    add_bullet("File Upload Sanitization", "Uploaded documents are processed through Werkzeug's secure_filename() function and prepended with student IDs to prevent directory traversal attacks (e.g., ../../etc/passwd) and filename collisions.")

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 8: CONCLUSION & FUTURE SCOPE
    # =========================================================================
    add_h1("CHAPTER 8: CONCLUSION, SOCIETAL IMPACT & FUTURE SCOPE")

    add_h2("8.1 Summary of Contributions")
    add_body(
        "The Smart Campus project successfully delivers an end-to-end, full-stack, AI-driven institutional platform that seamlessly "
        "merges daily collegiate ERP operations with advanced career placement intelligence. Key achievements of the project include:"
    )
    add_bullet("Integrated Platform", "Eliminates administrative fragmentation by unifying dynamic timetables, attendance tracking, course catalogs, and student profiles into a cohesive web portal.")
    add_bullet("High-Accuracy ML Predictor", "Deploys a Random Forest Classifier trained on 15,000 engineering student records achieving 76.27% test accuracy and providing explainable diagnostic feedback across 8 dimensions.")
    add_bullet("State-of-the-Art NLP ATS Engine", "Empowers students to parse PDF and DOCX resumes, extract technical and soft skills, evaluate cosine similarity against corporate job descriptions, and eliminate automated rejection risks.")
    add_bullet("Streamlined Recruitment ATS", "Provides placement officers with automated CGPA cutoff validation, drive postings, and live application pipeline tracking, drastically reducing administrative overhead.")

    add_h2("8.2 Practical & Societal Impact")
    add_body(
        "By delivering early, objective feedback on skill gaps during intermediate academic years, Smart Campus shifts the institutional "
        "placement paradigm from reactive panic to proactive preparation. Engineering students receive actionable targets (e.g., increasing "
        "DSA problem solving, enhancing communication, polishing resumes) while they still have ample time to improve. Placement cells gain "
        "data-driven visibility into departmental employability trends, allowing targeted training bootcamps to be organized where most needed."
    )

    add_h2("8.3 Limitations & Constraints")
    add_body(
        "While highly effective, current operational boundaries include: (1) SQLite is ideal for localized and single-server campus intranets "
        "but should be migrated to PostgreSQL for massive multi-campus horizontal scaling; (2) The ATS parser relies on keyword ontology and "
        "TF-IDF n-grams rather than full large language model (LLM) contextual embeddings; and (3) Notifications are currently in-portal "
        "rather than integrated with external SMS/WhatsApp gateways."
    )

    add_h2("8.4 Future Enhancement Roadmap")
    add_bullet("LLM-Powered AI Mock Interviewer", "Integrate speech-to-text models (Whisper) and generative AI (Gemini/Llama) to conduct simulated technical and HR mock interviews with real-time vocal feedback.")
    add_bullet("Automated Offer Letter Verification", "Implement OCR and document intelligence to verify company offer letters, validate salary package (CTC) breakups, and prevent fraudulent hiring claims.")
    add_bullet("Native Mobile Application", "Develop cross-platform Flutter/React Native mobile clients for real-time timetable alerts, attendance push notifications, and instant drive broadcasts.")
    add_bullet("WhatsApp & SMS Notification Gateway", "Integrate Twilio or Gupshup APIs to broadcast urgent interview schedule changes and drive registrations directly to student mobile phones.")

    # =========================================================================
    # REFERENCES
    # =========================================================================
    add_h1("REFERENCES & BIBLIOGRAPHY")
    
    refs = [
        "1. Breiman, L. (2001). 'Random Forests.' Machine Learning, 45(1), 5-32.",
        "2. Pedregosa, F., et al. (2011). 'Scikit-learn: Machine Learning in Python.' Journal of Machine Learning Research, 12, 2825-2830.",
        "3. Salton, G., & Buckley, C. (1988). 'Term-weighting approaches in automatic text retrieval.' Information Processing & Management, 24(5), 513-523.",
        "4. Romero, C., & Ventura, S. (2020). 'Educational data mining and learning analytics: An updated survey.' WIREs Data Mining and Knowledge Discovery, 10(3), e1355.",
        "5. Grinberg, M. (2018). 'Flask Web Development: Developing Web Applications with Python.' 2nd Edition, O'Reilly Media.",
        "6. Chandole, V. (2026). 'Indian Engineering Placement Dataset 2026: Benchmark Analysis of Student Employability Attributes.' Technical Dataset Repository.",
        "7. Manning, C. D., Raghavan, P., & Schütze, H. (2008). 'Introduction to Information Retrieval.' Cambridge University Press.",
        "8. McKinney, W. (2010). 'Data Structures for Statistical Computing in Python.' Proceedings of the 9th Python in Science Conference, 56-61."
    ]
    for ref in refs:
        p_ref = doc.add_paragraph()
        p_ref.paragraph_format.space_before = Pt(2)
        p_ref.paragraph_format.space_after = Pt(4)
        p_ref.paragraph_format.left_indent = Inches(0.4)
        p_ref.paragraph_format.first_line_indent = Inches(-0.4)
        r_ref = p_ref.add_run(ref)
        r_ref.font.name = "Calibri"
        r_ref.font.size = Pt(10)
        r_ref.font.color.rgb = COLOR_DARK

    output_filename = "Smart_Campus_Project_Report.docx"
    doc.save(output_filename)
    print(f"[OK] Successfully generated academic Project Report: '{output_filename}'")

if __name__ == "__main__":
    create_project_report()
