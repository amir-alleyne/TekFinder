from flask import Blueprint, jsonify
from sqlalchemy import text
from app import db
import pandas as pd


def read_data(filename):
    data = pd.read_csv(filename)
    return data


tables = Blueprint('tables', __name__)

@tables.route('/print_tables')
def print_tables():
    '''
    Print all tables in the database
    '''
    query = text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
    result = db.session.execute(query)
    table_names = [row[0] for row in result.fetchall()]

    tables_info = {}
    for table_name in table_names:
        column_query = text(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}';")
        column_result = db.session.execute(column_query)
        column_names = [row[0] for row in column_result.fetchall()]
        tables_info[table_name] = column_names

    return jsonify(tables_info)

@tables.route('/create_pass_types_table')
def create_pass_types_table():
    '''
    Create the pass_types table in the database
    '''
    db.create_tables("""CREATE TABLE public.pass_types (
                        player_id serial4 NOT NULL,
                        season varchar(10) NOT NULL,
                        club_id int4 NULL,
                        minute_90s float8 NULL,
                        attempted int4 NULL,
                        live int4 NULL,
                        dead int4 NULL,
                        fk int4 NULL,
                        through_balls int4 NULL,
                        switches int4 NULL,
                        crosses int4 NULL,
                        throw_ins int4 NULL,
                        corner_kicks int4 NULL,
                        corner_kicks_in int4 NULL,
                        corner_kicks_out int4 NULL,
                        corner_kicks_straight int4 NULL,
                        passes_completed int4 NULL,
                        passes_offside int4 NULL,
                        blocked_passes int4 NULL,
                        CONSTRAINT pass_types_pkey PRIMARY KEY (player_id, season, club_id),
                        CONSTRAINT fk_player FOREIGN KEY (player_id) REFERENCES public.players (player_id),
                        CONSTRAINT fk_club FOREIGN KEY (club_id) REFERENCES public.clubs (club_id)); """
                )
    
    return jsonify({"message": "Pass types table created"})


@tables.route('/create_goal_shot_creation_table')
def create_goal_shot_creation_table():
    '''
    Create the goal_shot_creation table in the database
    '''
    db.create_tables("""CREATE TABLE public.goal_shot_creation (
                        player_id serial4 NOT NULL,
                        season varchar(10) NOT NULL,
                        club_id int4 NULL,
                        minute_90s float8 NULL,
                        sca int4 NULL,
                        sca_90 float8 NULL,
                        passlive_sca int4 NULL,
                        passdead_sca int4 NULL,
                        to_sca int4 NULL,
                        sh_sca int4 NULL,
                        fld_sca int4 NULL,
                        def_sca int4 NULL,
                        gca int4 NULL,
                        gca_90 float8 NULL,
                        passlive_gca int4 NULL,
                        passdead_gca int4 NULL,
                        to_gca int4 NULL,
                        sh_gca int4 NULL,
                        fld_gca int4 NULL,
                        def_gca int4 NULL,
                        CONSTRAINT goal_shot_creation_pkey PRIMARY KEY (player_id, season),
                        CONSTRAINT fk_player FOREIGN KEY (player_id) REFERENCES public.players (player_id),
                        CONSTRAINT fk_club FOREIGN KEY (club_id) REFERENCES public.clubs (club_id)); """
                )
    
    return jsonify({"message": "Goal shot creation table created"})


@tables.route('/create_defensive_actions_table')
def create_defensive_actions_table():
    '''
    Create the defensive_actions table in the database
    '''
    db.create_tables("""CREATE TABLE public.defensive_actions (
                        player_id serial4 NOT NULL,
                        season varchar(10) NOT NULL,
                        club_id int4 NULL,
                        minute_90s float8 NULL,
                        tackles int4 NULL,
                        tackles_won int4 NULL,
                        tackles_def_3rd int4 NULL,
                        tackles_mid_3rd int4 NULL,
                        tackles_att_3rd int4 NULL,
                        dribble_tackles int4 NULL,
                        dribbles_vs int4 NULL,
                        dribble_tackles_pct float8 NULL,
                        dribbled_past int4 NULL,
                        blocks int4 NULL,
                        blocked_shots int4 NULL,
                        blocked_passes int4 NULL,
                        interceptions int4 NULL,
                        tackles_interceptions int4 NULL,
                        clearances int4 NULL,
                        errors int4 NULL,
                        CONSTRAINT defensive_actions_pkey PRIMARY KEY (player_id, season),
                        CONSTRAINT fk_player FOREIGN KEY (player_id) REFERENCES public.players (player_id),
                        CONSTRAINT fk_club FOREIGN KEY (club_id) REFERENCES public.clubs (club_id)); """
                )
    
    return jsonify({"message": "Defensive actions table created"})


@tables.route('/create_possession_table')
def create_possession_table():
    '''
    Create the possession table in the database
    '''
    db.create_tables("""CREATE TABLE public.possession (
                        player_id serial4 NOT NULL,
                        season varchar(10) NOT NULL,
                        club_id int4 NULL,
                        minute_90s float8 NULL,
                        touches int4 NULL,
                        touches_def_pen_area int4 NULL,
                        touches_def_3rd int4 NULL,
                        touches_mid_3rd int4 NULL,
                        touches_att_3rd int4 NULL,
                        touches_att_pen_area int4 NULL,
                        touches_live_ball int4 NULL,
                        dribbles int4 NULL,
                        dribbles_completed int4 NULL,
                        dribbles_completed_pct float8 NULL,
                        players_dribbled_past int4 NULL,
                        tackled_during_takeon int4 NULL,
                        tacked_takeon_pct float8 NULL,
                        carries int4 NULL,
                        total_carry_distance int4 NULL,
                        carry_progressive_distance int4 NULL,
                        progressive_carries int4 NULL,
                        carries_into_final_third int4 NULL,
                        carries_into_penalty_area int4 NULL,
                        missed_controls int4 NULL,
                        dispossessed int4 NULL,
                        passes_received int4 NULL,
                        progressive_passes_received int4 NULL,
                        CONSTRAINT possession_pkey PRIMARY KEY (player_id, season),
                        CONSTRAINT fk_player FOREIGN KEY (player_id) REFERENCES public.players (player_id),
                        CONSTRAINT fk_club FOREIGN KEY (club_id) REFERENCES public.clubs (club_id)); """
                )
    
    return jsonify({'message': "Possesion's table has been created"})
    

@tables.route('/create_shots_table')
def create_shots_table():
    '''
    Create the shots table in the database
    '''
    db.create_tables("""CREATE TABLE public.shots (
                        player_id serial4 NOT NULL,
                        season varchar(10) NOT NULL,
                        club_id int4 NULL,
                        minute_90s float8 NULL,
                        goals int4 NULL,
                        shots_total int4 NULL,
                        shots_on_target int4 NULL,
                        shots_on_target_pct float8 NULL,
                        shots_total_per90 float8 NULL,
                        shots_on_target_per90 float8 NULL,
                        goals_per_shot int4 NULL,
                        goals_per_shot_on_target int4 NULL,
                        avg_shot_distance float8 NULL,
                        shots_free_kicks int4 NULL,
                        pens_made int4 NULL,
                        pens_att int4 NULL,
                        xg int4 NULL,
                        npxg int4 NULL,
                        xg_per_shot float8 NULL,
                        goals_minus_xg int4 NULL,
                        npg_minus_npxg int4 NULL,
                        CONSTRAINT shots_pkey PRIMARY KEY (player_id, season),
                        CONSTRAINT fk_player FOREIGN KEY (player_id) REFERENCES public.players (player_id),
                        CONSTRAINT fk_club FOREIGN KEY (club_id) REFERENCES public.clubs (club_id)); """
                )


    return jsonify({"message": "Shots table has been created"})


@tables.route('/insert_passing_types_data')
def insert_passing_types_data():
    '''
    Insert passing types data into the database
    '''
    count = 0
    data = read_data("data/passing_types.csv")
    for row in data.iloc[2:].iterrows():
        curr_name = row[1][3]
        curr_club = row[1][2]

        # player_id = row[1][]
        season = row[1][1]
        minute_90s = row[1][8] if not pd.isna(row[1][8]) else 0
        attempted = row[1][9] if not pd.isna(row[1][9]) else 0
        live = row[1][10] if not pd.isna(row[1][10]) else 0
        dead = row[1][11] if not pd.isna(row[1][11]) else 0
        fk = row[1][12] if not pd.isna(row[1][12]) else 0
        through_balls = row[1][13] if not pd.isna(row[1][13]) else 0
        switches = row[1][14] if not pd.isna(row[1][14]) else 0
        crosses = row[1][15] if not pd.isna(row[1][15]) else 0
        throw_ins = row[1][16] if not pd.isna(row[1][16]) else 0
        corner_kicks = row[1][17] if not pd.isna(row[1][17]) else 0
        corner_kicks_in = row[1][18] if not pd.isna(row[1][18]) else 0
        corner_kicks_out = row[1][19] if not pd.isna(row[1][19]) else 0
        corner_kicks_straight = row[1][20] if not pd.isna(row[1][20]) else 0
        passes_completed = row[1][21] if not pd.isna(row[1][21]) else 0
        passes_offside = row[1][22] if not pd.isna(row[1][22]) else 0
        blocked_passes = row[1][23] if not pd.isna(row[1][23]) else 0

        # Make sure that none of these values are NaN and change them to 0.

        db.insert("""
            INSERT INTO pass_types (
                player_id, club_id, season, minute_90s, attempted, live, dead, fk, through_balls,
                switches, crosses, throw_ins, corner_kicks, corner_kicks_in, corner_kicks_out,
                corner_kicks_straight, passes_completed, passes_offside, blocked_passes
            )
            SELECT
                p.player_id, c.club_id, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            FROM
                players p
            JOIN clubs c ON p.club_id = c.club_id
            WHERE
                p.name = %s
                AND c.name = %s
            ON CONFLICT DO NOTHING;
            """,
            (
                season, minute_90s, attempted, live, dead, fk, through_balls,
                switches, crosses, throw_ins, corner_kicks, corner_kicks_in, corner_kicks_out,
                corner_kicks_straight, passes_completed, passes_offside, blocked_passes,
                curr_name, curr_club
            )
        )

        count += 1
        print(f"Inserted {curr_name} into the pass_types table. {count} rows inserted.")           
    return jsonify({"message": "Passing types data inserted"})


if __name__ == "__main__":

    from pathlib import Path

    fl = read_data("/Users/hayknazaryan/Desktop/School/Fall/CSC494/TekFinder/data/passing_types.csv")

    count = 0
    for row in fl.iloc[2:].iterrows():
        print(row[1][3])
        count += 1

    print(f"Total count: {count} \n")


        