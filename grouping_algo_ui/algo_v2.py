import random
import eel
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
    #group by 3
    traits = defaultdict(list) #holds the people w their data as the Key
    #default Dictionary stores the traits as array group, value is person
    for person in people:
        key = (
            person['studyType'], person['creditHours'], person['major'],
            person['availability'], person['learnerType'], person['intensity'],
            person['priority'], person['workingStyle'], person['environment']
        )
        traits[key].append(person)
    groups = [] #to hold the pairs that are generated
    unmatched = [] #if we have an odd number
    #first checking for all 3 traits
    for key, group in traits.items(): 
        #the group is groups of three, so for example night,CS,18 or something
        while len(group) >= group_size:
            groups.append([group.pop() for _ in range(group_size)])#pair these people up, they have three in common 
        if group:
            unmatched.extend(group)#no match found, they are alone (unique three trait combo)
    #now doing the same, but making our groups by the same study type and same major
    studyAndMajor = defaultdict(list)
    for person in unmatched:
        key = (person['studyType'], person['major'])
        studyAndMajor[key].append(person)
    unmatched = []
    for key, group in studyAndMajor.items():
        while len(group) >= group_size:
            groups.append([group.pop() for _ in range(group_size)])
        if group:
            unmatched.extend(group)
    #now just doing study type 
    studyTP = defaultdict(list)
    for person in unmatched:
        key = person['studyType']
        studyTP[key].append(person)
    unmatched = []
    for key, group in studyTP.items():
        while len(group) >= group_size:
            groups.append([group.pop() for _ in range(group_size)])
        if group:
            unmatched.extend(group)
    #for people with NOTHING in common, just do it randoly
    #all unique traits
    random.shuffle(unmatched)
    while len(unmatched) >= group_size:
        groups.append([unmatched.pop() for _ in range(group_size)])
    
    if unmatched:
        groups.append(unmatched)#Add remaining unmatched people as a smaller group
    
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