from fastapi.middleware.cors import CORSMiddleware
from . import models, schemas, database, images
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
import os
from os import getcwd
from fastapi import FastAPI, Depends, status, HTTPException, File, UploadFile, Form
from pprint import pprint
from typing import Union, List
from pydantic import BaseModel
from .S3 import upload_file, handle_upload_mp3, handle_upload_img
import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Callable
from sqlalchemy import inspect


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def hello():
    return "yeah"


@app.post("/source")
def save_source(upload_file: UploadFile, db:Session = Depends(get_db)):
    try:
        suffix = Path(upload_file.filename).suffix
        with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(upload_file.file, tmp)
            tmp_path = Path(tmp.name).as_posix()
            print(tmp_path)
    finally:
        upload_file.file.close()
    handle_upload_mp3(str(tmp_path), filename="audio/"+upload_file.filename)

    img_link = "랜덤으로 이미지 1개 넣기"
    link = f"https://mymusic49848.s3.ap-northeast-2.amazonaws.com/audio/{upload_file.filename}"
    new_source = models.Sources(title=upload_file.filename,link=link,img_link=img_link)

    db.add(new_source)
    db.commit()
    db.refresh(new_source)
    return

@app.get('/sources', response_model=List[schemas.SrcBase])
def all_sources(db:Session = Depends(get_db)):

    sources = db.query(models.Sources).all()
    return sources

@app.post("/music")
def save_music(upload_file: UploadFile, db:Session = Depends(get_db)):
    try:
        suffix = Path(upload_file.filename).suffix
        with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(upload_file.file, tmp)
            tmp_path = Path(tmp.name).as_posix()
            print(tmp_path)
    finally:
        upload_file.file.close()
    handle_upload_mp3(str(tmp_path), filename="audio/"+upload_file.filename)
    img_link = "이미지 랜덤으로 2~3개 넣기"
    link = f"https://mymusic49848.s3.ap-northeast-2.amazonaws.com/audio/{upload_file.filename}"
    new_music = models.Musics(title=upload_file.filename,link=link, img_link=img_link)

    db.add(new_music)
    db.commit()
    db.refresh(new_music)
    return

@app.get('/musics', response_model=List[schemas.MusicBase])
def all_musics(db:Session = Depends(get_db)):
    musics = db.query(models.Musics).all()
    return musics


@app.post('/user', status_code=status.HTTP_201_CREATED)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.Users(profile=request.profile, username=request.username)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.get('/users', response_model=List[schemas.User])
def all_users(db:Session = Depends(get_db)):
    users = db.query(models.Users).all()
    return users


