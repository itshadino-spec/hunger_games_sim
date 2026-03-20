import json
from google import genai

def reader(file_name):
    with open(file_name, 'r') as f:
        content = f.read()
        return content

config = json.loads(reader('key.json'))
api_key = config["GEMINI_API_KEY"]
client = genai.Client(api_key=api_key)


intro = reader('introduction.txt')
chat = client.chats.create(model = 'gemini-2.5-flash')
response = chat.send_message(intro)
response = chat.send_message('summarise the previous message i sent')
print(response.text)
