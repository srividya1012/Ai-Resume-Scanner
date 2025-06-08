import PyPDF2
import re

def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def parse_resume(text):
    # Define skills to look for
    skill_keywords = [
        "Python", "Java", "C++", "JavaScript", "SQL", "Git", "AWS", "Docker",
        "Machine Learning", "Pandas", "NumPy", "TensorFlow", "Statistics",
        "Project Management", "Agile", "Scrum", "Stakeholder Management", "UX",
        "SEO", "Content Marketing", "Social Media", "Google Analytics", "Branding",
        "Kubernetes", "CI/CD", "Linux", "Terraform", "Ansible"
    ]

    # Extract skills (case-insensitive keyword matching)
    skills = []
    for skill in skill_keywords:
        if re.search(r'\b' + re.escape(skill) + r'\b', text, re.IGNORECASE):
            if skill not in skills:
                skills.append(skill)

    # Extract education (match degrees and institutions)
    education_pattern = r"(Bachelor|Master|Ph\.D|B\.Sc|M\.Sc)\s*(?:of)?\s*[\w\s]+?(?:University|Institute|College)?[^\n]*"
    education_matches = re.findall(education_pattern, text, re.IGNORECASE)
    education = education_matches if education_matches else ["Not found"]

    # Extract experience (match sections labeled "Experience", "Work History", etc.)
    experience_pattern = r"(Experience|Work History|Employment)[\s\S]*?(?=(Education|Skills|$))"
    experience_match = re.search(experience_pattern, text, re.IGNORECASE)
    experience = experience_match.group(0).split("\n")[:3] if experience_match else ["Not found"]

    return {
        "skills": skills,
        "education": education,
        "experience": experience
    }