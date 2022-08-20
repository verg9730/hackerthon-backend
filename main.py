from typing import List
import os
from os import getcwd
from fastapi import FastAPI, Depends, status, HTTPException, File, UploadFile, Form
import models, schemas
from database import engine, SessionLocal
from sqlalchemy.orm import Session

from pprint import pprint
from typing import Union, List
from pydantic import BaseModel
from S3 import upload_file, handle_upload_mp3, handle_upload_img

app = FastAPI()

models.Base.metadata.create_all(engine)

@app.get("/")
def hello():
    return "hello"

# handle_upload_mp3("gun_sound")
# handle_upload_img("man_mask")

# @app.post('/source')
# # def upload_source(file:UploadFile, name:str):
# def upload_source(file:UploadFile):
#     # contents = file.file.read()
#     handle_upload_mp3(file)
#     return file.filename


# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# @app.get('/sources')
# def get_sources(db: Session = Depends(get_db)):
#     sources = db.query(models.Sources)
#     return 


# @app.get('/blog', response_model=List[schemas.ShowBlog])
# def all(db: Session = Depends(get_db)):
#     blogs = db.query(models.Blog).all()
#     return blogs


# @app.post('/blog', status_code=status.HTTP_201_CREATED)
# def create(request: schemas.Blog, db: Session = Depends(get_db)):
#     new_blog = models.Blog(title=request.title, body=request.body)
#     db.add(new_blog)
#     db.commit()
#     db.refresh(new_blog)

#     return new_blog


# @app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
# def destroy(id, db: Session = Depends(get_db)):
#     db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
#     db.commit()

#     return {'done'}


# @app.put('/blob/{id}', status_code=status.HTTP_202_ACCEPTED)
# def update(id, request: schemas.Blog, db: Session = Depends(get_db)):
#     blog = db.query(models.Blog).filter(models.Blog.id == id)

#     if not blog.first():
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
#             detail=f"Blog with id {id} not found")
    
#     blog.update(request.dict())
#     db.commit()

#     return 'updated'


# @app.get('/blog', response_model=List[schemas.ShowBlog])
# def all(db: Session = Depends(get_db)):
#     blogs = db.query(models.Blog).all()
#     return blogs


# @app.get('/blog/{id}', status_code=200, response_model=schemas.ShowBlog)
# def show(id, db: Session = Depends(get_db)):
#     blog = db.query(models.Blog).filter(models.Blog.id == id).first()
#     if not blog:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, 
#             detail=f"Blog with the id {id} is not available"
#         )
#         # response.status_code = status.HTTP_404_NOT_FOUND
#         # return {'detail': f"Blog with the id {id} is not available"}
#     return blog


# @app.post('/user')
# def create_user(request: schemas.User, db: Session = Depends(get_db)):
#     new_user = models.User(name=request.name, email=request.email, password=request.password)
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user

# if __name__ == "__main__":
#     import uvicorn

#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)