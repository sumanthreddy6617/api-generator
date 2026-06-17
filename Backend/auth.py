from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from database import User, get_db
from config import settings

router = APIRouter(prefix="/auth", tags=["auth"])
pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2 = OAuth2PasswordBearer(tokenUrl="auth/login")

class RegisterIn(BaseModel):
    name: str; email: EmailStr; password: str
class LoginIn(BaseModel):
    email: EmailStr; password: str
print(settings.model_dump())
def create_token(uid: int):
    exp = datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRE_MIN, seconds=1400)
    return jwt.encode({"sub": str(uid), "exp": exp}, settings.JWT_SECRET, algorithm=settings.JWT_ALG)

def current_user(token: str = Depends(oauth2), db: Session = Depends(get_db)) -> User:
    cred_exc = HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid credentials")
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALG])
        uid = int(payload.get("sub"))
    except (JWTError, ValueError, TypeError): raise cred_exc
    user = db.query(User).filter(User.id == uid).first()
    if not user: raise cred_exc
    return user

@router.post("/register")
def register(data: RegisterIn, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(400, "Email already registered")
    u = User(name=data.name, email=data.email, password=pwd.hash(data.password))
    db.add(u); db.commit(); db.refresh(u)
    return {"id": u.id, "email": u.email}

@router.post("/login")
def login(data: LoginIn, db: Session = Depends(get_db)):
    u = db.query(User).filter(User.email == data.email).first()
    if not u or not pwd.verify(data.password, u.password):
        raise HTTPException(401, "Invalid email or password")
    return {"access_token": create_token(u.id), "token_type": "bearer",
            "user": {"id": u.id, "name": u.name, "email": u.email}}

@router.get("/me")
def me(u: User = Depends(current_user)):
    return {"id": u.id, "name": u.name, "email": u.email, "created_at": u.created_at}
