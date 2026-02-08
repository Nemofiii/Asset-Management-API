from datetime import datetime, timedelta
from jose import jwt, JWTError

SECRET_KEY = "SECRET123"
ALGORITHM = "HS256"

def create_token(user_id: int, role: str):
    payload = {
        "sub": str(user_id),
        "role": role,
        "exp": datetime.utcnow() + timedelta(hours=2)
        }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")

        if user_id is None:
            return None

        return {
            "user_id": int(payload["sub"]),
            "role": payload["role"]
        }

    except JWTError:
        return None