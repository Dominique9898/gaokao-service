from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from cryptography.fernet import Fernet
from utils.WXBizDataCrypy import WXBizDataCrypt
from utils import crud


router = APIRouter(
    prefix="/api",
    tags=["user"],
    responses={404: {"description": "Not found /user"}},
)

@router.get("/getadmins")
async def get_admins():
    try:
        res = crud.get_admins()
        return {
            'code': 0,
            'data': res,
        }
    except Exception as e:
        return {
            "code": 1,
            "message": e
        }

@router.post("/createadmin")
async def create_admin(username: str, password: str):
    try:
        res = crud.create_admin(username, password)
        print(res)
        if (res):
            return {
            'code': 0,
            "message": 'ok',
            'data': res
            }
        else:
            return {
            "code": 1,
            "message": '增加失败'
        }
    except Exception as e:
        return {
            "code": 1,
            "message": e
        }

@router.post("/deleteadmin")
async def delete_admin(username):
    try:
        res = crud.delete_admin(username)
        return res
    except Exception as e:
        return {
            "code": 1,
            "message": e
        }