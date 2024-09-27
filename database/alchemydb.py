from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
import os

import json
from database.tables.base import Base
from tables.shots import Shots

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
        Base.metadata.bind = self.engine
        Base.metadata.create_all(self.engine)

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

    def query(self, *models):
        """Query one or more tables (models)."""
        with self.get_session() as session:
            return session.query(*models)
        
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






# db = Database()

# db = Database()

if __name__ == "__main__":

    # Initialize the Database using the .env file
    # db = Database()

    # players = (
    #     db.query(Passing, Players.name)
    #     .join(Players, Passing.player_id == Players.player_id)
    #     .all()
    # )

    # for player, name in players:
    #     if player.player_id == 343:
    #         print(player.player_id, player.season, player.club_id, player.assists, name)

    
    # offense = db.query(GoalShotCreation)
    # for off in offense:
    #     if off.player_id == 343:
    #         print(off.player_id, off.season, off.club_id, off.gca, off.sca)

    # pass_types = db.query(PassTypes)
    # for pass_type in pass_types:
    #     if pass_type.player_id == 343:
    #         print(pass_type.player_id, pass_type.season, pass_type.club_id, pass_type.live, pass_type.dead)

    # defensive_actions = db.query(DefensiveActions)
    # for def_act in defensive_actions:
    #     if def_act.player_id == 343:
    #         print(def_act.player_id, def_act.season, def_act.club_id, def_act.tackles, def_act.interceptions)

    # possession = db.query(Possession)
    # for poss in possession:
    #     if poss.player_id == 343:
    #         print(poss.player_id, poss.season, poss.club_id, poss.touches, poss.touches_def_pen_area)

    # new_json = {
    #     "age": "<27",
    #     "club_id": "5"
    # }

    # results = db.json_search(Players, json.dumps(new_json))

    # for result in results:
    #     print(result.name)
    
    # print(results)

    # Close the session
    # db.close()

    pass