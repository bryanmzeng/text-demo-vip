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

def get_shared_characteristics(group):
    if not group["members"]:
        return []

    characteristics = [
        "studyType", "creditHours", "major", "availability",
        "learnerType", "intensity", "workingStyle", "environment"
    ]

    shared = []
    for char in characteristics:
        values = [member[char] for member in group["members"]]
        if all(value == values[0] for value in values):
            shared.append(char)
    return shared

# Analyzing and printing shared characteristics for high-performing groups
print("\n---\nHigh-Performing Groups Analysis:\n")
for group in high_perf_groups:
    shared = get_shared_characteristics(group)
    print(f"Group {group['group_number']}:")
    print(f"- Average Grade: {round(group['average_grade'], 2)}")
    print(f"- Shared Characteristics: {shared}\n")