from typing import Optional

from pydantic import BaseModel


class ClientSchema(BaseModel):
    id: Optional[int]
    name: str

    class Config:
        orm_mode = True
