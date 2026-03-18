import json
import random

from events import events_instances
from tributes import tributes_instances

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