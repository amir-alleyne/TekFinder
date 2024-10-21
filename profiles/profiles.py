import numpy as np
import sys
import os
from sqlalchemy.orm import aliased
from sqlalchemy import select, func
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from database.alchemydb import Database
from database.tables.shots import Shots
from database.tables.possession import Possession
from database.tables.players import Players
from tekfinder.algo import preprocess, recommend_players
from database.tables.misc import Misc
from database.tables.defensive_actions import DefensiveActions
from database.tables.passing import Passing

player_profiles = {
    "Target Man": ([
                    "players.player_id",
                    "players.name",
                    
                    "misc.season",

                    "shots.goals",
                    "shots.shots_on_target",
                    "shots.goals_per_shot",
                    "shots.avg_shot_distance",
                    "shots.xg",
                    "possession.touches_att_pen_area",
                    "possession.passes_received",
                    "possession.progressive_passes_received",
                    "possession.touches_att_3rd",
                    "misc.offside",
                    "misc.aerials_won",
                    "misc.aerials_lost", #LOW
                    "misc.aerials_won_pct"
                    ],
                    np.array([
                        50,
                        40,
                        20,
                        80,
                        20,
                        20,
                        50,
                        50,
                        20,
                        20,
                        200,
                        200,
                        200
                    ])
                    ),
    "Box-to-Box": ([
                    "players.player_id",
                    "players.name",
                    
                    "misc.season",

                    "passing.completed_passes",
                    "passing.attempted_passes",
                    "passing.completed_percent",
                    "passing.tot_dist",
                    "passing.progressive_pass_dist",
                    "passing.assists",
                    "passing.expected_assists",
                    "passing.key_passes",
                    "passing.final_third_passes",
                    "passing.passes_into_pen_area",
                    "passing.progressive_passes",

                    "defensive_actions.tackles",
                    "defensive_actions.tackles_won", # aggregate all the values from a table and then compare with the aggregate
                    "defensive_actions.tackles_def_3rd",
                    "defensive_actions.tackles_mid_3rd",
                    "defensive_actions.tackles_att_3rd",
                    "defensive_actions.interceptions",
                    "defensive_actions.tackles_interceptions",
                    "defensive_actions.blocks",
                    "defensive_actions.dribble_tackles",
                    "defensive_actions.dribble_tackles_pct",

                    "possession.touches",
                    "possession.touches_def_pen_area",
                    "possession.touches_mid_3rd",
                    "possession.touches_att_3rd",
                    "possession.carries",
                    "possession.progressive_carries",
                    "possession.passes_received",
                    "possession.progressive_passes_received"
                    ],
                    np.array([
                        20,20,20,20,50,50,50,50,10,10,20,30,30,50,50,50,30,30,20,30,30,40,50,200,200,200,50,50,50

                    ])
                    ),
    "Deep Lying Playmaker": ([
                    "players.player_id",
                    "players.name",

                    "misc.season",

                    "passing.attempted_passes",
                    "passing.completed_passes",
                    "passing.long_completed",
                    "passing.long_completed_percent",
                    "passing.key_passes",
                    "passing.progressive_passes",

                    "defensive_actions.tackles",
                    "defensive_actions.interceptions",
                    "defensive_actions.tackles_interceptions",
                    
                    "possession.touches",
                    "possession.touches_def_3rd",
                    "possession.touches_mid_3rd",
                    "possession.carries",
                    "possession.total_carry_distance",
                    "possession.passes_received"],
                    np.array([
                        100,200,80,100,50,90,30,40,30,100,100,150,80,50,60
                    ])
    ),

    "Playmaker": ([
                    "players.player_id",
                    "players.name",

                    "misc.season",

                    "passing.key_passes",
                    "passing.assists",
                    "passing.expected_assists",
                    "passing.final_third_passes",
                    "passing.passes_into_pen_area",
                    "passing.progressive_passes",

                    "shots.goals",
                    "shots.shots_total",
                    "shots.avg_shot_distance",
                    "shots.xg",

                    "possession.dribbles_completed",
                    "possession.touches_att_3rd",
                    "possession.carries_into_final_third",
                    "possession.carries_into_penalty_area"
                    ],
                    np.array([
                        150,80,100,90,80,70,30,30,20,30,40,70,70,60
                    ]))
}

def get_player_stats(input_list, db):
    # Define aliases for the tables to make joins
    # Initialize the base query for Player
    query = db.query(Players)

    # Dictionary to map table names to their corresponding SQLAlchemy models and aliases
    table_mapping = {
        "shots": Shots,
        "possession": Possession,
        "players": Players,
        "misc": Misc,
        "passing": Passing,
        "defensive_actions": DefensiveActions
    }
    joined_tables = set()

    # Join tables and add columns based on input_list
    selected_columns = []
    for item in input_list:
        table_name, column_name = item.split('.')
        # Get the table alias
        table = table_mapping[table_name]

        # Dynamically join the table if not already done
        if table_name not in joined_tables:
            if table_name == "players":
                continue
            else:
                query = query.join(table, (Players.player_id == table.player_id) & (Misc.season == table.season) & (Misc.club_id == table.club_id))

            joined_tables.add(table_name)

        # Add the column to the list of selected columns
        selected_columns.append(getattr(table, column_name))
    
    selected_columns = [Players.name, Players.player_id] + selected_columns
    # Modify the query to select the desired columns
    query = query.with_entities(*selected_columns)

    # Iterate over the list and print the column names
    column_names = [col.key for col in selected_columns]
    print(column_names)
    
    # Execute the query
    results = query.all()
    results_dict = [dict(zip(column_names, row)) for row in results]
    # print(results_dict[0])

    # Convert the results to a numpy array
    # Replace None with 0 in the results
    cleaned_results = [[0 if value is None else value for value in row] for row in results]
    # print(f"Cleaned: {(cleaned_results)[0][3:]}")
    return np.array(cleaned_results)


if __name__ == "__main__":
    db = Database()

    profile = player_profiles["Playmaker"]

    # for player in get_player_stats(profile[0], db):
    #     print(player)

    # print(get_player_stats(profile[0], db)[:, 3:])

    normalized_player_data, player_data = preprocess(get_player_stats(profile[0], db), profile[1])

    print(recommend_players(np.ones(shape=14), normalized_player_data, 10, player_data))

