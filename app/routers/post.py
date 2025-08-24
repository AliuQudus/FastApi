from fastapi import APIRouter, Depends, FastAPI, Body, HTTPException, status, Path
from .. import Schemas, models
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

router = APIRouter(prefix="/posts", tags=["Post"])


@router.get(
    "",
    response_model=list[Schemas.Response],
    response_model_exclude_none=True,  # This excludes any null value in the response
)
def getPost(db: Session = Depends(get_db)):

    post = db.query(models.Post).all()
    return post


@router.post("", response_model=Schemas.Response, status_code=status.HTTP_201_CREATED)
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


@router.get("/{username}", response_model=Schemas.Response)
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


@router.delete("/{username}", status_code=status.HTTP_200_OK)
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


@router.put("/{username}", response_model=Schemas.Response)
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
