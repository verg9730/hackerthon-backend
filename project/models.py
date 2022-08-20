import datetime
from email.policy import default
from xmlrpc.client import DateTime
from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship
import random
from .database import Base
from typing import List

class Sources(Base):
    
    __tablename__ = 'sources'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    link = Column(String)  
    img_link = Column(String)
    likes = Column(Integer, default=random.randrange(10,3000))   
    created_at = Column(DateTime, default=datetime.datetime.utcnow)       

class Musics(Base):
    
    __tablename__ = 'musics'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    link = Column(String)    
    img_link = list[String]
    likes = Column(Integer, default=random.randrange(10,3000))  
    created_at = Column(DateTime, default=datetime.datetime.utcnow)     

class Users(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    profile = Column(String)
    username = Column(String)
