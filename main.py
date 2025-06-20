from typing import Optional
from uuid import uuid4
from fastapi import FastAPI, Body, HTTPException
from httpx import post
from pydantic import BaseModel


app = FastAPI()


class createPost(BaseModel):
    username: str
    title: str
    content: str
    rating: Optional[int] = None


dummy_posts = [{"username": "ScamHunter", "title": "Learning API", "content": "Hey guys, I am new to this and I am just started my journey as a BackEnd dev."},
               {"username": "Diablo", "title": "Strongest Necromancer",
                "content": "One of the best anime I have listened to on pocket fm", "rating": 8},
               {"username": "Anonymous", "title": "Donghua", "content": "The best donghua you can watch and enjoy every bit of it is definitely Battle Through the Heavens.", "rating": 9}]


def findPost(username):
    for post in dummy_posts:
        if post['username'] == "username":
            return post


@app.get("/")
async def root():
    return {"message": "Hello guys, Welcome to my World!!!"}


@app.get("/posts")
def getPost():
    return {"data": dummy_posts
            # {"Name": "Aliu Qudus", "Age": 27, "Gender": "Male", "Country": "Nigeria"}
            }


'''
@app.post("/create")
def createPost(post: dict = Body(...)):
    print(post)
    return {
        # "content": {
        #     "title": "Introduction",
        #     "content": "Hello, world! This is my first social media post. I hope you will follow me for more of my contents.",
        #     "user_id": "qudusaliu@gmail.com"
        # },
        "Message": "Post Successfully Created"
    }
'''


@app.post("/posts")
def createPost(post: createPost):

    for existing_post in dummy_posts:
        if existing_post["username"] == post.username:
            # if existing_post["title"] == post.title and existing_post["content"] == post.content:
            raise HTTPException(
                status_code=400, detail="Post with this username already exists")

    # model_dump() replaces dict() in the latest version.
    post_dict = post.model_dump()
    # post_dict["id"] = str(uuid4())  # This is to generate an automatic id
    dummy_posts.append(post_dict)
    return {"data": post_dict}


@app.get("/posts/{username}")
def getPost(username: str):
    posts = [post for post in dummy_posts if post["username"] == username]

    if not posts:
        raise HTTPException(
            status_code=404,
            detail=f"No posts found for username '{username}'"
        )

    return {"data": posts}
