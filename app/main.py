import os
from fastapi import FastAPI
import psycopg
from psycopg.rows import dict_row
from . import models
from .database import engine
from dotenv import load_dotenv
from .routers import post, user

load_dotenv()

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


db_user = os.environ.get("DB_USER")
db_password = os.environ.get("DB_PASSWORD")
host = os.environ.get("DB_HOST")
database = os.environ.get("DB_DATABASE")

while True:
    try:
        conn = psycopg.connect(
            host=host,
            dbname=database,
            user=db_user,
            password=db_password,
            row_factory=dict_row,
        )

        cursor = conn.cursor()
        print("Connected to database")
        break
    finally:
        print("Fail to connection with database")

app.include_router(post.router)
app.include_router(user.router)


@app.get("/")
def read_root():
    return {"Hello": "World!!"}
