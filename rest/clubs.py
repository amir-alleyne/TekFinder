import json
from flask import Blueprint, jsonify, request
from database.tables.clubs import Clubs
from app import db

from flask import Blueprint, jsonify, request
import numpy as np
from app import db


clubs_end = Blueprint('clubs', __name__)


# GET request to retrieve players with specific attributes
@clubs_end.route('/', methods=['GET'])
def GetClubs():
    """
    Takes in json input from the payload and uses the json search function to query the database
    """
   
    data = request.args.to_dict()
    results = db.json_search(Clubs, json.dumps(data))
    if not results:
        return jsonify({"Error": "No Clubs Found"})
    results = [result.__dict__ for result in results] 
    for result in results:
        result.pop('_sa_instance_state')
    return jsonify([json.loads(json.dumps(result, ensure_ascii=False)) for result in results])
