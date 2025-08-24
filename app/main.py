from email.policy import HTTP
from fastapi import Depends, FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import time
from . import models
from .database import engine, get_db
from .routers import post, user, auth


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


models.Base.metadata.create_all(bind=engine)


app = FastAPI()


while True:  # This is to keep the code running until it connects
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="Fastapi",
            user="postgres",
            password="quhduzski",
            cursor_factory=RealDictCursor,
        )
        cur = conn.cursor()
        print("Database connected successfully")
        break
    except Exception as error:
        print("Database connection failed")
        print("Error: ", error)
        time.sleep(5)  # The time it will wait before trying to reconnect


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/sqlachemy")
def sql_alchemy(db: Session = Depends(get_db)):

    return {"Status": "Successful"}
