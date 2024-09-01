from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from app.models import Request, User
from app.schemas import RequestCreate, UserCreate
from app.utils import hash_password

# Funciones para Requests

def create_request(db: Session, request: RequestCreate) -> Request:
    """
    Crea una nueva solicitud en la base de datos.

    :param db: Sesión de base de datos.
    :param request: Datos de la solicitud a crear.
    :return: La solicitud creada.
    """
    db_request = Request(**request.dict())
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request

def get_requests(db: Session, skip: int = 0, limit: int = 10) -> list[Request]:
    """
    Obtiene una lista de solicitudes desde la base de datos.

    :param db: Sesión de base de datos.
    :param skip: Número de solicitudes a omitir.
    :param limit: Número máximo de solicitudes a devolver.
    :return: Lista de solicitudes.
    """
    return db.query(Request).offset(skip).limit(limit).all()

# Funciones para Usuarios

def create_user(db: Session, user: UserCreate) -> User:
    """
    Crea un nuevo usuario en la base de datos.

    :param db: Sesión de base de datos.
    :param user: Datos del usuario a crear.
    :return: El usuario creado.
    """
    db_user = User(email=user.email, hashed_password=hash_password(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str) -> User:
    """
    Obtiene un usuario por su correo electrónico.

    :param db: Sesión de base de datos.
    :param email: Correo electrónico del usuario.
    :return: El usuario si se encuentra, None si no se encuentra.
    """
    return db.query(User).filter(User.email == email).first()

def activate_user(db: Session, email: str) -> User:
    """
    Activa un usuario verificando su correo electrónico.

    :param db: Sesión de base de datos.
    :param email: Correo electrónico del usuario.
    :return: El usuario activado si se encuentra, None si no se encuentra.
    """
    try:
        user = db.query(User).filter(User.email == email).one()
        if user.is_verified:
            return user
        user.is_verified = True
        db.commit()
        db.refresh(user)
        return user
    except NoResultFound:
        return None
