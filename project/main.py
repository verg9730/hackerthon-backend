from typing import List

from fastapi import FastAPI, Depends, status, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from . import models, schemas, database
from .database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# main에서 source와 music을 좋아요 순으로 리스트 보냄.
# @app.get("/main")
# def all_lists():


@app.get('/musics', response_model=List[schemas.MusicReview])
def all_musics(db:Session = Depends(get_db)):
    musics = db.query(models.Musics).all()
    return musics


@app.post('/music')
def create_music(request: schemas.MusicCreate, db: Session = Depends(get_db)):
    new_music = models.Musics(title=request.title, maker=request.maker, link=request.link, created_at=request.created_at, length=request.length)
    db.add(new_music)
    db.commit
    db.refresh(new_music)
    return 


# source 생성
# source schema 추가, models.Sources 에 들어가야 하는 속성 추가해야 함.
@app.post('/source')
def create_source(request: schemas.SrcReview, db: Session = Depends(get_db)):
    new_source = models.Sources()
    db.add(new_source)
    db.commit
    return db.refresh(new_source)


@app.get('/sources', response_model=List[schemas.SrcReview])
def all_sources(db:Session = Depends(get_db)):
    sources = db.query(models.Sources).all()
    return sources


@app.post('/user', status_code=status.HTTP_201_CREATED)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.Users(username=request.username)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
