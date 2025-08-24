from fastapi import Depends, APIRouter, Body, HTTPException, status, Path
from sqlalchemy.orm import Session

from app import Schemas, models, utils
from ..database import get_db


router = APIRouter(tags=["Authentication"])


@router.post("/login")
def login(user_details: Schemas.UserLogin, db: Session = Depends(get_db)):

    user = (
        db.query(models.Login).filter(models.Login.email == user_details.email).first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials"
        )

    if not utils.verify(user_details.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials"
        )

    return {"user": "Successful"}
