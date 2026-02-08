from fastapi import Header, HTTPException, Depends
from Backend.core.security import decode_token


def get_current_user(token: str = Header(...)):
    data = decode_token(token)

    if not data:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return data

def require_admin(user=Depends(get_current_user)):
    if user["role"] != "ADMIN":
        raise HTTPException(status_code=403, detail="Admin access required")
    return user