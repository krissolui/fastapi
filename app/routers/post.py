from typing import List
from fastapi import APIRouter, Depends, Response, status, HTTPException
from sqlalchemy.orm import Session
from app import models, oauth2
from ..database import get_db
from ..schemas import post

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("", response_model=List[post.PostResponse])
def list_posts(
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user),
    limit: int = 10,
    page: int = 1,
    search: str = "",
):
    offset = (max(1, page) - 1) * limit
    posts = (
        db.query(models.Post)
        .filter(models.Post.title.contains(search))
        .offset(offset)
        .limit(limit)
        .all()
    )
    return posts


@router.post("", status_code=status.HTTP_201_CREATED, response_model=post.PostResponse)
def create_post(
    post: post.PostCreate,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user),
):
    new_post = models.Post(**post.model_dump())
    new_post.owner_id = current_user.id
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.put("/{id}", response_model=post.PostResponse)
def update_post(
    id: int,
    updated_post: post.PostCreate,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user),
):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, f"post with id {id} does not exist"
        )

    if post.owner_id != current_user.id:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, f"Not authorized to perform requested action"
        )

    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()

    return post_query.first()


@router.get("/{id}", response_model=post.PostResponse)
def get_post(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user),
):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if post is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, f"post with id {id} does not exist"
        )

    return post


@router.delete("/{id}")
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user),
):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, f"post with id {id} does not exist"
        )

    if post.owner_id != current_user.id:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, f"Not authorized to perform requested action"
        )

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
