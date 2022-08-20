import datetime
from email.policy import default
from xmlrpc.client import DateTime
from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship

from .database import Base


association_table = Table(
    "association",
    Base.metadata,
    Column("musics_id", Integer, ForeignKey("musics.id"), primary_key=True),
    Column("sources_id", Integer, ForeignKey("sources.id"), primary_key=True),
)

class Musics(Base):
    
    __tablename__ = 'musics'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    maker = Column(Integer, ForeignKey("users.id"))    # 제작자
    link = Column(String)     # url
    likes = Column(Integer)    # 좋아요 수
    plays = Column(Integer)    # 재생 수
    length = Column(Integer)   # 길이
    used_sources = relationship("Sources",viewonly=True, secondary=association_table, uselist=True, lazy='noload')     # 사용한 소스
    created_at = Column(DateTime, default=datetime.datetime.utcnow)     # 생성된 시간


class Sources(Base):
    
    __tablename__ = 'sources'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    player = Column(Integer, ForeignKey("users.id"))   # 연주자
    link = Column(String)     # url
    inst = Column(String)     # 악기
    length = Column(Integer)   # 길이 단위는 second
    created_at = Column(DateTime, default=datetime.datetime.utcnow)       # 생성된 시간
    used_to = relationship('Musics', secondary=association_table, lazy='noload')

class Users(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
