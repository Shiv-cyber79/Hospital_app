from fastapi import APIRouter, Depends,HTTPException,Query
from sqlalchemy.orm import Session
from app.database import SessionLocal
from models.patient import Patient
from auth.jwt import get_current_user
from schemas.patient import PatientCreate,PatientUpdate

router = APIRouter(prefix="/patients", tags=["Patients"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_patient(
    patient: PatientCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    new_patient = Patient(
        user_id=user["user_id"],
        age=patient.age,
        phone=patient.phone,
        address=patient.address
    )
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    return new_patient

@router.get("/List all patients")
def get_patients(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    offset = (page - 1) * limit

    patients = (
        db.query(Patient)
        .offset(offset)
        .limit(limit)
        .all()
    )

    total = db.query(Patient).count()

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "data": patients
    }

@router.get("/retrieve a specific patient")
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    return db.query(Patient).filter(Patient.id == patient_id).first()

@router.put("/{patient_id}")
def update_patient(
    patient_id: int,
    patient: PatientUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    db_patient = db.query(Patient).filter(
        Patient.id == patient_id,
        Patient.user_id == user["user_id"]
    ).first()

    if not db_patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    if patient.age is not None:
        db_patient.age = patient.age

    if patient.phone is not None:
        db_patient.phone = patient.phone

    if patient.address is not None:
        db_patient.address = patient.address

    db.commit()
    db.refresh(db_patient)
    return db_patient
@router.delete("/delete a patient")
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    db.query(Patient).filter(Patient.id == patient_id).delete()
    db.commit()
    return {"message": "Patient deleted"}