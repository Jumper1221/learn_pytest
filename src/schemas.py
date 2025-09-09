# src/schemas.py
from pydantic import BaseModel, ConfigDict

class ItemBase(BaseModel):
    name: str
    description: str | None = None

class ItemCreate(ItemBase):
    pass

class ItemRead(ItemBase):
    id: int
    
    # Нотация для Pydantic V2
    model_config = ConfigDict(from_attributes=True)