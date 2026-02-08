from sqlalchemy import Column, Integer, String
from Backend.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True)
    password_hash = Column(String(255))
    role = Column(String(50), default="USER")