def calculate_ats_score(text, skills):
    score = 0
    max_score = 100

    # Keyword density (40% of score)
    keyword_count = len(skills)
    total_words = len(text.split())
    keyword_density = keyword_count / total_words if total_words > 0 else 0
    score += min(keyword_density * 400, 40)  # Max 40 points

    # Resume length (30% of score)
    if 300 <= total_words <= 700:
        score += 30
    elif 200 <= total_words < 300 or 700 < total_words <= 900:
        score += 15

    # Formatting (20% of score)
    if len(skills) > 5:  # Assumes clear skills section
        score += 10
    if "Education" in text and "Experience" in text:  # Assumes clear sections
        score += 10

    # Contact info presence (10% of score)
    if any(keyword in text.lower() for keyword in ["email", "phone", "linkedin"]):
        score += 10

    return round(score, 2)