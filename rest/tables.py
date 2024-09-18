import math
from flask import Blueprint, jsonify
import psycopg2
from database.db import db
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
    db.cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
    tables = db.cursor.fetchall()
    return jsonify(tables)



if __name__ == "__main__":

    from pathlib import Path

    fl = read_data("/Users/hayknazaryan/Desktop/School/Fall/CSC494/TekFinder/data/passing_types.csv")

    count = 0
    for row in fl.iloc[2:].iterrows():
        print(row[1][3])
        count += 1

    print(f"Total count: {count} \n")


        