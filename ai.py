from google import genai
from pydantic import BaseModel, Field
from typing import List, Optional
import json


def info(person):
    person_data = person.__dict__
    return  person_data

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

def reader(file_name):
    with open(file_name, 'r') as f:
        content = f.read()
        return content
    
config = json.loads(reader('key.json'))
api_key = config["GEMINI_API_KEY"]
client = genai.Client(api_key=api_key)


def generate_event(prompt):
    prompt = description('json.text', prompt)
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_json_schema": Event.model_json_schema(),
        },
    )
    event = Event.model_validate_json(response.text)
    return event

