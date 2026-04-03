from google import genai
from pydantic import BaseModel, Field
from typing import List, Optional
from string import Template
from objects import Weapon, Tribute, Event
import json


def info(objct):
    objct_data = objct.__dict__
    return  objct_data

def reader(file_name):
    with open(file_name, 'r') as f:
        content = f.read()
        return content


config = json.loads(reader('key.json'))
api_key = config["GEMINI_API_KEY"]
client = genai.Client(api_key=api_key)
intro = reader('introduction.txt')

def description(file_name, target):
    with open(file_name, 'r') as f:
        flag = False 
        description = ""     
        for i in f:
            clean = i.strip()          
            if flag and clean == "end":
                break
            if flag:
                description += i
            if clean == target:
                flag = True
    return description

class Event(BaseModel):
    event: str = Field(description= description('json.text',"event"))
    outcomes: object = Field(description= description('json.text',"outcomes"))
    traits: object = Field(description= description('json.text',"traits"))

    
config = json.loads(reader('key.json'))
api_key = config["GEMINI_API_KEY"]
client = genai.Client(api_key=api_key)


def generate_event(file):
    prompt = description(file, "prompt")
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": Event.model_json_schema(),
        },
    )
    event = Event.model_validate_json(response.text)
    return event

def userprompt(text):
    data = {"input": text}
    with open("json.text", "r") as f:
        content = f.read()
    temp = Template(content)
    final_text = temp.substitute(data)
    with open("backup.txt", "w") as f:
        f.write(final_text)
    a = generate_event('backup.txt')
    return a

def flavourtext(text):
    prompt = f"{text}\nobjectattributes"
    for i in text:
        if isinstance(i, (Weapon,Tribute,Event)):
            data = info(i)
            prompt += str(data)
    response = chat.send_message(prompt)
    responseresponse = f"{response.text}\n"
    with open('hungergames.txt', 'a') as f:
        f.write(responseresponse)
intro = reader('introduction.txt')

chat = client.chats.create(model = 'gemini-2.5-flash')
chat.send_message(intro) 