

def run(fighter, opponent_id):
    # Create new record
    record = {
        'wins_vs_opponent': 0,
        'wins_vs_opponent_by_sub': 0,
        'losses_vs_opponent': 0,
        'losses_vs_opponent_by_sub': 0
    }

    # Go through all fights
    for fight in fighter['history']:
        # Found a fight vs opponent
        if fight['opponent_id'] == opponent_id:
            # Win
            if fight['win_loss'] == 'W':
                record['wins_vs_opponent'] += 1

                # Win by submission
                if is_by_submission(fight['method']):
                    record['wins_vs_opponent_by_sub'] += 1

            # Loss
            elif fight['win_loss'] == 'L':
                record['losses_vs_opponent'] += 1

                # Loss by submission
                if is_by_submission(fight['method']):
                    record['losses_vs_opponent_by_sub'] += 1

    return record


# If the method of win/loss was by submission
def is_by_submission(method):
    if 'Pts' in method:
        return False
    if 'Points' in method:
        return False
    if 'Adv' in method:
        return False
    if 'Ref' in method:
        return False
    if 'N/A' in method:
        return False
    if 'DQ' in method:
        return False
    if 'Injury' in method:
        return False
    if 'EBI' in method:
        return False
    return True


# Returns a record vs an opponent
if __name__ == '__main__':
    run()
