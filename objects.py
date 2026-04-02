import json
from dataclasses import dataclass

@dataclass
class Tribute:
    name: str
    traits: list
    status: dict
    hp: int
    alive: bool
    inventory: list
    def __repr__(self): return f"{self.name}"

@dataclass
class Weapon:
    name: str
    type: str
    traits: list
    lethality: int
    def __repr__(self): return f"{self.name}"

@dataclass
class Event:
    event: str
    outcomes: dict
    traits: dict
    def __repr__(self): return f"{self.event}"

    
def generate_event():
    i = json.load(open('events.json'))
    events_instances   = [Event(**i)]
    return events_instances

tributes_instances = [Tribute(**i) for i in json.load(open('tributes.json'))]
weapons_instances  = [Weapon(**i)  for i in json.load(open('weapons.json'))]

eventfunction = generate_event
print(len(tributes_instances))