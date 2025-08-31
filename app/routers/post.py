"""
from fastapi import APIRouter, Depends, FastAPI, Body, HTTPException, status, Path
from .. import Schemas, models, Oauth
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
def createPost(
    post: Schemas.createPost,
    db: Session = Depends(get_db),
    # username: str = Depends(Oauth.getCurrentUser),
    current_user: Schemas.TokenData = Depends(Oauth.getCurrentUser),

):
    if not current_user.username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication data",
        )

    # Create the post tied to this username
    new_post = models.Post(
        username=current_user.username,
        **post.model_dump(),
    )

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
"""

from fastapi import APIRouter, Depends, FastAPI, Body, HTTPException, status, Path
from .. import Schemas, models, Oauth
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
def createPost(
    post: Schemas.createPost,
    db: Session = Depends(get_db),
    current_user: Schemas.TokenData = Depends(Oauth.getCurrentUser),
):
    if not current_user.username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication data",
        )

    # Verify that the user exists in the database
    user_exists = (
        db.query(models.Login)
        .filter(models.Login.username == current_user.username)
        .first()
    )
    if not user_exists:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User not found in database"
        )

    # Get post data and exclude username if it exists
    post_data = post.model_dump(exclude={"username"})

    # Create the post tied to the authenticated username
    new_post = models.Post(
        username=current_user.username,
        **post_data,
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# Changed to return all posts for a username (since multiple posts are allowed)
@router.get("/{username}", response_model=list[Schemas.Response])
def getPostsByUsername(
    username: str = Path(..., pattern="^[A-Za-z_ ]+$"), db: Session = Depends(get_db)
):
    posts = db.query(models.Post).filter(models.Post.username == username).all()

    if not posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No posts found for username '{username}'",
        )
    return posts


# Add endpoint to get current user's posts
@router.get("/my/posts", response_model=list[Schemas.Response])
def getMyPosts(
    db: Session = Depends(get_db),
    current_user: Schemas.TokenData = Depends(Oauth.getCurrentUser),
):
    if not current_user.username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication data",
        )

    posts = (
        db.query(models.Post)
        .filter(models.Post.username == current_user.username)
        .all()
    )

    if not posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No posts found for current user",
        )
    return posts


# Updated to work with specific post ID and add authorization
@router.delete("/{post_id}", status_code=status.HTTP_200_OK)
def deletePost(
    post_id: int = Path(...),
    db: Session = Depends(get_db),
    current_user: Schemas.TokenData = Depends(Oauth.getCurrentUser),
):
    if not current_user.username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication data",
        )

    # Find the post and ensure it belongs to the current user
    post = db.query(models.Post).filter(
        models.Post.id == post_id, models.Post.username == current_user.username
    )

    post_to_delete = post.first()
    if post_to_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No post found with ID '{post_id}' or you don't have permission to delete it",
        )

    post.delete(synchronize_session=False)
    db.commit()

    return {"message": f"Post with ID '{post_id}' has been successfully deleted"}


# Updated to work with specific post ID and add authorization
@router.put("/{post_id}", response_model=Schemas.Response)
def updatePost(
    post_id: int = Path(...),
    post: Schemas.UpdatePost = Body(...),
    db: Session = Depends(get_db),
    current_user: Schemas.TokenData = Depends(Oauth.getCurrentUser),
):
    if not current_user.username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication data",
        )

    # Find the post and ensure it belongs to the current user
    post_query = db.query(models.Post).filter(
        models.Post.id == post_id, models.Post.username == current_user.username
    )
    db_post = post_query.first()

    if db_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No post found with ID '{post_id}' or you don't have permission to update it",
        )

    # Use exclude_unset=True to only update provided fields
    post_query.update(post.model_dump(exclude_unset=True), synchronize_session=False)
    db.commit()
    db.refresh(db_post)

    return db_post
