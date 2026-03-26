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
    success_rate: float
    success: str
    fail: str
    traits: list
    def __repr__(self): return f"{self.event}"

tributes_instances = [Tribute(**i) for i in json.load(open('tributes.json'))]
weapons_instances  = [Weapon(**i)  for i in json.load(open('weapons.json'))]
events_instances   = [Event(**i)   for i in json.load(open('events.json'))]