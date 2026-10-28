from flask import Flask, render_template, request, redirect, session, jsonify
import sqlite3
import re
import os
import json
import csv
from datetime import datetime
import joblib
import pandas as pd
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader
from docx import Document
from resume_parser import parse_resume, analyze_resume_vs_job, calculate_company_matches
from timetable_data import get_dashboard_timetable_data, WEEKLY_TIMETABLE

app = Flask(__name__)

app.secret_key = "amity7one_secret_key"

DB_NAME = "smart_campus.db"
# ---------------- RESUME UPLOAD SETTINGS ----------------

UPLOAD_FOLDER = "uploads"

ALLOWED_EXTENSIONS = {"pdf", "docx"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def allowed_file(filename):

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )
# ---------------- RESUME TEXT EXTRACTION ----------------

def extract_resume_text(filepath):

    extension = filepath.rsplit(".", 1)[1].lower()

    # PDF
    if extension == "pdf":

        text = ""

        reader = PdfReader(filepath)

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        return text

    # DOCX
    elif extension == "docx":

        document = Document(filepath)

        text = ""

        for paragraph in document.paragraphs:
            text += paragraph.text + "\n"

        return text

    return ""

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


# ---------------- LOGIN ----------------

@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        student_id = request.form.get("student_id", "").strip()
        password = request.form.get("password", "").strip()

        conn = get_db()

        student = conn.execute(
            "SELECT * FROM students WHERE UPPER(student_id)=UPPER(?) AND password=?",
            (student_id, password)
        ).fetchone()

        conn.close()

        if student:
            session["student_id"] = student["student_id"]
            return redirect("/dashboard")

        return render_template(
            "login.html",
            error="Invalid Student ID or Password."
        )

    return render_template("login.html")


# ---------------- DASHBOARD ----------------

@app.route("/dashboard")
def dashboard():

    if "student_id" not in session:
        return redirect("/")

    conn = get_db()

    student = conn.execute(
        "SELECT * FROM students WHERE student_id=?",
        (session["student_id"],)
    ).fetchone()

    conn.close()

    if not student:
        return redirect("/")

    timetable_context = get_dashboard_timetable_data()

    return render_template(
        "dashboard.html",
        student=student,
        **timetable_context
    )


# ---------------- TIMETABLE API ----------------

@app.route("/api/timetable", methods=["GET"])
@app.route("/api/timetable/<day>", methods=["GET"])
def api_timetable(day=None):
    if "student_id" not in session and "is_admin" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    if day:
        day_key = day.strip().capitalize()
        classes = WEEKLY_TIMETABLE.get(day_key, [])
        return jsonify({"day": day_key, "classes": classes})
    
    return jsonify(get_dashboard_timetable_data())



# ---------------- SUBJECT ATTENDANCE ----------------

@app.route("/attendance")
def attendance():

    if "student_id" not in session:
        return redirect("/")

    conn = get_db()

    student = conn.execute(
        "SELECT * FROM students WHERE student_id=?",
        (session["student_id"],)
    ).fetchone()

    conn.close()

    if not student:
        return redirect("/")

    overall = student["attendance"]

    subjects = [
        {
            "code": "BCS501",
            "name": "Communication Skills-III",
            "att": min(100, overall + 5),
            "total": 20
        },
        {
            "code": "BCS503",
            "name": "Computer Architecture",
            "att": max(0, overall - 3),
            "total": 18
        },
        {
            "code": "BCS504",
            "name": "Java Programming",
            "att": min(100, overall + 2),
            "total": 16
        },
        {
            "code": "BCS523",
            "name": "Computer Architecture Lab",
            "att": max(0, overall - 5),
            "total": 10
        },
        {
            "code": "FLG501",
            "name": "German",
            "att": min(100, overall + 1),
            "total": 14
        },
        {
            "code": "BCS505",
            "name": "Python Programming",
            "att": overall,
            "total": 15
        },
        {
            "code": "BCS506",
            "name": "Data Structures",
            "att": max(0, overall - 2),
            "total": 20
        },
        {
            "code": "BCS507",
            "name": "Database Management",
            "att": min(100, overall + 3),
            "total": 18
        },
        {
            "code": "BCS508",
            "name": "Operating Systems",
            "att": max(0, overall - 4),
            "total": 17
        },
        {
            "code": "BSS504",
            "name": "Behavioural Science-V",
            "att": min(100, overall + 6),
            "total": 12
        },
        {
            "code": "BCS509",
            "name": "Web Technology",
            "att": overall,
            "total": 16
        }
    ]

    for subject in subjects:
        subject["present"] = round(
            subject["total"] * subject["att"] / 100
        )

    return render_template(
        "attendance.html",
        student=student,
        subjects=subjects
    )


# ---------------- PROFILE ----------------

@app.route("/profile")
def profile():

    if "student_id" not in session:
        return redirect("/")

    conn = get_db()

    student = conn.execute(
        "SELECT * FROM students WHERE student_id=?",
        (session["student_id"],)
    ).fetchone()

    conn.close()

    if not student:
        return redirect("/")

    return render_template(
        "profile.html",
        student=student
    )
# ---------------- CALENDAR ----------------

@app.route("/calendar")
def calendar():

    if "student_id" not in session:
        return redirect("/")

    return render_template("calendar.html")

# ---------------- COURSES ----------------

@app.route("/courses")
def courses():

    if "student_id" not in session:
        return redirect("/")

    conn = get_db()

    student = conn.execute(
        "SELECT * FROM students WHERE student_id=?",
        (session["student_id"],)
    ).fetchone()

    conn.close()

    if not student:
        return redirect("/")

    return render_template(
        "courses.html",
        student=student
    )
# ---------------- FACULTY ----------------

@app.route("/faculty")
def faculty():

    if "student_id" not in session:
        return redirect("/")

    conn = get_db()

    student = conn.execute(
        "SELECT * FROM students WHERE student_id=?",
        (session["student_id"],)
    ).fetchone()

    conn.close()

    if not student:
        return redirect("/")

    teachers = [
        {
            "name": "Dr Neha Gupta",
            "subject": "Behavioural Science – V"
        },
        {
            "name": "Dr Suman Paliwal",
            "subject": "Biodiversity and Law"
        },
        {
            "name": "Ms Padmakshi Sharma",
            "subject": "Communication Skills-III"
        },
        {
            "name": "Mr Amit Chaurasia",
            "subject": "Computer Architecture"
        },
        {
            "name": "Dr Sanjay Jain",
            "subject": "Java Programming"
        },
        {
            "name": "Mrs Deepti Saxena",
            "subject": "Software Engineering"
        },
        {
            "name": "Dr Taranpreet Singh Ruprah",
            "subject": "Python Programming"
        }
    ]

    return render_template(
        "faculty.html",
        student=student,
        teachers=teachers
    )
# ---------------- PLACEMENT HUB ----------------

@app.route("/placement")
def placement():

    if "student_id" not in session:
        return redirect("/")

    conn = get_db()

    student = conn.execute(
        "SELECT * FROM students WHERE student_id=?",
        (session["student_id"],)
    ).fetchone()

    conn.close()

    if not student:
        return redirect("/")

    return render_template(
        "placement.html",
        student=student
    )

# ---------------- AI RESUME ANALYZER ----------------

@app.route("/resume-analyzer", methods=["GET", "POST"])
def resume_analyzer():

    if "student_id" not in session:
        return redirect("/")

    conn = get_db()
    student = conn.execute(
        "SELECT * FROM students WHERE student_id=?",
        (session["student_id"],)
    ).fetchone()

    companies = conn.execute(
        "SELECT * FROM companies ORDER BY id ASC"
    ).fetchall()
    conn.close()

    if not student:
        return redirect("/")

    message = None
    error = None
    analysis = None
    job_description = ""
    selected_company_id = request.form.get("company_id", "") or request.args.get("company_id", "")

    # Auto-load latest uploaded resume for this student if not in session
    resume_text = session.get("resume_text")
    resume_filename = session.get("resume_filename")

    if not resume_text:
        prefix = f"{session['student_id']}_"
        if os.path.exists(app.config["UPLOAD_FOLDER"]):
            user_files = [f for f in os.listdir(app.config["UPLOAD_FOLDER"]) if f.startswith(prefix) and allowed_file(f)]
            if user_files:
                user_files.sort(key=lambda x: os.path.getmtime(os.path.join(app.config["UPLOAD_FOLDER"], x)), reverse=True)
                latest = user_files[0]
                latest_path = os.path.join(app.config["UPLOAD_FOLDER"], latest)
                extracted = extract_resume_text(latest_path)
                if extracted.strip():
                    resume_text = extracted
                    resume_filename = latest.replace(prefix, "")
                    session["resume_text"] = resume_text
                    session["resume_filename"] = resume_filename

    if request.method == "POST":
        action = request.form.get("action", "")

        # 1. FILE UPLOAD
        if action == "upload" or ("resume" in request.files and request.files["resume"].filename != ""):
            file = request.files.get("resume")
            if not file or file.filename == "":
                error = "Please choose a valid PDF or DOCX resume file to upload."
            elif not allowed_file(file.filename):
                error = "Unsupported file format. Please upload PDF or DOCX."
            else:
                orig_filename = secure_filename(file.filename)
                clean_filename = f"{session['student_id']}_{orig_filename}"
                filepath = os.path.join(app.config["UPLOAD_FOLDER"], clean_filename)
                file.save(filepath)

                extracted = extract_resume_text(filepath)
                if extracted.strip():
                    resume_text = extracted
                    resume_filename = orig_filename
                    session["resume_text"] = resume_text
                    session["resume_filename"] = resume_filename
                    message = f"Resume '{orig_filename}' uploaded and parsed successfully!"
                else:
                    error = "Resume uploaded, but no readable text could be extracted. Please check the file formatting."

        # 2. RUN AI ATS ANALYSIS
        elif action == "analyze":
            job_description = request.form.get("job_description", "").strip()

            # If user selected a company from dropdown/cards instead of typing
            if selected_company_id:
                for c in companies:
                    if str(c["id"]) == str(selected_company_id):
                        if not job_description:
                            job_description = f"Company: {c['name']}\nRole: {c['role']}\nRequired Skills: {c['required_skills']}\nPackage: {c['package']}\nEligibility: Min {c['min_cgpa']} CGPA\nJob Description: {c['description']}"
                        break

            if not resume_text:
                error = "Please upload your resume first before running AI analysis."
            elif not job_description:
                error = "Please provide or select a job description to compare against your resume."
            else:
                try:
                    analysis = analyze_resume_vs_job(resume_text, job_description)
                    message = "AI Resume & ATS Analysis generated successfully!"
                except Exception as e:
                    error = f"Analysis error: {str(e)}"

    # If GET request with company_id query parameter, pre-fill that company's description
    if request.method == "GET" and selected_company_id:
        for c in companies:
            if str(c["id"]) == str(selected_company_id):
                job_description = f"Company: {c['name']}\nRole: {c['role']}\nRequired Skills: {c['required_skills']}\nPackage: {c['package']}\nEligibility: Min {c['min_cgpa']} CGPA\nJob Description: {c['description']}"
                if resume_text:
                    analysis = analyze_resume_vs_job(resume_text, job_description)
                break

    parsed_resume = parse_resume(resume_text) if resume_text else None
    company_matches = calculate_company_matches(resume_text, companies) if resume_text else []

    return render_template(
        "resume_analyzer.html",
        student=student,
        message=message,
        error=error,
        resume_text=resume_text,
        resume_filename=resume_filename,
        parsed_resume=parsed_resume,
        job_description=job_description,
        selected_company_id=selected_company_id,
        analysis=analysis,
        companies=companies,
        company_matches=company_matches
    )


@app.route("/resume-analyzer/clear")
def clear_resume():
    if "student_id" not in session:
        return redirect("/")
    session.pop("resume_text", None)
    session.pop("resume_filename", None)
    return redirect("/resume-analyzer")
# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")
# ---------------- TIME TABLE ----------------

@app.route("/timetable")
def timetable():

    if "student_id" not in session:
        return redirect("/")

    return render_template("timetable.html")


# ---------------- ML PLACEMENT MODEL HELPERS ----------------

MODEL_PATH = "placement_model.pkl"
METRICS_PATH = "model_metadata.json"
DATASET_PATH = "indian_engineering_placement_2026.csv"

_cached_model = None

def get_placement_model():
    global _cached_model
    if _cached_model is None and os.path.exists(MODEL_PATH):
        try:
            _cached_model = joblib.load(MODEL_PATH)
        except Exception as e:
            print("Failed to load ML model:", e)
    return _cached_model

def get_model_metrics():
    if os.path.exists(METRICS_PATH):
        try:
            with open(METRICS_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print("Failed to load metrics:", e)
    return {
        "test_accuracy": 85.0,
        "train_accuracy": 99.25,
        "total_records": 500,
        "n_estimators": 100,
        "confusion_matrix": [[59, 5], [10, 26]],
        "feature_importances": {
            "CGPA": 0.3622,
            "Coding Score": 0.1743,
            "Aptitude Score": 0.1096,
            "Attendance": 0.0898,
            "Communication Score": 0.0843,
            "Projects": 0.0755,
            "Internships": 0.0710,
            "Skill Count": 0.0331
        },
        "classification_report": {
            "Not Placed": {"precision": 85.5, "recall": 92.2, "f1_score": 88.7, "support": 64},
            "Placed": {"precision": 83.9, "recall": 72.2, "f1_score": 77.6, "support": 36}
        }
    }

def generate_recommendations(cgpa, coding, aptitude, communication, projects, internships):
    recs = []
    if cgpa >= 7.5:
        recs.append("Solid CGPA! You comfortably meet the eligibility cutoff for top-tier campus recruitment drives.")
    else:
        recs.append(f"Current CGPA is {cgpa:.2f}. Try pushing it above 7.0–7.5 to open up elite consulting & product companies.")

    if coding >= 75:
        recs.append("Strong coding readiness! Maintain competitive coding practice in DSA (Arrays, Graphs, Dynamic Programming).")
    else:
        recs.append(f"Coding score ({coding:.1f}) has room for improvement. Regular practice on LeetCode / HackerRank is recommended.")

    if aptitude >= 70:
        recs.append("Aptitude & quantitative speed are well-suited for round-1 company screening tests.")
    else:
        recs.append(f"Aptitude score ({aptitude:.1f}) needs practice: focus on logical reasoning, quantitative analysis, and data interpretation.")

    if projects >= 2:
        recs.append(f"Great portfolio! You have completed {projects} practical project(s) to discuss in technical interviews.")
    else:
        recs.append("Build at least 2 full-stack or machine learning projects on GitHub with live deployed demos.")

    if internships >= 1:
        recs.append(f"Excellent industry exposure with {internships} internship(s) on your profile.")
    else:
        recs.append("Consider applying for summer internships or contributing to open-source software to gain hands-on team experience.")

    if communication >= 75:
        recs.append("Strong communication skills for HR behavioral, managerial, and group discussion rounds.")
    else:
        recs.append("Sharpen communication skills by participating in mock interviews and presentation sessions.")

    return recs


# ---------------- 1. PREDICT PLACEMENT ROUTE ----------------

@app.route("/predict-placement", methods=["GET", "POST"])
def predict_placement():
    if "student_id" not in session:
        return redirect("/")

    conn = get_db()
    student = conn.execute(
        "SELECT * FROM students WHERE student_id=?",
        (session["student_id"],)
    ).fetchone()
    conn.close()

    if not student:
        return redirect("/")

    # Default values from student's profile
    form_data = {
        "cgpa": float(student["cgpa"]),
        "attendance": float(student["attendance"]),
        "aptitude_score": float(student["aptitude_score"]),
        "coding_score": float(student["coding_score"]),
        "projects": int(student["projects"]),
        "internships": int(student["internships"]),
        "skill_count": int(student["skill_count"]),
        "communication_score": float(student["communication_score"])
    }

    if request.method == "POST":
        try:
            form_data["cgpa"] = float(request.form.get("cgpa", form_data["cgpa"]))
            form_data["attendance"] = float(request.form.get("attendance", form_data["attendance"]))
            form_data["aptitude_score"] = float(request.form.get("aptitude_score", form_data["aptitude_score"]))
            form_data["coding_score"] = float(request.form.get("coding_score", form_data["coding_score"]))
            form_data["projects"] = int(float(request.form.get("projects", form_data["projects"])))
            form_data["internships"] = int(float(request.form.get("internships", form_data["internships"])))
            form_data["skill_count"] = int(float(request.form.get("skill_count", form_data["skill_count"])))
            form_data["communication_score"] = float(request.form.get("communication_score", form_data["communication_score"]))
        except Exception as e:
            print("Form parse error:", e)

    # Machine Learning Model Inference
    model = get_placement_model()
    # In Indian Engineering Placement Dataset 2026:
    # Coding Score / DSA Problems Solved: average is ~180 problems. If student inputs 0-100 score, map to ~0-220 problems
    raw_coding = form_data["coding_score"]
    dsa_solved = int(raw_coding * 2.2) if raw_coding <= 100 else int(raw_coding)

    features = [[
        form_data["cgpa"],
        form_data["attendance"],
        form_data["aptitude_score"],
        dsa_solved,
        form_data["projects"],
        form_data["internships"],
        form_data["skill_count"],
        form_data["communication_score"]
    ]]

    if model is not None:
        try:
            feat_cols = [
                "CGPA",
                "Attendance_Percentage",
                "Aptitude_Score",
                "DSA_Problems_Solved",
                "Projects_Count",
                "Internships_Count",
                "Certifications_Count",
                "Communication_Score"
            ]
            df_features = pd.DataFrame(features, columns=feat_cols)
            probabilities = model.predict_proba(df_features)[0]
            # Probability of class 1 (Placed)
            probability = round(probabilities[1] * 100, 1)
        except Exception as e:
            print("Inference error:", e)
            probability = round(min(98.0, max(15.0, (form_data["cgpa"] / 10.0 * 40) + (form_data["coding_score"] * 0.35) + (form_data["projects"] * 5))), 1)
    else:
        probability = round(min(98.0, max(15.0, (form_data["cgpa"] / 10.0 * 40) + (form_data["coding_score"] * 0.35) + (form_data["projects"] * 5))), 1)

    recommendations = generate_recommendations(
        form_data["cgpa"],
        form_data["coding_score"],
        form_data["aptitude_score"],
        form_data["communication_score"],
        form_data["projects"],
        form_data["internships"]
    )

    return render_template(
        "predict_placement.html",
        student=student,
        form_data=form_data,
        probability=probability,
        recommendations=recommendations
    )


# ---------------- 2. COMPANIES & JOBS ROUTE ----------------

@app.route("/companies")
def companies_view():
    if "student_id" not in session:
        return redirect("/")

    conn = get_db()
    student = conn.execute(
        "SELECT * FROM students WHERE student_id=?",
        (session["student_id"],)
    ).fetchone()

    companies = conn.execute(
        "SELECT * FROM companies ORDER BY id ASC"
    ).fetchall()

    applied_apps = conn.execute(
        "SELECT company_id FROM applications WHERE student_id=?",
        (session["student_id"],)
    ).fetchall()
    conn.close()

    if not student:
        return redirect("/")

    applied_company_ids = [row["company_id"] for row in applied_apps]

    message = request.args.get("msg")
    error = request.args.get("err")

    return render_template(
        "companies.html",
        student=student,
        companies=companies,
        applied_company_ids=applied_company_ids,
        message=message,
        error=error
    )


# ---------------- 3. APPLY TO COMPANY ROUTE ----------------

@app.route("/apply-company/<int:company_id>", methods=["POST"])
def apply_company(company_id):
    if "student_id" not in session:
        return redirect("/")

    conn = get_db()
    student = conn.execute(
        "SELECT * FROM students WHERE student_id=?",
        (session["student_id"],)
    ).fetchone()

    company = conn.execute(
        "SELECT * FROM companies WHERE id=?",
        (company_id,)
    ).fetchone()

    if not student or not company:
        conn.close()
        return redirect("/companies")

    # Eligibility check
    if student["cgpa"] < company["min_cgpa"]:
        conn.close()
        return redirect(f"/companies?err=Your+CGPA+({student['cgpa']})+is+below+the+minimum+required+criteria+({company['min_cgpa']})+for+{company['name']}.")

    # Check if already applied
    existing = conn.execute(
        "SELECT id FROM applications WHERE student_id=? AND company_id=?",
        (session["student_id"], company_id)
    ).fetchone()

    if existing:
        conn.close()
        return redirect("/applications")

    today = datetime.now().strftime("%Y-%m-%d")
    conn.execute(
        """
        INSERT INTO applications (student_id, company_id, status, applied_date, notes)
        VALUES (?, ?, 'Applied', ?, 'Application submitted via student placement portal. Under review.')
        """,
        (session["student_id"], company_id, today)
    )
    conn.commit()
    conn.close()

    return redirect("/applications")


# ---------------- 4. APPLICATION STATUS ROUTE ----------------

@app.route("/applications")
def applications_view():
    if "student_id" not in session:
        return redirect("/")

    conn = get_db()
    student = conn.execute(
        "SELECT * FROM students WHERE student_id=?",
        (session["student_id"],)
    ).fetchone()

    applications = conn.execute(
        """
        SELECT 
            applications.id,
            applications.student_id,
            applications.company_id,
            applications.status,
            applications.applied_date,
            applications.notes,
            companies.name AS company_name,
            companies.role,
            companies.package,
            companies.location,
            companies.min_cgpa,
            companies.deadline
        FROM applications
        JOIN companies ON applications.company_id = companies.id
        WHERE applications.student_id = ?
        ORDER BY applications.id DESC
        """,
        (session["student_id"],)
    ).fetchall()
    conn.close()

    if not student:
        return redirect("/")

    return render_template(
        "applications.html",
        student=student,
        applications=applications
    )


# ---------------- 5. MODEL EVALUATION & DATASET ROUTE ----------------

@app.route("/model-analysis")
def model_analysis():
    if "student_id" not in session:
        return redirect("/")

    metrics = get_model_metrics()

    # Load records from indian_engineering_placement_2026.csv for interactive dataset explorer
    sample_students = []
    if os.path.exists(DATASET_PATH):
        try:
            with open(DATASET_PATH, "r", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                for i, row in enumerate(reader):
                    if i >= 350:
                        break
                    sample_students.append(row)
        except Exception as e:
            print("Error loading dataset:", e)

    return render_template(
        "model_analysis.html",
        metrics=metrics,
        sample_students=sample_students
    )


# ---------------- 6. ADMIN SYSTEM ROUTES ----------------

@app.route("/admin")
def admin_root():
    if "is_admin" in session:
        return redirect("/admin/dashboard")
    return redirect("/admin/login")


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if "is_admin" in session:
        return redirect("/admin/dashboard")

    error = None
    username_val = ""

    if request.method == "POST":
        username_val = request.form.get("username", "").strip()
        password_val = request.form.get("password", "").strip()

        conn = get_db()
        admin = conn.execute(
            "SELECT * FROM admins WHERE username=? AND password=?",
            (username_val, password_val)
        ).fetchone()
        conn.close()

        if admin:
            session["is_admin"] = True
            session["admin_id"] = admin["username"]
            session["admin_name"] = admin["name"]
            return redirect("/admin/dashboard")
        else:
            error = "Invalid Admin Credentials."

    return render_template("admin_login.html", error=error, username=username_val)


@app.route("/admin/logout")
def admin_logout():
    session.pop("is_admin", None)
    session.pop("admin_id", None)
    session.pop("admin_name", None)
    return redirect("/admin/login")


@app.route("/admin/dashboard")
def admin_dashboard():
    if "is_admin" not in session:
        return redirect("/admin/login")

    active_tab = request.args.get("tab", "students")
    search_query = request.args.get("q", "").strip()
    selected_branch = request.args.get("branch", "").strip()
    selected_status = request.args.get("status", "").strip()

    conn = get_db()

    # 1. High level statistics
    total_students = conn.execute("SELECT COUNT(*) FROM students").fetchone()[0]
    placed_students = conn.execute("SELECT COUNT(*) FROM students WHERE placement_status='Placed'").fetchone()[0]
    avg_pkg_row = conn.execute("SELECT AVG(package_lpa) FROM students WHERE placement_status='Placed' AND package_lpa > 0").fetchone()[0]
    avg_package = avg_pkg_row if avg_pkg_row is not None else 0.0
    top_pkg_row = conn.execute("SELECT MAX(package_lpa) FROM students").fetchone()[0]
    top_package = top_pkg_row if top_pkg_row is not None else 0.0

    # 2. Distinct branches for dropdown filter
    branch_rows = conn.execute(
        "SELECT DISTINCT branch FROM students WHERE branch IS NOT NULL AND branch != '' ORDER BY branch ASC"
    ).fetchall()
    all_branches = [r["branch"] for r in branch_rows]

    # 3. Filtered students list (cap to 150 for speedy UI rendering)
    sql = "SELECT * FROM students WHERE 1=1"
    params = []

    if search_query:
        sql += " AND (student_id LIKE ? OR name LIKE ? OR skills LIKE ?)"
        term = f"%{search_query}%"
        params.extend([term, term, term])

    if selected_branch:
        sql += " AND branch = ?"
        params.append(selected_branch)

    if selected_status:
        sql += " AND placement_status = ?"
        params.append(selected_status)

    sql += " ORDER BY student_id ASC LIMIT 150"
    students = conn.execute(sql, params).fetchall()

    # 4. Companies list
    companies = conn.execute("SELECT * FROM companies ORDER BY id ASC").fetchall()

    # 5. Student applications with student details
    applications = conn.execute("""
        SELECT 
            applications.id,
            applications.student_id,
            students.name AS student_name,
            students.cgpa AS student_cgpa,
            students.branch AS student_branch,
            applications.company_id,
            companies.name AS company_name,
            companies.role AS company_role,
            applications.status,
            applications.applied_date,
            applications.notes
        FROM applications
        JOIN students ON applications.student_id = students.student_id
        JOIN companies ON applications.company_id = companies.id
        ORDER BY applications.id DESC
    """).fetchall()

    # 6. Branch wise statistics for analytics tab
    branch_stats = conn.execute("""
        SELECT 
            branch,
            COUNT(*) AS total,
            SUM(CASE WHEN placement_status='Placed' THEN 1 ELSE 0 END) AS placed,
            AVG(cgpa) AS avg_cgpa,
            AVG(CASE WHEN placement_status='Placed' AND package_lpa > 0 THEN package_lpa ELSE 0 END) AS avg_pkg
        FROM students
        WHERE branch IS NOT NULL AND branch != ''
        GROUP BY branch
        ORDER BY total DESC
    """).fetchall()

    conn.close()

    return render_template(
        "admin_dashboard.html",
        total_students=total_students,
        placed_students=placed_students,
        avg_package=avg_package,
        top_package=top_package,
        all_branches=all_branches,
        students=students,
        companies=companies,
        applications=applications,
        branch_stats=branch_stats,
        active_tab=active_tab,
        search_query=search_query,
        selected_branch=selected_branch,
        selected_status=selected_status
    )


@app.route("/admin/company/add", methods=["POST"])
def admin_company_add():
    if "is_admin" not in session:
        return redirect("/admin/login")

    name = request.form.get("name", "").strip()
    role = request.form.get("role", "").strip()
    package = request.form.get("package", "").strip()
    min_cgpa = float(request.form.get("min_cgpa", 6.0))
    openings = int(request.form.get("openings", 5))
    location = request.form.get("location", "").strip()
    deadline = request.form.get("deadline", "").strip()
    required_skills = request.form.get("required_skills", "").strip()
    description = request.form.get("description", "").strip()

    if name and role:
        conn = get_db()
        conn.execute("""
            INSERT INTO companies (name, role, package, min_cgpa, required_skills, location, deadline, description, openings)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, role, package, min_cgpa, required_skills, location, deadline, description, openings))
        conn.commit()
        conn.close()

    return redirect("/admin/dashboard?tab=companies&msg=New+recruitment+drive+posted+successfully!")


@app.route("/admin/company/<int:comp_id>/delete", methods=["POST"])
def admin_company_delete(comp_id):
    if "is_admin" not in session:
        return redirect("/admin/login")

    conn = get_db()
    conn.execute("DELETE FROM applications WHERE company_id=?", (comp_id,))
    conn.execute("DELETE FROM companies WHERE id=?", (comp_id,))
    conn.commit()
    conn.close()

    return redirect("/admin/dashboard?tab=companies&msg=Company+drive+removed+successfully.")


@app.route("/admin/application/<int:app_id>/update", methods=["POST"])
def admin_application_update(app_id):
    if "is_admin" not in session:
        return redirect("/admin/login")

    status = request.form.get("status", "Applied").strip()

    conn = get_db()
    app_record = conn.execute("SELECT * FROM applications WHERE id=?", (app_id,)).fetchone()
    if app_record:
        conn.execute("UPDATE applications SET status=? WHERE id=?", (status, app_id))
        if status in ["Selected", "Placed"]:
            conn.execute(
                "UPDATE students SET placement_status='Placed' WHERE student_id=?",
                (app_record["student_id"],)
            )
        conn.commit()
    conn.close()

    return redirect("/admin/dashboard?tab=applications&msg=Application+status+updated+successfully!")


# ---------------- RUN FLASK ----------------

if __name__ == "__main__":
    app.run(debug=True)
