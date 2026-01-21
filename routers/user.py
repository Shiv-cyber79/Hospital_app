from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from models.user import User
from schemas.user import UserCreate
from auth.password import hash_password

router = APIRouter(prefix="/users", tags=["Users"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(
        username=user.username,
        hashed_password=hash_password(user.password),
        role="admin"
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "User created"}
