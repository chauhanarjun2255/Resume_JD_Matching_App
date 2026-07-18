import re

# ... existing scoring functions ...


def similarity_level(score):

    if score >= 90:
        return "Excellent Match"

    elif score >= 75:
        return "Good Match"

    elif score >= 60:
        return "Average Match"

    elif score >= 40:
        return "Weak Match"

    else:
        return "Poor Match"
    

def skill_match_score(resume_skills, jd_skills):
    """
    Calculate skill match percentage.
    """

    if len(jd_skills) == 0:
        return 0

    matched = set(resume_skills).intersection(set(jd_skills))

    score = (len(matched) / len(jd_skills)) * 100

    return round(score, 2)


def extract_years(text):
    """
    Extract years of experience from text.
    """

    text = text.lower()

    patterns = [
        r'(\d+)\+?\s*years',
        r'(\d+)\+?\s*yrs',
        r'(\d+)\+?\s*year'
    ]

    for pattern in patterns:

        match = re.search(pattern, text)

        if match:
            return int(match.group(1))

    return 0


def experience_score(resume_text, jd_text):

    resume_years = extract_years(resume_text)

    jd_years = extract_years(jd_text)

    if jd_years == 0:
        return 100

    if resume_years >= jd_years:
        return 100

    return round((resume_years / jd_years) * 100, 2)


def education_score(resume_text, jd_text):

    degrees = [
        "b.e",
        "b.tech",
        "bachelor",
        "m.e",
        "m.tech",
        "master",
        "phd"
    ]

    resume = resume_text.lower()

    jd = jd_text.lower()

    for degree in degrees:

        if degree in jd and degree in resume:
            return 100

    return 50


def final_score(
    skill_score,
    semantic_score,
    experience_score_value,
    education_score_value
):

    score = (
        skill_score * 0.50 +
        semantic_score * 0.30 +
        experience_score_value * 0.10 +
        education_score_value * 0.10
    )

    return round(score, 2)