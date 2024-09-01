from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.crud import get_user_by_email
from app.database import get_db
from app.auth.jwt import verify_token
from app.schemas import UserOut

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> UserOut:
    """
    Obtiene el usuario actual basado en el token de acceso JWT.

    :param token: Token JWT proporcionado en la solicitud.
    :param db: Sesión de base de datos.
    :return: Usuario actual.
    :raises HTTPException: Si el token es inválido o el usuario no se encuentra.
    """
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

    email = payload.get("sub")
    if not email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")

    user = get_user_by_email(db, email=email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return user
