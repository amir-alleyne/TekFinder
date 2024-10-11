from sqlalchemy import Column, Integer, Float, ForeignKey, VARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class KeeperAdv(Base):
    __tablename__ = 'keeper_adv'

    player_id = Column(Integer, ForeignKey('players.player_id'), nullable=False, primary_key=True)
    season = Column(VARCHAR(10), nullable=False, primary_key=True)
    club_id = Column(Integer, ForeignKey('clubs.club_id'), nullable=False, primary_key=True)
    minute_90s = Column(Float)

    goals_against = Column(Integer)
    pk_allowed = Column(Integer)
    fk_goals_against = Column(Integer)
    ck_goals_against = Column(Integer)
    og_against = Column(Integer)
    psxg = Column(Float)
    psxg_per_shot = Column(Float)
    psxg_net = Column(Float)
    psxg_net_per90 = Column(Float)
    launched_passed_completed = Column(Integer)
    launched_passes_att = Column(Integer)
    launched_passes_completed_pct = Column(Float)
    passes_att_gk = Column(Integer)
    throws_attempted = Column(Integer)
    launch_pass_pct = Column(Float)
    avg_pass_len = Column(Float)
    goal_kicks_att = Column(Float)
    goal_kicks_launch_pct = Column(Float)
    goal_kicks_avg_len = Column(Float)
    crosses_faced = Column(Integer)
    crosses_stopped = Column(Integer)
    crosses_stopped_pct = Column(Float)
    def_act_outside_pen_area = Column(Integer)
    def_act_outside_pen_area_per90 = Column(Float)
    avg_distance_def_actions = Column(Integer)