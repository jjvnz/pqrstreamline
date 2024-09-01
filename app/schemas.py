from pydantic import BaseModel, EmailStr

class RequestCreate(BaseModel):
    category: str
    description: str

class RequestResponse(RequestCreate):
    id: int
    status: str

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    email: EmailStr
    is_active: bool
    is_verified: bool

