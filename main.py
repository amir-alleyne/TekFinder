from app import create_app
from rest.players import players_end
from rest.tables import tables

app = create_app()
app.register_blueprint(players_end, url_prefix='/players')
app.register_blueprint(tables, url_prefix='/tables')

if __name__ == '__main__':
    print("============================Running the app============================")
    app.run(debug=True)
    print("============================App has stopped============================")
    

