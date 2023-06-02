from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from core.configs import settings


class PaymentMethodModel(settings.DBBaseModel):
    __tablename__ = 'payment_method'

    id = Column(Integer, primary_key=True)
    pay_method = Column(String(50))


class OrderModel(settings.DBBaseModel):
    __tablename__ = 'transaction'

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('product.id'))
    product_quantity = Column(Integer)
    amount = Column(Float, nullable=True)
    payment_date = Column(DateTime, default=datetime.now, nullable=True)
    payment_method = Column(Integer, ForeignKey('payment_method.id'))
    currency = Column(String(3), nullable=True)
    card_number = Column(String(16), nullable=True)
    user_id = Column(Integer, ForeignKey('user.id'))
