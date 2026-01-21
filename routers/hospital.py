from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from auth.jwt import admin_required
from models.hospital import Hospital
from schemas.hospital import HospitalCreate, HospitalUpdate, HospitalResponse

router = APIRouter(
    prefix="/hospitals",
    tags=["Hospitals"]
)

@router.post("/")
def create_hospital(
    hospital: HospitalCreate,
    db: Session = Depends(get_db),
    admin=Depends(admin_required)
):
    new_hospital = Hospital(**hospital.dict())
    db.add(new_hospital)
    db.commit()
    db.refresh(new_hospital)
    return new_hospital

@router.get("/")
def list_hospitals(db: Session = Depends(get_db)):
    return db.query(Hospital).all()