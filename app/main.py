from ast import And, Or
from email.policy import HTTP
from fastapi import Depends, FastAPI, Body, HTTPException, status, Path
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
import time
from . import Schemas, models
from .database import engine, get_db


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


@app.get("/sqlachemy")
def sql_alchemy(db: Session = Depends(get_db)):

    return {"Status": "Successful"}


@app.get(
    "/posts",
    response_model=list[Schemas.Response],
    response_model_exclude_none=True,  # This excludes any null value in the response
)
def getPost(db: Session = Depends(get_db)):

    post = db.query(models.Post).all()
    return post


@app.post(
    "/posts", response_model=Schemas.Response, status_code=status.HTTP_201_CREATED
)
def createPost(post: Schemas.createPost, db: Session = Depends(get_db)):

    existing_user = (
        db.query(models.Post).filter(models.Post.username == post.username).first()
    )
    if existing_user:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=jsonable_encoder(
                {"message": "User already exists", "detail": post.username}
            ),
        )

    # new_post = models.Post(
    #     username=post.username,
    #     title=post.title,
    #     content=post.content,
    #     rating=post.rating,
    #     published=post.published,
    # )

    new_post = models.Post(
        **post.model_dump()
    )  # This is same as the commented code above, it only looks cleaner than the above.

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@app.get("/posts/{username}", response_model=Schemas.Response)
def getPost(
    username: str = Path(..., pattern="^[A-Za-z_ ]+$"), db: Session = Depends(get_db)
):  # The path restrict the input to str
    getpost = db.query(models.Post).filter(models.Post.username == username).first()

    if not getpost:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No posts found for username '{username}'",
        )
    return getpost


@app.delete("/posts/{username}", status_code=status.HTTP_200_OK)
# The path restrict the input to str
def deletePost(
    username: str = Path(..., pattern="^[A-Za-z_ ]+$"), db: Session = Depends(get_db)
):

    post = db.query(models.Post).filter(models.Post.username == username)

    if post.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No post found for username '{username}'",
        )

    post.delete(synchronize_session=False)

    db.commit()

    return {
        "message": f"Post by '{username}' has been successfully deleted",
        **jsonable_encoder(post),
    }


@app.put("/posts/{username}", response_model=Schemas.Response)
def updatePost(
    username: str = Path(..., regex="^[A-Za-z_ ]+$"),
    post: Schemas.UpdatePost = Body(...),
    db: Session = Depends(get_db),
):
    post_query = db.query(models.Post).filter(models.Post.username == username)
    db_post = post_query.first()

    if db_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No post found for username '{username}'",
        )

    post_query.update(post.model_dump(), synchronize_session=False)

    db.commit()
    db.refresh(db_post)

    return {
        "message": f"Post by '{username}' was successfully updated.",
        **db_post.__dict__,
    }


@app.get(
    "/users",
    status_code=status.HTTP_201_CREATED,
    response_model=list[Schemas.UserResponse],
)
def getPost(db: Session = Depends(get_db)):

    post = db.query(models.Login).all()
    return post


@app.post(
    "/users", status_code=status.HTTP_201_CREATED, response_model=Schemas.UserResponse
)
def createAccount(post: Schemas.Login, db: Session = Depends(get_db)):

    existing_user = (
        db.query(models.Login).filter(models.Login.email == post.email).first()
    )
    if existing_user:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=jsonable_encoder(
                {"message": "Account already exists", "detail": post.email}
            ),
        )

    Or

    existing_user = (
        db.query(models.Login).filter(models.Login.username == post.username).first()
    )
    if existing_user:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=jsonable_encoder(
                {"message": "User already exists", "detail": post.username}
            ),
        )

    new_user = models.Login(
        **post.model_dump()
    )  # This is same as the commented code above, it only looks cleaner than the above.

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
