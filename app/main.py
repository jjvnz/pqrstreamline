from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, users, requests
from app.database import engine
from app.models import Base
from app.utils import CredentialsException
import logging

app = FastAPI()

# Configuración de CORS (si es necesario)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambia esto a una lista específica de orígenes permitidos en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuración del logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.errors()},
    )

@app.exception_handler(CredentialsException)
async def credentials_exception_handler(request: Request, exc: CredentialsException):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": exc.detail},
    )

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Incluir routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(requests.router)