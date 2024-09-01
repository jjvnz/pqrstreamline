from datetime import datetime, timedelta, timezone
from typing import Optional, Dict
from jose import JWTError, jwt
from app.config import settings

def create_access_token(data: Dict[str, str], expires_delta: Optional[timedelta] = None) -> str:
    """
    Crea un token de acceso JWT.

    :param data: Datos que se incluirán en el payload del token.
    :param expires_delta: Tiempo de expiración adicional para el token.
    :return: Token JWT codificado como cadena.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.access_token_expire_minutes))
    to_encode.update({"exp": int(expire.timestamp())})  # Mantener el timestamp como entero
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)

def verify_token(token: str) -> Optional[Dict[str, str]]:
    """
    Verifica y decodifica un token JWT.

    :param token: Token JWT a verificar.
    :return: Payload decodificado si es válido, None si no lo es.
    """
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return payload
    except JWTError as e:
        # Log the error with a proper logging framework
        print(f"JWT verification failed: {e}")
        return None
