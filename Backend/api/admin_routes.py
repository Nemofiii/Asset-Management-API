from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from Backend.core.database import SessionLocal
from Backend.models.coupon import Coupon
from Backend.api.authenticate import get_current_user, require_admin


router = APIRouter(prefix="/admin", tags=["Admin"])
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# Create coupon endpoint
@router.post("/coupons")
def create_coupon(code: str, available_count: int, db: Session = Depends(get_db), admin=Depends(require_admin)):
    existing = db.query(Coupon).filter(Coupon.code == code).first()
    if existing:
        raise HTTPException(status_code=400, detail="Coupon code already exists")

    coupon = Coupon(code=code, available_count=available_count, status="ACTIVE")
    db.add(coupon)
    db.commit()
    db.refresh(coupon)
    return coupon

# Update coupon endpoint
@router.put("/coupons/{coupon_id}")
def update_coupon(coupon_id: int, code: str = None, available_count: int = None, status: str = None, db: Session = Depends(get_db), admin=Depends(require_admin)):
    coupon = db.query(Coupon).filter(Coupon.id == coupon_id).first()
    if not coupon:
        raise HTTPException(status_code=404, detail="Coupon not found")

    if code:
        existing = db.query(Coupon).filter(Coupon.code == code, Coupon.id != coupon_id).first()
        if existing:
            raise HTTPException(status_code=400, detail="Coupon code already exists")
        coupon.code = code
    if available_count is not None:
        coupon.available_count = available_count
    if status:
        coupon.status = status

    db.commit()
    db.refresh(coupon)
    return coupon

# Delete coupon endpoint
@router.delete("/coupons/{coupon_id}")
def delete_coupon(coupon_id: int, db: Session = Depends(get_db), admin=Depends(require_admin)):
    coupon = db.query(Coupon).filter(Coupon.id == coupon_id).first()
    if not coupon:
        raise HTTPException(status_code=404, detail="Coupon not found")

    db.delete(coupon)
    db.commit()
    return {"detail": "Coupon deleted"}