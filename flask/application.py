from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
import numpy as np
import os
import boto3
import get_vs_record
from decimal import Decimal


application = app = Flask(__name__)
CORS(app)


@app.route('/')
def home():
    return 'BJJ Predictor API'


@app.route('/fighters', methods=['GET'])
def get_fighters():
    session = boto3.Session(
        aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
        region_name=os.environ['REGION_NAME']
    )
    dynamodb = session.resource('dynamodb')
    table = dynamodb.Table('fighters')

    # Get only a portion of all fighters' info for selection inputs
    fighters = []
    done = False
    start_key = None

    while not done:
        if start_key:
            response = table.scan(
                ProjectionExpression="id, first_name, last_name, nickname, team, wins, wins_by_sub, losses, losses_by_sub",
                ExclusiveStartKey=start_key,
            )
        else:
            response = table.scan(
                ProjectionExpression="id, first_name, last_name, nickname, team, wins, wins_by_sub, losses, losses_by_sub"
            )
        fighters = fighters + response.get("Items", [])
        start_key = response.get("LastEvaluatedKey", None)
        done = start_key is None
        
    return jsonify(fighters)


@app.route('/predict', methods=['GET'])
def get_prediction():
    session = boto3.Session(
        aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
        region_name=os.environ['REGION_NAME']
    )
    dynamodb = session.resource('dynamodb')
    table = dynamodb.Table('fighters')
    
    # Load the model
    model = tf.keras.models.load_model('bjj_model.h5')

    # Convert model to probability model
    model = tf.keras.Sequential([model, tf.keras.layers.Softmax()])

    # Load examples maxes for predictions
    path = os.path.join(os.getcwd(), 'examples_maxes.npz')
    with np.load(path) as data:
        examples_maxes = data['examples_maxes']

    # Get fighter id's from url parameters
    id_1 = request.args.get('id_1')
    id_2 = request.args.get('id_2')

    # Get fighter 1 from dynamodb
    response = table.get_item(
        Key={
            'id': id_1
        }
    )
    fighter_1 = response['Item']

    # Get fighter 2 from dynamodb
    response = table.get_item(
        Key={
            'id': id_2
        }
    )
    fighter_2 = response['Item']

    # Get record vs opponent
    record = get_vs_record.run(fighter_1, fighter_2['id'])

    # Create numpy array, dynamodb returns numbers as Decimal objects, so have to cast to int
    input_arr = np.array([int(fighter_1['wins']), int(fighter_1['wins_by_sub']), int(fighter_1['losses']), int(fighter_1['losses_by_sub']), int(fighter_2['wins']), int(fighter_2['wins_by_sub']), int(fighter_2['losses']),
                          int(fighter_2['losses_by_sub']), record['wins_vs_opponent'], record['wins_vs_opponent_by_sub'], record['losses_vs_opponent'], record['losses_vs_opponent_by_sub']])

    # Normalize input array
    input_arr = input_arr.astype('float32') / examples_maxes

    # Create model input
    model_input = np.expand_dims(input_arr, 0)

    # Predict
    prediction = model.predict(model_input)[0]

    # Get vs history to display
    vs_history = []
    for fight in fighter_1['history']:
        # Only get history vs opponent
        if fight['opponent_id'] == fighter_2['id']:
            # Don't need to include opponent id and name
            vs_history.append({
                'win_loss': fight['win_loss'],
                'method': fight['method'],
                'competition': fight['competition'],
                'weight': fight['weight'],
                'stage': fight['stage'],
                'year': fight['year']
            })

    return {
        'vs_history': vs_history,
        'win_by_sub': str(prediction[0]),
        'win_by_other': str(prediction[1]),
        'loss_by_sub': str(prediction[2]),
        'loss_by_other': str(prediction[3]),
        'draw': str(prediction[4])
    }


if __name__ == '__main__':
    app.run(debug=True)
