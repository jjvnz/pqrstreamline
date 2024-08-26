from asyncpg.pgproto.pgproto import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import crud
from app import schemas
from app.auth.jwt import create_access_token
from app.auth.jwt import verify_token
from app.dependencies import get_db
from app.email.email_service import send_verification_email
from app.utils import verify_password, CredentialsException

router = APIRouter()


@router.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = crud.get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    new_user = crud.create_user(db, user)
    verification_token = create_access_token(data={"sub": new_user.email}, expires_delta=timedelta(days=1))
    verification_link = f"http://localhost:8080/auth/verify/{verification_token}"
    send_verification_email(new_user.email, verification_link)

    return {"message": "User registered, please check your email to verify your account"}



@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, form_data.username)

    if not user:
        raise CredentialsException(detail="Invalid credentials")

    if not verify_password(form_data.password, user.hashed_password):
        raise CredentialsException(detail="Invalid credentials")

    if not user.is_verified:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Email not verified")

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/verify/{token}")
def verify_email(token: str, db: Session = Depends(get_db)):
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired token")

    email = payload.get("sub")
    user = crud.activate_user(db, email=email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"message": "Email verified successfully"}
