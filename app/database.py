from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import psycopg
from psycopg.rows import dict_row
from .config import config
from .models import post, user, vote

# psycopg connection
while True:
    try:
        conn = psycopg.connect(
            host=config.DB_HOST,
            dbname=config.DB_DATABASE,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            row_factory=dict_row,
        )

        cursor = conn.cursor()
        print("Connected to database")
        break
    except:
        print("Fail to connection with database")

# SQLAlchemy connection
SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}/{config.DB_DATABASE}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
