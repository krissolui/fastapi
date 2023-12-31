from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app import utils
from ..database import get_db
from ..schemas import user
from ..models import user as user_models

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=user.UserResponse)
def create_user(user: user.UserCreate, db: Session = Depends(get_db)):
    # hash the password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = user_models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", response_model=user.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(user_models.User).filter(user_models.User.id == id).first()

    if user is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, f"User with id: {id} does not exits"
        )

    return user
