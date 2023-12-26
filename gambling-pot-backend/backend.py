import sys
import uuid
from gevent import monkey
from pot import distrPoints
from gevent.pywsgi import WSGIServer

monkey.patch_all()

from flask import Flask, jsonify, request
from flask_cors import CORS
import json, atexit, time


USERS_PATH = 'data/users.json'
STATE_PATH = 'data/gamestate.json'
TRANSACTIONS_PATH = 'data/transactions.json'
SERVER = '0.0.0.0'
DEBUG = False

app = Flask(__name__)
app.config.from_object(__name__)

CORS(app, resources={r'/*': {'origins': '*'}})

"""
@app.route('/<path:path>')
def get_data(path):
    segments = path.split('/')
    if segments[0] == 'users':
        result = users
    elif segments[0] == 'items':
        result = items
    elif segments[0] == 'transactions':
        result = transactions
    else:
        return 'Invalid path!'
    segments.pop(0)
    for segment in segments:
        if segment in result:
            result = result[segment]
        elif type(result) == list and segment.isdigit() and len(result) > int(segment):
            result = result[int(segment)]
        else:
            return 'Invalid path!'
    return jsonify(result)

"""

@app.route('/users')
def get_users():
    return jsonify(users)

@app.route('/gamestate')
def get_gamestate():
    return jsonify(gamestate)

@app.route('/bets')
def get_transactions():
    return jsonify(transactions)

@app.route('/pots')
def results_pots():
    potForOpt = {}
    playerOptSelection = {}
    for e in transactions:
        if e["gameId"] != gamestate["gameId"]:
            continue

        if e["round"] != gamestate["round"]:
            continue

        playerOptSelection[e["id"]] = e['optSelected']
        if not (e['optSelected'] in potForOpt):
            potForOpt[e['optSelected']] = 0
        
        potForOpt[e['optSelected']] = potForOpt[e['optSelected']] + 1

    for i in [-1, 0, 1]:
        if not (i in potForOpt):
            potForOpt[i] = 0

    for user in users['users']:
        if not (user['id'] in playerOptSelection):
            potForOpt[-1] = potForOpt[-1] + 1


    return jsonify(potForOpt)

@app.route('/bets/add', methods=['POST'])
def add_transaction():
    transaction = request.json

    if gamestate['gameId'] != transaction['gameId']:
        return "Wrong Game"

    if gamestate['round'] != transaction["round"]:
        return "Wrong Round"
    
    if gamestate['betLocked']:
        return "Bets Locked"

    for e in transactions:
        if e['gameId'] == transaction['gameId'] and e['round'] == transaction['round'] and e['id'] == transaction['id']:
            print('Player Already Voted')
            return 'Player Already Voted'

    transactions.append(transaction)
    save_json(transactions, TRANSACTIONS_PATH)   
    return "Transaction recieved!" 


@app.route('/bets/lock', methods=['POST'])
def lock_bets():
    gamestate['betLocked'] = True

    save_json(gamestate, STATE_PATH)
    return "Bets Locked!" 


@app.route('/bets/unlock', methods=['POST'])
def unlock_bets():
    gamestate['betLocked'] = False

    save_json(gamestate, STATE_PATH)
    return "Bets Unlocked!" 

@app.route('/bets/choice', methods=['POST'])
def bet_status():
    data = request.json
    
    for tr in transactions:
        if tr['id'] == data['id'] and tr['gameId'] == data['gameId'] and tr['round'] == data['round']:
            return jsonify({'id': data['id'], 'optSelected': tr['optSelected']})

    return jsonify({'id': data['id'], 'optSelected': -1})


@app.route('/round/finish', methods=['POST'])
def finish_round():
    data = request.json

    res = round_results(data['opt'])    
    for u, a in res.items():
        for user in users['users']:
            if u == user['id']:
                user['balance'] = user['balance'] + a
    
    gamestate['round'] = gamestate['round'] + 1
    gamestate['betLocked'] = False
    save_json(users, USERS_PATH)
    save_json(gamestate, STATE_PATH)
    return "Next Round Initiated"

@app.route('/round/reset', methods=['POST'])
def reset_round():
    gamestate['gameId'] = str(uuid.uuid4())
    gamestate['round'] = 0
    for user in users['users']:
        user['balance'] = 0

    save_json(users, USERS_PATH)
    save_json(gamestate, STATE_PATH)
    return "Next Round Initiated"



def round_results(winOption):
    playerOptSelection = {}
    potForOpt = {}
    for e in transactions:
        if e["gameId"] != gamestate["gameId"]:
            continue

        if e["round"] != gamestate["round"]:
            continue

        playerOptSelection[e["id"]] = e['optSelected']
        if not (e['optSelected'] in potForOpt):
            potForOpt[e['optSelected']] = 0
        
        potForOpt[e['optSelected']] = potForOpt[e['optSelected']] + gamestate['betAmount']
    
    for user in users['users']:
        if not (user['id'] in playerOptSelection):
            playerOptSelection[user['id']] = -1

    potForOpt[-1] = 0

    return distrPoints(playerOptSelection, potForOpt, gamestate['betAmount'], winOption)



def load_json(path):
    with open(path, 'r', encoding='utf-8') as json_file:
        return json.load(json_file)


def save_json(data_to_save, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data_to_save, f, ensure_ascii=False, indent=4)


def load_data():
    global users, gamestate, transactions
    users = load_json(USERS_PATH)
    gamestate = load_json(STATE_PATH)
    transactions = load_json(TRANSACTIONS_PATH)


def save_data():
    save_json(users, USERS_PATH)
    save_json(gamestate, STATE_PATH)
    save_json(transactions, TRANSACTIONS_PATH)


def run():
    load_data()

    atexit.register(save_data)

    http_server = WSGIServer((SERVER, 5000), app)
    http_server.serve_forever()
     


if __name__ == '__main__':
    run()