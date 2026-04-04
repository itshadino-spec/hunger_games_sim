import json
import random

from objects import location_instances, tributes_instances, weapons_instances, generate_event
from ai import  userprompt, flavourtext

weapon_dict = {}
for i in weapons_instances:
    weapon_dict[i.name] = i

def llm(person,happening):
    if happening == "event":
        context = input("what do you wish to do")
        text = userprompt(person,context)
        a = genevent(text,person)
        return a
    flavourtext(happening)
    print(happening)
def genevent(event_object,person):
    data = event_object.model_dump()
    with open("events.json", "w") as f:
        json.dump(data, f, indent = 4)
    event_instances = generate_event()
    return event_instances

        
def odds(person, modifiers):
    roll = random.randint(0,100)
    event_mods = list(modifiers.keys())

    for i in person.traits:
        if i in event_mods:
            roll += modifiers.get(i)
    return roll

def happenstance(person,happening,day):
    status_effects = ["enraged", "bloodloss", "insanity", "healthy", "satiated", "hunger" "poisoned" ]
    rolled = odds(person, happening.traits)
    oddtable = list(happening.outcomes.keys())
 
    for i in oddtable:
        num = int(i)
        if rolled < num:
            add = happening.outcomes.get(i)

    if add in status_effects:
        person.status[add] = day
    else:
        person.inventory.append(add)
    flavour = [person, "in the event" , happening, "had outcome", add]
    llm(person, flavour)


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
def passives(person):
    passive_regen = {"faster healing": 15, "doctor": 20}
    for i in person.traits:
        if i in list(passive_regen.keys()): 
            heal = passive_regen.get(i)
            person.hp += heal

def evasion(person):
    evasion_odds = 25
    evasion_table = {"solar dragon": 5, "lucky": 5, "can hide": 10, "turns into a rat": 20, "stealthy": 15, "knows where everyone is": 50, 
                     "tuneller": 20 , "super hearing": 10 , "supher hearing": 20 }
    keys = list(evasion_table.keys())
    for i in person.traits:
        if i in keys:
            evasion_odds += evasion_table.get(i)
    print(evasion_odds)
    return evasion_odds


def flight(attacker, defender):
    roll = random.randint(0,100)
    flight_odds = 10
    flight_table = {"solar dragon": 5, "lucky": 5, "climb tree": 20, "can hide": 20, "turns into a rat": 10, "knows where everyone is": -20,
                    "massive sleepy birds": -100, "agile": 20, "fast": 20, "feather falling": 20}
    keys = flight_table.keys()
    for i in defender.traits:
        if i in keys:
            flight_odds += flight_table.get(i)
        if roll > flight_odds:
            fight(attacker, defender)
            flavour = [defender, "failed to flee from", attacker]
    else:
            flavour = [defender, "fled from", attacker]
    llm(attacker, flavour)

def weapon_damage (person, output):
    longrangetraits = {"longrange": 15, "lucky": 5, "solar dragon": 5, "good aim": 15 }
    throwingknives = {"knifethrower": 15}
    fryingpan = {"fryingpan": 50}
    maxdamage = 0
    damage = 0
    weapon = ""
    for i in person.inventory:
        if i in weapon_dict:
            weapon_obj = weapon_dict.get(i)
            damage = weapon_obj.lethality
            for j in person.traits:
                if weapon_obj.type == "longrange" and j in list(longrangetraits):
                    damage += longrangetraits.get(j)
                elif weapon_obj.type == "throwingknives" and j in list(throwingknives):
                    damage += throwingknives.get(j)
                elif weapon_obj.type == "fryingpan" and j in list(fryingpan):
                    damage += fryingpan.get(j)
        if damage > maxdamage:
            maxdamage = damage
            weapon = weapon_obj
    if output == "name":
        return weapon
    else:
        return damage

def fight(attacker , defender):
    combatstatus = {"strength": 15, "enraged": 10, "insanity": -10, "magic power": 5}
    roll = random.randint(0,100)
    attacker_weapon = weapon_damage(attacker,"name")
    defender_weapon = weapon_damage(defender, "name")
    attacker_status_bonus = sum(combatstatus[i] for i in attacker.status if i in combatstatus)
    defender_status_bonus = sum(combatstatus[i] for i in defender.status if i in combatstatus)

    attacker_odds = (weapon_damage(attacker, "damage") - weapon_damage(defender, "damage")) + (attacker_status_bonus - defender_status_bonus)
    print(attacker_odds)

    if ("projectile protection" in attacker.traits) and (defender_weapon.type == "longrange"):
        attacker_odds += 10
    if ("projectile protection" in defender.traits) and (attacker_weapon.type == "longrange"):
        attacker_odds -= 10
    if attacker_odds > roll:
        flavour = [attacker, "has killed with", attacker_weapon, defender, "who fought with", defender_weapon]
        llm(attacker, flavour)
        defender.alive = False
    else:
         flavour = (f"{defender} has killed with {defender_weapon} {attacker}") 
         flavour = [defender, "has killed with", defender_weapon, attacker, "who fought with", attacker_weapon ]
         llm(defender, flavour)
         attacker.alive = False

def combat(person):
    roll = 0
    defender = input(f"select a player to attack from {tributes_instances}: ")
    for i in tributes_instances:
        if i.name == defender:
            defender_object = i
            roll = random.randint(0,100)
            evasion_odds = evasion(i)
    
    if person.location != defender_object.location:
        flavour = [defender_object, "was in a different biome to" , person]
        return llm(person,flavour)
    if evasion_odds < roll:
        flavour = [defender_object, "was found by", person]
        defender_action = input(f"{defender_object}: fight or flight?: ")
        if defender_action == "flight":
            flight(person,defender_object)
        else:
            fight(person,defender_object)
    else:
        flavour = [defender_object, "escaped from", person]
    llm(person, flavour)
        

def status_condition(person,day): 
    hpstatus = {"frozen": -15,"thirst": -15, "very healthy": 20 ,"healthy": 10, "rested": 5, "satiated": 15 , 
                "bloodloss": -10, "poison": -15, "magic power": 5}
    immunetraits = {"poison resistance": "poison", "camel": "thirst", "can smell water": "thirst", "can filter water": "thirst"}
    for i in person.traits:
        if i in immunetraits:
            person.status.pop(immunetraits.get(i))
    inflicted_statuses = list(person.status.keys())
    for i in inflicted_statuses:
        val = person.status.get(i)
        if (day - val ) >= 3:
            person.status.pop(i)
        else:
            if i in list(hpstatus.keys()):
                person.hp += hpstatus.get(i)
            
def night(person,night):
    sleepge = input(f"{person}sleep y/n:")
    if sleepge == "n":
        person.status["insanity"] = night
        print(f"{person} did not rest")
    else:
        person.status["well rested"] = night
        print(f"{person} slept")
        return True

def inventory(person,day_night):
    items = {"artecorp potions": "very healthy" , "potion": "healthy", "candy": "satiated" , "carrots": "enraged", "fish": "satiated", "witch potion": "magic power"}
    print(person.inventory)
    pick = input("select an item: ")
    if pick in person.inventory:
        add = items.get(pick)
        person.status[add] = day_night
    else:
        print("invalid")
        inventory(person)
def alliances(person):
    pass

def genitem(person):
    items = {"witch doctor": "witch potion" , "artecorp potions": "artecorp potions",
             "pet whale": "fish", "pet cat": "fish", "super strength carrots": "carrots" }
    for i in person.traits:
        if i in items:
            person.inventory.append(items.get(i))

def move(person, day_night):
    inp = input(f"{person} do you wish to move?:")
    if inp == "y":
        curr = [i for i in location_instances if person.location == i.name][0]
        tomove = input((f"{curr.connections} where do you want to go?:"))
        person.location = tomove
        newloc = [i for i in location_instances if tomove == i.name ][0]
        if newloc.status_effect != "none":
            person.status[newloc.status_effect] = day_night
            flavour = [person, "moved to", newloc, "and recieved the", newloc.status_effect]
        else:
            flavour = [person, "moved to", newloc]
        llm(person, flavour)

def turn(person, day_night):
    while True:
        if "fast" in person.traits:
            move(person, day_night)
            move(person,day_night)
        else:
            move(person,day_night)
        choice = input(f"what will {person} do!")
        if day_night % 3 == 0:
            genitem(person)
        if choice == "event":
            b = llm(person,"event")
            happenstance(person,b[0],day_night)
        elif choice == "inventory":
            inventory(person, day_night)
        elif choice == "combat":
            combat(person)
        elif choice == "alliance":
            alliances(person)
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