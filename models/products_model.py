from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from core.configs import settings
from sqlalchemy.orm import relationship


class ProductsModel(settings.DBBaseModel):
    __tablename__ = 'products'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String, nullable=False)
    description: str = Column(String, nullaable=True)
    price: str = Column(String(10))
    available: bool = Column(Boolean, default=False)
    ready: bool = Column(Boolean, default=False)
    code: str = Column(String(10))
    category_id: int = Column(Integer, ForeignKey('categories.id'))
    ingredient_id: int = Column(Integer, ForeignKey('ingredients.id'))

    ingredient = relationship('IngredientsModel', back_populates='product')


class IngredientsModel(settings.DBBaseModel):
    __tablename__ = 'ingredients'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String, nullable=False)
    description: str = Column(String, nullaable=True)
    available: bool = Column(Boolean, default=False)

    product = relationship('ProductsModel', back_populates='ingredient')


class CategoriesModel(settings.DBBaseModel):
    __tablename__ = 'categories'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String, nullable=False)
    description: str = Column(String, nullaable=True)
    available: bool = Column(Boolean, default=False)

    product = relationship('ProductsModel', back_populates='category')
