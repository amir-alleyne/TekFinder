from dotenv import load_dotenv
import numpy as np
import psycopg2
from psycopg2.extras import RealDictCursor
from sklearn.neighbors import NearestNeighbors
import os

def recommend_players(target_profile, player_data, k, real_player_data):
    """Recommends k nearest player profiles based on a target profile.

    Args:
        target_profile: A list or NumPy array representing the target player profile.
        player_data: A NumPy array containing the player data (features).
        k: The number of nearest neighbors to find.

    Returns:
        A list of recommended player profiles.
    """

    # Create a NearestNeighbors object
    knn = NearestNeighbors(n_neighbors=k, metric='euclidean')

    # Fit the KNN model to the player data
    knn.fit(player_data)

    # Find the k nearest neighbors to the target profile
    distances, indices = knn.kneighbors([target_profile])
    print("Distances: ", distances)

    # Retrieve the recommended player profiles
    recommended_players = real_player_data[indices[0]]

    return recommended_players

def preprocess(player_data):
    """Preprocesses the player data by normalizing the features.

    Args:
        player_data: A NumPy array containing the player data (features).

    Returns:
        A NumPy array of normalized player data.
    """

    # Normalize the player data
    player_data = np.array([list(row.values()) for row in player_data])
    
    # Replace None values with 0
    player_data[player_data == None] = 0
    pd = player_data[:,2:]
    # Normalize the player data between 0 and 1
    normalized_player_data = ((pd - np.min(pd)) / (np.max(pd) - np.min(pd)))

    return normalized_player_data, player_data


if __name__ == '__main__':
    
    load_dotenv()
    print("============================Connecting to the database=============================")
    db = psycopg2.connect(
            f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}",
            cursor_factory=RealDictCursor
        )
    query = "SELECT p.name, s.season, goals,shots_total,shots_on_target,shots_on_target_pct,shots_total_per90,shots_on_target_per90,goals_per_shot,goals_per_shot_on_target,avg_shot_distance,shots_free_kicks,pens_made,pens_att,xg,npxg,xg_per_shot,goals_minus_xg,npg_minus_npxg FROM shots s join players p on p.player_id = s.player_id" #order by goals desc
    cur = db.cursor()
    cur.execute(query)
    player_data = cur.fetchall()
    np.set_printoptions(suppress=True)
    normalized_player_data, player_data = preprocess(player_data)
    
    # Number of nearest neighbors to recommend
    k = 10
    target_profile = np.ones(len(normalized_player_data[0]))
    # # Recommend k nearest player profiles
    recommended_players = recommend_players(target_profile, normalized_player_data, k, player_data)
    # ind = recommend_players_weighted(target_profile, normalized_player_data, weights)
    # print(player_data[ind])

    print("Recommended: " , recommended_players)
