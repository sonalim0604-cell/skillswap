def match_score(me, other):
    score = 0

    # Check skills I want to learn
    matching_learn = set(me["learn"]) & set(other["teach"])

    if me["learn"]:
        score += (len(matching_learn) / len(me["learn"])) * 40

    # Check skills the other student wants to learn
    matching_teach = set(me["teach"]) & set(other["learn"])

    if other["learn"]:
        score += (len(matching_teach) / len(other["learn"])) * 25

    # Check whether they attend the same college
    if me["college"] == other["college"]:
        score += 15

    # Check whether they are free on the same day
    common_days = set(me["free_days"]) & set(other["free_days"])

    if common_days:
        score += 10

    # Check whether they have the same skill level
    if me["level"] == other["level"]:
        score += 10

    return round(score, 2)


# Student 1
sonam = {
    "name": "Sonam",
    "college": "ABC College",
    "teach": ["Python", "Biology"],
    "learn": ["Machine Learning", "Python"],
    "free_days": ["Monday", "Wednesday"],
    "level": "Beginner"
}

# Student 2
priya = {
    "name": "Priya",
    "college": "XYZ College",
    "teach": ["Biology", "Python"],
    "learn": ["Machine Learning", "Python"],
    "free_days": ["Friday", "Saturday"],
    "level": "Beginner"
}


# Test the function
result = match_score(sonam, priya)

print("Student 1:", sonam["name"])
print("Student 2:", priya["name"])
print("Match Score:", result, "/ 100")