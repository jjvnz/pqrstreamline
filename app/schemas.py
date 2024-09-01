from pydantic import BaseModel

class RequestCreate(BaseModel):
    category: str
    description: str

class RequestResponse(RequestCreate):
    id: int
    status: str

    class Config:
        from_attributes = True
