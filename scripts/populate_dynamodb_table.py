import boto3
import json


# Read fighters json file
with open('bjj_fighters.json') as f:
    fighters = json.load(f)

# Create database connection
dynamodb = boto3.resource('dynamodb')

# Get table
table = dynamodb.Table('fighters')

# Use batch writer
with table.batch_writer() as batch:
    for fighter in fighters:
        batch.put_item(
            Item={
                "id": fighter['id'],
                "first_name": fighter['first_name'],
                "last_name": fighter['last_name'],
                "nickname": fighter['nickname'],
                "team": fighter['team'],
                "wins": fighter['wins'],
                "wins_by_sub": fighter['wins_by_sub'],
                "losses": fighter['losses'],
                "losses_by_sub": fighter['losses_by_sub'],
                "history": fighter['history']
            }
        )
