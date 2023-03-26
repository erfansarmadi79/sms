# -*- coding: utf-8 -*-

from sqlalchemy import Column
from sqlalchemy import String, Integer, BigInteger
from sqlalchemy.dialects.postgresql import JSONB

from app.model import Base
from app.config import UUID_LEN
from app.utils import alchemy


class Scout(Base):
    scout_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(20), nullable=True)
    last_name = Column(String(20), nullable=True)
    phone_number = Column(BigInteger, unique=True, nullable=True)
    username = Column(String(20), nullable=False)
    password = Column(String(20), nullable=False)

    def __repr__(self):
        return "<Scout(first_name='%s', last_name='%s', phone_number='%s', username='%s')>" % \
            (self.first_name, self.last_name, self.phone_number, self.username)

    @classmethod
    def get_id(cls):
        return Scout.scout_id

    @classmethod
    def find_by_phone_number(cls, session, phone_number):
        return session.query(Scout).filter(Scout.phone_number == phone_number).one()

    @classmethod
    def find_by_username(cls, session, username):
        return session.query(Scout).filter(Scout.username == username).one()

    FIELDS = {
        'first_name': str,
        'last_name': str,
        'phone_number': str,
        'username': str,
        'password': str
    }

    FIELDS.update(Base.FIELDS)
