from typing import Optional
from uuid import uuid4
from fastapi import FastAPI, Body, HTTPException, status, Path
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time


app = FastAPI()


class createPost(BaseModel):
    username: str
    title: str
    content: str
    ratings: Optional[float] = None


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


class UpdatePost(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    ratings: Optional[float] = None


@app.get("/")
async def root():
    return {"message": "Hello guys, Welcome to my World!!!"}


@app.get("/posts")
def getPost():
    cur.execute("""SELECT * FROM posts""")
    posts = cur.fetchall()
    # print(posts)
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def createPost(post: createPost):
    # 1️⃣ Check if post already exists
    cur.execute("SELECT * FROM posts WHERE username = %s", (post.username,))
    existing_user = cur.fetchone()

    if existing_user:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=jsonable_encoder(
                {"message": "User already exists", "username": existing_user}
            ),
        )
    # 2️⃣ If not, insert the new user
    cur.execute(
        """INSERT INTO posts (username, title, content, ratings)
VALUES(%s, %s, %s, %s) RETURNING * 
""",
        (post.username, post.title, post.content, post.ratings),
    )
    Post = cur.fetchone()
    conn.commit()

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=jsonable_encoder(
            {"message": "User created successfully", "data": Post}
        ),
    )


@app.get("/posts/{username}")
def getPost(
    username: str = Path(..., pattern="^[A-Za-z_ ]+$")
):  # The path restrict the input to str
    cur.execute("SELECT * FROM posts WHERE username = %s", (username,))
    post = cur.fetchone()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No posts found for username '{username}'",
        )
    return {"details": post}


@app.delete("/posts/{username}", status_code=status.HTTP_200_OK)
# The path restrict the input to str
def deletePost(username: str = Path(..., pattern="^[A-Za-z_ ]+$")):
    cur.execute("DELETE FROM posts WHERE username= %s RETURNING *", (username,))
    post = cur.fetchone()
    conn.commit()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No post found for username '{username}'",
        )
    return {
        "message": f"Post by '{username}' has been successfully deleted",
        "data": post,
    }


@app.put("/posts/{username}")
def updatePost(
    username: str = Path(..., pattern="^[A-Za-z_ ]+$"),
    post: UpdatePost = Body(...),
):
    # Update and check if any rows were affected
    cur.execute(
        "UPDATE posts SET title = %s, content = %s, ratings = %s WHERE username = %s RETURNING *",
        (
            post.title,
            post.content,
            post.ratings,
            username,
        ),  # Always pass in the username field if you want to upadate a specific record otherwise all the record will be updated.
    )

    new_post = cur.fetchone()
    conn.commit()

    if new_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No post found for username '{username}'",
        )

    return {
        "message": f"Post by '{username}' was successfully updated.",
        "data": new_post,
    }
