import random
import eel
import itertools
from collections import defaultdict

eel.init('web')

def load_people(filename):
    people = []
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) != 14:
                print(f"Skipping invalid line: {line.strip()}")
                continue  # Skip invalid lines
            try:
                person = {
                    'index': len(people),
                    'name': parts[0],
                    'studyType': parts[1],
                    'creditHours': int(parts[2]), # Ensure this is an integer
                    'major': parts[3],
                    'availability': parts[4],
                    'learnerType': parts[5],
                    'intensity': int(parts[6]),
                    'priority': parts[7],
                    'workingStyle': parts[8],
                    'environment': parts[9],
                    # the following attributes aren't considered in the algo, its data the facilitating interactions group needs collected
                    'gender': parts[10],
                    'minor': parts[11],
                    'year': parts[12],
                    'interests': parts[13]
                }
                people.append(person)
            except ValueError:
                print(f"Invalid data on line: {line.strip()}")
    return people


def calculate_compatibility(user1, user2, weights1, weights2):
    features = [
        (user1['studyType'] == user2['studyType']),
        abs(user1['creditHours'] - user2['creditHours']) / max(user1['creditHours'], user2['creditHours']),
        (user1['major'] == user2['major']),
        (user1['availability'] == user2['availability']),
        (user1['learnerType'] == user2['learnerType']),
        abs(user1['intensity'] - user2['intensity']) / max(user1['intensity'], user2['intensity']),
        (user1['priority'] == user2['priority']),
        (user1['workingStyle'] == user2['workingStyle']),
        (user1['environment'] == user2['environment'])
    ]
    
    weighted_similarity = sum(
        (weights1[i] + weights2[i]) / 2 * (1 - features[i] if isinstance(features[i], float) else features[i])
        for i in range(len(features))
    )
    return weighted_similarity

def calculate_group_score(group, weights_matrix):
    total_score = 0
    pair_count = 0
    
    for user1, user2 in itertools.combinations(group, 2):
        index1 = user1['index']
        index2 = user2['index']
        total_score += calculate_compatibility(user1, user2, weights_matrix[index1], weights_matrix[index2])
        pair_count += 1
    
    return total_score / pair_count if pair_count > 0 else 0

def match_people(people, group_size, weights_matrix):
    groups = []
    unmatched = people[:]
    
    while len(unmatched) >= group_size:
        best_group = None
        best_score = -1
        
        for group in itertools.combinations(unmatched, group_size):
            group_score = calculate_group_score(group, weights_matrix)
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
def match_from_file(content, group_size, weights_matrix):
    try:
        # Split the file content into lines
        lines = content.strip().split('\n')
        # Parse each line into a list of people
        people = []
        for line in lines:
            parts = line.strip().split()
            person = {
                'index': len(people),
                'name': parts[0],
                'studyType': parts[1],
                'creditHours': int(parts[2]),
                'major': parts[3],
                'availability': parts[4],
                'learnerType': parts[5],
                'intensity': int(parts[6]),
                'priority': parts[7],
                'workingStyle': parts[8],
                'environment': parts[9],
                'gender': parts[10],
                'minor': parts[11],
                'year': parts[12],
                'interests': parts[13]
            }
            people.append(person)
        groups = match_people(people, group_size, weights_matrix)
        return [[{k: v for k, v in person.items()} for person in group] for group in groups]
    except Exception as e:
        print("Error:", e)
        return []

def main():
   eel.start('index.html', size=(800, 600), block=True)

if __name__ == "__main__":
    main()