from operator import index
from typing import Optional
from uuid import uuid4
from fastapi import FastAPI, Body, HTTPException, status, Path
from pydantic import BaseModel


app = FastAPI()


class createPost(BaseModel):
    username: str
    title: str
    content: str
    rating: Optional[int] = None


class UpdatePost(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    rating: Optional[int] = None


dummy_posts = [
    {
        "username": "ScamHunter",
        "title": "Learning API",
        "content": "Hey guys, I am new to this and I am just started my journey as a BackEnd dev.",
    },
    {
        "username": "Diablo",
        "title": "Strongest Necromancer",
        "content": "One of the best anime I have listened to on pocket fm",
        "rating": 8,
    },
    {
        "username": "Anonymous",
        "title": "Donghua",
        "content": "The best donghua you can watch and enjoy every bit of it is definitely Battle Through the Heavens.",
        "rating": 9,
    },
]


def findPost(username):
    for post in dummy_posts:
        if post["username"] == username:
            return post


@app.get("/")
async def root():
    return {"message": "Hello guys, Welcome to my World!!!"}


@app.get("/posts")
def getPost():
    return {"data": dummy_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def createPost(post: createPost):

    for existing_post in dummy_posts:
        if existing_post["username"] == post.username:
            # if existing_post["title"] == post.title and existing_post["content"] == post.content:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Post with this username already exists",
            )

    # model_dump() replaces dict() in the latest version.
    post_dict = post.model_dump()
    # post_dict["id"] = str(uuid4())  # This is to generate an automatic id
    dummy_posts.append(post_dict)
    return {"data": post_dict}


@app.get("/posts/{username}")
# The path restrict the input to str
def getPost(username: str = Path(..., pattern="^[A-Za-z_]+$")):
    posts = [post for post in dummy_posts if post["username"] == username]

    if not posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No posts found for username '{username}'",
        )

    return {"data": posts}


@app.delete("/posts/{username}", status_code=status.HTTP_410_GONE)
# The path restrict the input to str
def deletePost(username: str = Path(..., pattern="^[A-Za-z_]+$")):
    for i, post in enumerate(dummy_posts):
        if post["username"] == username:
            dummy_posts.pop(i)
            return {"message": f"Post by '{username}' has been successfully deleted"}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No post found for username '{username}'",
    )


@app.put("/posts/{username}")
def updatePost(
    username: str = Path(..., pattern="^[A-Za-z_]+$"),
    updated_data: UpdatePost = Body(...),  # ✅ Marked explicitly as body input
):
    for i, post in enumerate(dummy_posts):
        if post["username"] == username:
            # Only update fields that are provided
            if updated_data.title is not None:
                post["title"] = updated_data.title
            if updated_data.content is not None:
                post["content"] = updated_data.content
            if updated_data.rating is not None:
                post["rating"] = updated_data.rating

            dummy_posts[i] = post
            return {
                "message": f"Post by '{username}' was successfully updated.",
                "data": post,
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No post found for username '{username}'",
    )
