from sqlalchemy import Column, Integer, String
from Backend.core.database import Base

class Coupon(Base):
    __tablename__ = "coupons"

    id = Column(Integer, primary_key=True)
    code = Column(String(100), unique=True)
    available_count = Column(Integer)
    status = Column(String(50))
