from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db
from app.auth.oauth2 import get_current_user

router = APIRouter()

@router.get("/me", response_model=schemas.UserInDB)
def read_users_me(current_user: schemas.UserInDB = Depends(get_current_user)):
    return current_user

@router.get("/{user_email}", response_model=schemas.UserInDB)
def get_user(user_email: str, db: Session = Depends(get_db), current_user: schemas.UserInDB = Depends(get_current_user)):
    if current_user.email != user_email:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this user's information")

    user = crud.get_user_by_email(db, email=user_email)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
