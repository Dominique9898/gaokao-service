from tempfile import NamedTemporaryFile
from typing import List
import shutil
import os
from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session
from utils._database import SessionLocal
from utils import crud, schemas
import os

_db = None

router = APIRouter(
    prefix="/api",
    tags=["test"],
    responses={404: {"description": "Not found /user"}},
)


def get_db():
    _db = SessionLocal()
    try:
        yield _db
    finally:
        _db.close()

@router.get("/getQuestions")
async def get_questions(type: str, db: Session = Depends(get_db)):
    try:
        res = crud.get_questions(db, type)
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