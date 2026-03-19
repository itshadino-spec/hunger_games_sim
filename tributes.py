import json

with open('tributes.json') as tribute_file:
    tributes = json.load(tribute_file)

tributes_instances = []

class Tribute:
    def __init__(self,name,traits,status,hp,alive):
        self.name = name
        self.traits = traits
        self.status = status
        self.hp = hp
        self.alive = alive
    def __repr__(self): 
        return f"{self.name}"

for i in tributes:
    new_tribute = Tribute(
        name=i['name'], 
        traits=i['traits'], 
        status=i['status'],
        hp = i['hp'], 
        alive=i['alive']
    )
    tributes_instances.append(new_tribute)
