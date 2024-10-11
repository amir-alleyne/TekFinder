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

player_profiles = {
    "Target Man": ([
                    "players.player_id",
                    "players.name",
                    "shots.season",

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
                    )
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
        "misc": Misc
    }
    joined_tables = set()

    # Join tables and add columns based on input_list
    selected_columns = []
    for item in input_list:
        table_name, column_name = item.split('.')
        
        # Get the table alias
        table_alias = table_mapping[table_name]

        # Dynamically join the table if not already done
        if table_name not in joined_tables:
            if table_name == "players":
                continue
            else:
                query = query.join(table_alias, (Players.player_id == table_alias.player_id) & (Shots.season == table_alias.season))

            joined_tables.add(table_name)

        # Add the column to the list of selected columns
        selected_columns.append(getattr(table_alias, column_name))
    
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

    profile = player_profiles["Target Man"]

    # for player in get_player_stats(profile[0], db):
    #     print(player)

    # print(get_player_stats(profile[0], db)[:, 3:])

    normalized_player_data, player_data = preprocess(get_player_stats(profile[0], db), profile[1])

    print(recommend_players(np.ones(shape=13), normalized_player_data, 5, player_data))

