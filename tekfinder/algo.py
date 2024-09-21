import numpy as np
from sklearn.neighbors import NearestNeighbors

def recommend_players(target_profile, player_data, k):
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
    recommended_players = player_data[indices[0]]

    return recommended_players

def recommend_players_weighted(target_profile, player_data):
    weights = np.array([0.9, 0.05, 0.05])



    # Calculate the weighted Euclidean distance
    distances = np.linalg.norm(player_data - target_profile, axis=1) * weights

    # Find the closest player
    closest_player_index = np.argmin(distances)
    closest_player = player_data[closest_player_index]

    print("Closest player:", closest_player)

def preprocess(player_data):
    """Preprocesses the player data by normalizing the features.

    Args:
        player_data: A NumPy array containing the player data (features).

    Returns:
        A NumPy array of normalized player data.
    """

    # Normalize the player data

    pass


if __name__ == '__main__':
    # Sample player data
    player_data = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    # normalized_player_data = preprocess(player_data)
    target_profile = np.array([1, 5, 6])

    # Number of nearest neighbors to recommend
    k =2

    # Recommend k nearest player profiles
    recommended_players = recommend_players_weighted(target_profile, player_data)

    print("Recommended: " , recommended_players)
