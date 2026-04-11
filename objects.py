import json
from dataclasses import dataclass

@dataclass
class Map:
    name: str
    description: str
    status_effect: str 
    connections: list
    curr_weather: str
    weather_type: list
    trap: list
    def __repr__(self): return f"{self.name}"

@dataclass
class Tribute:
    name: str
    traits: list
    status: dict
    hp: int
    alive: bool
    inventory: list
    location: str
    alliance: list
    awake: bool
    sleepdeprivation: int
    def __repr__(self): return f"{self.name}"

@dataclass
class Weapon:
    name: str
    type: str
    status: list
    lethality: int
    def __repr__(self): return f"{self.name}"

@dataclass
class Event:
    event: str
    outcomes: dict
    traits: dict
    def __repr__(self): return f"{self.event}"

class Misc:
    def __init__(self, day, order,moveflag, sleepflag):
        self.day = day
        self.order = order
        self.moveflag = moveflag
        self.sleepflag = sleepflag
    
def generate_event():
    i = json.load(open('events.json'))
    events_instances   = [Event(**i)]
    return events_instances

tributes_instances = [Tribute(**i) for i in json.load(open('tributes.json'))]
weapons_instances  = [Weapon(**i)  for i in json.load(open('weapons.json'))]
location_instances = [Map(**i) for i in json.load(open('map.json'))]
eventfunction = generate_event

with open('misc.json') as f:
    data = json.load(f)
    miscinstance = Misc(**data)


