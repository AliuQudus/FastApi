from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to my World!!!"}


@app.get("/post")
def getPost():
    return {"data":
            {"Name": "Aliu Qudus", "Age": 27, "Gender": "Male", "Country": "Nigeria"}
            }
