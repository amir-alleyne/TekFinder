import json
from flask import Blueprint, jsonify, request
from database.tables.players import Players
from app import db
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import declarative_base, sessionmaker


players_end = Blueprint('players', __name__)

# GET request to retrieve players with specific attributes
@players_end.route('/', methods=['GET'])
def GetPlayers():
    """
    Takes in json input from the payload and uses the json search function to query the database
    """
   
    data = request.args.to_dict()
    results = json_search(Players, json.dumps(data))
    if not results:
        return jsonify({"error": "No players found"})
    results = [result.__dict__ for result in results]
    
    for result in results:
        result.pop('_sa_instance_state')
    return jsonify([json.loads(json.dumps(result, ensure_ascii=False)) for result in results])

  

def json_search(model, json_input):
    """Search a table with a json query. """
    filters = json.loads(json_input)

    query = db.session.query(model)
    conditions = []
    for key, value in filters.items():
        column = getattr(model, key)

        if isinstance(value, str):
            if value.startswith("<="):
                conditions.append(column <= int(value[2:]))
            elif value.startswith(">="):
                conditions.append(column >= int(value[2:]))
            elif value.startswith("<"):
                conditions.append(column < int(value[1:]))
            elif value.startswith(">"):
                conditions.append(column > int(value[1:]))
            else:
                # No operator, assume equality check
                conditions.append(column == value)
        else:
            # Handle non-string cases (e.g., integers, floats)
            conditions.append(column == value)

    query =  query.filter(and_(*conditions))

    return query.all()