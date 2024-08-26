from sqlalchemy import Column, Integer, String, Text, Boolean
from app.database import Base

class Request(Base):
    __tablename__ = 'requests.py'
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, index=True)
    description = Column(Text)
    status = Column(String, default="Received")

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)

