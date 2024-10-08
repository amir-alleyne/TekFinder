from sqlalchemy import Column, Integer, Float, ForeignKey, VARCHAR
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from sqlalchemy.orm import declarative_base

# Define the base class for models
Base = declarative_base()

# Define the DefensiveActions model (mapping to your 'defensive_actions' table)
class DefensiveActions(Base):
    __tablename__ = 'defensive_actions'

    player_id = Column(Integer, ForeignKey('players.player_id'), nullable=False, primary_key=True)
    season = Column(VARCHAR, nullable=False, primary_key=True)
    club_id = Column(Integer, ForeignKey('clubs.club_id'), primary_key=True)

    minute_90s = Column(Float)
    tackles = Column(Integer)
    tackles_won = Column(Integer)
    tackles_def_3rd = Column(Integer)
    tackles_mid_3rd = Column(Integer)
    tackles_att_3rd = Column(Integer)
    dribble_tackles = Column(Integer)
    dribbles_vs = Column(Integer)
    dribble_tackles_pct = Column(Float)
    dribbled_past = Column(Integer)
    blocks = Column(Integer)
    blocked_shots = Column(Integer)
    blocked_passes = Column(Integer)
    interceptions = Column(Integer)
    tackles_interceptions = Column(Integer)
    clearances = Column(Integer)
    errors = Column(Integer)
