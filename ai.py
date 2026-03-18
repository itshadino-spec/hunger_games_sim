#llm generated code
import json
from google import genai

with open('/home/hadi/Desktop/code/python_code/projects/hunger_games_sim/.gitignore/key.json', 'r') as f:
    content = f.read()
    config = json.loads(content)
api_key = config["GEMINI_API_KEY"]
client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Confirm that you can hear me."
)

print(response.text)