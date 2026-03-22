import json
import random

from objects import tributes_instances, weapons_instances, events_instances
from ai import flavour_text


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
        llm_text = flavour_text(person,happening, False)
        person.status.append(happening.fail)
        print(llm_text)
    else:
        llm_text =flavour_text(person,happening, True)
        person.status.append(happening.success)
        print(llm_text)



def save():
    tributes_data = [i.__dict__ for i in tributes_instances] 
    with open('tributes.json', 'w') as f:
        json.dump(tributes_data,f,indent = 4)

def flag(person_instances):
    alive_tributes = 0
    for i in range(len(person_instances)):
        status = person_instances[i]
        if status.alive == True:
            alive_tributes += 1
    if alive_tributes == 1:
        return False
    return True

def randomplayer(person_instances):
    j = 0
    for i in person_instances:
        person = person_instances[j]
        if person.alive:
            temp_instances.append(person)
        j += 1

#day and night game loop

def main():
    while flag(tributes_instances):
        if len(temp_instances) == 0:
            #save()
            randomplayer(tributes_instances)
        while len(temp_instances) > 0:
            player = random.choice(temp_instances)
            player.hp -= 40 
            
            if player.hp <= 0:
                player.alive = False
                if flag(tributes_instances) == False:
                    temp_instances.clear()
                    break
            else:
                happenstance(player,events_instances[0])
            temp_instances.remove(player)
    winners = [p for p in tributes_instances if p.alive]
    print(f"{winners[0].name} has won the hunger games!")

if __name__ == "__main__":
    main()