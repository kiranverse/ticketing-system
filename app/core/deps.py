from fastapi import Depends, HTTPException
from jose import jwt
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.user import User
from app.core.jwt import SECRET_KEY, ALGORITHM, decode_access_token
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.core.logger import get_logger

logger = get_logger(__name__)

security = HTTPBearer()

def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    # 1. Extract token
    token = credentials.credentials

    # 2. Decode token
    payload = decode_access_token(token)

    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    # 3. Extract user_id
    user_id = payload.get("user_id")

    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    # 4. Fetch user from DB
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    logger.info(f"Decoded user_id={user.id}")
    db.close()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # 5. Return user
    return user
