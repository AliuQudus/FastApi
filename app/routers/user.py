"""
from ast import Or
from fastapi import Depends, APIRouter, Body, HTTPException, status, Path
from .. import Schemas, models, main, utils
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

router = APIRouter(prefix="/users", tags=["User"])


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=list[Schemas.UserResponse],
)
def users(db: Session = Depends(get_db)):

    user = db.query(models.Login).all()
    return user


@router.post(
    "", status_code=status.HTTP_201_CREATED, response_model=Schemas.UserResponse
)
def createUser(user: Schemas.Login, db: Session = Depends(get_db)):

    hashed_password = utils.pwd_context.hash(user.password)

    user.password = hashed_password

    existing_user = (
        db.query(models.Login).filter(models.Login.email == user.email).first()
    )
    if existing_user:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=jsonable_encoder(
                {"message": "Account already exists", "detail": user.email}
            ),
        )

    Or

    existing_user = (
        db.query(models.Login).filter(models.Login.username == user.username).first()
    )
    if existing_user:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=jsonable_encoder(
                {"message": "User already exists", "detail": user.username}
            ),
        )

    new_user = models.Login(**user.model_dump())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{username}", response_model=Schemas.UserResponse)
def getUser(
    username: str = Path(..., pattern="^[A-Za-z_ ]+$"), db: Session = Depends(get_db)
):  # The path restrict the input to str
    getUser = db.query(models.Login).filter(models.Login.username == username).first()

    if not getUser:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No posts found for username '{username}'",
        )
    return getUser


@router.delete("/{username}", status_code=status.HTTP_200_OK)
# The path restrict the input to str
def deleteUser(
    username: str = Path(..., pattern="^[A-Za-z_ ]+$"), db: Session = Depends(get_db)
):

    post = db.query(models.Login).filter(models.Login.username == username)

    if post.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No account found for username '{username}'",
        )

    post.delete(synchronize_session=False)

    db.commit()

    return {
        "message": f"Account by '{username}' has been successfully deleted",
        **jsonable_encoder(post),
    }
"""

from fastapi import Depends, APIRouter, HTTPException, status, Path
from .. import Schemas, models, utils, Oauth
from ..database import get_db
from sqlalchemy.orm import Session


router = APIRouter(prefix="/users", tags=["User"])


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=list[Schemas.UserResponse],
)
def users(db: Session = Depends(get_db)):
    user = db.query(models.Login).all()
    return user


@router.post(
    "", status_code=status.HTTP_201_CREATED, response_model=Schemas.UserResponse
)
def createUser(user: Schemas.Login, db: Session = Depends(get_db)):
    # Check if email already exists
    existing_email = (
        db.query(models.Login).filter(models.Login.email == user.email).first()
    )
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Account with email '{user.email}' already exists",
        )

    # Check if username already exists
    existing_username = (
        db.query(models.Login).filter(models.Login.username == user.username).first()
    )
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Username '{user.username}' already exists",
        )

    # Hash password
    hashed_password = utils.pwd_context.hash(user.password)
    user.password = hashed_password

    # Create new user
    new_user = models.Login(**user.model_dump())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{username}", response_model=Schemas.UserResponse)
def getUser(
    username: str = Path(..., pattern="^[A-Za-z_ ]+$"), db: Session = Depends(get_db)
):
    user = db.query(models.Login).filter(models.Login.username == username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No user found for username '{username}'",
        )
    return user


@router.delete("/{username}", status_code=status.HTTP_200_OK)
def deleteUser(
    username: str = Path(..., pattern="^[A-Za-z_ ]+$"),
    db: Session = Depends(get_db),
    current_user: Schemas.TokenData = Depends(Oauth.getCurrentUser),
):
    user_query = db.query(models.Login).filter(models.Login.username == username)
    user = user_query.first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No account found for username '{username}'",
        )

    if current_user.username != username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own account",
        )
    # Delete all posts by this user first (due to foreign key constraint)
    db.query(models.Post).filter(models.Post.username == username).delete(
        synchronize_session=False
    )

    # Then delete the user
    user_query.delete(synchronize_session=False)
    db.commit()

    return {
        "message": f"Account '{username}' and all associated posts have been successfully deleted"
    }
