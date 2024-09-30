from flask import Flask
from dotenv import load_dotenv
from rest.players import players
from rest.tables import tables
import database.db as db


# Create the app
def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.register_blueprint(players, url_prefix='/players')
    app.register_blueprint(tables, url_prefix='/tables')
    return app


app = create_app()

if __name__ == '__main__':
    print("============================Running the app============================")
    app.run(debug=True)

