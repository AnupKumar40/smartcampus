import csv
import random

# Seed for reproducibility
random.seed(42)

# Load existing 150 students if available
existing_students = []
try:
    with open("students_150_dataset.csv", "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            existing_students.append(row)
except Exception as e:
    print(f"Notice: {e}")

first_names = [
    "Aarav", "Aditi", "Aditya", "Akash", "Aman", "Amit", "Ananya", "Ankit", "Anushka", "Aryan",
    "Ayush", "Bhavya", "Chetan", "Deepak", "Divya", "Gaurav", "Harsh", "Isha", "Ishaan", "Jatin",
    "Karan", "Khushi", "Komal", "Manish", "Mehak", "Mohit", "Muskan", "Neha", "Nikhil", "Nisha",
    "Pooja", "Pranav", "Prashant", "Priya", "Rahul", "Rhea", "Rishi", "Rohan", "Rohit", "Sakshi",
    "Sameer", "Sanjay", "Shreya", "Siddharth", "Simran", "Sneha", "Tanmay", "Utkarsh", "Varun", "Vikas"
]

last_names = [
    "Sharma", "Verma", "Gupta", "Malhotra", "Mehta", "Singh", "Patel", "Kumar", "Mishra", "Joshi",
    "Chauhan", "Bhatia", "Saxena", "Agarwal", "Bansal", "Rao", "Reddy", "Nair", "Pandey", "Trivedi"
]

courses = ["B.Tech CSE", "B.Tech IT", "BCA", "MCA", "B.Sc CS"]
skills_pool = [
    "Python, Flask", "Python, ML", "Java, Spring Boot", "Java, Web Development",
    "C++, DSA", "SQL, Excel", "Python, SQL", "Web Development, React",
    "Python, Django", "Node.js, MongoDB", "Data Analysis, Tableau", "Cloud, DevOps"
]

fees_options = [15000, 18000, 20000, 25000, 30000]

fieldnames = [
    "Student ID", "Name", "Course", "Semester", "Attendance", "CGPA",
    "Aptitude Score", "Coding Score", "Projects", "Internships",
    "Skill Count", "Communication Score", "Placement Status", "Fees", "Skills"
]

all_students = []

# Keep existing 150 students
for s in existing_students:
    all_students.append({
        "Student ID": s["Student ID"],
        "Name": s["Name"],
        "Course": s["Course"],
        "Semester": int(float(s["Semester"])),
        "Attendance": round(float(s["Attendance"]), 1),
        "CGPA": round(float(s["CGPA"]), 2),
        "Aptitude Score": round(float(s["Aptitude Score"]), 1),
        "Coding Score": round(float(s["Coding Score"]), 1),
        "Projects": int(float(s["Projects"])),
        "Internships": int(float(s["Internships"])),
        "Skill Count": int(float(s["Skill Count"])),
        "Communication Score": round(float(s["Communication Score"]), 1),
        "Placement Status": s["Placement Status"],
        "Fees": int(float(s["Fees"])),
        "Skills": s["Skills"]
    })

start_id = 1001 + len(all_students)

# Generate up to 500 total students
while len(all_students) < 500:
    student_id = start_id
    start_id += 1
    name = f"{random.choice(first_names)} {random.choice(last_names)}"
    course = random.choice(courses)
    semester = random.randint(3, 8)
    
    # Realistic academic metrics
    attendance = round(random.uniform(62.0, 97.0), 1)
    cgpa = round(random.uniform(5.5, 9.8), 2)
    aptitude = round(random.uniform(45.0, 95.0), 1)
    coding = round(random.uniform(40.0, 98.0), 1)
    projects = random.choices([0, 1, 2, 3, 4], weights=[15, 35, 30, 15, 5])[0]
    internships = random.choices([0, 1, 2, 3], weights=[45, 35, 15, 5])[0]
    
    skills_entry = random.choice(skills_pool)
    skill_count = len([x.strip() for x in skills_entry.split(",") if x.strip()]) + random.choice([0, 1, 2])
    communication = round(random.uniform(50.0, 95.0), 1)
    fees = random.choice(fees_options)
    
    # Realistic placement logic based on holistic profile
    score = (
        (cgpa / 10.0) * 0.30 +
        (coding / 100.0) * 0.25 +
        (aptitude / 100.0) * 0.15 +
        (communication / 100.0) * 0.10 +
        (projects / 4.0) * 0.10 +
        (internships / 3.0) * 0.10
    )
    
    # Add a slight noise to reflect real-world placement variance
    score += random.uniform(-0.06, 0.06)
    
    # Threshold for placement
    if score >= 0.65 and cgpa >= 6.8:
        placement_status = "Placed"
    else:
        placement_status = "Not Placed"
        
    all_students.append({
        "Student ID": student_id,
        "Name": name,
        "Course": course,
        "Semester": semester,
        "Attendance": attendance,
        "CGPA": cgpa,
        "Aptitude Score": aptitude,
        "Coding Score": coding,
        "Projects": projects,
        "Internships": internships,
        "Skill Count": skill_count,
        "Communication Score": communication,
        "Placement Status": placement_status,
        "Fees": fees,
        "Skills": skills_entry
    })

# Write to students.csv
with open("students.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(all_students)

placed_count = sum(1 for s in all_students if s["Placement Status"] == "Placed")
print(f"Generated {len(all_students)} student records in students.csv!")
print(f"Placed: {placed_count}, Not Placed: {len(all_students) - placed_count}")
