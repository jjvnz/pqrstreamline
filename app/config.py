from pydantic_settings import BaseSettings
from pydantic import Field, EmailStr

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str
    smtp_server: str
    smtp_port: int
    smtp_user: EmailStr = Field(..., alias='SMTP_USER')
    smtp_password: str = Field(..., alias='SMTP_PASSWORD')
    access_token_expire_minutes: int
    refresh_token_expire_days: int = 7
    frontend_url: str
    terms_url: str
    base_url: str
    privacy_url: str

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
