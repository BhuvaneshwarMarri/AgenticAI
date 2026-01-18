from pydantic import BaseModel
from typing import Optional

class ItemCreate(BaseModel):
    name: str
    price: float
    description: Optional[str] = None


class ItemUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None


class ItemResponse(BaseModel):
    id: int
    name: str
    price: float
    description: Optional[str]

    class Config:
        from_attributes = True