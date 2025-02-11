import random
import eel
import itertools
from collections import defaultdict

eel.init('web')

def load_people(filename):
    #file reading from chat gpt because i don't remember how to do it
    people = []
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) != 10:
                print(f"Skipping invalid line: {line.strip()}")
                continue  # Skip invalid lines
            try:
                person = {
                    'name': parts[0],
                    'studyType': parts[1],
                    'creditHours': int(parts[2]), # Ensure this is an integer
                    'major': parts[3],
                    'availability': parts[4],
                    'learnerType': parts[5],
                    'intensity': int(parts[6]),
                    'priority': parts[7],
                    'workingStyle': parts[8],
                    'environment': parts[9]
                }
                people.append(person)
            except ValueError:
                print(f"Invalid data on line: {line.strip()}")
    return people

def match_people(people, group_size):
    # weights for each trait (adjust as needed)
    weights = {
        'studyType': 10,
        'creditHours': 5,
        'major': 15,
        'availability': 20,
        'learnerType': 10,
        'intensity': 5,
        'priority': 5,
        'workingStyle': 10,
        'environment': 10
    }
    
    def calculate_compatibility(p1, p2):
        score = 0
        for key, weight in weights.items():
            if p1.get(key) == p2.get(key):
                score += weight
        return score

    groups = []
    unmatched = people[:]  # create a working copy of the list

    # While enough people remain to form a full group...
    while len(unmatched) >= group_size:
        best_group = None
        best_score = -1
        
        for group in itertools.combinations(unmatched, group_size):
            # Sum compatibility for each pair in the group
            group_score = sum(calculate_compatibility(a, b) for a, b in itertools.combinations(group, 2))
            if group_score > best_score:
                best_score = group_score
                best_group = group
        
        if best_group is None:
            break
        
        groups.append(list(best_group))
        for person in best_group:
            unmatched.remove(person)
    
    if unmatched:
        groups.append(unmatched)
    
    return groups



@eel.expose
def match_from_file(content, group_size):
    try:
        # Split the file content into lines
        lines = content.strip().split('\n')
        # Parse each line into a list of people
        people = []
        for line in lines:
            parts = line.strip().split()
            person = {
                'name': parts[0],
                'studyType': parts[1],
                'creditHours': int(parts[2]),
                'major': parts[3],
                'availability': parts[4],
                'learnerType': parts[5],
                'intensity': int(parts[6]),
                'priority': parts[7],
                'workingStyle': parts[8],
                'environment': parts[9]
            }
            people.append(person)
        groups = match_people(people, group_size)
        return [[{k: v for k, v in person.items()} for person in group] for group in groups]
    except Exception as e:
        print("Error:", e)
        return []

def main():
   eel.start('index.html', size=(800, 600), block=True)

if __name__ == "__main__":
    main()