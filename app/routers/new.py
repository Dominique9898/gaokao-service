import shutil
from fastapi import APIRouter, Depends, File, UploadFile, Form
from sqlalchemy.orm import Session
from utils._database import SessionLocal
from utils import crud, schemas

images_saveDir = '/usr/share/nginx/www/static/images'

router = APIRouter(
    prefix="/api",
    tags=["news"],
    responses={404: {"description": "Not found /news"}},
)


def get_db():
    _db = SessionLocal()
    try:
        yield _db
    finally:
        _db.close()


@router.post('/updatenews')
async def update_new(*, id: int = Form(...), title: str = Form(...), author: str = Form(...), content: str = Form(...),
                     file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        filename = file.filename
        save_dir = f"{images_saveDir}/news"
        with open(f"{save_dir}/{filename}", "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        url = '/images/news/' + filename
        crud.update_new(db, id, title, author, content, url)
        return {
            "code": 0,
            "message": 'ok'
        }
    except Exception as e:
        return {
            "code": 1,
            "message": e
        }


@router.post("/deletenews")
async def delete_news(id: int, db: Session = Depends(get_db)):
    try:
        print(id)
        crud.delete_news(db, id)
        return {
            "code": 0,
            "message": 'ok'
        }
    except Exception as e:
        return {
            "code": 1,
            "message": e
        }


@router.post("/uploadnews")
async def upload_new(*, title: str = Form(...), author: str = Form(...), content: str = Form(...),
                     file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        filename = file.filename
        save_dir = f"{images_saveDir}/news"
        with open(f"{save_dir}/{filename}", "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        url = '/images/news/' + filename
        crud.create_new(db, schemas.New(title=title, author=author, content=content, img=url))
        return {
            'code': 0,
            'message': 'ok',
            "data": {
                'file': file
            }
        }
    except Exception as e:
        return {
            "code": 1,
            "message": e
        }


@router.get("/getnewsbyid")
async def get_news_by_id(id: int, db: Session = Depends(get_db)):
    try:
        print(id)
        res = crud.get_news_by_id(db, id)
        return {
            "code": 0,
            "message": 'ok',
            "data": res,
        }
    except Exception as e:
        return {
            "code": 1,
            "message": e,
        }


@router.get("/getnewslist")
async def get20newslist(page: int, limit: int, db: Session = Depends(get_db), total=None):
    try:
        res = crud.get_news(db, page - 1, limit)
        if not total:
            total = crud.get_all_news(db)

    except Exception as e:
        return {
            "code": 1,
            "message": e,
        }
    else:
        return {
            "code": 0,
            "message": "ok",
            "data": {
                "total": total,
                "list": res
            }
        }
