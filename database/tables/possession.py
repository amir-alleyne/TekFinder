from sqlalchemy import Column, Integer, Float, ForeignKey, VARCHAR
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from sqlalchemy.orm import declarative_base

# Define the base class for models
Base = declarative_base()

class Possession(Base):
    __tablename__ = 'possession'

    player_id = Column(Integer, ForeignKey('players.player_id'), nullable=False, primary_key=True)
    season = Column(VARCHAR, nullable=False, primary_key=True)
    club_id = Column(Integer, ForeignKey('clubs.club_id'), primary_key=True)

    minute_90s = Column(Float)
    touches = Column(Integer)
    touches_def_pen_area = Column(Integer)
    touches_def_3rd = Column(Integer)
    touches_mid_3rd = Column(Integer)
    touches_att_3rd = Column(Integer)
    touches_att_pen_area = Column(Integer)
    touches_live_ball = Column(Integer)
    dribbles = Column(Integer)
    dribbles_completed = Column(Integer)
    dribbles_completed_pct = Column(Float)
    tackled_during_takeon = Column(Integer)
    carries = Column(Integer)
    total_carry_distance = Column(Integer)
    progressive_carries = Column(Integer)
    carries_into_final_third = Column(Integer)
    carries_into_penalty_area = Column(Integer)
    missed_controls = Column(Integer)
    dispossessed = Column(Integer)
    passes_received = Column(Integer)
    progressive_passes_received = Column(Integer)