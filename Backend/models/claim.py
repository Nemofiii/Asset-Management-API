from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.sql import func
from Backend.core.database import Base

class Claim(Base):
    __tablename__ = "claims"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    coupon_id = Column(Integer, ForeignKey("coupons.id"))
    claimed_at = Column(DateTime, default=func.now())