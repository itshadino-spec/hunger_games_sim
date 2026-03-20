import json
from google import genai


def info(person,happening):
    event_data = happening.__dict__
    person_data = person.__dict__
    return event_data , person_data

def reader(file_name):
    with open(file_name, 'r') as f:
        content = f.read()
        return content

config = json.loads(reader('key.json'))
api_key = config["GEMINI_API_KEY"]
client = genai.Client(api_key=api_key)


intro = reader('introduction.txt')
chat = client.chats.create(model = 'gemini-2.5-flash-lite')
response = chat.send_message(intro)

def flavour_text(person, happening, outcome):
    data = info(person,happening)
    if outcome == True:
        win = chat.send_message(f"the person doing the event {data} suceeded, write an output similar to the example")
        return win.text
    else:
        fail = chat.send_message(f"the person doing the event {data} failed, write an output similar to the example")
        return fail.text