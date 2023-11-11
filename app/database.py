from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

load_dotenv()
db_user = os.environ.get("DB_USER")
db_password = os.environ.get("DB_PASSWORD")
host = os.environ.get("DB_HOST")
database = os.environ.get("DB_DATABASE")

# psycopg connection
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

# SQLAlchemy connection
SQLALCHEMY_DATABASE_URL = (
    f"postgresql+psycopg://{db_user}:{db_password}@{host}/{database}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
