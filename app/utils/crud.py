import json
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from utils import schemas
from utils.db import Database
from utils.models import University, New, Province, Tag, SchoolType, ScoreOfZJ, Test, Major
import copy
import math

# 查询一定数量的院校
def get_universities(db: Session, skip: int, limit: int):
    try:
        list = []
        res = db.query(University).offset(skip * limit).limit(limit).all()
        for obj in res:
            _tags = db.query(Tag.tagName).filter(University.id == SchoolType.uniId).filter(Tag.tagId == SchoolType.tagId).filter(SchoolType.uniId == obj.id).all()
            tags = []
            for tag in _tags:
                tags.append(tag.tagName)
            data = {
                "id": obj.id,
                "name": obj.name,
                "province": obj.province.name,
                "level": obj.level,
                "website": obj.website,
                "city": obj.city,
                "icon": obj.icon,
                'tags': tags
            }
            list.append(data)
        return list
    except Exception as e:
        print(e)

def get_recommend_university(db:Session, provinces, score, type):
    try:
        conditions = (ScoreOfZJ.province == province for province in provinces)
        results = db.query(ScoreOfZJ).filter(or_(*conditions), ScoreOfZJ.type == type).all()
        List = []
        for res in results:
            num = 0
            sum = 0
            avg = 0
            if (res.min1 != -1):
                num = num + 1
                sum = sum + res.min1
            if res.min2 != -1:
                num = num + 1
                sum = sum + res.min2
            if res.min3 != -1:
                num = num + 1
                sum = sum + res.min3
            avg = math.ceil(sum / num)
            if (score > avg):
                obj = {}
                obj['name'] = res.name
                obj['score'] = {
                    '2020': res.min1,
                    '2019': res.min2,
                    '2018': res.min3
                }
                obj['pc'] = res.pc
                obj['type'] = res.type
                obj['avg'] = avg
                List.append(obj)
        return List
    except Exception as e:
        print(e)

def get_all_universities(db: Session):
    try:
        return db.query(University.id).count()
    except Exception as e:
        print(e)

# 创建院校
def create_university(db: Session, id, name, level, province, city, tags, website):
    try:
        _db = Database()
        province_id = db.query(Province.id).filter(Province.name == province).first()[0]
        sql = 'insert into tb_university (id, name, level, province_id, city, website) values (%s, %s, %s, %s, %s, %s)'
        params = (id, name, level, province_id, city, website)
        _db.insert(sql, params)
        tags = json.loads(tags)
        for tag in tags:
            tagId = db.query(Tag.tagId).filter(Tag.tagName == tag).first()[0]
            sql = 'insert into tb_schoolType (tagId, uniId) values (%s, %s)'
            params = (tagId, id)
            _db.insert(sql, params)
        return {
            "code": "0",
            "message": "ok"
        }
    except Exception as e:
        return {
            "code": "1",
            "message": "e"
        }

def get_university_by_id(db: Session, id: str):
    obj = db.query(University).get(id)
    _tags = db.query(Tag.tagName).filter(University.id == SchoolType.uniId).filter(Tag.tagId == SchoolType.tagId).filter(SchoolType.uniId == id).all()
    tags = []
    for tag in _tags:
        tags.append(tag.tagName)
    data = {
        "id": obj.id,
        "name": obj.name,
        "province": obj.province.name,
        "level": obj.level,
        "website": obj.website,
        "city": obj.city,
        "icon": obj.icon,
        'tags': tags
    }
    return data

# 根据分类获取院校
def get_universities_by_type(type: str):
    try:
        db = Database()
        sql = "select tb_university.id, tb_university.name, tb_university.icon from tb_university, tb_tag, tb_schoolType where tb_university.id = tb_schoolType.uniId and tb_tag.tagId = tb_schoolType.tagId and tb_tag.tagName = %s"
        params = (type,)
        options = {
            "sql": sql,
            "type": "fetchall",
        }
        results = db.select(options, params)
        uniList = []
        for res in results:
            uni = {}
            uni['id'] = res[0]
            uni['name'] = res[1]
            uni['icon'] = res[2] if res[2] != None else '/images/yeqiangwei.png'
            uni['tags'] = []
            sql = "select  tb_tag.tagName from tb_university, tb_tag, tb_schoolType where tb_university.id = tb_schoolType.uniId and tb_tag.tagId = tb_schoolType.tagId and tb_university.name = %s"
            params = (uni['name'],)
            options = {
                "sql": sql,
                "type": "fetchall",
            }
            tags = db.select(options, params)
            for tag in tags:
                uni['tags'].append(tag[0])
            uniList.append(uni)
        return uniList
    except Exception as e:
        print(e)

def get_university_by_select(_province, _pc, _tag):
    try:
        db = Database()
        params = {}
        sql = "select tb_university.id, tb_university.name, tb_university.icon, tb_university.city, tb_university.level from tb_university, tb_tag, tb_schoolType, tb_province where tb_university.id = tb_schoolType.uniId and tb_tag.tagId = tb_schoolType.tagId and tb_university.province_id = tb_province.id"
        if _province != '地区' and _pc != '全部' and _tag != '全部':
            sql = sql + ' and tb_province.name = %(province)s'
            params['province'] = _province
            sql = sql + ' and tb_university.level = %(level)s'
            params['level'] = _pc
            sql = sql + ' and tb_tag.tagName = %(tag)s'
            params['tag'] = _tag
            print(1)
        elif _province != '地区' and _pc == '全部' and _tag == '全部':
            sql = "select tb_university.id, tb_university.name, tb_university.icon, tb_university.city, tb_university.level from tb_university, tb_province where tb_university.province_id = tb_province.id"
            sql = sql + ' and tb_province.name = %(province)s'
            params['province'] = _province
            print(2)
        elif  _province != '地区' and _pc != '全部' and _tag == '全部':
            sql = "select tb_university.id, tb_university.name, tb_university.icon, tb_university.city, tb_university.level from tb_university, tb_province where tb_university.province_id = tb_province.id"
            sql = sql + ' and tb_province.name = %(province)s'
            params['province'] = _province
            sql = sql + ' and tb_university.level = %(level)s'
            params['level'] = _pc
            print(3)
        elif _province != '地区' and _pc == '全部' and _tag != '全部':
            sql = sql + ' and tb_province.name = %(province)s'
            params['province'] = _province
            sql = sql + ' and tb_tag.tagName = %(tag)s'
            params['tag'] = _tag
            print(4)
        elif _province == '地区' and _pc == '全部' and _tag != '全部':
            sql = sql + ' and tb_university.level = %(level)s'
            params['level'] = _pc
            sql = sql + ' and tb_tag.tagName = %(tag)s'
            params['tag'] = _tag
            print(4)
        options = {
                "sql": sql,
                "type": "fetchall",
        }
        print(params)
        results = db.select(options, params)
        print(sql)
        uniList = []
        for res in results:
            uni = {}
            uni['id'] = res[0]
            uni['name'] = res[1]
            uni['icon'] = res[2] if res[2] != None else '/images/yeqiangwei.png'
            uni['province'] = res[3]
            uni['level'] = res[4]
            uniList.append(uni)
        return uniList
    except Exception as e:
        print(e)

def get_all_news(db: Session):
    try:
        return db.query(New.id).count()
    except Exception as e:
        print(e)


def get_news(db: Session, skip: int, limit: int):
    return db.query(New).offset(skip * limit).limit(limit).all()


def delete_news(db: Session, id: int):
    res = db.query(New).get(id)
    db.delete(res)
    db.commit()


def update_new(db: Session, id: int, title: str, author: str, content: str, img: str):
    res = db.query(New).get(id)
    res.title = title
    res.author = author
    res.content = content
    res.img = img
    db.commit()


def get_news_by_id(db: Session, id: int):
    return db.query(New).get(id)


def create_new(db: Session, new: schemas.New):
    try:
        db_new = New(**new.dict())
        db.add(db_new)
        db.commit()
        db.refresh(db_new)
    except Exception as e:
        print(e)
    else:
        return True


def upload_icon(db: Session, id, url):
    try:
        res = db.query(University).filter(University.id == id).update({"icon": url})
        print(res)
        db.commit()
    except Exception as e:
        print(e)

def get_questions(db: Session, type):
    try:
        list = []
        res = db.query(Test).filter(Test.type == type).all()
        for obj in res:
            data = {}
            data['id'] = obj.id
            data['question'] = obj.question
            data['options'] = {}
            if obj.A:
                data['options']['A'] = obj.A
            if obj.B:
                data['options']['B'] = obj.B
            if obj.C:
                data['options']['C'] = obj.C
            if obj.D:
                data['options']['D'] = obj.D
            list.append(data)
        return list
    except Exception as e:
        print(e)

def get_major(db):
    try:
        results = copy.deepcopy(db.query(Major).all())
        resArray = []
        tapTitle = []
        for res in results:
            if res.parent_id is None:
                list = {}
                list["id"] = res.id
                list['name'] = res.name
                list['nodes'] = []
                resArray.append(list)
                tapTitle.append({
                    "id": res.id,
                    "name": res.name
                })
            else:
                parentNode = resArray[len(resArray) - 1]
                parentNode['nodes'].append(res)
                # if (parentNode['id'] == res.parent_id):
                #     res.nodes = []
                #     parentNode['nodes'].append(res)
                # else:
                #     parentNodes = parentNode['nodes']
                #     for parentNode in parentNodes:
                #         if parentNode.id == res.parent_id:
                #             parentNode.nodes.append(res)
        # print(resArray)
        return {
            "title": tapTitle,
            "major": resArray
        }
    except Exception as e:
        print(e)

def get_major_parent_node(db):
    try:
        results = copy.deepcopy(db.query(Major).all())
        tapTitle = []
        tapTitle.append({
            "id":  '-1',
            "name": "无"
        })
        for res in results:
            if res.parent_id is None or len(res.parent_id) == 2:
                tapTitle.append({
                    "id": res.id,
                    "name": res.name
                })
        return tapTitle
    except Exception as e:
        print(e)

def get_majors(db, skip, limit):
    try:
        return db.query(Major).offset(skip * limit).limit(limit).all()
    except Exception as e:
        print(e)

def get_all_majors(db):
    return db.query(Major.id).count()

def create_major(db, _id, _name, _desc, _parentNode):
   try:
        if (_parentNode == '-1'):
            _parentNode = ''
        new_major = Major(id = _id, name = _name, desc = _desc, parent_id = _parentNode)
        db.add(new_major)
        db.commit()
        return True
   except Exception as e:
       db.rollback()
       print(e)

def update_major(db: Session, _id, _name, _desc):
    try:
        major = db.query(Major).filter(Major.id == _id).first()
        major.name = _name
        major.desc = _desc
        db.commit()
        return True
    except Exception as e:
        print(e)
        return False

def delete_major(id):
    try:
        db = Database()
        sql = 'delete from tb_major where id = %s'
        params = (id,)
        db.delete(sql, params)
        return True
    except Exception as e:
        print(e)
        return False
    
def get_admins():
    try:
        db = Database()
        sql = 'select * from tb_admin'
        options = {
            "sql": sql,
            "type": "fetchall",
        }
        results = db.select(options, None)
        list = []
        for res in results:
            data = {}
            data['username'] = res[0]
            data['password'] = res[1]
            list.append(data)
        return list
    except Exception as e:
        print(e)

def create_admin(username, password):
    try:
        sql = 'insert into tb_admin (username, password) values (%s, %s)'
        params = (username, password)
        db = Database()
        db.insert(sql, params)
        res = get_admins()
        return res
    except Exception as e:
        print(e)

def delete_admin(username):
    try:
        sql = 'delete from tb_admin where username = %s'
        params = (username,)
        db = Database()
        db.delete(sql, params)
        res = get_admins()
        return {
            "code": 0,
            "message": "ok",
            "data": res
        }
    except Exception as e:
        print(e)

def delete_admin(username):
    try:
        sql = 'delete from tb_admin where username = %s'
        params = (username,)
        db = Database()
        db.delete(sql, params)
        res = get_admins()
        return {
            "code": 0,
            "message": "ok",
            "data": res
        }
    except Exception as e:
        print(e)