import algorithm

# test 4: ensures groups of appropriate sizes are being formed
def test_algorithm():
    test_people = [
        {'index': 0, 'name': 'Francis', 'studyType': 'NightOwl', 'creditHours': 13, 'major': 'IE', 'availability': 'Weekdays(Morning)', 'learnerType': 'Analytical', 'intensity': 3, 'priority': 'Availability', 'workingStyle': 'Long', 'environment': 'Home'},
        {'index': 1, 'name': 'Alice', 'studyType': 'EarlyRiser', 'creditHours': 17, 'major': 'MechE', 'availability': 'Weekdays(Afternoon)', 'learnerType': 'Practical', 'intensity': 4, 'priority': 'LearningStyle', 'workingStyle': 'Short', 'environment': 'Library'},
        {'index': 2, 'name': 'Max', 'studyType': 'NightOwl', 'creditHours': 16, 'major': 'Business', 'availability': 'Weekdays(Evening)', 'learnerType': 'Interpersonal', 'intensity': 5, 'priority': 'Availability', 'workingStyle': 'Short', 'environment': 'Cafe'},
        {'index': 3, 'name': 'Kim', 'studyType': 'NightOwl', 'creditHours': 14, 'major': 'CS', 'availability': 'Weekends(Morning)', 'learnerType': 'Holistic', 'intensity': 2, 'priority': 'LearningStyle', 'workingStyle': 'Long', 'environment': 'Silent'}
    ]
    weight_matrix = [
        [0.3, 0.2, 0.2, 0.1, 0.1, 0.1, 0.0, 0.0, 0.0],  # Francis
        [0.1, 0.3, 0.2, 0.1, 0.1, 0.1, 0.0, 0.1, 0.0],  # Alice
        [0.2, 0.1, 0.3, 0.1, 0.1, 0.1, 0.0, 0.0, 0.1],  # Max
        [0.3, 0.1, 0.2, 0.1, 0.1, 0.1, 0.1, 0.0, 0.0]   # Kim
    ]
    group_size = 2
    groups = algorithm.match_people(test_people, group_size, weight_matrix)
    print("Final Groups:")
    for i, group in enumerate(groups):
        print(f"Group {i+1}:")
        for person in group:
            print(f"  - {person['name']}")
    assert len(groups) == 2, "Expected two groups of two people each"
    print("Test passed! The algorithm is grouping correctly.")

# test 5: ensures that students with higher matching weights get a higher compatability
def test_weight_effect():
    student1 = {'index': 0, 'name': 'Francis', 'studyType': 'NightOwl', 'creditHours': 13, 'major': 'IE', 'availability': 'Weekdays(Morning)', 'learnerType': 'Analytical', 'intensity': 3, 'priority': 'Availability', 'workingStyle': 'Long', 'environment': 'Home'}
    student2 = {'index': 1, 'name': 'Alice', 'studyType': 'EarlyRiser', 'creditHours': 17, 'major': 'MechE', 'availability': 'Weekdays(Afternoon)', 'learnerType': 'Practical', 'intensity': 4, 'priority': 'LearningStyle', 'workingStyle': 'Short', 'environment': 'Library'}
    
    weights_low = [0.1] * 9
    weights_high = [0.9] * 9
    
    score_low = algorithm.calculate_compatibility(student1, student2, weights_low, weights_low)
    score_high = algorithm.calculate_compatibility(student1, student2, weights_high, weights_high)
    
    print(f"Compatibility score with low weights: {score_low}")
    print(f"Compatibility score with high weights: {score_high}")
    
    assert score_high > score_low, "Higher weights should result in a higher score"
    print("Weight effect test passed!")

# test 6: ensures group with highest compatability is formed first
def test_highest_compatibility_groups_first():
    student1 = {'index': 0, 'name': 'Francis', 'studyType': 'NightOwl', 'creditHours': 13, 'major': 'IE', 'availability': 'Weekdays(Morning)', 'learnerType': 'Analytical', 'intensity': 3, 'priority': 'Availability', 'workingStyle': 'Long', 'environment': 'Home'}
    student2 = {'index': 1, 'name': 'Alice', 'studyType': 'NightOwl', 'creditHours': 13, 'major': 'CS', 'availability': 'Weekdays(Morning)', 'learnerType': 'Analytical', 'intensity': 3, 'priority': 'Availability', 'workingStyle': 'Long', 'environment': 'Home'}
    student3 = {'index': 2, 'name': 'Max', 'studyType': 'EarlyRiser', 'creditHours': 17, 'major': 'MechE', 'availability': 'Weekdays(Afternoon)', 'learnerType': 'Practical', 'intensity': 4, 'priority': 'LearningStyle', 'workingStyle': 'Short', 'environment': 'Library'}
    test_people = [student1, student2, student3]

    # Francis and Alice prioritize studyType and major and Max prioritizes credithours and availability
    weight_matrix = [
        [0.5, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.5, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.5, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0]
    ]

    groups = algorithm.match_people(test_people, 2, weight_matrix)
    group_sets = [set(person["name"] for person in group) for group in groups]

    print("Checking if highest compatibility groups are formed first:")
    assert {"Francis", "Alice"} in group_sets, "Francis and Alice should be grouped together first due to highest compatibility."
    print("Highest compatibility grouping test passed!")


if __name__ == "__main__":
    test_algorithm()
    test_weight_effect()
    test_highest_compatibility_groups_first()