from flask import Blueprint, jsonify
from database.db import db

players = Blueprint('players', __name__)

# Get all players at /players
@players.route('/')
def index():
    results = db.fetch("SELECT * FROM soccer_players")
    if not results:
        return jsonify({"error": "No players found"})
    
    return jsonify(results)