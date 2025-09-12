from fastapi import APIRouter, Depends, FastAPI, Body, HTTPException, status, Path
from .. import Schemas, database, models, Oauth
from sqlalchemy.orm import Session


router = APIRouter(prefix="/like", tags=["Likes"])


@router.get("", status_code=status.HTTP_200_OK)
def likes(db: Session = Depends(database.get_db)):
    user = db.query(models.Like).all()
    return user


@router.post("", status_code=status.HTTP_200_OK)
def likePost(
    vote: Schemas.Likes,
    db: Session = Depends(database.get_db),
    current_user: Schemas.TokenData = Depends(Oauth.getCurrentUser),
):

    query = db.query(models.Like).filter(
        models.Like.post_id == vote.post_id,
        models.Like.user_username == current_user.username,
    )
    liked = query.first()

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id '{vote.post_id}' does not exist",
        )

    if vote.dir == 1:
        if liked:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User '{current_user.username} already like this post '{vote.post_id}'",
            )

        new_vote = models.Like(
            post_id=vote.post_id, user_username=current_user.username
        )
        db.add(new_vote)
        db.commit()

        return {"message": "You liked a post"}

    else:
        if not liked:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"You haven't liked this post yet",
            )

        query.delete(synchronize_session=False)
        db.commit()

        return {"message": "You successfully unliked this post"}


# Add endpoint to get current user's likes
@router.get("/my/likes")
def getMylikess(
    db: Session = Depends(database.get_db),
    current_user: Schemas.TokenData = Depends(Oauth.getCurrentUser),
):

    posts = (
        db.query(models.Like)
        .filter(models.Like.user_username == current_user.username)
        .all()
    )

    if not posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No likes found for current user",
        )

    return posts


@router.get("/{username}")
def getlikesByUsername(
    username: str = Path(..., pattern="^[A-Za-z_ ]+$"),
    db: Session = Depends(database.get_db),
):

    post = db.query(models.Login).filter(models.Login.username == username).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User '{username}' does not exist",
        )

    likes = db.query(models.Like).filter(models.Like.user_username == username).all()

    if not likes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No post liked by user '{username}'",
        )

    return likes
