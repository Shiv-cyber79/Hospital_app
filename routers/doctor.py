from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from models.doctor import Doctor
from schemas.doctor import DoctorCreate
from auth.jwt import get_current_user

router = APIRouter(prefix="/doctors", tags=["Doctors"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_doctor(
    doctor: DoctorCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin only")

    new_doctor = Doctor(**doctor.dict())
    db.add(new_doctor)
    db.commit()
    db.refresh(new_doctor)
    return new_doctor

@router.get("/")
def get_doctors(db: Session = Depends(get_db)):
    return db.query(Doctor).all()