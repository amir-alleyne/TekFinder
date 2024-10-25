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
                    "defensive_actions.tackles_won",
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
                        150,80,150,90,80,70,30,30,20,30,40,70,70,60
                    ])),
    
    "False 9": ([
                    "players.player_id",
                    "players.name",

                    "misc.season",

                    "passing.completed_passes",
                    "passing.final_third_passes",
                    "passing.key_passes",
                    "passing.assists",
                    "passing.expected_assists",

                    "shots.goals",
                    "shots.shots_total",
                    "shots.xg",

                    "possession.dribbles_completed",
                    "possession.touches_mid_3rd",
                    "possession.touches_att_3rd",
                    "possession.carries_into_final_third"
                ],
                np.array([
                    30,70,60,80,80,200,100,150,80,75,75,80
                ])),
    
    "Inverted Fullback": ([
                    "players.player_id",
                    "players.name",

                    "misc.season",

                    "passing.completed_passes",
                    "passing.medium_completed",
                    "passing.final_third_passes",
                    "passing.crosses_into_pen_area",

                    "defensive_actions.tackles",
                    "defensive_actions.tackles_won",
                    "defensive_actions.tackles_mid_3rd",
                    "defensive_actions.interceptions",
                    "defensive_actions.blocks",

                    "possession.touches",
                    "possession.touches_mid_3rd",
                    "possession.carries",
                    "possession.passes_received"
                    ],
                    np.array([
                        60,70,40,40,60,60,70,50,50,70,80,60,60
                    ])),
    
    "Poacher": ([
                    "players.player_id",
                    "players.name",

                    "misc.season",

                    "shots.goals",
                    "shots.xg",
                    "shots.npxg",
                    "shots.shots_total",
                    "shots.shots_on_target",
                    "shots.goals_per_shot",
                    "shots.avg_shot_distance",

                    "possession.touches_att_pen_area",
                    "possession.dribbles_completed",
                    "possession.passes_received",
                    "misc.pens_won"
                ],
                np.array([
                    # Whats the best way to make sure one of the values is as low as possible?
                    150,120,100,100,80,120,0,140,70,90,40
                ])),
    
    "Sweeper Keeper": ([
                    "players.player_id",
                    "players.name",

                    "misc.season",

                    "keeper_adv.def_act_outside_pen_area",
                    "keeper_adv.def_act_outside_pen_area_per90",
                    "keeper_adv.avg_distance_def_actions"
                ],
                np.array([
                    100,200,70
                ])),
    
    "Playmaking Keeper": ([
                    "players.player_id",
                    "players.name",

                    "misc.season",

                    "keeper_adv.launched_passed_completed",
                    "keeper_adv.launched_passes_att",
                    "keeper_adv.launched_passes_completed_pct",
                    "keeper_adv.passes_att_gk",
                    "keeper_adv.throws_attempted",
                    "keeper_adv.launch_pass_pct",
                    "keeper_adv.avg_pass_len",

                    "possession.touches",
                    "possession.touches_def_pen_area",
                    "possession.touches_def_3rd",
                    "possession.touches_live_ball",
                    
                    "passing.completed_passes",
                    "passing.attempted_passes",
                    "passing.completed_percent",
                    "passing.assists"
                ],
                np.array([
                    90,80,110,120,70,80,80,300,80,80,80,200,100,100,1000
                ])),
    
    "Tricky Winger": ([
                    "players.player_id",
                    "players.name",

                    "misc.season",

                    "possession.touches_mid_3rd",
                    "possession.touches_att_3rd",
                    "possession.touches_att_pen_area",
                    "possession.touches_live_ball",
                    "possession.dribbles",
                    "possession.dribbles_completed",
                    "possession.dribbles_completed_pct",
                    "possession.tackled_during_takeon", # LOW
                    "possession.carries",
                    "possession.total_carry_distance",
                    "possession.progressive_carries",
                    "possession.carries_into_final_third",
                    "possession.carries_into_penalty_area",
                    "possession.dispossessed", # LOW

                    "passing.expected_assisted_goals",
                    "passing.expected_assists",
                    "passing.assists_minus_expected_goals_assisted",

                    "misc.crosses",

                    "goalshotcreation.to_gca",
                    "goalshotcreation.to_sca",
                    "goalshotcreation.sca_90",
                    "goalshotcreation.gca_90"
                ],
                np.array([
                    50,70,80,70,1000,280,145,90,95,80,100,80,80,150,140,70,80,80,90,90,90,90
                ])),

    "Ball Playing Centreback": ([
                    "players.player_id",
                    "players.name",

                    "misc.season",

                    "passing.completed_passes",
                    "passing.attempted_passes",
                    "passing.completed_percent",

                    "possession.touches",
                    "possession.touches_def_pen_area",
                    "possession.touches_def_3rd",
                    "possession.touches_mid_3rd",
                    "possession.touches_live_ball",
                    "possession.dribbles",
                    "possession.dribbles_completed",
                    "possession.dribbles_completed_pct",
                    "possession.tackled_during_takeon", # LOW
                    "possession.carries",
                    "possession.total_carry_distance",
                    "possession.progressive_carries",
                    "possession.dispossessed", #LOW

                    "defensive_actions.tackles",
                    "defensive_actions.tackles_won",
                    "defensive_actions.tackles_def_3rd",
                    "defensive_actions.dribble_tackles_pct",
                    "defensive_actions.dribbles_vs",
                    "defensive_actions.dribble_tackles",
                    "defensive_actions.dribbled_past" #LOW
                ],
                np.array([
                    150,140,120,100,110,110,70,80,60,60,60,60,90,90,90,60,85,85,85,85,85,85,70
                ])),

    "Traditional Centreback": ([
                    "players.player_id",
                    "players.name",

                    "misc.season",

                    "defensive_actions.tackles",
                    "defensive_actions.tackles_won",
                    "defensive_actions.tackles_def_3rd",
                    "defensive_actions.dribble_tackles_pct",
                    "defensive_actions.dribbles_vs",
                    "defensive_actions.dribble_tackles",
                    "defensive_actions.dribbled_past", #LOW
                    "defensive_actions.blocks",
                    "defensive_actions.blocked_shots",
                    "defensive_actions.blocked_passes",
                    "defensive_actions.interceptions",
                    "defensive_actions.tackles_interceptions",
                    "defensive_actions.errors", # LOW

                    "misc.pens_conceded", # LOW
                    "misc.aerials_won",
                    "misc.aerials_won_pct"

                ],
                np.array([
                    120,180,90,110,90,90,90,100,100,100,90,80,100,60,140,140
                ])),

    "Traditional Fullback": ([
                    "players.player_id",
                    "players.name",

                    "misc.season",

                    "misc.crosses",
                    "misc.ball_recoveries",

                    "defensive_actions.tackles",
                    "defensive_actions.tackles_won",
                    "defensive_actions.tackles_def_3rd",
                    "defensive_actions.dribble_tackles_pct",
                    "defensive_actions.dribbles_vs",
                    "defensive_actions.dribble_tackles",
                    "defensive_actions.dribbled_past", # LOW
                    "defensive_actions.blocked_passes",
                    "defensive_actions.interceptions",

                    "possession.touches_def_3rd",
                    "possession.touches_mid_3rd",
                    "possession.progressive_carries",
                    "possession.total_carry_distance"
                ],
                np.array([
                    150,100,90,90,90,90,90,90,90,90,80,70,70,80,80
                ]))
}

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


