import numpy as np
from sklearn.neighbors import NearestNeighbors
from typing import Tuple
import math

def _get_tek_score(distances: np.ndarray, alpha: float = 0.85) -> np.ndarray:
        """
        This is a private helper function to calculate a score given the distances found from KNN.
        The technique used is Exponential scaling. It can expand smaller differences while
        compressing larger ones. Furthermore, alpha is a constant that determines the rate of decay.
        Larger alpha results in more steeply compressed scores.

        Args:
            distances: A NumPy array which lists the distances of the chosen player nodes
                       based on our KNN algorithm.
            alpha: A float value which determines the rate of decay

        Returns:
            A NumPy array of the TekScores for each shortlisted player
        """
        min_distance = np.min(distances)

        # Apply exponential scaling
        scores = 95 * np.exp(-alpha * (distances - min_distance))

        return scores


def recommend_players(target_profile: np.ndarray, player_data: np.ndarray, 
                      k: int, real_player_data: np.ndarray) -> np.ndarray:
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

    # Retrieve the recommended player profiles
    recommended_players = real_player_data[indices[0]].tolist()

    scores = _get_tek_score(distances=distances).tolist()[0]


    for i in range(len(recommended_players)):
        recommended_players[i].append(math.ceil(scores[i]))

    return np.array(recommended_players)


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
