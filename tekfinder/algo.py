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
    knn = NearestNeighbors(n_neighbors=k, metric='manhattan')
    # knn = NearestNeighbors(n_neighbors=k, metric='euclidean')

    # Fit the KNN model to the player data
    knn.fit(player_data)

    # Find the k nearest neighbors to the target profile
    distances, indices = knn.kneighbors([target_profile])
    print("Distances: ", distances)
    d_min = np.min(distances)
    d_max = np.max(distances)

    # Normalize to a rating between 0 and 100
    # The reason why I am using 1 as the min distance is because nodes usually should not have a distance closer than 1 unless they are the node themselves
    ratings = 100 * (1 - (distances - 1) / (d_max - 1))

    print(f"Ratings: {ratings}")

    # Retrieve the recommended player profiles
    recommended_players = real_player_data[indices[0]]

    return recommended_players

def preprocess(player_data: np.array, weights, attributes=None):
    """Preprocesses the player data by normalizing the features.

    Args:
        player_data: A NumPy array containing the player data (features).

    Returns:
        A NumPy array of normalized player data.
    """

    # Normalize the player data
    # player_data = np.array([list(row.values()) for row in player_data])
    
    # Replace None values with 0
    player_data[player_data == None] = 0
    pd = player_data[:,3:].astype(np.float64)
    # Apply the weights to the player data
    pd = pd * weights
  
    # Normalize the player data between 0 and 1
    normalized_player_data = ((pd - np.min(pd)) / (np.max(pd) - np.min(pd)))
    if attributes:
        invert = [i-3 for i, attr in enumerate(attributes) if attr[1] is not None and attr[2]]
        for i in invert:
            normalized_player_data[:,i] = 1 - normalized_player_data[:,i]
     

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
    weights = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
    normalized_player_data, player_data = preprocess(player_data, weights)
    
    # Number of nearest neighbors to recommend
    k = 5
    target_profile = np.ones(len(normalized_player_data[0]))
    # # Recommend k nearest player profiles
    recommended_players = recommend_players(target_profile, normalized_player_data, k, player_data)
    # ind = recommend_players_weighted(target_profile, normalized_player_data, weights)
    # print(player_data[ind])
    # print the players with the corresponding features like goals: 0, shots_total: 1, shots_on_target: 2, shots_on_target_pct: 3, shots_total_per90: 4, shots_on_target_per90: 5, goals_per_shot: 6, goals_per_shot_on_target: 7, avg_shot_distance: 8, shots_free_kicks: 9, pens_made: 10, pens_att: 11, xg: 12, npxg: 13, xg_per_shot: 14, goals_minus_xg: 15, npg_minus_npxg: 16
    aligned_features = ["name", "season", "goals", "shots_total", "shots_on_target", "shots_on_target_pct", "shots_total_per90", "shots_on_target_per90", "goals_per_shot", "goals_per_shot_on_target", "avg_shot_distance", "shots_free_kicks", "pens_made", "pens_att", "xg", "npxg", "xg_per_shot", "goals_minus_xg", "npg_minus_npxg"]
    for i in range(len(recommended_players)):
        print(f"Player {i+1}:")
        for j in range(len(recommended_players[i])):
            print(f"{aligned_features[j]}: {recommended_players[i][j]}")
        print("\n")

    # print("Recommended: " , recommended_players)
