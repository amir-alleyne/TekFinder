from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
db = SQLAlchemy()

# Create the app
def create_app():
    load_dotenv()
    app = Flask(__name__)
    user = os.getenv('POSTGRES_USER')
    password = os.getenv('POSTGRES_PASSWORD')
    host = os.getenv('POSTGRES_HOST')
    port = os.getenv('POSTGRES_PORT')
    db_name = os.getenv('POSTGRES_DB')

    # Construct the database URL
    db_url = f'postgresql://{user}:{password}@{host}:{port}/{db_name}'

    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    
    db.init_app(app)
   
    

    return app

