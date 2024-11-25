from dotenv import load_dotenv
from flask import Flask

from database.alchemydb import Database
db = Database()

def create_app():
    load_dotenv()
    app = Flask(__name__)
   
    return app

