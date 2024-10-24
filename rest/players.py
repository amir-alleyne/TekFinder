import json
from flask import Blueprint, jsonify, request
import numpy as np
from database.tables.players import Players
from app import db
from profiles.profiles import player_profiles, get_player_stats, search_and_filter
from tekfinder.algo import preprocess, recommend_players

players_end = Blueprint('players', __name__)

# GET request to retrieve players with specific attributes
@players_end.route('/', methods=['GET'])
def GetPlayers():
    """
    Takes in json input from the payload and uses the json search function to query the database
    """
   
    data = request.args.to_dict()
    results = db.json_search(Players, json.dumps(data))
    if not results:
        return jsonify({"error": "No players found"})
    results = [result.__dict__ for result in results]
    
    for result in results:
        result.pop('_sa_instance_state')
    return jsonify([json.loads(json.dumps(result, ensure_ascii=False)) for result in results])

@players_end.route('/profiles', methods=['GET'])
def GetProfilePlayers():
    data = request.args.to_dict()
    if data == {}:
        return jsonify(["Error: Please enter a profile"])
    
    profile = player_profiles[data['profile']] if data['profile'] in player_profiles else []
    if profile == []:
        return jsonify(["Error: Please enter a correct profile"])

    del data['profile']
    
    res = search_and_filter(Players, db, json.dumps(data), input_list=profile[0])
    if len(res) == 0:
        return jsonify({"error": "No players found"})
    json_search_results = db.json_search(Players, json.dumps(data))
    for result in json_search_results:
        result.__dict__.pop('_sa_instance_state')
    json_search_player_ids = [result.player_id for result in json_search_results]
    stats = get_player_stats(profile[0], db, player_ids=json_search_player_ids)

    if len(stats) == 0:
        return jsonify({"error": "No players found"})
    
    normalized_player_data, player_data = preprocess(stats, profile[1])
    n = len(profile[1])

    target = np.ones(n)
    result = recommend_players(target, normalized_player_data, 20, player_data)
   
   
    return jsonify([json.loads(json.dumps([res[0],res[2]], ensure_ascii=False)) for res in result])
