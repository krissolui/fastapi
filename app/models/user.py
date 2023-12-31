from sqlalchemy import (
    TIMESTAMP,
    Column,
    Integer,
    String,
    text,
)
from .base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(True), nullable=False, server_default=text("now()"))
