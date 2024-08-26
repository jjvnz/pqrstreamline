from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str
    smtp_server: str
    smtp_port: int
    smtp_user: str = Field(..., alias='SMTP_USER')
    smtp_password: str = Field(..., alias='SMTP_PASSWORD')
    access_token_expire_minutes: int
    frontend_url: str

    class Config:
        env_file = ".env"
        case_sensitive = False  # Si deseas que la carga de variables sea insensible a mayúsculas/minúsculas

settings = Settings()
