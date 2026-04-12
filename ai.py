from google import genai
from pydantic import BaseModel, Field
from typing import List, Optional
from string import Template
from objects import Weapon, Tribute, Event, Map, location_instances
import json
import time
import random
from google.genai import errors


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
    max_retries = 3
    base_delay = 2 
    
    primary_model = "gemini-3-flash-preview"
    fallback_model = "gemini-2.5-flash" 
    current_model = primary_model

    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=current_model,
                contents=prompt,
                config={
                    "response_mime_type": "application/json",
                    "response_schema": Event.model_json_schema(),
                },
            )
            event = Event.model_validate_json(response.text)
            return event

        except errors.ClientError as e:
            status_code = e.code
            print(f"[ATTEMPT {attempt + 1}/{max_retries}] ClientError ({status_code}): {e}")

            if status_code == 429:
                if current_model == primary_model:
                    print(f"!!! FALLBACK !!! {primary_model} reached quota. Switching to {fallback_model}.")
                    current_model = fallback_model
                    continue
                    
                if attempt < max_retries - 1:
                    delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
                    print(f"-> Rate limit hit on fallback. Retrying in {delay:.2f} seconds...")
                    time.sleep(delay)
                    continue

def userprompt(person, text):
    location = [i for i in location_instances if person.location == i.name][0]
    text += f"\nlocation:{location.description}"
    data = {"input": text}
    with open("json.text", "r") as f:
        content = f.read()
    temp = Template(content)
    final_text = temp.substitute(data)
    with open("backup.txt", "w") as f:
        f.write(final_text)
    while True:
        a = generate_event('backup.txt')
        
        if a is not None:
            return a
            
        print("\n[!] API generation failed (models exhausted or server error).")
        input("Press Enter to try again...")
        return a

def flavourtext(text):
    pass
    prompt = f"{text}\nobjectattributes"
    for i in text:
        if isinstance(i, (Weapon,Tribute,Event,Map)):
            data = info(i)
            prompt += str(data)
    response = chat.send_message(prompt)
    responseresponse = f"{response.text}\n"
    with open('hungergames.txt', 'a') as f:
        f.write(responseresponse)
intro = reader('introduction.txt')

chat = client.chats.create(model = 'gemini-3-flash-preview')
chat.send_message(intro)