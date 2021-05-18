from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from utils._database import SessionLocal
from utils import crud, schemas


router = APIRouter(
    prefix="/api",
    tags=["major"],
    responses={404: {"description": "Not found /major"}},
)


def get_db():
    _db = SessionLocal()
    try:
        yield _db
    finally:
        _db.close()

@router.post("/createmajor")
async def creat_major(id: str, name: str, desc: str, parentNode: str, db: Session = Depends(get_db)):
    try:
        res = crud.create_major(db, id, name, desc, parentNode)
        if (res == True):
            return {
                "code": 0,
                "message": 'ok',
                "data": res
            }
        else:
            return {
            "code": 1,
            "message": res,
        }
    except Exception as e:
        return {
            "code": 1,
            "message": e,
        }

@router.post("/updatemajor")
async def update_major(id: str, name: str, desc: str, db: Session = Depends(get_db)):
    try:
        res = crud.update_major(db, id, name, desc)
        if (res == True):
            return {
                "code": 0,
                "message": 'ok',
                "data": res
            }
        else:
            return {
            "code": 1,
            "message": res,
        }
    except Exception as e:
        return {
            "code": 1,
            "message": e,
        }

@router.post("/deletemajor")
async def update_major(id: str):
    try:
        res = crud.delete_major(id)
        if (res == True):
            return {
                "code": 0,
                "message": 'ok',
                "data": res
            }
        else:
            return {
            "code": 1,
            "message": 'error',
        }
    except Exception as e:
        return {
            "code": 1,
            "message": e,
        }

@router.get("/getmajor")
async def get_major(db: Session = Depends(get_db)):
    try:
        res = crud.get_major(db)
        return {
            "code": 0,
            "data": res
        }
    except Exception as e:
        return {
            "code": 1,
            "message": e,
        }

@router.get("/getmajorparentnode")
async def get_major_parent_node(db: Session = Depends(get_db)):
    try:
        res = crud.get_major_parent_node(db)
        return {
            "code": 0,
            "data": res,
        }
    except Exception as e:
        return {
            "code": 1,
            "message": e,
        }

@router.get("/getmajors")
async def get_majors(page:int, limit:int, db: Session = Depends(get_db), total=None):
    try:
        res = crud.get_majors(db, page - 1, limit)
        if not total:
            total = crud.get_all_majors(db)
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



