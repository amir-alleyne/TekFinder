import os
from app import create_app
from rest.players import players_end
from rest.clubs import clubs_end
from rest.leagues import leagues_end
from rest.tables import tables

app = create_app()
app.register_blueprint(players_end, url_prefix='/players')
app.register_blueprint(clubs_end, url_prefix='/clubs')
app.register_blueprint(leagues_end, url_prefix='/leagues')
app.register_blueprint(tables, url_prefix='/tables')

if __name__ == '__main__':
    print("============================Running the app============================")
    port = 4000
    app.run(debug=True, port=port)
    print("============================App has stopped============================")
    

