from sqlalchemy import Column, Integer, Float, ForeignKey, VARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Misc(Base):
    __tablename__ = 'misc'

    player_id = Column(Integer, ForeignKey('players.player_id'), nullable=False, primary_key=True)
    season = Column(VARCHAR(10), nullable=False, primary_key=True)
    club_id = Column(Integer, ForeignKey('clubs.club_id'), nullable=False, primary_key=True)
    minute_90s = Column(Float)

    yellow = Column(Integer)
    red = Column(Integer)
    second_yellow = Column(Integer)
    fouls_commit = Column(Integer)
    fouls_drawn = Column(Integer)
    offside = Column(Integer)
    crosses = Column(Integer)
    interceptions = Column(Integer)
    tackles_won = Column(Integer)
    pens_won = Column(Integer)
    pens_conceded = Column(Integer)
    own_goals = Column(Integer)
    ball_recoveries = Column(Integer)
    aerials_won = Column(Integer)
    aerials_lost = Column(Integer)
    aerials_won_pct = Column(Float)