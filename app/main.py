from fastapi import FastAPI
from .database import engine
from .routers import auth, post, user
from .models import base


base.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(auth.router)
app.include_router(user.router)
app.include_router(post.router)


@app.get("/")
def read_root():
    return {"Hello": "World!!"}
