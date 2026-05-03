from fastapi import Depends, HTTPException
from jose import jwt
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.user import User
from app.core.jwt import SECRET_KEY, ALGORITHM
from fastapi.security import HTTPBearer

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

def get_current_user(token=Depends(security), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user = db.query(User).filter(User.id == payload["user_id"]).first()
        return user
    except:
        raise HTTPException(status_code=401, detail="Invalid token")
