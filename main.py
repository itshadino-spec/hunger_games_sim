import json
import random

from events import events_instances
from tributes import tributes_instances

temp_instances = []

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

def flag(person_instances):
    for i in range(len(person_instances)):
        status = person_instances[i]
        if status.alive == True:
            return True
    return False

def randomplayer(person_instances):
    j = 0
    for i in person_instances:
        person = person_instances[j]
        temp_instances.append(person)
        j += 1

#day and night game loop

while flag(tributes_instances):
    if len(temp_instances) == 0:
        #save()
        randomplayer(tributes_instances)
    while len(temp_instances) > 0:
        player = random.choice(temp_instances)
        health = player.hp
        health -= 10
        if health <= 0:
            player.alive = False
            continue
        else:
            happenstance(player,events_instances[0])
            temp_instances.remove(player)
