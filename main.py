from typing import Optional
from fastapi import FastAPI, Body
from pydantic import BaseModel


app = FastAPI()


class createPost(BaseModel):
    username: str
    title: str
    content: str
    rating: Optional[int] = None


@app.get("/")
async def root():
    return {"message": "Welcome to my World!!!"}


@app.get("/posts")
def getPost():
    return {"data":
            {"Name": "Aliu Qudus", "Age": 27, "Gender": "Male", "Country": "Nigeria"}
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


@app.post("/creates")
def createPost(post: createPost):
    print(post)
    print(post.model_dump())
    return {"data": post.model_dump(),
            "Message": "Post was successfully created"}
    # return {"Message": "Post was successfully created"}
