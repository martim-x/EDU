from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database.connection import Base


class User(Base):
    __tablename__ = "api_users"

    id = Column(Integer, primary_key=True, index=True)
    
    name = Column(String, nullable=False)

    orders = relationship("Order", back_populates="user")


class Product(Base):
    __tablename__ = "api_products"

    id = Column(Integer, primary_key=True, index=True)
    
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    orders = relationship("Order", back_populates="product")


class Order(Base):
    __tablename__ = "api_orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("api_users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("api_products.id"), nullable=False)
    
    quantity = Column(Integer, nullable=False) 
    
    user = relationship("User", back_populates="orders")
    product = relationship("Product", back_populates="orders")
