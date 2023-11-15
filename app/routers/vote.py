from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app import oauth2
from ..database import get_db
from ..schemas import vote as vote_schemas
from ..models import post as post_models, vote as vote_models

router = APIRouter(prefix="/vote", tags=["Votes"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(
    vote: vote_schemas.Vote,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    post = (
        db.query(post_models.Post).filter(post_models.Post.id == vote.post_id).first()
    )
    if not post:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, f"Post with id: {vote.post_id} does not exist"
        )

    vote_query = db.query(vote_models.Vote).filter(
        vote_models.Vote.post_id == vote.post_id,
        vote_models.Vote.user_id == current_user.id,
    )
    found_vote = vote_query.first()

    if vote.dir == 1:
        if found_vote:
            raise HTTPException(
                status.HTTP_409_CONFLICT,
                f"user {current_user.id} has already voted on post {vote.post_id}",
            )
        new_vote = vote_models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully deleted vote"}
