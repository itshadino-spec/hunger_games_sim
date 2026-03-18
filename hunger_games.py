import json
import random

with open('tributes.json') as tribute_file:
    tributes = json.load(tribute_file)

with open('events.json') as event_file:
    events = json.load(event_file)

tributes_instances = []
events_instances = []

class Event:
    def __init__(self,event,success_rate,success,fail,traits):
        self.event = event
        self.success_rate = success_rate
        self.success = success
        self.fail = fail
        self.traits = traits
    
    def __repr__(self): 
        return f"{self.event}"
class Tribute:
    def __init__(self,name,traits,status,alive):
        self.name = name
        self.traits = traits
        self.status = status
        self.alive = alive
    def __repr__(self): 
        return f"{self.name}"

for i in tributes:
    new_tribute = Tribute(
        name=i['name'], 
        traits=i['traits'], 
        status=i['status'], 
        alive=i['alive']
    )
    tributes_instances.append(new_tribute)
for j in events:
    new_event = Event(
        event=j['event'],
        success_rate = j['success_rate'], 
        success=j['success'], 
        fail=j['fail'], 
        traits=j['traits']
    )
    events_instances.append(new_event)

def happenstance(person,happening):
    event = happening.event
    name = person.name
    print("%s is attempting to %s" %(name,event))

    odds = happening.success_rate
    roll = random.randint(1,100)

    if any(trait in happening.traits for trait in person.traits):
        odds += 5
    if roll > odds:
        person.status.append(happening.fail)
        print("%s was poisoned by shifty berries" %(name)) #temp needs to be llm msg
    else:
        person.status.append(happening.success)
        print("%s ate delicious berries" %(name)) #temp, needs to be llm msg

def save():
    tributes_data = [i.__dict__ for i in tributes_instances] 
    with open('tributes.json', 'w') as f:
        json.dump(tributes_data,f,indent = 4)

happenstance(tributes_instances[1], events_instances[0])
save()


