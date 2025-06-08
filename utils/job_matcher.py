import json
import os

def load_job_roles():
    with open("data/job_roles.json", "r") as f:
        return json.load(f)

def suggest_job_roles(skills):
    job_roles = load_job_roles()
    suggestions = []
    for role, required_skills in job_roles.items():
        matched_skills = [skill for skill in skills if skill in required_skills]
        match_score = len(matched_skills) / len(required_skills) * 100
        if match_score > 20:  # Threshold for suggestion
            suggestions.append({"role": role, "match_score": round(match_score, 2), "matched_skills": matched_skills})
    return sorted(suggestions, key=lambda x: x["match_score"], reverse=True)