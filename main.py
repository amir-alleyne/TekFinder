import os
from app import create_app
from rest.players import players_end
from rest.tables import tables

app = create_app()
app.register_blueprint(players_end, url_prefix='/players')
app.register_blueprint(tables, url_prefix='/tables')

if __name__ == '__main__':
    print("============================Running the app============================")
    port = 4000 if os.environ.get('PORT') is None else os.environ.get('PORT')
    app.run(debug=True, port=port)
    print("============================App has stopped============================")
    

