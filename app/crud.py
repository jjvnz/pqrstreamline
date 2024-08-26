# app/crud.py
from sqlalchemy.orm import Session
from app.models import Request, User
from app.schemas import RequestCreate, UserCreate
from app.utils import hash_password

# Funciones para Requests

def create_request(db: Session, request: RequestCreate):
    db_request = Request(**request.dict())
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request

def get_requests(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Request).offset(skip).limit(limit).all()

# Funciones para Usuarios

def create_user(db: Session, user: UserCreate):
    db_user = User(email=user.email, hashed_password=hash_password(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def activate_user(db: Session, email: str):
    user = db.query(User).filter(User.email == email).first()
    if user:
        user.is_verified = True
        db.commit()
        db.refresh(user)
    return user
