import pandas as pd

def load_skills():

    skills = pd.read_csv(
        "data/skills.csv",
        header=None
    )

    skills = skills[0].str.lower().tolist()

    return skills


def extract_skills(text):

    text = text.lower()

    skills_database = load_skills()

    found_skills = []

    for skill in skills_database:

        if skill in text:

            found_skills.append(skill)

    return sorted(list(set(found_skills)))