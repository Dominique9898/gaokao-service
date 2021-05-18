from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel


# BaseModle

class University(BaseModel):
    id: str
    name: str
    province_id: str
    level: str
    website: str
    city: str
    
    class Config:
        orm_mode = True


class Province(BaseModel):
    id: str
    name: str
    pinyin: str

    class Config:
        orm_mode = True


class New(BaseModel):
    id: Optional[int] = None
    title: str
    author: str
    content: str
    img: str
    # create_time: Optional[datetime] = None

    class Config:
        orm_mode = True


class listQuery(BaseModel):
    page: int
    limit: int
