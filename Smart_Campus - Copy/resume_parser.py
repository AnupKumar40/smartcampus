import re
import math
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# -------------------------------------------------------------
# Comprehensive Curated Skill Catalog
# -------------------------------------------------------------
TECH_SKILLS = {
    # Programming Languages
    "python": "Python", "java": "Java", "c++": "C++", "cpp": "C++", "c#": "C#", "c": "C",
    "javascript": "JavaScript", "typescript": "TypeScript", "php": "PHP", "ruby": "Ruby",
    "go": "Go", "golang": "Go", "rust": "Rust", "kotlin": "Kotlin", "swift": "Swift",
    "r": "R", "scala": "Scala", "dart": "Dart", "sql": "SQL", "html": "HTML", "html5": "HTML5",
    "css": "CSS", "css3": "CSS3",

    # Frameworks & Libraries
    "react": "React", "react.js": "React", "reactjs": "React",
    "angular": "Angular", "vue": "Vue.js", "vue.js": "Vue.js",
    "node": "Node.js", "node.js": "Node.js", "nodejs": "Node.js",
    "express": "Express.js", "express.js": "Express.js",
    "flask": "Flask", "django": "Django", "fastapi": "FastAPI",
    "spring": "Spring", "spring boot": "Spring Boot", "hibernate": "Hibernate",
    "bootstrap": "Bootstrap", "tailwind": "Tailwind CSS", "tailwindcss": "Tailwind CSS",
    "jquery": "jQuery", "next.js": "Next.js", "nextjs": "Next.js",
    ".net": ".NET", "asp.net": "ASP.NET",

    # AI / ML / Data Science
    "machine learning": "Machine Learning", "ml": "Machine Learning",
    "artificial intelligence": "Artificial Intelligence", "ai": "Artificial Intelligence",
    "deep learning": "Deep Learning", "neural networks": "Neural Networks",
    "data science": "Data Science", "data analysis": "Data Analysis", "data analytics": "Data Analytics",
    "nlp": "Natural Language Processing", "natural language processing": "Natural Language Processing",
    "computer vision": "Computer Vision", "opencv": "OpenCV",
    "tensorflow": "TensorFlow", "pytorch": "PyTorch", "keras": "Keras",
    "scikit-learn": "Scikit-Learn", "sklearn": "Scikit-Learn",
    "pandas": "Pandas", "numpy": "NumPy", "scipy": "SciPy", "matplotlib": "Matplotlib", "seaborn": "Seaborn",
    "nltk": "NLTK", "spacy": "spaCy", "huggingface": "HuggingFace", "llm": "LLMs",

    # Databases
    "mysql": "MySQL", "postgresql": "PostgreSQL", "postgres": "PostgreSQL",
    "mongodb": "MongoDB", "sqlite": "SQLite", "oracle": "Oracle",
    "redis": "Redis", "cassandra": "Cassandra", "firebase": "Firebase",
    "dynamodb": "DynamoDB", "mariadb": "MariaDB",

    # Cloud & DevOps & Tools
    "aws": "AWS", "amazon web services": "AWS", "azure": "Azure", "microsoft azure": "Azure",
    "gcp": "Google Cloud", "google cloud": "Google Cloud",
    "docker": "Docker", "kubernetes": "Kubernetes", "jenkins": "Jenkins",
    "ci/cd": "CI/CD", "git": "Git", "github": "GitHub", "gitlab": "GitLab",
    "linux": "Linux", "unix": "Unix", "ubuntu": "Ubuntu",
    "nginx": "Nginx", "apache": "Apache", "terraform": "Terraform", "ansible": "Ansible",

    # Core Computer Science
    "data structures": "Data Structures", "algorithms": "Algorithms", "dsa": "DSA",
    "oop": "OOP", "object oriented programming": "OOP",
    "system design": "System Design", "operating systems": "Operating Systems",
    "computer networks": "Computer Networks", "dbms": "DBMS",
    "software engineering": "Software Engineering", "sdlc": "SDLC",
    "agile": "Agile", "scrum": "Scrum",
    "rest api": "REST API", "restful api": "REST API", "rest apis": "REST API",
    "microservices": "Microservices", "graphql": "GraphQL",
    "web development": "Web Development", "full stack": "Full Stack", "frontend": "Frontend", "backend": "Backend"
}

SOFT_SKILLS = {
    "communication": "Communication",
    "communication skills": "Communication",
    "leadership": "Leadership",
    "teamwork": "Teamwork",
    "problem solving": "Problem Solving",
    "critical thinking": "Critical Thinking",
    "time management": "Time Management",
    "adaptability": "Adaptability",
    "collaboration": "Collaboration",
    "presentation": "Presentation",
    "analytical skills": "Analytical Skills",
    "decision making": "Decision Making",
    "work ethic": "Work Ethic",
    "creativity": "Creativity",
    "project management": "Project Management",
    "interpersonal skills": "Interpersonal Skills"
}

ACTION_VERBS = [
    "developed", "created", "designed", "implemented", "built", "engineered", "optimized",
    "architected", "deployed", "managed", "led", "spearheaded", "automated", "improved",
    "integrated", "analyzed", "reduced", "increased", "maintained", "collaborated", "trained"
]

DEGREE_PATTERNS = [
    r"\bB\.?\s*Tech(?:\.|\b)",
    r"\bB\.E\.(?:\b|\s)",
    r"\bBachelor of Engineering\b",
    r"\bBachelor of Technology\b",
    r"\bM\.?\s*Tech(?:\.|\b)",
    r"\bM\.E\.(?:\b|\s)",
    r"\bMaster of Engineering\b",
    r"\bMaster of Technology\b",
    r"\bBCA\b",
    r"\bMCA\b",
    r"\bB\.?\s*Sc(?:\.|\b)",
    r"\bM\.?\s*Sc(?:\.|\b)",
    r"\bMBA\b",
    r"\bBBA\b",
    r"\bDiploma in Engineering\b"
]


def extract_skills_from_text(text):
    """
    Extracts technical and soft skills from raw text using boundary-safe regex.
    Returns normalized canonical skill names (unique).
    """
    if not text:
        return {"technical": [], "soft": [], "all": []}

    lower_text = " " + text.lower() + " "
    # Replace non-alphanumeric except common skill chars (+, #, ., -, /) with space
    cleaned = re.sub(r"[^\w\+\#\.\-\/]", " ", lower_text)

    found_tech = {}
    for phrase, canonical in TECH_SKILLS.items():
        # Match phrase with word boundaries or punctuation boundaries
        pattern = r"(?<![\w\+\#])" + re.escape(phrase) + r"(?![\w\+\#])"
        if re.search(pattern, cleaned):
            found_tech[canonical] = True

    found_soft = {}
    for phrase, canonical in SOFT_SKILLS.items():
        pattern = r"(?<!\w)" + re.escape(phrase) + r"(?!\w)"
        if re.search(pattern, cleaned):
            found_soft[canonical] = True

    return {
        "technical": sorted(list(found_tech.keys())),
        "soft": sorted(list(found_soft.keys())),
        "all": sorted(list(found_tech.keys()) + list(found_soft.keys()))
    }


def parse_resume(text):
    """
    Extracts structured information from resume text:
    - Contact Details (Email, Phone, Links)
    - Education details (Degrees, CGPA, College mentions)
    - Skills (Technical & Soft)
    - Experience / Internships
    - Projects
    - Formatting & Quality Metrics
    """
    if not text:
        text = ""

    # Contact: Email
    email_match = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
    email = email_match[0] if email_match else None

    # Contact: Phone
    phone_match = re.findall(r"(?:(?:\+?91[\-\s]?)?[6-9]\d{9})|(?:\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})", text)
    phone = phone_match[0] if phone_match else None

    # Contact: Links
    linkedin_match = re.findall(r"(?:https?:\/\/)?(?:www\.)?linkedin\.com\/[a-zA-Z0-9_\-\/]+", text, re.IGNORECASE)
    github_match = re.findall(r"(?:https?:\/\/)?(?:www\.)?github\.com\/[a-zA-Z0-9_\-\/]+", text, re.IGNORECASE)

    # Education: Degrees
    degrees_found = []
    for pat in DEGREE_PATTERNS:
        matches = re.findall(pat, text, re.IGNORECASE)
        for m in matches:
            clean_deg = m.strip()
            if clean_deg.upper() not in [d.upper() for d in degrees_found]:
                degrees_found.append(clean_deg)

    # Education: CGPA / Percentage
    cgpa_match = re.findall(r"(?:cgpa|gpa|percentage|aggregate)[\s:\-=]*([0-9]{1,2}(?:\.[0-9]{1,2})?%?)", text, re.IGNORECASE)
    cgpa = cgpa_match[0] if cgpa_match else None

    # Skills
    skills = extract_skills_from_text(text)

    # Sections detection
    lower = text.lower()
    has_contact = bool(email or phone or linkedin_match or github_match)
    has_education = bool("education" in lower or "academics" in lower or degrees_found)
    has_skills = bool("skill" in lower or len(skills["all"]) >= 3)
    has_projects = bool("project" in lower or "academic projects" in lower)
    has_experience = bool("experience" in lower or "internship" in lower or "work history" in lower)
    has_certifications = bool("certification" in lower or "certificate" in lower or "achievements" in lower)

    # Action verbs check
    verbs_found = [verb for verb in ACTION_VERBS if re.search(r"\b" + verb + r"\b", lower)]

    # Quantifiable metrics check (e.g. 25%, $5000, 10x, 100+ users, 500 records)
    metrics_match = re.findall(r"(?:\b\d+%\b|\b\d+\+\b|\b\d+x\b|\b\d+\s*(?:users|clients|records|downloads|ms|seconds|students|teams)\b)", text, re.IGNORECASE)

    word_count = len(text.split())

    # Resume completeness score (out of 100)
    completeness = 0
    if has_contact: completeness += 20
    if has_education: completeness += 20
    if has_skills: completeness += 20
    if has_projects: completeness += 20
    if has_experience: completeness += 10
    if has_certifications: completeness += 10

    return {
        "email": email,
        "phone": phone,
        "linkedin": linkedin_match[0] if linkedin_match else None,
        "github": github_match[0] if github_match else None,
        "degrees": degrees_found,
        "cgpa": cgpa,
        "skills": skills,
        "word_count": word_count,
        "sections": {
            "contact": has_contact,
            "education": has_education,
            "skills": has_skills,
            "projects": has_projects,
            "experience": has_experience,
            "certifications": has_certifications
        },
        "action_verbs": verbs_found,
        "quantifiable_metrics": metrics_match[:6],
        "completeness_score": completeness
    }


def analyze_resume_vs_job(resume_text, job_description):
    """
    Performs comprehensive AI/NLP comparison between Resume text and Job Description.
    Calculates:
    - Overall ATS Compatibility Score (0 - 100)
    - Skill Match (Matched Skills, Missing Skills, Extra Skills)
    - TF-IDF Cosine Similarity
    - Important Keyword Analysis
    - Resume Audit (Strengths & Warnings)
    - Personalized Actionable Recommendations
    """
    resume_parsed = parse_resume(resume_text)
    jd_skills = extract_skills_from_text(job_description)

    resume_all_skills = set(resume_parsed["skills"]["all"])
    jd_all_skills = set(jd_skills["all"])
    jd_tech_skills = set(jd_skills["technical"])

    # 1. Skill Matching
    if jd_all_skills:
        matched_skills = sorted(list(resume_all_skills.intersection(jd_all_skills)))
        missing_skills = sorted(list(jd_all_skills.difference(resume_all_skills)))
        skill_match_pct = round((len(matched_skills) / len(jd_all_skills)) * 100, 1)
    else:
        # If JD didn't explicitly list recognizable skills, fallback to resume skills present
        matched_skills = resume_parsed["skills"]["technical"][:6]
        missing_skills = []
        skill_match_pct = 75.0

    extra_skills = sorted(list(resume_all_skills.difference(jd_all_skills)))

    # 2. TF-IDF Semantic & Keyword Cosine Similarity
    cosine_pct = 0.0
    extracted_keywords = []
    try:
        corpus = [resume_text, job_description]
        tfidf = TfidfVectorizer(
            stop_words="english",
            max_features=40,
            ngram_range=(1, 2)
        )
        tfidf_matrix = tfidf.fit_transform(corpus)
        sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        cosine_pct = round(float(sim) * 100, 1)

        feature_names = tfidf.get_feature_names_out()
        # Get top weights in JD
        jd_vector = tfidf_matrix[1].toarray()[0]
        resume_vector = tfidf_matrix[0].toarray()[0]

        for i, word in enumerate(feature_names):
            if jd_vector[i] > 0:
                is_present = resume_vector[i] > 0
                extracted_keywords.append({
                    "keyword": word,
                    "importance": round(float(jd_vector[i]), 2),
                    "present": is_present
                })

        # Sort keywords by importance in JD
        extracted_keywords.sort(key=lambda x: x["importance"], reverse=True)
    except Exception as e:
        print("TF-IDF calculation note:", e)
        cosine_pct = 50.0

    # 3. Overall Weighted ATS Score
    # Weights: Skill Match: 45%, Cosine Similarity: 30%, Completeness: 15%, Formatting/Metrics: 10%
    formatting_bonus = min(100, (len(resume_parsed["action_verbs"]) * 10) + (len(resume_parsed["quantifiable_metrics"]) * 15))
    completeness_score = resume_parsed["completeness_score"]

    raw_score = (
        (skill_match_pct * 0.45) +
        (cosine_pct * 0.30) +
        (completeness_score * 0.15) +
        (formatting_bonus * 0.10)
    )
    ats_score = int(min(98, max(20, round(raw_score))))

    # Rating determination
    if ats_score >= 80:
        rating = "Excellent Match"
        status_color = "#28a745"
        summary = "Your resume is strongly optimized for this role and has a high likelihood of clearing ATS filters."
    elif ats_score >= 65:
        rating = "Good / Competitive"
        status_color = "#17a2b8"
        summary = "Your resume has a solid match with the job role. Adding a few missing skills and keywords will make it top-tier."
    elif ats_score >= 45:
        rating = "Moderate Match"
        status_color = "#ffc107"
        summary = "Your resume matches fundamental areas but has key skill gaps compared to the job description."
    else:
        rating = "Needs Significant Optimization"
        status_color = "#dc3545"
        summary = "Your resume lacks several required technical keywords and qualifications for this specific position."

    # 4. Actionable AI Improvement Suggestions
    suggestions = []

    if missing_skills:
        top_missing = missing_skills[:4]
        suggestions.append({
            "type": "critical",
            "title": "Add Missing Critical Skills",
            "detail": f"The job description specifically demands {', '.join(top_missing)}. If you have experience in these areas, make sure they appear prominently in your Skills and Projects sections."
        })

    missing_kw = [k["keyword"] for k in extracted_keywords if not k["present"]][:4]
    if missing_kw:
        suggestions.append({
            "type": "keyword",
            "title": "Incorporate High-Impact JD Keywords",
            "detail": f"Keywords such as '{', '.join(missing_kw)}' have strong weight in this job posting. Weaving them naturally into your project descriptions will significantly boost your ATS keyword score."
        })

    if not resume_parsed["quantifiable_metrics"]:
        suggestions.append({
            "type": "impact",
            "title": "Quantify Achievements with Metrics",
            "detail": "Include numerical results in your project descriptions (e.g., 'Improved performance by 30%', 'Handled 500+ database records', 'Cut loading time by 1.5s') to stand out to recruiters."
        })

    if len(resume_parsed["action_verbs"]) < 3:
        suggestions.append({
            "type": "action_verbs",
            "title": "Use Stronger Action Verbs",
            "detail": "Begin your bullet points with dynamic engineering action verbs such as 'Architected', 'Engineered', 'Optimized', 'Integrated', or 'Spearheaded' instead of passive phrasing."
        })

    if not resume_parsed["sections"]["projects"]:
        suggestions.append({
            "type": "section",
            "title": "Add a Dedicated Projects Section",
            "detail": "Technical recruiters and ATS screeners prioritize hands-on projects. Add at least 2 relevant projects with technology stacks and GitHub links."
        })

    if not resume_parsed["sections"]["experience"]:
        suggestions.append({
            "type": "section",
            "title": "Highlight Internships or Practical Experience",
            "detail": "Include internships, college lab roles, open-source contributions, or freelance projects under an Experience/Internship heading."
        })

    if resume_parsed["word_count"] < 150:
        suggestions.append({
            "type": "length",
            "title": "Expand Resume Content",
            "detail": "Your resume text appears very brief. An optimal single-page technical resume contains approximately 350 to 600 words covering education, skills, projects, and achievements."
        })

    return {
        "ats_score": ats_score,
        "rating": rating,
        "status_color": status_color,
        "summary": summary,
        "skill_match_pct": skill_match_pct,
        "cosine_similarity_pct": cosine_pct,
        "completeness_score": completeness_score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "extra_skills": extra_skills[:8],
        "keywords": extracted_keywords[:15],
        "resume_parsed": resume_parsed,
        "suggestions": suggestions
    }


def calculate_company_matches(resume_text, companies_list):
    """
    Computes real-time match scores against all campus companies.
    Returns sorted list of companies by match percentage.
    """
    if not resume_text:
        return []

    resume_skills = set(extract_skills_from_text(resume_text)["all"])
    results = []

    for comp in companies_list:
        comp_dict = dict(comp)
        req_text = f"{comp_dict.get('role', '')} {comp_dict.get('required_skills', '')} {comp_dict.get('description', '')}"
        comp_skills = set(extract_skills_from_text(req_text)["all"])

        if comp_skills:
            matched = sorted(list(resume_skills.intersection(comp_skills)))
            missing = sorted(list(comp_skills.difference(resume_skills)))
            score = round((len(matched) / len(comp_skills)) * 100)
        else:
            matched = []
            missing = []
            score = 60

        comp_dict["ats_match"] = max(15, min(98, score))
        comp_dict["matched_skills"] = matched
        comp_dict["missing_skills"] = missing
        results.append(comp_dict)

    results.sort(key=lambda x: x["ats_match"], reverse=True)
    return results

