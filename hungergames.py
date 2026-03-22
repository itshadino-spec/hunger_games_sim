import json
import random

from objects import tributes_instances, weapons_instances, events_instances
#from ai import flavour_text

status_effects = {"poisoned": "hp decreaser" , "healthy": "hp increaser"}
temp_instances = []

def happenstance(person,happening,day):
    event = happening.event
    name = person.name
    print("%s is attempting to %s" %(name,event))

    odds = happening.success_rate
    roll = random.randint(1,100)

    if any(trait in happening.traits for trait in person.traits):
        odds += 5
    if roll > odds:
        #llm_text = flavour_text(person,happening, False)
        person.status[happening.fail] = day
        print("place holder")
        #print(llm_text)
    else:
        #llm_text =flavour_text(person,happening, True)
        person.status[happening.success] = day
        print("place holder")
        #print(llm_text)

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

def passives(person):
    pass

def combat(attacker,defender):
    pass

def status_condition(person,day):
    infliction_day = person.status.values()
    ran = False
    for i in infliction_day:
        if (day - i) >= 3:
            key = i
            tuplelist = person.status.items()
            for j in tuplelist:
                if j[1] == key:
                    value = j[0]
            ran = True
        else:
            print("test 2")
    if ran == True:
        person.status.pop(value)


#day and night game loop

def main():
    day_count = 0
    while flag(tributes_instances):
        day_count += 1
        for i in tributes_instances:
            if len(i.status) > 0:
                status_condition(i,day_count)
        if len(temp_instances) == 0:
            #save()
            randomplayer(tributes_instances)
            pass
        while len(temp_instances) > 0:
            player = random.choice(temp_instances)
            player.hp -= 10 
            
            if player.hp <= 0:
                player.alive = False
                if flag(tributes_instances) == False:
                    temp_instances.clear()
                    break
            else:
                happenstance(player,events_instances[0],day_count)
                pass
            temp_instances.remove(player)
    winners = [p for p in tributes_instances if p.alive]
    print(f"{winners[0].name} has won the hunger games!")

if __name__ == "__main__":
    main()