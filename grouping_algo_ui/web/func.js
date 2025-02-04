function uploadFile() {
  const fileInput = document.getElementById('fileInput');
  const file = fileInput.files[0];
  const groupSize = parseInt(document.getElementById('groupSize').value);
  
  if (!file) {
    alert("Please choose a file first!");
    return;
  }

  if (isNaN(groupSize) || groupSize < 2 || groupSize > 6) {
    alert("Please enter a valid group size (minimum of 2, max of 6).");
    return;
  }
  const reader = new FileReader();
  reader.onload = function(event) {
    const content = event.target.result;
    eel.match_from_file(content, groupSize)(displayResults);
  };
  reader.readAsText(file);
}
  
function displayResults(groups) {
  const resultsDiv = document.getElementById('results');
  resultsDiv.innerHTML = "<h2>Matched Groups:</h2>";
  groups.forEach((group, index) => {
        //const p1 = pair[0]
        //const pairElement = document.createElement("p");
        //const p1Data = document.createElement("p");
        //pairElement.innerText = `${p1.name} WITH ${pair[1].name}`;
        //resultsDiv.appendChild(pairElement);
        const groupElement = document.createElement("div");
        groupElement.innerHTML = `<h3>Group ${index + 1}:</h3>`;
        group.forEach(person => {
            const personElement = document.createElement("p");
            personElement.textContent = `Name: ${person.name}, Study Type: ${person.studyType}, Credit Hours: ${person.creditHours}, Major: ${person.major}, Availability: ${person.availability}, Learner Type: ${person.learnerType}, Intensity: ${person.intensity}, Priority: ${person.priority}, Working Style: ${person.workingStyle}, Environment: ${person.environment}`;
            groupElement.appendChild(personElement);
        });
        resultsDiv.appendChild(groupElement);
    });
}