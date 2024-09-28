from sqlalchemy import create_engine, and_
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from tables.shots import Shots
from tables.players import Players
import json


# Database class to manage connections and sessions
class Database:
    def __init__(self):
        """Initialize the database connection and session using environment variables."""
        # Load the environment variables
        user = os.getenv('POSTGRES_USER')
        password = os.getenv('POSTGRES_PASSWORD')
        host = os.getenv('POSTGRES_HOST')
        port = os.getenv('POSTGRES_PORT')
        db_name = os.getenv('POSTGRES_DB')

        # Construct the database URL
        db_url = f'postgresql://{user}:{password}@{host}:{port}/{db_name}'

        # Create an engine that connects to the PostgreSQL AWS instance
        self.engine = create_engine(db_url, future=True)
        # Create a session factory (bind engine later on session instantiation)
        self.SessionLocal = sessionmaker(bind=self.engine, future=True)

    def get_session(self):
        """Create a new session."""
        return self.SessionLocal()

    def add(self, instance):
        """Add a single instance to the session."""
        with self.get_session() as session:
            session.add(instance)
            session.commit()

    def add_all(self, instances):
        """Add multiple instances to the session."""
        with self.get_session() as session:
            session.add_all(instances)
            session.commit()

    def query(self, model):
        """Query a table (model)."""
        with self.get_session() as session:
            return session.query(model)
        
    def json_search(self, model, json_input):
        """Search a table with a json query. """
        with self.get_session() as session:
            filters = json.loads(json_input)

            query = session.query(model)
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


    def delete(self, instance):
        """Delete an instance."""
        with self.get_session() as session:
            session.delete(instance)
            session.commit()

    def update(self):
        """Commit changes to the session."""
        with self.get_session() as session:
            session.commit()

    def close(self):
        """Close the session."""
        with self.get_session() as session:
            session.close()


if __name__ == "__main__":

    # Initialize the Database using the .env file
    db = Database()

    # # Query players
    # players = db.query(Shots).all()
    # for player in players:
    #     if player.player_id == 343:
    #         print(player.season)

    new_json = {
        "age": "<27",
        "club_id": "5"
    }

    results = db.json_search(Players, json.dumps(new_json))

    for result in results:
        print(result.name)
    
    # print(results)

    # Close the session
    db.close()