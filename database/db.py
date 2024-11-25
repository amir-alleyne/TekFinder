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
