import json

with open('weapons.json') as weapon_file:
    weapons = json.load(weapon_file)

weapons_instances = []

class Weapon:
    def __init__(self,name,type,traits,lethality):
        self.name = name
        self.type = type
        self.traits = traits
        self.lethality = lethality
    def __repr__(self): 
        return f"{self.name}"

for k in weapons:
    new_weapon = Weapon(
        name = k['name'],
        type = k['type'],
        traits = k['traits'],
        lethality = k['lethality']
    )
    weapons_instances.append(new_weapon)