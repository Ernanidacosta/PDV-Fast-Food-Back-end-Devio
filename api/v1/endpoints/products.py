from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.products_model import ProductsModel, IngredientsModel, CategoriesModel
from schemas.product_schema import ProductSchema
from core.deps import get_session


router = APIRouter()


# POST Product
@app.post("/products", status_code=201)
async def create_product(
    product: ProductSchema, db: AsyncSession = Depends(get_session)
):
    category = db.query(CategoriesModel).get(product.category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    ingredient = db.query(IngredientsModel).get(product.ingredient_id)
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")

    new_product = ProductsModel(
        name=product.name,
        description=product.description,
        price=product.price,
        available=product.available,
        code=product.code,
        category=category,
        ingredient=ingredient,
    )
    db.add(new_product)
    db.commit()

    return new_product


# GET Products
@router.get('/products', response_model=List[ProductSchema])
async def get_friends(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ProductsModel)
        result = await session.execute(query)
        products: List[ProductsModel] = result.scalars().all()

        return products


# GET Product by ID
@router.get('/products/{id}', response_model=ProductSchema)
async def get_product(id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ProductsModel).filter(ProductsModel.id == id)
        result = await session.execute(query)
        product: ProductsModel = result.scalars().one_or_none()

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        return product
