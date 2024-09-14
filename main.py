from flask import Flask
from dotenv import load_dotenv
from rest.players import players
import database.db as db


# Create the app
def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.register_blueprint(players, url_prefix='/players')
    return app


app = create_app()

if __name__ == '__main__':
    print("============================Running the app============================")
    app.run(debug=True)

