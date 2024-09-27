import numpy as np
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from database.db import db



# Function to normalize the data between 0 and 1, handling the case where max_vals == min_vals
def normalize_vectors(vectors):
    min_vals = np.min(vectors, axis=0)
    max_vals = np.max(vectors, axis=0)
    
    # Avoid division by zero by replacing (max_vals - min_vals) == 0 with 1 to avoid NaNs
    range_vals = max_vals - min_vals
    range_vals[range_vals == 0] = 1  # Prevent division by zero
    
    return (vectors - min_vals) / range_vals

# Function to calculate weighted Euclidean distance
def weighted_euclidean_distance(a, b, weights):
    return np.sqrt(np.sum(weights * (a - b) ** 2))

# KNN function
def knn_with_weighted_vector(target_vector, player_vectors, weights, k=5):
    distances = []
    
    # Normalize the player vectors and target vector
    normalized_player_vectors = normalize_vectors(player_vectors)
    normalized_target_vector = normalize_vectors(np.array([target_vector]))[0]  # normalize target_vector

    # Compute weighted Euclidean distances
    for i, player_vector in enumerate(normalized_player_vectors):
        distance = weighted_euclidean_distance(normalized_target_vector, player_vector, weights)
        distances.append((i, distance))  # store index and distance

    # Sort by distance and get top k nearest neighbors
    distances = sorted(distances, key=lambda x: x[1])
    top_k_indices = [idx for idx, _ in distances[:k]]
    
    return top_k_indices  # Return the indices of the top k neighbors

# Example of setting weights (more significance to pens_att and pens_made)
weights = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 1, 1, 1, 1, 1])

# Query to fetch player vectors and max values for each stat
query = """SELECT p.name, s.player_id, 
                ARRAY[
                        s.goals, s.shots_total, s.shots_on_target, s.shots_on_target_pct, s.shots_total_per90,
                        s.shots_on_target_per90, s.goals_per_shot, s.goals_per_shot_on_target, s.avg_shot_distance,
                        s.shots_free_kicks, s.pens_made, s.pens_att, s.xg, s.npxg, s.xg_per_shot, s.goals_minus_xg, s.npg_minus_npxg
                    ] AS stats_vector
            FROM public.shots s
            JOIN public.players p ON s.player_id = p.player_id;"""

# Fetch player vectors and max values
result_set = db.fetch(query=query)

# Replace None values with 0 in the stats vectors using list comprehension before converting to numpy arrays
player_vectors = np.array([[0 if x is None else x for x in row['stats_vector']] for row in result_set])

# Query to get max values for each stat
max_query = """
            SELECT 
                ARRAY[
                    MAX(s.goals), MAX(s.shots_total), MAX(s.shots_on_target), MAX(s.shots_on_target_pct), MAX(s.shots_total_per90),
                    MAX(s.shots_on_target_per90), MAX(s.goals_per_shot), MAX(s.goals_per_shot_on_target), MAX(s.avg_shot_distance),
                    MAX(s.shots_free_kicks), MAX(s.pens_made), MAX(s.pens_att), MAX(s.xg), MAX(s.npxg), MAX(s.xg_per_shot), 
                    MAX(s.goals_minus_xg), MAX(s.npg_minus_npxg)
                ] AS max_stats_vector
            FROM public.shots s
            JOIN public.players p ON s.player_id = p.player_id;
            """

# Fetch max values for each stat
max_result = db.fetch(query=max_query)

# Convert the max values to a numpy array
max_stats_vector = np.array(max_result[0]['max_stats_vector'])
print(f"Max: {max_stats_vector}")
# Create the ideal player vector by applying the weights to the max_stats_vector
ideal_target_vector = max_stats_vector * weights
print(f"Ideal: {ideal_target_vector}")

# Find top 5 most similar players to the ideal target vector using KNN
top_5_indices = knn_with_weighted_vector(ideal_target_vector, player_vectors, weights, k=10)

# Get the names of the top 5 players
top_5_players = [result_set[i]['name'] for i in top_5_indices]

if __name__ == "__main__":
    for player in top_5_players:
        print(player)