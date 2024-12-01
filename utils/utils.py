
import json
from flask import jsonify


PLAYER_ATTRS = ['name', 'age', 'pos', 'nationality', 'club_id']  # Example attributes
with open('rest/profiles.json', 'r') as json_file:
    player_profiles = json.load(json_file)


def getPlayerData(data):
    """
    Takes in json input from the payload and extracts any possible player data from it

    Returns:
        dict: A dictionary containing the player attribute data
    """

    # Extract the player data from the json input
    player_data = {}
    for key in data:
        if key in PLAYER_ATTRS:
            player_data[key] = data[key]

    return player_data


def checkVerbose(data):
    """
    Checks if the verbose key is present in the json input

    Returns:
        bool: True if the verbose key is present, False otherwise
    """
    verbose = None
    
    try:
        verbose = data['verbose']
    # Catch the KeyError in case the use forgot to mention verbose = True or False
    except KeyError:
        pass
    return verbose

def checkSeason(data):
    """
    Checks if the season key is present in the json input

    Returns:
        str: The season string if present, None otherwise
    """
    season = None
    try:
        season = data['season']
    except KeyError:
        pass
    return season

def mutate_json_search_results(json_search_results):
    """
    Mutates the json search results to remove the _sa_instance_state key

    Returns:
        list: A list of dictionaries containing the player data
    """

    for result in json_search_results:
        result.__dict__.pop('_sa_instance_state')
    return json_search_results

def clean_data(data):
    """
    Cleans the data by checking if data is empty, if the profile is present and if the profile is correct

    """
    if data == {}:
        return {},[], None, None, jsonify(["Error: Please enter a profile"])
    
    verbose = checkVerbose(data)
    season = checkSeason(data)
    
    profile_input = {'profile': data.get('profile', '')}
    if profile_input['profile'] == '':
        return {},[], None, None, jsonify(["Error: Please enter a profile"])
    
    profile = fetch_profile(profile_input)
    if profile == []:
        return {},[], None, None, jsonify(["Error: Please enter a correct profile"])
    del data['profile']
    
    try:
        del data['verbose']
    except KeyError:
        pass

    return data, profile, verbose, season, None

def fetch_profile(profile_input):
    return player_profiles[profile_input['profile']] if profile_input['profile'] in player_profiles else []