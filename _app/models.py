from sqlalchemy import Column, Integer, String, Float
from .database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    inventory_count = Column(Integer)
    category = Column(String)
    sales_count = Column(Integer, default=0)  # For popularity calculation
