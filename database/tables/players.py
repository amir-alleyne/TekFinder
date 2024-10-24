from sqlalchemy import Column, Integer, ForeignKey, VARCHAR
from sqlalchemy.orm import declarative_base
import sys
import os
from sqlalchemy.orm import declarative_base
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))



Base = declarative_base()

# Define the Player model (mapping to your 'players' table)
class Players(Base):
    __tablename__ = 'players'
    
    player_id = Column(Integer, primary_key=True)
    name = Column(VARCHAR)
    age = Column(Integer)
    nationality = Column(VARCHAR)
    club_id = Column(Integer, ForeignKey('clubs.club_id'))
    pos = Column(VARCHAR)
