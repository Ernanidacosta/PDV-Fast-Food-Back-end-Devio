from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from client_schema import ClientSchema
from product_schema import ProductSchema


class OrderSchema(BaseModel):
    id: Optional[int]
    amount: float
    user_id: ClientSchema = None
    product_id: ProductSchema = None
    billing_card: Optional[str] = None
    payment_method: Optional[str] = None

    class Config:
        orm_mode = True


class OrderCreateRequest(BaseModel):
    user_id: int
    products: List[int]  # List of product IDs


# Payment Base Model
class PaymentBase(BaseModel):
    amount: float
    payment_date: datetime = datetime.now()


# Money Payment Model
class MoneyPayment(PaymentBase):
    currency: str


# Credit Card Payment Model
class CreditCardPayment(PaymentBase):
    card_number: str


# Debit Card Payment Model
class DebitCardPayment(PaymentBase):
    card_number: str
