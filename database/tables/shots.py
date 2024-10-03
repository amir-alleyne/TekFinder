from sqlalchemy import create_engine, Column, Integer, Float, ForeignKey, VARCHAR
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from sqlalchemy.orm import declarative_base

# Define the base class for models
Base = declarative_base()

# Define the Shot model (mapping to your 'shots' table)
class Shots(Base):
    __tablename__ = 'shots'
    
    player_id = Column(Integer, ForeignKey('players.player_id'), nullable=False, primary_key=True)
    season = Column(VARCHAR, nullable=False, primary_key=True)
    club_id = Column(Integer, ForeignKey('clubs.club_id'), primary_key=True)
    minute_90s = Column(Float)
    goals = Column(Integer)
    shots_total = Column(Integer)
    shots_on_target = Column(Integer)
    shots_on_target_pct = Column(Float)
    shots_total_per90 = Column(Float)
    shots_on_target_per90 = Column(Float)
    goals_per_shot = Column(Float)
    goals_per_shot_on_target = Column(Float)
    avg_shot_distance = Column(Float)
    shots_free_kicks = Column(Integer)
    pens_made = Column(Integer)
    pens_att = Column(Integer)
    xg = Column(Float)
    npxg = Column(Float)
    xg_per_shot = Column(Float)
    goals_minus_xg = Column(Float)
    npg_minus_npxg = Column(Float)