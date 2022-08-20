from ssl import create_default_context
from typing import Union, List
import datetime
from pydantic import BaseModel


class MusicBase(BaseModel):
    title: str
    maker: int

    class Config:
        orm_mode=True

class MusicCreate(MusicBase):

    link: str
    length: int
    used_sources: list[int]

    created_at : datetime.datetime

    class Config:
        orm_mode=True


class MusicReview(MusicBase):

    likes: int
    plays: int
    class Config:
        orm_mode=True




class SrcBase(BaseModel):
    title: str
    player: int

    class Config:
        orm_mode=True


class SrcCreate(SrcBase):

    link: str
    length: int
    created_at : datetime.datetime

    class Config:
        orm_mode=True


class SrcReview(SrcBase):

    inst: str
    
    class Config:
        orm_mode=True


class User(BaseModel):
    username: str

    class Config:
        orm_mode=True