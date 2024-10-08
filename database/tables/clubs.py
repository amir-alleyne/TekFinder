from sqlalchemy import create_engine, Column, Integer, Float, String, ForeignKey, VARCHAR
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Clubs(Base):
    __tablename__ = 'clubs'

    club_id = Column(Integer, primary_key=True)
    league_id = Column(Integer, ForeignKey('leagues.league_id'))
    name = Column(VARCHAR)