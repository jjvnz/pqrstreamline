from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import crud, schemas
from app.auth.jwt import create_access_token, verify_token
from app.config import settings
from app.database import get_db
from app.email.email_service import send_verification_email
from app.utils import hash_password, verify_password, validate_password, validate_email, CredentialsException
from datetime import timedelta
from urllib.parse import urlencode

router = APIRouter()


@router.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Validaciones de entrada
    validate_email(user.email)
    validate_password(user.password)

    # Verifica si el correo electrónico ya está registrado
    existing_user = crud.get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    # Hash de la contraseña antes de guardarla
    hashed_password = hash_password(user.password)
    user_data = schemas.UserCreate(email=user.email, password=hashed_password)

    # Crea el nuevo usuario
    new_user = crud.create_user(db, user_data)

    # Genera y envía el token de verificación
    verification_token = create_access_token(data={"sub": new_user.email}, expires_delta=timedelta(days=1))
    verification_link = f"{settings.base_url}/auth/verify?{urlencode({'email': new_user.email, 'token': verification_token, 'mode': 'signup'})}"
    send_verification_email(new_user.email, verification_token)

    return {"message": "User registered, please check your email to verify your account"}


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, form_data.username)

    # Verifica credenciales
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise CredentialsException(detail="Invalid credentials")

    # Verifica si el correo electrónico está verificado
    if not user.is_verified:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Email not verified")

    # Genera el token de acceso
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/verify")
def verify_email(email: str = Query(...), token: str = Query(...), mode: str = Query(...),
                 db: Session = Depends(get_db)):
    # Verifica el token
    payload = verify_token(token)

    if not payload:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired token")

    # Verifica la dirección de correo electrónico
    if payload.get("sub") != email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token does not match the provided email")

    # Obtén el usuario desde la base de datos
    user = crud.get_user_by_email(db, email=email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Verifica si el usuario ya está verificado
    if user.is_verified:
        return {
            "message": "Your email address has already been verified. If you need further assistance, please contact support."}

    # Activa al usuario
    try:
        user = crud.activate_user(db, email=email)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found or already activated")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="An error occurred while verifying your email. Please try again later.")

    return {"message": "Email successfully verified. You can now log in to your account."}