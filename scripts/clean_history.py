import json


def run():
    # Read fighters json file
    with open('bjj_fighters.json') as f:
        fighters = json.load(f)
        
    # Create set of all fighter id's
    fighter_ids = {fighter['id'] for fighter in fighters}
    
    # Count number removed
    num_removed = 0

    # Go through each fighter
    for fighter in fighters:
        # Get their fight history
        history = fighter['history']

        # Go through each fight backwards to remove while iterating
        for i in range(len(history) - 1, -1, -1):
            # Get the fight
            fight = history[i]
        
            # Remove fight from history if opponent does not have a fight history
            if fight['opponent_id'] not in fighter_ids:
                history.remove(fight)
                num_removed += 1
                print("Removed: " + fight['opponent_id'] + ", " + fight['opponent_name'])

    # Log number removed
    print(str(num_removed) + " fights removed")

    # Update file if there were removals
    if num_removed > 0:
        with open('bjj_fighters.json', 'w') as f:
            json.dump(fighters, f)


# Cleans history
if __name__ == '__main__':
    run()
