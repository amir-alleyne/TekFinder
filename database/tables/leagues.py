from sqlalchemy import create_engine, Column, Integer, Float, String, ForeignKey, VARCHAR
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
import sys
import os
from sqlalchemy.orm import declarative_base

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))


Base = declarative_base()

class Leagues(Base):
    __tablename__ = 'leagues'

    league_id = Column(Integer, primary_key=True)
    name = Column(VARCHAR)
    country = Column(VARCHAR)