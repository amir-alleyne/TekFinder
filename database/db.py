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


# db = Database()


if __name__ == "__main__":


    # db.insert_goal_shot_creation_table('/Users/hayknazaryan/Desktop/School/Fall/CSC494/TekFinder/data/goal_shot_creation_copy.csv')

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
    
    # db.create_table(goal_shot_creation_table_query)

    fl = len(pd.read_csv('/Users/hayknazaryan/Desktop/School/Fall/CSC494/TekFinder/data/passing_types.csv'))
    print(fl)
    # print(fl)
