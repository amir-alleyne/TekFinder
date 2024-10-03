from sqlalchemy import create_engine, Column, Integer, Float, ForeignKey, VARCHAR
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from sqlalchemy.orm import declarative_base


# Define the base class for models
Base = declarative_base()

# Define the Passing model (mapping to your 'passing' table)
class Passing(Base):
    __tablename__ = 'passing'

    player_id = Column(Integer, ForeignKey('players.player_id'), nullable=False, primary_key=True)
    season = Column(VARCHAR, nullable=False, primary_key=True)
    club_id = Column(Integer, ForeignKey('clubs.club_id'), primary_key=True)
    minute_90s = Column(Float)

    completed_passes = Column(Integer)
    attempted_passes = Column(Integer)
    completed_percent = Column(Float)
    tot_dist = Column(Integer)
    progressive_pass_dist = Column(Integer)
    short_completed = Column(Integer)
    short_attempted = Column(Integer)
    short_completed_percent = Column(Float)
    medium_completed = Column(Integer)
    medium_attempted = Column(Integer)
    medium_completed_percent = Column(Float)
    long_completed = Column(Integer)
    long_attempted = Column(Integer)
    long_completed_percent = Column(Float)
    assists = Column(Integer)
    expected_assisted_goals = Column(Float)
    expected_assists = Column(Float)
    assists_minus_expected_goals_assisted = Column(Float)
    key_passes = Column(Integer)
    final_third_passes = Column(Integer)
    passes_into_pen_area = Column(Integer)
    crosses_into_pen_area = Column(Integer)
    progressive_passes = Column(Integer)



    

