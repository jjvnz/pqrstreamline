from fastapi import FastAPI
from app.api import auth, users
from app.database import engine, Base

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])

Base.metadata.create_all(bind=engine)
