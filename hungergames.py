import json
import random

from objects import tributes_instances, weapons_instances, generate_event
from tables import hpincreasestatus, hpdecreasestatus, passive_traits, combatodsincrease, items
from ai import  userprompt

status_effects = {"poisoned": "hp decreaser" , "healthy": "hp increaser"}
passive_traits = {"doctor": "hp increaser"}
combat_traits = {"gymbro": "damage", "robot": "evasion", "chef":"flee"}
items = {"potion" : "hp increaser"}

def llm(person,happening):
    if happening == "event":
        try:
            context = input("what do you wish to do")
            text = userprompt(person, context)
            genevent(text)
        except:
            save()
def genevent(text):
    print(text)
        
def odds(person, modifiers):
    roll = random.randint(0,100)
    event_mods = list(modifiers.keys())

    for i in person.traits:
        if i in event_mods:
            roll += modifiers.get(i)
    return roll

def happenstance(person,happening,day):
    rolled = odds(person, happening.traits)
    oddtable = list(happening.outcomes.keys())
 
    for i in oddtable:
        num = int(i)
        if rolled < num:
            add = happening.outcomes.get(i)

    if add in list(status_effects.keys()):
        person.status[add] = day
    else:
        person.inventory.append(add)


def save():
    tributes_data = [i.__dict__ for i in tributes_instances if i.alive == True] 
    with open('temp.json', 'w') as f:
        json.dump(tributes_data,f,indent = 4)

def flag(person_instances):
    alive_tributes = 0
    for i in range(len(person_instances)):
        status = person_instances[i]
        if status.alive == True:
            alive_tributes += 1
    if alive_tributes <= 1:
        print("end")
        return False
    print("continue")
    return True

def randomplayer(person_instances):
    temp_instances = []
    for i in range(len(person_instances)):
        person = person_instances[i]
        if person.alive:
            temp_instances.append(person)
    return temp_instances
def passives(person):#rewrite
    traits = passive_traits.keys()
    for i in person.traits:
        if i in traits:
            effect_passive = passive_traits.get(i)
            #temp code need if-else ladder later
            person.hp += 5

def evasion(person):
    evasion_odds = 25
    keys = combat_traits.keys()
    for i in person.traits:
        if i in keys:
            for j in keys:
                if i == j:
                    val = combat_traits.get(j)
                    if val == "evasion":
                        print(j)
                        evasion_odds += 10
    print(evasion_odds)
    return evasion_odds

def flight(attacker, defender):
    flight_odds = 10
    roll = random.randint(0,100)
    keys2 = combat_traits.keys()
    for i in defender.traits:
        if i in keys2:
            for j in keys2:
                val2 = combat_traits.get(j)
                if val2 == "flee":
                    flight_odds += 10
    if roll > flight_odds:
        fight(attacker, defender) 
        
def fight(attacker , defender):
    attacker_odds = 60
    roll = random.randint(0,100)
    for i in attacker.inventory:
        for j in weapons_instances:
            if i == j.name:
                attacker_weapon = j
    for i in defender.inventory:
        for j in weapons_instances:
            if i == j.name:
                defender_weapon = j
            
    attacker_odds += attacker_weapon.lethality
    attacker_odds -= defender_weapon.lethality

    if attacker_odds > roll:
        print(f"{attacker} has killed {defender}") #temp shud be a gemini call
        defender.alive = False
    else:
         print(f"{defender} has killed {attacker}") #temp shud be a gemini call
         attacker.alive = False

def combat(person):
    roll = 0
    defender = input(f"select a player to attack from {tributes_instances}: ")
    for i in tributes_instances:
        if i.name == defender:
            defender_object = i
            roll = random.randint(0,100)
            evasion_odds = evasion(i)
    if evasion_odds < roll:
        print("tribute found")
        defender_action = input(f"{defender_object}: fight or flight?: ")
        if defender_action == "flight":
            flight(person,defender_object)
        else:
            fight(person,defender_object)
    else:
        print("tribute could not be found")
        

def status_condition(person,day): #rewrite
    infliction_day = person.status.values()
    ran = False
    for i in infliction_day:
        value = i
        if (day - i) >= 3:
            tuplelist = person.status.items()
            for j in tuplelist:
                if j[1] == value:
                    key = j[0]
            ran = True
        else:
            if value == "hp decreaser":
                person.hp -= 5
            elif value == "hp increaser":
                person.hp += 5
            #will have to add more later
    if ran == True:
        person.status.pop(key)

def night(person,night):
    sleepge = input(f"{person}sleep y/n:")
    if sleepge == "n":
        person.status["insanity"] = night
        print(f"{person} did not rest")
    else:
        person.status["well rested"] = night
        print(f"{person} slept")
        return True

def inventory(person):
    print(person.inventory)
    pick = input("select an item:")
    if pick in person.inventory:
        effect_item = items.get(pick)
        person.hp += 20
        print(person.hp)
        #temp need an if ladder
    else:
        print("invalid item")
        inventory(person)

def turn(person, day_night):
    while True:
        choice = input(f"what will {person} do!")
        if choice == "event":
            llm(person,"event")
        elif choice == "inventory":
            inventory(person)
        elif choice == "combat":
            combat(person)
        person.hp -= 10
        if person.hp <= 0:
                person.alive = False
                if flag(tributes_instances) == False:
                    return False
        break
#day and night game loop

def main():
    day_night = 0
    while flag(tributes_instances):
        day_night += 1
        if day_night % 2 == 1:
            print("DAY HAS BEGUN")
        print(day_night)
        for i in tributes_instances:
            if len(i.status) > 0:
                status_condition(i,day_night)
        player_turns = randomplayer(tributes_instances)
        while len(player_turns) > 0:
            person = random.choice(player_turns)
            if day_night % 2 == 0:
                sleep = night(person,day_night)
                if sleep:
                    player_turns.remove(person)
                    continue
            if person.alive:
                turn(person,day_night)
            player_turns.remove(person)
            
    winners = [p for p in tributes_instances if p.alive]
    save()
    print(f"{winners[0].name} has won the hunger games!")

if __name__ == "__main__":
    main()