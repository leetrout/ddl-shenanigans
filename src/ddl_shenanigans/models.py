import json

from .dbx import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class AdderSaver:
    """AdderSaver provides convenience methods for adding and saving model
    instances.
    """

    def add(self, session):
        session.add(self)

    def save(self, session):
        self.add(session)
        session.commit()

    def delete(self, session):
        session.delete(self)
        session.commit()

    def to_json(self):
        return json.dumps(
            {k: v for k, v in self.__dict__.items() if not k.startswith("_")}
        )

    @classmethod
    def fields(cls):
        return [k for k in cls.__dict__.keys() if not k.startswith("_")]


class ToppingKind(Base, AdderSaver):
    __tablename__ = "topping_kinds"
    id = Column(Integer, primary_key=True)
    name = Column(String)

class Pizza(Base, AdderSaver):
    __tablename__ = "pizzas"
    id = Column(Integer, primary_key=True)
    name = Column(String)

    toppings = relationship("PizzaTopping", back_populates="pizza")

class PizzaTopping(Base, AdderSaver):
    __tablename__ = "pizza_toppings"
    id = Column(Integer, primary_key=True)
    pizza_id = Column(Integer, ForeignKey("pizzas.id"))
    topping_kind_id = Column(Integer, ForeignKey("topping_kinds.id"))
    topping_allocation = Column(String)


class OrderItem(Base, AdderSaver):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True)
    pizza_id = Column(Integer, ForeignKey("pizzas.id"))


class Order(Base, AdderSaver):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)

    items = relationship("OrderItem", back_populates="order")
