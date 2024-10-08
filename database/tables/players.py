from sqlalchemy import create_engine, Column, Integer, Float, String, ForeignKey, VARCHAR
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from tables.base import Base


# Define the Player model (mapping to your 'players' table)
class Players(Base):
    __tablename__ = 'players'
    
    player_id = Column(Integer, primary_key=True)
    name = Column(VARCHAR)
    age = Column(Integer)
    nationality = Column(VARCHAR)
    club_id = Column(Integer, ForeignKey('clubs.club_id'))

Players.shots = relationship('Shots', back_populates='players')
