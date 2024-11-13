import json
from flask import Blueprint, jsonify, request
import numpy as np
from database.tables.players import Players
from app import db
from profiles.profiles import get_player_stats, get_profile_attribute_list, get_profile_weights
from tekfinder.algo import preprocess, recommend_players
from collections import OrderedDict

players_end = Blueprint('players', __name__)

with open('rest/profiles.json', 'r') as json_file:
    player_profiles = json.load(json_file)


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
    
    verbose = None
    try:
        verbose = data['verbose']
        del data['verbose']
    # Catch the KeyError in case the use forgot to mention verbose = True or False
    except KeyError:
        pass
    season = None
    try:
        season = data['season']
        del data['season']
 
    except KeyError:
        pass
    
    profile_input = {'profile': data.get('profile', '')}

   
    if profile_input['profile'] == '':
        return jsonify(["Error: Please enter a profile"])
    
    profile = player_profiles[profile_input['profile']] if profile_input['profile'] in player_profiles else []
    if profile == []:
        return jsonify(["Error: Please enter a correct profile"])

    del data['profile']
    json_search_results = db.json_search(Players, json.dumps(data))
    if not json_search_results:
        return jsonify({"error": "No players found"})
    
    for result in json_search_results:
        result.__dict__.pop('_sa_instance_state')
    json_search_player_ids = [result.player_id for result in json_search_results]

    profile_attributes_list = get_profile_attribute_list(profile)
    stats = get_player_stats(profile_attributes_list, db, player_ids=json_search_player_ids, season=season)

    if len(stats) == 0:
        return jsonify({"error": "No players found"})
    
    profile_weights = get_profile_weights(profile)
    normalized_player_data, player_data = preprocess(stats, profile_weights, profile)
    n = len(profile_weights)
    target = np.ones(n)
    result = recommend_players(target, normalized_player_data, 20, player_data)

    profile_attributes_list = ['name', 'player_id', 'season'] + profile_attributes_list[3:]

    if verbose:
        final_list = []
        for player in result:
            final_list.append(dict(zip(profile_attributes_list, player)))
        return jsonify(json.loads(json.dumps(final_list, sort_keys=False)))
    else:
        return jsonify([json.loads(json.dumps([res[0],res[2]], ensure_ascii=False)) for res in result])


@players_end.route('/profiles/custom', methods=['GET'])
def GetCustomProfilePlayers():
    data = request.args.to_dict()
    verbose = None
    if data == {}:
        return jsonify(["Error: Please enter a profile"])
    
    try:
        verbose = data['verbose']
    # Catch the KeyError in case the use forgot to mention verbose = True or False
    except KeyError:
        pass
    
    season = None
    try:
        season = data['season']
        del data['season']
 
    except KeyError:
        pass
    
    profile_input = {'profile': data.get('profile', '')}
   
    if profile_input['profile'] == '':
        return jsonify(["Error: Please enter a profile"])
    
    profile = player_profiles[profile_input['profile']] if profile_input['profile'] in player_profiles else []
    if profile == []:
        return jsonify(["Error: Please enter a correct profile"])

    del data['profile']
   
    json_search_results = db.json_search(Players, json.dumps({}))
    if not json_search_results:
        return jsonify({"error": "No players found"})

    for result in json_search_results:
        result.__dict__.pop('_sa_instance_state')
    json_search_player_ids = [result.player_id for result in json_search_results]


    profile_attributes_list = get_profile_attribute_list(profile)
    stats = get_player_stats(profile_attributes_list, db, player_ids=json_search_player_ids, season=season)
    if len(stats) == 0:
        return jsonify({"error": "No players found"})
    
    profile_weights = get_profile_weights(profile, verbose=True)
    for i in range(len(profile_weights)):
        if profile_weights[i][0] in data:
            profile_weights[i][1] = int(data[profile_weights[i][0]])
    profile_weights = np.array([x[1] for x in profile_weights[3:]])
  
    normalized_player_data, player_data = preprocess(stats, profile_weights, profile[3:])
    n = len(profile_weights)
    target = np.ones(n)
    result = recommend_players(target, normalized_player_data, 20, player_data)

    profile_attributes_list = ['name', 'player_id', 'season'] + profile_attributes_list[3:]

    if verbose:
        final_list = []
        for player in result:
            final_list.append(dict(zip(profile_attributes_list, player)))
        return jsonify(json.loads(json.dumps(final_list, sort_keys=False)))
    else:
        return jsonify([json.loads(json.dumps([res[0],res[2]], ensure_ascii=False)) for res in result])



@players_end.route('/profiles/weights', methods=['GET'])
def GetProfileWeights():
    data = request.args.to_dict()
    profile_input = {'profile': data.get('profile', '')}
    if profile_input['profile'] == '':
        return jsonify(["Error: Please enter a profile"])
    
    profile = player_profiles[profile_input['profile']] if profile_input['profile'] in player_profiles else []
    if profile == []:
        return jsonify(["Error: Please enter a correct profile"])
    
    profile_weights = get_profile_weights(profile, verbose=True)
    return str(profile_weights)
    
