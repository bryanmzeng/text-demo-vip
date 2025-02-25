function uploadFile() {
  const fileInput = document.getElementById("fileInput");
  const file = fileInput.files[0];
  const groupSize = parseInt(document.getElementById("groupSize").value);

  if (!file) {
    alert("Please choose a file first!");
    return;
  }

  if (isNaN(groupSize) || groupSize < 2 || groupSize > 6) {
    alert("Please enter a valid group size (minimum of 2, max of 6).");
    return;
  }
  const reader = new FileReader();
  reader.onload = function (event) {
    const content = event.target.result;
    const { people, weightsMatrix } = parseUserFile(content);
    eel.match_from_file(content, groupSize, weightsMatrix)(displayResults);
  };
  reader.readAsText(file);
}

function parseUserFile(content) {
  let lines = content.trim().split("\n");
  let people = [];
  let weightsMatrix = [];

  lines.forEach((line) => {
    let parts = line.trim().split(/\s+/);
    if (parts.length !== 23) {
      console.warn("Skipping invalid line:", line);
      return;
    }

    let person = {
      name: parts[0],
      studyType: parts[1],
      creditHours: parseInt(parts[2]),
      major: parts[3],
      availability: parts[4],
      learnerType: parts[5],
      intensity: parseInt(parts[6]),
      priority: parts[7],
      workingStyle: parts[8],
      environment: parts[9],
      gender: parts[10],
      minor: parts[11],
      year: parts[12],
      interests: parts[13]
    };

    let weights = parts.slice(14).map(Number);

    people.push(person);
    weightsMatrix.push(weights);
  });

  return { people, weightsMatrix };
}

function displayResults(groups) {
  const resultsDiv = document.getElementById("results");
  resultsDiv.innerHTML = "<h2>Matched Groups:</h2>";
  groups.forEach((group, index) => {
    const groupElement = document.createElement("div");
    groupElement.innerHTML = `<h3>Group ${index + 1}:</h3>`;
    group.forEach((person) => {
      const personElement = document.createElement("p");
      personElement.textContent = `Name: ${person.name}, Study Type: ${person.studyType}, Credit Hours: ${person.creditHours}, Major: ${person.major}, Availability: ${person.availability}, Learner Type: ${person.learnerType}, Intensity: ${person.intensity}, Priority: ${person.priority}, Working Style: ${person.workingStyle}, Environment: ${person.environment}, Gender: ${person.gender}, Minor: ${person.minor}, Year: ${person.year}, Interests: ${person.interests} `;
      groupElement.appendChild(personElement);
    });
    resultsDiv.appendChild(groupElement);
  });
}
