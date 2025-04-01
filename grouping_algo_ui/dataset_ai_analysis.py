import json
import subprocess

with open("student_groups.json", "r", encoding="utf-8") as f:
    data = json.load(f)

prompt = f"""
You are analyzing a dataset of student study groups. Your goal is to:
1. Identify patterns between characteristics (availability, learner type, study style, intensity) and academic performance.
2. Determine if certain characteristics consistently correlate with **higher group grades**.
3. Suggest **weight adjustments** for the grouping algorithm based on these insights.

Here are **10 example groups** from the dataset:
{json.dumps(data[:10], indent=2)}

Please respond with a structured analysis:
- **High-Performing Group Patterns**: What characteristics lead to high grades?
- **Low-Performing Group Patterns**: What characteristics lead to low grades?
- **Recommended Weight Adjustments**: How should the algorithm prioritize characteristics based on this?
"""

response = subprocess.run(
    ["ollama", "run", "mistral", prompt],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    encoding="utf-8"
)

print(response.stdout)