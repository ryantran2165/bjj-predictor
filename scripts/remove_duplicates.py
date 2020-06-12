import json


def run():
    # Read fighters json file
    with open('bjj_fighters.json') as f:
        fighters = json.load(f)
        
    # List of all ids
    ids = []
    for fighter in fighters:
        ids.append(fighter['id'])
        
    # Set of duplicate ids
    duplicateIds = set(id for id in ids if ids.count(id) > 1)

    # Log number of duplicate ids
    print(str(len(duplicateIds)) + ' duplicate ids found')

    # List of lists for each duplicate id
    duplicates = [[fighter for fighter in fighters if fighter['id'] == duplicateId] for duplicateId in duplicateIds]

    # Log number of duplicates per id
    for duplicate in duplicates:
        print(str(duplicate[0]['id']) + ': ' + str(len(duplicate)) + ' duplicates')
        
    # Remove duplicates
    for duplicate in duplicates:
        bestScore = 0
        bestDuplicate = None
        
        # Find best score based on amount of info
        for dup in duplicate:
            score = 0
            
            # One point for each info detail available
            if dup['first_name'] is not None:
                score += 1
            if dup['last_name'] is not None:
                score += 1
            if dup['nickname'] is not None:
                score += 1
            if dup['team'] is not None:
                score += 1
            
            # Update new best
            if score > bestScore:
                bestScore = score
                bestDuplicate = dup
        
        # Remove non-bests from fighters
        for dup in duplicate:
            if dup is not bestDuplicate:
                fighters.remove(dup)
                
    # Update file if there are duplicates
    if len(duplicateIds) > 0:
        with open('bjj_fighters.json', 'w') as f:
            json.dump(fighters, f)


# Removes the duplicates
if __name__ == '__main__':
    run()
