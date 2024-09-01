from fastapi import FastAPI
from app.api import requests

app = FastAPI()

# Incluye los endpoints
app.include_router(requests.router)
