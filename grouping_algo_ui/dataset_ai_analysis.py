import json
import subprocess

'''
This file links student_groups.json to the local AI model and prompts it to identify patterns between characteristics availability, learner type, study style, intensity) and academic performance.
'''

with open("student_groups2.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Filtering json file to get high-performing groups
def get_high_performing_groups(groups, threshold=80):
    return [group for group in groups if group["average_grade"] >= threshold]

high_perf_groups = get_high_performing_groups(data)

prompt = f"""
You are analyzing student study groups. Each group contains multiple students. Each student has a set of characteristics and a final grade.

Your task is simple:

1. For each group listed below, compare the students **within that group only** and identify which of the following characteristics are **exactly the same for all members**:
   - studyType
   - creditHours
   - major
   - availability
   - learnerType
   - intensity
   - workingStyle
   - environment

2. Do not include any explanation, commentary, or summary — just output your analysis in the format below.

3. Use the following example as a guide:

Example Group:
{{
    "group_number": 19,
    "members": [
        {{
            "index": 98,
            "name": "Student99",
            "studyType": "NightOwl",
            "creditHours": 17,
            "major": "MechE",
            "availability": "Weekdays(Morning)",
            "learnerType": "Analytical",
            "intensity": 5,
            "priority": "LearningStyle",
            "workingStyle": "Long",
            "environment": "Cafe",
            "grade": 96
        }},
        {{
            "index": 51,
            "name": "Student52",
            "studyType": "NightOwl",
            "creditHours": 13,
            "major": "CS",
            "availability": "Weekends(Morning)",
            "learnerType": "Analytical",
            "intensity": 3,
            "priority": "Availability",
            "workingStyle": "Short",
            "environment": "Home",
            "grade": 91
        }},
        {{
            "index": 141,
            "name": "Student142",
            "studyType": "NightOwl",
            "creditHours": 15,
            "major": "CivilE",
            "availability": "Weekdays(Morning)",
            "learnerType": "Analytical",
            "intensity": 1,
            "priority": "LearningStyle",
            "workingStyle": "Long",
            "environment": "Home",
            "grade": 84
        }}
    ],
    "average_grade": 90.33
}}

Expected Output:
Group 19:  
- Average Grade: 90.33  
- Shared Characteristics: [studyType, learnerType]

4. Return your results in the following format — no extra commentary or explanation, just the structure:

---
High-Performing Groups Analysis:

Group [X]:  
- Average Grade: [XX.X]  
- Shared Characteristics: [list of exact-matching characteristics for all group members]

Group [Y]:  
- Average Grade: [XX.X]  
- Shared Characteristics: [list of exact-matching characteristics for all group members]
---

Here are the high-performing groups:
{json.dumps(high_perf_groups, indent=2)}
"""

response = subprocess.run(
    ["ollama", "run", "mistral", prompt],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    encoding="utf-8"
)
print("High-performing groups:", len(high_perf_groups))
print(response.stdout)