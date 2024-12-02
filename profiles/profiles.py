import numpy as np
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from database.tables.players import Players
from database.tables.shots import Shots
from database.tables.possession import Possession

from database.tables.misc import Misc
from database.tables.defensive_actions import DefensiveActions
from database.tables.passing import Passing
from database.tables.keepers_adv import KeeperAdv
from database.tables.goal_shot_creation import GoalShotCreation



def get_profile_weights(profile: list, verbose=False) -> np.array:
    """Input the player_profile list of tuples and get the weights as a numpy array. """
    final = []
    for stat in profile:
        # Have to make sure the weight is not None
        if verbose:
            final.append(stat)
        elif stat[1]:
            final.append(stat[1])
    return np.array(final)

def get_profile_attribute_list(profile: list) -> list:
    """Input the player_profile list of tuples and get the attributes list. """
    return [x[0] for x in profile]


def get_player_stats(input_list: list, db, season=None, player_ids=None) -> np.array:
    """
    This function is responsible for fetching the stats of players given a database db and an input list of wanted stats.
    Also you can input a string representing a season if wanted
    """
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
        "defensive_actions": DefensiveActions,
        "keeper_adv": KeeperAdv,
        "goalshotcreation": GoalShotCreation
    }
    joined_tables = set()


    # Join tables and add columns based on input_list
    selected_columns = []
    for item in input_list:
        # Split the table name and column name
        table_name, column_name = item.split('.')
        # Get the table alias
        table = table_mapping[table_name]

        # Dynamically join the table if not already done
        if table_name not in joined_tables:
            if table_name == "players":
                # Skip the players table
                continue
            else:
                if season:
                    query = query.join(table, (Players.player_id == table.player_id) &
                                       (Misc.season == table.season) & (Misc.club_id == table.club_id) &
                                       (table.season == season))
                else:
                    # Join the tables together with each iteration
                    query = query.join(table, (Players.player_id == table.player_id) &
                                       (Misc.season == table.season) &
                                       (Misc.club_id == table.club_id))

            joined_tables.add(table_name)

        # Add the column to the list of selected columns
        selected_columns.append(getattr(table, column_name))
    
    # Add the name and player_id to the output
    selected_columns = [Players.name, Players.player_id] + selected_columns
    # Modify the query to select the desired columns
    query = query.with_entities(*selected_columns)

    # Iterate over the list and print the column names
    if player_ids:
        query = query.filter(Players.player_id.in_(player_ids))
    # Execute the query
    results = query.all()

    # Convert the results to a numpy array
    # Replace None with 0 in the results
    cleaned_results = [[0 if value is None else value for value in row] for row in results]

    return np.array(cleaned_results)


