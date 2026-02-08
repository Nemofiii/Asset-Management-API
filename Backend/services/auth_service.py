from sqlalchemy.orm import Session
from passlib.hash import bcrypt
from Backend.models.user import User
from Backend.core.security import create_token, decode_token

def register(db: Session, email: str, password: str):
    hashed_password = bcrypt.hash(password)
    user = User(email=email, password_hash=hashed_password)

    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def login(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()

    if not user or not bcrypt.verify(password, user.password_hash):
        return None
    
    return create_token(user.id, user.role)