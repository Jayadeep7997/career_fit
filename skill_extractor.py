from roles import role_profiles

def extract_skills(text):

    skills_found = []

    for role in role_profiles.values():
        for skill in role["core_skills"]:
            if skill.lower() in text.lower():
                skills_found.append(skill)

    return list(set(skills_found))