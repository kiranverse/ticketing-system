from passlib.context import CryptContext
import hashlib

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    sha256_pass = hashlib.sha256(password.encode()).hexdigest()
    return pwd_context.hash(sha256_pass)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    sha256_pass = hashlib.sha256(plain_password.encode()).hexdigest()
    return pwd_context.verify(sha256_pass, hashed_password)