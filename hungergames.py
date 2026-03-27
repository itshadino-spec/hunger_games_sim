import json
import random

from objects import tributes_instances, weapons_instances, events_instances
#from ai import flavour_text

status_effects = {"poisoned": "hp decreaser" , "healthy": "hp increaser"}
passive_traits = {"doctor": "hp increaser"}
combat_traits = {"gymbro": "damage", "robot": "evasion", "chef":"flee"}
items = {"potion" : "hp increaser"}
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
        print("placeholder1")
        #print(llm_text)
    else:
        #llm_text =flavour_text(person,happening, True)
        person.status[happening.success] = day
        print("placeholder2")
        #print(llm_text)
    #rewrite this into one llm call and put it into a try and accept catch

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
    #check players inventory to see if they have any weapons
    #use lethality to find the odds of victory for the attacker 
    #update defender or attacker object to show player is dead
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
        defender.alive == False
    else:
         print(f"{defender} has killed {attacker}") #temp shud be a gemini call
         attacker.alive == False

def combat(person):
    roll = 0
    defender = input(f"select a player to attack from {tributes_instances}")
    for i in tributes_instances:
        if i.name == defender:
            defender_object = i
            roll = random.randint(0,100)
            evasion_odds = evasion(i)
    if evasion_odds < roll:
        print("tribute found")
        defender_action = input(f"{defender_object}: fight or flight?")
        if defender_action == "flight":
            flight(person,defender_object)
        else:
            fight(person,defender_object)
    else:
        print("tribute could not be found")
        

def status_condition(person,day):
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
    temp = random.randint(0,1) #temp needs to be user input later
    if temp == 0:
        person.status["insanity"] = night
    else:
        person.status["well rested"] = night

def inventory(person):
    print(person.inventory)
    pick = input("select an item")
    if pick in person.inventory:
        effect_item = items.get(pick)
        person.hp += 20
        print(person.hp)
        #temp need an if ladder
    else:
        print("invalid item")
        inventory(person)

def turn(person, day_night):
    choice = input(f"what will {person} do!")
    if choice == "event":
        happenstance(person,events_instances[0],day_night)
    elif choice == "inventory":
        inventory(person)
    elif choice == "combat":
        combat(person)
      
#day and night game loop

def main():
    day_night = 0
    while flag(tributes_instances):
        day_night += 1
        print(day_night)
        for i in tributes_instances:
            if len(i.status) > 0:
                status_condition(i,day_night)
        if len(temp_instances) == 0:
            #save()
            randomplayer(tributes_instances)
            pass
        while len(temp_instances) > 0:
            player = random.choice(temp_instances)
            player.hp -= 10 
            if day_night % 2 == 0:
                print("NIGHT HAS FALLEN!")
                night(player,day_night)
            else:
                print("A NEW DAY HAS DAWNED")
            if player.hp <= 0:
                player.alive = False
                if flag(tributes_instances) == False:
                    temp_instances.clear()
                    break
            else:
                turn(player,day_night)
                pass
            passives(player)
            temp_instances.remove(player)
    winners = [p for p in tributes_instances if p.alive]
    print(f"{winners[0].name} has won the hunger games!")

if __name__ == "__main__":
    main()