from fastapi.middleware.cors import CORSMiddleware
from . import models, schemas, database
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
def save_upload_file_tmp(upload_file: UploadFile):
    try:
        suffix = Path(upload_file.filename).suffix
        with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(upload_file.file, tmp)
            tmp_path = Path(tmp.name).as_posix()
            print(tmp_path)
    finally:
        upload_file.file.close()
    handle_upload_mp3(str(tmp_path), filename="audio/"+upload_file.filename)

    return


# main에서 source와 music을 좋아요 순으로 리스트 보냄.
# @app.get("/main")
# def all_lists():


@app.get('/musics', response_model=List[schemas.MusicBase])
def all_musics(db:Session = Depends(get_db)):
    musics = db.query(models.Musics).all()
    return musics


@app.post('/music')
def create_music(request: schemas.MusicBase, db: Session = Depends(get_db)):
    new_music = models.Musics(title=request.title, link=request.link, created_at=request.created_at)
    db.add(new_music)
    db.commit()
    db.refresh(new_music)
    return 


# source 생성
# source schema 추가, models.Sources 에 들어가야 하는 속성 추가해야 함.
@app.post('/src')
def create_source(request: schemas.SrcBase, db: Session = Depends(get_db)):
    new_source = models.Sources(title=request.title, link=request.link, created_at=request.created_at)
    db.add(new_source)
    db.commit()
    return db.refresh(new_source)


@app.get('/srcs', response_model=List[schemas.SrcBase])
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

@app.get('/users', response_model=List[schemas.User])
def all_users(db:Session = Depends(get_db)):
    users = db.query(models.Users).all()
    return users


