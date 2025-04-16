import random
import json
from itertools import combinations

"""
    This file generates a huge dataset of 50 groups, 3 students each. It also generates dummy student grades and finds the 
    average grade of each group. The weights of the characteristics are all equal. 
    This file is created to represent the data we collect after releasing the base grouping algorithm for a semester. 
    After the semester is over we would like to see which groups performed better and identify any patterns in the characteristics
    of the students in those better performing groups. To do so we will link this data to generative AI. If the generative AI 
    identifies a pattern correlating characteristics with better group performance it will display it and suggest a modification 
    in the weights of the characteristics. 
    The ultimate goal is to directly link the genAI results to the grouping algorithm and have it automatically update the weights
    of the characteristics.

    For now this generated dataset purposefully gives students higher grades if they are grouped with students having the same
    learningstyle and/or availability to later see if generativeAI accurately identifies which grouped characteristics are 
    associated to higher grades/averages.
"""
def generate_students(num_students=150):
    study_types = ['EarlyRiser', 'NightOwl']
    majors = ['CS', 'MechE', 'BME', 'CompE', 'CivilE', 'EnvE', 'Business']
    availabilities = ['Weekdays(Morning)', 'Weekdays(Afternoon)', 'Weekends(Morning)', 'Weekends(Afternoon)', 'Weekends(Evening)']
    learner_types = ['Practical', 'Analytical', 'Interpersonal', 'Holistic']
    priorities = ['LearningStyle', 'Availability']
    working_styles = ['Short', 'Long']
    environments = ['Library', 'Cafe', 'Silent', 'Home']
    
    students = []
    for i in range(num_students):
        students.append({
            'index': i,
            'name': f'Student{i+1}',
            'studyType': random.choice(study_types),
            'creditHours': random.randint(10, 21),
            'major': random.choice(majors),
            'availability': random.choice(availabilities),
            'learnerType': random.choice(learner_types),
            'intensity': random.randint(1, 5),
            'priority': random.choice(priorities),
            'workingStyle': random.choice(working_styles),
            'environment': random.choice(environments),
            'grade': 0  # Will be replaced
        })
    return students

def create_groups(students, group_size=3):
    # randomly creating groups (i.e. equal weights for all characterisitcs)
    random.shuffle(students)
    groups = []
    
    group_number = 1
    for i in range(0, len(students) - group_size + 1, group_size):
        group = students[i:i + group_size]
        
        # check for same availability/learnertype
        same_availability = all(s['availability'] == group[0]['availability'] for s in group)
        same_learner_type = all(s['learnerType'] == group[0]['learnerType'] for s in group)
        
        # Giving higher grade is students have same availability/learner type, else lower
        if same_availability or same_learner_type:
            for s in group:
                s['grade'] = random.randint(80, 100)
        else:
            for s in group:
                s['grade'] = random.randint(60, 80)
        
        avg_grade = sum(s['grade'] for s in group) / group_size
        groups.append({
            'group_number': group_number,
            'members': group,
            'average_grade': avg_grade
        })
        group_number += 1
    
    return groups

def save_to_json(data, filename="student_groups2.json"):
    """Save generated groups to a JSON file."""
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Dataset saved to {filename}")

if __name__ == "__main__":
    students = generate_students()
    groups = create_groups(students)
    save_to_json(groups)