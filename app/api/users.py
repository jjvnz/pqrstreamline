from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db
from app.auth.oauth2 import get_current_user

router = APIRouter()

@router.get("/me", response_model=schemas.UserOut)
def read_users_me(current_user: schemas.UserOut = Depends(get_current_user)):
    # El endpoint para obtener la información del usuario actual
    return current_user

@router.get("/{user_email}", response_model=schemas.UserOut)
def get_user(user_email: str, db: Session = Depends(get_db), current_user: schemas.UserOut = Depends(get_current_user)):
    # El endpoint para obtener la información de un usuario específico por email
    user = crud.get_user_by_email(db, email=user_email)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
