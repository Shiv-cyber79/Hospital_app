from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from models.appointment import Appointment
from schemas.appointment import AppointmentCreate

router = APIRouter(prefix="/appointments", tags=["Appointments"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_appointment(data: AppointmentCreate, db: Session = Depends(get_db)):
    appointment = Appointment(**data.dict())
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment

@router.get("/")
def get_appointments(db: Session = Depends(get_db)):
    return db.query(Appointment).all()
