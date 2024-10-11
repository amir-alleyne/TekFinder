from sqlalchemy import Column, Integer, Float, ForeignKey, VARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Keepers(Base):
    __tablename__ = 'keepers'

    player_id = Column(Integer, ForeignKey('players.player_id'), nullable=False, primary_key=True)
    season = Column(VARCHAR(10), nullable=False, primary_key=True)
    club_id = Column(Integer, ForeignKey('clubs.club_id'), nullable=False, primary_key=True)
    minutes = Column(Float)

    goals_against = Column(Integer)
    goals_against_per90 = Column(Float)
    shots_on_target_against = Column(Integer)
    saves = Column(Integer)
    save_pct = Column(Float)
    wins = Column(Integer)
    draws = Column(Integer)
    losses = Column(Integer)
    clean_sheets = Column(Integer)
    clean_sheets_pct = Column(Float)
    pens_att = Column(Integer)
    pens_allowed = Column(Integer)
    pens_saved = Column(Integer)
    pens_missed = Column(Integer)
    pens_saved_pct = Column(Float)