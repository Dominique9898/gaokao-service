from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from utils._database import SessionLocal
from utils import crud


router = APIRouter(
    prefix="/api",
    tags=["user"],
    responses={404: {"description": "Not found /user"}},
)

def get_db():
    _db = SessionLocal()
    try:
        yield _db
    finally:
        _db.close()

@router.post("/login")
async def login(username: str, password: str, db: Session = Depends(get_db)):
    try:
        res = crud.login(db, username, password)
        return res
    except Exception as e:
        return {
            "code": 1,
            "message": e
        }

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