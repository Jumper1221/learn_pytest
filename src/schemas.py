# src/schemas.py
from pydantic import BaseModel, ConfigDict, field_validator, model_validator


class ItemBase(BaseModel):
    name: str
    description: str | None = None


class ItemCreate(ItemBase):
    @field_validator("name")
    @classmethod
    def name_must_not_be_cursed(cls, v: str) -> str:
        if "cursed" in v.lower():
            raise ValueError("Item name cannot be 'Cursed'")
        return v

    @model_validator(mode="after")
    def name_and_description_cannot_be_the_same(self) -> "ItemCreate":
        if self.name == self.description:
            raise ValueError("Name and description cannot be the same")
        return self


class ItemRead(ItemBase):
    id: int

    # Нотация для Pydantic V2
    model_config = ConfigDict(from_attributes=True)
