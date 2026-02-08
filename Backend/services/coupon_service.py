from sqlalchemy import text
from sqlalchemy.exc import OperationalError, IntegrityError
from fastapi import HTTPException
from sqlalchemy.orm import Session

def claim_coupon(db: Session, user_id: int, coupon_id: int):
    try:
        
        with db.begin(): 

            coupon = db.execute(text("""SELECT id, available_count FROM coupons WHERE id = :cid FOR UPDATE"""), {"cid": coupon_id}).fetchone()

            if not coupon:
                raise HTTPException(status_code=404, detail="Coupon not found")
            
            if coupon.available_count <= 0:
                raise HTTPException(status_code=409, detail="No coupons available")
            
            db.execute(text("""UPDATE coupons SET available_count = available_count - 1 WHERE id = :cid"""), {"cid": coupon_id})

            db.execute(text("""INSERT INTO claims (user_id, coupon_id) VALUES (:uid, :cid)"""), {"uid": user_id, "cid": coupon_id})
            
            db.execute(text("COMMIT"))
            return {"message": "Coupon claimed successfully"} 

    except (OperationalError, IntegrityError):
        #handles deadlock / lock timeouts safely
        raise HTTPException(status_code=409, detail="Concurrent update, please try again")
