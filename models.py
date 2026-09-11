from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from database import Base

class ProductPrice(Base):
    __tablename__ = "product_prices"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    price = Column(Float, nullable=False)
    availability = Column(String)
    url = Column(String, unique=True, index=True)
    scraped_at = Column(DateTime, default=datetime.utcnow)