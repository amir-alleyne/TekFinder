from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
import os

import json
from database.tables.base import Base

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
