from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.products_model import ProductsModel
from models.order_model import PaymentMethodModel, OrderModel
from models.client_model import ClientModel
from schemas.order_schema import OrderSchema, OrderCreateRequest
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from core.deps import get_session


router = APIRouter()


# GET Products avaiables to order
@router.get(
    '/products',
    status_code=status.HTTP_200_OK,
    response_model=List[ProductsModel],
)
async def get_products(
    page: int = Query(1, gt=0),
    items_per_page: int = Query(12, gt=0),
    db: AsyncSession = Depends(get_session)
):
    total_products = db.query(func.count(ProductsModel.id)).scalar()
    total_pages = (total_products + items_per_page - 1) // items_per_page

    products = db.query(ProductsModel).filter(ProductsModel.available == True)\
        .offset((page - 1) * items_per_page).limit(items_per_page).all()

    return {
        "page": page,
        "total_pages": total_pages,
        "items_per_page": items_per_page,
        "total_products": total_products,
        "products": products,
    }


# POST Order
@router.post('/order', status_code=status.HTTP_201_CREATED, response_model=OrderSchema)
async def post_order(order: OrderCreateRequest, db: AsyncSession = Depends(get_session)):
    
    payment_method_data = order.payment_method

    payment_method = PaymentMethodModel(payment_method=payment_method_data.id)
    db.add(payment_method)
    await db.flush()

    user = db.query(ClientModel).get(order.user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    orders = []
    for product_id in order.products:
        product = db.query(ProductsModel).get(product_id)
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

        new_order = OrderModel(
            user_id=user.id,
            product_id=product_id,
            product_quantity=order.product_quantity,
            payment_date=order.payment_date,
            payment_method=payment_method,
            currency=order.currency,
            card_number=order.card_number,
            ready=order.ready,
        )
        orders.append(new_order)
        db.add(new_order)

    await db.commit()
    return orders


@router.get('/orders', response_model=List[OrderSchema])
async def get_bank_statement(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(OrderModel).options(
            selectinload(OrderModel.billing_card)
        )
        result = await session.execute(query)
        bank_statement: List[OrderModel] = result.scalars().all()

        return bank_statement


# GET transactions by id
@router.get(
    '/order/{orderId}',
    response_model=OrderSchema,
    status_code=status.HTTP_200_OK,
)
async def get_bank_statement_by_id(
    orderId: int, db: AsyncSession = Depends(get_session)
):
    async with db as session:
        query = (
            select(OrderModel)
            .join(OrderModel.payment_method)
            .filter(OrderModel.id == orderId)
            .options(selectinload(OrderModel.payment_method))
        )
        result = await session.execute(query)

        transfer = result.scalar_one_or_none()

        if transfer:
            return transfer

        raise HTTPException(
            detail='Bank statement not found',
            status_code=status.HTTP_404_NOT_FOUND,
        )
