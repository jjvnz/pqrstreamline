from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db
from app.auth.oauth2 import get_current_user

router = APIRouter()

@router.post("/requests", response_model=schemas.RequestResponse)
def create_request(request: schemas.RequestCreate, db: Session = Depends(get_db), current_user: schemas.UserOut = Depends(get_current_user)):
    return crud.create_request(db=db, request=request)

@router.get("/requests", response_model=list[schemas.RequestResponse])
def read_requests(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: schemas.UserOut = Depends(get_current_user)):
    requests = crud.get_requests(db, skip=skip, limit=limit)
    return requests
