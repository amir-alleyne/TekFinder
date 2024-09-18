import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os
import pandas as pd

class Database:
    """
    Database class to handle database operations
    
    Attributes:
    connection: psycopg2 connection object
    cursor: psycopg2 cursor object
    """

    def __init__(self):
        load_dotenv()
        print("============================Connecting to the database=============================")
        self.connection = psycopg2.connect(
            f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}",
            cursor_factory=RealDictCursor
        )
        if self.connection:
            print("============================Connected to the database============================")
        else:
            print("~~~~~~~~~~~~~~~~~~~~~~~~Failed to connect to the database~~~~~~~~~~~~~~~~~~~~~~~~")
        self.cursor = self.connection.cursor()

    def getDB(self):
        return self.connection
    
    def create_table(self, query):
        '''
        Create tables in the database
        '''
        self.cursor.execute(query)
        self.connection.commit()

    def insert(self, query, data):
        '''
        Insert data into the database

        Args:
        query: SQL query
        data: data to be inserted into the database
        '''
        # try:
            # self.cursor = self.connection.cursor()
        self.cursor.execute(query, data)
        self.connection.commit()
        self.cursor.close()
        self.connection.close()


        # except psycopg2.Error as e:
        #     # Print the error message for debugging
        #     print(f"Error: {e}")
            
        #     # Rollback the transaction if any command fails
        #     self.connection.rollback()

        # finally:
        #     # Clean up and close the cursor and connection
        #     self.cursor.close()
        #     self.connection.close()
    
    def fetch(self, query):
        '''
        Fetch data from the database
        
        Args:
        query: SQL query
        '''
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def fetch_one(self, query):
        '''
        Fetch one row from the database
        
        Args:
        query: SQL query
        '''
        self.cursor.execute(query)
        return self.cursor.fetchone()
    
    def close(self):
        '''
        Close the database connection
        '''
        self.cursor.close()
        self.connection.close()

    def insert_goal_shot_creation_table(self, csv_path):

        create_temp_table_query = """
        CREATE TEMP TABLE temp_goal_shot_creation (
            league VARCHAR(100),  -- Extra columns from CSV
            season VARCHAR(10) NOT NULL,
            team VARCHAR(100) NULL,  -- Temporary column to store 'team' from CSV
            name VARCHAR(100) NULL,  -- Temporary column to store 'name' from CSV
            nation VARCHAR(50) NULL,  -- Extra columns from CSV
            pos VARCHAR(10) NULL,     -- Extra columns from CSV
            age INTEGER NULL,         -- Extra columns from CSV
            born INTEGER NULL,        -- Extra columns from CSV
            minute_90s FLOAT8 NULL,
            sca INT4 NULL,
            sca_90 FLOAT8 NULL,
            passlive_sca INT4 NULL,
            passdead_sca INT4 NULL,
            to_sca INT4 NULL,
            sh_sca INT4 NULL,
            fld_sca INT4 NULL,
            def_sca INT4 NULL,
            gca INT4 NULL,
            gca_90 FLOAT8 NULL,
            passlive_gca INT4 NULL,
            passdead_gca INT4 NULL,
            to_gca INT4 NULL,
            sh_gca INT4 NULL,
            fld_gca INT4 NULL,
            def_gca INT4 NULL
        );
        """

        try:
            self.cursor.execute(create_temp_table_query)
            print("Temporary table created successfully.")

            # Step 2: Load the CSV data into the temporary table
            csv_file_path = csv_path
            with open(csv_file_path, 'r') as f:
                self.cursor.copy_expert("COPY temp_goal_shot_creation FROM STDIN WITH CSV HEADER", f)

            # Commit the transaction
            self.connection.commit()
            print("CSV data inserted into the temporary table.")

        except psycopg2.Error as e:
            self.connection.rollback()
            print(f"Error inserting CSV data: {e}")

        # Step 3: Insert relevant data from the temporary table into the main goal_shot_creation table
        # Join with 'players' and 'clubs' to get player_id and club_id

        insert_into_main_table_query = """
        INSERT INTO goal_shot_creation (
            player_id, club_id, season, minute_90s, sca, sca_90, passlive_sca, passdead_sca,
            to_sca, sh_sca, fld_sca, def_sca, gca, gca_90, passlive_gca, passdead_gca, to_gca, sh_gca, fld_gca
        )
        SELECT 
            p.player_id, 
            c.club_id, 
            t.season, 
            t.minute_90s, 
            t.sca, 
            t.sca_90, 
            t.passlive_sca, 
            t.passdead_sca, 
            t.to_sca, 
            t.sh_sca, 
            t.fld_sca, 
            t.def_sca, 
            t.gca, 
            t.gca_90, 
            t.passlive_gca, 
            t.passdead_gca, 
            t.to_gca, 
            t.sh_gca, 
            t.fld_gca
        FROM temp_goal_shot_creation t
        JOIN players p ON t.name = p.name  -- Map 'name' in CSV to 'name' in players to get player_id
        JOIN clubs c ON t.team = c.name  -- Map 'team' in CSV to 'club_name' in clubs to get club_id;
        """

        try:
            self.cursor.execute(insert_into_main_table_query)
            self.connection.commit()
            print("Data inserted into the goal_shot_creation table successfully.")

        except psycopg2.Error as e:
            self.connection.rollback()
            print(f"Error inserting data into goal_shot_creation: {e}")

        finally:
            self.cursor.close()
            self.connection.close()


    def insert_pass_types_table(self, csv_path):

        create_temp_table_query = """
        CREATE TEMP TABLE temp_pass_types (
            league VARCHAR(100),  -- Extra columns from CSV
            season VARCHAR(10) NOT NULL,
            team VARCHAR(100) NULL,  -- Temporary column to store 'team' from CSV
            name VARCHAR(100) NULL,  -- Temporary column to store 'name' from CSV
            nation VARCHAR(50) NULL,  -- Extra columns from CSV
            pos VARCHAR(10) NULL,     -- Extra columns from CSV
            age INTEGER NULL,         -- Extra columns from CSV
            born INTEGER NULL,        -- Extra columns from CSV
            minute_90s FLOAT8 NULL,
            attempted INT4 NULL,
            live INT4 NULL,
            dead INT4 NULL,
            fk INT4 NULL,
            through_balls INT4 NULL,
            switches INT4 NULL,
            crosses INT4 NULL,
            throw_ins INT4 NULL,
            corner_kicks INT4 NULL,
            corner_kicks_in INT4 NULL,
            corner_kicks_out INT4 NULL,
            corner_kicks_straight INT4 NULL,
            passes_completed INT4 NULL,
            passes_offside INT4 NULL,
            blocked_passes INT4 NULL
        );
        """

        try:
            self.cursor.execute(create_temp_table_query)
            print("Temporary table created successfully.")

            # Step 2: Load the CSV data into the temporary table
            csv_file_path = csv_path
            with open(csv_file_path, 'r') as f:
                self.cursor.copy_expert("COPY temp_pass_types FROM STDIN WITH CSV HEADER", f)

            # Commit the transaction
            self.connection.commit()
            print("CSV data inserted into the temporary table.")

        except psycopg2.Error as e:
            self.connection.rollback()
            print(f"Error inserting CSV data: {e}")

        # Step 3: Insert relevant data from the temporary table into the main pass_types table
        # Join with 'players' and 'clubs' to get player_id and club_id

        insert_into_main_table_query = """
        INSERT INTO pass_types (
            player_id, club_id, season, minute_90s, attempted, live, dead, fk, through_balls, switches, crosses, throw_ins,
            corner_kicks, corner_kicks_in, corner_kicks_out, corner_kicks_straight, passes_completed, passes_offside, blocked_passes
            )
        SELECT
            p.player_id,
            c.club_id,
            t.season,
            t.minute_90s,
            t.attempted,
            t.live,
            t.dead,
            t.fk,
            t.through_balls,
            t.switches,
            t.crosses,
            t.throw_ins,
            t.corner_kicks,
            t.corner_kicks_in,
            t.corner_kicks_out,
            t.corner_kicks_straight,
            t.passes_completed,
            t.passes_offside,
            t.blocked_passes
        FROM temp_pass_types t
        JOIN players p ON t.name = p.name  -- Map 'name' in CSV to 'name' in players to get player_id
        JOIN clubs c ON t.team = c.name  -- Map 'team' in CSV to 'club_name' in clubs to get club_id;
        """
        try:
            self.cursor.execute(insert_into_main_table_query)
            self.connection.commit()
            print("Data inserted into the pass_types table successfully.")
        except psycopg2.Error as e:
            self.connection.rollback()
            print(f"Error inserting data into pass_types: {e}")
        finally:
            self.cursor.close()
            self.connection.close()

    def insert_defensive_actions_table(self, csv_path):
            
            create_temp_table_query = """
            CREATE TEMP TABLE temp_defensive_actions (
                league VARCHAR(100),  -- Extra columns from CSV
                season VARCHAR(10) NOT NULL,
                team VARCHAR(100) NULL,  -- Temporary column to store 'team' from CSV
                name VARCHAR(100) NULL,  -- Temporary column to store 'name' from CSV
                nation VARCHAR(50) NULL,  -- Extra columns from CSV
                pos VARCHAR(10) NULL,     -- Extra columns from CSV
                age INTEGER NULL,         -- Extra columns from CSV
                born INTEGER NULL,        -- Extra columns from CSV
                minute_90s FLOAT8 NULL,
                tackles INT4 NULL,
                tackles_won INT4 NULL,
                tackles_def_3rd INT4 NULL,
                tackles_mid_3rd INT4 NULL,
                tackles_att_3rd INT4 NULL,
                dribble_tackles INT4 NULL,
                dribbles_vs INT4 NULL,
                dribble_tackles_pct FLOAT8 NULL,
                dribbled_past INT4 NULL,
                blocks INT4 NULL,
                blocked_shots INT4 NULL,
                blocked_passes INT4 NULL,
                interceptions INT4 NULL,
                tackles_interceptions INT4 NULL,
                clearances INT4 NULL,
                errors INT4 NULL
            );
            """
    
            try:
                self.cursor.execute(create_temp_table_query)
                print("Temporary table created successfully.")
    
                # Step 2: Load the CSV data into the temporary table
                csv_file_path = csv_path
                with open(csv_file_path, 'r') as f:
                    self.cursor.copy_expert("COPY temp_defensive_actions FROM STDIN WITH CSV HEADER", f)
    
                # Commit the transaction
                self.connection.commit()
                print("CSV data inserted into the temporary table.")
    
            except psycopg2.Error as e:
                self.connection.rollback()
                print(f"Error inserting CSV data: {e}")
    
            # Step 3: Insert relevant data from the temporary table into the main defensive_actions table
            # Join with 'players' and 'clubs' to get player_id and club_id
    
            insert_into_main_table_query = """
            INSERT INTO defensive_actions (
                player_id, club_id, season, minute_90s, tackles, tackles_won, tackles_def_3rd, tackles_mid_3rd, tackles_att_3rd,
                dribble_tackles, dribbles_vs, dribble_tackles_pct, dribbled_past, blocks, blocked_shots, blocked_passes,
                interceptions, tackles_interceptions, clearances, errors
            )
            SELECT
                p.player_id,
                c.club_id,
                t.season,
                t.minute_90s,
                t.tackles,
                t.tackles_won,
                t.tackles_def_3rd,
                t.tackles_mid_3rd,
                t.tackles_att_3rd,
                t.dribble_tackles,
                t.dribbles_vs,
                t.dribble_tackles_pct,
                t.dribbled_past,
                t.blocks,
                t.blocked_shots,
                t.blocked_passes,
                t.interceptions,
                t.tackles_interceptions,
                t.clearances,
                t.errors
            FROM temp_defensive_actions t
            JOIN players p ON t.name = p.name  -- Map 'name' in CSV to 'name' in players to get player_id
            JOIN clubs c ON t.team = c.name  -- Map 'team' in CSV to 'club_name' in clubs to get club_id;
            """
            try:
                self.cursor.execute(insert_into_main_table_query)
                self.connection.commit()
                print("Data inserted into the defensive_actions table successfully.")
            except psycopg2.Error as e:
                self.connection.rollback()
                print(f"Error inserting data into defensive_actions: {e}")
            finally:
                self.cursor.close()
                self.connection.close()

    def insert_possession_table(self, csv_path):
                
        create_temp_table_query = """
        CREATE TEMP TABLE temp_possession (
            league VARCHAR(100),  -- Extra columns from CSV
            season VARCHAR(10) NOT NULL,
            team VARCHAR(100) NULL,  -- Temporary column to store 'team' from CSV
            name VARCHAR(100) NULL,  -- Temporary column to store 'name' from CSV
            nation VARCHAR(50) NULL,  -- Extra columns from CSV
            pos VARCHAR(10) NULL,     -- Extra columns from CSV
            age INTEGER NULL,         -- Extra columns from CSV
            born INTEGER NULL,        -- Extra columns from CSV
            minute_90s FLOAT8 NULL,
            touches INT4 NULL,
            touches_def_pen_area INT4 NULL,
            touches_def_3rd INT4 NULL,
            touches_mid_3rd INT4 NULL,
            touches_att_3rd INT4 NULL,
            touches_att_pen_area INT4 NULL,
            touches_live_ball INT4 NULL,
            dribbles INT4 NULL,
            dribbles_completed INT4 NULL,
            dribbles_completed_pct FLOAT8 NULL,
            tackled_during_takeon INT4 NULL,
            tacked_takeon_pct FLOAT8 NULL,
            carries INT4 NULL,
            total_carry_distance INT4 NULL,
            carry_progressive_distance INT4 NULL,
            progressive_carries INT4 NULL,
            carries_into_final_third INT4 NULL,
            carries_into_penalty_area INT4 NULL,
            missed_controls INT4 NULL,
            dispossessed INT4 NULL,
            passes_received INT4 NULL,
            progressive_passes_received INT4 NULL
        );
        """

        try:
            self.cursor.execute(create_temp_table_query)
            print("Temporary table created successfully.")

            # Step 2: Load the CSV data into the temporary table
            csv_file_path = csv_path
            with open(csv_file_path, 'r') as f:
                self.cursor.copy_expert("COPY temp_possession FROM STDIN WITH CSV HEADER", f)

            # Commit the transaction
            self.connection.commit()
            print("CSV data inserted into the temporary table.")

        except psycopg2.Error as e:
            self.connection.rollback()
            print(f"Error inserting CSV data: {e}")

        # Step 3: Insert relevant data from the temporary table into the main possession table
        # Join with 'players' and 'clubs' to get player_id and club_id

        insert_into_main_table_query = """
            INSERT INTO possession (
                player_id, club_id, season, minute_90s, touches, touches_def_pen_area, touches_def_3rd, touches_mid_3rd, touches_att_3rd,
                touches_att_pen_area, touches_live_ball, dribbles, dribbles_completed, dribbles_completed_pct, tackled_during_takeon,
                tacked_takeon_pct, carries, total_carry_distance, carry_progressive_distance, progressive_carries, carries_into_final_third,
                carries_into_penalty_area, missed_controls, dispossessed, passes_received, progressive_passes_received
            )
            SELECT
                p.player_id,
                c.club_id,
                t.season,
                t.minute_90s,
                t.touches,
                t.touches_def_pen_area,
                t.touches_def_3rd,
                t.touches_mid_3rd,
                t.touches_att_3rd,
                t.touches_att_pen_area,
                t.touches_live_ball,
                t.dribbles,
                t.dribbles_completed,
                t.dribbles_completed_pct,
                t.tackled_during_takeon,
                t.tacked_takeon_pct,
                t.carries,
                t.total_carry_distance,
                t.carry_progressive_distance,
                t.progressive_carries,
                t.carries_into_final_third,
                t.carries_into_penalty_area,
                t.missed_controls,
                t.dispossessed,
                t.passes_received,
                t.progressive_passes_received
            FROM temp_possession t
            JOIN players p ON t.name = p.name  -- Map 'name' in CSV to 'name' in players to get player_id
            JOIN clubs c ON t.team = c.name  -- Map 'team' in CSV to 'club_name' in clubs to get club_id;
            """
        try:
            self.cursor.execute(insert_into_main_table_query)
            self.connection.commit()
            print("Data inserted into the possession table successfully.")
        except psycopg2.Error as e:
            self.connection.rollback()
            print(f"Error inserting data into possession: {e}")
        finally:
            self.cursor.close()
            self.connection.close()


    def insert_shots_table(self, csv_path):
                    
            create_temp_table_query = """
            CREATE TEMP TABLE temp_shots (
                league VARCHAR(100),  -- Extra columns from CSV
                season VARCHAR(10) NOT NULL,
                team VARCHAR(100) NULL,  -- Temporary column to store 'team' from CSV
                name VARCHAR(100) NULL,  -- Temporary column to store 'name' from CSV
                nation VARCHAR(50) NULL,  -- Extra columns from CSV
                pos VARCHAR(10) NULL,     -- Extra columns from CSV
                age INTEGER NULL,         -- Extra columns from CSV
                born INTEGER NULL,        -- Extra columns from CSV
                minute_90s FLOAT8 NULL,
                goals INT4 NULL,
                shots_total INT4 NULL,
                shots_on_target INT4 NULL,
                shots_on_target_pct FLOAT8 NULL,
                shots_total_per90 FLOAT8 NULL,
                shots_on_target_per90 FLOAT8 NULL,
                goals_per_shot FLOAT8 NULL,
                goals_per_shot_on_target FLOAT8 NULL,
                avg_shot_distance FLOAT8 NULL,
                shots_free_kicks INT4 NULL,
                pens_made INT4 NULL,
                pens_att INT4 NULL,
                xg FLOAT8 NULL,
                npxg FLOAT8 NULL,
                xg_per_shot FLOAT8 NULL,
                goals_minus_xg FLOAT8 NULL,
                npg_minus_npxg FLOAT8 NULL
            );
            """
    
            try:
                self.cursor.execute(create_temp_table_query)
                print("Temporary table created successfully.")
    
                # Step 2: Load the CSV data into the temporary table
                csv_file_path = csv_path
                with open(csv_file_path, 'r') as f:
                    self.cursor.copy_expert("COPY temp_shots FROM STDIN WITH CSV HEADER", f)
    
                # Commit the transaction
                self.connection.commit()
                print("CSV data inserted into the temporary table.")
    
            except psycopg2.Error as e:
                self.connection.rollback()
                print(f"Error inserting CSV data: {e}")
    
            # Step 3: Insert relevant data from the temporary table into the main shots table
            # Join with 'players' and 'clubs' to get player_id and club_id
    
            insert_into_main_table_query = """
            INSERT INTO shots (
                player_id, club_id, season, minute_90s, goals, shots_total, shots_on_target, shots_on_target_pct, shots_total_per90,
                shots_on_target_per90, goals_per_shot, goals_per_shot_on_target, avg_shot_distance, shots_free_kicks, pens_made, pens_att,
                xg, npxg, xg_per_shot, goals_minus_xg, npg_minus_npxg
            )
            SELECT
                p.player_id,
                c.club_id,
                t.season,
                t.minute_90s,
                t.goals,
                t.shots_total,
                t.shots_on_target,
                t.shots_on_target_pct,
                t.shots_total_per90,
                t.shots_on_target_per90,
                t.goals_per_shot,
                t.goals_per_shot_on_target,
                t.avg_shot_distance,
                t.shots_free_kicks,
                t.pens_made,
                t.pens_att,
                t.xg,
                t.npxg,
                t.xg_per_shot,
                t.goals_minus_xg,
                t.npg_minus_npxg
            FROM temp_shots t
            JOIN players p ON t.name = p.name  -- Map 'name' in CSV to 'name' in players to get player_id
            JOIN clubs c ON t.team = c.name  -- Map 'team' in CSV to 'club_name' in clubs to get club_id;
            """
            try:
                self.cursor.execute(insert_into_main_table_query)
                self.connection.commit()
                print("Data inserted into the shots table successfully.")
            except psycopg2.Error as e:
                self.connection.rollback()
                print(f"Error inserting data into shots: {e}")
            finally:
                self.cursor.close()
                self.connection.close()

db = Database()


if __name__ == "__main__":


    # db.insert_goal_shot_creation_table('/Users/hayknazaryan/Desktop/School/Fall/CSC494/TekFinder/data/goal_shot_creation_copy.csv')
    # db.insert_pass_types_table('/Users/hayknazaryan/Desktop/School/Fall/CSC494/TekFinder/data/passing_types_copy.csv')
    # db.insert_defensive_actions_table('/Users/hayknazaryan/Desktop/School/Fall/CSC494/TekFinder/data/defense_copy.csv')
    # db.insert_possession_table('/Users/hayknazaryan/Desktop/School/Fall/CSC494/TekFinder/data/possession_copy.csv')
    # db.insert_shots_table('/Users/hayknazaryan/Desktop/School/Fall/CSC494/TekFinder/data/shooting_copy.csv')


    pass_types_table_query = """CREATE TABLE public.pass_types (
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
    
    goal_shot_creation_table_query = """CREATE TABLE public.goal_shot_creation (
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
                                        CONSTRAINT goal_shot_creation_pkey PRIMARY KEY (player_id, season, club_id),
                                        CONSTRAINT fk_player FOREIGN KEY (player_id) REFERENCES public.players (player_id),
                                        CONSTRAINT fk_club FOREIGN KEY (club_id) REFERENCES public.clubs (club_id)); """
    
    defensive_actions_table_query = """CREATE TABLE public.defensive_actions (
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
                                        CONSTRAINT defensive_actions_pkey PRIMARY KEY (player_id, season, club_id),
                                        CONSTRAINT fk_player FOREIGN KEY (player_id) REFERENCES public.players (player_id),
                                        CONSTRAINT fk_club FOREIGN KEY (club_id) REFERENCES public.clubs (club_id)); """
    
    possession_table_query = """CREATE TABLE public.possession (
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
                                CONSTRAINT possession_pkey PRIMARY KEY (player_id, season, club_id),
                                CONSTRAINT fk_player FOREIGN KEY (player_id) REFERENCES public.players (player_id),
                                CONSTRAINT fk_club FOREIGN KEY (club_id) REFERENCES public.clubs (club_id)); """
    
    shots_table_query = """CREATE TABLE public.shots (
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
                        goals_per_shot float8 NULL,
                        goals_per_shot_on_target float8 NULL,
                        avg_shot_distance float8 NULL,
                        shots_free_kicks int4 NULL,
                        pens_made int4 NULL,
                        pens_att int4 NULL,
                        xg float8 NULL,
                        npxg float8 NULL,
                        xg_per_shot float8 NULL,
                        goals_minus_xg float8 NULL,
                        npg_minus_npxg float8 NULL,
                        CONSTRAINT shots_pkey PRIMARY KEY (player_id, season, club_id),
                        CONSTRAINT fk_player FOREIGN KEY (player_id) REFERENCES public.players (player_id),
                        CONSTRAINT fk_club FOREIGN KEY (club_id) REFERENCES public.clubs (club_id)); """
    
    # db.create_table(pass_types_table_query)
    # db.create_table(defensive_actions_table_query)
    # db.create_table(possession_table_query)
    # db.create_table(shots_table_query)

    # fl = len(pd.read_csv('/Users/hayknazaryan/Desktop/School/Fall/CSC494/TekFinder/data/passing_types_copy.csv'))
    # print(fl)
    # print(fl)
