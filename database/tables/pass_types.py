from sqlalchemy import Column, Integer, Float, ForeignKey, VARCHAR
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from sqlalchemy.orm import declarative_base

# Define the base class for models
Base = declarative_base()

# Define the PassTypes model (mapping to your 'pass_types' table)
class PassTypes(Base):
    __tablename__ = 'pass_types'

    player_id = Column(Integer, ForeignKey('players.player_id'), nullable=False, primary_key=True)
    season = Column(VARCHAR, nullable=False, primary_key=True)
    club_id = Column(Integer, ForeignKey('clubs.club_id'), primary_key=True)

    minute_90s = Column(Float)
    attempted = Column(Integer)
    live = Column(Integer)
    dead = Column(Integer)
    fk = Column(Integer)
    through_balls = Column(Integer)
    switches = Column(Integer)
    crosses = Column(Integer)
    throw_ins = Column(Integer)
    corner_kicks = Column(Integer)
    corner_kicks_in = Column(Integer)
    corner_kicks_out = Column(Integer)
    corner_kicks_straight = Column(Integer)
    passes_completed = Column(Integer)
    passes_offside = Column(Integer)
    blocked_passes = Column(Integer)