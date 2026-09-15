# ai_resume_analyzer.py

import re
import PyPDF2

# Skills database
SKILLS = [
    "python", "java", "c", "c++", "c#", "javascript", "typescript",
    "html", "css", "react", "angular", "node.js", "sql", "mysql",
    "mongodb", "postgresql", "machine learning", "deep learning",
    "artificial intelligence", "data science", "pandas", "numpy",
    "tensorflow", "pytorch", "flask", "django", "git", "github",
    "docker", "aws", "azure", "power bi", "excel", "nlp"
]


def extract_text_from_pdf(file_path):
    """Extract text from a PDF resume."""
    text = ""

    try:
        with open(file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)

            for page in reader.pages:
                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

    except Exception as e:
        print("Error reading PDF:", e)

    return text


def find_skills(text):
    """Find known skills in the resume/job description."""
    text = text.lower()
    found_skills = []

    for skill in SKILLS:
        if skill.lower() in text:
            found_skills.append(skill)

    return sorted(set(found_skills))


def calculate_match(resume_skills, job_skills):
    """Calculate resume-to-job skill match percentage."""
    if not job_skills:
        return 0

    matched = set(resume_skills).intersection(set(job_skills))

    score = (len(matched) / len(set(job_skills))) * 100

    return round(score, 2)


def analyze_resume(resume_text, job_description):
    resume_skills = find_skills(resume_text)
    job_skills = find_skills(job_description)

    matched_skills = sorted(
        set(resume_skills).intersection(set(job_skills))
    )

    missing_skills = sorted(
        set(job_skills) - set(resume_skills)
    )

    score = calculate_match(resume_skills, job_skills)

    return {
        "resume_skills": resume_skills,
        "job_skills": job_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "score": score
    }


def display_result(result):
    print("\n========== AI RESUME ANALYZER ==========")

    print("\nResume Skills:")
    print(", ".join(result["resume_skills"]) or "No skills detected")

    print("\nRequired Job Skills:")
    print(", ".join(result["job_skills"]) or "No skills detected")

    print("\nMatched Skills:")
    print(", ".join(result["matched_skills"]) or "None")

    print("\nMissing Skills:")
    print(", ".join(result["missing_skills"]) or "None")

    print("\nResume Match Score:")
    print(f"{result['score']}%")

    print("\nRecommendation:")

    if result["score"] >= 80:
        print("Excellent match! Your resume is highly relevant to this job.")
    elif result["score"] >= 60:
        print("Good match. Consider improving your resume with the missing skills.")
    elif result["score"] >= 40:
        print("Moderate match. Add relevant projects, skills, and experience.")
    else:
        print("Low match. Consider gaining more relevant skills and experience.")

    print("========================================")


# ---------------- MAIN PROGRAM ----------------

if __name__ == "__main__":

    resume_path = input("Enter resume PDF path: ")

    print("\nEnter the job description.")
    print("Type END on a new line when finished.\n")

    job_lines = []

    while True:
        line = input()

        if line.strip().upper() == "END":
            break

        job_lines.append(line)

    job_description = "\n".join(job_lines)

    print("\nAnalyzing resume...")

    resume_text = extract_text_from_pdf(resume_path)

    if not resume_text:
        print("Could not extract text from resume.")
    else:
        result = analyze_resume(
            resume_text,
            job_description
        )

        display_result(result)