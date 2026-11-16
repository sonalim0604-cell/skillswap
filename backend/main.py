import os
from dotenv import load_dotenv
from supabase import create_client
from fastapi import FastAPI, HTTPException

load_dotenv()

url = os.getenv("NEXT_PUBLIC_SUPABASE_URL")
key = os.getenv("NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY")


supabase = create_client(url, key)

print("Supabase connected successfully!")

profiles = supabase.table("profiles").select("*").execute().data

skills = supabase.table("skills").select("*").execute().data

user_skills = supabase.table("user_skills").select("*").execute().data

print("Profiles:", profiles)
print("Skills:", skills)
print("User Skills:", user_skills)

skill_names = {
    str(skill["id"]): skill["skill_name"]
    for skill in skills
}


# Organise students and their skills

students = {}

for profile in profiles:

    user_id = str(profile["id"])

    students[user_id] = {
        "name": profile.get("full_name") or profile.get("username"),
        "teach": [],
        "learn": []
    }


# Add teaching and learning skills

for item in user_skills:

    user_id = str(item["user_id"])

    skill_id = str(item["skill_id"])

    skill_name = skill_names.get(skill_id)

    if user_id in students and skill_name:

        if item["skill_type"] == "teach":
            students[user_id]["teach"].append(skill_name)

        elif item["skill_type"] == "learn":
            students[user_id]["learn"].append(skill_name)


print("Student data:", students)

def match_score(me, other):
    score = 0

    matching_learn = set(me["learn"]) & set(other["teach"])

    if me["learn"]:
        score += (len(matching_learn) / len(me["learn"])) * 40

    matching_teach = set(me["teach"]) & set(other["learn"])

    if other["learn"]:
        score += (len(matching_teach) / len(other["learn"])) * 25

    return round(score, 2)


app = FastAPI()

@app.get("/")
def home():
    return {"message": "SkillSwap is running"}

@app.get("/matches/{user_id}")
def get_matches(user_id: str):

    if user_id not in students:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    me = students[user_id]

    if not me["teach"] and not me["learn"]:
        return []

    matches = []

    for other_id, other in students.items():

        if other_id == user_id:
            continue

        if not other["teach"] and not other["learn"]:
            continue

        score = match_score(me, other)

        matches.append({
            "user_id": other_id,
            "name": other["name"],
            "match_score": score
        })

    matches.sort(
        key=lambda x: x["match_score"],
        reverse=True
    )

    return matches[:10]