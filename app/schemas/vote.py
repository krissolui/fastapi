from pydantic import BaseModel, EmailStr, conint
from datetime import datetime


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
