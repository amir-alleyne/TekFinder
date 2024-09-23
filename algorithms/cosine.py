import numpy as np
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from pprint import pprint

from database.db import db




# Query to fetch all the players' stats
query = """SELECT p.name, s.player_id, s.season,
                ARRAY[
                        s.goals, s.shots_total, s.shots_on_target, s.shots_on_target_pct, s.shots_total_per90,
                        s.shots_on_target_per90, s.goals_per_shot, s.goals_per_shot_on_target, s.avg_shot_distance,
                        s.shots_free_kicks, s.pens_made, s.pens_att, s.xg, s.npxg, s.xg_per_shot, s.goals_minus_xg, s.npg_minus_npxg
                    ] AS stats_vector
            FROM public.shots s
            JOIN public.players p ON s.player_id = p.player_id;"""

# Fetch the result set
result_set = db.fetch(query=query)

# Replace None values with 0 in the stats vectors using list comprehension before converting to numpy arrays
player_vectors = np.array([[0 if x is None else x for x in row['stats_vector']] for row in result_set])

# Query to fetch Erling Haaland's stats
find_haaland_query = """SELECT p.name, s.player_id, s.season,
                            ARRAY[
                                s.goals, s.shots_total, s.shots_on_target, s.shots_on_target_pct, s.shots_total_per90,
                                s.shots_on_target_per90, s.goals_per_shot, s.goals_per_shot_on_target, s.avg_shot_distance,
                                s.shots_free_kicks, s.pens_made, s.pens_att, s.xg, s.npxg, s.xg_per_shot, s.goals_minus_xg, s.npg_minus_npxg
                            ] AS stats_vector
                        FROM public.shots s
                        JOIN public.players p ON s.player_id = p.player_id
                        WHERE p.name = 'Marcus Rashford' AND s.season = '2324';"""

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

# haaland = db.fetch(query=find_haaland_query)
max_player = db.fetch(query=find_haaland_query)

# Replace None values with 0 in Haaland's target vector using list comprehension
target_vector = np.array([0 if x is None else x for x in max_player[0]['stats_vector']])

# Cosine similarity function with division by zero prevention
def cosine_similarity(a, b):
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    
    # If either norm is zero, return 0 similarity
    if norm_a == 0 or norm_b == 0:
        return 0
    
    return np.dot(a, b) / (norm_a * norm_b)

# Compute cosine similarity for each player vector
similarities = [cosine_similarity(target_vector, player_vector) for player_vector in player_vectors]

# Find the indices of the top 5 most similar players (sorted by highest cosine similarity)
top_10_indices = np.argsort(similarities)[-10:][::-1]

# Print the top 5 most similar players
top_10_players = [(result_set[i]['name'], result_set[i]['season']) for i in top_10_indices]

if __name__ == "__main__":
    print("Top 10 most similar players are: \n")
    i = 1
    for player in top_10_players:
        print(f'{i}: {player}')
        i += 1

    # target_arr = np.array([10, 10, 10])

    # test_arr = np.array([[5, 5, 5],
    #                     [10, 2, 1],
    #                     [100, 1000, 45]])
    

    # print([cosine_similarity(target_arr, x) for x in test_arr])
    

