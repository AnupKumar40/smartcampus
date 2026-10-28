import sqlite3
import csv
import os
from datetime import datetime

DB_NAME = "smart_campus.db"
CSV_FILE = "indian_engineering_placement_2026.csv"

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

# ----------------- 1. ADMINS TABLE -----------------
cursor.execute("DROP TABLE IF EXISTS admins")
cursor.execute("""
CREATE TABLE admins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    name TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'Head of Placement & Corporate Relations',
    email TEXT NOT NULL
)
""")

# Seed default Admin
cursor.execute("""
INSERT INTO admins (username, password, name, role, email)
VALUES (?, ?, ?, ?, ?)
""", ("admin", "admin123", "Campus Placement Officer", "Admin / Placement Cell", "admin@smartcampus.edu"))

# ----------------- 2. STUDENTS TABLE -----------------
cursor.execute("DROP TABLE IF EXISTS students")
cursor.execute("""
CREATE TABLE students (
    student_id TEXT PRIMARY KEY,
    password TEXT NOT NULL,
    name TEXT NOT NULL,
    course TEXT NOT NULL,
    semester INTEGER NOT NULL,
    attendance REAL NOT NULL,
    cgpa REAL NOT NULL,
    aptitude_score REAL NOT NULL,
    coding_score REAL NOT NULL,
    projects INTEGER NOT NULL,
    internships INTEGER NOT NULL,
    skill_count INTEGER NOT NULL,
    communication_score REAL NOT NULL,
    placement_status TEXT NOT NULL,
    fees REAL NOT NULL,
    skills TEXT NOT NULL,
    branch TEXT,
    gender TEXT,
    state TEXT,
    college_tier TEXT,
    package_lpa REAL DEFAULT 0.0
)
""")

print(f"[INFO] Importing records from '{CSV_FILE}' into SQLite database...")
student_rows = []
with open(CSV_FILE, "r", encoding="utf-8-sig") as file:
    reader = csv.DictReader(file)
    for row in reader:
        try:
            student_id = str(row.get("Student_ID") or row.get("Username")).strip()
            password = str(row.get("Password", "12345")).strip()
            name = str(row.get("Name", "Student " + student_id)).strip()
            course = str(row.get("Course", "B.Tech " + row.get("Branch", "CSE"))).strip()
            semester = int(float(row.get("Semester", 7)))
            attendance = float(row.get("Attendance_Percentage", row.get("attendance", 75.0)))
            cgpa = float(row.get("CGPA", 7.0))
            aptitude_score = float(row.get("Aptitude_Score", 60.0))
            
            # Map DSA_Problems_Solved to coding score (scale ~0-100 for display, min 0, max 100)
            dsa_solved = float(row.get("DSA_Problems_Solved", 100))
            coding_score = round(min(100.0, max(10.0, dsa_solved / 3.0)), 1)
            
            projects = int(float(row.get("Projects_Count", 2)))
            internships = int(float(row.get("Internships_Count", 1)))
            skill_count = int(float(row.get("Certifications_Count", 3)))
            communication_score = float(row.get("Communication_Score", 65.0))
            placement_status = str(row.get("Placement_Status", "Not Placed")).strip()
            fees = float(row.get("Fees", 120000.0))
            skills = str(row.get("Skills", "Python, DSA, SQL")).strip()
            branch = str(row.get("Branch", "CSE")).strip()
            gender = str(row.get("Gender", "Not Specified")).strip()
            state = str(row.get("State", "")).strip()
            college_tier = str(row.get("College_Tier", "Tier-2")).strip()
            package_lpa = float(row.get("Package_LPA", 0.0))

            student_rows.append((
                student_id,
                password,
                name,
                course,
                semester,
                attendance,
                cgpa,
                aptitude_score,
                coding_score,
                projects,
                internships,
                skill_count,
                communication_score,
                placement_status,
                fees,
                skills,
                branch,
                gender,
                state,
                college_tier,
                package_lpa
            ))
        except Exception as e:
            continue

cursor.executemany("""
INSERT INTO students (
    student_id, password, name, course, semester, attendance, cgpa,
    aptitude_score, coding_score, projects, internships, skill_count,
    communication_score, placement_status, fees, skills, branch, gender,
    state, college_tier, package_lpa
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", student_rows)

print(f"[OK] Successfully loaded {len(student_rows)} students into database.")

# ----------------- 3. COMPANIES TABLE -----------------
cursor.execute("DROP TABLE IF EXISTS companies")
cursor.execute("""
CREATE TABLE companies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    role TEXT NOT NULL,
    package TEXT NOT NULL,
    min_cgpa REAL NOT NULL,
    required_skills TEXT NOT NULL,
    location TEXT NOT NULL,
    deadline TEXT NOT NULL,
    description TEXT,
    openings INTEGER DEFAULT 5
)
""")

sample_companies = [
    (
        "TCS",
        "Software Developer",
        "7.2 LPA",
        7.0,
        "Java, Python, SQL",
        "Pune / Bengaluru",
        "2026-11-20",
        "Development and maintenance of enterprise cloud applications.",
        15
    ),
    (
        "Infosys",
        "Specialist Programmer",
        "9.5 LPA",
        7.5,
        "Python, DSA, Web Development",
        "Bengaluru / Hyderabad",
        "2026-11-25",
        "Core engineering role building scalable backend and microservices.",
        10
    ),
    (
        "Capgemini",
        "Senior Analyst",
        "6.8 LPA",
        6.5,
        "Java, Spring Boot, React",
        "Mumbai / Noida",
        "2026-11-18",
        "Full stack agile development and client solution engineering.",
        12
    ),
    (
        "Wipro",
        "Project Engineer",
        "6.5 LPA",
        6.5,
        "C++, Python, SQL",
        "Hyderabad / Chennai",
        "2026-11-30",
        "Digital transformation and automation engineering team.",
        20
    ),
    (
        "Accenture",
        "Associate Software Engineer",
        "8.0 LPA",
        7.0,
        "Cloud, DevOps, Python",
        "Gurugram / Bengaluru",
        "2026-12-05",
        "Modern application development and cloud migration initiatives.",
        18
    ),
    (
        "Microsoft",
        "Associate SWE Intern",
        "18.0 LPA",
        8.5,
        "DSA, System Design, C++, Python",
        "Hyderabad / Remote",
        "2026-12-10",
        "High-performance distributed systems engineering and AI tooling.",
        5
    ),
    (
        "Cognizant",
        "GenC Next Developer",
        "7.0 LPA",
        6.8,
        "Python, Flask, SQL, Web Development",
        "Kolkata / Chennai",
        "2026-11-28",
        "End-to-end web architecture and API development projects.",
        14
    )
]

cursor.executemany("""
INSERT INTO companies (name, role, package, min_cgpa, required_skills, location, deadline, description, openings)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
""", sample_companies)

# ----------------- 4. APPLICATIONS TABLE -----------------
cursor.execute("DROP TABLE IF EXISTS applications")
cursor.execute("""
CREATE TABLE applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT NOT NULL,
    company_id INTEGER NOT NULL,
    status TEXT NOT NULL DEFAULT 'Applied',
    applied_date TEXT NOT NULL,
    notes TEXT,
    UNIQUE(student_id, company_id),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (company_id) REFERENCES companies(id)
)
""")

# Seed initial applications for demo student ST00001
today = datetime.now().strftime("%Y-%m-%d")
sample_apps = [
    ("ST00001", 1, "Interview", today, "Technical interview scheduled for Round 2."),
    ("ST00001", 3, "Shortlisted", today, "Shortlisted based on CGPA and aptitude score."),
    ("ST00001", 4, "Applied", today, "Application received. Document verification in progress.")
]

cursor.executemany("""
INSERT INTO applications (student_id, company_id, status, applied_date, notes)
VALUES (?, ?, ?, ?, ?)
""", sample_apps)

conn.commit()

cursor.execute("SELECT COUNT(*) FROM students")
student_count = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM companies")
company_count = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM applications")
app_count = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM admins")
admin_count = cursor.fetchone()[0]

print("==================================================")
print("[OK] Smart Campus Database setup completed successfully!")
print(f"Total students in DB   : {student_count}")
print(f"Total companies active : {company_count}")
print(f"Total applications     : {app_count}")
print(f"Total admins active    : {admin_count}")
print("Admin Credentials      : admin / admin123")
print("Student Credentials    : ST00001 / 12345 (and ST00002, etc.)")
print("==================================================")

conn.close()