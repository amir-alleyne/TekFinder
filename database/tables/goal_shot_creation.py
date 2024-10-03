from sqlalchemy import Column, Integer, Float, ForeignKey, VARCHAR
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from sqlalchemy.orm import declarative_base

# Define the base class for models
Base = declarative_base()

# Define the GoalShotCreation model (mapping to your 'goal_shot_creation' table)
class GoalShotCreation(Base):
    __tablename__ = 'goal_shot_creation'

    player_id = Column(Integer, ForeignKey('players.player_id'), nullable=False, primary_key=True)
    season = Column(VARCHAR, nullable=False, primary_key=True)
    club_id = Column(Integer, ForeignKey('clubs.club_id'), primary_key=True)

    minute_90s = Column(Float)
    sca = Column(Integer)
    sca_90 = Column(Float)
    passlive_sca = Column(Integer)
    passdead_sca = Column(Integer)
    to_sca = Column(Integer)
    sh_sca = Column(Integer)
    fld_sca = Column(Integer)
    def_sca = Column(Integer)

    gca = Column(Integer)
    gca_90 = Column(Float)
    passlive_gca = Column(Integer)
    passdead_gca = Column(Integer)
    to_gca = Column(Integer)
    sh_gca = Column(Integer)
    fld_gca = Column(Integer)
    def_gca = Column(Integer)
