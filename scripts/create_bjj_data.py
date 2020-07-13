import json
import csv
import remove_duplicates
import clean_history
import get_vs_record


def run():
    # Read fighters json file
    with open('bjj_fighters.json') as f:
        fighters = json.load(f)

    # Create dict of all fighters by id
    fighters_dict = dict()
    for fighter in fighters:
        fighters_dict[fighter['id']] = fighter

    # Create data to convert to csv
    data = []
    
    # Add csv headers
    headers = ['wins', 'wins_by_sub', 'losses', 'losses_by_sub', 'opponent_wins', 'opponent_wins_by_sub', 'opponent_losses', 'opponent_losses_by_sub',
               'wins_vs_opponent', 'wins_vs_opponent_by_sub', 'losses_vs_opponent', 'losses_vs_opponent_by_sub', 'result']
    data.append(headers)
    
    # Create an example for each fight
    for fighter in fighters:
        # Dict for record vs opponents
        records_vs_opponents = dict()

        # Go through all fights
        for fight in fighter['history']:
            # This fighter's # wins
            wins = fighter['wins']

            # This fighter's # wins by submission
            wins_by_sub = fighter['wins_by_sub']

            # This fighter's # losses
            losses = fighter['losses']

            # This fighter's losses by submission
            losses_by_sub = fighter['losses_by_sub']

            # Get opponent
            opponent_id = fight['opponent_id']
            opponent = fighters_dict[opponent_id]

            # Opponent's # wins
            opponent_wins = opponent['wins']

            # Opponent's # wins by submission
            opponent_wins_by_sub = opponent['wins_by_sub']

            # Opponent's # losses
            opponent_losses = opponent['losses']

            # Opponent's # losses by submission
            opponent_losses_by_sub = opponent['losses_by_sub']

            # Get vs record if exists
            if opponent_id in records_vs_opponents:
                record = records_vs_opponents[opponent_id]
            else:
                # Get the vs record
                record = get_vs_record.run(fighter, opponent_id)

                # Add record to all records
                records_vs_opponents[opponent_id] = record

            # Get result of the fight
            if fight['win_loss'] == 'W':
                if get_vs_record.is_by_submission(fight['method']):
                    result = 0
                else:
                    result = 1
            elif fight['win_loss'] == 'L':
                if get_vs_record.is_by_submission(fight['method']):
                    result = 2
                else:
                    result = 3
            elif fight['win_loss'] == 'D':
                result = 4

            # Create new example
            example = [wins, wins_by_sub, losses, losses_by_sub, opponent_wins, opponent_wins_by_sub, opponent_losses, opponent_losses_by_sub,
                       record['wins_vs_opponent'], record['wins_vs_opponent_by_sub'], record['losses_vs_opponent'], record['losses_vs_opponent_by_sub'], result]

            # Add example to data
            data.append(example)

    with open('bjj_data.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)
        print('Created: bjj_data.csv')


# Creates the bjj data
if __name__ == '__main__':
    remove_duplicates.run()
    clean_history.run()
    run()
