import os
from typing import List
from fastapi import Depends, FastAPI, Response, status, HTTPException
import psycopg
from psycopg.rows import dict_row
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, get_db
from dotenv import load_dotenv

load_dotenv()

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


user = os.environ.get("DB_USER")
password = os.environ.get("DB_PASSWORD")
host = os.environ.get("DB_HOST")
database = os.environ.get("DB_DATABASE")
while True:
    try:
        conn = psycopg.connect(
            host=host,
            dbname=database,
            user=user,
            password=password,
            row_factory=dict_row,
        )

        cursor = conn.cursor()
        print("Connected to database")
        break
    finally:
        print("Fail to connection with database")


@app.get("/")
def read_root():
    return {"Hello": "World!!"}


@app.get("/posts", response_model=List[schemas.PostResponse])
def list_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts


@app.post(
    "/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse
)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # print(post)
    # cursor.execute(
    #     """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    #     [post.title, post.content, post.published],
    # )
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.put("/posts/{id}", response_model=schemas.PostResponse)
def update_post(
    id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)
):
    # cursor.execute(
    #     """UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #     (post.title, post.content, post.published, id),
    # )
    # updated_post = cursor.fetchone()
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, f"post with id {id} does not exist"
        )

    # conn.commit()
    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()

    return post_query.first()


@app.get("/posts/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", [str(id)])
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if post is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, f"post with id {id} does not exist"
        )

    return post


@app.delete("/posts/{id}")
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", [str(id)])
    # deleted_post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, f"post with id {id} does not exist"
        )

    # conn.commit()
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
