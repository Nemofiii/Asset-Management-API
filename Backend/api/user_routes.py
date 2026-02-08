from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from sqlalchemy import text
from jose import jwt

from Backend.core.database import SessionLocal
from Backend.services import auth_service, coupon_service
from Backend.models.coupon import Coupon
from Backend.api.authenticate import get_current_user


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


        
# Authentication endpoints

@router.post("/register")
def register(email: str, password: str, db:Session = Depends(get_db)):
    return auth_service.register(db, email, password)

@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    token = auth_service.login(db, email, password)
    if not token:
        raise HTTPException(401, "Invalid credentials")
    return {"token": token}

# Coupon endpoints

@router.get("/coupons")
def list_coupons(db: Session = Depends(get_db)):
    return db.query(Coupon).filter(Coupon.status == "ACTIVE").all()

@router.post("/coupons/{coupon_id}/claim")
def claim_coupon(coupon_id: int, user = Depends(get_current_user), db: Session = Depends(get_db)):
    return coupon_service.claim_coupon(db=db, user_id=user["user_id"], coupon_id=coupon_id)

# User history endpoint

@router.get("/users/me/history")
def my_claims(user = Depends(get_current_user), db: Session = Depends(get_db)):
    result = db.execute(text("""SELECT c.code, cl.claimed_at FROM claims cl JOIN coupons c ON cl.coupon_id = c.id WHERE cl.user_id = :uid"""), {"uid": user["user_id"]}).mappings().all()

    return result