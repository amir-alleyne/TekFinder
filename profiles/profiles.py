import numpy as np
import sys
import os

from sqlalchemy import and_
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from database.tables.players import Players
from database.tables.shots import Shots
from database.tables.possession import Possession

from tekfinder.algo import preprocess, recommend_players
from database.tables.misc import Misc
from database.tables.defensive_actions import DefensiveActions
from database.tables.passing import Passing
from database.tables.keepers_adv import KeeperAdv
from database.tables.goal_shot_creation import GoalShotCreation

player_profiles = {
    "Target Man": [
        ("players.player_id", None),
        ("players.name", None),
        ("misc.season", None),
        ("shots.goals", 200),
        ("shots.shots_on_target", 80),
        ("shots.goals_per_shot", 20),
        ("shots.avg_shot_distance", 50),
        ("shots.xg", 20),
        ("possession.touches_att_pen_area", 20),
        ("possession.passes_received", 50),
        ("possession.progressive_passes_received", 50),
        ("possession.touches_att_3rd", 20),
        ("misc.offside", 20),
        ("misc.aerials_won", 300),
        ("misc.aerials_lost", 200),
        ("misc.aerials_won_pct", 200),
    ],
    "Box-to-Box": [
        ("players.player_id", None),
        ("players.name", None),
        ("misc.season", None),
        ("passing.completed_passes", 20),
        ("passing.attempted_passes", 20),
        ("passing.completed_percent", 20),
        ("passing.tot_dist", 20),
        ("passing.progressive_pass_dist", 50),
        ("passing.assists", 50),
        ("passing.expected_assists", 50),
        ("passing.key_passes", 50),
        ("passing.final_third_passes", 10),
        ("passing.passes_into_pen_area", 10),
        ("passing.progressive_passes", 20),
        ("defensive_actions.tackles", 30),
        ("defensive_actions.tackles_won", 30),
        ("defensive_actions.tackles_def_3rd", 50),
        ("defensive_actions.tackles_mid_3rd", 50),
        ("defensive_actions.tackles_att_3rd", 50),
        ("defensive_actions.interceptions", 30),
        ("defensive_actions.tackles_interceptions", 30),
        ("defensive_actions.blocks", 20),
        ("defensive_actions.dribble_tackles", 30),
        ("defensive_actions.dribble_tackles_pct", 30),
        ("possession.touches", 40),
        ("possession.touches_def_pen_area", 50),
        ("possession.touches_mid_3rd", 200),
        ("possession.touches_att_3rd", 200),
        ("possession.carries", 200),
        ("possession.progressive_carries", 50),
        ("possession.passes_received", 50),
        ("possession.progressive_passes_received", 50),
    ],
    "Deep Lying Playmaker": [
        ("players.player_id", None),
        ("players.name", None),
        ("misc.season", None),
        ("passing.attempted_passes", 100),
        ("passing.completed_passes", 200),
        ("passing.long_completed", 80),
        ("passing.long_completed_percent", 100),
        ("passing.key_passes", 50),
        ("passing.progressive_passes", 90),
        ("defensive_actions.tackles", 30),
        ("defensive_actions.interceptions", 40),
        ("defensive_actions.tackles_interceptions", 30),
        ("possession.touches", 100),
        ("possession.touches_def_3rd", 100),
        ("possession.touches_mid_3rd", 150),
        ("possession.carries", 80),
        ("possession.total_carry_distance", 50),
        ("possession.passes_received", 60),
    ],
    "Playmaker": [
        ("players.player_id", None),
        ("players.name", None),
        ("misc.season", None),
        ("passing.key_passes", 150),
        ("passing.assists", 80),
        ("passing.expected_assists", 150),
        ("passing.final_third_passes", 90),
        ("passing.passes_into_pen_area", 80),
        ("passing.progressive_passes", 70),
        ("shots.goals", 30),
        ("shots.shots_total", 30),
        ("shots.avg_shot_distance", 20),
        ("shots.xg", 30),
        ("possession.dribbles_completed", 40),
        ("possession.touches_att_3rd", 70),
        ("possession.carries_into_final_third", 70),
        ("possession.carries_into_penalty_area", 60),
    ],
    "False 9": [
        ("players.player_id", None),
        ("players.name", None),
        ("misc.season", None),
        ("passing.completed_passes", 30),
        ("passing.final_third_passes", 70),
        ("passing.key_passes", 60),
        ("passing.assists", 80),
        ("passing.expected_assists", 80),
        ("shots.goals", 200),
        ("shots.shots_total", 100),
        ("shots.xg", 150),
        ("possession.dribbles_completed", 80),
        ("possession.touches_mid_3rd", 75),
        ("possession.touches_att_3rd", 75),
        ("possession.carries_into_final_third", 80),
    ],
    "Inverted Fullback": [
        ("players.player_id", None),
        ("players.name", None),
        ("misc.season", None),
        ("passing.completed_passes", 60),
        ("passing.medium_completed", 70),
        ("passing.final_third_passes", 40),
        ("passing.crosses_into_pen_area", 40),
        ("defensive_actions.tackles", 60),
        ("defensive_actions.tackles_won", 60),
        ("defensive_actions.tackles_mid_3rd", 70),
        ("defensive_actions.interceptions", 50),
        ("defensive_actions.blocks", 50),
        ("possession.touches", 70),
        ("possession.touches_mid_3rd", 80),
        ("possession.carries", 60),
        ("possession.passes_received", 60),
    ],
    "Poacher": [
        ("players.player_id", None),
        ("players.name", None),
        ("misc.season", None),
        ("shots.goals", 150),
        ("shots.xg", 120),
        ("shots.npxg", 100),
        ("shots.shots_total", 100),
        ("shots.shots_on_target", 80),
        ("shots.goals_per_shot", 120),
        ("shots.avg_shot_distance", 0),
        ("possession.touches_att_pen_area", 140),
        ("possession.dribbles_completed", 70),
        ("possession.passes_received", 90),
        ("misc.pens_won", 40),
    ],
    "Sweeper Keeper": [
        ("players.player_id", None),
        ("players.name", None),
        ("misc.season", None),
        ("keeper_adv.def_act_outside_pen_area", 100),
        ("keeper_adv.def_act_outside_pen_area_per90", 200),
        ("keeper_adv.avg_distance_def_actions", 70),
    ],
    "Playmaking Keeper": [
        ("players.player_id", None),
        ("players.name", None),
        ("misc.season", None),
        ("keeper_adv.launched_passed_completed", 90),
        ("keeper_adv.launched_passes_att", 80),
        ("keeper_adv.launched_passes_completed_pct", 110),
        ("keeper_adv.passes_att_gk", 120),
        ("keeper_adv.throws_attempted", 70),
        ("keeper_adv.launch_pass_pct", 80),
        ("keeper_adv.avg_pass_len", 80),
        ("possession.touches", 300),
        ("possession.touches_def_pen_area", 80),
        ("possession.touches_def_3rd", 80),
        ("possession.touches_live_ball", 80),
        ("passing.completed_passes", 200),
        ("passing.attempted_passes", 100),
        ("passing.completed_percent", 100),
        ("passing.assists", 1000),
    ],
    "Tricky Winger": [
    ("players.player_id", None),
    ("players.name", None),
    ("misc.season", None),
    ("possession.touches_mid_3rd", 50),
    ("possession.touches_att_3rd", 70),
    ("possession.touches_att_pen_area", 80),
    ("possession.touches_live_ball", 70),
    ("possession.dribbles", 1000),
    ("possession.dribbles_completed", 280),
    ("possession.dribbles_completed_pct", 145),
    ("possession.tackled_during_takeon", 90),
    ("possession.carries", 95),
    ("possession.total_carry_distance", 80),
    ("possession.progressive_carries", 100),
    ("possession.carries_into_final_third", 80),
    ("possession.carries_into_penalty_area", 80),
    ("possession.dispossessed", 150),
    ("passing.expected_assisted_goals", 140),
    ("passing.expected_assists", 70),
    ("passing.assists_minus_expected_goals_assisted", 80),
    ("misc.crosses", 80),
    ("goalshotcreation.to_gca", 90),
    ("goalshotcreation.to_sca", 90),
    ("goalshotcreation.sca_90", 90),
    ("goalshotcreation.gca_90", 90),
],
"Ball Playing Centreback": [
    ("players.player_id", None),
    ("players.name", None),
    ("misc.season", None),
    ("passing.completed_passes", 150),
    ("passing.attempted_passes", 140),
    ("passing.completed_percent", 120),
    ("possession.touches", 100),
    ("possession.touches_def_pen_area", 110),
    ("possession.touches_def_3rd", 110),
    ("possession.touches_mid_3rd", 70),
    ("possession.touches_live_ball", 80),
    ("possession.dribbles", 60),
    ("possession.dribbles_completed", 60),
    ("possession.dribbles_completed_pct", 60),
    ("possession.tackled_during_takeon", 90),
    ("possession.carries", 90),
    ("possession.total_carry_distance", 90),
    ("possession.progressive_carries", 60),
    ("possession.dispossessed", 85),
    ("defensive_actions.tackles", 85),
    ("defensive_actions.tackles_won", 85),
    ("defensive_actions.tackles_def_3rd", 85),
    ("defensive_actions.dribble_tackles_pct", 85),
    ("defensive_actions.dribbles_vs", 85),
    ("defensive_actions.dribble_tackles", 85),
    ("defensive_actions.dribbled_past", 70),
],
"Traditional Centreback": [
    ("players.player_id", None),
    ("players.name", None),
    ("misc.season", None),
    ("defensive_actions.tackles", 120),
    ("defensive_actions.tackles_won", 180),
    ("defensive_actions.tackles_def_3rd", 90),
    ("defensive_actions.dribble_tackles_pct", 110),
    ("defensive_actions.dribbles_vs", 90),
    ("defensive_actions.dribble_tackles", 90),
    ("defensive_actions.dribbled_past", 90),
    ("defensive_actions.blocks", 100),
    ("defensive_actions.blocked_shots", 100),
    ("defensive_actions.blocked_passes", 100),
    ("defensive_actions.interceptions", 90),
    ("defensive_actions.tackles_interceptions", 80),
    ("defensive_actions.errors", 100),
    ("misc.pens_conceded", 60),
    ("misc.aerials_won", 140),
    ("misc.aerials_won_pct", 140),
],
"Traditional Fullback": [
    ("players.player_id", None),
    ("players.name", None),
    ("misc.season", None),
    ("misc.crosses", 150),
    ("misc.ball_recoveries", 100),
    ("defensive_actions.tackles", 90),
    ("defensive_actions.tackles_won", 90),
    ("defensive_actions.tackles_def_3rd", 90),
    ("defensive_actions.dribble_tackles_pct", 90),
    ("defensive_actions.dribbles_vs", 90),
    ("defensive_actions.dribble_tackles", 90),
    ("defensive_actions.dribbled_past", 90),
    ("defensive_actions.blocked_passes", 90),
    ("defensive_actions.interceptions", 90),
    ("possession.touches_def_3rd", 80),
    ("possession.touches_mid_3rd", 70),
    ("possession.progressive_carries", 70),
    ("possession.total_carry_distance", 80),
]
}

def get_profile_weights(profile: list) -> np.array:
    """Input the player_profile list of tuples and get the weights as a numpy array. """
    final = []
    for stat in profile:
        # Have to make sure the weight is not None
        if stat[1]:
            final.append(stat[1])
    return np.array(final)

def get_profile_attribute_list(profile: list) -> list:
    """Input the player_profile list of tuples and get the attributes list. """

    return [x[0] for x in profile]


def get_player_stats(input_list, db, season=None, player_ids=None):
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
                    query = query.join(table, (Players.player_id == table.player_id) & (Misc.season == table.season) & (Misc.club_id == table.club_id) & (table.season == season))
                else:
                    # Join the tables together with each iteration
                    query = query.join(table, (Players.player_id == table.player_id) & (Misc.season == table.season) & (Misc.club_id == table.club_id))

            joined_tables.add(table_name)

        # Add the column to the list of selected columns
        selected_columns.append(getattr(table, column_name))
    
    # Add the name and player_id to the output
    selected_columns = [Players.name, Players.player_id] + selected_columns
    # Modify the query to select the desired columns
    query = query.with_entities(*selected_columns)

    # Iterate over the list and print the column names
    column_names = [col.key for col in selected_columns]
    if player_ids:
        query = query.filter(Players.player_id.in_(player_ids))
    # Execute the query
    results = query.all()
    results_dict = [dict(zip(column_names, row)) for row in results]

    # Convert the results to a numpy array
    # Replace None with 0 in the results
    cleaned_results = [[0 if value is None else value for value in row] for row in results]

    return np.array(cleaned_results)


