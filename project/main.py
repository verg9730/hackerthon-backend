from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from . import models, schemas, database, images
from .database import engine, SessionLocal
from .images import image
from sqlalchemy.orm import Session
import os
from os import getcwd, remove
from fastapi import FastAPI, Depends, status, HTTPException, File, UploadFile, Form
from pprint import pprint
from typing import Union, List
from pydantic import BaseModel
from .S3 import upload_file, handle_upload_mp3, handle_upload_img
import shutil, random, requests
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Callable
from sqlalchemy import inspect
from pydub import AudioSegment



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
async def save_source(upload_file: UploadFile, filename:str = Form(...), db:Session = Depends(get_db)):
    try:
        suffix = Path(filename).suffix
        with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(upload_file.file, tmp)
            tmp_path = Path(tmp.name).as_posix()
            print(tmp_path)
    finally:
        upload_file.file.close()
    # 여기 아래의 upload_file.filename 고쳐도 되는지 확인 필요.
    handle_upload_mp3(str(tmp_path), filename="audio/"+filename+".m4a")

    # 아래 링크들 확인 필요
    img_link = image[random.randint(0,len(image)-1)]
    link = f"https://mymusic49848.s3.ap-northeast-2.amazonaws.com/audio/{filename}.m4a"
    new_source = models.Sources(title=filename,link=link,img_link=img_link)

    db.add(new_source)
    db.commit()
    db.refresh(new_source)
    return

@app.get('/sources')
async def all_sources(db:Session = Depends(get_db)):

    sources = db.query(models.Sources).all()
    return {"sources" : sources}

@app.post("/music")
async def save_music(upload_file: UploadFile, filename: str = Form(...), db:Session = Depends(get_db)):
    try:
        suffix = Path(upload_file.filename).suffix
        with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(upload_file.file, tmp)
            tmp_path = Path(tmp.name).as_posix()
            print(tmp_path)
    finally:
        upload_file.file.close()

    # 여기도 그냥 filename으로 받는지 확인 필요
    handle_upload_mp3(str(tmp_path), filename="audio/"+filename+".m4a")

    # 여기도 아래 링크들 확인 필요
    img_link = image[random.randint(0,len(image)-1)]
    link = f"https://mymusic49848.s3.ap-northeast-2.amazonaws.com/audio/{filename}.m4a"
    new_music = models.Musics(title=filename,link=link, img_link=img_link)

    db.add(new_music)
    db.commit()
    db.refresh(new_music)
    return

@app.get('/musics')
async def all_musics(db:Session = Depends(get_db)):
    musics = db.query(models.Musics).all()
    return {"musics": musics}


@app.post('/user', status_code=status.HTTP_201_CREATED)
async def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.Users(username=request.username)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.get('/users')
async def all_users(db:Session = Depends(get_db)):
    users = db.query(models.Users).all()
    return {'users': users}

@app.get('/edit')
async def get_record(ids : List(int), db: Session=Depends(get_db)):
    sounds = range(len(ids))
    
    for i in range(len(ids)):

        # 쿼리를 해서 url 주소를 받아 놓으면
        URL = db.query(models.Sources.link).filter(models.Sources.id == ids[i]).first()
        filename = db.query(models.Sources.title).filter(models.Sources.id == ids[i]).first()
        # 거기서 response 얻어와서 byte 값 가져옴
        response = requests.get(URL)

        # 그걸 m4a 형태로 저장해 둠
        open(f"{filename}.m4a", 'wb').write(response.content)

        # wav로 전환
        track = AudioSegment.from_file(f"{filename}.m4a", foramt='m4a')
        file = track.export(f"{filename}.wav", format='wav')

        # 다시 오디오 세그먼트로 wav 파일을 편집에 사용케 함. 
        sound = AudioSegment.from_wav(f'{filename}.wav')

        sounds[i] = sound

        # m4a 로 저장해뒀던 파일은 다시 초기화.
        remove(f"{filename}.m4a")
    
    overlapped = sounds[0].overlay(sounds[1], position=0)

    for i in range(2, len(sounds)):
        overlapped = overlapped.overlay(sounds[i], position=0)
    
    file_handle = overlapped.export('output.m4a', format="m4a")

    # wav 파일도 지워야 하는데 어떡하지
    
    return FileResponse('output.m4a')