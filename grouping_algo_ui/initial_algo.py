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
            name = parts[0]
            study_type = parts[1]
            try:
                credit_hours = int(parts[2])  # Ensure this is an integer
            except ValueError:
                print(f"Invalid credit hours value: {parts[2]} on line {line.strip()}")
                continue
            major = parts[3]
            person = {
                'name': name,
                'studyType': study_type,
                'creditHours': credit_hours,
                'major': major
            }
            people.append(person)
    return people

def match_people(people):
    #group by 3
    traits = defaultdict(list) #holds the people w their data as the Key
    #default Dictionary stores the traits as array group, value is person
    for person in people:
        key = (person['studyType'], person['creditHours'], person['major'])
        traits[key].append(person)
    pairs = [] #to hold the pairs that are generated
    unmatched = [] #if we have an odd number
    #first checking for all 3 traits
    for key, group in traits.items(): 
        #the group is groups of three, so for example night,CS,18 or something
        while len(group) >= 2:
            pairs.append((group.pop(), group.pop()))#pair these people up, they have three in common 
        if group:
            unmatched.append(group.pop())#no match found, they are alone (unique three trait combo)
    #now doing the same, but making our groups by the same study type and same major
    studyAndMajor = defaultdict(list)
    for person in unmatched:
        key = (person['studyType'], person['major'])
        studyAndMajor[key].append(person)
    unmatched = []
    for key, group in studyAndMajor.items():
        while len(group) >= 2:
            pairs.append((group.pop(), group.pop()))
        if group:
            unmatched.append(group.pop())
    #now just doing study type 
    studyTP = defaultdict(list)
    for person in unmatched:
        key = person['studyType']
        studyTP[key].append(person)
    unmatched = []
    for key, group in studyTP.items():
        while len(group) >= 2:
            pairs.append((group.pop(), group.pop()))
        if group:
            unmatched.append(group.pop())
    #for people with NOTHING in common, just do it randoly
    #all unique traits
    random.shuffle(unmatched)
    while len(unmatched) >= 1:
        if len(unmatched) >= 2:
            person1 = unmatched.pop()
            person2 = unmatched.pop()
            pairs.append((person1, person2))
        if len(unmatched) == 1:
            person1 = unmatched.pop()
            pairs.append((person1, person1))
    return pairs

@eel.expose
def match_from_file(content):
    try:
        # Split the file content into lines
        lines = content.strip().split('\n')
        # Parse each line into a list of people
        people = []
        for line in lines:
            name, study_type, credit_hours, major = line.strip().split()
            people.append({
                "name": name,
                "studyType": study_type,
                "creditHours": int(credit_hours),
                "major": major
            })
        pairs = match_people(people)
        return [(pair[0], pair[1]) for pair in pairs]
    except Exception as e:
        print("Error:", e)  # Print any errors that occur
        return []

def main():
    filename = 'users.txt'
    people = load_people(filename)
    pairs = match_people(people)
    for i in range(len(pairs)):
        if (pairs[i][0]['name'] != pairs[i][1]['name']):
            print(f"--------------- Match Number {i+1} ---------------\n"
                  f"{pairs[i][0]['name']} WITH {pairs[i][1]['name']}\n"
                  f"({pairs[i][0]['name']}, : {pairs[i][0]['studyType']}, {pairs[i][0]['creditHours']} credits, {pairs[i][0]['major']})\n"
                  f"({pairs[i][1]['name']}, : {pairs[i][1]['studyType']}, {pairs[i][1]['creditHours']} credits, {pairs[i][1]['major']})\n"
                  f"-----------------------------------------------\n")
        else:
            print(f"Odd One Out :( {pairs[i][0]['name']}")

if __name__ == "__main__":
    eel.start('index.html')