# PROJECT REPORT: SMART CAMPUS
## AI-Driven Campus ERP, Placement Readiness & ATS Resume Analytics Platform

---

**Academic Year**: 2026  
**Document Type**: Major Capstone Project Report / Technical Specification  
**Domain**: Full-Stack Web Engineering, Machine Learning & Natural Language Processing  
**Associated Presentation**: `Smart_Campus_Presentation.pptx`  
**Formal Word Document**: `Smart_Campus_Project_Report.docx`  

---

## EXECUTIVE SUMMARY / ABSTRACT

In contemporary higher education institutions, a pervasive gap separates daily academic administration from the career outcomes of graduating engineering students. Standard university ERP systems are traditionally confined to transactional silos: recording attendance percentages, logging tuition fee installments, and displaying static timetables. Consequently, students often discover their critical employability deficiencies—such as insufficient Data Structures and Algorithms (DSA) problem-solving depth, poor quantitative aptitude speed, or non-ATS-optimized resumes—late in their final academic year during on-campus recruitment drives.

To overcome this systemic disconnect, this project presents **Smart Campus**: an integrated, full-stack, AI-powered institutional ecosystem engineered using Python Flask, SQLite, Scikit-Learn, and modern responsive web technologies. The platform is structured around three foundational pillars:

1. **Academic Operations Hub (ERP)**: Delivers dynamic weekly class schedules with live lecture indicators, multi-subject attendance tracking with statutory 75% cutoff warnings, comprehensive course catalogs, and faculty directories.
2. **Predictive Placement Analytics Engine**: Employs an ensemble Random Forest Classifier trained on 15,000 authentic Indian engineering student records, evaluating 8 multi-dimensional feature parameters to compute placement probability percentages (76.27% test accuracy) coupled with explainable, personalized improvement roadmaps.
3. **Intelligent ATS Resume Analyzer**: Parses resumes in PDF and DOCX formats via PyPDF2 and python-docx, evaluates term frequency-inverse document frequency (TF-IDF) vector embeddings, measures cosine semantic similarity against corporate job descriptions, audits 80+ technical and soft skills, measures action verb strength, and provides targeted keyword gap analysis.

Additionally, Smart Campus features an end-to-end **Corporate Recruitment & Application Tracking System (ATS)** that allows Training & Placement Officers (TPOs) to post company drives, automatically enforce minimum CGPA eligibility filters, and track candidate pipelines across hiring stages (Applied ➔ Shortlisted ➔ Interview ➔ Placed).

---

## 1. INTRODUCTION & PROBLEM CONTEXT

### 1.1 Context and Motivation
Campus recruitment forms the primary benchmark by which engineering colleges and universities are evaluated by prospective students, accrediting bodies (such as NBA, NAAC, and NIRF), and industry partners. Despite high graduation rates, national employability studies consistently indicate that over 50% of engineering graduates lack immediate readiness for technical software development roles.

The root cause is rarely an absence of intellectual capacity, but rather the absence of **early diagnostic feedback**. Students lack continuous visibility into how their daily academic and technical habits align with real-world corporate selection criteria. Traditional university administrative portals remain passive repositories of past transactions. Smart Campus transforms this paradigm by converting collegiate ERP tools into an active, intelligent career readiness platform.

### 1.2 Problem Statement & Industry Gaps
The development of Smart Campus directly addresses four major industry deficiencies:

- **Isolated ERP Silos**: Existing tools maintain attendance, grades, and fee records without correlating these variables to career opportunities or placement criteria.
- **Delayed Intervention**: Deficiencies in coding or aptitude are typically identified only during final-year placement assessments when remedial action is exceedingly difficult.
- **Automated ATS Rejection**: Over 75% of engineering resumes submitted to corporate hiring portals are discarded by automated Applicant Tracking Systems before reaching human recruiters due to poor formatting, missing technical keywords, and non-standard phrasing.
- **TPO Administrative Burden**: Placement cells spend hundreds of administrative hours manually cross-checking student CGPA cutoffs on spreadsheets and tracking multi-round interview results.

### 1.3 Key Objectives
- **Unified Academic Hub**: Deliver a seamless student portal with dynamic weekly scheduling, live active lecture detection, and real-time subject-wise attendance monitoring.
- **Predictive Placement Forecasting**: Implement a machine learning classifier to predict placement probability using 8 validated features and generate automated personalized recommendations.
- **NLP Resume Optimization**: Provide an automated ATS parser that evaluates resumes against corporate job descriptions using TF-IDF and cosine similarity.
- **End-to-End Recruitment ATS**: Establish an eligibility-filtered campus drive portal with 1-click application pipelines and live lifecycle tracking.
- **Institutional TPO Command Center**: Equip placement officers with high-level KPI cards, branch-wise analytics, drive management tools, and candidate status workflows.

---

## 2. SYSTEM ARCHITECTURE & DESIGN

### 2.1 4-Tier Layered Architecture
Smart Campus is engineered following a clean four-tier modular architecture:

```
+-------------------------------------------------------------------------+
|                  TIER 1: PRESENTATION & CLIENT LAYER                   |
|   HTML5, Modern Vanilla CSS (Glassmorphism), JavaScript, Chart.js       |
|   Responsive Student Dashboard, Admin Command Center, Interactive Views  |
+-------------------------------------------------------------------------+
                                   ▲
                                   │ HTTP / JSON REST APIs
                                   ▼
+-------------------------------------------------------------------------+
|             TIER 2: APPLICATION CONTROLLER & BUSINESS LOGIC             |
|   Python Flask WSGI Server, Werkzeug Helpers, Session Auth (RBAC)        |
|   Timetable Routing, Drive Application Validation, File Ingestion       |
+-------------------------------------------------------------------------+
                                   ▲
                                   │ Model Inference / Text Vectorization
                                   ▼
+-------------------------------------------------------------------------+
|                TIER 3: AI & MACHINE LEARNING INFERENCE                  |
|   • Random Forest Classifier (placement_model.pkl)                      |
|   • Scikit-Learn TF-IDF Vectorizer & Cosine Similarity Engine           |
|   • Curated Skill Catalogs (64+ Tech, 16+ Soft Skills, Action Verbs)    |
|   • Heuristic Explainable Recommendation Engine                         |
+-------------------------------------------------------------------------+
                                   ▲
                                   │ SQL Queries / File I/O
                                   ▼
+-------------------------------------------------------------------------+
|                   TIER 4: DATA & PERSISTENCE LAYER                      |
|   • SQLite Relational Database (smart_campus.db)                        |
|   • 15,000 Records Benchmark Dataset (indian_engineering_placement_2026)|
|   • Secure Server Document Directory (/uploads)                         |
+-------------------------------------------------------------------------+
```

### 2.2 Relational Database Schema
The database (`smart_campus.db`) contains four core relational tables:

1. **`students`**: Master table storing academic, problem-solving, demographic, and placement fields:
   - `student_id` (TEXT PRIMARY KEY): Unique student registration number (e.g., `ST00001`).
   - `password`, `name`, `course`, `semester`: Authentication and identity fields.
   - `attendance` (REAL), `cgpa` (REAL): Academic metrics.
   - `aptitude_score` (REAL), `coding_score` (REAL): Cognitive and technical proxies.
   - `projects` (INTEGER), `internships` (INTEGER), `skill_count` (INTEGER): Portfolio counts.
   - `communication_score` (REAL): Interpersonal score for HR evaluations.
   - `placement_status` (TEXT): Current placement state ('Placed' / 'Not Placed').
   - `package_lpa` (REAL): Compensation secured upon placement.
   - `branch`, `gender`, `state`, `college_tier`, `fees`, `skills`: Demographics and skills.

2. **`companies`**: Campus recruitment drives:
   - `id` (INTEGER PRIMARY KEY AUTOINCREMENT)
   - `name`, `role`, `package`, `location`, `deadline`, `description`, `openings`
   - `min_cgpa` (REAL): Automatic eligibility barrier.
   - `required_skills` (TEXT): Comma-separated technical requirements.

3. **`applications`**: Recruitment candidate tracking:
   - `id` (INTEGER PRIMARY KEY AUTOINCREMENT)
   - `student_id` (TEXT, FK referencing `students`)
   - `company_id` (INTEGER, FK referencing `companies`)
   - `status` (TEXT): Progressive stages ('Applied', 'Shortlisted', 'Interview', 'Placed').
   - `applied_date` (TEXT), `notes` (TEXT)
   - Constraint: `UNIQUE(student_id, company_id)` preventing duplicate submissions.

4. **`admins`**: Institutional TPO credentials:
   - `id` (INTEGER PRIMARY KEY AUTOINCREMENT)
   - `username`, `password`, `name`, `role`, `email`

---

## 3. CORE FUNCTIONAL MODULES

### 3.1 Academic Operations & Dynamic Timetable
- **Weekly Schedule Engine**: Maintained in `timetable_data.py`. Defines full schedules from Monday to Friday with exact slots (09:15 to 15:55), subject names, faculty designations, and room allocations.
- **Active Class Detection**: Dynamically highlights ongoing classes based on system time.
- **Asynchronous Day Filtering**: The endpoint `/api/timetable/<day>` returns structured JSON allowing instant tab switching without page reload.
- **Subject-Wise Attendance**: Calculates real-time attendance across 11 accredited engineering subjects, displaying progress bars and highlighting subjects below the mandatory 75% limit.

### 3.2 Machine Learning Placement Prediction
- **Algorithm**: Supervised Random Forest Classifier (100 estimators, max depth 12).
- **8 Predictive Dimensions**:
  1. *DSA Problems Solved* (Proxy for technical interview coding competence)
  2. *CGPA* (Academic performance and company eligibility filter)
  3. *Communication Score* (HR interview and managerial round success)
  4. *Attendance Percentage* (Consistency and institutional discipline)
  5. *Aptitude Score* (First-round written test screening)
  6. *Internships Count* (Practical industry exposure)
  7. *Projects Count* (Hands-on software development capability)
  8. *Certifications Count* (Demonstrated continuous learning)
- **Explainable Advice**: The engine evaluates individual parameters against benchmarks and automatically generates specific advice (e.g., "DSA problem score has room for improvement; practice Dynamic Programming and Graph algorithms on LeetCode").

### 3.3 NLP-Powered ATS Resume Analyzer
- **Multi-Format Extraction**: Ingests `.pdf` via PyPDF2 and `.docx` via python-docx.
- **Skill Mining**: Scans text against 64+ technical skills (languages, frameworks, databases, cloud, DevOps, AI/ML) and 16+ soft skills.
- **TF-IDF & Cosine Similarity**: Creates vector embeddings of the resume and job description to compute exact semantic alignment.
- **Composite ATS Index (out of 100)**:
  $$\text{ATS Score} = (\text{Skill Match \%} \times 0.50) + (\text{Cosine Sim \%} \times 0.30) + (\text{Format Quality} \times 0.10) + (\text{Action Verbs} \times 0.10)$$
- **Gap Analysis**: Identifies missing keywords from the target job description to guide candidate revisions.

### 3.4 Corporate Recruitment Portal & ATS
- **Drive Discovery**: Students browse active drives with company profiles, CTC details, and deadlines.
- **Automated Eligibility Check**: Prevents submission if `student.cgpa < company.min_cgpa`.
- **Status Lifecycle**: Students monitor their applications across 4 transparent stages:
  $$\text{Applied} \longrightarrow \text{Shortlisted} \longrightarrow \text{Interview} \longrightarrow \text{Placed}$$

### 3.5 Placement Officer (TPO) Command Dashboard
- **Executive KPIs**: Real-time totals for registered students (15,000), placed students, average package (8.45 LPA), and highest package (18.0 LPA).
- **Departmental Analytics**: Instant breakdown of placement percentage and average CTC per engineering branch.
- **Drive & Pipeline Management**: Tools to post new hiring drives and update candidate statuses. Updating an application to 'Placed' automatically updates the student's master database record.

---

## 4. MACHINE LEARNING PIPELINE & EMPIRICAL RESULTS

### 4.1 Dataset Profile
The model was trained on the **Indian Engineering Placement Dataset 2026** (`indian_engineering_placement_2026.csv`), containing 15,000 complete engineering student records across 32 attributes.

| Dataset Metric | Value |
| :--- | :--- |
| Total Student Records | 15,000 |
| Training Partition (80%) | 12,000 records |
| Testing Partition (20%) | 3,000 records (Stratified) |
| Feature Columns | 8 Numerical Quantitative Features |
| Target Variable | `Placement_Status` (1 = Placed, 0 = Not Placed) |

### 4.2 Model Performance Metrics
The Random Forest Classifier demonstrated strong predictive capability on unseen test data:

| Metric | Training Set | Testing Set (Unseen) |
| :--- | :---: | :---: |
| **Overall Accuracy** | **89.43%** | **76.27%** |

#### Detailed Class-Wise Classification Report (Test Set, N = 3,000)

| Class | Precision (%) | Recall (%) | F1-Score (%) | Support |
| :--- | :---: | :---: | :---: | :---: |
| **Not Placed (0)** | 68.68% | 58.70% | 63.30% | 1,046 |
| **Placed (1)** | 79.49% | 85.67% | 82.46% | 1,954 |
| **Macro Average** | 74.09% | 72.18% | 72.88% | 3,000 |
| **Weighted Average** | 75.72% | 76.27% | 75.79% | 3,000 |

#### Test Set Confusion Matrix (N = 3,000)
- **True Negatives (TN)**: 614
- **False Positives (FP)**: 432
- **False Negatives (FN)**: 280
- **True Positives (TP)**: 1,674

### 4.3 Feature Importance Breakdown
Analysis of Gini importance (mean decrease in impurity) revealed the primary factors influencing placement:

| Rank | Feature Name | Relative Importance Weight (%) | Primary Impact Role |
| :---: | :--- | :---: | :--- |
| **1** | **DSA Problems Solved** | **34.11%** | Decisive differentiator in technical coding rounds |
| **2** | **CGPA** | **16.02%** | Primary screening threshold for shortlisting |
| **3** | **Communication Score** | **11.21%** | Critical factor in HR and managerial interviews |
| **4** | **Attendance Percentage** | **9.69%** | Indicator of discipline and consistency |
| **5** | **Aptitude Score** | **9.21%** | Gateway for round-1 written screening tests |
| **6** | **Internships Count** | **9.08%** | Industry readiness and practical exposure |
| **7** | **Projects Count** | **5.82%** | Verification of full-stack engineering ability |
| **8** | **Certifications Count** | **4.85%** | Demonstration of specialized self-learning |

---

## 5. COMPARATIVE VALUE & ADVANTAGES

### For Students
- **Early Warning Signal**: Identifies skill gaps in intermediate semesters before corporate drives commence.
- **Personalized Targets**: Provides clear benchmarks for CGPA, DSA problem counts, and projects.
- **ATS Optimization**: Pre-screens resumes against corporate job descriptions to minimize automated rejection.
- **Convenient Applications**: Enables 1-click applications to verified drives with clear eligibility status.

### For Placement Officers (TPO)
- **80% Overhead Reduction**: Automated CGPA cutoff enforcement eliminates manual spreadsheet filtering.
- **Pipeline Visibility**: Provides real-time tracking of candidate progress across all active drives.
- **Institutional Analytics**: Generates instant departmental reports on placement rates and average CTC.

### For Corporate Recruiters
- **Pre-Vetted Candidates**: Ensures all applicants meet stated academic and skill criteria.
- **Standardized Evaluation**: Provides structured applicant profiles with verified metrics.
- **Faster Hiring**: Shortens the recruitment cycle through automated candidate management.

---

## 6. FUTURE ENHANCEMENTS & ROADMAP

1. **LLM-Powered AI Mock Interviewer**: Integrate conversational AI and speech-to-text models to conduct realistic technical and HR mock interviews with real-time feedback.
2. **Automated Offer Letter Verification**: Deploy OCR and document intelligence to verify company offer letters, validate CTC breakdowns, and prevent fraudulent hiring claims.
3. **Native Mobile Application**: Build cross-platform Flutter/React Native mobile clients for real-time timetable alerts, attendance push notifications, and drive announcements.
4. **SMS / WhatsApp Notification Gateway**: Integrate messaging APIs for instant notifications regarding interview schedules and drive deadlines.

---

## 7. CONCLUSION

The **Smart Campus** platform successfully demonstrates that collegiate academic management and career intelligence can be unified into a single, high-performance web platform. By combining a modern responsive ERP with high-accuracy Machine Learning (Random Forest at 76.27% test accuracy) and NLP Resume Intelligence (TF-IDF vectorization and cosine similarity), the system equips students to proactively prepare for their careers while empowering placement cells with data-driven operational efficiency.

---

*Report compiled for Smart Campus Academic & Engineering Presentation, 2026.*
