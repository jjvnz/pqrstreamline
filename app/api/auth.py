import secrets

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.auth.jwt import create_access_token
from app import crud, schemas
from app.config import settings
from app.email.email_service import send_verification_email
from app.database import get_db

router = APIRouter()

@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db=db, username=form_data.username)
    if not user or not crud.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email not verified",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db=db, username=user.username)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")

    verification_token = secrets.token_urlsafe(32)
    db_user = crud.create_user(db=db, user=user, verification_token=verification_token)

    verification_link = f"{settings.base_url}/auth/verify?email={user.email}&token={verification_token}&mode=signup"
    send_verification_email(email=user.email, token=verification_token)

    return {"message": "User created, please check your email to verify your account"}

@router.get("/verify")
def verify_email(email: str, token: str, mode: str, db: Session = Depends(get_db)):
    if mode != 'signup':
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid mode")

    user = crud.verify_user_email(db=db, token=token)
    if user:
        return {"message": "Email verified successfully"}
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired token")
