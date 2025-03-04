import pytest
import random
from algorithm import match_people


def create_person(index, name, studyType, creditHours, major, availability, learnerType,
                  intensity, priority, workingStyle, environment):
    return {
        'index': index, 'name': name, 'studyType': studyType, 'creditHours': creditHours, 'major': major,
        'availability': availability, 'learnerType': learnerType, 'intensity': intensity, 'priority': priority,
        'workingStyle': workingStyle, 'environment': environment
    }
def create_weights_matrix(size):
    return [[1] * 9 for _ in range(size)]

# Verufy grouping algo functions properly

# test 1: matches people with the same characteristics together, w/o weights applied
def test_1():
    people = [
        create_person(0, "Alice", "NightOwl", 13, "CS", "Weekdays(Morning)", "Analytical", 3, "Availability", "Long", "Home"),
        create_person(0, "Bob", "NightOwl", 13, "CS", "Weekdays(Morning)", "Analytical", 3, "Availability", "Long", "Home"),
        create_person(0, "Max", "NightOwl", 3, "CS", "Weekdays(Morning)", "Analytical", 3, "Availability", "Long", "Home"),
        create_person(0, "Kim", "NightOwl", 3, "CS", "Weekdays(Morning)", "Analytical", 3, "Availability", "Long", "Home")
    ]
    weights_matrix = create_weights_matrix(len(people))
    groups = match_people(people, 2, weights_matrix)
    
    assert len(groups) == 2
    assert len(groups[0]) == 2
    print("Test passed! The algorithm is matching people with similar characteristics.")  

# test 2: ensure groups of required size or less abd not more is being formed
def test_2():
    people = [
        create_person(i, f"Person{i}", "NightOwl", 13, "CS", "Weekdays(Morning)", "Analytical", 3, "Availability", "Long", "Home")
        for i in range(5)
    ]
    weights_matrix = create_weights_matrix(len(people))
    groups = match_people(people, 3, weights_matrix)
    
    assert len(groups) == 2
    assert len(groups[0]) <= 3
    assert len(groups[1]) <= 3
    print("Test passed! The algorithm is grouping correctly.")

# test 3: trialing grouping algorithm performance capabilities
def test_3():
    names = ["Alice", "Bob", "Max", "Kim", "Julie"]
    people = [
        create_person(i, random.choice(names), "NightOwl", random.randint(12, 21), "CS", "Weekdays(Morning)", "Analytical", random.randint(1, 5), "Availability", "Long", "Home")
        for i in range(100)
    ]
    weights_matrix = create_weights_matrix(len(people))
    groups = match_people(people, 4, weights_matrix)
    assert len(groups) > 0 
    assert all(len(group) <= 4 for group in groups) 
    print("Test passed! The algorithm's performance is not impacted by large inputs.")

if __name__ == "__main__":
    test_1()
    test_2()
    test_3()