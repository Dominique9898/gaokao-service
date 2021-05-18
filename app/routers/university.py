from tempfile import NamedTemporaryFile
from typing import List
import shutil
import json
from fastapi import APIRouter, Depends, File, UploadFile, Form
from sqlalchemy.orm import Session
from utils._database import SessionLocal
from utils import crud, schemas
import os

images_saveDir = '/usr/share/nginx/www/static/images'
_db = None

router = APIRouter(
    prefix="/api",
    tags=["university"],
    responses={404: {"description": "Not found /user"}},
)


def get_db():
    _db = SessionLocal()
    try:
        yield _db
    finally:
        _db.close()

@router.post("/createuniversity")
async def create_university(id: str, 
                     name: str, 
                     level: str, 
                     province: str, 
                     city: str, 
                     tags: str,
                     website: str,db: Session = Depends(get_db)):
    try:
        crud.create_university(db,id, name, level, province, city, tags, website)
        return {
            'code': 0,
            'message': 'ok',
        }
    except Exception as e:
        return {
            "code": 1,
            "message": e
        }

@router.get("/getUniversitiesbytype")
async def get_universities_by_type(type: str):
    try:
        res = crud.get_universities_by_type(type)
    except:
        return {
            "code": 1,
            "message": "error",
        }
    else:
        return {
            "code": 0,
            "message": "ok",
            "data": res
        } 

@router.get('/getuniversitybyid')
async def get_university_by_id(id: str, db: Session = Depends(get_db)):
    try:
        res = crud.get_university_by_id(db, id)
        return {
            "code": 0,
            "data": res,
        }
    except Exception as e:
        return {
            "code": 1,
            "message": e,
        }

@router.get("/getrecommenduniversity")
async def get_recommend_university(provinces: str, score: int, type:str, db: Session = Depends(get_db)):
    try:
        provinces = json.loads(provinces)
        res = crud.get_recommend_university(db, provinces, score, type)
        return {
            "code": 0,
            "data": res,
        }
    except Exception as e:
        return {
            "code": 1,
            "message": e,
        }
    # for index, province in enumerate(provinces):
    #     print(index, province)
    #     if index != len(provinces) - 1:
    #         provinceQuery += 'province = ' + province + ' or '
    #     else:
    #         provinceQuery += 'province = ' + province
    # print(provinceQuery)
    # sql = 'select * from tb_score_zhejiang where ' + provinceQuery
    # print(sql)


@router.get("/getUniversitiesbyselect")
async def get_university_by_select(province: str, pc: str, tag: str):
    try:
        res = crud.get_university_by_select(province, pc, tag)
    except Exception as e:
        return {
            "code": 1,
            "message": e,
        }
    else:
        return {
            "code": 0,
            "message": "ok",
            "data": res
        }  

@router.get("/getlistUniversity")
async def get20University(page:int, limit:int, db: Session = Depends(get_db), total=None):
    try:
        res = crud.get_universities(db, page - 1, limit)
        if not total:
            total = crud.get_all_universities(db)
        return {
            "code": 0,
            "message": "ok",
            "data": {
                "total": total,
                "list": res
            }
        }
    except Exception as e:
        return {
            "code": 1,
            "message": e,
        }


@router.post("/uploadicon/{item_id}")
async def uploadIcon(item_id, file:UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        filename = file.filename
        save_dir = f"{images_saveDir}/university"
        with open(f"{save_dir}/{filename}", "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        url = '/images/university/'+filename
        crud.upload_icon(db, item_id, url)
        return {
            "code": 0,
            "message":'ok',
            "data": {
                "url": url
            }
        }
    except Exception as e:
        return {
            "code": 1,
            "message": e
        }
