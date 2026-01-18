from pydantic import BaseModel
from typing import Optional

class Item(BaseModel):
    id: int
    name: str
    price: float
    description: Optional[str] = None
