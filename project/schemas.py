from ssl import create_default_context
from typing import Union, List
import datetime
from pydantic import BaseModel


class MusicBase(BaseModel):

    link: str
    title: str
    created_at : datetime.datetime
    img_link : list[str]
    likes:int
    class Config:
        orm_mode=True    
class SrcBase(BaseModel):
    
    link: str
    title: str
    created_at: datetime.datetime
    img_link : str
    likes:int
    class Config:
        orm_mode=True    

class User(BaseModel):
    username: str
    profile: str

    class Config:
        orm_mode=True