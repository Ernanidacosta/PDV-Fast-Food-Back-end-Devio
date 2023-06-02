from typing import Optional, List

from pydantic import BaseModel


class IngredientSchema(BaseModel):
    id: Optional[int]
    name: str
    description: str
    available: bool
    category: str
    ready: bool
    code: str

    class Config:
        orm_mode = True


class ProductSchema(BaseModel):
    id: Optional[int]
    name: str
    description: str
    price: str
    available: bool
    code: str
    ingredient: IngredientSchema = None

    class Config:
        orm_mode = True
