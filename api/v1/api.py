from fastapi import APIRouter

from api.v1.endpoints import client, card, products, transaction

api_router = APIRouter()
api_router.include_router(client.router, prefix='/client')
api_router.include_router(products.router, prefix='/products')
api_router.include_router(transaction.router, prefix='/transaction')
# api_router.include_router(card.router, prefix='/account')
