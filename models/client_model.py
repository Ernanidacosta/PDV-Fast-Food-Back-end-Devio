from sqlalchemy import Column, Integer, String
from core.configs import settings


class ClientModel(settings.DBBaseModel):
    __tablename__ = 'clients'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String(100))
