from fastapi import FastAPI, Body

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to my World!!!"}


@app.get("/post")
def getPost():
    return {"data":
            {"Name": "Aliu Qudus", "Age": 27, "Gender": "Male", "Country": "Nigeria"}
            }


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
