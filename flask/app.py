from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
from sklearn.preprocessing import StandardScaler
import numpy as np
import pickle
import os
import boto3
import get_vs_record
from decimal import Decimal
from simplejson import JSONEncoder


app = Flask(__name__)
app.json_encoder = JSONEncoder
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
    has_record = record['wins_vs_opponent'] > 0 or record['losses_vs_opponent'] > 0

    # Different models with and without fight history
    if has_record:
        # Load model and scaler with fight history
        model = tf.keras.models.load_model('model_1.h5')
        with open('scaler_1.pkl', 'rb') as f:
            scaler = pickle.load(f)

        # Create numpy array, dynamodb returns numbers as Decimal objects, so have to cast to int
        input_arr = np.array([[int(fighter_1['wins']), int(fighter_1['losses']), int(fighter_1['losses_by_sub']),
                                int(fighter_2['wins']), int(fighter_2['losses']), int(fighter_2['losses_by_sub']),
                                record['wins_vs_opponent'], record['wins_vs_opponent_by_sub'], record['losses_vs_opponent'],
                                record['losses_vs_opponent_by_sub']]])
    else:
        # Load model and scaler without fight history
        model = tf.keras.models.load_model('model_2.h5')
        with open('scaler_2.pkl', 'rb') as f:
            scaler = pickle.load(f)

        # Create numpy array, dynamodb returns numbers as Decimal objects, so have to cast to int
        input_arr = np.array([[int(fighter_1['wins']), int(fighter_1['losses']), int(fighter_1['losses_by_sub']),
                                int(fighter_2['wins']), int(fighter_2['losses']), int(fighter_2['losses_by_sub'])]])

    # Apply scaler
    input_arr = scaler.transform(input_arr)

    # Predict
    prediction = model.predict(input_arr)[0]

    # Get vs history to display, if there is a history
    vs_history = []
    if has_record:
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
