# coding: utf8 
import json
from sqlalchemy import Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import BigInteger, String


_Base = declarative_base()


def jsonify(t):
    if t is None:
        return None
    d = {}
    for k in t.__table__.columns.keys():
        v = getattr(t, k)
        if not isinstance(v, (int, float)):
            v = '' if v is None else str(v)
        d[k] = v
    return d


class User(_Base):
    """用户表"""
    __tablename__ = 'user'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uuid = Column(String(64), default='')
    nickname = Column(String(64), default='')

