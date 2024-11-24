
PLAYER_ATTRS = ['name', 'age', 'pos', 'nationality', 'club_id']  # Example attributes


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