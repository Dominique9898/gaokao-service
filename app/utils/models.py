# models.py
from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy.sql.expression import false
from sqlalchemy.types import DateTime

from sqlalchemy.orm import relationship, backref

from utils._database import Base

class University(Base):
    __tablename__ = 'tb_university'  # 数据表的表名

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False, comment='院校名称')
    province_id = Column(String, ForeignKey("tb_province.id"))
    level = Column(String, nullable=True, comment='办学类型')
    website = Column(String, nullable=True, comment='学校官网')
    city = Column(String, nullable=True, comment='城市')
    icon = Column(String, nullable=True, comment='校徽')

    province = relationship('Province', backref="universities")


class New(Base):
    __tablename__ = 'tb_news'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    content = Column(String, nullable=False)
    img = Column(String, nullable=False)
    create_time = Column(DateTime)

class Province(Base):
    __tablename__ = 'tb_province'

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False, comment='省/直辖市')
    pinyin = Column(String)

    # universities = relationship('University', backref="province")
    # def __repr__(self):
    #     return self.name

class Tag(Base):
    __tablename__ = 'tb_tag'

    tagId = Column(Integer, primary_key=True)
    tagName = Column(String, nullable=False)

class SchoolType(Base):
     __tablename__ = 'tb_schoolType'

     id = Column(Integer, primary_key=True)
     tagId = Column(Integer, ForeignKey("tb_tag.tagId"))
     uniId = Column(String, ForeignKey("tb_university.id"))



class Test(Base):
    __tablename__ = 'tb_test'

    id = Column(Integer, primary_key=True)
    question = Column(String, nullable=False)
    A = Column(String)
    B = Column(String)
    C = Column(String)
    D = Column(String)
    type = Column(String, nullable=False) 

class Major(Base):
    __tablename__ = 'tb_major'

    id = Column(String, primary_key=True)
    name = Column(String)
    parent_id = Column(String)
    desc = Column(Text)

class ScoreOfZJ(Base):
    __tablename__ = 'tb_score_zhejiang'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    province = Column(String)
    type = Column(String)
    min1 = Column(Integer)
    min2 = Column(Integer)
    min3 = Column(Integer)
    pc = Column(Integer)

""" 附上三个SQLAlchemy教程

SQLAlchemy的基本操作大全 
    http://www.taodudu.cc/news/show-175725.html

Python3+SQLAlchemy+Sqlite3实现ORM教程 
    https://www.cnblogs.com/jiangxiaobo/p/12350561.html

SQLAlchemy基础知识 Autoflush和Autocommit
    https://zhuanlan.zhihu.com/p/48994990
"""
