from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from . import models
from .database import engine, get_db
from .routers import post, user, auth, like


models.Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(like.router)


@app.get("/sqlachemy")
def sql_alchemy(db: Session = Depends(get_db)):

    return {"Status": "Successful"}
