import json

with open('events.json') as event_file:
    events = json.load(event_file)

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

for j in events:
    new_event = Event(
        event=j['event'],
        success_rate = j['success_rate'], 
        success=j['success'], 
        fail=j['fail'], 
        traits=j['traits']
    )
    events_instances.append(new_event)
