from sqlalchemy import (
    TIMESTAMP,
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    text,
)
from sqlalchemy.orm import relationship
from .database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, nullable=False, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, nullable=False, server_default="TRUE")
    created_at = Column(TIMESTAMP(True), nullable=False, server_default=text("now()"))
    owner_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )

    owner = relationship("User")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(True), nullable=False, server_default=text("now()"))
