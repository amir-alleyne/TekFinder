import math
from flask import Blueprint, jsonify
import psycopg2
from database.db import db
import pandas as pd
import pprint

def read_data(filename):
    data = pd.read_csv(filename)
    return data



players = Blueprint('players', __name__)

# Get all players at /players
@players.route('/')
def index():
    data = read_data("data/standard.csv")
    # data[1].sort_values('Unnamed: 1', ascending=False, inplace=True)    
    names = {}
    for row in data.iloc[2:].iterrows():
        league = row[1]['Unnamed: 0'].split("-")[1]
        name = row[1]['Unnamed: 3']
        season = row[1]['Unnamed: 1']
       
        age = row[1]['age'] if math.isnan(row[1]['age']) == False else 0
        nationality = row[1]['nation']  
        team = row[1]['Unnamed: 2']
        if name not in names and league != "INT" and season == "2324":
            names[name] = set(name)
            print("Season: ", season)
            print("Name: ", name)
            print("Age: ", age)
            print("=====================================")
            db.insert("INSERT INTO players (club_id, name, age, nationality) VALUES ((SELECT club_id from clubs where clubs.name = %s), %s, %s, %s) ON CONFLICT DO NOTHING", (team, name, age, nationality))
        # print(row[1])
        # if league not in teams and len(team) > 1 and country != "INT":
        #     teams[league] = set(team)
        # elif len(team) > 2 and country != "INT":
        #     teams[league].add(team)

    # for league in teams:
    #     for team in teams[league]:
    #         try:
    #             db.insert("INSERT INTO soccer_players (club_id, name, age, nationality) VALUES ((SELECT club_id from clubs where clubs.name = %s), %s) ON CONFLICT DO NOTHING", (team, name, age, nationality))
    #         except psycopg2.Error as e:
    #             print(f"Database error: {e}")
    #             continue
            # db.insert("INSERT INTO clubs (league_id, name) VALUES ((SELECT league_id from leagues where name = %s), %s) ON CONFLICT DO NOTHING", (league, team))
        # db.insert("INSERT INTO soccer_players (name, age,
    # db.insert("INSERT INTO clubs (league_id, name) VALUES ((SELECT league_id from leagues where name = %s), %s) ON CONFLICT DO NOTHING", (league, team))
        # db.insert("INSERT INTO soccer_players (name, age,
    # results = db.fetch("SELECT * FROM soccer_players")
   
    
    return jsonify("Done")


# insert leagues
# @players.route('/')
def index():
    data = read_data("data/standard.csv")
    teams = {}
    for row in data.iloc[2:].iterrows():
        league = row[1]['Unnamed: 0'].split("-")[1]
        country = row[1]['Unnamed: 0'].split("-")[0]    
        team = row[1]['Unnamed: 2']
        if league not in teams and len(team) > 1 and country != "INT":
            teams[league] = set(team)
        elif len(team) > 2 and country != "INT":
            teams[league].add(team)

    for league in teams:
        for team in teams[league]:
            try:
                db.insert("INSERT INTO clubs (league_id, name) VALUES ((SELECT league_id from leagues where leagues.name = %s), %s) ON CONFLICT DO NOTHING", (league, team))
            except psycopg2.Error as e:
                print(f"Database error: {e}")
                continue
            # db.insert("INSERT INTO clubs (league_id, name) VALUES ((SELECT league_id from leagues where name = %s), %s) ON CONFLICT DO NOTHING", (league, team))
        # db.insert("INSERT INTO soccer_players (name, age,
    # db.insert("INSERT INTO clubs (league_id, name) VALUES ((SELECT league_id from leagues where name = %s), %s) ON CONFLICT DO NOTHING", (league, team))
        # db.insert("INSERT INTO soccer_players (name, age,
    # results = db.fetch("SELECT * FROM soccer_players")
   
    
    return jsonify("Done")

# @players.route('/')
def index(): # insert 
    data = read_data("data/standard.csv")
    leagues = set(data.iloc[2:]['Unnamed: 0'])
    for league in leagues:
        country, league = league.split("-")
        if country != "INT":
            db.insert("INSERT INTO leagues (name, country) VALUES (%s, %s)", (league, country))
    if not leagues:
        return jsonify({"error": "No players found"})
    
    return jsonify(league)