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
    #flavourtext(happening)
    print(happening)

def genevent(event_object,person):
    data = event_object.model_dump()
    with open("events.json", "w") as f:
        json.dump(data, f, indent = 4)
    event_instances = generate_event()
    return event_instances

        
def odds(person, modifiers,day,name):
    roll = random.randint(0,100)
    event_mods = list(modifiers.keys())
    rolls_status = {"insanity":-10, "moreinsanity":-10, "magic power":5}
    for i in rolls_status:
        if i in person.status:
            roll += rolls_status.get(i)
    for i in person.traits:
        if i in event_mods:
            roll += modifiers.get(i)
    if ("nightvision" in person.traits) and day % 2 == 0:
        roll += 10
    if (("hunt" or "forage") in name) and ("lushlife" in person.status):
        roll += 10
    return roll

def weapontransform(person, outcomes, add, happening):
    transformations = {"poison tipped bow": "poisoncreek", "ice head bow": "tundra",
                       "poison tipped crossbow": "poincreek", "ice head crossbow": "tundra" }
    if outcomes.get("100") in transformations:
        if person.location != transformations.get(outcomes.get("100")):
            flavour = [person, "incorrect location for the modfication", happening]
            return llm(person,flavour)
        
    transformandbase = ["poison tipped bow", "ice head bow","poison tipped crossbow", "ice head crossbow",
                         "mythical longsword"]
    
    if outcomes.get("0") in person.inventory:
    
        if (add in transformandbase):
            person.inventory.append(add)
            person.inventory.remove(outcomes.get("0"))
            flavour = [person, "transformed their weapon", happening]

        else:
            flavour = [person, "destroyed their weapon", add, happening]
            person.inventory.remove(add)
    return llm(person,flavour)
        

def happenstance(person,happening,day):
    status_effects = ["enraged", "bloodloss", "insanity", "healthy", "satiated", "hunger" "poisoned" ]
    rolled = odds(person, happening.traits,day,happening.event)
    oddtable = list(happening.outcomes.keys())
 
    for i in oddtable:
        num = int(i)
        if rolled > num:
            add = happening.outcomes.get(i)
    if "transform" in happening.event:
        return weapontransform(person,happening.outcomes,add,happening)

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

def evasion(person,attacker, day):
    evasion_odds = 25
    evasion_table = {"solar dragon": 5, "lucky": 5, "can hide": 10, "turns into a rat": 20, "stealthy": 15, "knows where everyone is": 50, 
                     "tuneller": 20 , "super hearing": 10 , "supher hearing": 20 }
    evasion_fail = ["can track people", "knows where everyone is"]
    if any(i in evasion_fail for i in attacker.traits):
        flavour = [person, "could not hide from", attacker]
        evasion_odds = 0
        llm(attacker, flavour)
        return  evasion_odds 

    keys = list(evasion_table.keys())
    for i in person.traits:
        if i in keys:
            evasion_odds += evasion_table.get(i)
    if ("nightvision" in person.traits) and day % 2 == 0:
        evasion_odds += 10
    print(evasion_odds)
    return evasion_odds


def flight(attacker, defender, day):
    roll = random.randint(0,100)
    flight_odds = 10
    flight_table = {"solar dragon": 5, "lucky": 5, "climb tree": 20, "can hide": 20, "turns into a rat": 10,
                     "agile": 20, "fast": 20, "feather falling": 20}
    flight_status_table = {"mist": 10, "insanity": -10, "moreinsanity": -10, "magic power": 5}
    for i in flight_status_table:
        if i in defender.status:
            flight_odds += flight_status_table.get(i)
    flightfail = ["massive sleepy birds"]
    if any(i in flightfail for i in attacker.traits):
        flavour = [attacker, "prevented anyway of fleeing from" , defender ]
        return llm(attacker, flavour), fight(attacker,defender,day)
    keys = flight_table.keys()
    if ("nightvision" in attacker.traits) and day % 2 == 0:
        roll += 10
    for i in defender.traits:
        if i in keys:
            flight_odds += flight_table.get(i)
    if roll > flight_odds:
        fight(attacker, defender, day)
        flavour = [defender, "failed to flee from", attacker]
    else:
            flavour = [defender, "fled from", attacker]
    llm(attacker, flavour)

def weapon_damage (person, output):
    longrangetraits = {"longrange": 15, "lucky": 5, "solar dragon": 5, "good aim": 15 }
    throwingknives = {"knifethrower": 15}
    fryingpan = {"fryingpan": 40}
    vommit = {"projectile vommit": 30}
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
                elif weapon_obj.type == "vommit" and j in list(vommit):
                    damage += vommit.get(j)
        if damage > maxdamage:
            maxdamage = damage
            weapon = weapon_obj
    if output == "name":
        return weapon
    else:
        return damage

def fight(attacker , defender, day_night):
    combatstatus = {"strength": 15, "enraged": 10, "insanity": -10, "magic power": 5, "moreinsanity": -10}
    combattraits = {"martial arts": 15, "turns into a rat": 10, "lucky": 5, "solar dragon": 5, "angry": 10, "hunter": 10}

    attacker_weapon = weapon_damage(attacker,"name")
    defender_weapon = weapon_damage(defender, "name")
    attacker_status_bonus = sum(combatstatus[i] for i in attacker.status if i in combatstatus)
    defender_status_bonus = sum(combatstatus[i] for i in defender.status if i in combatstatus)
    attacker_trait_bonus = sum(combattraits[i] for i in attacker.traits if i in combattraits)
    defender_trait_bonus = sum(combattraits[i] for i in defender.traits if i in combattraits)

    attacker_odds = (weapon_damage(attacker, "damage")) + (attacker_status_bonus) + (attacker_trait_bonus)
    defender_odds = (weapon_damage(defender, "damage")) + (defender_status_bonus) + (defender_trait_bonus)
    print(attacker_odds)

    if ("nightvision" in attacker.traits) and day_night % 2 == 0:
        attacker_odds += 10

    if (("projectile protection" in attacker.traits) or ("cant see" in attacker.status)) and (defender_weapon.type == "longrange"):
        attacker_odds += 10
    if (("projectile protection" in defender.traits) or ("cant see"in defender.status)) and (attacker_weapon.type == "longrange"):
        attacker_odds -= 10

    def combat_outcome():
        combatdict = {0:"scratch" ,20: "bloodloss", 60: "fatal wound", 1000: "lethal damage taken" }
        for i in combatdict:
            num = int(i)
            if attacker_odds < num:
                attackerstatus = combatdict.get(i)
                attacker.status[attackerstatus] = day_night

        for i in combatdict:
            num = int(i)
            if defender_odds < num:
                defenderstatus = combatdict.get(i)
                defender.status[defenderstatus] = day_night
                if len(attacker_weapon.status) > 0:
                    defender.status[attacker_weapon.status[0]] = day_night
        flavour = [attacker, "fought" , defender, "atacker recieved" , attackerstatus, "the defender recieved", defenderstatus]
        return flavour
    
    def weapon_break(person, weapon):
        if (random.randint(0,5) == 5) and not any(i in person.traits for i in ["cant break weapon", "ropemaker"]) and (weapon != "hands"):
            person.inventory.remove(weapon)
        else:
            print("gjkfasklg")

    flavour = combat_outcome() 
    weapon_break(attacker,attacker_weapon)
    weapon_break(defender, defender_weapon)
    llm(attacker, flavour)
    

def combat(person, day_night):
    if "anticombat" in person.status:
        flavour = [person, "could not engage in combat", "due to the heavy rains"]
        return llm(person, flavour)
    roll = 0
    defender = input(f"select a player to attack from {tributes_instances}: ")
    for i in tributes_instances:
        if i.name == defender:
            defender_object = i
            if person.location != defender_object.location:
                flavour = [defender_object, "was in a different biome to" , person]
                return llm(person,flavour)
            roll = random.randint(0,100)
            evasion_odds = evasion(i,person,day_night)
    if evasion_odds < roll:
        flavour = [defender_object, "was found by", person]
        defender_action = input(f"{defender_object}: fight or flight?: ")
        if defender_action == "flight":
            flight(person,defender_object, day_night)
        else:
            fight(person,defender_object, day_night)
    else:
        flavour = [defender_object, "escaped from", person]
    llm(person, flavour)
        

def status_condition(person,day): 
    hpstatus = {"frozen": -5,"thirst": -5, "very healthy": 20 ,"healthy": 10, "rested": 5, "satiated": 15 , 
                "bloodloss": -10, "poison": -5, "magic power": 5, "scratch": -5}
    immunetraits = {"poison resistance": "poison", "camel": "thirst", "can smell water": "thirst", 
                    "can filter water": "thirst", "nocturnal": "insanity", "camelcamel": "extreme thirst"}
    

    tundra_effects = ["magic power", "cant move", "moreinsanity", "snow"]
    desert_effects = ["extreme thirst", "sanity", "hydrated", "heat", "mirage"]
    poisoncreek_effects = ["stinky", "damaged", "mist", "cant see", "lushlife"]

    for i in person.traits:
        if (i in immunetraits) and immunetraits.get(i) in person.status:
            person.status.pop(immunetraits.get(i))
    inflicted_statuses = list(person.status.keys())
    for i in inflicted_statuses:
        val = person.status.get(i)
        if (day - val ) >= 3:
            person.status.pop(i)
        else:
            if i in list(hpstatus.keys()):
                person.hp += hpstatus.get(i)
        if (i == "insanity") and ("sanity" in person.status):
            person.status.pop("insanity")
        elif (i == "hydrated") and ("hydrated" in person.status):
            person.status.pop("thirst")
        elif(i == "heat") and ("camel" not in person.traits):
            if random.randint(0,100) == 100:
                person.alive = False
                flavour = [person, "died due to the extreme heat of the desert"]
                llm(person,flavour)
        elif i == "mirage" or i == "cant move":
            person.status.pop(i)
        elif i == "lethal damage taken":
            person.alive = False
        elif (i == "damage") and random.randint(1,10) >= 9:
            person.hp -= 20
            person.status.pop("damage")
        elif (i == "lushlife") and (person.location != "poisoncreek"):
            person.status.pop("lushlife")
        elif(i in tundra_effects) and (person.location != "tundra"):
            person.status.pop(i)
        elif(i in desert_effects) and (person.location != "desert"):
            person.status.pop(i)
        elif(i in poisoncreek_effects) and (person.location != "poisoncreek"):
            person.status.pop(i)
        
            
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
    items = {"artecorp potions": "very healthy" , "potion": "healthy", "candy": "satiated" , "carrots": "enraged", "fish": "satiated",
              "witch potion": "magic power"}
    traps = ["bear trap","explosive","poison dart trap", "spike pit", ]
    print(person.inventory)
    pick = input("select an item:")
    if pick in person.inventory:
        add = items.get(pick)
        person.status[add] = day_night
    else:
        print("invalid")
        inventory(person)

    if pick in traps:
        for i in location_instances:
            if person.location == i.name:
                i.trap.append(pick)

def alliances(person):
    pass

def genitem(person):
    items = {"witch doctor": "witch potion" , "artecorp potions": "artecorp potions",
             "pet whale": "fish", "pet cat": "fish", "super strength carrots": "carrots" }
    for i in person.traits:
        if i in items:
            person.inventory.append(items.get(i))
    stoneweapons = ["ground stone axe", "flint dagger", "mace", "spears"]
    if "stoneweaponmaker" in person.traits:
        person.inventory.append(random.choice(stoneweapons))

def move(person, day_night, weatherdict):
    print(weatherdict)
    if "snow" in person.status:
        flavour = [person, "cannot exit the tundra due to the snow"]
        return llm(person, flavour)
    locs = ["tundra","desert","poisoncreek", "cornocopia"]
    curr = [i for i in location_instances if person.location == i.name][0]
    tomove = input((f"{curr.connections} {person.name} where do you want to go?:"))
    if tomove not in locs:
        print("error try again")
        move(person,day_night,weatherdict)
    if (tomove == "tundra") and (weatherdict.get("tundra") == "extreme snow"):
        flavour = [person, "could not enter into the tundra due to the snow"]
        return llm(person, flavour)
    if "mirage" in person.status:
        tomove = random.choice(locs)
    person.location = tomove
    newloc = [i for i in location_instances if tomove == i.name ][0]
    if newloc.status_effect != "none":
        person.status[newloc.status_effect] = day_night
        flavour = [person, "moved to", newloc, "and recieved the", newloc.status_effect]
    else:
        flavour = [person, "moved to", newloc]
    llm(person, flavour)

    if len(newloc.trap) > 0:
        trapdict = {"bear trap": "cant move", "poison dart trap": "poison", "spike pit": "bloodloss"
                    ,"explosive": "lethal damage taken"}
        key = newloc.trap[0]
        person.status[trapdict.get(key)] = day_night
        person.hp -= 10
        flavour=[person, "fell into" ,key, "and recieved" , trapdict.get(key)]
        newloc.trap.remove(key)
        llm(person,flavour)

def curr_weather():
    local_weather = {"tundra": "none", "poisoncreek": "none", "desert": "none"}
    for i in location_instances:
        local_weather[i.name] = i.curr_weather
    return local_weather

def weather(day):
    for i in location_instances:
        if random.randint(1,5) == 5:
            i.curr_weather = random.choice(i.weather_type)

    weather_dict  = curr_weather()

    tundra = {"aurora": "magic power", "snow layers": "cant move", 
                   "polar night": "moreinsanity", "extreme snow": "snow"}
    desert = {"drought": "extreme thirst", "pleasant night": "sanity",
              "heavy rains":"hydrated", "extreme heat": "heat", "mirage": "mirage"}
    poisoncreek = {"flood": "stinky", "slope failure": "damaged", "mist": "mist",
                   "thickfog":"cant see", "lushlife":"lushlife"}
    for i in tributes_instances:
        flavour = "none"
        if "builds shelter" in i.traits:
            flavour = [i, "is surviving in their shelter"]
            continue
        if (i.location == "tundra"):
            curr = weather_dict.get("tundra")
            if curr != "none":
                i.status[tundra.get(curr)] = day
                flavour = [i, "recieved the", curr, "status effect as he was in", i.location]
            if curr == "avalance":
                print("the avalanche is approaching you must move away from he tundra")
                move(i,day,weather_dict)
        elif i.location == "desert":
            curr = weather_dict.get("desert")
            if curr != "none":
                if (((curr == "drought") or (curr == "extreme head")) and ("camel" in i.traits)):
                    continue 
                i.status[desert.get(curr)] = day
                flavour = [i, "recieved the", curr, "status effect as he was in", i.location]
        elif i.location == "poisoncreek":
            curr = weather_dict.get("poisoncreek")
            if curr != "none":
                i.status[poisoncreek.get(curr)] = day
                flavour = [i, "recieved the", curr, "status effect as he was in", i.location]
        if flavour != "none":
            llm(i,flavour)
    return weather_dict 
            

def alliances(person,day):

    def formalliance():
        strangers = [i for i in tributes_instances if i.location == person.location]
        while True:
            ally = input(f"{strangers} who do you wish to form an alliance with?")
            for i in tributes_instances:
                target = next((t for t in tributes_instances if t.name == ally), None)
            if target and target.name != person.name:
                if target not in person.alliance:
                    person.alliance.append(target)
                    target.alliance.append(person)
                    print(f"Alliance formed with {target.name}")
                return 
            else:
                print("invalid")
    
    def trade(person):
        a = input(f"{tributes_instances}\n {person} choose a player to trade with")
        for i in tributes_instances:
            if i.name == a:
                trader = i
    
        take = input(f"{trader.inventory} {trader.name}inventory: ")
        give = input(f"{person.inventory} {person.name}inventory: ")

        confirm = input("confirmation")
        if confirm == "y":
            trader.inventory.append(give)
            trader.inventory.remove(take)
            person.inventory.append(take)
            person.inventory.remove(give)
            flavour = [person, "gave", give, "and recieved from", trader, take]
            llm(person,flavour)
    
    def backstab(person):
        if day % 2 == 1:
            print("backstabbing can only occur when night falls")
            return
        backstabbed = input(f"{person.alliance} select player to backstab")
        for i in tributes_instances:
            if i.name == backstabbed:
                backstabb = i
            else: return
        
        if "charismatic" in backstabb.traits:
            flavour = [backstabb, "staved off an attack from an ally"]
            llm(backstabb,flavour)
            return
        
        if random.randint(0,5) == 5:
            person.alive = False
            flavour = [person ,"tried to backstab", backstabb, "and was killed"]
        else:
            backstabb.alive = False
            flavour = [backstabb ,"was killed by an ally"]
        llm(backstabb,flavour)

    choice = input(f"{person} do you want to add allies")
    if choice == "yes":
        formalliance()
    else:
        flavour = [person, "has formed an alliance", person.alliance]
    

    allianceaction = input("what action do you want to do with your alliance")
    if allianceaction == "trade":
        trade(person)
    elif allianceaction == "backstab":
        backstab(person)
    llm(person,flavour)
    
def turn(person, day_night, weatherdict):
    while True:
        movechoice = input(f"{person} do you want to move")
        if "fast" in person.traits and movechoice == "yes":
            move(person, day_night, weatherdict)
            move(person, day_night, weatherdict)
        elif movechoice == "yes":
            move(person, day_night, weatherdict)
        if "cant move" in person.status:
            print(f"{person} is unable to move")
            break
        choice = input(f"what will {person} do!")
        if day_night % 3 == 0:
            genitem(person)
        if choice == "event":
            b = llm(person,"event")
            happenstance(person,b[0],day_night)
        elif choice == "inventory":
            inventory(person, day_night)
        elif choice == "combat":
            combat(person,day_night)
        elif choice == "ally":
            print("ran")
            alliances(person,day_night)
        else:
            print("invalid try again")
            turn(person,day_night, weather)
        person.hp -= 10
        if person.hp <= 0:
                person.alive = False
                if flag(tributes_instances) == False:
                    return False
        break

def main():
    day_night = 0
    while flag(tributes_instances):
        day_night += 1
        save()
        weather_dict = weather(day_night)
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
                turn(person,day_night,weather_dict)
            player_turns.remove(person)
            
    winners = [p for p in tributes_instances if p.alive]
    save()
    print(f"{winners[0].name} has won the hunger games!")

if __name__ == "__main__":
    main()