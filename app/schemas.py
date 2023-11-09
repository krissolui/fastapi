from pydantic import BaseModel
from datetime import datetime


# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool = True


# class CreatePost(BaseModel):
#     title: str
#     content: str
#     published: bool = True


# class UpdatePost(BaseModel):
#     title: str
#     content: str
#     published: bool


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class PostResponse(PostBase):
    id: int
    created_at: datetime
