# -*- coding: utf-8 -*-

from sqlalchemy import Column, ForeignKey
from sqlalchemy import String, Integer, Float, SmallInteger, LargeBinary
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import text

from app.model import Base
from app.config import UUID_LEN
from app.utils import alchemy


class Target(Base):
    target_id = Column(Integer, primary_key=True)
    scout_id = Column(ForeignKey("Scout.scout_id", ondelete="CASCADE"), primary_key=True)
    scout_lat = Column(Float, nullable=False)
    scout_lon = Column(Float, nullable=False)
    scout_alt = Column(Float, nullable=True)
    target_lat = Column(Float, nullable=False)
    target_lon = Column(Float, nullable=False)
    target_alt = Column(Float, nullable=True)
    target_type = Column(SmallInteger, nullable=True)
    target_desc = Column(String(100), nullable=True)

    def __repr__(self):
        return "<Target(target_id='%s', scout_id='%s', scout_lat='%s', scout_lon='%s', scout_alt='%s'," \
               " target_lat='%s', target_lon='%s', target_alt='%s', target_type='%s', target_desc='%s')>" % \
               (self.target_id, self.scout_id, self.scout_lat, self.scout_lon, self.scout_alt,
                self.target_lat, self.target_lon, self.target_alt, self.target_type, self.target_desc)

    @classmethod
    def get_id(cls):
        return Target.user_id

    @classmethod
    def find_by_last_n_minute(cls, session, last_n_minute, limit_num):
        return session.query(Target).filter(Target.modified >= text('NOW() - INTERVAL {0} MINUTES'
                                                                    .format(last_n_minute))).limit(limit_num)

    FIELDS = {
        'scout_lat': float,
        'scout_lon': float,
        'scout_alt': float,
        'target_lat': float,
        'target_lon': float,
        'target_alt': float,
        'target_type': int,
        'target_desc': str
    }

    FIELDS.update(Base.FIELDS)
