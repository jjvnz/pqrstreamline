from typing import List  # Asegúrate de importar List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter()

@router.post("/requests/", response_model=schemas.RequestResponse)
def create_request(request: schemas.RequestCreate, db: Session = Depends(get_db)):
    return crud.create_request(db=db, request=request)

@router.get("/requests/", response_model=List[schemas.RequestResponse])  # Asegúrate de usar List
def read_requests(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_requests(db=db, skip=skip, limit=limit)
