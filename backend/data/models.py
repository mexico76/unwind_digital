from sqlalchemy import (Column, Integer, Date)

from data.db import Base


class Order(Base):
    """Модель Заказов"""
    __tablename__ = "orders"

    number = Column(Integer, nullable=False)
    order_id = Column(Integer, primary_key=True, index=True)
    price_usd = Column(Integer, nullable=False)
    delivery_time = Column(Date, nullable=True)
    price_rub = Column(Integer, nullable=True)

    