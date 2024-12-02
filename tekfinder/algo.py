import numpy as np
from sklearn.neighbors import NearestNeighbors
from typing import Tuple

def recommend_players(target_profile: np.ndarray, player_data: np.ndarray, k: int, real_player_data: np.ndarray) -> np.ndarray:
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
    # print("Distances: ", distances)
    d_min = np.min(distances)
    d_max = np.max(distances)

    # Normalize to a rating between 0 and 100
    # The reason why I am using 1 as the min distance is because nodes usually should not have a distance closer than 1 unless they are the node themselves
    ratings = 100 * (1 - (distances - 1) / (d_max - 1))

    # Retrieve the recommended player profiles
    recommended_players = real_player_data[indices[0]]

    return recommended_players

def preprocess(player_data: np.ndarray, weights: np.ndarray, attributes:list=None) -> Tuple[np.ndarray, np.ndarray]:
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
