import json


# Read fighters json file
with open('bjj_fighters.json') as f:
    fighters = json.load(f)
    
# Output number of history elements for each fighter
for fighter in fighters:
    print(fighter['first_name'] + " " + fighter['last_name'] + ": " + str(len(fighter['history'])))
