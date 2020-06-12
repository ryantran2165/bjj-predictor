import json
import numpy as np
import random
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

    # Create examples and labels lists
    examples = []
    labels = []

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

            # Create new example
            example = [wins, wins_by_sub, losses, losses_by_sub, opponent_wins, opponent_wins_by_sub, opponent_losses, opponent_losses_by_sub,
                       record['wins_vs_opponent'], record['wins_vs_opponent_by_sub'], record['losses_vs_opponent'], record['losses_vs_opponent_by_sub']]

            # Add example
            examples.append(example)

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

            # Add label
            labels.append(result)

    # Zip to shuffle, then unzip
    zipped = list(zip(examples, labels))
    random.shuffle(zipped)
    unzipped = list(zip(*zipped))
    examples = unzipped[0]
    labels = unzipped[1]

    # Split into 80% train and 20% test
    num_train = int(len(examples) * 0.8)
    train_examples = examples[:num_train]
    train_labels = labels[:num_train]
    test_examples = examples[num_train:]
    test_labels = labels[num_train:]

    # Write to npz file
    np.savez('bjj.npz', train_examples=train_examples, train_labels=train_labels,
             test_examples=test_examples, test_labels=test_labels)
    print('Created: bjj.npz')


# Creates the bjj data
if __name__ == '__main__':
    remove_duplicates.run()
    clean_history.run()
    run()
